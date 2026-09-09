"""Fixed, read-only reference cases for the approved fresh capture comparison."""

import argparse
import json
from pathlib import Path

import malleus.compiler as api

from fresh_comparison import METHOD, METHOD_IDENTITY
from followup import checked_bytes, verify_materials
import pilot
from query_capacity import audit
from repair import frozen_queries, check_read_guard
from review_packet import canonical, digest, docket, new_private_directory

PRIVATE = pilot.ROOT / "private/paper-v4-answer-demonstration"
CORE = "160878cf14c0d27b11a440e26688708e9b7a7e2b"
CASES = {
    "earlier-fresh": (
        PRIVATE / "sol-e2e-corrected-01/attempt-01",
        PRIVATE / "sol-e2e-corrected-01/producer/accepted/population-surface.json",
        "sha256:f0823fcc85954d168eed7e401bb11cc9da61a5f0ccbabe146af869a156180363",
        "sha256:2b7e0beb4c505861d6bb4b203cbd52a515473dfcfd7f8628981e682c1e0cc243",
    ),
    "fixed-ontology": (
        PRIVATE / "sol-calibration-01/b/attempt-01",
        PRIVATE / "sol-calibration-01/b/producer/inputs/population-surface.json",
        "sha256:97be782288a78c78ee5150feafb562a84ac31d9fcd1105e73736081edc35f29f",
        "sha256:6406acaed78b371dfeea48224d587b619d7c9743832b113e9231171f49b9c6c8",
    ),
    "repaired": (
        PRIVATE / "sol-acquisition-01/evidence/attempt-01",
        PRIVATE / "sol-acquisition-01/evidence/producer/inputs/population-surface.json",
        "sha256:0b3513d1010f5270a45e3f0ada051810c6e430ab9e5a6eea0c1ecd5e383b279d",
        "sha256:6406acaed78b371dfeea48224d587b619d7c9743832b113e9231171f49b9c6c8",
    ),
}


def execute(case, output):
    if case not in CASES:
        raise ValueError("reference case was not selected")
    target = new_private_directory(output, PRIVATE)
    attempt, surface_path, result_id, surface_id = CASES[case]
    result = json.loads(
        checked_bytes(
            (attempt / "run-result.json").read_bytes(), result_id, "reference result"
        )
    )
    method = json.loads(
        checked_bytes(
            (METHOD / "method.json").read_bytes(), METHOD_IDENTITY, "common reader"
        )
    )
    verify_materials(METHOD, method["materials"])
    pilot.verify_runtime(CORE)
    if case == "repaired":
        receipt_id = result["artifacts"]["replay-receipt.json"]
        graph_id = result["artifacts"]["export-records.json"]
    else:
        receipt_id, graph_id = (
            result["replay_receipt_sha256"],
            result["export_records_sha256"],
        )
    surface_source = checked_bytes(
        surface_path.read_bytes(), surface_id, "reference surface"
    )
    surface = json.loads(surface_source)
    ledger = attempt / "ledger/history.jsonl"
    before = ledger.read_bytes()
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    checked_bytes(replay.receipt.canonical_bytes, receipt_id, "reference receipt")
    graph = pilot.canonical(replay.graph.export_records())
    checked_bytes(graph, graph_id, "reference graph")
    capacity = audit(
        surface,
        (METHOD / "answers.py").read_bytes(),
        (METHOD / "questions.json").read_bytes(),
    )
    queries, traces, guard_id, counters = frozen_queries(
        METHOD, replay, surface, reader="SubjectGraphReads"
    )
    check_read_guard(counters)
    if (
        ledger.read_bytes() != before
        or pilot.canonical(replay.graph.export_records()) != graph
    ):
        raise ValueError("reference read changed history or graph")
    query = {
        "schema": "malleus.paper-v4.comparison-reference/v1",
        "reference_case": case,
        "status": "UNREVIEWED",
        "core_commit": CORE,
        "inputs": {
            "reference_result_sha256": result_id,
            "query_method_sha256": METHOD_IDENTITY,
            "population_surface_sha256": digest(surface_source),
            "ledger_head": replay.ledger_head,
            "replay_receipt_sha256": receipt_id,
            "read_guard_sha256": guard_id,
        },
        "queries": queries,
    }
    trace = {"records": traces}
    files = {
        "query-result.json": canonical(query),
        "query-trace-summary.json": canonical(trace),
        "query-capacity.json": canonical(capacity),
        "review-docket.json": canonical(
            docket(json.loads((METHOD / "questions.json").read_bytes()), query, trace)
        ),
        "comparison_reads.py": Path(__file__).read_bytes(),
    }
    summary = {
        "reference_case": case,
        "reference_result_sha256": result_id,
        "query_result_sha256": digest(files["query-result.json"]),
        "query_method_sha256": METHOD_IDENTITY,
        "ledger_bytes_unchanged": True,
        "question_count": len(queries),
        "rows": sum(len(q["rows"]) for q in queries),
        "paths": sum(len(q["paths"]) for q in queries),
        "traced_records": len(traces),
        "declaration_gap_questions": [
            q["question_id"] for q in capacity["questions"] if q["missing_declarations"]
        ],
        "coverage": "NOT_ASSESSED",
    }
    files["summary.json"] = canonical(summary)
    target.mkdir(parents=True)
    for name, data in files.items():
        (target / name).write_bytes(data)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=tuple(CASES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(execute(args.case, args.output)))
