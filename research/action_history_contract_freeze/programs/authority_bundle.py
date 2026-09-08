"""Finite admission of real direct-grant judgments, not authorization/effects.

This authors the selected one-proposal conformance data. The owning executor
resolves actual records and the verified current-context index on each fold.
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
    output_schemas,
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


REFERENCES = {
    "proposal": "ProposedSubgraph",
    "action": "LocalAction",
    "grant": "AuthorityGrant",
    "scope_association": "SourceArtifact",
    "requested_interval": "SourceArtifact",
    "authorization_policy": "AuthorizationPolicyArtifact",
    "original_context": "SourceArtifact",
    "current_context": "SourceArtifact",
    "monitor": "MonitorSpecificationArtifact",
    "static0": "SourceArtifact",
    "static1": "SourceArtifact",
    "epistemic": "EpistemicDecision",
}
CLOSURE = tuple(name for name in REFERENCES if name != "epistemic")


def add_authority_assessment(bundle):
    bundle = deepcopy(bundle)
    schemas = output_schemas(
        prefix="authority", closure_length=len(CLOSURE), role="authority-monitor"
    )
    head = bundle["profile"]["record_schemas"]["ProposedSubgraph"]["properties"][
        "base_acceptance_head"
    ]
    for schema in schemas.values():
        schema["properties"]["base_acceptance_head"] = deepcopy(head)
    # MonitorFailure has distinct event-local TYPE and AUTHORITY shapes. Do not
    # replace the earlier TYPE resolution declaration with an AUTHORITY shape.
    for kind in ("AuthorityAssessment", "UnavailableAuthorityAssessment"):
        bundle["profile"]["record_schemas"][kind] = deepcopy(schemas[kind])
    bundle["profile"]["record_schemas"]["AuthorityGrant"] = deepcopy(
        bundle["transactions"]["grant"]["program"]["inputs"]["event"]["0"][
            "properties"
        ]["data"]["properties"]["records"]["properties"]["value"]["items"][
            "properties"
        ]["record"]
    )
    keys = [
        deepcopy(TEXT),
        deepcopy(TEXT),
        deepcopy(head),
        deepcopy(TEXT),
        deepcopy(TEXT),
    ]
    bundle["profile"]["targets"]["authority_assessments"] = {
        "target": "PROTOCOL_INDEX",
        "storage_path": ["protocol", "authority_assessments"],
        "key_schemas": keys,
        "value_schema": deepcopy(TEXT),
    }
    constants = {
        "types": REFERENCES,
        "accepted": "ACCEPTED",
        "accept": "ACCEPT",
        "pending": "PENDING",
        "role": "authority-monitor",
        "kind": "AUTHORITY",
        "contracts": {
            kind: {
                "contract_identity": digest(raw(bundle["record_contract_base64"])),
                "record_type": kind,
            }
            for kind in schemas
        },
    }
    cs = obj(
        types=obj(
            **{name: {**TEXT, "const": kind} for name, kind in REFERENCES.items()}
        ),
        **{
            key: {**TEXT, "const": constants[key]}
            for key in ("accepted", "accept", "pending", "role", "kind")
        },
        contracts=obj(
            **{
                kind: obj(contract_identity=DIGEST, record_type={**TEXT, "const": kind})
                for kind in schemas
            }
        ),
    )
    bundle["constants"]["authority_assessment"] = constants
    for transaction in bundle["transactions"].values():
        inputs = transaction["program"]["inputs"]
        contents = inputs["artifact"]["constants"]["properties"]["value"]
        contents["properties"]["authority_assessment"] = deepcopy(cs)
        contents["required"].append("authority_assessment")
        if "state" in inputs["current"]:
            inputs["current"]["state"]["properties"]["value"]["properties"]["protocol"][
                "properties"
            ]["authority_assessments"] = {
                "type": "array",
                "items": obj(keys=array(TEXT, 5), value=TEXT),
            }
    for unavailable in (False, True):
        name = "authority-unavailable" if unavailable else "authority-completed"
        bundle["transactions"][name] = {
            "event_types": ["ASSESSMENT_RECORDED"],
            "program": _program(bundle, schemas, unavailable),
        }
    return load_bundle(canonical(bundle))


def _program(bundle, schemas, unavailable):
    inputs = deepcopy(bundle["transactions"]["type-completed"]["program"]["inputs"])
    original = inputs["event"]["0"]["properties"]["data"]["properties"]["original"][
        "properties"
    ]["value"]
    current = bundle["transactions"]["capture-current"]["program"]["inputs"]["event"][
        "0"
    ]["properties"]["retained"]["properties"]["source"]["properties"]["value"]
    data = {
        "references": obj(
            **{name: obj(id=TEXT, record_hash=DIGEST) for name in REFERENCES}
        ),
        "contents": obj(original_context=original, current_context=current),
        "executor_id": TEXT,
    }
    kinds = {
        "assessment": "UnavailableAuthorityAssessment"
        if unavailable
        else "AuthorityAssessment"
    }
    if unavailable:
        kinds = {"failure": "MonitorFailure", **kinds}
    for name, kind in kinds.items():
        data[name] = obj(
            value=array(
                obj(record_type={**TEXT, "const": kind}, record=schemas[kind]), 1
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
    for name in (
        "proposal_states",
        "context_by_proposal",
        "epistemic_decisions",
        "current_contexts",
        "authorization_states",
    ):
        if name not in indexes["required"]:
            indexes["required"].append(name)
        indexes["properties"][name].update(minItems=1, maxItems=1)

    def setting(*path):
        return ref("artifact", "constants", "value", "authority_assessment", *path)

    def supplied(*path):
        return ref("event", "0", "data", *path)

    def resolved(name, *path):
        return ref("result", name, "value", *path)

    def record(name, *path):
        return supplied(name, "value", 0, "record", *path)

    def content(name, *path):
        return supplied("contents", name, *path)

    steps = [
        {
            "opcode": "RESOLVE_RECORD",
            "scope": "APPLIED",
            "record_id": supplied("references", name, "id"),
            "record_hash": supplied("references", name, "record_hash"),
            "record_type": setting("types", name),
            "result": name,
            "refusal": "UNAPPLIED_AUTHORITY_INPUT",
        }
        for name in REFERENCES
    ]
    for name in ("original_context", "current_context"):
        steps += [
            {
                "opcode": "HASH",
                "recipe": "VALUE",
                "value": content(name),
                "result": name + "-hash",
                "refusal": "INVALID_AUTHORITY_CONTEXT",
            },
            compare(
                resolved(name + "-hash"),
                resolved(name, "source_content_digest"),
                "MISBOUND_AUTHORITY_CONTEXT",
                "DIGEST",
            ),
            compare(
                content(name, "id"), resolved(name, "id"), "WRONG_AUTHORITY_CONTEXT_ID"
            ),
        ]
        for (group, field), (target, kind) in COORDINATES.items():
            if group == "domain":
                steps.append(
                    compare(
                        content(name, group, field),
                        ref("current", "context", "value", target),
                        "STALE_AUTHORITY_DOMAIN",
                        kind,
                    )
                )
    steps += [
        compare(
            content("current_context", "action_acceptance_head"),
            ref("current", "context", "value", "action_acceptance_head"),
            "STALE_AUTHORITY_ACTION",
            "HEAD",
        ),
        compare(
            content("original_context", "action_acceptance_head"),
            resolved("proposal", "base_acceptance_head"),
            "WRONG_ORIGINAL_ACTION_HEAD",
            "HEAD",
        ),
        compare(
            resolved("epistemic", "proposal_id"),
            resolved("proposal", "id"),
            "WRONG_ACCEPTED_PROPOSAL",
        ),
        compare(
            resolved("epistemic", "proposal_content_hash"),
            resolved("proposal", "content_hash"),
            "WRONG_ACCEPTED_PROPOSAL_HASH",
            "DIGEST",
        ),
        compare(
            resolved("epistemic", "epistemic_verdict"),
            setting("accept"),
            "ACTION_NOT_ACCEPTED",
        ),
        compare(
            content("original_context", "proposal_id"),
            resolved("proposal", "id"),
            "WRONG_AUTHORITY_PROPOSAL",
        ),
        compare(
            content("original_context", "action_id"),
            resolved("action", "id"),
            "WRONG_AUTHORITY_ACTION",
        ),
    ]
    for index, key, value, kind in (
        ("proposal_states", resolved("proposal", "id"), setting("accepted"), "STRING"),
        (
            "context_by_proposal",
            resolved("proposal", "id"),
            resolved("original_context", "id"),
            "STRING",
        ),
        (
            "epistemic_decisions",
            resolved("proposal", "id"),
            resolved("epistemic", "id"),
            "STRING",
        ),
        (
            "current_contexts",
            resolved("current_context", "id"),
            resolved("current_context", "source_content_digest"),
            "DIGEST",
        ),
        (
            "authorization_states",
            resolved("action", "id"),
            setting("pending"),
            "STRING",
        ),
    ):
        steps += [
            compare(
                ref("current", "state", "value", "protocol", index, 0, "keys", 0),
                key,
                "WRONG_AUTHORITY_STATE_KEY",
            ),
            compare(
                ref("current", "state", "value", "protocol", index, 0, "value"),
                value,
                "WRONG_AUTHORITY_STATE",
                kind,
            ),
        ]
    for name in ("original_context", "current_context"):
        for field, target, kind in (
            ("id", "id", "STRING"),
            ("record_hash", "content_hash", "DIGEST"),
        ):
            steps.append(
                compare(
                    content(name, "authorization_policy", field),
                    resolved("authorization_policy", target),
                    "WRONG_AUTHORITY_POLICY",
                    kind,
                )
            )
    for field, target, kind in (
        ("authorization_policy_id", "id", "STRING"),
        ("authorization_policy_hash", "content_hash", "DIGEST"),
    ):
        steps.append(
            compare(
                resolved("action", field),
                resolved("authorization_policy", target),
                "WRONG_ACTION_POLICY",
                kind,
            )
        )
    steps += [
        compare(
            resolved("monitor", "assessment_kind"),
            setting("kind"),
            "WRONG_AUTHORITY_MONITOR_KIND",
        ),
        {
            "opcode": "REQUIRE_MEMBER",
            "value_kind": "STRING",
            "value": resolved("monitor", "id"),
            "members": resolved("authorization_policy", "required_monitor_ids"),
            "refusal": "UNSELECTED_AUTHORITY_MONITOR",
        },
    ]
    for ordinal in range(2):
        for field, target, kind in (
            ("id", "input_artifact_ids", "STRING"),
            ("content_hash", "input_artifact_record_hashes", "DIGEST"),
        ):
            steps.append(
                compare(
                    resolved("static" + str(ordinal), field),
                    resolved("monitor", target, ordinal),
                    "WRONG_AUTHORITY_STATIC_INPUT",
                    kind,
                )
            )
    for name, kind in kinds.items():
        steps += [
            {
                "opcode": "VALIDATE_RECORD",
                "record": record(name),
                "contract": setting("contracts", kind),
                "result": name + "-validated",
                "refusal": "INVALID_AUTHORITY_RECORD",
            },
            {
                "opcode": "HASH",
                "recipe": "RECORD",
                "value": record(name),
                "record_type": supplied(name, "value", 0, "record_type"),
                "result": name + "-hash",
                "refusal": "INVALID_AUTHORITY_HASH",
            },
            compare(
                resolved(name + "-hash"),
                record(name, "content_hash"),
                "WRONG_AUTHORITY_HASH",
                "DIGEST",
            ),
            compare(
                record(name, "responsible_role"),
                setting("role"),
                "WRONG_AUTHORITY_ROLE",
            ),
            compare(
                record(name, "base_acceptance_head"),
                ref("current", "context", "value", "action_acceptance_head"),
                "STALE_AUTHORITY_OUTPUT",
                "HEAD",
            ),
            compare(
                record(name, "evaluated_actor_id"),
                supplied("executor_id"),
                "WRONG_AUTHORITY_EXECUTOR",
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
                    "MISBOUND_AUTHORITY_METADATA",
                )
            )
        for field, role, target, comparison in (
            ("proposal_id", "proposal", "id", "STRING"),
            ("proposal_content_hash", "proposal", "content_hash", "DIGEST"),
            ("action_proposal_id", "action", "id", "STRING"),
            ("action_content_hash", "action", "content_hash", "DIGEST"),
            ("monitor_id", "monitor", "id", "STRING"),
            ("monitor_hash", "monitor", "content_hash", "DIGEST"),
            ("monitor_version", "monitor", "artifact_version", "STRING"),
            ("authority_policy_id", "authorization_policy", "id", "STRING"),
            ("authority_policy_hash", "authorization_policy", "content_hash", "DIGEST"),
            ("evaluated_authority_grant_id", "grant", "id", "STRING"),
            ("evaluated_authority_grant_hash", "grant", "content_hash", "DIGEST"),
        ):
            steps.append(
                compare(
                    record(name, field),
                    resolved(role, target),
                    "MISBOUND_AUTHORITY_OUTPUT",
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
                        "WRONG_AUTHORITY_CLOSURE",
                    )
                )
    if unavailable:
        steps += [
            compare(
                record("assessment", "monitor_failure_id"),
                record("failure", "id"),
                "WRONG_AUTHORITY_FAILURE",
            ),
            compare(
                record("assessment", "source_record_ids", len(CLOSURE)),
                record("failure", "id"),
                "MISSING_AUTHORITY_FAILURE",
            ),
        ]
    fields = (
        "action_proposal_id",
        "evaluated_actor_id",
        "base_acceptance_head",
        "monitor_id",
        "evaluated_authority_grant_id",
    )
    steps.append(
        {
            "opcode": "REQUIRE_UNIQUE",
            "records": supplied("assessment", "value"),
            "key_paths": [["record", field] for field in fields],
            "target_index": "authority_assessments",
            "refusal": "DUPLICATE_AUTHORITY_ASSESSMENT",
        }
    )
    for name in kinds:
        steps.append(
            {
                "opcode": "INTRODUCE_RECORDS",
                "records": supplied(name, "value"),
                "dependencies": supplied(name + "_dependencies", "value"),
                "result": "introduced-" + name,
                "refusal": "INVALID_AUTHORITY_INTRODUCTION",
            }
        )
    steps.append(
        {
            "opcode": "SET_PROTOCOL_STATE",
            "target": "PROTOCOL_INDEX",
            "name": "authority_assessments",
            "keys": [record("assessment", field) for field in fields],
            "value": record("assessment", "id"),
            "refusal": "INVALID_AUTHORITY_INDEX",
        }
    )
    return {
        "name": "admit-authority-unavailable"
        if unavailable
        else "admit-authority-completed",
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
