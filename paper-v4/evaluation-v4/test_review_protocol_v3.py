"""Guards for review protocol v3: a declared evidence surface, coverage-derived
responsiveness, resolved row locators, control outcomes, and the v2 cells unchanged.

Protocol v3 is written for two consumers with different shapes: a document cell
whose surface is the selected reading's text layer, and a structured cell whose
surface is row-shaped source files. Both are exercised here from fixtures the
test writes, so the guards do not depend on a cell being open. The last test
runs the frozen v2 validation over every reviewed cell from run-13 to run-21,
because v3 supersedes v2 only for cells opened after it.
"""

from __future__ import annotations

import copy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def _module(name: str):
    spec = importlib.util.spec_from_file_location(
        f"paper_v4_evaluation_v4_{name}", HERE / f"{name}.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


review = _module("review")
ReviewRefusal = review.ReviewRefusal

PROTOCOL_V2 = HERE / "review-protocol-v2.json"
PROTOCOL_V3 = HERE / "review-protocol-v3.json"
TASK_V3 = HERE / "review-task-protocol-v3.template.md"
BLANK_V3 = HERE / "review-record-protocol-v3.blank.md"
READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"

# Every cell whose review was recorded under the frozen v2 protocol.
V2_REVIEWED_RUNS = ("13", "14", "15", "16", "19", "20", "21")


def _digest_bytes(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _digest(path: Path) -> str:
    return _digest_bytes(path.read_bytes())


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8")


def _wrap(record: dict[str, object]) -> bytes:
    body = json.dumps(record, ensure_ascii=False, indent=2)
    return f"# test record\n\n```json\n{body}\n```\n".encode("utf-8")


def _record_of(source: bytes) -> dict[str, object]:
    text = source.decode("utf-8")
    start = text.index("```json\n") + len("```json\n")
    end = text.index("\n```", start)
    return json.loads(text[start:end])


# --------------------------------------------------------------------------
# A structured-row cell, written here so the guard needs no open cell.
# --------------------------------------------------------------------------

INVOICES_CSV = b"invoice_id,amount,currency\nI1,100,EUR\nI2,250,EUR\n"
PAYMENTS_JSONL = (
    b'{"payment_id": "P1", "invoice_ids": ["I1", "I2"], "paid": 350}\n'
    b'{"payment_id": "P2", "invoice_ids": ["I2"], "paid": 250}\n'
)

ROW_QUESTIONS = {
    "schema": "malleus.paper-v4.competency-questions/v3",
    "status": "FROZEN_BEFORE_PRODUCER",
    "visibility": "WITHHELD_FROM_PRODUCER_UNTIL_POST_REPLAY",
    "scope": {
        "answer_surface": "REPLAY_DERIVED_NATIVE_GRAPH_QUERY_WITH_PROVENANCE_TRACE",
        "source_support": "THE_TWO_FIXTURE_SOURCE_FILES",
        "free_form_synthesis": "EXCLUDED",
    },
    "questions": [
        {
            "id": "CQ-R1",
            "question": "Which invoices did payment P1 settle?",
            "required_semantics": ["payment", "invoice"],
        },
        {
            "id": "CQ-R2",
            "question": "What amount and currency does invoice I1 carry?",
            "required_semantics": ["amount", "currency"],
        },
        {
            "id": "CQ-R3",
            "question": "Which carrier shipped invoice I2?",
            "required_semantics": ["shipping_carrier"],
            "expected_outcome": {"kind": "NOT_IN_SOURCE"},
        },
        {
            "id": "CQ-R4",
            "question": "Payment P1 settled which invoices?",
            "required_semantics": ["payment", "invoice"],
            "expected_outcome": {"kind": "PARAPHRASE", "of": "CQ-R1"},
        },
    ],
}

ROW_WITNESSES = {
    "CQ-R1": ["payment:P1", "invoice:I1", "rel:settles:1"],
    "CQ-R2": ["invoice:I1", "invoice:I2"],
    "CQ-R3": ["invoice:I2"],
    "CQ-R4": ["payment:P1", "invoice:I1"],
}

STAGE = {
    "accepted_ontology_sha256": "sha256:" + "a" * 64,
    "ledger_head": "sha256:" + "b" * 64,
    "population_trace_summary_sha256": "sha256:" + "c" * 64,
    "query_binding_sha256": "sha256:" + "d" * 64,
    "query_trace_summary_sha256": "sha256:" + "e" * 64,
    "replay_receipt_sha256": "sha256:" + "f" * 64,
}


def _row_query_result() -> bytes:
    queries = []
    for question_id, keys in ROW_WITNESSES.items():
        rows = []
        for key in keys:
            if key.startswith("rel:"):
                witness = {
                    "relation_id": key,
                    "source_id": "payment:P1",
                    "target_id": "invoice:I1",
                }
                kind = "RELATION"
            else:
                witness = {"record_id": key}
                kind = "ENTITY"
            rows.append({"case_ordinals": [1], "kind": kind, "witness": witness})
        queries.append(
            {"query_id": f"q:{question_id}", "question_id": question_id, "rows": rows}
        )
    result = {
        "schema": "malleus.paper-v4.query-result/v3",
        "graph_state_digest": "sha256:" + "9" * 64,
        "inputs": {
            "ledger_head": STAGE["ledger_head"],
            "query_binding_sha256": STAGE["query_binding_sha256"],
            "replay_receipt_sha256": STAGE["replay_receipt_sha256"],
        },
        "forbidden_attempts": {"embedding_import": 0, "file_read": 0, "network": 0},
        "queries": queries,
    }
    return _json_bytes(result)


ROW_QUERY_RESULT = _row_query_result()
ROW_QUESTIONS_BYTES = _json_bytes(ROW_QUESTIONS)
ROW_SOURCES = {
    "source:fixture:invoices": INVOICES_CSV,
    "source:fixture:payments": PAYMENTS_JSONL,
}


def _row_manifest(**overrides: object) -> dict[str, object]:
    sources = [
        {
            "source_id": "source:fixture:invoices",
            "path": "tests/fixtures/invoices.csv",
            "sha256": _digest_bytes(INVOICES_CSV),
            "format": "CSV",
        },
        {
            "source_id": "source:fixture:payments",
            "path": "tests/fixtures/payments.jsonl",
            "sha256": _digest_bytes(PAYMENTS_JSONL),
            "format": "JSONL",
        },
    ]
    manifest = {
        "schema": "malleus.paper-v4.source-grounded-review-inputs/v3",
        "status": "FROZEN_FOR_REVIEW",
        "run_id": "fixture-rows",
        "review_protocol_sha256": _digest(PROTOCOL_V3),
        "evidence_surface": {
            "kind": "STRUCTURED_ROWS",
            "locator_kind": "SOURCE_ROW_FIELD",
            "locator_convention": {
                "form": "SOURCE_ID_HASH_ROW_FIELD",
                "first_row_index": 0,
                "csv_header_is_a_row": False,
            },
            "sources": sources,
        },
        "fixed_identities": {
            "competency_questions_sha256": _digest_bytes(ROW_QUESTIONS_BYTES),
            "source_sha256": {item["source_id"]: item["sha256"] for item in sources},
        },
        "stage_identities": dict(
            STAGE, query_result_sha256=_digest_bytes(ROW_QUERY_RESULT)
        ),
        "materials": [
            {
                "name": "source:fixture:invoices",
                "path": "tests/fixtures/invoices.csv",
                "sha256": _digest_bytes(INVOICES_CSV),
                "visibility": "PUBLIC",
            },
            {
                "name": "source:fixture:payments",
                "path": "tests/fixtures/payments.jsonl",
                "sha256": _digest_bytes(PAYMENTS_JSONL),
                "visibility": "PUBLIC",
            },
            {
                "name": "competency_questions",
                "path": "tests/fixtures/competency-questions.json",
                "sha256": _digest_bytes(ROW_QUESTIONS_BYTES),
                "visibility": "PUBLIC",
            },
            {
                "name": "query_binding",
                "path": "tests/fixtures/native-query-binding.json",
                "sha256": STAGE["query_binding_sha256"],
                "visibility": "PUBLIC",
            },
            {
                "name": "query_result",
                "path": "tests/fixtures/query-result.json",
                "sha256": _digest_bytes(ROW_QUERY_RESULT),
                "visibility": "PUBLIC",
            },
            {
                "name": "population_trace",
                "path": "tests/fixtures/trace-summary.json",
                "sha256": STAGE["population_trace_summary_sha256"],
                "visibility": "PUBLIC",
            },
            {
                "name": "query_trace_summary",
                "path": "tests/fixtures/query-trace-summary.json",
                "sha256": STAGE["query_trace_summary_sha256"],
                "visibility": "PUBLIC",
            },
        ],
        "question_ids": ["CQ-R1", "CQ-R2", "CQ-R3", "CQ-R4"],
        "rows_per_question": {
            key: len(value) for key, value in ROW_WITNESSES.items()
        },
        "witnesses_traced": 4,
        "authorship": {
            "preliminary_evaluator_kind": "CLAUDE_PRELIMINARY",
            "ratifier_evaluator_kind": "HUMAN_AUTHOR",
            "ratifier_actor_id": "actor:luis",
        },
    }
    manifest.update(overrides)
    return manifest


def _row_record() -> dict[str, object]:
    witnesses = [
        {
            "witness_key": "payment:P1",
            "source_support": "SUPPORTED",
            "resolution": "VALUE_MATCHES_ROW",
            "source_locators": ["source:fixture:payments#row:0:payment_id"],
            "rationale": "the payment identifier is the field the derivation names",
        },
        {
            "witness_key": "invoice:I1",
            "source_support": "SUPPORTED",
            "resolution": "VALUE_MATCHES_ROW",
            "source_locators": ["source:fixture:invoices#row:0:invoice_id"],
            "rationale": "the invoice identifier is the field the derivation names",
        },
        {
            "witness_key": "rel:settles:1",
            "source_support": "SUPPORTED",
            "resolution": "VALUE_DERIVED_FROM_ROW",
            "source_locators": ["source:fixture:payments#row:0:invoice_ids[0]"],
            "rationale": "the endpoint is the row value under an identifier prefix",
        },
        {
            "witness_key": "invoice:I2",
            "source_support": "NOT_EVALUABLE",
            "resolution": "LOCATOR_NOT_RESOLVABLE",
            "source_locators": ["source:fixture:invoices#row:7:invoice_id"],
            "rationale": "the cited row is past the end of the file",
        },
    ]
    questions = []
    coverage = {
        "CQ-R1": [
            {"semantic": "payment", "row_index": 0, "absent_reason": None, "note": ""},
            {"semantic": "invoice", "row_index": 1, "absent_reason": None, "note": ""},
        ],
        "CQ-R2": [
            {"semantic": "amount", "row_index": 0, "absent_reason": None, "note": ""},
            {
                "semantic": "currency",
                "row_index": None,
                "absent_reason": "NOT_MODELLED",
                "note": "no projected field carries the currency",
            },
        ],
        "CQ-R3": [
            {
                "semantic": "shipping_carrier",
                "row_index": None,
                "absent_reason": "NOT_IN_SOURCE",
                "note": "neither source file names a carrier",
            }
        ],
        "CQ-R4": [
            {"semantic": "payment", "row_index": 0, "absent_reason": None, "note": ""},
            {"semantic": "invoice", "row_index": 1, "absent_reason": None, "note": ""},
        ],
    }
    stated = {
        "CQ-R1": "COVERED",
        "CQ-R2": "PARTIAL",
        "CQ-R3": "NONE",
        "CQ-R4": "COVERED",
    }
    assembly = {
        "CQ-R1": "LINKED_ROWS",
        "CQ-R2": "ONE_ROW",
        "CQ-R3": "ONE_ROW",
        "CQ-R4": "UNLINKED_ROWS",
    }
    for question_id, keys in ROW_WITNESSES.items():
        questions.append(
            {
                "question_id": question_id,
                "question_responsiveness": stated[question_id],
                "responsiveness_rationale": "coverage read from the rows",
                "assembly": assembly[question_id],
                "coverage": coverage[question_id],
                "source_locators": ["source:fixture:invoices#row:0:invoice_id"],
                "rows": [
                    {"row_index": index, "witness_key": key}
                    for index, key in enumerate(keys)
                ],
            }
        )
    return {
        "schema": "malleus.paper-v4.source-grounded-review/v3",
        "status": "PRELIMINARY_COMPLETE",
        "inputs": {
            "review_protocol_sha256": _digest(PROTOCOL_V3),
            "review_input_manifest_sha256": "",
        },
        "preliminary": {
            "evaluator_kind": "CLAUDE_PRELIMINARY",
            "actor_id": "actor:claude-preliminary-fixture",
            "completed_at": "2026-09-06T12:00:00Z",
        },
        "witnesses": witnesses,
        "questions": questions,
        "ratification": {
            "evaluator_kind": "HUMAN_AUTHOR",
            "actor_id": "actor:luis",
            "disposition": "PENDING",
            "completed_at": "",
            "notes": "",
        },
    }


def _validate_rows(
    record: dict[str, object] | None = None,
    manifest: dict[str, object] | None = None,
    **kwargs: object,
) -> dict[str, object]:
    manifest = _row_manifest() if manifest is None else manifest
    manifest_bytes = _json_bytes(manifest)
    record = _row_record() if record is None else record
    record["inputs"]["review_input_manifest_sha256"] = _digest_bytes(manifest_bytes)
    return review.validate_review(
        _wrap(record),
        PROTOCOL_V3.read_bytes(),
        review_input_manifest_source=manifest_bytes,
        query_result_source=ROW_QUERY_RESULT,
        competency_questions_source=ROW_QUESTIONS_BYTES,
        surface_sources=ROW_SOURCES,
        **kwargs,
    )


# --------------------------------------------------------------------------
# A text-layer cell, in the same shape the document cells use.
# --------------------------------------------------------------------------

TEXT_SOURCE_DIGEST = "sha256:" + "1" * 64
TEXT_READING = {
    "schema": "malleus.paper-v4.selected-reading/v1",
    "source_sha256": TEXT_SOURCE_DIGEST,
    "pages": [
        {
            "page": 1,
            "blocks": [
                {"id": "page:1:block:001", "text": "the campaign deployed instruments"},
                {"id": "page:1:block:002", "text": "the events sit beneath the axis"},
            ],
        }
    ],
}
TEXT_READING_BYTES = _json_bytes(TEXT_READING)
TEXT_QUESTIONS = {
    "schema": "malleus.paper-v4.competency-questions/v3",
    "status": "FROZEN_BEFORE_PRODUCER",
    "visibility": "WITHHELD_FROM_PRODUCER_UNTIL_POST_REPLAY",
    "scope": {
        "answer_surface": "REPLAY_DERIVED_NATIVE_GRAPH_QUERY_WITH_PROVENANCE_TRACE",
        "source_support": "SELECTED_READING_TEXT_LAYER",
        "free_form_synthesis": "EXCLUDED",
    },
    "questions": [
        {
            "id": "CQ-T1",
            "question": "Which campaign deployed the instruments?",
            "required_semantics": ["campaign", "instrument"],
        }
    ],
}
TEXT_QUESTIONS_BYTES = _json_bytes(TEXT_QUESTIONS)
TEXT_WITNESSES = {"CQ-T1": ["obs:campaign", "obs:instrument"]}


def _text_query_result() -> bytes:
    queries = [
        {
            "query_id": "q:CQ-T1",
            "question_id": "CQ-T1",
            "rows": [
                {"case_ordinals": [1], "kind": "ENTITY", "witness": {"record_id": key}}
                for key in TEXT_WITNESSES["CQ-T1"]
            ],
        }
    ]
    return _json_bytes(
        {
            "schema": "malleus.paper-v4.query-result/v3",
            "graph_state_digest": "sha256:" + "8" * 64,
            "inputs": {
                "ledger_head": STAGE["ledger_head"],
                "query_binding_sha256": STAGE["query_binding_sha256"],
                "replay_receipt_sha256": STAGE["replay_receipt_sha256"],
            },
            "forbidden_attempts": {
                "embedding_import": 0,
                "file_read": 0,
                "network": 0,
            },
            "queries": queries,
        }
    )


TEXT_QUERY_RESULT = _text_query_result()


def _text_manifest() -> dict[str, object]:
    names = [
        "selected_reading",
        "competency_questions",
        "query_binding",
        "query_result",
        "population_trace",
        "retained_capture",
        "query_trace_summary",
    ]
    return {
        "schema": "malleus.paper-v4.source-grounded-review-inputs/v3",
        "status": "FROZEN_FOR_REVIEW",
        "run_id": "fixture-text",
        "review_protocol_sha256": _digest(PROTOCOL_V3),
        "evidence_surface": {
            "kind": "SELECTED_READING_TEXT_LAYER",
            "locator_kind": "SELECTED_READING_BLOCK_ID",
        },
        "fixed_identities": {
            "competency_questions_sha256": _digest_bytes(TEXT_QUESTIONS_BYTES),
            "selected_reading_sha256": _digest_bytes(TEXT_READING_BYTES),
            "source_sha256": TEXT_SOURCE_DIGEST,
        },
        "stage_identities": dict(
            STAGE, query_result_sha256=_digest_bytes(TEXT_QUERY_RESULT)
        ),
        "materials": [
            {
                "name": name,
                "path": f"tests/fixtures/{name}.json",
                "sha256": "sha256:" + "7" * 64,
                "visibility": "PUBLIC",
            }
            for name in names
        ],
        "question_ids": ["CQ-T1"],
        "rows_per_question": {"CQ-T1": 2},
        "witnesses_traced": 2,
        "authorship": {
            "preliminary_evaluator_kind": "CLAUDE_PRELIMINARY",
            "ratifier_evaluator_kind": "HUMAN_AUTHOR",
            "ratifier_actor_id": "actor:luis",
        },
    }


def _text_record() -> dict[str, object]:
    return {
        "schema": "malleus.paper-v4.source-grounded-review/v3",
        "status": "PRELIMINARY_COMPLETE",
        "inputs": {
            "review_protocol_sha256": _digest(PROTOCOL_V3),
            "review_input_manifest_sha256": "",
        },
        "preliminary": {
            "evaluator_kind": "CLAUDE_PRELIMINARY",
            "actor_id": "actor:claude-preliminary-fixture",
            "completed_at": "2026-09-06T12:00:00Z",
        },
        "witnesses": [
            {
                "witness_key": "obs:campaign",
                "source_support": "SUPPORTED",
                "source_locators": ["page:1:block:001"],
                "rationale": "the block names the campaign",
            },
            {
                "witness_key": "obs:instrument",
                "source_support": "SUPPORTED",
                "source_locators": ["page:1:block:001"],
                "rationale": "the block names the instruments",
            },
        ],
        "questions": [
            {
                "question_id": "CQ-T1",
                "question_responsiveness": "COVERED",
                "responsiveness_rationale": "both semantics reach a supported row",
                "assembly": "LINKED_ROWS",
                "coverage": [
                    {
                        "semantic": "campaign",
                        "row_index": 0,
                        "absent_reason": None,
                        "note": "",
                    },
                    {
                        "semantic": "instrument",
                        "row_index": 1,
                        "absent_reason": None,
                        "note": "",
                    },
                ],
                "source_locators": ["page:1:block:001"],
                "rows": [
                    {"row_index": 0, "witness_key": "obs:campaign"},
                    {"row_index": 1, "witness_key": "obs:instrument"},
                ],
            }
        ],
        "ratification": {
            "evaluator_kind": "HUMAN_AUTHOR",
            "actor_id": "actor:luis",
            "disposition": "PENDING",
            "completed_at": "",
            "notes": "",
        },
    }


def _validate_text(
    record: dict[str, object] | None = None, **kwargs: object
) -> dict[str, object]:
    manifest_bytes = _json_bytes(_text_manifest())
    record = _text_record() if record is None else record
    record["inputs"]["review_input_manifest_sha256"] = _digest_bytes(manifest_bytes)
    return review.validate_review(
        _wrap(record),
        PROTOCOL_V3.read_bytes(),
        review_input_manifest_source=manifest_bytes,
        query_result_source=TEXT_QUERY_RESULT,
        competency_questions_source=TEXT_QUESTIONS_BYTES,
        selected_reading_source=TEXT_READING_BYTES,
        **kwargs,
    )


# --------------------------------------------------------------------------
# The protocol file itself
# --------------------------------------------------------------------------


def test_the_v3_protocol_declares_its_sets_and_supersedes_v2() -> None:
    protocol = review.validate_protocol(PROTOCOL_V3.read_bytes())

    assert protocol["schema"] == "malleus.paper-v4.source-grounded-review-protocol/v3"
    assert protocol["evidence_surface"]["declared_by"] == "REVIEW_INPUT_MANIFEST"
    assert set(protocol["evidence_surface"]["surface_kinds"]) == {
        "SELECTED_READING_TEXT_LAYER",
        "STRUCTURED_ROWS",
    }
    judgments = protocol["judgments"]
    assert judgments["source_support"] == [
        "SUPPORTED",
        "PARTIAL",
        "UNSUPPORTED",
        "NOT_EVALUABLE",
    ]
    assert judgments["coverage_absent_reasons"] == [
        "NOT_MODELLED",
        "WITHHELD_STATEMENT",
        "UNREACHED_RECORD",
        "NOT_IN_SOURCE",
        "LOCATOR_NOT_RESOLVABLE",
    ]
    assert judgments["question_responsiveness"] == ["COVERED", "PARTIAL", "NONE"]
    assert judgments["question_responsiveness_is"] == "DERIVED_BY_THE_VALIDATOR"
    assert judgments["assembly"] == ["ONE_ROW", "LINKED_ROWS", "UNLINKED_ROWS"]
    assert protocol["supersedes"]["sha256"] == _digest(PROTOCOL_V2)
    assert protocol["supersedes"]["binds"] == "CELLS_OPENED_AFTER_THIS_FILE_IS_FROZEN"


def test_v3_keeps_what_v2_fixed() -> None:
    v2 = json.loads(PROTOCOL_V2.read_bytes())
    v3 = json.loads(PROTOCOL_V3.read_bytes())

    assert v3["forbidden_record_fields"] == v2["forbidden_record_fields"]
    assert v3["withheld_from_producer"] == v2["withheld_from_producer"]
    assert v3["authorship"]["ratifier_evaluator_kind"] == "HUMAN_AUTHOR"
    assert v3["authorship"]["ratifier_actor_id"] == "actor:luis"
    text_materials = v3["review_materials"]["required"]["SELECTED_READING_TEXT_LAYER"]
    assert text_materials == v2["review_materials"]
    assert "retained_capture" in text_materials
    assert "query_trace_summary" in text_materials


# --------------------------------------------------------------------------
# The declared surface
# --------------------------------------------------------------------------


def test_a_v3_manifest_declares_a_row_surface() -> None:
    manifest = review.validate_review_input_manifest(
        _json_bytes(_row_manifest()), PROTOCOL_V3.read_bytes()
    )

    surface = manifest["evidence_surface"]
    assert surface["kind"] == "STRUCTURED_ROWS"
    assert surface["locator_kind"] == "SOURCE_ROW_FIELD"
    assert surface["locator_convention"]["first_row_index"] == 0
    assert surface["locator_convention"]["csv_header_is_a_row"] is False
    assert [item["source_id"] for item in surface["sources"]] == [
        "source:fixture:invoices",
        "source:fixture:payments",
    ]


def test_a_v3_manifest_declares_a_text_layer_surface() -> None:
    manifest = review.validate_review_input_manifest(
        _json_bytes(_text_manifest()), PROTOCOL_V3.read_bytes()
    )

    assert manifest["evidence_surface"]["kind"] == "SELECTED_READING_TEXT_LAYER"
    assert manifest["evidence_surface"]["locator_kind"] == "SELECTED_READING_BLOCK_ID"


def test_a_manifest_naming_an_unknown_surface_kind_is_refused() -> None:
    manifest = _row_manifest()
    manifest["evidence_surface"]["kind"] = "A_SURFACE_NOBODY_DECLARED"

    with pytest.raises(ReviewRefusal, match="surface"):
        review.validate_review_input_manifest(
            _json_bytes(manifest), PROTOCOL_V3.read_bytes()
        )


def test_a_row_record_is_accepted_on_the_declared_surface() -> None:
    record = _validate_rows()

    assert record["status"] == "PRELIMINARY_COMPLETE"
    assert [item["witness_key"] for item in record["witnesses"]] == [
        "payment:P1",
        "invoice:I1",
        "rel:settles:1",
        "invoice:I2",
    ]


def test_a_text_record_is_accepted_on_the_declared_surface() -> None:
    record = _validate_text()

    assert record["status"] == "PRELIMINARY_COMPLETE"
    assert record["questions"][0]["question_responsiveness"] == "COVERED"


def test_a_text_record_cannot_cite_a_block_outside_the_reading() -> None:
    record = _text_record()
    record["witnesses"][0]["source_locators"] = ["page:9:block:001"]

    with pytest.raises(ReviewRefusal, match="unknown"):
        _validate_text(record)


def test_a_row_record_cannot_cite_a_block_id() -> None:
    record = _row_record()
    record["witnesses"][0]["source_locators"] = ["page:1:block:001"]

    with pytest.raises(ReviewRefusal, match="locator"):
        _validate_rows(record)


# --------------------------------------------------------------------------
# Locator resolution under a declared convention
# --------------------------------------------------------------------------


def test_a_row_locator_is_resolved_against_the_source_file() -> None:
    record = _row_record()
    record["witnesses"][1]["source_locators"] = [
        "source:fixture:invoices#row:1:invoice_id"
    ]

    assert _validate_rows(record)["witnesses"][1]["resolution"] == "VALUE_MATCHES_ROW"


def test_the_declared_convention_decides_whether_a_locator_resolves() -> None:
    manifest = _row_manifest()
    manifest["evidence_surface"]["locator_convention"] = {
        "form": "SOURCE_ID_HASH_ROW_FIELD",
        "first_row_index": 1,
        "csv_header_is_a_row": True,
    }

    # row:0 is before the first row under this convention, and row:7 is still
    # past the end, so the record written for the zero-based convention is
    # refused rather than silently re-read.
    with pytest.raises(ReviewRefusal, match="does not resolve"):
        _validate_rows(manifest=manifest)


def test_a_record_claiming_a_value_match_on_an_unresolvable_locator_is_refused() -> None:
    record = _row_record()
    record["witnesses"][0]["source_locators"] = [
        "source:fixture:payments#row:9:payment_id"
    ]

    with pytest.raises(ReviewRefusal, match="does not resolve"):
        _validate_rows(record)


def test_a_record_claiming_an_unresolvable_locator_that_resolves_is_refused() -> None:
    record = _row_record()
    record["witnesses"][3]["source_locators"] = [
        "source:fixture:invoices#row:1:invoice_id"
    ]

    with pytest.raises(ReviewRefusal, match="resolves"):
        _validate_rows(record)


def test_a_locator_naming_an_undeclared_source_is_refused() -> None:
    record = _row_record()
    record["witnesses"][0]["source_locators"] = ["source:fixture:ledger#row:0:amount"]

    with pytest.raises(ReviewRefusal, match="source"):
        _validate_rows(record)


# --------------------------------------------------------------------------
# The unresolvable-locator rule (E-0204)
# --------------------------------------------------------------------------


def test_an_unresolvable_locator_is_not_evaluable_by_rule() -> None:
    record = _validate_rows()
    unresolvable = record["witnesses"][3]

    assert unresolvable["resolution"] == "LOCATOR_NOT_RESOLVABLE"
    assert unresolvable["source_support"] == "NOT_EVALUABLE"
    assert unresolvable["rationale"].strip()


@pytest.mark.parametrize("label", ["PARTIAL", "UNSUPPORTED", "SUPPORTED"])
def test_an_unresolvable_locator_cannot_be_labelled_anything_else(label: str) -> None:
    record = _row_record()
    record["witnesses"][3]["source_support"] = label

    with pytest.raises(ReviewRefusal, match="NOT_EVALUABLE"):
        _validate_rows(record)


def test_an_unresolvable_locator_must_record_its_reason() -> None:
    record = _row_record()
    record["witnesses"][3]["rationale"] = "   "

    with pytest.raises(ReviewRefusal, match="rationale"):
        _validate_rows(record)


# --------------------------------------------------------------------------
# Coverage and the derived label
# --------------------------------------------------------------------------


def test_responsiveness_is_derived_from_coverage() -> None:
    record = _validate_rows()
    labels = {
        question["question_id"]: question["question_responsiveness"]
        for question in record["questions"]
    }

    assert labels == {
        "CQ-R1": "COVERED",
        "CQ-R2": "PARTIAL",
        "CQ-R3": "NONE",
        "CQ-R4": "COVERED",
    }
    assert review.derived_responsiveness(record["questions"][0]["coverage"]) == "COVERED"
    assert review.derived_responsiveness(record["questions"][1]["coverage"]) == "PARTIAL"
    assert review.derived_responsiveness(record["questions"][2]["coverage"]) == "NONE"


def test_a_stated_label_the_derivation_does_not_produce_is_refused() -> None:
    record = _row_record()
    record["questions"][1]["question_responsiveness"] = "COVERED"

    with pytest.raises(ReviewRefusal, match="derivation"):
        _validate_rows(record)


def test_coverage_must_name_every_required_semantic_in_order() -> None:
    record = _row_record()
    record["questions"][0]["coverage"] = record["questions"][0]["coverage"][:1]

    with pytest.raises(ReviewRefusal, match="required_semantics"):
        _validate_rows(record)


def test_an_absent_semantic_needs_one_typed_reason() -> None:
    record = _row_record()
    record["questions"][1]["coverage"][1]["absent_reason"] = "BECAUSE_I_SAY_SO"

    with pytest.raises(ReviewRefusal, match="absent_reason"):
        _validate_rows(record)


def test_a_covered_semantic_cannot_name_both_a_row_and_a_reason() -> None:
    record = _row_record()
    record["questions"][0]["coverage"][0]["absent_reason"] = "NOT_MODELLED"

    with pytest.raises(ReviewRefusal, match="either"):
        _validate_rows(record)


def test_a_covered_semantic_must_name_a_supported_or_derived_row() -> None:
    record = _row_record()
    # invoice:I2 is NOT_EVALUABLE, so row 1 of CQ-R2 cannot carry a semantic.
    record["questions"][1]["coverage"][1] = {
        "semantic": "currency",
        "row_index": 1,
        "absent_reason": None,
        "note": "",
    }
    record["questions"][1]["question_responsiveness"] = "COVERED"

    with pytest.raises(ReviewRefusal, match="SUPPORTED"):
        _validate_rows(record)


def test_a_derived_row_may_carry_a_semantic() -> None:
    record = _row_record()
    record["questions"][0]["coverage"][1] = {
        "semantic": "invoice",
        "row_index": 2,
        "absent_reason": None,
        "note": "the relation endpoint is derived from the row",
    }

    assert _validate_rows(record)["questions"][0]["question_responsiveness"] == "COVERED"


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------


def test_assembly_is_recorded_and_never_moves_a_label() -> None:
    record = _row_record()
    record["questions"][0]["assembly"] = "UNLINKED_ROWS"

    validated = _validate_rows(record)

    assert validated["questions"][0]["assembly"] == "UNLINKED_ROWS"
    assert validated["questions"][0]["question_responsiveness"] == "COVERED"


def test_an_unknown_assembly_descriptor_is_refused() -> None:
    record = _row_record()
    record["questions"][0]["assembly"] = "SOME_ROWS"

    with pytest.raises(ReviewRefusal, match="assembly"):
        _validate_rows(record)


# --------------------------------------------------------------------------
# Witnesses judged once
# --------------------------------------------------------------------------


def test_a_witness_is_judged_once_and_referenced_by_the_rows_that_share_it() -> None:
    record = _validate_rows()

    keys = [item["witness_key"] for item in record["witnesses"]]
    assert len(keys) == len(set(keys)) == 4
    shared = [
        question["rows"][0]["witness_key"]
        for question in record["questions"]
        if question["question_id"] in {"CQ-R1", "CQ-R4"}
    ]
    assert shared == ["payment:P1", "payment:P1"]


def test_a_witness_judged_twice_is_refused() -> None:
    record = _row_record()
    record["witnesses"].append(copy.deepcopy(record["witnesses"][0]))

    with pytest.raises(ReviewRefusal, match="once"):
        _validate_rows(record)


def test_a_row_naming_a_witness_the_query_result_does_not_return_is_refused() -> None:
    record = _row_record()
    record["questions"][0]["rows"][0]["witness_key"] = "payment:P9"

    with pytest.raises(ReviewRefusal, match="witness"):
        _validate_rows(record)


def test_every_returned_row_must_be_judged_in_order() -> None:
    record = _row_record()
    record["questions"][0]["rows"] = record["questions"][0]["rows"][:-1]

    with pytest.raises(ReviewRefusal, match="every returned row"):
        _validate_rows(record)


# --------------------------------------------------------------------------
# Controls
# --------------------------------------------------------------------------


def test_control_outcomes_are_reported_as_findings() -> None:
    findings: list[dict[str, object]] = []
    _validate_rows(findings=findings)

    by_id = {item["question_id"]: item for item in findings}
    assert set(by_id) == {"CQ-R3", "CQ-R4"}
    assert by_id["CQ-R3"]["kind"] == "NOT_IN_SOURCE"
    assert by_id["CQ-R3"]["expected"] == "NONE"
    assert by_id["CQ-R3"]["observed"] == "NONE"
    assert by_id["CQ-R3"]["matched"] is True
    assert by_id["CQ-R4"]["kind"] == "PARAPHRASE"
    assert by_id["CQ-R4"]["of"] == "CQ-R1"
    assert by_id["CQ-R4"]["matched"] is True


def test_a_control_whose_outcome_differs_is_reported_and_refuses_nothing() -> None:
    record = _row_record()
    record["questions"][3]["coverage"][1] = {
        "semantic": "invoice",
        "row_index": None,
        "absent_reason": "UNREACHED_RECORD",
        "note": "the paraphrase reaches no invoice row",
    }
    record["questions"][3]["question_responsiveness"] = "PARTIAL"
    findings: list[dict[str, object]] = []

    validated = _validate_rows(record, findings=findings)

    by_id = {item["question_id"]: item for item in findings}
    assert validated["questions"][3]["question_responsiveness"] == "PARTIAL"
    assert by_id["CQ-R4"]["expected"] == "COVERED"
    assert by_id["CQ-R4"]["observed"] == "PARTIAL"
    assert by_id["CQ-R4"]["matched"] is False


def test_control_outcomes_can_be_read_without_validating() -> None:
    findings = review.control_outcomes(_row_record(), ROW_QUESTIONS_BYTES)

    assert [item["question_id"] for item in findings] == ["CQ-R3", "CQ-R4"]


# --------------------------------------------------------------------------
# Version dispatch
# --------------------------------------------------------------------------


def test_a_v3_record_under_the_v2_protocol_is_refused() -> None:
    manifest_bytes = _json_bytes(_row_manifest())

    with pytest.raises(ReviewRefusal):
        review.validate_review(
            _wrap(_row_record()),
            PROTOCOL_V2.read_bytes(),
            review_input_manifest_source=manifest_bytes,
            query_result_source=ROW_QUERY_RESULT,
            selected_reading_source=TEXT_READING_BYTES,
        )


def test_a_record_whose_schema_disagrees_with_the_protocol_is_refused() -> None:
    record = _row_record()
    record["schema"] = "malleus.paper-v4.source-grounded-review/v2"

    with pytest.raises(ReviewRefusal, match="schema"):
        _validate_rows(record)


def test_a_protocol_of_an_unknown_version_is_refused() -> None:
    protocol = json.loads(PROTOCOL_V3.read_bytes())
    protocol["schema"] = "malleus.paper-v4.source-grounded-review-protocol/v9"

    with pytest.raises(ReviewRefusal, match="protocol"):
        review.validate_protocol(_json_bytes(protocol))


# --------------------------------------------------------------------------
# The v3 task template and blank record
# --------------------------------------------------------------------------


def test_the_v3_task_template_states_the_protocol_it_implements() -> None:
    task = " ".join(TASK_V3.read_text(encoding="utf-8").split())

    assert "review-protocol-v3.json" in task
    assert "STRUCTURED_ROWS" in task
    assert "SELECTED_READING_TEXT_LAYER" in task
    assert "VALUE_DERIVED_FROM_ROW" in task
    assert "LOCATOR_NOT_RESOLVABLE" in task
    assert "NOT_EVALUABLE" in task
    assert "required_semantics" in task
    assert "ONE_ROW" in task and "LINKED_ROWS" in task and "UNLINKED_ROWS" in task
    assert "Do not calculate a score" in task
    assert "Luis" in task
    assert "{{ROWS_TOTAL}}" in task
    assert "{{WITNESSES_TOTAL}}" in task


def test_the_v3_blank_record_carries_placeholders_and_no_judgment() -> None:
    text = BLANK_V3.read_text(encoding="utf-8")
    record = _record_of(BLANK_V3.read_bytes())

    assert "{{ROWS_TOTAL}}" in text
    assert "{{WITNESSES_TOTAL}}" in text
    assert record["schema"] == "malleus.paper-v4.source-grounded-review/v3"
    assert record["status"] == "BLANK"
    assert record["witnesses"] == []
    assert record["inputs"]["review_input_manifest_sha256"] == ""
    for question in record["questions"]:
        assert question["question_responsiveness"] == "PENDING"
        assert question["assembly"] == "PENDING"
        assert question["coverage"] == []
        assert question["rows"] == []
        assert question["source_locators"] == []


def test_an_instantiated_v3_blank_validates_as_blank() -> None:
    manifest_bytes = _json_bytes(_row_manifest())
    blank = _record_of(BLANK_V3.read_bytes())
    blank["inputs"]["review_protocol_sha256"] = _digest(PROTOCOL_V3)
    blank["questions"] = [
        dict(copy.deepcopy(blank["questions"][0]), question_id=question_id)
        for question_id in ["CQ-R1", "CQ-R2", "CQ-R3", "CQ-R4"]
    ]

    validated = review.validate_blank_review(
        _wrap(blank), PROTOCOL_V3.read_bytes(), manifest_bytes
    )

    assert validated["status"] == "BLANK"


# --------------------------------------------------------------------------
# The v2 cells, unchanged
# --------------------------------------------------------------------------


@pytest.mark.parametrize("run", V2_REVIEWED_RUNS)
@pytest.mark.parametrize("name", ["preliminary", "human"])
def test_every_frozen_v2_record_is_still_accepted(run: str, name: str) -> None:
    cell = ROOT / f"paper-v4/evaluation-v4/run-{run}"
    record = review.validate_review(
        (cell / f"review-record.{name}.md").read_bytes(),
        PROTOCOL_V2.read_bytes(),
        review_input_manifest_source=(cell / "review-input-manifest.json").read_bytes(),
        query_result_source=(
            ROOT / f"private/paper-v4-v4-run-{run}/query/query-result.json"
        ).read_bytes(),
        selected_reading_source=READING.read_bytes(),
    )

    assert record["schema"] == "malleus.paper-v4.source-grounded-review/v2"
    assert record["status"] in {"PRELIMINARY_COMPLETE", "HUMAN_RATIFIED"}


@pytest.mark.parametrize("run", V2_REVIEWED_RUNS)
def test_every_frozen_v2_blank_is_still_accepted(run: str) -> None:
    cell = ROOT / f"paper-v4/evaluation-v4/run-{run}"

    for name in ("review-record.blank.md", f"review-record.run-{run}.blank.md"):
        record = review.validate_blank_review(
            (cell / name).read_bytes(),
            PROTOCOL_V2.read_bytes(),
            (cell / "review-input-manifest.json").read_bytes(),
        )
        assert record["status"] == "BLANK"


def test_the_active_gate_collects_this_guard() -> None:
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())

    assert "paper-v4/evaluation-v4" in manifest["paths"]
