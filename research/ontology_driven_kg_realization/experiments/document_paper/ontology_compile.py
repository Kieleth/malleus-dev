"""Exact, paper-local LinkML-to-validated-contract compilation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import tempfile

from malleus._contract_binder import BindingRefusal, bind_contract
from malleus._contract_linkml_adapter import (
    LinkMLAdapterRefusal,
    LinkMLImportReader,
    adapt_linkml_closure,
)
from malleus._contract_pipeline import (
    ArtifactRefusal,
    ElaborationRefusal,
    compile_binding,
)
from malleus._contract_pipeline.model import ValidatedContractCompilation
from malleus._contract_source import (
    CollaboratorRefusal,
    ImportRequest,
    ResolvedSource,
    ResolverSelection,
    RootRequest,
    SourceBoundaryRefusal,
    SourceClosure,
    build_source_closure,
)


_DIGEST_PREFIX = "sha256:"
_HEX = frozenset("0123456789abcdef")
_MALLEUS_LOCATOR = "malleus"
_LINKML_TYPES_LOCATOR = "linkml:types"
_MEDIA_TYPE = "application/yaml"
_RECEIPT_GRAMMAR = "malleus.paper-v4.ontology-compilation-receipt/v0"
VALIDATED_CONTRACT_FILENAME = "validated-contract.json"
COMPILE_RECEIPT_FILENAME = "compile-receipt.json"


class CompileStage(str, Enum):
    """One boundary in the exact paper-local compilation."""

    INPUT = "INPUT"
    SOURCE_CLOSURE = "SOURCE_CLOSURE"
    LINKML_ADAPTER = "LINKML_ADAPTER"
    CONTRACT_BINDER = "CONTRACT_BINDER"
    CONTRACT_COMPILER = "CONTRACT_COMPILER"
    PUBLICATION = "PUBLICATION"


class HarnessRefusalReason(str, Enum):
    """Failures owned by this harness rather than the compiler boundaries."""

    MALFORMED_INPUT = "MALFORMED_INPUT"
    SHA256_MISMATCH = "SHA256_MISMATCH"
    OUTPUT_EXISTS = "OUTPUT_EXISTS"
    PUBLICATION_FAILED = "PUBLICATION_FAILED"


def _plain(value: object) -> object:
    if isinstance(value, Enum):
        return value.name
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    if isinstance(value, list):
        return [_plain(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if hasattr(value, "__dataclass_fields__"):
        return {
            name: _plain(getattr(value, name)) for name in value.__dataclass_fields__
        }
    if value is None or type(value) in {bool, int, float, str}:
        return value
    return repr(value)


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _exception_chain(error: BaseException) -> tuple[dict[str, object], ...]:
    chain: list[dict[str, object]] = []
    current: BaseException | None = error
    while current is not None:
        item: dict[str, object] = {
            "message": str(current),
            "type": type(current).__name__,
        }
        for name in (
            "reason",
            "detail",
            "module_id",
            "path",
            "diagnostics",
            "request",
            "lineage",
        ):
            if hasattr(current, name):
                item[name] = _plain(getattr(current, name))
        chain.append(item)
        current = current.__cause__
    return tuple(chain)


class OntologyCompileRefusal(ValueError):
    """Typed stage-specific refusal retaining the complete compiler cause chain."""

    def __init__(
        self,
        stage: CompileStage,
        reason: Enum,
        detail: str,
        *,
        cause: BaseException | None = None,
    ) -> None:
        self.stage = stage
        self.reason = reason
        self.detail = detail
        self.diagnostics = _exception_chain(cause) if cause is not None else ()
        super().__init__(f"{stage.value}:{reason.name}: {detail}")

    def canonical_receipt_bytes(self) -> bytes:
        """Return a deterministic machine-readable refusal receipt."""

        return _canonical_json(
            {
                "diagnostics": list(self.diagnostics),
                "grammar": _RECEIPT_GRAMMAR,
                "reason": self.reason.name,
                "stage": self.stage.value,
                "status": "REFUSED",
            }
        )


@dataclass(frozen=True, slots=True)
class ExactSource:
    """One allowed locator, its exact bytes, and its precommitted digest."""

    locator: str
    source_bytes: bytes
    expected_sha256: str


@dataclass(frozen=True, slots=True)
class ExactOntologyCompilation:
    """Accepted compiler result and the two bytestrings retained by the paper."""

    compilation: ValidatedContractCompilation
    validated_contract_bytes: bytes
    receipt_bytes: bytes


def _digest(source: bytes) -> str:
    return _DIGEST_PREFIX + sha256(source).hexdigest()


def _valid_digest(value: object) -> bool:
    return (
        type(value) is str
        and value.startswith(_DIGEST_PREFIX)
        and len(value) == 71
        and all(character in _HEX for character in value[7:])
    )


def _validate_source(source: object, role: str) -> ExactSource:
    if type(source) is not ExactSource:
        raise OntologyCompileRefusal(
            CompileStage.INPUT,
            HarnessRefusalReason.MALFORMED_INPUT,
            f"{role} must be one ExactSource",
        )
    if type(source.locator) is not str or not source.locator:
        raise OntologyCompileRefusal(
            CompileStage.INPUT,
            HarnessRefusalReason.MALFORMED_INPUT,
            f"{role} locator must be nonblank text",
        )
    if type(source.source_bytes) is not bytes:
        raise OntologyCompileRefusal(
            CompileStage.INPUT,
            HarnessRefusalReason.MALFORMED_INPUT,
            f"{role} source_bytes must be exact bytes",
        )
    if not _valid_digest(source.expected_sha256):
        raise OntologyCompileRefusal(
            CompileStage.INPUT,
            HarnessRefusalReason.MALFORMED_INPUT,
            f"{role} expected_sha256 must be a lowercase sha256 digest",
        )
    actual = _digest(source.source_bytes)
    if actual != source.expected_sha256:
        raise OntologyCompileRefusal(
            CompileStage.INPUT,
            HarnessRefusalReason.SHA256_MISMATCH,
            (
                f"{role} bytes drifted for {source.locator!r}: "
                f"expected {source.expected_sha256}, observed {actual}"
            ),
        )
    return source


class _ExactResolver:
    def __init__(
        self,
        sources: tuple[ExactSource, ExactSource, ExactSource],
    ) -> None:
        self._sources = {source.locator: source for source in sources}

    def resolve(self, request: RootRequest | ImportRequest) -> ResolvedSource:
        locator = (
            request.requested_locator
            if type(request) is RootRequest
            else request.literal_import
        )
        try:
            source = self._sources[locator]
        except KeyError as error:
            raise CollaboratorRefusal(
                f"locator is outside the exact source set: {locator!r}"
            ) from error
        return ResolvedSource(source.locator, source.source_bytes, _MEDIA_TYPE)


def _raise_boundary(stage: CompileStage, error: BaseException) -> None:
    reason = getattr(error, "reason")
    raise OntologyCompileRefusal(
        stage,
        reason,
        str(error),
        cause=error,
    ) from error


def _selection(
    sources: tuple[ExactSource, ExactSource, ExactSource],
) -> ResolverSelection:
    configuration = _digest(
        _canonical_json(
            [
                {
                    "locator": source.locator,
                    "sha256": source.expected_sha256,
                }
                for source in sources
            ]
        )
    )
    return ResolverSelection(
        resolver_id="MALLEUS_PAPER_V4_EXACT_MEMORY_RESOLVER",
        profile_version="MALLEUS_PAPER_V4_EXACT_MEMORY_RESOLVER_V0",
        configuration_id=configuration,
    )


def _compile(
    sources: tuple[ExactSource, ExactSource, ExactSource],
) -> tuple[ValidatedContractCompilation, SourceClosure]:
    selection = _selection(sources)
    try:
        closure = build_source_closure(
            requested_locator=sources[0].locator,
            selection=selection,
            resolver=_ExactResolver(sources),
            import_reader=LinkMLImportReader(),
        )
    except SourceBoundaryRefusal as error:
        _raise_boundary(CompileStage.SOURCE_CLOSURE, error)
    try:
        declared = adapt_linkml_closure(closure)
    except LinkMLAdapterRefusal as error:
        _raise_boundary(CompileStage.LINKML_ADAPTER, error)
    try:
        binding = bind_contract(declared)
    except BindingRefusal as error:
        _raise_boundary(CompileStage.CONTRACT_BINDER, error)
    try:
        return compile_binding(binding), closure
    except (ElaborationRefusal, ArtifactRefusal) as error:
        _raise_boundary(CompileStage.CONTRACT_COMPILER, error)


def _receipt(
    compilation: ValidatedContractCompilation,
    closure: SourceClosure,
) -> bytes:
    artifact = compilation.artifact
    selection = closure.selection
    return _canonical_json(
        {
            "fact_count": artifact.fact_count,
            "facts_sha256": artifact.facts_sha256,
            "grammar": _RECEIPT_GRAMMAR,
            "imports": [
                {
                    "child_module_id": edge.child_module_id,
                    "literal_import": edge.literal_import,
                    "parent_import_ordinal": edge.parent_import_ordinal,
                    "parent_module_id": edge.parent_module_id,
                }
                for edge in closure.import_edges
            ],
            "resolver_selection": {
                "configuration_id": selection.configuration_id,
                "profile_version": selection.profile_version,
                "resolver_id": selection.resolver_id,
            },
            "root": {
                "requested_locator": closure.root.requested_locator,
                "resolved_locator": closure.root.resolved_locator,
                "source_sha256": closure.root.source_sha256,
            },
            "sources": [
                {
                    "byte_length": module.source.byte_length,
                    "media_type": module.source.media_type,
                    "module_id": module.module_id,
                    "sha256": module.source.sha256,
                }
                for module in closure.modules
            ],
            "status": "ACCEPTED",
            "validated_contract_sha256": _digest(artifact.artifact_bytes),
            "validated_fact_set_sha256": artifact.validated_fact_set_sha256,
        }
    )


def compile_exact_ontology(
    *,
    root: ExactSource,
    malleus: ExactSource,
    linkml_types: ExactSource,
) -> ExactOntologyCompilation:
    """Compile only the three precommitted in-memory sources or refuse."""

    sources = (
        _validate_source(root, "root"),
        _validate_source(malleus, "malleus"),
        _validate_source(linkml_types, "linkml_types"),
    )
    if malleus.locator != _MALLEUS_LOCATOR:
        raise OntologyCompileRefusal(
            CompileStage.INPUT,
            HarnessRefusalReason.MALFORMED_INPUT,
            f"malleus locator must be {_MALLEUS_LOCATOR!r}",
        )
    if linkml_types.locator != _LINKML_TYPES_LOCATOR:
        raise OntologyCompileRefusal(
            CompileStage.INPUT,
            HarnessRefusalReason.MALFORMED_INPUT,
            f"linkml_types locator must be {_LINKML_TYPES_LOCATOR!r}",
        )
    locators = tuple(source.locator for source in sources)
    if len(set(locators)) != len(locators):
        raise OntologyCompileRefusal(
            CompileStage.INPUT,
            HarnessRefusalReason.MALFORMED_INPUT,
            "root, malleus, and linkml_types locators must be distinct",
        )
    compilation, closure = _compile(sources)
    artifact_bytes = compilation.artifact.artifact_bytes
    return ExactOntologyCompilation(
        compilation=compilation,
        validated_contract_bytes=artifact_bytes,
        receipt_bytes=_receipt(compilation, closure),
    )


def _write_exclusive(path: Path, source: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(source)
        stream.flush()
        os.fsync(stream.fileno())


def publish_compilation(
    result: ExactOntologyCompilation,
    output_directory: Path,
) -> Path:
    """Publish both outputs through one staged directory rename, without overwrite."""

    if type(result) is not ExactOntologyCompilation or not isinstance(
        output_directory, Path
    ):
        raise OntologyCompileRefusal(
            CompileStage.PUBLICATION,
            HarnessRefusalReason.MALFORMED_INPUT,
            "publication requires ExactOntologyCompilation and Path inputs",
        )
    if output_directory.exists() or output_directory.is_symlink():
        raise OntologyCompileRefusal(
            CompileStage.PUBLICATION,
            HarnessRefusalReason.OUTPUT_EXISTS,
            f"output directory already exists: {output_directory}",
        )
    parent = output_directory.parent
    if not parent.is_dir() or parent.is_symlink():
        raise OntologyCompileRefusal(
            CompileStage.PUBLICATION,
            HarnessRefusalReason.MALFORMED_INPUT,
            f"output parent must be an existing non-symlink directory: {parent}",
        )
    staged = Path(tempfile.mkdtemp(prefix=f".{output_directory.name}.", dir=parent))
    try:
        _write_exclusive(
            staged / VALIDATED_CONTRACT_FILENAME,
            result.validated_contract_bytes,
        )
        _write_exclusive(staged / COMPILE_RECEIPT_FILENAME, result.receipt_bytes)
        if output_directory.exists() or output_directory.is_symlink():
            raise OntologyCompileRefusal(
                CompileStage.PUBLICATION,
                HarnessRefusalReason.OUTPUT_EXISTS,
                f"output directory appeared during publication: {output_directory}",
            )
        staged.rename(output_directory)
    except OntologyCompileRefusal:
        shutil.rmtree(staged, ignore_errors=True)
        raise
    except OSError as error:
        shutil.rmtree(staged, ignore_errors=True)
        reason = (
            HarnessRefusalReason.OUTPUT_EXISTS
            if output_directory.exists() or output_directory.is_symlink()
            else HarnessRefusalReason.PUBLICATION_FAILED
        )
        raise OntologyCompileRefusal(
            CompileStage.PUBLICATION,
            reason,
            str(error),
            cause=error,
        ) from error
    return output_directory


__all__ = [
    "COMPILE_RECEIPT_FILENAME",
    "VALIDATED_CONTRACT_FILENAME",
    "CompileStage",
    "ExactOntologyCompilation",
    "ExactSource",
    "HarnessRefusalReason",
    "OntologyCompileRefusal",
    "compile_exact_ontology",
    "publish_compilation",
]
