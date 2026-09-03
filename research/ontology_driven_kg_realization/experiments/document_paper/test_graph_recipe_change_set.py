"""Focused contract for the paper-local GraphRecipe history seam."""

from __future__ import annotations

import ast
from dataclasses import replace
from hashlib import sha256
import inspect
import json
from pathlib import Path

import pytest

from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeHistory,
    KnowledgeChangeHistoryBinding,
    KnowledgeChangeRefusal,
    KnowledgeChangeRefusalReason,
    KnowledgeValidTime,
)
from malleus.kg import OpType
from malleus.ledger import content_digest
from malleus.ontology import OntologyRegistry
from malleus.staging import ProposedOperation
from research.ontology_driven_kg_realization.experiments.document_paper import (
    graph_recipe_change_set as adapter_module,
)
from research.ontology_driven_kg_realization.experiments.document_paper.graph_recipe_change_set import (
    GraphRecipeChangeSetError,
    HistoryBaseCoordinates,
    RetainedReference,
    assembly_plan_to_change_set,
    canonical_assembly_plan_bytes,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.assembly import (
    AssemblyPlan,
    assemble_plan,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.contract import (
    derive_logical_contract,
    load_ontology_symbol_bindings,
)
from research.ontology_driven_kg_realization.experiments.graph_recipe.stottr import (
    RecipeTerm,
    compile_graph_recipe,
    expand_invocation,
    parse_stottr,
)
from tests.contract_compiler.pareto.test_protocol_machine import (
    CHECKS,
    POLICY_ID,
    _canonical,
    _effective,
    _event,
    _load_policy,
)
from tests.contract_compiler.pareto.test_validated_contract import (
    ROOT as CONTRACT_ROOT,
    _binding,
    _compile_binding,
    _trusted_types,
)


ROOT = Path(__file__).resolve().parents[4]
CORPUS = ROOT / "conformance" / "graph_recipe" / "v0"
GE020 = CORPUS / "experiments" / "ge-020-two-nodes-one-relation"
TRANSACTION_TIME = "2026-09-01T00:00:00Z"
PROFILE_ID = "https://malleus.dev/graph-recipe/profile/v0"


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _ge020_plan() -> AssemblyPlan:
    registry = OntologyRegistry(GE020 / "input" / "ontology.yaml")
    bindings = load_ontology_symbol_bindings(
        GE020 / "input" / "ontology-symbol-bindings.json"
    )
    contract = derive_logical_contract(
        registry,
        bindings,
        "https://fixtures.malleus.dev/graph-recipe/v0/contract/employment",
    )
    compiled = compile_graph_recipe(
        (
            parse_stottr(
                (CORPUS / "base" / "malleus-base-v0.stottr").read_bytes(),
                "base/malleus-base-v0.stottr",
            ),
            parse_stottr(
                (GE020 / "input" / "recipe.stottr").read_bytes(),
                "experiments/ge-020-two-nodes-one-relation/input/recipe.stottr",
            ),
        ),
        root_template=(
            "https://fixtures.malleus.dev/graph-recipe/v0/recipe/Employment-1.0.0"
        ),
        contract_digest=contract.contract_digest,
        profile_id=PROFILE_ID,
        expansion_profile_id=PROFILE_ID,
    )
    names = (
        "personMember",
        "personId",
        "personName",
        "organizationMember",
        "organizationId",
        "organizationName",
        "employmentMember",
        "employmentId",
    )
    values = (
        RecipeTerm.iri(
            "https://fixtures.malleus.dev/graph-recipe/v0/member/ge-020/01-person"
        ),
        RecipeTerm.literal("person:alice"),
        RecipeTerm.literal("Alice"),
        RecipeTerm.iri(
            "https://fixtures.malleus.dev/graph-recipe/v0/member/ge-020/02-organization"
        ),
        RecipeTerm.literal("org:acme"),
        RecipeTerm.literal("Acme"),
        RecipeTerm.iri(
            "https://fixtures.malleus.dev/graph-recipe/v0/member/ge-020/03-employment"
        ),
        RecipeTerm.literal("employment:alice-acme"),
    )
    expansion = expand_invocation(
        compiled,
        invocation_id=(
            "https://fixtures.malleus.dev/graph-recipe/v0/invocation/ge-020-employment"
        ),
        arguments=dict(zip(names, values, strict=True)),
    )
    return assemble_plan(
        contract,
        expansion.emissions,
        invocation_digests=(expansion.invocation_digest,),
    )


def _plan_with_operations(
    plan: AssemblyPlan,
    operations: tuple[ProposedOperation, ...],
) -> AssemblyPlan:
    draft = replace(
        plan,
        operations=operations,
        plan_digest="sha256:" + "0" * 64,
    )
    digest = content_digest(
        {
            "schema_version": "graph-recipe-plan-v0",
            "contract_digest": draft.contract_digest,
            "invocation_digests": list(draft.invocation_digests),
            "member_graph": draft.member_graph_artifact(),
            "proposed_operations": draft.proposed_operations_artifact(),
        }
    )
    return replace(draft, plan_digest=digest)


def _history_binding() -> KnowledgeChangeHistoryBinding:
    return KnowledgeChangeHistoryBinding.from_bytes(
        _canonical(
            {
                "accept_verdict": "ACCEPT",
                "decision": {
                    "event_type": "VERDICT_RECORDED",
                    "proposal_id_field": "proposal_id",
                    "record_type": "DecisionRecord",
                    "verdict_field": "verdict",
                },
                "grammar": "malleus.knowledge-history-binding/private-v0",
                "proposal": {
                    "change_set_identity_field": "knowledge_change_set_identity",
                    "event_type": "CHANGE_PROPOSED",
                    "proposal_id_field": "proposal_id",
                    "record_type": "ProposalRecord",
                },
                "retention_events": {
                    "ARTIFACT_REGISTERED": {
                        "identity_field": "artifact_identity",
                        "record_id_field": "artifact_id",
                    },
                    "SOURCE_REGISTERED": {
                        "identity_field": "source_identity",
                        "record_id_field": "source_id",
                    },
                },
            }
        )
    )


@pytest.fixture(scope="module")
def history_contract():
    source = b"""\
id: https://example.malleus.dev/document-paper
name: document_paper
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
imports:
  - linkml:types
  - malleus
enums:
  WorkKind:
    permissible_values:
      WORKS_FOR:
classes:
  Person:
    is_a: Entity
    slot_usage:
      name:
        required: true
  Organization:
    is_a: Entity
    slot_usage:
      name:
        required: true
  WorksForRelation:
    is_a: Relation
    slot_usage:
      relation_type:
        range: WorkKind
        required: true
        equals_string: WORKS_FOR
      source_id:
        range: Person
        required: true
      target_id:
        range: Organization
        required: true
"""
    compiled = _compile_binding(
        _binding(
            {
                "paper": source,
                "malleus": (CONTRACT_ROOT / "ontology/malleus.yaml").read_bytes(),
                "linkml:types": _trusted_types(),
            },
            "paper",
        )
    )
    partial = _effective(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256
    )
    return compiled, partial, _history_binding()


def _anchor(
    history: KnowledgeChangeHistory,
    *,
    event: bytes,
    retained: bytes,
    role: str,
) -> None:
    history.append_anchor(
        machine_event=event,
        retained_bytes=retained,
        media_type="application/octet-stream",
        role=role,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:paper-test",
    )


def _anchored_history(tmp_path: Path, history_contract, plan: AssemblyPlan):
    compiled, partial, binding = history_contract
    history = KnowledgeChangeHistory(
        tmp_path / "history.jsonl",
        partial_contract=partial,
        contract_view=compiled.view,
        binding=binding,
    )
    source_bytes = b"retained paper source\n"
    plan_bytes = canonical_assembly_plan_bytes(plan)
    anchors = (
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="validated-contract",
                artifact_identity=_digest(compiled.artifact.artifact_bytes),
            ),
            compiled.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="partial-contract",
                artifact_identity=_digest(partial.canonical_bytes),
            ),
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="history-binding",
                artifact_identity=_digest(binding.canonical_bytes),
            ),
            binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="paper-source-artifact",
                artifact_identity=_digest(source_bytes),
            ),
            source_bytes,
            "SOURCE_ARTIFACT",
        ),
        (
            _event(
                "SOURCE_REGISTERED",
                artifact_id="paper-source-artifact",
                source_id="paper-source",
                source_identity=_digest(source_bytes),
            ),
            source_bytes,
            "RETAINED_SOURCE",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="graph-recipe-plan",
                artifact_identity=_digest(plan_bytes),
            ),
            plan_bytes,
            "RETAINED_EVIDENCE",
        ),
    )
    for event, retained, role in anchors:
        _anchor(history, event=event, retained=retained, role=role)
    return history, partial, source_bytes, plan_bytes


def _base(history: KnowledgeChangeHistory) -> HistoryBaseCoordinates:
    replay = history.replay()
    return HistoryBaseCoordinates(
        ledger_head=replay.ledger_head,
        ledger_event_count=replay.ledger_event_count,
        acceptance_head=replay.acceptance_head,
        materialization_head=replay.materialization_head,
        accepted_state_digest=replay.graph.state_digest(),
    )


def _change(
    history: KnowledgeChangeHistory,
    partial,
    source_bytes: bytes,
    plan: AssemblyPlan,
    *,
    base: HistoryBaseCoordinates | None = None,
):
    return assembly_plan_to_change_set(
        plan,
        change_set_id="paper-change-1",
        contract_identity=partial.identity,
        base=base if base is not None else _base(history),
        sources=(RetainedReference("paper-source", _digest(source_bytes)),),
        evidence=(RetainedReference("graph-recipe-plan", plan.plan_digest),),
        valid_time=KnowledgeValidTime("INSTANT", TRANSACTION_TIME),
        supersedes=(),
    )


def _protocol_events(change_set, machine_state_identity: str) -> tuple[bytes, ...]:
    policy = _load_policy()
    proposal_id = "proposal-paper-1"
    proposal = _event(
        "CHANGE_PROPOSED",
        expected_machine_state_identity=machine_state_identity,
        knowledge_change_set_identity=change_set.identity,
        policy_id=POLICY_ID,
        policy_identity=policy.identity,
        proposal_id=proposal_id,
    )
    checks = tuple(
        _event(
            "CHECK_RECORDED",
            check_contract_id=check_id,
            check_contract_identity=check_identity,
            outcome="SATISFIED",
            policy_identity=policy.identity,
            proposal_id=proposal_id,
            receipt_id=f"receipt-paper-{index}",
        )
        for index, (check_id, check_identity) in enumerate(CHECKS)
    )
    decision = _event(
        "VERDICT_RECORDED",
        decision_id="decision-paper-1",
        proposal_id=proposal_id,
    )
    return (proposal, *checks, decision)


def test_ge020_mapping_is_deterministic_and_preserves_plan_semantics() -> None:
    plan = _ge020_plan()
    base = HistoryBaseCoordinates(
        ledger_head="sha256:" + "1" * 64,
        ledger_event_count=6,
        acceptance_head="GENESIS",
        materialization_head="GENESIS",
        accepted_state_digest="sha256:" + "2" * 64,
    )
    arguments = {
        "change_set_id": "paper-change-1",
        "contract_identity": "sha256:" + "3" * 64,
        "base": base,
        "sources": (RetainedReference("paper-source", "sha256:" + "4" * 64),),
        "evidence": (RetainedReference("graph-recipe-plan", plan.plan_digest),),
        "valid_time": KnowledgeValidTime("ORDER_ONLY", "paper-order-1"),
        "supersedes": (),
    }

    first = assembly_plan_to_change_set(plan, **arguments)
    second = assembly_plan_to_change_set(plan, **arguments)

    assert first.canonical_bytes == second.canonical_bytes
    assert first.identity == second.identity
    assert first.contract_identity == arguments["contract_identity"]
    assert first.base_ledger_head == base.ledger_head
    assert first.base_ledger_event_count == base.ledger_event_count
    assert first.base_acceptance_head == base.acceptance_head
    assert first.base_materialization_head == base.materialization_head
    assert first.base_accepted_state_digest == base.accepted_state_digest
    assert first.sources == (("paper-source", "sha256:" + "4" * 64),)
    assert first.evidence == (("graph-recipe-plan", plan.plan_digest),)
    assert [operation.operation_id for operation in first.operations] == list(
        plan.operation_members
    )
    assert [operation.operation_type for operation in first.operations] == [
        "CREATE_ENTITY",
        "CREATE_ENTITY",
        "CREATE_RELATION",
    ]
    assert [operation.record_id for operation in first.operations] == [
        "person:alice",
        "org:acme",
        "employment:alice-acme",
    ]
    assert first.operations[0].depends_on == ()
    assert first.operations[1].depends_on == ()
    assert first.operations[2].depends_on == (
        plan.operation_members[0],
        plan.operation_members[1],
    )
    data = json.loads(first.canonical_bytes)
    assert "source_id" not in data["operations"][0]
    assert "target_id" not in data["operations"][1]
    assert data["operations"][2]["source_id"] == "person:alice"
    assert data["operations"][2]["target_id"] == "org:acme"
    assert _digest(canonical_assembly_plan_bytes(plan)) == plan.plan_digest


def test_self_digested_plan_with_operations_swapped_is_refused() -> None:
    plan = _ge020_plan()
    swapped = _plan_with_operations(
        plan,
        (plan.operations[1], plan.operations[0], *plan.operations[2:]),
    )
    assert _digest(canonical_assembly_plan_bytes(swapped)) == swapped.plan_digest

    with pytest.raises(GraphRecipeChangeSetError, match="record_id does not match"):
        assembly_plan_to_change_set(
            swapped,
            change_set_id="paper-change-1",
            contract_identity="sha256:" + "3" * 64,
            base=HistoryBaseCoordinates(
                "sha256:" + "1" * 64,
                1,
                "GENESIS",
                "GENESIS",
                "sha256:" + "2" * 64,
            ),
            sources=(RetainedReference("paper-source", "sha256:" + "4" * 64),),
            evidence=(RetainedReference("graph-recipe-plan", swapped.plan_digest),),
            valid_time=KnowledgeValidTime("ORDER_ONLY", "paper-order-1"),
            supersedes=(),
        )


def test_self_digested_supported_operation_kind_mismatch_is_refused() -> None:
    plan = _ge020_plan()
    entity = plan.operations[0]
    mismatched = _plan_with_operations(
        plan,
        (
            ProposedOperation.relation(
                entity.record_type,
                entity.record_id,
                "person:source",
                "org:target",
                entity.properties,
            ),
            *plan.operations[1:],
        ),
    )
    assert _digest(canonical_assembly_plan_bytes(mismatched)) == (
        mismatched.plan_digest
    )

    with pytest.raises(GraphRecipeChangeSetError, match="type does not match"):
        assembly_plan_to_change_set(
            mismatched,
            change_set_id="paper-change-1",
            contract_identity="sha256:" + "3" * 64,
            base=HistoryBaseCoordinates(
                "sha256:" + "1" * 64,
                1,
                "GENESIS",
                "GENESIS",
                "sha256:" + "2" * 64,
            ),
            sources=(RetainedReference("paper-source", "sha256:" + "4" * 64),),
            evidence=(RetainedReference("graph-recipe-plan", mismatched.plan_digest),),
            valid_time=KnowledgeValidTime("ORDER_ONLY", "paper-order-1"),
            supersedes=(),
        )


def test_accepted_change_reopens_to_the_same_graph(
    tmp_path: Path,
    history_contract,
) -> None:
    plan = _ge020_plan()
    history, partial, source_bytes, _ = _anchored_history(
        tmp_path,
        history_contract,
        plan,
    )
    before = history.replay()
    change_set = _change(history, partial, source_bytes, plan)

    admitted = history.admit(
        change_set=change_set,
        machine_events=_protocol_events(change_set, before.machine_state.identity),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:paper-test",
    )
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()

    assert reopened.graph.snapshot() == admitted.graph.snapshot()
    assert reopened.graph.state_digest() == admitted.graph.state_digest()
    assert reopened.receipt.canonical_bytes == admitted.receipt.canonical_bytes
    assert reopened.change_sets[0].canonical_bytes == change_set.canonical_bytes
    assert reopened.graph.query("Person", name="Alice") == [
        {"id": "person:alice", "name": "Alice", "type": "Person"}
    ]
    assert reopened.graph.query_relations(
        "WorksForRelation",
        source_id="person:alice",
        target_id="org:acme",
    ) == [
        {
            "key": "employment:alice-acme",
            "relation_type": "WORKS_FOR",
            "source_id": "person:alice",
            "target_id": "org:acme",
            "type": "WorksForRelation",
        }
    ]


@pytest.mark.parametrize(
    ("failure", "reason"),
    (
        ("stale-base", KnowledgeChangeRefusalReason.STALE_BASE),
        ("invalid-relation", KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL),
    ),
)
def test_refusal_is_atomic_for_ledger_and_replay_graph(
    tmp_path: Path,
    history_contract,
    failure: str,
    reason: KnowledgeChangeRefusalReason,
) -> None:
    plan = _ge020_plan()
    if failure == "invalid-relation":
        relation = plan.operations[-1]
        plan = _plan_with_operations(
            plan,
            (
                *plan.operations[:-1],
                ProposedOperation(
                    relation.op_type,
                    relation.record_type,
                    relation.record_id,
                    {"relation_type": "INVALID"},
                    relation.source_id,
                    relation.target_id,
                ),
            ),
        )
    history, partial, source_bytes, _ = _anchored_history(
        tmp_path,
        history_contract,
        plan,
    )
    before = history.replay()
    base = _base(history)
    if failure == "stale-base":
        base = replace(
            base,
            accepted_state_digest="sha256:" + "9" * 64,
        )
    change_set = _change(
        history,
        partial,
        source_bytes,
        plan,
        base=base,
    )
    ledger_before = history.path.read_bytes()

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        history.admit(
            change_set=change_set,
            machine_events=_protocol_events(
                change_set,
                before.machine_state.identity,
            ),
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:paper-test",
        )

    assert refusal.value.reason is reason
    after = history.replay()
    assert history.path.read_bytes() == ledger_before
    assert after.graph.snapshot() == before.graph.snapshot()
    assert after.graph.state_digest() == before.graph.state_digest()
    assert after.machine_state.identity == before.machine_state.identity


@pytest.mark.parametrize("op_type", (OpType.CREATE_SIGNAL, OpType.CREATE_EVENT))
def test_signal_and_event_operations_fail_at_the_adapter(op_type: OpType) -> None:
    plan = _ge020_plan()
    operation = plan.operations[0]
    unsupported = _plan_with_operations(
        plan,
        (
            ProposedOperation(
                op_type,
                operation.record_type,
                operation.record_id,
                operation.properties,
            ),
            *plan.operations[1:],
        ),
    )

    with pytest.raises(GraphRecipeChangeSetError, match="unsupported"):
        assembly_plan_to_change_set(
            unsupported,
            change_set_id="paper-change-1",
            contract_identity="sha256:" + "3" * 64,
            base=HistoryBaseCoordinates(
                "sha256:" + "1" * 64,
                1,
                "GENESIS",
                "GENESIS",
                "sha256:" + "2" * 64,
            ),
            sources=(RetainedReference("paper-source", "sha256:" + "4" * 64),),
            evidence=(RetainedReference("graph-recipe-plan", unsupported.plan_digest),),
            valid_time=KnowledgeValidTime("ORDER_ONLY", "paper-order-1"),
            supersedes=(),
        )


def test_required_values_are_strict_and_plan_evidence_is_mandatory() -> None:
    plan = _ge020_plan()
    base = HistoryBaseCoordinates(
        "sha256:" + "1" * 64,
        1,
        "GENESIS",
        "GENESIS",
        "sha256:" + "2" * 64,
    )
    with pytest.raises(GraphRecipeChangeSetError, match="evidence must include"):
        assembly_plan_to_change_set(
            plan,
            change_set_id="paper-change-1",
            contract_identity="sha256:" + "3" * 64,
            base=base,
            sources=(RetainedReference("paper-source", "sha256:" + "4" * 64),),
            evidence=(RetainedReference("other", "sha256:" + "5" * 64),),
            valid_time=KnowledgeValidTime("ORDER_ONLY", "paper-order-1"),
            supersedes=(),
        )
    with pytest.raises(GraphRecipeChangeSetError, match="ordered nonempty tuple"):
        assembly_plan_to_change_set(
            plan,
            change_set_id="paper-change-1",
            contract_identity="sha256:" + "3" * 64,
            base=base,
            sources=(),
            evidence=(RetainedReference("graph-recipe-plan", plan.plan_digest),),
            valid_time=KnowledgeValidTime("ORDER_ONLY", "paper-order-1"),
            supersedes=(),
        )
    with pytest.raises(TypeError):
        assembly_plan_to_change_set(
            plan,
            change_set_id="paper-change-1",
            contract_identity="sha256:" + "3" * 64,
            sources=(RetainedReference("paper-source", "sha256:" + "4" * 64),),
            evidence=(RetainedReference("graph-recipe-plan", plan.plan_digest),),
            valid_time=KnowledgeValidTime("ORDER_ONLY", "paper-order-1"),
            supersedes=(),
        )
    with pytest.raises(GraphRecipeChangeSetError, match="disagree"):
        HistoryBaseCoordinates(
            "GENESIS",
            1,
            "GENESIS",
            "GENESIS",
            "sha256:" + "2" * 64,
        )
    with pytest.raises(GraphRecipeChangeSetError, match="nonblank"):
        RetainedReference("", "sha256:" + "4" * 64)
    with pytest.raises(GraphRecipeChangeSetError, match="sha256"):
        RetainedReference("paper-source", "not-a-digest")


def test_accepted_adapter_path_has_no_direct_staging_dependency(monkeypatch) -> None:
    tree = ast.parse(inspect.getsource(adapter_module))
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    } | {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    references = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)} | {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    }
    assert imported_modules.isdisjoint({"malleus.kg", "malleus.staging"})
    assert references.isdisjoint(
        {
            "CandidateSubgraph",
            "KnowledgeGraph",
            "create_entity",
            "create_relation",
            "materialize_into",
            "stage_and_materialize",
            "stage_subgraph",
        }
    )

    from research.ontology_driven_kg_realization.experiments.graph_recipe import (
        assembly,
    )
    from malleus import staging
    from malleus.kg import KnowledgeGraph

    def forbid_direct_staging(*args, **kwargs):
        raise AssertionError("paper adapter entered direct graph staging")

    monkeypatch.setattr(assembly, "stage_and_materialize", forbid_direct_staging)
    monkeypatch.setattr(staging, "stage_subgraph", forbid_direct_staging)
    monkeypatch.setattr(KnowledgeGraph, "create_entity", forbid_direct_staging)
    monkeypatch.setattr(KnowledgeGraph, "create_relation", forbid_direct_staging)
    plan = _ge020_plan()
    change_set = assembly_plan_to_change_set(
        plan,
        change_set_id="paper-change-1",
        contract_identity="sha256:" + "3" * 64,
        base=HistoryBaseCoordinates(
            "sha256:" + "1" * 64,
            1,
            "GENESIS",
            "GENESIS",
            "sha256:" + "2" * 64,
        ),
        sources=(RetainedReference("paper-source", "sha256:" + "4" * 64),),
        evidence=(RetainedReference("graph-recipe-plan", plan.plan_digest),),
        valid_time=KnowledgeValidTime("ORDER_ONLY", "paper-order-1"),
        supersedes=(),
    )
    assert change_set.operations[-1].operation_type == "CREATE_RELATION"
