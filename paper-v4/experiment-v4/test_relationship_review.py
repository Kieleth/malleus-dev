"""Review preparation preserves evidence identity and never supplies judgments."""

import importlib.util
import json
from collections import Counter
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def subject():
    spec = importlib.util.spec_from_file_location(
        "relationship_review", Path(__file__).with_name("relationship_review.py")
    )
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def test_witness_join_uses_ids_and_preserves_endpoint_evidence(subject):
    row = {
        "kind": "RELATION",
        "witness": {"relation_id": "r", "source_id": "a", "target_id": "b"},
        "relation": {"predicate": "SUPPORTS"},
    }
    query = {"queries": [{"question_id": "q", "rows": [row, row]}]}
    traces = {
        "records": [
            {"record_id": k, "derivations": [{"locator": "assertion:" + k}]}
            for k in ("b", "r", "a")
        ]
    }
    capture = {
        "assertions": [
            {"id": "assertion:" + k, "block": "block:" + k} for k in ("a", "b", "r")
        ]
    }
    result = subject.witness_inputs(query, traces, capture)
    assert len(result) == 1
    assert result[0]["witness_key"] == "r"
    assert set(result[0]["evidence_by_record"]) == {"a", "b", "r"}
    assert result[0]["evidence_by_record"]["r"][0]["block"] == "block:r"
    assert "source_support" not in result[0]
    del capture["assertions"][0]
    with pytest.raises(KeyError):
        subject.witness_inputs(query, traces, capture)


def test_changed_material_refuses(subject, tmp_path):
    p = tmp_path / "source.json"
    p.write_bytes(b"frozen")
    manifest = {
        "materials": [
            {"name": "source", "path": str(p), "sha256": subject.digest(p.read_bytes())}
        ]
    }
    assert subject.materials(manifest)["source"] == b"frozen"
    p.write_bytes(b"changed")
    with pytest.raises(ValueError, match="material"):
        subject.materials(manifest)


def test_question_group_order_is_not_row_order(subject):
    questions = [{"id": "T"}, {"id": "C"}]
    queries = [
        {"question_id": "C", "rows": [2, 1]},
        {"question_id": "T", "rows": [4, 3]},
    ]
    subject.check_question_ids(questions, queries)
    assert queries[0]["rows"] == [2, 1]
    with pytest.raises(ValueError):
        subject.check_question_ids(questions, queries[:1])
    with pytest.raises(ValueError):
        subject.check_question_ids(questions, queries + queries[:1])


def test_blank_review_uses_actual_validator_call_contract(subject):
    base = subject.ROOT / "paper-v4/evaluation-v4"
    result = subject.check_blank(
        (base / "run-26/review-record.blank.md").read_bytes(),
        (base / "review-protocol-v3.2.json").read_bytes(),
        (base / "run-26/review-input-manifest.json").read_bytes(),
    )
    assert result["status"] == "BLANK"


def test_review_can_read_complete_first_query_not_partial_files(subject, tmp_path):
    (tmp_path / "public").mkdir()
    (tmp_path / "query").mkdir()
    result = {
        "status": "ADMITTED_AND_REPLAYED",
        "ledger_head": "head",
        "replay_receipt_sha256": "receipt",
        "reopen_matches_admitted": {"receipt": True, "export_records": True},
    }
    (tmp_path / "public/run-result.json").write_text(json.dumps(result))
    (tmp_path / "query-binding.json").write_bytes(b"{}")
    query = {
        "inputs": {
            "ledger_head": "head",
            "replay_receipt_sha256": "receipt",
            "query_binding_sha256": subject.digest(b"{}"),
        },
        "forbidden_attempts": {"file_read": 0, "network": 0, "embedding_import": 0},
    }
    path = tmp_path / "query/query-result.json"
    path.write_text(json.dumps(query))
    with pytest.raises(FileNotFoundError):
        subject.checked_query(tmp_path)
    (tmp_path / "query/trace-summary.json").write_text('{"records":[]}')
    assert subject.checked_query(tmp_path) == (result, query)
    query["inputs"]["replay_receipt_sha256"] = "different"
    path.write_text(json.dumps(query))
    with pytest.raises(ValueError):
        subject.checked_query(tmp_path)


@pytest.mark.parametrize(
    "arm,attempt,witnesses,labels,elements",
    [
        ("a", 1, 216, {"COVERED": 7, "PARTIAL": 14, "NONE": 4}, 60),
        ("b", 3, 282, {"COVERED": 15, "PARTIAL": 8, "NONE": 2}, 78),
    ],
)
def test_reported_counts_come_from_complete_pending_human_reviews(
    subject, arm, attempt, witnesses, labels, elements
):
    packet = subject.PAIR / arm / "attempts" / f"attempt-{attempt:02d}" / "review"
    result = subject.validate(packet)
    assert (result["status"], result["witnesses"], result["questions"]) == (
        "PRELIMINARY_COMPLETE",
        witnesses,
        30,
    )
    validator = subject.module(
        subject.ROOT / "paper-v4/evaluation-v4/review.py", "contrast_review_checks"
    )
    record = validator._markdown_record(
        (packet / "output/review-record.preliminary.md").read_bytes()
    )
    assert record["ratification"]["disposition"] == "PENDING"
    positives = [q for q in record["questions"] if q["question_id"].startswith("CQ-T")]
    assert len(positives) == 25
    assert sum(len(q["coverage"]) for q in positives) == 102
    assert Counter(q["question_responsiveness"] for q in positives) == labels
    assert (
        sum(c["row_index"] is not None for q in positives for c in q["coverage"])
        == elements
    )


@pytest.mark.parametrize("arm,attempt", [("a", 1), ("b", 3)])
@pytest.mark.parametrize("defect", ["timestamp", "uncited_question"])
def test_full_parent_validator_refuses_review_handoff_defect_class(
    subject, tmp_path, arm, attempt, defect
):
    packet = subject.PAIR / arm / "attempts" / f"attempt-{attempt:02d}" / "review"
    for name in ("protocol.json", "review-input-manifest.json"):
        (tmp_path / name).write_bytes((packet / name).read_bytes())
    validator = subject.module(
        subject.ROOT / "paper-v4/evaluation-v4/review.py", "contrast_review_mutation"
    )
    record = validator._markdown_record(
        (packet / "output/review-record.preliminary.md").read_bytes()
    )
    if defect == "timestamp":
        record["preliminary"]["completed_at"] = "2026-09-15T00:00:00.123Z"
        expected = "RFC 3339 UTC second timestamp"
    else:
        record["questions"][0]["source_locators"] = []
        expected = "source_locators must cite the surface at least once"
    (tmp_path / "output").mkdir()
    (tmp_path / "output/review-record.preliminary.md").write_text(
        "```json\n" + json.dumps(record) + "\n```\n"
    )
    with pytest.raises(ValueError, match=expected):
        subject.validate(tmp_path)
