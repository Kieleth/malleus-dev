"""Focused checks for the paper-local ledger admission and replay seam."""

from __future__ import annotations

import ast
from hashlib import sha256
import inspect
import json
from pathlib import Path

import pytest

from malleus._contract_pipeline.admission import (
    PopulationAdmissionRefusal,
    check_and_admit_change_set,
)
from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeHistory,
    KnowledgeChangeRefusalReason,
    KnowledgeValidTime,
)
from malleus.kg import OpType
from malleus.ledger import canonical_json
from malleus.staging import ProposedOperation
from research.ontology_driven_kg_realization.experiments.document_paper import (
    document_run as document_run_module,
)
from research.ontology_driven_kg_realization.experiments.document_paper.document_run import (
    RetainedDocumentEvidence,
    RetainedDocumentSource,
    run_document_history,
)
from research.ontology_driven_kg_realization.experiments.document_paper.graph_recipe_change_set import (
    GraphRecipeChangeSetError,
    assembly_plan_to_operations,
    canonical_assembly_plan_bytes,
)
from research.ontology_driven_kg_realization.experiments.document_paper.test_graph_recipe_change_set import (
    _ge020_plan,
    _plan_with_operations,
    history_contract as _history_contract,
)
from tests.contract_compiler.pareto.test_protocol_machine import (
    CHECK_CONTRACT_IDS,
    CHECK_DOCUMENTS,
)


TRANSACTION_TIME = "2026-09-02T00:00:00Z"
ACTOR_ID = "actor:paper-v4-evaluator"
PLAN_EVIDENCE_ID = "evidence:paper-v4:assembly-plan"


@pytest.fixture(scope="module")
def contract_fixture():
    return _history_contract.__wrapped__()


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _run(path: Path, contract, *, plan=None):
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
            # Core resolves and runs every check the fixture policy requires,
            # so both contract documents have to be retained before admission.
            *(
                RetainedDocumentEvidence(check_id, document, "application/json")
                for check_id, document in zip(
                    CHECK_CONTRACT_IDS, CHECK_DOCUMENTS, strict=True
                )
            ),
        ),
        plan_evidence_id=PLAN_EVIDENCE_ID,
        change_set_id="change:paper-v4:population",
        valid_time=KnowledgeValidTime("ORDER_ONLY", "population-1"),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR_ID,
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
        *(
            (check_id, _digest(document))
            for check_id, document in zip(
                CHECK_CONTRACT_IDS, CHECK_DOCUMENTS, strict=True
            )
        ),
    )
    assert replayed.retained_bytes(PLAN_EVIDENCE_ID) == (
        canonical_assembly_plan_bytes(_ge020_plan())
    )
    # Core names the proposal and the decision after the change set; the
    # runner no longer chooses either identity.
    assert (
        replayed.machine_state.get_record(
            "DecisionRecord", "decision:change:paper-v4:population"
        )["verdict"]
        == "ACCEPT"
    )
    assert (
        replayed.machine_state.get_record(
            "ProposalRecord", "proposal:change:paper-v4:population"
        )
        is not None
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
    # Core mints one retained receipt per check and appends it in the same
    # batch as the change, ahead of the three protocol events it writes.
    assert event_types[-7:] == (
        "KNOWLEDGE_CHANGE_SET_RETAINED",
        "ARTIFACT_REGISTERED",
        "ARTIFACT_REGISTERED",
        "CHANGE_PROPOSED",
        "CHECK_RECORDED",
        "CHECK_RECORDED",
        "VERDICT_RECORDED",
    )
    assert len(event_types) == 15
    assert tuple(first_path.parent.iterdir()) == (first_path,)


def test_the_runner_has_no_seam_that_could_supply_a_protocol_event() -> None:
    """The protocol-event factory is gone, not merely unused.

    ``run_document_history`` used to take a ``protocol_events`` callable and
    validate the lifecycle it returned. Both were the caller writing Core's
    check and verdict records, which is what
    ``KnowledgeChangeRefusalReason.CALLER_SUPPLIED_CHECK_EVENT`` refuses.
    Core writes the lifecycle, so the parameter, the factory type and the
    lifecycle validator were deleted rather than left unreferenced.
    """

    assert "protocol_events" not in inspect.signature(run_document_history).parameters

    tree = ast.parse(Path(document_run_module.__file__).read_text())
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert "ProtocolEventFactory" not in names
    assert "_require_lifecycle" not in names

    # Docstrings are excluded: this module explains the three events Core
    # writes, and naming them in prose is not building one.
    docstrings = {
        ast.get_docstring(node, clean=False)
        for node in ast.walk(tree)
        if isinstance(
            node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        )
    }
    literals = {
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and node.value not in docstrings
    }
    for event_type in ("CHECK_RECORDED", "VERDICT_RECORDED", "CHANGE_PROPOSED"):
        assert event_type not in literals

    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert "check_and_admit_change_set" in calls
    assert "admit" not in calls


def test_a_change_set_that_binds_a_stale_base_admits_nothing(
    tmp_path: Path,
    contract_fixture,
) -> None:
    """Core refuses the composed change set when the ledger moved under it.

    The runner used to reach this through its ``protocol_events`` hook, which
    let a test append an anchor between composition and admission. The hook
    was the caller's way into the lifecycle and it is gone, so the same claim
    is made where the seam now is: compose against one head, move the ledger,
    then hand the change set to Core.
    """

    compiled, partial, binding = contract_fixture
    ledger = tmp_path / "semantic.jsonl"
    plan = _ge020_plan()
    plan_bytes = canonical_assembly_plan_bytes(plan)
    source_bytes = b'{"blocks":[{"block_id":"p1-b1","text":"source"}]}'

    history = KnowledgeChangeHistory(
        ledger,
        partial_contract=partial,
        contract_view=compiled.view,
        binding=binding,
    )
    anchors = (
        (
            "artifact:paper-v4:validated-contract",
            compiled.view.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        (
            "artifact:paper-v4:partial-contract",
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            "artifact:paper-v4:history-binding",
            binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        ("artifact:paper-v4:selected-reading", source_bytes, "SOURCE_ARTIFACT"),
        (PLAN_EVIDENCE_ID, plan_bytes, "RETAINED_EVIDENCE"),
        *(
            (check_id, document, "RETAINED_EVIDENCE")
            for check_id, document in zip(
                CHECK_CONTRACT_IDS, CHECK_DOCUMENTS, strict=True
            )
        ),
    )
    for artifact_id, content, role in anchors:
        history.append_anchor(
            machine_event=canonical_json(
                {
                    "event_type": "ARTIFACT_REGISTERED",
                    "payload": {
                        "artifact_id": artifact_id,
                        "artifact_identity": _digest(content),
                    },
                }
            ).encode("utf-8"),
            retained_bytes=content,
            media_type="application/json",
            role=role,
            transaction_time=TRANSACTION_TIME,
            actor_id=ACTOR_ID,
        )
    history.append_anchor(
        machine_event=canonical_json(
            {
                "event_type": "SOURCE_REGISTERED",
                "payload": {
                    "artifact_id": "artifact:paper-v4:selected-reading",
                    "source_id": "source:paper-v4:selected-reading",
                    "source_identity": _digest(source_bytes),
                },
            }
        ).encode("utf-8"),
        retained_bytes=source_bytes,
        media_type="application/json",
        role="RETAINED_SOURCE",
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR_ID,
    )

    change_set = history.compose_change_set(
        change_set_id="change:paper-v4:population",
        source_record_ids=("source:paper-v4:selected-reading",),
        evidence_record_ids=(PLAN_EVIDENCE_ID,),
        operations=assembly_plan_to_operations(plan),
        valid_time=KnowledgeValidTime("ORDER_ONLY", "population-1"),
        supersedes=(),
    )

    intervening = b'{"receipt":"intervening"}'
    history.append_anchor(
        machine_event=canonical_json(
            {
                "event_type": "ARTIFACT_REGISTERED",
                "payload": {
                    "artifact_id": "evidence:paper-v4:intervening",
                    "artifact_identity": _digest(intervening),
                },
            }
        ).encode("utf-8"),
        retained_bytes=intervening,
        media_type="application/json",
        role="RETAINED_EVIDENCE",
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR_ID,
    )
    boundary = ledger.read_bytes()

    with pytest.raises(PopulationAdmissionRefusal) as refusal:
        check_and_admit_change_set(
            history=history,
            change_set=change_set,
            transaction_time=TRANSACTION_TIME,
            actor_id=ACTOR_ID,
        )

    assert refusal.value.reason == KnowledgeChangeRefusalReason.STALE_BASE.name
    assert ledger.read_bytes() == boundary
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
