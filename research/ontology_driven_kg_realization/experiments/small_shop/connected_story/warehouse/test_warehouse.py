"""Figure 14 extends the retained Table 1 history, not a second graph."""

from copy import deepcopy
import importlib
import json
import shutil

import pytest
import yaml

import malleus.compiler as api
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    object_timelines,
    run,
)


IDS = ["e12", "e13", "e14", "e15", "e16", "e17", "e22", "e23", "e24", "e25", "e26", "e31", "e32"]


@pytest.fixture(scope="module")
def subject():
    return importlib.import_module(run.__package__ + ".warehouse.run")


@pytest.fixture(scope="module")
def executed(subject, tmp_path_factory):
    path = tmp_path_factory.mktemp("warehouse") / "history.jsonl"
    before = run.run_story(path)
    prefix = path.read_bytes()
    after = subject.append_warehouse(path)
    return path, prefix, before, after


def test_exact_figure_inventory_has_no_invented_actor(subject):
    rows, boundary = subject.load_source()
    assert [row["event_id"] for row in rows] == IDS
    assert all(set(row) == {"event_id", "activity", "time_text", "item_ids"} for row in rows)
    assert sum(map(len, rows)) == 52
    assert {x for row in rows for x in row["item_ids"]} == {"X1", "X2", "X3", "Y1", "Y2"}
    assert rows[0] == {"event_id": "e12", "activity": "Scan", "time_text": "04-05 13:00", "item_ids": ["X1"]}
    assert rows[-1] == {"event_id": "e32", "activity": "Retrieve", "time_text": "09-05 09:45", "item_ids": ["Y2"]}
    assert boundary["source"]["license"] == "CC-BY-4.0"
    assert boundary["source"]["figure_url"].endswith("/figures/14")


def test_changed_source_bytes_refuse(subject, tmp_path):
    directory = tmp_path / "inputs"
    shutil.copytree(subject.HERE / "sources", directory / "sources")
    shutil.copy2(subject.HERE / "source_boundary.json", directory)
    (directory / "sources/figure-14.jsonl").write_bytes(b'{}\n')
    with pytest.raises(ValueError, match="digest"):
        subject.load_source(directory)


def test_ontology_adds_only_three_activity_values(subject):
    before = yaml.safe_load((run.HERE / "shop.yaml").read_bytes())
    after = yaml.safe_load((subject.HERE / "shop.yaml").read_bytes())
    values = after["enums"]["ShopActivity"]["permissible_values"]
    assert set(values) - set(before["enums"]["ShopActivity"]["permissible_values"]) == {"SCAN", "STORE", "RETRIEVE"}
    for name in ("SCAN", "STORE", "RETRIEVE"):
        del values[name]
    after["version"] = before["version"]
    after["description"] = before["description"]
    assert after == before


def test_same_history_revision_preserves_the_complete_prefix(subject, executed):
    path, prefix, before, after = executed
    assert run.digest(prefix) == json.loads((run.HERE / "run_receipt.json").read_bytes())["ledger_sha256"]
    assert path.read_bytes().startswith(prefix)
    assert len(after.change_sets) == 34
    assert len(after.contract_revisions) == 1
    assert [change.kind for change in after.contract_revisions[0].changes] == ["ADD_ENUM_VALUE"] * 3
    assert len(after.graph.query("ShopOccurrence")) == 34
    assert len(after.graph.query_event_participations()) == 75
    for identifier in before.record_history:
        assert after.record_history[identifier] == before.record_history[identifier]
        assert after.graph.get_node(identifier) == before.graph.get_node(identifier)
    assert after.graph.query("SupplierOrderState", product_code="Y")[0]["ordered_quantity"] == 2
    assert after.retained_bytes(run.SOURCE_ID) == before.retained_bytes(run.SOURCE_ID)


def test_unit_paths_gain_only_the_sourced_warehouse_steps(subject, executed):
    _, _, before, after = executed
    report = subject.read_warehouse(after)
    expected = {
        "X1": (["e10", "e12", "e13", "e22", "e27"], ["e6"]),
        "X2": (["e11", "e14", "e15", "e23", "e27"], ["e6"]),
        "X3": (["e16", "e17", "e31", "e33"], ["e6", "e8"]),
        "Y1": (["e19", "e20", "e26", "e27"], []),
        "Y2": (["e19", "e21", "e24", "e25", "e32", "e33"], []),
    }
    for unit, (placed, unplaced) in expected.items():
        lane = report["objects"]["item:" + unit]
        assert lane["printed_sequence"] == [[event] for event in placed]
        assert lane["unplaced_events"] == unplaced
    old = object_timelines.read_timelines(before)
    assert len(report["objects"]) == len(old["objects"]) == 17
    for identifier, lane in old["objects"].items():
        if not identifier.startswith("item:"):
            assert report["objects"][identifier]["event_ids"] == lane["event_ids"]
    assert all(report["events"][identifier]["participants"].keys() == {"ITEM"} for identifier in IDS)
    assert report["interpretation"]["calendar_instants"] == "NOT_DERIVED"


def test_every_new_field_traces_to_exact_figure_rows(subject, executed):
    _, _, _, replay = executed
    rows, _ = subject.load_source()
    for ordinal, row in enumerate(rows):
        event_id = row["event_id"]
        targets = [event_id, "participation:" + event_id + ":item:" + row["item_ids"][0]]
        locators = set()
        for record_id in targets:
            trace = api.trace_population_record(replay, record_id)
            assert trace.change_set.valid_time.kind == "NONE_STATED"
            assert trace.change_set.valid_time.value is None
            assert trace.change_set.contract_identity == replay.partial_contract.identity
            for derivation in trace.derivations:
                assert derivation["source_id"] == subject.SOURCE_ID
                locators.add(derivation["locator"])
        assert locators == {f"row:{ordinal}:{field}" for field in ("event_id", "activity", "time_text", "item_ids[0]")}
    assert replay.retained_bytes(subject.SOURCE_ID) == (subject.HERE / "sources/figure-14.jsonl").read_bytes()


def test_unknown_unit_or_extra_field_is_not_silently_populated(subject, executed):
    _, _, before, _ = executed
    row = subject.load_source()[0][0]
    unknown = deepcopy(row)
    unknown["item_ids"] = ["Z1"]
    with pytest.raises(ValueError, match="existing InventoryUnit"):
        subject.build_plan(before, unknown, 0)
    invented = {**row, "actor_ids": ["R2"]}
    with pytest.raises(ValueError, match="four source fields"):
        subject.build_plan(before, invented, 0)


def test_second_append_refuses_without_changing_bytes(subject, executed):
    path, _, _, _ = executed
    saved = path.read_bytes()
    with pytest.raises(ValueError, match="exact Table 1 baseline"):
        subject.append_warehouse(path)
    assert path.read_bytes() == saved


def test_reopen_and_maintained_replay_agree(subject, executed):
    path, _, _, after = executed
    saved = path.read_bytes()
    reopened = api.KnowledgeChangeHistory.reopen(path).replay()
    maintained = api.KnowledgeHistoryProjection.open(path).current
    assert subject.read_warehouse(reopened) == subject.read_warehouse(after)
    assert subject.read_warehouse(maintained) == subject.read_warehouse(after)
    assert path.read_bytes() == saved


def test_recorded_receipt_is_reproducible(subject, executed):
    path, prefix, _, replay = executed
    assert subject.receipt(replay, path.read_bytes(), prefix) == json.loads((subject.HERE / "receipt.json").read_bytes())
