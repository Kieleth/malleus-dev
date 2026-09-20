"""Validate the baseline producer's answer file against its frozen grammar.

Two jobs and nothing else. The first is the grammar of
`answer-file-schema.json`: every question of the frozen file answered once, no
unknown id, every claim carrying a claim id and at least one block the reading
declares, and a question that declares NO_ANSWER_IN_SOURCE carrying no claim.
The second is the verbatim rule the cells already apply to everything they
publish: no answer text and no claim statement may share a sixty-character
normalized run with a block of the selected reading.

The second job is why the answer file can be public at all. The selected
reading is private; a baseline that paraphrases can be published beside the
graph cells, one that quotes cannot. Sixty normalized characters is the
threshold every frozen cell clears (`paper-v4/experiment-v4/run-25/freeze.py`
`LEAK_WINDOW`, and the same constant in each cell's contract test), and the
normalization is the same one: `" ".join(text.split())`.

It judges nothing. Whether a cited block supports its claim is the reviewer's
question under `paper-v4/evaluation-v4/review-protocol-v3.2.json`, and whether
the answer is right is nobody's here: the baseline has no oracle.

    .venv/bin/python paper-v4/experiment-v4/baseline-01/validate_answers.py \\
        --answers private/paper-v4-baseline-01/producer/work/answers.json \\
        --reading private/paper-v4-text-layer/selected-reading.json
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCHEMA_FILE = HERE / "answer-file-schema.json"
QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json"

ANSWER_SET_SCHEMA = "malleus.paper-v4.in-context-answer-set/v1"
CONDITION = "IN_CONTEXT_BASELINE"


class AnswerRefusal(ValueError):
    """The answer file is not one this cell can review."""


def _refuse(detail: str) -> None:
    raise AnswerRefusal(detail)


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _plain(text: str) -> str:
    """The normalization the cells' leak ladder uses: whitespace collapsed."""

    return " ".join(text.split())


def _object(value: object, subject: str) -> dict[str, Any]:
    if type(value) is not dict:
        _refuse(f"{subject} must be an object")
    return value  # type: ignore[return-value]


def _array(value: object, subject: str) -> list[Any]:
    if type(value) is not list:
        _refuse(f"{subject} must be an array")
    return value  # type: ignore[return-value]


def _text(value: object, subject: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _refuse(f"{subject} must be nonblank text")
    return value  # type: ignore[return-value]


def _exact_keys(value: dict[str, Any], expected: Iterable[str], subject: str) -> None:
    wanted = sorted(expected)
    if sorted(value) != wanted:
        _refuse(f"{subject} must contain exactly {wanted}")


def schema() -> dict[str, Any]:
    """The frozen grammar. The validator restates none of it in code."""

    document = json.loads(SCHEMA_FILE.read_bytes())
    if document["schema"] != "malleus.paper-v4.answer-file-schema/v1":
        _refuse("the answer file schema is not the one this validator carries")
    if document["describes"] != ANSWER_SET_SCHEMA:
        _refuse("the answer file schema describes another answer-set schema")
    return document


def reading_windows(reading: dict[str, Any], width: int) -> set[str]:
    """Every normalized run of `width` characters the reading writes."""

    windows: set[str] = set()
    for page in reading["pages"]:
        for block in page["blocks"]:
            plain = _plain(block["text"])
            for start in range(0, max(1, len(plain) - width + 1)):
                piece = plain[start : start + width]
                if len(piece) == width:
                    windows.add(piece)
    return windows


def _shared_run(text: str, windows: set[str], width: int) -> str | None:
    plain = _plain(text)
    for start in range(0, max(1, len(plain) - width + 1)):
        piece = plain[start : start + width]
        if len(piece) == width and piece in windows:
            return piece
    return None


def validate_answers(
    answers_source: bytes,
    reading_source: bytes,
    questions_source: bytes,
) -> dict[str, Any]:
    """Accept an answer file the review surface can be built from."""

    grammar = schema()
    root = _object(json.loads(answers_source), "answer file")
    _exact_keys(root, grammar["root_keys"], "answer file")
    if root["schema"] != ANSWER_SET_SCHEMA:
        _refuse("answer file schema differs")
    if root["condition"] != CONDITION:
        _refuse(f"answer file condition must be {CONDITION}")
    _text(root["producer_model_id"], "answer file.producer_model_id")
    inputs = _object(root["inputs"], "answer file.inputs")
    _exact_keys(inputs, grammar["inputs_keys"], "answer file.inputs")

    reading = _object(json.loads(reading_source), "selected reading")
    if inputs["selected_reading_sha256"] != _digest(reading_source):
        _refuse("answer file does not bind the selected reading it was given")
    if inputs["competency_questions_sha256"] != _digest(questions_source):
        _refuse("answer file does not bind the competency questions it was given")

    block_ids = {
        block["id"] for page in reading["pages"] for block in page["blocks"]
    }
    questions = json.loads(questions_source)
    expected = [str(item["id"]) for item in questions["questions"]]

    width = int(grammar["verbatim_rule"]["window"])
    windows = reading_windows(reading, width)

    seen_questions: list[str] = []
    claim_ids: set[str] = set()
    claims = 0
    unanswered: list[str] = []
    for index, raw in enumerate(_array(root["answers"], "answer file.answers")):
        subject = f"answer file.answers[{index}]"
        answer = _object(raw, subject)
        _exact_keys(answer, grammar["answer_keys"], subject)
        question_id = _text(answer["question_id"], f"{subject}.question_id")
        if question_id not in expected:
            _refuse(f"{subject} answers {question_id}, which the question file does not ask")
        if question_id in seen_questions:
            _refuse(f"{subject} answers {question_id} a second time")
        seen_questions.append(question_id)

        text = _text(answer["answer"], f"{subject}.answer")
        shared = _shared_run(text, windows, width)
        if shared is not None:
            _refuse(
                f"{subject}.answer shares a {width}-character run with the reading:"
                f" {shared!r}"
            )
        declared = answer["no_answer_in_source"]
        if type(declared) is not bool:
            _refuse(f"{subject}.no_answer_in_source must be true or false")
        if declared:
            unanswered.append(question_id)

        entries = _array(answer["claims"], f"{subject}.claims")
        if declared and entries:
            _refuse(f"{subject} declares NO_ANSWER_IN_SOURCE and cites claims")
        if not declared and not entries:
            _refuse(
                f"{subject} cites no claim and declares no NO_ANSWER_IN_SOURCE;"
                " an answer is either grounded in the reading or says it is not there"
            )
        for position, raw_claim in enumerate(entries):
            claim_subject = f"{subject}.claims[{position}]"
            claim = _object(raw_claim, claim_subject)
            _exact_keys(claim, grammar["claim_keys"], claim_subject)
            claim_id = _text(claim["claim_id"], f"{claim_subject}.claim_id")
            if claim_id in claim_ids:
                _refuse(f"{claim_subject} repeats claim id {claim_id}")
            claim_ids.add(claim_id)
            statement = _text(claim["statement"], f"{claim_subject}.statement")
            shared = _shared_run(statement, windows, width)
            if shared is not None:
                _refuse(
                    f"{claim_subject}.statement shares a {width}-character run with"
                    f" the reading: {shared!r}"
                )
            blocks = _array(claim["blocks"], f"{claim_subject}.blocks")
            if not blocks:
                _refuse(f"{claim_subject} cites no reading block")
            if any(not isinstance(item, str) or not item.strip() for item in blocks):
                _refuse(f"{claim_subject}.blocks must contain only nonblank text")
            if len(blocks) != len(set(blocks)):
                _refuse(f"{claim_subject}.blocks names a block twice")
            unknown = sorted(set(blocks) - block_ids)
            if unknown:
                _refuse(
                    f"{claim_subject} cites blocks the selected reading does not"
                    f" declare {unknown}"
                )
            claims += 1

    missing = [item for item in expected if item not in seen_questions]
    if missing:
        _refuse(f"the answer file leaves questions unanswered {missing}")
    if seen_questions != expected:
        _refuse("the answer file answers the questions out of the file's order")

    return {
        "schema": "malleus.paper-v4.answer-file-validation/v1",
        "status": "ACCEPTED",
        "answer_file_sha256": _digest(answers_source),
        "producer_model_id": root["producer_model_id"],
        "questions": len(expected),
        "claims": claims,
        "claims_per_question": {
            item["question_id"]: len(item["claims"]) for item in root["answers"]
        },
        "no_answer_in_source": unanswered,
        "verbatim_window": width,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--answers", type=Path, required=True)
    parser.add_argument("--reading", type=Path, required=True)
    parser.add_argument("--questions", type=Path, default=QUESTIONS)
    arguments = parser.parse_args(argv)
    try:
        report = validate_answers(
            arguments.answers.read_bytes(),
            arguments.reading.read_bytes(),
            arguments.questions.read_bytes(),
        )
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"answer-file: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
