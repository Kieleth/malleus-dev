"""Adopter compatibility probe, not approval of a new history profile."""

from pathlib import Path

import pytest
import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.history_probe import (
    run_probe,
)


def test_occurrences_and_replacement_survive_public_reopen(tmp_path):
    replay = run_probe(tmp_path / "history.jsonl")
    assert {row["id"] for row in replay.graph.query("SupplierOrderOccurrence")} == {"e4", "e7"}
    assert len(replay.graph.query("SupplierOrder")) == 1
    assert [(row["id"], row["ordered_quantity"]) for row in replay.graph.query("SupplierOrderState")] == [("state:B:e7", 2)]
    assert replay.record_history["state:B:e4"].superseded_by == "state:B:e7"
    assert {row["entity_id"] for row in replay.graph.query_event_participations(event_id="e7")} == {"supplier-order:B"}
    assert len(replay.change_sets) == 2
    reopened = api.KnowledgeChangeHistory.reopen(tmp_path / "history.jsonl").replay()
    assert reopened.receipt.identity == replay.receipt.identity
    for record_id in replay.record_history:
        trace = api.trace_population_record(reopened, record_id)
        assert trace.sources[0].record_id == "source:connected-shop:table-1"
        assert trace.sources[0].content == (Path(__file__).parent / "sources/table-1.jsonl").read_bytes()


def test_state_only_profile_cannot_silently_drop_events(tmp_path):
    with pytest.raises(api.PopulationPlanRefusal) as refused:
        run_probe(tmp_path / "refused.jsonl", profile=api.STATE_VERSION_PROFILE)
    assert refused.value.reason == api.PopulationPlanRefusalReason.FAMILY_NOT_ADMITTED
    replay = api.KnowledgeChangeHistory.reopen(tmp_path / "refused.jsonl").replay()
    assert not replay.change_sets
    assert not replay.record_history


def test_same_inputs_reproduce_the_probe_history(tmp_path):
    first, second = tmp_path / "first.jsonl", tmp_path / "second.jsonl"
    run_probe(first)
    run_probe(second)
    assert first.read_bytes() == second.read_bytes()
