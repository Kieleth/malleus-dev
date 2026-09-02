"""Pareto controls for one reloadable compiler-to-structural-view boundary."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import pytest

import malleus._contract_compiler as compiler
from malleus._contract_binder import BindingRefusal, BindingRefusalReason, bind_contract
from malleus._contract_linkml_adapter import LinkMLImportReader, adapt_linkml_closure
from malleus._contract_source import (
    CollaboratorRefusal,
    ImportRequest,
    ResolvedSource,
    ResolverSelection,
    RootRequest,
    build_source_closure,
)
from malleus.kg import KnowledgeGraph, OpStatus


ROOT = Path(__file__).resolve().parents[3]
SMALL_SHOP = (
    ROOT
    / "research"
    / "ontology_driven_kg_realization"
    / "fixtures"
    / "small_shop_fulfilment"
    / "input"
    / "tbox"
)
GREENHOUSE = (
    ROOT / "conformance/contract_kernel/v0/neutral_domain/sources/greenhouse"
)
FEATURES = ROOT / "conformance/contract_kernel/v0/feature_cases/inputs/x01"
SELECTION = ResolverSelection(
    resolver_id="TEST_ONLY_EXACT_MAPPING_RESOLVER",
    profile_version="TEST_ONLY_V0",
    configuration_id="TEST_ONLY_NO_AMBIENT_IO",
)


class _ExactResolver:
    def __init__(self, sources: dict[str, bytes | tuple[str, bytes]]) -> None:
        self._sources = sources

    def resolve(self, request: RootRequest | ImportRequest) -> ResolvedSource:
        locator = (
            request.requested_locator
            if isinstance(request, RootRequest)
            else request.literal_import
        )
        try:
            answer = self._sources[locator]
        except KeyError as error:
            raise CollaboratorRefusal(locator) from error
        resolved, source = answer if isinstance(answer, tuple) else (locator, answer)
        return ResolvedSource(resolved, source, "application/yaml")


def _trusted_types() -> bytes:
    return (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )


def _binding(sources: dict[str, bytes | tuple[str, bytes]], root: str):
    closure = build_source_closure(
        requested_locator=root,
        selection=SELECTION,
        resolver=_ExactResolver(sources),
        import_reader=LinkMLImportReader(),
    )
    return bind_contract(adapt_linkml_closure(closure))


def _small_shop_binding(*, description_variant: bool = False):
    source_name = (
        "small-shop-description-only.yaml"
        if description_variant
        else "small-shop.yaml"
    )
    return _binding(
        {
            "small-shop": (SMALL_SHOP / source_name).read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": _trusted_types(),
        },
        "small-shop",
    )


def _compile_binding(binding):
    from malleus._contract_pipeline import compile_binding

    return compile_binding(binding)


def _compile_feature(name: str):
    return _compile_binding(_binding({name: (FEATURES / name).read_bytes()}, name))


def test_small_shop_elaborates_inheritance_slot_usage_enum_and_neutral_facts() -> None:
    result = _compile_binding(_small_shop_binding())
    view = result.view

    assert view.is_subtype_of("SalesOrder", "Entity")
    assert view.is_subtype_of("OrderContainsUnit", "Relation")
    assert view.has_mixin("SalesOrder", "Identifiable")
    assert view.get_slot_constraint("SalesOrder", "order_number").required is True
    relation_kind = view.get_slot_constraint(
        "OrderContainsUnit", "relation_type"
    )
    assert relation_kind.range == "ShopRelationKind"
    assert relation_kind.equals_string == "ORDER_CONTAINS_UNIT"
    assert view.get_enum_values("ShopRelationKind") == frozenset(
        {"ORDER_CONTAINS_UNIT"}
    )
    assert result.facts == tuple(
        sorted(result.facts, key=lambda fact: result.fact_bytes(fact))
    )
    assert result.canonical_facts == json.dumps(
        [fact.as_dict() for fact in result.facts],
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def test_annotation_changes_source_attestation_not_semantic_contract_identity() -> None:
    baseline = _compile_binding(_small_shop_binding())
    described = _compile_binding(_small_shop_binding(description_variant=True))

    assert baseline.content_hash == described.content_hash
    assert baseline.canonical_facts == described.canonical_facts
    assert baseline.artifact.evidence != described.artifact.evidence
    assert baseline.artifact.artifact_bytes != described.artifact.artifact_bytes


def test_root_instances_refuses_atomically_before_elaboration() -> None:
    source = (SMALL_SHOP / "small-shop-root-instances.yaml").read_bytes()

    with pytest.raises(compiler.ContractCompileError, match="instances"):
        compiler.compile_linkml_contract(source, locator="memory:root-instances")


def test_defaults_explicit_false_bounds_and_mixin_conflict_are_mechanical() -> None:
    explicit = _compile_feature("explicit_false.json")
    use = explicit.view.get_slot_constraint("Thing", "value")
    assert use.required is False
    assert use.multivalued is False
    assert use.identifier is False
    assert use.inlined is False
    assert use.range == "string"

    bounds = _compile_feature("numeric_bounds.json")
    inherited = bounds.view.get_slot_constraint("Child", "value")
    assert inherited.minimum_value == 10
    assert inherited.maximum_value == 90

    from malleus._contract_pipeline import ElaborationRefusal, ElaborationRefusalReason

    for name in ("conflicting_mixins_ab.json", "conflicting_mixins_ba.json"):
        with pytest.raises(ElaborationRefusal) as refusal:
            _compile_feature(name)
        assert refusal.value.reason is ElaborationRefusalReason.MIXIN_CONFLICT


def test_greenhouse_uses_formal_pipeline_and_preserves_accepted_facts() -> None:
    path = GREENHOUSE / "baseline.yaml"
    result = compiler.compile_linkml_contract(path.read_bytes(), locator=path.as_uri())

    assert result.facts_sha256 == (
        "4103a7cf5db383a1bf29f88bcf94e0057707ea94452f0a36a073b9bb95564db4"
    )
    assert result.artifact.capability == "VALIDATED_FACTS_AND_STRUCTURAL_VIEW_ONLY"
    assert result.elaborated.classes


def test_imported_quiet_bell_missing_dependency_refuses_without_ambient_fallback() -> None:
    quiet = ROOT / "conformance/contract_kernel/v0/themed_fixture/sources"
    with pytest.raises(BindingRefusal) as refusal:
        _binding(
            {
                "quiet": (quiet / "v1.0.0/quiet_bell.yaml").read_bytes(),
                "../modules/entities": (
                    "entities",
                    (quiet / "modules/entities.yaml").read_bytes(),
                ),
                "../modules/activity": (
                    "activity",
                    (quiet / "modules/activity.yaml").read_bytes(),
                ),
                "foundation": (quiet / "modules/foundation.yaml").read_bytes(),
                "entities": (quiet / "modules/entities.yaml").read_bytes(),
                "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
                "linkml:types": _trusted_types(),
            },
            "quiet",
        )

    assert refusal.value.reason is BindingRefusalReason.UNKNOWN_REFERENCE


def test_validated_artifact_round_trip_needs_no_linkml_and_refuses_tampering() -> None:
    from malleus._contract_pipeline import (
        ArtifactRefusal,
        ArtifactRefusalReason,
        load_validated_contract_artifact,
    )

    compiled = _compile_binding(_small_shop_binding())
    loaded = load_validated_contract_artifact(compiled.artifact.artifact_bytes)

    assert loaded.content_hash == compiled.content_hash
    assert loaded.validate_instance(
        "SalesOrder", {"id": "O1", "order_number": "O1"}
    ) == []

    payload = json.loads(compiled.artifact.artifact_bytes)
    payload["facts"][0]["object"] = "tampered"
    tampered = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode()
    with pytest.raises(ArtifactRefusal) as refusal:
        load_validated_contract_artifact(tampered)
    assert refusal.value.reason is ArtifactRefusalReason.ARTIFACT_INTEGRITY_MISMATCH

    payload = json.loads(compiled.artifact.artifact_bytes)
    payload["grammar"] = "unknown"
    unknown = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode()
    with pytest.raises(ArtifactRefusal) as refusal:
        load_validated_contract_artifact(unknown)
    assert refusal.value.reason is ArtifactRefusalReason.UNSUPPORTED_ARTIFACT_GRAMMAR


def test_contract_view_drives_small_shop_knowledge_graph_validation() -> None:
    view = _compile_binding(_small_shop_binding()).view
    graph = KnowledgeGraph(view)

    order = graph.create_entity("SalesOrder", "O1", {"order_number": "O1"})
    unit = graph.create_entity("InventoryUnit", "X1", {"product_code": "X"})
    relation = graph.create_relation(
        "OrderContainsUnit",
        "contains:O1:X1",
        "O1",
        "X1",
        {"relation_type": "ORDER_CONTAINS_UNIT"},
    )
    wrong_enum = graph.create_relation(
        "OrderContainsUnit",
        "bad:O1:X1",
        "O1",
        "X1",
        {"relation_type": "WRONG"},
    )

    assert [order.op_status, unit.op_status, relation.op_status] == [
        OpStatus.COMMITTED,
        OpStatus.COMMITTED,
        OpStatus.COMMITTED,
    ]
    assert wrong_enum.op_status is OpStatus.REJECTED


def test_pipeline_values_are_frozen_and_missing_required_data_fails_loudly() -> None:
    result = _compile_binding(_small_shop_binding())

    with pytest.raises(FrozenInstanceError):
        result.elaborated.classes[0].abstract = True
    assert result.view.validate_instance("SalesOrder", {})


def test_legacy_lowerer_is_not_a_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args, **_kwargs):
        raise AssertionError("legacy lowerer was invoked")

    monkeypatch.setattr(compiler._LinkMLAdapter, "adapt", forbidden)
    path = GREENHOUSE / "baseline.yaml"

    result = compiler.compile_linkml_contract(path.read_bytes(), locator=path.as_uri())

    assert result.facts


def test_arbitrary_python_mapping_cannot_change_compiler_semantics() -> None:
    profile = json.loads(
        (ROOT / "src/malleus/_contract_compiler_profile.json").read_text()
    )
    profile["defaults"]["class"]["abstract"] = True
    source = (GREENHOUSE / "baseline.yaml").read_bytes()

    with pytest.raises(compiler.ContractCompileError, match="INVALID_PROFILE"):
        compiler.compile_linkml_contract(
            source,
            locator="memory:unidentified-profile",
            profile=profile,
        )

    baseline = compiler.compile_linkml_contract(
        source, locator="memory:canonical-profile"
    )
    assert baseline.facts_sha256 == sha256(baseline.canonical_facts).hexdigest()
