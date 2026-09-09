"""The active-test runner materialises each declared Core pin from git history.

A frozen paper run replays only against the Core commit it was produced with
(answer-demonstration/pilot.py verify_runtime). The manifest therefore names
that commit per path group, and the runner exports ``src/malleus`` at that
commit from the repository's own history into a temporary directory placed
first on PYTHONPATH. No copy of Core is tracked twice and no path outside the
repository is an input to the gate.
"""
from __future__ import annotations

from hashlib import sha1
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "paper-v4"))

import run_active_tests as runner  # noqa: E402

MANIFEST = json.loads((ROOT / "paper-v4" / "active-test-manifest.json").read_bytes())


def test_manifest_declares_the_answer_demonstration_core_pin() -> None:
    pins = MANIFEST["core_pins"]
    assert len(pins) == 1
    pin = pins[0]
    assert pin["commit"] == "160878cf14c0d27b11a440e26688708e9b7a7e2b"
    assert pin["pythonpath"] == ["paper-v4/answer-demonstration"]
    assert set(pin["paths"]) == {
        "paper-v4/answer-demonstration",
        "paper-v4/submission-candidate/test_prepare.py",
    }
    assert set(pin["paths"]) <= set(MANIFEST["paths"])
    assert MANIFEST["pythonpath"] == [".", "src"]


def test_export_matches_the_pinned_git_tree_blob_for_blob() -> None:
    commit = MANIFEST["core_pins"][0]["commit"]
    with tempfile.TemporaryDirectory() as tmp:
        exported = runner.export_core(commit, Path(tmp))
        assert exported == Path(tmp) / "src"
        listing = subprocess.run(
            ["git", "ls-tree", "-r", commit, "src/malleus"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.splitlines()
        assert listing
        for line in listing:
            entry, name = line.split("\t")
            expected = entry.split()[2]
            data = (Path(tmp) / name).read_bytes()
            assert sha1(f"blob {len(data)}\0".encode() + data).hexdigest() == expected, name


def test_plan_partitions_pinned_paths_and_orders_the_pin_first() -> None:
    manifest, paths = runner.load_active_paths()
    plan = runner.plan(manifest, paths, export_root=Path("/exports"))
    assert [group["pin"] for group in plan] == [
        "160878cf14c0d27b11a440e26688708e9b7a7e2b",
        None,
    ]
    pinned, rest = plan
    assert set(pinned["paths"]) == set(manifest["core_pins"][0]["paths"])
    assert set(rest["paths"]) == set(paths) - set(pinned["paths"])
    assert pinned["pythonpath"][0] == str(Path("/exports") / pinned["pin"] / "src")
    assert pinned["pythonpath"][1] == str((ROOT / "paper-v4/answer-demonstration").resolve())
    assert pinned["pythonpath"][2:] == [str((ROOT / p).resolve()) for p in manifest["pythonpath"]]
    assert rest["pythonpath"] == [str((ROOT / p).resolve()) for p in manifest["pythonpath"]]


def test_a_pin_that_is_not_a_full_commit_identity_is_refused() -> None:
    manifest = json.loads(json.dumps(MANIFEST))
    manifest["core_pins"][0]["commit"] = "160878cf"
    try:
        runner.plan(manifest, manifest["paths"], export_root=Path("/exports"))
    except ValueError as error:
        assert "full commit identity" in str(error)
    else:
        raise AssertionError("short pin accepted")
