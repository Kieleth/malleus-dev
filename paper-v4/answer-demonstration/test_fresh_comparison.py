"""Prospective condition and schema diagnostics, never source truth scoring."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

HERE = Path(__file__).resolve().parent
PRIVATE = HERE.parents[1] / "private/paper-v4-answer-demonstration"


def test_new_condition_keeps_inputs_but_not_historical_effort_or_revision_loop():
    import current_adoption
    import fresh_comparison as fresh

    old = current_adoption.make_manifest("control")
    new = fresh.make_manifest("sol-fresh-comparison-01")
    assert new["declared_inputs"] == old["declared_inputs"]
    assert new["producer"]["reasoning_effort"] == "ultra"
    assert new["session"]["max_additive_revision_rounds"] == 0
    assert new["session"]["max_compiler_diagnostic_returns"] == 2
    assert current_adoption.SETTINGS["reasoning_effort"] == "low"
    files = current_adoption.input_bytes(new)
    fresh.verify_inputs(new, files)
    for key, value in (("reasoning_effort", "low"), ("model_id", "gpt-6-astra")):
        wrong = deepcopy(new)
        wrong["producer"][key] = value
        with pytest.raises(ValueError):
            fresh.verify_inputs(wrong, files)
    with pytest.raises(ValueError):
        fresh.verify_inputs(old, files)
    for changed in (
        {**files, "inputs/ontology.yaml": b"old"},
        {**files, "inputs/research.yaml": b"changed"},
    ):
        with pytest.raises(ValueError):
            fresh.verify_inputs(new, changed)


def test_prompt_matches_approved_generic_checklist_and_no_old_results():
    import fresh_comparison as fresh

    text = fresh.producer_task(PRIVATE / "synthetic-fresh")
    assert "same session" in text
    assert fresh.CHECKLIST in text
    for forbidden in (
        "CQ-T",
        "SMARTIES",
        "RC2",
        "21 days",
        "19 ocean",
        "sol-calibration",
        "sol-acquisition",
        "count:obs",
    ):
        assert forbidden not in text
    assert "at most twice" in text
    assert "No additive ontology revision" in text


def slot(name, kind="String", **extra):
    return {
        "name": name,
        "range_id": "https://malleus.dev/contract-facts/" + kind,
        "identifier": name == "id",
        "multivalued": False,
        **extra,
    }


def schema():
    return {
        "record_types": [
            {
                "name": "Observation",
                "family": "ENTITY",
                "slots": [
                    slot("id"),
                    slot("quantity_kind"),
                    slot("value_lower", "Float"),
                    slot("unit"),
                    slot("quantity_kind_class", "Enum", enum_values=["Length"]),
                ],
            },
            {
                "name": "Instrument",
                "family": "ENTITY",
                "slots": [slot("id"), slot("name")],
            },
            {
                "name": "Link",
                "family": "RELATION",
                "slots": [slot("relation_type", "Enum", enum_values=["OBSERVED_WITH"])],
            },
        ]
    }


def audited(surface):
    from query_capacity import audit

    method = PRIVATE / "duration-query-01/method"
    return audit(
        surface,
        (method / "answers.py").read_bytes(),
        (method / "questions.json").read_bytes(),
    )


def question(result, name):
    return next(q for q in result["questions"] if q["question_id"] == name)


def test_schema_audit_is_value_free_and_covers_all_questions():
    surface = schema()
    before = deepcopy(surface)
    result = audited(surface)
    assert len(result["questions"]) == 30
    assert surface == before
    assert question(result, "CQ-T1-05")["missing_declarations"] == []
    assert question(result, "CQ-T1-03")["missing_declarations"]
    assert "not semantic" in result["limit"].lower()


@pytest.mark.parametrize(
    "mutation,marker",
    [
        ("rename", "value_lower"),
        ("subclass", "Instrument"),
        ("predicate", "OBSERVED_WITH"),
        ("wrong_numeric_type", "value_lower"),
        ("multivalued", "value_lower"),
    ],
)
def test_unreadable_shapes_never_look_like_empty_compatible_graphs(mutation, marker):
    s = schema()
    if mutation == "rename":
        s["record_types"][0]["slots"][2]["name"] = "magnitude"
    elif mutation == "subclass":
        s["record_types"][1]["name"] = "SpecialInstrument"
    elif mutation == "predicate":
        s["record_types"][2]["slots"][0]["enum_values"] = ["MEASURED_USING"]
    elif mutation == "wrong_numeric_type":
        s["record_types"][0]["slots"][2]["range_id"] = (
            "https://malleus.dev/contract-facts/String"
        )
    else:
        s["record_types"][0]["slots"][2]["multivalued"] = True
    assert marker in str(question(audited(s), "CQ-T1-05")["missing_declarations"])


def test_unread_text_is_reported_not_aliased_or_filled():
    s = schema()
    s["record_types"][0]["slots"].append(slot("observation_kind"))
    assert (
        "Observation.observation_kind" in audited(s)["text_slots_not_searched_locally"]
    )


def test_wrong_program_questions_and_duplicate_declarations_refuse():
    from query_capacity import audit

    method = PRIVATE / "duration-query-01/method"
    code, questions = (
        (method / "answers.py").read_bytes(),
        (method / "questions.json").read_bytes(),
    )
    for c, q in ((code + b"\n", questions), (code, questions + b"\n")):
        with pytest.raises(ValueError):
            audit(schema(), c, q)
    s = schema()
    s["record_types"].append(deepcopy(s["record_types"][0]))
    with pytest.raises(ValueError):
        audit(s, code, questions)


def test_prospective_packet_freezes_only_declared_inputs_and_refuses_drift():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_fresh_comparison import check_packet; check_packet()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_packet():
    from tempfile import TemporaryDirectory
    import fresh_comparison as fresh

    with TemporaryDirectory(dir=PRIVATE, prefix="fresh-packet-test-") as directory:
        run = Path(directory) / "fresh-synthetic"
        fresh.prepare(run)
        fresh.verify_packet(run)
        assert not (run / "producer/inputs/ontology.yaml").exists()
        assert not (run / "producer/inputs/questions.json").exists()
        assert not (run / "producer/accepted").exists()
        assert (
            len(
                json.loads((run / "producer-input-manifest.json").read_bytes())[
                    "declared_inputs"
                ]
            )
            == 8
        )
        with pytest.raises(ValueError):
            fresh.prepare(run)
        (run / "spawn-message.md").write_text("injected")
        with pytest.raises(ValueError):
            fresh.verify_packet(run)


def test_new_acceptance_binds_current_reader_and_schema_audit_before_population():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_fresh_comparison import check_stage; check_stage()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_stage(review_callback=None):
    from tempfile import TemporaryDirectory
    from unittest.mock import patch
    import e2e
    import fresh_comparison as fresh
    from review_packet import digest

    original_query = e2e.QUERY_IDENTITY
    baseline = PRIVATE / "sol-e2e-corrected-01"
    old_manifest = json.loads((baseline / "manifest.json").read_bytes())
    # This is a compiler-acceptance fixture, never an input to a live producer.
    ontology = (baseline / old_manifest["ontology_path"]).read_bytes()
    diagnostic = (baseline / "producer/accepted/diagnostic.json").read_bytes()
    surface = (baseline / "producer/accepted/population-surface.json").read_bytes()
    with TemporaryDirectory(dir=PRIVATE, prefix="fresh-stage-test-") as directory:
        run = Path(directory) / "fresh-stage-fixture"
        fresh.prepare(run)
        (run / "producer/work").mkdir()
        (run / "producer/work/ontology-attempt-01.yaml").write_bytes(ontology)
        gate = run / "gate/attempt-01"
        gate.mkdir(parents=True)
        (gate / "diagnostic.json").write_bytes(diagnostic)
        (gate / "population-surface.json").write_bytes(surface)
        (run / "launch.json").write_text(json.dumps({"agent_id": "fixture-only"}))
        with patch.object(
            fresh, "verify_observed", return_value={"fixture": True}
        ) as observed:
            result = e2e.stage(run, 1, "fixture-only")
        observed.assert_called_once_with(run, "initial")
        assert result["query_program_sha256"] == digest(
            (fresh.METHOD / "answers.py").read_bytes()
        )
        assert result["query_reader"] == "SubjectGraphReads"
        assert (run / "query-capacity.json").is_file()
        assert result["query_capacity_sha256"] == digest(
            (run / "query-capacity.json").read_bytes()
        )
        assert (run / "frozen-code/subject_answers.py").read_bytes() == (
            fresh.METHOD / "subject_answers.py"
        ).read_bytes()
        assert not (run / "producer/accepted/query-capacity.json").exists()
        assert e2e.QUERY_IDENTITY == original_query
        import e2e_execute

        population = baseline / "attempt-01/submitted-population.json"
        with patch.object(fresh, "verify_observed", return_value={"fixture": True}):
            with pytest.raises(ValueError, match="attempt"):
                e2e_execute.execute(
                    run, population, run / "attempt-04", "2026-09-08T00:00:00Z"
                )
        assert not (run / "attempt-04").exists()
        with patch.object(
            fresh, "verify_observed", return_value={"fixture": True}
        ) as observed:
            execution = e2e_execute.execute(
                run, population, run / "attempt-01", "2026-09-08T00:00:00Z"
            )
        assert observed.call_count == 2
        assert execution["status"] == "ADMITTED_AND_REPLAYED"
        query = json.loads((run / "attempt-01/query-result.json").read_bytes())
        assert (
            query["inputs"]["query_capacity_sha256"] == result["query_capacity_sha256"]
        )
        assert query["inputs"]["reader_class"] == "SubjectGraphReads"
        with patch.object(fresh, "verify_observed", return_value={"fixture": True}):
            e2e_execute.execute(
                run, population, run / "reproduction-01", "2026-09-08T00:00:00Z"
            )
        for name in (
            "ledger/history.jsonl",
            "query-result.json",
            "query-trace-summary.json",
        ):
            assert (run / "attempt-01" / name).read_bytes() == (
                run / "reproduction-01" / name
            ).read_bytes()
        if review_callback is not None:
            review_callback(run)
