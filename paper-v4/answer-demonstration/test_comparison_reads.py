"""One frozen reader applied to distinct histories, never new model output."""

import json
from pathlib import Path
import subprocess
import sys


def test_comparison_reads_preserve_histories_and_current_answer_control():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_comparison_reads import check_reads; check_reads()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_reads():
    from tempfile import TemporaryDirectory
    from unittest.mock import patch
    import pytest
    import comparison_reads as reads
    from review_packet import digest

    with TemporaryDirectory(
        dir=reads.PRIVATE, prefix="comparison-read-test-"
    ) as directory:
        root = Path(directory)
        for name in reads.CASES:
            protected = (reads.CASES[name][0] / "ledger/history.jsonl").read_bytes()
            result = reads.execute(name, root / name)
            assert result["ledger_bytes_unchanged"]
            assert result["question_count"] == 30
            assert (
                reads.CASES[name][0] / "ledger/history.jsonl"
            ).read_bytes() == protected
            repeat = root / (name + "-repeat")
            reads.execute(name, repeat)
            assert {p.name: p.read_bytes() for p in (root / name).iterdir()} == {
                p.name: p.read_bytes() for p in repeat.iterdir()
            }
        new = json.loads((root / "repaired/query-result.json").read_bytes())["queries"]
        old = json.loads(
            (reads.PRIVATE / "duration-query-01/first/query-result.json").read_bytes()
        )["queries"]
        assert new == old
        case = reads.CASES["repaired"]
        with patch.dict(
            reads.CASES, {"repaired": (*case[:2], "sha256:" + "0" * 64, case[3])}
        ):
            with pytest.raises(ValueError):
                reads.execute("repaired", root / "bad")
        assert not (root / "bad").exists()
        with patch.dict(reads.CASES, {"repaired": (*case[:3], "sha256:" + "0" * 64)}):
            with pytest.raises(ValueError):
                reads.execute("repaired", root / "bad-surface")
        assert not (root / "bad-surface").exists()
        with pytest.raises(ValueError):
            reads.execute("unselected", root / "unselected")
        assert not (root / "unselected").exists()
        assert digest(protected).startswith("sha256:")
