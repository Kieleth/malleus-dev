"""Thin execution of declared epistemic monitor adapters."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Callable, Mapping

from malleus.assent import (
    ASSESSMENT_TYPES_BY_KIND,
    EventType,
    ProposalState,
    ProtocolLedger,
)
from malleus.control import (
    MonitoringError,
    monitor_failure_records,
    policy_requirements,
)
from malleus.ledger import LedgerError, aware_datetime, require_digest
from malleus.logic import LogicError, LogicExecutionError, logic_monitor_failure_records


class AssentPlanError(ValueError):
    """A plan or monitor adapter violated the thin orchestration contract."""


@dataclass(frozen=True)
class MonitorEvent:
    """One explicit event returned by a successful monitor adapter."""

    event_id: str
    event_type: EventType
    transaction_time: str
    actor_id: str
    payload: Mapping[str, Any]


@dataclass(frozen=True)
class MonitorContext:
    """Read-only exact records supplied to one declared monitor adapter."""

    proposal: Mapping[str, Any]
    monitor: Mapping[str, Any]
    input_artifacts: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True)
class MonitorFailurePlan:
    """Explicit provenance for the UNKNOWN output if an adapter cannot complete."""

    event_id: str
    failure_id: str
    assessment_id: str
    transaction_time: str
    actor_id: str
    role: str
    failure_category: str
    error_code: str


MonitorAdapter = Callable[[MonitorContext], MonitorEvent | tuple[MonitorEvent, ...]]


@dataclass(frozen=True)
class MonitorStep:
    """Bind one exact monitor record to one adapter and failure record plan."""

    monitor_id: str
    monitor_record_hash: str
    adapter: MonitorAdapter = field(repr=False, compare=False)
    failure: MonitorFailurePlan


@dataclass(frozen=True)
class MonitorRunResult:
    """Replay-visible result of one monitor invocation."""

    monitor_id: str
    assessment_id: str
    assessment_outcome: str
    event_ids: tuple[str, ...]


@dataclass(frozen=True)
class AssentPlan:
    """Run exactly the epistemic monitors precommitted by one proposal."""

    proposal_id: str
    proposal_record_hash: str
    steps: tuple[MonitorStep, ...]

    def run(self, ledger: ProtocolLedger) -> tuple[MonitorRunResult, ...]:
        """Run each adapter once and record a completed or UNKNOWN assessment."""
        contexts = self._validate(ledger)
        results = []
        for step, context in zip(self.steps, contexts, strict=True):
            try:
                returned = step.adapter(context)
                events = (returned,) if isinstance(returned, MonitorEvent) else returned
                self._validate_success(events, context)
            except Exception as error:
                result = self._record_failure(ledger, step, context, error)
            else:
                try:
                    envelopes = ledger.append_events(
                        {
                            "event_id": event.event_id,
                            "event_type": event.event_type,
                            "transaction_time": event.transaction_time,
                            "actor_id": event.actor_id,
                            "payload": event.payload,
                        }
                        for event in events
                    )
                except LedgerError as error:
                    if str(error).startswith("Ledger append failed without changing"):
                        raise
                    result = self._record_failure(ledger, step, context, error)
                except ValueError as error:
                    result = self._record_failure(ledger, step, context, error)
                else:
                    assessment = events[-1].payload["assessment"]
                    result = MonitorRunResult(
                        monitor_id=step.monitor_id,
                        assessment_id=assessment["id"],
                        assessment_outcome=assessment["assessment_outcome"],
                        event_ids=tuple(event["event_id"] for event in envelopes),
                    )
            results.append(result)
        return tuple(results)

    def _validate(self, ledger: ProtocolLedger) -> tuple[MonitorContext, ...]:
        if not isinstance(ledger, ProtocolLedger):
            raise TypeError("ledger must be a ProtocolLedger")
        _nonblank(self.proposal_id, "proposal_id")
        _digest(self.proposal_record_hash, "proposal_record_hash")
        if not isinstance(self.steps, tuple) or not self.steps:
            raise AssentPlanError("steps must be a nonempty tuple")
        if any(not isinstance(step, MonitorStep) for step in self.steps):
            raise AssentPlanError("steps must contain MonitorStep values")
        projection = ledger.replay()
        proposal = _exact_record(projection.objects, self.proposal_id, "ProposedSubgraph")
        if proposal["content_hash"] != self.proposal_record_hash:
            raise AssentPlanError("proposal_record_hash does not match replay")
        if projection.proposal_states[self.proposal_id] != ProposalState.PROPOSED:
            raise AssentPlanError("proposal is not open for monitoring")
        policy = _exact_record(
            projection.objects,
            proposal["epistemic_policy_id"],
            "EpistemicPolicyArtifact",
        )
        if policy["content_hash"] != proposal["epistemic_policy_hash"]:
            raise AssentPlanError("proposal epistemic policy hash does not match replay")
        requirements = policy_requirements(policy)
        step_ids = [step.monitor_id for step in self.steps]
        expected_ids = [item["monitor_id"] for item in requirements]
        if step_ids != expected_ids:
            raise AssentPlanError(
                "steps must cover the policy's exact monitors in canonical order"
            )
        contexts = []
        for step, requirement in zip(self.steps, requirements, strict=True):
            if not callable(step.adapter):
                raise AssentPlanError(f"monitor '{step.monitor_id}' adapter is not callable")
            _validate_failure_plan(step.failure, ledger)
            event_ids = {event["event_id"] for event in projection.events}
            if step.failure.event_id in event_ids:
                raise AssentPlanError(
                    f"monitor '{step.monitor_id}' failure event ID already exists"
                )
            for record_id in (step.failure.failure_id, step.failure.assessment_id):
                if record_id in projection.objects:
                    raise AssentPlanError(
                        f"monitor '{step.monitor_id}' failure record ID already exists"
                    )
            _digest(step.monitor_record_hash, "monitor_record_hash")
            if step.monitor_record_hash != requirement["monitor_record_hash"]:
                raise AssentPlanError(
                    f"monitor '{step.monitor_id}' record hash differs from policy"
                )
            monitor = _exact_record(
                projection.objects,
                step.monitor_id,
                "MonitorSpecificationArtifact",
            )
            if monitor["content_hash"] != step.monitor_record_hash:
                raise AssentPlanError(
                    f"monitor '{step.monitor_id}' record hash does not match replay"
                )
            existing = projection.monitor_output_ids.get(
                (self.proposal_id, step.monitor_id)
            )
            if existing is not None:
                raise AssentPlanError(
                    f"monitor '{step.monitor_id}' already produced assessment '{existing}'"
                )
            inputs = []
            for artifact_id, artifact_hash in zip(
                monitor["input_artifact_ids"],
                monitor["input_artifact_record_hashes"],
                strict=True,
            ):
                artifact = _artifact_record(projection.objects, artifact_id)
                if artifact["content_hash"] != artifact_hash:
                    raise AssentPlanError("monitor input artifact changed after replay")
                inputs.append(_freeze(artifact))
            contexts.append(
                MonitorContext(
                    proposal=_freeze(proposal),
                    monitor=_freeze(monitor),
                    input_artifacts=tuple(inputs),
                )
            )
        return tuple(contexts)

    def _validate_success(
        self,
        events: Any,
        context: MonitorContext,
    ) -> None:
        if not isinstance(events, tuple) or not events:
            raise AssentPlanError(
                "monitor adapter must return MonitorEvent or a nonempty tuple"
            )
        if any(not isinstance(event, MonitorEvent) for event in events):
            raise AssentPlanError("monitor adapter returned a non-MonitorEvent value")
        kind = context.monitor["assessment_kind"]
        expected_types = (
            (EventType.LOGIC_CHECK_RECORDED, EventType.ASSESSMENT_RECORDED)
            if kind == "LOGICAL"
            else (EventType.ASSESSMENT_RECORDED,)
        )
        if tuple(event.event_type for event in events) != expected_types:
            raise AssentPlanError(
                f"{kind} adapter must return "
                + " then ".join(event_type.value for event_type in expected_types)
            )
        for event in events:
            for name, value in (
                ("event_id", event.event_id),
                ("transaction_time", event.transaction_time),
                ("actor_id", event.actor_id),
            ):
                _nonblank(value, name)
            if not isinstance(event.payload, Mapping):
                raise AssentPlanError("monitor event payload must be a mapping")
        payload = events[-1].payload
        if payload.get("assessment_type") != ASSESSMENT_TYPES_BY_KIND[kind]:
            raise AssentPlanError(f"{kind} adapter returned the wrong assessment type")
        if not isinstance(payload.get("assessment"), Mapping):
            raise AssentPlanError("assessment payload must be a mapping")
        if kind == "LOGICAL":
            if not isinstance(events[0].payload.get("check"), Mapping):
                raise AssentPlanError("logical adapter check payload must be a mapping")

    def _record_failure(
        self,
        ledger: ProtocolLedger,
        step: MonitorStep,
        context: MonitorContext,
        error: Exception,
    ) -> MonitorRunResult:
        failure_plan = step.failure
        message = str(error).strip() or f"{type(error).__name__} without a message"
        common = {
            "failure_id": failure_plan.failure_id,
            "assessment_id": failure_plan.assessment_id,
            "event_id": failure_plan.event_id,
            "generated_at": failure_plan.transaction_time,
            "actor_id": failure_plan.actor_id,
            "role": failure_plan.role,
            "proposal_id": context.proposal["id"],
            "proposal_content_hash": context.proposal["content_hash"],
            "base_acceptance_head": context.proposal["base_acceptance_head"],
            "monitor_id": context.monitor["id"],
            "monitor_version": context.monitor["artifact_version"],
            "monitor_hash": context.monitor["content_hash"],
            "failure_category": failure_plan.failure_category,
            "error_code": failure_plan.error_code,
        }
        if context.monitor["assessment_kind"] == "LOGICAL":
            contracts = [
                artifact
                for artifact in context.input_artifacts
                if artifact["artifact_kind"] == "LOGIC_CONTRACT"
            ]
            if len(contracts) != 1:
                raise AssentPlanError(
                    "LOGICAL monitor requires exactly one declared logic contract input"
                ) from error
            contract = contracts[0]
            failure, assessment = logic_monitor_failure_records(
                error=_logic_error(message),
                logic_contract_id=contract["id"],
                logic_contract_record_hash=contract["content_hash"],
                ruleset_id=contract["ruleset_id"],
                ruleset_record_hash=contract["ruleset_record_hash"],
                **common,
            )
        else:
            failure, assessment = monitor_failure_records(
                error=_monitoring_error(error, message),
                assessment_kind=context.monitor["assessment_kind"],
                **common,
            )
        envelope = ledger.append_event(
            event_id=failure_plan.event_id,
            event_type=EventType.MONITOR_FAILED,
            transaction_time=failure_plan.transaction_time,
            actor_id=failure_plan.actor_id,
            payload={
                "failure": failure,
                "assessment_type": "UnavailableAssessment",
                "assessment": assessment,
            },
        )
        return MonitorRunResult(
            monitor_id=step.monitor_id,
            assessment_id=assessment["id"],
            assessment_outcome="UNKNOWN",
            event_ids=(envelope["event_id"],),
        )


def _exact_record(
    objects: Mapping[str, Mapping[str, Any]],
    record_id: str,
    record_type: str,
) -> dict[str, Any]:
    item = objects.get(record_id)
    if item is None:
        raise AssentPlanError(f"unknown record '{record_id}'")
    if item["record_type"] != record_type:
        raise AssentPlanError(
            f"record '{record_id}' has type {item['record_type']}, expected {record_type}"
        )
    return item["record"]


def _artifact_record(
    objects: Mapping[str, Mapping[str, Any]],
    record_id: str,
) -> dict[str, Any]:
    item = objects.get(record_id)
    if item is None or "artifact_kind" not in item["record"]:
        raise AssentPlanError(f"unknown artifact '{record_id}'")
    return item["record"]


def _validate_failure_plan(plan: MonitorFailurePlan, ledger: ProtocolLedger) -> None:
    if not isinstance(plan, MonitorFailurePlan):
        raise AssentPlanError("failure must be a MonitorFailurePlan")
    for name in (
        "event_id",
        "failure_id",
        "assessment_id",
        "transaction_time",
        "actor_id",
        "role",
        "failure_category",
        "error_code",
    ):
        _nonblank(getattr(plan, name), name)
    if plan.failure_id == plan.assessment_id:
        raise AssentPlanError("failure_id and assessment_id must differ")
    try:
        aware_datetime(plan.transaction_time, "transaction_time")
    except LedgerError as error:
        raise AssentPlanError(str(error)) from error
    enums = {
        "failure_category": "MonitorFailureCategory",
        "error_code": "MonitorErrorCode",
        "role": "ResponsibleRole",
    }
    for field_name, enum_name in enums.items():
        value = getattr(plan, field_name)
        if value not in ledger.registry.get_enum_values(enum_name):
            raise AssentPlanError(f"{field_name} '{value}' is outside {enum_name}")


def _monitoring_error(error: Exception, message: str) -> MonitoringError:
    return error if isinstance(error, MonitoringError) else MonitoringError(message)


def _logic_error(message: str) -> LogicError:
    return LogicExecutionError(message)


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        copied = deepcopy(dict(value))
        return MappingProxyType({key: _freeze(item) for key, item in copied.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


def _nonblank(value: Any, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise AssentPlanError(f"{name} must be a nonblank string")


def _digest(value: Any, name: str) -> None:
    try:
        require_digest(value, name)
    except LedgerError as error:
        raise AssentPlanError(str(error)) from error
