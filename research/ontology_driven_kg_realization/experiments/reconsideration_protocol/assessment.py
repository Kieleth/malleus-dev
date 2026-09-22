"""The two mechanical halves of a review assessment that both consumers share.

Not the rulebook. The two protocol files that exist are different versions with
different sections and different check ids, and each validator reads its own;
that stays with the adapter. What is here is what both do identically:

``check_ratification`` is the clause a record cannot assert about itself. A
record that is not ratified carries ``PENDING``. A ratified or rejected record
carries every declared field, the status the record's own status implies, the
declared ratifier as its actor, and a ``record_sha256`` that is the digest of
the record **without** its ratification block, so ratifying cannot alter a
judgement.

``tally`` is the record's own arithmetic: one judgement per obligation, each
obligation judged once, every token declared, every locator present, no blank
rationale, no forbidden field, and counts that equal the judgements.

Neither chooses a judgement, changes one, or turns judgements into a rate.
"""

from __future__ import annotations

from .digests import canonical, digest


RATIFIED_STATUSES = {"HUMAN_RATIFIED": "RATIFIED", "HUMAN_REJECTED": "REJECTED"}
RATIFICATION_FIELDS = (
    "status",
    "actor_id",
    "at",
    "binding_file",
    "binding_file_sha256",
    "record_sha256",
    "scope",
)


class AssessmentRefusal(ValueError):
    """The protocol, the containment or the record does not hold."""


def check_ratification(record, *, ratifier, fields=RATIFICATION_FIELDS, prefix=""):
    """A ratification a record cannot assert about itself.

    ``prefix`` is the check id a consumer's refusals carry, if its rulebook
    numbers them.
    """
    block = record["ratification"]
    if not isinstance(block, dict):
        raise AssessmentRefusal(f"{prefix}the ratification block is not an object")
    expected = RATIFIED_STATUSES.get(record["status"])
    if expected is None:
        if block.get("status") != "PENDING":
            raise AssessmentRefusal(
                f"{prefix}a {record['status']} record requires ratification status"
                " PENDING"
            )
        return "PENDING"
    for field in fields:
        if not block.get(field):
            raise AssessmentRefusal(
                f"{prefix}a {record['status']} record requires ratification {field}"
            )
    if block["status"] != expected:
        raise AssessmentRefusal(
            f"{prefix}a {record['status']} record requires ratification status"
            f" {expected}"
        )
    if block["actor_id"] != ratifier:
        raise AssessmentRefusal(
            f"{prefix}the ratifier is {ratifier}; this names {block['actor_id']}"
        )
    naked = {key: value for key, value in record.items() if key != "ratification"}
    if block["record_sha256"] != digest(canonical(naked)):
        raise AssessmentRefusal(
            f"{prefix}ratification record_sha256 is not the digest of this record"
            " without its ratification block; ratifying cannot alter a judgement"
        )
    return expected


def tally(
    record,
    *,
    obligation_keys,
    assessment_outcomes,
    producer_outcomes,
    outcome_counts,
    forbidden_fields=(),
):
    """The record's judgements, counted, or a refusal naming what does not hold."""
    tokens = set(assessment_outcomes)
    outcomes = set(producer_outcomes)
    forbidden = set(forbidden_fields)
    seen, counts = set(), {name: 0 for name in outcome_counts}
    for entry in record["obligations"]:
        present = set(entry)
        if present & forbidden:
            raise AssessmentRefusal(
                "forbidden field in the record:"
                f" {', '.join(sorted(present & forbidden))}"
            )
        if present != set(obligation_keys):
            raise AssessmentRefusal(
                f"obligation keys are not {', '.join(obligation_keys)}"
            )
        if entry["obligation_id"] in seen:
            raise AssessmentRefusal(f"{entry['obligation_id']} is judged twice")
        seen.add(entry["obligation_id"])
        if entry["assessed_as"] not in tokens:
            raise AssessmentRefusal(
                f"{entry['obligation_id']}: unknown assessment outcome"
                f" {entry['assessed_as']}"
            )
        if entry["producer_outcome"] not in outcomes:
            raise AssessmentRefusal(
                f"{entry['obligation_id']}: unknown producer outcome"
                f" {entry['producer_outcome']}"
            )
        if not entry["source_locators"]:
            raise AssessmentRefusal(f"{entry['obligation_id']}: no source_locators")
        if not entry["rationale"].strip():
            raise AssessmentRefusal(f"{entry['obligation_id']}: blank rationale")
        counts[entry["assessed_as"]] += 1
    if record["counts"] != counts:
        raise AssessmentRefusal(
            f"the counts do not tally the judgements: {record['counts']} vs {counts}"
        )
    if sum(counts.values()) != len(record["obligations"]):
        raise AssessmentRefusal("the counts do not tally the judgements")
    return dict(counts), seen


def contained(workspace, forbidden, *, label="evaluator-only file"):
    """No forbidden file reached this directory, under any name.

    By name, by digest and by substring, which is what makes renaming one or
    pasting it into another file fail rather than pass.
    """
    from pathlib import Path

    workspace = Path(workspace)
    seen = 0
    for path in sorted(workspace.rglob("*")):
        if not path.is_file():
            continue
        seen += 1
        data = path.read_bytes()
        for name, content in forbidden.items():
            where = path.relative_to(workspace)
            if path.name == name:
                raise AssessmentRefusal(f"{where}: {label} {name}")
            if data == content:
                raise AssessmentRefusal(f"{where}: {label} {name}, renamed")
            if content in data:
                raise AssessmentRefusal(f"{where}: embeds {label} {name}")
    return {"status": "CONTAINED", "files": seen, "checked_against": sorted(forbidden)}
