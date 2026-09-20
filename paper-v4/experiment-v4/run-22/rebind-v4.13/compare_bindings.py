"""Count what run-22's frozen ledger returns under v4.12 and under v4.13.

Run-22 was bound by harness v4.12, whose binder reached a listed
subject-bearing type only through ``ENTITY_NO_SUBJECT`` (its subject-less
records) and through ``SUBJECT`` paired with the subject types the set itself
listed. Eleven of the cell's 102 required semantics were read UNREACHED_RECORD
at review for that reason (E-0342). Harness v4.13 added the ``SUBJECT_ANY``
case kind (E-0343): a listed subject-bearing type reaches its subject-carrying
records whatever their subjects' types.

A query reads a ledger and writes nothing into it, so run-22's frozen ledger
can be re-queried under the later binder and reported under both. This script
is the comparison and nothing else: it counts cases, rows and witnesses and
writes ``comparison.json``. No figure in that file or in the README is typed
by hand.

Counting rules, taken from the executor rather than invented here:

* A **case** is one entry of ``queries[].cases``; its ``kind`` is one of the
  four v4.12 kinds plus ``SUBJECT_ANY``.
* A **row** is one entry of ``queries[].rows``. The executor emits one row per
  distinct witness per question, so a question's row count is also its count of
  distinct witness keys.
* A **witness record id** is a value of a row's ``witness`` object: the record
  for an ``ENTITY`` row, the record and its subject for a ``SUBJECT`` row, the
  relation and its two endpoints for a ``RELATION`` row. These are exactly the
  ids the executor collects and the trace resolves, so the cell total of the
  distinct ones is ``witnesses_traced`` in the trace summary.

Nothing read here is projected: only counts and digests are written, so the
output carries no text of the reading.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

BINDER = ROOT / "paper-v4/experiment-v4/run-23/bind_from_surface.py"
EXECUTOR = ROOT / "paper-v4/experiment-v4/run-23/native_query.py"

V412 = {
    "harness": "v4.12",
    "binding": ROOT / "paper-v4/experiment-v4/run-22/results/native-query-binding.json",
    "query_result": ROOT / "private/paper-v4-v4-run-22/query/query-result.json",
    "trace_summary": ROOT / "private/paper-v4-v4-run-22/query/trace-summary.json",
}
V413 = {
    "harness": "v4.13",
    "binding": HERE / "native-query-binding.json",
    "query_result": ROOT / "private/paper-v4-v4-run-22/rebind-v4.13/query-result.json",
    "trace_summary": ROOT / "private/paper-v4-v4-run-22/rebind-v4.13/trace-summary.json",
}
OUTPUT = HERE / "comparison.json"

SCHEMA = "malleus.paper-v4.run-22-rebind-comparison/v1"


class ComparisonRefusal(ValueError):
    """The comparison cannot be made from what is on disk."""


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _read(path: Path) -> dict:
    if not path.is_file():
        raise ComparisonRefusal(f"input is not on disk: {path}")
    return json.loads(path.read_bytes())


def _witness_ids(row: dict) -> list[str]:
    return [value for value in row["witness"].values() if isinstance(value, str)]


def measure(side: dict) -> dict:
    binding = _read(side["binding"])
    result = _read(side["query_result"])
    summary = _read(side["trace_summary"])

    cases_by_kind: Counter[str] = Counter()
    cases_per_question: dict[str, int] = {}
    for query in binding["queries"]:
        question_id = str(query["question_id"])
        cases_per_question[question_id] = len(query["cases"])
        for case in query["cases"]:
            cases_by_kind[str(case["kind"])] += 1

    rows_per_question: dict[str, int] = {}
    witnesses_per_question: dict[str, int] = {}
    rows_by_kind: Counter[str] = Counter()
    cell_witnesses: set[str] = set()
    for query in result["queries"]:
        question_id = str(query["question_id"])
        rows = query["rows"]
        rows_per_question[question_id] = len(rows)
        seen: set[str] = set()
        for row in rows:
            rows_by_kind[str(row["kind"])] += 1
            ids = _witness_ids(row)
            seen.update(ids)
            cell_witnesses.update(ids)
        witnesses_per_question[question_id] = len(seen)

    traced = int(summary["witnesses_traced"])
    if traced != len(cell_witnesses):
        raise ComparisonRefusal(
            f"{side['harness']}: the trace summary traced {traced} witnesses "
            f"and the rows carry {len(cell_witnesses)} distinct ids"
        )

    return {
        "harness": side["harness"],
        "binding_path": str(side["binding"].relative_to(ROOT)),
        "binding_schema": binding["schema"],
        "binding_sha256": _digest(side["binding"].read_bytes()),
        "cases_sha256": binding["cases_sha256"],
        "population_surface_sha256": binding["population_surface_sha256"],
        "bound_after_replay_receipt_sha256": binding[
            "bound_after_replay_receipt_sha256"
        ],
        "case_kinds": list(binding["expansion"]["case_kinds"]),
        "cases_total": sum(cases_by_kind.values()),
        "cases_by_kind": dict(sorted(cases_by_kind.items())),
        "cases_per_question": cases_per_question,
        "query_result_path": str(side["query_result"].relative_to(ROOT)),
        "query_result_sha256": _digest(side["query_result"].read_bytes()),
        "query_result_ledger_head": result["inputs"]["ledger_head"],
        "query_result_replay_receipt_sha256": result["inputs"][
            "replay_receipt_sha256"
        ],
        "graph_state_digest": result["graph_state_digest"],
        "forbidden_attempts": result["forbidden_attempts"],
        "rows_total": sum(rows_per_question.values()),
        "rows_by_kind": dict(sorted(rows_by_kind.items())),
        "rows_per_question": rows_per_question,
        "witness_ids_per_question": witnesses_per_question,
        "witnesses_traced": traced,
        "trace_summary_sha256": _digest(side["trace_summary"].read_bytes()),
    }


def build() -> dict:
    before = measure(V412)
    after = measure(V413)
    if before["query_result_ledger_head"] != after["query_result_ledger_head"]:
        raise ComparisonRefusal("the two queries did not read the same ledger head")
    if before["graph_state_digest"] != after["graph_state_digest"]:
        raise ComparisonRefusal("the two queries did not read the same graph state")
    if before["population_surface_sha256"] != after["population_surface_sha256"]:
        raise ComparisonRefusal("the two bindings were not bound from one surface")

    ids = list(before["rows_per_question"])
    if sorted(ids) != sorted(after["rows_per_question"]):
        raise ComparisonRefusal("the two query results do not answer one question set")

    per_question = [
        {
            "question_id": question_id,
            "rows_v4_12": before["rows_per_question"][question_id],
            "rows_v4_13": after["rows_per_question"][question_id],
            "rows_delta": after["rows_per_question"][question_id]
            - before["rows_per_question"][question_id],
            "witness_ids_v4_12": before["witness_ids_per_question"][question_id],
            "witness_ids_v4_13": after["witness_ids_per_question"][question_id],
            "witness_ids_delta": after["witness_ids_per_question"][question_id]
            - before["witness_ids_per_question"][question_id],
            "cases_v4_12": before["cases_per_question"][question_id],
            "cases_v4_13": after["cases_per_question"][question_id],
        }
        for question_id in ids
    ]
    return {
        "schema": SCHEMA,
        "run_id": "run-22",
        "what": (
            "run-22's frozen ledger queried twice: once by the binding frozen with"
            " the cell under harness v4.12, once by the binding this directory"
            " holds, written by run-23's v4.13 binder from run-22's own accepted"
            " surface, contract and type sets. The ledger, the surface, the"
            " contract and the thirty type sets are unchanged; the binder is the"
            " single difference."
        ),
        "binder": {
            "path": str(BINDER.relative_to(ROOT)),
            "sha256": _digest(BINDER.read_bytes()),
        },
        "executor": {
            "path": str(EXECUTOR.relative_to(ROOT)),
            "sha256": _digest(EXECUTOR.read_bytes()),
        },
        "v4_12": before,
        "v4_13": after,
        "per_question": per_question,
        "totals": {
            "cases_v4_12": before["cases_total"],
            "cases_v4_13": after["cases_total"],
            "rows_v4_12": before["rows_total"],
            "rows_v4_13": after["rows_total"],
            "witnesses_traced_v4_12": before["witnesses_traced"],
            "witnesses_traced_v4_13": after["witnesses_traced"],
            "questions_with_more_rows": sum(
                1 for item in per_question if item["rows_delta"] > 0
            ),
            "questions_with_fewer_rows": sum(
                1 for item in per_question if item["rows_delta"] < 0
            ),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="report the totals without writing comparison.json",
    )
    arguments = parser.parse_args(argv)
    try:
        comparison = build()
        if not arguments.print_only:
            OUTPUT.write_bytes(
                json.dumps(comparison, ensure_ascii=False, indent=2).encode("utf-8")
                + b"\n"
            )
        print(json.dumps(comparison["totals"], indent=2, sort_keys=True))
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"compare-bindings: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
