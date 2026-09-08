"""Author an optional sequential profile using existing finite instructions.

This module transforms declarations, never a running history. Original indexes
remain cumulative. Separate current pointers support the existing literal-path
instruction set. Append and replay import no authoring module.
"""

from copy import deepcopy

from research.action_history_contract_freeze.programs.registration_bundle import (
    compare,
    obj,
    ref,
)


TEXT = {"type": "string"}


def _constant(name):
    return ref("artifact", "constants", "value", "sequential", name)


def _target(name, value_schema):
    return {
        "target": "PROTOCOL_INDEX",
        "storage_path": ["protocol", name],
        "key_schemas": [deepcopy(TEXT)],
        "value_schema": deepcopy(value_schema),
    }


def _index(value_schema, count):
    return {
        "type": "array",
        "items": obj(
            keys={"type": "array", "items": TEXT, "minItems": 1, "maxItems": 1},
            value=deepcopy(value_schema),
        ),
        "minItems": count,
        "maxItems": count,
    }


def _set(name, key, value):
    return {
        "opcode": "SET_PROTOCOL_STATE",
        "target": "PROTOCOL_INDEX",
        "name": name,
        "keys": [key],
        "value": value,
        "refusal": "INVALID_SEQUENTIAL_POINTER",
    }


def with_current_indexes(original, selectors):
    """Mirror declared indexes, selecting a fixed slot or a declared key position.

    ``None`` selects one CURRENT slot. Assessment indexes select their monitor
    key so the reference profile still has exactly two current monitor outputs.
    This is authoring data, not a keyed lookup or new runtime instruction.
    """
    bundle = deepcopy(original)
    targets = bundle["profile"]["targets"]
    mirrors = {}
    for name in selectors:
        declaration = targets[name]
        fields = {
            **{
                f"key_{i}": schema
                for i, schema in enumerate(declaration["key_schemas"])
            },
            "value": declaration["value_schema"],
        }
        mirrors[name] = fields
        for field, schema in fields.items():
            target = f"current_{name}_{field}"
            targets[target] = _target(target, schema)

    def rewrite(value):
        if type(value) is list:
            return [rewrite(item) for item in value]
        if type(value) is not dict:
            return value
        if set(value) == {"root", "name", "path"}:
            path = value["path"]
            if (value["root"], value["name"]) == ("current", "state") and (
                len(path) >= 5
                and path[:2] == ["value", "protocol"]
                and path[2] in selectors
            ):
                field = f"key_{path[5]}" if path[4] == "keys" else "value"
                end = 6 if path[4] == "keys" else 5
                return {
                    **value,
                    "path": [
                        "value",
                        "protocol",
                        f"current_{path[2]}_{field}",
                        path[3],
                        "value",
                        *path[end:],
                    ],
                }
        return {key: rewrite(item) for key, item in value.items()}

    bundle["constants"]["sequential"] = {
        "slot": "CURRENT",
        "ready": "READY",
        "active": "ACTIVE",
        "payload_type": "SourceArtifact",
        "dispatch_type": "ActionDispatch",
    }
    constants = obj(
        **{
            name: {**TEXT, "const": value}
            for name, value in bundle["constants"]["sequential"].items()
        }
    )
    for transaction in bundle["transactions"].values():
        program = transaction["program"]
        inputs = program["inputs"]
        if "artifact" not in inputs:
            inputs["artifact"] = {"constants": obj(value=obj())}
        cs = inputs["artifact"]["constants"]["properties"]["value"]
        cs["properties"]["sequential"] = deepcopy(constants)
        cs["required"].append("sequential")
        if "state" in inputs.get("current", {}):
            state = inputs["current"]["state"]["properties"]["value"]["properties"][
                "protocol"
            ]
            for name, fields in mirrors.items():
                required = name in state["required"]
                count = 1 if selectors[name] is None else 2
                prior = (
                    deepcopy(state["properties"][name])
                    if name in state["properties"]
                    else None
                )
                for field, schema in fields.items():
                    target = f"current_{name}_{field}"
                    if field == "value" and prior is not None:
                        schema = prior["items"]["properties"]["value"]
                    state["properties"][target] = _index(schema, count)
                    state["properties"][target]["minItems"] = (
                        state["properties"][name].get("minItems", 0)
                        if name in state["properties"]
                        else 0
                    )
                    if required:
                        state["required"].append(target)
                if name in state["properties"]:
                    state["properties"][name].pop("maxItems", None)
                    state["properties"][name]["items"]["properties"]["value"] = (
                        deepcopy(targets[name]["value_schema"])
                    )
        steps = []
        for step in program["steps"]:
            steps.append(rewrite(step))
            if step["opcode"] == "SET_PROTOCOL_STATE" and step["name"] in selectors:
                name = step["name"]
                position = selectors[name]
                key = _constant("slot") if position is None else step["keys"][position]
                for field in mirrors[name]:
                    value = (
                        step["value"]
                        if field == "value"
                        else step["keys"][int(field[4:])]
                    )
                    steps.append(_set(f"current_{name}_{field}", key, value))
        program["steps"] = steps
    return bundle


def add_sequential_actions(original):
    """One observed action at a time, with retained payload-byte identity."""
    selectors = {
        name: {"type_assessments": 1, "authority_assessments": 3}.get(name)
        for name, declaration in original["profile"]["targets"].items()
        if declaration["target"] == "PROTOCOL_INDEX" and name != "initialization"
    }
    bundle = with_current_indexes(original, selectors)
    bundle["profile"]["targets"]["episode_phase"] = _target("episode_phase", TEXT)
    for transaction in bundle["transactions"].values():
        inputs = transaction["program"]["inputs"]
        if "state" in inputs.get("current", {}):
            state = inputs["current"]["state"]["properties"]["value"]["properties"][
                "protocol"
            ]
            state["properties"]["episode_phase"] = _index(TEXT, 1)
    for name, phase in (
        ("initialize", "ready"),
        ("context-proposal", "active"),
        ("observation", "ready"),
    ):
        program = bundle["transactions"][name]["program"]
        program["steps"].append(
            _set("episode_phase", _constant("slot"), _constant(phase))
        )
    program = bundle["transactions"]["context-proposal"]["program"]
    state = program["inputs"]["current"]["state"]["properties"]["value"]["properties"][
        "protocol"
    ]
    state["required"].append("episode_phase")
    payload = obj(id=TEXT, record_hash={**TEXT, "format": "sha256"})
    data = program["inputs"]["event"]["1"]["properties"]["data"]
    data["properties"]["payload"] = payload
    data["required"].append("payload")

    def action(*path):
        return ref("event", "1", "data", "action", "value", 0, "record", *path)

    program["steps"][:0] = [
        compare(
            ref("current", "state", "value", "protocol", "episode_phase", 0, "value"),
            _constant("ready"),
            "PREVIOUS_ACTION_NOT_OBSERVED",
        ),
        {
            "opcode": "RESOLVE_RECORD",
            "record_id": ref("event", "1", "data", "payload", "id"),
            "record_hash": ref("event", "1", "data", "payload", "record_hash"),
            "record_type": _constant("payload_type"),
            "scope": "APPLIED",
            "result": "action-payload",
            "refusal": "UNAPPLIED_ACTION_PAYLOAD",
        },
        compare(
            action("action_payload_hash"),
            ref("result", "action-payload", "value", "source_content_digest"),
            "ACTION_PAYLOAD_BYTES_MISMATCH",
            "DIGEST",
        ),
        {
            "opcode": "REQUIRE_MEMBER",
            "value_kind": "STRING",
            "value": ref("event", "1", "data", "payload", "id"),
            "members": action("source_record_ids"),
            "refusal": "ACTION_PAYLOAD_PROVENANCE_MISSING",
        },
    ]
    observation = bundle["transactions"]["observation"]["program"]
    state = observation["inputs"]["current"]["state"]["properties"]["value"][
        "properties"
    ]["protocol"]
    state["required"].extend(["episode_phase", "current_action_to_proposal_key_0"])
    state["properties"]["current_action_to_proposal_key_0"]["minItems"] = 1
    at = (
        next(
            i
            for i, step in enumerate(observation["steps"])
            if step["opcode"] == "RESOLVE_RECORD" and step["result"] == "execution"
        )
        + 1
    )
    observation["steps"][at:at] = [
        compare(
            ref("current", "state", "value", "protocol", "episode_phase", 0, "value"),
            _constant("active"),
            "NO_ACTIVE_ACTION",
        ),
        {
            "opcode": "RESOLVE_RECORD",
            "scope": "APPLIED",
            "record_id": ref("result", "execution", "value", "dispatch_id"),
            "record_hash": ref("result", "execution", "value", "dispatch_hash"),
            "record_type": _constant("dispatch_type"),
            "result": "observed-dispatch",
            "refusal": "UNAPPLIED_OBSERVED_DISPATCH",
        },
        compare(
            ref("result", "observed-dispatch", "value", "action_proposal_id"),
            ref(
                "current",
                "state",
                "value",
                "protocol",
                "current_action_to_proposal_key_0",
                0,
                "value",
            ),
            "OBSERVATION_NOT_CURRENT_ACTION",
        ),
    ]
    return bundle
