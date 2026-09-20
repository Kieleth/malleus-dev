"""Assemble reuse-01's preliminary review record from the reviewer's own files.

The reviewer judges 429 witnesses and thirty questions. Typing that into one
markdown block by hand is how run-05's task carried run-02's counts into a live
review, so the reviewer writes two kinds of file and this script assembles them:

* ``review-witnesses.json``, a list of ``{witness_key, source_support,
  source_locators, rationale}``, one entry per distinct witness the query result
  returns;
* ``review-block.<question id>.json``, the per-question surface this package
  already wrote, with ``question_responsiveness``, ``responsiveness_rationale``,
  ``assembly``, ``coverage`` and ``source_locators`` filled in.

Nothing here judges. It rebuilds each question's ``rows`` from the query result
rather than trusting the block's copy, refuses a block whose rows were edited,
strips the two reader-facing keys the record's exact key set does not carry,
orders the questions as the question file orders them, and writes the record.
``completed_at`` is the newest block's modification time, which is the practice
run-22's record used, floored to the second and stamped in UTC.

    .venv/bin/python paper-v4/evaluation-v4/reuse-01/assemble_record.py \\
        --actor actor:claude-preliminary-reuse-01
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
PRIVATE = ROOT / "private/paper-v4-reuse-01"
MANIFEST = HERE / "review-input-manifest.json"
WITNESSES = HERE / "review-witnesses.json"
RECORD = HERE / "review-record.preliminary.md"
PROTOCOL = ROOT / "paper-v4/evaluation-v4/review-protocol-v3.2.json"

RECORD_SCHEMA = "malleus.paper-v4.source-grounded-review/v3.2"
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


def _rows_from_result() -> dict[str, list[dict[str, Any]]]:
    result = json.loads((PRIVATE / "query/query-result.json").read_bytes())
    rows: dict[str, list[dict[str, Any]]] = {}
    for query in result["queries"]:
        rows[str(query["question_id"])] = [
            {
                "row_index": index,
                "witness_key": str(
                    row["witness"].get("relation_id") or row["witness"]["record_id"]
                ),
            }
            for index, row in enumerate(query["rows"])
        ]
    return rows


def assemble(actor: str) -> dict[str, object]:
    manifest = json.loads(MANIFEST.read_bytes())
    ids = list(manifest["question_ids"])
    rows_by_question = _rows_from_result()

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
                f"{path.name} rows differ from the query result; the rows are the"
                " script's and are not the reviewer's to edit"
            )
        if block["question_responsiveness"] == "PENDING" or block["assembly"] == "PENDING":
            raise AssemblyRefusal(f"{path.name} is not filled in")
        questions.append(
            {
                "question_id": question_id,
                "question_responsiveness": block["question_responsiveness"],
                "responsiveness_rationale": block["responsiveness_rationale"],
                "assembly": block["assembly"],
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
        " reuse-01\n\n"
        "Assembled by `paper-v4/evaluation-v4/reuse-01/assemble_record.py` from the"
        " preliminary\nreviewer's `review-witnesses.json` and its thirty filled"
        " review blocks. The rows are\nrebuilt from the query result, not copied"
        " from the blocks. `PRELIMINARY_COMPLETE` is\nnot paper evidence; Luis"
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
