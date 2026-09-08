"""Finite terminal receipt admission, with exact retained result bytes."""

from copy import deepcopy
import json

from malleus._contract_pipeline.protocol_runtime import canonical, load_bundle
from research.action_history_contract_freeze.programs.dispatch_bundle import (
    add_record_stage,
    record,
    resolved,
    state,
    resolve_step,
    require_indexes,
    compare_time,
    introduction,
)
from research.action_history_contract_freeze.programs.registration_bundle import (
    HERE,
    obj,
    ref,
    compare,
    retention,
)


def add_execution(bundle):
    bundle = deepcopy(bundle)
    specimen = json.loads((HERE / "lifecycle/execution.json").read_bytes())
    schema = deepcopy(
        specimen["program"]["inputs"]["event"]["records"]["properties"]["value"][
            "items"
        ]["properties"]["record"]
    )
    schema["properties"]["source_record_ids"].update(
        uniqueItems=True, minItems=1, maxItems=1
    )
    schema["properties"]["executor_id"]["format"] = "nonblank"
    inputs, steps, setting = add_record_stage(
        bundle,
        "execution",
        "ActionExecution",
        schema,
        role="executor",
        references={"dispatch": "ActionDispatch"},
        indexes={"execution_by_dispatch": 1},
    )
    inputs["event"]["0"]["properties"]["retained"] = obj(
        result=retention("RETAINED_EVIDENCE")
    )
    require_indexes(inputs, ("dispatch_by_action",))
    steps += [
        resolve_step(
            "dispatch", record("dispatch_id"), record("dispatch_hash"), setting
        ),
        compare(
            state("dispatch_by_action", 0, "keys", 0),
            resolved("dispatch", "action_proposal_id"),
            "UNAPPLIED_DISPATCH",
        ),
        compare(
            state("dispatch_by_action", 0, "value"),
            resolved("dispatch", "id"),
            "UNAPPLIED_DISPATCH",
        ),
        compare(
            record("executor_id"), resolved("dispatch", "executor_id"), "WRONG_EXECUTOR"
        ),
        compare(
            record("executor_id"),
            record("responsible_actor_id"),
            "EXECUTOR_MUST_RECORD",
        ),
        compare_time(
            resolved("dispatch", "dispatched_at"),
            record("execution_started_at"),
            "LE",
            "EXECUTION_BEFORE_DISPATCH",
        ),
        compare_time(
            record("execution_started_at"),
            record("execution_ended_at"),
            "LT",
            "INVALID_EXECUTION_INTERVAL",
        ),
        compare_time(
            record("execution_ended_at"),
            record("generated_at"),
            "EQ",
            "WRONG_EXECUTION_EVENT_TIME",
        ),
        compare(
            record("source_record_ids", 0),
            resolved("dispatch", "id"),
            "MISSING_DISPATCH_SOURCE",
        ),
        compare(
            record("id"),
            ref("event", "0", "retained", "result", "record_id"),
            "MISBOUND_EXECUTION_RETENTION",
        ),
        compare(
            record("execution_result_hash"),
            ref("event", "0", "retained", "result", "identity"),
            "WRONG_EXECUTION_RESULT_BYTES",
            "DIGEST",
        ),
    ]
    steps += introduction("execution_by_dispatch", ("dispatch_id",))
    bundle["transactions"]["execution"] = {
        "event_types": ["ACTION_EXECUTED"],
        "program": {
            "name": "record-terminal-execution",
            "inputs": inputs,
            "required_capabilities": [],
            "introductions": [{"name": "execution", "depends_on": []}],
            "steps": steps,
        },
    }
    return load_bundle(canonical(bundle))
