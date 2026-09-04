#!/usr/bin/env python3
"""Run Malleus' fixed local continuous-integration checks."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
from tempfile import TemporaryDirectory
from typing import Sequence
import zipfile


ROOT = Path(__file__).resolve().parents[1]
GRAPH_RECIPE = Path(
    "research/ontology_driven_kg_realization/experiments/graph_recipe"
)
SMALL_SHOP = Path(
    "research/ontology_driven_kg_realization/experiments/small_shop"
)


@dataclass(frozen=True)
class Command:
    """One repository-owned command, never loaded from a manifest."""

    name: str
    argv: tuple[str, ...]


@dataclass(frozen=True)
class Context:
    """Fresh output locations shared by one runner invocation."""

    temporary: Path
    artifacts: Path


@dataclass(frozen=True)
class RepositoryState:
    """Exact tracked and untracked state around one CI run."""

    diff_status: int
    diff: bytes
    status: bytes
    untracked: tuple[tuple[str, str], ...]


QUALITY = Command(
    "quality",
    (
        sys.executable,
        "-m",
        "ruff",
        "check",
        "scripts/ci.py",
        "scripts/contract_compiler_ledger.py",
        "scripts/contract_compiler_integration.py",
        "tests/contract_compiler",
        "tests/test_contract_compiler_ledger.py",
        "tests/test_contract_compiler_integration.py",
        "src/malleus",
        str(GRAPH_RECIPE),
        str(SMALL_SHOP),
    ),
)
TEST = (
    QUALITY,
    Command("tests", (sys.executable, "-m", "pytest")),
    Command(
        "ledger",
        (sys.executable, "scripts/contract_compiler_ledger.py", "check"),
    ),
    Command(
        "integration",
        (sys.executable, "scripts/contract_compiler_integration.py", "check"),
    ),
    Command(
        "graph-recipe",
        (
            sys.executable,
            "-m",
            "pytest",
            "-q",
            str(GRAPH_RECIPE / "test_cases.py"),
        ),
    ),
)
RECON = (
    Command(
        "recon-tests",
        (
            sys.executable,
            "-m",
            "pytest",
            "tests/test_recon.py",
            "tests/test_recon_ontology.py",
        ),
    ),
)
SMALL_SHOP_TEST = Command(
    "small-shop",
    (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        str(SMALL_SHOP),
    ),
)
DOCS = tuple(
    Command(
        f"docs-{builder}",
        (
            sys.executable,
            "-m",
            "sphinx",
            "-W",
            "--keep-going",
            "-n",
            "-b",
            builder,
            "docs",
        ),
    )
    for builder in ("html", "doctest", "linkcheck")
)
PACKAGE = (
    Command(
        "package-build",
        (sys.executable, "-m", "build", "--sdist", "--wheel"),
    ),
    Command("package-check", (sys.executable, "-m", "twine", "check")),
    Command("package-parity", (sys.executable, "-m", "build")),
    Command("package-smoke", (sys.executable, "-m", "venv")),
)
PROFILES = {
    "all": (*TEST, SMALL_SHOP_TEST, *DOCS),
    "test": TEST,
    "recon": RECON,
    "docs": DOCS,
    "package": PACKAGE,
}
DIFF_ARGV = ("git", "diff", "--binary", "--exit-code", "HEAD", "--")
STATUS_ARGV = (
    "git",
    "status",
    "--porcelain=v1",
    "-z",
    "--untracked-files=all",
)


def plan(profile: str) -> tuple[Command, ...]:
    """Return one immutable, repository-owned command plan."""
    try:
        return PROFILES[profile]
    except KeyError as error:
        choices = ", ".join(PROFILES)
        raise ValueError(
            f"unknown CI profile {profile!r}; choose one of: {choices}"
        ) from error


def _call(
    argv: Sequence[str],
    *,
    env: dict[str, str] | None = None,
    cwd: Path = ROOT,
) -> int:
    print("[ci]", " ".join(argv), flush=True)
    try:
        return subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            check=False,
        ).returncode
    except OSError as error:
        print(f"[ci] cannot run {argv[0]!r}: {error}", file=sys.stderr)
        return 2


def _git_capture(argv: Sequence[str], accepted: set[int]) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(
            argv,
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise RuntimeError(f"cannot run {argv[0]!r}: {error}") from error
    if result.returncode not in accepted:
        message = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"{' '.join(argv)} failed: {message}")
    return result


def _repository_state() -> RepositoryState:
    diff = _git_capture(DIFF_ARGV, {0, 1})
    status = _git_capture(STATUS_ARGV, {0})
    untracked: list[tuple[str, str]] = []
    for record in status.stdout.split(b"\0"):
        if not record.startswith(b"?? "):
            continue
        relative = os.fsdecode(record[3:])
        path = ROOT / relative
        if path.is_symlink():
            source = os.fsencode(os.readlink(path))
        else:
            try:
                source = path.read_bytes()
            except OSError as error:
                raise RuntimeError(f"cannot fingerprint {relative}: {error}") from error
        untracked.append((relative, hashlib.sha256(source).hexdigest()))
    return RepositoryState(
        diff_status=diff.returncode,
        diff=diff.stdout,
        status=status.stdout,
        untracked=tuple(untracked),
    )


def _built_artifacts(context: Context) -> tuple[Path, ...]:
    artifacts = tuple(sorted(path for path in context.artifacts.iterdir() if path.is_file()))
    wheels = [path for path in artifacts if path.suffix == ".whl"]
    sdists = [path for path in artifacts if path.name.endswith(".tar.gz")]
    if len(wheels) != 1 or len(sdists) != 1 or len(artifacts) != 2:
        names = [path.name for path in artifacts]
        raise ValueError(
            "package build must produce exactly one wheel and one sdist; "
            f"found {names}"
        )
    return artifacts


def _extract_sdist(sdist: Path, destination: Path) -> Path:
    with tarfile.open(sdist, "r:gz") as archive:
        members = archive.getmembers()
        paths = tuple(PurePosixPath(member.name) for member in members)
        if not paths or any(
            path.is_absolute()
            or not path.parts
            or ".." in path.parts
            or not (member.isfile() or member.isdir())
            for path, member in zip(paths, members, strict=True)
        ):
            raise ValueError("source archive contains an unsafe member")
        roots = {path.parts[0] for path in paths}
        if len(roots) != 1:
            raise ValueError("source archive must contain one root directory")
        if sys.version_info >= (3, 12):
            archive.extractall(destination, members=members, filter="data")
        else:  # pragma: no cover - compatibility with supported Python 3.10/3.11
            archive.extractall(destination, members=members)
    return destination / next(iter(roots))


def _wheel_contents(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("wheel contains duplicate members")
        return {name: archive.read(name) for name in names if not name.endswith("/")}


def _check_package_parity(context: Context, command: Command) -> int:
    try:
        artifacts = _built_artifacts(context)
        direct = next(path for path in artifacts if path.suffix == ".whl")
        sdist = next(path for path in artifacts if path.name.endswith(".tar.gz"))
        source = _extract_sdist(sdist, context.temporary / "sdist-source")
    except (OSError, ValueError, tarfile.TarError) as error:
        print(f"[ci] cannot inspect source archive: {error}", file=sys.stderr)
        return 2
    rebuilt_directory = context.temporary / "sdist-wheel"
    rebuilt_directory.mkdir()
    result = _call(
        (
            *command.argv,
            "--no-isolation",
            "--wheel",
            "--outdir",
            str(rebuilt_directory),
            str(source),
        ),
        cwd=context.temporary,
    )
    if result:
        return result
    rebuilt = tuple(rebuilt_directory.glob("*.whl"))
    if len(rebuilt) != 1:
        print("[ci] source archive must rebuild exactly one wheel", file=sys.stderr)
        return 2
    try:
        if _wheel_contents(direct) != _wheel_contents(rebuilt[0]):
            print(
                "[ci] repository and source-archive wheels differ",
                file=sys.stderr,
            )
            return 1
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"[ci] cannot compare wheels: {error}", file=sys.stderr)
        return 2
    return 0


def _smoke_package(context: Context) -> int:
    try:
        artifacts = _built_artifacts(context)
    except ValueError as error:
        print(f"[ci] {error}", file=sys.stderr)
        return 2
    wheel = next(path for path in artifacts if path.suffix == ".whl")
    environment = context.temporary / "wheel-smoke"
    result = _call(
        (sys.executable, "-m", "venv", str(environment)),
        cwd=context.temporary,
    )
    if result:
        return result
    scripts = environment / ("Scripts" if os.name == "nt" else "bin")
    python = scripts / ("python.exe" if os.name == "nt" else "python")
    result = _call(
        (str(python), "-m", "pip", "install", "--quiet", str(wheel)),
        cwd=context.temporary,
    )
    if result:
        return result
    schema = subprocess.run(
        (
            str(python),
            "-c",
            "from malleus.ontology import bundled_ontology_path; "
            "print(bundled_ontology_path('malleus.yaml'))",
        ),
        cwd=context.temporary,
        capture_output=True,
        check=False,
        text=True,
    )
    if schema.returncode:
        sys.stderr.write(schema.stderr)
        return schema.returncode
    checks = (
        (scripts / "malleus-inquisitor", schema.stdout.strip()),
        (scripts / "malleus-compiler", "--help"),
        (scripts / "malleus-ocr", "--help"),
        (scripts / "malleus-recon", "--help"),
    )
    for executable, argument in checks:
        result = _call((str(executable), argument), cwd=context.temporary)
        if result:
            return result
    return 0


def run_command(command: Command, context: Context) -> int:
    """Execute one known command without a shell or manifest input."""
    if command.name == "package-build":
        return _call((*command.argv, "--outdir", str(context.artifacts)))
    if command.name == "package-check":
        try:
            artifacts = _built_artifacts(context)
        except ValueError as error:
            print(f"[ci] {error}", file=sys.stderr)
            return 2
        return _call((*command.argv, *(str(path) for path in artifacts)))
    if command.name == "package-parity":
        return _check_package_parity(context, command)
    if command.name == "package-smoke":
        return _smoke_package(context)
    if command.name.startswith("docs-"):
        builder = command.name.removeprefix("docs-")
        output = context.temporary / "docs" / builder
        env = os.environ.copy()
        env.update(
            PYTHONDONTWRITEBYTECODE="1",
            PYTHONHASHSEED="0",
            SOURCE_DATE_EPOCH="0",
        )
        return _call((*command.argv, str(output)), env=env)
    return _call(command.argv)


def run(
    profile: str,
    *,
    artifacts: Path | None = None,
    require_clean: bool = False,
) -> int:
    """Run a fixed profile and stop at the first failed boundary."""
    commands = plan(profile)
    try:
        initial = _repository_state()
    except RuntimeError as error:
        print(f"[ci] cannot inspect repository: {error}", file=sys.stderr)
        return 2
    if require_clean and (initial.diff_status or initial.status):
        print("[ci] --require-clean refused a dirty repository", file=sys.stderr)
        return 2
    with TemporaryDirectory(prefix="malleus-ci-") as temporary_name:
        temporary = Path(temporary_name)
        artifact_root = artifacts.resolve() if artifacts else temporary / "dist"
        if artifacts is not None and (
            artifact_root == ROOT or ROOT in artifact_root.parents
        ):
            print(
                "[ci] retained artifacts must be outside the repository",
                file=sys.stderr,
            )
            return 2
        if artifact_root.exists() and any(artifact_root.iterdir()):
            print(
                f"[ci] artifact directory must be empty: {artifact_root}",
                file=sys.stderr,
            )
            return 2
        artifact_root.mkdir(parents=True, exist_ok=True)
        context = Context(temporary=temporary, artifacts=artifact_root)
        result = 0
        for command in commands:
            result = run_command(command, context)
            if result:
                print(f"[ci] {command.name} failed with status {result}", file=sys.stderr)
                break
    try:
        final = _repository_state()
    except RuntimeError as error:
        print(f"[ci] cannot inspect repository after checks: {error}", file=sys.stderr)
        return 2
    if final != initial:
        print(
            "[ci] checks changed tracked or untracked repository state",
            file=sys.stderr,
        )
        return 1
    if result:
        return result
    print(f"[ci] {profile} passed", flush=True)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", choices=tuple(PROFILES), default="all")
    parser.add_argument(
        "--artifacts",
        type=Path,
        help="retain package artifacts in this empty directory outside the repository",
    )
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="refuse unless repository state is clean before and after checks",
    )
    arguments = parser.parse_args(argv)
    if arguments.artifacts is not None and arguments.profile not in {"all", "package"}:
        parser.error("--artifacts requires the all or package profile")
    return run(
        arguments.profile,
        artifacts=arguments.artifacts,
        require_clean=arguments.require_clean,
    )


if __name__ == "__main__":
    raise SystemExit(main())
