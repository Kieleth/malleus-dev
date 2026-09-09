"""Current adoption must not silently become historical replication."""

from copy import deepcopy
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
PRIVATE = ROOT / "private/paper-v4-answer-demonstration"


@pytest.mark.parametrize(
    "run_id", ["overnight-sol-01", "overnight-sol-02", "sol-e2e-01", "sol-e2e-02"]
)
def test_accepted_core_guidance_rejects_regressed_actual_packets(run_id):
    from current_adoption import check_guidance

    skill = PRIVATE / run_id / "producer/.claude/skills/malleus-acolyte/SKILL.md"
    with pytest.raises(ValueError, match="accepted capture guidance"):
        check_guidance(skill.read_bytes())


def test_accepted_core_guidance_accepts_the_earlier_corrected_packet():
    from current_adoption import check_guidance

    check_guidance(
        (
            PRIVATE / "followup-sol-01/producer/.claude/skills/malleus-acolyte/SKILL.md"
        ).read_bytes()
    )


def test_current_condition_changes_only_the_skill_of_the_eight_inputs():
    from current_adoption import make_manifest, verify_inputs, input_bytes

    manifest = make_manifest("sol-e2e-corrected-01")
    files = input_bytes(manifest)
    verify_inputs(manifest, files)
    original = json.loads(
        (
            ROOT / "paper-v4/experiment-v4/run-21/producer-input-manifest.json"
        ).read_bytes()
    )
    changed = [
        a["name"]
        for a, b in zip(manifest["declared_inputs"], original["declared_inputs"])
        if a != b
    ]
    assert changed == ["MALLEUS_NASCENT_PROJECT_SKILL"]
    assert len(files) == 8
    assert manifest["producer"]["reasoning_effort"] == "low"
    assert "PRIOR_ONTOLOGY" in manifest["producer"]["forbidden_inputs"]
    for key, value in (("model_id", "other"), ("reasoning_effort", "high")):
        wrong = deepcopy(manifest)
        wrong["producer"][key] = value
        with pytest.raises(ValueError, match="producer setting"):
            verify_inputs(wrong, files)
    for value in (
        {**files, "inputs/ontology.yaml": b"prior"},
        {**files, "inputs/research.yaml": b"changed"},
    ):
        with pytest.raises(ValueError):
            verify_inputs(manifest, value)
    wrong = deepcopy(manifest)
    wrong["core"] = original["core"]
    with pytest.raises(ValueError, match="selected current-adoption Core"):
        verify_inputs(wrong, files)
    wrong = deepcopy(manifest)
    del wrong["producer"]["reasoning_effort"]
    with pytest.raises(KeyError):
        verify_inputs(wrong, files)


def test_manifest_cannot_redeclare_changed_bytes_as_the_accepted_condition():
    from current_adoption import make_manifest, verify_inputs, input_bytes
    from review_packet import digest

    manifest = make_manifest("sol-e2e-corrected-01")
    files = input_bytes(manifest)
    files["inputs/research.yaml"] = b"changed"
    for item in manifest["declared_inputs"]:
        if item["target"] == "inputs/research.yaml":
            item["sha256"] = digest(b"changed")
    with pytest.raises(ValueError, match="declared input condition"):
        verify_inputs(manifest, files)


def test_delivery_requires_complete_exact_frames_not_only_names_or_digests():
    from input_delivery import frames, verify_frames

    data = ("α actual source text\n" * 1000).encode()
    expected = frames("inputs/source.json", data)
    assert len(expected) > 1
    assert all(len(frame) < 6500 for frame in expected)
    verify_frames(expected, expected)
    verify_frames(expected, [json.dumps({"output": x}) for x in expected])
    for outputs in (
        expected[:-1],
        [x[:100] for x in expected],
        ["read all"],
        [x.replace("actual", "other") for x in expected],
    ):
        with pytest.raises(ValueError, match="incomplete model-visible delivery"):
            verify_frames(expected, outputs)


def test_delivery_evidence_ignores_non_tool_messages_and_checks_observed_settings():
    from input_delivery import transcript_evidence

    rows = [
        {"type": "session_meta", "payload": {"id": "thread:a"}},
        {"type": "turn_context", "payload": {"model": "gpt-5.6-sol", "effort": "low"}},
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": "not tool evidence",
            },
        },
        {
            "type": "response_item",
            "payload": {
                "type": "function_call_output",
                "output": "exact tool evidence",
            },
        },
    ]
    launch = {
        "thread_id": "thread:a",
        "model": "gpt-5.6-sol",
        "reasoning_effort": "low",
        "fork_turns": "none",
    }
    assert transcript_evidence(rows, launch) == ["exact tool evidence"]
    wrong = deepcopy(rows)
    wrong[1]["payload"]["effort"] = "high"
    with pytest.raises(ValueError, match="observed producer setting"):
        transcript_evidence(wrong, launch)
    with pytest.raises(ValueError, match="observed producer setting"):
        transcript_evidence([rows[0], *rows[2:]], launch)


def test_delivery_reads_actual_custom_tool_text_blocks_without_reasoning():
    from input_delivery import transcript_evidence

    rows = [
        {"type": "session_meta", "payload": {"id": "thread:a"}},
        {"type": "turn_context", "payload": {"model": "gpt-5.6-sol", "effort": "low"}},
        {
            "type": "response_item",
            "payload": {"type": "reasoning", "summary": "not delivery"},
        },
        {
            "type": "response_item",
            "payload": {
                "type": "custom_tool_call_output",
                "output": [
                    {"type": "input_text", "text": "tool envelope\n"},
                    {"type": "input_text", "text": "exact frame"},
                ],
            },
        },
    ]
    launch = {
        "thread_id": "thread:a",
        "model": "gpt-5.6-sol",
        "reasoning_effort": "low",
        "fork_turns": "none",
    }
    assert transcript_evidence(rows, launch) == ["tool envelope\nexact frame"]


def test_delivery_helper_and_dispatch_text_cannot_drift_after_freeze(tmp_path):
    from current_adoption import verify_control_files
    from review_packet import digest

    for name in ("input_delivery.py", "spawn-message.md"):
        (tmp_path / name).write_bytes(name.encode())
    (tmp_path / "staging-check.json").write_text(
        json.dumps(
            {
                "delivery_helper_sha256": digest(b"input_delivery.py"),
                "spawn_message_sha256": digest(b"spawn-message.md"),
            }
        )
    )
    verify_control_files(tmp_path)
    for name in ("input_delivery.py", "spawn-message.md"):
        (tmp_path / name).write_bytes(b"changed")
        with pytest.raises(ValueError, match="fixed input differs"):
            verify_control_files(tmp_path)
        (tmp_path / name).write_bytes(name.encode())
