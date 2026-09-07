"""Real finite-instruction execution, still below owning-history admission."""

from copy import deepcopy
from hashlib import sha256
from importlib import import_module
import json

import pytest

from malleus.ledger import GENESIS, canonical_json, content_digest, record_hash
from research.action_history_contract_freeze.programs.lifecycle.test_prerequisites import (
    HERE,
    T0,
    compiled,
    packet,
    specimen,
)
from research.action_history_contract_freeze.programs.test_packet_validator import (
    obj,
    operand,
    profile,
    specimen as neutral_program,
)


def api():
    return import_module("research.action_history_contract_freeze.programs.executor")


def empty_state():
    return {"protocol": {}, "action_acceptance_head": GENESIS}


def arguments(program, declaration, inputs, *, applied=None, state=None):
    return {
        "program": program,
        "profile": declaration,
        "instruction_schema": json.loads(
            (HERE.parents[1] / "instructions.schema.json").read_bytes()
        ),
        "inputs": inputs,
        "applied_records": {} if applied is None else applied,
        "state": empty_state() if state is None else state,
        "record_contract_bytes": compiled().artifact_bytes,
    }


def run(args):
    return api().execute_program(**args)


def neutral():
    identity = content_digest({"id": "context:1"})
    action = content_digest("action-head")
    return arguments(
        neutral_program(),
        profile(),
        {
            "event": {"context": {"identity": identity}},
            "original": {"action": {"value": action}},
            "current": {"action": {"value": action}},
            "artifact": {"context": {"value": {"id": "context:1"}}},
        },
    )


def grant():
    definition = packet("grant")
    value = specimen("grant")
    return arguments(
        definition["program"],
        definition["profile"],
        {
            "event": {
                "records": {
                    "value": [{"record_type": "AuthorityGrant", "record": value}]
                },
                "header": {
                    "event_id": value["generation_event_id"],
                    "transaction_time": T0,
                    "actor_id": "actor:registrar",
                },
                "dependencies": {"value": []},
            },
            "artifact": {
                "record_contract": {
                    "value": {
                        "contract_identity": "sha256:"
                        + sha256(compiled().artifact_bytes).hexdigest(),
                        "record_type": "AuthorityGrant",
                    }
                },
                "constants": {"registrar_role": "registrar"},
            },
        },
    )


def test_real_execution_is_deterministic_immutable_and_stages_keyed_state():
    args = neutral()
    before = deepcopy(args)
    first, second = run(args), run(args)
    assert first.canonical_bytes == second.canonical_bytes
    assert args == before
    result = first.data
    identity = args["inputs"]["event"]["context"]["identity"]
    assert result["state"]["protocol"]["context-identities"] == [
        {"keys": [identity], "value": identity}
    ]
    assert result["state"]["action_acceptance_head"] == GENESIS
    assert result["introductions"] == []
    assert result["runtime_executed"] is True
    assert result["history_authenticated"] is False
    result["state"]["protocol"].clear()
    assert first.canonical_bytes == second.canonical_bytes


def test_late_refusal_discards_already_staged_write():
    args = neutral()
    args["program"]["steps"].append(deepcopy(args["program"]["steps"][2]))
    args["program"]["steps"][-1]["comparison"] = "NE"
    before = deepcopy(args)
    with pytest.raises(api().ExecutionRefusal) as caught:
        run(args)
    assert caught.value.reason == "STALE_ACTION_CONTEXT"
    assert caught.value.step == 4
    assert args == before


@pytest.mark.parametrize(
    "fault",
    ["missing", "extra", "wrong_type", "bool_index", "unknown_opcode", "callback"],
)
def test_closed_runtime_inputs_and_programs_refuse_without_mutation(fault):
    args = neutral()
    if fault == "missing":
        del args["inputs"]["event"]["context"]["identity"]
    elif fault == "extra":
        args["inputs"]["event"]["outcome"] = "SATISFIED"
    elif fault == "wrong_type":
        args["inputs"]["event"]["context"]["identity"] = 1
    elif fault == "bool_index":
        args["program"]["steps"][0]["value"]["path"] = [True]
    elif fault == "unknown_opcode":
        args["program"]["steps"][0]["opcode"] = "CALL_PYTHON"
    else:
        args["program"]["steps"][0]["callback"] = "os.system"
    before = deepcopy(args)
    with pytest.raises(api().ExecutionRefusal):
        run(args)
    assert args == before


def test_complete_grant_program_executes_and_introduces_real_typed_record():
    args = grant()
    before = deepcopy(args)
    result = run(args).data
    assert result["introductions"] == args["inputs"]["event"]["records"]["value"]
    assert args == before


@pytest.mark.parametrize(
    "fault,reason",
    [
        ("hash", "RECORD_HASH_MISMATCH"),
        ("grantor", "WRONG_GRANTOR"),
        ("interval", "INVALID_GRANT_INTERVAL"),
        ("actor", "RESPONSIBLE_ACTOR_ID_MISMATCH"),
        ("order", "NONCANONICAL_IDS_OR_PERMISSIONS"),
        ("duplicate", "NONCANONICAL_IDS_OR_PERMISSIONS"),
        ("contract", "INVALID_RECORD"),
        ("reused", "DUPLICATE_RECORD"),
    ],
)
def test_grant_program_refuses_real_invalid_values(fault, reason):
    args = grant()
    value = args["inputs"]["event"]["records"]["value"][0]["record"]
    if fault == "hash":
        value["scope_record_id"] = "changed"
    elif fault == "grantor":
        value["grantor_actor_id"] = "someone-else"
    elif fault == "interval":
        value["grant_valid_to"] = value["grant_valid_from"]
    elif fault == "actor":
        args["inputs"]["event"]["header"]["actor_id"] = "someone-else"
    elif fault == "order":
        value["permitted_action_types"].reverse()
    elif fault == "duplicate":
        value["permitted_action_types"] *= 2
    elif fault == "contract":
        args["inputs"]["artifact"]["record_contract"]["value"]["contract_identity"] = (
            content_digest("wrong")
        )
    else:
        args["state"]["protocol"]["global_ids"] = [
            {"keys": [value["id"]], "value": value["content_hash"]}
        ]
    if fault != "hash":
        value["content_hash"] = record_hash("AuthorityGrant", value)
    before = deepcopy(args)
    with pytest.raises(api().ExecutionRefusal) as caught:
        run(args)
    assert caught.value.reason == reason
    assert args == before


@pytest.mark.parametrize(
    "value,valid",
    [("AMEND", True), (" AMEND ", True), ("", False), (" \t\u2003", False)],
)
def test_explicit_nonblank_constraint_has_no_regex_or_normalization(value, valid):
    args = grant()
    shape = args["program"]["inputs"]["event"]["records"]["properties"]["value"][
        "items"
    ]["properties"]["record"]
    shape["properties"]["permitted_action_types"]["items"]["format"] = "nonblank"
    record = args["inputs"]["event"]["records"]["value"][0]["record"]
    record["permitted_action_types"] = [value]
    record["content_hash"] = record_hash("AuthorityGrant", record)
    if valid:
        assert run(args).data["introductions"][0]["record"][
            "permitted_action_types"
        ] == [value]
    else:
        with pytest.raises(api().ExecutionRefusal, match="INPUT_SHAPE"):
            run(args)


def test_unknown_runtime_format_cannot_silently_pass():
    args = neutral()
    args["program"]["inputs"]["artifact"]["context"]["properties"]["value"][
        "properties"
    ]["id"]["format"] = "invented-constraint"
    with pytest.raises(api().ExecutionRefusal, match="UNSUPPORTED_FORMAT"):
        run(args)


@pytest.mark.parametrize(
    "values,member,valid",
    [
        (["READ", "AMEND"], "AMEND", True),
        ([], "AMEND", False),
        (["READ"], "AMEND", False),
    ],
)
def test_membership_executes_exact_values(values, member, valid):
    program = {
        "name": "membership",
        "inputs": {
            "event": {
                "payload": obj(
                    value={"type": "string"},
                    members={"type": "array", "items": {"type": "string"}},
                )
            }
        },
        "required_capabilities": [],
        "introductions": [],
        "steps": [
            {
                "opcode": "REQUIRE_MEMBER",
                "value_kind": "STRING",
                "value": operand("event", "payload", "value"),
                "members": operand("event", "payload", "members"),
                "refusal": "NOT_PERMITTED",
            }
        ],
    }
    args = arguments(
        program,
        {"targets": {}, "capabilities": []},
        {"event": {"payload": {"value": member, "members": values}}},
    )
    if valid:
        assert run(args).data["state"] == empty_state()
    else:
        with pytest.raises(api().ExecutionRefusal, match="NOT_PERMITTED"):
            run(args)


def test_runtime_has_no_io_or_callable_executor_hook(monkeypatch):
    args = neutral()
    runtime = api()

    # Import/load setup is outside the pure invocation. Inputs already contain bytes.
    def forbidden(*args, **kwargs):
        raise AssertionError("runtime attempted file I/O")

    monkeypatch.setattr("builtins.open", forbidden)
    monkeypatch.setattr("pathlib.Path.open", forbidden)
    result = runtime.execute_program(**args)
    assert canonical_json(result.data).encode() == result.canonical_bytes
