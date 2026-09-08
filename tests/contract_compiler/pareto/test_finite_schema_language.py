"""Finite value schemas cannot enable reference resolution or hidden programs.

Nonlocal references are checked only by definition/selection preflight. No
negative test executes or retrieves a nonlocal schema.
"""

from copy import deepcopy

import pytest

from malleus._contract_pipeline.finite_executor import (
    ExecutionRefusal,
    validate_program_definition,
)
from malleus._contract_pipeline.finite_program import PacketRefusal
from malleus._contract_pipeline.protocol_runtime import (
    ProtocolProgramRefusal,
    load_bundle,
)
from malleus.ledger import content_digest
from research.action_history_contract_freeze.programs.test_executor import neutral, run
from research.action_history_contract_freeze.programs.test_packet_validator import obj
from tests.contract_compiler.pareto.test_finite_protocol_history import (
    canonical,
    specimen,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _anchored_history,
    _evidence_anchor,
)


def validate(args):
    return validate_program_definition(
        args["program"],
        instruction_schema=args["instruction_schema"],
        profile=args["profile"],
    )


@pytest.mark.parametrize("keyword", ["$ref", "$dynamicRef"])
@pytest.mark.parametrize("reference", ["#/missing", "https://example.invalid/schema"])
@pytest.mark.parametrize("position", ["binding", "property", "items"])
def test_schema_references_refuse_at_definition_before_execution(
    keyword, reference, position
):
    args = neutral()
    schema = args["program"]["inputs"]["artifact"]["context"]
    if position == "property":
        schema = schema["properties"]["value"]
    elif position == "items":
        schema["properties"]["extra"] = {"type": "array", "items": {"type": "string"}}
        schema = schema["properties"]["extra"]["items"]
    schema[keyword] = reference
    with pytest.raises(PacketRefusal, match="DEFINITION_SCHEMA"):
        validate(args)


def test_unsupported_schema_applicator_cannot_hide_a_dynamic_reference():
    args = neutral()
    args["program"]["inputs"]["artifact"]["context"]["not"] = {
        "$dynamicRef": "#/missing"
    }
    with pytest.raises(PacketRefusal, match="DEFINITION_SCHEMA"):
        validate(args)


def test_missing_local_dynamic_reference_is_a_typed_pure_execution_refusal():
    args = neutral()
    args["program"]["inputs"]["artifact"]["context"]["$dynamicRef"] = "#/missing"
    before = deepcopy(args)
    with pytest.raises(ExecutionRefusal):
        run(args)
    assert args == before


@pytest.mark.parametrize("reference", ["#/missing", "https://example.invalid/schema"])
def test_owning_bundle_refuses_dynamic_reference_before_selection(reference):
    bundle, _ = specimen()
    bundle["transactions"]["register-pair"]["program"]["inputs"]["event"]["0"][
        "$dynamicRef"
    ] = reference
    with pytest.raises(ProtocolProgramRefusal, match="MALFORMED_PROGRAM"):
        load_bundle(canonical(bundle))


def test_owner_selection_refusal_preserves_exact_ledger_bytes(tmp_path):
    history = _anchored_history(tmp_path)[0]
    bundle, _ = specimen()
    bundle["transactions"]["register-pair"]["program"]["inputs"]["event"]["0"][
        "$dynamicRef"
    ] = "#/missing"
    history.append_anchors(
        anchors=(_evidence_anchor("finite-bundle", canonical(bundle)),),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    before = history.path.read_bytes()
    base = history.replay()
    with pytest.raises(ProtocolProgramRefusal, match="MALFORMED_PROGRAM"):
        history.select_protocol_programs(
            record_id="finite-bundle",
            identity=content_digest(bundle),
            expected_head=base.ledger_head,
            expected_count=base.ledger_event_count,
            event_id="select:1",
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert history.path.read_bytes() == before


@pytest.mark.parametrize("name", ["$ref", "$dynamicRef"])
def test_reference_named_domain_properties_and_constant_values_remain_ordinary_data(
    name,
):
    args = neutral()
    value = {"id": "context:1", name: "ordinary domain text"}
    schema = obj(id={"type": "string"}, **{name: {"type": "string"}})
    schema["const"] = value
    args["program"]["inputs"]["artifact"]["context"] = obj(value=schema)
    args["inputs"]["artifact"]["context"]["value"] = value
    args["inputs"]["event"]["context"]["identity"] = content_digest(value)
    assert run(args).data["runtime_executed"] is True


def test_neutral_control_still_executes():
    assert run(neutral()).data["runtime_executed"] is True
