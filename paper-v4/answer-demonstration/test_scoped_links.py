"""A links successor uses current state, complete evidence and a fixed reader."""

import json
from pathlib import Path
import subprocess
import sys

import pytest


def test_scoped_successor_has_a_fresh_closed_artifact_namespace():
    from repair import artifact_ids

    manifest = {
        "schema": "malleus.paper-v4.argument/v1",
        "amendment_id": "argument-scope-01",
    }
    current = artifact_ids(manifest, "evidence")
    assert current == (
        "actor:codex:argument-scope-01:evidence",
        "capture:paper-v4:argument-scope-01:evidence",
        "plan:paper-v4:argument-scope-01:evidence",
    )
    prior = artifact_ids({**manifest, "amendment_id": "argument-01"}, "evidence")
    assert not set(current) & set(prior)
    for name in ("repair-01", "argument-scope-02", "", "../argument-scope-01"):
        with pytest.raises(ValueError):
            artifact_ids({**manifest, "amendment_id": name}, "evidence")


@pytest.mark.parametrize("existing_duplicate", [False, True])
def test_evidence_refuses_duplicate_payload_even_with_fresh_ids(
    monkeypatch, existing_duplicate
):
    from repair import FAMILIES, check_scope

    monkeypatch.setattr("repair.population_parts", lambda value: value)
    edge = {
        "id": "edge:first",
        "type": "ResearchRelation",
        "source_id": "observation:one",
        "target_id": "claim:one",
        "properties": {"relation_type": "SUPPORTS"},
    }
    base = {family: [] for family in FAMILIES}
    base["entities"] = [{"id": key} for key in ("observation:one", "claim:one")]
    records = {family: [] for family in FAMILIES}
    if existing_duplicate:
        base["relations"] = [edge]
    else:
        records["relations"] = [edge]
    records["relations"].append({**edge, "id": "edge:second"})
    candidate = {"records": records, "supersessions": []}
    with pytest.raises(ValueError, match="duplicate relation payload"):
        check_scope("evidence", candidate, base, hypothesis_id="claim:one")
    records["relations"][-1]["properties"] = {
        "relation_type": "SUPPORTS",
        "name": "distinct qualification",
    }
    check_scope("evidence", candidate, base, hypothesis_id="claim:one")


def test_scoped_stage_uses_current_history_corrected_reader_and_all_captures():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_scoped_links import check_stage; check_stage()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_stage():
    from tempfile import TemporaryDirectory
    from argument import BASE, stage, task
    from followup import verify_materials
    from input_delivery import input_frames
    from repair import preflight

    previous = BASE.parent / "sol-argument-01"
    attempt = previous / "evidence/attempt-01"
    with TemporaryDirectory(dir=BASE.parents[1], prefix="scoped-stage-test-") as tmp:
        run = Path(tmp) / "run"
        manifest = stage(run, successor=True)
        verify_materials(run, manifest["materials"])
        _, replay, queries = preflight(run)
        assert manifest["decision"] == "E-0266"
        assert manifest["amendment_id"] == "argument-scope-01"
        assert replay.ledger_event_count == 26
        assert sum(map(len, replay.graph.export_records().values())) == 162
        assert len(queries) == 30
        assert (run / "base-history.jsonl").read_bytes() == (
            attempt / "ledger/history.jsonl"
        ).read_bytes()
        assert (run / "before-query.json").read_bytes() == (
            previous / "scope-query-01/query-result.json"
        ).read_bytes()
        for name in ("answers.py", "subject_answers.py", "questions.json"):
            assert (run / name).read_bytes() == (
                previous / "scope-method-01" / name
            ).read_bytes()
        inputs = run / "evidence/producer/inputs"
        assert (inputs / "baseline-records.json").read_bytes() == (
            attempt / "export-records.json"
        ).read_bytes()
        for name in (
            "baseline-capture.json",
            "prior-amendment-capture.json",
            "argument-criteria.json",
            "competency-question.json",
        ):
            assert (inputs / name).read_bytes() == (
                previous / "evidence/producer/inputs" / name
            ).read_bytes()
        assert (inputs / "argument-capture.json").read_bytes() == (
            attempt / "retained-capture.json"
        ).read_bytes()
        text = task(run, successor=True)
        assert (run / "evidence/TASK.md").read_text() == text
        assert "argument-scope:evidence:" in text
        assert "argument-capture.json" in text
        for forbidden in ("observation:", "page:5", "RC2", "0.4", "PARTIAL"):
            assert forbidden not in text
        frames = input_frames(run / "evidence", "initial")
        assert "inputs/argument-capture.json" in frames
        assert "inputs/argument-criteria.json" in frames
        assert not {"answers.py", "review.md", "rationale.md", "before-query.json"} & {
            path.name for path in inputs.iterdir()
        }
        with pytest.raises(ValueError, match="refusing to overwrite"):
            stage(run, successor=True)


def test_frozen_successor_closes_every_before_witness_to_its_own_capture():
    from argument import BASE
    from followup import verify_materials
    from review_packet import digest, verify_trace_materials

    run = BASE.parent / "sol-argument-scope-01"
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    inputs = run / "evidence/producer/inputs"
    captures = {digest(p.read_bytes()): p for p in inputs.glob("*capture.json")}
    assert len(captures) == 3
    traces = json.loads(
        (
            BASE.parent / "sol-argument-01/scope-query-01/query-trace-summary.json"
        ).read_bytes()
    )["records"]
    query = json.loads((run / "before-query.json").read_bytes())
    assert {row["record_id"] for row in traces} == {
        key for q in query["queries"] for key in q["witness_ids"]
    }
    assert len(traces) == 53
    for trace in traces:
        selected = set(trace["evidence"].values()) & set(captures)
        assert len(selected) == 1
        verify_trace_materials(
            (inputs / "selected-reading.json").read_bytes(),
            captures[next(iter(selected))].read_bytes(),
            {"records": [trace]},
        )


def test_delivery_uses_event_metadata_and_exact_outputs_not_notification_text():
    from argument import BASE
    from input_delivery import input_frames, transcript_evidence, verify_frames

    run = BASE.parent / "sol-argument-scope-01/evidence"
    launch = json.loads((run / "launch.json").read_bytes())
    order = json.loads((run / "delivery-order.json").read_bytes())
    rows = [
        json.loads(line)
        for line in Path(launch["metadata_source"]).read_text().splitlines()
    ]
    before = [
        row for row in rows if row["timestamp"] <= order["delivery_output_cutoff"]
    ]
    boundary = before[-1]
    assert boundary["type"] == "response_item"
    assert boundary["payload"]["type"] == "function_call"
    assert boundary["payload"]["name"] == "send_message"
    expected = [
        frame for group in input_frames(run, "initial").values() for frame in group
    ]
    assert len(expected) == order["verified_frames"] == order["expected_frames"] == 98
    outputs = transcript_evidence(before, launch)
    verify_frames(expected, outputs)
    # An opaque notification is not proof that the preceding frame arrived.
    with pytest.raises(ValueError, match="incomplete model-visible delivery"):
        verify_frames(expected, outputs[:-1])
    assert order["producer_work_files_at_check"] == []


def test_admitted_successor_preserves_history_records_and_corrected_queries():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_scoped_links import check_outcome; check_outcome()",
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
        check_record_history,
        check_read_guard,
        preflight,
    )
    from review_packet import digest, docket, verify_trace_materials

    run = BASE.parent / "sol-argument-scope-01"
    attempt = run / "evidence/attempt-01"
    _, before, old = preflight(run)
    result = json.loads((attempt / "run-result.json").read_bytes())
    candidate = json.loads((attempt / "submitted-population.json").read_bytes())
    assert result["status"] == "ADMITTED_REPLAYED_UNREVIEWED"
    assert result["submitted_sha256"] == digest(
        (run / "evidence/producer/work/candidate-01.json").read_bytes()
    )
    for name, identity in result["artifacts"].items():
        assert digest((attempt / name).read_bytes()) == identity
    after = api.KnowledgeChangeHistory.reopen(attempt / "ledger/history.jsonl").replay()
    assert before.ledger_event_count == 26 and after.ledger_event_count == 32
    assert result["graph"] == {
        "entities": 138,
        "relations": 25,
        "events": 1,
        "signals": 0,
        "event_participations": 0,
    }
    check_preservation(
        before.graph.export_records(), after.graph.export_records(), candidate
    )
    check_record_history(before.record_history, after.record_history, candidate)
    assert (
        (attempt / "ledger/history.jsonl")
        .read_bytes()
        .startswith((run / "base-history.jsonl").read_bytes())
    )
    query = json.loads((attempt / "query-result.json").read_bytes())
    trace = json.loads((attempt / "query-trace-summary.json").read_bytes())
    check_read_guard(query["forbidden_attempts"])
    assert query["query_program_sha256"] == digest((run / "answers.py").read_bytes())
    new = query["queries"]
    assert len(old) == len(new) == 30
    assert [b["question_id"] for a, b in zip(old, new, strict=True) if a != b] == [
        "CQ-T5-01"
    ]
    for a, b in zip(old, new, strict=True):
        assert all(row in b["rows"] for row in a["rows"])
        assert all(path in b["paths"] for path in a["paths"])
    changed = next(q for q in new if q["question_id"] == "CQ-T5-01")
    assert len(changed["rows"]) == 6 and len(changed["paths"]) == 5
    assert len(changed["witness_ids"]) == 15
    additions = {r["id"] for r in candidate["records"]["relations"]}
    assert len(additions) == 2
    assert {p[1] for p in changed["paths"]} >= additions
    nodes = {r["id"]: r for r in after.graph.export_records()["entities"]}
    for row in changed["rows"]:
        if row["kind"] != "RELATION" or row["witness"]["relation_id"] not in additions:
            continue
        for role in ("source", "target"):
            assert row[role + "_subject"] == nodes[row[role]["subject"]]["properties"]
            assert row["witness"][role + "_subject_id"] == row[role]["subject"]
    seismic = next(
        r
        for r in changed["rows"]
        if r["witness"].get("source_id") == "observation:rc2-deep-depth"
    )
    assert "determination" not in seismic["source"]
    assert seismic["target"]["assertion_modality"] == "HYPOTHESISED"
    docket(json.loads((run / "questions.json").read_bytes()), query, trace)
    inputs = run / "evidence/producer/inputs"
    captures = {
        digest(p.read_bytes()): p
        for p in [*inputs.glob("*capture.json"), attempt / "retained-capture.json"]
    }
    assert len(captures) == 4
    for row in trace["records"]:
        selected = set(row["evidence"].values()) & set(captures)
        assert len(selected) == 1
        verify_trace_materials(
            (inputs / "selected-reading.json").read_bytes(),
            captures[next(iter(selected))].read_bytes(),
            {"records": [row]},
        )


def test_reproduction_and_review_keep_exact_bytes_and_all_four_captures():
    from argument import BASE
    from followup import verify_materials
    from review_packet import digest

    run = BASE.parent / "sol-argument-scope-01"

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
    assert manifest["cases"]["evidence"]["run_result_sha256"] == digest(
        original["run-result.json"]
    )
    assert not any("rationale" in m["path"] for m in manifest["materials"])
    for name in (
        "baseline-capture.json",
        "prior-amendment-capture.json",
        "argument-capture.json",
        "argument-criteria.json",
    ):
        assert (packet / "evidence" / name).read_bytes() == (
            run / "evidence/producer/inputs" / name
        ).read_bytes()
    assert (packet / "evidence/after-retained-capture.json").read_bytes() == original[
        "retained-capture.json"
    ]


def test_completed_review_is_closed_bound_and_assesses_every_returned_identity():
    import re
    from argument import BASE
    from review_packet import digest

    run = BASE.parent / "sol-argument-scope-01"
    packet = run / "review-01"
    manifest = json.loads((packet / "manifest.json").read_bytes())
    assert {str(p.relative_to(packet)) for p in packet.rglob("*") if p.is_file()} == {
        m["path"] for m in manifest["materials"]
    } | {"manifest.json", "review.md"}
    data = (packet / "review.md").read_bytes()
    assert (
        digest(data)
        == "sha256:357f3c96fb5f34e642ca3629b60eba4150e8b101e6b423399c710703a0cd9d9f"
    )
    text = data.decode()
    assert "HUMAN RATIFICATION PENDING" in text
    assert "not a complete validator-certified thirty-question review" in text
    query = json.loads((packet / "evidence/after-query-result.json").read_bytes())
    question = next(q for q in query["queries"] if q["question_id"] == "CQ-T5-01")
    for key in question["witness_ids"]:
        assert "`" + key + "`" in text
    criteria = json.loads((packet / "evidence/argument-criteria.json").read_bytes())
    section = text.split("## Prospective criterion comparison", 1)[1]
    offsets = [
        section.index("**" + c["semantic"] + ".**") for c in criteria["criteria"]
    ]
    assert offsets == sorted(offsets)
    reading = json.loads((packet / "evidence/selected-reading.json").read_bytes())
    blocks = {b["id"] for p in reading["pages"] for b in p["blocks"]}
    assert set(re.findall(r"page:\d+:block:\d+", text)) <= blocks
    previous = BASE.parent / "sol-argument-01/review-01"
    assert digest((previous / "review.md").read_bytes()) == (
        "sha256:f2b03bf1c91520c859a47acbb0a2ec91e0783f7ea902e29b5273c2e7f50d77c7"
    )
    assert (previous / "evidence/argument-criteria.json").read_bytes() == (
        packet / "evidence/argument-criteria.json"
    ).read_bytes()
