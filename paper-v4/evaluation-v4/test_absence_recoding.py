"""Guards for the derived absence recoding.

The file is a derivation, so the guard that matters is that it is still the
derivation: recomputing it from the frozen records, contracts, gaps, exports and
captures must reproduce the bytes on disk. The rest of the guards are the four
mechanical checks the proposal names, plus the one this task adds: no entry
reaches the file without an evidence pointer.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUTPUT = HERE / "absence-recoding-2026-09-12.json"

CONTRACT_FACTS = "https://malleus.dev/contract-facts/"


def _module(name: str):
    spec = importlib.util.spec_from_file_location(
        f"paper_v4_evaluation_v4_{name}", HERE / f"{name}.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


recoding = _module("absence_recoding")
review = _module("review")

DERIVED = recoding.build()
ON_DISK = json.loads(OUTPUT.read_bytes())


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def test_the_file_on_disk_is_what_the_script_derives() -> None:
    rendered = (
        json.dumps(DERIVED, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    )

    assert rendered == OUTPUT.read_bytes()


def test_every_entry_carries_an_evidence_pointer() -> None:
    for entry in ON_DISK["entries"]:
        where = f"{entry['cell']}/{entry['question_id']}/{entry['semantic']}"
        assert entry["evidence"], f"{where} carries no evidence pointer"
        for pointer in entry["evidence"]:
            assert pointer["file"], f"{where} carries a pointer with no file"
            assert pointer["sha256"].startswith("sha256:"), where
            assert pointer["kind"], f"{where} carries an untyped pointer"


def test_every_bound_input_still_has_the_digest_the_file_records() -> None:
    inputs = ON_DISK["inputs"]
    assert _digest((ROOT / inputs["review_protocol"]["path"]).read_bytes()) == (
        inputs["review_protocol"]["sha256"]
    )
    for cell in inputs["cells"].values():
        for bound in cell.values():
            assert _digest((ROOT / bound["path"]).read_bytes()) == bound["sha256"]


def test_every_pointer_names_a_file_the_inputs_bind() -> None:
    """A pointer to a file the artifact does not bind by digest is not evidence."""

    bound = {ON_DISK["inputs"]["review_protocol"]["path"]}
    for cell in ON_DISK["inputs"]["cells"].values():
        bound |= {item["path"] for item in cell.values()}

    for entry in ON_DISK["entries"]:
        for pointer in entry["evidence"]:
            assert pointer["file"] in bound, pointer["file"]


def test_the_entries_are_exactly_the_absences_the_records_carry() -> None:
    expected: list[tuple[str, str, str, str]] = []
    for name, paths in recoding.CELLS.items():
        record = review._markdown_record((ROOT / paths["record"]).read_bytes())
        questions = review._question_file((ROOT / paths["questions"]).read_bytes())
        controls = {item["id"] for item in questions if item.get("expected_outcome")}
        for question in record["questions"]:
            if question["question_id"] in controls:
                continue
            for item in question["coverage"]:
                if item["row_index"] is not None:
                    continue
                if item["absent_reason"] not in recoding.IN_SCOPE_REASONS:
                    continue
                expected.append(
                    (
                        name,
                        question["question_id"],
                        item["semantic"],
                        item["absent_reason"],
                    )
                )

    found = [
        (
            entry["cell"],
            entry["question_id"],
            entry["semantic"],
            entry["recorded_reason"],
        )
        for entry in ON_DISK["entries"]
    ]

    assert found == expected


def test_no_recorded_reason_is_changed() -> None:
    """The recoding reads the records; it never rewrites one."""

    for entry in ON_DISK["entries"]:
        assert entry["recorded_reason"] in recoding.IN_SCOPE_REASONS
        assert entry["derived_case"] in recoding.CASES


def test_every_withheld_statement_is_carried_forward_as_held_as_digest() -> None:
    for entry in ON_DISK["entries"]:
        if entry["recorded_reason"] != "WITHHELD_STATEMENT":
            continue
        assert entry["derived_case"] == "HELD_AS_DIGEST"
        assert entry["judgement"] == "RECORDED_CODE_CARRIED_FORWARD"
        kinds = {pointer["kind"] for pointer in entry["evidence"]}
        assert "DIGEST_BOUND_RECORDS" in kinds


def test_every_no_type_or_slot_entry_cites_a_declared_type_absent_gap() -> None:
    entries = [
        entry for entry in ON_DISK["entries"] if entry["derived_case"] == "NO_TYPE_OR_SLOT"
    ]
    assert entries

    for entry in entries:
        gap = next(
            pointer for pointer in entry["evidence"] if pointer["kind"] == "DECLARED_GAP"
        )
        assert gap["gap_kind"] == "TYPE_ABSENT"
        declared = json.loads((ROOT / gap["file"]).read_bytes())["gaps"]
        assert any(
            item["locator"] == gap["locator"] and item["kind"] == "TYPE_ABSENT"
            for item in declared
        )


def test_every_name_mismatch_entry_cites_a_slot_use_the_contract_declares() -> None:
    entries = [
        entry
        for entry in ON_DISK["entries"]
        if entry["derived_case"] == "SLOT_ENTITY_NAME_MISMATCH"
    ]
    assert entries

    for entry in entries:
        uses = [
            pointer
            for pointer in entry["evidence"]
            if pointer["kind"] == "CONTRACT_SLOT_USE"
        ]
        assert uses
        for use in uses:
            facts = json.loads((ROOT / use["file"]).read_bytes())["facts"]
            declared = {
                (fact["subject"], fact["predicate"], fact["object"]) for fact in facts
            }
            assert (
                use["node"],
                f"{CONTRACT_FACTS}onClass",
                use["on_class"],
            ) in declared
            assert (
                use["node"],
                f"{CONTRACT_FACTS}usesSlot",
                use["uses_slot"],
            ) in declared


def test_every_name_mismatch_entry_shows_the_rule_finding_no_form() -> None:
    for entry in ON_DISK["entries"]:
        if entry["derived_case"] != "SLOT_ENTITY_NAME_MISMATCH":
            continue
        rule = next(
            pointer
            for pointer in entry["evidence"]
            if pointer["kind"] == "SUBJECT_NAME_RULE"
        )
        assert rule["rule"] == recoding.SUBJECT_NAME_RULE
        assert rule["checks"]
        for check in rule["checks"]:
            assert check["occurs_as_word"] == []


def test_the_name_rule_is_cores_own_and_still_refuses_a_descriptive_name() -> None:
    """The check is the compiler's, so the claim it makes is the compiler's."""

    occurs = recoding._occurs_as_word

    assert occurs("RC2", "the R C 2 segment") is True
    assert occurs("MAR", "the events mark the axis") is False
    assert (
        occurs(
            "number of events well relocated and replacing the NonLinLoc"
            " locations in the final catalog",
            "As a result, 276 events were well relocated",
        )
        is False
    )


def test_a_reviewer_sourced_referent_is_marked_as_the_reviewers() -> None:
    for entry in ON_DISK["entries"]:
        if entry["derived_case"] != "SLOT_WITHOUT_ENTITY":
            continue
        assert entry["judgement"] == "THE_REVIEWER_S"
        kinds = {pointer["kind"] for pointer in entry["evidence"]}
        assert "REFERENT_FROM_REVIEWER_NOTE" in kinds
        assert "REFERENT_SCAN" in kinds


def test_every_undecided_entry_says_what_is_missing() -> None:
    undecided = [
        entry for entry in ON_DISK["entries"] if entry["derived_case"] == "UNDECIDED"
    ]
    assert undecided

    for entry in undecided:
        assert entry["undecided_reason"]
        assert entry["recorded_reason"] in recoding.IN_SCOPE_REASONS
    assert ON_DISK["summary"]["undecided"] == len(undecided)


def test_run_25_is_recoded_against_the_contract_it_shares_with_run_23() -> None:
    cells = ON_DISK["inputs"]["cells"]

    assert cells["run-25"]["validated_contract"]["same_contract_as"] == "run-23"
    assert (
        cells["run-25"]["validated_contract"]["sha256"]
        == cells["run-23"]["validated_contract"]["sha256"]
    )


def test_the_artifact_says_it_is_not_review_evidence() -> None:
    assert ON_DISK["status"] == "DERIVED_ARTIFACT_NOT_REVIEW_EVIDENCE"
    assert "only a human-ratified record is paper evidence" in ON_DISK["is_not"]


def test_the_summary_counts_what_the_entries_carry() -> None:
    counted: dict[str, dict[str, int]] = {}
    for entry in ON_DISK["entries"]:
        counted.setdefault(entry["cell"], {})
        counted[entry["cell"]][entry["derived_case"]] = (
            counted[entry["cell"]].get(entry["derived_case"], 0) + 1
        )

    assert ON_DISK["summary"]["by_cell_and_case"] == counted
    assert ON_DISK["summary"]["entries"] == len(ON_DISK["entries"])


def test_an_entry_without_evidence_is_refused() -> None:
    """The refusal the task asks for, exercised rather than asserted."""

    cell = recoding.Cell("run-23", recoding.CELLS["run-23"])
    item = next(
        found
        for found in recoding._coverage_in_scope(cell)
        if found["entry"]["absent_reason"] == "WITHHELD_STATEMENT"
    )
    original = recoding._held_as_digest

    def _empty(*arguments: object, **keywords: object) -> dict[str, object]:
        return {
            "derived_case": "HELD_AS_DIGEST",
            "judgement": "RECORDED_CODE_CARRIED_FORWARD",
            "undecided_reason": None,
            "evidence": [],
        }

    recoding._held_as_digest = _empty  # type: ignore[assignment]
    try:
        with pytest.raises(recoding.RecodingRefusal, match="no evidence pointer"):
            recoding._derive(cell, item)
    finally:
        recoding._held_as_digest = original  # type: ignore[assignment]


def test_the_active_gate_collects_this_guard() -> None:
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())

    assert "paper-v4/evaluation-v4" in manifest["paths"]
