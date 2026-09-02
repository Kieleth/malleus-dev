#!/usr/bin/env python3
"""Refuse live rebinding of the immutable first-slice report."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "FIRST_SLICE_CONFORMANCE_REPORT.json is an immutable dated snapshot; "
        "validate its recorded bytes instead of rebinding it to current files.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
