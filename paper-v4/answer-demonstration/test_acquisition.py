"""The experiment-context amendment is distinct, additive and review-bound."""

import pytest
import repair
from copy import deepcopy
import json
import subprocess
import sys
from review_packet import canonical, digest


def condition():
    return {
        "schema": "malleus.paper-v4.acquisition/v1",
        "condition": "SOURCE_GROUNDED_ACQUISITION_RELATIONS",
        "amendment_id": "acquisition-01",
        "query_reader": "SubjectGraphReads",
    }


def test_acquisition_uses_current_reader_and_its_own_namespace():
    assert repair.context(condition()) == (
        "evidence/producer/inputs",
        None,
        "SubjectGraphReads",
    )
    assert all(
        "acquisition-01" in value
        for value in repair.artifact_ids(condition(), "evidence")
    )


@pytest.mark.parametrize(
    "key,value",
    [
        ("condition", "FRESH_END_TO_END"),
        ("amendment_id", "reconciliation-feedback-01"),
        ("query_reader", "GraphReads"),
    ],
)
def test_acquisition_rejects_a_mislabelled_condition(key, value):
    manifest = condition()
    manifest[key] = value
    with pytest.raises(ValueError):
        repair.context(manifest)


def sample():
    import acquisition as a

    records = {
        k: []
        for k in ("entities", "relations", "events", "signals", "event_participations")
    }
    base = deepcopy(records)
    base["entities"] = [
        {"id": key, "type": kind, "properties": {}} for key, kind in a.TARGETS.items()
    ]
    reading = canonical(
        {
            "pages": [
                {
                    "blocks": [
                        {"id": "b:test", "text": "The campaign used the instrument."}
                    ]
                }
            ]
        }
    )
    candidate = {
        "records": records,
        "supersessions": [],
        "capture": {
            "schema": "malleus.document-capture/private-v0",
            "reading_sha256": digest(reading),
            "attribution": {
                "source_id": "source:test",
                "author": "author",
                "date": "2026",
            },
            "nothing_assertable": [],
            "assertions": [
                {
                    "id": "a:new",
                    "block": "b:test",
                    "statement": "The campaign used the instrument.",
                    "modality": "STATED",
                    "formalized_by": [],
                    "gaps": [],
                }
            ],
        },
    }
    records["relations"] = [
        {
            "id": "acquisition:evidence:new",
            "type": "ResearchRelation",
            "source_id": "campaign:smarties",
            "target_id": "instrument:obs",
            "properties": {"relation_type": "OBSERVED_WITH"},
        }
    ]
    report = {
        "schema": "malleus.paper-v4.acquisition-report/v1",
        "relations": [
            {
                "record_id": "acquisition:evidence:new",
                "reason": "Synthetic test explanation, not paper evidence.",
                "assertion_ids": ["a:new"],
            }
        ],
        "limitations": [],
    }
    return base, candidate, report, reading


def check(base, candidate, report, reading):
    from acquisition import check_acquisition

    check_acquisition(base, candidate, report, reading, "source:test")


def test_supported_shape_passes_without_certifying_source_meaning():
    args = sample()
    before = deepcopy(args)
    check(*args)
    assert args == before


@pytest.mark.parametrize(
    "defect",
    [
        "supersession",
        "entity",
        "event",
        "reused",
        "unknown_endpoint",
        "reversed",
        "wrong_predicate",
        "wrong_family",
        "extra_property",
        "duplicate",
        "missing_base",
        "wrong_reading",
        "wrong_source",
        "partial_block",
        "unknown_block",
        "unknown_assertion",
        "missing_explanation",
        "duplicate_explanation",
        "empty_reason",
    ],
)
def test_scope_and_evidence_binding_refuse(defect):
    base, candidate, report, reading = sample()
    row = candidate["records"]["relations"][0]
    assertion = candidate["capture"]["assertions"][0]
    if defect == "supersession":
        candidate["supersessions"] = [
            {"record_id": row["id"], "supersedes_record_id": "campaign:smarties"}
        ]
    elif defect == "entity":
        candidate["records"]["entities"] = [
            {"id": "new", "type": "Campaign", "properties": {}}
        ]
    elif defect == "event":
        candidate["records"]["events"] = [
            {"id": "new", "type": "Event", "properties": {}}
        ]
    elif defect == "reused":
        row["id"] = "campaign:smarties"
    elif defect == "unknown_endpoint":
        row["target_id"] = "count:useful-obs"
    elif defect == "reversed":
        row["source_id"], row["target_id"] = row["target_id"], row["source_id"]
    elif defect == "wrong_predicate":
        row["properties"]["relation_type"] = "SUPPORTS"
    elif defect == "wrong_family":
        row["type"] = "FundingRelation"
    elif defect == "extra_property":
        row["properties"]["count"] = 555
    elif defect == "duplicate":
        candidate["records"]["relations"].append(
            {**row, "id": "acquisition:evidence:duplicate"}
        )
    elif defect == "missing_base":
        base["entities"].pop()
    elif defect == "wrong_reading":
        candidate["capture"]["reading_sha256"] = "sha256:" + "0" * 64
    elif defect == "wrong_source":
        candidate["capture"]["attribution"]["source_id"] = "source:wrong"
    elif defect == "partial_block":
        assertion["statement"] = "The campaign"
    elif defect == "unknown_block":
        assertion["block"] = "absent"
    elif defect == "unknown_assertion":
        report["relations"][0]["assertion_ids"] = ["absent"]
    elif defect == "missing_explanation":
        report["relations"] = []
    elif defect == "duplicate_explanation":
        report["relations"] *= 2
    elif defect == "empty_reason":
        report["relations"][0]["reason"] = " "
    with pytest.raises(ValueError):
        check(base, candidate, report, reading)


def test_stage_uses_accepted_history_and_count_reader_without_feedback():
    command = "from test_acquisition import check_stage; check_stage()"
    result = subprocess.run(
        [sys.executable, "-c", command], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


def check_stage():
    from pathlib import Path
    from tempfile import TemporaryDirectory
    import pilot
    from acquisition import stage

    with TemporaryDirectory(
        prefix="acquisition-test-", dir=pilot.ROOT / "private"
    ) as directory:
        run = Path(directory) / "run"
        stage(run)
        assert_stage(run)


def assert_stage(run):
    manifest = json.loads((run / "manifest.json").read_bytes())
    assert manifest["condition"] == condition()["condition"]
    assert (
        manifest["base_receipt_sha256"]
        == "sha256:8a6a7c85df6b873e19806ffc09b916dc53332d6b3a8492d155908f34ec0a8b6a"
    )
    declared = json.loads((run / "evidence/producer-input-manifest.json").read_bytes())[
        "declared_inputs"
    ]
    assert not any(
        any(
            word in item["target"]
            for word in (
                "question",
                "feedback",
                "review",
                "answers",
                "reconciliation-context",
            )
        )
        for item in declared
    )
    assert (
        len([item for item in declared if item["target"].endswith("-capture.json")])
        == 6
    )
    assert (
        digest((run / "answers.py").read_bytes())
        == "sha256:7ad378ba843765f7a06df42932c8aee7316dcb62d798ffdd1a9a1b610e48e08f"
    )
    assert (
        sum(
            len(v)
            for v in json.loads(
                (run / "evidence/producer/inputs/baseline-records.json").read_bytes()
            ).values()
        )
        == 164
    )


def test_execution_requires_review_before_creating_output(tmp_path, monkeypatch):
    monkeypatch.setattr(repair, "preflight", lambda _: (condition(), None, []))
    output = tmp_path / "evidence/attempt-01"
    with pytest.raises(ValueError, match="source-review authorization unavailable"):
        repair.execute(
            tmp_path,
            "evidence",
            tmp_path / "candidate.json",
            output,
            transaction_time="2026-09-08T00:00:00Z",
        )
    assert not output.exists()


def test_structural_preflight_calls_match_public_signatures():
    import ast
    import inspect
    import acquisition

    tree = ast.parse(inspect.getsource(acquisition.structural_check))
    for name in ("adapt_document_assertions", "compile_population_plan"):
        call = next(
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == name
        )
        inspect.signature(getattr(repair.api, name)).bind(
            *[None for _ in call.args], **{item.arg: None for item in call.keywords}
        )
