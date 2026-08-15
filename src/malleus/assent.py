"""Category-safe assent records and pure replay-derived state machines."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
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
from malleus.kg import KnowledgeGraph
from malleus.logic import logic_contract_digest
from malleus.accepted import (
    AcceptedGraphError,
    acceptance_result_head,
    accepted_application_record,
    apply_temporal_writes,
    base_record_metadata,
    candidate_artifact_digest,
    graph_base_artifact_digest,
    graph_base_operations,
    parse_candidate_manifest,
    parse_graph_base_metadata,
    validate_temporal_writes,
)
from malleus.staging import StagingError, stage_subgraph
from malleus.source import SourceError, source_artifact_digest
from malleus.control import (
    ControlError,
    EPISTEMIC_MONITOR_KINDS,
    authorization_policy_digest,
    authorization_policy_requirements,
    epistemic_policy_digest,
    evaluate_authorization_policy,
    evaluate_epistemic_policy,
    monitor_specification_digest,
    policy_requirements,
)


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
ASSESSMENT_TYPES_BY_KIND = {
    "TYPE": "TypeAssessment",
    "EVIDENCE_COMPLETENESS": "EvidenceCompletenessAssessment",
    "CONFLICT": "ConflictAssessment",
    "UNCERTAINTY": "UncertaintyAssessment",
    "LOGICAL": "LogicalAssessment",
    "TEMPORAL": "TemporalAssessment",
    "AUTHORITY": "AuthorityAssessment",
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
    EventType.EPISTEMIC_DECIDED: {
        "decision",
        "requests",
        "revisions",
        "transition",
        "application",
    },
    EventType.AUTHORIZATION_DECIDED: {"decision", "transition"},
}
PRESENT_FIELDS = {
    "MonitorSpecificationArtifact": {
        "input_artifact_ids",
        "input_artifact_record_hashes",
    },
    "EpistemicPolicyArtifact": {
        "required_monitor_ids",
        "required_monitor_record_hashes",
        "violation_verdicts",
        "unknown_verdicts",
        "control_precedence",
    },
    "AuthorizationPolicyArtifact": {
        "required_monitor_ids",
        "required_monitor_record_hashes",
    },
    "ProposedSubgraph": {
        "claim_version_ids",
        "evidence_ids",
        "evidence_assertion_ids",
        "action_proposal_ids",
    },
    "ClaimVersion": {"dependency_ids"},
    "EpistemicDecision": {
        "triggered_assessment_ids",
        "evidence_assertion_ids",
        "request_ids",
        "claim_revision_ids",
    },
    "EvidenceCompletenessAssessment": {"missing_requirement_ids"},
    "ConflictAssessment": {"conflicting_assertion_ids"},
    "AuthorizationDecision": {
        "epistemic_decision_ids",
        "relied_on_claim_version_ids",
        "authority_assessment_ids",
        "triggered_assessment_ids",
        "authority_grant_id",
        "authority_grant_hash",
        "authorization_valid_from",
        "authorization_valid_to",
    },
    "AuthorityAssessment": {
        "checked_policy_predicates",
        "violated_policy_predicates",
        "evaluated_authority_grant_id",
        "evaluated_authority_grant_hash",
    },
    "UnavailableAuthorityAssessment": {
        "evaluated_authority_grant_id",
        "evaluated_authority_grant_hash",
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
    "AcceptedGraphApplication": {"applied_record_ids"},
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
    action_to_proposal: dict[str, str] = field(default_factory=dict)
    current_claim_by_key: dict[str, str] = field(default_factory=dict)
    latest_action_by_key: dict[str, str] = field(default_factory=dict)
    superseded_claim_ids: set[str] = field(default_factory=set)
    monitor_output_ids: dict[tuple[str, ...], str] = field(default_factory=dict)
    logic_check_by_monitor_context: dict[tuple[str, str], str] = field(default_factory=dict)
    snapshot_hash: str | None = None
    acceptance_head: str = GENESIS
    materialization_head: str = GENESIS
    graph_base_id: str | None = None
    graph_base_hash: str | None = None
    accepted_graph: KnowledgeGraph | None = None
    accepted_record_metadata: dict[str, dict[str, Any]] = field(default_factory=dict)
    candidate_manifests: dict[str, tuple[Any, ...]] = field(default_factory=dict)
    accepted_application_ids: set[str] = field(default_factory=set)
    accepted_application_order: list[str] = field(default_factory=list)
    applied_candidate_ids: set[str] = field(default_factory=set)
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

    def __init__(
        self,
        path: str | Path,
        registry: OntologyRegistry,
        *,
        accepted_graph_base: KnowledgeGraph | None = None,
    ):
        self.registry = registry
        self._validate_registry_contract()
        self.ontology_hash = f"sha256:{registry.content_hash()}"
        if accepted_graph_base is not None:
            if not isinstance(accepted_graph_base, KnowledgeGraph):
                raise TypeError("accepted_graph_base must be a KnowledgeGraph")
            base_ontology_hash = f"sha256:{accepted_graph_base.registry.content_hash()}"
            if base_ontology_hash != self.ontology_hash:
                raise ProtocolError(
                    "accepted_graph_base and protocol ledger must use the same ontology"
                )
        self._accepted_graph_base = (
            accepted_graph_base.state_projection()
            if accepted_graph_base is not None
            else None
        )
        self._storage = JsonlLedger(path, self.ontology_hash)

    @property
    def path(self) -> Path:
        return self._storage.path

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
        return self._storage.append(
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
        events = self._read_events(
            expected_head_hash=expected_head_hash,
            expected_event_count=expected_event_count,
        )
        if not events:
            raise ProtocolError("Protocol ledger is empty")
        return self._replay_events(events).copy()

    def _read_events(
        self,
        *,
        expected_head_hash: str | None = None,
        expected_event_count: int | None = None,
    ) -> list[dict[str, Any]]:
        return self._storage.read(
            expected_head_hash=expected_head_hash,
            expected_event_count=expected_event_count,
        )

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
        if artifact_type == "AuthorityGrant":
            _canonical_unique(
                artifact["permitted_action_types"],
                f"event {event['event_id']} permitted_action_types",
            )
            _nonblank_values(
                artifact["permitted_action_types"],
                f"event {event['event_id']} permitted_action_types",
            )
            if not artifact["permitted_action_types"]:
                raise ProtocolError(
                    f"event {event['event_id']}: AuthorityGrant permits no action types"
                )
        typed_artifacts = {
            "SOURCE": "SourceArtifact",
            "GRAPH_BASE": "GraphBaseArtifact",
            "CANDIDATE_SUBGRAPH": "CandidateSubgraphArtifact",
            "MONITOR_SPECIFICATION": "MonitorSpecificationArtifact",
            "EPISTEMIC_POLICY": "EpistemicPolicyArtifact",
            "AUTHORIZATION_POLICY": "AuthorizationPolicyArtifact",
            "LOGIC_CONTRACT": "LogicContractArtifact",
        }
        expected_type = typed_artifacts.get(artifact["artifact_kind"])
        if expected_type and artifact_type != expected_type:
            raise ProtocolError(
                f"event {event['event_id']}: {artifact['artifact_kind']} requires {expected_type}"
            )
        candidate_manifest = None
        if artifact_type == "SourceArtifact":
            self._validate_source_artifact(artifact, event)
        elif artifact_type == "GraphBaseArtifact":
            self._validate_graph_base_artifact(projection, artifact, event)
        elif artifact_type == "CandidateSubgraphArtifact":
            candidate_manifest = self._validate_candidate_artifact(
                projection,
                artifact,
                event,
            )
        elif artifact_type == "MonitorSpecificationArtifact":
            self._validate_monitor_specification_artifact(projection, artifact, event)
        elif artifact_type == "EpistemicPolicyArtifact":
            self._validate_epistemic_policy_artifact(projection, artifact, event)
        elif artifact_type == "AuthorizationPolicyArtifact":
            self._validate_authorization_policy_artifact(projection, artifact, event)
        elif artifact_type == "LogicContractArtifact":
            self._validate_logic_contract_artifact(projection, artifact, event)
        self._validate_sources(artifact, projection.objects, event)
        self._add_objects(projection, {artifact["id"]: _wrapped(artifact_type, artifact)}, event)
        projection.artifact_ids.add(artifact["id"])
        if artifact_type == "GraphBaseArtifact":
            projection.graph_base_id = artifact["id"]
            projection.graph_base_hash = artifact["content_hash"]
            projection.materialization_head = content_digest(
                {"graph_base_artifact_hash": artifact["content_hash"]}
            )
            projection.accepted_graph = self._accepted_graph_base.state_projection()
            projection.accepted_record_metadata = base_record_metadata(
                projection.accepted_graph,
                artifact["base_record_metadata"],
                graph_base_id=artifact["id"],
            )
        elif artifact_type == "CandidateSubgraphArtifact":
            projection.candidate_manifests[artifact["id"]] = candidate_manifest

    def _validate_source_artifact(
        self,
        artifact: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        try:
            expected_hash = source_artifact_digest(
                schema_version=artifact["source_schema_version"],
                artifact_id=artifact["id"],
                artifact_version=artifact["artifact_version"],
                source_content_digest=artifact["source_content_digest"],
                source_byte_length=artifact["source_byte_length"],
                source_media_type=artifact["source_media_type"],
                source_locator=artifact["source_locator"],
            )
        except SourceError as error:
            raise ProtocolError(f"event {event['event_id']}: {error}") from error
        if artifact["artifact_hash"] != expected_hash:
            raise ProtocolError(f"event {event['event_id']}: source artifact semantic hash mismatch")

    def _validate_graph_base_artifact(
        self,
        projection: ProtocolProjection,
        artifact: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        context = f"event {event['event_id']}"
        if projection.graph_base_id is not None:
            raise ProtocolError(f"{context}: graph base is already recorded")
        if projection.accepted_application_ids:
            raise ProtocolError(f"{context}: graph base cannot follow accepted applications")
        if self._accepted_graph_base is None:
            raise ProtocolError(
                f"{context}: GraphBaseArtifact requires an externally supplied graph base"
            )
        expected_ontology = f"sha256:{self._accepted_graph_base.registry.content_hash()}"
        if artifact["graph_ontology_hash"] != expected_ontology:
            raise ProtocolError(f"{context}: graph base ontology hash mismatch")
        if artifact["base_state_digest"] != self._accepted_graph_base.state_digest():
            raise ProtocolError(f"{context}: graph base state digest mismatch")
        try:
            records = parse_graph_base_metadata(artifact["base_record_metadata"])
            metadata = base_record_metadata(
                self._accepted_graph_base,
                artifact["base_record_metadata"],
                graph_base_id=artifact["id"],
            )
            reconstructed = stage_subgraph(
                KnowledgeGraph(self.registry),
                graph_base_operations(self._accepted_graph_base),
            ) if metadata else None
            expected_hash = graph_base_artifact_digest(
                artifact_id=artifact["id"],
                artifact_version=artifact["artifact_version"],
                graph_ontology_hash=artifact["graph_ontology_hash"],
                base_state_digest=artifact["base_state_digest"],
                base_record_metadata=artifact["base_record_metadata"],
            )
        except AcceptedGraphError as error:
            raise ProtocolError(f"{context}: {error}") from error
        if artifact["base_record_count"] != len(records):
            raise ProtocolError(f"{context}: graph base record count mismatch")
        if reconstructed is not None and (
            not reconstructed.valid
            or reconstructed.candidate_state_digest != artifact["base_state_digest"]
        ):
            raise ProtocolError(f"{context}: graph base does not round-trip canonically")
        if artifact["artifact_hash"] != expected_hash:
            raise ProtocolError(f"{context}: graph base semantic hash mismatch")

    def _validate_candidate_artifact(
        self,
        projection: ProtocolProjection,
        artifact: dict[str, Any],
        event: dict[str, Any],
    ) -> tuple[Any, ...]:
        context = f"event {event['event_id']}"
        if projection.graph_base_id is None or projection.accepted_graph is None:
            raise ProtocolError(f"{context}: candidate requires a verified graph base")
        graph_base = self._artifact_ref(
            projection,
            artifact["graph_base_id"],
            artifact["graph_base_hash"],
            "GRAPH_BASE",
            record_type="GraphBaseArtifact",
        )
        if graph_base["id"] != projection.graph_base_id:
            raise ProtocolError(f"{context}: candidate graph base is not active")
        if artifact["graph_ontology_hash"] != graph_base["graph_ontology_hash"]:
            raise ProtocolError(f"{context}: candidate ontology differs from graph base")
        if artifact["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"{context}: candidate has stale base_acceptance_head")
        if artifact["base_materialization_head"] != projection.materialization_head:
            raise ProtocolError(f"{context}: candidate has stale base_materialization_head")
        if artifact["base_state_digest"] != projection.accepted_graph.state_digest():
            raise ProtocolError(f"{context}: candidate has stale base_state_digest")
        self._require_sources(artifact, {graph_base["id"]}, event)
        try:
            expected_hash = candidate_artifact_digest(
                artifact_id=artifact["id"],
                artifact_version=artifact["artifact_version"],
                candidate_schema_version=artifact["candidate_schema_version"],
                graph_base_id=artifact["graph_base_id"],
                graph_base_hash=artifact["graph_base_hash"],
                graph_ontology_hash=artifact["graph_ontology_hash"],
                base_acceptance_head=artifact["base_acceptance_head"],
                base_materialization_head=artifact["base_materialization_head"],
                base_state_digest=artifact["base_state_digest"],
                candidate_manifest=artifact["candidate_manifest"],
                candidate_manifest_hash=artifact["candidate_manifest_hash"],
                candidate_write_count=artifact["candidate_write_count"],
                candidate_digest=artifact["candidate_digest"],
                candidate_state_digest=artifact["candidate_state_digest"],
            )
            manifest = parse_candidate_manifest(artifact["candidate_manifest"])
            validate_temporal_writes(projection.accepted_record_metadata, manifest)
            staged = stage_subgraph(
                projection.accepted_graph,
                [item.operation for item in manifest],
            )
        except (AcceptedGraphError, StagingError) as error:
            raise ProtocolError(f"{context}: {error}") from error
        if artifact["artifact_hash"] != expected_hash:
            raise ProtocolError(f"{context}: candidate semantic hash mismatch")
        if not staged.valid:
            raise ProtocolError(f"{context}: candidate is structurally invalid")
        bindings = {
            "graph_ontology_hash": staged.ontology_hash,
            "base_state_digest": staged.base_state_digest,
            "candidate_digest": staged.candidate_digest,
            "candidate_state_digest": staged.candidate_state_digest,
        }
        for name, expected in bindings.items():
            if artifact[name] != expected:
                raise ProtocolError(f"{context}: candidate {name} mismatch")
        return manifest

    def _validate_monitor_specification_artifact(
        self,
        projection: ProtocolProjection,
        artifact: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        _canonical_unique(
            artifact["input_artifact_ids"],
            f"event {event['event_id']} input_artifact_ids",
        )
        if len(artifact["input_artifact_ids"]) != len(artifact["input_artifact_record_hashes"]):
            raise ProtocolError(
                f"event {event['event_id']}: monitor input artifact fields differ in length"
            )
        if artifact["assessment_kind"] not in {*EPISTEMIC_MONITOR_KINDS, "AUTHORITY"}:
            raise ProtocolError(f"event {event['event_id']}: unsupported monitor assessment kind")
        require_digest(
            artifact["monitor_implementation_hash"],
            f"event {event['event_id']} monitor_implementation_hash",
        )
        for artifact_id, record_hash_value in zip(
            artifact["input_artifact_ids"],
            artifact["input_artifact_record_hashes"],
            strict=True,
        ):
            dependency = self._object(projection.objects, artifact_id, "ProtocolArtifact")
            if dependency["content_hash"] != record_hash_value:
                raise ProtocolError(
                    f"event {event['event_id']}: monitor input artifact hash mismatch"
                )
        self._require_sources(artifact, set(artifact["input_artifact_ids"]), event)
        try:
            expected_hash = monitor_specification_digest(
                schema_version=artifact["monitor_schema_version"],
                monitor_id=artifact["id"],
                monitor_version=artifact["artifact_version"],
                assessment_kind=artifact["assessment_kind"],
                implementation_hash=artifact["monitor_implementation_hash"],
                input_artifact_ids=artifact["input_artifact_ids"],
                input_artifact_record_hashes=artifact["input_artifact_record_hashes"],
            )
        except ControlError as error:
            raise ProtocolError(f"event {event['event_id']}: {error}") from error
        if artifact["artifact_hash"] != expected_hash:
            raise ProtocolError(f"event {event['event_id']}: monitor semantic hash mismatch")

    def _validate_epistemic_policy_artifact(
        self,
        projection: ProtocolProjection,
        artifact: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        try:
            requirements = policy_requirements(artifact)
        except ControlError as error:
            raise ProtocolError(f"event {event['event_id']}: {error}") from error
        ruleset = self._artifact_ref(
            projection,
            artifact["ruleset_id"],
            artifact["ruleset_record_hash"],
            "RULE_SET",
        )
        if artifact["ruleset_artifact_hash"] != ruleset["artifact_hash"]:
            raise ProtocolError(f"event {event['event_id']}: policy ruleset artifact hash mismatch")
        required_sources = {artifact["ruleset_id"]}
        for requirement in requirements:
            monitor = self._artifact_ref(
                projection,
                requirement["monitor_id"],
                requirement["monitor_record_hash"],
                "MONITOR_SPECIFICATION",
                record_type="MonitorSpecificationArtifact",
            )
            if monitor["assessment_kind"] not in EPISTEMIC_MONITOR_KINDS:
                raise ProtocolError(
                    f"event {event['event_id']}: epistemic policy cannot require "
                    f"{monitor['assessment_kind']} monitor"
                )
            required_sources.add(monitor["id"])
        self._require_sources(artifact, required_sources, event)
        try:
            expected_hash = epistemic_policy_digest(
                schema_version=artifact["policy_schema_version"],
                policy_id=artifact["id"],
                policy_version=artifact["artifact_version"],
                ruleset_id=artifact["ruleset_id"],
                ruleset_record_hash=artifact["ruleset_record_hash"],
                ruleset_artifact_hash=artifact["ruleset_artifact_hash"],
                required_monitor_ids=artifact["required_monitor_ids"],
                required_monitor_record_hashes=artifact["required_monitor_record_hashes"],
                violation_verdicts=artifact["violation_verdicts"],
                unknown_verdicts=artifact["unknown_verdicts"],
                control_precedence=artifact["control_precedence"],
            )
        except ControlError as error:
            raise ProtocolError(f"event {event['event_id']}: {error}") from error
        if artifact["artifact_hash"] != expected_hash:
            raise ProtocolError(f"event {event['event_id']}: epistemic policy semantic hash mismatch")

    def _validate_authorization_policy_artifact(
        self,
        projection: ProtocolProjection,
        artifact: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        try:
            requirements = authorization_policy_requirements(artifact)
        except ControlError as error:
            raise ProtocolError(f"event {event['event_id']}: {error}") from error
        required_sources = set()
        for requirement in requirements:
            monitor = self._artifact_ref(
                projection,
                requirement["monitor_id"],
                requirement["monitor_record_hash"],
                "MONITOR_SPECIFICATION",
                record_type="MonitorSpecificationArtifact",
            )
            if monitor["assessment_kind"] != "AUTHORITY":
                raise ProtocolError(
                    f"event {event['event_id']}: authorization policy cannot require "
                    f"{monitor['assessment_kind']} monitor"
                )
            required_sources.add(monitor["id"])
        self._require_sources(artifact, required_sources, event)
        try:
            expected_hash = authorization_policy_digest(
                schema_version=artifact["policy_schema_version"],
                policy_id=artifact["id"],
                policy_version=artifact["artifact_version"],
                required_monitor_ids=artifact["required_monitor_ids"],
                required_monitor_record_hashes=artifact["required_monitor_record_hashes"],
            )
        except ControlError as error:
            raise ProtocolError(f"event {event['event_id']}: {error}") from error
        if artifact["artifact_hash"] != expected_hash:
            raise ProtocolError(
                f"event {event['event_id']}: authorization policy semantic hash mismatch"
            )

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
        self._artifact_ref(
            projection,
            proposal["epistemic_policy_id"],
            proposal["epistemic_policy_hash"],
            "EPISTEMIC_POLICY",
            record_type="EpistemicPolicyArtifact",
        )
        required_sources = {proposal["epistemic_policy_id"]}
        candidate = self._candidate_binding(projection, proposal, event)
        if candidate is not None:
            if candidate["base_acceptance_head"] != proposal["base_acceptance_head"]:
                raise ProtocolError(
                    f"event {event['event_id']}: proposal and candidate base acceptance differ"
                )
            required_sources.add(candidate["id"])
        self._require_sources(proposal, required_sources, event)
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
            if record_type == "Evidence":
                source = self._artifact_ref(
                    projection,
                    record["source_artifact_id"],
                    record["source_artifact_hash"],
                    "SOURCE",
                    record_type="SourceArtifact",
                )
                self._require_sources(record, {source["id"]}, event)
            elif record_type == "EvidenceAssertion":
                self._object(combined, record["claim_version_id"], "ClaimVersion")
                self._object(combined, record["evidence_id"], "Evidence")
            elif record_type == "ClaimVersion":
                self._validate_claim_lineage(combined, record, event)
            elif self.registry.is_subtype_of(record_type, "ActionProposal"):
                policy = self._artifact_ref(
                    projection,
                    record["authorization_policy_id"],
                    record["authorization_policy_hash"],
                    "AUTHORIZATION_POLICY",
                    record_type="AuthorizationPolicyArtifact",
                )
                self._require_sources(record, {policy["id"]}, event)
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
        candidate = self._candidate_binding(projection, proposal, event)
        if projection.proposal_states[proposal["id"]] != ProposalState.PROPOSED:
            raise ProtocolError(f"event {event['event_id']}: proposal is not open for logic check")
        self._same_proposal(check, proposal, event)
        if check["base_acceptance_head"] != proposal["base_acceptance_head"]:
            raise ProtocolError(f"event {event['event_id']}: logic check base mismatch")
        if check["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"event {event['event_id']}: logic check has stale acceptance head")
        if candidate is not None:
            candidate_bindings = {
                "candidate_digest": "candidate_digest",
                "base_state_digest": "base_state_digest",
                "candidate_state_digest": "candidate_state_digest",
                "ontology_hash": "graph_ontology_hash",
            }
            for check_name, candidate_name in candidate_bindings.items():
                if check[check_name] != candidate[candidate_name]:
                    raise ProtocolError(
                        f"event {event['event_id']}: logic check targets a different candidate"
                    )
        check_key = (check["proposal_id"], check["monitor_id"])
        existing_output = projection.monitor_output_ids.get(check_key)
        if existing_output is not None:
            raise ProtocolError(
                f"event {event['event_id']}: logical monitor already produced unavailable output "
                f"'{existing_output}' for proposal '{check['proposal_id']}'"
            )
        existing_check = projection.logic_check_by_monitor_context.get(check_key)
        if existing_check is not None:
            raise ProtocolError(
                f"event {event['event_id']}: logical monitor already produced check "
                f"'{existing_check}' for proposal '{check['proposal_id']}'"
            )

        monitor = self._artifact_ref(
            projection,
            check["monitor_id"],
            check["monitor_hash"],
            "MONITOR_SPECIFICATION",
            record_type="MonitorSpecificationArtifact",
        )
        if check["monitor_version"] != monitor["artifact_version"]:
            raise ProtocolError(f"event {event['event_id']}: monitor_version mismatch")
        if monitor["assessment_kind"] != "LOGICAL":
            raise ProtocolError(f"event {event['event_id']}: logic check requires LOGICAL monitor")
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
        monitor_inputs = dict(zip(
            monitor["input_artifact_ids"],
            monitor["input_artifact_record_hashes"],
            strict=True,
        ))
        if monitor_inputs.get(contract["id"]) != contract["content_hash"]:
            raise ProtocolError(f"event {event['event_id']}: logic contract differs from monitor")
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

        _require_distinct_record_ids([check, *witness_records], event)
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
        projection.logic_check_by_monitor_context[check_key] = check["id"]

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
        self._require_new_monitor_output(projection, assessment, event)
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
        self._index_monitor_output(projection, assessment)

    def _monitor_failure(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        self._require_anchor(projection, event)
        payload = event["payload"]
        failure = self._record("MonitorFailure", payload["failure"], event)
        assessment_type = payload["assessment_type"]
        assessment = self._record(assessment_type, payload["assessment"], event, root="Assessment")
        expected_unavailable_type = (
            "UnavailableAuthorityAssessment"
            if assessment["assessment_kind"] == "AUTHORITY"
            else "UnavailableAssessment"
        )
        if assessment_type != expected_unavailable_type:
            raise ProtocolError(
                f"event {event['event_id']}: MONITOR_FAILED requires "
                f"{expected_unavailable_type}"
            )
        if assessment["assessment_outcome"] != "UNKNOWN":
            raise ProtocolError(f"event {event['event_id']}: failed monitor must produce UNKNOWN")
        if assessment["assessment_kind"] not in {*EPISTEMIC_MONITOR_KINDS, "AUTHORITY"}:
            raise ProtocolError(
                f"event {event['event_id']}: MONITOR_FAILED has unsupported assessment kind"
            )
        if failure["id"] == assessment["id"]:
            raise ProtocolError(
                f"event {event['event_id']}: monitor failure and assessment IDs must differ"
            )
        self._require_new_monitor_output(projection, assessment, event)
        if (
            assessment["assessment_kind"] == "LOGICAL"
            and (assessment["proposal_id"], assessment["monitor_id"])
            in projection.logic_check_by_monitor_context
        ):
            raise ProtocolError(
                f"event {event['event_id']}: completed logical check already exists for monitor"
            )
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
        logic_fields = (
            "logic_contract_id",
            "logic_contract_record_hash",
            "ruleset_id",
            "ruleset_hash",
        )
        if assessment["assessment_kind"] == "LOGICAL":
            for name in logic_fields:
                if (
                    name not in failure
                    or name not in assessment
                    or failure[name] != assessment[name]
                ):
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
        elif any(name in failure or name in assessment for name in logic_fields):
            raise ProtocolError(
                f"event {event['event_id']}: non-logical failure contains logical contract fields"
            )
        authority_fields = (
            "action_proposal_id",
            "action_content_hash",
            "evaluated_actor_id",
            "authority_policy_id",
            "authority_policy_hash",
            "evaluated_authority_grant_id",
            "evaluated_authority_grant_hash",
        )
        if assessment["assessment_kind"] == "AUTHORITY":
            for name in authority_fields:
                if failure.get(name) != assessment.get(name):
                    raise ProtocolError(
                        f"event {event['event_id']}: failure and assessment {name} differ"
                    )
            required_failure_sources.update(
                {failure["action_proposal_id"], failure["authority_policy_id"]}
            )
            required_assessment_sources.update(
                {assessment["action_proposal_id"], assessment["authority_policy_id"]}
            )
            if assessment.get("evaluated_authority_grant_id") is not None:
                required_failure_sources.add(failure["evaluated_authority_grant_id"])
                required_assessment_sources.add(assessment["evaluated_authority_grant_id"])
        elif any(name in failure or name in assessment for name in authority_fields):
            raise ProtocolError(
                f"event {event['event_id']}: non-authority failure contains authority fields"
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
        self._index_monitor_output(projection, assessment)

    def _epistemic(self, projection: ProtocolProjection, event: dict[str, Any]) -> None:
        self._require_anchor(projection, event)
        payload = event["payload"]
        decision = self._record("EpistemicDecision", payload["decision"], event)
        proposal = self._object(projection.objects, decision["proposal_id"], "ProposedSubgraph")
        if projection.proposal_states[proposal["id"]] != ProposalState.PROPOSED:
            raise ProtocolError(f"event {event['event_id']}: proposal is not open")
        self._same_proposal(decision, proposal, event)
        proposal_candidate = self._candidate_binding(projection, proposal, event)
        decision_candidate = self._candidate_binding(projection, decision, event)
        if (proposal_candidate is None) != (decision_candidate is None):
            raise ProtocolError(
                f"event {event['event_id']}: proposal and decision candidate bindings differ"
            )
        if proposal_candidate is not None:
            for name in (
                "candidate_artifact_id",
                "candidate_artifact_hash",
                "candidate_digest",
            ):
                if proposal[name] != decision[name]:
                    raise ProtocolError(
                        f"event {event['event_id']}: decision changes proposal candidate binding"
                    )
        if decision["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"event {event['event_id']}: decision has stale acceptance head")
        if proposal["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"event {event['event_id']}: proposal has stale acceptance head")
        policy = self._artifact_ref(
            projection,
            decision["policy_id"],
            decision["policy_hash"],
            "EPISTEMIC_POLICY",
            record_type="EpistemicPolicyArtifact",
        )
        if (
            policy["id"] != proposal["epistemic_policy_id"]
            or policy["content_hash"] != proposal["epistemic_policy_hash"]
        ):
            raise ProtocolError(f"event {event['event_id']}: decision policy differs from proposal")
        if decision["ruleset_id"] != policy["ruleset_id"]:
            raise ProtocolError(f"event {event['event_id']}: decision ruleset differs from policy")
        if decision["ruleset_hash"] != policy["ruleset_record_hash"]:
            raise ProtocolError(f"event {event['event_id']}: decision ruleset hash differs from policy")
        _unique(decision["assessment_ids"], "assessment_ids")
        _unique(decision["triggered_assessment_ids"], "triggered_assessment_ids")
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
        monitors = {
            requirement["monitor_id"]: self._object(
                projection.objects,
                requirement["monitor_id"],
                "MonitorSpecificationArtifact",
            )
            for requirement in policy_requirements(policy)
        }
        try:
            evaluation = evaluate_epistemic_policy(
                policy,
                monitors,
                assessments,
                proposal_id=proposal["id"],
                proposal_content_hash=proposal["content_hash"],
                base_acceptance_head=projection.acceptance_head,
            )
        except ControlError as error:
            raise ProtocolError(f"event {event['event_id']}: {error}") from error
        if decision["assessment_ids"] != list(evaluation.assessment_ids):
            raise ProtocolError(f"event {event['event_id']}: assessment order differs from policy")
        if decision["triggered_assessment_ids"] != list(evaluation.triggered_assessment_ids):
            raise ProtocolError(f"event {event['event_id']}: triggered assessments differ from policy")
        if decision["policy_evaluation_hash"] != evaluation.evaluation_hash:
            raise ProtocolError(f"event {event['event_id']}: policy evaluation hash mismatch")
        verdict = decision["epistemic_verdict"]
        if verdict != evaluation.verdict:
            raise ProtocolError(
                f"event {event['event_id']}: verdict differs from deterministic policy "
                f"({evaluation.verdict})"
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

        revision_hashes = sorted(
            item["record"]["content_hash"] for item in revisions.values()
        )
        result_acceptance_head = (
            acceptance_result_head(
                previous_acceptance_head=projection.acceptance_head,
                proposal_content_hash=proposal["content_hash"],
                decision_content_hash=decision["content_hash"],
                revision_content_hashes=revision_hashes,
            )
            if verdict == "ACCEPT"
            else projection.acceptance_head
        )
        application = None
        staged = None
        temporal_writes = ()
        if verdict == "ACCEPT" and proposal_candidate is not None:
            application, staged, temporal_writes = self._validate_accepted_application(
                projection,
                proposal,
                decision,
                proposal_candidate,
                assessments,
                payload["application"],
                result_acceptance_head,
                event,
            )
        else:
            if payload["application"] is not None:
                raise ProtocolError(
                    f"event {event['event_id']}: graph application is forbidden for this decision"
                )
            if decision.get("accepted_application_id") is not None:
                raise ProtocolError(
                    f"event {event['event_id']}: decision cites a forbidden graph application"
                )

        transition = self._record("TransitionRecord", payload["transition"], event)
        self._transition(
            transition,
            subject=proposal["id"],
            from_state="PROPOSED",
            to_state=EPISTEMIC_TARGETS[verdict].value,
            trigger=decision["id"],
            event=event,
        )
        new_records = [
            decision,
            transition,
            *(item["record"] for item in requests.values()),
            *(item["record"] for item in revisions.values()),
        ]
        if application is not None:
            new_records.append(application)
        _require_distinct_record_ids(new_records, event)
        introduced = {
            decision["id"]: _wrapped("EpistemicDecision", decision),
            transition["id"]: _wrapped("TransitionRecord", transition),
            **requests,
            **revisions,
        }
        if application is not None:
            introduced[application["id"]] = _wrapped(
                "AcceptedGraphApplication",
                application,
            )
        required_decision_sources = {
            proposal["id"],
            policy["id"],
            policy["ruleset_id"],
            *decision["assessment_ids"],
        }
        if proposal_candidate is not None:
            required_decision_sources.add(proposal_candidate["id"])
        self._require_sources(
            decision,
            required_decision_sources,
            event,
        )
        self._validate_sources(decision, {**projection.objects, **introduced}, event)
        for item in [*requests.values(), *revisions.values()]:
            self._validate_sources(item["record"], {**projection.objects, **introduced}, event)
        self._validate_sources(transition, {**projection.objects, **introduced}, event)
        if application is not None:
            self._validate_sources(application, {**projection.objects, **introduced}, event)
        self._add_objects(projection, introduced, event)
        projection.epistemic_decision_ids.add(decision["id"])
        projection.proposal_states[proposal["id"]] = EPISTEMIC_TARGETS[verdict]
        if application is not None:
            try:
                staged.materialize_into(projection.accepted_graph)
                projection.accepted_graph = projection.accepted_graph.state_projection()
                apply_temporal_writes(
                    projection.accepted_record_metadata,
                    temporal_writes,
                    transaction_time=event["transaction_time"],
                    transaction_sequence=event["sequence"],
                    application_id=application["id"],
                )
            except (AcceptedGraphError, StagingError) as error:
                raise ProtocolError(f"event {event['event_id']}: {error}") from error
            projection.materialization_head = application["result_materialization_head"]
            projection.accepted_application_ids.add(application["id"])
            projection.accepted_application_order.append(application["id"])
            projection.applied_candidate_ids.add(proposal_candidate["id"])
        if verdict == "ACCEPT":
            projection.acceptance_head = result_acceptance_head

    def _validate_accepted_application(
        self,
        projection: ProtocolProjection,
        proposal: dict[str, Any],
        decision: dict[str, Any],
        candidate: dict[str, Any],
        assessments: list[dict[str, Any]],
        value: Any,
        result_acceptance_head: str,
        event: dict[str, Any],
    ) -> tuple[dict[str, Any], Any, tuple[Any, ...]]:
        context = f"event {event['event_id']}"
        if projection.accepted_graph is None or projection.graph_base_id is None:
            raise ProtocolError(f"{context}: accepted graph base is unavailable")
        if not isinstance(value, dict):
            raise ProtocolError(f"{context}: candidate-bound ACCEPT requires one application")
        application = self._record("AcceptedGraphApplication", value, event)
        if decision.get("accepted_application_id") != application["id"]:
            raise ProtocolError(f"{context}: decision application reference mismatch")
        if candidate["id"] in projection.applied_candidate_ids:
            raise ProtocolError(f"{context}: candidate was already applied")
        if application["id"] in projection.accepted_application_ids:
            raise ProtocolError(f"{context}: application was already applied")
        if candidate["base_acceptance_head"] != projection.acceptance_head:
            raise ProtocolError(f"{context}: application candidate has stale acceptance base")
        if candidate["base_materialization_head"] != projection.materialization_head:
            raise ProtocolError(f"{context}: application candidate has stale materialization base")
        if candidate["base_state_digest"] != projection.accepted_graph.state_digest():
            raise ProtocolError(f"{context}: application candidate has stale graph base")
        temporal_writes = projection.candidate_manifests.get(candidate["id"])
        if temporal_writes is None:
            raise ProtocolError(f"{context}: candidate manifest is unavailable")
        try:
            validate_temporal_writes(projection.accepted_record_metadata, temporal_writes)
            staged = stage_subgraph(
                projection.accepted_graph,
                [item.operation for item in temporal_writes],
            )
        except (AcceptedGraphError, StagingError) as error:
            raise ProtocolError(f"{context}: {error}") from error
        if not staged.valid:
            raise ProtocolError(f"{context}: applied candidate is structurally invalid")
        staged_bindings = {
            "graph_ontology_hash": staged.ontology_hash,
            "base_state_digest": staged.base_state_digest,
            "candidate_digest": staged.candidate_digest,
            "candidate_state_digest": staged.candidate_state_digest,
        }
        for name, expected in staged_bindings.items():
            if candidate[name] != expected:
                raise ProtocolError(f"{context}: applied candidate {name} mismatch")
        for assessment in assessments:
            if assessment["assessment_kind"] != "LOGICAL" or assessment["assessment_outcome"] == "UNKNOWN":
                continue
            for check_id in assessment["logic_check_record_ids"]:
                check = self._object(projection.objects, check_id, "LogicCheckRecord")
                exact = {
                    "candidate_digest": candidate["candidate_digest"],
                    "base_state_digest": candidate["base_state_digest"],
                    "candidate_state_digest": candidate["candidate_state_digest"],
                    "ontology_hash": candidate["graph_ontology_hash"],
                }
                if any(check[name] != expected for name, expected in exact.items()):
                    raise ProtocolError(f"{context}: logical check targets a different candidate")
        expected_application = accepted_application_record(
            application_id=application["id"],
            event_id=event["event_id"],
            generated_at=event["transaction_time"],
            actor_id=event["actor_id"],
            role=application["responsible_role"],
            proposal=proposal,
            decision=decision,
            candidate=candidate,
            previous_acceptance_head=projection.acceptance_head,
            result_acceptance_head=result_acceptance_head,
            previous_materialization_head=projection.materialization_head,
        )
        if application != expected_application:
            raise ProtocolError(f"{context}: accepted application binding mismatch")
        return application, staged, temporal_writes

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
        policy = self._artifact_ref(
            projection,
            decision["policy_id"],
            decision["policy_hash"],
            "AUTHORIZATION_POLICY",
            record_type="AuthorizationPolicyArtifact",
        )
        if (
            policy["id"] != action["authorization_policy_id"]
            or policy["content_hash"] != action["authorization_policy_hash"]
        ):
            raise ProtocolError(f"event {event['event_id']}: decision policy differs from action")
        _unique(decision["epistemic_decision_ids"], "epistemic_decision_ids")
        if not decision["epistemic_decision_ids"]:
            raise ProtocolError(f"event {event['event_id']}: action proposal lacks ACCEPT decision")
        for decision_id in decision["epistemic_decision_ids"]:
            if decision_id not in projection.epistemic_decision_ids:
                raise ProtocolError(f"event {event['event_id']}: epistemic decision was not applied")
            epistemic = self._object(projection.objects, decision_id, "EpistemicDecision")
            if epistemic["epistemic_verdict"] != "ACCEPT" or epistemic["proposal_id"] != proposal_id:
                raise ProtocolError(
                    f"event {event['event_id']}: epistemic decision does not accept action proposal"
                )
        _unique(decision["relied_on_claim_version_ids"], "relied_on_claim_version_ids")
        for claim_id in decision["relied_on_claim_version_ids"]:
            claim = self._object(projection.objects, claim_id, "ClaimVersion")
            if projection.current_claim_by_key.get(claim["claim_key"]) != claim_id:
                raise ProtocolError(f"event {event['event_id']}: authorization relies on noncurrent claim")

        assessments = []
        _unique(decision["authority_assessment_ids"], "authority_assessment_ids")
        _unique(decision["triggered_assessment_ids"], "triggered_assessment_ids")
        if not decision["authority_assessment_ids"]:
            raise ProtocolError(f"event {event['event_id']}: authorization requires assessments")
        for assessment_id in decision["authority_assessment_ids"]:
            if assessment_id not in projection.assessment_ids:
                raise ProtocolError(f"event {event['event_id']}: authority assessment was not applied")
            assessment = self._object(projection.objects, assessment_id, "Assessment")
            if assessment["assessment_kind"] != "AUTHORITY":
                raise ProtocolError(
                    f"event {event['event_id']}: authorization cites non-authority assessment"
                )
            assessments.append(assessment)
        monitors = {
            requirement["monitor_id"]: self._object(
                projection.objects,
                requirement["monitor_id"],
                "MonitorSpecificationArtifact",
            )
            for requirement in authorization_policy_requirements(policy)
        }
        try:
            evaluation = evaluate_authorization_policy(
                policy,
                monitors,
                assessments,
                proposal_id=proposal_id,
                proposal_content_hash=proposal["content_hash"],
                action_id=action_id,
                action_content_hash=action["content_hash"],
                evaluated_actor_id=decision["authorized_actor_id"],
                base_acceptance_head=projection.acceptance_head,
            )
        except ControlError as error:
            raise ProtocolError(f"event {event['event_id']}: {error}") from error
        if decision["authority_assessment_ids"] != list(evaluation.assessment_ids):
            raise ProtocolError(
                f"event {event['event_id']}: authority assessment order differs from policy"
            )
        if decision["triggered_assessment_ids"] != list(evaluation.triggered_assessment_ids):
            raise ProtocolError(
                f"event {event['event_id']}: triggered authority assessments differ from policy"
            )
        if decision["policy_evaluation_hash"] != evaluation.evaluation_hash:
            raise ProtocolError(
                f"event {event['event_id']}: authorization policy evaluation hash mismatch"
            )
        verdict = decision["authorization_verdict"]
        if verdict != evaluation.verdict:
            raise ProtocolError(
                f"event {event['event_id']}: verdict differs from deterministic authorization "
                f"policy ({evaluation.verdict})"
            )

        grant_id = decision.get("authority_grant_id")
        grant_hash = decision.get("authority_grant_hash")
        if (grant_id is None) != (grant_hash is None):
            raise ProtocolError(
                f"event {event['event_id']}: authority grant binding must be all-or-none"
            )
        grant = None
        if grant_id is not None:
            grant = self._artifact_ref(
                projection,
                grant_id,
                grant_hash,
                "AUTHORITY_GRANT",
                record_type="AuthorityGrant",
            )
        valid_from = decision.get("authorization_valid_from")
        valid_to = decision.get("authorization_valid_to")
        if verdict == "AUTHORIZE":
            if grant is None or valid_from is None:
                raise ProtocolError(
                    f"event {event['event_id']}: AUTHORIZE requires grant and validity start"
                )
            _valid_interval(valid_from, valid_to, "authorization validity")
            if grant["grantee_actor_id"] != decision["authorized_actor_id"]:
                raise ProtocolError(f"event {event['event_id']}: authority grant actor mismatch")
            if action["action_type"] not in grant["permitted_action_types"]:
                raise ProtocolError(
                    f"event {event['event_id']}: action type is outside authority grant"
                )
            if aware_datetime(valid_from, "authorization valid from") < aware_datetime(
                grant["grant_valid_from"], "grant valid from"
            ):
                raise ProtocolError(
                    f"event {event['event_id']}: authorization begins before its grant"
                )
            grant_end = grant.get("grant_valid_to")
            if grant_end is not None and (
                valid_to is None
                or aware_datetime(valid_to, "authorization valid to")
                > aware_datetime(grant_end, "grant valid to")
            ):
                raise ProtocolError(
                    f"event {event['event_id']}: authorization exceeds its grant"
                )
            for assessment in assessments:
                if (
                    assessment.get("evaluated_authority_grant_id") != grant["id"]
                    or assessment.get("evaluated_authority_grant_hash") != grant["content_hash"]
                ):
                    raise ProtocolError(
                        f"event {event['event_id']}: AUTHORIZE grant differs from assessed grant"
                    )
        else:
            if valid_from is not None or valid_to is not None:
                raise ProtocolError(
                    f"event {event['event_id']}: non-AUTHORIZE decision cannot grant validity"
                )
            if grant is not None:
                eligible_outcome = "VIOLATED" if verdict == "BLOCK" else "UNKNOWN"
                triggered = [
                    assessment
                    for assessment in assessments
                    if assessment["id"] in decision["triggered_assessment_ids"]
                    and assessment["assessment_outcome"] == eligible_outcome
                ]
                if not any(
                    item.get("evaluated_authority_grant_id") == grant["id"]
                    and item.get("evaluated_authority_grant_hash") == grant["content_hash"]
                    for item in triggered
                ):
                    raise ProtocolError(
                        f"event {event['event_id']}: cited grant was not evaluated by a "
                        f"triggering {eligible_outcome} authority assessment"
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
        _require_distinct_record_ids([decision, transition], event)
        introduced = {
            decision["id"]: _wrapped("AuthorizationDecision", decision),
            transition["id"]: _wrapped("TransitionRecord", transition),
        }
        required_sources = {
            action_id,
            policy["id"],
            *decision["epistemic_decision_ids"],
            *decision["relied_on_claim_version_ids"],
            *decision["authority_assessment_ids"],
        }
        if grant is not None:
            required_sources.add(grant["id"])
        self._require_sources(decision, required_sources, event)
        self._require_sources(transition, {decision["id"]}, event)
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
            record_type="MonitorSpecificationArtifact",
        )
        if assessment["monitor_version"] != monitor["artifact_version"]:
            raise ProtocolError(f"event {event['event_id']}: monitor_version mismatch")
        if assessment["assessment_kind"] != monitor["assessment_kind"]:
            raise ProtocolError(f"event {event['event_id']}: assessment kind differs from monitor")
        expected_type = ASSESSMENT_TYPES_BY_KIND[assessment["assessment_kind"]]
        unavailable = assessment_type in {
            "UnavailableAssessment",
            "UnavailableAuthorityAssessment",
        }
        if unavailable:
            if assessment["assessment_outcome"] != "UNKNOWN":
                raise ProtocolError(
                    f"event {event['event_id']}: unavailable assessment must be UNKNOWN"
                )
            if (
                assessment_type == "UnavailableAuthorityAssessment"
                and assessment["assessment_kind"] != "AUTHORITY"
            ):
                raise ProtocolError(
                    f"event {event['event_id']}: UnavailableAuthorityAssessment must be AUTHORITY"
                )
            if assessment_type == "UnavailableAssessment" and assessment["assessment_kind"] == "AUTHORITY":
                raise ProtocolError(
                    f"event {event['event_id']}: AUTHORITY failure requires "
                    "UnavailableAuthorityAssessment"
                )
        elif assessment_type != expected_type:
            raise ProtocolError(
                f"event {event['event_id']}: {assessment['assessment_kind']} monitor requires "
                f"{expected_type}"
            )
        self._require_sources(
            assessment,
            {assessment["proposal_id"], assessment["monitor_id"]},
            event,
        )
        authority_output = assessment_type in {
            "AuthorityAssessment",
            "UnavailableAuthorityAssessment",
        }
        if authority_output:
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
            if assessment["action_content_hash"] != action["content_hash"]:
                raise ProtocolError(
                    f"event {event['event_id']}: authority action_content_hash mismatch"
                )
            if action["id"] not in assessment["input_record_ids"]:
                raise ProtocolError(f"event {event['event_id']}: authority inputs must include action")
            if (
                assessment["authority_policy_id"] != action["authorization_policy_id"]
                or assessment["authority_policy_hash"] != action["authorization_policy_hash"]
            ):
                raise ProtocolError(
                    f"event {event['event_id']}: authority assessment policy differs from action"
                )
            grant_fields = (
                assessment.get("evaluated_authority_grant_id"),
                assessment.get("evaluated_authority_grant_hash"),
            )
            if (grant_fields[0] is None) != (grant_fields[1] is None):
                raise ProtocolError(
                    f"event {event['event_id']}: evaluated authority grant binding must be all-or-none"
                )
            if (
                assessment_type == "AuthorityAssessment"
                and assessment["assessment_outcome"] == "SATISFIED"
                and grant_fields[0] is None
            ):
                raise ProtocolError(
                    f"event {event['event_id']}: SATISFIED authority assessment requires a grant"
                )
            if grant_fields[0] is not None:
                grant = self._artifact_ref(
                    projection,
                    grant_fields[0],
                    grant_fields[1],
                    "AUTHORITY_GRANT",
                    record_type="AuthorityGrant",
                )
                self._require_sources(assessment, {grant["id"]}, event)
                if grant["id"] not in assessment["input_record_ids"]:
                    raise ProtocolError(
                        f"event {event['event_id']}: evaluated grant must be an authority input"
                    )
            if assessment_type == "AuthorityAssessment":
                _canonical_unique(
                    assessment["checked_policy_predicates"],
                    "checked_policy_predicates",
                )
                _canonical_unique(
                    assessment["violated_policy_predicates"],
                    "violated_policy_predicates",
                )
                _nonblank_values(
                    assessment["checked_policy_predicates"],
                    "checked_policy_predicates",
                )
                _nonblank_values(
                    assessment["violated_policy_predicates"],
                    "violated_policy_predicates",
                )
                if not assessment["checked_policy_predicates"]:
                    raise ProtocolError(
                        f"event {event['event_id']}: authority assessment checked no predicates"
                    )
                if not set(assessment["violated_policy_predicates"]).issubset(
                    assessment["checked_policy_predicates"]
                ):
                    raise ProtocolError(
                        f"event {event['event_id']}: violated authority predicates were not checked"
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
            "LogicalAssessment": (
                "logic_contract_id",
                "logic_contract_record_hash",
                "LOGIC_CONTRACT",
            ),
            "AuthorityAssessment": (
                "authority_policy_id",
                "authority_policy_hash",
                "AUTHORIZATION_POLICY",
            ),
            "UnavailableAuthorityAssessment": (
                "authority_policy_id",
                "authority_policy_hash",
                "AUTHORIZATION_POLICY",
            ),
        }
        requirement = artifact_requirements.get(assessment_type)
        if assessment_type == "UnavailableAssessment" and assessment["assessment_kind"] == "LOGICAL":
            requirement = (
                "logic_contract_id",
                "logic_contract_record_hash",
                "LOGIC_CONTRACT",
            )
        if requirement:
            dependency = self._artifact_ref(
                projection,
                assessment[requirement[0]],
                assessment[requirement[1]],
                requirement[2],
            )
            if not authority_output:
                monitor_inputs = dict(zip(
                    monitor["input_artifact_ids"],
                    monitor["input_artifact_record_hashes"],
                    strict=True,
                ))
                if monitor_inputs.get(dependency["id"]) != dependency["content_hash"]:
                    raise ProtocolError(
                        f"event {event['event_id']}: assessment dependency differs from monitor"
                    )
            self._require_sources(assessment, {dependency["id"]}, event)
        if assessment_type == "LogicalAssessment":
            self._validate_logical_assessment(projection, assessment, event)
        elif not unavailable:
            self._validate_completed_assessment(
                proposal,
                assessment_type,
                assessment,
                event,
            )

    @staticmethod
    def _monitor_output_key(assessment: Mapping[str, Any]) -> tuple[str, ...]:
        if assessment["assessment_kind"] == "AUTHORITY":
            return (
                assessment["action_proposal_id"],
                assessment["evaluated_actor_id"],
                assessment["base_acceptance_head"],
                assessment["monitor_id"],
                assessment.get("evaluated_authority_grant_id") or "",
                assessment.get("evaluated_authority_grant_hash") or "",
            )
        return assessment["proposal_id"], assessment["monitor_id"]

    def _require_new_monitor_output(
        self,
        projection: ProtocolProjection,
        assessment: Mapping[str, Any],
        event: Mapping[str, Any],
    ) -> None:
        key = self._monitor_output_key(assessment)
        existing = projection.monitor_output_ids.get(key)
        if existing is not None:
            raise ProtocolError(
                f"event {event['event_id']}: monitor already produced assessment '{existing}' "
                f"for subject '{key[0]}'"
            )

    def _index_monitor_output(
        self,
        projection: ProtocolProjection,
        assessment: Mapping[str, Any],
    ) -> None:
        projection.monitor_output_ids[self._monitor_output_key(assessment)] = assessment["id"]

    def _validate_completed_assessment(
        self,
        proposal: dict[str, Any],
        assessment_type: str,
        assessment: dict[str, Any],
        event: dict[str, Any],
    ) -> None:
        outcome = assessment["assessment_outcome"]
        if outcome not in {"SATISFIED", "VIOLATED"}:
            raise ProtocolError(f"event {event['event_id']}: completed assessment has UNKNOWN outcome")
        if assessment_type == "EvidenceCompletenessAssessment":
            missing = assessment["missing_requirement_ids"]
            _canonical_unique(missing, f"event {event['event_id']} missing_requirement_ids")
            _nonblank_values(missing, f"event {event['event_id']} missing_requirement_ids")
            if outcome == "SATISFIED" and missing:
                raise ProtocolError(
                    f"event {event['event_id']}: SATISFIED evidence assessment has missing requirements"
                )
            if outcome == "VIOLATED" and not missing:
                raise ProtocolError(
                    f"event {event['event_id']}: VIOLATED evidence assessment has no missing requirement"
                )
        elif assessment_type == "ConflictAssessment":
            conflicts = assessment["conflicting_assertion_ids"]
            _canonical_unique(conflicts, f"event {event['event_id']} conflicting_assertion_ids")
            _nonblank_values(conflicts, f"event {event['event_id']} conflicting_assertion_ids")
            if outcome == "SATISFIED" and conflicts:
                raise ProtocolError(
                    f"event {event['event_id']}: SATISFIED conflict assessment names conflicts"
                )
            if outcome == "VIOLATED" and len(conflicts) < 2:
                raise ProtocolError(
                    f"event {event['event_id']}: VIOLATED conflict assessment requires two assertions"
                )
            if not set(conflicts).issubset(proposal["evidence_assertion_ids"]):
                raise ProtocolError(
                    f"event {event['event_id']}: conflict assertion is outside proposal"
                )
            if not set(conflicts).issubset(assessment["input_record_ids"]):
                raise ProtocolError(
                    f"event {event['event_id']}: conflict assertions must be assessment inputs"
                )

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
        if outcome not in {"SATISFIED", "VIOLATED"}:
            raise ProtocolError(f"event {event['event_id']}: completed logic assessment is UNKNOWN")
        required_sources = {
            assessment["proposal_id"],
            assessment["monitor_id"],
            assessment["logic_contract_id"],
            assessment["ruleset_id"],
        }
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
                if (
                    old.get("domain_valid_to") is not None
                    and old["domain_valid_to"] != revision["replaced_valid_to"]
                ):
                    raise ProtocolError(
                        f"event {event['event_id']}: prior claim valid_to disagrees with revision"
                    )
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

    def _candidate_binding(
        self,
        projection: ProtocolProjection,
        record: Mapping[str, Any],
        event: Mapping[str, Any],
    ) -> dict[str, Any] | None:
        names = (
            "candidate_artifact_id",
            "candidate_artifact_hash",
            "candidate_digest",
        )
        present = [name for name in names if record.get(name) is not None]
        if present and len(present) != len(names):
            raise ProtocolError(
                f"event {event['event_id']}: candidate binding must be all-or-none"
            )
        if not present:
            return None
        candidate = self._artifact_ref(
            projection,
            record["candidate_artifact_id"],
            record["candidate_artifact_hash"],
            "CANDIDATE_SUBGRAPH",
            record_type="CandidateSubgraphArtifact",
        )
        if record["candidate_digest"] != candidate["candidate_digest"]:
            raise ProtocolError(f"event {event['event_id']}: candidate digest mismatch")
        return candidate

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
            "SourceArtifact",
            "GraphBaseArtifact",
            "CandidateSubgraphArtifact",
            "MonitorSpecificationArtifact",
            "EpistemicPolicyArtifact",
            "AuthorizationPolicyArtifact",
            "LogicContractArtifact",
            "AuthorityGrant",
            "ProposedSubgraph",
            "ClaimVersion",
            "Evidence",
            "EvidenceAssertion",
            "ActionProposal",
            "Assessment",
            "UnavailableAssessment",
            "UnavailableAuthorityAssessment",
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
            "AcceptedGraphApplication",
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
            "SourceArtifact": "ProtocolArtifact",
            "GraphBaseArtifact": "ProtocolArtifact",
            "CandidateSubgraphArtifact": "ProtocolArtifact",
            "MonitorSpecificationArtifact": "ProtocolArtifact",
            "EpistemicPolicyArtifact": "ProtocolArtifact",
            "AuthorizationPolicyArtifact": "ProtocolArtifact",
            "LogicContractArtifact": "ProtocolArtifact",
            "AuthorityGrant": "ProtocolArtifact",
            "ProposedSubgraph": "ProtocolRecord",
            "ClaimVersion": "ProtocolRecord",
            "Evidence": "ProtocolRecord",
            "EvidenceAssertion": "ProtocolRecord",
            "ActionProposal": "ProtocolRecord",
            "Assessment": "ProtocolRecord",
            "UnavailableAssessment": "Assessment",
            "UnavailableAuthorityAssessment": "UnavailableAssessment",
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
            "AcceptedGraphApplication": "ProtocolRecord",
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
            # The one enum duplicated in Python twice; pinning it here keeps
            # all three copies honest (control.EPISTEMIC_MONITOR_KINDS,
            # ASSESSMENT_TYPES_BY_KIND, and the schema).
            "AssessmentKind": {
                "TYPE",
                "EVIDENCE_COMPLETENESS",
                "CONFLICT",
                "UNCERTAINTY",
                "LOGICAL",
                "TEMPORAL",
                "AUTHORITY",
            },
            "AssessmentOutcome": {"SATISFIED", "VIOLATED", "UNKNOWN"},
            "LogicCheckOutcome": {"SATISFIED", "VIOLATED"},
            "EpistemicVerdict": {"ACCEPT", "REJECT", "DEFER", "CONTEST"},
            "ViolationEpistemicVerdict": {"REJECT", "DEFER", "CONTEST"},
            "UnknownEpistemicVerdict": {"DEFER", "CONTEST"},
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


def _require_distinct_record_ids(
    records: Iterable[Mapping[str, Any]],
    event: Mapping[str, Any],
) -> None:
    identifiers = [record["id"] for record in records]
    if len(identifiers) != len(set(identifiers)):
        raise ProtocolError(f"event {event['event_id']}: introduced record IDs contain duplicates")


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
