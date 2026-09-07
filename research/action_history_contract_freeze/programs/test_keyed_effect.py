"""Keyed instruction definitions only. No assignment or action executes."""

from copy import deepcopy
import json

import pytest

from research.action_history_contract_freeze.programs.test_packet_validator import (
    HERE,
    api,
    obj,
    operand,
    validate,
)


def fixture():
    program = {
        "name": "keyed-index-fragment",
        "inputs": {
            "event": {
                "entry": obj(
                    id={"type": "string"},
                    identity={"type": "string", "format": "sha256"},
                    value={"type": "string"},
                )
            }
        },
        "required_capabilities": [],
        "introductions": [],
        "steps": [
            {
                "opcode": "SET_PROTOCOL_STATE",
                "target": "PROTOCOL_INDEX",
                "name": "entries",
                "keys": [operand("event", "entry", "id")],
                "value": operand("event", "entry", "value"),
                "refusal": "INVALID_ENTRY",
            }
        ],
    }
    profile = {
        "targets": {
            "entries": {
                "target": "PROTOCOL_INDEX",
                "storage_path": ["protocol", "entries"],
                "key_schemas": [{"type": "string"}],
                "value_schema": {"type": "string"},
            }
        },
        "capabilities": [],
    }
    return program, profile


def refuses(program, profile, reason):
    before = deepcopy((program, profile))
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program, profile)
    assert caught.value.reason == reason
    assert (program, profile) == before


@pytest.mark.parametrize("composite", [False, True])
def test_ordered_key_operands_resolve_without_execution_or_input_mutation(composite):
    program, profile = fixture()
    if composite:
        program["steps"][0]["keys"].append(operand("event", "entry", "identity"))
        profile["targets"]["entries"]["key_schemas"].append(
            {"type": "string", "format": "sha256"}
        )
    before = deepcopy((program, profile))
    assert validate(program, profile) == {
        "status": "STATIC_VALID",
        "steps": 1,
        "runtime_executed": False,
    }
    assert (program, profile) == before
    if composite:
        program["steps"][0]["keys"].reverse()
        refuses(program, profile, "OPERAND_TYPE")


@pytest.mark.parametrize("bad", [[], None, "id", ["id"]])
def test_missing_or_malformed_key_operands_refuse(bad):
    program, profile = fixture()
    program["steps"][0]["keys"] = bad
    refuses(program, profile, "INSTRUCTION_SHAPE")


def test_keyless_legacy_index_assignment_has_no_fallback():
    program, profile = fixture()
    del program["steps"][0]["keys"]
    del profile["targets"]["entries"]["key_schemas"]
    refuses(program, profile, "DEFINITION_SHAPE")


@pytest.mark.parametrize("bad", [[], None, {"type": "string"}, [{"type": "integer"}]])
def test_target_must_declare_nonempty_string_key_schemas(bad):
    program, profile = fixture()
    profile["targets"]["entries"]["key_schemas"] = bad
    refuses(program, profile, "DEFINITION_SHAPE")


def test_missing_operand_does_not_infer_a_key_from_the_value():
    program, profile = fixture()
    del program["steps"][0]["keys"]
    refuses(program, profile, "INSTRUCTION_SHAPE")


def test_key_count_must_match_the_declared_index():
    program, profile = fixture()
    program["steps"][0]["keys"].append(operand("event", "entry", "identity"))
    refuses(program, profile, "INDEX_KEY_ARITY")


@pytest.mark.parametrize("kind", ["boolean", "integer", "null", "array"])
def test_keys_cannot_be_cast_to_strings(kind):
    program, profile = fixture()
    program["inputs"]["event"]["entry"]["properties"]["id"] = {"type": kind}
    refuses(program, profile, "OPERAND_TYPE")


@pytest.mark.parametrize(
    ("key", "reason"),
    [
        (operand("event", "missing", "id"), "UNDECLARED_BINDING"),
        (operand("event", "entry", "missing"), "UNRESOLVED_PATH"),
        (operand("result", "future", "value"), "FORWARD_RESULT"),
    ],
)
def test_keys_use_the_existing_operand_resolution_boundary(key, reason):
    program, profile = fixture()
    program["steps"][0]["keys"] = [key]
    refuses(program, profile, reason)


def test_action_head_assignment_stays_scalar_and_keyless():
    program, profile = fixture()
    step = program["steps"][0]
    step.update(target="ACTION_ACCEPTANCE_HEAD", name="action-head")
    del step["keys"]
    profile["targets"] = {
        "action-head": {
            "target": "ACTION_ACCEPTANCE_HEAD",
            "storage_path": ["action_acceptance_head"],
            "value_schema": {"type": "string"},
        }
    }
    assert validate(program, profile)["status"] == "STATIC_VALID"
    step["keys"] = [operand("event", "entry", "id")]
    refuses(program, profile, "INSTRUCTION_SHAPE")
    del step["keys"]
    profile["targets"]["action-head"]["key_schemas"] = [{"type": "string"}]
    refuses(program, profile, "DEFINITION_SHAPE")


def test_index_uniqueness_and_assignment_share_the_declared_key_shape():
    program, profile = fixture()
    program["inputs"]["event"]["records"] = obj(
        value={
            "type": "array",
            "items": obj(id={"type": "string"}, other={"type": "integer"}),
        }
    )
    step = {
        "opcode": "REQUIRE_UNIQUE",
        "records": operand("event", "records", "value"),
        "key_paths": [["id"]],
        "target_index": "entries",
        "refusal": "DUPLICATE_ENTRY",
    }
    program["steps"].insert(0, step)
    assert validate(program, profile)["steps"] == 2
    step["key_paths"] = [["id"], ["other"]]
    refuses(program, profile, "INDEX_KEY_ARITY")
    step["key_paths"] = [["other"]]
    refuses(program, profile, "OPERAND_TYPE")


def test_key_approval_is_recorded_without_claiming_runtime_readiness():
    binding = json.loads((HERE.parent / "definition-inputs.json").read_bytes())
    assert any(
        "KEYED_EFFECT_DECISION.md" in item for item in binding["accepted_decisions"]
    )
    assert binding["interpreter"] == "NOT_IMPLEMENTED"
    assert binding["event_programs"] == "NOT_FROZEN"
    decision = (HERE / "lifecycle/KEYED_EFFECT_DECISION.md").read_text()
    assert "Status: ACCEPTED" in decision
    assert "This does not authorize runtime work" in decision
