#!/usr/bin/env python3
"""Rebind the report's repository-file digests to the current snapshot.

`bound_file_identities` pins the exact bytes of the core sources this slice
ran against. It is a projection of the working tree, not an independent
record, and every edit to a pinned file drifts it. Hand-editing one digest is
how the drift became invisible: a v0.11.0 tag attempt died on this file, and
two runs in one session repeated it.

This prints every rebinding it performs, so a rebind is never silent. It
refuses to touch anything else in the report: corpus identities, case receipt
identities and the checksum set describe frozen fixtures, and a fixture that
changed is a deliberate act with its own review.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))

from malleus.source import source_bytes_digest  # noqa: E402

REPORT = Path(__file__).with_name("FIRST_SLICE_CONFORMANCE_REPORT.json")


def rebind() -> list[tuple[str, str, str, str]]:
    text = REPORT.read_text()
    report = json.loads(text)
    changed: list[tuple[str, str, str, str]] = []
    for group, items in report["bound_file_identities"].items():
        if not isinstance(items, dict):
            continue
        for relative_path, pinned in items.items():
            actual = source_bytes_digest((ROOT / relative_path).read_bytes())
            if actual != pinned:
                changed.append((group, relative_path, pinned, actual))
                text = text.replace(f'"{pinned}"', f'"{actual}"')
    if changed:
        REPORT.write_text(text)
    return changed


if __name__ == "__main__":
    rebindings = rebind()
    for group, relative_path, pinned, actual in rebindings:
        print(f"{group}/{relative_path}\n  was {pinned}\n  now {actual}")
    print(f"{len(rebindings)} binding(s) rebound")
