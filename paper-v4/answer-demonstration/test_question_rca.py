"""Keep graph inventory separate from failures of the frozen answer instrument.

These checks reproduce historical misses. They do not alter queries or labels.
They prevent the RCA from regressing to a claim that absent rows mean absent facts.
"""

import json
from pathlib import Path

from binding import load_query_program
from test_answers import Graph


PRIVATE = Path(__file__).resolve().parents[2] / "private/paper-v4-answer-demonstration"


def frozen_followup():
    base = PRIVATE / "followup-sol-01"
    binding = json.loads((base / "query-binding.acceptance.json").read_bytes())
    program = load_query_program(
        base / "frozen-code/answers.py", binding["query_program_sha256"]
    )
    records = json.loads((base / "attempt-01/export-records.json").read_bytes())
    surface = json.loads(
        (base / "producer/inputs/population-surface.json").read_bytes()
    )
    # Export envelopes nest properties; GraphReads consumes flat query nodes.
    # This is an instrument-only fixture, not a replacement Core graph loader.
    graph = Graph(
        [
            {"id": node["id"], "type": node["type"], **node["properties"]}
            for node in records["entities"]
        ]
    )
    return program, program.GraphReads(graph, surface)


def test_correct_site_depth_exists_despite_query_selecting_other_site():
    program, reads = frozen_followup()
    rc2 = reads.graph.get_node("obs:rc2-depth")
    ntd2 = reads.graph.get_node("obs:ntd2-depth")
    assert rc2["subject"] != ntd2["subject"]
    assert all(type(rc2[k]) in (int, float) for k in ("value_lower", "value_upper"))
    result = program.answer(reads, "CQ-T3-01")
    assert "obs:rc2-depth" not in result["witness_ids"]
    assert "obs:ntd2-depth" in result["witness_ids"]
    assert "microseismicity" in program.text_of(rc2)
    assert not program.contains(program.text_of(rc2), "seismicity")


def test_two_site_scoped_carbon_values_exist_but_comparison_query_misses_them():
    program, reads = frozen_followup()
    ids = ("obs:rc2-melt-co2", "obs:rc3-melt-co2")
    nodes = [reads.graph.get_node(key) for key in ids]
    assert len({node["subject"] for node in nodes}) == 2
    for node in nodes:
        assert all(
            type(node[k]) in (int, float) for k in ("value_lower", "value_upper")
        )
        assert node["unit"]
        assert node["assertion_modality"] == "CALCULATED"
        assert not program.contains(program.text_of(node), "primary melt")
    result = program.answer(reads, "CQ-T5-02")
    assert not set(ids) & set(result["witness_ids"])


def test_campaign_count_exists_despite_deployment_filter():
    program, reads = frozen_followup()
    campaign = reads.graph.get_node("campaign:smarties-2019")
    assert type(campaign["count"]) is int
    assert not program.answer(reads, "CQ-T1-02")["rows"]


def test_control_paraphrases_are_not_independent_query_programs():
    program, _ = frozen_followup()
    assert program.PROGRAMS["CQ-C-04"] is program.PROGRAMS["CQ-T1-02"]
    assert program.PROGRAMS["CQ-C-05"] is program.PROGRAMS["CQ-T3-02"]


def test_latest_surface_cannot_supply_the_date_or_award_slots():
    from review_packet import digest

    base = PRIVATE / "sol-e2e-corrected-01"
    manifest = json.loads((base / "manifest.json").read_bytes())
    # Definition paths must come from acceptance, not a guessed accepted/ folder.
    accepted = (base / manifest["ontology_path"]).resolve()
    assert accepted.is_relative_to(base.resolve())
    assert digest(accepted.read_bytes()) == manifest["ontology_sha256"]
    surface = json.loads(
        (
            PRIVATE / "sol-e2e-corrected-01/producer/accepted/population-surface.json"
        ).read_bytes()
    )
    slots = {slot["name"] for item in surface["record_types"] for slot in item["slots"]}
    assert not {"accepted_date", "award_identifier"} & slots
