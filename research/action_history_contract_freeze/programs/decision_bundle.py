"""Author finite action-only decision programs. Append/replay imports no builder.

One open proposal, two TYPE monitors, no claim revisions or graph application.
The existing control capability recomputes the verdict; variants declare effects.
"""

from copy import deepcopy

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
    compare,
    obj,
    ref,
    owner_header,
)


TARGETS = {
    "ACCEPT": "ACCEPTED",
    "REJECT": "REJECTED",
    "DEFER": "DEFERRED",
    "CONTEST": "CONTESTED",
}
REFERENCES = {
    "proposal": "ProposedSubgraph",
    "policy": "EpistemicPolicyArtifact",
    "context": "SourceArtifact",
    "rules": "ProtocolArtifact",
}
RECIPE = "ASSENT_EPISTEMIC_CONTROL_V1"


def strings(**bounds):
    return {"type": "array", "items": deepcopy(TEXT), "uniqueItems": True, **bounds}


def schemas(bundle):
    completed = deepcopy(bundle["profile"]["record_schemas"]["TypeAssessment"])
    unavailable = bundle["profile"]["record_schemas"]["UnavailableAssessment"]
    assessment = deepcopy(completed)
    assessment["properties"].update(deepcopy(unavailable["properties"]))
    assessment["required"] = sorted(
        set(completed["required"]) & set(unavailable["required"])
    )
    assessment["properties"]["assessment_outcome"] = {
        **TEXT,
        "enum": ["SATISFIED", "VIOLATED", "UNKNOWN"],
    }
    assessment["properties"]["source_record_ids"] = strings(minItems=6, maxItems=7)
    metadata = {
        k: deepcopy(completed["properties"][k])
        for k in (
            "id",
            "content_hash",
            "generation_event_id",
            "generated_at",
            "responsible_actor_id",
            "responsible_role",
        )
    }
    metadata["responsible_role"] = deepcopy(TEXT)
    decision = obj(
        **metadata,
        source_record_ids=strings(minItems=5, maxItems=5),
        proposal_id=TEXT,
        proposal_content_hash=DIGEST,
        base_acceptance_head=deepcopy(completed["properties"]["base_acceptance_head"]),
        epistemic_verdict={**TEXT, "enum": list(TARGETS)},
        assessment_ids=array(TEXT, 2),
        triggered_assessment_ids=strings(maxItems=2),
        policy_evaluation_hash=DIGEST,
        evidence_assertion_ids=strings(maxItems=0),
        request_ids=strings(maxItems=0),
        claim_revision_ids=strings(maxItems=0),
        policy_id=TEXT,
        policy_hash=DIGEST,
        ruleset_id=TEXT,
        ruleset_hash=DIGEST,
        rationale_codes=strings(minItems=1),
        rationale=TEXT,
    )
    transition = obj(
        **metadata,
        source_record_ids=array(TEXT, 1),
        transition_subject_id=TEXT,
        from_state=TEXT,
        to_state=TEXT,
        triggering_record_id=TEXT,
        ledger_event_id=TEXT,
        sequence={"type": "integer"},
        transition_time={**TEXT, "format": "aware-instant"},
    )
    return {
        "Assessment": assessment,
        "EpistemicDecision": decision,
        "TransitionRecord": transition,
    }


def add_epistemic_decision(bundle):
    bundle = deepcopy(bundle)
    bundle["profile"]["record_schemas"].update(schemas(bundle))
    policy = bundle["profile"]["record_schemas"]["EpistemicPolicyArtifact"]
    for field in ("required_monitor_ids", "required_monitor_record_hashes"):
        policy["properties"][field].update(minItems=2, maxItems=2)
    bundle["profile"]["capabilities"].append(RECIPE)
    bundle["profile"]["control_result_schema"] = obj(
        verdict=TEXT,
        assessment_ids=strings(),
        triggered_assessment_ids=strings(),
        evaluation_hash=DIGEST,
    )
    bundle["profile"]["targets"]["epistemic_decisions"] = {
        "target": "PROTOCOL_INDEX",
        "storage_path": ["protocol", "epistemic_decisions"],
        "key_schemas": [deepcopy(TEXT)],
        "value_schema": deepcopy(TEXT),
    }
    kinds = {
        **REFERENCES,
        "monitor": "MonitorSpecificationArtifact",
        "assessment": "Assessment",
    }
    constants = {
        "types": kinds,
        "targets": TARGETS,
        "proposed": "PROPOSED",
        "recipe": RECIPE,
        "roles": {"decision": "epistemic-controller", "transition": "state-controller"},
        "contracts": {
            k: {
                "contract_identity": digest(raw(bundle["record_contract_base64"])),
                "record_type": k,
            }
            for k in ("EpistemicDecision", "TransitionRecord")
        },
    }
    constant_schema = obj(
        types=obj(**{k: {**TEXT, "const": v} for k, v in kinds.items()}),
        targets=obj(**{k: {**TEXT, "const": v} for k, v in TARGETS.items()}),
        proposed={**TEXT, "const": "PROPOSED"},
        recipe={**TEXT, "const": RECIPE},
        roles=obj(**{k: {**TEXT, "const": v} for k, v in constants["roles"].items()}),
        contracts=obj(
            **{
                k: obj(contract_identity=DIGEST, record_type={**TEXT, "const": k})
                for k in constants["contracts"]
            }
        ),
    )
    bundle["constants"]["epistemic_decision"] = constants
    for transaction in bundle["transactions"].values():
        inputs = transaction["program"]["inputs"]
        cs = inputs["artifact"]["constants"]["properties"]["value"]
        cs["properties"]["epistemic_decision"] = deepcopy(constant_schema)
        cs["required"].append("epistemic_decision")
        if "state" in inputs["current"]:
            inputs["current"]["state"]["properties"]["value"]["properties"]["protocol"][
                "properties"
            ]["epistemic_decisions"] = {
                "type": "array",
                "items": obj(keys=array(TEXT, 1), value=TEXT),
            }
    for verdict in TARGETS:
        bundle["transactions"]["epistemic-" + verdict.lower()] = {
            "event_types": ["EPISTEMIC_DECIDED"],
            "program": _program(bundle, verdict),
        }
    return load_bundle(canonical(bundle))


def _program(bundle, verdict):
    inputs = deepcopy(bundle["transactions"]["type-completed"]["program"]["inputs"])
    catalog = bundle["profile"]["record_schemas"]
    original = inputs["event"]["0"]["properties"]["data"]["properties"]["original"]
    head = catalog["ProposedSubgraph"]["properties"]["base_acceptance_head"]
    data = {
        "references": obj(**{k: obj(id=TEXT, record_hash=DIGEST) for k in REFERENCES}),
        "original": original,
        "control": obj(
            recipe={**TEXT, "const": RECIPE},
            monitors=array(catalog["MonitorSpecificationArtifact"], 2),
            bindings=obj(
                proposal_id=TEXT,
                proposal_content_hash=DIGEST,
                base_acceptance_head=head,
            ),
        ),
        "outputs": array(catalog["Assessment"], 2),
    }
    for name, kind in (
        ("decision", "EpistemicDecision"),
        ("transition", "TransitionRecord"),
    ):
        data[name] = obj(
            value=array(
                obj(record_type={**TEXT, "const": kind}, record=catalog[kind]), 1
            )
        )
        data[name + "_dependencies"] = obj(value=strings())
    if verdict == "ACCEPT":
        data["acceptance_preimage"] = obj(
            previous_acceptance_head=head,
            proposal_content_hash=DIGEST,
            decision_content_hash=DIGEST,
            revision_content_hashes=array(DIGEST, 0),
        )
    inputs["event"] = {
        "0": obj(header=owner_header(), data=obj(**data), retained=obj())
    }
    indexes = inputs["current"]["state"]["properties"]["value"]["properties"][
        "protocol"
    ]
    indexes["required"].append("type_assessments")
    indexes["properties"]["type_assessments"].update(minItems=2, maxItems=2)

    def setting(*path):
        return ref("artifact", "constants", "value", "epistemic_decision", *path)

    def supplied(*path):
        return ref("event", "0", "data", *path)

    def record(name, *path):
        return supplied(name, "value", 0, "record", *path)

    def resolved(name, *path):
        return ref("result", name, "value", *path)

    def resolve(name, kind, identifier, identity):
        return {
            "opcode": "RESOLVE_RECORD",
            "scope": "APPLIED",
            "record_type": setting("types", kind),
            "record_id": identifier,
            "record_hash": identity,
            "result": name,
            "refusal": "UNAPPLIED_DECISION_INPUT",
        }

    def same_value(name, left, right, reason):
        return [
            {
                "opcode": "HASH",
                "recipe": "VALUE",
                "value": left,
                "result": name + "-left",
                "refusal": reason,
            },
            {
                "opcode": "HASH",
                "recipe": "VALUE",
                "value": right,
                "result": name + "-right",
                "refusal": reason,
            },
            compare(
                resolved(name + "-left"), resolved(name + "-right"), reason, "DIGEST"
            ),
        ]

    steps = [
        resolve(
            name,
            name,
            supplied("references", name, "id"),
            supplied("references", name, "record_hash"),
        )
        for name in REFERENCES
    ]
    steps += [
        {
            "opcode": "HASH",
            "recipe": "VALUE",
            "value": supplied("original", "value"),
            "result": "original-hash",
            "refusal": "INVALID_ORIGINAL_CONTEXT",
        },
        compare(
            resolved("original-hash"),
            resolved("context", "source_content_digest"),
            "MISBOUND_ORIGINAL_CONTEXT",
            "DIGEST",
        ),
        compare(
            supplied("original", "value", "proposal_id"),
            resolved("proposal", "id"),
            "WRONG_DECISION_PROPOSAL",
        ),
        compare(
            resolved("proposal", "base_acceptance_head"),
            ref("current", "context", "value", "action_acceptance_head"),
            "STALE_ACTION_HEAD",
            "HEAD",
        ),
    ]
    for (group, field), (target, kind) in COORDINATES.items():
        if group == "domain":
            steps.append(
                compare(
                    supplied("original", "value", group, field),
                    ref("current", "context", "value", target),
                    "STALE_ORIGINAL_DOMAIN",
                    kind,
                )
            )
    for index, expected in (
        ("context_by_proposal", resolved("context", "id")),
        ("proposal_states", setting("proposed")),
    ):
        steps += [
            compare(
                ref("current", "state", "value", "protocol", index, 0, "keys", 0),
                resolved("proposal", "id"),
                "WRONG_DECISION_STATE_KEY",
            ),
            compare(
                ref("current", "state", "value", "protocol", index, 0, "value"),
                expected,
                "PROPOSAL_NOT_OPEN",
            ),
        ]
    for field, source, target, kind in (
        ("policy_id", "policy", "id", "STRING"),
        ("policy_hash", "policy", "content_hash", "DIGEST"),
        ("proposal_id", "proposal", "id", "STRING"),
        ("proposal_content_hash", "proposal", "content_hash", "DIGEST"),
        ("base_acceptance_head", "proposal", "base_acceptance_head", "HEAD"),
        ("ruleset_id", "rules", "id", "STRING"),
        ("ruleset_hash", "rules", "content_hash", "DIGEST"),
    ):
        steps.append(
            compare(
                record("decision", field),
                resolved(source, target),
                "MISBOUND_DECISION",
                kind,
            )
        )
    for field, expected, kind in (
        ("epistemic_policy_id", resolved("policy", "id"), "STRING"),
        ("epistemic_policy_hash", resolved("policy", "content_hash"), "DIGEST"),
    ):
        steps.append(
            compare(
                resolved("proposal", field), expected, "WRONG_SELECTED_POLICY", kind
            )
        )
    for field, expected, kind in (
        ("ruleset_id", resolved("rules", "id"), "STRING"),
        ("ruleset_record_hash", resolved("rules", "content_hash"), "DIGEST"),
    ):
        steps.append(
            compare(resolved("policy", field), expected, "WRONG_SELECTED_RULESET", kind)
        )
    for field, kind in (
        ("proposal_id", "STRING"),
        ("proposal_content_hash", "DIGEST"),
        ("base_acceptance_head", "HEAD"),
    ):
        target = {
            "proposal_id": "id",
            "proposal_content_hash": "content_hash",
            "base_acceptance_head": "base_acceptance_head",
        }[field]
        steps.append(
            compare(
                supplied("control", "bindings", field),
                resolved("proposal", target),
                "MISBOUND_CONTROL_CONTEXT",
                kind,
            )
        )
    for ordinal in range(2):
        monitor, assessment = "monitor" + str(ordinal), "assessment" + str(ordinal)
        steps += [
            resolve(
                monitor,
                "monitor",
                resolved("policy", "required_monitor_ids", ordinal),
                resolved("policy", "required_monitor_record_hashes", ordinal),
            ),
            resolve(
                assessment,
                "assessment",
                supplied("outputs", ordinal, "id"),
                supplied("outputs", ordinal, "content_hash"),
            ),
            compare(
                ref(
                    "current",
                    "state",
                    "value",
                    "protocol",
                    "type_assessments",
                    ordinal,
                    "keys",
                    0,
                ),
                resolved("proposal", "id"),
                "WRONG_ASSESSMENT_PROPOSAL",
            ),
            compare(
                ref(
                    "current",
                    "state",
                    "value",
                    "protocol",
                    "type_assessments",
                    ordinal,
                    "keys",
                    1,
                ),
                resolved(monitor, "id"),
                "WRONG_ASSESSMENT_MONITOR",
            ),
            compare(
                ref(
                    "current",
                    "state",
                    "value",
                    "protocol",
                    "type_assessments",
                    ordinal,
                    "value",
                ),
                resolved(assessment, "id"),
                "WRONG_APPLIED_ASSESSMENT",
            ),
        ]
        steps += same_value(
            monitor,
            supplied("control", "monitors", ordinal),
            resolved(monitor),
            "FORGED_CONTROL_MONITOR",
        )
        steps += same_value(
            assessment,
            supplied("outputs", ordinal),
            resolved(assessment),
            "FORGED_CONTROL_OUTPUT",
        )
    steps.append(
        {
            "opcode": "SELECT_CONTROL",
            "policy": resolved("policy"),
            "outputs": supplied("outputs"),
            "context": supplied("control"),
            "result": "control",
            "refusal": "INVALID_EPISTEMIC_CONTROL",
        }
    )
    steps += [
        compare(
            record("decision", "epistemic_verdict"),
            resolved("control", "verdict"),
            "FORGED_EPISTEMIC_VERDICT",
        ),
        compare(
            record("decision", "policy_evaluation_hash"),
            resolved("control", "evaluation_hash"),
            "FORGED_EVALUATION_IDENTITY",
            "DIGEST",
        ),
    ]
    for field in ("assessment_ids", "triggered_assessment_ids"):
        steps += same_value(
            field,
            record("decision", field),
            resolved("control", field),
            "WRONG_POLICY_ASSESSMENT_ORDER",
        )
    # Variant choice is checked against the recomputed verdict, not trusted.
    inputs["event"]["0"]["properties"]["data"]["properties"]["decision"]["properties"][
        "value"
    ]["items"]["properties"]["record"] = deepcopy(catalog["EpistemicDecision"])
    inputs["event"]["0"]["properties"]["data"]["properties"]["decision"]["properties"][
        "value"
    ]["items"]["properties"]["record"]["properties"]["epistemic_verdict"][
        "const"
    ] = verdict
    for name, kind in (
        ("decision", "EpistemicDecision"),
        ("transition", "TransitionRecord"),
    ):
        steps += [
            {
                "opcode": "VALIDATE_RECORD",
                "record": record(name),
                "contract": setting("contracts", kind),
                "result": name + "-validated",
                "refusal": "INVALID_DECISION_RECORD",
            },
            {
                "opcode": "HASH",
                "recipe": "RECORD",
                "value": record(name),
                "record_type": supplied(name, "value", 0, "record_type"),
                "result": name + "-hash",
                "refusal": "INVALID_DECISION_HASH",
            },
            compare(
                resolved(name + "-hash"),
                record(name, "content_hash"),
                "WRONG_DECISION_RECORD_HASH",
                "DIGEST",
            ),
            compare(
                record(name, "responsible_role"),
                setting("roles", name),
                "WRONG_DECISION_ROLE",
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
                    "MISBOUND_DECISION_METADATA",
                )
            )
    for field, expected, kind in (
        ("transition_subject_id", resolved("proposal", "id"), "STRING"),
        ("from_state", setting("proposed"), "STRING"),
        ("to_state", setting("targets", verdict), "STRING"),
        ("triggering_record_id", record("decision", "id"), "STRING"),
        ("ledger_event_id", ref("event", "0", "header", "event_id"), "STRING"),
        ("sequence", ref("event", "0", "header", "sequence"), "INTEGER"),
        ("transition_time", ref("event", "0", "header", "transaction_time"), "STRING"),
    ):
        steps.append(
            compare(
                record("transition", field),
                expected,
                "MISBOUND_DECISION_TRANSITION",
                kind,
            )
        )
    steps.append(
        compare(
            record("transition", "source_record_ids", 0),
            record("decision", "id"),
            "MISSING_DECISION_PROVENANCE",
        )
    )
    for role in ("proposal", "policy", "rules", "assessment0", "assessment1"):
        steps.append(
            {
                "opcode": "REQUIRE_MEMBER",
                "value_kind": "STRING",
                "value": resolved(role, "id"),
                "members": record("decision", "source_record_ids"),
                "refusal": "MISSING_DECISION_PROVENANCE",
            }
        )
    for name in ("decision", "transition"):
        steps.append(
            {
                "opcode": "INTRODUCE_RECORDS",
                "records": supplied(name, "value"),
                "dependencies": supplied(name + "_dependencies", "value"),
                "result": "introduced-" + name,
                "refusal": "INVALID_DECISION_INTRODUCTION",
            }
        )
    if verdict == "ACCEPT":
        for field, expected, kind in (
            (
                "previous_acceptance_head",
                ref("current", "context", "value", "action_acceptance_head"),
                "HEAD",
            ),
            ("proposal_content_hash", resolved("proposal", "content_hash"), "DIGEST"),
            ("decision_content_hash", record("decision", "content_hash"), "DIGEST"),
        ):
            steps.append(
                compare(
                    supplied("acceptance_preimage", field),
                    expected,
                    "WRONG_ACTION_ACCEPTANCE_PREIMAGE",
                    kind,
                )
            )
        steps += [
            {
                "opcode": "HASH",
                "recipe": "VALUE",
                "value": supplied("acceptance_preimage"),
                "result": "accepted-head",
                "refusal": "INVALID_ACTION_ACCEPTANCE_HEAD",
            },
            {
                "opcode": "SET_PROTOCOL_STATE",
                "target": "ACTION_ACCEPTANCE_HEAD",
                "name": "action_head",
                "value": resolved("accepted-head"),
                "refusal": "INVALID_ACTION_ACCEPTANCE_HEAD",
            },
        ]
    for name, value in (
        ("proposal_states", setting("targets", verdict)),
        ("epistemic_decisions", record("decision", "id")),
    ):
        steps.append(
            {
                "opcode": "SET_PROTOCOL_STATE",
                "target": "PROTOCOL_INDEX",
                "name": name,
                "keys": [resolved("proposal", "id")],
                "value": value,
                "refusal": "INVALID_DECISION_STATE",
            }
        )
    return {
        "name": "action-only-" + verdict.lower(),
        "inputs": inputs,
        "required_capabilities": [RECIPE],
        "introductions": [
            {"name": "decision", "depends_on": []},
            {"name": "transition", "depends_on": ["decision"]},
        ],
        "steps": steps,
    }
