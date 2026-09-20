"""Freeze reuse-01: copy the public set, measure the leak ladder, write the record.

reuse-01 has no producer, no gate and no runner, so this is a smaller freeze than
``paper-v4/experiment-v4/run-25/freeze.py``. What it keeps from that script is
the part that matters for publication: every file that is about to become public
is measured against the selected reading with the same ladder, and one that
shares a sixty-character normalized run is moved into ``private/`` and recorded
as withheld instead. The rule is run-25's, in its
``results/withheld-artifacts.json``.

It also writes ``results/graph-reference.json``, which is this cell's honest
statement about the graph it queried: the identities are run-23's, read out of
run-23's own frozen run record, and the ledger digest is measured before and
after the query so that "nothing about the graph moved" is a number rather than
a promise.

    .venv/bin/python paper-v4/experiment-v4/reuse-01/freeze.py \\
        --ledger-before <sha256 hex> --ledger-after <sha256 hex>
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRIVATE = ROOT / "private/paper-v4-reuse-01"
PUBLIC = HERE / "results"
RUN_23 = ROOT / "paper-v4/experiment-v4/run-23"
RUN_23_LEDGER = ROOT / "private/paper-v4-v4-run-23/ledger/history.jsonl"
QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-set-b.json"
READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"

LEAK_WINDOW = 60

PUBLIC_FILES = {
    "native-query-binding.json": "results/native-query-binding.json",
    "query-trace-summary.json": "query/trace-summary.json",
    "query-type-sets.json": "query-type-sets.json",
    "query-type-sets.note.json": "query-type-sets.note.json",
    "launch-log.json": "launch-log.json",
}
WITHHELD_SOURCES = {
    "query-result.json": "query/query-result.json",
}
CARRIES = {
    "query-result.json": "PROJECTED_ROW_FIELDS_QUOTING_THE_READING",
}
SUBSTITUTES = {
    "query-result.json": (
        "results/query-trace-summary.json and the row counts in the review input"
        " manifest"
    ),
}


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _ladder():
    path = HERE / "leak_ladder.py"
    specification = importlib.util.spec_from_file_location("reuse_01_ladder", path)
    if specification is None or specification.loader is None:
        raise ValueError(f"the ladder is not readable: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def copy_public() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    for name, relative in PUBLIC_FILES.items():
        shutil.copyfile(PRIVATE / relative, PUBLIC / name)


def graph_reference(before: str, after: str) -> dict[str, object]:
    run_result = json.loads((RUN_23 / "results/run-result.json").read_bytes())
    binding = json.loads((PUBLIC / "native-query-binding.json").read_bytes())
    result = json.loads((PRIVATE / "query/query-result.json").read_bytes())
    measured = "sha256:" + hashlib.sha256(RUN_23_LEDGER.read_bytes()).hexdigest()
    if measured != after:
        raise ValueError("the ledger digest moved after the run was reported")
    if before != after:
        raise ValueError(f"the ledger changed during the query: {before} to {after}")
    if result["inputs"]["ledger_head"] != run_result["ledger_head"]:
        raise ValueError("the query did not read run-23's ledger head")
    if result["inputs"]["replay_receipt_sha256"] != run_result["replay_receipt_sha256"]:
        raise ValueError("the replay receipt differs from run-23's frozen one")
    if binding["bound_after_replay_receipt_sha256"] != run_result["replay_receipt_sha256"]:
        raise ValueError("the binding was not bound after run-23's replay receipt")
    if result["forbidden_attempts"] != {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }:
        raise ValueError("the query region recorded a forbidden access attempt")
    rows = {item["question_id"]: len(item["rows"]) for item in result["queries"]}
    witnesses = {
        (row["witness"].get("relation_id") or row["witness"]["record_id"])
        for item in result["queries"]
        for row in item["rows"]
    }
    question_ids = [
        item["id"] for item in json.loads(QUESTIONS.read_bytes())["questions"]
    ]
    if sorted(rows) != sorted(question_ids):
        raise ValueError("the query did not answer this cell's questions")
    kinds: dict[str, int] = {}
    for item in result["queries"]:
        for row in item["rows"]:
            kinds[row["kind"]] = kinds.get(row["kind"], 0) + 1
    case_kinds: dict[str, int] = {}
    for query in binding["queries"]:
        for case in query["cases"]:
            case_kinds[case["kind"]] = case_kinds.get(case["kind"], 0) + 1
    return {
        "schema": "malleus.paper-v4.reuse-01-graph-reference/v1",
        "run_id": "reuse-01",
        "status": "QUERIED_RUN_23_WITHOUT_MOVING_IT",
        "what_this_cell_is": (
            "A second, independent question set put to run-23's already accepted"
            " and frozen graph. No producer ran, no ontology was authored, nothing"
            " was captured, admitted, disposed or replayed here. The only new"
            " artefacts are the thirty type sets, the binding they expand to and"
            " the query result."
        ),
        "graph": {
            "authored_by": "run-23",
            "ledger": str(RUN_23_LEDGER.relative_to(ROOT)),
            "ledger_sha256_before_query": before,
            "ledger_sha256_after_query": after,
            "ledger_unchanged": True,
            "ledger_head": run_result["ledger_head"],
            "accepted_ontology_sha256": run_result["ontology_sha256"],
            "validated_contract_sha256": run_result["validated_contract_sha256"],
            "replay_receipt_sha256": run_result["replay_receipt_sha256"],
            "graph_state_digest": result["graph_state_digest"],
            "entities": run_result["graph"]["entities"],
            "events": run_result["graph"]["events"],
            "relations": run_result["graph"]["relations"],
        },
        "questions": {
            "file": str(QUESTIONS.relative_to(ROOT)),
            "sha256": digest(QUESTIONS),
            "set": "B",
            "count": len(question_ids),
            "authored_blind_to_this_graph": True,
        },
        "binding": {
            "file": "paper-v4/experiment-v4/reuse-01/results/native-query-binding.json",
            "sha256": digest(PUBLIC / "native-query-binding.json"),
            "cases_sha256": binding["cases_sha256"],
            "population_surface_sha256": binding["population_surface_sha256"],
            "cases": sum(case_kinds.values()),
            "cases_by_kind": dict(sorted(case_kinds.items())),
            "bound_by": (
                "paper-v4/experiment-v4/run-23/bind_from_surface.py, unedited, from"
                " run-23's accepted population surface and validated contract"
            ),
            "type_set_closure": "ACCEPTED",
        },
        "query": {
            "executed_by": "paper-v4/experiment-v4/run-23/native_query.py, unedited",
            "core_pin": "c95dba7b86bb61487bda9a52458e1ea47cce20ab",
            "forbidden_attempts": result["forbidden_attempts"],
            "rows_total": sum(rows.values()),
            "rows_per_question": rows,
            "rows_by_kind": dict(sorted(kinds.items())),
            "distinct_witnesses": len(witnesses),
            "records_traced": json.loads(
                (PUBLIC / "query-trace-summary.json").read_bytes()
            )["witnesses_traced"],
        },
    }


def freeze(before: str, after: str) -> dict[str, object]:
    copy_public()
    reference = graph_reference(before, after)
    (PUBLIC / "graph-reference.json").write_text(
        json.dumps(reference, indent=2) + "\n", encoding="utf-8"
    )

    ladder = _ladder()
    public_paths = [
        path
        for path in sorted(PUBLIC.iterdir())
        if path.is_file() and path.name not in {".gitkeep", "withheld-artifacts.json"}
    ]
    private_paths = [PRIVATE / relative for relative in WITHHELD_SOURCES.values()]
    measured = ladder.measure(public_paths + private_paths, READING)
    leaks = [path for path in public_paths if measured[str(path)] >= LEAK_WINDOW]
    moved: list[tuple[str, Path, int]] = []
    for path in leaks:
        destination = PRIVATE / "withheld-results" / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(path), destination)
        moved.append((path.name, destination, measured[str(path)]))

    withheld = []
    for name, relative in WITHHELD_SOURCES.items():
        source = PRIVATE / relative
        item = {
            "name": name,
            "private_path": str(source.relative_to(ROOT)),
            "sha256": digest(source),
            "carries": CARRIES[name],
            "shared_run_chars_at_least": measured[str(source)],
        }
        if name in SUBSTITUTES:
            item["public_substitute"] = SUBSTITUTES[name]
        withheld.append(item)
    for name, destination, rung in moved:
        withheld.append(
            {
                "name": name,
                "private_path": str(destination.relative_to(ROOT)),
                "sha256": digest(destination),
                "carries": "SHARES_A_60_CHARACTER_RUN_WITH_THE_READING",
                "shared_run_chars_at_least": rung,
            }
        )
    withheld.sort(key=lambda item: item["name"])
    public_measured = {
        path.name: measured[str(path)] for path in public_paths if path not in leaks
    }
    (PUBLIC / "withheld-artifacts.json").write_text(
        json.dumps(
            {
                "schema": "malleus.paper-v4.reuse-01-withheld-artifacts/v1",
                "run_id": "reuse-01",
                "reason": (
                    "The file below reproduces text of the selected reading. Only"
                    " its identity is public. This cell withholds one file where a"
                    " graph cell withholds eight, because it ran no producer, no"
                    " admission and no replay and so produced no capture, plan,"
                    " gap set, export, receipt or ledger of its own."
                ),
                "check": {
                    "method": "SHARED_NORMALIZED_CHARACTER_RUN_AGAINST_EVERY_READING_BLOCK",
                    "normalization": "UNICODE_WHITESPACE_COLLAPSED_TO_SINGLE_SPACE",
                    "ladder": list(ladder.LADDER),
                    "measured_by": "paper-v4/experiment-v4/reuse-01/leak_ladder.py",
                    "frozen_threshold": "NO_PUBLIC_FILE_SHARES_A_60_CHARACTER_RUN",
                    "public_files_measured": public_measured,
                    "also_measured": {
                        "paper-v4/experiment-v4/competency-questions-set-b.json": (
                            ladder.measure([QUESTIONS], READING)[str(QUESTIONS)]
                        )
                    },
                },
                "withheld": withheld,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    frozen = {
        f"results/{path.name}": digest(path)
        for path in sorted(PUBLIC.iterdir())
        if path.is_file() and path.suffix != ".pyc" and path.name != ".gitkeep"
    }
    return {
        "frozen": frozen,
        "withheld": [item["name"] for item in withheld],
        "public_ladder_max": max(public_measured.values()),
        "rows_total": reference["query"]["rows_total"],
        "distinct_witnesses": reference["query"]["distinct_witnesses"],
        "ledger_unchanged": reference["graph"]["ledger_unchanged"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ledger-before", required=True)
    parser.add_argument("--ledger-after", required=True)
    arguments = parser.parse_args(argv)
    try:
        report = freeze(arguments.ledger_before, arguments.ledger_after)
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"reuse-01-freeze: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
