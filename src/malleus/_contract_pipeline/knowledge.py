"""Private single-ledger knowledge-change experiment."""

from __future__ import annotations

from base64 import b64decode, b64encode
from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum, auto
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Callable, Mapping

from malleus._contract_pipeline.machine import (
    MachineReceipt,
    MachineState,
    PartialEffectiveContract,
    execute_event,
)
from malleus._contract_pipeline.view import (
    ContractView,
    load_validated_contract_artifact,
)
from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ledger import GENESIS, JsonlLedger, LedgerError, content_digest


_CHANGE_GRAMMAR = "malleus.knowledge-change-set/private-v0"
_BINDING_GRAMMAR = "malleus.knowledge-history-binding/private-v1"
_CONTRACT_KIND = "PRIVATE_PARTIAL_EFFECTIVE_CONTRACT_V0"
_CHANGE_EVENT = "KNOWLEDGE_CHANGE_SET_RETAINED"
_HEAD_ROLES = frozenset(
    {
        "KNOWLEDGE_HISTORY_BINDING",
        "PARTIAL_EFFECTIVE_CONTRACT",
        "RETAINED_EVIDENCE",
        "RETAINED_SOURCE",
        "SOURCE_ARTIFACT",
        "VALIDATED_CONTRACT",
    }
)
_REOPEN_ROLES = frozenset(
    {
        "KNOWLEDGE_HISTORY_BINDING",
        "PARTIAL_EFFECTIVE_CONTRACT",
        "VALIDATED_CONTRACT",
    }
)
_EVIDENCE_ROLES = frozenset({"RETAINED_EVIDENCE", "VALIDATED_CONTRACT"})
_VERDICTS = frozenset({"ACCEPT", "CONTEST", "DEFER", "REJECT"})
_DIGEST_PREFIX = "sha256:"
_HEX = frozenset("0123456789abcdef")
_ROOT_FIELDS = frozenset(
    {
        "base_acceptance_head",
        "base_accepted_state_digest",
        "base_ledger_event_count",
        "base_ledger_head",
        "base_materialization_head",
        "change_set_id",
        "contract_identity",
        "contract_kind",
        "evidence",
        "grammar",
        "operations",
        "sources",
        "supersedes",
        "valid_time",
    }
)
_ENTITY_OPERATION_FIELDS = frozenset(
    {
        "depends_on",
        "operation_id",
        "operation_type",
        "ordinal",
        "properties",
        "record_id",
        "record_type",
    }
)
_RELATION_OPERATION_FIELDS = _ENTITY_OPERATION_FIELDS | frozenset(
    {"source_id", "target_id"}
)
_SUPERSESSION_FIELD = "supersedes_record_id"
_ANCHOR_FIELDS = frozenset(
    {
        "machine_payload",
        "media_type",
        "record_id",
        "retained_bytes_base64",
        "retained_sha256",
        "role",
    }
)
_CHANGE_FIELDS = frozenset(
    {"change_set_bytes_base64", "change_set_id", "change_set_identity"}
)


class KnowledgeChangeRefusalReason(Enum):
    MALFORMED_CHANGE_SET = auto()
    NONCANONICAL_CHANGE_SET = auto()
    UNSUPPORTED_GRAMMAR = auto()
    UNSUPPORTED_CONTRACT_KIND = auto()
    CYCLIC_OPERATION_DEPENDENCY = auto()
    IDENTITY_MISMATCH = auto()
    RETAINED_BYTES_MISMATCH = auto()
    MALFORMED_BINDING = auto()
    NONCANONICAL_BINDING = auto()
    MALFORMED_HISTORY = auto()
    INCOMPLETE_ADMISSION = auto()
    STALE_BASE = auto()
    UNRETAINED_INPUT = auto()
    UNKNOWN_SUPERSESSION = auto()
    PROTOCOL_REFUSAL = auto()
    REJECTED_CHANGE = auto()
    STRUCTURAL_REFUSAL = auto()


class KnowledgeChangeRefusal(ValueError):
    def __init__(self, reason: KnowledgeChangeRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


def _refuse(
    reason: KnowledgeChangeRefusalReason, detail: str
) -> KnowledgeChangeRefusal:
    return KnowledgeChangeRefusal(reason, detail)


def _digest(source: bytes) -> str:
    return _DIGEST_PREFIX + sha256(source).hexdigest()


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and value.startswith(_DIGEST_PREFIX)
        and len(value) == 71
        and all(character in _HEX for character in value[7:])
    )


def _is_head(value: object) -> bool:
    return value == GENESIS or _is_digest(value)


def _canonical(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, UnicodeError, ValueError) as error:
        raise _refuse(
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
            "value is not canonical JSON",
        ) from error


def _decode(
    source: bytes,
    *,
    malformed: KnowledgeChangeRefusalReason,
    noncanonical: KnowledgeChangeRefusalReason,
) -> dict[str, object]:
    if type(source) is not bytes:
        raise _refuse(malformed, "artifact input must be exact bytes")

    def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
        answer: dict[str, object] = {}
        for key, value in pairs:
            if key in answer:
                raise ValueError(f"duplicate JSON key: {key}")
            answer[key] = value
        return answer

    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON constant: {value}")

    try:
        value = json.loads(
            source.decode("utf-8"),
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise _refuse(malformed, "artifact is not closed canonical JSON") from error
    if not isinstance(value, dict):
        raise _refuse(malformed, "artifact root must be an object")
    if _canonical(value) != source:
        raise _refuse(noncanonical, "artifact bytes are not canonical")
    return value


def _freeze(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _text(value: object, detail: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(detail)
    return value


def _digest_value(value: object, detail: str) -> str:
    if not _is_digest(value):
        raise ValueError(detail)
    assert isinstance(value, str)
    return value


def _head(value: object, detail: str) -> str:
    if not _is_head(value):
        raise ValueError(detail)
    assert isinstance(value, str)
    return value


def _object(value: object, detail: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(detail)
    return value


def _array(value: object, detail: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(detail)
    return value


def _exact(value: Mapping[str, object], fields: frozenset[str], detail: str) -> None:
    if set(value) != fields:
        raise ValueError(detail)


def _aware_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("instant valid time must carry a timezone")
    return parsed


@dataclass(frozen=True, slots=True)
class KnowledgeValidTime:
    kind: str
    value: str


@dataclass(frozen=True, slots=True)
class KnowledgeOperation:
    ordinal: int
    operation_id: str
    operation_type: str
    record_type: str
    record_id: str
    properties: Mapping[str, object]
    depends_on: tuple[str, ...]
    source_id: str | None = None
    target_id: str | None = None
    supersedes_record_id: str | None = None


def _closures(
    raw: object,
    *,
    id_field: str,
    label: str,
) -> tuple[tuple[str, str], ...]:
    values: list[tuple[str, str]] = []
    for member in _array(raw, f"{label} closure must be an array"):
        item = _object(member, f"{label} closure member must be an object")
        _exact(item, frozenset({id_field, "sha256"}), f"{label} member is not exact")
        values.append(
            (
                _text(item[id_field], f"{label} ID is required"),
                _digest_value(item["sha256"], f"{label} digest is required"),
            )
        )
    if not values or len(values) != len({identifier for identifier, _ in values}):
        raise ValueError(f"{label} closure must be nonempty and unique")
    return tuple(values)


def _operation(raw: object, expected_ordinal: int) -> KnowledgeOperation:
    value = _object(raw, "operation must be an object")
    operation_type = _text(value.get("operation_type"), "operation type is required")
    required_fields = (
        _ENTITY_OPERATION_FIELDS
        if operation_type == "CREATE_ENTITY"
        else _RELATION_OPERATION_FIELDS
        if operation_type == "CREATE_RELATION"
        else frozenset()
    )
    if not required_fields:
        raise ValueError("operation type is unsupported")
    if set(value) not in (
        required_fields,
        required_fields | frozenset({_SUPERSESSION_FIELD}),
    ):
        raise ValueError("operation fields are not closed")
    ordinal = value["ordinal"]
    if type(ordinal) is not int or ordinal != expected_ordinal:
        raise ValueError("operation ordinals must be contiguous and zero-based")
    properties = _object(value["properties"], "operation properties must be an object")
    if not all(isinstance(key, str) for key in properties):
        raise ValueError("operation property names must be strings")
    dependencies = tuple(
        _text(item, "operation dependency must be an ID")
        for item in _array(
            value["depends_on"], "operation dependencies must be an array"
        )
    )
    if len(dependencies) != len(set(dependencies)):
        raise ValueError("operation dependencies must be unique")
    source_id = None
    target_id = None
    if operation_type == "CREATE_RELATION":
        source_id = _text(value["source_id"], "relation source ID is required")
        target_id = _text(value["target_id"], "relation target ID is required")
    supersedes_record_id = (
        _text(value[_SUPERSESSION_FIELD], "superseded record ID is required")
        if _SUPERSESSION_FIELD in value
        else None
    )
    return KnowledgeOperation(
        ordinal=ordinal,
        operation_id=_text(value["operation_id"], "operation ID is required"),
        operation_type=operation_type,
        record_type=_text(value["record_type"], "record type is required"),
        record_id=_text(value["record_id"], "record ID is required"),
        properties=_freeze(dict(properties)),
        depends_on=dependencies,
        source_id=source_id,
        target_id=target_id,
        supersedes_record_id=supersedes_record_id,
    )


def _validate_dependencies(operations: tuple[KnowledgeOperation, ...]) -> None:
    names = {operation.operation_id for operation in operations}
    if len(names) != len(operations):
        raise ValueError("operation IDs must be unique")
    if len({operation.record_id for operation in operations}) != len(operations):
        raise ValueError("record IDs must be globally unique inside a change set")
    for operation in operations:
        if not set(operation.depends_on).issubset(names):
            raise ValueError("operation dependency references an unknown operation")

    visiting: set[str] = set()
    visited: set[str] = set()
    dependencies = {
        operation.operation_id: operation.depends_on for operation in operations
    }

    def visit(name: str) -> None:
        if name in visiting:
            raise _refuse(
                KnowledgeChangeRefusalReason.CYCLIC_OPERATION_DEPENDENCY,
                "operation dependency cycle",
            )
        if name in visited:
            return
        visiting.add(name)
        for dependency in dependencies[name]:
            visit(dependency)
        visiting.remove(name)
        visited.add(name)

    for name in dependencies:
        visit(name)
    positions = {operation.operation_id: operation.ordinal for operation in operations}
    if any(
        positions[dependency] >= operation.ordinal
        for operation in operations
        for dependency in operation.depends_on
    ):
        raise ValueError("operation dependencies must precede their consumers")


@dataclass(frozen=True, slots=True)
class KnowledgeChangeSet:
    canonical_bytes: bytes
    identity: str
    data: Mapping[str, object]
    change_set_id: str
    contract_kind: str
    contract_identity: str
    base_ledger_head: str
    base_ledger_event_count: int
    base_acceptance_head: str
    base_materialization_head: str
    base_accepted_state_digest: str
    sources: tuple[tuple[str, str], ...]
    evidence: tuple[tuple[str, str], ...]
    operations: tuple[KnowledgeOperation, ...]
    valid_time: KnowledgeValidTime
    supersedes: tuple[str, ...]

    @classmethod
    def from_bytes(cls, source: bytes) -> KnowledgeChangeSet:
        data = _decode(
            source,
            malformed=KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
            noncanonical=KnowledgeChangeRefusalReason.NONCANONICAL_CHANGE_SET,
        )
        try:
            _exact(data, _ROOT_FIELDS, "change-set fields are not closed")
            if data["grammar"] != _CHANGE_GRAMMAR:
                raise _refuse(
                    KnowledgeChangeRefusalReason.UNSUPPORTED_GRAMMAR,
                    "unsupported change-set grammar",
                )
            if data["contract_kind"] != _CONTRACT_KIND:
                raise _refuse(
                    KnowledgeChangeRefusalReason.UNSUPPORTED_CONTRACT_KIND,
                    "unsupported effective-contract kind",
                )
            count = data["base_ledger_event_count"]
            if type(count) is not int or count < 0:
                raise ValueError(
                    "base ledger event count must be a nonnegative integer"
                )
            ledger_head = _head(data["base_ledger_head"], "base ledger head is invalid")
            if (count == 0) != (ledger_head == GENESIS):
                raise ValueError("base ledger head and count disagree")
            valid_time_data = _object(
                data["valid_time"], "valid time must be an object"
            )
            _exact(
                valid_time_data,
                frozenset({"kind", "value"}),
                "valid time fields are not closed",
            )
            valid_time = KnowledgeValidTime(
                kind=_text(valid_time_data["kind"], "valid-time kind is required"),
                value=_text(valid_time_data["value"], "valid-time value is required"),
            )
            if valid_time.kind not in {"INSTANT", "ORDER_ONLY"}:
                raise ValueError("valid-time kind is unsupported")
            if valid_time.kind == "INSTANT":
                _aware_time(valid_time.value)
            operations = tuple(
                _operation(raw, ordinal)
                for ordinal, raw in enumerate(
                    _array(data["operations"], "operations must be an array")
                )
            )
            if not operations:
                raise ValueError("a change set must contain an operation")
            _validate_dependencies(operations)
            supersedes = tuple(
                _text(item, "supersession reference must be an ID")
                for item in _array(data["supersedes"], "supersedes must be an array")
            )
            if len(supersedes) != len(set(supersedes)):
                raise ValueError("supersession references must be unique")
            sources = _closures(data["sources"], id_field="source_id", label="source")
            evidence = _closures(
                data["evidence"], id_field="evidence_id", label="evidence"
            )
            return cls(
                canonical_bytes=source,
                identity=_digest(source),
                data=_freeze(data),
                change_set_id=_text(data["change_set_id"], "change-set ID is required"),
                contract_kind=_CONTRACT_KIND,
                contract_identity=_digest_value(
                    data["contract_identity"], "contract identity is required"
                ),
                base_ledger_head=ledger_head,
                base_ledger_event_count=count,
                base_acceptance_head=_head(
                    data["base_acceptance_head"], "base acceptance head is invalid"
                ),
                base_materialization_head=_head(
                    data["base_materialization_head"],
                    "base materialization head is invalid",
                ),
                base_accepted_state_digest=_digest_value(
                    data["base_accepted_state_digest"],
                    "base accepted-state digest is required",
                ),
                sources=sources,
                evidence=evidence,
                operations=operations,
                valid_time=valid_time,
                supersedes=supersedes,
            )
        except KnowledgeChangeRefusal:
            raise
        except (KeyError, TypeError, ValueError) as error:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
                str(error),
            ) from error


@dataclass(frozen=True, slots=True)
class KnowledgeRecordHistory:
    operation: KnowledgeOperation
    change_set_id: str
    valid_from: KnowledgeValidTime
    valid_to: KnowledgeValidTime | None
    supersedes_record_id: str | None
    superseded_by: str | None


@dataclass(frozen=True, slots=True)
class KnowledgeChangeHistoryBinding:
    canonical_bytes: bytes
    identity: str
    data: Mapping[str, object]

    @classmethod
    def from_bytes(cls, source: bytes) -> KnowledgeChangeHistoryBinding:
        data = _decode(
            source,
            malformed=KnowledgeChangeRefusalReason.MALFORMED_BINDING,
            noncanonical=KnowledgeChangeRefusalReason.NONCANONICAL_BINDING,
        )
        try:
            _exact(
                data,
                frozenset(
                    {
                        "accept_verdict",
                        "decision",
                        "grammar",
                        "proposal",
                        "retention_events",
                    }
                ),
                "history binding fields are not closed",
            )
            if data["grammar"] != _BINDING_GRAMMAR:
                raise ValueError("history binding grammar is unsupported")
            if data["accept_verdict"] not in _VERDICTS:
                raise ValueError("accepted verdict is unsupported")
            proposal = _object(data["proposal"], "proposal binding must be an object")
            _exact(
                proposal,
                frozenset(
                    {
                        "change_set_identity_field",
                        "event_type",
                        "proposal_id_field",
                        "record_type",
                    }
                ),
                "proposal binding is not closed",
            )
            decision = _object(data["decision"], "decision binding must be an object")
            _exact(
                decision,
                frozenset(
                    {
                        "event_type",
                        "proposal_id_field",
                        "record_type",
                        "verdict_field",
                    }
                ),
                "decision binding is not closed",
            )
            retention = _object(
                data["retention_events"],
                "retention event bindings must be an object",
            )
            if not retention:
                raise ValueError("at least one retention event is required")
            for event_type, raw in retention.items():
                _text(event_type, "retention event name is required")
                fields = _object(raw, "retention event binding must be an object")
                _exact(
                    fields,
                    frozenset({"allowed_roles", "identity_field", "record_id_field"}),
                    "retention event binding is not closed",
                )
                for field in (fields["identity_field"], fields["record_id_field"]):
                    _text(field, "retention event field name is required")
                allowed_roles = fields["allowed_roles"]
                if not isinstance(allowed_roles, list) or not allowed_roles:
                    raise ValueError("retention event allowed roles must be nonempty")
                for role in allowed_roles:
                    _text(role, "retention event allowed role is required")
                    if role not in _HEAD_ROLES:
                        raise ValueError(
                            f"retention event allowed role is unsupported: {role}"
                        )
                if allowed_roles != sorted(set(allowed_roles)):
                    raise ValueError(
                        "retention event allowed roles must be sorted and unique"
                    )
            for group in (proposal, decision):
                for field in group.values():
                    _text(field, "history binding field is required")
        except (KeyError, TypeError, ValueError) as error:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_BINDING,
                str(error),
            ) from error
        return cls(source, _digest(source), _freeze(data))


def _validated_change(value: object) -> KnowledgeChangeSet:
    if not isinstance(value, KnowledgeChangeSet):
        raise _refuse(
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
            "a KnowledgeChangeSet value is required",
        )
    try:
        rebuilt = KnowledgeChangeSet.from_bytes(value.canonical_bytes)
    except KnowledgeChangeRefusal as error:
        raise _refuse(
            KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
            "change-set fields cannot be reproduced from canonical bytes",
        ) from error
    if rebuilt != value:
        raise _refuse(
            KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
            "change-set fields do not match canonical bytes",
        )
    return rebuilt


def _validated_binding(value: object) -> KnowledgeChangeHistoryBinding:
    if not isinstance(value, KnowledgeChangeHistoryBinding):
        raise _refuse(
            KnowledgeChangeRefusalReason.MALFORMED_BINDING,
            "a history binding is required",
        )
    try:
        rebuilt = KnowledgeChangeHistoryBinding.from_bytes(value.canonical_bytes)
    except KnowledgeChangeRefusal as error:
        raise _refuse(
            KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
            "history binding cannot be reproduced from canonical bytes",
        ) from error
    if rebuilt != value:
        raise _refuse(
            KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
            "history binding fields do not match canonical bytes",
        )
    return rebuilt


@dataclass(frozen=True, slots=True)
class KnowledgeHistoryReceipt:
    canonical_bytes: bytes
    identity: str


@dataclass(frozen=True, slots=True)
class KnowledgeAnchorResult:
    machine_receipt: MachineReceipt


@dataclass(frozen=True, slots=True)
class KnowledgeAnchorInput:
    machine_event: bytes
    retained_bytes: bytes
    media_type: str
    role: str


@dataclass(frozen=True, slots=True)
class KnowledgeRetainedInput:
    record_id: str
    content: bytes
    identity: str
    media_type: str
    role: str


@dataclass(frozen=True, slots=True)
class KnowledgeHistoryReplay:
    graph: KnowledgeGraph
    machine_state: MachineState
    ledger_head: str
    ledger_event_count: int
    acceptance_head: str
    materialization_head: str
    receipt: KnowledgeHistoryReceipt
    partial_contract: PartialEffectiveContract
    contract_view: ContractView
    binding: KnowledgeChangeHistoryBinding
    change_sets: tuple[KnowledgeChangeSet, ...]
    _retained: Mapping[str, KnowledgeRetainedInput]
    _machine_receipts: tuple[MachineReceipt, ...]
    _record_history: Mapping[str, KnowledgeRecordHistory]
    _graphs_by_change: Mapping[str, KnowledgeGraph]

    @property
    def retained_inputs(self) -> tuple[KnowledgeRetainedInput, ...]:
        return tuple(self._retained.values())

    def retained_bytes(self, record_id: str) -> bytes:
        try:
            return bytes(self._retained[record_id].content)
        except KeyError as error:
            raise KeyError(f"unknown retained record: {record_id}") from error

    @property
    def record_history(self) -> Mapping[str, KnowledgeRecordHistory]:
        return MappingProxyType(dict(self._record_history))

    def graph_at_change(self, change_set_id: str) -> KnowledgeGraph:
        try:
            graph = self._graphs_by_change[change_set_id]
        except KeyError as error:
            raise KeyError(f"unknown accepted change: {change_set_id}") from error
        return graph.state_projection()


def _decode_b64(value: object, detail: str) -> bytes:
    if not isinstance(value, str):
        raise _refuse(KnowledgeChangeRefusalReason.MALFORMED_HISTORY, detail)
    try:
        return b64decode(value.encode("ascii"), validate=True)
    except (UnicodeError, ValueError) as error:
        raise _refuse(KnowledgeChangeRefusalReason.MALFORMED_HISTORY, detail) from error


def _event_object(source: bytes) -> tuple[str, dict[str, object]]:
    data = _decode(
        source,
        malformed=KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
        noncanonical=KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
    )
    if set(data) != {"event_type", "payload"}:
        raise _refuse(
            KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
            "machine event fields are not closed",
        )
    event_type = data["event_type"]
    payload = data["payload"]
    if (
        not isinstance(event_type, str)
        or not event_type
        or not isinstance(payload, dict)
    ):
        raise _refuse(
            KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
            "machine event type and payload are required",
        )
    return event_type, payload


def _history_receipt(
    *,
    contract: PartialEffectiveContract,
    binding: KnowledgeChangeHistoryBinding,
    machine_state: MachineState,
    ledger_head: str,
    ledger_count: int,
    graph: KnowledgeGraph,
    retained: Mapping[str, KnowledgeRetainedInput],
    accepted_changes: tuple[KnowledgeChangeSet, ...],
) -> KnowledgeHistoryReceipt:
    policies = contract.normative_profile.policy_programs
    if len(policies) != 1:
        raise _refuse(
            KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
            "this private history requires one policy program",
        )
    snapshot = graph.snapshot()
    change_identity_field = binding.data["proposal"]["change_set_identity_field"]
    source = _canonical(
        {
            "contract_identity": contract.identity,
            "graph_state_digest": graph.state_digest(),
            "history_binding_identity": binding.identity,
            change_identity_field: (
                accepted_changes[-1].identity if accepted_changes else GENESIS
            ),
            "ledger_event_count": ledger_count,
            "ledger_head": ledger_head,
            "machine_identity": contract.normative_profile.protocol_machine_program.identity,
            "machine_state_identity": machine_state.identity,
            "policy_identity": policies[0][1].identity,
            "queries": {
                "entities": snapshot["nodes"],
                "relations": snapshot["relations"],
            },
            "source_identities": {
                record_id: member.identity
                for record_id, member in sorted(retained.items())
                if member.role == "RETAINED_SOURCE"
            },
            "validated_fact_set_sha256": contract.validated_fact_set_sha256,
        }
    )
    return KnowledgeHistoryReceipt(source, _digest(source))


class KnowledgeChangeHistory:
    def __init__(
        self,
        path: str | Path,
        *,
        partial_contract: PartialEffectiveContract,
        contract_view: ContractView,
        binding: KnowledgeChangeHistoryBinding,
    ) -> None:
        if not isinstance(partial_contract, PartialEffectiveContract):
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "partial effective contract is required",
            )
        rebuilt_contract = PartialEffectiveContract.from_bytes(
            partial_contract.canonical_bytes
        )
        if rebuilt_contract != partial_contract:
            raise _refuse(
                KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
                "partial effective contract fields do not match its bytes",
            )
        if not isinstance(contract_view, ContractView):
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "validated contract view is required",
            )
        fact_set = _DIGEST_PREFIX + contract_view.content_hash()
        if fact_set != partial_contract.validated_fact_set_sha256:
            raise _refuse(
                KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
                "contract view and partial effective contract disagree",
            )
        self.path = Path(path)
        self.partial_contract = rebuilt_contract
        self.contract_view = contract_view
        self.binding = _validated_binding(binding)
        self._ledger = JsonlLedger(self.path, fact_set)

    def _bootstrap_bytes(self, role: object) -> bytes | None:
        return {
            "VALIDATED_CONTRACT": self.contract_view.artifact_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT": self.partial_contract.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING": self.binding.canonical_bytes,
        }.get(role)

    def _append(
        self,
        entries: tuple[Mapping[str, object], ...] | list[dict[str, object]],
        *,
        validate: Callable[[list[dict[str, object]]], None],
    ) -> None:
        try:
            self._ledger.append_many(entries, validate=validate)
        except LedgerError as error:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                f"ledger refused the candidate batch: {error}",
            ) from error

    @classmethod
    def reopen(cls, path: str | Path) -> KnowledgeChangeHistory:
        ledger_path = Path(path)
        try:
            raw = ledger_path.read_bytes()
            first = json.loads(raw.splitlines()[0])
            ontology_hash = first["ontology_hash"]
            events = JsonlLedger(ledger_path, ontology_hash).read()
        except (
            IndexError,
            KeyError,
            OSError,
            TypeError,
            ValueError,
            LedgerError,
        ) as error:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "ledger cannot supply its retained bootstrap artifacts",
            ) from error
        retained_by_role: dict[str, bytes] = {}
        for event in events:
            payload = event["payload"]
            if set(payload) != _ANCHOR_FIELDS:
                continue
            role = payload["role"]
            if role not in _REOPEN_ROLES:
                continue
            if role in retained_by_role:
                raise _refuse(
                    KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                    f"ledger contains duplicate bootstrap role: {role}",
                )
            retained_by_role[role] = _decode_b64(
                payload["retained_bytes_base64"],
                f"retained {role} bytes are malformed",
            )
        if set(retained_by_role) != _REOPEN_ROLES:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "ledger lacks one exact retained bootstrap artifact",
            )
        try:
            view = load_validated_contract_artifact(
                retained_by_role["VALIDATED_CONTRACT"]
            )
            contract = PartialEffectiveContract.from_bytes(
                retained_by_role["PARTIAL_EFFECTIVE_CONTRACT"]
            )
            binding = KnowledgeChangeHistoryBinding.from_bytes(
                retained_by_role["KNOWLEDGE_HISTORY_BINDING"]
            )
        except ValueError as error:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "retained bootstrap artifact is invalid",
            ) from error
        history = cls(
            ledger_path,
            partial_contract=contract,
            contract_view=view,
            binding=binding,
        )
        history.replay()
        return history

    def _anchor_entry(
        self,
        *,
        anchor: KnowledgeAnchorInput,
        transaction_time: str,
        actor_id: str,
    ) -> dict[str, object]:
        if not isinstance(anchor, KnowledgeAnchorInput):
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "anchor batch members must be KnowledgeAnchorInput values",
            )
        machine_event = anchor.machine_event
        retained_bytes = anchor.retained_bytes
        media_type = anchor.media_type
        role = anchor.role
        if type(retained_bytes) is not bytes:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "retained input must be exact bytes",
            )
        if role not in _HEAD_ROLES:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "retained input role is unsupported",
            )
        if not isinstance(media_type, str) or not media_type:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "retained input media type is required",
            )
        event_type, machine_payload = _event_object(machine_event)
        retention = self.binding.data["retention_events"]
        if event_type not in retention:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "machine event is not declared as a retention event",
            )
        fields = retention[event_type]
        if role not in fields["allowed_roles"]:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                f"machine event cannot retain role: {role}",
            )
        record_id = machine_payload.get(fields["record_id_field"])
        declared_identity = machine_payload.get(fields["identity_field"])
        actual_identity = _digest(retained_bytes)
        expected_bootstrap = self._bootstrap_bytes(role)
        if expected_bootstrap is not None and retained_bytes != expected_bootstrap:
            raise _refuse(
                KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
                f"retained {role} bytes do not match the active history",
            )
        if not isinstance(record_id, str) or not record_id:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "retention event lacks its declared record ID",
            )
        if declared_identity != actual_identity:
            raise _refuse(
                KnowledgeChangeRefusalReason.RETAINED_BYTES_MISMATCH,
                "retained bytes do not match the machine event identity",
            )
        return {
            "actor_id": actor_id,
            "event_id": f"anchor:{role}:{record_id}",
            "event_type": event_type,
            "payload": {
                "machine_payload": machine_payload,
                "media_type": media_type,
                "record_id": record_id,
                "retained_bytes_base64": b64encode(retained_bytes).decode("ascii"),
                "retained_sha256": actual_identity,
                "role": role,
            },
            "transaction_time": transaction_time,
        }

    def append_anchors(
        self,
        *,
        anchors: tuple[KnowledgeAnchorInput, ...],
        transaction_time: str,
        actor_id: str,
    ) -> tuple[KnowledgeAnchorResult, ...]:
        if not isinstance(anchors, tuple) or not anchors:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "an ordered nonempty anchor tuple is required",
            )
        entries = tuple(
            self._anchor_entry(
                anchor=anchor,
                transaction_time=transaction_time,
                actor_id=actor_id,
            )
            for anchor in anchors
        )
        self._append(entries, validate=self._validate_candidate)
        replay = self.replay()
        return tuple(
            KnowledgeAnchorResult(receipt)
            for receipt in replay._machine_receipts[-len(anchors) :]
        )

    def append_anchor(
        self,
        *,
        machine_event: bytes,
        retained_bytes: bytes,
        media_type: str,
        role: str,
        transaction_time: str,
        actor_id: str,
    ) -> KnowledgeAnchorResult:
        return self.append_anchors(
            anchors=(
                KnowledgeAnchorInput(
                    machine_event=machine_event,
                    retained_bytes=retained_bytes,
                    media_type=media_type,
                    role=role,
                ),
            ),
            transaction_time=transaction_time,
            actor_id=actor_id,
        )[0]

    def compose_change_set(
        self,
        *,
        change_set_id: str,
        source_record_ids: tuple[str, ...],
        evidence_record_ids: tuple[str, ...],
        operations: tuple[KnowledgeOperation, ...],
        valid_time: KnowledgeValidTime,
        supersedes: tuple[str, ...],
    ) -> KnowledgeChangeSet:
        """Compose one private change set against the exact current history."""

        if not isinstance(change_set_id, str) or not change_set_id:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
                "change-set ID is required",
            )
        tuple_inputs = (
            (source_record_ids, "source record IDs"),
            (evidence_record_ids, "evidence record IDs"),
            (operations, "operations"),
            (supersedes, "supersession references"),
        )
        for values, label in tuple_inputs:
            if not isinstance(values, tuple):
                raise _refuse(
                    KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
                    f"{label} must be an ordered tuple",
                )
        for values, label in (
            (source_record_ids, "source record ID"),
            (evidence_record_ids, "evidence record ID"),
            (supersedes, "supersession reference"),
        ):
            if any(not isinstance(value, str) or not value for value in values):
                raise _refuse(
                    KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
                    f"{label} must be a nonempty string",
                )
        if any(
            not isinstance(operation, KnowledgeOperation) for operation in operations
        ):
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
                "operations must contain only KnowledgeOperation values",
            )
        if not isinstance(valid_time, KnowledgeValidTime):
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
                "valid time must be a KnowledgeValidTime value",
            )

        replay = self.replay()

        def closure(
            record_ids: tuple[str, ...],
            *,
            roles: frozenset[str],
            id_field: str,
            label: str,
        ) -> list[dict[str, str]]:
            members: list[dict[str, str]] = []
            for record_id in record_ids:
                retained = replay._retained.get(record_id)
                if retained is None or retained.role not in roles:
                    raise _refuse(
                        KnowledgeChangeRefusalReason.UNRETAINED_INPUT,
                        f"{label} {record_id} is not retained with an accepted role",
                    )
                members.append({id_field: record_id, "sha256": retained.identity})
            return members

        operation_payloads: list[dict[str, object]] = []
        for operation in operations:
            payload: dict[str, object] = {
                "depends_on": list(operation.depends_on),
                "operation_id": operation.operation_id,
                "operation_type": operation.operation_type,
                "ordinal": operation.ordinal,
                "properties": _thaw(operation.properties),
                "record_id": operation.record_id,
                "record_type": operation.record_type,
            }
            if (
                operation.operation_type == "CREATE_RELATION"
                or operation.source_id is not None
                or operation.target_id is not None
            ):
                payload["source_id"] = operation.source_id
                payload["target_id"] = operation.target_id
            if operation.supersedes_record_id is not None:
                payload[_SUPERSESSION_FIELD] = operation.supersedes_record_id
            operation_payloads.append(payload)

        return KnowledgeChangeSet.from_bytes(
            _canonical(
                {
                    "base_acceptance_head": replay.acceptance_head,
                    "base_accepted_state_digest": replay.graph.state_digest(),
                    "base_ledger_event_count": replay.ledger_event_count,
                    "base_ledger_head": replay.ledger_head,
                    "base_materialization_head": replay.materialization_head,
                    "change_set_id": change_set_id,
                    "contract_identity": self.partial_contract.identity,
                    "contract_kind": _CONTRACT_KIND,
                    "evidence": closure(
                        evidence_record_ids,
                        roles=_EVIDENCE_ROLES,
                        id_field="evidence_id",
                        label="evidence",
                    ),
                    "grammar": _CHANGE_GRAMMAR,
                    "operations": operation_payloads,
                    "sources": closure(
                        source_record_ids,
                        roles=frozenset({"RETAINED_SOURCE"}),
                        id_field="source_id",
                        label="source",
                    ),
                    "supersedes": list(supersedes),
                    "valid_time": {
                        "kind": valid_time.kind,
                        "value": valid_time.value,
                    },
                }
            )
        )

    def admit(
        self,
        *,
        change_set: KnowledgeChangeSet,
        machine_events: tuple[bytes, ...],
        transaction_time: str,
        actor_id: str,
    ) -> KnowledgeHistoryReplay:
        return self._admit(
            anchors=(),
            change_set=change_set,
            machine_events=machine_events,
            transaction_time=transaction_time,
            actor_id=actor_id,
        )

    def admit_with_anchors(
        self,
        *,
        anchors: tuple[KnowledgeAnchorInput, ...],
        change_set: KnowledgeChangeSet,
        machine_events: tuple[bytes, ...],
        transaction_time: str,
        actor_id: str,
    ) -> KnowledgeHistoryReplay:
        """Retain protocol artifacts and admit one change in one ledger batch.

        The change-set event precedes these anchors, so every source and
        evidence member named by the change must already be retained. These
        anchors support later protocol events, such as executed-check receipts.
        """
        if not isinstance(anchors, tuple) or not anchors:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "an ordered nonempty anchor tuple is required",
            )
        return self._admit(
            anchors=anchors,
            change_set=change_set,
            machine_events=machine_events,
            transaction_time=transaction_time,
            actor_id=actor_id,
        )

    def _admit(
        self,
        *,
        anchors: tuple[KnowledgeAnchorInput, ...],
        change_set: KnowledgeChangeSet,
        machine_events: tuple[bytes, ...],
        transaction_time: str,
        actor_id: str,
    ) -> KnowledgeHistoryReplay:
        change = _validated_change(change_set)
        if not isinstance(machine_events, tuple) or not machine_events:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "an ordered nonempty machine-event tuple is required",
            )
        entries: list[dict[str, object]] = [
            {
                "actor_id": actor_id,
                "event_id": f"change:{change.identity}:retained",
                "event_type": _CHANGE_EVENT,
                "payload": {
                    "change_set_bytes_base64": b64encode(change.canonical_bytes).decode(
                        "ascii"
                    ),
                    "change_set_id": change.change_set_id,
                    "change_set_identity": change.identity,
                },
                "transaction_time": transaction_time,
            }
        ]
        entries.extend(
            self._anchor_entry(
                anchor=anchor,
                transaction_time=transaction_time,
                actor_id=actor_id,
            )
            for anchor in anchors
        )
        for index, machine_event in enumerate(machine_events):
            event_type, payload = _event_object(machine_event)
            entries.append(
                {
                    "actor_id": actor_id,
                    "event_id": f"change:{change.identity}:protocol:{index}",
                    "event_type": event_type,
                    "payload": payload,
                    "transaction_time": transaction_time,
                }
            )
        accepted_before = len(self.replay().change_sets)

        def validate_complete(candidate: list[dict[str, object]]) -> None:
            replay = self._replay_envelopes(candidate)
            if (
                len(replay.change_sets) != accepted_before + 1
                or replay.change_sets[-1].identity != change.identity
            ):
                raise _refuse(
                    KnowledgeChangeRefusalReason.INCOMPLETE_ADMISSION,
                    "admit requires one terminal acceptance of the retained change set",
                )

        self._append(entries, validate=validate_complete)
        return self.replay()

    def replay(self) -> KnowledgeHistoryReplay:
        try:
            return self._replay_envelopes(self._ledger.read())
        except KnowledgeChangeRefusal:
            raise
        except (KeyError, TypeError, ValueError, LedgerError) as error:
            raise _refuse(
                KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                "ledger replay failed",
            ) from error

    def _validate_candidate(self, events: list[dict[str, object]]) -> None:
        self._replay_envelopes(events)

    def _replay_envelopes(
        self, events: list[dict[str, object]]
    ) -> KnowledgeHistoryReplay:
        machine_state = MachineState.empty(self.partial_contract.identity)
        projection = KnowledgeGraph(self.contract_view)
        acceptance_head = GENESIS
        materialization_head = GENESIS
        retained: dict[str, KnowledgeRetainedInput] = {}
        changes: dict[str, KnowledgeChangeSet] = {}
        change_ids: set[str] = set()
        applied_ids: set[str] = set()
        proposal_changes: dict[str, str] = {}
        machine_receipts: list[MachineReceipt] = []
        accepted_changes: list[KnowledgeChangeSet] = []
        record_history: dict[str, KnowledgeRecordHistory] = {}
        graphs_by_change: dict[str, KnowledgeGraph] = {}
        bootstrap_roles: set[str] = set()

        for event in events:
            event_type = event["event_type"]
            payload = event["payload"]
            if event_type == _CHANGE_EVENT:
                if bootstrap_roles != _REOPEN_ROLES:
                    raise _refuse(
                        KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                        "change admission requires the complete retained bootstrap",
                    )
                _exact(payload, _CHANGE_FIELDS, "retained change event is not closed")
                source = _decode_b64(
                    payload["change_set_bytes_base64"],
                    "retained change-set bytes are malformed",
                )
                change = KnowledgeChangeSet.from_bytes(source)
                if (
                    payload["change_set_identity"] != change.identity
                    or payload["change_set_id"] != change.change_set_id
                    or change.identity in changes
                    or change.change_set_id in change_ids
                ):
                    raise _refuse(
                        KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
                        "retained change-set identity does not match its bytes",
                    )
                self._validate_change_base(
                    change,
                    event,
                    projection,
                    acceptance_head,
                    materialization_head,
                    retained,
                    applied_ids,
                )
                changes[change.identity] = change
                change_ids.add(change.change_set_id)
                continue

            if set(payload) == _ANCHOR_FIELDS:
                machine_payload = _object(
                    payload["machine_payload"],
                    "retained machine payload must be an object",
                )
                retained_bytes = _decode_b64(
                    payload["retained_bytes_base64"],
                    "retained bytes are malformed",
                )
                role = payload["role"]
                record_id = payload["record_id"]
                if (
                    role not in _HEAD_ROLES
                    or not isinstance(record_id, str)
                    or not record_id
                    or record_id in retained
                    or payload["retained_sha256"] != _digest(retained_bytes)
                ):
                    raise _refuse(
                        KnowledgeChangeRefusalReason.RETAINED_BYTES_MISMATCH,
                        "retained ledger input is inconsistent",
                    )
                expected_bootstrap = self._bootstrap_bytes(role)
                if (
                    expected_bootstrap is not None
                    and retained_bytes != expected_bootstrap
                ):
                    raise _refuse(
                        KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
                        f"retained {role} bytes do not match the active history",
                    )
                if role in _REOPEN_ROLES:
                    if role in bootstrap_roles:
                        raise _refuse(
                            KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                            f"duplicate bootstrap role: {role}",
                        )
                    bootstrap_roles.add(role)
                event_binding = self.binding.data["retention_events"].get(event_type)
                if event_binding is None:
                    raise _refuse(
                        KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                        "retained event is absent from the history binding",
                    )
                if (
                    role not in event_binding["allowed_roles"]
                    or machine_payload.get(event_binding["record_id_field"])
                    != record_id
                    or machine_payload.get(event_binding["identity_field"])
                    != payload["retained_sha256"]
                ):
                    raise _refuse(
                        KnowledgeChangeRefusalReason.RETAINED_BYTES_MISMATCH,
                        "retained bytes do not match their machine event",
                    )
                machine_event = _canonical(
                    {"event_type": event_type, "payload": machine_payload}
                )
                result = execute_event(
                    self.partial_contract, machine_state, machine_event
                )
                if result.receipt.outcome != "APPLIED":
                    raise _refuse(
                        KnowledgeChangeRefusalReason.PROTOCOL_REFUSAL,
                        f"retention machine event refused: {result.receipt.refusal_code}",
                    )
                machine_state = result.state
                machine_receipts.append(result.receipt)
                retained[record_id] = KnowledgeRetainedInput(
                    record_id,
                    retained_bytes,
                    payload["retained_sha256"],
                    _text(payload["media_type"], "retained media type is required"),
                    role,
                )
                continue

            if bootstrap_roles != _REOPEN_ROLES:
                raise _refuse(
                    KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
                    "protocol execution requires the complete retained bootstrap",
                )
            machine_event = _canonical({"event_type": event_type, "payload": payload})
            result = execute_event(self.partial_contract, machine_state, machine_event)
            if result.receipt.outcome != "APPLIED":
                raise _refuse(
                    KnowledgeChangeRefusalReason.PROTOCOL_REFUSAL,
                    f"machine event refused: {result.receipt.refusal_code}",
                )
            machine_state = result.state
            machine_receipts.append(result.receipt)
            proposal = self.binding.data["proposal"]
            if event_type == proposal["event_type"]:
                proposal_id = payload[proposal["proposal_id_field"]]
                change_identity = payload[proposal["change_set_identity_field"]]
                stored = machine_state.get_record(proposal["record_type"], proposal_id)
                if (
                    change_identity not in changes
                    or stored is None
                    or stored[proposal["change_set_identity_field"]] != change_identity
                ):
                    raise _refuse(
                        KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
                        "proposal does not reference one retained change set",
                    )
                proposal_changes[proposal_id] = change_identity
            decision = self.binding.data["decision"]
            if event_type == decision["event_type"]:
                proposal_id = payload[decision["proposal_id_field"]]
                change_identity = proposal_changes.get(proposal_id)
                decisions = tuple(
                    record
                    for record in machine_state.records
                    if record.record_type == decision["record_type"]
                    and record.fields[decision["proposal_id_field"]] == proposal_id
                )
                if change_identity is None or len(decisions) != 1:
                    raise _refuse(
                        KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
                        "terminal decision lacks one retained proposal",
                    )
                verdict = decisions[0].fields[decision["verdict_field"]]
                if verdict != self.binding.data["accept_verdict"]:
                    raise _refuse(
                        KnowledgeChangeRefusalReason.REJECTED_CHANGE,
                        f"terminal policy verdict is {verdict}",
                    )
                change = changes[change_identity]
                projection, record_history = self._apply_change(
                    projection,
                    record_history,
                    change,
                )
                applied_ids.add(change.change_set_id)
                accepted_changes.append(change)
                graphs_by_change[change.change_set_id] = projection.state_projection()
                acceptance_head = event["event_hash"]
                materialization_head = content_digest(
                    {
                        "accepted_event": acceptance_head,
                        "change_set": change.identity,
                        "previous": materialization_head,
                        "state": projection.state_digest(),
                    }
                )

        ledger_head = events[-1]["event_hash"] if events else GENESIS
        receipt = _history_receipt(
            contract=self.partial_contract,
            binding=self.binding,
            machine_state=machine_state,
            ledger_head=ledger_head,
            ledger_count=len(events),
            graph=projection,
            retained=retained,
            accepted_changes=tuple(accepted_changes),
        )
        return KnowledgeHistoryReplay(
            graph=projection,
            machine_state=machine_state,
            ledger_head=ledger_head,
            ledger_event_count=len(events),
            acceptance_head=acceptance_head,
            materialization_head=materialization_head,
            receipt=receipt,
            partial_contract=self.partial_contract,
            contract_view=self.contract_view,
            binding=self.binding,
            change_sets=tuple(accepted_changes),
            _retained=MappingProxyType(dict(retained)),
            _machine_receipts=tuple(machine_receipts),
            _record_history=MappingProxyType(dict(record_history)),
            _graphs_by_change=MappingProxyType(dict(graphs_by_change)),
        )

    def _validate_change_base(
        self,
        change: KnowledgeChangeSet,
        event: Mapping[str, object],
        projection: KnowledgeGraph,
        acceptance_head: str,
        materialization_head: str,
        retained: Mapping[str, KnowledgeRetainedInput],
        applied_ids: set[str],
    ) -> None:
        if change.contract_identity != self.partial_contract.identity:
            raise _refuse(
                KnowledgeChangeRefusalReason.STALE_BASE,
                "change set names a different effective contract",
            )
        coordinates = (
            (change.base_ledger_head, event["previous_event_hash"], "ledger head"),
            (change.base_ledger_event_count, event["sequence"] - 1, "ledger count"),
            (change.base_acceptance_head, acceptance_head, "acceptance head"),
            (
                change.base_materialization_head,
                materialization_head,
                "materialization head",
            ),
            (
                change.base_accepted_state_digest,
                projection.state_digest(),
                "accepted-state digest",
            ),
        )
        for actual, expected, label in coordinates:
            if actual != expected:
                raise _refuse(
                    KnowledgeChangeRefusalReason.STALE_BASE,
                    f"change-set base {label} is stale",
                )
        for label, closure in (
            ("source", change.sources),
            ("evidence", change.evidence),
        ):
            accepted_roles = (
                frozenset({"RETAINED_SOURCE"}) if label == "source" else _EVIDENCE_ROLES
            )
            for identifier, identity in closure:
                member = retained.get(identifier)
                if (
                    member is None
                    or member.identity != identity
                    or member.role not in accepted_roles
                ):
                    raise _refuse(
                        KnowledgeChangeRefusalReason.UNRETAINED_INPUT,
                        f"{label} {identifier} is not retained at its declared digest",
                    )
        unknown = set(change.supersedes).difference(applied_ids)
        if unknown:
            raise _refuse(
                KnowledgeChangeRefusalReason.UNKNOWN_SUPERSESSION,
                f"unknown superseded change: {sorted(unknown)[0]}",
            )

    @staticmethod
    def _apply_change(
        before: KnowledgeGraph,
        before_history: Mapping[str, KnowledgeRecordHistory],
        change: KnowledgeChangeSet,
    ) -> tuple[KnowledgeGraph, dict[str, KnowledgeRecordHistory]]:
        history = dict(before_history)
        for operation in change.operations:
            if operation.record_id in history:
                raise _refuse(
                    KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL,
                    f"record ID already exists in history: {operation.record_id}",
                )
            prior_id = operation.supersedes_record_id
            if prior_id == operation.record_id:
                raise _refuse(
                    KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL,
                    f"record {operation.record_id} cannot supersede itself",
                )
            if prior_id is not None:
                if prior_id not in before_history:
                    raise _refuse(
                        KnowledgeChangeRefusalReason.UNKNOWN_SUPERSESSION,
                        f"unknown superseded record: {prior_id}",
                    )
                prior = history[prior_id]
                if prior.superseded_by is not None:
                    raise _refuse(
                        KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL,
                        f"record supersession forks prior record: {prior_id}",
                    )
                if (
                    prior.operation.operation_type != operation.operation_type
                    or prior.operation.record_type != operation.record_type
                ):
                    raise _refuse(
                        KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL,
                        f"record supersession type differs from prior record: {prior_id}",
                    )
                if prior.valid_from.kind != change.valid_time.kind:
                    raise _refuse(
                        KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL,
                        f"record replacement valid-time kind differs from prior record: {prior_id}",
                    )
                if prior.valid_from.kind == "INSTANT" and _aware_time(
                    change.valid_time.value
                ) <= _aware_time(prior.valid_from.value):
                    raise _refuse(
                        KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL,
                        f"record replacement contradicts prior valid time: {prior_id}",
                    )
                history[prior_id] = replace(
                    prior,
                    valid_to=change.valid_time,
                    superseded_by=operation.record_id,
                )
            history[operation.record_id] = KnowledgeRecordHistory(
                operation=operation,
                change_set_id=change.change_set_id,
                valid_from=change.valid_time,
                valid_to=None,
                supersedes_record_id=prior_id,
                superseded_by=None,
            )

        staged = KnowledgeGraph(before.registry)
        for member in history.values():
            if member.superseded_by is not None:
                continue
            operation = member.operation
            if operation.operation_type == "CREATE_ENTITY":
                result = staged.create_entity(
                    operation.record_type,
                    operation.record_id,
                    dict(operation.properties),
                )
            else:
                assert operation.source_id is not None
                assert operation.target_id is not None
                result = staged.create_relation(
                    operation.record_type,
                    operation.record_id,
                    operation.source_id,
                    operation.target_id,
                    dict(operation.properties),
                )
            if result.op_status is not OpStatus.COMMITTED:
                raise _refuse(
                    KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL,
                    result.rejection_reason or "structural operation refused",
                )
        return staged, history


__all__ = [
    "KnowledgeAnchorInput",
    "KnowledgeAnchorResult",
    "KnowledgeChangeHistory",
    "KnowledgeChangeHistoryBinding",
    "KnowledgeChangeRefusal",
    "KnowledgeChangeRefusalReason",
    "KnowledgeChangeSet",
    "KnowledgeHistoryReceipt",
    "KnowledgeHistoryReplay",
    "KnowledgeOperation",
    "KnowledgeRecordHistory",
    "KnowledgeRetainedInput",
    "KnowledgeValidTime",
]
