"""Duration retrieval follows evidence-bearing instrument links, not proximity."""

import ast
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from answers import answer
from test_answers import obs, view

PRIVATE = Path(__file__).resolve().parents[2] / "private/paper-v4-answer-demonstration"


def edge(key="link", source="duration", target="instrument", predicate="OBSERVED_WITH"):
    return {
        "key": key,
        "type": "ResearchRelation",
        "source_id": source,
        "target_id": target,
        "relation_type": predicate,
    }


def example(*, value=7.5, qualification="APPROXIMATE", edges=None):
    from subject_answers import SubjectGraphReads

    duration = obs(
        "duration",
        quantity_kind="continuous seismic recording duration",
        quantity_kind_class="Time",
        value_lower=value,
        value_upper=value,
        value_qualification=qualification,
        unit="hours",
        subject="campaign",
    )
    nodes = [
        duration,
        {"id": "campaign", "type": "Campaign", "name": "synthetic expedition"},
        {"id": "instrument", "type": "Instrument", "name": "test recorder"},
    ]
    raw = view(nodes, [edge()] if edges is None else edges)
    for item in raw.types.values():
        if item["family"] == "RELATION":
            item["slots"][0]["enum_values"] = [
                "OBSERVED_WITH",
                "PART_OF_CAMPAIGN",
                "SUPPORTS",
            ]
    reads = SubjectGraphReads(raw.graph, {"record_types": list(raw.types.values())})
    return reads, duration


@pytest.mark.parametrize("value,qualification", [(0, "EXACT"), (7.5, "APPROXIMATE")])
def test_duration_adds_only_its_direct_instrument_and_preserves_all_fields(
    value, qualification
):
    reads, duration = example(value=value, qualification=qualification)
    protected = deepcopy((reads.graph.nodes, reads.graph.edges))
    result = answer(reads, "CQ-T1-05")
    assert result["rows"][0] == reads.row(duration)
    assert result["paths"] == [["duration", "link", "instrument"]]
    assert result["witness_ids"] == ["campaign", "duration", "instrument", "link"]
    relation = result["rows"][1]
    assert relation["source"] == result["rows"][0]["record"]
    assert relation["source_subject"] == result["rows"][0]["subject"]
    assert relation["target"] == {"name": "test recorder"}
    assert relation["relation"] == {"relation_type": "OBSERVED_WITH"}
    assert protected == (reads.graph.nodes, reads.graph.edges)


@pytest.mark.parametrize(
    "edges",
    [
        [],
        [edge(source="instrument", target="duration")],
        [edge(target="campaign")],
        [edge(source="campaign")],
        [edge(predicate="SUPPORTS")],
    ],
)
def test_missing_reverse_wrong_type_and_campaign_links_do_not_supply_instrument(edges):
    reads, duration = example(edges=edges)
    result = answer(reads, "CQ-T1-05")
    assert result["rows"] == [reads.row(duration)]
    assert result["paths"] == []
    assert "instrument" not in result["witness_ids"]


def test_no_duration_is_invented_from_an_instrument_or_neighbour():
    reads, duration = example()
    for node in reads.graph.nodes:
        if node["id"] == duration["id"]:
            del node["value_lower"], node["value_upper"]
    result = answer(reads, "CQ-T1-05")
    assert result["rows"] == result["paths"] == []


def test_missing_selected_endpoint_fails_loudly():
    reads, _ = example(edges=[edge(target="missing")])
    with pytest.raises(ValueError, match="missing.*endpoint"):
        answer(reads, "CQ-T1-05")


def test_each_duration_keeps_its_own_instrument():
    reads, duration = example()
    reads.graph.nodes.extend(
        [
            {**duration, "id": "second", "value_lower": 12.0, "value_upper": 12.0},
            {"id": "second-instrument", "type": "Instrument", "name": "other recorder"},
        ]
    )
    reads.graph.edges.append(edge("second-link", "second", "second-instrument"))
    result = answer(reads, "CQ-T1-05")
    assert result["paths"] == [
        ["duration", "link", "instrument"],
        ["second", "second-link", "second-instrument"],
    ]
    linked = {
        row["witness"]["source_id"]: row
        for row in result["rows"]
        if row["kind"] == "RELATION"
    }
    assert linked["duration"]["target"]["name"] == "test recorder"
    assert linked["second"]["target"]["name"] == "other recorder"


def test_missing_relation_vocabulary_is_explicitly_inexpressible():
    reads, _ = example()
    reads.types["ResearchRelation"]["slots"][0]["enum_values"] = ["SUPPORTS"]
    result = answer(reads, "CQ-T1-05")
    assert result["outcome"] == "NOT_EXPRESSIBLE"
    assert "OBSERVED_WITH" in result["note"]


def test_only_duration_function_changes_from_frozen_count_program():
    def body(raw):
        tree = ast.parse(raw)
        tree.body = [
            n
            for n in tree.body
            if not isinstance(n, ast.FunctionDef) or n.name != "recording_duration"
        ]
        return ast.dump(tree)

    assert body((Path(__file__).parent / "answers.py").read_bytes()) == body(
        (PRIVATE / "count-query-01/method/answers.py").read_bytes()
    )


@pytest.mark.parametrize(
    "fault",
    [
        "unrelated",
        "duration",
        "qualifier",
        "instrument",
        "direction",
        "missing",
        "duplicate",
        "path",
        "witness",
    ],
)
def test_duration_delta_guard_checks_exact_rows_links_and_unchanged_answers(fault):
    from relation_query import check_duration_links

    before_reads, _ = example(edges=[])
    reads, _ = example()
    old = [answer(before_reads, "CQ-T1-05"), answer(before_reads, "CQ-T1-02")]
    new = [answer(reads, "CQ-T1-05"), answer(reads, "CQ-T1-02")]
    check_duration_links(old, new, reads)
    mutated = deepcopy(new)
    result = mutated[0]
    if fault == "unrelated":
        mutated[1]["note"] = "changed"
    elif fault == "duration":
        result["rows"][0]["record"]["value_lower"] = 888
    elif fault == "qualifier":
        del result["rows"][1]["source"]["value_qualification"]
    elif fault == "instrument":
        result["rows"][1]["target"]["name"] = "borrowed recorder"
    elif fault == "direction":
        result["rows"][1]["witness"]["source_id"] = "instrument"
    elif fault == "missing":
        result["rows"].pop()
    elif fault == "duplicate":
        result["rows"].append(deepcopy(result["rows"][1]))
    elif fault == "path":
        result["paths"] = [["invented"]]
    elif fault == "witness":
        result["witness_ids"] = []
    with pytest.raises(ValueError):
        check_duration_links(old, mutated, reads)


def test_duration_runner_rejects_wrong_condition_and_runtime_before_writes(
    tmp_path, monkeypatch
):
    import relation_query

    wrong = tmp_path / "wrong"
    wrong.mkdir()
    (wrong / "manifest.json").write_text(
        json.dumps({"schema": "other", "condition": "other"})
    )
    with pytest.raises(ValueError, match="duration.*condition"):
        relation_query.inputs(wrong, duration=True)

    def refuse(*args):
        raise ValueError("runtime differs")

    monkeypatch.setattr(relation_query.pilot, "verify_runtime", refuse)
    target = PRIVATE / "must-not-create-duration-method"
    assert not target.exists()
    with pytest.raises(ValueError, match="runtime differs"):
        relation_query.freeze(PRIVATE / "sol-acquisition-01", target, duration=True)
    assert not target.exists()


def test_duration_comparison_reproduces_and_preserves_the_accepted_run():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_duration_query import check_execution; check_execution()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_execution():
    from tempfile import TemporaryDirectory
    from relation_query import freeze, execute

    run = PRIVATE / "sol-acquisition-01"

    def tree(path):
        return {
            str(p.relative_to(path)): p.read_bytes()
            for p in path.rglob("*")
            if p.is_file()
        }

    protected = tree(run)
    with TemporaryDirectory(dir=PRIVATE, prefix="duration-query-test-") as directory:
        root = Path(directory)
        freeze(run, root / "method", duration=True)
        summary = execute(run, root / "method", root / "first")
        assert summary["changed_questions"] == ["CQ-T1-05"]
        assert summary["duration_links_only"] and summary["ledger_bytes_unchanged"]
        assert summary["original_queries_reproduced"]
        execute(run, root / "method", root / "repeat")
        assert tree(root / "first") == tree(root / "repeat")
        (root / "method/answers.py").write_bytes(b"drift")
        with pytest.raises(ValueError):
            execute(run, root / "method", root / "drift")
        assert not (root / "drift").exists()
    assert tree(run) == protected
