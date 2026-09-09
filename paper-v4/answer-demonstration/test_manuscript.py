"""Working-draft consistency, not validation of scientific or review judgments."""

from collections import Counter
import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper-v4"
PRIVATE = ROOT / "private/paper-v4-answer-demonstration"
DRAFT = PAPER / "manuscript-v4-working.md"


def exact_subset(selected, retained):
    if isinstance(selected, dict):
        assert selected
        for key, value in selected.items():
            exact_subset(value, retained[key])
    else:
        assert selected == retained


def test_working_draft_has_no_unresolved_results_and_stays_lean():
    text = DRAFT.read_text()
    assert not re.search(r"\[(?:FINAL|TERMINAL|AFTER THE|RECHECK)\b", text)
    main = text.split("## Appendix A.", 1)[0]
    assert 1700 <= len(main.split()) <= 3500
    assert "—" not in text


@pytest.mark.parametrize(
    "run,label", [("run-20", "Capture A"), ("run-21", "Capture B")]
)
def test_working_result_row_matches_the_frozen_run_and_complete_review(run, label):
    result_path = PAPER / f"experiment-v4/{run}/results/run-result.json"
    review_path = PRIVATE / f"review-01/{run}/review-record.preliminary.md"
    result = json.loads(result_path.read_bytes())
    blocks = re.findall(r"```json\s*(.*?)\s*```", review_path.read_text(), re.S)
    assert len(blocks) == 1, f"Expected one complete review object: {review_path}"
    review = json.loads(blocks[0])
    assert len(review["questions"]) == 30
    assert review["ratification"]["disposition"] == "PENDING"
    counts = Counter(q["question_responsiveness"] for q in review["questions"])
    assert set(counts) <= {"COVERED", "PARTIAL", "NONE"}
    graph = result["graph"]
    values = [
        graph["entities"],
        graph["events"],
        graph["relations"],
        result["ledger_event_count"],
        counts["COVERED"],
        counts["PARTIAL"],
        counts["NONE"],
    ]
    expected = "| " + " | ".join([label, *map(str, values)]) + " |"
    assert expected in DRAFT.read_text()


def test_repair_claims_are_bounded_and_reviews_are_not_human_annotations():
    text = " ".join(DRAFT.read_text().split())
    assert "### 4.4 Two repairs through the same path" in text
    assert "29 of 30 query outputs remain identical" in text
    assert "still does not assemble the geochemical and seismic evidence" in text
    assert "not a matched model comparison" in text
    assert "Human ratification of these selective reviews is pending." in text
    assert "no matched RAG baseline" in text


def test_development_chronology_is_not_the_paper_narrative():
    text = DRAFT.read_text()
    main, supplement = text.split("## Evidence and supplementary experiments", 1)
    assert "Sol-01" not in main
    assert "E-021" not in text
    assert "## 5. Semantic re-entry: the next test" not in text
    for path in [
        "answer-demonstration/REVIEW-RESULTS.md",
        "answer-demonstration/QUERY-CORRECTION.md",
        "answer-demonstration/FOLLOWUP-RESULTS.md",
        "answer-demonstration/SUBJECT-QUERY.md",
    ]:
        assert path in supplement


def test_six_worked_cases_match_complete_review_labels():
    cases = [
        "CQ-T1-02",
        "CQ-T2-01",
        "CQ-T3-02",
        "CQ-T4-01",
        "CQ-T5-01",
        "CQ-C-01",
    ]
    labels = {}
    for run in ["run-20", "run-21"]:
        path = PRIVATE / f"review-01/{run}/review-record.preliminary.md"
        blocks = re.findall(r"```json\s*(.*?)\s*```", path.read_text(), re.S)
        assert len(blocks) == 1
        review = json.loads(blocks[0])
        labels[run] = {
            q["question_id"]: q["question_responsiveness"] for q in review["questions"]
        }
    table = DRAFT.read_text().split("### 4.2 ", 1)[1].split("### 4.3 ", 1)[0]
    rows = [
        line
        for line in table.splitlines()
        if line.startswith("| ") and re.search(r"CQ-[TC]", line)
    ]
    assert [re.search(r"CQ-[TC][0-9]?-\d{2}", row).group() for row in rows] == cases
    for case, row in zip(cases, rows, strict=True):
        assert "?" in row.split("|")[1], "Show the question, not only its identifier"
        assert [cell.strip() for cell in row.split("|")[2:4]] == [
            labels[run][case] for run in ["run-20", "run-21"]
        ]


def test_examples_show_question_specific_coverage_and_two_meanings_of_none():
    text = " ".join(DRAFT.read_text().split())
    assert "Same record, different question." in text
    assert "No sulfur/chlorine values" in text
    assert "NONE despite returning three rows" in text
    assert "A PARTIAL witness contributes none of its fields" in text
    for requirement in (
        "causal_mechanism",
        "supporting_observation",
        "geochemical_evidence",
        "seismic_evidence",
        "evidence_relation",
    ):
        assert f"| {requirement} |" in text


def test_repair_examples_bind_displayed_fields_to_unchanged_query_outputs():
    text = " ".join(DRAFT.read_text().split())
    root = PRIVATE / "repair-02"
    result = json.loads((root / "funding/attempt-01/query-result.json").read_bytes())
    query = next(q for q in result["queries"] if q["question_id"] == "CQ-T2-05")
    row = next(
        r
        for r in query["rows"]
        if r["witness"]["relation_id"] == "repair:funding:erc-funds-singh"
    )
    assert row["relation"]["award_identifier"] == ["339442_TransAtlanticILAB"]
    assert "339442_TransAtlanticILAB" in text
    assert row["target"]["name"] in text
    result = json.loads((root / "evidence/attempt-01/query-result.json").read_bytes())
    query = next(q for q in result["queries"] if q["question_id"] == "CQ-T5-01")
    edge = next(r for r in query["rows"] if r["kind"] == "RELATION")
    assert edge["source"]["value_lower"] == edge["source"]["value_upper"] == 25
    assert edge["source"]["unit"] == "km"
    assert edge["source"]["determination"] == "MODELLED"
    assert "approximately 25 km" in text
    assert "not an observed earthquake depth" in text


def test_draft_evidence_inputs_are_declared_for_the_isolated_gate():
    manifest = json.loads((PAPER / "active-test-manifest.json").read_bytes())
    assert (
        "private/paper-v4-answer-demonstration" in manifest["private_fixture_patterns"]
    )


def test_working_draft_local_evidence_links_resolve():
    links = re.findall(r"\]\(([^)]+)\)", DRAFT.read_text())
    assert links
    for target in links:
        if "://" not in target:
            assert (DRAFT.parent / target.split("#", 1)[0]).is_file(), target


def test_appendix_record_extracts_are_exact_subsets_of_retained_outputs():
    text = DRAFT.read_text().split("## Appendix A.", 1)[1].split("## Appendix B.", 1)[0]
    extracts = [json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", text, re.S)]
    baseline = json.loads((PRIVATE / "pilot-03/run-21/query-result.json").read_bytes())
    queries = {q["question_id"]: q for q in baseline["queries"]}
    capture = json.loads(
        (PRIVATE / "review-01/run-21/retained-capture.json").read_bytes()
    )
    evidence = json.loads(
        (PRIVATE / "repair-02/evidence/attempt-01/query-result.json").read_bytes()
    )
    funding = json.loads(
        (PRIVATE / "repair-02/funding/attempt-01/query-result.json").read_bytes()
    )
    older = json.loads((PRIVATE / "pilot-03/run-20/query-result.json").read_bytes())
    sources = [
        queries["CQ-T1-02"]["rows"][0],
        next(a for a in capture["assertions"] if a["id"] == "assertion:175"),
        queries["CQ-T3-02"]["rows"][0],
        queries["CQ-T4-01"]["rows"][0],
        queries["CQ-T5-01"],
        next(q for q in evidence["queries"] if q["question_id"] == "CQ-T5-01")["rows"][
            1
        ],
        queries["CQ-T2-05"]["rows"][0],
        next(
            r
            for q in funding["queries"]
            if q["question_id"] == "CQ-T2-05"
            for r in q["rows"]
            if r["witness"]["relation_id"] == "repair:funding:erc-funds-singh"
        ),
        next(
            r
            for q in older["queries"]
            if q["question_id"] == "CQ-T4-04"
            for r in q["rows"]
            if r["witness"]["record_id"] == "claim:no-active-vents-rc2"
        ),
        queries["CQ-C-01"],
    ]

    assert len(extracts) == len(sources) == 10
    for selected, retained in zip(extracts, sources, strict=True):
        exact_subset(selected, retained)


def test_composition_appendix_prints_both_new_witnesses_without_rewriting_them():
    text = DRAFT.read_text().split("## Appendix B.", 1)[1]
    extracts = [json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", text, re.S)]
    result = json.loads(
        (PRIVATE / "composition-01/evidence/attempt-01/query-result.json").read_bytes()
    )
    query = next(q for q in result["queries"] if q["question_id"] == "CQ-T5-01")
    witnesses = query["rows"][1:]
    assert len(extracts) == len(witnesses) == 2
    for selected, retained in zip(extracts, witnesses, strict=True):
        exact_subset(selected, retained)
        assert selected["witness"] == retained["witness"]
        assert selected["source"]["assertion_modality"] in {"CALCULATED", "MEASURED"}
        assert selected["target"]["assertion_modality"] == "HYPOTHESISED"
    requirements = next(
        q
        for q in json.loads(
            (PAPER / "experiment-v4/competency-questions-v3.json").read_bytes()
        )["questions"]
        if q["id"] == query["question_id"]
    )["required_semantics"]
    positions = [text.index("| " + requirement + " |") for requirement in requirements]
    assert positions == sorted(positions)


def test_composition_claim_is_separate_and_binds_its_own_replay_identity():
    text = " ".join(DRAFT.read_text().split())
    assert "### 4.5 One task-directed composition test" in text
    assert "not a controlled test of question conditioning" in text
    assert "answer-demonstration/COMPOSITION-RESULTS.md" in text
    appendix = text.split("## Appendix B.", 1)[1]
    result = json.loads(
        (PRIVATE / "composition-01/evidence/attempt-01/run-result.json").read_bytes()
    )
    for identity in (result["ledger_head"], result["artifacts"]["replay-receipt.json"]):
        assert identity.removeprefix("sha256:") in appendix
    assert "HUMAN RATIFICATION PENDING" in appendix


def test_appendix_quotes_resolve_and_labels_remain_preliminary():
    text = " ".join(DRAFT.read_text().split("## Appendix A.", 1)[1].split())
    reading = json.loads(
        (ROOT / "private/paper-v4-text-layer/selected-reading.json").read_bytes()
    )
    blocks = {
        b["id"]: " ".join(b["text"].split())
        for p in reading["pages"]
        for b in p["blocks"]
    }
    quotes = re.findall(
        r'\*\*Source excerpt, (page:\d+:block:\d+):\*\* "([^"]+)"',
        " ".join(text.split()),
    )
    assert len(quotes) == 6
    for locator, quote in quotes:
        assert quote in blocks[locator], (locator, quote)
    assert "HUMAN RATIFICATION PENDING" in text
    assert "not a complete reproduction package" in text
    assert "unshown fields are omitted, not null" in text
    assert "CC BY-NC-ND 4.0" in text


def test_appendix_identity_and_count_trace_match_retained_evidence():
    text = DRAFT.read_text().split("## Appendix A.", 1)[1]
    result = json.loads(
        (PAPER / "experiment-v4/run-21/results/run-result.json").read_bytes()
    )
    query = json.loads((PRIVATE / "pilot-03/run-21/query-result.json").read_bytes())
    reading = json.loads(
        (ROOT / "private/paper-v4-text-layer/selected-reading.json").read_bytes()
    )
    for digest in [
        reading["source_sha256"],
        result["reading_sha256"],
        result["ontology_sha256"],
        result["ledger_head"],
        result["replay_receipt_sha256"],
        query["inputs"]["binding_program_sha256"],
        query["inputs"]["query_program_sha256"],
    ]:
        assert digest.removeprefix("sha256:") in text
    assert result["admitted_receipt_sha256"] == result["replay_receipt_sha256"]
    assert result["reopen_matches_admitted"] == {
        "export_records": True,
        "receipt": True,
    }
    trace = json.loads(
        (PRIVATE / "review-01/run-21/population-trace.json").read_bytes()
    )
    record = next(
        r for r in trace["records"] if r["record_id"] == "obs:obs-network-size-methods"
    )
    for field in ("count", "count_scope"):
        derivations = [
            d for d in record["derivations"] if d["path"] == ["properties", field]
        ]
        assert len(derivations) == 1
        assert derivations[0]["locator"] == "assertion:175"
    assert (
        record["sources"]["source:yu-2025-mid-atlantic-ridge"]
        == result["reading_sha256"]
    )


def test_appendix_spatial_and_hypothesis_prose_are_returned_not_new_answers():
    text = " ".join(DRAFT.read_text().split("## Appendix A.", 1)[1].split())
    query = json.loads((PRIVATE / "pilot-03/run-21/query-result.json").read_bytes())
    queries = {q["question_id"]: q for q in query["queries"]}
    for question_id in ("CQ-T2-01", "CQ-T4-01"):
        statement = " ".join(
            queries[question_id]["rows"][0]["record"]["statement"].split()
        )
        # The spatial quote omits only the final figure citation, declared in prose.
        if question_id == "CQ-T2-01":
            statement = statement.split(" (Figs.", 1)[0]
        assert statement in text
    assert queries["CQ-T4-01"]["rows"] == queries["CQ-T5-01"]["rows"]
