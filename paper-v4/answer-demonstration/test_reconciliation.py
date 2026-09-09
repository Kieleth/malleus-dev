"""Bound source reconciliation, not automated semantic evaluation."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest
import pilot

from review_packet import canonical, digest


def example():
    from test_integration import example as previous

    base, candidate, _, reading = previous()
    reading["source_sha256"] = "sha256:" + "1" * 64
    candidate["capture"] = {
        "schema": "malleus.document-capture/private-v0",
        "reading_sha256": digest(canonical(reading)),
        "attribution": {"source_id": "source:one", "author": "Author", "date": "2025"},
        "assertions": [
            {
                "id": "a1",
                "block": "b1",
                "statement": "Synthetic scope qualifier",
                "formalized_by": [],
                "gaps": [],
                "modality": "STATED",
            }
        ],
        "nothing_assertable": [],
    }
    evidence = [
        {
            "capture_sha256": digest(pilot.canonical(candidate["capture"])),
            "assertion_id": "a1",
        }
    ]
    report = {
        "schema": "malleus.paper-v4.reconciliation-report/v1",
        "assessments": [
            {
                "record_id": "observation:old",
                "status": "AMENDMENT",
                "contexts": [
                    {
                        "status": "REPRESENTED",
                        "statement": "The numeric value is present.",
                        "graph_refs": [
                            {
                                "record_id": "observation:old",
                                "path": ["properties", "value_lower"],
                                "value": base["entities"][0]["properties"][
                                    "value_lower"
                                ],
                            }
                        ],
                        "evidence": evidence,
                    }
                ],
            }
        ],
        "changes": [
            {
                "record_id": "observation:old",
                "property": "description",
                "reason": "Source qualifies this value.",
                "evidence": evidence,
            }
        ],
        "out_of_scope": [],
    }
    return base, candidate, report, canonical(reading)


def check(base, candidate, report, reading, captures=None):
    from reconciliation import check_reconciliation

    return check_reconciliation(
        base,
        candidate,
        report,
        reading,
        {} if captures is None else captures,
        "source:one",
        targets={"observation:old"},
    )


def test_accepts_supported_shape_without_certifying_meaning():
    check(*example())


@pytest.mark.parametrize(
    "fault",
    [
        "missing_path",
        "wrong_value",
        "wrong_record",
        "proposed_as_existing",
        "empty_refs",
        "wrong_capture",
        "wrong_assertion",
        "wrong_reading",
        "wrong_source",
        "truncated_block",
        "missing_change",
        "duplicate_change",
        "missing_edge",
        "changed_predicate",
        "number_change",
        "unit_removal",
        "wrong_type",
        "extra_record",
        "no_op",
        "false_status",
        "missing_assessment",
        "empty_context",
        "duplicate_assertion",
    ],
)
def test_refuses_reconciliation_error_classes(fault):
    base, candidate, report, reading = example()
    context = report["assessments"][0]["contexts"][0]
    ref = context["graph_refs"][0]
    entity = candidate["records"]["entities"][0]
    if fault == "missing_path":
        ref["path"] = ["properties", "absent"]
    elif fault == "wrong_value":
        ref["value"] = "wrong"
    elif fault == "wrong_record":
        ref["record_id"] = "site:one"
    elif fault == "proposed_as_existing":
        ref.update(
            record_id=entity["id"],
            path=["properties", "description"],
            value=entity["properties"]["description"],
        )
    elif fault == "empty_refs":
        context["graph_refs"] = []
    elif fault == "wrong_capture":
        context["evidence"][0]["capture_sha256"] = "sha256:" + "9" * 64
    elif fault == "wrong_assertion":
        context["evidence"][0]["assertion_id"] = "absent"
    elif fault in {
        "wrong_reading",
        "wrong_source",
        "truncated_block",
        "duplicate_assertion",
    }:
        if fault == "wrong_reading":
            candidate["capture"]["reading_sha256"] = "sha256:" + "9" * 64
        elif fault == "wrong_source":
            candidate["capture"]["attribution"]["source_id"] = "source:other"
        elif fault == "duplicate_assertion":
            candidate["capture"]["assertions"] *= 2
        else:
            candidate["capture"]["assertions"][0]["statement"] = "qualifier"
        context["evidence"][0]["capture_sha256"] = digest(
            pilot.canonical(candidate["capture"])
        )
    elif fault == "missing_change":
        report["changes"] = []
    elif fault == "duplicate_change":
        report["changes"] *= 2
    elif fault == "missing_edge":
        candidate["records"]["relations"] = []
        candidate["supersessions"].pop()
    elif fault == "changed_predicate":
        candidate["records"]["relations"][0]["properties"]["relation_type"] = (
            "CONTRADICTS"
        )
    elif fault == "number_change":
        entity["properties"]["value_lower"] = 8
        report["changes"].append({**report["changes"][0], "property": "value_lower"})
    elif fault == "unit_removal":
        del entity["properties"]["unit"]
        report["changes"].append({**report["changes"][0], "property": "unit"})
    elif fault == "wrong_type":
        entity["type"] = "Claim"
    elif fault == "extra_record":
        candidate["records"]["entities"].append({**entity, "id": "extra"})
    elif fault == "no_op":
        del entity["properties"]["description"]
        report["changes"] = []
    elif fault == "false_status":
        report["assessments"][0]["status"] = "NO_CHANGE"
    elif fault == "missing_assessment":
        report["assessments"] = []
    else:
        report["assessments"][0]["contexts"] = []
    with pytest.raises(ValueError):
        check(base, candidate, report, reading)


def test_same_assertion_id_resolves_only_inside_the_identified_capture():
    base, candidate, report, reading = example()
    prior = deepcopy(candidate["capture"])
    prior["assertions"][0]["statement"] = "Synthetic"
    identity = digest(canonical(prior))
    report["assessments"][0]["contexts"][0]["evidence"] = [
        {"capture_sha256": identity, "assertion_id": "a1"}
    ]
    check(base, candidate, report, reading, {identity: canonical(prior)})
    prior["assertions"][0]["id"] = "other"
    with pytest.raises(ValueError, match="identity"):
        check(base, candidate, report, reading, {identity: canonical(prior)})


def test_missing_context_can_be_reported_without_inventing_a_field_or_candidate():
    base, _, report, reading = example()
    report["assessments"][0].update(
        status="UNRESOLVED",
        contexts=[
            {
                "status": "MISSING",
                "statement": "This context is not represented.",
                "graph_refs": [],
                "evidence": [],
            }
        ],
    )
    report["changes"] = []
    check(base, None, report, reading)


def test_historical_core_whitespace_rule_does_not_weaken_new_complete_blocks():
    base, candidate, report, reading_bytes = example()
    reading = json.loads(reading_bytes)
    reading["pages"][0]["blocks"][0]["text"] = "Synthetic\nscope qualifier"
    reading_bytes = canonical(reading)
    candidate["capture"]["reading_sha256"] = digest(reading_bytes)
    prior = deepcopy(candidate["capture"])
    prior_identity = digest(canonical(prior))
    candidate["capture"]["assertions"][0]["statement"] = "Synthetic\nscope qualifier"
    candidate_identity = digest(pilot.canonical(candidate["capture"]))
    report["assessments"][0]["contexts"][0]["evidence"] = [
        {"capture_sha256": prior_identity, "assertion_id": "a1"}
    ]
    report["changes"][0]["evidence"] = [
        {"capture_sha256": candidate_identity, "assertion_id": "a1"}
    ]
    check(base, candidate, report, reading_bytes, {prior_identity: canonical(prior)})
    candidate["capture"]["assertions"][0]["statement"] = "Synthetic scope qualifier"
    with pytest.raises(ValueError, match="complete selected block"):
        check(
            base, candidate, report, reading_bytes, {prior_identity: canonical(prior)}
        )


def test_context_is_actual_values_subjects_and_definitions():
    from reconciliation import build_context

    base, _, _, _ = example()
    documents = {
        "ontology.yaml": b"classes:\n  Observation:\n    description: A reported observation\n"
    }
    context = build_context(base, documents, targets={"observation:old"})
    assert context["records"]["observation:old"] == base["entities"][0]
    assert context["records"]["site:one"] == base["entities"][2]
    assert (
        context["definitions"]["ontology.yaml"]["classes"]["Observation"]["description"]
        == "A reported observation"
    )
    base["entities"][0]["properties"]["subject"] = "absent"
    with pytest.raises(ValueError, match="subject"):
        build_context(base, documents, targets={"observation:old"})


def decision_fixture(tmp_path):
    run = tmp_path / "run"
    packet = run / "source-review-01"
    (packet / "evidence").mkdir(parents=True)
    candidate = run / "candidate.json"
    candidate.write_bytes(b'{"candidate":1}')
    candidate.with_suffix(".report.json").write_bytes(b'{"report":1}')
    (run / "manifest.json").write_bytes(b'{"run":1}')
    (packet / "review.md").write_text("Independent assessment supports the batch.")
    manifest = {
        "run_manifest_sha256": digest((run / "manifest.json").read_bytes()),
        "candidate_sha256": digest(candidate.read_bytes()),
        "report_sha256": digest(candidate.with_suffix(".report.json").read_bytes()),
        "materials": [],
    }
    (packet / "manifest.json").write_bytes(canonical(manifest))
    decision = {
        "status": "ALLOW_SUPPORTED_BATCH",
        "run_manifest_sha256": manifest["run_manifest_sha256"],
        "candidate_sha256": manifest["candidate_sha256"],
        "report_sha256": manifest["report_sha256"],
        "review_sha256": digest((packet / "review.md").read_bytes()),
        "reviewer_thread_id": "independent-session",
        "ratification": "PENDING_HUMAN",
    }
    (packet / "decision.json").write_bytes(canonical(decision))
    return run, candidate, packet, decision


def test_affirmative_exact_review_is_required_not_a_semantic_oracle(tmp_path):
    from reconciliation import authorize

    run, candidate, _, decision = decision_fixture(tmp_path)
    assert authorize(run, candidate) == decision


@pytest.mark.parametrize(
    "fault",
    [
        "missing",
        "withheld",
        "structural_only",
        "candidate",
        "report",
        "run",
        "review",
        "packet",
        "no_reviewer",
    ],
)
def test_absent_or_stale_review_cannot_authorize_retention(tmp_path, fault):
    from reconciliation import authorize

    run, candidate, packet, decision = decision_fixture(tmp_path)
    if fault == "missing":
        (packet / "decision.json").unlink()
    elif fault in {"withheld", "structural_only", "no_reviewer"}:
        if fault == "no_reviewer":
            decision["reviewer_thread_id"] = ""
        else:
            decision["status"] = (
                "WITHHOLD" if fault == "withheld" else "STRUCTURAL_PREFLIGHT_ONLY"
            )
        (packet / "decision.json").write_bytes(canonical(decision))
    else:
        path = {
            "candidate": candidate,
            "report": candidate.with_suffix(".report.json"),
            "run": run / "manifest.json",
            "review": packet / "review.md",
            "packet": packet / "manifest.json",
        }[fault]
        path.write_bytes(b"{}")
    before = {str(p): p.read_bytes() for p in run.rglob("*") if p.is_file()}
    with pytest.raises(ValueError):
        authorize(run, candidate)
    assert {str(p): p.read_bytes() for p in run.rglob("*") if p.is_file()} == before


def test_executor_routes_review_before_attempt_creation_or_retention():
    import inspect
    import repair

    source = inspect.getsource(repair.execute)
    assert source.index("authorize(run, candidate_path)") < source.index("target.mkdir")
    assert source.index("authorize(run, candidate_path)") < source.index(
        "copy_history("
    )


@pytest.mark.parametrize("status", ["WITHHOLD", "STRUCTURAL_PREFLIGHT_ONLY"])
def test_actual_executor_refuses_without_writing_an_attempt(
    tmp_path, monkeypatch, status
):
    import repair

    run, candidate, packet, decision = decision_fixture(tmp_path)
    decision["status"] = status
    (packet / "decision.json").write_bytes(canonical(decision))
    monkeypatch.setattr(
        repair,
        "preflight",
        lambda _: ({"schema": "malleus.paper-v4.reconciliation/v1"}, None, []),
    )
    output = run / "evidence/attempt-01"
    with pytest.raises(ValueError, match="affirmative"):
        repair.execute(
            run, "evidence", candidate, output, transaction_time="2026-09-08T00:00:00Z"
        )
    assert not output.exists()


def test_prior_withheld_outcome_stays_exact():
    from integration import BASE

    previous = BASE.parent / "sol-integration-01"
    assert (
        digest((previous / "outcome.json").read_bytes())
        == "sha256:aa31bf28834586ee92d1031acd8c8ee632df2f12a7c5dcecc266cc5ad918582e"
    )


def test_real_frozen_packet_and_public_no_candidate_preflight():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_reconciliation import check_real_packet; check_real_packet()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_frozen_first_submission_and_corrected_harness_preserve_the_run():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_reconciliation import check_submission; check_submission()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_frozen_withheld_batch_cannot_reach_retention_or_after_queries():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_reconciliation import check_withheld; check_withheld()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_withheld():
    from followup import verify_materials
    from integration import BASE
    import repair

    run = BASE.parent / "sol-reconciliation-01"
    packet = run / "source-review-01"
    outcome = json.loads((run / "outcome.json").read_bytes())
    decision = json.loads((packet / "decision.json").read_bytes())
    manifest = json.loads((packet / "manifest.json").read_bytes())
    assert outcome["status"] == "WITHHELD_AFTER_SOURCE_ASSESSMENT"
    assert decision["status"] == "WITHHOLD"
    assert decision["ratification"] == "PENDING_HUMAN"
    for field, path in {
        "run_manifest_sha256": run / "manifest.json",
        "candidate_sha256": run / outcome["candidate"],
        "report_sha256": (run / outcome["candidate"]).with_suffix(".report.json"),
    }.items():
        assert (
            outcome[field]
            == decision[field]
            == manifest[field]
            == digest(path.read_bytes())
        )
    assert (
        outcome["source_review_sha256"]
        == decision["review_sha256"]
        == digest((packet / "review.md").read_bytes())
    )
    assert outcome["source_review_sha256"] == (
        "sha256:c89bb08903a4110df789ecd665ae28a7cf1622d228e990de041e52d0f320e071"
    )
    assert outcome["source_review_decision_sha256"] == digest(
        (packet / "decision.json").read_bytes()
    )
    verify_materials(packet, manifest["materials"])
    accepted = BASE / "evidence/attempt-01"
    for field, path in {
        "base_ledger_sha256": accepted / "ledger/history.jsonl",
        "base_graph_sha256": accepted / "export-records.json",
        "base_replay_receipt_sha256": accepted / "replay-receipt.json",
        "base_query_sha256": BASE / "depth-query-01/query-result.json",
    }.items():
        assert outcome[field] == digest(path.read_bytes())
    assert (run / "base-history.jsonl").read_bytes() == (
        accepted / "ledger/history.jsonl"
    ).read_bytes()
    assert not outcome["retention_performed"]
    assert not outcome["admission_performed"]
    assert not outcome["after_queries_run"]
    assert not list((run / "evidence").glob("attempt-*"))
    assert not list(run.rglob("query-result.json"))
    before = {str(p): digest(p.read_bytes()) for p in run.rglob("*") if p.is_file()}
    with pytest.raises(ValueError, match=outcome["execution_guard_refusal"]):
        repair.execute(
            run,
            "evidence",
            run / outcome["candidate"],
            run / "evidence/attempt-01",
            transaction_time="2026-09-08T00:00:00Z",
        )
    assert {
        str(p): digest(p.read_bytes()) for p in run.rglob("*") if p.is_file()
    } == before


def check_submission():
    from followup import verify_materials
    from input_delivery import verify_delivery
    from integration_review import inspect_candidate

    run = pilot.ROOT / "private/paper-v4-answer-demonstration/sol-reconciliation-01"
    manifest = json.loads((run / "manifest.json").read_bytes())
    old_bytes = (run / "harness-v1/manifest.json").read_bytes()
    assert digest(old_bytes) == manifest["supersedes_manifest_sha256"]
    old = {item["path"]: item["sha256"] for item in json.loads(old_bytes)["materials"]}
    current = {item["path"]: item["sha256"] for item in manifest["materials"]}
    assert {name for name in old if old[name] != current[name]} == {"reconciliation.py"}
    assert (
        digest((run / "harness-v1/reconciliation.py").read_bytes())
        == old["reconciliation.py"]
    )
    candidate = run / "evidence/producer/work/candidate-01.json"
    assert (
        digest(candidate.read_bytes())
        == "sha256:5d5b3613bb3fc48c981b811167e1ffebb36e06813c9c91e7ff75a683c583af9e"
    )
    assert (
        digest(candidate.with_suffix(".report.json").read_bytes())
        == "sha256:f53767ee2af5011722c1b037f9e60881a88ae570d0e5719e81b971d3bdc3206b"
    )
    before = (run / "base-history.jsonl").read_bytes()
    result = inspect_candidate(run, candidate)
    assert result["status"] == "STRUCTURAL_PREFLIGHT_ONLY"
    assert (
        result["plan_sha256"]
        == "sha256:d1bd47a13ba5f646bab933c44174c033091da84e564574ab564b1a37ea4352db"
    )
    assert (run / "base-history.jsonl").read_bytes() == before
    review = run / "source-review-01"
    packet = json.loads((review / "manifest.json").read_bytes())
    verify_materials(review, packet["materials"])
    assert len(packet["materials"]) == 22
    assert (
        verify_delivery(run / "evidence", "initial")["frames_per_input"]
        == json.loads((run / "evidence/input-delivery-initial.json").read_bytes())[
            "frames_per_input"
        ]
    )


def check_real_packet():
    from tempfile import TemporaryDirectory
    from integration_review import inspect_candidate, prepare
    from reconciliation import TARGETS, stage
    import repair

    with TemporaryDirectory(
        dir=pilot.ROOT / "private", prefix="reconciliation-test-"
    ) as directory:
        root = Path(directory)
        run = root / "run"
        manifest = stage(run)
        assert manifest["maximum_structural_returns"] == 2
        assert manifest["producer_effort"] == "ultra"
        declared = json.loads(
            (run / "evidence/producer-input-manifest.json").read_bytes()
        )["declared_inputs"]
        assert not any(
            any(
                word in item["target"]
                for word in ("question", "review", "answer", "candidate")
            )
            for item in declared
        )
        assert (
            len([item for item in declared if item["target"].endswith("-capture.json")])
            == 5
        )
        inputs = run / "evidence/producer/inputs"
        actual = repair.indexed(
            json.loads((inputs / "baseline-records.json").read_bytes())
        )
        context = json.loads((inputs / "reconciliation-context.json").read_bytes())
        assert set(context["targets"]) == TARGETS
        assert all(actual[key][1] == row for key, row in context["records"].items())
        assert (
            context["records"]["interface:lab"]["properties"]["name"]
            == "lithosphere-asthenosphere boundary"
        )
        before = (run / "base-history.jsonl").read_bytes()
        candidate = run / "evidence/producer/work/candidate-01.json"
        report = {
            "schema": "malleus.paper-v4.reconciliation-report/v1",
            "assessments": [
                {
                    "record_id": key,
                    "status": "UNRESOLVED",
                    "contexts": [
                        {
                            "status": "UNRESOLVED",
                            "statement": "Synthetic no-candidate control, not a semantic judgment.",
                            "graph_refs": [],
                            "evidence": [],
                        }
                    ],
                }
                for key in sorted(TARGETS)
            ],
            "changes": [],
            "out_of_scope": [],
        }
        candidate.with_suffix(".report.json").write_bytes(canonical(report))
        candidate.with_name("refusal.md").write_text("Synthetic no-candidate control")
        assert inspect_candidate(run, candidate)["status"] == "NO_CANDIDATE_REPORTED"
        packet = prepare(run, candidate, root / "review")
        assert packet["candidate_sha256"] is None
        assert packet["schema"] == "malleus.paper-v4.reconciliation-source-review/v1"
        assert (run / "base-history.jsonl").read_bytes() == before
        assert not list(run.rglob("population-plan.json"))
        assert not list(run.rglob("ledger"))
