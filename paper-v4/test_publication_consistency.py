"""Mechanical guards for claims duplicated across the paper-v4 publications."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper-v4"
MANUSCRIPT = PAPER / "manuscript.md"
TEX = PAPER / "arxiv/main.tex"
README = PAPER / "arxiv/README.md"
QUERY_RESULT = PAPER / "experiment-v2/results/query-result.json"
BUILD_RESULT = PAPER / "experiment-v2/results/experiment-result.json"
COMPILE_RECEIPT = PAPER / "experiment-v2/ontology-run/compilation/compile-receipt.json"
# The reproducer tag pins the v2 and v3 runs only. The v4 run-02 single-producer
# run has no tag: it lives at the commit that carries paper-v4/experiment-v4/run-02/,
# and the publications must say so rather than name a coordinate that does not exist.
REPRODUCER_TAG = "paper-v4-multimodel-v2"
V3_RUNS = PAPER / "experiment-v3/runs"
RUN02 = PAPER / "experiment-v4/run-02"
RUN03 = PAPER / "experiment-v4/run-03"
SHOP = (
    ROOT
    / "research/ontology_driven_kg_realization/experiments/small_shop/public_population"
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_publication_claims_match_frozen_v2_results() -> None:
    query = json.loads(QUERY_RESULT.read_bytes())
    build = json.loads(BUILD_RESULT.read_bytes())
    compile_receipt = json.loads(COMPILE_RECEIPT.read_bytes())

    assert [len(item["rows"]) for item in query["queries"]] == [0, 2, 4, 0]
    assert query["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert (build["entity_count"], build["relation_count"]) == (7, 6)
    assert compile_receipt["fact_count"] == 4146
    assert {item["module_id"] for item in compile_receipt["sources"]} == {
        "linkml:types",
        "malleus",
        "paper-v4:mid-ocean-ridge-geodynamics",
    }

    for publication in (MANUSCRIPT, TEX):
        body = _text(publication)
        assert "holds 4,146 facts" in body
        assert "seven entities and six relations" in body
        assert "Eighteen anchor events retaining the contract, sources and evidence, plus a five-event atomic admission batch" in body
        assert REPRODUCER_TAG in body
        for stale in (
            "UNSCORABLE_ORACLE_SCHEMA_MISMATCH",
            "Admission produced a 23-event history",
            "24-event history",
            "eight entities and six relations",
            "8e818103e6867e326544123a30abe756bdd45117",
            "4,146-fact validated import closure",
        ):
            assert stale not in body


def test_arxiv_citations_and_reproduction_coordinate_are_closed() -> None:
    tex = _text(TEX)
    bibliography = _text(PAPER / "arxiv/references.bib")
    keys = set(re.findall(r"@\w+\{([^,]+),", bibliography))
    citations = {
        key
        for group in re.findall(r"\\citep\{([^}]+)\}", tex)
        for key in group.split(",")
    }

    assert citations == keys
    assert REPRODUCER_TAG in _text(README)
    for path in (MANUSCRIPT, TEX, README):
        body = _text(path)
        assert "TODO" not in body
        assert "TBD" not in body
        assert "PLACEHOLDER" not in body


def test_publication_claims_match_frozen_v3_producer_results() -> None:
    expected = {
        "claude-sonnet-5": ("1,738", "8 / 8", "0, 0, 0, 0"),
        "claude-opus-5": ("3,869", "20 / 18", "0, 0, 0, 1"),
    }
    for run_id, (facts, classes, rows) in expected.items():
        run = V3_RUNS / run_id
        query = json.loads((run / "results/query-result.json").read_bytes())
        ontology = json.loads((run / "ontology-run/acquisition-record.json").read_bytes())
        assert [len(item["rows"]) for item in query["queries"]] == [
            int(value) for value in rows.split(", ")
        ]
        assert sum(query["forbidden_attempts"].values()) == 0
        assert f"{ontology['attempts'][-1]['fact_count']:,}" == facts
        for publication in (MANUSCRIPT, TEX):
            body = _text(publication)
            assert facts in body
            assert classes in body
            assert rows in body


def test_publication_claims_match_the_calibration_fixture() -> None:
    """Section 4.1 states the shop fixture's counts; they come from its evidence."""

    evidence = json.loads((SHOP / "evidence.json").read_bytes())

    assert evidence["history"]["change_set_count"] == 5
    assert evidence["contract_revision"]["count"] == 1
    assert evidence["history"]["ledger_event_count"] == 48
    assert evidence["record_counts"] == {"current": 9, "historical": 10}
    assert len(evidence["records"]) == 10
    assert len({record["population_plan"]["plan_id"] for record in evidence["records"]}) == 5
    assert len(
        {
            source["record_id"]
            for record in evidence["records"]
            for source in record["sources"]
        }
    ) == 5
    assert [
        record["record_id"]
        for record in evidence["records"]
        if record["supersedes_record_id"]
    ] == ["supplier-order-state:B:e7"]
    assert [
        record["record_id"]
        for record in evidence["records"]
        if record["superseded_by"]
    ] == ["supplier-order-state:B:e4"]
    assert all(record["derivations"] for record in evidence["records"])

    for publication in (MANUSCRIPT, TEX):
        body = _text(publication)
        assert "five accepted change sets and one additive contract revision" in body
        assert "48 ledger events, nine current and ten historical records" in body
        assert "five source files" in body


def test_publications_match_the_refused_run_03_cell() -> None:
    """The run-03 row and its narrative must match the frozen refusal record."""

    assert not (RUN03 / "results/run-result.json").exists()

    ontology = json.loads((RUN03 / "ontology-run/result.json").read_bytes())
    assert ontology["status"] == "REFUSED_AFTER_DIAGNOSTIC_BUDGET"
    assert ontology["population_started"] is False
    assert ontology["accepted_ontology_sha256"] is None
    assert [item["status"] for item in ontology["attempts"]] == ["REFUSED"] * 3
    assert {item["stage"] for item in ontology["attempts"]} == {"PACK_GROUNDING"}
    assert [item["reason"] for item in ontology["attempts"]] == [
        "DIRECT_ROOT_GROUNDING_REQUIRED",
        "GROUNDING_NOT_CLOSED",
        "GROUNDING_INCOMPLETE",
    ]
    assert ontology["attempts"][0]["subjects"] == 10
    assert ontology["terminal_diagnostic"]["reason"] == "GROUNDING_INCOMPLETE"

    # The first two gates are the ones run-02 met, in the same order.
    run02 = json.loads((RUN02 / "ontology-run/result.json").read_bytes())
    assert [item.get("reason") for item in run02["attempts"][:2]] == [
        item["reason"] for item in ontology["attempts"][:2]
    ]

    for publication in (MANUSCRIPT, TEX):
        body = _text(publication)
        assert "in progress" not in body
        assert "refused at ontology stage" in body
        assert (
            "All three permitted ontology attempts were refused at the "
            "pack-grounding rite, both diagnostic returns were used, no "
            "ontology was accepted, and population never started"
        ) in body
        assert (
            "The two cells of the current protocol hit the same first two "
            "grounding gates in the same order"
        ) in body
        assert "each of these gates reports one entry at a time" in body
        assert (
            "its second cell was refused at the ontology stage by a grounding "
            "rite that reports one defect at a time"
        ) in body
        assert "paper-v4/experiment-v4/run-03/ontology-run/" in body


def test_publication_claims_match_frozen_v4_run_02_results() -> None:
    ontology = json.loads((RUN02 / "ontology-run/result.json").read_bytes())
    run = json.loads((RUN02 / "results/run-result.json").read_bytes())
    census = json.loads((RUN02 / "results/census.json").read_bytes())
    binding = json.loads((RUN02 / "results/native-query-binding.json").read_bytes())
    query_trace = json.loads((RUN02 / "results/query-trace-summary.json").read_bytes())
    trace = json.loads((RUN02 / "results/trace-summary.json").read_bytes())
    withheld = json.loads((RUN02 / "results/withheld-artifacts.json").read_bytes())

    assert ontology["status"] == "ACCEPTED"
    assert [item["status"] for item in ontology["attempts"]] == [
        "REFUSED",
        "REFUSED",
        "ACCEPTED",
    ]
    assert [item.get("reason") for item in ontology["attempts"][:2]] == [
        "DIRECT_ROOT_GROUNDING_REQUIRED",
        "GROUNDING_NOT_CLOSED",
    ]
    assert ontology["attempts"][0]["subjects"] == 10
    assert ontology["accepted"]["fact_count"] == 3515
    assert ontology["accepted"]["population_surface_families"] == {
        "ENTITY": 26,
        "RELATION": 3,
    }

    assert run["status"] == "ADMITTED_AND_REPLAYED"
    assert run["ledger_event_count"] == 14
    assert run["records_traced"] == 589
    assert run["graph"] == {
        "entities": 419,
        "event_participations": 0,
        "events": 0,
        "relations": 170,
        "signals": 0,
    }
    assert run["reopen_matches_admitted"] == {"export_records": True, "receipt": True}

    assert census["assertions"] == {
        "FULLY_FORMALIZED": 226,
        "PARTLY_FORMALIZED": 103,
        "UNFORMALIZED": 0,
    }
    assert sum(census["assertions"].values()) == 329
    assert census["blocks_reviewed"] == census["blocks_total"] == 186
    assert census["gaps_by_kind"] == {
        "AGGREGATE_ONLY": 84,
        "INTERVAL_NOT_EXPRESSIBLE": 1,
        "RELATION_ABSENT": 3,
        "TYPE_ABSENT": 16,
    }
    assert sum(census["gaps_by_kind"].values()) == 104

    assert binding["status"] == "FROZEN_AFTER_REPLAY"
    assert sum(len(item["cases"]) for item in binding["queries"]) == 21
    assert query_trace["witnesses_traced"] == len(query_trace["records"]) == 126

    # Section 4.5 states how much of the admitted graph the binding reaches.
    witnesses = {item["record_id"] for item in query_trace["records"]}
    admitted = {item["record_id"] for item in trace["records"]}
    assert len(admitted) == run["records_traced"] == 589
    assert witnesses <= admitted
    assert len(admitted - witnesses) == 463
    named_types = {
        case[key]
        for query in binding["queries"]
        for case in query["cases"]
        for key in (
            "source_record_type",
            "relation_record_type",
            "target_record_type",
            "record_type",
        )
        if case.get(key)
    }
    assert len(named_types) == 13
    assert named_types == {item["record_type"] for item in query_trace["records"]}

    # Section 4.4 credits the source-assertion profile with carrying modality.
    assert sum(
        any(
            derivation["path"][-1] == "assertion_modality"
            for derivation in item["derivations"]
        )
        for item in trace["records"]
    ) == 194

    # The four row counts live only in the withheld query result, because its
    # projected fields quote the reading. The file is named and digest-pinned
    # here; the counts themselves are pinned as literal prose below.
    assert len(withheld["withheld"]) == 8
    assert {item["name"] for item in withheld["withheld"]} == {
        "population-plan.json",
        "gaps.json",
        "replay-receipt.json",
        "export-records.json",
        "query-result.json",
        "document-population.json",
        "retained-capture.json",
        "history.jsonl",
    }
    assert all(item["sha256"].startswith("sha256:") for item in withheld["withheld"])

    for publication in (MANUSCRIPT, TEX):
        body = _text(publication)
        assert "3,515 compiled facts" in body
        assert "26 concrete entity types and 3 relation types" in body
        assert (
            "329 verbatim assertions with their modality, 419 entity records, "
            "170 relation records, and 104 typed gaps"
        ) in body
        assert (
            "all 186 blocks reviewed, 226 assertions fully formalized, "
            "103 partly formalized, and none unformalized"
        ) in body
        assert "deleted 41 of its own" in body
        assert "One change set entered a 14-event ledger." in body
        assert (
            "Each of the 589 records traces to the assertion and the block "
            "it was read from."
        ) in body
        assert "21 cases over the same four questions" in body
        assert (
            "returned 4, 32, 34, and 3 rows for CQ1 through CQ4, with 126 "
            "witness records each traced"
        ) in body
        assert "an ontology accepted at 3,515 facts" in body
        assert "a type-only binding written after replay returned 4, 32, 34, and 3 rows" in body
        assert "Seven of the 16" in body
        assert "gaps state that the population surface holds no Event record type" in body
        assert "zero events and zero event participations" in body
        assert (
            "The 21 cases name 13 record types and reach 126 of the 589 "
            "admitted records as witnesses. The remaining 463 are in the graph"
        ) in body
        assert (
            "194 of the 589 admitted records carry an assertion-modality derivation"
        ) in body
        assert (
            "Eight files are therefore withheld from this repository and "
            "published by digest only"
        ) in body
        assert (
            "preliminary until the human author ratifies it"
        ) in body
        assert "This run has no reproducer tag" in body
        assert "4881b3a040aaafc7600d009a16ae910084ae32c2" in body

    for publication in (MANUSCRIPT, TEX, README):
        body = _text(publication)
        assert "paper-v4/experiment-v4/run-02/" in body
        assert REPRODUCER_TAG in body
        assert "run-02-v1" not in body
        assert "paper-v4-run-02" not in body

