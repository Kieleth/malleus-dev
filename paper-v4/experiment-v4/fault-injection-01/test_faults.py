"""The fault-injection control's contract: what each class must be observed to do.

Written before the trials ran. Each class states the mechanism the frozen Core
declares for it and the outcome that mechanism implies; the run either meets
the statement or the statement was wrong about the code, which is the finding
the experiment is for. No test here adjusts an expectation to match a result.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q \
        paper-v4/experiment-v4/fault-injection-01/test_faults.py
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

import faults  # noqa: E402
import verify  # noqa: E402


OUTCOMES = HERE / "outcomes.json"
RESULTS = HERE / "RESULTS.md"
PRODUCER = ROOT / "private/paper-v4-v4-run-23/producer"
SELECTED_READING = PRODUCER / "inputs/selected-reading.json"
CORE_COMMIT = "c95dba7b86bb61487bda9a52458e1ea47cce20ab"
FROZEN_RECEIPT = (
    "sha256:a3abceec58dc93692cbdeabf9a95c03551177ba97d9ee4225fe29198f37f1eec"
)

# Nothing public may reproduce the reading. Sixty normalized characters is the
# threshold every file this cell writes clears, as in every other v4 cell.
LEAK_WINDOW = 60
PUBLIC_FILES = (
    "faults.py",
    "run_faults.py",
    "verify.py",
    "test_faults.py",
    "outcomes.json",
    "RESULTS.md",
)

# The outcome each class is expected to land on, and the mechanism the frozen
# Core declares for it. ``NONE_REVIEW_ONLY`` says no mechanism on the admission
# path reads the thing the fault changes.
EXPECTED = {
    "VALUE_NOT_IN_BLOCK": ("NONE_REVIEW_ONLY", "ADMITTED_INVISIBLE"),
    "LOCATOR_REPOINTED_STALE_DIGEST": ("DIGEST_BINDING", "REFUSED"),
    "LOCATOR_REPOINTED_COHERENT_DIGEST": ("TRACE_DERIVATION", "ADMITTED_EXPOSED"),
    "LOCATOR_REPOINTED_COHERENT_DERIVATION": (
        "NONE_REVIEW_ONLY",
        "ADMITTED_INVISIBLE",
    ),
    "DIGEST_MISMATCH": ("DIGEST_BINDING", "REFUSED"),
    "DANGLING_ENDPOINT": ("ADMISSION_STRUCTURAL_CHECK", "REFUSED"),
    "TYPE_OUTSIDE_ONTOLOGY": ("COMPILER", "REFUSED"),
    "SLOT_OUTSIDE_ONTOLOGY": ("COMPILER", "REFUSED"),
    "DUPLICATE_RECORD_ID": ("ADMISSION_STRUCTURAL_CHECK", "REFUSED"),
    "RECORD_WITH_NO_SOURCE_WITH_FIELDS": ("ADMISSION_STRUCTURAL_CHECK", "REFUSED"),
    "RECORD_WITH_NO_SOURCE_NO_FIELDS": ("NONE_REVIEW_ONLY", "ADMITTED_INVISIBLE"),
}
# The typed diagnostic each refusing class must carry. A refusal under some
# other reason is a different mechanism firing and fails the test.
EXPECTED_REASON = {
    "LOCATOR_REPOINTED_STALE_DIGEST": "DIGEST_MISMATCH",
    "DIGEST_MISMATCH": "DIGEST_MISMATCH",
    "DANGLING_ENDPOINT": "DANGLING_ENDPOINT",
    "TYPE_OUTSIDE_ONTOLOGY": "RECORDS_NOT_REHYDRATABLE",
    "SLOT_OUTSIDE_ONTOLOGY": "RECORDS_NOT_REHYDRATABLE",
    "DUPLICATE_RECORD_ID": "MALFORMED_CAPTURE",
    "RECORD_WITH_NO_SOURCE_WITH_FIELDS": "UNDERIVED_FIELD",
}


def _outcomes() -> dict[str, object]:
    if not OUTCOMES.exists():
        pytest.fail("outcomes.json is not written yet")
    return json.loads(OUTCOMES.read_bytes())


def _trials() -> list[dict[str, object]]:
    return _outcomes()["trials"]


def _by_class(fault_class: str) -> list[dict[str, object]]:
    return [item for item in _trials() if item["fault_class"] == fault_class]


def _plain(text: str) -> str:
    return " ".join(text.split())


def _reading_windows(width: int) -> set[str]:
    reading = json.loads(SELECTED_READING.read_bytes())
    windows: set[str] = set()
    for page in reading["pages"]:
        for block in page["blocks"]:
            plain = _plain(block["text"])
            for start in range(0, max(1, len(plain) - width + 1)):
                piece = plain[start : start + width]
                if len(piece) == width:
                    windows.add(piece)
    return windows


def test_the_catalog_is_deterministic_and_covers_every_declared_class() -> None:
    honest = json.loads((PRODUCER / "work/document-population.json").read_bytes())
    first = faults.catalog(honest)
    second = faults.catalog(honest)
    assert [item["trial_id"] for item in first] == [item["trial_id"] for item in second]
    assert [item["target"] for item in first] == [item["target"] for item in second]
    classes = {item["fault_class"] for item in first}
    assert classes == set(EXPECTED)
    assert set("abcdefg") == {item["letter"] for item in first}
    for fault_class in EXPECTED:
        assert (
            len([item for item in first if item["fault_class"] == fault_class])
            >= faults.INSTANCES_PER_VARIANT
        )


def test_every_injected_value_is_synthetic_and_not_read_from_the_source() -> None:
    honest = json.loads((PRODUCER / "work/document-population.json").read_bytes())
    windows = _reading_windows(LEAK_WINDOW)
    for trial in faults.catalog(honest):
        for value in trial["target"].values():
            if not isinstance(value, str):
                continue
            plain = _plain(value)
            shared = [
                plain[start : start + LEAK_WINDOW]
                for start in range(0, max(1, len(plain) - LEAK_WINDOW + 1))
                if plain[start : start + LEAK_WINDOW] in windows
            ]
            assert shared == [], trial["trial_id"]


def test_the_control_reproduces_run_23s_frozen_receipt() -> None:
    outcomes = _outcomes()
    assert outcomes["core_commit"] == CORE_COMMIT
    assert outcomes["control"]["replay_receipt_sha256"] == FROZEN_RECEIPT
    assert outcomes["control"]["equals_frozen_run_23"] is True


def test_the_honest_run_still_reproduces_the_receipt_after_every_trial() -> None:
    replay = _outcomes()["replay_after_trials"]
    assert replay["exit_status"] == 0
    assert replay["replay_receipt_sha256"] == FROZEN_RECEIPT


@pytest.mark.parametrize("fault_class", sorted(EXPECTED))
def test_each_fault_class_lands_on_its_declared_outcome(fault_class: str) -> None:
    catcher, outcome = EXPECTED[fault_class]
    trials = _by_class(fault_class)
    assert len(trials) >= faults.INSTANCES_PER_VARIANT
    for trial in trials:
        assert trial["designed_catcher"] == catcher, trial["trial_id"]
        assert trial["outcome"] == outcome, (
            trial["trial_id"],
            trial["outcome"],
            trial["diagnostic"]["reason"],
        )


@pytest.mark.parametrize("fault_class", sorted(EXPECTED_REASON))
def test_each_refused_class_carries_its_typed_diagnostic(fault_class: str) -> None:
    expected = EXPECTED_REASON[fault_class]
    for trial in _by_class(fault_class):
        assert trial["exit_status"] != 0, trial["trial_id"]
        assert trial["diagnostic"]["reason"] == expected, (
            trial["trial_id"],
            trial["diagnostic"]["reason"],
        )


def test_no_refusal_writes_an_admission_event() -> None:
    """A refused population leaves a history with no change set in it.

    The control's ledger carries fourteen events and its last four are the
    admission: the retained change set, the proposal, the check and the
    verdict. A refusal must carry none of the four, whatever it did to the
    retention that precedes them.
    """

    refused = [trial for trial in _trials() if trial["outcome"] == "REFUSED"]
    assert refused
    for trial in refused:
        assert trial["ledger"]["admission_events"] == [], trial["trial_id"]
        assert trial["ledger"]["event_count"] < 14, trial["trial_id"]


def test_a_refusal_whose_capture_is_untouched_leaves_the_control_ledgers_bytes() -> (
    None
):
    """A fault in the records alone must not move a byte of the retained history.

    A fault that rewrites the capture retains different evidence, so its
    ledger is a different history from the first event that names the capture;
    those trials are excluded here and reported by their event list instead.
    """

    capture_touched = {
        "LOCATOR_REPOINTED_COHERENT_DERIVATION",
        "SLOT_OUTSIDE_ONTOLOGY",
    }
    checked = 0
    for trial in _trials():
        if trial["outcome"] != "REFUSED" or trial["fault_class"] in capture_touched:
            continue
        assert trial["ledger"]["opens_the_control_ledger"] is True, trial["trial_id"]
        checked += 1
    assert checked > 0


def test_every_admission_carries_its_fault_into_the_exported_records() -> None:
    admitted = [
        trial for trial in _trials() if str(trial["outcome"]).startswith("ADMITTED")
    ]
    assert admitted
    for trial in admitted:
        assert trial["fault_in_export"]["present"] is True, trial["trial_id"]
        assert trial["run"]["reopen_matches_admitted"] == {
            "receipt": True,
            "export_records": True,
        }
        assert trial["run"]["receipt_equals_frozen"] is False, trial["trial_id"]


def test_an_exposed_admission_is_exposed_by_a_named_check() -> None:
    for trial in _trials():
        if trial["outcome"] != "ADMITTED_EXPOSED":
            continue
        checks = trial["post_admission_checks"]
        assert checks["locator_disagreements"] or checks["digest_disagreements"], trial[
            "trial_id"
        ]


def test_an_invisible_admission_passes_every_check_a_reader_can_run() -> None:
    for trial in _trials():
        if trial["outcome"] != "ADMITTED_INVISIBLE":
            continue
        checks = trial["post_admission_checks"]
        assert checks["locator_disagreements"] == [], trial["trial_id"]
        assert checks["digest_disagreements"] == [], trial["trial_id"]


def test_the_control_itself_passes_both_post_admission_checks() -> None:
    private = ROOT / "private/paper-v4-fault-injection-01/control/results"
    export = json.loads((private / "export-records.json").read_bytes())
    trace = json.loads((private / "trace-summary.json").read_bytes())
    capture = json.loads((PRODUCER / "work/document-population.json").read_bytes())[
        "capture"
    ]
    assert verify.locator_disagreements(export, trace) == []
    assert verify.digest_disagreements(export, capture) == []


def test_nothing_public_reproduces_sixty_characters_of_the_reading() -> None:
    windows = _reading_windows(LEAK_WINDOW)
    for name in PUBLIC_FILES:
        path = HERE / name
        assert path.exists(), name
        plain = _plain(path.read_text(encoding="utf-8"))
        shared = [
            plain[start : start + LEAK_WINDOW]
            for start in range(0, max(1, len(plain) - LEAK_WINDOW + 1))
            if plain[start : start + LEAK_WINDOW] in windows
        ]
        assert shared == [], name


def test_the_results_note_carries_the_classification_and_the_coordinate() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert CORE_COMMIT in text
    for fault_class in EXPECTED:
        assert fault_class in text, fault_class
