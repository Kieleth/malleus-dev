"""Recompute the retained paper OCR result and its public boundary."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from malleus.ocr import Bundle, canonical_digest, verify_bundle


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "paper-v4/experiment"
RECEIPT = EXPERIMENT / "ocr-execution-receipt.json"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_retained_ocr_result_matches_its_receipt() -> None:
    receipt = json.loads(RECEIPT.read_bytes())
    outputs = receipt["outputs"]
    inputs = receipt["inputs"]
    bundle_path = ROOT / outputs["bundle_path"]
    verification_path = ROOT / outputs["verification_path"]
    source_path = ROOT / "paper-v4/source/yu-et-al-2025-mid-atlantic-ridge.pdf"

    assert receipt["status"] == "PASS"
    assert receipt["run_class"] == "OFFICIAL_RETAINED_RUN_1"
    assert receipt["exploratory_probe_is_evidence"] is False
    assert _digest(source_path) == inputs["source_sha256"]
    assert source_path.stat().st_size == inputs["source_byte_length"]
    assert _digest(bundle_path) == outputs["bundle_sha256"]
    assert _digest(verification_path) == outputs["verification_sha256"]

    bundle = Bundle.from_document(json.loads(bundle_path.read_bytes()))
    verification = json.loads(verification_path.read_bytes())
    result = verify_bundle(bundle)
    assert result.conforms and result.account.complete
    assert not result.diagnostics
    assert bundle.id == outputs["bundle_id"]
    assert len(bundle.sources) == 1
    assert len(bundle.rasters) == 11
    assert len(bundle.regions) == 11
    assert len(bundle.attempts) == 11
    assert len(bundle.hypotheses) == 11
    assert len(bundle.corrections) == 0
    assert len(bundle.selections) == 11
    assert len(bundle._members()) == receipt["account"]["bundle_members"]
    assert (
        bundle.transport_metadata["retained_sidecars_sha256"]
        == outputs["retained_sidecar_closure_sha256"]
    )
    assert verification["result"]["strict_alignment"] == "PASS"
    assert verification["result"]["account"]["complete"] is True
    assert verification["result"]["account"]["metrics"] == [
        {
            "denominator": "declared_units",
            "family": "page_coverage",
            "threshold": 1.0,
            "value": 1.0,
            "verdict": "MET",
        }
    ]


def test_public_artifacts_bind_every_private_sidecar_without_text() -> None:
    receipt = json.loads(RECEIPT.read_bytes())
    verification_path = ROOT / receipt["outputs"]["verification_path"]
    bundle_path = ROOT / receipt["outputs"]["bundle_path"]
    verification = json.loads(verification_path.read_bytes())
    public_bytes = bundle_path.read_bytes() + verification_path.read_bytes()
    private_files: list[Path] = []

    assert len(verification["sidecars"]) == 11
    assert (
        canonical_digest(verification["sidecars"])
        == receipt["outputs"]["retained_sidecar_closure_sha256"]
    )
    for page in verification["sidecars"]:
        response = ROOT / page["response"]["path"]
        selected = ROOT / page["selected"]["path"]
        for kind in ("raster", "request", "response", "selected"):
            path = ROOT / page[kind]["path"]
            assert path.is_file() and not path.is_symlink()
            assert _digest(path) == page[kind]["sha256"]
            private_files.append(path)
        assert response.read_bytes() == selected.read_bytes()
        assert selected.read_bytes() not in public_bytes

    assert len(private_files) == receipt["outputs"]["retained_sidecar_files"]
    assert (
        sum(path.stat().st_size for path in private_files)
        == receipt["outputs"]["retained_sidecar_bytes"]
    )
    assert verification["publication_boundary"] == {
        "public_text": "DIGEST_ONLY",
        "raw_ocr_text": "PRIVATE_SIDECAR_ONLY",
    }
