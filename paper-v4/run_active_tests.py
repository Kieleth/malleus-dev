from __future__ import annotations

import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = Path(__file__).with_name("active-test-manifest.json")
COMMIT = re.compile(r"[0-9a-f]{40}")


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


def export_core(commit: str, root: Path) -> Path:
    """Export ``src/malleus`` at ``commit`` from this repository's history into ``root``.

    A frozen paper run replays only against the Core it was produced with, and
    the pin is a commit that git already holds, so nothing is tracked twice and
    no path outside the repository becomes an input to the gate.
    """
    if not COMMIT.fullmatch(commit):
        raise ValueError(f"Core pin requires a full commit identity: {commit}")
    archive = subprocess.run(
        ["git", "archive", "--format=tar", commit, "src/malleus"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(root, filter="data")
    return root / "src"


def plan(
    manifest: dict[str, object], paths: list[str], *, export_root: Path
) -> list[dict[str, object]]:
    """Partition the active paths into one pytest run per Core pin plus the rest."""
    base = [str((ROOT / value).resolve()) for value in manifest["pythonpath"]]
    groups: list[dict[str, object]] = []
    taken: set[str] = set()
    for pin in manifest.get("core_pins", []):
        commit = pin["commit"]
        if not COMMIT.fullmatch(commit):
            raise ValueError(f"Core pin requires a full commit identity: {commit}")
        wanted = set(pin["paths"])
        missing = wanted - set(paths)
        if missing:
            raise ValueError(f"Core pin names paths outside the manifest: {sorted(missing)}")
        pinned = [value for value in paths if value in wanted]
        taken |= wanted
        pythonpath = [
            str(export_root / commit / "src"),
            *(str((ROOT / value).resolve()) for value in pin["pythonpath"]),
            *base,
        ]
        groups.append({"pin": commit, "paths": pinned, "pythonpath": pythonpath})
    groups.append(
        {"pin": None, "paths": [value for value in paths if value not in taken], "pythonpath": base}
    )
    return groups


def main() -> int:
    manifest, paths = load_active_paths()
    status = 0
    with tempfile.TemporaryDirectory(prefix="malleus-core-pin-") as tmp:
        export_root = Path(tmp)
        for group in plan(manifest, paths, export_root=export_root):
            if not group["paths"]:
                continue
            if group["pin"]:
                export_core(group["pin"], export_root / group["pin"])
            environment = dict(os.environ)
            environment["PYTHONPATH"] = os.pathsep.join(group["pythonpath"])
            command = [
                sys.executable,
                "-m",
                "pytest",
                *manifest["pytest_args"],
                *group["paths"],
                *sys.argv[1:],
            ]
            status = subprocess.call(command, cwd=ROOT, env=environment) or status
    return status


if __name__ == "__main__":
    raise SystemExit(main())
