"""Recompute the frozen selected-reading projection result."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "paper-v4/experiment/reading-projection-receipt.json"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_projection_result_matches_receipt_and_exposes_no_text() -> None:
    receipt = json.loads(RECEIPT.read_bytes())
    inputs = receipt["inputs"]
    outputs = receipt["outputs"]
    paths = {
        "projection_precommit_sha256": ROOT
        / "paper-v4/experiment/reading-projection-precommit.json",
        "ocr_precommit_sha256": ROOT / "paper-v4/experiment/ocr-precommit.json",
        "ocr_bundle_sha256": ROOT / "paper-v4/experiment/ocr-bundle.json",
        "ocr_verification_sha256": ROOT / "paper-v4/experiment/ocr-verification.json",
        "source_sha256": ROOT / "paper-v4/source/yu-et-al-2025-mid-atlantic-ridge.pdf",
    }
    assert receipt["status"] == "PASS"
    for field, path in paths.items():
        assert _digest(path) == inputs[field]

    private_path = ROOT / outputs["private_reading_path"]
    public_path = ROOT / outputs["public_manifest_path"]
    assert _digest(private_path) == outputs["private_reading_sha256"]
    assert _digest(public_path) == outputs["public_manifest_sha256"]
    assert private_path.stat().st_size == outputs["private_reading_bytes"]
    assert public_path.stat().st_size == outputs["public_manifest_bytes"]

    private = json.loads(private_path.read_bytes())
    public = json.loads(public_path.read_bytes())
    assert private["block_count"] == public["block_count"] == outputs["blocks"]
    assert len(private["pages"]) == len(public["pages"]) == outputs["pages"]
    private_blocks = [block for page in private["pages"] for block in page["blocks"]]
    public_blocks = [block for page in public["pages"] for block in page["blocks"]]
    assert len(private_blocks) == len(public_blocks) == outputs["blocks"]
    assert all("text" in block for block in private_blocks)
    assert all("text" not in block for block in public_blocks)
    assert public["private_reading"]["sha256"] == outputs["private_reading_sha256"]
    assert public["publication_boundary"] == {"public_text": "DIGEST_ONLY"}
    assert not any(
        block["text"].encode() in public_path.read_bytes() for block in private_blocks
    )
