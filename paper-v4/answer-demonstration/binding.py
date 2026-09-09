"""Freeze query source and accepted surface before population is visible.

This is a paper input manifest, not a query language. The caller records its
digest at ontology acceptance before dispatching population. Creating these
bytes alone does not attest when that dispatch happened.
"""

from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from types import ModuleType

import answers


QUESTION_IDENTITY = (
    "sha256:76d501cdb91741ede6ab51e36f1a567d59009f0b3ecf970cf7b19adf97c7490d"
)


def identity(source):
    return "sha256:" + sha256(source).hexdigest()


def load_query_program(path, expected_identity):
    """Execute the exact identified local query bytes, not an ambient import."""
    source = path.read_bytes()
    if identity(source) != expected_identity:
        raise ValueError("selected query identity differs from frozen bytes")
    name = "paper_query_" + expected_identity.removeprefix("sha256:")
    module = ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    try:
        exec(compile(source, str(path), "exec"), module.__dict__)
    except BaseException:
        del sys.modules[name]
        raise
    module._source_bytes = source
    return module


def prepare_binding(
    surface_source, question_source, core_commit, program_source, *, program=answers
):
    if identity(question_source) != QUESTION_IDENTITY:
        raise ValueError("question bytes differ from frozen E-0206")
    if not re.fullmatch(r"[0-9a-f]{40}", core_commit):
        raise ValueError("Core binding requires a full commit identity")
    loaded_source = (
        Path(answers.__file__).read_bytes()
        if program is answers
        else program._source_bytes
    )
    if program_source != loaded_source:
        raise ValueError("manifest source differs from loaded query program")
    surface = json.loads(surface_source)
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", surface["validated_fact_set_sha256"]):
        raise ValueError("surface lacks a valid compiled fact identity")
    # Validate the surface's named types without creating or reading a graph.
    program.GraphReads(None, surface)
    questions = json.loads(question_source)["questions"]
    if len(questions) != len(program.PROGRAMS) or {q["id"] for q in questions} != set(
        program.PROGRAMS
    ):
        raise ValueError("each frozen question must bind exactly one query program")
    value = {
        "schema": "malleus.paper-v4.answer-query-inputs/v1",
        "intended_stage": "ONTOLOGY_ACCEPTANCE",
        "core_commit": core_commit,
        "question_set_sha256": identity(question_source),
        "population_surface_sha256": identity(surface_source),
        "validated_fact_set_sha256": surface["validated_fact_set_sha256"],
        "query_program_sha256": identity(program_source),
        "programs": [
            {"question_id": q["id"], "function": program.PROGRAMS[q["id"]].__name__}
            for q in questions
        ],
    }
    return json.dumps(
        value, allow_nan=False, sort_keys=True, separators=(",", ":")
    ).encode()


def validate_binding(
    source,
    surface_source,
    question_source,
    core_commit,
    program_source,
    *,
    program=answers,
):
    expected = prepare_binding(
        surface_source, question_source, core_commit, program_source, program=program
    )
    if source != expected:
        raise ValueError(
            "binding differs from frozen query inputs; no result-driven rebinding"
        )
    return json.loads(expected)
