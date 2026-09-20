"""Check and admit, as one Core operation, from a plan or from a change set.

An adopter used to write this sequence itself: compile the plan, find the
check contract the history requires, run it, build a receipt, and call
``admit_with_anchors`` with three protocol events. Two shipped consumers wrote
the same four hundred lines with different mistakes in them, and what Core did
when a producer skipped the check was never measured. It accepted: the machine
requires a ``CHECK_RECORDED`` event naming the required contract, and it reads
the outcome string off that event, so a fabricated ``SATISFIED`` admitted with
no engine run.

``check_and_admit_population_plan`` closes that for a producer's plan bytes,
and ``check_and_admit_change_set`` closes it for a change set the caller
composed itself. The outcome written to the ledger is the one the engine
returned on the state the change would produce, because neither entry point
takes an outcome and, since ``admit`` and ``admit_with_anchors`` refuse a
caller's ``CHECK_RECORDED`` and ``VERDICT_RECORDED``, there is no other way in.

The two entry points differ only in where the operations come from. One
compiles them out of plan bytes against the contract the history requires; the
other is handed them already composed, which is the lower primitive and the
shape every research consumer works in. Everything after that is one shared
implementation: ``_check_stage`` resolves and runs every required check, and
``_admit_checked`` retains one receipt each and appends the change with the
three protocol events through ``_admit``.

Which engine runs is not a call-site choice. The history's selected
``PolicyProgram`` names its required check contracts by identity, in its own
order, and the operation runs every one of them through the closed executor
set of ``malleus.check-contract/v1``: a retained Prolog rule layer under
``PrologVerifier``, or a Core builtin from the registry in
``check_contract.py``. A required check whose contract the history does not
retain, or whose executor Core cannot run, refuses before the first append.

Each check writes its own ``CHECK_RECORDED``, and its payload is exactly the
fields the selected machine's ``CheckRecord`` declares as inputs. Core carries
a superset of values and the machine's own declaration selects from it, so a
machine that declares ``receipt_identity`` gets it and one that does not never
sees it.

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

from malleus._contract_pipeline.check_contract import (
    CandidateChange,
    CheckContract,
    CheckContractError,
    CheckExecutorKind,
    CheckOutcome,
    CheckRequest,
    resolve_check_contract,
    resolve_core_builtin,
)
from malleus._contract_pipeline.knowledge import (
    KnowledgeAnchorInput,
    KnowledgeChangeHistory,
    KnowledgeChangeRefusal,
    KnowledgeChangeRefusalReason,
    KnowledgeChangeSet,
    KnowledgeHistoryReplay,
    KnowledgeOperation,
    KnowledgeValidTime,
    _staged_properties,
)
from malleus._contract_pipeline.machine import execute_event
from malleus._contract_pipeline.population import (
    DomainHistoryProfile,
    PopulationBaseState,
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
class AdmittedCheck:
    """One required check Core ran, and the receipt it anchored for it."""

    check_contract_id: str
    check_contract_identity: str
    executor_kind: CheckExecutorKind
    outcome: str
    receipt_id: str
    receipt_identity: str
    record_receipt_id: str
    result: Mapping[str, object]
    logic_result: LogicCheckResult | None = None


@dataclass(frozen=True, slots=True)
class PopulationAdmission:
    """One admitted plan, with every check Core ran to admit it.

    ``checks`` holds them in the policy's own order. The singular fields name
    the first of them, which is the whole story for a policy requiring one
    check and the entry point to ``checks`` for a policy requiring more.
    """

    replay: KnowledgeHistoryReplay
    change_set: KnowledgeChangeSet
    check: LogicCheckResult | None
    check_contract_id: str
    check_contract_identity: str
    plan_id: str
    plan_identity: str
    receipt_id: str
    receipt_identity: str
    gap_count: int
    checks: tuple[AdmittedCheck, ...] = ()


@dataclass(frozen=True, slots=True)
class ChangeSetAdmission:
    """One admitted change set, with every check Core ran to admit it.

    ``checks`` holds them in the policy's own order. There are no plan fields
    here, because no plan produced this change: the caller composed it, which
    is the whole reason this result stands beside ``PopulationAdmission``.
    """

    replay: KnowledgeHistoryReplay
    change_set: KnowledgeChangeSet
    checks: tuple[AdmittedCheck, ...]


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


def _selected_check_contracts(
    replay: KnowledgeHistoryReplay,
) -> tuple[CheckContract, ...]:
    """Every check this history currently requires, in the policy's own order.

    The identities come from ``required_checks``, never from a record ID a
    producer chose once: an additive revision that re-binds the rule layer
    moves a required identity and leaves the superseded contract retained
    beside the new one.

    A required check Core cannot reach refuses here, before the first append,
    naming the contract rather than the count. The count is the policy's to
    declare, and an operation that ran a strict subset of what the policy
    requires would admit under a check nobody ran.
    """

    required = tuple(replay.required_checks.get(REQUIRED_CHECK_POLICY_REFERENCE, ()))
    if not required:
        raise _refuse(
            PopulationAdmissionStage.CHECK,
            "NO_REQUIRED_CHECK",
            f"policy {REQUIRED_CHECK_POLICY_REFERENCE} requires no check contract; "
            "this operation admits only what a check accepted",
            unchanged=True,
        )
    contracts = []
    for contract_id, identity in required:
        try:
            contracts.append(resolve_check_contract(replay, contract_id, identity))
        except CheckContractError as error:
            raise _refuse(
                PopulationAdmissionStage.CHECK,
                error.reason,
                error.detail,
                unchanged=True,
            ) from error
    return tuple(contracts)


def _run_check(
    contract: CheckContract,
    request: CheckRequest,
    provenance: GraphProvenance | None,
) -> CheckOutcome:
    """Run one required check through the executor its own contract names."""

    if contract.executor_kind is CheckExecutorKind.CORE_BUILTIN:
        builtin = resolve_core_builtin(contract.builtin_id, contract.builtin_version)
        return builtin(request)
    checked = PrologVerifier(contract.pinned_logic_contract).verify_candidate_subgraph(
        request.candidate_graph, provenance=provenance
    )
    return CheckOutcome(
        outcome=checked.outcome,
        detail="; ".join(
            f"{violation.rule_id} {violation.violation_code} on "
            + ", ".join(violation.witness_record_ids)
            for violation in checked.violations
        ),
        violated_rule_ids=checked.violated_rule_ids,
        witness_record_ids=tuple(
            sorted(
                {
                    record_id
                    for violation in checked.violations
                    for record_id in violation.witness_record_ids
                }
            )
        ),
        logic_result=checked,
    )


_SUPPORTED_EVENT_FIELDS = {
    "CHANGE_PROPOSED": frozenset(
        {
            "expected_machine_state_identity",
            "knowledge_change_set_identity",
            "policy_id",
            "policy_identity",
            "proposal_id",
        }
    ),
    "CHECK_RECORDED": frozenset(
        {
            "check_contract_id",
            "check_contract_identity",
            "outcome",
            "policy_identity",
            "proposal_id",
            "receipt_id",
            "receipt_identity",
        }
    ),
    "VERDICT_RECORDED": frozenset({"decision_id", "proposal_id"}),
}
"""Every field Core can state for each protocol event it writes.

The machine's own declaration selects from this, so a machine that declares
``receipt_identity`` on its ``CheckRecord`` gets it and one that does not never
sees it. A machine that declares a field outside this set refuses at CHECK,
before the first append, instead of being handed a guess.
"""


def _declared_fields(
    replay: KnowledgeHistoryReplay, event_type: str
) -> tuple[str, ...]:
    """The input fields the selected machine declares for one protocol event.

    ``correction/machine.json`` declares seven ``CheckRecord`` input fields
    where the shipped structural machine declares six, and an event carrying
    the wrong set refuses ``MALFORMED_EVENT`` with the retention already
    appended. Reading the declaration here moves that refusal before the first
    byte.
    """

    program = replay.partial_contract.normative_profile.protocol_machine_program
    try:
        record_type = program.data["events"][event_type]["record_type"]
        declared = tuple(program.data["record_schemas"][record_type]["input_fields"])
    except (KeyError, TypeError) as error:
        raise _refuse(
            PopulationAdmissionStage.CHECK,
            "UNDECLARED_PROTOCOL_EVENT",
            f"the selected protocol machine declares no {event_type} event",
            unchanged=True,
        ) from error
    unsupported = sorted(set(declared) - _SUPPORTED_EVENT_FIELDS[event_type])
    if unsupported:
        raise _refuse(
            PopulationAdmissionStage.CHECK,
            "UNSUPPORTED_EVENT_FIELD",
            f"the selected protocol machine declares {event_type} fields Core "
            "cannot state: " + ", ".join(unsupported),
            unchanged=True,
        )
    return declared


def _declared_event(
    event_type: str, declared: tuple[str, ...], values: Mapping[str, object]
) -> bytes:
    """One protocol event carrying exactly the fields the machine declared."""

    return _machine_event(event_type, **{name: values[name] for name in declared})


def _check_base(
    replay: KnowledgeHistoryReplay, operations: tuple[KnowledgeOperation, ...]
) -> KnowledgeGraph:
    """The accepted graph this candidate applies to, with its retirements gone.

    Core removes superseded records before applying a change, so the check must
    see the same base or an explicit correction reads as a live disagreement.
    """

    retired = {
        operation.supersedes_record_id
        for operation in operations
        if operation.supersedes_record_id is not None
    }
    if not retired:
        return replay.graph
    kept = {
        family: [record for record in records if record["id"] not in retired]
        for family, records in replay.graph.export_records().items()
    }
    try:
        return KnowledgeGraph.from_records(replay.graph.registry, kept)
    except ValueError as error:
        # A retirement the accepted state cannot carry, such as an entity a
        # live relation still names. ``_apply_change`` refuses the same case
        # with the same words; refusing here keeps the check from crashing
        # before any executor has run, and writes no byte either way.
        raise _refuse(
            PopulationAdmissionStage.CHECK,
            KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL.name,
            str(error),
            unchanged=True,
        ) from error


def _check_writes(
    operations: tuple[KnowledgeOperation, ...],
) -> list[ProposedOperation]:
    """The candidate's operations as staged graph writes, with values thawed.

    A compiled or composed operation freezes list values into tuples. The
    ontology validator accepts only ``list`` for a multivalued slot, so a
    shallow copy would refuse every multivalued property at the check.
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
        for operation in operations
    ]


def _declares_provenance(contract: LogicContract) -> bool:
    return "m_derivation" in FACT_PREDICATES_BY_VERSION.get(
        contract.fact_contract_version, {}
    )


def _provenance(
    contracts: tuple[CheckContract, ...],
    plan: Mapping[str, object] | None,
    source_texts: tuple[RetainedSourceText, ...],
) -> GraphProvenance | None:
    """The plan's own derivations and the caller's retained sentences.

    Whether a rule may read them is the contract's declaration, not a call-site
    option: a fact contract that declares no ``m_derivation`` predicate gets no
    provenance, and supplying source text when no required rule layer can read
    it refuses rather than being dropped in silence. A builtin reads the
    candidate and the accepted state, never a sentence, so it is not consulted
    here.

    A composed change set has no plan, so it declares no derivation and Core
    invents none: a rule layer able to read provenance finds no derivation
    fact rather than a guessed one.
    """

    rule_layers = tuple(
        contract.pinned_logic_contract
        for contract in contracts
        if contract.executor_kind is CheckExecutorKind.PROLOG_RULES
    )
    if not any(_declares_provenance(logic) for logic in rule_layers):
        if source_texts:
            named = rule_layers[0] if rule_layers else None
            raise _refuse(
                PopulationAdmissionStage.CHECK,
                "PROVENANCE_NOT_DECLARED",
                (
                    f"check contract {named.contract_id} declares fact contract "
                    f"{named.fact_contract_version}, whose rules cannot read "
                    "retained source text"
                )
                if named is not None
                else "no required check runs rules that can read retained source text",
                unchanged=True,
            )
        return None
    if plan is None:
        return GraphProvenance(derivations=(), source_texts=source_texts)
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
    contract: CheckContract,
    outcome: CheckOutcome,
    change: KnowledgeChangeSet,
    plan_identity: str | None,
) -> bytes:
    """One check's receipt, stating the executor that produced its verdict.

    ``plan_identity`` is absent for a change set the caller composed, which no
    plan produced, and the receipt says so by naming none.
    """

    check: dict[str, object] = {}
    if outcome.logic_result is not None:
        check.update(asdict(outcome.logic_result))
    check.update(
        {
            "check_contract_id": contract.check_contract_id,
            "check_contract_identity": contract.identity,
            "executor_kind": contract.executor_kind.value,
            "outcome": outcome.outcome,
        }
    )
    if outcome.result:
        check["result"] = dict(outcome.result)
    body: dict[str, object] = {
        "check": check,
        "knowledge_change_set_identity": change.identity,
    }
    if plan_identity is not None:
        body["population_plan_identity"] = plan_identity
    return _canonical(body)


def _receipt_ids(change_set_id: str, contract: CheckContract) -> tuple[str, str]:
    """The retained receipt's ID and the ``CheckRecord`` ID, for one check.

    Both name the change and the check. The single-check form they replace
    named only the change, which cannot say which of two receipts is which,
    and the machine refuses a repeated ``CheckRecord`` ID outright.
    """

    return (
        f"receipt:{change_set_id}:{contract.check_contract_id}",
        f"check:{change_set_id}:{contract.check_contract_id}",
    )


def _check_stage(
    replay: KnowledgeHistoryReplay,
    *,
    change_set_id: str,
    operations: tuple[KnowledgeOperation, ...],
    valid_time: KnowledgeValidTime,
    plan: Mapping[str, object] | None = None,
    retained_source_texts: tuple[RetainedSourceText, ...] = (),
) -> tuple[
    tuple[CheckContract, ...],
    Mapping[str, tuple[str, ...]],
    tuple[CheckOutcome, ...],
]:
    """Run every check this history's policy requires, in the policy's order.

    Both entry points share this, which is the point of it: the checks Core
    runs cannot depend on whether the caller arrived with plan bytes or with a
    change set it composed. It is pure. It resolves each required contract,
    reads the fields the selected machine declares for the three protocol
    events, and runs each executor over the state the candidate would produce.
    Every refusal here leaves the ledger byte-identical, and nothing in the
    signature carries an outcome.
    """

    contracts = _selected_check_contracts(replay)
    declared = {
        event_type: _declared_fields(replay, event_type)
        for event_type in ("CHANGE_PROPOSED", "CHECK_RECORDED", "VERDICT_RECORDED")
    }
    provenance = _provenance(contracts, plan, retained_source_texts)
    request = CheckRequest(
        replay=replay,
        candidate=CandidateChange(
            change_set_id=change_set_id,
            operations=operations,
            valid_time=valid_time,
        ),
        candidate_graph=stage_subgraph(
            _check_base(replay, operations), _check_writes(operations)
        ),
        provenance=provenance,
    )
    outcomes: list[CheckOutcome] = []
    for contract in contracts:
        try:
            checked = _run_check(contract, request, provenance)
        except CheckContractError as error:
            raise _refuse(
                PopulationAdmissionStage.CHECK,
                error.reason,
                error.detail,
                unchanged=True,
            ) from error
        except (LogicError, TypeError, ValueError) as error:
            raise _refuse(
                PopulationAdmissionStage.CHECK,
                "CHECK_ENGINE_FAILED",
                f"{type(error).__name__}: {error}",
                unchanged=True,
            ) from error
        if checked.outcome not in contract.outcomes:
            raise _refuse(
                PopulationAdmissionStage.CHECK,
                "UNDECLARED_CHECK_OUTCOME",
                f"check contract {contract.check_contract_id} declares "
                + ", ".join(contract.outcomes)
                + f" and its executor returned {checked.outcome}",
                unchanged=True,
                check=checked.logic_result,
            )
        if checked.outcome != "SATISFIED":
            raise _refuse(
                PopulationAdmissionStage.CHECK,
                "CONTENT_RULE_VIOLATED",
                f"{checked.outcome}: {checked.detail}",
                unchanged=True,
                check=checked.logic_result,
                witness_record_ids=checked.witness_record_ids,
                violated_rule_ids=checked.violated_rule_ids,
            )
        outcomes.append(checked)
    return contracts, declared, tuple(outcomes)


def _admit_checked(
    *,
    history: KnowledgeChangeHistory,
    staged: KnowledgeHistoryReplay,
    change: KnowledgeChangeSet,
    contracts: tuple[CheckContract, ...],
    outcomes: tuple[CheckOutcome, ...],
    declared: Mapping[str, tuple[str, ...]],
    plan_identity: str | None,
    caller_anchors: tuple[KnowledgeAnchorInput, ...],
    transaction_time: str,
    actor_id: str,
    opening: tuple[str, int],
) -> tuple[KnowledgeHistoryReplay, tuple[AdmittedCheck, ...]]:
    """Retain one receipt per check and append the change in one batch.

    The machine state advances through every anchor of this batch in order,
    the caller's retained inputs first and then Core's receipts, because
    ``_admit`` puts the change event first and the anchors before the protocol
    events. The three protocol events are Core's: no caller writes one, which
    is exactly what the public ``admit`` door now refuses.
    """

    state = staged.machine_state
    anchors: list[KnowledgeAnchorInput] = []
    for anchor in caller_anchors:
        preview = execute_event(staged.partial_contract, state, anchor.machine_event)
        if preview.receipt.outcome != "APPLIED":
            raise _refuse(
                PopulationAdmissionStage.ADMIT,
                "ANCHOR_REFUSED",
                "a retained input of this batch cannot enter the history's "
                f"protocol machine: {preview.receipt.refusal_code}",
                unchanged=_coordinates(history.replay()) == opening,
            )
        state = preview.state
        anchors.append(anchor)
    admitted_checks: list[AdmittedCheck] = []
    for contract, checked in zip(contracts, outcomes, strict=True):
        receipt_bytes = _receipt_bytes(contract, checked, change, plan_identity)
        receipt_id, record_receipt_id = _receipt_ids(change.change_set_id, contract)
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
        preview = execute_event(staged.partial_contract, state, receipt.machine_event)
        if preview.receipt.outcome != "APPLIED":
            raise _refuse(
                PopulationAdmissionStage.ADMIT,
                "RECEIPT_REFUSED",
                f"the receipt of check {contract.check_contract_id} cannot "
                "enter this history's protocol machine",
                unchanged=_coordinates(history.replay()) == opening,
            )
        state = preview.state
        anchors.append(receipt)
        admitted_checks.append(
            AdmittedCheck(
                check_contract_id=contract.check_contract_id,
                check_contract_identity=contract.identity,
                executor_kind=contract.executor_kind,
                outcome=checked.outcome,
                receipt_id=receipt_id,
                receipt_identity=_digest(receipt_bytes),
                record_receipt_id=record_receipt_id,
                result=dict(checked.result),
                logic_result=checked.logic_result,
            )
        )
    policy = staged.partial_contract.normative_profile.policy(
        REQUIRED_CHECK_POLICY_REFERENCE
    )
    proposal_id = f"proposal:{change.change_set_id}"
    events = [
        _declared_event(
            "CHANGE_PROPOSED",
            declared["CHANGE_PROPOSED"],
            {
                "expected_machine_state_identity": state.identity,
                "knowledge_change_set_identity": change.identity,
                "policy_id": policy.identifier,
                "policy_identity": policy.identity,
                "proposal_id": proposal_id,
            },
        )
    ]
    events.extend(
        _declared_event(
            "CHECK_RECORDED",
            declared["CHECK_RECORDED"],
            {
                "check_contract_id": admitted.check_contract_id,
                "check_contract_identity": admitted.check_contract_identity,
                "outcome": admitted.outcome,
                "policy_identity": policy.identity,
                "proposal_id": proposal_id,
                "receipt_id": admitted.record_receipt_id,
                "receipt_identity": admitted.receipt_identity,
            },
        )
        for admitted in admitted_checks
    )
    events.append(
        _declared_event(
            "VERDICT_RECORDED",
            declared["VERDICT_RECORDED"],
            {
                "decision_id": f"decision:{change.change_set_id}",
                "proposal_id": proposal_id,
            },
        )
    )
    replay = history._admit(
        anchors=tuple(anchors),
        change_set=change,
        machine_events=tuple(events),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    return replay, tuple(admitted_checks)


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

    # --- CHECK: pure. Every outcome is an engine's; no caller supplies one.
    contracts, declared, outcomes = _check_stage(
        before,
        change_set_id=f"change:{compilation.plan_id}",
        operations=compilation.operations,
        valid_time=compilation.valid_time,
        plan=canonical_plan,
        retained_source_texts=retained_source_texts,
    )

    # --- ADMIT: retention, then the change and every receipt in one batch.
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
        plan_identity = _digest(compilation.canonical_plan_bytes)
        replay, admitted_checks = _admit_checked(
            history=history,
            staged=prepared.retention_replay,
            change=change,
            contracts=contracts,
            outcomes=outcomes,
            declared=declared,
            plan_identity=plan_identity,
            caller_anchors=(),
            transaction_time=transaction_time,
            actor_id=actor_id,
            opening=opening,
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
            check=outcomes[0].logic_result,
        ) from error

    gaps = canonical_plan["gaps"]
    assert isinstance(gaps, list)
    first = admitted_checks[0]
    return PopulationAdmission(
        replay=replay,
        change_set=change,
        check=first.logic_result,
        check_contract_id=first.check_contract_id,
        check_contract_identity=first.check_contract_identity,
        plan_id=compilation.plan_id,
        plan_identity=plan_identity,
        receipt_id=first.receipt_id,
        receipt_identity=first.receipt_identity,
        gap_count=len(gaps),
        checks=tuple(admitted_checks),
    )


def check_and_admit_change_set(
    *,
    history: KnowledgeChangeHistory,
    change_set: KnowledgeChangeSet,
    transaction_time: str,
    actor_id: str,
    anchors: tuple[KnowledgeAnchorInput, ...] = (),
) -> ChangeSetAdmission:
    """Check and admit one change set the caller composed, as one operation.

    A caller that already has its operations, rather than a producer's plan
    bytes, composes the change set through ``compose_change_set`` from a
    verified read of this history. Everything after that is Core's: the
    policy's required checks are resolved through
    ``malleus.check-contract/v1``, run in the policy's own order over the state
    the change would produce, retained one receipt each, and recorded in
    ``CHANGE_PROPOSED``, one ``CHECK_RECORDED`` per check and
    ``VERDICT_RECORDED``, each carrying exactly the fields the selected machine
    declares. No parameter takes an outcome.

    ``anchors`` are retained inputs this change needs in the same batch, such
    as a source or evidence member the change set names. They are appended
    ahead of Core's receipts and they cannot be protocol events: the check and
    verdict records are Core's to write, which is what ``admit`` and
    ``admit_with_anchors`` now refuse.

    A ``CHECK`` refusal writes no byte. An ``ADMIT`` refusal admits nothing and
    reports ``ledger_unchanged``.
    """

    if not isinstance(history, KnowledgeChangeHistory):
        raise TypeError("history must be a KnowledgeChangeHistory")
    if not isinstance(change_set, KnowledgeChangeSet):
        raise TypeError("change_set must be a KnowledgeChangeSet")
    if not isinstance(anchors, tuple) or any(
        not isinstance(anchor, KnowledgeAnchorInput) for anchor in anchors
    ):
        raise TypeError("anchors must be a KnowledgeAnchorInput tuple")

    before = history.replay()
    opening = _coordinates(before)

    # --- CHECK: pure. Every outcome is an engine's; no caller supplies one.
    contracts, declared, outcomes = _check_stage(
        before,
        change_set_id=change_set.change_set_id,
        operations=change_set.operations,
        valid_time=change_set.valid_time,
    )

    # --- ADMIT: the caller's anchors, Core's receipts and the change, at once.
    try:
        replay, admitted_checks = _admit_checked(
            history=history,
            staged=before,
            change=change_set,
            contracts=contracts,
            outcomes=outcomes,
            declared=declared,
            plan_identity=None,
            caller_anchors=anchors,
            transaction_time=transaction_time,
            actor_id=actor_id,
            opening=opening,
        )
    except PopulationAdmissionRefusal:
        raise
    except KnowledgeChangeRefusal as error:
        reason = getattr(error.reason, "name", None) or str(error.reason)
        raise _refuse(
            PopulationAdmissionStage.ADMIT,
            reason,
            error.detail,
            unchanged=_coordinates(history.replay()) == opening,
            check=outcomes[0].logic_result,
        ) from error
    return ChangeSetAdmission(
        replay=replay, change_set=change_set, checks=admitted_checks
    )
