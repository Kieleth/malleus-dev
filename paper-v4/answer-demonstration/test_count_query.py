"""Count retrieval keeps network membership distinct from useful subsets."""

import ast
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from answers import answer, PROGRAMS
from test_answers import obs, view
from test_subject_answers import subject_view


PRIVATE = Path(__file__).resolve().parents[2] / "private/paper-v4-answer-demonstration"


@pytest.mark.parametrize(
    "scope",
    [
        "ocean-bottom seismometers in the network",
        "OBS network total",
        "whole network of OBSs",
        "entire network of OBSs",
    ],
)
@pytest.mark.parametrize("count", [0, 11])
def test_network_count_is_reachable_without_inventing_deployment(scope, count):
    node = obs("arbitrary:q", count=count, count_scope=scope, subject="s")
    reads = subject_view([node, {"id": "s", "type": "Instrument", "name": "OBSs"}])
    protected = deepcopy(reads.graph.nodes)
    result = answer(reads, "CQ-T1-02")
    assert result["rows"] == [reads.row(node)]
    assert result["witness_ids"] == ["arbitrary:q", "s"]
    assert result["paths"] == []
    assert "deployment" not in result["rows"][0]["record"]
    assert reads.graph.nodes == protected
    assert PROGRAMS["CQ-T1-02"] is PROGRAMS["CQ-C-04"]


@pytest.mark.parametrize(
    "scope",
    [
        "useful OBSs in the network",
        "recovered OBSs in the network",
        "operational OBSs in the network",
        "subset of deployed OBSs",
        "minimum OBSs detecting an event in the network",
        "at least three deployed OBSs detecting an event",
        "OBSs in the network used for arrival detection",
        "OBSs not deployed",
        "undeployed OBSs",
        "OBS network",
    ],
)
def test_subset_threshold_negation_and_unspecified_network_do_not_supply_total(scope):
    assert (
        answer(view([obs("x", count=8, count_scope=scope)]), "CQ-T1-02")["rows"] == []
    )


@pytest.mark.parametrize("value", [True, "11", 11.0, None])
def test_count_requires_its_explicit_integer_field(value):
    assert (
        answer(view([obs("x", count=value, name="deployed OBSs")]), "CQ-T1-02")["rows"]
        == []
    )


def test_subject_words_cannot_supply_count_scope_and_unlinked_counts_are_not_borrowed():
    nodes = [
        obs("x", count=11, subject="s"),
        {"id": "s", "type": "Instrument", "name": "deployed OBSs"},
        obs("other", name="whole network of OBSs"),
    ]
    assert answer(subject_view(nodes), "CQ-T1-02")["rows"] == []
    with pytest.raises(ValueError, match="missing subject"):
        answer(
            subject_view(
                [
                    obs(
                        "x",
                        count=11,
                        count_scope="OBSs in the network",
                        subject="absent",
                    )
                ]
            ),
            "CQ-T1-02",
        )


def test_frozen_count_method_changes_only_the_count_function():
    def body(raw):
        parsed = ast.parse(raw)
        parsed.body = [
            n
            for n in parsed.body
            if not isinstance(n, ast.FunctionDef) or n.name != "instrument_count"
        ]
        return ast.dump(parsed)

    assert body((PRIVATE / "count-query-01/method/answers.py").read_bytes()) == body(
        (PRIVATE / "current-thirty-review-01/answers.py").read_bytes()
    )


def test_count_delta_guard_preserves_exact_projection_paths_and_unrelated_answers():
    from relation_query import check_count_selection

    reads = view([obs("q", count=11, name="deployed OBSs")])
    before = [answer(reads, "CQ-T1-02"), answer(reads, "CQ-T4-01")]
    check_count_selection(before, deepcopy(before), reads)
    for fault in ("unrelated", "value", "path", "witness", "missing", "duplicate"):
        after = deepcopy(before)
        if fault == "unrelated":
            after[1]["note"] = "changed"
        elif fault == "value":
            after[0]["rows"][0]["record"]["count"] = 13
        elif fault == "path":
            after[0]["paths"] = [["invented"]]
        elif fault == "witness":
            after[0]["witness_ids"] = []
        elif fault == "missing":
            after[0]["rows"] = []
            after[0]["witness_ids"] = []
        else:
            after[0]["rows"] *= 2
        with pytest.raises(ValueError):
            check_count_selection(before, after, reads)


def test_exact_count_base_and_runtime_refuse_before_method_write(tmp_path, monkeypatch):
    import relation_query

    wrong = tmp_path / "wrong"
    wrong.mkdir()
    (wrong / "manifest.json").write_text(
        json.dumps({"schema": "other", "condition": "other"})
    )
    with pytest.raises(ValueError, match="current.*condition"):
        relation_query.inputs(wrong, count=True)

    def refuse(*args):
        raise ValueError("runtime differs")

    monkeypatch.setattr(relation_query.pilot, "verify_runtime", refuse)
    output = PRIVATE / "must-not-create-count-method"
    assert not output.exists()
    with pytest.raises(ValueError, match="runtime differs"):
        relation_query.freeze(
            PRIVATE / "sol-reconciliation-feedback-01", output, count=True
        )
    assert not output.exists()


def test_historical_depth_freeze_does_not_consume_living_query_bytes():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_count_query import check_historical; check_historical()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_historical():
    import relation_query
    from tempfile import TemporaryDirectory

    run = PRIVATE / "sol-qualification-01"
    with TemporaryDirectory(dir=PRIVATE, prefix="historical-depth-test-") as tmp:
        output = Path(tmp) / "method"
        relation_query.freeze(run, output, depth=True)
        assert (output / "answers.py").read_bytes() == (
            run / "depth-method-01/answers.py"
        ).read_bytes()


def test_count_comparison_reproduces_all_queries_and_preserves_run():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_count_query import check_execution; check_execution()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_execution():
    from tempfile import TemporaryDirectory
    from relation_query import freeze, execute

    def tree(path):
        return {
            str(p.relative_to(path)): p.read_bytes()
            for p in path.rglob("*")
            if p.is_file()
        }

    run = PRIVATE / "sol-reconciliation-feedback-01"
    protected = tree(run)
    with TemporaryDirectory(dir=PRIVATE, prefix="count-query-test-") as tmp:
        root = Path(tmp)
        method = freeze(run, root / "method", count=True)
        assert method["decision"] == "E-0304"
        assert (root / "method/answers.py").read_bytes() == (
            PRIVATE / "count-query-01/method/answers.py"
        ).read_bytes()
        summary = execute(run, root / "method", root / "first")
        assert summary["changed_questions"] == ["CQ-T1-02", "CQ-C-04"]
        assert summary["count_selection_only"] and summary["ledger_bytes_unchanged"]
        assert summary["original_queries_reproduced"]
        execute(run, root / "method", root / "repeat")
        assert tree(root / "first") == tree(root / "repeat")
        result = json.loads((root / "first/query-result.json").read_bytes())
        assert not any(result["forbidden_attempts"].values())
        q = next(q for q in result["queries"] if q["question_id"] == "CQ-T1-02")
        assert q["witness_ids"] == ["count:obs-network", "instrument:obs"]
        assert q["paths"] == []
        (root / "method/answers.py").write_bytes(b"drift")
        with pytest.raises(ValueError):
            execute(run, root / "method", root / "drift")
        assert not (root / "drift").exists()
    assert tree(run) == protected
