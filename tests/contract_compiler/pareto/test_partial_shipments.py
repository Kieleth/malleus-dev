"""Synthetic Shop extension, tested through real public history boundaries."""

import ast
from hashlib import sha256
from importlib import import_module
import json
from pathlib import Path
import shutil

import pytest

import malleus.compiler as api


MODULE = "research.ontology_driven_kg_realization.experiments.small_shop.partial_shipments.run"
HERE = (
    Path(__file__).resolve().parents[3]
    / "research/ontology_driven_kg_realization/experiments/small_shop/partial_shipments"
)
ACTOR = "actor:synthetic-partial-shipments"
TIME = "2026-09-08T01:00:00Z"


def _example():
    return import_module(MODULE)


def test_partial_shipments_preserve_prior_shop_then_reopen_and_trace(tmp_path):
    example = _example()
    report = example.run_shipments(tmp_path / "first")
    history_path = tmp_path / "first/shop/history.jsonl"
    source = history_path.read_bytes()
    assert example.run_shipments(tmp_path / "second") == report
    assert (tmp_path / "second/shop/history.jsonl").read_bytes() == source
    assert (tmp_path / "first/evidence.json").read_bytes() == (
        tmp_path / "second/evidence.json"
    ).read_bytes()
    isolated = tmp_path / "only-history.jsonl"
    shutil.copyfile(history_path, isolated)
    replay = api.KnowledgeChangeHistory.reopen(isolated).replay()

    assert report["checkpoints"] == json.loads((HERE / "expected.json").read_bytes())
    assert report["prior_records_preserved"] is True
    assert (
        "sha256:" + sha256(source[: report["baseline_byte_count"]]).hexdigest()
        == (report["baseline_sha256"])
    )
    assert len(replay.change_sets) == 8
    assert len(replay.contract_revisions) == 2
    assert len(replay.record_history) == 21
    assert replay.graph.query("SupplierOrderState")[0]["ordered_quantity"] == 2
    assert replay.record_history["supplier-order-state:B:e4"].superseded_by == (
        "supplier-order-state:B:e7"
    )
    assert replay.graph.query("Shipment") == [
        {"id": "SYN-S1", "type": "Shipment", "tracking_id": "SYN-TRACK-1"},
        {"id": "SYN-S2", "type": "Shipment", "tracking_id": "SYN-TRACK-2"},
    ]
    previous = replay.graph_at_change("change:plan:partial-shipments:order")
    assert previous.get_node("SYN-PS-ORDER")["order_number"] == "SYN-PS-ORDER"
    assert previous.get_node("SYN-S1") is None
    revision = replay.contract_revisions[-1]
    assert {change.kind for change in revision.changes} == {
        "ADD_CLASS",
        "ADD_SLOT",
        "ADD_ENUM_VALUE",
    }
    assert len(revision.changes) == 6
    assert (
        replay.change_sets[-3].contract_identity
        != replay.change_sets[-2].contract_identity
    )
    assert (
        replay.change_sets[-2].contract_identity
        == replay.change_sets[-1].contract_identity
    )

    for row, shipment in enumerate(("SYN-S1", "SYN-S2")):
        trace = api.trace_population_record(replay, shipment)
        assert trace.history_profile == api.STATE_VERSION_PROFILE
        assert trace.record_history.valid_from.kind == "NONE_STATED"
        assert trace.record_history.supersedes_record_id is None
        assert trace.record_history.superseded_by is None
        assert len(trace.sources) == 1
        assert trace.sources[0].record_id == "source:partial-shipments:shipments"
        assert trace.sources[0].content == (HERE / "shipments.jsonl").read_bytes()
        assert {item["locator"] for item in trace.derivations} == {
            f"row:{row}:tracking_id"
        }
        evidence = {item.record_id: item.content for item in trace.evidence}
        assert (
            evidence["artifact:partial-shipments:mapping"]
            == (HERE / "mapping.json").read_bytes()
        )
    assert isolated.read_bytes() == source


def test_shipment_type_requires_revision_and_bad_endpoint_is_atomic(tmp_path):
    example = _example()
    history = example.start(tmp_path / "shop")
    example.admit_plan(history, "order", transaction_time=TIME, actor_id=ACTOR)
    before = history.path.read_bytes()
    with pytest.raises(api.PopulationPlanRefusal):
        example.prepare_plan(
            history, "shipment-1", transaction_time=TIME, actor_id=ACTOR
        )
    assert history.path.read_bytes() == before

    example.revise(history, transaction_time=TIME, actor_id=ACTOR)
    plan = example.plan_for(history, "shipment-1")
    plan["records"]["relations"][1]["target_id"] = "missing-unit"
    before = history.path.read_bytes()
    before_graph = history.replay().graph.export_records()
    with pytest.raises(api.PopulationPlanRefusal):
        example.prepare_plan(history, plan, transaction_time=TIME, actor_id=ACTOR)
    assert history.path.read_bytes() == before
    assert history.replay().graph.export_records() == before_graph


def test_shipment_preparation_refuses_after_intervening_evidence(tmp_path):
    example = _example()
    history = example.start(tmp_path / "shop")
    example.admit_plan(history, "order", transaction_time=TIME, actor_id=ACTOR)
    example.revise(history, transaction_time=TIME, actor_id=ACTOR)
    prepared = example.prepare_plan(
        history, "shipment-1", transaction_time=TIME, actor_id=ACTOR
    )
    history.append_anchors(
        anchors=(
            api.structural_evidence_anchor(
                record_id="artifact:intervening",
                content=b"later",
                media_type="text/plain",
            ),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    before = history.path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as error:
        api.admit_structural_change(
            history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
        )
    assert error.value.reason is api.KnowledgeChangeRefusalReason.STALE_BASE
    assert history.path.read_bytes() == before


def test_runner_reuses_public_core_and_never_reads_its_answer_key():
    example = _example()
    source = Path(example.__file__).read_text()
    imports = {
        name
        for node in ast.walk(ast.parse(source))
        for name in (
            [node.module or ""]
            if isinstance(node, ast.ImportFrom)
            else [item.name for item in node.names]
            if isinstance(node, ast.Import)
            else []
        )
    }
    assert {name for name in imports if name.startswith("malleus")} == {
        "malleus.compiler"
    }
    assert not any(
        name.startswith("tests") or "_contract_pipeline" in name for name in imports
    )
    assert "expected.json" not in source
    assert "CHECK_RECORDED" not in source
    assert "SATISFIED" not in source
