"""Bounded amendment guards. Synthetic records are not paper population."""

from copy import deepcopy
from collections import Counter
import ast
import importlib.util
from pathlib import Path
import json
import os
import subprocess
import sys
from types import SimpleNamespace
import unicodedata

import pytest
import yaml


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PAIR = ROOT / "private/paper-v4-relationship-contrast-01"


@pytest.fixture(scope="module")
def subject():
    spec = importlib.util.spec_from_file_location(
        "relationship_repair", HERE / "relationship_repair.py"
    )
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def test_only_the_two_approved_declarations_change(subject):
    source = (PAIR / "b/producer/work/ontology-attempt-02.yaml").read_bytes()
    before = yaml.safe_load(source)
    after = yaml.safe_load(subject.approved_ontology(source))
    assert (
        "PORE_PRESSURE_INCREASE"
        not in before["enums"]["EarthScienceEventType"]["permissible_values"]
    )
    assert after["slots"]["proposed_trigger"]["range"] == "EarthScienceProcess"
    assert after["slots"]["proposed_trigger"]["required"] is False
    assert after["classes"]["HypothesisClaim"]["slots"] == ["proposed_trigger"]
    del after["enums"]["EarthScienceEventType"]["permissible_values"][
        "PORE_PRESSURE_INCREASE"
    ]
    del after["slots"]["proposed_trigger"]
    del after["classes"]["HypothesisClaim"]["slots"]
    assert after == before


@pytest.mark.parametrize("bad", [b"", b"{}", b"classes: {}", b"null"])
def test_missing_ontology_never_defaults(subject, bad):
    with pytest.raises(ValueError, match="ontology"):
        subject.approved_ontology(bad)


def test_unapproved_existing_ontology_refuses(subject):
    source = (PAIR / "b/producer/work/ontology-attempt-02.yaml").read_bytes()
    changed = yaml.safe_load(source)
    changed["classes"]["HypothesisClaim"]["slots"] = ["unapproved"]
    with pytest.raises(ValueError, match="ontology"):
        subject.approved_ontology(yaml.safe_dump(changed).encode())


def test_revision_reopens_with_exact_old_records_and_prefix(subject, tmp_path):
    program = r"""
import json
from pathlib import Path
import sys
import malleus.compiler as api
from relationship_repair import compile_extension, append_revision, BASE
from datetime import datetime, timedelta
old = (BASE / "ledger/history.jsonl").read_bytes()
path = Path(sys.argv[1]) / "history.jsonl"
path.write_bytes(old)
history = api.KnowledgeChangeHistory.reopen(path)
before = history.replay()
compiled, partial, surface = compile_extension(history)
last = datetime.fromisoformat(json.loads(old.splitlines()[-1])["transaction_time"])
try:
    append_revision(history, compiled, partial, (last - timedelta(seconds=1)).isoformat())
except api.KnowledgeChangeRefusal as error:
    assert "transaction_time decreased" in str(error)
else:
    raise AssertionError("decreasing transaction time was accepted")
assert path.read_bytes() == old
revised = append_revision(history, compiled, partial, (last + timedelta(seconds=1)).isoformat())
reopened = api.KnowledgeChangeHistory.reopen(path).replay()
assert path.read_bytes().startswith(old)
assert (BASE / "ledger/history.jsonl").read_bytes() == old
assert revised.graph.export_records() == before.graph.export_records()
assert reopened.graph.export_records() == before.graph.export_records()
assert dict(reopened.record_history) == dict(before.record_history)
assert revised.receipt.canonical_bytes == reopened.receipt.canonical_bytes
assert reopened.partial_contract.identity != before.partial_contract.identity
revision = reopened.contract_revisions[-1]
assert sorted(c.kind for c in revision.changes) == ["ADD_ENUM_VALUE", "ADD_SLOT"]
assert len(reopened.contract_revisions) == len(before.contract_revisions) + 1
field = next(s for t in surface["record_types"] if t["name"] == "HypothesisClaim"
             for s in t["slots"] if s["name"] == "proposed_trigger")
assert field["range_id"].endswith("/EarthScienceProcess")
assert field["required"] is False

# A synthetic source exercises capture -> preparation -> admission after revision.
# It is local test data, not a proposal or finding about the article.
from relationship_repair import canonical, digest, references
import subprocess
text = "In this synthetic example, a hypothesis proposes a pressure increase."
reading = canonical({"pages": [{"page": 1, "blocks": [{"id": "toy:block", "ordinal": 0, "text": text}]}]})
records = {f: [] for f in before.graph.export_records()}
records["events"] = [{"id": "toy:process", "type": "EarthScienceProcess", "properties": {
    "event_type": "PORE_PRESSURE_INCREASE", "assertion_modality": "HYPOTHESISED"}}]
records["entities"] = [{"id": "toy:claim", "type": "HypothesisClaim", "properties": {
    "proposed_trigger": "toy:process", "assertion_modality": "HYPOTHESISED"}}]
capture = canonical({"schema": api.DOCUMENT_CAPTURE_GRAMMAR, "reading_sha256": digest(reading),
    "attribution": {"source_id": "toy:source", "author": "Synthetic test", "date": "2026-01-01"},
    "nothing_assertable": [], "assertions": [{"id": "toy:assertion", "block": "toy:block",
    "modality": "HYPOTHESISED", "statement": text, "gaps": [], "formalized_by": [
        {"record_id": r["id"], "path": ["properties", key]}
        for rows in records.values() for r in rows for key in r["properties"]]}]})
adapted = api.adapt_document_assertions(reading_bytes=reading, capture_bytes=capture,
    capture_id="toy:capture", plan_id="toy:plan", contract_identity=partial.identity,
    records=records, supersessions=[], contract_view=reopened.contract_view)
profile = api.SOURCE_ASSERTION_PROFILE
plan = api.compile_population_plan(json.loads(adapted.canonical_plan_bytes),
    partial_contract=partial, contract_view=reopened.contract_view,
    base_state=api.PopulationBaseState.from_replay(reopened), history_profile=profile)
folder = path.parent
(folder / "reading.json").write_bytes(reading)
(folder / "capture.json").write_bytes(capture)
clock = (last + timedelta(seconds=2)).isoformat()
retained = subprocess.run([sys.executable, "-m", "malleus.compiler_cli", "retain", "--ledger", str(path),
    "--source", "toy:source", "toy:artifact", str(folder / "reading.json"), "application/json",
    "--evidence", "toy:capture", str(folder / "capture.json"), "application/json",
    "--transaction-time", clock, "--actor-id", "toy:actor"], capture_output=True, text=True)
assert retained.returncode == 0, retained.stdout + retained.stderr
history = api.KnowledgeChangeHistory.reopen(path)
prepared = api.prepare_population_change(history=history, plan=json.loads(adapted.canonical_plan_bytes),
    profile=json.loads(profile.canonical_bytes), retention_events=api.population_retention_events(
        history=history, compilation=plan, profile=profile), transaction_time=clock, actor_id="toy:actor")
admitted = api.admit_structural_change(history=history, preparation=prepared,
    transaction_time=clock, actor_id="toy:actor")
final = api.KnowledgeChangeHistory.reopen(path).replay()
assert final.receipt == admitted.receipt
expected = {f: reopened.graph.export_records()[f] + records[f] for f in records}
assert {f: {r["id"]: r for r in rows} for f, rows in final.graph.export_records().items()} == {
    f: {r["id"]: r for r in rows} for f, rows in expected.items()}
references(final.graph.export_records(), final.contract_view)
assert path.read_bytes().startswith(old)
assert (BASE / "ledger/history.jsonl").read_bytes() == old
print(json.dumps({"revision": revision.identity, "graph_preserved": True}))
"""
    env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": os.pathsep.join((str(PAIR / "core/src"), str(HERE))),
    }
    result = subprocess.run(
        [sys.executable, "-c", program, str(tmp_path)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["graph_preserved"] is True


def test_projection_preserves_every_unmentioned_record(subject):
    before = {family: [] for family in subject.FAMILIES}
    before["entities"] = [
        {"id": "old", "type": "Thing", "properties": {"name": "synthetic"}},
        {"id": "untouched", "type": "Thing", "properties": {"name": "keep"}},
    ]
    candidate = {
        "capture": {},
        "records": {f: [] for f in subject.FAMILIES},
        "supersessions": [{"record_id": "new", "supersedes_record_id": "old"}],
    }
    candidate["records"]["entities"] = [
        {"id": "new", "type": "Thing", "properties": {"name": "revised"}}
    ]
    after = subject.project(before, candidate)
    assert after["entities"] == [
        before["entities"][1],
        candidate["records"]["entities"][0],
    ]
    assert before["entities"][0]["id"] == "old"
    changed = deepcopy(after)
    changed["entities"][0]["properties"]["name"] = "lost"
    with pytest.raises(ValueError, match="preservation"):
        subject.check_preservation(before, changed, candidate)


class ToyView:
    """Only slot metadata for unit tests, not a replacement for the Core gate."""

    def has_type(self, name):
        return name in {"Entity", "Claim", "Process", "Event", "Link"}

    def is_subtype_of(self, child, parent):
        return child == parent or (child, parent) in {
            ("Claim", "Entity"),
            ("Process", "Event"),
            ("Link", "Relation"),
        }

    def effective_slots(self, name):
        fields = {
            "Entity": {},
            "Claim": {"subject": "Entity", "proposed_trigger": "Process"},
            "Process": {},
            "Link": {"source_id": "Entity", "target_id": "Entity"},
        }
        return {
            k: SimpleNamespace(range_id=v, multivalued=False)
            for k, v in fields[name].items()
        }


@pytest.fixture
def toy(subject):
    before = {f: [] for f in subject.FAMILIES}
    before["entities"] = [
        {"id": "claim:old", "type": "Claim", "properties": {"name": "synthetic claim"}},
        {
            "id": "evidence:old",
            "type": "Entity",
            "properties": {"name": "synthetic evidence"},
        },
        {"id": "other", "type": "Entity", "properties": {"name": "untouched"}},
    ]
    before["relations"] = [
        {
            "id": "edge:old",
            "type": "Link",
            "source_id": "evidence:old",
            "target_id": "claim:old",
            "properties": {"predicate": "SUPPORTS"},
        }
    ]
    candidate = {
        "capture": {},
        "records": {f: [] for f in subject.FAMILIES},
        "supersessions": [
            {"record_id": "claim:new", "supersedes_record_id": "claim:old"},
            {"record_id": "edge:new", "supersedes_record_id": "edge:old"},
        ],
    }
    candidate["records"]["entities"] = [
        {
            "id": "claim:new",
            "type": "Claim",
            "properties": {
                "name": "revised synthetic claim",
                "proposed_trigger": "process:new",
            },
        }
    ]
    candidate["records"]["events"] = [
        {"id": "process:new", "type": "Process", "properties": {}}
    ]
    candidate["records"]["relations"] = [
        {**deepcopy(before["relations"][0]), "id": "edge:new", "target_id": "claim:new"}
    ]
    return before, candidate


def check_toy(subject, before, candidate):
    return subject.check_scope(
        before, candidate, ToyView(), primary={"claim:old"}, addition_types={"Process"}
    )


def test_supported_referral_structure_survives_replacement(subject, toy):
    before, candidate = toy
    after = check_toy(subject, before, candidate)
    assert next(r for r in after["relations"] if r["id"] == "edge:new")[
        "properties"
    ] == {"predicate": "SUPPORTS"}


@pytest.mark.parametrize(
    "mutation",
    [
        "omitted_dependent",
        "wrong_target_type",
        "missing_target",
        "unrelated_edit",
        "changed_evidence_predicate",
        "reused_id",
        "duplicate_prior",
        "new_outside_type",
    ],
)
def test_scope_and_reference_failures_refuse(subject, toy, mutation):
    before, candidate = toy
    if mutation == "omitted_dependent":
        candidate["records"]["relations"] = []
        candidate["supersessions"].pop()
    elif mutation in {"wrong_target_type", "missing_target"}:
        candidate["records"]["entities"][0]["properties"]["proposed_trigger"] = (
            "other" if mutation == "wrong_target_type" else "missing"
        )
    elif mutation == "unrelated_edit":
        candidate["records"]["entities"].append(
            {"id": "other:new", "type": "Entity", "properties": {}}
        )
        candidate["supersessions"].append(
            {"record_id": "other:new", "supersedes_record_id": "other"}
        )
    elif mutation == "changed_evidence_predicate":
        candidate["records"]["relations"][0]["properties"]["predicate"] = "CHALLENGES"
    elif mutation == "reused_id":
        candidate["records"]["events"][0]["id"] = "other"
    elif mutation == "duplicate_prior":
        candidate["supersessions"].append(candidate["supersessions"][0])
    else:
        candidate["records"]["entities"].append(
            {"id": "new:extra", "type": "Entity", "properties": {}}
        )
    with pytest.raises(ValueError):
        check_toy(subject, before, candidate)


def test_each_problem_and_each_proposed_record_must_be_accounted(subject, toy):
    _, candidate = toy
    problems = {"bounds", "cause", "uncertainty"}
    report = {
        "problems": [
            {
                "id": name,
                "status": "PROPOSED" if name == "cause" else "UNRESOLVED",
                "record_ids": [
                    r["id"] for rows in candidate["records"].values() for r in rows
                ]
                if name == "cause"
                else [],
                "blocks": ["synthetic:block"],
                "reason": "Specific synthetic explanation",
            }
            for name in sorted(problems)
        ]
    }
    subject.check_report(report, candidate, problems, {"synthetic:block"})
    bad = deepcopy(report)
    bad["problems"].pop()
    with pytest.raises(ValueError, match="problem"):
        subject.check_report(bad, candidate, problems, {"synthetic:block"})
    bad = deepcopy(report)
    next(r for r in bad["problems"] if r["id"] == "cause")["record_ids"].pop()
    with pytest.raises(ValueError, match="record"):
        subject.check_report(bad, candidate, problems, {"synthetic:block"})


@pytest.mark.parametrize(
    "failure", ["absent", "refused", "stale", "missing_record", "same_author"]
)
def test_no_admission_without_complete_independent_review(subject, toy, failure):
    _, candidate = toy
    bindings = {
        "candidate": subject.digest(subject.canonical(candidate)),
        "reading": "sha256:toy",
    }
    review = {
        "status": "ALLOW_SUPPORTED_BATCH",
        "bindings": bindings,
        "reviewer_thread_id": "reviewer",
        "ratification": "PENDING_HUMAN",
        "records": [
            {
                "id": r["id"],
                "verdict": "SUPPORTED",
                "blocks": ["synthetic:block"],
                "reason": "checked",
            }
            for rows in candidate["records"].values()
            for r in rows
        ],
        "problems": [
            {
                "id": p,
                "status": "UNRESOLVED",
                "reason": "synthetic limit",
                "blocks": ["synthetic:block"],
            }
            for p in ("bounds", "cause", "uncertainty")
        ],
    }
    subject.check_review(
        review, candidate, bindings, "producer", "reviewer", {"synthetic:block"}
    )
    if failure == "absent":
        review = None
    elif failure == "refused":
        review["status"] = "REFUSE_BATCH"
    elif failure == "stale":
        review["bindings"] = {**bindings, "candidate": "changed"}
    elif failure == "missing_record":
        review["records"].pop()
    else:
        review["reviewer_thread_id"] = "producer"
    with pytest.raises(ValueError, match="review"):
        subject.check_review(
            review, candidate, bindings, "producer", "reviewer", {"synthetic:block"}
        )


def test_staging_never_overwrites_a_retained_file(subject, tmp_path):
    subject.write_new(tmp_path, {"a.json": b"first"})
    with pytest.raises(FileExistsError):
        subject.write_new(tmp_path, {"b.json": b"new", "a.json": b"replacement"})
    assert (tmp_path / "a.json").read_bytes() == b"first"
    assert not (tmp_path / "b.json").exists()


def test_source_refusal_precedes_any_history_copy(subject, tmp_path, monkeypatch):
    def refuse(*args):
        raise ValueError("source review refused")

    monkeypatch.setattr(subject, "authorize", refuse)
    destination = tmp_path / "accepted"
    with pytest.raises(ValueError, match="source review refused"):
        subject.execute(
            tmp_path, tmp_path / "candidate.json", tmp_path / "review", destination
        )
    assert not destination.exists()


def test_retained_packet_must_still_match_its_original_baseline(subject):
    run = ROOT / "private/paper-v4-relationship-repair-01"
    manifest = json.loads((run / "manifest.json").read_bytes())
    inputs = {
        name: (run / "producer/inputs" / name).read_bytes()
        for name in (
            "selected-reading.json",
            "base-capture.json",
            "base-records.json",
            "ontology.yaml",
        )
    }
    subject.check_baseline_inputs(manifest["baseline"], inputs)
    for name in inputs:
        changed = {**inputs, name: inputs[name] + b" "}
        with pytest.raises(ValueError, match="baseline"):
            subject.check_baseline_inputs(manifest["baseline"], changed)


def test_witness_evidence_uses_capture_identity_not_global_assertion_label(subject):
    old = subject.canonical(
        {
            "assertions": [
                {"id": "same-local-id", "block": "old:block", "statement": "old"}
            ]
        }
    )
    new = subject.canonical(
        {
            "assertions": [
                {"id": "same-local-id", "block": "new:block", "statement": "new"}
            ]
        }
    )
    traces = {
        "records": [
            {
                "record_id": "old:record",
                "evidence": {"old:capture": subject.digest(old)},
                "derivations": [{"locator": "same-local-id"}],
            },
            {
                "record_id": "new:record",
                "evidence": {"new:capture": subject.digest(new)},
                "derivations": [{"locator": "same-local-id"}],
            },
        ]
    }
    query = {
        "queries": [
            {
                "question_id": "synthetic:q",
                "rows": [
                    {
                        "kind": "ENTITY",
                        "witness": {"record_id": identity},
                        "case_ordinals": [1],
                    }
                    for identity in ("old:record", "new:record")
                ],
            }
        ]
    }
    captures = {"old:capture": old, "new:capture": new}
    joined = subject.join_witnesses(query, traces, captures)
    assert joined[0]["evidence_by_record"]["old:record"][0]["block"] == "old:block"
    assert joined[1]["evidence_by_record"]["new:record"][0]["block"] == "new:block"
    captures["new:capture"] = old
    with pytest.raises(ValueError, match="capture"):
        subject.join_witnesses(query, traces, captures)


def test_measurement_checks_exact_receipt_binding_and_repeat(subject):
    receipt = subject.canonical({"ledger_head": "sha256:toy-head"})
    binding = b"synthetic frozen binding"

    def check(*args):
        return subject.check_measurement(
            *args, frozen_binding_sha256=subject.digest(binding)
        )

    query = {
        "inputs": {
            "ledger_head": "sha256:toy-head",
            "replay_receipt_sha256": subject.digest(receipt),
            "query_binding_sha256": subject.digest(binding),
        },
        "forbidden_attempts": {"source_read": 0},
        "queries": [],
    }
    raw = subject.canonical(query)
    trace = b'{"records":[]}'
    check(receipt, binding, raw, trace, raw, trace)
    for name in query["inputs"]:
        bad = deepcopy(query)
        bad["inputs"][name] = "sha256:wrong"
        changed = subject.canonical(bad)
        with pytest.raises(ValueError, match="measurement"):
            check(receipt, binding, changed, trace, changed, trace)
    bad = deepcopy(query)
    bad["forbidden_attempts"]["source_read"] = 1
    changed = subject.canonical(bad)
    with pytest.raises(ValueError, match="measurement"):
        check(receipt, binding, changed, trace, changed, trace)
    with pytest.raises(ValueError, match="repeat"):
        check(receipt, binding, raw, trace, raw + b" ", trace)
    with pytest.raises(ValueError, match="repeat"):
        check(receipt, binding, raw, trace, raw, trace + b" ")


def test_query_change_report_does_not_confuse_new_head_with_new_answers(subject):
    before = {
        "inputs": {"ledger_head": "old"},
        "queries": [
            {"question_id": "same", "rows": [{"value": 1}]},
            {"question_id": "changed", "rows": [{"value": 2}]},
        ],
    }
    after = deepcopy(before)
    after["inputs"]["ledger_head"] = "new"
    assert subject.query_changes(before, after) == {
        "changed": [],
        "unchanged": ["same", "changed"],
    }
    after["queries"][1]["rows"][0]["value"] = 3
    assert subject.query_changes(before, after) == {
        "changed": ["changed"],
        "unchanged": ["same"],
    }
    after["queries"].pop()
    with pytest.raises(ValueError, match="question"):
        subject.query_changes(before, after)


def test_measurement_task_declares_continued_assessor_exposure(subject):
    task = subject.measurement_task()
    assert "continuing" in task
    assert "source reviewer" in task
    assert "not blind" in task
    assert "every returned witness" in task
    assert "all thirty questions" in task
    assert "Fresh source-grounded" not in task
    assert "no prior exposure" not in task


def test_measurement_packet_refuses_unaccepted_run_before_writing(subject, tmp_path):
    accepted = tmp_path / "refused"
    accepted.mkdir()
    (accepted / "result.json").write_bytes(subject.canonical({"status": "REFUSED"}))
    packet = tmp_path / "measurement"
    with pytest.raises(ValueError, match="accepted"):
        subject.prepare_measurement(tmp_path, accepted, packet)
    assert not packet.exists()


def test_measurement_refuses_rebound_queries_even_when_each_other_digest_matches(
    subject,
):
    receipt = subject.canonical({"ledger_head": "sha256:toy-head"})
    binding = b"changed binding"
    query = subject.canonical(
        {
            "inputs": {
                "ledger_head": "sha256:toy-head",
                "replay_receipt_sha256": subject.digest(receipt),
                "query_binding_sha256": subject.digest(binding),
            },
            "forbidden_attempts": {"source_read": 0},
            "queries": [],
        }
    )
    with pytest.raises(ValueError, match="frozen binding"):
        subject.check_measurement(
            receipt,
            binding,
            query,
            b"{}",
            query,
            b"{}",
            frozen_binding_sha256=subject.digest(b"original binding"),
        )


def test_one_partial_source_record_blocks_the_actual_whole_batch(subject):
    run = ROOT / "private/paper-v4-relationship-repair-01"
    packet = run / "source-review-01"
    review = json.loads((packet / "output/review.json").read_bytes())
    candidate = json.loads((run / "attempts/attempt-01/population.json").read_bytes())
    blocks = {
        b["id"]
        for p in json.loads(
            (run / "producer/inputs/selected-reading.json").read_bytes()
        )["pages"]
        for b in p["blocks"]
    }
    args = (
        candidate,
        review["bindings"],
        "01a0a2b8-61d5-73d0-9d54-e8841b661970",
        "01a0a2ce-0554-7201-a892-7909fc45ae63",
        blocks,
    )
    with pytest.raises(ValueError, match="affirmative source review"):
        subject.check_review(review, *args)
    changed = deepcopy(review)
    changed["status"] = "ALLOW_SUPPORTED_BATCH"
    with pytest.raises(ValueError, match="whole proposed batch"):
        subject.check_review(changed, *args)


def test_accepted_amendment_preserves_old_records_and_reports_partial_reconciliation(
    subject,
):
    run = ROOT / "private/paper-v4-relationship-repair-01"
    base = PAIR / "b/attempts/attempt-03"
    candidate = json.loads((run / "accepted/candidate.json").read_bytes())
    before = json.loads((base / "public/export-records.json").read_bytes())
    after = json.loads((run / "accepted/export-records.json").read_bytes())
    subject.check_preservation(before, after, candidate)
    indexed_before = subject.preservation().indexed(before)
    indexed_after = subject.preservation().indexed(after)
    for key in (
        "population:all-earthquakes",
        "obs:located-earthquake-count",
        "obs:quality-criteria-share",
    ):
        assert indexed_after[key] == indexed_before[key]
    assert len(indexed_after) == len(indexed_before) + 3
    assert len(candidate["supersessions"]) == 6
    ledger = (run / "accepted/ledger/history.jsonl").read_bytes()
    assert ledger.startswith((base / "ledger/history.jsonl").read_bytes())
    assert ledger.startswith((run / "schema/history.jsonl").read_bytes())
    review = json.loads((run / "source-review-02/output/review.json").read_bytes())
    assert review["status"] == "ALLOW_SUPPORTED_BATCH"
    assert all(row["verdict"] == "SUPPORTED" for row in review["records"])
    assert (
        next(row for row in review["problems"] if row["id"] == "uncertainty")["status"]
        == "PARTIAL"
    )
    assert review["ratification"] == "PENDING_HUMAN"


def test_public_role_inspection_is_qualified_and_separate_from_frozen_queries(subject):
    run = ROOT / "private/paper-v4-relationship-repair-01"
    inspected = json.loads(
        (run / "accepted/representation-inspection.json").read_bytes()
    )
    hypothesis, trigger, upstream = (
        inspected[key] for key in ("hypothesis", "trigger", "upstream_process")
    )
    assert hypothesis["proposed_trigger"] == trigger["id"]
    assert trigger["caused_by"] == upstream["id"]
    assert all(
        row["assertion_modality"] == "HYPOTHESISED"
        for row in (hypothesis, trigger, upstream)
    )
    assert len(inspected["supports"]) == 2
    assert {row["target_id"] for row in inspected["supports"]} == {hypothesis["id"]}
    binding = (PAIR / "b/attempts/attempt-03/query-binding.json").read_bytes()
    assert b"proposed_trigger" not in binding
    query = (run / "accepted/query/query-result.json").read_bytes()
    assert b"proposed_trigger" not in query
    assert b"PORE_PRESSURE_INCREASE" in query
    assert "Separate representation inspection" in inspected["measurement_limit"]


def test_actual_query_repeats_and_measurement_materials_remain_frozen(subject):
    run = ROOT / "private/paper-v4-relationship-repair-01"
    base = PAIR / "b/attempts/attempt-03"
    accepted = run / "accepted"
    baseline = json.loads((run / "baseline.json").read_bytes())
    checked = subject.check_measurement(
        (accepted / "replay-receipt.json").read_bytes(),
        (base / "query-binding.json").read_bytes(),
        (accepted / "query/query-result.json").read_bytes(),
        (accepted / "query/trace-summary.json").read_bytes(),
        (accepted / "query-repeat/query-result.json").read_bytes(),
        (accepted / "query-repeat/trace-summary.json").read_bytes(),
        frozen_binding_sha256=baseline["identities"]["query_binding_sha256"],
    )
    assert len(checked["queries"]) == 30
    packet = run / "measurement"
    helper = subject.module(HERE / "relationship_review.py", "repair_review_fixture")
    manifest = json.loads((packet / "review-input-manifest.json").read_bytes())
    materials = helper.materials(manifest)
    assert materials["retained_capture"] != materials["amendment_capture"]
    assert len(materials["witness_inputs"].splitlines()) == 285
    assert manifest["witnesses_traced"] == 285
    assert len(json.loads(materials["population_trace"])["records"]) == 291


def comparison_fixture():
    def witness(key, value):
        return {
            "witness_key": key,
            "projected_variants": [{"value": value}],
            "evidence_by_record": {key: [{"block": "b1"}]},
            "occurrences": [],
        }

    def record(support, credits):
        return {
            "witnesses": [
                {"witness_key": key, "source_support": value}
                for key, value in support.items()
            ],
            "questions": [
                {
                    "question_id": "q1",
                    "question_responsiveness": "PARTIAL",
                    "rows": [
                        {"row_index": index, "witness_key": key}
                        for index, key in enumerate(support)
                    ],
                    "coverage": [
                        {"semantic": key, "row_index": index}
                        for key, index in credits.items()
                    ],
                }
            ],
        }

    before = [witness("old", 1), witness("same", 2)]
    after = [witness("same", 2), witness("new", 3)]
    after[0]["occurrences"] = [{"question_id": "q1", "row_index": 0}]
    old_review = record(
        {"old": "PARTIAL", "same": "SUPPORTED"},
        {"gain": None, "loss": 1},
    )
    new_review = record(
        {"same": "PARTIAL", "new": "SUPPORTED"},
        {"gain": 1, "loss": None},
    )
    return before, after, old_review, new_review


def test_comparison_separates_new_information_from_old_witness_reassessment(subject):
    compared = subject.assessment_changes(*comparison_fixture())
    assert compared["witness_content"] == {
        "unchanged": ["same"],
        "changed": [],
        "added": ["new"],
        "removed": ["old"],
    }
    assert compared["unchanged_witness_support_changes"] == [
        {"witness_key": "same", "before": "SUPPORTED", "after": "PARTIAL"}
    ]
    question = compared["questions"][0]
    assert question["before_credited"] == question["after_credited"] == 1
    assert question["credit_changes"] == [
        {
            "semantic": "gain",
            "direction": "GAIN",
            "witness_key": "new",
            "witness_content": "ADDED_OR_CHANGED",
        },
        {
            "semantic": "loss",
            "direction": "LOSS",
            "witness_key": "same",
            "witness_content": "UNCHANGED",
        },
    ]


@pytest.mark.parametrize("part", ["projected_variants", "evidence_by_record"])
def test_changed_witness_or_evidence_is_not_called_unchanged(subject, part):
    before, after, old_review, new_review = comparison_fixture()
    after[0][part] = [] if part == "projected_variants" else {}
    compared = subject.assessment_changes(before, after, old_review, new_review)
    assert compared["witness_content"]["unchanged"] == []
    assert compared["witness_content"]["changed"] == ["same"]
    assert compared["unchanged_witness_support_changes"] == []


@pytest.mark.parametrize("failure", ["duplicate", "missing", "semantic_drift"])
def test_comparison_refuses_missing_or_different_review_units(subject, failure):
    before, after, old_review, new_review = comparison_fixture()
    if failure == "duplicate":
        after.append(deepcopy(after[0]))
    elif failure == "missing":
        del after[0]["evidence_by_record"]
    else:
        new_review["questions"][0]["coverage"][0]["semantic"] = "different"
    with pytest.raises((ValueError, KeyError)):
        subject.assessment_changes(before, after, old_review, new_review)


def test_every_checklist_surface_declaration_must_match_its_manifest(subject):
    manifest = {"evidence_surface": {"kind": "SELECTED_READING_TEXT_LAYER"}}
    correct = "the declared `SELECTED_READING_TEXT_LAYER` surface"
    wrong = "the declared `STRUCTURED_ROWS` surface"
    subject.check_companion_surface(correct + "\n" + correct, manifest)
    for text in (wrong + "\n" + wrong, correct + "\n" + wrong, "no declaration"):
        with pytest.raises(ValueError, match="checklist surface"):
            subject.check_companion_surface(text, manifest)


@pytest.fixture(scope="module")
def completed_measurement(subject):
    helper = subject.module(HERE / "relationship_review.py", "repair_final_review")
    validator = subject.module(
        ROOT / "paper-v4/evaluation-v4/review.py", "repair_final_validator"
    )
    packets = {
        "before": PAIR / "b/attempts/attempt-03/review",
        "after": ROOT / "private/paper-v4-relationship-repair-01/measurement",
    }
    result = {}
    for stage, packet in packets.items():
        manifest = json.loads((packet / "review-input-manifest.json").read_bytes())
        supplied = helper.materials(manifest)
        source = (packet / "output/review-record.preliminary.md").read_bytes()
        result[stage] = {
            "packet": packet,
            "manifest": manifest,
            "source": source,
            "validated": helper.validate(packet),
            "review": validator._markdown_record(source),
            "inputs": [
                json.loads(line) for line in supplied["witness_inputs"].splitlines()
            ],
            "questions": json.loads(supplied["competency_questions"])["questions"],
        }
    return result


def test_final_measurement_validates_complete_reviews_and_exact_totals(
    subject, completed_measurement
):
    comparison = json.loads(
        (completed_measurement["after"]["packet"] / "comparison.json").read_bytes()
    )
    for stage, expected in (
        ("before", (282, {"COVERED": 15, "PARTIAL": 8, "NONE": 2}, 78)),
        ("after", (285, {"COVERED": 17, "PARTIAL": 8}, 90)),
    ):
        data = completed_measurement[stage]
        review = data["review"]
        assert data["validated"]["status"] == "PRELIMINARY_COMPLETE"
        assert data["validated"]["witnesses"] == expected[0]
        assert data["validated"]["questions"] == 30
        assert review["ratification"]["disposition"] == "PENDING"
        ids = {q["id"] for q in data["questions"] if q["tier"] != "C"}
        positives = [q for q in review["questions"] if q["question_id"] in ids]
        labels = Counter(q["question_responsiveness"] for q in positives)
        credited = sum(
            c["row_index"] is not None for q in positives for c in q["coverage"]
        )
        assert labels == expected[1]
        assert credited == expected[2]
        assert comparison[stage] == {
            "review_sha256": subject.digest(data["source"]),
            "positive_questions": len(positives),
            "required_semantics": sum(len(q["coverage"]) for q in positives),
            "credited_semantics": credited,
            "labels": {
                label: labels[label] for label in ("COVERED", "PARTIAL", "NONE")
            },
            "witness_support": dict(
                Counter(w["source_support"] for w in review["witnesses"])
            ),
        }
        assert len(positives) == 25
        assert comparison[stage]["required_semantics"] == 102
    after = completed_measurement["after"]
    validation = json.loads((after["packet"] / "validation.json").read_bytes())
    for key, value in after["validated"].items():
        assert validation[key] == value
    assert (
        validation["review_sha256"]
        == ("sha256:bba31ff9475efe52aff5d8f9806ba6ca3acd8bc7637b44d2a265006372b2f553")
        == subject.digest(after["source"])
    )
    assert validation["ratification"] == "PENDING_HUMAN"
    assert comparison["controls"]["recorded_findings"] == validation["control_findings"]
    assert comparison["controls"]["count"] == 5
    assert comparison["controls"]["excluded_from_positive_totals"] is True
    assert comparison["controls"]["defective_not_comparative"] == ["CQ-C-03"]


def test_final_comparison_does_not_count_reassessment_as_changed_information(
    subject, completed_measurement
):
    before, after = (completed_measurement[s] for s in ("before", "after"))
    recorded = json.loads((after["packet"] / "comparison.json").read_bytes())
    recomputed = subject.assessment_changes(
        before["inputs"], after["inputs"], before["review"], after["review"]
    )
    assert recomputed == {key: recorded[key] for key in recomputed}
    assert {key: len(rows) for key, rows in recomputed["witness_content"].items()} == {
        "unchanged": 276,
        "changed": 0,
        "added": 9,
        "removed": 6,
    }
    support_changes = Counter(
        (row["before"], row["after"])
        for row in recomputed["unchanged_witness_support_changes"]
    )
    assert support_changes == {
        ("PARTIAL", "SUPPORTED"): 111,
        ("SUPPORTED", "PARTIAL"): 1,
    }
    credit_changes = [c for q in recomputed["questions"] for c in q["credit_changes"]]
    partition = Counter((c["direction"], c["witness_content"]) for c in credit_changes)
    assert partition == {
        ("GAIN", "ADDED_OR_CHANGED"): 6,
        ("GAIN", "UNCHANGED"): 7,
        ("LOSS", "UNCHANGED"): 1,
    }
    assert recorded["credit_change_partition"] == [
        {"direction": direction, "witness_content": content, "elements": count}
        for (direction, content), count in sorted(partition.items())
    ]
    amended_gains = Counter(
        c["witness_key"]
        for c in credit_changes
        if c["direction"] == "GAIN" and c["witness_content"] == "ADDED_OR_CHANGED"
    )
    assert amended_gains == {
        "obs:final-catalog-horizontal-uncertainty:repair-02": 5,
        "relation:rc1-bounded-by-detachment:repair-02": 1,
    }
    losses = [c for c in credit_changes if c["direction"] == "LOSS"]
    assert losses[0]["witness_key"] == "method:double-difference"
    assert losses[0]["witness_content"] == "UNCHANGED"


def test_companion_returns_preserve_all_semantic_judgments(
    subject, completed_measurement
):
    data = completed_measurement["after"]
    output = data["packet"] / "output"
    checklist = (output / "checklist.md").read_text()
    subject.check_companion_surface(checklist, data["manifest"])
    for previous in ("returned-01", "returned-02"):
        for name in (
            "review-record.preliminary.md",
            "findings.md",
            "assemble_review.py",
        ):
            assert (output / previous / name).read_bytes() == (
                output / name
            ).read_bytes()
        prior_checklist = (output / previous / "checklist.md").read_text()
        with pytest.raises(ValueError, match="checklist surface"):
            subject.check_companion_surface(prior_checklist, data["manifest"])
        assert (
            prior_checklist.replace(
                "declared `STRUCTURED_ROWS` surface",
                "declared `SELECTED_READING_TEXT_LAYER` surface",
            )
            == checklist
        )


def test_uncertainty_value_and_categories_already_occur_in_unchanged_returned_prose(
    completed_measurement,
):
    key = "claim:block:page-3-block-004"
    content = []
    for stage, row_index in (("before", 65), ("after", 66)):
        data = completed_measurement[stage]
        witness = next(w for w in data["inputs"] if w["witness_key"] == key)
        review = next(w for w in data["review"]["witnesses"] if w["witness_key"] == key)
        assert review["source_support"] == "SUPPORTED"
        for qid in ("CQ-T3-04", "CQ-T5-04"):
            question = next(
                q for q in data["review"]["questions"] if q["question_id"] == qid
            )
            assert question["rows"][row_index]["witness_key"] == key
        statement = witness["projected_variants"][0]["record"]["statement"]
        assert "2.1 km" in statement
        assert all(f"Quality {label}:" in statement for label in "ABCD")
        content.append((witness["projected_variants"], witness["evidence_by_record"]))
    assert content[0] == content[1]
    report = (HERE / "RELATIONSHIP-REPAIR-RESULTS.md").read_text()
    assert "not first availability of the number" in report
    assert "not evidence of six previously unavailable elements" in report


def test_frozen_positive_regrades_follow_text_matching_not_a_category_check(
    subject,
    completed_measurement,
):
    packet = completed_measurement["after"]["packet"]
    script_path = packet / "output/assemble_review.py"
    source = script_path.read_bytes()
    tree = ast.parse(source)
    function = next(
        n
        for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "support_for"
    )
    # Execute only the retained function, never the module's output-writing code.
    scope = {
        "partial": {},
        "variant_payload": lambda item: ({}, item["record"]),
        "ordered_locators": lambda item: ["synthetic:block"],
        "blocks": {"synthetic:block": "The project received funding."},
    }
    exec(
        compile(ast.Module(body=[function], type_ignores=[]), str(script_path), "exec"),
        scope,
    )
    ontology = yaml.safe_load(
        (PAIR / "b/producer/work/ontology-attempt-02.yaml").read_bytes()
    )
    kinds = ontology["enums"]["EarthScienceClaimKind"]["permissible_values"]
    assert all(value is None for value in kinds.values())
    for kind in ("FUNDING", "OBSERVATIONAL_RESULT", "METHOD_JUSTIFICATION"):
        assert kind in kinds
        item = {
            "witness_key": "claim:block:synthetic",
            "record": {
                "statement": scope["blocks"]["synthetic:block"],
                "claim_kind": kind,
                "assertion_modality": "STATED",
            },
        }
        assert scope["support_for"](item)[0] == "SUPPORTED"
    comparison = json.loads((packet / "comparison.json").read_bytes())
    positives = [
        r
        for r in comparison["unchanged_witness_support_changes"]
        if r["after"] == "SUPPORTED"
    ]
    assert len(positives) == 111
    assert all(r["witness_key"].startswith("claim:block:") for r in positives)
    partial = next(
        n.value
        for n in tree.body
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "partial" for t in n.targets)
    )
    scope["partial"] = ast.literal_eval(partial)
    reading = json.loads(
        (ROOT / "private/paper-v4-text-layer/selected-reading.json").read_bytes()
    )
    scope["blocks"] = {
        b["id"]: b["text"] for p in reading["pages"] for b in p["blocks"]
    }
    support = {
        w["witness_key"]: w
        for w in completed_measurement["after"]["review"]["witnesses"]
    }
    inputs = {w["witness_key"]: w for w in completed_measurement["after"]["inputs"]}
    scope["variant_payload"] = lambda item: (
        item["projected_variants"][0],
        item["projected_variants"][0]["record"],
    )
    scope["ordered_locators"] = lambda item: support[item["witness_key"]][
        "source_locators"
    ]
    for change in positives:
        key = change["witness_key"]
        assert key not in scope["partial"]
        assert scope["support_for"](inputs[key])[0] == "SUPPORTED"
    assert script_path.read_bytes() == source


def test_crustal_reference_context_is_projected_not_only_in_retained_evidence(
    completed_measurement,
):
    keys = ("claim:block:page-7-block-011", "claim:block:page-9-block-036")
    content = []
    for stage, label in (("before", "PARTIAL"), ("after", "SUPPORTED")):
        data = completed_measurement[stage]
        inputs = {w["witness_key"]: w for w in data["inputs"]}
        judgments = {w["witness_key"]: w for w in data["review"]["witnesses"]}
        question = next(
            q for q in data["review"]["questions"] if q["question_id"] == "CQ-T2-04"
        )
        returned = {r["witness_key"] for r in question["rows"]}
        statements = []
        for key in keys:
            assert key in returned
            assert judgments[key]["source_support"] == label
            statements.append(
                inputs[key]["projected_variants"][0]["record"]["statement"]
            )
        assert "5.4" in statements[0] and "thick32" in statements[0]
        assert statements[1].startswith("32. Wang")
        content.append(statements)
    assert content[0] == content[1]


def test_evidence_units_differ_from_meaning_units_on_the_frozen_public_path():
    """Synthetic compilation only. Never prepare or admit these toy records."""
    program = r"""
from copy import deepcopy
import json
import malleus.compiler as api
from relationship_repair import RUN, canonical, digest

path = RUN / "accepted/ledger/history.jsonl"
old = path.read_bytes()
replay = api.KnowledgeChangeHistory.reopen(path).replay()
base = api.PopulationBaseState.from_replay(replay)
a = "The sensor remained stable."
metadata = "The report is named Alpha."
b = "That stability applies only during the observation interval."
reading = canonical({"pages": [{"page": 1, "blocks": [
    {"id": "toy:block-a", "ordinal": 0, "text": a + " " + metadata},
    {"id": "toy:block-b", "ordinal": 1, "text": b}]}]})
claim = {"id": "toy:claim", "type": "EarthScienceClaim", "properties": {
    "statement": "Sensor stability is reported only for the observation interval.",
    "claim_kind": "OBSERVATIONAL_RESULT", "assertion_modality": "STATED",
    "assertion_locator": "toy:observation", "statement_sha256": digest(a.encode("utf-8"))}}
report = {"id": "toy:report", "type": "ResearchArticle", "properties": {"name": "Alpha"}}
records = {family: [] for family in replay.graph.export_records()}
records["entities"] = [claim, report]
def targets(record):
    return [{"record_id": record["id"], "path": ["properties", key]}
            for key in record["properties"]]
capture = {"schema": api.DOCUMENT_CAPTURE_GRAMMAR, "reading_sha256": digest(reading),
    "attribution": {"source_id": "toy:source", "author": "Synthetic test", "date": "2026-01-01"},
    "nothing_assertable": [], "assertions": [
        {"id": "toy:observation", "block": "toy:block-a", "statement": a,
         "modality": "STATED", "gaps": [], "formalized_by": targets(claim)},
        {"id": "toy:metadata", "block": "toy:block-a", "statement": metadata,
         "modality": "STATED", "gaps": [], "formalized_by": targets(report)},
        {"id": "toy:qualification", "block": "toy:block-b", "statement": b,
         "modality": "STATED", "gaps": [], "formalized_by": [
             {"record_id": claim["id"], "path": ["properties", "statement"]}]}]}
capture_bytes = canonical(capture)
def adapt(candidate):
    return api.adapt_document_assertions(reading_bytes=reading,
        capture_bytes=canonical(candidate), capture_id="toy:capture", plan_id="toy:plan",
        contract_identity=replay.partial_contract.identity, records=records,
        supersessions=[], contract_view=replay.contract_view)
def compile_plan(plan):
    return api.compile_population_plan(plan, partial_contract=replay.partial_contract,
        contract_view=replay.contract_view, base_state=base,
        history_profile=api.SOURCE_ASSERTION_PROFILE)
adapted = adapt(capture)
plan = json.loads(adapted.canonical_plan_bytes)
assert compile_plan(plan).status is api.PopulationPlanStatus.CHANGE_SET
assert adapted.capture_bytes == capture_bytes
assert adapted.reading_identity == digest(reading)
assert plan["records"] == records
assert [d["locator"] for d in plan["derivations"]
        if d["record_id"] == "toy:claim" and d["path"] == ["properties", "statement"]] == [
            "toy:observation", "toy:qualification"]
assert any(d["record_id"] == "toy:report" and d["locator"] == "toy:metadata"
           for d in plan["derivations"])
assert claim["properties"]["statement"] not in (a, b)

# A coherent graph statement may synthesize context. A source excerpt cannot
# pretend that two separately located passages are one verbatim block.
joined = deepcopy(capture)
joined["assertions"][0]["statement"] = a + " " + b
try:
    adapt(joined)
except api.DocumentAssertionRefusal as error:
    assert "NOT_VERBATIM" in str(error)
else:
    raise AssertionError("a false single-block quotation passed")

# These are compiler-boundary probes, not proposed article amendments.
old_id = "claim:block:page-9-block-036"
same_type = deepcopy(plan)
same_type["supersessions"] = [{"record_id": "toy:claim", "supersedes_record_id": old_id}]
assert compile_plan(same_type).status is api.PopulationPlanStatus.CHANGE_SET
cross_type = deepcopy(plan)
cross_type["supersessions"] = [{"record_id": "toy:report", "supersedes_record_id": old_id}]
fork = deepcopy(same_type)
second = deepcopy(claim)
second["id"] = "toy:second-claim"
fork["records"]["entities"].append(second)
fork["derivations"].extend({**d, "record_id": second["id"]}
    for d in plan["derivations"] if d["record_id"] == claim["id"])
fork["supersessions"].append({"record_id": second["id"], "supersedes_record_id": old_id})
for candidate, reason in ((cross_type, api.PopulationPlanRefusalReason.SUPERSESSION_TYPE_MISMATCH),
                          (fork, api.PopulationPlanRefusalReason.SUPERSESSION_FORK)):
    try:
        compile_plan(candidate)
    except api.PopulationPlanRefusal as error:
        assert error.reason is reason, str(error)
    else:
        raise AssertionError(f"missing refusal: {reason}")
assert path.read_bytes() == old
print(json.dumps({"compiled_only": True, "accepted_history_unchanged": True}))
"""
    result = subprocess.run(
        [sys.executable, "-c", program],
        env={
            **os.environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": os.pathsep.join((str(PAIR / "core/src"), str(HERE))),
        },
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "compiled_only": True,
        "accepted_history_unchanged": True,
    }


def test_category_description_is_retained_but_not_a_structural_meaning_check():
    """A synthetic annotation change is compiled in memory, never accepted."""
    program = r"""
import json
import yaml
import malleus.compiler as api
from relationship_repair import HERE, PAIR, RUN, module
helper = module(HERE / "run-26/compile_ontology_candidate.py", "unit_probe_compiler")
helper.MANIFEST = PAIR / "b/producer-input-manifest.json"
path = RUN / "producer/inputs/ontology.yaml"
source = path.read_bytes()
imports = helper._declared_sources(PAIR / "b/producer")
def compile_source(value):
    return api.compile_linkml_contract(root_locator="paper-v4-project",
        sources={"paper-v4-project": value, **imports}).artifact
before = compile_source(source)
document = yaml.safe_load(source)
values = document["enums"]["EarthScienceClaimKind"]["permissible_values"]
assert values["BACKGROUND"] is None
values["BACKGROUND"] = {"description": "Synthetic description for a compiler-boundary test."}
after = compile_source(yaml.safe_dump(document, sort_keys=False).encode())
assert before.canonical_facts == after.canonical_facts
assert before.validated_fact_set_sha256 == after.validated_fact_set_sha256
assert before.evidence_sha256 != after.evidence_sha256
assert before.artifact_bytes != after.artifact_bytes
assert path.read_bytes() == source
print(json.dumps({"structural_facts_unchanged": True, "source_evidence_changed": True}))
"""
    result = subprocess.run(
        [sys.executable, "-c", program],
        env={
            **os.environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": os.pathsep.join((str(PAIR / "core/src"), str(HERE))),
        },
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "structural_facts_unchanged": True,
        "source_evidence_changed": True,
    }


def test_thickness_origin_and_schematic_application_are_separate_source_contexts():
    """Freeze the observed gap, not a replacement fact or new semantic grade."""
    run = ROOT / "private/paper-v4-relationship-repair-01"
    reading = json.loads((run / "producer/inputs/selected-reading.json").read_bytes())
    blocks = {
        b["id"]: " ".join(unicodedata.normalize("NFKC", b["text"]).split())
        for p in reading["pages"]
        for b in p["blocks"]
    }
    body = blocks["page:2:block:006"]
    caption = blocks["page:7:block:011"]
    assert "8-Ma-old" in body and "western ridge flank" in body
    assert "5.4 ± 0.3 km" in body
    assert "beneath the segment RC2" in caption and "~5.4 ± 0.3 km" in caption
    records = json.loads((run / "accepted/export-records.json").read_bytes())
    indexed = {r["id"]: r for rows in records.values() for r in rows}
    # A block ID does not imply a corresponding copied-block graph record.
    assert "claim:block:page-2-block-006" not in indexed
    observed = indexed["obs:rc2-crust-thickness"]["properties"]
    assert observed["value_lower"] == observed["value_upper"] == 5.4
    assert observed["uncertainty"] == 0.3 and observed["unit"] == "km"
    assert "observation_context" not in observed
    assert "value_qualification" not in observed
    assert indexed[observed["subject"]]["properties"] == {"name": "crust"}
    capture = json.loads((run / "producer/inputs/base-capture.json").read_bytes())
    evidence = next(
        a for a in capture["assertions"] if a["id"] == observed["assertion_locator"]
    )
    assert evidence["block"] == "page:2:block:006"
    assert "8-Ma-old" in evidence["statement"]
    assert {
        "record_id": "obs:rc2-crust-thickness",
        "path": ["properties", "value_lower"],
    } in evidence["formalized_by"]


@pytest.mark.parametrize(
    "record_id,version",
    [
        (
            "claim:block:page-1-block-006",
            "sha256:4d1d22cc0d3bc92130f642482e254e756ebbd52fa2a848d0f48daa071d93fc99",
        ),
        (
            "source:yu-2025-mid-atlantic-ridge",
            "sha256:9a121e650626134f67936e91f5fe15eab920ff7829083b7e7f5f7e884a67370c",
        ),
        (
            "claim:block:page-9-block-036",
            "sha256:94990afd3822a96de8baa65976c83e8d355c7ddee34e5037753de0366be5d9d9",
        ),
    ],
)
def test_proposed_contextual_review_binds_exact_existing_versions(
    subject, record_id, version
):
    """Reference versions for a proposal, not evidence of a completed review."""
    records = json.loads((subject.RUN / "accepted/export-records.json").read_bytes())
    indexed = {r["id"]: r for rows in records.values() for r in rows}
    assert subject.digest(subject.canonical(indexed[record_id])) == version
    report = (HERE / "RELATIONSHIP-REPAIR-RESULTS.md").read_text()
    row = next(
        line for line in report.splitlines() if line.startswith(f"| `{record_id}` |")
    )
    assert version.removeprefix("sha256:") in row


def test_mixed_metadata_is_already_in_returned_graph_prose(
    subject, completed_measurement
):
    """Removing it is not lossless merely because the original source survives."""
    reading = json.loads(
        (subject.RUN / "producer/inputs/selected-reading.json").read_bytes()
    )
    blocks = {b["id"]: b["text"] for p in reading["pages"] for b in p["blocks"]}
    key = "claim:block:page-1-block-006"
    witness = next(
        w for w in completed_measurement["after"]["inputs"] if w["witness_key"] == key
    )
    record = witness["projected_variants"][0]["record"]
    statement = record["statement"]
    assert statement == blocks["page:1:block:006"].strip()
    assert "Received: 23 February 2023" in statement
    assert "Accepted: 30 December 2024" in statement
    assert "e-mail:" in statement
    assert "subject" not in record
    assert "RTI segment (named RC1)" in blocks["page:1:block:005"]
    assert "exhumed mantle" in blocks["page:2:block:001"]
    assert "exhumed mantle" not in statement
    capture = json.loads(
        (subject.RUN / "producer/inputs/base-capture.json").read_bytes()
    )
    assertion = next(a for a in capture["assertions"] if a["id"] == "assertion:060")
    assert assertion["block"] == "page:1:block:006"
    assert assertion["statement"] == statement
    assert record["statement_sha256"] == subject.digest(statement.encode("utf-8"))
    assert {"record_id": key, "path": ["properties", "statement"]} in assertion[
        "formalized_by"
    ]
    records = json.loads((subject.RUN / "accepted/export-records.json").read_bytes())
    article = next(
        r for r in records["entities"] if r["id"] == "source:yu-2025-mid-atlantic-ridge"
    )
    assert article["properties"]["publication_year"] == 2025
    surface = json.loads(
        (subject.RUN / "producer/inputs/population-surface.json").read_bytes()
    )
    article_type = next(
        t for t in surface["record_types"] if t["name"] == "ResearchArticle"
    )
    assert not {"publication_received_date", "publication_accepted_date"} & {
        s["name"] for s in article_type["slots"]
    }


def test_bibliography_review_starts_from_a_claim_not_a_publication(subject):
    """A source-local label and a printed title are not typed scientific support."""
    records = json.loads((subject.RUN / "accepted/export-records.json").read_bytes())
    indexed = {r["id"]: r for rows in records.values() for r in rows}
    key = "claim:block:page-9-block-036"
    record = indexed[key]
    assert record["type"] == "EarthScienceClaim"
    assert record["properties"]["claim_kind"] == "BACKGROUND"
    assert "subject" not in record["properties"]
    capture = json.loads(
        (subject.RUN / "producer/inputs/base-capture.json").read_bytes()
    )
    assertion = next(a for a in capture["assertions"] if a["id"] == "assertion:126")
    assert assertion["block"] == "page:9:block:036"
    assert assertion["statement"] == record["properties"]["statement"]
    assert assertion["statement"].startswith("32. Wang")
    assert "13, 7809 (2022)" in assertion["statement"]
    assert {"record_id": key, "path": ["properties", "statement"]} in assertion[
        "formalized_by"
    ]
    title_fragment = "uniform crustal"
    assert title_fragment in assertion["statement"]
    assert not any(
        title_fragment in r["properties"]["name"]
        for r in records["entities"]
        if r["type"] == "ResearchArticle" and "name" in r["properties"]
    )
    assert all(
        key not in (r["source_id"], r["target_id"]) for r in records["relations"]
    )


def test_exact_delta_preservation_does_not_certify_replaced_meaning(subject):
    """Synthetic characterization of the existing guard, not a semantic repair."""
    evidence = b"The sensor is stable. The report was accepted on 2 May 2020."
    evidence_before = evidence
    before = {family: [] for family in subject.FAMILIES}
    before["entities"] = [
        {
            "id": "toy:mixed",
            "type": "Claim",
            "properties": {"statement": evidence.decode()},
        },
        {"id": "toy:control", "type": "Thing", "properties": {"name": "keep"}},
    ]
    old = deepcopy(before)
    candidate = {
        "records": {family: [] for family in subject.FAMILIES},
        "supersessions": [
            {"record_id": "toy:science", "supersedes_record_id": "toy:mixed"}
        ],
    }
    candidate["records"]["entities"] = [
        {
            "id": "toy:science",
            "type": "Claim",
            "properties": {"statement": "The sensor is stable."},
        }
    ]
    after = subject.project(before, candidate)
    subject.check_preservation(before, after, candidate)
    assert before == old and evidence == evidence_before
    assert "2 May 2020" not in json.dumps(after)
    assert b"2 May 2020" in evidence
    damaged = deepcopy(after)
    damaged["entities"][0]["properties"]["name"] = "lost"
    with pytest.raises(ValueError, match="preservation"):
        subject.check_preservation(before, damaged, candidate)
