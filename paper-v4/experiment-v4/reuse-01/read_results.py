"""Read both halves of reuse-01 out of their own review records.

Every figure RESULTS.md prints comes from here, and every figure here comes from
a file on disk: the two preliminary review records, the two input manifests, the
two question files and the four launch logs. Nothing is entered by hand and
nothing is judged: the labels were the reviewers', the coverage entries were the
reviewers', and this script counts them.

Four blocks come out:

``sets`` the two question sets' shapes;
``graph`` and ``baseline`` this cell's two halves, each with elements reached
per tier, question labels over the positives, witness support, absence codes and
control outcomes;
``first_set`` the same read of run-23 and baseline-01, which answered the first
question set, so the cost table has both columns;
``cost`` the token and tool-call figures the launch logs recorded.

    .venv/bin/python paper-v4/experiment-v4/reuse-01/read_results.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EVALUATION = ROOT / "paper-v4/evaluation-v4"
EXPERIMENT = ROOT / "paper-v4/experiment-v4"

SET_B = EXPERIMENT / "competency-questions-set-b.json"
SET_A_V3 = EXPERIMENT / "competency-questions-v3.json"
SET_A_V31 = EXPERIMENT / "competency-questions-v3.1.json"

JSON_BLOCK = re.compile(r"```json\n(?P<record>.*?)\n```", re.DOTALL)

CELLS = {
    "graph": {
        "package": EVALUATION / "reuse-01",
        "questions": SET_B,
        "surface": "SELECTED_READING_TEXT_LAYER",
        "launch_log": ROOT / "private/paper-v4-reuse-01/launch-log.json",
    },
    "baseline": {
        "package": EVALUATION / "reuse-01-baseline",
        "questions": SET_B,
        "surface": "IN_CONTEXT_ANSWER_SET",
        "launch_log": ROOT / "private/paper-v4-reuse-01-baseline/launch-log.json",
    },
}
FIRST_SET = {
    "run-23": {
        "package": EVALUATION / "run-23",
        "questions": SET_A_V3,
        "surface": "SELECTED_READING_TEXT_LAYER",
    },
    "baseline-01": {
        "package": EVALUATION / "baseline-01",
        "questions": SET_A_V31,
        "surface": "IN_CONTEXT_ANSWER_SET",
    },
}


def _record(path: Path) -> dict[str, Any]:
    match = JSON_BLOCK.search(path.read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"{path} carries no json record block")
    return json.loads(match.group("record"))


def _questions(path: Path) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in json.loads(path.read_bytes())["questions"]}


def read_cell(package: Path, questions_path: Path) -> dict[str, Any]:
    record = _record(package / "review-record.preliminary.md")
    questions = _questions(questions_path)

    support: dict[str, int] = {}
    for witness in record["witnesses"]:
        token = witness["source_support"]
        support[token] = support.get(token, 0) + 1

    labels: dict[str, int] = {}
    positive_labels: dict[str, int] = {}
    assembly: dict[str, int] = {}
    absences: dict[str, int] = {}
    reached = 0
    total = 0
    positive_reached = 0
    positive_total = 0
    by_tier: dict[str, dict[str, int]] = {}
    per_question: dict[str, dict[str, Any]] = {}

    for entry in record["questions"]:
        question_id = entry["question_id"]
        question = questions[question_id]
        tier = question["tier"]
        label = entry["question_responsiveness"]
        labels[label] = labels.get(label, 0) + 1
        assembly[entry["assembly"]] = assembly.get(entry["assembly"], 0) + 1
        named = sum(1 for item in entry["coverage"] if item["row_index"] is not None)
        count = len(entry["coverage"])
        if count != len(question["required_semantics"]):
            raise ValueError(f"{question_id} coverage does not cover its semantics")
        reached += named
        total += count
        bucket = by_tier.setdefault(tier, {"reached": 0, "of": 0, "questions": 0})
        bucket["reached"] += named
        bucket["of"] += count
        bucket["questions"] += 1
        if tier != "C":
            positive_reached += named
            positive_total += count
            positive_labels[label] = positive_labels.get(label, 0) + 1
        for item in entry["coverage"]:
            if item["absent_reason"] is not None:
                absences[item["absent_reason"]] = absences.get(item["absent_reason"], 0) + 1
        per_question[question_id] = {
            "tier": tier,
            "label": label,
            "reached": named,
            "of": count,
            "rows": len(entry["rows"]),
        }

    sys.path.insert(0, str(EVALUATION))
    import review  # noqa: PLC0415

    findings = review.control_outcomes(record, questions_path.read_bytes())
    manifest = json.loads((package / "review-input-manifest.json").read_bytes())
    return {
        "record": str((package / "review-record.preliminary.md").relative_to(ROOT)),
        "status": record["status"],
        "evaluator_kind": record["preliminary"]["evaluator_kind"],
        "completed_at": record["preliminary"]["completed_at"],
        "rows_total": sum(manifest["rows_per_question"].values()),
        "witnesses": manifest["witnesses_traced"],
        "witnesses_judged": len(record["witnesses"]),
        "source_support": dict(sorted(support.items())),
        "question_responsiveness_all": dict(sorted(labels.items())),
        "question_responsiveness_positive": dict(sorted(positive_labels.items())),
        "assembly": dict(sorted(assembly.items())),
        "elements_reached": reached,
        "elements_total": total,
        "elements_reached_positive": positive_reached,
        "elements_total_positive": positive_total,
        "elements_by_tier": {
            tier: by_tier[tier] for tier in sorted(by_tier)
        },
        "absences": dict(sorted(absences.items())),
        "controls": findings,
        "controls_matched": sum(1 for item in findings if item["matched"]),
        "controls_total": len(findings),
        "per_question": per_question,
    }


def read_costs() -> dict[str, Any]:
    graph_log = json.loads(CELLS["graph"]["launch_log"].read_bytes())
    baseline_log = json.loads(CELLS["baseline"]["launch_log"].read_bytes())
    run_23_usage = json.loads(
        (EXPERIMENT / "run-23/results/usage.json").read_bytes()
    )
    baseline_01_log = json.loads(
        (ROOT / "private/paper-v4-baseline-01/launch-log.json").read_bytes()
    )
    author = next(
        item for item in graph_log["launches"] if item["role"] == "QUESTION_SET_AUTHOR"
    )
    producer = next(
        item for item in baseline_log["launches"] if item["role"] == "ANSWER_PRODUCER"
    )
    baseline_01_producer = baseline_01_log["launches"][0]
    return {
        "second_question_set": {
            "shared": {
                "question_set_author_tokens": author["usage"]["author_total_tokens"],
                "question_set_author_tool_uses": author["usage"]["tool_uses"],
                "note": (
                    "One authoring session produced the set both halves answer, so"
                    " this cost is shared and is counted once, not twice."
                ),
            },
            "graph": {
                "type_set_tool_calls": graph_log["type_sets"]["cost_in_tool_calls"],
                "type_set_tokens": None,
                "type_set_note": (
                    "Authored by hand by the parent session. No token figure"
                    " carries it; the tool-call count is the honest unit."
                ),
                "binding_cases": graph_log["binding"]["cases"],
                "query_wall_clock_seconds": 100,
                "producer_tokens": 0,
                "producer_note": (
                    "No producer ran. Nothing was captured, admitted, disposed or"
                    " replayed for this question set."
                ),
                "review_tokens": graph_log["review"].get("usage", {}).get(
                    "reviewer_total_tokens"
                ),
                "review_tool_uses": graph_log["review"].get("usage", {}).get("tool_uses"),
            },
            "baseline": {
                "producer_tokens": producer["usage"]["producer_total_tokens"],
                "producer_tool_uses": producer["usage"]["tool_uses"],
                "producer_duration_ms": producer["usage"]["duration_ms"],
                "review_tokens": baseline_log["review"].get("usage", {}).get(
                    "reviewer_total_tokens"
                ),
                "review_tool_uses": baseline_log["review"].get("usage", {}).get(
                    "tool_uses"
                ),
            },
        },
        "to_exist": {
            "graph": {
                "cell": "run-23",
                "producer_tokens": run_23_usage["producer_total_tokens"],
                "producer_stages": {
                    item["stage"]: item["tokens"] for item in run_23_usage["stages"]
                },
                "review_tokens": 487927,
                "review_tokens_source": (
                    "paper-v4/paper-ledger.md E-0345, the harness figure for"
                    " run-23's one review session"
                ),
            },
            "baseline": {
                "cell": "baseline-01",
                "producer_tokens": baseline_01_producer["usage"][
                    "producer_total_tokens"
                ],
                "review_tokens": baseline_01_log["review"]["usage"][
                    "reviewer_total_tokens"
                ],
                "note": (
                    "The baseline has nothing that persists between question sets."
                    " Its first-set cost is not a build cost; it is the same cost"
                    " again, on a different set."
                ),
            },
        },
    }


def read_all() -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": "malleus.paper-v4.reuse-01-read/v1",
        "sets": {},
        "second_set": {},
        "first_set": {},
    }
    for name, path in (("A", SET_A_V31), ("B", SET_B)):
        document = json.loads(path.read_bytes())
        questions = document["questions"]
        positives = [item for item in questions if item["tier"] != "C"]
        result["sets"][name] = {
            "path": str(path.relative_to(ROOT)),
            "questions": len(questions),
            "positive_questions": len(positives),
            "elements_over_positives": sum(
                len(item["required_semantics"]) for item in positives
            ),
            "elements_over_all": sum(
                len(item["required_semantics"]) for item in questions
            ),
        }
    for name, cell in CELLS.items():
        result["second_set"][name] = read_cell(cell["package"], cell["questions"])
        result["second_set"][name]["surface"] = cell["surface"]
    for name, cell in FIRST_SET.items():
        result["first_set"][name] = read_cell(cell["package"], cell["questions"])
        result["first_set"][name]["surface"] = cell["surface"]
    result["cost"] = read_costs()
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--output", type=Path, default=None)
    arguments = parser.parse_args(argv)
    try:
        report = read_all()
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"reuse-01-read: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    text = json.dumps(report, indent=2, sort_keys=True)
    if arguments.output is not None:
        arguments.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
