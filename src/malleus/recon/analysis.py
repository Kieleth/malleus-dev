"""Deterministic graph, matrix, comparison, and report generation."""

from __future__ import annotations

import csv
import errno
import hashlib
import html
import io
import json
import os
import platform
import re
import tempfile
import zipfile
import zlib
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping
from urllib.parse import quote
from xml.etree import ElementTree as ET

import networkx as nx
import yaml

from malleus.ledger import GENESIS
from malleus.ontology import OntologyRegistry, OntologySourceClosure
from malleus.recon.store import (
    BUILD_DIRECTORY,
    PROJECT_FILE,
    ReconError,
    ReconProject,
    StoredRecord,
    _assert_reserved_lock_identity,
    _precheck_reserved_lock,
)
from malleus.status import IMPLEMENTATION_STATUS


MATERIAL_LEVELS = frozenset({"CENTRAL", "MATERIAL"})
STRUCTURAL_CAPTURE_PROFILE = "malleus.recon.structural-capture/v1"
_BUILD_GENERATOR = {
    "name": "malleus-recon",
    "package": "malleus-dev",
    "package_version": IMPLEMENTATION_STATUS.package_version,
}
_BUILD_RUNTIME = {
    "python": platform.python_version(),
    "python_implementation": platform.python_implementation(),
    "networkx": nx.__version__,
    "pyyaml": yaml.__version__,
    "zlib": zlib.ZLIB_RUNTIME_VERSION,
}
_XSD = "http://www.w3.org/2001/XMLSchema#"
_SCALAR_COERCIONS = {
    "boolean": _XSD + "boolean",
    "date": _XSD + "date",
    "datetime": _XSD + "dateTime",
    "decimal": _XSD + "decimal",
    "double": _XSD + "double",
    "float": _XSD + "float",
    "integer": _XSD + "integer",
    "time": _XSD + "time",
    "timestamp": _XSD + "dateTime",
    "uri": _XSD + "anyURI",
    "uriorcurie": _XSD + "anyURI",
}
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_ABSOLUTE_IRI = re.compile(r'^[A-Za-z][A-Za-z0-9+.-]*:[^\s<>"{}|\\^`]+$')
_BUILD_MANIFEST_SCHEMA_VERSION = "3"
_GENERATOR_CLOSURE_SCHEMA_VERSION = "1"
_BUILD_LOCK_NAME = ".recon-build.lock"
_LOCK_CONTENTION_ERRNOS = frozenset({errno.EACCES, errno.EAGAIN, errno.EWOULDBLOCK})
_LOCK_CONTENTION_WINERRORS = frozenset({33})
_NODE_COLUMNS = (
    "id",
    "type",
    "label",
    "title",
    "review_state",
    "priority_date",
    "statement",
    "source_uri",
)
_EDGE_COLUMNS = (
    "id",
    "type",
    "source_id",
    "target_id",
    "review_state",
    "assertion_status",
    "confidence",
    "coverage_level",
    "basis",
    "evidence_ids",
)
_HISTORICAL_OUTPUT_ALLOWLIST = frozenset(
    {
        "bibliography.bib",
        "comparisons.json",
        "edges.csv",
        "evidence.csv",
        "literature_kg.graphml",
        "literature_kg.json",
        "literature_kg.jsonld",
        "metrics.json",
        "nodes.csv",
        "report.md",
        "work_axis_matrix.csv",
    }
)
_MANIFEST_FIELDS = frozenset(
    {
        "archive",
        "event_count",
        "files",
        "generator",
        "jsonld_ontology",
        "ledger_head",
        "ontology_verification",
        "ontology_hash",
        "profile",
        "project",
        "runtime",
        "schema_version",
        "state",
    }
)
_IMPLEMENTATION_SOURCES = (
    ("malleus.recon.analysis", Path(__file__)),
    ("malleus.recon.store", Path(__file__).with_name("store.py")),
    ("malleus.ontology", Path(__file__).parents[1] / "ontology.py"),
    ("malleus.migration", Path(__file__).parents[1] / "migration.py"),
    ("malleus.kg", Path(__file__).parents[1] / "kg.py"),
    ("malleus.ledger", Path(__file__).parents[1] / "ledger.py"),
)


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def _csv_text(columns: Iterable[str], rows: Iterable[Mapping[str, Any]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(columns), lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                column: (
                    json.dumps(row.get(column), ensure_ascii=False, sort_keys=True)
                    if isinstance(row.get(column), (list, dict))
                    else row.get(column, "")
                )
                for column in writer.fieldnames
            }
        )
    return stream.getvalue()


def _split_records(
    project: ReconProject,
    records: Mapping[str, StoredRecord],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    nodes = []
    edges = []
    for identifier, stored in sorted(records.items()):
        record = {"id": identifier, "type": stored.record_type, **deepcopy(stored.record)}
        if project.registry.is_subtype_of(stored.record_type, "Relation"):
            edges.append(record)
        else:
            nodes.append(record)
    return nodes, edges


def _meta(project: ReconProject, events: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "1",
        "title": project.config["title"],
        "target_id": project.config["target_id"],
        "created_at": project.config["created_at"],
        "ontology_hash": project.ontology_hash,
        "ledger_head": events[-1]["event_hash"] if events else GENESIS,
        "event_count": len(events),
        "rejected_event_count": sum(
            event["payload"]["decision"] == "REJECTED" for event in events
        ),
    }


def _canonical_snapshot(
    project: ReconProject,
    events: list[dict[str, Any]],
    records: Mapping[str, StoredRecord],
) -> dict[str, Any]:
    errors = project.validate(records)
    if errors:
        raise ReconError("Recon project is incomplete: " + "; ".join(errors))
    nodes, edges = _split_records(project, records)
    return {"meta": _meta(project, events), "nodes": nodes, "edges": edges}


def canonical_graph(project: ReconProject) -> dict[str, Any]:
    events, records = project.snapshot()
    return _canonical_snapshot(project, events, records)


def _networkx_graph(canonical: Mapping[str, Any]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph(**canonical["meta"])
    for node in canonical["nodes"]:
        attributes = {key: _graphml_value(value) for key, value in node.items() if key != "id"}
        graph.add_node(node["id"], **attributes)
    for edge in canonical["edges"]:
        attributes = {
            key: _graphml_value(value)
            for key, value in edge.items()
            if key not in {"id", "source_id", "target_id"}
        }
        graph.add_edge(
            edge["source_id"],
            edge["target_id"],
            key=edge["id"],
            id=edge["id"],
            **attributes,
        )
    return graph


def current_graph(project: ReconProject) -> nx.MultiDiGraph:
    return _networkx_graph(canonical_graph(project))


def _graphml_value(value: Any) -> str | int | float | bool:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _profiles(records: Mapping[str, StoredRecord]) -> dict[str, dict[str, str]]:
    active_axes = _active_axis_ids(records)
    profiles: dict[str, dict[str, str]] = {}
    for stored in records.values():
        if stored.record_type != "CoversAxisRelation":
            continue
        record = stored.record
        if (
            record.get("review_state") != "REVIEWED"
            or record["target_id"] not in active_axes
        ):
            continue
        profiles.setdefault(record["source_id"], {})[record["target_id"]] = record[
            "coverage_level"
        ]
    return profiles


def _contested_profiles(
    records: Mapping[str, StoredRecord],
) -> dict[str, dict[str, str]]:
    active_axes = _active_axis_ids(records)
    profiles: dict[str, dict[str, str]] = {}
    for stored in records.values():
        if stored.record_type != "CoversAxisRelation":
            continue
        record = stored.record
        if (
            record.get("review_state") != "CONTESTED"
            or record["target_id"] not in active_axes
        ):
            continue
        profiles.setdefault(record["source_id"], {})[record["target_id"]] = record[
            "coverage_level"
        ]
    return profiles


def _active_axis_ids(records: Mapping[str, StoredRecord]) -> set[str]:
    return {
        identifier
        for identifier, stored in records.items()
        if stored.record_type == "ComparisonAxis"
        and stored.record.get("review_state") != "RETIRED"
    }


def _reported_coverage(
    reviewed: Mapping[str, str],
    contested: Mapping[str, str],
    axis: str,
) -> str | None:
    if axis in reviewed:
        return reviewed[axis]
    if axis in contested:
        return f"CONTESTED:{contested[axis]}"
    return None


def compare_subjects(
    project: ReconProject,
    target_id: str,
    work_id: str,
) -> dict[str, Any]:
    records = project.current_records()
    return _compare_subjects(project, records, target_id, work_id)


def _compare_subjects(
    project: ReconProject,
    records: Mapping[str, StoredRecord],
    target_id: str,
    work_id: str,
) -> dict[str, Any]:
    for identifier in (target_id, work_id):
        stored = records.get(identifier)
        if stored is None:
            raise ReconError(f"Unknown comparison subject: '{identifier}'")
        if not project.registry.is_subtype_of(stored.record_type, "ReviewSubject"):
            raise ReconError(
                f"Comparison subject '{identifier}' is {stored.record_type}, "
                "expected ReviewSubject"
            )
        if stored.record.get("review_state") == "RETIRED":
            raise ReconError(f"Comparison subject '{identifier}' is retired")
    profiles = _profiles(records)
    contested_profiles = _contested_profiles(records)
    target_profile = profiles.get(target_id, {})
    work_profile = profiles.get(work_id, {})
    target_contested = contested_profiles.get(target_id, {})
    work_contested = contested_profiles.get(work_id, {})
    target_set = {
        axis for axis, level in target_profile.items() if level in MATERIAL_LEVELS
    }
    work_set = {axis for axis, level in work_profile.items() if level in MATERIAL_LEVELS}
    all_axes = sorted(
        identifier
        for identifier, stored in records.items()
        if stored.record_type == "ComparisonAxis"
        and stored.record.get("review_state") != "RETIRED"
    )
    reported = {
        axis: {
            "target": _reported_coverage(target_profile, target_contested, axis),
            "work": _reported_coverage(work_profile, work_contested, axis),
        }
        for axis in all_axes
    }
    unresolved = {
        axis: values
        for axis, values in reported.items()
        if values["target"] in {"NOT_ESTABLISHED", "CONTRADICTED"}
        or values["work"] in {"NOT_ESTABLISHED", "CONTRADICTED"}
    }
    unassessed = {
        axis: values
        for axis, values in reported.items()
        if values["target"] is None or values["work"] is None
    }
    partial = {
        axis: reported[axis]
        for axis in all_axes
        if target_profile.get(axis) in {"PARTIAL", "ADJACENT"}
        or work_profile.get(axis) in {"PARTIAL", "ADJACENT"}
    }
    return {
        "target_id": target_id,
        "work_id": work_id,
        "material_levels": sorted(MATERIAL_LEVELS),
        "intersection": sorted(target_set & work_set),
        "union": sorted(target_set | work_set),
        "target_difference": sorted(target_set - work_set),
        "work_difference": sorted(work_set - target_set),
        "symmetric_difference": sorted(target_set ^ work_set),
        "partial_or_adjacent": partial,
        "unresolved": unresolved,
        "unassessed": unassessed,
        "contested": {
            axis: {
                "target": target_contested.get(axis),
                "work": work_contested.get(axis),
            }
            for axis in sorted(set(target_contested) | set(work_contested))
        },
        "target_profile": dict(sorted(target_profile.items())),
        "work_profile": dict(sorted(work_profile.items())),
        "boundary": (
            "Set membership reflects reviewer-coded CENTRAL or MATERIAL coverage only; "
            "null means no active assessment is recorded, while NOT_ESTABLISHED is an "
            "explicit reviewer-coded assessment. This is not a novelty verdict."
        ),
    }


def metrics(project: ReconProject) -> dict[str, Any]:
    events, records = project.snapshot()
    _canonical_snapshot(project, events, records)
    return _metrics_snapshot(project, events, records)


def _metrics_snapshot(
    project: ReconProject,
    events: list[dict[str, Any]],
    records: Mapping[str, StoredRecord],
) -> dict[str, Any]:
    nodes, edges = _split_records(project, records)
    active_nodes = [node for node in nodes if node.get("review_state") != "RETIRED"]
    active_node_ids = {node["id"] for node in active_nodes}
    active_edges = [
        edge
        for edge in edges
        if edge.get("review_state") != "RETIRED"
        and edge["source_id"] in active_node_ids
        and edge["target_id"] in active_node_ids
    ]
    retired_records = sum(
        record.get("review_state") == "RETIRED" for record in [*nodes, *edges]
    )
    excluded_relations = len(edges) - len(active_edges) - sum(
        edge.get("review_state") == "RETIRED" for edge in edges
    )
    relations = {edge["id"]: edge for edge in active_edges}
    owned_claims = {
        edge["target_id"] for edge in active_edges if edge["type"] == "HasClaimRelation"
    }
    owned_results = {
        edge["target_id"] for edge in active_edges if edge["type"] == "HasResultRelation"
    }
    claims = {node["id"] for node in active_nodes if node["type"] == "Claim"}
    results = {node["id"] for node in active_nodes if node["type"] == "Result"}
    evidence_bearing = [
        record
        for record in [*active_nodes, *active_edges]
        if record.get("review_state") in {"REVIEWED", "CONTESTED"}
        and record["type"]
        in {"Work", "Claim", "Result", *{edge["type"] for edge in active_edges}}
    ]
    supported = [record for record in evidence_bearing if record.get("evidence_ids")]
    undirected = nx.Graph()
    undirected.add_nodes_from(active_node_ids)
    undirected.add_edges_from(
        (edge["source_id"], edge["target_id"]) for edge in active_edges
    )
    active_subjects = {
        node["id"]
        for node in active_nodes
        if project.registry.is_subtype_of(node["type"], "ReviewSubject")
    }
    active_axes = {
        node["id"] for node in active_nodes if node["type"] == "ComparisonAxis"
    }
    assessed_pairs = {
        (edge["source_id"], edge["target_id"])
        for edge in active_edges
        if edge["type"] == "CoversAxisRelation"
        and edge.get("review_state") in {"REVIEWED", "CONTESTED"}
        and edge["source_id"] in active_subjects
        and edge["target_id"] in active_axes
    }
    return {
        "records": len(records),
        "active_records": len(active_nodes) + len(active_edges),
        "retired_records": retired_records,
        "relations_excluded_by_inactive_endpoint": excluded_relations,
        "nodes": len(active_nodes),
        "relations": len(relations),
        "events": len(events),
        "rejections": sum(
            event["payload"]["decision"] == "REJECTED" for event in events
        ),
        "works": sum(node["type"] == "Work" for node in active_nodes),
        "claims": len(claims),
        "results": len(results),
        "axes": sum(node["type"] == "ComparisonAxis" for node in active_nodes),
        "orphan_claims": sorted(claims - owned_claims),
        "orphan_results": sorted(results - owned_results),
        "reviewed_evidence_coverage": (
            len(supported) / len(evidence_bearing) if evidence_bearing else None
        ),
        "weakly_connected_components": (
            nx.number_connected_components(undirected) if undirected.number_of_nodes() else 0
        ),
        "unresolved_axis_assessments": sum(
            edge.get("coverage_level") in {"NOT_ESTABLISHED", "CONTRADICTED"}
            for edge in active_edges
            if edge["type"] == "CoversAxisRelation"
            and edge.get("review_state") == "REVIEWED"
        ),
        "unassessed_subject_axis_pairs": (
            len(active_subjects) * len(active_axes) - len(assessed_pairs)
        ),
        "boundary": "Counts navigate the review; they do not rank paper quality or novelty.",
    }


def _matrix(
    project: ReconProject,
    records: Mapping[str, StoredRecord],
) -> tuple[list[str], list[dict[str, Any]]]:
    subjects = sorted(
        identifier
        for identifier, stored in records.items()
        if project.registry.is_subtype_of(stored.record_type, "ReviewSubject")
        and stored.record.get("review_state") != "RETIRED"
    )
    axes = sorted(
        identifier
        for identifier, stored in records.items()
        if stored.record_type == "ComparisonAxis"
        and stored.record.get("review_state") != "RETIRED"
    )
    profiles = _profiles(records)
    contested = _contested_profiles(records)
    rows = []
    for subject in subjects:
        row = {"subject_id": subject}
        row.update(
            {
                axis: (
                    profiles.get(subject, {}).get(axis)
                    or (
                        f"CONTESTED:{contested[subject][axis]}"
                        if axis in contested.get(subject, {})
                        else ""
                    )
                )
                for axis in axes
            }
        )
        rows.append(row)
    return ["subject_id", *axes], rows


@dataclass(frozen=True)
class _JsonLdOntology:
    classes: Mapping[str, str]
    slots: Mapping[str, str]
    identity: Mapping[str, Any]
    source_closure: OntologySourceClosure
    structural_hash: str


def _schema_document(path: Path) -> tuple[bytes, Mapping[str, Any]]:
    try:
        body = path.read_bytes()
    except OSError as error:
        raise ReconError(f"Cannot derive JSON-LD ontology terms from {path}: {error}") from error
    return body, _schema_document_from_bytes(body, str(path))


def _schema_document_from_bytes(
    body: bytes,
    locator: str,
) -> Mapping[str, Any]:
    try:
        document = yaml.safe_load(body.decode("utf-8"))
    except (TypeError, UnicodeDecodeError, yaml.YAMLError) as error:
        raise ReconError(
            f"Cannot derive JSON-LD ontology terms from {locator}: {error}"
        ) from error
    if not isinstance(document, dict):
        raise ReconError(f"JSON-LD ontology source {locator} must contain one mapping")
    return document


def _schema_terms_from_document(
    document: Mapping[str, Any],
    path: Path,
    section: str,
) -> dict[str, str]:
    try:
        values = document[section]
        schema_id = document["id"]
        prefixes = document.get("prefixes", {})
    except (KeyError, TypeError) as error:
        raise ReconError(f"Cannot derive JSON-LD {section} ownership from {path}: {error}") from error
    if (
        not isinstance(values, dict)
        or not all(isinstance(name, str) for name in values)
        or not isinstance(schema_id, str)
        or not isinstance(prefixes, dict)
    ):
        raise ReconError(f"Ontology {section} in {path} must be a mapping with string names")
    uri_field = {"classes": "class_uri", "slots": "slot_uri"}.get(section)
    if uri_field is None:
        raise ReconError(f"Cannot derive JSON-LD terms for unsupported ontology section: {section}")
    if _ABSOLUTE_IRI.fullmatch(schema_id) is None:
        raise ReconError(f"Ontology schema id in {path} must be an absolute IRI")
    vocabulary = schema_id.rstrip("/#") + "/"
    terms = {}
    for name, raw_definition in values.items():
        definition = raw_definition if isinstance(raw_definition, dict) else {}
        declared = definition.get(uri_field)
        if declared is None:
            term = vocabulary + name
            if _ABSOLUTE_IRI.fullmatch(term) is None:
                raise ReconError(
                    f"Ontology {section}.{name} derived IRI must be absolute"
                )
            terms[name] = term
            continue
        if not isinstance(declared, str) or not declared:
            raise ReconError(f"Ontology {section}.{name}.{uri_field} must be a nonblank string")
        prefix, separator, local_name = declared.partition(":")
        if separator and prefix in prefixes:
            expansion = prefixes[prefix]
            if not isinstance(expansion, str) or _ABSOLUTE_IRI.fullmatch(expansion) is None:
                raise ReconError(
                    f"Ontology prefix '{prefix}' expansion must be an absolute IRI"
                )
            term = expansion + local_name
        elif re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", declared):
            term = declared
        else:
            raise ReconError(
                f"Ontology {section}.{name}.{uri_field} is not an absolute IRI or known CURIE"
            )
        if _ABSOLUTE_IRI.fullmatch(term) is None:
            raise ReconError(
                f"Ontology {section}.{name}.{uri_field} expanded IRI must be absolute"
            )
        terms[name] = term
    return terms


def _schema_terms(path: Path, section: str) -> dict[str, str]:
    _, document = _schema_document(path)
    return _schema_terms_from_document(document, path, section)


def _jsonld_ontology(registry: OntologyRegistry) -> _JsonLdOntology:
    closure = registry.source_closure()
    documents = {
        source.resolved_locator: _schema_document_from_bytes(
            source.source_bytes,
            source.resolved_locator,
        )
        for source in closure.sources
    }
    terms_by_source: dict[tuple[str, str], dict[str, str]] = {}

    def owned_term(locator: str, section: str, name: str) -> str:
        key = (locator, section)
        if key not in terms_by_source:
            terms_by_source[key] = _schema_terms_from_document(
                documents[locator],
                Path(locator),
                section,
            )
        try:
            return terms_by_source[key][name]
        except KeyError as error:
            raise ReconError(
                f"Ontology closure says {locator} owns {section}.{name}, but the "
                "retained source does not declare it"
            ) from error

    classes = {
        definition.name: owned_term(
            definition.source_locator,
            "classes",
            definition.name,
        )
        for definition in closure.definitions
        if definition.kind == "class"
    }
    slots = {
        definition.name: owned_term(
            definition.source_locator,
            "slots",
            definition.name,
        )
        for definition in closure.definitions
        if definition.kind == "slot"
    }
    term_map = {"classes": classes, "slots": slots}
    term_map_body = _json_text(term_map).encode("utf-8")
    identity = {
        "sources": [
            {
                "source_role": source.source_role,
                "resolved_locator": source.resolved_locator,
                "bytes": source.byte_length,
                "sha256": source.sha256,
            }
            for source in closure.sources
        ],
        "imports": [
            {
                "parent_locator": edge.parent_locator,
                "ordinal": edge.ordinal,
                "literal": edge.literal,
                "target_role": edge.target_role,
                "resolved_locator": edge.resolved_locator,
            }
            for edge in closure.imports
        ],
        "definitions": [
            {
                "kind": definition.kind,
                "name": definition.name,
                "source_locator": definition.source_locator,
            }
            for definition in closure.definitions
        ],
        "term_map": _file_identity(term_map_body),
    }
    return _JsonLdOntology(
        classes=classes,
        slots=slots,
        identity=identity,
        source_closure=closure,
        structural_hash=f"sha256:{registry.content_hash()}",
    )


def _assert_jsonld_ontology_current(ontology: _JsonLdOntology) -> None:
    for source in ontology.source_closure.sources:
        path = Path(source.resolved_locator)
        try:
            body = path.read_bytes()
        except OSError as error:
            raise ReconError(
                "Cannot recheck JSON-LD ontology "
                f"{source.source_role} source {source.resolved_locator}: {error}"
            ) from error
        if body != source.source_bytes:
            raise ReconError(
                "JSON-LD ontology "
                f"{source.source_role} source {source.resolved_locator} "
                "changed during generation"
            )


def _ontology_iri(
    name: str,
    terms: Mapping[str, str],
    *,
    kind: str,
) -> str:
    try:
        return terms[name]
    except KeyError as error:
        raise ReconError(
            f"Cannot emit JSON-LD for ontology {kind} without ownership: {name}"
        ) from error


def _record_iri(identifier: Any) -> str:
    if not isinstance(identifier, str) or not identifier.strip():
        raise ReconError("JSON-LD record identifiers must be nonblank strings")
    return "urn:malleus:recon:record:" + quote(identifier, safe="")


def _range_coercion(registry: OntologyRegistry, range_name: str | None) -> str | None:
    if range_name is None:
        return None
    if registry.has_type(range_name):
        return "@id"
    return _SCALAR_COERCIONS.get(range_name)


def _jsonld_context(
    registry: OntologyRegistry,
    record_types: Iterable[str],
    ontology: _JsonLdOntology | None = None,
) -> dict[str, Any]:
    ontology = ontology or _jsonld_ontology(registry)
    ranges: dict[str, set[str | None]] = {}
    for record_type in sorted(set(record_types)):
        if not registry.has_type(record_type):
            raise ReconError(f"Cannot emit JSON-LD for unknown ontology class: {record_type}")
        for slot, constraint in registry.effective_slots(record_type).items():
            if slot != "id":
                ranges.setdefault(slot, set()).add(_range_coercion(registry, constraint.range))

    context: dict[str, Any] = {}
    for slot, coercions in sorted(ranges.items()):
        if len(coercions) != 1:
            raise ReconError(
                f"Cannot emit one JSON-LD term for ontology slot '{slot}' with "
                f"incompatible coercions: {sorted(str(item) for item in coercions)}"
            )
        definition: dict[str, str] = {
            "@id": _ontology_iri(
                slot,
                ontology.slots,
                kind="slot",
            )
        }
        coercion = next(iter(coercions))
        if coercion is not None:
            definition["@type"] = coercion
        context[slot] = definition if len(definition) > 1 else definition["@id"]
    return context


def _jsonld_property_value(
    registry: OntologyRegistry,
    record_type: str,
    slot: str,
    value: Any,
) -> Any:
    constraint = registry.effective_slots(record_type).get(slot)
    if constraint is None:
        raise ReconError(f"{record_type} JSON-LD record contains unknown slot: {slot}")
    if constraint.range is not None and registry.has_type(constraint.range):
        if isinstance(value, list):
            return [_record_iri(item) for item in value]
        return _record_iri(value)
    return value


def _jsonld(
    canonical: Mapping[str, Any],
    registry: OntologyRegistry,
    ontology: _JsonLdOntology | None = None,
) -> dict[str, Any]:
    records = [*canonical["nodes"], *canonical["edges"]]
    ontology = ontology or _jsonld_ontology(registry)
    items = []
    for record in records:
        record_type = record["type"]
        item = {
            "@id": _record_iri(record["id"]),
            "@type": _ontology_iri(
                record_type,
                ontology.classes,
                kind="class",
            ),
        }
        item.update(
            {
                slot: _jsonld_property_value(registry, record_type, slot, value)
                for slot, value in record.items()
                if slot not in {"id", "type"}
            }
        )
        items.append(item)
    return {
        "@context": _jsonld_context(
            registry,
            (record["type"] for record in records),
            ontology,
        ),
        "@graph": items,
    }


def _graphml_bytes(graph: nx.MultiDiGraph) -> bytes:
    generator = nx.generate_graphml(graph, encoding="utf-8", prettyprint=True)
    text = "\n".join(generator) + "\n"
    # Parse before writing so a malformed serializer result never enters build/.
    try:
        ET.fromstring(text.encode("utf-8"))
    except ET.ParseError as error:
        raise ReconError(
            "Cannot generate GraphML: a source value contains an XML-invalid "
            f"character ({error})"
        ) from error
    return text.encode("utf-8")


def _bibtex(records: Mapping[str, StoredRecord]) -> str:
    entries = []
    for stored in sorted(records.values(), key=lambda item: item.record["id"]):
        if stored.record_type != "Work" or stored.record.get("review_state") == "RETIRED":
            continue
        record = stored.record
        key = _bibtex_key(record["id"])
        identifiers = record.get("identifiers", [])
        doi = next((value[4:] for value in identifiers if value.lower().startswith("doi:")), None)
        arxiv = next(
            (value[6:] for value in identifiers if value.lower().startswith("arxiv:")), None
        )
        fields = {
            "title": record["title"],
            "author": " and ".join(record.get("authors", [])),
            "year": record.get("priority_date", "")[:4],
            "venue": record.get("venue", ""),
            "doi": doi or "",
            "eprint": arxiv or "",
        }
        lines = [f"@misc{{{key},"]
        for name, value in fields.items():
            if value:
                lines.append(f"  {name} = {{{_bibtex_escape(value)}}},")
        lines.append("}")
        entries.append("\n".join(lines))
    return "\n\n".join(entries) + ("\n" if entries else "")


def _bibtex_key(value: str) -> str:
    return "work_" + value.encode("utf-8").hex()


def _bibtex_escape(value: str) -> str:
    escaped = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "%": r"\%",
        "&": r"\&",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(escaped.get(character, character) for character in value)


def _markdown_single_line(value: Any) -> str:
    return re.sub(r"[\r\n]+", " ", str(value))


def _markdown_text(value: Any) -> str:
    text = _markdown_single_line(value)
    text = re.sub(r"([\\`*{}\[\]()#+.!_|-])", r"\\\1", text)
    return html.escape(text, quote=False)


def _markdown_code_span(value: Any) -> str:
    text = _markdown_single_line(value).replace("|", r"\|")
    longest_run = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * (longest_run + 1)
    padding = " " if text.startswith(("`", " ")) or text.endswith(("`", " ")) else ""
    return f"{fence}{padding}{text}{padding}{fence}"


def _report(
    project: ReconProject,
    records: Mapping[str, StoredRecord],
    result_metrics: Mapping[str, Any],
    comparisons: Mapping[str, Mapping[str, Any]],
) -> str:
    works = sorted(
        (
            item.record
            for item in records.values()
            if item.record_type == "Work" and item.record.get("review_state") != "RETIRED"
        ),
        key=lambda record: record["id"],
    )
    lines = [
        f"# {_markdown_text(project.config['title'])}",
        "",
        "This report is generated from the current recorded Recon state. Structural recording",
        "does not establish truth, novelty, copying, intent, or paper quality.",
        "",
        "## Inventory",
        "",
        f"- {result_metrics['works']} works",
        f"- {result_metrics['claims']} atomic claims",
        f"- {result_metrics['results']} reported results",
        f"- {result_metrics['axes']} comparison axes",
        f"- {result_metrics['rejections']} rejected candidates preserved in the ledger",
        "",
        "## Works",
        "",
        "| Work | First public date | Status |",
        "|---|---|---|",
    ]
    for work in works:
        lines.append(
            f"| {_markdown_text(work['title'])} ({_markdown_code_span(work['id'])}) | "
            f"{_markdown_text(work.get('priority_date', 'unverified'))} | "
            f"{_markdown_text(work['publication_status'])} |"
        )
    target_id = project.config["target_id"]
    target_profile = _profiles(records).get(target_id, {})
    target_set = sorted(
        axis for axis, level in target_profile.items() if level in MATERIAL_LEVELS
    )
    lines.extend(
        [
            "",
            "## Target material set",
            "",
            ", ".join(_markdown_code_span(axis) for axis in target_set)
            or "None recorded.",
            "",
            "## Claim-level comparison summary",
            "",
            "| Work | Material axes | Shared | Target-only | Work-only | Partial | Unresolved | Unassessed | Contested |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for work in works:
        comparison = comparisons[work["id"]]
        lines.append(
            f"| {_markdown_text(work['title'])} ({_markdown_code_span(work['id'])}) | "
            f"{sum(level in MATERIAL_LEVELS for level in comparison['work_profile'].values())} | "
            f"{len(comparison['intersection'])} | {len(comparison['target_difference'])} | "
            f"{len(comparison['work_difference'])} | "
            f"{len(comparison['partial_or_adjacent'])} | {len(comparison['unresolved'])} | "
            f"{len(comparison['unassessed'])} | {len(comparison['contested'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "The sets above contain only reviewer-coded CENTRAL or MATERIAL axes. A blank",
            "matrix cell means no active assessment is recorded. NOT_ESTABLISHED is an",
            "explicit reviewer-coded assessment, not proof of absence.",
            "Exact per-work sets and unresolved axes are in `comparisons.json` and are",
            "also available through `malleus-recon compare`.",
            "",
        ]
    )
    return "\n".join(lines)


def _write_zip(path: Path, files: Mapping[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, body in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, body, compresslevel=9)


def _file_identity(body: bytes) -> dict[str, Any]:
    return {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}


def _read_generator_identity() -> dict[str, Any]:
    components = []
    for name, path in _IMPLEMENTATION_SOURCES:
        try:
            body = path.read_bytes()
        except OSError as error:
            raise ReconError(
                f"Cannot bind Recon generator implementation source {name}: {error}"
            ) from error
        components.append({"name": name, **_file_identity(body)})
    closure_body = _json_text(
        {
            "schema_version": _GENERATOR_CLOSURE_SCHEMA_VERSION,
            "components": components,
        }
    ).encode("utf-8")
    return {
        **_BUILD_GENERATOR,
        "implementation": {
            "schema_version": _GENERATOR_CLOSURE_SCHEMA_VERSION,
            "components": components,
            "closure": _file_identity(closure_body),
        },
    }


_LOADED_GENERATOR_IDENTITY = _read_generator_identity()


def _generator_identity() -> dict[str, Any]:
    current = _read_generator_identity()
    if current != _LOADED_GENERATOR_IDENTITY:
        raise ReconError(
            "Recon generator implementation sources differ from the code loaded "
            "by this process"
        )
    return deepcopy(_LOADED_GENERATOR_IDENTITY)


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key '{key}'")
        result[key] = value
    return result


def _project_identity(project: ReconProject) -> dict[str, Any]:
    path = project.root / PROJECT_FILE
    try:
        body = path.read_bytes()
        decoded = json.loads(
            body.decode("utf-8"),
            object_pairs_hook=_unique_json_object,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ReconError(f"Cannot bind exact {PROJECT_FILE} bytes: {error}") from error
    if decoded != project.config:
        raise ReconError(
            f"Cannot bind {PROJECT_FILE}: filesystem content differs from the loaded "
            "project configuration"
        )
    return {"name": PROJECT_FILE, **_file_identity(body)}


def _safe_build_name(name: Any) -> str:
    if not isinstance(name, str) or name not in _HISTORICAL_OUTPUT_ALLOWLIST:
        raise ValueError(f"manifest files contains undeclared output name: {name!r}")
    return name


def _exact_manifest_fields(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise ValueError(
            f"{label} fields differ from the v{_BUILD_MANIFEST_SCHEMA_VERSION} "
            "build contract"
        )


def _validate_file_identity(value: Any, label: str, *, named: bool = False) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    expected = {"bytes", "name", "sha256"} if named else {"bytes", "sha256"}
    _exact_manifest_fields(value, expected, label)
    if named and (not isinstance(value["name"], str) or not value["name"]):
        raise ValueError(f"{label}.name must be a nonblank string")
    if not isinstance(value["bytes"], int) or isinstance(value["bytes"], bool):
        raise ValueError(f"{label}.bytes must be an integer")
    if value["bytes"] < 0:
        raise ValueError(f"{label}.bytes must not be negative")
    if not isinstance(value["sha256"], str) or _DIGEST.fullmatch(value["sha256"]) is None:
        raise ValueError(f"{label}.sha256 must be 64 lowercase hex digits")


def _nonblank_manifest_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonblank string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ValueError(f"{label} must be UTF-8 encodable") from error
    return value


def _validate_jsonld_ontology_identity(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("jsonld_ontology must be an object")
    _exact_manifest_fields(
        value,
        {"sources", "imports", "definitions", "term_map"},
        "jsonld_ontology",
    )

    sources = value["sources"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("jsonld_ontology.sources must be a nonempty list")
    locators = []
    for index, source in enumerate(sources):
        label = f"jsonld_ontology.sources[{index}]"
        if not isinstance(source, dict):
            raise ValueError(f"{label} must be an object")
        _exact_manifest_fields(
            source,
            {"source_role", "resolved_locator", "bytes", "sha256"},
            label,
        )
        expected_role = "entry" if index == 0 else "import"
        if source["source_role"] != expected_role:
            raise ValueError(f"{label}.source_role must be {expected_role}")
        locator = _nonblank_manifest_text(
            source["resolved_locator"], f"{label}.resolved_locator"
        )
        if not Path(locator).is_absolute():
            raise ValueError(f"{label}.resolved_locator must be absolute")
        if locator in locators:
            raise ValueError(f"{label}.resolved_locator is duplicated")
        locators.append(locator)
        _validate_file_identity(
            {"bytes": source["bytes"], "sha256": source["sha256"]},
            label,
        )
    if locators[1:] != sorted(locators[1:]):
        raise ValueError("jsonld_ontology imported sources must be locator-sorted")
    locator_set = set(locators)

    imports = value["imports"]
    if not isinstance(imports, list):
        raise ValueError("jsonld_ontology.imports must be a list")
    import_keys = []
    parent_ordinals: dict[str, set[int]] = {}
    for index, edge in enumerate(imports):
        label = f"jsonld_ontology.imports[{index}]"
        if not isinstance(edge, dict):
            raise ValueError(f"{label} must be an object")
        _exact_manifest_fields(
            edge,
            {
                "parent_locator",
                "ordinal",
                "literal",
                "target_role",
                "resolved_locator",
            },
            label,
        )
        parent = _nonblank_manifest_text(
            edge["parent_locator"], f"{label}.parent_locator"
        )
        literal = _nonblank_manifest_text(edge["literal"], f"{label}.literal")
        target = _nonblank_manifest_text(
            edge["resolved_locator"], f"{label}.resolved_locator"
        )
        ordinal = edge["ordinal"]
        if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 0:
            raise ValueError(f"{label}.ordinal must be a nonnegative integer")
        if parent not in locator_set:
            raise ValueError(f"{label}.parent_locator is not a retained source")
        ordinals = parent_ordinals.setdefault(parent, set())
        if ordinal in ordinals:
            raise ValueError(f"{label}.ordinal is duplicated for its parent")
        ordinals.add(ordinal)
        role = edge["target_role"]
        if role == "ontology":
            if target not in locator_set:
                raise ValueError(f"{label} targets an unretained ontology source")
        elif role == "builtin":
            if literal != "linkml:types" or target != "linkml:types":
                raise ValueError(f"{label} names an unsupported builtin import")
        else:
            raise ValueError(f"{label}.target_role must be ontology or builtin")
        import_keys.append((parent, ordinal, literal, role, target))
    if import_keys != sorted(import_keys):
        raise ValueError("jsonld_ontology.imports must be deterministically ordered")
    for parent, ordinals in parent_ordinals.items():
        if ordinals != set(range(len(ordinals))):
            raise ValueError(
                "jsonld_ontology.import ordinals must be contiguous for " + parent
            )
    reachable = {locators[0]}
    changed = True
    while changed:
        changed = False
        for parent, _ordinal, _literal, role, target in import_keys:
            if role == "ontology" and parent in reachable and target not in reachable:
                reachable.add(target)
                changed = True
    if reachable != locator_set:
        raise ValueError(
            "jsonld_ontology.sources contains a source unreachable from the entry"
        )

    definitions = value["definitions"]
    if not isinstance(definitions, list):
        raise ValueError("jsonld_ontology.definitions must be a list")
    definition_keys = []
    claimed = set()
    for index, definition in enumerate(definitions):
        label = f"jsonld_ontology.definitions[{index}]"
        if not isinstance(definition, dict):
            raise ValueError(f"{label} must be an object")
        _exact_manifest_fields(
            definition,
            {"kind", "name", "source_locator"},
            label,
        )
        kind = definition["kind"]
        if kind not in {"type", "enum", "slot", "class"}:
            raise ValueError(f"{label}.kind is unsupported")
        name = _nonblank_manifest_text(definition["name"], f"{label}.name")
        owner = _nonblank_manifest_text(
            definition["source_locator"], f"{label}.source_locator"
        )
        if owner not in locator_set:
            raise ValueError(f"{label}.source_locator is not a retained source")
        claim = (kind, name)
        if claim in claimed:
            raise ValueError(f"{label} duplicates a definition owner")
        claimed.add(claim)
        definition_keys.append((kind, name, owner))
    if definition_keys != sorted(definition_keys):
        raise ValueError("jsonld_ontology.definitions must be deterministically ordered")

    _validate_file_identity(value["term_map"], "jsonld_ontology.term_map")


def _validate_digest_list(value: Any, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a list")
    if not all(
        isinstance(identity, str)
        and identity.startswith("sha256:")
        and _DIGEST.fullmatch(identity[7:]) is not None
        for identity in value
    ):
        raise ValueError(f"{label} must contain only sha256 identities")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} must not contain duplicates")
    return tuple(value)


def _validate_ontology_verification(value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError("ontology_verification must be an object")
    _exact_manifest_fields(
        value,
        {
            "current_ontology_hash",
            "verified_ontology_hashes",
            "grammar_ontology_hashes",
            "migrated_ontology_hashes",
            "receipt_digests",
        },
        "ontology_verification",
    )
    current = value["current_ontology_hash"]
    if (
        not isinstance(current, str)
        or not current.startswith("sha256:")
        or _DIGEST.fullmatch(current[7:]) is None
    ):
        raise ValueError(
            "ontology_verification.current_ontology_hash must be a sha256 identity"
        )
    verified = _validate_digest_list(
        value["verified_ontology_hashes"],
        "ontology_verification.verified_ontology_hashes",
    )
    grammar = _validate_digest_list(
        value["grammar_ontology_hashes"],
        "ontology_verification.grammar_ontology_hashes",
    )
    migrated = _validate_digest_list(
        value["migrated_ontology_hashes"],
        "ontology_verification.migrated_ontology_hashes",
    )
    receipts = _validate_digest_list(
        value["receipt_digests"],
        "ontology_verification.receipt_digests",
    )
    if set(grammar) & set(migrated):
        raise ValueError(
            "ontology_verification identity cannot be both grammar and migration"
        )
    if verified != (*grammar, *migrated):
        raise ValueError(
            "ontology_verification.verified_ontology_hashes must equal grammar "
            "hashes followed by migrated hashes"
        )
    if bool(migrated) != bool(receipts):
        raise ValueError(
            "ontology_verification migrated identities and receipts must coexist"
        )


def _validate_manifest(
    body: bytes,
    expected_generator: Mapping[str, Any],
) -> tuple[dict[str, Any], set[str]]:
    manifest = json.loads(
        body.decode("utf-8"),
        object_pairs_hook=_unique_json_object,
    )
    if not isinstance(manifest, dict):
        raise ValueError("manifest root must be an object")
    _exact_manifest_fields(manifest, set(_MANIFEST_FIELDS), "manifest")
    if manifest["schema_version"] != _BUILD_MANIFEST_SCHEMA_VERSION:
        raise ValueError(f"schema_version must be '{_BUILD_MANIFEST_SCHEMA_VERSION}'")
    if manifest["state"] != "COMMITTED":
        raise ValueError("state must be COMMITTED")
    if manifest["profile"] != STRUCTURAL_CAPTURE_PROFILE:
        raise ValueError("profile does not identify the Recon structural-capture profile")
    if manifest["generator"] != expected_generator:
        raise ValueError("generator does not identify this exact Recon implementation")
    if manifest["runtime"] != _BUILD_RUNTIME:
        raise ValueError("runtime does not identify this Recon build runtime")

    project_identity = manifest["project"]
    _validate_file_identity(project_identity, "project", named=True)
    if project_identity["name"] != PROJECT_FILE:
        raise ValueError(f"project.name must be {PROJECT_FILE}")

    _validate_jsonld_ontology_identity(manifest["jsonld_ontology"])
    _validate_ontology_verification(manifest["ontology_verification"])
    for field in ("ontology_hash", "ledger_head"):
        value = manifest[field]
        if (
            not isinstance(value, str)
            or not value.startswith("sha256:")
            or _DIGEST.fullmatch(value[7:]) is None
        ):
            raise ValueError(f"{field} must be sha256:<64 lowercase hex digits>")
    if (
        manifest["ontology_verification"]["current_ontology_hash"]
        != manifest["ontology_hash"]
    ):
        raise ValueError(
            "ontology_verification.current_ontology_hash differs from ontology_hash"
        )
    event_count = manifest["event_count"]
    if not isinstance(event_count, int) or isinstance(event_count, bool) or event_count < 0:
        raise ValueError("event_count must be a nonnegative integer")

    identities = manifest["files"]
    if not isinstance(identities, dict):
        raise ValueError("files must be an object")
    managed = set()
    for raw_name, identity in identities.items():
        name = _safe_build_name(raw_name)
        _validate_file_identity(identity, f"files.{name}")
        managed.add(name)
    archive = manifest["archive"]
    if not isinstance(archive, dict):
        raise ValueError("archive must be an object")
    _exact_manifest_fields(archive, {"members", "name"}, "archive")
    if archive["name"] != "recon_bundle.zip":
        raise ValueError("archive.name must be recon_bundle.zip")
    if archive["members"] != sorted({*managed, "manifest.json"}):
        raise ValueError("archive.members differs from files")
    return manifest, managed


def _existing_managed_files(
    destination: Path,
    expected_generator: Mapping[str, Any] | None = None,
) -> set[str]:
    manifest_path = destination / "manifest.json"
    if not manifest_path.exists():
        return set()
    if not manifest_path.is_file():
        raise ReconError(f"Existing build manifest is not a file: {manifest_path}")
    try:
        manifest_body = manifest_path.read_bytes()
        manifest, managed = _validate_manifest(
            manifest_body,
            expected_generator or _generator_identity(),
        )
        identities = manifest["files"]
        for name, identity in identities.items():
            path = destination / name
            if not path.is_file():
                raise ValueError(f"managed file is missing: {name}")
            body = path.read_bytes()
            if _file_identity(body) != {
                "bytes": identity["bytes"],
                "sha256": identity["sha256"],
            }:
                raise ValueError(f"managed file identity differs: {name}")
        expected_members = sorted({*managed, "manifest.json"})
        bundle_path = destination / "recon_bundle.zip"
        if not bundle_path.is_file():
            raise ValueError("managed archive is missing: recon_bundle.zip")
        with zipfile.ZipFile(bundle_path, "r") as bundle:
            if bundle.testzip() is not None:
                raise ValueError("managed archive contains a corrupt member")
            if bundle.namelist() != expected_members:
                raise ValueError("managed archive member set differs from files")
            if bundle.read("manifest.json") != manifest_body:
                raise ValueError("managed archive manifest differs from commit marker")
            for name in managed:
                if bundle.read(name) != (destination / name).read_bytes():
                    raise ValueError(f"managed archive member differs: {name}")
        return managed & _HISTORICAL_OUTPUT_ALLOWLIST
    except (
        KeyError,
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        ValueError,
        zipfile.BadZipFile,
    ):
        # Derived output is recoverable. An unverifiable prior build grants no
        # authority to delete stale names, but it does not block regeneration.
        return set()


def _write_staged_file(path: Path, body: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(body)
        stream.flush()
        os.fsync(stream.fileno())


def _verify_staged_build(
    stage: Path,
    files: Mapping[str, bytes],
    expected_generator: Mapping[str, Any],
) -> None:
    for name, expected in files.items():
        if (stage / name).read_bytes() != expected:
            raise ReconError(f"Staged Recon output differs before commit: {name}")
    try:
        _, managed = _validate_manifest(files["manifest.json"], expected_generator)
    except (KeyError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        raise ReconError(
            "Staged Recon manifest violates its "
            f"v{_BUILD_MANIFEST_SCHEMA_VERSION} contract: {error}"
        ) from error
    if managed != set(files) - {"manifest.json"}:
        raise ReconError("Staged Recon manifest file set differs from generated files")
    archive_path = stage / "recon_bundle.zip"
    with zipfile.ZipFile(archive_path, "r") as archive:
        if archive.testzip() is not None:
            raise ReconError("Staged Recon archive contains a corrupt member")
        if archive.namelist() != sorted(files):
            raise ReconError("Staged Recon archive member set differs from its manifest")
        for name, expected in files.items():
            if archive.read(name) != expected:
                raise ReconError(f"Staged Recon archive member differs: {name}")


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        # Python cannot open directory handles for fsync on Windows. Every
        # staged file is flushed before os.replace, and the manifest remains
        # the last atomic replacement, so process failures still fail closed.
        return
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _fsync_file(path: Path) -> None:
    with path.open("r+b") as stream:
        os.fsync(stream.fileno())


def _initialize_build_lock(stream: Any) -> None:
    if os.name == "nt":
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)


def _acquire_build_lock(stream: Any) -> None:
    if os.name == "nt":
        import msvcrt

        msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        return

    import fcntl

    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def _release_build_lock(stream: Any) -> None:
    if os.name == "nt":
        import msvcrt

        stream.seek(0)
        msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        return

    import fcntl

    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _is_lock_contention(error: OSError) -> bool:
    return error.errno in _LOCK_CONTENTION_ERRNOS or getattr(
        error, "winerror", None
    ) in _LOCK_CONTENTION_WINERRORS


@contextmanager
def _exclusive_build(destination: Path) -> Iterator[None]:
    """Serialize one destination's manifest inspection and commit transaction."""

    destination = _canonical_build_destination(destination)
    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise ReconError(
            f"Could not prepare Recon build lock destination {destination}: {error}"
        ) from error
    lock_path = destination / _BUILD_LOCK_NAME
    _precheck_reserved_lock(lock_path, "Recon build lock")
    try:
        descriptor = os.open(
            lock_path,
            os.O_RDWR
            | os.O_CREAT
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
    except OSError as error:
        raise ReconError(f"Could not open Recon build lock {lock_path}: {error}") from error
    try:
        stream = os.fdopen(descriptor, "r+b", closefd=False)
    except (OSError, ValueError) as error:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise ReconError(f"Could not initialize Recon build lock {lock_path}: {error}") from error
    try:
        _assert_reserved_lock_identity(lock_path, descriptor, "Recon build lock")
    except BaseException:
        try:
            stream.close()
        except BaseException:
            pass
        try:
            os.close(descriptor)
        except BaseException:
            pass
        raise

    acquired = False
    body_failed = False
    try:
        try:
            _initialize_build_lock(stream)
        except OSError as error:
            raise ReconError(
                f"Could not initialize Recon build lock {lock_path}: {error}"
            ) from error
        try:
            _acquire_build_lock(stream)
            acquired = True
        except OSError as error:
            if _is_lock_contention(error):
                raise ReconError(
                    f"Recon build destination already has an active builder: {destination}"
                ) from error
            raise ReconError(f"Could not acquire Recon build lock {lock_path}: {error}") from error
        _assert_reserved_lock_identity(lock_path, descriptor, "Recon build lock")
        yield
    except BaseException:
        body_failed = True
        raise
    finally:
        cleanup_interrupt = None
        if acquired:
            try:
                _release_build_lock(stream)
            except Exception:
                # Closing the descriptor remains the final lock-release guard.
                pass
            except BaseException as error:
                cleanup_interrupt = error
        try:
            stream.close()
        except Exception:
            pass
        except BaseException as error:
            if cleanup_interrupt is None:
                cleanup_interrupt = error
        try:
            os.close(descriptor)
        except Exception:
            pass
        except BaseException as error:
            if cleanup_interrupt is None:
                cleanup_interrupt = error
        if not body_failed and cleanup_interrupt is not None:
            raise cleanup_interrupt


def _canonical_build_destination(destination: Path) -> Path:
    try:
        return destination.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise ReconError(f"Could not resolve Recon build destination {destination}: {error}") from error


def _commit_build(
    destination: Path,
    files: Mapping[str, bytes],
    expected_generator: Mapping[str, Any],
) -> dict[str, Path]:
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        previous = _existing_managed_files(destination, expected_generator)
        destination.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(
            prefix=".recon.", suffix=".staging", dir=destination
        )
        try:
            stage = Path(temporary.name)
            for name, body in sorted(files.items()):
                _write_staged_file(stage / name, body)
            bundle = stage / "recon_bundle.zip"
            _write_zip(bundle, files)
            _fsync_file(bundle)
            _verify_staged_build(stage, files, expected_generator)

            manifest_path = destination / "manifest.json"
            manifest_path.unlink(missing_ok=True)
            _fsync_directory(destination)
            try:
                for name in sorted(set(files) - {"manifest.json"}):
                    (stage / name).replace(destination / name)
                bundle.replace(destination / bundle.name)
                for stale in sorted(previous - set(files)):
                    (destination / stale).unlink(missing_ok=True)
                _fsync_directory(destination)
                (stage / "manifest.json").replace(manifest_path)
                _fsync_directory(destination)
            except BaseException:
                rollback_error = None
                try:
                    manifest_path.unlink(missing_ok=True)
                    _fsync_directory(destination)
                except BaseException as failure:
                    rollback_error = failure
                if rollback_error is not None:
                    try:
                        marker_remains = manifest_path.exists()
                    except OSError:
                        marker_remains = True
                    if marker_remains:
                        raise ReconError(
                            "Recon build outcome is indeterminate: manifest.json remains "
                            "after publication and rollback both failed"
                        )
                raise
        except BaseException:
            try:
                temporary.cleanup()
            except BaseException:
                pass
            raise
        try:
            temporary.cleanup()
        except Exception:
            # The manifest is already replaced and directory-synced. Staging
            # cleanup is maintenance now, not part of commit success.
            pass
    except OSError as error:
        if error.errno == errno.EXDEV:
            raise ReconError(
                "Could not commit Recon build: staging and destination must be on "
                "the same filesystem"
            ) from error
        raise ReconError(f"Could not commit Recon build without a torn manifest: {error}") from error
    except zipfile.BadZipFile as error:
        raise ReconError(f"Could not commit Recon build without a torn manifest: {error}") from error
    return {
        name: destination / name
        for name in sorted({*files, "recon_bundle.zip"})
    }


def build_outputs(
    project: ReconProject,
    output_directory: str | Path | None = None,
) -> dict[str, Path]:
    requested = Path(output_directory or project.root / BUILD_DIRECTORY)
    destination = _canonical_build_destination(requested)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise ReconError(f"Could not prepare Recon build destination {destination}: {error}") from error
    with _exclusive_build(destination):
        return _build_outputs_locked(project, destination)


def _build_outputs_locked(
    project: ReconProject,
    destination: Path,
) -> dict[str, Path]:
    events, records, ontology_verification = project.snapshot_verified()
    project_identity = _project_identity(project)
    generator_identity = _generator_identity()
    jsonld_ontology = _jsonld_ontology(project.registry)
    if jsonld_ontology.structural_hash != project.ontology_hash:
        raise ReconError(
            "Recon JSON-LD ontology snapshot does not match the project's active "
            "ontology identity"
        )
    canonical = _canonical_snapshot(project, events, records)
    graph = _networkx_graph(canonical)
    result_metrics = _metrics_snapshot(project, events, records)
    matrix_columns, matrix_rows = _matrix(project, records)
    works = sorted(
        identifier
        for identifier, stored in records.items()
        if stored.record_type == "Work" and stored.record.get("review_state") != "RETIRED"
    )
    comparisons = {
        work_id: _compare_subjects(
            project,
            records,
            project.config["target_id"],
            work_id,
        )
        for work_id in works
    }
    evidence_rows = [
        node for node in canonical["nodes"] if node["type"] == "EvidenceAttachment"
    ]
    files: dict[str, bytes] = {
        "literature_kg.json": _json_text(canonical).encode("utf-8"),
        "literature_kg.jsonld": _json_text(
            _jsonld(canonical, project.registry, jsonld_ontology)
        ).encode("utf-8"),
        "literature_kg.graphml": _graphml_bytes(graph),
        "nodes.csv": _csv_text(_NODE_COLUMNS, canonical["nodes"]).encode("utf-8"),
        "edges.csv": _csv_text(_EDGE_COLUMNS, canonical["edges"]).encode("utf-8"),
        "evidence.csv": _csv_text(
            (
                "id",
                "label",
                "source_uri",
                "local_path",
                "locator",
                "source_class",
                "accessed_on",
                "access_status",
                "artifact_sha256",
                "artifact_byte_length",
            ),
            evidence_rows,
        ).encode("utf-8"),
        "work_axis_matrix.csv": _csv_text(matrix_columns, matrix_rows).encode("utf-8"),
        "bibliography.bib": _bibtex(records).encode("utf-8"),
        "comparisons.json": _json_text(comparisons).encode("utf-8"),
        "metrics.json": _json_text(result_metrics).encode("utf-8"),
        "report.md": _report(
            project,
            records,
            result_metrics,
            comparisons,
        ).encode("utf-8"),
    }
    if not set(files) <= _HISTORICAL_OUTPUT_ALLOWLIST:
        raise ReconError("Recon generated-output set differs from its deletion allowlist")
    manifest = {
        "schema_version": _BUILD_MANIFEST_SCHEMA_VERSION,
        "state": "COMMITTED",
        "profile": STRUCTURAL_CAPTURE_PROFILE,
        "generator": deepcopy(generator_identity),
        "runtime": dict(_BUILD_RUNTIME),
        "project": project_identity,
        "jsonld_ontology": deepcopy(jsonld_ontology.identity),
        "ontology_verification": {
            "current_ontology_hash": ontology_verification.current_ontology_hash,
            "verified_ontology_hashes": list(
                ontology_verification.verified_ontology_hashes
            ),
            "grammar_ontology_hashes": list(
                ontology_verification.grammar_ontology_hashes
            ),
            "migrated_ontology_hashes": list(
                ontology_verification.migrated_ontology_hashes
            ),
            "receipt_digests": list(ontology_verification.receipt_digests),
        },
        "ontology_hash": project.ontology_hash,
        "ledger_head": canonical["meta"]["ledger_head"],
        "event_count": canonical["meta"]["event_count"],
        "files": {
            name: _file_identity(body)
            for name, body in sorted(files.items())
        },
        "archive": {
            "name": "recon_bundle.zip",
            "members": sorted({*files, "manifest.json"}),
        },
    }
    files["manifest.json"] = _json_text(manifest).encode("utf-8")
    if _project_identity(project) != project_identity:
        raise ReconError(f"Cannot commit Recon build: {PROJECT_FILE} changed during generation")
    if _generator_identity() != generator_identity:
        raise ReconError("Cannot commit Recon build: generator implementation changed during generation")
    _assert_jsonld_ontology_current(jsonld_ontology)
    return _commit_build(destination, files, generator_identity)


def visualize(
    project: ReconProject,
    output_path: str | Path | None = None,
) -> Path:
    try:
        from pyvis.network import Network
    except ImportError as error:
        raise ReconError(
            'Interactive visualization requires: pip install "malleus-dev[recon]"'
        ) from error
    graph = current_graph(project)
    network = Network(height="850px", width="100%", directed=True, notebook=False)
    network.from_nx(graph)
    network.set_options(
        json.dumps(
            {
                "layout": {"improvedLayout": True, "randomSeed": 17},
                "physics": {"stabilization": {"iterations": 200}},
                "interaction": {"hover": True, "navigationButtons": True},
            }
        )
    )
    destination = Path(output_path or project.root / BUILD_DIRECTORY / "literature_kg.html")
    destination.parent.mkdir(parents=True, exist_ok=True)
    network.write_html(str(destination), open_browser=False, notebook=False)
    return destination
