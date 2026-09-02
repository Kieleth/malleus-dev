"""Pareto controls for one reloadable compiler-to-structural-view boundary."""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import pytest

import malleus._contract_compiler as compiler
import malleus._contract_linkml_adapter as linkml_adapter
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
from malleus.ontology import OntologyRegistry


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
FEATURES = ROOT / "conformance/contract_kernel/v0/feature_cases/inputs"
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


def _small_shop_binding(
    *,
    description_variant: bool = False,
    source: bytes | None = None,
):
    source_name = (
        "small-shop-description-only.yaml"
        if description_variant
        else "small-shop.yaml"
    )
    return _binding(
        {
            "small-shop": source or (SMALL_SHOP / source_name).read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": _trusted_types(),
        },
        "small-shop",
    )


def _compile_binding(binding):
    from malleus._contract_pipeline import compile_binding

    return compile_binding(binding)


def _compile_feature(name: str):
    return _compile_binding(
        _binding(
            {
                name: (FEATURES / name).read_bytes(),
                "linkml:types": _trusted_types(),
            },
            name,
        )
    )


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def _rebind_fact_payload(payload: dict[str, object]) -> bytes:
    from malleus._contract_pipeline.view import _fact_set_digest

    facts = sorted(payload["facts"], key=_canonical_bytes)
    payload["facts"] = facts
    payload["fact_count"] = len(facts)
    facts_sha256 = "sha256:" + sha256(_canonical_bytes(facts)).hexdigest()
    payload["facts_sha256"] = facts_sha256
    payload["validated_fact_set_sha256"] = _fact_set_digest(
        facts_sha256, payload["metamodel"]["id"]
    )
    payload["evidence_sha256"] = "sha256:" + sha256(
        _canonical_bytes(payload["evidence"])
    ).hexdigest()
    return _canonical_bytes(payload)


def test_small_shop_elaborates_inheritance_slot_usage_enum_and_neutral_facts() -> None:
    result = _compile_binding(_small_shop_binding())
    view = result.view
    shop = "https://malleus.dev/schema/small-shop-fulfilment"
    foundation = "https://malleus.dev/schema"
    facts = set(result.facts)
    rdf_type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
    subclass = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
    vocabulary = "https://malleus.dev/contract-facts"

    assert view.is_subtype_of(f"{shop}/SalesOrder", f"{foundation}/Entity")
    assert view.is_subtype_of(
        f"{shop}/OrderContainsUnit", f"{foundation}/Relation"
    )
    assert view.has_mixin(f"{shop}/SalesOrder", f"{foundation}/Identifiable")
    assert view.get_slot_constraint(
        f"{shop}/SalesOrder", f"{shop}/order_number"
    ).required is True
    relation_kind = view.get_slot_constraint(
        f"{shop}/OrderContainsUnit", f"{foundation}/relation_type"
    )
    assert relation_kind.range == f"{shop}/ShopRelationKind"
    assert relation_kind.equals_string == "ORDER_CONTAINS_UNIT"
    assert view.get_enum_values(f"{shop}/ShopRelationKind") == frozenset(
        {"ORDER_CONTAINS_UNIT"}
    )
    assert compiler.ContractFact(
        f"{shop}/SalesOrder", subclass, f"{foundation}/Entity"
    ) in facts
    assert compiler.ContractFact(
        f"{shop}/ShopRelationKind", f"{vocabulary}/enumValue", "ORDER_CONTAINS_UNIT"
    ) in facts
    assert compiler.ContractFact(
        f"{foundation}/Entity", rdf_type, f"{vocabulary}/Class"
    ) in facts
    assert any(
        fact.predicate == f"{vocabulary}/usesSlot"
        and fact.object == f"{foundation}/id"
        for fact in facts
    )
    relation_type_use = next(
        fact.subject
        for fact in facts
        if fact.predicate == f"{vocabulary}/onClass"
        and fact.object == f"{shop}/OrderContainsUnit"
        and compiler.ContractFact(
            fact.subject,
            f"{vocabulary}/usesSlot",
            f"{foundation}/relation_type",
        )
        in facts
    )
    assert {
        compiler.ContractFact(
            relation_type_use,
            f"{vocabulary}/valueRange",
            f"{shop}/ShopRelationKind",
        ),
        compiler.ContractFact(
            relation_type_use, f"{vocabulary}/equalsString", "ORDER_CONTAINS_UNIT"
        ),
        compiler.ContractFact(relation_type_use, f"{vocabulary}/required", True),
    }.issubset(facts)
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

    changed_source = (SMALL_SHOP / "small-shop.yaml").read_bytes().replace(
        b"        required: true\n",
        b"        required: false\n",
        1,
    )
    changed = _compile_binding(_small_shop_binding(source=changed_source))
    assert changed.content_hash != baseline.content_hash


def test_root_instances_refuses_atomically_before_elaboration() -> None:
    source = (SMALL_SHOP / "small-shop-root-instances.yaml").read_bytes()

    with pytest.raises(compiler.ContractCompileError, match="instances"):
        compiler.compile_linkml_contract(source, locator="memory:root-instances")


def test_defaults_explicit_false_bounds_and_mixin_conflict_are_mechanical() -> None:
    explicit = _compile_feature("positive/valid_explicit_false.json")
    use = explicit.view.get_slot_constraint(
        "https://example.malleus.dev/d08-explicit-false/Record",
        "https://example.malleus.dev/d08-explicit-false/value",
    )
    assert use.required is False
    assert use.multivalued is False
    assert use.identifier is False
    assert use.inlined is False
    assert use.range == "https://malleus.dev/contract-facts/String"

    bounds = _compile_feature("x01/numeric_bounds.json")
    inherited = bounds.view.get_slot_constraint(
        "https://example.org/cc-x01/numeric-bounds/Child",
        "https://example.org/cc-x01/numeric-bounds/value",
    )
    assert inherited.minimum_value == 10
    assert inherited.maximum_value == 90

    from malleus._contract_pipeline import ElaborationRefusal, ElaborationRefusalReason

    for name in (
        "x01/conflicting_mixins_ab.json",
        "x01/conflicting_mixins_ba.json",
    ):
        with pytest.raises(ElaborationRefusal) as refusal:
            _compile_feature(name)
        assert refusal.value.reason is ElaborationRefusalReason.MIXIN_CONFLICT

    with pytest.raises(ElaborationRefusal):
        _compile_feature("x01/explicit_false.json")


def test_explicit_adoption_emits_the_authoritative_owner_once() -> None:
    owner = "https://example.malleus.dev/cc013/adoption-owner"
    adopter = "https://example.malleus.dev/cc013/adoption-subject"
    result = _compile_binding(
        _binding(
            {
                adopter: (FEATURES / "explicit_adoption/adopter.json").read_bytes(),
                owner: (FEATURES / "explicit_adoption/owner.json").read_bytes(),
            },
            adopter,
        )
    )
    owner_slot = f"{owner}/shared_value"
    adopter_slot = f"{adopter}/shared_value"

    assert sum(fact.subject == owner_slot for fact in result.facts) > 0
    assert all(fact.subject != adopter_slot for fact in result.facts)
    assert [slot.identifier for slot in result.elaborated.slots].count(owner_slot) == 1


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


def test_validated_artifact_round_trip_needs_no_source_or_linkml(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from malleus._contract_pipeline import load_validated_contract_artifact

    compiled = _compile_binding(_small_shop_binding())

    def forbidden(*_args, **_kwargs):
        raise AssertionError("artifact reload crossed the compiled boundary")

    monkeypatch.setattr(Path, "read_bytes", forbidden)
    monkeypatch.setattr(linkml_adapter, "_parse_linkml_source", forbidden)
    monkeypatch.setattr(OntologyRegistry, "__init__", forbidden)
    loaded = load_validated_contract_artifact(compiled.artifact.artifact_bytes)

    assert loaded.content_hash() == compiled.content_hash
    assert loaded.artifact_bytes == compiled.artifact.artifact_bytes
    assert loaded.validate_instance(
        "https://malleus.dev/schema/small-shop-fulfilment/SalesOrder",
        {
            "https://malleus.dev/schema/id": "O1",
            "https://malleus.dev/schema/small-shop-fulfilment/order_number": "O1",
        },
    ) == []


def test_validated_artifact_refuses_fact_and_bound_identity_tampering() -> None:
    from malleus._contract_pipeline import (
        ArtifactRefusal,
        ArtifactRefusalReason,
        load_validated_contract_artifact,
    )

    compiled = _compile_binding(_small_shop_binding())
    for malformed in (b'{"grammar":NaN}', b'{"grammar":"\\ud800"}'):
        with pytest.raises(ArtifactRefusal) as refusal:
            load_validated_contract_artifact(malformed)
        assert refusal.value.reason is ArtifactRefusalReason.MALFORMED_ARTIFACT

    payload = json.loads(compiled.artifact.artifact_bytes)
    payload["evidence"] = None
    payload["evidence_sha256"] = "sha256:" + sha256(
        _canonical_bytes(None)
    ).hexdigest()
    with pytest.raises(ArtifactRefusal) as refusal:
        load_validated_contract_artifact(_canonical_bytes(payload))
    assert refusal.value.reason is ArtifactRefusalReason.MALFORMED_ARTIFACT

    payload = json.loads(compiled.artifact.artifact_bytes)
    payload["fact_count"] = float(payload["fact_count"])
    with pytest.raises(ArtifactRefusal) as refusal:
        load_validated_contract_artifact(_canonical_bytes(payload))
    assert refusal.value.reason is ArtifactRefusalReason.ARTIFACT_INTEGRITY_MISMATCH

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

    for identity in ("metamodel", "canonicalization", "symbol_policy"):
        payload = json.loads(compiled.artifact.artifact_bytes)
        payload[identity]["sha256"] = "sha256:" + "0" * 64
        changed = json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode()
        with pytest.raises(ArtifactRefusal) as refusal:
            load_validated_contract_artifact(changed)
        assert (
            refusal.value.reason
            is ArtifactRefusalReason.ARTIFACT_INTEGRITY_MISMATCH
        )


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


def test_bare_slot_convenience_refuses_same_tail_ambiguity() -> None:
    from malleus._contract_pipeline import load_validated_contract_artifact

    compiled = _compile_binding(_small_shop_binding())
    payload = json.loads(compiled.artifact.artifact_bytes)
    shop = "https://malleus.dev/schema/small-shop-fulfilment"
    class_id = f"{shop}/SalesOrder"
    slot_id = f"{shop}/id"
    vocabulary = "https://malleus.dev/contract-facts"
    use_id = (
        "urn:malleus:contract-structure:slot-use:v0:sha256:"
        + sha256(
            _canonical_bytes(
                {
                    "class": class_id,
                    "domain": "malleus.contract-structure.slot-use/v0",
                    "slot": slot_id,
                }
            )
        ).hexdigest()
    )
    payload["facts"].extend(
        [
            {"object": f"{vocabulary}/Slot", "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "subject": slot_id},
            {"object": f"{vocabulary}/String", "predicate": f"{vocabulary}/valueRange", "subject": slot_id},
            {"object": False, "predicate": f"{vocabulary}/required", "subject": slot_id},
            {"object": False, "predicate": f"{vocabulary}/multivalued", "subject": slot_id},
            {"object": False, "predicate": f"{vocabulary}/identifier", "subject": slot_id},
            {"object": False, "predicate": f"{vocabulary}/inlined", "subject": slot_id},
            {"object": f"{vocabulary}/SlotUse", "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type", "subject": use_id},
            {"object": class_id, "predicate": f"{vocabulary}/onClass", "subject": use_id},
            {"object": slot_id, "predicate": f"{vocabulary}/usesSlot", "subject": use_id},
            {"object": f"{vocabulary}/String", "predicate": f"{vocabulary}/valueRange", "subject": use_id},
            {"object": False, "predicate": f"{vocabulary}/required", "subject": use_id},
            {"object": False, "predicate": f"{vocabulary}/multivalued", "subject": use_id},
            {"object": False, "predicate": f"{vocabulary}/identifier", "subject": use_id},
            {"object": False, "predicate": f"{vocabulary}/inlined", "subject": use_id},
        ]
    )
    view = load_validated_contract_artifact(_rebind_fact_payload(payload))

    with pytest.raises(ValueError, match="Ambiguous slot: id"):
        view.effective_slots("SalesOrder")


def test_pipeline_values_are_frozen_and_missing_required_data_fails_loudly() -> None:
    result = _compile_binding(_small_shop_binding())

    with pytest.raises(FrozenInstanceError):
        result.elaborated.classes[0].abstract = True
    with pytest.raises(AttributeError):
        result.view._classes = {}
    with pytest.raises(TypeError):
        result.view._classes["X"] = result.view.get_type("SalesOrder")
    sales_order = "https://malleus.dev/schema/small-shop-fulfilment/SalesOrder"
    with pytest.raises(TypeError):
        result.view._slot_uses[sales_order]["X"] = next(
            iter(result.view._slot_uses[sales_order].values())
        )
    assert result.view.validate_instance("SalesOrder", {})
    errors = result.view.validate_instance(
        "SalesOrder",
        {"id": "O1", "order_number": []},
    )
    assert any("must be singular" in error for error in errors)


def test_seed_primitive_cannot_be_redeclared_as_a_fact_subject() -> None:
    from malleus._contract_pipeline.model import SEED_METAMODEL_ID
    from malleus._contract_pipeline.view import _validate_fact_set

    seed = "https://malleus.dev/contract-facts/String"
    facts = (
        compiler.ContractFact(
            seed,
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "https://malleus.dev/contract-facts/Class",
        ),
        compiler.ContractFact(
            seed, "https://malleus.dev/contract-facts/abstract", False
        ),
        compiler.ContractFact(
            seed, "https://malleus.dev/contract-facts/isMixin", False
        ),
    )

    from malleus._contract_pipeline import ArtifactRefusal, ArtifactRefusalReason

    with pytest.raises(ArtifactRefusal) as refusal:
        _validate_fact_set(facts, SEED_METAMODEL_ID)
    assert refusal.value.reason is ArtifactRefusalReason.INVALID_FACT_SET


def test_artifact_refuses_bare_declaration_subject_under_qualified_policy() -> None:
    from malleus._contract_pipeline import (
        ArtifactRefusal,
        ArtifactRefusalReason,
        load_validated_contract_artifact,
    )

    payload = json.loads(
        _compile_binding(_small_shop_binding()).artifact.artifact_bytes
    )
    payload["facts"] = [
        {
            "object": False,
            "predicate": "https://malleus.dev/contract-facts/abstract",
            "subject": "X",
        },
        {
            "object": False,
            "predicate": "https://malleus.dev/contract-facts/isMixin",
            "subject": "X",
        },
        {
            "object": "https://malleus.dev/contract-facts/Class",
            "predicate": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "subject": "X",
        },
    ]

    with pytest.raises(ArtifactRefusal) as refusal:
        load_validated_contract_artifact(_rebind_fact_payload(payload))
    assert refusal.value.reason is ArtifactRefusalReason.INVALID_FACT_SET


def test_artifact_evidence_must_be_one_rooted_import_closure() -> None:
    from malleus._contract_pipeline import (
        ArtifactRefusal,
        ArtifactRefusalReason,
        load_validated_contract_artifact,
    )

    payload = json.loads(
        _compile_binding(_small_shop_binding()).artifact.artifact_bytes
    )
    source = dict(payload["evidence"]["sources"][0])
    source.update(
        {
            "byte_length": 1,
            "module_id": "unconnected",
            "schema_id": "https://evil.example/schema",
            "sha256": "sha256:" + sha256(b"x").hexdigest(),
            "trusted": False,
        }
    )
    payload["evidence"]["sources"].append(source)

    with pytest.raises(ArtifactRefusal) as refusal:
        load_validated_contract_artifact(_rebind_fact_payload(payload))
    assert refusal.value.reason is ArtifactRefusalReason.MALFORMED_ARTIFACT


def test_trusted_source_schema_cannot_author_declaration_facts() -> None:
    from malleus._contract_pipeline import (
        ArtifactRefusal,
        ArtifactRefusalReason,
        load_validated_contract_artifact,
    )

    payload = json.loads(
        _compile_binding(_small_shop_binding()).artifact.artifact_bytes
    )
    foundation = next(
        source
        for source in payload["evidence"]["sources"]
        if source["module_id"] == "malleus"
    )
    foundation["trusted"] = True

    with pytest.raises(ArtifactRefusal) as refusal:
        load_validated_contract_artifact(_rebind_fact_payload(payload))
    assert refusal.value.reason is ArtifactRefusalReason.INVALID_FACT_SET


def test_legacy_lowerer_is_absent_and_cannot_be_a_fallback() -> None:
    implementation = Path(compiler.__file__).read_text(encoding="utf-8")
    tree = ast.parse(implementation)
    definitions = {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.ClassDef, ast.FunctionDef))
    }

    assert not hasattr(compiler, "_LinkMLAdapter")
    assert "_LinkMLAdapter" not in definitions
    assert {
        "_emit_classes",
        "_emit_enums",
        "_emit_expressions",
        "_emit_slots",
        "_emit_types",
        "_emit_uses",
    }.isdisjoint(definitions)
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
