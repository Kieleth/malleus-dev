"""Compare recorded unit order, not elapsed time or a complete physical queue."""

from copy import deepcopy
import importlib
import json
import subprocess
import sys

import pytest
import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    run as base,
)
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.warehouse import (
    run,
)


@pytest.fixture(scope="module")
def subject():
    return importlib.import_module(run.__package__ + ".ordering")


@pytest.fixture(scope="module")
def executed(subject, tmp_path_factory):
    path = tmp_path_factory.mktemp("shop-ordering") / "history.jsonl"
    base.run_story(path)
    replay = run.append_warehouse(path)
    return path, replay


def synthetic():
    spec = {
        "id": "synthetic-ordering",
        "unit_type": "InventoryUnit",
        "participation_role": "ITEM",
        "units": ["item:A", "item:B"],
        "queues": [{"entry": "UNPACK", "exit": "SCAN"}],
    }
    view = {"objects": {}, "events": {}}
    for unit, entry, exit in (
        ("A", "04-05 10:00", "04-05 13:00"),
        ("B", "04-05 11:00", "04-05 14:00"),
    ):
        identifiers = [f"{unit}:entry", f"{unit}:exit"]
        view["objects"]["item:" + unit] = {
            "type": "InventoryUnit",
            "event_ids": identifiers,
        }
        for identifier, activity, time in zip(
            identifiers, ["UNPACK", "SCAN"], [entry, exit], strict=True
        ):
            view["events"][identifier] = {
                "event_type": activity,
                "time_text": time,
                "participants": {"ITEM": ["item:" + unit]},
            }
    return view, spec


def pair_result(subject, view, spec):
    return subject.inspect_ordering(view, spec)["queues"]["UNPACK:SCAN"]["pairs"][0]


@pytest.mark.parametrize("reversed_order", [False, True])
def test_preserved_and_reversed_order_discriminate(subject, reversed_order):
    view, spec = synthetic()
    if reversed_order:
        view["events"]["A:exit"]["time_text"] = "04-05 15:00"
    result = pair_result(subject, view, spec)
    assert result["outcome"] == ("REVERSED" if reversed_order else "PRESERVED")
    assert result["entry_order"] == "BEFORE"
    assert result["exit_order"] == ("AFTER" if reversed_order else "BEFORE")
    assert result["issues"] == []


@pytest.mark.parametrize("stage", ["entry", "exit"])
def test_ties_never_use_identifier_order_as_a_tiebreaker(subject, stage):
    view, spec = synthetic()
    view["events"][f"B:{stage}"]["time_text"] = view["events"][f"A:{stage}"][
        "time_text"
    ]
    result = pair_result(subject, view, spec)
    assert result["outcome"] == "UNDETERMINED"
    assert result[f"{stage}_order"] == "TIED"
    assert any(x["reason"] == "TIED_PRINTED_TIMES" for x in result["issues"])


@pytest.mark.parametrize("problem", ["missing", "unplaced", "repeated", "backward"])
def test_incomplete_or_ambiguous_routes_cannot_certify_order(subject, problem):
    view, spec = synthetic()
    if problem == "missing":
        view["objects"]["item:B"]["event_ids"].remove("B:entry")
    elif problem == "unplaced":
        view["events"]["B:entry"]["time_text"] = "00-01 10:30"
    elif problem == "repeated":
        view["events"]["B:again"] = deepcopy(view["events"]["B:entry"])
        view["objects"]["item:B"]["event_ids"].append("B:again")
    else:
        view["events"]["B:exit"]["time_text"] = "04-05 09:00"
    result = pair_result(subject, view, spec)
    assert result["outcome"] == "UNDETERMINED"
    expected = {
        "missing": "MISSING_OBSERVATION",
        "unplaced": "UNPLACED_TIME",
        "repeated": "REPEATED_ACTIVITY",
        "backward": "NON_FORWARD_STAGE_PAIR",
    }[problem]
    assert any(x["reason"] == expected for x in result["issues"])


def test_missing_unit_does_not_shrink_the_declared_denominator(subject):
    view, spec = synthetic()
    del view["objects"]["item:B"]
    result = subject.inspect_ordering(view, spec)["queues"]["UNPACK:SCAN"]
    assert len(result["pairs"]) == 1
    assert result["counts"] == {"PRESERVED": 0, "REVERSED": 0, "UNDETERMINED": 1}
    assert result["conclusion"] == "NO_COMPARABLE_PAIRS"
    assert any(x["reason"] == "MISSING_UNIT" for x in result["pairs"][0]["issues"])


def test_view_iteration_and_unrelated_events_do_not_change_the_result(subject):
    view, spec = synthetic()
    expected = subject.inspect_ordering(view, spec)
    view["events"] = dict(reversed(list(view["events"].items())))
    for unit in view["objects"].values():
        unit["event_ids"].reverse()
    view["events"]["unrelated"] = {
        "event_type": "OTHER",
        "time_text": "00-01 00:00",
        "participants": {"ITEM": ["item:A"]},
    }
    view["objects"]["item:A"]["event_ids"].append("unrelated")
    assert subject.inspect_ordering(view, spec) == expected


def test_duplicate_units_and_misbound_links_refuse(subject):
    view, spec = synthetic()
    spec["units"].append("item:A")
    with pytest.raises(ValueError, match="unique"):
        subject.inspect_ordering(view, spec)
    spec["units"].pop()
    view["events"]["A:entry"]["participants"]["ITEM"] = ["item:B"]
    with pytest.raises(ValueError, match="participation"):
        subject.inspect_ordering(view, spec)


def test_real_chapter_comparison_keeps_unknown_pairs_visible(subject, executed):
    _, replay = executed
    report = subject.read_ordering(replay)
    for name, counts in {
        "UNPACK:SCAN": {"PRESERVED": 5, "REVERSED": 1, "UNDETERMINED": 4},
        "SCAN:STORE": {"PRESERVED": 6, "REVERSED": 0, "UNDETERMINED": 4},
        "STORE:RETRIEVE": {"PRESERVED": 6, "REVERSED": 0, "UNDETERMINED": 4},
    }.items():
        queue = report["queues"][name]
        assert queue["counts"] == counts
        assert len(queue["pairs"]) == 10
        assert queue["coverage"] == "PARTIAL"
        assert queue["conclusion"] == (
            "OBSERVED_REVERSAL"
            if name == "UNPACK:SCAN"
            else "NO_REVERSAL_IN_COMPARABLE_PAIRS"
        )
    pairs = report["queues"]["UNPACK:SCAN"]["pairs"]
    assert [p["units"] for p in pairs if p["outcome"] == "REVERSED"] == [
        ["item:Y1", "item:Y2"]
    ]
    assert all(p["outcome"] == "UNDETERMINED" for p in pairs if "item:X3" in p["units"])
    assert report["observations"]["e8"]["time_text"] == "00-01 10:30"
    assert report["not_claimed"] == ["FULL_FIFO", "ELAPSED_TIME", "CAUSALITY"]


def test_every_compared_observation_has_exact_source_and_unit_witnesses(
    subject, executed
):
    _, replay = executed
    report = subject.read_ordering(replay)
    seen_sources = set()
    for identifier, observation in report["observations"].items():
        witnesses = observation["witnesses"]
        assert any(
            w["record_id"] == identifier and w["path"] == ["properties", "time_text"]
            for w in witnesses
        )
        assert any(w["path"] == ["properties", "entity_id"] for w in witnesses)
        for witness in witnesses:
            trace = api.trace_population_record(replay, witness["record_id"])
            assert any(
                dict(d) == {**witness, "path": tuple(witness["path"])}
                for d in trace.derivations
            )
            seen_sources.add(witness["source_id"])
    assert seen_sources == {base.SOURCE_ID, run.SOURCE_ID}


def test_reopen_maintained_reader_and_cli_are_read_only_and_reproducible(
    subject, executed
):
    path, replay = executed
    saved = path.read_bytes()
    expected = subject.read_ordering(replay)
    reopened = api.KnowledgeChangeHistory.reopen(path).replay()
    maintained = api.KnowledgeHistoryProjection.open(path).current(
        expected_head_hash=replay.ledger_head,
        expected_event_count=replay.ledger_event_count,
    )
    assert (
        subject.read_ordering(reopened) == subject.read_ordering(maintained) == expected
    )
    result = subprocess.run(
        [sys.executable, "-m", subject.__name__, str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == expected
    assert subject.receipt(expected) == json.loads(
        (run.HERE / "ordering_receipt.json").read_bytes()
    )
    assert (
        base.digest(saved)
        == json.loads((run.HERE / "receipt.json").read_bytes())["history_sha256"]
    )
    assert path.read_bytes() == saved
