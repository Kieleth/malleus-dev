"""Put the structural gate beside the structural gate plus the four rules.

The left column is ``fault-injection-02``: the same 55 faults on the hardened
Core with no rule layer, 45 refused and 10 admitted. The right column is this
cell: the same 55 faults, the same population bytes trial for trial, through
the same admission with the policy selected.

The rows are rendered from the two ``outcomes.json`` files, never typed out, so
the table in ``RESULTS.md`` cannot drift from the runs it reports.
``test_content_rules_doc_02.py`` re-renders it and compares.

Which rule refused which trial is read from each trial's own
``content-rule-violations.json``, written by ``admit.py`` beside that trial's
results. Only the rule, the violation code and the witness record identities
reach the public record.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
        paper-v4/experiment-v4/content-rules-doc-02/gate2.py \
        --private private/paper-v4-content-rules-doc-02
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper-v4/experiment-v4/fault-injection-02"))

import compare  # noqa: E402

BEFORE = ROOT / "paper-v4/experiment-v4/fault-injection-02/outcomes.json"
AFTER = HERE / "fault-outcomes.json"
OUTCOMES = HERE / "outcomes.json"

HEADER = (
    "| # | class | n | structural gate alone | structural gate plus the four rules |",
    "| :-- | :-- | --: | :-- | :-- |",
)


def markdown(before: dict, after: dict) -> list[str]:
    """The side-by-side, one row per construction, without the prose column."""

    rows = []
    for row in compare.rows(before, after):
        index, fault_class, _construction, count, left, right = row
        rows.append("| " + " | ".join([index, fault_class, count, left, right]) + " |")
    return list(HEADER) + rows


def rule_rows(after: dict, private: Path) -> dict[str, list[dict]]:
    """Per trial, what the rules said, from that trial's own written result."""

    found: dict[str, list[dict]] = {}
    for trial in after["trials"]:
        trial_id = str(trial["trial_id"])
        path = (
            private
            / "faults/trials"
            / trial_id
            / "results/content-rule-violations.json"
        )
        if not path.exists():
            continue
        detail = json.loads(path.read_bytes())
        found[trial_id] = detail["violations"]
    return found


def block(before: dict, after: dict, private: Path) -> dict:
    """The public gate-2 record: counts, movements and one row per violation."""

    rules = rule_rows(after, private)
    outcomes = {trial["trial_id"]: str(trial["outcome"]) for trial in after["trials"]}
    refused = [key for key, value in outcomes.items() if value == "REFUSED"]
    by_rule: dict[str, list[str]] = {}
    for trial_id, violations in sorted(rules.items()):
        for violation in violations:
            by_rule.setdefault(violation["rule_id"], []).append(trial_id)
    return {
        "runner": after["runner"],
        "core_commit": after["core_commit"],
        "refused": len(refused),
        "admitted": len(outcomes) - len(refused),
        "reached_the_rules": sorted(rules),
        "refused_by_a_rule": sorted(
            trial_id
            for trial_id, violations in rules.items()
            if violations and outcomes[trial_id] == "REFUSED"
        ),
        "trials_by_rule": {
            rule: sorted(set(trials)) for rule, trials in sorted(by_rule.items())
        },
        "violations": [
            {
                "trial_id": trial_id,
                "fault_class": next(
                    str(trial["fault_class"])
                    for trial in after["trials"]
                    if trial["trial_id"] == trial_id
                ),
                "rule_id": violation["rule_id"],
                "violation_code": violation["violation_code"],
                "slot": violation["violation_code"].split("/", 1)[-1]
                if "/" in violation["violation_code"]
                else None,
                "record_ids": violation["record_ids"],
            }
            for trial_id, violations in sorted(rules.items())
            for violation in violations
        ],
        "moved_against_the_structural_gate": compare.moved(before, after),
        "population_digests_match_the_first_cell": [
            trial["population_sha256"] for trial in after["trials"]
        ]
        == [trial["population_sha256"] for trial in before["trials"]],
        "table": markdown(before, after),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--private",
        default=ROOT / "private/paper-v4-content-rules-doc-02",
        type=Path,
    )
    arguments = parser.parse_args(argv)
    before = json.loads(BEFORE.read_bytes())
    after = json.loads(AFTER.read_bytes())
    found = block(before, after, arguments.private.resolve())
    for line in found["table"]:
        print(line)
    print()
    for direction, entries in sorted(
        found["moved_against_the_structural_gate"].items()
    ):
        print(f"{direction}: {len(entries)}")
        for entry in entries:
            print(
                f"  {entry['trial_id']} {entry['fault_class']}"
                f" {entry['before']} -> {entry['after']} {entry['reason']}"
            )
    print()
    for row in found["violations"]:
        print(
            f"  {row['trial_id']} {row['fault_class']} {row['rule_id']}"
            f" {row['violation_code']} {','.join(row['record_ids'])}"
        )
    existing = json.loads(OUTCOMES.read_bytes()) if OUTCOMES.exists() else {}
    existing["gate_2"] = found
    OUTCOMES.write_bytes(
        json.dumps(existing, ensure_ascii=False, indent=1, sort_keys=True).encode()
        + b"\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
