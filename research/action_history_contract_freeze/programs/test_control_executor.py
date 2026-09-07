"""Finite control operations against the existing independent control recipe."""

from copy import deepcopy
from dataclasses import asdict

import pytest

from malleus.ledger import canonical_json, content_digest
from research.action_history_contract_freeze.programs.test_executor import (
    arguments,
    run,
    api,
)
from research.action_history_contract_freeze.programs.test_packet_validator import (
    obj,
    operand,
)
from tests import test_control as established


def shape(value):
    """Closed finite test-input schema, not expected outputs or an oracle."""
    if type(value) is dict:
        return obj(**{k: shape(v) for k, v in value.items()})
    if type(value) is list:
        return {
            "type": "array",
            "items": shape(value[0]) if value else {"type": "string"},
        }
    return {"type": {str: "string", int: "integer", bool: "boolean"}[type(value)]}


def control(kind, outcomes=("SATISFIED", "SATISFIED")):
    authority = kind == "AUTHORIZATION"
    monitors = [
        established.authority_monitor(f"monitor:{i}")
        if authority
        else established.monitor(f"monitor:{i}", "TYPE")
        for i in range(2)
    ]
    policy = (
        established.authorization_policy(monitors)
        if authority
        else established.policy([(m, "REJECT", "DEFER") for m in monitors])
    )
    outputs = [
        established.authority_assessment(m, policy, outcome, suffix=str(i))
        if authority
        else established.assessment(m, outcome, suffix=str(i))
        for i, (m, outcome) in enumerate(zip(monitors, outcomes, strict=True))
    ]
    bindings = {
        "proposal_id": "proposal:1",
        "proposal_content_hash": established.PROPOSAL_HASH,
        "base_acceptance_head": established.BASE_HEAD,
    }
    if authority:
        bindings.update(
            action_proposal_id="action:1",
            action_content_hash=established.ACTION_HASH,
            evaluated_actor_id="actor:executor",
            authority_policy_id=policy["id"],
            authority_policy_hash=policy["content_hash"],
        )
    recipe = f"ASSENT_{kind}_CONTROL_V1"
    context = {"recipe": recipe, "monitors": monitors, "bindings": bindings}
    required = [
        {"monitor_id": m["id"], "monitor_record_hash": m["content_hash"]}
        for m in monitors
    ]
    inputs = {
        "event": {"outputs": {"value": outputs}},
        "artifact": {
            "policy": {"value": policy},
            "context": {"value": context},
            "required": {"value": required},
        },
    }
    expected = (established.evaluate_authority if authority else established.evaluate)(
        policy, monitors, outputs
    )
    definition = {
        "name": "existing-control",
        "inputs": {
            r: {k: shape(v) for k, v in names.items()} for r, names in inputs.items()
        },
        "required_capabilities": [recipe],
        "introductions": [],
        "steps": [
            {
                "opcode": "REQUIRE_COVERAGE",
                "required": operand("artifact", "required", "value"),
                "outputs": operand("event", "outputs", "value"),
                "context": operand("artifact", "context", "value"),
                "refusal": "CHECK_COVERAGE",
            },
            {
                "opcode": "SELECT_CONTROL",
                "policy": operand("artifact", "policy", "value"),
                "outputs": operand("event", "outputs", "value"),
                "context": operand("artifact", "context", "value"),
                "result": "control",
                "refusal": "INVALID_CONTROL",
            },
        ],
    }
    strings = {"type": "array", "items": {"type": "string"}}
    profile = {
        "targets": {},
        "capabilities": [recipe],
        "control_result_schema": obj(
            verdict={"type": "string"},
            assessment_ids=strings,
            triggered_assessment_ids=strings,
            evaluation_hash={"type": "string", "format": "sha256"},
        ),
    }
    return arguments(definition, profile, inputs), expected


@pytest.mark.parametrize("kind", ["EPISTEMIC", "AUTHORIZATION"])
@pytest.mark.parametrize(
    "outcomes",
    [
        ("SATISFIED", "SATISFIED"),
        ("VIOLATED", "SATISFIED"),
        ("UNKNOWN", "SATISFIED"),
        ("UNKNOWN", "VIOLATED"),
    ],
)
def test_control_recomputes_established_verdict_hash_and_order(kind, outcomes):
    args, expected = control(kind, outcomes)
    before = deepcopy(args)
    result = run(args).data
    assert canonical_json(result["results"]["control"]["value"]) == canonical_json(
        asdict(expected)
    )
    assert result["history_authenticated"] is False
    assert args == before
    args["inputs"]["event"]["outputs"]["value"].reverse()
    assert run(args).data["results"] == result["results"]


@pytest.mark.parametrize("kind", ["EPISTEMIC", "AUTHORIZATION"])
@pytest.mark.parametrize(
    "fault",
    [
        "missing",
        "extra",
        "duplicate",
        "monitor_hash",
        "version",
        "head",
        "proposal",
        "requirement_hash",
    ],
)
def test_coverage_checks_actual_values_not_just_array_shapes(kind, fault):
    args, _ = control(kind)
    outputs = args["inputs"]["event"]["outputs"]["value"]
    if fault == "missing":
        outputs.pop()
    elif fault in {"extra", "duplicate"}:
        outputs.append(deepcopy(outputs[0]))
        if fault == "extra":
            outputs[-1]["monitor_id"] = "unrequired"
    elif fault == "requirement_hash":
        args["inputs"]["artifact"]["required"]["value"][0]["monitor_record_hash"] = (
            content_digest("wrong")
        )
    else:
        field = {
            "monitor_hash": "monitor_hash",
            "version": "monitor_version",
            "head": "base_acceptance_head",
            "proposal": "proposal_id",
        }[fault]
        outputs[0][field] = content_digest("wrong")
    before = deepcopy(args)
    with pytest.raises(api().ExecutionRefusal, match="CHECK_COVERAGE"):
        run(args)
    assert args == before


@pytest.mark.parametrize(
    "field",
    [
        "action_proposal_id",
        "action_content_hash",
        "evaluated_actor_id",
        "authority_policy_id",
        "authority_policy_hash",
    ],
)
def test_authority_coverage_binds_each_actual_action_actor_and_policy_field(field):
    args, _ = control("AUTHORIZATION")
    args["inputs"]["event"]["outputs"]["value"][0][field] = content_digest("wrong")
    with pytest.raises(api().ExecutionRefusal, match="CHECK_COVERAGE"):
        run(args)


def test_selection_rechecks_coverage_against_policy_and_not_caller_required_list():
    args, _ = control("EPISTEMIC")
    args["inputs"]["event"]["outputs"]["value"].pop()
    args["inputs"]["artifact"]["required"]["value"].pop()
    args["inputs"]["artifact"]["context"]["value"]["monitors"].pop()
    with pytest.raises(api().ExecutionRefusal, match="INVALID_CONTROL"):
        run(args)


def test_control_requires_declared_capability_not_arbitrary_recipe_or_callback():
    args, _ = control("EPISTEMIC")
    args["program"]["required_capabilities"] = []
    with pytest.raises(api().ExecutionRefusal, match="UNDECLARED_CAPABILITY"):
        run(args)
    args, _ = control("EPISTEMIC")
    args["inputs"]["artifact"]["context"]["value"]["recipe"] = "os.system"
    with pytest.raises(api().ExecutionRefusal, match="UNDECLARED_CAPABILITY"):
        run(args)
