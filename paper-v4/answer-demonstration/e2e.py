"""Stage the accepted ontology of a two-phase producer, never a prior run's."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from binding import load_query_program, prepare_binding
from followup import checked_bytes
import pilot
from review_packet import canonical, digest


ROOT = pilot.ROOT
QUERY_SOURCE = ROOT / "private/paper-v4-answer-demonstration/pilot-03/run-21/answers.py"
QUERY_IDENTITY = (
    "sha256:389c4ff9565304be63caf432ece17ef108f3a0b2f229fbc53be70caf962dc698"
)


def phase_two_guard(ontology_agent, population_agent, diagnostic, population_exists):
    if not isinstance(ontology_agent, str) or not ontology_agent.strip():
        raise ValueError("an observed producer identity is required")
    if population_agent != ontology_agent:
        raise ValueError("population must resume the same producer as ontology")
    if diagnostic["status"] != "ACCEPTED":
        raise ValueError("phase two requires an accepted ontology")
    if population_exists:
        raise ValueError("query binding must be frozen before population exists")


def stage(run, attempt, population_agent):
    run = run.resolve()
    if not run.is_relative_to(ROOT / "private"):
        raise ValueError("end-to-end inputs must remain private")
    manifest_path = run / "manifest.json"
    if manifest_path.exists():
        raise ValueError("end-to-end acceptance is already frozen")
    initial = json.loads((run / "producer-input-manifest.json").read_bytes())
    prospective = initial["schema"] == "malleus.paper-v4.fresh-comparison-inputs/v1"
    if prospective:
        from fresh_comparison import verify_observed

        verify_observed(run, "initial")
    if initial["schema"] == "malleus.paper-v4.current-adoption-inputs/v1":
        from current_adoption import verify_observed

        verify_observed(run, "initial")
    launch = json.loads((run / "launch.json").read_bytes())
    producer = run / "producer"
    gate = run / "gate" / f"attempt-{attempt:02d}"
    diagnostic = json.loads((gate / "diagnostic.json").read_bytes())
    phase_two_guard(
        launch["agent_id"],
        population_agent,
        diagnostic,
        (producer / "work/document-population.json").exists(),
    )
    pilot.verify_runtime(initial["core"]["commit"])
    for item in initial["declared_inputs"]:
        checked_bytes(
            (producer / item["target"]).read_bytes(), item["sha256"], item["target"]
        )
    ontology_path = producer / "work" / f"ontology-attempt-{attempt:02d}.yaml"
    ontology = checked_bytes(
        ontology_path.read_bytes(), diagnostic["ontology_sha256"], "own ontology"
    )
    surface = checked_bytes(
        (gate / "population-surface.json").read_bytes(),
        diagnostic["population_surface_sha256"],
        "surface",
    )
    if prospective:
        from query_capacity import PROGRAM_IDENTITY, audit

        program = load_query_program(run / "method/answers.py", PROGRAM_IDENTITY)
    else:
        program = load_query_program(QUERY_SOURCE, QUERY_IDENTITY)
    questions = (
        ROOT / "paper-v4/experiment-v4/competency-questions-v3.json"
    ).read_bytes()
    binding = prepare_binding(
        surface,
        questions,
        initial["core"]["commit"],
        program._source_bytes,
        program=program,
    )
    sources = {
        "paper-v4-project": ontology,
        **{
            key: (producer / "inputs" / name).read_bytes()
            for key, name in {
                "malleus": "malleus.yaml",
                "linkml:types": "linkml-types.yaml",
                "metrology": "metrology.yaml",
                "chronology": "chronology.yaml",
                "research": "research.yaml",
            }.items()
        },
    }
    files = {
        "producer/accepted/population-surface.json": surface,
        "producer/accepted/diagnostic.json": (gate / "diagnostic.json").read_bytes(),
        "query-binding.acceptance.json": binding,
        "competency-questions.json": questions,
        "frozen-code/answers.py": program._source_bytes,
        "frozen-code/binding.py": Path(__file__).with_name("binding.py").read_bytes(),
    }
    if prospective:
        files.update(
            {
                "frozen-code/subject_answers.py": (
                    run / "method/subject_answers.py"
                ).read_bytes(),
                "query-capacity.json": canonical(
                    audit(json.loads(surface), program._source_bytes, questions)
                ),
            }
        )
    for name, data in files.items():
        path = run / name
        if path.exists():
            raise ValueError(f"refusing to overwrite acceptance input: {path}")
    for name, data in files.items():
        path = run / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    result = {
        "schema": "malleus.paper-v4.end-to-end/v1",
        "run_id": initial["run_id"],
        "producer_condition": "FRESH_END_TO_END",
        "core_commit": initial["core"]["commit"],
        "core_tree": initial["core"]["tree"],
        "ontology_agent_id": launch["agent_id"],
        "population_agent_id": population_agent,
        "ontology_path": str(ontology_path.relative_to(run)),
        "ontology_sha256": digest(ontology),
        "reading_sha256": digest(
            (producer / "inputs/selected-reading.json").read_bytes()
        ),
        "source_closure_sha256": {key: digest(value) for key, value in sources.items()},
        "query_binding_sha256": digest(binding),
        "query_program_sha256": digest(program._source_bytes),
        "accepted_at": datetime.now(timezone.utc).isoformat(),
        "ontology_attempt": attempt,
        "interface_coordinates": initial["interface_coordinates"],
        "materials": [
            {"path": name, "sha256": digest(data)}
            for name, data in sorted(files.items())
        ],
    }
    if prospective:
        result.update(
            query_reader="SubjectGraphReads",
            query_capacity_sha256=digest(files["query-capacity.json"]),
        )
    manifest_path.write_bytes(canonical(result))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--attempt", type=int, required=True)
    parser.add_argument("--agent-id", required=True)
    args = parser.parse_args()
    print(canonical(stage(args.run, args.attempt, args.agent_id)).decode())
