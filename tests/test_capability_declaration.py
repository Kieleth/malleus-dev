"""The capability declaration the skills load must stay true to Core.

This guards one failure mode: a consumer project meets a limitation, does not
know Core already answers it, and writes an adapter or declares a gap instead.
The declaration is the list an agent reads before deciding that; these checks
keep it honest by refusing an entry point that does not exist and refusing a
capability the status boundary knows about and the declaration does not.

Anchors, chosen because prose moves and these do not:

* ``malleus.IMPLEMENTATION_STATUS`` - ``docs/IMPLEMENTATION_STATUS.md`` names it
  as its own machine-readable source, so its ``implemented_capabilities`` and
  ``pending_capabilities`` IDs are the closed capability vocabulary.
* the ``## `` section headings of ``docs/IMPLEMENTATION_STATUS.md`` - every
  section either contributes declared rows or is listed here as carrying no
  capability, so a new section fails this test until someone reads it.

These checks establish that the declaration names real, importable entry points
and omits no known capability. They do not establish that a sentence describing
a capability is accurate; that stays a reader's job.
"""

from __future__ import annotations

import importlib
from pathlib import Path
import re

import pytest

from malleus import IMPLEMENTATION_STATUS

ROOT = Path(__file__).resolve().parents[1]
STATUS_DOCUMENT = ROOT / "docs" / "IMPLEMENTATION_STATUS.md"
SKILLS = ROOT / ".claude" / "skills"
DECLARATION = SKILLS / "malleus-dev" / "references" / "CAPABILITIES.md"

COLUMNS = (
    "Capability",
    "Entry point",
    "What it does",
    "Status",
    "Protocol role",
    "Status document section",
)
STATUSES = frozenset({"implemented", "partial", "not implemented"})

# The closed protocol-boundary taxonomy of docs/PRINCIPLES.md.
ROLES = (
    "PROTOCOL_INVARIANT",
    "OPTIONAL_PROFILE",
    "REFERENCE_IMPLEMENTATION",
    "CONFORMANCE_FIXTURE",
    "ADOPTER_CHOICE",
)

# Sections of docs/IMPLEMENTATION_STATUS.md that declare no capability. A new
# section is a capability section until someone reads it and says otherwise
# here, which is the point: this list fails closed.
NON_CAPABILITY_SECTIONS = frozenset({"Release boundary rule", "History"})

# What a row writes in the section column for a shipped capability the status
# document does not mention at all. The omission is the finding; the row records
# it rather than hiding it, and the check below proves the omission is real.
ABSENT_SECTION = "(absent)"

# The skills that must point an agent at the declaration before it declares a
# gap, writes adopter code, or works around a limitation.
SKILL_FILES = (
    SKILLS / "malleus-dev" / "SKILL.md",
    SKILLS / "malleus-acolyte" / "SKILL.md",
    SKILLS / "malleus-paper" / "SKILL.md",
)

_SYMBOL = re.compile(r"`(malleus[A-Za-z0-9_.]*)`")


def _rows():
    lines = [
        line.strip()
        for line in DECLARATION.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("|")
    ]
    assert lines, "the declaration carries no table"
    cells = [[cell.strip() for cell in line.strip("|").split("|")] for line in lines]
    assert tuple(cells[0]) == COLUMNS, f"unexpected columns: {cells[0]}"
    assert set(cells[1]) <= {"---", ":---", "---:", ":---:"}, "missing header rule"
    body = cells[2:]
    for row in body:
        assert len(row) == len(COLUMNS), f"row has {len(row)} cells: {row}"
    return body


def _sections():
    return [
        line[3:].strip()
        for line in STATUS_DOCUMENT.read_text(encoding="utf-8").splitlines()
        if line.startswith("## ")
    ]


def _resolve(path: str):
    parts = path.split(".")
    for stop in range(len(parts), 0, -1):
        try:
            module = importlib.import_module(".".join(parts[:stop]))
        except ImportError:
            continue
        value = module
        for attribute in parts[stop:]:
            value = getattr(value, attribute)
        return value
    raise ImportError(path)


def test_the_declaration_exists():
    assert DECLARATION.is_file(), f"no capability declaration at {DECLARATION}"


def test_every_declared_entry_point_imports():
    unresolved = []
    for row in _rows():
        for symbol in _SYMBOL.findall(row[1]):
            try:
                _resolve(symbol)
            except (AttributeError, ImportError):
                unresolved.append(f"{row[0]}: {symbol}")
    assert not unresolved, "declared entry points that do not resolve: " + "; ".join(
        unresolved
    )


def test_an_implemented_row_names_an_entry_point():
    missing = [
        row[0]
        for row in _rows()
        if row[3] in {"implemented", "partial"} and not _SYMBOL.findall(row[1])
    ]
    assert not missing, "rows claiming code with no entry point: " + "; ".join(missing)


def test_every_status_and_role_is_from_its_closed_vocabulary():
    bad_status = {row[3] for row in _rows()} - STATUSES
    assert not bad_status, f"status values outside the closed set: {sorted(bad_status)}"
    bad_roles = [row[4] for row in _rows() if not row[4].startswith(ROLES)]
    assert not bad_roles, f"protocol roles outside the taxonomy: {bad_roles}"


def test_every_landed_capability_appears_in_the_declaration():
    text = DECLARATION.read_text(encoding="utf-8")
    implemented = {
        capability
        for capability in IMPLEMENTATION_STATUS.implemented_capabilities
        if f"`{capability}`" not in text
    }
    assert not implemented, (
        "landed capabilities absent from the declaration: " + ", ".join(sorted(implemented))
    )


def test_every_pending_capability_appears_as_not_implemented():
    rows = _rows()
    absent, miscategorised = [], []
    for capability in IMPLEMENTATION_STATUS.pending_capabilities:
        carrying = [row for row in rows if f"`{capability}`" in row[0]]
        if not carrying:
            absent.append(capability)
        elif any(row[3] != "not implemented" for row in carrying):
            miscategorised.append(capability)
    assert not absent, "pending capabilities absent: " + ", ".join(sorted(absent))
    assert not miscategorised, "pending capabilities not marked not implemented: " + ", ".join(
        sorted(miscategorised)
    )


def test_every_status_document_section_is_accounted_for():
    sections = _sections()
    declared = {row[5] for row in _rows()} - {ABSENT_SECTION}
    unknown = declared - set(sections)
    assert not unknown, f"rows cite sections the status document lacks: {sorted(unknown)}"
    uncovered = [
        section
        for section in sections
        if section not in declared and section not in NON_CAPABILITY_SECTIONS
    ]
    assert not uncovered, (
        "status document sections with no declared capability: " + ", ".join(uncovered)
    )


def test_a_row_claiming_no_status_section_really_has_none():
    status = STATUS_DOCUMENT.read_text(encoding="utf-8")
    wrong = []
    for row in _rows():
        if row[5] != ABSENT_SECTION:
            continue
        modules = {".".join(symbol.split(".")[:2]) for symbol in _SYMBOL.findall(row[1])}
        if any(module in status for module in modules):
            wrong.append(row[0])
    assert not wrong, (
        "rows claim the status document omits a module it names: " + "; ".join(wrong)
    )


@pytest.mark.parametrize("skill", SKILL_FILES, ids=lambda path: path.parent.name)
def test_every_skill_points_at_the_declaration(skill):
    text = skill.read_text(encoding="utf-8")
    assert "CAPABILITIES.md" in text, f"{skill} does not reference the declaration"
    assert "before declaring a gap" in text, f"{skill} does not carry the rule"
