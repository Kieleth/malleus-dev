"""Core checks and admits a change set the caller composed.

Paper ledger E-0504, decision D, step 2. Two ways into the ledger existed: a
producer's plan bytes through ``check_and_admit_population_plan``, and a
composed ``KnowledgeChangeSet`` through ``admit``/``admit_with_anchors`` with
the caller writing the protocol events, which is the hole ROADMAP F1 measured.
A composed change set is the lower primitive and the shape every research
consumer works in, so closing the public door needed a third Core-authored
entry point rather than a rewrite of those consumers into plan authors.

``check_and_admit_change_set`` is that entry point. It shares the check stage
and the admission stage with the plan operation; only where the operations
come from differs.
"""

from __future__ import annotations

import ast
import inspect
import json
from pathlib import Path

import pytest

import malleus.compiler as compiler
from malleus._contract_pipeline import admission as admission_module

from tests.contract_compiler.pareto.test_atomic_population_admission import (
    ACTOR,
    SOURCE_ID,
    _artifact,
    _record,
    _shop_shaped,
    history_path,
    swipl,
)
from tests.contract_compiler.pareto.test_check_contract_executor import (
    BUILTIN_CONTRACT,
    BUILTIN_IDENTITY,
    STRUCTURAL_CHECK_ID,
    _two_check_history,
)
from tests.contract_compiler.pareto.test_public_compiler import (
    TRANSACTION_TIME,
    _canonical,
    _digest,
)


def _operations(*records: dict) -> tuple[compiler.KnowledgeOperation, ...]:
    return tuple(
        compiler.KnowledgeOperation(
            ordinal=ordinal,
            operation_id=f"operation:composed:{ordinal}",
            operation_type="CREATE_ENTITY",
            record_type="SupplierOrderState",
            record_id=record["id"],
            properties=record["properties"],
            depends_on=(),
            source_id=None,
            target_id=None,
        )
        for ordinal, record in enumerate(records)
    )


def _composed(history, *records: dict, change_set_id: str = "change:composed"):
    """One change set composed by the caller, the way a research program does."""

    return history.compose_change_set(
        change_set_id=change_set_id,
        source_record_ids=(SOURCE_ID,),
        evidence_record_ids=("artifact:logic",),
        operations=_operations(*records),
        valid_time=compiler.KnowledgeValidTime("ORDER_ONLY", records[0]["id"]),
        supersedes=(),
    )


def _admit(history, change_set, **extra):
    return compiler.check_and_admit_change_set(
        history=history,
        change_set=change_set,
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR,
        **extra,
    )


# --- the third entry point admits what a caller composed --------------------


@swipl
def test_a_composed_change_set_admits_under_a_builtin_and_a_rule_layer(
    tmp_path: Path,
) -> None:
    """Both executors run, both receipts are retained, and Core writes both records."""

    history, _, logic = _two_check_history(tmp_path)
    change = _composed(history, _record("e1", 2))

    admitted = _admit(history, change)

    assert [check.check_contract_id for check in admitted.checks] == [
        STRUCTURAL_CHECK_ID,
        logic.contract_id,
    ]
    assert [check.executor_kind.value for check in admitted.checks] == [
        "CORE_BUILTIN",
        "PROLOG_RULES",
    ]
    assert all(check.outcome == "SATISFIED" for check in admitted.checks)
    assert admitted.replay.change_sets == (change,)
    retained = {member.record_id for member in admitted.replay.retained_inputs}
    assert {check.receipt_id for check in admitted.checks} <= retained
    records = [
        record
        for record in admitted.replay.machine_state.records
        if record.record_type == "CheckRecord"
    ]
    assert {record.fields["outcome"] for record in records} == {"SATISFIED"}
    assert {record.fields["check_contract_identity"] for record in records} == {
        BUILTIN_IDENTITY,
        logic.contract_hash,
    }


@swipl
def test_a_composed_change_set_admits_under_a_rule_layer_alone(
    tmp_path: Path,
) -> None:
    """The Prolog-only policy, which is the shape a shipped adopter runs."""

    history, _, logic, _ = _shop_shaped(tmp_path)
    change = _composed(history, _record("e1", 2))

    admitted = _admit(history, change)

    assert [check.check_contract_id for check in admitted.checks] == [
        logic.contract_id
    ]
    assert admitted.checks[0].executor_kind is compiler.CheckExecutorKind.PROLOG_RULES
    assert admitted.replay.change_sets == (change,)
    assert admitted.change_set is change


def test_a_composed_change_set_admits_under_the_structural_builtin_alone(
    tmp_path: Path,
) -> None:
    """Core's own structural check, which needs no Prolog and no rule bytes."""

    history, _, _ = _two_check_history(tmp_path, builtin_only=True)
    change = _composed(history, _record("e1", 2))

    admitted = _admit(history, change)

    assert len(admitted.checks) == 1
    assert admitted.checks[0].executor_kind is compiler.CheckExecutorKind.CORE_BUILTIN
    assert admitted.checks[0].result["result_state_digest"].startswith("sha256:")
    assert admitted.replay.change_sets == (change,)


# --- and refuses without writing a byte --------------------------------------


@swipl
def test_a_violated_rule_refuses_the_composed_change_and_writes_nothing(
    tmp_path: Path,
) -> None:
    """The same conflicting pair a caller-written SATISFIED used to admit."""

    history, _, _, _ = _shop_shaped(tmp_path)
    change = _composed(history, _record("e1", 2), _record("e2", 5))
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(history, change)

    error = refusal.value
    assert error.stage is compiler.PopulationAdmissionStage.CHECK
    assert error.reason == "CONTENT_RULE_VIOLATED"
    assert error.violated_rule_ids == ("NO_CONFLICTING_QUANTITY",)
    assert error.witness_record_ids == (
        "supplier-order-state:B:e1",
        "supplier-order-state:B:e2",
    )
    assert error.ledger_unchanged is True
    assert history_path(history).read_bytes() == ledger_before
    assert history.replay().change_sets == ()


def test_a_change_the_builtin_cannot_apply_refuses_at_the_check_stage(
    tmp_path: Path,
) -> None:
    """The builtin reports the refusal that stopped the application, by name."""

    history, _, _ = _two_check_history(tmp_path, builtin_only=True)
    change = history.compose_change_set(
        change_set_id="change:composed-unknown-supersession",
        source_record_ids=(SOURCE_ID,),
        evidence_record_ids=("artifact:logic",),
        operations=(
            compiler.KnowledgeOperation(
                ordinal=0,
                operation_id="operation:composed:0",
                operation_type="CREATE_ENTITY",
                record_type="SupplierOrderState",
                record_id="supplier-order-state:B:e1",
                properties=_record("e1", 2)["properties"],
                depends_on=(),
                source_id=None,
                target_id=None,
                supersedes_record_id="supplier-order-state:B:absent",
            ),
        ),
        valid_time=compiler.KnowledgeValidTime("ORDER_ONLY", "e1"),
        supersedes=(),
    )
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(history, change)

    error = refusal.value
    assert error.stage is compiler.PopulationAdmissionStage.CHECK
    assert error.reason == "CONTENT_RULE_VIOLATED"
    assert error.violated_rule_ids == (
        "OPERATIONS_APPLY_ATOMICALLY_TO_ACCEPTED_STATE",
    )
    assert "UNKNOWN_SUPERSESSION" in error.detail
    assert error.ledger_unchanged is True
    assert history_path(history).read_bytes() == ledger_before


def test_a_required_check_the_history_does_not_retain_refuses(tmp_path: Path) -> None:
    history, _, _ = _two_check_history(
        tmp_path, builtin_only=True, retain_check_contract=False
    )
    change = _composed(history, _record("e1", 2))
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(history, change)

    assert refusal.value.stage is compiler.PopulationAdmissionStage.CHECK
    assert refusal.value.reason == "CHECK_CONTRACT_NOT_RETAINED"
    assert refusal.value.ledger_unchanged is True
    assert history_path(history).read_bytes() == ledger_before


def test_a_required_check_core_cannot_run_refuses(tmp_path: Path) -> None:
    """A retained v1 document naming a builtin the registry does not hold."""

    unrunnable = _canonical(
        {
            "check_contract_id": STRUCTURAL_CHECK_ID,
            "executor": {
                "builtin_id": "malleus.core.invented-check",
                "builtin_version": "1",
                "kind": "CORE_BUILTIN",
            },
            "grammar": compiler.CHECK_CONTRACT_GRAMMAR,
            "outcomes": ["SATISFIED", "VIOLATED"],
        }
    )
    history, _, _ = _two_check_history(
        tmp_path, builtin_only=True, check_contract_bytes=unrunnable
    )
    change = _composed(history, _record("e1", 2))
    ledger_before = history_path(history).read_bytes()

    with pytest.raises(compiler.PopulationAdmissionRefusal) as refusal:
        _admit(history, change)

    assert refusal.value.stage is compiler.PopulationAdmissionStage.CHECK
    assert refusal.value.reason == "UNRUNNABLE_REQUIRED_CHECK"
    assert refusal.value.ledger_unchanged is True
    assert history_path(history).read_bytes() == ledger_before


def test_the_check_record_carries_exactly_the_fields_the_machine_declares(
    tmp_path: Path,
) -> None:
    """``correction/machine.json`` declares a seventh field; Core states it."""

    from tests.contract_compiler.pareto.test_check_contract_executor import (
        _machine_bytes,
    )

    history, _, _ = _two_check_history(
        tmp_path, builtin_only=True, machine=_machine_bytes(receipt_identity=True)
    )
    change = _composed(history, _record("e1", 2))

    admitted = _admit(history, change)

    record = next(
        record
        for record in admitted.replay.machine_state.records
        if record.record_type == "CheckRecord"
    )
    assert record.fields["receipt_identity"] == admitted.checks[0].receipt_identity
    assert set(record.fields) == {
        "check_contract_id",
        "check_contract_identity",
        "outcome",
        "policy_identity",
        "proposal_id",
        "receipt_id",
        "receipt_identity",
    }


def test_a_caller_anchor_is_retained_in_the_same_batch(tmp_path: Path) -> None:
    """Retained inputs a composed change needs travel with it, not before it."""

    history, _, _ = _two_check_history(tmp_path, builtin_only=True)
    note = b'{"note":"one retained companion"}\n'
    anchor = _artifact("artifact:companion", note, "RETAINED_EVIDENCE")
    change = _composed(history, _record("e1", 2))

    admitted = _admit(history, change, anchors=(anchor,))

    assert admitted.replay.retained_bytes("artifact:companion") == note
    assert admitted.replay.change_sets == (change,)


# --- one implementation, two entry points ------------------------------------


def test_both_entry_points_run_the_same_check_and_admission_code() -> None:
    """The shared halves are called by name from both, not copied into each."""

    module = ast.parse(inspect.getsource(admission_module))
    called = {
        node.name: {
            inner.func.id
            for inner in ast.walk(node)
            if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name)
        }
        for node in ast.walk(module)
        if isinstance(node, ast.FunctionDef)
    }
    for entry_point in (
        "check_and_admit_population_plan",
        "check_and_admit_change_set",
    ):
        assert "_check_stage" in called[entry_point]
        assert "_admit_checked" in called[entry_point]
    assert "_run_check" in called["_check_stage"]
    assert "_declared_event" in called["_admit_checked"]


def test_the_entry_point_is_declared_on_the_public_facade() -> None:
    assert "check_and_admit_change_set" in compiler.__all__
    assert "ChangeSetAdmission" in compiler.__all__
    assert compiler.check_and_admit_change_set is (
        admission_module.check_and_admit_change_set
    )


def test_no_parameter_of_either_entry_point_takes_an_outcome() -> None:
    """The guarantee, mechanically: an outcome cannot be passed in."""

    for entry_point in (
        compiler.check_and_admit_change_set,
        compiler.check_and_admit_population_plan,
    ):
        names = set(inspect.signature(entry_point).parameters)
        assert not {name for name in names if "outcome" in name or "verdict" in name}
        assert "machine_events" not in names


def test_the_admitted_change_set_reopens_and_replays_to_the_same_state(
    tmp_path: Path,
) -> None:
    history, _, _ = _two_check_history(tmp_path, builtin_only=True)
    change = _composed(history, _record("e1", 2))

    admitted = _admit(history, change)
    reopened = compiler.KnowledgeChangeHistory.reopen(history.path).replay()

    assert reopened.graph.export_records() == admitted.replay.graph.export_records()
    assert reopened.receipt == admitted.replay.receipt
    assert reopened.change_sets == admitted.replay.change_sets


def test_the_receipt_states_the_executor_and_names_no_plan(tmp_path: Path) -> None:
    """A composed change has no plan, so its receipt binds none."""

    history, _, _ = _two_check_history(tmp_path, builtin_only=True)
    change = _composed(history, _record("e1", 2))

    admitted = _admit(history, change)
    receipt = json.loads(
        admitted.replay.retained_bytes(admitted.checks[0].receipt_id)
    )

    assert set(receipt) == {"check", "knowledge_change_set_identity"}
    assert receipt["knowledge_change_set_identity"] == change.identity
    assert receipt["check"]["executor_kind"] == "CORE_BUILTIN"
    assert receipt["check"]["outcome"] == "SATISFIED"
    assert receipt["check"]["check_contract_identity"] == BUILTIN_IDENTITY
    assert _digest(admitted.replay.retained_bytes(admitted.checks[0].receipt_id)) == (
        admitted.checks[0].receipt_identity
    )


def test_the_entry_point_refuses_inputs_that_are_not_what_it_declares(
    tmp_path: Path,
) -> None:
    history, _, _ = _two_check_history(tmp_path, builtin_only=True)
    change = _composed(history, _record("e1", 2))

    with pytest.raises(TypeError, match="KnowledgeChangeHistory"):
        compiler.check_and_admit_change_set(
            history=object(),
            change_set=change,
            transaction_time=TRANSACTION_TIME,
            actor_id=ACTOR,
        )
    with pytest.raises(TypeError, match="KnowledgeChangeSet"):
        _admit(history, object())
    with pytest.raises(TypeError, match="KnowledgeAnchorInput"):
        _admit(history, change, anchors=(object(),))
    assert history.replay().change_sets == ()


def test_the_builtin_contract_bytes_are_the_ones_this_module_pins() -> None:
    """Guard: the fixture contract and its identity move together or not at all."""

    assert _digest(BUILTIN_CONTRACT) == BUILTIN_IDENTITY
    assert compiler.parse_check_contract(BUILTIN_CONTRACT).builtin_id == (
        compiler.OPERATIONS_APPLY_ATOMICALLY
    )
