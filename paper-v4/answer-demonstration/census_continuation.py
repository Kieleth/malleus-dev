"""One question-withheld continuation, using the existing public capture runner."""

import argparse
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path

from current_adoption import verify_observed
from followup import checked_bytes, reference_module, verify_materials
from input_delivery import input_frames, transcript_evidence, verify_frames
from ontology_query import method_inputs
import pilot
from review_packet import canonical, digest, new_private_directory


TASK = """# One census-guided capture continuation

This continues your own accepted ontology and your own first population. It is
not a fresh session. The ontology, source reading, packs, skill and model setting
are unchanged. Your first population was structurally admitted, not certified
as faithful or complete. The exact census and your prior population are supplied.

Make one whole-source pass. Use the census as a worklist: inspect the untreated
source blocks and reconsider your own nothing_assertable classifications. Read
the surrounding source when a proposition or reference spans blocks. Capture
source-supported domain content under your accepted ontology, preserving scope,
units, attribution and uncertainty. Check that your records carry the proposition
or observation they claim to formalize, not merely a category or assertion label.
Retain source-supported relationships where the accepted ontology expresses
them; a relationship requires source evidence, not co-occurrence. No minimum
record or relation count is required. Do not turn a hypothesis into established
truth or invent facts to increase the census. A ledger-admitted record is not
evidence that its semantic interpretation is correct.

Return a complete consolidated population in work/candidate-01.json with exactly
capture, records and supersessions. Retain or correct your prior records only
where the source warrants them, and include all new records in this same complete
file. It will be evaluated in a separate from-empty history, not appended to the
first history; supersessions must be empty. Use the same capture grammar and
source identity as before. Each value and endpoint needs a source-located
formalized_by path. Do not change the ontology, compiled surface or input files.
Do not run admission or fabricate successful check outcomes.

Write work/coverage-note.md recording what you revisited, what remains untreated,
and the concrete source or representation limits. Declare only justified gaps.
UNTOUCHED remains honest for work not completed; never mark a substantive block
nothing_assertable merely because it was difficult. If you cannot make a faithful
revision, write work/refusal.md with evidence and stop instead of inventing one.
This condition has one semantic-feedback round. The coordinator can return at
most two exact structural diagnostics, not semantic grades or answer hints.

Read only your producer packet and the designated read-only delivery helper.
Do not read questions, query code, answers, scores or reviews, other runs, parent
reports, network sources or repository files. No delegation. You are not alone
in the workspace; write only this packet's work directory. Use apply_patch.
Do not alter your original workspace or any git state. No commit, push or refs.
"""

INPUTS = {
    "inputs/selected-reading.json",
    "inputs/malleus.yaml",
    "inputs/linkml-types.yaml",
    "inputs/metrology.yaml",
    "inputs/chronology.yaml",
    "inputs/research.yaml",
    "inputs/profile-source-assertion.json",
    ".claude/skills/malleus-acolyte/SKILL.md",
    "accepted/ontology.yaml",
    "accepted/population-surface.json",
    "feedback/census.json",
    "feedback/prior-population.json",
    "TASK.md",
}
FEEDBACK = ("TASK.md", "feedback/census.json", "feedback/prior-population.json")


def check_producer_files(files):
    if set(files) != INPUTS:
        raise ValueError("producer input closure differs from question-withheld packet")
    if files["TASK.md"] != TASK.encode():
        raise ValueError("feedback task differs from the selected condition")


def producer_files(base):
    initial = json.loads((base / "producer-input-manifest.json").read_bytes())
    manifest = json.loads((base / "manifest.json").read_bytes())
    files = {
        item["target"]: checked_bytes(
            (base / "producer" / item["target"]).read_bytes(),
            item["sha256"],
            item["target"],
        )
        for item in initial["declared_inputs"]
    }
    files.update(
        {
            "accepted/ontology.yaml": checked_bytes(
                (base / manifest["ontology_path"]).read_bytes(),
                manifest["ontology_sha256"],
                "own ontology",
            ),
            "accepted/population-surface.json": (
                base / "producer/accepted/population-surface.json"
            ).read_bytes(),
            "feedback/census.json": (
                base / "attempt-01/public/census.json"
            ).read_bytes(),
            "feedback/prior-population.json": (
                base / "attempt-01/submitted-population.json"
            ).read_bytes(),
            "TASK.md": TASK.encode(),
        }
    )
    check_producer_files(files)
    return files


def stage(base, run):
    if (run / "manifest.json").exists() or (run / "producer").exists():
        raise ValueError("refusing to overwrite a continuation packet")
    verify_observed(base, "initial")
    verify_observed(base, "accepted")
    method, _ = method_inputs(run / "query-method")
    original = json.loads((base / "manifest.json").read_bytes())
    files = producer_files(base)
    for name, data in files.items():
        path = run / "producer" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (run / "producer/work").mkdir()
    initial = {
        "declared_inputs": [
            {"target": name, "sha256": digest(data)} for name, data in files.items()
        ]
    }
    (run / "producer-input-manifest.json").write_bytes(canonical(initial))
    helper = Path(__file__).with_name("input_delivery.py").read_bytes()
    (run / "input_delivery.py").write_bytes(helper)
    runner = reference_module("run.py", base_run="run-21")
    runner_bytes = (
        Path(runner.__file__).read_bytes().replace(b"run-21", run.name.encode())
    )
    (run / "public-runner.py").write_bytes(runner_bytes)
    (run / "census_continuation.py").write_bytes(Path(__file__).read_bytes())
    manifest = {
        **original,
        "run_id": run.name,
        "producer_condition": "CENSUS_GUIDED_CONTINUATION",
        "base_run": str(base),
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "ontology_path": "producer/accepted/ontology.yaml",
        "text_binding_sha256": digest((run / "query-method/method.json").read_bytes()),
        "interface_coordinates": {
            "capture_id": "capture:paper-v4:" + run.name,
            "plan_id": "plan:paper-v4:" + run.name,
            "source_id": original["interface_coordinates"]["source_id"],
        },
        "materials": [
            {"path": "producer/" + name, "sha256": digest(data)}
            for name, data in files.items()
        ]
        + [
            {"path": name, "sha256": digest((run / name).read_bytes())}
            for name in (
                "producer-input-manifest.json",
                "input_delivery.py",
                "public-runner.py",
                "census_continuation.py",
            )
        ],
    }
    # This is not acceptance of a new ontology or the historical query program.
    for key in ("accepted_at", "query_binding_sha256", "query_program_sha256"):
        del manifest[key]
    if method["ontology_sha256"] != manifest["ontology_sha256"]:
        raise ValueError("query method and continuation ontology differ")
    (run / "manifest.json").write_bytes(canonical(manifest))
    return manifest


def verify(run, *, observed):
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    checked_bytes(
        Path(__file__).read_bytes(),
        digest((run / "census_continuation.py").read_bytes()),
        "loaded continuation executor",
    )
    method_inputs(run / "query-method")
    checked_bytes(
        (run / "query-method/method.json").read_bytes(),
        manifest["text_binding_sha256"],
        "pre-continuation query binding",
    )
    actual = {
        str(p.relative_to(run / "producer")): p.read_bytes()
        for p in (run / "producer").rglob("*")
        if p.is_file() and not p.is_relative_to(run / "producer/work")
    }
    check_producer_files(actual)
    pilot.verify_runtime(manifest["core_commit"])
    if observed:
        dispatch = json.loads((run / "dispatch.json").read_bytes())
        base = Path(manifest["base_run"])
        launch = json.loads((base / "launch.json").read_bytes())
        if dispatch["thread_id"] != launch["thread_id"]:
            raise ValueError("continuation producer changed")
        rows = [
            json.loads(line)
            for line in Path(launch["metadata_source"]).read_text().splitlines()
        ]
        outputs = transcript_evidence(rows, launch)
        frames = input_frames(run, "initial")
        verify_frames([frame for name in FEEDBACK for frame in frames[name]], outputs)
    return manifest


def execute(run, candidate, output, transaction_time):
    manifest = verify(run, observed=True)
    target = new_private_directory(output, pilot.ROOT / "private")
    if not target.is_relative_to(run):
        raise ValueError("attempt must remain inside the continuation run")
    target.mkdir(parents=True)
    submitted = candidate.read_bytes()
    (target / "submitted-population.json").write_bytes(submitted)
    spec = importlib.util.spec_from_file_location(
        "census_public_runner", run / "public-runner.py"
    )
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    sources = [["paper-v4-project", str(run / manifest["ontology_path"])]] + [
        [key, str(run / "producer/inputs" / name)]
        for key, name in {
            "malleus": "malleus.yaml",
            "linkml:types": "linkml-types.yaml",
            "metrology": "metrology.yaml",
            "chronology": "chronology.yaml",
            "research": "research.yaml",
        }.items()
    ]
    for key, name in sources:
        checked_bytes(
            Path(name).read_bytes(), manifest["source_closure_sha256"][key], key
        )
    try:
        result = runner.execute(
            argparse.Namespace(
                root="paper-v4-project",
                source=sources,
                reading=str(run / "producer/inputs/selected-reading.json"),
                population=str(target / "submitted-population.json"),
                **manifest["interface_coordinates"],
                artifact_id="artifact:" + run.name + ":reading",
                ledger=str(target / "ledger/history.jsonl"),
                results=str(target / "public"),
                transaction_time=transaction_time,
                actor_id="actor:codex:" + run.name,
            )
        )
        result.update(
            condition="CENSUS_GUIDED_CONTINUATION", core_commit=manifest["core_commit"]
        )
    except (ValueError, TypeError, OSError) as error:
        result = {
            "status": "REFUSED",
            "condition": "CENSUS_GUIDED_CONTINUATION",
            "cause_chain": reference_module(
                "compile_ontology_candidate.py", base_run="run-21"
            )._cause_chain(error),
        }
    (target / "run-result.json").write_bytes(canonical(result))
    verify(run, observed=True)
    return result
