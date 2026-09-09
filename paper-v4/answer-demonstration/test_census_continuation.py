"""Census feedback must not become a question-conditioned producer packet."""

from pathlib import Path

import pytest


def test_feedback_packet_is_exact_and_question_free():
    from census_continuation import producer_files, check_producer_files

    base = (
        Path(__file__).resolve().parents[2]
        / "private/paper-v4-answer-demonstration/sol-e2e-corrected-01"
    )
    files = producer_files(base)
    check_producer_files(files)
    for extra in ("competency-questions.json", "query-result.json", "review-record.md"):
        with pytest.raises(ValueError, match="producer input closure"):
            check_producer_files({**files, extra: b"hidden"})
    missing = dict(files)
    del missing["feedback/census.json"]
    with pytest.raises(ValueError, match="producer input closure"):
        check_producer_files(missing)
    modified = dict(files)
    modified["TASK.md"] += b"\nReturn the expected answer."
    with pytest.raises(ValueError, match="feedback task differs"):
        check_producer_files(modified)


def test_feedback_has_one_pass_and_no_mandatory_relation_or_answer_value():
    from census_continuation import TASK

    wording = " ".join(TASK.split())
    assert "one whole-source pass" in wording
    assert "No minimum record or relation count" in wording
    assert "questions, query code, answers, scores or reviews" in wording
    assert "complete consolidated population" in wording
    assert "supersessions must be empty" in wording
    assert "CQ-" not in TASK
