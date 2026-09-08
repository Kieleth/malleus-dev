"""Bind the existing finite registration definitions to owner input frames.

Research authoring only. The result is data, retained and executed by Core.
Neither this builder nor a research import runs during append or replay.
The two-input/two-monitor arities remain this explicit conformance variant.
"""

from base64 import b64encode
from copy import deepcopy
import json
from pathlib import Path

from malleus._contract_pipeline.protocol_runtime import canonical, digest, load_bundle


HERE = Path(__file__).parent
SOURCE_PROJECTION = {
    "source_schema_version": "source_schema_version",
    "artifact_id": "id",
    "artifact_version": "artifact_version",
    "source_content_digest": "source_content_digest",
    "source_byte_length": "source_byte_length",
    "source_media_type": "source_media_type",
    "source_locator": "source_locator",
}


def obj(**properties):
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def ref(root, name, *path):
    return {"root": root, "name": name, "path": list(path)}


def compare(left, right, reason, kind="STRING"):
    return {
        "opcode": "REQUIRE_COMPARE",
        "comparison": "EQ",
        "value_kind": kind,
        "left": left,
        "right": right,
        "refusal": reason,
    }


def rewrite(value, destinations):
    """Exact operand substitution, no evaluation or inferred bindings."""
    if type(value) is list:
        return [rewrite(item, destinations) for item in value]
    if type(value) is not dict:
        return value
    if set(value) == {"root", "name", "path"} and value["root"] != "result":
        target = destinations[(value["root"], value["name"])]
        return {**target, "path": target["path"] + value["path"]}
    return {k: rewrite(v, destinations) for k, v in value.items()}


def owner_header():
    text = {"type": "string"}
    head = {**text, "format": "ledger-head"}
    return obj(
        event_id=text,
        actor_id=text,
        transaction_time={**text, "format": "aware-instant"},
        sequence={"type": "integer"},
        previous_event_hash=head,
        event_hash={**text, "format": "sha256"},
    )


def owner_context():
    identity = {"type": "string", "format": "sha256"}
    head = {"type": "string", "format": "ledger-head"}
    return obj(
        value=obj(
            ledger_head=head,
            ledger_event_count={"type": "integer", "minimum": 0},
            contract_identity=identity,
            acceptance_head=head,
            materialization_head=head,
            graph_state_digest=identity,
            action_acceptance_head=head,
        )
    )


def retention(role, encoding="BYTES", **extra):
    return obj(
        record_id={"type": "string"},
        identity={"type": "string", "format": "sha256"},
        byte_length={"type": "integer", "minimum": 0},
        media_type={"type": "string"},
        role={"type": "string", "const": role},
        encoding={"type": "string", "const": encoding},
        **extra,
    )


def bind_registration(name, packet, contract_identity):
    program = deepcopy(packet["program"])
    inputs = program["inputs"]
    constants_schema = {
        k: deepcopy(inputs["artifact"][k]) for k in ("record_contract", "constants")
    }
    constants = {
        "record_contract": {
            "value": {
                "contract_identity": contract_identity,
                "record_type": inputs["artifact"]["record_contract"]["properties"][
                    "value"
                ]["properties"]["record_type"]["const"],
            }
        },
        "constants": {
            k: deepcopy(v["const"])
            for k, v in inputs["artifact"]["constants"]["properties"].items()
        },
    }
    destinations = {
        ("event", "header"): ref("event", "0", "header"),
        ("event", "records"): ref("event", "0", "data", "records"),
        ("event", "dependencies"): ref("event", "0", "data", "dependencies"),
        **{
            ("artifact", k): ref("artifact", "constants", "value", name, k)
            for k in constants
        },
    }
    data = {k: deepcopy(v) for k, v in inputs["event"].items() if k != "header"}
    # The original gap document retains the accepted field census. Bind it to
    # actual event schemas; its historical unresolved status is not rewritten.
    census = json.loads(
        (HERE / "lifecycle" / "registration-nonblank-gap.json").read_bytes()
    )["affected_fields"]
    item = data["records"]["properties"]["value"]["items"]["properties"]
    kind = item["record_type"]["const"]
    if kind in census:
        for field in census[kind]:
            schema = item["record"]["properties"][field.removesuffix("[]")]
            if field.endswith("[]"):
                schema = schema["items"]
            if schema["type"] != "string" or "format" in schema:
                raise ValueError(
                    f"nonblank census requires an unformatted string: {kind}.{field}"
                )
            schema["format"] = "nonblank"
    retained = obj()
    if "preimage" in inputs["artifact"]:
        data["preimage"] = deepcopy(inputs["artifact"]["preimage"])
        destinations[("artifact", "preimage")] = ref("event", "0", "data", "preimage")
    if name == "source":
        record = data["records"]["properties"]["value"]["items"]["properties"]["record"]
        for field in packet["semantic_hash_contract"]["field_checks"][
            "nonblank_fields"
        ]:
            record["properties"][field]["format"] = "nonblank"
        data["preimage"] = obj(
            value=obj(
                **{
                    k: deepcopy(record["properties"][v])
                    for k, v in SOURCE_PROJECTION.items()
                }
            )
        )
        retained = obj(source=retention("SOURCE_ARTIFACT"))
        steps = []
        for step in program["steps"]:
            if step["opcode"] == "HASH" and step["recipe"] == "ARTIFACT":
                for field, source in SOURCE_PROJECTION.items():
                    steps.append(
                        compare(
                            ref("event", "0", "data", "preimage", "value", field),
                            ref(
                                "event",
                                "0",
                                "data",
                                "records",
                                "value",
                                0,
                                "record",
                                source,
                            ),
                            "SOURCE_PREIMAGE_MISMATCH",
                            "INTEGER" if source == "source_byte_length" else "STRING",
                        )
                    )
                steps.append(
                    {
                        "opcode": "HASH",
                        "recipe": "VALUE",
                        "value": ref("event", "0", "data", "preimage", "value"),
                        "result": step["result"],
                        "refusal": step["refusal"],
                    }
                )
            elif any(
                type(v) is dict
                and v.get("root") == "artifact"
                and v.get("name") == "retention"
                for v in step.values()
            ):
                bound = deepcopy(step)
                for value in bound.values():
                    if type(value) is dict and value.get("name") == "retention":
                        value.update(
                            root="event",
                            name="0",
                            path=[
                                "retained",
                                "source",
                                {
                                    "bytes_sha256": "identity",
                                    "byte_length": "byte_length",
                                }[value["path"][0]],
                            ],
                        )
                    elif type(value) is dict and set(value) == {"root", "name", "path"}:
                        value.update(rewrite(value, destinations))
                steps.append(bound)
            else:
                steps.append(rewrite(step, destinations))
        for field, meta in (("id", "record_id"), ("source_media_type", "media_type")):
            steps.insert(
                -1,
                compare(
                    ref("event", "0", "data", "records", "value", 0, "record", field),
                    ref("event", "0", "retained", "source", meta),
                    "SOURCE_RETENTION_MISMATCH",
                ),
            )
    else:
        steps = rewrite(program["steps"], destinations)
    program.update(
        inputs={
            "event": {
                "0": obj(header=owner_header(), data=obj(**data), retained=retained)
            },
            "current": {"context": owner_context()},
            "artifact": {},
        },
        steps=steps,
    )
    return program, constants, obj(**constants_schema)


def _ruleset_packet(grant, epistemic):
    packet = deepcopy(grant)
    schema = deepcopy(epistemic["profile"]["record_schemas"]["ProtocolArtifact"])
    schema["properties"]["artifact_kind"]["const"] = "RULE_SET"
    item = packet["program"]["inputs"]["event"]["records"]["properties"]["value"][
        "items"
    ]
    item["properties"]["record"] = schema
    item["properties"]["record_type"]["const"] = "ProtocolArtifact"
    packet["program"]["inputs"]["artifact"]["record_contract"]["properties"]["value"][
        "properties"
    ]["record_type"]["const"] = "ProtocolArtifact"
    # Exact shared record/provenance checks plus uniqueness/introduction. Grant
    # interval and grantor rules are not rules for a ProtocolArtifact.
    steps = packet["program"]["steps"]
    packet["program"]["steps"] = steps[:7] + steps[-2:]
    packet["program"]["name"] = "retained-ruleset-registration"
    return packet


def build_registration_bundle(record_contract_bytes):
    packets = {
        name: json.loads(
            (HERE / "lifecycle" / f"{name}-registration.json").read_bytes()
        )
        for name in ("source", "grant", "monitor", "epistemic", "authorization")
    }
    packets["ruleset"] = _ruleset_packet(packets["grant"], packets["epistemic"])
    profile = {"targets": {}, "capabilities": [], "record_schemas": {}}
    programs, constants, schemas = {}, {}, {}
    for name, packet in packets.items():
        program, constant, schema = bind_registration(
            name, packet, digest(record_contract_bytes)
        )
        programs[name], constants[name], schemas[name] = program, constant, schema
        for key in ("targets", "record_schemas"):
            if key in packet["profile"]:
                for identifier, declaration in packet["profile"][key].items():
                    if (
                        identifier in profile[key]
                        and profile[key][identifier] != declaration
                    ):
                        raise ValueError(f"incompatible declared {key}: {identifier}")
                    profile[key][identifier] = deepcopy(declaration)
    ruleset = programs["ruleset"]
    ruleset["inputs"]["event"]["0"]["properties"]["retained"] = obj(
        source=retention("RETAINED_EVIDENCE")
    )
    for field, meta in (("id", "record_id"), ("artifact_hash", "identity")):
        ruleset["steps"].insert(
            -1,
            compare(
                ref("event", "0", "data", "records", "value", 0, "record", field),
                ref("event", "0", "retained", "source", meta),
                "RULESET_RETENTION_MISMATCH",
                "DIGEST" if field == "artifact_hash" else "STRING",
            ),
        )
    for program in programs.values():
        program["inputs"]["artifact"] = {
            "constants": obj(value=obj(**deepcopy(schemas)))
        }
    bundle = {
        "grammar": "malleus.finite-protocol-bundle/private-v0",
        "record_contract_base64": b64encode(record_contract_bytes).decode(),
        "instruction_schema": json.loads(
            (HERE.parent / "instructions.schema.json").read_bytes()
        ),
        "profile": profile,
        "constants": constants,
        "transactions": {
            name: {"event_types": ["PREREQUISITE_RECORDED"], "program": p}
            for name, p in programs.items()
        },
    }
    return load_bundle(canonical(bundle))
