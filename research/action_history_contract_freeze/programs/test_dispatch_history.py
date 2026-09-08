"""Actual permission precedes dispatch eligibility in the same Shop history."""

from copy import deepcopy
from importlib import import_module
import json

import pytest

from malleus.assent import make_record
from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs import (
    test_authorization_history as authorization,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    reopen,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api


TIME = "2026-09-07T00:10:00Z"


def authorized_prefix(directory, bundle):
    directory.mkdir(exist_ok=True)
    base = directory / "base"
    base.mkdir()
    accepted = authorization.authority.current.accepted_prefix(base, bundle)
    assessed_dir = directory / "assessed"
    assessed_dir.mkdir()
    content, request = authorization.assessed_prefix(
        assessed_dir, accepted, "AUTHORIZE"
    )
    history = KnowledgeChangeHistory.reopen(assessed_dir / "history.jsonl")
    draft, result = authorization.event(history, request)
    authorization.authorize(history, draft, result.verdict)
    return history.path.read_bytes(), content


@pytest.fixture(scope="module")
def authorized(tmp_path_factory):
    extend = import_module(
        "research.action_history_contract_freeze.programs.dispatch_bundle"
    ).add_dispatch
    return authorized_prefix(
        tmp_path_factory.mktemp("dispatch-prefix"), extend(authorization.build_bundle())
    )


def event(history):
    replay = history.replay()
    records = {
        k: v["record"] for k, v in replay.protocol_replay.data["records"].items()
    }
    action, permission, context = (
        records["action:1"],
        records["authorization:1"],
        records["source:current-context"],
    )
    value = make_record(
        "ActionDispatch",
        id="dispatch:1",
        event_id="event:dispatch",
        generated_at=TIME,
        actor_id="actor:dispatcher",
        role="dispatcher",
        source_record_ids=[action["id"], permission["id"]],
        action_proposal_id=action["id"],
        action_content_hash=action["content_hash"],
        authorization_decision_id=permission["id"],
        authorization_decision_hash=permission["content_hash"],
        executor_id="actor:executor",
        dispatch_adapter_id="adopter:declared-adapter:v1",
        base_acceptance_head=replay.protocol_replay.data["state"][
            "action_acceptance_head"
        ],
        dispatched_at=TIME,
    )
    return {
        "event_id": "event:dispatch",
        "event_type": "ACTION_DISPATCHED",
        "actor_id": value["responsible_actor_id"],
        "transaction_time": TIME,
        "data": {
            "records": {"value": [{"record_type": "ActionDispatch", "record": value}]},
            "dependencies": {"value": deepcopy(value["source_record_ids"])},
            "context": {
                "id": context["id"],
                "record_hash": context["content_hash"],
                "value": json.loads(history.retained_bytes(context["id"])),
            },
        },
        "retained": {},
    }


def dispatch(history, draft):
    replay = history.replay()
    return history.append_protocol_events(
        transaction="dispatch",
        events=(draft,),
        expected_head=replay.ledger_head,
        expected_count=replay.ledger_event_count,
    )


def test_actual_authorization_allows_dispatch_without_effect_or_domain_write(
    tmp_path, authorized
):
    history = reopen(tmp_path, authorized[0])
    before = history.replay()
    after = dispatch(history, event(history))
    assert after.protocol_replay.data["state"]["protocol"]["dispatch_by_action"] == [
        {"keys": ["action:1"], "value": "dispatch:1"}
    ]
    assert (
        "execution_by_dispatch" not in after.protocol_replay.data["state"]["protocol"]
    )
    assert after.graph.export_records() == before.graph.export_records()
    assert after.change_sets == before.change_sets
    assert after.acceptance_head == before.acceptance_head
    assert after.materialization_head == before.materialization_head
    assert (
        after.protocol_replay.data["state"]["action_acceptance_head"]
        == before.protocol_replay.data["state"]["action_acceptance_head"]
    )
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == after.receipt


@pytest.mark.parametrize(
    "fault",
    [
        "permission",
        "executor",
        "head",
        "context",
        "expiry",
        "adapter",
        "provenance",
        "duplicate",
    ],
)
def test_dispatch_refuses_missing_permission_and_misbinding_atomically(
    tmp_path, authorized, fault
):
    history = reopen(tmp_path, authorized[0])
    draft = event(history)
    value = draft["data"]["records"]["value"][0]["record"]
    if fault == "permission":
        # The same draft is ineligible before the permission event exists.
        history.path.write_bytes(authorized[1])
        history = KnowledgeChangeHistory.reopen(history.path)
    elif fault == "executor":
        value["executor_id"] = "actor:other"
    elif fault == "head":
        value["base_acceptance_head"] = content_digest("stale")
    elif fault == "context":
        draft["data"]["context"]["value"]["domain"]["accepted_graph_digest"] = (
            content_digest("other")
        )
    elif fault == "expiry":
        value["dispatched_at"] = value["generated_at"] = draft["transaction_time"] = (
            "2026-09-07T01:00:00Z"
        )
    elif fault == "adapter":
        value["dispatch_adapter_id"] = " "
    elif fault == "provenance":
        draft["data"]["dependencies"]["value"] = []
    else:
        dispatch(history, deepcopy(draft))
        value["id"] = "dispatch:duplicate"
        value["generation_event_id"] = draft["event_id"] = "event:duplicate-dispatch"
    value["content_hash"] = record_hash("ActionDispatch", value)
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal):
        dispatch(history, draft)
    assert history.path.read_bytes() == before
