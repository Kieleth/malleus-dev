"""Deterministic graph, matrix, comparison, and report generation."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import zipfile
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping
from xml.etree import ElementTree as ET

import networkx as nx

from malleus.ledger import GENESIS
from malleus.recon.store import BUILD_DIRECTORY, ReconError, ReconProject, StoredRecord


MATERIAL_LEVELS = frozenset({"CENTRAL", "MATERIAL"})
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
    profiles: dict[str, dict[str, str]] = {}
    for stored in records.values():
        if stored.record_type != "CoversAxisRelation":
            continue
        record = stored.record
        if record.get("review_state") != "REVIEWED":
            continue
        profiles.setdefault(record["source_id"], {})[record["target_id"]] = record[
            "coverage_level"
        ]
    return profiles


def _contested_profiles(
    records: Mapping[str, StoredRecord],
) -> dict[str, dict[str, str]]:
    profiles: dict[str, dict[str, str]] = {}
    for stored in records.values():
        if stored.record_type != "CoversAxisRelation":
            continue
        record = stored.record
        if record.get("review_state") != "CONTESTED":
            continue
        profiles.setdefault(record["source_id"], {})[record["target_id"]] = record[
            "coverage_level"
        ]
    return profiles


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
    unresolved = {
        axis: {
            "target": target_profile.get(axis, "NOT_ESTABLISHED"),
            "work": work_profile.get(axis, "NOT_ESTABLISHED"),
        }
        for axis in all_axes
        if target_profile.get(axis, "NOT_ESTABLISHED")
        in {"NOT_ESTABLISHED", "CONTRADICTED"}
        or work_profile.get(axis, "NOT_ESTABLISHED")
        in {"NOT_ESTABLISHED", "CONTRADICTED"}
    }
    partial = {
        axis: {
            "target": target_profile.get(axis, "NOT_ESTABLISHED"),
            "work": work_profile.get(axis, "NOT_ESTABLISHED"),
        }
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
            "this is not a novelty verdict."
        ),
    }


def metrics(project: ReconProject) -> dict[str, Any]:
    events, records = project.snapshot()
    canonical = _canonical_snapshot(project, events, records)
    return _metrics_snapshot(project, events, records, _networkx_graph(canonical))


def _metrics_snapshot(
    project: ReconProject,
    events: list[dict[str, Any]],
    records: Mapping[str, StoredRecord],
    graph: nx.MultiDiGraph,
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
    undirected = nx.Graph(graph.subgraph(active_node_ids))
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


def _jsonld(canonical: Mapping[str, Any]) -> dict[str, Any]:
    items = []
    for node in canonical["nodes"]:
        items.append({"@id": node["id"], "@type": f"recon:{node['type']}", **{
            key: value for key, value in node.items() if key not in {"id", "type"}
        }})
    for edge in canonical["edges"]:
        items.append({
            "@id": edge["id"],
            "@type": f"recon:{edge['type']}",
            "source": {"@id": edge["source_id"]},
            "target": {"@id": edge["target_id"]},
            **{
                key: value
                for key, value in edge.items()
                if key not in {"id", "type", "source_id", "target_id"}
            },
        })
    return {
        "@context": {
            "@vocab": "https://malleus.dev/schema/recon/",
            "recon": "https://malleus.dev/schema/recon/",
            "source": {"@id": "recon:source", "@type": "@id"},
            "target": {"@id": "recon:target", "@type": "@id"},
        },
        "@graph": items,
    }


def _graphml_bytes(graph: nx.MultiDiGraph) -> bytes:
    generator = nx.generate_graphml(graph, encoding="utf-8", prettyprint=True)
    text = "\n".join(generator) + "\n"
    # Parse before writing so a malformed serializer result never enters build/.
    ET.fromstring(text.encode("utf-8"))
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
    cleaned = "".join(
        character if character.isalnum() else "_" for character in value
    ).strip("_")
    return cleaned or "work_" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def _bibtex_escape(value: str) -> str:
    return (
        value.replace("\\", "\\textbackslash{}")
        .replace("{", "\\{")
        .replace("}", "\\}")
    )


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
        f"# {project.config['title']}",
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
            f"| {work['title']} (`{work['id']}`) | "
            f"{work.get('priority_date', 'unverified')} | "
            f"{work['publication_status']} |"
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
            ", ".join(target_set) or "None recorded.",
            "",
            "## Claim-level comparison summary",
            "",
            "| Work | Material axes | Shared | Target-only | Work-only | Partial | Unresolved | Contested |",
            "|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for work in works:
        comparison = comparisons[work["id"]]
        lines.append(
            f"| {work['title']} (`{work['id']}`) | "
            f"{sum(level in MATERIAL_LEVELS for level in comparison['work_profile'].values())} | "
            f"{len(comparison['intersection'])} | {len(comparison['target_difference'])} | "
            f"{len(comparison['work_difference'])} | "
            f"{len(comparison['partial_or_adjacent'])} | {len(comparison['unresolved'])} | "
            f"{len(comparison['contested'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "The sets above contain only reviewer-coded CENTRAL or MATERIAL axes. Missing",
            "coverage means not established in the recorded review, not proof of absence.",
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
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, body)


def build_outputs(
    project: ReconProject,
    output_directory: str | Path | None = None,
) -> dict[str, Path]:
    events, records = project.snapshot()
    canonical = _canonical_snapshot(project, events, records)
    graph = _networkx_graph(canonical)
    result_metrics = _metrics_snapshot(project, events, records, graph)
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
        "literature_kg.jsonld": _json_text(_jsonld(canonical)).encode("utf-8"),
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
    manifest = {
        "schema_version": "1",
        "ontology_hash": project.ontology_hash,
        "ledger_head": canonical["meta"]["ledger_head"],
        "files": {
            name: {
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
            }
            for name, body in sorted(files.items())
        },
    }
    files["manifest.json"] = _json_text(manifest).encode("utf-8")
    destination = Path(output_directory or project.root / BUILD_DIRECTORY)
    destination.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, body in sorted(files.items()):
        path = destination / name
        path.write_bytes(body)
        paths[name] = path
    bundle = destination / "recon_bundle.zip"
    _write_zip(bundle, files)
    paths[bundle.name] = bundle
    return paths


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
