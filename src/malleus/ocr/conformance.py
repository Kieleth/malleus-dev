"""The packaged conformance cases.

An adapter emits bundle documents. These are what it checks its wiring
against: four documents that must be accepted, three that must be refused,
because a verifier that refuses nothing is indistinguishable from one that is
not running. Each case also fixes whether the bundle is a complete reading, so
a case cannot pass on integrity while quietly accounting for nothing.

Each case additionally fixes its census, unit by unit, as an outcome and the
disposition that outcome carries. Whether the bundle is complete is one bit and
was the only thing a case could state, so a case could not distinguish a unit
nobody fetched from a unit whose only call failed, and could not have noticed
that a reviewer's ABSENT was being reported READ.

The cases are authored, not generated. Their `expect` lists are checked
against the live verifier on every test run, so a case that stops meaning what
it says fails rather than drifts. Everything in them is invented: no
production document, credential, network dependency or adopter fixture is
present, and none may be added. An adopter's real document is a private
fixture that stays in the adopter.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CASE_ROOT = Path(__file__).parent / "cases"
CASES: tuple[str, ...] = (
    "conforming",
    "refuses-ungoverned-value",
    "refuses-broken-lineage",
    "registration-is-not-a-reading",
    "absence-is-not-a-reading",
    "silence-is-not-success",
    "refuses-conflicting-review",
)


def load_case(name: str) -> dict[str, Any]:
    """Read one case, or refuse. A missing case is a packaging failure."""
    if name not in CASES:
        raise KeyError(f"unknown conformance case '{name}'")
    path = CASE_ROOT / f"{name}.json"
    if not path.is_file():
        raise FileNotFoundError(
            f"conformance case '{name}' is declared and not installed at {path}"
        )
    return json.loads(path.read_text())
