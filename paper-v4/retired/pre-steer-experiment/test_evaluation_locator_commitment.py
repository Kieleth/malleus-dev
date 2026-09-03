"""Guard the sealed oracle-to-reading locator commitment."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMMITMENT = ROOT / "paper-v4/experiment/evaluation-locator-commitment.json"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_sealed_evaluation_files_and_reading_are_content_bound() -> None:
    value = json.loads(COMMITMENT.read_bytes())
    assert value["status"] == "FROZEN_BEFORE_MODEL_ACQUISITION"
    assert value["review_feedback"] == "FORBIDDEN"
    assert value["review_retry"] == "FORBIDDEN"
    for field in (
        "prior_evaluation_commitment",
        "oracle_locator_binding",
        "support_adjudication_guide",
    ):
        item = value[field]
        path = item.get("path", item.get("sealed_path"))
        assert _digest(ROOT / path) == item["sha256"]
    reading = value["selected_reading"]
    assert _digest(ROOT / reading["manifest_path"]) == reading["manifest_sha256"]
    assert _digest(ROOT / reading["sealed_path"]) == reading["sha256"]


def test_oracle_bindings_name_exact_manifest_blocks() -> None:
    value = json.loads(COMMITMENT.read_bytes())
    manifest = json.loads(
        (ROOT / value["selected_reading"]["manifest_path"]).read_bytes()
    )
    locator = json.loads(
        (ROOT / value["oracle_locator_binding"]["sealed_path"]).read_bytes()
    )
    blocks = {
        block["id"]: block["sha256"]
        for page in manifest["pages"]
        for block in page["blocks"]
    }
    assert [item["question_id"] for item in locator["bindings"]] == [
        "CQ-01",
        "CQ-02",
        "CQ-03",
        "CQ-04",
    ]
    for binding in locator["bindings"]:
        assert binding["blocks"]
        for block in binding["blocks"]:
            assert blocks[block["id"]] == block["sha256"]
