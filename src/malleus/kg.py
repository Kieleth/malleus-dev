"""Knowledge Graph: ontology-typed, write-time validated, operation-logged.

The KG takes an OntologyRegistry as its constructor parameter.
Every write is validated against the type system before commitment.
All operations are logged for audit trail and Prolog extraction.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import networkx as nx

from malleus.ontology import OntologyRegistry


class OpType(str, Enum):
    CREATE_ENTITY = "CREATE_ENTITY"
    CREATE_RELATION = "CREATE_RELATION"
    CREATE_SIGNAL = "CREATE_SIGNAL"
    CREATE_EVENT = "CREATE_EVENT"


class OpStatus(str, Enum):
    COMMITTED = "COMMITTED"
    REJECTED = "REJECTED"


@dataclass
class Operation:
    """A single KG operation with its validation outcome."""
    turn: int
    op_type: OpType
    op_status: OpStatus
    entity_type: str
    data: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    rejection_reason: str | None = None


@dataclass
class ValidationResult:
    """Result of validating a proposed write."""
    valid: bool
    error: str | None = None


class KnowledgeGraph:
    """Ontology-typed Knowledge Graph backed by NetworkX.

    The ontology is the constructor parameter. The KG cannot be
    instantiated without it. Every write is validated as a precondition.
    """

    def __init__(self, registry: OntologyRegistry):
        self._registry = registry
        self._graph = nx.MultiDiGraph()  # MultiDiGraph: supports multiple edges between same pair
        self._operations: list[Operation] = []
        self._current_turn: int = 0

    @property
    def registry(self) -> OntologyRegistry:
        return self._registry

    @property
    def operations(self) -> list[Operation]:
        return list(self._operations)

    @property
    def node_count(self) -> int:
        return self._graph.number_of_nodes()

    @property
    def edge_count(self) -> int:
        return self._graph.number_of_edges()

    def set_turn(self, turn: int):
        self._current_turn = turn

    # --- Validation ---

    def _validate_entity(self, entity_type: str, entity_id: str, properties: dict) -> ValidationResult:
        if not self._registry.has_type(entity_type):
            return ValidationResult(False, f"Unknown entity type: '{entity_type}'")
        if not self._registry.is_subtype_of(entity_type, "Entity"):
            return ValidationResult(False, f"'{entity_type}' is not an Entity subtype")
        if entity_id in self._graph:
            return ValidationResult(False, f"Entity '{entity_id}' already exists")

        for slot_name, value in properties.items():
            error = self._registry.validate_enum_field(entity_type, slot_name, value)
            if error:
                return ValidationResult(False, error)

        return self._check_required_slots(entity_type, properties)

    def _validate_relation(
        self, relation_type: str, relation_id: str, source_id: str, target_id: str,
        properties: dict,
    ) -> ValidationResult:
        if not self._registry.has_type(relation_type):
            return ValidationResult(False, f"Unknown relation type: '{relation_type}'")
        if not self._registry.is_subtype_of(relation_type, "Relation"):
            return ValidationResult(False, f"'{relation_type}' is not a Relation subtype")
        if source_id not in self._graph:
            return ValidationResult(False, f"Source entity '{source_id}' does not exist")
        if target_id not in self._graph:
            return ValidationResult(False, f"Target entity '{target_id}' does not exist")

        rel_type_value = properties.get("relation_type")
        if rel_type_value:
            error = self._registry.validate_enum_field(relation_type, "relation_type", rel_type_value)
            if error:
                return ValidationResult(False, error)

        for slot_name, value in properties.items():
            if slot_name == "relation_type":
                continue
            error = self._registry.validate_enum_field(relation_type, slot_name, value)
            if error:
                return ValidationResult(False, error)

        strength = properties.get("strength")
        if strength is not None:
            if not isinstance(strength, (int, float)) or not (0.0 <= float(strength) <= 1.0):
                return ValidationResult(False, f"Strength must be 0.0-1.0, got {strength}")

        return ValidationResult(True)

    def _validate_signal(self, signal_type_class: str, properties: dict) -> ValidationResult:
        if not self._registry.has_type(signal_type_class):
            return ValidationResult(False, f"Unknown signal type class: '{signal_type_class}'")
        if not self._registry.is_subtype_of(signal_type_class, "Signal"):
            return ValidationResult(False, f"'{signal_type_class}' is not a Signal subtype")

        bearer_id = properties.get("bearer_id")
        if not bearer_id:
            return ValidationResult(False, "Signal requires bearer_id (dependent continuant)")
        if bearer_id not in self._graph:
            return ValidationResult(False, f"Bearer entity '{bearer_id}' does not exist")

        signal_type_value = properties.get("signal_type")
        if signal_type_value:
            error = self._registry.validate_enum_field(signal_type_class, "signal_type", signal_type_value)
            if error:
                return ValidationResult(False, error)

        return ValidationResult(True)

    def _validate_event(self, event_type_class: str, properties: dict) -> ValidationResult:
        if not self._registry.has_type(event_type_class):
            return ValidationResult(False, f"Unknown event type class: '{event_type_class}'")
        if not self._registry.is_subtype_of(event_type_class, "Event"):
            return ValidationResult(False, f"'{event_type_class}' is not an Event subtype")

        event_type_value = properties.get("event_type")
        if event_type_value:
            error = self._registry.validate_enum_field(event_type_class, "event_type", event_type_value)
            if error:
                return ValidationResult(False, error)

        return ValidationResult(True)

    def _check_required_slots(self, type_name: str, properties: dict) -> ValidationResult:
        """Check required slots walking up the inheritance chain."""
        current = type_name
        while current is not None:
            typedef = self._registry._types.get(current)
            if typedef:
                for slot_name, constraint in typedef.slot_usage.items():
                    if constraint.required and slot_name not in properties:
                        return ValidationResult(False, f"Required slot '{slot_name}' missing for {type_name}")
            current = self._registry._inheritance.get(current)
        return ValidationResult(True)

    # --- Write operations ---

    def create_entity(self, entity_type: str, entity_id: str, properties: dict | None = None) -> Operation:
        """Create a typed entity. Validates against ontology before committing."""
        props = properties or {}
        result = self._validate_entity(entity_type, entity_id, props)

        if not result.valid:
            op = Operation(
                turn=self._current_turn,
                op_type=OpType.CREATE_ENTITY,
                op_status=OpStatus.REJECTED,
                entity_type=entity_type,
                data={"id": entity_id, **props},
                rejection_reason=result.error,
            )
            self._operations.append(op)
            return op

        self._graph.add_node(entity_id, type=entity_type, **props)
        op = Operation(
            turn=self._current_turn,
            op_type=OpType.CREATE_ENTITY,
            op_status=OpStatus.COMMITTED,
            entity_type=entity_type,
            data={"id": entity_id, **props},
        )
        self._operations.append(op)
        return op

    def create_relation(
        self, relation_type: str, relation_id: str,
        source_id: str, target_id: str,
        properties: dict | None = None,
    ) -> Operation:
        """Create a typed relation. Validates against ontology before committing."""
        props = properties or {}
        result = self._validate_relation(relation_type, relation_id, source_id, target_id, props)

        if not result.valid:
            op = Operation(
                turn=self._current_turn,
                op_type=OpType.CREATE_RELATION,
                op_status=OpStatus.REJECTED,
                entity_type=relation_type,
                data={"id": relation_id, "source_id": source_id, "target_id": target_id, **props},
                rejection_reason=result.error,
            )
            self._operations.append(op)
            return op

        self._graph.add_edge(
            source_id, target_id,
            key=relation_id, type=relation_type, **props,
        )
        op = Operation(
            turn=self._current_turn,
            op_type=OpType.CREATE_RELATION,
            op_status=OpStatus.COMMITTED,
            entity_type=relation_type,
            data={"id": relation_id, "source_id": source_id, "target_id": target_id, **props},
        )
        self._operations.append(op)
        return op

    def create_signal(self, signal_type_class: str, signal_id: str, properties: dict | None = None) -> Operation:
        """Create a typed signal. Validates against ontology before committing."""
        props = properties or {}
        result = self._validate_signal(signal_type_class, props)

        status = OpStatus.COMMITTED if result.valid else OpStatus.REJECTED
        op = Operation(
            turn=self._current_turn,
            op_type=OpType.CREATE_SIGNAL,
            op_status=status,
            entity_type=signal_type_class,
            data={"id": signal_id, **props},
            rejection_reason=result.error if not result.valid else None,
        )
        self._operations.append(op)

        if result.valid:
            self._graph.add_node(signal_id, type=signal_type_class, is_signal=True, **props)

        return op

    def create_event(self, event_type_class: str, event_id: str, properties: dict | None = None) -> Operation:
        """Create a typed event. Validates against ontology before committing."""
        props = properties or {}
        result = self._validate_event(event_type_class, props)

        status = OpStatus.COMMITTED if result.valid else OpStatus.REJECTED
        op = Operation(
            turn=self._current_turn,
            op_type=OpType.CREATE_EVENT,
            op_status=status,
            entity_type=event_type_class,
            data={"id": event_id, **props},
            rejection_reason=result.error if not result.valid else None,
        )
        self._operations.append(op)

        if result.valid:
            self._graph.add_node(event_id, type=event_type_class, is_event=True, **props)

        return op

    # --- Read operations ---

    def query(self, entity_type: str | None = None, **filters) -> list[dict]:
        """Query entities/relations matching type and filter criteria."""
        results = []
        for node_id, data in self._graph.nodes(data=True):
            if entity_type and data.get("type") != entity_type:
                if entity_type and not self._registry.is_subtype_of(data.get("type", ""), entity_type):
                    continue
            if all(data.get(k) == v for k, v in filters.items()):
                results.append({"id": node_id, **data})
        return results

    def query_relations(self, relation_type: str | None = None, source_id: str | None = None, target_id: str | None = None) -> list[dict]:
        """Query relations matching type and/or endpoints."""
        results = []
        for u, v, key, data in self._graph.edges(data=True, keys=True):
            if relation_type and data.get("type") != relation_type:
                continue
            if source_id and u != source_id:
                continue
            if target_id and v != target_id:
                continue
            results.append({"source_id": u, "target_id": v, "key": key, **data})
        return results

    def get_node(self, node_id: str) -> dict | None:
        if node_id not in self._graph:
            return None
        return {"id": node_id, **self._graph.nodes[node_id]}

    def has_node(self, node_id: str) -> bool:
        return node_id in self._graph

    # --- Audit ---

    def committed_operations(self, turn: int | None = None) -> list[Operation]:
        ops = [op for op in self._operations if op.op_status == OpStatus.COMMITTED]
        if turn is not None:
            ops = [op for op in ops if op.turn == turn]
        return ops

    def rejected_operations(self, turn: int | None = None) -> list[Operation]:
        ops = [op for op in self._operations if op.op_status == OpStatus.REJECTED]
        if turn is not None:
            ops = [op for op in ops if op.turn == turn]
        return ops

    def rejection_rate(self, turn: int | None = None) -> float:
        if turn is not None:
            ops = [op for op in self._operations if op.turn == turn]
        else:
            ops = self._operations
        if not ops:
            return 0.0
        rejected = sum(1 for op in ops if op.op_status == OpStatus.REJECTED)
        return rejected / len(ops)
