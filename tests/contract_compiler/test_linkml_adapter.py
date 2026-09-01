"""Fixed tests for the private retained-source LinkML adapter."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError, fields, is_dataclass
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import pytest

from malleus._contract_linkml_adapter import (
    AuthoredMapping,
    AuthoredScalar,
    AuthoredSequence,
    DeclaredContractClosure,
    DeclaredModule,
    LinkMLAdapterRefusal,
    LinkMLImportReader,
    LinkMLRefusalReason,
    adapt_linkml_closure,
    parse_linkml_module,
)
from malleus._contract_source import (
    ModuleObservation,
    ResolvedImportEdge,
    ResolverSelection,
    RetainedSource,
    RootResolution,
    SourceClosure,
)


ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "src/malleus/_contract_linkml_adapter.py"
COMPILER = ROOT / "src/malleus/_contract_compiler.py"
PROFILE = ROOT / "src/malleus/_contract_compiler_profile.json"
QUIET_ROOT = ROOT / "conformance/contract_kernel/v0/themed_fixture"
QUIET_SOURCES = QUIET_ROOT / "sources"
QUIET_ORACLE = json.loads(
    (QUIET_ROOT / "oracle/quiet_bell.json").read_text(encoding="utf-8")
)
GREENHOUSE = ROOT / "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse"
FEATURES = ROOT / "conformance/contract_kernel/v0/feature_cases/inputs"
FEATURE_ORACLE = json.loads(
    (
        ROOT / "conformance/contract_kernel/v0/feature_cases/oracle/feature_cases.json"
    ).read_text(encoding="utf-8")
)
SELECTION = ResolverSelection(
    resolver_id="TEST_ONLY_STRICT_RESOLVER",
    profile_version="TEST_ONLY_LINKML_V0",
    configuration_id="TEST_ONLY_NO_AMBIENT_IO",
)


def _retained(
    module_id: str,
    source_bytes: bytes,
    *,
    media_type: str = "application/yaml",
) -> RetainedSource:
    return RetainedSource(
        resolved_locator=module_id,
        source_bytes=source_bytes,
        byte_length=len(source_bytes),
        sha256=f"sha256:{sha256(source_bytes).hexdigest()}",
        media_type=media_type,
        resolver_selection=SELECTION,
    )


def _observation(
    module_id: str,
    source_bytes: bytes,
    imports: tuple[str, ...] | None = None,
    *,
    media_type: str = "application/yaml",
) -> ModuleObservation:
    retained = _retained(module_id, source_bytes, media_type=media_type)
    authored_imports = (
        LinkMLImportReader().read_imports(retained) if imports is None else imports
    )
    return ModuleObservation(
        module_id=module_id,
        source=retained,
        authored_imports=authored_imports,
    )


def _path_observation(relative: str) -> ModuleObservation:
    path = QUIET_SOURCES / relative
    return _observation(relative, path.read_bytes())


def _edge(
    parent: str,
    ordinal: int,
    literal: str,
    child: str,
) -> ResolvedImportEdge:
    return ResolvedImportEdge(
        parent_module_id=parent,
        parent_import_ordinal=ordinal,
        literal_import=literal,
        child_module_id=child,
        resolver_selection=SELECTION,
    )


def _closure(
    modules: tuple[ModuleObservation, ...],
    edges: tuple[ResolvedImportEdge, ...],
    *,
    root: str,
) -> SourceClosure:
    root_module = next(module for module in modules if module.module_id == root)
    return SourceClosure(
        selection=SELECTION,
        root=RootResolution(
            requested_locator=f"request:{root}",
            resolved_locator=root,
            source_sha256=root_module.source.sha256,
            resolver_selection=SELECTION,
        ),
        modules=modules,
        import_edges=edges,
    )


def _occurrence(module: DeclaredModule, *path: str | int):
    return next(item for item in module.occurrences if item.path == path)


def _declaration_inventory(module: DeclaredModule) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {}
    for declaration in module.declarations:
        inventory.setdefault(declaration.kind, []).append(declaration.identifier)
    return {kind: sorted(identifiers) for kind, identifiers in inventory.items()}


def _assert_deeply_immutable(value: object) -> None:
    if is_dataclass(value):
        for field in fields(value):
            _assert_deeply_immutable(getattr(value, field.name))
        return
    if isinstance(value, tuple):
        for item in value:
            _assert_deeply_immutable(item)
        return
    assert value is None or type(value) in {bool, bytes, int, str}


# Quiet Bell comes first. It proves authored local evidence, not compilation.


@pytest.mark.parametrize(
    "relative", tuple(source["path"] for source in QUIET_ORACLE["sources"])
)
def test_quiet_bell_modules_preserve_exact_source_imports_and_declarations(
    relative: str,
) -> None:
    observation = _path_observation(relative)

    module = parse_linkml_module(observation)

    source_record = next(
        source for source in QUIET_ORACLE["sources"] if source["path"] == relative
    )
    expected_imports = tuple(
        edge["literal"]
        for edge in QUIET_ORACLE["import_edges"]
        if edge["parent"] == relative
    )
    assert module.module_id == relative
    assert module.source is observation.source
    assert module.source.byte_length == source_record["byte_length"]
    assert module.source.sha256.removeprefix("sha256:") in source_record["source_blob"]
    assert module.authored_imports == expected_imports
    assert _declaration_inventory(module) == QUIET_ORACLE["declarations"][relative]


def test_quiet_bell_preserves_prefix_annotation_numeric_and_nested_evidence() -> None:
    foundation = parse_linkml_module(_path_observation("modules/foundation.yaml"))
    entities = parse_linkml_module(_path_observation("modules/entities.yaml"))
    activity = parse_linkml_module(_path_observation("modules/activity.yaml"))

    prefix = _occurrence(foundation, "prefixes", "quiet")
    type_uri = _occurrence(foundation, "types", "ArchiveShelfmark", "uri")
    minimum = _occurrence(foundation, "slots", "certainty", "minimum_value")
    maximum = _occurrence(foundation, "slots", "certainty", "maximum_value")
    inlined = _occurrence(
        entities, "classes", "EvidenceFolio", "attributes", "locator", "inlined"
    )
    slot_override = _occurrence(
        activity,
        "classes",
        "SealReviewEvent",
        "slot_usage",
        "event_type",
        "equals_string",
    )

    assert prefix.classification == "IDENTITY_ONLY"
    assert type_uri.classification == "ANNOTATION_ONLY"
    assert minimum.value == AuthoredScalar("NUMBER", "0", "0")
    assert maximum.value == AuthoredScalar("NUMBER", "1", "1")
    assert inlined.value == AuthoredScalar("BOOLEAN", "true", True)
    assert slot_override.value == AuthoredScalar("STRING", "SEAL_REVIEW", "SEAL_REVIEW")


def test_quiet_bell_closure_refuses_only_after_local_modules_are_available() -> None:
    module_names = (
        "modules/activity.yaml",
        "modules/entities.yaml",
        "modules/foundation.yaml",
        "v1.0.0/quiet_bell.yaml",
    )
    modules = tuple(_path_observation(name) for name in module_names)
    edges = (
        _edge("modules/activity.yaml", 0, "foundation", "modules/foundation.yaml"),
        _edge("modules/activity.yaml", 1, "entities", "modules/entities.yaml"),
        _edge("modules/entities.yaml", 0, "foundation", "modules/foundation.yaml"),
        _edge(
            "v1.0.0/quiet_bell.yaml",
            0,
            "../modules/entities",
            "modules/entities.yaml",
        ),
        _edge(
            "v1.0.0/quiet_bell.yaml",
            1,
            "../modules/activity",
            "modules/activity.yaml",
        ),
    )
    closure = _closure(modules, edges, root="v1.0.0/quiet_bell.yaml")

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        adapt_linkml_closure(closure)

    assert caught.value.reason is LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH
    assert caught.value.module_id == "modules/foundation.yaml"
    assert caught.value.path == ("imports", 0)
    assert "linkml:types" in str(caught.value)
    assert not hasattr(caught.value, "modules")
    assert not hasattr(caught.value, "partial")


def test_trusted_linkml_types_is_exact_and_not_parsed_as_an_open_schema() -> None:
    source = (
        files("linkml_runtime.linkml_model.model.schema")
        .joinpath("types.yaml")
        .read_bytes()
    )
    observation = _observation("linkml:types", source, ())

    module = parse_linkml_module(observation)

    assert module.trusted is True
    assert module.schema_id == "https://w3id.org/linkml/types"
    assert [declaration.name for declaration in module.declarations] == [
        "string",
        "integer",
        "float",
        "boolean",
        "datetime",
        "date",
        "uri",
    ]
    mutated = source.replace(b"name: types", b"name: TYPES", 1)
    with pytest.raises(LinkMLAdapterRefusal) as caught:
        parse_linkml_module(_observation("linkml:types", mutated, ()))
    assert caught.value.reason is LinkMLRefusalReason.TRUSTED_MODULE_MISMATCH


# Neutral Greenhouse follows. Differences remain visible until later semantics.


@pytest.mark.parametrize(
    "name",
    (
        "baseline.yaml",
        "explicit-defaults.yaml",
        "numeric-equivalent.yaml",
        "presentation-only.yaml",
        "reordered.yaml",
        "semantic-change.yaml",
    ),
)
def test_greenhouse_variants_parse_as_exact_neutral_authored_evidence(
    name: str,
) -> None:
    path = GREENHOUSE / name
    module = parse_linkml_module(_observation(name, path.read_bytes()))

    assert module.module_id == name
    assert module.schema_id == "https://example.malleus.dev/greenhouse"
    assert module.source.source_bytes == path.read_bytes()
    assert module.source.sha256 == f"sha256:{sha256(path.read_bytes()).hexdigest()}"
    assert {declaration.kind for declaration in module.declarations} == {
        "Class",
        "Enum",
        "Scalar",
        "Slot",
        "Attribute",
    }


def test_greenhouse_differences_are_not_normalized_by_the_parser_stage() -> None:
    parsed = {
        name: parse_linkml_module(_observation(name, (GREENHOUSE / name).read_bytes()))
        for name in (
            "baseline.yaml",
            "explicit-defaults.yaml",
            "numeric-equivalent.yaml",
            "presentation-only.yaml",
            "reordered.yaml",
        )
    }

    baseline = parsed["baseline.yaml"]
    assert all(
        module.root != baseline.root
        for module in parsed.values()
        if module is not baseline
    )
    assert (
        _occurrence(
            parsed["numeric-equivalent.yaml"],
            "slots",
            "temperature",
            "minimum_value",
        ).value.lexeme
        == "-2.0e1"
    )
    assert (
        _occurrence(
            parsed["numeric-equivalent.yaml"],
            "slots",
            "temperature",
            "maximum_value",
        ).value.lexeme
        == "6.0e1"
    )
    assert (
        _occurrence(
            parsed["explicit-defaults.yaml"], "slots", "state", "required"
        ).value.value
        is False
    )
    assert not any(
        occurrence.path == ("slots", "state", "required")
        for occurrence in baseline.occurrences
    )
    assert (
        _occurrence(parsed["presentation-only.yaml"], "description").classification
        == "ANNOTATION_ONLY"
    )


def test_adapter_preserves_prior_stage_module_order_without_resorting() -> None:
    alpha = _observation(
        "z-last-by-name",
        b'id: https://example.org/z\nname: z\nimports: ["child"]\n',
    )
    child = _observation("a-first-by-name", b"id: https://example.org/a\nname: a\n", ())
    closure = _closure(
        (alpha, child),
        (_edge("z-last-by-name", 0, "child", "a-first-by-name"),),
        root="z-last-by-name",
    )

    result = adapt_linkml_closure(closure)

    assert [module.module_id for module in result.modules] == [
        "z-last-by-name",
        "a-first-by-name",
    ]


# Feature and refusal edges come last. Later stages own semantic conflicts.


@pytest.mark.parametrize(
    "relative", tuple(FEATURE_ORACLE["sources"][index]["path"] for index in range(18))
)
def test_every_governed_feature_source_reaches_declared_evidence(relative: str) -> None:
    path = FEATURES / relative
    module = parse_linkml_module(
        _observation(relative, path.read_bytes(), media_type="application/json")
    )

    assert module.module_id == relative
    assert module.declarations


def test_later_conflicts_and_authored_values_remain_lossless() -> None:
    repeated_path = FEATURES / "x01/repeated_mixin.json"
    repeated = parse_linkml_module(
        _observation(
            "x01/repeated_mixin.json",
            repeated_path.read_bytes(),
            media_type="application/json",
        )
    )
    mixins = _occurrence(repeated, "classes", "Child", "mixins").value
    assert isinstance(mixins, AuthoredSequence)
    assert tuple(item.value.value for item in mixins.items) == ("MixinA", "MixinA")
    assert tuple(item.ordinal for item in mixins.items) == (0, 1)

    numeric_path = FEATURES / "metamorphic/numeric_bounds_equivalent_lexemes.json"
    numeric = parse_linkml_module(
        _observation(
            "numeric.json",
            numeric_path.read_bytes(),
            media_type="application/json",
        )
    )
    assert (
        _occurrence(
            numeric, "classes", "Child", "slot_usage", "value", "maximum_value"
        ).value.lexeme
        == "9.5e1"
    )
    assert _occurrence(numeric, "slots", "value", "minimum_value").value.lexeme == "0e0"

    adoption_path = FEATURES / "explicit_adoption/adopter.json"
    adoption = parse_linkml_module(
        _observation(
            "adopter.json",
            adoption_path.read_bytes(),
            media_type="application/json",
        )
    )
    adopts = _occurrence(adoption, "slots", "shared_value", "annotations", "adopts")
    assert adopts.classification == "IDENTITY_ONLY"
    assert adopts.value == AuthoredScalar("BOOLEAN", "true", True)


def test_explicit_false_is_distinct_from_missing_without_deciding_validity() -> None:
    explicit_path = FEATURES / "positive/valid_explicit_false.json"
    missing_path = FEATURES / "x01/default_range.json"
    explicit = parse_linkml_module(
        _observation(
            "explicit.json",
            explicit_path.read_bytes(),
            media_type="application/json",
        )
    )
    missing = parse_linkml_module(
        _observation(
            "missing.json",
            missing_path.read_bytes(),
            media_type="application/json",
        )
    )

    assert _occurrence(explicit, "slots", "value", "required").value == AuthoredScalar(
        "BOOLEAN", "false", False
    )
    assert not any(
        occurrence.path == ("slots", "value", "required")
        for occurrence in missing.occurrences
    )


@pytest.mark.parametrize(
    "name,source,reason",
    (
        (
            "unknown-root",
            b"id: https://example.org/x\nname: x\ninstances: {}\n",
            LinkMLRefusalReason.UNSUPPORTED_SOURCE,
        ),
        (
            "duplicate-key",
            b"id: https://example.org/x\nname: x\nname: repeated\n",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "yaml-boolean",
            b"id: https://example.org/x\nname: x\nslots:\n  value:\n    required: TRUE\n",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "quoted-number",
            b'id: https://example.org/x\nname: x\nslots:\n  value:\n    minimum_value: "1"\n',
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "retired-annotation",
            b"id: https://example.org/x\nname: x\nslots:\n  value:\n    annotations:\n      retires: true\n",
            LinkMLRefusalReason.UNSUPPORTED_SOURCE,
        ),
        (
            "alias",
            b"id: https://example.org/x\nname: x\nslots: &slots {}\nclasses: *slots\n",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "two-documents",
            b"id: https://example.org/x\nname: x\n---\nid: https://example.org/y\nname: y\n",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "invalid-utf8",
            b"\xff",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
    ),
)
def test_raw_source_refusals_are_closed_and_typed(
    name: str, source: bytes, reason: LinkMLRefusalReason
) -> None:
    with pytest.raises(LinkMLAdapterRefusal) as caught:
        parse_linkml_module(_observation(name, source, ()))

    assert caught.value.reason is reason
    assert caught.value.module_id == name
    assert not hasattr(caught.value, "module")
    assert not hasattr(caught.value, "partial")


def test_observation_and_closure_cross_checks_refuse_atomically() -> None:
    root = _observation(
        "root",
        b'id: https://example.org/root\nname: root\nimports: ["child"]\n',
        (),
    )
    with pytest.raises(LinkMLAdapterRefusal) as observation_refusal:
        parse_linkml_module(root)
    assert (
        observation_refusal.value.reason
        is LinkMLRefusalReason.OBSERVATION_IMPORT_MISMATCH
    )

    root = _observation(
        "root",
        b'id: https://example.org/root\nname: root\nimports: ["child"]\n',
    )
    child = _observation("child", b"id: https://example.org/child\nname: child\n", ())
    wrong_edge = _edge("root", 0, "different", "child")
    with pytest.raises(LinkMLAdapterRefusal) as closure_refusal:
        adapt_linkml_closure(_closure((root, child), (wrong_edge,), root="root"))
    assert closure_refusal.value.reason is LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH
    assert not hasattr(closure_refusal.value, "modules")


def test_result_is_repeatable_deeply_immutable_and_preserves_zero_based_order() -> None:
    source = (
        b"id: https://example.org/order\n"
        b"name: order\n"
        b"slots:\n"
        b"  first:\n"
        b"    required: false\n"
        b"  second:\n"
        b"    range: string\n"
    )
    observation = _observation("order", source, ())

    first = parse_linkml_module(observation)
    second = parse_linkml_module(observation)

    assert first == second
    assert isinstance(first.root, AuthoredMapping)
    assert tuple(field.ordinal for field in first.root.fields) == (0, 1, 2)
    assert tuple(declaration.ordinal for declaration in first.declarations) == (0, 1)
    assert isinstance(first, DeclaredModule)
    _assert_deeply_immutable(first)
    with pytest.raises(FrozenInstanceError):
        first.module_id = "changed"  # type: ignore[misc]


def test_profile_is_closed_machine_readable_and_domain_neutral() -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))

    assert profile["schema"] == "malleus.contract-compiler.linkml-profile/v0"
    assert profile["linkml_version"] == "1.11.1"
    assert profile["source_ordering"] == {
        "module_order": "PRESERVE_SOURCE_CLOSURE",
        "ordinal_base": 0,
        "field_order": "PRESERVE_AUTHORED",
    }
    assert set(profile["builtins"]) == {
        "boolean",
        "date",
        "datetime",
        "float",
        "integer",
        "string",
        "uri",
    }
    assert (
        profile["node_shapes"]["schema"]["fields"]["prefixes"]["classification"]
        == "IDENTITY_ONLY"
    )
    assert (
        profile["node_shapes"]["class"]["fields"]["slot_usage"]["classification"]
        == "ENFORCED"
    )
    assert (
        profile["node_shapes"]["slot"]["fields"]["annotations"]["classification"]
        == "IDENTITY_ONLY"
    )
    combined = ADAPTER.read_text(encoding="utf-8") + PROFILE.read_text(encoding="utf-8")
    for fixture_name in ("greenhouse", "Quiet Bell", "ArchiveExaminer", "PlantState"):
        assert fixture_name not in combined


def test_one_parser_is_shared_and_has_no_registry_or_source_io_fallback() -> None:
    compiler_tree = ast.parse(COMPILER.read_text(encoding="utf-8"))
    adapter_tree = ast.parse(ADAPTER.read_text(encoding="utf-8"))
    compiler_imports = {
        alias.name
        for node in ast.walk(compiler_tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    adapter_imports = {
        alias.name
        for node in ast.walk(adapter_tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    adapter_calls = {
        node.func.attr
        for node in ast.walk(adapter_tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }

    assert "malleus._contract_linkml_adapter" in compiler_imports
    assert "malleus.ontology" not in compiler_imports | adapter_imports
    assert "OntologyRegistry" not in COMPILER.read_text(encoding="utf-8")
    assert "OntologyRegistry" not in ADAPTER.read_text(encoding="utf-8")
    assert not ({"open", "urlopen", "connect"} & adapter_calls)
    assert not any(
        isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name == "_RawParser"
        for node in ast.walk(compiler_tree)
    )


def test_declared_closure_type_is_part_of_the_private_boundary() -> None:
    assert DeclaredContractClosure is not None
