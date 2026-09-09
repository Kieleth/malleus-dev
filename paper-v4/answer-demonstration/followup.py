"""Stage one fixed-ontology, question-blind population follow-up. No producer call."""

import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import subprocess

import malleus.compiler as api

from binding import load_query_program, prepare_binding
import pilot
from review_packet import canonical, digest, new_private_directory


ROOT = pilot.ROOT
HERE = Path(__file__).resolve().parent
BASE = ROOT / "paper-v4/experiment-v4/run-20"
QUERY_IDENTITY = (
    "sha256:1ace62715e813125fce9ec5b38278faae25018468069b22c52bf2d87ea1bbdb1"
)
RUN_ID = "followup-sol-01"


def checked_bytes(source, expected, name):
    if digest(source) != expected:
        raise ValueError(f"fixed input differs: {name}")
    return source


def verify_materials(root, entries):
    root = root.resolve()
    for entry in entries:
        path = (root / entry["path"]).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"material escapes run: {entry['path']}")
        checked_bytes(path.read_bytes(), entry["sha256"], entry["path"])


def git_bytes(commit, path):
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def population_condition(base_run, run_id):
    if base_run not in {"run-20", "run-21"}:
        raise ValueError("fixed population requires a selected run-20/run-21 ontology")
    if not isinstance(run_id, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", run_id):
        raise ValueError("population run ID must be a safe lowercase identifier")
    return BASE.parent / base_run, run_id


def reference_module(name, *, base_run="run-20"):
    base, _ = population_condition(base_run, RUN_ID)
    path = base / name
    source = git_bytes(pilot.PAPER_BASELINE, str(path.relative_to(ROOT)))
    checked_bytes(path.read_bytes(), digest(source), str(path))
    spec = importlib.util.spec_from_file_location(
        "followup_reference_" + path.stem, path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare(
    core_commit,
    output,
    *,
    base_run="run-20",
    run_id=RUN_ID,
    query_identity=QUERY_IDENTITY,
    query_path=HERE / "answers.py",
):
    """Check and compile all inputs before writing a new private workspace."""
    base, run_id = population_condition(base_run, run_id)
    target = new_private_directory(output, ROOT / "private")
    pilot.verify_runtime(core_commit)
    reference_module("prepare_producer.py", base_run=base_run).preflight()
    historical = json.loads((base / "results/run-result.json").read_bytes())
    source_paths = {
        "paper-v4-project": base / "ontology-run/ontology-01.yaml",
        **{
            locator: ROOT / f"private/paper-v4-v4-{base_run}/producer/inputs" / filename
            for locator, filename in {
                "malleus": "malleus.yaml",
                "linkml:types": "linkml-types.yaml",
                "metrology": "metrology.yaml",
                "chronology": "chronology.yaml",
                "research": "research.yaml",
            }.items()
        },
    }
    if set(source_paths) != set(historical["source_closure_sha256"]):
        raise ValueError("selected ontology source closure differs")
    sources = {
        locator: checked_bytes(
            path.read_bytes(), historical["source_closure_sha256"][locator], locator
        )
        for locator, path in source_paths.items()
    }
    reading = checked_bytes(
        (ROOT / "private/paper-v4-text-layer/selected-reading.json").read_bytes(),
        historical["reading_sha256"],
        "selected reading",
    )
    compilation = api.compile_linkml_contract(
        root_locator="paper-v4-project", sources=sources
    )
    profile = api.SOURCE_ASSERTION_PROFILE.canonical_bytes
    surface = reference_module(
        "compile_ontology_candidate.py", base_run=base_run
    )._population_surface(compilation, json.loads(profile))
    surface_bytes = canonical(surface)
    query_program = load_query_program(query_path, query_identity)
    program = query_program._source_bytes
    questions = (
        ROOT / "paper-v4/experiment-v4/competency-questions-v3.json"
    ).read_bytes()
    query_binding = prepare_binding(
        surface_bytes, questions, core_commit, program, program=query_program
    )
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=api.STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    )
    coordinates = {
        "source_id": f"source:{run_id}:reading",
        "artifact_id": f"artifact:{run_id}:reading",
        "capture_id": f"capture:{run_id}:01",
        "plan_id": f"plan:{run_id}:01",
        "reading_sha256": digest(reading),
        "contract_identity": partial.identity,
        "capture_grammar": api.DOCUMENT_CAPTURE_GRAMMAR,
        "history_profile_identity": api.SOURCE_ASSERTION_PROFILE.identity,
    }
    producer_files = {
        "inputs/selected-reading.json": reading,
        "inputs/profile-source-assertion.json": profile,
        "inputs/population-surface.json": surface_bytes,
        "inputs/coordinates.json": canonical(coordinates),
        **{
            "inputs/"
            + (
                "ontology.yaml"
                if locator == "paper-v4-project"
                else source_paths[locator].name
            ): source
            for locator, source in sources.items()
        },
    }
    # Stage the whole identified skill folder, not an untracked installed copy.
    skill_root = ".claude/skills/malleus-acolyte/"
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", core_commit, skill_root],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if skill_root + "SKILL.md" not in listing:
        raise ValueError("Core coordinate has no acolyte skill")
    producer_files.update({path: git_bytes(core_commit, path) for path in listing})
    files = {"producer/" + name: value for name, value in producer_files.items()}
    task = (
        (HERE / "FOLLOWUP-PRODUCER.md")
        .read_text()
        .replace("<PRODUCER_WORKSPACE>", str(target / "producer"))
    )
    task += "\nDeclared input files, relative to the producer workspace:\n\n"
    task += "\n".join("- " + name for name in sorted(producer_files)) + "\n"
    files.update(
        {
            "producer-task.md": task.encode(),
            "query-binding.acceptance.json": query_binding,
            "competency-questions.json": questions,
            "validated-contract.json": compilation.artifact.artifact_bytes,
            **{
                "frozen-code/" + name: (HERE / name).read_bytes()
                for name in (
                    "binding.py",
                    "pilot.py",
                    "followup.py",
                    "capture.py",
                    "review_packet.py",
                )
            },
            "frozen-code/answers.py": program,
        }
    )
    tree = subprocess.run(
        ["git", "rev-parse", core_commit + "^{tree}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    manifest = {
        "schema": "malleus.paper-v4.fixed-ontology-followup/v1",
        "run_id": run_id,
        "base_ontology_run": base_run,
        "status": "STAGED_NOT_DISPATCHED",
        "staged_at": datetime.now(timezone.utc).isoformat(),
        "core_commit": core_commit,
        "core_tree": tree,
        "requested_model": "gpt-5.6-sol",
        "producer_condition": "FRESH_POPULATION_ONLY_FIXED_ONTOLOGY",
        "source_sha256": json.loads(reading)["source_sha256"],
        "reading_sha256": digest(reading),
        "ontology_sha256": digest(sources["paper-v4-project"]),
        "source_closure_sha256": {key: digest(value) for key, value in sources.items()},
        "query_binding_sha256": digest(query_binding),
        "contract_identity": partial.identity,
        "producer_inputs": sorted(producer_files),
        "materials": [
            {"path": name, "sha256": digest(value)}
            for name, value in sorted(files.items())
        ],
    }
    target.mkdir(parents=True)
    for name, value in files.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)
    (target / "manifest.json").write_bytes(canonical(manifest))
    verify_materials(target, manifest["materials"])
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-run", choices=["run-20", "run-21"], default="run-20")
    parser.add_argument("--run-id", default=RUN_ID)
    parser.add_argument("--query-identity", default=QUERY_IDENTITY)
    parser.add_argument("--query-path", type=Path, default=HERE / "answers.py")
    arguments = parser.parse_args()
    print(
        canonical(
            prepare(
                arguments.core_commit,
                arguments.output,
                base_run=arguments.base_run,
                run_id=arguments.run_id,
                query_identity=arguments.query_identity,
                query_path=arguments.query_path,
            )
        ).decode()
    )
