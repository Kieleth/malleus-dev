"""Private neutral population-plan compiler."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
from types import MappingProxyType

from malleus._contract_pipeline.knowledge import (
    KnowledgeHistoryReplay,
    KnowledgeOperation,
    KnowledgeValidTime,
)
from malleus._contract_pipeline.machine import PartialEffectiveContract
from malleus._contract_pipeline.view import ContractView
from malleus.kg import KnowledgeGraph, RECORD_FAMILIES


__all__ = (
    "PopulationBaseState",
    "PopulationPlanCompilation",
    "PopulationPlanRefusal",
    "PopulationPlanRefusalReason",
    "PopulationPlanStatus",
    "compile_population_plan",
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
    DUPLICATE_RECORD_ID = "DUPLICATE_RECORD_ID"
    FAMILY_NOT_ADMITTED = "FAMILY_NOT_ADMITTED"
    FIELDS_NOT_CLOSED = "FIELDS_NOT_CLOSED"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    MALFORMED_EVIDENCE_REFERENCE = "MALFORMED_EVIDENCE_REFERENCE"
    MALFORMED_IDENTITY = "MALFORMED_IDENTITY"
    MALFORMED_PLAN = "MALFORMED_PLAN"
    MALFORMED_PROFILE_REFERENCE = "MALFORMED_PROFILE_REFERENCE"
    MALFORMED_SUPERSESSION = "MALFORMED_SUPERSESSION"
    SOURCES_REQUIRED = "SOURCES_REQUIRED"
    UNDERIVED_FIELD = "UNDERIVED_FIELD"
    UNKNOWN_FAMILY = "UNKNOWN_FAMILY"
    UNKNOWN_GAP_KIND = "UNKNOWN_GAP_KIND"
    UNKNOWN_RECORD = "UNKNOWN_RECORD"
    UNKNOWN_SUPERSESSION = "UNKNOWN_SUPERSESSION"
    UNLISTED_SOURCE = "UNLISTED_SOURCE"
    UNSUPPORTED_GRAMMAR = "UNSUPPORTED_GRAMMAR"
    UNSUPPORTED_VALID_TIME = "UNSUPPORTED_VALID_TIME"


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


@dataclass(frozen=True, slots=True)
class PopulationBaseState:
    """Immutable active graph records paired with their creating changes."""

    _members: tuple[_BaseRecord, ...]

    @classmethod
    def empty(cls) -> PopulationBaseState:
        return cls(())

    @classmethod
    def from_replay(cls, replay: KnowledgeHistoryReplay) -> PopulationBaseState:
        if not isinstance(replay, KnowledgeHistoryReplay):
            raise TypeError("a knowledge-history replay is required")
        records = replay.graph.export_records()
        active_history = {
            record_id: member
            for record_id, member in replay.record_history.items()
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
                )
                for record_id, (family, record) in exported.items()
            )
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
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "plan is not canonical JSON data",
        ) from error


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
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError as error:
            raise _refuse(reason, "instant valid time is malformed") from error
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise _refuse(reason, "instant valid time must carry a timezone")
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
    for prior_id in superseded_by_record.values():
        if prior_id not in base_changes:
            raise _refuse(
                PopulationPlanRefusalReason.UNKNOWN_SUPERSESSION,
                f"unknown superseded record: {prior_id}",
            )

    KnowledgeGraph.from_records(
        contract_view,
        _merged_records(
            records,
            base_state,
            excluded_base_record_ids=frozenset(superseded_by_record.values()),
        ),
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
    for family, operation_type in (
        ("entities", "CREATE_ENTITY"),
        ("relations", "CREATE_RELATION"),
    ):
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
