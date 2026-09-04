from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMITMENTS = ROOT / "paper-v4/experiment/evaluation-commitments.json"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_evaluation_inputs_are_committed_and_separated_from_producer() -> None:
    document = json.loads(COMMITMENTS.read_bytes())
    questions = document["question_set"]
    oracle = document["answer_oracle"]
    rubric = document["ontology_adequacy_rubric"]

    assert document["schema"] == "malleus.paper-v4.evaluation-commitments/v1"
    assert document["status"] == "FROZEN_BEFORE_MODEL_ACQUISITION"
    assert _digest(ROOT / questions["path"]) == questions["sha256"]
    assert _digest(ROOT / oracle["sealed_path"]) == oracle["sha256"]
    assert _digest(ROOT / rubric["sealed_path"]) == rubric["sha256"]
    assert questions["visibility"] == "MODEL_VISIBLE"
    assert oracle["visibility"] == "SEALED_FROM_PROPOSAL_PRODUCER"
    assert rubric["visibility"] == "SEALED_FROM_PROPOSAL_PRODUCER"
    assert rubric["review_feedback"] == "FORBIDDEN"
    assert rubric["review_retry"] == "FORBIDDEN"
