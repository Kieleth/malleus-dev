"""Prepare the existing source-grounded review for one fresh capture result."""

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
    digest,
    docket,
    new_private_directory,
    verify_trace_materials,
    vocabulary_sources,
)


def prepare(run, attempt, output, *, result_identity):
    target = new_private_directory(output, ROOT / "private")
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    result = checked_result(
        (attempt / "run-result.json").read_bytes(), result_identity, manifest["run_id"]
    )
    if result["status"] not in {"ADMITTED_AND_REPLAYED", "NO_DOMAIN_CHANGE"}:
        raise ValueError("a refused capture has no query review packet")
    for key in (
        "core_commit",
        "reading_sha256",
        "ontology_sha256",
        "query_binding_sha256",
    ):
        if result[key] != manifest[key]:
            raise ValueError(f"fresh run binding differs: {key}")
    inputs = run / "producer/inputs"
    paths = {
        "selected-reading.json": inputs / "selected-reading.json",
        "retained-capture.json": attempt / "retained-capture.json",
        "competency-questions.json": run / "competency-questions.json",
        "query-result.json": attempt / "query-result.json",
        "query-trace-summary.json": attempt / "query-trace-summary.json",
        "population-trace.json": attempt / "trace-summary.json",
        "population-surface.json": inputs / "population-surface.json",
        "answers.py": run / "frozen-code/answers.py",
        "capture.py": run / "frozen-code/capture.py",
        "binding.py": run / "frozen-code/binding.py",
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
            raise ValueError(f"fresh replay binding differs: {key}")
    for name, key in (
        ("answers.py", "query_program_sha256"),
        ("capture.py", "runner_sha256"),
        ("binding.py", "binding_program_sha256"),
        ("population-surface.json", "population_surface_sha256"),
        ("competency-questions.json", "question_set_sha256"),
        ("query-binding.acceptance.json", "query_binding_sha256"),
    ):
        if digest(sources[name]) != query["inputs"][key]:
            raise ValueError(f"fresh query input differs: {name}")
    trace = json.loads(sources["query-trace-summary.json"])
    verify_trace_materials(
        sources["selected-reading.json"], sources["retained-capture.json"], trace
    )
    index = docket(json.loads(sources["competency-questions.json"]), query, trace)
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
        "ledger_head": result["ledger_head"],
        "replay_receipt_sha256": result["replay_receipt_sha256"],
        "rows_per_question": {
            q["question_id"]: len(q["rows"]) for q in query["queries"]
        },
    }
    return freeze_sources(sources, prepared, target, manifest["run_id"] + "-review")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--attempt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--result-identity", required=True)
    args = parser.parse_args()
    print(
        canonical(
            prepare(
                args.run,
                args.attempt,
                args.output,
                result_identity=args.result_identity,
            )
        ).decode()
    )
