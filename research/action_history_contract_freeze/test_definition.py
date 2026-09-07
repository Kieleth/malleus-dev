"""Definition-shape checks only, not action execution conformance."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

import malleus.compiler as api
from malleus.ledger import canonical_json, content_digest


HERE = Path(__file__).parent


def schema(name):
    value = json.loads((HERE / name).read_bytes())
    Draft202012Validator.check_schema(value)
    return value


def shape_witness(kind):
    # Lexical witnesses only. These are not published runtime coordinates,
    # monitor instances, initialized state or proof of reference resolution.
    identity = content_digest({"purpose": "shape witness, not a runtime head"})
    record = {"id": "shape-witness", "record_hash": identity}
    artifact = {"id": "shape-witness", "bytes_sha256": identity}
    value = {
        "schema": f"malleus.action-history.{kind}/research-v1",
        "id": "shape-witness",
        "prefix": {"head": "GENESIS", "event_count": 0},
        "domain": {
            "effective_contract_identity": identity,
            "kcs_acceptance_head": "GENESIS",
            "materialization_head": "GENESIS",
            "accepted_graph_digest": identity,
        },
        "epistemic_policy": record,
        "authorization_policy": record,
    }
    if kind == "initialization":
        value.update(
            profile=artifact,
            record_contract=artifact,
            machine=artifact,
            history_binding=artifact,
        )
    else:
        value.update(
            initialization_identity=identity,
            action_acceptance_head=identity,
            proposal_id="proposal:shape",
            action_id="action:shape",
            episode_key="episode:shape",
            goal=artifact,
            preservation=artifact,
            mapping=artifact,
            pre_state_source=artifact,
        )
    return value


@pytest.mark.parametrize("kind", ["initialization", "original-context"])
def test_context_shapes_are_closed_and_have_no_self_identity(kind):
    validator = Draft202012Validator(schema("contexts.schema.json"))
    value = shape_witness(kind)
    validator.validate(value)
    for field in value:
        missing = deepcopy(value)
        del missing[field]
        assert not validator.is_valid(missing), field
    for field in ("identity", "content_hash", "future_field"):
        assert not validator.is_valid({**value, field: "unbound"})
    assert (
        content_digest(value)
        == "sha256:" + sha256(canonical_json(value).encode()).hexdigest()
    )
    assert content_digest(value) == content_digest(dict(reversed(list(value.items()))))


@pytest.mark.parametrize(
    "prefix",
    [
        {"head": "GENESIS", "event_count": 1},
        {"head": "bad", "event_count": 0},
        {"head": "GENESIS", "event_count": True},
    ],
)
def test_prefix_is_not_a_loose_digest_or_boolean_count(prefix):
    value = shape_witness("initialization")
    value["prefix"] = prefix
    assert not Draft202012Validator(schema("contexts.schema.json")).is_valid(value)


def test_context_coordinate_domains_cannot_replace_each_others_fields():
    value = shape_witness("original-context")
    value["domain"]["action_acceptance_head"] = value.pop("action_acceptance_head")
    assert not Draft202012Validator(schema("contexts.schema.json")).is_valid(value)


def test_instruction_vocabulary_is_finite_and_cannot_write_domain_state():
    declaration = schema("instructions.schema.json")
    validator = Draft202012Validator(declaration)
    names = {item["properties"]["opcode"]["const"] for item in declaration["oneOf"]}
    assert names == {
        "VALIDATE_RECORD",
        "HASH",
        "RESOLVE_RECORD",
        "REQUIRE_COMPARE",
        "REQUIRE_MEMBER",
        "REQUIRE_UNIQUE",
        "REQUIRE_COVERAGE",
        "REQUIRE_INTERVAL",
        "SELECT_CONTROL",
        "INTRODUCE_RECORDS",
        "SET_PROTOCOL_STATE",
    }
    operand = {"root": "result", "name": "checked", "path": ["value"]}
    valid = {
        "opcode": "SET_PROTOCOL_STATE",
        "target": "ACTION_ACCEPTANCE_HEAD",
        "name": "action-head",
        "value": operand,
        "refusal": "INVALID_STATE_TARGET",
    }
    validator.validate(valid)
    for target in (
        "KG",
        "KCS_ACCEPTANCE_HEAD",
        "MATERIALIZATION_HEAD",
        "DOMAIN_CONTRACT",
    ):
        assert not validator.is_valid({**valid, "target": target})
    for opcode in ("CALL_PYTHON", "LOOP", "EVAL", "DISPATCH_EFFECT"):
        assert not validator.is_valid({**valid, "opcode": opcode})
    assert not validator.is_valid({**valid, "callback": "malleus.assent.handler"})


def test_typed_operands_and_comparisons_do_not_accept_ambient_paths():
    validator = Draft202012Validator(schema("instructions.schema.json"))
    operand = {"root": "current", "name": "domain", "path": ["accepted_graph_digest"]}
    valid = {
        "opcode": "REQUIRE_COMPARE",
        "left": operand,
        "right": operand,
        "comparison": "EQ",
        "value_kind": "DIGEST",
        "refusal": "STALE_DOMAIN",
    }
    validator.validate(valid)
    for bad in (
        {**operand, "root": "filesystem"},
        {**operand, "path": []},
        {**operand, "path": [True]},
    ):
        assert not validator.is_valid({**valid, "left": bad})
    assert not validator.is_valid({**valid, "comparison": "PYTHON_EXPRESSION"})


def test_current_machine_does_not_pretend_to_execute_the_candidate_grammar():
    candidate = {
        "grammar": "malleus.action-history-machine/research-v1",
        "capabilities": [],
        "events": {},
        "indexes": {},
        "record_schemas": {},
    }
    with pytest.raises(api.ProtocolMachineProgramRefusal) as caught:
        api.ProtocolMachineProgram.from_bytes(canonical_json(candidate).encode())
    assert caught.value.reason.name == "UNSUPPORTED_GRAMMAR"


def test_definition_does_not_claim_missing_producer_implementations_exist():
    text = (HERE / "DEFINITION.md").read_text()
    assert (
        "implementation hashes and\nvalid monitor/policy instances remain UNBOUND"
        in text
    )
    assert "not a completed executable\ncontract freeze" in text
    prose = " ".join(text.split())
    assert "Failing tests may precede implementation" in prose
    assert "before successful executable freeze" in prose
    assert "before runtime RED" not in prose


OPERAND = {"root": "event", "name": "body", "path": ["record"]}
INSTRUCTIONS = [
    {
        "opcode": "VALIDATE_RECORD",
        "record": OPERAND,
        "contract": OPERAND,
        "result": "checked",
    },
    {"opcode": "HASH", "recipe": "VALUE", "value": OPERAND, "result": "digest"},
    {
        "opcode": "RESOLVE_RECORD",
        "record_id": OPERAND,
        "record_type": OPERAND,
        "record_hash": OPERAND,
        "scope": "APPLIED",
        "result": "resolved",
    },
    {
        "opcode": "REQUIRE_COMPARE",
        "left": OPERAND,
        "right": OPERAND,
        "comparison": "EQ",
        "value_kind": "DIGEST",
    },
    {"opcode": "REQUIRE_UNIQUE", "records": OPERAND, "key_paths": [["id"]]},
    {
        "opcode": "REQUIRE_MEMBER",
        "value": OPERAND,
        "members": OPERAND,
        "value_kind": "STRING",
    },
    {
        "opcode": "REQUIRE_COVERAGE",
        "required": OPERAND,
        "outputs": OPERAND,
        "context": OPERAND,
    },
    {"opcode": "REQUIRE_INTERVAL", "inner": OPERAND, "outer": OPERAND},
    {
        "opcode": "SELECT_CONTROL",
        "policy": OPERAND,
        "outputs": OPERAND,
        "context": OPERAND,
        "result": "selection",
    },
    {
        "opcode": "INTRODUCE_RECORDS",
        "records": OPERAND,
        "dependencies": OPERAND,
        "result": "introduced",
    },
    {
        "opcode": "SET_PROTOCOL_STATE",
        "target": "PROTOCOL_INDEX",
        "name": "records",
        "keys": [OPERAND],
        "value": OPERAND,
    },
]


@pytest.mark.parametrize("instruction", INSTRUCTIONS, ids=lambda item: item["opcode"])
def test_each_instruction_has_a_positive_and_closed_required_operands(instruction):
    validator = Draft202012Validator(schema("instructions.schema.json"))
    value = {**instruction, "refusal": "BOUNDARY_REFUSED"}
    validator.validate(value)
    for field in value:
        missing = deepcopy(value)
        del missing[field]
        assert not validator.is_valid(missing), field
    assert not validator.is_valid({**value, "implementation": "python:handler"})


def test_hash_recipes_require_their_distinct_identity_inputs():
    validator = Draft202012Validator(schema("instructions.schema.json"))
    value = {**INSTRUCTIONS[1], "refusal": "INVALID_HASH_INPUT"}
    for recipe, field in (("RECORD", "record_type"), ("ARTIFACT", "artifact_contract")):
        selected = {**value, "recipe": recipe}
        assert not validator.is_valid(selected)
        validator.validate({**selected, field: OPERAND})
    assert not validator.is_valid({**value, "record_type": OPERAND})
    assert not validator.is_valid({**value, "recipe": "EVAL"})


def capability_witness(kind):
    # No actual producer is represented by these synthetic shape bindings.
    identity = content_digest({"purpose": "capability shape witness only"})
    artifact = {"id": "shape:artifact", "bytes_sha256": identity}
    record = {"id": "shape:record", "record_hash": identity}
    inputs = {"proposal": record, "action": record}
    if kind == "TYPE":
        inputs["record_contract"] = artifact
    else:
        inputs.update(
            executor_id="shape:executor",
            grant=record,
            scope_association=artifact,
            requested_interval=artifact,
            authorization_policy=record,
            original_context=artifact,
            current_context=artifact,
        )
    return {
        "kind": kind,
        "contract": artifact,
        "implementation": {
            "id": "shape:producer",
            "version": "shape-only",
            "bytes_sha256": identity,
        },
        "effects": "PURE",
        "inputs": inputs,
    }


@pytest.mark.parametrize("kind", ["TYPE", "DIRECT_GRANT"])
def test_check_binding_requires_real_identity_slots_without_placeholder_escape(kind):
    validator = Draft202012Validator(schema("capabilities.schema.json"))
    value = capability_witness(kind)
    validator.validate(value)
    for field in value:
        missing = deepcopy(value)
        del missing[field]
        assert not validator.is_valid(missing), field
    for role in value["inputs"]:
        missing = deepcopy(value)
        del missing["inputs"][role]
        assert not validator.is_valid(missing), role
    for implementation in (
        None,
        "UNBOUND",
        {"specification_sha256": value["contract"]["bytes_sha256"]},
    ):
        assert not validator.is_valid({**value, "implementation": implementation})
    for field in ("outcome", "callback", "writer"):
        assert not validator.is_valid({**value, field: "SATISFIED"})
    assert not validator.is_valid({**value, "effects": "WRITE_SOURCE"})


@pytest.mark.parametrize("kind", ["initialization", "original-context"])
def test_nested_context_identity_slots_reject_missing_extra_and_mistyped_fields(kind):
    validator = Draft202012Validator(schema("contexts.schema.json"))
    value = shape_witness(kind)
    for name, nested in value.items():
        if not isinstance(nested, dict):
            continue
        for field in nested:
            missing = deepcopy(value)
            del missing[name][field]
            assert not validator.is_valid(missing), (name, field)
        extra = deepcopy(value)
        extra[name]["hidden_default"] = True
        assert not validator.is_valid(extra), name
    for bad in ("", None, True, "UNBOUND", "sha256:" + "x" * 64):
        wrong = deepcopy(value)
        wrong["domain"]["accepted_graph_digest"] = bad
        assert not validator.is_valid(wrong)


def test_nonempty_verified_prefix_shape_and_canonical_round_trip():
    validator = Draft202012Validator(schema("contexts.schema.json"))
    value = shape_witness("initialization")
    value["prefix"] = {"head": content_digest({"shape": "head"}), "event_count": 1}
    validator.validate(value)
    assert json.loads(canonical_json(value)) == value
    assert not validator.is_valid(
        {**value, "prefix": {**value["prefix"], "event_count": 0}}
    )


def assert_local_binding(binding):
    expected = {
        "DEFINITION.md",
        "contexts.schema.json",
        "instructions.schema.json",
        "capabilities.schema.json",
        "test_definition.py",
    }
    assert set(binding["local_files"]) == expected
    for name, digest in binding["local_files"].items():
        assert "sha256:" + sha256((HERE / name).read_bytes()).hexdigest() == digest, (
            name
        )


def test_definition_packet_binds_every_declared_local_file():
    assert_local_binding(json.loads((HERE / "definition-inputs.json").read_bytes()))


def test_packet_binding_guard_rejects_changed_digest_and_missing_file():
    binding = json.loads((HERE / "definition-inputs.json").read_bytes())
    changed = deepcopy(binding)
    changed["local_files"]["contexts.schema.json"] = "sha256:" + "0" * 64
    with pytest.raises(AssertionError, match="contexts.schema.json"):
        assert_local_binding(changed)
    missing = deepcopy(binding)
    del missing["local_files"]["contexts.schema.json"]
    with pytest.raises(AssertionError):
        assert_local_binding(missing)
