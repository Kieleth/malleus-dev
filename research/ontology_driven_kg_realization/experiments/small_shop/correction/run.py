"""Run the bounded Small Shop source-to-history-to-graph correction proof.

This module is a private research adapter. Domain choices live in the retained
fixture, mapping, run program, ontology, machine, policy, and check contracts.
The Python code verifies and executes those declarations. The proof retains this
entrypoint's bytes, not the full imported Core, RET-010, or Python closure.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from enum import Enum, auto
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path, PurePosixPath
import sys
from types import MappingProxyType
from typing import Mapping

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
    KnowledgeHistoryReplay,
)
from malleus._contract_pipeline.machine import (
    PartialEffectiveContract,
    PolicyProgram,
    ProtocolMachineProgram,
    compose_normative_profile,
    compose_partial_effective_contract,
    execute_event,
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
from research.ontology_driven_kg_realization.experiments.small_shop.pareto.ret010 import (
    Ret010Mapping,
    Ret010Refusal,
    Ret010Vertical,
    _verify_source_values,
    load_ret010_vertical,
)


_HERE = Path(__file__).resolve().parent
_PROJECT = Path(__file__).resolve().parents[5]
_MACHINE = _HERE / "machine.json"
_POLICY = _HERE / "policy.json"
_PROGRAM = _HERE / "run.json"
_CHECKS = _HERE / "checks"
_CONTRACT_KIND = "PRIVATE_PARTIAL_EFFECTIVE_CONTRACT_V0"
_CHANGE_GRAMMAR = "malleus.knowledge-change-set/private-v0"
_CHECK_GRAMMAR = "malleus.check-contract/private-v0"
_RECEIPT_GRAMMAR = "malleus.check-receipt/private-v0"
_RUN_GRAMMAR = "malleus.small-shop.correction-run/private-v0"
_CORRECTION_MAPPING_GRAMMAR = (
    "malleus.small-shop.supplier-order-correction-mapping/private-v0"
)
_DIGEST_PREFIX = "sha256:"
_HEX = frozenset("0123456789abcdef")


class CorrectionRefusalReason(Enum):
    MISSING_CONFIGURATION = auto()
    MALFORMED_CONFIGURATION = auto()
    NONCANONICAL_CONFIGURATION = auto()
    CONFIGURATION_IDENTITY_MISMATCH = auto()
    SOURCE_DIGEST_MISMATCH = auto()
    CONTRACT_COMPILATION_FAILED = auto()
    CHECK_FAILED = auto()
    INCOMPATIBLE_HISTORY = auto()


class CorrectionRefusal(ValueError):
    def __init__(self, reason: CorrectionRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


def _refuse(reason: CorrectionRefusalReason, detail: str) -> CorrectionRefusal:
    return CorrectionRefusal(reason, detail)


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
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "value cannot be encoded as canonical JSON",
        ) from error


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and value.startswith(_DIGEST_PREFIX)
        and len(value) == 71
        and all(character in _HEX for character in value[7:])
    )


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _read(path: Path, label: str) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError as error:
        raise _refuse(
            CorrectionRefusalReason.MISSING_CONFIGURATION,
            f"missing {label}: {path}",
        ) from error


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    answer: dict[str, object] = {}
    for key, value in pairs:
        if key in answer:
            raise ValueError(f"duplicate key: {key}")
        answer[key] = value
    return answer


def _json(source: bytes, label: str, *, canonical: bool) -> dict[str, object]:
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
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"{label} is not closed JSON",
        ) from error
    if not isinstance(value, dict):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"{label} root must be an object",
        )
    if canonical and _canonical(value) != source:
        raise _refuse(
            CorrectionRefusalReason.NONCANONICAL_CONFIGURATION,
            f"{label} must use compact sorted canonical JSON",
        )
    return value


def _object(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"{label} must be an object",
        )
    return value


def _array(value: object, label: str) -> tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"{label} must be an array",
        )
    return tuple(value)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"{label} must be a nonempty string",
        )
    return value


def _integer(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"{label} must be an integer",
        )
    return value


def _relative_repository_path(value: object, label: str) -> str:
    text = _text(value, label)
    path = PurePosixPath(text)
    if path.is_absolute() or ".." in path.parts:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"{label} must be a repository-relative path",
        )
    return text


def _validate_program(program: dict[str, object]) -> Mapping[str, object]:
    if program.get("grammar") != _RUN_GRAMMAR or set(program) != {
        "actor_id",
        "artifact_ids",
        "baseline",
        "claim",
        "correction",
        "grammar",
        "limitations",
        "outputs",
        "policy_ref",
        "stages",
        "transaction_time",
    }:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "run program grammar or fields are unsupported",
        )
    artifact_ids = _object(program.get("artifact_ids"), "artifact IDs")
    expected_artifacts = {
        "baseline_mapping",
        "check_entrypoint",
        "correction_mapping",
        "history_binding",
        "machine",
        "partial_contract",
        "policy",
        "run_program",
        "source_mapping_check",
        "structural_check",
        "validated_contract",
    }
    if set(artifact_ids) != expected_artifacts:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "run program artifact IDs are not closed",
        )
    artifact_values = tuple(
        _text(artifact_ids[key], f"{key} artifact ID")
        for key in sorted(expected_artifacts)
    )
    if len(artifact_values) != len(set(artifact_values)):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "run program artifact IDs must be unique",
        )
    for key in ("baseline", "correction"):
        source = _object(program.get(key), f"{key} configuration")
        if set(source) != {"fixture_root", "mapping_path", "source_id_prefix"}:
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                f"{key} configuration fields are not closed",
            )
        _relative_repository_path(source.get("fixture_root"), f"{key} fixture root")
        _relative_repository_path(source.get("mapping_path"), f"{key} mapping path")
        _text(source.get("source_id_prefix"), f"{key} source prefix")
    outputs = _object(program.get("outputs"), "output names")
    if set(outputs) != {"explanation", "graph", "history", "receipt"}:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "output names are not closed",
        )
    output_names = []
    for key, value in outputs.items():
        name = _text(value, f"{key} output name")
        output_names.append(name)
        path = PurePosixPath(name)
        if path.is_absolute() or len(path.parts) != 1 or path.name != name:
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                f"{key} output must be a basename",
            )
    if outputs.get("history") != "history.jsonl":
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "history output must be history.jsonl",
        )
    if len(output_names) != len(set(output_names)):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "output names must be unique",
        )
    stages = _array(program.get("stages"), "run stages")
    if len(stages) != 3:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "bounded proof requires three stages",
        )
    selectors = []
    identities = []
    for raw_stage in stages:
        stage = _object(raw_stage, "run stage")
        if set(stage) != {
            "change_set_id",
            "decision_id",
            "mapping_change",
            "proposal_id",
            "receipt_id_prefix",
            "transaction_time",
        }:
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                "run stage fields are not closed",
            )
        selectors.append(stage["mapping_change"])
        identities.extend(
            _text(stage[key], f"stage {key}")
            for key in (
                "change_set_id",
                "decision_id",
                "proposal_id",
                "receipt_id_prefix",
            )
        )
        _text(stage.get("transaction_time"), "stage transaction time")
    if selectors != ["BASELINE", 0, 1] or len(identities) != len(set(identities)):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "run stage selectors or identities are invalid",
        )
    _text(program.get("actor_id"), "actor ID")
    _text(program.get("claim"), "claim")
    _text(program.get("policy_ref"), "policy reference")
    _text(program.get("transaction_time"), "bootstrap transaction time")
    for item in _array(program.get("limitations"), "limitations"):
        _text(item, "limitation")
    return MappingProxyType(program)


def _refuse_output_symlinks(
    output: Path, program: Mapping[str, object]
) -> None:
    outputs = _object(program.get("outputs"), "output names")
    if output.is_symlink() or any(
        (output / _text(name, f"{key} output name")).is_symlink()
        for key, name in outputs.items()
    ):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "output paths must not be symbolic links",
        )


@dataclass(frozen=True, slots=True)
class _SourceBundle:
    retained: tuple[tuple[str, bytes], ...]
    identities: tuple[tuple[str, str], ...]
    mapping_bytes: bytes
    mapping: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class _Configuration:
    program_bytes: bytes
    program: Mapping[str, object]
    entrypoint_bytes: bytes
    machine_bytes: bytes
    machine: ProtocolMachineProgram
    policy_bytes: bytes
    policy: PolicyProgram
    check_contracts: tuple[tuple[bytes, Mapping[str, object]], ...]
    baseline: Ret010Vertical
    correction: _SourceBundle
    compilation: ValidatedContractCompilation
    effective_contract: PartialEffectiveContract
    binding: KnowledgeChangeHistoryBinding


@dataclass(frozen=True, slots=True)
class CorrectionRun:
    replay: KnowledgeHistoryReplay
    receipt_bytes: bytes
    graph_bytes: bytes
    explanation_bytes: bytes


@dataclass(frozen=True, slots=True)
class _CheckReceipt:
    canonical_bytes: bytes
    identity: str
    data: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class _SourceMappingVerification:
    selected_source: Mapping[str, object]
    result: Mapping[str, object]


def _check_contract(
    source: bytes,
    *,
    entrypoint_id: str,
    entrypoint_identity: str,
    shape_reason: CorrectionRefusalReason,
    identity_reason: CorrectionRefusalReason,
) -> Mapping[str, object]:
    """Parse one exact check contract for both fresh and replay paths."""
    try:
        data = _json(source, "check contract", canonical=True)
        if set(data) != {
            "algorithm",
            "check_contract_id",
            "executor",
            "grammar",
            "outcomes",
        }:
            raise ValueError("check contract fields are not closed")
        if data.get("grammar") != _CHECK_GRAMMAR:
            raise ValueError("check contract grammar is unsupported")
        _text(data.get("algorithm"), "check algorithm")
        _text(data.get("check_contract_id"), "check contract ID")
        if data.get("outcomes") != ["SATISFIED", "VIOLATED"]:
            raise ValueError("check contract outcomes are unsupported")
        binding = _object(data.get("executor"), "check entrypoint binding")
        if set(binding) != {"artifact_id", "sha256"}:
            raise ValueError("check entrypoint binding fields are not closed")
    except CorrectionRefusal as error:
        raise _refuse(
            shape_reason, f"invalid check contract: {error.detail}"
        ) from error
    except ValueError as error:
        raise _refuse(shape_reason, f"invalid check contract: {error}") from error
    if binding != {
        "artifact_id": entrypoint_id,
        "sha256": entrypoint_identity,
    }:
        raise _refuse(
            identity_reason,
            "check contract does not pin the exact entrypoint bytes",
        )
    return MappingProxyType(data)


def _check_receipt(
    source: bytes,
    *,
    retained_role: str,
    reason: CorrectionRefusalReason,
) -> _CheckReceipt:
    """Parse one exact receipt under the same rules before admission and replay."""
    if retained_role != "RETAINED_EVIDENCE":
        raise _refuse(reason, "check receipt must be retained evidence")
    try:
        data = _json(source, "check receipt", canonical=True)
        if set(data) != {
            "base",
            "change",
            "check_contract_id",
            "check_contract_identity",
            "grammar",
            "outcome",
            "result",
        }:
            raise ValueError("receipt root fields are not closed")
        if data.get("grammar") != _RECEIPT_GRAMMAR:
            raise ValueError("receipt grammar is unsupported")
        _text(data.get("check_contract_id"), "receipt check contract ID")
        if not _is_digest(data.get("check_contract_identity")):
            raise ValueError("receipt check contract identity is invalid")
        if data.get("outcome") not in {"SATISFIED", "VIOLATED"}:
            raise ValueError("receipt outcome is unsupported")

        base = _object(data.get("base"), "receipt base")
        if set(base) != {
            "acceptance_head",
            "accepted_state_digest",
            "materialization_head",
        }:
            raise ValueError("receipt base fields are not closed")
        for key in ("acceptance_head", "materialization_head"):
            if base.get(key) != "GENESIS" and not _is_digest(base.get(key)):
                raise ValueError(f"receipt base {key} is invalid")
        if not _is_digest(base.get("accepted_state_digest")):
            raise ValueError("receipt base state identity is invalid")

        change = _object(data.get("change"), "receipt change")
        if set(change) != {
            "change_set_id",
            "contract_identity",
            "operations",
            "sources",
            "supersedes",
            "valid_time",
        }:
            raise ValueError("receipt change fields are not closed")
        _text(change.get("change_set_id"), "receipt change ID")
        if not _is_digest(change.get("contract_identity")):
            raise ValueError("receipt contract identity is invalid")
        operations = _array(change.get("operations"), "receipt operations")
        if not operations or not all(isinstance(item, Mapping) for item in operations):
            raise ValueError("receipt operations must be nonempty objects")
        sources = _array(change.get("sources"), "receipt sources")
        source_ids = []
        for raw_source in sources:
            item = _object(raw_source, "receipt source")
            if set(item) != {"sha256", "source_id"}:
                raise ValueError("receipt source fields are not closed")
            source_ids.append(_text(item.get("source_id"), "receipt source ID"))
            if not _is_digest(item.get("sha256")):
                raise ValueError("receipt source identity is invalid")
        if not sources or len(source_ids) != len(set(source_ids)):
            raise ValueError("receipt source closure must be nonempty and unique")
        supersedes = tuple(
            _text(item, "receipt supersession ID")
            for item in _array(change.get("supersedes"), "receipt supersedes")
        )
        if len(supersedes) != len(set(supersedes)):
            raise ValueError("receipt supersession IDs must be unique")
        valid_time = _object(change.get("valid_time"), "receipt valid time")
        if set(valid_time) != {"kind", "value"} or valid_time.get("kind") not in {
            "INSTANT",
            "ORDER_ONLY",
        }:
            raise ValueError("receipt valid-time fields are invalid")
        _text(valid_time.get("value"), "receipt valid-time value")

        result = _object(data.get("result"), "receipt result")
        if set(result) == {
            "mapping_sha256",
            "selected_record_sha256",
            "verified_operation_count",
        }:
            count = result.get("verified_operation_count")
            if not isinstance(count, int) or isinstance(count, bool) or count < 1:
                raise ValueError("receipt verified-operation count is invalid")
            for key in ("mapping_sha256", "selected_record_sha256"):
                if not _is_digest(result.get(key)):
                    raise ValueError(f"receipt {key} is invalid")
        elif set(result) == {"result_state_digest"}:
            if not _is_digest(result.get("result_state_digest")):
                raise ValueError("receipt result-state identity is invalid")
        else:
            raise ValueError("receipt result fields are not closed")
    except CorrectionRefusal as error:
        raise _refuse(reason, f"invalid check receipt: {error.detail}") from error
    except ValueError as error:
        raise _refuse(reason, f"invalid check receipt: {error}") from error
    return _CheckReceipt(source, _digest(source), MappingProxyType(data))


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


def _safe_member(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"fixture member escapes its root: {relative}",
        )
    target = root / relative
    try:
        target.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"fixture member escapes its root: {relative}",
        ) from error
    return target


def _at_path(value: object, path: tuple[object, ...]) -> object:
    current = value
    for part in path:
        if not isinstance(current, Mapping) or not isinstance(part, str):
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                "mapping target path does not resolve",
            )
        if part not in current:
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                "mapping target path does not resolve",
            )
        current = current[part]
    return current


def _correction_sources(fixture: Path, mapping_path: Path) -> _SourceBundle:
    mapping_bytes = _read(mapping_path, "correction mapping")
    mapping = _json(mapping_bytes, "correction mapping", canonical=False)
    expected_mapping_fields = {
        "changes",
        "compiler",
        "fixture_id",
        "grammar",
        "history_base",
        "input_manifest_sha256",
        "input_set_id",
        "publication_contract",
        "selection_member",
        "source",
        "state_bindings",
    }
    if set(mapping) != expected_mapping_fields:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "correction mapping fields are not closed",
        )
    if mapping.get("grammar") != _CORRECTION_MAPPING_GRAMMAR:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "correction mapping grammar is unsupported",
        )
    input_root = fixture / "input"
    manifest_bytes = _read(input_root / "manifest.json", "correction manifest")
    if _digest(manifest_bytes) != mapping["input_manifest_sha256"]:
        raise _refuse(
            CorrectionRefusalReason.SOURCE_DIGEST_MISMATCH,
            "correction manifest differs from the selected mapping",
        )
    manifest = _json(manifest_bytes, "correction manifest", canonical=False)
    retained: dict[str, bytes] = {"input/manifest.json": manifest_bytes}
    for raw_member in _array(manifest.get("members"), "manifest members"):
        member = _object(raw_member, "manifest member")
        relative = _text(member.get("path"), "manifest member path")
        source = _read(_safe_member(input_root, relative), f"source member {relative}")
        if (
            _digest(source) != member.get("sha256")
            or len(source) != member.get("byte_length")
        ):
            raise _refuse(
                CorrectionRefusalReason.SOURCE_DIGEST_MISMATCH,
                f"declared fixture member drifted: {relative}",
            )
        source_id = "input/" + relative
        if source_id in retained:
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                f"duplicate fixture member: {relative}",
            )
        retained[source_id] = source

    selection_id = "input/" + _text(
        mapping.get("selection_member"), "selection member"
    )
    source_config = _object(mapping.get("source"), "source configuration")
    source_id = "input/" + _text(source_config.get("member"), "source member")
    try:
        selection = _json(retained[selection_id], "selection", canonical=False)
        source_lines = tuple(
            line for line in retained[source_id].splitlines() if line.strip()
        )
    except KeyError as error:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "selected correction input is not retained",
        ) from error
    ordinal_base = source_config.get("ordinal_base")
    if ordinal_base != 0 or source_config.get("record_order") != "SOURCE_ORDER":
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "correction source must declare zero-based source order",
        )
    if (
        selection.get("ordinal_base") != ordinal_base
        or selection.get("record_order") != "SOURCE_ORDER"
        or selection.get("temporal_semantics") != "ORDER_ONLY"
    ):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "selection and mapping order conventions disagree",
        )
    records = tuple(
        _json(line, "supplier-order source row", canonical=False)
        for line in source_lines
    )
    changes = _array(mapping.get("changes"), "correction changes")
    if len(changes) != len(records):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "each selected source row requires one declared change",
        )
    declared_ordinals = []
    for raw_change in changes:
        change = _object(raw_change, "correction change")
        ordinal = _integer(change.get("source_record_ordinal"), "source ordinal")
        declared_ordinals.append(ordinal)
        index = ordinal - ordinal_base
        if index < 0 or index >= len(records):
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                "source ordinal lies outside retained source order",
            )
    if tuple(declared_ordinals) != tuple(
        range(ordinal_base, ordinal_base + len(records))
    ):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "correction changes must select every source row once in source order",
        )
    ordered = tuple(sorted(retained.items()))
    return _SourceBundle(
        retained=ordered,
        identities=tuple((identifier, _digest(source)) for identifier, source in ordered),
        mapping_bytes=mapping_bytes,
        mapping=MappingProxyType(mapping),
    )


def _compile_extended_contract(
    correction: _SourceBundle,
) -> ValidatedContractCompilation:
    config = _object(correction.mapping.get("compiler"), "compiler configuration")
    retained = dict(correction.retained)
    answers: dict[str, tuple[bytes, str]] = {}
    for raw_spec in _array(config.get("sources"), "compiler sources"):
        spec = _object(raw_spec, "compiler source")
        kind = _text(spec.get("kind"), "compiler source kind")
        expected_fields = {
            "FIXTURE_MEMBER": {"kind", "locator", "media_type", "path"},
            "REPOSITORY_PATH": {"kind", "locator", "media_type", "path"},
            "PACKAGE_RESOURCE": {
                "kind",
                "locator",
                "media_type",
                "package",
                "path",
            },
        }.get(kind)
        if expected_fields is None or set(spec) != expected_fields:
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                "compiler source fields or kind are unsupported",
            )
        locator = _text(spec.get("locator"), "compiler source locator")
        media_type = _text(spec.get("media_type"), "compiler media type")
        if locator in answers:
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                f"duplicate compiler source locator: {locator}",
            )
        if kind == "FIXTURE_MEMBER":
            relative = "input/" + _relative_repository_path(
                spec.get("path"), "fixture compiler path"
            )
            try:
                source = retained[relative]
            except KeyError as error:
                raise _refuse(
                    CorrectionRefusalReason.MISSING_CONFIGURATION,
                    f"compiler source is not retained: {relative}",
                ) from error
        elif kind == "REPOSITORY_PATH":
            relative = _relative_repository_path(
                spec.get("path"), "repository compiler path"
            )
            source = _read(
                _safe_member(_PROJECT, relative), f"compiler source {relative}"
            )
        elif kind == "PACKAGE_RESOURCE":
            package = _text(spec.get("package"), "compiler source package")
            parts = tuple(
                _text(item, "package path part")
                for item in _array(spec.get("path"), "package path")
            )
            if not parts or any(
                part in {".", ".."} or "/" in part or "\\" in part
                for part in parts
            ):
                raise _refuse(
                    CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                    "compiler package path parts are unsafe",
                )
            try:
                source = files(package).joinpath(*parts).read_bytes()
            except (FileNotFoundError, ModuleNotFoundError) as error:
                raise _refuse(
                    CorrectionRefusalReason.MISSING_CONFIGURATION,
                    f"missing compiler resource: {package}/{'.'.join(parts)}",
                ) from error
        answers[locator] = (source, media_type)
    selection = ResolverSelection(
        resolver_id=_text(config.get("resolver_id"), "resolver ID"),
        profile_version=_text(config.get("profile_version"), "resolver profile"),
        configuration_id=_text(config.get("configuration_id"), "resolver config"),
    )
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
            CorrectionRefusalReason.CONTRACT_COMPILATION_FAILED,
            f"extended ontology could not compile: {error}",
        ) from error


def _load_configuration(
    *,
    program_path: Path,
    correction_fixture: Path | None,
    correction_mapping: Path | None,
    entrypoint_bytes: bytes,
    checks_root: Path,
) -> _Configuration:
    program_bytes = _read(program_path, "run program")
    program = _validate_program(
        _json(program_bytes, "run program", canonical=True)
    )
    machine_bytes = _read(_MACHINE, "machine program")
    policy_bytes = _read(_POLICY, "policy program")
    try:
        machine = ProtocolMachineProgram.from_bytes(machine_bytes)
        policy = PolicyProgram.from_bytes(policy_bytes)
    except ValueError as error:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"machine or policy program is invalid: {error}",
        ) from error
    entrypoint_id = _text(
        _object(program.get("artifact_ids"), "artifact IDs").get(
            "check_entrypoint"
        ),
        "check entrypoint artifact ID",
    )
    check_paths = (
        checks_root / "source-mapping-conformance.json",
        checks_root / "structural-conformance.json",
    )
    check_contracts = tuple(
        (
            source := _read(path, f"check contract {path.name}"),
            _check_contract(
                source,
                entrypoint_id=entrypoint_id,
                entrypoint_identity=_digest(entrypoint_bytes),
                shape_reason=CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                identity_reason=(
                    CorrectionRefusalReason.CONFIGURATION_IDENTITY_MISMATCH
                ),
            ),
        )
        for path in check_paths
    )
    declared_checks = tuple(
        (
            _text(contract.get("check_contract_id"), "check contract ID"),
            _digest(source),
        )
        for source, contract in check_contracts
    )
    if declared_checks != policy.required_checks:
        raise _refuse(
            CorrectionRefusalReason.CONFIGURATION_IDENTITY_MISMATCH,
            "policy does not pin the exact check contracts",
        )
    baseline_config = _object(program.get("baseline"), "baseline configuration")
    baseline_fixture = _PROJECT / _text(
        baseline_config.get("fixture_root"), "baseline fixture root"
    )
    try:
        baseline = load_ret010_vertical(
            fixture_root=baseline_fixture,
            mapping_path=_PROJECT
            / _text(baseline_config.get("mapping_path"), "baseline mapping path"),
        )
    except Ret010Refusal as error:
        reason = (
            CorrectionRefusalReason.SOURCE_DIGEST_MISMATCH
            if "DIGEST" in error.reason.name
            else CorrectionRefusalReason.MALFORMED_CONFIGURATION
        )
        raise _refuse(reason, f"baseline input refused: {error}") from error
    correction_config = _object(
        program.get("correction"), "correction configuration"
    )
    selected_fixture = correction_fixture or (
        _PROJECT
        / _text(correction_config.get("fixture_root"), "correction fixture root")
    )
    selected_mapping = correction_mapping or (
        _PROJECT
        / _text(correction_config.get("mapping_path"), "correction mapping path")
    )
    correction = _correction_sources(selected_fixture, selected_mapping)
    compilation = _compile_extended_contract(correction)
    profile = compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={
            _text(program.get("policy_ref"), "policy reference"): policy,
        },
        capability_refs=(),
    )
    effective_contract = compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=profile,
    )
    try:
        binding = KnowledgeChangeHistoryBinding.from_bytes(
            _canonical(_plain(baseline.mapping.data["history_binding"]))
        )
    except (KeyError, KnowledgeChangeRefusal) as error:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "baseline does not declare a compatible history binding",
        ) from error
    return _Configuration(
        program_bytes=program_bytes,
        program=program,
        entrypoint_bytes=entrypoint_bytes,
        machine_bytes=machine_bytes,
        machine=machine,
        policy_bytes=policy_bytes,
        policy=policy,
        check_contracts=check_contracts,
        baseline=baseline,
        correction=correction,
        compilation=compilation,
        effective_contract=effective_contract,
        binding=binding,
    )


def _event(event_type: str, payload: Mapping[str, object]) -> bytes:
    return _canonical({"event_type": event_type, "payload": dict(payload)})


def _artifact_anchor(
    *,
    record_id: str,
    content: bytes,
    role: str,
    media_type: str = "application/json",
) -> KnowledgeAnchorInput:
    identity = _digest(content)
    return KnowledgeAnchorInput(
        machine_event=_event(
            "ARTIFACT_REGISTERED",
            {"artifact_id": record_id, "artifact_identity": identity},
        ),
        retained_bytes=content,
        media_type=media_type,
        role=role,
    )


def _source_anchors(
    source_id: str, content: bytes
) -> tuple[KnowledgeAnchorInput, KnowledgeAnchorInput]:
    identity = _digest(content)
    artifact_id = "artifact:source:" + source_id
    return (
        KnowledgeAnchorInput(
            machine_event=_event(
                "ARTIFACT_REGISTERED",
                {"artifact_id": artifact_id, "artifact_identity": identity},
            ),
            retained_bytes=content,
            media_type="application/octet-stream",
            role="SOURCE_ARTIFACT",
        ),
        KnowledgeAnchorInput(
            machine_event=_event(
                "SOURCE_REGISTERED",
                {
                    "artifact_id": artifact_id,
                    "source_id": source_id,
                    "source_identity": identity,
                },
            ),
            retained_bytes=content,
            media_type="application/octet-stream",
            role="RETAINED_SOURCE",
        ),
    )


def _artifact_ids(configuration: _Configuration) -> Mapping[str, object]:
    return _object(configuration.program.get("artifact_ids"), "artifact IDs")


def _bootstrap(history: KnowledgeChangeHistory, config: _Configuration) -> None:
    ids = _artifact_ids(config)
    check_by_id = {
        contract["check_contract_id"]: source
        for source, contract in config.check_contracts
    }
    artifacts = (
        (
            _text(ids.get("validated_contract"), "validated contract artifact ID"),
            config.compilation.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
            "application/json",
        ),
        (
            _text(ids.get("partial_contract"), "partial contract artifact ID"),
            config.effective_contract.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
            "application/json",
        ),
        (
            _text(ids.get("history_binding"), "history binding artifact ID"),
            config.binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
            "application/json",
        ),
        (
            _text(ids.get("run_program"), "run artifact ID"),
            config.program_bytes,
            "RETAINED_EVIDENCE",
            "application/json",
        ),
        (
            _text(ids.get("check_entrypoint"), "check entrypoint artifact ID"),
            config.entrypoint_bytes,
            "RETAINED_EVIDENCE",
            "text/x-python",
        ),
        (
            _text(ids.get("machine"), "machine artifact ID"),
            config.machine_bytes,
            "RETAINED_EVIDENCE",
            "application/json",
        ),
        (
            _text(ids.get("policy"), "policy artifact ID"),
            config.policy_bytes,
            "RETAINED_EVIDENCE",
            "application/json",
        ),
        (
            _text(ids.get("baseline_mapping"), "baseline mapping artifact ID"),
            config.baseline.mapping.canonical_bytes,
            "RETAINED_EVIDENCE",
            "application/json",
        ),
        (
            _text(ids.get("correction_mapping"), "correction mapping artifact ID"),
            config.correction.mapping_bytes,
            "RETAINED_EVIDENCE",
            "application/json",
        ),
        (
            _text(
                ids.get("source_mapping_check"),
                "source-mapping check artifact ID",
            ),
            check_by_id["source-mapping-conformance"],
            "RETAINED_EVIDENCE",
            "application/json",
        ),
        (
            _text(ids.get("structural_check"), "structural check artifact ID"),
            check_by_id["structural-conformance"],
            "RETAINED_EVIDENCE",
            "application/json",
        ),
    )
    anchors = [
        _artifact_anchor(
            record_id=record_id,
            content=content,
            role=role,
            media_type=media_type,
        )
        for record_id, content, role, media_type in artifacts
    ]
    baseline_prefix = _text(
        _object(config.program.get("baseline"), "baseline configuration").get(
            "source_id_prefix"
        ),
        "baseline source prefix",
    )
    correction_prefix = _text(
        _object(config.program.get("correction"), "correction configuration").get(
            "source_id_prefix"
        ),
        "correction source prefix",
    )
    for identifier, content in config.baseline.inputs.source_bytes:
        anchors.extend(_source_anchors(baseline_prefix + identifier, content))
    for identifier, content in config.correction.retained:
        anchors.extend(_source_anchors(correction_prefix + identifier, content))
    try:
        history.append_anchors(
            anchors=tuple(anchors),
            transaction_time=_text(
                config.program.get("transaction_time"), "bootstrap transaction time"
            ),
            actor_id=_text(config.program.get("actor_id"), "actor ID"),
        )
    except KnowledgeChangeRefusal as error:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"bootstrap inputs could not be retained atomically: {error}",
        ) from error


@dataclass(frozen=True, slots=True)
class _Stage:
    change_set_id: str
    operations: tuple[object, ...]
    sources: tuple[tuple[str, str], ...]
    supersedes: tuple[str, ...]
    valid_time: Mapping[str, object]
    proposal_id: str
    receipt_id_prefix: str
    decision_id: str
    transaction_time: str
    mapping_artifact_id: str


def _stages(config: _Configuration) -> tuple[_Stage, ...]:
    ids = _artifact_ids(config)
    baseline_prefix = _text(
        _object(config.program.get("baseline"), "baseline configuration").get(
            "source_id_prefix"
        ),
        "baseline source prefix",
    )
    correction_prefix = _text(
        _object(config.program.get("correction"), "correction configuration").get(
            "source_id_prefix"
        ),
        "correction source prefix",
    )
    stage_configs = _array(config.program.get("stages"), "run stages")
    if len(stage_configs) != 3:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "bounded proof requires exactly three declared stages",
        )
    result: list[_Stage] = []
    corrections = _array(config.correction.mapping.get("changes"), "changes")
    for raw_stage in stage_configs:
        stage = _object(raw_stage, "run stage")
        selector = stage.get("mapping_change")
        if selector == "BASELINE":
            change_config = _object(
                config.baseline.mapping.data.get("change_set"),
                "baseline change configuration",
            )
            change_set_id = _text(
                change_config.get("change_set_id"), "baseline change ID"
            )
            operations = _array(
                config.baseline.mapping.data.get("operations"), "baseline operations"
            )
            sources = tuple(
                (baseline_prefix + identifier, identity)
                for identifier, identity in config.baseline.inputs.source_identities
            )
            supersedes = tuple(
                _text(item, "superseded change")
                for item in _array(change_config.get("supersedes"), "supersedes")
            )
            valid_time = {
                "kind": "INSTANT",
                "value": config.baseline.inputs.valid_time,
            }
            mapping_artifact_id = _text(
                ids.get("baseline_mapping"), "baseline mapping artifact ID"
            )
        elif isinstance(selector, int) and not isinstance(selector, bool):
            if selector < 0 or selector >= len(corrections):
                raise _refuse(
                    CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                    "run stage references an absent correction change",
                )
            change = _object(corrections[selector], "correction change")
            change_set_id = _text(change.get("change_set_id"), "correction change ID")
            operations = _array(change.get("operations"), "correction operations")
            sources = tuple(
                (correction_prefix + identifier, identity)
                for identifier, identity in config.correction.identities
            )
            supersedes = tuple(
                _text(item, "superseded change")
                for item in _array(change.get("supersedes"), "supersedes")
            )
            valid_time = _object(change.get("valid_time"), "correction valid time")
            mapping_artifact_id = _text(
                ids.get("correction_mapping"), "correction mapping artifact ID"
            )
        else:
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                "run stage mapping selector is unsupported",
            )
        declared_change_set_id = _text(
            stage.get("change_set_id"), "declared stage change ID"
        )
        if declared_change_set_id != change_set_id:
            raise _refuse(
                CorrectionRefusalReason.MALFORMED_CONFIGURATION,
                "run stage change ID differs from its selected mapping",
            )
        result.append(
            _Stage(
                change_set_id=declared_change_set_id,
                operations=operations,
                sources=sources,
                supersedes=supersedes,
                valid_time=valid_time,
                proposal_id=_text(stage.get("proposal_id"), "proposal ID"),
                receipt_id_prefix=_text(
                    stage.get("receipt_id_prefix"), "receipt ID prefix"
                ),
                decision_id=_text(stage.get("decision_id"), "decision ID"),
                transaction_time=_text(
                    stage.get("transaction_time"), "stage transaction time"
                ),
                mapping_artifact_id=mapping_artifact_id,
            )
        )
    return tuple(result)


def _base_evidence(config: _Configuration, stage: _Stage) -> tuple[str, ...]:
    ids = _artifact_ids(config)
    return (
        stage.mapping_artifact_id,
        _text(ids.get("validated_contract"), "validated contract artifact ID"),
        _text(ids.get("run_program"), "run artifact ID"),
        _text(ids.get("check_entrypoint"), "check entrypoint artifact ID"),
        _text(ids.get("machine"), "machine artifact ID"),
        _text(ids.get("policy"), "policy artifact ID"),
        _text(
            ids.get("source_mapping_check"),
            "source-mapping check artifact ID",
        ),
        _text(ids.get("structural_check"), "structural check artifact ID"),
    )


def _change_set(
    config: _Configuration,
    replay: KnowledgeHistoryReplay,
    stage: _Stage,
    evidence_ids: tuple[str, ...],
) -> KnowledgeChangeSet:
    retained = {item.record_id: item for item in replay.retained_inputs}
    try:
        evidence = [
            {"evidence_id": identifier, "sha256": retained[identifier].identity}
            for identifier in evidence_ids
        ]
    except KeyError as error:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"unretained evidence: {error.args[0]}",
        ) from error
    payload = {
        "base_acceptance_head": replay.acceptance_head,
        "base_accepted_state_digest": replay.graph.state_digest(),
        "base_ledger_event_count": replay.ledger_event_count,
        "base_ledger_head": replay.ledger_head,
        "base_materialization_head": replay.materialization_head,
        "change_set_id": stage.change_set_id,
        "contract_identity": config.effective_contract.identity,
        "contract_kind": _CONTRACT_KIND,
        "evidence": evidence,
        "grammar": _CHANGE_GRAMMAR,
        "operations": _plain(stage.operations),
        "sources": [
            {"sha256": identity, "source_id": identifier}
            for identifier, identity in stage.sources
        ],
        "supersedes": list(stage.supersedes),
        "valid_time": _plain(stage.valid_time),
    }
    try:
        return KnowledgeChangeSet.from_bytes(_canonical(payload))
    except KnowledgeChangeRefusal as error:
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            f"declared change set is invalid: {error}",
        ) from error


def _check_receipts(
    config: _Configuration,
    replay: KnowledgeHistoryReplay,
    change: KnowledgeChangeSet,
) -> tuple[bytes, ...]:
    receipts = []
    for source, contract in config.check_contracts:
        algorithm = _text(contract.get("algorithm"), "check algorithm")
        receipts.append(
            _canonical(
                {
                    "base": _plain(_receipt_base(change)),
                    "change": _plain(_change_claim(change)),
                    "check_contract_id": contract["check_contract_id"],
                    "check_contract_identity": _digest(source),
                    "grammar": _RECEIPT_GRAMMAR,
                    "outcome": "SATISFIED",
                    "result": _plain(
                        _expected_check_result(
                            replay,
                            config.program,
                            change,
                            algorithm,
                            reason=CorrectionRefusalReason.CHECK_FAILED,
                        )
                    ),
                }
            )
        )
    return tuple(receipts)


def _protocol_events(
    config: _Configuration,
    stage: _Stage,
    change: KnowledgeChangeSet,
    machine_state_identity: str,
    receipts: tuple[_CheckReceipt, ...],
) -> tuple[bytes, ...]:
    events = [
        _event(
            "CHANGE_PROPOSED",
            {
                "expected_machine_state_identity": machine_state_identity,
                "knowledge_change_set_identity": change.identity,
                "policy_id": config.policy.identifier,
                "policy_identity": config.policy.identity,
                "proposal_id": stage.proposal_id,
            },
        )
    ]
    if len(receipts) != len(config.check_contracts):
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "each required check needs one receipt",
        )
    for receipt, (contract_bytes, contract) in zip(
        receipts, config.check_contracts, strict=True
    ):
        check_id = _text(contract.get("check_contract_id"), "check contract ID")
        outcome = _text(receipt.data.get("outcome"), "executed check outcome")
        if (
            receipt.data.get("check_contract_id") != check_id
            or receipt.data.get("check_contract_identity") != _digest(contract_bytes)
            or outcome not in contract.get("outcomes", ())
        ):
            raise _refuse(
                CorrectionRefusalReason.CHECK_FAILED,
                "executed receipt differs from its check contract",
            )
        events.append(
            _event(
                "CHECK_RECORDED",
                {
                    "check_contract_id": check_id,
                    "check_contract_identity": _digest(contract_bytes),
                    "outcome": outcome,
                    "policy_identity": config.policy.identity,
                    "proposal_id": stage.proposal_id,
                    "receipt_id": stage.receipt_id_prefix + check_id,
                    "receipt_identity": receipt.identity,
                },
            )
        )
    events.append(
        _event(
            "VERDICT_RECORDED",
            {"decision_id": stage.decision_id, "proposal_id": stage.proposal_id},
        )
    )
    return tuple(events)


def _admit_stage(
    history: KnowledgeChangeHistory,
    config: _Configuration,
    stage: _Stage,
) -> KnowledgeHistoryReplay:
    before = history.replay()
    preliminary = _change_set(config, before, stage, _base_evidence(config, stage))
    receipt_bytes = _check_receipts(config, before, preliminary)
    receipt_anchors = tuple(
        _artifact_anchor(
            record_id=_digest(receipt), content=receipt, role="RETAINED_EVIDENCE"
        )
        for receipt in receipt_bytes
    )
    receipts = tuple(
        _check_receipt(
            anchor.retained_bytes,
            retained_role=anchor.role,
            reason=CorrectionRefusalReason.CHECK_FAILED,
        )
        for anchor in receipt_anchors
    )
    for receipt, (contract_bytes, contract) in zip(
        receipts, config.check_contracts, strict=True
    ):
        _verify_receipt_semantics(
            receipt,
            replay=before,
            program=config.program,
            change=preliminary,
            contract=contract,
            contract_identity=_digest(contract_bytes),
            reason=CorrectionRefusalReason.CHECK_FAILED,
        )
    try:
        machine_state = before.machine_state
        for anchor in receipt_anchors:
            preview = execute_event(
                config.effective_contract,
                machine_state,
                anchor.machine_event,
            )
            if preview.receipt.outcome != "APPLIED":
                raise _refuse(
                    CorrectionRefusalReason.CHECK_FAILED,
                    "check receipt artifact cannot enter the declared machine",
                )
            machine_state = preview.state
        return history.admit_with_anchors(
            anchors=receipt_anchors,
            change_set=preliminary,
            machine_events=_protocol_events(
                config,
                stage,
                preliminary,
                machine_state.identity,
                receipts,
            ),
            transaction_time=stage.transaction_time,
            actor_id=_text(config.program.get("actor_id"), "actor ID"),
        )
    except KnowledgeChangeRefusal as error:
        raise _refuse(
            CorrectionRefusalReason.CHECK_FAILED,
            f"checked change could not be admitted atomically: {error}",
        ) from error


def _receipt_base(change: KnowledgeChangeSet) -> Mapping[str, object]:
    return MappingProxyType(
        {
            "acceptance_head": change.base_acceptance_head,
            "accepted_state_digest": change.base_accepted_state_digest,
            "materialization_head": change.base_materialization_head,
        }
    )


def _change_claim(change: KnowledgeChangeSet) -> Mapping[str, object]:
    return MappingProxyType(
        {
            "change_set_id": change.change_set_id,
            "contract_identity": change.contract_identity,
            "operations": _plain(change.data["operations"]),
            "sources": _plain(change.data["sources"]),
            "supersedes": list(change.supersedes),
            "valid_time": _plain(change.data["valid_time"]),
        }
    )


def _expected_check_result(
    replay: KnowledgeHistoryReplay,
    program: Mapping[str, object],
    change: KnowledgeChangeSet,
    algorithm: str,
    *,
    reason: CorrectionRefusalReason,
) -> Mapping[str, object]:
    if algorithm == "SOURCE_MAPPING_CONFORMS_TO_CHANGE_SET":
        return _verify_source_mapping(
            replay,
            program,
            change,
            reason=reason,
        ).result
    if algorithm != "OPERATIONS_APPLY_ATOMICALLY_TO_ACCEPTED_STATE":
        raise _refuse(reason, f"check algorithm is unsupported: {algorithm}")

    accepted = tuple(
        item for item in replay.change_sets if item.change_set_id == change.change_set_id
    )
    if accepted:
        if len(accepted) != 1 or accepted[0].identity != change.identity:
            raise _refuse(reason, "accepted change identity is ambiguous")
        projected = replay.graph_at_change(change.change_set_id)
    else:
        try:
            projected, _ = KnowledgeChangeHistory._apply_change(
                replay.graph,
                replay.record_history,
                change,
            )
        except KnowledgeChangeRefusal as error:
            raise _refuse(
                reason,
                f"structural-conformance check refused the operations: {error}",
            ) from error
    return MappingProxyType({"result_state_digest": projected.state_digest()})


def _verify_receipt_semantics(
    receipt: _CheckReceipt,
    *,
    replay: KnowledgeHistoryReplay,
    program: Mapping[str, object],
    change: KnowledgeChangeSet,
    contract: Mapping[str, object],
    contract_identity: str,
    reason: CorrectionRefusalReason,
) -> None:
    algorithm = _text(contract.get("algorithm"), "check algorithm")
    expected = {
        "base": _plain(_receipt_base(change)),
        "change": _plain(_change_claim(change)),
        "check_contract_id": _text(
            contract.get("check_contract_id"), "check contract ID"
        ),
        "check_contract_identity": contract_identity,
        "grammar": _RECEIPT_GRAMMAR,
        "outcome": "SATISFIED",
        "result": _plain(
            _expected_check_result(
                replay,
                program,
                change,
                algorithm,
                reason=reason,
            )
        ),
    }
    if receipt.data != expected:
        raise _refuse(reason, "check receipt differs from recomputed semantics")


def _validate_replay(
    replay: KnowledgeHistoryReplay, *, entrypoint_bytes: bytes
) -> Mapping[str, object]:
    retained = {item.record_id: item for item in replay.retained_inputs}
    run_candidates = []
    for item in replay.retained_inputs:
        if item.role != "RETAINED_EVIDENCE":
            continue
        try:
            value = _json(item.content, "retained evidence", canonical=True)
        except CorrectionRefusal:
            continue
        if value.get("grammar") == _RUN_GRAMMAR:
            run_candidates.append(_validate_program(value))
    if len(run_candidates) != 1:
        raise _refuse(
            CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
            "history must retain one exact correction run program",
        )
    program = run_candidates[0]
    artifact_ids = _object(program.get("artifact_ids"), "retained artifact IDs")
    entrypoint_id = _text(
        artifact_ids.get("check_entrypoint"), "check entrypoint artifact ID"
    )
    entrypoint = retained.get(entrypoint_id)
    if entrypoint is None:
        raise _refuse(
            CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
            "history lacks the retained check entrypoint",
        )
    if (
        entrypoint.role != "RETAINED_EVIDENCE"
        or entrypoint.identity != _digest(entrypoint_bytes)
    ):
        raise _refuse(
            CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
            "active check entrypoint differs from retained bytes",
        )
    check_contracts: dict[str, Mapping[str, object]] = {}
    for key in ("source_mapping_check", "structural_check"):
        contract_id = _text(artifact_ids.get(key), f"{key} artifact ID")
        artifact = retained.get(contract_id)
        if artifact is None:
            raise _refuse(
                CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
                f"history lacks retained check contract: {contract_id}",
            )
        if artifact.role != "RETAINED_EVIDENCE":
            raise _refuse(
                CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
                "check contract must be retained evidence",
            )
        contract = _check_contract(
            artifact.content,
            entrypoint_id=entrypoint_id,
            entrypoint_identity=entrypoint.identity,
            shape_reason=CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
            identity_reason=CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
        )
        check_contracts[artifact.identity] = contract
    stages = _array(program.get("stages"), "retained run stages")
    expected_change_ids = []
    for raw_stage in stages:
        stage = _object(raw_stage, "retained run stage")
        expected_change_ids.append(
            _text(stage.get("change_set_id"), "retained stage change ID")
        )
    if [change.change_set_id for change in replay.change_sets] != expected_change_ids:
        raise _refuse(
            CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
            "history does not contain the exact declared change sequence",
        )
    changes_by_identity = {change.identity: change for change in replay.change_sets}
    proposals = {
        record.record_id: record
        for record in replay.machine_state.records
        if record.record_type == "ProposalRecord"
    }
    checks = [
        record
        for record in replay.machine_state.records
        if record.record_type == "CheckRecord"
    ]
    if len(checks) != 2 * len(replay.change_sets):
        raise _refuse(
            CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
            "history lacks the exact required check receipts",
        )
    for check in checks:
        receipt_id = check.fields.get("receipt_identity")
        artifact = retained.get(receipt_id)
        if artifact is None or artifact.identity != receipt_id:
            raise _refuse(
                CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
                "protocol check does not reference retained receipt bytes",
            )
        parsed_receipt = _check_receipt(
            artifact.content,
            retained_role=artifact.role,
            reason=CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
        )
        receipt = parsed_receipt.data
        contract_identity = check.fields.get("check_contract_identity")
        contract = check_contracts.get(contract_identity)
        if contract is None or not isinstance(contract_identity, str):
            raise _refuse(
                CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
                "protocol check lacks its retained contract",
            )
        proposal = proposals.get(check.fields.get("proposal_id"))
        if proposal is None:
            raise _refuse(
                CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
                "check receipt lacks its proposal",
            )
        change = changes_by_identity.get(
            proposal.fields.get("knowledge_change_set_identity")
        )
        if change is None:
            raise _refuse(
                CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
                "check receipt lacks its accepted change",
            )
        _verify_receipt_semantics(
            parsed_receipt,
            replay=replay,
            program=program,
            change=change,
            contract=contract,
            contract_identity=contract_identity,
            reason=CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
        )
        if (
            receipt.get("outcome") != check.fields.get("outcome")
            or receipt.get("check_contract_id")
            != check.fields.get("check_contract_id")
            or receipt.get("check_contract_identity") != contract_identity
        ):
            raise _refuse(
                CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
                "retained receipt content differs from its protocol record",
            )
    return program


def _verify_source_mapping(
    replay: KnowledgeHistoryReplay,
    program: Mapping[str, object],
    change: KnowledgeChangeSet,
    *,
    reason: CorrectionRefusalReason,
) -> _SourceMappingVerification:
    retained = {item.record_id: item for item in replay.retained_inputs}
    artifact_ids = _object(program.get("artifact_ids"), "retained artifact IDs")
    baseline_id = _text(
        artifact_ids.get("baseline_mapping"), "baseline mapping artifact ID"
    )
    correction_id = _text(
        artifact_ids.get("correction_mapping"), "correction mapping artifact ID"
    )
    try:
        baseline_artifact = retained[baseline_id]
        correction_artifact = retained[correction_id]
    except KeyError as error:
        raise _refuse(
            reason,
            f"history lacks retained mapping: {error.args[0]}",
        ) from error
    try:
        baseline_mapping = Ret010Mapping.from_bytes(baseline_artifact.content)
    except Ret010Refusal as error:
        raise _refuse(reason, f"retained baseline mapping is invalid: {error}") from error
    baseline = baseline_mapping.data
    correction = _json(
        correction_artifact.content, "retained correction mapping", canonical=False
    )
    baseline_config = _object(program.get("baseline"), "baseline configuration")
    correction_config = _object(
        program.get("correction"), "correction configuration"
    )
    baseline_prefix = _text(
        baseline_config.get("source_id_prefix"), "baseline source prefix"
    )
    correction_prefix = _text(
        correction_config.get("source_id_prefix"), "correction source prefix"
    )
    def selected(
        source_id: str,
        ordinal: int,
        ordinal_base: int,
        record_order: object,
        mapping_id: str,
        mapping_identity: str,
    ) -> Mapping[str, object]:
        try:
            source = retained[source_id]
        except KeyError as error:
            raise _refuse(
                reason,
                f"history lacks selected source member: {source_id}",
            ) from error
        lines = tuple(line for line in source.content.splitlines() if line.strip())
        index = ordinal - ordinal_base
        if index < 0 or index >= len(lines):
            raise _refuse(
                reason,
                "retained source ordinal lies outside its member",
            )
        return MappingProxyType(
            {
                "mapping_artifact_id": mapping_id,
                "mapping_sha256": mapping_identity,
                "member": source_id,
                "member_sha256": source.identity,
                "ordinal": ordinal,
                "ordinal_base": ordinal_base,
                "record_order": _text(record_order, "source record order"),
                "record_sha256": _digest(lines[index]),
            }
        )

    matching_stages = tuple(
        _object(raw_stage, "run stage")
        for raw_stage in _array(program.get("stages"), "run stages")
        if _object(raw_stage, "run stage").get("change_set_id")
        == change.change_set_id
    )
    if len(matching_stages) != 1:
        raise _refuse(reason, "change does not select one retained mapping stage")
    selector = matching_stages[0].get("mapping_change")

    if selector == "BASELINE":
        sources = {
            record_id.removeprefix(baseline_prefix): item.content
            for record_id, item in retained.items()
            if item.role == "RETAINED_SOURCE" and record_id.startswith(baseline_prefix)
        }
        try:
            verified = _verify_source_values(sources, baseline_mapping)
        except Ret010Refusal as error:
            raise _refuse(
                reason, f"baseline source and mapping do not conform: {error}"
            ) from error
        selection_config = _object(baseline.get("selection"), "baseline selection")
        source_id = baseline_prefix + "input/" + _text(
            verified.selection.get("source_member"), "baseline selected source member"
        )
        ordinal = _integer(
            verified.selection.get("source_record_ordinal"), "baseline source ordinal"
        )
        ordinal_base = _integer(
            selection_config.get("ordinal_base"), "baseline ordinal base"
        )
        record_order = selection_config.get("record_order")
        change_config = _object(baseline.get("change_set"), "baseline change")
        expected_change_id = _text(
            change_config.get("change_set_id"), "baseline change ID"
        )
        expected_operations = _plain(
            _array(baseline.get("operations"), "baseline operations")
        )
        expected_sources = tuple(
            (baseline_prefix + identifier, identity)
            for identifier, identity in verified.source_identities
        )
        expected_supersedes = tuple(
            _text(item, "baseline supersession ID")
            for item in _array(change_config.get("supersedes"), "baseline supersedes")
        )
        expected_valid_time = {
            "kind": "INSTANT",
            "value": verified.valid_time,
        }
        mapping_id = baseline_id
        mapping_identity = baseline_artifact.identity
    else:
        if not isinstance(selector, int) or isinstance(selector, bool):
            raise _refuse(reason, "retained stage mapping selector is unsupported")
        correction_changes = _array(correction.get("changes"), "correction changes")
        if selector < 0 or selector >= len(correction_changes):
            raise _refuse(reason, "retained stage selects an absent correction")
        mapped_change = _object(correction_changes[selector], "correction change")
        correction_source = _object(correction.get("source"), "correction source")
        source_id = correction_prefix + "input/" + _text(
            correction_source.get("member"), "correction source member"
        )
        ordinal = _integer(
            mapped_change.get("source_record_ordinal"), "correction source ordinal"
        )
        ordinal_base = _integer(
            correction_source.get("ordinal_base"), "correction ordinal base"
        )
        record_order = correction_source.get("record_order")
        try:
            source = retained[source_id]
            rows = tuple(line for line in source.content.splitlines() if line.strip())
            row = _json(
                rows[ordinal - ordinal_base],
                "retained correction source row",
                canonical=False,
            )
        except (IndexError, KeyError) as error:
            raise _refuse(reason, "retained correction source selection is invalid") from error
        selection_id = correction_prefix + "input/" + _text(
            correction.get("selection_member"), "correction selection member"
        )
        try:
            selection_artifact = retained[selection_id]
        except KeyError as error:
            raise _refuse(reason, "history lacks correction selection") from error
        selection = _json(
            selection_artifact.content,
            "retained correction selection",
            canonical=False,
        )
        if (
            selection.get("source_member") != correction_source.get("member")
            or selection.get("ordinal_base") != ordinal_base
            or selection.get("record_order") != record_order
            or selection.get("temporal_semantics") != "ORDER_ONLY"
        ):
            raise _refuse(
                reason,
                "retained selection and correction mapping conventions disagree",
            )
        initial = _object(selection.get("initial"), "initial source selection")
        corrected = _object(
            selection.get("correction"), "correction source selection"
        )
        row_event = _text(row.get("event_id"), "selected source event ID")
        expected_prior_record_id: str | None
        if ordinal == _integer(
            initial.get("source_record_ordinal"), "initial source ordinal"
        ):
            if row_event != _text(initial.get("event_id"), "initial event ID"):
                raise _refuse(reason, "initial selection differs from its source row")
            expected_supersedes = ()
            expected_prior_record_id = None
        elif ordinal == _integer(
            corrected.get("source_record_ordinal"), "correction source ordinal"
        ):
            if row_event != _text(corrected.get("event_id"), "correction event ID"):
                raise _refuse(reason, "correction selection differs from its source row")
            earlier_event = _text(
                corrected.get("supersedes_event_id"), "superseded event ID"
            )
            predecessors = tuple(
                _object(item, "predecessor change")
                for item in correction_changes
                if _object(item, "predecessor change").get(
                    "source_record_ordinal"
                )
                == initial.get("source_record_ordinal")
            )
            if len(predecessors) != 1 or earlier_event != initial.get("event_id"):
                raise _refuse(reason, "correction lacks one selected predecessor")
            predecessor = predecessors[0]
            expected_supersedes = (
                _text(predecessor.get("change_set_id"), "predecessor change ID"),
            )
            predecessor_operations = _array(
                predecessor.get("operations"), "predecessor operations"
            )
            if len(predecessor_operations) != 1:
                raise _refuse(reason, "predecessor must contain one operation")
            expected_prior_record_id = _text(
                _object(
                    predecessor_operations[0], "predecessor operation"
                ).get("record_id"),
                "predecessor record ID",
            )
        else:
            raise _refuse(reason, "change does not select an admitted source role")
        operations = _array(mapped_change.get("operations"), "correction operations")
        if len(operations) != 1:
            raise _refuse(reason, "correction mapping must select one operation")
        operation = _object(operations[0], "correction operation")
        properties = _object(operation.get("properties"), "operation properties")
        source_fields = []
        property_fields = []
        bindings = _array(correction.get("state_bindings"), "state bindings")
        for raw_binding in bindings:
            binding = _object(raw_binding, "state binding")
            if set(binding) != {"source_field", "target_path"}:
                raise _refuse(reason, "state binding fields are not closed")
            source_field = _text(binding.get("source_field"), "source field")
            target_path = _array(binding.get("target_path"), "target path")
            if len(target_path) != 2 or target_path[0] != "properties":
                raise _refuse(reason, "state binding must target one operation property")
            property_field = _text(target_path[1], "target property")
            source_fields.append(source_field)
            property_fields.append(property_field)
            if (
                source_field not in row
                or property_field not in properties
                or properties[property_field] != row[source_field]
            ):
                raise _refuse(
                    reason,
                    f"mapped change differs from retained source field: {source_field}",
                )
        if (
            len(source_fields) != len(set(source_fields))
            or len(property_fields) != len(set(property_fields))
            or set(source_fields) != set(row)
            or set(property_fields) != set(properties)
        ):
            raise _refuse(
                reason,
                "state bindings must uniquely cover every source field and property",
            )
        if (
            expected_prior_record_id is None
            and operation.get("supersedes_record_id") is not None
        ) or (
            expected_prior_record_id is not None
            and operation.get("supersedes_record_id") != expected_prior_record_id
        ):
            raise _refuse(
                reason,
                "mapped operation supersession differs from retained selection",
            )
        manifest_id = correction_prefix + "input/manifest.json"
        try:
            manifest_artifact = retained[manifest_id]
        except KeyError as error:
            raise _refuse(reason, "history lacks correction manifest") from error
        if manifest_artifact.identity != correction.get("input_manifest_sha256"):
            raise _refuse(reason, "correction manifest differs from mapping")
        manifest = _json(
            manifest_artifact.content, "retained correction manifest", canonical=False
        )
        declared_ids = {manifest_id}
        for raw_member in _array(manifest.get("members"), "manifest members"):
            member = _object(raw_member, "manifest member")
            record_id = correction_prefix + "input/" + _text(
                member.get("path"), "manifest member path"
            )
            declared_ids.add(record_id)
            item = retained.get(record_id)
            if (
                item is None
                or item.role != "RETAINED_SOURCE"
                or item.identity != member.get("sha256")
                or len(item.content) != member.get("byte_length")
            ):
                raise _refuse(reason, f"retained source differs from manifest: {record_id}")
        expected_sources = tuple(
            (record_id, retained[record_id].identity)
            for record_id in sorted(declared_ids)
        )
        expected_change_id = _text(
            mapped_change.get("change_set_id"), "correction change ID"
        )
        expected_operations = _plain(operations)
        if tuple(
            _text(item, "correction supersession ID")
            for item in _array(mapped_change.get("supersedes"), "supersedes")
        ) != expected_supersedes:
            raise _refuse(
                reason,
                "mapped change supersession differs from retained selection",
            )
        expected_valid_time = {"kind": "ORDER_ONLY", "value": row_event}
        mapping_id = correction_id
        mapping_identity = correction_artifact.identity

    provenance = selected(
        source_id,
        ordinal,
        ordinal_base,
        record_order,
        mapping_id,
        mapping_identity,
    )
    if (
        change.change_set_id != expected_change_id
        or _plain(change.data["operations"]) != expected_operations
        or change.sources != expected_sources
        or change.supersedes != expected_supersedes
        or _plain(change.data["valid_time"]) != expected_valid_time
    ):
        raise _refuse(
            reason,
            "accepted change differs from its retained source and mapping program",
        )
    return _SourceMappingVerification(
        selected_source=provenance,
        result=MappingProxyType(
            {
                "mapping_sha256": mapping_identity,
                "selected_record_sha256": provenance["record_sha256"],
                "verified_operation_count": len(change.operations),
            }
        ),
    )


def _explanation(
    replay: KnowledgeHistoryReplay, program: Mapping[str, object]
) -> bytes:
    history = []
    for record_id in sorted(replay.record_history):
        item = replay.record_history[record_id]
        history.append(
            {
                "change_set_id": item.change_set_id,
                "record_id": record_id,
                "record_type": item.operation.record_type,
                "superseded_by": item.superseded_by,
                "supersedes_record_id": item.supersedes_record_id,
                "valid_from": {
                    "kind": item.valid_from.kind,
                    "value": item.valid_from.value,
                },
                "valid_to": (
                    {"kind": item.valid_to.kind, "value": item.valid_to.value}
                    if item.valid_to is not None
                    else None
                ),
            }
        )
    checks = []
    for record in replay.machine_state.records:
        if record.record_type != "CheckRecord":
            continue
        checks.append(
            {
                "check_contract_id": record.fields["check_contract_id"],
                "outcome": record.fields["outcome"],
                "proposal_id": record.fields["proposal_id"],
                "receipt_identity": record.fields["receipt_identity"],
            }
        )
    checks.sort(key=lambda value: (value["proposal_id"], value["check_contract_id"]))
    snapshot = replay.graph.snapshot()
    selected_sources = {
        change.change_set_id: _verify_source_mapping(
            replay,
            program,
            change,
            reason=CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
        ).selected_source
        for change in replay.change_sets
    }
    value = {
        "changes": [
            {
                "change_set_id": change.change_set_id,
                "identity": change.identity,
                "selected_source": _plain(selected_sources[change.change_set_id]),
                "source_closure": [
                    {"sha256": identity, "source_id": identifier}
                    for identifier, identity in change.sources
                ],
                "supersedes": list(change.supersedes),
                "valid_time": {
                    "kind": change.valid_time.kind,
                    "value": change.valid_time.value,
                },
            }
            for change in replay.change_sets
        ],
        "checks": checks,
        "claim": program["claim"],
        "contract": {
            "effective_contract_identity": replay.partial_contract.identity,
            "history_binding_identity": replay.binding.identity,
            "machine_identity": replay.partial_contract.normative_profile.protocol_machine_program.identity,
            "validated_fact_set_identity": snapshot["ontology_hash"],
        },
        "current_graph": {
            "record_ids": [
                *(node["id"] for node in snapshot["nodes"]),
                *(relation["key"] for relation in snapshot["relations"]),
            ],
            "state_digest": replay.graph.state_digest(),
        },
        "history": {
            "acceptance_head": replay.acceptance_head,
            "event_count": replay.ledger_event_count,
            "ledger_head": replay.ledger_head,
            "materialization_head": replay.materialization_head,
            "records": history,
        },
        "limitations": _plain(program["limitations"]),
        "schema": "malleus.small-shop.correction-explanation/private-v0",
    }
    return _canonical(value)


def _write_outputs(
    output: Path,
    replay: KnowledgeHistoryReplay,
    program: Mapping[str, object],
) -> CorrectionRun:
    _refuse_output_symlinks(output, program)
    outputs = _object(program.get("outputs"), "output names")
    receipt_bytes = replay.receipt.canonical_bytes
    graph_bytes = _canonical(replay.graph.snapshot())
    explanation_bytes = _explanation(replay, program)
    for key, content in (
        ("receipt", receipt_bytes),
        ("graph", graph_bytes),
        ("explanation", explanation_bytes),
    ):
        (output / _text(outputs.get(key), f"{key} output name")).write_bytes(content)
    return CorrectionRun(replay, receipt_bytes, graph_bytes, explanation_bytes)


def run_correction(
    output: Path,
    *,
    correction_fixture: Path | None = None,
    correction_mapping: Path | None = None,
    entrypoint_path: Path | None = None,
    checks_root: Path = _CHECKS,
    program_path: Path = _PROGRAM,
) -> CorrectionRun:
    """Create or reopen the exact bounded proof and derive its three views."""
    output = Path(output)
    correction_fixture = (
        Path(correction_fixture) if correction_fixture is not None else None
    )
    correction_mapping = (
        Path(correction_mapping) if correction_mapping is not None else None
    )
    active_entrypoint = Path(entrypoint_path) if entrypoint_path else Path(__file__)
    entrypoint_bytes = _read(active_entrypoint, "active check entrypoint")
    checks_root = Path(checks_root)
    program_path = Path(program_path)
    history_path = output / "history.jsonl"
    if output.is_symlink() or history_path.is_symlink():
        raise _refuse(
            CorrectionRefusalReason.MALFORMED_CONFIGURATION,
            "history path must not be a symbolic link",
        )
    if history_path.exists():
        try:
            replay = KnowledgeChangeHistory.reopen(history_path).replay()
        except KnowledgeChangeRefusal as error:
            raise _refuse(
                CorrectionRefusalReason.INCOMPATIBLE_HISTORY,
                f"existing history cannot replay: {error}",
            ) from error
        program = _validate_replay(replay, entrypoint_bytes=entrypoint_bytes)
        return _write_outputs(output, replay, program)

    config = _load_configuration(
        program_path=program_path,
        correction_fixture=correction_fixture,
        correction_mapping=correction_mapping,
        entrypoint_bytes=entrypoint_bytes,
        checks_root=checks_root,
    )
    _refuse_output_symlinks(output, config.program)
    output.mkdir(parents=True, exist_ok=True)
    history = KnowledgeChangeHistory(
        history_path,
        partial_contract=config.effective_contract,
        contract_view=config.compilation.view,
        binding=config.binding,
    )
    _bootstrap(history, config)
    replay = history.replay()
    for stage in _stages(config):
        replay = _admit_stage(history, config, stage)
    program = _validate_replay(replay, entrypoint_bytes=entrypoint_bytes)
    return _write_outputs(output, replay, program)


def main(argv: tuple[str, ...] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args(argv)
    result = run_correction(arguments.output)
    sys.stdout.buffer.write(result.explanation_bytes + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
