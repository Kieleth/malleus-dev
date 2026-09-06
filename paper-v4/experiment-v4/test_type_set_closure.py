from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SUBJECT_PATH = HERE / "type_set_closure.py"
SPEC = importlib.util.spec_from_file_location("paper_v4_type_set_closure", SUBJECT_PATH)
assert SPEC is not None and SPEC.loader is not None
SUBJECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SUBJECT)

RUN_21_FIRST_OMISSIONS = {
    "CQ-01": ["AnalyticalMethod"],
    "CQ-03": ["AnalyticalMethod"],
    "CQ-04": ["AnalyticalMethod"],
}


def _load(path: Path) -> dict:
    return json.loads(path.read_bytes())


def _cell(run: str) -> tuple[dict, dict]:
    ontology_run = HERE / run / "ontology-run"
    return (
        _load(ontology_run / "population-surface.json"),
        _load(ontology_run / "validated-contract.json"),
    )


def test_run_21_first_sets_listed_method_without_analytical_method() -> None:
    # The binding run-21 froze at acceptance; the executor refused it after
    # admission (E-0196). The check names the same omission before phase two.
    surface, contract = _cell("run-21")
    sets = _load(HERE / "run-21/results/query-type-sets.first.json")
    assert SUBJECT.omissions(surface, contract, sets) == RUN_21_FIRST_OMISSIONS


def test_run_21_amended_sets_are_closed() -> None:
    surface, contract = _cell("run-21")
    sets = _load(HERE / "run-21/results/query-type-sets.json")
    assert SUBJECT.omissions(surface, contract, sets) == {}


def test_run_20_sets_were_not_closed_per_question() -> None:
    # Run-20 listed Method in every set, GeophysicalModel only in CQ-03 and
    # CQ-04 and SoftwareTool only in CQ-01. The executor never refused,
    # because its projection map is binding-wide: a type named in any
    # question projects in every question. The reach was silent, and this
    # check names it per question, which is what the set claims to state.
    surface, contract = _cell("run-20")
    sets = _load(HERE / "run-20/results/query-type-sets.json")
    assert SUBJECT.omissions(surface, contract, sets) == {
        "CQ-01": ["GeophysicalModel"],
        "CQ-03": ["SoftwareTool"],
        "CQ-04": ["SoftwareTool"],
    }


def test_ancestry_is_read_from_the_contract_and_not_the_surface() -> None:
    # The surface carries no ancestry. With no subClassOf fact every set is
    # closed, which is the wrong answer for run-21 and proves where the
    # check looks.
    surface, _ = _cell("run-21")
    sets = _load(HERE / "run-21/results/query-type-sets.first.json")
    assert SUBJECT.omissions(surface, {"facts": []}, sets) == {}


def test_a_listed_type_absent_from_the_surface_is_refused_plainly() -> None:
    surface, contract = _cell("run-21")
    try:
        SUBJECT.omissions(surface, contract, {"CQ-01": ["SoftwareTool"]})
    except ValueError as error:
        assert "SoftwareTool" in str(error)
    else:
        raise AssertionError("a type the surface does not carry was accepted")


def test_cli_refuses_with_a_typed_reason_and_accepts_a_closed_set() -> None:
    ontology_run = HERE / "run-21/ontology-run"
    common = [
        sys.executable,
        str(SUBJECT_PATH),
        "--surface",
        str(ontology_run / "population-surface.json"),
        "--contract",
        str(ontology_run / "validated-contract.json"),
        "--type-sets",
    ]
    refused = subprocess.run(
        common + [str(HERE / "run-21/results/query-type-sets.first.json")],
        capture_output=True,
        text=True,
    )
    assert refused.returncode == 1
    assert json.loads(refused.stdout) == {
        "status": "REFUSED",
        "reason": "TYPE_SET_NOT_CLOSED_UNDER_SUBTYPES",
        "omissions": RUN_21_FIRST_OMISSIONS,
    }
    accepted = subprocess.run(
        common + [str(HERE / "run-21/results/query-type-sets.json")],
        capture_output=True,
        text=True,
    )
    assert accepted.returncode == 0
    assert json.loads(accepted.stdout) == {
        "status": "ACCEPTED",
        "reason": None,
        "omissions": {},
    }
