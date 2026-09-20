"""Admit run-23's honest population under the three document-path rules.

Three steps, each a separate observation.

``control`` runs run-23's own ``run.py``, unmodified, against the Core exported
from the isolated candidate, so a refusal by Core's hardened structural gate is
never read as a refusal by the rules.

``honest`` rebuilds the same run in a fresh history whose selected policy is
this directory's, executes the pinned Prolog rules over the staged candidate
with the plan's derivations and the capture's retained sentences supplied as
provenance, and submits the real result to the policy. Nothing here invents an
outcome.

``probe`` does the same with one deliberately faulted population, trial
``a-01`` of ``fault-injection-01``'s frozen catalog, which that cell admitted
under Core ``c95dba7b`` with nothing in the run's own artifacts to show for it.

Source-bearing outputs stay under ``--private``. The public record is
``outcomes.json`` beside this file: identities, digests, counts, refused record
identities and slot names, and no value from the reading.

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<core>/src:. .venv/bin/python \
        paper-v4/experiment-v4/content-rules-doc-01/run_policy.py \
        --producer private/paper-v4-v4-run-23/producer \
        --private private/paper-v4-content-rules-doc-01
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import malleus.compiler as api
from malleus.kg import KnowledgeGraph
from malleus.logic import (
    GraphProvenance,
    LogicCheckResult,
    LogicContract,
    LogicError,
    RecordDerivation,
    RetainedSourceText,
)
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, stage_subgraph


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUNNER = ROOT / "paper-v4/experiment-v4/run-23/run.py"
FAULTS = ROOT / "paper-v4/experiment-v4/fault-injection-01"

OUTCOME_SCHEMA = "malleus.paper-v4.content-rules-doc-01-outcomes/v1"
CORE_COMMIT = "e7937b89"
POLICY_REFERENCE = "required-check-verdict"
PROBE_TRIAL = "a-01"

# run-23's own coordinates, unchanged.
CAPTURE_ID = "capture:paper-v4:yu-2025:v4:23"
PLAN_ID = "plan:paper-v4:yu-2025:v4:23"
SOURCE_ID = "source:yu-2025-mid-atlantic-ridge"
ARTIFACT_ID = "artifact:selected-reading:yu-2025:v4:23"
TRANSACTION_TIME = "2026-09-09T22:00:20Z"
ACTOR_ID = "actor:overseer-run-23"
CLOSURE = (
    ("paper-v4-project", "work/ontology-attempt-01.yaml"),
    ("malleus", "inputs/malleus.yaml"),
    ("linkml:types", "inputs/linkml-types.yaml"),
    ("metrology", "inputs/metrology.yaml"),
    ("chronology", "inputs/chronology.yaml"),
    ("research", "inputs/research.yaml"),
)
READING = "inputs/selected-reading.json"
POPULATION = "work/document-population.json"
FROZEN_RECEIPT = (
    "sha256:a3abceec58dc93692cbdeabf9a95c03551177ba97d9ee4225fe29198f37f1eec"
)

LOGIC_ID = "paper-v4:content-rules-doc-01:logic"
RULES_ID = "paper-v4:content-rules-doc-01:rules"

# The mirror of the rule's declared normalisation, used only to describe a
# refusal after Prolog has made it. Never to decide one.
WHITESPACE = re.compile("[ \t\n\r\v\f\u00a0]+")


def canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def digest(content: bytes) -> str:
    return "sha256:" + sha256(content).hexdigest()


def event(kind: str, **payload: object) -> bytes:
    return canonical({"event_type": kind, "payload": payload})


def anchor(record_id, content, media_type, role="RETAINED_EVIDENCE"):
    return api.KnowledgeAnchorInput(
        machine_event=event(
            "ARTIFACT_REGISTERED",
            artifact_id=record_id,
            artifact_identity=digest(content),
        ),
        retained_bytes=content,
        media_type=media_type,
        role=role,
    )


def load_contract() -> LogicContract:
    return LogicContract.load(HERE / "logic.yaml")


def load_policy() -> api.PolicyProgram:
    return api.PolicyProgram.from_bytes(
        canonical(json.loads((HERE / "policy.json").read_bytes()))
    )


def compile_ontology(producer: Path):
    sources = {locator: (producer / rel).read_bytes() for locator, rel in CLOSURE}
    return api.compile_linkml_contract(root_locator="paper-v4-project", sources=sources)


def start(path: Path, producer: Path, population: dict):
    """Select this directory's policy in a fresh history before the first record."""

    if path.exists():
        raise ValueError("use a fresh history path; reopen existing history explicitly")
    compilation = compile_ontology(producer)
    logic = load_contract()
    if not compilation.view.verifies(logic.ontology_hash):
        raise LogicError("the document rules require run-23's exact compiled ontology")
    policy = load_policy()
    if policy.required_checks != ((logic.contract_id, logic.contract_hash),):
        raise LogicError("policy does not select this exact content-rule contract")
    normative = api.compose_normative_profile(
        protocol_machine_program=api.STRUCTURAL_HISTORY_BUNDLE.protocol_machine_program,
        policy_programs={POLICY_REFERENCE: policy},
        capability_refs=(),
    )
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=normative,
    )
    binding = api.STRUCTURAL_HISTORY_BUNDLE.history_binding
    path.parent.mkdir(parents=True, exist_ok=True)
    history = api.KnowledgeChangeHistory(
        path,
        partial_contract=partial,
        contract_view=compilation.view,
        binding=binding,
    )
    bootstrap = (
        anchor(
            "malleus:bootstrap:validated-contract",
            compilation.artifact.artifact_bytes,
            "application/json",
            "VALIDATED_CONTRACT",
        ),
        anchor(
            "malleus:bootstrap:partial-effective-contract",
            partial.canonical_bytes,
            "application/json",
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        anchor(
            "malleus:bootstrap:knowledge-history-binding",
            binding.canonical_bytes,
            "application/json",
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        anchor(LOGIC_ID, (HERE / "logic.yaml").read_bytes(), "application/yaml"),
        anchor(RULES_ID, logic.rules_source.encode(), "text/x-prolog"),
        *api.structural_source_anchors(
            source_id=SOURCE_ID,
            artifact_id=ARTIFACT_ID,
            content=(producer / READING).read_bytes(),
            media_type="application/json",
        ),
        api.structural_evidence_anchor(
            record_id=CAPTURE_ID,
            content=canonical(population["capture"]),
            media_type="application/json",
        ),
    )
    history.append_anchors(
        anchors=bootstrap, transaction_time=TRANSACTION_TIME, actor_id=ACTOR_ID
    )
    return history


def adapt(history, producer: Path, population: dict):
    """Run-23's own document adapter over the same reading and capture."""

    retention = history.replay()
    adapted = api.adapt_document_assertions(
        reading_bytes=(producer / READING).read_bytes(),
        capture_bytes=canonical(population["capture"]),
        capture_id=CAPTURE_ID,
        plan_id=PLAN_ID,
        contract_identity=retention.partial_contract.identity,
        records=population["records"],
        supersessions=population["supersessions"],
        contract_view=retention.contract_view,
    )
    return json.loads(adapted.canonical_plan_bytes), adapted


def prepare(history, plan: dict):
    retention = history.replay()
    compiled = api.compile_population_plan(
        plan,
        partial_contract=retention.partial_contract,
        contract_view=retention.contract_view,
        base_state=api.PopulationBaseState.from_replay(retention),
        history_profile=api.SOURCE_ASSERTION_PROFILE,
    )
    return api.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(api.SOURCE_ASSERTION_PROFILE.canonical_bytes),
        retention_events=api.population_retention_events(
            history=history,
            compilation=compiled,
            profile=api.SOURCE_ASSERTION_PROFILE,
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id=ACTOR_ID,
    )


def provenance(plan: dict, capture: dict) -> GraphProvenance:
    """The plan's own derivations and the capture's own retained sentences."""

    source_id = str(capture["attribution"]["source_id"])
    return GraphProvenance(
        derivations=tuple(
            RecordDerivation(
                record_id=str(item["record_id"]),
                path=tuple(str(step) for step in item["path"]),
                source_id=str(item["source_id"]),
                locator=str(item["locator"]),
            )
            for item in plan["derivations"]
        ),
        source_texts=tuple(
            RetainedSourceText(
                source_id=source_id,
                locator=str(assertion["id"]),
                text=str(assertion["statement"]),
            )
            for assertion in capture["assertions"]
        ),
    )


def check_base(replay, change):
    """The accepted graph this candidate applies to, with retirements removed."""

    retired = {
        operation.supersedes_record_id
        for operation in change.operations
        if operation.supersedes_record_id is not None
    }
    if not retired:
        return replay.graph
    kept = {
        family: [record for record in records if record["id"] not in retired]
        for family, records in replay.graph.export_records().items()
    }
    return KnowledgeGraph.from_records(replay.graph.registry, kept)


def check_writes(change):
    return [
        ProposedOperation(
            op_type=operation.operation_type,
            record_type=operation.record_type,
            record_id=operation.record_id,
            properties=dict(operation.properties),
            source_id=operation.source_id,
            target_id=operation.target_id,
        )
        for operation in change.operations
    ]


@dataclass(frozen=True)
class ContentAdmission:
    replay: object
    check: LogicCheckResult
    receipt_identity: str


class ContentRuleRefusal(ValueError):
    def __init__(self, check, refusal):
        self.check = check
        self.refusal = refusal
        super().__init__(f"document content policy {check.outcome}: {refusal}")


def admit(history, prepared, facts: GraphProvenance):
    """Run the selected rules, then atomically admit their receipt and the change."""

    before = history.replay()
    if before.receipt.identity != prepared.retention_replay.receipt.identity:
        raise api.KnowledgeChangeRefusal(
            api.KnowledgeChangeRefusalReason.STALE_BASE,
            "document content preparation is stale",
        )
    if prepared.change_set is None:
        raise ValueError("the document population must carry a change set")
    change = api.KnowledgeChangeSet.from_bytes(prepared.change_set.canonical_bytes)
    logic = load_contract()
    for identifier, content in (
        (LOGIC_ID, (HERE / "logic.yaml").read_bytes()),
        (RULES_ID, logic.rules_source.encode()),
    ):
        if before.retained_bytes(identifier) != content:
            raise LogicError("rule evidence differs from the selected history")
    policy = before.partial_contract.normative_profile.policy(POLICY_REFERENCE)
    if json.loads(policy.canonical_bytes)["required_checks"] != [
        {
            "check_contract_id": logic.contract_id,
            "check_contract_identity": logic.contract_hash,
        }
    ]:
        raise LogicError("history policy does not select this exact logic contract")
    checked = PrologVerifier(logic).verify_candidate_subgraph(
        stage_subgraph(check_base(before, change), check_writes(change)),
        provenance=facts,
    )
    plan_id = prepared.compilation.plan_id
    receipt_bytes = canonical(
        {
            "check": asdict(checked),
            "knowledge_change_set_identity": change.identity,
            "population_plan_identity": digest(before.retained_bytes(plan_id)),
        }
    )
    receipt_id = f"receipt:{change.change_set_id}"
    receipt_anchor = anchor(receipt_id, receipt_bytes, "application/json")
    preview = api.execute_event(
        before.partial_contract, before.machine_state, receipt_anchor.machine_event
    )
    if preview.receipt.outcome != "APPLIED":
        raise LogicError("check receipt cannot enter the selected protocol machine")
    proposal = f"proposal:{change.change_set_id}"
    events = (
        event(
            "CHANGE_PROPOSED",
            expected_machine_state_identity=preview.state.identity,
            knowledge_change_set_identity=change.identity,
            policy_id=policy.identifier,
            policy_identity=policy.identity,
            proposal_id=proposal,
        ),
        event(
            "CHECK_RECORDED",
            check_contract_id=logic.contract_id,
            check_contract_identity=logic.contract_hash,
            outcome=checked.outcome,
            policy_identity=policy.identity,
            proposal_id=proposal,
            receipt_id=f"check:{change.change_set_id}",
        ),
        event(
            "VERDICT_RECORDED",
            decision_id=f"decision:{change.change_set_id}",
            proposal_id=proposal,
        ),
    )
    try:
        replay = history.admit_with_anchors(
            anchors=(receipt_anchor,),
            change_set=change,
            machine_events=events,
            transaction_time=TRANSACTION_TIME,
            actor_id=ACTOR_ID,
        )
    except api.KnowledgeChangeRefusal as error:
        raise ContentRuleRefusal(checked, error) from error
    return ContentAdmission(replay, checked, digest(receipt_bytes))


# ---------------------------------------------------------------------------
# Describing a refusal, after Prolog has made it
# ---------------------------------------------------------------------------


def normalise(value: object) -> str:
    """The rule's declared normalisation, mirrored to describe what it refused."""

    if isinstance(value, bool):
        text = "true" if value else "false"
    elif isinstance(value, float):
        text = repr(value)
    else:
        text = str(value)
    return " ".join(piece for piece in WHITESPACE.split(text.lower()) if piece)


def mechanism(
    *,
    value: object,
    cited_text: str,
    slot_texts: list[str],
    record_texts: list[str],
    capture_texts: list[str],
    numeric: bool,
) -> tuple[str, dict[str, bool]]:
    """One label per refusal, from observations fixed before the run."""

    needle = normalise(value)
    flags = {
        "in_cited_text": needle in normalise(cited_text),
        "in_a_text_this_slot_derives_from": any(
            needle in normalise(text) for text in slot_texts
        ),
        "in_a_text_this_record_derives_from": any(
            needle in normalise(text) for text in record_texts
        ),
        "in_some_retained_sentence": any(
            needle in normalise(text) for text in capture_texts
        ),
        "integral_float_matches_without_its_trailing_zero": bool(
            numeric and needle.endswith(".0") and needle[:-2] in normalise(cited_text)
        ),
    }
    if flags["integral_float_matches_without_its_trailing_zero"]:
        label = "FLOAT_SPELLED_WITH_A_TRAILING_ZERO"
    elif flags["in_a_text_this_slot_derives_from"]:
        label = "CITES_ONE_SENTENCE_DERIVED_FOR_THIS_SLOT_FROM_ANOTHER"
    elif flags["in_a_text_this_record_derives_from"]:
        label = "IN_ANOTHER_SENTENCE_THE_RECORD_USES"
    elif flags["in_some_retained_sentence"]:
        label = "IN_A_RETAINED_SENTENCE_THE_RECORD_DOES_NOT_USE"
    elif numeric:
        label = "NUMBER_NOT_SPELLED_AS_THE_SENTENCE_SPELLS_IT"
    else:
        label = "IN_NO_RETAINED_SENTENCE"
    return label, flags


def describe(check: LogicCheckResult, plan: dict, capture: dict) -> list[dict]:
    """Every refused record property, with the mechanism and the exact evidence."""

    statements = {
        str(item["id"]): str(item["statement"]) for item in capture["assertions"]
    }
    records = {
        str(record["id"]): record
        for family in sorted(plan["records"])
        for record in plan["records"][family]
    }
    by_record: dict[str, set[str]] = {}
    by_slot: dict[tuple[str, str], set[str]] = {}
    for item in plan["derivations"]:
        record_id = str(item["record_id"])
        locator = str(item["locator"])
        by_record.setdefault(record_id, set()).add(locator)
        path = [str(step) for step in item["path"]]
        if len(path) == 2 and path[0] == "properties":
            by_slot.setdefault((record_id, path[1]), set()).add(locator)
    rows: list[dict] = []
    for violation in check.violations:
        if violation.rule_id != "VALUE_IN_CITED_TEXT":
            rows.append(
                {
                    "rule_id": violation.rule_id,
                    "violation_code": violation.violation_code,
                    "record_ids": list(violation.witness_record_ids),
                }
            )
            continue
        slot = violation.violation_code.split("/", 1)[1]
        for record_id in violation.witness_record_ids:
            properties = records[record_id].get("properties", {})
            value = properties[slot]
            cited = str(properties["assertion_locator"])
            label, flags = mechanism(
                value=value,
                cited_text=statements[cited],
                slot_texts=[
                    statements[locator]
                    for locator in sorted(by_slot.get((record_id, slot), set()))
                ],
                record_texts=[
                    statements[locator]
                    for locator in sorted(by_record.get(record_id, set()))
                ],
                capture_texts=list(statements.values()),
                numeric=isinstance(value, (int, float)) and not isinstance(value, bool),
            )
            rows.append(
                {
                    "rule_id": violation.rule_id,
                    "violation_code": violation.violation_code,
                    "record_id": record_id,
                    "record_type": str(records[record_id]["type"]),
                    "slot": slot,
                    "value": value,
                    "cited_locator": cited,
                    "cited_text": statements[cited],
                    "derived_for_this_slot_from": sorted(
                        by_slot.get((record_id, slot), set())
                    ),
                    "mechanism": label,
                    "observations": flags,
                    "mirror_agrees": not flags["in_cited_text"],
                }
            )
    return rows


def public_rows(rows: list[dict]) -> list[dict]:
    """The same rows with every value and every retained sentence removed."""

    public = []
    for row in rows:
        if "record_id" not in row:
            public.append(dict(row))
            continue
        public.append(
            {
                "rule_id": row["rule_id"],
                "record_id": row["record_id"],
                "record_type": row["record_type"],
                "slot": row["slot"],
                "value_kind": type(row["value"]).__name__,
                "value_length": len(str(row["value"])),
                "cited_locator": row["cited_locator"],
                "derived_for_this_slot_from": row["derived_for_this_slot_from"],
                "mechanism": row["mechanism"],
                "observations": row["observations"],
                "mirror_agrees": row["mirror_agrees"],
            }
        )
    return public


# ---------------------------------------------------------------------------
# The three steps
# ---------------------------------------------------------------------------


def control(producer: Path, private: Path) -> dict:
    """Run-23's own runner, unmodified, against the Core on this PYTHONPATH."""

    root = private / "control"
    shutil.rmtree(root, ignore_errors=True)
    command = [sys.executable, str(RUNNER), "--root", "paper-v4-project"]
    for locator, relative in CLOSURE:
        command += ["--source", locator, str(producer / relative)]
    command += [
        "--reading",
        str(producer / READING),
        "--population",
        str(producer / POPULATION),
        "--capture-id",
        CAPTURE_ID,
        "--plan-id",
        PLAN_ID,
        "--source-id",
        SOURCE_ID,
        "--artifact-id",
        ARTIFACT_ID,
        "--ledger",
        str(root / "ledger/history.jsonl"),
        "--results",
        str(root / "results"),
        "--transaction-time",
        TRANSACTION_TIME,
        "--actor-id",
        ACTOR_ID,
    ]
    completed = subprocess.run(
        command, cwd=ROOT, env=dict(os.environ), capture_output=True, text=True
    )
    if completed.returncode != 0:
        return {"exit_status": completed.returncode, "stderr": completed.stderr.strip()}
    result = json.loads((root / "results/run-result.json").read_bytes())
    return {
        "exit_status": 0,
        "status": result["status"],
        "replay_receipt_sha256": result["replay_receipt_sha256"],
        "equals_frozen_run_23": result["replay_receipt_sha256"] == FROZEN_RECEIPT,
        "graph": result["graph"],
        "ledger_event_count": result["ledger_event_count"],
    }


def policied(label: str, producer: Path, private: Path, population: dict) -> dict:
    """One policied run of one population, refused or admitted by the rules."""

    root = private / label
    shutil.rmtree(root, ignore_errors=True)
    ledger = root / "ledger/history.jsonl"
    history = start(ledger, producer, population)
    plan, adapted = adapt(history, producer, population)
    prepared = prepare(history, plan)
    facts = provenance(plan, population["capture"])
    results = root / "results"
    results.mkdir(parents=True)
    (results / "population-plan.json").write_bytes(canonical(plan))
    before = ledger.read_bytes()
    outcome: dict[str, object] = {
        "label": label,
        "capture_sha256": adapted.capture_identity,
        "plan_sha256": digest(canonical(plan)),
        "derivations": len(plan["derivations"]),
        "retained_sentences": len(population["capture"]["assertions"]),
    }
    try:
        admitted = admit(history, prepared, facts)
    except ContentRuleRefusal as error:
        rows = describe(error.check, plan, population["capture"])
        (results / "refused-detail.json").write_bytes(canonical(rows))
        outcome.update(
            {
                "outcome": "REFUSED",
                "check_outcome": error.check.outcome,
                "refusal_reason": error.refusal.reason.name,
                "ledger_unchanged": ledger.read_bytes() == before,
                "violated_rule_ids": list(error.check.violated_rule_ids),
                "fact_count": error.check.fact_count,
                "engine": f"{error.check.engine_name} {error.check.engine_version}",
                "refused": public_rows(rows),
            }
        )
        return outcome
    (results / "export-records.json").write_bytes(
        canonical(admitted.replay.graph.export_records())
    )
    (results / "check-result.json").write_bytes(canonical(asdict(admitted.check)))
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    outcome.update(
        {
            "outcome": "ADMITTED",
            "check_outcome": admitted.check.outcome,
            "violated_rule_ids": list(admitted.check.violated_rule_ids),
            "fact_count": admitted.check.fact_count,
            "engine": f"{admitted.check.engine_name} {admitted.check.engine_version}",
            "checked_rule_ids": list(admitted.check.checked_rule_ids),
            "receipt_identity": admitted.receipt_identity,
            "history_identity": replay.receipt.identity,
            "ledger_sha256": digest(ledger.read_bytes()),
            "ledger_events": replay.ledger_event_count,
            "accepted_changes": len(replay.change_sets),
            "historical_records": len(replay.record_history),
            "graph": {
                family: len(records)
                for family, records in sorted(replay.graph.export_records().items())
            },
            "refused": [],
        }
    )
    return outcome


def faulted(producer: Path) -> dict:
    """Trial ``a-01`` of fault-injection-01's frozen catalog, seed and all."""

    sys.path.insert(0, str(FAULTS))
    import faults  # noqa: PLC0415

    honest = json.loads((producer / POPULATION).read_bytes())
    trials = faults.value_not_in_block(copy.deepcopy(honest))
    for trial in trials:
        if trial["trial_id"] == PROBE_TRIAL:
            return trial
    raise ValueError(f"the frozen catalog has no trial {PROBE_TRIAL}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--producer", required=True, type=Path)
    parser.add_argument("--private", required=True, type=Path)
    parser.add_argument(
        "--steps",
        default="control,honest,probe",
        help="comma-separated subset of control, honest and probe",
    )
    arguments = parser.parse_args(argv)
    producer = arguments.producer.resolve()
    private = arguments.private.resolve()
    private.mkdir(parents=True, exist_ok=True)
    steps = [item.strip() for item in arguments.steps.split(",") if item.strip()]
    honest = json.loads((producer / POPULATION).read_bytes())

    outcomes: dict[str, object] = {
        "schema": OUTCOME_SCHEMA,
        "core_commit": CORE_COMMIT,
        "base_run": "run-23",
        "contract_identity": load_contract().contract_hash,
        "policy_identity": load_policy().identity,
        "ontology_hash": load_contract().ontology_hash,
        "inputs": {
            "honest_population_sha256": digest((producer / POPULATION).read_bytes()),
            "reading_sha256": digest((producer / READING).read_bytes()),
        },
    }
    if "control" in steps:
        outcomes["control"] = control(producer, private)
        print("control", outcomes["control"].get("status", "REFUSED"), flush=True)
    if "honest" in steps:
        outcomes["honest"] = policied("honest", producer, private, honest)
        print("honest", outcomes["honest"]["outcome"], flush=True)
    if "probe" in steps:
        trial = faulted(producer)
        outcomes["probe"] = policied("probe", producer, private, trial["population"])
        outcomes["probe"]["trial_id"] = trial["trial_id"]
        outcomes["probe"]["fault_class"] = trial["fault_class"]
        outcomes["probe"]["target"] = trial["target"]
        print("probe", outcomes["probe"]["outcome"], flush=True)

    (HERE / "outcomes.json").write_bytes(
        json.dumps(outcomes, ensure_ascii=False, indent=1, sort_keys=True).encode(
            "utf-8"
        )
        + b"\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
