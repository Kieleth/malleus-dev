"""The bridge's contract: what a replay of a frozen cell must be observed to do.

Written before the replays ran. The load-bearing statement is the frozen
coordinate: replaying the seven cells against the Core they were admitted on
has to give back their own receipt, export and ledger, byte for byte. Until
that holds, a difference at the candidate coordinate says nothing about Core,
because it could be the harness. Nothing here states which cells the hardened
gate admits; that is the measurement.

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
        paper-v4/experiment-v4/bridge-01/test_bridge.py
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))

import bridge  # noqa: E402

# The leak ladder and the contract-artifact reader are fault-injection-01's,
# imported rather than rewritten.
sys.path.insert(0, str(ROOT / "paper-v4/experiment-v4/fault-injection-01"))
import test_faults  # noqa: E402
import verify  # noqa: E402


OUTCOMES = HERE / "outcomes.json"
RESULTS = HERE / "RESULTS.md"
FROZEN_CORE = "c95dba7b86bb61487bda9a52458e1ea47cce20ab"
CANDIDATE_CORE = "e7937b89"
PUBLIC_FILES = (
    "bridge.py",
    "replay.py",
    "test_bridge.py",
    "outcomes.json",
    "RESULTS.md",
)

# The two leaves a Core change is allowed to move without moving meaning: the
# digest of the five Core source files, and the digest of the evidence block
# that carries it.
PRODUCER_ONLY = list(verify.PRODUCER_ONLY_PATHS)
# The run products that carry the admitted state rather than its provenance.
SEMANTIC_PRODUCTS = ("export_records", "trace_summary", "population_plan", "census")


def _outcomes() -> dict[str, object]:
    if not OUTCOMES.exists():
        pytest.fail("outcomes.json is not written yet")
    return json.loads(OUTCOMES.read_bytes())


def _coordinate(label: str) -> dict[str, object]:
    return _outcomes()["coordinates"][label]


def _cells(label: str) -> list[dict[str, object]]:
    return _coordinate(label)["cells"]


def test_every_cell_resolves_its_own_closure_reading_and_population() -> None:
    for cell in bridge.CELLS:
        frozen = bridge.frozen_result(cell)
        closure = bridge.source_closure(cell)
        assert [locator for locator, _ in closure] == sorted(
            frozen["source_closure_sha256"]
        )
        for locator, path in closure:
            assert bridge.file_digest(path) == frozen["source_closure_sha256"][locator]
        assert bridge.file_digest(bridge.reading_path(cell)) == frozen["reading_sha256"]
        population = json.loads(bridge.population_path(cell).read_bytes())
        assert set(population) == bridge.POPULATION_FIELDS


def test_the_root_ontology_is_found_by_digest_and_is_not_one_hardcoded_path() -> None:
    """run-25 populated run-23's ontology from ``inputs/``, not from ``work/``."""

    resolved = {}
    for cell in bridge.CELLS:
        closure = dict(bridge.source_closure(cell))
        root = closure[bridge.ROOT_LOCATOR]
        resolved[cell] = root.relative_to(bridge.producer_root(cell)).as_posix()
    assert resolved["run-23"] == "work/ontology-attempt-01.yaml"
    assert resolved["run-25"] == "inputs/ontology-run-23.yaml"
    assert len(set(resolved.values())) == 2


def test_every_cell_carries_the_identifiers_its_own_ledger_registered() -> None:
    for cell in bridge.CELLS:
        found = bridge.identifiers(cell)
        frozen = bridge.frozen_result(cell)
        assert found["capture_id"] == frozen["capture"]["capture_id"]
        assert found["plan_id"] == frozen["plan"]["plan_id"]
        assert found["transaction_time"] == frozen["transaction_time"]
        assert found["actor_id"] == frozen["actor_id"]
        assert found["source_id"] and found["artifact_id"]


def test_the_recomputed_producer_digest_is_the_one_each_frozen_ledger_declares() -> (
    None
):
    declared = {
        bridge.declared_producer_digest(
            verify.contract_artifact(bridge.frozen_ledger(cell))
        )
        for cell in bridge.CELLS
    }
    assert len(declared) == 1, declared
    assert declared.pop() == _outcomes()["coordinates"]["FROZEN"]["producer_sha256"]


def test_the_frozen_coordinate_reproduces_every_cell_byte_for_byte() -> None:
    """The control. Without this the candidate column measures the harness."""

    coordinate = _coordinate("FROZEN")
    assert coordinate["core_commit"] == FROZEN_CORE
    cells = _cells("FROZEN")
    assert [item["cell"] for item in cells] == list(bridge.CELLS)
    for item in cells:
        assert item["outcome"] == "ADMITTED", (item["cell"], item["diagnostic"])
        assert item["contract_artifact_differences"] == [], item["cell"]
        for product, identical in sorted(item["byte_identical"].items()):
            assert identical is True, (item["cell"], product)


def test_every_cell_has_a_candidate_outcome_against_the_hardened_core() -> None:
    coordinate = _coordinate("CANDIDATE")
    assert coordinate["core_commit"].startswith(CANDIDATE_CORE)
    assert coordinate["producer_sha256"] != _coordinate("FROZEN")["producer_sha256"]
    cells = _cells("CANDIDATE")
    assert [item["cell"] for item in cells] == list(bridge.CELLS)
    for item in cells:
        assert item["outcome"] in {"ADMITTED", "REFUSED"}, item["cell"]
        assert (item["outcome"] == "REFUSED") is (item["exit_status"] != 0)


def test_an_admitted_cell_keeps_its_meaning_and_moves_only_the_producer_digest() -> (
    None
):
    """An admission that changed an exported record is a difference, not a pass."""

    admitted = [item for item in _cells("CANDIDATE") if item["outcome"] == "ADMITTED"]
    assert admitted
    for item in admitted:
        for product in SEMANTIC_PRODUCTS:
            assert item["byte_identical"][product] is True, (item["cell"], product)
        paths = [entry["path"] for entry in item["contract_artifact_differences"]]
        assert paths == PRODUCER_ONLY, (item["cell"], paths)
        assert (
            item["declared_producer_sha256"]
            == (_coordinate("CANDIDATE")["producer_sha256"])
        )


def test_a_refused_cell_names_a_typed_reason_and_records_of_its_own_population() -> (
    None
):
    for item in _cells("CANDIDATE"):
        if item["outcome"] != "REFUSED":
            continue
        assert item["diagnostic"]["reason"], item["cell"]
        assert item["records_named"], item["cell"]
        population = json.loads(bridge.population_path(item["cell"]).read_bytes())
        known = {
            record["id"]
            for family in population["records"].values()
            for record in family
        }
        for record_id in item["records_named"]:
            assert record_id in known, (item["cell"], record_id)
        assert item["byte_identical"]["replay_receipt"] is False, item["cell"]


def test_the_source_binding_gate_is_live_on_this_path_and_was_not_before() -> None:
    """Seven admissions are only a finding if the new gate can refuse at all.

    One record keeps its ``assertion_locator`` and loses its
    ``statement_sha256``. Both slots are optional on the frozen Core, so the
    same file is admitted there and must be refused here, naming that record.
    """

    frozen = _coordinate("FROZEN")["probe"]
    candidate = _coordinate("CANDIDATE")["probe"]
    assert frozen["record_id"] == candidate["record_id"]
    assert frozen["population_sha256"] == candidate["population_sha256"]
    assert frozen["outcome"] == "ADMITTED", frozen["diagnostic"]
    assert candidate["outcome"] == "REFUSED"
    assert candidate["diagnostic"]["reason"] == "SOURCE_BINDING_REQUIRED"
    assert candidate["records_named"] == [candidate["record_id"]]
    assert "statement_sha256" in candidate["diagnostic"]["detail"]


def test_no_refusal_writes_an_admission_event() -> None:
    refused = [item for item in _cells("CANDIDATE") if item["outcome"] == "REFUSED"]
    for item in refused:
        assert item["ledger"]["admission_events"] == [], item["cell"]


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


def test_the_results_note_carries_both_coordinates_and_every_cell() -> None:
    text = RESULTS.read_text(encoding="utf-8")
    assert FROZEN_CORE in text
    assert CANDIDATE_CORE in text
    for cell in bridge.CELLS:
        assert cell in text, cell
    for label in ("FROZEN", "CANDIDATE"):
        assert str(_coordinate(label)["producer_sha256"]) in text, label
