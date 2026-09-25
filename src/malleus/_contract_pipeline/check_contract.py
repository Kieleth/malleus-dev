"""One check-contract grammar Core parses, and the executors Core can run.

Until now a check contract was whatever an adopter retained. Core read the
policy's required identity, found a retained ``LogicContract`` that reproduced
it, and ran Prolog. Anything else was a document Core stored and never opened,
so the adopter ran its own program and handed Core the outcome.

``malleus.check-contract/v1`` closes that. A check contract names its executor,
and the executor kind comes from a closed set:

``PROLOG_RULES``
    Today's ``LogicContract``: a retained descriptor and its retained rule
    bytes, run by ``PrologVerifier`` in its own process, exactly as before.
    The document references the two retained records; it does not restate
    them. ``LogicContract`` closes its fields and this grammar does not
    reopen them.

``CORE_BUILTIN``
    A function Core ships, named by id and version, resolved from the closed
    registry in this module. An id the registry does not hold is refused.

There is no adopter-program kind. Architectural law 12 (``EXECUTOR_ONLY``)
forbids the unrestricted callback that would be, and an executor named by
artifact id and sha256 is exactly that callback with a digest on it.

Core also keeps reading a bare retained ``LogicContract`` pair as a
``PROLOG_RULES`` contract. That is not a second grammar: it is the form every
live Prolog check is already pinned in. Wrapping one in a v1 document would
mint a second identity for the same rules and move the policy identity, the
normative profile, the partial effective contract and every frozen coordinate
downstream of them. This step is additive, so the pinned form stands.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
from enum import Enum
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Callable, Mapping

from malleus._contract_pipeline.knowledge import (
    OPERATIONS_APPLY_ATOMICALLY,
    KnowledgeChangeHistory,
    KnowledgeChangeRefusal,
    KnowledgeHistoryReplay,
    KnowledgeOperation,
    KnowledgeValidTime,
)
from malleus.kg import KnowledgeGraph
from malleus.logic import GraphProvenance, LogicCheckResult, LogicContract, LogicError


CHECK_CONTRACT_GRAMMAR = "malleus.check-contract/v1"
"""The one check-contract grammar Core parses."""

CLOSED_OUTCOMES = ("SATISFIED", "UNKNOWN", "VIOLATED")
"""Every outcome a check may declare. The policy maps these to verdicts."""

_DOCUMENT_FIELDS = frozenset({"check_contract_id", "executor", "grammar", "outcomes"})


class CheckContractError(ValueError):
    """A check contract document, or its executor, is not one Core can run.

    ``reason`` names which of the two it is, so a caller reports the fault it
    has rather than one refusal for both: a history that retains nothing that
    reproduces the pin is a different repair from one that retains a contract
    naming an executor Core does not ship.
    """

    def __init__(self, detail: str, *, reason: str = "UNRUNNABLE_REQUIRED_CHECK") -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(detail)


class CheckExecutorKind(str, Enum):
    """The closed set of executors Core runs. No adopter-program kind exists."""

    CORE_BUILTIN = "CORE_BUILTIN"
    PROLOG_RULES = "PROLOG_RULES"


_EXECUTOR_FIELDS = {
    CheckExecutorKind.CORE_BUILTIN: frozenset(
        {"builtin_id", "builtin_version", "kind"}
    ),
    CheckExecutorKind.PROLOG_RULES: frozenset(
        {"descriptor_record_id", "kind", "rules_record_id"}
    ),
}


@dataclass(frozen=True, slots=True)
class CheckContract:
    """One parsed check contract, identified by the exact bytes it was read from."""

    check_contract_id: str
    identity: str
    executor_kind: CheckExecutorKind
    outcomes: tuple[str, ...]
    builtin_id: str | None = None
    builtin_version: str | None = None
    descriptor_record_id: str | None = None
    rules_record_id: str | None = None
    logic_contract: LogicContract | None = None

    @property
    def pinned_logic_contract(self) -> LogicContract:
        """The bound Prolog contract, or a refusal naming what is missing."""

        if self.logic_contract is None:
            raise CheckContractError(
                f"check contract {self.check_contract_id} has no bound rule layer"
            )
        return self.logic_contract


@dataclass(frozen=True, slots=True)
class CandidateChange:
    """The candidate a check reads, before any ledger coordinate exists.

    ``KnowledgeChangeHistory._apply_change`` reads exactly ``operations``,
    ``valid_time`` and ``change_set_id``; a composed ``KnowledgeChangeSet``
    additionally binds the ledger head it was composed against, which does not
    exist while the check is still deciding whether to admit anything.
    ``test_the_candidate_change_carries_every_field_the_application_reads``
    pins that attribute set by AST so a new read cannot slip past this value.
    """

    change_set_id: str
    operations: tuple[KnowledgeOperation, ...]
    valid_time: KnowledgeValidTime


@dataclass(frozen=True, slots=True)
class CheckRequest:
    """Everything an executor may read. Nothing in it is a caller's outcome."""

    replay: KnowledgeHistoryReplay
    candidate: CandidateChange
    candidate_graph: KnowledgeGraph
    provenance: GraphProvenance | None = None


@dataclass(frozen=True, slots=True)
class CheckOutcome:
    """What an executor returned, in the vocabulary the policy maps."""

    outcome: str
    detail: str = ""
    result: Mapping[str, object] = field(default_factory=dict)
    violated_rule_ids: tuple[str, ...] = ()
    witness_record_ids: tuple[str, ...] = ()
    logic_result: LogicCheckResult | None = None


def _operations_apply_atomically(
    request: CheckRequest, *, supersession_kinds: bool
) -> CheckOutcome:
    """Apply the candidate's operations to the accepted state and digest the result.

    The adopters call this ``OPERATIONS_APPLY_ATOMICALLY_TO_ACCEPTED_STATE`` and
    implement it by calling ``KnowledgeChangeHistory._apply_change`` and reading
    ``state_digest()`` off the projection. That is Core's own primitive read
    through an adopter's function, so it is Core work already.

    Version 1 refuses an operation that declares ``supersession_kind``;
    version 2 applies it (TRANSITION, REVISION). Each version's bytes and
    behaviour stay fixed, so a history keeps the one its policy recorded.
    """

    try:
        projected, _ = KnowledgeChangeHistory._apply_change(
            request.replay.graph,
            request.replay.record_history,
            request.candidate,
            supersession_kinds=supersession_kinds,
        )
    except KnowledgeChangeRefusal as error:
        return CheckOutcome(
            outcome="VIOLATED",
            detail=f"{error.reason.name}: {error.detail}",
            violated_rule_ids=("OPERATIONS_APPLY_ATOMICALLY_TO_ACCEPTED_STATE",),
            witness_record_ids=tuple(
                sorted(operation.record_id for operation in request.candidate.operations)
            ),
        )
    return CheckOutcome(
        outcome="SATISFIED",
        result=MappingProxyType({"result_state_digest": projected.state_digest()}),
    )


CORE_BUILTIN_CHECKS: Mapping[tuple[str, str], Callable[[CheckRequest], CheckOutcome]] = (
    MappingProxyType(
        {
            (OPERATIONS_APPLY_ATOMICALLY, "1"): partial(
                _operations_apply_atomically, supersession_kinds=False
            ),
            (OPERATIONS_APPLY_ATOMICALLY, "2"): partial(
                _operations_apply_atomically, supersession_kinds=True
            ),
        }
    )
)
"""The closed registry. A builtin id outside it is refused, never guessed."""


def resolve_core_builtin(
    builtin_id: object, builtin_version: object
) -> Callable[[CheckRequest], CheckOutcome]:
    """The registered function, or a refusal naming the id that is not held."""

    try:
        return CORE_BUILTIN_CHECKS[(builtin_id, builtin_version)]  # type: ignore[index]
    except (KeyError, TypeError) as error:
        raise CheckContractError(
            f"Core holds no builtin check '{builtin_id}' at version "
            f"'{builtin_version}'"
        ) from error


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _nonblank(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CheckContractError(f"check contract {label} must be a nonblank string")
    return value


def parse_check_contract(document_bytes: bytes) -> CheckContract:
    """Read one ``malleus.check-contract/v1`` document from its exact bytes.

    The identity is the digest of those bytes, so a policy requires a contract
    by naming what it will be read from and nothing else.
    """

    if type(document_bytes) is not bytes:
        raise CheckContractError("a check contract must be read from exact bytes")
    try:
        document = json.loads(document_bytes)
    except (UnicodeDecodeError, ValueError) as error:
        raise CheckContractError(f"check contract is not JSON data: {error}") from error
    if not isinstance(document, dict):
        raise CheckContractError("check contract must be a JSON object")
    if document.get("grammar") != CHECK_CONTRACT_GRAMMAR:
        raise CheckContractError(
            f"check contract grammar must be {CHECK_CONTRACT_GRAMMAR}"
        )
    if set(document) != _DOCUMENT_FIELDS:
        raise CheckContractError(
            "check contract fields must be exactly "
            + ", ".join(sorted(_DOCUMENT_FIELDS))
        )
    check_contract_id = _nonblank(document["check_contract_id"], "check_contract_id")
    outcomes = document["outcomes"]
    if (
        not isinstance(outcomes, list)
        or not outcomes
        or len(set(outcomes)) != len(outcomes)
        or any(outcome not in CLOSED_OUTCOMES for outcome in outcomes)
        or list(outcomes) != [name for name in CLOSED_OUTCOMES if name in outcomes]
    ):
        raise CheckContractError(
            "check contract outcomes must be a nonempty ordered subset of "
            + ", ".join(CLOSED_OUTCOMES)
        )
    executor = document["executor"]
    if not isinstance(executor, dict):
        raise CheckContractError("check contract executor must be an object")
    try:
        kind = CheckExecutorKind(executor.get("kind"))
    except ValueError as error:
        raise CheckContractError(
            "check contract executor kind must be one of "
            + ", ".join(sorted(member.value for member in CheckExecutorKind))
        ) from error
    if set(executor) != _EXECUTOR_FIELDS[kind]:
        raise CheckContractError(
            f"a {kind.value} executor declares exactly "
            + ", ".join(sorted(_EXECUTOR_FIELDS[kind]))
        )
    identity = _digest(document_bytes)
    if kind is CheckExecutorKind.CORE_BUILTIN:
        builtin_id = _nonblank(executor["builtin_id"], "builtin_id")
        builtin_version = _nonblank(executor["builtin_version"], "builtin_version")
        resolve_core_builtin(builtin_id, builtin_version)
        return CheckContract(
            check_contract_id=check_contract_id,
            identity=identity,
            executor_kind=kind,
            outcomes=tuple(outcomes),
            builtin_id=builtin_id,
            builtin_version=builtin_version,
        )
    return CheckContract(
        check_contract_id=check_contract_id,
        identity=identity,
        executor_kind=kind,
        outcomes=tuple(outcomes),
        descriptor_record_id=_nonblank(
            executor["descriptor_record_id"], "descriptor_record_id"
        ),
        rules_record_id=_nonblank(executor["rules_record_id"], "rules_record_id"),
    )


def _bind_prolog(
    contract: CheckContract, retained: Mapping[str, bytes]
) -> CheckContract:
    try:
        descriptor_bytes = retained[str(contract.descriptor_record_id)]
        rules_bytes = retained[str(contract.rules_record_id)]
    except KeyError as error:
        raise CheckContractError(
            f"check contract {contract.check_contract_id} names a rule layer the "
            f"history does not retain: {error.args[0]}"
        ) from error
    try:
        logic = LogicContract.from_bytes(descriptor_bytes, rules_bytes)
    except LogicError as error:
        raise CheckContractError(
            f"check contract {contract.check_contract_id} names records that are "
            f"not a pinned rule layer: {error}"
        ) from error
    return CheckContract(
        check_contract_id=contract.check_contract_id,
        identity=contract.identity,
        executor_kind=contract.executor_kind,
        outcomes=contract.outcomes,
        descriptor_record_id=contract.descriptor_record_id,
        rules_record_id=contract.rules_record_id,
        logic_contract=logic,
    )


def _pinned_logic_pair(
    retained: Mapping[str, bytes], contract_id: str, identity: str
) -> CheckContract | None:
    """Today's form: a retained descriptor and rules pair reproducing the pin.

    A descriptor declares both of these, so the scan stays linear in a history
    that retains one plan per admitted change rather than quadratic in it.
    """

    descriptors = [
        record_id
        for record_id in sorted(retained)
        if b"contract_id" in retained[record_id] and b"rules_file" in retained[record_id]
    ]
    for descriptor_id in descriptors:
        for rules_id in sorted(retained):
            if rules_id == descriptor_id:
                continue
            try:
                logic = LogicContract.from_bytes(
                    retained[descriptor_id], retained[rules_id]
                )
            except LogicError:
                continue
            if logic.contract_id == contract_id and logic.contract_hash == identity:
                return CheckContract(
                    check_contract_id=contract_id,
                    identity=identity,
                    executor_kind=CheckExecutorKind.PROLOG_RULES,
                    outcomes=CLOSED_OUTCOMES,
                    descriptor_record_id=descriptor_id,
                    rules_record_id=rules_id,
                    logic_contract=logic,
                )
    return None


def _claims_grammar(source: bytes) -> bool:
    """Whether these bytes present themselves as a check contract at all.

    Retained inputs hold plans, sources, ontologies and rule files too. Only a
    document that names this grammar is read as one, so a fault in it refuses
    instead of being passed over as though the history retained nothing.
    """

    try:
        document = json.loads(source)
    except (UnicodeDecodeError, ValueError):
        return False
    return (
        isinstance(document, dict)
        and document.get("grammar") == CHECK_CONTRACT_GRAMMAR
    )


def resolve_check_contract(
    replay: KnowledgeHistoryReplay, contract_id: str, identity: str
) -> CheckContract:
    """The contract this history retains for one required check, bound to run.

    A ``malleus.check-contract/v1`` document retained under the required
    identity wins. Otherwise the retained descriptor and rules pair that
    reproduces the pin is read as a ``PROLOG_RULES`` contract, which is the
    form every check pinned before this grammar existed carries.

    Raises ``CheckContractError`` when the history retains neither, or when the
    document it retains names an executor Core cannot run.
    """

    retained = {
        member.record_id: bytes(member.content) for member in replay.retained_inputs
    }
    for record_id in sorted(retained):
        if _digest(retained[record_id]) != identity or not _claims_grammar(
            retained[record_id]
        ):
            continue
        # The document claims this grammar under the required identity, so a
        # fault in it is reported rather than read as an absent contract.
        parsed = parse_check_contract(retained[record_id])
        if parsed.check_contract_id != contract_id:
            raise CheckContractError(
                f"the check contract retained at {identity} names "
                f"{parsed.check_contract_id} and this history requires "
                f"{contract_id}"
            )
        if parsed.executor_kind is CheckExecutorKind.PROLOG_RULES:
            return _bind_prolog(parsed, retained)
        return parsed
    pinned = _pinned_logic_pair(retained, contract_id, identity)
    if pinned is not None:
        return pinned
    raise CheckContractError(
        f"this history requires check contract {contract_id} at {identity} and "
        "retains no check contract document and no descriptor and rules pair "
        "that reproduces it",
        reason="CHECK_CONTRACT_NOT_RETAINED",
    )


__all__ = (
    "CHECK_CONTRACT_GRAMMAR",
    "CLOSED_OUTCOMES",
    "CORE_BUILTIN_CHECKS",
    "CandidateChange",
    "CheckContract",
    "CheckContractError",
    "CheckExecutorKind",
    "CheckOutcome",
    "CheckRequest",
    "OPERATIONS_APPLY_ATOMICALLY",
    "parse_check_contract",
    "resolve_check_contract",
    "resolve_core_builtin",
)
