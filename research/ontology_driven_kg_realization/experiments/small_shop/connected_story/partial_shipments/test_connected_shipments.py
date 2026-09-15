"""The synthetic shipment cohort composes without changing chapter history or policy."""

import importlib
import json
import subprocess
import sys

import pytest
import yaml

import malleus.compiler as api
from malleus import bundled_ontology_path
from research.ontology_driven_kg_realization.experiments.small_shop.partial_shipments import (
    run as original,
)
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    run as base,
    shipment_explanation,
)
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.warehouse import (
    ordering,
    run as warehouse,
)


@pytest.fixture(scope="module")
def subject():
    return importlib.import_module(base.__package__ + ".partial_shipments.run")


@pytest.fixture(scope="module")
def executed(subject, tmp_path_factory):
    path = tmp_path_factory.mktemp("connected-shipments") / "history.jsonl"
    base.run_story(path)
    before = warehouse.append_warehouse(path)
    prefix = path.read_bytes()
    maintained = api.KnowledgeHistoryProjection.open(path)
    history = subject.start(path)
    states, views = {}, {}
    for name in ("order", "shipment-1", "shipment-2"):
        prepared = subject.prepare(history, subject.plan_for(history.replay(), name))
        replay = subject.admit(history, prepared)
        states[name] = path.read_bytes()
        refreshed = maintained.refresh(
            expected_head_hash=replay.ledger_head,
            expected_event_count=replay.ledger_event_count,
        )
        view = original.shipment_view(refreshed.graph, "SYN-PS-ORDER")
        assert view == original.shipment_view(replay.graph, "SYN-PS-ORDER")
        views[name] = view
    return path, prefix, before, replay, states, views


def test_schema_preserves_existing_declarations_and_optional_old_unit_data(subject):
    before = yaml.safe_load((warehouse.HERE / "shop.yaml").read_bytes())
    after = yaml.safe_load((subject.HERE / "shop.yaml").read_bytes())
    assert set(after["classes"]) - set(before["classes"]) == {
        "Shipment",
        "OrderContainsUnit",
        "OrderHasShipment",
        "ShipmentContainsUnit",
    }
    assert after["classes"]["InventoryUnit"]["slot_usage"] == {
        "product_code": {"required": False}
    }
    for name in set(after["classes"]) - set(before["classes"]):
        del after["classes"][name]
    after["classes"]["InventoryUnit"].pop("slots")
    after["classes"]["InventoryUnit"].pop("slot_usage")
    del after["slots"]["tracking_id"]
    for key in ("version", "description"):
        after[key] = before[key]
    assert after == before


def test_same_history_and_policy_preserve_every_prior_record(subject, executed):
    path, prefix, before, after, _, _ = executed
    assert (
        base.digest(prefix)
        == json.loads((warehouse.HERE / "receipt.json").read_bytes())["history_sha256"]
    )
    assert path.read_bytes().startswith(prefix)
    assert (
        after.partial_contract.normative_profile
        == before.partial_contract.normative_profile
    )
    assert len(after.change_sets) == len(before.change_sets) + 3
    assert len(after.contract_revisions) == 2
    kinds = [c.kind for c in after.contract_revisions[-1].changes]
    assert kinds.count("ADD_CLASS") == 4 and kinds.count("ADD_SLOT") == 2
    for key in before.record_history:
        assert after.record_history[key] == before.record_history[key]
        assert after.graph.get_node(key) == before.graph.get_node(key)
    assert len(after.record_history) - len(before.record_history) == 11
    assert len(after.graph.query("ShopOccurrence")) == 34
    assert "product_code" not in after.graph.get_node("item:X1")
    assert after.graph.get_node("SYN-PS-X1")["product_code"] == "X"


def test_remaining_units_match_the_existing_independent_answer_key(subject, executed):
    _, _, _, replay, _, views = executed
    expected = json.loads((original.HERE / "expected.json").read_bytes())
    assert list(views.values()) == list(expected.values())
    report = subject.report(replay)
    assert report["checkpoints"] == expected
    assert report["kind"] == "SYNTHETIC_CONFORMANCE_EXTENSION"
    assert report["duplicate_assignment_rule"] == "NOT_SELECTED"
    assert report["admission"] == "UNCHANGED_CONNECTED_STRUCTURAL_POLICY"


def test_new_records_and_every_property_retain_synthetic_source_witnesses(
    subject, executed
):
    _, _, before, after, _, _ = executed
    report = subject.report(after)
    added = set(after.record_history) - set(before.record_history)
    assert set(report["witnesses"]) == added
    source_ids = set()
    for record_id in added:
        trace = api.trace_population_record(after, record_id)
        assert trace.change_set.valid_time.kind == "NONE_STATED"
        assert trace.change_set.valid_time.value is None
        assert trace.change_set.contract_identity == after.partial_contract.identity
        for d in trace.derivations:
            source_ids.add(d["source_id"])
            assert {**d, "path": list(d["path"])} in report["witnesses"][record_id]
        node = after.graph.get_node(record_id)
        if node is not None and "source_identifier" in node:
            assert node["source_identifier"] == record_id
    assert source_ids == {
        "source:connected-shop:synthetic-order",
        "source:connected-shop:synthetic-shipments",
    }
    for name in ("order", "shipments"):
        assert (
            after.retained_bytes(subject.source_id(name))
            == (original.HERE / f"{name}.jsonl").read_bytes()
        )
    assert (
        after.retained_bytes(subject.BOUNDARY_ID)
        == (subject.HERE / "input_boundary.json").read_bytes()
    )


def test_chapter_explanations_and_ordering_results_keep_their_meaning(
    subject, executed
):
    _, _, before, after, _, _ = executed
    old = shipment_explanation.explain_shipments(before)
    new = shipment_explanation.explain_shipments(after)
    assert {k: v for k, v in old.items() if k != "checkpoint"} == {
        k: v for k, v in new.items() if k != "checkpoint"
    }
    old_ordering = ordering.read_ordering(before)
    new_ordering = ordering.read_ordering(after)
    assert {k: v for k, v in old_ordering.items() if k != "binding"} == {
        k: v for k, v in new_ordering.items() if k != "binding"
    }


@pytest.mark.parametrize("problem", ["missing_endpoint", "missing_tracking"])
def test_bad_plans_refuse_before_preparation_writes(
    subject, executed, tmp_path, problem
):
    path = tmp_path / "history.jsonl"
    path.write_bytes(executed[4]["shipment-1"])
    history = api.KnowledgeChangeHistory.reopen(path)
    plan = subject.plan_for(history.replay(), "shipment-2")
    if problem == "missing_endpoint":
        plan["records"]["relations"][-1]["target_id"] = "ABSENT-UNIT"
    else:
        del plan["records"]["entities"][0]["properties"]["tracking_id"]
        plan["derivations"] = [
            d for d in plan["derivations"] if d["path"] != ["properties", "tracking_id"]
        ]
    saved = path.read_bytes()
    with pytest.raises(api.PopulationPlanRefusal) as found:
        subject.prepare(history, plan)
    assert found.value.reason.name == (
        "DANGLING_ENDPOINT"
        if problem == "missing_endpoint"
        else "RECORDS_NOT_REHYDRATABLE"
    )
    assert path.read_bytes() == saved


@pytest.mark.parametrize("problem", ["changed_source", "wrong_prefix"])
def test_start_refuses_before_revision_or_source_writes(
    subject, executed, tmp_path, problem
):
    path = tmp_path / "history.jsonl"
    path.write_bytes(
        executed[1] if problem == "changed_source" else executed[4]["shipment-2"]
    )
    directory = subject.HERE
    if problem == "changed_source":
        directory = tmp_path / "inputs"
        directory.mkdir()
        boundary = json.loads((subject.HERE / "input_boundary.json").read_bytes())
        bad = directory / "bad.jsonl"
        bad.write_bytes(b"{}\n")
        boundary["sources"]["order"]["path"] = str(bad)
        (directory / "input_boundary.json").write_bytes(base.canonical(boundary))
    saved = path.read_bytes()
    with pytest.raises(ValueError, match="digest|exact warehouse"):
        subject.start(path, directory=directory)
    assert path.read_bytes() == saved


def test_structural_policy_is_not_misreported_as_duplicate_assignment_enforcement(
    subject, executed, tmp_path
):
    path = tmp_path / "duplicate-control.jsonl"
    path.write_bytes(executed[4]["shipment-1"])
    history = api.KnowledgeChangeHistory.reopen(path)
    content = (
        original.HERE.parent / "shipment_policy/duplicate-unit.jsonl"
    ).read_bytes()
    history.append_anchors(
        anchors=api.structural_source_anchors(
            source_id="source:duplicate-control",
            artifact_id="artifact:duplicate-control",
            content=content,
            media_type="application/x-ndjson",
        ),
        transaction_time=subject.TIME,
        actor_id=subject.ACTOR,
    )
    plan = subject.plan_for(
        history.replay(), "shipment-2", source_id="source:duplicate-control"
    )
    after = subject.admit(history, subject.prepare(history, plan))
    assert (
        len(after.graph.query_relations("ShipmentContainsUnit", target_id="SYN-PS-X1"))
        == 2
    )
    assert original.shipment_view(after.graph, "SYN-PS-ORDER")["remaining_units"] == [
        "SYN-PS-X2"
    ]
    assert (
        after.partial_contract.normative_profile
        == executed[2].partial_contract.normative_profile
    )


def test_public_schema_inspector_and_cli_reproduce_the_frozen_result(
    subject, executed, tmp_path
):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.inquisition.cli",
            str(subject.HERE / "shop.yaml"),
            "--map",
            f"object-event={bundled_ontology_path('profiles', 'object-event.yaml').resolve()}",
            "--map",
            f"malleus={bundled_ontology_path('malleus.yaml').resolve()}",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ROOT ONTOLOGY PROFILE PURITY SEAL GRANTED" in result.stdout
    path = tmp_path / "history.jsonl"
    path.write_bytes(executed[1])
    result = subprocess.run(
        [sys.executable, "-m", subject.__name__, str(path), "--append"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert path.read_bytes() == executed[0].read_bytes()
    assert json.loads(result.stdout) == json.loads(
        (subject.HERE / "receipt.json").read_bytes()
    )
    saved = path.read_bytes()
    replay = api.KnowledgeChangeHistory.reopen(path).replay()
    result = subprocess.run(
        [sys.executable, "-m", subject.__name__, str(path), "--reopen"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (
        json.loads(result.stdout)
        == subject.report(replay)
        == subject.report(executed[3])
    )
    assert path.read_bytes() == saved


def test_runner_reuses_the_query_without_reading_the_expected_answers(subject):
    assert subject.shipment_view is original.shipment_view
    assert "expected.json" not in (subject.HERE / "run.py").read_text()
