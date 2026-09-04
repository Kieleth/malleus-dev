"""Guards for the run-02 source-grounded review inputs and record grammar."""

from __future__ import annotations

import copy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def _module(name: str):
    spec = importlib.util.spec_from_file_location(
        f"paper_v4_evaluation_v4_{name}", HERE / f"{name}.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


review = _module("review")
ReviewRefusal = review.ReviewRefusal
validate_blank_review = review.validate_blank_review
validate_review = review.validate_review
validate_review_input_manifest = review.validate_review_input_manifest

RUN_02 = ROOT / "paper-v4/experiment-v4/run-02"
PROTOCOL = HERE / "review-protocol.json"
MANIFEST = HERE / "review-input-manifest.json"
BLANK = HERE / "review-record.blank.md"
TASK = HERE / "review-task.md"
READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"
QUERY_RESULT = ROOT / "private/paper-v4-v4-run-02/query/query-result.json"

# The protocol was frozen before the producer ran and is not edited here.
PROTOCOL_DIGEST = (
    "sha256:7cee52a7d6ea5018fe8443e621c72280b05c2bb5cc1e4a2eeaa27208665ed379"
)
ROWS_PER_QUESTION = {"CQ-01": 4, "CQ-02": 32, "CQ-03": 34, "CQ-04": 3}


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def _record(source: str) -> dict[str, object]:
    start = source.index("```json\n") + len("```json\n")
    end = source.index("\n```", start)
    return json.loads(source[start:end])


def _blank() -> dict[str, object]:
    return _record(BLANK.read_text(encoding="utf-8"))


def _filled(**overrides: object) -> dict[str, object]:
    record = _blank()
    record["status"] = "PRELIMINARY_COMPLETE"
    record["inputs"]["review_input_manifest_sha256"] = _digest(MANIFEST)
    record["preliminary"]["actor_id"] = "actor:claude-preliminary-run-02"
    record["preliminary"]["completed_at"] = "2026-09-04T20:00:00Z"
    for question in record["questions"]:
        count = ROWS_PER_QUESTION[question["question_id"]]
        question["question_responsiveness"] = "PARTIAL"
        question["responsiveness_rationale"] = "placeholder for the grammar test"
        question["source_locators"] = ["page:1:block:002"]
        question["rows"] = [
            {
                "row_index": index,
                "source_support": "SUPPORTED",
                "source_locators": ["page:1:block:002"],
                "rationale": "placeholder for the grammar test",
            }
            for index in range(count)
        ]
    record.update(overrides)
    return record


def _wrap(record: dict[str, object]) -> bytes:
    body = json.dumps(record, ensure_ascii=False, indent=2)
    return f"# test record\n\n```json\n{body}\n```\n".encode("utf-8")


def _validate(record: dict[str, object], **kwargs: object) -> dict[str, object]:
    return validate_review(
        _wrap(record),
        PROTOCOL.read_bytes(),
        review_input_manifest_source=MANIFEST.read_bytes(),
        query_result_source=QUERY_RESULT.read_bytes(),
        selected_reading_source=READING.read_bytes(),
        **kwargs,
    )


def test_the_frozen_protocol_is_untouched_and_names_codex() -> None:
    protocol = json.loads(PROTOCOL.read_bytes())

    assert _digest(PROTOCOL) == PROTOCOL_DIGEST
    assert protocol["schema"] == "malleus.paper-v4.source-grounded-review-protocol/v2"
    assert protocol["status"] == "FROZEN_BEFORE_V4_PRODUCER"
    assert protocol["authorship"]["preliminary_evaluator_kind"] == "CODEX_PRELIMINARY"


def test_the_manifest_binds_the_exact_run_02_review_surface() -> None:
    manifest = validate_review_input_manifest(
        MANIFEST.read_bytes(), PROTOCOL.read_bytes()
    )
    protocol = json.loads(PROTOCOL.read_bytes())
    stage = manifest["stage_identities"]

    assert manifest["status"] == "FROZEN_FOR_REVIEW"
    assert manifest["run_id"] == "run-02"
    assert manifest["review_protocol_sha256"] == PROTOCOL_DIGEST
    assert manifest["fixed_identities"] == protocol["fixed_identities"]
    assert stage["query_binding_sha256"] == _digest(
        RUN_02 / "results/native-query-binding.json"
    )
    assert stage["query_result_sha256"] == _digest(QUERY_RESULT)
    assert stage["query_trace_summary_sha256"] == _digest(
        RUN_02 / "results/query-trace-summary.json"
    )
    assert stage["population_trace_summary_sha256"] == _digest(
        RUN_02 / "results/trace-summary.json"
    )
    assert stage["accepted_ontology_sha256"] == _digest(
        RUN_02 / "ontology-run/ontology-03.yaml"
    )
    assert manifest["rows_per_question"] == ROWS_PER_QUESTION
    assert {item["name"] for item in manifest["materials"]} == {
        "selected_reading",
        "competency_questions",
        "query_binding",
        "query_result",
        "population_trace",
    }
    for item in manifest["materials"]:
        assert _digest(ROOT / item["path"]) == item["sha256"], item["path"]


def test_the_recorded_deviation_names_the_claude_reviewer() -> None:
    manifest = json.loads(MANIFEST.read_bytes())
    authorship = manifest["authorship"]

    assert authorship["preliminary_evaluator_kind"] == "CLAUDE_PRELIMINARY"
    assert authorship["deviation"]["from"] == "CODEX_PRELIMINARY"
    assert authorship["deviation"]["to"] == "CLAUDE_PRELIMINARY"
    assert authorship["deviation"]["reason"].strip()
    assert authorship["deviation"]["protocol_edited"] is False
    assert authorship["ratifier_evaluator_kind"] == "HUMAN_AUTHOR"
    assert authorship["ratifier_actor_id"] == "actor:luis"


def test_an_undeclared_reviewer_kind_is_refused() -> None:
    manifest = json.loads(MANIFEST.read_bytes())
    del manifest["authorship"]["deviation"]

    with pytest.raises(ReviewRefusal, match="deviation"):
        validate_review_input_manifest(
            json.dumps(manifest).encode("utf-8"), PROTOCOL.read_bytes()
        )


def test_the_blank_record_validates_and_carries_no_judgment() -> None:
    record = validate_blank_review(
        BLANK.read_bytes(), PROTOCOL.read_bytes(), MANIFEST.read_bytes()
    )

    assert record["status"] == "BLANK"
    assert record["preliminary"]["evaluator_kind"] == "CLAUDE_PRELIMINARY"
    assert record["inputs"]["review_input_manifest_sha256"] == ""
    assert [question["question_id"] for question in record["questions"]] == [
        "CQ-01",
        "CQ-02",
        "CQ-03",
        "CQ-04",
    ]
    for question in record["questions"]:
        assert question["question_responsiveness"] == "PENDING"
        assert question["rows"] == []
        assert question["source_locators"] == []


def test_a_filled_record_carries_the_reviewer_kind_and_a_pending_ratification() -> None:
    review = _validate(_filled())

    assert review["status"] == "PRELIMINARY_COMPLETE"
    assert review["preliminary"]["evaluator_kind"] == "CLAUDE_PRELIMINARY"
    assert review["ratification"] == {
        "evaluator_kind": "HUMAN_AUTHOR",
        "actor_id": "actor:luis",
        "disposition": "PENDING",
        "completed_at": "",
        "notes": "",
    }
    assert [len(question["rows"]) for question in review["questions"]] == [4, 32, 34, 3]


def test_a_filled_record_is_not_paper_evidence_until_ratified() -> None:
    with pytest.raises(ReviewRefusal, match="human ratification is required"):
        _validate(_filled(), require_human_ratification=True)


def test_a_record_claiming_the_codex_kind_is_refused() -> None:
    record = _filled()
    record["preliminary"]["evaluator_kind"] = "CODEX_PRELIMINARY"

    with pytest.raises(ReviewRefusal, match="evaluator kind"):
        _validate(record)


def test_a_record_carrying_a_forbidden_field_is_refused() -> None:
    record = _filled()
    record["questions"][0]["rows"][0]["score"] = 1

    with pytest.raises(ReviewRefusal, match="forbidden field"):
        _validate(record)


def test_a_record_must_judge_every_returned_row_in_order() -> None:
    record = _filled()
    record["questions"][1]["rows"] = record["questions"][1]["rows"][:-1]

    with pytest.raises(ReviewRefusal, match="every returned row"):
        _validate(record)


def test_a_record_cannot_cite_a_block_outside_the_reading() -> None:
    record = _filled()
    record["questions"][0]["rows"][0]["source_locators"] = ["page:99:block:001"]

    with pytest.raises(ReviewRefusal, match="unknown"):
        _validate(record)


def test_a_ratified_record_needs_a_disposition_and_a_later_timestamp() -> None:
    record = _filled()
    record["status"] = "HUMAN_RATIFIED"
    record["ratification"] = copy.deepcopy(record["ratification"])
    record["ratification"]["disposition"] = "RATIFIED_AS_RECORDED"
    record["ratification"]["completed_at"] = "2026-09-04T19:00:00Z"
    record["ratification"]["notes"] = "checked every cited block"

    with pytest.raises(ReviewRefusal, match="cannot precede"):
        _validate(record)


def test_the_review_task_sends_the_reviewer_to_the_frozen_surface() -> None:
    task = " ".join(TASK.read_text(encoding="utf-8").split())

    assert "CLAUDE_PRELIMINARY" in task
    assert "review-input-manifest.json" in task
    assert "private/paper-v4-v4-run-02/query/query-result.json" in task
    assert "private/paper-v4-v4-run-02/ledger/retained-capture.json" in task
    assert "Do not calculate a score" in task
    assert "Luis" in task


def test_the_active_gate_collects_the_v4_evaluation() -> None:
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())

    assert "paper-v4/evaluation-v4" in manifest["paths"]
