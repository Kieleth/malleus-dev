"""Bound Git work without caching repository validation across calls."""

from pathlib import Path
import subprocess

import pytest

from scripts import contract_compiler_ledger as ledger


def _git(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repository, check=True, capture_output=True, text=True
    ).stdout.strip()


@pytest.fixture
def repository(tmp_path):
    _git(tmp_path, "init", "-b", "main")
    _git(tmp_path, "config", "user.name", "Malleus tests")
    _git(tmp_path, "config", "user.email", "tests@malleus.invalid")
    _git(tmp_path, "commit", "--allow-empty", "-m", "base")
    design = tmp_path / "design"
    (design / "contract_compiler").mkdir(parents=True)
    (design / "contract_compiler/program.md").write_text("")
    (design / "contract_compiler/decisions.md").write_text("")
    (design / "PROTOCOL_FOUNDATION_GRAPH.ttl").write_text("")
    return tmp_path


def _validate(repository, *commits):
    entries = [
        {
            "entry_id": "OVR-000001",
            "references": [
                {"type": "COMMIT", "relation": "EVIDENCES", "target": commit}
                for commit in commits
            ],
        }
    ]
    ledger._validate_references(entries, repository, None)


def test_many_commit_references_use_one_git_scan(repository, monkeypatch):
    head = _git(repository, "rev-parse", "HEAD")
    _git(repository, "commit", "--allow-empty", "-m", "next")
    successor = _git(repository, "rev-parse", "HEAD")
    calls = []
    run = subprocess.run

    def counted(*args, **kwargs):
        calls.append(args[0])
        return run(*args, **kwargs)

    monkeypatch.setattr(ledger.subprocess, "run", counted)
    _validate(repository, *([head, successor] * 20))
    assert len(calls) == 1, calls
    assert calls[0][1] == "rev-list"


def test_next_validation_observes_changed_head_and_evidence_tags(repository):
    head = _git(repository, "rev-parse", "HEAD")
    _git(repository, "commit", "--allow-empty", "-m", "next")
    successor = _git(repository, "rev-parse", "HEAD")
    _validate(repository, head, successor)
    _git(repository, "update-ref", "refs/heads/main", head)
    with pytest.raises(ledger.LedgerValidationError, match="reachable"):
        _validate(repository, successor)
    _git(repository, "tag", "ordinary", successor)
    with pytest.raises(ledger.LedgerValidationError, match="reachable"):
        _validate(repository, successor)
    _git(repository, "tag", "-a", "evidence/retained", successor, "-m", "retained")
    _validate(repository, successor)
    _git(repository, "tag", "-d", "evidence/retained")
    with pytest.raises(ledger.LedgerValidationError, match="reachable"):
        _validate(repository, successor)


def test_unknown_commit_still_refuses_as_unresolved(repository):
    with pytest.raises(ledger.LedgerValidationError, match="commit does not resolve"):
        _validate(repository, "1" * 40)


def test_annotated_tag_object_keeps_existing_commit_peeling_semantics(repository):
    _git(repository, "tag", "-a", "snapshot", "HEAD", "-m", "snapshot")
    tag_object = _git(repository, "rev-parse", "refs/tags/snapshot")
    _validate(repository, tag_object)


def test_current_document_is_rechecked_after_a_successful_call(repository):
    document = repository / "current.md"
    document.write_text("# Current\n")
    entry = {
        "entry_id": "OVR-000001",
        "references": [
            {"type": "DOCUMENT", "relation": "DEFINES", "target": "current.md#current"}
        ],
    }
    ledger._validate_references([entry], repository, None)
    document.write_text("# Changed\n")
    with pytest.raises(ledger.LedgerValidationError, match="heading anchor"):
        ledger._validate_references([entry], repository, None)
