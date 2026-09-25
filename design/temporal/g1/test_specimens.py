"""The G1 specimens pass their validator, and deliberately broken copies fail it."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("validate_specimens", HERE / "validate_specimens.py")
validator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validator)


def _errors(directory: Path) -> list[str]:
    results, dir_errors = validator.validate_dir(directory)
    return [e for errs in results.values() for e in errs] + dir_errors


def _copy_tree(tmp_path: Path) -> Path:
    """Copy the specimens and the reused answer key, keeping their relative layout."""
    shutil.copy(HERE.parent / "expected-views-v1.json", tmp_path / "expected-views-v1.json")
    target = tmp_path / "g1"
    target.mkdir()
    for path in HERE.glob("g1-*.json"):
        shutil.copy(path, target / path.name)
    return target


def _edit(directory: Path, name: str, change) -> None:
    path = directory / name
    data = json.loads(path.read_text(encoding="utf-8"))
    change(data)
    path.write_text(json.dumps(data), encoding="utf-8")


def _query(data: dict, qid: str) -> dict:
    return next(q for q in data["queries"] if q["id"] == qid)


def test_committed_specimens_pass():
    assert _errors(HERE) == []


def test_unbroken_copy_passes(tmp_path):
    assert _errors(_copy_tree(tmp_path)) == []


BROKEN = [
    pytest.param(
        "g1-01-price-history.json",
        lambda d: _query(d, "P02")["expected"].update(selected_refs=["c"]),
        "derived label 'c' starts after K1",
        id="future-closure-leak",
    ),
    pytest.param(
        "g1-01-price-history.json",
        lambda d: _query(d, "P04")["expected"]["value"].update(lexical="750"),
        "value_cents differs from ../expected-views-v1.json",
        id="copied-answer-drifts",
    ),
    pytest.param(
        "g1-02-order-premises.json",
        lambda d: d["objects"].append(dict(d["objects"][7])),
        "duplicate id 'A-price'",
        id="duplicate-assertion-id",
    ),
    pytest.param(
        "g1-03-competing-accounts.json",
        lambda d: _query(d, "CA01")["expected"].update(selected_refs=["Q9"]),
        "undefined id 'Q9'",
        id="undefined-reference",
    ),
    pytest.param(
        "g1-04-unknown-time-diameter.json",
        lambda d: _query(d, "S02")["inputs"].update(at="M9"),
        "'M9' is not a position of this specimen",
        id="unknown-position",
    ),
    pytest.param(
        "g1-05-conditional-statement.json",
        lambda d: _query(d, "CC06")["expected"].update(state="READY"),
        "expected answer needs a state from the allowed list",
        id="unknown-answer-state",
    ),
    pytest.param(
        "g1-08-storage-closure.json",
        lambda d: d["refusals"][0].update(head_after="R3"),
        "head_after must equal head",
        id="refusal-moves-head",
    ),
]


@pytest.mark.parametrize("name, change, message", BROKEN)
def test_broken_copy_fails(tmp_path, name, change, message):
    directory = _copy_tree(tmp_path)
    _edit(directory, name, change)
    errors = _errors(directory)
    assert any(message in e for e in errors), errors
