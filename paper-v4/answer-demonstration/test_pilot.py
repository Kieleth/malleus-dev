"""Identity, source-free and output-boundary guards for the private pilot."""

import ast
import builtins
import socket

import pytest

import pilot


@pytest.mark.parametrize("coordinate", ["main", "abc", "-h", "", "a" * 39])
def test_runtime_requires_an_exact_commit_before_git_lookup(coordinate):
    with pytest.raises(ValueError, match="full commit"):
        pilot.verify_runtime(coordinate)


def test_guard_is_resolved_at_a_paper_coordinate_not_the_core_coordinate():
    native, identity = pilot.load_native()
    assert native.FORBIDDEN_ATTEMPTS == ("embedding_import", "file_read", "network")
    assert identity.startswith("sha256:")


@pytest.mark.parametrize(
    "operation",
    [
        lambda: builtins.open("a-source-file.txt"),
        lambda: socket.socket(),
        lambda: __import__("sentence_transformers"),
    ],
)
def test_reused_guard_refuses_source_network_and_embedding_access(operation):
    native, _ = pilot.load_native()
    guard = native._SourceFreeGuard()
    with pytest.raises(native.NativeQueryRefusal):
        with guard:
            operation()
    assert sum(guard.attempts.values()) == 1


def test_source_bearing_output_cannot_be_published():
    with pytest.raises(ValueError, match="under private"):
        pilot.output_directory(pilot.ROOT / "paper-v4/answer-output")


def test_existing_private_directory_cannot_be_overwritten():
    with pytest.raises(ValueError, match="overwrite"):
        pilot.output_directory(pilot.ROOT / "private")


def test_question_text_drift_refuses_even_when_ids_match():
    source = (
        pilot.ROOT / "paper-v4/experiment-v4/competency-questions-v3.json"
    ).read_bytes()
    changed = source.replace(b"How many ocean-bottom", b"How few ocean-bottom")
    assert changed != source
    with pytest.raises(ValueError, match="frozen question"):
        pilot.load_questions(changed)


def test_retained_programs_include_all_local_import_dependencies():
    sources = pilot.program_sources()
    assert "pilot.py" in sources
    for name, source in sources.items():
        assert source == (pilot.HERE / name).read_bytes()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module is not None:
                modules = [node.module]
            elif isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            else:
                continue
            for module in modules:
                local_name = module.split(".")[0] + ".py"
                if (pilot.HERE / local_name).is_file():
                    assert local_name in sources, f"unretained dependency: {local_name}"
