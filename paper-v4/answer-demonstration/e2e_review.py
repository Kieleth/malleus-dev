"""Reuse the complete review instrument for a fresh end-to-end result."""

import argparse
import json
from pathlib import Path

from followup import verify_materials
from freeze_review import freeze_sources
from review_packet import (
    HERE,
    ROOT,
    canonical,
    checked_result,
    docket,
    new_private_directory,
    verify_trace_materials,
    vocabulary_sources,
)


def prepare(run, attempt, output):
    target = new_private_directory(output, ROOT / "private")
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    result = json.loads((attempt / "run-result.json").read_bytes())
    if (
        result["status"] != "ADMITTED_AND_REPLAYED"
        or result["run_id"] != manifest["run_id"]
    ):
        raise ValueError("review requires this run's admitted end-to-end result")
    for key in (
        "core_commit",
        "ontology_sha256",
        "reading_sha256",
        "query_binding_sha256",
    ):
        if result[key] != manifest[key]:
            raise ValueError(f"result differs from frozen acceptance: {key}")
    paths = {
        "selected-reading.json": run / "producer/inputs/selected-reading.json",
        "retained-capture.json": attempt / "ledger/retained-capture.json",
        "competency-questions.json": run / "competency-questions.json",
        "query-result.json": attempt / "query-result.json",
        "query-trace-summary.json": attempt / "query-trace-summary.json",
        "population-trace.json": attempt / "public/trace-summary.json",
        "population-surface.json": run / "producer/accepted/population-surface.json",
        "answers.py": run / "frozen-code/answers.py",
        "binding.py": run / "frozen-code/binding.py",
        "e2e_execute.py": attempt / "e2e_execute.py",
        "query-binding.acceptance.json": run / "query-binding.acceptance.json",
        "review-protocol-v3.json": ROOT
        / "paper-v4/evaluation-v4/review-protocol-v3.json",
        "review.py": ROOT / "paper-v4/evaluation-v4/review.py",
        "review-extension.md": HERE / "REVIEW-EXTENSION.md",
    }
    sources = {name: path.read_bytes() for name, path in paths.items()}
    query = checked_result(
        sources["query-result.json"], result["query_result_sha256"], manifest["run_id"]
    )
    for key in ("ledger_head", "replay_receipt_sha256"):
        if query["inputs"][key] != result[key]:
            raise ValueError(f"query replay identity differs: {key}")
    trace = json.loads(sources["query-trace-summary.json"])
    verify_trace_materials(
        sources["selected-reading.json"], sources["retained-capture.json"], trace
    )
    sources["review-docket.json"] = canonical(
        docket(json.loads(sources["competency-questions.json"]), query, trace)
    )
    sources.update(
        vocabulary_sources(
            manifest["source_closure_sha256"],
            [run / manifest["ontology_path"]]
            + list((run / "producer/inputs").glob("*.yaml")),
            manifest["ontology_sha256"],
        )
    )
    prepared = {
        "accepted_ontology_sha256": manifest["ontology_sha256"],
        "ledger_head": result["ledger_head"],
        "replay_receipt_sha256": result["replay_receipt_sha256"],
        "rows_per_question": {
            q["question_id"]: len(q["rows"]) for q in query["queries"]
        },
    }
    return freeze_sources(sources, prepared, target, manifest["run_id"] + "-review")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--attempt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(canonical(prepare(args.run, args.attempt, args.output)).decode())
