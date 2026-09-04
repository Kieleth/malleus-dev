"""Guard the fresh ontology-session inputs before acquisition."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRECOMMIT = ROOT / "paper-v4/experiment/model-acquisition-precommit.json"
RETENTION = ROOT / "paper-v4/experiment/model-acquisition-input-retention.json"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_model_acquisition_uses_only_content_bound_inputs() -> None:
    value = json.loads(PRECOMMIT.read_bytes())
    retention = json.loads(RETENTION.read_bytes())
    retained = {item["original_path"]: item for item in retention["retained_inputs"]}
    assert value["status"] == "FROZEN_BEFORE_MODEL_ACQUISITION"
    assert value["stage"] == "ONTOLOGY_PROPOSAL"
    assert value["session"]["kind"] == "NEW_CODEX_TASK"
    assert value["session"]["prior_conversation"] == "NONE"
    assert value["session"]["model"] == "gpt-5.6-sol"
    assert value["session"]["reasoning_effort"] == "high"
    drifted = []
    for item in (value["prompt"], value["task_contract"], *value["allowed_inputs"]):
        current = _digest(ROOT / item["path"])
        if current == item["sha256"]:
            continue
        drifted.append(item["path"])
        record = retained[item["path"]]
        retained_path = ROOT / record["retained_path"]
        assert record["original_sha256"] == item["sha256"]
        assert _digest(retained_path) == record["retained_sha256"] == item["sha256"]
        assert len(retained_path.read_bytes()) == record["retained_byte_length"]
        assert current == record["current_sha256"]
        assert record["reason"] == (
            "AUTHORITATIVE_CORE_REBIND_AFTER_COMPLETED_PRIMARY_ACQUISITION"
        )
    assert drifted == ["docs/IMPLEMENTATION_STATUS.md"]
    assert retention["status"] == "POST_ACQUISITION_CORE_REBIND"
    assert retention["original_core_commit"] == (
        "1611944eb8856dbd4f25c2ea8bddbecdb970a3a3"
    )
    assert retention["current_core_commit"] == (
        "92ae0af8cb65a46aba0431372e3573a5642c2622"
    )


def test_model_acquisition_excludes_evaluator_and_ambient_access() -> None:
    value = json.loads(PRECOMMIT.read_bytes())
    allowed = {item["path"] for item in value["allowed_inputs"]}
    assert len(allowed) == 7
    assert not any("evaluation" in path or "oracle" in path for path in allowed)
    assert value["tool_policy"] == {
        "file_reads": "ALLOWLIST_ONLY",
        "file_writes": "FORBIDDEN",
        "network": "FORBIDDEN",
        "shell": "READ_ONLY_HASH_AND_FILE_INSPECTION_OF_ALLOWLIST",
        "subtasks": "FORBIDDEN",
    }
    policy = value["correction_policy"]
    assert policy["structural_compiler_retries_after_initial_proposal"] == 2
    assert policy["same_session_required"] is True
    assert policy["restart"] == "FORBIDDEN"
    assert policy["best_of_session_selection"] == "FORBIDDEN"
    assert policy["hidden_adequacy_review_attempts"] == 1
    assert policy["hidden_review_feedback"] == "FORBIDDEN"
    assert policy["retry_after_hidden_review"] == "FORBIDDEN"
