"""Freeze the approved two-arm packet; reuse capture and observed-delivery gates."""

import argparse
import json
from pathlib import Path

import capture
from current_adoption import CORE, TREE
from followup import checked_bytes, verify_materials
from input_delivery import verify_delivery
import pilot
from review_packet import canonical, digest, new_private_directory


HERE = Path(__file__).resolve().parent
BASE = pilot.ROOT / "private/paper-v4-answer-demonstration/followup-sol-01"
BASE_ID = "sha256:bd22c14b6b47e1cad22cd9603cb5182586f4f117ed9d3cac167971374117666c"
ARMS = {"a": "low", "b": "ultra"}
INFRASTRUCTURE = (
    "binding.py",
    "pilot.py",
    "followup.py",
    "capture.py",
    "review_packet.py",
)


def baseline():
    value = json.loads(
        checked_bytes(
            (BASE / "manifest.json").read_bytes(), BASE_ID, "baseline manifest"
        )
    )
    verify_materials(BASE, value["materials"])
    if (value["core_commit"], value["core_tree"]) != (CORE, TREE):
        raise ValueError("calibration Core differs")
    return value


def packet_files(run):
    original = baseline()
    files = {
        entry["path"]: (BASE / entry["path"]).read_bytes()
        for entry in original["materials"]
    }
    files.update(
        {"frozen-code/" + name: (HERE / name).read_bytes() for name in INFRASTRUCTURE}
    )
    task = (
        files["producer-task.md"]
        .decode()
        .replace(str(BASE / "producer"), str(run / "producer"))
    )
    task += f"""\nAdministrative input delivery, not modelling guidance. Before authoring a
population, read every part of every declared input using the read-only helper.
First list targets and counts:
`/Users/luis/Projects/malleus-dev/.venv/bin/python {run}/input_delivery.py --run {run} --phase initial`
Then invoke it separately for each part, adding `--target TARGET --part N`.
Read the skill completely first, then the selected reading, then all remaining
inputs. Use one command per tool output, with at least 9000 output tokens. Do
not batch frames into one response that may truncate. Re-read any truncated
frame. This helper is the only extra allowed infrastructure path. Do not inspect
its source, the run directory or undeclared material. Actual tool outputs will
be checked; a self-reported read receipt cannot replace them.
"""
    files["producer-task.md"] = task.encode()
    files["input_delivery.py"] = (HERE / "input_delivery.py").read_bytes()
    files["calibration.py"] = Path(__file__).read_bytes()
    files["producer-input-manifest.json"] = canonical(
        {
            "declared_inputs": [
                {"target": name, "sha256": digest(files["producer/" + name])}
                for name in original["producer_inputs"]
            ]
        }
    )
    return files


def check_files(run, files):
    expected = packet_files(run)
    if set(files) != set(expected):
        raise ValueError("calibration material closure differs")
    for name, data in expected.items():
        if files[name] != data:
            raise ValueError(f"calibration input differs: {name}")


def check_launch(arm, launch):
    if (launch["model"], launch["reasoning_effort"], launch["fork_turns"]) != (
        "gpt-5.6-sol",
        ARMS[arm],
        "none",
    ):
        raise ValueError("producer does not match explicit calibration settings")


def stage(root):
    root = new_private_directory(root, pilot.ROOT / "private")
    original = baseline()
    pilot.verify_runtime(CORE)
    for arm, effort in ARMS.items():
        run = root / arm
        files = packet_files(run)
        for name, data in files.items():
            path = run / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (run / "producer/work").mkdir()
        manifest = {
            **original,
            "status": "FROZEN_NOT_DISPATCHED",
            "decision": "E-0250",
            "calibration_arm": arm,
            "requested_effort": effort,
            "baseline_manifest_sha256": BASE_ID,
            "materials": [
                {"path": name, "sha256": digest(data)}
                for name, data in sorted(files.items())
            ],
        }
        (run / "manifest.json").write_bytes(canonical(manifest))
    return {arm: verify(root / arm, observed=False)["requested_effort"] for arm in ARMS}


def verify(run, *, observed):
    manifest = json.loads((run / "manifest.json").read_bytes())
    if (
        manifest["calibration_arm"] != run.name
        or manifest["requested_effort"] != ARMS[run.name]
    ):
        raise ValueError("calibration arm differs")
    original = baseline()
    for key in original:
        if key not in {"materials", "status"} and manifest[key] != original[key]:
            raise ValueError(f"calibration baseline coordinate differs: {key}")
    verify_materials(run, manifest["materials"])
    files = {
        entry["path"]: (run / entry["path"]).read_bytes()
        for entry in manifest["materials"]
    }
    check_files(run, files)
    producer = {
        "producer/" + str(path.relative_to(run / "producer"))
        for path in (run / "producer").rglob("*")
        if path.is_file() and not path.is_relative_to(run / "producer/work")
    }
    if producer != {"producer/" + name for name in original["producer_inputs"]}:
        raise ValueError("calibration producer closure differs")
    pilot.verify_runtime(CORE)
    if observed:
        launch = json.loads((run / "launch.json").read_bytes())
        check_launch(run.name, launch)
        verify_delivery(run, "initial")
    return manifest


def execute(run, population, output, *, transaction_time):
    verify(run, observed=True)
    return capture.execute(run, population, output, transaction_time=transaction_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "verify", "execute"))
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--population", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--transaction-time")
    args = parser.parse_args()
    if args.action == "stage":
        result = stage(args.run)
    elif args.action == "verify":
        result = verify(args.run, observed=True)
    else:
        result = execute(
            args.run,
            args.population,
            args.output,
            transaction_time=args.transaction_time,
        )
    print(canonical(result).decode())
