"""Fixed question and witness accounting, never automatic semantic grading."""

from copy import deepcopy
import pytest


def example():
    questions = {"questions": [{"id": "q1"}, {"id": "q2"}]}
    before = {
        "queries": [
            {"question_id": "q1", "rows": []},
            {"question_id": "q2", "rows": []},
        ]
    }
    after = deepcopy(before)
    after["queries"][0]["rows"] = [{"value": "synthetic"}]
    after["changed_question_ids"] = ["q1"]
    return questions, before, after, ["q1"]


def test_exact_changed_question_accounting_does_not_grade_answers():
    from reconciliation_query_review import changed_questions

    assert changed_questions(*example()) == ["q1"]


@pytest.mark.parametrize(
    "fault",
    ["missing", "order", "duplicate", "wrong_delta", "query_metadata", "unchanged"],
)
def test_query_review_refuses_question_or_change_misreporting(fault):
    from reconciliation_query_review import changed_questions

    questions, before, after, declared = example()
    if fault == "missing":
        after["queries"].pop()
    elif fault == "order":
        before["queries"].reverse()
    elif fault == "duplicate":
        questions["questions"][1]["id"] = "q1"
    elif fault == "wrong_delta":
        declared = ["q2"]
    elif fault == "query_metadata":
        after["changed_question_ids"] = ["q2"]
    else:
        after["queries"] = before["queries"]
    with pytest.raises(ValueError):
        changed_questions(questions, before, after, declared)


@pytest.mark.parametrize("status", [None, "REFUSED_OR_CHECK_FAILED"])
def test_no_query_review_packet_before_accepted_execution(
    tmp_path, monkeypatch, status
):
    import reconciliation_query_review as review
    from review_packet import canonical

    monkeypatch.setattr(review.pilot, "ROOT", tmp_path)
    monkeypatch.setattr(
        review.repair,
        "preflight",
        lambda _: ({"condition": "SOURCE_REVIEW_FEEDBACK_RECONCILIATION"}, None, []),
    )
    run = tmp_path / "private/run"
    attempt = run / "evidence/attempt-01"
    attempt.mkdir(parents=True)
    if status is not None:
        (attempt / "run-result.json").write_bytes(canonical({"status": status}))
    output = run / "query-review-01"
    with pytest.raises((FileNotFoundError, ValueError)):
        review.prepare(run, attempt, output)
    assert not output.exists()
