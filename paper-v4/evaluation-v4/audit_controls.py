"""Read-only retrospective control screen from retained model judgements.

This is a derived check, not an independent source review. A returned supported
witness establishes a recorded presence judgement; a recorded NOT_IN_SOURCE
establishes an absence judgement. Other omissions stay UNCERTAIN. Original
questions, reviews, scores and source bytes are never rewritten.
"""

import importlib.util
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location(
    "audit_control_screen", HERE / "control_screen.py"
)
screen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(screen)
SETS = {
    "set-a-v3": ("competency-questions-v3.json", "run-23"),
    "set-a-v3.1": ("competency-questions-v3.1.json", "run-26"),
    "set-b": ("competency-questions-set-b.json", "reuse-01"),
}


def audit():
    reading = (ROOT / "private/paper-v4-text-layer/selected-reading.json").read_bytes()
    results = {}
    for name, (question_file, cell) in SETS.items():
        questions = (ROOT / "paper-v4/experiment-v4" / question_file).read_bytes()
        review_path = HERE / cell / "review-record.preliminary.md"
        review_bytes = review_path.read_bytes()
        review = json.loads(
            re.findall(r"```json\s*(.*?)\s*```", review_bytes.decode(), re.S)[-1]
        )
        manifest = json.loads((HERE / cell / "review-input-manifest.json").read_bytes())
        if manifest["fixed_identities"]["competency_questions_sha256"] != screen.digest(
            questions
        ):
            raise ValueError(f"{cell}: questions differ from reviewed bytes")
        if manifest["fixed_identities"]["selected_reading_sha256"] != screen.digest(
            reading
        ):
            raise ValueError(f"{cell}: reading differs from reviewed bytes")
        by_question = {q["question_id"]: q for q in review["questions"]}
        witnesses = {w["witness_key"]: w for w in review["witnesses"]}
        entries = []
        for question in json.loads(questions)["questions"]:
            if (
                question["tier"] != "C"
                or question["expected_outcome"]["kind"] == "PARAPHRASE"
            ):
                continue
            judged = by_question[question["id"]]
            rows = {row["row_index"]: row["witness_key"] for row in judged["rows"]}
            for element in judged["coverage"]:
                blocks = []
                if element["row_index"] is not None:
                    witness = witnesses[rows[element["row_index"]]]
                    finding = (
                        "IN_READING"
                        if witness["source_support"] == "SUPPORTED"
                        else "UNCERTAIN"
                    )
                    blocks = witness["source_locators"]
                else:
                    finding = (
                        "NOT_IN_READING"
                        if element["absent_reason"] == "NOT_IN_SOURCE"
                        else "UNCERTAIN"
                    )
                entries.append(
                    {
                        "question_id": question["id"],
                        "semantic": element["semantic"],
                        "finding": finding,
                        "blocks": blocks,
                        "reason": f"Retained {cell} review: {question['id']}/{element['semantic']}.",
                    }
                )
        assessment = {
            "schema": "malleus.paper-v4.control-assessment/v1",
            "questions_sha256": screen.digest(questions),
            "reading_sha256": screen.digest(reading),
            "assessor": {
                "kind": "DERIVED_MODEL_REVIEW",
                "id": str(review_path.relative_to(ROOT)),
            },
            "elements": entries,
        }
        source = json.dumps(assessment, sort_keys=True).encode()
        try:
            verdict = screen.validate(questions, reading, source)
        except screen.ControlScreenRefusal as error:
            verdict = {"status": "REFUSED", "reason": str(error)}
        results[name] = {
            **verdict,
            "new_semantic_review": False,
            "review_sha256": screen.digest(review_bytes),
            "assessment": assessment,
        }
    return results


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
