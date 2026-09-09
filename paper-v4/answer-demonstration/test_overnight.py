"""Report both frozen fixed-ontology captures without upgrading their claims."""

from collections import Counter
import json
from pathlib import Path
import re

import pytest

from followup import verify_materials


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private/paper-v4-answer-demonstration"
REPORT = Path(__file__).with_name("OVERNIGHT-RESULTS.md")


@pytest.mark.parametrize("run", ["overnight-sol-01", "overnight-sol-02"])
def test_report_matches_every_complete_review_and_exact_reexecution(run):
    root = PRIVATE / run
    manifest = json.loads((root / "manifest.json").read_bytes())
    verify_materials(root, manifest["materials"])
    result = json.loads((root / "attempt-01/run-result.json").read_bytes())
    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert result["replay_matches_preclose"] is True
    assert not any(result["forbidden_attempts"].values())
    review = json.loads(
        re.findall(
            r"```json\s*(.*?)\s*```",
            (root / "review-01/review-record.md").read_text(),
            re.S,
        )[0]
    )
    assert len(review["questions"]) == 30
    assert review["status"] == "PRELIMINARY_COMPLETE"
    assert review["ratification"]["disposition"] == "PENDING"
    counts = Counter(q["question_responsiveness"] for q in review["questions"])
    row = [
        run,
        result["graph"]["entities"],
        result["graph"]["relations"],
        counts["COVERED"],
        counts["PARTIAL"],
        counts["NONE"],
    ]
    assert "| " + " | ".join(map(str, row)) + " |" in REPORT.read_text()
    actual = {
        p.relative_to(root / "attempt-01"): p.read_bytes()
        for p in (root / "attempt-01").rglob("*")
        if p.is_file()
    }
    replayed = {
        p.relative_to(root / "reproduction-01"): p.read_bytes()
        for p in (root / "reproduction-01").rglob("*")
        if p.is_file()
    }
    assert actual == replayed


def test_packets_differ_only_in_administrative_identity_and_path():
    roots = [PRIVATE / name for name in ("overnight-sol-01", "overnight-sol-02")]
    manifests = [json.loads((root / "manifest.json").read_bytes()) for root in roots]
    for key in (
        "reading_sha256",
        "ontology_sha256",
        "source_closure_sha256",
        "core_commit",
        "query_binding_sha256",
        "producer_inputs",
    ):
        assert manifests[0][key] == manifests[1][key]
    materials = [
        {item["path"]: item["sha256"] for item in m["materials"]} for m in manifests
    ]
    assert materials[0].keys() == materials[1].keys()
    changed = {
        name for name in materials[0] if materials[0][name] != materials[1][name]
    }
    assert changed == {"producer-task.md", "producer/inputs/coordinates.json"}


def test_new_condition_does_not_become_model_ranking_or_typed_composition():
    report = REPORT.read_text()
    for phrase in (
        "COVERED is not typed graph composition",
        "not a model ranking",
        "HUMAN RATIFICATION PENDING",
        "original A/B totals remain unchanged",
    ):
        assert phrase in report
    manuscript = (ROOT / "paper-v4/manuscript-v4-working.md").read_text()
    assert "answer-demonstration/OVERNIGHT-RESULTS.md" in manuscript
