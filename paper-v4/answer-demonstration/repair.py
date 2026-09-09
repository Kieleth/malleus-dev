"""Paper-owned bounded delta experiments. No source interpretation lives here."""

import argparse
from dataclasses import replace
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sys

import malleus.compiler as api

from capture import population_parts, verify_replay
from followup import checked_bytes, reference_module, verify_materials
import pilot
from review_packet import canonical, digest, new_private_directory


ROOT = pilot.ROOT
LOADED_EXECUTOR_BYTES = Path(__file__).read_bytes()
BASE = ROOT / "private/paper-v4-v4-run-21"
EXPERIMENT = ROOT / "paper-v4/experiment-v4/run-21"
FAMILIES = {"entities", "relations", "events", "signals", "event_participations"}
FINDINGS = {
    "funding": "Inspect rel:erc-funds-singh against page:10:block:044. The prior source-grounded review found an award identifier attributed to the wrong funder. Propose a source-faithful replacement or refuse. Preserve endpoints and legitimate properties. Do not change other records.",
    "evidence": "Inspect the source's argument for claim:hyp-co2-degassing, especially page:5:block:006. The graph captures quantities but no incoming SUPPORTS relationship. Decide whether the text justifies explicit source-attributed evidence links from existing records. Add only justified ResearchRelation records involving that hypothesis, or refuse. Preserve qualifications. An author's argument is not independent proof of truth. Do not invent measurements or require a link to satisfy an evaluator.",
}


def indexed(records):
    if set(records) != FAMILIES:
        raise ValueError("record families must be explicit and closed")
    result = {}
    for family, rows in records.items():
        for row in rows:
            if row["id"] in result:
                raise ValueError("duplicate record identity")
            result[row["id"]] = (family, row)
    return result


def executor_source(path, loaded_bytes):
    return checked_bytes(
        path.read_bytes(), digest(loaded_bytes), "loaded executor source"
    )


def check_scope(
    case,
    candidate,
    base,
    *,
    funding_id="rel:erc-funds-singh",
    hypothesis_id="claim:hyp-co2-degassing",
):
    population_parts(candidate)
    proposed, existing = indexed(candidate["records"]), indexed(base)
    if not proposed or set(proposed) & set(existing):
        raise ValueError("delta requires new identities, not reused base records")
    if any(family != "relations" for family, _ in proposed.values()):
        raise ValueError("this experiment permits relation deltas only")
    relations = candidate["records"]["relations"]
    if case == "funding":
        if len(relations) != 1:
            raise ValueError("funding permits one replacement")
        edge, old = relations[0], existing[funding_id][1]
        if candidate["supersessions"] != [
            {"record_id": edge["id"], "supersedes_record_id": funding_id}
        ]:
            raise ValueError("funding requires exact supersession")
        if any(edge[key] != old[key] for key in ("type", "source_id", "target_id")):
            raise ValueError("funding replacement must preserve type and endpoints")
    elif case == "evidence":
        if candidate["supersessions"]:
            raise ValueError("evidence case permits additions only")
        payloads = {
            canonical({key: value for key, value in row.items() if key != "id"})
            for row in base["relations"]
        }
        for edge in relations:
            endpoints = {edge["source_id"], edge["target_id"]}
            if edge["type"] != "ResearchRelation" or hypothesis_id not in endpoints:
                raise ValueError(
                    "evidence case requires a ResearchRelation involving the existing hypothesis"
                )
            if not endpoints <= {
                key for key, (family, _) in existing.items() if family == "entities"
            }:
                raise ValueError("evidence endpoints must already exist")
            payload = canonical(
                {key: value for key, value in edge.items() if key != "id"}
            )
            if payload in payloads:
                raise ValueError("duplicate relation payload despite distinct ID")
            payloads.add(payload)
    else:
        raise ValueError("unknown repair case")


def check_qualification(candidate, base, *, observation_id, relation_id):
    """Permit only an additive qualification and its atomic incident-edge version."""
    population_parts(candidate)
    proposed, existing = indexed(candidate["records"]), indexed(base)
    records = candidate["records"]
    if (
        len(proposed) != 2
        or len(records["entities"]) != 1
        or len(records["relations"]) != 1
        or set(proposed) & set(existing)
    ):
        raise ValueError("qualification requires exactly two fresh replacement records")
    observation, edge = records["entities"][0], records["relations"][0]
    old_observation, old_edge = existing[observation_id][1], existing[relation_id][1]
    incident = {
        row["id"]
        for row in base["relations"]
        if observation_id in {row["source_id"], row["target_id"]}
    }
    if (
        incident != {relation_id}
        or existing[observation_id][0] != "entities"
        or existing[relation_id][0] != "relations"
        or old_edge["source_id"] != observation_id
    ):
        raise ValueError("qualification dependency closure differs from declared pair")
    expected_supersessions = [
        {"record_id": observation["id"], "supersedes_record_id": observation_id},
        {"record_id": edge["id"], "supersedes_record_id": relation_id},
    ]
    if sorted(candidate["supersessions"], key=lambda s: s["record_id"]) != sorted(
        expected_supersessions, key=lambda s: s["record_id"]
    ):
        raise ValueError("qualification requires exact atomic pair supersession")
    old_properties, properties = (
        old_observation["properties"],
        observation["properties"],
    )
    additions = set(properties) - set(old_properties)
    if (
        not additions
        or not additions
        <= {"determination", "assertion_modality", "description", "duration"}
        or any(
            key not in properties or properties[key] != value
            for key, value in old_properties.items()
        )
        or {
            key: value
            for key, value in observation.items()
            if key not in {"id", "properties"}
        }
        != {
            key: value
            for key, value in old_observation.items()
            if key not in {"id", "properties"}
        }
    ):
        raise ValueError(
            "qualification must preserve all existing values and add only declared fields"
        )
    if edge != {**old_edge, "id": edge["id"], "source_id": observation["id"]}:
        raise ValueError(
            "qualification relation must preserve all content except its versioned source"
        )


def check_preservation(before, after, candidate):
    expected = indexed(before)
    for item in candidate["supersessions"]:
        del expected[item["supersedes_record_id"]]
    expected.update(indexed(candidate["records"]))
    if expected != indexed(after):
        raise ValueError("record preservation or exact delta closure failed")


def check_record_history(before, after, candidate):
    if set(after) != set(before) | set(indexed(candidate["records"])):
        raise ValueError("record history closure differs")
    retired = {
        s["supersedes_record_id"]: s["record_id"] for s in candidate["supersessions"]
    }
    for key, old in before.items():
        expected = old
        if key in retired:
            replacement = retired[key]
            expected = replace(
                old, superseded_by=replacement, valid_to=after[replacement].valid_from
            )
        if expected != after[key]:
            raise ValueError("record history preservation failed: " + key)


def copy_history(source, target, identity):
    data = checked_bytes(source.read_bytes(), identity, "base history identity")
    if target.exists():
        raise ValueError("refusing to overwrite history")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as stream:
        stream.write(data)


def producer_task(case, *, composition_question=None):
    finding = FINDINGS[case]
    excluded = "No questions, query code,"
    if composition_question is not None:
        if case != "evidence":
            raise ValueError("task-directed composition permits only the evidence case")
        question = composition_question
        if not question["required_semantics"]:
            raise ValueError("composition requires explicit coverage requirements")
        finding = (
            "This is task-directed repair, not question-withheld capture.\n\n"
            + question["id"]
            + ": "
            + question["question"]
            + "\nRequired semantics: "
            + ", ".join(question["required_semantics"])
            + ".\n\nYou have no expected answer values. Inspect the source and accepted graph. "
            "Decide which new source-attributed evidence connections to "
            "claim:hyp-co2-degassing are justified, preserving qualifications. "
            "Add only supported ResearchRelation records or refuse. Identify "
            "unfulfilled requirements honestly; no connection is mandatory. "
            "Do not invent measurements or treat an author's argument as proof."
        )
        excluded = "The supplied competency question is allowed. No other questions, query code,"
    obligation = {
        "funding": "You must supersede rel:erc-funds-singh exactly once with one FundingRelation, preserving its endpoints and exact type. Only that replacement is permitted.",
        "evidence": "This case permits additions only: ResearchRelation records between existing entities and the existing hypothesis. Supersessions must be empty.",
    }[case]
    return f"""# Bounded source-grounded repair: {case}

{finding}

This is feedback-guided correction, not a fresh capture. Read only this task's
inputs and write only this task's work directory. {excluded}
prior reviews, network, delegation, or other runs. You are not alone in the
workspace; do not change anyone else's files. Read the ontology and complete
import closure before interpreting its types or relation meanings.

Return work/candidate-01.json with exactly capture, records, supersessions.
The capture has the same closed grammar as baseline-capture.json, but contains
only new assertion IDs and verbatim evidence for your delta. Keep its attribution
and reading identity. nothing_assertable is empty unless justified. Unexamined
blocks remain UNTOUCHED, not fabricated gaps. Each new record value and relation
endpoint needs an explicit formalized_by path to a source assertion. Use only
existing ontology types and enums. Existing records are context, never resubmit
them with reused IDs. records has five explicit arrays: entities, relations,
events, signals, event_participations. Only relations may be nonempty here.
Use fresh record IDs prefixed repair:{case}: and fresh assertion IDs with that
prefix. Supersessions use record_id and supersedes_record_id.
{obligation}
If scope or source prevents a faithful change, write work/refusal.md instead.
Write work/rationale.md with exact locators, qualifications and limitations.
Do not execute admission or invent a successful check. The coordinator returns
at most two structural diagnostics; no semantic adequacy retry is promised.
"""


def stage(output, *, composition=False):
    target = new_private_directory(output, ROOT / "private")
    pilot.verify_runtime()
    expected = json.loads((EXPERIMENT / "results/run-result.json").read_bytes())
    replay = api.KnowledgeChangeHistory.reopen(BASE / "ledger/history.jsonl").replay()
    checked_bytes(
        replay.receipt.canonical_bytes, expected["replay_receipt_sha256"], "base replay"
    )
    checked_bytes(
        pilot.canonical(replay.graph.export_records()),
        expected["export_records_sha256"],
        "base graph",
    )
    common = {
        "selected-reading.json": (
            ROOT / "private/paper-v4-text-layer/selected-reading.json"
        ).read_bytes(),
        "ontology.yaml": (EXPERIMENT / "ontology-run/ontology-01.yaml").read_bytes(),
        "population-surface.json": (
            EXPERIMENT / "ontology-run/population-surface.json"
        ).read_bytes(),
        "baseline-records.json": pilot.canonical(replay.graph.export_records()),
        "baseline-capture.json": (BASE / "ledger/retained-capture.json").read_bytes(),
    }
    for name in (
        "malleus.yaml",
        "linkml-types.yaml",
        "metrology.yaml",
        "chronology.yaml",
        "research.yaml",
        "profile-source-assertion.json",
    ):
        common[name] = (BASE / "producer/inputs" / name).read_bytes()
    closure = set(expected["source_closure_sha256"].values())
    if not closure <= {digest(value) for value in common.values()}:
        raise ValueError("accepted ontology closure differs")
    checked_bytes(
        common["selected-reading.json"],
        "sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17",
        "reading",
    )
    target.mkdir(parents=True)
    plan_name = (
        "composition-experiment-plan.md" if composition else "repair-experiment-plan.md"
    )
    fixed = {
        "base-history.jsonl": (BASE / "ledger/history.jsonl").read_bytes(),
        "before-query.json": (
            ROOT
            / "private/paper-v4-answer-demonstration/pilot-03/run-21/query-result.json"
        ).read_bytes(),
        "answers.py": (
            ROOT / "private/paper-v4-answer-demonstration/pilot-03/run-21/answers.py"
        ).read_bytes(),
        "questions.json": (
            ROOT / "paper-v4/experiment-v4/competency-questions-v3.json"
        ).read_bytes(),
        "plan.md": (ROOT / "paper-v4" / plan_name).read_bytes(),
    }
    checked_bytes(
        fixed["answers.py"],
        json.loads(fixed["before-query.json"])["inputs"]["query_program_sha256"],
        "query program",
    )
    materials = []
    for name, source in fixed.items():
        (target / name).write_bytes(source)
        materials.append({"path": name, "sha256": digest(source)})
    question = None
    if composition:
        question = next(
            q
            for q in pilot.load_questions(fixed["questions.json"])
            if q["id"] == "CQ-T5-01"
        )
    cases = ("evidence",) if composition else tuple(FINDINGS)
    for case in cases:
        inputs = target / case / "inputs"
        inputs.mkdir(parents=True)
        (target / case / "work").mkdir()
        for name, source in common.items():
            (inputs / name).write_bytes(source)
            materials.append(
                {
                    "path": str((inputs / name).relative_to(target)),
                    "sha256": digest(source),
                }
            )
        if composition:
            source = canonical(question)
            (inputs / "competency-question.json").write_bytes(source)
            materials.append(
                {
                    "path": str(
                        (inputs / "competency-question.json").relative_to(target)
                    ),
                    "sha256": digest(source),
                }
            )
        source = producer_task(case, composition_question=question).encode()
        (inputs / "TASK.md").write_bytes(source)
        materials.append(
            {
                "path": str((inputs / "TASK.md").relative_to(target)),
                "sha256": digest(source),
            }
        )
    manifest = {
        "schema": "malleus.paper-v4.bounded-repair/v1",
        "status": "FROZEN_BEFORE_DISPATCH",
        "core_commit": pilot.CORE,
        "base_run": "run-21",
        "producer_model": "gpt-5.6-sol",
        "condition": "TASK_DIRECTED_COMPOSITION"
        if composition
        else "FINDING_GUIDED_REPAIR",
        "contract_identity": replay.partial_contract.identity,
        "base_receipt_sha256": digest(replay.receipt.canonical_bytes),
        "materials": materials,
    }
    (target / "manifest.json").write_bytes(canonical(manifest))
    return manifest


def context(manifest):
    if manifest["schema"] == "malleus.paper-v4.acquisition/v1":
        if (
            manifest["condition"],
            manifest["amendment_id"],
            manifest["query_reader"],
        ) != (
            "SOURCE_GROUNDED_ACQUISITION_RELATIONS",
            "acquisition-01",
            "SubjectGraphReads",
        ):
            raise ValueError(
                "acquisition requires its exact condition, identity and reader"
            )
        return "evidence/producer/inputs", None, manifest["query_reader"]
    if manifest["schema"] == "malleus.paper-v4.reconciliation/v1":
        conditions = {
            "RCA_GUIDED_SIX_RECORD_RECONCILIATION": "reconciliation-01",
            "SOURCE_REVIEW_FEEDBACK_RECONCILIATION": "reconciliation-feedback-01",
        }
        if (
            manifest["condition"] not in conditions
            or manifest["amendment_id"] != conditions[manifest["condition"]]
            or manifest["query_reader"] != "SubjectGraphReads"
        ):
            raise ValueError(
                "reconciliation requires its exact condition, identity and reader"
            )
        return "evidence/producer/inputs", None, manifest["query_reader"]
    if manifest["schema"] == "malleus.paper-v4.integration/v1":
        if (
            manifest["condition"] != "QUESTION_WITHHELD_CONTEXT_INTEGRATION"
            or manifest["query_reader"] != "SubjectGraphReads"
        ):
            raise ValueError("integration requires its exact condition and reader")
        return "evidence/producer/inputs", None, manifest["query_reader"]
    if manifest["schema"] in {
        "malleus.paper-v4.links/v1",
        "malleus.paper-v4.argument/v1",
        "malleus.paper-v4.qualification/v1",
    }:
        if (
            manifest["query_reader"] != "SubjectGraphReads"
            or not manifest["hypothesis_id"]
        ):
            raise ValueError(
                "links requires its explicit hypothesis and subject reader"
            )
        return (
            "evidence/producer/inputs",
            manifest["hypothesis_id"],
            manifest["query_reader"],
        )
    if manifest["schema"] == "malleus.paper-v4.bounded-repair/v1":
        return "evidence/inputs", "claim:hyp-co2-degassing", "GraphReads"
    raise ValueError("unknown amendment condition")


def artifact_ids(manifest, case):
    if manifest["schema"] in {
        "malleus.paper-v4.reconciliation/v1",
        "malleus.paper-v4.acquisition/v1",
    }:
        context(manifest)
        name = manifest["amendment_id"]
        if case != "evidence":
            raise ValueError("reconciliation requires its exact identity and case")
    elif manifest["schema"] == "malleus.paper-v4.integration/v1":
        name = manifest["amendment_id"]
        if name != "integration-01" or case != "evidence":
            raise ValueError(
                "integration requires its exact amendment identity and case"
            )
    elif manifest["schema"] == "malleus.paper-v4.qualification/v1":
        name = manifest["amendment_id"]
        if name != "qualification-01" or case != "evidence":
            raise ValueError(
                "qualification requires its exact amendment identity and case"
            )
    elif manifest["schema"] == "malleus.paper-v4.argument/v1":
        name = manifest["amendment_id"]
        if name not in {"argument-01", "argument-scope-01"}:
            raise ValueError(
                "argument completion requires its fresh amendment identity"
            )
    elif manifest["schema"] in {
        "malleus.paper-v4.links/v1",
        "malleus.paper-v4.bounded-repair/v1",
    }:
        name = "repair-01"
    else:
        raise ValueError("unknown amendment condition")
    return (
        f"actor:codex:{name}:{case}",
        f"capture:paper-v4:{name}:{case}",
        f"plan:paper-v4:{name}:{case}",
    )


def frozen_queries(run, replay, surface, *, reader="GraphReads", questions_path=None):
    if reader not in {"GraphReads", "SubjectGraphReads"}:
        raise ValueError("unknown frozen query reader")
    path = run / "answers.py"
    spec = importlib.util.spec_from_file_location("frozen_repair_answers", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    reader_class = module.GraphReads
    if reader == "SubjectGraphReads":
        # The subject reader imports answers. Bind that import to the exact
        # frozen module, not whichever live query module the harness imported.
        previous = sys.modules["answers"] if "answers" in sys.modules else None
        sys.modules["answers"] = module
        try:
            subject_spec = importlib.util.spec_from_file_location(
                "frozen_repair_subject_answers", run / "subject_answers.py"
            )
            subject = importlib.util.module_from_spec(subject_spec)
            subject_spec.loader.exec_module(subject)
            reader_class = subject.SubjectGraphReads
        finally:
            if previous is None:
                del sys.modules["answers"]
            else:
                sys.modules["answers"] = previous
    native, guard_identity = pilot.load_native()
    guard = native._SourceFreeGuard()
    questions = pilot.load_questions(
        (
            run / "questions.json" if questions_path is None else questions_path
        ).read_bytes()
    )
    with guard:
        reads = reader_class(replay.graph, surface)
        queries = [module.answer(reads, question["id"]) for question in questions]
        traces = native.trace_witnesses(
            replay, sorted({key for row in queries for key in row["witness_ids"]})
        )
    return queries, traces, guard_identity, guard.attempts


def check_read_guard(attempts):
    if set(attempts) != {"file_read", "network", "embedding_import"} or any(
        type(count) is not int or count != 0 for count in attempts.values()
    ):
        raise ValueError("query guard counters are missing, malformed or nonzero")


def preflight(run):
    manifest = json.loads((run / "manifest.json").read_bytes())
    verify_materials(run, manifest["materials"])
    pilot.verify_runtime(manifest["core_commit"])
    replay = api.KnowledgeChangeHistory.reopen(run / "base-history.jsonl").replay()
    checked_bytes(
        replay.receipt.canonical_bytes, manifest["base_receipt_sha256"], "base receipt"
    )
    input_directory, _, reader = context(manifest)
    surface = json.loads(
        (run / input_directory / "population-surface.json").read_bytes()
    )
    queries, _, _, attempts = frozen_queries(run, replay, surface, reader=reader)
    if queries != json.loads((run / "before-query.json").read_bytes())["queries"]:
        raise ValueError("frozen before queries do not reproduce")
    check_read_guard(attempts)
    return manifest, replay, queries


def execute(run, case, candidate_path, output, *, transaction_time):
    executor_source(Path(__file__), LOADED_EXECUTOR_BYTES)
    run = run.resolve()
    manifest, baseline, before_queries = preflight(run)
    review_decision = None
    if manifest["schema"] in {
        "malleus.paper-v4.reconciliation/v1",
        "malleus.paper-v4.acquisition/v1",
    }:
        from reconciliation import authorize

        review_decision = authorize(run, candidate_path)
    input_directory, hypothesis_id, reader = context(manifest)
    inputs = run / input_directory
    target = new_private_directory(output, ROOT / "private")
    if not target.is_relative_to(run / case):
        raise ValueError("attempt must be inside its case")
    submitted = candidate_path.read_bytes()
    target.mkdir(parents=True)
    (target / "executor.py").write_bytes(LOADED_EXECUTOR_BYTES)
    (target / "submitted-population.json").write_bytes(submitted)
    clock = transaction_time
    actor, capture_id, plan_id = artifact_ids(manifest, case)
    phase = "scope"
    result = {
        "core_commit": manifest["core_commit"],
        "case": case,
        "submitted_sha256": digest(submitted),
        "transaction_time": clock,
        "runner_sha256": digest(LOADED_EXECUTOR_BYTES),
    }
    try:
        candidate = population_parts(json.loads(submitted))
        base_graph = baseline.graph.export_records()
        if manifest["schema"] in {
            "malleus.paper-v4.reconciliation/v1",
            "malleus.paper-v4.acquisition/v1",
        }:
            if manifest["schema"] == "malleus.paper-v4.acquisition/v1":
                from acquisition import load_check

                report_key = "acquisition_report_sha256"
            else:
                from reconciliation import load_check

                report_key = "reconciliation_report_sha256"

            report_bytes = load_check(run, base_graph, candidate_path)
            (target / "submitted-report.json").write_bytes(report_bytes)
            (target / "source-review-decision.json").write_bytes(
                canonical(review_decision)
            )
            result[report_key] = digest(report_bytes)
            result["source_review_decision_sha256"] = digest(canonical(review_decision))
        elif manifest["schema"] == "malleus.paper-v4.integration/v1":
            from integration import check_integration

            checked_bytes(
                (Path(__file__).parent / "integration.py").read_bytes(),
                digest((run / "integration.py").read_bytes()),
                "frozen integration scope",
            )
            report_bytes = candidate_path.with_suffix(".report.json").read_bytes()
            (target / "submitted-report.json").write_bytes(report_bytes)
            result["integration_report_sha256"] = digest(report_bytes)
            check_integration(
                base_graph,
                candidate,
                json.loads(report_bytes),
                json.loads((inputs / "selected-reading.json").read_bytes()),
            )
        elif manifest["schema"] == "malleus.paper-v4.qualification/v1":
            if manifest["condition"] != "FINDING_GUIDED_QUALIFICATION":
                raise ValueError("qualification requires its exact condition")
            check_qualification(
                candidate,
                base_graph,
                observation_id=manifest["observation_id"],
                relation_id=manifest["relation_id"],
            )
        else:
            check_scope(case, candidate, base_graph, hypothesis_id=hypothesis_id)
        phase = "adapter"
        capture_bytes = pilot.canonical(candidate["capture"])
        capture_path = target / "retained-capture.json"
        capture_path.write_bytes(capture_bytes)
        adapted = api.adapt_document_assertions(
            reading_bytes=(inputs / "selected-reading.json").read_bytes(),
            capture_bytes=capture_bytes,
            capture_id=capture_id,
            plan_id=plan_id,
            contract_identity=baseline.partial_contract.identity,
            records=candidate["records"],
            supersessions=candidate["supersessions"],
            contract_view=baseline.contract_view,
        )
        plan = json.loads(adapted.canonical_plan_bytes)
        profile = api.DomainHistoryProfile.from_data(
            json.loads((inputs / "profile-source-assertion.json").read_bytes())
        )
        phase = "compile"
        compiled = api.compile_population_plan(
            plan,
            partial_contract=baseline.partial_contract,
            contract_view=baseline.contract_view,
            base_state=api.PopulationBaseState.from_replay(baseline),
            history_profile=profile,
        )
        phase = "retention"
        ledger = target / "ledger/history.jsonl"
        base_bytes = (run / "base-history.jsonl").read_bytes()
        copy_history(run / "base-history.jsonl", ledger, digest(base_bytes))
        helpers = reference_module("run.py")
        helpers._quiet_cli(
            [
                "retain",
                "--ledger",
                str(ledger),
                "--evidence",
                capture_id,
                str(capture_path),
                "application/json",
                "--transaction-time",
                clock,
                "--actor-id",
                actor,
            ]
        )
        history = api.KnowledgeChangeHistory.reopen(ledger)
        phase = "preparation"
        prepared = api.prepare_population_change(
            history=history,
            plan=plan,
            profile=json.loads(profile.canonical_bytes),
            retention_events=api.population_retention_events(
                history=history, compilation=compiled, profile=profile
            ),
            transaction_time=clock,
            actor_id=actor,
        )
        if prepared.change_set is None:
            raise ValueError(
                "nonempty scoped delta unexpectedly produced no change set"
            )
        phase = "admission"
        admitted = api.admit_structural_change(
            history=history,
            preparation=prepared,
            transaction_time=clock,
            actor_id=actor,
        )
        receipt, graph = (
            admitted.receipt.canonical_bytes,
            admitted.graph.export_records(),
        )
        del admitted, history, prepared
        phase = "reopen"
        replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
        verify_replay(
            receipt,
            graph,
            replay.receipt.canonical_bytes,
            replay.graph.export_records(),
            admission_occurred=True,
        )
        check_preservation(base_graph, replay.graph.export_records(), candidate)
        if not ledger.read_bytes().startswith(base_bytes):
            raise ValueError("base ledger prefix changed")
        retired = {
            item["supersedes_record_id"]: item["record_id"]
            for item in candidate["supersessions"]
        }
        check_record_history(baseline.record_history, replay.record_history, candidate)
        phase = "query"
        ledger_before, graph_before = ledger.read_bytes(), replay.graph.state_digest()
        surface = json.loads((inputs / "population-surface.json").read_bytes())
        queries, traces, guard, forbidden = frozen_queries(
            run, replay, surface, reader=reader
        )
        check_read_guard(forbidden)
        if (
            ledger_before != ledger.read_bytes()
            or graph_before != replay.graph.state_digest()
        ):
            raise ValueError("query changed state or attempted source access")
        changed = [
            after["question_id"]
            for before, after in zip(before_queries, queries, strict=True)
            if before != after
        ]
        artifacts = {
            "population-plan.json": adapted.canonical_plan_bytes,
            "census.json": adapted.canonical_census_bytes,
            "replay-receipt.json": replay.receipt.canonical_bytes,
            "export-records.json": pilot.canonical(replay.graph.export_records()),
            "query-trace-summary.json": canonical({"records": traces}),
            "query-result.json": canonical(
                {
                    "queries": queries,
                    "changed_question_ids": changed,
                    "query_program_sha256": digest((run / "answers.py").read_bytes()),
                    "query_reader": reader,
                    "reader_sha256": digest(
                        (
                            run
                            / (
                                "subject_answers.py"
                                if reader == "SubjectGraphReads"
                                else "answers.py"
                            )
                        ).read_bytes()
                    ),
                    "read_guard_sha256": guard,
                    "forbidden_attempts": forbidden,
                }
            ),
            "delta-trace.json": canonical(
                {
                    "records": [
                        helpers._trace_record(replay, key)
                        for key in sorted(
                            set(indexed(candidate["records"])) | set(retired)
                        )
                    ]
                }
            ),
        }
        for name, source in artifacts.items():
            (target / name).write_bytes(source)
        result.update(
            status="ADMITTED_REPLAYED_UNREVIEWED",
            ledger_head=replay.ledger_head,
            ledger_event_count=replay.ledger_event_count,
            base_prefix_preserved=True,
            exact_delta_preserved=True,
            historical_traces_preserved=True,
            replay_matches_preclose=True,
            ledger_bytes_unchanged_by_query=True,
            graph={family: len(rows) for family, rows in graph.items()},
            changed_question_ids=changed,
            artifacts={name: digest(source) for name, source in artifacts.items()},
        )
    except (ValueError, TypeError, OSError) as error:
        result.update(
            status="REFUSED_OR_CHECK_FAILED",
            phase=phase,
            error_type=type(error).__name__,
            detail=str(error),
        )
    verify_materials(run, manifest["materials"])
    executor_source(Path(__file__), LOADED_EXECUTOR_BYTES)
    (target / "run-result.json").write_bytes(canonical(result))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", type=Path)
    parser.add_argument(
        "--composition",
        action="store_true",
        help="Stage the separate question-conditioned evidence repair",
    )
    parser.add_argument("--run", type=Path)
    parser.add_argument("--case", choices=sorted(FINDINGS))
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--transaction-time",
        help="Explicit protocol time for deterministic reproduction, not execution wall time",
    )
    args = parser.parse_args()
    if args.stage:
        result = stage(args.stage, composition=args.composition)
    elif args.case and args.run and args.candidate and args.output:
        clock = (
            args.transaction_time
            if args.transaction_time is not None
            else datetime.now(timezone.utc).isoformat()
        )
        result = execute(
            args.run, args.case, args.candidate, args.output, transaction_time=clock
        )
    elif args.run and not (args.case or args.candidate or args.output):
        preflight(args.run)
        result = {"status": "BASE_AND_30_QUERIES_REPRODUCED"}
    else:
        parser.error(
            "require --stage, --run alone, or --run/--case/--candidate/--output"
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
