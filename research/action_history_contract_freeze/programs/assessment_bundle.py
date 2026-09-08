"""Finite TYPE assessment admission, not checker invocation or acceptance.

This conformance variant has one open proposal and the existing two-static-input
monitor shape. Completed and paired-unavailable outputs are separate programs.
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
    obj,
    ref,
    compare,
    owner_header,
)


TEXT = {"type": "string"}
DIGEST = {"type": "string", "format": "sha256"}
REFERENCES = {
    "proposal": "ProposedSubgraph",
    "action": "LocalAction",
    "monitor": "MonitorSpecificationArtifact",
    "policy": "EpistemicPolicyArtifact",
    "contract": "SourceArtifact",
    "context": "SourceArtifact",
    "static0": "SourceArtifact",
    "static1": "SourceArtifact",
}
CLOSURE = ("proposal", "action", "contract", "monitor", "static0", "static1")


def array(items, length):
    return {
        "type": "array",
        "items": deepcopy(items),
        "minItems": length,
        "maxItems": length,
    }


def output_schemas():
    """Select fields from the existing authoritative producer field census."""
    census = json.loads((HERE / "monitor-output-fields.json").read_bytes())
    result = {}
    for name in ("type_result", "type_failure", "type_unavailable"):
        variant = census["variants"][name]
        names = {"content_hash", *variant["fields"], *variant["constants"]}
        for group in variant["groups"]:
            names.update(census["groups"][group])
        fields = {name: deepcopy(TEXT) for name in sorted(names)}
        for field in fields:
            if field.endswith("_hash"):
                fields[field] = deepcopy(DIGEST)
            elif field == "base_acceptance_head":
                fields[field] = {**TEXT, "format": "ledger-head"}
            elif field == "generated_at":
                fields[field] = {**TEXT, "format": "aware-instant"}
            elif field in ("source_record_ids", "input_record_ids", "reason_codes"):
                fields[field] = {
                    "type": "array",
                    "items": deepcopy(TEXT),
                    "uniqueItems": True,
                }
        fields["source_record_ids"] = array(
            TEXT, 7 if name == "type_unavailable" else 6
        )
        if "input_record_ids" in fields:
            fields["input_record_ids"] = array(TEXT, 6)
        if name == "type_result":
            fields["assessment_outcome"]["enum"] = ["SATISFIED", "VIOLATED"]
        for field, value in variant["constants"].items():
            fields[field]["const"] = value
        fields["responsible_role"]["const"] = "type-monitor"
        result[variant["record_type"]] = obj(**fields)
    return result


def add_type_assessment(bundle):
    bundle = deepcopy(bundle)
    records = bundle["transactions"]["context-proposal"]["program"]["inputs"]["event"][
        "1"
    ]["properties"]["data"]["properties"]
    for name, kind in (("action", "LocalAction"), ("proposal", "ProposedSubgraph")):
        bundle["profile"]["record_schemas"][kind] = deepcopy(
            records[name]["properties"]["value"]["items"]["properties"]["record"]
        )
    schemas = output_schemas()
    for schema in schemas.values():
        schema["properties"]["base_acceptance_head"] = deepcopy(
            bundle["profile"]["record_schemas"]["ProposedSubgraph"]["properties"][
                "base_acceptance_head"
            ]
        )
    bundle["profile"]["record_schemas"].update(deepcopy(schemas))
    target = {
        "target": "PROTOCOL_INDEX",
        "storage_path": ["protocol", "type_assessments"],
        "key_schemas": [deepcopy(TEXT), deepcopy(TEXT)],
        "value_schema": deepcopy(TEXT),
    }
    bundle["profile"]["targets"]["type_assessments"] = target
    constant = {
        "role": "type-monitor",
        "kind": "TYPE",
        "proposed": "PROPOSED",
        "types": REFERENCES,
        "contracts": {
            kind: {
                "contract_identity": digest(raw(bundle["record_contract_base64"])),
                "record_type": kind,
            }
            for kind in schemas
        },
    }
    constant_schema = obj(
        role={**TEXT, "const": "type-monitor"},
        kind={**TEXT, "const": "TYPE"},
        proposed={**TEXT, "const": "PROPOSED"},
        types=obj(**{k: {**TEXT, "const": v} for k, v in REFERENCES.items()}),
        contracts=obj(
            **{
                k: obj(contract_identity=DIGEST, record_type={**TEXT, "const": k})
                for k in schemas
            }
        ),
    )
    bundle["constants"]["type_assessment"] = constant
    for transaction in bundle["transactions"].values():
        program = transaction["program"]
        constants = program["inputs"]["artifact"]["constants"]["properties"]["value"]
        constants["properties"]["type_assessment"] = deepcopy(constant_schema)
        constants["required"].append("type_assessment")
        if "state" in program["inputs"]["current"]:
            protocol = program["inputs"]["current"]["state"]["properties"]["value"][
                "properties"
            ]["protocol"]
            protocol["properties"]["type_assessments"] = {
                "type": "array",
                "items": obj(keys=array(TEXT, 2), value=TEXT),
            }
    for unavailable in (False, True):
        name = "type-unavailable" if unavailable else "type-completed"
        bundle["transactions"][name] = {
            "event_types": ["ASSESSMENT_RECORDED"],
            "program": _program(bundle, unavailable),
        }
    return load_bundle(canonical(bundle))


def _program(bundle, unavailable):
    predecessor = bundle["transactions"]["context-proposal"]["program"]
    inputs = deepcopy(predecessor["inputs"])
    inputs["artifact"]["selection"] = deepcopy(
        bundle["transactions"]["initialize"]["program"]["inputs"]["artifact"][
            "selection"
        ]
    )
    original = deepcopy(
        inputs["event"]["0"]["properties"]["retained"]["properties"]["source"][
            "properties"
        ]["value"]
    )
    data = {
        "references": obj(**{k: obj(id=TEXT, record_hash=DIGEST) for k in REFERENCES}),
        "original": obj(value=original),
    }
    kinds = {"assessment": "UnavailableAssessment" if unavailable else "TypeAssessment"}
    if unavailable:
        kinds = {"failure": "MonitorFailure", **kinds}
    for name, kind in kinds.items():
        data[name] = obj(
            value=array(
                obj(
                    record_type={**TEXT, "const": kind},
                    record=deepcopy(bundle["profile"]["record_schemas"][kind]),
                ),
                1,
            )
        )
        data[name + "_dependencies"] = obj(
            value={"type": "array", "items": TEXT, "uniqueItems": True}
        )
    inputs["event"] = {
        "0": obj(header=owner_header(), data=obj(**data), retained=obj())
    }
    indexes = inputs["current"]["state"]["properties"]["value"]["properties"][
        "protocol"
    ]
    for name in ("context_by_proposal", "proposal_states"):
        indexes["required"].append(name)
        indexes["properties"][name].update(minItems=1, maxItems=1)

    def setting(*path):
        return ref("artifact", "constants", "value", "type_assessment", *path)

    def resolved(name, *path):
        return ref("result", "applied-" + name, "value", *path)

    def record(name, *path):
        return ref("event", "0", "data", name, "value", 0, "record", *path)

    def original_ref(*path):
        return ref("event", "0", "data", "original", "value", *path)

    steps = []
    for name in REFERENCES:
        steps.append(
            {
                "opcode": "RESOLVE_RECORD",
                "record_id": ref("event", "0", "data", "references", name, "id"),
                "record_hash": ref(
                    "event", "0", "data", "references", name, "record_hash"
                ),
                "record_type": setting("types", name),
                "scope": "APPLIED",
                "result": "applied-" + name,
                "refusal": "UNAPPLIED_ASSESSMENT_INPUT",
            }
        )
    steps += [
        {
            "opcode": "HASH",
            "recipe": "VALUE",
            "value": original_ref(),
            "result": "original-hash",
            "refusal": "INVALID_ORIGINAL_CONTEXT",
        },
        compare(
            ref("result", "original-hash", "value"),
            resolved("context", "source_content_digest"),
            "MISBOUND_ORIGINAL_CONTEXT",
            "DIGEST",
        ),
        compare(
            original_ref("id"), resolved("context", "id"), "WRONG_ORIGINAL_CONTEXT_ID"
        ),
        compare(
            resolved("contract", "source_content_digest"),
            ref("artifact", "selection", "value", "record_contract_identity"),
            "WRONG_CHECK_RECORD_CONTRACT",
            "DIGEST",
        ),
        compare(
            resolved("monitor", "assessment_kind"),
            setting("kind"),
            "WRONG_ASSESSMENT_KIND",
        ),
        compare(
            resolved("policy", "id"),
            original_ref("epistemic_policy", "id"),
            "WRONG_ASSESSMENT_POLICY",
        ),
        compare(
            resolved("policy", "content_hash"),
            original_ref("epistemic_policy", "record_hash"),
            "WRONG_ASSESSMENT_POLICY_HASH",
            "DIGEST",
        ),
        {
            "opcode": "REQUIRE_MEMBER",
            "value_kind": "STRING",
            "value": resolved("monitor", "id"),
            "members": resolved("policy", "required_monitor_ids"),
            "refusal": "UNSELECTED_MONITOR",
        },
        compare(
            resolved("proposal", "id"),
            original_ref("proposal_id"),
            "WRONG_CHECK_PROPOSAL",
        ),
        compare(
            resolved("action", "id"), original_ref("action_id"), "WRONG_CHECK_ACTION"
        ),
        compare(
            original_ref("action_acceptance_head"),
            ref("current", "context", "value", "action_acceptance_head"),
            "STALE_CHECK_ACTION_HEAD",
            "HEAD",
        ),
    ]
    for path, (target, kind) in COORDINATES.items():
        if path[0] == "domain":
            steps.append(
                compare(
                    original_ref(*path),
                    ref("current", "context", "value", target),
                    "STALE_CHECK_DOMAIN",
                    kind,
                )
            )
    for index, role in (("context_by_proposal", "context"), ("proposal_states", None)):
        current = ("value", "protocol", index, 0)
        steps += [
            compare(
                ref("current", "state", *current, "keys", 0),
                resolved("proposal", "id"),
                "WRONG_PROPOSAL_STATE_KEY",
            ),
            compare(
                ref("current", "state", *current, "value"),
                resolved(role, "id") if role else setting("proposed"),
                "WRONG_CHECK_PROPOSAL_STATE",
            ),
        ]
    for ordinal in range(2):
        role = "static" + str(ordinal)
        steps += [
            compare(
                resolved(role, "id"),
                resolved("monitor", "input_artifact_ids", ordinal),
                "WRONG_MONITOR_STATIC_ID",
            ),
            compare(
                resolved(role, "content_hash"),
                resolved("monitor", "input_artifact_record_hashes", ordinal),
                "WRONG_MONITOR_STATIC_HASH",
                "DIGEST",
            ),
        ]
    for name, kind in kinds.items():
        steps += [
            {
                "opcode": "VALIDATE_RECORD",
                "record": record(name),
                "contract": setting("contracts", kind),
                "result": name + "-validated",
                "refusal": "INVALID_CHECK_OUTPUT_RECORD",
            },
            {
                "opcode": "HASH",
                "recipe": "RECORD",
                "value": record(name),
                "record_type": ref(
                    "event", "0", "data", name, "value", 0, "record_type"
                ),
                "result": name + "-hash",
                "refusal": "INVALID_CHECK_OUTPUT_HASH",
            },
            compare(
                ref("result", name + "-hash", "value"),
                record(name, "content_hash"),
                "WRONG_CHECK_OUTPUT_HASH",
                "DIGEST",
            ),
            compare(
                record(name, "responsible_role"), setting("role"), "WRONG_CHECKER_ROLE"
            ),
        ]
        for field, header in (
            ("generation_event_id", "event_id"),
            ("generated_at", "transaction_time"),
            ("responsible_actor_id", "actor_id"),
        ):
            steps.append(
                compare(
                    record(name, field),
                    ref("event", "0", "header", header),
                    "MISBOUND_CHECKER_METADATA",
                )
            )
        for field, role, target, comparison in (
            ("proposal_id", "proposal", "id", "STRING"),
            ("proposal_content_hash", "proposal", "content_hash", "DIGEST"),
            ("base_acceptance_head", "proposal", "base_acceptance_head", "HEAD"),
            ("monitor_id", "monitor", "id", "STRING"),
            ("monitor_hash", "monitor", "content_hash", "DIGEST"),
            ("monitor_version", "monitor", "artifact_version", "STRING"),
        ):
            steps.append(
                compare(
                    record(name, field),
                    resolved(role, target),
                    "MISBOUND_CHECK_OUTPUT",
                    comparison,
                )
            )
        for field in (
            ("source_record_ids", "input_record_ids")
            if name == "assessment"
            else ("source_record_ids",)
        ):
            for ordinal, role in enumerate(CLOSURE):
                steps.append(
                    compare(
                        record(name, field, ordinal),
                        resolved(role, "id"),
                        "WRONG_CHECK_INPUT_CLOSURE",
                    )
                )
    if unavailable:
        steps += [
            compare(
                record("assessment", "monitor_failure_id"),
                record("failure", "id"),
                "MISBOUND_FAILURE_PAIR",
            ),
            compare(
                record("assessment", "source_record_ids", 6),
                record("failure", "id"),
                "MISSING_FAILURE_PROVENANCE",
            ),
        ]
    steps.append(
        {
            "opcode": "REQUIRE_UNIQUE",
            "records": ref("event", "0", "data", "assessment", "value"),
            "key_paths": [["record", "proposal_id"], ["record", "monitor_id"]],
            "target_index": "type_assessments",
            "refusal": "DUPLICATE_TYPE_ASSESSMENT",
        }
    )
    for name in kinds:
        steps.append(
            {
                "opcode": "INTRODUCE_RECORDS",
                "records": ref("event", "0", "data", name, "value"),
                "dependencies": ref(
                    "event", "0", "data", name + "_dependencies", "value"
                ),
                "result": "introduced-" + name,
                "refusal": "INVALID_CHECK_OUTPUT_INTRODUCTION",
            }
        )
    steps.append(
        {
            "opcode": "SET_PROTOCOL_STATE",
            "target": "PROTOCOL_INDEX",
            "name": "type_assessments",
            "keys": [
                record("assessment", "proposal_id"),
                record("assessment", "monitor_id"),
            ],
            "value": record("assessment", "id"),
            "refusal": "INVALID_TYPE_ASSESSMENT_INDEX",
        }
    )
    return {
        "name": "admit-type-unavailable" if unavailable else "admit-type-completed",
        "inputs": inputs,
        "required_capabilities": [],
        "introductions": [
            {
                "name": name,
                "depends_on": ["failure"]
                if name == "assessment" and unavailable
                else [],
            }
            for name in kinds
        ],
        "steps": steps,
    }
