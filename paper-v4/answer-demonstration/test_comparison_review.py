"""Comparison packets preserve returned evidence and hide old judgments."""

import json
from pathlib import Path
import subprocess
import sys


def test_fresh_review_requires_delivered_reproduced_answers():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_fresh_comparison import check_stage; from test_comparison_review import check_fresh; check_stage(check_fresh)",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_fresh(run):
    from unittest.mock import patch
    import pytest
    import fresh_comparison as fresh
    import comparison_review as review
    from followup import verify_materials

    with patch.object(
        fresh, "verify_observed", side_effect=ValueError("incomplete delivery")
    ):
        with pytest.raises(ValueError, match="incomplete delivery"):
            review.prepare_fresh(run, run / "attempt-01", run / "undelivered-review")
    assert not (run / "undelivered-review").exists()
    with patch.object(fresh, "verify_observed", return_value={"fixture": True}):
        report = review.prepare_fresh(run, run / "attempt-01", run / "review")
        assert report["questions"] == 30
        manifest = json.loads((run / "review/manifest.json").read_bytes())
        verify_materials(run / "review", manifest["materials"])
        expected = json.loads((run / "attempt-01/query-result.json").read_bytes())[
            "queries"
        ]
        actual = json.loads((run / "review/query-result.json").read_bytes())["queries"]
        assert expected == actual
        with patch.object(review, "load_query", return_value={"queries": []}):
            with pytest.raises(ValueError, match="query"):
                review.prepare_fresh(run, run / "attempt-01", run / "bad-fresh")
        assert not (run / "bad-fresh").exists()
        raw = Path.read_bytes

        def wrong_repeat(path):
            if path == run / "reproduction-01/query-result.json":
                return b"changed"
            return raw(path)

        with patch.object(Path, "read_bytes", wrong_repeat):
            with pytest.raises(ValueError, match="reproduction"):
                review.prepare_fresh(run, run / "attempt-01", run / "bad-repeat")
        assert not (run / "bad-repeat").exists()


def test_reference_review_packets():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_comparison_review import check_packets; check_packets()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_packets():
    from tempfile import TemporaryDirectory
    from unittest.mock import patch
    import pytest
    import comparison_review as review
    import comparison_reads as reads
    from followup import verify_materials
    from review_packet import digest

    with TemporaryDirectory(
        dir=reads.PRIVATE, prefix="comparison-review-test-"
    ) as directory:
        root = Path(directory)
        for number, case in enumerate(reads.CASES):
            evidence = root / (case + "-read")
            reads.execute(case, evidence)
            target = root / str(number)
            report = review.prepare_reference(case, evidence, target)
            assert report["questions"] == 30
            manifest = json.loads((target / "manifest.json").read_bytes())
            verify_materials(target, manifest["materials"])
            expected = json.loads((evidence / "query-result.json").read_bytes())
            actual = json.loads((target / "query-result.json").read_bytes())
            assert actual == {"queries": expected["queries"]}
            assert (target / "review-docket.json").read_bytes() == (
                evidence / "review-docket.json"
            ).read_bytes()
            assert (
                len(
                    json.loads((target / "resolved-trace.json").read_bytes())["records"]
                )
                == report["traced_records"]
            )
            assert all(
                x["path"]
                not in {"review.json", "review.md", "summary.json", "run-result.json"}
                for x in manifest["materials"]
            )
            assert case not in json.dumps(manifest)
            assert "iteratively refined" not in (target / "TASK.md").read_text()
            assert (
                "Fixed interpretation before assessment"
                in (target / "review-criteria.md").read_text()
            )
            assert manifest["reviewer_mode"] == "FRESH_INDEPENDENT"
            repeat = root / (str(number) + "-repeat")
            review.prepare_reference(case, evidence, repeat)
            assert {p.name: p.read_bytes() for p in target.iterdir()} == {
                p.name: p.read_bytes() for p in repeat.iterdir()
            }
            wrong = expected.copy()
            wrong["queries"] = []
            with patch.object(review, "load_query", return_value=wrong):
                with pytest.raises(
                    ValueError, match="question order or closure differs"
                ):
                    review.prepare_reference(case, evidence, root / "bad-query")
            assert not (root / "bad-query").exists()
        with patch.object(review, "CRITERIA_ID", digest(b"wrong")):
            with pytest.raises(ValueError):
                review.prepare_reference("repaired", evidence, root / "bad-criteria")
        assert not (root / "bad-criteria").exists()
        with pytest.raises(ValueError):
            review.prepare_reference("unknown", evidence, root / "unknown")
        assert not (root / "unknown").exists()
