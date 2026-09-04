from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess


SUBJECT_PATH = Path(__file__).with_name("compile_ontology_candidate.py")
SPEC = importlib.util.spec_from_file_location(
    "paper_v4_compile_candidate", SUBJECT_PATH
)
assert SPEC is not None and SPEC.loader is not None
SUBJECT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SUBJECT)
ROOT = Path(__file__).resolve().parents[2]


def _producer_inputs(tmp_path: Path) -> Path:
    # Run-01 is frozen at its recorded paper merge commit (which carries Core
    # 6488ddb); its inputs are the bytes at that commit, not the live tree,
    # which has moved since (the packs were revised on 2026-09-04).
    contract = json.loads(Path(__file__).with_name("run-contract.json").read_bytes())
    frozen_commit = contract["core_gate"]["execution_baseline"]["paper_merge_commit"]
    producer = tmp_path / "producer"
    for target in SUBJECT.SOURCE_TARGETS.values():
        source = {
            "inputs/malleus.yaml": "ontology/malleus.yaml",
            "inputs/linkml-types.yaml": (
                "paper-v4/experiment-v2/run-inputs/linkml-types.yaml"
            ),
            "inputs/metrology.yaml": "ontology/packs/metrology.yaml",
            "inputs/chronology.yaml": "ontology/packs/chronology.yaml",
            "inputs/research.yaml": "ontology/packs/research.yaml",
        }[target]
        frozen = subprocess.run(
            ["git", "show", f"{frozen_commit}:{source}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        destination = producer / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(frozen)
    return producer


def test_direct_root_class_without_grounding_is_a_typed_refusal(
    tmp_path: Path,
) -> None:
    producer = _producer_inputs(tmp_path)
    ontology = tmp_path / "candidate.yaml"
    ontology.write_text(
        """id: https://example.org/project
name: project
imports: [linkml:types, malleus]
classes:
  ProjectThing:
    is_a: Entity
""",
        encoding="utf-8",
    )
    output = tmp_path / "gate"

    assert not SUBJECT.compile_candidate(
        ontology_path=ontology,
        producer_root=producer,
        output=output,
        attempt=1,
    )
    diagnostic = json.loads((output / "diagnostic.json").read_bytes())
    assert diagnostic["status"] == "REFUSED"
    assert diagnostic["stage"] == "PACK_GROUNDING"
    assert diagnostic["reason"] == "DIRECT_ROOT_GROUNDING_REQUIRED"
    assert set(path.name for path in output.iterdir()) == {"diagnostic.json"}


def test_pack_derived_project_compiles_to_an_exact_population_surface(
    tmp_path: Path,
) -> None:
    producer = _producer_inputs(tmp_path)
    ontology = tmp_path / "candidate.yaml"
    ontology.write_text(
        """id: https://example.org/project
name: project
imports: [linkml:types, malleus, research]
classes:
  StudyObservation:
    is_a: Observation
""",
        encoding="utf-8",
    )
    output = tmp_path / "gate"

    assert SUBJECT.compile_candidate(
        ontology_path=ontology,
        producer_root=producer,
        output=output,
        attempt=1,
    )
    diagnostic = json.loads((output / "diagnostic.json").read_bytes())
    surface = json.loads((output / "population-surface.json").read_bytes())
    assert diagnostic["status"] == "ACCEPTED"
    assert diagnostic["stage"] == "COMPLETE"
    assert any(
        item["name"] == "StudyObservation" and item["family"] == "ENTITY"
        for item in surface["record_types"]
    )
    assert set(path.name for path in output.iterdir()) == {
        "diagnostic.json",
        "grounding-receipt.json",
        "population-surface.json",
        "validated-contract.json",
    }


def test_cli_binds_ontology_argument_to_ontology_path(
    monkeypatch,
    tmp_path: Path,
) -> None:
    observed = {}

    def fake_compile_candidate(**values) -> bool:
        observed.update(values)
        return True

    monkeypatch.setattr(SUBJECT, "compile_candidate", fake_compile_candidate)
    ontology = tmp_path / "ontology.yaml"
    producer = tmp_path / "producer"
    output = tmp_path / "gate"

    assert (
        SUBJECT.main(
            [
                "--ontology",
                str(ontology),
                "--producer-root",
                str(producer),
                "--output",
                str(output),
                "--attempt",
                "3",
            ]
        )
        == 0
    )
    assert observed == {
        "ontology_path": ontology,
        "producer_root": producer,
        "output": output,
        "attempt": 3,
    }
