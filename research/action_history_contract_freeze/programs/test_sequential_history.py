"""Two actions, one actual Shop ledger, no injected outcomes or replay state."""

from copy import deepcopy
from importlib import import_module
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import record_hash
from malleus._contract_pipeline.protocol_runtime import ProtocolProgramRefusal
from research.action_history_contract_freeze.programs.fixture_episode import (
    FIRST,
    FixtureEpisode,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    reopen,
)


SECOND = FixtureEpisode("2", 60)


@pytest.fixture(scope="module")
def sequence(tmp_path_factory):
    fixture = import_module(
        "research.action_history_contract_freeze.programs.sequential_fixture"
    )
    return fixture.run_sequence(tmp_path_factory.mktemp("sequential-shop"))


def test_two_complete_actions_survive_the_intervening_shop_correction(sequence):
    fixture, states, metadata = sequence
    replay = KnowledgeChangeHistory.reopen(metadata["path"]).replay()
    records = replay.protocol_replay.data["records"]
    for episode in (FIRST, SECOND):
        for name in (
            "action:1",
            "decision:1",
            "authorization:1",
            "dispatch:1",
            "execution:1",
            "observation:1",
        ):
            assert episode.id(name) in records
        assert (
            records[episode.id("execution:1")]["record"]["execution_status"]
            == "SUCCEEDED"
        )
        assert (
            records[episode.id("observation:1")]["record"]["observation_result"]
            == "CONFIRMED"
        )
    protocol = replay.protocol_replay.data["state"]["protocol"]
    assert len(protocol["type_assessments"]) == 4
    assert len(protocol["authority_assessments"]) == 4
    assert len(protocol["dispatch_by_action"]) == 2
    assert protocol["episode_phase"] == [{"keys": ["CURRENT"], "value": "READY"}]
    assert len(replay.change_sets) == 5
    assert replay.graph.get_node("supplier-order-state:B:e7")["ordered_quantity"] == 2
    assert (
        replay.record_history["supplier-order-state:B:e4"].superseded_by
        == "supplier-order-state:B:e7"
    )
    assert replay.graph.state_digest() == metadata["corrected_graph"]
    assert states["first_observed"] != states["corrected"]


def test_fresh_process_replays_without_fixture_or_check_producer_imports(sequence):
    _, _, metadata = sequence
    replay = KnowledgeChangeHistory.reopen(metadata["path"]).replay()
    script = """
import importlib.abc, json, sys
class NoAuthoring(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'research', 'tests'}:
            raise AssertionError('authoring or check producer imported: ' + fullname)
sys.meta_path.insert(0, NoAuthoring())
from malleus.compiler import KnowledgeChangeHistory
r = KnowledgeChangeHistory.reopen(sys.argv[1]).replay()
print(json.dumps([r.ledger_head, r.ledger_event_count, r.graph.state_digest(), r.protocol_replay.identity]))
"""
    root = Path(__file__).resolve().parents[3]
    result = subprocess.run(
        [sys.executable, "-c", script, str(metadata["path"])],
        cwd=metadata["path"].parent,
        env={
            **os.environ,
            "PYTHONPATH": str(root / "src"),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(result.stdout) == [
        replay.ledger_head,
        replay.ledger_event_count,
        replay.graph.state_digest(),
        replay.protocol_replay.identity,
    ]


def test_fresh_observation_of_old_execution_cannot_unlock_the_active_action(
    tmp_path, sequence
):
    fixture, states, metadata = sequence
    history = reopen(tmp_path, states["second_proposed"])
    extra = FixtureEpisode("different-outcome", 60)
    fixture.observations.observer_inputs(history, episode=extra)
    event = fixture.observations.event(history, episode=FIRST)
    value = event["data"]["records"]["value"][0]["record"]
    contract = history.replay().protocol_replay.data["records"][
        extra.id("outcome-contract:1")
    ]["record"]
    value["id"] = "observation:old-execution:new-contract"
    event["event_id"] = value["generation_event_id"] = (
        "event:old-execution:new-contract"
    )
    event["transaction_time"] = value["generated_at"] = value["observed_at"] = (
        extra.time(fixture.observations.TIME)
    )
    value["outcome_contract_id"] = contract["id"]
    value["outcome_contract_hash"] = contract["content_hash"]
    value["source_record_ids"] = [
        value["execution_id"],
        contract["id"],
        value["observed_source_artifact_id"],
    ]
    event["data"]["dependencies"]["value"] = list(value["source_record_ids"])
    value["content_hash"] = record_hash("OutcomeObservation", value)
    before = history.path.read_bytes()
    with pytest.raises(ProtocolProgramRefusal, match="OBSERVATION_NOT_CURRENT_ACTION"):
        fixture.append(history, "observation", event)
    assert history.path.read_bytes() == before


def test_successor_before_independent_observation_preserves_exact_bytes(
    tmp_path, sequence
):
    fixture, states, metadata = sequence
    history = reopen(tmp_path, states["first_executed"])
    candidate = fixture.proposal(history, metadata, SECOND)
    before = history.path.read_bytes()
    with pytest.raises(ProtocolProgramRefusal, match="PREVIOUS_ACTION_NOT_OBSERVED"):
        fixture.proposals.submit(history, candidate)
    assert history.path.read_bytes() == before


def test_misbound_payload_preserves_context_and_proposal_atomicity(tmp_path, sequence):
    fixture, states, metadata = sequence
    history = reopen(tmp_path, states["corrected"])
    candidate = fixture.proposal(history, metadata, SECOND, bad_payload=True)
    before = history.path.read_bytes()
    with pytest.raises(ProtocolProgramRefusal, match="ACTION_PAYLOAD_BYTES_MISMATCH"):
        fixture.proposals.submit(history, candidate)
    assert history.path.read_bytes() == before


def test_pre_correction_context_cannot_start_the_successor(tmp_path, sequence):
    fixture, states, metadata = sequence
    history = reopen(tmp_path, states["first_observed"])
    candidate = fixture.proposal(history, metadata, SECOND)
    fixture.correct(history, when="2026-09-07T01:00:00Z")
    before = history.path.read_bytes()
    with pytest.raises(ProtocolProgramRefusal):
        fixture.proposals.submit(history, candidate)
    assert history.path.read_bytes() == before


@pytest.mark.parametrize(
    "stage", ["type", "authority", "authorization", "dispatch", "observation"]
)
def test_first_action_output_is_not_a_successor_credential(tmp_path, sequence, stage):
    fixture, states, metadata = sequence
    checkpoint = {
        "type": "second_proposed",
        "authority": "2:before-authorization",
        "authorization": "2:before-authorization",
        "dispatch": "2:authorized",
        "observation": "second_executed",
    }[stage]
    history = reopen(tmp_path, states[checkpoint])
    transaction, draft = metadata["first_events"][stage]
    draft = deepcopy(draft)
    # Fresh event/record IDs prevent duplicate-ID guards from concealing a
    # missing action-binding check. The retained first-action references stay.
    draft["event_id"] += ":fresh-forgery"
    draft["transaction_time"] = "2026-09-07T01:30:00Z"

    def fresh(value):
        if type(value) is dict and set(value) == {"record_type", "record"}:
            record = value["record"]
            record["id"] += ":fresh-forgery"
            record["generation_event_id"] = draft["event_id"]
            record["generated_at"] = draft["transaction_time"]
            for field in ("transition_time", "dispatched_at", "observed_at"):
                if field in record:
                    record[field] = draft["transaction_time"]
            record["content_hash"] = record_hash(value["record_type"], record)
        elif type(value) is dict:
            for child in value.values():
                fresh(child)
        elif type(value) is list:
            for child in value:
                fresh(child)

    fresh(draft["data"])
    before = history.path.read_bytes()
    base = history.replay()
    with pytest.raises(ProtocolProgramRefusal):
        history.append_protocol_events(
            transaction=transaction,
            events=(draft,),
            expected_head=base.ledger_head,
            expected_count=base.ledger_event_count,
        )
    assert history.path.read_bytes() == before
