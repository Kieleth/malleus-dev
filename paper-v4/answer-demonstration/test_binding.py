"""A binding freezes query code and schema, never a populated graph."""

from hashlib import sha256
import json
from pathlib import Path

import pytest

from binding import prepare_binding, validate_binding


HERE = Path(__file__).resolve().parent
QUESTIONS = (HERE.parent / "experiment-v4/competency-questions-v3.json").read_bytes()
SURFACE = (
    HERE.parent / "experiment-v4/run-20/ontology-run/population-surface.json"
).read_bytes()
CORE = "c95dba7b86bb61487bda9a52458e1ea47cce20ab"
PROGRAM = (HERE / "answers.py").read_bytes()


def test_binding_has_no_graph_input_and_binds_all_thirty_programs():
    source = prepare_binding(SURFACE, QUESTIONS, CORE, PROGRAM)
    value = validate_binding(source, SURFACE, QUESTIONS, CORE, PROGRAM)
    assert len(value["programs"]) == 30
    assert value["intended_stage"] == "ONTOLOGY_ACCEPTANCE"
    assert "rows" not in value
    assert "ledger_head" not in value
    assert "replay_receipt_sha256" not in value
    assert value["query_program_sha256"] == "sha256:" + sha256(PROGRAM).hexdigest()


@pytest.mark.parametrize("changed", ["surface", "questions", "core", "program"])
def test_binding_refuses_any_input_drift(changed):
    source = prepare_binding(SURFACE, QUESTIONS, CORE, PROGRAM)
    args = [SURFACE, QUESTIONS, CORE, PROGRAM]
    index = ["surface", "questions", "core", "program"].index(changed)
    args[index] += "0" if changed == "core" else b"\n"
    with pytest.raises(ValueError):
        validate_binding(source, *args)


def test_query_list_cannot_change_after_binding():
    source = prepare_binding(SURFACE, QUESTIONS, CORE, PROGRAM)
    value = json.loads(source)
    value["programs"][0]["function"] = "preferred_mechanism"
    with pytest.raises(ValueError, match="binding differs"):
        validate_binding(json.dumps(value).encode(), SURFACE, QUESTIONS, CORE, PROGRAM)


def test_surface_requires_a_compiled_fact_identity():
    value = json.loads(SURFACE)
    del value["validated_fact_set_sha256"]
    with pytest.raises((ValueError, KeyError)):
        prepare_binding(json.dumps(value).encode(), QUESTIONS, CORE, PROGRAM)


def test_fake_program_bytes_cannot_masquerade_as_loaded_programs():
    with pytest.raises(ValueError, match="loaded query program"):
        prepare_binding(SURFACE, QUESTIONS, CORE, b"a different program")


def test_identified_query_executes_selected_bytes_without_replacing_live_program(
    tmp_path,
):
    import answers
    from binding import load_query_program

    selected = PROGRAM.replace(b'"carbon dioxide", "co2", "co 2"', b'"selected only",')
    path = tmp_path / "selected.py"
    path.write_bytes(selected)
    identity = "sha256:" + sha256(selected).hexdigest()
    module = load_query_program(path, identity)
    assert module.CARBON_DIOXIDE == ("selected only",)
    assert answers.CARBON_DIOXIDE == ("carbon dioxide", "co2", "co 2")
    source = prepare_binding(SURFACE, QUESTIONS, CORE, selected, program=module)
    assert json.loads(source)["query_program_sha256"] == identity
    validate_binding(source, SURFACE, QUESTIONS, CORE, selected, program=module)
    with pytest.raises(ValueError, match="loaded query program"):
        prepare_binding(SURFACE, QUESTIONS, CORE, PROGRAM, program=module)
    path.write_bytes(PROGRAM)
    with pytest.raises(ValueError, match="query identity"):
        load_query_program(path, identity)


@pytest.mark.parametrize("missing", ["family", "slots"])
def test_incomplete_surface_refuses_before_a_binding_is_issued(missing):
    value = json.loads(SURFACE)
    del value["record_types"][0][missing]
    with pytest.raises((KeyError, ValueError)):
        prepare_binding(json.dumps(value).encode(), QUESTIONS, CORE, PROGRAM)
