"""Guards for the isolated v2 population acquisition input set."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "paper-v4/experiment-v2/population-run"
MANIFEST = RUN / "input-manifest.json"

EXPECTED = {
    "TASK": (
        RUN / "task.md",
        "sha256:00cca7d26cd37260fd3bf056f55e96f6562cad25f9d1c951d2fac43f916825c2",
    ),
    "SELECTED_ONTOLOGY": (
        RUN / "inputs/ontology.yaml",
        "sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed",
    ),
    "GENERIC_RECIPES": (
        RUN / "inputs/generic-recipes.stottr",
        "sha256:7324dbe955a7f0395d878c4e6198704a4fa11c296b79a66c8a30729ab4fbb968",
    ),
    "COMPETENCY_QUESTIONS": (
        RUN / "inputs/competency-questions.json",
        "sha256:5ec41374e32a8745963a0f0498e2044f225dec47a6cbfcfde1417752b27b9a92",
    ),
    "SELECTED_READING": (
        ROOT / "private/paper-v4-text-layer/selected-reading.json",
        "sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17",
    ),
}


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_manifest_closes_the_only_model_visible_files() -> None:
    manifest = json.loads(MANIFEST.read_bytes())

    assert manifest["schema"] == "malleus.paper-v4.population-input-manifest/v2"
    assert manifest["status"] == "FROZEN_BEFORE_POPULATION_ACQUISITION"
    assert manifest["attempt_policy"] == {
        "maximum_structural_retries": 1,
        "semantic_repair": "FORBIDDEN",
        "fallback_population": "FORBIDDEN",
    }
    assert manifest["session_policy"] == {
        "fresh_context": True,
        "network_access": "FORBIDDEN",
        "delegation": "FORBIDDEN",
        "read_scope": "DECLARED_FILES_ONLY",
        "write_scope": "POPULATION_JSON_ONLY",
    }
    files = {item["role"]: item for item in manifest["files"]}
    assert set(files) == set(EXPECTED)
    for role, (path, digest) in EXPECTED.items():
        assert path.is_file() and not path.is_symlink()
        assert (ROOT / files[role]["locator"]).resolve() == path.resolve()
        assert files[role]["sha256"] == digest == _digest(path)


def test_public_input_copies_are_byte_identical_to_their_frozen_sources() -> None:
    assert (RUN / "inputs/ontology.yaml").read_bytes() == (
        ROOT / "paper-v4/experiment-v2/ontology-run/ontology-02.yaml"
    ).read_bytes()
    assert (RUN / "inputs/generic-recipes.stottr").read_bytes() == (
        ROOT / "paper-v4/experiment-v2/generic-recipes.stottr"
    ).read_bytes()
    assert (RUN / "inputs/competency-questions.json").read_bytes() == (
        ROOT / "paper-v4/experiment/competency-questions.json"
    ).read_bytes()


def test_task_forbids_answer_smuggling_and_fixes_closed_output() -> None:
    task = (RUN / "task.md").read_text()

    for leaked_value in (
        "SMARTIES",
        "segment RC2",
        "10 to 20",
        "0.4 to 3.0",
        "preferred CO2",
    ):
        assert leaked_value not in task
    for required_guard in (
        "Do not represent a campaign as an observation method",
        "Do not expand an aggregate instrument count",
        "Do not turn a proposed or preferred mechanism",
        "count, location, direction, relationship",
        "must not carry a fact that lacks a corresponding typed property or relation",
        "Missing ontology semantics must remain missing",
        "start at `001` and increase without gaps",
        "malleus.paper-v4.population/v2",
        "malleus.paper-v4.population-refusal/v2",
        "Write only `population.json`",
    ):
        assert required_guard in task
