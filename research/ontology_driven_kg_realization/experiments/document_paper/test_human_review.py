"""Focused guards for source-grounded human-review records."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper.human_review import (
    HumanReviewRefusal,
    MANIFEST_SCHEMA,
    PENDING_STAGE_IDENTITY,
    PROTOCOL_SCHEMA,
    REVIEW_SCHEMA,
    validate_blank_human_review,
    validate_blank_review_input_manifest,
    validate_human_review,
)


ROOT = Path(__file__).resolve().parents[4]
PROTOCOL = ROOT / "paper-v4/evaluation-v2/review-protocol.json"
BLANK_MANIFEST = ROOT / "paper-v4/evaluation-v2/review-input-manifest.blank.json"
BLANK_RECORD = ROOT / "paper-v4/evaluation-v2/review-record.blank.md"


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _markdown(value: object) -> bytes:
    payload = json.dumps(value, indent=2)
    return f"# Fictional review\n\n```json\n{payload}\n```\n".encode()


def _inputs() -> dict[str, bytes]:
    source = b"fictional source PDF bytes"
    source_digest = _digest(source)
    questions = _json(
        {
            "source_sha256": source_digest,
            "questions": [
                {"id": f"CQ-0{index}", "question": f"Question {index}"}
                for index in range(1, 5)
            ],
        }
    )
    reading = _json(
        {
            "source_sha256": source_digest,
            "pages": [
                {
                    "page": 1,
                    "blocks": [
                        {"id": f"p001-b{index:03d}", "text": f"Fictional {index}"}
                        for index in range(1, 5)
                    ],
                }
            ],
        }
    )
    case = {
        "ordinal": 1,
        "source_record_type": "FictionalSource",
        "relation_record_type": "FictionalRelation",
        "relation_type": {"enum": "FictionalRelationType", "value": "CONNECTS"},
        "target_record_type": "FictionalTarget",
        "output_fields": {"source": ["name"], "relation": [], "target": []},
    }
    binding = _json(
        {
            "schema": "malleus.paper-v4.native-query-binding/v1",
            "status": "FROZEN_BEFORE_POPULATION",
            "queries": [
                {
                    "id": f"NQ-CQ-0{index}",
                    "question_id": f"CQ-0{index}",
                    "cases": [case],
                }
                for index in range(1, 5)
            ],
        }
    )
    ontology = b"fictional corrected ontology bytes"
    graph_state_digest = "sha256:" + "5" * 64
    receipt = _json(
        {
            "ledger_head": "sha256:" + "3" * 64,
            "graph_state_digest": graph_state_digest,
            "source_identities": {"source:v2:selected-reading": _digest(reading)},
        }
    )
    fixed = {
        "source_sha256": source_digest,
        "selected_reading_sha256": _digest(reading),
        "competency_questions_sha256": _digest(questions),
    }
    stage = {
        "selected_ontology_sha256": _digest(ontology),
        "ledger_head": "sha256:" + "3" * 64,
        "replay_receipt_sha256": _digest(receipt),
        "query_binding_sha256": _digest(binding),
    }
    result = _json(
        {
            "schema": "malleus.paper-v4.query-replay/v1",
            "inputs": {
                "ontology_sha256": stage["selected_ontology_sha256"],
                "query_binding_sha256": stage["query_binding_sha256"],
                "replay_receipt_sha256": stage["replay_receipt_sha256"],
            },
            "graph_state_digest": graph_state_digest,
            "queries": [
                {
                    "query_id": f"NQ-CQ-0{index}",
                    "question_id": f"CQ-0{index}",
                    "rows": [
                        {
                            "case_ordinal": 1,
                            "source": {},
                            "relation": {},
                            "target": {},
                            "witness": {
                                "source_id": f"source:{index}",
                                "relation_id": f"relation:{index}",
                                "target_id": f"target:{index}",
                            },
                        }
                    ],
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
    stage["query_result_sha256"] = _digest(result)
    protocol = _json(
        {
            "schema": PROTOCOL_SCHEMA,
            "status": "FROZEN_BEFORE_V2_QUERY_OUTPUT",
            "purpose": ["SOURCE_SUPPORT", "QUESTION_RESPONSIVENESS"],
            "evidence_surface": {
                "authoritative": "SELECTED_READING_TEXT_LAYER",
                "locator_kind": "SELECTED_READING_BLOCK_ID",
                "source_pdf_role": "OPTIONAL_PROJECTION_FIDELITY_CROSS_CHECK_ONLY",
            },
            "fixed_identities": fixed,
            "review_input_manifest": {
                "schema": MANIFEST_SCHEMA,
                "pending_status": PENDING_STAGE_IDENTITY,
                "frozen_status": "FROZEN_FOR_REVIEW",
                "stage_identity_template": {
                    field: PENDING_STAGE_IDENTITY for field in stage
                },
            },
            "question_ids": [f"CQ-0{index}" for index in range(1, 5)],
            "judgments": {
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
            },
            "authorship": {
                "preliminary_evaluator_kind": "CODEX_PRELIMINARY",
                "ratifier_evaluator_kind": "HUMAN_AUTHOR",
                "ratifier_actor_id": "actor:luis",
            },
            "review_materials": [
                "selected_reading",
                "competency_questions",
                "query_binding",
                "query_result",
            ],
            "validator_materials": [
                "review_input_manifest",
                "selected_ontology",
                "replay_receipt",
            ],
            "withheld_materials": [
                "answer_oracle",
                "canonical_answer",
                "automated_score",
                "score_result",
                "model_transcripts",
                "population_proposal",
                "population_provenance",
                "manuscript_results",
                "paper_ledger_results",
            ],
            "forbidden_record_fields": [
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
            ],
        }
    )
    manifest = _json(
        {
            "schema": MANIFEST_SCHEMA,
            "status": "FROZEN_FOR_REVIEW",
            "review_protocol_sha256": _digest(protocol),
            "fixed_identities": fixed,
            "stage_identities": stage,
        }
    )
    return {
        "binding": binding,
        "manifest": manifest,
        "ontology": ontology,
        "protocol": protocol,
        "questions": questions,
        "reading": reading,
        "receipt": receipt,
        "result": result,
        "source": source,
    }


def _record(inputs: dict[str, bytes], *, ratified: bool = False) -> dict:
    support = ["SUPPORTED", "PARTIAL", "UNSUPPORTED", "NOT_EVALUABLE"]
    responsiveness = ["RESPONSIVE", "PARTIAL", "NOT_RESPONSIVE", "NOT_EVALUABLE"]
    return {
        "schema": REVIEW_SCHEMA,
        "status": "HUMAN_RATIFIED" if ratified else "PRELIMINARY_COMPLETE",
        "inputs": {
            "review_protocol_sha256": _digest(inputs["protocol"]),
            "review_input_manifest_sha256": _digest(inputs["manifest"]),
        },
        "preliminary": {
            "evaluator_kind": "CODEX_PRELIMINARY",
            "actor_id": "actor:codex-paper-v4",
            "completed_at": "2026-09-03T01:02:03Z",
        },
        "questions": [
            {
                "question_id": f"CQ-0{index}",
                "source_support": support[index - 1],
                "question_responsiveness": responsiveness[index - 1],
                "row_refs": [{"query_id": f"NQ-CQ-0{index}", "row_index": 0}],
                "source_locators": [f"p001-b{index:03d}"],
                "rationale": f"Fictional reason {index}.",
            }
            for index in range(1, 5)
        ],
        "ratification": {
            "evaluator_kind": "HUMAN_AUTHOR",
            "actor_id": "actor:luis",
            "disposition": "RATIFIED_AS_RECORDED" if ratified else "PENDING",
            "completed_at": "2026-09-03T02:03:04Z" if ratified else "",
            "notes": "Reviewed against the declared source." if ratified else "",
        },
    }


def _validate(
    record: dict,
    inputs: dict[str, bytes],
    *,
    include_source_pdf: bool = True,
    **kwargs,
) -> dict:
    return validate_human_review(
        _markdown(record),
        inputs["protocol"],
        review_input_manifest_source=inputs["manifest"],
        competency_questions_source=inputs["questions"],
        query_binding_source=inputs["binding"],
        query_result_source=inputs["result"],
        replay_receipt_source=inputs["receipt"],
        selected_reading_source=inputs["reading"],
        selected_ontology_source=inputs["ontology"],
        source_pdf_source=inputs["source"] if include_source_pdf else None,
        **kwargs,
    )


def test_committed_method_freezes_only_pre_v2_identities() -> None:
    protocol_source = PROTOCOL.read_bytes()
    protocol = json.loads(protocol_source)
    assert protocol["schema"] == PROTOCOL_SCHEMA
    assert protocol["status"] == "FROZEN_BEFORE_V2_QUERY_OUTPUT"
    assert protocol["fixed_identities"]["competency_questions_sha256"] == _digest(
        (ROOT / "paper-v4/experiment/competency-questions.json").read_bytes()
    )
    assert set(protocol["fixed_identities"]) == {
        "source_sha256",
        "selected_reading_sha256",
        "competency_questions_sha256",
    }
    assert set(
        protocol["review_input_manifest"]["stage_identity_template"].values()
    ) == {PENDING_STAGE_IDENTITY}
    blank_manifest = validate_blank_review_input_manifest(
        BLANK_MANIFEST.read_bytes(), protocol_source
    )
    assert blank_manifest["status"] == PENDING_STAGE_IDENTITY
    blank_record = validate_blank_human_review(
        BLANK_RECORD.read_bytes(), protocol_source
    )
    assert blank_record["inputs"] == {
        "review_protocol_sha256": _digest(protocol_source),
        "review_input_manifest_sha256": "",
    }


def test_preliminary_review_preserves_authored_labels_without_scoring() -> None:
    inputs = _inputs()
    record = _record(inputs)
    observed = _validate(record, inputs)
    assert observed == record
    assert [item["source_support"] for item in observed["questions"]] == [
        "SUPPORTED",
        "PARTIAL",
        "UNSUPPORTED",
        "NOT_EVALUABLE",
    ]
    assert "score" not in observed
    with pytest.raises(HumanReviewRefusal, match="human ratification is required"):
        _validate(record, inputs, require_human_ratification=True)


def test_selected_reading_is_authoritative_and_pdf_is_optional() -> None:
    inputs = _inputs()
    record = _record(inputs)
    assert _validate(record, inputs, include_source_pdf=False) == record
    protocol = json.loads(inputs["protocol"])
    assert protocol["evidence_surface"] == {
        "authoritative": "SELECTED_READING_TEXT_LAYER",
        "locator_kind": "SELECTED_READING_BLOCK_ID",
        "source_pdf_role": "OPTIONAL_PROJECTION_FIDELITY_CROSS_CHECK_ONLY",
    }


def test_luis_human_ratification_is_distinct_and_required_for_evidence() -> None:
    inputs = _inputs()
    record = _record(inputs, ratified=True)
    assert _validate(record, inputs, require_human_ratification=True) == record

    wrong_actor = deepcopy(record)
    wrong_actor["ratification"]["actor_id"] = "actor:not-luis"
    with pytest.raises(HumanReviewRefusal, match="declared human author"):
        _validate(wrong_actor, inputs, require_human_ratification=True)

    reversed_order = deepcopy(record)
    reversed_order["ratification"]["completed_at"] = "2026-09-03T00:02:03Z"
    with pytest.raises(HumanReviewRefusal, match="cannot precede"):
        _validate(reversed_order, inputs, require_human_ratification=True)


@pytest.mark.parametrize("field", ["score", "oracle", "canonical_answer"])
def test_answer_and_score_fields_are_forbidden_recursively(field: str) -> None:
    inputs = _inputs()
    record = _record(inputs)
    record["questions"][0][field] = "forbidden"
    with pytest.raises(HumanReviewRefusal, match="forbidden field"):
        _validate(record, inputs)


def test_review_must_bind_the_exact_frozen_manifest() -> None:
    inputs = _inputs()
    record = _record(inputs)
    record["inputs"]["review_input_manifest_sha256"] = "sha256:" + "9" * 64
    with pytest.raises(HumanReviewRefusal, match="input-manifest identity differs"):
        _validate(record, inputs)


def test_pending_manifest_cannot_authorize_review() -> None:
    inputs = _inputs()
    manifest = json.loads(inputs["manifest"])
    manifest["status"] = PENDING_STAGE_IDENTITY
    manifest["stage_identities"] = {
        field: PENDING_STAGE_IDENTITY for field in manifest["stage_identities"]
    }
    inputs["manifest"] = _json(manifest)
    record = _record(inputs)
    with pytest.raises(HumanReviewRefusal, match="must be frozen before review"):
        _validate(record, inputs)


@pytest.mark.parametrize("failure", ["missing-row", "unknown-locator"])
def test_every_row_and_source_locator_must_close(failure: str) -> None:
    inputs = _inputs()
    record = _record(inputs)
    if failure == "missing-row":
        record["questions"][0]["row_refs"] = []
        message = "cover every returned row"
    else:
        record["questions"][0]["source_locators"] = ["p999-b999"]
        message = "unknown blocks"
    with pytest.raises(HumanReviewRefusal, match=message):
        _validate(record, inputs)


@pytest.mark.parametrize(
    ("artifact", "message"),
    [
        ("source", "optional source PDF differs"),
        ("reading", "selected reading differs"),
        ("ontology", "selected ontology differs"),
        ("receipt", "replay receipt differs"),
        ("binding", "query binding differs"),
        ("result", "query result differs"),
    ],
)
def test_each_frozen_review_artifact_is_digest_checked(
    artifact: str, message: str
) -> None:
    inputs = _inputs()
    record = _record(inputs)
    inputs[artifact] += b"\n"
    with pytest.raises(HumanReviewRefusal, match=message):
        _validate(record, inputs)


def test_query_rows_must_come_from_the_frozen_replay_graph() -> None:
    inputs = _inputs()
    result = json.loads(inputs["result"])
    result["graph_state_digest"] = "sha256:" + "9" * 64
    inputs["result"] = _json(result)
    manifest = json.loads(inputs["manifest"])
    manifest["stage_identities"]["query_result_sha256"] = _digest(inputs["result"])
    inputs["manifest"] = _json(manifest)
    record = _record(inputs)
    with pytest.raises(HumanReviewRefusal, match="query result graph state differs"):
        _validate(record, inputs)
