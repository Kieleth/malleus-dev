"""A richer-looking replacement must not hide lost typed values."""

import pytest


def records(rows):
    return {
        "entities": rows,
        "relations": [],
        "events": [],
        "signals": [],
        "event_participations": [],
    }


def test_prose_replacement_exposes_removed_typed_quantity():
    from capture_delta import compare

    before = records(
        [
            {
                "id": "q",
                "type": "Observation",
                "properties": {"value_lower": 7, "unit": "u"},
            }
        ]
    )
    after = records(
        [{"id": "c", "type": "Claim", "properties": {"statement": "A value of 7 u."}}]
    )
    result = compare(before, after)
    assert result["removed_record_ids"] == ["q"]
    assert result["added_record_ids"] == ["c"]
    assert result["numeric_properties_before"] == 1
    assert result["numeric_properties_after"] == 0
    assert result["lost_properties"]["q"] == ["unit", "value_lower"]


def test_same_identity_changed_value_is_not_preservation():
    from capture_delta import compare

    before = records(
        [{"id": "q", "type": "Observation", "properties": {"value_lower": 0}}]
    )
    after = records(
        [{"id": "q", "type": "Observation", "properties": {"value_lower": 1}}]
    )
    result = compare(before, after)
    assert result["changed_record_ids"] == ["q"]
    assert result["changed_properties"]["q"] == ["value_lower"]
    assert result["unchanged_record_ids"] == []
    assert (
        result["numeric_properties_before"] == result["numeric_properties_after"] == 1
    )


def test_incomplete_or_duplicate_export_refuses():
    from capture_delta import compare

    with pytest.raises(ValueError, match="families"):
        compare({}, records([]))
    row = {"id": "q", "type": "Observation", "properties": {}}
    with pytest.raises(ValueError, match="duplicate"):
        compare(records([row, row]), records([]))
