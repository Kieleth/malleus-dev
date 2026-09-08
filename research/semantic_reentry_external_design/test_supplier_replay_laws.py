"""Current-Core replay witness; historical runtime-bound evidence is immutable."""

import ast
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

import malleus.compiler as core
from research.semantic_reentry_external_design import (
    test_supplier_initial_source as ingress,
)


ROOT = Path(__file__).resolve().parents[2]
CORE_COMMIT = "90146c380994621a2f8df25876affd03fc9e57e3"
CORE_SOURCE_TREE = "763d3b72ad2143bc5735eed32d47a69e3f6b8cd1"
HISTORICAL = "research/semantic_reentry_external_design/test_replay_noninvertibility.py"
HISTORICAL_SHA256 = "8cd5eea6de67ca085cf2848820660809e40e70fbf276e44a65784e5e9d882200"

complement_owner = ingress.complement_owner
initial_inputs = ingress.initial_inputs


def require_compatible_epoch(source, expected):
    """Check the explicit CORE_COMMIT convention used by these witness modules."""
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "CORE_COMMIT"
            for target in node.targets
        ):
            actual = ast.literal_eval(node.value)
            if actual != expected:
                raise ValueError(
                    f"Incompatible Core epoch: {actual}; expected {expected}"
                )


def test_unified_gate_has_one_compatible_runtime_epoch():
    gate = json.loads(
        Path(__file__).with_name("supplier-reentry-gate.json").read_bytes()
    )
    for name in gate["tests"]:
        require_compatible_epoch((ROOT / name).read_bytes(), CORE_COMMIT)
    assert gate["runtime"]["core_commit"] == CORE_COMMIT
    assert gate["runtime"]["core_source_tree"] == CORE_SOURCE_TREE
    assert str(Path(__file__).relative_to(ROOT)) in gate["tests"]
    assert gate["historical_witnesses"] == [
        {
            "path": HISTORICAL,
            "core_commit": "2af45e03ee7d7bf528cef8db42c0798e6d99685b",
            "sha256": HISTORICAL_SHA256,
        }
    ]
    assert not set(gate["tests"]) & {
        entry["path"] for entry in gate["historical_witnesses"]
    }
    assert sha256((ROOT / HISTORICAL).read_bytes()).hexdigest() == HISTORICAL_SHA256
    assert (
        subprocess.check_output(
            ["git", "rev-parse", "HEAD:src"], cwd=ROOT, text=True
        ).strip()
        == CORE_SOURCE_TREE
    )
    subprocess.run(
        ["git", "diff", "--exit-code", CORE_COMMIT, "--", "src"],
        cwd=ROOT,
        check=True,
    )
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] == "malleus" and getattr(module, "__file__", None):
            assert Path(module.__file__).resolve().is_relative_to(ROOT / "src/malleus")


def test_epoch_guard_rejects_historical_and_unknown_pins():
    for source in (
        (ROOT / HISTORICAL).read_bytes(),
        b'CORE_COMMIT = "unreviewed-core"',
    ):
        with pytest.raises(ValueError, match="Incompatible Core epoch"):
            require_compatible_epoch(source, CORE_COMMIT)
    require_compatible_epoch(f'CORE_COMMIT = "{CORE_COMMIT}"', CORE_COMMIT)


def test_current_supplier_distinct_histories_same_graph(
    complement_owner, initial_inputs, tmp_path
):
    owner = complement_owner
    preparation = ingress.prepare_initial(owner, initial_inputs)
    initial = core.admit_structural_change(
        history=owner,
        preparation=preparation,
        transaction_time=ingress.TIME,
        actor_id=ingress.ACTOR,
    )
    short_directory = tmp_path / "short-jsonl-only"
    short_directory.mkdir()
    short_path = short_directory / "history.jsonl"
    shutil.copyfile(owner.path, short_path)
    prefix = short_path.read_bytes()
    note_id = "evidence:supplier:noninvertibility"
    note = ingress.canonical(
        {
            "classification": "CONFORMANCE_FIXTURE",
            "meaning": "Evidence-only witness, not an action or observed source",
        }
    )
    owner.append_anchors(
        anchors=(
            core.structural_evidence_anchor(
                record_id=note_id,
                content=note,
                media_type="application/json",
            ),
        ),
        transaction_time=ingress.TIME,
        actor_id=ingress.ACTOR,
    )
    long_directory = tmp_path / "long-jsonl-only"
    long_directory.mkdir()
    long_path = long_directory / "history.jsonl"
    shutil.copyfile(owner.path, long_path)
    extended = long_path.read_bytes()
    short = core.KnowledgeChangeHistory.reopen(short_path).replay()
    long = core.KnowledgeChangeHistory.reopen(long_path).replay()
    assert extended.startswith(prefix) and extended != prefix
    assert long.ledger_event_count == short.ledger_event_count + 1
    assert long.ledger_head != short.ledger_head
    assert long.receipt.identity != short.receipt.identity
    assert short.receipt == initial.receipt
    assert long.receipt == owner.replay().receipt
    assert (
        long.graph.export_records()
        == short.graph.export_records()
        == initial.graph.export_records()
    )
    assert long.graph.state_digest() == short.graph.state_digest()
    assert long.change_sets == short.change_sets == initial.change_sets
    assert long.record_history == short.record_history == initial.record_history
    assert long.partial_contract == short.partial_contract
    assert long.acceptance_head == short.acceptance_head
    assert long.materialization_head == short.materialization_head
    assert long.retained_bytes(ingress.SOURCE_ID) == initial_inputs["source_bytes"]
    assert long.retained_bytes(note_id) == note
    assert note_id not in {entry.record_id for entry in short.retained_inputs}
    assert set(long.record_history) == {
        "O1",
        "X1",
        "contains:O1:X1",
        "supplier-order-state:B:e4",
    }
    assert long.graph.get_node("supplier-order-state:B:e4")["ordered_quantity"] == 1
    for change in long.change_sets:
        assert core.KnowledgeChangeSet.from_bytes(change.canonical_bytes) == change
    for directory in (short_directory, long_directory):
        assert sorted(path.name for path in directory.iterdir()) == ["history.jsonl"]
    assert short_path.read_bytes() == prefix and long_path.read_bytes() == extended
