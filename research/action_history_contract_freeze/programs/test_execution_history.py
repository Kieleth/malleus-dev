"""A terminal receipt follows dispatch, retains bytes, and proves no observation."""

from research.action_history_contract_freeze.programs.fixture_episode import FIRST

from copy import deepcopy
from importlib import import_module

import pytest

from malleus.assent import make_record
from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs import (
    test_dispatch_history as dispatching,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    reopen,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api, canonical


TIME = "2026-09-07T00:20:00Z"


def dispatched_prefix(directory, bundle):
    content, _ = dispatching.authorized_prefix(directory, bundle)
    path = directory / "dispatched"
    path.mkdir()
    history = reopen(path, content)
    dispatching.dispatch(history, dispatching.event(history))
    return history.path.read_bytes()


@pytest.fixture(scope="module")
def dispatched(tmp_path_factory):
    module = import_module(
        "research.action_history_contract_freeze.programs.execution_bundle"
    )
    from research.action_history_contract_freeze.programs.dispatch_bundle import (
        add_dispatch,
    )

    return dispatched_prefix(
        tmp_path_factory.mktemp("execution-prefix"),
        module.add_execution(add_dispatch(dispatching.authorization.build_bundle())),
    )


def event(history, status="SUCCEEDED", episode=FIRST):
    dispatch = history.replay().protocol_replay.data["records"][
        episode.id("dispatch:1")
    ]["record"]
    content = canonical(
        {"status": status, "scope": "synthetic terminal-receipt conformance"}
    )
    value = make_record(
        "ActionExecution",
        id=episode.id("execution:1"),
        event_id=episode.id("event:execution"),
        generated_at=episode.time(TIME),
        actor_id="actor:executor",
        role="executor",
        source_record_ids=[dispatch["id"]],
        dispatch_id=dispatch["id"],
        dispatch_hash=dispatch["content_hash"],
        executor_id="actor:executor",
        execution_started_at=episode.time(dispatching.TIME),
        execution_ended_at=episode.time(TIME),
        execution_status=status,
        execution_result_hash=api().digest(content),
    )
    return {
        "event_id": episode.id("event:execution"),
        "event_type": "ACTION_EXECUTED",
        "actor_id": value["responsible_actor_id"],
        "transaction_time": episode.time(TIME),
        "data": {
            "records": {"value": [{"record_type": "ActionExecution", "record": value}]},
            "dependencies": {"value": deepcopy(value["source_record_ids"])},
        },
        "retained": {
            "result": {
                "record_id": value["id"],
                "content": content,
                "media_type": "application/json",
                "role": "RETAINED_EVIDENCE",
                "encoding": "BYTES",
            }
        },
    }


def execute(history, draft):
    replay = history.replay()
    return history.append_protocol_events(
        transaction="execution",
        events=(draft,),
        expected_head=replay.ledger_head,
        expected_count=replay.ledger_event_count,
    )


@pytest.mark.parametrize("status", ["SUCCEEDED", "FAILED", "ABORTED"])
def test_terminal_receipt_retains_exact_result_without_observation_or_knowledge(
    tmp_path, dispatched, status
):
    history = reopen(tmp_path, dispatched)
    before = history.replay()
    after = execute(history, event(history, status))
    assert after.protocol_replay.data["state"]["protocol"]["execution_by_dispatch"] == [
        {"keys": ["dispatch:1"], "value": "execution:1"}
    ]
    assert (
        "observation_by_execution_contract"
        not in after.protocol_replay.data["state"]["protocol"]
    )
    assert after.graph.export_records() == before.graph.export_records()
    assert after.change_sets == before.change_sets
    assert after.acceptance_head == before.acceptance_head
    reopened = KnowledgeChangeHistory.reopen(history.path)
    assert reopened.replay().receipt == after.receipt
    record = after.protocol_replay.data["records"]["execution:1"]["record"]
    assert (
        api().digest(reopened.replay().retained_bytes(record["id"]))
        == record["execution_result_hash"]
    )


@pytest.mark.parametrize(
    "fault",
    [
        "dispatch",
        "executor",
        "start",
        "end",
        "status",
        "result",
        "retention",
        "duplicate",
    ],
)
def test_execution_refuses_misbound_receipt_before_append(tmp_path, dispatched, fault):
    history = reopen(tmp_path, dispatched)
    draft = event(history)
    value = draft["data"]["records"]["value"][0]["record"]
    if fault == "dispatch":
        value["dispatch_hash"] = content_digest("wrong")
    elif fault == "executor":
        value["executor_id"] = value["responsible_actor_id"] = draft["actor_id"] = (
            "actor:other"
        )
    elif fault == "start":
        value["execution_started_at"] = "2026-09-07T00:09:00Z"
    elif fault == "end":
        value["execution_ended_at"] = value["execution_started_at"]
    elif fault == "status":
        value["execution_status"] = "PENDING"
    elif fault == "result":
        value["execution_result_hash"] = content_digest("other bytes")
    elif fault == "retention":
        draft["retained"]["result"]["record_id"] = "execution:other"
    else:
        execute(history, deepcopy(draft))
        value["id"] = draft["retained"]["result"]["record_id"] = "execution:duplicate"
        value["generation_event_id"] = draft["event_id"] = "event:execution:duplicate"
    value["content_hash"] = record_hash("ActionExecution", value)
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal):
        execute(history, draft)
    assert history.path.read_bytes() == before
