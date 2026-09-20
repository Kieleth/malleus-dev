"""reuse-01's frozen figures, checked against the files they came from.

Every number in this file was written by a script that ran, never typed from a
report: the question set by ``freeze_questions.py``, the binding by run-23's
``bind_from_surface.py``, the rows and witnesses by run-23's ``native_query.py``,
the public set and the ladder by ``freeze.py``, and the manifest by
``paper-v4/evaluation-v4/reuse-01/build_review_inputs.py``. The tests read the
public artefacts and the selected reading, which is the one private input the
active-test manifest already declares, so the gate needs no new private fixture.

What they are for. reuse-01's one claim about run-23 is that it did not touch
it: the same ledger, the same head, the same replay receipt, the same ontology,
the same population trace. Five of these tests are that claim, expressed as
digests that a later edit to run-23 would break.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULTS = HERE / "results"
PACKAGE = ROOT / "paper-v4/evaluation-v4/reuse-01"
RUN_23 = ROOT / "paper-v4/experiment-v4/run-23"
QUESTIONS = ROOT / "paper-v4/experiment-v4/competency-questions-set-b.json"
READING = ROOT / "private/paper-v4-text-layer/selected-reading.json"
PROTOCOL = ROOT / "paper-v4/evaluation-v4/review-protocol-v3.2.json"

CORE_PIN = "c95dba7b86bb61487bda9a52458e1ea47cce20ab"
LEDGER_SHA256 = "sha256:d5ef64c0ca6558967aa664705aa9661d3aec399d73c94aa7a5286ea6a991a908"
LEDGER_HEAD = "sha256:9fb776938683d0c5b04666dda13a0711cdd2a78ea99593a2264705a2d825f5ab"
REPLAY_RECEIPT = "sha256:a3abceec58dc93692cbdeabf9a95c03551177ba97d9ee4225fe29198f37f1eec"
ONTOLOGY_SHA256 = "sha256:9aa5fdcfb74dc9cad9b36b16b27e8a829b5a71ad1b2bc61892e12a2568b06d21"
QUESTIONS_SHA256 = (
    "sha256:1d2d1c0f589432ab24b6d4ba6817c0bab3abbce5172364e394bed5a307e10bcf"
)
BINDING_SHA256 = (
    "sha256:d80a95518eee22b39f59e69b5f414b8127011e23cd7d7a7b4bfd7f622630c83b"
)
CASES_SHA256 = (
    "sha256:b57a84386fa7a86d7fa154680fb7e8f35db28874b77d41a53d28c28460f97eb0"
)
CASES = 11912
CASES_BY_KIND = {
    "ENTITY": 104,
    "ENTITY_NO_SUBJECT": 125,
    "RELATION": 7596,
    "SUBJECT": 962,
    "SUBJECT_ANY": 3125,
}
ROWS_TOTAL = 7433
DISTINCT_WITNESSES = 429
RECORDS_TRACED = 429
POSITIVE_QUESTIONS = 25
ELEMENTS_OVER_POSITIVES = 102
ELEMENTS_OVER_ALL = 121
LEAK_WINDOW = 60


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_bytes())


def _module(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


# These private fixtures are declared in the active manifest. Missing bytes
# must fail rather than silently remove an evidence check from the gate.
def _need(path: Path):
    if not path.is_file():
        raise FileNotFoundError(f"declared private fixture is absent: {path}")
    return path.read_bytes()


# ---------------------------------------------------------------------------
# The second question set
# ---------------------------------------------------------------------------


def test_the_question_set_is_frozen_independent_and_shaped_as_declared() -> None:
    document = load(QUESTIONS)
    assert document["schema"] == "malleus.paper-v4.competency-questions/v3"
    assert document["status"] == "FROZEN"
    assert document["set"] == "B"
    assert digest(QUESTIONS) == QUESTIONS_SHA256
    questions = document["questions"]
    assert len(questions) == 30
    ids = [item["id"] for item in questions]
    assert len(set(ids)) == 30
    assert all(item.startswith("CQ-B-") for item in ids)
    positives = [item for item in questions if item["tier"] != "C"]
    assert len(positives) == POSITIVE_QUESTIONS
    assert sorted({item["tier"] for item in positives}) == ["T1", "T2", "T3", "T4", "T5"]
    for tier in ("T1", "T2", "T3", "T4", "T5"):
        assert len([item for item in positives if item["tier"] == tier]) == 5
    assert sum(len(item["required_semantics"]) for item in positives) == (
        ELEMENTS_OVER_POSITIVES
    )
    assert sum(len(item["required_semantics"]) for item in questions) == (
        ELEMENTS_OVER_ALL
    )
    assert document["shape"]["required_elements_over_positive_questions"] == (
        ELEMENTS_OVER_POSITIVES
    )
    # Neither set supersedes the other; set A is bound by digest as a separate file.
    assert document["independent_of"]["relation"] == "NEITHER_A_REVISION_NOR_A_SUPERSESSION"
    assert document["independent_of"]["sha256"] == digest(
        ROOT / "paper-v4/experiment-v4/competency-questions-v3.1.json"
    )


def test_no_positive_question_declares_an_expected_outcome_and_every_control_does() -> None:
    questions = load(QUESTIONS)["questions"]
    controls = {}
    for item in questions:
        if item["tier"] == "C":
            outcome = item["expected_outcome"]
            controls[item["id"]] = outcome["kind"]
            if outcome["kind"] == "PARAPHRASE":
                named = next(q for q in questions if q["id"] == outcome["of"])
                assert named["tier"] != "C"
                assert named["required_semantics"] == item["required_semantics"]
            else:
                assert outcome["expected_coverage"] == "NONE"
        else:
            assert "expected_outcome" not in item
    assert len(controls) == 5
    assert sorted(set(controls.values())) == [
        "EXCLUDED_SURFACE",
        "NOT_IN_SOURCE",
        "PARAPHRASE",
    ]


def test_the_public_question_file_reproduces_no_passage_of_the_reading() -> None:
    ladder = _module(HERE / "leak_ladder.py", "reuse_01_ladder_questions")
    measured = ladder.measure([QUESTIONS], READING)
    assert measured[str(QUESTIONS)] == 0


# ---------------------------------------------------------------------------
# The type sets and the binding
# ---------------------------------------------------------------------------


def test_the_type_sets_name_this_cells_questions_and_close_under_the_subtypes() -> None:
    type_sets = load(RESULTS / "query-type-sets.json")
    ids = [item["id"] for item in load(QUESTIONS)["questions"]]
    assert sorted(type_sets) == sorted(ids)
    closure = _module(
        ROOT / "paper-v4/experiment-v4/type_set_closure.py", "reuse_01_closure"
    )
    omissions = closure.omissions(
        load(RUN_23 / "ontology-run/population-surface.json"),
        load(RUN_23 / "ontology-run/validated-contract.json"),
        type_sets,
    )
    assert omissions == {}
    # Entity is the ancestor of twenty-four surface types; listing it would drag
    # every one of them into a question's set.
    assert not any("Entity" in names for names in type_sets.values())


def test_each_paraphrase_control_carries_its_named_questions_type_set() -> None:
    type_sets = load(RESULTS / "query-type-sets.json")
    for item in load(QUESTIONS)["questions"]:
        outcome = item.get("expected_outcome")
        if outcome and outcome["kind"] == "PARAPHRASE":
            assert sorted(type_sets[item["id"]]) == sorted(type_sets[outcome["of"]])


def test_the_binding_is_run_23s_binder_over_run_23s_surface() -> None:
    binding = load(RESULTS / "native-query-binding.json")
    assert binding["schema"] == "malleus.paper-v4.native-query-binding/v6"
    assert digest(RESULTS / "native-query-binding.json") == BINDING_SHA256
    assert binding["cases_sha256"] == CASES_SHA256
    assert binding["population_surface_sha256"] == digest(
        RUN_23 / "ontology-run/population-surface.json"
    )
    assert binding["bound_after_replay_receipt_sha256"] == REPLAY_RECEIPT
    kinds: dict[str, int] = {}
    for query in binding["queries"]:
        for case in query["cases"]:
            kinds[case["kind"]] = kinds.get(case["kind"], 0) + 1
    assert kinds == CASES_BY_KIND
    assert sum(kinds.values()) == CASES
    assert len(binding["queries"]) == 30


# ---------------------------------------------------------------------------
# What this cell claims about run-23
# ---------------------------------------------------------------------------


def test_the_graph_reference_says_the_ledger_did_not_move() -> None:
    reference = load(RESULTS / "graph-reference.json")
    assert reference["status"] == "QUERIED_RUN_23_WITHOUT_MOVING_IT"
    graph = reference["graph"]
    assert graph["authored_by"] == "run-23"
    assert graph["ledger_sha256_before_query"] == LEDGER_SHA256
    assert graph["ledger_sha256_after_query"] == LEDGER_SHA256
    assert graph["ledger_unchanged"] is True
    assert graph["ledger_head"] == LEDGER_HEAD
    assert graph["replay_receipt_sha256"] == REPLAY_RECEIPT
    assert graph["accepted_ontology_sha256"] == ONTOLOGY_SHA256


def test_run_23s_own_run_record_still_carries_the_identities_this_cell_bound() -> None:
    run_result = load(RUN_23 / "results/run-result.json")
    assert run_result["run_id"] == "run-23"
    assert run_result["ledger_head"] == LEDGER_HEAD
    assert run_result["replay_receipt_sha256"] == REPLAY_RECEIPT
    assert run_result["ontology_sha256"] == ONTOLOGY_SHA256
    assert run_result["trace_summary_sha256"] == digest(
        RUN_23 / "results/trace-summary.json"
    )


def test_the_query_ran_against_the_pinned_core_and_reached_no_source() -> None:
    reference = load(RESULTS / "graph-reference.json")
    assert reference["query"]["core_pin"] == CORE_PIN
    assert reference["query"]["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert reference["query"]["rows_total"] == ROWS_TOTAL
    assert reference["query"]["distinct_witnesses"] == DISTINCT_WITNESSES
    assert reference["query"]["records_traced"] == RECORDS_TRACED


def test_the_pinned_core_commit_is_in_this_repositorys_history() -> None:
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", CORE_PIN, "src/malleus"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    assert listing
    assert "src/malleus/compiler.py" in listing


# ---------------------------------------------------------------------------
# The public set and the review package
# ---------------------------------------------------------------------------


def test_no_public_file_of_this_cell_reproduces_the_reading() -> None:
    withheld = load(RESULTS / "withheld-artifacts.json")
    assert withheld["check"]["frozen_threshold"] == (
        "NO_PUBLIC_FILE_SHARES_A_60_CHARACTER_RUN"
    )
    measured = withheld["check"]["public_files_measured"]
    assert measured
    assert max(measured.values()) < LEAK_WINDOW
    ladder = _module(HERE / "leak_ladder.py", "reuse_01_ladder_public")
    public = sorted(
        path
        for path in RESULTS.iterdir()
        if path.is_file() and path.suffix != ".pyc"
    )
    remeasured = ladder.measure(public, READING)
    assert max(remeasured.values()) < LEAK_WINDOW
    assert [item["name"] for item in withheld["withheld"]] == ["query-result.json"]


def test_the_review_manifest_validates_under_v3_2_and_binds_run_23s_stage() -> None:
    sys.path.insert(0, str(ROOT / "paper-v4/evaluation-v4"))
    import review  # noqa: PLC0415

    manifest_source = (PACKAGE / "review-input-manifest.json").read_bytes()
    manifest = review.validate_review_input_manifest(
        manifest_source, PROTOCOL.read_bytes()
    )
    assert manifest["run_id"] == "reuse-01"
    assert manifest["schema"] == "malleus.paper-v4.source-grounded-review-inputs/v3.2"
    assert manifest["evidence_surface"] == {
        "kind": "SELECTED_READING_TEXT_LAYER",
        "locator_kind": "SELECTED_READING_BLOCK_ID",
    }
    stage = manifest["stage_identities"]
    assert stage["ledger_head"] == LEDGER_HEAD
    assert stage["replay_receipt_sha256"] == REPLAY_RECEIPT
    assert stage["accepted_ontology_sha256"] == ONTOLOGY_SHA256
    assert stage["query_binding_sha256"] == BINDING_SHA256
    assert manifest["fixed_identities"]["competency_questions_sha256"] == QUESTIONS_SHA256
    assert sum(manifest["rows_per_question"].values()) == ROWS_TOTAL
    assert manifest["witnesses_traced"] == DISTINCT_WITNESSES
    by_name = {item["name"]: item for item in manifest["materials"]}
    assert by_name["population_trace"]["path"] == (
        "paper-v4/experiment-v4/run-23/results/trace-summary.json"
    )
    assert by_name["retained_capture"]["path"] == (
        "private/paper-v4-v4-run-23/ledger/retained-capture.json"
    )


def test_the_review_task_carries_the_checklist_the_codes_and_the_subject_tie_rule() -> None:
    task = (PACKAGE / "review-task.md").read_text(encoding="utf-8")
    protocol = load(PROTOCOL)
    for name in protocol["judgments"]["coverage_absent_reasons"]:
        assert f"`{name}`" in task
        assert protocol["judgments"]["coverage_absent_reason_definitions"][name][:40] in task
    checks = [
        item
        for item in protocol["checklist"]["checks"]
        if "SELECTED_READING_TEXT_LAYER" in item["applies_to"]
    ]
    assert checks
    for item in checks:
        assert f"(`{item['id']}`)" in task
    clarification = ROOT / "paper-v4/evaluation-v4/review-task-v3-clarification-2026-09-12.md"
    assert digest(clarification) in task
    assert "## The subject-tie rule" in task
    assert "{{" not in task


def test_the_review_package_carries_one_block_per_question_with_its_rows() -> None:
    manifest = load(PACKAGE / "review-input-manifest.json")
    for question_id, rows in manifest["rows_per_question"].items():
        block = load(PACKAGE / f"review-block.{question_id}.json")
        assert block["question_id"] == question_id
        assert len(block["rows"]) == rows
        assert [item["row_index"] for item in block["rows"]] == list(range(rows))
        assert len(block["coverage"]) == len(block["required_semantics"])
        assert "expected_outcome" not in block


# ---------------------------------------------------------------------------
# The review, and the read that quotes it
# ---------------------------------------------------------------------------

REVIEW_RECORD_SHA256 = (
    "sha256:13558349e320e267c9e4881fcbabd037dce3776dba11f4b44f1f81dfdcdd6adf"
)
WITNESSES_JUDGED = 429
SUPPORT = {"SUPPORTED": 421, "PARTIAL": 8}
POSITIVE_LABELS = {"COVERED": 15, "PARTIAL": 10}
ELEMENTS_REACHED_POSITIVE = 88
CONTROLS_MATCHED = 2


def _read():
    module = _module(HERE / "read_results.py", "reuse_01_read")
    return module.read_cell(PACKAGE, QUESTIONS)


def test_the_review_record_validates_under_v3_2_and_is_the_bytes_the_read_quotes() -> None:
    sys.path.insert(0, str(ROOT / "paper-v4/evaluation-v4"))
    import review  # noqa: PLC0415

    record_path = PACKAGE / "review-record.preliminary.md"
    assert digest(record_path) == REVIEW_RECORD_SHA256
    findings: list = []
    root = review.validate_review(
        record_path.read_bytes(),
        PROTOCOL.read_bytes(),
        review_input_manifest_source=(PACKAGE / "review-input-manifest.json").read_bytes(),
        query_result_source=_need(
            ROOT / "private/paper-v4-reuse-01/query/query-result.json"
        ),
        selected_reading_source=_need(READING),
        competency_questions_source=QUESTIONS.read_bytes(),
        findings=findings,
    )
    assert root["status"] == "PRELIMINARY_COMPLETE"
    assert root["schema"] == "malleus.paper-v4.source-grounded-review/v3.2"
    assert root["preliminary"]["evaluator_kind"] == "CLAUDE_PRELIMINARY"
    assert root["ratification"]["disposition"] == "PENDING"
    assert len(root["witnesses"]) == WITNESSES_JUDGED
    assert sum(1 for item in findings if item["matched"]) == CONTROLS_MATCHED
    assert len(findings) == 5


def test_the_read_reproduces_the_records_own_counts() -> None:
    cell = _read()
    assert cell["witnesses_judged"] == WITNESSES_JUDGED
    assert cell["source_support"] == SUPPORT
    assert cell["question_responsiveness_positive"] == POSITIVE_LABELS
    assert cell["elements_reached_positive"] == ELEMENTS_REACHED_POSITIVE
    assert cell["elements_total_positive"] == ELEMENTS_OVER_POSITIVES
    assert cell["rows_total"] == ROWS_TOTAL
    assert cell["controls_matched"] == CONTROLS_MATCHED
    assert sum(
        bucket["reached"]
        for tier, bucket in cell["elements_by_tier"].items()
        if tier != "C"
    ) == ELEMENTS_REACHED_POSITIVE


def test_no_witness_is_unsupported_and_every_row_is_judged_once() -> None:
    cell = _read()
    assert cell["source_support"].get("UNSUPPORTED", 0) == 0
    assert cell["source_support"].get("NOT_EVALUABLE", 0) == 0
    assert sum(cell["source_support"].values()) == WITNESSES_JUDGED
