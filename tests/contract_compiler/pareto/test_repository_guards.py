"""Mechanical guards for couplings that can return without a test.

Two invariants live here. No Python file under ``src`` or ``tests`` may name a
handover path, because a handover directory is archived evidence and never a
fixture. Every fixture manifest must match the bytes of the members it pins,
because nothing else recomputes those digests.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "research" / "ontology_driven_kg_realization" / "fixtures"
SCANNED_ROOTS = ("src", "tests")
SELF = Path(__file__).resolve()
HANDOVER_PATH = re.compile(
    r"handover/|[\"']handover[\"']\s*/|/\s*[\"']handover[\"']"
)


def _handover_references() -> dict[str, int]:
    """Count the lines naming a handover path in every scanned Python file."""

    hits: dict[str, int] = {}
    for name in SCANNED_ROOTS:
        for path in sorted((ROOT / name).rglob("*.py")):
            if path.resolve() == SELF:
                continue
            count = sum(
                1
                for line in path.read_text(encoding="utf-8").splitlines()
                if HANDOVER_PATH.search(line)
            )
            if count:
                hits[path.relative_to(ROOT).as_posix()] = count
    return hits


def test_no_python_source_or_test_names_a_handover_path() -> None:
    assert _handover_references() == {}


def test_every_fixture_manifest_matches_its_members_bytes() -> None:
    manifests = sorted(FIXTURES.glob("*/manifest.json"))
    assert manifests

    for manifest in manifests:
        label = manifest.relative_to(ROOT).as_posix()
        data = json.loads(manifest.read_bytes())
        members = data["members"]
        assert members, f"{label}: manifest pins no member"
        seen: set[str] = set()
        for member in members:
            relative = member["path"]
            assert relative not in seen, f"{label}: duplicate member {relative}"
            seen.add(relative)
            assert ".." not in Path(relative).parts, (
                f"{label}: member escapes the fixture: {relative}"
            )
            path = manifest.parent / relative
            assert path.is_file(), f"{label}: pinned member is absent: {relative}"
            content = path.read_bytes()
            digest = "sha256:" + hashlib.sha256(content).hexdigest()
            assert digest == member["sha256"], (
                f"{label}: digest drift for {relative}: "
                f"pinned {member['sha256']}, found {digest}"
            )
            if "bytes" in member:
                assert len(content) == member["bytes"], (
                    f"{label}: byte-length drift for {relative}: "
                    f"pinned {member['bytes']}, found {len(content)}"
                )
