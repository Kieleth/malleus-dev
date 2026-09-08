"""Selected Shop policy, real rule execution, atomic admission and replay."""

from dataclasses import replace
from hashlib import sha256
from importlib import import_module
import json
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
    prepared = shop.prepare(history, "duplicate-unit")
    before = path.read_bytes()
    before_graph = history.replay().graph.export_records()
    with pytest.raises(shop.ShipmentPolicyRefusal) as refused:
        shop.admit(history, prepared)
    error = refused.value
    assert error.refusal.reason is api.KnowledgeChangeRefusalReason.REJECTED_CHANGE
    assert error.check.outcome == "VIOLATED"
    assert error.check.violations[0].violation_code == "UNIT_ASSIGNED_TWICE"
    assert error.check.violations[0].witness_record_ids == (
        "SYN-PS-X1",
        "ships_unit:SYN-S1:SYN-PS-X1",
        "ships_unit:SYN-S2:SYN-PS-X1",
    )
    assert path.read_bytes() == before
    assert history.replay().graph.export_records() == before_graph

    prepared = shop.prepare(history, "shipment-2")
    admitted = shop.admit(history, prepared)
    assert admitted.check.outcome == "SATISFIED"
    assert len(admitted.replay.change_sets) == 3
    receipt = json.loads(admitted.replay.retained_bytes(admitted.receipt_identity))
    assert receipt["knowledge_change_set_identity"] == prepared.change_set.identity
    assert receipt["population_plan_identity"] == (
        "sha256:" + sha256(prepared.compilation.canonical_plan_bytes).hexdigest()
    )
    assert receipt["check"]["contract_hash"] == admitted.check.contract_hash
    assert receipt["check"]["ruleset_hash"] == admitted.check.ruleset_hash
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


def test_stale_preparation_refuses_before_engine_or_write(tmp_path, monkeypatch):
    shop, path, history = fixture(tmp_path)
    prepared = shop.prepare(history, "shipment-2")
    history.append_anchors(
        anchors=(
            api.structural_evidence_anchor(
                record_id="later-evidence", content=b"later", media_type="text/plain"
            ),
        ),
        transaction_time=shop.TIME,
        actor_id=shop.ACTOR,
    )
    before = path.read_bytes()

    def no_engine(*args, **kwargs):
        raise AssertionError("stale preparation reached the engine")

    monkeypatch.setattr(PrologVerifier, "verify_candidate_subgraph", no_engine)
    with pytest.raises(api.KnowledgeChangeRefusal) as refused:
        shop.admit(history, prepared)
    assert refused.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert path.read_bytes() == before


def test_failed_execution_is_not_a_satisfied_check(tmp_path, monkeypatch):
    shop, path, history = fixture(tmp_path)
    prepared = shop.prepare(history, "shipment-2")
    before = path.read_bytes()

    def failed(*args, **kwargs):
        raise LogicExecutionError("test engine failure")

    monkeypatch.setattr(PrologVerifier, "verify_candidate_subgraph", failed)
    with pytest.raises(LogicExecutionError, match="test engine failure"):
        shop.admit(history, prepared)
    assert path.read_bytes() == before


def test_check_uses_actual_change_not_mutable_preparation_metadata(tmp_path):
    shop, path, history = fixture(tmp_path)
    prepared = shop.prepare(history, "duplicate-unit")
    altered = replace(
        prepared, compilation=replace(prepared.compilation, operations=())
    )
    before = path.read_bytes()
    with pytest.raises(shop.ShipmentPolicyRefusal) as refused:
        shop.admit(history, altered)
    assert refused.value.check.outcome == "VIOLATED"
    assert path.read_bytes() == before


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
