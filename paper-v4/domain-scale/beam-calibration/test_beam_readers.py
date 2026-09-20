"""Reader packets expose questions, never answer keys or investigator findings."""

import json
from pathlib import Path

import pytest
import yaml

from beam_prepare import canonical, digest
from beam_readers import question_view, validate_answers


def test_reader_packets_are_exact_separated_and_share_question_bytes():
    root = Path(__file__).resolve().parents[3]
    run = root / "private/beam-weather-calibration-01"
    packets = run / "readers-01"
    assert (packets / "source/questions.json").read_bytes() == (
        packets / "graph/questions.json"
    ).read_bytes()
    questions = json.loads((packets / "source/questions.json").read_bytes())[
        "questions"
    ]
    assert len(questions) == 20
    assert all(set(q) == {"id", "question"} for q in questions)
    for condition, origin in (
        ("source", "reading-packet/reading.json"),
        ("graph", "producer/work/records.json"),
    ):
        packet = packets / condition
        assert (packet / "evidence.json").read_bytes() == (run / origin).read_bytes()
        manifest = json.loads((packet / "manifest.json").read_bytes())
        for item in manifest["inputs"]:
            path = packet / item["path"]
            assert path.resolve().is_relative_to(packet)
            assert digest(path.read_bytes()) == item["sha256"]
        names = {i["path"] for i in manifest["inputs"]}
        assert not any("capture" in n or "rubric" in n or "report" in n for n in names)
        if condition == "source":
            assert names == {"task.md", "questions.json", "evidence.json"}
    graph = packets / "graph"
    pending, visited = ["ontology.yaml"], set()
    while pending:
        name = pending.pop()
        if name in visited:
            continue
        source = yaml.safe_load((graph / name).read_bytes())
        visited.add(name)
        if "imports" in source:
            pending.extend(
                f"imports/{i.replace(':', '_')}.yaml" for i in source["imports"]
            )
    assert len(visited) == 6


def test_question_view_preserves_text_and_order_but_removes_evaluator_metadata():
    raw = canonical(
        {
            "hidden_category": [
                {
                    "question": "Question?",
                    "answer": "SECRET",
                    "rubric": ["SECRET"],
                    "source_chat_ids": [99],
                }
            ]
        }
    )
    result = question_view(raw)
    assert result == {"questions": [{"id": "q01", "question": "Question?"}]}
    assert b"SECRET" not in canonical(result)
    assert b"hidden_category" not in canonical(result)


def valid_case():
    questions = canonical({"questions": [{"id": "q01", "question": "What?"}]})
    evidence = canonical(
        {"pages": [{"blocks": [{"id": "block:1", "text": "Reported five items."}]}]}
    )
    answer = {
        "condition": "source",
        "questions_sha256": digest(questions),
        "evidence_sha256": digest(evidence),
        "answers": [
            {
                "question_id": "q01",
                "answer": "Five items were reported.",
                "status": "ANSWERED",
                "evidence": [
                    {
                        "locator": "block:1",
                        "path": ["text"],
                        "excerpt": "five items",
                        "supports": "Reported count",
                    }
                ],
                "limitations": "Report only.",
            }
        ],
    }
    return answer, questions, evidence


def test_valid_citation_is_not_semantic_certification():
    answer, questions, evidence = valid_case()
    answer["answers"][0]["answer"] = (
        "An unsupported interpretation can still have a valid citation."
    )
    assert (
        validate_answers(canonical(answer), questions, evidence, "source")[
            "semantic_support"
        ]
        == "NOT_CHECKED"
    )


@pytest.mark.parametrize(
    "mutation",
    [
        "missing",
        "duplicate",
        "wrong_input",
        "unknown_locator",
        "unknown_path",
        "invented_excerpt",
        "no_evidence",
        "wrong_condition",
    ],
)
def test_answer_contract_refuses_missing_or_unbound_evidence(mutation):
    answer, questions, evidence = valid_case()
    row = answer["answers"][0]
    if mutation == "missing":
        answer["answers"] = []
    elif mutation == "duplicate":
        answer["answers"].append(row)
    elif mutation == "wrong_input":
        answer["evidence_sha256"] = "sha256:wrong"
    elif mutation == "unknown_locator":
        row["evidence"][0]["locator"] = "block:2"
    elif mutation == "unknown_path":
        row["evidence"][0]["path"] = ["absent"]
    elif mutation == "invented_excerpt":
        row["evidence"][0]["excerpt"] = "six items"
    elif mutation == "no_evidence":
        row["evidence"] = []
    else:
        answer["condition"] = "graph"
    with pytest.raises(ValueError):
        validate_answers(canonical(answer), questions, evidence, "source")


def test_missing_required_question_is_not_defaulted():
    with pytest.raises(ValueError):
        question_view(canonical({"category": [{"rubric": ["secret"]}]}))


def test_graph_citations_resolve_exact_properties():
    answer, questions, _ = valid_case()
    evidence = canonical(
        {
            "entities": [{"id": "entity:1", "properties": {"number": 5}}],
            "relations": [],
            "events": [],
            "signals": [],
            "event_participations": [],
        }
    )
    answer["condition"] = "graph"
    answer["evidence_sha256"] = digest(evidence)
    answer["answers"][0]["evidence"][0].update(
        locator="entity:1", path=["properties", "number"], excerpt="5"
    )
    result = validate_answers(canonical(answer), questions, evidence, "graph")
    assert result["citations"] == 1
