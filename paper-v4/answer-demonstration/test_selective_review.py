"""The additive review instrument checks records, never supplies judgments."""

from copy import deepcopy
from pathlib import Path

import pytest

from review_packet import canonical, digest
from selective_review import (
    MANIFEST_SCHEMA,
    RECORD_SCHEMA,
    assembly_check,
    load_base,
    protocol_bytes,
    validate,
)


@pytest.mark.parametrize("admitted", [False, True])
def test_fresh_replay_is_not_labelled_historical(admitted):
    from selective_review import replay_mode

    result = {
        "schema": "malleus.paper-v4.followup-answers/v1",
        "execution_mode": "FRESH_FIXED_ONTOLOGY",
        "replay_matches_preclose": True,
        "admission_occurred": admitted,
        "ledger_bytes_unchanged": True,
    }
    assert replay_mode(result) == "FRESH_FIXED_ONTOLOGY"
    assert "historical_replay_matches" not in result


def test_end_to_end_review_cannot_be_labelled_population_only():
    from selective_review import replay_mode

    result = {
        "schema": "malleus.paper-v4.followup-answers/v1",
        "execution_mode": "FRESH_END_TO_END",
        "replay_matches_preclose": True,
        "admission_occurred": True,
        "ledger_bytes_unchanged": True,
    }
    assert replay_mode(result) == "FRESH_END_TO_END"


@pytest.mark.parametrize(
    "key,value",
    [
        ("replay_matches_preclose", False),
        ("admission_occurred", "true"),
        ("execution_mode", "RETROSPECTIVE"),
        ("ledger_bytes_unchanged", False),
    ],
)
def test_fresh_execution_metadata_cannot_be_defaulted(key, value):
    from selective_review import replay_mode

    result = {
        "schema": "malleus.paper-v4.followup-answers/v1",
        "execution_mode": "FRESH_FIXED_ONTOLOGY",
        "replay_matches_preclose": True,
        "admission_occurred": False,
        "ledger_bytes_unchanged": True,
    }
    result[key] = value
    with pytest.raises(ValueError, match="replay/read-only"):
        replay_mode(result)


BASE = Path(__file__).parents[1] / "evaluation-v4"


def test_extension_leaves_frozen_protocol_and_validator_unchanged():
    source = (BASE / "review-protocol-v3.json").read_bytes()
    original = source
    protocol = protocol_bytes(source)
    extension = load_base(BASE / "review.py")
    validated = extension.validate_protocol(protocol)
    assert validated["judgments"]["assembly"][-1] == "NO_ANSWER"
    assert source == original == (BASE / "review-protocol-v3.json").read_bytes()


@pytest.mark.parametrize("rows", [[], [{"row_index": 0, "witness_key": "a"}]])
def test_no_answer_describes_no_covered_semantics_even_with_distractors(rows):
    record = {
        "questions": [
            {"assembly": "NO_ANSWER", "rows": rows, "coverage": [{"row_index": None}]}
        ]
    }
    before = deepcopy(record)
    assembly_check(record)
    assert record == before


def test_no_answer_cannot_hide_answering_fields():
    with pytest.raises(ValueError, match="NO_ANSWER"):
        assembly_check(
            {"questions": [{"assembly": "NO_ANSWER", "coverage": [{"row_index": 0}]}]}
        )


def test_empty_answer_cannot_be_called_one_row():
    with pytest.raises(ValueError, match="NO_ANSWER"):
        assembly_check(
            {"questions": [{"assembly": "ONE_ROW", "coverage": [{"row_index": None}]}]}
        )


def test_partial_coverage_keeps_the_reviewers_assembly():
    record = {
        "questions": [
            {"assembly": "ONE_ROW", "coverage": [{"row_index": 0}, {"row_index": None}]}
        ]
    }
    before = deepcopy(record)
    assembly_check(record)
    assert record == before


def test_altered_base_validator_refuses(tmp_path):
    path = tmp_path / "review.py"
    path.write_bytes((BASE / "review.py").read_bytes() + b"\n# drift\n")
    with pytest.raises(ValueError, match="base validator"):
        load_base(path)


@pytest.fixture
def synthetic_packet(tmp_path):
    protocol = protocol_bytes((BASE / "review-protocol-v3.json").read_bytes())
    reading = canonical(
        {
            "source_sha256": digest(b"synthetic source"),
            "pages": [
                {"blocks": [{"id": "block:a", "text": "A synthetic observation."}]}
            ],
        }
    )
    questions = canonical(
        {
            "schema": "malleus.paper-v4.competency-questions/v3",
            "questions": [
                {"id": "A", "required_semantics": ["quantity"]},
                {"id": "B", "required_semantics": ["unreported_quantity"]},
            ],
        }
    )
    sources = {
        "review_protocol": protocol,
        "selected_reading": reading,
        "competency_questions": questions,
        "query_program": b"# synthetic query",
        "query_runner": b"# synthetic runner",
        "program_binding_helper": b"# synthetic input binding",
        "population_surface": b"{}",
        "population_trace": b"{}",
        "query_trace_summary": b"{}",
        "retained_capture": b"{}",
    }
    inputs = {
        "ledger_head": digest(b"ledger"),
        "replay_receipt_sha256": digest(b"replay"),
    }
    for name, key in (
        ("query_program", "query_program_sha256"),
        ("query_runner", "runner_sha256"),
        ("program_binding_helper", "binding_program_sha256"),
        ("population_surface", "population_surface_sha256"),
        ("competency_questions", "question_set_sha256"),
    ):
        inputs[key] = digest(sources[name])
    sources["query_result"] = canonical(
        {
            "status": "EXPLORATORY_UNREVIEWED",
            "inputs": inputs,
            "historical_replay_matches": True,
            "ledger_bytes_unchanged": True,
            "forbidden_attempts": {"embedding_import": 0, "file_read": 0, "network": 0},
            "queries": [
                {
                    "question_id": "A",
                    "rows": [
                        {
                            "kind": "ENTITY",
                            "witness": {"record_id": "r"},
                            "record": {"quantity": 7},
                        }
                    ],
                },
                {"question_id": "B", "rows": []},
            ],
        }
    )
    sources["query_binding"] = canonical(
        {
            "mode": "RETROSPECTIVE_EXECUTED_PROGRAMS",
            "recorded_query_inputs": inputs,
            "query_result_sha256": digest(sources["query_result"]),
        }
    )
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "status": "FROZEN_FOR_REVIEW",
        "run_id": "synthetic",
        "review_protocol_sha256": digest(protocol),
        "evidence_surface": {
            "kind": "SELECTED_READING_TEXT_LAYER",
            "locator_kind": "SELECTED_READING_BLOCK_ID",
        },
        "fixed_identities": {
            "competency_questions_sha256": digest(questions),
            "selected_reading_sha256": digest(reading),
            "source_sha256": digest(b"synthetic source"),
        },
        "stage_identities": {
            "accepted_ontology_sha256": digest(b"ontology"),
            "ledger_head": inputs["ledger_head"],
            "replay_receipt_sha256": inputs["replay_receipt_sha256"],
            "query_binding_sha256": digest(sources["query_binding"]),
            "query_result_sha256": digest(sources["query_result"]),
            "population_trace_summary_sha256": digest(sources["population_trace"]),
            "query_trace_summary_sha256": digest(sources["query_trace_summary"]),
        },
        "question_ids": ["A", "B"],
        "rows_per_question": {"A": 1, "B": 0},
        "witnesses_traced": 1,
        "materials": [
            {
                "name": n,
                "path": n + ".json",
                "sha256": digest(s),
                "visibility": "PRIVATE",
            }
            for n, s in sources.items()
        ],
        "authorship": {
            "preliminary_evaluator_kind": "CODEX_PRELIMINARY",
            "ratifier_evaluator_kind": "HUMAN_AUTHOR",
            "ratifier_actor_id": "actor:luis",
            "deviation": {
                "from": "CLAUDE_PRELIMINARY",
                "to": "CODEX_PRELIMINARY",
                "protocol_edited": False,
                "reason": "Synthetic instrument test.",
            },
        },
    }
    record = {
        "schema": RECORD_SCHEMA,
        "status": "PRELIMINARY_COMPLETE",
        "inputs": {
            "review_protocol_sha256": digest(protocol),
            "review_input_manifest_sha256": digest(canonical(manifest)),
        },
        "preliminary": {
            "evaluator_kind": "CODEX_PRELIMINARY",
            "actor_id": "actor:synthetic",
            "completed_at": "2026-09-06T00:00:00Z",
        },
        "ratification": {
            "evaluator_kind": "HUMAN_AUTHOR",
            "actor_id": "actor:luis",
            "disposition": "PENDING",
            "completed_at": "",
            "notes": "",
        },
        "witnesses": [
            {
                "witness_key": "r",
                "source_support": "SUPPORTED",
                "source_locators": ["block:a"],
                "rationale": "Synthetic judgment for exercising structure, not paper evidence.",
            }
        ],
        "questions": [
            {
                "question_id": "A",
                "question_responsiveness": "COVERED",
                "responsiveness_rationale": "Synthetic coverage.",
                "assembly": "ONE_ROW",
                "coverage": [
                    {
                        "semantic": "quantity",
                        "row_index": 0,
                        "absent_reason": None,
                        "note": "quantity field",
                    }
                ],
                "rows": [{"row_index": 0, "witness_key": "r"}],
                "source_locators": ["block:a"],
            },
            {
                "question_id": "B",
                "question_responsiveness": "NONE",
                "responsiveness_rationale": "Synthetic absence.",
                "assembly": "NO_ANSWER",
                "coverage": [
                    {
                        "semantic": "unreported_quantity",
                        "row_index": None,
                        "absent_reason": "NOT_IN_SOURCE",
                        "note": "Synthetic source does not report it.",
                    }
                ],
                "rows": [],
                "source_locators": ["block:a"],
            },
        ],
    }
    for n, s in sources.items():
        (tmp_path / (n + ".json")).write_bytes(s)
    (tmp_path / "base-review.py").write_bytes((BASE / "review.py").read_bytes())
    (tmp_path / "review-input-manifest.json").write_bytes(canonical(manifest))
    return tmp_path, record


def write_record(folder, record):
    path = folder / "record.md"
    path.write_bytes(b"```json\n" + canonical(record).rstrip() + b"\n```\n")
    return path


def test_complete_synthetic_review_validates_without_rewriting(synthetic_packet):
    folder, record = synthetic_packet
    assert validate(folder, write_record(folder, record)) == record


@pytest.mark.parametrize(
    "mutation, match",
    [
        (lambda r: r["witnesses"].clear(), "every returned witness"),
        (
            lambda r: r["witnesses"][0].update(source_support="PARTIAL"),
            "neither SUPPORTED",
        ),
        (
            lambda r: r["questions"][0].update(question_responsiveness="NONE"),
            "derivation",
        ),
        (lambda r: r["questions"][1].update(assembly="ONE_ROW"), "NO_ANSWER"),
        (
            lambda r: r["questions"][0].update(source_locators=["missing:block"]),
            "unknown blocks",
        ),
        (
            lambda r: r["ratification"].update(disposition="RATIFIED_AS_RECORDED"),
            "pending",
        ),
    ],
)
def test_existing_guards_survive_extension(synthetic_packet, mutation, match):
    folder, record = synthetic_packet
    mutation(record)
    with pytest.raises(ValueError, match=match):
        validate(folder, write_record(folder, record))


def test_changed_material_refuses_before_review(synthetic_packet):
    folder, record = synthetic_packet
    (folder / "query_result.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="material drift"):
        validate(folder, write_record(folder, record))


@pytest.mark.parametrize("drift", [False, True])
def test_fresh_full_record_binds_acceptance_inputs(synthetic_packet, drift):
    import json

    folder, record = synthetic_packet
    manifest = json.loads((folder / "review-input-manifest.json").read_bytes())
    result = json.loads((folder / "query_result.json").read_bytes())
    del result["historical_replay_matches"]
    result.update(
        schema="malleus.paper-v4.followup-answers/v1",
        execution_mode="FRESH_FIXED_ONTOLOGY",
        core_commit="a" * 40,
        replay_matches_preclose=True,
        admission_occurred=True,
    )
    acceptance = {
        key: result["inputs"][key]
        for key in (
            "query_program_sha256",
            "question_set_sha256",
            "population_surface_sha256",
        )
    }
    acceptance["core_commit"] = result["core_commit"]
    if drift:
        acceptance["query_program_sha256"] = digest(b"different query")
    acceptance_source = canonical(acceptance)
    result["inputs"]["query_binding_sha256"] = digest(acceptance_source)
    binding = {
        "mode": "FRESH_FIXED_ONTOLOGY",
        "recorded_query_inputs": result["inputs"],
        "query_result_sha256": digest(canonical(result)),
    }
    replacements = {
        "query_result": canonical(result),
        "query_binding": canonical(binding),
        "acceptance_query_binding": acceptance_source,
    }
    for name, source in replacements.items():
        path = name + ".json"
        (folder / path).write_bytes(source)
        existing = [item for item in manifest["materials"] if item["name"] == name]
        if existing:
            existing[0]["sha256"] = digest(source)
        else:
            manifest["materials"].append(
                {
                    "name": name,
                    "path": path,
                    "sha256": digest(source),
                    "visibility": "PRIVATE",
                }
            )
    manifest["stage_identities"].update(
        query_result_sha256=digest(replacements["query_result"]),
        query_binding_sha256=digest(replacements["query_binding"]),
    )
    (folder / "review-input-manifest.json").write_bytes(canonical(manifest))
    record["inputs"]["review_input_manifest_sha256"] = digest(canonical(manifest))
    path = write_record(folder, record)
    if drift:
        with pytest.raises(ValueError, match="acceptance-time input differs"):
            validate(folder, path)
    else:
        assert validate(folder, path) == record
