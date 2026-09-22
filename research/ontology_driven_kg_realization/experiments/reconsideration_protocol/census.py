"""Scan this package for an adapter's own vocabulary.

The split is honest only while no generic module carries a term that belongs to
one consumer. That is a mechanical property, so it is measured rather than
asserted: ``scan`` reads the bytes of every module here and reports every line
carrying a term the adapter declares.

The scan takes the vocabulary as an argument and holds none of its own, so this
package never learns a consumer's terms in order to check that it does not
carry them. Each adapter runs the scan against its own ``Vocabulary`` from its
own suite; the test beside this module runs it against an invented vocabulary,
which is what proves the scan fires.
"""

from __future__ import annotations

from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
EXCLUDED = ("census.py",)
"""This module names the mechanism, never a term, and is not its own subject."""


def modules(package=None):
    """Every generic module the scan reads, tests and caches excluded."""
    package = PACKAGE if package is None else Path(package)
    return tuple(
        path
        for path in sorted(package.glob("*.py"))
        if path.is_file() and path.name not in EXCLUDED
    )


def scan(terms, *, package=None):
    """Every (module, term, line number, line) a generic module should not hold.

    Matching is literal and case sensitive. A term is a term as the adapter
    declares it, including a regular expression's source: a generic module has
    no business carrying either.
    """
    found = []
    for path in modules(package):
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            for term in terms:
                if term and term in line:
                    found.append((path.name, term, number, line.strip()))
    return sorted(found)


def report(terms, *, package=None):
    """The scan as lines a failing test can print."""
    return [
        f"{name}:{number}: carries {term!r}: {line}"
        for name, term, number, line in scan(terms, package=package)
    ]
