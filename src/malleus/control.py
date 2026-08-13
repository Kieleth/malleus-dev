"""Typed monitor contracts and deterministic epistemic and authorization control."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from malleus.ledger import LedgerError, content_digest, require_digest, with_content_hash


EPISTEMIC_MONITOR_KINDS = {
    "TYPE",
    "EVIDENCE_COMPLETENESS",
    "CONFLICT",
    "UNCERTAINTY",
    "LOGICAL",
    "TEMPORAL",
}
COMPLETED_OUTCOMES = {"SATISFIED", "VIOLATED"}
VIOLATION_VERDICTS = {"REJECT", "DEFER", "CONTEST"}
UNKNOWN_VERDICTS = {"DEFER", "CONTEST"}
CONTROL_PRECEDENCE = {"REJECT", "DEFER", "CONTEST"}


class ControlError(ValueError):
    """A monitor contract, policy, or evaluation is invalid."""


class MonitoringError(ControlError):
    """A required monitor did not produce a completed assessment."""


@dataclass(frozen=True)
class PolicyEvaluation:
    """Canonical result of applying one policy to exact monitor outputs."""

    verdict: str
    assessment_ids: tuple[str, ...]
    triggered_assessment_ids: tuple[str, ...]
    evaluation_hash: str


@dataclass(frozen=True)
class AuthorizationEvaluation:
    """Canonical authorization control selected from exact authority outputs."""

    verdict: str
    assessment_ids: tuple[str, ...]
    triggered_assessment_ids: tuple[str, ...]
    evaluation_hash: str


def monitor_specification_digest(
    *,
    schema_version: str,
    monitor_id: str,
    monitor_version: str,
    assessment_kind: str,
    implementation_hash: str,
    input_artifact_ids: Iterable[str] = (),
    input_artifact_record_hashes: Iterable[str] = (),
) -> str:
    """Hash the replay-visible semantics of one monitor specification."""
    if schema_version != "1":
        raise ControlError(f"unsupported monitor schema_version '{schema_version}'")
    identifiers = tuple(input_artifact_ids)
    hashes = tuple(input_artifact_record_hashes)
    _monitor_shape(
        schema_version=schema_version,
        monitor_id=monitor_id,
        monitor_version=monitor_version,
        assessment_kind=assessment_kind,
        implementation_hash=implementation_hash,
        input_artifact_ids=identifiers,
        input_artifact_record_hashes=hashes,
    )
    return content_digest({
        "schema_version": schema_version,
        "monitor_id": monitor_id,
        "monitor_version": monitor_version,
        "assessment_kind": assessment_kind,
        "implementation_hash": implementation_hash,
        "input_artifacts": [
            {"id": artifact_id, "record_hash": record_hash}
            for artifact_id, record_hash in zip(identifiers, hashes, strict=True)
        ],
    })


def epistemic_policy_digest(
    *,
    schema_version: str,
    policy_id: str,
    policy_version: str,
    ruleset_id: str,
    ruleset_record_hash: str,
    ruleset_artifact_hash: str,
    required_monitor_ids: Iterable[str],
    required_monitor_record_hashes: Iterable[str],
    violation_verdicts: Iterable[str],
    unknown_verdicts: Iterable[str],
    control_precedence: Iterable[str],
) -> str:
    """Hash the exact monitor coverage and outcome-to-control policy."""
    if schema_version != "1":
        raise ControlError(f"unsupported policy schema_version '{schema_version}'")
    policy = {
        "policy_schema_version": schema_version,
        "id": policy_id,
        "artifact_version": policy_version,
        "ruleset_id": ruleset_id,
        "ruleset_record_hash": ruleset_record_hash,
        "ruleset_artifact_hash": ruleset_artifact_hash,
        "required_monitor_ids": list(required_monitor_ids),
        "required_monitor_record_hashes": list(required_monitor_record_hashes),
        "violation_verdicts": list(violation_verdicts),
        "unknown_verdicts": list(unknown_verdicts),
        "control_precedence": list(control_precedence),
    }
    requirements = policy_requirements(policy)
    _digest(ruleset_record_hash, "ruleset_record_hash")
    _digest(ruleset_artifact_hash, "ruleset_artifact_hash")
    _text(schema_version, "schema_version")
    _text(policy_id, "policy_id")
    _text(policy_version, "policy_version")
    _text(ruleset_id, "ruleset_id")
    return content_digest({
        "schema_version": schema_version,
        "policy_id": policy_id,
        "policy_version": policy_version,
        "ruleset_id": ruleset_id,
        "ruleset_record_hash": ruleset_record_hash,
        "ruleset_artifact_hash": ruleset_artifact_hash,
        "requirements": requirements,
        "control_precedence": policy["control_precedence"],
    })


def authorization_policy_digest(
    *,
    schema_version: str,
    policy_id: str,
    policy_version: str,
    required_monitor_ids: Iterable[str],
    required_monitor_record_hashes: Iterable[str],
) -> str:
    """Hash one authorization policy's exact authority-monitor coverage."""
    if schema_version != "1":
        raise ControlError(f"unsupported authorization policy schema_version '{schema_version}'")
    _text(policy_id, "policy_id")
    _text(policy_version, "policy_version")
    requirements = authorization_policy_requirements({
        "required_monitor_ids": _iterable_values(
            required_monitor_ids,
            "required_monitor_ids",
        ),
        "required_monitor_record_hashes": _iterable_values(
            required_monitor_record_hashes,
            "required_monitor_record_hashes",
        ),
    })
    return content_digest({
        "schema_version": schema_version,
        "policy_id": policy_id,
        "policy_version": policy_version,
        "requirements": requirements,
        "outcome_controls": {
            "SATISFIED": "AUTHORIZE",
            "VIOLATED": "BLOCK",
            "UNKNOWN": "CLARIFY",
        },
        "control_precedence": ["BLOCK", "CLARIFY", "AUTHORIZE"],
    })


def authorization_policy_requirements(policy: Mapping[str, Any]) -> list[dict[str, str]]:
    """Return validated authority-monitor requirements in canonical ID order."""
    if not isinstance(policy, Mapping):
        raise ControlError("authorization policy must be a mapping")
    monitor_ids = policy.get("required_monitor_ids")
    monitor_hashes = policy.get("required_monitor_record_hashes")
    if not isinstance(monitor_ids, list) or not monitor_ids:
        raise ControlError("required_monitor_ids must be a nonempty list")
    if not isinstance(monitor_hashes, list) or not monitor_hashes:
        raise ControlError("required_monitor_record_hashes must be a nonempty list")
    if len(monitor_ids) != len(monitor_hashes):
        raise ControlError("authorization policy requirement fields must have equal lengths")
    if any(not isinstance(value, str) or not value.strip() for value in monitor_ids):
        raise ControlError("required_monitor_ids must contain nonblank strings")
    if monitor_ids != sorted(set(monitor_ids)):
        raise ControlError("required_monitor_ids must be unique and canonical")
    for index, value in enumerate(monitor_hashes):
        _digest(value, f"required_monitor_record_hashes[{index}]")
    return [
        {"monitor_id": monitor_id, "monitor_record_hash": monitor_hash}
        for monitor_id, monitor_hash in zip(monitor_ids, monitor_hashes, strict=True)
    ]


def policy_requirements(policy: Mapping[str, Any]) -> list[dict[str, str]]:
    """Return validated requirements in canonical monitor-ID order."""
    if not isinstance(policy, Mapping):
        raise ControlError("epistemic policy must be a mapping")
    names = (
        "required_monitor_ids",
        "required_monitor_record_hashes",
        "violation_verdicts",
        "unknown_verdicts",
    )
    values = []
    for name in names:
        value = policy.get(name)
        if not isinstance(value, list) or not value:
            raise ControlError(f"{name} must be a nonempty list")
        values.append(value)
    lengths = {len(value) for value in values}
    if len(lengths) != 1:
        raise ControlError("epistemic policy requirement fields must have equal lengths")
    monitor_ids, monitor_hashes, violation_verdicts, unknown_verdicts = values
    if any(not isinstance(value, str) or not value.strip() for value in monitor_ids):
        raise ControlError("required_monitor_ids must contain nonblank strings")
    if monitor_ids != sorted(set(monitor_ids)):
        raise ControlError("required_monitor_ids must be unique and canonical")
    for index, value in enumerate(monitor_hashes):
        _digest(value, f"required_monitor_record_hashes[{index}]")
    if any(not isinstance(value, str) for value in violation_verdicts):
        raise ControlError("violation_verdicts must contain strings")
    invalid_violations = sorted(set(violation_verdicts) - VIOLATION_VERDICTS)
    if invalid_violations:
        raise ControlError(f"invalid violation verdict '{invalid_violations[0]}'")
    if any(not isinstance(value, str) for value in unknown_verdicts):
        raise ControlError("unknown_verdicts must contain strings")
    invalid_unknowns = sorted(set(unknown_verdicts) - UNKNOWN_VERDICTS)
    if invalid_unknowns:
        raise ControlError(f"invalid UNKNOWN verdict '{invalid_unknowns[0]}'")
    precedence = policy.get("control_precedence")
    if (
        not isinstance(precedence, list)
        or any(not isinstance(value, str) for value in precedence)
        or set(precedence) != CONTROL_PRECEDENCE
    ):
        raise ControlError("control_precedence must contain REJECT, DEFER, and CONTEST")
    if len(precedence) != len(set(precedence)):
        raise ControlError("control_precedence values must be unique")
    return [
        {
            "monitor_id": monitor_id,
            "monitor_record_hash": monitor_hash,
            "violation_verdict": violation_verdict,
            "unknown_verdict": unknown_verdict,
        }
        for monitor_id, monitor_hash, violation_verdict, unknown_verdict in zip(
            monitor_ids,
            monitor_hashes,
            violation_verdicts,
            unknown_verdicts,
            strict=True,
        )
    ]


def evaluate_epistemic_policy(
    policy: Mapping[str, Any],
    monitors: Mapping[str, Mapping[str, Any]],
    assessments: Iterable[Mapping[str, Any]],
    *,
    proposal_id: str,
    proposal_content_hash: str,
    base_acceptance_head: str,
) -> PolicyEvaluation:
    """Select one verdict only when every required monitor has one exact output."""
    requirements = policy_requirements(policy)
    _text(policy.get("id"), "policy id")
    _digest(policy.get("content_hash"), "policy content_hash")
    if not isinstance(monitors, Mapping):
        raise ControlError("monitors must be a mapping")
    assessment_by_monitor: dict[str, Mapping[str, Any]] = {}
    for assessment in assessments:
        if not isinstance(assessment, Mapping):
            raise ControlError("assessments must be mappings")
        monitor_id = assessment.get("monitor_id")
        _text(monitor_id, "assessment monitor_id")
        if monitor_id in assessment_by_monitor:
            raise ControlError(f"multiple assessments cite required monitor '{monitor_id}'")
        assessment_by_monitor[monitor_id] = assessment
    required_ids = [item["monitor_id"] for item in requirements]
    missing = sorted(set(required_ids) - set(assessment_by_monitor))
    if missing:
        raise ControlError(
            f"required monitor '{missing[0]}' has no assessment; record MonitorFailure plus "
            "UnavailableAssessment"
        )
    extra = sorted(set(assessment_by_monitor) - set(required_ids))
    if extra:
        raise ControlError(f"assessment from unrequired monitor '{extra[0]}'")

    ordered_assessment_ids = []
    triggered_assessment_ids = []
    triggered_controls = set()
    bindings = []
    for requirement in requirements:
        monitor_id = requirement["monitor_id"]
        if monitor_id not in monitors:
            raise ControlError(f"required monitor specification '{monitor_id}' is unavailable")
        monitor = monitors[monitor_id]
        if not isinstance(monitor, Mapping):
            raise ControlError(f"required monitor specification '{monitor_id}' must be a mapping")
        if monitor.get("id") != monitor_id:
            raise ControlError(f"required monitor specification '{monitor_id}' has mismatched id")
        assessment = assessment_by_monitor[monitor_id]
        if monitor.get("content_hash") != requirement["monitor_record_hash"]:
            raise ControlError(f"required monitor '{monitor_id}' record hash mismatch")
        if assessment.get("monitor_hash") != monitor.get("content_hash"):
            raise ControlError(f"assessment monitor hash mismatch for '{monitor_id}'")
        if assessment.get("monitor_version") != monitor.get("artifact_version"):
            raise ControlError(f"assessment monitor version mismatch for '{monitor_id}'")
        if assessment.get("assessment_kind") != monitor.get("assessment_kind"):
            raise ControlError(f"assessment kind mismatch for monitor '{monitor_id}'")
        for name, expected in (
            ("proposal_id", proposal_id),
            ("proposal_content_hash", proposal_content_hash),
            ("base_acceptance_head", base_acceptance_head),
        ):
            if assessment.get(name) != expected:
                raise ControlError(f"assessment {name} mismatch for monitor '{monitor_id}'")
        outcome = assessment.get("assessment_outcome")
        if outcome not in {*COMPLETED_OUTCOMES, "UNKNOWN"}:
            raise ControlError(f"invalid assessment outcome for monitor '{monitor_id}'")
        assessment_id = assessment.get("id")
        assessment_hash = assessment.get("content_hash")
        _text(assessment_id, "assessment id")
        _digest(assessment_hash, "assessment content_hash")
        selected_control = None
        if outcome == "VIOLATED":
            selected_control = requirement["violation_verdict"]
        elif outcome == "UNKNOWN":
            selected_control = requirement["unknown_verdict"]
        if selected_control:
            triggered_controls.add(selected_control)
            triggered_assessment_ids.append(assessment_id)
        ordered_assessment_ids.append(assessment_id)
        bindings.append({
            "monitor_id": monitor_id,
            "monitor_record_hash": monitor["content_hash"],
            "assessment_id": assessment_id,
            "assessment_content_hash": assessment_hash,
            "assessment_outcome": outcome,
            "selected_control": selected_control,
        })

    if len(ordered_assessment_ids) != len(set(ordered_assessment_ids)):
        raise ControlError("assessment IDs must be unique")

    verdict = "ACCEPT"
    if triggered_controls:
        verdict = next(
            control
            for control in policy["control_precedence"]
            if control in triggered_controls
        )
    evaluation_hash = content_digest({
        "policy_id": policy.get("id"),
        "policy_record_hash": policy.get("content_hash"),
        "proposal_id": proposal_id,
        "proposal_content_hash": proposal_content_hash,
        "base_acceptance_head": base_acceptance_head,
        "bindings": bindings,
        "selected_verdict": verdict,
        "triggered_assessment_ids": triggered_assessment_ids,
    })
    return PolicyEvaluation(
        verdict=verdict,
        assessment_ids=tuple(ordered_assessment_ids),
        triggered_assessment_ids=tuple(triggered_assessment_ids),
        evaluation_hash=evaluation_hash,
    )


def evaluate_authorization_policy(
    policy: Mapping[str, Any],
    monitors: Mapping[str, Mapping[str, Any]],
    assessments: Iterable[Mapping[str, Any]],
    *,
    proposal_id: str,
    proposal_content_hash: str,
    action_id: str,
    action_content_hash: str,
    evaluated_actor_id: str,
    base_acceptance_head: str,
) -> AuthorizationEvaluation:
    """Derive a verdict from records already type- and hash-validated by replay."""
    _text(proposal_id, "proposal_id")
    _digest(proposal_content_hash, "proposal_content_hash")
    _text(action_id, "action_id")
    _digest(action_content_hash, "action_content_hash")
    _text(evaluated_actor_id, "evaluated_actor_id")
    _digest(base_acceptance_head, "base_acceptance_head")
    if not isinstance(policy, Mapping):
        raise ControlError("authorization policy must be a mapping")
    policy_id = policy.get("id")
    policy_record_hash = policy.get("content_hash")
    policy_version = policy.get("artifact_version")
    policy_schema_version = policy.get("policy_schema_version")
    _text(policy_id, "policy id")
    _digest(policy_record_hash, "policy content_hash")
    _text(policy_version, "policy artifact_version")
    if policy.get("artifact_kind") != "AUTHORIZATION_POLICY":
        raise ControlError("authorization policy artifact_kind must be AUTHORIZATION_POLICY")
    if policy_schema_version != "1":
        raise ControlError(
            f"unsupported authorization policy schema_version '{policy_schema_version}'"
        )
    expected_policy_hash = authorization_policy_digest(
        schema_version=policy_schema_version,
        policy_id=policy_id,
        policy_version=policy_version,
        required_monitor_ids=policy.get("required_monitor_ids"),
        required_monitor_record_hashes=policy.get("required_monitor_record_hashes"),
    )
    if policy.get("artifact_hash") != expected_policy_hash:
        raise ControlError("authorization policy semantic hash mismatch")
    requirements = authorization_policy_requirements(policy)

    if not isinstance(monitors, Mapping):
        raise ControlError("monitors must be a mapping")
    if any(not isinstance(value, str) or not value.strip() for value in monitors):
        raise ControlError("monitor mapping keys must be nonblank strings")
    required_ids = [item["monitor_id"] for item in requirements]
    missing_monitors = sorted(set(required_ids) - set(monitors))
    if missing_monitors:
        raise ControlError(
            f"required authority monitor specification '{missing_monitors[0]}' is unavailable"
        )
    extra_monitors = sorted(set(monitors) - set(required_ids))
    if extra_monitors:
        raise ControlError(f"unrequired monitor specification '{extra_monitors[0]}'")

    assessment_by_monitor: dict[str, Mapping[str, Any]] = {}
    for assessment in _iterable_values(assessments, "authority assessments"):
        if not isinstance(assessment, Mapping):
            raise ControlError("authority assessments must be mappings")
        monitor_id = assessment.get("monitor_id")
        _text(monitor_id, "authority assessment monitor_id")
        if monitor_id in assessment_by_monitor:
            raise ControlError(f"multiple assessments cite authority monitor '{monitor_id}'")
        assessment_by_monitor[monitor_id] = assessment
    missing_assessments = sorted(set(required_ids) - set(assessment_by_monitor))
    if missing_assessments:
        raise ControlError(
            f"required authority monitor '{missing_assessments[0]}' has no assessment"
        )
    extra_assessments = sorted(set(assessment_by_monitor) - set(required_ids))
    if extra_assessments:
        raise ControlError(
            f"assessment from unrequired authority monitor '{extra_assessments[0]}'"
        )

    ordered_assessment_ids: list[str] = []
    triggered_assessment_ids: list[str] = []
    bindings: list[dict[str, Any]] = []
    triggered_controls: set[str] = set()
    for requirement in requirements:
        monitor_id = requirement["monitor_id"]
        monitor = monitors[monitor_id]
        if not isinstance(monitor, Mapping):
            raise ControlError(
                f"required authority monitor specification '{monitor_id}' must be a mapping"
            )
        if monitor.get("id") != monitor_id:
            raise ControlError(
                f"required authority monitor specification '{monitor_id}' has mismatched id"
            )
        if monitor.get("content_hash") != requirement["monitor_record_hash"]:
            raise ControlError(f"required authority monitor '{monitor_id}' record hash mismatch")
        if monitor.get("artifact_kind") != "MONITOR_SPECIFICATION":
            raise ControlError(
                f"required authority monitor '{monitor_id}' artifact_kind mismatch"
            )
        if monitor.get("assessment_kind") != "AUTHORITY":
            raise ControlError(f"required monitor '{monitor_id}' is not an AUTHORITY monitor")
        input_ids = monitor.get("input_artifact_ids")
        input_hashes = monitor.get("input_artifact_record_hashes")
        if not isinstance(input_ids, list) or not isinstance(input_hashes, list):
            raise ControlError(f"authority monitor '{monitor_id}' input fields must be lists")
        expected_monitor_hash = monitor_specification_digest(
            schema_version=monitor.get("monitor_schema_version"),
            monitor_id=monitor_id,
            monitor_version=monitor.get("artifact_version"),
            assessment_kind=monitor.get("assessment_kind"),
            implementation_hash=monitor.get("monitor_implementation_hash"),
            input_artifact_ids=input_ids,
            input_artifact_record_hashes=input_hashes,
        )
        if monitor.get("artifact_hash") != expected_monitor_hash:
            raise ControlError(f"authority monitor '{monitor_id}' semantic hash mismatch")

        assessment = assessment_by_monitor[monitor_id]
        if assessment.get("monitor_hash") != monitor.get("content_hash"):
            raise ControlError(f"authority assessment monitor hash mismatch for '{monitor_id}'")
        if assessment.get("monitor_version") != monitor.get("artifact_version"):
            raise ControlError(f"authority assessment monitor version mismatch for '{monitor_id}'")
        if assessment.get("assessment_kind") != "AUTHORITY":
            raise ControlError(f"assessment kind mismatch for authority monitor '{monitor_id}'")
        for name, expected in (
            ("proposal_id", proposal_id),
            ("proposal_content_hash", proposal_content_hash),
            ("action_proposal_id", action_id),
            ("action_content_hash", action_content_hash),
            ("evaluated_actor_id", evaluated_actor_id),
            ("base_acceptance_head", base_acceptance_head),
            ("authority_policy_id", policy_id),
            ("authority_policy_hash", policy_record_hash),
        ):
            if assessment.get(name) != expected:
                raise ControlError(
                    f"authority assessment {name} mismatch for monitor '{monitor_id}'"
                )
        outcome = assessment.get("assessment_outcome")
        try:
            selected_control = _authorization_control(outcome)
        except ControlError as error:
            raise ControlError(
                f"invalid authority assessment outcome for monitor '{monitor_id}'"
            ) from error
        assessment_id = assessment.get("id")
        assessment_hash = assessment.get("content_hash")
        _text(assessment_id, "authority assessment id")
        _digest(assessment_hash, "authority assessment content_hash")
        if selected_control != "AUTHORIZE":
            triggered_controls.add(selected_control)
            triggered_assessment_ids.append(assessment_id)
        ordered_assessment_ids.append(assessment_id)
        bindings.append({
            "monitor_id": monitor_id,
            "monitor_record_hash": monitor["content_hash"],
            "assessment_id": assessment_id,
            "assessment_content_hash": assessment_hash,
            "assessment_outcome": outcome,
            "selected_control": selected_control,
        })

    if len(ordered_assessment_ids) != len(set(ordered_assessment_ids)):
        raise ControlError("authority assessment IDs must be unique")
    verdict = "AUTHORIZE"
    if "BLOCK" in triggered_controls:
        verdict = "BLOCK"
    elif "CLARIFY" in triggered_controls:
        verdict = "CLARIFY"
    evaluation_hash = content_digest({
        "policy_id": policy_id,
        "policy_record_hash": policy_record_hash,
        "proposal_id": proposal_id,
        "proposal_content_hash": proposal_content_hash,
        "action_id": action_id,
        "action_content_hash": action_content_hash,
        "evaluated_actor_id": evaluated_actor_id,
        "base_acceptance_head": base_acceptance_head,
        "bindings": bindings,
        "selected_verdict": verdict,
        "triggered_assessment_ids": triggered_assessment_ids,
    })
    return AuthorizationEvaluation(
        verdict=verdict,
        assessment_ids=tuple(ordered_assessment_ids),
        triggered_assessment_ids=tuple(triggered_assessment_ids),
        evaluation_hash=evaluation_hash,
    )


def monitor_failure_records(
    *,
    error: MonitoringError,
    failure_id: str,
    assessment_id: str,
    event_id: str,
    generated_at: str,
    actor_id: str,
    role: str,
    proposal_id: str,
    proposal_content_hash: str,
    base_acceptance_head: str,
    monitor_id: str,
    monitor_version: str,
    monitor_hash: str,
    assessment_kind: str,
    failure_category: str,
    error_code: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build the atomic UNKNOWN records for a non-logical monitor failure."""
    if not isinstance(error, MonitoringError):
        raise TypeError("error must be a MonitoringError")
    if assessment_kind == "LOGICAL":
        raise ControlError("logical failures require logic_monitor_failure_records")
    return build_monitor_failure_records(
        error=error,
        failure_id=failure_id,
        assessment_id=assessment_id,
        event_id=event_id,
        generated_at=generated_at,
        actor_id=actor_id,
        role=role,
        proposal_id=proposal_id,
        proposal_content_hash=proposal_content_hash,
        base_acceptance_head=base_acceptance_head,
        monitor_id=monitor_id,
        monitor_version=monitor_version,
        monitor_hash=monitor_hash,
        assessment_kind=assessment_kind,
        failure_category=failure_category,
        error_code=error_code,
    )


def authority_monitor_failure_records(
    *,
    error: MonitoringError,
    failure_id: str,
    assessment_id: str,
    event_id: str,
    generated_at: str,
    actor_id: str,
    role: str,
    proposal_id: str,
    proposal_content_hash: str,
    base_acceptance_head: str,
    action_proposal_id: str,
    action_content_hash: str,
    evaluated_actor_id: str,
    authority_policy_id: str,
    authority_policy_hash: str,
    monitor_id: str,
    monitor_version: str,
    monitor_hash: str,
    failure_category: str,
    error_code: str,
    evaluated_authority_grant_id: str | None = None,
    evaluated_authority_grant_hash: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build one atomic UNKNOWN authority output with exact action context."""
    if not isinstance(error, MonitoringError):
        raise TypeError("error must be a MonitoringError")
    for name, value in (
        ("action_proposal_id", action_proposal_id),
        ("evaluated_actor_id", evaluated_actor_id),
        ("authority_policy_id", authority_policy_id),
    ):
        _text(value, name)
    for name, value in (
        ("action_content_hash", action_content_hash),
        ("authority_policy_hash", authority_policy_hash),
    ):
        _digest(value, name)
    if (evaluated_authority_grant_id is None) != (
        evaluated_authority_grant_hash is None
    ):
        raise ControlError("evaluated authority grant binding must be all-or-none")
    if evaluated_authority_grant_id is not None:
        _text(evaluated_authority_grant_id, "evaluated_authority_grant_id")
        _digest(evaluated_authority_grant_hash, "evaluated_authority_grant_hash")
    authority_fields = {
        "action_proposal_id": action_proposal_id,
        "action_content_hash": action_content_hash,
        "evaluated_actor_id": evaluated_actor_id,
        "authority_policy_id": authority_policy_id,
        "authority_policy_hash": authority_policy_hash,
        "evaluated_authority_grant_id": evaluated_authority_grant_id,
        "evaluated_authority_grant_hash": evaluated_authority_grant_hash,
    }
    additional_sources = {action_proposal_id, authority_policy_id}
    additional_inputs = {action_proposal_id}
    if evaluated_authority_grant_id is not None:
        additional_sources.add(evaluated_authority_grant_id)
        additional_inputs.add(evaluated_authority_grant_id)
    return build_monitor_failure_records(
        error=error,
        failure_id=failure_id,
        assessment_id=assessment_id,
        event_id=event_id,
        generated_at=generated_at,
        actor_id=actor_id,
        role=role,
        proposal_id=proposal_id,
        proposal_content_hash=proposal_content_hash,
        base_acceptance_head=base_acceptance_head,
        monitor_id=monitor_id,
        monitor_version=monitor_version,
        monitor_hash=monitor_hash,
        assessment_kind="AUTHORITY",
        failure_category=failure_category,
        error_code=error_code,
        additional_source_record_ids=additional_sources,
        additional_input_record_ids=additional_inputs,
        failure_fields=authority_fields,
        assessment_fields=authority_fields,
        assessment_record_type="UnavailableAuthorityAssessment",
    )


def build_monitor_failure_records(
    *,
    error: Exception,
    failure_id: str,
    assessment_id: str,
    event_id: str,
    generated_at: str,
    actor_id: str,
    role: str,
    proposal_id: str,
    proposal_content_hash: str,
    base_acceptance_head: str,
    monitor_id: str,
    monitor_version: str,
    monitor_hash: str,
    assessment_kind: str,
    failure_category: str,
    error_code: str,
    additional_source_record_ids: Iterable[str] = (),
    additional_input_record_ids: Iterable[str] = (),
    failure_fields: Mapping[str, Any] | None = None,
    assessment_fields: Mapping[str, Any] | None = None,
    assessment_record_type: str = "UnavailableAssessment",
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Internal common builder used by generic and logical failure helpers."""
    if assessment_kind not in {*EPISTEMIC_MONITOR_KINDS, "AUTHORITY"}:
        raise ControlError(f"unsupported assessment kind '{assessment_kind}'")
    expected_record_type = (
        "UnavailableAuthorityAssessment"
        if assessment_kind == "AUTHORITY"
        else "UnavailableAssessment"
    )
    if assessment_record_type != expected_record_type:
        raise ControlError(
            f"{assessment_kind} failure requires {expected_record_type}"
        )
    if failure_id == assessment_id:
        raise ControlError("failure_id and assessment_id must differ")
    error_message = str(error)
    for name, value in (
        ("failure_id", failure_id),
        ("assessment_id", assessment_id),
        ("event_id", event_id),
        ("generated_at", generated_at),
        ("actor_id", actor_id),
        ("role", role),
        ("proposal_id", proposal_id),
        ("monitor_id", monitor_id),
        ("monitor_version", monitor_version),
        ("assessment_kind", assessment_kind),
        ("failure_category", failure_category),
        ("error_code", error_code),
        ("error_message", error_message),
    ):
        _text(value, name)
    for name, value in (
        ("proposal_content_hash", proposal_content_hash),
        ("base_acceptance_head", base_acceptance_head),
        ("monitor_hash", monitor_hash),
    ):
        _digest(value, name)
    extra_sources = set(additional_source_record_ids)
    if any(not isinstance(value, str) or not value.strip() for value in extra_sources):
        raise ControlError("additional_source_record_ids must contain nonblank strings")
    extra_inputs = set(additional_input_record_ids)
    if any(not isinstance(value, str) or not value.strip() for value in extra_inputs):
        raise ControlError("additional_input_record_ids must contain nonblank strings")
    failure_extra = dict(failure_fields or {})
    assessment_extra = dict(assessment_fields or {})
    provenance_names = {
        "id",
        "generation_event_id",
        "generated_at",
        "responsible_actor_id",
        "responsible_role",
        "source_record_ids",
        "proposal_id",
        "proposal_content_hash",
        "base_acceptance_head",
        "monitor_id",
        "monitor_version",
        "monitor_hash",
    }
    failure_names = provenance_names | {
        "failed_assessment_kind",
        "failure_category",
        "error_code",
        "error_message",
    }
    assessment_names = provenance_names | {
        "assessment_kind",
        "assessment_outcome",
        "monitor_failure_id",
        "input_record_ids",
        "reason_codes",
        "rationale",
    }
    if failure_names & set(failure_extra) or assessment_names & set(assessment_extra):
        raise ControlError("extension fields cannot replace required monitor-failure fields")
    failure = with_content_hash(
        "MonitorFailure",
        {
            "id": failure_id,
            "generation_event_id": event_id,
            "generated_at": generated_at,
            "responsible_actor_id": actor_id,
            "responsible_role": role,
            "source_record_ids": sorted({proposal_id, monitor_id, *extra_sources}),
            "proposal_id": proposal_id,
            "proposal_content_hash": proposal_content_hash,
            "base_acceptance_head": base_acceptance_head,
            "monitor_id": monitor_id,
            "monitor_version": monitor_version,
            "monitor_hash": monitor_hash,
            "failed_assessment_kind": assessment_kind,
            "failure_category": failure_category,
            "error_code": error_code,
            "error_message": error_message,
            **failure_extra,
        },
    )
    assessment = with_content_hash(
        assessment_record_type,
        {
            "id": assessment_id,
            "generation_event_id": event_id,
            "generated_at": generated_at,
            "responsible_actor_id": actor_id,
            "responsible_role": role,
            "source_record_ids": sorted({
                proposal_id,
                monitor_id,
                failure_id,
                *extra_sources,
            }),
            "proposal_id": proposal_id,
            "proposal_content_hash": proposal_content_hash,
            "base_acceptance_head": base_acceptance_head,
            "assessment_kind": assessment_kind,
            "assessment_outcome": "UNKNOWN",
            "monitor_id": monitor_id,
            "monitor_version": monitor_version,
            "monitor_hash": monitor_hash,
            "monitor_failure_id": failure_id,
            "input_record_ids": sorted({proposal_id, *extra_inputs}),
            "reason_codes": [error_code],
            "rationale": "The required monitor did not complete; no result is available.",
            **assessment_extra,
        },
    )
    return failure, assessment


def _monitor_shape(
    *,
    schema_version: str,
    monitor_id: str,
    monitor_version: str,
    assessment_kind: str,
    implementation_hash: str,
    input_artifact_ids: tuple[str, ...],
    input_artifact_record_hashes: tuple[str, ...],
) -> None:
    for name, value in (
        ("schema_version", schema_version),
        ("monitor_id", monitor_id),
        ("monitor_version", monitor_version),
    ):
        _text(value, name)
    if assessment_kind not in {*EPISTEMIC_MONITOR_KINDS, "AUTHORITY"}:
        raise ControlError(f"unsupported assessment kind '{assessment_kind}'")
    _digest(implementation_hash, "implementation_hash")
    if len(input_artifact_ids) != len(input_artifact_record_hashes):
        raise ControlError("monitor input artifact fields must have equal lengths")
    if list(input_artifact_ids) != sorted(set(input_artifact_ids)):
        raise ControlError("input_artifact_ids must be unique and canonical")
    for index, artifact_id in enumerate(input_artifact_ids):
        _text(artifact_id, f"input_artifact_ids[{index}]")
    for index, record_hash in enumerate(input_artifact_record_hashes):
        _digest(record_hash, f"input_artifact_record_hashes[{index}]")


def _text(value: Any, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ControlError(f"{name} must be a nonblank string")


def _iterable_values(value: Any, name: str) -> list[Any]:
    if isinstance(value, (str, bytes, Mapping)):
        raise ControlError(f"{name} must be an iterable collection")
    try:
        return list(value)
    except TypeError as error:
        raise ControlError(f"{name} must be an iterable collection") from error


def _authorization_control(outcome: Any) -> str:
    if outcome == "SATISFIED":
        return "AUTHORIZE"
    if outcome == "VIOLATED":
        return "BLOCK"
    if outcome == "UNKNOWN":
        return "CLARIFY"
    raise ControlError("invalid authority assessment outcome")


def _digest(value: Any, name: str) -> None:
    try:
        require_digest(value, name)
    except LedgerError as error:
        raise ControlError(str(error)) from error
