"""Depth selection uses typed bounds, with no document-specific answers."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from answers import answer
from test_answers import obs, view


@pytest.mark.parametrize(
    "wording",
    [
        "microseismicity depth",
        "MICROSEISMICITY depths",
        "micro-\nseismicity depth",
        "earthquake depth",
    ],
)
def test_depth_recognises_wording_and_preserves_scope_and_qualifications(wording):
    node = obs(
        "q",
        quantity_kind=wording,
        quantity_kind_class="Length",
        value_lower=2.5,
        value_upper=7.5,
        unit="m",
        determination="MEASURED",
        description="Synthetic short window",
        subject="s",
    )
    subject = {"id": "s", "type": "Site", "name": "synthetic site"}
    reads = view([node, subject])
    before = deepcopy(reads.graph.nodes)
    result = answer(reads, "CQ-T3-01")
    assert result["witness_ids"] == ["q", "s"]
    assert result["rows"][0]["record"] == {
        k: v for k, v in node.items() if k not in {"id", "type"}
    }
    assert result["rows"][0]["subject"] == {"name": "synthetic site"}
    assert "reference_surface" not in result["rows"][0]["record"]
    assert result["paths"] == []
    assert reads.graph.nodes == before


@pytest.mark.parametrize(
    "fields",
    [
        {"quantity_kind_class": "Temperature", "value_lower": 700},
        {"quantity_kind_class": "MassFraction", "value_lower": 0.5},
        {"quantity_kind_class": "Length", "count": 5},
        {"quantity_kind_class": "Length", "ratio_value": 0.5},
        {"quantity_kind_class": "Length", "uncertainty": 2},
        {"quantity_kind_class": "Length", "value_lower": "2"},
        {"quantity_kind_class": "Length", "value_lower": True},
        {"quantity_kind_class": "Length"},
        {"unit": "km", "value_lower": 2},
    ],
)
def test_depth_excludes_nonlength_and_nonbound_candidates_without_inference(fields):
    node = obs("depth-Length-2", quantity_kind="earthquake depth 2", **fields)
    assert answer(view([node]), "CQ-T3-01")["outcome"] == "NO_CANDIDATE"


@pytest.mark.parametrize("field", ["value_lower", "value_upper"])
def test_depth_keeps_zero_and_open_bounds_without_filling_the_other(field):
    node = obs(
        "q",
        quantity_kind="microseismicity depth",
        quantity_kind_class="Length",
        **{field: 0},
    )
    record = answer(view([node]), "CQ-T3-01")["rows"][0]["record"]
    assert record[field] == 0
    assert ({"value_lower", "value_upper"} - {field}).isdisjoint(record)
    assert "unit" not in record and "determination" not in record


def test_depth_change_does_not_widen_other_programs_or_global_word_matching():
    from answers import contains

    assert not contains("microseismicity", "seismicity")
    node = obs(
        "q",
        quantity_kind="earthquake depth",
        quantity_kind_class="Temperature",
        value_lower=700,
    )
    assert answer(view([node]), "CQ-T3-01")["rows"] == []
    node["quantity_kind"] = "horizontal uncertainty"
    assert answer(view([node]), "CQ-T3-04")["witness_ids"] == ["q"]


def test_depth_delta_guard_refuses_other_questions_changed_fields_and_paths():
    from relation_query import check_depth_selection

    node = obs(
        "q",
        quantity_kind="earthquake depth",
        quantity_kind_class="Length",
        value_lower=3,
    )
    query = answer(view([node]), "CQ-T3-01")
    unrelated = answer(view([node]), "CQ-T4-01")
    before = [query, unrelated]
    check_depth_selection(before, deepcopy(before))
    for fault in ("other_question", "value", "path", "witness", "dimension"):
        after = deepcopy(before)
        if fault == "other_question":
            after[1]["note"] = "changed"
        elif fault == "value":
            after[0]["rows"][0]["record"]["value_lower"] = 4
        elif fault == "path":
            after[0]["paths"] = [["invented"]]
        elif fault == "witness":
            after[0]["witness_ids"] = []
        else:
            after[0]["rows"][0]["record"]["quantity_kind_class"] = "Temperature"
        with pytest.raises(ValueError):
            check_depth_selection(before, after)


def test_depth_comparison_reproduces_the_control_and_preserves_all_run_bytes():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_depth_query import check_execution; check_execution()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_execution():
    from tempfile import TemporaryDirectory
    from relation_query import freeze, execute
    from review_packet import digest

    run = (
        Path(__file__).resolve().parents[2]
        / "private/paper-v4-answer-demonstration/sol-qualification-01"
    )

    def tree(path):
        return {
            str(p.relative_to(path)): p.read_bytes()
            for p in path.rglob("*")
            if p.is_file()
        }

    protected = tree(run)
    with TemporaryDirectory(dir=run.parent, prefix="depth-query-test-") as tmp:
        root = Path(tmp)
        method = freeze(run, root / "method", depth=True)
        assert method["decision"] == "E-0277"
        assert method["condition"] == "QUERY_ONLY_TYPED_DEPTH_SELECTION"
        summary = execute(run, root / "method", root / "first")
        assert summary["changed_questions"] == ["CQ-T3-01"]
        assert summary["depth_selection_only"] and summary["ledger_bytes_unchanged"]
        assert summary["original_queries_reproduced"]
        execute(run, root / "method", root / "repeat")
        assert tree(root / "first") == tree(root / "repeat")
        result = json.loads((root / "first/query-result.json").read_bytes())
        assert not any(result["forbidden_attempts"].values())
        query = next(q for q in result["queries"] if q["question_id"] == "CQ-T3-01")
        candidate = json.loads(
            (run / "evidence/attempt-01/submitted-population.json").read_bytes()
        )
        qualified = candidate["records"]["entities"][0]
        assert qualified["id"] in query["witness_ids"]
        assert {"count:forced-depth-subset", "observation:bdb-temperature"}.isdisjoint(
            query["witness_ids"]
        )
        nodes = {
            r["id"]: r["properties"]
            for r in json.loads(
                (run / "evidence/attempt-01/export-records.json").read_bytes()
            )["entities"]
        }
        for row in query["rows"]:
            assert row["record"] == nodes[row["witness"]["record_id"]]
        assert (
            digest((run / "evidence/attempt-01/replay-receipt.json").read_bytes())
            == result["inputs"]["replay_receipt_sha256"]
        )
        (root / "method/answers.py").write_bytes(b"drift")
        with pytest.raises(ValueError):
            execute(run, root / "method", root / "drift")
        assert not (root / "drift").exists()
    assert tree(run) == protected


def test_retained_depth_comparison_binds_every_projection_and_capture():
    from followup import verify_materials
    from review_packet import digest, verify_trace_materials

    run = (
        Path(__file__).resolve().parents[2]
        / "private/paper-v4-answer-demonstration/sol-qualification-01"
    )
    method = run / "depth-method-01"
    verify_materials(
        method, json.loads((method / "method.json").read_bytes())["materials"]
    )

    def tree(path):
        return {
            str(p.relative_to(path)): p.read_bytes()
            for p in path.rglob("*")
            if p.is_file()
        }

    result = tree(run / "depth-query-01")
    assert len(result) == 4
    assert result == tree(run / "depth-query-reproduction-01")
    query = json.loads(result["query-result.json"])
    traces = json.loads(result["query-trace-summary.json"])["records"]
    assert (
        digest(result["query-result.json"])
        == "sha256:af325d88662ec2aee0fd29fb2cfcd37c5f9bd47e65375a9498fb9c1522e930aa"
    )
    assert len(traces) == 55
    assert {t["record_id"] for t in traces} == {
        key for q in query["queries"] for key in q["witness_ids"]
    }
    inputs = run / "evidence/producer/inputs"
    captures = {
        digest(p.read_bytes()): p
        for p in [
            *inputs.glob("*capture.json"),
            run / "evidence/attempt-01/retained-capture.json",
        ]
    }
    assert len(captures) == 5
    for trace in traces:
        selected = set(trace["evidence"].values()) & set(captures)
        assert len(selected) == 1
        verify_trace_materials(
            (inputs / "selected-reading.json").read_bytes(),
            captures[next(iter(selected))].read_bytes(),
            {"records": [trace]},
        )
    old = json.loads((run / "evidence/attempt-01/query-result.json").read_bytes())[
        "queries"
    ]
    for before, after in zip(old, query["queries"], strict=True):
        if before["question_id"] != "CQ-T3-01":
            assert before == after
    assert (
        digest((run / "review-01/review.md").read_bytes())
        == "sha256:f02323dd6762629c7da9c5eea7a89aab60650a58635cd44706dacfa91bed083a"
    )
