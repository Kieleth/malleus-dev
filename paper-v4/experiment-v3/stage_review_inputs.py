"""Freeze one run's source-grounded review inputs from the v2 review method.

The v2 protocol, task and blank record are reused; only the preliminary reviewer
kind (a Claude session instead of a Codex session) and the run's stage identities
change. Written after the run's query result exists, exactly as v2 did.

Usage: stage_review_inputs.py --run-dir <run dir>
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from research.ontology_driven_kg_realization.experiments.document_paper.human_review import (  # noqa: E402
    validate_blank_human_review,
    validate_blank_review_input_manifest,
)

V2 = ROOT / "paper-v4/evaluation-v2"
REVIEWER_KIND = "CLAUDE_PRELIMINARY"


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _write_new(path: Path, source: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(source)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    args = parser.parse_args()
    run = args.run_dir.resolve()
    out = run / "evaluation"
    manifest = json.loads((run / "run-manifest.json").read_bytes())
    result = json.loads((run / "results/experiment-result.json").read_bytes())

    protocol = json.loads((V2 / "review-protocol.json").read_bytes())
    protocol["authorship"]["preliminary_evaluator_kind"] = REVIEWER_KIND
    protocol_bytes = (json.dumps(protocol, indent=2) + "\n").encode("utf-8")
    protocol_sha = _digest(protocol_bytes)
    _write_new(out / "review-protocol.json", protocol_bytes)

    task = (V2 / "review-task.md").read_text(encoding="utf-8")
    task = task.replace(
        "Codex performs the preliminary inspection first and records its kind as `CODEX_PRELIMINARY`.",
        f"A fresh Claude session performs the preliminary inspection first and records its kind as `{REVIEWER_KIND}`.",
    ).replace("Ask Codex to run that check", "Ask the overseer session to run that check")
    _write_new(out / "review-task.md", task.encode("utf-8"))

    blank = (V2 / "review-record.blank.md").read_text(encoding="utf-8")
    blank = blank.replace("CODEX_PRELIMINARY", REVIEWER_KIND).replace(
        json.loads((V2 / "review-input-manifest.json").read_bytes())["review_protocol_sha256"],
        protocol_sha,
    )
    _write_new(out / "review-record.blank.md", blank.encode("utf-8"))

    blank_manifest = json.loads((V2 / "review-input-manifest.blank.json").read_bytes())
    blank_manifest["review_protocol_sha256"] = protocol_sha
    blank_manifest_bytes = (json.dumps(blank_manifest, indent=2) + "\n").encode("utf-8")
    _write_new(out / "review-input-manifest.blank.json", blank_manifest_bytes)

    frozen = dict(blank_manifest)
    frozen["status"] = "FROZEN_FOR_REVIEW"
    frozen["stage_identities"] = {
        "selected_ontology_sha256": manifest["sha256"]["ontology"],
        "ledger_head": result["ledger_head"],
        "replay_receipt_sha256": result["replay_receipt_sha256"],
        "query_binding_sha256": manifest["sha256"]["binding"],
        "query_result_sha256": _digest((run / "results/query-result.json").read_bytes()),
    }
    frozen_bytes = (json.dumps(frozen, indent=2) + "\n").encode("utf-8")
    _write_new(out / "review-input-manifest.json", frozen_bytes)

    guide = (V2 / "ratification-guide.md").read_text(encoding="utf-8")
    rel = run.relative_to(ROOT)
    guide = (
        guide.replace("paper-v4/experiment/competency-questions.json", f"{rel}/population-run/inputs/competency-questions.json")
        .replace("paper-v4/experiment-v2/results/query-result.json", f"{rel}/results/query-result.json")
        .replace("paper-v4/experiment-v2/native-query-binding.json", f"{rel}/native-query-binding.json")
        .replace("paper-v4/evaluation-v2/", f"{rel}/evaluation/")
        .replace("Ask Codex to run that check", "Ask the overseer session to run that check")
    )
    _write_new(out / "ratification-guide.md", guide.encode("utf-8"))

    validate_blank_review_input_manifest(blank_manifest_bytes, protocol_bytes)
    validate_blank_human_review(blank.encode("utf-8"), protocol_bytes)
    print("review protocol", protocol_sha)
    for key, value in frozen["stage_identities"].items():
        print(f"{key:26} {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
