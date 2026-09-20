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


CORE_TREES = ("src/malleus", "ontology")


def export_core(commit: str, root: Path) -> Path:
    """Export Core at ``commit`` from this repository's history into ``root``.

    A frozen paper run replays only against the Core it was produced with, and
    the pin is a commit that git already holds, so nothing is tracked twice and
    no path outside the repository becomes an input to the gate.

    Core is the package and the ontology it ships beside it:
    ``bundled_ontology_path`` reads ``<root>/ontology`` before any installed
    copy, so a package-only export refuses every bundled profile as soon as a
    pinned group loads one in process.
    """
    if not COMMIT.fullmatch(commit):
        raise ValueError(f"Core pin requires a full commit identity: {commit}")
    archive = subprocess.run(
        ["git", "archive", "--format=tar", commit, *CORE_TREES],
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
    for group in groups:
        group["ignore"] = _swept_from_other_groups(group["paths"], paths)
    return groups


def _swept_from_other_groups(group_paths: list[str], paths: list[str]) -> list[str]:
    """Paths of other groups that this group's directory entries would sweep in.

    A cell can be named by a Core pin and still sit under a directory entry the
    unpinned partition collects, and pytest would then run it twice, once
    against the wrong Core. The group that does not own the path ignores it.
    """
    roots = [(ROOT / value).resolve() for value in group_paths]
    mine = set(group_paths)
    return [
        value
        for value in paths
        if value not in mine
        and any(_inside((ROOT / value).resolve(), root) for root in roots)
    ]


def pytest_command(
    manifest: dict[str, object], group: dict[str, object], extra: list[str]
) -> list[str]:
    """Build the pytest invocation for one planned group.

    pytest inserts pyproject's ``pythonpath`` at the front of ``sys.path``,
    ahead of everything the runner puts on PYTHONPATH, so a pinned module that
    imported Core while it was being collected got the checkout's
    ``src/malleus`` and the pin bound only in the tests that shell out
    (E-0434). A pinned group replaces that ini value with its own import path,
    the export first, so the pin holds in process as well.
    """
    options: list[str] = []
    if group["pin"]:
        entries = [str(value) for value in group["pythonpath"]]
        spaced = [value for value in entries if re.search(r"\s", value)]
        if spaced:
            raise ValueError(f"a pinned import path cannot contain whitespace: {spaced}")
        options += ["-o", "pythonpath=" + " ".join(entries)]
    options += [f"--ignore={(ROOT / value).resolve()}" for value in group["ignore"]]
    return [
        sys.executable,
        "-m",
        "pytest",
        *manifest["pytest_args"],
        *options,
        *group["paths"],
        *extra,
    ]


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
            command = pytest_command(manifest, group, list(sys.argv[1:]))
            status = subprocess.call(command, cwd=ROOT, env=environment) or status
    return status


if __name__ == "__main__":
    raise SystemExit(main())
