"""Put the two fault runs side by side, one row per construction.

The rows are rendered from the two ``outcomes.json`` files, never typed out, so
the table in ``RESULTS.md`` cannot drift from the runs it reports.
``test_rerun.py`` re-renders it and compares.

The construction column is the one thing here that is prose. Each line is the
construction ``fault-injection-01/RESULTS.md`` declares for that class,
shortened; the class names themselves come from the catalog.

    .venv/bin/python paper-v4/experiment-v4/fault-injection-02/compare.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BEFORE = ROOT / "paper-v4/experiment-v4/fault-injection-01/outcomes.json"
AFTER = HERE / "outcomes.json"

CONSTRUCTIONS = {
    "VALUE_NOT_IN_BLOCK": "one property value replaced; locator and digest untouched",
    "LOCATOR_REPOINTED_STALE_DIGEST": "locator moved, digest left behind",
    "LOCATOR_REPOINTED_COHERENT_DIGEST": "locator and digest moved, formalizations left",
    "LOCATOR_REPOINTED_COHERENT_DERIVATION": "locator, digest and formalizations moved together",
    "DIGEST_MISMATCH": "digest replaced with the digest of synthetic bytes",
    "DANGLING_ENDPOINT": "a relation endpoint pointed at an absent record",
    "TYPE_OUTSIDE_ONTOLOGY": "record type replaced with an undeclared type",
    "SLOT_OUTSIDE_ONTOLOGY": "an undeclared property added and cited",
    "DUPLICATE_RECORD_ID": "one record carried twice in its own family",
    "RECORD_WITH_NO_SOURCE_WITH_FIELDS": "a new record with one property and no source",
    "RECORD_WITH_NO_SOURCE_NO_FIELDS": "the same record carrying no property at all",
}
HEADER = (
    "| # | class | construction | n | on `c95dba7b` | on `e7937b89` |",
    "| :-- | :-- | :-- | --: | :-- | :-- |",
)


def outcomes(path: Path) -> dict[str, object]:
    return json.loads(path.read_bytes())


def _ordered_classes(run: dict[str, object]) -> list[str]:
    order: list[str] = []
    for trial in run["trials"]:
        if trial["fault_class"] not in order:
            order.append(str(trial["fault_class"]))
    return order


def _verdict(trials: list[dict[str, object]]) -> str:
    """One class's observed outcome, stated as the trials state it."""

    seen = sorted(
        {
            (
                str(trial["outcome"]),
                str(trial["diagnostic"]["reason"]),
            )
            for trial in trials
        }
    )
    return " / ".join(
        f"{outcome}, `{reason}`" if reason else outcome for outcome, reason in seen
    )


def rows(before: dict[str, object], after: dict[str, object]) -> list[list[str]]:
    found: list[list[str]] = []
    for index, fault_class in enumerate(_ordered_classes(before), start=1):
        own = {
            label: [
                trial for trial in run["trials"] if trial["fault_class"] == fault_class
            ]
            for label, run in (("before", before), ("after", after))
        }
        found.append(
            [
                str(index),
                f"`{fault_class}`",
                CONSTRUCTIONS[fault_class],
                str(len(own["before"])),
                _verdict(own["before"]),
                _verdict(own["after"]),
            ]
        )
    return found


def markdown(before: dict[str, object], after: dict[str, object]) -> list[str]:
    return list(HEADER) + ["| " + " | ".join(row) + " |" for row in rows(before, after)]


def moved(
    before: dict[str, object], after: dict[str, object]
) -> dict[str, list[dict[str, str]]]:
    """Every trial whose outcome changed, by direction."""

    first = {str(trial["trial_id"]): trial for trial in before["trials"]}
    second = {str(trial["trial_id"]): trial for trial in after["trials"]}
    changed: dict[str, list[dict[str, str]]] = {
        "admitted_to_refused": [],
        "refused_to_admitted": [],
        "other": [],
    }
    for trial_id in sorted(set(first) | set(second)):
        one, other = first.get(trial_id), second.get(trial_id)
        if one is None or other is None or one["outcome"] == other["outcome"]:
            continue
        entry = {
            "trial_id": trial_id,
            "fault_class": str(one["fault_class"]),
            "before": str(one["outcome"]),
            "after": str(other["outcome"]),
            "reason": str(other["diagnostic"]["reason"]),
        }
        if str(one["outcome"]).startswith("ADMITTED") and other["outcome"] == "REFUSED":
            changed["admitted_to_refused"].append(entry)
        elif one["outcome"] == "REFUSED" and str(other["outcome"]).startswith(
            "ADMITTED"
        ):
            changed["refused_to_admitted"].append(entry)
        else:
            changed["other"].append(entry)
    return changed


def main() -> int:
    before, after = outcomes(BEFORE), outcomes(AFTER)
    for line in markdown(before, after):
        print(line)
    print()
    for direction, entries in sorted(moved(before, after).items()):
        print(f"{direction}: {len(entries)}")
        for entry in entries:
            print(
                f"  {entry['trial_id']} {entry['fault_class']}"
                f" {entry['before']} -> {entry['after']} {entry['reason']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
