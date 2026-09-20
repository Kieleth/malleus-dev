"""Verify the selected private source packet. Missing evidence fails loudly."""

import json
import subprocess
import sys
from pathlib import Path

from beam_prepare import (
    canonical,
    check_questions,
    prepare,
    project_chat,
    unpack_source,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRIVATE = ROOT / "private" / "beam-weather-calibration-01"
PINS = json.loads((HERE / "source-pins.json").read_bytes())


def source():
    return (PRIVATE / "upstream" / "conversation-archive.json").read_bytes()


def test_frozen_reading_reproduces_all_exact_source_text_and_roles():
    raw = unpack_source(source(), PINS["conversation"])
    original = json.loads(raw)
    reading, locators = project_chat(raw)
    assert len(locators) == 200
    for page in reading["pages"]:
        for block in page["blocks"]:
            item = locators[block["ordinal"]]
            parts = item["json_pointer"].split("/")
            message = original[int(parts[1])]["turns"][int(parts[3])][int(parts[4])]
            assert (
                block["text"] == f"[speaker={message['role']}]\n" + message["content"]
            )
            assert item["message_id"] == message["id"]
    assert [len(page["blocks"]) for page in reading["pages"]] == [72, 62, 66]


def test_packet_rebuild_matches_frozen_bytes():
    outputs = prepare(source(), PINS["conversation"])
    for name, raw in outputs.items():
        assert raw == (PRIVATE / "reading-packet" / name).read_bytes()
    assert set(outputs) == {"reading.json", "source-map.json", "input-manifest.json"}
    assert outputs == prepare(source(), PINS["conversation"])


def test_all_twenty_question_rubrics_and_references_have_structural_closure():
    raw = unpack_source(
        (PRIVATE / "evaluation" / "questions-archive.json").read_bytes(),
        PINS["evaluation"],
    )
    _, locators = project_chat(unpack_source(source(), PINS["conversation"]))
    report = check_questions(raw, {item["message_id"] for item in locators})
    assert report["questions"] == 20
    assert report["source_references"] == 55
    assert len(report["categories"]) == 10
    assert set(report["categories"].values()) == {2}
    assert report["semantic_review"] == "NOT_PERFORMED"


def test_cli_refuses_overwriting_prior_packet(tmp_path):
    output = tmp_path / "existing"
    output.mkdir()
    sentinel = output / "reading.json"
    sentinel.write_bytes(b"prior evidence")
    result = subprocess.run(
        [
            sys.executable,
            str(HERE / "beam_prepare.py"),
            "--archive",
            str(PRIVATE / "upstream" / "conversation-archive.json"),
            "--pins",
            str(HERE / "source-pins.json"),
            "--output",
            str(output),
        ],
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert sentinel.read_bytes() == b"prior evidence"
    assert list(output.iterdir()) == [sentinel]


def test_bad_source_refuses_before_any_output(tmp_path):
    archive = json.loads(source())
    archive["content"] += " "
    bad = tmp_path / "corrupt.json"
    bad.write_bytes(canonical(archive))
    output = tmp_path / "must-not-exist"
    result = subprocess.run(
        [
            sys.executable,
            str(HERE / "beam_prepare.py"),
            "--archive",
            str(bad),
            "--pins",
            str(HERE / "source-pins.json"),
            "--output",
            str(output),
        ],
        capture_output=True,
        check=False,
    )
    assert result.returncode != 0
    assert b"SOURCE_LENGTH_MISMATCH" in result.stderr
    assert not output.exists()
