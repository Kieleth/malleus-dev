"""Reading-quality screens must not turn quiet extraction into completeness."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

import reading_audit as audit


SOURCE = b"synthetic source identity"
EXPECT = {
    "source_sha256": sha256(SOURCE).hexdigest(),
    "page_count": 2,
    "probes": [
        {"id": "unit", "page": 1, "text": "M⊙"},
        {"id": "sign", "page": 2, "text": "−0.006"},
        {"id": "label", "page": 2, "text": "Peak periods"},
    ],
}
CANDIDATE = {
    "source_sha256": EXPECT["source_sha256"],
    "pages": [
        {"page": 1, "text": "Table: M⊙", "warnings": []},
        {"page": 2, "text": "Peak periods\n−0.006", "warnings": []},
    ],
}


def test_checks_pass_is_never_reading_approval():
    result = audit.check(CANDIDATE, EXPECT)
    assert result["status"] == "CHECKS_PASS_REVIEW_REQUIRED"
    assert result["launch_ready"] is False
    assert result["probes_passed"] == 3
    assert audit.check(CANDIDATE, EXPECT) == result


def test_private_use_math_glyph_is_review_needed_not_confirmed_loss():
    candidate = deepcopy(CANDIDATE)
    candidate["pages"][0]["text"] += "\uf8ee"
    result = audit.check(candidate, EXPECT)
    assert result["status"] == "REVIEW_REQUIRED"
    assert result["probes_passed"] == 3
    assert result["launch_ready"] is False


@pytest.mark.parametrize(
    "mutation",
    [
        lambda p: p[1].update(text="−0.006"),
        lambda p: p[1].update(text="Peak periods 0.006"),
        lambda p: p[0].update(text="Table: M"),
        lambda p: p[0].update(warnings=["content skipped"]),
        lambda p: p[1].update(text="Peak periods −0.006\x02"),
    ],
)
def test_known_content_loss_or_diagnostic_blocks_quiet_success(mutation):
    candidate = deepcopy(CANDIDATE)
    mutation(candidate["pages"])
    result = audit.check(candidate, EXPECT)
    assert result["status"] == "DEFECTS_FOUND"
    assert result["issues"]
    assert result["launch_ready"] is False


@pytest.mark.parametrize(
    "pages",
    [
        CANDIDATE["pages"][:1],
        [CANDIDATE["pages"][1], CANDIDATE["pages"][0]],
        [CANDIDATE["pages"][0], CANDIDATE["pages"][0]],
        [{"page": 1, "text": "", "warnings": []}, CANDIDATE["pages"][1]],
    ],
)
def test_missing_reordered_duplicate_or_empty_page_is_explicit(pages):
    candidate = {**CANDIDATE, "pages": pages}
    assert audit.check(candidate, EXPECT)["status"] == "DEFECTS_FOUND"


@pytest.mark.parametrize(
    "candidate,expect",
    [
        ({}, EXPECT),
        (CANDIDATE, {}),
        ({**CANDIDATE, "source_sha256": "0" * 64}, EXPECT),
        (CANDIDATE, {**EXPECT, "probes": []}),
        (CANDIDATE, {**EXPECT, "probes": [EXPECT["probes"][0]] * 2}),
        (CANDIDATE, {**EXPECT, "probes": [{"id": "outside", "page": 3, "text": "X"}]}),
    ],
)
def test_missing_or_unbound_audit_inputs_refuse(candidate, expect):
    with pytest.raises(audit.ReadingAuditRefusal):
        audit.check(candidate, expect)


def test_whitespace_matching_does_not_rewrite_retained_text_or_repair_symbols():
    candidate = deepcopy(CANDIDATE)
    candidate["pages"][0]["text"] = "Table: M ⊙"
    original = deepcopy(candidate)
    assert audit.check(candidate, EXPECT)["probes_passed"] == 3
    assert candidate == original


def test_report_write_is_complete_or_absent_and_never_overwrites(tmp_path, monkeypatch):
    from inspect_pdf_readings import publish_report

    path = tmp_path / "result.json"
    with monkeypatch.context() as patch:

        def fail_write(self, data):
            raise OSError("write failure")

        patch.setattr(Path, "write_bytes", fail_write)
        with pytest.raises(OSError):
            publish_report(path, b"{}")
    assert not path.exists()
    publish_report(path, b"{}")
    with pytest.raises(FileExistsError):
        publish_report(path, b"changed")
    assert path.read_bytes() == b"{}"


def test_retained_real_readings_preserve_the_distinct_loss_cases():
    root = Path(__file__).parent
    private = root.parents[1] / "private/paper-v4-exoplanets-lhs1140-01"
    data = (private / "reading-investigation-v2.json").read_bytes()
    assert (
        sha256(data).hexdigest()
        == "4a05200d6057932c8b1e7554a5a28de3ac3656676faa24ecac6859dff6d62eef"
    )
    report = json.loads(data)
    expected = json.loads((private / "reading-probes-v1.json").read_bytes())
    assert report["selected_reader"] is None
    assert len(report["cases"]) == 8
    assert sum(len(c["candidate"]["pages"]) for c in report["cases"]) == 212
    for case in report["cases"]:
        result = audit.check(case["candidate"], expected[case["source"]])
        assert result == case["assessment"]
        assert not result["launch_ready"]
        missing = {p["id"] for p in result["probes"] if not p["present"]}
        if case["source"] == "2010.06928v1.pdf":
            if case["method"].startswith("pypdf"):
                assert missing == {
                    "figure-5-negative-tick",
                    "figure-5-axis-label",
                    "figure-6-legend",
                    "figure-6-peak-label",
                }
                if case["method"] == "pypdf-layout":
                    assert case["candidate"]["pages"][5]["warnings"] == []
            else:
                assert missing == {"table-b3-solar-unit"}
        else:
            assert not missing
            assert {
                i["page"] for i in result["issues"] if i["kind"] == "CONTROL_CHARACTER"
            } == {19, 22, 23, 25}


def test_reclassification_did_not_change_any_extracted_page_or_warning():
    private = Path(__file__).parents[2] / "private/paper-v4-exoplanets-lhs1140-01"
    old = json.loads((private / "reading-investigation-v1.json").read_bytes())
    new = json.loads((private / "reading-investigation-v2.json").read_bytes())
    assert [(c["source"], c["method"], c["candidate"]) for c in old["cases"]] == [
        (c["source"], c["method"], c["candidate"]) for c in new["cases"]
    ]
