from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUESTIONS = ROOT / "paper-v4/experiment/competency-questions.json"


def test_competency_questions_are_frozen_model_visible_and_oracle_free() -> None:
    document = json.loads(QUESTIONS.read_bytes())
    questions = document["questions"]

    assert document["schema"] == "malleus.paper-v4.competency-questions/v1"
    assert document["status"] == "FROZEN_BEFORE_MODEL_ACQUISITION"
    assert document["visibility"] == "MODEL_VISIBLE"
    assert document["scope"] == {
        "answer_surface": "REPLAY_DERIVED_NATIVE_GRAPH_QUERY",
        "source_support": "PROSE_ONLY",
        "figures": "EXCLUDED",
        "tables": "EXCLUDED",
        "free_form_synthesis": "EXCLUDED",
    }
    assert [item["id"] for item in questions] == [
        "CQ-01",
        "CQ-02",
        "CQ-03",
        "CQ-04",
    ]
    assert all(item["question"].strip() for item in questions)
    assert all(item["required_semantics"] for item in questions)
    assert not any(
        key in item
        for item in questions
        for key in ("answer", "expected_answer", "support", "source_locator")
    )
