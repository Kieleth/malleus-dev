"""The active paper gate must collect the answer harness in its declared mode."""

import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def test_answer_harness_is_part_of_the_active_paper_gate():
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())
    assert "paper-v4/answer-demonstration" in manifest["paths"]
    assert "--import-mode=importlib" in manifest["pytest_args"]


def test_isolated_gate_declares_its_private_fixture_inputs():
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())
    assert manifest["private_fixture_patterns"] == [
        "private/paper-v4-text-layer",
        "private/paper-v4-v4-run-*",
        "private/paper-v4-v4-shop-01",
        "private/paper-v4-answer-demonstration",
    ]
    assert manifest["private_fixture_excludes"] == ["*.pdf", "__pycache__/"]


def test_active_import_mode_collects_standalone_answer_modules():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--import-mode=importlib",
            "-q",
            "-p",
            "no:cacheprovider",
            str(HERE / "test_subject_answers.py"),
            "-k",
            "existing_subject_recovers",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
