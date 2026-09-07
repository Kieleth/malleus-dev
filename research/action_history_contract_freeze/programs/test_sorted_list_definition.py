"""Canonical-list definitions and legacy witnesses, not a new interpreter."""

from copy import deepcopy
import json

from jsonschema import Draft202012Validator
import pytest

from malleus.assent import ProtocolError, _canonical_unique
from research.action_history_contract_freeze.programs.test_packet_validator import (
    HERE,
    api,
    obj,
    operand,
    validate,
)


def instruction():
    return {
        "opcode": "REQUIRE_SORTED_UNIQUE_STRINGS",
        "values": operand("event", "body", "values"),
        "refusal": "LIST_NOT_CANONICAL",
    }


def program():
    return {
        "name": "neutral-canonical-list-fragment",
        "inputs": {
            "event": {
                "body": obj(values={"type": "array", "items": {"type": "string"}})
            }
        },
        "required_capabilities": [],
        "introductions": [],
        "steps": [instruction()],
    }


def test_sorted_list_instruction_is_closed_without_result_or_callback():
    schema = json.loads((HERE.parent / "instructions.schema.json").read_bytes())
    validator = Draft202012Validator(schema)
    value = instruction()
    validator.validate(value)
    for field in value:
        missing = deepcopy(value)
        del missing[field]
        assert not validator.is_valid(missing), field
    for field in ("result", "target", "callback", "comparison", "normalization"):
        assert not validator.is_valid({**value, field: "unused"}), field


def test_sorted_list_static_check_preserves_program_without_execution():
    value = program()
    before = deepcopy(value)
    assert validate(value) == {
        "status": "STATIC_VALID",
        "steps": 1,
        "runtime_executed": False,
    }
    assert value == before


@pytest.mark.parametrize(
    ("replacement", "reason"),
    [
        ({"type": "string"}, "OPERAND_TYPE"),
        ({"type": "array"}, "UNRESOLVED_PATH"),
        ({"type": "array", "items": {"type": "integer"}}, "OPERAND_TYPE"),
        ({"type": "array", "items": {"type": "boolean"}}, "OPERAND_TYPE"),
        ({"type": "array", "items": {"type": "null"}}, "OPERAND_TYPE"),
        ({"type": "array", "items": obj(id={"type": "string"})}, "OPERAND_TYPE"),
    ],
)
def test_sorted_list_rejects_mistyped_or_unbound_item_schemas(replacement, reason):
    value = program()
    value["inputs"]["event"]["body"]["properties"]["values"] = replacement
    with pytest.raises(api().PacketRefusal) as caught:
        validate(value)
    assert caught.value.reason == reason


@pytest.mark.parametrize(
    ("replacement", "reason"),
    [
        (operand("event", "unknown", "values"), "UNDECLARED_BINDING"),
        (operand("event", "body", "missing"), "UNRESOLVED_PATH"),
        (operand("result", "later", "value"), "FORWARD_RESULT"),
    ],
)
def test_sorted_list_requires_an_explicit_available_operand(replacement, reason):
    value = program()
    value["steps"][0]["values"] = replacement
    with pytest.raises(api().PacketRefusal) as caught:
        validate(value)
    assert caught.value.reason == reason


def test_registration_fields_and_refusals_are_data_not_checker_branches():
    packet = json.loads((HERE / "registration-list-checks.json").read_bytes())
    value = packet["program"]
    before = deepcopy(packet)
    assert packet["status"] == "STATIC_VALID_FRAGMENT"
    assert packet["runtime_executed"] is False
    assert validate(value)["steps"] == 2
    assert value["steps"] == [
        {
            "opcode": "REQUIRE_SORTED_UNIQUE_STRINGS",
            "values": operand("event", "grant", "record", "permitted_action_types"),
            "refusal": "GRANT_ACTION_TYPES_NOT_CANONICAL",
        },
        {
            "opcode": "REQUIRE_SORTED_UNIQUE_STRINGS",
            "values": operand("event", "monitor", "record", "input_artifact_ids"),
            "refusal": "MONITOR_INPUT_IDS_NOT_CANONICAL",
        },
    ]
    assert not value["introductions"] and not value["required_capabilities"]
    assert packet == before


def test_frozen_value_cases_are_legacy_witnesses_not_instruction_execution():
    packet = json.loads((HERE / "sorted-list-cases.json").read_bytes())
    assert packet["runtime_executed"] is False
    assert packet["cases"] == [
        {"values": ["AMEND", "READ"], "expected": "PASS"},
        {"values": ["READ", "AMEND"], "expected": "REFUSE"},
        {"values": ["AMEND", "AMEND"], "expected": "REFUSE"},
        {"values": [], "expected": "PASS"},
        {"values": ["AMEND"], "expected": "PASS"},
        {"values": [""], "expected": "PASS"},
        {"values": ["A", "a"], "expected": "PASS"},
        {"values": ["A ", "A"], "expected": "REFUSE"},
        {"values": ["e\u0301", "\u00e9"], "expected": "PASS"},
        {"values": ["\ue000", "\U00010000"], "expected": "PASS"},
        {"values": ["\U00010000", "\ue000"], "expected": "REFUSE"},
        {"values": "AMEND", "expected": "REFUSE"},
        {"values": ["A", None], "expected": "REFUSE"},
        {"values": ["A", 1], "expected": "REFUSE"},
        {"values": [{}], "expected": "REFUSE"},
    ]
    # The private legacy helper assumes earlier record typing. Do not turn it
    # into a new instruction executor or claim its malformed-input behavior.
    for case in packet["cases"]:
        values = case["values"]
        if isinstance(values, list) and all(isinstance(v, str) for v in values):
            before = deepcopy(values)
            if case["expected"] == "PASS":
                _canonical_unique(values, "existing Assent witness")
            else:
                with pytest.raises(ProtocolError):
                    _canonical_unique(values, "existing Assent witness")
            assert values == before


def test_sorted_list_decision_is_closed_but_runtime_remains_unimplemented():
    binding = json.loads((HERE.parent / "definition-inputs.json").read_bytes())
    assert "SORTED_LIST_DECISION.md" in " ".join(binding["accepted_decisions"])
    assert binding["interpreter"] == "NOT_IMPLEMENTED"
    text = (HERE.parent / "DEFINITION.md").read_text()
    assert "REQUIRE_SORTED_UNIQUE_STRINGS" in text
    assert "code-point order" in text
