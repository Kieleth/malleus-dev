"""Capture an exact current context before grant checks, without authorizing.

The retained prefix precedes this capture event. Later protocol events may
advance that prefix; authority admission must independently recheck A and D.
"""

from copy import deepcopy

from malleus._contract_pipeline.protocol_runtime import canonical, load_bundle
from research.action_history_contract_freeze.programs.assessment_bundle import (
    TEXT,
    DIGEST,
    array,
)
from research.action_history_contract_freeze.programs.initialization_bundle import (
    COORDINATES,
    POLICY_TYPES,
)
from research.action_history_contract_freeze.programs.registration_bundle import (
    compare,
    obj,
    ref,
    retention,
)


def add_current_context(bundle):
    bundle = deepcopy(bundle)
    # Select the exact existing context fields, not a new context grammar.
    original = bundle["transactions"]["type-completed"]["program"]["inputs"]["event"][
        "0"
    ]["properties"]["data"]["properties"]["original"]["properties"]["value"]
    names = (
        "id",
        "prefix",
        "domain",
        "action_acceptance_head",
        "initialization_identity",
        "epistemic_policy",
        "authorization_policy",
    )
    current = obj(**{name: deepcopy(original["properties"][name]) for name in names})
    bundle["profile"]["targets"]["current_contexts"] = {
        "target": "PROTOCOL_INDEX",
        "storage_path": ["protocol", "current_contexts"],
        "key_schemas": [deepcopy(TEXT)],
        "value_schema": deepcopy(DIGEST),
    }
    for transaction in bundle["transactions"].values():
        inputs = transaction["program"]["inputs"]
        if "state" in inputs["current"]:
            inputs["current"]["state"]["properties"]["value"]["properties"]["protocol"][
                "properties"
            ]["current_contexts"] = {
                "type": "array",
                "items": obj(keys=array(TEXT, 1), value=DIGEST),
            }
    program = deepcopy(bundle["transactions"]["source"]["program"])
    program["name"] = "capture-real-current-context"
    program["inputs"]["event"]["0"]["properties"]["retained"] = obj(
        source=retention("SOURCE_ARTIFACT", "CANONICAL_JSON", value=current)
    )
    prior = bundle["transactions"]["type-completed"]["program"]["inputs"]["current"]
    program["inputs"]["current"] = deepcopy(prior)
    indexes = program["inputs"]["current"]["state"]["properties"]["value"][
        "properties"
    ]["protocol"]
    indexes["required"] = ["initialization"]
    indexes["properties"]["initialization"].update(minItems=1, maxItems=1)

    def content(*path):
        return ref("event", "0", "retained", "source", "value", *path)

    def setting(*path):
        return ref("artifact", "constants", "value", "initialization", *path)

    source_ids = ref(
        "event", "0", "data", "records", "value", 0, "record", "source_record_ids"
    )
    guards = [
        compare(
            content(*path),
            ref("current", "context", "value", target),
            "STALE_CURRENT_CONTEXT",
            kind,
        )
        for path, (target, kind) in COORDINATES.items()
    ]
    guards += [
        compare(
            content("action_acceptance_head"),
            ref("current", "context", "value", "action_acceptance_head"),
            "STALE_CURRENT_ACTION",
            "HEAD",
        ),
        compare(
            content("initialization_identity"),
            ref("current", "state", "value", "protocol", "initialization", 0, "value"),
            "WRONG_CURRENT_INITIALIZATION",
            "DIGEST",
        ),
        compare(
            content("id"),
            ref("event", "0", "retained", "source", "record_id"),
            "WRONG_CURRENT_RECORD_ID",
        ),
    ]
    for name in POLICY_TYPES:
        field = name + "_policy"
        guards += [
            compare(
                content(field, "id"), setting("policies", name), "WRONG_CURRENT_POLICY"
            ),
            {
                "opcode": "RESOLVE_RECORD",
                "record_id": content(field, "id"),
                "record_hash": content(field, "record_hash"),
                "record_type": setting("policy_types", name),
                "scope": "APPLIED",
                "result": "selected-" + name,
                "refusal": "WRONG_CURRENT_POLICY",
            },
            {
                "opcode": "REQUIRE_MEMBER",
                "value_kind": "STRING",
                "value": content(field, "id"),
                "members": source_ids,
                "refusal": "MISSING_CURRENT_POLICY_PROVENANCE",
            },
        ]
    # Preserve every existing source hash, record and retention check.
    program["steps"] = (
        guards
        + program["steps"]
        + [
            {
                "opcode": "SET_PROTOCOL_STATE",
                "target": "PROTOCOL_INDEX",
                "name": "current_contexts",
                "keys": [content("id")],
                "value": ref("event", "0", "retained", "source", "identity"),
                "refusal": "INVALID_CURRENT_CONTEXT_INDEX",
            },
        ]
    )
    bundle["transactions"]["capture-current"] = {
        "event_types": ["PREREQUISITE_RECORDED"],
        "program": program,
    }
    return load_bundle(canonical(bundle))
