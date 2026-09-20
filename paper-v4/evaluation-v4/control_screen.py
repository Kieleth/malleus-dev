"""Enforce source-bound, element-level control assessments, not entailment.

An assessor judges presence/absence in the whole selected reading. Code checks
closure, identities, locators and contradictions. It cannot prove absence or
that a cited block entails a natural-language requirement. Frozen reviews and
question sets are not changed by this pre-freeze check.
"""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


class ControlScreenRefusal(ValueError):
    pass


def digest(source):
    return "sha256:" + sha256(source).hexdigest()


def validate(questions_source, reading_source, assessment_source):
    try:
        return _validate(questions_source, reading_source, assessment_source)
    except (KeyError, TypeError) as error:
        raise ControlScreenRefusal(
            f"missing or malformed assessment field: {error}"
        ) from error


def _validate(questions_source, reading_source, assessment_source):
    questions = json.loads(questions_source)["questions"]
    reading = json.loads(reading_source)
    assessment = json.loads(assessment_source)
    if assessment["schema"] != "malleus.paper-v4.control-assessment/v1":
        raise ControlScreenRefusal("unknown control assessment schema")
    if assessment["questions_sha256"] != digest(questions_source):
        raise ControlScreenRefusal("questions digest mismatch")
    if assessment["reading_sha256"] != digest(reading_source):
        raise ControlScreenRefusal("reading digest mismatch")
    assessor = assessment["assessor"]
    if assessor["kind"] not in {"HUMAN", "MODEL_ASSISTED", "DERIVED_MODEL_REVIEW"}:
        raise ControlScreenRefusal("unknown assessor kind")
    if not isinstance(assessor["id"], str) or not assessor["id"].strip():
        raise ControlScreenRefusal("assessor id is required")
    by_id = {q["id"]: q for q in questions}
    if len(by_id) != len(questions):
        raise ControlScreenRefusal("duplicate question id")
    wanted = set()
    for question in questions:
        if question["tier"] != "C":
            continue
        semantics = question["required_semantics"]
        if not semantics or len(set(semantics)) != len(semantics):
            raise ControlScreenRefusal("missing or duplicate control semantics")
        outcome = question["expected_outcome"]
        if outcome["kind"] == "PARAPHRASE":
            original = by_id[outcome["of"]]
            if (
                original["tier"] == "C"
                or outcome["expected_coverage"] != "SAME_AS"
                or original["required_semantics"] != semantics
            ):
                raise ControlScreenRefusal(
                    "paraphrase semantics differ from its positive question"
                )
        elif outcome["kind"] in {"NOT_IN_SOURCE", "EXCLUDED_SURFACE"}:
            if outcome["expected_coverage"] != "NONE":
                raise ControlScreenRefusal("absence control must expect NONE")
            wanted.update((question["id"], semantic) for semantic in semantics)
        else:
            raise ControlScreenRefusal("unknown control kind")
    blocks = [block["id"] for page in reading["pages"] for block in page["blocks"]]
    if not blocks or len(set(blocks)) != len(blocks):
        raise ControlScreenRefusal("empty reading or duplicate block ids")
    seen, blocked = set(), []
    for item in assessment["elements"]:
        key = item["question_id"], item["semantic"]
        if key in seen:
            raise ControlScreenRefusal("duplicate element assessment")
        seen.add(key)
        if not isinstance(item["reason"], str) or not item["reason"].strip():
            raise ControlScreenRefusal("element reason is required")
        locators = item["blocks"]
        if type(locators) is not list or len(set(locators)) != len(locators):
            raise ControlScreenRefusal("element blocks must be a unique list")
        if set(locators) - set(blocks):
            raise ControlScreenRefusal("unknown block in assessment")
        finding = item["finding"]
        if finding == "IN_READING":
            if not locators:
                raise ControlScreenRefusal("present element needs blocks")
        elif finding == "NOT_IN_READING":
            if locators:
                raise ControlScreenRefusal("absence carries blocks")
        elif finding != "UNCERTAIN":
            raise ControlScreenRefusal("unknown element finding")
        if finding != "NOT_IN_READING":
            blocked.append(f"{key[0]}/{key[1]}: {finding}")
    if seen != wanted:
        raise ControlScreenRefusal("control element closure differs from question set")
    if blocked:
        raise ControlScreenRefusal("; ".join(blocked))
    return {
        "status": "ASSESSMENT_ACCEPTED",
        "elements_checked": len(seen),
        "questions_sha256": digest(questions_source),
        "reading_sha256": digest(reading_source),
        "assessment_sha256": digest(assessment_source),
        "semantic_truth_verified_by_code": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--reading", type=Path, required=True)
    parser.add_argument("--assessment", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = validate(
            args.questions.read_bytes(),
            args.reading.read_bytes(),
            args.assessment.read_bytes(),
        )
    except (OSError, ValueError) as error:
        print(f"control-screen: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
