"""Category-safe assent records and pure replay-derived state machines."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping

from malleus.ledger import (
    GENESIS,
    JsonlLedger,
    LedgerError,
    aware_datetime,
    content_digest,
    record_hash,
    require_digest,
    with_content_hash,
)
from malleus.ontology import OntologyRegistry
from malleus.logic import logic_contract_digest


class ProtocolError(LedgerError):
    """A typed record, reference, or state transition is invalid."""


class EventType(str, Enum):
    EXTERNAL_SNAPSHOT_ANCHORED = "EXTERNAL_SNAPSHOT_ANCHORED"
    ARTIFACT_RECORDED = "ARTIFACT_RECORDED"
    PROPOSAL_RECORDED = "PROPOSAL_RECORDED"
    LOGIC_CHECK_RECORDED = "LOGIC_CHECK_RECORDED"
    ASSESSMENT_RECORDED = "ASSESSMENT_RECORDED"
    MONITOR_FAILED = "MONITOR_FAILED"
    EPISTEMIC_DECIDED = "EPISTEMIC_DECIDED"
    AUTHORIZATION_DECIDED = "AUTHORIZATION_DECIDED"


class ProposalState(str, Enum):
    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    DEFERRED = "DEFERRED"
    CONTESTED = "CONTESTED"


class AuthorizationState(str, Enum):
    PENDING = "PENDING"
    AUTHORIZED = "AUTHORIZED"
    BLOCKED = "BLOCKED"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"


EPISTEMIC_TARGETS = {
    "ACCEPT": ProposalState.ACCEPTED,
    "REJECT": ProposalState.REJECTED,
    "DEFER": ProposalState.DEFERRED,
    "CONTEST": ProposalState.CONTESTED,
}
AUTHORIZATION_TARGETS = {
    "AUTHORIZE": AuthorizationState.AUTHORIZED,
    "BLOCK": AuthorizationState.BLOCKED,
    "CLARIFY": AuthorizationState.CLARIFICATION_REQUIRED,
}
PAYLOAD_FIELDS = {
    EventType.EXTERNAL_SNAPSHOT_ANCHORED: {
        "snapshot_id",
        "snapshot_hash",
        "source",
        "record_count",
        "opaque",
    },
    EventType.ARTIFACT_RECORDED: {"artifact_type", "artifact"},
    EventType.PROPOSAL_RECORDED: {"proposal", "members"},
    EventType.LOGIC_CHECK_RECORDED: {"check", "witnesses"},
    EventType.ASSESSMENT_RECORDED: {"assessment_type", "assessment"},
    EventType.MONITOR_FAILED: {"failure", "assessment_type", "assessment"},
    EventType.EPISTEMIC_DECIDED: {"decision", "requests", "revisions", "transition"},
    EventType.AUTHORIZATION_DECIDED: {"decision", "transition"},
}
PRESENT_FIELDS = {
    "ProposedSubgraph": {
        "claim_version_ids",
        "evidence_ids",
        "evidence_assertion_ids",
        "action_proposal_ids",
    },
    "ClaimVersion": {"dependency_ids"},
    "EpistemicDecision": {
        "evidence_assertion_ids",
        "request_ids",
        "claim_revision_ids",
    },
    "AuthorizationDecision": {
        "epistemic_decision_ids",
        "relied_on_claim_version_ids",
        "authority_assessment_ids",
    },
    "LogicalAssessment": {
        "checked_rule_ids",
        "violated_rule_ids",
        "logic_check_record_ids",
    },
    "LogicCheckRecord": {
        "context_state_digests",
        "translated_record_ids",
        "checked_rule_ids",
        "violated_rule_ids",
        "violation_witness_ids",
    },
    "ViolationWitness": {"witness_record_ids"},
}


@dataclass
class ProtocolProjection:
    """State rebuilt solely from verified immutable protocol events."""

    events: list[dict[str, Any]] = field(default_factory=list)
    objects: dict[str, dict[str, Any]] = field(default_factory=dict)
    artifact_ids: set[str] = field(default_factory=set)
    assessment_ids: set[str] = field(default_factory=set)
    logic_check_ids: set[str] = field(default_factory=set)
    violation_witness_ids: set[str] = field(default_factory=set)
    monitor_failure_ids: set[str] = field(default_factory=set)
    epistemic_decision_ids: set[str] = field(default_factory=set)
    authorization_decision_ids: set[str] = field(default_factory=set)
    proposal_states: dict[str, ProposalState] = field(default_factory=dict)
    authorization_states: dict[str, AuthorizationState] = field(default_factory=dict)
    request_states: dict[str, str] = field(default_factory=dict)
    action_to_proposal: dict[str, str] = field(default_factory=dict)
    current_claim_by_key: dict[str, str] = field(default_factory=dict)
    latest_action_by_key: dict[str, str] = field(default_factory=dict)
    superseded_claim_ids: set[str] = field(default_factory=set)
    snapshot_hash: str | None = None
    acceptance_head: str = GENESIS
    head_hash: str = GENESIS

    @property
    def event_count(self) -> int:
        return len(self.events)

    def copy(self) -> "ProtocolProjection":
        return deepcopy(self)


def make_record(
    record_type: str,
    *,
    event_id: str,
    generated_at: str,
    actor_id: str,
    role: str,
    source_record_ids: Iterable[str] = (),
    **fields: Any,
) -> dict[str, Any]:
    """Build one immutable record with its ledger-attribution fields."""
    return with_content_hash(
        record_type,
        {
            **fields,
            "generation_event_id": event_id,
            "generated_at": generated_at,
            "responsible_actor_id": actor_id,
            "responsible_role": role,
            "source_record_ids": list(source_record_ids),
        },
    )


class ProtocolLedger:
    """Assent state machine persisted through a strict JSONL ledger."""

    def __init__(self, path: str | Path, registry: OntologyRegistry):
        self.registry = registry
        self._validate_registry_contract()
        self.ontology_hash = f"sha256:{registry.content_hash()}"
        self.storage = JsonlLedger(path, self.ontology_hash)

    @property
    def path(self) -> Path:
        return self.storage.path

    def append_event(
        self,
        *,
        event_id: str,
        event_type: EventType | str,
        transaction_time: str,
        actor_id: str,
        payload: Mapping[str, Any],
    ) -> dict[str, Any]:
        name = event_type.value if isinstance(event_type, EventType) else event_type
        return self.storage.append(
            event_id=event_id,
            event_type=name,
            transaction_time=transaction_time,
            actor_id=actor_id,
            payload=payload,
            validate=self._replay_events,
        )

    def replay(
        self,
        *,
        expected_head_hash: str | None = None,
        expected_event_count: int | None = None,
    ) -> ProtocolProjection:
        events = self.storage.read(
            expected_head_hash=expected_head_hash,
            expected_event_count=expected_event_count,
        )
        if not events:
            raise ProtocolError("Protocol ledger is empty")
        return self._replay_events(events).copy()

    def _replay_events(self, events: list[dict[str, Any]]) -> ProtocolProjection:
        projection = ProtocolProjection()
        for event in events:
            self._apply(projection, event)
        return projection

    def _apply(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        context = f"event {event['event_id']}"
        try:
            event_type = EventType(event["event_type"])
        except ValueError as error:
            raise ProtocolError(f"{context}: unknown event_type '{event['event_type']}'") from error
        _exact_fields(event["payload"], PAYLOAD_FIELDS[event_type], f"{context} payload")
        handlers = {
            EventType.EXTERNAL_SNAPSHOT_ANCHORED: self._anchor,
            EventType.ARTIFACT_RECORDED: self._artifact,
            EventType.PROPOSAL_RECORDED: self._proposal,
            EventType.LOGIC_CHECK_RECORDED: self._logic_check,
            EventType.ASSESSMENT_RECORDED: self._assessment,
            EventType.MONITOR_FAILED: self._monitor_failure,
            EventType.EPISTEMIC_DECIDED: self._epistemic,
            EventType.AUTHORIZATION_DECIDED: self._authorization,
        }
        handlers[event_type](projection, event)
        projection.events.append(deepcopy(event))
        projection.head_hash = event["event_hash"]

    def _anchor(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        payload = event["payload"]
        if projection.events:
            raise ProtocolError(f"event {event['event_id']}: snapshot anchor must be first")
        if payload["opaque"] is not True:
            raise ProtocolError(f"event {event['event_id']}: external snapshot must be marked opaque")
        _nonblank(payload, ("snapshot_id", "source"), event["event_id"])
        require_digest(payload["snapshot_hash"], f"event {event['event_id']} snapshot_hash")
        if not isinstance(payload["record_count"], int) or isinstance(payload["record_count"], bool):
            raise ProtocolError(f"event {event['event_id']}: record_count must be an integer")
        if payload["record_count"] < 0:
            raise ProtocolError(f"event {event['event_id']}: record_count cannot be negative")
        projection.snapshot_hash = payload["snapshot_hash"]
        projection.acceptance_head = content_digest(
            {"opaque_external_snapshot": payload["snapshot_hash"]}
        )

    def _artifact(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        self._require_anchor(projection, event)
        artifact_type = event["payload"]["artifact_type"]
        artifact = self._record(
            artifact_type,
            event["payload"]["artifact"],
            event,
            root="ProtocolArtifact",
        )
        if artifact_type == "AuthorityGrant" and artifact["grantor_actor_id"] != event["actor_id"]:
            raise ProtocolError(
                f"event {event['event_id']}: AuthorityGrant grantor must be the generating actor"
            )
        if artifact_type == "LogicContractArtifact":
            self._validate_logic_contract_artifact(projection, artifact, event)
        self._validate_sources(artifact, projection.objects, event)
        self._add_objects(projection, {artifact["id"]: _wrapped(artifact_type, artifact)}, event)
        projection.artifact_ids.add(artifact["id"])

    def _validate_logic_contract_artifact(
        self,
        projection: ProtocolProjection,
        artifact: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        _canonical_unique(artifact["rule_ids"], f"event {event['event_id']} rule_ids")
        _nonblank_values(artifact["rule_ids"], f"event {event['event_id']} rule_ids")
        if not artifact["rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: logic contract has no rules")
        if artifact["ruleset_id"] not in artifact["source_record_ids"]:
            raise ProtocolError(f"event {event['event_id']}: logic contract sources must include ruleset")
        ruleset = self._artifact_ref(
            projection,
            artifact["ruleset_id"],
            artifact["ruleset_record_hash"],
            "RULE_SET",
        )
        if artifact["ruleset_version"] != ruleset["artifact_version"]:
            raise ProtocolError(f"event {event['event_id']}: logic contract ruleset_version mismatch")
        if artifact["ruleset_artifact_hash"] != ruleset["artifact_hash"]:
            raise ProtocolError(f"event {event['event_id']}: logic contract ruleset artifact hash mismatch")
        require_digest(artifact["ontology_hash"], f"event {event['event_id']} ontology_hash")
        expected_hash = logic_contract_digest(
            schema_version=artifact["logic_contract_schema_version"],
            contract_id=artifact["id"],
            contract_version=artifact["artifact_version"],
            ontology_hash=artifact["ontology_hash"],
            fact_contract_version=artifact["fact_contract_version"],
            ruleset_id=artifact["ruleset_id"],
            ruleset_version=artifact["ruleset_version"],
            rule_ids=artifact["rule_ids"],
            timeout_seconds=artifact["timeout_seconds"],
            ruleset_hash=artifact["ruleset_artifact_hash"],
        )
        if artifact["artifact_hash"] != expected_hash:
            raise ProtocolError(f"event {event['event_id']}: logic contract semantic hash mismatch")

    def _proposal(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        self._require_anchor(projection, event)
        payload = event["payload"]
        proposal = self._record("ProposedSubgraph", payload["proposal"], event)
        if proposal["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"event {event['event_id']}: proposal has stale base_acceptance_head")
        self._validate_proposal_revision(projection, proposal, event)
        if not isinstance(payload["members"], list) or not payload["members"]:
            raise ProtocolError(f"event {event['event_id']}: proposal members must be nonempty")

        members = {}
        category_ids = {
            "ClaimVersion": [],
            "Evidence": [],
            "EvidenceAssertion": [],
            "ActionProposal": [],
        }
        for index, wrapper in enumerate(payload["members"]):
            context = f"event {event['event_id']} member {index}"
            if not isinstance(wrapper, dict):
                raise ProtocolError(f"{context}: member must be an object")
            _exact_fields(wrapper, {"record_type", "record"}, context)
            record_type = wrapper["record_type"]
            category = self._proposal_member_category(record_type)
            record = self._record(record_type, wrapper["record"], event)
            if record["id"] in members or record["id"] == proposal["id"]:
                raise ProtocolError(f"{context}: duplicate object id '{record['id']}'")
            members[record["id"]] = _wrapped(record_type, record)
            category_ids[category].append(record["id"])

        expected = {
            "claim_version_ids": category_ids["ClaimVersion"],
            "evidence_ids": category_ids["Evidence"],
            "evidence_assertion_ids": category_ids["EvidenceAssertion"],
            "action_proposal_ids": category_ids["ActionProposal"],
        }
        for name, identifiers in expected.items():
            _same_unique_set(proposal[name], identifiers, f"event {event['event_id']} {name}")
        _same_unique_set(
            proposal["member_content_hashes"],
            [item["record"]["content_hash"] for item in members.values()],
            f"event {event['event_id']} member_content_hashes",
        )

        combined = {**projection.objects, **members}
        for item in members.values():
            record_type = item["record_type"]
            record = item["record"]
            self._validate_sources(record, combined, event)
            if record_type == "EvidenceAssertion":
                self._object(combined, record["claim_version_id"], "ClaimVersion")
                self._object(combined, record["evidence_id"], "Evidence")
            elif record_type == "ClaimVersion":
                self._validate_claim_lineage(combined, record, event)
            elif self.registry.is_subtype_of(record_type, "ActionProposal"):
                self._validate_action_lineage(projection, combined, record, event)
        action_keys = [
            members[action_id]["record"]["action_key"]
            for action_id in category_ids["ActionProposal"]
        ]
        _unique(action_keys, "proposal action_key values")

        introduced = {
            proposal["id"]: _wrapped("ProposedSubgraph", proposal),
            **members,
        }
        self._validate_sources(proposal, {**projection.objects, **introduced}, event)
        self._add_objects(projection, introduced, event)
        projection.proposal_states[proposal["id"]] = ProposalState.PROPOSED
        for action_id in category_ids["ActionProposal"]:
            action = members[action_id]["record"]
            projection.action_to_proposal[action_id] = proposal["id"]
            projection.authorization_states[action_id] = AuthorizationState.PENDING
            projection.latest_action_by_key[action["action_key"]] = action_id

    def _logic_check(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        self._require_anchor(projection, event)
        payload = event["payload"]
        check = self._record("LogicCheckRecord", payload["check"], event)
        proposal = self._object(projection.objects, check["proposal_id"], "ProposedSubgraph")
        if projection.proposal_states[proposal["id"]] != ProposalState.PROPOSED:
            raise ProtocolError(f"event {event['event_id']}: proposal is not open for logic check")
        self._same_proposal(check, proposal, event)
        if check["base_acceptance_head"] != proposal["base_acceptance_head"]:
            raise ProtocolError(f"event {event['event_id']}: logic check base mismatch")
        if check["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"event {event['event_id']}: logic check has stale acceptance head")

        monitor = self._artifact_ref(
            projection,
            check["monitor_id"],
            check["monitor_hash"],
            "MONITOR_SPECIFICATION",
        )
        if check["monitor_version"] != monitor["artifact_version"]:
            raise ProtocolError(f"event {event['event_id']}: monitor_version mismatch")
        contract = self._artifact_ref(
            projection,
            check["logic_contract_id"],
            check["logic_contract_record_hash"],
            "LOGIC_CONTRACT",
            record_type="LogicContractArtifact",
        )
        if check["logic_contract_version"] != contract["artifact_version"]:
            raise ProtocolError(f"event {event['event_id']}: logic_contract_version mismatch")
        if check["logic_contract_artifact_hash"] != contract["artifact_hash"]:
            raise ProtocolError(f"event {event['event_id']}: logic contract artifact hash mismatch")
        ruleset = self._artifact_ref(
            projection,
            check["ruleset_id"],
            check["ruleset_record_hash"],
            "RULE_SET",
        )
        if check["ruleset_version"] != ruleset["artifact_version"]:
            raise ProtocolError(f"event {event['event_id']}: ruleset_version mismatch")
        if check["ruleset_artifact_hash"] != ruleset["artifact_hash"]:
            raise ProtocolError(f"event {event['event_id']}: ruleset artifact hash mismatch")
        self._require_sources(
            check,
            {
                check["proposal_id"],
                check["monitor_id"],
                check["logic_contract_id"],
                check["ruleset_id"],
            },
            event,
        )
        contract_bindings = {
            "ontology_hash": "ontology hash",
            "fact_contract_version": "fact contract version",
            "ruleset_id": "ruleset",
            "ruleset_version": "ruleset version",
            "ruleset_artifact_hash": "ruleset artifact hash",
            "timeout_seconds": "timeout",
        }
        for name, label in contract_bindings.items():
            if check[name] != contract[name]:
                raise ProtocolError(f"event {event['event_id']}: logic check {label} differs from contract")
        _nonblank(
            check,
            (
                "monitor_id",
                "monitor_version",
                "logic_contract_id",
                "logic_contract_version",
                "ruleset_id",
                "ruleset_version",
                "engine_name",
                "engine_version",
            ),
            event["event_id"],
        )

        for name in (
            "candidate_digest",
            "base_state_digest",
            "candidate_state_digest",
            "ontology_hash",
            "facts_hash",
        ):
            require_digest(check[name], f"event {event['event_id']} {name}")
        for digest in check["context_state_digests"]:
            require_digest(digest, f"event {event['event_id']} context_state_digest")
        for name in (
            "context_state_digests",
            "translated_record_ids",
            "checked_rule_ids",
            "violated_rule_ids",
        ):
            _canonical_unique(check[name], f"event {event['event_id']} {name}")
        _unique(check["violation_witness_ids"], f"event {event['event_id']} violation_witness_ids")
        if not check["translated_record_ids"]:
            raise ProtocolError(f"event {event['event_id']}: logic check translated no records")
        for name in ("translated_record_ids", "checked_rule_ids", "violated_rule_ids"):
            _nonblank_values(check[name], f"event {event['event_id']} {name}")
        if not check["checked_rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: logic check checked no rules")
        if check["checked_rule_ids"] != contract["rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: checked rules differ from logic contract")
        if not set(check["violated_rule_ids"]).issubset(check["checked_rule_ids"]):
            raise ProtocolError(f"event {event['event_id']}: violated rules were not checked")
        if check["check_outcome"] == "SATISFIED" and check["violated_rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: SATISFIED logic check has violations")
        if check["check_outcome"] == "VIOLATED" and not check["violated_rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: VIOLATED logic check has no violations")

        if not isinstance(payload["witnesses"], list):
            raise ProtocolError(f"event {event['event_id']}: witnesses must be a list")
        witnesses: dict[str, dict[str, Any]] = {}
        for index, value in enumerate(payload["witnesses"]):
            witness = self._record("ViolationWitness", value, event)
            if witness["id"] in witnesses or witness["id"] in projection.objects:
                raise ProtocolError(
                    f"event {event['event_id']} witness {index}: duplicate object id '{witness['id']}'"
                )
            if witness["logic_check_id"] != check["id"]:
                raise ProtocolError(f"event {event['event_id']}: witness logic_check_id mismatch")
            self._require_sources(witness, {check["id"]}, event)
            if witness["rule_id"] not in check["violated_rule_ids"]:
                raise ProtocolError(f"event {event['event_id']}: witness cites nonviolated rule")
            _nonblank(
                witness,
                ("logic_check_id", "rule_id", "violation_code"),
                event["event_id"],
            )
            _canonical_unique(
                witness["witness_record_ids"],
                f"event {event['event_id']} witness_record_ids",
            )
            if not witness["witness_record_ids"]:
                raise ProtocolError(f"event {event['event_id']}: witness record IDs must be nonempty")
            _nonblank_values(
                witness["witness_record_ids"],
                f"event {event['event_id']} witness_record_ids",
            )
            if not set(witness["witness_record_ids"]).issubset(check["translated_record_ids"]):
                raise ProtocolError(f"event {event['event_id']}: witness cites untranslated record")
            expected_binding_hash = content_digest({
                "rule_id": witness["rule_id"],
                "violation_code": witness["violation_code"],
                "witness_record_ids": witness["witness_record_ids"],
            })
            if witness["witness_binding_hash"] != expected_binding_hash:
                raise ProtocolError(f"event {event['event_id']}: witness binding hash mismatch")
            witnesses[witness["id"]] = _wrapped("ViolationWitness", witness)

        _same_unique_set(
            check["violation_witness_ids"],
            witnesses,
            f"event {event['event_id']} violation_witness_ids",
        )
        witness_records = [item["record"] for item in witnesses.values()]
        if set(check["violated_rule_ids"]) != {item["rule_id"] for item in witness_records}:
            raise ProtocolError(f"event {event['event_id']}: every violated rule requires a witness")
        _unique(
            [item["witness_binding_hash"] for item in witness_records],
            "witness_binding_hash values",
        )

        introduced = {
            check["id"]: _wrapped("LogicCheckRecord", check),
            **witnesses,
        }
        combined = {**projection.objects, **introduced}
        self._validate_sources(check, combined, event)
        for item in witnesses.values():
            self._validate_sources(item["record"], combined, event)
        self._add_objects(projection, introduced, event)
        projection.logic_check_ids.add(check["id"])
        projection.violation_witness_ids.update(witnesses)

    def _assessment(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        self._require_anchor(projection, event)
        payload = event["payload"]
        assessment_type = payload["assessment_type"]
        assessment = self._record(assessment_type, payload["assessment"], event, root="Assessment")
        if assessment_type == "MonitorFailure":
            raise ProtocolError("MonitorFailure is not an Assessment")
        if assessment["assessment_outcome"] == "UNKNOWN":
            raise ProtocolError(
                f"event {event['event_id']}: UNKNOWN assessment requires atomic MONITOR_FAILED event"
            )
        self._validate_assessment_context(projection, assessment_type, assessment, event)
        if assessment.get("monitor_failure_id") is not None:
            raise ProtocolError(
                f"event {event['event_id']}: non-UNKNOWN assessment cannot cite MonitorFailure"
            )
        self._validate_sources(assessment, projection.objects, event)
        self._add_objects(
            projection,
            {assessment["id"]: _wrapped(assessment_type, assessment)},
            event,
        )
        projection.assessment_ids.add(assessment["id"])

    def _monitor_failure(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        self._require_anchor(projection, event)
        payload = event["payload"]
        failure = self._record("MonitorFailure", payload["failure"], event)
        assessment_type = payload["assessment_type"]
        assessment = self._record(assessment_type, payload["assessment"], event, root="Assessment")
        if assessment["assessment_outcome"] != "UNKNOWN":
            raise ProtocolError(f"event {event['event_id']}: failed monitor must produce UNKNOWN")
        if assessment.get("monitor_failure_id") != failure["id"]:
            raise ProtocolError(f"event {event['event_id']}: UNKNOWN assessment must cite failure")
        for name in (
            "proposal_id",
            "proposal_content_hash",
            "base_acceptance_head",
            "monitor_id",
            "monitor_version",
            "monitor_hash",
            "responsible_role",
        ):
            if assessment[name] != failure[name]:
                raise ProtocolError(f"event {event['event_id']}: failure and assessment {name} differ")
        if assessment["assessment_kind"] != failure["failed_assessment_kind"]:
            raise ProtocolError(f"event {event['event_id']}: failed assessment kind mismatch")
        required_failure_sources = {failure["proposal_id"], failure["monitor_id"]}
        required_assessment_sources = {
            assessment["proposal_id"],
            assessment["monitor_id"],
            failure["id"],
        }
        if assessment_type == "LogicalAssessment":
            for name in (
                "logic_contract_id",
                "logic_contract_record_hash",
                "ruleset_id",
                "ruleset_hash",
            ):
                if name not in failure or failure[name] != assessment[name]:
                    raise ProtocolError(
                        f"event {event['event_id']}: failure and assessment {name} differ"
                    )
            required_failure_sources.update({failure["logic_contract_id"], failure["ruleset_id"]})
            required_assessment_sources.update(
                {assessment["logic_contract_id"], assessment["ruleset_id"]}
            )
            contract = self._artifact_ref(
                projection,
                assessment["logic_contract_id"],
                assessment["logic_contract_record_hash"],
                "LOGIC_CONTRACT",
                record_type="LogicContractArtifact",
            )
            if assessment["ruleset_id"] != contract["ruleset_id"]:
                raise ProtocolError(
                    f"event {event['event_id']}: failed logical assessment ruleset differs from contract"
                )
            if assessment["ruleset_hash"] != contract["ruleset_record_hash"]:
                raise ProtocolError(
                    f"event {event['event_id']}: failed logical assessment ruleset hash mismatch"
                )
        self._require_sources(failure, required_failure_sources, event)
        self._require_sources(assessment, required_assessment_sources, event)
        self._validate_assessment_context(projection, assessment_type, assessment, event)
        combined = {
            **projection.objects,
            failure["id"]: _wrapped("MonitorFailure", failure),
            assessment["id"]: _wrapped(assessment_type, assessment),
        }
        self._validate_sources(failure, combined, event)
        self._validate_sources(assessment, combined, event)
        self._add_objects(
            projection,
            {
                failure["id"]: _wrapped("MonitorFailure", failure),
                assessment["id"]: _wrapped(assessment_type, assessment),
            },
            event,
        )
        projection.monitor_failure_ids.add(failure["id"])
        projection.assessment_ids.add(assessment["id"])

    def _epistemic(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        self._require_anchor(projection, event)
        payload = event["payload"]
        decision = self._record("EpistemicDecision", payload["decision"], event)
        proposal = self._object(projection.objects, decision["proposal_id"], "ProposedSubgraph")
        if projection.proposal_states[proposal["id"]] != ProposalState.PROPOSED:
            raise ProtocolError(f"event {event['event_id']}: proposal is not open")
        self._same_proposal(decision, proposal, event)
        if decision["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"event {event['event_id']}: decision has stale acceptance head")
        if proposal["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"event {event['event_id']}: proposal has stale acceptance head")
        self._artifact_ref(projection, decision["policy_id"], decision["policy_hash"], "EPISTEMIC_POLICY")
        self._artifact_ref(projection, decision["ruleset_id"], decision["ruleset_hash"], "RULE_SET")
        _unique(decision["assessment_ids"], "assessment_ids")
        if not decision["assessment_ids"]:
            raise ProtocolError(f"event {event['event_id']}: decision requires assessments")
        assessments = []
        for assessment_id in decision["assessment_ids"]:
            if assessment_id not in projection.assessment_ids:
                raise ProtocolError(f"event {event['event_id']}: assessment was not applied")
            assessment = self._object(projection.objects, assessment_id, "Assessment")
            self._same_proposal(assessment, proposal, event)
            if assessment["base_acceptance_head"] != projection.acceptance_head:
                raise ProtocolError(f"event {event['event_id']}: assessment has stale acceptance head")
            assessments.append(assessment)
        verdict = decision["epistemic_verdict"]
        if verdict not in EPISTEMIC_TARGETS:
            raise ProtocolError(f"event {event['event_id']}: invalid epistemic verdict '{verdict}'")
        if verdict == "ACCEPT" and any(
            assessment["assessment_outcome"] != "SATISFIED" for assessment in assessments
        ):
            raise ProtocolError(
                f"event {event['event_id']}: ACCEPT requires every cited assessment SATISFIED"
            )
        for assertion_id in decision["evidence_assertion_ids"]:
            self._object(projection.objects, assertion_id, "EvidenceAssertion")
            if assertion_id not in proposal["evidence_assertion_ids"]:
                raise ProtocolError(f"event {event['event_id']}: evidence is outside proposal")

        requests = self._embedded(projection, payload["requests"], event, root="Request")
        revisions = self._embedded(
            projection,
            payload["revisions"],
            event,
            exact_type="ClaimRevision",
        )
        _same_unique_set(decision["request_ids"], requests, f"event {event['event_id']} request_ids")
        _same_unique_set(
            decision["claim_revision_ids"],
            revisions,
            f"event {event['event_id']} claim_revision_ids",
        )
        for item in requests.values():
            request = item["record"]
            if request["triggering_decision_id"] != decision["id"]:
                raise ProtocolError(f"event {event['event_id']}: request decision reference mismatch")
            if request["target_proposal_id"] != proposal["id"] or request["request_state"] != "OPEN":
                raise ProtocolError(f"event {event['event_id']}: invalid new request state or target")
        if revisions and verdict != "ACCEPT":
            raise ProtocolError(f"event {event['event_id']}: revisions require ACCEPT")
        self._validate_claim_acceptance(projection, proposal, revisions, decision, event)

        transition = self._record("TransitionRecord", payload["transition"], event)
        self._transition(
            transition,
            subject=proposal["id"],
            from_state="PROPOSED",
            to_state=EPISTEMIC_TARGETS[verdict].value,
            trigger=decision["id"],
            event=event,
        )
        introduced = {
            decision["id"]: _wrapped("EpistemicDecision", decision),
            transition["id"]: _wrapped("TransitionRecord", transition),
            **requests,
            **revisions,
        }
        self._validate_sources(decision, {**projection.objects, **introduced}, event)
        for item in [*requests.values(), *revisions.values()]:
            self._validate_sources(item["record"], {**projection.objects, **introduced}, event)
        self._validate_sources(transition, {**projection.objects, **introduced}, event)
        self._add_objects(projection, introduced, event)
        projection.epistemic_decision_ids.add(decision["id"])
        projection.proposal_states[proposal["id"]] = EPISTEMIC_TARGETS[verdict]
        for request_id in requests:
            projection.request_states[request_id] = "OPEN"
        if verdict == "ACCEPT":
            revision_hashes = sorted(item["record"]["content_hash"] for item in revisions.values())
            projection.acceptance_head = content_digest(
                {
                    "previous_acceptance_head": projection.acceptance_head,
                    "proposal_content_hash": proposal["content_hash"],
                    "decision_content_hash": decision["content_hash"],
                    "revision_content_hashes": revision_hashes,
                }
            )

    def _authorization(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        self._require_anchor(projection, event)
        payload = event["payload"]
        decision = self._record("AuthorizationDecision", payload["decision"], event)
        action = self._object(projection.objects, decision["action_proposal_id"], "ActionProposal")
        action_id = action["id"]
        proposal_id = projection.action_to_proposal[action_id]
        proposal = self._object(projection.objects, proposal_id, "ProposedSubgraph")
        if projection.proposal_states[proposal_id] != ProposalState.ACCEPTED:
            raise ProtocolError(f"event {event['event_id']}: action proposal is not epistemically accepted")
        if projection.authorization_states[action_id] != AuthorizationState.PENDING:
            raise ProtocolError(f"event {event['event_id']}: action already has a terminal decision")
        if decision["action_content_hash"] != action["content_hash"]:
            raise ProtocolError(f"event {event['event_id']}: action_content_hash mismatch")
        if decision["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"event {event['event_id']}: authorization has stale acceptance head")
        self._artifact_ref(
            projection,
            decision["policy_id"],
            decision["policy_hash"],
            "AUTHORIZATION_POLICY",
        )
        grant = self._artifact_ref(
            projection,
            decision["authority_grant_id"],
            decision["authority_grant_hash"],
            "AUTHORITY_GRANT",
            record_type="AuthorityGrant",
        )
        _valid_interval(
            decision["authorization_valid_from"],
            decision.get("authorization_valid_to"),
            "authorization validity",
        )
        if grant["grantee_actor_id"] != decision["authorized_actor_id"]:
            raise ProtocolError(f"event {event['event_id']}: authority grant actor mismatch")
        if action["action_type"] not in grant["permitted_action_types"]:
            raise ProtocolError(f"event {event['event_id']}: action type is outside authority grant")
        if aware_datetime(
            decision["authorization_valid_from"],
            "authorization valid from",
        ) < aware_datetime(grant["grant_valid_from"], "grant valid from"):
            raise ProtocolError(f"event {event['event_id']}: authorization begins before its grant")
        grant_end = grant.get("grant_valid_to")
        authorization_end = decision.get("authorization_valid_to")
        if grant_end is not None and (
            authorization_end is None
            or aware_datetime(authorization_end, "authorization valid to")
            > aware_datetime(grant_end, "grant valid to")
        ):
            raise ProtocolError(f"event {event['event_id']}: authorization exceeds its grant")
        _unique(decision["epistemic_decision_ids"], "epistemic_decision_ids")
        accepted_decisions = []
        for decision_id in decision["epistemic_decision_ids"]:
            if decision_id not in projection.epistemic_decision_ids:
                raise ProtocolError(f"event {event['event_id']}: epistemic decision was not applied")
            epistemic = self._object(projection.objects, decision_id, "EpistemicDecision")
            if epistemic["epistemic_verdict"] == "ACCEPT" and epistemic["proposal_id"] == proposal_id:
                accepted_decisions.append(epistemic)
        if not accepted_decisions:
            raise ProtocolError(f"event {event['event_id']}: action proposal lacks ACCEPT decision")
        for claim_id in decision["relied_on_claim_version_ids"]:
            claim = self._object(projection.objects, claim_id, "ClaimVersion")
            if projection.current_claim_by_key.get(claim["claim_key"]) != claim_id:
                raise ProtocolError(f"event {event['event_id']}: authorization relies on noncurrent claim")

        assessments = []
        _unique(decision["authority_assessment_ids"], "authority_assessment_ids")
        for assessment_id in decision["authority_assessment_ids"]:
            if assessment_id not in projection.assessment_ids:
                raise ProtocolError(f"event {event['event_id']}: authority assessment was not applied")
            assessment = self._object(projection.objects, assessment_id, "AuthorityAssessment")
            if assessment["action_proposal_id"] != action_id:
                raise ProtocolError(f"event {event['event_id']}: authority assessment action mismatch")
            if assessment["proposal_id"] != proposal_id:
                raise ProtocolError(f"event {event['event_id']}: authority assessment proposal mismatch")
            if assessment["base_acceptance_head"] != projection.acceptance_head:
                raise ProtocolError(f"event {event['event_id']}: authority assessment is stale")
            if assessment["evaluated_actor_id"] != decision["authorized_actor_id"]:
                raise ProtocolError(f"event {event['event_id']}: authority assessment actor mismatch")
            if (
                assessment["authority_policy_id"] != decision["policy_id"]
                or assessment["authority_policy_hash"] != decision["policy_hash"]
            ):
                raise ProtocolError(f"event {event['event_id']}: authority policy mismatch")
            assessments.append(assessment)
        verdict = decision["authorization_verdict"]
        if verdict not in AUTHORIZATION_TARGETS:
            raise ProtocolError(f"event {event['event_id']}: invalid authorization verdict '{verdict}'")
        if verdict == "AUTHORIZE" and (
            not assessments
            or any(item["assessment_outcome"] != "SATISFIED" for item in assessments)
        ):
            raise ProtocolError(
                f"event {event['event_id']}: AUTHORIZE requires SATISFIED authority assessments"
            )
        transition = self._record("TransitionRecord", payload["transition"], event)
        self._transition(
            transition,
            subject=action_id,
            from_state="PENDING",
            to_state=AUTHORIZATION_TARGETS[verdict].value,
            trigger=decision["id"],
            event=event,
        )
        introduced = {
            decision["id"]: _wrapped("AuthorizationDecision", decision),
            transition["id"]: _wrapped("TransitionRecord", transition),
        }
        self._validate_sources(decision, {**projection.objects, **introduced}, event)
        self._validate_sources(transition, {**projection.objects, **introduced}, event)
        self._add_objects(projection, introduced, event)
        projection.authorization_decision_ids.add(decision["id"])
        projection.authorization_states[action_id] = AUTHORIZATION_TARGETS[verdict]

    def _validate_assessment_context(
        self,
        projection: ProtocolProjection,
        assessment_type: str,
        assessment: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        proposal = self._object(projection.objects, assessment["proposal_id"], "ProposedSubgraph")
        self._same_proposal(assessment, proposal, event)
        _unique(assessment["input_record_ids"], "assessment input_record_ids")
        if proposal["id"] not in assessment["input_record_ids"]:
            raise ProtocolError(f"event {event['event_id']}: assessment inputs must include proposal")
        for input_id in assessment["input_record_ids"]:
            if input_id not in projection.objects:
                raise ProtocolError(f"event {event['event_id']}: unknown assessment input '{input_id}'")
        monitor = self._artifact_ref(
            projection,
            assessment["monitor_id"],
            assessment["monitor_hash"],
            "MONITOR_SPECIFICATION",
        )
        if assessment["monitor_version"] != monitor["artifact_version"]:
            raise ProtocolError(f"event {event['event_id']}: monitor_version mismatch")
        if assessment_type == "AuthorityAssessment":
            if projection.proposal_states[proposal["id"]] != ProposalState.ACCEPTED:
                raise ProtocolError(f"event {event['event_id']}: authority checks require accepted proposal")
            if assessment["base_acceptance_head"] != projection.acceptance_head:
                raise ProtocolError(f"event {event['event_id']}: authority assessment is stale")
            action = self._object(
                projection.objects,
                assessment["action_proposal_id"],
                "ActionProposal",
            )
            if projection.action_to_proposal[action["id"]] != proposal["id"]:
                raise ProtocolError(f"event {event['event_id']}: authority action is outside proposal")
            if action["id"] not in assessment["input_record_ids"]:
                raise ProtocolError(f"event {event['event_id']}: authority inputs must include action")
            _unique(
                assessment["checked_policy_predicates"],
                "checked_policy_predicates",
            )
            _unique(
                assessment["violated_policy_predicates"],
                "violated_policy_predicates",
            )
            if not assessment["checked_policy_predicates"]:
                raise ProtocolError(
                    f"event {event['event_id']}: authority assessment checked no predicates"
                )
            if (
                assessment["assessment_outcome"] == "SATISFIED"
                and assessment["violated_policy_predicates"]
            ):
                raise ProtocolError(
                    f"event {event['event_id']}: SATISFIED authority assessment has violations"
                )
            if (
                assessment["assessment_outcome"] == "VIOLATED"
                and not assessment["violated_policy_predicates"]
            ):
                raise ProtocolError(
                    f"event {event['event_id']}: VIOLATED authority assessment has no violations"
                )
            self._artifact_ref(
                projection,
                assessment["authority_policy_id"],
                assessment["authority_policy_hash"],
                "AUTHORIZATION_POLICY",
            )
        else:
            if projection.proposal_states[proposal["id"]] != ProposalState.PROPOSED:
                raise ProtocolError(f"event {event['event_id']}: proposal is not open for assessment")
            if assessment["base_acceptance_head"] != proposal["base_acceptance_head"]:
                raise ProtocolError(f"event {event['event_id']}: assessment base mismatch")
        artifact_requirements = {
            "EvidenceCompletenessAssessment": (
                "evidence_contract_id",
                "evidence_contract_hash",
                "EVIDENCE_CONTRACT",
            ),
            "ConflictAssessment": ("conflict_rule_id", "conflict_rule_hash", "CONFLICT_RULE"),
            "UncertaintyAssessment": (
                "uncertainty_contract_id",
                "uncertainty_contract_hash",
                "UNCERTAINTY_CONTRACT",
            ),
            "TemporalAssessment": (
                "temporal_contract_id",
                "temporal_contract_hash",
                "TEMPORAL_CONTRACT",
            ),
            "LogicalAssessment": ("ruleset_id", "ruleset_hash", "RULE_SET"),
        }
        requirement = artifact_requirements.get(assessment_type)
        if requirement:
            self._artifact_ref(
                projection,
                assessment[requirement[0]],
                assessment[requirement[1]],
                requirement[2],
            )
        if assessment_type == "LogicalAssessment":
            self._validate_logical_assessment(projection, assessment, event)

    def _validate_logical_assessment(
        self,
        projection: ProtocolProjection,
        assessment: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        for name in ("checked_rule_ids", "violated_rule_ids"):
            _canonical_unique(assessment[name], f"event {event['event_id']} {name}")
        _unique(
            assessment["logic_check_record_ids"],
            f"event {event['event_id']} logic_check_record_ids",
        )
        contract = self._artifact_ref(
            projection,
            assessment["logic_contract_id"],
            assessment["logic_contract_record_hash"],
            "LOGIC_CONTRACT",
            record_type="LogicContractArtifact",
        )
        outcome = assessment["assessment_outcome"]
        required_sources = {
            assessment["proposal_id"],
            assessment["monitor_id"],
            assessment["logic_contract_id"],
            assessment["ruleset_id"],
        }
        if outcome == "UNKNOWN":
            self._require_sources(
                assessment,
                {*required_sources, assessment["monitor_failure_id"]},
                event,
            )
            if any(
                assessment[name]
                for name in ("checked_rule_ids", "violated_rule_ids", "logic_check_record_ids")
            ):
                raise ProtocolError(
                    f"event {event['event_id']}: UNKNOWN logical assessment cannot cite a completed check"
                )
            return
        if not assessment["checked_rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: logical assessment checked no rules")
        _nonblank_values(
            assessment["checked_rule_ids"],
            f"event {event['event_id']} checked_rule_ids",
        )
        _nonblank_values(
            assessment["violated_rule_ids"],
            f"event {event['event_id']} violated_rule_ids",
        )
        if not set(assessment["violated_rule_ids"]).issubset(assessment["checked_rule_ids"]):
            raise ProtocolError(f"event {event['event_id']}: violated rules were not checked")
        if outcome == "SATISFIED" and assessment["violated_rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: SATISFIED logical assessment has violations")
        if outcome == "VIOLATED" and not assessment["violated_rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: VIOLATED logical assessment has no violations")
        if len(assessment["logic_check_record_ids"]) != 1:
            raise ProtocolError(
                f"event {event['event_id']}: completed logical assessment requires one logic check"
            )
        check_id = assessment["logic_check_record_ids"][0]
        self._require_sources(assessment, {*required_sources, check_id}, event)
        if check_id not in projection.logic_check_ids:
            raise ProtocolError(f"event {event['event_id']}: logic check was not applied")
        if check_id not in assessment["input_record_ids"]:
            raise ProtocolError(f"event {event['event_id']}: assessment inputs must include logic check")
        check = self._object(projection.objects, check_id, "LogicCheckRecord")
        for name in (
            "proposal_id",
            "proposal_content_hash",
            "base_acceptance_head",
            "monitor_id",
            "monitor_version",
            "monitor_hash",
        ):
            if assessment[name] != check[name]:
                raise ProtocolError(f"event {event['event_id']}: assessment and logic check {name} differ")
        if assessment["ruleset_id"] != check["ruleset_id"]:
            raise ProtocolError(f"event {event['event_id']}: assessment and logic check ruleset differ")
        if assessment["ruleset_hash"] != check["ruleset_record_hash"]:
            raise ProtocolError(f"event {event['event_id']}: assessment ruleset hash mismatch")
        if assessment["logic_contract_id"] != check["logic_contract_id"]:
            raise ProtocolError(f"event {event['event_id']}: assessment logic contract differs")
        if assessment["logic_contract_record_hash"] != check["logic_contract_record_hash"]:
            raise ProtocolError(f"event {event['event_id']}: assessment logic contract hash mismatch")
        if contract["id"] != check["logic_contract_id"]:
            raise ProtocolError(f"event {event['event_id']}: applied logic contract differs")
        if assessment["checked_rule_ids"] != check["checked_rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: checked rules differ from logic check")
        if assessment["violated_rule_ids"] != check["violated_rule_ids"]:
            raise ProtocolError(f"event {event['event_id']}: violated rules differ from logic check")
        if outcome != check["check_outcome"]:
            raise ProtocolError(f"event {event['event_id']}: outcome differs from logic check")

    def _validate_claim_acceptance(
        self,
        projection: ProtocolProjection,
        proposal: dict[str, Any],
        revisions: dict[str, dict[str, Any]],
        decision: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        if decision["epistemic_verdict"] != "ACCEPT":
            if revisions:
                raise ProtocolError(f"event {event['event_id']}: non-acceptance cannot revise claims")
            return
        by_new = {}
        old_ids = set()
        for item in revisions.values():
            revision = item["record"]
            old_id = revision["replaced_claim_version_id"]
            new_id = revision["replacement_claim_version_id"]
            if old_id in old_ids or new_id in by_new:
                raise ProtocolError(f"event {event['event_id']}: claim revision endpoints must be unique")
            if revision["triggering_decision_id"] != decision["id"]:
                raise ProtocolError(f"event {event['event_id']}: revision decision reference mismatch")
            old_ids.add(old_id)
            by_new[new_id] = revision

        proposed_claims = [
            self._object(projection.objects, claim_id, "ClaimVersion")
            for claim_id in proposal["claim_version_ids"]
        ]
        keys = [claim["claim_key"] for claim in proposed_claims]
        _unique(keys, "accepted proposal claim_key values")
        for claim in proposed_claims:
            current_id = projection.current_claim_by_key.get(claim["claim_key"])
            revision = by_new.get(claim["id"])
            if current_id is None:
                if claim["revision"] != 1 or claim.get("revises_claim_version_id") is not None:
                    raise ProtocolError(f"event {event['event_id']}: first accepted claim must be revision 1")
                if revision is not None:
                    raise ProtocolError(f"event {event['event_id']}: new claim cannot have ClaimRevision")
            else:
                if revision is None or revision["replaced_claim_version_id"] != current_id:
                    raise ProtocolError(f"event {event['event_id']}: replacement claim needs atomic revision")
                old = self._object(projection.objects, current_id, "ClaimVersion")
                if claim["revision"] != old["revision"] + 1:
                    raise ProtocolError(f"event {event['event_id']}: claim revisions must be contiguous")
                if claim.get("revises_claim_version_id") != current_id:
                    raise ProtocolError(f"event {event['event_id']}: direct claim revision link mismatch")
                if revision["replacement_valid_from"] != claim["domain_valid_from"]:
                    raise ProtocolError(f"event {event['event_id']}: replacement valid time mismatch")
                if revision["replaced_valid_to"] != claim["domain_valid_from"]:
                    raise ProtocolError(f"event {event['event_id']}: replaced interval must close at replacement")
                _valid_interval(old["domain_valid_from"], revision["replaced_valid_to"], "claim revision")
        if set(by_new) != {
            claim["id"] for claim in proposed_claims if projection.current_claim_by_key.get(claim["claim_key"])
        }:
            raise ProtocolError(f"event {event['event_id']}: revision records do not match replacements")
        for claim in proposed_claims:
            old_id = projection.current_claim_by_key.get(claim["claim_key"])
            if old_id:
                projection.superseded_claim_ids.add(old_id)
            projection.current_claim_by_key[claim["claim_key"]] = claim["id"]

    def _validate_proposal_revision(
        self,
        projection: ProtocolProjection,
        proposal: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        previous_id = proposal.get("revises_proposal_id")
        if proposal["revision"] == 1:
            if previous_id is not None:
                raise ProtocolError(f"event {event['event_id']}: first proposal cannot revise another")
            return
        previous = self._object(projection.objects, previous_id, "ProposedSubgraph")
        if previous["proposal_key"] != proposal["proposal_key"]:
            raise ProtocolError(f"event {event['event_id']}: proposal lineage key mismatch")
        if previous["revision"] + 1 != proposal["revision"]:
            raise ProtocolError(f"event {event['event_id']}: proposal revisions must be contiguous")
        if projection.proposal_states[previous_id] == ProposalState.PROPOSED:
            raise ProtocolError(f"event {event['event_id']}: cannot revise an open proposal")

    def _validate_claim_lineage(
        self,
        objects: Mapping[str, dict[str, Any]],
        claim: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        previous_id = claim.get("revises_claim_version_id")
        if claim["revision"] == 1:
            if previous_id is not None:
                raise ProtocolError(f"event {event['event_id']}: first claim cannot revise another")
            return
        previous = self._object(objects, previous_id, "ClaimVersion")
        if previous["claim_key"] != claim["claim_key"] or previous["revision"] + 1 != claim["revision"]:
            raise ProtocolError(f"event {event['event_id']}: invalid claim lineage")

    def _validate_action_lineage(
        self,
        projection: ProtocolProjection,
        objects: Mapping[str, dict[str, Any]],
        action: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        previous_id = action.get("revises_action_proposal_id")
        if action["revision"] == 1:
            if previous_id is not None:
                raise ProtocolError(f"event {event['event_id']}: first action cannot revise another")
            if action["action_key"] in projection.latest_action_by_key:
                raise ProtocolError(f"event {event['event_id']}: duplicate action lineage root")
            return
        if projection.latest_action_by_key.get(action["action_key"]) != previous_id:
            raise ProtocolError(f"event {event['event_id']}: action revision must extend latest revision")
        previous = self._object(objects, previous_id, "ActionProposal")
        if previous["action_key"] != action["action_key"] or previous["revision"] + 1 != action["revision"]:
            raise ProtocolError(f"event {event['event_id']}: invalid action lineage")
        prior_proposal_id = projection.action_to_proposal[previous_id]
        if (
            projection.authorization_states.get(previous_id) == AuthorizationState.PENDING
            and projection.proposal_states[prior_proposal_id] == ProposalState.ACCEPTED
        ):
            raise ProtocolError(f"event {event['event_id']}: cannot revise a pending accepted action")

    def _proposal_member_category(self, record_type: str) -> str:
        if record_type in {"ClaimVersion", "Evidence", "EvidenceAssertion"}:
            return record_type
        if self.registry.has_type(record_type) and self.registry.is_subtype_of(record_type, "ActionProposal"):
            if self.registry.get_type(record_type).abstract:
                raise ProtocolError(f"Proposal member type '{record_type}' is abstract")
            return "ActionProposal"
        raise ProtocolError(f"'{record_type}' is not an allowed proposed content type")

    def _record(
        self,
        record_type: Any,
        value: Any,
        event: Mapping[str, Any],
        *,
        root: str | None = None,
    ) -> dict[str, Any]:
        if not isinstance(record_type, str) or not self.registry.has_type(record_type):
            raise ProtocolError(f"Unknown protocol record type: '{record_type}'")
        typedef = self.registry.get_type(record_type)
        if typedef.abstract:
            raise ProtocolError(f"Protocol record type '{record_type}' is abstract")
        if root and not self.registry.is_subtype_of(record_type, root):
            raise ProtocolError(f"'{record_type}' is not a {root} subtype")
        if not isinstance(value, dict):
            raise ProtocolError(f"{record_type} record must be an object")
        errors = self.registry.validate_instance(record_type, value)
        if errors:
            raise ProtocolError(f"Invalid {record_type}: {'; '.join(errors)}")
        required_presence = {"source_record_ids", *PRESENT_FIELDS.get(record_type, set())}
        missing_presence = sorted(required_presence - set(value))
        if missing_presence:
            raise ProtocolError(
                f"Invalid {record_type}: missing required fields: {', '.join(missing_presence)}"
            )
        if value["content_hash"] != record_hash(record_type, value):
            raise ProtocolError(f"Invalid {record_type}: content_hash mismatch")
        if value["generation_event_id"] != event["event_id"]:
            raise ProtocolError(f"Invalid {record_type}: generation_event_id mismatch")
        if aware_datetime(value["generated_at"], f"{record_type} generated_at") != aware_datetime(
            event["transaction_time"],
            "event transaction_time",
        ):
            raise ProtocolError(f"Invalid {record_type}: generated_at mismatch")
        if value["responsible_actor_id"] != event["actor_id"]:
            raise ProtocolError(f"Invalid {record_type}: responsible_actor_id mismatch")
        _hash_fields(value, record_type)
        _time_fields(value, record_type)
        return deepcopy(value)

    def _embedded(
        self,
        projection: ProtocolProjection,
        values: Any,
        event: dict[str, Any],
        *,
        root: str | None = None,
        exact_type: str | None = None,
    ) -> dict[str, dict[str, Any]]:
        if not isinstance(values, list):
            raise ProtocolError(f"event {event['event_id']}: embedded records must be a list")
        result = {}
        for index, wrapper in enumerate(values):
            context = f"event {event['event_id']} embedded record {index}"
            if not isinstance(wrapper, dict):
                raise ProtocolError(f"{context}: wrapper must be an object")
            _exact_fields(wrapper, {"record_type", "record"}, context)
            record_type = wrapper["record_type"]
            if exact_type and record_type != exact_type:
                raise ProtocolError(f"{context}: expected {exact_type}")
            record = self._record(record_type, wrapper["record"], event, root=root)
            if record["id"] in projection.objects or record["id"] in result:
                raise ProtocolError(f"{context}: duplicate object id '{record['id']}'")
            result[record["id"]] = _wrapped(record_type, record)
        return result

    def _artifact_ref(
        self,
        projection: ProtocolProjection,
        artifact_id: str,
        artifact_hash: str,
        artifact_kind: str,
        *,
        record_type: str = "ProtocolArtifact",
    ) -> dict[str, Any]:
        if artifact_id not in projection.artifact_ids:
            raise ProtocolError(f"Unknown applied artifact '{artifact_id}'")
        artifact = self._object(projection.objects, artifact_id, record_type)
        if artifact["content_hash"] != artifact_hash:
            raise ProtocolError(f"Artifact hash mismatch for '{artifact_id}'")
        if artifact["artifact_kind"] != artifact_kind:
            raise ProtocolError(
                f"Artifact '{artifact_id}' has kind {artifact['artifact_kind']}, expected {artifact_kind}"
            )
        return artifact

    def _same_proposal(
        self,
        record: Mapping[str, Any],
        proposal: Mapping[str, Any],
        event: Mapping[str, Any],
    ) -> None:
        if record["proposal_content_hash"] != proposal["content_hash"]:
            raise ProtocolError(f"event {event['event_id']}: proposal_content_hash mismatch")

    def _transition(
        self,
        transition: Mapping[str, Any],
        *,
        subject: str,
        from_state: str,
        to_state: str,
        trigger: str,
        event: Mapping[str, Any],
    ) -> None:
        expected = {
            "transition_subject_id": subject,
            "from_state": from_state,
            "to_state": to_state,
            "triggering_record_id": trigger,
            "ledger_event_id": event["event_id"],
            "sequence": event["sequence"],
            "transition_time": event["transaction_time"],
        }
        for name, value in expected.items():
            if transition[name] != value:
                raise ProtocolError(f"event {event['event_id']}: transition {name} mismatch")

    def _validate_sources(
        self,
        record: Mapping[str, Any],
        objects: Mapping[str, dict[str, Any]],
        event: Mapping[str, Any],
    ) -> None:
        _unique(record["source_record_ids"], f"{record['id']} source_record_ids")
        for source_id in record["source_record_ids"]:
            if source_id not in objects:
                raise ProtocolError(f"event {event['event_id']}: unknown source record '{source_id}'")

    def _require_sources(
        self,
        record: Mapping[str, Any],
        required: set[str],
        event: Mapping[str, Any],
    ) -> None:
        missing = sorted(required - set(record["source_record_ids"]))
        if missing:
            raise ProtocolError(
                f"event {event['event_id']}: {record['id']} source_record_ids missing "
                f"required records: {', '.join(missing)}"
            )

    def _object(
        self,
        objects: Mapping[str, dict[str, Any]],
        object_id: Any,
        expected_type: str,
    ) -> dict[str, Any]:
        if not isinstance(object_id, str) or object_id not in objects:
            raise ProtocolError(f"Unknown referenced object '{object_id}'")
        item = objects[object_id]
        if not self.registry.is_subtype_of(item["record_type"], expected_type):
            raise ProtocolError(
                f"Object '{object_id}' has type {item['record_type']}, expected {expected_type}"
            )
        return item["record"]

    @staticmethod
    def _add_objects(
        projection: ProtocolProjection,
        introduced: Mapping[str, dict[str, Any]],
        event: Mapping[str, Any],
    ) -> None:
        overlap = set(projection.objects) & set(introduced)
        if overlap:
            raise ProtocolError(f"event {event['event_id']}: duplicate object id '{sorted(overlap)[0]}'")
        if len(introduced) != len(set(introduced)):
            raise ProtocolError(f"event {event['event_id']}: duplicate object ids")
        projection.objects.update(deepcopy(dict(introduced)))

    @staticmethod
    def _require_anchor(projection: ProtocolProjection, event: Mapping[str, Any]) -> None:
        if projection.snapshot_hash is None:
            raise ProtocolError(
                f"event {event['event_id']}: first event must anchor an external snapshot"
            )

    def _validate_registry_contract(self) -> None:
        required = {
            "ProtocolRecord",
            "ProtocolArtifact",
            "LogicContractArtifact",
            "AuthorityGrant",
            "ProposedSubgraph",
            "ClaimVersion",
            "Evidence",
            "EvidenceAssertion",
            "ActionProposal",
            "Assessment",
            "TypeAssessment",
            "EvidenceCompletenessAssessment",
            "ConflictAssessment",
            "UncertaintyAssessment",
            "LogicalAssessment",
            "LogicCheckRecord",
            "ViolationWitness",
            "TemporalAssessment",
            "AuthorityAssessment",
            "Decision",
            "MonitorFailure",
            "EpistemicDecision",
            "AuthorizationDecision",
            "Request",
            "EvidenceRequest",
            "HumanReviewRequest",
            "ReviewReport",
            "ClaimRevision",
            "TransitionRecord",
            "ActionExecution",
            "OutcomeObservation",
        }
        missing = sorted(name for name in required if not self.registry.has_type(name))
        if missing:
            raise ProtocolError(f"Assent ontology is missing required classes: {', '.join(missing)}")
        abstract_types = {"ProtocolRecord", "Assessment", "Decision", "Request", "ActionProposal"}
        for name in abstract_types:
            if not self.registry.get_type(name).abstract:
                raise ProtocolError(f"Assent ontology class '{name}' must be abstract")
        inheritance = {
            "ProtocolRecord": "Entity",
            "ProtocolArtifact": "ProtocolRecord",
            "LogicContractArtifact": "ProtocolArtifact",
            "AuthorityGrant": "ProtocolArtifact",
            "ProposedSubgraph": "ProtocolRecord",
            "ClaimVersion": "ProtocolRecord",
            "Evidence": "ProtocolRecord",
            "EvidenceAssertion": "ProtocolRecord",
            "ActionProposal": "ProtocolRecord",
            "Assessment": "ProtocolRecord",
            "TypeAssessment": "Assessment",
            "EvidenceCompletenessAssessment": "Assessment",
            "ConflictAssessment": "Assessment",
            "UncertaintyAssessment": "Assessment",
            "LogicalAssessment": "Assessment",
            "LogicCheckRecord": "ProtocolRecord",
            "ViolationWitness": "ProtocolRecord",
            "TemporalAssessment": "Assessment",
            "AuthorityAssessment": "Assessment",
            "MonitorFailure": "ProtocolRecord",
            "Decision": "ProtocolRecord",
            "EpistemicDecision": "Decision",
            "AuthorizationDecision": "Decision",
            "Request": "ProtocolRecord",
            "EvidenceRequest": "Request",
            "HumanReviewRequest": "Request",
            "ReviewReport": "ProtocolRecord",
            "ClaimRevision": "ProtocolRecord",
            "TransitionRecord": "ProtocolRecord",
            "ActionExecution": "ProtocolRecord",
            "OutcomeObservation": "ProtocolRecord",
        }
        for child, parent in inheritance.items():
            if not self.registry.is_subtype_of(child, parent):
                raise ProtocolError(f"Assent ontology class '{child}' must inherit '{parent}'")
        if self.registry.is_subtype_of("MonitorFailure", "Assessment"):
            raise ProtocolError("Assent ontology MonitorFailure must not be an Assessment")
        enum_values = {
            "AssessmentOutcome": {"SATISFIED", "VIOLATED", "UNKNOWN"},
            "LogicCheckOutcome": {"SATISFIED", "VIOLATED"},
            "EpistemicVerdict": {"ACCEPT", "REJECT", "DEFER", "CONTEST"},
            "AuthorizationVerdict": {"AUTHORIZE", "BLOCK", "CLARIFY"},
            "RequestState": {"OPEN", "FULFILLED", "CANCELLED"},
        }
        for name, expected in enum_values.items():
            if not self.registry.has_enum(name) or self.registry.get_enum_values(name) != expected:
                raise ProtocolError(f"Assent ontology enum '{name}' does not match the protocol")


def _wrapped(record_type: str, record: dict[str, Any]) -> dict[str, Any]:
    return {"record_type": record_type, "record": deepcopy(record)}


def _exact_fields(value: Mapping[str, Any], expected: set[str], context: str) -> None:
    if not isinstance(value, Mapping):
        raise ProtocolError(f"{context} must be an object")
    if any(not isinstance(key, str) for key in value):
        raise ProtocolError(f"{context} keys must be strings")
    missing = sorted(expected - set(value))
    unknown = sorted(set(value) - expected)
    if missing:
        raise ProtocolError(f"{context}: missing required fields: {', '.join(missing)}")
    if unknown:
        raise ProtocolError(f"{context}: unknown fields: {', '.join(unknown)}")


def _nonblank(value: Mapping[str, Any], names: Iterable[str], context: str) -> None:
    invalid = [name for name in names if not isinstance(value[name], str) or not value[name].strip()]
    if invalid:
        raise ProtocolError(f"{context}: fields must be nonblank: {', '.join(invalid)}")


def _unique(values: Any, context: str) -> None:
    if not isinstance(values, list):
        raise ProtocolError(f"{context} must be a list")
    if len(values) != len(set(values)):
        raise ProtocolError(f"{context} contains duplicates")


def _canonical_unique(values: Any, context: str) -> None:
    _unique(values, context)
    if values != sorted(values):
        raise ProtocolError(f"{context} must be in canonical sorted order")


def _nonblank_values(values: list[Any], context: str) -> None:
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ProtocolError(f"{context} must contain nonblank strings")


def _same_unique_set(actual: Any, expected: Iterable[Any], context: str) -> None:
    _unique(actual, context)
    expected_list = list(expected)
    if sorted(actual) != sorted(expected_list):
        raise ProtocolError(f"{context} does not exactly match introduced records")


def _hash_fields(value: Any, context: str) -> None:
    if isinstance(value, dict):
        for name, item in value.items():
            if name.endswith(("_hash", "_head")) and item is not None:
                require_digest(item, f"{context} {name}")
            _hash_fields(item, f"{context}.{name}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _hash_fields(item, f"{context}[{index}]")


def _time_fields(record: Mapping[str, Any], context: str) -> None:
    for name, value in record.items():
        if value is not None and name.endswith(("_at", "_from", "_to")):
            aware_datetime(value, f"{context} {name}")
    for start, end in (
        ("domain_valid_from", "domain_valid_to"),
        ("issued_at", "expires_at"),
        ("authorization_valid_from", "authorization_valid_to"),
        ("grant_valid_from", "grant_valid_to"),
        ("execution_started_at", "execution_ended_at"),
    ):
        if record.get(start) is not None:
            _valid_interval(record[start], record.get(end), f"{context} {start}/{end}")


def _valid_interval(start: str, end: str | None, context: str) -> None:
    parsed_start = aware_datetime(start, f"{context} start")
    if end is not None and aware_datetime(end, f"{context} end") <= parsed_start:
        raise ProtocolError(f"{context}: end must be later than start")
