"""Strict adapter for the literature-forensics graph schema version 1.x."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from malleus.ledger import canonical_json
from malleus.recon.store import ReconError, ReconProject, RecordCandidate


_WORK_TYPES = frozenset(
    {
        "paper",
        "project",
        "software",
        "standard",
        "ontology",
        "ontology_inventory_entry",
        "dataset",
    }
)
_NODE_TYPES = {**{name: "Work" for name in _WORK_TYPES}, "claim": "Claim", "result": "Result", "concept": "ComparisonAxis"}
_SOURCE_CLASSES = {
    "publisher": "PUBLISHER",
    "preprint": "PREPRINT",
    "author_copy": "AUTHOR_COPY",
    "standard": "STANDARD",
    "project_documentation": "PROJECT_DOCUMENTATION",
    "repository": "REPOSITORY",
    "dataset": "DATASET",
    "patent": "PATENT",
    "index": "INDEX",
    "other": "OTHER",
}
_PUBLICATION_STATUS = {
    "peer_reviewed": "PEER_REVIEWED",
    "accepted": "ACCEPTED",
    "preprint": "PREPRINT",
    "standard": "STANDARD",
    "documentation": "DOCUMENTATION",
    "software": "SOFTWARE",
    "patent": "PATENT",
    "unknown": "UNKNOWN",
}
_ASSERTION_STATUS = {
    "source_explicit": "SOURCE_EXPLICIT",
    "reviewer_inference": "REVIEWER_INFERENCE",
    "negative_bibliography_audit": "NEGATIVE_AUDIT",
}
_WORK_RELATIONS = {
    "cites": ("CitesRelation", "CITES"),
    "complements": ("ComplementsRelation", "COMPLEMENTS"),
    "contrasts_with": ("ContrastsWithRelation", "CONTRASTS_WITH"),
    "depends_on": ("DependsOnRelation", "DEPENDS_ON"),
    "evaluates_on": ("EvaluatesOnRelation", "EVALUATES_ON"),
    "extends": ("ExtendsRelation", "EXTENDS"),
    "implements": ("ImplementsRelation", "IMPLEMENTS"),
    "omits_relevant_citation_to": (
        "OmitsRelevantCitationRelation",
        "OMITS_RELEVANT_CITATION_TO",
    ),
    "precedes": ("PrecedesRelation", "PRECEDES"),
    "simultaneous_with": ("SimultaneousWithRelation", "SIMULTANEOUS_WITH"),
    "substantially_overlaps_with": (
        "SubstantiallyOverlapsWithRelation",
        "SUBSTANTIALLY_OVERLAPS_WITH",
    ),
    "surveys": ("SurveysRelation", "SURVEYS"),
    "uses": ("UsesRelation", "USES"),
}


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value = {}
    for key, item in pairs:
        if key in value:
            raise ReconError(f"duplicate JSON key '{key}' in imported graph")
        value[key] = item
    return value


def _required(mapping: Mapping[str, Any], key: str, context: str) -> Any:
    if key not in mapping:
        raise ReconError(f"{context} is missing required field '{key}'")
    value = mapping[key]
    if value is None or value == "" or value == []:
        raise ReconError(f"{context} field '{key}' must not be empty")
    return value


def _required_string(mapping: Mapping[str, Any], key: str, context: str) -> str:
    value = _required(mapping, key, context)
    if not isinstance(value, str) or not value.strip():
        raise ReconError(f"{context} field '{key}' must be a nonblank string")
    return value


def _list_of_strings(value: Any, context: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ReconError(f"{context} must be a list of strings")
    return list(value)


def _evidence_key(evidence: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(evidence).encode("utf-8")).hexdigest()


def _coverage_level(strength: Any, maturity: str | None) -> str:
    if maturity == "UNRESOLVED":
        return "NOT_ESTABLISHED"
    if maturity == "CONTRADICTED":
        return "CONTRADICTED"
    mapping = {3: "CENTRAL", 2: "MATERIAL", 1: "PARTIAL", 0: "NOT_ESTABLISHED"}
    if not isinstance(strength, int) or isinstance(strength, bool) or strength not in mapping:
        raise ReconError(f"legacy comparison strength must be 0, 1, 2, or 3, got {strength!r}")
    return mapping[strength]


class LiteratureV1Importer:
    """Translate one canonical v1 graph without silently dropping a record."""

    def __init__(self, project: ReconProject, source_path: str | Path):
        self.project = project
        self.path = Path(source_path)
        try:
            self.source_bytes = self.path.read_bytes()
            self.graph = json.loads(
                self.source_bytes.decode("utf-8"), object_pairs_hook=_unique_object
            )
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ReconError(f"Cannot read legacy literature graph {self.path}: {error}") from error
        if not isinstance(self.graph, dict):
            raise ReconError("Legacy literature graph must be one JSON object")
        self.meta = _required(self.graph, "meta", "legacy graph")
        self.nodes = _required(self.graph, "nodes", "legacy graph")
        self.edges = _required(self.graph, "edges", "legacy graph")
        if not isinstance(self.meta, dict) or not isinstance(self.nodes, list) or not isinstance(self.edges, list):
            raise ReconError("Legacy graph meta must be an object and nodes/edges must be lists")
        self.version = _required_string(self.meta, "version", "legacy graph meta")
        if not self.version.startswith("1."):
            raise ReconError(
                f"Legacy importer accepts schema 1.x, got version '{self.version}'"
            )
        self.as_of = _required_string(self.meta, "as_of", "legacy graph meta")
        self.source_hash = hashlib.sha256(self.source_bytes).hexdigest()
        self.node_index = self._index_nodes()
        self.edge_ids = self._validate_edges()
        self.evidence_records: dict[str, dict[str, Any]] = {}
        self.unknown_source_classes: Counter[str] = Counter()

    def _index_nodes(self) -> dict[str, dict[str, Any]]:
        result = {}
        for position, node in enumerate(self.nodes, start=1):
            context = f"legacy node {position}"
            if not isinstance(node, dict):
                raise ReconError(f"{context} must be an object")
            identifier = _required_string(node, "id", context)
            if identifier in result:
                raise ReconError(f"duplicate legacy node id '{identifier}'")
            node_type = _required_string(node, "type", context)
            if node_type not in _NODE_TYPES:
                raise ReconError(f"{context} has unsupported type '{node_type}'")
            result[identifier] = node
        return result

    def _validate_edges(self) -> set[str]:
        identifiers = set()
        for position, edge in enumerate(self.edges, start=1):
            context = f"legacy edge {position}"
            if not isinstance(edge, dict):
                raise ReconError(f"{context} must be an object")
            identifier = _required_string(edge, "id", context)
            if identifier in identifiers or identifier in self.node_index:
                raise ReconError(f"duplicate legacy graph identifier '{identifier}'")
            identifiers.add(identifier)
            for role in ("source", "target"):
                endpoint = _required_string(edge, role, context)
                if endpoint not in self.node_index:
                    raise ReconError(
                        f"{context} {role} '{endpoint}' does not name a legacy node"
                    )
        return identifiers

    def _evidence_ids(self, owner: Mapping[str, Any], context: str) -> list[str]:
        evidence_items = _required(owner, "evidence", context)
        if not isinstance(evidence_items, list):
            raise ReconError(f"{context} evidence must be a list")
        identifiers = []
        for position, evidence in enumerate(evidence_items, start=1):
            evidence_context = f"{context} evidence {position}"
            if not isinstance(evidence, dict):
                raise ReconError(f"{evidence_context} must be an object")
            url = _required_string(evidence, "url", evidence_context)
            locator = _required_string(evidence, "locator", evidence_context)
            description = _required_string(evidence, "description", evidence_context)
            source_class_raw = _required_string(
                evidence, "source_class", evidence_context
            ).lower()
            accessed = _required_string(evidence, "accessed", evidence_context)
            source_class = _SOURCE_CLASSES.get(source_class_raw)
            notes = [
                "Imported from literature graph v1, whose attachment schema did not "
                "encode an independent access-status field."
            ]
            if source_class is None:
                source_class = "OTHER"
                self.unknown_source_classes[source_class_raw] += 1
                notes.append(f"Legacy source_class: {source_class_raw}")
            normalized = {
                "url": url,
                "locator": locator,
                "description": description,
                "source_class": source_class_raw,
                "accessed": accessed,
            }
            digest = _evidence_key(normalized)
            identifier = f"evidence:legacy:{digest}"
            record = {
                "id": identifier,
                "label": description,
                "review_state": "REVIEWED",
                "source_uri": url,
                "locator": locator,
                "evidence_description": description,
                "source_class": source_class,
                "accessed_on": accessed,
                "access_status": "UNVERIFIED",
                "notes": notes,
            }
            prior = self.evidence_records.get(identifier)
            if prior is not None and prior != record:
                raise ReconError(f"evidence digest collision at '{identifier}'")
            self.evidence_records[identifier] = record
            identifiers.append(identifier)
        return sorted(set(identifiers))

    def _work(self, node: Mapping[str, Any]) -> dict[str, Any]:
        identifier = node["id"]
        context = f"legacy work '{identifier}'"
        status_raw = _required_string(node, "peer_review_status", context).lower()
        if status_raw not in _PUBLICATION_STATUS:
            raise ReconError(f"{context} has unsupported peer_review_status '{status_raw}'")
        identifiers = _required(node, "identifiers", context)
        if not isinstance(identifiers, dict) or any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in identifiers.items()
        ):
            raise ReconError(f"{context} identifiers must be a string-to-string object")
        record = {
            "id": identifier,
            "label": _required_string(node, "label", context),
            "title": _required_string(node, "title", context),
            "priority_date_basis": _required_string(node, "priority_date_basis", context),
            "publication_status": _PUBLICATION_STATUS[status_raw],
            "review_state": "REVIEWED",
            "evidence_ids": self._evidence_ids(node, context),
        }
        if node.get("authors") is not None:
            record["authors"] = _list_of_strings(node["authors"], f"{context} authors")
        if node.get("venue"):
            record["venue"] = node["venue"]
        if identifiers:
            record["identifiers"] = [
                f"{key}:{value}" for key, value in sorted(identifiers.items())
            ]
        if node.get("priority_date"):
            record["priority_date"] = node["priority_date"]
        if node.get("summary"):
            record["description"] = node["summary"]
        notes = list(node.get("notes", []))
        if node.get("set_comparison_note"):
            notes.append(f"Set comparison note: {node['set_comparison_note']}")
        if node.get("dates"):
            notes.append(
                "Legacy date records: "
                + json.dumps(node["dates"], ensure_ascii=False, sort_keys=True)
            )
        if notes:
            record["notes"] = _list_of_strings(notes, f"{context} notes")
        return record

    def _claim_or_result(self, node: Mapping[str, Any], record_type: str) -> dict[str, Any]:
        identifier = node["id"]
        context = f"legacy {record_type.lower()} '{identifier}'"
        kind_field = "claim_kind" if record_type == "Claim" else "result_kind"
        record = {
            "id": identifier,
            "label": _required_string(node, "label", context),
            "statement": _required_string(
                node,
                "text" if "text" in node else "summary",
                context,
            ),
            kind_field: _required_string(node, kind_field, context),
            "review_state": "REVIEWED",
            "evidence_ids": self._evidence_ids(node, context),
        }
        if node.get("confidence") is not None:
            record["confidence"] = node["confidence"]
        if node.get("notes"):
            record["notes"] = _list_of_strings(node["notes"], f"{context} notes")
        return record

    @staticmethod
    def _axis(node: Mapping[str, Any]) -> dict[str, Any]:
        context = f"legacy concept '{node['id']}'"
        record = {
            "id": node["id"],
            "label": _required_string(node, "label", context),
            "axis_definition": _required_string(node, "summary", context),
            "review_state": "REVIEWED",
        }
        if node.get("comparison_code"):
            record["axis_code"] = node["comparison_code"]
        if node.get("comparison_scope"):
            record["axis_scope"] = node["comparison_scope"]
        return record

    def _relation_base(
        self,
        edge: Mapping[str, Any],
        record_type_value: str,
        *,
        basis: str | None = None,
        evidence_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        context = f"legacy edge '{edge['id']}'"
        assertion_raw = _required_string(edge, "assertion_status", context)
        if assertion_raw not in _ASSERTION_STATUS:
            raise ReconError(f"{context} has unsupported assertion_status '{assertion_raw}'")
        confidence = _required(edge, "confidence", context)
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
            raise ReconError(f"{context} confidence must be a number")
        notes = list(edge.get("review_notes", []))
        if edge.get("dimensions"):
            notes.append("Legacy dimensions: " + ", ".join(edge["dimensions"]))
        if edge.get("symmetric"):
            notes.append("Legacy relation declared symmetric.")
        for field in ("absence_confidence", "relevance_confidence"):
            if edge.get(field) is not None:
                notes.append(f"Legacy {field}: {edge[field]}")
        record = {
            "id": edge["id"],
            "source_id": edge["source"],
            "target_id": edge["target"],
            "relation_type": record_type_value,
            "review_state": "REVIEWED",
            "assertion_status": _ASSERTION_STATUS[assertion_raw],
            "confidence": confidence,
            "basis": basis or _required_string(edge, "basis", context),
            "evidence_ids": evidence_ids or self._evidence_ids(edge, context),
        }
        if notes:
            record["notes"] = _list_of_strings(notes, f"{context} notes")
        return record

    def _profile_relation(
        self,
        edge: Mapping[str, Any],
        source_node: Mapping[str, Any],
    ) -> RecordCandidate:
        axis_id = edge["target"]
        profile = source_node.get("set_profile", {}).get(axis_id)
        if profile is not None:
            if not isinstance(profile, dict):
                raise ReconError(
                    f"legacy work '{source_node['id']}' set_profile '{axis_id}' must be an object"
                )
            strength = _required(profile, "strength", f"set profile '{source_node['id']}'")
            maturity = _required_string(
                profile, "maturity", f"set profile '{source_node['id']}'"
            )
            basis = _required_string(
                profile, "basis", f"set profile '{source_node['id']}'"
            )
        else:
            scores = _required(source_node, "concept_scores", f"legacy work '{source_node['id']}'")
            if not isinstance(scores, dict) or axis_id not in scores:
                raise ReconError(
                    f"legacy work '{source_node['id']}' lacks a score for edge axis '{axis_id}'"
                )
            strength = scores[axis_id]
            maturity = None
            basis = _required_string(edge, "basis", f"legacy edge '{edge['id']}'")
        record = self._relation_base(edge, "COVERS_AXIS", basis=basis)
        record["coverage_level"] = _coverage_level(strength, maturity)
        if maturity:
            record["coverage_maturity"] = maturity
        return RecordCandidate("CoversAxisRelation", record)

    def _mapped_relation(self, edge: Mapping[str, Any]) -> RecordCandidate | None:
        relation = _required_string(edge, "relation", f"legacy edge '{edge['id']}'")
        source_node = self.node_index[edge["source"]]
        target_node = self.node_index[edge["target"]]
        source_type = _NODE_TYPES[source_node["type"]]
        target_type = _NODE_TYPES[target_node["type"]]
        if relation == "about_concept":
            if target_type != "ComparisonAxis":
                return None
            if source_type == "Work":
                return self._profile_relation(edge, source_node)
            if source_type == "Claim":
                return RecordCandidate(
                    "ClaimAboutAxisRelation",
                    self._relation_base(edge, "CLAIM_ABOUT_AXIS"),
                )
            if source_type == "Result":
                return RecordCandidate(
                    "ResultAboutAxisRelation",
                    self._relation_base(edge, "RESULT_ABOUT_AXIS"),
                )
            return None
        if relation == "has_claim" and (source_type, target_type) == ("Work", "Claim"):
            return RecordCandidate(
                "HasClaimRelation", self._relation_base(edge, "HAS_CLAIM")
            )
        if relation == "has_result" and (source_type, target_type) == ("Work", "Result"):
            return RecordCandidate(
                "HasResultRelation", self._relation_base(edge, "HAS_RESULT")
            )
        if relation == "explicitly_builds_on":
            if (source_type, target_type) == ("Work", "Work"):
                return RecordCandidate(
                    "ExplicitlyBuildsOnRelation",
                    self._relation_base(edge, "EXPLICITLY_BUILDS_ON"),
                )
            if (source_type, target_type) == ("Claim", "Claim"):
                return RecordCandidate(
                    "ClaimBuildsOnRelation",
                    self._relation_base(edge, "CLAIM_BUILDS_ON"),
                )
        if relation == "compares_to":
            if (source_type, target_type) == ("Work", "Work"):
                return RecordCandidate(
                    "WorkComparesToRelation",
                    self._relation_base(edge, "WORK_COMPARES_TO"),
                )
            if (source_type, target_type) == ("Claim", "Claim"):
                return RecordCandidate(
                    "ClaimComparesToRelation",
                    self._relation_base(edge, "CLAIM_COMPARES_TO"),
                )
        if relation == "qualifies":
            if (source_type, target_type) == ("Claim", "Claim"):
                return RecordCandidate(
                    "QualifiesClaimRelation",
                    self._relation_base(edge, "QUALIFIES_CLAIM"),
                )
            if (source_type, target_type) == ("Work", "Work"):
                return RecordCandidate(
                    "QualifiesWorkRelation",
                    self._relation_base(edge, "QUALIFIES_WORK"),
                )
            if (source_type, target_type) == ("Work", "Claim"):
                return RecordCandidate(
                    "WorkQualifiesClaimRelation",
                    self._relation_base(edge, "WORK_QUALIFIES_CLAIM"),
                )
        if relation == "possible_prior_art_for" and (source_type, target_type) == (
            "Claim",
            "Claim",
        ):
            return RecordCandidate(
                "PossiblePriorArtForRelation",
                self._relation_base(edge, "POSSIBLE_PRIOR_ART_FOR"),
            )
        if relation == "supports" and (source_type, target_type) == ("Result", "Claim"):
            return RecordCandidate(
                "SupportsClaimRelation",
                self._relation_base(edge, "SUPPORTS_CLAIM"),
            )
        if relation in _WORK_RELATIONS and (source_type, target_type) == ("Work", "Work"):
            record_type, relation_type = _WORK_RELATIONS[relation]
            return RecordCandidate(record_type, self._relation_base(edge, relation_type))
        return None

    def plan(self, *, allow_unmapped: bool = False) -> tuple[list[RecordCandidate], dict[str, Any]]:
        self.evidence_records = {}
        self.unknown_source_classes = Counter()
        if self.project.events():
            raise ReconError("Legacy import requires an empty Recon ledger")
        if self.project.config["target_id"] in self.node_index:
            raise ReconError(
                "Project target_id collides with a legacy node; choose a distinct ReviewTarget id"
            )
        comparison = _required(self.meta, "set_comparison", "legacy graph meta")
        if not isinstance(comparison, dict):
            raise ReconError("legacy graph meta set_comparison must be an object")
        source_target_id = _required_string(
            comparison, "target_paper_id", "legacy set_comparison"
        )
        source_target = self.node_index.get(source_target_id)
        if source_target is None:
            raise ReconError(f"legacy set comparison target '{source_target_id}' is missing")
        target_profile = _required(source_target, "set_profile", f"legacy target '{source_target_id}'")
        if not isinstance(target_profile, dict):
            raise ReconError(f"legacy target '{source_target_id}' set_profile must be an object")

        node_candidates = []
        for node in sorted(self.nodes, key=lambda item: item["id"]):
            mapped = _NODE_TYPES[node["type"]]
            if mapped == "Work":
                record = self._work(node)
            elif mapped in {"Claim", "Result"}:
                record = self._claim_or_result(node, mapped)
            else:
                record = self._axis(node)
            node_candidates.append(RecordCandidate(mapped, record))

        target_evidence = self._evidence_ids(
            source_target, f"legacy target '{source_target_id}'"
        )
        target_record = {
            "id": self.project.config["target_id"],
            "label": source_target["label"],
            "scope": _required_string(
                source_target,
                "text" if "text" in source_target else "summary",
                f"legacy target '{source_target_id}'",
            ),
            "cutoff_date": self.as_of,
            "review_method": _required_string(self.meta, "method", "legacy graph meta"),
            "review_state": "REVIEWED",
            "evidence_ids": target_evidence,
            "notes": [
                f"Imported comparison target from legacy node {source_target_id}.",
                "This ReviewTarget is separate from the imported atomic claim node.",
            ],
        }
        node_candidates.append(RecordCandidate("ReviewTarget", target_record))
        target_confidence = _required(
            source_target, "confidence", f"legacy target '{source_target_id}'"
        )
        if not isinstance(target_confidence, (int, float)) or isinstance(
            target_confidence, bool
        ):
            raise ReconError(f"legacy target '{source_target_id}' confidence must be a number")

        relation_candidates = []
        unmapped = []
        for edge in sorted(self.edges, key=lambda item: item["id"]):
            candidate = self._mapped_relation(edge)
            if candidate is None:
                source_type = _NODE_TYPES[self.node_index[edge["source"]]["type"]]
                target_type = _NODE_TYPES[self.node_index[edge["target"]]["type"]]
                unmapped.append(
                    {
                        "id": edge["id"],
                        "relation": edge["relation"],
                        "source_type": source_type,
                        "target_type": target_type,
                    }
                )
            else:
                relation_candidates.append(candidate)

        for axis_id, profile in sorted(target_profile.items()):
            if axis_id not in self.node_index or self.node_index[axis_id]["type"] != "concept":
                raise ReconError(f"legacy target profile axis '{axis_id}' is missing")
            strength = _required(profile, "strength", f"legacy target profile '{axis_id}'")
            maturity = _required_string(
                profile, "maturity", f"legacy target profile '{axis_id}'"
            )
            basis = _required_string(profile, "basis", f"legacy target profile '{axis_id}'")
            relation_id = "relation:imported-target:" + hashlib.sha256(
                f"{self.project.config['target_id']}\0{axis_id}".encode("utf-8")
            ).hexdigest()
            relation_candidates.append(
                RecordCandidate(
                    "CoversAxisRelation",
                    {
                        "id": relation_id,
                        "source_id": self.project.config["target_id"],
                        "target_id": axis_id,
                        "relation_type": "COVERS_AXIS",
                        "review_state": "REVIEWED",
                        "assertion_status": "REVIEWER_INFERENCE",
                        "confidence": target_confidence,
                        "basis": basis,
                        "evidence_ids": target_evidence,
                        "coverage_level": _coverage_level(strength, maturity),
                        "coverage_maturity": maturity,
                    },
                )
            )

        if unmapped and not allow_unmapped:
            counts = Counter(item["relation"] for item in unmapped)
            summary = ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))
            raise ReconError(
                f"Legacy import has {len(unmapped)} unmapped edges ({summary}); "
                "extend the typed adapter or pass allow_unmapped=True explicitly"
            )

        source_evidence_id = f"evidence:import-source:{self.source_hash}"
        source_evidence = {
            "id": source_evidence_id,
            "label": f"Imported literature graph v{self.version}",
            "review_state": "REVIEWED",
            "local_path": str(self.path.resolve()),
            "locator": "whole JSON artifact",
            "evidence_description": "Exact canonical literature graph supplied to the v1 importer.",
            "source_class": "OTHER",
            "accessed_on": self.as_of,
            "access_status": "INSPECTED",
            "artifact_sha256": f"sha256:{self.source_hash}",
            "artifact_byte_length": len(self.source_bytes),
        }
        self.evidence_records[source_evidence_id] = source_evidence
        unmapped_counts = Counter(item["relation"] for item in unmapped)
        boundary_id = f"boundary:legacy-import:{self.source_hash}"
        boundary = {
            "id": boundary_id,
            "label": f"Legacy literature graph v{self.version} import boundary",
            "review_state": "REVIEWED",
            "evidence_ids": [source_evidence_id],
            "boundary_kind": "LEGACY_V1_IMPORT",
            "boundary_reason": (
                f"Imported {len(self.nodes)} nodes and mapped "
                f"{len(relation_candidates)} relations; {len(unmapped)} source edges were "
                "not mapped and remain identified in the import report."
            ),
            "notes": [
                f"Source sha256: {self.source_hash}",
                *[
                    f"Unmapped {relation}: {count}"
                    for relation, count in sorted(unmapped_counts.items())
                ],
                *[
                    f"Unknown legacy source_class '{name}' mapped to OTHER: {count}"
                    for name, count in sorted(self.unknown_source_classes.items())
                ],
            ],
        }
        evidence_candidates = [
            RecordCandidate("EvidenceAttachment", record)
            for _, record in sorted(self.evidence_records.items())
        ]
        candidates = [
            *evidence_candidates,
            *node_candidates,
            RecordCandidate("ReviewBoundary", boundary),
            *relation_candidates,
        ]
        report = {
            "source_path": str(self.path.resolve()),
            "source_version": self.version,
            "source_sha256": self.source_hash,
            "source_nodes": len(self.nodes),
            "source_edges": len(self.edges),
            "evidence_records": len(evidence_candidates),
            "mapped_relations": len(relation_candidates),
            "unmapped_edges": unmapped,
            "unmapped_by_relation": dict(sorted(unmapped_counts.items())),
            "unknown_source_classes": dict(sorted(self.unknown_source_classes.items())),
            "review_target_id": self.project.config["target_id"],
            "source_target_id": source_target_id,
            "boundary_id": boundary_id,
            "planned_records": len(candidates),
        }
        return candidates, report

    def import_all(
        self,
        *,
        actor_id: str,
        allow_unmapped: bool = False,
    ) -> dict[str, Any]:
        candidates, report = self.plan(allow_unmapped=allow_unmapped)
        events = self.project.record_many(
            candidates,
            actor_id=actor_id,
            require_all_recorded=True,
        )
        report = {**report, "recorded_events": len(events)}
        return report


def import_literature_kg_v1(
    project: ReconProject,
    source_path: str | Path,
    *,
    actor_id: str,
    allow_unmapped: bool = False,
) -> dict[str, Any]:
    return LiteratureV1Importer(project, source_path).import_all(
        actor_id=actor_id,
        allow_unmapped=allow_unmapped,
    )
