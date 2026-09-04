"""Ontology-typed graph with strict pre-materialization validation."""

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import networkx as nx

from malleus.ledger import content_digest
from malleus.ontology import OntologyRegistry


class OpType(str, Enum):
    CREATE_ENTITY = "CREATE_ENTITY"
    CREATE_RELATION = "CREATE_RELATION"
    CREATE_SIGNAL = "CREATE_SIGNAL"
    CREATE_EVENT = "CREATE_EVENT"
    CREATE_EVENT_PARTICIPATION = "CREATE_EVENT_PARTICIPATION"


class OpStatus(str, Enum):
    STAGED = "STAGED"
    COMMITTED = "COMMITTED"
    REJECTED = "REJECTED"


# Family order is replay order: event participation and relations need their
# endpoints, and a signal needs its bearer already materialized.
RECORD_FAMILIES: tuple[tuple[str, str], ...] = (
    ("entities", "ENTITY"),
    ("events", "EVENT"),
    ("event_participations", "EVENT_PARTICIPATION"),
    ("relations", "RELATION"),
    ("signals", "SIGNAL"),
)


@dataclass
class Operation:
    """A structurally validated graph operation and its materialization result."""

    turn: int
    op_type: OpType
    op_status: OpStatus
    entity_type: str
    data: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    rejection_reason: str | None = None


@dataclass
class ValidationResult:
    """Result of validating one proposed graph write."""

    valid: bool
    error: str | None = None


class KnowledgeGraph:
    """A NetworkX projection that rejects structurally invalid writes."""

    def __init__(self, registry: OntologyRegistry):
        self._registry = registry
        self._graph = nx.MultiDiGraph()
        self._operations: list[Operation] = []
        self._identifiers: dict[str, tuple[str, str]] = {}
        self._current_turn = 0

    @property
    def registry(self) -> OntologyRegistry:
        return self._registry

    @property
    def operations(self) -> list[Operation]:
        return deepcopy(self._operations)

    @property
    def node_count(self) -> int:
        return self._graph.number_of_nodes()

    @property
    def edge_count(self) -> int:
        return self._graph.number_of_edges()

    @property
    def current_turn(self) -> int:
        return self._current_turn

    def snapshot(self) -> dict[str, Any]:
        """Return a defensive, canonicalizable view of materialized graph state."""
        nodes = [
            deepcopy({"id": node_id, **data})
            for node_id, data in self._graph.nodes(data=True)
        ]
        relations = [
            deepcopy({"source_id": source, "target_id": target, "key": key, **data})
            for source, target, key, data in self._graph.edges(data=True, keys=True)
        ]
        nodes.sort(key=lambda node: node["id"])
        relations.sort(key=lambda relation: relation["key"])
        return {
            "ontology_hash": f"sha256:{self._registry.content_hash()}",
            "nodes": nodes,
            "relations": relations,
        }

    def state_digest(self) -> str:
        """Hash materialized graph state, excluding the operation audit log."""
        return content_digest(self.snapshot())

    def fork(self) -> "KnowledgeGraph":
        """Return an isolated graph copy suitable for candidate evaluation."""
        copy = KnowledgeGraph(self._registry)
        copy._graph = deepcopy(self._graph)
        copy._operations = deepcopy(self._operations)
        copy._identifiers = deepcopy(self._identifiers)
        copy._current_turn = self._current_turn
        return copy

    def state_projection(self) -> "KnowledgeGraph":
        """Return materialized graph state without the local operation audit."""
        projection = KnowledgeGraph(self._registry)
        projection._graph = deepcopy(self._graph)
        projection._identifiers = deepcopy(self._identifiers)
        return projection

    def canonical_operations(self) -> tuple[dict[str, Any], ...]:
        """Export exact materialized records with explicit graph categories."""
        operations = []
        relations = {
            key: (source, target, data)
            for source, target, key, data in self._graph.edges(data=True, keys=True)
        }
        for record_id, (kind, record_type) in self._identifiers.items():
            if kind == "RELATION":
                source_id, target_id, data = relations[record_id]
                properties = {
                    key: deepcopy(value)
                    for key, value in data.items()
                    if key != "type"
                }
            else:
                data = self._graph.nodes[record_id]
                properties = {
                    key: deepcopy(value)
                    for key, value in data.items()
                    if key not in {
                        "type",
                        "is_signal",
                        "is_event",
                        "is_event_participation",
                    }
                }
                source_id = None
                target_id = None
            operations.append({
                "kind": kind,
                "record_type": record_type,
                "record_id": record_id,
                "properties": properties,
                "source_id": source_id,
                "target_id": target_id,
            })
        operations.sort(key=lambda item: item["record_id"])
        return tuple(operations)

    def export_records(self) -> dict[str, list[dict[str, Any]]]:
        """Export materialized state as records that replay through from_records.

        Structural state only. The operation audit log is deliberately not
        exported: refusals and their reasons are execution-local diagnostics,
        not transferable state (docs/DELIMITATIONS.md, "Deliberate boundaries").
        Every record carries exactly the arguments of its create_* call.
        """
        export: dict[str, list[dict[str, Any]]] = {family: [] for family, _ in RECORD_FAMILIES}
        families = {kind: family for family, kind in RECORD_FAMILIES}
        for record in self.canonical_operations():
            kind = record["kind"]
            endpoints = (
                {"source_id": record["source_id"], "target_id": record["target_id"]}
                if kind == "RELATION"
                else {}
            )
            export[families[kind]].append({
                "type": record["record_type"],
                "id": record["record_id"],
                **endpoints,
                "properties": record["properties"],
            })
        return export

    @classmethod
    def from_records(
        cls,
        registry: OntologyRegistry,
        records: dict[str, list[dict[str, Any]]],
    ) -> "KnowledgeGraph":
        """Rehydrate a graph by replaying every record through the create_* gate.

        All or nothing: the graph is built in isolation and returned only when
        every record commits. Any refusal raises ValueError carrying every
        reason, so a caller never holds a partially rehydrated graph. An absent
        family means no records of that kind; an unknown family is a refusal.
        """
        if not isinstance(records, dict):
            raise TypeError("Records must be a mapping")
        graph = cls(registry)
        known = {family for family, _ in RECORD_FAMILIES}
        failures = [f"Unknown record family: '{name}'" for name in sorted(set(records) - known)]
        for family, kind in RECORD_FAMILIES:
            entries = records.get(family, [])
            if not isinstance(entries, (list, tuple)):
                failures.append(f"Record family '{family}' must be a list")
                continue
            for position, record in enumerate(entries):
                failures.extend(graph._replay_record(family, kind, position, record))
        if failures:
            raise ValueError(f"Cannot rehydrate graph from records: {'; '.join(failures)}")
        return graph

    def _replay_record(
        self,
        family: str,
        kind: str,
        position: int,
        record: Any,
    ) -> list[str]:
        label = f"{family}[{position}]"
        if not isinstance(record, dict):
            return [f"{label} is not a mapping"]
        expected = ["type", "id", "properties"]
        if kind == "RELATION":
            expected = ["type", "id", "source_id", "target_id", "properties"]
        missing = [key for key in expected if key not in record]
        if missing:
            return [f"{label} is missing required keys: {missing}"]
        unexpected = sorted(set(record) - set(expected))
        if unexpected:
            return [f"{label} carries unexpected keys: {unexpected}"]
        if kind == "ENTITY":
            operation = self.create_entity(record["type"], record["id"], record["properties"])
        elif kind == "RELATION":
            operation = self.create_relation(
                record["type"],
                record["id"],
                record["source_id"],
                record["target_id"],
                record["properties"],
            )
        elif kind == "SIGNAL":
            operation = self.create_signal(record["type"], record["id"], record["properties"])
        elif kind == "EVENT":
            operation = self.create_event(record["type"], record["id"], record["properties"])
        else:
            operation = self.create_event_participation(
                record["type"], record["id"], record["properties"]
            )
        if operation.op_status == OpStatus.REJECTED:
            return [f"{label} '{record['id']}': {operation.rejection_reason}"]
        return []

    def _replace_materialized_state(self, other: "KnowledgeGraph") -> None:
        """Atomically replace state from a fully validated isolated graph."""
        if not isinstance(other, KnowledgeGraph):
            raise TypeError("Replacement state must be a KnowledgeGraph")
        if self._registry.content_hash() != other._registry.content_hash():
            raise ValueError("Replacement graph uses a different ontology")
        graph = deepcopy(other._graph)
        identifiers = deepcopy(other._identifiers)
        operations = deepcopy(other._operations)
        current_turn = other._current_turn
        self._graph = graph
        self._identifiers = identifiers
        self._operations = operations
        self._current_turn = current_turn

    def set_turn(self, turn: int) -> None:
        self._current_turn = turn

    def _validate_entity(
        self,
        entity_type: str,
        entity_id: str,
        properties: dict[str, Any],
    ) -> ValidationResult:
        type_result = self._validate_category(entity_type, "Entity", "entity type")
        if not type_result.valid:
            return type_result
        common = self._validate_common_id(
            entity_id,
            properties,
            {"id", "type", "is_signal", "is_event"},
        )
        if not common.valid:
            return common
        return self._validate_payload(entity_type, {**properties, "id": entity_id})

    def _validate_relation(
        self,
        relation_type: str,
        relation_id: str,
        source_id: str,
        target_id: str,
        properties: dict[str, Any],
    ) -> ValidationResult:
        type_result = self._validate_category(relation_type, "Relation", "relation type")
        if not type_result.valid:
            return type_result
        common = self._validate_common_id(
            relation_id,
            properties,
            {"id", "type", "source_id", "target_id"},
        )
        if not common.valid:
            return common
        payload = {
            **properties,
            "id": relation_id,
            "source_id": source_id,
            "target_id": target_id,
        }
        structural = self._validate_payload(relation_type, payload)
        if not structural.valid:
            return structural
        for role, identifier, slot_name in (
            ("Source", source_id, "source_id"),
            ("Target", target_id, "target_id"),
        ):
            endpoint = self._identifiers.get(identifier)
            if endpoint is None:
                return ValidationResult(False, f"{role} entity '{identifier}' does not exist")
            endpoint_kind, endpoint_type = endpoint
            if endpoint_kind != "ENTITY":
                return ValidationResult(False, f"{role} '{identifier}' is not an Entity")
            expected = self._registry.get_slot_constraint(relation_type, slot_name)
            if expected and expected.range and self._registry.has_type(expected.range):
                if not self._registry.is_subtype_of(endpoint_type, expected.range):
                    return ValidationResult(
                        False,
                        f"{role} '{identifier}' has type '{endpoint_type}', "
                        f"expected '{expected.range}' for {relation_type}",
                    )
        return ValidationResult(True)

    def _validate_signal(
        self,
        signal_type: str,
        signal_id: str,
        properties: dict[str, Any],
    ) -> ValidationResult:
        type_result = self._validate_category(signal_type, "Signal", "signal type class")
        if not type_result.valid:
            return type_result
        common = self._validate_common_id(
            signal_id,
            properties,
            {"id", "type", "is_signal", "is_event"},
        )
        if not common.valid:
            return common
        structural = self._validate_payload(signal_type, {**properties, "id": signal_id})
        if not structural.valid:
            return structural
        bearer_id = properties.get("bearer_id")
        if not bearer_id:
            # Reachable when a domain schema relaxes bearer_id to optional.
            # A refusal is data, never a KeyError.
            return ValidationResult(False, "Signal requires bearer_id")
        bearer = self._identifiers.get(bearer_id)
        if bearer is None:
            return ValidationResult(False, f"Bearer '{bearer_id}' does not exist")
        if bearer[0] not in {"ENTITY", "RELATION"}:
            return ValidationResult(False, f"Bearer '{bearer_id}' must be an Entity or Relation")
        return ValidationResult(True)

    def _validate_event(
        self,
        event_type: str,
        event_id: str,
        properties: dict[str, Any],
    ) -> ValidationResult:
        type_result = self._validate_category(event_type, "Event", "event type class")
        if not type_result.valid:
            return type_result
        common = self._validate_common_id(
            event_id,
            properties,
            {"id", "type", "is_signal", "is_event"},
        )
        if not common.valid:
            return common
        return self._validate_payload(event_type, {**properties, "id": event_id})

    def _validate_event_participation(
        self,
        participation_type: str,
        participation_id: str,
        properties: dict[str, Any],
    ) -> ValidationResult:
        type_result = self._validate_category(
            participation_type,
            "EventParticipation",
            "event participation type",
        )
        if not type_result.valid:
            return type_result
        common = self._validate_common_id(
            participation_id,
            properties,
            {"id", "type", "is_event_participation"},
        )
        if not common.valid:
            return common
        structural = self._validate_payload(
            participation_type, {**properties, "id": participation_id}
        )
        if not structural.valid:
            return structural
        for role, property_name, expected_kind in (
            ("Event", "event_id", "EVENT"),
            ("Entity", "entity_id", "ENTITY"),
        ):
            identifier = properties.get(property_name)
            if not isinstance(identifier, str) or not identifier:
                return ValidationResult(False, f"{role} ID is required")
            endpoint = self._identifiers.get(identifier)
            if endpoint is None:
                return ValidationResult(False, f"{role} '{identifier}' does not exist")
            endpoint_kind, endpoint_type = endpoint
            if endpoint_kind != expected_kind:
                return ValidationResult(
                    False, f"{role} '{identifier}' is not an {role}"
                )
            expected = self._registry.get_slot_constraint(
                participation_type, property_name
            )
            if expected and expected.range and self._registry.has_type(expected.range):
                if not self._registry.is_subtype_of(endpoint_type, expected.range):
                    return ValidationResult(
                        False,
                        f"{role} '{identifier}' has type '{endpoint_type}', "
                        f"expected '{expected.range}' for {participation_type}",
                    )
        return ValidationResult(True)

    def _validate_category(
        self,
        type_name: str,
        root_type: str,
        label: str,
    ) -> ValidationResult:
        if not isinstance(type_name, str) or not type_name.strip():
            return ValidationResult(False, f"{label.capitalize()} must be a nonblank string")
        if not self._registry.has_type(type_name):
            return ValidationResult(False, f"Unknown {label}: '{type_name}'")
        if self._registry.get_type(type_name).abstract:
            return ValidationResult(False, f"'{type_name}' is abstract and cannot be instantiated")
        if not self._registry.is_subtype_of(type_name, root_type):
            article = "an" if root_type[0].lower() in "aeiou" else "a"
            return ValidationResult(False, f"'{type_name}' is not {article} {root_type} subtype")
        return ValidationResult(True)

    def _validate_common_id(
        self,
        identifier: Any,
        properties: dict[str, Any],
        reserved: set[str],
    ) -> ValidationResult:
        supplied = sorted(reserved & set(properties))
        if supplied:
            return ValidationResult(
                False,
                f"Reserved positional properties cannot be repeated: {supplied}",
            )
        if not isinstance(identifier, str) or not identifier.strip():
            return ValidationResult(False, "Identifier must be a nonblank string")
        if identifier in self._identifiers:
            kind, _ = self._identifiers[identifier]
            return ValidationResult(False, f"Identifier '{identifier}' already exists as {kind}")
        return ValidationResult(True)

    def _validate_payload(self, type_name: str, payload: dict[str, Any]) -> ValidationResult:
        errors = self._registry.validate_instance(type_name, payload)
        return ValidationResult(not errors, "; ".join(errors) if errors else None)

    @staticmethod
    def _properties(properties: dict[str, Any] | None) -> tuple[dict[str, Any], str | None]:
        if properties is None:
            return {}, None
        if not isinstance(properties, dict):
            return {}, "Properties must be a mapping"
        return dict(properties), None

    def _record(
        self,
        op_type: OpType,
        record_type: str,
        data: dict[str, Any],
        result: ValidationResult,
    ) -> Operation:
        operation = Operation(
            turn=self._current_turn,
            op_type=op_type,
            op_status=OpStatus.COMMITTED if result.valid else OpStatus.REJECTED,
            entity_type=record_type,
            data=data,
            rejection_reason=result.error,
        )
        self._operations.append(deepcopy(operation))
        return operation

    def create_entity(
        self,
        entity_type: str,
        entity_id: str,
        properties: dict[str, Any] | None = None,
    ) -> Operation:
        props, property_error = self._properties(properties)
        result = (
            ValidationResult(False, property_error)
            if property_error
            else self._validate_entity(entity_type, entity_id, props)
        )
        data = {**deepcopy(props), "id": entity_id}
        operation = self._record(OpType.CREATE_ENTITY, entity_type, data, result)
        if result.valid:
            self._graph.add_node(entity_id, type=entity_type, **deepcopy(props))
            self._identifiers[entity_id] = ("ENTITY", entity_type)
        return operation

    def create_relation(
        self,
        relation_type: str,
        relation_id: str,
        source_id: str,
        target_id: str,
        properties: dict[str, Any] | None = None,
    ) -> Operation:
        props, property_error = self._properties(properties)
        result = (
            ValidationResult(False, property_error)
            if property_error
            else self._validate_relation(
                relation_type,
                relation_id,
                source_id,
                target_id,
                props,
            )
        )
        data = {
            **deepcopy(props),
            "id": relation_id,
            "source_id": source_id,
            "target_id": target_id,
        }
        operation = self._record(OpType.CREATE_RELATION, relation_type, data, result)
        if result.valid:
            self._graph.add_edge(
                source_id,
                target_id,
                key=relation_id,
                type=relation_type,
                **deepcopy(props),
            )
            self._identifiers[relation_id] = ("RELATION", relation_type)
        return operation

    def create_signal(
        self,
        signal_type_class: str,
        signal_id: str,
        properties: dict[str, Any] | None = None,
    ) -> Operation:
        props, property_error = self._properties(properties)
        result = (
            ValidationResult(False, property_error)
            if property_error
            else self._validate_signal(signal_type_class, signal_id, props)
        )
        data = {**deepcopy(props), "id": signal_id}
        operation = self._record(OpType.CREATE_SIGNAL, signal_type_class, data, result)
        if result.valid:
            self._graph.add_node(
                signal_id,
                type=signal_type_class,
                is_signal=True,
                **deepcopy(props),
            )
            self._identifiers[signal_id] = ("SIGNAL", signal_type_class)
        return operation

    def create_event(
        self,
        event_type_class: str,
        event_id: str,
        properties: dict[str, Any] | None = None,
    ) -> Operation:
        props, property_error = self._properties(properties)
        result = (
            ValidationResult(False, property_error)
            if property_error
            else self._validate_event(event_type_class, event_id, props)
        )
        data = {**deepcopy(props), "id": event_id}
        operation = self._record(OpType.CREATE_EVENT, event_type_class, data, result)
        if result.valid:
            self._graph.add_node(
                event_id,
                type=event_type_class,
                is_event=True,
                **deepcopy(props),
            )
            self._identifiers[event_id] = ("EVENT", event_type_class)
        return operation

    def create_event_participation(
        self,
        participation_type: str,
        participation_id: str,
        properties: dict[str, Any] | None = None,
    ) -> Operation:
        """Create one qualified Entity participation in an Event."""

        props, property_error = self._properties(properties)
        result = (
            ValidationResult(False, property_error)
            if property_error
            else self._validate_event_participation(
                participation_type, participation_id, props
            )
        )
        data = {**deepcopy(props), "id": participation_id}
        operation = self._record(
            OpType.CREATE_EVENT_PARTICIPATION,
            participation_type,
            data,
            result,
        )
        if result.valid:
            self._graph.add_node(
                participation_id,
                type=participation_type,
                is_event_participation=True,
                **deepcopy(props),
            )
            self._identifiers[participation_id] = (
                "EVENT_PARTICIPATION",
                participation_type,
            )
        return operation

    def query(
        self,
        entity_type: str | None = None,
        mixin: str | None = None,
        **filters: Any,
    ) -> list[dict[str, Any]]:
        results = []
        for node_id, data in self._graph.nodes(data=True):
            node_type = data.get("type", "")
            if entity_type and node_type != entity_type:
                if not self._registry.is_subtype_of(node_type, entity_type):
                    continue
            if mixin and not self._registry.has_mixin(node_type, mixin):
                continue
            if all(data.get(key) == value for key, value in filters.items()):
                results.append(deepcopy({"id": node_id, **data}))
        return results

    def query_relations(
        self,
        relation_type: str | None = None,
        source_id: str | None = None,
        target_id: str | None = None,
    ) -> list[dict[str, Any]]:
        results = []
        for source, target, key, data in self._graph.edges(data=True, keys=True):
            if relation_type and data.get("type") != relation_type:
                continue
            if source_id and source != source_id:
                continue
            if target_id and target != target_id:
                continue
            results.append(deepcopy({"source_id": source, "target_id": target, "key": key, **data}))
        return results

    def query_event_participations(
        self,
        *,
        event_id: str | None = None,
        entity_id: str | None = None,
        qualifier: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return qualified Event-to-Entity participation records."""

        results = []
        for node_id, data in self._graph.nodes(data=True):
            if not data.get("is_event_participation"):
                continue
            if event_id is not None and data.get("event_id") != event_id:
                continue
            if entity_id is not None and data.get("entity_id") != entity_id:
                continue
            if qualifier is not None and data.get("qualifier") != qualifier:
                continue
            results.append(
                deepcopy(
                    {
                        "id": node_id,
                        **{
                            key: value
                            for key, value in data.items()
                            if key != "is_event_participation"
                        },
                    }
                )
            )
        results.sort(key=lambda item: item["id"])
        return results

    def get_node(self, node_id: str) -> dict[str, Any] | None:
        if node_id not in self._graph:
            return None
        return deepcopy({"id": node_id, **self._graph.nodes[node_id]})

    def get_relation(self, relation_id: str) -> dict[str, Any] | None:
        """Return the committed relation record, or None when no such relation exists."""
        for source, target, key, data in self._graph.edges(data=True, keys=True):
            if key == relation_id:
                return deepcopy({
                    "id": key,
                    "source_id": source,
                    "target_id": target,
                    **data,
                })
        return None

    def has_node(self, node_id: str) -> bool:
        return node_id in self._graph

    def committed_operations(self, turn: int | None = None) -> list[Operation]:
        operations = [op for op in self._operations if op.op_status == OpStatus.COMMITTED]
        selected = [op for op in operations if op.turn == turn] if turn is not None else operations
        return deepcopy(selected)

    def rejected_operations(self, turn: int | None = None) -> list[Operation]:
        operations = [op for op in self._operations if op.op_status == OpStatus.REJECTED]
        selected = [op for op in operations if op.turn == turn] if turn is not None else operations
        return deepcopy(selected)

    def rejection_rate(self, turn: int | None = None) -> float:
        operations = (
            [op for op in self._operations if op.turn == turn]
            if turn is not None
            else self._operations
        )
        if not operations:
            return 0.0
        return sum(op.op_status == OpStatus.REJECTED for op in operations) / len(operations)
