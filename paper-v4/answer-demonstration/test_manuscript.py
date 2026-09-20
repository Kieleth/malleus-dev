"""Working-draft consistency against frozen cells, not validation of judgments."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper-v4"
DRAFT = PAPER / "manuscript-v4-working.md"
CELLS = ["run-20", "run-21", "run-22", "run-23", "run-24"]
V3_CELLS = ["run-22", "run-23", "run-24"]
# The review table reports run-22 under both query binders; the v4.13 row is
# the record the coverage figures rest on. Directory name -> (table label, cell
# whose run contract binds the question file).
REPORTED = [
    ("run-22", "run-22, v4.12 binder", "run-22"),
    ("run-22-v413", "run-22, v4.13 binder", "run-22"),
    ("run-23", "run-23", "run-23"),
    ("run-24", "run-24", "run-24"),
]
COVERAGE_CELLS = ["run-22-v413", "run-23", "run-24"]
V32_CELL = "run-26"
CONTROL = "run-25"
BASELINE = "baseline-01"
ADMISSION = (
    [(run, run) for run in CELLS]
    + [(CONTROL, "run-25, fixed ontology"), (V32_CELL, "run-26")]
)
REPORTED = REPORTED + [
    (CONTROL, "run-25, fixed ontology", CONTROL),
    (V32_CELL, "run-26, under the next protocol", V32_CELL),
]
# Every graph cell the paper reports its coverage for.
GRAPH_CELLS = COVERAGE_CELLS + [CONTROL, V32_CELL]
EXHIBIT_CELL = "run-23"
PRIVATE_EXHIBIT_CELL = ROOT / "private/paper-v4-v4-run-23"


def text():
    return DRAFT.read_text()


def prose():
    return " ".join(DRAFT.read_text().split())


def review(run):
    record = (PAPER / f"evaluation-v4/{run}/review-record.preliminary.md").read_text()
    blocks = re.findall(r"```json\s*(.*?)\s*```", record, re.S)
    return json.loads(blocks[-1])


def run_result(run):
    return json.loads((PAPER / f"experiment-v4/{run}/results/run-result.json").read_bytes())


def ontology_result(run):
    return json.loads((PAPER / f"experiment-v4/{run}/ontology-run/result.json").read_bytes())


def launch_log(run):
    return json.loads((PAPER / f"experiment-v4/{run}/results/launch-log.json").read_bytes())


def positive(questions):
    return [q for q in questions if not q["question_id"].startswith("CQ-C")]


def exact_subset(selected, retained):
    if isinstance(selected, dict):
        assert selected and isinstance(retained, dict)
        for key, value in selected.items():
            assert key in retained, key
            exact_subset(value, retained[key])
    elif isinstance(selected, list):
        assert isinstance(retained, list) and len(selected) == len(retained)
        for left, right in zip(selected, retained, strict=True):
            exact_subset(left, right)
    else:
        assert selected == retained


def is_exact_subset(selected, retained):
    try:
        exact_subset(selected, retained)
    except AssertionError:
        return False
    return True


def test_working_draft_stays_lean_and_free_of_placeholders():
    body = text()
    assert not re.search(r"\[(?:FINAL|TERMINAL|AFTER THE|RECHECK|VALUE)\b", body)
    main = body.split("## Appendix A.", 1)[0]
    # Luis, 2026-09-11: the 3,500-word figure of D4 is a guideline, not a
    # requirement. Only a floor remains, so a truncated draft cannot pass.
    assert len(main.split()) >= 1700
    assert "—" not in body


def test_development_chronology_is_not_the_paper_narrative():
    body = text()
    assert "E-0" not in body
    assert "Sol" not in body
    assert not re.search(r"\brun-(0[2-9]|1[0-9])\b", body)
    assert "Eighteen earlier development cells" in prose()


@pytest.mark.parametrize("run,label", ADMISSION)
def test_admission_table_row_matches_the_frozen_cell(run, label):
    result = run_result(run)
    ontology = ontology_result(run)
    log = launch_log(run)
    usage = json.loads((PAPER / f"experiment-v4/{run}/results/usage.json").read_bytes())
    graph = result["graph"]
    facts = f"{ontology['accepted']['fact_count']:,}"
    gaps = sum(result["gaps_by_kind"].values())
    reopen = "yes" if all(result["reopen_matches_admitted"].values()) else "no"
    expected = (
        f"| {label} | {facts} | {graph['entities']} / {graph['relations']} | {gaps} | "
        f"{len(log['runner'])} | {result['ledger_event_count']} | {reopen} | "
        f"{usage['producer_total_tokens']:,} |"
    )
    assert expected in text(), expected


def absences(record):
    reached = 0
    causes = Counter()
    for q in positive(record["questions"]):
        for c in q["coverage"]:
            if c["row_index"] is None:
                causes[c["absent_reason"]] += 1
            else:
                reached += 1
    assert reached + sum(causes.values()) == 102
    return reached, causes


@pytest.mark.parametrize("directory,label,contract_cell", REPORTED)
def test_review_table_row_matches_the_validated_record(directory, label, contract_cell):
    record = review(directory)
    support = Counter(w["source_support"] for w in record["witnesses"])
    assert support["UNSUPPORTED"] == 0 and support["NOT_EVALUABLE"] == 0
    labels = Counter(q["question_responsiveness"] for q in positive(record["questions"]))
    reached, causes = absences(record)
    protocol = record["schema"].rsplit("/", 1)[1]
    if protocol == "v3.2":
        pair = f"{causes['NOT_MODELLED']} and {causes['NOT_CAPTURED']}"
    else:
        assert "NOT_CAPTURED" not in causes, "the code does not exist under v3"
        pair = f"{causes['NOT_MODELLED']} and no code"
    expected = (
        f"| {label} | {reached} | {support['SUPPORTED']} / {support['PARTIAL']} | "
        f"{labels['COVERED']} / {labels['PARTIAL']} / {labels['NONE']} | "
        f"{pair} | {causes['WITHHELD_STATEMENT']} | "
        f"{causes['UNREACHED_RECORD']} | {controls_matched(directory, contract_cell)} |"
    )
    assert expected in text(), expected


def test_rebind_paragraph_matches_both_retained_attempts():
    first = json.loads(
        re.findall(
            r"```json\s*(.*?)\s*```",
            (PAPER / "evaluation-v4/run-22-v413/review-record.preliminary.attempt-01.md").read_text(),
            re.S,
        )[-1]
    )
    second = review("run-22-v413")
    body = prose()
    for record, controls in ((first, 2), (second, 5)):
        reached, _ = absences(record)
        assert f"{reached} of 102" in body
        assert f"controls {controls} of 5" in body
        assert controls_matched_record(record, "run-22") == controls
    s1 = Counter(w["source_support"] for w in first["witnesses"])
    s2 = Counter(w["source_support"] for w in second["witnesses"])
    assert (s1["SUPPORTED"], s1["PARTIAL"], s2["SUPPORTED"], s2["PARTIAL"]) == (456, 1, 457, 0)
    assert "456 and 457 of 457" in body
    assert (PAPER / "evaluation-v4/review-task-v3-clarification-2026-09-12.md").is_file()


def test_earlier_protocol_cells_are_reported_in_prose():
    body = prose()
    for run in ("run-20", "run-21"):
        record = review(run)
        support = Counter(row["source_support"] for q in record["questions"] for row in q["rows"])
        assert support["UNSUPPORTED"] == 0
        labels = Counter(q["question_responsiveness"] for q in record["questions"])
        assert f"{support['SUPPORTED']} of {sum(support.values())} rows" in body, run
        assert labels["RESPONSIVE"] + labels["PARTIAL"] == 4


@pytest.mark.parametrize("run", CELLS + [CONTROL, V32_CELL])
def test_admission_replay_and_provenance_claims_hold_in_every_cell(run):
    result = run_result(run)
    ontology = ontology_result(run)
    census = result["census"]
    assert ontology["status"] == "ACCEPTED" and len(ontology["attempts"]) == 1
    assert result["status"] == "ADMITTED_AND_REPLAYED"
    assert result["ledger_event_count"] == 14
    assert result["reopen_matches_admitted"] == {"export_records": True, "receipt": True}
    assert census["blocks_total"] == 186 and census["blocks_untouched"] == 0
    graph = result["graph"]
    assert result["records_traced"] == graph["entities"] + graph["events"] + graph["relations"]
    coverage = census["provenance_coverage"]
    assert coverage["total"] == coverage["with_digest"] == coverage["with_locator"]
    assert result["reading_sha256"].endswith(
        "f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17"
    )


def test_reviewer_model_named_in_prose_is_the_recorded_one():
    for run in V3_CELLS:
        log = json.loads((ROOT / f"private/paper-v4-v4-{run}/launch-log.json").read_bytes())
        assert log["review"]["model_id"] == "claude-opus-5"
        assert log["review"]["evaluator_kind"] == "CLAUDE_PRELIMINARY"
    assert "the same model family as the producers" in prose()


def test_runner_attempts_and_token_note_are_as_written():
    attempts = {run: len(launch_log(run)["runner"]) for run in CELLS + [CONTROL, V32_CELL]}
    assert attempts == {
        "run-20": 2, "run-21": 1, "run-22": 1, "run-23": 1,
        "run-24": 1, "run-25": 1, "run-26": 1,
    }
    launches = len(launch_log("run-22")["launches"])
    assert launches == 2, "run-22's token figure is described as covering two launches"
    assert "run-22's figure includes a launch that was set aside and relaunched" in prose()


def test_faithfulness_totals_match_the_reported_graph_cells():
    """The abstract and 4.5 count every graph cell the paper reports."""
    supports = Counter()
    for run in GRAPH_CELLS:
        supports.update(w["source_support"] for w in review(run)["witnesses"])
    total = sum(supports.values())
    assert supports["UNSUPPORTED"] == 0 and supports["NOT_EVALUABLE"] == 0
    body = prose()
    assert f"{total:,} distinct witnesses were judged" in body
    assert f"{supports['PARTIAL']} were PARTIAL" in body
    assert f"{total:,} returned facts" in body
    per_cell = {
        run: Counter(w["source_support"] for w in review(run)["witnesses"])
        for run in GRAPH_CELLS
    }
    clean = min(per_cell, key=lambda r: (per_cell[r]["PARTIAL"], r))
    assert clean == "run-22-v413" and per_cell[clean]["PARTIAL"] == 0
    assert f"none at all over {sum(per_cell[clean].values())}" in body
    second = per_cell[V32_CELL]
    assert f"run-26 two over {sum(second.values())}" in body and second["PARTIAL"] == 2
    urls = sum(ontology_result(run)["citation_check"]["urls"] for run in CELLS)
    fabricated = sum(ontology_result(run)["citation_check"]["fabricated"] for run in CELLS)
    assert fabricated == 0
    assert f"{urls} URLs in all" in body
    # The two readings of run-22's re-query are reported in 4.4 and bound by
    # test_rebind_paragraph_matches_both_retained_attempts, not here.


def question_file(contract_cell):
    """The question file a cell bound, read from its contract or, for a surface
    with no evaluation block, from the material its review manifest binds."""
    contract = json.loads((PAPER / f"experiment-v4/{contract_cell}/run-contract.json").read_bytes())
    evaluation = contract.get("evaluation")
    if evaluation:
        path = evaluation["competency_questions"]["path"]
    else:
        manifest = json.loads(
            (PAPER / f"evaluation-v4/{contract_cell}/review-input-manifest.json").read_bytes()
        )
        path = next(
            m["path"] for m in manifest["materials"] if m["name"] == "competency_questions"
        )
    return json.loads((ROOT / path).read_bytes())["questions"]


def controls_matched_record(record, contract_cell):
    labels = {q["question_id"]: q["question_responsiveness"] for q in record["questions"]}
    matched = 0
    for question in question_file(contract_cell):
        control = question.get("expected_outcome")
        if not control:
            continue
        if control["kind"] == "PARAPHRASE":
            matched += labels[question["id"]] == labels[control["of"]]
        else:
            matched += labels[question["id"]] == control["expected_coverage"]
    return matched


def controls_matched(directory, contract_cell):
    return controls_matched_record(review(directory), contract_cell)


def test_coverage_range_sentences_match_the_reported_cells():
    body = prose()
    reached = {d: absences(review(d))[0] for d in GRAPH_CELLS}
    assert f"reached {min(reached.values())} to {max(reached.values())}" in body
    assert "run-22, v4.12 binder | 82" in body
    original = absences(review("run-22"))[1]["UNREACHED_RECORD"]
    corrected = absences(review("run-22-v413"))[1]["UNREACHED_RECORD"]
    assert (original, corrected) == (11, 2)
    assert "from 82 to 90 of 102" in body


def test_modelling_variance_sentences_match_the_frozen_cells():
    body = prose()
    relations = ", ".join(str(run_result(run)["graph"]["relations"]) for run in CELLS)
    gaps = ", ".join(str(sum(run_result(run)["gaps_by_kind"].values())) for run in CELLS)
    relations = relations.replace(", 21", " and 21")
    gaps = gaps.replace(", 153", " and 153")
    assert f"proposed {relations} relations" in body
    assert f"declared {gaps}" in body
    assert run_result("run-24")["gaps_by_kind"]["TYPE_ABSENT"] == 137
    unlinked = sorted(
        Counter(q["assembly"] for q in review(run)["questions"])["UNLINKED_ROWS"]
        for run in COVERAGE_CELLS
    )
    assert unlinked == [20, 20, 21]
    assert "In 20 or 21 of the thirty questions" in body


def test_worked_examples_match_the_exhibit_cell_review():
    record = review(EXHIBIT_CELL)
    labels = {q["question_id"]: q for q in record["questions"]}
    assert labels["CQ-T1-02"]["question_responsiveness"] == "COVERED"
    assert labels["CQ-T1-02"]["assembly"] == "UNLINKED_ROWS"
    assert labels["CQ-T4-01"]["question_responsiveness"] == "COVERED"
    assert labels["CQ-T5-01"]["question_responsiveness"] == "PARTIAL"
    assert labels["CQ-T5-01"]["assembly"] == "UNLINKED_ROWS"
    assert labels["CQ-T1-03"]["question_responsiveness"] == "PARTIAL"
    assert labels["CQ-C-01"]["question_responsiveness"] == "NONE"
    partial = [w for w in record["witnesses"] if w["source_support"] == "PARTIAL"]
    assert len(partial) == 6
    assert any(w["witness_key"] == "claim:acknowledgement-discussions" for w in partial)
    assert "found six PARTIAL witnesses among 428" in prose()
    assert len(record["witnesses"]) == 428


def test_appendix_a_exhibits_are_exact_subsets_of_retained_outputs():
    appendix = text().split("## Appendix A.", 1)[1].split("## Appendix B.", 1)[0]
    exhibits = [json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", appendix, re.S)]
    assert len(exhibits) == 8
    record = review(EXHIBIT_CELL)
    result = json.loads((PRIVATE_EXHIBIT_CELL / "query/query-result.json").read_bytes())
    queries = {q["question_id"]: q for q in result["queries"]}
    pool = []
    for qid in ("CQ-T1-02", "CQ-T4-01", "CQ-T5-01", "CQ-T1-03"):
        pool.extend(queries[qid]["rows"])
    pool.extend(record["witnesses"])
    pool.extend(record["questions"])
    for q in record["questions"]:
        if q["question_id"] == "CQ-T5-01":
            pool.extend(q["coverage"])
    for exhibit in exhibits:
        assert any(is_exact_subset(exhibit, candidate) for candidate in pool), exhibit


def test_exhibit_locators_resolve_to_the_blocks_named_in_prose():
    capture = json.loads(
        (PRIVATE_EXHIBIT_CELL / "producer/work/document-population.json").read_bytes()
    )
    assertions = {a["id"]: a for a in capture["capture"]["assertions"]}
    expected = {
        "assertion:039": "page:2:block:002",
        "assertion:007": "page:1:block:001",
        "assertion:118": "page:5:block:005",
        "assertion:062": "page:2:block:006",
        "assertion:027": "page:1:block:006",
    }
    body = text()
    for locator, block in expected.items():
        assert assertions[locator]["block"] == block
        assert locator in body and block in body
    gaps = json.loads((PRIVATE_EXHIBIT_CELL / "results/gaps.json").read_bytes())["gaps"]
    assert any(g["kind"] == "TYPE_ABSENT" and g["locator"] == "assertion:027" for g in gaps)


def test_identity_paragraph_matches_every_cell():
    body = text()
    for run in CELLS:
        result = run_result(run)
        for key in ("ontology_sha256", "ledger_head", "replay_receipt_sha256"):
            assert result[key].removeprefix("sha256:") in body, (run, key)
    assert "7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9" in body


def test_draft_evidence_inputs_are_declared_for_the_isolated_gate():
    manifest = json.loads((PAPER / "active-test-manifest.json").read_bytes())
    assert "private/paper-v4-v4-run-*" in manifest["private_fixture_patterns"]
    assert "private/paper-v4-text-layer" in manifest["private_fixture_patterns"]


def test_working_draft_local_evidence_links_resolve():
    links = re.findall(r"\]\(([^)]+)\)", text())
    assert links
    for target in links:
        if "://" not in target and not target.startswith("#"):
            assert (DRAFT.parent / target.split("#", 1)[0]).is_file(), target


def test_control_paragraph_matches_run_25_and_run_23():
    body = prose()
    control, base = run_result(CONTROL), run_result("run-23")
    contract = json.loads((PAPER / f"experiment-v4/{CONTROL}/run-contract.json").read_bytes())
    assert contract["condition"] == "FIXED_ONTOLOGY_CONTROL"
    assert control["ontology_sha256"] == base["ontology_sha256"]
    total = lambda r: r["graph"]["entities"] + r["graph"]["events"] + r["graph"]["relations"]
    assert f"proposed {total(control)} records against run-23's {total(base)}" in body
    assert f"{control['graph']['relations']} relations against {base['graph']['relations']}" in body
    gaps = lambda r: sum(r["gaps_by_kind"].values())
    assert f"declared {gaps(control)} gaps against {gaps(base)}" in body
    assert control["census"]["blocks_asserted"] == 186
    record = review(CONTROL)
    support = Counter(w["source_support"] for w in record["witnesses"])
    assert f"{support['SUPPORTED']} of {sum(support.values())} witnesses" in body
    reached, causes = absences(record)
    base_reached, _ = absences(review("run-23"))
    assert f"reached {reached} of 102 against run-23's {base_reached}" in body
    assert controls_matched(CONTROL, CONTROL) == 5
    exported = json.loads(
        (ROOT / f"private/paper-v4-v4-{CONTROL}/results/export-records.json").read_bytes()
    )
    relations = exported["relations"] if isinstance(exported, dict) else exported
    kinds = {
        (r.get("properties") or {}).get("relation_type") or r.get("relation_type")
        for r in relations
        if "relation_type" in json.dumps(r)
    }
    assert not kinds & {"SUPPORTS", "CHALLENGES"}
    assert "Of its 57 relations, 27 are contribution credits, and none is SUPPORTS or CHALLENGES" in body


def test_evidence_relation_claim_covers_every_reported_graph():
    # A claim about all reported graphs cannot be supported by one control.
    sources = {cell: run for cell, _, run in REPORTED}
    counts = {}
    for cell in GRAPH_CELLS:
        run = sources[cell]
        raw = (ROOT / f"private/paper-v4-v4-{run}/results/export-records.json").read_bytes()
        assert "sha256:" + hashlib.sha256(raw).hexdigest() == run_result(run)["export_records_sha256"]
        relations = json.loads(raw)["relations"]
        counts[cell] = Counter(
            r["properties"]["relation_type"]
            for r in relations if r["type"] == "ResearchRelation"
        )
    assert set(counts) == set(GRAPH_CELLS)
    with_support = [cell for cell, kinds in counts.items() if kinds["SUPPORTS"]]
    assert with_support == [V32_CELL]
    assert not any(kinds["CHALLENGES"] for kinds in counts.values())
    body = prose()
    assert (
        f"Run-26 contains {counts[V32_CELL]['SUPPORTS']} SUPPORTS relations"
        in body
    )
    assert "none of the five graph results in the coverage comparison uses them" not in body
    assert "selective omission, not a complete failure to capture evidence links" in body


def test_existing_support_links_remain_distinct_from_missing_argument_links():
    exported = json.loads(
        (ROOT / f"private/paper-v4-v4-{V32_CELL}/results/export-records.json").read_bytes()
    )
    links = {
        r["id"]: r for r in exported["relations"]
        if r["type"] == "ResearchRelation" and r["properties"]["relation_type"] == "SUPPORTS"
    }
    assert {r["target_id"] for r in links.values()} == {
        "claim:deep-events-well-constrained", "claim:depths-not-artifact"
    }
    record = review(V32_CELL)
    witnesses = {w["witness_key"]: w for w in record["witnesses"]}
    for key in links:
        assert witnesses[key]["source_support"] == "SUPPORTED"
    questions = {q["question_id"]: q for q in record["questions"]}
    for key in ("CQ-T5-01", "CQ-T5-05"):
        edge = next(e for e in questions[key]["coverage"] if e["semantic"] == "evidence_relation")
        assert edge["row_index"] is None and edge["absent_reason"] == "NOT_CAPTURED"
    assert "depth-resolution tests to claims about the reliability of the reported depths" in prose()


def _clopper_pearson_upper(k, n, alpha=0.05):
    from math import comb
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if sum(comb(n, i) * mid**i * (1 - mid) ** (n - i) for i in range(k + 1)) > alpha:
            lo = mid
        else:
            hi = mid
    return hi


def _judge(short):
    text_ = (PAPER / f"evaluation-v4/sample/judge-record-20260912-{short}.md").read_text()
    return json.loads(re.findall(r"```json\s*(.*?)\s*```", text_, re.S)[-1])


def _recorded(sample_name):
    sample = json.loads((PAPER / f"evaluation-v4/sample/{sample_name}").read_bytes())
    return {(w["cell"], w["witness_key"]): w["recorded_source_support"] for w in sample["witnesses"]}


def test_independent_judge_paragraph_matches_the_judge_records():
    body = prose()
    supported = _judge("f573af6b")
    recorded = _recorded("sample-20260912-supported.json")
    assert supported["judge"]["model_id"] == "claude-fable-5-1"
    assert supported["judge"]["evaluator_kind"] == "INDEPENDENT_MODEL_JUDGE"
    labels = Counter(j["source_support"] for j in supported["judgements"])
    assert len(supported["judgements"]) == 200 and set(recorded.values()) == {"SUPPORTED"}
    assert labels == {"SUPPORTED": 196, "PARTIAL": 4}
    per_cell = Counter(j["cell"] for j in supported["judgements"] if j["source_support"] == "PARTIAL")
    assert set(per_cell.values()) == {1}
    assert "agreed on 196 and moved four to PARTIAL, one per cell" in body
    assert f"{round(_clopper_pearson_upper(4, 200) * 100, 1)} percent" in body
    assert f"{round(_clopper_pearson_upper(0, 200) * 100, 1)} percent" in body
    partial = _judge("ce1e451c")
    recorded_p = _recorded("sample-20260912-partial-all.json")
    assert len(partial["judgements"]) == 22 and set(recorded_p.values()) == {"PARTIAL"}
    labels_p = Counter(j["source_support"] for j in partial["judgements"])
    assert labels_p == {"PARTIAL": 18, "SUPPORTED": 4}
    assert "agreed on 18 and moved four to SUPPORTED" in body
    assert "agreed on 196, moving four to partial and none to unsupported" in body


def test_recoding_split_matches_the_derived_file():
    derived = json.loads((PAPER / "evaluation-v4/absence-recoding-2026-09-12.json").read_bytes())
    entries = derived["entries"]
    assert {e["cell"] for e in entries} == {"run-22", "run-23", "run-24", "run-25"}
    cases = Counter(e["derived_case"] for e in entries)
    recorded = Counter(e["recorded_reason"] for e in entries)
    body = prose()
    assert recorded["NOT_MODELLED"] == 25 and f"the {recorded['NOT_MODELLED']} such absences" in body
    assert f"{cases['NO_TYPE_OR_SLOT']} where the accepted contract declares no type or slot" in body
    assert f"{cases['SLOT_WITHOUT_ENTITY']} where the slot exists and the graph holds no entity" in body
    assert f"{cases['SLOT_ENTITY_NAME_MISMATCH']} where the slot and the entity both exist" in body
    assert f"and {cases['UNDECIDED']} that the four cases" in body
    assert cases["HELD_AS_DIGEST"] == recorded["WITHHELD_STATEMENT"] == 16
    assert "All 16 WITHHELD_STATEMENT absences" in body
    for e in entries:
        assert e["evidence"] or e["derived_case"] == "UNDECIDED", e


def test_baseline_section_matches_its_validated_record():
    record = review(BASELINE)
    assert record["schema"].endswith("/v3.2")
    body = prose()
    support = Counter(w["source_support"] for w in record["witnesses"])
    assert support["UNSUPPORTED"] == 0 and support["NOT_EVALUABLE"] == 0
    answers = json.loads(
        (ROOT / f"private/paper-v4-{BASELINE}/producer/work/answers.json").read_bytes()
    )
    claims = sum(len(a["claims"]) for a in answers["answers"])
    declared = sum(1 for a in answers["answers"] if a["no_answer_in_source"])
    assert claims == len(record["witnesses"]) == 135 and len(answers["answers"]) == 30
    assert f"{claims} cited claims over {len(answers['answers'])} answers" in body
    assert declared == 3 and "three of them declaring" in body
    labels = Counter(q["question_responsiveness"] for q in positive(record["questions"]))
    reached, causes = absences(record)
    assert (reached, dict(causes)) == (101, {"NOT_CAPTURED": 1})
    assert labels["COVERED"] == 24
    assert {q["assembly"] for q in record["questions"]} == {"NOT_APPLICABLE"}
    assert controls_matched(BASELINE, BASELINE) == 5
    graph_reached = sorted(absences(review(c))[0] for c in GRAPH_CELLS)
    assert f"| elements reached of 102 | {graph_reached[0]} to {graph_reached[-1]} | {reached} |" in body
    graph_covered = sorted(
        Counter(q["question_responsiveness"] for q in positive(review(c)["questions"]))["COVERED"]
        for c in GRAPH_CELLS
    )
    assert (
        f"| positive questions covered of 25 | {graph_covered[0]} to {graph_covered[-1]} | "
        f"{labels['COVERED']} |" in body
    )
    log = json.loads((ROOT / f"private/paper-v4-{BASELINE}/launch-log.json").read_bytes())
    tokens = log["launches"][0]["usage"]["producer_total_tokens"]
    cells = [
        json.loads((PAPER / f"experiment-v4/{run}/results/usage.json").read_bytes())[
            "producer_total_tokens"
        ]
        for run in CELLS + [CONTROL]
    ]
    assert f"| producer tokens | {min(cells):,} to {max(cells):,} | {tokens:,} |" in body
    assert min(cells) / tokens >= 3 and max(cells) / tokens <= 4.5
    assert "roughly three to four times the reported session tokens" in body
    assert "not an isolated cost of admission" in body


def test_baseline_is_not_claimed_to_replay_or_refuse():
    body = prose()
    for phrase in (
        "prose and citations, not an admitted history",
        "with replay, supersession or typed capture gaps",
        "not impossibilities for systems built around prose",
    ):
        assert phrase in body, phrase
    contract = json.loads(
        (PAPER / f"experiment-v4/{BASELINE}/run-contract.json").read_bytes()
    )
    assert contract["condition"] == "IN_CONTEXT_BASELINE"
    assert contract["questions_are_visible_to_this_producer"] is True
    assert "the thirty questions visible" in body


TIERS = [
    ("T1", "direct facts", 16),
    ("T2", "relationships", 20),
    ("T3", "quantities", 23),
    ("T4", "qualifications", 20),
    ("T5", "composition", 23),
]


def _reached_by_tier(record):
    reached = Counter()
    total = Counter()
    for q in positive(record["questions"]):
        tier = q["question_id"].split("-")[1][:2]
        for c in q["coverage"]:
            total[tier] += 1
            if c["row_index"] is not None:
                reached[tier] += 1
    return reached, total


def test_tier_table_matches_every_reported_record():
    body = prose()
    graph = {run: _reached_by_tier(review(run)) for run in GRAPH_CELLS}
    base_reached, base_total = _reached_by_tier(review(BASELINE))
    for tier, name, elements in TIERS:
        for reached, total in graph.values():
            assert total[tier] == elements, (tier, total[tier])
        assert base_total[tier] == elements
        values = sorted(reached[tier] for reached, _ in graph.values())
        span = (
            f"{values[0]} of {elements}"
            if values[0] == values[-1]
            else f"{values[0]} to {values[-1]} of {elements}"
        )
        if values[0] == values[-1]:
            span = f"{values[0]} of {elements} in every cell"
        row = f"| {name} | {span} | {base_reached[tier]} of {elements} |"
        assert row in body, row
    # the two sentences the table is there to support
    assert graph["run-23"][0]["T5"] == graph[CONTROL][0]["T5"] == 20
    quantities = [reached["T3"] for reached, _ in graph.values()]
    assert quantities.count(23) == 2 and base_reached["T3"] == 23
    assert "two of the five graph cells reach" in body
    facts = max(reached["T1"] for reached, _ in graph.values())
    assert facts == 16 > base_reached["T1"] == 15
    assert "the best of them reaches one more than the" in body


def test_different_witness_units_do_not_establish_comparative_precision():
    body = prose()
    for unsupported in ("Precision runs the other way", "three and a half times the rate",
                        "correct unverifiably", "does not drift that way", "the gate costs coverage"):
        assert unsupported not in body
    assert "does not establish a precision advantage" in body
    assert "typed field can still attach a correct value to the wrong subject" in body


def test_every_current_cell_is_counted_in_the_condition_and_abstract():
    body = prose()
    assert len(CELLS + [V32_CELL]) == 6
    assert len(ADMISSION) == 7
    assert "six fresh" in body and "all seven populations" in body
    assert "five fresh" not in body.split("## 1.", 1)[0]
    assert "A sixth cell, run-25" not in body
    assert "the later three" not in body
    assert "Run-23 is the cell with the highest coverage" not in body
    assert "illustrative cell" in body


def test_reuse_is_reported_with_quality_cost_and_control_caveats():
    body = prose()
    reuse = review("reuse-01")
    reached = sum(c["row_index"] is not None for q in reuse["questions"]
                  if not q["question_id"].startswith("CQ-B-C") for c in q["coverage"])
    assert reached == 88
    assert "88 of 102" in body and "459,121" in body and "327,772" in body
    assert "manual query bindings" in body
    assert "excluded from comparative conclusions" in body
    assert "No break-even point was measured" in body
    assert "not a measured cross-session learning benefit" in body


def test_the_sixth_absence_code_is_exercised_only_where_it_exists():
    """v3.2's first graph cell records NOT_CAPTURED and no NOT_MODELLED."""
    record = review(V32_CELL)
    assert record["schema"].endswith("/v3.2")
    _, causes = absences(record)
    assert causes["NOT_CAPTURED"] == 5 and causes["NOT_MODELLED"] == 0
    contract = json.loads(
        (PAPER / f"experiment-v4/{V32_CELL}/run-contract.json").read_bytes()
    )
    assert "v3.2" in json.dumps(contract["evaluation"])
    for cell in COVERAGE_CELLS + [CONTROL]:
        older = review(cell)
        assert older["schema"].endswith("/v3")
        assert absences(older)[1]["NOT_CAPTURED"] == 0
    body = prose()
    assert "records NOT_MODELLED nowhere and" in body
    assert f"NOT_CAPTURED {causes['NOT_CAPTURED']} times" in body.replace("five times", "5 times")


def test_the_relation_count_does_not_buy_composition():
    body = prose()
    relations = {run: run_result(run)["graph"]["relations"] for run in CELLS + [CONTROL, V32_CELL]}
    assert relations[V32_CELL] == 152
    assert relations[V32_CELL] > 7 * relations["run-24"] - 1
    assert relations[V32_CELL] > 2.5 * relations[CONTROL]
    assert f"proposed {relations[V32_CELL]} relations, seven times run-24's {relations['run-24']}" in body
    composition = {run: _reached_by_tier(review(run))[0]["T5"] for run in GRAPH_CELLS}
    assert set(composition.values()) == {20}, composition
    assert "lost the same three composition elements as" in body


FAULTS = PAPER / "experiment-v4/fault-injection-01"
# The prose label the manuscript prints for each mechanism outcomes.json names.
CATCHERS = {
    "NONE_REVIEW_ONLY": "none, review only",
    "DIGEST_BINDING": "digest binding",
    "TRACE_DERIVATION": "trace derivation",
    "ADMISSION_STRUCTURAL_CHECK": "admission structural check",
    "COMPILER": "compiler",
}


def fault_outcomes():
    return json.loads((FAULTS / "outcomes.json").read_bytes())


def fault_subsection():
    return text().split("### 4.6 Injected faults", 1)[1].split("### 4.7", 1)[0]


def fault_trials(predicate):
    return [trial for trial in fault_outcomes()["trials"] if predicate(trial)]


def test_fault_table_rows_match_every_trial_of_their_class():
    outcomes = fault_outcomes()
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in fault_subsection().splitlines()
        if line.startswith("|")
    ]
    assert rows[0] == [
        "Injected fault",
        "Designed catcher",
        "Trials",
        "Observed outcome",
    ]
    assert all(len(row) == 4 for row in rows)
    printed = {row[0]: row for row in rows[2:]}
    assert len(printed) == len(rows[2:]) == 11
    assert set(printed) == {trial["fault_class"] for trial in outcomes["trials"]}
    for fault_class, row in printed.items():
        own = fault_trials(lambda t, c=fault_class: t["fault_class"] == c)
        assert len(own) == outcomes["instances_per_variant"]
        assert row[2] == str(len(own))
        assert {CATCHERS[trial["designed_catcher"]] for trial in own} == {row[1]}
        outcome = {trial["outcome"] for trial in own}
        reasons = {trial["diagnostic"]["reason"] for trial in own}
        assert len(outcome) == 1 and len(reasons) == 1, fault_class
        observed, reason = outcome.pop(), reasons.pop()
        expected = {
            "REFUSED": f"Refused, {reason}",
            "ADMITTED_EXPOSED": "Admitted, exposed by the trace",
            "ADMITTED_INVISIBLE": "Admitted, invisible",
        }[observed]
        assert row[3] == expected, fault_class
        assert bool(reason) is (observed == "REFUSED"), fault_class


def test_fault_paragraph_matches_the_outcomes_file():
    outcomes = fault_outcomes()
    trials = outcomes["trials"]
    refused = fault_trials(lambda t: t["outcome"] == "REFUSED")
    admitted = fault_trials(lambda t: t["outcome"].startswith("ADMITTED"))
    exposed = fault_trials(lambda t: t["outcome"] == "ADMITTED_EXPOSED")
    invisible = fault_trials(lambda t: t["outcome"] == "ADMITTED_INVISIBLE")
    prefix = [t for t in refused if t["ledger"]["opens_the_control_ledger"]]
    mutated = [t for t in refused if not t["ledger"]["opens_the_control_ledger"]]
    body = " ".join(fault_subsection().split())
    assert (len(trials), len(refused), len(admitted)) == (55, 35, 20)
    assert (len(prefix), len(mutated), len(exposed), len(invisible)) == (30, 5, 5, 15)
    assert outcomes["base_run"] == "run-23"
    assert {t["fault_class"] for t in mutated} == {"SLOT_OUTSIDE_ONTOLOGY"}
    assert all(trial["diagnostic"]["reason"] for trial in refused)
    assert all(trial["predicted_outcome"] == trial["outcome"] for trial in trials)
    assert f"{len(trials)} typed faults were injected into run-23's" in body
    assert f"Of the {len(trials)}, {len(refused)} were refused at admission" in body
    assert (
        f"In {len(prefix)} of those the refused ledger is a byte-exact prefix" in body
    )
    assert (
        f"the other {len(mutated)} differ only in the event that retains the evidence"
        in body
    )
    assert "Twenty were admitted" in body
    assert "Five of the twenty are exposed" in body
    assert f"{len(invisible)} are invisible to every check a reader can run" in body
    classes = {trial["fault_class"] for trial in invisible}
    assert len(classes) == 3
    for fault_class in classes:
        assert fault_class in body, fault_class
    assert outcomes["core_commit"].startswith("c95dba7")
    assert "recorded before any trial ran" in body


def test_the_fault_subsection_states_the_limits_of_the_measurement():
    body = " ".join(fault_subsection().split())
    assert "This is a property of the structural gate alone" in body
    assert "It faults run-23 and no other cell" in body
    assert "no query and no review was run over any faulted graph" in body
    assert "without Core's rule layer or any logic check" in body
    assert "the seven classes are ours" in body


def test_the_digest_binding_reach_sentence_matches_run_23s_census():
    census = json.loads(
        (PAPER / "experiment-v4/run-23/results/census.json").read_bytes()
    )
    coverage = census["provenance_coverage"]
    traced = run_result("run-23")["records_traced"]
    body = " ".join(fault_subsection().split())
    assert coverage["with_locator"] == coverage["with_digest"] == coverage["total"]
    assert len(coverage["by_type"]) == 5
    assert "declared on five record types" in body
    assert f"covers {coverage['total']} of run-23's {traced} records" in body


def test_the_abstract_reports_the_fault_injection():
    trials = fault_outcomes()["trials"]
    refused = fault_trials(lambda t: t["outcome"] == "REFUSED")
    exposed = fault_trials(lambda t: t["outcome"] == "ADMITTED_EXPOSED")
    invisible = fault_trials(lambda t: t["outcome"] == "ADMITTED_INVISIBLE")
    abstract = " ".join(text().split("## Abstract", 1)[1].split("## 1.", 1)[0].split())
    assert (
        f"A fault-injection control put {len(trials)} typed faults into one of those "
        f"admitted populations: {len(refused)} were refused at admission with a typed "
        f"diagnostic and {len(exposed) + len(invisible)} admitted, {len(exposed)} of "
        f"them exposed afterwards by their own trace and {len(invisible)} invisible "
        "without reading the source."
    ) in abstract


def test_the_closing_paragraph_keeps_its_claim_and_adds_the_measurement():
    trials = fault_outcomes()["trials"]
    refused = fault_trials(lambda t: t["outcome"] == "REFUSED")
    admitted = fault_trials(lambda t: t["outcome"].startswith("ADMITTED"))
    invisible = fault_trials(lambda t: t["outcome"] == "ADMITTED_INVISIBLE")
    closing = " ".join(
        text()
        .split("What the evidence supports is narrow", 1)[1]
        .split("## Appendix A.", 1)[0]
        .split()
    )
    assert "The gate guards form and lineage." in closing
    assert "Content remains the producer's" in closing
    assert (
        f"{len(trials)} typed faults into one admitted population measures where "
        f"that boundary falls: {len(refused)} were refused with a typed diagnostic "
        f"and {len(admitted)} admitted, {len(invisible)} of them invisible to any "
        "check that does not read the source"
    ) in closing
    assert "Core's rule layer" in closing
    assert "was not applied to these faults" in closing


def test_the_shop_and_fault_calibrations_are_in_the_active_gate():
    manifest = json.loads((PAPER / "active-test-manifest.json").read_bytes())
    assert "paper-v4/test_shop_connected_calibration.py" in manifest["paths"]
    assert (
        "paper-v4/experiment-v4/fault-injection-01/test_faults.py" in manifest["paths"]
    )
    assert "paper-v4/test_shop_calibration.py" in manifest["paths"]


RATIFICATION = PAPER / "evaluation-v4/author-ratification-2026-09-16.md"
RATIFIED_CELLS = ["run-22-v413", "run-23", "run-24", "run-25", "run-26"]


def test_author_ratification_of_the_five_graph_reviews_is_recorded():
    """Luis, 2026-09-16: "I read all five records in full." The manuscript may
    say the five later graph-result reviews are ratified only while a record
    names each reviewed file by its digest and those digests still match."""
    record = RATIFICATION.read_text()
    for cell in RATIFIED_CELLS:
        path = PAPER / f"evaluation-v4/{cell}/review-record.preliminary.md"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest in record, f"{cell} review record digest not in the ratification"
    body = prose()
    assert "the author read the five later graph-result reviews in full and ratified them" in body
    assert "baseline and reuse" in body and "not ratified" in body
    assert "remain unratified" not in body
