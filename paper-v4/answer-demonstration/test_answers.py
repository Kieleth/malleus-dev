"""Synthetic tests of paper-owned reads, with no paper answers in fixtures."""

from copy import deepcopy
from pathlib import Path

import pytest

from answers import GraphReads, QueryNotExpressible, PROGRAMS, answer, contains, normal


class Graph:
    def __init__(self, nodes, edges=()):
        self.nodes = deepcopy(nodes)
        self.edges = deepcopy(list(edges))

    def query(self, entity_type=None):
        return deepcopy([n for n in self.nodes if n["type"] == entity_type])

    def query_relations(self):
        return deepcopy(self.edges)

    def get_node(self, node_id):
        return next((deepcopy(n) for n in self.nodes if n["id"] == node_id), None)


def view(nodes, edges=()):
    types = {}
    for node in nodes:
        types.setdefault(node["type"], set()).update(node)
    surface = {
        "record_types": [
            {
                "name": name,
                "family": "ENTITY",
                "slots": [{"name": x} for x in sorted(slots)],
            }
            for name, slots in types.items()
        ]
    }
    for name in sorted({edge["type"] for edge in edges}):
        surface["record_types"].append(
            {
                "name": name,
                "family": "RELATION",
                "slots": [
                    {
                        "name": "relation_type",
                        "enum_values": sorted(
                            {e["relation_type"] for e in edges if e["type"] == name}
                        ),
                    }
                ],
            }
        )
    if not edges:
        surface["record_types"].append(
            {
                "name": "ResearchRelation",
                "family": "RELATION",
                "slots": [{"name": "relation_type", "enum_values": ["SUPPORTS"]}],
            }
        )
    return GraphReads(Graph(nodes, edges), surface)


def obs(record_id, **fields):
    return {"id": record_id, "type": "Observation", **fields}


def test_registry_covers_thirty_questions():
    import json

    questions = json.loads(
        (
            Path(__file__).parents[1] / "experiment-v4/competency-questions-v3.json"
        ).read_bytes()
    )
    assert set(PROGRAMS) == {q["id"] for q in questions["questions"]}


def test_subjectless_count_is_reachable_without_inventing_subject():
    result = answer(
        view([obs("r-a", name="deployed ocean-bottom seismometers", count=7)]),
        "CQ-T1-02",
    )
    assert result["rows"][0]["record"]["count"] == 7
    assert result["rows"][0]["kind"] == "ENTITY"
    assert "subject" not in result["rows"][0]


def test_count_zero_is_not_missing():
    result = answer(view([obs("r-a", name="deployed OBSs", count=0)]), "CQ-T1-02")
    assert result["rows"][0]["record"]["count"] == 0


def test_minimum_detection_count_is_not_deployment_count():
    nodes = [
        obs("r-a", name="minimum OBSs detecting an event", count=4),
        obs("r-b", name="deployed OBS network", count=7),
    ]
    assert answer(view(nodes), "CQ-T1-02")["witness_ids"] == ["r-b"]


def test_id_locator_and_digest_are_not_search_text():
    node = obs(
        "deployed-OBSs", count=7, name="unrelated", assertion_locator="deployed OBSs"
    )
    assert answer(view([node]), "CQ-T1-02")["outcome"] == "NO_CANDIDATE"


def test_quantity_preserves_bounds_units_scope_and_modality():
    node = obs(
        "r-a",
        name="primary melt CO2 content",
        value_lower=2.5,
        value_upper=6.5,
        unit="arbitrary-unit",
        subject="r-b",
        assertion_modality="CALCULATED",
    )
    subject = {"id": "r-b", "type": "Material", "name": "primary melt"}
    result = answer(view([node, subject]), "CQ-T3-02")
    assert result["rows"][0]["record"]["value_lower"] == 2.5
    assert result["rows"][0]["record"]["unit"] == "arbitrary-unit"
    assert result["rows"][0]["record"]["assertion_modality"] == "CALCULATED"
    assert result["rows"][0]["subject"]["name"] == "primary melt"
    assert set(result["witness_ids"]) == {"r-a", "r-b"}


def test_missing_quantity_is_not_filled_from_name():
    node = obs("r-a", name="primary melt CO2 content about 7 arbitrary-units")
    assert answer(view([node]), "CQ-T3-02")["outcome"] == "NO_CANDIDATE"


def test_distinct_ranges_remain_distinct_candidates():
    nodes = [
        obs("a", name="primary melt CO2 content", value_lower=2),
        obs("b", name="primary melt CO2 content", value_lower=8),
    ]
    assert len(answer(view(nodes), "CQ-T3-02")["rows"]) == 2


def test_pre_eruptive_stage_not_substituted_for_primary_melt():
    node = obs("r-a", name="pre-eruptive melt CO2 concentration", value_lower=2)
    assert answer(view([node]), "CQ-T3-02")["outcome"] == "NO_CANDIDATE"


def test_hypothesis_keeps_status_and_does_not_select_by_record_id():
    node = {
        "id": "arbitrary-id",
        "type": "Claim",
        "name": "candidate explanation",
        "hypothesis_disposition": "PREFERRED",
        "assertion_modality": "HYPOTHESISED",
    }
    result = answer(view([node]), "CQ-T4-01")
    assert result["rows"][0]["record"]["assertion_modality"] == "HYPOTHESISED"
    assert result["outcome"] == "CANDIDATES_FOR_REVIEW"


def test_declined_candidates_use_disposition_without_answer_word_selection():
    nodes = [
        {
            "id": "a",
            "type": "Claim",
            "name": "candidate alpha",
            "hypothesis_disposition": "NOT_SUPPORTED",
        },
        {
            "id": "b",
            "type": "ReportedClaim",
            "statement": "candidate beta",
            "hypothesis_disposition": "NOT_SUPPORTED",
        },
        {
            "id": "c",
            "type": "Claim",
            "name": "melt movement",
            "hypothesis_disposition": "PREFERRED",
        },
        {"id": "d", "type": "Claim", "name": "unsupported melt movement"},
    ]
    reads = view(nodes)
    before = deepcopy(reads.graph.nodes)
    result = answer(reads, "CQ-T4-02")
    assert result["witness_ids"] == ["a", "b"]
    assert result["paths"] == []
    assert all("subject" not in row for row in result["rows"])
    assert reads.graph.nodes == before


@pytest.mark.parametrize(
    "wording",
    [
        "Assumption for CO₂ from trace elements: an unspecified condition.",
        "Assumption for CO 2 from trace ele-\nment abundances: an unspecified condition.",
        "Assumption for carbon dioxide from trace ele-\r\nment abundances: an unspecified condition.",
    ],
)
def test_caveat_reaches_line_wrapped_text_without_rewriting_it(wording):
    node = {"id": "a", "type": "ReportedClaim", "statement": wording}
    result = answer(view([node]), "CQ-T4-03")
    assert result["witness_ids"] == ["a"]
    assert result["rows"][0]["record"]["statement"] == wording
    assert result["paths"] == []


def test_linebreak_matching_preserves_word_boundaries_and_compound_alternative():
    assert contains("trace ele-\nment", "trace element")
    assert contains("signal-\nprocessing", "signal processing")
    assert not contains("trace ele-ment", "trace element")
    assert not contains("trace elephant", "trace element")
    assert not contains("trace ele-\nmentary", "trace element")


def test_caveat_does_not_search_identifiers_or_unrelated_prose():
    nodes = [
        {"id": "CO 2 trace elements assumption", "type": "Claim", "name": "other"},
        {"id": "a", "type": "Claim", "statement": "CO 2 from trace elements"},
        {
            "id": "b",
            "type": "Claim",
            "statement": "Assumption about a different method",
        },
    ]
    assert answer(view(nodes), "CQ-T4-03")["outcome"] == "NO_CANDIDATE"


def test_no_implicit_support_edge_from_cooccurrence():
    claim = {
        "id": "c",
        "type": "Claim",
        "name": "degassing mechanism",
        "hypothesis_disposition": "PREFERRED",
    }
    evidence = obs("o", name="volatile content and earthquake depth", value_lower=3)
    result = answer(view([claim, evidence]), "CQ-T5-01")
    assert result["paths"] == []
    assert not any(row["kind"] == "RELATION" for row in result["rows"])


def test_support_traversal_uses_and_returns_real_edge():
    claim = {
        "id": "c",
        "type": "Claim",
        "name": "degassing mechanism",
        "hypothesis_disposition": "PREFERRED",
    }
    evidence = obs("o", name="volatile content", value_lower=3)
    edge = {
        "key": "e",
        "type": "ResearchRelation",
        "source_id": "o",
        "target_id": "c",
        "relation_type": "SUPPORTS",
    }
    result = answer(view([claim, evidence], [edge]), "CQ-T5-01")
    assert result["paths"] == [["o", "e", "c"]]
    assert set(result["witness_ids"]) == {"o", "e", "c"}


def test_controls_are_executed_not_short_circuited_to_expected_none():
    node = obs("s", name="basalt sulfur concentration", value_lower=1, unit="unit")
    assert answer(view([node]), "CQ-C-01")["rows"]


def test_paraphrases_execute_same_program():
    assert PROGRAMS["CQ-C-04"] is PROGRAMS["CQ-T1-02"]
    assert PROGRAMS["CQ-C-05"] is PROGRAMS["CQ-T3-02"]


def test_unknown_question_refuses():
    with pytest.raises(ValueError, match="unknown question"):
        answer(view([]), "missing")


def test_broken_reference_refuses_instead_of_omitting_subject():
    node = obs("a", name="primary melt CO2", value_lower=2, subject="missing")
    with pytest.raises(ValueError, match="missing subject"):
        answer(view([node]), "CQ-T3-02")


def test_malformed_surface_refuses():
    with pytest.raises((KeyError, ValueError)):
        GraphReads(Graph([]), {})


def test_duplicate_surface_type_refuses():
    entry = {"name": "A", "family": "ENTITY", "slots": []}
    with pytest.raises(ValueError, match="duplicate"):
        GraphReads(Graph([]), {"record_types": [entry, entry]})


def test_unicode_normalization_does_not_use_substring_as_word():
    assert normal("CO₂") == "co2"
    assert not view([obs("a", name="chlorinated basalt", value_lower=1)]).matching(
        ("chlorine",)
    )


def test_reads_do_not_mutate_graph():
    reads = view([obs("a", name="primary melt CO2", value_lower=2)])
    before = deepcopy(reads.graph.nodes)
    answer(reads, "CQ-T3-02")
    assert reads.graph.nodes == before


def test_absent_schema_type_is_not_an_empty_success():
    with pytest.raises(QueryNotExpressible):
        view([]).typed("Campaign")


def test_undeclared_relation_meaning_is_not_invented():
    result = answer(view([obs("a", name="initial location method")]), "CQ-T2-02")
    assert result["outcome"] == "NOT_EXPRESSIBLE"
    assert result["rows"] == []


def test_missing_required_record_id_refuses():
    with pytest.raises(KeyError):
        answer(
            view(
                [{"type": "Observation", "name": "primary melt CO2", "value_lower": 2}]
            ),
            "CQ-T3-02",
        )


def test_relational_answer_excludes_unjoined_mentions_and_bibliography():
    nodes = [
        {"id": "f", "type": "Feature", "name": "detachment fault"},
        {"id": "r", "type": "Feature", "name": "ridge subsection"},
        {"id": "b", "type": "Book", "name": "detachment fault textbook"},
    ]
    edge = {
        "key": "e",
        "type": "SpatialRelation",
        "source_id": "r",
        "target_id": "f",
        "relation_type": "BOUNDED_BY",
    }
    result = answer(view(nodes, [edge]), "CQ-T2-01")
    assert len(result["rows"]) == 1
    assert result["rows"][0]["kind"] == "RELATION"
    assert "b" not in result["witness_ids"]


def test_bounding_qualifier_is_returned_only_through_existing_subject():
    nodes = [
        {"id": "f", "type": "Feature", "name": "detachment fault"},
        {"id": "r", "type": "Feature", "name": "subsection alpha"},
        {"id": "other", "type": "Feature", "name": "subsection beta"},
        {
            "id": "c",
            "type": "Claim",
            "subject": "r",
            "statement": "A detachment fault and oceanic core complex bound this subsection on its western side.",
            "assertion_modality": "STATED",
        },
        {
            "id": "wrong-subject",
            "type": "Claim",
            "subject": "other",
            "statement": "A detachment fault carries an oceanic core complex.",
        },
        {
            "id": "unjoined",
            "type": "Claim",
            "statement": "A detachment fault carries an oceanic core complex.",
        },
        {
            "id": "irrelevant",
            "type": "Claim",
            "subject": "r",
            "statement": "Some other property of this subsection.",
        },
    ]
    edge = {
        "key": "e",
        "type": "SpatialRelation",
        "source_id": "r",
        "target_id": "f",
        "relation_type": "BOUNDED_BY",
    }
    result = answer(view(nodes, [edge]), "CQ-T2-01")
    assert set(result["witness_ids"]) == {"r", "f", "e", "c"}
    assert result["paths"] == [["r", "e", "f"]]
    prose, relation = result["rows"]
    assert prose["kind"] == "SUBJECT"
    assert prose["record"]["statement"] == nodes[3]["statement"]
    assert relation["kind"] == "RELATION"
    assert relation["relation"] == {"relation_type": "BOUNDED_BY"}
