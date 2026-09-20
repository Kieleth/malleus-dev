"""Guards for the in-context baseline harness: schema, validator, builder.

The producer has not run, so every guard here works over a synthetic reading, a
synthetic question file and a synthetic answer file written in this module. What
is exercised against the real files is what does not need a producer: that the
frozen grammar says what the validator enforces, that the spawn message states
the isolation the run contract declares, and that the staging refuses outside
`private/`.

The builder is run end to end over the synthetic cell, and its manifest is put
through `review.py` under the real v3.2 protocol, so the package this cell will
produce is one the validator already accepts.
"""

from __future__ import annotations

import copy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re

import pytest


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EVALUATION = ROOT / "paper-v4/evaluation-v4"
PROTOCOL_V32 = EVALUATION / "review-protocol-v3.2.json"
SCHEMA_FILE = HERE / "answer-file-schema.json"
CONTRACT = HERE / "run-contract.json"
SPAWN = HERE / "spawn-message.md"


def _module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate_answers = _module(HERE / "validate_answers.py", "baseline_validate_answers")
prepare_producer = _module(HERE / "prepare_producer.py", "baseline_prepare_producer")
builder = _module(HERE / "build_review_inputs.py", "baseline_build_review_inputs")
review = _module(EVALUATION / "review.py", "baseline_review")

AnswerRefusal = validate_answers.AnswerRefusal


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8")


# --------------------------------------------------------------------------
# A synthetic cell: a reading whose blocks are short enough to quote by mistake
# --------------------------------------------------------------------------

LONG_SENTENCE = (
    "The ocean-bottom seismometer network recorded continuously for eleven "
    "months across the ridge segment and the adjacent transform fault."
)
READING = {
    "schema": "malleus.paper-v4.selected-reading/v1",
    "source_sha256": "sha256:" + "1" * 64,
    "pages": [
        {
            "page": 1,
            "blocks": [
                {"id": "page:1:block:001", "text": LONG_SENTENCE},
                {"id": "page:1:block:002", "text": "The events sit beneath the axis."},
            ],
        }
    ],
}
READING_BYTES = _json_bytes(READING)

QUESTIONS = {
    "schema": "malleus.paper-v4.competency-questions/v3",
    "status": "FROZEN_BEFORE_V3_1_CELLS",
    "visibility": "VISIBLE_TO_THE_BASELINE_PRODUCER_BY_DESIGN",
    "scope": {"answer_surface": "IN_CONTEXT_ANSWER_SET"},
    "questions": [
        {
            "id": "CQ-B1",
            "question": "How long did the network record?",
            "required_semantics": ["duration", "observing_system"],
        },
        {
            "id": "CQ-B2",
            "question": "Which carrier shipped the instruments?",
            "required_semantics": ["shipping_carrier"],
            "expected_outcome": {"kind": "NOT_IN_SOURCE"},
        },
    ],
}
QUESTIONS_BYTES = _json_bytes(QUESTIONS)
TASK_DIGEST = "sha256:" + "3" * 64


def _answers(**overrides: object) -> dict[str, object]:
    document = {
        "schema": "malleus.paper-v4.in-context-answer-set/v1",
        "condition": "IN_CONTEXT_BASELINE",
        "producer_model_id": "claude-opus-5",
        "inputs": {
            "selected_reading_sha256": _digest(READING_BYTES),
            "competency_questions_sha256": _digest(QUESTIONS_BYTES),
            "producer_task_sha256": TASK_DIGEST,
        },
        "answers": [
            {
                "question_id": "CQ-B1",
                "answer": "It ran for eleven months, using seafloor seismometers.",
                "no_answer_in_source": False,
                "claims": [
                    {
                        "claim_id": "CQ-B1:c1",
                        "statement": "Recording lasted eleven months.",
                        "blocks": ["page:1:block:001"],
                    },
                    {
                        "claim_id": "CQ-B1:c2",
                        "statement": "Seafloor seismometers made the recordings.",
                        "blocks": ["page:1:block:001"],
                    },
                ],
            },
            {
                "question_id": "CQ-B2",
                "answer": "No carrier is named anywhere in what I was given.",
                "no_answer_in_source": True,
                "claims": [],
            },
        ],
    }
    document.update(overrides)
    return document


def _validate(document: dict[str, object] | None = None) -> dict[str, object]:
    document = _answers() if document is None else document
    return validate_answers.validate_answers(
        _json_bytes(document), READING_BYTES, QUESTIONS_BYTES
    )


# --------------------------------------------------------------------------
# The frozen grammar
# --------------------------------------------------------------------------


def test_the_schema_describes_the_answer_set_the_protocol_reviews() -> None:
    grammar = json.loads(SCHEMA_FILE.read_bytes())

    assert grammar["describes"] == review.ANSWER_SET_SCHEMA
    assert grammar["condition"] == "IN_CONTEXT_BASELINE"
    assert grammar["verbatim_rule"]["window"] == 60
    assert grammar["verbatim_rule"]["normalization"] == "WHITESPACE_COLLAPSED"
    assert grammar["validator"]["path"] == (
        "paper-v4/experiment-v4/baseline-01/validate_answers.py"
    )


def test_the_grammar_and_the_validator_name_the_same_keys() -> None:
    """The validator restates no key set; it reads the frozen one."""

    grammar = validate_answers.schema()
    document = _answers()

    assert sorted(document) == sorted(grammar["root_keys"])
    assert sorted(document["inputs"]) == sorted(grammar["inputs_keys"])
    assert sorted(document["answers"][0]) == sorted(grammar["answer_keys"])
    assert sorted(document["answers"][0]["claims"][0]) == sorted(grammar["claim_keys"])


def test_the_schemas_example_runs_through_the_validator() -> None:
    """The example is executed, not asserted: only its digests are placeholders."""

    example = {
        key: value
        for key, value in json.loads(SCHEMA_FILE.read_bytes())["example"].items()
        if key != "example_note"
    }
    reading = _json_bytes(
        {
            "schema": "malleus.paper-v4.selected-reading/v1",
            "source_sha256": "sha256:" + "5" * 64,
            "pages": [
                {
                    "page": 1,
                    "blocks": [
                        {
                            "id": "page:1:block:001",
                            "text": "Two instruments went in during the campaign.",
                        }
                    ],
                }
            ],
        }
    )
    questions = _json_bytes(
        {
            "schema": "malleus.paper-v4.competency-questions/v3",
            "status": "FROZEN_BEFORE_V3_1_CELLS",
            "questions": [
                {
                    "id": "CQ-EXAMPLE-01",
                    "question": "How many instruments were deployed, and by whom?",
                    "required_semantics": ["instrument_count", "campaign_name"],
                },
                {
                    "id": "CQ-EXAMPLE-02",
                    "question": "Which carrier shipped them?",
                    "required_semantics": ["shipping_carrier"],
                },
            ],
        }
    )
    example["inputs"]["selected_reading_sha256"] = _digest(reading)
    example["inputs"]["competency_questions_sha256"] = _digest(questions)

    report = validate_answers.validate_answers(
        _json_bytes(example), reading, questions
    )

    assert report["status"] == "ACCEPTED"
    assert report["questions"] == 2
    assert report["claims"] == 1
    assert report["no_answer_in_source"] == ["CQ-EXAMPLE-02"]


# --------------------------------------------------------------------------
# The validator
# --------------------------------------------------------------------------


def test_a_well_formed_answer_file_is_accepted() -> None:
    report = _validate()

    assert report["status"] == "ACCEPTED"
    assert report["questions"] == 2
    assert report["claims"] == 2
    assert report["claims_per_question"] == {"CQ-B1": 2, "CQ-B2": 0}
    assert report["no_answer_in_source"] == ["CQ-B2"]


def test_an_unknown_question_id_is_refused() -> None:
    document = _answers()
    document["answers"][0]["question_id"] = "CQ-NOT-ASKED"

    with pytest.raises(AnswerRefusal, match="the question file does not ask"):
        _validate(document)


def test_a_missing_question_is_refused() -> None:
    document = _answers()
    document["answers"] = [document["answers"][0]]

    with pytest.raises(AnswerRefusal, match="leaves questions unanswered"):
        _validate(document)


def test_a_claim_with_no_cited_block_is_refused() -> None:
    document = _answers()
    document["answers"][0]["claims"][0]["blocks"] = []

    with pytest.raises(AnswerRefusal, match="cites no reading block"):
        _validate(document)


def test_a_block_the_reading_does_not_declare_is_refused() -> None:
    document = _answers()
    document["answers"][0]["claims"][0]["blocks"] = ["page:9:block:999"]

    with pytest.raises(AnswerRefusal, match="the selected reading does not"):
        _validate(document)


def test_a_claim_quoting_the_reading_is_refused() -> None:
    """The rule that lets the answer file be published beside the graph cells."""

    document = _answers()
    document["answers"][0]["claims"][0]["statement"] = LONG_SENTENCE[:70]

    with pytest.raises(AnswerRefusal, match="shares a 60-character run"):
        _validate(document)


def test_an_answer_quoting_the_reading_is_refused() -> None:
    document = _answers()
    document["answers"][0]["answer"] = "It says: " + LONG_SENTENCE

    with pytest.raises(AnswerRefusal, match="shares a 60-character run"):
        _validate(document)


def test_a_quote_broken_across_whitespace_is_still_refused() -> None:
    """Normalization is the cells' own: whitespace collapsed, then compared."""

    document = _answers()
    document["answers"][0]["claims"][0]["statement"] = (
        LONG_SENTENCE[:70].replace(" ", "\n  ")
    )

    with pytest.raises(AnswerRefusal, match="shares a 60-character run"):
        _validate(document)


def test_a_shorter_shared_run_is_accepted() -> None:
    """Fifty-nine characters is below the threshold, and stays below it."""

    document = _answers()
    document["answers"][0]["claims"][0]["statement"] = LONG_SENTENCE[:59]

    assert _validate(document)["status"] == "ACCEPTED"


def test_a_no_answer_question_that_cites_a_claim_is_refused() -> None:
    document = _answers()
    document["answers"][1]["claims"] = [
        {
            "claim_id": "CQ-B2:c1",
            "statement": "A carrier is named.",
            "blocks": ["page:1:block:002"],
        }
    ]

    with pytest.raises(AnswerRefusal, match="declares NO_ANSWER_IN_SOURCE"):
        _validate(document)


def test_an_answer_with_no_claim_and_no_declaration_is_refused() -> None:
    document = _answers()
    document["answers"][0]["claims"] = []

    with pytest.raises(AnswerRefusal, match="cites no claim and declares no"):
        _validate(document)


def test_a_repeated_claim_id_is_refused() -> None:
    document = _answers()
    document["answers"][0]["claims"][1]["claim_id"] = "CQ-B1:c1"

    with pytest.raises(AnswerRefusal, match="repeats claim id"):
        _validate(document)


def test_an_answer_file_that_does_not_bind_its_inputs_is_refused() -> None:
    document = _answers()
    document["inputs"]["selected_reading_sha256"] = "sha256:" + "0" * 64

    with pytest.raises(AnswerRefusal, match="does not bind the selected reading"):
        _validate(document)


# --------------------------------------------------------------------------
# The builder, over the synthetic cell
# --------------------------------------------------------------------------


@pytest.fixture
def synthetic_cell(tmp_path, monkeypatch):
    reading = tmp_path / "selected-reading.json"
    reading.write_bytes(READING_BYTES)
    questions = tmp_path / "competency-questions.json"
    questions.write_bytes(QUESTIONS_BYTES)
    task = tmp_path / "spawn-message.md"
    task.write_bytes(b"# synthetic producer task\n")
    document = _answers()
    document["inputs"]["producer_task_sha256"] = _digest(task.read_bytes())
    answers = tmp_path / "answers.json"
    answers.write_bytes(_json_bytes(document))
    package = tmp_path / "package"

    # ROOT too: the builder writes repository-relative paths into the task and
    # the manifest, and the synthetic cell lives outside the repository.
    monkeypatch.setattr(builder, "ROOT", tmp_path)
    monkeypatch.setattr(builder, "SELECTED_READING", reading)
    monkeypatch.setattr(builder, "QUESTIONS", questions)
    monkeypatch.setattr(builder, "SPAWN_MESSAGE", task)
    monkeypatch.setattr(builder, "ANSWER_FILE", answers)
    monkeypatch.setattr(builder, "PACKAGE", package)
    monkeypatch.setattr(builder, "TASK", package / "review-task.md")
    monkeypatch.setattr(builder, "BLANK", package / "review-record.blank.md")
    monkeypatch.setattr(builder, "MANIFEST", package / "review-input-manifest.json")
    monkeypatch.setattr(
        builder,
        "MATERIALS",
        (
            ("selected_reading", reading, "PRIVATE"),
            ("competency_questions", questions, "PUBLIC"),
            ("answer_file", answers, "PUBLIC"),
            ("producer_task", task, "PUBLIC"),
        ),
    )
    return package, document, answers


def test_the_open_stage_leaves_the_counts_standing(synthetic_cell) -> None:
    package, _, _ = synthetic_cell

    written = builder.execute("open")

    assert written["questions"] == 2
    assert written["blocks"] == 2
    assert not (package / "review-input-manifest.json").exists()
    task = (package / "review-task.md").read_text(encoding="utf-8")
    assert "{{CLAIMS_TOTAL}}" in task and "{{WITNESSES_TOTAL}}" in task
    assert "{{RUN_ID}}" not in task


def test_the_freeze_stage_fills_every_figure(synthetic_cell) -> None:
    package, _, _ = synthetic_cell

    written = builder.execute("freeze")

    assert written["claims_total"] == 2
    assert written["witnesses_traced"] == 2
    task = (package / "review-task.md").read_text(encoding="utf-8")
    blank = (package / "review-record.blank.md").read_text(encoding="utf-8")
    assert "{{" not in task and "{{" not in blank
    assert "2 claims for `CQ-B1`, 0 for `CQ-B2`" in task


def test_the_frozen_manifest_validates_under_the_real_v32_protocol(
    synthetic_cell,
) -> None:
    package, _, _ = synthetic_cell
    builder.execute("freeze")

    manifest = review.validate_review_input_manifest(
        (package / "review-input-manifest.json").read_bytes(),
        PROTOCOL_V32.read_bytes(),
    )

    assert manifest["evidence_surface"]["kind"] == "IN_CONTEXT_ANSWER_SET"
    assert sorted(manifest["stage_identities"]) == [
        "answer_file_sha256",
        "producer_model_id",
        "producer_task_sha256",
    ]
    assert manifest["rows_per_question"] == {"CQ-B1": 2, "CQ-B2": 0}
    assert manifest["witnesses_traced"] == 2


def test_the_blank_record_validates_as_blank(synthetic_cell) -> None:
    package, _, _ = synthetic_cell
    builder.execute("freeze")

    validated = review.validate_blank_review(
        (package / "review-record.blank.md").read_bytes(),
        PROTOCOL_V32.read_bytes(),
        (package / "review-input-manifest.json").read_bytes(),
    )

    assert validated["schema"] == "malleus.paper-v4.source-grounded-review/v3.2"
    assert validated["status"] == "BLANK"
    assert validated["witnesses"] == []


def test_one_review_block_per_question_carries_its_claims(synthetic_cell) -> None:
    package, _, _ = synthetic_cell
    builder.execute("freeze")

    first = json.loads((package / "review-block.CQ-B1.json").read_bytes())
    second = json.loads((package / "review-block.CQ-B2.json").read_bytes())

    assert first["required_semantics"] == ["duration", "observing_system"]
    assert first["assembly"] == "NOT_APPLICABLE"
    assert first["question_responsiveness"] == "PENDING"
    assert [item["witness_key"] for item in first["rows"]] == ["CQ-B1:c1", "CQ-B1:c2"]
    assert first["claims"][0]["blocks"] == ["page:1:block:001"]
    assert second["rows"] == []
    assert second["no_answer_in_source"] is True
    assert [item["absent_reason"] for item in second["coverage"]] == [None]


def test_the_builder_refuses_an_answer_file_the_grammar_refuses(
    synthetic_cell,
) -> None:
    package, document, answers = synthetic_cell
    broken = copy.deepcopy(document)
    broken["answers"][0]["claims"][0]["blocks"] = ["page:9:block:999"]
    answers.write_bytes(_json_bytes(broken))

    # The builder loads its own copy of the validator, so the refusal it raises
    # is that module's class and not this one's.
    with pytest.raises(
        builder.answers_validator.AnswerRefusal, match="the selected reading does not"
    ):
        builder.execute("freeze")


def test_the_builder_refuses_before_the_producer_has_run(synthetic_cell) -> None:
    package, _, answers = synthetic_cell
    answers.unlink()

    with pytest.raises(builder.ReviewPackageRefusal, match="has not written an answer"):
        builder.execute("freeze")


def test_the_task_prints_the_checklist_as_a_numbered_list(synthetic_cell) -> None:
    package, _, _ = synthetic_cell
    builder.execute("freeze")
    task = (package / "review-task.md").read_text(encoding="utf-8")
    entries = [
        check
        for check in json.loads(PROTOCOL_V32.read_bytes())["checklist"]["checks"]
        if "IN_CONTEXT_ANSWER_SET" in check["applies_to"]
    ]

    assert "## The checklist" in task
    assert "Reproduce it in your handover note beside the record" in task
    numbers = [int(item) for item in re.findall(r"^(\d+)\. \*\*", task, re.M)]
    ids = re.findall(r"\(`(C-\d+)`\)", task)
    assert numbers == list(range(1, len(entries) + 1))
    assert ids == [check["id"] for check in entries]
    for check in entries:
        assert check["name"] in " ".join(task.split())
        assert check["records_outcome_in"] in task


def test_a_check_that_does_not_apply_to_this_surface_is_not_printed(
    synthetic_cell,
) -> None:
    """The graph surfaces' row-resolution checks are not the baseline's."""

    package, _, _ = synthetic_cell
    builder.execute("freeze")
    task = (package / "review-task.md").read_text(encoding="utf-8")
    section = json.loads(PROTOCOL_V32.read_bytes())["checklist"]["checks"]
    absent = [
        check
        for check in section
        if "IN_CONTEXT_ANSWER_SET" not in check["applies_to"]
    ]

    for check in absent:
        assert f"(`{check['id']}`)" not in task


def test_the_task_states_the_answer_set_differences(synthetic_cell) -> None:
    package, _, _ = synthetic_cell
    builder.execute("freeze")
    whole = (package / "review-task.md").read_text(encoding="utf-8")
    # The checklist quotes the protocol's cross-surface wording verbatim, so the
    # tokens this surface never asks for are checked against the task's own
    # prose, which is everything before it.
    task = " ".join(whole.split("## The checklist")[0].split())

    assert "review-protocol-v3.2.json" in task
    assert "IN_CONTEXT_ANSWER_SET" in task
    assert "NOT_CAPTURED" in task
    assert "NOT_APPLICABLE" in task
    assert "one cited claim" in task
    assert "There is no query binding, no query result" in task
    assert "This producer saw the questions." in task
    assert "Do not calculate a score" in task
    assert "Luis" in task
    # The graph cells' mechanical tokens must not be asked for here.
    for absent in ("VALUE_DERIVED_FROM_ROW", "DIGEST_OK", "SUBJECT_IN_BLOCK"):
        assert absent not in task


# --------------------------------------------------------------------------
# The run contract, the spawn message and the staging
# --------------------------------------------------------------------------


def test_the_run_contract_says_what_this_cell_is_not() -> None:
    contract = json.loads(CONTRACT.read_bytes())

    assert contract["condition"] == "IN_CONTEXT_BASELINE"
    assert contract["is_not_a_malleus_cell"] is True
    assert contract["questions_are_visible_to_this_producer"] is True
    assert contract["producer"]["skill"] == "NONE"
    assert contract["what_it_measures"]["reviewed_under"] == (
        "paper-v4/evaluation-v4/review-protocol-v3.2.json"
    )
    assert contract["verbatim_rule"]["window"] == 60


def test_the_spawn_message_carries_the_isolation_the_contract_declares() -> None:
    text = " ".join(SPAWN.read_text(encoding="utf-8").split())
    contract = json.loads(CONTRACT.read_bytes())

    assert "Own only `<PRODUCER_WORKSPACE>/work/`" in text
    assert "Do not inspect the repository" in text
    assert "Do not use the network or delegate" in text
    assert "There is no Malleus skill in this workspace" in text
    assert "work/answers.json" in text
    assert "sixty characters" in text
    assert contract["producer"]["spawn_message"] == (
        "paper-v4/experiment-v4/baseline-01/spawn-message.md"
    )


def test_the_contract_names_the_command_that_stages_the_producer() -> None:
    contract = json.loads(CONTRACT.read_bytes())
    prepare = next(
        stage for stage in contract["stages"] if stage["stage"] == "PREPARE"
    )

    assert "prepare_producer.py" in prepare["command"]
    assert "--output private/paper-v4-baseline-01/producer" in prepare["command"]


def test_staging_outside_private_is_refused(tmp_path) -> None:
    with pytest.raises(
        prepare_producer.ProducerPreparationRefusal, match="below private/"
    ):
        prepare_producer.prepare(tmp_path / "reading.json", tmp_path / "producer")


def test_staging_writes_the_declared_closure_and_nothing_else(tmp_path, monkeypatch) -> None:
    private = tmp_path / "private"
    private.mkdir()
    monkeypatch.setattr(prepare_producer, "ROOT", tmp_path)
    reading = tmp_path / "selected-reading.json"
    reading.write_bytes(READING_BYTES)
    contract = json.loads(CONTRACT.read_bytes())
    for item in contract["declared_inputs"]:
        if item["name"] == "SELECTED_READING":
            continue
        target = tmp_path / item["source"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / item["source"]).read_bytes())

    receipt = prepare_producer.prepare(reading, private / "paper-v4-baseline-01/producer")

    workspace = private / "paper-v4-baseline-01/producer"
    written = sorted(
        str(path.relative_to(workspace))
        for path in workspace.rglob("*")
        if path.is_file()
    )
    assert written == sorted(item["target"] for item in contract["declared_inputs"])
    assert (workspace / "work").is_dir()
    assert receipt["status"] == "FROZEN"
    assert receipt["producer"]["skill"] == "NONE"
    assert {item["name"] for item in receipt["files"]} == {
        item["name"] for item in contract["declared_inputs"]
    }
    task = next(item for item in receipt["files"] if item["name"] == "PRODUCER_TASK")
    assert task["sha256"] == _digest(SPAWN.read_bytes())


def test_staging_refuses_to_overwrite_an_existing_workspace(tmp_path, monkeypatch) -> None:
    private = tmp_path / "private"
    workspace = private / "paper-v4-baseline-01/producer"
    workspace.mkdir(parents=True)
    monkeypatch.setattr(prepare_producer, "ROOT", tmp_path)
    reading = tmp_path / "selected-reading.json"
    reading.write_bytes(READING_BYTES)

    with pytest.raises(
        prepare_producer.ProducerPreparationRefusal, match="already exists"
    ):
        prepare_producer.prepare(reading, workspace)


def test_the_active_gate_collects_this_cell() -> None:
    manifest = json.loads((ROOT / "paper-v4/active-test-manifest.json").read_bytes())

    assert "paper-v4/experiment-v4/baseline-01" in manifest["paths"]
