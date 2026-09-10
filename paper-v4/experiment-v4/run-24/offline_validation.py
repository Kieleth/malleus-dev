"""Validate the v4.4 restriction, the v4.9 removal and the two restorations.

The first two changes in the query surface are removals and the last two are
additions, and all four can be measured on one frozen record: expand run-09's frozen type sets against run-09's frozen surface
with this cell's rule, keep the cases the rule keeps, select the rows of run-09's
frozen query result that came from those cases, collapse the rows that repeat a
witness inside one question the way this cell's executor now does, and read the
labels off run-09's preliminary review record. Nothing is executed. No graph is
reopened, no query is run, no ontology is compiled and no model is called.

The carried stages are reported first and their counts must not move, because
neither the v4.4 rule nor the v4.9 removal moved under this cell. The third
stage is v4.12's own. Run-09 ran under the v3 binding, which emitted a plain
ENTITY case for every type in a question's set, so the rows an ENTITY_NO_SUBJECT
case returns are already in run-09's result: they are the rows of the ENTITY
case of a subject-bearing type whose projected record carries no subject. They
are counted here with the labels run-09's reviewers gave them, which is what the
addition brings back into reach and nothing more.

The fourth stage is v4.13's. A SUBJECT_ANY case returns the records of a listed
subject-bearing type whose subject resolves, whatever the subject's type, so its
counterpart in run-09's v3 record is the same ENTITY case read the other way:
its rows whose projected record does carry a subject. Beside that count is how
many of those records no typed SUBJECT case of the same question returned, which
is what widening the pairing reaches and nothing more.

Run-09 is frozen, so every one of its files is read and none is written. The
rows themselves stay where they are: this script writes counts, per question and
per label, and no row content, no record identifier and no reading text.

What it can establish: how many of run-09's rows the restriction keeps, how many
of those survive one row per witness per question, and what the reviewers already
said about exactly those rows. What it cannot: anything about run-24's own
producer, whose graph does not exist. A row count carried over from another
cell's graph is a bound on the review, not a result. A collapsed row's label is
the first producing row's, and the record counts separately how many of the
collapsed rows the reviewers had labelled otherwise.

    .venv/bin/python paper-v4/experiment-v4/run-24/offline_validation.py
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

RECORD_SCHEMA = "malleus.paper-v4.run-24-offline-validation/v3"
QUESTION_IDS = ("CQ-01", "CQ-02", "CQ-03", "CQ-04")
# v4.12's case kind. A v3 binding knows nothing of it, so its counterpart there
# is the ENTITY case of the same type and the rows it would return are that
# case's rows whose record carries no subject.
ENTITY_NO_SUBJECT = "ENTITY_NO_SUBJECT"
# v4.13's. A v3 binding knows nothing of it either, and its counterpart there is
# the same ENTITY case read the other way: the rows whose record does carry a
# subject, which a SUBJECT_ANY case returns whatever that subject's type is.
SUBJECT_ANY = "SUBJECT_ANY"

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
        "paper_v4_run_24_binder", HERE / "bind_from_surface.py"
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
    if kind == ENTITY_NO_SUBJECT:
        return (kind, str(case["record_type"]))
    if kind == SUBJECT_ANY:
        return (kind, str(case["record_type"]), str(case["subject_record_type"]))
    raise OfflineValidationRefusal(f"unknown case kind: {kind}")


def witness_identity(row: dict[str, object]) -> str:
    """A row's identity under the v4.9 removal: its kind and its record ids.

    ``record_id`` for an ENTITY row, ``record_id`` and ``subject_id`` for a
    SUBJECT row, ``relation_id`` with both endpoints for a RELATION row, which
    is exactly what the executor writes into ``witness``.
    """

    return json.dumps(
        [row["kind"], row["witness"]],
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


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
        "rows_one_per_witness": 0,
        "rows_re_projected": 0,
        "rows_re_projected_under_another_label": 0,
        "rows_restored_by_entity_no_subject": 0,
        "rows_restored_witnesses": 0,
        "rows_restored_new_witnesses": 0,
        "rows_reached_by_subject_any": 0,
        "rows_reached_by_subject_any_witnesses": 0,
        "rows_reached_by_subject_any_beyond_typed_subject": 0,
        "rows_reached_by_subject_any_beyond_typed_subject_witnesses": 0,
    }
    restored_by_label_total: dict[str, int] = {}
    reached_by_label_total: dict[str, int] = {}
    kept_by_kind: dict[str, int] = {}
    kept_by_label: dict[str, int] = {}
    one_by_kind: dict[str, int] = {}
    one_by_label: dict[str, int] = {}

    for question_id in QUESTION_IDS:
        types = sorted(set(type_sets[question_id]))
        bearing = [
            name
            for name in types
            if binder.SUBJECT_SLOT in binder._slot_names(by_name[name])
        ]
        expanded = binder._cases(
            types=types, relations=relations, by_name=by_name
        )
        restricted = [
            case
            for case in expanded
            if str(case["kind"]) not in {ENTITY_NO_SUBJECT, SUBJECT_ANY}
        ]
        restored_types = {
            str(case["record_type"])
            for case in expanded
            if str(case["kind"]) == ENTITY_NO_SUBJECT
        }
        reached_types = {
            str(case["record_type"])
            for case in expanded
            if str(case["kind"]) == SUBJECT_ANY
        }
        kept_identities = {case_identity(case) for case in restricted}
        frozen_cases = frozen[question_id]
        frozen_identities = {case_identity(case) for case in frozen_cases}
        if not kept_identities <= frozen_identities:
            raise OfflineValidationRefusal(
                f"the v4 expansion of {question_id} is not a subset of the v3 one"
            )
        if restored_types != set(bearing):
            raise OfflineValidationRefusal(
                f"the ENTITY_NO_SUBJECT cases of {question_id} do not cover its"
                " subject-bearing types"
            )
        if reached_types != set(bearing):
            raise OfflineValidationRefusal(
                f"the SUBJECT_ANY cases of {question_id} do not cover its"
                " subject-bearing types"
            )
        kept_ordinals = {
            int(case["ordinal"])
            for case in frozen_cases
            if case_identity(case) in kept_identities
        }
        # The v3 ENTITY case of each subject-bearing type. Its subject-less rows
        # are the ones v4.4 took out of reach and v4.12 gives back; its
        # subject-carrying rows are the ones a v4.13 SUBJECT_ANY case returns.
        restored_ordinals = {
            int(case["ordinal"])
            for case in frozen_cases
            if str(case["kind"]) == "ENTITY"
            and str(case["record_type"]) in restored_types
        }

        rows = rows_by_question[question_id]
        # The records the v3 SUBJECT cases of this question already returned. A
        # subject-carrying record of a listed bearing type that is not among
        # them is one the typed pairing lost and a SUBJECT_ANY case reaches.
        typed_subject_records = {
            str(row["witness"]["record_id"])
            for row in rows
            if str(row["kind"]) == "SUBJECT"
        }
        judged = labels[question_id]
        if sorted(judged) != list(range(len(rows))):
            raise OfflineValidationRefusal(
                f"the review record does not judge every row of {question_id}"
            )
        by_kind: dict[str, int] = {}
        by_label: dict[str, int] = {}
        single_kind: dict[str, int] = {}
        single_label: dict[str, int] = {}
        survivor_label: dict[str, str] = {}
        kept = 0
        relabelled = 0
        restored = 0
        restored_by_label: dict[str, int] = {}
        restored_witnesses: set[str] = set()
        reached = 0
        reached_by_label: dict[str, int] = {}
        reached_witnesses: set[str] = set()
        reached_beyond = 0
        reached_beyond_witnesses: set[str] = set()
        for index, row in enumerate(rows):
            ordinal = int(row["case_ordinal"])
            if (
                ordinal in restored_ordinals
                and row["record"].get(binder.SUBJECT_SLOT) is None
            ):
                restored += 1
                restored_by_label[judged[index]] = (
                    restored_by_label.get(judged[index], 0) + 1
                )
                restored_witnesses.add(witness_identity(row))
            if (
                ordinal in restored_ordinals
                and row["record"].get(binder.SUBJECT_SLOT) is not None
            ):
                record_id = str(row["witness"]["record_id"])
                reached += 1
                reached_by_label[judged[index]] = (
                    reached_by_label.get(judged[index], 0) + 1
                )
                reached_witnesses.add(record_id)
                if record_id not in typed_subject_records:
                    reached_beyond += 1
                    reached_beyond_witnesses.add(record_id)
            if ordinal not in kept_ordinals:
                continue
            kept += 1
            by_kind[str(row["kind"])] = by_kind.get(str(row["kind"]), 0) + 1
            label = judged[index]
            by_label[label] = by_label.get(label, 0) + 1
            witness = witness_identity(row)
            if witness in survivor_label:
                relabelled += int(survivor_label[witness] != label)
                continue
            survivor_label[witness] = label
            single_kind[str(row["kind"])] = single_kind.get(str(row["kind"]), 0) + 1
            single_label[label] = single_label.get(label, 0) + 1
        for source, target in (
            (by_kind, kept_by_kind),
            (by_label, kept_by_label),
            (single_kind, one_by_kind),
            (single_label, one_by_label),
        ):
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
                "rows_one_per_witness": len(survivor_label),
                "rows_re_projected": kept - len(survivor_label),
                "rows_one_per_witness_by_kind": dict(sorted(single_kind.items())),
                "rows_one_per_witness_by_label": dict(sorted(single_label.items())),
                "rows_re_projected_under_another_label": relabelled,
                "rows_restored_by_entity_no_subject": restored,
                "rows_restored_witnesses": len(restored_witnesses),
                "rows_restored_new_witnesses": len(
                    restored_witnesses - set(survivor_label)
                ),
                "rows_restored_by_label": dict(sorted(restored_by_label.items())),
                "rows_reached_by_subject_any": reached,
                "rows_reached_by_subject_any_witnesses": len(reached_witnesses),
                "rows_reached_by_subject_any_beyond_typed_subject": (
                    reached_beyond
                ),
                "rows_reached_by_subject_any_beyond_typed_subject_witnesses": (
                    len(reached_beyond_witnesses)
                ),
                "rows_reached_by_subject_any_by_label": dict(
                    sorted(reached_by_label.items())
                ),
            }
        )
        totals["cases_v3"] += len(frozen_cases)
        totals["cases_v4"] += len(restricted)
        totals["cases_removed"] += len(frozen_cases) - len(restricted)
        totals["rows_v3"] += len(rows)
        totals["rows_kept"] += kept
        totals["rows_removed"] += len(rows) - kept
        totals["rows_one_per_witness"] += len(survivor_label)
        totals["rows_re_projected"] += kept - len(survivor_label)
        totals["rows_re_projected_under_another_label"] += relabelled
        totals["rows_restored_by_entity_no_subject"] += restored
        totals["rows_restored_witnesses"] += len(restored_witnesses)
        totals["rows_restored_new_witnesses"] += len(
            restored_witnesses - set(survivor_label)
        )
        totals["rows_reached_by_subject_any"] += reached
        totals["rows_reached_by_subject_any_witnesses"] += len(reached_witnesses)
        totals["rows_reached_by_subject_any_beyond_typed_subject"] += (
            reached_beyond
        )
        totals[
            "rows_reached_by_subject_any_beyond_typed_subject_witnesses"
        ] += len(reached_beyond_witnesses)
        for name, count in restored_by_label.items():
            restored_by_label_total[name] = restored_by_label_total.get(name, 0) + count
        for name, count in reached_by_label.items():
            reached_by_label_total[name] = reached_by_label_total.get(name, 0) + count

    totals["rows_kept_by_kind"] = dict(sorted(kept_by_kind.items()))
    totals["rows_kept_by_label"] = dict(sorted(kept_by_label.items()))
    totals["rows_kept_unjudged"] = 0
    totals["rows_one_per_witness_by_kind"] = dict(sorted(one_by_kind.items()))
    totals["rows_one_per_witness_by_label"] = dict(sorted(one_by_label.items()))
    totals["rows_restored_by_label"] = dict(sorted(restored_by_label_total.items()))
    totals["rows_reached_by_subject_any_by_label"] = dict(
        sorted(reached_by_label_total.items())
    )

    return {
        "schema": RECORD_SCHEMA,
        "run_id": "run-24",
        "status": "COMPUTED",
        "change_id": "ENTITY_KIND_RESTRICTED",
        "rule": (
            "one ENTITY case per type in a question's set that carries no subject"
            " on the surface; SUBJECT and RELATION expansion unchanged"
        ),
        "and_change_id": "ONE_ROW_PER_WITNESS_OWN_TYPE_PROJECTION",
        "third_change_id": "ENTITY_NO_SUBJECT_REACHABILITY",
        "third_rule": (
            "one ENTITY_NO_SUBJECT case per subject-bearing type in a question's"
            " set, returning the records of that type whose subject slot is"
            " absent as ENTITY rows; measured here as the rows of run-09's v3"
            " ENTITY case of the same type whose record carries no subject"
        ),
        "fourth_change_id": "SUBJECT_ANY_REACHABILITY",
        "fourth_rule": (
            "one SUBJECT_ANY case per subject-bearing type in a question's set"
            " and every entity type the surface declares, returning the records"
            " of that type whose subject resolves whatever the subject's type"
            " is; measured here as the rows of run-09's v3 ENTITY case of the"
            " same type whose record does carry a subject, and beside them the"
            " ones no typed SUBJECT case of the same question returned"
        ),
        "and_rule": (
            "within one question, rows with the same witness are one row, the row"
            " projecting the fields of the witness record's own type; a collapsed"
            " row's label here is the first producing row's"
        ),
        "executes": "NOTHING",
        "measured_on": "run-09",
        "inputs": {
            "binder": {
                "path": "paper-v4/experiment-v4/run-24/bind_from_surface.py",
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
            "These are run-09's rows under run-24's rule, not run-24's rows. No"
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
