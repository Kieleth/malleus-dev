"""Fixed tests for the private retained-source LinkML adapter."""

from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import FrozenInstanceError, fields, is_dataclass
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import pytest

import malleus._contract_linkml_adapter as adapter_module
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
    assert module.support_profile == "malleus.linkml/private-v0"
    assert module.profile_sha256 == sha256(PROFILE.read_bytes()).hexdigest()
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


def test_quiet_bell_separates_enforced_containers_from_reference_identity() -> None:
    foundation = parse_linkml_module(_path_observation("modules/foundation.yaml"))
    entities = parse_linkml_module(_path_observation("modules/entities.yaml"))
    activity = parse_linkml_module(_path_observation("modules/activity.yaml"))

    scalar_references = (
        (foundation, ("default_range",)),
        (foundation, ("types", "ArchiveShelfmark", "typeof")),
        (foundation, ("slots", "shelfmark", "range")),
        (
            entities,
            ("classes", "EvidenceFolio", "attributes", "locator", "range"),
        ),
        (
            activity,
            ("classes", "SealReviewEvent", "slot_usage", "event_type", "range"),
        ),
        (entities, ("classes", "ArchiveExaminer", "is_a")),
    )
    for module, path in scalar_references:
        matches = [item for item in module.occurrences if item.path == path]
        assert len(matches) == 1
        assert matches[0].classification == "ENFORCED"
        assert matches[0].value_classification == "IDENTITY_ONLY"

    prefix = _occurrence(foundation, "prefixes", "quiet")
    assert prefix.classification == "IDENTITY_ONLY"
    assert prefix.value_classification == "IDENTITY_ONLY"

    nested_references = (
        (foundation, ("imports", 0)),
        (entities, ("classes", "ArchiveExaminer", "mixins", 0)),
        (entities, ("classes", "EvidenceLocator", "slots", 0)),
        (
            entities,
            ("classes", "ArchiveExaminer", "slot_usage", "agent_type"),
        ),
        (
            entities,
            (
                "classes",
                "EvidenceLocator",
                "exactly_one_of",
                0,
                "slot_conditions",
                "shelfmark",
            ),
        ),
    )
    for module, path in nested_references:
        occurrence = _occurrence(module, *path)
        assert occurrence.classification == "IDENTITY_ONLY"
        assert occurrence.value_classification is None

    assert _occurrence(foundation, "imports").classification == "ENFORCED"
    assert (
        _occurrence(entities, "classes", "ArchiveExaminer", "slot_usage").classification
        == "ENFORCED"
    )


def test_reference_key_syntax_is_profile_driven_and_defers_binding() -> None:
    source = b"""\
id: https://example.org/reference-keys
name: reference_keys
prefixes:
  ext: https://example.net/schema/
classes:
  Record:
    slot_usage:
      ext:status:
        required: true
    exactly_one_of:
      - slot_conditions:
          ext:status:
            value_presence: PRESENT
"""

    module = parse_linkml_module(_observation("reference-keys", source, ()))

    assert (
        _occurrence(
            module,
            "classes",
            "Record",
            "slot_usage",
            "ext:status",
        ).classification
        == "IDENTITY_ONLY"
    )
    assert (
        _occurrence(
            module,
            "classes",
            "Record",
            "exactly_one_of",
            0,
            "slot_conditions",
            "ext:status",
        ).classification
        == "IDENTITY_ONLY"
    )

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        parse_linkml_module(
            _observation(
                "invalid-declaration-key",
                source.replace(b"  Record:\n", b"  ext:Record:\n"),
                (),
            )
        )
    assert caught.value.reason is LinkMLRefusalReason.MALFORMED_SOURCE


def test_quiet_bell_closure_refuses_only_after_local_modules_are_available() -> None:
    module_names = (
        "modules/activity.yaml",
        "modules/entities.yaml",
        "modules/foundation.yaml",
        "v1.0.0/quiet_bell.yaml",
    )
    trusted_source = (
        files("linkml_runtime.linkml_model.model.schema")
        .joinpath("types.yaml")
        .read_bytes()
    )
    modules = tuple(_path_observation(name) for name in module_names) + (
        _observation("linkml:types", trusted_source, ()),
    )
    edges = (
        _edge("modules/activity.yaml", 0, "foundation", "modules/foundation.yaml"),
        _edge("modules/activity.yaml", 1, "entities", "modules/entities.yaml"),
        _edge("modules/entities.yaml", 0, "foundation", "modules/foundation.yaml"),
        _edge("modules/foundation.yaml", 0, "linkml:types", "linkml:types"),
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
    assert caught.value.path == ("imports", 1)
    assert "malleus" in str(caught.value)
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
        == "-20.0"
    )
    assert (
        _occurrence(
            parsed["numeric-equivalent.yaml"],
            "slots",
            "temperature",
            "maximum_value",
        ).value.lexeme
        == "6e1"
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
            LinkMLRefusalReason.REJECTED_SOURCE,
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
            LinkMLRefusalReason.REJECTED_SOURCE,
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
        (
            "byte-order-mark",
            b"\xef\xbb\xbfid: https://example.org/x\nname: x\n",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "empty-document",
            b"",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "explicit-tag",
            b"id: !!str https://example.org/x\nname: x\n",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "non-string-key",
            b"id: https://example.org/x\nname: x\n1: value\n",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "invalid-number",
            b"id: https://example.org/x\nname: x\nslots:\n  value:\n"
            b"    minimum_value: +1\n",
            LinkMLRefusalReason.MALFORMED_SOURCE,
        ),
        (
            "unknown-nested-field",
            b"id: https://example.org/x\nname: x\nclasses:\n  Record:\n"
            b"    unknown_member: true\n",
            LinkMLRefusalReason.REJECTED_SOURCE,
        ),
        (
            "moved-accepted-field",
            b"id: https://example.org/x\nname: x\nclasses:\n  Record:\n"
            b"    required: true\n",
            LinkMLRefusalReason.REJECTED_SOURCE,
        ),
        (
            "null-declaration-body",
            b"id: https://example.org/x\nname: x\nclasses:\n  Record:\n",
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

    foreign_selection = ResolverSelection(
        resolver_id="TEST_ONLY_OTHER_RESOLVER",
        profile_version=SELECTION.profile_version,
        configuration_id=SELECTION.configuration_id,
    )
    foreign_bytes = b"id: https://example.org/foreign\nname: foreign\n"
    foreign_source = RetainedSource(
        resolved_locator="foreign",
        source_bytes=foreign_bytes,
        byte_length=len(foreign_bytes),
        sha256="sha256:" + sha256(foreign_bytes).hexdigest(),
        media_type="application/yaml",
        resolver_selection=foreign_selection,
    )
    foreign = ModuleObservation("foreign", foreign_source, ())
    foreign_closure = SourceClosure(
        selection=SELECTION,
        root=RootResolution(
            requested_locator="request:foreign",
            resolved_locator="foreign",
            source_sha256=foreign_source.sha256,
            resolver_selection=SELECTION,
        ),
        modules=(foreign,),
        import_edges=(),
    )
    with pytest.raises(LinkMLAdapterRefusal) as selection_refusal:
        adapt_linkml_closure(foreign_closure)
    assert selection_refusal.value.reason is LinkMLRefusalReason.MALFORMED_OBSERVATION
    assert not hasattr(selection_refusal.value, "modules")


def test_closure_refuses_atomically_after_an_earlier_valid_module() -> None:
    valid = _observation(
        "valid",
        b'id: https://example.org/valid\nname: valid\nimports: ["invalid"]\n',
    )
    invalid = _observation(
        "invalid",
        b"id: https://example.org/invalid\nname: invalid\ninstances: {}\n",
        (),
    )
    edge = _edge("valid", 0, "invalid", "invalid")

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        adapt_linkml_closure(_closure((valid, invalid), (edge,), root="valid"))

    assert caught.value.reason is LinkMLRefusalReason.REJECTED_SOURCE
    assert caught.value.module_id == "invalid"
    assert not hasattr(caught.value, "modules")
    assert not hasattr(caught.value, "partial")


def test_closure_refuses_a_module_not_reachable_from_the_exact_root() -> None:
    root = _observation("root", b"id: https://example.org/root\nname: root\n", ())
    orphan = _observation(
        "orphan", b"id: https://example.org/orphan\nname: orphan\n", ()
    )

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        adapt_linkml_closure(_closure((root, orphan), (), root="root"))

    assert caught.value.reason is LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH
    assert caught.value.module_id == "orphan"
    assert not hasattr(caught.value, "modules")


@pytest.mark.parametrize("ordinal", (False, 0.0))
def test_closure_refuses_non_exact_import_ordinals(ordinal: object) -> None:
    root = _observation(
        "root",
        b'id: https://example.org/root\nname: root\nimports: ["child"]\n',
    )
    child = _observation("child", b"id: https://example.org/child\nname: child\n", ())
    malformed = ResolvedImportEdge(
        parent_module_id="root",
        parent_import_ordinal=ordinal,  # type: ignore[arg-type]
        literal_import="child",
        child_module_id="child",
        resolver_selection=SELECTION,
    )

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        adapt_linkml_closure(_closure((root, child), (malformed,), root="root"))

    assert caught.value.reason is LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH
    assert not hasattr(caught.value, "modules")


@pytest.mark.parametrize("member", ("modules", "import_edges"))
def test_closure_refuses_mutable_member_containers(member: str) -> None:
    root = _observation("root", b"id: https://example.org/root\nname: root\n", ())
    closure = _closure((root,), (), root="root")
    malformed = SourceClosure(
        selection=closure.selection,
        root=closure.root,
        modules=list(closure.modules) if member == "modules" else closure.modules,  # type: ignore[arg-type]
        import_edges=(
            list(closure.import_edges)  # type: ignore[arg-type]
            if member == "import_edges"
            else closure.import_edges
        ),
    )

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        adapt_linkml_closure(malformed)

    assert caught.value.reason is LinkMLRefusalReason.MALFORMED_OBSERVATION


def test_unauthored_edge_refusal_preserves_prior_stage_edge_order() -> None:
    root = _observation("root", b"id: https://example.org/root\nname: root\n", ())
    first = _edge("z-first", 7, "first", "root")
    second = _edge("a-second", 2, "second", "root")

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        adapt_linkml_closure(_closure((root,), (first, second), root="root"))

    assert caught.value.reason is LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH
    assert caught.value.module_id == "z-first"
    assert caught.value.path == ("imports", 7)


def test_repeated_imports_and_class_slots_remain_authored_evidence() -> None:
    source = b"""\
id: https://example.org/repeats
name: repeats
imports:
  - child
  - child
slots:
  value: {}
classes:
  Record:
    slots:
      - value
      - value
"""

    module = parse_linkml_module(_observation("repeats", source))

    assert module.authored_imports == ("child", "child")
    imports = _occurrence(module, "imports").value
    slots = _occurrence(module, "classes", "Record", "slots").value
    assert isinstance(imports, AuthoredSequence)
    assert isinstance(slots, AuthoredSequence)
    assert tuple(item.value.value for item in imports.items) == ("child", "child")
    assert tuple(item.value.value for item in slots.items) == ("value", "value")


def test_trusted_import_cannot_bless_bytes_under_another_module_identity() -> None:
    root = _observation(
        "root",
        b'id: https://example.org/root\nname: root\nimports: ["linkml:types"]\n',
    )
    trusted_source = (
        files("linkml_runtime.linkml_model.model.schema")
        .joinpath("types.yaml")
        .read_bytes()
    )
    wrong_identity = _observation("not-linkml-types", trusted_source, ())
    edge = _edge("root", 0, "linkml:types", "not-linkml-types")

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        adapt_linkml_closure(_closure((root, wrong_identity), (edge,), root="root"))

    assert caught.value.reason is LinkMLRefusalReason.CLOSURE_IMPORT_MISMATCH
    assert caught.value.module_id == "root"
    assert caught.value.path == ("imports", 0)
    assert not hasattr(caught.value, "modules")


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


def test_adapter_retains_large_decimal_exponent_without_fixed_point_expansion() -> None:
    lexeme = "1e100000"
    source = (
        "id: https://example.org/large-number\n"
        "name: large_number\n"
        "slots:\n"
        "  value:\n"
        f"    minimum_value: {lexeme}\n"
    ).encode()

    module = parse_linkml_module(_observation("large-number", source, ()))
    value = _occurrence(module, "slots", "value", "minimum_value").value

    assert value == AuthoredScalar("NUMBER", lexeme, lexeme)
    assert len(value.value) == len(lexeme)


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
    assert (
        profile["node_shapes"]["schema"]["fields"]["default_range"][
            "value_classification"
        ]
        == "IDENTITY_ONLY"
    )
    assert (
        profile["node_shapes"]["class"]["fields"]["slot_usage"]["key_parser"]
        == "reference"
    )
    assert (
        profile["node_shapes"]["schema"]["fields"]["classes"]["key_parser"]
        == "ascii_identifier"
    )
    combined = ADAPTER.read_text(encoding="utf-8") + PROFILE.read_text(encoding="utf-8")
    for fixture_name in ("greenhouse", "Quiet Bell", "ArchiveExaminer", "PlantState"):
        assert fixture_name not in combined


@pytest.mark.parametrize("mutation", ("missing-key-parser", "bad-value-classification"))
def test_adapter_refuses_unexecutable_occurrence_policy(mutation: str) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    if mutation == "missing-key-parser":
        profile["node_shapes"]["class"]["fields"]["slot_usage"].pop("key_parser")
    else:
        profile["node_shapes"]["slot"]["fields"]["range"]["value_classification"] = (
            "REJECTED"
        )

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        parse_linkml_module(
            _observation(
                "invalid-profile", b"id: https://example.org/x\nname: x\n", ()
            ),
            profile=profile,
        )

    assert caught.value.reason is LinkMLRefusalReason.INVALID_PROFILE


@pytest.mark.parametrize(
    "mutation",
    (
        "missing-support-profile",
        "foreign-support-profile",
        "foreign-namespace",
        "foreign-trusted-import",
        "forged-trusted-module",
        "forged-builtin",
        "reordered-seeds",
        "extra-root-member",
        "extra-shape",
        "extra-shape-member",
        "field-classification",
        "field-parser",
        "missing-item-shape",
        "rejected-mapping-parser",
    ),
)
def test_direct_adapter_refuses_profile_trust_or_closure_mutation(
    mutation: str,
) -> None:
    profile = deepcopy(json.loads(PROFILE.read_text(encoding="utf-8")))
    if mutation == "missing-support-profile":
        profile.pop("support_profile")
    elif mutation == "foreign-support-profile":
        profile["support_profile"] = "attacker-controlled"
    elif mutation == "foreign-namespace":
        profile["namespace"] = "https://attacker.invalid/"
    elif mutation == "foreign-trusted-import":
        profile["trusted_import"] = "attacker:types"
    elif mutation == "forged-trusted-module":
        profile["trusted_module"] = {
            "module_id": "attacker:types",
            "schema_id": "https://attacker.invalid/types",
            "byte_length": 12,
            "sha256": "sha256:" + "0" * 64,
        }
    elif mutation == "forged-builtin":
        profile["builtins"] = {
            "attacker": {"form": "ABSOLUTE", "value": "urn:attacker:builtin"}
        }
        profile["seed_primitives"] = ["attacker"]
    elif mutation == "reordered-seeds":
        profile["seed_primitives"] = list(reversed(profile["seed_primitives"]))
    elif mutation == "extra-root-member":
        profile["unread"] = True
    elif mutation == "extra-shape":
        profile["node_shapes"]["attacker"] = {
            "fields": {},
            "label": "attacker",
        }
    elif mutation == "extra-shape-member":
        profile["node_shapes"]["schema"]["unread"] = True
    elif mutation == "field-classification":
        profile["node_shapes"]["schema"]["fields"]["name"]["classification"] = (
            "IDENTITY_ONLY"
        )
    elif mutation == "field-parser":
        profile["node_shapes"]["schema"]["fields"]["name"]["parser"] = "string"
    elif mutation == "missing-item-shape":
        profile["node_shapes"]["schema"]["fields"]["classes"].pop("item_shape")
    else:
        profile["node_shapes"]["schema"]["fields"]["name"] = {
            "classification": "REJECTED",
            "parser": "mapping",
        }

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        parse_linkml_module(
            _observation(
                "invalid-profile", b"id: https://example.org/x\nname: x\n", ()
            ),
            profile=profile,
        )

    assert caught.value.reason is LinkMLRefusalReason.INVALID_PROFILE


def test_mutated_profile_cannot_bless_arbitrary_trusted_module_bytes() -> None:
    source = b"not LinkML\n"
    profile = deepcopy(json.loads(PROFILE.read_text(encoding="utf-8")))
    profile["trusted_import"] = "attacker:types"
    profile["trusted_module"] = {
        "module_id": "attacker:types",
        "schema_id": "urn:attacker:schema",
        "byte_length": len(source),
        "sha256": "sha256:" + sha256(source).hexdigest(),
    }
    profile["builtins"] = {
        "attacker": {"form": "ABSOLUTE", "value": "urn:attacker:builtin"}
    }
    profile["seed_primitives"] = ["attacker"]

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        parse_linkml_module(
            _observation("attacker:types", source, ()),
            profile=profile,
        )

    assert caught.value.reason is LinkMLRefusalReason.INVALID_PROFILE


def test_caller_cannot_bypass_profile_validation_with_internal_wrapper() -> None:
    source = b"not LinkML\n"
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    profile["trusted_import"] = "attacker:types"
    profile["trusted_module"] = {
        "module_id": "attacker:types",
        "schema_id": "urn:attacker:schema",
        "byte_length": len(source),
        "sha256": "sha256:" + sha256(source).hexdigest(),
    }
    profile["builtins"] = {
        "attacker": {"form": "ABSOLUTE", "value": "urn:attacker:builtin"}
    }
    profile["seed_primitives"] = ["attacker"]
    forged = adapter_module._AdapterProfile(profile, "attacker-selected-digest")

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        parse_linkml_module(
            _observation("attacker:types", source, ()),
            profile=forged,  # type: ignore[arg-type]
        )

    assert caught.value.reason is LinkMLRefusalReason.INVALID_PROFILE


@pytest.mark.parametrize(
    "mutation",
    (
        "ordinal-bool",
        "ordinal-float",
        "required-int",
        "required-float",
        "min-fields-bool",
        "values-int",
    ),
)
def test_adapter_policy_comparison_is_type_exact(mutation: str) -> None:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    if mutation == "ordinal-bool":
        profile["source_ordering"]["ordinal_base"] = False
    elif mutation == "ordinal-float":
        profile["source_ordering"]["ordinal_base"] = 0.0
    elif mutation == "required-int":
        profile["node_shapes"]["schema"]["fields"]["name"]["required"] = 1
    elif mutation == "required-float":
        profile["node_shapes"]["schema"]["fields"]["name"]["required"] = 1.0
    elif mutation == "min-fields-bool":
        profile["node_shapes"]["condition"]["min_fields"] = True
    else:
        profile["node_shapes"]["adoption_annotations"]["fields"]["adopts"][
            "values"
        ] = [1]

    with pytest.raises(LinkMLAdapterRefusal) as caught:
        parse_linkml_module(
            _observation(
                "aliased-profile", b"id: https://example.org/x\nname: x\n", ()
            ),
            profile=profile,
        )

    assert caught.value.reason is LinkMLRefusalReason.INVALID_PROFILE


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
    path_reads = [
        node
        for node in ast.walk(adapter_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"read_bytes", "read_text"}
    ]
    adapter_direct_calls = {
        node.func.id
        for node in ast.walk(adapter_tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    compiler_modules = {
        node.module
        for node in ast.walk(compiler_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    adapter_modules = {
        node.module
        for node in ast.walk(adapter_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }

    assert "malleus._contract_linkml_adapter" in compiler_imports | compiler_modules
    assert "malleus.ontology" not in compiler_imports | adapter_imports
    assert "OntologyRegistry" not in COMPILER.read_text(encoding="utf-8")
    assert "OntologyRegistry" not in ADAPTER.read_text(encoding="utf-8")
    assert not ({"open", "urlopen", "connect"} & adapter_calls)
    assert not ({"open", "urlopen", "connect"} & adapter_direct_calls)
    assert not (
        {"http.client", "requests", "socket", "urllib.request"}
        & (adapter_imports | adapter_modules)
    )
    assert len(path_reads) == 1
    assert ast.unparse(path_reads[0].func.value) == "_PROFILE_PATH"
    assert not any(
        isinstance(node, (ast.ClassDef, ast.FunctionDef)) and node.name == "_RawParser"
        for node in ast.walk(compiler_tree)
    )


def test_declared_closure_type_is_part_of_the_private_boundary() -> None:
    assert DeclaredContractClosure is not None
