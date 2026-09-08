"""Bind the accepted atomic pair to owner state and retained input identities.

Authors data only. LocalAction remains the neutral conformance record variant;
this does not define supplier, robot or other domain action semantics.
"""

from copy import deepcopy
import json

from malleus._contract_pipeline.protocol_runtime import (
    canonical,
    load_bundle,
    raw,
    digest,
)
from research.action_history_contract_freeze.programs.initialization_bundle import (
    COORDINATES,
)
from research.action_history_contract_freeze.programs.registration_bundle import (
    HERE,
    compare,
    obj,
    ref,
    retention,
    owner_header,
    owner_context,
)


ROLES = ("goal", "preservation", "mapping", "pre_state_source")


def add_context_proposal(bundle):
    bundle = deepcopy(bundle)
    packet = json.loads((HERE / "lifecycle/context-proposal.json").read_bytes())
    program = deepcopy(packet["program"])
    source = bundle["transactions"]["source"]["program"]
    inputs = program["inputs"]
    # This fixed literal already excludes blanks. Preserve that refinement
    # when the later permission program compares it with nonblank grant items.
    inputs["event"]["action"]["properties"]["value"]["items"]["properties"]["record"][
        "properties"
    ]["action_type"]["format"] = "nonblank"
    constants_schema = {
        k: deepcopy(v) for k, v in inputs["artifact"].items() if k != "retention"
    }
    constants = {
        "constants": {
            k: v["const"]
            for k, v in constants_schema["constants"]["properties"].items()
        }
    }
    for name in ("context", "action", "proposal"):
        key = name + "_contract"
        constants[key] = {
            "value": {
                "contract_identity": digest(raw(bundle["record_contract_base64"])),
                "record_type": constants_schema[key]["properties"]["value"][
                    "properties"
                ]["record_type"]["const"],
            }
        }
    bundle["constants"]["proposal"] = constants
    for key in ("targets", "record_schemas"):
        for name, value in packet["profile"][key].items():
            if name in bundle["profile"][key] and bundle["profile"][key][name] != value:
                raise ValueError("conflicting proposal declaration: " + name)
            bundle["profile"][key][name] = deepcopy(value)

    # This is the same finite source-registration contract, without its final
    # introduction. The atomic pair introduces context before action/proposal.
    assert source["steps"][-1]["opcode"] == "INTRODUCE_RECORDS"
    source_guards = deepcopy(source["steps"][:-1])
    data = deepcopy(source["inputs"]["event"]["0"]["properties"]["data"])
    checkpoint = deepcopy(
        bundle["transactions"]["initialize"]["program"]["inputs"]["event"]["0"][
            "properties"
        ]["retained"]["properties"]["source"]["properties"]["value"]
    )
    reference = obj(
        id={"type": "string"}, record_hash={"type": "string", "format": "sha256"}
    )
    data["properties"].update(
        initialization=obj(
            value=checkpoint, record_hash={"type": "string", "format": "sha256"}
        ),
        references=obj(**{k: deepcopy(reference) for k in ROLES}),
    )
    data["required"] += ["initialization", "references"]
    original = inputs["original"]["context"]["properties"]["value"]
    current = owner_context()
    for (group, field), (target, _) in COORDINATES.items():
        current["properties"]["value"]["properties"][target] = deepcopy(
            original["properties"][group]["properties"][field]
        )
    current["properties"]["value"]["properties"]["action_acceptance_head"] = deepcopy(
        original["properties"]["action_acceptance_head"]
    )
    state_indexes = {}
    for name, target in bundle["profile"]["targets"].items():
        if target["target"] == "PROTOCOL_INDEX":
            if len(target["key_schemas"]) != 1:
                raise ValueError("this conformance profile requires single-key indexes")
            state_indexes[name] = {
                "type": "array",
                "items": obj(
                    keys={
                        "type": "array",
                        "items": deepcopy(target["key_schemas"][0]),
                        "minItems": 1,
                        "maxItems": 1,
                    },
                    value=deepcopy(target["value_schema"]),
                ),
            }
    state_indexes["initialization"].update(minItems=1, maxItems=1)
    state_indexes["initialization"]["items"]["properties"]["keys"]["items"]["const"] = (
        "ACTIVE"
    )
    protocol = obj(**state_indexes)
    protocol["required"] = ["initialization"]
    program["inputs"] = {
        "event": {
            "0": obj(
                header=owner_header(),
                data=data,
                retained=obj(
                    source=retention(
                        "SOURCE_ARTIFACT", "CANONICAL_JSON", value=original
                    )
                ),
            ),
            "1": obj(
                header=owner_header(),
                data=obj(
                    **{
                        k: deepcopy(inputs["event"][k])
                        for k in (
                            "action",
                            "proposal",
                            "action_dependencies",
                            "proposal_dependencies",
                        )
                    }
                ),
                retained=obj(),
            ),
        },
        "current": {
            "context": current,
            "state": obj(
                value=obj(
                    protocol=protocol,
                    action_acceptance_head={"type": "string", "format": "ledger-head"},
                )
            ),
        },
        "artifact": deepcopy(source["inputs"]["artifact"]),
    }
    for transaction in [*bundle["transactions"].values(), {"program": program}]:
        schema = transaction["program"]["inputs"]["artifact"]["constants"][
            "properties"
        ]["value"]
        schema["properties"]["proposal"] = obj(**deepcopy(constants_schema))
        schema["required"].append("proposal")

    def bind(value):
        if type(value) is list:
            return [bind(v) for v in value]
        if type(value) is not dict:
            return value
        if set(value) != {"root", "name", "path"} or value["root"] == "result":
            return {k: bind(v) for k, v in value.items()}
        root, name, path = value["root"], value["name"], value["path"]
        if root == "event":
            if name in ("context_header", "proposal_header"):
                return ref(
                    "event", "0" if name == "context_header" else "1", "header", *path
                )
            if name in ("context", "context_dependencies"):
                return ref(
                    "event",
                    "0",
                    "data",
                    "records" if name == "context" else "dependencies",
                    *path,
                )
            return ref("event", "1", "data", name, *path)
        if root == "original":
            return ref("event", "0", "retained", "source", *path)
        if root == "artifact":
            if name == "retention":
                return ref(
                    "event",
                    "0",
                    "retained",
                    "source",
                    "identity" if path == ["bytes_sha256"] else "byte_length",
                )
            return ref("artifact", "constants", "value", "proposal", name, *path)
        if root == "current":
            if tuple(path) in COORDINATES:
                return ref("current", "context", "value", COORDINATES[tuple(path)][0])
            if path == ["action_acceptance_head"]:
                return ref("current", "context", "value", *path)
            if path == ["initialization_identity"]:
                return ref(
                    "current",
                    "state",
                    "value",
                    "protocol",
                    "initialization",
                    0,
                    "value",
                )
            if path[0] in ("epistemic_policy", "authorization_policy"):
                return ref("event", "0", "data", "initialization", "value", *path)
        raise ValueError("unbound proposal input: " + str(value))

    def content(*path):
        return ref("event", "0", "retained", "source", "value", *path)

    def checkpoint_ref(*path):
        return ref("event", "0", "data", "initialization", "value", *path)

    source_type = ref(
        "artifact", "constants", "value", "proposal", "constants", "source_type"
    )
    guards = [
        {
            "opcode": "HASH",
            "recipe": "VALUE",
            "value": checkpoint_ref(),
            "result": "initialized-checkpoint-hash",
            "refusal": "INVALID_INITIALIZATION_CONTENT",
        },
        compare(
            ref("result", "initialized-checkpoint-hash", "value"),
            ref("current", "state", "value", "protocol", "initialization", 0, "value"),
            "UNAPPLIED_INITIALIZATION_CONTENT",
            "DIGEST",
        ),
        {
            "opcode": "RESOLVE_RECORD",
            "record_id": checkpoint_ref("id"),
            "record_hash": ref("event", "0", "data", "initialization", "record_hash"),
            "record_type": source_type,
            "scope": "APPLIED",
            "result": "initialization-source",
            "refusal": "UNAPPLIED_INITIALIZATION_SOURCE",
        },
        compare(
            ref("result", "initialization-source", "value", "source_content_digest"),
            ref("result", "initialized-checkpoint-hash", "value"),
            "MISBOUND_INITIALIZATION_SOURCE",
            "DIGEST",
        ),
    ]
    for name in ROLES:
        guards += [
            compare(
                content(name, "id"),
                ref("event", "0", "data", "references", name, "id"),
                "MISBOUND_CONTEXT_SOURCE_ID",
            ),
            {
                "opcode": "RESOLVE_RECORD",
                "record_id": content(name, "id"),
                "record_hash": ref(
                    "event", "0", "data", "references", name, "record_hash"
                ),
                "record_type": source_type,
                "scope": "APPLIED",
                "result": "source-" + name,
                "refusal": "UNAPPLIED_CONTEXT_SOURCE",
            },
            compare(
                content(name, "bytes_sha256"),
                ref("result", "source-" + name, "value", "source_content_digest"),
                "MISBOUND_CONTEXT_SOURCE_BYTES",
                "DIGEST",
            ),
        ]
    for identifier in [checkpoint_ref("id"), *(content(k, "id") for k in ROLES)]:
        guards.append(
            {
                "opcode": "REQUIRE_MEMBER",
                "value_kind": "STRING",
                "value": identifier,
                "members": ref(
                    "event",
                    "0",
                    "data",
                    "records",
                    "value",
                    0,
                    "record",
                    "source_record_ids",
                ),
                "refusal": "MISSING_CONTEXT_PROVENANCE",
            }
        )
    program["steps"] = guards + source_guards + bind(program["steps"])
    program["name"] = "owner-bound-context-proposal"
    bundle["transactions"]["context-proposal"] = {
        "event_types": ["ARTIFACT_RECORDED", "PROPOSAL_RECORDED"],
        "program": program,
    }
    return load_bundle(canonical(bundle))
