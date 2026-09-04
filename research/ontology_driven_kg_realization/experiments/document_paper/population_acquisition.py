"""Structural envelope check for one model-authored population candidate."""

from __future__ import annotations

from enum import Enum
import json

from malleus.ledger import canonical_json


class PopulationCandidateKind(str, Enum):
    """Terminal model refusal or candidate eligible for ontology compilation."""

    PROPOSAL = "PROPOSAL"
    MODEL_REFUSAL = "MODEL_REFUSAL"


class PopulationAcquisitionError(ValueError):
    """Typed structural defect eligible for the single acquisition retry."""

    def __init__(self, code: str, subject: str, detail: str) -> None:
        self.code = code
        self.subject = subject
        self.detail = detail
        super().__init__(f"{code}:{subject}: {detail}")

    def canonical_diagnostic_bytes(self) -> bytes:
        """Serialize the exact diagnostic returned to the producer."""

        return canonical_json(
            {
                "code": self.code,
                "detail": self.detail,
                "stage": "POPULATION_ACQUISITION",
                "status": "REFUSED",
                "subject": self.subject,
            }
        ).encode("utf-8")


def _fail(code: str, subject: str, detail: str) -> None:
    raise PopulationAcquisitionError(code, subject, detail)


def _pairs(values: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in values:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value: str) -> None:
    raise ValueError(f"nonstandard numeric constant: {value}")


def classify_population_candidate(
    source: bytes,
    *,
    success_schema: str,
    refusal_schema: str,
    record_id_prefix: str,
    ordinal_width: int,
) -> PopulationCandidateKind:
    """Classify exact model bytes without judging their domain meaning."""

    if type(source) is not bytes:
        raise TypeError("source must be exact bytes")
    for value, label in (
        (success_schema, "success_schema"),
        (refusal_schema, "refusal_schema"),
        (record_id_prefix, "record_id_prefix"),
    ):
        if type(value) is not str or not value.strip():
            raise ValueError(f"{label} must be nonblank text")
    if type(ordinal_width) is not int or ordinal_width < 1:
        raise ValueError("ordinal_width must be a positive integer")
    try:
        value = json.loads(
            source.decode("utf-8"),
            object_pairs_hook=_pairs,
            parse_constant=_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        _fail(
            "POPULATION_CANDIDATE_JSON_INVALID",
            "population",
            f"candidate must be one strict UTF-8 JSON object: {type(error).__name__}",
        )
    if type(value) is not dict:
        _fail(
            "POPULATION_CANDIDATE_SCHEMA_INVALID",
            "population",
            "candidate must be one JSON object",
        )
    schema = value.get("schema")
    if schema == refusal_schema:
        if set(value) != {"schema", "reason"}:
            _fail(
                "POPULATION_REFUSAL_FIELDS_INVALID",
                "population",
                "model refusal must contain exactly schema and reason",
            )
        reason = value["reason"]
        if type(reason) is not str or not reason.strip():
            _fail(
                "POPULATION_REFUSAL_REASON_INVALID",
                "population.reason",
                "model refusal reason must be nonblank text",
            )
        return PopulationCandidateKind.MODEL_REFUSAL
    if schema != success_schema:
        _fail(
            "POPULATION_CANDIDATE_SCHEMA_INVALID",
            "population.schema",
            "candidate schema is neither the success nor refusal schema",
        )
    expected_fields = {"schema", "ontology_sha256", "reading_sha256", "records"}
    if set(value) != expected_fields:
        _fail(
            "POPULATION_CANDIDATE_FIELDS_INVALID",
            "population",
            "proposal fields do not match the closed acquisition envelope",
        )
    records = value["records"]
    if type(records) is not list or not records:
        _fail(
            "POPULATION_CANDIDATE_RECORDS_INVALID",
            "population.records",
            "proposal records must be a nonempty array",
        )
    for index, record in enumerate(records, start=1):
        subject = f"population.records[{index - 1}].record_id"
        if type(record) is not dict or "record_id" not in record:
            _fail(
                "POPULATION_RECORD_ID_POLICY_VIOLATION",
                subject,
                "record must contain its opaque sequential id",
            )
        expected = record_id_prefix + f"{index:0{ordinal_width}d}"
        if record["record_id"] != expected:
            _fail(
                "POPULATION_RECORD_ID_POLICY_VIOLATION",
                subject,
                f"record id must equal {expected!r}",
            )
    return PopulationCandidateKind.PROPOSAL


__all__ = [
    "PopulationAcquisitionError",
    "PopulationCandidateKind",
    "classify_population_candidate",
]
