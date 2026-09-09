"""The E-0245 current-adoption gate, separate from frozen historical replication."""

import argparse
import ast
import json
from pathlib import Path
import re

from followup import checked_bytes, git_bytes, reference_module
from input_delivery import verify_delivery
import pilot
from review_packet import canonical, digest, new_private_directory


CORE = "160878cf14c0d27b11a440e26688708e9b7a7e2b"
TREE = "d946a7550dee247a371889f5eadf1cfecc964450"
SCHEMA = "malleus.paper-v4.current-adoption-inputs/v1"
SKILL = ".claude/skills/malleus-acolyte/SKILL.md"
SKILL_IDENTITY = (
    "sha256:ddc28bbc894dbcd5996bb668d2a72c1534070098394756144095b570c2eacb9d"
)
GUIDANCE = "tests/contract_compiler/pareto/test_capture_coverage_boundary.py"
GUIDANCE_IDENTITY = (
    "sha256:3a49d670fce7de4eb42da4e2d6b3d01b966cefd77fe88344c9f64308ccc02bf2"
)
BASE = pilot.ROOT / "paper-v4/experiment-v4/run-21"
SETTINGS = {
    "model_id": "gpt-5.6-sol",
    "reasoning_effort": "low",
    "session": "FRESH_SINGLE_SESSION",
}


def check_guidance(skill):
    source = checked_bytes(
        git_bytes(CORE, GUIDANCE), GUIDANCE_IDENTITY, "Core guidance check"
    )
    parsed = ast.parse(source, filename=GUIDANCE)
    # Execute only the existing pure guidance check and its label constant.
    # Do not import or run unrelated Core fixtures, and do not rewrite the check.
    nodes = [
        node
        for node in parsed.body
        if (isinstance(node, ast.FunctionDef) and node.name == "_assert_guidance")
        or (
            isinstance(node, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "LABELS" for t in node.targets)
        )
    ]
    scope = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), GUIDANCE, "exec"), scope)
    try:
        scope["_assert_guidance"](skill.decode("utf-8"))
    except AssertionError as error:
        raise ValueError("staged skill lacks accepted capture guidance") from error


def make_manifest(run_id):
    if not re.fullmatch(r"[a-z][a-z0-9-]*", run_id):
        raise ValueError("current-adoption run ID must be a safe lowercase identifier")
    manifest = json.loads((BASE / "producer-input-manifest.json").read_bytes())
    manifest.update(
        {
            "schema": SCHEMA,
            "run_id": run_id,
            "core": {"commit": CORE, "tree": TREE},
            "producer_workspace": f"private/paper-v4-answer-demonstration/{run_id}/producer",
            "decision": "E-0245",
            "condition": "CURRENT_ADOPTION_CORRECTED_GUIDANCE_AND_BOUNDED_DELIVERY",
            "interface_coordinates": {
                "capture_id": f"capture:paper-v4:{run_id}",
                "plan_id": f"plan:paper-v4:{run_id}",
                "source_id": "source:yu-2025-mid-atlantic-ridge",
            },
            "moved_since": {
                "reference_run": "run-21",
                "moved": ["MALLEUS_NASCENT_PROJECT_SKILL"],
                "delivery_change": "BOUNDED_EXACT_TOOL_OUTPUT_FRAMES",
            },
        }
    )
    manifest["producer"].update(
        {
            **SETTINGS,
            "kind": "CODEX_FRESH_SUBAGENT",
            "harness": "Codex collaboration.spawn_agent, fork_turns=none",
            "requested_model": "gpt-5.6-sol",
            "model_family": "GPT-5.6 Sol",
            "spawn_message": "ORIGINAL_TWO_PHASE_TASK_PLUS_ADMINISTRATIVE_DELIVERY_APPENDIX",
        }
    )
    for item in manifest["declared_inputs"]:
        if item["target"] == SKILL:
            item["sha256"] = SKILL_IDENTITY
    return manifest


def input_bytes(manifest):
    return {
        item["target"]: (pilot.ROOT / item["source"]).read_bytes()
        if item["name"] == "SELECTED_READING"
        else git_bytes(manifest["core"]["commit"], item["source"])
        for item in manifest["declared_inputs"]
    }


def verify_inputs(manifest, files):
    if manifest["schema"] != SCHEMA or manifest["core"] != {
        "commit": CORE,
        "tree": TREE,
    }:
        raise ValueError("packet is not the selected current-adoption Core condition")
    expected = make_manifest(manifest["run_id"])
    if manifest["declared_inputs"] != expected["declared_inputs"]:
        raise ValueError("declared input condition differs from E-0245")
    if set(files) != {item["target"] for item in expected["declared_inputs"]}:
        raise ValueError(
            "current-adoption input closure must be the exact eight inputs"
        )
    for key, value in SETTINGS.items():
        if manifest["producer"][key] != value:
            raise ValueError(f"producer setting differs from selected condition: {key}")
    for item in expected["declared_inputs"]:
        checked_bytes(files[item["target"]], item["sha256"], item["target"])
    check_guidance(files[SKILL])


def verify_packet(run):
    manifest = json.loads((run / "producer-input-manifest.json").read_bytes())
    files = {
        str(p.relative_to(run / "producer")): p.read_bytes()
        for folder in ("inputs", ".claude")
        for p in (run / "producer" / folder).rglob("*")
        if p.is_file()
    }
    verify_inputs(manifest, files)
    verify_control_files(run)
    pilot.verify_runtime(CORE)
    return manifest


def verify_control_files(run):
    check = json.loads((run / "staging-check.json").read_bytes())
    for name, key in (
        ("input_delivery.py", "delivery_helper_sha256"),
        ("spawn-message.md", "spawn_message_sha256"),
    ):
        checked_bytes((run / name).read_bytes(), check[key], name)


def verify_observed(run, phase):
    verify_packet(run)
    launch = json.loads((run / "launch.json").read_bytes())
    if (launch["model"], launch["reasoning_effort"]) != (
        SETTINGS["model_id"],
        SETTINGS["reasoning_effort"],
    ):
        raise ValueError("producer setting differs from selected condition")
    return verify_delivery(run, phase)


def prepare(run_id, output):
    output = new_private_directory(output, pilot.ROOT / "private")
    manifest = make_manifest(run_id)
    files = input_bytes(manifest)
    verify_inputs(manifest, files)
    pilot.verify_runtime(CORE)
    preparer = reference_module("prepare_producer.py", base_run="run-21")
    preparer.preflight()
    manifest_path = output / "producer-input-manifest.json"
    output.mkdir(parents=True)
    manifest_path.write_bytes(canonical(manifest))
    preparer.MANIFEST = manifest_path
    preparer.prepare(
        pilot.ROOT / "private/paper-v4-text-layer/selected-reading.json",
        output / "producer",
    )
    helper = output / "input_delivery.py"
    helper.write_bytes(Path(__file__).with_name("input_delivery.py").read_bytes())
    task = (
        (BASE / "spawn-message.md")
        .read_text()
        .replace("run-21", run_id)
        .replace("<PRODUCER_WORKSPACE>", str(output / "producer"))
    )
    appendix = f"""\n\nAdministrative input delivery, not modelling guidance. Before writing an ontology,
read every part of every initial input using the read-only helper below. It prints
exact bounded frames from the same eight declared files; it supplies no other data.
First list the targets and part counts:
`/Users/luis/Projects/malleus-dev/.venv/bin/python {helper} --run {output} --phase initial`
Then invoke that command separately for each part, adding `--target TARGET --part N`.
Read the skill completely first, then the selected reading, then the remaining
inputs. Use one command per tool result with an output budget of at least 9000
tokens. Do not batch frame outputs into a response that may truncate. If any
frame is truncated, read it again before continuing. After acceptance, use
`--phase accepted` in the same way for both accepted files. This helper is the
only additional allowed infrastructure path; do not inspect its source, the run
directory, or undeclared material. Input delivery will be checked against the
actual tool outputs. No self-reported read receipt replaces those outputs.
"""
    (output / "spawn-message.md").write_text(task + appendix)
    (output / "staging-check.json").write_bytes(
        canonical(
            {
                "status": "VERIFIED",
                "core": manifest["core"],
                "guidance_check_sha256": GUIDANCE_IDENTITY,
                "delivery_helper_sha256": digest(helper.read_bytes()),
                "spawn_message_sha256": digest((task + appendix).encode()),
                "condition": manifest["condition"],
                "limit": "Not semantic success or proof of model comprehension.",
            }
        )
    )
    return manifest


def gate(run, attempt):
    observed = verify_observed(run, "initial")
    module = reference_module("compile_ontology_candidate.py", base_run="run-21")
    module.MANIFEST = run / "producer-input-manifest.json"
    accepted = module.compile_candidate(
        ontology_path=run / "producer/work" / f"ontology-attempt-{attempt:02d}.yaml",
        producer_root=run / "producer",
        output=run / "gate" / f"attempt-{attempt:02d}",
        attempt=attempt,
    )
    (run / "gate" / f"attempt-{attempt:02d}" / "input-delivery.json").write_bytes(
        canonical(observed)
    )
    return accepted


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("prepare", "gate", "verify"))
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--attempt", type=int)
    parser.add_argument("--phase", choices=("initial", "accepted"))
    args = parser.parse_args()
    if args.action == "prepare":
        print(canonical(prepare(args.run.name, args.run)).decode())
    elif args.action == "gate" and args.attempt in (1, 2, 3):
        print(json.dumps({"accepted": gate(args.run, args.attempt)}))
    elif args.action == "verify" and args.phase is not None:
        print(canonical(verify_observed(args.run, args.phase)).decode())
    else:
        parser.error("gate needs attempt 1..3; verify needs a phase")
