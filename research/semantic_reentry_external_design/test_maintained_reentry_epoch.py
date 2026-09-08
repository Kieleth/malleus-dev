"""One reviewed current-Core integration, with earlier evidence left intact."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CORE_COMMIT = "0af4364025a6fdff2b032e028d30e4d12ebf4289"
CORE_SOURCE_TREE = "156592a98156f51562eda5f8164cf02ed654a0f5"


def require_epoch(identity):
    if identity != CORE_SOURCE_TREE:
        raise ValueError("Unreviewed Core source epoch: " + identity)


def test_maintained_gate_pins_actual_core_and_preserves_prior_evidence():
    gate = json.loads((HERE / "maintained-integration-gate.json").read_bytes())
    assert gate["runtime"]["core_commit"] == CORE_COMMIT
    assert gate["runtime"]["core_source_tree"] == CORE_SOURCE_TREE
    selectors = gate["tests"]
    assert len(selectors) == len(set(selectors))
    assert str(Path(__file__).relative_to(ROOT)) in selectors
    assert "tests/contract_compiler/pareto/test_maintained_projection.py" in selectors
    for selector in selectors:
        assert (ROOT / selector.split("::")[0]).is_file()
    for historical in gate["historical_epoch_guards"]:
        assert historical["selector"] not in selectors
        path = ROOT / historical["selector"].split("::")[0]
        assert sha256(path.read_bytes()).hexdigest() == historical["source_sha256"]
    for historical in gate["historical_evidence"]:
        assert (
            sha256((HERE / historical["path"]).read_bytes()).hexdigest()
            == (historical["sha256"])
        )
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
    "identity",
    [
        "31e11514b1f999dd145724c3a0f9b7e95c126595",
        "763d3b72ad2143bc5735eed32d47a69e3f6b8cd1",
        "unknown",
    ],
)
def test_maintained_epoch_guard_rejects_older_and_unknown_source(identity):
    with pytest.raises(ValueError, match="Unreviewed Core source epoch"):
        require_epoch(identity)
