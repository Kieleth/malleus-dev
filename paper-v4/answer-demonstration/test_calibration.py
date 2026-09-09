"""The calibration must not silently change more than its declared effort arm."""

from copy import deepcopy
import json

import pytest


def test_pair_preserves_every_original_input_and_primary_query(tmp_path):
    from calibration import BASE, packet_files, check_files

    original = json.loads((BASE / "manifest.json").read_bytes())
    a, b = (packet_files(tmp_path / arm) for arm in ("a", "b"))
    for name in original["producer_inputs"]:
        assert a["producer/" + name] == b["producer/" + name]
        assert a["producer/" + name] == (BASE / "producer" / name).read_bytes()
    for name in ("frozen-code/answers.py", "query-binding.acceptance.json"):
        assert a[name] == b[name] == (BASE / name).read_bytes()
    assert a["producer-task.md"].replace(str(tmp_path / "a").encode(), b"ARM") == (
        b["producer-task.md"].replace(str(tmp_path / "b").encode(), b"ARM")
    )
    check_files(tmp_path / "a", a)


@pytest.mark.parametrize(
    "name",
    [
        "producer/inputs/ontology.yaml",
        "producer/inputs/selected-reading.json",
        "producer/.claude/skills/malleus-acolyte/SKILL.md",
        "frozen-code/answers.py",
        "producer-task.md",
    ],
)
def test_changed_condition_cannot_be_blessed_by_its_own_manifest(tmp_path, name):
    from calibration import packet_files, check_files

    run = tmp_path / "a"
    files = packet_files(run)
    files[name] += b"\nchanged"
    with pytest.raises(ValueError, match="calibration input differs"):
        check_files(run, files)


@pytest.mark.parametrize(
    "name",
    [
        "producer/inputs/questions.json",
        "producer/inputs/prior-population.json",
    ],
)
def test_undeclared_producer_material_refuses(tmp_path, name):
    from calibration import packet_files, check_files

    run = tmp_path / "a"
    files = packet_files(run)
    files[name] = b"{}"
    with pytest.raises(ValueError, match="closure"):
        check_files(run, files)


def test_settings_are_explicit_and_arm_specific():
    from calibration import check_launch

    launch = {"model": "gpt-5.6-sol", "reasoning_effort": "low", "fork_turns": "none"}
    check_launch("a", launch)
    check_launch("b", {**launch, "reasoning_effort": "ultra"})
    for key, value in (
        ("model", "other"),
        ("reasoning_effort", "ultra"),
        ("fork_turns", "all"),
    ):
        bad = deepcopy(launch)
        bad[key] = value
        with pytest.raises(ValueError, match="explicit calibration settings"):
            check_launch("a", bad)
    with pytest.raises(KeyError):
        check_launch("a", {"model": "gpt-5.6-sol"})


def test_calibration_uses_existing_observed_delivery_guard():
    from calibration import check_launch
    from input_delivery import transcript_evidence, verify_frames, frames

    launch = {
        "model": "gpt-5.6-sol",
        "reasoning_effort": "ultra",
        "fork_turns": "none",
        "thread_id": "new",
    }
    check_launch("b", launch)
    rows = [
        {"type": "session_meta", "payload": {"id": "new"}},
        {"type": "turn_context", "payload": {"model": "gpt-5.6-sol", "effort": "low"}},
    ]
    with pytest.raises(ValueError, match="observed producer setting"):
        transcript_evidence(rows, launch)
    with pytest.raises(ValueError, match="incomplete model-visible delivery"):
        verify_frames(frames("reading", b"exact source"), ["I read everything"])


def test_actual_low_submission_never_satisfies_delivery_at_its_frozen_cut():
    from calibration import BASE
    from input_delivery import input_frames, transcript_evidence, verify_frames
    from review_packet import digest

    run = BASE.parent / "sol-calibration-01/a"
    refusal = json.loads((run / "delivery-refusal.json").read_bytes())
    launch = json.loads((run / "launch.json").read_bytes())
    evidence = (run / "delivery-evidence.json").read_bytes()
    assert digest(evidence) == refusal["delivery_evidence_sha256"]
    rows = json.loads(evidence)
    expected = input_frames(run, "initial")
    outputs = transcript_evidence(rows, launch)
    with pytest.raises(ValueError, match="incomplete model-visible delivery"):
        verify_frames([f for group in expected.values() for f in group], outputs)
    parts = expected[refusal["missing_target"]]
    verify_frames(parts[:5], outputs)
    for part in refusal["missing_parts"]:
        with pytest.raises(ValueError, match="incomplete model-visible delivery"):
            verify_frames([parts[part - 1]], outputs)


def test_low_delivery_cut_omits_the_compiled_domain_type_definitions():
    from calibration import BASE
    from input_delivery import CHUNK_CHARS

    run = BASE.parent / "sol-calibration-01/a"
    refusal = json.loads((run / "delivery-refusal.json").read_bytes())
    source = (run / "producer/inputs/population-surface.json").read_text()
    key = '"record_types": ['
    offset = source.index(key) + len(key)
    decoder, intervals = json.JSONDecoder(), {}
    while True:
        while source[offset].isspace() or source[offset] == ",":
            offset += 1
        if source[offset] == "]":
            break
        value, end = decoder.raw_decode(source, offset)
        intervals[value["name"]] = (offset, end)
        offset = end
    boundary = CHUNK_CHARS * (min(refusal["missing_parts"]) - 1)
    assert [name for name, (_, end) in intervals.items() if end <= boundary] == (
        refusal["complete_surface_types_delivered"]
    )
    for name, parts in refusal["undelivered_examples"].items():
        start, end = intervals[name]
        assert start >= boundary
        assert [start // CHUNK_CHARS + 1, (end - 1) // CHUNK_CHARS + 1] == parts
