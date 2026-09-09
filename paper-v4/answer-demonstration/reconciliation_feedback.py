"""Freeze one disclosed feedback continuation. Reuse reconciliation and admission."""

import argparse
import json
from pathlib import Path

import pilot
import repair
from followup import checked_bytes
from review_packet import canonical, digest, new_private_directory

HERE = Path(__file__).resolve().parent
PREVIOUS = pilot.ROOT / "private/paper-v4-answer-demonstration/sol-reconciliation-01"


def stage(run):
    run = new_private_directory(run, pilot.ROOT / "private")
    checked_bytes(
        (PREVIOUS / "manifest.json").read_bytes(),
        "sha256:bc285796a9033e8283726387846ece537bc789bea9377d09ac64ef515a915d95",
        "original reconciliation manifest",
    )
    previous, _, _ = repair.preflight(PREVIOUS)
    outcome_bytes = checked_bytes(
        (PREVIOUS / "outcome.json").read_bytes(),
        "sha256:82c84a3bd3f8c0be568d5730f578901f5f1f4e92fa66b649d92dca42c1c07e9a",
        "original withheld outcome",
    )
    outcome = json.loads(outcome_bytes)
    files = {
        item["path"]: (PREVIOUS / item["path"]).read_bytes()
        for item in previous["materials"]
    }
    work = PREVIOUS / "evidence/producer/work"
    for name, path, key in (
        ("prior-candidate.json", work / "candidate-01.json", "candidate_sha256"),
        ("prior-report.json", work / "candidate-01.report.json", "report_sha256"),
        (
            "source-review.md",
            PREVIOUS / outcome["source_review"],
            "source_review_sha256",
        ),
    ):
        files["evidence/producer/feedback/" + name] = checked_bytes(
            path.read_bytes(), outcome[key], name
        )
    task = (
        (HERE / "reconciliation-feedback-task.md")
        .read_text()
        .replace("{RUN}", str(run))
        .encode()
    )
    files["evidence/TASK.md"] = task
    files["evidence/producer/feedback/task.md"] = task
    files["plan.md"] = (HERE / "RECONCILIATION-FEEDBACK-PLAN.md").read_bytes()
    files["repair.py"] = (HERE / "repair.py").read_bytes()
    files["reconciliation_feedback.py"] = Path(__file__).read_bytes()
    files["integration-query-review-task.md"] = (
        b"For CQ-T5-01, use qualification-criteria.json for BOTH states. These are "
        b"the existing accepted-baseline criteria, not new requirements. For the "
        b"other questions, use their unchanged required_semantics.\n\n"
        + (HERE / "integration-query-review-task.md").read_bytes()
    )
    files["qualification-criteria.json"] = (
        HERE / "qualification-criteria.json"
    ).read_bytes()
    files["evidence/producer-input-manifest.json"] = canonical(
        {
            "declared_inputs": [
                {
                    "target": name.removeprefix("evidence/producer/"),
                    "sha256": digest(data),
                }
                for name, data in sorted(files.items())
                if name.startswith("evidence/producer/")
            ]
        }
    )
    manifest = {
        **{
            key: previous[key]
            for key in (
                "schema",
                "core_commit",
                "core_tree",
                "producer_model",
                "producer_effort",
                "maximum_structural_returns",
                "query_reader",
                "base_run",
                "base_receipt_sha256",
            )
        },
        "condition": "SOURCE_REVIEW_FEEDBACK_RECONCILIATION",
        "amendment_id": "reconciliation-feedback-01",
        "decision": "E-0292",
        "status": "FROZEN_BEFORE_DISPATCH",
        "producer_session": "CONTINUATION",
        "feedback_from_run_manifest_sha256": digest(
            (PREVIOUS / "manifest.json").read_bytes()
        ),
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    for name, data in files.items():
        path = run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (run / "evidence/producer/work").mkdir()
    (run / "manifest.json").write_bytes(canonical(manifest))
    repair.preflight(run)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", type=Path, required=True)
    args = parser.parse_args()
    print(canonical(stage(args.stage)).decode())
