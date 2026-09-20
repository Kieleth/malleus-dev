"""A clean control needs an assessment of each element, not a question label."""

import copy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "control_screen", HERE / "control_screen.py"
)
screen = importlib.util.module_from_spec(SPEC)


def encoded(value):
    return json.dumps(value, sort_keys=True).encode()


def digest(value):
    return "sha256:" + sha256(value).hexdigest()


READING = encoded(
    {"pages": [{"blocks": [{"id": "b1", "text": "Three sensors were used."}]}]}
)
QUESTIONS = encoded(
    {
        "questions": [
            {"id": "P", "tier": "T1", "required_semantics": ["count"]},
            {
                "id": "C",
                "tier": "C",
                "required_semantics": ["count", "sample_rate"],
                "expected_outcome": {
                    "kind": "NOT_IN_SOURCE",
                    "expected_coverage": "NONE",
                },
            },
            {
                "id": "CP",
                "tier": "C",
                "required_semantics": ["count"],
                "expected_outcome": {
                    "kind": "PARAPHRASE",
                    "expected_coverage": "SAME_AS",
                    "of": "P",
                },
            },
        ]
    }
)


@pytest.fixture(autouse=True)
def implementation():
    SPEC.loader.exec_module(screen)


def assessment():
    return {
        "schema": "malleus.paper-v4.control-assessment/v1",
        "questions_sha256": digest(QUESTIONS),
        "reading_sha256": digest(READING),
        "assessor": {"kind": "MODEL_ASSISTED", "id": "test-reviewer"},
        "elements": [
            {
                "question_id": "C",
                "semantic": "count",
                "finding": "IN_READING",
                "blocks": ["b1"],
                "reason": "The count is stated for these sensors.",
            },
            {
                "question_id": "C",
                "semantic": "sample_rate",
                "finding": "NOT_IN_READING",
                "blocks": [],
                "reason": "No sampling frequency is given in the selected reading.",
            },
        ],
    }


def test_partial_answer_refuses_a_wholly_unanswerable_control():
    with pytest.raises(screen.ControlScreenRefusal, match="C/count: IN_READING"):
        screen.validate(QUESTIONS, READING, encoded(assessment()))


def test_clean_assessment_passes_but_does_not_claim_machine_entailment():
    value = assessment()
    value["elements"][0].update(
        finding="NOT_IN_READING", blocks=[], reason="Assessor reports absence."
    )
    result = screen.validate(QUESTIONS, READING, encoded(value))
    assert result["status"] == "ASSESSMENT_ACCEPTED"
    assert result["semantic_truth_verified_by_code"] is False
    assert result["elements_checked"] == 2
    assert result["assessment_sha256"] == digest(encoded(value))


@pytest.mark.parametrize(
    "change,match",
    [
        (lambda a: a.pop("assessor"), "assessor"),
        (lambda a: a.update(questions_sha256="sha256:" + "0" * 64), "questions digest"),
        (lambda a: a.update(reading_sha256="sha256:" + "0" * 64), "reading digest"),
        (lambda a: a["elements"].pop(), "element closure"),
        (
            lambda a: a["elements"].append(copy.deepcopy(a["elements"][0])),
            "duplicate element",
        ),
        (lambda a: a["elements"][0].update(semantic="invented"), "element closure"),
        (lambda a: a["elements"][0].update(finding="UNCERTAIN"), "UNCERTAIN"),
        (
            lambda a: a["elements"][0].update(finding="NOT_IN_READING"),
            "absence carries blocks",
        ),
        (lambda a: a["elements"][0].update(blocks=["unknown"]), "unknown block"),
        (lambda a: a["elements"][0].update(blocks=[]), "present element needs blocks"),
        (lambda a: a["elements"][0].update(reason=""), "reason"),
    ],
)
def test_missing_uncertain_or_contradictory_assessments_fail_closed(change, match):
    value = assessment()
    change(value)
    with pytest.raises(screen.ControlScreenRefusal, match=match):
        screen.validate(QUESTIONS, READING, encoded(value))


def test_paraphrases_are_not_treated_as_absence_controls():
    questions = json.loads(QUESTIONS)
    questions["questions"][2]["required_semantics"] = ["wrong"]
    source = encoded(questions)
    value = assessment()
    value["questions_sha256"] = digest(source)
    with pytest.raises(screen.ControlScreenRefusal, match="paraphrase semantics"):
        screen.validate(source, READING, encoded(value))


def test_existing_question_freezer_requires_screen_before_any_write(
    tmp_path, monkeypatch
):
    path = HERE.parent / "experiment-v4/reuse-01/freeze_questions.py"
    spec = importlib.util.spec_from_file_location("screened_freezer", path)
    freezer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(freezer)
    output = tmp_path / "frozen.json"
    monkeypatch.setattr(freezer, "OUTPUT", output)
    with pytest.raises(freezer.QuestionSetRefusal, match="control assessment"):
        freezer.freeze(tmp_path / "draft.json")
    assert not output.exists()


def test_retrospective_screen_exposes_both_known_defects_without_new_judgements():
    spec = importlib.util.spec_from_file_location(
        "control_audit", HERE / "audit_controls.py"
    )
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    result = audit.audit()
    assert result["set-a-v3"]["status"] == "REFUSED"
    assert "CQ-C-03/compilation_source" in result["set-a-v3"]["reason"]
    assert result["set-a-v3.1"]["status"] == "ASSESSMENT_ACCEPTED"
    assert result["set-b"]["status"] == "REFUSED"
    for field in ("instrument_count", "magnitude_scale", "site_name"):
        assert field in result["set-b"]["reason"]
    assert all(not item["new_semantic_review"] for item in result.values())


def test_freezer_rejects_real_set_b_assessment_before_writing(tmp_path, monkeypatch):
    path = HERE.parent / "experiment-v4/reuse-01/freeze_questions.py"
    spec = importlib.util.spec_from_file_location("refusing_question_freezer", path)
    freezer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(freezer)
    questions = json.loads(
        (HERE.parent / "experiment-v4/competency-questions-set-b.json").read_bytes()
    )
    source = encoded(
        {"schema": questions["schema"], "questions": questions["questions"]}
    )
    draft = tmp_path / "draft.json"
    draft.write_bytes(source)
    spec = importlib.util.spec_from_file_location(
        "refusing_audit", HERE / "audit_controls.py"
    )
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    value = audit.audit()["set-b"]["assessment"]
    value["questions_sha256"] = digest(source)
    assessment_path = tmp_path / "assessment.json"
    assessment_path.write_bytes(encoded(value))
    output = tmp_path / "must-not-exist.json"
    monkeypatch.setattr(freezer, "OUTPUT", output)
    with pytest.raises(freezer.QuestionSetRefusal, match="instrument_count"):
        freezer.freeze(draft, assessment_path)
    assert not output.exists()
    output.write_bytes(b"preserve existing frozen bytes")
    with pytest.raises(freezer.QuestionSetRefusal, match="already exists"):
        freezer.freeze(draft, assessment_path)
    assert output.read_bytes() == b"preserve existing frozen bytes"
