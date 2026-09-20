"""Derive CQ-C-03's label under competency questions v3.1 for the two v3 cells.

Run-22 and run-23 were reviewed under ``competency-questions-v3.json``, whose
CQ-C-03 requires four semantics. Both reviews covered ``compilation_source``
from a row and read PARTIAL against the control's expected NONE (E-0342,
E-0345), because the sentence naming the compilation is in the selected reading
while the per-site depths and rates are not. ``competency-questions-v3.1.json``
(E-0346) drops ``compilation_source`` from CQ-C-03's required semantics and
leaves everything else in the question unmoved.

Neither cell is re-reviewed here and nothing is rewritten. The two preliminary
records already say, per semantic, whether a row names it; that is the whole
input this rule needs, so the v3.1 label is derived from what the reviewers
wrote rather than asked of them again:

* COVERED when every remaining semantic names a row,
* NONE when none of them does,
* PARTIAL otherwise.

The script refuses rather than guesses. It refuses if v3.1 drops anything other
than ``compilation_source``, if a record's coverage does not carry each of v3's
four semantics exactly once, or if the label the rule recomputes for v3
disagrees with the responsiveness the reviewer recorded, since in that case the
rule is not the one the reviews were read under and the derivation would not be
comparable.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

QUESTION_ID = "CQ-C-03"
QUESTIONS_V3 = ROOT / "paper-v4/experiment-v4/competency-questions-v3.json"
QUESTIONS_V31 = ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json"
RUNS = ("run-22", "run-23")
OUTPUT = HERE / "derived-cq-c-03-v3.1.json"

SCHEMA = "malleus.paper-v4.derived-cq-c-03-v3-1/v1"
JSON_BLOCK = re.compile(r"```json\n(?P<record>.*?)\n```", re.DOTALL)


class DerivationRefusal(ValueError):
    """The label cannot be derived from what the records carry."""


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _question(path: Path) -> dict:
    document = json.loads(path.read_bytes())
    for question in document["questions"]:
        if question["id"] == QUESTION_ID:
            return question
    raise DerivationRefusal(f"{path.name} carries no {QUESTION_ID}")


def _record(path: Path) -> dict:
    if not path.is_file():
        raise DerivationRefusal(f"preliminary record is not on disk: {path}")
    blocks = JSON_BLOCK.findall(path.read_text(encoding="utf-8"))
    if len(blocks) != 1:
        raise DerivationRefusal(f"{path} must carry exactly one fenced JSON block")
    return json.loads(blocks[0])


def label(coverage: list[dict], semantics: list[str]) -> str:
    """COVERED, NONE or PARTIAL over the semantics that name a row."""

    named = sum(
        1
        for item in coverage
        if item["semantic"] in semantics and item.get("row_index") is not None
    )
    if named == len(semantics):
        return "COVERED"
    if named == 0:
        return "NONE"
    return "PARTIAL"


def build() -> dict:
    v3 = _question(QUESTIONS_V3)
    v31 = _question(QUESTIONS_V31)
    semantics_v3 = list(v3["required_semantics"])
    semantics_v31 = list(v31["required_semantics"])
    dropped = [item for item in semantics_v3 if item not in semantics_v31]
    added = [item for item in semantics_v31 if item not in semantics_v3]
    if dropped != ["compilation_source"] or added:
        raise DerivationRefusal(
            f"v3.1 moves {added or 'nothing'} in and {dropped or 'nothing'} out of"
            f" {QUESTION_ID}; this rule was written for compilation_source alone"
        )

    cells = []
    for run_id in RUNS:
        path = ROOT / f"paper-v4/evaluation-v4/{run_id}/review-record.preliminary.md"
        record = _record(path)
        entries = [
            question
            for question in record["questions"]
            if question["question_id"] == QUESTION_ID
        ]
        if len(entries) != 1:
            raise DerivationRefusal(f"{run_id} does not answer {QUESTION_ID} once")
        coverage = entries[0]["coverage"]
        seen = [item["semantic"] for item in coverage]
        if sorted(seen) != sorted(semantics_v3):
            raise DerivationRefusal(
                f"{run_id}'s coverage carries {sorted(seen)}, not v3's"
                f" {sorted(semantics_v3)}"
            )
        recorded = entries[0]["question_responsiveness"]
        recomputed_v3 = label(coverage, semantics_v3)
        if recomputed_v3 != recorded:
            raise DerivationRefusal(
                f"{run_id}'s recorded responsiveness is {recorded} and this rule"
                f" reads {recomputed_v3} over v3's semantics"
            )
        cells.append(
            {
                "run_id": run_id,
                "review_record_path": str(path.relative_to(ROOT)),
                "review_record_sha256": _digest(path.read_bytes()),
                "recorded_responsiveness_v3": recorded,
                "derived_label_v3": recomputed_v3,
                "derived_label_v3_1": label(coverage, semantics_v31),
                "semantics_v3_1": [
                    {
                        "semantic": item["semantic"],
                        "row_index": item.get("row_index"),
                        "absent_reason": item.get("absent_reason"),
                        "names_a_row": item.get("row_index") is not None,
                    }
                    for item in coverage
                    if item["semantic"] in semantics_v31
                ],
                "dropped_semantic": {
                    "semantic": "compilation_source",
                    "row_index": next(
                        item.get("row_index")
                        for item in coverage
                        if item["semantic"] == "compilation_source"
                    ),
                },
            }
        )

    return {
        "schema": SCHEMA,
        "question_id": QUESTION_ID,
        "what": (
            "CQ-C-03's label under competency questions v3.1, derived from the"
            " coverage entries the v3 reviews already wrote. Neither cell was"
            " re-reviewed and neither review record is touched. The rule: COVERED"
            " when every remaining semantic names a row, NONE when none does,"
            " PARTIAL otherwise."
        ),
        "expected_outcome": {
            "kind": v31["expected_outcome"]["kind"],
            "expected_coverage": v31["expected_outcome"]["expected_coverage"],
        },
        "questions_v3_sha256": _digest(QUESTIONS_V3.read_bytes()),
        "questions_v3_1_sha256": _digest(QUESTIONS_V31.read_bytes()),
        "required_semantics_v3": semantics_v3,
        "required_semantics_v3_1": semantics_v31,
        "dropped_semantics": dropped,
        "cells": cells,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="report the derivation without writing the file",
    )
    arguments = parser.parse_args(argv)
    try:
        derived = build()
        if not arguments.print_only:
            OUTPUT.write_bytes(
                json.dumps(derived, ensure_ascii=False, indent=2).encode("utf-8")
                + b"\n"
            )
        for cell in derived["cells"]:
            print(
                f"{cell['run_id']}: v3 {cell['derived_label_v3']}"
                f" -> v3.1 {cell['derived_label_v3_1']}"
                f" (expected {derived['expected_outcome']['expected_coverage']})"
            )
    except (OSError, KeyError, StopIteration, TypeError, ValueError) as error:
        print(f"derive-cq-c-03: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
