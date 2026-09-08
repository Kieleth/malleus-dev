"""Finite action-only authorization control. No dispatch or effect is implied."""

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
from research.action_history_contract_freeze.programs.decision_bundle import strings
from research.action_history_contract_freeze.programs.registration_bundle import (
    obj,
    ref,
    compare,
)


RECIPE = "ASSENT_AUTHORIZATION_CONTROL_V1"
TARGETS = {
    "AUTHORIZE": "AUTHORIZED",
    "BLOCK": "BLOCKED",
    "CLARIFY": "CLARIFICATION_REQUIRED",
}


def _assessment_schema(catalog):
    completed, unavailable = (
        catalog["AuthorityAssessment"],
        catalog["UnavailableAuthorityAssessment"],
    )
    schema = deepcopy(completed)
    schema["properties"].update(deepcopy(unavailable["properties"]))
    schema["required"] = sorted(
        set(completed["required"]) & set(unavailable["required"])
    )
    schema["properties"]["assessment_outcome"] = {
        **TEXT,
        "enum": ["SATISFIED", "VIOLATED", "UNKNOWN"],
    }
    schema["properties"]["source_record_ids"] = strings(minItems=11, maxItems=12)
    return schema


def add_authorization(bundle):
    bundle = deepcopy(bundle)
    catalog = bundle["profile"]["record_schemas"]
    assessment = _assessment_schema(catalog)
    # Resolution uses the abstract Assessment root and still validates each
    # concrete applied record with the compiled contract. Event inputs retain
    # their narrower TYPE or AUTHORITY shape; no fields are dropped or cast.
    broad = catalog["Assessment"]
    required = sorted(set(broad["required"]) & set(assessment["required"]))
    broad["properties"].update(deepcopy(assessment["properties"]))
    broad["required"] = required
    broad["properties"]["assessment_kind"] = {**TEXT, "enum": ["TYPE", "AUTHORITY"]}
    broad["properties"]["responsible_role"] = TEXT
    broad["properties"]["source_record_ids"] = strings(minItems=6, maxItems=12)
    broad["properties"]["input_record_ids"] = strings(minItems=6, maxItems=11)
    head = deepcopy(catalog["ProposedSubgraph"]["properties"]["base_acceptance_head"])
    base = catalog["EpistemicDecision"]["properties"]
    fields = {
        k: deepcopy(base[k])
        for k in (
            "id",
            "content_hash",
            "generation_event_id",
            "generated_at",
            "responsible_actor_id",
            "responsible_role",
            "base_acceptance_head",
            "policy_id",
            "policy_hash",
            "rationale_codes",
            "rationale",
        )
    }
    fields.update(
        source_record_ids=strings(minItems=6, maxItems=6),
        action_proposal_id=TEXT,
        action_content_hash=DIGEST,
        authorization_verdict={**TEXT, "enum": list(TARGETS)},
        epistemic_decision_ids=array(TEXT, 1),
        relied_on_claim_version_ids=strings(maxItems=0),
        authority_assessment_ids=array(TEXT, 2),
        triggered_assessment_ids=strings(maxItems=2),
        policy_evaluation_hash=DIGEST,
        authority_grant_id=TEXT,
        authority_grant_hash=DIGEST,
        authorized_actor_id=TEXT,
    )
    # Dates are explicit event-local variants, not a null/date union grammar.
    catalog["AuthorizationDecision"] = obj(
        **fields,
        authorization_valid_from={**TEXT, "format": "aware-instant"},
        authorization_valid_to={**TEXT, "format": "aware-instant"},
    )
    for name in ("required_monitor_ids", "required_monitor_record_hashes"):
        catalog["AuthorizationPolicyArtifact"]["properties"][name].update(
            minItems=2, maxItems=2
        )
    bundle["profile"]["targets"]["authorization_decisions"] = {
        "target": "PROTOCOL_INDEX",
        "storage_path": ["protocol", "authorization_decisions"],
        "key_schemas": [deepcopy(TEXT)],
        "value_schema": deepcopy(TEXT),
    }
    bundle["profile"]["capabilities"].append(RECIPE)
    constants = {
        "targets": TARGETS,
        "monitor_type": "MonitorSpecificationArtifact",
        "assessment_type": "Assessment",
        "roles": {"decision": "authorizer", "transition": "state-controller"},
        "contracts": {
            kind: {
                "contract_identity": digest(raw(bundle["record_contract_base64"])),
                "record_type": kind,
            }
            for kind in ("AuthorizationDecision", "TransitionRecord")
        },
    }
    cs = obj(
        targets=obj(**{k: {**TEXT, "const": v} for k, v in TARGETS.items()}),
        monitor_type={**TEXT, "const": constants["monitor_type"]},
        assessment_type={**TEXT, "const": "Assessment"},
        roles=obj(**{k: {**TEXT, "const": v} for k, v in constants["roles"].items()}),
        contracts=obj(
            **{
                k: obj(contract_identity=DIGEST, record_type={**TEXT, "const": k})
                for k in constants["contracts"]
            }
        ),
    )
    bundle["constants"]["authorization_decision"] = constants
    for transaction in bundle["transactions"].values():
        inputs = transaction["program"]["inputs"]
        schemas = inputs["artifact"]["constants"]["properties"]["value"]
        schemas["properties"]["authorization_decision"] = deepcopy(cs)
        schemas["required"].append("authorization_decision")
        if "state" in inputs["current"]:
            inputs["current"]["state"]["properties"]["value"]["properties"]["protocol"][
                "properties"
            ]["authorization_decisions"] = {
                "type": "array",
                "items": obj(keys=array(TEXT, 1), value=TEXT),
            }
    for verdict in TARGETS:
        bundle["transactions"]["authorization-" + verdict.lower()] = {
            "event_types": ["AUTHORIZATION_DECIDED"],
            "program": _program(bundle, fields, assessment, head, verdict),
        }
    return load_bundle(canonical(bundle))


def _program(bundle, fields, assessment, head, verdict):
    prior = bundle["transactions"]["authority-completed"]["program"]
    inputs = deepcopy(prior["inputs"])
    # The preceding named context checks resolve ACCEPT, A/D, policies and
    # retained inputs. Stop before output validation or introduction, not after
    # an effect. The conformance test guards this read-only prefix.
    boundary = next(
        i
        for i, step in enumerate(prior["steps"])
        if step["opcode"] == "VALIDATE_RECORD"
    )
    steps = deepcopy(prior["steps"][:boundary])
    data = inputs["event"]["0"]["properties"]["data"]
    for key in ("assessment", "assessment_dependencies"):
        del data["properties"][key]
        data["required"].remove(key)
    instant = {**TEXT, "format": "aware-instant"}
    decision = obj(
        **deepcopy(fields),
        authorization_valid_from=instant
        if verdict == "AUTHORIZE"
        else {"type": "null"},
        authorization_valid_to=instant if verdict == "AUTHORIZE" else {"type": "null"},
    )
    decision["properties"]["authorization_verdict"]["const"] = verdict
    bindings = obj(
        proposal_id=TEXT,
        proposal_content_hash=DIGEST,
        base_acceptance_head=head,
        action_proposal_id=TEXT,
        action_content_hash=DIGEST,
        evaluated_actor_id=TEXT,
        authority_policy_id=TEXT,
        authority_policy_hash=DIGEST,
    )
    extra = {
        "outputs": array(assessment, 2),
        "control": obj(
            recipe={**TEXT, "const": RECIPE},
            monitors=array(
                bundle["profile"]["record_schemas"]["MonitorSpecificationArtifact"], 2
            ),
            bindings=bindings,
        ),
    }
    for name, kind, schema in (
        ("decision", "AuthorizationDecision", decision),
        (
            "transition",
            "TransitionRecord",
            bundle["profile"]["record_schemas"]["TransitionRecord"],
        ),
    ):
        extra[name] = obj(
            value=array(obj(record_type={**TEXT, "const": kind}, record=schema), 1)
        )
        extra[name + "_dependencies"] = obj(value=strings())
    if verdict == "AUTHORIZE":
        extra["intervals"] = obj(
            authorization=obj(start=instant, end=instant),
            grant=obj(start=instant, end=instant),
        )
    data["properties"].update(extra)
    data["required"].extend(extra)
    indexes = inputs["current"]["state"]["properties"]["value"]["properties"][
        "protocol"
    ]
    indexes["required"].append("authority_assessments")
    indexes["properties"]["authority_assessments"].update(minItems=2, maxItems=2)

    def setting(*path):
        return ref("artifact", "constants", "value", "authorization_decision", *path)

    def supplied(*path):
        return ref("event", "0", "data", *path)

    def resolved(name, *path):
        return ref("result", name, "value", *path)

    def record(name, *path):
        return supplied(name, "value", 0, "record", *path)

    def same(name, left, right, reason):
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

    for field, expected, kind in (
        ("proposal_id", resolved("proposal", "id"), "STRING"),
        ("proposal_content_hash", resolved("proposal", "content_hash"), "DIGEST"),
        (
            "base_acceptance_head",
            ref("current", "context", "value", "action_acceptance_head"),
            "HEAD",
        ),
        ("action_proposal_id", resolved("action", "id"), "STRING"),
        ("action_content_hash", resolved("action", "content_hash"), "DIGEST"),
        ("evaluated_actor_id", supplied("executor_id"), "STRING"),
        ("authority_policy_id", resolved("authorization_policy", "id"), "STRING"),
        (
            "authority_policy_hash",
            resolved("authorization_policy", "content_hash"),
            "DIGEST",
        ),
    ):
        steps.append(
            compare(
                supplied("control", "bindings", field),
                expected,
                "MISBOUND_AUTHORIZATION_CONTROL",
                kind,
            )
        )
    for ordinal in range(2):
        monitor, output = (
            "control-monitor" + str(ordinal),
            "control-output" + str(ordinal),
        )
        for name, identifier, identity, kind in (
            (
                monitor,
                resolved("authorization_policy", "required_monitor_ids", ordinal),
                resolved(
                    "authorization_policy", "required_monitor_record_hashes", ordinal
                ),
                "monitor_type",
            ),
            (
                output,
                supplied("outputs", ordinal, "id"),
                supplied("outputs", ordinal, "content_hash"),
                "assessment_type",
            ),
        ):
            steps.append(
                {
                    "opcode": "RESOLVE_RECORD",
                    "scope": "APPLIED",
                    "record_id": identifier,
                    "record_hash": identity,
                    "record_type": setting(kind),
                    "result": name,
                    "refusal": "UNAPPLIED_AUTHORIZATION_INPUT",
                }
            )
        steps += same(
            monitor,
            supplied("control", "monitors", ordinal),
            resolved(monitor),
            "FORGED_AUTHORIZATION_MONITOR",
        )
        steps += same(
            output,
            supplied("outputs", ordinal),
            resolved(output),
            "FORGED_AUTHORIZATION_OUTPUT",
        )
        keys = [
            resolved("action", "id"),
            supplied("executor_id"),
            ref("current", "context", "value", "action_acceptance_head"),
            resolved(monitor, "id"),
            resolved("grant", "id"),
        ]
        for key, expected in enumerate(keys):
            actual = ref(
                "current",
                "state",
                "value",
                "protocol",
                "authority_assessments",
                ordinal,
                "keys",
                key,
            )
            # The persisted tuple uses a homogeneous string-list schema.
            # Exact VALUE equality preserves the head bytes without casting
            # that list element into an action-head coordinate.
            if key == 2:
                steps += same(
                    "authority-head-key-" + str(ordinal),
                    actual,
                    expected,
                    "WRONG_APPLIED_AUTHORITY_KEY",
                )
            else:
                steps.append(compare(actual, expected, "WRONG_APPLIED_AUTHORITY_KEY"))
        steps.append(
            compare(
                ref(
                    "current",
                    "state",
                    "value",
                    "protocol",
                    "authority_assessments",
                    ordinal,
                    "value",
                ),
                supplied("outputs", ordinal, "id"),
                "WRONG_APPLIED_AUTHORITY_OUTPUT",
            )
        )
        for field, target, kind in (
            ("evaluated_authority_grant_id", "id", "STRING"),
            ("evaluated_authority_grant_hash", "content_hash", "DIGEST"),
        ):
            steps.append(
                compare(
                    supplied("outputs", ordinal, field),
                    resolved("grant", target),
                    "WRONG_ASSESSED_AUTHORIZATION_GRANT",
                    kind,
                )
            )
    steps.append(
        {
            "opcode": "SELECT_CONTROL",
            "policy": resolved("authorization_policy"),
            "outputs": supplied("outputs"),
            "context": supplied("control"),
            "result": "control",
            "refusal": "INVALID_AUTHORIZATION_CONTROL",
        }
    )
    steps += [
        compare(
            record("decision", "authorization_verdict"),
            resolved("control", "verdict"),
            "FORGED_AUTHORIZATION_VERDICT",
        ),
        compare(
            record("decision", "policy_evaluation_hash"),
            resolved("control", "evaluation_hash"),
            "FORGED_AUTHORIZATION_EVALUATION",
            "DIGEST",
        ),
    ]
    for field, target in (
        ("authority_assessment_ids", "assessment_ids"),
        ("triggered_assessment_ids", "triggered_assessment_ids"),
    ):
        steps += same(
            field,
            record("decision", field),
            resolved("control", target),
            "WRONG_AUTHORIZATION_ASSESSMENT_ORDER",
        )
    for field, expected, kind in (
        (
            "base_acceptance_head",
            ref("current", "context", "value", "action_acceptance_head"),
            "HEAD",
        ),
        ("action_proposal_id", resolved("action", "id"), "STRING"),
        ("action_content_hash", resolved("action", "content_hash"), "DIGEST"),
        ("policy_id", resolved("authorization_policy", "id"), "STRING"),
        ("policy_hash", resolved("authorization_policy", "content_hash"), "DIGEST"),
        ("authority_grant_id", resolved("grant", "id"), "STRING"),
        ("authority_grant_hash", resolved("grant", "content_hash"), "DIGEST"),
        ("authorized_actor_id", supplied("executor_id"), "STRING"),
    ):
        steps.append(
            compare(
                record("decision", field),
                expected,
                "MISBOUND_AUTHORIZATION_DECISION",
                kind,
            )
        )
    steps.append(
        compare(
            record("decision", "epistemic_decision_ids", 0),
            resolved("epistemic", "id"),
            "WRONG_AUTHORIZATION_ACCEPT",
        )
    )
    if verdict == "AUTHORIZE":
        steps += [
            compare(
                record("decision", "authorized_actor_id"),
                resolved("grant", "grantee_actor_id"),
                "WRONG_AUTHORIZED_GRANTEE",
            ),
            {
                "opcode": "REQUIRE_MEMBER",
                "value_kind": "STRING",
                "value": resolved("action", "action_type"),
                "members": resolved("grant", "permitted_action_types"),
                "refusal": "ACTION_TYPE_NOT_PERMITTED",
            },
        ]
        for role, start, end in (
            (
                "authorization",
                record("decision", "authorization_valid_from"),
                record("decision", "authorization_valid_to"),
            ),
            (
                "grant",
                resolved("grant", "grant_valid_from"),
                resolved("grant", "grant_valid_to"),
            ),
        ):
            steps += [
                compare(
                    supplied("intervals", role, "start"),
                    start,
                    "MISBOUND_AUTHORIZATION_INTERVAL",
                ),
                compare(
                    supplied("intervals", role, "end"),
                    end,
                    "MISBOUND_AUTHORIZATION_INTERVAL",
                ),
            ]
        steps.append(
            {
                "opcode": "REQUIRE_INTERVAL",
                "inner": supplied("intervals", "authorization"),
                "outer": supplied("intervals", "grant"),
                "refusal": "AUTHORIZATION_EXCEEDS_GRANT",
            }
        )
    for name, kind in (
        ("decision", "AuthorizationDecision"),
        ("transition", "TransitionRecord"),
    ):
        steps += [
            {
                "opcode": "VALIDATE_RECORD",
                "record": record(name),
                "contract": setting("contracts", kind),
                "result": name + "-validated",
                "refusal": "INVALID_AUTHORIZATION_RECORD",
            },
            {
                "opcode": "HASH",
                "recipe": "RECORD",
                "value": record(name),
                "record_type": supplied(name, "value", 0, "record_type"),
                "result": name + "-hash",
                "refusal": "INVALID_AUTHORIZATION_HASH",
            },
            compare(
                resolved(name + "-hash"),
                record(name, "content_hash"),
                "WRONG_AUTHORIZATION_HASH",
                "DIGEST",
            ),
            compare(
                record(name, "responsible_role"),
                setting("roles", name),
                "WRONG_AUTHORIZATION_ROLE",
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
                    "MISBOUND_AUTHORIZATION_METADATA",
                )
            )
    for field, expected, kind in (
        ("transition_subject_id", resolved("action", "id"), "STRING"),
        (
            "from_state",
            ref("artifact", "constants", "value", "authority_assessment", "pending"),
            "STRING",
        ),
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
                "MISBOUND_AUTHORIZATION_TRANSITION",
                kind,
            )
        )
    steps.append(
        compare(
            record("transition", "source_record_ids", 0),
            record("decision", "id"),
            "MISSING_AUTHORIZATION_PROVENANCE",
        )
    )
    for role in (
        "action",
        "authorization_policy",
        "epistemic",
        "grant",
        "control-output0",
        "control-output1",
    ):
        steps.append(
            {
                "opcode": "REQUIRE_MEMBER",
                "value_kind": "STRING",
                "value": resolved(role, "id"),
                "members": record("decision", "source_record_ids"),
                "refusal": "MISSING_AUTHORIZATION_PROVENANCE",
            }
        )
    for name in ("decision", "transition"):
        steps.append(
            {
                "opcode": "INTRODUCE_RECORDS",
                "records": supplied(name, "value"),
                "dependencies": supplied(name + "_dependencies", "value"),
                "result": "introduced-" + name,
                "refusal": "INVALID_AUTHORIZATION_INTRODUCTION",
            }
        )
    for name, value in (
        ("authorization_states", setting("targets", verdict)),
        ("authorization_decisions", record("decision", "id")),
    ):
        steps.append(
            {
                "opcode": "SET_PROTOCOL_STATE",
                "target": "PROTOCOL_INDEX",
                "name": name,
                "keys": [resolved("action", "id")],
                "value": value,
                "refusal": "INVALID_AUTHORIZATION_STATE",
            }
        )
    return {
        "name": "authorize-action-" + verdict.lower(),
        "inputs": inputs,
        "required_capabilities": [RECIPE],
        "introductions": [
            {"name": "decision", "depends_on": []},
            {"name": "transition", "depends_on": ["decision"]},
        ],
        "steps": steps,
    }
