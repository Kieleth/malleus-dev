"""Audit accounting must not substitute source text for graph meaning."""

from copy import deepcopy
import json
from pathlib import Path
import re
import subprocess
import sys

import pytest


def fixture():
    def record(key, **properties):
        return {"id": key, "type": "Claim", "properties": properties}

    graph = {"entities": [record("a", subject="b"), record("b", name="site")]}
    surface = {
        "record_types": [
            {
                "name": "Claim",
                "qualified_name": "urn:Claim",
                "slots": [
                    {"name": "subject", "range_id": "urn:Claim", "multivalued": False},
                    {"name": "name", "range_id": "urn:String", "multivalued": False},
                ],
            }
        ]
    }
    reading = {"pages": [{"blocks": [{"id": "block", "text": "First. Second."}]}]}
    capture = {
        "assertions": [
            {
                "id": "first",
                "block": "block",
                "statement": "First.",
                "modality": "STATED",
                "formalized_by": [
                    {"record_id": "a", "path": ["properties", "subject"]}
                ],
            },
            {
                "id": "second",
                "block": "block",
                "statement": "Second.",
                "modality": "STATED",
                "formalized_by": [
                    {"record_id": "a", "path": ["properties", "subject"]}
                ],
            },
        ]
    }
    return graph, surface, capture, reading


def test_keeps_all_field_sources_separate_from_record_content():
    from meaning_audit import inventory

    rows = inventory(*fixture(), targets={"a"})
    row = rows[0]
    assert row["record"] == fixture()[0]["entities"][0]
    assert [s["assertion_id"] for s in row["sources"]] == ["first", "second"]
    assert "statement" not in row["record"]["properties"]
    assert row["neighbors"]["b"]["properties"]["name"] == "site"
    assert "assessment" not in row


def test_report_prose_style_allows_markdown_table_separators():
    for name in (
        "MEANING-AUDIT.md",
        "MEANING-REPAIR-PLAN.md",
        "meaning-repair-task.md",
    ):
        lines = (Path(__file__).parent / name).read_text().splitlines()
        prose = "\n".join(line for line in lines if not re.fullmatch(r"[| :\-]+", line))
        assert "\u2014" not in prose and "--" not in prose


def test_reference_walk_uses_declarations_not_strings_or_ids():
    from meaning_audit import references, replacement_closure

    graph, surface, _, _ = fixture()
    graph["entities"][1]["properties"]["name"] = "a"
    refs = references(graph, surface)
    assert refs == [
        {"record_id": "a", "path": ["properties", "subject"], "target_id": "b"}
    ]
    assert replacement_closure({"b"}, refs) == {"a", "b"}
    assert replacement_closure({"a"}, refs) == {"a"}


def test_closure_includes_multivalued_header_and_transitive_dependencies():
    from meaning_audit import references, replacement_closure

    graph, surface, _, _ = fixture()
    surface["record_types"][0]["slots"].append(
        {"name": "refs", "range_id": "urn:Claim", "multivalued": True}
    )
    graph["entities"].append(
        {"id": "c", "type": "Claim", "properties": {"refs": ["a"]}}
    )
    graph["entities"].append(
        {"id": "d", "type": "Claim", "subject": "c", "properties": {}}
    )
    assert replacement_closure({"b"}, references(graph, surface)) == {
        "a",
        "b",
        "c",
        "d",
    }


@pytest.mark.parametrize(
    "fault",
    [
        "missing_target",
        "duplicate_record",
        "duplicate_assertion",
        "missing_assertion_field",
        "wrong_block",
        "wrong_source_text",
        "wrong_field_path",
        "unknown_record",
        "unknown_type",
        "dangling_reference",
        "wrong_reference_shape",
        "shadowed_header",
    ],
)
def test_refuses_incomplete_or_ambiguous_audit_inputs(fault):
    from meaning_audit import inventory

    graph, surface, capture, reading = deepcopy(fixture())
    targets = {"a"}
    if fault == "missing_target":
        targets.add("absent")
    elif fault == "duplicate_record":
        graph["entities"].append(graph["entities"][0])
    elif fault == "duplicate_assertion":
        capture["assertions"].append(capture["assertions"][0])
    elif fault == "missing_assertion_field":
        del capture["assertions"][0]["modality"]
    elif fault == "wrong_block":
        capture["assertions"][0]["block"] = "absent"
    elif fault == "wrong_source_text":
        capture["assertions"][0]["statement"] = "Invented."
    elif fault == "wrong_field_path":
        capture["assertions"][0]["formalized_by"][0]["path"] = ["properties", "absent"]
    elif fault == "unknown_record":
        capture["assertions"][0]["formalized_by"][0]["record_id"] = "absent"
    elif fault == "unknown_type":
        graph["entities"][0]["type"] = "absent"
    elif fault == "dangling_reference":
        graph["entities"][0]["properties"]["subject"] = "absent"
    elif fault == "wrong_reference_shape":
        graph["entities"][0]["properties"]["subject"] = ["b"]
    elif fault == "shadowed_header":
        graph["entities"][0]["subject"] = "a"
    with pytest.raises(ValueError):
        inventory(graph, surface, capture, reading, targets=targets)


def test_exact_fresh_run_has_76_audited_records_and_existing_site_paths():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_meaning_audit import check_fresh; check_fresh()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_fresh():
    from event_query import BASE, inputs
    from followup import checked_bytes
    from meaning_audit import inventory, references, replacement_closure

    attempt, expected, surface, _ = inputs()
    graph = json.loads(
        checked_bytes(
            (attempt / "public/export-records.json").read_bytes(),
            expected["export_records_sha256"],
            "audit graph",
        )
    )
    capture = json.loads(
        checked_bytes(
            (attempt / "ledger/retained-capture.json").read_bytes(),
            expected["capture"]["capture_sha256"],
            "audit capture",
        )
    )
    reading = json.loads(
        checked_bytes(
            (BASE / "producer/inputs/selected-reading.json").read_bytes(),
            expected["reading_sha256"],
            "audit reading",
        )
    )
    types = {
        "ScientificClaim",
        "ScientificObservation",
        "CountObservation",
        "RatioObservation",
    }
    targets = {r["id"] for r in graph["entities"] if r["type"] in types}
    rows = inventory(graph, json.loads(surface), capture, reading, targets=targets)
    assert len(rows) == 76
    assert sum(r["record"]["type"] == "ScientificClaim" for r in rows) == 37
    claims = [r for r in rows if r["record"]["type"] == "ScientificClaim"]
    assert all(
        not {"statement", "name", "description"} & r["record"]["properties"].keys()
        for r in claims
    )
    mechanism = next(r for r in rows if r["record"]["id"] == "claim:co2-mechanism")
    assert {s["block"] for s in mechanism["sources"]} == {
        "page:1:block:001",
        "page:5:block:002",
    }
    refs = references(graph, json.loads(surface))
    closure = replacement_closure(targets, refs)
    assert closure - targets == {
        r["id"]
        for r in graph["relations"]
        if r["source_id"] in targets or r["target_id"] in targets
    }
    rels = {r["id"]: r for r in graph["relations"]}
    assert rels["relation:deep-at-rc2"]["target_id"] == "feature:rc2"
    assert rels["relation:deep-beneath-axis"]["target_id"] == "feature:mar-axis"
    # Do not import the older graph's useful-instrument count into this run.
    assert not any(r["properties"].get("count") == 17 for r in graph["entities"])
    audit = (Path(__file__).parent / "MEANING-AUDIT.md").read_text()
    claim_table = audit.split("## All 37 claims\n", 1)[1].split(
        "## All 39 quantitative records", 1
    )[0]
    observation_table = audit.split("## All 39 quantitative records\n", 1)[1].split(
        "## Why this happens", 1
    )[0]
    for prefix, table in (("claim:", claim_table), ("observation:", observation_table)):
        listed = [
            prefix + name
            for name in re.findall(r"^\| ([a-z][a-z0-9-]+) \|", table, re.M)
        ]
        assert len(listed) == len(set(listed))
        assert set(listed) == {key for key in targets if key.startswith(prefix)}
