"""Every tracked source module must reach the packaged distributions.

``pyproject.toml`` names each packaged file one by one under
``[tool.hatch.build] include``. Three modules ``malleus.compiler`` imports
reached main without joining that list, and no suite saw it, because every
suite runs from the tree and the only gate that opens a built distribution,
``scripts/ci.py package``, runs on a release tag and not on a push.

What the list governs was measured, not assumed. Hatchling appends every entry
of a target's ``packages`` to that target's include patterns, in the
``include_spec`` property of ``hatchling/builders/config.py``. The wheel target
sets ``packages = ["src/malleus"]``, so ``/src/malleus/`` joins the wheel's
include set and the wheel ships the whole package directory whatever the list
says: a scratch module dropped into ``src/malleus`` was measured into the wheel
and absent from the sdist. The sdist target declares no ``packages``, so the
list is the sdist's entire include set. The sdist is the artifact an unlisted
module breaks, and the wheel rebuilt from that sdist is what
``scripts/ci.py package-parity`` compares.

The static check asks hatchling's own sdist builder which files it would take,
so a missing line is named without a build and without a second matcher here.
The two build checks observe the built artifact, because a projection of the
manifest is not the distribution.
"""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tomllib
import zipfile

from hatchling.builders.sdist import SdistBuilder
import pytest


ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = ROOT / "pyproject.toml"
PACKAGE_ROOT = "src/malleus/"


def _tracked(*arguments: str) -> tuple[str, ...]:
    listed = subprocess.run(
        ["git", "ls-files", "-z", *arguments],
        cwd=ROOT,
        capture_output=True,
        check=True,
        text=True,
    ).stdout
    return tuple(entry for entry in listed.split("\0") if entry)


def _include_patterns() -> list[str]:
    build = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["tool"]["hatch"]
    return list(build["build"]["include"])


def _tracked_source_modules() -> tuple[str, ...]:
    return tuple(
        path
        for path in _tracked("--", "src/malleus")
        if path.startswith(PACKAGE_ROOT) and path.endswith(".py")
    )


def _build(target: str, source: Path, output: Path) -> Path:
    """Build one distribution offline from the installed backend."""

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            target,
            "--no-isolation",
            "--outdir",
            str(output),
        ],
        cwd=source,
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, f"{target} build failed:\n{result.stderr}"
    suffixes = {"--sdist": ".tar.gz", "--wheel": ".whl"}
    built = [path for path in output.iterdir() if path.name.endswith(suffixes[target])]
    assert len(built) == 1, f"expected one {target} artifact, found {built}"
    return built[0]


@pytest.fixture(scope="module")
def sdist(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return _build("--sdist", ROOT, tmp_path_factory.mktemp("sdist"))


@pytest.fixture(scope="module")
def sdist_wheel_tree(sdist: Path, tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A wheel rebuilt from the source archive, unpacked outside the tree."""

    source = tmp_path_factory.mktemp("sdist-source")
    # ``filter`` reached tarfile in 3.12 and the default changes in 3.14. The
    # member check below is the portable half and runs on every version.
    options = {"filter": "data"} if sys.version_info >= (3, 12) else {}
    with tarfile.open(sdist, "r:gz") as archive:
        for member in archive.getmembers():
            if member.issym() or member.islnk() or Path(member.name).is_absolute():
                pytest.fail(f"source archive member is not a plain path: {member.name}")
        archive.extractall(source, **options)
    extracted = [path for path in source.iterdir() if path.is_dir()]
    assert len(extracted) == 1, f"expected one source root, found {extracted}"
    wheel = _build("--wheel", extracted[0], tmp_path_factory.mktemp("sdist-wheel"))
    tree = tmp_path_factory.mktemp("sdist-wheel-tree")
    with zipfile.ZipFile(wheel) as archive:
        archive.extractall(tree)
    return tree


def test_every_tracked_source_module_is_named_by_the_include_list() -> None:
    selected = {
        included.relative_path.replace(os.sep, "/")
        for included in SdistBuilder(str(ROOT)).recurse_included_files()
    }
    missing = [path for path in _tracked_source_modules() if path not in selected]
    assert not missing, (
        "pyproject.toml [tool.hatch.build] include does not name these tracked "
        f"modules, so the source distribution drops them: {missing}"
    )


def test_every_include_pattern_selects_a_file() -> None:
    empty = []
    for pattern in _include_patterns():
        relative = pattern.lstrip("/")
        if any(character in relative for character in "*?["):
            if not any(ROOT.glob(relative)):
                empty.append(pattern)
        elif not (ROOT / relative).is_file():
            empty.append(pattern)
    assert not empty, (
        "pyproject.toml [tool.hatch.build] include names patterns that select "
        f"no file: {empty}"
    )


def test_the_source_distribution_ships_every_tracked_source_module(
    sdist: Path,
) -> None:
    with tarfile.open(sdist, "r:gz") as archive:
        members = {name.split("/", 1)[1] for name in archive.getnames() if "/" in name}
    missing = [path for path in _tracked_source_modules() if path not in members]
    assert not missing, f"the source archive {sdist.name} drops: {missing}"


def test_a_wheel_rebuilt_from_the_source_distribution_imports_the_compiler(
    sdist_wheel_tree: Path,
) -> None:
    environment = dict(os.environ)
    environment["PYTHONPATH"] = str(sdist_wheel_tree)
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import malleus, malleus.compiler;print(malleus.__file__)",
        ],
        cwd=sdist_wheel_tree.parent,
        capture_output=True,
        check=False,
        env=environment,
        text=True,
    )
    assert result.returncode == 0, (
        "a wheel rebuilt from the source archive cannot import "
        f"malleus.compiler:\n{result.stderr}"
    )
    imported = Path(result.stdout.strip())
    assert sdist_wheel_tree in imported.parents, (
        f"the import resolved to {imported}, not to the unpacked wheel; the "
        "observation says nothing about the distribution"
    )
