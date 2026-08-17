import csv
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

from malleus.ledger import LedgerError
from malleus.recon import (
    ReconError,
    ReconProject,
    RecordCandidate,
    build_outputs,
    bundled_contract_path,
    compare_subjects,
    visualize,
)
from malleus.recon.cli import main
from malleus.recon.import_v1 import import_literature_kg_v1
from malleus.recon.store import load_record_file


NOW = lambda: "2026-08-16T12:00:00+00:00"


def test_bundled_contract_is_resolvable():
    path = bundled_contract_path()
    assert path.name == "RECON_CONTRACT.md"
    assert path.read_text(encoding="utf-8").startswith("# Malleus Recon contract")


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


def test_comparison_reports_exact_set_algebra_and_keeps_partial_separate(tmp_path):
    project = _project(tmp_path)
    result = compare_subjects(project, "target:malleus", "work:paper-a")
    assert result["intersection"] == ["axis:atomic"]
    assert result["union"] == ["axis:atomic", "axis:history", "axis:sandbox"]
    assert result["target_difference"] == ["axis:history"]
    assert result["work_difference"] == ["axis:sandbox"]
    assert result["symmetric_difference"] == ["axis:history", "axis:sandbox"]
    assert result["partial_or_adjacent"]["axis:history"]["work"] == "PARTIAL"
    assert result["unresolved"]["axis:sandbox"]["target"] == "NOT_ESTABLISHED"
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
    assert any(item["@id"] == "work:paper-a" for item in jsonld["@graph"])
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
