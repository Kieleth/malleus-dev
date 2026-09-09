"""Verify this retained run, not future model output or scientific truth."""

import json
import subprocess
import sys


def test_reviewed_context_additions_preserve_and_reproduce():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_completed_acquisition import check_completed; check_completed()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_completed():
    import acquisition
    import input_delivery
    import pilot
    import repair
    from followup import verify_materials
    from reconciliation import authorize
    from review_packet import digest
    from snapshot_review import trace_closure

    run = pilot.ROOT / "private/paper-v4-answer-demonstration/sol-acquisition-01"
    manifest, before, old_queries = repair.preflight(run)
    assert manifest["schema"] == acquisition.SCHEMA
    assert (
        digest((run / "manifest.json").read_bytes())
        == "sha256:5060be6e6c6dc2ed6e77eff9f59cd12e6690eabfde5146b3ef0faf2455006830"
    )
    evidence = run / "evidence"
    delivery = input_delivery.verify_delivery(evidence, "initial")
    assert delivery == json.loads(
        (evidence / "input-delivery-receipt.json").read_bytes()
    )
    assert sum(delivery["frames_per_input"].values()) == 104
    candidate_path = evidence / "producer/work/candidate-01.json"
    candidate = json.loads(candidate_path.read_bytes())
    acquisition.load_check(run, before.graph.export_records(), candidate_path)
    decision = authorize(run, candidate_path)
    assert decision["ratification"] == "PENDING_HUMAN"
    assert decision["reviewer_thread_id"] != delivery["thread_id"]
    verify_materials(
        run / "source-review-01",
        json.loads((run / "source-review-01/manifest.json").read_bytes())["materials"],
    )
    attempt = evidence / "attempt-01"
    files = {
        str(p.relative_to(attempt)): p.read_bytes()
        for p in attempt.rglob("*")
        if p.is_file()
    }
    repeat = evidence / "reproduction-01"
    assert len(files) == 14
    assert files == {
        str(p.relative_to(repeat)): p.read_bytes()
        for p in repeat.rglob("*")
        if p.is_file()
    }
    result = json.loads(files["run-result.json"])
    assert result["status"] == "ADMITTED_REPLAYED_UNREVIEWED"
    for name, identity in result["artifacts"].items():
        assert digest(files[name]) == identity
    assert files["submitted-population.json"] == candidate_path.read_bytes()
    ledger = attempt / "ledger/history.jsonl"
    assert ledger.read_bytes().startswith((run / "base-history.jsonl").read_bytes())
    after = repair.api.KnowledgeChangeHistory.reopen(ledger).replay()
    repair.check_preservation(
        before.graph.export_records(), after.graph.export_records(), candidate
    )
    repair.check_record_history(before.record_history, after.record_history, candidate)
    assert len(repair.indexed(before.graph.export_records())) == 164
    assert len(repair.indexed(after.graph.export_records())) == 167
    assert len(after.record_history) == 176
    assert after.ledger_event_count == 51
    assert after.receipt.canonical_bytes == files["replay-receipt.json"]
    assert pilot.canonical(after.graph.export_records()) == files["export-records.json"]
    inputs = evidence / "producer/inputs"
    new_queries, traces, _, counters = repair.frozen_queries(
        run,
        after,
        json.loads((inputs / "population-surface.json").read_bytes()),
        reader="SubjectGraphReads",
    )
    repair.check_read_guard(counters)
    assert new_queries == json.loads(files["query-result.json"])["queries"]
    assert traces == json.loads(files["query-trace-summary.json"])["records"]
    changed = [
        new["question_id"]
        for old, new in zip(old_queries, new_queries, strict=True)
        if old != new
    ]
    assert changed == result["changed_question_ids"] == ["CQ-T1-01"]
    captures = {p.name: p.read_bytes() for p in inputs.glob("*-capture.json")}
    captures["acquisition-capture.json"] = files["retained-capture.json"]
    closure = trace_closure(
        (inputs / "selected-reading.json").read_bytes(), captures, {"records": traces}
    )
    outcome = json.loads((run / "outcome.json").read_bytes())
    expected = {
        "status": "ADMITTED_REPLAYED_SOURCE_REVIEWED",
        "ratification": decision["ratification"],
        "source_review_sha256": decision["review_sha256"],
        "producer_thread_id": delivery["thread_id"],
        "reviewer_thread_id": decision["reviewer_thread_id"],
        "candidate_sha256": decision["candidate_sha256"],
        "report_sha256": decision["report_sha256"],
        "run_manifest_sha256": decision["run_manifest_sha256"],
        "source_pdf_sha256": json.loads(
            (inputs / "selected-reading.json").read_bytes()
        )["source_sha256"],
        "reading_sha256": digest((inputs / "selected-reading.json").read_bytes()),
        "ontology_sha256": digest((inputs / "ontology.yaml").read_bytes()),
        "query_binding_sha256": digest((run / "count-method.json").read_bytes()),
        "ledger_head": result["ledger_head"],
        "ledger_file_sha256": digest(files["ledger/history.jsonl"]),
        "accepted_result_sha256": digest(files["run-result.json"]),
        "replay_receipt_sha256": result["artifacts"]["replay-receipt.json"],
        "export_records_sha256": result["artifacts"]["export-records.json"],
        "query_result_sha256": result["artifacts"]["query-result.json"],
        "changed_question_ids": changed,
        "unchanged_questions": len(new_queries) - len(changed),
        "old_records_preserved": len(repair.indexed(before.graph.export_records())),
        "current_records": len(repair.indexed(after.graph.export_records())),
        "added_relations": len(candidate["records"]["relations"]),
        "historical_record_versions": len(after.record_history),
        "ledger_events": after.ledger_event_count,
        "reproduction_file_count": len(files),
        "query_rows": sum(len(q["rows"]) for q in new_queries),
        "query_paths": sum(len(q["paths"]) for q in new_queries),
        "traced_records": len(traces),
        "resolved_derivations": sum(
            len(row["resolved_derivations"]) for row in closure["records"]
        ),
        "coverage_assessment": "NO_NEW_QUESTION_GRADES_OR_AGGREGATE_TOTAL",
    }
    assert {key: outcome[key] for key in expected} == expected
    print(
        json.dumps(
            {
                "changed_questions": changed,
                "query_rows": sum(len(q["rows"]) for q in new_queries),
                "query_paths": sum(len(q["paths"]) for q in new_queries),
                "traced_records": len(traces),
                "resolved_derivations": sum(
                    len(row["resolved_derivations"]) for row in closure["records"]
                ),
                "run_result_sha256": digest(files["run-result.json"]),
                "ledger_file_sha256": digest(files["ledger/history.jsonl"]),
            }
        )
    )
