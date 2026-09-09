"""Explicit schema text binding, independent of paper answer values."""

from copy import deepcopy
from pathlib import Path

import pytest

from binding import load_query_program
from test_answers import Graph


# These controls measure the historical text-binding intervention, not today's
# independently approved typed-depth selector. Keep their program explicit.
answers = load_query_program(
    Path(__file__).resolve().parents[2]
    / "private/paper-v4-answer-demonstration/sol-qualification-01/answers.py",
    "sha256:55c1e5cc50245c5eae8879bce71f4badb055027e50c51f85d38cd650eb4281a2",
)
HistoricalReads, answer = answers.GraphReads, answers.answer


STRING = "https://malleus.dev/contract-facts/String"


def surface(extra=()):
    names = ("id", "observation_kind", "quantity_kind", "assertion_locator", "unit")
    return {
        "record_types": [
            {
                "name": "Observation",
                "family": "ENTITY",
                "slots": [
                    {
                        "name": name,
                        "range_id": STRING,
                        "identifier": name == "id",
                        "multivalued": False,
                    }
                    for name in (*names, *extra)
                ]
                + [
                    {
                        "name": "value_lower",
                        "range_id": "https://malleus.dev/contract-facts/Float",
                        "identifier": False,
                        "multivalued": False,
                    }
                ],
            }
        ]
    }


def test_declared_observation_text_recovers_quantity_without_rewriting_it():
    from ontology_answers import GraphReads

    node = {
        "id": "r",
        "type": "Observation",
        "quantity_kind": "depth",
        "observation_kind": "earthquake depth",
        "value_lower": 7.25,
        "unit": "synthetic-unit",
    }
    graph = Graph([node])
    assert answer(HistoricalReads(graph, surface()), "CQ-T3-01")["rows"] == []
    result = answer(GraphReads(graph, surface(), program=answers), "CQ-T3-01")
    assert result["rows"][0]["record"] == {
        key: value for key, value in node.items() if key not in {"id", "type"}
    }
    assert result["paths"] == []
    assert graph.nodes == [node]


@pytest.mark.parametrize("field", ["id", "assertion_locator", "unit"])
def test_metadata_or_unit_cannot_supply_semantic_qualifier(field):
    from ontology_answers import GraphReads

    node = {
        "id": "r",
        "type": "Observation",
        "value_lower": 0,
        field: "earthquake depth",
    }
    assert (
        answer(GraphReads(Graph([node]), surface(), program=answers), "CQ-T3-01")[
            "rows"
        ]
        == []
    )


def test_missing_numeric_value_is_not_extracted_from_text():
    from ontology_answers import GraphReads

    node = {"id": "r", "type": "Observation", "observation_kind": "earthquake depth 7"}
    assert (
        answer(GraphReads(Graph([node]), surface(), program=answers), "CQ-T3-01")[
            "rows"
        ]
        == []
    )


def test_unknown_string_slot_refuses_instead_of_being_silently_ignored():
    from ontology_answers import text_binding

    with pytest.raises(ValueError, match="unclassified.*new_label"):
        text_binding(surface(("new_label",)))


def test_binding_depends_on_schema_not_graph_or_values():
    from ontology_answers import text_binding

    assert text_binding(surface()) == {
        "Observation": ["observation_kind", "quantity_kind"]
    }
    wrong = deepcopy(surface())
    del wrong["record_types"][0]["slots"][0]["range_id"]
    with pytest.raises(KeyError):
        text_binding(wrong)
    duplicate = deepcopy(surface())
    duplicate["record_types"][0]["slots"].append(
        duplicate["record_types"][0]["slots"][1]
    )
    with pytest.raises(ValueError, match="duplicate slot"):
        text_binding(duplicate)


def test_declared_multivalued_text_is_checked_and_projected_exactly():
    from ontology_answers import GraphReads

    schema = surface(("tags",))
    schema["record_types"][0]["slots"][-2]["multivalued"] = True
    node = {
        "id": "r",
        "type": "Observation",
        "tags": ["earthquake", "depth"],
        "value_lower": 0,
    }
    assert (
        answer(GraphReads(Graph([node]), schema, program=answers), "CQ-T3-01")["rows"][
            0
        ]["record"]["tags"]
        == node["tags"]
    )
    node["tags"] = "earthquake depth"
    with pytest.raises(ValueError, match="text value shape"):
        answer(GraphReads(Graph([node]), schema, program=answers), "CQ-T3-01")


def test_actual_frozen_graph_query_and_review_packet_remain_separate():
    import subprocess
    import sys

    # Repository pytest injects living src/ ahead of PYTHONPATH. The experiment
    # subprocess must use the explicitly selected runtime, just like execution.
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_ontology_answers import check_actual; check_actual()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_actual():
    import json
    from pathlib import Path
    from tempfile import TemporaryDirectory
    from ontology_query import freeze, execute, prepare_review, method_inputs
    from review_packet import digest

    root = Path(__file__).resolve().parents[2]
    run = root / "private/paper-v4-answer-demonstration/sol-e2e-corrected-01"
    original = run / "attempt-01"
    protected = {p: digest(p.read_bytes()) for p in original.rglob("*") if p.is_file()}
    with TemporaryDirectory(dir=root / "private") as temporary:
        target = Path(temporary)
        freeze(run, target / "method")
        result = execute(
            run, original, target / "method", target / "query", compare_original=True
        )
        assert result["original_queries_reproduced"]
        assert result["ledger_bytes_unchanged"]
        prepare_review(
            run, original, target / "method", target / "query", target / "review"
        )
        packet = json.loads((target / "review/review-input-manifest.json").read_bytes())
        names = {m["name"]: m["path"] for m in packet["materials"]}
        assert names["query_program"] == "ontology_answers.py"
        assert names["base_query_program"] == "answers.py"
        assert names["query_runner"] == "ontology_query.py"
        (target / "method/ontology_answers.py").write_bytes(b"# changed")
        with pytest.raises(ValueError):
            method_inputs(target / "method")
    assert protected == {
        p: digest(p.read_bytes()) for p in original.rglob("*") if p.is_file()
    }
