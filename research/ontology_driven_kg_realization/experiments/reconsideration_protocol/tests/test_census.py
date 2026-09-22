"""The split is honest only while no generic module carries an adapter's terms.

That is a mechanical property, so it is measured. The scan takes the vocabulary
as an argument and this package holds none of its own, which is the point: it
never learns a consumer's terms in order to check that it does not carry them.
Each adapter runs the scan against its own vocabulary from its own suite; here
it runs against an invented one, which is what proves the scan fires.
"""

from __future__ import annotations

import shutil

from .. import census


# Invented. No consumer uses these, and that is why they belong in a tracked
# test: a real adapter's terms in this file would be the leak the scan exists
# to prevent.
INVENTED = (
    "Quibblewick",
    "obligation:sprocket-alignment",
    "source:fnord-almanac",
    r"\bQ[137]\b",
    "at most one sprocket",
)


def test_the_scan_reads_every_generic_module_and_not_itself():
    names = {path.name for path in census.modules()}
    assert "census.py" not in names
    for expected in (
        "adapter.py",
        "archive.py",
        "assessment.py",
        "digests.py",
        "exposure.py",
        "freeze.py",
        "handoff.py",
        "index.py",
        "launch.py",
        "obligations.py",
        "packets.py",
        "pin.py",
        "producer.py",
        "windows.py",
    ):
        assert expected in names, expected


def test_a_planted_term_is_found(tmp_path):
    """RED, on a copy: a generic module carrying one term fails the scan."""
    poisoned = tmp_path / "reconsideration_protocol"
    shutil.copytree(census.PACKAGE, poisoned)
    target = poisoned / "exposure.py"
    target.write_bytes(
        target.read_bytes() + b'\nPLANTED = "Quibblewick"  # deliberate\n'
    )
    found = census.scan(INVENTED, package=poisoned)
    assert [(name, term) for name, term, _, _ in found] == [
        ("exposure.py", "Quibblewick")
    ], found
    assert census.report(INVENTED, package=poisoned)[0].startswith("exposure.py:")


def test_every_planted_kind_is_found(tmp_path):
    """A name, an id, a source id, a pattern's source and a phrase, each caught."""
    poisoned = tmp_path / "reconsideration_protocol"
    shutil.copytree(census.PACKAGE, poisoned)
    target = poisoned / "obligations.py"
    body = target.read_bytes()
    for term in INVENTED:
        # Appended as a comment so the term appears in the file exactly as the
        # adapter declares it. A repr would escape a pattern's backslashes and
        # the scan would honestly report no hit for a term that is not there.
        body += f"\n# planted: {term}\n".encode()
    target.write_bytes(body)
    found = {term for _, term, _, _ in census.scan(INVENTED, package=poisoned)}
    assert found == set(INVENTED), sorted(set(INVENTED) - found)


def test_the_shipped_package_carries_none_of_it():
    """GREEN, on the real modules."""
    assert census.scan(INVENTED) == []


def test_no_generic_module_imports_a_consumer():
    """A generic module never reaches for an adapter. The adapter reaches here."""
    offenders = []
    for path in census.modules():
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped.startswith(("import ", "from ")):
                continue
            if " d0" in f" {stripped}" or "harness" in stripped:
                offenders.append(f"{path.name}:{number}: {stripped}")
    assert offenders == [], offenders
