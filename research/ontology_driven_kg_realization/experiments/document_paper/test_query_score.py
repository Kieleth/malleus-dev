"""Focused tests for strict paper-v4 query scoring."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from malleus.ledger import canonical_json
from research.ontology_driven_kg_realization.experiments.document_paper import (
    query_score as subject,
)
from research.ontology_driven_kg_realization.experiments.document_paper.query_score import (
    CANDIDATE_SCHEMA,
    ORACLE_SCHEMA,
    QUERY_RESULT_SCHEMA,
    ScoringInputRefusal,
    candidate_from_query_result,
    main,
    score_query_result,
    write_score_result,
)


ONTOLOGY_DIGEST = "sha256:" + "1" * 64
ROOT = Path(__file__).resolve().parents[4]
RETIRED_V1_ORACLE_SHA256 = (
    "sha256:95b206a8a8eac20f208854c2374ed8433187402d9ab1e50771003e412066b571"
)
REBOUND_V2_ORACLE_SHA256 = (
    "sha256:6f1564887aa908ac2cd0ff9f06e823ccf936ca18d24595252a0c04a6c0cc09b4"
)


def _canonical(value: object) -> bytes:
    return canonical_json(value).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _binding() -> bytes:
    case = {
        "ordinal": 1,
        "source_record_type": "FictionalSource",
        "relation_record_type": "FictionalRelation",
        "relation_type": {"enum": "FictionalRelationType", "value": "CONNECTS"},
        "target_record_type": "FictionalTarget",
        "output_fields": {
            "source": ["value"],
            "relation": ["kind"],
            "target": ["name"],
        },
    }
    queries = []
    for index in range(1, 5):
        cases = [deepcopy(case)]
        if index == 3:
            second = deepcopy(case)
            second["ordinal"] = 2
            cases.append(second)
        queries.append(
            {
                "id": f"NQ-CQ-0{index}",
                "question_id": f"CQ-0{index}",
                "cases": cases,
            }
        )
    return _canonical(
        {
            "schema": "malleus.paper-v4.native-query-binding/v1",
            "status": "FROZEN_BEFORE_POPULATION",
            "queries": queries,
        }
    )


def _row(index: int, *, ordinal: int = 1, value: object | None = None) -> dict:
    return {
        "case_ordinal": ordinal,
        "source": {"value": f"Source {index}" if value is None else value},
        "relation": {"kind": "CONNECTS"},
        "target": {"name": "Target"},
        "witness": {
            "relation_id": f"relation:{index}:{ordinal}",
            "source_id": f"source:{index}",
            "target_id": "target:1",
        },
    }


def _query_result(binding: bytes, *, value: object | None = None) -> bytes:
    queries = []
    for index in range(1, 5):
        rows = [_row(2, value=value), _row(1, value=value)]
        if index == 1:
            rows.append(_row(1, value=value))
        queries.append(
            {
                "query_id": f"NQ-CQ-0{index}",
                "question_id": f"CQ-0{index}",
                "rows": rows,
            }
        )
    return _canonical(
        {
            "schema": QUERY_RESULT_SCHEMA,
            "inputs": {
                "ontology_sha256": ONTOLOGY_DIGEST,
                "query_binding_sha256": _digest(binding),
                "replay_receipt_sha256": "sha256:" + "3" * 64,
            },
            "graph_state_digest": "sha256:" + "4" * 64,
            "queries": queries,
            "forbidden_attempts": {
                "embedding_import": 0,
                "file_read": 0,
                "network": 0,
            },
        }
    )


def _oracle(candidate: dict[str, object]) -> bytes:
    return _canonical({"schema": ORACLE_SCHEMA, "candidate": candidate})


@pytest.fixture
def frozen(monkeypatch: pytest.MonkeyPatch) -> bytes:
    binding = _binding()
    monkeypatch.setattr(subject, "FROZEN_QUERY_BINDING_SHA256", _digest(binding))
    monkeypatch.setattr(subject, "FROZEN_ONTOLOGY_SHA256", ONTOLOGY_DIGEST)
    return binding


def _freeze_score(
    monkeypatch: pytest.MonkeyPatch, query_result: bytes, oracle: bytes
) -> None:
    monkeypatch.setattr(subject, "FROZEN_QUERY_RESULT_SHA256", _digest(query_result))
    monkeypatch.setattr(subject, "FROZEN_ORACLE_SHA256", _digest(oracle))


def test_committed_query_result_matches_frozen_production_identity() -> None:
    source = (ROOT / "paper-v4/experiment/results/query-result.json").read_bytes()
    assert _digest(source) == subject.FROZEN_QUERY_RESULT_SHA256


def test_scorer_uses_d1_rebound_oracle_not_retired_v1_coordinate() -> None:
    assert subject.FROZEN_ORACLE_SHA256 == REBOUND_V2_ORACLE_SHA256
    assert subject.FROZEN_ORACLE_SHA256 != RETIRED_V1_ORACLE_SHA256


def test_exact_four_of_four_uses_binding_and_retains_duplicates(
    frozen: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    query_result = _query_result(frozen)
    candidate = candidate_from_query_result(query_result, frozen)
    rows = candidate["questions"][0]["cases"][0]["rows"]
    assert candidate["schema"] == CANDIDATE_SCHEMA
    assert len(rows) == 3 and rows[0] == rows[1]
    assert set(rows[0]) == {"source", "relation", "target"}
    assert [case["case_ordinal"] for case in candidate["questions"][2]["cases"]] == [
        1,
        2,
    ]
    assert candidate["questions"][2]["cases"][1]["rows"] == []

    oracle = _oracle(candidate)
    _freeze_score(monkeypatch, query_result, oracle)
    result = json.loads(score_query_result(query_result, oracle, frozen))
    assert result["score"] == {"exact_questions": 4, "total_questions": 4}
    assert result["inputs"] == {
        "oracle_sha256": _digest(oracle),
        "query_binding_sha256": _digest(frozen),
        "query_result_sha256": _digest(query_result),
    }


def test_one_question_mismatch_scores_three_of_four(
    frozen: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    query_result = _query_result(frozen)
    expected = deepcopy(candidate_from_query_result(query_result, frozen))
    expected["questions"][2]["cases"][0]["rows"][0]["source"]["value"] = "Other"
    oracle = _oracle(expected)
    _freeze_score(monkeypatch, query_result, oracle)

    result = json.loads(score_query_result(query_result, oracle, frozen))
    assert result["score"] == {"exact_questions": 3, "total_questions": 4}
    assert [item["exact"] for item in result["questions"]] == [
        True,
        True,
        False,
        True,
    ]


@pytest.mark.parametrize(("observed", "expected"), [(1, 1.0), (True, 1)])
def test_json_types_do_not_compare_equal(
    frozen: bytes,
    monkeypatch: pytest.MonkeyPatch,
    observed: object,
    expected: object,
) -> None:
    query_result = _query_result(frozen, value=observed)
    wanted = deepcopy(candidate_from_query_result(query_result, frozen))
    wanted["questions"][0]["cases"][0]["rows"][0]["source"]["value"] = expected
    wanted["questions"][0]["cases"][0]["rows"].sort(key=canonical_json)
    oracle = _oracle(wanted)
    _freeze_score(monkeypatch, query_result, oracle)

    result = json.loads(score_query_result(query_result, oracle, frozen))
    assert result["score"] == {"exact_questions": 3, "total_questions": 4}
    assert result["questions"][0]["exact"] is False


def test_old_exact_oracle_shape_is_unscorable_after_identity_checks(
    frozen: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    query_result = _query_result(frozen)
    old_oracle = _canonical(
        {
            "schema": "malleus.paper-v4.answer-oracle/v1",
            "answers": [{"question_id": "CQ-01", "answer": {"prose": "not parsed"}}],
        }
    )
    _freeze_score(monkeypatch, query_result, old_oracle)

    result = json.loads(score_query_result(query_result, old_oracle, frozen))
    assert result["status"] == "UNSCORABLE_ORACLE_SCHEMA_MISMATCH"
    assert result["score"] is None


def test_fabricated_binding_refuses(frozen: bytes) -> None:
    fabricated = json.loads(frozen)
    fabricated["queries"][0]["cases"][0]["output_fields"]["source"].append("answer")
    with pytest.raises(ScoringInputRefusal, match="binding digest differs"):
        candidate_from_query_result(_query_result(frozen), _canonical(fabricated))


def test_extra_candidate_role_field_refuses(frozen: bytes) -> None:
    query_result = json.loads(_query_result(frozen))
    query_result["queries"][0]["rows"][0]["source"]["answer"] = "fabricated"
    with pytest.raises(ScoringInputRefusal, match="must contain exactly"):
        candidate_from_query_result(_canonical(query_result), frozen)


def test_oracle_missing_case_or_extra_role_is_unscorable(
    frozen: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    query_result = _query_result(frozen)
    wanted = deepcopy(candidate_from_query_result(query_result, frozen))
    wanted["questions"][2]["cases"].pop()
    oracle = _oracle(wanted)
    _freeze_score(monkeypatch, query_result, oracle)
    result = json.loads(score_query_result(query_result, oracle, frozen))
    assert result["status"] == "UNSCORABLE_ORACLE_SCHEMA_MISMATCH"

    wanted = deepcopy(candidate_from_query_result(query_result, frozen))
    wanted["questions"][0]["cases"][0]["rows"][0]["source"]["answer"] = "extra"
    oracle = _oracle(wanted)
    _freeze_score(monkeypatch, query_result, oracle)
    result = json.loads(score_query_result(query_result, oracle, frozen))
    assert result["status"] == "UNSCORABLE_ORACLE_SCHEMA_MISMATCH"


@pytest.mark.parametrize("ordinal", [True, 1.0])
def test_oracle_case_ordinal_requires_exact_integer(
    frozen: bytes, monkeypatch: pytest.MonkeyPatch, ordinal: object
) -> None:
    query_result = _query_result(frozen)
    wanted = deepcopy(candidate_from_query_result(query_result, frozen))
    wanted["questions"][0]["cases"][0]["case_ordinal"] = ordinal
    oracle = _oracle(wanted)
    _freeze_score(monkeypatch, query_result, oracle)
    result = json.loads(score_query_result(query_result, oracle, frozen))
    assert result["status"] == "UNSCORABLE_ORACLE_SCHEMA_MISMATCH"


def test_oracle_digest_drift_refuses(
    frozen: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    query_result = _query_result(frozen)
    oracle = _oracle(candidate_from_query_result(query_result, frozen))
    _freeze_score(monkeypatch, query_result, oracle)
    with pytest.raises(ScoringInputRefusal, match="oracle digest differs"):
        score_query_result(query_result, oracle + b"\n", frozen)


def test_query_result_pending_refuses(
    frozen: bytes, monkeypatch: pytest.MonkeyPatch
) -> None:
    query_result = _query_result(frozen)
    oracle = _oracle(candidate_from_query_result(query_result, frozen))
    monkeypatch.setattr(subject, "FROZEN_QUERY_RESULT_SHA256", None)
    monkeypatch.setattr(subject, "FROZEN_ORACLE_SHA256", _digest(oracle))
    with pytest.raises(ScoringInputRefusal, match="query result digest is PENDING"):
        score_query_result(query_result, oracle, frozen)


def test_malformed_candidate_and_result_binding_drift_refuse(frozen: bytes) -> None:
    query_result = json.loads(_query_result(frozen))
    del query_result["queries"][0]["rows"][0]["target"]
    with pytest.raises(ScoringInputRefusal, match="must contain exactly"):
        candidate_from_query_result(_canonical(query_result), frozen)

    query_result = json.loads(_query_result(frozen))
    query_result["inputs"]["query_binding_sha256"] = "sha256:" + "9" * 64
    with pytest.raises(ScoringInputRefusal, match="supplied binding"):
        candidate_from_query_result(_canonical(query_result), frozen)


@pytest.mark.parametrize("failure", ["pending", "invalid"])
def test_cli_does_not_read_oracle_before_query_preflight(
    frozen: bytes,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    failure: str,
) -> None:
    binding_path = tmp_path / "binding.json"
    result_path = tmp_path / "query-result.json"
    oracle_path = tmp_path / "oracle.json"
    output_path = tmp_path / "score.json"
    query_result = _query_result(frozen)
    if failure == "invalid":
        value = json.loads(query_result)
        del value["queries"][0]["rows"][0]["target"]
        query_result = _canonical(value)
        monkeypatch.setattr(
            subject, "FROZEN_QUERY_RESULT_SHA256", _digest(query_result)
        )
    else:
        monkeypatch.setattr(subject, "FROZEN_QUERY_RESULT_SHA256", None)
    binding_path.write_bytes(frozen)
    result_path.write_bytes(query_result)
    oracle_path.write_bytes(b"fictional oracle must remain unread")

    reads = []
    read_bytes = Path.read_bytes

    def spy(path: Path) -> bytes:
        reads.append(path)
        return read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", spy)
    with pytest.raises(ScoringInputRefusal):
        main(
            [
                "--binding",
                str(binding_path),
                "--query-result",
                str(result_path),
                "--oracle",
                str(oracle_path),
                "--output",
                str(output_path),
            ]
        )
    assert oracle_path not in reads
    assert not output_path.exists()


def test_cli_read_errors_are_typed_and_name_role_and_path(
    frozen: bytes, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    binding_path = tmp_path / "binding.json"
    result_path = tmp_path / "query-result.json"
    missing_oracle = tmp_path / "missing-oracle.json"
    output_path = tmp_path / "score.json"
    argv = [
        "--binding",
        str(binding_path),
        "--query-result",
        str(result_path),
        "--oracle",
        str(missing_oracle),
        "--output",
        str(output_path),
    ]
    query_result = _query_result(frozen)

    with pytest.raises(
        ScoringInputRefusal, match=f"cannot read query binding at {binding_path}"
    ):
        main(argv)
    binding_path.write_bytes(frozen)

    with pytest.raises(
        ScoringInputRefusal, match=f"cannot read query result at {result_path}"
    ):
        main(argv)
    result_path.write_bytes(query_result)
    monkeypatch.setattr(subject, "FROZEN_QUERY_RESULT_SHA256", _digest(query_result))

    with pytest.raises(
        ScoringInputRefusal,
        match=f"cannot read oracle at {missing_oracle}",
    ):
        main(argv)


def test_score_writer_never_overwrites(tmp_path) -> None:
    output = tmp_path / "score.json"
    write_score_result(output, b"first")
    with pytest.raises(ScoringInputRefusal, match="already exists"):
        write_score_result(output, b"second")
    assert output.read_bytes() == b"first"
