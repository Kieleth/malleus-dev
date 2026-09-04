"""Full Small Shop object-event conformance run."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import malleus.compiler as compiler

from research.ontology_driven_kg_realization.experiments.small_shop.object_event.run import (
    EXPECTED_EVIDENCE_PATH,
    ORACLE_PATH,
    PLAN_PATH,
    SOURCE_PATH,
    run_object_event,
)
from research.ontology_driven_kg_realization.experiments.small_shop.public_population.run import (
    _canonical,
)


def test_ret040_admits_reopens_replays_queries_and_traces(tmp_path: Path) -> None:
    output = tmp_path / "object-event"

    first = run_object_event(output)
    history_bytes = (output / "history.jsonl").read_bytes()
    second = run_object_event(output)

    assert first.evidence_bytes == second.evidence_bytes
    assert first.evidence_bytes == EXPECTED_EVIDENCE_PATH.read_bytes()
    assert first.replay.receipt == second.replay.receipt
    assert (output / "history.jsonl").read_bytes() == history_bytes
    evidence = json.loads(first.evidence_bytes)
    oracle = json.loads(ORACLE_PATH.read_bytes())
    assert evidence["oracle_matches"] is True
    assert evidence["source_identity"] == (
        "sha256:" + sha256(SOURCE_PATH.read_bytes()).hexdigest()
    )
    assert evidence["history"]["change_set_count"] == 1
    assert len(second.replay.record_history) == 11
    assert second.replay.graph.query_relations() == []
    assert evidence["observed"] == {
        "entities": oracle["expected"]["entities"],
        "event": [{**oracle["expected"]["event"], "is_event": True}],
        "participations": oracle["expected"]["participations"],
        "relation_count": 0,
    }

    for record_id in second.replay.record_history:
        trace = compiler.trace_population_record(second.replay, record_id)
        assert trace.history_profile == compiler.OBJECT_EVENT_PROFILE
        assert trace.population_plan["plan_id"] == (
            "plan:small-shop:ret-040-object-event"
        )
        assert trace.population_plan_bytes == _canonical(
            json.loads(PLAN_PATH.read_bytes())
        )
        assert [member.content for member in trace.sources] == [
            SOURCE_PATH.read_bytes()
        ]


def test_ret040_keeps_event_participation_out_of_ordinary_relations(
    tmp_path: Path,
) -> None:
    replay = run_object_event(tmp_path / "object-event").replay

    assert replay.graph.get_relation("participation:e27:O1:ORDER") is None
    assert replay.graph.query_relations() == []
    assert {
        record["entity_id"]
        for record in replay.graph.query_event_participations(event_id="e27")
    } == {"O1", "R4", "X1", "X2", "Y1"}


def test_ret040_fixture_manifest_binds_every_input_byte() -> None:
    fixture = PLAN_PATH.parents[2]
    manifest = json.loads((fixture / "manifest.json").read_bytes())

    assert manifest["input_set_id"] == "small-shop-object-event-ret-040-v1"
    for member in manifest["members"]:
        content = (fixture / member["path"]).read_bytes()
        assert member["bytes"] == len(content)
        assert member["sha256"] == "sha256:" + sha256(content).hexdigest()
