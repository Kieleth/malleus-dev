"""Deterministic Stage 6 monitoring-policy guardrails."""

import pytest

from malleus.control import (
    AuthorizationEvaluation,
    ControlError,
    MonitoringError,
    authority_monitor_failure_records,
    authorization_policy_digest,
    authorization_policy_requirements,
    build_monitor_failure_records,
    epistemic_policy_digest,
    evaluate_authorization_policy,
    evaluate_epistemic_policy,
    monitor_failure_records,
    monitor_specification_digest,
    policy_requirements,
)
from malleus.protocol import content_digest, record_hash


DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64
DIGEST_C = "sha256:" + "c" * 64
PROPOSAL_HASH = "sha256:" + "d" * 64
BASE_HEAD = "sha256:" + "e" * 64
ACTION_HASH = "sha256:" + "f" * 64


def monitor(monitor_id: str, kind: str) -> dict:
    record = {
        "id": monitor_id,
        "artifact_version": "1",
        "assessment_kind": kind,
    }
    record["content_hash"] = content_digest(record)
    return record


def policy(requirements, *, precedence=None) -> dict:
    ordered = sorted(requirements, key=lambda item: item[0]["id"])
    value = {
        "id": "policy:1",
        "required_monitor_ids": [item[0]["id"] for item in ordered],
        "required_monitor_record_hashes": [item[0]["content_hash"] for item in ordered],
        "violation_verdicts": [item[1] for item in ordered],
        "unknown_verdicts": [item[2] for item in ordered],
        "control_precedence": precedence or ["REJECT", "CONTEST", "DEFER"],
    }
    value["content_hash"] = content_digest(value)
    return value


def assessment(monitor_record: dict, outcome: str, *, suffix: str = "1") -> dict:
    value = {
        "id": f"assessment:{suffix}",
        "proposal_id": "proposal:1",
        "proposal_content_hash": PROPOSAL_HASH,
        "base_acceptance_head": BASE_HEAD,
        "assessment_kind": monitor_record["assessment_kind"],
        "assessment_outcome": outcome,
        "monitor_id": monitor_record["id"],
        "monitor_version": monitor_record["artifact_version"],
        "monitor_hash": monitor_record["content_hash"],
    }
    value["content_hash"] = content_digest(value)
    return value


def evaluate(policy_record: dict, monitors: list[dict], assessments: list[dict]):
    return evaluate_epistemic_policy(
        policy_record,
        {item["id"]: item for item in monitors},
        assessments,
        proposal_id="proposal:1",
        proposal_content_hash=PROPOSAL_HASH,
        base_acceptance_head=BASE_HEAD,
    )


def authority_monitor(monitor_id: str) -> dict:
    record = {
        "id": monitor_id,
        "artifact_kind": "MONITOR_SPECIFICATION",
        "artifact_version": "1",
        "monitor_schema_version": "1",
        "assessment_kind": "AUTHORITY",
        "monitor_implementation_hash": DIGEST_A,
        "input_artifact_ids": ["artifact:authority-rules"],
        "input_artifact_record_hashes": [DIGEST_B],
    }
    record["artifact_hash"] = monitor_specification_digest(
        schema_version=record["monitor_schema_version"],
        monitor_id=record["id"],
        monitor_version=record["artifact_version"],
        assessment_kind=record["assessment_kind"],
        implementation_hash=record["monitor_implementation_hash"],
        input_artifact_ids=record["input_artifact_ids"],
        input_artifact_record_hashes=record["input_artifact_record_hashes"],
    )
    record["content_hash"] = content_digest(record)
    return record


def authorization_policy(monitors: list[dict], *, policy_id: str = "policy:authority") -> dict:
    ordered = sorted(monitors, key=lambda item: item["id"])
    record = {
        "id": policy_id,
        "artifact_kind": "AUTHORIZATION_POLICY",
        "artifact_version": "1",
        "policy_schema_version": "1",
        "required_monitor_ids": [item["id"] for item in ordered],
        "required_monitor_record_hashes": [item["content_hash"] for item in ordered],
    }
    record["artifact_hash"] = authorization_policy_digest(
        schema_version=record["policy_schema_version"],
        policy_id=record["id"],
        policy_version=record["artifact_version"],
        required_monitor_ids=record["required_monitor_ids"],
        required_monitor_record_hashes=record["required_monitor_record_hashes"],
    )
    record["content_hash"] = content_digest(record)
    return record


def authority_assessment(
    monitor_record: dict,
    policy_record: dict,
    outcome: str,
    *,
    suffix: str = "1",
    proposal_id: str = "proposal:1",
    proposal_hash: str = PROPOSAL_HASH,
    action_id: str = "action:1",
    action_hash: str = ACTION_HASH,
    actor_id: str = "actor:executor",
    acceptance_head: str = BASE_HEAD,
) -> dict:
    record = {
        "id": f"assessment:authority:{suffix}",
        "proposal_id": proposal_id,
        "proposal_content_hash": proposal_hash,
        "action_proposal_id": action_id,
        "action_content_hash": action_hash,
        "evaluated_actor_id": actor_id,
        "base_acceptance_head": acceptance_head,
        "authority_policy_id": policy_record["id"],
        "authority_policy_hash": policy_record["content_hash"],
        "assessment_kind": "AUTHORITY",
        "assessment_outcome": outcome,
        "monitor_id": monitor_record["id"],
        "monitor_version": monitor_record["artifact_version"],
        "monitor_hash": monitor_record["content_hash"],
    }
    record["content_hash"] = content_digest(record)
    return record


def evaluate_authority(
    policy_record: dict,
    monitors: list[dict],
    assessments: list[dict],
    *,
    proposal_id: str = "proposal:1",
    proposal_hash: str = PROPOSAL_HASH,
    action_id: str = "action:1",
    action_hash: str = ACTION_HASH,
    actor_id: str = "actor:executor",
    acceptance_head: str = BASE_HEAD,
) -> AuthorizationEvaluation:
    return evaluate_authorization_policy(
        policy_record,
        {item["id"]: item for item in monitors},
        assessments,
        proposal_id=proposal_id,
        proposal_content_hash=proposal_hash,
        action_id=action_id,
        action_content_hash=action_hash,
        evaluated_actor_id=actor_id,
        base_acceptance_head=acceptance_head,
    )


def test_monitor_digest_binds_kind_implementation_and_inputs():
    base = dict(
        schema_version="1",
        monitor_id="monitor:1",
        monitor_version="1",
        assessment_kind="TYPE",
        implementation_hash=DIGEST_A,
        input_artifact_ids=["contract:1"],
        input_artifact_record_hashes=[DIGEST_B],
    )
    first = monitor_specification_digest(**base)
    assert first.startswith("sha256:")
    assert first != monitor_specification_digest(**{**base, "assessment_kind": "CONFLICT"})
    assert first != monitor_specification_digest(
        **{**base, "input_artifact_record_hashes": [DIGEST_C]}
    )


@pytest.mark.parametrize(
    "mutation,message",
    [
        (lambda value: value["required_monitor_record_hashes"].append(DIGEST_A), "equal lengths"),
        (
            lambda value: value.update({
                "required_monitor_ids": ["monitor:2", "monitor:1"],
                "required_monitor_record_hashes": [DIGEST_A, DIGEST_B],
                "violation_verdicts": ["REJECT", "REJECT"],
                "unknown_verdicts": ["DEFER", "DEFER"],
            }),
            "canonical",
        ),
        (lambda value: value["unknown_verdicts"].__setitem__(0, "REJECT"), "UNKNOWN verdict"),
        (lambda value: value["control_precedence"].remove("DEFER"), "must contain"),
    ],
)
def test_policy_shape_fails_loudly(mutation, message):
    monitor_record = monitor("monitor:1", "TYPE")
    value = policy([(monitor_record, "REJECT", "DEFER")])
    mutation(value)
    with pytest.raises(ControlError, match=message):
        policy_requirements(value)


def test_policy_digest_binds_rules_monitors_mappings_and_precedence():
    monitor_record = monitor("monitor:1", "TYPE")
    fields = dict(
        schema_version="1",
        policy_id="policy:1",
        policy_version="1",
        ruleset_id="rules:1",
        ruleset_record_hash=DIGEST_A,
        ruleset_artifact_hash=DIGEST_B,
        required_monitor_ids=[monitor_record["id"]],
        required_monitor_record_hashes=[monitor_record["content_hash"]],
        violation_verdicts=["REJECT"],
        unknown_verdicts=["DEFER"],
        control_precedence=["REJECT", "CONTEST", "DEFER"],
    )
    first = epistemic_policy_digest(**fields)
    assert first != epistemic_policy_digest(
        **{**fields, "violation_verdicts": ["CONTEST"]}
    )
    assert first != epistemic_policy_digest(
        **{**fields, "control_precedence": ["CONTEST", "REJECT", "DEFER"]}
    )


def test_all_required_satisfied_selects_accept_without_triggers():
    type_monitor = monitor("monitor:type", "TYPE")
    conflict_monitor = monitor("monitor:conflict", "CONFLICT")
    policy_record = policy([
        (type_monitor, "REJECT", "DEFER"),
        (conflict_monitor, "CONTEST", "DEFER"),
    ])
    result = evaluate(
        policy_record,
        [type_monitor, conflict_monitor],
        [assessment(type_monitor, "SATISFIED", suffix="type"),
         assessment(conflict_monitor, "SATISFIED", suffix="conflict")],
    )
    assert result.verdict == "ACCEPT"
    assert result.triggered_assessment_ids == ()
    assert result.evaluation_hash.startswith("sha256:")


def test_precedence_resolves_multiple_triggered_controls_deterministically():
    type_monitor = monitor("monitor:type", "TYPE")
    conflict_monitor = monitor("monitor:conflict", "CONFLICT")
    policy_record = policy([
        (type_monitor, "REJECT", "DEFER"),
        (conflict_monitor, "CONTEST", "DEFER"),
    ], precedence=["CONTEST", "REJECT", "DEFER"])
    result = evaluate(
        policy_record,
        [type_monitor, conflict_monitor],
        [assessment(type_monitor, "VIOLATED", suffix="type"),
         assessment(conflict_monitor, "VIOLATED", suffix="conflict")],
    )
    assert result.verdict == "CONTEST"
    assert result.triggered_assessment_ids == (
        "assessment:conflict",
        "assessment:type",
    )


def test_unknown_selects_declared_nonaccept_control():
    monitor_record = monitor("monitor:type", "TYPE")
    policy_record = policy([(monitor_record, "REJECT", "DEFER")])
    result = evaluate(
        policy_record,
        [monitor_record],
        [assessment(monitor_record, "UNKNOWN")],
    )
    assert result.verdict == "DEFER"
    assert result.triggered_assessment_ids == ("assessment:1",)


@pytest.mark.parametrize(
    "assessments,message",
    [
        ([], "has no assessment"),
        ([{"monitor_id": "monitor:other"}], "has no assessment|unrequired monitor"),
    ],
)
def test_missing_or_unrequired_monitor_output_cannot_be_omitted(assessments, message):
    monitor_record = monitor("monitor:type", "TYPE")
    policy_record = policy([(monitor_record, "REJECT", "DEFER")])
    if assessments:
        assessments[0].update(assessment(monitor("monitor:other", "TYPE"), "SATISFIED"))
    with pytest.raises(ControlError, match=message):
        evaluate(policy_record, [monitor_record], assessments)


@pytest.mark.parametrize(
    "field,value,message",
    [
        ("monitor_hash", DIGEST_A, "monitor hash mismatch"),
        ("monitor_version", "2", "monitor version mismatch"),
        ("assessment_kind", "CONFLICT", "kind mismatch"),
        ("proposal_id", "proposal:other", "proposal_id mismatch"),
    ],
)
def test_assessment_must_match_exact_monitor_and_proposal(field, value, message):
    monitor_record = monitor("monitor:type", "TYPE")
    policy_record = policy([(monitor_record, "REJECT", "DEFER")])
    result = assessment(monitor_record, "SATISFIED")
    result[field] = value
    result["content_hash"] = content_digest(result)
    with pytest.raises(ControlError, match=message):
        evaluate(policy_record, [monitor_record], [result])


def test_monitor_mapping_key_must_match_record_id():
    monitor_record = monitor("monitor:type", "TYPE")
    policy_record = policy([(monitor_record, "REJECT", "DEFER")])
    forged = {**monitor_record, "id": "monitor:other"}
    with pytest.raises(ControlError, match="mismatched id"):
        evaluate_epistemic_policy(
            policy_record,
            {"monitor:type": forged},
            [assessment(monitor_record, "SATISFIED")],
            proposal_id="proposal:1",
            proposal_content_hash=PROPOSAL_HASH,
            base_acceptance_head=BASE_HEAD,
        )


def test_generic_monitor_failure_builds_atomic_unavailable_assessment():
    failure, unknown = monitor_failure_records(
        error=MonitoringError("monitor timed out"),
        failure_id="failure:1",
        assessment_id="assessment:1",
        event_id="event:1",
        generated_at="2026-08-12T08:00:00Z",
        actor_id="actor:monitor",
        role="type-monitor",
        proposal_id="proposal:1",
        proposal_content_hash=PROPOSAL_HASH,
        base_acceptance_head=BASE_HEAD,
        monitor_id="monitor:type",
        monitor_version="1",
        monitor_hash=DIGEST_A,
        assessment_kind="TYPE",
        failure_category="TIMEOUT",
        error_code="DEADLINE",
    )
    assert failure["failed_assessment_kind"] == "TYPE"
    assert unknown["assessment_outcome"] == "UNKNOWN"
    assert unknown["monitor_failure_id"] == failure["id"]
    assert failure["id"] in unknown["source_record_ids"]


def test_authority_monitor_failure_binds_exact_action_actor_policy_and_optional_grant():
    failure, unknown = authority_monitor_failure_records(
        error=MonitoringError("authority source unavailable"),
        failure_id="failure:authority",
        assessment_id="assessment:authority:unknown",
        event_id="event:authority",
        generated_at="2026-08-12T08:00:00Z",
        actor_id="actor:monitor",
        role="authority-monitor",
        proposal_id="proposal:1",
        proposal_content_hash=PROPOSAL_HASH,
        base_acceptance_head=BASE_HEAD,
        action_proposal_id="action:1",
        action_content_hash=ACTION_HASH,
        evaluated_actor_id="actor:executor",
        authority_policy_id="policy:authority",
        authority_policy_hash=DIGEST_B,
        monitor_id="monitor:authority",
        monitor_version="1",
        monitor_hash=DIGEST_A,
        failure_category="DEPENDENCY",
        error_code="AUTHORITY_SOURCE_UNAVAILABLE",
        evaluated_authority_grant_id="grant:1",
        evaluated_authority_grant_hash=DIGEST_C,
    )
    assert failure["action_content_hash"] == ACTION_HASH
    assert unknown["action_content_hash"] == ACTION_HASH
    assert unknown["assessment_kind"] == "AUTHORITY"
    assert {"proposal:1", "action:1", "grant:1"} == set(unknown["input_record_ids"])
    assert unknown["content_hash"] == record_hash("UnavailableAuthorityAssessment", unknown)


def test_authority_monitor_failure_rejects_partial_grant_binding():
    fields = dict(
        error=MonitoringError("authority source unavailable"),
        failure_id="failure:authority",
        assessment_id="assessment:authority:unknown",
        event_id="event:authority",
        generated_at="2026-08-12T08:00:00Z",
        actor_id="actor:monitor",
        role="authority-monitor",
        proposal_id="proposal:1",
        proposal_content_hash=PROPOSAL_HASH,
        base_acceptance_head=BASE_HEAD,
        action_proposal_id="action:1",
        action_content_hash=ACTION_HASH,
        evaluated_actor_id="actor:executor",
        authority_policy_id="policy:authority",
        authority_policy_hash=DIGEST_B,
        monitor_id="monitor:authority",
        monitor_version="1",
        monitor_hash=DIGEST_A,
        failure_category="DEPENDENCY",
        error_code="AUTHORITY_SOURCE_UNAVAILABLE",
        evaluated_authority_grant_id="grant:1",
    )
    with pytest.raises(ControlError, match="all-or-none"):
        authority_monitor_failure_records(**fields)


def test_generic_failure_helper_refuses_logical_failure_without_contract():
    fields = dict(
        error=MonitoringError("monitor failed"),
        failure_id="failure:1",
        assessment_id="assessment:1",
        event_id="event:1",
        generated_at="2026-08-12T08:00:00Z",
        actor_id="actor:monitor",
        role="logic-monitor",
        proposal_id="proposal:1",
        proposal_content_hash=PROPOSAL_HASH,
        base_acceptance_head=BASE_HEAD,
        monitor_id="monitor:logic",
        monitor_version="1",
        monitor_hash=DIGEST_A,
        assessment_kind="LOGICAL",
        failure_category="EXECUTION",
        error_code="FAILED",
    )
    with pytest.raises(ControlError, match="logic_monitor_failure_records"):
        monitor_failure_records(**fields)


def test_failure_extensions_cannot_replace_required_outcome_fields():
    with pytest.raises(ControlError, match="cannot replace"):
        build_monitor_failure_records(
            error=MonitoringError("monitor failed"),
            failure_id="failure:1",
            assessment_id="assessment:1",
            event_id="event:1",
            generated_at="2026-08-12T08:00:00Z",
            actor_id="actor:monitor",
            role="type-monitor",
            proposal_id="proposal:1",
            proposal_content_hash=PROPOSAL_HASH,
            base_acceptance_head=BASE_HEAD,
            monitor_id="monitor:type",
            monitor_version="1",
            monitor_hash=DIGEST_A,
            assessment_kind="TYPE",
            failure_category="EXECUTION",
            error_code="FAILED",
            assessment_fields={"assessment_outcome": "SATISFIED"},
        )


def test_monitor_failure_and_unavailable_assessment_ids_must_differ():
    with pytest.raises(ControlError, match="must differ"):
        monitor_failure_records(
            error=MonitoringError("monitor failed"),
            failure_id="record:same",
            assessment_id="record:same",
            event_id="event:1",
            generated_at="2026-08-12T08:00:00Z",
            actor_id="actor:monitor",
            role="type-monitor",
            proposal_id="proposal:1",
            proposal_content_hash=PROPOSAL_HASH,
            base_acceptance_head=BASE_HEAD,
            monitor_id="monitor:type",
            monitor_version="1",
            monitor_hash=DIGEST_A,
            assessment_kind="TYPE",
            failure_category="EXECUTION",
            error_code="FAILED",
        )


def test_authorization_policy_digest_binds_exact_monitor_coverage():
    first = authority_monitor("monitor:authority:1")
    second = authority_monitor("monitor:authority:2")
    fields = {
        "schema_version": "1",
        "policy_id": "policy:authority",
        "policy_version": "1",
        "required_monitor_ids": [first["id"], second["id"]],
        "required_monitor_record_hashes": [first["content_hash"], second["content_hash"]],
    }
    digest = authorization_policy_digest(**fields)
    assert digest.startswith("sha256:")
    assert digest != authorization_policy_digest(
        **{
            **fields,
            "required_monitor_record_hashes": [first["content_hash"], DIGEST_C],
        }
    )
    assert digest != authorization_policy_digest(
        **{**fields, "policy_version": "2"}
    )
    with pytest.raises(ControlError, match="iterable collection"):
        authorization_policy_digest(
            **{**fields, "required_monitor_ids": None}
        )


@pytest.mark.parametrize(
    "mutation,message",
    [
        (lambda value: value["required_monitor_ids"].clear(), "nonempty"),
        (
            lambda value: value["required_monitor_record_hashes"].append(DIGEST_A),
            "equal lengths",
        ),
        (
            lambda value: value.update({
                "required_monitor_ids": ["monitor:2", "monitor:1"],
                "required_monitor_record_hashes": [DIGEST_A, DIGEST_B],
            }),
            "canonical",
        ),
        (
            lambda value: value.update({
                "required_monitor_ids": ["monitor:1", "monitor:1"],
                "required_monitor_record_hashes": [DIGEST_A, DIGEST_B],
            }),
            "canonical",
        ),
        (
            lambda value: value["required_monitor_record_hashes"].__setitem__(0, "not-a-hash"),
            "sha256 digest",
        ),
    ],
)
def test_authorization_policy_requirements_fail_loudly(mutation, message):
    value = {
        "required_monitor_ids": ["monitor:1"],
        "required_monitor_record_hashes": [DIGEST_A],
    }
    mutation(value)
    with pytest.raises(ControlError, match=message):
        authorization_policy_requirements(value)


def test_satisfied_authority_outputs_select_authorize_in_canonical_order():
    first = authority_monitor("monitor:authority:a")
    second = authority_monitor("monitor:authority:b")
    policy_record = authorization_policy([first, second])
    assessments = [
        authority_assessment(second, policy_record, "SATISFIED", suffix="b"),
        authority_assessment(first, policy_record, "SATISFIED", suffix="a"),
    ]
    result = evaluate_authority(policy_record, [first, second], assessments)
    reversed_result = evaluate_authority(
        policy_record,
        [second, first],
        list(reversed(assessments)),
    )
    assert result.verdict == "AUTHORIZE"
    assert result.assessment_ids == (
        "assessment:authority:a",
        "assessment:authority:b",
    )
    assert result.triggered_assessment_ids == ()
    assert result.evaluation_hash == reversed_result.evaluation_hash


@pytest.mark.parametrize(
    "outcome,verdict",
    [("VIOLATED", "BLOCK"), ("UNKNOWN", "CLARIFY")],
)
def test_non_satisfied_authority_output_selects_fixed_control(outcome, verdict):
    monitor_record = authority_monitor("monitor:authority")
    policy_record = authorization_policy([monitor_record])
    assessment_record = authority_assessment(monitor_record, policy_record, outcome)
    result = evaluate_authority(
        policy_record,
        [monitor_record],
        [assessment_record],
    )
    assert result.verdict == verdict
    assert result.triggered_assessment_ids == (assessment_record["id"],)


def test_block_precedes_clarify_regardless_of_input_order():
    block_monitor = authority_monitor("monitor:authority:block")
    unknown_monitor = authority_monitor("monitor:authority:unknown")
    policy_record = authorization_policy([block_monitor, unknown_monitor])
    assessments = [
        authority_assessment(unknown_monitor, policy_record, "UNKNOWN", suffix="unknown"),
        authority_assessment(block_monitor, policy_record, "VIOLATED", suffix="block"),
    ]
    result = evaluate_authority(
        policy_record,
        [unknown_monitor, block_monitor],
        assessments,
    )
    assert result.verdict == "BLOCK"
    assert result.triggered_assessment_ids == (
        "assessment:authority:block",
        "assessment:authority:unknown",
    )


@pytest.mark.parametrize(
    "field,value,message",
    [
        ("action_proposal_id", "action:other", "action_proposal_id mismatch"),
        ("action_content_hash", DIGEST_C, "action_content_hash mismatch"),
        ("proposal_id", "proposal:other", "proposal_id mismatch"),
        ("proposal_content_hash", DIGEST_C, "proposal_content_hash mismatch"),
        ("evaluated_actor_id", "actor:other", "evaluated_actor_id mismatch"),
        ("base_acceptance_head", DIGEST_C, "base_acceptance_head mismatch"),
        ("authority_policy_id", "policy:other", "authority_policy_id mismatch"),
        ("authority_policy_hash", DIGEST_C, "authority_policy_hash mismatch"),
        ("monitor_hash", DIGEST_C, "monitor hash mismatch"),
        ("monitor_version", "2", "monitor version mismatch"),
        ("assessment_kind", "TYPE", "kind mismatch"),
        ("assessment_outcome", "ACCEPT", "invalid authority assessment outcome"),
    ],
)
def test_authority_assessment_must_match_every_bound_input(field, value, message):
    monitor_record = authority_monitor("monitor:authority")
    policy_record = authorization_policy([monitor_record])
    assessment_record = authority_assessment(monitor_record, policy_record, "SATISFIED")
    assessment_record[field] = value
    assessment_record["content_hash"] = content_digest(assessment_record)
    with pytest.raises(ControlError, match=message):
        evaluate_authority(policy_record, [monitor_record], [assessment_record])


@pytest.mark.parametrize(
    "mutation,message",
    [
        (lambda value: value.update({"artifact_kind": "EPISTEMIC_POLICY"}), "artifact_kind"),
        (lambda value: value.update({"policy_schema_version": "2"}), "schema_version"),
        (lambda value: value.update({"artifact_hash": DIGEST_C}), "semantic hash mismatch"),
        (lambda value: value.pop("content_hash"), "policy content_hash"),
        (lambda value: value.pop("required_monitor_ids"), "iterable collection"),
    ],
)
def test_authorization_policy_identity_and_semantics_are_verified(mutation, message):
    monitor_record = authority_monitor("monitor:authority")
    policy_record = authorization_policy([monitor_record])
    assessment_record = authority_assessment(monitor_record, policy_record, "SATISFIED")
    mutation(policy_record)
    with pytest.raises(ControlError, match=message):
        evaluate_authority(policy_record, [monitor_record], [assessment_record])


@pytest.mark.parametrize(
    "mutation,message",
    [
        (lambda value: value.update({"id": "monitor:other"}), "mismatched id"),
        (lambda value: value.update({"content_hash": DIGEST_C}), "record hash mismatch"),
        (lambda value: value.update({"artifact_kind": "RULE_SET"}), "artifact_kind mismatch"),
        (lambda value: value.update({"assessment_kind": "TYPE"}), "not an AUTHORITY"),
        (lambda value: value.update({"artifact_hash": DIGEST_C}), "semantic hash mismatch"),
        (lambda value: value.update({"input_artifact_ids": None}), "input fields must be lists"),
    ],
)
def test_required_authority_monitor_is_typed_and_content_addressed(mutation, message):
    monitor_record = authority_monitor("monitor:authority")
    policy_record = authorization_policy([monitor_record])
    assessment_record = authority_assessment(monitor_record, policy_record, "SATISFIED")
    forged = dict(monitor_record)
    mutation(forged)
    with pytest.raises(ControlError, match=message):
        evaluate_authorization_policy(
            policy_record,
            {monitor_record["id"]: forged},
            [assessment_record],
            proposal_id="proposal:1",
            proposal_content_hash=PROPOSAL_HASH,
            action_id="action:1",
            action_content_hash=ACTION_HASH,
            evaluated_actor_id="actor:executor",
            base_acceptance_head=BASE_HEAD,
        )


@pytest.mark.parametrize(
    "monitors,assessments,message",
    [
        ([], None, "specification.*unavailable"),
        (None, [], "unrequired monitor specification"),
        (None, [], "has no assessment"),
        (None, None, "unrequired authority monitor"),
    ],
)
def test_authorization_coverage_must_be_exact(monitors, assessments, message):
    required = authority_monitor("monitor:authority")
    extra = authority_monitor("monitor:extra")
    policy_record = authorization_policy([required])
    required_assessment = authority_assessment(required, policy_record, "SATISFIED")
    extra_assessment = authority_assessment(extra, policy_record, "SATISFIED", suffix="extra")
    if monitors is None:
        monitors = [required]
    if assessments is None:
        assessments = [required_assessment]
    if message == "unrequired monitor specification":
        monitors = [required, extra]
    elif message == "unrequired authority monitor":
        assessments = [required_assessment, extra_assessment]
    with pytest.raises(ControlError, match=message):
        evaluate_authority(policy_record, monitors, assessments)


def test_duplicate_authority_outputs_and_ids_are_rejected():
    first = authority_monitor("monitor:authority:a")
    second = authority_monitor("monitor:authority:b")
    policy_record = authorization_policy([first, second])
    first_assessment = authority_assessment(first, policy_record, "SATISFIED", suffix="same")
    duplicate_monitor = authority_assessment(first, policy_record, "SATISFIED", suffix="other")
    with pytest.raises(ControlError, match="multiple assessments"):
        evaluate_authority(
            authorization_policy([first]),
            [first],
            [first_assessment, duplicate_monitor],
        )
    second_assessment = authority_assessment(second, policy_record, "SATISFIED", suffix="same")
    with pytest.raises(ControlError, match="assessment IDs must be unique"):
        evaluate_authority(
            policy_record,
            [first, second],
            [first_assessment, second_assessment],
        )


def test_malformed_authority_collections_fail_with_control_error():
    monitor_record = authority_monitor("monitor:authority")
    policy_record = authorization_policy([monitor_record])
    assessment_record = authority_assessment(monitor_record, policy_record, "SATISFIED")
    common = {
        "proposal_id": "proposal:1",
        "proposal_content_hash": PROPOSAL_HASH,
        "action_id": "action:1",
        "action_content_hash": ACTION_HASH,
        "evaluated_actor_id": "actor:executor",
        "base_acceptance_head": BASE_HEAD,
    }
    with pytest.raises(ControlError, match="authority assessments must be an iterable"):
        evaluate_authorization_policy(
            policy_record,
            {monitor_record["id"]: monitor_record},
            None,
            **common,
        )
    with pytest.raises(ControlError, match="monitor mapping keys"):
        evaluate_authorization_policy(
            policy_record,
            {1: monitor_record},
            [assessment_record],
            **common,
        )


def test_evaluation_hash_binds_action_actor_head_policy_and_assessments():
    monitor_record = authority_monitor("monitor:authority")

    def result(
        *,
        proposal_id="proposal:1",
        proposal_hash=PROPOSAL_HASH,
        action_id="action:1",
        action_hash=ACTION_HASH,
        actor_id="actor:executor",
        acceptance_head=BASE_HEAD,
        policy_id="policy:authority",
        outcome="SATISFIED",
    ):
        policy_record = authorization_policy([monitor_record], policy_id=policy_id)
        assessment_record = authority_assessment(
            monitor_record,
            policy_record,
            outcome,
            proposal_id=proposal_id,
            proposal_hash=proposal_hash,
            action_id=action_id,
            action_hash=action_hash,
            actor_id=actor_id,
            acceptance_head=acceptance_head,
        )
        return evaluate_authority(
            policy_record,
            [monitor_record],
            [assessment_record],
            proposal_id=proposal_id,
            proposal_hash=proposal_hash,
            action_id=action_id,
            action_hash=action_hash,
            actor_id=actor_id,
            acceptance_head=acceptance_head,
        ).evaluation_hash

    baseline = result()
    assert baseline != result(proposal_id="proposal:2")
    assert baseline != result(proposal_hash=DIGEST_C)
    assert baseline != result(action_id="action:2")
    assert baseline != result(action_hash=DIGEST_C)
    assert baseline != result(actor_id="actor:other")
    assert baseline != result(acceptance_head=DIGEST_C)
    assert baseline != result(policy_id="policy:other")
    assert baseline != result(outcome="UNKNOWN")
