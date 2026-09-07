"""Executable binding of the already accepted initialization checkpoint.

This authors finite data for the selected profile. It does not initialize a
history, manufacture applied records, or run during append/replay.
"""

from copy import deepcopy
import json

from malleus._contract_pipeline.protocol_runtime import canonical, load_bundle
from research.action_history_contract_freeze.programs.registration_bundle import (
    HERE,
    compare,
    obj,
    ref,
    retention,
)


DEFINITIONS = {
    "profile": "profile_identity",
    "record_contract": "record_contract_identity",
    "machine": "bundle_identity",
    "history_binding": "history_binding_identity",
}
POLICY_TYPES = {
    "epistemic": "EpistemicPolicyArtifact",
    "authorization": "AuthorizationPolicyArtifact",
}
COORDINATES = {
    ("prefix", "head"): ("ledger_head", "HEAD"),
    ("prefix", "event_count"): ("ledger_event_count", "INTEGER"),
    ("domain", "effective_contract_identity"): ("contract_identity", "DIGEST"),
    ("domain", "kcs_acceptance_head"): ("acceptance_head", "HEAD"),
    ("domain", "materialization_head"): ("materialization_head", "HEAD"),
    ("domain", "accepted_graph_digest"): ("graph_state_digest", "DIGEST"),
}


def add_initialization(bundle, *, source_ids, policy_ids):
    if set(source_ids) != set(DEFINITIONS) or set(policy_ids) != set(POLICY_TYPES):
        raise ValueError("every selected source and policy role must be explicit")
    identifiers = [*source_ids.values(), *policy_ids.values()]
    if any(type(i) is not str or not i.strip() for i in identifiers) or len(
        set(identifiers)
    ) != len(identifiers):
        raise ValueError("selected roles require distinct nonblank record IDs")
    bundle = deepcopy(bundle)
    packet = json.loads((HERE / "lifecycle/initialization.json").read_bytes())
    program = deepcopy(bundle["transactions"]["source"]["program"])
    program["name"] = "owner-bound-action-initialization"
    checkpoint = packet["program"]["inputs"]["artifact"]["checkpoint"]["properties"][
        "value"
    ]
    for (group, field), (target, _) in COORDINATES.items():
        program["inputs"]["current"]["context"]["properties"]["value"]["properties"][
            target
        ] = deepcopy(checkpoint["properties"][group]["properties"][field])
    event_schema = program["inputs"]["event"]["0"]["properties"]
    event_schema["retained"] = obj(
        source=retention("SOURCE_ARTIFACT", "CANONICAL_JSON", value=checkpoint)
    )
    event_schema["data"]["properties"]["references"] = obj(
        **{
            name: obj(
                id={"type": "string"},
                record_hash={"type": "string", "format": "sha256"},
            )
            for name in DEFINITIONS
        }
    )
    event_schema["data"]["required"].append("references")
    selected = {
        "sources": source_ids,
        "policies": policy_ids,
        "source_type": "SourceArtifact",
        "policy_types": POLICY_TYPES,
        "singleton": [{"key": "ACTIVE"}],
    }
    selected_schema = obj(
        sources=obj(
            **{k: {"type": "string", "const": v} for k, v in source_ids.items()}
        ),
        policies=obj(
            **{k: {"type": "string", "const": v} for k, v in policy_ids.items()}
        ),
        source_type={"type": "string", "const": "SourceArtifact"},
        policy_types=obj(
            **{k: {"type": "string", "const": v} for k, v in POLICY_TYPES.items()}
        ),
        singleton=packet["program"]["inputs"]["artifact"]["singleton"]["properties"][
            "value"
        ],
    )
    bundle["constants"]["initialization"] = selected
    bundle["transactions"]["initialize"] = {
        "event_types": ["PREREQUISITE_RECORDED"],
        "program": program,
    }
    for transaction in bundle["transactions"].values():
        value = transaction["program"]["inputs"]["artifact"]["constants"]["properties"][
            "value"
        ]
        value["properties"]["initialization"] = deepcopy(selected_schema)
        value["required"].append("initialization")
    program["inputs"]["artifact"]["selection"] = obj(
        value=obj(
            **{
                k: {"type": "string", "format": "sha256"}
                for k in (*DEFINITIONS.values(), "instruction_schema_identity")
            }
        )
    )
    for key in ("targets", "record_schemas"):
        for name, value in packet["profile"][key].items():
            if name in bundle["profile"][key] and value != bundle["profile"][key][name]:
                raise ValueError("conflicting initialization declaration: " + name)
            bundle["profile"][key][name] = deepcopy(value)

    def content(*path):
        return ref("event", "0", "retained", "source", "value", *path)

    def setting(*path):
        return ref("artifact", "constants", "value", "initialization", *path)

    sources = ref(
        "event", "0", "data", "records", "value", 0, "record", "source_record_ids"
    )
    guards = [
        {
            "opcode": "REQUIRE_UNIQUE",
            "records": setting("singleton"),
            "key_paths": [["key"]],
            "target_index": "initialization",
            "refusal": "ALREADY_INITIALIZED",
        }
    ]
    guards.extend(
        compare(
            content(*path),
            ref("current", "context", "value", target),
            "STALE_INITIALIZATION_" + target.upper(),
            kind,
        )
        for path, (target, kind) in COORDINATES.items()
    )
    for name, identity in DEFINITIONS.items():
        guards.extend(
            [
                compare(
                    content(name, "id"), setting("sources", name), "WRONG_DEFINITION_ID"
                ),
                compare(
                    content(name, "bytes_sha256"),
                    ref("artifact", "selection", "value", identity),
                    "WRONG_DEFINITION_BYTES",
                    "DIGEST",
                ),
                compare(
                    content(name, "id"),
                    ref("event", "0", "data", "references", name, "id"),
                    "WRONG_DEFINITION_REFERENCE",
                ),
                {
                    "opcode": "RESOLVE_RECORD",
                    "record_id": content(name, "id"),
                    "record_hash": ref(
                        "event", "0", "data", "references", name, "record_hash"
                    ),
                    "record_type": setting("source_type"),
                    "scope": "APPLIED",
                    "result": "selected-" + name,
                    "refusal": "UNAPPLIED_DEFINITION",
                },
                compare(
                    ref("result", "selected-" + name, "value", "source_content_digest"),
                    content(name, "bytes_sha256"),
                    "MISBOUND_DEFINITION_BYTES",
                    "DIGEST",
                ),
                {
                    "opcode": "REQUIRE_MEMBER",
                    "value_kind": "STRING",
                    "value": content(name, "id"),
                    "members": sources,
                    "refusal": "MISSING_DEFINITION_PROVENANCE",
                },
            ]
        )
    for name in POLICY_TYPES:
        field = name + "_policy"
        guards.extend(
            [
                compare(
                    content(field, "id"),
                    setting("policies", name),
                    "WRONG_SELECTED_POLICY",
                ),
                {
                    "opcode": "RESOLVE_RECORD",
                    "record_id": content(field, "id"),
                    "record_hash": content(field, "record_hash"),
                    "record_type": setting("policy_types", name),
                    "scope": "APPLIED",
                    "result": "selected-" + name,
                    "refusal": "UNAPPLIED_SELECTED_POLICY",
                },
                {
                    "opcode": "REQUIRE_MEMBER",
                    "value_kind": "STRING",
                    "value": content(field, "id"),
                    "members": sources,
                    "refusal": "MISSING_POLICY_PROVENANCE",
                },
            ]
        )
    guards.extend(
        [
            compare(
                content("id"),
                ref("event", "0", "retained", "source", "record_id"),
                "WRONG_CHECKPOINT_ID",
            ),
            {
                "opcode": "HASH",
                "recipe": "VALUE",
                "value": content(),
                "result": "checkpoint-hash",
                "refusal": "INVALID_CHECKPOINT",
            },
            compare(
                ref("result", "checkpoint-hash", "value"),
                ref("event", "0", "retained", "source", "identity"),
                "WRONG_CHECKPOINT_BYTES",
                "DIGEST",
            ),
        ]
    )
    program["steps"] = (
        guards
        + program["steps"]
        + [
            {
                "opcode": "SET_PROTOCOL_STATE",
                "target": "PROTOCOL_INDEX",
                "name": "initialization",
                "keys": [setting("singleton", 0, "key")],
                "value": ref("result", "checkpoint-hash", "value"),
                "refusal": "INVALID_INITIALIZATION_INDEX",
            },
            {
                "opcode": "SET_PROTOCOL_STATE",
                "target": "ACTION_ACCEPTANCE_HEAD",
                "name": "action_head",
                "value": ref("result", "checkpoint-hash", "value"),
                "refusal": "INVALID_INITIAL_ACTION_HEAD",
            },
        ]
    )
    return load_bundle(canonical(bundle))
