"""Author dispatch eligibility as finite data, never invoke an effect adapter."""

from copy import deepcopy
import json

from malleus._contract_pipeline.protocol_runtime import (
    canonical,
    digest,
    load_bundle,
    raw,
)
from research.action_history_contract_freeze.programs.assessment_bundle import (
    TEXT,
    DIGEST,
    array,
)
from research.action_history_contract_freeze.programs.initialization_bundle import (
    COORDINATES,
)
from research.action_history_contract_freeze.programs.registration_bundle import (
    HERE,
    obj,
    ref,
    compare,
    owner_header,
)


def supplied(*path):
    return ref("event", "0", "data", *path)


def record(*path):
    return supplied("records", "value", 0, "record", *path)


def resolved(name, *path):
    return ref("result", name, "value", *path)


def state(name, *path):
    return ref("current", "state", "value", "protocol", name, *path)


def compare_time(left, right, comparison, reason):
    return {**compare(left, right, reason, "INSTANT"), "comparison": comparison}


def add_record_stage(bundle, name, kind, schema, *, role, references, indexes):
    """Generate shared full-record/header checks, not runtime policy branches."""
    bundle["profile"]["record_schemas"][kind] = deepcopy(schema)
    constants = {
        "contract": {
            "contract_identity": digest(raw(bundle["record_contract_base64"])),
            "record_type": kind,
        },
        "role": role,
        "types": references,
    }
    cs = obj(
        contract=obj(contract_identity=DIGEST, record_type={**TEXT, "const": kind}),
        role={**TEXT, "const": role},
        types=obj(**{k: {**TEXT, "const": v} for k, v in references.items()}),
    )
    bundle["constants"][name] = constants
    for key, key_count in indexes.items():
        bundle["profile"]["targets"][key] = {
            "target": "PROTOCOL_INDEX",
            "storage_path": ["protocol", key],
            "key_schemas": [deepcopy(TEXT) for _ in range(key_count)],
            "value_schema": deepcopy(TEXT),
        }
    for transaction in bundle["transactions"].values():
        inputs = transaction["program"]["inputs"]
        container = inputs["artifact"]["constants"]["properties"]["value"]
        container["properties"][name] = deepcopy(cs)
        container["required"].append(name)
        if "state" in inputs["current"]:
            props = inputs["current"]["state"]["properties"]["value"]["properties"][
                "protocol"
            ]["properties"]
            for key, key_count in indexes.items():
                props[key] = {
                    "type": "array",
                    "items": obj(keys=array(TEXT, key_count), value=TEXT),
                }
    inputs = deepcopy(
        bundle["transactions"]["authority-completed"]["program"]["inputs"]
    )
    inputs["current"]["state"]["properties"]["value"]["properties"]["protocol"][
        "required"
    ] = []
    inputs["event"] = {
        "0": obj(
            header=owner_header(),
            data=obj(
                records=obj(
                    value=array(
                        obj(record_type={**TEXT, "const": kind}, record=schema), 1
                    )
                ),
                dependencies=obj(
                    value={"type": "array", "items": TEXT, "uniqueItems": True}
                ),
            ),
            retained=obj(),
        )
    }

    def setting(*path):
        return ref("artifact", "constants", "value", name, *path)

    steps = [
        {
            "opcode": "VALIDATE_RECORD",
            "record": record(),
            "contract": setting("contract"),
            "result": "checked",
            "refusal": "INVALID_" + name.upper() + "_RECORD",
        },
        {
            "opcode": "HASH",
            "recipe": "RECORD",
            "value": record(),
            "record_type": supplied("records", "value", 0, "record_type"),
            "result": "record-hash",
            "refusal": "INVALID_RECORD_HASH",
        },
        compare(
            record("content_hash"),
            resolved("record-hash"),
            "WRONG_RECORD_HASH",
            "DIGEST",
        ),
        compare(record("responsible_role"), setting("role"), "WRONG_RECORD_ROLE"),
    ]
    for field, header in (
        ("generation_event_id", "event_id"),
        ("generated_at", "transaction_time"),
        ("responsible_actor_id", "actor_id"),
    ):
        steps.append(
            compare(
                record(field),
                ref("event", "0", "header", header),
                "MISBOUND_RECORD_METADATA",
            )
        )
    return inputs, steps, setting


def resolve_step(name, identifier, identity, setting):
    return {
        "opcode": "RESOLVE_RECORD",
        "scope": "APPLIED",
        "record_id": identifier,
        "record_hash": identity,
        "record_type": setting("types", name),
        "result": name,
        "refusal": "UNAPPLIED_" + name.upper(),
    }


def require_indexes(inputs, names):
    indexes = inputs["current"]["state"]["properties"]["value"]["properties"][
        "protocol"
    ]
    indexes["required"] = list(names)
    for name in names:
        indexes["properties"][name].update(minItems=1, maxItems=1)


def introduction(index, fields):
    return [
        {
            "opcode": "REQUIRE_UNIQUE",
            "records": supplied("records", "value"),
            "key_paths": [["record", field] for field in fields],
            "target_index": index,
            "refusal": "DUPLICATE_" + index.upper(),
        },
        {
            "opcode": "INTRODUCE_RECORDS",
            "records": supplied("records", "value"),
            "dependencies": supplied("dependencies", "value"),
            "result": "introduced",
            "refusal": "INVALID_RECORD_INTRODUCTION",
        },
        {
            "opcode": "SET_PROTOCOL_STATE",
            "target": "PROTOCOL_INDEX",
            "name": index,
            "keys": [record(field) for field in fields],
            "value": record("id"),
            "refusal": "INVALID_RECORD_INDEX",
        },
    ]


def add_dispatch(bundle):
    bundle = deepcopy(bundle)
    specimen = json.loads((HERE / "lifecycle/execution.json").read_bytes())
    schema = deepcopy(specimen["profile"]["record_schemas"]["ActionDispatch"])
    schema["properties"]["source_record_ids"].update(
        uniqueItems=True, minItems=2, maxItems=2
    )
    for field in ("executor_id", "dispatch_adapter_id"):
        schema["properties"][field]["format"] = "nonblank"
    inputs, steps, setting = add_record_stage(
        bundle,
        "dispatch",
        "ActionDispatch",
        schema,
        role="dispatcher",
        references={
            "action": "LocalAction",
            "permission": "AuthorizationDecision",
            "context": "SourceArtifact",
        },
        indexes={"dispatch_by_action": 1},
    )
    context = bundle["transactions"]["capture-current"]["program"]["inputs"]["event"][
        "0"
    ]["properties"]["retained"]["properties"]["source"]["properties"]["value"]
    data = inputs["event"]["0"]["properties"]["data"]
    data["properties"]["context"] = obj(
        id=TEXT, record_hash=DIGEST, value=deepcopy(context)
    )
    data["required"].append("context")
    require_indexes(
        inputs, ("authorization_states", "authorization_decisions", "current_contexts")
    )
    # State precedes resolution: BLOCK and CLARIFY are not dispatch variants.
    permission_state = inputs["current"]["state"]["properties"]["value"]["properties"][
        "protocol"
    ]["properties"]["authorization_states"]["items"]["properties"]["value"]
    permission_state["const"] = "AUTHORIZED"
    steps += [
        compare(
            state("authorization_states", 0, "keys", 0),
            record("action_proposal_id"),
            "UNAUTHORIZED_ACTION",
        ),
        compare(
            state("authorization_decisions", 0, "keys", 0),
            record("action_proposal_id"),
            "UNAUTHORIZED_ACTION",
        ),
        compare(
            state("authorization_decisions", 0, "value"),
            record("authorization_decision_id"),
            "UNAPPLIED_PERMISSION",
        ),
        resolve_step(
            "action",
            record("action_proposal_id"),
            record("action_content_hash"),
            setting,
        ),
        resolve_step(
            "permission",
            record("authorization_decision_id"),
            record("authorization_decision_hash"),
            setting,
        ),
        resolve_step(
            "context",
            supplied("context", "id"),
            supplied("context", "record_hash"),
            setting,
        ),
    ]

    def content(*path):
        return supplied("context", "value", *path)

    steps += [
        {
            "opcode": "HASH",
            "recipe": "VALUE",
            "value": content(),
            "result": "context-hash",
            "refusal": "INVALID_DISPATCH_CONTEXT",
        },
        compare(
            resolved("context-hash"),
            resolved("context", "source_content_digest"),
            "FORGED_DISPATCH_CONTEXT",
            "DIGEST",
        ),
        compare(content("id"), resolved("context", "id"), "WRONG_DISPATCH_CONTEXT"),
        compare(
            state("current_contexts", 0, "keys", 0),
            resolved("context", "id"),
            "UNVERIFIED_DISPATCH_CONTEXT",
        ),
        compare(
            state("current_contexts", 0, "value"),
            resolved("context-hash"),
            "UNVERIFIED_DISPATCH_CONTEXT",
            "DIGEST",
        ),
    ]
    for path, (target, kind) in COORDINATES.items():
        if path[0] == "domain":
            steps.append(
                compare(
                    content(*path),
                    ref("current", "context", "value", target),
                    "STALE_DISPATCH_DOMAIN",
                    kind,
                )
            )
    for left in (
        content("action_acceptance_head"),
        record("base_acceptance_head"),
        resolved("permission", "base_acceptance_head"),
    ):
        steps.append(
            compare(
                left,
                ref("current", "context", "value", "action_acceptance_head"),
                "STALE_DISPATCH_ACTION",
                "HEAD",
            )
        )
    for field, target, kind in (
        ("action_proposal_id", "action_proposal_id", "STRING"),
        ("action_content_hash", "action_content_hash", "DIGEST"),
        ("executor_id", "authorized_actor_id", "STRING"),
    ):
        steps.append(
            compare(
                record(field),
                resolved("permission", target),
                "MISBOUND_DISPATCH_PERMISSION",
                kind,
            )
        )
    steps += [
        compare_time(
            record("dispatched_at"), record("generated_at"), "EQ", "WRONG_DISPATCH_TIME"
        ),
        compare_time(
            resolved("permission", "authorization_valid_from"),
            record("dispatched_at"),
            "LE",
            "DISPATCH_BEFORE_PERMISSION",
        ),
        compare_time(
            record("dispatched_at"),
            resolved("permission", "authorization_valid_to"),
            "LT",
            "DISPATCH_PERMISSION_EXPIRED",
        ),
    ]
    for name in ("action", "permission"):
        steps.append(
            {
                "opcode": "REQUIRE_MEMBER",
                "value_kind": "STRING",
                "value": resolved(name, "id"),
                "members": record("source_record_ids"),
                "refusal": "MISSING_DISPATCH_SOURCE",
            }
        )
    steps += introduction("dispatch_by_action", ("action_proposal_id",))
    bundle["transactions"]["dispatch"] = {
        "event_types": ["ACTION_DISPATCHED"],
        "program": {
            "name": "dispatch-eligible-action",
            "inputs": inputs,
            "required_capabilities": [],
            "introductions": [{"name": "dispatch", "depends_on": []}],
            "steps": steps,
        },
    }
    return load_bundle(canonical(bundle))
