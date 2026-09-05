"""Build the run-10 producer workspace from the bytes at the recorded commit.

Core is expected to change the skill and the packs on main while this run is
open. A run's declared inputs are the bytes its producer consumed, so every
tracked input is read with ``git show <core commit>:<path>`` and never from the
working tree; the skill is installed by writing those bytes to the Claude path
rather than by running the installer against a tree that may have moved. The
selected reading is untracked and is read from its private path. Every input is
checked against the manifest digest, and the resulting file set must equal the
declared targets exactly.

Before any of that, the builder refuses unless it is executing on the
repository ``.venv`` interpreter with the ``linkml`` and ``linkml-runtime``
versions the paper environment lock names, and records that check in the
receipt.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from importlib import metadata
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = Path(__file__).with_name("producer-input-manifest.json")
UNTRACKED_INPUTS = {"SELECTED_READING"}
VENV = ROOT / ".venv"
ENVIRONMENT_LOCK = ROOT / "paper-v4/environment/requirements-cp312-macos-arm64.lock"
PINNED_PACKAGES = ("linkml", "linkml-runtime")
PINNED_LINE = re.compile(r"^(?P<name>[A-Za-z0-9_.-]+)==(?P<version>[^\s\\]+)")


class ProducerPreparationRefusal(ValueError):
    pass


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _locked_versions() -> dict[str, str]:
    """The compiler versions the paper environment lock names, by package."""
    versions: dict[str, str] = {}
    for line in ENVIRONMENT_LOCK.read_text(encoding="utf-8").splitlines():
        match = PINNED_LINE.match(line)
        if match is None:
            continue
        name = match.group("name").lower().replace("_", "-")
        if name in PINNED_PACKAGES:
            versions[name] = match.group("version")
    absent = [name for name in PINNED_PACKAGES if name not in versions]
    if absent:
        raise ProducerPreparationRefusal(
            f"the environment lock names no version for: {', '.join(absent)}"
        )
    return versions


def preflight() -> dict[str, object]:
    """Refuse before a workspace exists if the interpreter is not the pinned one.

    A run launched from the wrong interpreter spends the producer's whole
    ontology phase and only then refuses at the gate, which the base conda
    python at ``linkml-runtime`` 1.10.0 did (deep sweep D-10). The check reads
    the environment lock rather than restating a version.
    """
    prefix = Path(sys.prefix).resolve()
    required = VENV.resolve()
    if prefix != required:
        raise ProducerPreparationRefusal(
            f"the harness runs on {required}; this interpreter is {prefix}"
        )
    locked = _locked_versions()
    installed: dict[str, str] = {}
    for name in PINNED_PACKAGES:
        try:
            installed[name] = metadata.version(name)
        except metadata.PackageNotFoundError as error:
            raise ProducerPreparationRefusal(
                f"{name} is not installed on {prefix}"
            ) from error
        if installed[name] != locked[name]:
            raise ProducerPreparationRefusal(
                f"{name} is {installed[name]} on {prefix};"
                f" the environment lock names {locked[name]}"
            )
    return {
        "checked": "INTERPRETER_AND_LOCKED_COMPILER_VERSIONS",
        "environment_lock": str(ENVIRONMENT_LOCK.relative_to(ROOT)),
        "environment_lock_sha256": _digest(ENVIRONMENT_LOCK.read_bytes()),
        "executable": sys.executable,
        "installed_versions": installed,
        "locked_versions": locked,
        "prefix": str(prefix),
        "required_prefix": str(required),
        "status": "VERIFIED",
    }


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _git_show(commit: str, path: str) -> bytes:
    """The tracked bytes at ``commit``, or a refusal naming what is missing."""
    completed = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        capture_output=True,
        cwd=ROOT,
    )
    if completed.returncode != 0:
        raise ProducerPreparationRefusal(
            f"declared input is not readable at {commit}: {path}"
            f" ({completed.stderr.decode(errors='replace').strip()})"
        )
    return completed.stdout


def prepare(reading: Path, output: Path) -> dict[str, object]:
    interpreter = preflight()
    manifest = json.loads(MANIFEST.read_bytes())
    commit = manifest["core"]["commit"]
    private_root = (ROOT / "private").resolve()
    output = output.resolve()
    if output == private_root or not _inside(output, private_root):
        raise ProducerPreparationRefusal("producer output must be below private/")
    if output.exists():
        raise ProducerPreparationRefusal("producer output already exists")

    sources: dict[str, bytes] = {}
    for item in manifest["declared_inputs"]:
        data = (
            reading.read_bytes()
            if item["name"] in UNTRACKED_INPUTS
            else _git_show(commit, item["source"])
        )
        if _digest(data) != item["sha256"]:
            raise ProducerPreparationRefusal(
                f"declared input digest mismatch: {item['name']}"
            )
        sources[item["name"]] = data

    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    declared_targets: set[Path] = set()
    for item in manifest["declared_inputs"]:
        target = output / item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(sources[item["name"]])
        declared_targets.add(target.resolve())

    actual = {
        path.resolve()
        for path in output.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual != declared_targets:
        raise ProducerPreparationRefusal("producer input closure is not exact")

    receipt = {
        "schema": "malleus.paper-v4.producer-input-receipt/v1",
        "run_id": manifest["run_id"],
        "core": manifest["core"],
        "input_bytes": manifest["input_bytes"],
        "interpreter": interpreter,
        "producer": manifest["producer"],
        "files": [
            {
                "name": item["name"],
                "path": item["target"],
                "sha256": _digest((output / item["target"]).read_bytes()),
            }
            for item in manifest["declared_inputs"]
        ],
        "manifest_sha256": _digest(MANIFEST.read_bytes()),
        "status": "FROZEN",
    }
    receipt_path = output.parent / "producer-input-receipt.json"
    receipt_path.write_bytes(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode() + b"\n"
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reading", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    prepare(args.reading, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
