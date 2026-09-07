"""Approved instruction definition checks, not execution conformance."""

from copy import deepcopy
import json

from jsonschema import Draft202012Validator
import pytest

from research.action_history_contract_freeze.programs.test_packet_validator import (
    HERE,
    api,
    obj,
    operand,
    profile,
    validate,
)


def instruction():
    return {
        "opcode": "REQUIRE_MEMBER",
        "value": operand("applied_record", "action", "record", "action_type"),
        "members": operand(
            "applied_record", "grant", "record", "permitted_action_types"
        ),
        "value_kind": "STRING",
        "refusal": "ACTION_TYPE_OUTSIDE_GRANT",
    }


def program():
    return {
        "name": "action-type-membership-fragment",
        "inputs": {
            "applied_record": {
                "action": obj(record=obj(action_type={"type": "string"})),
                "grant": obj(
                    record=obj(
                        permitted_action_types={
                            "type": "array",
                            "items": {"type": "string"},
                        }
                    )
                ),
            }
        },
        "required_capabilities": [],
        "introductions": [],
        "steps": [instruction()],
    }


def test_membership_shape_is_closed_and_does_not_overload_compare():
    schema = json.loads((HERE.parent / "instructions.schema.json").read_bytes())
    validator = Draft202012Validator(schema)
    value = instruction()
    validator.validate(value)
    for field in value:
        missing = deepcopy(value)
        del missing[field]
        assert not validator.is_valid(missing), field
    for field in ("result", "target", "callback", "comparison"):
        assert not validator.is_valid({**value, field: "unused"})
    assert not validator.is_valid({**value, "value_kind": "INTEGER"})
    prior = json.loads((HERE / "missing-membership.json").read_bytes())
    assert not validator.is_valid(prior["instruction_attempt"])


def test_membership_static_program_accepts_real_field_paths_without_execution():
    value = program()
    before = deepcopy(value)
    assert validate(value) == {
        "status": "STATIC_VALID",
        "steps": 1,
        "runtime_executed": False,
    }
    assert value == before


@pytest.mark.parametrize(
    ("role", "field", "replacement", "reason"),
    [
        ("action", "action_type", {"type": "integer"}, "OPERAND_TYPE"),
        ("action", "action_type", {"type": "boolean"}, "OPERAND_TYPE"),
        ("grant", "permitted_action_types", {"type": "string"}, "OPERAND_TYPE"),
        ("grant", "permitted_action_types", {"type": "array"}, "UNRESOLVED_PATH"),
        (
            "grant",
            "permitted_action_types",
            {"type": "array", "items": {"type": "integer"}},
            "OPERAND_TYPE",
        ),
    ],
)
def test_membership_refuses_wrong_scalar_list_and_member_types(
    role, field, replacement, reason
):
    value = program()
    value["inputs"]["applied_record"][role]["properties"]["record"]["properties"][
        field
    ] = replacement
    with pytest.raises(api().PacketRefusal) as caught:
        validate(value)
    assert caught.value.reason == reason


def test_membership_cannot_consume_undeclared_or_future_operands():
    value = program()
    for bad, reason in (
        (operand("applied_record", "unknown", "record"), "UNDECLARED_BINDING"),
        (operand("result", "later", "value"), "FORWARD_RESULT"),
        (operand("applied_record", "grant", "record", "unknown"), "UNRESOLVED_PATH"),
    ):
        value["steps"][0]["members"] = bad
        with pytest.raises(api().PacketRefusal) as caught:
            validate(value)
        assert caught.value.reason == reason


def test_membership_has_no_result_to_consume_or_domain_write():
    value = program()
    value["steps"].append(
        {
            "opcode": "SET_PROTOCOL_STATE",
            "target": "PROTOCOL_INDEX",
            "name": "context-identities",
            "value": operand("result", "membership", "value"),
            "refusal": "NO_RESULT",
        }
    )
    with pytest.raises(api().PacketRefusal) as caught:
        api().validate_program(
            value,
            instruction_schema=json.loads(
                (HERE.parent / "instructions.schema.json").read_bytes()
            ),
            profile=profile(),
        )
    assert caught.value.reason == "FORWARD_RESULT"


def test_retained_membership_cases_are_definition_evidence_not_runtime_results():
    value = json.loads((HERE / "membership-cases.json").read_bytes())
    assert value["runtime_executed"] is False
    assert value["cases"] == [
        {"value": "AMEND", "members": ["READ", "AMEND"], "expected": "PASS"},
        {"value": "DELETE", "members": ["READ", "AMEND"], "expected": "REFUSE"},
        {"value": "AMEND", "members": [], "expected": "REFUSE"},
        {"value": "amend", "members": ["AMEND"], "expected": "REFUSE"},
        {"value": "AMEND ", "members": ["AMEND"], "expected": "REFUSE"},
        {"value": "AMEND", "members": ["AMEND", "AMEND"], "expected": "PASS"},
        {"value": "AMEND", "members": ["AMEND", "READ"], "expected": "PASS"},
    ]
