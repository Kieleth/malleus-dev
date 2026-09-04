"""Mechanical guard for the selected source bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "paper-v4" / "source" / "source-manifest.json"


def test_selected_source_bytes_match_the_freeze() -> None:
    manifest = json.loads(MANIFEST.read_bytes())
    assert manifest["schema"] == "malleus.paper-v4.source-freeze/v1"
    assert manifest["doi"] == "10.1038/s41467-024-55792-9"
    assert manifest["license"]["identifier"] == "CC-BY-NC-ND-4.0"

    artifact = manifest["artifact"]
    source = (ROOT / artifact["path"]).read_bytes()
    assert source.startswith(b"%PDF-1.4")
    assert len(source) == artifact["byte_length"]
    assert "sha256:" + hashlib.sha256(source).hexdigest() == artifact["sha256"]
