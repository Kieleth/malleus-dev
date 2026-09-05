"""Validate the v4.4 ENTITY restriction against run-09's already-judged record.

The change under test in the query surface is a removal, so it can be measured
before a producer runs: expand run-09's frozen type sets against run-09's frozen
surface with this cell's rule, keep the cases the rule keeps, select the rows of
run-09's frozen query result that came from those cases, and read their labels
off run-09's preliminary review record. Nothing is executed. No graph is
reopened, no query is run, no ontology is compiled and no model is called.

Run-09 is frozen, so every one of its files is read and none is written. The
rows themselves stay where they are: this script writes counts, per question and
per label, and no row content, no record identifier and no reading text.

What it can establish: how many of run-09's rows the restriction keeps, and what
the reviewers already said about exactly those rows. What it cannot: anything
about run-14's own producer, whose graph does not exist. A row count carried
over from another cell's graph is a bound on the review, not a result.

    .venv/bin/python paper-v4/experiment-v4/run-14/offline_validation.py
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN_09 = HERE.parent / "run-09"

RECORD_SCHEMA = "malleus.paper-v4.run-14-offline-validation/v1"
QUESTION_IDS = ("CQ-01", "CQ-02", "CQ-03", "CQ-04")

# Run-09's frozen inputs. The first three are public and digest-pinned by
# run-09's own contract test; the fourth is the withheld query result; the fifth
# is the merged preliminary review record.
TYPE_SETS = RUN_09 / "results/query-type-sets.json"
SURFACE = RUN_09 / "ontology-run/population-surface.json"
EXECUTED_BINDING = RUN_09 / "results/native-query-binding.json"
QUERY_RESULT = ROOT / "private/paper-v4-v4-run-09/query/query-result.json"
REVIEW_RECORD = ROOT / "paper-v4/evaluation-v4/run-09/review-record.preliminary.md"

OUTPUT = HERE / "offline-validation.json"


class OfflineValidationRefusal(ValueError):
    """A frozen input is not the shape this validation reads."""


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _binder():
    """This cell's binder. The rule under validation is the shipped rule."""
    spec = importlib.util.spec_from_file_location(
        "paper_v4_run_14_binder", HERE / "bind_from_surface.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def case_identity(case: dict[str, object]) -> tuple[str, ...]:
    """A case's types, which is all a type-only case is."""
    kind = str(case["kind"])
    if kind == "ENTITY":
        return (kind, str(case["record_type"]))
    if kind == "RELATION":
        return (
            kind,
            str(case["source_record_type"]),
            str(case["relation_record_type"]),
            str(case["target_record_type"]),
        )
    if kind == "SUBJECT":
        return (kind, str(case["record_type"]), str(case["subject_record_type"]))
    raise OfflineValidationRefusal(f"unknown case kind: {kind}")


def review_labels(source: str) -> dict[str, dict[int, str]]:
    """Every judged row's label, by question and zero-based row index."""
    opening = "```json\n"
    start = source.index(opening) + len(opening)
    record = json.loads(source[start : source.index("\n```", start)])
    if record["status"] != "PRELIMINARY_COMPLETE":
        raise OfflineValidationRefusal(
            f"the review record is {record['status']}, not PRELIMINARY_COMPLETE"
        )
    labels: dict[str, dict[int, str]] = {}
    for question in record["questions"]:
        labels[str(question["question_id"])] = {
            int(row["row_index"]): str(row["source_support"])
            for row in question["rows"]
        }
    return labels


def validate() -> dict[str, object]:
    binder = _binder()
    surface_source = SURFACE.read_bytes()
    by_name = binder.load_surface(surface_source)
    relations = binder._relation_types(by_name)
    type_sets = json.loads(TYPE_SETS.read_bytes())
    executed = json.loads(EXECUTED_BINDING.read_bytes())
    result = json.loads(QUERY_RESULT.read_bytes())
    labels = review_labels(REVIEW_RECORD.read_text(encoding="utf-8"))

    if executed["schema"] != "malleus.paper-v4.native-query-binding/v3":
        raise OfflineValidationRefusal(
            "run-09's executed binding is not the v3 binding this validation reads"
        )
    frozen = {
        str(query["question_id"]): query["cases"] for query in executed["queries"]
    }
    rows_by_question = {
        str(query["question_id"]): query["rows"] for query in result["queries"]
    }
    if sorted(type_sets) != list(QUESTION_IDS):
        raise OfflineValidationRefusal("run-09's type sets name other questions")

    questions: list[dict[str, object]] = []
    totals = {
        "cases_v3": 0,
        "cases_v4": 0,
        "cases_removed": 0,
        "rows_v3": 0,
        "rows_kept": 0,
        "rows_removed": 0,
    }
    kept_by_kind: dict[str, int] = {}
    kept_by_label: dict[str, int] = {}

    for question_id in QUESTION_IDS:
        types = sorted(set(type_sets[question_id]))
        bearing = [
            name
            for name in types
            if binder.SUBJECT_SLOT in binder._slot_names(by_name[name])
        ]
        restricted = binder._cases(
            types=types, relations=relations, by_name=by_name
        )
        kept_identities = {case_identity(case) for case in restricted}
        frozen_cases = frozen[question_id]
        frozen_identities = {case_identity(case) for case in frozen_cases}
        if not kept_identities <= frozen_identities:
            raise OfflineValidationRefusal(
                f"the v4 expansion of {question_id} is not a subset of the v3 one"
            )
        kept_ordinals = {
            int(case["ordinal"])
            for case in frozen_cases
            if case_identity(case) in kept_identities
        }

        rows = rows_by_question[question_id]
        judged = labels[question_id]
        if sorted(judged) != list(range(len(rows))):
            raise OfflineValidationRefusal(
                f"the review record does not judge every row of {question_id}"
            )
        by_kind: dict[str, int] = {}
        by_label: dict[str, int] = {}
        kept = 0
        for index, row in enumerate(rows):
            if int(row["case_ordinal"]) not in kept_ordinals:
                continue
            kept += 1
            by_kind[str(row["kind"])] = by_kind.get(str(row["kind"]), 0) + 1
            label = judged[index]
            by_label[label] = by_label.get(label, 0) + 1
        for source, target in ((by_kind, kept_by_kind), (by_label, kept_by_label)):
            for name, count in source.items():
                target[name] = target.get(name, 0) + count

        questions.append(
            {
                "question_id": question_id,
                "types": len(types),
                "subject_bearing_types": len(bearing),
                "cases_v3": len(frozen_cases),
                "cases_v4": len(restricted),
                "cases_removed": len(frozen_cases) - len(restricted),
                "rows_v3": len(rows),
                "rows_kept": kept,
                "rows_removed": len(rows) - kept,
                "rows_kept_by_kind": dict(sorted(by_kind.items())),
                "rows_kept_by_label": dict(sorted(by_label.items())),
            }
        )
        totals["cases_v3"] += len(frozen_cases)
        totals["cases_v4"] += len(restricted)
        totals["cases_removed"] += len(frozen_cases) - len(restricted)
        totals["rows_v3"] += len(rows)
        totals["rows_kept"] += kept
        totals["rows_removed"] += len(rows) - kept

    totals["rows_kept_by_kind"] = dict(sorted(kept_by_kind.items()))
    totals["rows_kept_by_label"] = dict(sorted(kept_by_label.items()))
    totals["rows_kept_unjudged"] = 0

    return {
        "schema": RECORD_SCHEMA,
        "run_id": "run-14",
        "status": "COMPUTED",
        "change_id": "ENTITY_KIND_RESTRICTED",
        "rule": (
            "one ENTITY case per type in a question's set that carries no subject"
            " on the surface; SUBJECT and RELATION expansion unchanged"
        ),
        "executes": "NOTHING",
        "measured_on": "run-09",
        "inputs": {
            "binder": {
                "path": "paper-v4/experiment-v4/run-14/bind_from_surface.py",
                "sha256": _digest((HERE / "bind_from_surface.py").read_bytes()),
                "binding_schema": binder.BINDING_SCHEMA,
            },
            "type_sets": {
                "path": "paper-v4/experiment-v4/run-09/results/query-type-sets.json",
                "sha256": _digest(TYPE_SETS.read_bytes()),
            },
            "population_surface": {
                "path": (
                    "paper-v4/experiment-v4/run-09/ontology-run/population-surface.json"
                ),
                "sha256": _digest(surface_source),
            },
            "executed_binding": {
                "path": (
                    "paper-v4/experiment-v4/run-09/results/native-query-binding.json"
                ),
                "sha256": _digest(EXECUTED_BINDING.read_bytes()),
                "schema": executed["schema"],
            },
            "query_result": {
                "path": "private/paper-v4-v4-run-09/query/query-result.json",
                "sha256": _digest(QUERY_RESULT.read_bytes()),
                "visibility": "PRIVATE",
            },
            "review_record": {
                "path": "paper-v4/evaluation-v4/run-09/review-record.preliminary.md",
                "sha256": _digest(REVIEW_RECORD.read_bytes()),
                "status": "PRELIMINARY_NOT_RATIFIED",
            },
        },
        "questions": questions,
        "totals": totals,
        "non_claim": (
            "These are run-09's rows under run-14's rule, not run-14's rows. No"
            " producer has run at this cell's coordinate and no graph of its own"
            " exists. The labels are run-09's preliminary reviewers' and are not"
            " ratified. What the numbers bound is the review, not the result."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=OUTPUT, help="the record to write"
    )
    arguments = parser.parse_args(argv)
    try:
        record = validate()
    except (OSError, TypeError, ValueError) as error:
        print(
            f"offline-validation: {type(error).__name__}: {error}", file=sys.stderr
        )
        return 2
    arguments.output.write_bytes(
        json.dumps(record, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    )
    print(json.dumps(record["totals"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
