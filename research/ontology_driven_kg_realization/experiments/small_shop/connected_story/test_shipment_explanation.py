"""Read-side shipment explanation over the real connected history."""

from copy import deepcopy
import importlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
from malleus import KnowledgeGraph
import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    run,
)


MODULE = run.__package__ + ".shipment_explanation"


@pytest.fixture(scope="module")
def subject():
    return importlib.import_module(MODULE)


@pytest.fixture(scope="module")
def executed(tmp_path_factory):
    path = tmp_path_factory.mktemp("shop-explanation") / "history.jsonl"
    return path, run.run_story(path)


def test_before_and_after_explains_clearance_not_unpaid_balances(subject, executed):
    path, replay = executed
    before_bytes, before_graph = path.read_bytes(), replay.graph.snapshot()
    before = subject.explain_shipments(replay, at_occurrence="e28")
    after = subject.explain_shipments(replay, at_occurrence="e30")
    final = subject.explain_shipments(replay)
    assert {x["invoice"]: x["clearing_events"] for x in before["invoices"]} == {
        "I1": [],
        "I2": [],
    }
    assert {x["invoice"]: x["clearing_events"] for x in after["invoices"]} == {
        "I1": ["e30"],
        "I2": ["e30"],
    }
    for result in (before, after, final):
        assert result["invoice_limit"]["outcome"] == "CANNOT_DETERMINE"
        assert result["invoice_limit"]["unpaid_lower_bound"] == 0
        assert result["invoice_limit"]["unpaid_upper_bound"] is None
        assert result["invoice_limit"]["unknown_status_invoices"] == ["I1", "I2"]
        assert result["account_completeness"] == "NOT_ESTABLISHED"
        assert result["customer_identifier"] is None
        assert result["authorization"] == "NOT_ASSESSED"
    assert before["orders"]["O2"]["shipping_events"] == []
    assert final["orders"]["O2"]["shipping_events"] == ["e34"]
    assert final["orders"]["O2"]["packing_events"] == ["e33"]
    assert final["orders"]["O2"]["packed_units"] == ["X3", "Y2"]
    assert final["orders"]["O1"]["shipping_events"] == ["e28"]
    assert final["orders"]["O2"]["invoices"] == ["I2"]
    assert final["payments"] == {
        "P1": {"receipt_events": ["e29"], "cleared_invoices": ["I1", "I2"]}
    }
    assert after["checkpoint"]["kind"] == "ACCEPTED_IMPORT_POSITION_NOT_DOMAIN_TIME"
    assert before["checkpoint"]["graph_sha256"] != after["checkpoint"]["graph_sha256"]
    assert path.read_bytes() == before_bytes
    assert replay.graph.snapshot() == before_graph


def test_retained_context_and_graph_witnesses_are_inspectable(subject, executed):
    _, replay = executed
    result = subject.explain_shipments(replay)
    text = result["source_account"]["reported_delay"]
    assert text["passage_id"] == "intro-7-payment"
    assert text["source_id"] == "source:connected-shop:context"
    assert "delayed until Payment P1" in text["text"]
    assert text["locator"] == "row:3:text"
    assert text["sha256"] == run.digest(replay.retained_bytes(text["source_id"]))
    assert result["rule"]["maximum_unpaid"] == 1
    assert result["rule"]["source"]["passage_id"] == "intro-7-policy"
    assert result["reader"]["spec_sha256"] == run.digest(
        (run.HERE / "shipment_read_spec.json").read_bytes()
    )
    for invoice in result["invoices"]:
        assert invoice["status"] == "UNKNOWN"
        assert invoice["source_witnesses"]
        for witness in invoice["source_witnesses"]:
            trace = api.trace_population_record(replay, witness["record_id"])
            assert any(d["locator"] == witness["locator"] for d in trace.derivations)
    assert {x["invoice"]: x["order"] for x in result["invoices"]} == {
        "I1": "O1",
        "I2": "O2",
    }


def test_reopen_cli_is_read_only_and_matches_api(subject, executed):
    path, replay = executed
    before = path.read_bytes()
    reopened = api.KnowledgeChangeHistory.reopen(path).replay()
    assert subject.explain_shipments(reopened) == subject.explain_shipments(replay)
    result = subprocess.run(
        [sys.executable, "-m", MODULE, str(path), "--at-occurrence", "e30"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == subject.explain_shipments(
        replay, at_occurrence="e30"
    )
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "statuses,complete,outcome,upper",
    [
        (["UNPAID", "UNPAID"], True, "VIOLATED", 2),
        (["UNPAID", "PAID"], True, "SATISFIED", 1),
        (["PAID", "PAID"], True, "SATISFIED", 0),
        (["UNKNOWN", "UNKNOWN"], True, "CANNOT_DETERMINE", 2),
        (["PAID", "PAID"], False, "CANNOT_DETERMINE", None),
        (["UNPAID", "UNPAID"], False, "VIOLATED", None),
    ],
)
def test_synthetic_explicit_status_bounds(subject, statuses, complete, outcome, upper):
    observations = [
        {"invoice": f"synthetic:{i}", "status": status}
        for i, status in enumerate(statuses)
    ]
    result = subject.check_invoice_limit(
        observations, account_complete=complete, maximum_unpaid=1
    )
    assert result["outcome"] == outcome
    assert result["unpaid_upper_bound"] == upper


@pytest.mark.parametrize(
    "observations",
    [
        [{"invoice": "synthetic:A"}],
        [{"invoice": "synthetic:A", "status": "CLEARED_SO_PAID_FOREVER"}],
        [{"invoice": "synthetic:A", "status": "PAID"}] * 2,
    ],
)
def test_missing_invalid_duplicate_status_cannot_manufacture_pass(
    subject, observations
):
    with pytest.raises(ValueError):
        subject.check_invoice_limit(
            observations, account_complete=True, maximum_unpaid=1
        )


@pytest.mark.parametrize("damage", ["invoice", "ownership", "receipt", "clearing"])
def test_damaged_read_evidence_is_unknown_not_a_smaller_pass(subject, executed, damage):
    _, replay = executed
    records = deepcopy(replay.graph.export_records())
    removed = {
        "invoice": "invoice:I2",
        "ownership": "participation:e5:order:O2",
        "receipt": "e29",
        "clearing": "participation:e30:invoice:I2",
    }[damage]
    # A checked hypothetical read projection, not a mutation of source/history.
    for family in records:
        records[family] = [r for r in records[family] if r["id"] != removed]
    records["event_participations"] = [
        r
        for r in records["event_participations"]
        if r["properties"]["event_id"] != removed
        and r["properties"]["entity_id"] != removed
    ]
    graph = KnowledgeGraph.from_records(replay.contract_view, records)
    result = subject.inspect_invoice_evidence(graph, replay)
    assert {x["invoice"] for x in result["invoices"]} == {"I1", "I2"}
    assert all(x["status"] == "UNKNOWN" for x in result["invoices"])
    assert result["gaps"]
    if damage in ("receipt", "clearing"):
        assert (
            next(x for x in result["invoices"] if x["invoice"] == "I2")[
                "clearing_events"
            ]
            == []
        )


def test_wrong_invoice_link_does_not_count_as_expected_order(subject, executed):
    _, replay = executed
    records = deepcopy(replay.graph.export_records())
    next(
        x
        for x in records["event_participations"]
        if x["id"] == "participation:e5:order:O2"
    )["properties"]["entity_id"] = "order:O1"
    graph = KnowledgeGraph.from_records(replay.contract_view, records)
    result = subject.inspect_invoice_evidence(graph, replay)
    assert "INVOICE_ORDER_LINK_MISMATCH:I2" in result["gaps"]


def test_unrelated_supplier_update_does_not_change_rule_assessment(subject, executed):
    _, replay = executed
    assert (
        subject.explain_shipments(replay, at_occurrence="e6")["invoice_limit"]
        == subject.explain_shipments(replay, at_occurrence="e7")["invoice_limit"]
    )
    with pytest.raises(ValueError, match="occurrence"):
        subject.explain_shipments(replay, at_occurrence="missing")
