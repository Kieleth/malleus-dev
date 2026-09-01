from __future__ import annotations

import ast
import builtins
from dataclasses import FrozenInstanceError, dataclass, fields, is_dataclass
from hashlib import sha256
import inspect
from pathlib import Path
import socket
import subprocess
from typing import Any
from urllib import request as url_request

import pytest

from malleus._contract_source import (
    CanonicalOrdering,
    CollaboratorRefusal,
    ClosureOrdering,
    ImportReader,
    ImportRequest,
    ModuleObservation,
    RefusalReason,
    ResolvedImportEdge,
    ResolvedSource,
    Resolver,
    ResolverSelection,
    RetainedSource,
    RootRequest,
    RootResolution,
    SourceBoundaryRefusal,
    SourceClosure,
    TraversalOrdering,
    build_source_closure,
)


ROOT = Path(__file__).resolve().parents[2]
CORRECTED_RED_COMMIT = "8a297ed84fb15e96dfd4ef73a4db8475b86225de"
CORRECTED_GREEN_COMMIT = "16d11cc0a6ad2ac944e6fe2d87d174bb23190a24"
CORRECTED_RED_TEST_BLOB = "38aa69ce63a97a29c04c1e96405a5e09ef9f7d77"
MODULE_PATH = "src/malleus/_contract_source.py"
TEST_PATH = "tests/contract_compiler/test_retained_source_boundary.py"
SELECTION = ResolverSelection(
    resolver_id="TEST_ONLY_MEMORY_RESOLVER",
    profile_version="TEST_ONLY_PROFILE_V0",
    configuration_id="TEST_ONLY_CONFIGURATION_V0",
)


class _MemoryResolver:
    def __init__(
        self,
        routes: dict[str, ResolvedSource | tuple[ResolvedSource, ...]],
        *,
        refused: frozenset[str] = frozenset(),
    ) -> None:
        self.routes = routes
        self.refused = refused
        self.requests: list[RootRequest | ImportRequest] = []
        self._counts: dict[str, int] = {}

    def resolve(self, request: RootRequest | ImportRequest) -> ResolvedSource:
        self.requests.append(request)
        locator = (
            request.requested_locator
            if isinstance(request, RootRequest)
            else request.literal_import
        )
        if locator in self.refused:
            raise CollaboratorRefusal(f"refused {locator}")
        result = self.routes[locator]
        if isinstance(result, tuple):
            index = self._counts.get(locator, 0)
            self._counts[locator] = index + 1
            return result[index]
        return result


class _MemoryImportReader:
    def __init__(
        self,
        imports: dict[str, tuple[str, ...]],
        *,
        refused: frozenset[str] = frozenset(),
    ) -> None:
        self.imports = imports
        self.refused = refused
        self.sources: list[RetainedSource] = []

    def read_imports(self, source: RetainedSource) -> tuple[str, ...]:
        self.sources.append(source)
        if source.resolved_locator in self.refused:
            raise CollaboratorRefusal(f"cannot inspect {source.resolved_locator}")
        return self.imports[source.resolved_locator]


def _source(
    locator: str, content: bytes, media_type: str = "test/type"
) -> ResolvedSource:
    return ResolvedSource(
        resolved_locator=locator,
        source_bytes=content,
        media_type=media_type,
    )


def _build(
    resolver: Resolver,
    reader: ImportReader,
    requested_locator: str = "root",
    ordering: ClosureOrdering = CanonicalOrdering(),
) -> SourceClosure:
    return build_source_closure(
        requested_locator=requested_locator,
        selection=SELECTION,
        resolver=resolver,
        import_reader=reader,
        ordering=ordering,
    )


def _module(closure: SourceClosure, locator: str) -> ModuleObservation:
    return next(module for module in closure.modules if module.module_id == locator)


def _assert_no_partial_result(refusal: SourceBoundaryRefusal) -> None:
    assert not hasattr(refusal, "closure")
    assert not hasattr(refusal, "sources")
    assert not hasattr(refusal, "modules")
    assert not hasattr(refusal, "edges")


def _assert_deeply_immutable(value: object) -> None:
    if is_dataclass(value):
        for field in fields(value):
            _assert_deeply_immutable(getattr(value, field.name))
        return
    if isinstance(value, tuple):
        for item in value:
            _assert_deeply_immutable(item)
        return
    assert isinstance(value, (bytes, int, str))


def test_retained_source_boundary_exposes_the_authorized_private_api() -> None:
    assert all(
        value is not None
        for value in (
            CanonicalOrdering,
            CollaboratorRefusal,
            ClosureOrdering,
            ImportReader,
            ImportRequest,
            ModuleObservation,
            RefusalReason,
            ResolvedImportEdge,
            ResolvedSource,
            Resolver,
            ResolverSelection,
            RetainedSource,
            RootRequest,
            RootResolution,
            SourceBoundaryRefusal,
            SourceClosure,
            TraversalOrdering,
            build_source_closure,
        )
    )


def test_root_retains_exact_bytes_metadata_and_separate_provenance() -> None:
    content = b"first\nsecond  \n"
    resolver = _MemoryResolver({"requested": _source("module:root", content)})
    reader = _MemoryImportReader({"module:root": ()})

    closure = _build(resolver, reader, "requested")

    retained = closure.modules[0].source
    assert closure.selection is SELECTION
    assert closure.root == RootResolution(
        requested_locator="requested",
        resolved_locator="module:root",
        source_sha256=f"sha256:{sha256(content).hexdigest()}",
        resolver_selection=SELECTION,
    )
    assert retained == RetainedSource(
        resolved_locator="module:root",
        source_bytes=content,
        byte_length=len(content),
        sha256=f"sha256:{sha256(content).hexdigest()}",
        media_type="test/type",
        resolver_selection=SELECTION,
    )
    assert reader.sources == [retained]
    assert closure.modules == (
        ModuleObservation(
            module_id="module:root",
            source=retained,
            authored_imports=(),
        ),
    )
    assert closure.import_edges == ()
    assert not hasattr(closure.root, "parent_module_id")
    assert not hasattr(closure.root, "parent_import_ordinal")
    assert not hasattr(closure.root, "literal_import")


def test_nested_diamond_resolves_every_edge_and_observes_each_locator_once() -> None:
    common = _source("module:common", b"common")
    resolver = _MemoryResolver(
        {
            "root": _source("module:root", b"root"),
            "left": _source("module:left", b"left"),
            "right": _source("module:right", b"right"),
            "common": (common, common),
        }
    )
    reader = _MemoryImportReader(
        {
            "module:root": ("left", "right"),
            "module:left": ("common",),
            "module:right": ("common",),
            "module:common": (),
        }
    )

    closure = _build(resolver, reader)

    assert [
        request.literal_import
        for request in resolver.requests
        if isinstance(request, ImportRequest)
    ] == ["left", "common", "right", "common"]
    assert [module.module_id for module in closure.modules] == [
        "module:common",
        "module:left",
        "module:right",
        "module:root",
    ]
    assert [source.resolved_locator for source in reader.sources] == [
        "module:root",
        "module:left",
        "module:common",
        "module:right",
    ]
    assert all(
        module.source.resolver_selection is SELECTION for module in closure.modules
    )
    assert all(edge.resolver_selection is SELECTION for edge in closure.import_edges)
    assert closure.import_edges == (
        ResolvedImportEdge(
            parent_module_id="module:left",
            parent_import_ordinal=0,
            literal_import="common",
            child_module_id="module:common",
            resolver_selection=SELECTION,
        ),
        ResolvedImportEdge(
            parent_module_id="module:right",
            parent_import_ordinal=0,
            literal_import="common",
            child_module_id="module:common",
            resolver_selection=SELECTION,
        ),
        ResolvedImportEdge(
            parent_module_id="module:root",
            parent_import_ordinal=0,
            literal_import="left",
            child_module_id="module:left",
            resolver_selection=SELECTION,
        ),
        ResolvedImportEdge(
            parent_module_id="module:root",
            parent_import_ordinal=1,
            literal_import="right",
            child_module_id="module:right",
            resolver_selection=SELECTION,
        ),
    )
    requests = [
        request for request in resolver.requests if isinstance(request, ImportRequest)
    ]
    assert requests[0] == ImportRequest(
        parent_module_id="module:root",
        parent_import_ordinal=0,
        literal_import="left",
        base_locator="module:root",
    )
    assert requests[1] == ImportRequest(
        parent_module_id="module:left",
        parent_import_ordinal=0,
        literal_import="common",
        base_locator="module:left",
    )


def test_duplicate_authored_imports_keep_zero_based_ordinals_and_both_edges() -> None:
    child = _source("module:child", b"child")
    resolver = _MemoryResolver(
        {
            "root": _source("module:root", b"root"),
            "repeat": (child, child),
        }
    )
    reader = _MemoryImportReader(
        {
            "module:root": ("repeat", "repeat"),
            "module:child": (),
        }
    )

    closure = _build(resolver, reader)

    child_requests = [
        request for request in resolver.requests if isinstance(request, ImportRequest)
    ]
    assert [request.parent_import_ordinal for request in child_requests] == [0, 1]
    assert len(closure.import_edges) == 2
    assert [edge.parent_import_ordinal for edge in closure.import_edges] == [0, 1]
    assert [source.resolved_locator for source in reader.sources].count(
        "module:child"
    ) == 1


def test_ordering_changes_only_tuple_presentation() -> None:
    routes = {
        "root": _source("module:root", b"root"),
        "left": _source("module:left", b"left"),
        "right": _source("module:right", b"right"),
        "common": _source("module:common", b"common"),
    }
    imports = {
        "module:root": ("left", "right"),
        "module:left": ("common",),
        "module:right": ("common",),
        "module:common": (),
    }

    canonical = _build(_MemoryResolver(routes), _MemoryImportReader(imports))
    traversal = _build(
        _MemoryResolver({**routes, "common": (routes["common"], routes["common"])}),
        _MemoryImportReader(imports),
        ordering=TraversalOrdering(),
    )

    assert [module.module_id for module in canonical.modules] == [
        "module:common",
        "module:left",
        "module:right",
        "module:root",
    ]
    assert [module.module_id for module in traversal.modules] == [
        "module:root",
        "module:left",
        "module:common",
        "module:right",
    ]
    assert [
        (edge.parent_module_id, edge.parent_import_ordinal)
        for edge in traversal.import_edges
    ] == [
        ("module:root", 0),
        ("module:left", 0),
        ("module:root", 1),
        ("module:right", 0),
    ]
    assert frozenset(canonical.modules) == frozenset(traversal.modules)
    assert frozenset(canonical.import_edges) == frozenset(traversal.import_edges)

    class CallerOrdering:
        def module_key(self, module: ModuleObservation) -> int:
            return {
                "module:right": 0,
                "module:root": 1,
                "module:left": 2,
                "module:common": 3,
            }[module.module_id]

        def import_edge_key(self, edge: ResolvedImportEdge) -> int:
            return {
                ("module:right", 0): 0,
                ("module:root", 1): 1,
                ("module:root", 0): 2,
                ("module:left", 0): 3,
            }[(edge.parent_module_id, edge.parent_import_ordinal)]

    custom = _build(
        _MemoryResolver({**routes, "common": (routes["common"], routes["common"])}),
        _MemoryImportReader(imports),
        ordering=CallerOrdering(),
    )
    assert [module.module_id for module in custom.modules] == [
        "module:right",
        "module:root",
        "module:left",
        "module:common",
    ]
    assert [
        (edge.parent_module_id, edge.parent_import_ordinal)
        for edge in custom.import_edges
    ] == [
        ("module:right", 0),
        ("module:root", 1),
        ("module:root", 0),
        ("module:left", 0),
    ]
    assert frozenset(custom.modules) == frozenset(canonical.modules)
    assert frozenset(custom.import_edges) == frozenset(canonical.import_edges)


def test_one_selected_resolver_refusal_has_no_fallback_or_partial_result() -> None:
    resolver = _MemoryResolver(
        {"root": _source("module:root", b"root")},
        refused=frozenset({"root"}),
    )
    reader = _MemoryImportReader({})

    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(resolver, reader)

    refusal = caught.value
    assert refusal.reason is RefusalReason.RESOLUTION_REFUSED
    assert refusal.request == RootRequest(requested_locator="root")
    assert refusal.lineage == ()
    assert len(resolver.requests) == 1
    assert reader.sources == []
    assert list(inspect.signature(build_source_closure).parameters) == [
        "requested_locator",
        "selection",
        "resolver",
        "import_reader",
        "ordering",
    ]
    _assert_no_partial_result(refusal)


def test_import_reader_refusal_has_exact_lineage_and_no_partial_result() -> None:
    resolver = _MemoryResolver({"root": _source("module:root", b"root")})
    reader = _MemoryImportReader(
        {"module:root": ()},
        refused=frozenset({"module:root"}),
    )

    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(resolver, reader)

    refusal = caught.value
    assert refusal.reason is RefusalReason.IMPORT_READER_REFUSED
    assert refusal.request == RootRequest(requested_locator="root")
    assert refusal.lineage == ("module:root",)
    _assert_no_partial_result(refusal)


def test_nested_collaborator_refusals_keep_the_failed_request_and_lineage() -> None:
    root = _source("module:root", b"root")
    child = _source("module:child", b"child")
    reader = _MemoryImportReader({"module:root": ("child",)})
    resolver = _MemoryResolver(
        {"root": root, "child": child},
        refused=frozenset({"child"}),
    )

    with pytest.raises(SourceBoundaryRefusal) as resolver_caught:
        _build(resolver, reader)

    resolver_refusal = resolver_caught.value
    assert resolver_refusal.reason is RefusalReason.RESOLUTION_REFUSED
    assert resolver_refusal.request == ImportRequest(
        parent_module_id="module:root",
        parent_import_ordinal=0,
        literal_import="child",
        base_locator="module:root",
    )
    assert resolver_refusal.lineage == ("module:root",)
    _assert_no_partial_result(resolver_refusal)

    with pytest.raises(SourceBoundaryRefusal) as reader_caught:
        _build(
            _MemoryResolver({"root": root, "child": child}),
            _MemoryImportReader(
                {"module:root": ("child",), "module:child": ()},
                refused=frozenset({"module:child"}),
            ),
        )

    reader_refusal = reader_caught.value
    assert reader_refusal.reason is RefusalReason.IMPORT_READER_REFUSED
    assert isinstance(reader_refusal.request, ImportRequest)
    assert reader_refusal.request.literal_import == "child"
    assert reader_refusal.lineage == ("module:root", "module:child")
    _assert_no_partial_result(reader_refusal)


def test_unexpected_collaborator_errors_are_not_reclassified() -> None:
    resolver_error = RuntimeError("resolver bug")

    class BrokenResolver:
        def resolve(self, request: RootRequest | ImportRequest) -> ResolvedSource:
            del request
            raise resolver_error

    with pytest.raises(RuntimeError) as resolver_caught:
        _build(BrokenResolver(), _MemoryImportReader({}))
    assert resolver_caught.value is resolver_error

    reader_error = RuntimeError("reader bug")

    class BrokenReader:
        def read_imports(self, source: RetainedSource) -> tuple[str, ...]:
            del source
            raise reader_error

    with pytest.raises(RuntimeError) as reader_caught:
        _build(
            _MemoryResolver({"root": _source("module:root", b"root")}),
            BrokenReader(),
        )
    assert reader_caught.value is reader_error


def test_same_locator_with_different_bytes_refuses_the_whole_closure() -> None:
    resolver = _MemoryResolver(
        {
            "root": _source("module:root", b"root"),
            "left": _source("module:left", b"left"),
            "right": _source("module:right", b"right"),
            "first-common": _source("module:common", b"first"),
            "second-common": _source("module:common", b"second"),
        }
    )
    reader = _MemoryImportReader(
        {
            "module:root": ("left", "right"),
            "module:left": ("first-common",),
            "module:right": ("second-common",),
            "module:common": (),
        }
    )

    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(resolver, reader)

    refusal = caught.value
    assert refusal.reason is RefusalReason.LOCATOR_CONTENT_CONFLICT
    assert refusal.request == ImportRequest(
        parent_module_id="module:right",
        parent_import_ordinal=0,
        literal_import="second-common",
        base_locator="module:right",
    )
    assert refusal.lineage == ("module:root", "module:right", "module:common")
    _assert_no_partial_result(refusal)


def test_same_locator_and_bytes_with_different_media_type_refuses() -> None:
    resolver = _MemoryResolver(
        {
            "root": _source("module:root", b"root"),
            "first": _source("module:shared", b"same", "type:first"),
            "second": _source("module:shared", b"same", "type:second"),
        }
    )
    reader = _MemoryImportReader(
        {
            "module:root": ("first", "second"),
            "module:shared": (),
        }
    )

    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(resolver, reader)

    refusal = caught.value
    assert refusal.reason is RefusalReason.LOCATOR_OBSERVATION_CONFLICT
    assert isinstance(refusal.request, ImportRequest)
    assert refusal.request.literal_import == "second"
    assert refusal.lineage == ("module:root", "module:shared")
    _assert_no_partial_result(refusal)


def test_source_conflict_precedes_cycle_classification() -> None:
    resolver = _MemoryResolver(
        {
            "root": _source("module:root", b"root"),
            "child": _source("module:child", b"child"),
            "back": _source("module:root", b"changed"),
        }
    )
    reader = _MemoryImportReader(
        {
            "module:root": ("child",),
            "module:child": ("back",),
        }
    )

    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(resolver, reader)

    refusal = caught.value
    assert refusal.reason is RefusalReason.LOCATOR_CONTENT_CONFLICT
    assert refusal.lineage == ("module:root", "module:child", "module:root")
    _assert_no_partial_result(refusal)


def test_media_type_conflict_also_precedes_cycle_classification() -> None:
    resolver = _MemoryResolver(
        {
            "root": _source("module:root", b"root", "type:first"),
            "child": _source("module:child", b"child"),
            "back": _source("module:root", b"root", "type:second"),
        }
    )
    reader = _MemoryImportReader(
        {
            "module:root": ("child",),
            "module:child": ("back",),
        }
    )

    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(resolver, reader)

    refusal = caught.value
    assert refusal.reason is RefusalReason.LOCATOR_OBSERVATION_CONFLICT
    assert refusal.lineage == ("module:root", "module:child", "module:root")
    _assert_no_partial_result(refusal)


def test_distinct_locators_with_identical_bytes_remain_distinct() -> None:
    shared = b"same"
    resolver = _MemoryResolver(
        {
            "root": _source("module:root", b"root"),
            "first": _source("module:first", shared),
            "second": _source("module:second", shared),
        }
    )
    reader = _MemoryImportReader(
        {
            "module:root": ("first", "second"),
            "module:first": (),
            "module:second": (),
        }
    )

    closure = _build(resolver, reader)

    first = _module(closure, "module:first")
    second = _module(closure, "module:second")
    assert first.source.sha256 == second.source.sha256
    assert first.module_id != second.module_id
    assert first.source.resolved_locator != second.source.resolved_locator
    assert len(closure.modules) == 3


def test_bytes_are_opaque_and_resolved_locators_are_never_normalized() -> None:
    opaque = b"\xff\x00trailing  \n"
    resolver = _MemoryResolver(
        {
            "root": _source("root", b"root"),
            "first": _source("x", opaque),
            "second": _source("./x", opaque),
        }
    )
    reader = _MemoryImportReader(
        {
            "root": ("first", "second"),
            "x": (),
            "./x": (),
        }
    )

    closure = _build(resolver, reader)

    first = _module(closure, "x").source
    second = _module(closure, "./x").source
    assert first.source_bytes == opaque
    assert first.byte_length == len(opaque)
    assert first.sha256 == f"sha256:{sha256(opaque).hexdigest()}"
    assert second.source_bytes == opaque
    assert first.resolved_locator == "x"
    assert second.resolved_locator == "./x"


@pytest.mark.parametrize(
    ("routes", "imports", "expected_lineage"),
    [
        (
            {
                "root": _source("module:root", b"root"),
                "self": _source("module:root", b"root"),
            },
            {"module:root": ("self",)},
            ("module:root", "module:root"),
        ),
        (
            {
                "root": _source("module:root", b"root"),
                "child": _source("module:child", b"child"),
                "back": _source("module:root", b"root"),
            },
            {"module:root": ("child",), "module:child": ("back",)},
            ("module:root", "module:child", "module:root"),
        ),
        (
            {
                "root": _source("module:root", b"root"),
                "middle": _source("module:middle", b"middle"),
                "leaf": _source("module:leaf", b"leaf"),
                "back": _source("module:root", b"root"),
            },
            {
                "module:root": ("middle",),
                "module:middle": ("leaf",),
                "module:leaf": ("back",),
            },
            ("module:root", "module:middle", "module:leaf", "module:root"),
        ),
    ],
)
def test_every_directed_cycle_refuses_with_exact_locator_lineage(
    routes: dict[str, ResolvedSource],
    imports: dict[str, tuple[str, ...]],
    expected_lineage: tuple[str, ...],
) -> None:
    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(_MemoryResolver(routes), _MemoryImportReader(imports))

    refusal = caught.value
    assert refusal.reason is RefusalReason.IMPORT_CYCLE
    assert refusal.lineage == expected_lineage
    assert isinstance(refusal.request, ImportRequest)
    _assert_no_partial_result(refusal)


def test_deep_acyclic_chain_has_no_host_recursion_boundary() -> None:
    module_count = 1_201
    routes = {"root": _source("module:0000", b"0")}
    imports: dict[str, tuple[str, ...]] = {}
    for index in range(module_count):
        module = f"module:{index:04d}"
        if index + 1 == module_count:
            imports[module] = ()
            continue
        literal = f"next:{index + 1:04d}"
        routes[literal] = _source(f"module:{index + 1:04d}", str(index + 1).encode())
        imports[module] = (literal,)

    closure = _build(_MemoryResolver(routes), _MemoryImportReader(imports))

    assert len(closure.modules) == module_count
    assert len(closure.import_edges) == module_count - 1
    assert closure.root.resolved_locator == "module:0000"
    assert closure.import_edges[0].parent_module_id == "module:0000"
    assert closure.import_edges[-1].child_module_id == "module:1200"


@pytest.mark.parametrize(
    "result",
    [
        object(),
        ResolvedSource("", b"root", "test/type"),
        ResolvedSource(7, b"root", "test/type"),
        ResolvedSource("module:root", bytearray(b"root"), "test/type"),
        ResolvedSource("module:root", b"root", ""),
        ResolvedSource("module:root", b"root", 7),
    ],
)
def test_malformed_resolver_results_refuse_atomically(result: Any) -> None:
    class MalformedResolver:
        def resolve(self, request: RootRequest | ImportRequest) -> Any:
            del request
            return result

    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(MalformedResolver(), _MemoryImportReader({}))

    refusal = caught.value
    assert refusal.reason is RefusalReason.MALFORMED_RESOLVER_RESULT
    assert refusal.request == RootRequest(requested_locator="root")
    assert refusal.lineage == ()
    _assert_no_partial_result(refusal)


def test_resolver_result_subclasses_refuse_before_field_access() -> None:
    class PoisonResolvedSource(ResolvedSource):
        def __getattribute__(self, name: str) -> Any:
            if name in {"resolved_locator", "source_bytes", "media_type"}:
                raise AssertionError("subclass field was read")
            return super().__getattribute__(name)

    result = PoisonResolvedSource("module:root", b"root", "test/type")

    class ExtendedResultResolver:
        def resolve(self, request: RootRequest | ImportRequest) -> PoisonResolvedSource:
            del request
            return result

    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(ExtendedResultResolver(), _MemoryImportReader({}))

    assert caught.value.reason is RefusalReason.MALFORMED_RESOLVER_RESULT
    _assert_no_partial_result(caught.value)


@pytest.mark.parametrize("imports", [[], ("",), (b"child",)])
def test_malformed_import_reader_results_refuse_atomically(imports: Any) -> None:
    class MalformedReader:
        def read_imports(self, source: RetainedSource) -> Any:
            del source
            return imports

    resolver = _MemoryResolver({"root": _source("module:root", b"root")})

    with pytest.raises(SourceBoundaryRefusal) as caught:
        _build(resolver, MalformedReader())

    refusal = caught.value
    assert refusal.reason is RefusalReason.MALFORMED_IMPORT_RESULT
    assert refusal.request == RootRequest(requested_locator="root")
    assert refusal.lineage == ("module:root",)
    _assert_no_partial_result(refusal)


@pytest.mark.parametrize(
    ("requested_locator", "selection"),
    [
        ("", SELECTION),
        (b"root", SELECTION),
        (
            "root",
            ResolverSelection(
                resolver_id="",
                profile_version="TEST_ONLY_PROFILE_V0",
                configuration_id="TEST_ONLY_CONFIGURATION_V0",
            ),
        ),
        ("root", object()),
    ],
)
def test_malformed_root_or_selection_refuses_before_resolution(
    requested_locator: Any,
    selection: Any,
) -> None:
    resolver = _MemoryResolver({"root": _source("module:root", b"root")})

    with pytest.raises(SourceBoundaryRefusal) as caught:
        build_source_closure(
            requested_locator=requested_locator,
            selection=selection,
            resolver=resolver,
            import_reader=_MemoryImportReader({}),
        )

    refusal = caught.value
    assert refusal.reason is RefusalReason.MALFORMED_REQUEST
    assert refusal.lineage == ()
    assert resolver.requests == []
    _assert_no_partial_result(refusal)


def test_resolver_selection_subclasses_cannot_add_mutable_state() -> None:
    @dataclass(frozen=True)
    class ExtendedSelection(ResolverSelection):
        mutable: list[str]

    selection = ExtendedSelection(
        resolver_id="TEST_ONLY_MEMORY_RESOLVER",
        profile_version="TEST_ONLY_PROFILE_V0",
        configuration_id="TEST_ONLY_CONFIGURATION_V0",
        mutable=[],
    )
    resolver = _MemoryResolver({"root": _source("module:root", b"root")})

    with pytest.raises(SourceBoundaryRefusal) as caught:
        build_source_closure(
            requested_locator="root",
            selection=selection,
            resolver=resolver,
            import_reader=_MemoryImportReader({}),
        )

    assert caught.value.reason is RefusalReason.MALFORMED_REQUEST
    assert resolver.requests == []
    _assert_no_partial_result(caught.value)


def test_successful_closure_is_deeply_immutable_and_repeatable() -> None:
    routes = {
        "root": _source("module:root", b"root"),
        "child": _source("module:child", b"child"),
    }
    imports = {"module:root": ("child",), "module:child": ()}

    first = _build(_MemoryResolver(routes), _MemoryImportReader(imports))
    second = _build(_MemoryResolver(routes), _MemoryImportReader(imports))

    assert first == second
    _assert_deeply_immutable(first)
    with pytest.raises(FrozenInstanceError):
        first.root = RootResolution("other", "other", "other", SELECTION)
    with pytest.raises(FrozenInstanceError):
        first.modules[0].source = RetainedSource(
            "other", b"", 0, "other", "other", SELECTION
        )


def test_executor_uses_only_injected_collaborators(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("executor attempted ambient I/O")

    monkeypatch.setattr(builtins, "open", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)
    monkeypatch.setattr(Path, "read_bytes", forbidden)
    monkeypatch.setattr(Path, "read_text", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(url_request, "urlopen", forbidden)

    closure = _build(
        _MemoryResolver({"root": _source("module:root", b"root")}),
        _MemoryImportReader({"module:root": ()}),
    )

    assert closure.root.resolved_locator == "module:root"


def test_production_source_is_syntax_and_transport_neutral() -> None:
    source = (ROOT / "src/malleus/_contract_source.py").read_text(encoding="utf-8")

    for forbidden in (
        "linkml",
        "yaml",
        "quiet bell",
        "greenhouse",
        "pathlib",
        "socket",
        "urllib",
        "requests",
        "network",
        "fixture",
    ):
        assert forbidden not in source.casefold()
    assert "re.compile" not in source
    assert all(
        line.strip() != "import re" and not line.strip().startswith("from re import ")
        for line in source.splitlines()
    )


def test_production_imports_are_an_exact_executor_allowlist() -> None:
    source = (ROOT / MODULE_PATH).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = {
        (node.module, tuple(alias.name for alias in node.names))
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }

    assert not any(isinstance(node, ast.Import) for node in ast.walk(tree))
    assert imports == {
        ("__future__", ("annotations",)),
        ("dataclasses", ("dataclass",)),
        ("enum", ("Enum", "auto")),
        ("hashlib", ("sha256",)),
        ("typing", ("Any", "Protocol", "TypeAlias")),
    }


def _git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def _commit_has(commit: str, path: str) -> bool:
    return _git("cat-file", "-e", f"{commit}:{path}", check=False).returncode == 0


def test_complete_fixed_test_bytes_precede_the_corrected_green_module() -> None:
    assert _git("rev-parse", f"{CORRECTED_GREEN_COMMIT}^").stdout.strip() == (
        CORRECTED_RED_COMMIT
    )
    assert _commit_has(CORRECTED_RED_COMMIT, TEST_PATH)
    assert not _commit_has(CORRECTED_RED_COMMIT, MODULE_PATH)
    assert _commit_has(CORRECTED_GREEN_COMMIT, MODULE_PATH)
    assert _git("rev-parse", f"{CORRECTED_RED_COMMIT}:{TEST_PATH}").stdout.strip() == (
        CORRECTED_RED_TEST_BLOB
    )
    assert (
        _git("rev-parse", f"{CORRECTED_GREEN_COMMIT}:{TEST_PATH}").stdout.strip()
        == CORRECTED_RED_TEST_BLOB
    )
