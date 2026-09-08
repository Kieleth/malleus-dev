"""Bind the new gate to actual current Core, preserving the old epoch guard."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CORE_COMMIT = "f99c886f939db95a003f6d30d2e73d3f2a341020"
CORE_SOURCE_TREE = "31e11514b1f999dd145724c3a0f9b7e95c126595"


def require_epoch(identity):
    if identity != CORE_SOURCE_TREE:
        raise ValueError("Unreviewed Core source epoch: " + identity)


def test_new_gate_pins_actual_core_and_preserves_historical_evidence():
    gate = json.loads((HERE / "observed-mismatch-gate.json").read_bytes())
    assert gate["runtime"]["core_commit"] == CORE_COMMIT
    assert gate["runtime"]["core_source_tree"] == CORE_SOURCE_TREE
    assert len(gate["tests"]) == len(set(gate["tests"]))
    assert str(Path(__file__).relative_to(ROOT)) in gate["tests"]
    for selector in gate["tests"]:
        assert (ROOT / selector.split("::")[0]).is_file()
    historical = gate["historical_epoch_guard"]
    assert historical["selector"] not in gate["tests"]
    assert (
        sha256((ROOT / historical["selector"].split("::")[0]).read_bytes()).hexdigest()
        == historical["source_sha256"]
    )
    for name, expected in (
        (
            "supplier-reentry-gate.json",
            "c55c0ef92a47204cb67e19593ca81a74a3397830d2f7afbda419afaaaf624585",
        ),
        (
            "current-core-landing-result.json",
            "a2907c4c8703fb764acf9ee95ac45ca03e3de70a699785b4451662c6fbe3922e",
        ),
    ):
        assert sha256((HERE / name).read_bytes()).hexdigest() == expected
    require_epoch(
        subprocess.check_output(
            ["git", "rev-parse", "HEAD:src"], cwd=ROOT, text=True
        ).strip()
    )
    subprocess.run(
        ["git", "diff", "--exit-code", CORE_COMMIT, "--", "src"],
        cwd=ROOT,
        check=True,
    )
    for name, module in tuple(sys.modules.items()):
        if name.split(".")[0] == "malleus" and getattr(module, "__file__", None):
            assert Path(module.__file__).resolve().is_relative_to(ROOT / "src/malleus")


@pytest.mark.parametrize(
    "identity", ["763d3b72ad2143bc5735eed32d47a69e3f6b8cd1", "unknown"]
)
def test_new_epoch_guard_rejects_older_and_unknown_source(identity):
    with pytest.raises(ValueError, match="Unreviewed Core source epoch"):
        require_epoch(identity)
