"""Review preparation preserves evidence and never supplies judgments."""

from copy import deepcopy
import inspect
from pathlib import Path

import pytest
import review_packet
import freeze_review

from review_packet import (
    canonical,
    digest,
    docket,
    new_private_directory,
    verify_trace_materials,
    vocabulary_sources,
)


def inputs():
    questions = {
        "questions": [
            {"id": "A", "question": "Which value?", "required_semantics": ["value"]},
            {
                "id": "B",
                "question": "Which missing value?",
                "required_semantics": ["value"],
                "expected_outcome": {"kind": "NOT_IN_SOURCE"},
            },
        ]
    }
    row = {
        "kind": "SUBJECT",
        "record_type": "Observation",
        "record": {"value_lower": 7, "subject": "s"},
        "subject": {"name": "some subject"},
        "witness": {"record_id": "r", "subject_id": "s"},
    }
    result = {
        "queries": [
            {"question_id": "A", "rows": [row]},
            {"question_id": "B", "rows": []},
        ]
    }
    trace = {"records": [{"record_id": "r"}, {"record_id": "s"}]}
    return questions, result, trace


def test_review_preparation_requires_explicit_result_selection():
    signature = inspect.signature(review_packet.prepare)
    for name in ("pilot", "result_identity"):
        assert name in signature.parameters
        assert signature.parameters[name].default is inspect.Parameter.empty


def test_review_freeze_requires_explicit_preparation_and_review_identity():
    signature = inspect.signature(freeze_review.freeze)
    for name in ("preparation", "review_id"):
        assert name in signature.parameters
        assert signature.parameters[name].default is inspect.Parameter.empty


def test_review_task_preserves_prose_semantics_without_inventing_subjects():
    task = (Path(review_packet.__file__).parent / "REVIEW-TASK.md").read_text()
    assert "a missing subject slot does not alone make claim_subject absent" in task
    assert "external source context to fill a missing or ambiguous subject" in task


def test_selected_query_result_binds_exact_bytes_and_run():
    source = canonical({"run_id": "synthetic-run", "queries": []})
    assert review_packet.checked_result(source, digest(source), "synthetic-run") == {
        "run_id": "synthetic-run",
        "queries": [],
    }
    with pytest.raises(ValueError, match="identity"):
        review_packet.checked_result(source + b"\n", digest(source), "synthetic-run")
    with pytest.raises(ValueError, match="run"):
        review_packet.checked_result(source, digest(source), "another-run")


def test_docket_preserves_fields_order_and_empty_questions_without_judgments():
    q, result, trace = inputs()
    original = deepcopy((q, result, trace))
    packet = docket(q, result, trace)
    assert packet["questions"][0]["rows"] == result["queries"][0]["rows"]
    assert packet["questions"][1]["rows"] == []
    assert "expected_outcome" not in packet["questions"][1]
    assert "assembly" not in packet["questions"][1]
    assert (q, result, trace) == original
    assert packet["distinct_central_witnesses"] == 1
    assert packet["traced_records_including_context"] == 2


def test_repeated_witness_is_grouped_with_every_projection_and_occurrence():
    q, result, trace = inputs()
    extra = deepcopy(result["queries"][0]["rows"][0])
    extra["record"]["unit"] = "unit"
    result["queries"][1]["rows"] = [extra]
    packet = docket(q, result, trace)
    witness = packet["witnesses"][0]
    assert witness["occurrences"] == [
        {"question_id": "A", "row_index": 0},
        {"question_id": "B", "row_index": 0},
    ]
    assert len(witness["projections"]) == 2
    assert packet["distinct_central_witnesses"] == 1


def test_missing_context_trace_refuses():
    q, result, trace = inputs()
    trace["records"].pop()
    with pytest.raises(ValueError, match="missing trace"):
        docket(q, result, trace)


def test_question_omission_or_reordering_refuses():
    q, result, trace = inputs()
    result["queries"].reverse()
    with pytest.raises(ValueError, match="question order"):
        docket(q, result, trace)


def test_duplicate_trace_identity_refuses():
    q, result, trace = inputs()
    trace["records"].append(trace["records"][0])
    with pytest.raises(ValueError, match="duplicate trace"):
        docket(q, result, trace)


def test_required_witness_identity_is_not_defaulted():
    q, result, trace = inputs()
    del result["queries"][0]["rows"][0]["witness"]["record_id"]
    with pytest.raises((KeyError, ValueError)):
        docket(q, result, trace)


def test_packet_directory_must_be_new_and_private(tmp_path):
    private = tmp_path / "private"
    private.mkdir()
    with pytest.raises(ValueError, match="private"):
        new_private_directory(tmp_path / "public", private)
    with pytest.raises(ValueError, match="overwrite"):
        new_private_directory(private, private)


def trace_inputs():
    reading = canonical(
        {
            "block_count": 1,
            "pages": [{"blocks": [{"id": "block:a", "text": "A source statement."}]}],
        }
    )
    capture = canonical(
        {
            "assertions": [
                {
                    "id": "assertion:a",
                    "block": "block:a",
                    "statement": "source statement",
                    "formalized_by": [
                        {"record_id": "r", "path": ["properties", "name"]}
                    ],
                }
            ]
        }
    )
    trace = {
        "records": [
            {
                "record_id": "r",
                "sources": {"source:a": digest(reading)},
                "evidence": {"capture:a": digest(capture)},
                "derivations": [
                    {"locator": "assertion:a", "path": ["properties", "name"]}
                ],
            }
        ]
    }
    return reading, capture, trace


def test_exact_trace_closure_accepts_without_grading():
    assert verify_trace_materials(*trace_inputs()) is None


@pytest.mark.parametrize("field", ["sources", "evidence"])
def test_unbound_evidence_bytes_refuse(field):
    reading, capture, trace = trace_inputs()
    trace["records"][0][field] = {}
    with pytest.raises(ValueError, match="unbound"):
        verify_trace_materials(reading, capture, trace)


def test_substituted_derivation_path_refuses():
    reading, capture, trace = trace_inputs()
    trace["records"][0]["derivations"][0]["path"] = ["properties", "other"]
    with pytest.raises(ValueError, match="not formalized"):
        verify_trace_materials(reading, capture, trace)


def test_capture_not_contained_in_selected_block_refuses():
    reading, capture, trace = trace_inputs()
    changed = reading.replace(b"source statement", b"different words")
    trace["records"][0]["sources"] = {"source:a": digest(changed)}
    with pytest.raises(ValueError, match="not exact selected text"):
        verify_trace_materials(changed, capture, trace)


@pytest.mark.parametrize("separator", ["\n", "\t", "\u00a0", "  "])
def test_trace_source_matching_uses_declared_whitespace_collapse(separator):
    import json

    reading, capture, trace = trace_inputs()
    source = json.loads(reading)
    source["pages"][0]["blocks"][0]["text"] = f"A source{separator}statement."
    reading = canonical(source)
    trace["records"][0]["sources"] = {"source:a": digest(reading)}
    before = deepcopy((reading, capture, trace))
    verify_trace_materials(reading, capture, trace)
    assert (reading, capture, trace) == before


@pytest.mark.parametrize(
    "text",
    [
        "A sourcestatement.",
        "A Source statement.",
        "A source, statement.",
        "A source other statement.",
    ],
)
def test_source_whitespace_rule_does_not_change_words_case_or_punctuation(text):
    import json

    reading, capture, trace = trace_inputs()
    source = json.loads(reading)
    source["pages"][0]["blocks"][0]["text"] = text
    reading = canonical(source)
    trace["records"][0]["sources"] = {"source:a": digest(reading)}
    with pytest.raises(ValueError, match="not exact selected text"):
        verify_trace_materials(reading, capture, trace)


def test_vocabulary_closure_retains_all_exact_definitions(tmp_path):
    root = tmp_path / "root.yaml"
    imported = tmp_path / "arbitrary-import-filename.yaml"
    root.write_bytes(b"id: synthetic-root\n")
    imported.write_bytes(b"id: synthetic-import\n")
    closure = {
        "root": digest(root.read_bytes()),
        "import": digest(imported.read_bytes()),
    }
    sources = vocabulary_sources(closure, [root, imported], closure["root"])
    assert root.read_bytes() in sources.values()
    assert imported.read_bytes() in sources.values()
    assert "vocabulary-closure.json" in sources


@pytest.mark.parametrize("failure", ["missing", "drift", "root_omitted"])
def test_incomplete_vocabulary_fails_before_a_packet_can_be_written(tmp_path, failure):
    root = tmp_path / "root.yaml"
    imported = tmp_path / "import.yaml"
    root.write_bytes(b"root definition")
    imported.write_bytes(b"import definition")
    identity = digest(root.read_bytes())
    closure = {"root": identity, "import": digest(imported.read_bytes())}
    paths = [root, imported]
    if failure == "missing":
        paths.pop()
    elif failure == "drift":
        imported.write_bytes(b"changed definition")
    else:
        del closure["root"]
    with pytest.raises(ValueError, match="(vocabulary closure|exact vocabulary bytes)"):
        vocabulary_sources(closure, paths, identity)
