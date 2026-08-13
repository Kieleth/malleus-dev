"""Deterministic Stage 6 monitoring-policy guardrails."""

import pytest

from malleus.control import (
    ControlError,
    MonitoringError,
    build_monitor_failure_records,
    epistemic_policy_digest,
    evaluate_epistemic_policy,
    monitor_failure_records,
    monitor_specification_digest,
    policy_requirements,
)
from malleus.protocol import content_digest


DIGEST_A = "sha256:" + "a" * 64
DIGEST_B = "sha256:" + "b" * 64
DIGEST_C = "sha256:" + "c" * 64
PROPOSAL_HASH = "sha256:" + "d" * 64
BASE_HEAD = "sha256:" + "e" * 64


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
