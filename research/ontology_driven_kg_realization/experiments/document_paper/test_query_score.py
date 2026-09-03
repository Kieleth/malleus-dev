"""Focused tests for strict paper-v4 query scoring."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json

import pytest

from malleus.ledger import canonical_json
from research.ontology_driven_kg_realization.experiments.document_paper.query_score import (
    CANDIDATE_SCHEMA,
    ORACLE_SCHEMA,
    QUERY_RESULT_SCHEMA,
    ScoringInputRefusal,
    candidate_from_query_result,
    score_query_result,
    write_score_result,
)


def _canonical(value: object) -> bytes:
    return canonical_json(value).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _row(index: int, *, name: str | None = None) -> dict[str, object]:
    return {
        "case_ordinal": 1,
        "source": {"name": name or f"Source {index}"},
        "relation": {"relation_type": "CONNECTS"},
        "target": {"name": "Target"},
        "witness": {
            "relation_id": f"relation:{index}",
            "source_id": f"source:{index}",
            "target_id": "target:1",
        },
    }


def _query_result() -> bytes:
    return _canonical(
        {
            "schema": QUERY_RESULT_SCHEMA,
            "inputs": {
                "ontology_sha256": "sha256:" + "1" * 64,
                "query_binding_sha256": "sha256:" + "2" * 64,
                "replay_receipt_sha256": "sha256:" + "3" * 64,
            },
            "graph_state_digest": "sha256:" + "4" * 64,
            "queries": [
                {
                    "query_id": f"NQ-CQ-0{index}",
                    "question_id": f"CQ-0{index}",
                    "rows": [_row(2), _row(1), _row(1)],
                }
                for index in range(1, 5)
            ],
            "forbidden_attempts": {
                "embedding_import": 0,
                "file_read": 0,
                "network": 0,
            },
        }
    )


def _oracle(candidate: dict[str, object]) -> bytes:
    return _canonical({"schema": ORACLE_SCHEMA, "candidate": candidate})


def test_exact_four_of_four_strips_witnesses_and_retains_duplicates() -> None:
    query_result = _query_result()
    candidate = candidate_from_query_result(query_result)
    assert candidate["schema"] == CANDIDATE_SCHEMA
    rows = candidate["questions"][0]["cases"][0]["rows"]
    assert len(rows) == 3
    assert rows[0] == rows[1]
    assert set(rows[0]) == {"source", "relation", "target"}

    oracle = _oracle(candidate)
    result = json.loads(score_query_result(query_result, oracle))
    assert result["status"] == "SCORED"
    assert result["score"] == {"exact_questions": 4, "total_questions": 4}
    assert result["inputs"] == {
        "oracle_sha256": _digest(oracle),
        "query_result_sha256": _digest(query_result),
    }


def test_one_question_mismatch_scores_three_of_four() -> None:
    query_result = _query_result()
    expected = deepcopy(candidate_from_query_result(query_result))
    expected["questions"][2]["cases"][0]["rows"][0]["source"]["name"] = "Other"

    result = json.loads(score_query_result(query_result, _oracle(expected)))
    assert result["score"] == {"exact_questions": 3, "total_questions": 4}
    assert [item["exact"] for item in result["questions"]] == [
        True,
        True,
        False,
        True,
    ]


def test_old_style_oracle_is_typed_unscorable() -> None:
    query_result = _query_result()
    old_oracle = (
        json.dumps(
            {
                "schema": "malleus.paper-v4.answer-oracle/v1",
                "answers": [
                    {"question_id": "CQ-01", "answer": {"prose": "not parsed"}}
                ],
            },
            indent=2,
        ).encode("utf-8")
        + b"\n"
    )

    result = json.loads(score_query_result(query_result, old_oracle))
    assert result == {
        "schema": "malleus.paper-v4.query-score/v1",
        "status": "UNSCORABLE_ORACLE_SCHEMA_MISMATCH",
        "inputs": {
            "oracle_sha256": _digest(old_oracle),
            "query_result_sha256": _digest(query_result),
        },
        "score": None,
        "questions": [],
    }


def test_malformed_candidate_raises_typed_refusal() -> None:
    query_result = json.loads(_query_result())
    del query_result["queries"][0]["rows"][0]["target"]

    with pytest.raises(ScoringInputRefusal, match="must contain exactly") as error:
        score_query_result(_canonical(query_result), _oracle({}))
    assert error.value.status == "SCORING_INPUT_REFUSAL"


def test_empty_answers_keep_bound_cases_and_forbidden_attempts_refuse() -> None:
    query_result = json.loads(_query_result())
    for query in query_result["queries"]:
        query["rows"] = []
    candidate = candidate_from_query_result(_canonical(query_result))
    assert [
        [case["case_ordinal"] for case in question["cases"]]
        for question in candidate["questions"]
    ] == [[1], [1], [1, 2], [1]]
    assert all(
        not case["rows"]
        for question in candidate["questions"]
        for case in question["cases"]
    )

    query_result["forbidden_attempts"]["file_read"] = 1
    with pytest.raises(ScoringInputRefusal, match="must be zero"):
        candidate_from_query_result(_canonical(query_result))


def test_score_writer_never_overwrites(tmp_path) -> None:
    output = tmp_path / "score.json"
    write_score_result(output, b"first")
    with pytest.raises(ScoringInputRefusal, match="already exists"):
        write_score_result(output, b"second")
    assert output.read_bytes() == b"first"
