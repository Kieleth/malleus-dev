"""Research definition preflight, never an action lifecycle simulation."""

from copy import deepcopy
from importlib import import_module
import json
from pathlib import Path

import pytest


HERE = Path(__file__).parent


def api():
    return import_module(
        "research.action_history_contract_freeze.programs.packet_validator"
    )


def scalar(kind, coordinate=None):
    value = {"type": kind}
    if coordinate is not None:
        value["x-coordinate"] = coordinate
        value["format"] = "sha256"
    return value


def obj(**properties):
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def operand(root, name, *path):
    return {"root": root, "name": name, "path": list(path)}


def specimen():
    digest = {"type": "string", "format": "sha256"}
    state = obj(value=scalar("string", "ACTION_ACCEPTANCE"))
    return {
        "name": "neutral-context-fragment",
        "inputs": {
            "event": {"context": obj(identity=digest)},
            "original": {"action": deepcopy(state)},
            "current": {"action": deepcopy(state)},
            "artifact": {"context": obj(value=obj(id=scalar("string")))},
        },
        "required_capabilities": [],
        "introductions": [],
        "steps": [
            {
                "opcode": "HASH",
                "recipe": "VALUE",
                "value": operand("artifact", "context", "value"),
                "result": "context-digest",
                "refusal": "BAD_CONTEXT",
            },
            {
                "opcode": "REQUIRE_COMPARE",
                "left": operand("event", "context", "identity"),
                "right": operand("result", "context-digest", "value"),
                "comparison": "EQ",
                "value_kind": "DIGEST",
                "refusal": "WRONG_CONTEXT_IDENTITY",
            },
            {
                "opcode": "REQUIRE_COMPARE",
                "left": operand("original", "action", "value"),
                "right": operand("current", "action", "value"),
                "comparison": "EQ",
                "value_kind": "DIGEST",
                "refusal": "STALE_ACTION_CONTEXT",
            },
            {
                "opcode": "SET_PROTOCOL_STATE",
                "target": "PROTOCOL_INDEX",
                "name": "context-identities",
                "value": operand("result", "context-digest", "value"),
                "refusal": "INVALID_STATE_TARGET",
            },
        ],
    }


def profile():
    return {
        "targets": {
            "context-identities": {
                "target": "PROTOCOL_INDEX",
                "storage_path": ["protocol", "context-identities"],
                "value_schema": {"type": "string", "format": "sha256"},
            },
        },
        "capabilities": ["TYPE", "DIRECT_GRANT"],
    }


def validate(program=None, declaration=None):
    return api().validate_program(
        specimen() if program is None else program,
        instruction_schema=json.loads(
            (HERE.parent / "instructions.schema.json").read_bytes()
        ),
        profile=profile() if declaration is None else declaration,
    )


def test_static_program_accepts_closed_paths_and_does_not_execute_or_mutate():
    program = specimen()
    original = deepcopy(program)
    result = validate(program)
    assert result == {"status": "STATIC_VALID", "steps": 4, "runtime_executed": False}
    assert program == original


@pytest.mark.parametrize(
    ("root", "name", "path", "reason"),
    [
        ("filesystem", "context", ["value"], "INSTRUCTION_SHAPE"),
        ("artifact", "missing", ["value"], "UNDECLARED_BINDING"),
        ("artifact", "context", ["missing"], "UNRESOLVED_PATH"),
        ("artifact", "context", [], "INSTRUCTION_SHAPE"),
        ("artifact", "context", [True], "INSTRUCTION_SHAPE"),
        ("result", "later", ["value"], "FORWARD_RESULT"),
    ],
)
def test_unresolvable_operands_refuse(root, name, path, reason):
    program = specimen()
    program["steps"][0]["value"] = {"root": root, "name": name, "path": path}
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == reason


@pytest.mark.parametrize("optional", [True, False])
def test_paths_require_guaranteed_fields_and_zero_based_array_bounds(optional):
    program = specimen()
    container = program["inputs"]["artifact"]["context"]
    if optional:
        container["required"] = []
    else:
        container["properties"]["value"] = {
            "type": "array",
            "minItems": 1,
            "items": scalar("string"),
        }
        program["steps"][0]["value"]["path"] = ["value", 1]
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "UNRESOLVED_PATH"
    if not optional:
        program["steps"][0]["value"]["path"] = ["value", 0]
        assert validate(program)["status"] == "STATIC_VALID"


@pytest.mark.parametrize("kind", ["boolean", "integer", "array"])
def test_compare_rejects_wrong_types(kind):
    program = specimen()
    program["inputs"]["current"]["action"]["properties"]["value"] = scalar(kind)
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "OPERAND_TYPE"


def test_digest_operand_cannot_be_an_unconstrained_string():
    program = specimen()
    program["inputs"]["event"]["context"]["properties"]["identity"] = scalar("string")
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "OPERAND_TYPE"


def test_equal_lexical_types_do_not_alias_action_and_domain_heads():
    program = specimen()
    program["inputs"]["current"]["action"]["properties"]["value"]["x-coordinate"] = (
        "KCS_ACCEPTANCE"
    )
    assert (
        program["inputs"]["original"]["action"]["properties"]["value"]["x-coordinate"]
        == "ACTION_ACCEPTANCE"
    )
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "COORDINATE_DOMAIN"


@pytest.mark.parametrize(
    "invalid", [True, {"type": ["string", "null"]}, {"type": "object"}]
)
def test_unsupported_input_schema_refuses_typed(invalid):
    program = specimen()
    program["inputs"]["event"]["context"] = invalid
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "DEFINITION_SCHEMA"


@pytest.mark.parametrize(
    "opcode",
    [
        "VALIDATE_RECORD",
        "HASH",
        "RESOLVE_RECORD",
        "REQUIRE_UNIQUE",
        "REQUIRE_COVERAGE",
        "REQUIRE_INTERVAL",
        "SELECT_CONTROL",
        "INTRODUCE_RECORDS",
    ],
)
def test_remaining_instruction_types_resolve_from_explicit_wrappers(opcode):
    program, declaration = specimen(), profile()
    record = obj(
        id=scalar("string"), content_hash={"type": "string", "format": "sha256"}
    )
    records = {"type": "array", "minItems": 1, "items": record}
    interval = obj(start={"type": "string", "format": "aware-instant"})
    program["inputs"]["event"]["payload"] = obj(
        record=record,
        records=records,
        dependencies={"type": "array", "items": scalar("string")},
        record_id=scalar("string"),
        record_hash={"type": "string", "format": "sha256"},
        record_type={"type": "string", "const": "NeutralRecord"},
        contract=obj(identity=scalar("string")),
        required=records,
        outputs=records,
        context=obj(id=scalar("string")),
        inner=interval,
        outer=interval,
        policy=obj(id=scalar("string")),
    )
    fields = {
        "VALIDATE_RECORD": ["record", "contract"],
        "HASH": ["record_type"],
        "RESOLVE_RECORD": ["record_id", "record_type", "record_hash"],
        "REQUIRE_UNIQUE": ["records"],
        "REQUIRE_COVERAGE": ["required", "outputs", "context"],
        "REQUIRE_INTERVAL": ["inner", "outer"],
        "SELECT_CONTROL": ["policy", "outputs", "context"],
        "INTRODUCE_RECORDS": ["records", "dependencies"],
    }
    step = {"opcode": opcode, "refusal": "INVALID_INPUT"}
    step.update({name: operand("event", "payload", name) for name in fields[opcode]})
    if opcode in {
        "VALIDATE_RECORD",
        "HASH",
        "RESOLVE_RECORD",
        "SELECT_CONTROL",
        "INTRODUCE_RECORDS",
    }:
        step["result"] = "checked"
    if opcode == "HASH":
        step.update(recipe="RECORD", value=operand("event", "payload", "record"))
    if opcode == "RESOLVE_RECORD":
        step["scope"] = "APPLIED"
        declaration["record_schemas"] = {"NeutralRecord": record}
    if opcode == "REQUIRE_UNIQUE":
        step["key_paths"] = [["id"]]
    if opcode == "SELECT_CONTROL":
        declaration["control_result_schema"] = obj(verdict=scalar("string"))
    program["steps"] = [step]
    assert validate(program, declaration)["status"] == "STATIC_VALID"
    first_operand = next(value for value in step.values() if isinstance(value, dict))
    first_operand["path"] = ["unknown"]
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program, declaration)
    assert caught.value.reason == "UNRESOLVED_PATH"


def test_results_are_single_assignment_and_not_caller_inputs():
    program = specimen()
    program["steps"].append(deepcopy(program["steps"][0]))
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "REUSED_RESULT"
    program = specimen()
    program["inputs"]["result"] = {"forged": obj(value=scalar("string"))}
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "INPUT_ROOT"


@pytest.mark.parametrize(
    ("introductions", "reason"),
    [
        ([{"name": "one", "depends_on": ["missing"]}], "UNRESOLVED_DEPENDENCY"),
        (
            [{"name": "one", "depends_on": ["two"]}, {"name": "two", "depends_on": []}],
            "FORWARD_DEPENDENCY",
        ),
        (
            [
                {"name": "one", "depends_on": ["two"]},
                {"name": "two", "depends_on": ["one"]},
            ],
            "CYCLIC_DEPENDENCY",
        ),
        (
            [{"name": "one", "depends_on": []}, {"name": "one", "depends_on": []}],
            "REUSED_INTRODUCTION",
        ),
    ],
)
def test_introduction_dependencies_are_finite_and_ordered(introductions, reason):
    program = specimen()
    program["introductions"] = introductions
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == reason


def test_protocol_index_requires_declared_target_and_cannot_alias_domain_state():
    program = specimen()
    program["steps"][-1]["name"] = "undeclared"
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "UNDECLARED_TARGET"
    for path in (["domain", "accepted_graph"], ["kcs_acceptance_head"], ["contract"]):
        declaration = profile()
        declaration["targets"]["context-identities"]["storage_path"] = path
        with pytest.raises(api().PacketRefusal) as caught:
            validate(declaration=declaration)
        assert caught.value.reason == "DOMAIN_STATE_TARGET"


def test_unknown_capability_refuses_even_when_instruction_shapes_pass():
    program = specimen()
    program["required_capabilities"] = ["CALL_PYTHON"]
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "UNKNOWN_CAPABILITY"


def test_actual_membership_instruction_attempt_is_not_silently_implemented():
    attempt = json.loads((HERE / "missing-membership.json").read_bytes())
    program = specimen()
    program["steps"] = [attempt["instruction_attempt"]]
    with pytest.raises(api().PacketRefusal) as caught:
        validate(program)
    assert caught.value.reason == "INSTRUCTION_SHAPE"
    assert attempt["positive"] == {
        "action_type": "AMEND",
        "permitted_action_types": ["READ", "AMEND"],
    }
    assert attempt["negative"] == {
        "action_type": "DELETE",
        "permitted_action_types": ["READ", "AMEND"],
    }


@pytest.mark.parametrize(
    "end",
    [None, "2026-09-07T00:00:00", "2026-09-06T23:59:59Z", "2026-09-07T00:00:00+00:00"],
)
def test_interval_content_refuses_null_naive_reversed_and_equal_end(end):
    value = {"start": "2026-09-07T00:00:00Z", "end": end}
    with pytest.raises(api().PacketRefusal) as caught:
        api().validate_interval(value)
    assert caught.value.reason == "INVALID_INTERVAL"


def test_interval_absent_end_is_unbounded_and_does_not_infer_a_timezone():
    value = {"start": "2026-09-07T00:00:00Z"}
    assert api().validate_interval(value) is None
    assert value == {"start": "2026-09-07T00:00:00Z"}
    with pytest.raises(api().PacketRefusal):
        api().validate_interval({"start": "2026-09-07"})
    with pytest.raises(api().PacketRefusal):
        api().validate_interval({**value, "default_timezone": "UTC"})


def test_closed_current_context_and_equality_scope_contents():
    content = json.loads((HERE / "content-examples.json").read_bytes())
    for kind, value in content.items():
        api().validate_content(kind, value)
        for field in value:
            missing = deepcopy(value)
            del missing[field]
            with pytest.raises(api().PacketRefusal):
                api().validate_content(kind, missing)
        with pytest.raises(api().PacketRefusal):
            api().validate_content(kind, {**value, "ambient_path": "/elsewhere"})


def test_monitor_contract_closes_input_order_and_separates_hash_domains():
    contract = json.loads((HERE / "monitor-contract.json").read_bytes())
    api().validate_monitor_contract(contract)
    for roles in (
        [],
        ["action", "proposal", "record_contract"],
        ["proposal", "proposal", "record_contract"],
    ):
        broken = deepcopy(contract)
        broken["TYPE"]["ordered_inputs"] = roles
        with pytest.raises(api().PacketRefusal):
            api().validate_monitor_contract(broken)
    for field, wrong in (
        ("monitor_hash", "implementation.bytes_sha256"),
        ("monitor_version", "implementation.version"),
        ("assessment_outcome", "caller.outcome"),
    ):
        broken = deepcopy(contract)
        broken["output_bindings"][field] = wrong
        with pytest.raises(api().PacketRefusal):
            api().validate_monitor_contract(broken)
    assert contract["implementations"] == {"TYPE": "UNBOUND", "DIRECT_GRANT": "UNBOUND"}
