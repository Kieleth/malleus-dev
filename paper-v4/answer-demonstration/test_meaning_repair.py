"""Mechanical limits for a source-reviewed amendment, not semantic approval."""

from copy import deepcopy
import pytest


def fixture():
    def slot(name, range_id="urn:String"):
        return {"name": name, "range_id": range_id, "multivalued": False}

    surface = {
        "record_types": [
            {
                "name": "Claim",
                "qualified_name": "urn:Claim",
                "slots": [
                    slot("statement"),
                    slot("description"),
                    slot("subject", "urn:Claim"),
                ],
            },
            {
                "name": "Link",
                "qualified_name": "urn:Link",
                "slots": [
                    slot("source_id", "urn:Claim"),
                    slot("target_id", "urn:Claim"),
                ],
            },
        ]
    }
    base = {
        "entities": [
            {
                "id": "a",
                "type": "Claim",
                "properties": {
                    "count": 1,
                    "unit": "m",
                    "uncertainty": 0.2,
                    "assertion_modality": "HYPOTHESISED",
                    "hypothesis_disposition": "PREFERRED",
                },
            },
            {"id": "b", "type": "Claim", "properties": {}},
        ],
        "relations": [
            {
                "id": "r",
                "type": "Link",
                "source_id": "a",
                "target_id": "b",
                "properties": {"relation_type": "SUPPORTS"},
            }
        ],
    }
    after = deepcopy(base["entities"][0])
    after["id"] = "a2"
    after["properties"]["statement"] = "Synthetic proposed statement."
    candidate = {
        "records": {
            "entities": [after],
            "relations": [{**base["relations"][0], "id": "r2", "source_id": "a2"}],
        },
        "supersessions": [
            {"supersedes_record_id": "a", "record_id": "a2"},
            {"supersedes_record_id": "r", "record_id": "r2"},
        ],
    }
    return base, deepcopy(candidate), surface


def check(base, candidate, surface):
    from meaning_repair import check_scope

    return check_scope(base, candidate, surface, targets={"a"})


def test_permits_shape_without_asserting_source_support():
    assert check(*fixture()) == {"a": "a2", "r": "r2"}


def test_mutation_fixture_does_not_modify_its_own_reference():
    base, candidate, _ = fixture()
    candidate["records"]["relations"][0]["properties"]["relation_type"] = "CHALLENGES"
    assert base["relations"][0]["properties"]["relation_type"] == "SUPPORTS"


@pytest.mark.parametrize(
    "fault",
    [
        "count",
        "numeric_boolean",
        "unit",
        "uncertainty",
        "modality",
        "disposition",
        "type",
        "extra_field",
        "missing_edge",
        "changed_edge",
        "duplicate_prior",
        "reused_id",
        "no_op",
        "unselected",
        "dangling_subject",
        "new_relation",
        "header",
        "undeclared_field",
        "dropped_family",
        "empty_text",
    ],
)
def test_refuses_scope_drift(fault):
    base, candidate, surface = fixture()
    row = candidate["records"]["entities"][0]
    p = row["properties"]
    if fault == "count":
        p["count"] = 2
    elif fault == "numeric_boolean":
        p["count"] = True
    elif fault == "unit":
        del p["unit"]
    elif fault == "uncertainty":
        p["uncertainty"] = 0.3
    elif fault == "modality":
        p["assertion_modality"] = "MEASURED"
    elif fault == "disposition":
        p["hypothesis_disposition"] = "CONFIRMED"
    elif fault == "type":
        row["type"] = "Different"
    elif fault == "extra_field":
        p["confidence"] = 1
    elif fault == "missing_edge":
        candidate["records"]["relations"] = []
        candidate["supersessions"].pop()
    elif fault == "changed_edge":
        candidate["records"]["relations"][0]["properties"]["relation_type"] = (
            "CHALLENGES"
        )
    elif fault == "duplicate_prior":
        candidate["supersessions"].append(candidate["supersessions"][0])
    elif fault == "reused_id":
        row["id"] = "a"
    elif fault == "no_op":
        del p["statement"]
    elif fault == "unselected":
        candidate["supersessions"][0]["supersedes_record_id"] = "b"
    elif fault == "dangling_subject":
        p["subject"] = "missing"
    elif fault == "new_relation":
        candidate["records"]["relations"].append({**base["relations"][0], "id": "new"})
    elif fault == "header":
        row["extra"] = "value"
    elif fault == "undeclared_field":
        surface["record_types"][0]["slots"] = []
    elif fault == "dropped_family":
        del candidate["records"]["relations"]
    elif fault == "empty_text":
        p["statement"] = "  "
    with pytest.raises(ValueError):
        check(base, candidate, surface)


def test_context_removal_is_explicit_not_silent_preservation():
    base, candidate, surface = fixture()
    base["entities"][0]["properties"]["subject"] = "b"
    # The original subject can be removed, but still requires source review.
    assert check(base, candidate, surface)["a"] == "a2"


def test_other_typed_dependants_must_be_retargeted_exactly():
    base, candidate, surface = fixture()
    base["entities"][1]["properties"]["subject"] = "a"
    with pytest.raises(ValueError, match="closure"):
        check(base, candidate, surface)
    candidate["records"]["entities"].append(
        {"id": "b2", "type": "Claim", "properties": {"subject": "a2"}}
    )
    candidate["supersessions"].append({"supersedes_record_id": "b", "record_id": "b2"})
    candidate["records"]["relations"][0]["target_id"] = "b2"
    assert check(base, candidate, surface)["b"] == "b2"
    candidate["records"]["entities"][1]["properties"]["description"] = (
        "Unselected new meaning"
    )
    with pytest.raises(ValueError):
        check(base, candidate, surface)
