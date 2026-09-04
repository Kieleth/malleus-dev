"""Mechanical guard for the paper's frozen Core coordinate."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from malleus.ontology import OntologyRegistry


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).with_name("core-baseline.json")


def _git(*arguments: str) -> bytes:
    return subprocess.run(
        ("git", *arguments),
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def test_core_baseline_is_exact_and_current() -> None:
    baseline = json.loads(MANIFEST.read_bytes())
    assert set(baseline) == {
        "schema",
        "repository",
        "assent_ontology",
        "paper_ledger_epoch",
    }
    assert baseline["schema"] == "malleus.paper-v4.core-baseline/v1"

    repository = baseline["repository"]
    commit = repository["commit"]
    assert _git("rev-parse", f"{commit}^{{commit}}").decode().strip() == commit
    assert (
        _git("rev-parse", f"{commit}^{{tree}}").decode().strip() == repository["tree"]
    )

    ontology = baseline["assent_ontology"]
    source = _git("show", f"{commit}:{ontology['path']}")
    assert (ROOT / ontology["path"]).read_bytes() == source
    assert len(source) == ontology["byte_length"]
    assert "sha256:" + hashlib.sha256(source).hexdigest() == ontology["source_sha256"]
    assert f"version: {ontology['version']}\n".encode() in source
    assert ontology["semantic_grammar"] == 4
    actual_identity = OntologyRegistry(ROOT / ontology["path"]).content_hash_under(4)
    assert "sha256:" + actual_identity == ontology["semantic_identity"]

    epoch = baseline["paper_ledger_epoch"]
    assert epoch == {
        "initial_head": "GENESIS",
        "initial_event_count": 0,
        "prior_ledger_reuse": "FORBIDDEN",
    }
