"""Focused checks for the paper-local ledger admission and replay seam."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import pytest

from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeHistory,
    KnowledgeChangeRefusal,
    KnowledgeChangeRefusalReason,
    KnowledgeValidTime,
)
from malleus.kg import OpType
from malleus.ledger import canonical_json
from malleus.staging import ProposedOperation
from research.ontology_driven_kg_realization.experiments.document_paper.document_run import (
    DocumentRunError,
    RetainedDocumentEvidence,
    RetainedDocumentSource,
    run_document_history,
)
from research.ontology_driven_kg_realization.experiments.document_paper.graph_recipe_change_set import (
    GraphRecipeChangeSetError,
    canonical_assembly_plan_bytes,
)
from research.ontology_driven_kg_realization.experiments.document_paper.test_graph_recipe_change_set import (
    _ge020_plan,
    _plan_with_operations,
    _protocol_events,
    history_contract as _history_contract,
)


TRANSACTION_TIME = "2026-09-02T00:00:00Z"
ACTOR_ID = "actor:paper-v4-evaluator"
PLAN_EVIDENCE_ID = "evidence:paper-v4:assembly-plan"


@pytest.fixture(scope="module")
def contract_fixture():
    return _history_contract.__wrapped__()


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _run(path: Path, contract, *, plan=None, protocol_events=_protocol_events):
    compiled, partial, binding = contract
    selected_plan = _ge020_plan() if plan is None else plan
    plan_bytes = canonical_assembly_plan_bytes(selected_plan)
    return run_document_history(
        path,
        plan=selected_plan,
        partial_contract=partial,
        contract_view=compiled.view,
        binding=binding,
        source=RetainedDocumentSource(
            artifact_id="artifact:paper-v4:selected-reading",
            source_id="source:paper-v4:selected-reading",
            content=b'{"blocks":[{"block_id":"p1-b1","text":"source"}]}',
            media_type="application/json",
        ),
        evidence=(
            RetainedDocumentEvidence(
                PLAN_EVIDENCE_ID,
                plan_bytes,
                "application/json",
            ),
        ),
        plan_evidence_id=PLAN_EVIDENCE_ID,
        change_set_id="change:paper-v4:population",
        valid_time=KnowledgeValidTime("ORDER_ONLY", "population-1"),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR_ID,
        protocol_events=protocol_events,
    )


def test_genesis_run_is_exact_after_disposal_and_reopen(
    tmp_path: Path,
    contract_fixture,
) -> None:
    first_path = tmp_path / "first/semantic.jsonl"
    second_path = tmp_path / "second/semantic.jsonl"

    first = _run(first_path, contract_fixture)
    second = _run(second_path, contract_fixture)

    assert first.ledger_bytes == first_path.read_bytes()
    assert first.ledger_bytes == second.ledger_bytes
    assert first.replay.graph.snapshot() == second.replay.graph.snapshot()
    assert first.replay.graph.state_digest() == second.replay.graph.state_digest()
    assert first.replay.receipt.canonical_bytes == second.replay.receipt.canonical_bytes
    assert first.replay.receipt.identity == _digest(
        first.replay.receipt.canonical_bytes
    )
    receipt = json.loads(first.replay.receipt.canonical_bytes)
    assert first.replay.receipt.canonical_bytes == canonical_json(receipt).encode(
        "utf-8"
    )

    replayed = KnowledgeChangeHistory.reopen(first_path).replay()
    assert replayed.graph.snapshot() == first.replay.graph.snapshot()
    assert replayed.machine_state.canonical_bytes == (
        first.replay.machine_state.canonical_bytes
    )
    assert replayed.receipt.canonical_bytes == first.replay.receipt.canonical_bytes
    assert replayed.change_sets == first.replay.change_sets
    assert replayed.change_sets[0].sources == (
        (
            "source:paper-v4:selected-reading",
            _digest(b'{"blocks":[{"block_id":"p1-b1","text":"source"}]}'),
        ),
    )
    assert replayed.change_sets[0].evidence == (
        (PLAN_EVIDENCE_ID, _ge020_plan().plan_digest),
    )
    assert replayed.retained_bytes(PLAN_EVIDENCE_ID) == (
        canonical_assembly_plan_bytes(_ge020_plan())
    )
    assert (
        replayed.machine_state.get_record("DecisionRecord", "decision-paper-1")[
            "verdict"
        ]
        == "ACCEPT"
    )
    assert replayed.graph.query("Person", name="Alice") == [
        {"id": "person:alice", "name": "Alice", "type": "Person"}
    ]
    assert replayed.graph.query_relations(
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
    event_types = tuple(
        json.loads(line)["event_type"] for line in first.ledger_bytes.splitlines()
    )
    assert event_types[-5:] == (
        "KNOWLEDGE_CHANGE_SET_RETAINED",
        "CHANGE_PROPOSED",
        "CHECK_RECORDED",
        "CHECK_RECORDED",
        "VERDICT_RECORDED",
    )
    assert len(event_types) == 11
    assert tuple(first_path.parent.iterdir()) == (first_path,)


def test_intervening_anchor_makes_change_stale_without_partial_admission(
    tmp_path: Path,
    contract_fixture,
) -> None:
    ledger = tmp_path / "semantic.jsonl"
    boundary: list[bytes] = []

    def insert_intervening_event(change_set, machine_state_identity):
        content = b'{"outcome":"SATISFIED","receipt":"intervening"}'
        history = KnowledgeChangeHistory.reopen(ledger)
        history.append_anchor(
            machine_event=canonical_json(
                {
                    "event_type": "ARTIFACT_REGISTERED",
                    "payload": {
                        "artifact_id": "evidence:paper-v4:intervening",
                        "artifact_identity": _digest(content),
                    },
                }
            ).encode("utf-8"),
            retained_bytes=content,
            media_type="application/json",
            role="RETAINED_EVIDENCE",
            transaction_time=TRANSACTION_TIME,
            actor_id=ACTOR_ID,
        )
        boundary.append(ledger.read_bytes())
        return _protocol_events(change_set, machine_state_identity)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        _run(
            ledger,
            contract_fixture,
            protocol_events=insert_intervening_event,
        )

    assert refusal.value.reason is KnowledgeChangeRefusalReason.STALE_BASE
    assert ledger.read_bytes() == boundary[0]
    replayed = KnowledgeChangeHistory.reopen(ledger).replay()
    assert replayed.change_sets == ()
    assert replayed.graph.node_count == 0
    assert replayed.graph.edge_count == 0
    assert b"KNOWLEDGE_CHANGE_SET_RETAINED" not in ledger.read_bytes()


def test_lifecycle_refusal_retains_anchors_but_admits_no_change(
    tmp_path: Path,
    contract_fixture,
) -> None:
    ledger = tmp_path / "semantic.jsonl"

    def incomplete_lifecycle(change_set, machine_state_identity):
        return _protocol_events(change_set, machine_state_identity)[:-1]

    with pytest.raises(DocumentRunError, match="proposal, two checks, and one verdict"):
        _run(ledger, contract_fixture, protocol_events=incomplete_lifecycle)

    replayed = KnowledgeChangeHistory.reopen(ledger).replay()
    assert replayed.change_sets == ()
    assert replayed.graph.node_count == 0
    assert replayed.graph.edge_count == 0
    assert b"KNOWLEDGE_CHANGE_SET_RETAINED" not in ledger.read_bytes()


def test_non_entity_relation_plan_refuses_before_ledger_creation(
    tmp_path: Path,
    contract_fixture,
) -> None:
    plan = _ge020_plan()
    operation = plan.operations[0]
    unsupported = _plan_with_operations(
        plan,
        (
            ProposedOperation(
                OpType.CREATE_SIGNAL,
                operation.record_type,
                operation.record_id,
                operation.properties,
            ),
            *plan.operations[1:],
        ),
    )
    ledger = tmp_path / "semantic.jsonl"

    with pytest.raises(GraphRecipeChangeSetError, match="unsupported"):
        _run(ledger, contract_fixture, plan=unsupported)

    assert not ledger.exists()
