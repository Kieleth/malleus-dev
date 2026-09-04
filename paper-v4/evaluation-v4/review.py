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
materials, and a query result at `malleus.paper-v4.query-result/v2` whose
inputs name a ledger head. Every one of those refuses in the v1 validator, so
this module carries the v2 grammar instead.

It checks identities, references and authorship state. It never chooses,
changes or aggregates a judgment.
"""

from __future__ import annotations

from datetime import datetime
from hashlib import sha256
import json
import re
from typing import Any, Mapping


PROTOCOL_SCHEMA = "malleus.paper-v4.source-grounded-review-protocol/v2"
PROTOCOL_STATUS = "FROZEN_BEFORE_V4_PRODUCER"
MANIFEST_SCHEMA = "malleus.paper-v4.source-grounded-review-inputs/v2"
REVIEW_SCHEMA = "malleus.paper-v4.source-grounded-review/v2"
QUERY_RESULT_SCHEMA = "malleus.paper-v4.query-result/v2"
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


def validate_protocol(protocol_source: bytes) -> dict[str, Any]:
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
    if result.get("schema") != QUERY_RESULT_SCHEMA:
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
    selected_reading_source: bytes,
    require_human_ratification: bool = False,
) -> dict[str, Any]:
    """Validate identities, references and authorship, never a judgment."""

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
