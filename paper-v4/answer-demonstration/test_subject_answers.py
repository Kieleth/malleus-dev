"""Subject-aware matching must follow one explicit reference, not join guesses."""

from copy import deepcopy

import pytest

from answers import answer
from test_answers import obs, view


def subject_view(nodes):
    from subject_answers import SubjectGraphReads

    original = view(nodes)
    return SubjectGraphReads(
        original.graph, {"record_types": list(original.types.values())}
    )


def test_existing_subject_recovers_split_description_and_preserves_row():
    nodes = [
        obs(
            "quantity:a",
            quantity_kind="CO2",
            value_lower=2.5,
            value_upper=6.5,
            unit="synthetic-unit",
            subject="material:a",
            assertion_modality="CALCULATED",
        ),
        {"id": "material:a", "type": "Material", "name": "primary melts"},
    ]
    assert answer(view(nodes), "CQ-T3-02")["rows"] == []
    reads = subject_view(nodes)
    before = deepcopy(reads.graph.nodes)
    result = answer(reads, "CQ-T3-02")
    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["record"] == {
        k: v for k, v in nodes[0].items() if k not in {"id", "type"}
    }
    assert row["subject"] == {"name": "primary melts"}
    assert result["paths"] == []
    assert reads.graph.nodes == before


@pytest.mark.parametrize("field", ["name", "description", "tags"])
def test_declared_subject_identity_text_can_select(field):
    subject = {
        "id": "s",
        "type": "Material",
        field: ["primary melt"] if field == "tags" else "primary melt",
    }
    result = answer(
        subject_view([obs("q", quantity_kind="CO2", count=0, subject="s"), subject]),
        "CQ-T3-02",
    )
    assert result["rows"][0]["record"]["count"] == 0


def test_unlinked_neighbor_cannot_supply_subject_words():
    nodes = [
        obs("q", quantity_kind="CO2", count=7),
        {"id": "s", "type": "Material", "name": "primary melt"},
    ]
    assert answer(subject_view(nodes), "CQ-T3-02")["rows"] == []


def test_numeric_fields_are_not_borrowed_from_subject():
    nodes = [
        obs("q", quantity_kind="CO2", subject="s"),
        {"id": "s", "type": "Material", "name": "primary melt", "count": 7},
    ]
    assert answer(subject_view(nodes), "CQ-T3-02")["rows"] == []


def test_subject_metadata_is_not_semantic_text():
    nodes = [
        obs("q", quantity_kind="CO2", count=7, subject="primary melt"),
        {
            "id": "primary melt",
            "type": "Material",
            "assertion_locator": "primary melt",
            "name": "other",
        },
    ]
    assert answer(subject_view(nodes), "CQ-T3-02")["rows"] == []


def test_subject_traversal_is_one_hop_only():
    nodes = [
        obs("q", quantity_kind="CO2", count=7, subject="a"),
        {"id": "a", "type": "Material", "name": "other", "subject": "b"},
        {"id": "b", "type": "Material", "name": "primary melt"},
    ]
    assert answer(subject_view(nodes), "CQ-T3-02")["rows"] == []


def test_missing_subject_is_an_error_not_an_empty_match():
    nodes = [obs("q", quantity_kind="CO2", count=7, subject="absent")]
    with pytest.raises(ValueError, match="missing subject"):
        answer(subject_view(nodes), "CQ-T3-02")


def test_subject_scope_does_not_cross_between_quantity_rows():
    nodes = [
        obs("a", quantity_kind="CO2", count=7, subject="pre"),
        obs("b", quantity_kind="water", count=3, subject="primary"),
        {"id": "pre", "type": "Material", "name": "pre-eruptive melt"},
        {"id": "primary", "type": "Material", "name": "primary melt"},
    ]
    assert answer(subject_view(nodes), "CQ-T3-02")["rows"] == []
