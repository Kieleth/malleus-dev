import ast
import csv
import errno
import hashlib
import importlib.util
import json
import multiprocessing
import re
import zipfile
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET

import networkx as nx
import pytest
import yaml
from markdown_it import MarkdownIt
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD

import malleus.recon.analysis as analysis
import malleus.recon.store as recon_store
from malleus.kg import KnowledgeGraph
from malleus.ledger import LedgerError
from malleus.migration import (
    PARTIAL,
    TOTAL,
    MigrationAwareJsonlLedger,
    MigrationChain,
    MigrationReceipt,
    MigrationVerifier,
)
from malleus.ontology import OntologyRegistry, bundled_ontology_path
from malleus.recon import (
    ReconError,
    ReconProject,
    RecordCandidate,
    STRUCTURAL_CAPTURE_PROFILE,
    StoredRecord,
    build_outputs,
    bundled_contract_path,
    compare_subjects,
    visualize,
)
from malleus.recon.cli import main
from malleus.recon.import_v1 import import_literature_kg_v1
from malleus.recon.store import LEDGER_FILE, RECORDED, REJECTED, load_record_file
from malleus.status import IMPLEMENTATION_STATUS


def NOW():
    return "2026-08-16T12:00:00+00:00"


def test_bundled_contract_is_resolvable():
    path = bundled_contract_path()
    assert path.name == "RECON_CONTRACT.md"
    assert path.read_text(encoding="utf-8").startswith("# Malleus Recon contract")
    assert STRUCTURAL_CAPTURE_PROFILE == "malleus.recon.structural-capture/v1"


def test_recon_source_has_no_direct_static_governed_or_private_import():
    package = Path(__file__).parents[1] / "src" / "malleus" / "recon"
    forbidden_public_modules = (
        "malleus.accepted",
        "malleus.assent",
        "malleus.protocol",
    )
    forbidden_names = {
        "AcceptedGraphProjector",
        "KnowledgeChangeSet",
        "ProtocolLedger",
    }

    def forbidden_module(module):
        return (
            module == "malleus"
            or module.startswith("malleus._contract")
            or any(
                module == forbidden or module.startswith(f"{forbidden}.")
                for forbidden in forbidden_public_modules
            )
        )

    violations = []
    for path in sorted(package.rglob("*.py")):
        name = path.relative_to(package).as_posix()
        current_package = ".".join(
            ("malleus", "recon", *path.relative_to(package).parts[:-1])
        )
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Import):
                violations.extend(
                    f"{name}: imports {alias.name}"
                    for alias in node.names
                    if forbidden_module(alias.name)
                )
            elif isinstance(node, ast.ImportFrom):
                requested = "." * node.level + (node.module or "")
                try:
                    module = (
                        importlib.util.resolve_name(requested, current_package)
                        if node.level
                        else requested
                    )
                except (ImportError, ValueError):
                    violations.append(f"{name}: invalid relative import {requested}")
                    continue
                imported_modules = {
                    f"{module}.{alias.name}"
                    for alias in node.names
                    if alias.name != "*"
                }
                if forbidden_module(module) or any(
                    forbidden_module(imported) for imported in imported_modules
                ):
                    violations.append(f"{name}: imports from {module}")
                violations.extend(
                    f"{name}: imports {alias.name} from {module}"
                    for alias in node.names
                    if alias.name in forbidden_names
                )
    assert violations == []


def _record(project, record_type, record, supersedes=None):
    event = project.record(
        record_type,
        record,
        actor_id="reviewer:luis",
        supersedes_event_id=supersedes,
    )
    assert event["payload"]["decision"] == "RECORDED", event["payload"]["errors"]
    return event


def _evidence(identifier="evidence:paper"):
    return {
        "id": identifier,
        "label": "Inspected paper",
        "review_state": "REVIEWED",
        "source_uri": "https://example.org/paper",
        "locator": "section 3",
        "evidence_description": "The inspected section states the system boundary.",
        "source_class": "PUBLISHER",
        "accessed_on": "2026-08-16",
        "access_status": "INSPECTED",
    }


def _relation(identifier, source, target, coverage):
    return {
        "id": identifier,
        "source_id": source,
        "target_id": target,
        "relation_type": "COVERS_AXIS",
        "review_state": "REVIEWED",
        "assertion_status": "REVIEWER_INFERENCE",
        "confidence": 0.9,
        "basis": "The cited section was inspected against the axis definition.",
        "evidence_ids": ["evidence:paper"],
        "coverage_level": coverage,
    }


def _legacy_evidence():
    return {
        "url": "https://example.org/paper",
        "locator": "section 3",
        "description": "Inspected source section.",
        "source_class": "publisher",
        "accessed": "2026-08-16",
    }


def _legacy_graph(extra_edges=None):
    evidence = [_legacy_evidence()]
    return {
        "meta": {
            "version": "1.4.0",
            "as_of": "2026-08-16",
            "method": "Claim-conditioned primary-source review",
            "set_comparison": {"target_paper_id": "claim:target"},
        },
        "nodes": [
            {
                "id": "axis:atomic",
                "type": "concept",
                "label": "Atomic commitment",
                "summary": "The accepted transition and graph application are atomic.",
                "comparison_code": "A13",
                "comparison_scope": "TARGET_CURRENT",
            },
            {
                "id": "claim:target",
                "type": "claim",
                "label": "Target claim",
                "text": "The target implements atomic commitment.",
                "claim_kind": "systems_claim",
                "confidence": 0.95,
                "evidence": evidence,
                "set_profile": {
                    "axis:atomic": {
                        "strength": 3,
                        "maturity": "IMPLEMENTED_TESTED",
                        "basis": "The target transaction binds acceptance and application.",
                    }
                },
            },
            {
                "id": "work:paper-a",
                "type": "paper",
                "label": "Paper A",
                "title": "Paper A",
                "authors": ["Ada Example"],
                "venue": "ExampleConf",
                "identifiers": {"doi": "10.0000/example"},
                "priority_date": "2025-01-02",
                "priority_date_basis": "First public preprint",
                "peer_review_status": "preprint",
                "summary": "A system with material atomic commitment.",
                "evidence": evidence,
                "notes": [],
                "concept_scores": {"axis:atomic": 2},
                "set_profile": {
                    "axis:atomic": {
                        "strength": 2,
                        "maturity": "REPORTED_IMPLEMENTED",
                        "basis": "The paper reports a transaction around the update.",
                    }
                },
            },
        ],
        "edges": [
            {
                "id": "edge:work-axis",
                "source": "work:paper-a",
                "target": "axis:atomic",
                "relation": "about_concept",
                "assertion_status": "reviewer_inference",
                "confidence": 0.9,
                "basis": "Concept score 2/3.",
                "dimensions": [],
                "evidence": evidence,
                "review_notes": [],
                "symmetric": False,
            },
            {
                "id": "edge:claim-axis",
                "source": "claim:target",
                "target": "axis:atomic",
                "relation": "about_concept",
                "assertion_status": "reviewer_inference",
                "confidence": 0.95,
                "basis": "The target claim names atomic commitment.",
                "dimensions": [],
                "evidence": evidence,
                "review_notes": [],
                "symmetric": False,
            },
            *(extra_edges or []),
        ],
    }


def _project(tmp_path, *, complete=True):
    project = ReconProject.initialize(
        tmp_path / "recon",
        title="Atomic review",
        target_id="target:malleus",
        creator_id="reviewer:luis",
        clock=NOW,
    )
    if not complete:
        return project
    _record(project, "EvidenceAttachment", _evidence())
    _record(
        project,
        "ReviewTarget",
        {
            "id": "target:malleus",
            "label": "Malleus target",
            "review_state": "REVIEWED",
            "scope": "Atomic commitment and review history",
            "cutoff_date": "2026-08-16",
            "review_method": "Claim-conditioned primary-source review",
        },
    )
    for identifier, label in (
        ("axis:atomic", "Atomic commitment"),
        ("axis:history", "Replayable history"),
        ("axis:sandbox", "Sandbox execution"),
    ):
        _record(
            project,
            "ComparisonAxis",
            {
                "id": identifier,
                "label": label,
                "review_state": "REVIEWED",
                "axis_definition": f"Whether the system materially implements {label.lower()}.",
            },
        )
    _record(
        project,
        "Work",
        {
            "id": "work:paper-a",
            "label": "Paper A",
            "title": "Paper A",
            "authors": ["Ada Example"],
            "identifiers": ["doi:10.0000/example"],
            "priority_date": "2025-01-02",
            "priority_date_basis": "First public preprint",
            "publication_status": "PREPRINT",
            "review_state": "REVIEWED",
            "evidence_ids": ["evidence:paper"],
        },
    )
    for relation in (
        _relation("coverage:target:atomic", "target:malleus", "axis:atomic", "CENTRAL"),
        _relation("coverage:target:history", "target:malleus", "axis:history", "MATERIAL"),
        _relation("coverage:work:atomic", "work:paper-a", "axis:atomic", "MATERIAL"),
        _relation("coverage:work:history", "work:paper-a", "axis:history", "PARTIAL"),
        _relation("coverage:work:sandbox", "work:paper-a", "axis:sandbox", "CENTRAL"),
    ):
        _record(project, "CoversAxisRelation", relation)
    return project


def test_project_initialization_refuses_to_overwrite_nonempty_directory(tmp_path):
    destination = tmp_path / "occupied"
    destination.mkdir()
    (destination / "notes.txt").write_text("mine", encoding="utf-8")
    with pytest.raises(ReconError, match="not empty"):
        ReconProject.initialize(
            destination,
            title="Review",
            target_id="target:one",
            creator_id="reviewer:one",
        )
    assert (destination / "notes.txt").read_text(encoding="utf-8") == "mine"


def test_missing_evidence_is_recorded_as_rejection_without_graph_mutation(tmp_path):
    project = _project(tmp_path)
    before = project.current_records()
    bad = _relation("coverage:bad", "work:paper-a", "axis:history", "MATERIAL")
    bad["evidence_ids"] = ["evidence:missing"]
    event = project.record("CoversAxisRelation", bad, actor_id="reviewer:luis")
    assert event["payload"]["decision"] == "REJECTED"
    assert event["payload"]["errors"] == [
        "CoversAxisRelation 'coverage:bad' references missing evidence "
        "'evidence:missing'",
        "CoversAxisRelation 'coverage:bad' duplicates subject-axis profile already "
        "recorded by 'coverage:work:history'",
    ]
    assert project.current_records() == before
    assert project.events()[-1]["payload"]["record"] == bad


def test_revision_requires_the_latest_recorded_event_and_preserves_history(tmp_path):
    project = _project(tmp_path, complete=False)
    first = _record(
        project,
        "Work",
        {
            "id": "work:draft",
            "label": "Draft",
            "title": "Draft title",
            "priority_date": "2026-01-01",
            "priority_date_basis": "Repository snapshot",
            "publication_status": "UNKNOWN",
            "review_state": "PROPOSED",
        },
    )
    revision = {
        "id": "work:draft",
        "label": "Draft",
        "title": "Corrected title",
        "priority_date": "2026-01-01",
        "priority_date_basis": "Repository snapshot",
        "publication_status": "UNKNOWN",
        "review_state": "PROPOSED",
    }
    rejected = project.record(
        "Work",
        revision,
        actor_id="reviewer:luis",
        supersedes_event_id="recon-event:wrong",
    )
    assert rejected["payload"]["decision"] == "REJECTED"
    assert project.current_records()["work:draft"].record["title"] == "Draft title"
    accepted = _record(
        project,
        "Work",
        revision,
        supersedes=first["event_id"],
    )
    assert project.current_records()["work:draft"].record["title"] == "Corrected title"
    assert [event["payload"]["decision"] for event in project.events()] == [
        "RECORDED",
        "REJECTED",
        "RECORDED",
    ]
    assert accepted["payload"]["supersedes_event_id"] == first["event_id"]


def test_required_batch_is_atomic_when_one_candidate_would_be_rejected(tmp_path):
    project = _project(tmp_path, complete=False)
    candidates = [
        RecordCandidate("EvidenceAttachment", _evidence()),
        RecordCandidate(
            "Work",
            {
                "id": "work:unsupported",
                "label": "Unsupported",
                "title": "Unsupported",
                "priority_date_basis": "No date verified",
                "publication_status": "UNKNOWN",
                "review_state": "REVIEWED",
                "evidence_ids": ["evidence:missing"],
            },
        ),
    ]
    with pytest.raises(
        ReconError,
        match="batch final state is invalid.*references missing evidence",
    ):
        project.record_many(
            candidates,
            actor_id="reviewer:luis",
            require_all_recorded=True,
        )
    assert project.events() == []


def test_valid_batch_commits_as_one_failure_atomic_append(tmp_path):
    project = _project(tmp_path, complete=False)
    events = project.record_many(
        [
            RecordCandidate("EvidenceAttachment", _evidence()),
            RecordCandidate(
                "Work",
                {
                    "id": "work:batched",
                    "label": "Batched",
                    "title": "Batched work",
                    "priority_date_basis": "No date verified",
                    "publication_status": "UNKNOWN",
                    "review_state": "REVIEWED",
                    "evidence_ids": ["evidence:paper"],
                },
            ),
        ],
        actor_id="reviewer:luis",
        require_all_recorded=True,
    )
    assert [event["sequence"] for event in events] == [1, 2]
    assert set(project.current_records()) == {"evidence:paper", "work:batched"}


def test_required_batch_refuses_a_forward_reference_that_cannot_replay(tmp_path):
    project = _project(tmp_path, complete=False)
    work = RecordCandidate(
        "Work",
        {
            "id": "work:forward-reference",
            "label": "Forward reference",
            "title": "Forward reference",
            "priority_date_basis": "No date verified",
            "publication_status": "UNKNOWN",
            "review_state": "REVIEWED",
            "evidence_ids": ["evidence:paper"],
        },
    )

    with pytest.raises(
        ReconError,
        match=(
            "record batch item 1 is not replay-valid in caller order.*"
            "references missing evidence 'evidence:paper'"
        ),
    ):
        project.record_many(
            [work, RecordCandidate("EvidenceAttachment", _evidence())],
            actor_id="reviewer:luis",
            require_all_recorded=True,
        )

    assert project.events() == []


def test_comparison_reports_exact_set_algebra_and_keeps_partial_separate(tmp_path):
    project = _project(tmp_path)
    result = compare_subjects(project, "target:malleus", "work:paper-a")
    assert result["intersection"] == ["axis:atomic"]
    assert result["union"] == ["axis:atomic", "axis:history", "axis:sandbox"]
    assert result["target_difference"] == ["axis:history"]
    assert result["work_difference"] == ["axis:sandbox"]
    assert result["symmetric_difference"] == ["axis:history", "axis:sandbox"]
    assert result["partial_or_adjacent"]["axis:history"]["work"] == "PARTIAL"
    assert "axis:sandbox" not in result["unresolved"]
    assert result["unassessed"]["axis:sandbox"]["target"] is None
    assert "novelty verdict" in result["boundary"]


def test_contested_axis_stays_visible_but_does_not_enter_material_set(tmp_path):
    project = _project(tmp_path)
    current = project.current_records()["coverage:work:history"]
    contested = _relation(
        "coverage:work:history", "work:paper-a", "axis:history", "MATERIAL"
    )
    contested["review_state"] = "CONTESTED"
    _record(
        project,
        "CoversAxisRelation",
        contested,
        supersedes=current.event_id,
    )
    result = compare_subjects(project, "target:malleus", "work:paper-a")
    assert result["contested"] == {
        "axis:history": {"target": None, "work": "MATERIAL"}
    }
    assert "axis:history" not in result["work_profile"]
    paths = build_outputs(project)
    with paths["work_axis_matrix.csv"].open(newline="", encoding="utf-8") as stream:
        rows = {row["subject_id"]: row for row in csv.DictReader(stream)}
    assert rows["work:paper-a"]["axis:history"] == "CONTESTED:MATERIAL"


def test_duplicate_subject_axis_profile_is_rejected(tmp_path):
    project = _project(tmp_path)
    duplicate = _relation(
        "coverage:duplicate", "work:paper-a", "axis:atomic", "CENTRAL"
    )
    event = project.record("CoversAxisRelation", duplicate, actor_id="reviewer:luis")
    assert event["payload"]["decision"] == "REJECTED"
    assert "duplicates subject-axis profile" in event["payload"]["errors"][0]


def test_reviewed_work_without_evidence_is_rejected(tmp_path):
    project = _project(tmp_path, complete=False)
    event = project.record(
        "Work",
        {
            "id": "work:unsupported",
            "label": "Unsupported",
            "title": "Unsupported work",
            "priority_date": "2026-01-01",
            "priority_date_basis": "Unverified memory",
            "publication_status": "UNKNOWN",
            "review_state": "REVIEWED",
        },
        actor_id="reviewer:luis",
    )
    assert event["payload"]["decision"] == "REJECTED"
    assert event["payload"]["errors"] == [
        "Reviewed Work 'work:unsupported' requires evidence_ids"
    ]


def test_evidence_identity_is_preserved_but_requires_a_complete_pair(tmp_path):
    project = _project(tmp_path, complete=False)
    evidence = _evidence("evidence:bytes")
    evidence["artifact_sha256"] = "sha256:" + "a" * 64
    rejected = project.record(
        "EvidenceAttachment", evidence, actor_id="reviewer:luis"
    )
    assert rejected["payload"]["decision"] == "REJECTED"
    assert "must be supplied together" in rejected["payload"]["errors"][0]
    evidence["artifact_byte_length"] = 42
    accepted = _record(project, "EvidenceAttachment", evidence)
    assert accepted["payload"]["record"]["artifact_sha256"] == "sha256:" + "a" * 64


def test_invalid_dates_are_rejected_instead_of_normalized(tmp_path):
    project = _project(tmp_path, complete=False)
    evidence = _evidence()
    evidence["accessed_on"] = "16 August 2026"
    event = project.record("EvidenceAttachment", evidence, actor_id="reviewer:luis")
    assert event["payload"]["decision"] == "REJECTED"
    assert event["payload"]["errors"] == [
        "EvidenceAttachment 'evidence:paper' accessed_on must be YYYY-MM-DD"
    ]


def test_blank_source_locator_is_not_treated_as_a_source(tmp_path):
    project = _project(tmp_path, complete=False)
    evidence = _evidence()
    evidence["source_uri"] = " "
    event = project.record("EvidenceAttachment", evidence, actor_id="reviewer:luis")
    assert event["payload"]["decision"] == "REJECTED"
    assert event["payload"]["errors"] == [
        "EvidenceAttachment 'evidence:paper' requires source_uri or local_path",
        "EvidenceAttachment 'evidence:paper' source_uri must be a nonblank string",
    ]


def test_retired_work_is_kept_in_graph_but_excluded_from_analysis(tmp_path):
    project = _project(tmp_path)
    current = project.current_records()["work:paper-a"]
    retired = dict(current.record)
    retired["review_state"] = "RETIRED"
    _record(project, "Work", retired, supersedes=current.event_id)
    with pytest.raises(ReconError, match="is retired"):
        compare_subjects(project, "target:malleus", "work:paper-a")
    paths = build_outputs(project)
    metrics = json.loads(paths["metrics.json"].read_text(encoding="utf-8"))
    assert metrics["works"] == 0
    assert metrics["retired_records"] == 1
    assert "Paper A (`work:paper-a`)" not in paths["report.md"].read_text(encoding="utf-8")


def test_project_validation_requires_the_declared_target(tmp_path):
    project = _project(tmp_path, complete=False)
    assert project.validate() == [
        "Project target 'target:malleus' has not been recorded"
    ]
    with pytest.raises(ReconError, match="incomplete"):
        build_outputs(project)


def test_build_is_byte_deterministic_and_manifest_matches(tmp_path):
    project = _project(tmp_path)
    first_paths = build_outputs(project)
    first = {name: path.read_bytes() for name, path in first_paths.items()}
    second_paths = build_outputs(project)
    second = {name: path.read_bytes() for name, path in second_paths.items()}
    assert first == second
    manifest = json.loads(first["manifest.json"])
    for name, identity in manifest["files"].items():
        assert identity["bytes"] == len(first[name])
        assert identity["sha256"] == hashlib.sha256(first[name]).hexdigest()
    assert "recon_bundle.zip" not in manifest["files"]


def test_generated_graph_matrix_and_report_are_inspectable(tmp_path):
    project = _project(tmp_path)
    paths = build_outputs(project)
    ET.fromstring(paths["literature_kg.graphml"].read_bytes())
    jsonld = json.loads(paths["literature_kg.jsonld"].read_text(encoding="utf-8"))
    assert any(
        item["@id"] == "urn:malleus:recon:record:work%3Apaper-a"
        for item in jsonld["@graph"]
    )
    with paths["work_axis_matrix.csv"].open(newline="", encoding="utf-8") as stream:
        rows = {row["subject_id"]: row for row in csv.DictReader(stream)}
    assert rows["target:malleus"]["axis:history"] == "MATERIAL"
    assert rows["work:paper-a"]["axis:history"] == "PARTIAL"
    report = paths["report.md"].read_text(encoding="utf-8")
    assert "Paper A (`work:paper-a`) | 2 | 1 | 1 | 1 | 1" in report
    assert "not proof of absence" in report
    comparisons = json.loads(paths["comparisons.json"].read_text(encoding="utf-8"))
    assert comparisons["work:paper-a"]["target_difference"] == ["axis:history"]


def test_ledger_edit_is_detected_before_projection(tmp_path):
    project = _project(tmp_path)
    ledger = project.root / "ledger.jsonl"
    text = ledger.read_text(encoding="utf-8")
    ledger.write_text(text.replace('"decision":"RECORDED"', '"decision":"REJECTED"', 1))
    with pytest.raises(LedgerError, match="event_hash mismatch"):
        project.current_records()


def test_record_loader_refuses_duplicate_json_keys(tmp_path):
    source = tmp_path / "record.json"
    source.write_text('{"id":"work:a","id":"work:b"}', encoding="utf-8")
    with pytest.raises(ReconError, match="duplicate JSON key 'id'"):
        load_record_file(source)


def test_cli_catches_bad_record_without_traceback(tmp_path, capsys):
    project = _project(tmp_path, complete=False)
    source = tmp_path / "bad.json"
    source.write_text("{not-json", encoding="utf-8")
    assert (
        main(
            [
                "record",
                str(project.root),
                "Work",
                str(source),
                "--actor",
                "reviewer:luis",
            ]
        )
        == 2
    )
    captured = capsys.readouterr()
    assert "Cannot read record file" in captured.err
    assert "Traceback" not in captured.err


def test_cli_validate_reuses_one_verified_snapshot(tmp_path, monkeypatch, capsys):
    project = ReconProject.initialize(
        tmp_path / "single-snapshot",
        title="One-pass validation",
        target_id="target:one",
        creator_id="reviewer:one",
        clock=NOW,
    )
    event = project.record(
        "ReviewTarget",
        {
            "id": "target:one",
            "label": "Target one",
            "review_state": "PROPOSED",
            "scope": "Verify that CLI validation reuses one snapshot.",
            "cutoff_date": "2026-08-16",
            "review_method": "Contract test",
        },
        actor_id="reviewer:one",
    )
    assert event["payload"]["decision"] == "RECORDED"

    original = ReconProject.snapshot
    calls = 0

    def counted_snapshot(self):
        nonlocal calls
        calls += 1
        return original(self)

    monkeypatch.setattr(ReconProject, "snapshot", counted_snapshot)

    assert main(["validate", str(project.root)]) == 0
    assert calls == 1
    assert capsys.readouterr().out == "valid: 1 current records, 1 ledger events\n"


def test_visualization_dependency_failure_is_actionable(tmp_path, monkeypatch):
    project = _project(tmp_path)
    modules = __import__("sys").modules
    monkeypatch.setitem(modules, "pyvis", None)
    monkeypatch.setitem(modules, "pyvis.network", None)
    with pytest.raises(ReconError, match=r"malleus-dev\[recon\]"):
        visualize(project)


def test_v1_import_preserves_profiles_evidence_and_source_identity(tmp_path):
    source = tmp_path / "legacy.json"
    source.write_text(json.dumps(_legacy_graph(), sort_keys=True), encoding="utf-8")
    project = ReconProject.initialize(
        tmp_path / "imported",
        title="Imported review",
        target_id="target:imported",
        creator_id="reviewer:luis",
        clock=NOW,
    )
    report = import_literature_kg_v1(
        project, source, actor_id="reviewer:luis"
    )
    assert report["source_version"] == "1.4.0"
    assert report["unmapped_edges"] == []
    assert report["mapped_relations"] == 3
    records = project.current_records()
    assert records["work:paper-a"].record_type == "Work"
    assert records["edge:work-axis"].record["coverage_level"] == "MATERIAL"
    assert records["edge:work-axis"].record["coverage_maturity"] == "REPORTED_IMPLEMENTED"
    evidence = next(
        item.record
        for item in records.values()
        if item.record_type == "EvidenceAttachment"
        and item.record.get("source_uri") == "https://example.org/paper"
    )
    assert evidence["access_status"] == "UNVERIFIED"
    source_record = records[f"evidence:import-source:{report['source_sha256']}"]
    assert source_record.record["artifact_byte_length"] == source.stat().st_size
    comparison = compare_subjects(project, "target:imported", "work:paper-a")
    assert comparison["intersection"] == ["axis:atomic"]


def test_v1_import_refuses_unmapped_edges_before_any_ledger_write(tmp_path):
    alien = {
        "id": "edge:alien",
        "source": "work:paper-a",
        "target": "work:paper-a",
        "relation": "unknown_relation",
        "assertion_status": "reviewer_inference",
        "confidence": 0.5,
        "basis": "Deliberate adapter test.",
        "dimensions": [],
        "evidence": [_legacy_evidence()],
        "review_notes": [],
        "symmetric": False,
    }
    source = tmp_path / "legacy.json"
    source.write_text(
        json.dumps(_legacy_graph(extra_edges=[alien]), sort_keys=True), encoding="utf-8"
    )
    project = ReconProject.initialize(
        tmp_path / "imported",
        title="Imported review",
        target_id="target:imported",
        creator_id="reviewer:luis",
        clock=NOW,
    )
    with pytest.raises(ReconError, match="1 unmapped edges"):
        import_literature_kg_v1(project, source, actor_id="reviewer:luis")
    assert project.events() == []


def test_explicit_unmapped_import_records_the_boundary(tmp_path):
    alien = {
        "id": "edge:alien",
        "source": "work:paper-a",
        "target": "work:paper-a",
        "relation": "unknown_relation",
        "assertion_status": "reviewer_inference",
        "confidence": 0.5,
        "basis": "Deliberate adapter test.",
        "dimensions": [],
        "evidence": [_legacy_evidence()],
        "review_notes": [],
        "symmetric": False,
    }
    source = tmp_path / "legacy.json"
    source.write_text(
        json.dumps(_legacy_graph(extra_edges=[alien]), sort_keys=True), encoding="utf-8"
    )
    project = ReconProject.initialize(
        tmp_path / "imported",
        title="Imported review",
        target_id="target:imported",
        creator_id="reviewer:luis",
        clock=NOW,
    )
    report = import_literature_kg_v1(
        project,
        source,
        actor_id="reviewer:luis",
        allow_unmapped=True,
    )
    assert report["unmapped_by_relation"] == {"unknown_relation": 1}
    boundary = project.current_records()[report["boundary_id"]].record
    assert "1 source edges were not mapped" in boundary["boundary_reason"]
    assert "Unmapped unknown_relation: 1" in boundary["notes"]


def _store_hold_writer_lock(path, ready, release):
    with recon_store._exclusive_writer(Path(path)):
        ready.set()
        if not release.wait(10):
            raise RuntimeError("parent did not release the writer-lock holder")


def _store_initialize_concurrently(root, title, release, messages):
    atomic_json = recon_store._atomic_json

    def gated_atomic_json(path, value):
        messages.put(("write", title))
        if not release.wait(20):
            raise RuntimeError("parent did not release the initializer")
        atomic_json(path, value)

    recon_store._atomic_json = gated_atomic_json
    try:
        project = ReconProject.initialize(
            root,
            title=title,
            target_id=f"target:{title}",
            creator_id=f"reviewer:{title}",
            clock=_store_now,
        )
    except BaseException as error:
        messages.put(("done", "error", title, type(error).__name__, str(error)))
    else:
        messages.put(("done", "success", title, project.config))


def _store_now():
    return "2026-09-02T12:00:00+00:00"


def _store_project(tmp_path):
    return ReconProject.initialize(
        tmp_path / "recon",
        title="Store hardening",
        target_id="target:malleus",
        creator_id="reviewer:test",
        clock=_store_now,
    )


def _store_work(identifier, *, title=None):
    return {
        "id": identifier,
        "label": title or identifier,
        "title": title or identifier,
        "priority_date_basis": "Repository snapshot",
        "publication_status": "UNKNOWN",
        "review_state": "PROPOSED",
    }


def _store_evidence(review_state="REVIEWED"):
    return {
        "id": "evidence:paper",
        "label": "Inspected paper",
        "review_state": review_state,
        "source_uri": "https://example.org/paper",
        "locator": "section 3",
        "evidence_description": "The section states the system boundary.",
        "source_class": "PUBLISHER",
        "accessed_on": "2026-09-02",
        "access_status": "INSPECTED",
    }


def _store_reviewed_work():
    return {
        **_store_work("work:paper", title="Paper"),
        "review_state": "REVIEWED",
        "evidence_ids": ["evidence:paper"],
    }


def _store_axis():
    return {
        "id": "axis:atomic",
        "label": "Atomicity",
        "review_state": "REVIEWED",
        "axis_definition": "Whether the update commits atomically.",
    }


def _store_coverage(identifier="coverage:paper:atomic"):
    return {
        "id": identifier,
        "source_id": "work:paper",
        "target_id": "axis:atomic",
        "relation_type": "COVERS_AXIS",
        "review_state": "REVIEWED",
        "assertion_status": "REVIEWER_INFERENCE",
        "confidence": 0.9,
        "basis": "The inspected section describes the commit boundary.",
        "evidence_ids": ["evidence:paper"],
        "coverage_level": "MATERIAL",
    }


def _store_legacy_candidate_errors(
    project,
    state,
    latest,
    record_type,
    record,
    supersedes_event_id,
):
    errors = project._identity_errors(
        state,
        latest,
        record_type,
        record,
        supersedes_event_id,
    )
    if errors:
        return errors
    identifier = record["id"]
    candidate = dict(state)
    candidate[identifier] = StoredRecord(
        record_type, deepcopy(record), "candidate"
    )
    errors = project._state_errors(candidate)
    if record_type == "CoversAxisRelation":
        profile = (record.get("source_id"), record.get("target_id"))
        for existing_id, existing_record in sorted(state.items()):
            if existing_id == identifier or existing_record.record_type != record_type:
                continue
            existing_profile = (
                existing_record.record.get("source_id"),
                existing_record.record.get("target_id"),
            )
            if profile == existing_profile:
                errors.append(
                    f"CoversAxisRelation '{identifier}' duplicates subject-axis profile "
                    f"already recorded by '{existing_id}'"
                )
                break
    return errors


def _store_legacy_replay(project, events):
    state = {}
    latest = {}
    for event in events:
        payload = event["payload"]
        errors = _store_legacy_candidate_errors(
            project,
            state,
            latest,
            payload["record_type"],
            payload["record"],
            payload["supersedes_event_id"],
        )
        decision = RECORDED if not errors else REJECTED
        assert payload["decision"] == decision
        assert payload["errors"] == errors
        if not errors:
            record = payload["record"]
            identifier = record["id"]
            state[identifier] = StoredRecord(
                payload["record_type"], deepcopy(record), event["event_id"]
            )
            latest[identifier] = event["event_id"]
    return state


def test_incremental_replay_is_exactly_equivalent_to_legacy_full_state_replay(tmp_path):
    project = _store_project(tmp_path)
    evidence = project.record(
        "EvidenceAttachment", _store_evidence(), actor_id="reviewer:test"
    )
    work = project.record("Work", _store_reviewed_work(), actor_id="reviewer:test")
    project.record("ComparisonAxis", _store_axis(), actor_id="reviewer:test")
    project.record("CoversAxisRelation", _store_coverage(), actor_id="reviewer:test")

    missing_title = _store_reviewed_work()
    del missing_title["title"]
    invalid_work = project.record(
        "Work",
        missing_title,
        actor_id="reviewer:test",
        supersedes_event_id=work["event_id"],
    )
    assert invalid_work["payload"]["errors"] == [
        "Work 'work:paper': Required slot 'title' missing for Work",
        "CoversAxisRelation 'coverage:paper:atomic': Source entity "
        "'work:paper' does not exist",
    ]

    retired_evidence = project.record(
        "EvidenceAttachment",
        _store_evidence("RETIRED"),
        actor_id="reviewer:test",
        supersedes_event_id=evidence["event_id"],
    )
    assert retired_evidence["payload"]["errors"] == [
        "CoversAxisRelation 'coverage:paper:atomic' references retired evidence "
        "'evidence:paper'",
        "Work 'work:paper' references retired evidence 'evidence:paper'",
    ]

    duplicate = project.record(
        "CoversAxisRelation",
        _store_coverage("coverage:duplicate"),
        actor_id="reviewer:test",
    )
    assert duplicate["payload"]["decision"] == REJECTED

    revised = _store_reviewed_work()
    revised["title"] = "Corrected paper"
    project.record(
        "Work",
        revised,
        actor_id="reviewer:test",
        supersedes_event_id=work["event_id"],
    )

    ledger_path = project.root / LEDGER_FILE
    before = ledger_path.read_bytes()
    events = project.events()
    expected = _store_legacy_replay(project, events)
    assert project._replay(events) == expected
    assert project.current_records() == expected
    assert ledger_path.read_bytes() == before


def test_replay_does_not_rematerialize_prior_independent_records(
    tmp_path, monkeypatch
):
    project = _store_project(tmp_path)
    first_batch = [
        RecordCandidate("Work", _store_work(f"work:{index:03d}"))
        for index in range(100)
    ]
    first = project.record_many(first_batch, actor_id="reviewer:test")
    rejected = project.record(
        "Work",
        _store_work("work:000", title="Wrong predecessor"),
        actor_id="reviewer:test",
        supersedes_event_id="recon-event:wrong",
    )
    assert rejected["payload"]["decision"] == REJECTED
    project.record(
        "Work",
        _store_work("work:000", title="Revised"),
        actor_id="reviewer:test",
        supersedes_event_id=first[0]["event_id"],
    )
    project.record_many(
        [
            RecordCandidate("Work", _store_work(f"work:{index:03d}"))
            for index in range(100, 200)
        ],
        actor_id="reviewer:test",
    )

    calls = 0
    create_entity = KnowledgeGraph.create_entity

    def counted_create_entity(self, *args, **kwargs):
        nonlocal calls
        calls += 1
        return create_entity(self, *args, **kwargs)

    monkeypatch.setattr(KnowledgeGraph, "create_entity", counted_create_entity)
    reopened = ReconProject(project.root, clock=_store_now)
    events, records = reopened.snapshot()
    assert len(records) == 200
    assert calls <= len(events)


def test_harmless_evidence_revision_does_not_rescan_high_fanout_dependents(
    tmp_path, monkeypatch
):
    project = _store_project(tmp_path)
    evidence = project.record(
        "EvidenceAttachment", _store_evidence(), actor_id="reviewer:test"
    )
    project.record_many(
        [
            RecordCandidate(
                "Work",
                {
                    **_store_work(f"work:{index:03d}"),
                    "review_state": "REVIEWED",
                    "evidence_ids": ["evidence:paper"],
                },
            )
            for index in range(100)
        ],
        actor_id="reviewer:test",
    )
    events_before = len(project.events())
    checked = []
    semantic_errors = project._record_semantic_errors

    def counted_semantic_errors(identifier, stored, lookup):
        checked.append(identifier)
        return semantic_errors(identifier, stored, lookup)

    monkeypatch.setattr(project, "_record_semantic_errors", counted_semantic_errors)
    revised = _store_evidence()
    revised["evidence_description"] = "Same source, clearer local description."
    event = project.record(
        "EvidenceAttachment",
        revised,
        actor_id="reviewer:test",
        supersedes_event_id=evidence["event_id"],
    )
    assert event["payload"]["decision"] == RECORDED
    assert len(checked) == events_before + 2
    assert checked.count("work:000") == 1


def test_append_replays_prefix_once_and_validates_only_new_suffix(tmp_path, monkeypatch):
    project = _store_project(tmp_path)
    project.record_many(
        [RecordCandidate("Work", _store_work(f"work:{index:03d}")) for index in range(40)],
        actor_id="reviewer:test",
    )
    calls = 0
    event_payload = project._event_payload

    def counted_event_payload(event, position):
        nonlocal calls
        calls += 1
        return event_payload(event, position)

    monkeypatch.setattr(project, "_event_payload", counted_event_payload)
    project.record("Work", _store_work("work:new"), actor_id="reviewer:test")
    assert calls == 41


def test_concurrent_recon_writer_is_refused_without_losing_either_attempt(
    tmp_path, monkeypatch
):
    first = _store_project(tmp_path)
    second = ReconProject(first.root, clock=_store_now)
    append_many = first._ledger.append_many
    refused = None

    def attempt_second_writer(entries, *, validate):
        nonlocal refused
        with pytest.raises(ReconError, match="active writer") as raised:
            second.record("Work", _store_work("work:second"), actor_id="reviewer:second")
        refused = raised.value
        return append_many(entries, validate=validate)

    monkeypatch.setattr(first._ledger, "append_many", attempt_second_writer)
    committed = first.record(
        "Work", _store_work("work:first"), actor_id="reviewer:first"
    )
    assert refused is not None
    assert committed["sequence"] == 1
    second_event = second.record(
        "Work", _store_work("work:second"), actor_id="reviewer:second"
    )
    assert second_event["sequence"] == 2
    assert set(first.current_records()) == {"work:first", "work:second"}


def test_concurrent_initializers_cannot_both_report_success(tmp_path):
    context = multiprocessing.get_context("spawn")
    root = tmp_path / "recon"
    release = context.Event()
    messages = context.Queue()
    processes = [
        context.Process(
            target=_store_initialize_concurrently,
            args=(root, title, release, messages),
        )
        for title in ("first", "second")
    ]
    for process in processes:
        process.start()

    initial = [messages.get(timeout=20) for _ in processes]
    release.set()
    outcomes = [message for message in initial if message[0] == "done"]
    while len(outcomes) < len(processes):
        message = messages.get(timeout=20)
        if message[0] == "done":
            outcomes.append(message)
    for process in processes:
        process.join(timeout=20)
        assert process.exitcode == 0

    successes = [outcome for outcome in outcomes if outcome[1] == "success"]
    failures = [outcome for outcome in outcomes if outcome[1] == "error"]
    assert len(successes) == 1
    assert len(failures) == 1
    assert failures[0][3] == "ReconError"
    assert "active writer" in failures[0][4]
    recorded = ReconProject(root, clock=_store_now)
    assert recorded.config == successes[0][3]


def test_initialization_can_retry_when_only_its_writer_lock_remains(tmp_path):
    root = tmp_path / "recon"
    with pytest.raises(ReconError, match="clock must return"):
        ReconProject.initialize(
            root,
            title="first",
            target_id="target:first",
            creator_id="reviewer:first",
            clock=lambda: "not-a-datetime",
        )

    project = ReconProject.initialize(
        root,
        title="second",
        target_id="target:second",
        creator_id="reviewer:second",
        clock=_store_now,
    )
    assert project.config["title"] == "second"


def test_initialization_refuses_non_utf8_project_text_as_recon_error(tmp_path):
    with pytest.raises(ReconError, match="canonical UTF-8 JSON"):
        ReconProject.initialize(
            tmp_path / "recon",
            title="invalid \ud800 title",
            target_id="target:first",
            creator_id="reviewer:first",
            clock=_store_now,
        )


def test_initialization_configures_the_return_object_before_publishing(tmp_path, monkeypatch):
    root = tmp_path / "recon"

    def fail_before_publish(self):
        raise RuntimeError("simulated return-object configuration failure")

    monkeypatch.setattr(ReconProject, "_configure_ledger", fail_before_publish)
    with pytest.raises(RuntimeError, match="return-object configuration failure"):
        ReconProject.initialize(
            root,
            title="first",
            target_id="target:first",
            creator_id="reviewer:first",
            clock=_store_now,
        )
    assert not (root / "project.json").exists()

    monkeypatch.undo()
    project = ReconProject.initialize(
        root,
        title="second",
        target_id="target:second",
        creator_id="reviewer:second",
        clock=_store_now,
    )
    assert project.config["title"] == "second"


@pytest.mark.parametrize("failure", ["oserror", "interrupt"])
def test_initialization_removes_project_marker_when_replace_reports_postpublish_failure(
    tmp_path, monkeypatch, failure
):
    root = tmp_path / "recon"
    replace = Path.replace

    def replace_then_fail(source, target):
        replace(source, target)
        if failure == "oserror":
            raise OSError(errno.EIO, "simulated post-replace failure")
        raise KeyboardInterrupt("simulated post-replace interruption")

    monkeypatch.setattr(Path, "replace", replace_then_fail)
    expected = ReconError if failure == "oserror" else KeyboardInterrupt
    with pytest.raises(expected, match="post-replace"):
        ReconProject.initialize(
            root,
            title="first",
            target_id="target:first",
            creator_id="reviewer:first",
            clock=_store_now,
        )
    assert not (root / "project.json").exists()

    monkeypatch.undo()
    project = ReconProject.initialize(
        root,
        title="second",
        target_id="target:second",
        creator_id="reviewer:second",
        clock=_store_now,
    )
    assert project.config["title"] == "second"


def test_initialization_cleanup_failure_does_not_mask_the_primary_write_failure(
    tmp_path, monkeypatch
):
    root = tmp_path / "recon"

    def fail_replace(source, target):
        raise OSError(errno.EIO, "primary replace failure")

    def fail_cleanup(path, *, missing_ok=False):
        raise OSError(errno.EIO, "secondary cleanup failure")

    monkeypatch.setattr(Path, "replace", fail_replace)
    monkeypatch.setattr(Path, "unlink", fail_cleanup)
    with pytest.raises(ReconError, match="primary replace failure") as raised:
        ReconProject.initialize(
            root,
            title="first",
            target_id="target:first",
            creator_id="reviewer:first",
            clock=_store_now,
        )
    assert "secondary cleanup failure" not in str(raised.value)


def test_initialization_reports_indeterminate_when_postpublish_rollback_fails(
    tmp_path, monkeypatch
):
    root = tmp_path / "recon"
    replace = Path.replace
    unlink = Path.unlink

    def replace_then_fail(source, target):
        replace(source, target)
        raise OSError(errno.EIO, "simulated post-replace failure")

    def fail_project_rollback(path, *, missing_ok=False):
        if path == root / "project.json":
            raise OSError(errno.EIO, "simulated rollback failure")
        return unlink(path, missing_ok=missing_ok)

    monkeypatch.setattr(Path, "replace", replace_then_fail)
    monkeypatch.setattr(Path, "unlink", fail_project_rollback)
    with pytest.raises(ReconError, match="outcome is indeterminate"):
        ReconProject.initialize(
            root,
            title="first",
            target_id="target:first",
            creator_id="reviewer:first",
            clock=_store_now,
        )
    assert (root / "project.json").is_file()


def _rewrite_analysis_manifest(paths, manifest):
    destination = paths["manifest.json"].parent
    manifest_body = analysis._json_text(manifest).encode("utf-8")
    paths["manifest.json"].write_bytes(manifest_body)
    archive_members = {
        name: (destination / name).read_bytes() for name in manifest["files"]
    }
    archive_members["manifest.json"] = manifest_body
    analysis._write_zip(paths["recon_bundle.zip"], archive_members)


@pytest.mark.parametrize("schema_version", ["1", "2", "999"])
def test_prior_or_unknown_manifest_cannot_authorize_deletion(
    tmp_path, schema_version
):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    manifest = json.loads(paths["manifest.json"].read_text(encoding="utf-8"))
    manifest["schema_version"] = schema_version
    _rewrite_analysis_manifest(paths, manifest)

    assert analysis._existing_managed_files(paths["manifest.json"].parent) == set()


def test_manifest_binds_exact_jsonld_ontology_sources_and_pyyaml(tmp_path):
    project = _analysis_project(tmp_path)
    manifest = json.loads(
        build_outputs(project)["manifest.json"].read_text(encoding="utf-8")
    )
    assert manifest["runtime"]["pyyaml"] == yaml.__version__
    closure = project.registry.source_closure()
    identity = analysis._jsonld_ontology(project.registry).identity
    assert manifest["jsonld_ontology"] == identity
    assert manifest["jsonld_ontology"]["sources"] == [
        {
            "source_role": source.source_role,
            "resolved_locator": source.resolved_locator,
            "bytes": source.byte_length,
            "sha256": source.sha256,
        }
        for source in closure.sources
    ]
    assert manifest["jsonld_ontology"]["imports"] == [
        {
            "parent_locator": edge.parent_locator,
            "ordinal": edge.ordinal,
            "literal": edge.literal,
            "target_role": edge.target_role,
            "resolved_locator": edge.resolved_locator,
        }
        for edge in closure.imports
    ]
    assert manifest["jsonld_ontology"]["definitions"] == [
        {
            "kind": definition.kind,
            "name": definition.name,
            "source_locator": definition.source_locator,
        }
        for definition in closure.definitions
    ]


def test_jsonld_uses_the_loaded_custom_root_and_transitive_import_owners(tmp_path):
    root_source = bundled_ontology_path("malleus.yaml")
    recon_source = bundled_ontology_path("domains", "recon.yaml")
    custom_root = tmp_path / "root.yaml"
    custom_recon = tmp_path / "recon.yaml"
    third = tmp_path / "third.yaml"
    entry = tmp_path / "entry.yaml"
    custom_root.write_text(
        root_source.read_text(encoding="utf-8")
        .replace(
            "id: https://malleus.dev/schema",
            "id: https://example.org/custom-root",
            1,
        )
        .replace(
            "malleus: https://malleus.dev/schema/",
            "malleus: https://example.org/custom-root/",
            1,
        ),
        encoding="utf-8",
    )
    custom_recon.write_bytes(recon_source.read_bytes())
    third.write_text(
        """id: https://example.org/third
name: third
version: 0.1.0
default_range: string
imports: [linkml:types]
prefixes: {linkml: 'https://w3id.org/linkml/'}
classes:
  ThirdThing:
    slots: [third_value]
slots:
  third_value:
    range: string
""",
        encoding="utf-8",
    )
    entry.write_text(
        """id: https://example.org/entry
name: entry
version: 0.1.0
default_range: string
imports: [recon, third]
prefixes: {linkml: 'https://w3id.org/linkml/'}
""",
        encoding="utf-8",
    )
    registry = OntologyRegistry(
        entry,
        import_map={
            "recon": custom_recon,
            "malleus": custom_root,
            "third": third,
        },
    )
    ontology = analysis._jsonld_ontology(registry)

    assert ontology.classes["Entity"] == "https://example.org/custom-root/Entity"
    assert ontology.classes["ThirdThing"] == "https://example.org/third/ThirdThing"
    owners = {
        (definition.kind, definition.name): definition.source_locator
        for definition in registry.source_closure().definitions
    }
    assert owners[("class", "Entity")] == str(custom_root.resolve())
    assert owners[("class", "ThirdThing")] == str(third.resolve())
    assert str(root_source.resolve()) not in {
        source.resolved_locator for source in registry.source_closure().sources
    }
    document = analysis._jsonld(
        {
            "nodes": [{"id": "root:one", "type": "Entity"}],
            "edges": [],
        },
        registry,
        ontology,
    )
    assert document["@graph"][0]["@type"] == (
        "https://example.org/custom-root/Entity"
    )


@pytest.mark.parametrize(
    "old,new",
    [
        (
            "class_uri: recon:Work",
            "class_uri: https://example.org/recon/ChangedWork",
        ),
        (
            "  source_uri:\n    range: uri",
            "  source_uri:\n    slot_uri: https://example.org/recon/changedSourceUri\n    range: uri",
        ),
    ],
)
def test_uri_only_ontology_change_alters_declared_jsonld_build_identity(
    tmp_path, old, new
):
    project = _analysis_project(tmp_path)
    baseline = json.loads(
        build_outputs(project, tmp_path / "baseline")["manifest.json"].read_text(
            encoding="utf-8"
        )
    )
    source = bundled_ontology_path("domains", "recon.yaml")
    custom_path = tmp_path / "custom-recon.yaml"
    source_text = source.read_text(encoding="utf-8")
    custom_body = source_text.replace(old, new, 1)
    assert custom_body != source_text
    custom_path.write_text(custom_body, encoding="utf-8")
    custom_registry = OntologyRegistry(
        custom_path,
        import_map={"malleus": bundled_ontology_path("malleus.yaml")},
    )
    assert custom_registry.content_hash() == project.registry.content_hash()
    project.registry = custom_registry

    changed = json.loads(
        build_outputs(project, tmp_path / "changed")["manifest.json"].read_text(
            encoding="utf-8"
        )
    )
    assert changed["ontology_hash"] == baseline["ontology_hash"]
    assert (
        changed["jsonld_ontology"]["sources"][0]
        != baseline["jsonld_ontology"]["sources"][0]
    )
    assert (
        changed["jsonld_ontology"]["term_map"]
        != baseline["jsonld_ontology"]["term_map"]
    )


def test_build_holds_destination_exclusion_before_snapshot(tmp_path):
    project = _analysis_project(tmp_path)
    destination = project.root / "build"
    original_snapshot = project.snapshot_verified
    observed = []

    def snapshot_verified():
        context = multiprocessing.get_context("spawn")
        queue = context.Queue()
        process = context.Process(
            target=_analysis_probe_build_lock,
            args=(str(destination), queue),
        )
        process.start()
        process.join(15)
        assert process.exitcode == 0
        observed.append(queue.get(timeout=2))
        return original_snapshot()

    project.snapshot_verified = snapshot_verified
    build_outputs(project)
    assert len(observed) == 1
    assert "active builder" in observed[0]


def test_real_and_symlink_destination_aliases_share_one_lock(tmp_path):
    real_destination = tmp_path / "actual-build"
    real_destination.mkdir()
    alias_destination = tmp_path / "alias-build"
    try:
        alias_destination.symlink_to(real_destination, target_is_directory=True)
    except OSError as error:
        pytest.skip(f"directory symlink unavailable: {error}")
    context = multiprocessing.get_context("spawn")
    queue = context.Queue()

    with analysis._exclusive_build(real_destination):
        process = context.Process(
            target=_analysis_probe_build_lock,
            args=(str(alias_destination), queue),
        )
        process.start()
        process.join(15)
        assert process.exitcode == 0
        observed = queue.get(timeout=2)

    assert analysis._canonical_build_destination(real_destination) == (
        analysis._canonical_build_destination(alias_destination)
    )
    assert "active builder" in observed


@pytest.mark.parametrize("failure", [OSError("cleanup I/O"), RuntimeError("cleanup bug")])
def test_staging_cleanup_failure_after_commit_does_not_report_failure(
    tmp_path, monkeypatch, failure
):
    project = _analysis_project(tmp_path)
    calls = []
    original_cleanup = analysis.tempfile.TemporaryDirectory.cleanup

    def fail_cleanup(temporary):
        if temporary.name.endswith(".staging"):
            calls.append(temporary.name)
            raise failure
        return original_cleanup(temporary)

    monkeypatch.setattr(analysis.tempfile.TemporaryDirectory, "cleanup", fail_cleanup)
    paths = build_outputs(project)
    manifest = json.loads(paths["manifest.json"].read_text(encoding="utf-8"))
    assert calls
    assert manifest["state"] == "COMMITTED"


def test_zip_bytes_ignore_platform_default_create_system(tmp_path, monkeypatch):
    files = {"a.txt": b"alpha", "b.txt": b"beta"}
    baseline = tmp_path / "baseline.zip"
    simulated_windows = tmp_path / "simulated-windows.zip"
    analysis._write_zip(baseline, files)
    original = analysis.zipfile.ZipInfo

    class WindowsDefaultZipInfo(original):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.create_system = 0

    monkeypatch.setattr(analysis.zipfile, "ZipInfo", WindowsDefaultZipInfo)
    analysis._write_zip(simulated_windows, files)

    assert simulated_windows.read_bytes() == baseline.read_bytes()
    with zipfile.ZipFile(simulated_windows) as archive:
        assert {member.create_system for member in archive.infolist()} == {3}


def test_zipinfo_members_receive_the_declared_level_nine_compression(tmp_path):
    body = json.dumps(
        [
            {"position": position, "text": "abc" * (position % 20), "values": list(range(position % 30))}
            for position in range(5000)
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    actual = tmp_path / "actual.zip"
    expected = tmp_path / "expected.zip"
    implicit_default = tmp_path / "implicit-default.zip"
    analysis._write_zip(actual, {"corpus.bin": body})

    def write(path, *, level):
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            info = zipfile.ZipInfo("corpus.bin", date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            if level is None:
                archive.writestr(info, body)
            else:
                archive.writestr(info, body, compresslevel=level)

    write(expected, level=9)
    write(implicit_default, level=None)
    assert expected.read_bytes() != implicit_default.read_bytes()
    assert actual.read_bytes() == expected.read_bytes()


def test_manifest_binds_ordered_migration_receipts_used_for_replay(tmp_path):
    project = _analysis_project(tmp_path)
    historical = "sha256:" + "c" * 64
    project.config["ontology_hash"] = historical
    project._events[0]["ontology_hash"] = historical
    (project.root / "project.json").write_text(
        json.dumps(project.config, indent=4, sort_keys=False) + "  \n",
        encoding="utf-8",
    )

    def receipt(reason):
        return MigrationReceipt(
            ontology="recon",
            from_hash=historical,
            to_hash=project.ontology_hash,
            grade=TOTAL,
            reason=reason,
            issued_at="2026-09-02T12:00:00+00:00",
        )

    first_receipt = receipt("first reading rule")
    _analysis_set_migrations(project, MigrationChain((first_receipt,)))
    first = json.loads(
        build_outputs(project, tmp_path / "first")["manifest.json"].read_text(
            encoding="utf-8"
        )
    )
    second_receipt = receipt("changed reading rule identity")
    _analysis_set_migrations(project, MigrationChain((second_receipt,)))
    second = json.loads(
        build_outputs(project, tmp_path / "second")["manifest.json"].read_text(
            encoding="utf-8"
        )
    )

    assert first["ontology_verification"]["receipt_digests"] == [
        first_receipt.digest
    ]
    assert second["ontology_verification"]["receipt_digests"] == [
        second_receipt.digest
    ]
    assert first["ontology_verification"] != second["ontology_verification"]


def test_manifest_preserves_oldest_to_newest_order_for_required_receipt_chain(
    tmp_path,
):
    project = _analysis_project(tmp_path)
    oldest = "sha256:" + "c" * 64
    middle = "sha256:" + "d" * 64
    first = MigrationReceipt(
        ontology="recon",
        from_hash=oldest,
        to_hash=middle,
        grade=TOTAL,
        reason="first reading rule",
        issued_at="2026-09-01T12:00:00+00:00",
    )
    second = MigrationReceipt(
        ontology="recon",
        from_hash=middle,
        to_hash=project.ontology_hash,
        grade=TOTAL,
        reason="second reading rule",
        issued_at="2026-09-02T12:00:00+00:00",
        previous_receipt=first.digest,
    )
    project.config["ontology_hash"] = oldest
    project._events[0]["ontology_hash"] = oldest
    _analysis_set_migrations(project, MigrationChain((first, second)))
    (project.root / "project.json").write_text(
        json.dumps(project.config, indent=4, sort_keys=False) + "  \n",
        encoding="utf-8",
    )

    manifest = json.loads(
        build_outputs(project)["manifest.json"].read_text(encoding="utf-8")
    )
    assert manifest["ontology_verification"]["receipt_digests"] == [
        first.digest,
        second.digest,
    ]


def test_shipped_historical_recon_project_uses_migration_aware_replay():
    root = Path(__file__).parents[1]
    project = ReconProject(root / "research" / "neurosymbolic_aws_samples_recon")
    historical = project.config["ontology_hash"]

    assert isinstance(project._ledger, MigrationAwareJsonlLedger)
    assert historical not in project.historical_ontology_hashes
    events, records, verification = project.snapshot_verified()
    persisted_events = tuple(
        line
        for line in (project.root / "ledger.jsonl").read_bytes().splitlines()
        if line
    )
    assert len(events) == len(persisted_events)
    assert records
    assert verification.grammar_ontology_hashes == ()
    assert verification.migrated_ontology_hashes == (historical,)
    assert verification.receipts == project.migrations.receipts
    assert verification.receipt_digests == tuple(
        receipt.digest for receipt in project.migrations.receipts
    )


def test_recon_project_refuses_a_config_that_crosses_a_partial_receipt(
    tmp_path, monkeypatch
):
    project = ReconProject.initialize(
        tmp_path / "partial-config",
        title="Partial migration refusal",
        target_id="target:one",
        creator_id="reviewer:one",
        clock=NOW,
    )
    historical = "sha256:" + "c" * 64
    receipt = MigrationReceipt(
        ontology="recon",
        from_hash=historical,
        to_hash=project.ontology_hash,
        grade=PARTIAL,
        reason="only some historical records have a reader",
        issued_at="2026-09-02T12:00:00+00:00",
    )
    config = json.loads((project.root / "project.json").read_text(encoding="utf-8"))
    config["ontology_hash"] = historical
    (project.root / "project.json").write_text(
        analysis._json_text(config), encoding="utf-8"
    )
    monkeypatch.setattr(
        recon_store,
        "migration_chain",
        lambda registry: MigrationChain((receipt,)),
    )

    with pytest.raises(ReconError, match="PARTIAL.*only some historical records"):
        ReconProject(project.root)


# Derived-output and build-transaction guards.
class _AnalysisProject:
    def __init__(self, root: Path, records: dict[str, StoredRecord]):
        self.root = root
        self.registry = OntologyRegistry(bundled_ontology_path("domains", "recon.yaml"))
        self.records = records
        self.ontology_hash = f"sha256:{self.registry.content_hash()}"
        self.config = {
            "schema_version": "1",
            "title": "Hardening fixture",
            "target_id": "target:one",
            "created_at": "2026-09-02T12:00:00+00:00",
            "creator_id": "reviewer:one",
            "ontology_hash": self.ontology_hash,
        }
        self._events = [
            {
                "event_hash": "sha256:" + "b" * 64,
                "ontology_hash": self.ontology_hash,
                "payload": {"decision": "RECORDED"},
            }
        ]
        self.migrations = MigrationChain(())
        self.migration_verifier = MigrationVerifier(self.registry, self.migrations)

    def snapshot(self):
        return self._events, self.records

    def snapshot_verified(self):
        identities = (
            self.config["ontology_hash"],
            *(event["ontology_hash"] for event in self._events),
        )
        return self._events, self.records, self.migration_verifier.verify(identities)

    def current_records(self):
        return self.records

    def validate(self, records=None):
        return []


def _analysis_probe_build_lock(destination: str, queue) -> None:
    try:
        with analysis._exclusive_build(Path(destination)):
            queue.put("acquired")
    except ReconError as error:
        queue.put(str(error))


def _analysis_stored(record_type: str, identifier: str, **properties) -> StoredRecord:
    return StoredRecord(
        record_type,
        {"id": identifier, **properties},
        f"event:{identifier}",
    )


def _analysis_coverage(
    identifier: str,
    source_id: str,
    target_id: str,
    level: str,
    *,
    review_state: str = "REVIEWED",
) -> StoredRecord:
    return _analysis_stored(
        "CoversAxisRelation",
        identifier,
        source_id=source_id,
        target_id=target_id,
        relation_type="COVERS_AXIS",
        review_state=review_state,
        assertion_status="REVIEWER_INFERENCE",
        confidence=0.9,
        coverage_level=level,
        basis="Inspected evidence against the axis definition.",
        evidence_ids=["evidence:one"],
    )


def _analysis_records() -> dict[str, StoredRecord]:
    return {
        "evidence:one": _analysis_stored(
            "EvidenceAttachment",
            "evidence:one",
            label="Evidence",
            description="Inspected primary source.",
            review_state="REVIEWED",
            source_uri="https://example.org/source",
        ),
        "target:one": _analysis_stored(
            "ReviewTarget",
            "target:one",
            label="Target",
            review_state="REVIEWED",
            scope="Structural capture",
        ),
        "work:one": _analysis_stored(
            "Work",
            "work:one",
            label="Work",
            title="Work",
            publication_status="PREPRINT",
            priority_date="2025-01-01",
            review_state="REVIEWED",
            evidence_ids=["evidence:one"],
        ),
        "axis:active": _analysis_stored(
            "ComparisonAxis",
            "axis:active",
            label="Active axis",
            review_state="REVIEWED",
        ),
        "coverage:target:active": _analysis_coverage(
            "coverage:target:active", "target:one", "axis:active", "MATERIAL"
        ),
        "coverage:work:active": _analysis_coverage(
            "coverage:work:active", "work:one", "axis:active", "CENTRAL"
        ),
    }


def _analysis_project(tmp_path: Path, records=None) -> _AnalysisProject:
    project = _AnalysisProject(tmp_path / "project", records or _analysis_records())
    project.root.mkdir(parents=True)
    (project.root / "project.json").write_text(
        json.dumps(project.config, indent=4, sort_keys=False) + "  \n",
        encoding="utf-8",
    )
    return project


def _analysis_use_registry(project: _AnalysisProject, registry: OntologyRegistry) -> None:
    project.registry = registry
    project.ontology_hash = f"sha256:{registry.content_hash()}"
    project.config["ontology_hash"] = project.ontology_hash
    for event in project._events:
        event["ontology_hash"] = project.ontology_hash
    _analysis_set_migrations(project, MigrationChain(()))
    (project.root / "project.json").write_text(
        json.dumps(project.config, indent=4, sort_keys=False) + "  \n",
        encoding="utf-8",
    )


def _analysis_set_migrations(
    project: _AnalysisProject,
    migrations: MigrationChain,
) -> None:
    project.migrations = migrations
    project.migration_verifier = MigrationVerifier(project.registry, migrations)


def test_retired_axis_cannot_leak_into_comparisons_matrix_or_report(tmp_path):
    records = _analysis_records()
    records.update(
        {
            "axis:retired": _analysis_stored(
                "ComparisonAxis",
                "axis:retired",
                label="Retired axis",
                review_state="RETIRED",
            ),
            "coverage:target:retired": _analysis_coverage(
                "coverage:target:retired", "target:one", "axis:retired", "CENTRAL"
            ),
            "coverage:work:retired": _analysis_coverage(
                "coverage:work:retired", "work:one", "axis:retired", "CENTRAL"
            ),
        }
    )
    project = _analysis_project(tmp_path, records)

    comparison = compare_subjects(project, "target:one", "work:one")
    assert comparison["intersection"] == ["axis:active"]
    assert comparison["target_profile"] == {"axis:active": "MATERIAL"}
    assert comparison["work_profile"] == {"axis:active": "CENTRAL"}

    paths = build_outputs(project)
    with paths["work_axis_matrix.csv"].open(newline="", encoding="utf-8") as stream:
        assert "axis:retired" not in next(csv.reader(stream))
    assert "axis:retired" not in paths["report.md"].read_text(encoding="utf-8")


def test_contested_coverage_is_not_relabelled_not_established(tmp_path):
    records = _analysis_records()
    records["coverage:target:active"] = _analysis_coverage(
        "coverage:target:active", "target:one", "axis:active", "PARTIAL"
    )
    records["coverage:work:active"] = _analysis_coverage(
        "coverage:work:active",
        "work:one",
        "axis:active",
        "MATERIAL",
        review_state="CONTESTED",
    )
    project = _analysis_project(tmp_path, records)

    comparison = compare_subjects(project, "target:one", "work:one")
    assert comparison["unresolved"] == {}
    assert comparison["contested"] == {
        "axis:active": {"target": None, "work": "MATERIAL"}
    }
    assert comparison["partial_or_adjacent"] == {
        "axis:active": {"target": "PARTIAL", "work": "CONTESTED:MATERIAL"}
    }
    assert comparison["unassessed"] == {}

    paths = build_outputs(project)
    persisted = json.loads(paths["comparisons.json"].read_text(encoding="utf-8"))
    assert persisted["work:one"]["unassessed"] == {}
    result_metrics = json.loads(paths["metrics.json"].read_text(encoding="utf-8"))
    assert result_metrics["unresolved_axis_assessments"] == 0
    assert result_metrics["unassessed_subject_axis_pairs"] == 0


def test_absent_and_explicit_not_established_assessments_remain_distinct(tmp_path):
    records = _analysis_records()
    records["axis:unresolved"] = _analysis_stored(
        "ComparisonAxis",
        "axis:unresolved",
        label="Unresolved axis",
        review_state="REVIEWED",
    )
    records["coverage:target:unresolved"] = _analysis_coverage(
        "coverage:target:unresolved",
        "target:one",
        "axis:unresolved",
        "NOT_ESTABLISHED",
    )
    project = _analysis_project(tmp_path, records)

    comparison = compare_subjects(project, "target:one", "work:one")
    expected = {
        "axis:unresolved": {"target": "NOT_ESTABLISHED", "work": None}
    }
    assert comparison["unresolved"] == expected
    assert comparison["unassessed"] == expected

    paths = build_outputs(project)
    with paths["work_axis_matrix.csv"].open(newline="", encoding="utf-8") as stream:
        rows = {row["subject_id"]: row for row in csv.DictReader(stream)}
    assert rows["target:one"]["axis:unresolved"] == "NOT_ESTABLISHED"
    assert rows["work:one"]["axis:unresolved"] == ""
    result_metrics = json.loads(paths["metrics.json"].read_text(encoding="utf-8"))
    assert result_metrics["unresolved_axis_assessments"] == 1
    assert result_metrics["unassessed_subject_axis_pairs"] == 1


def test_retired_relation_does_not_connect_active_components(tmp_path):
    records = _analysis_records()
    records["work:two"] = _analysis_stored(
        "Work",
        "work:two",
        label="Second work",
        title="Second work",
        publication_status="PREPRINT",
        priority_date="2025-02-01",
        review_state="REVIEWED",
        evidence_ids=["evidence:one"],
    )
    records["relation:retired"] = _analysis_stored(
        "CitesRelation",
        "relation:retired",
        source_id="work:one",
        target_id="work:two",
        relation_type="CITES",
        review_state="RETIRED",
        assertion_status="SOURCE_EXPLICIT",
        confidence=1.0,
        basis="Retired fixture relation.",
        evidence_ids=["evidence:one"],
    )
    project = _analysis_project(tmp_path, records)

    result_metrics = json.loads(
        build_outputs(project)["metrics.json"].read_text(encoding="utf-8")
    )
    # Target, work and axis form one component. Evidence and the second work are
    # isolated once the retired citation is excluded.
    assert result_metrics["weakly_connected_components"] == 3


def test_jsonld_uses_owned_terms_stable_iris_references_and_datatypes():
    registry = OntologyRegistry(bundled_ontology_path("domains", "recon.yaml"))
    canonical = {
        "meta": {},
        "nodes": [
            {
                "id": "root entity",
                "type": "Entity",
                "name": "Root entity",
                "created_at": "2026-09-02T12:00:00+00:00",
            },
            {
                "id": "evidence:one",
                "type": "EvidenceAttachment",
                "label": "Evidence",
                "description": "Inspected source.",
                "source_uri": "https://example.org/source",
            },
            {
                "id": "work:one",
                "type": "Work",
                "label": "Work",
                "priority_date": "2025-01-01",
                "evidence_ids": ["evidence:one"],
            },
            {
                "id": "claim:one",
                "type": "Claim",
                "label": "Claim",
                "statement": "Claim text",
                "confidence": 0.75,
            },
            {"id": "axis:one", "type": "ComparisonAxis", "label": "Axis"},
        ],
        "edges": [
            {
                "id": "coverage:one",
                "type": "CoversAxisRelation",
                "source_id": "work:one",
                "target_id": "axis:one",
                "relation_type": "COVERS_AXIS",
                "evidence_ids": ["evidence:one"],
            }
        ],
    }
    document = analysis._jsonld(canonical, registry)
    record_iri = analysis._record_iri
    edge = next(
        item
        for item in document["@graph"]
        if item["@id"] == record_iri("coverage:one")
    )
    assert edge["source_id"] == record_iri("work:one")
    assert edge["target_id"] == record_iri("axis:one")
    assert "source" not in edge
    assert "target" not in edge

    graph = Graph().parse(data=json.dumps(document), format="json-ld")
    root = "https://malleus.dev/schema/"
    recon = "https://malleus.dev/schema/recon/"
    assert (
        URIRef(record_iri("coverage:one")),
        URIRef(root + "source_id"),
        URIRef(record_iri("work:one")),
    ) in graph
    assert (
        URIRef(record_iri("coverage:one")),
        URIRef(root + "target_id"),
        URIRef(record_iri("axis:one")),
    ) in graph
    assert (
        URIRef(record_iri("work:one")),
        URIRef(recon + "evidence_ids"),
        URIRef(record_iri("evidence:one")),
    ) in graph
    assert (
        URIRef(record_iri("root entity")),
        RDF.type,
        URIRef(root + "Entity"),
    ) in graph
    assert (
        URIRef(record_iri("work:one")),
        RDF.type,
        URIRef(recon + "Work"),
    ) in graph
    assert (
        URIRef(record_iri("work:one")),
        URIRef(recon + "priority_date"),
        Literal("2025-01-01", datatype=XSD.date),
    ) in graph
    assert (
        URIRef(record_iri("claim:one")),
        URIRef(recon + "confidence"),
        Literal(0.75, datatype=XSD.float),
    ) in graph
    assert (
        URIRef(record_iri("root entity")),
        URIRef(root + "created_at"),
        Literal("2026-09-02T12:00:00+00:00", datatype=XSD.dateTime),
    ) in graph
    assert (
        URIRef(record_iri("evidence:one")),
        URIRef(recon + "source_uri"),
        Literal("https://example.org/source", datatype=XSD.anyURI),
    ) in graph
    assert not any(predicate == URIRef(recon + "source") for _, predicate, _ in graph)


def test_jsonld_context_tracks_ontology_ownership_ranges_and_classes():
    root_path = bundled_ontology_path("malleus.yaml")
    recon_path = bundled_ontology_path("domains", "recon.yaml")
    root = yaml.safe_load(root_path.read_text(encoding="utf-8"))
    recon = yaml.safe_load(recon_path.read_text(encoding="utf-8"))
    registry = OntologyRegistry(recon_path)
    root_slots = set(root["slots"])
    recon_slots = set(recon["slots"])
    context = analysis._jsonld_context(registry, registry.type_names())
    for slot_name, definition in context.items():
        iri = definition["@id"] if isinstance(definition, dict) else definition
        assert slot_name in root_slots | recon_slots
        source = root_path if slot_name in root_slots else recon_path
        assert iri == analysis._schema_terms(source, "slots")[slot_name]

    assert context["priority_date"]["@type"] == str(XSD.date)
    assert context["occurred_at"]["@type"] == str(XSD.dateTime)
    assert context["source_uri"]["@type"] == str(XSD.anyURI)
    assert context["confidence"]["@type"] == str(XSD.float)
    assert context["source_id"]["@type"] == "@id"
    root_class_terms = analysis._schema_terms(root_path, "classes")
    recon_class_terms = analysis._schema_terms(recon_path, "classes")
    ontology = analysis._jsonld_ontology(registry)
    for type_name in registry.type_names():
        expected = (
            root_class_terms[type_name]
            if type_name in root_class_terms
            else recon_class_terms[type_name]
        )
        assert analysis._ontology_iri(
            type_name,
            ontology.classes,
            kind="class",
        ) == expected
    assert "@vocab" not in context
    assert "malleus" not in context
    assert "recon" not in context


@pytest.mark.parametrize("identifier", ["", "   ", None])
def test_jsonld_refuses_blank_or_non_string_record_iris(identifier):
    with pytest.raises(ReconError, match="identifiers must be nonblank strings"):
        analysis._record_iri(identifier)


def test_manifest_commits_structural_profile_generator_and_source_identity(tmp_path):
    project = _analysis_project(tmp_path)
    (project.root / "ledger.jsonl").write_text("rejected private record", encoding="utf-8")

    paths = build_outputs(project)
    manifest_body = paths["manifest.json"].read_bytes()
    manifest = json.loads(manifest_body)
    project_body = (project.root / "project.json").read_bytes()
    assert manifest["schema_version"] == "3"
    assert manifest["state"] == "COMMITTED"
    assert manifest["profile"] == "malleus.recon.structural-capture/v1"
    assert manifest["generator"] == analysis._LOADED_GENERATOR_IDENTITY
    assert manifest["generator"]["package_version"] == IMPLEMENTATION_STATUS.package_version
    implementation = manifest["generator"]["implementation"]
    assert implementation["schema_version"] == "1"
    assert [component["name"] for component in implementation["components"]] == [
        name for name, _ in analysis._IMPLEMENTATION_SOURCES
    ]
    assert all(
        set(component) == {"name", "bytes", "sha256"}
        for component in implementation["components"]
    )
    assert implementation["closure"] == analysis._file_identity(
        analysis._json_text(
            {
                "schema_version": implementation["schema_version"],
                "components": implementation["components"],
            }
        ).encode("utf-8")
    )
    assert manifest["runtime"] == analysis._BUILD_RUNTIME
    assert manifest["project"] == {
        "name": "project.json",
        "bytes": len(project_body),
        "sha256": hashlib.sha256(project_body).hexdigest(),
    }
    assert manifest["ontology_hash"] == project.ontology_hash
    assert manifest["ledger_head"] == project._events[-1]["event_hash"]
    assert manifest["event_count"] == len(project._events)

    with zipfile.ZipFile(paths["recon_bundle.zip"]) as bundle:
        assert bundle.namelist() == manifest["archive"]["members"]
        assert bundle.read("manifest.json") == manifest_body
        assert "project.json" not in bundle.namelist()
        assert "ledger.jsonl" not in bundle.namelist()


def test_manifest_cannot_authorize_deletion_of_an_arbitrary_file(tmp_path):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    destination = paths["manifest.json"].parent
    stale = destination / "obsolete.txt"
    stale.write_bytes(b"obsolete generated output")
    sentinel = destination / "reviewer-notes.txt"
    sentinel.write_bytes(b"preserve me")

    manifest = json.loads(paths["manifest.json"].read_text(encoding="utf-8"))
    manifest["files"][stale.name] = {
        "bytes": stale.stat().st_size,
        "sha256": hashlib.sha256(stale.read_bytes()).hexdigest(),
    }
    manifest["archive"]["members"] = sorted(
        {*manifest["files"], "manifest.json"}
    )
    manifest_body = analysis._json_text(manifest).encode("utf-8")
    paths["manifest.json"].write_bytes(manifest_body)
    archive_members = {
        name: (destination / name).read_bytes() for name in manifest["files"]
    }
    archive_members["manifest.json"] = manifest_body
    analysis._write_zip(paths["recon_bundle.zip"], archive_members)

    build_outputs(project)
    assert stale.read_bytes() == b"obsolete generated output"
    assert sentinel.read_bytes() == b"preserve me"


@pytest.mark.parametrize(
    "field,value",
    [
        ("profile", "some-other-profile"),
        ("generator", {"name": "not-recon"}),
    ],
)
def test_foreign_manifest_identity_grants_no_deletion_authority(
    tmp_path, field, value
):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    destination = paths["manifest.json"].parent
    manifest = json.loads(paths["manifest.json"].read_text(encoding="utf-8"))
    manifest[field] = value
    manifest_body = analysis._json_text(manifest).encode("utf-8")
    paths["manifest.json"].write_bytes(manifest_body)
    archive_members = {
        name: (destination / name).read_bytes() for name in manifest["files"]
    }
    archive_members["manifest.json"] = manifest_body
    analysis._write_zip(paths["recon_bundle.zip"], archive_members)

    assert analysis._existing_managed_files(destination) == set()


def test_staging_failure_leaves_previous_committed_build_unchanged(
    tmp_path, monkeypatch
):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    before = {name: path.read_bytes() for name, path in paths.items()}

    def fail_archive(path, files):
        raise OSError("simulated staging failure")

    monkeypatch.setattr(analysis, "_write_zip", fail_archive)
    with pytest.raises(ReconError, match="without a torn manifest"):
        build_outputs(project)
    assert {name: path.read_bytes() for name, path in paths.items()} == before


def test_staging_cleanup_failure_does_not_mask_precommit_failure(
    tmp_path, monkeypatch
):
    project = _analysis_project(tmp_path)
    original_cleanup = analysis.tempfile.TemporaryDirectory.cleanup

    def fail_archive(path, files):
        raise OSError("primary staging failure")

    def fail_staging_cleanup(temporary):
        if temporary.name.endswith(".staging"):
            raise RuntimeError("secondary cleanup failure")
        return original_cleanup(temporary)

    monkeypatch.setattr(analysis, "_write_zip", fail_archive)
    monkeypatch.setattr(
        analysis.tempfile.TemporaryDirectory,
        "cleanup",
        fail_staging_cleanup,
    )
    with pytest.raises(ReconError, match="primary staging failure"):
        build_outputs(project)


def test_manifest_inspection_runs_under_cross_process_destination_lock(
    tmp_path, monkeypatch
):
    project = _analysis_project(tmp_path)
    original = analysis._existing_managed_files
    observed = []

    def inspect(destination, expected_generator=None):
        context = multiprocessing.get_context("spawn")
        queue = context.Queue()
        process = context.Process(
            target=_analysis_probe_build_lock,
            args=(str(destination), queue),
        )
        process.start()
        process.join(15)
        assert process.exitcode == 0
        observed.append(queue.get(timeout=2))
        return original(destination, expected_generator)

    monkeypatch.setattr(analysis, "_existing_managed_files", inspect)
    build_outputs(project)

    assert len(observed) == 1
    assert "active builder" in observed[0]


def test_build_lock_distinguishes_io_failure_and_closes_stream(tmp_path, monkeypatch):
    class Stream:
        closed = False

        def fileno(self):
            return 41

        def close(self):
            self.closed = True

    stream = Stream()
    closed = []
    monkeypatch.setattr(analysis.os, "open", lambda *args, **kwargs: 41)
    monkeypatch.setattr(analysis.os, "fdopen", lambda *args, **kwargs: stream)
    monkeypatch.setattr(analysis.os, "close", closed.append)
    monkeypatch.setattr(analysis, "_assert_reserved_lock_identity", lambda *args: None)

    def fail_acquire(_stream):
        raise OSError(errno.EIO, "simulated lock I/O failure")

    monkeypatch.setattr(analysis, "_acquire_build_lock", fail_acquire)
    with pytest.raises(ReconError, match="Could not acquire Recon build lock") as failure:
        with analysis._exclusive_build(tmp_path / "build"):
            pytest.fail("I/O failure must not enter the transaction")
    assert "active builder" not in str(failure.value)
    assert stream.closed
    assert closed == [41]


def test_winerror_36_is_not_classified_as_lock_contention():
    error = OSError("sharing violation")
    error.winerror = 36
    assert not analysis._is_lock_contention(error)


def test_build_lock_stream_close_failure_cannot_close_a_reused_descriptor(
    tmp_path, monkeypatch
):
    project = _analysis_project(tmp_path)
    original_fdopen = analysis.os.fdopen
    opened = {}
    replacement_path = tmp_path / "replacement.txt"

    class FailingCloseLock:
        def __init__(self, stream, descriptor):
            self.stream = stream
            self.descriptor = descriptor

        def fileno(self):
            return self.descriptor

        def close(self):
            self.stream.close()
            opened["replacement"] = analysis.os.open(
                replacement_path,
                analysis.os.O_RDWR | analysis.os.O_CREAT,
                0o600,
            )
            raise OSError("simulated close failure")

    def wrapping_fdopen(descriptor, mode, *, closefd):
        assert closefd is False
        opened["lock"] = descriptor
        return FailingCloseLock(
            original_fdopen(descriptor, mode, closefd=closefd),
            descriptor,
        )

    monkeypatch.setattr(analysis.os, "fdopen", wrapping_fdopen)

    paths = build_outputs(project)
    replacement = opened["replacement"]
    try:
        assert paths["manifest.json"].is_file()
        assert replacement != opened["lock"]
        analysis.os.fstat(replacement)
    finally:
        analysis.os.close(replacement)


def test_build_lock_hard_interrupt_still_releases_for_real_reacquisition(
    tmp_path, monkeypatch
):
    destination = tmp_path / "build"
    original = analysis._release_build_lock
    releases = 0

    def interrupt_first_release(stream):
        nonlocal releases
        releases += 1
        if releases == 1:
            raise KeyboardInterrupt("simulated lock release interruption")
        return original(stream)

    monkeypatch.setattr(analysis, "_release_build_lock", interrupt_first_release)
    with pytest.raises(KeyboardInterrupt, match="lock release interruption"):
        with analysis._exclusive_build(destination):
            pass
    with analysis._exclusive_build(destination):
        pass
    assert releases == 2


def test_build_lock_cleanup_interrupt_does_not_mask_the_body_failure(
    tmp_path, monkeypatch
):
    destination = tmp_path / "build"

    def interrupt_release(stream):
        raise KeyboardInterrupt("simulated lock release interruption")

    monkeypatch.setattr(analysis, "_release_build_lock", interrupt_release)
    with pytest.raises(RuntimeError, match="primary build failure"):
        with analysis._exclusive_build(destination):
            raise RuntimeError("primary build failure")

    monkeypatch.undo()
    with analysis._exclusive_build(destination):
        pass


def test_build_lock_refuses_a_symlink_without_touching_its_target(tmp_path):
    destination = tmp_path / "build"
    destination.mkdir()
    target = tmp_path / "unrelated"
    target.write_bytes(b"")
    lock = destination / analysis._BUILD_LOCK_NAME
    try:
        lock.symlink_to(target)
    except OSError as error:
        pytest.skip(f"file symlink unavailable: {error}")

    with pytest.raises(ReconError, match="Recon build lock"):
        with analysis._exclusive_build(destination):
            pytest.fail("symlink lock must not be acquired")
    assert target.read_bytes() == b""


def test_build_lock_refuses_a_hard_link_without_touching_its_target(tmp_path):
    destination = tmp_path / "build"
    destination.mkdir()
    target = tmp_path / "unrelated"
    target.write_bytes(b"")
    lock = destination / analysis._BUILD_LOCK_NAME
    try:
        lock.hardlink_to(target)
    except OSError as error:
        pytest.skip(f"file hard link unavailable: {error}")

    with pytest.raises(ReconError, match="single-link regular file"):
        with analysis._exclusive_build(destination):
            pytest.fail("hard-linked lock must not be acquired")
    assert target.read_bytes() == b""


def test_archive_fsync_uses_a_writable_descriptor(tmp_path, monkeypatch):
    archive = tmp_path / "recon_bundle.zip"
    archive.write_bytes(b"archive")
    original = Path.open
    modes = []

    def track_open(path, mode="r", *args, **kwargs):
        if path == archive:
            modes.append(mode)
        return original(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", track_open)
    analysis._fsync_file(archive)
    assert modes == ["r+b"]


def test_commit_failure_removes_manifest_commit_marker(tmp_path, monkeypatch):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    destination = paths["manifest.json"].parent
    original_replace = Path.replace

    def fail_during_commit(path, target):
        if path.name == "metrics.json" and Path(target).parent == destination:
            raise OSError("simulated commit failure")
        return original_replace(path, target)

    monkeypatch.setattr(Path, "replace", fail_during_commit)
    with pytest.raises(ReconError, match="without a torn manifest"):
        build_outputs(project)
    assert not (destination / "manifest.json").exists()


def test_manifest_commit_marker_is_replaced_last(tmp_path, monkeypatch):
    project = _analysis_project(tmp_path)
    destination = project.root / "build"
    original_replace = Path.replace
    committed = []

    def track_commit(path, target):
        if Path(target).parent == destination:
            committed.append(Path(target).name)
        return original_replace(path, target)

    monkeypatch.setattr(Path, "replace", track_commit)
    build_outputs(project)
    assert committed[-2:] == ["recon_bundle.zip", "manifest.json"]


def test_windows_does_not_attempt_unsupported_directory_fsync(tmp_path, monkeypatch):
    monkeypatch.setattr(analysis.os, "name", "nt")

    def unsupported_open(*args, **kwargs):
        pytest.fail("Windows directory handles cannot be opened through os.open")

    monkeypatch.setattr(analysis.os, "open", unsupported_open)
    analysis._fsync_directory(tmp_path)


def test_torn_existing_build_is_recovered_without_deleting_unknown_files(tmp_path):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    unknown = paths["manifest.json"].parent / "reviewer-notes.txt"
    unknown.write_bytes(b"preserve me")
    paths["metrics.json"].write_bytes(b"tampered")

    rebuilt = build_outputs(project)
    manifest = json.loads(rebuilt["manifest.json"].read_text(encoding="utf-8"))
    assert manifest["state"] == "COMMITTED"
    assert rebuilt["metrics.json"].read_bytes() != b"tampered"
    assert unknown.read_bytes() == b"preserve me"


def test_build_refuses_to_invent_missing_project_identity(tmp_path):
    project = _analysis_project(tmp_path)
    (project.root / "project.json").unlink()

    with pytest.raises(ReconError, match="Cannot bind exact project.json bytes"):
        build_outputs(project)


def test_build_refuses_filesystem_and_loaded_project_config_divergence(tmp_path):
    project = _analysis_project(tmp_path)
    changed = dict(project.config)
    changed["title"] = "Changed behind the loaded project"
    (project.root / "project.json").write_text(
        json.dumps(changed),
        encoding="utf-8",
    )

    with pytest.raises(ReconError, match="differs from the loaded project configuration"):
        build_outputs(project)


def test_build_refuses_duplicate_project_config_keys_even_when_last_value_matches(
    tmp_path,
):
    project = _analysis_project(tmp_path)
    body = json.dumps(project.config)
    (project.root / "project.json").write_text(
        body.replace("{", '{"title":"shadow",', 1),
        encoding="utf-8",
    )

    with pytest.raises(ReconError, match="duplicate JSON key 'title'"):
        build_outputs(project)


def test_build_refuses_project_byte_change_during_generation(tmp_path, monkeypatch):
    project = _analysis_project(tmp_path)
    original = analysis._bibtex

    def mutate_project(records):
        result = original(records)
        path = project.root / "project.json"
        path.write_text(
            json.dumps(project.config, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return result

    monkeypatch.setattr(analysis, "_bibtex", mutate_project)
    with pytest.raises(ReconError, match="project.json changed during generation"):
        build_outputs(project)


def test_bibtex_keys_are_collision_free_for_sanitization_collisions():
    records = {
        "work:a-b": _analysis_stored(
            "Work",
            "work:a-b",
            title="First",
            review_state="REVIEWED",
        ),
        "work:a_b": _analysis_stored(
            "Work",
            "work:a_b",
            title="Second",
            review_state="REVIEWED",
        ),
    }
    keys = re.findall(r"^@misc\{([^,]+),", analysis._bibtex(records), flags=re.MULTILINE)
    assert len(keys) == 2
    assert len(set(keys)) == 2
    assert keys == [analysis._bibtex_key("work:a-b"), analysis._bibtex_key("work:a_b")]


def test_bibtex_escaping_does_not_reescape_generated_commands():
    value = r"slash\ braces{} 100% R&D $x #1 under_score ~caret^"
    assert analysis._bibtex_escape(value) == (
        r"slash\textbackslash{} braces\{\} 100\% R\&D \$x \#1 "
        r"under\_score \textasciitilde{}caret\textasciicircum{}"
    )


@pytest.mark.parametrize(
    "missing", ["jsonld_ontology", "ontology_verification", "runtime"]
)
def test_incomplete_v3_manifest_grants_no_deletion_authority(tmp_path, missing):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    manifest = json.loads(paths["manifest.json"].read_text(encoding="utf-8"))
    manifest.pop(missing)
    paths["manifest.json"].write_text(analysis._json_text(manifest), encoding="utf-8")

    assert analysis._existing_managed_files(paths["manifest.json"].parent) == set()


@pytest.mark.parametrize(
    "malformation",
    [
        "relative source",
        "duplicate source",
        "unretained import target",
        "unretained definition owner",
        "unordered imports",
        "orphan source",
    ],
)
def test_malformed_v3_ontology_closure_grants_no_deletion_authority(
    tmp_path, malformation
):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    manifest = json.loads(paths["manifest.json"].read_text(encoding="utf-8"))
    closure = manifest["jsonld_ontology"]
    if malformation == "relative source":
        closure["sources"][0]["resolved_locator"] = "relative/recon.yaml"
    elif malformation == "duplicate source":
        closure["sources"][1]["resolved_locator"] = closure["sources"][0][
            "resolved_locator"
        ]
    elif malformation == "unretained import target":
        edge = next(item for item in closure["imports"] if item["target_role"] == "ontology")
        edge["resolved_locator"] = str((tmp_path / "unretained.yaml").resolve())
    elif malformation == "unretained definition owner":
        closure["definitions"][0]["source_locator"] = str(
            (tmp_path / "unretained.yaml").resolve()
        )
    elif malformation == "unordered imports":
        closure["imports"].reverse()
    else:
        closure["sources"].append(
            {
                "source_role": "import",
                "resolved_locator": str((tmp_path / "orphan.yaml").resolve()),
                "bytes": 0,
                "sha256": hashlib.sha256(b"").hexdigest(),
            }
        )
        closure["sources"][1:] = sorted(
            closure["sources"][1:], key=lambda item: item["resolved_locator"]
        )
    paths["manifest.json"].write_text(
        analysis._json_text(manifest), encoding="utf-8"
    )

    assert analysis._existing_managed_files(paths["manifest.json"].parent) == set()


@pytest.mark.parametrize(
    "malformation",
    ["category collision", "unexplained receipt", "wrong current identity"],
)
def test_malformed_v3_migration_evidence_grants_no_deletion_authority(
    tmp_path, malformation
):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    manifest = json.loads(paths["manifest.json"].read_text(encoding="utf-8"))
    evidence = manifest["ontology_verification"]
    identity = project.ontology_hash
    if malformation == "category collision":
        evidence["migrated_ontology_hashes"] = [identity]
        evidence["verified_ontology_hashes"] = [identity, identity]
        evidence["receipt_digests"] = ["sha256:" + "a" * 64]
    elif malformation == "unexplained receipt":
        evidence["receipt_digests"] = ["sha256:" + "a" * 64]
    else:
        evidence["current_ontology_hash"] = "sha256:" + "a" * 64
    paths["manifest.json"].write_text(
        analysis._json_text(manifest), encoding="utf-8"
    )

    assert analysis._existing_managed_files(paths["manifest.json"].parent) == set()


@pytest.mark.parametrize(
    "hostile_name",
    ["..", r"..\outside", r"C:\outside", "CON", "trailing.", "/absolute"],
)
def test_manifest_output_names_are_a_host_independent_closed_set(
    tmp_path, hostile_name
):
    project = _analysis_project(tmp_path)
    paths = build_outputs(project)
    manifest = json.loads(paths["manifest.json"].read_text(encoding="utf-8"))
    identity = manifest["files"].pop("metrics.json")
    manifest["files"][hostile_name] = identity
    manifest["archive"]["members"] = sorted({*manifest["files"], "manifest.json"})
    paths["manifest.json"].write_text(analysis._json_text(manifest), encoding="utf-8")

    assert analysis._existing_managed_files(paths["manifest.json"].parent) == set()


def test_generator_identity_is_bound_to_loaded_implementation_bytes(
    tmp_path, monkeypatch
):
    name, source = analysis._IMPLEMENTATION_SOURCES[0]
    changed_source = tmp_path / source.name
    changed_source.write_bytes(source.read_bytes() + b"\n# changed after import\n")
    monkeypatch.setattr(
        analysis,
        "_IMPLEMENTATION_SOURCES",
        ((name, changed_source), *analysis._IMPLEMENTATION_SOURCES[1:]),
    )

    current = analysis._read_generator_identity()
    assert current["implementation"]["closure"] != (
        analysis._LOADED_GENERATOR_IDENTITY["implementation"]["closure"]
    )
    with pytest.raises(ReconError, match="differ from the code loaded"):
        analysis._generator_identity()


def test_generator_identity_refuses_an_unreadable_bound_source(tmp_path, monkeypatch):
    monkeypatch.setattr(
        analysis,
        "_IMPLEMENTATION_SOURCES",
        (("malleus.recon.analysis", tmp_path / "missing.py"),),
    )
    with pytest.raises(ReconError, match="Cannot bind Recon generator implementation"):
        analysis._generator_identity()


def test_jsonld_refuses_live_structural_bytes_that_differ_from_loaded_registry(
    tmp_path,
):
    project = _analysis_project(tmp_path)
    source = bundled_ontology_path("domains", "recon.yaml")
    local = tmp_path / "recon.yaml"
    local.write_bytes(source.read_bytes())
    registry = OntologyRegistry(
        local,
        import_map={"malleus": bundled_ontology_path("malleus.yaml")},
    )
    _analysis_use_registry(project, registry)
    body = local.read_text(encoding="utf-8")
    changed = body.replace("  source_uri:\n    range: uri", "  source_uri:\n    range: integer", 1)
    assert changed != body
    local.write_text(changed, encoding="utf-8")

    with pytest.raises(ReconError, match="ontology entry source .* changed"):
        build_outputs(project)


def test_jsonld_ontology_source_change_during_generation_fails_closed(
    tmp_path, monkeypatch
):
    project = _analysis_project(tmp_path)
    source = bundled_ontology_path("domains", "recon.yaml")
    local = tmp_path / "recon.yaml"
    local.write_bytes(source.read_bytes())
    _analysis_use_registry(
        project,
        OntologyRegistry(
            local,
            import_map={"malleus": bundled_ontology_path("malleus.yaml")},
        ),
    )
    original = analysis._report

    def mutate_source(*args, **kwargs):
        result = original(*args, **kwargs)
        local.write_bytes(local.read_bytes() + b"\n# changed during build\n")
        return result

    monkeypatch.setattr(analysis, "_report", mutate_source)
    with pytest.raises(ReconError, match="ontology entry source .* changed during generation"):
        build_outputs(project)


def test_jsonld_transitive_source_change_during_generation_fails_closed(
    tmp_path, monkeypatch
):
    project = _analysis_project(tmp_path)
    root = tmp_path / "malleus.yaml"
    local = tmp_path / "recon.yaml"
    root.write_bytes(bundled_ontology_path("malleus.yaml").read_bytes())
    local.write_bytes(bundled_ontology_path("domains", "recon.yaml").read_bytes())
    _analysis_use_registry(
        project,
        OntologyRegistry(local, import_map={"malleus": root}),
    )
    original = analysis._report

    def mutate_import(*args, **kwargs):
        result = original(*args, **kwargs)
        root.write_bytes(root.read_bytes() + b"\n# changed during build\n")
        return result

    monkeypatch.setattr(analysis, "_report", mutate_import)
    with pytest.raises(
        ReconError,
        match="ontology import source .*malleus.yaml changed during generation",
    ):
        build_outputs(project)


def test_schema_id_and_prefix_only_change_is_bound_without_stale_jsonld_metadata(
    tmp_path,
):
    project = _analysis_project(tmp_path)
    baseline = json.loads(
        build_outputs(project, tmp_path / "baseline")["manifest.json"].read_text(
            encoding="utf-8"
        )
    )
    source = bundled_ontology_path("domains", "recon.yaml")
    local = tmp_path / "recon.yaml"
    body = source.read_text(encoding="utf-8")
    changed = body.replace(
        "id: https://malleus.dev/schema/recon",
        "id: https://example.org/custom-recon",
        1,
    ).replace(
        "  recon: https://malleus.dev/schema/recon/",
        "  recon: https://example.org/custom-recon/",
        1,
    )
    assert changed != body
    local.write_text(changed, encoding="utf-8")
    registry = OntologyRegistry(
        local,
        import_map={"malleus": bundled_ontology_path("malleus.yaml")},
    )
    assert registry.content_hash() == project.registry.content_hash()
    _analysis_use_registry(project, registry)

    paths = build_outputs(project, tmp_path / "changed")
    manifest = json.loads(paths["manifest.json"].read_text(encoding="utf-8"))
    document = json.loads(paths["literature_kg.jsonld"].read_text(encoding="utf-8"))
    work = next(item for item in document["@graph"] if item["@id"].endswith("work%3Aone"))
    assert work["@type"] == "https://example.org/custom-recon/Work"
    assert {"@vocab", "malleus", "recon"}.isdisjoint(document["@context"])
    assert manifest["ontology_hash"] == baseline["ontology_hash"]
    assert manifest["jsonld_ontology"] != baseline["jsonld_ontology"]


@pytest.mark.parametrize(
    "old,new,error",
    [
        (
            "id: https://malleus.dev/schema/recon",
            "id: relative/recon",
            "schema id.*absolute IRI",
        ),
        (
            "  recon: https://malleus.dev/schema/recon/",
            "  recon: relative/recon/",
            "expansion must be an absolute IRI",
        ),
        (
            "  recon: https://malleus.dev/schema/recon/",
            "  recon:\n    invalid: expansion",
            "expansion must be an absolute IRI",
        ),
    ],
)
def test_jsonld_refuses_relative_schema_or_prefix_iris(tmp_path, old, new, error):
    project = _analysis_project(tmp_path)
    source = bundled_ontology_path("domains", "recon.yaml")
    local = tmp_path / "recon.yaml"
    body = source.read_text(encoding="utf-8")
    changed = body.replace(old, new, 1)
    assert changed != body
    local.write_text(changed, encoding="utf-8")
    registry = OntologyRegistry(
        local,
        import_map={"malleus": bundled_ontology_path("malleus.yaml")},
    )
    assert registry.content_hash() == project.registry.content_hash()
    _analysis_use_registry(project, registry)

    with pytest.raises(ReconError, match=error):
        build_outputs(project)


def test_graphml_refuses_xml_invalid_source_data_without_mutating_it():
    value = "invalid\x01value"
    graph = nx.MultiDiGraph()
    graph.add_node("node:one", label=value)

    with pytest.raises(ReconError, match="source value contains an XML-invalid character"):
        analysis._graphml_bytes(graph)
    assert graph.nodes["node:one"]["label"] == value


def test_xml_invalid_but_ontology_valid_record_cannot_torn_a_committed_build(tmp_path):
    project = _project(tmp_path)
    paths = build_outputs(project)
    committed = {name: path.read_bytes() for name, path in paths.items()}
    stored = project.current_records()["work:paper-a"]
    changed = deepcopy(stored.record)
    changed["title"] = "Paper with invalid XML \x00 content"
    _record(project, "Work", changed, supersedes=stored.event_id)

    with pytest.raises(ReconError, match="source value contains an XML-invalid character"):
        build_outputs(project)
    assert {name: path.read_bytes() for name, path in paths.items()} == committed
    assert project.current_records()["work:paper-a"].record["title"] == changed["title"]


def test_markdown_code_span_handles_backslashes_pipes_and_any_backtick_run():
    value = "`start````back\\slash|<tag>\nnext`"
    span = analysis._markdown_code_span(value)
    rendered = MarkdownIt("commonmark").enable("table").render(
        "| Value | Other |\n|---|---|\n| " + span + " | intact |\n"
    )
    root = ET.fromstring(f"<root>{rendered}</root>")

    assert len(root.findall(".//tr")) == 2
    assert len(root.findall(".//tbody/tr/td")) == 2
    assert root.find(".//code").text == value.replace("\n", " ")
    assert root.findall(".//tbody/tr/td")[1].text == "intact"


def test_report_escapes_adversarial_headings_tables_ids_and_raw_html(tmp_path):
    records = _analysis_records()
    identifier = "work\\|````<id>\nnext"
    work = records.pop("work:one")
    work.record["id"] = identifier
    work.record["title"] = "Title | break\\out\n<script>owned</script> `ticks`"
    records[identifier] = work
    records["coverage:work:active"].record["source_id"] = identifier
    project = _analysis_project(tmp_path, records)
    project.config["title"] = "# forged\n<style>body{display:none}</style> | root\\"
    (project.root / "project.json").write_text(
        json.dumps(project.config, indent=4, sort_keys=False) + "  \n",
        encoding="utf-8",
    )

    paths = build_outputs(project)
    report = paths["report.md"].read_text(encoding="utf-8")
    rendered = MarkdownIt("commonmark").enable("table").render(report)
    root = ET.fromstring(f"<root>{rendered}</root>")
    canonical = json.loads(paths["literature_kg.json"].read_text(encoding="utf-8"))

    assert root.find("h1").text == project.config["title"].replace("\n", " ")
    assert not root.findall(".//script")
    assert not root.findall(".//style")
    assert len(root.findall("table")) == 2
    assert len(root.findall(".//tbody/tr/td")) == 12
    assert identifier.replace("\n", " ") in [item.text for item in root.findall(".//code")]
    assert canonical["meta"]["title"] == project.config["title"]
    canonical_work = next(item for item in canonical["nodes"] if item["type"] == "Work")
    assert canonical_work["id"] == identifier
    assert canonical_work["title"] == work.record["title"]


def test_staging_is_inside_destination_to_avoid_mount_boundary_replace(
    tmp_path, monkeypatch
):
    project = _analysis_project(tmp_path)
    destination = project.root / "build"
    original = Path.replace

    def reject_sibling_stage(path, target):
        target = Path(target)
        if target.parent == destination and destination not in path.parents:
            raise OSError(errno.EXDEV, "simulated mount boundary")
        return original(path, target)

    monkeypatch.setattr(Path, "replace", reject_sibling_stage)
    paths = build_outputs(project)
    assert paths["manifest.json"].is_file()


def test_cross_device_commit_error_is_actionable_and_fails_closed(tmp_path, monkeypatch):
    project = _analysis_project(tmp_path)
    destination = project.root / "build"
    original = Path.replace

    def fail_cross_device(path, target):
        if path.name == "metrics.json" and Path(target).parent == destination:
            raise OSError(errno.EXDEV, "simulated cross-device replace")
        return original(path, target)

    monkeypatch.setattr(Path, "replace", fail_cross_device)
    with pytest.raises(ReconError, match="staging and destination must be on the same filesystem"):
        build_outputs(project)
    assert not (destination / "manifest.json").exists()


def test_interrupt_during_final_manifest_fsync_removes_commit_marker(
    tmp_path, monkeypatch
):
    project = _analysis_project(tmp_path)
    destination = project.root / "build"
    original = analysis._fsync_directory
    calls = 0

    def interrupt_third_fsync(path):
        nonlocal calls
        calls += 1
        if calls == 3:
            raise KeyboardInterrupt("simulated interruption after manifest replace")
        return original(path)

    monkeypatch.setattr(analysis, "_fsync_directory", interrupt_third_fsync)
    with pytest.raises(KeyboardInterrupt, match="after manifest replace"):
        build_outputs(project)
    assert calls >= 4
    assert not (destination / "manifest.json").exists()


def test_build_reports_indeterminate_when_manifest_rollback_also_fails(
    tmp_path, monkeypatch
):
    project = _analysis_project(tmp_path)
    destination = project.root / "build"
    manifest_path = destination / "manifest.json"
    fsync_directory = analysis._fsync_directory
    unlink = Path.unlink
    calls = 0

    def fail_final_fsync(path):
        nonlocal calls
        calls += 1
        if calls == 3:
            raise OSError(errno.EIO, "simulated final directory sync failure")
        return fsync_directory(path)

    def fail_manifest_rollback(path, *, missing_ok=False):
        if path == manifest_path and path.exists() and calls >= 3:
            raise OSError(errno.EIO, "simulated manifest rollback failure")
        return unlink(path, missing_ok=missing_ok)

    monkeypatch.setattr(analysis, "_fsync_directory", fail_final_fsync)
    monkeypatch.setattr(Path, "unlink", fail_manifest_rollback)
    with pytest.raises(ReconError, match="outcome is indeterminate"):
        build_outputs(project)
    assert manifest_path.is_file()


def test_fixed_in_destination_lock_supports_a_long_valid_destination_name(tmp_path):
    destination = tmp_path / ("d" * 240)
    with analysis._exclusive_build(destination):
        assert (destination / analysis._BUILD_LOCK_NAME).is_file()


def test_recon_project_does_not_expose_a_public_mutable_ledger(tmp_path):
    project = _store_project(tmp_path)
    assert not hasattr(project, "ledger")
    with pytest.raises(AttributeError):
        _ = project.ledger


def test_writer_lock_closes_raw_descriptor_when_stream_initialization_fails(
    tmp_path, monkeypatch
):
    closed = []

    def fake_open(path, flags, mode):
        return 73

    def fail_fdopen(descriptor, mode, *, closefd):
        raise OSError(errno.EMFILE, "descriptor table full")

    def capture_close(descriptor):
        closed.append(descriptor)

    monkeypatch.setattr(recon_store.os, "open", fake_open)
    monkeypatch.setattr(recon_store.os, "fdopen", fail_fdopen)
    monkeypatch.setattr(recon_store.os, "close", capture_close)
    with pytest.raises(ReconError, match="Could not initialize Recon writer lock"):
        with recon_store._exclusive_writer(tmp_path / "writer.lock"):
            pytest.fail("lock body must not run")
    assert closed == [73]


def test_writer_lock_reports_open_acquisition_and_contention_failures_separately(
    tmp_path, monkeypatch
):
    path = tmp_path / "writer.lock"

    def fail_open(path, flags, mode):
        raise OSError(errno.EROFS, "read-only filesystem")

    monkeypatch.setattr(recon_store.os, "open", fail_open)
    with pytest.raises(ReconError, match="Could not open Recon writer lock"):
        with recon_store._exclusive_writer(path):
            pytest.fail("lock body must not run")

    monkeypatch.undo()

    def contend(stream):
        raise BlockingIOError(errno.EAGAIN, "locked")

    monkeypatch.setattr(recon_store, "_acquire_writer_lock", contend)
    with pytest.raises(ReconError, match="already has an active writer"):
        with recon_store._exclusive_writer(path):
            pytest.fail("lock body must not run")

    def fail_acquisition(stream):
        raise OSError(errno.EIO, "filesystem lock failure")

    monkeypatch.setattr(recon_store, "_acquire_writer_lock", fail_acquisition)
    with pytest.raises(ReconError, match="Could not acquire Recon writer lock") as raised:
        with recon_store._exclusive_writer(path):
            pytest.fail("lock body must not run")
    assert "active writer" not in str(raised.value)


def test_writer_lock_classifier_only_treats_winerror_33_as_contention():
    lock_violation = OSError(errno.EIO, "lock violation")
    lock_violation.winerror = 33
    sharing_buffer_exceeded = OSError(errno.EIO, "sharing buffer exceeded")
    sharing_buffer_exceeded.winerror = 36
    assert recon_store._is_lock_contention(lock_violation)
    assert not recon_store._is_lock_contention(sharing_buffer_exceeded)


def test_writer_cleanup_is_exact_and_does_not_turn_a_commit_into_apparent_failure(
    tmp_path, monkeypatch
):
    project = _store_project(tmp_path)
    fdopen = recon_store.os.fdopen
    lock_descriptors = []
    unrelated_descriptors = []

    class CloseFailingStream:
        def __init__(self, stream):
            self._stream = stream

        def __getattr__(self, name):
            return getattr(self._stream, name)

        def close(self):
            self._stream.close()
            unrelated_descriptors.append(
                recon_store.os.open(
                    tmp_path / f"unrelated-{len(unrelated_descriptors)}",
                    recon_store.os.O_RDWR | recon_store.os.O_CREAT,
                    0o600,
                )
            )
            raise OSError(errno.EIO, "injected stream close failure")

    def failing_fdopen(descriptor, mode, *, closefd):
        assert closefd is False
        lock_descriptors.append(descriptor)
        return CloseFailingStream(fdopen(descriptor, mode, closefd=closefd))

    def fail_release(stream):
        raise OSError(errno.EIO, "injected lock release failure")

    monkeypatch.setattr(recon_store.os, "fdopen", failing_fdopen)
    monkeypatch.setattr(recon_store, "_release_writer_lock", fail_release)
    try:
        event = project.record(
            "Work", _store_work("work:committed"), actor_id="reviewer:test"
        )
        assert event["sequence"] == 1
        assert len(project.events()) == 1

        with pytest.raises(RuntimeError, match="body failure"):
            with recon_store._exclusive_writer(project.root / recon_store._WRITER_LOCK_FILE):
                raise RuntimeError("body failure")
        assert len(project.events()) == 1
        assert len(lock_descriptors) == len(unrelated_descriptors) == 2
        for descriptor in unrelated_descriptors:
            recon_store.os.fstat(descriptor)
    finally:
        for descriptor in unrelated_descriptors:
            try:
                recon_store.os.close(descriptor)
            except OSError:
                pass


def test_writer_lock_closes_its_descriptor_after_a_release_interrupt(
    tmp_path, monkeypatch
):
    path = tmp_path / "writer.lock"

    def interrupt_release(stream):
        raise KeyboardInterrupt("simulated writer-lock release interruption")

    monkeypatch.setattr(recon_store, "_release_writer_lock", interrupt_release)
    with pytest.raises(KeyboardInterrupt, match="release interruption"):
        with recon_store._exclusive_writer(path):
            pass

    monkeypatch.undo()
    with recon_store._exclusive_writer(path):
        pass


def test_writer_lock_refuses_a_symlink_without_touching_its_target(tmp_path):
    path = tmp_path / "writer.lock"
    target = tmp_path / "unrelated"
    target.write_bytes(b"")
    try:
        path.symlink_to(target)
    except OSError as error:
        pytest.skip(f"file symlink unavailable: {error}")

    with pytest.raises(ReconError, match="Recon writer lock"):
        with recon_store._exclusive_writer(path):
            pytest.fail("symlink lock must not be acquired")
    assert target.read_bytes() == b""


def test_writer_lock_refuses_a_hard_link_without_touching_its_target(tmp_path):
    path = tmp_path / "writer.lock"
    target = tmp_path / "unrelated"
    target.write_bytes(b"")
    try:
        path.hardlink_to(target)
    except OSError as error:
        pytest.skip(f"file hard link unavailable: {error}")

    with pytest.raises(ReconError, match="single-link regular file"):
        with recon_store._exclusive_writer(path):
            pytest.fail("hard-linked lock must not be acquired")
    assert target.read_bytes() == b""


def test_recon_writer_lock_refuses_a_real_competing_process(tmp_path):
    project = _store_project(tmp_path)
    context = multiprocessing.get_context("spawn")
    ready = context.Event()
    release = context.Event()
    process = context.Process(
        target=_store_hold_writer_lock,
        args=(str(project.root / recon_store._WRITER_LOCK_FILE), ready, release),
    )
    process.start()
    try:
        assert ready.wait(10)
        with pytest.raises(ReconError, match="already has an active writer"):
            project.record("Work", _store_work("work:blocked"), actor_id="reviewer:test")
    finally:
        release.set()
        process.join(10)
        if process.is_alive():
            process.terminate()
            process.join(10)
    assert process.exitcode == 0
    committed = project.record(
        "Work", _store_work("work:after-release"), actor_id="reviewer:test"
    )
    assert committed["sequence"] == 1
