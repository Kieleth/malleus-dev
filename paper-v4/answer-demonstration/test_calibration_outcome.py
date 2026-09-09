"""Retain the calibration outcomes without equating graph size with coverage."""

import json

from calibration import BASE
from input_delivery import input_frames, transcript_evidence, verify_frames
from review_packet import digest


RUN = BASE.parent / "sol-calibration-01/b"


def test_complete_ultra_delivery_precedes_authoring():
    rows = json.loads((RUN / "delivery-evidence.json").read_bytes())
    launch = json.loads((RUN / "launch.json").read_bytes())
    assert len(rows) == 79
    assert all(row["timestamp"] < "2026-09-07T18:52:58.254Z" for row in rows)
    outputs = transcript_evidence(rows, launch)
    expected = [f for group in input_frames(RUN, "initial").values() for f in group]
    assert len(expected) == 74
    verify_frames(expected, outputs)


def test_ultra_first_submission_and_exact_reproduction_remain_bound():
    attempt = RUN / "attempt-01"
    result = json.loads((attempt / "run-result.json").read_bytes())
    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert result["replay_matches_preclose"]
    assert result["graph"] == {
        "entities": 138,
        "relations": 20,
        "events": 1,
        "signals": 0,
        "event_participations": 0,
    }
    assert (
        digest((attempt / "submitted-population.json").read_bytes())
        == (result["submitted_population_sha256"])
    )
    for name, identity in result["artifacts"].items():
        assert digest((attempt / name).read_bytes()) == identity
    originals = {
        str(path.relative_to(attempt)): path.read_bytes()
        for path in attempt.rglob("*")
        if path.is_file()
    }
    repeated = {
        str(path.relative_to(RUN / "reproduction-01")): path.read_bytes()
        for path in (RUN / "reproduction-01").rglob("*")
        if path.is_file()
    }
    assert len(originals) == 12
    assert originals == repeated


def test_scoped_values_exist_outside_the_frozen_returned_rows():
    attempt = RUN / "attempt-01"
    graph = json.loads((attempt / "export-records.json").read_bytes())
    nodes = {node["id"]: node["properties"] for node in graph["entities"]}
    query = json.loads((attempt / "query-result.json").read_bytes())
    questions = {item["question_id"]: item for item in query["queries"]}
    ids = {
        f"observation:{site}-primary-{basis}"
        for site in ("rc2", "rc3")
        for basis in ("rb90", "ba90")
    }
    for key in ids:
        node = nodes[key]
        assert type(node["value_lower"]) is float
        assert type(node["value_upper"]) is float
        subject = nodes[node["subject"]]
        assert subject["name"] == "primary melts"
        assert subject["tags"] in (["segment RC2"], ["segment RC3"])
    for key in ("CQ-T3-02", "CQ-T5-02", "CQ-C-05"):
        assert not ids & set(questions[key]["witness_ids"])
    assert nodes["count:obs-network"]["count"] == 19
    assert questions["CQ-T1-02"]["outcome"] == "NO_CANDIDATE"
    assert not questions["CQ-T1-02"]["rows"]


def test_complete_census_is_not_a_proof_of_source_content_absence():
    attempt = RUN / "attempt-01"
    census = json.loads((attempt / "census.json").read_bytes())
    capture = json.loads((attempt / "submitted-population.json").read_bytes())[
        "capture"
    ]
    reading = json.loads((RUN / "producer/inputs/selected-reading.json").read_bytes())
    blocks = {
        block["id"]: block for page in reading["pages"] for block in page["blocks"]
    }
    assert census["blocks_untouched"] == 0
    assert census["blocks_reviewed"] == census["blocks_total"] == len(blocks)
    key = "page:5:block:005"
    assert key in capture["nothing_assertable"]
    assert "CO2(calculated)" in blocks[key]["text"]
    assert "segment RC2" in blocks[key]["text"]
    assert "segment RC3" in blocks[key]["text"]
    assert not [a for a in capture["assertions"] if a["block"] == key]


def test_existing_subject_reader_recovers_the_four_hidden_estimates():
    from answers import answer
    from subject_answers import SubjectGraphReads
    from test_answers import Graph

    exported = json.loads((RUN / "attempt-01/export-records.json").read_bytes())
    graph = Graph(
        [
            {"id": node["id"], "type": node["type"], **node["properties"]}
            for node in exported["entities"]
        ]
    )
    surface = json.loads((RUN / "producer/inputs/population-surface.json").read_bytes())
    reads = SubjectGraphReads(graph, surface)
    expected = {
        f"observation:{site}-primary-{basis}"
        for site in ("rc2", "rc3")
        for basis in ("rb90", "ba90")
    }
    for key in ("CQ-T3-02", "CQ-T5-02"):
        diagnostic = answer(reads, key)
        assert len(diagnostic["rows"]) == 5
        assert expected <= set(diagnostic["witness_ids"])


def test_complete_ultra_review_is_bound_and_unratified():
    from collections import Counter
    from selective_review import validate

    packet = RUN / "review-01"
    record = validate(packet, packet / "review-record.md")
    assert record["ratification"]["disposition"] == "PENDING"
    assert len(record["witnesses"]) == 28
    assert len(record["questions"]) == 30
    assert sum(len(q["coverage"]) for q in record["questions"]) == 121
    assert Counter(q["question_responsiveness"] for q in record["questions"]) == {
        "COVERED": 3,
        "PARTIAL": 11,
        "NONE": 16,
    }
