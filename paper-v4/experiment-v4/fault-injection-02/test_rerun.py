"""The rerun's contract: the same catalog, a different Core, an honest control.

Written before the rerun landed. Nothing here says which faults the hardened
Core refuses; that is the measurement. What it does say is that the comparison
is legitimate: the same fifty-five constructions from the same seed, an honest
control that reproduces run-23's export on the new Core with only the producer
digest moved, and a table in RESULTS.md rendered from the two runs rather than
typed.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
        paper-v4/experiment-v4/fault-injection-02/test_rerun.py
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FIRST_CELL = ROOT / "paper-v4/experiment-v4/fault-injection-01"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(FIRST_CELL))

import compare  # noqa: E402
import faults  # noqa: E402
import run_faults  # noqa: E402
import test_faults  # noqa: E402
import verify  # noqa: E402


OUTCOMES = HERE / "outcomes.json"
RESULTS = HERE / "RESULTS.md"
FROZEN_CORE = "c95dba7b86bb61487bda9a52458e1ea47cce20ab"
CANDIDATE_CORE = "e7937b89"
FROZEN_EXPORT = (
    "sha256:0634e0696a34bc2cc736f84dbeadf6b65416ebcd9f84f0e67eeb11bb9a44a286"
)
PUBLIC_FILES = ("compare.py", "test_rerun.py", "outcomes.json", "RESULTS.md")


def _after() -> dict[str, object]:
    if not OUTCOMES.exists():
        pytest.fail("outcomes.json is not written yet")
    return json.loads(OUTCOMES.read_bytes())


def _before() -> dict[str, object]:
    return json.loads(compare.BEFORE.read_bytes())


def _trials() -> list[dict[str, object]]:
    return _after()["trials"]


def test_the_core_coordinate_is_an_argument_defaulting_to_the_frozen_pin() -> None:
    """The first cell keeps its coordinate by default; this one states its own."""

    minimal = ["--producer", "p", "--private", "q"]
    default = run_faults.build_parser().parse_args(minimal)
    assert default.core_commit == FROZEN_CORE
    assert default.core_repo == run_faults.CORE_REPOSITORY
    assert default.outcomes is None
    explicit = run_faults.build_parser().parse_args(
        minimal + ["--core-repo", "/elsewhere", "--core-commit", CANDIDATE_CORE]
    )
    assert explicit.core_commit == CANDIDATE_CORE
    assert str(explicit.core_repo) == "/elsewhere"


def test_the_rerun_is_the_same_catalog_at_a_different_core() -> None:
    before, after = _before(), _after()
    assert before["core_commit"] == FROZEN_CORE
    assert after["core_commit"].startswith(CANDIDATE_CORE)
    assert after["core_is_the_frozen_pin"] is False
    assert after["seed"] == before["seed"] == faults.SEED
    assert after["instances_per_variant"] == before["instances_per_variant"]
    assert [trial["trial_id"] for trial in after["trials"]] == [
        trial["trial_id"] for trial in before["trials"]
    ]
    assert [trial["population_sha256"] for trial in after["trials"]] == [
        trial["population_sha256"] for trial in before["trials"]
    ]
    assert len(after["trials"]) == 55


def test_the_control_reproduces_the_export_and_moves_only_the_producer_digest() -> None:
    control = _after()["control"]
    assert control["export_records_sha256"] == FROZEN_EXPORT
    assert control["export_equals_frozen_run_23"] is True
    assert control["equals_frozen_run_23"] is False
    differences = control["contract_differences_from_frozen_run_23"]
    assert [item["path"] for item in differences] == list(verify.PRODUCER_ONLY_PATHS)


def test_the_honest_run_still_reproduces_the_control_after_every_trial() -> None:
    replay = _after()["replay_after_trials"]
    assert replay["exit_status"] == 0
    assert replay["equals_control"] is True


def test_every_trial_lands_on_an_outcome_and_a_refusal_carries_its_reason() -> None:
    for trial in _trials():
        assert trial["outcome"] in {
            "REFUSED",
            "ADMITTED_EXPOSED",
            "ADMITTED_INVISIBLE",
        }, trial["trial_id"]
        refused = trial["outcome"] == "REFUSED"
        assert refused is (trial["exit_status"] != 0), trial["trial_id"]
        assert bool(trial["diagnostic"]["reason"]) is refused, trial["trial_id"]


def test_no_refusal_writes_an_admission_event() -> None:
    refused = [trial for trial in _trials() if trial["outcome"] == "REFUSED"]
    assert refused
    for trial in refused:
        assert trial["ledger"]["admission_events"] == [], trial["trial_id"]


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
        assert trial["run"]["receipt_equals_control"] is False, trial["trial_id"]


def test_an_invisible_admission_still_passes_every_check_a_reader_can_run() -> None:
    for trial in _trials():
        if trial["outcome"] != "ADMITTED_INVISIBLE":
            continue
        checks = trial["post_admission_checks"]
        assert checks["locator_disagreements"] == [], trial["trial_id"]
        assert checks["digest_disagreements"] == [], trial["trial_id"]


def test_the_side_by_side_table_in_results_is_the_one_compare_renders() -> None:
    rendered = compare.markdown(_before(), _after())
    printed = [
        line.strip()
        for line in RESULTS.read_text(encoding="utf-8").splitlines()
        if line.startswith("| ") and "`c95dba7b`" not in line
    ]
    body = [line for line in rendered if not line.startswith("| # ")]
    for line in body:
        assert line in printed, line
    assert set(compare.CONSTRUCTIONS) == {
        trial["fault_class"] for trial in _before()["trials"]
    }


def test_every_moved_trial_is_named_in_the_results_note() -> None:
    changed = compare.moved(_before(), _after())
    assert changed["other"] == []
    text = RESULTS.read_text(encoding="utf-8")
    for direction in ("admitted_to_refused", "refused_to_admitted"):
        assert str(len(changed[direction])) in text, direction
        for entry in changed[direction]:
            assert entry["trial_id"] in text, entry["trial_id"]


def test_nothing_public_reproduces_sixty_characters_of_the_reading() -> None:
    windows = test_faults._reading_windows(test_faults.LEAK_WINDOW)
    width = test_faults.LEAK_WINDOW
    for name in PUBLIC_FILES:
        path = HERE / name
        assert path.exists(), name
        plain = test_faults._plain(path.read_text(encoding="utf-8"))
        shared = [
            plain[start : start + width]
            for start in range(0, max(1, len(plain) - width + 1))
            if plain[start : start + width] in windows
        ]
        assert shared == [], name


def test_the_results_note_carries_both_coordinates_and_every_class() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert FROZEN_CORE in text
    assert _after()["core_commit"] in text
    for fault_class in compare.CONSTRUCTIONS:
        assert fault_class in text, fault_class
