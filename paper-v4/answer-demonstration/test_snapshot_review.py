"""Snapshot accounting refuses drift; it never decides semantic support."""

from copy import deepcopy

import pytest


def fixture():
    docket = {
        "questions": [
            {
                "question_id": "q",
                "required_semantics": ["a", "b"],
                "rows": [{"kind": "ENTITY", "witness": {"record_id": "r"}}],
            }
        ],
        "witnesses": [{"witness_key": "r"}],
    }
    queries = {
        "queries": [
            {"question_id": "q", "rows": docket["questions"][0]["rows"], "paths": []}
        ]
    }
    record = {
        "schema": "malleus.paper-v4.current-snapshot-review/v1",
        "manifest_sha256": "identity",
        "status": "PRELIMINARY_COMPLETE",
        "ratification": "PENDING_HUMAN",
        "reviewer": {
            "actor_id": "actor:reviewer",
            "method": "MODEL_ASSISTED",
            "independence": "FRESH_INDEPENDENT",
            "completed_at": "2026-09-08T23:00:00Z",
        },
        "witnesses": [
            {
                "witness_key": "r",
                "source_support": "PARTIAL",
                "source_locators": ["block"],
                "rationale": "One field supported, another not.",
            }
        ],
        "questions": [
            {
                "question_id": "q",
                "responsiveness": "PARTIAL",
                "assembly": "ONE_ROW",
                "answer": "Only the supported field.",
                "coverage": [
                    {
                        "semantic": "a",
                        "row_indices": [0],
                        "path_indices": [],
                        "source_locators": ["block"],
                        "absent_reason": None,
                        "note": "The named returned field is supported.",
                    },
                    {
                        "semantic": "b",
                        "row_indices": [],
                        "path_indices": [],
                        "source_locators": ["block"],
                        "absent_reason": "UNRETURNED",
                        "note": "The requested content is not returned.",
                    },
                ],
            }
        ],
    }
    return docket, queries, record


def test_supported_field_is_not_lost_to_another_witness_omission():
    from snapshot_review import check_review

    docket, queries, record = fixture()
    assert check_review(record, docket, queries, {"block"}, "identity") == record


def test_runtime_pin_refusal_precedes_any_packet_write(tmp_path, monkeypatch):
    import pilot
    import repair
    from snapshot_review import prepare

    monkeypatch.setattr(pilot, "ROOT", tmp_path)

    def wrong_runtime(_):
        raise ValueError("Core runtime differs from frozen pin")

    monkeypatch.setattr(repair, "preflight", wrong_runtime)
    target = tmp_path / "private/review"
    with pytest.raises(ValueError, match="Core runtime differs"):
        prepare(tmp_path / "run", target, reviewer_mode="FRESH_INDEPENDENT")
    assert not target.exists()


def test_frozen_current_packet_preserves_exact_questions_answers_and_capture_scope():
    import json
    import pilot
    from review_packet import digest
    from snapshot_review import trace_closure

    root = pilot.ROOT / "private/paper-v4-answer-demonstration"
    packet = root / "current-thirty-review-01"
    run = root / "sol-reconciliation-feedback-01"
    manifest = json.loads((packet / "manifest.json").read_bytes())
    materials = {}
    for entry in manifest["materials"]:
        data = (packet / entry["path"]).read_bytes()
        assert digest(data) == entry["sha256"]
        materials[entry["path"]] = data
    assert not any(
        "prior-review" in name or "source-review" in name or "report" in name
        for name in materials
    )
    source_questions = json.loads((run / "questions.json").read_bytes())["questions"]
    index = json.loads(materials["review-docket.json"])
    assert len(index["questions"]) == 30
    for expected, question in zip(source_questions, index["questions"], strict=True):
        assert (
            expected["id"],
            expected["question"],
            expected["required_semantics"],
        ) == (
            question["question_id"],
            question["question"],
            question["required_semantics"],
        )
        assert "expected_outcome" not in question
    for name in (
        "query-result.json",
        "query-trace-summary.json",
        "export-records.json",
        "replay-receipt.json",
    ):
        assert materials[name] == (run / "evidence/attempt-01" / name).read_bytes()
    for name in (
        "answers.py",
        "subject_answers.py",
        "depth-method.json",
        "qualification-criteria.json",
    ):
        assert materials[name] == (run / name).read_bytes()
    captures = json.loads(materials["capture-catalog.json"])
    assert len(captures) == 6
    for name, identity in captures.items():
        assert digest(materials[name]) == identity
    assert trace_closure(
        materials["selected-reading.json"],
        {name: materials[name] for name in captures},
        json.loads(materials["query-trace-summary.json"]),
    ) == json.loads(materials["resolved-trace.json"])
    assert manifest["reproduced_queries_and_traces"] is True
    assert manifest["ledger_unchanged"] is True
    assert (
        digest((run / "evidence/attempt-01/ledger/history.jsonl").read_bytes())
        == manifest["ledger_sha256"]
    )
    assert manifest["ratification"] == "PENDING_HUMAN"


@pytest.mark.parametrize(
    "fault",
    [
        "missing_question",
        "duplicate_witness",
        "semantic_order",
        "boolean_row",
        "absent_row",
        "absent_path",
        "unknown_block",
        "false_total",
        "ratified",
        "identity",
        "no_reason",
        "unjustified_credit",
        "blank_rationale",
        "missing_actor",
    ],
)
def test_incomplete_or_unbound_assessment_refuses(fault):
    from snapshot_review import check_review

    docket, queries, record = fixture()
    record = deepcopy(record)
    q = record["questions"][0]
    if fault == "missing_question":
        record["questions"] = []
    elif fault == "duplicate_witness":
        record["witnesses"] *= 2
    elif fault == "semantic_order":
        q["coverage"].reverse()
    elif fault == "boolean_row":
        q["coverage"][0]["row_indices"] = [False]
    elif fault == "absent_row":
        q["coverage"][0]["row_indices"] = [1]
    elif fault == "absent_path":
        q["coverage"][0]["path_indices"] = [0]
    elif fault == "unknown_block":
        record["witnesses"][0]["source_locators"] = ["unknown"]
    elif fault == "false_total":
        q["responsiveness"] = "COVERED"
    elif fault == "ratified":
        record["ratification"] = "RATIFIED"
    elif fault == "identity":
        record["manifest_sha256"] = "other"
    elif fault == "no_reason":
        q["coverage"][1]["absent_reason"] = None
    elif fault == "unjustified_credit":
        q["coverage"][0]["row_indices"] = []
    elif fault == "blank_rationale":
        record["witnesses"][0]["rationale"] = ""
    else:
        del record["reviewer"]["actor_id"]
    with pytest.raises(ValueError):
        check_review(record, docket, queries, {"block"}, "identity")
