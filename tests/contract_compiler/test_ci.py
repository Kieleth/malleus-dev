from __future__ import annotations

from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 CI
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import ci  # noqa: E402


def test_default_ci_plan_covers_every_boundary_once() -> None:
    commands = ci.plan("all")

    assert [command.name for command in commands] == [
        "quality",
        "tests",
        "compiler-tests",
        "ledger",
        "integration",
        "graph-recipe",
        "small-shop",
        "docs-html",
        "docs-doctest",
        "docs-linkcheck",
        "package-build",
        "package-check",
        "package-smoke",
    ]
    assert sum(command.argv[-1] == "pytest" for command in commands) == 1
    compiler = next(command for command in commands if command.name == "compiler-tests")
    assert compiler.argv[1:] == (
        "-m",
        "pytest",
        "-q",
        "tests/contract_compiler",
    )
    small_shop = next(command for command in commands if command.name == "small-shop")
    assert small_shop.argv == (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        str(ci.SMALL_SHOP),
    )
    assert sum(command.name == "small-shop" for command in commands) == 1
    quality = next(command for command in commands if command.name == "quality")
    assert quality.argv.count(str(ci.SMALL_SHOP)) == 1


def test_compiler_tests_are_not_duplicated_in_pytest_configuration() -> None:
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert "tests/contract_compiler" not in config["tool"]["pytest"][
        "ini_options"
    ]["testpaths"]


def test_fixed_profiles_are_subsets_of_the_default_plan() -> None:
    all_names = {command.name for command in ci.plan("all")}

    for profile in ("test", "docs", "package"):
        commands = ci.plan(profile)
        assert commands
        assert {command.name for command in commands} < all_names
        assert all(command.name != "small-shop" for command in commands)


def test_unknown_ci_profile_is_refused() -> None:
    with pytest.raises(ValueError, match="unknown CI profile"):
        ci.plan("manifest supplied command")


def test_ci_stops_at_the_first_failed_fixed_command(monkeypatch) -> None:
    calls: list[str] = []

    def fake_run(command, context):
        calls.append(command.name)
        return 9 if command.name == "tests" else 0

    monkeypatch.setattr(ci, "run_command", fake_run)

    assert ci.run("test") == 9
    assert calls == ["quality", "tests"]


def test_repository_purity_uses_fixed_git_argv_without_a_shell() -> None:
    assert ci.DIFF_ARGV == (
        "git",
        "diff",
        "--binary",
        "--exit-code",
        "HEAD",
        "--",
    )
    assert ci.STATUS_ARGV == (
        "git",
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    )


def test_local_ci_allows_unchanged_preexisting_dirt(monkeypatch) -> None:
    dirty = ci.RepositoryState(
        diff_status=1,
        diff=b"tracked diff",
        status=b" M tracked\0?? note\0",
        untracked=(("note", "digest"),),
    )
    monkeypatch.setattr(ci, "_repository_state", lambda: dirty)
    monkeypatch.setattr(ci, "run_command", lambda command, context: 0)

    assert ci.run("docs") == 0


def test_local_ci_refuses_any_new_repository_drift(monkeypatch) -> None:
    initial = ci.RepositoryState(1, b"before", b" M tracked\0", ())
    final = ci.RepositoryState(1, b"after", b" M tracked\0", ())
    states = iter((initial, final))
    monkeypatch.setattr(ci, "_repository_state", lambda: next(states))
    monkeypatch.setattr(ci, "run_command", lambda command, context: 0)

    assert ci.run("docs") == 1


def test_remote_ci_refuses_initial_dirt(monkeypatch) -> None:
    dirty = ci.RepositoryState(0, b"", b"?? generated\0", ())
    called = False

    def should_not_run(command, context):
        nonlocal called
        called = True
        return 0

    monkeypatch.setattr(ci, "_repository_state", lambda: dirty)
    monkeypatch.setattr(ci, "run_command", should_not_run)

    assert ci.run("test", require_clean=True) == 2
    assert not called


def test_wheel_probes_run_outside_the_repository(tmp_path: Path, monkeypatch) -> None:
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    (artifacts / "malleus.tar.gz").write_bytes(b"sdist")
    (artifacts / "malleus.whl").write_bytes(b"wheel")
    context = ci.Context(temporary=tmp_path, artifacts=artifacts)
    calls: list[tuple[tuple[str, ...], Path]] = []

    def fake_call(argv, *, env=None, cwd=ci.ROOT):
        calls.append((tuple(argv), cwd))
        return 0

    def fake_schema(argv, **kwargs):
        assert kwargs["cwd"] == tmp_path
        assert kwargs["check"] is False
        return SimpleNamespace(returncode=0, stdout="/installed/malleus.yaml\n", stderr="")

    monkeypatch.setattr(ci, "_call", fake_call)
    monkeypatch.setattr(ci.subprocess, "run", fake_schema)

    assert ci._smoke_package(context) == 0
    assert len(calls) == 5
    assert all(cwd == tmp_path for _, cwd in calls)
    assert [Path(argv[0]).name for argv, _ in calls[-3:]] == [
        "malleus-inquisitor",
        "malleus-ocr",
        "malleus-recon",
    ]


def test_docs_command_keeps_deterministic_environment(
    tmp_path: Path,
    monkeypatch,
) -> None:
    context = ci.Context(temporary=tmp_path, artifacts=tmp_path / "artifacts")
    captured = {}

    def fake_call(argv, *, env=None, cwd=ci.ROOT):
        captured.update(argv=tuple(argv), env=env, cwd=cwd)
        return 0

    monkeypatch.setattr(ci, "_call", fake_call)

    for command, builder in zip(
        ci.DOCS,
        ("html", "doctest", "linkcheck"),
        strict=True,
    ):
        captured.clear()
        assert ci.run_command(command, context) == 0
        assert captured["argv"][-1] == str(tmp_path / "docs" / builder)
        assert captured["env"]["PYTHONDONTWRITEBYTECODE"] == "1"
        assert captured["env"]["PYTHONHASHSEED"] == "0"
        assert captured["env"]["SOURCE_DATE_EPOCH"] == "0"
        assert captured["cwd"] == ci.ROOT


def test_ci_runner_is_not_ignored() -> None:
    result = subprocess.run(
        ("git", "check-ignore", "--quiet", "scripts/ci.py"),
        cwd=ROOT,
        check=False,
    )

    assert result.returncode == 1
