"""Versioned qualifications preserve values, dependencies and the review boundary."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest


def example():
    from repair import FAMILIES

    base = {family: [] for family in FAMILIES}
    observation = {
        "id": "observation:old",
        "type": "Observation",
        "properties": {"value_lower": 3.0, "subject": "site:one", "unit": "km"},
    }
    edge = {
        "id": "edge:old",
        "type": "ResearchRelation",
        "source_id": observation["id"],
        "target_id": "claim:one",
        "properties": {"relation_type": "SUPPORTS"},
    }
    base["entities"] = [observation, {"id": "claim:one"}, {"id": "site:one"}]
    base["relations"] = [edge]
    records = {family: [] for family in FAMILIES}
    records["entities"] = [{**deepcopy(observation), "id": "observation:new"}]
    records["entities"][0]["properties"]["description"] = "Synthetic scope qualifier"
    records["relations"] = [
        {**deepcopy(edge), "id": "edge:new", "source_id": "observation:new"}
    ]
    candidate = {
        "capture": {},
        "records": records,
        "supersessions": [
            {"record_id": "observation:new", "supersedes_record_id": "observation:old"},
            {"record_id": "edge:new", "supersedes_record_id": "edge:old"},
        ],
    }
    return base, candidate


def check(base, candidate):
    from repair import check_qualification

    check_qualification(
        candidate, base, observation_id="observation:old", relation_id="edge:old"
    )


def test_qualification_accepts_only_added_fields_and_atomic_relation_retarget():
    base, candidate = example()
    check(base, candidate)
    candidate["supersessions"].reverse()
    check(base, candidate)
    from repair import check_scope

    with pytest.raises(ValueError, match="relation deltas only"):
        check_scope("evidence", candidate, base, hypothesis_id="claim:one")


@pytest.mark.parametrize(
    "mutation",
    [
        "value",
        "subject",
        "unit",
        "remove_value",
        "type",
        "extra_field",
        "no_qualification",
        "predicate",
        "target",
        "source",
        "edge_type",
        "extra_entity",
        "extra_edge",
        "event",
        "reuse_id",
        "missing_supersession",
        "fork_supersession",
        "wrong_supersession",
        "extra_dependency",
    ],
)
def test_qualification_refuses_scope_expansion_and_dangling_dependencies(mutation):
    base, candidate = example()
    entity = candidate["records"]["entities"][0]
    edge = candidate["records"]["relations"][0]
    if mutation in {"value", "subject", "unit"}:
        entity["properties"][
            {"value": "value_lower", "subject": "subject", "unit": "unit"}[mutation]
        ] = "changed"
    elif mutation == "remove_value":
        del entity["properties"]["value_lower"]
    elif mutation == "type":
        entity["type"] = "Claim"
    elif mutation == "extra_field":
        entity["properties"]["name"] = "unauthorized"
    elif mutation == "no_qualification":
        del entity["properties"]["description"]
    elif mutation == "predicate":
        edge["properties"]["relation_type"] = "CONTRADICTS"
    elif mutation in {"target", "source", "edge_type"}:
        edge[
            {"target": "target_id", "source": "source_id", "edge_type": "type"}[
                mutation
            ]
        ] = "changed"
    elif mutation in {"extra_entity", "extra_edge", "event"}:
        candidate["records"][
            {"extra_entity": "entities", "extra_edge": "relations", "event": "events"}[
                mutation
            ]
        ].append({"id": "extra"})
    elif mutation == "reuse_id":
        entity["id"] = "observation:old"
    elif mutation == "missing_supersession":
        candidate["supersessions"].pop()
    elif mutation == "fork_supersession":
        candidate["supersessions"][1]["supersedes_record_id"] = "observation:old"
    elif mutation == "wrong_supersession":
        candidate["supersessions"][0]["record_id"] = "unbound"
    elif mutation == "extra_dependency":
        base["relations"].append({**base["relations"][0], "id": "another"})
    with pytest.raises((ValueError, KeyError)):
        check(base, candidate)


def test_qualification_stage_pins_current_state_all_captures_and_prospective_rule():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_qualification import check_stage; check_stage()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_qualification_review_refuses_a_different_condition(tmp_path, monkeypatch):
    import repair_review_packet as review

    monkeypatch.setattr(review, "ROOT", tmp_path)
    run = tmp_path / "private/run"
    run.mkdir(parents=True)
    (run / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "malleus.paper-v4.qualification/v1",
                "condition": "WRONG",
                "materials": [],
            }
        )
    )
    with pytest.raises(
        ValueError, match="qualification review requires its exact condition"
    ):
        review.prepare(run, tmp_path / "private/review", links=True)
    assert not (tmp_path / "private/review").exists()


def test_frozen_qualification_keeps_prior_rules_and_every_before_trace():
    from argument import BASE
    from followup import verify_materials
    from review_packet import digest, verify_trace_materials

    run = BASE.parent / "sol-qualification-01"
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    inputs = run / "evidence/producer/inputs"
    previous = BASE.parent / "sol-argument-scope-01"
    old_criteria = previous / "evidence/producer/inputs/argument-criteria.json"
    assert digest(old_criteria.read_bytes()) == (
        "sha256:d90aa751744c18b022e9d6a147275abc9c21be482d81b1dc8d3fab53d69a35ef"
    )
    assert (inputs / "argument-criteria.json").read_bytes() == (
        Path(__file__).parent / "qualification-criteria.json"
    ).read_bytes()
    assert (run / "qualification-review-task.md").read_bytes() == (
        Path(__file__).parent / "qualification-review-task.md"
    ).read_bytes()
    captures = {digest(p.read_bytes()): p for p in inputs.glob("*capture.json")}
    assert len(captures) == 4
    traces = json.loads(
        (previous / "evidence/attempt-01/query-trace-summary.json").read_bytes()
    )["records"]
    queries = json.loads((run / "before-query.json").read_bytes())["queries"]
    assert {t["record_id"] for t in traces} == {
        key for q in queries for key in q["witness_ids"]
    }
    assert len(traces) == 56
    for trace in traces:
        selected = set(trace["evidence"].values()) & set(captures)
        assert len(selected) == 1
        verify_trace_materials(
            (inputs / "selected-reading.json").read_bytes(),
            captures[next(iter(selected))].read_bytes(),
            {"records": [trace]},
        )


def test_qualification_delivery_precedes_authoring_with_exact_frame_count():
    from argument import BASE
    from input_delivery import input_frames, transcript_evidence, verify_frames

    run = BASE.parent / "sol-qualification-01/evidence"
    launch = json.loads((run / "launch.json").read_bytes())
    order = json.loads((run / "delivery-order.json").read_bytes())
    rows = [
        json.loads(line)
        for line in Path(launch["metadata_source"]).read_text().splitlines()
    ]
    before = [
        row for row in rows if row["timestamp"] <= order["delivery_output_cutoff"]
    ]
    assert before[-1]["payload"]["name"] == "send_message"
    expected = [
        frame for group in input_frames(run, "initial").values() for frame in group
    ]
    assert len(expected) == order["verified_frames"] == order["expected_frames"] == 99
    outputs = transcript_evidence(before, launch)
    verify_frames(expected, outputs)
    with pytest.raises(ValueError, match="incomplete model-visible delivery"):
        verify_frames(expected, outputs[:-1])
    assert order["producer_work_files_at_check"] == []


def test_qualified_replacements_replay_preserve_and_project_exactly():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_qualification import check_outcome; check_outcome()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_outcome():
    import malleus.compiler as api
    from argument import BASE
    from repair import (
        check_preservation,
        check_qualification,
        check_record_history,
        check_read_guard,
        preflight,
    )
    from review_packet import canonical, digest, docket, verify_trace_materials

    run = BASE.parent / "sol-qualification-01"
    attempt = run / "evidence/attempt-01"
    manifest, before, old_queries = preflight(run)
    candidate = json.loads((attempt / "submitted-population.json").read_bytes())
    result = json.loads((attempt / "run-result.json").read_bytes())
    assert result["status"] == "ADMITTED_REPLAYED_UNREVIEWED"
    assert result["submitted_sha256"] == digest(
        (run / "evidence/producer/work/candidate-01.json").read_bytes()
    )
    for name, identity in result["artifacts"].items():
        assert digest((attempt / name).read_bytes()) == identity
    after = api.KnowledgeChangeHistory.reopen(attempt / "ledger/history.jsonl").replay()
    old, new = before.graph.export_records(), after.graph.export_records()
    check_qualification(
        candidate,
        old,
        observation_id=manifest["observation_id"],
        relation_id=manifest["relation_id"],
    )
    check_preservation(old, new, candidate)
    check_record_history(before.record_history, after.record_history, candidate)
    assert len(before.record_history) == 164 and len(after.record_history) == 166
    assert before.ledger_event_count == 32 and after.ledger_event_count == 39
    assert (
        {k: len(v) for k, v in old.items()}
        == {k: len(v) for k, v in new.items()}
        == result["graph"]
    )
    assert (
        (attempt / "ledger/history.jsonl")
        .read_bytes()
        .startswith((run / "base-history.jsonl").read_bytes())
    )
    query = json.loads((attempt / "query-result.json").read_bytes())
    trace = json.loads((attempt / "query-trace-summary.json").read_bytes())
    check_read_guard(query["forbidden_attempts"])
    assert [
        b["question_id"]
        for a, b in zip(old_queries, query["queries"], strict=True)
        if a != b
    ] == ["CQ-T5-01"]
    current = next(q for q in query["queries"] if q["question_id"] == "CQ-T5-01")
    prior = next(q for q in old_queries if q["question_id"] == "CQ-T5-01")
    observation, edge = (
        candidate["records"]["entities"][0],
        candidate["records"]["relations"][0],
    )
    row = next(
        r for r in current["rows"] if r["witness"].get("relation_id") == edge["id"]
    )
    old_row = next(
        r
        for r in prior["rows"]
        if r["witness"].get("relation_id") == manifest["relation_id"]
    )
    assert row["source"] == observation["properties"]
    assert row["target"] == old_row["target"]
    assert row["source_subject"] == old_row["source_subject"]
    assert len(current["rows"]) == len(prior["rows"]) == 6
    assert len(current["paths"]) == len(prior["paths"]) == 5
    assert len(current["witness_ids"]) == len(prior["witness_ids"]) == 15
    assert [observation["id"], edge["id"], edge["target_id"]] in current["paths"]
    # Bind the observed limitation of the unchanged historical reader; this is
    # not the desired contract of a future query-only correction.
    depth = next(q for q in query["queries"] if q["question_id"] == "CQ-T3-01")
    assert observation["id"] not in depth["witness_ids"]
    assert {"count:forced-depth-subset", "observation:bdb-temperature"} <= set(
        depth["witness_ids"]
    )
    assert sorted(canonical(r) for r in current["rows"] if r != row) == sorted(
        canonical(r) for r in prior["rows"] if r != old_row
    )
    docket(json.loads((run / "questions.json").read_bytes()), query, trace)
    inputs = run / "evidence/producer/inputs"
    captures = {
        digest(p.read_bytes()): p
        for p in [*inputs.glob("*capture.json"), attempt / "retained-capture.json"]
    }
    assert len(captures) == 5
    assert len(trace["records"]) == 56
    delta = json.loads((attempt / "delta-trace.json").read_bytes())["records"]
    assert len(delta) == 4
    for item in [*trace["records"], *delta]:
        selected = set(item["evidence"].values()) & set(captures)
        assert len(selected) == 1
        verify_trace_materials(
            (inputs / "selected-reading.json").read_bytes(),
            captures[next(iter(selected))].read_bytes(),
            {"records": [item]},
        )


def test_qualification_reproduces_and_reviews_the_frozen_rule_with_five_captures():
    from argument import BASE
    from followup import verify_materials
    from review_packet import digest

    run = BASE.parent / "sol-qualification-01"

    def tree(path):
        return {
            str(p.relative_to(path)): p.read_bytes()
            for p in path.rglob("*")
            if p.is_file()
        }

    original = tree(run / "evidence/attempt-01")
    assert len(original) == 13
    assert original == tree(run / "evidence/reproduction-01")
    packet = run / "review-01"
    manifest = json.loads((packet / "manifest.json").read_bytes())
    verify_materials(packet, manifest["materials"])
    assert manifest["ratification"] == "PENDING"
    assert len(list((packet / "evidence").glob("*capture.json"))) == 5
    assert (packet / "TASK.md").read_bytes() == (
        run / "qualification-review-task.md"
    ).read_bytes()
    assert (packet / "evidence/argument-criteria.json").read_bytes() == (
        run / "evidence/producer/inputs/argument-criteria.json"
    ).read_bytes()
    assert manifest["cases"]["evidence"]["run_result_sha256"] == digest(
        original["run-result.json"]
    )
    assert not any("rationale" in m["path"] for m in manifest["materials"])


def test_completed_qualification_review_binds_both_states_without_regrading_history():
    import re
    from argument import BASE
    from review_packet import digest

    run = BASE.parent / "sol-qualification-01"
    packet = run / "review-01"
    manifest = json.loads((packet / "manifest.json").read_bytes())
    assert {str(p.relative_to(packet)) for p in packet.rglob("*") if p.is_file()} == {
        m["path"] for m in manifest["materials"]
    } | {"manifest.json", "review.md"}
    content = (packet / "review.md").read_bytes()
    assert (
        digest(content)
        == "sha256:f02323dd6762629c7da9c5eea7a89aab60650a58635cd44706dacfa91bed083a"
    )
    text = content.decode()
    assert "HUMAN RATIFICATION PENDING" in text
    assert "PARTIAL before, COVERED after" in text
    assert "not a validator-certified review of all thirty questions" in text
    identities = set()
    for name in ("before-query.json", "evidence/after-query-result.json"):
        query = json.loads((packet / name).read_bytes())
        question = next(q for q in query["queries"] if q["question_id"] == "CQ-T5-01")
        identities.update(question["witness_ids"])
    assert len(identities) == 17
    assert all(key in text for key in identities)
    reading = json.loads((packet / "evidence/selected-reading.json").read_bytes())
    locators = {block["id"] for page in reading["pages"] for block in page["blocks"]}
    assert set(re.findall(r"page:\d+:block:\d+", text)) <= locators
    assert digest(
        (BASE.parent / "sol-argument-scope-01/review-01/review.md").read_bytes()
    ) == ("sha256:357f3c96fb5f34e642ca3629b60eba4150e8b101e6b423399c710703a0cd9d9f")


def check_stage():
    from tempfile import TemporaryDirectory
    from argument import BASE, stage, task
    from followup import verify_materials
    from repair import artifact_ids, preflight

    base = BASE.parent / "sol-argument-scope-01"
    attempt = base / "evidence/attempt-01"
    with TemporaryDirectory(dir=BASE.parents[1], prefix="qualification-test-") as tmp:
        run = Path(tmp) / "run"
        manifest = stage(run, qualification=True)
        verify_materials(run, manifest["materials"])
        _, replay, queries = preflight(run)
        assert manifest["decision"] == "E-0272"
        assert manifest["condition"] == "FINDING_GUIDED_QUALIFICATION"
        assert manifest["amendment_id"] == "qualification-01"
        assert replay.ledger_event_count == 32
        assert sum(map(len, replay.graph.export_records().values())) == 164
        assert len(queries) == 30
        assert (run / "base-history.jsonl").read_bytes() == (
            attempt / "ledger/history.jsonl"
        ).read_bytes()
        assert (run / "before-query.json").read_bytes() == (
            attempt / "query-result.json"
        ).read_bytes()
        for name in ("answers.py", "subject_answers.py", "questions.json"):
            assert (run / name).read_bytes() == (base / name).read_bytes()
        inputs = run / "evidence/producer/inputs"
        assert len(list(inputs.glob("*capture.json"))) == 4
        assert (inputs / "scope-capture.json").read_bytes() == (
            attempt / "retained-capture.json"
        ).read_bytes()
        criteria = json.loads((inputs / "argument-criteria.json").read_bytes())
        assert criteria["condition"] == manifest["condition"]
        assert criteria["review_rule"] == "CLAIM_FAITHFULNESS_SEPARATE_FROM_COVERAGE"
        assert "meaning-changing" in criteria["assessment_rule"]
        assert "observation-window" in criteria["criteria"][3]["requirement"]
        assert (run / "qualification-review-task.md").is_file()
        assert (run / "evidence/TASK.md").read_text() == task(run, qualification=True)
        assert "MEASURED" not in task(run, qualification=True)
        assert (
            artifact_ids(manifest, "evidence")[1]
            == "capture:paper-v4:qualification-01:evidence"
        )
        with pytest.raises(ValueError):
            artifact_ids({**manifest, "amendment_id": "argument-scope-01"}, "evidence")
        with pytest.raises(ValueError):
            stage(Path(tmp) / "invalid", qualification=True, successor=True)
        # The shared executor must invoke the new guard before retention.
        from repair import execute, FAMILIES

        current = replay.graph.export_records()
        old = next(
            r for r in current["entities"] if r["id"] == manifest["observation_id"]
        )
        edge = next(
            r for r in current["relations"] if r["id"] == manifest["relation_id"]
        )
        records = {family: [] for family in FAMILIES}
        records["entities"] = [{**deepcopy(old), "id": "test:new"}]
        records["entities"][0]["properties"].update(
            description="Synthetic test", value_lower=-1
        )
        records["relations"] = [{**edge, "id": "test:edge", "source_id": "test:new"}]
        candidate = {
            "capture": {},
            "records": records,
            "supersessions": [
                {"record_id": "test:new", "supersedes_record_id": old["id"]},
                {"record_id": "test:edge", "supersedes_record_id": edge["id"]},
            ],
        }
        submitted = run / "evidence/producer/work/synthetic-refusal.json"
        submitted.write_text(json.dumps(candidate))
        output = run / "evidence/synthetic-refusal"
        result = execute(
            run,
            "evidence",
            submitted,
            output,
            transaction_time="2026-09-08T01:00:00+00:00",
        )
        assert result["status"] == "REFUSED_OR_CHECK_FAILED"
        assert result["phase"] == "scope"
        assert "preserve all existing values" in result["detail"]
        assert not (output / "ledger").exists()
