"""Selected Shop policy, real rule execution, atomic admission and replay."""

import ast
from importlib import import_module
import json
from pathlib import Path
import subprocess
import sys

import pytest

import malleus.compiler as api
from malleus.logic import LogicExecutionError
from malleus.prolog_verifier import PrologVerifier


MODULE = (
    "research.ontology_driven_kg_realization.experiments.small_shop.shipment_policy.run"
)


def fixture(tmp_path):
    shop = import_module(MODULE)
    path = tmp_path / "history.jsonl"
    history = shop.start(path)
    for step in ("order", "shipment-1"):
        shop.admit(history, shop.prepare(history, step))
    return shop, path, history


def test_duplicate_refuses_atomically_then_distinct_unit_admits_and_replays(
    tmp_path, monkeypatch
):
    shop, path, history = fixture(tmp_path)
    plan = shop.prepare(history, "duplicate-unit")
    before = path.read_bytes()
    before_graph = history.replay().graph.export_records()
    with pytest.raises(shop.ShipmentPolicyRefusal) as refused:
        shop.admit(history, plan)
    error = refused.value
    # Core refuses at CHECK, before the first append. It was REJECTED_CHANGE
    # while the program ran the engine and handed Core the outcome.
    assert error.refusal.stage is api.PopulationAdmissionStage.CHECK
    assert error.refusal.reason == "CONTENT_RULE_VIOLATED"
    assert error.check.outcome == "VIOLATED"
    assert error.check.violations[0].violation_code == "UNIT_ASSIGNED_TWICE"
    assert error.check.violations[0].witness_record_ids == (
        "SYN-PS-X1",
        "ships_unit:SYN-S1:SYN-PS-X1",
        "ships_unit:SYN-S2:SYN-PS-X1",
    )
    assert path.read_bytes() == before
    assert history.replay().graph.export_records() == before_graph

    admitted = shop.admit(history, shop.prepare(history, "shipment-2"))
    assert admitted.check.outcome == "SATISFIED"
    assert len(admitted.replay.change_sets) == 3
    receipt = json.loads(
        admitted.replay.retained_bytes(
            f"receipt:{admitted.replay.change_sets[-1].change_set_id}"
            ":shop-one-shipment-per-unit"
        )
    )
    assert receipt["knowledge_change_set_identity"] == (
        admitted.replay.change_sets[-1].identity
    )
    assert receipt["population_plan_identity"] == admitted.plan_identity
    assert receipt["check"]["contract_hash"] == admitted.check.contract_hash
    assert receipt["check"]["ruleset_hash"] == admitted.check.ruleset_hash
    assert receipt["check"]["executor_kind"] == "PROLOG_RULES"
    checks = [
        r
        for r in admitted.replay.machine_state.records
        if r.record_type == "CheckRecord"
    ]
    assert len(checks) == 3
    assert all(r.fields["outcome"] == "SATISFIED" for r in checks)
    assert {r.fields["check_contract_identity"] for r in checks} == {
        admitted.check.contract_hash
    }

    def no_engine(*args, **kwargs):
        raise AssertionError("replay must fold retained history, not rerun the engine")

    monkeypatch.setattr(PrologVerifier, "verify_candidate_subgraph", no_engine)
    replay = api.KnowledgeChangeHistory.reopen(path).replay()
    assert replay.receipt.identity == admitted.replay.receipt.identity
    assert replay.graph.export_records() == admitted.replay.graph.export_records()
    edges = replay.graph.query_relations("ShipmentContainsUnit")
    assert {(r["source_id"], r["target_id"]) for r in edges} == {
        ("SYN-S1", "SYN-PS-X1"),
        ("SYN-S2", "SYN-PS-X2"),
    }
    assert path.read_bytes().startswith(before)
    trace = api.trace_population_record(replay, "SYN-S2")
    assert {item.record_id for item in trace.sources} == {
        "source:partial-shipments:shipments"
    }
    evidence = {item.record_id: item.content for item in trace.evidence}
    assert evidence["shop:rules"] == (shop.HERE / "rules.pl").read_bytes()
    assert evidence["shop:logic"] == (shop.HERE / "logic.yaml").read_bytes()


def test_stale_plan_refuses_before_engine_or_write(tmp_path, monkeypatch):
    """A stale preparation is gone; a stale pin in the plan still refuses first.

    The program used to retain the plan, then admit it, and the gap between
    the two could go stale. The one-call operation reads the base itself, so
    the only thing left that can be stale is what the plan pins. It refuses at
    COMPILE, before the engine and before any write.
    """
    shop, path, history = fixture(tmp_path)
    plan = shop.prepare(history, "shipment-2")
    plan["contract_identity"] = "sha256:" + "0" * 64
    before = path.read_bytes()

    def no_engine(*args, **kwargs):
        raise AssertionError("a stale plan reached the engine")

    monkeypatch.setattr(PrologVerifier, "verify_candidate_subgraph", no_engine)
    with pytest.raises(api.PopulationAdmissionRefusal) as refused:
        shop.admit(history, plan)
    assert refused.value.stage is api.PopulationAdmissionStage.COMPILE
    assert refused.value.ledger_unchanged is True
    assert path.read_bytes() == before


def test_failed_execution_is_not_a_satisfied_check(tmp_path, monkeypatch):
    shop, path, history = fixture(tmp_path)
    plan = shop.prepare(history, "shipment-2")
    before = path.read_bytes()

    def failed(*args, **kwargs):
        raise LogicExecutionError("test engine failure")

    monkeypatch.setattr(PrologVerifier, "verify_candidate_subgraph", failed)
    # The engine failure used to reach the caller raw; Core now names the
    # stage and the engine, and still writes nothing.
    with pytest.raises(api.PopulationAdmissionRefusal, match="test engine failure"):
        shop.admit(history, plan)
    assert path.read_bytes() == before


def test_the_program_hands_core_plan_bytes_and_nothing_else():
    """There is no object between the program and the engine left to alter.

    The predecessor of this test altered a prepared compilation's operations
    and required the check to read the real change anyway. The program no
    longer holds a compilation: it passes the plan bytes, and every other
    argument of the one call is a coordinate.
    """
    module = import_module(MODULE)
    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "check_and_admit_population_plan"
    ]
    assert len(calls) == 1
    assert not calls[0].args
    assert {keyword.arg for keyword in calls[0].keywords} == {
        "history",
        "plan_bytes",
        "history_profile",
        "transaction_time",
        "actor_id",
    }


def test_cli_and_second_run_produce_exact_history_and_report(tmp_path):
    shop = import_module(MODULE)
    first, second = tmp_path / "first.jsonl", tmp_path / "second.jsonl"
    command = [sys.executable, "-m", MODULE, "--history", str(first)]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    report = json.loads(completed.stdout)
    assert shop.canonical(shop.run(second)) == shop.canonical(report)
    assert first.read_bytes() == second.read_bytes()
    assert report["accepted_changes"] == 3
    assert report["duplicate_unit"]["ledger_unchanged"] is True
    before = first.read_bytes()
    with pytest.raises(ValueError, match="fresh history path"):
        shop.run(first)
    assert first.read_bytes() == before
