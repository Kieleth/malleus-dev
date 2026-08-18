#!/usr/bin/env python3
"""Regenerate `profile.json` from the authoritative registry in the package.

Run from the repository root. Never hand-edit the output.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from malleus.ocr.verify import profile_projection  # noqa: E402

if __name__ == "__main__":
    target = Path(__file__).with_name("profile.json")
    target.write_text(json.dumps(profile_projection(), indent=2, sort_keys=True) + "\n")
    print(f"wrote {target.relative_to(ROOT)}")
