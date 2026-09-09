"""Relation evidence owns its scope; a hypothesis cannot supply it by proximity."""

from copy import deepcopy

import pytest

from answers import answer
from review_packet import docket
from test_answers import obs, view


def scenario(roles=("source", "target")):
    source = obs("e", quantity_kind="synthetic quantity", value_lower=7)
    target = {"id": "h", "type": "Claim", "hypothesis_disposition": "PREFERRED"}
    for role, node in (("source", source), ("target", target)):
        if role in roles:
            node["subject"] = role + ":subject"
    nodes = [
        source,
        target,
        {
            "id": "source:subject",
            "type": "Material",
            "name": "sample",
            "tags": ["site A"],
        },
        {"id": "target:subject", "type": "Site", "name": "site B"},
    ]
    edge = {
        "key": "r",
        "type": "ResearchRelation",
        "source_id": "e",
        "target_id": "h",
        "relation_type": "SUPPORTS",
    }
    return view(nodes, [edge])


def relation(result):
    return next(row for row in result["rows"] if row["kind"] == "RELATION")


@pytest.mark.parametrize("roles", [(), ("source",), ("target",), ("source", "target")])
def test_each_endpoint_projects_only_its_own_explicit_subject(roles):
    reads = scenario(roles)
    original = deepcopy(reads.graph.nodes)
    result = answer(reads, "CQ-T5-01")
    row = relation(result)
    for role, record_id in (("source", "e"), ("target", "h")):
        node = reads.graph.get_node(record_id)
        assert row[role] == reads.row_without_subject(node)
        if role in roles:
            context_id = node["subject"]
            assert (
                row[role + "_subject"]
                == reads.row(reads.graph.get_node(record_id))["subject"]
            )
            assert row["witness"][role + "_subject_id"] == context_id
            assert context_id in result["witness_ids"]
        else:
            assert role + "_subject" not in row
            assert role + "_subject_id" not in row["witness"]
    assert result["paths"] == [["e", "r", "h"]]
    assert reads.graph.nodes == original


def test_relation_subject_expansion_is_one_hop_not_recursive_or_cross_endpoint():
    reads = scenario()
    subject = next(n for n in reads.graph.nodes if n["id"] == "source:subject")
    subject["subject"] = "not-fetched"
    reads.types["Material"]["slots"].append({"name": "subject"})
    row = relation(answer(reads, "CQ-T5-01"))
    assert row["source_subject"] == {
        "name": "sample",
        "tags": ["site A"],
        "subject": "not-fetched",
    }
    assert row["target_subject"] == {"name": "site B"}
    assert row["source"]["value_lower"] == 7
    assert "not-fetched" not in row["witness"].values()


def test_missing_evidence_subject_fails_loud_instead_of_losing_context():
    reads = scenario()
    reads.graph.nodes = [n for n in reads.graph.nodes if n["id"] != "source:subject"]
    with pytest.raises(ValueError, match="missing subject source:subject for e"):
        answer(reads, "CQ-T5-01")


def enriched_docket_input():
    # Construct the proposed envelope explicitly so docket RED is independent
    # of whether the query projection has been implemented yet.
    query = answer(scenario(()), "CQ-T5-01")
    row = relation(query)
    row["source"]["subject"] = "source:subject"
    row["source_subject"] = {"name": "sample", "tags": ["site A"]}
    row["witness"]["source_subject_id"] = "source:subject"
    query["witness_ids"] = sorted(set(query["witness_ids"]) | {"source:subject"})
    questions = {
        "questions": [
            {"id": "CQ-T5-01", "question": "synthetic", "required_semantics": ["scope"]}
        ]
    }
    trace = {"records": [{"record_id": r} for r in query["witness_ids"]]}
    return questions, {"queries": [query]}, trace


def test_docket_accepts_and_retains_traced_endpoint_scope():
    questions, result, trace = enriched_docket_input()
    record = docket(questions, result, trace)
    witness = next(w for w in record["witnesses"] if w["witness_key"] == "r")
    assert witness["projections"] == [relation(result["queries"][0])]
    assert record["traced_records_including_context"] == 4


def test_query_docket_and_review_validator_share_the_same_witness_contract():
    import review_packet
    import selective_review

    _, result, _ = enriched_docket_input()
    assert selective_review.central_key(relation(result["queries"][0])) == "r"
    assert selective_review.central_key is review_packet.central_key


@pytest.mark.parametrize(
    "fault", ["untraced", "unpaired", "wrong_endpoint", "unidentified"]
)
def test_docket_refuses_unbound_endpoint_context(fault):
    questions, result, trace = enriched_docket_input()
    row = relation(result["queries"][0])
    if fault == "untraced":
        trace["records"] = [
            r for r in trace["records"] if r["record_id"] != "source:subject"
        ]
    elif fault == "unpaired":
        del row["source_subject"]
    elif fault == "unidentified":
        del row["witness"]["source_subject_id"]
    else:
        row["source"]["subject"] = "target:subject"
    with pytest.raises(ValueError):
        docket(questions, result, trace)


def test_projection_comparison_refuses_any_change_beyond_bound_context():
    from relation_query import check_projection

    _, enriched, _ = enriched_docket_input()
    after = enriched["queries"]
    before = deepcopy(after)
    old_row = relation(before[0])
    del old_row["source_subject"]
    del old_row["witness"]["source_subject_id"]
    before[0]["witness_ids"].remove("source:subject")
    check_projection(before, after)
    for fault in ("value", "path", "identity", "missing_context", "borrowed"):
        changed = deepcopy(after)
        row = relation(changed[0])
        if fault == "value":
            row["source"]["value_lower"] = 8
        elif fault == "path":
            changed[0]["paths"] = []
        elif fault == "identity":
            row["witness"]["source_subject_id"] = "other"
        elif fault == "missing_context":
            del row["source_subject"]
        else:
            row["target_subject"] = {"name": "borrowed"}
            row["witness"]["target_subject_id"] = "source:subject"
        with pytest.raises((ValueError, KeyError)):
            check_projection(before, changed)


def test_query_only_control_and_repeat_use_frozen_bytes_without_state_writes():
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_relation_scope import check_control; check_control()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_control():
    import json
    from pathlib import Path
    from tempfile import TemporaryDirectory
    from relation_query import freeze, execute
    from review_packet import digest
    from selective_review import selective_witnesses

    run = (
        Path(__file__).resolve().parents[2]
        / "private/paper-v4-answer-demonstration/sol-argument-01"
    )

    def tree(root):
        return {
            str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob("*")
            if p.is_file()
        }

    protected = tree(run / "evidence/attempt-01")
    with TemporaryDirectory(dir=run.parent) as temporary:
        target = Path(temporary)
        freeze(run, target / "method")
        summary = execute(run, target / "method", target / "first")
        assert summary["original_queries_reproduced"]
        assert summary["projection_only"]
        assert summary["ledger_bytes_unchanged"]
        execute(run, target / "method", target / "repeat")
        assert tree(target / "first") == tree(target / "repeat")
        query = json.loads((target / "first/query-result.json").read_bytes())
        assert query["forbidden_attempts"] == {
            "file_read": 0,
            "network": 0,
            "embedding_import": 0,
        }
        result = next(q for q in query["queries"] if q["question_id"] == "CQ-T5-01")
        rows = [r for r in result["rows"] if r["kind"] == "RELATION"]
        assert rows[0]["source_subject"]["name"] == "Mid-Atlantic Ridge"
        assert rows[1]["source_subject"] == {"name": "primary melts"}
        assert "source_subject" not in rows[2]
        assert all(r["target_subject"]["tags"] == ["RC2"] for r in rows)
        review = json.loads((target / "first/review-docket.json").read_bytes())
        record = {
            "stage_identities": {
                "query_result_sha256": digest(
                    (target / "first/query-result.json").read_bytes()
                ),
                **{
                    k: query["inputs"][k]
                    for k in ("ledger_head", "replay_receipt_sha256")
                },
            },
            "question_ids": [q["question_id"] for q in query["queries"]],
            "rows_per_question": {
                q["question_id"]: len(q["rows"]) for q in query["queries"]
            },
            "witnesses_traced": review["distinct_central_witnesses"],
        }
        assert (
            len(
                selective_witnesses(
                    (target / "first/query-result.json").read_bytes(), record
                )
            )
            == 30
        )
        (target / "method/answers.py").write_bytes(b"changed query")
        with pytest.raises(ValueError):
            execute(run, target / "method", target / "drift")
        assert not (target / "drift").exists()
    assert tree(run / "evidence/attempt-01") == protected


def test_execute_cli_requires_an_explicit_method_before_reading_or_writing():
    import subprocess
    import sys
    from pathlib import Path

    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).parent / "relation_query.py"),
            "execute",
            "--run",
            "unused",
            "--output",
            "unused",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "execute requires --method" in result.stderr


def test_historical_projection_and_frozen_depth_changes_have_exact_ast_scope():
    import ast
    import json
    from pathlib import Path
    from followup import verify_materials

    here = Path(__file__).resolve().parent
    old = (
        here.parents[1]
        / "private/paper-v4-answer-demonstration/sol-argument-01/answers.py"
    )

    def except_functions(path, names):
        tree = ast.parse(path.read_bytes())
        return [
            ast.dump(node)
            for node in tree.body
            if not (isinstance(node, ast.FunctionDef) and node.name in names)
        ]

    historical = old.parent / "scope-method-01/answers.py"
    assert except_functions(historical, {"answer"}) == except_functions(old, {"answer"})
    depth_method = old.parent.parent / "sol-qualification-01/depth-method-01"
    verify_materials(
        depth_method,
        json.loads((depth_method / "method.json").read_bytes())["materials"],
    )
    assert except_functions(
        depth_method / "answers.py", {"earthquake_depth"}
    ) == except_functions(historical, {"earthquake_depth"})


def test_retained_comparison_matches_graph_context_and_preserves_old_evidence():
    import json
    from pathlib import Path
    from followup import verify_materials
    from relation_query import check_projection
    from review_packet import digest

    run = (
        Path(__file__).resolve().parents[2]
        / "private/paper-v4-answer-demonstration/sol-argument-01"
    )
    method = run / "scope-method-01"
    verify_materials(
        method, json.loads((method / "method.json").read_bytes())["materials"]
    )

    def tree(root):
        return {
            str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob("*")
            if p.is_file()
        }

    result = tree(run / "scope-query-01")
    assert len(result) == 4
    assert result == tree(run / "scope-query-reproduction-01")
    before = json.loads((run / "evidence/attempt-01/query-result.json").read_bytes())[
        "queries"
    ]
    after = json.loads(result["query-result.json"])["queries"]
    check_projection(before, after)
    assert [b["question_id"] for a, b in zip(before, after, strict=True) if a != b] == [
        "CQ-T5-01"
    ]
    exported = json.loads(
        (run / "evidence/attempt-01/export-records.json").read_bytes()
    )
    nodes = {r["id"]: r["properties"] for r in exported["entities"]}
    trace = {
        r["record_id"]
        for r in json.loads(result["query-trace-summary.json"])["records"]
    }
    for query in after:
        assert set(query["witness_ids"]) <= trace
        for row in query["rows"]:
            if row["kind"] == "RELATION":
                for role in ("source", "target"):
                    if role + "_subject" in row:
                        identity = row["witness"][role + "_subject_id"]
                        assert identity == row[role]["subject"]
                        assert row[role + "_subject"] == nodes[identity]
    assert tree(run / "evidence/attempt-01") == tree(run / "evidence/reproduction-01")
    assert (
        digest((run / "review-01/review.md").read_bytes())
        == "sha256:f2b03bf1c91520c859a47acbb0a2ec91e0783f7ea902e29b5273c2e7f50d77c7"
    )
