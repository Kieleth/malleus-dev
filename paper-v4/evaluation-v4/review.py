"""Validate the run-02 source-grounded review without judging its content.

`research/.../document_paper/human_review.py` cannot be reused. Its grammar is
pinned to the v1 protocol: schema `.../review-protocol/v1`, status
`FROZEN_BEFORE_V2_QUERY_OUTPUT`, an exact key set carrying
`review_input_manifest` and `validator_materials`, a four-item
`review_materials` list, and a query result at
`malleus.paper-v4.query-replay/v1` whose inputs name an ontology digest. The
protocol frozen for v4 is `.../review-protocol/v2`, status
`FROZEN_BEFORE_V4_PRODUCER`, with `withheld_from_producer`, a
`graph_claim_path` in the evidence surface, `population_trace` among the review
materials, and a query result at `malleus.paper-v4.query-result/v2` or `/v3`
(v3, from run-15, carries `case_ordinals` and one row per witness) whose
inputs name a ledger head. Every one of those refuses in the v1 validator, so
this module carries the v2 grammar instead.

It checks identities, references and authorship state. It never chooses,
changes or aggregates a judgment.

Protocol v3 lives here beside v2 and is dispatched by the version each file
declares in its own `schema`. It differs from v2 in six places, every one of
them from `handover/2026-09-06-grading-rca.md` or
`handover/2026-09-06-shop-01-rca.md`: the evidence surface is declared by the
cell's manifest rather than fixed here, so a row-shaped cell can be validated
at all; a row locator is opened in the declared source file under the declared
numbering convention; source support is judged once per distinct witness and
referenced by the rows that share it; a witness whose locator does not resolve
is NOT_EVALUABLE by rule; the responsiveness label is derived from coverage per
required semantic instead of chosen; and a control question's outcome is
reported as a finding and refuses nothing. A protocol, manifest and record that
do not declare the same version are refused.
"""

from __future__ import annotations

import csv
from datetime import datetime
from hashlib import sha256
import io
import json
import re
from typing import Any, Mapping


PROTOCOL_SCHEMA = "malleus.paper-v4.source-grounded-review-protocol/v2"
PROTOCOL_STATUS = "FROZEN_BEFORE_V4_PRODUCER"
MANIFEST_SCHEMA = "malleus.paper-v4.source-grounded-review-inputs/v2"
REVIEW_SCHEMA = "malleus.paper-v4.source-grounded-review/v2"
QUERY_RESULT_SCHEMAS = frozenset(
    {"malleus.paper-v4.query-result/v2", "malleus.paper-v4.query-result/v3"}
)
FROZEN_MANIFEST_STATUS = "FROZEN_FOR_REVIEW"
# Codex is unavailable, so run-02's preliminary reviewer is a fresh Claude
# session. The protocol is frozen and says CODEX_PRELIMINARY; the manifest
# carries the substitution and must declare it as a deviation.
PRELIMINARY_EVALUATOR_KINDS = ("CODEX_PRELIMINARY", "CLAUDE_PRELIMINARY")

_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")
_JSON_BLOCK = re.compile(r"```json\n(?P<record>.*?)\n```", re.DOTALL)
_REVIEW_STATUSES = {
    "BLANK",
    "PRELIMINARY_COMPLETE",
    "HUMAN_RATIFIED",
    "HUMAN_REJECTED",
}
_RATIFIED_DISPOSITIONS = {"RATIFIED_AS_RECORDED", "RATIFIED_WITH_EDITS"}
_FIXED_IDENTITY_KEYS = {
    "competency_questions_sha256",
    "selected_reading_sha256",
    "source_sha256",
}
_STAGE_IDENTITY_KEYS = {
    "accepted_ontology_sha256",
    "ledger_head",
    "population_trace_summary_sha256",
    "query_binding_sha256",
    "query_result_sha256",
    "query_trace_summary_sha256",
    "replay_receipt_sha256",
}
_MATERIAL_KEYS = {"name", "path", "sha256", "visibility"}
_DEVIATION_KEYS = {"from", "protocol_edited", "reason", "to"}

PROTOCOL_SCHEMA_V3 = "malleus.paper-v4.source-grounded-review-protocol/v3"
PROTOCOL_STATUS_V3 = "FROZEN_BEFORE_NEXT_CELL"
MANIFEST_SCHEMA_V3 = "malleus.paper-v4.source-grounded-review-inputs/v3"
REVIEW_SCHEMA_V3 = "malleus.paper-v4.source-grounded-review/v3"
QUESTION_FILE_SCHEMAS = frozenset(
    {
        "malleus.paper-v4.competency-questions/v2",
        "malleus.paper-v4.competency-questions/v3",
    }
)

SURFACE_LOCATOR_KINDS = {
    "SELECTED_READING_TEXT_LAYER": "SELECTED_READING_BLOCK_ID",
    "STRUCTURED_ROWS": "SOURCE_ROW_FIELD",
}
ROW_RESOLUTIONS = (
    "VALUE_MATCHES_ROW",
    "VALUE_DERIVED_FROM_ROW",
    "VALUE_DIFFERS_FROM_ROW",
    "LOCATOR_NOT_RESOLVABLE",
)
RESOLVING_ROW_RESOLUTIONS = frozenset(ROW_RESOLUTIONS[:3])
COVERAGE_ABSENT_REASONS = (
    "NOT_MODELLED",
    "WITHHELD_STATEMENT",
    "UNREACHED_RECORD",
    "NOT_IN_SOURCE",
    "LOCATOR_NOT_RESOLVABLE",
)
COVERAGE_LABELS = ("COVERED", "PARTIAL", "NONE")
ASSEMBLY_DESCRIPTORS = ("ONE_ROW", "LINKED_ROWS", "UNLINKED_ROWS")
CONTROL_KINDS = ("NOT_IN_SOURCE", "EXCLUDED_SURFACE", "PARAPHRASE")
SOURCE_FORMATS = ("CSV", "JSONL")

_ROW_LOCATOR = re.compile(
    r"(?P<source>[^\s#]+)#row:(?P<row>\d+):"
    r"(?P<field>[A-Za-z_][A-Za-z0-9_.\-]*(?:\[\d+\])*)\Z"
)
_BRACKET = re.compile(r"\[(\d+)\]")
_SOURCE_KEYS = {"format", "path", "sha256", "source_id"}
_CONVENTION_KEYS = {"csv_header_is_a_row", "first_row_index", "form"}
_MANIFEST_KEYS_V3 = {
    "authorship",
    "evidence_surface",
    "fixed_identities",
    "materials",
    "question_ids",
    "review_protocol_sha256",
    "rows_per_question",
    "run_id",
    "schema",
    "stage_identities",
    "status",
    "witnesses_traced",
}
_RECORD_KEYS_V3 = {
    "inputs",
    "preliminary",
    "questions",
    "ratification",
    "schema",
    "status",
    "witnesses",
}
_QUESTION_KEYS_V3 = {
    "assembly",
    "coverage",
    "question_id",
    "question_responsiveness",
    "responsiveness_rationale",
    "rows",
    "source_locators",
}
_ROW_KEYS_V3 = {"row_index", "witness_key"}
_COVERAGE_KEYS = {"absent_reason", "note", "row_index", "semantic"}
_WITNESS_KEYS = {"rationale", "source_locators", "source_support", "witness_key"}
_QUESTION_KEYS = {
    "question_id",
    "question_responsiveness",
    "responsiveness_rationale",
    "rows",
    "source_locators",
}
_ROW_KEYS = {"rationale", "row_index", "source_locators", "source_support"}


class ReviewRefusal(ValueError):
    """A review protocol, input manifest or record is structurally invalid."""


def _refuse(detail: str) -> None:
    raise ReviewRefusal(detail)


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


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            _refuse(f"JSON contains duplicate key {key!r}")
        result[key] = value
    return result


def _json(source: bytes, subject: str) -> object:
    if type(source) is not bytes:
        raise TypeError(f"{subject} source must be bytes")
    try:
        return json.loads(source, object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReviewRefusal(f"{subject} must be UTF-8 JSON") from error


def _digest(source: bytes) -> str:
    if type(source) is not bytes:
        raise TypeError("digest source must be bytes")
    return "sha256:" + sha256(source).hexdigest()


def _sha256(value: object, subject: str) -> str:
    if not isinstance(value, str) or _DIGEST.fullmatch(value) is None:
        _refuse(f"{subject} must be a lowercase sha256 digest")
    return value


def _text(value: object, subject: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _refuse(f"{subject} must be nonblank text")
    return value


def _timestamp(value: object, subject: str) -> datetime:
    text = _text(value, subject)
    if _TIMESTAMP.fullmatch(text) is None:
        _refuse(f"{subject} must be an RFC 3339 UTC second timestamp")
    return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")


def _string_array(value: object, subject: str) -> list[str]:
    values = _array(value, subject)
    if any(not isinstance(item, str) or not item.strip() for item in values):
        _refuse(f"{subject} must contain only nonblank text")
    if len(values) != len(set(values)):
        _refuse(f"{subject} must not contain duplicates")
    return values


def _protocol_version(protocol_source: bytes) -> str:
    """Read the version a protocol file declares, and refuse any other."""

    root = _object(_json(protocol_source, "review protocol"), "review protocol")
    schema = root.get("schema")
    if schema == PROTOCOL_SCHEMA:
        return "v2"
    if schema == PROTOCOL_SCHEMA_V3:
        return "v3"
    _refuse("review protocol declares no version this validator accepts")
    raise AssertionError("unreachable")


def validate_protocol(protocol_source: bytes) -> dict[str, Any]:
    """Accept a frozen review protocol of a version this validator carries."""

    if _protocol_version(protocol_source) == "v3":
        return _validate_protocol_v3(protocol_source)
    return _validate_protocol_v2(protocol_source)


def _validate_protocol_v2(protocol_source: bytes) -> dict[str, Any]:
    """Accept only the protocol frozen before the v4 producer ran."""

    root = _object(_json(protocol_source, "review protocol"), "review protocol")
    if root.get("schema") != PROTOCOL_SCHEMA or root.get("status") != PROTOCOL_STATUS:
        _refuse("review protocol is not the frozen v4 protocol")
    if root["purpose"] != ["SOURCE_SUPPORT", "QUESTION_RESPONSIVENESS"]:
        _refuse("review protocol purpose differs")
    if root["evidence_surface"]["authoritative"] != "SELECTED_READING_TEXT_LAYER":
        _refuse("review protocol must declare one authoritative evidence surface")
    if root["evidence_surface"]["locator_kind"] != "SELECTED_READING_BLOCK_ID":
        _refuse("review protocol must locate evidence by reading block")
    fixed = _object(root["fixed_identities"], "review protocol.fixed_identities")
    _exact_keys(fixed, _FIXED_IDENTITY_KEYS, "review protocol.fixed_identities")
    for field, value in fixed.items():
        _sha256(value, f"review protocol.fixed_identities.{field}")
    _string_array(root["question_ids"], "review protocol.question_ids")
    authorship = _object(root["authorship"], "review protocol.authorship")
    if authorship["preliminary_evaluator_kind"] not in PRELIMINARY_EVALUATOR_KINDS:
        _refuse("review protocol preliminary evaluator kind is unknown")
    if (
        authorship["ratifier_evaluator_kind"] != "HUMAN_AUTHOR"
        or authorship["ratifier_actor_id"] != "actor:luis"
    ):
        _refuse("review protocol must name the human ratifier")
    _string_array(
        root["forbidden_record_fields"], "review protocol.forbidden_record_fields"
    )
    return root


def _authorship(
    manifest: Mapping[str, Any], protocol: Mapping[str, Any]
) -> dict[str, Any]:
    authorship = _object(manifest["authorship"], "review input manifest.authorship")
    declared = authorship.get("preliminary_evaluator_kind")
    if declared not in PRELIMINARY_EVALUATOR_KINDS:
        _refuse("review input manifest preliminary evaluator kind is unknown")
    if (
        authorship.get("ratifier_evaluator_kind")
        != protocol["authorship"]["ratifier_evaluator_kind"]
        or authorship.get("ratifier_actor_id")
        != protocol["authorship"]["ratifier_actor_id"]
    ):
        _refuse("review input manifest must keep the protocol's human ratifier")

    frozen = protocol["authorship"]["preliminary_evaluator_kind"]
    if declared == frozen:
        if "deviation" in authorship:
            _refuse("review input manifest records a deviation it does not take")
        return authorship
    if "deviation" not in authorship:
        _refuse(
            "a preliminary evaluator kind other than the protocol's requires a"
            " recorded deviation"
        )
    deviation = _object(authorship["deviation"], "review input manifest.deviation")
    _exact_keys(deviation, _DEVIATION_KEYS, "review input manifest.deviation")
    if deviation["from"] != frozen or deviation["to"] != declared:
        _refuse("recorded deviation does not describe the substitution taken")
    if deviation["protocol_edited"] is not False:
        _refuse("the frozen review protocol must not be edited")
    _text(deviation["reason"], "review input manifest.deviation.reason")
    return authorship


def validate_review_input_manifest(
    manifest_source: bytes, protocol_source: bytes
) -> dict[str, Any]:
    """Accept a frozen manifest that binds every review input by digest."""

    if _protocol_version(protocol_source) == "v3":
        return _validate_manifest_v3(manifest_source, protocol_source)
    return _validate_manifest_v2(manifest_source, protocol_source)


def _validate_manifest_v2(
    manifest_source: bytes, protocol_source: bytes
) -> dict[str, Any]:
    protocol = validate_protocol(protocol_source)
    root = _object(
        _json(manifest_source, "review input manifest"), "review input manifest"
    )
    _exact_keys(
        root,
        {
            "authorship",
            "fixed_identities",
            "materials",
            "review_protocol_sha256",
            "rows_per_question",
            "run_id",
            "schema",
            "stage_identities",
            "status",
        },
        "review input manifest",
    )
    if root["schema"] != MANIFEST_SCHEMA:
        _refuse("review input manifest schema differs")
    if root["status"] != FROZEN_MANIFEST_STATUS:
        _refuse("review input manifest must be frozen before review")
    if root["review_protocol_sha256"] != _digest(protocol_source):
        _refuse("review input manifest does not bind the supplied protocol")
    _text(root["run_id"], "review input manifest.run_id")

    fixed = _object(root["fixed_identities"], "review input manifest.fixed_identities")
    if fixed != protocol["fixed_identities"]:
        _refuse("review input manifest fixed identities differ from the protocol")
    stage = _object(root["stage_identities"], "review input manifest.stage_identities")
    _exact_keys(stage, _STAGE_IDENTITY_KEYS, "review input manifest.stage_identities")
    for field, value in stage.items():
        _sha256(value, f"review input manifest.stage_identities.{field}")

    materials = _array(root["materials"], "review input manifest.materials")
    names = [item["name"] for item in materials]
    if names != protocol["review_materials"]:
        _refuse("review input manifest materials differ from the protocol")
    for index, raw in enumerate(materials):
        item = _object(raw, f"review input manifest.materials[{index}]")
        _exact_keys(item, _MATERIAL_KEYS, f"review input manifest.materials[{index}]")
        _text(item["path"], f"review input manifest.materials[{index}].path")
        _sha256(item["sha256"], f"review input manifest.materials[{index}].sha256")
        if item["visibility"] not in {"PUBLIC", "PRIVATE"}:
            _refuse(f"review input manifest.materials[{index}].visibility is unknown")

    rows = _object(root["rows_per_question"], "review input manifest.rows_per_question")
    if sorted(rows) != sorted(protocol["question_ids"]):
        _refuse("review input manifest row counts do not cover every question")
    for question_id, count in rows.items():
        if type(count) is not int or count < 0:
            _refuse(f"review input manifest row count for {question_id} is not a count")
    _authorship(root, protocol)
    return root


def _markdown_record(source: bytes) -> dict[str, Any]:
    if type(source) is not bytes:
        raise TypeError("review record source must be bytes")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReviewRefusal("review record must be UTF-8 Markdown") from error
    blocks = list(_JSON_BLOCK.finditer(text))
    if len(blocks) != 1:
        _refuse("review record must contain exactly one fenced JSON block")
    return _object(
        _json(blocks[0].group("record").encode("utf-8"), "review JSON"), "review"
    )


def _reject_forbidden_fields(
    value: object, forbidden: set[str], subject: str = "review"
) -> None:
    if type(value) is dict:
        for key, child in value.items():
            if key.casefold() in forbidden:
                _refuse(f"{subject} contains forbidden field {key!r}")
            _reject_forbidden_fields(child, forbidden, f"{subject}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            _reject_forbidden_fields(child, forbidden, f"{subject}[{index}]")


def _record_root(
    record_source: bytes,
    protocol: Mapping[str, Any],
    manifest: Mapping[str, Any],
    protocol_digest: str,
) -> dict[str, Any]:
    root = _markdown_record(record_source)
    _exact_keys(
        root,
        {"inputs", "preliminary", "questions", "ratification", "schema", "status"},
        "review",
    )
    if root["schema"] != REVIEW_SCHEMA:
        _refuse("review schema differs")
    if root["status"] not in _REVIEW_STATUSES:
        _refuse("review status differs")
    forbidden = {value.casefold() for value in protocol["forbidden_record_fields"]}
    _reject_forbidden_fields(root, forbidden)
    inputs = _object(root["inputs"], "review.inputs")
    _exact_keys(
        inputs,
        {"review_input_manifest_sha256", "review_protocol_sha256"},
        "review.inputs",
    )
    if inputs["review_protocol_sha256"] != protocol_digest:
        _refuse("review does not bind the supplied protocol")

    preliminary = _object(root["preliminary"], "review.preliminary")
    _exact_keys(
        preliminary,
        {"actor_id", "completed_at", "evaluator_kind"},
        "review.preliminary",
    )
    declared = manifest["authorship"]["preliminary_evaluator_kind"]
    if preliminary["evaluator_kind"] != declared:
        _refuse(
            "review preliminary evaluator kind must be the one the input manifest"
            f" declares: {declared}"
        )
    ratification = _object(root["ratification"], "review.ratification")
    _exact_keys(
        ratification,
        {"actor_id", "completed_at", "disposition", "evaluator_kind", "notes"},
        "review.ratification",
    )
    if (
        ratification["evaluator_kind"]
        != manifest["authorship"]["ratifier_evaluator_kind"]
        or ratification["actor_id"] != manifest["authorship"]["ratifier_actor_id"]
    ):
        _refuse("ratification must identify the declared human author")
    return root


def validate_blank_review(
    record_source: bytes, protocol_source: bytes, manifest_source: bytes
) -> dict[str, Any]:
    """Validate the template without accepting it as a review."""

    if _protocol_version(protocol_source) == "v3":
        return _validate_blank_v3(record_source, protocol_source, manifest_source)
    return _validate_blank_v2(record_source, protocol_source, manifest_source)


def _validate_blank_v2(
    record_source: bytes, protocol_source: bytes, manifest_source: bytes
) -> dict[str, Any]:
    protocol = validate_protocol(protocol_source)
    manifest = validate_review_input_manifest(manifest_source, protocol_source)
    root = _record_root(record_source, protocol, manifest, _digest(protocol_source))
    if root["status"] != "BLANK":
        _refuse("blank review status must be BLANK")
    if root["inputs"]["review_input_manifest_sha256"] != "":
        _refuse("blank review must not bind a stage manifest")
    if root["preliminary"]["actor_id"] or root["preliminary"]["completed_at"]:
        _refuse("blank review preliminary authorship must remain empty")
    ratification = root["ratification"]
    if ratification["disposition"] != "PENDING" or any(
        ratification[field] for field in ("completed_at", "notes")
    ):
        _refuse("blank review human ratification must remain pending")

    questions = _array(root["questions"], "review.questions")
    if [item["question_id"] for item in questions] != protocol["question_ids"]:
        _refuse("blank review questions differ from the protocol")
    for index, raw in enumerate(questions):
        question = _object(raw, f"review.questions[{index}]")
        _exact_keys(question, _QUESTION_KEYS, f"review.questions[{index}]")
        if question["question_responsiveness"] != "PENDING":
            _refuse(f"blank review question {index} must carry no judgment")
        if question["rows"] != [] or question["source_locators"] != []:
            _refuse(f"blank review question {index} must carry no row or locator")
        if question["responsiveness_rationale"] != "":
            _refuse(f"blank review question {index} must carry no rationale")
    return root


def _reading_blocks(source: bytes, fixed: Mapping[str, Any]) -> set[str]:
    if _digest(source) != fixed["selected_reading_sha256"]:
        _refuse("selected reading differs from the frozen protocol")
    root = _object(_json(source, "selected reading"), "selected reading")
    if root.get("source_sha256") != fixed["source_sha256"]:
        _refuse("selected reading does not bind the frozen source")
    block_ids = [
        _text(block.get("id"), "selected reading block id")
        for page in _array(root.get("pages"), "selected reading.pages")
        for block in _array(page.get("blocks"), "selected reading page blocks")
    ]
    if len(block_ids) != len(set(block_ids)):
        _refuse("selected reading block ids must be unique")
    return set(block_ids)


def _query_rows(source: bytes, manifest: Mapping[str, Any]) -> dict[str, int]:
    stage = manifest["stage_identities"]
    if _digest(source) != stage["query_result_sha256"]:
        _refuse("query result differs from the frozen review inputs")
    result = _object(_json(source, "query result"), "query result")
    if result.get("schema") not in QUERY_RESULT_SCHEMAS:
        _refuse("query result schema differs")
    if result["inputs"]["query_binding_sha256"] != stage["query_binding_sha256"]:
        _refuse("query result does not bind the frozen query binding")
    if result["inputs"]["replay_receipt_sha256"] != stage["replay_receipt_sha256"]:
        _refuse("query result does not bind the frozen replay receipt")
    if result["inputs"]["ledger_head"] != stage["ledger_head"]:
        _refuse("query result does not bind the frozen ledger head")
    if result["forbidden_attempts"] != {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }:
        _refuse("query result records a forbidden access attempt")
    rows: dict[str, int] = {}
    for index, raw in enumerate(_array(result["queries"], "query result.queries")):
        query = _object(raw, f"query result.queries[{index}]")
        question_id = _text(query["question_id"], "query result question id")
        if question_id in rows:
            _refuse("query result question ids must be unique")
        rows[question_id] = len(_array(query["rows"], "query result rows"))
    if rows != manifest["rows_per_question"]:
        _refuse("query result row counts differ from the frozen review inputs")
    return rows


def _authorship_state(
    root: Mapping[str, Any], *, require_human_ratification: bool
) -> None:
    preliminary = root["preliminary"]
    _text(preliminary["actor_id"], "review.preliminary.actor_id")
    preliminary_at = _timestamp(
        preliminary["completed_at"], "review.preliminary.completed_at"
    )
    ratification = root["ratification"]
    status = root["status"]

    if status == "PRELIMINARY_COMPLETE":
        if ratification["disposition"] != "PENDING" or any(
            ratification[field] for field in ("completed_at", "notes")
        ):
            _refuse("preliminary review must leave human ratification pending")
    elif status in {"HUMAN_RATIFIED", "HUMAN_REJECTED"}:
        expected = (
            _RATIFIED_DISPOSITIONS if status == "HUMAN_RATIFIED" else {"REJECTED"}
        )
        if ratification["disposition"] not in expected:
            _refuse(f"{status} requires a matching disposition")
        ratification_at = _timestamp(
            ratification["completed_at"], "review.ratification.completed_at"
        )
        _text(ratification["notes"], "review.ratification.notes")
        if ratification_at < preliminary_at:
            _refuse("human ratification cannot precede the preliminary review")
    else:
        _refuse("completed review cannot retain BLANK status")
    if require_human_ratification and status != "HUMAN_RATIFIED":
        _refuse("human ratification is required for paper evidence")


def _questions(
    root: Mapping[str, Any],
    protocol: Mapping[str, Any],
    rows_per_question: Mapping[str, int],
    block_ids: set[str],
) -> None:
    questions = _array(root["questions"], "review.questions")
    if [item["question_id"] for item in questions] != protocol["question_ids"]:
        _refuse("review questions differ from the protocol")
    allowed_support = set(protocol["judgments"]["source_support"])
    allowed_responsiveness = set(protocol["judgments"]["question_responsiveness"])

    for index, raw in enumerate(questions):
        subject = f"review.questions[{index}]"
        question = _object(raw, subject)
        _exact_keys(question, _QUESTION_KEYS, subject)
        if question["question_responsiveness"] not in allowed_responsiveness:
            _refuse(f"{subject}.question_responsiveness is not an allowed judgment")
        _text(
            question["responsiveness_rationale"], f"{subject}.responsiveness_rationale"
        )
        locators = _string_array(
            question["source_locators"], f"{subject}.source_locators"
        )
        if not locators:
            _refuse(f"{subject}.source_locators must cite at least one reading block")
        unknown = sorted(set(locators) - block_ids)
        if unknown:
            _refuse(f"{subject}.source_locators contain unknown blocks {unknown}")

        rows = _array(question["rows"], f"{subject}.rows")
        expected = rows_per_question[question["question_id"]]
        if [item.get("row_index") for item in rows] != list(range(expected)):
            _refuse(f"{subject}.rows must judge every returned row in order")
        for row_index, raw_row in enumerate(rows):
            row_subject = f"{subject}.rows[{row_index}]"
            row = _object(raw_row, row_subject)
            _exact_keys(row, _ROW_KEYS, row_subject)
            if row["source_support"] not in allowed_support:
                _refuse(f"{row_subject}.source_support is not an allowed judgment")
            _text(row["rationale"], f"{row_subject}.rationale")
            row_locators = _string_array(
                row["source_locators"], f"{row_subject}.source_locators"
            )
            unknown = sorted(set(row_locators) - block_ids)
            if unknown:
                _refuse(
                    f"{row_subject}.source_locators contain unknown blocks {unknown}"
                )
            if not row_locators and row["source_support"] != "NOT_EVALUABLE":
                _refuse(f"{row_subject} must cite a reading block or be NOT_EVALUABLE")


def validate_review(
    record_source: bytes,
    protocol_source: bytes,
    *,
    review_input_manifest_source: bytes,
    query_result_source: bytes,
    selected_reading_source: bytes | None = None,
    competency_questions_source: bytes | None = None,
    surface_sources: Mapping[str, bytes] | None = None,
    require_human_ratification: bool = False,
    findings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate identities, references and authorship, never a judgment.

    `selected_reading_source` is required by v2 and by a v3 cell whose declared
    surface is the text layer. `competency_questions_source` and
    `surface_sources` are v3 inputs: the first carries the required semantics
    coverage is read against, the second the bytes a row locator is opened in.
    `findings` collects the control outcomes, which refuse nothing.
    """

    if _protocol_version(protocol_source) == "v3":
        return _validate_review_v3(
            record_source,
            protocol_source,
            review_input_manifest_source=review_input_manifest_source,
            query_result_source=query_result_source,
            selected_reading_source=selected_reading_source,
            competency_questions_source=competency_questions_source,
            surface_sources=surface_sources,
            require_human_ratification=require_human_ratification,
            findings=findings,
        )
    if selected_reading_source is None:
        _refuse("the v2 protocol requires the selected reading")
    return _validate_review_v2(
        record_source,
        protocol_source,
        review_input_manifest_source=review_input_manifest_source,
        query_result_source=query_result_source,
        selected_reading_source=selected_reading_source,
        require_human_ratification=require_human_ratification,
    )


def _validate_review_v2(
    record_source: bytes,
    protocol_source: bytes,
    *,
    review_input_manifest_source: bytes,
    query_result_source: bytes,
    selected_reading_source: bytes,
    require_human_ratification: bool = False,
) -> dict[str, Any]:
    protocol = validate_protocol(protocol_source)
    manifest = validate_review_input_manifest(
        review_input_manifest_source, protocol_source
    )
    root = _record_root(record_source, protocol, manifest, _digest(protocol_source))
    if root["status"] == "BLANK":
        _refuse("blank review is not a completed review")
    if root["inputs"]["review_input_manifest_sha256"] != _digest(
        review_input_manifest_source
    ):
        _refuse("review input-manifest identity differs from the supplied manifest")

    block_ids = _reading_blocks(selected_reading_source, manifest["fixed_identities"])
    rows_per_question = _query_rows(query_result_source, manifest)
    _authorship_state(root, require_human_ratification=require_human_ratification)
    _questions(root, protocol, rows_per_question, block_ids)
    return root


# ---------------------------------------------------------------------------
# Protocol v3: a declared evidence surface, resolved locators, derived coverage
# ---------------------------------------------------------------------------


def _enum(value: object, allowed: tuple[str, ...], subject: str) -> str:
    if value not in allowed:
        _refuse(f"{subject} must be one of {list(allowed)}")
    return value  # type: ignore[return-value]


def _validate_protocol_v3(protocol_source: bytes) -> dict[str, Any]:
    """Accept the v3 protocol: it declares kinds, not one cell's surface."""

    root = _object(_json(protocol_source, "review protocol"), "review protocol")
    if root.get("status") != PROTOCOL_STATUS_V3:
        _refuse("review protocol v3 is not frozen")
    if root["purpose"] != ["SOURCE_SUPPORT", "SEMANTIC_COVERAGE"]:
        _refuse("review protocol purpose differs")

    surface = _object(root["evidence_surface"], "review protocol.evidence_surface")
    if surface["declared_by"] != "REVIEW_INPUT_MANIFEST":
        _refuse("review protocol v3 must leave the evidence surface to the manifest")
    kinds = _object(surface["surface_kinds"], "review protocol.surface_kinds")
    if set(kinds) != set(SURFACE_LOCATOR_KINDS):
        _refuse("review protocol must declare exactly the two evidence surfaces")
    for kind, declared in kinds.items():
        if _object(declared, f"review protocol.surface_kinds.{kind}")[
            "locator_kind"
        ] != SURFACE_LOCATOR_KINDS[kind]:
            _refuse(f"review protocol surface {kind} declares the wrong locator kind")

    judgments = _object(root["judgments"], "review protocol.judgments")
    if judgments["source_support"] != list(_SOURCE_SUPPORT_V2):
        _refuse("review protocol v3 must keep the v2 source-support judgments")
    if judgments["row_resolution"] != list(ROW_RESOLUTIONS):
        _refuse("review protocol row resolution tokens differ")
    if judgments["coverage_absent_reasons"] != list(COVERAGE_ABSENT_REASONS):
        _refuse("review protocol coverage absent reasons differ")
    if judgments["question_responsiveness"] != list(COVERAGE_LABELS):
        _refuse("review protocol question responsiveness labels differ")
    if judgments["question_responsiveness_is"] != "DERIVED_BY_THE_VALIDATOR":
        _refuse("review protocol v3 must derive the responsiveness label")
    if judgments["assembly"] != list(ASSEMBLY_DESCRIPTORS):
        _refuse("review protocol assembly descriptors differ")
    if judgments["assembly_is"] != "A_DESCRIPTOR_NEVER_A_GRADE":
        _refuse("review protocol assembly must never be a grade")

    controls = _object(root["controls"], "review protocol.controls")
    if set(controls["kinds"]) != set(CONTROL_KINDS):
        _refuse("review protocol control kinds differ")
    if controls["validator_behaviour"] != (
        "REPORTS_EACH_CONTROL_OUTCOME_AS_A_FINDING_AND_REFUSES_NOTHING"
    ):
        _refuse("review protocol controls must refuse nothing")

    identities = _object(root["fixed_identities"], "review protocol.fixed_identities")
    by_kind = _object(
        identities["required_keys_by_surface_kind"],
        "review protocol.fixed_identities.required_keys_by_surface_kind",
    )
    if set(by_kind) != set(SURFACE_LOCATOR_KINDS):
        _refuse("review protocol must fix identities for both surfaces")
    for kind, keys in by_kind.items():
        _string_array(keys, f"review protocol.fixed_identities.{kind}")
    stage = _object(root["stage_identities"], "review protocol.stage_identities")
    if set(_string_array(stage["required_keys"], "review protocol.stage_identities")) != (
        _STAGE_IDENTITY_KEYS
    ):
        _refuse("review protocol stage identities differ from the v2 set")

    materials = _object(root["review_materials"], "review protocol.review_materials")
    required = _object(materials["required"], "review protocol.review_materials")
    if set(required) != set(SURFACE_LOCATOR_KINDS):
        _refuse("review protocol must name required materials for both surfaces")
    for kind, names in required.items():
        _string_array(names, f"review protocol.review_materials.{kind}")
    if materials["sources_are_materials"] is not True:
        _refuse("review protocol must bind every declared source as a material")

    authorship = _object(root["authorship"], "review protocol.authorship")
    if authorship["preliminary_evaluator_kind"] not in PRELIMINARY_EVALUATOR_KINDS:
        _refuse("review protocol preliminary evaluator kind is unknown")
    if (
        authorship["ratifier_evaluator_kind"] != "HUMAN_AUTHOR"
        or authorship["ratifier_actor_id"] != "actor:luis"
    ):
        _refuse("review protocol must name the human ratifier")
    _string_array(
        root["forbidden_record_fields"], "review protocol.forbidden_record_fields"
    )
    _string_array(root["withheld_from_producer"], "review protocol.withheld_from_producer")
    return root


_SOURCE_SUPPORT_V2 = ("SUPPORTED", "PARTIAL", "UNSUPPORTED", "NOT_EVALUABLE")


def _surface(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return manifest["evidence_surface"]


def _sources_by_id(manifest: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    surface = _surface(manifest)
    return {item["source_id"]: item for item in surface.get("sources", [])}


def _validate_manifest_v3(
    manifest_source: bytes, protocol_source: bytes
) -> dict[str, Any]:
    """Accept a frozen manifest that declares its own evidence surface."""

    protocol = validate_protocol(protocol_source)
    root = _object(
        _json(manifest_source, "review input manifest"), "review input manifest"
    )
    _exact_keys(root, _MANIFEST_KEYS_V3, "review input manifest")
    if root["schema"] != MANIFEST_SCHEMA_V3:
        _refuse("review input manifest schema is not the v3 schema the protocol needs")
    if root["status"] != FROZEN_MANIFEST_STATUS:
        _refuse("review input manifest must be frozen before review")
    if root["review_protocol_sha256"] != _digest(protocol_source):
        _refuse("review input manifest does not bind the supplied protocol")
    _text(root["run_id"], "review input manifest.run_id")

    surface = _object(root["evidence_surface"], "review input manifest.evidence_surface")
    kind = surface.get("kind")
    if kind not in SURFACE_LOCATOR_KINDS:
        _refuse("review input manifest declares an evidence surface kind nobody froze")
    if surface.get("locator_kind") != SURFACE_LOCATOR_KINDS[kind]:
        _refuse(f"an evidence surface of kind {kind} carries the wrong locator kind")

    if kind == "STRUCTURED_ROWS":
        _exact_keys(
            surface,
            {"kind", "locator_convention", "locator_kind", "sources"},
            "review input manifest.evidence_surface",
        )
        convention = _object(
            surface["locator_convention"],
            "review input manifest.evidence_surface.locator_convention",
        )
        _exact_keys(
            convention,
            _CONVENTION_KEYS,
            "review input manifest.evidence_surface.locator_convention",
        )
        if convention["form"] != "SOURCE_ID_HASH_ROW_FIELD":
            _refuse("the declared locator form is not one this validator resolves")
        if convention["first_row_index"] not in (0, 1):
            _refuse("the declared convention must say which line is the first row")
        if type(convention["csv_header_is_a_row"]) is not bool:
            _refuse("the declared convention must say whether a CSV header is a row")
        sources = _array(
            surface["sources"], "review input manifest.evidence_surface.sources"
        )
        if not sources:
            _refuse("a row surface must declare at least one source")
        seen: set[str] = set()
        for index, raw in enumerate(sources):
            subject = f"review input manifest.evidence_surface.sources[{index}]"
            item = _object(raw, subject)
            _exact_keys(item, _SOURCE_KEYS, subject)
            source_id = _text(item["source_id"], f"{subject}.source_id")
            if source_id in seen:
                _refuse(f"{subject}.source_id is declared twice")
            seen.add(source_id)
            _text(item["path"], f"{subject}.path")
            _sha256(item["sha256"], f"{subject}.sha256")
            _enum(item["format"], SOURCE_FORMATS, f"{subject}.format")
    else:
        _exact_keys(
            surface, {"kind", "locator_kind"}, "review input manifest.evidence_surface"
        )

    fixed = _object(root["fixed_identities"], "review input manifest.fixed_identities")
    expected_keys = set(
        protocol["fixed_identities"]["required_keys_by_surface_kind"][kind]
    )
    _exact_keys(fixed, expected_keys, "review input manifest.fixed_identities")
    _sha256(
        fixed["competency_questions_sha256"],
        "review input manifest.fixed_identities.competency_questions_sha256",
    )
    if kind == "STRUCTURED_ROWS":
        declared = _object(
            fixed["source_sha256"],
            "review input manifest.fixed_identities.source_sha256",
        )
        if declared != {
            item["source_id"]: item["sha256"] for item in surface["sources"]
        }:
            _refuse("the fixed source identities differ from the declared sources")
    else:
        _sha256(
            fixed["source_sha256"],
            "review input manifest.fixed_identities.source_sha256",
        )
        _sha256(
            fixed["selected_reading_sha256"],
            "review input manifest.fixed_identities.selected_reading_sha256",
        )

    stage = _object(root["stage_identities"], "review input manifest.stage_identities")
    _exact_keys(stage, _STAGE_IDENTITY_KEYS, "review input manifest.stage_identities")
    for field, value in stage.items():
        _sha256(value, f"review input manifest.stage_identities.{field}")

    materials = _array(root["materials"], "review input manifest.materials")
    names: list[str] = []
    for index, raw in enumerate(materials):
        item = _object(raw, f"review input manifest.materials[{index}]")
        _exact_keys(item, _MATERIAL_KEYS, f"review input manifest.materials[{index}]")
        names.append(_text(item["name"], f"review input manifest.materials[{index}].name"))
        _text(item["path"], f"review input manifest.materials[{index}].path")
        _sha256(item["sha256"], f"review input manifest.materials[{index}].sha256")
        if item["visibility"] not in {"PUBLIC", "PRIVATE"}:
            _refuse(f"review input manifest.materials[{index}].visibility is unknown")
    if len(names) != len(set(names)):
        _refuse("review input manifest materials must be named once each")
    missing = sorted(
        set(protocol["review_materials"]["required"][kind]) - set(names)
    )
    if missing:
        _refuse(f"review input manifest is missing required materials {missing}")
    bound = {(item["path"], item["sha256"]) for item in materials}
    for item in _surface(root).get("sources", []):
        if (item["path"], item["sha256"]) not in bound:
            _refuse(
                f"declared source {item['source_id']} is not bound as a material"
            )

    question_ids = _string_array(root["question_ids"], "review input manifest.question_ids")
    if not question_ids:
        _refuse("review input manifest must name the cell's questions")
    rows = _object(root["rows_per_question"], "review input manifest.rows_per_question")
    if sorted(rows) != sorted(question_ids):
        _refuse("review input manifest row counts do not cover every question")
    for question_id, count in rows.items():
        if type(count) is not int or count < 0:
            _refuse(f"review input manifest row count for {question_id} is not a count")
    traced = root["witnesses_traced"]
    if type(traced) is not int or traced < 0:
        _refuse("review input manifest witnesses_traced is not a count")
    _authorship(root, protocol)
    return root


def _question_file(source: bytes) -> list[dict[str, Any]]:
    """Read the questions and their required semantics; controls are optional."""

    root = _object(_json(source, "competency questions"), "competency questions")
    if root.get("schema") not in QUESTION_FILE_SCHEMAS:
        _refuse("competency question file schema differs")
    questions: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw in enumerate(_array(root["questions"], "competency questions.questions")):
        subject = f"competency questions.questions[{index}]"
        question = _object(raw, subject)
        question_id = _text(question["id"], f"{subject}.id")
        semantics = _string_array(
            question["required_semantics"], f"{subject}.required_semantics"
        )
        if not semantics:
            _refuse(f"{subject}.required_semantics must name at least one item")
        ids.append(question_id)
        questions.append(question)
    if len(ids) != len(set(ids)):
        _refuse("competency question ids must be unique")
    for question in questions:
        expected = question.get("expected_outcome")
        if expected is None:
            continue
        subject = f"competency questions.{question['id']}.expected_outcome"
        expected = _object(expected, subject)
        kind = _enum(expected.get("kind"), CONTROL_KINDS, f"{subject}.kind")
        if kind == "PARAPHRASE":
            named = _text(expected.get("of"), f"{subject}.of")
            if named not in ids:
                _refuse(f"{subject}.of names a question the file does not carry")
        elif "of" in expected:
            _refuse(f"{subject}.of is meaningless for a {kind} control")
    return questions


def derived_responsiveness(coverage: list[Mapping[str, Any]]) -> str:
    """COVERED when every semantic names a row, NONE when none does, else PARTIAL."""

    if not coverage:
        _refuse("coverage must carry one entry per required semantic")
    named = [item for item in coverage if item.get("row_index") is not None]
    if len(named) == len(coverage):
        return "COVERED"
    if not named:
        return "NONE"
    return "PARTIAL"


def control_outcomes(
    record: Mapping[str, Any], competency_questions_source: bytes
) -> list[dict[str, Any]]:
    """Report each control's outcome. This refuses nothing and grades nothing."""

    questions = _question_file(competency_questions_source)
    observed = {
        question["question_id"]: derived_responsiveness(question["coverage"])
        for question in record["questions"]
    }
    findings: list[dict[str, Any]] = []
    for question in questions:
        expected_outcome = question.get("expected_outcome")
        if expected_outcome is None:
            continue
        question_id = question["id"]
        kind = expected_outcome["kind"]
        finding: dict[str, Any] = {"question_id": question_id, "kind": kind}
        if kind == "PARAPHRASE":
            finding["of"] = expected_outcome["of"]
            expected = observed.get(expected_outcome["of"])
        else:
            expected = "NONE"
        finding["expected"] = expected
        finding["observed"] = observed.get(question_id)
        finding["matched"] = (
            expected is not None
            and finding["observed"] is not None
            and expected == finding["observed"]
        )
        findings.append(finding)
    return findings


def _field_resolves(value: object, field: str) -> bool:
    for part in field.split("."):
        name, bracket, rest = part.partition("[")
        if type(value) is not dict or name not in value:
            return False
        value = value[name]
        if bracket:
            for token in _BRACKET.findall(bracket + rest):
                index = int(token)
                if type(value) is not list or index >= len(value):
                    return False
                value = value[index]
    return True


def _source_rows(source_bytes: bytes, descriptor: Mapping[str, Any], convention: Mapping[str, Any]):
    """The row sequence of one source under the declared convention."""

    try:
        text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReviewRefusal("a declared source is not UTF-8") from error
    if descriptor["format"] == "JSONL":
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
        return rows, None
    parsed = [row for row in csv.reader(io.StringIO(text)) if row]
    if not parsed:
        _refuse(f"declared source {descriptor['source_id']} carries no rows")
    header = parsed[0]
    rows = parsed if convention["csv_header_is_a_row"] else parsed[1:]
    return rows, header


def _row_locator_resolves(
    locator: str,
    sources: Mapping[str, dict[str, Any]],
    source_bytes: Mapping[str, bytes],
    convention: Mapping[str, Any],
    subject: str,
) -> bool:
    match = _ROW_LOCATOR.fullmatch(locator)
    if match is None:
        _refuse(
            f"{subject} locator {locator!r} is not of the declared form"
            " <source_id>#row:N:field"
        )
    assert match is not None
    source_id = match["source"]
    if source_id not in sources:
        _refuse(f"{subject} names a source the manifest does not declare: {source_id}")
    rows, header = _source_rows(
        source_bytes[source_id], sources[source_id], convention
    )
    index = int(match["row"]) - convention["first_row_index"]
    if index < 0 or index >= len(rows):
        return False
    entry = rows[index]
    field = match["field"]
    if header is not None:
        if field not in header:
            return False
        return header.index(field) < len(entry)
    return _field_resolves(entry, field)


def _query_witnesses(
    source: bytes, manifest: Mapping[str, Any]
) -> dict[str, list[str]]:
    """The witness of every returned row, in order, checked against the manifest."""

    stage = manifest["stage_identities"]
    if _digest(source) != stage["query_result_sha256"]:
        _refuse("query result differs from the frozen review inputs")
    result = _object(_json(source, "query result"), "query result")
    if result.get("schema") not in QUERY_RESULT_SCHEMAS:
        _refuse("query result schema differs")
    if result["inputs"]["query_binding_sha256"] != stage["query_binding_sha256"]:
        _refuse("query result does not bind the frozen query binding")
    if result["inputs"]["replay_receipt_sha256"] != stage["replay_receipt_sha256"]:
        _refuse("query result does not bind the frozen replay receipt")
    if result["inputs"]["ledger_head"] != stage["ledger_head"]:
        _refuse("query result does not bind the frozen ledger head")
    if result["forbidden_attempts"] != {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }:
        _refuse("query result records a forbidden access attempt")

    witnesses: dict[str, list[str]] = {}
    for index, raw in enumerate(_array(result["queries"], "query result.queries")):
        query = _object(raw, f"query result.queries[{index}]")
        question_id = _text(query["question_id"], "query result question id")
        if question_id in witnesses:
            _refuse("query result question ids must be unique")
        keys: list[str] = []
        for position, row in enumerate(_array(query["rows"], "query result rows")):
            witness = _object(row["witness"], f"query result row {position} witness")
            key = witness.get("relation_id") or witness.get("record_id")
            keys.append(_text(key, f"query result row {position} witness identity"))
        witnesses[question_id] = keys
    if {key: len(value) for key, value in witnesses.items()} != manifest[
        "rows_per_question"
    ]:
        _refuse("query result row counts differ from the frozen review inputs")
    distinct = {key for keys in witnesses.values() for key in keys}
    if len(distinct) != manifest["witnesses_traced"]:
        _refuse("query result witness count differs from the frozen review inputs")
    return witnesses


def _record_root_v3(
    record_source: bytes,
    protocol: Mapping[str, Any],
    manifest: Mapping[str, Any],
    protocol_digest: str,
) -> dict[str, Any]:
    root = _markdown_record(record_source)
    _exact_keys(root, _RECORD_KEYS_V3, "review")
    if root["schema"] != REVIEW_SCHEMA_V3:
        _refuse("review schema is not the v3 schema the protocol needs")
    if root["status"] not in _REVIEW_STATUSES:
        _refuse("review status differs")
    forbidden = {value.casefold() for value in protocol["forbidden_record_fields"]}
    _reject_forbidden_fields(root, forbidden)
    inputs = _object(root["inputs"], "review.inputs")
    _exact_keys(
        inputs,
        {"review_input_manifest_sha256", "review_protocol_sha256"},
        "review.inputs",
    )
    if inputs["review_protocol_sha256"] != protocol_digest:
        _refuse("review does not bind the supplied protocol")

    preliminary = _object(root["preliminary"], "review.preliminary")
    _exact_keys(
        preliminary, {"actor_id", "completed_at", "evaluator_kind"}, "review.preliminary"
    )
    declared = manifest["authorship"]["preliminary_evaluator_kind"]
    if preliminary["evaluator_kind"] != declared:
        _refuse(
            "review preliminary evaluator kind must be the one the input manifest"
            f" declares: {declared}"
        )
    ratification = _object(root["ratification"], "review.ratification")
    _exact_keys(
        ratification,
        {"actor_id", "completed_at", "disposition", "evaluator_kind", "notes"},
        "review.ratification",
    )
    if (
        ratification["evaluator_kind"]
        != manifest["authorship"]["ratifier_evaluator_kind"]
        or ratification["actor_id"] != manifest["authorship"]["ratifier_actor_id"]
    ):
        _refuse("ratification must identify the declared human author")
    _array(root["witnesses"], "review.witnesses")
    _array(root["questions"], "review.questions")
    return root


def _validate_blank_v3(
    record_source: bytes, protocol_source: bytes, manifest_source: bytes
) -> dict[str, Any]:
    protocol = validate_protocol(protocol_source)
    manifest = validate_review_input_manifest(manifest_source, protocol_source)
    root = _record_root_v3(record_source, protocol, manifest, _digest(protocol_source))
    if root["status"] != "BLANK":
        _refuse("blank review status must be BLANK")
    if root["inputs"]["review_input_manifest_sha256"] != "":
        _refuse("blank review must not bind a stage manifest")
    if root["preliminary"]["actor_id"] or root["preliminary"]["completed_at"]:
        _refuse("blank review preliminary authorship must remain empty")
    ratification = root["ratification"]
    if ratification["disposition"] != "PENDING" or any(
        ratification[field] for field in ("completed_at", "notes")
    ):
        _refuse("blank review human ratification must remain pending")
    if root["witnesses"] != []:
        _refuse("blank review must carry no witness judgment")

    questions = root["questions"]
    if [item["question_id"] for item in questions] != manifest["question_ids"]:
        _refuse("blank review questions differ from the input manifest")
    for index, raw in enumerate(questions):
        question = _object(raw, f"review.questions[{index}]")
        _exact_keys(question, _QUESTION_KEYS_V3, f"review.questions[{index}]")
        if question["question_responsiveness"] != "PENDING":
            _refuse(f"blank review question {index} must carry no judgment")
        if question["assembly"] != "PENDING":
            _refuse(f"blank review question {index} must carry no assembly descriptor")
        if (
            question["rows"] != []
            or question["source_locators"] != []
            or question["coverage"] != []
        ):
            _refuse(f"blank review question {index} must carry no row, locator or coverage")
        if question["responsiveness_rationale"] != "":
            _refuse(f"blank review question {index} must carry no rationale")
    return root


def _check_locators(
    locators: list[str],
    kind: str,
    block_ids: set[str] | None,
    sources: Mapping[str, dict[str, Any]],
    source_bytes: Mapping[str, bytes],
    convention: Mapping[str, Any] | None,
    subject: str,
) -> list[bool]:
    """Membership on a text layer, resolution in the file on a row surface."""

    if kind == "SELECTED_READING_TEXT_LAYER":
        assert block_ids is not None
        unknown = sorted(set(locators) - block_ids)
        if unknown:
            _refuse(f"{subject} contain unknown blocks {unknown}")
        return [True] * len(locators)
    assert convention is not None
    return [
        _row_locator_resolves(locator, sources, source_bytes, convention, subject)
        for locator in locators
    ]


def _witnesses_v3(
    root: Mapping[str, Any],
    kind: str,
    returned: set[str],
    block_ids: set[str] | None,
    sources: Mapping[str, dict[str, Any]],
    source_bytes: Mapping[str, bytes],
    convention: Mapping[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    judged: dict[str, dict[str, Any]] = {}
    expected_keys = _WITNESS_KEYS | ({"resolution"} if kind == "STRUCTURED_ROWS" else set())
    for index, raw in enumerate(root["witnesses"]):
        subject = f"review.witnesses[{index}]"
        witness = _object(raw, subject)
        _exact_keys(witness, expected_keys, subject)
        key = _text(witness["witness_key"], f"{subject}.witness_key")
        if key in judged:
            _refuse(f"{subject} judges {key} a second time; judge a witness once")
        judged[key] = witness
        _enum(witness["source_support"], _SOURCE_SUPPORT_V2, f"{subject}.source_support")
        _text(witness["rationale"], f"{subject}.rationale")
        locators = _string_array(witness["source_locators"], f"{subject}.source_locators")
        if not locators:
            _refuse(f"{subject}.source_locators must cite the surface at least once")
        resolved = _check_locators(
            locators,
            kind,
            block_ids,
            sources,
            source_bytes,
            convention,
            f"{subject}.source_locators",
        )
        if kind != "STRUCTURED_ROWS":
            continue
        resolution = _enum(
            witness["resolution"], ROW_RESOLUTIONS, f"{subject}.resolution"
        )
        if resolution in RESOLVING_ROW_RESOLUTIONS:
            unresolved = [
                locator for locator, ok in zip(locators, resolved) if not ok
            ]
            if unresolved:
                _refuse(
                    f"{subject} declares {resolution} and its locator"
                    f" {unresolved[0]!r} does not resolve under the declared convention"
                )
        else:
            if all(resolved):
                _refuse(
                    f"{subject} declares LOCATOR_NOT_RESOLVABLE and every locator"
                    " it cites resolves under the declared convention"
                )
            if witness["source_support"] != "NOT_EVALUABLE":
                _refuse(
                    f"{subject} carries an unresolvable locator, whose support is"
                    " NOT_EVALUABLE by rule"
                )
    if set(judged) != returned:
        missing = sorted(returned - set(judged))
        extra = sorted(set(judged) - returned)
        _refuse(
            "review.witnesses must judge every returned witness once and no other"
            f" (missing {missing}, unreturned {extra})"
        )
    return judged


def _coverage_v3(
    question: Mapping[str, Any],
    semantics: list[str],
    row_witnesses: list[str],
    judged: Mapping[str, dict[str, Any]],
    subject: str,
) -> None:
    coverage = _array(question["coverage"], f"{subject}.coverage")
    if [item.get("semantic") for item in coverage] != semantics:
        _refuse(
            f"{subject}.coverage must name the question's required_semantics in order"
        )
    for index, raw in enumerate(coverage):
        entry_subject = f"{subject}.coverage[{index}]"
        entry = _object(raw, entry_subject)
        _exact_keys(entry, _COVERAGE_KEYS, entry_subject)
        row_index = entry["row_index"]
        reason = entry["absent_reason"]
        if (row_index is None) == (reason is None):
            _refuse(
                f"{entry_subject} must name either a row or one absent_reason"
            )
        if reason is not None:
            _enum(reason, COVERAGE_ABSENT_REASONS, f"{entry_subject}.absent_reason")
            _text(entry["note"], f"{entry_subject}.note")
            continue
        if type(row_index) is not int or not 0 <= row_index < len(row_witnesses):
            _refuse(f"{entry_subject}.row_index is not a row of this question")
        witness = judged[row_witnesses[row_index]]
        if witness["source_support"] != "SUPPORTED" and (
            witness.get("resolution") != "VALUE_DERIVED_FROM_ROW"
        ):
            _refuse(
                f"{entry_subject} names a row whose witness is neither SUPPORTED nor"
                " VALUE_DERIVED_FROM_ROW"
            )


def _questions_v3(
    root: Mapping[str, Any],
    manifest: Mapping[str, Any],
    questions_file: list[dict[str, Any]],
    returned: Mapping[str, list[str]],
    judged: Mapping[str, dict[str, Any]],
    kind: str,
    block_ids: set[str] | None,
    sources: Mapping[str, dict[str, Any]],
    source_bytes: Mapping[str, bytes],
    convention: Mapping[str, Any] | None,
) -> None:
    questions = root["questions"]
    ids = [item["question_id"] for item in questions]
    if ids != manifest["question_ids"]:
        _refuse("review questions differ from the input manifest")
    if [item["id"] for item in questions_file] != ids:
        _refuse("review questions differ from the competency question file")

    semantics_by_id = {
        item["id"]: list(item["required_semantics"]) for item in questions_file
    }
    for index, raw in enumerate(questions):
        subject = f"review.questions[{index}]"
        question = _object(raw, subject)
        _exact_keys(question, _QUESTION_KEYS_V3, subject)
        question_id = question["question_id"]
        _enum(question["assembly"], ASSEMBLY_DESCRIPTORS, f"{subject}.assembly")
        _text(question["responsiveness_rationale"], f"{subject}.responsiveness_rationale")
        locators = _string_array(question["source_locators"], f"{subject}.source_locators")
        if not locators:
            _refuse(f"{subject}.source_locators must cite the surface at least once")
        _check_locators(
            locators,
            kind,
            block_ids,
            sources,
            source_bytes,
            convention,
            f"{subject}.source_locators",
        )

        expected = returned[question_id]
        rows = _array(question["rows"], f"{subject}.rows")
        if [item.get("row_index") for item in rows] != list(range(len(expected))):
            _refuse(f"{subject}.rows must judge every returned row in order")
        row_witnesses: list[str] = []
        for row_index, raw_row in enumerate(rows):
            row_subject = f"{subject}.rows[{row_index}]"
            row = _object(raw_row, row_subject)
            _exact_keys(row, _ROW_KEYS_V3, row_subject)
            key = _text(row["witness_key"], f"{row_subject}.witness_key")
            if key != expected[row_index]:
                _refuse(
                    f"{row_subject} names witness {key!r}; the query result returns"
                    f" {expected[row_index]!r}"
                )
            row_witnesses.append(key)

        _coverage_v3(question, semantics_by_id[question_id], row_witnesses, judged, subject)
        derived = derived_responsiveness(question["coverage"])
        if question["question_responsiveness"] != derived:
            _refuse(
                f"{subject}.question_responsiveness states"
                f" {question['question_responsiveness']!r}; the derivation from"
                f" coverage produces {derived!r}"
            )


def _validate_review_v3(
    record_source: bytes,
    protocol_source: bytes,
    *,
    review_input_manifest_source: bytes,
    query_result_source: bytes,
    selected_reading_source: bytes | None,
    competency_questions_source: bytes | None,
    surface_sources: Mapping[str, bytes] | None,
    require_human_ratification: bool,
    findings: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    protocol = validate_protocol(protocol_source)
    manifest = validate_review_input_manifest(
        review_input_manifest_source, protocol_source
    )
    root = _record_root_v3(record_source, protocol, manifest, _digest(protocol_source))
    if root["status"] == "BLANK":
        _refuse("blank review is not a completed review")
    if root["inputs"]["review_input_manifest_sha256"] != _digest(
        review_input_manifest_source
    ):
        _refuse("review input-manifest identity differs from the supplied manifest")
    if competency_questions_source is None:
        _refuse("the v3 protocol reads coverage against the competency questions")
    assert competency_questions_source is not None
    if _digest(competency_questions_source) != manifest["fixed_identities"][
        "competency_questions_sha256"
    ]:
        _refuse("competency questions differ from the frozen review inputs")
    questions_file = _question_file(competency_questions_source)

    kind = _surface(manifest)["kind"]
    block_ids: set[str] | None = None
    sources: dict[str, dict[str, Any]] = {}
    source_bytes: dict[str, bytes] = {}
    convention: Mapping[str, Any] | None = None
    if kind == "SELECTED_READING_TEXT_LAYER":
        if selected_reading_source is None:
            _refuse("a text-layer cell is validated against its selected reading")
        assert selected_reading_source is not None
        block_ids = _reading_blocks(
            selected_reading_source, manifest["fixed_identities"]
        )
    else:
        if surface_sources is None:
            _refuse(
                "a row cell is validated against its source files; the locator is"
                " resolved, never taken on trust"
            )
        assert surface_sources is not None
        sources = _sources_by_id(manifest)
        if set(surface_sources) != set(sources):
            _refuse("the supplied sources differ from the ones the manifest declares")
        for source_id, item in sources.items():
            if _digest(surface_sources[source_id]) != item["sha256"]:
                _refuse(f"declared source {source_id} differs from its frozen digest")
        source_bytes = dict(surface_sources)
        convention = _surface(manifest)["locator_convention"]

    returned = _query_witnesses(query_result_source, manifest)
    if sorted(returned) != sorted(manifest["question_ids"]):
        _refuse("query result questions differ from the frozen review inputs")
    _authorship_state(root, require_human_ratification=require_human_ratification)
    judged = _witnesses_v3(
        root,
        kind,
        {key for keys in returned.values() for key in keys},
        block_ids,
        sources,
        source_bytes,
        convention,
    )
    _questions_v3(
        root,
        manifest,
        questions_file,
        returned,
        judged,
        kind,
        block_ids,
        sources,
        source_bytes,
        convention,
    )
    if findings is not None:
        findings.extend(control_outcomes(root, competency_questions_source))
    return root
