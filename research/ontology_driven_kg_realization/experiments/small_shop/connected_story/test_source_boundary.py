"""Independent source-boundary checks, not a semantic completeness score."""

from copy import deepcopy
from pathlib import Path

import pytest

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.source_boundary import (
    inspect_sources,
    load_sources,
)


HERE = Path(__file__).resolve().parent
EVENTS = (
    "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", "e11",
    "e18", "e19", "e20", "e21", "e27", "e28", "e29", "e30", "e33", "e34",
)


def test_every_selected_table_row_and_nonempty_field_is_accounted_for():
    rows, boundary = load_sources(HERE)
    report = inspect_sources(rows, boundary)
    assert tuple(row["event_id"] for row in rows) == EVENTS
    assert report["selected_rows"] == 21
    assert report["unaccounted_fields"] == []
    assert report["graph_populated"] is False
    assert report["inventory"] == {
        "actor_ids": ["R1", "R2", "R3", "R4", "R5"],
        "order_ids": ["O1", "O2"],
        "supplier_order_ids": ["A", "B"],
        "item_ids": ["X1", "X2", "X3", "Y1", "Y2"],
        "invoice_ids": ["I1", "I2"],
        "payment_ids": ["P1"],
    }


@pytest.mark.parametrize("defect", ["missing", "duplicate", "extra_field", "bad_locator"])
def test_source_census_refuses_silent_loss_or_invention(defect):
    rows, boundary = load_sources(HERE)
    before = deepcopy(rows)
    if defect == "missing":
        rows.pop(8)
    elif defect == "duplicate":
        rows.append(deepcopy(rows[0]))
    elif defect == "extra_field":
        rows[8]["invoice_amount"] = 42
    else:
        boundary["field_dispositions"]["time_text"]["source_field"] = "timestamp"
    with pytest.raises(ValueError):
        inspect_sources(rows, boundary)
    if defect == "bad_locator":
        assert rows == before


def test_invoice_update_and_ambiguous_times_are_not_repaired():
    rows, boundary = load_sources(HERE)
    by_id = {row["event_id"]: row for row in rows}
    assert by_id["e9"]["invoice_ids"] == ["I2"]
    assert "invoice_amount" not in by_id["e9"]
    assert "order_details_text" not in by_id["e9"]
    assert by_id["e6"]["time_text"] == "00-01 10:00"
    assert by_id["e8"]["time_text"] == "00-01 10:30"
    assert boundary["temporal_policy"]["calendar_instants"] == "NOT_DERIVED"
    assert by_id["e27"]["item_ids"] == ["X1", "X2", "Y1"]
    assert by_id["e33"]["item_ids"] == ["X3", "Y2"]
    assert by_id["e4"]["order_details_text"] == "1·Y"
    assert by_id["e7"]["order_details_text"] == "2·Y"


def test_exact_retained_table_bytes_are_checked(tmp_path):
    import shutil

    shutil.copytree(HERE / "sources", tmp_path / "sources")
    shutil.copyfile(HERE / "source_boundary.json", tmp_path / "source_boundary.json")
    path = tmp_path / "sources" / "table-1.png"
    path.write_bytes(path.read_bytes() + b"changed")
    with pytest.raises(ValueError, match="source digest"):
        load_sources(tmp_path)
