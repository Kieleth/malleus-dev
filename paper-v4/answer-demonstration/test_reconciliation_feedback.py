"""Feedback is a separate condition, never an alteration of the rejected run."""

import json
from pathlib import Path
import subprocess
import sys

import pytest
import repair
from review_packet import digest


def condition():
    return {
        "schema": "malleus.paper-v4.reconciliation/v1",
        "condition": "SOURCE_REVIEW_FEEDBACK_RECONCILIATION",
        "amendment_id": "reconciliation-feedback-01",
        "query_reader": "SubjectGraphReads",
    }


def test_feedback_uses_the_existing_reader_and_distinct_artifact_namespace():
    manifest = condition()
    assert repair.context(manifest) == (
        "evidence/producer/inputs",
        None,
        "SubjectGraphReads",
    )
    assert all(
        "reconciliation-feedback-01" in value
        for value in repair.artifact_ids(manifest, "evidence")
    )


@pytest.mark.parametrize(
    "key,value",
    [
        ("condition", "RCA_GUIDED_SIX_RECORD_RECONCILIATION"),
        ("condition", "UNDISCLOSED_RETRY"),
        ("amendment_id", "reconciliation-01"),
        ("query_reader", "GraphReads"),
    ],
)
def test_feedback_cannot_be_mislabelled_as_the_original_condition(key, value):
    manifest = condition()
    manifest[key] = value
    with pytest.raises(ValueError):
        repair.context(manifest)


def test_feedback_staging_preserves_original_and_separates_reviewer_inputs():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_reconciliation_feedback import check_stage; check_stage()",
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_feedback_keeps_the_accepted_baseline_coverage_requirements():
    import pilot

    root = pilot.ROOT / "private/paper-v4-answer-demonstration"
    assert (
        root / "sol-reconciliation-feedback-01/qualification-criteria.json"
    ).read_bytes() == (
        root / "sol-qualification-01/evidence/producer/inputs/argument-criteria.json"
    ).read_bytes()


def test_frozen_feedback_completion_binds_reviews_and_exact_reproduction():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_reconciliation_feedback import check_completed; check_completed()",
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_identical_historical_answers_keep_the_interpretation_disagreement_visible():
    import pilot

    root = pilot.ROOT / "private/paper-v4-answer-demonstration"
    run = root / "sol-reconciliation-feedback-01"
    old = json.loads(
        (root / "sol-calibration-01/b/subject-query-01/query-result.json").read_bytes()
    )
    before = json.loads((run / "before-query.json").read_bytes())

    def indexed(value):
        return {q["question_id"]: q for q in value["queries"]}

    old, before = indexed(old), indexed(before)
    outcome = json.loads((run / "outcome.json").read_bytes())
    comparison = outcome["historical_review_disagreement"]
    assert comparison["question_ids"] == ["CQ-T3-02", "CQ-C-05"]
    for key in comparison["question_ids"]:
        assert old[key] == before[key]
    assert comparison["limit"] == "NOT_A_LONGITUDINAL_COVERAGE_GAIN"
    assert (
        digest((root / comparison["earlier_review"]).read_bytes())
        == comparison["earlier_review_sha256"]
    )


def check_completed():
    import malleus.compiler as api
    import pilot
    from followup import verify_materials
    from reconciliation import authorize
    from reconciliation_query_review import changed_questions
    from review_packet import canonical

    run = (
        pilot.ROOT
        / "private/paper-v4-answer-demonstration/sol-reconciliation-feedback-01"
    )
    outcome = json.loads((run / "outcome.json").read_bytes())
    assert outcome["status"] == "ADMITTED_REPLAYED_ASSESSED"
    assert outcome["ratification"] == "PENDING_HUMAN"
    assert {
        "manifest.json",
        "source-review-01/manifest.json",
        "source-review-01/review.md",
        "source-review-01/decision.json",
        "query-review-01/manifest.json",
        "query-review-01/query-review.md",
        "evidence/attempt-01/run-result.json",
        "evidence/attempt-01/ledger/history.jsonl",
    } <= {item["path"] for item in outcome["materials"]}
    verify_materials(run, outcome["materials"])
    for directory in (run, run / "source-review-01", run / "query-review-01"):
        manifest = json.loads((directory / "manifest.json").read_bytes())
        verify_materials(directory, manifest["materials"])
    candidate_path = run / "evidence/producer/work/candidate-01.json"
    candidate = json.loads(candidate_path.read_bytes())
    decision = authorize(run, candidate_path)
    assert decision["ratification"] == "PENDING_HUMAN"
    attempt = run / "evidence/attempt-01"
    reproduction = run / "evidence/reproduction-01"
    files = {
        str(path.relative_to(attempt)): path.read_bytes()
        for path in attempt.rglob("*")
        if path.is_file()
    }
    assert len(files) == outcome["reproduction_file_count"] == 14
    assert files == {
        str(path.relative_to(reproduction)): path.read_bytes()
        for path in reproduction.rglob("*")
        if path.is_file()
    }
    result = json.loads(files["run-result.json"])
    assert result["status"] == "ADMITTED_REPLAYED_UNREVIEWED"
    assert result["source_review_decision_sha256"] == digest(canonical(decision))
    packet = json.loads((run / "query-review-01/manifest.json").read_bytes())
    assert packet["run_result_sha256"] == digest(files["run-result.json"])
    assert packet["run_manifest_sha256"] == decision["run_manifest_sha256"]
    for name, identity in result["artifacts"].items():
        assert digest(files[name]) == identity
    base_bytes = (run / "base-history.jsonl").read_bytes()
    assert files["ledger/history.jsonl"].startswith(base_bytes)
    base = api.KnowledgeChangeHistory.reopen(run / "base-history.jsonl").replay()
    replay = api.KnowledgeChangeHistory.reopen(
        attempt / "ledger/history.jsonl"
    ).replay()
    repair.check_preservation(
        base.graph.export_records(), replay.graph.export_records(), candidate
    )
    repair.check_record_history(base.record_history, replay.record_history, candidate)
    assert replay.receipt.canonical_bytes == files["replay-receipt.json"]
    assert (
        pilot.canonical(replay.graph.export_records()) == files["export-records.json"]
    )
    assert len(base.record_history) == 166
    assert len(replay.record_history) == 173
    assert replay.ledger_event_count == 45
    before = json.loads((run / "before-query.json").read_bytes())
    after = json.loads(files["query-result.json"])
    assert (
        changed_questions(
            json.loads((run / "questions.json").read_bytes()),
            before,
            after,
            result["changed_question_ids"],
        )
        == outcome["changed_question_ids"]
    )
    assert len(outcome["changed_question_ids"]) == 5
    repair.check_read_guard(after["forbidden_attempts"])
    assert (run / "base-history.jsonl").read_bytes() == base_bytes
    assert (attempt / "ledger/history.jsonl").read_bytes() == files[
        "ledger/history.jsonl"
    ]


def check_stage():
    from tempfile import TemporaryDirectory
    import pilot
    from reconciliation_feedback import stage
    from integration_review import prepare
    from followup import verify_materials

    previous = (
        pilot.ROOT / "private/paper-v4-answer-demonstration/sol-reconciliation-01"
    )
    before = {
        str(p): digest(p.read_bytes()) for p in previous.rglob("*") if p.is_file()
    }
    with TemporaryDirectory(
        dir=pilot.ROOT / "private", prefix="feedback-test-"
    ) as temporary:
        run = Path(temporary) / "run"
        manifest = stage(run)
        assert manifest["producer_session"] == "CONTINUATION"
        assert (
            "qualification-criteria.json"
            in (run / "integration-query-review-task.md").read_text()
        )
        assert manifest["feedback_from_run_manifest_sha256"] == digest(
            (previous / "manifest.json").read_bytes()
        )
        assert (run / "base-history.jsonl").read_bytes() == (
            previous / "base-history.jsonl"
        ).read_bytes()
        assert (run / "before-query.json").read_bytes() == (
            previous / "before-query.json"
        ).read_bytes()
        declared = json.loads(
            (run / "evidence/producer-input-manifest.json").read_bytes()
        )["declared_inputs"]
        assert {
            entry["target"]
            for entry in declared
            if entry["target"].startswith("feedback/")
        } == {
            "feedback/task.md",
            "feedback/prior-candidate.json",
            "feedback/prior-report.json",
            "feedback/source-review.md",
        }
        verify_materials(run, manifest["materials"])
        work = run / "evidence/producer/work"
        candidate = work / "candidate-01.json"
        candidate.write_bytes(
            (previous / "evidence/producer/work/candidate-01.json").read_bytes()
        )
        candidate.with_suffix(".report.json").write_bytes(
            (previous / "evidence/producer/work/candidate-01.report.json").read_bytes()
        )
        packet = prepare(run, candidate, run / "source-review-01")
        assert len(packet["materials"]) == 22
        assert not any(
            "feedback" in item["path"]
            or "prior-candidate" in item["path"]
            or "source-review.md" in item["path"]
            for item in packet["materials"]
        )
        assert not list(run.rglob("ledger"))
        with pytest.raises(ValueError, match="source-review authorization"):
            repair.execute(
                run,
                "evidence",
                candidate,
                run / "evidence/attempt-01",
                transaction_time="2026-09-08T00:00:00Z",
            )
        assert not (run / "evidence/attempt-01").exists()
    assert before == {
        str(p): digest(p.read_bytes()) for p in previous.rglob("*") if p.is_file()
    }
