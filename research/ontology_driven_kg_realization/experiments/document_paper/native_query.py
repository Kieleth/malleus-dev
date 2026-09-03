"""Type-bound native graph queries for the paper-v4 document run."""

from __future__ import annotations

from copy import deepcopy
import json
from typing import Any, Mapping

from malleus.kg import KnowledgeGraph
from malleus.ontology import OntologyRegistry


QUERY_IDS = ("NQ-CQ-01", "NQ-CQ-02", "NQ-CQ-03", "NQ-CQ-04")
QUESTION_IDS = ("CQ-01", "CQ-02", "CQ-03", "CQ-04")
_SCHEMA = "malleus.paper-v4.native-query-binding/v1"
_STATUS = "FROZEN_BEFORE_POPULATION"


class NativeQueryRefusal(ValueError):
    """The query binding or replayed graph cannot produce a valid result."""

    def __init__(self, subject: str, detail: str) -> None:
        self.subject = subject
        self.detail = detail
        super().__init__(f"{subject}: {detail}")


def _refuse(subject: str, detail: str) -> None:
    raise NativeQueryRefusal(subject, detail)


def _object(value: object, subject: str) -> dict[str, Any]:
    if type(value) is not dict:
        _refuse(subject, "must be an object")
    return value


def _array(value: object, subject: str) -> list[Any]:
    if type(value) is not list:
        _refuse(subject, "must be an array")
    return value


def _text(value: object, subject: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _refuse(subject, "must be nonblank text")
    return value


def _exact_keys(
    value: Mapping[str, Any], expected: frozenset[str], subject: str
) -> None:
    observed = set(value)
    if observed != expected:
        _refuse(
            subject,
            f"keys differ: missing={sorted(expected - observed)}, "
            f"extra={sorted(observed - expected)}",
        )


def _output_fields(value: object, subject: str) -> dict[str, list[str]]:
    result = _object(value, subject)
    _exact_keys(result, frozenset({"source", "relation", "target"}), subject)
    for role in ("source", "relation", "target"):
        fields = _array(result[role], f"{subject}.{role}")
        if not all(isinstance(item, str) and item.strip() for item in fields):
            _refuse(f"{subject}.{role}", "fields must be nonblank strings")
        if len(fields) != len(set(fields)):
            _refuse(f"{subject}.{role}", "fields must be unique")
    if not any(result.values()):
        _refuse(subject, "must project at least one field")
    return result


def validate_query_binding(binding: object) -> dict[str, Any]:
    """Validate the closed type-only binding grammar, without reading files."""

    root = _object(binding, "binding")
    _exact_keys(root, frozenset({"schema", "status", "queries"}), "binding")
    if root["schema"] != _SCHEMA:
        _refuse("binding.schema", f"must equal {_SCHEMA!r}")
    if root["status"] != _STATUS:
        _refuse("binding.status", f"must equal {_STATUS!r}")
    queries = _array(root["queries"], "binding.queries")
    if [item.get("id") if type(item) is dict else None for item in queries] != list(
        QUERY_IDS
    ):
        _refuse("binding.queries", "query ids or order differ from the four fixed queries")
    if [
        item.get("question_id") if type(item) is dict else None for item in queries
    ] != list(QUESTION_IDS):
        _refuse(
            "binding.queries", "question ids or order differ from the four fixed questions"
        )

    for query_index, raw_query in enumerate(queries):
        query_subject = f"binding.queries[{query_index}]"
        query = _object(raw_query, query_subject)
        _exact_keys(query, frozenset({"id", "question_id", "cases"}), query_subject)
        cases = _array(query["cases"], f"{query_subject}.cases")
        if not cases:
            _refuse(f"{query_subject}.cases", "must not be empty")
        for case_index, raw_case in enumerate(cases):
            case_subject = f"{query_subject}.cases[{case_index}]"
            case = _object(raw_case, case_subject)
            _exact_keys(
                case,
                frozenset(
                    {
                        "ordinal",
                        "source_record_type",
                        "relation_record_type",
                        "relation_type",
                        "target_record_type",
                        "output_fields",
                    }
                ),
                case_subject,
            )
            if type(case["ordinal"]) is not int or case["ordinal"] != case_index + 1:
                _refuse(f"{case_subject}.ordinal", "must be its one-based case position")
            for field in (
                "source_record_type",
                "relation_record_type",
                "target_record_type",
            ):
                _text(case[field], f"{case_subject}.{field}")
            relation_type = _object(
                case["relation_type"], f"{case_subject}.relation_type"
            )
            _exact_keys(
                relation_type,
                frozenset({"enum", "value"}),
                f"{case_subject}.relation_type",
            )
            _text(relation_type["enum"], f"{case_subject}.relation_type.enum")
            _text(relation_type["value"], f"{case_subject}.relation_type.value")
            _output_fields(case["output_fields"], f"{case_subject}.output_fields")
    return root


def load_query_binding(source: bytes) -> dict[str, Any]:
    """Parse exact JSON bytes into the closed query-binding grammar."""

    if not isinstance(source, bytes):
        raise TypeError("query binding source must be bytes")
    try:
        value = json.loads(source)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        _refuse("binding", f"must be UTF-8 JSON: {error}")
    return validate_query_binding(value)


def validate_query_binding_against_ontology(
    binding: object, registry: OntologyRegistry
) -> dict[str, Any]:
    """Prove that binding types, enums, directions, and fields exist."""

    root = validate_query_binding(binding)
    if type(registry) is not OntologyRegistry:
        raise TypeError("registry must be one exact OntologyRegistry")
    for query in root["queries"]:
        for case in query["cases"]:
            subject = f"{query['id']}.case-{case['ordinal']}"
            source_type = case["source_record_type"]
            relation_type = case["relation_record_type"]
            target_type = case["target_record_type"]
            for type_name, role in (
                (source_type, "Entity"),
                (relation_type, "Relation"),
                (target_type, "Entity"),
            ):
                if not registry.has_type(type_name):
                    _refuse(subject, f"unknown record type {type_name!r}")
                if not registry.is_subtype_of(type_name, role):
                    _refuse(subject, f"{type_name!r} is not a {role} record type")

            slots = registry.effective_slots(relation_type)
            enum = case["relation_type"]["enum"]
            enum_value = case["relation_type"]["value"]
            relation_slot = slots.get("relation_type")
            if relation_slot is None or relation_slot.range != enum:
                _refuse(subject, "relation_type enum does not match the relation record")
            if relation_slot.equals_string != enum_value:
                _refuse(subject, "relation_type value does not match the relation record")
            if not registry.is_valid_enum_value(enum, enum_value):
                _refuse(subject, f"unknown enum value {enum}.{enum_value}")

            for endpoint, selected_type in (
                ("source_id", source_type),
                ("target_id", target_type),
            ):
                constraint = slots.get(endpoint)
                if constraint is None or constraint.range is None:
                    _refuse(subject, f"relation lacks a typed {endpoint}")
                if not registry.is_subtype_of(selected_type, constraint.range):
                    _refuse(
                        subject,
                        f"{selected_type!r} is outside {endpoint} range {constraint.range!r}",
                    )

            for role, type_name in (
                ("source", source_type),
                ("relation", relation_type),
                ("target", target_type),
            ):
                legal_fields = registry.effective_slots(type_name)
                unknown = sorted(set(case["output_fields"][role]) - set(legal_fields))
                if unknown:
                    _refuse(subject, f"unknown {role} output fields: {unknown}")
    return root


def _required(record: Mapping[str, Any], field: str, subject: str) -> Any:
    if field not in record:
        _refuse(subject, f"required graph field {field!r} is absent")
    return record[field]


def _record_text(record: Mapping[str, Any], field: str, subject: str) -> str:
    return _text(_required(record, field, subject), f"{subject}.{field}")


def _project(
    record: Mapping[str, Any], fields: list[str], subject: str
) -> dict[str, Any]:
    return {field: deepcopy(_required(record, field, subject)) for field in fields}


def _run_query(graph: KnowledgeGraph, query: Mapping[str, Any]) -> dict[str, Any]:
    rows = []
    for case in query["cases"]:
        query_id = query["id"]
        subject = f"{query_id}.case-{case['ordinal']}"
        relations = graph.query_relations(
            relation_type=case["relation_record_type"]
        )
        for relation in relations:
            if _record_text(relation, "type", subject) != case["relation_record_type"]:
                _refuse(subject, "graph returned the wrong relation record type")
            observed_enum = _record_text(relation, "relation_type", subject)
            if observed_enum != case["relation_type"]["value"]:
                _refuse(subject, "relation record violates its bound enum value")
            source_id = _record_text(relation, "source_id", subject)
            target_id = _record_text(relation, "target_id", subject)
            source = graph.get_node(source_id)
            target = graph.get_node(target_id)
            if source is None or target is None:
                _refuse(subject, "relation endpoint does not resolve")
            if (
                _record_text(source, "type", subject)
                != case["source_record_type"]
                or _record_text(target, "type", subject)
                != case["target_record_type"]
            ):
                continue
            fields = case["output_fields"]
            rows.append(
                {
                    "case_ordinal": case["ordinal"],
                    "source": _project(source, fields["source"], subject),
                    "relation": _project(relation, fields["relation"], subject),
                    "target": _project(target, fields["target"], subject),
                    "witness": {
                        "relation_id": _record_text(relation, "key", subject),
                        "source_id": source_id,
                        "target_id": target_id,
                    },
                }
            )
    rows.sort(key=lambda item: (item["case_ordinal"], item["witness"]["relation_id"]))
    return {
        "query_id": query["id"],
        "question_id": query["question_id"],
        "rows": rows,
    }


def run_native_query(
    graph: KnowledgeGraph, binding: object, query_id: str
) -> dict[str, Any]:
    """Run one frozen type-bound query against replayed graph state."""

    if not isinstance(graph, KnowledgeGraph):
        raise TypeError("graph must be a KnowledgeGraph")
    root = validate_query_binding(binding)
    for query in root["queries"]:
        if query["id"] == query_id:
            return _run_query(graph, query)
    _refuse("NQ-DISPATCH", f"unknown query id {query_id!r}")


def run_frozen_queries(
    graph: KnowledgeGraph, binding: object
) -> tuple[dict[str, Any], ...]:
    """Run the four frozen queries without graph-closure assumptions."""

    if not isinstance(graph, KnowledgeGraph):
        raise TypeError("graph must be a KnowledgeGraph")
    root = validate_query_binding(binding)
    return tuple(_run_query(graph, query) for query in root["queries"])
