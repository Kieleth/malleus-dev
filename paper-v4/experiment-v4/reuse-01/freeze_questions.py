"""Freeze the second competency-question set from its author's draft.

The draft is the authoring session's only output, written from the selected
reading alone. This script checks it, adds the identity block the cells read,
and writes ``paper-v4/experiment-v4/competency-questions-set-b.json``. Nothing
here authors a question, edits one, or reorders the file; the questions are
copied through byte-for-byte in the author's order.

What it refuses:

* a missing or refusing source-bound control assessment;
* an existing frozen destination (old files are never overwritten);
* a file whose schema is not the one ``review.py`` accepts;
* thirty questions that are not the five tiers of five plus five controls, in
  that order, with unique ids;
* a positive question carrying ``expected_outcome`` or a control carrying none;
* a required-semantics list outside three to five items, or a name that is not
  lowercase snake case;
* a paraphrase control whose semantics are not its named question's, in order;
* anything in the file that shares a sixty-character normalized run with a block
  of the selected reading, which is the rule that lets the file be public at all
  (``paper-v4/experiment-v4/run-25/results/withheld-artifacts.json``).

    .venv/bin/python paper-v4/experiment-v4/reuse-01/freeze_questions.py \\
        --draft private/paper-v4-reuse-01/author/questions-set-b.draft.json \\
        --assessment <assessment-for-exact-draft-and-reading.json>

The existing set B is historical and must not be re-frozen. Another set needs
its own destination and authorship metadata, not a copy of this cell's identity.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUTPUT = ROOT / "paper-v4/experiment-v4/competency-questions-set-b.json"
READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"
SET_A = ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json"

SCHEMA = "malleus.paper-v4.competency-questions/v3"
TIERS = ("T1", "T2", "T3", "T4", "T5")
PER_TIER = 5
CONTROLS = 5
SNAKE = re.compile(r"[a-z][a-z0-9_]*")
LEAK_WINDOW = 60


class QuestionSetRefusal(ValueError):
    """The draft is not a set this experiment can freeze."""


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _ladder():
    path = HERE / "leak_ladder.py"
    specification = importlib.util.spec_from_file_location("reuse_01_ladder", path)
    if specification is None or specification.loader is None:
        raise QuestionSetRefusal(f"the ladder is not readable: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def expected_ids() -> list[str]:
    positives = [
        f"CQ-B-{tier}-{index:02d}"
        for tier in TIERS
        for index in range(1, PER_TIER + 1)
    ]
    return positives + [f"CQ-B-C-{index:02d}" for index in range(1, CONTROLS + 1)]


def check(questions: list[dict[str, Any]]) -> dict[str, Any]:
    ids = [str(item["id"]) for item in questions]
    if ids != expected_ids():
        raise QuestionSetRefusal("the draft's question ids are not this set's, in order")
    by_id = {item["id"]: item for item in questions}
    positives = 0
    elements = 0
    control_kinds: dict[str, str] = {}
    for item in questions:
        subject = item["id"]
        tier = str(item["tier"])
        if tier not in (*TIERS, "C"):
            raise QuestionSetRefusal(f"{subject} carries an unknown tier {tier}")
        if not str(item["question"]).strip():
            raise QuestionSetRefusal(f"{subject} carries no question text")
        semantics = list(item["required_semantics"])
        if not 3 <= len(semantics) <= 5:
            raise QuestionSetRefusal(
                f"{subject} carries {len(semantics)} required semantics, not three to five"
            )
        for name in semantics:
            if not SNAKE.fullmatch(str(name)):
                raise QuestionSetRefusal(f"{subject} names a semantic {name!r}")
        if len(set(semantics)) != len(semantics):
            raise QuestionSetRefusal(f"{subject} names a required semantic twice")
        outcome = item.get("expected_outcome")
        if tier == "C":
            if outcome is None:
                raise QuestionSetRefusal(f"{subject} is a control and declares no outcome")
            kind = str(outcome["kind"])
            if kind not in ("NOT_IN_SOURCE", "EXCLUDED_SURFACE", "PARAPHRASE"):
                raise QuestionSetRefusal(f"{subject} declares an unknown control kind")
            control_kinds[subject] = kind
            if kind == "PARAPHRASE":
                if outcome["expected_coverage"] != "SAME_AS":
                    raise QuestionSetRefusal(f"{subject} must expect the same coverage")
                named = str(outcome["of"])
                if named not in by_id or by_id[named]["tier"] == "C":
                    raise QuestionSetRefusal(
                        f"{subject} paraphrases {named}, which is not a positive question"
                    )
                if list(by_id[named]["required_semantics"]) != semantics:
                    raise QuestionSetRefusal(
                        f"{subject} does not carry {named}'s required semantics in order"
                    )
            else:
                if outcome["expected_coverage"] != "NONE":
                    raise QuestionSetRefusal(f"{subject} must expect NONE")
                if "of" in outcome:
                    raise QuestionSetRefusal(f"{subject} names a question it does not paraphrase")
            if not str(outcome["why"]).strip():
                raise QuestionSetRefusal(f"{subject} gives no reason for its expectation")
        else:
            if outcome is not None:
                raise QuestionSetRefusal(f"{subject} is a positive question and declares an outcome")
            positives += 1
            elements += len(semantics)
    if positives != len(TIERS) * PER_TIER:
        raise QuestionSetRefusal(f"the draft carries {positives} positive questions")
    kinds = set(control_kinds.values())
    if "PARAPHRASE" not in kinds or not kinds - {"PARAPHRASE"}:
        raise QuestionSetRefusal("the controls must carry paraphrases and unanswerables")
    return {
        "positive_questions": positives,
        "required_elements_over_positives": elements,
        "required_elements_over_all": sum(
            len(item["required_semantics"]) for item in questions
        ),
        "control_kinds": control_kinds,
    }


def freeze(draft_path: Path, assessment_path: Path | None = None) -> dict[str, Any]:
    # Old question files remain historical evidence. No unscreened or
    # overwrite path is allowed for another freeze.
    if assessment_path is None:
        raise QuestionSetRefusal("a source-bound control assessment is required before freeze")
    if OUTPUT.exists():
        raise QuestionSetRefusal("the frozen question file already exists; select a new destination")
    draft_path = draft_path.resolve()
    draft_source = draft_path.read_bytes()
    path = ROOT / "paper-v4/evaluation-v4/control_screen.py"
    spec = importlib.util.spec_from_file_location("question_control_screen", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        screen = module.validate(draft_source, READING.read_bytes(), assessment_path.read_bytes())
    except ValueError as error:
        raise QuestionSetRefusal(f"control assessment refused: {error}") from error
    draft = json.loads(draft_source)
    if draft.get("schema") != SCHEMA:
        raise QuestionSetRefusal(f"the draft must declare {SCHEMA}")
    if sorted(draft) != ["questions", "schema"]:
        raise QuestionSetRefusal("the draft must carry the schema and the questions only")
    questions = list(draft["questions"])
    counts = check(questions)

    ladder = _ladder()
    reached = ladder.measure([draft_path], READING)[str(draft_path)]
    if reached >= LEAK_WINDOW:
        raise QuestionSetRefusal(
            f"the draft shares a {reached}-character run with the reading and"
            " cannot be published"
        )

    document = {
        "schema": SCHEMA,
        "status": "FROZEN",
        "set": "B",
        "set_note": (
            "An independent second question set, not a revision of"
            " competency-questions-v3.1.json. It was authored from the selected"
            " reading alone by one fresh Claude Opus 5 session that saw no"
            " ontology, no graph, no capture, no query material, no review record"
            " and no earlier question file, and it exists to put a second set to"
            " a graph that was built question-blind against the first. Its ids"
            " carry the prefix CQ-B- so that no id of either set can be mistaken"
            " for the other's."
        ),
        "visibility": "WITHHELD_FROM_PRODUCER_UNTIL_POST_REPLAY",
        "visibility_note": (
            "Withheld from every graph producer, as set A was. The in-context"
            " baseline of reuse-01-baseline is handed this file, which is the one"
            " place the question-blind rule is broken and is the condition that"
            " cell prices."
        ),
        "scope": {
            "answer_surface": "REPLAY_DERIVED_NATIVE_GRAPH_QUERY_WITH_PROVENANCE_TRACE",
            "source_support": "SELECTED_READING_TEXT_LAYER",
            "figures": "EXCLUDED",
            "tables": "EXCLUDED",
            "free_form_synthesis": "EXCLUDED",
        },
        "authored": {
            "kind": "CLAUDE_FRESH_SESSION",
            "model": "claude-opus-5",
            "harness": (
                "Claude Code Agent tool, subagent_type general-purpose, no"
                " inherited context"
            ),
            "blind_to": [
                "EVERY_ONTOLOGY",
                "EVERY_GRAPH",
                "EVERY_CAPTURE",
                "EVERY_EXISTING_QUESTION_FILE",
                "EVERY_REVIEW_RECORD",
                "THE_REPOSITORY",
            ],
            "inputs": [
                {
                    "role": "paper_text_layer",
                    "path": "private/paper-v4-text-layer/selected-reading.json",
                    "sha256": _digest(READING.read_bytes()),
                }
            ],
            "draft": {
                "path": str(draft_path.relative_to(ROOT)),
                "sha256": _digest(draft_source),
            },
            "launch_log": "private/paper-v4-reuse-01/launch-log.json",
        },
        "shape": {
            "questions": len(questions),
            "positive_questions": counts["positive_questions"],
            "tiers": {
                "T1": "direct facts",
                "T2": "relationships",
                "T3": "quantities",
                "T4": "qualifications",
                "T5": "composition",
            },
            "required_elements_over_positive_questions": counts[
                "required_elements_over_positives"
            ],
            "required_elements_over_all_questions": counts["required_elements_over_all"],
            "controls": counts["control_kinds"],
        },
        "independent_of": {
            "file": "paper-v4/experiment-v4/competency-questions-v3.1.json",
            "sha256": _digest(SET_A.read_bytes()),
            "relation": "NEITHER_A_REVISION_NOR_A_SUPERSESSION",
            "relation_note": (
                "Set A stays frozen and binds run-24, run-25 and baseline-01."
                " Neither file supersedes the other; they are two independent"
                " sets over one reading, and the author of this one never saw"
                " that one."
            ),
        },
        "publication_rule": {
            "check": "SHARED_NORMALIZED_CHARACTER_RUN_AGAINST_EVERY_READING_BLOCK",
            "measured_by": "paper-v4/experiment-v4/reuse-01/leak_ladder.py",
            "window": LEAK_WINDOW,
            "draft_reached": reached,
        },
        "questions": questions,
        "control_assessment": screen,
    }
    OUTPUT.write_bytes(
        json.dumps(document, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    )
    frozen_reached = ladder.measure([OUTPUT], READING)[str(OUTPUT)]
    if frozen_reached >= LEAK_WINDOW:
        raise QuestionSetRefusal("the frozen file shares a run with the reading")
    return {
        "path": str(OUTPUT.relative_to(ROOT)),
        "sha256": _digest(OUTPUT.read_bytes()),
        "questions": len(questions),
        "frozen_file_ladder": frozen_reached,
        **counts,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--assessment", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        print(json.dumps(freeze(arguments.draft, arguments.assessment), indent=2, sort_keys=True))
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"question-set: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
