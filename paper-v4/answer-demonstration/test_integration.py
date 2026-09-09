"""Context integration is source-located, bounded and preservation checked."""

import json
from pathlib import Path
import subprocess
import sys

import pytest


def example():
    from test_qualification import example as pair

    base, candidate = pair()
    for row in base["entities"][1:]:
        row.update(type="Entity", properties={})
    quote = "Synthetic scope qualifier"
    reading = {"pages": [{"blocks": [{"id": "b1", "text": quote}]}]}
    evidence = [{"block": "b1", "quote": quote}]
    report = {
        "schema": "malleus.paper-v4.integration-report/v1",
        "assessments": [
            {
                "record_id": "observation:old",
                "status": "AMENDMENT",
                "reason": "Source scope applies to this observation",
                "evidence": evidence,
            }
        ],
        "changes": [
            {
                "record_id": "observation:old",
                "property": "description",
                "reason": "Source supplies this qualification",
                "evidence": evidence,
            }
        ],
    }
    return base, candidate, report, reading


def test_accepts_explicit_qualification_and_atomic_dependency_replacement():
    from integration import check_integration

    check_integration(*example())


@pytest.mark.parametrize(
    "fault",
    [
        "silent_value",
        "dropped_value",
        "boolean_value",
        "missing_edge",
        "new_edge",
        "changed_edge",
        "wrong_type",
        "unquantified",
        "reuse",
        "fork",
        "orphan_subject",
        "missing_assessment",
        "duplicate_assessment",
        "false_disposition",
        "invented_quote",
        "normalized_quote",
        "wrong_block",
        "empty_reason",
        "empty_evidence",
        "duplicate_change",
        "extra_change",
        "no_op",
        "bad_schema",
    ],
)
def test_refuses_unexplained_changes_wrong_context_bindings_and_scope_expansion(fault):
    from integration import check_integration

    base, candidate, report, reading = example()
    entity = candidate["records"]["entities"][0]
    edge = candidate["records"]["relations"][0]
    if fault in {"silent_value", "boolean_value"}:
        entity["properties"]["value_lower"] = True if fault == "boolean_value" else 8
    elif fault == "dropped_value":
        del entity["properties"]["value_lower"]
    elif fault == "missing_edge":
        candidate["records"]["relations"] = []
        candidate["supersessions"].pop()
    elif fault == "new_edge":
        candidate["records"]["relations"].append({**edge, "id": "extra"})
    elif fault == "changed_edge":
        edge["properties"]["relation_type"] = "CONTRADICTS"
    elif fault == "wrong_type":
        entity["type"] = "Claim"
    elif fault == "unquantified":
        base["entities"][0]["properties"] = {"subject": "site:one"}
    elif fault == "reuse":
        entity["id"] = "observation:old"
    elif fault == "fork":
        candidate["supersessions"][1]["supersedes_record_id"] = "observation:old"
    elif fault == "orphan_subject":
        base["entities"].append(
            {
                "id": "outside",
                "type": "Claim",
                "properties": {"subject": "observation:old"},
            }
        )
    elif fault == "missing_assessment":
        report["assessments"] = []
    elif fault == "duplicate_assessment":
        report["assessments"] *= 2
    elif fault == "false_disposition":
        report["assessments"][0]["status"] = "NO_CHANGE"
    elif fault == "invented_quote":
        report["changes"][0]["evidence"] = [{"block": "b1", "quote": "invented"}]
    elif fault == "normalized_quote":
        reading["pages"][0]["blocks"][0]["text"] = "Synthetic\nscope qualifier"
        assert report["changes"][0]["evidence"][0]["quote"].split() == (
            reading["pages"][0]["blocks"][0]["text"].split()
        )
    elif fault == "wrong_block":
        report["changes"][0]["evidence"] = [
            {"block": "absent", "quote": "Synthetic scope qualifier"}
        ]
    elif fault == "empty_reason":
        report["changes"][0]["reason"] = " "
    elif fault == "empty_evidence":
        report["changes"][0]["evidence"] = []
    elif fault == "duplicate_change":
        report["changes"] *= 2
    elif fault == "extra_change":
        report["changes"].append({**report["changes"][0], "property": "unit"})
    elif fault == "no_op":
        del entity["properties"]["description"]
        report["changes"] = []
    else:
        report["schema"] = "unknown"
    with pytest.raises((ValueError, KeyError)):
        check_integration(base, candidate, report, reading)


def test_explicit_source_backed_change_is_inspectable_not_automatically_true():
    from integration import check_integration

    base, candidate, report, reading = example()
    candidate["records"]["entities"][0]["properties"]["value_lower"] = 8
    report["changes"].append({**report["changes"][0], "property": "value_lower"})
    check_integration(base, candidate, report, reading)


def test_no_change_and_unresolved_are_real_results_without_empty_admission():
    from integration import check_report

    base, _, report, reading = example()
    report["changes"] = []
    report["assessments"][0]["status"] = "UNRESOLVED"
    report["assessments"][0]["evidence"] = []
    check_report(base, None, report, reading)


def test_retained_structural_returns_preserve_the_semantic_proposal():
    from integration import BASE
    from review_packet import digest

    run = BASE.parent / "sol-integration-01"
    work = run / "evidence/producer/work"
    candidates = [
        json.loads((work / f"candidate-{n:02}.json").read_bytes()) for n in (1, 2, 3)
    ]
    assert (work / "candidate-01.json").read_bytes() == (
        work / "candidate-02.json"
    ).read_bytes()
    assert digest((work / "candidate-01.json").read_bytes()) == (
        "sha256:d05bbaf8e729b86f7e7fbdacdf0648bcbab1be359e8779d0b7903174a90ee169"
    )
    assert digest((work / "candidate-01.report.json").read_bytes()) == (
        "sha256:e4d2542e931c9d2d558c0108ecb5b82c5813e580506a90f63ba8eb0a312c7558"
    )
    assert digest((work / "candidate-02.report.json").read_bytes()) == (
        "sha256:0e5e49faec490c6891259a34ac9b0601a6170f8e3a2c346b18f74f723e391b6e"
    )
    for candidate in candidates[1:]:
        assert set(candidate) == set(candidates[0])
        assert candidate["records"] == candidates[0]["records"]
        assert candidate["supersessions"] == candidates[0]["supersessions"]
    first, final = candidates[0]["capture"], candidates[2]["capture"]
    assert set(first) == set(final)
    for key in first.keys() - {"assertions"}:
        assert first[key] == final[key]
    changed = []
    for before, after in zip(first["assertions"], final["assertions"], strict=True):
        assert set(before) == set(after)
        changed.extend(
            (before["id"], key) for key in before if before[key] != after[key]
        )
    assert changed == [
        ("integration:evidence:assertion:trace-element-assumption", "statement")
    ]
    reports = [
        json.loads((work / f"candidate-{n:02}.report.json").read_bytes())
        for n in (1, 2, 3)
    ]
    for report in reports[1:]:
        assert set(report) == set(reports[0])
        assert report["schema"] == reports[0]["schema"]
        for section in ("assessments", "changes"):
            for before, after in zip(reports[0][section], report[section], strict=True):
                assert set(before) == set(after)
                for key in before.keys() - {"evidence"}:
                    assert before[key] == after[key]
    from followup import verify_materials

    packet = run / "source-review-01"
    manifest = json.loads((packet / "manifest.json").read_bytes())
    verify_materials(packet, manifest["materials"])
    assert manifest["candidate_sha256"] == digest(
        (work / "candidate-03.json").read_bytes()
    )
    assert manifest["report_sha256"] == digest(
        (work / "candidate-03.report.json").read_bytes()
    )
    assert not any("question" in item["path"] for item in manifest["materials"])


def test_retained_candidate_preflight_is_read_only_and_does_not_waive_refusals():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_integration import check_retained; check_retained()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_source_withheld_result_cannot_be_reported_as_an_admitted_graph():
    from integration import BASE
    from review_packet import digest

    run = BASE.parent / "sol-integration-01"
    outcome = json.loads((run / "outcome.json").read_bytes())
    assert outcome["status"] == "WITHHELD_AFTER_SOURCE_ASSESSMENT"
    assert outcome["structural_preflight_passed"] is True
    assert outcome["admission_performed"] is False
    assert outcome["after_queries_run"] is False
    assert outcome["human_ratification"] == "PENDING"
    for key, path in (
        ("run_manifest_sha256", "manifest.json"),
        ("candidate_sha256", outcome["candidate"]),
        ("report_sha256", "evidence/producer/work/candidate-03.report.json"),
        ("source_review_sha256", outcome["source_review"]),
        ("base_ledger_sha256", "base-history.jsonl"),
        ("base_graph_sha256", "evidence/producer/inputs/baseline-records.json"),
    ):
        assert outcome[key] == digest((run / path).read_bytes())
    assert not list((run / "evidence").glob("attempt-*"))
    assert not list((run / "evidence").glob("reproduction-*"))
    assert {
        p.name for p in (run / "evidence/producer/work").glob("candidate-??.json")
    } == {f"candidate-{n:02}.json" for n in (1, 2, 3)}
    result_note = (Path(__file__).parent / "INTEGRATION-RESULTS.md").read_text()
    assert "batch was not admitted" in result_note
    assert "No after-query" in result_note


def check_retained():
    from integration import BASE
    from integration_review import inspect_candidate

    run = BASE.parent / "sol-integration-01"
    work = run / "evidence/producer/work"
    ledger = (run / "base-history.jsonl").read_bytes()
    for ordinal in (1, 2):
        with pytest.raises(ValueError, match="exact selected-reading text"):
            inspect_candidate(run, work / f"candidate-{ordinal:02}.json")
        assert (run / "base-history.jsonl").read_bytes() == ledger
    result = inspect_candidate(run, work / "candidate-03.json")
    assert result["status"] == "STRUCTURAL_PREFLIGHT_ONLY"
    assert result["ledger_unchanged"] is True
    assert result["plan_sha256"] == (
        "sha256:fba1262f76940ec5aa9b14753da41140da42b33038b11b0be8d5a997684f1e17"
    )
    assert (run / "base-history.jsonl").read_bytes() == ledger


def test_stage_excludes_questions_audit_and_expected_values_and_reproduces_reader():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_integration import check_stage; check_stage()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_stage():
    from tempfile import TemporaryDirectory
    from integration import stage, BASE
    from review_packet import digest

    with TemporaryDirectory(dir=BASE.parent, prefix="integration-test-") as temp:
        run = Path(temp) / "run"
        manifest = stage(run)
        assert manifest["condition"] == "QUESTION_WITHHELD_CONTEXT_INTEGRATION"
        declared = json.loads(
            (run / "evidence/producer-input-manifest.json").read_bytes()
        )["declared_inputs"]
        names = {item["target"] for item in declared}
        assert not any(
            any(word in name for word in ("question", "criteria", "audit", "review"))
            for name in names
        )
        assert len([name for name in names if name.endswith("capture.json")]) == 5
        task = (run / "evidence/TASK.md").read_text()
        assert "CQ-" not in task and "RC2" not in task and "seafloor" not in task
        assert digest((run / "answers.py").read_bytes()) == digest(
            (BASE / "depth-method-01/answers.py").read_bytes()
        )
        assert (run / "base-history.jsonl").read_bytes() == (
            BASE / "evidence/attempt-01/ledger/history.jsonl"
        ).read_bytes()


def test_candidate_review_retains_exact_inputs_and_refuses_drift(tmp_path, monkeypatch):
    import integration_review as review
    from review_packet import canonical, digest

    run = tmp_path / "run"
    work = run / "evidence/producer/work"
    work.mkdir(parents=True)
    candidate = work / "candidate-01.json"
    candidate.write_bytes(b"{}")
    candidate.with_suffix(".report.json").write_bytes(b"{}")
    (run / "integration-review-task.md").write_text("Review every changed field")
    inputs = run / "evidence/producer/inputs"
    inputs.mkdir()
    (inputs / "selected-reading.json").write_bytes(b"{}")
    manifest = {
        "schema": "malleus.paper-v4.integration/v1",
        "condition": "QUESTION_WITHHELD_CONTEXT_INTEGRATION",
        "materials": [
            {
                "path": "integration-review-task.md",
                "sha256": digest((run / "integration-review-task.md").read_bytes()),
            },
            {
                "path": "evidence/producer/inputs/selected-reading.json",
                "sha256": digest(b"{}"),
            },
        ],
    }
    (run / "manifest.json").write_bytes(canonical(manifest))
    monkeypatch.setattr(review, "ROOT", tmp_path)
    monkeypatch.setattr(
        review,
        "inspect_candidate",
        lambda run, candidate: {"status": "STRUCTURAL_PREFLIGHT_ONLY"},
    )
    frozen = review.prepare(run, candidate, tmp_path / "review")
    assert frozen["candidate_sha256"] == digest(b"{}")
    assert (
        tmp_path / "review/evidence/candidate.json"
    ).read_bytes() == candidate.read_bytes()
    assert (tmp_path / "review/evidence/report.json").read_bytes() == b"{}"
    assert not (tmp_path / "review/questions.json").exists()
    (inputs / "selected-reading.json").write_bytes(b"drift")
    with pytest.raises(ValueError):
        review.prepare(run, candidate, tmp_path / "bad-review")
    assert not (tmp_path / "bad-review").exists()


def test_real_pinned_preflight_preserves_history_on_refusal_and_no_candidate():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_integration import check_preflight; check_preflight()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_preflight():
    from tempfile import TemporaryDirectory
    from integration import BASE, quantities, stage
    from integration_review import inspect_candidate, prepare
    from review_packet import canonical, digest

    with TemporaryDirectory(
        dir=BASE.parent, prefix="integration-preflight-test-"
    ) as temp:
        root = Path(temp)
        run = root / "run"
        stage(run)
        history = (run / "base-history.jsonl").read_bytes()
        base = json.loads(
            (run / "evidence/producer/inputs/baseline-records.json").read_bytes()
        )
        candidate = run / "evidence/producer/work/candidate-01.json"
        report = {
            "schema": "malleus.paper-v4.integration-report/v1",
            "assessments": [
                {
                    "record_id": key,
                    "status": "UNRESOLVED",
                    "reason": "Synthetic no-candidate control, no semantic assessment",
                    "evidence": [],
                }
                for key in sorted(quantities(base))
            ],
            "changes": [],
        }
        candidate.with_suffix(".report.json").write_bytes(canonical(report))
        result = inspect_candidate(run, candidate)
        assert result["status"] == "NO_CANDIDATE_REPORTED"
        assert result["ledger_unchanged"]
        candidate.with_name("refusal.md").write_text("Synthetic no-candidate control")
        review = prepare(run, candidate, root / "review")
        assert review["candidate_sha256"] is None
        assert review["report_sha256"] == digest(canonical(report))
        assert not (root / "review/evidence/candidate.json").exists()
        candidate.write_bytes(
            canonical(
                {
                    "capture": {},
                    "records": {key: [] for key in base},
                    "supersessions": [],
                }
            )
        )
        with pytest.raises(ValueError, match="one-to-one supersessions"):
            inspect_candidate(run, candidate)
        assert (run / "base-history.jsonl").read_bytes() == history
        assert not list(run.rglob("population-plan.json"))
        assert not list(run.rglob("ledger"))
