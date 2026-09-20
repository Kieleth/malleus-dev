"""Preserve observed reader evidence, not an automated semantic score."""

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from beam_readers import validate_answers


RUN = Path(__file__).resolve().parents[3] / "private/beam-weather-calibration-01"


@pytest.mark.parametrize("condition", ["graph", "source"])
def test_frozen_answers_and_actual_input_delivery(condition):
    root = RUN / "readers-01" / condition
    audit = json.loads((RUN / "readers-01/audit.json").read_bytes())["readers"][
        condition
    ]
    launch = json.loads((root / "launch.json").read_bytes())
    spec = importlib.util.spec_from_file_location("delivery", RUN / "input_delivery.py")
    delivery = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(delivery)
    rows = [
        json.loads(line)
        for line in Path(launch["metadata_source"]).read_text().splitlines()
    ]
    outputs = delivery.transcript_evidence(rows, launch)
    frame_counts = {}
    for item in json.loads((root / "manifest.json").read_bytes())["inputs"]:
        raw = (root / item["path"]).read_bytes()
        assert "sha256:" + hashlib.sha256(raw).hexdigest() == item["sha256"]
        if item["full_read"]:
            frames = delivery.frames(item["path"], raw)
            delivery.verify_frames(frames, outputs)
            frame_counts[item["path"]] = len(frames)
    assert frame_counts == audit["required_frames"]
    assert sum(frame_counts.values()) == audit["required_frame_count"]
    raw = (root / "work/answers.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == audit["answer_sha256"]
    assert (
        validate_answers(
            raw,
            (root / "questions.json").read_bytes(),
            (root / "evidence.json").read_bytes(),
            condition,
        )
        == audit["mechanical_validation"]
    )
    assert audit["mechanical_validation"]["semantic_support"] == "NOT_CHECKED"
    assert launch["model"] == audit["model"] == "gpt-5.6-sol"
    assert launch["reasoning_effort"] == audit["effort"] == "low"
    assert sum(row["type"] == "compacted" for row in rows) == audit["compactions"] == 0


def test_reported_representation_witnesses_are_the_frozen_bytes():
    artifacts = json.loads((RUN / "producer/work/artifacts.json").read_bytes())
    # Resolve retained artifacts from the producer manifest, not guessed filenames.
    population = json.loads(Path(artifacts["population"]).read_bytes())
    records = json.loads(Path(artifacts["records"]).read_bytes())
    entities = {r["id"]: r for r in records["entities"]}
    assertions = {a["id"]: a for a in population["capture"]["assertions"]}
    edges = {r["id"]: r for r in records["relations"]}
    ratio = entities["ratio:beam:2273"]["properties"]
    assert ratio["ratio_value"] == 0.78
    assert "API integration" not in json.dumps(ratio)
    assert "API integration" in assertions[ratio["assertion_locator"]]["statement"]
    edge = edges["relation:beam:6505"]
    prior = entities[edge["target_id"]]["properties"]
    assert prior["proposition_status"] == "REQUEST"
    assert "simple counter" in assertions[prior["assertion_locator"]]["statement"]
    assert "obtained" not in assertions[prior["assertion_locator"]]["statement"]
    rows = json.loads((RUN / "readers-01/graph/work/answers.json").read_bytes())[
        "answers"
    ]
    citations = [c for row in rows for c in row["evidence"]]
    assert len(citations) == 62
    assert sum(c["path"] == ["properties", "quantity_kind"] for c in citations) == 55
    assert sum(c["locator"] == "quantity:beam:2138" for c in citations) == 36
    assert (
        len(
            [
                row
                for row in rows
                if any(c["locator"] == "quantity:beam:2138" for c in row["evidence"])
            ]
        )
        == 10
    )
