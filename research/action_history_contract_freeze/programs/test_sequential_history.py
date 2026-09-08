"""Two actions, one actual Shop ledger, no injected outcomes or replay state."""

from copy import deepcopy
from importlib import import_module

import pytest

from malleus.compiler import KnowledgeChangeHistory
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
        replay.record_history["supplier-order-state:B:e4"]["superseded_by"]
        == "supplier-order-state:B:e7"
    )
    assert replay.graph.state_digest() == metadata["corrected_graph"]
    assert states["first_observed"] != states["corrected"]


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
    fixture.correct(history)
    before = history.path.read_bytes()
    with pytest.raises(ProtocolProgramRefusal):
        fixture.proposals.submit(history, candidate)
    assert history.path.read_bytes() == before


@pytest.mark.parametrize("stage", ["type", "authorization", "dispatch", "observation"])
def test_first_action_output_is_not_a_successor_credential(tmp_path, sequence, stage):
    fixture, states, metadata = sequence
    history = reopen(tmp_path, states["second_proposed"])
    transaction, draft = metadata["first_events"][stage]
    before = history.path.read_bytes()
    base = history.replay()
    with pytest.raises(ProtocolProgramRefusal):
        history.append_protocol_events(
            transaction=transaction,
            events=(deepcopy(draft),),
            expected_head=base.ledger_head,
            expected_count=base.ledger_event_count,
        )
    assert history.path.read_bytes() == before
