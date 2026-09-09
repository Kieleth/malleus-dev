"""Bounded amendments cannot silently replace the base or expand their scope."""

import pytest
import json
import re
from pathlib import Path
from dataclasses import dataclass, replace


def records(relations):
    return {
        "entities": [],
        "events": [],
        "signals": [],
        "event_participations": [],
        "relations": relations,
    }


BASE = records(
    [
        {
            "id": "old",
            "type": "FundingRelation",
            "source_id": "funder",
            "target_id": "person",
            "properties": {"relation_type": "FUNDS"},
        }
    ]
)
BASE["entities"] = [
    {"id": "funder"},
    {"id": "person"},
    {"id": "claim:hyp-co2-degassing"},
]


def test_producer_task_contains_only_its_own_operation_obligation():
    from repair import producer_task

    funding, evidence = producer_task("funding"), producer_task("evidence")
    assert "must supersede rel:erc-funds-singh" in funding
    assert "additions only" not in funding
    assert "additions only" in evidence
    assert "supersede rel:erc-funds-singh" not in evidence


def test_composition_task_explicitly_allows_only_the_frozen_question():
    from repair import producer_task

    question = {
        "id": "CQ-T5-01",
        "question": "Connect the source evidence?",
        "required_semantics": ["causal_mechanism", "evidence_relation"],
    }
    task = producer_task("evidence", composition_question=question)
    assert question["question"] in task
    assert all(item in task for item in question["required_semantics"])
    assert "task-directed" in task
    assert "No questions" not in task
    assert "no expected answer values" in task
    assert "especially page:5:block:006" not in task
    assert "additions only" in task
    assert "supersede rel:erc-funds-singh" not in task
    assert "No questions" in producer_task("evidence")


def test_composition_task_refuses_missing_requirements_or_wrong_case():
    from repair import producer_task

    question = {"id": "CQ-T5-01", "question": "Question?"}
    with pytest.raises((KeyError, ValueError)):
        producer_task("evidence", composition_question=question)
    with pytest.raises(ValueError):
        producer_task("funding", composition_question=question)


def test_composition_packet_freezes_original_base_and_only_one_visible_question():
    from followup import verify_materials
    from repair import producer_task
    from review_packet import digest

    root = Path(__file__).resolve().parents[2]
    run = root / "private/paper-v4-answer-demonstration/composition-01"
    if not run.exists():
        pytest.skip("declared private composition fixture unavailable")
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    assert manifest["condition"] == "TASK_DIRECTED_COMPOSITION"
    assert manifest["base_run"] == "run-21"
    assert not (run / "funding").exists()
    old = root / "private/paper-v4-answer-demonstration/repair-02"
    for name in (
        "base-history.jsonl",
        "before-query.json",
        "answers.py",
        "questions.json",
    ):
        assert (run / name).read_bytes() == (old / name).read_bytes()
    inputs = run / "evidence/inputs"
    visible = json.loads((inputs / "competency-question.json").read_bytes())
    questions = json.loads((run / "questions.json").read_bytes())["questions"]
    assert visible == next(q for q in questions if q["id"] == "CQ-T5-01")
    assert (inputs / "TASK.md").read_text() == producer_task(
        "evidence", composition_question=visible
    )
    assert not {"answers.py", "questions.json", "before-query.json", "review.md"} & {
        p.name for p in inputs.iterdir()
    }
    result = json.loads(
        (root / "paper-v4/experiment-v4/run-21/results/run-result.json").read_bytes()
    )
    assert manifest["base_receipt_sha256"] == result["replay_receipt_sha256"]
    assert (
        digest((inputs / "baseline-records.json").read_bytes())
        == result["export_records_sha256"]
    )


def test_composition_review_task_assesses_all_changes_without_expected_answers():
    task = (Path(__file__).with_name("composition-review-task.md")).read_text()
    assert "every changed question" in task
    assert "every property and both endpoints" in task
    assert "HUMAN RATIFICATION PENDING" in task
    assert "PARTIAL witness contributes no" in task
    assert "Producer rationales are excluded" in task


def test_guard_checks_counts_not_mapping_truthiness_and_requires_closure():
    from repair import check_read_guard

    check_read_guard({"file_read": 0, "network": 0, "embedding_import": 0})
    for invalid in (
        {"file_read": 1, "network": 0, "embedding_import": 0},
        {},
        {"file_read": False, "network": 0, "embedding_import": 0},
    ):
        with pytest.raises(ValueError):
            check_read_guard(invalid)


def test_capture_binding_comes_from_exact_plan_evidence_not_output_inventory():
    from repair_review_packet import check_capture
    from review_packet import canonical, digest

    plan = canonical(
        {"evidence": [{"evidence_id": "capture", "sha256": digest(b"capture bytes")}]}
    )
    check_capture(plan, b"capture bytes")
    for wrong in (b"changed", b""):
        with pytest.raises(ValueError, match="capture"):
            check_capture(plan, wrong)
    with pytest.raises(ValueError):
        check_capture(canonical({"evidence": []}), b"capture bytes")


def test_executor_source_must_match_loaded_bytes_before_and_after_execution(tmp_path):
    from repair import executor_source

    path = tmp_path / "runner.py"
    path.write_bytes(b"loaded")
    assert executor_source(path, b"loaded") == b"loaded"
    path.write_bytes(b"reformatted")
    with pytest.raises(ValueError, match="executor"):
        executor_source(path, b"loaded")


def test_retirement_changes_only_supersession_and_valid_to():
    from repair import check_record_history

    @dataclass(frozen=True)
    class History:
        payload: str
        valid_from: str
        valid_to: object
        superseded_by: object

    old = History("prior", "capture-1", None, None)
    new = History("replacement", "capture-2", None, None)
    candidate = {
        "records": records([{"id": "new"}]),
        "supersessions": [{"record_id": "new", "supersedes_record_id": "old"}],
    }
    after = {"old": replace(old, valid_to="capture-2", superseded_by="new"), "new": new}
    check_record_history({"old": old}, after, candidate)
    for broken in (
        replace(after["old"], payload="corrupted"),
        replace(after["old"], valid_to="wrong-time"),
    ):
        with pytest.raises(ValueError, match="history"):
            check_record_history({"old": old}, {**after, "old": broken}, candidate)


def test_funding_scope_requires_exact_replacement_and_preserved_endpoints():
    from repair import check_scope

    relation = {**BASE["relations"][0], "id": "new"}
    candidate = {
        "capture": {},
        "records": records([relation]),
        "supersessions": [{"record_id": "new", "supersedes_record_id": "old"}],
    }
    check_scope("funding", candidate, BASE, funding_id="old")
    for altered in (
        {**candidate, "supersessions": []},
        {**candidate, "records": records([{**relation, "target_id": "funder"}])},
        {**candidate, "records": records([relation, {**relation, "id": "another"}])},
    ):
        with pytest.raises(ValueError):
            check_scope("funding", altered, BASE, funding_id="old")


def test_support_scope_requires_existing_endpoints_and_no_other_family_changes():
    from repair import check_scope

    edge = {
        "id": "new",
        "type": "ResearchRelation",
        "source_id": "person",
        "target_id": "claim:hyp-co2-degassing",
        "properties": {"relation_type": "SUPPORTS"},
    }
    candidate = {"capture": {}, "records": records([edge]), "supersessions": []}
    check_scope("evidence", candidate, BASE)
    for bad in (
        {**edge, "source_id": "invented"},
        {**edge, "id": "old"},
        {**edge, "type": "FundingRelation"},
    ):
        with pytest.raises(ValueError):
            check_scope("evidence", {**candidate, "records": records([bad])}, BASE)
    candidate["records"]["entities"] = [{"id": "invented"}]
    with pytest.raises(ValueError):
        check_scope("evidence", candidate, BASE)


def test_preservation_checks_exact_untouched_records_and_change_closure():
    from repair import check_preservation

    candidate = {
        "records": records([{**BASE["relations"][0], "id": "new"}]),
        "supersessions": [{"record_id": "new", "supersedes_record_id": "old"}],
    }
    after = {**BASE, "relations": candidate["records"]["relations"]}
    check_preservation(BASE, after, candidate)
    with pytest.raises(ValueError, match="preservation"):
        check_preservation(
            BASE, {**after, "entities": BASE["entities"][:-1]}, candidate
        )


def test_history_copy_refuses_overwrite_or_incorrect_base(tmp_path):
    from repair import copy_history
    from review_packet import digest

    source, target = tmp_path / "base", tmp_path / "case/history"
    source.write_bytes(b"base\n")
    with pytest.raises(ValueError, match="identity"):
        copy_history(source, target, digest(b"different"))
    assert not target.exists()
    copy_history(source, target, digest(b"base\n"))
    with pytest.raises(ValueError, match="overwrite"):
        copy_history(source, target, digest(b"base\n"))
    assert source.read_bytes() == b"base\n"


@pytest.mark.parametrize(
    "run,case,question",
    [
        ("repair-02", "funding", "CQ-T2-05"),
        ("repair-02", "evidence", "CQ-T5-01"),
        ("composition-01", "evidence", "CQ-T5-01"),
    ],
)
def test_retained_repair_outputs_bind_exact_delta_and_unchanged_queries(
    run, case, question
):
    from followup import verify_materials
    from repair import check_preservation, check_scope
    from repair_review_packet import check_capture
    from review_packet import digest

    root = (
        Path(__file__).resolve().parents[2]
        / "private/paper-v4-answer-demonstration"
        / run
    )
    if not root.exists():
        pytest.skip("declared private repair fixture unavailable")
    manifest = json.loads((root / "manifest.json").read_bytes())
    verify_materials(root, manifest["materials"])
    attempt = root / case / "attempt-01"
    result = json.loads((attempt / "run-result.json").read_bytes())
    assert result["status"] == "ADMITTED_REPLAYED_UNREVIEWED"
    for name, identity in result["artifacts"].items():
        assert digest((attempt / name).read_bytes()) == identity
    submitted = (attempt / "submitted-population.json").read_bytes()
    assert digest(submitted) == result["submitted_sha256"]
    candidate = json.loads(submitted)
    base = json.loads((root / case / "inputs/baseline-records.json").read_bytes())
    after = json.loads((attempt / "export-records.json").read_bytes())
    check_scope(case, candidate, base)
    check_preservation(base, after, candidate)
    check_capture(
        (attempt / "population-plan.json").read_bytes(),
        (attempt / "retained-capture.json").read_bytes(),
    )
    assert (
        (attempt / "ledger/history.jsonl")
        .read_bytes()
        .startswith((root / "base-history.jsonl").read_bytes())
    )
    before_queries = json.loads((root / "before-query.json").read_bytes())["queries"]
    after_queries = json.loads((attempt / "query-result.json").read_bytes())["queries"]
    changed = [
        a["question_id"]
        for b, a in zip(before_queries, after_queries, strict=True)
        if b != a
    ]
    assert len(before_queries) == len(after_queries) == 30
    assert changed == result["changed_question_ids"] == [question]
    reproduced = root / case / "reproduction-01"
    reproduction = json.loads((reproduced / "run-result.json").read_bytes())
    assert reproduction["status"] == result["status"]
    assert reproduction["artifacts"] == result["artifacts"]
    assert (
        digest((reproduced / "executor.py").read_bytes())
        == reproduction["runner_sha256"]
    )
    assert (reproduced / "ledger/history.jsonl").read_bytes() == (
        attempt / "ledger/history.jsonl"
    ).read_bytes()
    for name in result["artifacts"]:
        assert (reproduced / name).read_bytes() == (attempt / name).read_bytes()


def test_composition_review_packet_binds_actual_output_and_excludes_rationale():
    from followup import verify_materials
    from review_packet import digest

    run = (
        Path(__file__).resolve().parents[2]
        / "private/paper-v4-answer-demonstration/composition-01"
    )
    packet = run / "review-01"
    if not packet.exists():
        pytest.skip("declared private composition review unavailable")
    manifest = json.loads((packet / "manifest.json").read_bytes())
    verify_materials(packet, manifest["materials"])
    assert manifest["ratification"] == "PENDING"
    assert manifest["attempt"] == "attempt-01"
    assert set(manifest["cases"]) == {"evidence"}
    materials = {m["path"] for m in manifest["materials"]}
    assert not any("rationale" in path or "review.md" in path for path in materials)
    assert "evidence/competency-question.json" in materials
    assert (packet / "before-query.json").read_bytes() == (
        run / "before-query.json"
    ).read_bytes()
    attempt = run / "evidence/attempt-01"
    result_bytes = (attempt / "run-result.json").read_bytes()
    assert manifest["cases"]["evidence"]["run_result_sha256"] == digest(result_bytes)
    for name in (
        "query-result.json",
        "submitted-population.json",
        "export-records.json",
        "run-result.json",
    ):
        assert (packet / "evidence" / ("after-" + name)).read_bytes() == (
            attempt / name
        ).read_bytes()


def test_composition_review_locators_resolve_and_execution_roles_remain_distinct():
    packet = (
        Path(__file__).resolve().parents[2]
        / "private/paper-v4-answer-demonstration/composition-01/review-01"
    )
    if not packet.exists():
        pytest.skip("declared private composition review unavailable")
    text = (packet / "review.md").read_text()
    reading = json.loads((packet / "evidence/selected-reading.json").read_bytes())
    blocks = {b["id"] for p in reading["pages"] for b in p["blocks"]}
    citations = set(re.findall(r"page:\d+:block:\d+", text))
    assert citations and citations <= blocks
    assert "HUMAN RATIFICATION PENDING" in text
    assert "coordinator reports" in text
    assert "not a validator-certified v3 review record" in text
