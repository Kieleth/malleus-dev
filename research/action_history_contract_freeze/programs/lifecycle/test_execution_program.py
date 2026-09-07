"""Static candidate checks; no action event executes or is persisted."""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from malleus.assent import make_record
from malleus.ledger import content_digest
from research.action_history_contract_freeze.programs.packet_validator import (
    FORMATS,
    PacketRefusal,
    validate_program,
)
from tests.contract_compiler.pareto.test_assent_contract_compatibility import _compile


HERE = Path(__file__).parent


def packet():
    return json.loads((HERE / "execution.json").read_bytes())


def check(program):
    value = packet()
    schema = json.loads((HERE.parents[1] / "instructions.schema.json").read_bytes())
    return validate_program(
        program, instruction_schema=schema, profile=value["profile"]
    )


def prefix():
    value = packet()["program"]
    assert value["steps"][-1]["opcode"] == "SET_PROTOCOL_STATE"
    value["steps"] = value["steps"][:-1]
    return value


def test_execution_record_reference_prefix_is_static_only_and_unchanged():
    value = prefix()
    before = deepcopy(value)
    assert check(value) == {
        "status": "STATIC_VALID",
        "steps": 17,
        "runtime_executed": False,
    }
    assert value == before


def test_full_candidate_is_statically_valid_with_the_approved_key():
    value = packet()["program"]
    before = deepcopy(value)
    assert check(value) == {
        "status": "STATIC_VALID",
        "steps": 18,
        "runtime_executed": False,
    }
    assert value == before
    effect = value["steps"][-1]
    assert effect["keys"] == [
        {
            "root": "event",
            "name": "records",
            "path": ["value", 0, "record", "dispatch_id"],
        }
    ]
    assert effect["value"] == {
        "root": "event",
        "name": "records",
        "path": ["value", 0, "record", "id"],
    }
    assert packet()["status"] == "STATIC_VALID_PARTIAL"
    assert packet()["runtime_executed"] is False


def test_receipt_index_write_cannot_regress_to_an_inferred_key():
    value = packet()["program"]
    del value["steps"][-1]["keys"]
    with pytest.raises(PacketRefusal) as caught:
        check(value)
    assert caught.value.reason == "INSTRUCTION_SHAPE"


def test_every_execution_preflight_binding_is_explicit_in_the_retained_program():
    steps = prefix()["steps"]
    assert [step["refusal"] for step in steps] == [
        "INVALID_EXECUTION_RECORD",
        "INVALID_EXECUTION_HASH_INPUT",
        "EXECUTION_HASH_MISMATCH",
        "GENERATION_EVENT_MISMATCH",
        "GENERATION_TIME_MISMATCH",
        "RESPONSIBLE_ACTOR_MISMATCH",
        "EXECUTOR_MUST_RECORD",
        "EXECUTOR_ROLE_REQUIRED",
        "EXECUTION_INTERVAL_INVALID",
        "EXECUTION_END_NOT_EVENT_TIME",
        "DISPATCH_REFERENCE_INVALID",
        "DISPATCH_NOT_APPLIED",
        "DISPATCH_EXECUTOR_MISMATCH",
        "EXECUTION_BEFORE_DISPATCH",
        "REQUIRED_DISPATCH_SOURCE_MISSING",
        "DUPLICATE_EXECUTION",
        "INVALID_INTRODUCTION",
    ]
    assert steps[0]["record"] == steps[1]["value"]
    assert steps[10]["scope"] == "APPLIED"
    assert steps[15]["key_paths"] == [["record", "dispatch_id"]]
    assert steps[15]["target_index"] == "execution_by_dispatch"
    assert not any(
        step["target"] == "ACTION_ACCEPTANCE_HEAD" for step in steps if "target" in step
    )


def test_record_shapes_match_real_compiled_assent_without_dropping_fields():
    value = packet()
    digest = content_digest({"purpose": "record-shape fixture, not an applied object"})
    dispatch = make_record(
        "ActionDispatch",
        id="dispatch:1",
        event_id="event:dispatch",
        generated_at="2026-09-07T00:00:00Z",
        actor_id="actor:dispatcher",
        role="dispatcher",
        source_record_ids=["action:1", "authorization:1"],
        action_proposal_id="action:1",
        action_content_hash=digest,
        authorization_decision_id="authorization:1",
        authorization_decision_hash=digest,
        executor_id="actor:executor",
        dispatch_adapter_id="adapter:fixture",
        base_acceptance_head=digest,
        dispatched_at="2026-09-07T00:00:00Z",
    )
    execution = make_record(
        "ActionExecution",
        id="execution:1",
        event_id="event:execution",
        generated_at="2026-09-07T00:00:02Z",
        actor_id="actor:executor",
        role="executor",
        source_record_ids=[dispatch["id"]],
        dispatch_id=dispatch["id"],
        dispatch_hash=dispatch["content_hash"],
        executor_id="actor:executor",
        execution_started_at="2026-09-07T00:00:01Z",
        execution_ended_at="2026-09-07T00:00:02Z",
        execution_status="FAILED",
        execution_result_hash=digest,
    )
    compiled = _compile().view
    assert compiled.validate_instance("ActionDispatch", dispatch) == []
    assert compiled.validate_instance("ActionExecution", execution) == []
    record_schema = value["program"]["inputs"]["event"]["records"]
    Draft202012Validator(record_schema, format_checker=FORMATS).validate(
        {"value": [{"record_type": "ActionExecution", "record": execution}]}
    )
    dispatch_schema = value["profile"]["record_schemas"]["ActionDispatch"]
    Draft202012Validator(dispatch_schema, format_checker=FORMATS).validate(dispatch)
    assert set(execution) == set(
        record_schema["properties"]["value"]["items"]["properties"]["record"][
            "properties"
        ]
    )
    assert set(dispatch) == set(dispatch_schema["properties"])
    assert set(
        record_schema["properties"]["value"]["items"]["properties"]["record"][
            "properties"
        ]["execution_status"]["enum"]
    ) == compiled.get_enum_values("ExecutionStatus")


def test_a_wrong_dispatch_time_type_cannot_pass_cross_record_comparison():
    value = packet()
    value["profile"]["record_schemas"]["ActionDispatch"]["properties"][
        "dispatched_at"
    ] = {"type": "boolean"}
    schema = json.loads((HERE.parents[1] / "instructions.schema.json").read_bytes())
    with pytest.raises(PacketRefusal) as caught:
        validate_program(prefix(), instruction_schema=schema, profile=value["profile"])
    assert caught.value.reason == "OPERAND_TYPE"
