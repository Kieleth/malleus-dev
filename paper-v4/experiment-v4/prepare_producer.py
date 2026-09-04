from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).with_name("producer-input-manifest.json")


class ProducerPreparationRefusal(ValueError):
    pass


def _digest(data: bytes) -> str:
    return "sha256:" + sha256(data).hexdigest()


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _prune_skill_tree(skill_root: Path, allowed: set[Path]) -> None:
    for path in sorted(skill_root.rglob("*"), reverse=True):
        if path.is_file() or path.is_symlink():
            if path.resolve() not in allowed:
                path.unlink()
        elif path.is_dir() and not any(path.iterdir()):
            path.rmdir()


def prepare(reading: Path, output: Path) -> dict[str, object]:
    manifest = json.loads(MANIFEST.read_bytes())
    private_root = (ROOT / "private").resolve()
    output = output.resolve()
    if output == private_root or not _inside(output, private_root):
        raise ProducerPreparationRefusal("producer output must be below private/")
    if output.exists():
        raise ProducerPreparationRefusal("producer output already exists")

    sources: dict[str, bytes] = {}
    for item in manifest["declared_inputs"]:
        source = (
            reading if item["name"] == "SELECTED_READING" else ROOT / item["source"]
        )
        data = source.read_bytes()
        if _digest(data) != item["sha256"]:
            raise ProducerPreparationRefusal(
                f"declared input digest mismatch: {item['name']}"
            )
        sources[item["name"]] = data

    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    subprocess.run(
        [
            sys.executable,
            "-m",
            "malleus.inquisition.cli",
            "install-skills",
            "--agent",
            "codex",
            "--project",
            str(output),
        ],
        cwd=ROOT,
        check=True,
    )

    declared_targets: set[Path] = set()
    for item in manifest["declared_inputs"]:
        target = output / item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(sources[item["name"]])
        declared_targets.add(target.resolve())

    _prune_skill_tree(output / ".codex" / "skills", declared_targets)
    actual = {
        path.resolve()
        for path in output.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual != declared_targets:
        raise ProducerPreparationRefusal("producer input closure is not exact")

    receipt = {
        "schema": "malleus.paper-v4.producer-input-receipt/v1",
        "core": manifest["core"],
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
