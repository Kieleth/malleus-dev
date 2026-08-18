"""Accepted-graph candidate manifests, application bindings, and as-of views."""

from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Mapping, TYPE_CHECKING

from malleus.kg import KnowledgeGraph, OpType
from malleus.ledger import (
    LedgerError,
    aware_datetime,
    canonical_json,
    content_digest,
    require_digest,
    with_content_hash,
)
from malleus.staging import (
    CandidateSubgraph,
    ProposedOperation,
    StagingError,
    stage_subgraph,
)
from malleus.valid_time import (
    BoundaryRelation,
    TemporalRecordState,
    ValidTime,
    ValidTimeError,
    ValidTimeViewState,
    transition_cannot_follow,
)

if TYPE_CHECKING:
    from malleus.assent import ProtocolLedger, ProtocolProjection


GRAPH_BASE_SCHEMA_VERSION = "2"
CANDIDATE_SCHEMA_VERSION = "2"


class AcceptedGraphError(ValueError):
    """An accepted-graph artifact, application, or projection is invalid."""


@dataclass(frozen=True)
class TemporalWrite:
    """One structural write with precision-aware valid-time boundaries."""

    operation: ProposedOperation
    valid_from: ValidTime
    valid_to: ValidTime | None = None
    supersedes_record_id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.operation, ProposedOperation):
            raise TypeError("operation must be a ProposedOperation")
        start = _stored_valid_time(self.valid_from, "valid_from")
        object.__setattr__(self, "valid_from", start)
        if self.valid_to is not None:
            end = _stored_valid_time(self.valid_to, "valid_to")
            object.__setattr__(self, "valid_to", end)
            if transition_cannot_follow(start, end):
                raise AcceptedGraphError("valid_to contradicts valid_from ordering")
        if self.supersedes_record_id is not None:
            _text(self.supersedes_record_id, "supersedes_record_id")
            if self.supersedes_record_id == self.operation.record_id:
                raise AcceptedGraphError("a temporal write cannot supersede itself")

    def as_dict(self) -> dict[str, Any]:
        return {
            "operation": self.operation.as_dict(),
            "valid_from": self.valid_from.as_dict(),
            "valid_to": self.valid_to.as_dict() if self.valid_to is not None else None,
            "supersedes_record_id": self.supersedes_record_id,
        }


@dataclass(frozen=True)
class IndeterminateTransition:
    """One unresolved boundary and the extracted reason it cannot be resolved."""

    prior_record_id: str | None
    replacement_record_id: str | None
    reason_code: str
    reason: str
    earliest_possible: str | None
    latest_possible: str | None
    valid_time: ValidTime

    def as_dict(self) -> dict[str, Any]:
        return {
            "prior_record_id": self.prior_record_id,
            "replacement_record_id": self.replacement_record_id,
            "reason_code": self.reason_code,
            "reason": self.reason,
            "earliest_possible": self.earliest_possible,
            "latest_possible": self.latest_possible,
            "valid_time": self.valid_time.as_dict(),
        }


@dataclass(frozen=True, init=False)
class AcceptedGraphView:
    """Defensive accepted-graph projection at one transaction and valid time."""

    _graph: KnowledgeGraph
    protocol_head_hash: str
    event_count: int
    acceptance_head: str
    materialization_head: str
    accepted_history_state_digest: str
    visible_graph_digest: str
    valid_time_resolution_digest: str
    valid_time_state: str
    transaction_as_of: str
    transaction_sequence: int
    valid_as_of: str
    application_ids: tuple[str, ...]
    indeterminate_transitions: tuple[IndeterminateTransition, ...]
    _record_states: dict[str, str]

    def __init__(
        self,
        *,
        graph: KnowledgeGraph,
        protocol_head_hash: str,
        event_count: int,
        acceptance_head: str,
        materialization_head: str,
        accepted_history_state_digest: str,
        visible_graph_digest: str,
        valid_time_resolution_digest: str,
        valid_time_state: str,
        transaction_as_of: str,
        transaction_sequence: int,
        valid_as_of: str,
        application_ids: Iterable[str],
        record_states: Mapping[str, str],
        indeterminate_transitions: Iterable[IndeterminateTransition],
    ) -> None:
        object.__setattr__(self, "_graph", graph.state_projection())
        object.__setattr__(self, "protocol_head_hash", protocol_head_hash)
        object.__setattr__(self, "event_count", event_count)
        object.__setattr__(self, "acceptance_head", acceptance_head)
        object.__setattr__(self, "materialization_head", materialization_head)
        object.__setattr__(self, "accepted_history_state_digest", accepted_history_state_digest)
        object.__setattr__(self, "visible_graph_digest", visible_graph_digest)
        object.__setattr__(self, "valid_time_resolution_digest", valid_time_resolution_digest)
        object.__setattr__(self, "valid_time_state", valid_time_state)
        object.__setattr__(self, "transaction_as_of", transaction_as_of)
        object.__setattr__(self, "transaction_sequence", transaction_sequence)
        object.__setattr__(self, "valid_as_of", valid_as_of)
        object.__setattr__(self, "application_ids", tuple(application_ids))
        object.__setattr__(self, "_record_states", dict(record_states))
        object.__setattr__(
            self,
            "indeterminate_transitions",
            tuple(indeterminate_transitions),
        )

    @property
    def graph(self) -> KnowledgeGraph:
        if self.valid_time_state == ValidTimeViewState.INDETERMINATE.value:
            raise AcceptedGraphError(
                "valid-time view is indeterminate; inspect indeterminate_transitions "
                "and use definite_graph"
            )
        return self._graph.state_projection()

    @property
    def definite_graph(self) -> KnowledgeGraph:
        return self._graph.state_projection()

    @property
    def record_states(self) -> dict[str, str]:
        return dict(self._record_states)


@dataclass(frozen=True)
class _VisibleProjection:
    graph: KnowledgeGraph
    record_states: dict[str, str]
    indeterminate_transitions: tuple[IndeterminateTransition, ...]
    resolution_digest: str
    state: ValidTimeViewState


class AcceptedGraphProjector:
    """Rebuild accepted graph views from a fully verified protocol ledger."""

    def __init__(self, ledger: "ProtocolLedger") -> None:
        from malleus.assent import ProtocolLedger

        if not isinstance(ledger, ProtocolLedger):
            raise TypeError("ledger must be a ProtocolLedger")
        self._ledger = ledger

    def current(self, *, valid_as_of: str) -> AcceptedGraphView:
        valid = _canonical_time(valid_as_of, "valid_as_of")
        projection = self._ledger.replay()
        transaction_time = projection.events[-1]["transaction_time"]
        return self._view(projection, transaction_time, projection.event_count, valid)

    def as_of(
        self,
        *,
        transaction_as_of: str,
        valid_as_of: str,
        transaction_sequence: int | None = None,
    ) -> AcceptedGraphView:
        transaction = _canonical_time(transaction_as_of, "transaction_as_of")
        valid = _canonical_time(valid_as_of, "valid_as_of")
        if transaction_sequence is not None and (
            not isinstance(transaction_sequence, int)
            or isinstance(transaction_sequence, bool)
            or transaction_sequence < 1
        ):
            raise AcceptedGraphError("transaction_sequence must be a positive integer")
        events = self._ledger._read_events()
        self._ledger._replay_events(events)
        cutoff = _time(transaction, "transaction_as_of")
        prefix = [
            event
            for event in events
            if _time(event["transaction_time"], "event transaction_time") < cutoff
            or (
                _time(event["transaction_time"], "event transaction_time") == cutoff
                and (transaction_sequence is None or event["sequence"] <= transaction_sequence)
            )
        ]
        if not prefix:
            raise AcceptedGraphError("transaction cutoff precedes the ledger anchor")
        projection = self._ledger._replay_events(prefix)
        return self._view(projection, transaction, prefix[-1]["sequence"], valid)

    def _view(
        self,
        projection: "ProtocolProjection",
        transaction_as_of: str,
        transaction_sequence: int,
        valid_as_of: str,
    ) -> AcceptedGraphView:
        if projection.graph_base_id is None or projection.accepted_graph is None:
            raise AcceptedGraphError("verified graph base is unavailable at this transaction prefix")
        visible = _visible_projection(
            projection.accepted_graph.registry,
            projection.accepted_record_metadata,
            valid_as_of=valid_as_of,
        )
        return AcceptedGraphView(
            graph=visible.graph,
            protocol_head_hash=projection.head_hash,
            event_count=projection.event_count,
            acceptance_head=projection.acceptance_head,
            materialization_head=projection.materialization_head,
            accepted_history_state_digest=projection.accepted_graph.state_digest(),
            visible_graph_digest=visible.graph.state_digest(),
            valid_time_resolution_digest=visible.resolution_digest,
            valid_time_state=visible.state.value,
            transaction_as_of=transaction_as_of,
            transaction_sequence=transaction_sequence,
            valid_as_of=valid_as_of,
            application_ids=projection.accepted_application_order,
            record_states=visible.record_states,
            indeterminate_transitions=visible.indeterminate_transitions,
        )


def temporal_write(
    operation: ProposedOperation,
    *,
    valid_from: ValidTime | Mapping[str, Any],
    valid_to: ValidTime | Mapping[str, Any] | None = None,
    supersedes_record_id: str | None = None,
) -> TemporalWrite:
    return TemporalWrite(operation, valid_from, valid_to, supersedes_record_id)


def candidate_manifest(writes: Iterable[TemporalWrite]) -> str:
    values = tuple(writes)
    if not values:
        raise AcceptedGraphError("candidate manifest requires at least one temporal write")
    if any(not isinstance(item, TemporalWrite) for item in values):
        raise TypeError("candidate manifest values must be TemporalWrite instances")
    identifiers = [item.operation.record_id for item in values]
    if len(identifiers) != len(set(identifiers)):
        raise AcceptedGraphError("candidate manifest record IDs must be unique")
    return canonical_json({
        "schema_version": CANDIDATE_SCHEMA_VERSION,
        "writes": [item.as_dict() for item in values],
    })


def parse_candidate_manifest(value: Any) -> tuple[TemporalWrite, ...]:
    parsed = _canonical_object(value, "candidate_manifest")
    _exact(parsed, {"schema_version", "writes"}, "candidate_manifest")
    if parsed["schema_version"] != CANDIDATE_SCHEMA_VERSION:
        raise AcceptedGraphError(
            f"unsupported candidate manifest schema '{parsed['schema_version']}'"
        )
    if not isinstance(parsed["writes"], list) or not parsed["writes"]:
        raise AcceptedGraphError("candidate manifest writes must be a nonempty list")
    result = []
    for index, item in enumerate(parsed["writes"]):
        context = f"candidate manifest write {index}"
        if not isinstance(item, dict):
            raise AcceptedGraphError(f"{context} must be an object")
        _exact(
            item,
            {"operation", "valid_from", "valid_to", "supersedes_record_id"},
            context,
        )
        operation = _operation(item["operation"], context)
        result.append(TemporalWrite(
            operation,
            item["valid_from"],
            item["valid_to"],
            item["supersedes_record_id"],
        ))
    identifiers = [item.operation.record_id for item in result]
    if len(identifiers) != len(set(identifiers)):
        raise AcceptedGraphError("candidate manifest record IDs must be unique")
    return tuple(result)


def candidate_manifest_hash(manifest: str) -> str:
    return _candidate_manifest_hash(manifest)


def _candidate_manifest_hash(manifest: str) -> str:
    writes = parse_candidate_manifest(manifest)
    return content_digest({
        "schema_version": CANDIDATE_SCHEMA_VERSION,
        "writes": [item.as_dict() for item in writes],
    })


def graph_base_metadata(
    graph: KnowledgeGraph,
    intervals: Iterable[Mapping[str, Any]],
) -> str:
    if not isinstance(graph, KnowledgeGraph):
        raise TypeError("graph must be a KnowledgeGraph")
    values = []
    for index, item in enumerate(intervals):
        if not isinstance(item, Mapping):
            raise AcceptedGraphError(f"base interval {index} must be an object")
        value = dict(item)
        _exact(
            value,
            {"record_id", "valid_from", "valid_to", "supersedes_record_id"},
            f"base interval {index}",
        )
        _text(value["record_id"], f"base interval {index} record_id")
        if value["supersedes_record_id"] is not None:
            _text(
                value["supersedes_record_id"],
                f"base interval {index} supersedes_record_id",
            )
        start = _stored_valid_time(
            value["valid_from"],
            f"base interval {index} valid_from",
        )
        value["valid_from"] = start.as_dict()
        if value["valid_to"] is not None:
            end = _stored_valid_time(
                value["valid_to"],
                f"base interval {index} valid_to",
            )
            value["valid_to"] = end.as_dict()
            if transition_cannot_follow(start, end):
                raise AcceptedGraphError(f"base interval {index} ordering is contradictory")
        values.append(value)
    values.sort(key=lambda item: item["record_id"])
    identifiers = [item["record_id"] for item in values]
    if identifiers != sorted(set(identifiers)):
        raise AcceptedGraphError("base interval record IDs must be unique")
    expected = sorted(_graph_operations(graph))
    if identifiers != expected:
        raise AcceptedGraphError("base intervals must exactly cover graph records")
    _validate_base_lineage(_graph_operations(graph), values)
    return canonical_json({
        "schema_version": GRAPH_BASE_SCHEMA_VERSION,
        "records": values,
    })


def parse_graph_base_metadata(value: Any) -> tuple[dict[str, Any], ...]:
    parsed = _canonical_object(value, "base_record_metadata")
    _exact(parsed, {"schema_version", "records"}, "base_record_metadata")
    if parsed["schema_version"] != GRAPH_BASE_SCHEMA_VERSION:
        raise AcceptedGraphError(
            f"unsupported graph base schema '{parsed['schema_version']}'"
        )
    if not isinstance(parsed["records"], list):
        raise AcceptedGraphError("base_record_metadata records must be a list")
    result = []
    for index, item in enumerate(parsed["records"]):
        if not isinstance(item, dict):
            raise AcceptedGraphError(f"base record {index} must be an object")
        _exact(
            item,
            {"record_id", "valid_from", "valid_to", "supersedes_record_id"},
            f"base record {index}",
        )
        _text(item["record_id"], f"base record {index} record_id")
        if item["supersedes_record_id"] is not None:
            _text(
                item["supersedes_record_id"],
                f"base record {index} supersedes_record_id",
            )
        start = _stored_valid_time(
            item["valid_from"],
            f"base record {index} valid_from",
        )
        if item["valid_to"] is not None:
            end = _stored_valid_time(
                item["valid_to"],
                f"base record {index} valid_to",
            )
            if transition_cannot_follow(start, end):
                raise AcceptedGraphError(
                    f"base record {index} interval ordering is contradictory"
                )
        else:
            end = None
        result.append({
            **item,
            "valid_from": start.as_dict(),
            "valid_to": end.as_dict() if end is not None else None,
        })
    identifiers = [item["record_id"] for item in result]
    if identifiers != sorted(set(identifiers)):
        raise AcceptedGraphError("base record metadata must be canonical and unique")
    return tuple(result)


def graph_base_artifact_digest(
    *,
    artifact_id: str,
    artifact_version: str,
    graph_ontology_hash: str,
    base_state_digest: str,
    base_record_metadata: str,
) -> str:
    _text(artifact_id, "artifact_id")
    _text(artifact_version, "artifact_version")
    _digest(graph_ontology_hash, "graph_ontology_hash")
    _digest(base_state_digest, "base_state_digest")
    records = parse_graph_base_metadata(base_record_metadata)
    return content_digest({
        "schema_version": GRAPH_BASE_SCHEMA_VERSION,
        "artifact_id": artifact_id,
        "artifact_version": artifact_version,
        "graph_ontology_hash": graph_ontology_hash,
        "base_state_digest": base_state_digest,
        "base_records": records,
    })


def graph_base_operations(graph: KnowledgeGraph) -> tuple[ProposedOperation, ...]:
    """Return a canonical structural reconstruction sequence for a graph base."""
    operations = _graph_operations(graph)
    return tuple(operations[record_id] for record_id in _base_operation_order(graph))


def candidate_artifact_fields(
    graph: KnowledgeGraph,
    writes: Iterable[TemporalWrite],
    *,
    graph_base_id: str,
    graph_base_hash: str,
    base_acceptance_head: str,
    base_materialization_head: str,
) -> tuple[dict[str, Any], CandidateSubgraph]:
    if not isinstance(graph, KnowledgeGraph):
        raise TypeError("graph must be a KnowledgeGraph")
    temporal_writes = tuple(writes)
    manifest = candidate_manifest(temporal_writes)
    candidate = stage_subgraph(graph, [item.operation for item in temporal_writes])
    if not candidate.valid:
        raise AcceptedGraphError(f"candidate is structurally invalid: {candidate.rejection_reason}")
    fields = {
        "candidate_schema_version": CANDIDATE_SCHEMA_VERSION,
        "graph_base_id": graph_base_id,
        "graph_base_hash": graph_base_hash,
        "graph_ontology_hash": candidate.ontology_hash,
        "base_acceptance_head": base_acceptance_head,
        "base_materialization_head": base_materialization_head,
        "base_state_digest": candidate.base_state_digest,
        "candidate_manifest": manifest,
        "candidate_manifest_hash": candidate_manifest_hash(manifest),
        "candidate_write_count": len(temporal_writes),
        "candidate_digest": candidate.candidate_digest,
        "candidate_state_digest": candidate.candidate_state_digest,
    }
    return fields, candidate


def candidate_artifact_digest(
    *,
    artifact_id: str,
    artifact_version: str,
    candidate_schema_version: str,
    graph_base_id: str,
    graph_base_hash: str,
    graph_ontology_hash: str,
    base_acceptance_head: str,
    base_materialization_head: str,
    base_state_digest: str,
    candidate_manifest: str,
    candidate_manifest_hash: str,
    candidate_write_count: int,
    candidate_digest: str,
    candidate_state_digest: str,
) -> str:
    if candidate_schema_version != CANDIDATE_SCHEMA_VERSION:
        raise AcceptedGraphError(
            f"unsupported candidate schema '{candidate_schema_version}'"
        )
    for name, value in (
        ("artifact_id", artifact_id),
        ("artifact_version", artifact_version),
        ("graph_base_id", graph_base_id),
    ):
        _text(value, name)
    for name, value in (
        ("graph_base_hash", graph_base_hash),
        ("graph_ontology_hash", graph_ontology_hash),
        ("base_acceptance_head", base_acceptance_head),
        ("base_materialization_head", base_materialization_head),
        ("base_state_digest", base_state_digest),
        ("candidate_manifest_hash", candidate_manifest_hash),
        ("candidate_digest", candidate_digest),
        ("candidate_state_digest", candidate_state_digest),
    ):
        _digest(value, name)
    if not isinstance(candidate_write_count, int) or isinstance(candidate_write_count, bool):
        raise AcceptedGraphError("candidate_write_count must be an integer")
    writes = parse_candidate_manifest(candidate_manifest)
    if candidate_write_count != len(writes):
        raise AcceptedGraphError("candidate_write_count differs from manifest")
    if candidate_manifest_hash != _candidate_manifest_hash(candidate_manifest):
        raise AcceptedGraphError("candidate_manifest_hash mismatch")
    return content_digest({
        "schema_version": candidate_schema_version,
        "artifact_id": artifact_id,
        "artifact_version": artifact_version,
        "graph_base_id": graph_base_id,
        "graph_base_hash": graph_base_hash,
        "graph_ontology_hash": graph_ontology_hash,
        "base_acceptance_head": base_acceptance_head,
        "base_materialization_head": base_materialization_head,
        "base_state_digest": base_state_digest,
        "candidate_manifest_hash": candidate_manifest_hash,
        "candidate_write_count": candidate_write_count,
        "candidate_digest": candidate_digest,
        "candidate_state_digest": candidate_state_digest,
        "writes": [item.as_dict() for item in writes],
    })


def acceptance_result_head(
    *,
    previous_acceptance_head: str,
    proposal_content_hash: str,
    decision_content_hash: str,
    revision_content_hashes: Iterable[str],
) -> str:
    hashes = sorted(revision_content_hashes)
    for index, value in enumerate(hashes):
        _digest(value, f"revision_content_hashes[{index}]")
    return content_digest({
        "previous_acceptance_head": previous_acceptance_head,
        "proposal_content_hash": proposal_content_hash,
        "decision_content_hash": decision_content_hash,
        "revision_content_hashes": hashes,
    })


def materialization_result_head(
    *,
    previous_materialization_head: str,
    proposal_content_hash: str,
    decision_content_hash: str,
    candidate_artifact_hash: str,
    candidate_digest: str,
    candidate_state_digest: str,
) -> str:
    return content_digest({
        "previous_materialization_head": previous_materialization_head,
        "proposal_content_hash": proposal_content_hash,
        "decision_content_hash": decision_content_hash,
        "candidate_artifact_hash": candidate_artifact_hash,
        "candidate_digest": candidate_digest,
        "candidate_state_digest": candidate_state_digest,
    })


def accepted_application_record(
    *,
    application_id: str,
    event_id: str,
    generated_at: str,
    actor_id: str,
    role: str,
    proposal: Mapping[str, Any],
    decision: Mapping[str, Any],
    candidate: Mapping[str, Any],
    previous_acceptance_head: str,
    result_acceptance_head: str,
    previous_materialization_head: str,
) -> dict[str, Any]:
    result_materialization_head = materialization_result_head(
        previous_materialization_head=previous_materialization_head,
        proposal_content_hash=proposal["content_hash"],
        decision_content_hash=decision["content_hash"],
        candidate_artifact_hash=candidate["content_hash"],
        candidate_digest=candidate["candidate_digest"],
        candidate_state_digest=candidate["candidate_state_digest"],
    )
    writes = parse_candidate_manifest(candidate["candidate_manifest"])
    return with_content_hash(
        "AcceptedGraphApplication",
        {
            "id": application_id,
            "generation_event_id": event_id,
            "generated_at": generated_at,
            "responsible_actor_id": actor_id,
            "responsible_role": role,
            "source_record_ids": sorted({
                proposal["id"],
                decision["id"],
                candidate["id"],
                candidate["graph_base_id"],
            }),
            "proposal_id": proposal["id"],
            "proposal_content_hash": proposal["content_hash"],
            "epistemic_decision_id": decision["id"],
            "epistemic_decision_hash": decision["content_hash"],
            "candidate_artifact_id": candidate["id"],
            "candidate_artifact_hash": candidate["content_hash"],
            "candidate_digest": candidate["candidate_digest"],
            "candidate_manifest_hash": candidate["candidate_manifest_hash"],
            "graph_ontology_hash": candidate["graph_ontology_hash"],
            "previous_acceptance_head": previous_acceptance_head,
            "result_acceptance_head": result_acceptance_head,
            "previous_materialization_head": previous_materialization_head,
            "result_materialization_head": result_materialization_head,
            "base_state_digest": candidate["base_state_digest"],
            "candidate_state_digest": candidate["candidate_state_digest"],
            "applied_record_ids": [item.operation.record_id for item in writes],
        },
    )


def validate_temporal_writes(
    metadata: Mapping[str, Mapping[str, Any]],
    writes: Iterable[TemporalWrite],
) -> None:
    working = deepcopy(dict(metadata))
    for index, temporal in enumerate(writes):
        operation = temporal.operation
        if operation.record_id in working:
            raise AcceptedGraphError(
                f"candidate write {index} record ID '{operation.record_id}' already exists"
            )
        supersedes = temporal.supersedes_record_id
        if supersedes is not None:
            if supersedes not in working:
                raise AcceptedGraphError(
                    f"candidate write {index} supersedes unknown record '{supersedes}'"
                )
            prior = working[supersedes]
            if prior.get("superseded_by") is not None:
                raise AcceptedGraphError(
                    f"candidate write {index} forks superseded record '{supersedes}'"
                )
            prior_operation = _operation(prior["operation"], "accepted metadata operation")
            if (
                prior_operation.op_type != operation.op_type
                or prior_operation.record_type != operation.record_type
            ):
                raise AcceptedGraphError(
                    f"candidate write {index} supersession type differs from prior record"
                )
            prior_start = _stored_valid_time(prior["valid_from"], "prior valid_from")
            replacement_start = temporal.valid_from
            if transition_cannot_follow(prior_start, replacement_start):
                raise AcceptedGraphError(
                    f"candidate write {index} replacement contradicts prior ordering"
                )
            prior_end = prior.get("valid_to")
            if (
                prior_end is not None
                and _stored_valid_time(prior_end, "prior valid_to") != replacement_start
            ):
                raise AcceptedGraphError(
                    f"candidate write {index} replacement disagrees with prior valid_to"
                )
            prior["valid_to"] = temporal.valid_from.as_dict()
            prior["superseded_by"] = operation.record_id
        working[operation.record_id] = {
            "operation": operation.as_dict(),
            "valid_from": temporal.valid_from.as_dict(),
            "valid_to": temporal.valid_to.as_dict() if temporal.valid_to is not None else None,
            "supersedes_record_id": supersedes,
            "superseded_by": None,
        }


def apply_temporal_writes(
    metadata: dict[str, dict[str, Any]],
    writes: Iterable[TemporalWrite],
    *,
    transaction_time: str,
    transaction_sequence: int,
    application_id: str,
) -> None:
    values = tuple(writes)
    validate_temporal_writes(metadata, values)
    for index, temporal in enumerate(values):
        supersedes = temporal.supersedes_record_id
        if supersedes is not None:
            metadata[supersedes]["valid_to"] = temporal.valid_from.as_dict()
            metadata[supersedes]["superseded_by"] = temporal.operation.record_id
        metadata[temporal.operation.record_id] = {
            "operation": temporal.operation.as_dict(),
            "valid_from": temporal.valid_from.as_dict(),
            "valid_to": temporal.valid_to.as_dict() if temporal.valid_to is not None else None,
            "supersedes_record_id": supersedes,
            "superseded_by": None,
            "transaction_time": transaction_time,
            "transaction_sequence": transaction_sequence,
            "application_id": application_id,
            "order": (transaction_sequence, index),
        }


def _validate_base_lineage(
    operations: Mapping[str, ProposedOperation],
    intervals: list[Mapping[str, Any]],
) -> None:
    by_id = {item["record_id"]: item for item in intervals}
    children = set()
    for index, item in enumerate(intervals):
        prior_id = item["supersedes_record_id"]
        if prior_id is None:
            continue
        if prior_id == item["record_id"]:
            raise AcceptedGraphError(f"base interval {index} cannot supersede itself")
        if prior_id not in by_id:
            raise AcceptedGraphError(
                f"base interval {index} supersedes unknown record '{prior_id}'"
            )
        if prior_id in children:
            raise AcceptedGraphError(f"base supersession forks record '{prior_id}'")
        children.add(prior_id)
        prior_operation = operations[prior_id]
        operation = operations[item["record_id"]]
        if (
            prior_operation.op_type != operation.op_type
            or prior_operation.record_type != operation.record_type
        ):
            raise AcceptedGraphError(
                f"base interval {index} supersession type differs from prior record"
            )
        prior = by_id[prior_id]
        if prior["valid_to"] != item["valid_from"]:
            raise AcceptedGraphError(
                f"base interval {index} must begin at the prior valid_to"
            )
        if transition_cannot_follow(
            _stored_valid_time(prior["valid_from"], "base prior valid_from"),
            _stored_valid_time(item["valid_from"], "base replacement valid_from"),
        ):
            raise AcceptedGraphError(
                f"base interval {index} replacement contradicts prior ordering"
            )


def base_record_metadata(
    graph: KnowledgeGraph,
    metadata_json: str,
    *,
    graph_base_id: str,
) -> dict[str, dict[str, Any]]:
    intervals = parse_graph_base_metadata(metadata_json)
    operations = _graph_operations(graph)
    if sorted(operations) != [item["record_id"] for item in intervals]:
        raise AcceptedGraphError("base record metadata does not cover the supplied graph")
    interval_by_id = {item["record_id"]: item for item in intervals}
    _validate_base_lineage(operations, list(intervals))
    superseded_by = {
        item["supersedes_record_id"]: item["record_id"]
        for item in intervals
        if item["supersedes_record_id"] is not None
    }
    result = {}
    for order, record_id in enumerate(_base_operation_order(graph)):
        interval = interval_by_id[record_id]
        result[record_id] = {
            "operation": operations[record_id].as_dict(),
            "valid_from": interval["valid_from"],
            "valid_to": interval["valid_to"],
            "supersedes_record_id": interval["supersedes_record_id"],
            "superseded_by": superseded_by.get(record_id),
            "transaction_time": None,
            "transaction_sequence": 0,
            "application_id": graph_base_id,
            "order": (0, order),
        }
    return result


def visible_graph(
    registry: Any,
    metadata: Mapping[str, Mapping[str, Any]],
    *,
    valid_as_of: str,
) -> KnowledgeGraph:
    projection = _visible_projection(registry, metadata, valid_as_of=valid_as_of)
    if projection.state is ValidTimeViewState.INDETERMINATE:
        raise AcceptedGraphError(
            "valid-time projection is indeterminate; use AcceptedGraphProjector "
            "to inspect its reasons"
        )
    return projection.graph.state_projection()


def _visible_projection(
    registry: Any,
    metadata: Mapping[str, Mapping[str, Any]],
    *,
    valid_as_of: str,
) -> _VisibleProjection:
    point = _time(valid_as_of, "valid_as_of")
    states: dict[str, TemporalRecordState] = {}
    transitions: dict[str, IndeterminateTransition] = {}
    selected = []
    for record_id, item in metadata.items():
        start = _stored_valid_time(item["valid_from"], f"record {record_id} valid_from")
        end = (
            _stored_valid_time(item["valid_to"], f"record {record_id} valid_to")
            if item.get("valid_to") is not None
            else None
        )
        state = _record_state(start, end, point)
        states[record_id] = state
        if state is TemporalRecordState.DEFINITELY_PRESENT:
            selected.append(item)
        _add_indeterminate_transition(
            transitions,
            start,
            point,
            prior_record_id=item.get("supersedes_record_id"),
            replacement_record_id=record_id,
        )
        if end is not None:
            _add_indeterminate_transition(
                transitions,
                end,
                point,
                prior_record_id=record_id,
                replacement_record_id=item.get("superseded_by"),
            )
    selected.sort(key=lambda item: item["order"])
    graph = KnowledgeGraph(registry)
    if selected:
        candidate = stage_subgraph(
            graph,
            [_operation(item["operation"], "accepted metadata operation") for item in selected],
        )
        if not candidate.valid:
            raise AcceptedGraphError(
                "valid-time projection is structurally incomplete: "
                f"{candidate.rejection_reason}"
            )
        candidate.materialize_into(graph)
    result_graph = graph.state_projection()
    ordered_transitions = tuple(
        transitions[key] for key in sorted(transitions)
    )
    view_state = (
        ValidTimeViewState.INDETERMINATE
        if any(state is TemporalRecordState.INDETERMINATE for state in states.values())
        else ValidTimeViewState.DETERMINATE
    )
    record_states = {
        record_id: states[record_id].value for record_id in sorted(states)
    }
    resolution_digest = content_digest({
        "valid_as_of": valid_as_of,
        "valid_time_state": view_state.value,
        "definite_graph_digest": result_graph.state_digest(),
        "record_states": record_states,
        "indeterminate_transitions": [
            item.as_dict() for item in ordered_transitions
        ],
    })
    return _VisibleProjection(
        result_graph,
        record_states,
        ordered_transitions,
        resolution_digest,
        view_state,
    )


def _record_state(
    start: ValidTime,
    end: ValidTime | None,
    point: datetime,
) -> TemporalRecordState:
    start_relation = start.relation_at(point)
    end_relation = end.relation_at(point) if end is not None else BoundaryRelation.BEFORE
    if start_relation is BoundaryRelation.BEFORE or end_relation is BoundaryRelation.AFTER:
        return TemporalRecordState.DEFINITELY_ABSENT
    if start_relation is BoundaryRelation.AFTER and end_relation is BoundaryRelation.BEFORE:
        return TemporalRecordState.DEFINITELY_PRESENT
    return TemporalRecordState.INDETERMINATE


def _add_indeterminate_transition(
    transitions: dict[str, IndeterminateTransition],
    boundary: ValidTime,
    point: datetime,
    *,
    prior_record_id: str | None,
    replacement_record_id: str | None,
) -> None:
    if boundary.relation_at(point) is not BoundaryRelation.INDETERMINATE:
        return
    reason_code = boundary.reason_code
    reason = boundary.indeterminacy_reason
    if reason_code is None or reason is None:
        raise AcceptedGraphError("indeterminate valid time lacks its canonical reason")
    earliest, latest = boundary.display_bounds()
    item = IndeterminateTransition(
        prior_record_id,
        replacement_record_id,
        reason_code,
        reason,
        earliest,
        latest,
        boundary,
    )
    transitions[canonical_json(item.as_dict())] = item


def _graph_operations(graph: KnowledgeGraph) -> dict[str, ProposedOperation]:
    result = {}
    constructors = {
        "ENTITY": ProposedOperation.entity,
        "SIGNAL": ProposedOperation.signal,
        "EVENT": ProposedOperation.event,
    }
    for item in graph.canonical_operations():
        kind = item["kind"]
        if kind == "RELATION":
            operation = ProposedOperation.relation(
                item["record_type"],
                item["record_id"],
                item["source_id"],
                item["target_id"],
                item["properties"],
            )
        else:
            try:
                constructor = constructors[kind]
            except KeyError as error:
                raise AcceptedGraphError(
                    f"base record '{item['record_id']}' has unknown category '{kind}'"
                ) from error
            operation = constructor(
                item["record_type"],
                item["record_id"],
                item["properties"],
            )
        result[item["record_id"]] = operation
    return result


def _base_operation_order(graph: KnowledgeGraph) -> list[str]:
    operations = _graph_operations(graph)
    categories = {
        OpType.CREATE_ENTITY: 0,
        OpType.CREATE_EVENT: 0,
        OpType.CREATE_RELATION: 1,
        OpType.CREATE_SIGNAL: 2,
    }
    return sorted(operations, key=lambda key: (categories[operations[key].op_type], key))


def _operation(value: Any, context: str) -> ProposedOperation:
    if not isinstance(value, dict):
        raise AcceptedGraphError(f"{context} operation must be an object")
    _exact(
        value,
        {"op_type", "record_type", "record_id", "properties", "source_id", "target_id"},
        f"{context} operation",
    )
    try:
        return ProposedOperation(
            value["op_type"],
            value["record_type"],
            value["record_id"],
            value["properties"],
            value["source_id"],
            value["target_id"],
        )
    except (StagingError, TypeError) as error:
        raise AcceptedGraphError(f"{context} operation is invalid: {error}") from error


def _canonical_object(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, str):
        raise AcceptedGraphError(f"{context} must be canonical JSON text")
    try:
        parsed = json.loads(
            value,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_nonfinite,
        )
    except (json.JSONDecodeError, AcceptedGraphError) as error:
        raise AcceptedGraphError(f"{context} is invalid JSON: {error}") from error
    if not isinstance(parsed, dict):
        raise AcceptedGraphError(f"{context} must encode an object")
    if canonical_json(parsed) != value:
        raise AcceptedGraphError(f"{context} must use canonical JSON encoding")
    return parsed


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise AcceptedGraphError(f"duplicate JSON key '{key}'")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> None:
    raise AcceptedGraphError(f"nonfinite JSON number '{value}' is not allowed")


def _exact(value: Mapping[str, Any], expected: set[str], context: str) -> None:
    missing = sorted(expected - set(value))
    unknown = sorted(set(value) - expected)
    if missing:
        raise AcceptedGraphError(f"{context} missing fields: {', '.join(missing)}")
    if unknown:
        raise AcceptedGraphError(f"{context} unknown fields: {', '.join(unknown)}")


def _text(value: Any, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise AcceptedGraphError(f"{name} must be a nonblank string")


def _digest(value: Any, name: str) -> None:
    try:
        require_digest(value, name)
    except LedgerError as error:
        raise AcceptedGraphError(str(error)) from error


def _time(value: Any, name: str) -> datetime:
    try:
        return aware_datetime(value, name)
    except LedgerError as error:
        raise AcceptedGraphError(str(error)) from error


def _stored_valid_time(value: Any, name: str) -> ValidTime:
    try:
        return ValidTime.from_value(value, name)
    except ValidTimeError as error:
        raise AcceptedGraphError(str(error)) from error


def _canonical_time(value: Any, name: str) -> str:
    parsed = _time(value, name)
    return parsed.isoformat()
