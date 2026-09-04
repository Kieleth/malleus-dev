"""Private neutral population-plan compiler."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
import json
from types import MappingProxyType

from malleus._contract_pipeline.knowledge import (
    KnowledgeAnchorInput,
    KnowledgeChangeHistory,
    KnowledgeChangeSet,
    KnowledgeHistoryReplay,
    KnowledgeOperation,
    KnowledgeValidTime,
)
from malleus._contract_pipeline.machine import PartialEffectiveContract
from malleus._contract_pipeline.view import ContractView
from malleus.kg import KnowledgeGraph, RECORD_FAMILIES


__all__ = (
    "DomainHistoryProfile",
    "PopulationBaseState",
    "PopulationPlanCompilation",
    "PopulationPlanRefusal",
    "PopulationPlanRefusalReason",
    "PopulationPlanStatus",
    "PopulationPreparation",
    "SOURCE_ASSERTION_PROFILE",
    "STATE_VERSION_PROFILE",
    "compile_population_plan",
    "prepare_population_change",
)

_GRAMMAR = "malleus.population-plan/private-v0"
_DIGEST_PREFIX = "sha256:"
_HEX = frozenset("0123456789abcdef")
_ROOT_FIELDS = frozenset(
    {
        "adapter",
        "contract_identity",
        "derivations",
        "evidence",
        "gaps",
        "grammar",
        "history_profile",
        "plan_id",
        "records",
        "sources",
        "supersessions",
        "valid_time",
    }
)
_PUBLIC_FAMILIES = frozenset(family for family, _ in RECORD_FAMILIES)
_ADMITTED_FAMILIES = ("entities", "relations")
_OPERATION_TYPES = (
    ("entities", "CREATE_ENTITY"),
    ("relations", "CREATE_RELATION"),
)
_OPERATION_TYPE_BY_FAMILY = MappingProxyType(dict(_OPERATION_TYPES))
_PROFILE_GRAMMAR = "malleus.domain-history-profile/private-v0"
_PROFILE_FIELDS = frozenset(
    {"grammar", "grounding", "origin", "profile_id", "semantic_unit"}
)
_PROFILE_ORIGINS = frozenset(
    {"EMPTY", "HISTORICAL_RECONSTRUCTION", "PARTIAL_IMPORT", "SNAPSHOT"}
)
_PROFILE_SEMANTIC_UNITS = frozenset(
    {"ASSERTION", "COMMITMENT", "COMPOSITION", "OCCURRENCE", "STATE_VERSION"}
)
_POPULATION_EVIDENCE_ROLES = frozenset({"RETAINED_EVIDENCE", "VALIDATED_CONTRACT"})
_GAP_KINDS = frozenset(
    {
        "AGGREGATE_ONLY",
        "INTERVAL_NOT_EXPRESSIBLE",
        "MODALITY_NOT_EXPRESSIBLE",
        "RELATION_ABSENT",
        "REQUIRED_FIELD_ABSENT_IN_SOURCE",
        "TYPE_ABSENT",
    }
)


class PopulationPlanStatus(str, Enum):
    CHANGE_SET = "CHANGE_SET"
    NO_DOMAIN_CHANGE = "NO_DOMAIN_CHANGE"


class PopulationPlanRefusalReason(str, Enum):
    ABSENT_PATH = "ABSENT_PATH"
    DANGLING_ENDPOINT = "DANGLING_ENDPOINT"
    DUPLICATE_ARTIFACT_ID = "DUPLICATE_ARTIFACT_ID"
    DUPLICATE_CHANGE_SET_ID = "DUPLICATE_CHANGE_SET_ID"
    DUPLICATE_PLAN_ID = "DUPLICATE_PLAN_ID"
    DUPLICATE_RECORD_ID = "DUPLICATE_RECORD_ID"
    FAMILY_NOT_ADMITTED = "FAMILY_NOT_ADMITTED"
    FIELDS_NOT_CLOSED = "FIELDS_NOT_CLOSED"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    MALFORMED_EVIDENCE_REFERENCE = "MALFORMED_EVIDENCE_REFERENCE"
    MALFORMED_IDENTITY = "MALFORMED_IDENTITY"
    MALFORMED_PLAN = "MALFORMED_PLAN"
    MALFORMED_PROFILE_REFERENCE = "MALFORMED_PROFILE_REFERENCE"
    MALFORMED_RETENTION_EVENT = "MALFORMED_RETENTION_EVENT"
    MALFORMED_SUPERSESSION = "MALFORMED_SUPERSESSION"
    SOURCES_REQUIRED = "SOURCES_REQUIRED"
    SUPERSESSION_FORK = "SUPERSESSION_FORK"
    SUPERSESSION_TYPE_MISMATCH = "SUPERSESSION_TYPE_MISMATCH"
    SUPERSESSION_VALID_TIME_MISMATCH = "SUPERSESSION_VALID_TIME_MISMATCH"
    UNDERIVED_FIELD = "UNDERIVED_FIELD"
    UNKNOWN_ORIGIN = "UNKNOWN_ORIGIN"
    UNKNOWN_FAMILY = "UNKNOWN_FAMILY"
    UNKNOWN_GAP_KIND = "UNKNOWN_GAP_KIND"
    UNKNOWN_RECORD = "UNKNOWN_RECORD"
    UNKNOWN_SUPERSESSION = "UNKNOWN_SUPERSESSION"
    UNKNOWN_SEMANTIC_UNIT = "UNKNOWN_SEMANTIC_UNIT"
    UNLISTED_SOURCE = "UNLISTED_SOURCE"
    UNRETAINED_EVIDENCE = "UNRETAINED_EVIDENCE"
    UNRETAINED_SOURCE = "UNRETAINED_SOURCE"
    UNSUPPORTED_GRAMMAR = "UNSUPPORTED_GRAMMAR"
    UNSUPPORTED_VALID_TIME = "UNSUPPORTED_VALID_TIME"
    GROUNDING_REQUIRED = "GROUNDING_REQUIRED"


class PopulationPlanRefusal(ValueError):
    def __init__(self, reason: PopulationPlanRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


def _refuse(reason: PopulationPlanRefusalReason, detail: str) -> PopulationPlanRefusal:
    return PopulationPlanRefusal(reason, detail)


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


@dataclass(frozen=True, slots=True)
class _BaseRecord:
    family: str
    record: Mapping[str, object]
    change_set_id: str
    operation_type: str
    record_type: str
    valid_from: KnowledgeValidTime


@dataclass(frozen=True, slots=True)
class PopulationBaseState:
    """Immutable active records and the complete historical ID namespace."""

    _members: tuple[_BaseRecord, ...]
    _historical_record_ids: frozenset[str]

    @classmethod
    def empty(cls) -> PopulationBaseState:
        return cls((), frozenset())

    @classmethod
    def from_replay(cls, replay: KnowledgeHistoryReplay) -> PopulationBaseState:
        if not isinstance(replay, KnowledgeHistoryReplay):
            raise TypeError("a knowledge-history replay is required")
        records = replay.graph.export_records()
        history = replay.record_history
        active_history = {
            record_id: member
            for record_id, member in history.items()
            if member.superseded_by is None
        }
        exported = {
            record["id"]: (family, record)
            for family, _ in RECORD_FAMILIES
            for record in records[family]
        }
        if set(exported) != set(active_history):
            raise ValueError("replayed graph and active record history disagree")
        return cls(
            tuple(
                _BaseRecord(
                    family=family,
                    record=_freeze(record),
                    change_set_id=active_history[record_id].change_set_id,
                    operation_type=active_history[record_id].operation.operation_type,
                    record_type=active_history[record_id].operation.record_type,
                    valid_from=active_history[record_id].valid_from,
                )
                for record_id, (family, record) in exported.items()
            ),
            frozenset(history),
        )

    def _records(self) -> dict[str, list[dict[str, object]]]:
        records: dict[str, list[dict[str, object]]] = {
            family: [] for family, _ in RECORD_FAMILIES
        }
        for member in self._members:
            record = _thaw(member.record)
            assert isinstance(record, dict)
            records[member.family].append(record)
        return records

    def _changes(self) -> dict[str, str]:
        return {
            str(member.record["id"]): member.change_set_id for member in self._members
        }

    def _by_id(self) -> dict[str, _BaseRecord]:
        return {str(member.record["id"]): member for member in self._members}


@dataclass(frozen=True, slots=True)
class PopulationPlanCompilation:
    status: PopulationPlanStatus
    canonical_plan_bytes: bytes
    plan_id: str
    source_record_ids: tuple[str, ...]
    evidence_record_ids: tuple[str, ...]
    operations: tuple[KnowledgeOperation, ...]
    valid_time: KnowledgeValidTime
    supersedes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PopulationPreparation:
    """One compiled plan after its evidence is retained and its change composed."""

    profile: DomainHistoryProfile
    compilation: PopulationPlanCompilation
    change_set: KnowledgeChangeSet | None
    retention_replay: KnowledgeHistoryReplay


def _object(
    value: object, reason: PopulationPlanRefusalReason, detail: str
) -> dict[str, object]:
    if not isinstance(value, dict):
        raise _refuse(reason, detail)
    return value


def _array(
    value: object, reason: PopulationPlanRefusalReason, detail: str
) -> list[object]:
    if not isinstance(value, list):
        raise _refuse(reason, detail)
    return value


def _text(value: object, reason: PopulationPlanRefusalReason, detail: str) -> str:
    if not isinstance(value, str) or not value:
        raise _refuse(reason, detail)
    return value


def _exact(
    value: Mapping[str, object],
    fields: frozenset[str],
    reason: PopulationPlanRefusalReason,
    detail: str,
) -> None:
    if set(value) != fields:
        raise _refuse(reason, detail)


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and value.startswith(_DIGEST_PREFIX)
        and len(value) == 71
        and all(character in _HEX for character in value[7:])
    )


def _canonical(
    value: object,
    *,
    reason: PopulationPlanRefusalReason = PopulationPlanRefusalReason.MALFORMED_PLAN,
    detail: str = "plan is not canonical JSON data",
) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, UnicodeError, ValueError) as error:
        raise _refuse(reason, detail) from error


def _digest(source: bytes) -> str:
    return _DIGEST_PREFIX + sha256(source).hexdigest()


def _verify_retention_event(
    *,
    history: KnowledgeChangeHistory,
    expected_record_id: str,
    expected_role: str,
    retained_bytes: bytes,
    machine_event: bytes,
) -> None:
    try:
        event = json.loads(machine_event)
    except (json.JSONDecodeError, TypeError, UnicodeDecodeError) as error:
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            "retention event is not valid JSON",
        ) from error
    if not isinstance(event, dict) or set(event) != {"event_type", "payload"}:
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            "retention event fields are not closed",
        )
    if (
        _canonical(
            event,
            reason=PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            detail="retention event is not canonical JSON data",
        )
        != machine_event
    ):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            "retention event bytes are not canonical",
        )
    event_type = event["event_type"]
    payload = event["payload"]
    if not isinstance(event_type, str) or not isinstance(payload, dict):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            "retention event type and payload are required",
        )
    bindings = history.binding.data["retention_events"]
    assert isinstance(bindings, Mapping)
    binding = bindings.get(event_type)
    if not isinstance(binding, Mapping):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            f"event is not an active retention event: {event_type}",
        )
    record_id_field = binding["record_id_field"]
    identity_field = binding["identity_field"]
    allowed_roles = binding["allowed_roles"]
    assert isinstance(record_id_field, str)
    assert isinstance(identity_field, str)
    assert isinstance(allowed_roles, tuple)
    if expected_role not in allowed_roles:
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            f"retention event cannot retain role: {expected_role}",
        )
    if record_id_field not in payload or identity_field not in payload:
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            "retention event lacks its bound record ID or identity",
        )
    if payload[record_id_field] != expected_record_id:
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            f"retention event names the wrong record: {expected_record_id}",
        )
    if payload[identity_field] != _digest(retained_bytes):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            f"retention event names the wrong bytes: {expected_record_id}",
        )


@dataclass(frozen=True, slots=True)
class DomainHistoryProfile:
    """Canonical minimal statement of one adopter's domain-history semantics."""

    canonical_bytes: bytes
    identity: str
    data: Mapping[str, object]
    profile_id: str
    semantic_unit: str
    origin: str
    grounding: Mapping[str, object]

    @classmethod
    def from_data(cls, value: object) -> DomainHistoryProfile:
        if isinstance(value, cls):
            try:
                decoded = json.loads(value.canonical_bytes)
            except (json.JSONDecodeError, TypeError, UnicodeDecodeError) as error:
                raise _refuse(
                    PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
                    "domain-history profile bytes are not valid JSON",
                ) from error
            rebuilt = cls.from_data(decoded)
            if rebuilt != value:
                raise _refuse(
                    PopulationPlanRefusalReason.IDENTITY_MISMATCH,
                    "domain-history profile fields do not match its bytes",
                )
            return rebuilt
        supplied = _object(
            value,
            PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
            "domain-history profile must be an object",
        )
        canonical = _canonical(
            supplied,
            reason=PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
            detail="domain-history profile is not canonical JSON data",
        )
        root = _object(
            json.loads(canonical),
            PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
            "domain-history profile must be an object",
        )
        if (
            _canonical(
                root,
                reason=PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
                detail="domain-history profile is not canonical JSON data",
            )
            != canonical
        ):
            raise _refuse(
                PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
                "domain-history profile has ambiguous JSON object keys",
            )
        _exact(
            root,
            _PROFILE_FIELDS,
            PopulationPlanRefusalReason.FIELDS_NOT_CLOSED,
            "domain-history profile fields are not closed",
        )
        if root["grammar"] != _PROFILE_GRAMMAR:
            raise _refuse(
                PopulationPlanRefusalReason.UNSUPPORTED_GRAMMAR,
                "domain-history profile grammar is unsupported",
            )
        profile_id = _text(
            root["profile_id"],
            PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
            "domain-history profile ID is required",
        )
        semantic_unit = _text(
            root["semantic_unit"],
            PopulationPlanRefusalReason.UNKNOWN_SEMANTIC_UNIT,
            "domain-history semantic unit is required",
        )
        if semantic_unit not in _PROFILE_SEMANTIC_UNITS:
            raise _refuse(
                PopulationPlanRefusalReason.UNKNOWN_SEMANTIC_UNIT,
                f"unknown domain-history semantic unit: {semantic_unit}",
            )
        origin = _text(
            root["origin"],
            PopulationPlanRefusalReason.UNKNOWN_ORIGIN,
            "domain-history origin is required",
        )
        if origin not in _PROFILE_ORIGINS:
            raise _refuse(
                PopulationPlanRefusalReason.UNKNOWN_ORIGIN,
                f"unknown domain-history origin: {origin}",
            )
        grounding = _object(
            root["grounding"],
            PopulationPlanRefusalReason.GROUNDING_REQUIRED,
            "domain-history grounding must be an object",
        )
        if not grounding:
            raise _refuse(
                PopulationPlanRefusalReason.GROUNDING_REQUIRED,
                "domain-history grounding must not be empty",
            )
        frozen = _freeze(root)
        assert isinstance(frozen, Mapping)
        frozen_grounding = frozen["grounding"]
        assert isinstance(frozen_grounding, Mapping)
        return cls(
            canonical_bytes=canonical,
            identity=_digest(canonical),
            data=frozen,
            profile_id=profile_id,
            semantic_unit=semantic_unit,
            origin=origin,
            grounding=frozen_grounding,
        )


SOURCE_ASSERTION_PROFILE = DomainHistoryProfile.from_data(
    {
        "grammar": _PROFILE_GRAMMAR,
        "grounding": {
            "note": "minimal artifact: identity and unit only; full fields per P6",
            "taxonomy": (
                "Micropublications (Clark, Ciccarese, Goble 2014); nanopublications"
            ),
        },
        "origin": "EMPTY",
        "profile_id": "source-assertion",
        "semantic_unit": "ASSERTION",
    }
)
STATE_VERSION_PROFILE = DomainHistoryProfile.from_data(
    {
        "grammar": _PROFILE_GRAMMAR,
        "grounding": {
            "note": "minimal artifact: identity and unit only; full fields per P6",
            "taxonomy": "temporal database versioning; Small Shop walkthrough",
        },
        "origin": "EMPTY",
        "profile_id": "state-version",
        "semantic_unit": "STATE_VERSION",
    }
)


def _validate_contract(
    partial_contract: PartialEffectiveContract, contract_view: ContractView
) -> PartialEffectiveContract:
    if not isinstance(partial_contract, PartialEffectiveContract):
        raise _refuse(
            PopulationPlanRefusalReason.IDENTITY_MISMATCH,
            "a partial effective contract is required",
        )
    if not isinstance(contract_view, ContractView):
        raise _refuse(
            PopulationPlanRefusalReason.IDENTITY_MISMATCH,
            "a validated contract view is required",
        )
    try:
        rebuilt = PartialEffectiveContract.from_bytes(partial_contract.canonical_bytes)
    except (TypeError, ValueError) as error:
        raise _refuse(
            PopulationPlanRefusalReason.IDENTITY_MISMATCH,
            "partial effective contract cannot be reproduced from its bytes",
        ) from error
    if rebuilt != partial_contract:
        raise _refuse(
            PopulationPlanRefusalReason.IDENTITY_MISMATCH,
            "partial effective contract fields do not match its bytes",
        )
    if (
        _DIGEST_PREFIX + contract_view.content_hash()
        != rebuilt.validated_fact_set_sha256
    ):
        raise _refuse(
            PopulationPlanRefusalReason.IDENTITY_MISMATCH,
            "contract view and partial effective contract disagree",
        )
    return rebuilt


def _references(
    raw: object,
    *,
    id_field: str,
    reason: PopulationPlanRefusalReason,
    require_nonempty: bool,
) -> tuple[tuple[str, str], ...]:
    values = _array(raw, reason, f"{id_field} references must be an array")
    references: list[tuple[str, str]] = []
    for raw_member in values:
        member = _object(raw_member, reason, f"{id_field} reference must be an object")
        _exact(
            member,
            frozenset({id_field, "sha256"}),
            reason,
            f"{id_field} reference fields are not closed",
        )
        identifier = _text(member[id_field], reason, f"{id_field} is required")
        digest = member["sha256"]
        if not _is_digest(digest):
            raise _refuse(reason, f"{id_field} digest is malformed")
        assert isinstance(digest, str)
        references.append((identifier, digest))
    identifiers = [identifier for identifier, _ in references]
    if (require_nonempty and not references) or len(identifiers) != len(
        set(identifiers)
    ):
        raise _refuse(reason, f"{id_field} references must be unique")
    return tuple(references)


def _aware_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("instant valid time must carry a timezone")
    return parsed


def _valid_time(raw: object) -> KnowledgeValidTime:
    reason = PopulationPlanRefusalReason.UNSUPPORTED_VALID_TIME
    value = _object(raw, reason, "valid time must be an object")
    _exact(
        value,
        frozenset({"kind", "value"}),
        reason,
        "valid-time fields are not closed",
    )
    kind = _text(value["kind"], reason, "valid-time kind is required")
    text = _text(value["value"], reason, "valid-time value is required")
    if kind not in {"INSTANT", "ORDER_ONLY"}:
        raise _refuse(reason, f"unsupported valid-time kind: {kind}")
    if kind == "INSTANT":
        try:
            _aware_time(text)
        except ValueError as error:
            raise _refuse(reason, "instant valid time is malformed") from error
    return KnowledgeValidTime(kind, text)


def _merged_records(
    plan_records: Mapping[str, object],
    base_state: PopulationBaseState,
    *,
    excluded_base_record_ids: frozenset[str] = frozenset(),
) -> dict[str, list[object]]:
    merged: dict[str, list[object]] = {
        family: [
            record
            for record in family_records
            if record["id"] not in excluded_base_record_ids
        ]
        for family, family_records in base_state._records().items()
    }
    for family in _ADMITTED_FAMILIES:
        for raw in plan_records.get(family, []):
            merged[family].append(raw)
    return merged


def compile_population_plan(
    plan: object,
    *,
    partial_contract: PartialEffectiveContract,
    contract_view: ContractView,
    base_state: PopulationBaseState,
) -> PopulationPlanCompilation:
    """Validate and lower one neutral population plan without I/O."""

    contract = _validate_contract(partial_contract, contract_view)
    if not isinstance(base_state, PopulationBaseState):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "a population base-state view is required",
        )
    root = _object(
        plan, PopulationPlanRefusalReason.MALFORMED_PLAN, "plan must be an object"
    )
    _exact(
        root,
        _ROOT_FIELDS,
        PopulationPlanRefusalReason.FIELDS_NOT_CLOSED,
        "plan fields are not closed",
    )
    if root["grammar"] != _GRAMMAR:
        raise _refuse(
            PopulationPlanRefusalReason.UNSUPPORTED_GRAMMAR,
            "population-plan grammar is unsupported",
        )
    contract_identity = root["contract_identity"]
    if not _is_digest(contract_identity):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_IDENTITY,
            "contract identity must be a SHA-256 digest",
        )
    if contract_identity != contract.identity:
        raise _refuse(
            PopulationPlanRefusalReason.IDENTITY_MISMATCH,
            "plan and partial effective contract disagree",
        )
    plan_id = _text(
        root["plan_id"],
        PopulationPlanRefusalReason.MALFORMED_PLAN,
        "plan ID is required",
    )

    profile = _object(
        root["history_profile"],
        PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
        "history profile must be an object",
    )
    _exact(
        profile,
        frozenset({"profile_id", "sha256"}),
        PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
        "history-profile fields are not closed",
    )
    profile_id = _text(
        profile["profile_id"],
        PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
        "history profile ID is required",
    )
    if not _is_digest(profile["sha256"]):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_PROFILE_REFERENCE,
            "history-profile digest is malformed",
        )

    adapter = _object(
        root["adapter"],
        PopulationPlanRefusalReason.MALFORMED_PLAN,
        "adapter must be an object",
    )
    _exact(
        adapter,
        frozenset({"adapter_id", "version"}),
        PopulationPlanRefusalReason.MALFORMED_PLAN,
        "adapter fields are not closed",
    )
    _text(
        adapter["adapter_id"],
        PopulationPlanRefusalReason.MALFORMED_PLAN,
        "adapter ID is required",
    )
    _text(
        adapter["version"],
        PopulationPlanRefusalReason.MALFORMED_PLAN,
        "adapter version is required",
    )

    sources = _references(
        root["sources"],
        id_field="source_id",
        reason=PopulationPlanRefusalReason.SOURCES_REQUIRED,
        require_nonempty=True,
    )
    evidence = _references(
        root["evidence"],
        id_field="evidence_id",
        reason=PopulationPlanRefusalReason.MALFORMED_EVIDENCE_REFERENCE,
        require_nonempty=False,
    )
    source_ids = {identifier for identifier, _ in sources}

    records = _object(
        root["records"],
        PopulationPlanRefusalReason.MALFORMED_PLAN,
        "records must be an object",
    )
    unknown_families = set(records) - _PUBLIC_FAMILIES
    if unknown_families:
        raise _refuse(
            PopulationPlanRefusalReason.UNKNOWN_FAMILY,
            f"unknown record families: {sorted(unknown_families)}",
        )
    for family in _PUBLIC_FAMILIES:
        if family in records and not isinstance(records[family], list):
            raise _refuse(
                PopulationPlanRefusalReason.MALFORMED_PLAN,
                f"record family {family} must be an array",
            )
    for family in ("signals", "events"):
        if records.get(family, []):
            raise _refuse(
                PopulationPlanRefusalReason.FAMILY_NOT_ADMITTED,
                f"{family} cannot be admitted by the governed path",
            )

    by_id: dict[str, dict[str, object]] = {}
    family_by_id: dict[str, str] = {}
    for family in _ADMITTED_FAMILIES:
        for raw_record in records.get(family, []):
            if not isinstance(raw_record, dict):
                KnowledgeGraph.from_records(
                    contract_view, _merged_records(records, base_state)
                )
                raise AssertionError(
                    "structural validation accepted a malformed record"
                )
            if "id" not in raw_record:
                KnowledgeGraph.from_records(
                    contract_view, _merged_records(records, base_state)
                )
                raise AssertionError(
                    "structural validation accepted a record without an ID"
                )
            record_id = raw_record["id"]
            if not isinstance(record_id, str) or not record_id:
                KnowledgeGraph.from_records(
                    contract_view, _merged_records(records, base_state)
                )
                raise AssertionError(
                    "structural validation accepted a malformed record ID"
                )
            if "properties" in raw_record and not isinstance(
                raw_record["properties"], dict
            ):
                raise _refuse(
                    PopulationPlanRefusalReason.MALFORMED_PLAN,
                    f"record properties must be an object: {record_id}",
                )
            if record_id in by_id:
                raise _refuse(
                    PopulationPlanRefusalReason.DUPLICATE_RECORD_ID,
                    f"duplicate record ID: {record_id}",
                )
            by_id[record_id] = raw_record
            family_by_id[record_id] = family

    duplicate_historical_ids = set(by_id) & base_state._historical_record_ids
    if duplicate_historical_ids:
        duplicate_id = sorted(duplicate_historical_ids)[0]
        raise _refuse(
            PopulationPlanRefusalReason.DUPLICATE_RECORD_ID,
            f"record ID already exists in history: {duplicate_id}",
        )

    base_by_id = base_state._by_id()
    base_changes = base_state._changes()
    for relation in records.get("relations", []):
        assert isinstance(relation, dict)
        for endpoint_name in ("source_id", "target_id"):
            if endpoint_name not in relation:
                continue
            endpoint = relation[endpoint_name]
            if (
                isinstance(endpoint, str)
                and endpoint not in by_id
                and endpoint not in base_changes
            ):
                raise _refuse(
                    PopulationPlanRefusalReason.DANGLING_ENDPOINT,
                    f"relation {relation['id']} has absent {endpoint_name}: {endpoint}",
                )

    superseded_by_record: dict[str, str] = {}
    supersessions = _array(
        root["supersessions"],
        PopulationPlanRefusalReason.MALFORMED_SUPERSESSION,
        "supersessions must be an array",
    )
    for raw_supersession in supersessions:
        supersession = _object(
            raw_supersession,
            PopulationPlanRefusalReason.MALFORMED_SUPERSESSION,
            "supersession must be an object",
        )
        _exact(
            supersession,
            frozenset({"record_id", "supersedes_record_id"}),
            PopulationPlanRefusalReason.MALFORMED_SUPERSESSION,
            "supersession fields are not closed",
        )
        record_id = _text(
            supersession["record_id"],
            PopulationPlanRefusalReason.MALFORMED_SUPERSESSION,
            "supersession record ID is required",
        )
        if record_id not in by_id or record_id in superseded_by_record:
            raise _refuse(
                PopulationPlanRefusalReason.UNKNOWN_RECORD,
                f"supersession names unknown or repeated record: {record_id}",
            )
        prior_id = _text(
            supersession["supersedes_record_id"],
            PopulationPlanRefusalReason.MALFORMED_SUPERSESSION,
            "superseded record ID is required",
        )
        superseded_by_record[record_id] = prior_id
    prior_ids: set[str] = set()
    for prior_id in superseded_by_record.values():
        if prior_id not in base_by_id:
            if prior_id in base_state._historical_record_ids:
                raise _refuse(
                    PopulationPlanRefusalReason.SUPERSESSION_FORK,
                    f"record supersession forks prior record: {prior_id}",
                )
            raise _refuse(
                PopulationPlanRefusalReason.UNKNOWN_SUPERSESSION,
                f"unknown superseded record: {prior_id}",
            )
        if prior_id in prior_ids:
            raise _refuse(
                PopulationPlanRefusalReason.SUPERSESSION_FORK,
                f"record supersession forks prior record: {prior_id}",
            )
        prior_ids.add(prior_id)

    KnowledgeGraph.from_records(
        contract_view,
        _merged_records(
            records,
            base_state,
            excluded_base_record_ids=frozenset(superseded_by_record.values()),
        ),
    )
    for record_id, prior_id in superseded_by_record.items():
        prior = base_by_id[prior_id]
        planned_type = by_id[record_id]["type"]
        planned_operation_type = _OPERATION_TYPE_BY_FAMILY[family_by_id[record_id]]
        if (
            prior.operation_type != planned_operation_type
            or prior.record_type != planned_type
        ):
            raise _refuse(
                PopulationPlanRefusalReason.SUPERSESSION_TYPE_MISMATCH,
                f"record supersession type differs from prior record: {prior_id}",
            )

    derived: set[tuple[str, tuple[str, ...]]] = set()
    derivations = _array(
        root["derivations"],
        PopulationPlanRefusalReason.MALFORMED_PLAN,
        "derivations must be an array",
    )
    for raw_derivation in derivations:
        derivation = _object(
            raw_derivation,
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "derivation must be an object",
        )
        _exact(
            derivation,
            frozenset({"locator", "path", "record_id", "source_id"}),
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "derivation fields are not closed",
        )
        record_id = _text(
            derivation["record_id"],
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "derivation record ID is required",
        )
        if record_id not in by_id:
            raise _refuse(
                PopulationPlanRefusalReason.UNKNOWN_RECORD,
                f"derivation names unknown record: {record_id}",
            )
        raw_path = _array(
            derivation["path"],
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "derivation path must be an array",
        )
        if not raw_path or not all(isinstance(step, str) and step for step in raw_path):
            raise _refuse(
                PopulationPlanRefusalReason.MALFORMED_PLAN,
                "derivation path must contain nonempty field names",
            )
        path = tuple(raw_path)
        node: object = by_id[record_id]
        for step in path:
            if not isinstance(node, dict) or step not in node:
                raise _refuse(
                    PopulationPlanRefusalReason.ABSENT_PATH,
                    f"record {record_id} has no path {list(path)}",
                )
            node = node[step]
        source_id = _text(
            derivation["source_id"],
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "derivation source ID is required",
        )
        if source_id not in source_ids:
            raise _refuse(
                PopulationPlanRefusalReason.UNLISTED_SOURCE,
                f"derivation source is not listed: {source_id}",
            )
        _text(
            derivation["locator"],
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "derivation locator is required",
        )
        derived.add((record_id, path))

    for record_id, record in by_id.items():
        properties = record["properties"]
        assert isinstance(properties, dict)
        required = [("properties", key) for key in properties]
        if "source_id" in record:
            required.extend((("source_id",), ("target_id",)))
        for path in required:
            if (record_id, path) not in derived:
                raise _refuse(
                    PopulationPlanRefusalReason.UNDERIVED_FIELD,
                    f"record field lacks derivation: {record_id}:{list(path)}",
                )

    gaps = _array(
        root["gaps"],
        PopulationPlanRefusalReason.MALFORMED_PLAN,
        "gaps must be an array",
    )
    for raw_gap in gaps:
        gap = _object(
            raw_gap,
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "gap must be an object",
        )
        _exact(
            gap,
            frozenset({"kind", "locator", "source_id", "statement"}),
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "gap fields are not closed",
        )
        kind = _text(
            gap["kind"],
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "gap kind is required",
        )
        if kind not in _GAP_KINDS:
            raise _refuse(
                PopulationPlanRefusalReason.UNKNOWN_GAP_KIND,
                f"unknown gap kind: {kind}",
            )
        source_id = _text(
            gap["source_id"],
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "gap source ID is required",
        )
        if source_id not in source_ids:
            raise _refuse(
                PopulationPlanRefusalReason.UNLISTED_SOURCE,
                f"gap source is not listed: {source_id}",
            )
        _text(
            gap["statement"],
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "gap statement is required",
        )
        _text(
            gap["locator"],
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "gap locator is required",
        )

    valid_time = _valid_time(root["valid_time"])
    for prior_id in superseded_by_record.values():
        prior_time = base_by_id[prior_id].valid_from
        if prior_time.kind != valid_time.kind:
            raise _refuse(
                PopulationPlanRefusalReason.SUPERSESSION_VALID_TIME_MISMATCH,
                f"replacement valid-time kind differs from prior record: {prior_id}",
            )
        if prior_time.kind == "INSTANT" and _aware_time(
            valid_time.value
        ) <= _aware_time(prior_time.value):
            raise _refuse(
                PopulationPlanRefusalReason.SUPERSESSION_VALID_TIME_MISMATCH,
                f"replacement contradicts prior valid time: {prior_id}",
            )
    canonical_plan_bytes = _canonical(root)
    evidence_ids = (
        f"profile:{profile_id}",
        plan_id,
        *(identifier for identifier, _ in evidence),
        *((f"{plan_id}:gaps",) if gaps else ()),
    )
    if len(evidence_ids) != len(set(evidence_ids)) or source_ids & set(evidence_ids):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_EVIDENCE_REFERENCE,
            "source and evidence closure IDs must be globally unique",
        )

    if not by_id:
        return PopulationPlanCompilation(
            status=PopulationPlanStatus.NO_DOMAIN_CHANGE,
            canonical_plan_bytes=canonical_plan_bytes,
            plan_id=plan_id,
            source_record_ids=tuple(identifier for identifier, _ in sources),
            evidence_record_ids=evidence_ids,
            operations=(),
            valid_time=valid_time,
            supersedes=(),
        )

    operation_by_record: dict[str, str] = {}
    operations: list[KnowledgeOperation] = []
    for family, operation_type in _OPERATION_TYPES:
        for record in records.get(family, []):
            assert isinstance(record, dict)
            record_id = record["id"]
            record_type = record["type"]
            assert isinstance(record_id, str)
            assert isinstance(record_type, str)
            ordinal = len(operations)
            operation_id = f"operation:{plan_id}:{ordinal}"
            dependencies: list[str] = []
            if family == "relations":
                for endpoint in (record["source_id"], record["target_id"]):
                    assert isinstance(endpoint, str)
                    dependency = operation_by_record.get(endpoint)
                    if dependency is not None and dependency not in dependencies:
                        dependencies.append(dependency)
            operation = KnowledgeOperation(
                ordinal=ordinal,
                operation_id=operation_id,
                operation_type=operation_type,
                record_type=record_type,
                record_id=record_id,
                properties=_freeze(dict(record["properties"])),
                depends_on=tuple(dependencies),
                source_id=(record["source_id"] if family == "relations" else None),
                target_id=(record["target_id"] if family == "relations" else None),
                supersedes_record_id=superseded_by_record.get(record_id),
            )
            operation_by_record[record_id] = operation_id
            operations.append(operation)

    change_supersedes: list[str] = []
    for prior_id in superseded_by_record.values():
        change_id = base_changes[prior_id]
        if change_id not in change_supersedes:
            change_supersedes.append(change_id)

    return PopulationPlanCompilation(
        status=PopulationPlanStatus.CHANGE_SET,
        canonical_plan_bytes=canonical_plan_bytes,
        plan_id=plan_id,
        source_record_ids=tuple(identifier for identifier, _ in sources),
        evidence_record_ids=evidence_ids,
        operations=tuple(operations),
        valid_time=valid_time,
        supersedes=tuple(change_supersedes),
    )


def prepare_population_change(
    *,
    history: KnowledgeChangeHistory,
    plan: object,
    profile: object,
    retention_events: Mapping[str, bytes],
    transaction_time: str,
    actor_id: str,
) -> PopulationPreparation:
    """Retain a compiled plan's evidence and compose its governed change.

    Source and adapter evidence must already be retained. The caller supplies
    the selected protocol machine's exact retention event bytes. Admission
    stays separate because its protocol events bind the newly composed change
    identity.
    """

    if not isinstance(history, KnowledgeChangeHistory):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "a knowledge-change history is required",
        )
    before = history.replay()
    retained = {member.record_id: member for member in before.retained_inputs}
    if isinstance(plan, dict):
        proposed_plan_id = plan.get("plan_id")
        if isinstance(proposed_plan_id, str) and proposed_plan_id:
            if proposed_plan_id in retained:
                raise _refuse(
                    PopulationPlanRefusalReason.DUPLICATE_PLAN_ID,
                    f"plan ID is already retained: {proposed_plan_id}",
                )

    compiled_profile = DomainHistoryProfile.from_data(profile)
    compilation = compile_population_plan(
        plan,
        partial_contract=before.partial_contract,
        contract_view=before.contract_view,
        base_state=PopulationBaseState.from_replay(before),
    )
    root = json.loads(compilation.canonical_plan_bytes)
    assert isinstance(root, dict)
    plan_id = compilation.plan_id
    if compilation.status is PopulationPlanStatus.CHANGE_SET:
        change_set_id = f"change:{plan_id}"
        if any(change.change_set_id == change_set_id for change in before.change_sets):
            raise _refuse(
                PopulationPlanRefusalReason.DUPLICATE_CHANGE_SET_ID,
                f"change-set ID is already retained: {change_set_id}",
            )

    profile_reference = root["history_profile"]
    assert isinstance(profile_reference, dict)
    if (
        profile_reference["profile_id"] != compiled_profile.profile_id
        or profile_reference["sha256"] != compiled_profile.identity
    ):
        raise _refuse(
            PopulationPlanRefusalReason.IDENTITY_MISMATCH,
            "plan and domain-history profile disagree",
        )

    def require_retained(
        references: object,
        *,
        id_field: str,
        roles: frozenset[str],
        missing_reason: PopulationPlanRefusalReason,
        label: str,
    ) -> None:
        assert isinstance(references, list)
        for reference in references:
            assert isinstance(reference, dict)
            record_id = reference[id_field]
            declared_identity = reference["sha256"]
            assert isinstance(record_id, str)
            member = retained.get(record_id)
            if member is None or member.role not in roles:
                raise _refuse(
                    missing_reason,
                    f"{label} is not retained with an accepted role: {record_id}",
                )
            if member.identity != declared_identity:
                raise _refuse(
                    PopulationPlanRefusalReason.IDENTITY_MISMATCH,
                    f"{label} digest differs from retained bytes: {record_id}",
                )

    require_retained(
        root["sources"],
        id_field="source_id",
        roles=frozenset({"RETAINED_SOURCE"}),
        missing_reason=PopulationPlanRefusalReason.UNRETAINED_SOURCE,
        label="source",
    )
    require_retained(
        root["evidence"],
        id_field="evidence_id",
        roles=_POPULATION_EVIDENCE_ROLES,
        missing_reason=PopulationPlanRefusalReason.UNRETAINED_EVIDENCE,
        label="evidence",
    )

    artifacts: list[tuple[str, bytes]] = []
    profile_record_id = f"profile:{compiled_profile.profile_id}"
    retained_profile = retained.get(profile_record_id)
    if retained_profile is None:
        artifacts.append((profile_record_id, compiled_profile.canonical_bytes))
    elif (
        retained_profile.role != "RETAINED_EVIDENCE"
        or retained_profile.identity != compiled_profile.identity
    ):
        raise _refuse(
            PopulationPlanRefusalReason.IDENTITY_MISMATCH,
            f"retained domain-history profile differs: {profile_record_id}",
        )

    artifacts.append((plan_id, compilation.canonical_plan_bytes))
    gaps = root["gaps"]
    assert isinstance(gaps, list)
    if gaps:
        gaps_id = f"{plan_id}:gaps"
        if gaps_id in retained:
            raise _refuse(
                PopulationPlanRefusalReason.DUPLICATE_ARTIFACT_ID,
                f"generated gaps artifact ID is already retained: {gaps_id}",
            )
        artifacts.append((gaps_id, _canonical({"gaps": gaps, "plan_id": plan_id})))

    if not isinstance(retention_events, Mapping):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            "retention events must exactly cover the artifacts to retain",
        )
    try:
        event_snapshot = dict(retention_events.items())
    except (KeyError, RuntimeError, TypeError, ValueError) as error:
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            "retention events could not be read as one stable snapshot",
        ) from error
    if set(event_snapshot) != {record_id for record_id, _ in artifacts} or any(
        type(event) is not bytes for event in event_snapshot.values()
    ):
        raise _refuse(
            PopulationPlanRefusalReason.MALFORMED_RETENTION_EVENT,
            "retention events must exactly cover the artifacts to retain",
        )

    for record_id, content in artifacts:
        _verify_retention_event(
            history=history,
            expected_record_id=record_id,
            expected_role="RETAINED_EVIDENCE",
            retained_bytes=content,
            machine_event=event_snapshot[record_id],
        )

    history.append_anchors(
        anchors=tuple(
            KnowledgeAnchorInput(
                machine_event=event_snapshot[record_id],
                retained_bytes=content,
                media_type="application/json",
                role="RETAINED_EVIDENCE",
            )
            for record_id, content in artifacts
        ),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    retention_replay = history.replay()
    if compilation.status is PopulationPlanStatus.NO_DOMAIN_CHANGE:
        return PopulationPreparation(
            profile=compiled_profile,
            compilation=compilation,
            change_set=None,
            retention_replay=retention_replay,
        )

    change_set = history.compose_change_set(
        change_set_id=f"change:{plan_id}",
        source_record_ids=compilation.source_record_ids,
        evidence_record_ids=compilation.evidence_record_ids,
        operations=compilation.operations,
        valid_time=compilation.valid_time,
        supersedes=compilation.supersedes,
    )
    return PopulationPreparation(
        profile=compiled_profile,
        compilation=compilation,
        change_set=change_set,
        retention_replay=retention_replay,
    )
