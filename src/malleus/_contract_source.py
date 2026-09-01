"""Syntax-neutral retention and recursive import execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from hashlib import sha256
from typing import Any, Protocol, TypeAlias


@dataclass(frozen=True, slots=True)
class ResolverSelection:
    """Exact identity of the selected resolver and its configuration."""

    resolver_id: str
    profile_version: str
    configuration_id: str


@dataclass(frozen=True, slots=True)
class RootRequest:
    """One caller-authored root request."""

    requested_locator: str


@dataclass(frozen=True, slots=True)
class ImportRequest:
    """One ordered import request emitted by an injected reader."""

    parent_module_id: str
    parent_import_ordinal: int
    literal_import: str
    base_locator: str


SourceRequest: TypeAlias = RootRequest | ImportRequest


@dataclass(frozen=True, slots=True)
class ResolvedSource:
    """Exact answer returned by the selected resolver."""

    resolved_locator: str
    source_bytes: bytes
    media_type: str


@dataclass(frozen=True, slots=True)
class RetainedSource:
    """One verified byte-bearing resolver answer."""

    resolved_locator: str
    source_bytes: bytes
    byte_length: int
    sha256: str
    media_type: str
    resolver_selection: ResolverSelection


@dataclass(frozen=True, slots=True)
class RootResolution:
    """Separate provenance for the root request and its exact answer."""

    requested_locator: str
    resolved_locator: str
    source_sha256: str
    resolver_selection: ResolverSelection


@dataclass(frozen=True, slots=True)
class ResolvedImportEdge:
    """One authored import and its exact resolved child."""

    parent_module_id: str
    parent_import_ordinal: int
    literal_import: str
    child_module_id: str
    resolver_selection: ResolverSelection


@dataclass(frozen=True, slots=True)
class ModuleObservation:
    """One exact module locator observed during closure."""

    module_id: str
    source: RetainedSource
    authored_imports: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SourceClosure:
    """One complete immutable retained-source closure."""

    selection: ResolverSelection
    root: RootResolution
    modules: tuple[ModuleObservation, ...]
    import_edges: tuple[ResolvedImportEdge, ...]


class CollaboratorRefusal(ValueError):
    """A selected collaborator refused its exact input."""


class RefusalReason(Enum):
    """Structural reasons the closure executor can refuse."""

    MALFORMED_REQUEST = auto()
    RESOLUTION_REFUSED = auto()
    IMPORT_READER_REFUSED = auto()
    MALFORMED_RESOLVER_RESULT = auto()
    MALFORMED_IMPORT_RESULT = auto()
    LOCATOR_CONTENT_CONFLICT = auto()
    LOCATOR_OBSERVATION_CONFLICT = auto()
    IMPORT_CYCLE = auto()


class SourceBoundaryRefusal(ValueError):
    """Typed atomic refusal with its failed request and locator lineage."""

    def __init__(
        self,
        reason: RefusalReason,
        request: SourceRequest,
        lineage: tuple[str, ...],
    ) -> None:
        self.reason = reason
        self.request = request
        self.lineage = lineage
        super().__init__(reason.name)


class Resolver(Protocol):
    """The sole provider of exact source answers."""

    def resolve(self, request: SourceRequest) -> ResolvedSource:
        """Resolve one root or authored import request."""


class ImportReader(Protocol):
    """An injected reader of ordered authored import literals."""

    def read_imports(self, source: RetainedSource) -> tuple[str, ...]:
        """Read ordered literal imports from exact retained bytes."""


class ClosureOrdering(Protocol):
    """Caller-selected presentation keys for complete closure members."""

    def module_key(self, module: ModuleObservation) -> Any:
        """Return the presentation key for one module."""

    def import_edge_key(self, edge: ResolvedImportEdge) -> Any:
        """Return the presentation key for one import edge."""


@dataclass(frozen=True, slots=True)
class CanonicalOrdering:
    """Default exact-locator and authored-edge presentation order."""

    def module_key(self, module: ModuleObservation) -> str:
        return module.module_id

    def import_edge_key(self, edge: ResolvedImportEdge) -> tuple[str, int, str, str]:
        return (
            edge.parent_module_id,
            edge.parent_import_ordinal,
            edge.literal_import,
            edge.child_module_id,
        )


@dataclass(frozen=True, slots=True)
class TraversalOrdering:
    """Preserve deterministic first-observation and authored-edge order."""

    def module_key(self, module: ModuleObservation) -> int:
        del module
        return 0

    def import_edge_key(self, edge: ResolvedImportEdge) -> int:
        del edge
        return 0


def _refuse(
    reason: RefusalReason,
    request: SourceRequest,
    lineage: tuple[str, ...],
) -> SourceBoundaryRefusal:
    return SourceBoundaryRefusal(reason, request, lineage)


class _ClosureBuilder:
    def __init__(
        self,
        *,
        selection: ResolverSelection,
        resolver: Resolver,
        import_reader: ImportReader,
        ordering: ClosureOrdering,
    ) -> None:
        self.selection = selection
        self.resolver = resolver
        self.import_reader = import_reader
        self.ordering = ordering
        self.retained: dict[str, RetainedSource] = {}
        self.observations: dict[str, ModuleObservation] = {}
        self.observation_order: list[ModuleObservation] = []
        self.edges: list[ResolvedImportEdge] = []

    def resolve(
        self,
        request: SourceRequest,
        lineage: tuple[str, ...],
    ) -> RetainedSource:
        try:
            answer = self.resolver.resolve(request)
        except CollaboratorRefusal as error:
            raise _refuse(
                RefusalReason.RESOLUTION_REFUSED,
                request,
                lineage,
            ) from error
        retained = self._retain(answer, request, lineage)
        prior = self.retained.get(retained.resolved_locator)
        if prior is None:
            self.retained[retained.resolved_locator] = retained
            return retained
        conflict_lineage = lineage + (retained.resolved_locator,)
        if prior.source_bytes != retained.source_bytes:
            raise _refuse(
                RefusalReason.LOCATOR_CONTENT_CONFLICT,
                request,
                conflict_lineage,
            )
        if prior.media_type != retained.media_type:
            raise _refuse(
                RefusalReason.LOCATOR_OBSERVATION_CONFLICT,
                request,
                conflict_lineage,
            )
        return prior

    def _retain(
        self,
        answer: object,
        request: SourceRequest,
        lineage: tuple[str, ...],
    ) -> RetainedSource:
        if type(answer) is not ResolvedSource:
            raise _refuse(
                RefusalReason.MALFORMED_RESOLVER_RESULT,
                request,
                lineage,
            )
        if (
            type(answer.resolved_locator) is not str
            or not answer.resolved_locator
            or type(answer.source_bytes) is not bytes
            or type(answer.media_type) is not str
            or not answer.media_type
        ):
            raise _refuse(
                RefusalReason.MALFORMED_RESOLVER_RESULT,
                request,
                lineage,
            )
        return RetainedSource(
            resolved_locator=answer.resolved_locator,
            source_bytes=answer.source_bytes,
            byte_length=len(answer.source_bytes),
            sha256=f"sha256:{sha256(answer.source_bytes).hexdigest()}",
            media_type=answer.media_type,
            resolver_selection=self.selection,
        )

    def visit(
        self,
        source: RetainedSource,
        request: SourceRequest,
        active: tuple[str, ...],
    ) -> None:
        locator = source.resolved_locator
        lineage = active + (locator,)
        if locator in active:
            raise _refuse(RefusalReason.IMPORT_CYCLE, request, lineage)
        if locator in self.observations:
            return
        try:
            imports = self.import_reader.read_imports(source)
        except CollaboratorRefusal as error:
            raise _refuse(
                RefusalReason.IMPORT_READER_REFUSED,
                request,
                lineage,
            ) from error
        if type(imports) is not tuple or any(
            type(literal) is not str or not literal for literal in imports
        ):
            raise _refuse(
                RefusalReason.MALFORMED_IMPORT_RESULT,
                request,
                lineage,
            )
        observation = ModuleObservation(
            module_id=locator,
            source=source,
            authored_imports=imports,
        )
        self.observations[locator] = observation
        self.observation_order.append(observation)
        for ordinal, literal in enumerate(imports):
            child_request = ImportRequest(
                parent_module_id=locator,
                parent_import_ordinal=ordinal,
                literal_import=literal,
                base_locator=locator,
            )
            child = self.resolve(child_request, lineage)
            self.edges.append(
                ResolvedImportEdge(
                    parent_module_id=locator,
                    parent_import_ordinal=ordinal,
                    literal_import=literal,
                    child_module_id=child.resolved_locator,
                    resolver_selection=self.selection,
                )
            )
            self.visit(child, child_request, lineage)

    def build(self, requested_locator: str) -> SourceClosure:
        root_request = RootRequest(requested_locator=requested_locator)
        if (
            type(requested_locator) is not str
            or not requested_locator
            or type(self.selection) is not ResolverSelection
            or any(
                type(value) is not str or not value
                for value in (
                    self.selection.resolver_id,
                    self.selection.profile_version,
                    self.selection.configuration_id,
                )
            )
        ):
            raise _refuse(RefusalReason.MALFORMED_REQUEST, root_request, ())
        root_source = self.resolve(root_request, ())
        self.visit(root_source, root_request, ())
        return SourceClosure(
            selection=self.selection,
            root=RootResolution(
                requested_locator=requested_locator,
                resolved_locator=root_source.resolved_locator,
                source_sha256=root_source.sha256,
                resolver_selection=self.selection,
            ),
            modules=tuple(sorted(self.observation_order, key=self.ordering.module_key)),
            import_edges=tuple(sorted(self.edges, key=self.ordering.import_edge_key)),
        )


def build_source_closure(
    *,
    requested_locator: str,
    selection: ResolverSelection,
    resolver: Resolver,
    import_reader: ImportReader,
    ordering: ClosureOrdering = CanonicalOrdering(),
) -> SourceClosure:
    """Build one complete closure from explicit collaborators or refuse."""

    return _ClosureBuilder(
        selection=selection,
        resolver=resolver,
        import_reader=import_reader,
        ordering=ordering,
    ).build(requested_locator)
