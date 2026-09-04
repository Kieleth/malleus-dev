"""Atomic proposed-subgraph staging over an isolated graph overlay."""

from __future__ import annotations

from copy import deepcopy
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from malleus.kg import KnowledgeGraph, Operation, OpStatus, OpType
from malleus.ledger import LedgerError, canonical_json, content_digest


class StagingError(ValueError):
    """A candidate cannot be staged or safely materialized."""


class StaleCandidateError(StagingError):
    """The materialized graph changed after the candidate was staged."""


@dataclass(frozen=True, init=False)
class ProposedOperation:
    """One immutable proposed graph operation."""

    op_type: OpType
    record_type: str
    record_id: str
    _properties_json: str
    source_id: str | None = None
    target_id: str | None = None

    def __init__(
        self,
        op_type: OpType,
        record_type: str,
        record_id: str,
        properties: Any = None,
        source_id: str | None = None,
        target_id: str | None = None,
    ):
        try:
            op_type = op_type if isinstance(op_type, OpType) else OpType(op_type)
        except (TypeError, ValueError) as error:
            raise StagingError(f"Unsupported proposed operation type: {op_type!r}") from error
        _require_nonblank(record_type, "record_type")
        _require_nonblank(record_id, "record_id")
        if op_type != OpType.CREATE_RELATION and (
            source_id is not None or target_id is not None
        ):
            raise StagingError("Only relation proposals may declare source_id or target_id")
        if op_type == OpType.CREATE_RELATION:
            _require_nonblank(source_id, "source_id")
            _require_nonblank(target_id, "target_id")
        _require_string_keys(properties, "properties")
        try:
            properties_json = canonical_json(properties)
        except LedgerError as error:
            raise StagingError(f"Proposed operation properties are invalid: {error}") from error
        object.__setattr__(self, "op_type", op_type)
        object.__setattr__(self, "record_type", record_type)
        object.__setattr__(self, "record_id", record_id)
        object.__setattr__(self, "_properties_json", properties_json)
        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "target_id", target_id)

    @property
    def properties(self) -> Any:
        return json.loads(self._properties_json)

    @classmethod
    def entity(
        cls,
        record_type: str,
        record_id: str,
        properties: Mapping[str, Any] | None = None,
    ) -> "ProposedOperation":
        return cls(OpType.CREATE_ENTITY, record_type, record_id, properties)

    @classmethod
    def relation(
        cls,
        record_type: str,
        record_id: str,
        source_id: str,
        target_id: str,
        properties: Mapping[str, Any] | None = None,
    ) -> "ProposedOperation":
        return cls(
            OpType.CREATE_RELATION,
            record_type,
            record_id,
            properties,
            source_id,
            target_id,
        )

    @classmethod
    def signal(
        cls,
        record_type: str,
        record_id: str,
        properties: Mapping[str, Any] | None = None,
    ) -> "ProposedOperation":
        return cls(OpType.CREATE_SIGNAL, record_type, record_id, properties)

    @classmethod
    def event(
        cls,
        record_type: str,
        record_id: str,
        properties: Mapping[str, Any] | None = None,
    ) -> "ProposedOperation":
        return cls(OpType.CREATE_EVENT, record_type, record_id, properties)

    @classmethod
    def event_participation(
        cls,
        record_type: str,
        record_id: str,
        properties: Mapping[str, Any] | None = None,
    ) -> "ProposedOperation":
        return cls(
            OpType.CREATE_EVENT_PARTICIPATION,
            record_type,
            record_id,
            properties,
        )

    def copy(self) -> "ProposedOperation":
        return ProposedOperation(
            self.op_type,
            self.record_type,
            self.record_id,
            self.properties,
            self.source_id,
            self.target_id,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "op_type": self.op_type.value,
            "record_type": self.record_type,
            "record_id": self.record_id,
            "properties": self.properties,
            "source_id": self.source_id,
            "target_id": self.target_id,
        }


class CandidateSubgraph:
    """A staged batch whose overlay never aliases the materialized graph."""

    def __init__(
        self,
        *,
        ontology_hash: str,
        base_state_digest: str,
        candidate_digest: str,
        candidate_state_digest: str | None,
        writes: tuple[ProposedOperation, ...],
        operations: tuple[Operation, ...],
        overlay: KnowledgeGraph | None,
        turn: int,
    ):
        self._ontology_hash = ontology_hash
        self._base_state_digest = base_state_digest
        self._candidate_digest = candidate_digest
        self._candidate_state_digest = candidate_state_digest
        self._writes = tuple(write.copy() for write in writes)
        self._operations = tuple(deepcopy(operations))
        self._overlay = overlay.fork() if overlay is not None else None
        self._turn = turn

    @property
    def valid(self) -> bool:
        return self._overlay is not None

    @property
    def ontology_hash(self) -> str:
        return self._ontology_hash

    @property
    def base_state_digest(self) -> str:
        return self._base_state_digest

    @property
    def candidate_digest(self) -> str:
        return self._candidate_digest

    @property
    def candidate_state_digest(self) -> str | None:
        return self._candidate_state_digest

    @property
    def writes(self) -> tuple[ProposedOperation, ...]:
        return tuple(write.copy() for write in self._writes)

    @property
    def operations(self) -> tuple[Operation, ...]:
        return deepcopy(self._operations)

    @property
    def rejection_reason(self) -> str | None:
        reasons = [
            operation.rejection_reason
            for operation in self._operations
            if operation.op_status == OpStatus.REJECTED and operation.rejection_reason
        ]
        return "; ".join(reasons) if reasons else None

    def overlay(self) -> KnowledgeGraph:
        if self._overlay is None:
            raise StagingError("Rejected candidate has no usable overlay")
        return self._overlay.fork()

    def materialize_into(self, graph: KnowledgeGraph) -> tuple[Operation, ...]:
        """Rebuild on a fresh clone and swap only after the whole batch succeeds."""
        if not isinstance(graph, KnowledgeGraph):
            raise TypeError("Materialization target must be a KnowledgeGraph")
        if not self.valid:
            raise StagingError("Rejected candidate cannot be materialized")
        ontology_hash = f"sha256:{graph.registry.content_hash()}"
        if ontology_hash != self._ontology_hash:
            raise StagingError("Candidate and materialization target use different ontologies")
        if graph.state_digest() != self._base_state_digest:
            raise StaleCandidateError("Materialized graph changed after candidate staging")

        replacement = graph.fork()
        replacement.set_turn(self._turn)
        start = len(replacement.operations)
        for write in self._writes:
            operation = _apply(replacement, write)
            if operation.op_status != OpStatus.COMMITTED:
                raise StagingError(
                    "Candidate failed revalidation before materialization: "
                    f"{operation.rejection_reason}"
                )
        if replacement.state_digest() != self._candidate_state_digest:
            raise StagingError("Rebuilt candidate state does not match staged state")

        committed = tuple(replacement.operations[start:])
        graph._replace_materialized_state(replacement)
        return deepcopy(committed)


def stage_subgraph(
    graph: KnowledgeGraph,
    writes: Sequence[ProposedOperation],
    *,
    turn: int | None = None,
) -> CandidateSubgraph:
    """Validate an ordered proposed subgraph without mutating the base graph."""
    if not isinstance(graph, KnowledgeGraph):
        raise TypeError("Staging base must be a KnowledgeGraph")
    if isinstance(writes, (str, bytes)) or not isinstance(writes, Sequence):
        raise TypeError("writes must be a sequence of ProposedOperation values")
    proposed = tuple(writes)
    if not proposed:
        raise StagingError("A proposed subgraph must contain at least one operation")
    for index, write in enumerate(proposed):
        if not isinstance(write, ProposedOperation):
            raise TypeError(f"writes[{index}] must be a ProposedOperation")
    if turn is not None and (
        not isinstance(turn, int) or isinstance(turn, bool) or turn < 0
    ):
        raise TypeError("turn must be a nonnegative integer")

    base_digest = graph.state_digest()
    working = graph.fork()
    candidate_turn = graph.current_turn if turn is None else turn
    working.set_turn(candidate_turn)
    outcomes = []
    valid = True
    for write in proposed:
        operation = _apply(working, write)
        if operation.op_status == OpStatus.COMMITTED:
            operation = Operation(
                turn=operation.turn,
                op_type=operation.op_type,
                op_status=OpStatus.STAGED,
                entity_type=operation.entity_type,
                data=deepcopy(operation.data),
                timestamp=operation.timestamp,
            )
        else:
            valid = False
        outcomes.append(operation)

    ontology_hash = f"sha256:{graph.registry.content_hash()}"
    candidate_digest = content_digest({
        "ontology_hash": ontology_hash,
        "base_state_digest": base_digest,
        "writes": [write.as_dict() for write in proposed],
    })
    return CandidateSubgraph(
        ontology_hash=ontology_hash,
        base_state_digest=base_digest,
        candidate_digest=candidate_digest,
        candidate_state_digest=working.state_digest() if valid else None,
        writes=proposed,
        operations=tuple(outcomes),
        overlay=working if valid else None,
        turn=candidate_turn,
    )


def _apply(graph: KnowledgeGraph, write: ProposedOperation) -> Operation:
    properties = deepcopy(write.properties)
    if write.op_type == OpType.CREATE_ENTITY:
        return graph.create_entity(write.record_type, write.record_id, properties)
    if write.op_type == OpType.CREATE_RELATION:
        return graph.create_relation(
            write.record_type,
            write.record_id,
            write.source_id,
            write.target_id,
            properties,
        )
    if write.op_type == OpType.CREATE_SIGNAL:
        return graph.create_signal(write.record_type, write.record_id, properties)
    if write.op_type == OpType.CREATE_EVENT:
        return graph.create_event(write.record_type, write.record_id, properties)
    if write.op_type == OpType.CREATE_EVENT_PARTICIPATION:
        return graph.create_event_participation(
            write.record_type, write.record_id, properties
        )
    raise StagingError(f"Unsupported proposed operation type: {write.op_type}")


def _require_string_keys(value: Any, path: str) -> None:
    if isinstance(value, Mapping):
        for key, member in value.items():
            if not isinstance(key, str):
                raise StagingError(f"{path} object keys must be strings")
            _require_string_keys(member, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, member in enumerate(value):
            _require_string_keys(member, f"{path}[{index}]")


def _require_nonblank(value: Any, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise StagingError(f"{name} must be a nonblank string")
