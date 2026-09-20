"""The derived CQ-C-03 file is what the script writes, and the rule is the rule.

Three things are checked: that ``derived-cq-c-03-v3.1.json`` on disk is byte for
byte what ``derive_cq_c_03_v31.build`` produces now, that the label rule reads
the three outcomes it claims to read, and that both v3 cells derive NONE, which
is what the control expects under v3.1.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import derive_cq_c_03_v31 as derive  # noqa: E402


SEMANTICS = ["site_set", "maximum_depth_quantity", "spreading_rate_quantity"]


def _coverage(*rows: int | None) -> list[dict]:
    return [
        {"semantic": semantic, "row_index": row_index}
        for semantic, row_index in zip(SEMANTICS, rows)
    ]


def test_file_on_disk_is_what_the_script_writes_now() -> None:
    expected = (
        json.dumps(derive.build(), ensure_ascii=False, indent=2).encode("utf-8")
        + b"\n"
    )
    assert derive.OUTPUT.read_bytes() == expected


def test_every_semantic_naming_a_row_is_covered() -> None:
    assert derive.label(_coverage(1, 2, 3), SEMANTICS) == "COVERED"


def test_no_semantic_naming_a_row_is_none() -> None:
    assert derive.label(_coverage(None, None, None), SEMANTICS) == "NONE"


def test_some_semantics_naming_a_row_is_partial() -> None:
    assert derive.label(_coverage(1, None, None), SEMANTICS) == "PARTIAL"


def test_the_dropped_semantic_no_longer_counts() -> None:
    coverage = _coverage(None, None, None) + [
        {"semantic": "compilation_source", "row_index": 140}
    ]
    four = SEMANTICS + ["compilation_source"]
    assert derive.label(coverage, four) == "PARTIAL"
    assert derive.label(coverage, SEMANTICS) == "NONE"


def test_v3_1_drops_compilation_source_alone() -> None:
    derived = json.loads(derive.OUTPUT.read_bytes())
    assert derived["dropped_semantics"] == ["compilation_source"]
    assert derived["required_semantics_v3_1"] == SEMANTICS


@pytest.mark.parametrize("run_id", derive.RUNS)
def test_both_v3_cells_derive_none_under_v3_1(run_id: str) -> None:
    derived = json.loads(derive.OUTPUT.read_bytes())
    cell = next(item for item in derived["cells"] if item["run_id"] == run_id)
    assert cell["recorded_responsiveness_v3"] == "PARTIAL"
    assert cell["derived_label_v3"] == "PARTIAL"
    assert cell["derived_label_v3_1"] == "NONE"
    assert cell["dropped_semantic"]["row_index"] is not None
    assert all(not item["names_a_row"] for item in cell["semantics_v3_1"])
