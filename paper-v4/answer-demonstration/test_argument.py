"""A successor amendment keeps its predecessor and has explicit identities."""

import json
from pathlib import Path
import pytest


def test_successor_identity_namespace_is_explicit_and_not_the_predecessor():
    from repair import context, artifact_ids

    new = {
        "schema": "malleus.paper-v4.argument/v1",
        "hypothesis_id": "claim:co2-degassing",
        "query_reader": "SubjectGraphReads",
        "amendment_id": "argument-01",
    }
    assert context(new) == (
        "evidence/producer/inputs",
        "claim:co2-degassing",
        "SubjectGraphReads",
    )
    ids = artifact_ids(new, "evidence")
    assert ids == (
        "actor:codex:argument-01:evidence",
        "capture:paper-v4:argument-01:evidence",
        "plan:paper-v4:argument-01:evidence",
    )
    old = artifact_ids({"schema": "malleus.paper-v4.links/v1"}, "evidence")
    assert not set(ids) & set(old)
    with pytest.raises((KeyError, ValueError)):
        artifact_ids({k: v for k, v in new.items() if k != "amendment_id"}, "evidence")
    with pytest.raises(ValueError):
        artifact_ids({**new, "amendment_id": "repair-01"}, "evidence")


def test_completion_criteria_define_roles_without_answer_values_or_endpoints():
    text = (Path(__file__).parent / "argument-criteria.json").read_text()
    criteria = json.loads(text)
    assert criteria["prospective_only"] is True
    assert [c["semantic"] for c in criteria["criteria"]] == [
        "causal_mechanism",
        "supporting_observation",
        "geochemical_evidence",
        "seismic_evidence",
        "evidence_relation",
    ]
    assert "saturation depth" in text
    for forbidden in ("observation:", "25 km", "16", "0.4", "page:5"):
        assert forbidden not in text


def test_argument_packet_uses_the_current_graph_and_keeps_both_captures():
    import subprocess
    import sys

    # As in test_ontology_answers, pytest's configured living src/ must not
    # replace the experiment's pinned PYTHONPATH in a Core identity check.
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_argument import check_argument_packet; check_argument_packet()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_argument_packet():
    from argument import BASE, task
    from followup import verify_materials
    from input_delivery import input_frames
    from repair import preflight

    run = BASE.parent / "sol-argument-01"
    manifest, replay, queries = preflight(run)
    verify_materials(run, manifest["materials"])
    assert manifest["decision"] == "E-0259"
    assert manifest["condition"] == "TASK_DIRECTED_ARGUMENT_COMPLETION"
    assert replay.ledger_event_count == 20
    assert sum(map(len, replay.graph.export_records().values())) == 160
    assert len(queries) == 30
    previous = BASE / "evidence/attempt-01"
    assert (run / "base-history.jsonl").read_bytes() == (
        previous / "ledger/history.jsonl"
    ).read_bytes()
    assert (run / "before-query.json").read_bytes() == (
        previous / "query-result.json"
    ).read_bytes()
    inputs = run / "evidence/producer/inputs"
    assert (inputs / "baseline-records.json").read_bytes() == (
        previous / "export-records.json"
    ).read_bytes()
    assert (inputs / "baseline-capture.json").read_bytes() == (
        BASE / "evidence/producer/inputs/baseline-capture.json"
    ).read_bytes()
    assert (inputs / "prior-amendment-capture.json").read_bytes() == (
        previous / "retained-capture.json"
    ).read_bytes()
    assert (run / "evidence/TASK.md").read_text() == task(run)
    assert "no incoming SUPPORTS" not in task(run)
    assert "question and prospective completion requirements" in task(run)
    assert sum(map(len, input_frames(run / "evidence", "initial").values())) == 97
    question = json.loads((inputs / "competency-question.json").read_bytes())
    criteria = json.loads((inputs / "argument-criteria.json").read_bytes())
    assert question["id"] == criteria["question_id"] == "CQ-T5-01"
    assert question["required_semantics"] == [
        c["semantic"] for c in criteria["criteria"]
    ]
    assert not {"questions.json", "answers.py", "review.md", "rationale.md"} & {
        p.name for p in inputs.iterdir()
    }


def test_argument_review_route_accepts_only_its_declared_condition(
    tmp_path, monkeypatch
):
    import repair_review_packet as review

    monkeypatch.setattr(review, "ROOT", tmp_path)
    run = tmp_path / "private/run"
    run.mkdir(parents=True)
    (run / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "malleus.paper-v4.argument/v1",
                "condition": "WRONG",
                "materials": [],
            }
        )
    )
    with pytest.raises(
        ValueError, match="argument review requires its exact condition"
    ):
        review.prepare(run, tmp_path / "private/review", links=True)
    assert not (tmp_path / "private/review").exists()


def test_argument_delivery_precedes_authoring_and_includes_the_criteria():
    from argument import BASE
    from input_delivery import input_frames, transcript_evidence, verify_frames

    run = BASE.parent / "sol-argument-01/evidence"
    launch = json.loads((run / "launch.json").read_bytes())
    order = json.loads((run / "delivery-order.json").read_bytes())
    rows = [
        json.loads(line)
        for line in Path(launch["metadata_source"]).read_text().splitlines()
    ]
    before = [r for r in rows if r["timestamp"] <= order["delivery_output_cutoff"]]
    frames = input_frames(run, "initial")
    assert "inputs/competency-question.json" in frames
    assert "inputs/argument-criteria.json" in frames
    expected = [frame for group in frames.values() for frame in group]
    assert len(expected) == order["verified_frames"] == 97
    verify_frames(expected, transcript_evidence(before, launch))
    assert order["producer_work_files_at_check"] == []
    for row in before:
        if row["type"] == "response_item" and row["payload"]["type"] in {
            "function_call",
            "custom_tool_call",
        }:
            assert "apply_patch" not in json.dumps(row["payload"])


def test_argument_execution_preserves_the_accepted_successor_and_old_answers():
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_argument import check_outcome; check_outcome()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_outcome():
    import malleus.compiler as api
    from argument import BASE
    from repair import check_preservation, check_record_history, check_read_guard
    from repair_review_packet import check_capture
    from review_packet import digest

    run = BASE.parent / "sol-argument-01"
    attempt = run / "evidence/attempt-01"
    result = json.loads((attempt / "run-result.json").read_bytes())
    candidate = json.loads((attempt / "submitted-population.json").read_bytes())
    assert result["status"] == "ADMITTED_REPLAYED_UNREVIEWED"
    assert result["submitted_sha256"] == digest(
        (run / "evidence/producer/work/candidate-01.json").read_bytes()
    )
    for name, identity in result["artifacts"].items():
        assert digest((attempt / name).read_bytes()) == identity
    before = api.KnowledgeChangeHistory.reopen(run / "base-history.jsonl").replay()
    after = api.KnowledgeChangeHistory.reopen(attempt / "ledger/history.jsonl").replay()
    assert before.ledger_event_count == 20 and after.ledger_event_count == 26
    assert result["graph"] == {
        "entities": 138,
        "relations": 23,
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
    check_capture(
        (attempt / "population-plan.json").read_bytes(),
        (attempt / "retained-capture.json").read_bytes(),
    )
    trace = json.loads((attempt / "delta-trace.json").read_bytes())["records"]
    assert len(trace) == 2
    assert {r["change_set_id"] for r in trace} == {
        "change:plan:paper-v4:argument-01:evidence"
    }
    assert all(r["supersedes_record_id"] is None for r in trace)
    old = json.loads((run / "before-query.json").read_bytes())["queries"]
    query = json.loads((attempt / "query-result.json").read_bytes())
    check_read_guard(query["forbidden_attempts"])
    new = query["queries"]
    assert len(old) == len(new) == 30
    assert [b["question_id"] for a, b in zip(old, new, strict=True) if a != b] == [
        "CQ-T5-01"
    ]
    a = next(q for q in old if q["question_id"] == "CQ-T5-01")
    b = next(q for q in new if q["question_id"] == "CQ-T5-01")
    assert all(row in b["rows"] for row in a["rows"])
    assert all(path in b["paths"] for path in a["paths"])
    assert len(b["paths"]) == 3 and len(b["rows"]) == 4
    for row in b["rows"][1:]:
        assert row["target"]["assertion_modality"] == "HYPOTHESISED"
        assert row["target"]["hypothesis_disposition"] == "PREFERRED"
    assert [r["source"]["determination"] for r in b["rows"][1:]] == [
        "MEASURED",
        "DERIVED",
        "MODELLED",
    ]


def test_argument_repeat_and_review_closure_preserve_the_declared_condition():
    from argument import BASE
    from followup import verify_materials
    from review_packet import digest

    run = BASE.parent / "sol-argument-01"

    def tree(root):
        return {
            str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob("*")
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
    assert all("rationale" not in m["path"] for m in manifest["materials"])
    for name in (
        "argument-criteria.json",
        "baseline-capture.json",
        "prior-amendment-capture.json",
    ):
        assert (packet / "evidence" / name).read_bytes() == (
            run / "evidence/producer/inputs" / name
        ).read_bytes()
    assert (packet / "evidence/after-retained-capture.json").read_bytes() == original[
        "retained-capture.json"
    ]


def test_argument_review_is_bound_scoped_and_keeps_the_failed_launch():
    import re
    from argument import BASE
    from review_packet import digest

    run = BASE.parent / "sol-argument-01"
    packet = run / "review-01"
    data = (packet / "review.md").read_bytes()
    manifest = json.loads((packet / "manifest.json").read_bytes())
    assert {str(p.relative_to(packet)) for p in packet.rglob("*") if p.is_file()} == {
        m["path"] for m in manifest["materials"]
    } | {"manifest.json", "review.md"}
    assert digest(data) == (
        "sha256:f2b03bf1c91520c859a47acbb0a2ec91e0783f7ea902e29b5273c2e7f50d77c7"
    )
    text = data.decode()
    assert "PARTIAL before and PARTIAL after" in text
    assert "HUMAN RATIFICATION PENDING" in text
    assert "not a complete validator-certified thirty-question review" in text
    reading = json.loads((packet / "evidence/selected-reading.json").read_bytes())
    blocks = {b["id"] for p in reading["pages"] for b in p["blocks"]}
    assert set(re.findall(r"page:\d+:block:\d+", text)) <= blocks
    query = json.loads((packet / "evidence/after-query-result.json").read_bytes())
    changed = next(q for q in query["queries"] if q["question_id"] == "CQ-T5-01")
    assert len(changed["witness_ids"]) == 8
    for record_id in changed["witness_ids"]:
        assert f"| `{record_id}` |" in text
    criteria = json.loads((packet / "evidence/argument-criteria.json").read_bytes())
    offsets = [text.index(f"| `{c['semantic']}` |") for c in criteria["criteria"]]
    assert offsets == sorted(offsets)
    failed = json.loads((run / "review-launch-01.json").read_bytes())
    resumed = json.loads((run / "review-resume-01.json").read_bytes())
    assert failed["status"] == "FAILED_USAGE_LIMIT_NO_COMPLETED_REVIEW"
    assert failed["completed_review_at_failure"] is False
    for key in ("session_id", "model", "effort", "packet_manifest_sha256"):
        assert failed[key] == resumed[key]
    assert resumed["model_or_packet_changed"] is False


def test_frozen_argument_scope_does_not_transfer_from_hypothesis_to_evidence():
    from argument import BASE
    from subject_answers import SubjectGraphReads
    from test_answers import Graph

    run = BASE.parent / "sol-argument-01"
    exported = json.loads(
        (run / "evidence/attempt-01/export-records.json").read_bytes()
    )
    nodes = {
        r["id"]: {"id": r["id"], "type": r["type"], **r["properties"]}
        for r in exported["entities"]
    }
    surface = json.loads(
        (run / "evidence/producer/inputs/population-surface.json").read_bytes()
    )
    reads = SubjectGraphReads(Graph(list(nodes.values())), surface)
    query = json.loads((run / "evidence/attempt-01/query-result.json").read_bytes())
    changed = next(q for q in query["queries"] if q["question_id"] == "CQ-T5-01")
    for row in changed["rows"][1:3]:
        assert row["source"]["subject"] != row["target"]["subject"]
        assert row["target"]["subject"] == "segment:rc2"
    assert "tags" not in reads.row(nodes["observation:abstract-primary-co2"])["subject"]
    assert (
        reads.row(nodes["observation:abstract-deep-depth"])["subject"]["name"]
        == "Mid-Atlantic Ridge"
    )
    specific = {
        "observation:rc2-primary-ba90",
        "observation:rc2-primary-rb90",
        "observation:rc2-deep-depth",
    }
    assert not specific & set(changed["witness_ids"])
    for record_id in specific:
        node = nodes[record_id]
        expanded = reads.row(node)
        assert expanded["subject"]["tags"] in (["segment RC2"], ["RC2"])
        flat = reads.row_without_subject(node)
        assert flat["subject"] == node["subject"]
        assert "tags" not in flat
