"""Hard checks for the paper-local compiled-IR GraphRecipe adapter."""

from __future__ import annotations

from dataclasses import replace

import pytest

from malleus.kg import OpType
from malleus.staging import ProposedOperation
from research.ontology_driven_kg_realization.experiments.document_paper import (
    compiled_graph_recipe_contract as adapter_module,
)
from research.ontology_driven_kg_realization.experiments.document_paper.compiled_graph_recipe_contract import (
    BASE,
    XSD,
    derive_compiled_logical_contract,
    require_plan_contract_alignment,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.assembly import (
    AssemblyPlan,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.model import (
    ConstructionMember,
    GraphRecipeFailure,
)
from tests.contract_compiler.pareto.test_validated_contract import (
    ROOT,
    _binding,
    _compile_binding,
    _trusted_types,
)


DOMAIN = "https://example.malleus.dev/paper-domain"
FOUNDATION = "https://malleus.dev/schema"
CONTRACT_ID = "https://example.malleus.dev/contracts/paper-domain"
RECORDS = tuple(
    DOMAIN + "/" + name
    for name in ("MeasuredSubject", "Observation", "ObservationAtSite")
)


SOURCE = b"""\
id: https://example.malleus.dev/paper-domain
name: paper_domain
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
imports:
  - linkml:types
  - malleus
enums:
  FindingKind:
    permissible_values:
      REPORTED: {}
      CALCULATED: {}
  PaperRelationKind:
    permissible_values:
      OBSERVATION_AT_SITE: {}
classes:
  MeasuredSubject:
    is_a: Entity
    abstract: true
  Observation:
    is_a: Entity
    slots:
      - observed_at
      - finding_kind
      - lower_bound
      - upper_bound
      - inline_subject
    slot_usage:
      name:
        required: true
  ObservationAtSite:
    is_a: Relation
    slot_usage:
      relation_type:
        range: PaperRelationKind
        required: true
        equals_string: OBSERVATION_AT_SITE
      source_id:
        range: Observation
        required: true
      target_id:
        range: MeasuredSubject
        required: true
  DomainSignal:
    is_a: Signal
slots:
  observed_at:
    range: timestamp
    required: true
  finding_kind:
    range: FindingKind
    required: true
  lower_bound:
    range: float
    required: true
    minimum_value: 0.4
  upper_bound:
    range: float
    required: true
    maximum_value: 3.0
  inline_subject:
    range: MeasuredSubject
    required: true
    inlined: true
"""


def _compiled(source: bytes = SOURCE):
    return _compile_binding(
        _binding(
            {
                "paper": source,
                "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
                "linkml:types": _trusted_types(),
            },
            "paper",
        )
    )


@pytest.fixture(scope="module")
def compiled():
    return _compiled()


@pytest.fixture(scope="module")
def contract(compiled):
    return derive_compiled_logical_contract(
        compiled,
        record_type_iris=RECORDS,
        contract_id=CONTRACT_ID,
    )


def _slot(contract, record: str, symbol: str):
    return next(
        item
        for item in contract.record_for_iri(DOMAIN + "/" + record).slots
        if item.runtime_symbol == symbol
    )


def test_projects_enum_and_imported_timestamp_without_source_registry(
    compiled,
    contract,
) -> None:
    observation = contract.record_for_iri(DOMAIN + "/Observation")
    measured = contract.record_for_iri(DOMAIN + "/MeasuredSubject")
    relation = contract.record_for_iri(DOMAIN + "/ObservationAtSite")

    assert contract.registry_hash == compiled.artifact.validated_fact_set_sha256
    assert observation.role == "ENTITY"
    assert observation.legal_operation_kind == BASE + "CreateEntity"
    assert measured.abstract is True
    assert measured.legal_operation_kind is None
    assert relation.role == "RELATION"
    assert relation.legal_operation_kind == BASE + "CreateRelation"
    assert relation.endpoint_constraints.source == DOMAIN + "/Observation"
    assert relation.endpoint_constraints.target == DOMAIN + "/MeasuredSubject"

    assert _slot(contract, "Observation", "observed_at").constraints.range == (
        XSD + "dateTime"
    )
    assert _slot(contract, "Observation", "created_at").constraints.range == (
        XSD + "dateTime"
    )
    finding = _slot(contract, "Observation", "finding_kind").constraints
    assert finding.range == DOMAIN + "/FindingKind"
    assert finding.required is True
    assert _slot(contract, "Observation", "id").constraints.identifier is True
    assert _slot(contract, "Observation", "tags").constraints.multivalued is True
    assert _slot(contract, "Observation", "inline_subject").constraints.inlined is True
    assert _slot(contract, "Observation", "created_at").constraints.required is False
    assert (
        _slot(contract, "Observation", "lower_bound").constraints.minimum_value == 0.4
    )
    assert _slot(contract, "Observation", "upper_bound").constraints.maximum_value == 3
    relation_kind = _slot(
        contract,
        "ObservationAtSite",
        "relation_type",
    ).constraints
    assert relation_kind.range == DOMAIN + "/PaperRelationKind"
    assert relation_kind.equals_string == "OBSERVATION_AT_SITE"

    assert FOUNDATION + "/Event" not in {
        item.type_iri for item in contract.record_types
    }
    assert contract.symbol_bindings.derivation == "compiled-frontend-neutral-ir"
    assert {item.iri for item in contract.symbol_bindings.types} == set(RECORDS)


def test_contract_digest_is_exact_and_independent_of_selection_order(
    compiled,
    contract,
) -> None:
    reordered = derive_compiled_logical_contract(
        compiled,
        record_type_iris=tuple(reversed(RECORDS)),
        contract_id=CONTRACT_ID,
    )

    assert reordered.identity_payload() == contract.identity_payload()
    assert reordered.contract_digest == contract.contract_digest
    assert contract.contract_digest == (
        "sha256:f9926be0955aa059484a51c2b3bb31b624b24f467072ac811531d39a14a194cd"
    )


@pytest.mark.parametrize(
    ("selection", "evidence_key"),
    (
        ((RECORDS[0], RECORDS[0]), "record_type_iris"),
        ((DOMAIN + "/Missing",), "unknown_record_types"),
        ((FOUNDATION + "/Entity",), "imported_role_roots"),
        ((FOUNDATION + "/Identifiable",), "mixin_record_types"),
        ((FOUNDATION + "/Signal",), "imported_role_roots"),
        ((DOMAIN + "/DomainSignal",), "matching_roles"),
    ),
)
def test_selection_refuses_duplicates_unknowns_roots_mixins_and_other_roles(
    compiled,
    selection,
    evidence_key,
) -> None:
    with pytest.raises(GraphRecipeFailure) as refusal:
        derive_compiled_logical_contract(
            compiled,
            record_type_iris=selection,
            contract_id=CONTRACT_ID,
        )

    diagnostic = refusal.value.diagnostics[0]
    assert diagnostic.code == "COMPILED_LOGICAL_CONTRACT_DERIVATION_FAILED"
    assert evidence_key in diagnostic.evidence or evidence_key in diagnostic.subject


def test_runtime_symbol_collision_refuses() -> None:
    with pytest.raises(GraphRecipeFailure) as refusal:
        adapter_module._reject_suffix_collisions(
            {
                "https://example.malleus.dev/a/Shared",
                "https://example.malleus.dev/b/Shared",
            },
            kind="record type",
        )

    assert refusal.value.diagnostics[0].evidence["collisions"] == {
        "Shared": [
            "https://example.malleus.dev/a/Shared",
            "https://example.malleus.dev/b/Shared",
        ]
    }


def _plan(contract, *, operation_record_type: str = "Observation") -> AssemblyPlan:
    member_iri = "https://example.malleus.dev/member/observation-1"
    member = ConstructionMember(
        member=member_iri,
        operation_kind=BASE + "CreateEntity",
        record_type=DOMAIN + "/Observation",
        record_id="observation:1",
    )
    operation = ProposedOperation(
        op_type=OpType.CREATE_ENTITY,
        record_type=operation_record_type,
        record_id="observation:1",
        properties={},
    )
    digest = "sha256:" + "1" * 64
    return AssemblyPlan(
        contract_digest=contract.contract_digest,
        invocation_digests=(digest,),
        members=(member,),
        dependencies=(),
        topological_order=(member_iri,),
        operations=(operation,),
        operation_members=(member_iri,),
        member_emissions=((member_iri, (("emission:1", "path:1"),)),),
        plan_digest=digest,
    )


def test_plan_guard_accepts_exact_compiled_contract_and_runtime_symbol(
    compiled,
    contract,
) -> None:
    plan = _plan(contract)
    assert require_plan_contract_alignment(plan, contract, compiled) is plan


def test_plan_guard_refuses_contract_and_runtime_symbol_drift(
    compiled,
    contract,
) -> None:
    plan = _plan(contract)
    wrong_registry = replace(contract, registry_hash="sha256:" + "2" * 64)
    wrong_plan_contract = replace(plan, contract_digest="sha256:" + "3" * 64)
    wrong_runtime = _plan(contract, operation_record_type="WrongObservation")

    for candidate_plan, candidate_contract in (
        (plan, wrong_registry),
        (wrong_plan_contract, contract),
        (wrong_runtime, contract),
    ):
        with pytest.raises(GraphRecipeFailure) as refusal:
            require_plan_contract_alignment(
                candidate_plan,
                candidate_contract,
                compiled,
            )
        assert refusal.value.diagnostics[0].code == ("COMPILED_LOGICAL_CONTRACT_DRIFT")
