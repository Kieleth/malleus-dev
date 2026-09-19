"""Compile, check and admit one population plan as one Core operation.

An adopter used to write this sequence itself: compile the plan, find the
check contract the history requires, run it, build a receipt, and call
``admit_with_anchors`` with three protocol events. Two shipped consumers wrote
the same four hundred lines with different mistakes in them, and what Core did
when a producer skipped the check was never measured. It accepted: the machine
requires a ``CHECK_RECORDED`` event naming the required contract, and it reads
the outcome string off that event, so a fabricated ``SATISFIED`` admitted with
no engine run.

``check_and_admit_population_plan`` closes that. The outcome written to the
ledger is the one the engine returned on the state the change would produce,
because the caller supplies no outcome and there is no other way in.

Which engine runs is not a call-site choice. The history's selected
``PolicyProgram`` names the check contract by identity; the operation loads the
retained bytes that hash to it. A ``LogicContract`` names no engine and closes
its fields, so a retained check contract of that shape is a Prolog contract and
``PrologVerifier`` runs it.

Atomicity, stated exactly. A ``COMPILE`` or ``CHECK`` refusal writes no byte:
both stages run before the first append. An ``ADMIT`` refusal may leave the
retained plan, gaps and profile artifact of the batch that preceded it, because
a change set binds ledger coordinates that only exist after that retention is
appended. Nothing is admitted either way, and every refusal reports
``ledger_unchanged``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from typing import Mapping

from malleus._contract_pipeline.knowledge import (
    KnowledgeAnchorInput,
    KnowledgeChangeHistory,
    KnowledgeChangeRefusal,
    KnowledgeChangeSet,
    KnowledgeHistoryReplay,
    _staged_properties,
)
from malleus._contract_pipeline.machine import execute_event
from malleus._contract_pipeline.population import (
    DomainHistoryProfile,
    PopulationBaseState,
    PopulationPlanCompilation,
    PopulationPlanRefusal,
    PopulationPlanRefusalReason,
    PopulationPlanStatus,
    compile_population_plan,
    population_retention_events,
    prepare_population_change,
)
from malleus.kg import KnowledgeGraph
from malleus.logic import (
    FACT_PREDICATES_BY_VERSION,
    GraphProvenance,
    LogicCheckResult,
    LogicContract,
    LogicError,
    RecordDerivation,
    RetainedSourceText,
)
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, stage_subgraph


REQUIRED_CHECK_POLICY_REFERENCE = "required-check-verdict"
"""The profile reference the shipped protocol machine consults for a verdict."""


class PopulationAdmissionStage(str, Enum):
    """Where the one transaction stopped."""

    COMPILE = "COMPILE"
    CHECK = "CHECK"
    ADMIT = "ADMIT"


class PopulationAdmissionRefusal(ValueError):
    """One stage refused. ``reason`` is the refusing layer's own typed name."""

    def __init__(
        self,
        stage: PopulationAdmissionStage,
        reason: str,
        detail: str,
        *,
        ledger_unchanged: bool,
        check: LogicCheckResult | None = None,
        witness_record_ids: tuple[str, ...] = (),
        violated_rule_ids: tuple[str, ...] = (),
    ) -> None:
        self.stage = stage
        self.reason = reason
        self.detail = detail
        self.ledger_unchanged = ledger_unchanged
        self.check = check
        self.witness_record_ids = witness_record_ids
        self.violated_rule_ids = violated_rule_ids
        super().__init__(f"{stage.value}/{reason}: {detail}")


@dataclass(frozen=True, slots=True)
class PopulationAdmission:
    """One admitted plan, with the check Core ran to admit it."""

    replay: KnowledgeHistoryReplay
    change_set: KnowledgeChangeSet
    check: LogicCheckResult
    check_contract_id: str
    check_contract_identity: str
    plan_id: str
    plan_identity: str
    receipt_id: str
    receipt_identity: str
    gap_count: int


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _machine_event(event_type: str, **payload: object) -> bytes:
    return _canonical({"event_type": event_type, "payload": payload})


def _coordinates(replay: KnowledgeHistoryReplay) -> tuple[str, int]:
    return replay.ledger_head, replay.ledger_event_count


def _refuse(
    stage: PopulationAdmissionStage,
    reason: str,
    detail: str,
    *,
    unchanged: bool,
    **extra: object,
) -> PopulationAdmissionRefusal:
    return PopulationAdmissionRefusal(
        stage, reason, detail, ledger_unchanged=unchanged, **extra
    )


def _selected_check_contract(
    replay: KnowledgeHistoryReplay,
) -> tuple[LogicContract, str, str]:
    """The check contract this history currently requires, from what it retains.

    The identity comes from ``required_checks``, never from a record ID a
    producer chose once: an additive revision that re-binds the rule layer
    moves the required identity and leaves the superseded contract retained
    beside the new one.
    """

    required = tuple(replay.required_checks.get(REQUIRED_CHECK_POLICY_REFERENCE, ()))
    if len(required) != 1:
        raise _refuse(
            PopulationAdmissionStage.CHECK,
            "UNEXPECTED_REQUIRED_CHECKS",
            f"policy {REQUIRED_CHECK_POLICY_REFERENCE} requires {len(required)} "
            "check contracts; this operation runs exactly one",
            unchanged=True,
        )
    contract_id, identity = required[0]
    retained = {
        member.record_id: bytes(member.content) for member in replay.retained_inputs
    }
    # A descriptor declares both of these, so the scan stays linear in a history
    # that retains one plan per admitted change rather than quadratic in it.
    descriptors = [
        record_id
        for record_id in sorted(retained)
        if b"contract_id" in retained[record_id]
        and b"rules_file" in retained[record_id]
    ]
    for descriptor_id in descriptors:
        for rules_id in sorted(retained):
            if rules_id == descriptor_id:
                continue
            try:
                contract = LogicContract.from_bytes(
                    retained[descriptor_id], retained[rules_id]
                )
            except LogicError:
                continue
            if (
                contract.contract_id == contract_id
                and contract.contract_hash == identity
            ):
                return contract, contract_id, identity
    raise _refuse(
        PopulationAdmissionStage.CHECK,
        "CHECK_CONTRACT_NOT_RETAINED",
        f"this history requires check contract {contract_id} at {identity} and "
        "retains no descriptor and rules pair that reproduces it",
        unchanged=True,
    )


def _check_base(
    replay: KnowledgeHistoryReplay, compilation: PopulationPlanCompilation
) -> KnowledgeGraph:
    """The accepted graph this candidate applies to, with its retirements gone.

    Core removes superseded records before applying a change, so the check must
    see the same base or an explicit correction reads as a live disagreement.
    """

    retired = {
        operation.supersedes_record_id
        for operation in compilation.operations
        if operation.supersedes_record_id is not None
    }
    if not retired:
        return replay.graph
    kept = {
        family: [record for record in records if record["id"] not in retired]
        for family, records in replay.graph.export_records().items()
    }
    return KnowledgeGraph.from_records(replay.graph.registry, kept)


def _check_writes(
    compilation: PopulationPlanCompilation,
) -> list[ProposedOperation]:
    """The compiled operations as staged graph writes, with values thawed.

    A compiled operation freezes list values into tuples. The ontology
    validator accepts only ``list`` for a multivalued slot, so a shallow copy
    would refuse every multivalued property at the check.
    """

    return [
        ProposedOperation(
            op_type=operation.operation_type,
            record_type=operation.record_type,
            record_id=operation.record_id,
            properties=_staged_properties(operation.properties),
            source_id=operation.source_id,
            target_id=operation.target_id,
        )
        for operation in compilation.operations
    ]


def _provenance(
    contract: LogicContract,
    plan: Mapping[str, object],
    source_texts: tuple[RetainedSourceText, ...],
) -> GraphProvenance | None:
    """The plan's own derivations and the caller's retained sentences.

    Whether a rule may read them is the contract's declaration, not a call-site
    option: a fact contract that declares no ``m_derivation`` predicate gets no
    provenance, and supplying source text against such a contract refuses
    rather than being dropped in silence.
    """

    declared = "m_derivation" in FACT_PREDICATES_BY_VERSION.get(
        contract.fact_contract_version, {}
    )
    if not declared:
        if source_texts:
            raise _refuse(
                PopulationAdmissionStage.CHECK,
                "PROVENANCE_NOT_DECLARED",
                f"check contract {contract.contract_id} declares fact contract "
                f"{contract.fact_contract_version}, whose rules cannot read "
                "retained source text",
                unchanged=True,
            )
        return None
    raw = plan["derivations"]
    assert isinstance(raw, list)
    try:
        derivations = tuple(
            RecordDerivation(
                record_id=str(item["record_id"]),
                path=tuple(str(step) for step in item["path"]),
                source_id=str(item["source_id"]),
                locator=str(item["locator"]),
            )
            for item in raw
        )
    except (KeyError, LogicError, TypeError) as error:
        raise _refuse(
            PopulationAdmissionStage.CHECK,
            "MALFORMED_DERIVATION",
            f"a plan derivation cannot be read as a check fact: {error}",
            unchanged=True,
        ) from error
    return GraphProvenance(derivations=derivations, source_texts=source_texts)


def _receipt_bytes(
    check: LogicCheckResult, change: KnowledgeChangeSet, plan_identity: str
) -> bytes:
    """The check receipt, stating its own verdict beside the engine's fields."""

    return _canonical(
        {
            "check": {**asdict(check), "outcome": check.outcome},
            "knowledge_change_set_identity": change.identity,
            "population_plan_identity": plan_identity,
        }
    )


def check_and_admit_population_plan(
    *,
    history: KnowledgeChangeHistory,
    plan_bytes: bytes,
    history_profile: DomainHistoryProfile,
    transaction_time: str,
    actor_id: str,
    retained_source_texts: tuple[RetainedSourceText, ...] = (),
) -> PopulationAdmission:
    """Compile, check and admit one population plan as one operation.

    ``plan_bytes`` are the plan as its producer wrote it. The operation
    compiles it against the contract the history currently requires, runs that
    history's required check contract over the state the change would produce,
    and on a satisfied outcome appends the retained plan, its gaps, the change
    set, the check receipt and ``CHANGE_PROPOSED``, ``CHECK_RECORDED`` and
    ``VERDICT_RECORDED``. Nothing is admitted otherwise.

    ``retained_source_texts`` carry the sentences a rule compares a value
    against, for a check contract that declares a fact contract able to read
    them. Core resolves no locator into text itself.
    """

    if not isinstance(history, KnowledgeChangeHistory):
        raise TypeError("history must be a KnowledgeChangeHistory")
    if type(plan_bytes) is not bytes:
        raise TypeError("plan_bytes must be the producer's exact plan bytes")
    if not isinstance(history_profile, DomainHistoryProfile):
        raise TypeError("history_profile must be a DomainHistoryProfile")
    if not isinstance(retained_source_texts, tuple) or any(
        not isinstance(item, RetainedSourceText) for item in retained_source_texts
    ):
        raise TypeError("retained_source_texts must be a RetainedSourceText tuple")

    before = history.replay()
    opening = _coordinates(before)

    # --- COMPILE: pure, and the last stage that can refuse a producer's shape.
    try:
        plan = json.loads(plan_bytes)
    except (UnicodeDecodeError, ValueError) as error:
        raise _refuse(
            PopulationAdmissionStage.COMPILE,
            PopulationPlanRefusalReason.MALFORMED_PLAN.value,
            f"plan bytes are not JSON data: {error}",
            unchanged=True,
        ) from error
    try:
        compilation = compile_population_plan(
            plan,
            partial_contract=before.partial_contract,
            contract_view=before.contract_view,
            base_state=PopulationBaseState.from_replay(before),
            history_profile=history_profile,
        )
    except PopulationPlanRefusal as error:
        raise _refuse(
            PopulationAdmissionStage.COMPILE,
            error.reason.value,
            error.detail,
            unchanged=True,
        ) from error
    if compilation.status is not PopulationPlanStatus.CHANGE_SET:
        raise _refuse(
            PopulationAdmissionStage.COMPILE,
            PopulationPlanStatus.NO_DOMAIN_CHANGE.value,
            f"plan {compilation.plan_id} admits no record",
            unchanged=True,
        )
    canonical_plan = json.loads(compilation.canonical_plan_bytes)
    assert isinstance(canonical_plan, dict)

    # --- CHECK: pure. The outcome is the engine's; no caller supplies one.
    contract, check_contract_id, check_identity = _selected_check_contract(before)
    provenance = _provenance(contract, canonical_plan, retained_source_texts)
    try:
        checked = PrologVerifier(contract).verify_candidate_subgraph(
            stage_subgraph(_check_base(before, compilation), _check_writes(compilation)),
            provenance=provenance,
        )
    except (LogicError, TypeError, ValueError) as error:
        raise _refuse(
            PopulationAdmissionStage.CHECK,
            "CHECK_ENGINE_FAILED",
            f"{type(error).__name__}: {error}",
            unchanged=True,
        ) from error
    if checked.outcome != "SATISFIED":
        witnesses = tuple(
            sorted(
                {
                    record_id
                    for violation in checked.violations
                    for record_id in violation.witness_record_ids
                }
            )
        )
        raise _refuse(
            PopulationAdmissionStage.CHECK,
            "CONTENT_RULE_VIOLATED",
            f"{checked.outcome}: "
            + "; ".join(
                f"{violation.rule_id} {violation.violation_code} on "
                + ", ".join(violation.witness_record_ids)
                for violation in checked.violations
            ),
            unchanged=True,
            check=checked,
            witness_record_ids=witnesses,
            violated_rule_ids=checked.violated_rule_ids,
        )

    # --- ADMIT: retention, then the change and its receipt in one batch.
    try:
        prepared = prepare_population_change(
            history=history,
            plan=plan,
            profile=history_profile,
            retention_events=population_retention_events(
                history=history, compilation=compilation, profile=history_profile
            ),
            transaction_time=transaction_time,
            actor_id=actor_id,
        )
        change = prepared.change_set
        assert change is not None
        receipt_bytes = _receipt_bytes(
            checked, change, _digest(compilation.canonical_plan_bytes)
        )
        receipt_id = f"receipt:{change.change_set_id}"
        receipt = KnowledgeAnchorInput(
            machine_event=_machine_event(
                "ARTIFACT_REGISTERED",
                artifact_id=receipt_id,
                artifact_identity=_digest(receipt_bytes),
            ),
            retained_bytes=receipt_bytes,
            media_type="application/json",
            role="RETAINED_EVIDENCE",
        )
        retention = prepared.retention_replay
        preview = execute_event(
            retention.partial_contract, retention.machine_state, receipt.machine_event
        )
        if preview.receipt.outcome != "APPLIED":
            raise _refuse(
                PopulationAdmissionStage.ADMIT,
                "RECEIPT_REFUSED",
                "the check receipt cannot enter this history's protocol machine",
                unchanged=_coordinates(history.replay()) == opening,
            )
        policy = retention.partial_contract.normative_profile.policy(
            REQUIRED_CHECK_POLICY_REFERENCE
        )
        proposal_id = f"proposal:{change.change_set_id}"
        replay = history.admit_with_anchors(
            anchors=(receipt,),
            change_set=change,
            machine_events=(
                _machine_event(
                    "CHANGE_PROPOSED",
                    expected_machine_state_identity=preview.state.identity,
                    knowledge_change_set_identity=change.identity,
                    policy_id=policy.identifier,
                    policy_identity=policy.identity,
                    proposal_id=proposal_id,
                ),
                _machine_event(
                    "CHECK_RECORDED",
                    check_contract_id=check_contract_id,
                    check_contract_identity=check_identity,
                    outcome=checked.outcome,
                    policy_identity=policy.identity,
                    proposal_id=proposal_id,
                    receipt_id=f"check:{change.change_set_id}",
                ),
                _machine_event(
                    "VERDICT_RECORDED",
                    decision_id=f"decision:{change.change_set_id}",
                    proposal_id=proposal_id,
                ),
            ),
            transaction_time=transaction_time,
            actor_id=actor_id,
        )
    except PopulationAdmissionRefusal:
        raise
    except (KnowledgeChangeRefusal, PopulationPlanRefusal) as error:
        reason = getattr(error.reason, "name", None) or str(error.reason)
        raise _refuse(
            PopulationAdmissionStage.ADMIT,
            reason,
            error.detail,
            unchanged=_coordinates(history.replay()) == opening,
            check=checked,
        ) from error

    gaps = canonical_plan["gaps"]
    assert isinstance(gaps, list)
    return PopulationAdmission(
        replay=replay,
        change_set=change,
        check=checked,
        check_contract_id=check_contract_id,
        check_contract_identity=check_identity,
        plan_id=compilation.plan_id,
        plan_identity=_digest(compilation.canonical_plan_bytes),
        receipt_id=receipt_id,
        receipt_identity=_digest(receipt_bytes),
        gap_count=len(gaps),
    )
