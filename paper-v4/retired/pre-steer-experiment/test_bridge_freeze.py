from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HISTORICAL_RECEIPT = ROOT / "paper-v4/experiment/bridge-verification.json"
RECEIPT = ROOT / "paper-v4/experiment/bridge-verification-02.json"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_bridge_receipt_names_the_exact_verified_files_and_baseline() -> None:
    receipt = json.loads(RECEIPT.read_bytes())
    baseline = receipt["core_baseline"]
    implementation = receipt["implementation"]

    assert receipt["schema"] == "malleus.paper-v4.bridge-verification/v2"
    assert receipt["status"] == "FROZEN"
    assert receipt["supersedes"] == {
        "path": "paper-v4/experiment/bridge-verification.json",
        "sha256": _digest(HISTORICAL_RECEIPT),
        "reason": "STYLE_ONLY_BYTE_REBIND",
    }
    assert _digest(ROOT / baseline["manifest"]) == baseline["manifest_sha256"]
    assert (
        baseline["commit"]
        == json.loads((ROOT / baseline["manifest"]).read_bytes())["repository"][
            "commit"
        ]
    )
    for artifact in implementation.values():
        assert _digest(ROOT / artifact["path"]) == artifact["sha256"]
    verification = receipt["verification"]
    assert verification["command"] == [
        ".venv/bin/python",
        "-m",
        "pytest",
        "-q",
        "research/ontology_driven_kg_realization/experiments/document_paper/test_graph_recipe_change_set.py",
    ]
    assert verification["passed"] == verification["collected"] == 10
    assert verification["status"] == "PASS"
    assert "COMPONENT_BRIDGE_ONLY" in receipt["limits"]
    assert "NO_SAME_ONTOLOGY_CONTINUITY_EVIDENCE" in receipt["limits"]
    assert "NO_ACTUAL_PDF_DERIVED_GRAPH_YET" in receipt["limits"]
