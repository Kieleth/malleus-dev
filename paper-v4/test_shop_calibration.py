"""The Small Shop shipment-policy figures are read from a fresh run.

Section 3 used to print three separate fixtures and this file reran all three.
The connected history replaced the default-admission and partial-shipment rows,
so the calibration for those two rows went with them;
``paper-v4/test_shop_connected_calibration.py`` binds the chain that replaced
them. The shipment-policy fixture stayed in the manuscript as prose, because it
is the only Small Shop history in which a retained domain rule executes at
admission, and this file is what still binds the figures printed for it.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "paper-v4/manuscript-v4-working.md"
MODULE = "research.ontology_driven_kg_realization.experiments.small_shop"


def run_module(name, *args):
    env = {"PYTHONPATH": f"{ROOT}:{ROOT / 'src'}", "PATH": __import__("os").environ["PATH"]}
    completed = subprocess.run(
        [sys.executable, "-m", f"{MODULE}.{name}.run", *args],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr[-2000:]
    return completed.stdout


def exact_subset(selected, retained):
    if isinstance(selected, dict):
        for key, value in selected.items():
            assert key in retained, key
            exact_subset(value, retained[key])
    elif isinstance(selected, list):
        assert len(selected) == len(retained)
        for left, right in zip(selected, retained, strict=True):
            exact_subset(left, right)
    else:
        assert selected == retained


def appendix_b_exhibits():
    appendix = MANUSCRIPT.read_text().split("## Appendix B.", 1)[1]
    return [json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", appendix, re.S)]


@pytest.mark.skipif(shutil.which("swipl") is None, reason="SWI-Prolog is not on PATH")
def test_shipment_policy_figures_and_refusal_match_a_fresh_run(tmp_path):
    stdout = run_module("shipment_policy", "--history", str(tmp_path / "policy.jsonl"))
    report = json.loads(stdout[stdout.index("{") :])
    assert report["accepted_changes"] == 3 and report["event_count"] == 31
    refusal = report["duplicate_unit"]
    assert refusal["outcome"] == "VIOLATED" and refusal["ledger_unchanged"] is True
    assert len(refusal["violations"][0]["witness_record_ids"]) == 3
    prose = " ".join(MANUSCRIPT.read_text().split())
    assert "3 accepted changes and 31 ledger events" in prose
    assert "refused as VIOLATED with three witness records" in prose
    exact_subset(appendix_b_exhibits()[2], report)
