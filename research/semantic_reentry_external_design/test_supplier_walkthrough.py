"""The demonstration must execute without pytest or test-fixture imports."""

from importlib import import_module
import json
from pathlib import Path
import subprocess
import sys

import pytest

import malleus.compiler as core


MODULE = "research.semantic_reentry_external_design.supplier_walkthrough"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


@pytest.mark.parametrize("kind", ["directory", "file", "symlink", "dangling"])
def test_output_collision_refuses_before_compilation(tmp_path, monkeypatch, kind):
    demo = import_module(MODULE)
    target = tmp_path / "run"
    if kind == "directory":
        target.mkdir()
        (target / "evidence").write_bytes(b"keep")
    elif kind == "file":
        target.write_bytes(b"keep")
    else:
        destination = tmp_path / "destination"
        if kind == "symlink":
            destination.write_bytes(b"keep")
        target.symlink_to(destination)

    def forbidden(*args, **kwargs):
        pytest.fail("collision reached the compiler")

    monkeypatch.setattr(core, "compile_linkml_contract", forbidden)
    with pytest.raises(demo.WalkthroughError, match="OUTPUT_EXISTS"):
        demo.run(target)
    if kind == "directory":
        assert (target / "evidence").read_bytes() == b"keep"
    elif kind == "file":
        assert target.read_bytes() == b"keep"
    else:
        assert target.is_symlink()


def test_walkthrough_without_test_imports_executes_all_six_boundaries(tmp_path):
    target = tmp_path / "run"
    # Block test infrastructure and answer-key reads in the actual CLI process.
    program = """
import importlib.abc
from pathlib import Path
import runpy
import sys
class NoTestImports(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith(("pytest", "_pytest")) or any(
            part.startswith("test_") for part in fullname.split(".")
        ):
            raise AssertionError("test dependency: " + fullname)
sys.meta_path.insert(0, NoTestImports())
original_open = Path.open
def input_guard(path, *args, **kwargs):
    if "oracle" in path.parts or path.name == "supplier-order-history.jsonl":
        raise AssertionError("answer-key input: " + str(path))
    return original_open(path, *args, **kwargs)
Path.open = input_guard
sys.argv = [sys.argv[1], sys.argv[2]]
runpy.run_module(sys.argv[0], run_name="__main__")
"""
    completed = subprocess.run(
        [sys.executable, "-c", program, MODULE, str(target)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=1200,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    report = json.loads((target / "walkthrough.json").read_bytes())
    assert report["complete"] is True
    steps = report["checkpoints"]
    assert [step["stage"] for step in steps] == [
        "accepted_start",
        "proposal_only",
        "executed_not_observed",
        "observed_kcs_not_admitted",
        "admitted_and_replayed",
        "quiescent",
    ]
    assert [step["source_quantity"] for step in steps] == [1, 1, 2, 2, 2, 2]
    assert [step["accepted_quantity"] for step in steps] == [1, 1, 1, 1, 2, 2]
    assert len({step["graph_digest"] for step in steps[:4]}) == 1
    assert len({step["acceptance_head"] for step in steps[:4]}) == 1
    assert steps[0]["ledger_head"] == steps[1]["ledger_head"]
    assert steps[4]["ledger_head"] == steps[5]["ledger_head"]
    assert steps[1]["candidate_count"] == 1
    assert steps[1]["shortfall"] == 1
    assert steps[2]["execution_status"] == "SUCCEEDED"
    assert steps[3]["observation_result"] == "CONFIRMED"
    assert steps[5]["candidate_count"] == 0
    assert steps[5]["reentry_status"] == "SATISFIED"
    assert steps[5]["reentry_reason"] == "LINKED_OBSERVED_KCS"
    action = json.loads((target / "action-proposal.json").read_bytes())
    assert (action["expected_quantity"], action["requested_quantity"]) == (1, 2)
    change = core.KnowledgeChangeSet.from_bytes(
        (target / "observed-change-set.json").read_bytes()
    )
    ledger = (target / "history.jsonl").read_bytes()
    # Reopen only the ledger in a separate directory. Check the recorded prefix
    # before admission too, not just the presentation's claimed quantities.
    for index in (3, 5):
        path = tmp_path / f"reopen-{index}.jsonl"
        path.write_bytes(ledger[: steps[index]["ledger_byte_length"]])
        replay = core.KnowledgeChangeHistory.reopen(path).replay()
        assert replay.ledger_head == steps[index]["ledger_head"]
        assert replay.graph.state_digest() == steps[index]["graph_digest"]
        assert (change in replay.change_sets) == (index == 5)
        relation = replay.graph.export_records()["relations"][0]
        assert (relation["id"], relation["source_id"], relation["target_id"]) == (
            "contains:O1:X1",
            "O1",
            "X1",
        )
        for identifier in ("O1", "X1", "contains:O1:X1"):
            assert identifier in replay.record_history
    replacement = "supplier-order-state:B:reentry-amendment-1"
    assert (
        replay.record_history["supplier-order-state:B:e4"].superseded_by == replacement
    )
    trace = core.trace_population_record(replay, replacement)
    assert trace.sources[0].content == (target / "observed-source.jsonl").read_bytes()
    assert trace.sources[0].content == (target / "supplier.jsonl").read_bytes()
    assert (
        len(
            [
                value
                for value in replay.protocol_replay.data["records"].values()
                if value["record_type"] == "ActionDispatch"
            ]
        )
        == 1
    )
    assert "accepted=1" in completed.stdout and "accepted=2" in completed.stdout
    assert "quiescent" in completed.stdout


def test_walkthrough_guard_is_not_a_disableable_assertion():
    demo = import_module(MODULE)
    with pytest.raises(demo.WalkthroughError, match="CHECKPOINT_DISAGREEMENT"):
        demo.require(False, "checkpoint differs")
