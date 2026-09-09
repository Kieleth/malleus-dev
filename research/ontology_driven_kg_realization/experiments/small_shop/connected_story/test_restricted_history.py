"""Shop-owned compatibility tests for Core's selected transition restriction."""

from copy import deepcopy
import json

import pytest
import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    core_contract_probe,
    restricted_history as subject,
)
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.history_probe import (
    ACTOR,
    HERE,
    SOURCE_ID,
)


TIME = "2026-09-08T00:03:00Z"


def _event_replacement(replay):
    """Synthetic hostile input, never another observation from the chapter."""
    plan = json.loads(replay.retained_bytes("plan:shop-probe:e7"))
    replacements = {
        "e7": "e7:replacement-probe",
        "participation:e7:B": "participation:e7:replacement-probe:B",
    }
    plan["plan_id"] = "plan:shop-restricted:replace-event"
    plan["records"]["entities"] = []
    for family in ("events", "event_participations"):
        for record in plan["records"][family]:
            record["id"] = replacements[record["id"]]
    plan["records"]["event_participations"][0]["properties"]["event_id"] = replacements[
        "e7"
    ]
    plan["derivations"] = [
        dict(deepcopy(item), record_id=replacements[item["record_id"]])
        for item in plan["derivations"]
        if item["record_id"] in replacements
    ]
    plan["supersessions"] = [
        {"record_id": new, "supersedes_record_id": old}
        for old, new in replacements.items()
    ]
    return plan


@pytest.mark.parametrize("match", ["EXACT", "SUBTYPE"])
def test_selected_state_replacement_and_events_survive_replay(tmp_path, match):
    profile = subject.proposed_profile()
    path = tmp_path / "history.jsonl"
    history = subject.start_history(path, profile=profile, match=match)
    reader = api.KnowledgeHistoryProjection.open(path)
    subject.admit_row(history, profile=profile, event_id="e4", previous=None)
    result = subject.admit_row(
        history, profile=profile, event_id="e7", previous="state:B:e4"
    )
    assert [
        (r["id"], r["ordered_quantity"])
        for r in result.graph.query("SupplierOrderState")
    ] == [("state:B:e7", 2)]
    assert {r["id"] for r in result.graph.query("SupplierOrderOccurrence")} == {
        "e4",
        "e7",
    }
    assert result.record_history["state:B:e4"].superseded_by == "state:B:e7"
    assert result.record_history["e4"].superseded_by is None
    assert result.record_history["e7"].superseded_by is None
    assert len(result.change_sets) == 2
    assert len(result.record_history) == 7
    assert len(result.graph.query_event_participations(event_id="e7")) == 1
    for replay in (
        api.KnowledgeChangeHistory.reopen(path).replay(),
        reader.refresh(
            expected_head_hash=result.ledger_head,
            expected_event_count=result.ledger_event_count,
        ),
    ):
        assert replay.receipt == result.receipt
        assert replay.record_history == result.record_history
        assert replay.graph.snapshot() == result.graph.snapshot()
        program = replay.partial_contract.normative_profile.protocol_machine_program
        assert program == subject.transition_program(profile=profile, match=match)
        for record_id in replay.record_history:
            trace = api.trace_population_record(replay, record_id)
            assert (
                next(
                    item.content
                    for item in trace.sources
                    if item.record_id == SOURCE_ID
                )
                == (HERE / "sources/table-1.jsonl").read_bytes()
            )


@pytest.mark.parametrize("match", ["EXACT", "SUBTYPE"])
def test_event_replacement_refuses_after_preparation_without_admission_mutation(
    tmp_path, match
):
    path = tmp_path / "history.jsonl"
    profile = subject.proposed_profile()
    before = subject.run_probe(path, profile=profile, match=match)
    history = api.KnowledgeChangeHistory.reopen(path)
    prepared = subject.prepare_plan(
        history, profile=profile, plan=_event_replacement(before), transaction_time=TIME
    )
    # Preparation retained evidence separately. Refusal preserves this boundary,
    # not the earlier bytes from before successful preparation.
    admission_bytes = path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as caught:
        api.admit_structural_change(
            history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
        )
    assert caught.value.reason.name == "TRANSITION_RULE_REFUSAL"
    assert "REPLACEMENT_OUTSIDE_SHOP_STATE_ROLE" in caught.value.detail
    assert "e7:replacement-probe" in caught.value.detail
    assert path.read_bytes() == admission_bytes
    after = api.KnowledgeChangeHistory.reopen(path).replay()
    assert after.record_history == before.record_history
    assert after.change_sets == before.change_sets
    assert after.graph.snapshot() == before.graph.snapshot()
    assert after.acceptance_head == before.acceptance_head
    assert after.materialization_head == before.materialization_head


@pytest.mark.parametrize("match,allowed", [("EXACT", False), ("SUBTYPE", True)])
def test_matching_choice_is_executable_data_not_an_ignored_label(
    tmp_path, match, allowed
):
    # Deliberately broader control role, not the proposed Shop selection.
    data = json.loads(subject.proposed_profile().canonical_bytes)
    data["ontology_roles"]["state"] = ["Entity"]
    profile = api.DomainHistoryProfile.from_data(data)
    path = tmp_path / "history.jsonl"
    if allowed:
        result = subject.run_probe(path, profile=profile, match=match)
        assert result.graph.query("SupplierOrderState")[0]["ordered_quantity"] == 2
    else:
        with pytest.raises(api.KnowledgeChangeRefusal) as caught:
            subject.run_probe(path, profile=profile, match=match)
        assert caught.value.reason.name == "TRANSITION_RULE_REFUSAL"
        assert (
            api.KnowledgeChangeHistory.reopen(path)
            .replay()
            .graph.query("SupplierOrderState")[0]["ordered_quantity"]
            == 1
        )


def test_earlier_structural_only_counterexample_keeps_its_original_result(tmp_path):
    assert (
        core_contract_probe.probe_event_replacement(tmp_path / "old.jsonl")["outcome"]
        == "ADMITTED"
    )


def test_repeated_restricted_inputs_reproduce_bytes(tmp_path):
    profile = subject.proposed_profile()
    first, second = tmp_path / "first.jsonl", tmp_path / "second.jsonl"
    subject.run_probe(first, profile=profile, match="EXACT")
    subject.run_probe(second, profile=profile, match="EXACT")
    assert first.read_bytes() == second.read_bytes()
