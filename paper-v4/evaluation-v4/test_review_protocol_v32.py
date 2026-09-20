"""Guards for review protocol v3.2: a sixth absence code, stage identities per
surface kind, and a third surface whose witness is one cited claim.

The first guard is the one that matters most and it runs first: the four
validated v3 records the paper reports still validate, byte-identical, against
the v3 protocol file, which is not edited. Dispatch is per file on the schema
each declares (`review.py` `_protocol_version`), so a v3 protocol, manifest and
record never meet a v3.2 branch; this file proves that rather than asserting it.

The answer-set fixtures are written here, so the guards do not depend on the
baseline cell having run.
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

PROTOCOL_V3 = HERE / "review-protocol-v3.json"
PROTOCOL_V32 = HERE / "review-protocol-v3.2.json"
READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"

# The four validated v3 records the paper reports, each with the cell directory
# that carries its manifest, the query result it was reviewed against and the
# competency question file its own manifest binds by digest.
V3_CELLS = {
    "run-22": (
        "paper-v4/evaluation-v4/run-22-v413",
        "private/paper-v4-v4-run-22/rebind-v4.13/query-result.json",
        "paper-v4/experiment-v4/competency-questions-v3.json",
    ),
    "run-23": (
        "paper-v4/evaluation-v4/run-23",
        "private/paper-v4-v4-run-23/query/query-result.json",
        "paper-v4/experiment-v4/competency-questions-v3.json",
    ),
    "run-24": (
        "paper-v4/evaluation-v4/run-24",
        "private/paper-v4-v4-run-24/query/query-result.json",
        "paper-v4/experiment-v4/competency-questions-v3.1.json",
    ),
    "run-25": (
        "paper-v4/evaluation-v4/run-25",
        "private/paper-v4-v4-run-25/query/query-result.json",
        "paper-v4/experiment-v4/competency-questions-v3.1.json",
    ),
}


def _baseline_module(name: str):
    spec = importlib.util.spec_from_file_location(
        f"paper_v4_baseline_01_{name}",
        ROOT / f"paper-v4/experiment-v4/baseline-01/{name}.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _digest_bytes(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _digest(path: Path) -> str:
    return _digest_bytes(path.read_bytes())


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8")


def _wrap(record: dict[str, object]) -> bytes:
    body = json.dumps(record, ensure_ascii=False, indent=2)
    return f"# test record\n\n```json\n{body}\n```\n".encode("utf-8")


# --------------------------------------------------------------------------
# The frozen v3 cells, unchanged
# --------------------------------------------------------------------------


@pytest.mark.parametrize("cell", sorted(V3_CELLS))
def test_every_validated_v3_record_still_validates_byte_identical(cell: str) -> None:
    directory, query_result, questions = V3_CELLS[cell]
    record_path = ROOT / directory / "review-record.preliminary.md"
    manifest_path = ROOT / directory / "review-input-manifest.json"
    before = {
        path: _digest(path)
        for path in (record_path, manifest_path, PROTOCOL_V3, READING)
    }

    findings: list[dict[str, object]] = []
    record = review.validate_review(
        record_path.read_bytes(),
        PROTOCOL_V3.read_bytes(),
        review_input_manifest_source=manifest_path.read_bytes(),
        query_result_source=(ROOT / query_result).read_bytes(),
        selected_reading_source=READING.read_bytes(),
        competency_questions_source=(ROOT / questions).read_bytes(),
        findings=findings,
    )

    assert record["schema"] == "malleus.paper-v4.source-grounded-review/v3"
    assert record["status"] == "PRELIMINARY_COMPLETE"
    assert len(findings) == 5
    assert {path: _digest(path) for path in before} == before


def test_the_v3_protocol_file_is_not_edited() -> None:
    """v3.2 supersedes by a new file, and names the bytes it supersedes."""

    v32 = json.loads(PROTOCOL_V32.read_bytes())

    assert v32["supersedes"]["protocol_file"] == (
        "paper-v4/evaluation-v4/review-protocol-v3.json"
    )
    assert v32["supersedes"]["sha256"] == _digest(PROTOCOL_V3)
    assert review.validate_protocol(PROTOCOL_V3.read_bytes())["status"] == (
        "FROZEN_BEFORE_NEXT_CELL"
    )


def test_v3_keeps_its_five_absence_codes() -> None:
    protocol = review.validate_protocol(PROTOCOL_V3.read_bytes())

    assert protocol["judgments"]["coverage_absent_reasons"] == [
        "NOT_MODELLED",
        "WITHHELD_STATEMENT",
        "UNREACHED_RECORD",
        "NOT_IN_SOURCE",
        "LOCATOR_NOT_RESOLVABLE",
    ]
    assert set(protocol["evidence_surface"]["surface_kinds"]) == {
        "SELECTED_READING_TEXT_LAYER",
        "STRUCTURED_ROWS",
    }
    assert "required_keys" in protocol["stage_identities"]


# --------------------------------------------------------------------------
# The v3.2 protocol file
# --------------------------------------------------------------------------


def test_the_v32_protocol_validates() -> None:
    protocol = review.validate_protocol(PROTOCOL_V32.read_bytes())

    assert protocol["schema"] == "malleus.paper-v4.source-grounded-review-protocol/v3.2"
    assert protocol["status"] == "FROZEN_BEFORE_THE_BASELINE_CELL"
    assert protocol["judgments"]["coverage_absent_reasons"][-1] == "NOT_CAPTURED"
    assert set(protocol["evidence_surface"]["surface_kinds"]) == {
        "SELECTED_READING_TEXT_LAYER",
        "STRUCTURED_ROWS",
        "IN_CONTEXT_ANSWER_SET",
    }
    assert protocol["judgments"]["assembly_not_applicable_on"] == [
        "IN_CONTEXT_ANSWER_SET"
    ]


def test_v32_declares_stage_identities_per_surface_kind() -> None:
    protocol = review.validate_protocol(PROTOCOL_V32.read_bytes())
    by_kind = protocol["stage_identities"]["required_keys_by_surface_kind"]

    assert set(by_kind) == set(protocol["evidence_surface"]["surface_kinds"])
    assert set(by_kind["SELECTED_READING_TEXT_LAYER"]) == review._STAGE_IDENTITY_KEYS
    assert set(by_kind["IN_CONTEXT_ANSWER_SET"]) == {
        "answer_file_sha256",
        "producer_model_id",
        "producer_task_sha256",
    }
    assert "ledger_head" not in by_kind["IN_CONTEXT_ANSWER_SET"]


def test_the_answer_surface_has_no_ledger_side_materials() -> None:
    protocol = review.validate_protocol(PROTOCOL_V32.read_bytes())
    required = protocol["review_materials"]["required"]["IN_CONTEXT_ANSWER_SET"]

    assert "answer_file" in required
    assert not set(required) & set(review._LEDGER_SIDE_MATERIALS)


def test_a_v32_protocol_binding_a_query_result_on_the_answer_surface_is_refused() -> None:
    protocol = json.loads(PROTOCOL_V32.read_bytes())
    protocol["review_materials"]["required"]["IN_CONTEXT_ANSWER_SET"].append(
        "query_result"
    )

    with pytest.raises(ReviewRefusal, match="no ledger, binding, replay or trace"):
        review.validate_protocol(_json_bytes(protocol))


def test_a_v32_protocol_that_keeps_v3s_one_stage_identity_set_is_refused() -> None:
    protocol = json.loads(PROTOCOL_V32.read_bytes())
    protocol["stage_identities"]["required_keys_by_surface_kind"][
        "IN_CONTEXT_ANSWER_SET"
    ] = sorted(review._STAGE_IDENTITY_KEYS)

    with pytest.raises(ReviewRefusal, match="stage identities for IN_CONTEXT_ANSWER_SET"):
        review.validate_protocol(_json_bytes(protocol))


def test_a_v3_protocol_carrying_the_sixth_code_is_refused() -> None:
    protocol = json.loads(PROTOCOL_V3.read_bytes())
    protocol["judgments"]["coverage_absent_reasons"].append("NOT_CAPTURED")

    with pytest.raises(ReviewRefusal, match="coverage absent reasons differ"):
        review.validate_protocol(_json_bytes(protocol))


# --------------------------------------------------------------------------
# An answer-set cell, written here so the guard needs no open cell
# --------------------------------------------------------------------------

ANSWER_SOURCE_DIGEST = "sha256:" + "1" * 64
ANSWER_READING = {
    "schema": "malleus.paper-v4.selected-reading/v1",
    "source_sha256": ANSWER_SOURCE_DIGEST,
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
ANSWER_READING_BYTES = _json_bytes(ANSWER_READING)
ANSWER_QUESTIONS = {
    "schema": "malleus.paper-v4.competency-questions/v3",
    "status": "FROZEN_BEFORE_PRODUCER",
    "visibility": "VISIBLE_TO_THE_BASELINE_PRODUCER_BY_DESIGN",
    "scope": {
        "answer_surface": "IN_CONTEXT_ANSWER_SET",
        "source_support": "SELECTED_READING_TEXT_LAYER",
        "free_form_synthesis": "EXCLUDED",
    },
    "questions": [
        {
            "id": "CQ-A1",
            "question": "Which campaign deployed the instruments?",
            "required_semantics": ["campaign", "instrument"],
        },
        {
            "id": "CQ-A2",
            "question": "Which carrier shipped the instruments?",
            "required_semantics": ["shipping_carrier"],
            "expected_outcome": {"kind": "NOT_IN_SOURCE"},
        },
    ],
}
ANSWER_QUESTIONS_BYTES = _json_bytes(ANSWER_QUESTIONS)
PRODUCER_TASK_DIGEST = "sha256:" + "3" * 64
PRODUCER_MODEL_ID = "claude-opus-5"


def _answer_set(**overrides: object) -> dict[str, object]:
    document = {
        "schema": "malleus.paper-v4.in-context-answer-set/v1",
        "condition": "IN_CONTEXT_BASELINE",
        "producer_model_id": PRODUCER_MODEL_ID,
        "inputs": {
            "selected_reading_sha256": _digest_bytes(ANSWER_READING_BYTES),
            "competency_questions_sha256": _digest_bytes(ANSWER_QUESTIONS_BYTES),
            "producer_task_sha256": PRODUCER_TASK_DIGEST,
        },
        "answers": [
            {
                "question_id": "CQ-A1",
                "answer": "A campaign put the instruments in place.",
                "no_answer_in_source": False,
                "claims": [
                    {
                        "claim_id": "CQ-A1:c1",
                        "statement": "A campaign placed the instruments.",
                        "blocks": ["page:1:block:001"],
                    },
                    {
                        "claim_id": "CQ-A1:c2",
                        "statement": "Instruments were put in place.",
                        "blocks": ["page:1:block:001"],
                    },
                ],
            },
            {
                "question_id": "CQ-A2",
                "answer": "The reading names no carrier.",
                "no_answer_in_source": True,
                "claims": [],
            },
        ],
    }
    document.update(overrides)
    return document


def _answer_manifest(document: dict[str, object], **overrides: object) -> dict[str, object]:
    answers = _json_bytes(document)
    counts = {
        str(item["question_id"]): len(item["claims"]) for item in document["answers"]
    }
    manifest = {
        "schema": "malleus.paper-v4.source-grounded-review-inputs/v3.2",
        "status": "FROZEN_FOR_REVIEW",
        "run_id": "fixture-answers",
        "review_protocol_sha256": _digest(PROTOCOL_V32),
        "evidence_surface": {
            "kind": "IN_CONTEXT_ANSWER_SET",
            "locator_kind": "SELECTED_READING_BLOCK_ID",
        },
        "fixed_identities": {
            "competency_questions_sha256": _digest_bytes(ANSWER_QUESTIONS_BYTES),
            "selected_reading_sha256": _digest_bytes(ANSWER_READING_BYTES),
            "source_sha256": ANSWER_SOURCE_DIGEST,
        },
        "stage_identities": {
            "answer_file_sha256": _digest_bytes(answers),
            "producer_model_id": PRODUCER_MODEL_ID,
            "producer_task_sha256": PRODUCER_TASK_DIGEST,
        },
        "materials": [
            {
                "name": "selected_reading",
                "path": "tests/fixtures/selected-reading.json",
                "sha256": _digest_bytes(ANSWER_READING_BYTES),
                "visibility": "PRIVATE",
            },
            {
                "name": "competency_questions",
                "path": "tests/fixtures/competency-questions.json",
                "sha256": _digest_bytes(ANSWER_QUESTIONS_BYTES),
                "visibility": "PUBLIC",
            },
            {
                "name": "answer_file",
                "path": "tests/fixtures/answers.json",
                "sha256": _digest_bytes(answers),
                "visibility": "PUBLIC",
            },
        ],
        "question_ids": ["CQ-A1", "CQ-A2"],
        "rows_per_question": counts,
        "witnesses_traced": sum(counts.values()),
        "authorship": {
            "preliminary_evaluator_kind": "CLAUDE_PRELIMINARY",
            "ratifier_evaluator_kind": "HUMAN_AUTHOR",
            "ratifier_actor_id": "actor:luis",
        },
    }
    manifest.update(overrides)
    return manifest


def _answer_record() -> dict[str, object]:
    return {
        "schema": "malleus.paper-v4.source-grounded-review/v3.2",
        "status": "PRELIMINARY_COMPLETE",
        "inputs": {
            "review_protocol_sha256": _digest(PROTOCOL_V32),
            "review_input_manifest_sha256": "",
        },
        "preliminary": {
            "evaluator_kind": "CLAUDE_PRELIMINARY",
            "actor_id": "actor:claude-preliminary-fixture",
            "completed_at": "2026-09-12T12:00:00Z",
        },
        "witnesses": [
            {
                "witness_key": "CQ-A1:c1",
                "source_support": "SUPPORTED",
                "source_locators": ["page:1:block:001"],
                "rationale": "the block names the campaign and the instruments",
            },
            {
                "witness_key": "CQ-A1:c2",
                "source_support": "SUPPORTED",
                "source_locators": ["page:1:block:001"],
                "rationale": "the same block carries the placement",
            },
        ],
        "questions": [
            {
                "question_id": "CQ-A1",
                "question_responsiveness": "COVERED",
                "responsiveness_rationale": "both semantics reach a supported claim",
                "assembly": "NOT_APPLICABLE",
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
                    {"row_index": 0, "witness_key": "CQ-A1:c1"},
                    {"row_index": 1, "witness_key": "CQ-A1:c2"},
                ],
            },
            {
                "question_id": "CQ-A2",
                "question_responsiveness": "NONE",
                "responsiveness_rationale": "the answer declares the reading silent",
                "assembly": "NOT_APPLICABLE",
                "coverage": [
                    {
                        "semantic": "shipping_carrier",
                        "row_index": None,
                        "absent_reason": "NOT_IN_SOURCE",
                        "note": "the reading names no carrier",
                    }
                ],
                "source_locators": ["page:1:block:002"],
                "rows": [],
            },
        ],
        "ratification": {
            "evaluator_kind": "HUMAN_AUTHOR",
            "actor_id": "actor:luis",
            "disposition": "PENDING",
            "completed_at": "",
            "notes": "",
        },
    }


def _validate_answers(
    record: dict[str, object] | None = None,
    document: dict[str, object] | None = None,
    manifest: dict[str, object] | None = None,
    **kwargs: object,
) -> dict[str, object]:
    document = _answer_set() if document is None else document
    answers = _json_bytes(document)
    manifest = _answer_manifest(document) if manifest is None else manifest
    manifest_bytes = _json_bytes(manifest)
    record = _answer_record() if record is None else record
    record["inputs"]["review_input_manifest_sha256"] = _digest_bytes(manifest_bytes)
    return review.validate_review(
        _wrap(record),
        PROTOCOL_V32.read_bytes(),
        review_input_manifest_source=manifest_bytes,
        answer_set_source=answers,
        selected_reading_source=ANSWER_READING_BYTES,
        competency_questions_source=ANSWER_QUESTIONS_BYTES,
        **kwargs,
    )


def test_an_answer_set_record_is_accepted_on_the_third_surface() -> None:
    record = _validate_answers()

    assert record["schema"] == "malleus.paper-v4.source-grounded-review/v3.2"
    assert [item["witness_key"] for item in record["witnesses"]] == [
        "CQ-A1:c1",
        "CQ-A1:c2",
    ]
    assert [item["assembly"] for item in record["questions"]] == [
        "NOT_APPLICABLE",
        "NOT_APPLICABLE",
    ]


def test_control_outcomes_are_reported_on_the_answer_surface() -> None:
    findings: list[dict[str, object]] = []
    _validate_answers(findings=findings)

    assert findings == [
        {
            "question_id": "CQ-A2",
            "kind": "NOT_IN_SOURCE",
            "expected": "NONE",
            "observed": "NONE",
            "matched": True,
        }
    ]


def test_an_answer_set_manifest_with_a_ledger_head_is_refused() -> None:
    document = _answer_set()
    manifest = _answer_manifest(document)
    manifest["stage_identities"]["ledger_head"] = "sha256:" + "b" * 64

    with pytest.raises(ReviewRefusal, match="stage_identities must contain exactly"):
        review.validate_review_input_manifest(
            _json_bytes(manifest), PROTOCOL_V32.read_bytes()
        )


def test_an_answer_set_manifest_binding_a_ledger_side_material_is_refused() -> None:
    document = _answer_set()
    manifest = _answer_manifest(document)
    manifest["materials"].append(
        {
            "name": "query_result",
            "path": "tests/fixtures/query-result.json",
            "sha256": "sha256:" + "c" * 64,
            "visibility": "PUBLIC",
        }
    )

    with pytest.raises(ReviewRefusal, match="no ledger, binding, replay or trace"):
        review.validate_review_input_manifest(
            _json_bytes(manifest), PROTOCOL_V32.read_bytes()
        )


def test_an_answer_whose_claim_cites_a_block_outside_the_reading_is_refused() -> None:
    document = _answer_set()
    document["answers"][0]["claims"][0]["blocks"] = ["page:9:block:999"]

    with pytest.raises(ReviewRefusal, match="cites blocks outside the selected reading"):
        _validate_answers(document=document)


def test_a_witness_that_omits_the_block_its_claim_cites_is_refused() -> None:
    record = _answer_record()
    record["witnesses"][0]["source_locators"] = ["page:1:block:002"]

    with pytest.raises(ReviewRefusal, match="without citing the blocks the claim"):
        _validate_answers(record=record)


def test_an_answer_set_record_cannot_carry_a_graph_assembly_descriptor() -> None:
    record = _answer_record()
    record["questions"][0]["assembly"] = "LINKED_ROWS"

    with pytest.raises(ReviewRefusal, match="must be one of \\['NOT_APPLICABLE'\\]"):
        _validate_answers(record=record)


def test_a_question_declaring_no_answer_in_source_cannot_cite_claims() -> None:
    document = _answer_set()
    document["answers"][1]["claims"] = [
        {
            "claim_id": "CQ-A2:c1",
            "statement": "A carrier is named.",
            "blocks": ["page:1:block:002"],
        }
    ]

    with pytest.raises(ReviewRefusal, match="declares NO_ANSWER_IN_SOURCE"):
        _validate_answers(document=document)


def test_an_answer_set_is_refused_without_its_answer_file() -> None:
    document = _answer_set()
    manifest_bytes = _json_bytes(_answer_manifest(document))
    record = _answer_record()
    record["inputs"]["review_input_manifest_sha256"] = _digest_bytes(manifest_bytes)

    with pytest.raises(ReviewRefusal, match="instead of a query result"):
        review.validate_review(
            _wrap(record),
            PROTOCOL_V32.read_bytes(),
            review_input_manifest_source=manifest_bytes,
            selected_reading_source=ANSWER_READING_BYTES,
            competency_questions_source=ANSWER_QUESTIONS_BYTES,
        )


def test_not_captured_is_accepted_under_v32_and_refused_under_v3() -> None:
    document = _answer_set()
    record = _answer_record()
    record["questions"][0]["coverage"][1] = {
        "semantic": "instrument",
        "row_index": None,
        "absent_reason": "NOT_CAPTURED",
        "note": "the answer states the campaign and never the instruments",
    }
    record["questions"][0]["question_responsiveness"] = "PARTIAL"
    record["questions"][0]["rows"] = [record["questions"][0]["rows"][0]]
    record["witnesses"] = [record["witnesses"][0]]
    document["answers"][0]["claims"] = [document["answers"][0]["claims"][0]]

    accepted = _validate_answers(record=copy.deepcopy(record), document=document)
    assert accepted["questions"][0]["question_responsiveness"] == "PARTIAL"

    assert "NOT_CAPTURED" not in review.COVERAGE_ABSENT_REASONS
    assert review.COVERAGE_ABSENT_REASONS_BY_VERSION["v3.2"][-1] == "NOT_CAPTURED"


def test_a_v3_record_does_not_validate_against_v32_and_says_why() -> None:
    """A record of the older schema meets the newer protocol and is named."""

    directory, query_result, questions = V3_CELLS["run-23"]
    with pytest.raises(ReviewRefusal) as refusal:
        review.validate_review(
            (ROOT / directory / "review-record.preliminary.md").read_bytes(),
            PROTOCOL_V32.read_bytes(),
            review_input_manifest_source=(
                ROOT / directory / "review-input-manifest.json"
            ).read_bytes(),
            query_result_source=(ROOT / query_result).read_bytes(),
            selected_reading_source=READING.read_bytes(),
            competency_questions_source=(ROOT / questions).read_bytes(),
        )

    assert "review input manifest schema is not the v3.2 schema" in str(refusal.value)


def test_a_v3_shaped_record_under_a_v32_manifest_is_refused_and_says_why() -> None:
    """The manifest refuses first above; this is the record's own refusal."""

    document = _answer_set()
    manifest_bytes = _json_bytes(_answer_manifest(document))
    record = _answer_record()
    record["schema"] = "malleus.paper-v4.source-grounded-review/v3"
    record["inputs"]["review_input_manifest_sha256"] = _digest_bytes(manifest_bytes)

    with pytest.raises(ReviewRefusal) as refusal:
        review.validate_review(
            _wrap(record),
            PROTOCOL_V32.read_bytes(),
            review_input_manifest_source=manifest_bytes,
            answer_set_source=_json_bytes(document),
            selected_reading_source=ANSWER_READING_BYTES,
            competency_questions_source=ANSWER_QUESTIONS_BYTES,
        )

    assert str(refusal.value) == "review schema is not the v3.2 schema the protocol needs"


def test_a_v32_record_is_refused_under_v3_and_says_why() -> None:
    document = _answer_set()
    manifest_bytes = _json_bytes(_answer_manifest(document))
    record = _answer_record()
    record["inputs"]["review_input_manifest_sha256"] = _digest_bytes(manifest_bytes)

    with pytest.raises(ReviewRefusal, match="v3 schema the protocol needs"):
        review.validate_review(
            _wrap(record),
            PROTOCOL_V3.read_bytes(),
            review_input_manifest_source=manifest_bytes,
            answer_set_source=_json_bytes(document),
            selected_reading_source=ANSWER_READING_BYTES,
            competency_questions_source=ANSWER_QUESTIONS_BYTES,
        )


def test_an_answer_surface_under_v3_is_refused() -> None:
    """The third kind does not exist for a cell that declares the v3 protocol."""

    document = _answer_set()
    manifest = _answer_manifest(document)
    manifest["schema"] = "malleus.paper-v4.source-grounded-review-inputs/v3"
    manifest["review_protocol_sha256"] = _digest(PROTOCOL_V3)

    with pytest.raises(ReviewRefusal, match="evidence surface kind nobody froze"):
        review.validate_review_input_manifest(
            _json_bytes(manifest), PROTOCOL_V3.read_bytes()
        )


def test_a_blank_answer_set_record_validates_as_blank() -> None:
    document = _answer_set()
    manifest_bytes = _json_bytes(_answer_manifest(document))
    blank = _answer_record()
    blank["status"] = "BLANK"
    blank["inputs"]["review_input_manifest_sha256"] = ""
    blank["preliminary"] = {
        "evaluator_kind": "CLAUDE_PRELIMINARY",
        "actor_id": "",
        "completed_at": "",
    }
    blank["witnesses"] = []
    for question in blank["questions"]:
        question["question_responsiveness"] = "PENDING"
        question["responsiveness_rationale"] = ""
        question["assembly"] = "PENDING"
        question["coverage"] = []
        question["source_locators"] = []
        question["rows"] = []

    validated = review.validate_blank_review(
        _wrap(blank), PROTOCOL_V32.read_bytes(), manifest_bytes
    )

    assert validated["status"] == "BLANK"


# --------------------------------------------------------------------------
# The checklist: how each rule of the rulebook is verified
# --------------------------------------------------------------------------


def _checklist() -> dict[str, object]:
    return review.validate_protocol(PROTOCOL_V32.read_bytes())["checklist"]


def _record_keys() -> set[str]:
    record = json.loads(PROTOCOL_V32.read_bytes())["record"]
    keys: set[str] = set()
    for name in (
        "root_keys",
        "witness_keys",
        "question_keys",
        "row_keys",
        "coverage_keys",
    ):
        keys |= set(record[name])
    return keys


def test_every_checklist_entry_names_a_verifier_that_exists() -> None:
    """A check that names a function nobody wrote is a rule nobody applies."""

    modules = {
        "review": review,
        "validate_answers": _baseline_module("validate_answers"),
    }
    record_keys = _record_keys()
    checked = {"VALIDATOR": 0, "REVIEWER": 0}

    for check in _checklist()["checks"]:
        where = check["id"]
        if check["verified_by"] == "VALIDATOR":
            module_name, _, function = check["validator_function"].partition(".")
            assert module_name in modules, where
            resolved = getattr(modules[module_name], function, None)
            assert callable(resolved), f"{where} names {check['validator_function']}"
        else:
            segments = [
                segment.replace("[]", "")
                for segment in check["reviewer_judgement"].split(".")
            ]
            assert segments[0] == "review", where
            for segment in segments[1:]:
                assert segment in record_keys, f"{where} names {segment!r}"
        checked[check["verified_by"]] += 1

    assert checked["VALIDATOR"] and checked["REVIEWER"]


def test_every_checklist_outcome_lands_where_the_protocol_declares() -> None:
    section = _checklist()
    fields = section["outcome_fields"]
    record_keys = _record_keys()

    for check in section["checks"]:
        assert check["records_outcome_in"] in fields, check["id"]
    for path, where in fields.items():
        if where != "THE_RECORD":
            continue
        first = path.split(".")[1].replace("[]", "")
        assert first in record_keys, path


def test_the_checklist_covers_the_checks_the_author_named() -> None:
    names = " ".join(
        f"{check['name']} {check['passes_when']}" for check in _checklist()["checks"]
    )

    for wanted in (
        "sha256 equals the digest",
        "locator",
        "once and no other",
        "absent_reason",
        "derived",
        "expected_outcome",
        "sixty characters",
        "required_keys_by_surface_kind",
        "claim_id",
    ):
        assert wanted in names, wanted


def test_every_surface_kind_the_protocol_declares_has_checks() -> None:
    section = _checklist()
    kinds = set(json.loads(PROTOCOL_V32.read_bytes())["evidence_surface"]["surface_kinds"])

    for kind in kinds:
        assert [check for check in section["checks"] if kind in check["applies_to"]]


def test_a_checklist_entry_naming_no_verifier_is_refused() -> None:
    protocol = json.loads(PROTOCOL_V32.read_bytes())
    del protocol["checklist"]["checks"][0]["validator_function"]

    with pytest.raises(ReviewRefusal, match="must contain exactly"):
        review.validate_protocol(_json_bytes(protocol))


def test_a_checklist_outcome_the_protocol_does_not_declare_is_refused() -> None:
    protocol = json.loads(PROTOCOL_V32.read_bytes())
    protocol["checklist"]["checks"][0]["records_outcome_in"] = "review.somewhere_else"

    with pytest.raises(ReviewRefusal, match="outcome_fields does not declare"):
        review.validate_protocol(_json_bytes(protocol))


def test_v3_carries_no_checklist_and_is_not_edited() -> None:
    assert "checklist" not in json.loads(PROTOCOL_V3.read_bytes())
    assert review.validate_protocol(PROTOCOL_V3.read_bytes())["status"] == (
        "FROZEN_BEFORE_NEXT_CELL"
    )


def test_the_active_gate_collects_this_guard() -> None:
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())

    assert "paper-v4/evaluation-v4" in manifest["paths"]
