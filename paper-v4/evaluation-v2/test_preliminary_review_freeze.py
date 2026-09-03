"""Guards for the exact Codex-authored v2 preliminary review."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper.human_review import (
    HumanReviewRefusal,
    validate_human_review,
)


ROOT = Path(__file__).resolve().parents[2]
EVALUATION = ROOT / "paper-v4/evaluation-v2"
EXPERIMENT = ROOT / "paper-v4/experiment-v2"
RECORD = EVALUATION / "review-record.preliminary.md"
EXPECTED_RECORD_DIGEST = (
    "sha256:4ccab912c693d0f751276d45ad58d9536c4ce75552d337b39b3fab6ddc97e574"
)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _validate(*, require_human_ratification: bool = False) -> dict[str, object]:
    return validate_human_review(
        RECORD.read_bytes(),
        (EVALUATION / "review-protocol.json").read_bytes(),
        review_input_manifest_source=(
            EVALUATION / "review-input-manifest.json"
        ).read_bytes(),
        competency_questions_source=(
            ROOT / "paper-v4/experiment/competency-questions.json"
        ).read_bytes(),
        query_binding_source=(EXPERIMENT / "native-query-binding.json").read_bytes(),
        query_result_source=(EXPERIMENT / "results/query-result.json").read_bytes(),
        replay_receipt_source=(
            EXPERIMENT / "results/replay-receipt.json"
        ).read_bytes(),
        selected_reading_source=(
            ROOT / "private/paper-v4-text-layer/selected-reading.json"
        ).read_bytes(),
        selected_ontology_source=(
            EXPERIMENT / "ontology-run/ontology-02.yaml"
        ).read_bytes(),
        require_human_ratification=require_human_ratification,
    )


def test_preliminary_review_is_exact_and_closes_all_rows_and_locators() -> None:
    assert _digest(RECORD.read_bytes()) == EXPECTED_RECORD_DIGEST
    review = _validate()

    assert review["status"] == "PRELIMINARY_COMPLETE"
    assert [
        (question["source_support"], question["question_responsiveness"])
        for question in review["questions"]
    ] == [
        ("NOT_EVALUABLE", "NOT_RESPONSIVE"),
        ("SUPPORTED", "PARTIAL"),
        ("SUPPORTED", "RESPONSIVE"),
        ("NOT_EVALUABLE", "NOT_RESPONSIVE"),
    ]


def test_preliminary_review_cannot_pass_as_human_evidence() -> None:
    with pytest.raises(HumanReviewRefusal, match="human ratification is required"):
        _validate(require_human_ratification=True)
