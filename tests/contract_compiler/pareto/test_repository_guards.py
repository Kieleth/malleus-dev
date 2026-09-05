"""Mechanical guards for couplings that can return without a test.

Three invariants live here. No Python file under ``src`` or ``tests`` may name
a handover path, because a handover directory is archived evidence and never a
fixture. Every fixture manifest must match the bytes of the members it pins,
because nothing else recomputes those digests. Every staged graph write in the
knowledge history must thaw the change set's frozen properties, because a
shallow copy refuses every multivalued slot at admit.
"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[3]
FIXTURES = ROOT / "research" / "ontology_driven_kg_realization" / "fixtures"
SCANNED_ROOTS = ("src", "tests")
SELF = Path(__file__).resolve()
KNOWLEDGE = ROOT / "src" / "malleus" / "_contract_pipeline" / "knowledge.py"
STAGED_WRITE_METHODS = frozenset(
    {
        "create_entity",
        "create_event",
        "create_event_participation",
        "create_relation",
    }
)
HANDOVER_PATH = re.compile(
    r"handover/|[\"']handover[\"']\s*/|/\s*[\"']handover[\"']"
)


# The two governance tests below take a handover document as their subject:
# one asserts the ledger entry that pins a handover path, the other verifies the
# recorded review evidence against its historical blob. Neither reads fixture
# bytes out of a handover directory, which is the coupling this guard defends.
# Any other file, and any change to these counts, fails.
RECORDED_HANDOVER_REFERENCES = {
    "tests/contract_compiler/test_core_review_response.py": 3,
    "tests/test_contract_compiler_integration.py": 2,
}


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


def test_handover_paths_stay_out_of_python_sources_and_tests() -> None:
    references = _handover_references()

    assert set(references) <= set(RECORDED_HANDOVER_REFERENCES), (
        "a Python source or test names a handover path: "
        f"{sorted(set(references) - set(RECORDED_HANDOVER_REFERENCES))}"
    )
    assert references == RECORDED_HANDOVER_REFERENCES


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


def test_staged_writes_thaw_the_frozen_change_set_properties() -> None:
    """Every staged graph write must thaw the operation's frozen properties.

    A change set freezes list values into tuples. The ontology validator
    accepts only ``list`` for a multivalued slot, so a shallow ``dict()``
    copy refuses every multivalued property at admit. Nothing else catches
    the shallow copy: a population without a list-valued property replays
    either way.
    """

    source = KNOWLEDGE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(KNOWLEDGE))
    writes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in STAGED_WRITE_METHODS
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "staged"
    ]

    assert len(writes) == len(STAGED_WRITE_METHODS), (
        "the staged write sites moved: "
        f"{sorted(call.func.attr for call in writes)}"
    )
    for call in writes:
        argument = call.args[-1]
        assert (
            isinstance(argument, ast.Call)
            and isinstance(argument.func, ast.Name)
            and argument.func.id == "_staged_properties"
        ), (
            f"staged.{call.func.attr} at line {call.lineno} does not thaw the "
            "operation properties"
        )
