"""Validate paper-v4 human-review structure without judging its content."""

from __future__ import annotations

from datetime import datetime
from hashlib import sha256
import json
import re
from typing import Any, Mapping, Sequence

from research.ontology_driven_kg_realization.experiments.document_paper.native_query import (
    NativeQueryRefusal,
    load_query_binding,
)


PROTOCOL_SCHEMA = "malleus.paper-v4.source-grounded-review-protocol/v1"
MANIFEST_SCHEMA = "malleus.paper-v4.source-grounded-review-inputs/v1"
REVIEW_SCHEMA = "malleus.paper-v4.source-grounded-review/v1"
QUERY_RESULT_SCHEMA = "malleus.paper-v4.query-replay/v1"
PENDING_STAGE_IDENTITY = "PENDING_UNTIL_STAGE_FREEZE"
_PROTOCOL_STATUS = "FROZEN_BEFORE_V2_QUERY_OUTPUT"
_FROZEN_MANIFEST_STATUS = "FROZEN_FOR_REVIEW"
_REVIEW_STATUSES = {
    "BLANK",
    "PRELIMINARY_COMPLETE",
    "HUMAN_RATIFIED",
    "HUMAN_REJECTED",
}
_RATIFIED_DISPOSITIONS = {"RATIFIED_AS_RECORDED", "RATIFIED_WITH_EDITS"}
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")
_JSON_BLOCK = re.compile(r"```json\n(?P<record>.*?)\n```", re.DOTALL)
_FIXED_IDENTITY_KEYS = {
    "competency_questions_sha256",
    "selected_reading_sha256",
    "source_sha256",
}
_STAGE_IDENTITY_KEYS = {
    "ledger_head",
    "query_binding_sha256",
    "query_result_sha256",
    "replay_receipt_sha256",
    "selected_ontology_sha256",
}
_QUESTION_KEYS = {
    "question_id",
    "question_responsiveness",
    "rationale",
    "row_refs",
    "source_locators",
    "source_support",
}
_REQUIRED_FORBIDDEN_FIELDS = {
    "accuracy",
    "answer",
    "answer_key",
    "answers",
    "automated_score",
    "canonical_answer",
    "correctness",
    "exact_match",
    "numeric_score",
    "oracle",
    "oracle_sha256",
    "score",
}
_WITHHELD_MATERIALS = {
    "answer_oracle",
    "automated_score",
    "canonical_answer",
    "manuscript_results",
    "model_transcripts",
    "paper_ledger_results",
    "population_proposal",
    "population_provenance",
    "score_result",
}


class HumanReviewRefusal(ValueError):
    """A review protocol, source, or record is structurally invalid."""


def _refuse(detail: str) -> None:
    raise HumanReviewRefusal(detail)


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
        raise HumanReviewRefusal(f"{subject} must be UTF-8 JSON") from error


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
    try:
        return datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise HumanReviewRefusal(
            f"{subject} must be an RFC 3339 UTC second timestamp"
        ) from error


def _string_array(value: object, subject: str) -> list[str]:
    values = _array(value, subject)
    if any(not isinstance(item, str) or not item.strip() for item in values):
        _refuse(f"{subject} must contain only nonblank text")
    if len(values) != len(set(values)):
        _refuse(f"{subject} must not contain duplicates")
    return values


def _markdown_record(source: bytes) -> dict[str, Any]:
    if type(source) is not bytes:
        raise TypeError("review record source must be bytes")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        raise HumanReviewRefusal("review record must be UTF-8 Markdown") from error
    blocks = list(_JSON_BLOCK.finditer(text))
    if len(blocks) != 1:
        _refuse("review record must contain exactly one fenced JSON block")
    return _object(
        _json(blocks[0].group("record").encode("utf-8"), "review JSON"),
        "review",
    )


def _protocol(source: bytes) -> dict[str, Any]:
    root = _object(_json(source, "review protocol"), "review protocol")
    _exact_keys(
        root,
        {
            "authorship",
            "evidence_surface",
            "fixed_identities",
            "forbidden_record_fields",
            "judgments",
            "purpose",
            "question_ids",
            "review_input_manifest",
            "review_materials",
            "schema",
            "status",
            "validator_materials",
            "withheld_materials",
        },
        "review protocol",
    )
    if root["schema"] != PROTOCOL_SCHEMA or root["status"] != _PROTOCOL_STATUS:
        _refuse("review protocol schema or v2 freeze status differs")
    if root["purpose"] != ["SOURCE_SUPPORT", "QUESTION_RESPONSIVENESS"]:
        _refuse("review protocol purpose differs")
    if root["evidence_surface"] != {
        "authoritative": "SELECTED_READING_TEXT_LAYER",
        "locator_kind": "SELECTED_READING_BLOCK_ID",
        "source_pdf_role": "OPTIONAL_PROJECTION_FIDELITY_CROSS_CHECK_ONLY",
    }:
        _refuse("review protocol must declare one authoritative evidence surface")

    fixed = _object(root["fixed_identities"], "review protocol.fixed_identities")
    _exact_keys(fixed, _FIXED_IDENTITY_KEYS, "review protocol.fixed_identities")
    for field, value in fixed.items():
        _sha256(value, f"review protocol.fixed_identities.{field}")

    manifest = _object(
        root["review_input_manifest"], "review protocol.review_input_manifest"
    )
    _exact_keys(
        manifest,
        {"frozen_status", "pending_status", "schema", "stage_identity_template"},
        "review protocol.review_input_manifest",
    )
    if manifest != {
        "schema": MANIFEST_SCHEMA,
        "pending_status": PENDING_STAGE_IDENTITY,
        "frozen_status": _FROZEN_MANIFEST_STATUS,
        "stage_identity_template": {
            field: PENDING_STAGE_IDENTITY for field in _STAGE_IDENTITY_KEYS
        },
    }:
        _refuse("review protocol must leave every v2 stage identity pending")

    question_ids = _string_array(root["question_ids"], "review protocol.question_ids")
    if not question_ids:
        _refuse("review protocol.question_ids must not be empty")

    judgments = _object(root["judgments"], "review protocol.judgments")
    _exact_keys(
        judgments,
        {"question_responsiveness", "source_support"},
        "review protocol.judgments",
    )
    if judgments != {
        "source_support": [
            "SUPPORTED",
            "PARTIAL",
            "UNSUPPORTED",
            "NOT_EVALUABLE",
        ],
        "question_responsiveness": [
            "RESPONSIVE",
            "PARTIAL",
            "NOT_RESPONSIVE",
            "NOT_EVALUABLE",
        ],
    }:
        _refuse("review protocol judgment labels differ")

    authorship = _object(root["authorship"], "review protocol.authorship")
    _exact_keys(
        authorship,
        {
            "preliminary_evaluator_kind",
            "ratifier_actor_id",
            "ratifier_evaluator_kind",
        },
        "review protocol.authorship",
    )
    if (
        authorship["preliminary_evaluator_kind"] != "CODEX_PRELIMINARY"
        or authorship["ratifier_evaluator_kind"] != "HUMAN_AUTHOR"
        or authorship["ratifier_actor_id"] != "actor:luis"
    ):
        _refuse("review protocol must distinguish Codex from the human ratifier")
    _text(authorship["ratifier_actor_id"], "review protocol ratifier actor")

    review_materials = _string_array(
        root["review_materials"], "review protocol.review_materials"
    )
    if review_materials != [
        "selected_reading",
        "competency_questions",
        "query_binding",
        "query_result",
    ]:
        _refuse("review protocol review materials differ")
    validator_materials = set(
        _string_array(
            root["validator_materials"], "review protocol.validator_materials"
        )
    )
    withheld = set(
        _string_array(root["withheld_materials"], "review protocol.withheld_materials")
    )
    if validator_materials != {
        "review_input_manifest",
        "selected_ontology",
        "replay_receipt",
    }:
        _refuse("review protocol validator materials differ")
    if withheld != _WITHHELD_MATERIALS:
        _refuse("review protocol withheld materials differ")
    if set(review_materials) & withheld or validator_materials & withheld:
        _refuse("allowed and withheld review materials must be disjoint")
    forbidden = set(
        _string_array(
            root["forbidden_record_fields"],
            "review protocol.forbidden_record_fields",
        )
    )
    if forbidden != _REQUIRED_FORBIDDEN_FIELDS:
        _refuse("review protocol does not forbid every answer or score field")
    return root


def _manifest(
    source: bytes,
    protocol: Mapping[str, Any],
    protocol_digest: str,
    *,
    require_frozen: bool,
) -> dict[str, Any]:
    root = _object(_json(source, "review input manifest"), "review input manifest")
    _exact_keys(
        root,
        {
            "fixed_identities",
            "review_protocol_sha256",
            "schema",
            "stage_identities",
            "status",
        },
        "review input manifest",
    )
    if root["schema"] != MANIFEST_SCHEMA:
        _refuse("review input manifest schema differs")
    if root["review_protocol_sha256"] != protocol_digest:
        _refuse("review input manifest does not bind the supplied protocol")
    fixed = _object(root["fixed_identities"], "review input manifest.fixed_identities")
    _exact_keys(fixed, _FIXED_IDENTITY_KEYS, "review input manifest.fixed_identities")
    if fixed != protocol["fixed_identities"]:
        _refuse("review input manifest fixed identities differ from the protocol")
    stage = _object(root["stage_identities"], "review input manifest.stage_identities")
    _exact_keys(stage, _STAGE_IDENTITY_KEYS, "review input manifest.stage_identities")
    if require_frozen:
        if root["status"] != _FROZEN_MANIFEST_STATUS:
            _refuse("review input manifest must be frozen before review")
        for field, value in stage.items():
            _sha256(value, f"review input manifest.stage_identities.{field}")
    elif root["status"] != PENDING_STAGE_IDENTITY or stage != {
        field: PENDING_STAGE_IDENTITY for field in _STAGE_IDENTITY_KEYS
    }:
        _refuse("blank review input manifest must leave every stage identity pending")
    return root


def validate_blank_review_input_manifest(
    manifest_source: bytes, protocol_source: bytes
) -> dict[str, Any]:
    """Validate the v2 manifest template without accepting it for review."""

    return _manifest(
        manifest_source,
        _protocol(protocol_source),
        _digest(protocol_source),
        require_frozen=False,
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
    source: bytes, protocol: Mapping[str, Any], protocol_digest: str
) -> dict[str, Any]:
    root = _markdown_record(source)
    _exact_keys(
        root,
        {"inputs", "preliminary", "questions", "ratification", "schema", "status"},
        "review",
    )
    if root["schema"] != REVIEW_SCHEMA or root["status"] not in _REVIEW_STATUSES:
        _refuse("review schema or status differs")
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
    return root


def _blank_actor_state(root: Mapping[str, Any], protocol: Mapping[str, Any]) -> None:
    preliminary = _object(root["preliminary"], "review.preliminary")
    _exact_keys(
        preliminary,
        {"actor_id", "completed_at", "evaluator_kind"},
        "review.preliminary",
    )
    if preliminary != {
        "evaluator_kind": protocol["authorship"]["preliminary_evaluator_kind"],
        "actor_id": "",
        "completed_at": "",
    }:
        _refuse("blank review preliminary authorship must remain empty")

    ratification = _object(root["ratification"], "review.ratification")
    _exact_keys(
        ratification,
        {"actor_id", "completed_at", "disposition", "evaluator_kind", "notes"},
        "review.ratification",
    )
    if ratification != {
        "evaluator_kind": protocol["authorship"]["ratifier_evaluator_kind"],
        "actor_id": protocol["authorship"]["ratifier_actor_id"],
        "disposition": "PENDING",
        "completed_at": "",
        "notes": "",
    }:
        _refuse("blank review human ratification must remain pending")


def _blank_questions(root: Mapping[str, Any], protocol: Mapping[str, Any]) -> None:
    questions = _array(root["questions"], "review.questions")
    if len(questions) != len(protocol["question_ids"]):
        _refuse("blank review question count differs from the protocol")
    for index, (raw, question_id) in enumerate(
        zip(questions, protocol["question_ids"], strict=True)
    ):
        question = _object(raw, f"review.questions[{index}]")
        _exact_keys(question, _QUESTION_KEYS, f"review.questions[{index}]")
        if question != {
            "question_id": question_id,
            "source_support": "PENDING",
            "question_responsiveness": "PENDING",
            "row_refs": [],
            "source_locators": [],
            "rationale": "",
        }:
            _refuse(f"blank review question {question_id} must remain empty")


def validate_blank_human_review(
    record_source: bytes, protocol_source: bytes
) -> dict[str, Any]:
    """Validate the pre-output blank without accepting it as evidence."""

    protocol = _protocol(protocol_source)
    root = _record_root(record_source, protocol, _digest(protocol_source))
    if root["status"] != "BLANK":
        _refuse("blank review status must be BLANK")
    if root["inputs"]["review_input_manifest_sha256"] != "":
        _refuse("blank review must not bind a stage manifest")
    _blank_actor_state(root, protocol)
    _blank_questions(root, protocol)
    return root


def _question_ids(source: bytes, expected_digest: str) -> list[str]:
    if _digest(source) != expected_digest:
        _refuse("competency questions differ from the frozen protocol")
    root = _object(_json(source, "competency questions"), "competency questions")
    questions = _array(root.get("questions"), "competency questions.questions")
    return [
        _text(
            _object(question, f"competency questions.questions[{index}]").get("id"),
            f"competency questions.questions[{index}].id",
        )
        for index, question in enumerate(questions)
    ]


def _reading_blocks(source: bytes, fixed: Mapping[str, Any]) -> set[str]:
    if _digest(source) != fixed["selected_reading_sha256"]:
        _refuse("selected reading differs from the frozen protocol")
    root = _object(_json(source, "selected reading"), "selected reading")
    if root.get("source_sha256") != fixed["source_sha256"]:
        _refuse("selected reading does not bind the frozen source")
    pages = _array(root.get("pages"), "selected reading.pages")
    block_ids = [
        _text(
            _object(
                block, f"selected reading.pages[{page_index}].blocks[{block_index}]"
            ).get("id"),
            "selected reading block id",
        )
        for page_index, page in enumerate(pages)
        for block_index, block in enumerate(
            _array(
                _object(page, f"selected reading.pages[{page_index}]").get("blocks"),
                f"selected reading.pages[{page_index}].blocks",
            )
        )
    ]
    if len(block_ids) != len(set(block_ids)):
        _refuse("selected reading block ids must be unique")
    return set(block_ids)


def _replay_graph_identity(
    *,
    fixed: Mapping[str, Any],
    stage: Mapping[str, Any],
    selected_ontology_source: bytes,
    replay_receipt_source: bytes,
    source_pdf_source: bytes | None,
) -> str:
    if (
        source_pdf_source is not None
        and _digest(source_pdf_source) != fixed["source_sha256"]
    ):
        _refuse("optional source PDF differs from the frozen protocol")
    if _digest(selected_ontology_source) != stage["selected_ontology_sha256"]:
        _refuse("selected ontology differs from the frozen review inputs")
    if _digest(replay_receipt_source) != stage["replay_receipt_sha256"]:
        _refuse("replay receipt differs from the frozen review inputs")

    receipt = _object(_json(replay_receipt_source, "replay receipt"), "replay receipt")
    if receipt.get("ledger_head") != stage["ledger_head"]:
        _refuse("replay receipt ledger head differs from the frozen review inputs")
    source_identities = _object(
        receipt.get("source_identities"), "replay receipt.source_identities"
    )
    if fixed["selected_reading_sha256"] not in source_identities.values():
        _refuse("replay receipt does not bind the frozen selected reading")
    return _sha256(receipt.get("graph_state_digest"), "replay graph-state identity")


def _query_rows(
    source: bytes,
    binding_source: bytes,
    stage: Mapping[str, Any],
    replay_graph_state_digest: str,
) -> dict[str, tuple[str, int]]:
    if _digest(binding_source) != stage["query_binding_sha256"]:
        _refuse("query binding differs from the frozen review inputs")
    if _digest(source) != stage["query_result_sha256"]:
        _refuse("query result differs from the frozen review inputs")
    try:
        binding = load_query_binding(binding_source)
    except NativeQueryRefusal as error:
        raise HumanReviewRefusal(f"query binding refused: {error}") from error

    result = _object(_json(source, "query result"), "query result")
    _exact_keys(
        result,
        {"forbidden_attempts", "graph_state_digest", "inputs", "queries", "schema"},
        "query result",
    )
    if result["schema"] != QUERY_RESULT_SCHEMA:
        _refuse("query result schema differs")
    if result["graph_state_digest"] != replay_graph_state_digest:
        _refuse("query result graph state differs from the frozen replay")
    inputs = _object(result["inputs"], "query result.inputs")
    _exact_keys(
        inputs,
        {"ontology_sha256", "query_binding_sha256", "replay_receipt_sha256"},
        "query result.inputs",
    )
    if inputs != {
        "ontology_sha256": stage["selected_ontology_sha256"],
        "query_binding_sha256": stage["query_binding_sha256"],
        "replay_receipt_sha256": stage["replay_receipt_sha256"],
    }:
        _refuse("query result inputs differ from the frozen review inputs")

    queries = _array(result["queries"], "query result.queries")
    if len(queries) != len(binding["queries"]):
        _refuse("query result query count differs from the binding")
    rows: dict[str, tuple[str, int]] = {}
    for index, (raw_query, bound) in enumerate(
        zip(queries, binding["queries"], strict=True)
    ):
        query = _object(raw_query, f"query result.queries[{index}]")
        _exact_keys(
            query,
            {"query_id", "question_id", "rows"},
            f"query result.queries[{index}]",
        )
        if (
            query["query_id"] != bound["id"]
            or query["question_id"] != bound["question_id"]
        ):
            _refuse(f"query result.queries[{index}] ids differ from the binding")
        result_rows = _array(query["rows"], f"query result.queries[{index}].rows")
        if query["question_id"] in rows:
            _refuse("query result question ids must be unique")
        rows[query["question_id"]] = (query["query_id"], len(result_rows))
    return rows


def _completed_authorship(
    root: Mapping[str, Any],
    protocol: Mapping[str, Any],
    *,
    require_human_ratification: bool,
) -> None:
    preliminary = _object(root["preliminary"], "review.preliminary")
    _exact_keys(
        preliminary,
        {"actor_id", "completed_at", "evaluator_kind"},
        "review.preliminary",
    )
    if (
        preliminary["evaluator_kind"]
        != protocol["authorship"]["preliminary_evaluator_kind"]
    ):
        _refuse("preliminary evaluator kind must identify Codex honestly")
    _text(preliminary["actor_id"], "review.preliminary.actor_id")
    preliminary_at = _timestamp(
        preliminary["completed_at"], "review.preliminary.completed_at"
    )

    ratification = _object(root["ratification"], "review.ratification")
    _exact_keys(
        ratification,
        {"actor_id", "completed_at", "disposition", "evaluator_kind", "notes"},
        "review.ratification",
    )
    if (
        ratification["evaluator_kind"]
        != protocol["authorship"]["ratifier_evaluator_kind"]
        or ratification["actor_id"] != protocol["authorship"]["ratifier_actor_id"]
    ):
        _refuse("ratification must identify the declared human author")

    status = root["status"]
    if status == "PRELIMINARY_COMPLETE":
        if ratification["disposition"] != "PENDING" or any(
            ratification[field] for field in ("completed_at", "notes")
        ):
            _refuse("preliminary review must leave human ratification pending")
    elif status == "HUMAN_RATIFIED":
        if ratification["disposition"] not in _RATIFIED_DISPOSITIONS:
            _refuse("human-ratified review requires a ratified disposition")
        ratification_at = _timestamp(
            ratification["completed_at"], "review.ratification.completed_at"
        )
        _text(ratification["notes"], "review.ratification.notes")
    elif status == "HUMAN_REJECTED":
        if ratification["disposition"] != "REJECTED":
            _refuse("human-rejected review requires disposition REJECTED")
        ratification_at = _timestamp(
            ratification["completed_at"], "review.ratification.completed_at"
        )
        _text(ratification["notes"], "review.ratification.notes")
    else:
        _refuse("completed review cannot retain BLANK status")
    if status in {"HUMAN_RATIFIED", "HUMAN_REJECTED"} and (
        ratification_at < preliminary_at
    ):
        _refuse("human ratification cannot precede the Codex preliminary review")
    if require_human_ratification and status != "HUMAN_RATIFIED":
        _refuse("human ratification is required for paper evidence")


def _completed_questions(
    root: Mapping[str, Any],
    protocol: Mapping[str, Any],
    question_ids: Sequence[str],
    query_rows: Mapping[str, tuple[str, int]],
    block_ids: set[str],
) -> None:
    if list(question_ids) != protocol["question_ids"]:
        _refuse("competency question order differs from the review protocol")
    if set(query_rows) != set(question_ids):
        _refuse("query result question ids differ from the competency questions")
    questions = _array(root["questions"], "review.questions")
    if len(questions) != len(question_ids):
        _refuse("review question count differs")
    allowed_support = set(protocol["judgments"]["source_support"])
    allowed_responsiveness = set(protocol["judgments"]["question_responsiveness"])

    for index, (raw, question_id) in enumerate(
        zip(questions, question_ids, strict=True)
    ):
        subject = f"review.questions[{index}]"
        question = _object(raw, subject)
        _exact_keys(question, _QUESTION_KEYS, subject)
        if question["question_id"] != question_id:
            _refuse(f"{subject}.question_id differs")
        if question["source_support"] not in allowed_support:
            _refuse(f"{subject}.source_support is not an allowed human judgment")
        if question["question_responsiveness"] not in allowed_responsiveness:
            _refuse(
                f"{subject}.question_responsiveness is not an allowed human judgment"
            )

        query_id, row_count = query_rows[question_id]
        refs = _array(question["row_refs"], f"{subject}.row_refs")
        expected_refs = [
            {"query_id": query_id, "row_index": row_index}
            for row_index in range(row_count)
        ]
        for ref_index, raw_ref in enumerate(refs):
            ref = _object(raw_ref, f"{subject}.row_refs[{ref_index}]")
            _exact_keys(
                ref,
                {"query_id", "row_index"},
                f"{subject}.row_refs[{ref_index}]",
            )
            if type(ref["row_index"]) is not int or ref["row_index"] < 0:
                _refuse(
                    f"{subject}.row_refs[{ref_index}].row_index must be nonnegative"
                )
        if refs != expected_refs:
            _refuse(f"{subject}.row_refs must cover every returned row in order")

        locators = _string_array(
            question["source_locators"], f"{subject}.source_locators"
        )
        if not locators:
            _refuse(f"{subject}.source_locators must cite at least one source block")
        unknown = sorted(set(locators) - block_ids)
        if unknown:
            _refuse(f"{subject}.source_locators contain unknown blocks {unknown}")
        _text(question["rationale"], f"{subject}.rationale")


def validate_human_review(
    record_source: bytes,
    protocol_source: bytes,
    *,
    review_input_manifest_source: bytes,
    competency_questions_source: bytes,
    query_binding_source: bytes,
    query_result_source: bytes,
    replay_receipt_source: bytes,
    selected_reading_source: bytes,
    selected_ontology_source: bytes,
    source_pdf_source: bytes | None = None,
    require_human_ratification: bool = False,
) -> dict[str, Any]:
    """Validate identities and references while preserving authored judgments."""

    protocol = _protocol(protocol_source)
    protocol_digest = _digest(protocol_source)
    manifest = _manifest(
        review_input_manifest_source,
        protocol,
        protocol_digest,
        require_frozen=True,
    )
    root = _record_root(record_source, protocol, protocol_digest)
    if root["status"] == "BLANK":
        _refuse("blank review is not a completed review")
    if root["inputs"]["review_input_manifest_sha256"] != _digest(
        review_input_manifest_source
    ):
        _refuse("review input-manifest identity differs from the supplied manifest")

    fixed = manifest["fixed_identities"]
    stage = manifest["stage_identities"]
    question_ids = _question_ids(
        competency_questions_source, fixed["competency_questions_sha256"]
    )
    block_ids = _reading_blocks(selected_reading_source, fixed)
    replay_graph_state_digest = _replay_graph_identity(
        fixed=fixed,
        stage=stage,
        selected_ontology_source=selected_ontology_source,
        replay_receipt_source=replay_receipt_source,
        source_pdf_source=source_pdf_source,
    )
    query_rows = _query_rows(
        query_result_source,
        query_binding_source,
        stage,
        replay_graph_state_digest,
    )

    _completed_authorship(
        root,
        protocol,
        require_human_ratification=require_human_ratification,
    )
    _completed_questions(root, protocol, question_ids, query_rows, block_ids)
    return root
