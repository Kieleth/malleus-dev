"""An explicit new hypothesis cannot broaden the frozen amendment boundary."""

import json
from pathlib import Path

import pytest

from repair import check_scope
from test_repair import BASE, records


def test_explicit_hypothesis_scope_preserves_existing_entity_boundary(monkeypatch):
    monkeypatch.setattr("repair.population_parts", lambda value: value)
    base = {**BASE, "entities": [{"id": "claim:new"}, {"id": "observation:one"}]}
    edge = {
        "id": "link:new",
        "type": "ResearchRelation",
        "source_id": "observation:one",
        "target_id": "claim:new",
        "properties": {"relation_type": "SUPPORTS"},
    }
    candidate = {"records": records([edge]), "supersessions": []}
    check_scope("evidence", candidate, base, hypothesis_id="claim:new")
    for replacement in (
        {"target_id": "claim:hyp-co2-degassing"},
        {"source_id": "invented"},
        {"type": "Relation"},
    ):
        bad = {**candidate, "records": records([{**edge, **replacement}])}
        with pytest.raises(ValueError):
            check_scope("evidence", bad, base, hypothesis_id="claim:new")
    with pytest.raises(ValueError):
        check_scope(
            "evidence",
            {
                **candidate,
                "supersessions": [
                    {"record_id": "link:new", "supersedes_record_id": "old"}
                ],
            },
            base,
            hypothesis_id="claim:new",
        )


def test_links_context_requires_explicit_target_and_reader():
    from repair import context

    manifest = {
        "schema": "malleus.paper-v4.links/v1",
        "hypothesis_id": "claim:new",
        "query_reader": "SubjectGraphReads",
    }
    assert context(manifest) == (
        "evidence/producer/inputs",
        "claim:new",
        "SubjectGraphReads",
    )
    for key in ("hypothesis_id", "query_reader"):
        with pytest.raises((KeyError, ValueError)):
            context({k: v for k, v in manifest.items() if k != key})
    with pytest.raises(ValueError):
        context({**manifest, "query_reader": "unknown"})


def test_links_frozen_subject_reader_reproduces_baseline():
    from repair import frozen_queries
    import malleus.compiler as api

    root = (
        Path(__file__).resolve().parents[2]
        / "private/paper-v4-answer-demonstration/sol-calibration-01/b"
    )
    if not root.exists():
        pytest.skip("declared private calibration fixture unavailable")
    replay = api.KnowledgeChangeHistory.reopen(
        root / "attempt-01/ledger/history.jsonl"
    ).replay()
    surface = json.loads(
        (root / "producer/inputs/population-surface.json").read_bytes()
    )
    queries, _, _, attempts = frozen_queries(
        root / "subject-query-01",
        replay,
        surface,
        reader="SubjectGraphReads",
        questions_path=root / "competency-questions.json",
    )
    assert (
        queries
        == json.loads((root / "subject-query-01/query-result.json").read_bytes())[
            "queries"
        ]
    )
    assert attempts == {"file_read": 0, "network": 0, "embedding_import": 0}


def test_frozen_packet_separates_producer_from_evaluation_and_preserves_inputs():
    from followup import verify_materials
    from input_delivery import input_frames
    from links import BASE as CALIBRATION, task
    from review_packet import digest

    run = CALIBRATION.parent.parent / "sol-links-01"
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    assert manifest["decision"] == "E-0255"
    assert manifest["hypothesis_id"] == "claim:co2-degassing"
    assert manifest["query_reader"] == "SubjectGraphReads"
    assert (run / "evidence/TASK.md").read_text() == task(run)
    inputs = run / "evidence/producer/inputs"
    assert not {"questions.json", "answers.py", "review.md", "before-query.json"} & {
        p.name for p in inputs.iterdir()
    }
    task_text = task(run)
    assert all(
        term not in task_text
        for term in (
            "CQ-T",
            "obs:co2-calculated",
            "observation:rc2-primary",
            "page:5:block:006",
        )
    )
    assert "No number of links" in task_text
    assert "SUPPORTS does not mean physical causation" in task_text
    assert sum(map(len, input_frames(run / "evidence", "initial").values())) == 94
    for name in ("selected-reading.json", "ontology.yaml", "population-surface.json"):
        assert (inputs / name).read_bytes() == (
            CALIBRATION / "producer/inputs" / name
        ).read_bytes()
    assert (
        digest((inputs / "baseline-records.json").read_bytes())
        == "sha256:17ed1dd187fac464b4a38a60641e4ab8cddd4705733189d5d189a4368136c95d"
    )
    assert (run / "before-query.json").read_bytes() == (
        CALIBRATION / "subject-query-01/query-result.json"
    ).read_bytes()


def test_links_review_is_scoped_and_has_no_expected_endpoints_or_grades():
    task = (Path(__file__).parent / "links-review-task.md").read_text()
    assert "Unchanged queries are not rescored" in task.replace("\n", " ")
    assert "HUMAN RATIFICATION PENDING" in task
    assert "not a complete" in task
    for forbidden in ("CQ-T5-01", "observation:rc2", "0.4", "sixteen", "five covered"):
        assert forbidden not in task


def test_links_review_refuses_a_different_condition(tmp_path, monkeypatch):
    import repair_review_packet as review

    monkeypatch.setattr(review, "ROOT", tmp_path)
    run = tmp_path / "private/run"
    run.mkdir(parents=True)
    (run / "manifest.json").write_text(json.dumps({"schema": "other", "materials": []}))
    with pytest.raises(ValueError, match="exact finding-guided condition"):
        review.prepare(run, tmp_path / "private/review", links=True)
    assert not (tmp_path / "private/review").exists()


def test_links_complete_delivery_was_observed_before_authoring():
    from input_delivery import input_frames, transcript_evidence, verify_frames
    from links import BASE as CALIBRATION

    run = CALIBRATION.parent.parent / "sol-links-01/evidence"
    order = json.loads((run / "delivery-order.json").read_bytes())
    launch = json.loads((run / "launch.json").read_bytes())
    rows = [
        json.loads(line)
        for line in Path(launch["metadata_source"]).read_text().splitlines()
    ]
    before = [
        row for row in rows if row["timestamp"] <= order["delivery_output_cutoff"]
    ]
    expected = [
        frame for group in input_frames(run, "initial").values() for frame in group
    ]
    assert len(expected) == order["verified_frames"] == order["expected_frames"] == 94
    verify_frames(expected, transcript_evidence(before, launch))
    assert order["producer_work_files_at_check"] == []
    for row in before:
        if row["type"] != "response_item":
            continue
        payload = row["payload"]
        if payload["type"] in {"function_call", "custom_tool_call"}:
            assert "apply_patch" not in json.dumps(payload)


def test_links_admission_preserves_all_old_records_history_and_query_objects():
    import malleus.compiler as api
    from links import BASE as CALIBRATION
    from repair import check_preservation, check_record_history, check_read_guard
    from repair_review_packet import check_capture
    from review_packet import digest

    run = CALIBRATION.parent.parent / "sol-links-01"
    attempt = run / "evidence/attempt-01"
    result = json.loads((attempt / "run-result.json").read_bytes())
    assert result["status"] == "ADMITTED_REPLAYED_UNREVIEWED"
    assert (
        result["submitted_sha256"]
        == "sha256:19e0b38e2bb10ffeab765c10c00a3f165a773cde6ea628ad27c0f4ab5c90d7b1"
    )
    assert (
        digest((attempt / "submitted-population.json").read_bytes())
        == result["submitted_sha256"]
    )
    assert result["graph"] == {
        "entities": 138,
        "relations": 21,
        "events": 1,
        "signals": 0,
        "event_participations": 0,
    }
    for name, identity in result["artifacts"].items():
        assert digest((attempt / name).read_bytes()) == identity
    before = api.KnowledgeChangeHistory.reopen(run / "base-history.jsonl").replay()
    after = api.KnowledgeChangeHistory.reopen(attempt / "ledger/history.jsonl").replay()
    assert before.ledger_event_count == 14 and after.ledger_event_count == 20
    candidate = json.loads((attempt / "submitted-population.json").read_bytes())
    check_scope(
        "evidence",
        candidate,
        before.graph.export_records(),
        hypothesis_id="claim:co2-degassing",
    )
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
    old = json.loads((run / "before-query.json").read_bytes())["queries"]
    result_query = json.loads((attempt / "query-result.json").read_bytes())
    check_read_guard(result_query["forbidden_attempts"])
    assert result_query["query_reader"] == "SubjectGraphReads"
    assert result_query["reader_sha256"] == digest(
        (run / "subject_answers.py").read_bytes()
    )
    assert len(old) == len(result_query["queries"]) == 30
    assert [
        b["question_id"]
        for a, b in zip(old, result_query["queries"], strict=True)
        if a != b
    ] == ["CQ-T5-01"]
    changed = next(q for q in result_query["queries"] if q["question_id"] == "CQ-T5-01")
    assert changed["paths"] == [
        [
            "observation:saturation-depth",
            "repair:evidence:relation:saturation-depth-supports-co2-degassing",
            "claim:co2-degassing",
        ]
    ]
    assert changed["rows"][1]["source"]["determination"] == "MODELLED"
    assert changed["rows"][1]["target"]["assertion_modality"] == "HYPOTHESISED"
    assert changed["rows"][1]["target"]["hypothesis_disposition"] == "PREFERRED"


def test_links_reproduction_and_independent_review_materials_are_exact():
    from followup import verify_materials
    from links import BASE as CALIBRATION
    from review_packet import digest

    run = CALIBRATION.parent.parent / "sol-links-01"

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
    assert set(manifest["cases"]) == {"evidence"}
    assert manifest["cases"]["evidence"]["changed_question_ids"] == ["CQ-T5-01"]
    assert manifest["cases"]["evidence"]["run_result_sha256"] == digest(
        original["run-result.json"]
    )
    assert all("rationale" not in entry["path"] for entry in manifest["materials"])
    assert (
        packet / "evidence/after-submitted-population.json"
    ).read_bytes() == original["submitted-population.json"]


def test_links_scoped_review_is_frozen_without_overwriting_prior_grades():
    import re
    from links import BASE as CALIBRATION
    from review_packet import digest
    from selective_review import validate

    packet = CALIBRATION.parent.parent / "sol-links-01/review-01"
    source = (packet / "review.md").read_bytes()
    assert (
        digest(source)
        == "sha256:3e3363dfdcbc8c3034df35a7f49fa66e93746fb367d64243bba23f6981277427"
    )
    text = source.decode()
    assert "HUMAN RATIFICATION PENDING" in text
    assert "not a complete validator-certified thirty-question v3 review" in text
    assert "PARTIAL before and PARTIAL after" in text
    reading = json.loads((packet / "evidence/selected-reading.json").read_bytes())
    blocks = {block["id"] for page in reading["pages"] for block in page["blocks"]}
    assert set(re.findall(r"page:\d+:block:\d+", text)) <= blocks
    assert "page:5:block:007" in text
    questions = json.loads((packet / "questions.json").read_bytes())["questions"]
    required = next(q["required_semantics"] for q in questions if q["id"] == "CQ-T5-01")
    for index, semantic in enumerate(required, start=1):
        assert f"{index}. `{semantic}`:" in text
    old_packet = CALIBRATION / "subject-review-01"
    old_review = validate(old_packet, old_packet / "review-record.md")
    old = next(q for q in old_review["questions"] if q["question_id"] == "CQ-T5-01")
    assert old["question_responsiveness"] == "PARTIAL"
    assert [
        item["semantic"] for item in old["coverage"] if item["row_index"] is not None
    ] == ["causal_mechanism"]
    report = (Path(__file__).parent / "LINKS-RESULTS.md").read_text()
    assert "two changed judgments about old text are not gains" in report
