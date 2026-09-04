from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from malleus.ocr.verify import profile_registry


ROOT = Path(__file__).resolve().parents[2]
PRECOMMIT = ROOT / "paper-v4/experiment/ocr-precommit.json"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_ocr_precommit_binds_source_profile_inventory_and_policy() -> None:
    freeze = json.loads(PRECOMMIT.read_bytes())
    source = freeze["source"]
    source_manifest = json.loads((ROOT / source["manifest"]).read_bytes())
    profile = freeze["malleus_ocr"]
    source_class = freeze["source_class"]
    policies = freeze["policies"]

    assert set(freeze) == {
        "schema",
        "frozen_at",
        "status",
        "source",
        "malleus_ocr",
        "source_class",
        "renderer",
        "reader",
        "selector",
        "selection",
        "policies",
        "retention",
        "execution",
    }
    assert freeze["schema"] == "malleus.paper-v4.ocr-precommit/v1"
    assert freeze["status"] == "FROZEN_BEFORE_RETAINED_READING"
    assert source["sha256"] == source_manifest["artifact"]["sha256"]
    assert source["byte_length"] == source_manifest["artifact"]["byte_length"]
    assert source["page_count"] == source_manifest["artifact"]["page_count"] == 11
    assert _digest(ROOT / source["path"]) == source["sha256"]
    assert _digest(ROOT / profile["ontology_path"]) == profile["ontology_sha256"]
    assert (
        "sha256:" + profile_registry().content_hash()
        == profile["registry_content_hash"]
    )
    assert source_class["required_units"] == [f"page:{page}" for page in range(1, 12)]
    assert source_class["metric_families"] == {
        "page_coverage": {"denominator": "declared_units", "threshold": 1.0}
    }
    assert source_class["frozen_at"] == freeze["frozen_at"]
    assert policies["data_handling"]["id"]
    assert policies["hostile_content"]["id"]
    assert freeze["reader"]["confidence_policy"] == "OMIT_UNCALIBRATED_CONFIDENCE"
    assert freeze["selection"]["human_verified"] is False
    assert freeze["execution"] == {
        "network": "forbidden",
        "embedded_pdf_text_layer": "forbidden",
        "pdftotext": "forbidden",
        "preprocessing": "none",
        "retries": 0,
        "final_output_on_partial_failure": "forbidden",
        "reproducibility_status": (
            "LOCAL_EXACT_BINARIES_PINNED; CLEAN_CONTAINER_PENDING"
        ),
    }


def test_ocr_precommit_names_exact_local_tool_bytes() -> None:
    freeze = json.loads(PRECOMMIT.read_bytes())

    for tool in (freeze["renderer"], freeze["reader"]):
        executable = Path(tool["executable"])
        assert executable.is_absolute()
        assert _digest(executable) == tool["binary_sha256"]
    traineddata = Path(freeze["reader"]["traineddata_path"])
    assert traineddata.is_absolute()
    assert _digest(traineddata) == freeze["reader"]["traineddata_sha256"]
    assert "pdftotext" not in freeze["renderer"]["single_page_arguments"]
    assert "pdftotext" not in freeze["reader"]["arguments"]
