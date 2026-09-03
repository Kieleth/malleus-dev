"""Strict exact-match scoring for the four paper-v4 query results."""

from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from malleus.ledger import LedgerError, canonical_json
from research.ontology_driven_kg_realization.experiments.document_paper.native_query import (
    NativeQueryRefusal,
    load_query_binding,
)


QUERY_RESULT_SCHEMA = "malleus.paper-v4.query-replay/v1"
CANDIDATE_SCHEMA = "malleus.paper-v4.query-candidate/v1"
ORACLE_SCHEMA = "malleus.paper-v4.query-oracle/v1"
SCORE_SCHEMA = "malleus.paper-v4.query-score/v1"
FROZEN_QUERY_BINDING_SHA256 = (
    "sha256:115009ff737600d63eb9761bfc11f69ee62cd11f41d60682772556f5fa56c6d9"
)
FROZEN_ONTOLOGY_SHA256 = (
    "sha256:df483285ede9820e25e17215d18ee089d9faeff8d7afaf02365083e19671c941"
)
FROZEN_ORACLE_SHA256 = (
    "sha256:95b206a8a8eac20f208854c2374ed8433187402d9ab1e50771003e412066b571"
)
FROZEN_QUERY_RESULT_SHA256: str | None = None


class ScoringInputRefusal(ValueError):
    """A retained byte input cannot enter scoring."""

    status = "SCORING_INPUT_REFUSAL"


def _refuse(detail: str) -> None:
    raise ScoringInputRefusal(detail)


def _digest(source: bytes) -> str:
    if type(source) is not bytes:
        raise TypeError("digest source must be bytes")
    return "sha256:" + sha256(source).hexdigest()


def _object(value: object, subject: str) -> dict[str, Any]:
    if type(value) is not dict:
        _refuse(f"{subject} must be an object")
    return value


def _array(value: object, subject: str) -> list[Any]:
    if type(value) is not list:
        _refuse(f"{subject} must be an array")
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str], subject: str) -> None:
    if set(value) != expected:
        _refuse(f"{subject} must contain exactly {sorted(expected)}")


def _json(source: bytes, subject: str, *, canonical: bool) -> object:
    if type(source) is not bytes:
        raise TypeError(f"{subject} source must be bytes")
    try:
        value = json.loads(source)
        encoded = canonical_json(value).encode("utf-8")
    except (UnicodeDecodeError, json.JSONDecodeError, LedgerError) as error:
        raise ScoringInputRefusal(f"{subject} must be UTF-8 JSON") from error
    if canonical and encoded != source:
        _refuse(f"{subject} bytes are not canonical JSON")
    return value


def _sha256(value: object, subject: str) -> str:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        _refuse(f"{subject} must be a sha256 digest")
    if len(value) != 71 or any(c not in "0123456789abcdef" for c in value[7:]):
        _refuse(f"{subject} must be a sha256 digest")
    return value


def _frozen(source: bytes, expected: str | None, subject: str) -> str:
    if expected is None:
        _refuse(f"{subject} digest is PENDING")
    observed = _digest(source)
    if observed != expected:
        _refuse(f"{subject} digest differs from the frozen identity")
    return observed


def _binding(source: bytes) -> dict[str, Any]:
    _frozen(source, FROZEN_QUERY_BINDING_SHA256, "query binding")
    try:
        return load_query_binding(source)
    except NativeQueryRefusal as error:
        raise ScoringInputRefusal(f"query binding refused: {error}") from error


def _answer_row(value: object, case: Mapping[str, Any], subject: str) -> dict[str, Any]:
    row = _object(value, subject)
    roles = {"source", "relation", "target"}
    _exact_keys(row, roles, subject)
    answer = {}
    for role in sorted(roles):
        fields = set(case["output_fields"][role])
        record = _object(row[role], f"{subject}.{role}")
        _exact_keys(record, fields, f"{subject}.{role}")
        answer[role] = deepcopy(record)
    return answer


def _strip_query_row(
    value: object, cases: Mapping[int, Mapping[str, Any]], subject: str
) -> tuple[int, dict[str, Any]]:
    row = _object(value, subject)
    _exact_keys(
        row,
        {"case_ordinal", "source", "relation", "target", "witness"},
        subject,
    )
    ordinal = row["case_ordinal"]
    if type(ordinal) is not int or ordinal not in cases:
        _refuse(f"{subject}.case_ordinal is not bound for this question")
    witness = _object(row["witness"], f"{subject}.witness")
    _exact_keys(
        witness,
        {"relation_id", "source_id", "target_id"},
        f"{subject}.witness",
    )
    if any(
        not isinstance(witness[field], str) or not witness[field].strip()
        for field in witness
    ):
        _refuse(f"{subject}.witness ids must be nonblank text")
    answer = _answer_row(
        {role: row[role] for role in ("source", "relation", "target")},
        cases[ordinal],
        subject,
    )
    return ordinal, answer


def _result_queries(
    source: bytes, binding: Mapping[str, Any], binding_digest: str
) -> list[Any]:
    root = _object(_json(source, "query result", canonical=True), "query result")
    _exact_keys(
        root,
        {"schema", "inputs", "graph_state_digest", "queries", "forbidden_attempts"},
        "query result",
    )
    if root["schema"] != QUERY_RESULT_SCHEMA:
        _refuse(f"query result.schema must equal {QUERY_RESULT_SCHEMA!r}")
    inputs = _object(root["inputs"], "query result.inputs")
    input_keys = {
        "ontology_sha256",
        "query_binding_sha256",
        "replay_receipt_sha256",
    }
    _exact_keys(inputs, input_keys, "query result.inputs")
    for field in input_keys:
        _sha256(inputs[field], f"query result.inputs.{field}")
    if inputs["ontology_sha256"] != FROZEN_ONTOLOGY_SHA256:
        _refuse("query result ontology digest differs from the frozen identity")
    if inputs["query_binding_sha256"] != binding_digest:
        _refuse("query result binding digest differs from the supplied binding")
    _sha256(root["graph_state_digest"], "query result.graph_state_digest")
    attempts = _object(root["forbidden_attempts"], "query result.forbidden_attempts")
    _exact_keys(attempts, {"embedding_import", "file_read", "network"}, "attempts")
    if any(type(count) is not int or count != 0 for count in attempts.values()):
        _refuse("query result forbidden attempts must all be integer zero")
    queries = _array(root["queries"], "query result.queries")
    if len(queries) != len(binding["queries"]):
        _refuse("query result query count differs from the frozen binding")
    return queries


def _candidate(
    source: bytes, binding: Mapping[str, Any], digest: str
) -> dict[str, Any]:
    questions = []
    queries = _result_queries(source, binding, digest)
    for index, (raw_query, bound) in enumerate(
        zip(queries, binding["queries"], strict=True)
    ):
        subject = f"query result.queries[{index}]"
        query = _object(raw_query, subject)
        _exact_keys(query, {"query_id", "question_id", "rows"}, subject)
        if (
            query["query_id"] != bound["id"]
            or query["question_id"] != bound["question_id"]
        ):
            _refuse(f"{subject} ids differ from the frozen binding")
        cases = {case["ordinal"]: case for case in bound["cases"]}
        grouped = {ordinal: [] for ordinal in cases}
        for row_index, row in enumerate(_array(query["rows"], f"{subject}.rows")):
            ordinal, answer = _strip_query_row(
                row, cases, f"{subject}.rows[{row_index}]"
            )
            grouped[ordinal].append(answer)
        questions.append(
            {
                "question_id": bound["question_id"],
                "cases": [
                    {
                        "case_ordinal": ordinal,
                        "rows": sorted(grouped[ordinal], key=canonical_json),
                    }
                    for ordinal in cases
                ],
            }
        )
    return {"schema": CANDIDATE_SCHEMA, "questions": questions}


def candidate_from_query_result(source: bytes, binding_source: bytes) -> dict[str, Any]:
    """Derive the exact witness-free answer shape from the frozen binding."""

    binding = _binding(binding_source)
    return _candidate(source, binding, _digest(binding_source))


def _validate_candidate(value: object, binding: Mapping[str, Any]) -> dict[str, Any]:
    root = _object(value, "oracle candidate")
    _exact_keys(root, {"schema", "questions"}, "oracle candidate")
    if root["schema"] != CANDIDATE_SCHEMA:
        _refuse("oracle candidate schema differs")
    questions = _array(root["questions"], "oracle candidate.questions")
    if len(questions) != len(binding["queries"]):
        _refuse("oracle candidate question count differs")
    for index, (question, bound) in enumerate(
        zip(questions, binding["queries"], strict=True)
    ):
        subject = f"oracle candidate.questions[{index}]"
        question = _object(question, subject)
        _exact_keys(question, {"question_id", "cases"}, subject)
        if question["question_id"] != bound["question_id"]:
            _refuse(f"{subject}.question_id differs from binding")
        cases = _array(question["cases"], f"{subject}.cases")
        if len(cases) != len(bound["cases"]):
            _refuse(f"{subject}.cases differ from binding")
        for case_index, (case, bound_case) in enumerate(
            zip(cases, bound["cases"], strict=True)
        ):
            case_subject = f"{subject}.cases[{case_index}]"
            case = _object(case, case_subject)
            _exact_keys(case, {"case_ordinal", "rows"}, case_subject)
            ordinal = case["case_ordinal"]
            if type(ordinal) is not int or ordinal != bound_case["ordinal"]:
                _refuse(f"{case_subject}.case_ordinal differs from binding")
            rows = _array(case["rows"], f"{case_subject}.rows")
            normalized = [
                _answer_row(row, bound_case, f"{case_subject}.rows[{row_index}]")
                for row_index, row in enumerate(rows)
            ]
            if canonical_json(rows) != canonical_json(
                sorted(normalized, key=canonical_json)
            ):
                _refuse(f"{case_subject}.rows are not canonically sorted")
    return root


def _oracle_candidate(
    value: object, binding: Mapping[str, Any]
) -> dict[str, Any] | None:
    if type(value) is not dict or set(value) != {"schema", "candidate"}:
        return None
    if value["schema"] != ORACLE_SCHEMA:
        return None
    try:
        return _validate_candidate(value["candidate"], binding)
    except ScoringInputRefusal:
        return None


def _preflight(
    query_result_source: bytes, binding_source: bytes
) -> tuple[dict[str, Any], dict[str, Any], str]:
    """Validate every non-oracle scoring input and its frozen identity."""

    _frozen(query_result_source, FROZEN_QUERY_RESULT_SHA256, "query result")
    binding = _binding(binding_source)
    binding_digest = _digest(binding_source)
    candidate = _candidate(query_result_source, binding, binding_digest)
    return candidate, binding, binding_digest


def score_query_result(
    query_result_source: bytes, oracle_source: bytes, binding_source: bytes
) -> bytes:
    """Return four-question exact-match score, or a typed oracle mismatch."""

    candidate, binding, binding_digest = _preflight(query_result_source, binding_source)
    _frozen(oracle_source, FROZEN_ORACLE_SHA256, "oracle")
    expected = _oracle_candidate(
        _json(oracle_source, "oracle", canonical=False), binding
    )
    inputs = {
        "oracle_sha256": _digest(oracle_source),
        "query_binding_sha256": binding_digest,
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
                "exact": canonical_json(observed) == canonical_json(wanted),
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


def write_score_result(path: Path, source: bytes) -> None:
    """Write one score result without replacing an existing artifact."""

    if not isinstance(path, Path) or type(source) is not bytes:
        raise TypeError("score result requires one Path and exact bytes")
    try:
        with path.open("xb") as stream:
            stream.write(source)
    except FileExistsError as error:
        raise ScoringInputRefusal(f"score result already exists at {path}") from error
    except OSError as error:
        raise ScoringInputRefusal(
            f"cannot write score result {path}: {error}"
        ) from error


def _read_source(path: Path, role: str) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise ScoringInputRefusal(f"cannot read {role} at {path}: {error}") from error


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query-result", required=True, type=Path)
    parser.add_argument("--oracle", required=True, type=Path)
    parser.add_argument("--binding", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    binding_source = _read_source(args.binding, "query binding")
    query_result_source = _read_source(args.query_result, "query result")
    _preflight(query_result_source, binding_source)
    oracle_source = _read_source(args.oracle, "oracle")
    result = score_query_result(
        query_result_source,
        oracle_source,
        binding_source,
    )
    write_score_result(args.output, result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
