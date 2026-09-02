"""Deterministic private RET-010 source-to-history experiment."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum, auto
from hashlib import sha256
from importlib.resources import files
import io
import json
from pathlib import Path
import sys
from types import MappingProxyType
from typing import Mapping
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from malleus._contract_binder import BindingRefusal, bind_contract
from malleus._contract_linkml_adapter import (
    LinkMLAdapterRefusal,
    LinkMLImportReader,
    adapt_linkml_closure,
)
from malleus._contract_pipeline import (
    ArtifactRefusal,
    ElaborationRefusal,
    ValidatedContractCompilation,
    compile_binding,
)
from malleus._contract_pipeline.knowledge import (
    KnowledgeAnchorInput,
    KnowledgeChangeHistory,
    KnowledgeChangeHistoryBinding,
    KnowledgeChangeRefusal,
    KnowledgeChangeSet,
    KnowledgeHistoryReceipt,
    KnowledgeHistoryReplay,
    KnowledgeRetainedInput,
)
from malleus._contract_pipeline.machine import (
    PartialEffectiveContract,
    PolicyProgram,
    ProtocolMachineProgram,
    compose_normative_profile,
    compose_partial_effective_contract,
)
from malleus._contract_source import (
    CollaboratorRefusal,
    ImportRequest,
    ResolvedSource,
    ResolverSelection,
    RootRequest,
    SourceBoundaryRefusal,
    build_source_closure,
)


_HERE = Path(__file__).resolve().parent
_PROJECT = Path(__file__).resolve().parents[5]
_DEFAULT_FIXTURE = (
    _PROJECT
    / "research"
    / "ontology_driven_kg_realization"
    / ("fixtures/small_shop_fulfilment")
)
_MAPPING_GRAMMAR = "malleus.small-shop.ret010-mapping/private-v0"
_INPUT_PREFIX = "input/"
_MISSING = object()
_MAPPING_FIELDS = frozenset(
    {
        "actor_id",
        "anchor_events",
        "artifact_ids",
        "artifact_roles",
        "change_set",
        "compiler",
        "grammar",
        "history_binding",
        "input_manifest_sha256",
        "inventory_lookup",
        "operation_bindings",
        "operations",
        "policy_ref",
        "protocol",
        "publication_contract",
        "selection",
        "selection_id",
        "source_artifact_id_prefix",
        "time",
        "transaction_time",
        "valid_time",
    }
)


class Ret010RefusalReason(Enum):
    MISSING_CONFIGURATION = auto()
    MALFORMED_CONFIGURATION = auto()
    NONCANONICAL_CONFIGURATION = auto()
    MISSING_SOURCE_MEMBER = auto()
    SOURCE_DIGEST_MISMATCH = auto()
    INVALID_SOURCE_MANIFEST = auto()
    INVALID_SOURCE_SELECTION = auto()
    INVALID_INVENTORY_LOOKUP = auto()
    AMBIGUOUS_INVENTORY_LOOKUP = auto()
    SOURCE_TIME_MISMATCH = auto()
    AMBIGUOUS_SOURCE_TIME = auto()
    NONEXISTENT_SOURCE_TIME = auto()
    CONTRACT_COMPILATION_FAILED = auto()
    INCOMPLETE_HISTORY = auto()
    INCOMPATIBLE_HISTORY = auto()


class Ret010Refusal(ValueError):
    def __init__(self, reason: Ret010RefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


def _refuse(reason: Ret010RefusalReason, detail: str) -> Ret010Refusal:
    return Ret010Refusal(reason, detail)


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
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            "private data is not canonical JSON",
        ) from error


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _freeze(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _decode_json(source: bytes, *, canonical: bool, label: str) -> dict[str, object]:
    try:
        value = json.loads(
            source.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"non-finite value: {value}")
            ),
        )
    except (UnicodeError, ValueError, json.JSONDecodeError) as error:
        raise _refuse(
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            f"{label} is not valid JSON: {error}",
        ) from error
    if not isinstance(value, dict):
        raise _refuse(
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            f"{label} root must be an object",
        )
    if canonical and _canonical(value) != source:
        raise _refuse(
            Ret010RefusalReason.NONCANONICAL_CONFIGURATION,
            f"{label} must use compact sorted canonical JSON",
        )
    return value


def _object(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise _refuse(
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            f"{label} must be an object",
        )
    return value


def _array(value: object, label: str) -> tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        raise _refuse(
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            f"{label} must be an array",
        )
    return tuple(value)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise _refuse(
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            f"{label} must be a nonempty string",
        )
    return value


def _integer(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise _refuse(
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            f"{label} must be an integer",
        )
    return value


@dataclass(frozen=True, slots=True)
class Ret010Mapping:
    canonical_bytes: bytes
    identity: str
    data: Mapping[str, object]
    publication_contract: str

    @classmethod
    def from_bytes(cls, source: bytes) -> Ret010Mapping:
        data = _decode_json(source, canonical=True, label="mapping")
        if set(data) != _MAPPING_FIELDS:
            raise _refuse(
                Ret010RefusalReason.MALFORMED_CONFIGURATION,
                "mapping root fields are not the closed required set",
            )
        if data.get("grammar") != _MAPPING_GRAMMAR:
            raise _refuse(
                Ret010RefusalReason.MALFORMED_CONFIGURATION,
                "mapping grammar is unsupported",
            )
        publication = _text(
            data.get("publication_contract"), "mapping publication contract"
        )
        return cls(source, _digest(source), _freeze(data), publication)


@dataclass(frozen=True, slots=True)
class _VerifiedInputs:
    source_bytes: tuple[tuple[str, bytes], ...]
    source_identities: tuple[tuple[str, str], ...]
    selection: Mapping[str, object]
    lookup: Mapping[str, object]
    valid_time: str


@dataclass(frozen=True, slots=True)
class Ret010Vertical:
    fixture_root: Path
    mapping: Ret010Mapping
    machine_program: ProtocolMachineProgram
    policy_program: PolicyProgram
    compilation: ValidatedContractCompilation
    effective_contract: PartialEffectiveContract
    history_binding: KnowledgeChangeHistoryBinding
    inputs: _VerifiedInputs


@dataclass(frozen=True, slots=True)
class Ret010Run:
    receipt: KnowledgeHistoryReceipt
    replay: KnowledgeHistoryReplay
    effective_contract: PartialEffectiveContract
    machine_program: ProtocolMachineProgram
    policy_program: PolicyProgram
    history_binding: KnowledgeChangeHistoryBinding
    change_set: KnowledgeChangeSet | None


class _ExactResolver:
    def __init__(self, sources: Mapping[str, tuple[bytes, str]]) -> None:
        self._sources = sources

    def resolve(self, request: RootRequest | ImportRequest) -> ResolvedSource:
        locator = (
            request.requested_locator
            if isinstance(request, RootRequest)
            else request.literal_import
        )
        try:
            source, media_type = self._sources[locator]
        except KeyError as error:
            raise CollaboratorRefusal(locator) from error
        return ResolvedSource(locator, source, media_type)


def _read_required(path: Path, *, label: str) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError as error:
        raise _refuse(
            Ret010RefusalReason.MISSING_CONFIGURATION,
            f"missing {label}: {path}",
        ) from error


def _safe_member(input_root: Path, relative: str) -> Path:
    candidate = input_root / relative
    try:
        candidate.resolve().relative_to(input_root.resolve())
    except ValueError as error:
        raise _refuse(
            Ret010RefusalReason.INVALID_SOURCE_MANIFEST,
            f"member escapes input root: {relative}",
        ) from error
    return candidate


def _manifest_members(
    manifest_bytes: bytes, mapping: Ret010Mapping
) -> dict[str, Mapping[str, object]]:
    expected_manifest = _text(
        mapping.data.get("input_manifest_sha256"), "input manifest identity"
    )
    if _digest(manifest_bytes) != expected_manifest:
        raise _refuse(
            Ret010RefusalReason.SOURCE_DIGEST_MISMATCH,
            "input/manifest.json does not match the selected mapping",
        )
    manifest = _decode_json(manifest_bytes, canonical=False, label="input manifest")
    members: dict[str, Mapping[str, object]] = {}
    for raw_member in _array(manifest.get("members"), "manifest members"):
        member = _object(raw_member, "manifest member")
        relative = _text(member.get("path"), "manifest member path")
        if relative in members:
            raise _refuse(
                Ret010RefusalReason.INVALID_SOURCE_MANIFEST,
                f"duplicate manifest member: {relative}",
            )
        members[relative] = member
    return members


def _verify_member_bytes(
    relative: str, source: bytes, member: Mapping[str, object]
) -> None:
    identity = _text(member.get("sha256"), f"{relative} identity")
    length = _integer(member.get("byte_length"), f"{relative} byte length")
    if _digest(source) != identity or len(source) != length:
        raise _refuse(
            Ret010RefusalReason.SOURCE_DIGEST_MISMATCH,
            f"declared bytes drifted: {relative}",
        )


def _verify_manifest(
    fixture_root: Path, mapping: Ret010Mapping
) -> tuple[dict[str, bytes], dict[str, Mapping[str, object]]]:
    input_root = fixture_root / "input"
    manifest_path = input_root / "manifest.json"
    try:
        manifest_bytes = manifest_path.read_bytes()
    except FileNotFoundError as error:
        raise _refuse(
            Ret010RefusalReason.MISSING_SOURCE_MEMBER,
            "missing input/manifest.json",
        ) from error
    members = _manifest_members(manifest_bytes, mapping)
    sources = {_INPUT_PREFIX + "manifest.json": manifest_bytes}
    for relative, member in members.items():
        path = _safe_member(input_root, relative)
        try:
            source = path.read_bytes()
        except FileNotFoundError as error:
            raise _refuse(
                Ret010RefusalReason.MISSING_SOURCE_MEMBER,
                f"missing declared source member: {relative}",
            ) from error
        _verify_member_bytes(relative, source, member)
        sources[_INPUT_PREFIX + relative] = source
    return sources, members


def _source_json(
    sources: Mapping[str, bytes], relative: str, *, label: str
) -> dict[str, object]:
    try:
        source = sources[_INPUT_PREFIX + relative]
    except KeyError as error:
        raise _refuse(
            Ret010RefusalReason.MISSING_SOURCE_MEMBER,
            f"undeclared {label} member: {relative}",
        ) from error
    return _decode_json(source, canonical=False, label=label)


def _validate_constraints(
    value: Mapping[str, object], constraints: tuple[object, ...], *, label: str
) -> None:
    for raw_constraint in constraints:
        constraint = _object(raw_constraint, f"{label} constraint")
        field = _text(constraint.get("field"), f"{label} constraint field")
        if value.get(field) != constraint.get("equals"):
            raise _refuse(
                Ret010RefusalReason.INVALID_SOURCE_SELECTION,
                f"{label} field does not match the selected fixture: {field}",
            )


def _selected_record(
    sources: Mapping[str, bytes],
    selection: Mapping[str, object],
    config: Mapping[str, object],
) -> Mapping[str, object]:
    member_field = next(
        _text(item.get("field"), "selection constraint field")
        for item in (
            _object(raw, "selection constraint")
            for raw in _array(config.get("constraints"), "selection constraints")
        )
        if item.get("equals") in sources
        or (
            isinstance(item.get("equals"), str)
            and _INPUT_PREFIX + item["equals"] in sources
        )
    )
    relative = _text(selection.get(member_field), "selected source member")
    try:
        source = sources[_INPUT_PREFIX + relative]
    except KeyError as error:
        raise _refuse(
            Ret010RefusalReason.INVALID_SOURCE_SELECTION,
            f"selected source is not retained: {relative}",
        ) from error
    constraints = tuple(
        _object(item, "selection constraint")
        for item in _array(config.get("constraints"), "selection constraints")
    )
    ordinal_field = next(
        _text(item.get("field"), "selection ordinal field")
        for item in constraints
        if isinstance(item.get("equals"), int)
    )
    ordinal_base = config.get("ordinal_base")
    record_order = config.get("record_order")
    if ordinal_base != 1 or record_order != "SOURCE_ORDER":
        raise _refuse(
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            "selection must declare the supported one-based source order",
        )
    ordinal = selection.get(ordinal_field)
    if (
        not isinstance(ordinal, int)
        or isinstance(ordinal, bool)
        or ordinal < ordinal_base
    ):
        raise _refuse(
            Ret010RefusalReason.INVALID_SOURCE_SELECTION,
            "selected source ordinal must use the declared one-based convention",
        )
    lines = tuple(line for line in source.splitlines() if line.strip())
    index = ordinal - ordinal_base
    if index >= len(lines):
        raise _refuse(
            Ret010RefusalReason.INVALID_SOURCE_SELECTION,
            "selected source ordinal is outside the retained member",
        )
    return _decode_json(lines[index], canonical=False, label="selected source record")


def _validate_source_bindings(
    selection: Mapping[str, object],
    record: Mapping[str, object],
    bindings: tuple[object, ...],
) -> None:
    for raw_binding in bindings:
        binding = _object(raw_binding, "source binding")
        selected = selection.get(
            _text(binding.get("selection_field"), "selection binding field"),
            _MISSING,
        )
        observed = record.get(
            _text(binding.get("source_field"), "source binding field"),
            _MISSING,
        )
        comparison = binding.get("comparison")
        if comparison == "EQUAL":
            matches = (
                selected is not _MISSING
                and observed is not _MISSING
                and selected == observed
            )
        elif comparison == "MEMBER":
            matches = isinstance(observed, list) and selected in observed
        else:
            raise _refuse(
                Ret010RefusalReason.MALFORMED_CONFIGURATION,
                f"unsupported source comparison: {comparison}",
            )
        if not matches:
            raise _refuse(
                Ret010RefusalReason.INVALID_SOURCE_SELECTION,
                "selection does not identify the retained source record",
            )


def _inventory_value(
    sources: Mapping[str, bytes],
    selection: Mapping[str, object],
    config: Mapping[str, object],
) -> Mapping[str, object]:
    relative = _text(config.get("member"), "inventory member")
    try:
        source = sources[_INPUT_PREFIX + relative]
    except KeyError as error:
        raise _refuse(
            Ret010RefusalReason.MISSING_SOURCE_MEMBER,
            f"inventory member is not retained: {relative}",
        ) from error
    try:
        rows = tuple(csv.DictReader(io.StringIO(source.decode("utf-8"))))
    except UnicodeError as error:
        raise _refuse(
            Ret010RefusalReason.INVALID_INVENTORY_LOOKUP,
            "inventory member is not UTF-8 CSV",
        ) from error
    key_field = _text(config.get("key_field"), "inventory key field")
    selection_field = _text(
        config.get("selection_key_field"), "inventory selection field"
    )
    value_field = _text(config.get("value_field"), "inventory value field")
    selected = selection.get(selection_field, _MISSING)
    matches = tuple(
        row
        for row in rows
        if selected is not _MISSING and row.get(key_field, _MISSING) == selected
    )
    if not matches:
        raise _refuse(
            Ret010RefusalReason.INVALID_INVENTORY_LOOKUP,
            f"no inventory row matches selected key: {selected}",
        )
    if len(matches) > 1:
        raise _refuse(
            Ret010RefusalReason.AMBIGUOUS_INVENTORY_LOOKUP,
            f"multiple inventory rows match selected key: {selected}",
        )
    value = matches[0].get(value_field)
    if not value:
        raise _refuse(
            Ret010RefusalReason.INVALID_INVENTORY_LOOKUP,
            f"inventory row lacks required value: {value_field}",
        )
    return MappingProxyType({value_field: value})


def _local_time_state(naive: datetime, zone: ZoneInfo) -> tuple[str, datetime | None]:
    candidates = tuple(naive.replace(tzinfo=zone, fold=fold) for fold in (0, 1))
    valid = tuple(
        candidate
        for candidate in candidates
        if candidate.astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None)
        == naive
    )
    if not valid:
        return "NONEXISTENT", None
    offsets = {candidate.utcoffset() for candidate in valid}
    if len(valid) == 2 and len(offsets) == 2:
        return "AMBIGUOUS", None
    return "VALID", valid[0]


def _valid_time(
    sources: Mapping[str, bytes],
    record: Mapping[str, object],
    mapping: Ret010Mapping,
) -> str:
    config = _object(mapping.data.get("time"), "time mapping")
    context = _source_json(
        sources,
        _text(config.get("context_member"), "time context member"),
        label="time context",
    )
    _validate_constraints(
        context,
        _array(config.get("context_constraints"), "time context constraints"),
        label="time context",
    )
    source_field = _text(
        context.get(
            _text(config.get("source_field_field"), "time source-field pointer")
        ),
        "time source field",
    )
    source_value = _text(record.get(source_field), "source time value")
    source_format = _text(
        context.get(_text(config.get("format_field"), "time format pointer")),
        "source time format",
    )
    year = _integer(
        context.get(_text(config.get("year_field"), "time year pointer")),
        "fixture year",
    )
    try:
        naive = datetime.strptime(f"{year} {source_value}", f"%Y {source_format}")
        zone = ZoneInfo(
            _text(
                context.get(
                    _text(config.get("timezone_field"), "timezone field pointer")
                ),
                "source timezone",
            )
        )
    except (ValueError, ZoneInfoNotFoundError) as error:
        raise _refuse(
            Ret010RefusalReason.SOURCE_TIME_MISMATCH,
            f"source time cannot be resolved under retained context: {error}",
        ) from error
    state, aware = _local_time_state(naive, zone)
    if state == "AMBIGUOUS":
        raise _refuse(
            Ret010RefusalReason.AMBIGUOUS_SOURCE_TIME,
            "source local time has multiple UTC interpretations",
        )
    if state == "NONEXISTENT":
        raise _refuse(
            Ret010RefusalReason.NONEXISTENT_SOURCE_TIME,
            "source local time does not exist in the selected timezone",
        )
    assert aware is not None
    resolved = aware.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    expected = _text(mapping.data.get("valid_time"), "mapped valid time")
    if resolved != expected:
        raise _refuse(
            Ret010RefusalReason.SOURCE_TIME_MISMATCH,
            f"resolved source time {resolved} does not match mapping {expected}",
        )
    return resolved


def _at_path(value: object, path: tuple[object, ...]) -> object:
    current = value
    for part in path:
        if isinstance(current, Mapping) and isinstance(part, str):
            current = current.get(part, _MISSING)
        elif isinstance(current, (list, tuple)) and isinstance(part, int):
            if part < 0 or part >= len(current):
                return _MISSING
            current = current[part]
        else:
            return _MISSING
        if current is _MISSING:
            return _MISSING
    return current


def _validate_operations(
    mapping: Ret010Mapping,
    selection: Mapping[str, object],
    lookup: Mapping[str, object] | None,
) -> None:
    operations = _array(mapping.data.get("operations"), "mapped operations")
    by_ordinal = {
        _integer(
            _object(item, "mapped operation").get("ordinal"), "operation ordinal"
        ): item
        for item in operations
    }
    inputs: dict[str, object] = {"selection": selection}
    if lookup is not None:
        inputs["lookup"] = lookup
    for raw_binding in _array(
        mapping.data.get("operation_bindings"), "operation bindings"
    ):
        binding = _object(raw_binding, "operation binding")
        ordinal = _integer(binding.get("operation_ordinal"), "bound operation ordinal")
        operation = by_ordinal.get(ordinal)
        if operation is None:
            raise _refuse(
                Ret010RefusalReason.MALFORMED_CONFIGURATION,
                f"operation binding references absent ordinal: {ordinal}",
            )
        operation_path = _array(binding.get("operation_path"), "operation path")
        input_path = _array(binding.get("input_path"), "input path")
        if not input_path or input_path[0] not in {"selection", "lookup"}:
            raise _refuse(
                Ret010RefusalReason.MALFORMED_CONFIGURATION,
                "operation binding input root is unsupported",
            )
        if input_path[0] == "lookup" and lookup is None:
            continue
        operation_value = _at_path(operation, operation_path)
        input_value = _at_path(inputs, input_path)
        if operation_value is _MISSING or input_value is _MISSING:
            raise _refuse(
                Ret010RefusalReason.MALFORMED_CONFIGURATION,
                "operation binding path does not resolve",
            )
        if operation_value != input_value:
            raise _refuse(
                Ret010RefusalReason.INVALID_SOURCE_SELECTION,
                f"mapped operation {ordinal} does not match retained inputs",
            )


def _verify_source_values(
    sources: Mapping[str, bytes], mapping: Ret010Mapping
) -> _VerifiedInputs:
    selection_config = _object(mapping.data.get("selection"), "selection mapping")
    selection = _source_json(
        sources,
        _text(selection_config.get("member"), "selection member"),
        label="selection",
    )
    constraints = _array(selection_config.get("constraints"), "selection constraints")
    _validate_constraints(selection, constraints, label="selection")
    record = _selected_record(sources, selection, selection_config)
    _validate_source_bindings(
        selection,
        record,
        _array(selection_config.get("source_bindings"), "source bindings"),
    )
    _validate_operations(mapping, selection, None)
    lookup = _inventory_value(
        sources,
        selection,
        _object(mapping.data.get("inventory_lookup"), "inventory mapping"),
    )
    valid_time = _valid_time(sources, record, mapping)
    _validate_operations(mapping, selection, lookup)
    ordered = tuple(sorted(sources.items()))
    identities = tuple((name, _digest(source)) for name, source in ordered)
    return _VerifiedInputs(
        source_bytes=ordered,
        source_identities=identities,
        selection=_freeze(dict(selection)),
        lookup=lookup,
        valid_time=valid_time,
    )


def _verified_inputs(fixture_root: Path, mapping: Ret010Mapping) -> _VerifiedInputs:
    sources, _ = _verify_manifest(fixture_root, mapping)
    return _verify_source_values(sources, mapping)


def _compiler_sources(
    fixture_root: Path,
    verified: _VerifiedInputs,
    config: Mapping[str, object],
) -> dict[str, tuple[bytes, str]]:
    retained = dict(verified.source_bytes)
    answers: dict[str, tuple[bytes, str]] = {}
    for raw_spec in _array(config.get("sources"), "compiler sources"):
        spec = _object(raw_spec, "compiler source")
        locator = _text(spec.get("locator"), "compiler source locator")
        media_type = _text(spec.get("media_type"), "compiler source media type")
        kind = spec.get("kind")
        if kind == "FIXTURE_MEMBER":
            relative = _text(spec.get("path"), "fixture compiler source path")
            try:
                source = retained[_INPUT_PREFIX + relative]
            except KeyError as error:
                raise _refuse(
                    Ret010RefusalReason.MISSING_SOURCE_MEMBER,
                    f"compiler source is not retained: {relative}",
                ) from error
        elif kind == "REPOSITORY_PATH":
            relative = _text(spec.get("path"), "repository compiler source path")
            source = _read_required(_PROJECT / relative, label=relative)
        elif kind == "PACKAGE_RESOURCE":
            package = _text(spec.get("package"), "compiler source package")
            parts = tuple(
                _text(item, "compiler resource path part")
                for item in _array(spec.get("path"), "compiler resource path")
            )
            try:
                source = files(package).joinpath(*parts).read_bytes()
            except (FileNotFoundError, ModuleNotFoundError) as error:
                raise _refuse(
                    Ret010RefusalReason.MISSING_CONFIGURATION,
                    f"compiler package resource is missing: {package}/{'.'.join(parts)}",
                ) from error
        else:
            raise _refuse(
                Ret010RefusalReason.MALFORMED_CONFIGURATION,
                f"unsupported compiler source kind: {kind}",
            )
        answers[locator] = (source, media_type)
    return answers


def _compile_contract(
    fixture_root: Path,
    verified: _VerifiedInputs,
    mapping: Ret010Mapping,
) -> ValidatedContractCompilation:
    config = _object(mapping.data.get("compiler"), "compiler mapping")
    selection = ResolverSelection(
        resolver_id=_text(config.get("resolver_id"), "resolver ID"),
        profile_version=_text(config.get("profile_version"), "resolver profile"),
        configuration_id=_text(
            config.get("configuration_id"), "resolver configuration"
        ),
    )
    answers = _compiler_sources(fixture_root, verified, config)
    try:
        closure = build_source_closure(
            requested_locator=_text(
                config.get("requested_locator"), "requested compiler locator"
            ),
            selection=selection,
            resolver=_ExactResolver(answers),
            import_reader=LinkMLImportReader(),
        )
        return compile_binding(bind_contract(adapt_linkml_closure(closure)))
    except (
        ArtifactRefusal,
        BindingRefusal,
        ElaborationRefusal,
        LinkMLAdapterRefusal,
        SourceBoundaryRefusal,
    ) as error:
        raise _refuse(
            Ret010RefusalReason.CONTRACT_COMPILATION_FAILED,
            f"retained TBox could not compile: {error}",
        ) from error


def _load_mapping(path: Path) -> Ret010Mapping:
    return Ret010Mapping.from_bytes(_read_required(path, label="mapping"))


def _configured_checks(mapping: Ret010Mapping) -> tuple[tuple[str, str], ...]:
    return tuple(
        (
            _text(
                _object(item, "configured check").get("check_contract_id"),
                "check ID",
            ),
            _text(
                _object(item, "configured check").get("check_contract_identity"),
                "check identity",
            ),
        )
        for item in _array(
            _object(mapping.data.get("protocol"), "protocol mapping").get("checks"),
            "configured checks",
        )
    )


def load_ret010_vertical(
    *,
    fixture_root: Path = _DEFAULT_FIXTURE,
    machine_path: Path = _HERE / "machine.json",
    policy_path: Path = _HERE / "policy.json",
    mapping_path: Path = _HERE / "mapping.json",
) -> Ret010Vertical:
    mapping = _load_mapping(mapping_path)
    verified = _verified_inputs(fixture_root, mapping)
    machine = ProtocolMachineProgram.from_bytes(
        _read_required(machine_path, label="machine program")
    )
    policy = PolicyProgram.from_bytes(
        _read_required(policy_path, label="policy program")
    )
    if _configured_checks(mapping) != policy.required_checks:
        raise _refuse(
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            "configured checks do not match the selected policy",
        )
    policy_ref = _text(mapping.data.get("policy_ref"), "policy reference")
    profile = compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={policy_ref: policy},
        capability_refs=(),
    )
    compilation = _compile_contract(fixture_root, verified, mapping)
    effective = compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=profile,
    )
    history_binding = KnowledgeChangeHistoryBinding.from_bytes(
        _canonical(_plain(mapping.data["history_binding"]))
    )
    return Ret010Vertical(
        fixture_root=fixture_root,
        mapping=mapping,
        machine_program=machine,
        policy_program=policy,
        compilation=compilation,
        effective_contract=effective,
        history_binding=history_binding,
        inputs=verified,
    )


def _event(event_type: str, payload: Mapping[str, object]) -> bytes:
    return _canonical({"event_type": event_type, "payload": dict(payload)})


def _anchor_event(
    mapping: Ret010Mapping,
    kind: str,
    *,
    record_id: str,
    identity: str,
    artifact_reference: str | None = None,
) -> bytes:
    config = _object(
        _object(mapping.data.get("anchor_events"), "anchor events").get(kind),
        f"{kind} anchor event",
    )
    fields = _object(config.get("fields"), f"{kind} anchor fields")
    payload = {
        _text(fields.get("record_id"), "anchor record ID field"): record_id,
        _text(fields.get("identity"), "anchor identity field"): identity,
    }
    if artifact_reference is not None:
        payload[_text(fields.get("artifact_reference"), "artifact reference field")] = (
            artifact_reference
        )
    return _event(_text(config.get("event_type"), "anchor event type"), payload)


def _artifact_anchor(
    mapping: Ret010Mapping,
    *,
    artifact_id: str,
    retained_bytes: bytes,
    media_type: str,
    role: str,
) -> KnowledgeAnchorInput:
    return KnowledgeAnchorInput(
        machine_event=_anchor_event(
            mapping,
            "artifact",
            record_id=artifact_id,
            identity=_digest(retained_bytes),
        ),
        retained_bytes=retained_bytes,
        media_type=media_type,
        role=role,
    )


def _append_anchors(
    history: KnowledgeChangeHistory, vertical: Ret010Vertical
) -> tuple[tuple[str, str], ...]:
    data = vertical.mapping.data
    artifact_ids = _object(data.get("artifact_ids"), "artifact IDs")
    roles = _object(data.get("artifact_roles"), "artifact roles")
    transaction_time = _text(data.get("transaction_time"), "transaction time")
    actor_id = _text(data.get("actor_id"), "actor ID")
    prefix = _text(data.get("source_artifact_id_prefix"), "source artifact prefix")
    source_role = _text(roles.get("source"), "source artifact role")
    registration_role = _text(
        roles.get("source_registration"), "source registration role"
    )
    _anchor_event(
        vertical.mapping,
        "artifact",
        record_id="preflight-artifact",
        identity="sha256:" + "0" * 64,
    )
    _anchor_event(
        vertical.mapping,
        "source",
        record_id="preflight-source",
        identity="sha256:" + "0" * 64,
        artifact_reference="preflight-artifact",
    )
    artifacts = (
        (
            _text(artifact_ids.get("validated_contract"), "validated contract ID"),
            vertical.compilation.artifact.artifact_bytes,
            "application/json",
            _text(roles.get("validated_contract"), "validated contract role"),
        ),
        (
            _text(artifact_ids.get("partial_contract"), "partial contract ID"),
            vertical.effective_contract.canonical_bytes,
            "application/json",
            _text(roles.get("partial_contract"), "partial contract role"),
        ),
        (
            _text(artifact_ids.get("history_binding"), "history binding ID"),
            vertical.history_binding.canonical_bytes,
            "application/json",
            _text(roles.get("history_binding"), "history binding role"),
        ),
        (
            _text(artifact_ids.get("mapping"), "mapping artifact ID"),
            vertical.mapping.canonical_bytes,
            "application/json",
            _text(roles.get("mapping"), "mapping role"),
        ),
    )
    anchors = [
        _artifact_anchor(
            vertical.mapping,
            artifact_id=artifact_id,
            retained_bytes=retained,
            media_type=media_type,
            role=role,
        )
        for artifact_id, retained, media_type, role in artifacts
    ]
    source_identities: list[tuple[str, str]] = []
    for source_id, source in vertical.inputs.source_bytes:
        artifact_id = prefix + source_id
        identity = _digest(source)
        anchors.append(
            _artifact_anchor(
                vertical.mapping,
                artifact_id=artifact_id,
                retained_bytes=source,
                media_type="application/octet-stream",
                role=source_role,
            )
        )
        anchors.append(
            KnowledgeAnchorInput(
                machine_event=_anchor_event(
                    vertical.mapping,
                    "source",
                    record_id=source_id,
                    identity=identity,
                    artifact_reference=artifact_id,
                ),
                retained_bytes=source,
                media_type="application/octet-stream",
                role=registration_role,
            )
        )
        source_identities.append((source_id, identity))
    try:
        history.append_anchors(
            anchors=tuple(anchors),
            transaction_time=transaction_time,
            actor_id=actor_id,
        )
    except KnowledgeChangeRefusal as error:
        raise _refuse(
            Ret010RefusalReason.MALFORMED_CONFIGURATION,
            f"retained bootstrap cannot be admitted atomically: {error}",
        ) from error
    return tuple(source_identities)


def _change_set(
    vertical: Ret010Vertical, history: KnowledgeChangeHistory
) -> KnowledgeChangeSet:
    replay = history.replay()
    data = vertical.mapping.data
    config = _object(data.get("change_set"), "change-set mapping")
    artifact_ids = _object(data.get("artifact_ids"), "artifact IDs")
    evidence_ids = {
        "mapping": _text(artifact_ids.get("mapping"), "mapping artifact ID"),
        "validated_contract": _text(
            artifact_ids.get("validated_contract"), "validated contract ID"
        ),
    }
    evidence_bytes = {
        "mapping": vertical.mapping.canonical_bytes,
        "validated_contract": vertical.compilation.artifact.artifact_bytes,
    }
    evidence = []
    for item in _array(config.get("evidence_roles"), "evidence roles"):
        role = _text(item, "evidence role")
        if role not in evidence_ids:
            raise _refuse(
                Ret010RefusalReason.MALFORMED_CONFIGURATION,
                f"unsupported change-set evidence role: {role}",
            )
        evidence.append(
            {
                "evidence_id": evidence_ids[role],
                "sha256": _digest(evidence_bytes[role]),
            }
        )
    payload = {
        "base_acceptance_head": replay.acceptance_head,
        "base_accepted_state_digest": replay.graph.state_digest(),
        "base_ledger_event_count": replay.ledger_event_count,
        "base_ledger_head": replay.ledger_head,
        "base_materialization_head": replay.materialization_head,
        "change_set_id": _text(config.get("change_set_id"), "change-set ID"),
        "contract_identity": vertical.effective_contract.identity,
        "contract_kind": _text(config.get("contract_kind"), "contract kind"),
        "evidence": evidence,
        "grammar": _text(config.get("grammar"), "change-set grammar"),
        "operations": _plain(_array(data.get("operations"), "mapped operations")),
        "sources": [
            {"sha256": identity, "source_id": source_id}
            for source_id, identity in vertical.inputs.source_identities
        ],
        "supersedes": _plain(
            _array(config.get("supersedes"), "supersession references")
        ),
        "valid_time": {"kind": "INSTANT", "value": vertical.inputs.valid_time},
    }
    return KnowledgeChangeSet.from_bytes(_canonical(payload))


def _protocol_events(
    vertical: Ret010Vertical,
    change_set: KnowledgeChangeSet,
    machine_state_identity: str,
) -> tuple[bytes, ...]:
    config = _object(vertical.mapping.data.get("protocol"), "protocol mapping")
    proposal = _object(config.get("proposal"), "proposal mapping")
    proposal_fields = _object(proposal.get("fields"), "proposal fields")
    proposal_id = _text(proposal.get("proposal_id"), "proposal ID")
    proposal_payload = {
        _text(
            proposal_fields.get("expected_state_identity"), "state field"
        ): machine_state_identity,
        _text(
            proposal_fields.get("change_set_identity"), "change-set field"
        ): change_set.identity,
        _text(
            proposal_fields.get("policy_id"), "policy ID field"
        ): vertical.policy_program.identifier,
        _text(
            proposal_fields.get("policy_identity"), "policy identity field"
        ): vertical.policy_program.identity,
        _text(proposal_fields.get("proposal_id"), "proposal ID field"): proposal_id,
    }
    events = [
        _event(
            _text(proposal.get("event_type"), "proposal event type"), proposal_payload
        )
    ]
    receipt = _object(config.get("receipt"), "receipt mapping")
    receipt_fields = _object(receipt.get("fields"), "receipt fields")
    for raw_check in _array(config.get("checks"), "configured checks"):
        check = _object(raw_check, "configured check")
        payload = {
            _text(receipt_fields.get(key), f"receipt {key} field"): _text(
                check.get(key), f"configured {key}"
            )
            for key in (
                "check_contract_id",
                "check_contract_identity",
                "outcome",
                "receipt_id",
            )
        }
        payload[
            _text(receipt_fields.get("policy_identity"), "receipt policy field")
        ] = vertical.policy_program.identity
        payload[_text(receipt_fields.get("proposal_id"), "receipt proposal field")] = (
            proposal_id
        )
        events.append(
            _event(_text(receipt.get("event_type"), "receipt event type"), payload)
        )
    decision = _object(config.get("decision"), "decision mapping")
    decision_fields = _object(decision.get("fields"), "decision fields")
    events.append(
        _event(
            _text(decision.get("event_type"), "decision event type"),
            {
                _text(decision_fields.get("decision_id"), "decision ID field"): _text(
                    decision.get("decision_id"), "decision ID"
                ),
                _text(
                    decision_fields.get("proposal_id"), "decision proposal field"
                ): proposal_id,
            },
        )
    )
    return tuple(events)


def _retained_mapping(
    replay: KnowledgeHistoryReplay,
) -> tuple[KnowledgeRetainedInput, Ret010Mapping]:
    candidates = []
    for retained in replay.retained_inputs:
        if retained.role != "RETAINED_EVIDENCE":
            continue
        try:
            mapping = Ret010Mapping.from_bytes(retained.content)
        except Ret010Refusal:
            continue
        candidates.append((retained, mapping))
    if len(candidates) != 1:
        raise _refuse(
            Ret010RefusalReason.INCOMPATIBLE_HISTORY,
            "ledger must retain one exact RET-010 mapping artifact",
        )
    return candidates[0]


def _retained_vertical_inputs(
    replay: KnowledgeHistoryReplay, mapping: Ret010Mapping
) -> _VerifiedInputs:
    roles = _object(mapping.data.get("artifact_roles"), "artifact roles")
    source_role = _text(roles.get("source"), "source artifact role")
    registration_role = _text(
        roles.get("source_registration"), "source registration role"
    )
    retained_by_id = {item.record_id: item for item in replay.retained_inputs}
    sources = {
        item.record_id: item.content
        for item in replay.retained_inputs
        if item.role == registration_role
    }
    try:
        manifest_bytes = sources[_INPUT_PREFIX + "manifest.json"]
        members = _manifest_members(manifest_bytes, mapping)
        expected_ids = {_INPUT_PREFIX + "manifest.json"} | {
            _INPUT_PREFIX + relative for relative in members
        }
        if set(sources) != expected_ids:
            raise _refuse(
                Ret010RefusalReason.INVALID_SOURCE_MANIFEST,
                "retained source closure differs from the selected manifest",
            )
        for relative, member in members.items():
            _verify_member_bytes(relative, sources[_INPUT_PREFIX + relative], member)
        prefix = _text(
            mapping.data.get("source_artifact_id_prefix"), "source artifact prefix"
        )
        for source_id, source in sources.items():
            artifact = retained_by_id.get(prefix + source_id)
            if (
                artifact is None
                or artifact.role != source_role
                or artifact.content != source
                or artifact.identity != _digest(source)
            ):
                raise _refuse(
                    Ret010RefusalReason.INVALID_SOURCE_MANIFEST,
                    f"retained source lacks its exact source artifact: {source_id}",
                )
        return _verify_source_values(sources, mapping)
    except (KeyError, Ret010Refusal) as error:
        raise _refuse(
            Ret010RefusalReason.INCOMPATIBLE_HISTORY,
            f"ledger-retained source closure is not RET-010: {error}",
        ) from error


def _required_artifact(
    replay: KnowledgeHistoryReplay,
    *,
    record_id: str,
    role: str,
    content: bytes,
) -> bool:
    return any(
        retained.record_id == record_id
        and retained.role == role
        and retained.content == content
        and retained.identity == _digest(content)
        for retained in replay.retained_inputs
    )


def _reopened_result(replay: KnowledgeHistoryReplay) -> Ret010Run:
    effective = replay.partial_contract
    machine = effective.normative_profile.protocol_machine_program
    policy_bindings = effective.normative_profile.policy_programs
    changes = replay.change_sets
    if not changes:
        raise _refuse(
            Ret010RefusalReason.INCOMPLETE_HISTORY,
            "ledger has no accepted RET-010 change",
        )
    mapping_member, mapping = _retained_mapping(replay)
    data = mapping.data
    artifact_ids = _object(data.get("artifact_ids"), "artifact IDs")
    roles = _object(data.get("artifact_roles"), "artifact roles")
    policy_ref = _text(data.get("policy_ref"), "policy reference")
    try:
        expected_binding = KnowledgeChangeHistoryBinding.from_bytes(
            _canonical(_plain(data["history_binding"]))
        )
    except (KeyError, KnowledgeChangeRefusal) as error:
        raise _refuse(
            Ret010RefusalReason.INCOMPATIBLE_HISTORY,
            f"retained mapping has no valid history binding: {error}",
        ) from error
    if len(policy_bindings) != 1:
        raise _refuse(
            Ret010RefusalReason.INCOMPATIBLE_HISTORY,
            "RET-010 requires one retained policy program",
        )
    bound_ref, policy = policy_bindings[0]
    inputs = _retained_vertical_inputs(replay, mapping)
    change = changes[-1]
    mapping_id = _text(artifact_ids.get("mapping"), "mapping artifact ID")
    config = _object(data.get("change_set"), "change-set mapping")
    evidence_artifacts = {
        "mapping": (mapping_id, mapping.canonical_bytes),
        "validated_contract": (
            _text(artifact_ids.get("validated_contract"), "validated contract ID"),
            replay.contract_view.artifact_bytes,
        ),
    }
    expected_evidence = []
    for raw_role in _array(config.get("evidence_roles"), "evidence roles"):
        role = _text(raw_role, "evidence role")
        try:
            record_id, content = evidence_artifacts[role]
        except KeyError as error:
            raise _refuse(
                Ret010RefusalReason.INCOMPATIBLE_HISTORY,
                f"retained mapping names an unsupported evidence role: {role}",
            ) from error
        expected_evidence.append((record_id, _digest(content)))
    required_artifacts = (
        (
            _text(artifact_ids.get("validated_contract"), "validated contract ID"),
            _text(roles.get("validated_contract"), "validated contract role"),
            replay.contract_view.artifact_bytes,
        ),
        (
            _text(artifact_ids.get("partial_contract"), "partial contract ID"),
            _text(roles.get("partial_contract"), "partial contract role"),
            effective.canonical_bytes,
        ),
        (
            _text(artifact_ids.get("history_binding"), "history binding ID"),
            _text(roles.get("history_binding"), "history binding role"),
            replay.binding.canonical_bytes,
        ),
        (
            mapping_id,
            _text(roles.get("mapping"), "mapping role"),
            mapping.canonical_bytes,
        ),
    )
    incompatible = (
        len(changes) != 1
        or mapping_member.record_id != mapping_id
        or mapping_member.identity != mapping.identity
        or replay.binding.identity != expected_binding.identity
        or bound_ref != policy_ref
        or _configured_checks(mapping) != policy.required_checks
        or not all(
            _required_artifact(
                replay,
                record_id=record_id,
                role=role,
                content=content,
            )
            for record_id, role, content in required_artifacts
        )
        or change.change_set_id != _text(config.get("change_set_id"), "change-set ID")
        or change.contract_identity != effective.identity
        or change.contract_kind != _text(config.get("contract_kind"), "contract kind")
        or change.data["grammar"] != _text(config.get("grammar"), "change grammar")
        or change.sources != inputs.source_identities
        or change.evidence != tuple(expected_evidence)
        or _plain(change.data["operations"]) != _plain(data["operations"])
        or change.valid_time.value != inputs.valid_time
        or change.supersedes
        != tuple(
            _text(item, "supersession reference")
            for item in _array(config.get("supersedes"), "supersession references")
        )
    )
    if incompatible:
        raise _refuse(
            Ret010RefusalReason.INCOMPATIBLE_HISTORY,
            "ledger is not the exact selected RET-010 vertical",
        )
    return Ret010Run(
        receipt=replay.receipt,
        replay=replay,
        effective_contract=effective,
        machine_program=machine,
        policy_program=policy,
        history_binding=replay.binding,
        change_set=change,
    )


def run_ret010(
    ledger: Path,
    *,
    fixture_root: Path = _DEFAULT_FIXTURE,
    machine_path: Path = _HERE / "machine.json",
    policy_path: Path = _HERE / "policy.json",
    mapping_path: Path = _HERE / "mapping.json",
) -> Ret010Run:
    ledger = Path(ledger)
    if ledger.exists():
        try:
            replay = KnowledgeChangeHistory.reopen(ledger).replay()
        except KnowledgeChangeRefusal as error:
            raise _refuse(
                Ret010RefusalReason.INCOMPLETE_HISTORY,
                f"existing ledger cannot replay: {error}",
            ) from error
        return _reopened_result(replay)
    vertical = load_ret010_vertical(
        fixture_root=fixture_root,
        machine_path=machine_path,
        policy_path=policy_path,
        mapping_path=mapping_path,
    )
    history = KnowledgeChangeHistory(
        ledger,
        partial_contract=vertical.effective_contract,
        contract_view=vertical.compilation.view,
        binding=vertical.history_binding,
    )
    preflight_change = _change_set(vertical, history)
    _protocol_events(
        vertical,
        preflight_change,
        history.replay().machine_state.identity,
    )
    _append_anchors(history, vertical)
    before = history.replay()
    change_set = _change_set(vertical, history)
    replay = history.admit(
        change_set=change_set,
        machine_events=_protocol_events(
            vertical, change_set, before.machine_state.identity
        ),
        transaction_time=_text(
            vertical.mapping.data.get("transaction_time"), "transaction time"
        ),
        actor_id=_text(vertical.mapping.data.get("actor_id"), "actor ID"),
    )
    return Ret010Run(
        receipt=replay.receipt,
        replay=replay,
        effective_contract=vertical.effective_contract,
        machine_program=vertical.machine_program,
        policy_program=vertical.policy_program,
        history_binding=vertical.history_binding,
        change_set=change_set,
    )


def main(argv: tuple[str, ...] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", required=True, type=Path)
    arguments = parser.parse_args(argv)
    result = run_ret010(arguments.ledger)
    sys.stdout.buffer.write(result.receipt.canonical_bytes + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
