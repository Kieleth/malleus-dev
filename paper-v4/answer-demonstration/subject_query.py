"""Requery the frozen Sol graph. No capture, population or history writes."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

import malleus.compiler as api

from answers import GraphReads, answer
from followup import HERE, ROOT, QUERY_IDENTITY, checked_bytes, verify_materials
from freeze_review import freeze_sources
import pilot
from review_packet import (
    canonical,
    digest,
    docket,
    new_private_directory,
    verify_trace_materials,
    vocabulary_sources,
)
from subject_answers import SubjectGraphReads


def execute(run, output):
    target = new_private_directory(output, ROOT / "private")
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    pilot.verify_runtime(manifest["core_commit"])
    attempt = run / "attempt-01"
    expected = json.loads((attempt / "run-result.json").read_bytes())
    old = json.loads(
        checked_bytes(
            (attempt / "query-result.json").read_bytes(),
            expected["query_result_sha256"],
            "original query",
        )
    )
    if expected["status"] != "ADMITTED_AND_REPLAYED":
        raise ValueError("this query experiment requires the frozen admitted capture")
    code = {
        name: (HERE / name).read_bytes()
        for name in (
            "answers.py",
            "subject_answers.py",
            "subject_query.py",
            "binding.py",
        )
    }
    checked_bytes(code["answers.py"], QUERY_IDENTITY, "base query program")
    surface_bytes = (run / "producer/inputs/population-surface.json").read_bytes()
    questions_bytes = (run / "competency-questions.json").read_bytes()
    questions = pilot.load_questions(questions_bytes)
    ledger = attempt / "ledger/history.jsonl"
    ledger_digest = digest(ledger.read_bytes())
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    checked_bytes(
        replay.receipt.canonical_bytes,
        expected["replay_receipt_sha256"],
        "replay receipt",
    )
    checked_bytes(
        pilot.canonical(replay.graph.export_records()),
        expected["export_records_sha256"],
        "graph export",
    )
    native, guard_identity = pilot.load_native()
    graph_digest = replay.graph.state_digest()
    reads = SubjectGraphReads(replay.graph, json.loads(surface_bytes))
    baseline_reads = GraphReads(replay.graph, json.loads(surface_bytes))
    target.mkdir(parents=True)
    method = {
        "mode": "RETROSPECTIVE_QUERY_ONLY",
        "run_id": manifest["run_id"],
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "core_commit": manifest["core_commit"],
        "original_query_result_sha256": expected["query_result_sha256"],
        "code": {name: digest(source) for name, source in code.items()},
    }
    for name, source in code.items():
        (target / name).write_bytes(source)
    (target / "method.json").write_bytes(canonical(method))
    guard = native._SourceFreeGuard()
    with guard:
        baseline = [answer(baseline_reads, q["id"]) for q in questions]
        if baseline != old["queries"]:
            raise ValueError("original query outputs no longer reproduce")
        queries = [answer(reads, q["id"]) for q in questions]
        witnesses = sorted({rid for q in queries for rid in q["witness_ids"]})
        traces = native.trace_witnesses(replay, witnesses)
    if (
        digest(ledger.read_bytes()) != ledger_digest
        or replay.graph.state_digest() != graph_digest
    ):
        raise ValueError("query changed graph or ledger")
    result = {
        "schema": "malleus.paper-v4.subject-query/v1",
        "status": "EXPLORATORY_UNREVIEWED",
        "run_id": manifest["run_id"],
        "core_commit": manifest["core_commit"],
        "historical_replay_matches": True,
        "ledger_bytes_unchanged": True,
        "graph_state_digest": graph_digest,
        "forbidden_attempts": guard.attempts,
        "inputs": {
            "query_program_sha256": digest(code["subject_answers.py"]),
            "base_query_program_sha256": digest(code["answers.py"]),
            "runner_sha256": digest(code["subject_query.py"]),
            "binding_program_sha256": digest(code["binding.py"]),
            "population_surface_sha256": digest(surface_bytes),
            "question_set_sha256": digest(questions_bytes),
            "read_guard_sha256": guard_identity,
            "ledger_head": replay.ledger_head,
            "replay_receipt_sha256": expected["replay_receipt_sha256"],
        },
        "queries": queries,
    }
    changed = [
        q["question_id"]
        for before, q in zip(baseline, queries, strict=True)
        if before != q
    ]
    (target / "query-result.json").write_bytes(canonical(result))
    (target / "query-trace-summary.json").write_bytes(canonical({"records": traces}))
    summary = {
        "changed_questions": changed,
        "rows_before": sum(len(q["rows"]) for q in baseline),
        "rows_after": sum(len(q["rows"]) for q in queries),
        "queries_with_rows_before": sum(bool(q["rows"]) for q in baseline),
        "queries_with_rows_after": sum(bool(q["rows"]) for q in queries),
        "all_paths_unchanged": all(
            a["paths"] == b["paths"] for a, b in zip(baseline, queries, strict=True)
        ),
        "query_result_sha256": digest(canonical(result)),
        "ledger_bytes_unchanged": True,
        "original_queries_reproduced": True,
    }
    (target / "summary.json").write_bytes(canonical(summary))
    return summary


def review_packet(run, query, output):
    target = new_private_directory(output, ROOT / "private")
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    attempt, inputs = run / "attempt-01", run / "producer/inputs"
    expected = json.loads((attempt / "run-result.json").read_bytes())
    method = json.loads((query / "method.json").read_bytes())
    summary = json.loads((query / "summary.json").read_bytes())
    result_source = checked_bytes(
        (query / "query-result.json").read_bytes(),
        summary["query_result_sha256"],
        "subject query",
    )
    result = json.loads(result_source)
    for key in ("ledger_head", "replay_receipt_sha256"):
        if result["inputs"][key] != expected[key]:
            raise ValueError(f"query replay binding differs: {key}")
    paths = {
        "selected-reading.json": inputs / "selected-reading.json",
        "retained-capture.json": attempt / "retained-capture.json",
        "population-trace.json": attempt / "trace-summary.json",
        "population-surface.json": inputs / "population-surface.json",
        "competency-questions.json": run / "competency-questions.json",
        "query-trace-summary.json": query / "query-trace-summary.json",
        "review.py": ROOT / "paper-v4/evaluation-v4/review.py",
        "review-protocol-v3.json": ROOT
        / "paper-v4/evaluation-v4/review-protocol-v3.json",
    }
    sources = {name: path.read_bytes() for name, path in paths.items()}
    sources["query-result.json"] = result_source
    for name, identity in method["code"].items():
        sources[name] = checked_bytes((query / name).read_bytes(), identity, name)
    trace = json.loads(sources["query-trace-summary.json"])
    verify_trace_materials(
        sources["selected-reading.json"], sources["retained-capture.json"], trace
    )
    index = docket(json.loads(sources["competency-questions.json"]), result, trace)
    sources["review-docket.json"] = canonical(index)
    sources.update(
        vocabulary_sources(
            manifest["source_closure_sha256"],
            list(inputs.glob("*.yaml")),
            manifest["ontology_sha256"],
        )
    )
    prepared = {
        "accepted_ontology_sha256": manifest["ontology_sha256"],
        "ledger_head": expected["ledger_head"],
        "replay_receipt_sha256": expected["replay_receipt_sha256"],
        "rows_per_question": {
            q["question_id"]: len(q["rows"]) for q in result["queries"]
        },
    }
    return freeze_sources(
        sources, prepared, target, manifest["run_id"] + "-subject-query-review"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    args = parser.parse_args()
    print(canonical(execute(args.run, args.output)).decode())
    print(canonical(review_packet(args.run, args.output, args.review)).decode())
