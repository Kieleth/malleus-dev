"""Assemble reuse-01-baseline's preliminary review record from the reviewer's files.

The answer surface's twin of `paper-v4/evaluation-v4/reuse-01/assemble_record.py`
and the same division of labour: the reviewer writes one judgement per cited
claim in ``review-witnesses.json`` and fills the thirty per-question review
blocks, and this script rebuilds each question's ``rows`` from the answer file,
refuses a block whose rows were edited, and writes the record.

Two differences from the graph twin, both forced by the surface:

* a witness is one cited claim keyed by its ``claim_id``, so the rows come from
  the answer file's claims and not from a query result;
* ``assembly`` is ``NOT_APPLICABLE`` on every question and this script refuses
  anything else, because a prose answer always assembles and a constant token in
  a comparison table reads as a grade.

    .venv/bin/python paper-v4/evaluation-v4/reuse-01-baseline/assemble_record.py \\
        --actor actor:claude-preliminary-reuse-01-baseline
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ANSWER_FILE = ROOT / "private/paper-v4-reuse-01-baseline/producer/work/answers.json"
MANIFEST = HERE / "review-input-manifest.json"
WITNESSES = HERE / "review-witnesses.json"
RECORD = HERE / "review-record.preliminary.md"
PROTOCOL = ROOT / "paper-v4/evaluation-v4/review-protocol-v3.2.json"

RECORD_SCHEMA = "malleus.paper-v4.source-grounded-review/v3.2"
ASSEMBLY = "NOT_APPLICABLE"
QUESTION_KEYS = (
    "question_id",
    "question_responsiveness",
    "responsiveness_rationale",
    "assembly",
    "coverage",
    "source_locators",
    "rows",
)
WITNESS_KEYS = ("witness_key", "source_support", "source_locators", "rationale")


class AssemblyRefusal(ValueError):
    """The reviewer's files do not assemble into a record."""


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _rows_from_answers() -> dict[str, list[dict[str, Any]]]:
    document = json.loads(ANSWER_FILE.read_bytes())
    return {
        str(answer["question_id"]): [
            {"row_index": index, "witness_key": str(claim["claim_id"])}
            for index, claim in enumerate(answer["claims"])
        ]
        for answer in document["answers"]
    }


def assemble(actor: str) -> dict[str, object]:
    manifest = json.loads(MANIFEST.read_bytes())
    ids = list(manifest["question_ids"])
    rows_by_question = _rows_from_answers()

    witnesses = json.loads(WITNESSES.read_bytes())
    if not isinstance(witnesses, list) or not witnesses:
        raise AssemblyRefusal("review-witnesses.json must be a nonempty list")
    judged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(witnesses):
        if sorted(raw) != sorted(WITNESS_KEYS):
            raise AssemblyRefusal(
                f"review-witnesses.json[{index}] must carry exactly"
                f" {sorted(WITNESS_KEYS)}"
            )
        key = str(raw["witness_key"])
        if key in seen:
            raise AssemblyRefusal(f"review-witnesses.json judges {key} twice")
        seen.add(key)
        judged.append({name: raw[name] for name in WITNESS_KEYS})

    questions: list[dict[str, Any]] = []
    newest = 0.0
    for question_id in ids:
        path = HERE / f"review-block.{question_id}.json"
        if not path.is_file():
            raise AssemblyRefusal(f"the reviewer wrote no block for {question_id}")
        newest = max(newest, path.stat().st_mtime)
        block = json.loads(path.read_bytes())
        if str(block["question_id"]) != question_id:
            raise AssemblyRefusal(f"{path.name} carries another question's id")
        expected_rows = rows_by_question[question_id]
        if block["rows"] != expected_rows:
            raise AssemblyRefusal(
                f"{path.name} rows differ from the answer file; the rows are the"
                " script's and are not the reviewer's to edit"
            )
        if block["question_responsiveness"] == "PENDING":
            raise AssemblyRefusal(f"{path.name} is not filled in")
        if block["assembly"] != ASSEMBLY:
            raise AssemblyRefusal(
                f"{path.name} carries assembly {block['assembly']!r}; the answer"
                f" surface takes {ASSEMBLY} and nothing else"
            )
        questions.append(
            {
                "question_id": question_id,
                "question_responsiveness": block["question_responsiveness"],
                "responsiveness_rationale": block["responsiveness_rationale"],
                "assembly": ASSEMBLY,
                "coverage": block["coverage"],
                "source_locators": block["source_locators"],
                "rows": expected_rows,
            }
        )
    for question in questions:
        if sorted(question) != sorted(QUESTION_KEYS):
            raise AssemblyRefusal("a question entry does not carry the exact key set")

    completed_at = (
        datetime.fromtimestamp(newest, tz=timezone.utc)
        .replace(microsecond=0)
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    )
    record = {
        "schema": RECORD_SCHEMA,
        "status": "PRELIMINARY_COMPLETE",
        "inputs": {
            "review_protocol_sha256": _digest(PROTOCOL.read_bytes()),
            "review_input_manifest_sha256": _digest(MANIFEST.read_bytes()),
        },
        "preliminary": {
            "evaluator_kind": "CLAUDE_PRELIMINARY",
            "actor_id": actor,
            "completed_at": completed_at,
        },
        "witnesses": judged,
        "questions": questions,
        "ratification": {
            "evaluator_kind": "HUMAN_AUTHOR",
            "actor_id": "actor:luis",
            "disposition": "PENDING",
            "completed_at": "",
            "notes": "",
        },
    }
    body = (
        "# Malleus paper v4 source-grounded review record, protocol v3.2,"
        " reuse-01-baseline\n\n"
        "Assembled by"
        " `paper-v4/evaluation-v4/reuse-01-baseline/assemble_record.py` from the\n"
        "preliminary reviewer's `review-witnesses.json` and its thirty filled"
        " review blocks.\nThe rows are rebuilt from the answer file, not copied"
        " from the blocks.\n`PRELIMINARY_COMPLETE` is not paper evidence; Luis"
        " ratifies.\n\n"
        "```json\n"
        + json.dumps(record, ensure_ascii=False, indent=2)
        + "\n```\n"
    )
    RECORD.write_text(body, encoding="utf-8")
    support: dict[str, int] = {}
    for witness in judged:
        support[witness["source_support"]] = support.get(witness["source_support"], 0) + 1
    labels: dict[str, int] = {}
    for question in questions:
        labels[question["question_responsiveness"]] = (
            labels.get(question["question_responsiveness"], 0) + 1
        )
    return {
        "record": str(RECORD.relative_to(ROOT)),
        "record_sha256": _digest(RECORD.read_bytes()),
        "witnesses": len(judged),
        "questions": len(questions),
        "completed_at": completed_at,
        "source_support": dict(sorted(support.items())),
        "question_responsiveness": dict(sorted(labels.items())),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--actor", required=True)
    arguments = parser.parse_args(argv)
    try:
        print(json.dumps(assemble(arguments.actor), indent=2, sort_keys=True))
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"assemble-record: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
