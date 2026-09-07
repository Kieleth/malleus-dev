"""Refuse positional schemas rather than infer the wrong operand type."""

from copy import deepcopy

from jsonschema import Draft202012Validator
import pytest

from research.action_history_contract_freeze.programs.test_membership_definition import (
    program as membership_program,
)
from research.action_history_contract_freeze.programs.test_packet_validator import (
    api,
    obj,
    operand,
    specimen,
    validate,
)


def positional():
    return {
        "type": "array",
        "minItems": 1,
        "prefixItems": [{"type": "integer"}],
        "items": {"type": "string"},
    }


def comparison(array):
    value = specimen()
    value["inputs"]["artifact"]["context"] = obj(value=array)
    value["inputs"]["event"]["literal"] = obj(
        value={"type": "string", "const": "AMEND"}
    )
    value["steps"] = [
        {
            "opcode": "REQUIRE_COMPARE",
            "left": operand("artifact", "context", "value", 0),
            "right": operand("event", "literal", "value"),
            "comparison": "EQ",
            "value_kind": "STRING",
            "refusal": "NOT_STRING_EQUAL",
        }
    ]
    return value


def test_positional_integer_cannot_be_misread_as_trailing_string_items():
    schema = positional()
    Draft202012Validator(schema).validate([7])
    value = comparison(schema)
    before = deepcopy(value)
    with pytest.raises(api().PacketRefusal) as caught:
        validate(value)
    assert caught.value.reason == "DEFINITION_SCHEMA"
    assert value == before


@pytest.mark.parametrize("nested", ["object", "array"])
def test_unsupported_positional_schema_refuses_recursively(nested):
    schema = (
        obj(unread=positional())
        if nested == "object"
        else {"type": "array", "items": positional()}
    )
    value = specimen()
    value["inputs"]["artifact"]["unused"] = obj(value=schema)
    with pytest.raises(api().PacketRefusal) as caught:
        validate(value)
    assert caught.value.reason == "DEFINITION_SCHEMA"


def test_homogeneous_array_still_resolves_a_guaranteed_string_item():
    schema = {"type": "array", "minItems": 1, "items": {"type": "string"}}
    Draft202012Validator(schema).validate(["AMEND"])
    assert validate(comparison(schema))["status"] == "STATIC_VALID"


def test_membership_cannot_treat_a_mixed_positional_array_as_a_string_list():
    value = membership_program()
    fields = value["inputs"]["applied_record"]["grant"]["properties"]["record"][
        "properties"
    ]
    fields["permitted_action_types"] = positional()
    Draft202012Validator(fields["permitted_action_types"]).validate([7, "AMEND"])
    with pytest.raises(api().PacketRefusal) as caught:
        validate(value)
    assert caught.value.reason == "DEFINITION_SCHEMA"
