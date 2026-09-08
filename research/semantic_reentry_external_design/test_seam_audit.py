"""Snapshot probes of existing seams, not an external-action implementation.

These tests describe Core 63a0565 and the unchanged landed consumer. They do
not make the default structural bundle an action profile or freeze future APIs.
All writes are ordinary Core fixture setup in pytest-owned temporary paths.
"""

import json

import pytest

import malleus.compiler as api
from research.semantic_reentry_protocol import consumer
from research.semantic_reentry_protocol.test_consumer import bundle
from research.semantic_reentry_protocol.test_prerequisites import (
    ACTOR,
    CORRECTION,
    SOURCE,
    TIME,
    canonical,
)


EFFECT_EVENTS = ("ACTION_DISPATCHED", "ACTION_EXECUTED", "OUTCOME_OBSERVED")


@pytest.mark.parametrize("event_type", EFFECT_EVENTS)
def test_default_machine_refuses_undeclared_effect_events(shop, event_type):
    history, path = shop
    replay = history.replay()
    before = path.read_bytes()
    result = api.execute_event(
        replay.partial_contract,
        replay.machine_state,
        canonical({"event_type": event_type, "payload": {}}),
    )
    assert result.receipt.outcome == "REFUSED"
    assert result.receipt.refusal_code == "UNKNOWN_EVENT"
    assert result.state == replay.machine_state
    assert path.read_bytes() == before
    assert history.replay().graph.state_digest() == replay.graph.state_digest()


@pytest.mark.parametrize("event_type", EFFECT_EVENTS)
def test_default_retention_is_not_an_effect_event_append_route(shop, event_type):
    history, path = shop
    before = path.read_bytes()
    with pytest.raises(api.KnowledgeChangeRefusal) as refusal:
        history.append_anchor(
            machine_event=canonical({"event_type": event_type, "payload": {}}),
            retained_bytes=b"{}",
            media_type="application/json",
            role="RETAINED_EVIDENCE",
            transaction_time=TIME,
            actor_id=ACTOR,
        )
    assert refusal.value.reason is api.KnowledgeChangeRefusalReason.MALFORMED_HISTORY
    assert "not declared as a retention event" in str(refusal.value)
    assert path.read_bytes() == before


def test_landed_consumer_does_not_claim_goal_to_action_support(shop):
    request = bundle(shop[0])
    contract = request["contract"]
    contract["input_kind"] = "GoalPredicate"
    contract["output_kind"] = "ActionProposal"
    with pytest.raises(consumer.ReentryRefusal) as refusal:
        consumer.ReentryContract.from_bytes(canonical(contract))
    assert refusal.value.reason is consumer.Reason.UNSUPPORTED_CONTRACT


def test_correction_fixture_is_not_an_external_effect_observation(shop):
    history, _ = shop
    attribution = json.loads((CORRECTION / "attribution.json").read_bytes())
    assert {"DEMAND_OR_SUPPLY_GAP", "ACTION_OR_EFFECT"} <= set(
        attribution["excluded_claims"]
    )
    rows = [
        json.loads(line)
        for line in history.replay().retained_bytes(SOURCE).splitlines()
    ]
    assert [row["event_id"] for row in rows] == ["e4", "e7"]
    assert [row["quantity"] for row in rows] == [1, 2]
    assert (
        history.replay().graph.query("SupplierOrderState", supplier_order_id="B")[0][
            "ordered_quantity"
        ]
        == 1
    )
