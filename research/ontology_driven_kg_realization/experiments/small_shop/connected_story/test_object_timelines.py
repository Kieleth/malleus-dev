"""Per-object Shop views, not a flattened case log or invented calendar."""

from copy import deepcopy
import importlib
import json
import subprocess
import sys

import pytest
from malleus import KnowledgeGraph
import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    run,
)


MODULE = run.__package__ + ".object_timelines"


@pytest.fixture(scope="module")
def subject():
    return importlib.import_module(MODULE)


@pytest.fixture(scope="module")
def executed(tmp_path_factory):
    path = tmp_path_factory.mktemp("shop-timelines") / "history.jsonl"
    return path, run.run_story(path)


def test_separate_objects_share_one_occurrence(subject, executed):
    _, replay = executed
    report = subject.read_timelines(replay)
    assert len(report["events"]) == 21
    assert len(report["objects"]) == 18
    assert report["objects"]["invoice:I2"]["printed_sequence"] == [
        ["e5"],
        ["e9"],
        ["e30"],
    ]
    assert report["objects"]["order:O1"]["printed_sequence"] == [
        ["e1"],
        ["e18"],
        ["e27"],
        ["e28"],
    ]
    assert report["objects"]["order:O2"]["printed_sequence"] == [
        ["e2"],
        ["e5"],
        ["e7"],
        ["e33"],
        ["e34"],
    ]
    for identifier in ("invoice:I1", "invoice:I2", "payment:P1"):
        assert "e30" in report["objects"][identifier]["event_ids"]
    assert report["events"]["e30"]["participants"]["INVOICE"] == [
        "invoice:I1",
        "invoice:I2",
    ]
    assert set(report["order_views"]["O1"]["objects"]) == {
        "order:O1",
        "invoice:I1",
        "payment:P1",
        "item:X1",
        "item:X2",
        "item:Y1",
        "supplier-order:A",
        "supplier-order:B",
    }
    assert set(report["order_views"]["O2"]["objects"]) == {
        "order:O2",
        "invoice:I2",
        "payment:P1",
        "item:X3",
        "item:Y2",
        "supplier-order:A",
        "supplier-order:B",
    }
    assert "printed_sequence" not in report["order_views"]["O1"]
    assert report["order_views"]["O1"]["scope"] == "RETROSPECTIVE_RECORDED_JOINS"


def test_bad_source_dates_stay_visible_and_do_not_create_adjacency(subject, executed):
    _, replay = executed
    report = subject.read_timelines(replay)
    lane = report["objects"]["supplier-order:A"]
    assert lane["unplaced_events"] == ["e6", "e8"]
    assert lane["printed_sequence"] == [["e3"], ["e10"], ["e11"]]
    assert lane["ordering_gaps"] == ["UNPLACED_EVENTS"]
    assert report["events"]["e6"]["time_text"] == "00-01 10:00"
    assert report["events"]["e8"]["time_text"] == "00-01 10:30"
    assert report["objects"]["supplier-order:B"]["printed_sequence"] == [
        ["e4"],
        ["e7"],
        ["e19"],
        ["e20"],
        ["e21"],
    ]
    assert "e7" not in lane["event_ids"]  # B's update is not A's successor.
    assert report["interpretation"]["calendar_instants"] == "NOT_DERIVED"
    assert report["interpretation"]["source_trust"] == "TRUSTED_FOR_THIS_EXPERIMENT"


def test_all_occurrences_and_links_have_real_trace_witnesses(subject, executed):
    _, replay = executed
    report = subject.read_timelines(replay)
    for record in [*report["events"].values(), *report["objects"].values()]:
        assert record["witnesses"]
        for witness in record["witnesses"]:
            trace = api.trace_population_record(replay, witness["record_id"])
            assert any(
                d["source_id"] == witness["source_id"]
                and d["locator"] == witness["locator"]
                for d in trace.derivations
            )
    assert {x["locator"] for x in report["events"]["e30"]["witnesses"]} >= {
        "row:18:time_text"
    }


def test_graph_iteration_order_is_not_business_order(subject, executed):
    _, replay = executed
    records = deepcopy(replay.graph.export_records())
    for family in records:
        records[family].reverse()
    reordered = KnowledgeGraph.from_records(replay.contract_view, records)
    mapping = json.loads(replay.retained_bytes(run.MAPPING_ID))
    assert subject.inspect_object_views(
        reordered, mapping
    ) == subject.inspect_object_views(replay.graph, mapping)


def test_tied_printed_times_stay_unordered_and_missing_time_stays_unplaced(subject):
    events = [
        {"id": "z", "time_text": "04-05 10:00"},
        {"id": "a", "time_text": "04-05 10:00"},
        {"id": "earlier", "time_text": "03-05 15:00"},
        {"id": "unknown", "time_text": "not stated"},
    ]
    expected = {
        "printed_sequence": [["earlier"], ["a", "z"]],
        "unplaced_events": ["unknown"],
        "ordering_gaps": ["TIED_PRINTED_TIMES", "UNPLACED_EVENTS"],
    }
    assert subject.order_printed_events(events) == expected
    assert subject.order_printed_events(list(reversed(events))) == expected


@pytest.mark.parametrize(
    "value", ["00-01 10:00", "31-04 10:00", "01-05 24:00", "29-02 10:00"]
)
def test_unusable_or_year_dependent_clock_is_not_repaired(subject, value):
    assert subject.order_printed_events([{"id": "synthetic", "time_text": value}]) == {
        "printed_sequence": [],
        "unplaced_events": ["synthetic"],
        "ordering_gaps": ["UNPLACED_EVENTS"],
    }


def test_missing_required_time_and_duplicate_event_ids_refuse(subject):
    with pytest.raises(ValueError, match="time_text"):
        subject.order_printed_events([{"id": "missing"}])
    with pytest.raises(ValueError, match="unique"):
        subject.order_printed_events([{"id": "same", "time_text": "01-05 09:00"}] * 2)


def test_reopen_cli_and_report_do_not_change_history(subject, executed):
    path, replay = executed
    before, graph = path.read_bytes(), replay.graph.snapshot()
    report = subject.read_timelines(replay)
    assert (
        subject.read_timelines(api.KnowledgeChangeHistory.reopen(path).replay())
        == report
    )
    result = subprocess.run(
        [sys.executable, "-m", MODULE, str(path)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == report
    assert path.read_bytes() == before
    assert replay.graph.snapshot() == graph


def test_maintained_views_match_full_replay_after_each_real_admission(
    subject, tmp_path, monkeypatch
):
    path = tmp_path / "history.jsonl"
    original = api.admit_structural_change
    reader, observations = None, []

    def admit(**kwargs):
        nonlocal reader
        if reader is None:
            reader = api.KnowledgeHistoryProjection.open(path)
        result = original(**kwargs)
        full = api.KnowledgeChangeHistory.reopen(path).replay()
        maintained = reader.refresh(
            expected_head_hash=full.ledger_head,
            expected_event_count=full.ledger_event_count,
        )
        assert subject.read_timelines(maintained) == subject.read_timelines(full)
        observations.append(len(full.graph.query("ShopOccurrence")))
        return result

    monkeypatch.setattr(api, "admit_structural_change", admit)
    replay = run.run_story(path)
    assert observations == list(range(1, 22))
    assert len(subject.read_timelines(replay)["events"]) == 21
