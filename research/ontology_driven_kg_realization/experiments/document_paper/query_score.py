"""Strict exact-match scoring for the four paper-v4 query results."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from typing import Any, Mapping

from malleus.ledger import LedgerError, canonical_json


QUERY_RESULT_SCHEMA = "malleus.paper-v4.query-replay/v1"
CANDIDATE_SCHEMA = "malleus.paper-v4.query-candidate/v1"
ORACLE_SCHEMA = "malleus.paper-v4.query-oracle/v1"
SCORE_SCHEMA = "malleus.paper-v4.query-score/v1"
QUESTION_IDS = ("CQ-01", "CQ-02", "CQ-03", "CQ-04")
QUERY_IDS = ("NQ-CQ-01", "NQ-CQ-02", "NQ-CQ-03", "NQ-CQ-04")
CASE_ORDINALS = ((1,), (1,), (1, 2), (1,))


class ScoringInputRefusal(ValueError):
    """The candidate query-result bytes cannot enter scoring."""

    status = "SCORING_INPUT_REFUSAL"


def _refuse(detail: str) -> None:
    raise ScoringInputRefusal(detail)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _object(value: object, subject: str) -> dict[str, Any]:
    if type(value) is not dict:
        _refuse(f"{subject} must be an object")
    return value


def _array(value: object, subject: str) -> list[Any]:
    if type(value) is not list:
        _refuse(f"{subject} must be an array")
    return value


def _exact_keys(
    value: Mapping[str, Any], expected: frozenset[str], subject: str
) -> None:
    if set(value) != expected:
        _refuse(f"{subject} must contain exactly {sorted(expected)}")


def _canonical_value(source: bytes, subject: str) -> object:
    if type(source) is not bytes:
        raise TypeError(f"{subject} source must be bytes")
    try:
        value = json.loads(source)
        encoded = canonical_json(value).encode("utf-8")
    except (UnicodeDecodeError, json.JSONDecodeError, LedgerError) as error:
        raise ScoringInputRefusal(f"{subject} must be canonical UTF-8 JSON") from error
    if encoded != source:
        _refuse(f"{subject} bytes are not canonical JSON")
    return value


def _json_value(source: bytes, subject: str) -> object:
    if type(source) is not bytes:
        raise TypeError(f"{subject} source must be bytes")
    try:
        return json.loads(source)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ScoringInputRefusal(f"{subject} must be UTF-8 JSON") from error


def _text(value: object, subject: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _refuse(f"{subject} must be nonblank text")
    return value


def _sha256(value: object, subject: str) -> str:
    text = _text(value, subject)
    if (
        not text.startswith("sha256:")
        or len(text) != 71
        or any(character not in "0123456789abcdef" for character in text[7:])
    ):
        _refuse(f"{subject} must be a sha256 digest")
    return text


def _role(value: object, subject: str) -> dict[str, Any]:
    role = _object(value, subject)
    if any(not key.strip() for key in role):
        _refuse(f"{subject} field names must be nonblank")
    return deepcopy(role)


def _candidate_row(value: object, subject: str) -> dict[str, Any]:
    row = _object(value, subject)
    _exact_keys(
        row,
        frozenset({"case_ordinal", "source", "relation", "target", "witness"}),
        subject,
    )
    ordinal = row["case_ordinal"]
    if type(ordinal) is not int or ordinal < 1:
        _refuse(f"{subject}.case_ordinal must be a positive integer")
    witness = _object(row["witness"], f"{subject}.witness")
    _exact_keys(
        witness,
        frozenset({"relation_id", "source_id", "target_id"}),
        f"{subject}.witness",
    )
    for field in ("relation_id", "source_id", "target_id"):
        _text(witness[field], f"{subject}.witness.{field}")
    return {
        "source": _role(row["source"], f"{subject}.source"),
        "relation": _role(row["relation"], f"{subject}.relation"),
        "target": _role(row["target"], f"{subject}.target"),
    }


def _validate_result_envelope(root: Mapping[str, Any]) -> None:
    _exact_keys(
        root,
        frozenset(
            {
                "schema",
                "inputs",
                "graph_state_digest",
                "queries",
                "forbidden_attempts",
            }
        ),
        "query result",
    )
    if root["schema"] != QUERY_RESULT_SCHEMA:
        _refuse(f"query result.schema must equal {QUERY_RESULT_SCHEMA!r}")
    inputs = _object(root["inputs"], "query result.inputs")
    expected_inputs = frozenset(
        {
            "ontology_sha256",
            "query_binding_sha256",
            "replay_receipt_sha256",
        }
    )
    _exact_keys(inputs, expected_inputs, "query result.inputs")
    for field in expected_inputs:
        _sha256(inputs[field], f"query result.inputs.{field}")
    _sha256(root["graph_state_digest"], "query result.graph_state_digest")
    attempts = _object(root["forbidden_attempts"], "query result.forbidden_attempts")
    expected_attempts = frozenset({"embedding_import", "file_read", "network"})
    _exact_keys(attempts, expected_attempts, "query result.forbidden_attempts")
    for field in expected_attempts:
        if type(attempts[field]) is not int or attempts[field] < 0:
            _refuse(
                f"query result.forbidden_attempts.{field} "
                "must be a non-negative integer"
            )
        if attempts[field] != 0:
            _refuse(
                f"query result.forbidden_attempts.{field} must be zero before scoring"
            )


def candidate_from_query_result(source: bytes) -> dict[str, Any]:
    """Strip witnesses and canonicalize observed cases and row multisets."""

    root = _object(_canonical_value(source, "query result"), "query result")
    _validate_result_envelope(root)
    queries = _array(root["queries"], "query result.queries")
    if len(queries) != len(QUESTION_IDS):
        _refuse("query result must contain exactly four queries")

    questions = []
    for index, raw_query in enumerate(queries):
        subject = f"query result.queries[{index}]"
        query = _object(raw_query, subject)
        _exact_keys(query, frozenset({"query_id", "question_id", "rows"}), subject)
        if query["query_id"] != QUERY_IDS[index]:
            _refuse(f"{subject}.query_id is out of order or unknown")
        if query["question_id"] != QUESTION_IDS[index]:
            _refuse(f"{subject}.question_id is out of order or unknown")

        expected_ordinals = CASE_ORDINALS[index]
        grouped: dict[int, list[dict[str, Any]]] = {
            ordinal: [] for ordinal in expected_ordinals
        }
        for row_index, raw_row in enumerate(_array(query["rows"], f"{subject}.rows")):
            row_subject = f"{subject}.rows[{row_index}]"
            row = _object(raw_row, row_subject)
            ordinal = row.get("case_ordinal")
            candidate_row = _candidate_row(row, row_subject)
            if ordinal not in grouped:
                _refuse(f"{row_subject}.case_ordinal is not bound for this question")
            grouped[ordinal].append(candidate_row)
        cases = []
        for ordinal in sorted(grouped):
            rows = sorted(grouped[ordinal], key=canonical_json)
            cases.append({"case_ordinal": ordinal, "rows": rows})
        questions.append({"question_id": QUESTION_IDS[index], "cases": cases})
    return {"schema": CANDIDATE_SCHEMA, "questions": questions}


def _valid_role(value: object) -> bool:
    return type(value) is dict and all(key.strip() for key in value)


def _valid_candidate(value: object) -> bool:
    if type(value) is not dict or set(value) != {"schema", "questions"}:
        return False
    if value["schema"] != CANDIDATE_SCHEMA or type(value["questions"]) is not list:
        return False
    if len(value["questions"]) != len(QUESTION_IDS):
        return False
    for expected_id, question in zip(QUESTION_IDS, value["questions"], strict=True):
        if type(question) is not dict or set(question) != {"question_id", "cases"}:
            return False
        if (
            question["question_id"] != expected_id
            or type(question["cases"]) is not list
        ):
            return False
        ordinals = []
        for case in question["cases"]:
            if type(case) is not dict or set(case) != {"case_ordinal", "rows"}:
                return False
            ordinal = case["case_ordinal"]
            if (
                type(ordinal) is not int
                or ordinal < 1
                or type(case["rows"]) is not list
            ):
                return False
            ordinals.append(ordinal)
            row_keys = {"source", "relation", "target"}
            if any(
                type(row) is not dict
                or set(row) != row_keys
                or not all(_valid_role(row[role]) for role in row_keys)
                for row in case["rows"]
            ):
                return False
            if case["rows"] != sorted(case["rows"], key=canonical_json):
                return False
        if ordinals != sorted(set(ordinals)):
            return False
    return True


def _oracle_candidate(value: object) -> dict[str, Any] | None:
    if type(value) is not dict or set(value) != {"schema", "candidate"}:
        return None
    if value["schema"] != ORACLE_SCHEMA or not _valid_candidate(value["candidate"]):
        return None
    return value["candidate"]


def score_query_result(query_result_source: bytes, oracle_source: bytes) -> bytes:
    """Return four-question exact-match score, or a typed oracle mismatch."""

    candidate = candidate_from_query_result(query_result_source)
    oracle_value = _json_value(oracle_source, "oracle")
    expected = _oracle_candidate(oracle_value)
    inputs = {
        "oracle_sha256": _digest(oracle_source),
        "query_result_sha256": _digest(query_result_source),
    }
    if expected is None:
        result = {
            "schema": SCORE_SCHEMA,
            "status": "UNSCORABLE_ORACLE_SCHEMA_MISMATCH",
            "inputs": inputs,
            "score": None,
            "questions": [],
        }
    else:
        questions = [
            {
                "question_id": observed["question_id"],
                "exact": observed == wanted,
            }
            for observed, wanted in zip(
                candidate["questions"], expected["questions"], strict=True
            )
        ]
        result = {
            "schema": SCORE_SCHEMA,
            "status": "SCORED",
            "inputs": inputs,
            "score": {
                "exact_questions": sum(item["exact"] for item in questions),
                "total_questions": len(questions),
            },
            "questions": questions,
        }
    return canonical_json(result).encode("utf-8")
