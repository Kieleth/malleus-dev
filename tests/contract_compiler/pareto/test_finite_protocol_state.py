"""Selected programs read actual pre-transaction state, never supplied state."""

from copy import deepcopy

import pytest

from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest
from research.action_history_contract_freeze.programs.lifecycle.test_prerequisites import (
    T0,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import (
    api,
    append,
    canonical,
    drafts,
    obj,
    operand,
    specimen,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _anchored_history,
    _evidence_anchor,
)


def setup(tmp_path):
    history = _anchored_history(tmp_path)[0]
    bundle, args = specimen()
    pair = bundle["transactions"]["register-pair"]["program"]
    bundle["profile"]["targets"]["observed"] = {
        "target": "PROTOCOL_INDEX",
        "storage_path": ["protocol", "observed"],
        "key_schemas": [{"type": "string"}],
        "value_schema": {"type": "string"},
    }
    pair["steps"].append(
        {
            "opcode": "SET_PROTOCOL_STATE",
            "target": "PROTOCOL_INDEX",
            "name": "observed",
            "keys": [
                operand("event", "1", "data", "records", "value", 0, "record", "id")
            ],
            "value": operand(
                "event", "1", "data", "records", "value", 0, "record", "id"
            ),
            "refusal": "BAD_OBSERVATION",
        }
    )
    indexes = obj(
        observed={
            "type": "array",
            "items": obj(
                keys={"type": "array", "items": {"type": "string"}},
                value={"type": "string"},
            ),
        }
    )
    indexes["required"] = []
    inspect = deepcopy(pair)
    inspect["name"] = "read-owner-state"
    inspect["introductions"] = []
    inspect["inputs"]["event"] = {
        "0": obj(
            header=pair["inputs"]["event"]["0"]["properties"]["header"],
            data=obj(identity={"type": "string", "format": "sha256"}),
            retained=obj(),
        )
    }
    inspect["inputs"]["current"]["state"] = obj(
        value=obj(
            protocol=indexes,
            action_acceptance_head={"type": "string", "format": "ledger-head"},
        )
    )
    inspect["steps"] = [
        {
            "opcode": "HASH",
            "recipe": "VALUE",
            "value": operand("current", "state", "value"),
            "result": "actual",
            "refusal": "BAD_STATE",
        },
        {
            "opcode": "REQUIRE_COMPARE",
            "comparison": "EQ",
            "value_kind": "DIGEST",
            "left": operand("result", "actual", "value"),
            "right": operand("event", "0", "data", "identity"),
            "refusal": "WRONG_CURRENT_STATE",
        },
    ]
    bundle["transactions"]["inspect"] = {
        "event_types": ["INSPECTED"],
        "program": inspect,
    }
    history.append_anchors(
        anchors=(_evidence_anchor("programs", canonical(bundle)),),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    base = history.replay()
    history.select_protocol_programs(
        record_id="programs",
        identity=content_digest(bundle),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
        event_id="select",
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    return history, args


def inspect(history, state, identifier):
    base = history.replay()
    return history.append_protocol_events(
        transaction="inspect",
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
        events=(
            {
                "event_id": identifier,
                "event_type": "INSPECTED",
                "actor_id": "actor:test",
                "transaction_time": T0,
                "data": {"identity": content_digest(state)},
                "retained": {},
            },
        ),
    )


def test_state_input_comes_from_prior_fold_and_is_recomputed_on_reopen(tmp_path):
    history, args = setup(tmp_path)
    initial = history.replay().protocol_replay.data["state"]
    inspect(history, initial, "inspect:initial")
    changed = append_pair(history, args)
    state = changed.protocol_replay.data["state"]
    assert state != initial
    after = inspect(history, state, "inspect:changed")
    assert after.protocol_replay.data["state"] == state
    assert KnowledgeChangeHistory.reopen(history.path).replay().receipt == after.receipt


@pytest.mark.parametrize("fault", ["stale", "invented"])
def test_state_claims_cannot_replace_actual_state(tmp_path, fault):
    history, args = setup(tmp_path)
    state = history.replay().protocol_replay.data["state"]
    append_pair(history, args)
    if fault == "invented":
        state["action_acceptance_head"] = content_digest("invented")
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal, match="WRONG_CURRENT_STATE"):
        inspect(history, state, "inspect:forged")
    assert history.path.read_bytes() == before


def append_pair(history, args):
    events = drafts(history, args)
    events[0]["transaction_time"] = events[1]["transaction_time"]
    assert events[1]["transaction_time"] == T0
    return append(history, events)
