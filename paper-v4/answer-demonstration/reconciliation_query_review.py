"""Package fixed before/after query evidence; assign no semantic verdicts."""

import argparse
import json
from pathlib import Path

import pilot
import repair
from followup import checked_bytes
from reconciliation import require
from review_packet import canonical, digest, docket, new_private_directory


def changed_questions(questions, before, after, declared):
    ids = [item["id"] for item in questions["questions"]]
    require(len(set(ids)) == len(ids), "duplicate question identity")
    require(
        ids
        == [q["question_id"] for q in before["queries"]]
        == [q["question_id"] for q in after["queries"]],
        "before/after question closure or order differs",
    )
    changed = [
        a["question_id"]
        for b, a in zip(before["queries"], after["queries"], strict=True)
        if b != a
    ]
    require(
        changed == declared == after["changed_question_ids"],
        "declared changed questions differ from actual output",
    )
    return changed


def prepare(run, attempt, output):
    target = new_private_directory(output, pilot.ROOT / "private")
    manifest, baseline, before_queries = repair.preflight(run)
    require(
        manifest["condition"] == "SOURCE_REVIEW_FEEDBACK_RECONCILIATION",
        "exact feedback condition required",
    )
    result_bytes = (attempt / "run-result.json").read_bytes()
    result = json.loads(result_bytes)
    require(
        result["status"] == "ADMITTED_REPLAYED_UNREVIEWED",
        "accepted execution required before query review",
    )
    for name, identity in result["artifacts"].items():
        checked_bytes((attempt / name).read_bytes(), identity, name)
    decision = json.loads((run / "source-review-01/decision.json").read_bytes())
    require(
        decision["status"] == "ALLOW_SUPPORTED_BATCH",
        "supported source-review decision required",
    )
    checked_bytes(
        canonical(decision),
        result["source_review_decision_sha256"],
        "admitted source-review decision",
    )
    checked_bytes(
        (attempt / "submitted-population.json").read_bytes(),
        decision["candidate_sha256"],
        "reviewed candidate",
    )
    checked_bytes(
        (attempt / "submitted-report.json").read_bytes(),
        decision["report_sha256"],
        "reviewed report",
    )
    inputs = run / "evidence/producer/inputs"
    native, _ = pilot.load_native()
    before_trace = {
        "records": native.trace_witnesses(
            baseline,
            sorted({key for query in before_queries for key in query["witness_ids"]}),
        )
    }
    before = json.loads((run / "before-query.json").read_bytes())
    after = json.loads((attempt / "query-result.json").read_bytes())
    repair.check_read_guard(after["forbidden_attempts"])
    require(
        after["query_program_sha256"] == digest((run / "answers.py").read_bytes()),
        "query program differs",
    )
    questions = json.loads((run / "questions.json").read_bytes())
    changed = changed_questions(
        questions, before, after, result["changed_question_ids"]
    )
    after_trace = json.loads((attempt / "query-trace-summary.json").read_bytes())
    sources = {
        "TASK.md": (run / "integration-query-review-task.md").read_bytes(),
        "questions.json": (run / "questions.json").read_bytes(),
        "qualification-criteria.json": (
            run / "qualification-criteria.json"
        ).read_bytes(),
        "before-query.json": (run / "before-query.json").read_bytes(),
        "before-query-trace-summary.json": canonical(before_trace),
        "before-docket.json": canonical(docket(questions, before, before_trace)),
        "after-docket.json": canonical(docket(questions, after, after_trace)),
        "packet-builder.py": Path(__file__).read_bytes(),
    }
    sources.update(
        {
            "evidence/" + path.name: path.read_bytes()
            for path in inputs.iterdir()
            if path.is_file()
        }
    )
    for name in (
        "query-result.json",
        "query-trace-summary.json",
        "export-records.json",
        "retained-capture.json",
        "population-plan.json",
        "delta-trace.json",
        "run-result.json",
    ):
        sources["evidence/after-" + name] = (attempt / name).read_bytes()
    packet = {
        "schema": "malleus.paper-v4.reconciliation-query-review/v1",
        "status": "FROZEN_BEFORE_MODEL_ASSISTED_REVIEW",
        "ratification": "PENDING",
        "run_manifest_sha256": digest((run / "manifest.json").read_bytes()),
        "run_result_sha256": digest(result_bytes),
        "changed_question_ids": changed,
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(sources.items())
        ],
    }
    target.mkdir(parents=True)
    for name, data in sources.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (target / "manifest.json").write_bytes(canonical(packet))
    return packet


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--attempt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(canonical(prepare(args.run, args.attempt, args.output)).decode())
