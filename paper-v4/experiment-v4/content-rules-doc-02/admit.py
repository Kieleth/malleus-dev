"""Run one population through run-23's path with the four rules selected.

The command line is run-23's own, argument for argument, so the same harness
can drive either: ``fault-injection-01/run_faults.py --runner`` points at this
file and every other coordinate of that cell stays where it is.

What differs from ``run-23/run.py`` is the policy. The history selects this
directory's ``PolicyProgram`` before the first record, retains ``logic.yaml``
and ``rules.pl`` as evidence, executes the pinned Prolog rules over the staged
candidate with the plan's derivations and the capture's retained sentences
supplied as provenance, and admits the check receipt and the change atomically.
It never accepts a caller-supplied outcome: the outcome is the one the engine
returned.

Outputs land under ``--results``. ``run-result.json``, ``trace-summary.json``
and ``content-rule-violations.json`` are digest-bearing and free of source
text; the plan, the gaps, the export and the refusal detail carry source values
and belong beside the run in private storage.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
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

RESULT_SCHEMA = "malleus.paper-v4.content-rules-doc-02-result/v1"
TRACE_SCHEMA = "malleus.paper-v4.trace-summary/v1"
POLICY_REFERENCE = "required-check-verdict"
LOGIC_ID = "paper-v4:content-rules-doc-02:logic"
RULES_ID = "paper-v4:content-rules-doc-02:rules"
POPULATION_FIELDS = {"capture", "records", "supersessions"}


class RunRefusal(ValueError):
    """The run inputs or the selected policy refuse this population."""


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


def anchor(record_id: str, content: bytes, media_type: str, role="RETAINED_EVIDENCE"):
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


@dataclass(frozen=True)
class Admission:
    replay: object
    check: LogicCheckResult
    receipt_identity: str


class ContentRuleRefusal(ValueError):
    def __init__(self, check: LogicCheckResult, refusal):
        self.check = check
        self.refusal = refusal
        super().__init__(f"document content policy {check.outcome}: {refusal}")


def start(
    ledger: Path,
    compilation,
    reading_bytes: bytes,
    capture_bytes: bytes,
    *,
    source_id: str,
    artifact_id: str,
    capture_id: str,
    transaction_time: str,
    actor_id: str,
):
    """Select this directory's policy in a fresh history before the first record."""

    if ledger.exists():
        raise RunRefusal("use a fresh history path; reopening is a different run")
    logic = load_contract()
    if not compilation.view.verifies(logic.ontology_hash):
        raise RunRefusal("the document rules require run-23's exact compiled ontology")
    policy = load_policy()
    if policy.required_checks != ((logic.contract_id, logic.contract_hash),):
        raise RunRefusal("policy does not select this exact content-rule contract")
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
    ledger.parent.mkdir(parents=True, exist_ok=True)
    history = api.KnowledgeChangeHistory(
        ledger,
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
            source_id=source_id,
            artifact_id=artifact_id,
            content=reading_bytes,
            media_type="application/json",
        ),
        api.structural_evidence_anchor(
            record_id=capture_id,
            content=capture_bytes,
            media_type="application/json",
        ),
    )
    history.append_anchors(
        anchors=bootstrap, transaction_time=transaction_time, actor_id=actor_id
    )
    return history


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


def admit(history, prepared, facts: GraphProvenance, *, transaction_time, actor_id):
    """Run the selected rules, then atomically admit their receipt and the change."""

    before = history.replay()
    if before.receipt.identity != prepared.retention_replay.receipt.identity:
        raise api.KnowledgeChangeRefusal(
            api.KnowledgeChangeRefusalReason.STALE_BASE,
            "document content preparation is stale",
        )
    if prepared.change_set is None:
        raise RunRefusal("the document population must carry a change set")
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
            transaction_time=transaction_time,
            actor_id=actor_id,
        )
    except api.KnowledgeChangeRefusal as error:
        raise ContentRuleRefusal(checked, error) from error
    return Admission(replay, checked, digest(receipt_bytes))


def violation_rows(check: LogicCheckResult) -> list[dict]:
    """Every violation by rule, code and witness. No value, no sentence."""

    return [
        {
            "rule_id": violation.rule_id,
            "violation_code": violation.violation_code,
            "record_ids": list(violation.witness_record_ids),
        }
        for violation in sorted(check.violations)
    ]


def _trace_record(replay, record_id: str) -> dict:
    trace = api.trace_population_record(replay, record_id)
    return {
        "record_id": trace.record_id,
        "record_type": trace.record_history.operation.record_type,
        "change_set_id": trace.change_set.change_set_id,
        "contract_identity": trace.change_set.contract_identity,
        "plan_id": str(trace.population_plan["plan_id"]),
        "plan_sha256": trace.population_plan_identity,
        "history_profile": {
            "profile_id": trace.history_profile.profile_id,
            "sha256": trace.history_profile.identity,
        },
        "evidence": {item.record_id: item.identity for item in trace.evidence},
        "sources": {item.record_id: item.identity for item in trace.sources},
        "derivations": [
            {
                "path": list(item["path"]),
                "locator": item["locator"],
                "source_id": item["source_id"],
            }
            for item in trace.derivations
        ],
        "valid_from": {
            "kind": trace.record_history.valid_from.kind,
            "value": trace.record_history.valid_from.value,
        },
        "superseded_by": trace.record_history.superseded_by,
        "supersedes_record_id": trace.record_history.supersedes_record_id,
    }


def _population(path: Path) -> dict:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict) or set(value) != POPULATION_FIELDS:
        raise RunRefusal(
            "producer population must contain exactly capture, records and"
            " supersessions"
        )
    return value


def _sources(pairs: list[list[str]]) -> dict[str, bytes]:
    sources: dict[str, bytes] = {}
    for locator, path in pairs:
        if locator in sources:
            raise RunRefusal(f"source locator is repeated: {locator}")
        sources[locator] = Path(path).read_bytes()
    return sources


def execute(arguments: argparse.Namespace) -> dict:
    results = Path(arguments.results)
    if results.exists():
        raise RunRefusal(f"results directory already exists: {results}")
    ledger = Path(arguments.ledger)
    reading_bytes = Path(arguments.reading).read_bytes()
    population = _population(Path(arguments.population))
    capture_bytes = canonical(population["capture"])
    sources = _sources(arguments.source)
    if arguments.root not in sources:
        raise RunRefusal(f"root locator is not among the sources: {arguments.root}")

    compilation = api.compile_linkml_contract(
        root_locator=arguments.root, sources=sources
    )
    history = start(
        ledger,
        compilation,
        reading_bytes,
        capture_bytes,
        source_id=arguments.source_id,
        artifact_id=arguments.artifact_id,
        capture_id=arguments.capture_id,
        transaction_time=arguments.transaction_time,
        actor_id=arguments.actor_id,
    )
    retention = history.replay()
    adapted = api.adapt_document_assertions(
        reading_bytes=reading_bytes,
        capture_bytes=capture_bytes,
        capture_id=arguments.capture_id,
        plan_id=arguments.plan_id,
        contract_identity=retention.partial_contract.identity,
        records=population["records"],
        supersessions=population["supersessions"],
        contract_view=retention.contract_view,
    )
    plan = json.loads(adapted.canonical_plan_bytes)
    compiled = api.compile_population_plan(
        plan,
        partial_contract=retention.partial_contract,
        contract_view=retention.contract_view,
        base_state=api.PopulationBaseState.from_replay(retention),
        history_profile=api.SOURCE_ASSERTION_PROFILE,
    )
    prepared = api.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(api.SOURCE_ASSERTION_PROFILE.canonical_bytes),
        retention_events=api.population_retention_events(
            history=history,
            compilation=compiled,
            profile=api.SOURCE_ASSERTION_PROFILE,
        ),
        transaction_time=arguments.transaction_time,
        actor_id=arguments.actor_id,
    )
    facts = provenance(plan, population["capture"])
    results.mkdir(parents=True)
    (results / "population-plan.json").write_bytes(adapted.canonical_plan_bytes)
    (results / "census.json").write_bytes(adapted.canonical_census_bytes)
    (results / "gaps.json").write_bytes(
        canonical({"gaps": plan["gaps"], "plan_id": plan["plan_id"]})
    )
    try:
        admitted = admit(
            history,
            prepared,
            facts,
            transaction_time=arguments.transaction_time,
            actor_id=arguments.actor_id,
        )
    except ContentRuleRefusal as error:
        (results / "content-rule-violations.json").write_bytes(
            canonical(
                {
                    "outcome": "REFUSED",
                    "check_outcome": error.check.outcome,
                    "refusal_reason": error.refusal.reason.name,
                    "violated_rule_ids": list(error.check.violated_rule_ids),
                    "violations": violation_rows(error.check),
                }
            )
        )
        raise RunRefusal(
            f"CONTENT_RULE_VIOLATED: the selected policy returned"
            f" {error.check.outcome} on"
            f" {', '.join(error.check.violated_rule_ids)}; the atomic admission"
            f" is refused with {error.refusal.reason.name}"
        ) from error

    del history, prepared, retention
    replay = api.KnowledgeChangeHistory.reopen(ledger).replay()
    reopened_receipt = replay.receipt.canonical_bytes
    reopened_export = replay.graph.export_records()
    traces = [
        _trace_record(replay, record_id) for record_id in sorted(replay.record_history)
    ]
    (results / "replay-receipt.json").write_bytes(reopened_receipt)
    (results / "export-records.json").write_bytes(canonical(reopened_export))
    (results / "check-result.json").write_bytes(canonical(asdict(admitted.check)))
    (results / "content-rule-violations.json").write_bytes(
        canonical(
            {
                "outcome": "ADMITTED",
                "check_outcome": admitted.check.outcome,
                "violated_rule_ids": list(admitted.check.violated_rule_ids),
                "checked_rule_ids": list(admitted.check.checked_rule_ids),
                "fact_count": admitted.check.fact_count,
                "engine": f"{admitted.check.engine_name} {admitted.check.engine_version}",
                "violations": violation_rows(admitted.check),
            }
        )
    )
    (results / "trace-summary.json").write_bytes(
        canonical(
            {
                "schema": TRACE_SCHEMA,
                "evidence_selection": "BY_RECORD_ID_NEVER_BY_POSITION",
                "records": traces,
            }
        )
    )
    result = {
        "schema": RESULT_SCHEMA,
        "run_id": "content-rules-doc-02",
        "status": "ADMITTED_AND_REPLAYED",
        "policy_identity": load_policy().identity,
        "check_contract_identity": load_contract().contract_hash,
        "check_outcome": admitted.check.outcome,
        "checked_rule_ids": list(admitted.check.checked_rule_ids),
        "violated_rule_ids": list(admitted.check.violated_rule_ids),
        "fact_count": admitted.check.fact_count,
        "engine": f"{admitted.check.engine_name} {admitted.check.engine_version}",
        "receipt_identity": admitted.receipt_identity,
        "capture": {
            "capture_id": adapted.capture_id,
            "capture_sha256": adapted.capture_identity,
            "reading_sha256": adapted.reading_identity,
        },
        "plan_sha256": digest(adapted.canonical_plan_bytes),
        "derivations": len(plan["derivations"]),
        "retained_sentences": len(population["capture"]["assertions"]),
        "replay_receipt_sha256": digest(reopened_receipt),
        "export_records_sha256": digest(canonical(reopened_export)),
        "trace_summary_sha256": digest((results / "trace-summary.json").read_bytes()),
        "ledger_sha256": digest(ledger.read_bytes()),
        "ledger_event_count": replay.ledger_event_count,
        "ledger_head": replay.ledger_head,
        "accepted_changes": len(replay.change_sets),
        "graph": {
            family: len(records) for family, records in sorted(reopened_export.items())
        },
        "records_traced": len(traces),
        "reopen_matches_admitted": {"receipt": True, "export_records": True},
    }
    (results / "run-result.json").write_bytes(canonical(result))
    return result


def build_parser() -> argparse.ArgumentParser:
    """run-23's own command line, argument for argument."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="root source locator")
    parser.add_argument(
        "--source",
        action="append",
        nargs=2,
        required=True,
        metavar=("LOCATOR", "PATH"),
        help="one exact source locator and file; repeat for the whole closure",
    )
    parser.add_argument("--reading", required=True)
    parser.add_argument("--population", required=True)
    parser.add_argument("--capture-id", required=True)
    parser.add_argument("--plan-id", required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--results", required=True)
    parser.add_argument("--transaction-time", required=True)
    parser.add_argument("--actor-id", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        execute(arguments)
    except (OSError, TypeError, ValueError) as error:
        print(f"content-rules-doc-02: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
