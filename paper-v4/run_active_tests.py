from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path(__file__).with_name("active-test-manifest.json")


def _inside(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def load_active_paths() -> tuple[dict[str, object], list[str]]:
    manifest = json.loads(MANIFEST_PATH.read_bytes())
    if manifest["schema"] != "malleus.paper-v4.active-test-manifest/v1":
        raise ValueError("unsupported active-test manifest schema")

    excluded = [(ROOT / value).resolve() for value in manifest["excluded_roots"]]
    paths: list[str] = []
    for value in manifest["paths"]:
        candidate = (ROOT / value).resolve()
        if not _inside(candidate, ROOT):
            raise ValueError(f"active-test path escapes repository: {value}")
        if any(_inside(candidate, blocked) for blocked in excluded):
            raise ValueError(f"active-test path enters excluded history: {value}")
        if not candidate.exists():
            raise FileNotFoundError(f"active-test path is missing: {value}")
        paths.append(value)
    return manifest, paths


def main() -> int:
    manifest, paths = load_active_paths()
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        str((ROOT / value).resolve()) for value in manifest["pythonpath"]
    )
    command = [
        sys.executable,
        "-m",
        "pytest",
        *manifest["pytest_args"],
        *paths,
        *sys.argv[1:],
    ]
    return subprocess.call(command, cwd=ROOT, env=environment)


if __name__ == "__main__":
    raise SystemExit(main())
