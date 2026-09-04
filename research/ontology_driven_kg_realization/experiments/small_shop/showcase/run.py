"""Run the retained five-stage Small Shop source-to-ledger-to-graph proof."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from enum import Enum, auto
from hashlib import sha256
from importlib.resources import files
from io import StringIO
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
    compile_binding,
)
from malleus._contract_pipeline.knowledge import (
    KnowledgeAnchorInput,
    KnowledgeChangeHistory,
    KnowledgeChangeRefusal,
    KnowledgeChangeSet,
    KnowledgeHistoryReplay,
    KnowledgeOperation,
    KnowledgeValidTime,
)
from malleus._contract_pipeline.machine import (
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
from malleus.ledger import LedgerError, aware_datetime
from research.ontology_driven_kg_realization.experiments.small_shop.pareto.ret010 import (
    Ret010Refusal,
    load_ret010_vertical,
)


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
PROGRAM = HERE / "run.json"
RUN_GRAMMAR = "malleus.small-shop.showcase-run/private-v0"
SETTLEMENT_GRAMMAR = "malleus.small-shop.settlement-mapping/private-v0"
CORRECTION_GRAMMAR = "malleus.small-shop.supplier-order-correction-mapping/private-v0"
RECEIPT_GRAMMAR = "malleus.small-shop.source-mapping-receipt/private-v0"
CHECK_GRAMMAR = "malleus.check-contract/private-v0"
CHECK_ID = "source-mapping-conformance"
CHECK_ALGORITHM = "RECOMPUTE_DECLARED_SOURCE_TO_CHANGE_SET"
CHECK_OUTCOMES = ("SATISFIED", "VIOLATED")
SELECTORS = (
    "RET010",
    "SETTLEMENT:0",
    "SETTLEMENT:1",
    "CORRECTION:0",
    "CORRECTION:1",
)
PROGRAM_FIELDS = {
    "actor_id",
    "artifact_ids",
    "decisions",
    "grammar",
    "history_binding",
    "inputs",
    "limitations",
    "outputs",
    "policy_ref",
    "stages",
    "transaction_time",
}
STAGE_FIELDS = {
    "change_set_id",
    "decision_id",
    "proposal_id",
    "receipt_id",
    "selector",
    "transaction_time",
}
DECISIONS = {
    "accepted_query_surface": {
        "choice": "CUSTOM_READ_ONLY_QUERY_FACADE",
        "deferred": "CYPHER_ADAPTER",
    },
    "history_shape": {
        "choice": "FRESH_SINGLE_CONTRACT_FIVE_STAGE_HISTORY",
        "order_basis": "FROZEN_RET_TEST_LADDER_NOT_BUSINESS_EVENT_CHRONOLOGY",
    },
    "invoice_valid_time": {
        "choice": "ORDER_ONLY",
        "meaning": "FIXTURE_ORCHESTRATION_NOT_SOURCE_EVENT_OR_TIMESTAMP",
        "value": "fixture:invoice-base-before-e30",
    },
    "provenance_granularity": {
        "choice": "CHANGE_LEVEL_SOURCE_AND_EVIDENCE_CLOSURE",
        "deferred": "OPERATION_LEVEL_PROVENANCE",
    },
    "scoring": {
        "choice": "EXCLUDED",
        "meaning": "NO_EVALUATOR_OR_ANSWER_COMPARISON_IN_CORE_SHOWCASE",
    },
    "source_arrival_model": {
        "choice": "PREPROVISIONED_BOOTSTRAP",
        "deferred": "STAGE_WISE_SOURCE_REGISTRATION_AND_OBSERVATION",
        "meaning": "STAGED_ADMISSION_NOT_LIVE_OBSERVATION",
    },
    "transaction_prefix_read": {
        "choice": "DEFERRED",
        "meaning": "GRAPH_AT_ACCEPTED_CHANGE_ONLY",
    },
}


class ShowcaseRefusalReason(Enum):
    MISSING_INPUT = auto()
    MALFORMED_CONFIGURATION = auto()
    IDENTITY_MISMATCH = auto()
    SOURCE_MISMATCH = auto()
    SOURCE_MAPPING_FAILED = auto()
    CONTRACT_COMPILATION_FAILED = auto()
    ADMISSION_FAILED = auto()
    INCOMPATIBLE_HISTORY = auto()


class ShowcaseRefusal(ValueError):
    def __init__(self, reason: ShowcaseRefusalReason, detail: str) -> None:
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.name}: {detail}")


def refuse(reason: ShowcaseRefusalReason, detail: str) -> ShowcaseRefusal:
    return ShowcaseRefusal(reason, detail)


def canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [plain(item) for item in value]
    return value


def read(path: Path, label: str) -> bytes:
    try:
        return path.read_bytes()
    except FileNotFoundError as error:
        raise refuse(ShowcaseRefusalReason.MISSING_INPUT, f"missing {label}") from error


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate key: {key}")
        value[key] = item
    return value


def reject_json_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant: {value}")


def decode(source: bytes, label: str, *, require_canonical: bool = False) -> dict:
    try:
        value = json.loads(
            source,
            object_pairs_hook=unique_object,
            parse_constant=reject_json_constant,
        )
        encoded = canonical(value) if require_canonical else None
    except (UnicodeError, ValueError, json.JSONDecodeError) as error:
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
            f"{label} is not closed JSON",
        ) from error
    if not isinstance(value, dict) or (require_canonical and encoded != source):
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
            f"{label} is not a canonical object",
        )
    return value


def obj(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION, f"{label} is not an object"
        )
    return value


def array(value: object, label: str) -> tuple:
    if not isinstance(value, (list, tuple)):
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION, f"{label} is not an array"
        )
    return tuple(value)


def text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION, f"{label} is required"
        )
    return value


def integer(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION, f"{label} is not an integer"
        )
    return value


def relative(value: object, label: str) -> str:
    result = text(value, label)
    path = PurePosixPath(result)
    if path.is_absolute() or ".." in path.parts:
        raise refuse(ShowcaseRefusalReason.MALFORMED_CONFIGURATION, f"unsafe {label}")
    return result


def at(value: object, path: tuple, label: str) -> object:
    current = value
    for part in path:
        try:
            current = current[part]  # type: ignore[index]
        except (IndexError, KeyError, TypeError) as error:
            raise refuse(
                ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
                f"{label} path does not resolve",
            ) from error
    return current


@dataclass(frozen=True, slots=True)
class Bundle:
    name: str
    prefix: str
    mapping_id: str
    mapping_bytes: bytes
    mapping: Mapping[str, object]
    sources: Mapping[str, bytes]
    media_types: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class Stage:
    selector: str
    change_set_id: str
    operations: tuple[KnowledgeOperation, ...]
    sources: tuple[str, ...]
    evidence: tuple[str, ...]
    supersedes: tuple[str, ...]
    valid_time: KnowledgeValidTime
    mapping_id: str
    mapping_identity: str
    declaration: Mapping[str, object]
    bundle: Bundle


@dataclass(slots=True)
class PreparedShowcase:
    history: KnowledgeChangeHistory
    program: Mapping[str, object]
    policy: PolicyProgram
    check: SourceMappingCheck
    stages: tuple[Stage, ...]


@dataclass(frozen=True, slots=True)
class ShowcaseRun:
    replay: KnowledgeHistoryReplay
    graph_bytes: bytes
    receipt_bytes: bytes


@dataclass(frozen=True, slots=True)
class VerifiedSourceMappingReceipt:
    change_set_id: str
    receipt_identity: str


@dataclass(frozen=True, slots=True)
class SourceMappingCheck:
    identifier: str
    identity: str
    source: bytes


class ExactResolver:
    def __init__(self, values: Mapping[str, tuple[bytes, str]]) -> None:
        self.values = values

    def resolve(self, request: RootRequest | ImportRequest) -> ResolvedSource:
        locator = (
            request.requested_locator
            if isinstance(request, RootRequest)
            else request.literal_import
        )
        try:
            source, media_type = self.values[locator]
        except KeyError as error:
            raise CollaboratorRefusal(locator) from error
        return ResolvedSource(locator, source, media_type)


def validate_program(source: bytes) -> Mapping[str, object]:
    value = decode(source, "run program", require_canonical=True)
    decisions = obj(value.get("decisions"), "decisions")
    if (
        set(value) != PROGRAM_FIELDS
        or value.get("grammar") != RUN_GRAMMAR
        or decisions != DECISIONS
    ):
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION, "unsupported run program"
        )
    declared = tuple(
        obj(item, f"stage {index}")
        for index, item in enumerate(array(value.get("stages"), "stages"))
    )
    if tuple(item.get("selector") for item in declared) != SELECTORS:
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION, "wrong five-stage order"
        )
    try:
        prior_time = aware_datetime(
            text(value.get("transaction_time"), "bootstrap transaction time"),
            "bootstrap transaction time",
        )
        for index, item in enumerate(declared):
            if set(item) != STAGE_FIELDS:
                raise refuse(
                    ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
                    f"stage {index} has the wrong fields",
                )
            for field in (
                "change_set_id",
                "decision_id",
                "proposal_id",
                "receipt_id",
                "selector",
            ):
                text(item.get(field), f"stage {index} {field}")
            transaction_time = aware_datetime(
                text(item.get("transaction_time"), f"stage {index} transaction time"),
                f"stage {index} transaction time",
            )
            if transaction_time < prior_time:
                raise refuse(
                    ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
                    "stage transaction time decreased",
                )
            prior_time = transaction_time
    except LedgerError as error:
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION, str(error)
        ) from error
    return MappingProxyType(value)


def validate_check(
    source: bytes, *, entrypoint_id: str, entrypoint_identity: str
) -> SourceMappingCheck:
    value = decode(source, "source-mapping check", require_canonical=True)
    executor = obj(value.get("executor"), "check executor")
    if (
        set(value)
        != {"algorithm", "check_contract_id", "executor", "grammar", "outcomes"}
        or set(executor) != {"artifact_id", "sha256"}
        or value.get("grammar") != CHECK_GRAMMAR
        or value.get("check_contract_id") != CHECK_ID
        or value.get("algorithm") != CHECK_ALGORITHM
        or tuple(array(value.get("outcomes"), "check outcomes")) != CHECK_OUTCOMES
        or executor != {"artifact_id": entrypoint_id, "sha256": entrypoint_identity}
    ):
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
            "unsupported source-mapping check contract",
        )
    return SourceMappingCheck(
        text(value.get("check_contract_id"), "check contract ID"),
        digest(source),
        source,
    )


def pinned(
    config: Mapping[str, object], label: str, override: Path | None = None
) -> tuple[Path, bytes]:
    path = override or ROOT / relative(config.get("path"), f"{label} path")
    source = read(path, label)
    if digest(source) != config.get("sha256"):
        raise refuse(
            ShowcaseRefusalReason.IDENTITY_MISMATCH, f"{label} digest mismatch"
        )
    return path, source


def verify_manifest(sources: Mapping[str, bytes], expected: object) -> None:
    try:
        manifest_bytes = sources["input/manifest.json"]
    except KeyError as error:
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MISMATCH, "fixture manifest is missing"
        ) from error
    if digest(manifest_bytes) != expected:
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MISMATCH, "fixture manifest digest mismatch"
        )
    manifest = decode(manifest_bytes, "fixture manifest")
    members = {"input/manifest.json"}
    for raw in array(manifest.get("members"), "manifest members"):
        member = obj(raw, "manifest member")
        identifier = "input/" + relative(member.get("path"), "manifest path")
        members.add(identifier)
        content = sources.get(identifier)
        if (
            content is None
            or digest(content) != member.get("sha256")
            or len(content) != member.get("byte_length")
        ):
            raise refuse(
                ShowcaseRefusalReason.SOURCE_MISMATCH,
                f"manifest member drift: {identifier}",
            )
    if set(sources) != members:
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MISMATCH,
            "fixture member set differs from manifest",
        )


def manifest_media_types(sources: Mapping[str, bytes]) -> Mapping[str, str]:
    manifest = decode(sources["input/manifest.json"], "fixture manifest")
    result = {"input/manifest.json": "application/json"}
    for raw in array(manifest.get("members"), "manifest members"):
        member = obj(raw, "manifest member")
        result["input/" + relative(member.get("path"), "manifest path")] = text(
            member.get("media_type"), "media type"
        )
    if set(result) != set(sources):
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MISMATCH,
            "fixture media types differ from retained members",
        )
    return MappingProxyType(result)


def fixture_bundle(
    root: Path, name: str, prefix: str, mapping_id: str, mapping_bytes: bytes
) -> Bundle:
    mapping = decode(
        mapping_bytes, f"{name} mapping", require_canonical=name == "settlement"
    )
    input_root = root / "input"
    manifest = read(input_root / "manifest.json", f"{name} manifest")
    manifest_value = decode(manifest, f"{name} manifest")
    sources = {"input/manifest.json": manifest}
    for raw in array(manifest_value.get("members"), "manifest members"):
        member = obj(raw, "manifest member")
        path = relative(member.get("path"), "manifest path")
        sources["input/" + path] = read(input_root / path, f"{name} member")
    verify_manifest(sources, mapping.get("input_manifest_sha256"))
    return Bundle(
        name,
        prefix,
        mapping_id,
        mapping_bytes,
        MappingProxyType(mapping),
        MappingProxyType(sources),
        manifest_media_types(sources),
    )


def retained_bundle(
    replay: KnowledgeHistoryReplay,
    program: Mapping[str, object],
    name: str,
    mapping_key: str,
) -> Bundle:
    retained = {item.record_id: item for item in replay.retained_inputs}
    ids = obj(program.get("artifact_ids"), "artifact IDs")
    config = obj(obj(program.get("inputs"), "inputs").get(name), name)
    prefix = text(config.get("source_prefix"), "source prefix")
    mapping_id = text(ids.get(mapping_key), "mapping ID")
    try:
        mapping_bytes = retained[mapping_id].content
    except KeyError as error:
        raise refuse(
            ShowcaseRefusalReason.INCOMPATIBLE_HISTORY, f"missing {name} mapping"
        ) from error
    sources = {
        item.record_id.removeprefix(prefix): item.content
        for item in retained.values()
        if item.role == "RETAINED_SOURCE" and item.record_id.startswith(prefix)
    }
    media_types = {
        item.record_id.removeprefix(prefix): item.media_type
        for item in retained.values()
        if item.role == "RETAINED_SOURCE" and item.record_id.startswith(prefix)
    }
    mapping = decode(mapping_bytes, f"retained {name} mapping")
    verify_manifest(sources, mapping.get("input_manifest_sha256"))
    if set(media_types) != set(sources):
        raise refuse(
            ShowcaseRefusalReason.INCOMPATIBLE_HISTORY,
            f"retained {name} media types are incomplete",
        )
    return Bundle(
        name,
        prefix,
        mapping_id,
        mapping_bytes,
        MappingProxyType(mapping),
        MappingProxyType(sources),
        MappingProxyType(media_types),
    )


def compile_contract(mapping: Mapping[str, object], bundles: Mapping[str, Bundle]):
    config = obj(mapping.get("compiler"), "compiler")
    values = {}
    bundle_kinds = {
        "BASELINE_MEMBER": "baseline",
        "CORRECTION_MEMBER": "correction",
        "SETTLEMENT_MEMBER": "settlement",
    }
    for raw in array(config.get("sources"), "compiler sources"):
        item = obj(raw, "compiler source")
        kind = text(item.get("kind"), "source kind")
        locator = text(item.get("locator"), "source locator")
        media_type = text(item.get("media_type"), "media type")
        if kind in bundle_kinds:
            bundle = bundles[bundle_kinds[kind]]
            source = bundle.sources[
                "input/" + relative(item.get("path"), "source path")
            ]
        elif kind == "REPOSITORY_PATH":
            source = read(
                ROOT / relative(item.get("path"), "repository path"), "compiler source"
            )
        elif kind == "PACKAGE_RESOURCE":
            parts = tuple(
                text(part, "package path")
                for part in array(item.get("path"), "package path")
            )
            source = (
                files(text(item.get("package"), "package"))
                .joinpath(*parts)
                .read_bytes()
            )
        else:
            raise refuse(
                ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
                f"unsupported compiler source: {kind}",
            )
        if locator in values:
            raise refuse(
                ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
                "duplicate compiler locator",
            )
        values[locator] = (source, media_type)
    try:
        closure = build_source_closure(
            requested_locator=text(config.get("requested_locator"), "compiler root"),
            selection=ResolverSelection(
                resolver_id=text(config.get("resolver_id"), "resolver ID"),
                profile_version=text(config.get("profile_version"), "profile"),
                configuration_id=text(config.get("configuration_id"), "configuration"),
            ),
            resolver=ExactResolver(values),
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
        raise refuse(
            ShowcaseRefusalReason.CONTRACT_COMPILATION_FAILED, str(error)
        ) from error


def operation(raw: object) -> KnowledgeOperation:
    value = obj(raw, "operation")
    return KnowledgeOperation(
        integer(value.get("ordinal"), "ordinal"),
        text(value.get("operation_id"), "operation ID"),
        text(value.get("operation_type"), "operation type"),
        text(value.get("record_type"), "record type"),
        text(value.get("record_id"), "record ID"),
        MappingProxyType(dict(obj(value.get("properties"), "properties"))),
        tuple(
            text(item, "dependency")
            for item in array(value.get("depends_on"), "dependencies")
        ),
        value.get("source_id"),
        value.get("target_id"),
        value.get("supersedes_record_id"),
    )


def validate_correction_selection(bundle: Bundle) -> None:
    mapping = bundle.mapping
    changes = tuple(
        obj(item, "correction change")
        for item in array(mapping.get("changes"), "correction changes")
    )
    if len(changes) != 2:
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
            "correction mapping must contain two changes",
        )
    source = obj(mapping.get("source"), "correction source")
    initial_time = obj(changes[0].get("valid_time"), "initial valid time")
    correction_time = obj(changes[1].get("valid_time"), "correction valid time")
    expected = {
        "correction": {
            "event_id": correction_time.get("value"),
            "source_record_ordinal": changes[1].get("source_record_ordinal"),
            "supersedes_event_id": initial_time.get("value"),
        },
        "initial": {
            "event_id": initial_time.get("value"),
            "source_record_ordinal": changes[0].get("source_record_ordinal"),
        },
        "ordinal_base": source.get("ordinal_base"),
        "record_order": source.get("record_order"),
        "schema": "malleus.small-shop.correction-selection/v1",
        "selection_id": "SHOP-SUPPLIER-ORDER-CORRECTION",
        "source_member": source.get("member"),
        "temporal_semantics": "ORDER_ONLY",
    }
    selection_member = "input/" + relative(
        mapping.get("selection_member"), "correction selection member"
    )
    selection = decode(bundle.sources[selection_member], "correction selection")
    if (
        selection != expected
        or initial_time.get("kind") != "ORDER_ONLY"
        or correction_time.get("kind") != "ORDER_ONLY"
    ):
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "correction selection and mapping differ",
        )


def validate_settlement_selection(bundle: Bundle) -> None:
    mapping = bundle.mapping
    stages = tuple(
        obj(item, "settlement stage")
        for item in array(mapping.get("stages"), "settlement stages")
    )
    if len(stages) != 2:
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
            "settlement mapping must contain two stages",
        )
    invoice_operations = tuple(
        obj(item, "invoice operation")
        for item in array(stages[0].get("operations"), "invoice operations")
    )
    invoice_selections = tuple(
        obj(item, "invoice selection")
        for item in array(stages[0].get("selections"), "invoice selections")
    )
    payment_operations = tuple(
        obj(item, "payment operation")
        for item in array(stages[1].get("operations"), "payment operations")
    )
    payment_selections = tuple(
        obj(item, "payment selection")
        for item in array(stages[1].get("selections"), "payment selections")
    )
    if (
        len(invoice_operations) != 2
        or len(invoice_selections) != 2
        or len(payment_operations) != 3
        or len(payment_selections) != 1
    ):
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "fixed settlement mapping shape is incomplete",
        )
    invoice_members = {
        text(item.get("member"), "invoice source member") for item in invoice_selections
    }
    if len(invoice_members) != 1:
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "invoice selections use different source members",
        )
    invoice_ids = [
        obj(item.get("properties"), "invoice properties").get("invoice_number")
        for item in invoice_operations
    ]
    payment_time = obj(stages[1].get("valid_time"), "payment valid time")
    payment_properties = obj(
        payment_operations[0].get("properties"), "payment properties"
    )
    expected = {
        "event_id": payment_time.get("value"),
        "invoice_ids": invoice_ids,
        "invoice_record_ordinals": [
            item.get("record_ordinal") for item in invoice_selections
        ],
        "invoice_source_member": next(iter(invoice_members)),
        "ordinal_base": 0,
        "payment_id": payment_properties.get("payment_number"),
        "payment_record_ordinal": payment_selections[0].get("record_ordinal"),
        "payment_source_member": payment_selections[0].get("member"),
        "record_order": "SOURCE_ORDER",
        "schema": "malleus.small-shop.settlement-selection/v1",
        "selection_id": "SHOP-PAYMENT-SETTLEMENT",
        "settlement_semantics": "FIXTURE_DEFINED_DIRECTED_PAYMENT_TO_INVOICE",
        "temporal_semantics": "ORDER_ONLY",
    }
    selection_member = "input/" + relative(
        mapping.get("selection_member"), "settlement selection member"
    )
    selection = decode(bundle.sources[selection_member], "settlement selection")
    valid_times = tuple(
        obj(stage.get("valid_time"), "settlement valid time") for stage in stages
    )
    if selection != expected or any(
        item.get("kind") != "ORDER_ONLY" for item in valid_times
    ):
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "settlement selection and mapping differ",
        )


def mapped_stages(
    program: Mapping[str, object], bundles: Mapping[str, Bundle]
) -> tuple[Stage, ...]:
    baseline = bundles["baseline"]
    correction = bundles["correction"]
    settlement = bundles["settlement"]
    if (
        correction.mapping.get("grammar") != CORRECTION_GRAMMAR
        or settlement.mapping.get("grammar") != SETTLEMENT_GRAMMAR
    ):
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION, "unsupported mapping grammar"
        )
    validate_correction_selection(correction)
    validate_settlement_selection(settlement)
    raw: dict[str, tuple[Bundle, Mapping[str, object], str]] = {}
    base_change = obj(baseline.mapping.get("change_set"), "RET-010 change")
    raw["RET010"] = (
        baseline,
        {
            "change_set_id": base_change["change_set_id"],
            "operations": baseline.mapping["operations"],
            "supersedes": base_change["supersedes"],
            "valid_time": {"kind": "INSTANT", "value": baseline.mapping["valid_time"]},
        },
        "RET010",
    )
    for index, item in enumerate(
        array(correction.mapping.get("changes"), "correction changes")
    ):
        raw[f"CORRECTION:{index}"] = (
            correction,
            obj(item, "correction change"),
            "CORRECTION",
        )
    for index, item in enumerate(
        array(settlement.mapping.get("stages"), "settlement stages")
    ):
        raw[f"SETTLEMENT:{index}"] = (
            settlement,
            obj(item, "settlement stage"),
            "SETTLEMENT",
        )
    if set(raw) != set(SELECTORS):
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
            "mappings must define exactly the selected five stages",
        )
    ids = obj(program.get("artifact_ids"), "artifact IDs")
    common = tuple(
        text(ids.get(key), key)
        for key in (
            "validated_contract",
            "run_program",
            "entrypoint",
            "machine",
            "policy",
            "check_contract",
        )
    )
    result = []
    for declaration_raw in array(program.get("stages"), "run stages"):
        declaration = obj(declaration_raw, "run stage")
        selector = text(declaration.get("selector"), "selector")
        try:
            bundle, value, _ = raw[selector]
        except KeyError as error:
            raise refuse(
                ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
                f"unknown selector: {selector}",
            ) from error
        valid = obj(value.get("valid_time"), "valid time")
        change_id = text(value.get("change_set_id"), "change ID")
        if declaration.get("change_set_id") != change_id:
            raise refuse(
                ShowcaseRefusalReason.MALFORMED_CONFIGURATION,
                "run and mapping change IDs differ",
            )
        result.append(
            Stage(
                selector=selector,
                change_set_id=change_id,
                operations=tuple(
                    operation(item)
                    for item in array(value.get("operations"), "operations")
                ),
                sources=tuple(bundle.prefix + key for key in bundle.sources),
                evidence=(bundle.mapping_id, *common),
                supersedes=tuple(
                    text(item, "supersession")
                    for item in array(value.get("supersedes"), "supersedes")
                ),
                valid_time=KnowledgeValidTime(
                    text(valid.get("kind"), "valid kind"),
                    text(valid.get("value"), "valid value"),
                ),
                mapping_id=bundle.mapping_id,
                mapping_identity=digest(bundle.mapping_bytes),
                declaration=declaration,
                bundle=bundle,
            )
        )
    return tuple(result)


def records(source: bytes, parser: str) -> tuple[Mapping[str, object], ...]:
    if parser == "JSON_LINES":
        return tuple(
            MappingProxyType(decode(line, "JSON line"))
            for line in source.splitlines()
            if line.strip()
        )
    if parser == "CSV_HEADER":
        return tuple(
            MappingProxyType(dict(row))
            for row in csv.DictReader(StringIO(source.decode()))
        )
    raise refuse(
        ShowcaseRefusalReason.SOURCE_MAPPING_FAILED, f"unsupported parser: {parser}"
    )


def selected(
    bundle: Bundle, member: str, parser: str, ordinal: int
) -> tuple[Mapping[str, object], Mapping[str, object]]:
    identifier = "input/" + member
    try:
        source = bundle.sources[identifier]
        row = records(source, parser)[ordinal]
    except (IndexError, KeyError) as error:
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "source selection is outside retained bytes",
        ) from error
    return row, MappingProxyType(
        {
            "member": bundle.prefix + identifier,
            "member_sha256": digest(source),
            "ordinal": ordinal,
            "record_sha256": digest(canonical(plain(row))),
        }
    )


def verify_ret010(stage: Stage) -> tuple[Mapping[str, object], ...]:
    mapping = stage.bundle.mapping
    selection_config = obj(mapping.get("selection"), "RET-010 selection")
    selection = decode(
        stage.bundle.sources[
            "input/" + text(selection_config.get("member"), "selection member")
        ],
        "selection",
    )
    member = text(selection.get("source_member"), "source member")
    ordinal = integer(selection.get("source_record_ordinal"), "source ordinal")
    row, provenance = selected(
        stage.bundle,
        member,
        "JSON_LINES",
        ordinal - integer(selection_config.get("ordinal_base"), "ordinal base"),
    )
    for raw in array(selection_config.get("source_bindings"), "source bindings"):
        binding = obj(raw, "source binding")
        left = selection.get(text(binding.get("selection_field"), "selection field"))
        right = row.get(text(binding.get("source_field"), "source field"))
        if not (
            left == right
            if binding.get("comparison") == "EQUAL"
            else isinstance(right, list) and left in right
        ):
            raise refuse(
                ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
                "RET-010 selection differs from source",
            )
    lookup = obj(mapping.get("inventory_lookup"), "lookup")
    lookup_member = text(lookup.get("member"), "lookup member")
    lookup_rows = records(stage.bundle.sources["input/" + lookup_member], "CSV_HEADER")
    matches = [
        (index, item)
        for index, item in enumerate(lookup_rows)
        if item[text(lookup.get("key_field"), "key field")]
        == selection[text(lookup.get("selection_key_field"), "selection key")]
    ]
    if len(matches) != 1:
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "RET-010 lookup is not singular",
        )
    lookup_ordinal, lookup_row = matches[0]
    _, lookup_provenance = selected(
        stage.bundle, lookup_member, "CSV_HEADER", lookup_ordinal
    )
    context = {"selection": selection, "lookup": lookup_row}
    operations = array(mapping.get("operations"), "operations")
    for raw in array(mapping.get("operation_bindings"), "operation bindings"):
        binding = obj(raw, "operation binding")
        expected = at(context, array(binding.get("input_path"), "input path"), "input")
        actual = at(
            operations[integer(binding.get("operation_ordinal"), "ordinal")],
            array(binding.get("operation_path"), "operation path"),
            "operation",
        )
        if expected != actual:
            raise refuse(
                ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
                "RET-010 operation differs from source",
            )
    return provenance, lookup_provenance


def verify_correction(stage: Stage) -> tuple[Mapping[str, object], ...]:
    mapping = stage.bundle.mapping
    index = int(stage.selector.split(":")[1])
    change = obj(array(mapping.get("changes"), "changes")[index], "change")
    source = obj(mapping.get("source"), "source")
    ordinal = integer(change.get("source_record_ordinal"), "source ordinal")
    row, provenance = selected(
        stage.bundle,
        text(source.get("member"), "member"),
        "JSON_LINES",
        ordinal - integer(source.get("ordinal_base"), "ordinal base"),
    )
    operation_value = obj(array(change.get("operations"), "operations")[0], "operation")
    properties = obj(operation_value.get("properties"), "properties")
    bound_source, bound_properties = set(), set()
    for raw in array(mapping.get("state_bindings"), "state bindings"):
        binding = obj(raw, "state binding")
        source_field = text(binding.get("source_field"), "source field")
        target = array(binding.get("target_path"), "target path")
        target_field = text(target[-1], "property field")
        if row.get(source_field) != properties.get(target_field):
            raise refuse(
                ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
                "correction differs from source",
            )
        bound_source.add(source_field)
        bound_properties.add(target_field)
    if (
        bound_source != set(row)
        or bound_properties != set(properties)
        or stage.valid_time.value != row.get("event_id")
    ):
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "correction mapping is incomplete",
        )
    return (provenance,)


def verify_settlement(stage: Stage) -> tuple[Mapping[str, object], ...]:
    mapping = stage.bundle.mapping
    index = int(stage.selector.split(":")[1])
    value = obj(array(mapping.get("stages"), "stages")[index], "settlement stage")
    selections = array(value.get("selections"), "selections")
    expected_counts = ((2, 2), (1, 3))[index]
    if (len(selections), len(stage.operations)) != expected_counts:
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "fixed settlement shape is incomplete",
        )
    provenance = []
    raw_operations = array(value.get("operations"), "operations")
    for raw in selections:
        selection = obj(raw, "source selection")
        row, item = selected(
            stage.bundle,
            text(selection.get("member"), "member"),
            text(selection.get("parser"), "parser"),
            integer(selection.get("record_ordinal"), "ordinal"),
        )
        provenance.append(item)
        for binding_raw in array(selection.get("bindings"), "bindings"):
            binding = obj(binding_raw, "binding")
            source_value = at(
                row, array(binding.get("source_path"), "source path"), "source"
            )
            target = (
                value
                if "stage_path" in binding
                else raw_operations[
                    integer(binding.get("operation_ordinal"), "operation ordinal")
                ]
            )
            path = binding.get("stage_path", binding.get("operation_path"))
            actual = at(target, array(path, "target path"), "target")
            expected = (
                text(binding.get("prefix"), "prefix") + str(source_value)
                if binding.get("comparison") == "PREFIX"
                else source_value
            )
            if (
                binding.get("comparison") not in {"EQUAL", "PREFIX"}
                or actual != expected
            ):
                raise refuse(
                    ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
                    "settlement operation differs from source",
                )
    selection_bytes = stage.bundle.sources[
        "input/" + text(mapping.get("selection_member"), "selection member")
    ]
    declared = decode(selection_bytes, "settlement selection")
    if (
        declared.get("invoice_ids") != ["I1", "I2"]
        or declared.get("payment_id") != "P1"
        or declared.get("event_id") != "e30"
    ):
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "settlement selection is not P1 to I1/I2",
        )
    return tuple(provenance)


def verify_stage(stage: Stage) -> tuple[Mapping[str, object], ...]:
    if stage.selector == "RET010":
        return verify_ret010(stage)
    if stage.selector.startswith("CORRECTION:"):
        return verify_correction(stage)
    return verify_settlement(stage)


def event(event_type: str, payload: Mapping[str, object]) -> bytes:
    return canonical({"event_type": event_type, "payload": dict(payload)})


def artifact(
    record_id: str, content: bytes, media_type: str, role: str
) -> KnowledgeAnchorInput:
    return KnowledgeAnchorInput(
        machine_event=event(
            "ARTIFACT_REGISTERED",
            {"artifact_id": record_id, "artifact_identity": digest(content)},
        ),
        retained_bytes=content,
        media_type=media_type,
        role=role,
    )


def source_anchors(
    identifier: str, content: bytes, media_type: str
) -> tuple[KnowledgeAnchorInput, ...]:
    artifact_id = "artifact:small-shop-showcase:source:" + identifier
    identity = digest(content)
    return (
        artifact(artifact_id, content, media_type, "SOURCE_ARTIFACT"),
        KnowledgeAnchorInput(
            machine_event=event(
                "SOURCE_REGISTERED",
                {
                    "artifact_id": artifact_id,
                    "source_id": identifier,
                    "source_identity": identity,
                },
            ),
            retained_bytes=content,
            media_type=media_type,
            role="RETAINED_SOURCE",
        ),
    )


def bootstrap(
    history,
    program_bytes,
    program,
    compilation,
    contract,
    binding,
    machine_bytes,
    policy_bytes,
    check_bytes,
    bundles,
):
    ids = obj(program.get("artifact_ids"), "artifact IDs")
    values = (
        (
            "validated_contract",
            compilation.artifact.artifact_bytes,
            "application/json",
            "VALIDATED_CONTRACT",
        ),
        (
            "partial_contract",
            contract.canonical_bytes,
            "application/json",
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            "history_binding",
            binding.canonical_bytes,
            "application/json",
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        ("run_program", program_bytes, "application/json", "RETAINED_EVIDENCE"),
        (
            "entrypoint",
            read(Path(__file__), "entrypoint"),
            "text/x-python",
            "RETAINED_EVIDENCE",
        ),
        ("machine", machine_bytes, "application/json", "RETAINED_EVIDENCE"),
        ("policy", policy_bytes, "application/json", "RETAINED_EVIDENCE"),
        ("check_contract", check_bytes, "application/json", "RETAINED_EVIDENCE"),
        (
            "baseline_mapping",
            bundles["baseline"].mapping_bytes,
            "application/json",
            "RETAINED_EVIDENCE",
        ),
        (
            "correction_mapping",
            bundles["correction"].mapping_bytes,
            "application/json",
            "RETAINED_EVIDENCE",
        ),
        (
            "settlement_mapping",
            bundles["settlement"].mapping_bytes,
            "application/json",
            "RETAINED_EVIDENCE",
        ),
    )
    anchors = [
        artifact(text(ids.get(key), key), content, media_type, role)
        for key, content, media_type, role in values
    ]
    for bundle in bundles.values():
        for identifier, content in bundle.sources.items():
            anchors.extend(
                source_anchors(
                    bundle.prefix + identifier,
                    content,
                    bundle.media_types[identifier],
                )
            )
    history.append_anchors(
        anchors=tuple(anchors),
        transaction_time=text(program.get("transaction_time"), "transaction time"),
        actor_id=text(program.get("actor_id"), "actor ID"),
    )


def operation_data(item: KnowledgeOperation) -> dict[str, object]:
    return {
        "depends_on": list(item.depends_on),
        "operation_id": item.operation_id,
        "operation_type": item.operation_type,
        "ordinal": item.ordinal,
        "properties": plain(item.properties),
        "record_id": item.record_id,
        "record_type": item.record_type,
        **(
            {"source_id": item.source_id, "target_id": item.target_id}
            if item.operation_type == "CREATE_RELATION"
            else {}
        ),
        **(
            {"supersedes_record_id": item.supersedes_record_id}
            if item.supersedes_record_id is not None
            else {}
        ),
    }


def receipt_bytes(
    stage: Stage,
    change: KnowledgeChangeSet,
    check: SourceMappingCheck,
    provenance: tuple[Mapping[str, object], ...],
) -> bytes:
    claim = {
        "change_set_id": change.change_set_id,
        "change_set_identity": change.identity,
        "mapping_artifact_id": stage.mapping_id,
        "mapping_identity": stage.mapping_identity,
        "selected_records": plain(provenance),
    }
    return canonical(
        {
            **claim,
            "check_contract_id": check.identifier,
            "check_contract_identity": check.identity,
            "grammar": RECEIPT_GRAMMAR,
            "outcome": "SATISFIED",
            "verification_identity": digest(canonical(claim)),
        }
    )


def assert_change(stage: Stage, change: KnowledgeChangeSet) -> None:
    if (
        change.change_set_id != stage.change_set_id
        or plain(change.data["operations"])
        != [operation_data(item) for item in stage.operations]
        or tuple(identifier for identifier, _ in change.sources) != stage.sources
        or tuple(identifier for identifier, _ in change.evidence) != stage.evidence
        or change.supersedes != stage.supersedes
        or change.valid_time != stage.valid_time
    ):
        raise refuse(
            ShowcaseRefusalReason.SOURCE_MAPPING_FAILED,
            "change differs from source mapping",
        )


def _admit_stage(prepared: PreparedShowcase, stage: Stage) -> KnowledgeHistoryReplay:
    try:
        provenance = verify_stage(stage)
        change = prepared.history.compose_change_set(
            change_set_id=stage.change_set_id,
            source_record_ids=stage.sources,
            evidence_record_ids=stage.evidence,
            operations=stage.operations,
            valid_time=stage.valid_time,
            supersedes=stage.supersedes,
        )
        assert_change(stage, change)
        receipt = receipt_bytes(stage, change, prepared.check, provenance)
        receipt_identity = digest(receipt)
        anchor = artifact(
            receipt_identity, receipt, "application/json", "RETAINED_EVIDENCE"
        )
        before = prepared.history.replay()
        preview = execute_event(
            before.partial_contract, before.machine_state, anchor.machine_event
        )
        if preview.receipt.outcome != "APPLIED":
            raise refuse(
                ShowcaseRefusalReason.ADMISSION_FAILED, "receipt anchor refused"
            )
        declaration = stage.declaration
        events = (
            event(
                "CHANGE_PROPOSED",
                {
                    "expected_machine_state_identity": preview.state.identity,
                    "knowledge_change_set_identity": change.identity,
                    "policy_id": prepared.policy.identifier,
                    "policy_identity": prepared.policy.identity,
                    "proposal_id": declaration["proposal_id"],
                },
            ),
            event(
                "CHECK_RECORDED",
                {
                    "check_contract_id": prepared.check.identifier,
                    "check_contract_identity": prepared.check.identity,
                    "outcome": "SATISFIED",
                    "policy_identity": prepared.policy.identity,
                    "proposal_id": declaration["proposal_id"],
                    "receipt_id": declaration["receipt_id"],
                    "receipt_identity": receipt_identity,
                },
            ),
            event(
                "VERDICT_RECORDED",
                {
                    "decision_id": declaration["decision_id"],
                    "proposal_id": declaration["proposal_id"],
                },
            ),
        )
        return prepared.history.admit_with_anchors(
            anchors=(anchor,),
            change_set=change,
            machine_events=events,
            transaction_time=declaration["transaction_time"],
            actor_id=text(prepared.program.get("actor_id"), "actor ID"),
        )
    except ShowcaseRefusal:
        raise
    except KnowledgeChangeRefusal as error:
        raise refuse(
            ShowcaseRefusalReason.ADMISSION_FAILED, f"stage refused atomically: {error}"
        ) from error


def _prepare_showcase(
    output: Path,
    *,
    program_path: Path = PROGRAM,
    correction_fixture: Path | None = None,
    correction_mapping: Path | None = None,
    policy_path: Path | None = None,
    check_contract: Path | None = None,
    settlement_fixture: Path | None = None,
    settlement_mapping: Path | None = None,
) -> PreparedShowcase:
    output = Path(output)
    if output.is_symlink() or (output / "history.jsonl").is_symlink():
        raise refuse(
            ShowcaseRefusalReason.MALFORMED_CONFIGURATION, "output path is a symlink"
        )
    program_bytes = read(Path(program_path), "run program")
    program = validate_program(program_bytes)
    inputs = obj(program.get("inputs"), "inputs")
    ids = obj(program.get("artifact_ids"), "artifact IDs")
    baseline_config = obj(inputs.get("baseline"), "baseline")
    baseline_path, baseline_mapping = pinned(
        {
            "path": baseline_config["mapping_path"],
            "sha256": baseline_config["mapping_sha256"],
        },
        "RET-010 mapping",
    )
    try:
        vertical = load_ret010_vertical(
            fixture_root=ROOT
            / relative(baseline_config.get("fixture_root"), "baseline root"),
            mapping_path=baseline_path,
        )
    except Ret010Refusal as error:
        raise refuse(ShowcaseRefusalReason.SOURCE_MISMATCH, str(error)) from error
    baseline = Bundle(
        "baseline",
        text(baseline_config.get("source_prefix"), "baseline prefix"),
        text(ids.get("baseline_mapping"), "baseline mapping ID"),
        baseline_mapping,
        vertical.mapping.data,
        MappingProxyType(dict(vertical.inputs.source_bytes)),
        manifest_media_types(dict(vertical.inputs.source_bytes)),
    )
    correction_config = obj(inputs.get("correction"), "correction")
    _, correction_bytes = pinned(
        {
            "path": correction_config["mapping_path"],
            "sha256": correction_config["mapping_sha256"],
        },
        "correction mapping",
        Path(correction_mapping) if correction_mapping else None,
    )
    correction = fixture_bundle(
        Path(correction_fixture)
        if correction_fixture
        else ROOT / relative(correction_config.get("fixture_root"), "correction root"),
        "correction",
        text(correction_config.get("source_prefix"), "correction prefix"),
        text(ids.get("correction_mapping"), "correction mapping ID"),
        correction_bytes,
    )
    settlement_config = obj(inputs.get("settlement"), "settlement")
    _, settlement_bytes = pinned(
        {
            "path": settlement_config["mapping_path"],
            "sha256": settlement_config["mapping_sha256"],
        },
        "settlement mapping",
        Path(settlement_mapping) if settlement_mapping else None,
    )
    settlement = fixture_bundle(
        Path(settlement_fixture)
        if settlement_fixture
        else ROOT / relative(settlement_config.get("fixture_root"), "settlement root"),
        "settlement",
        text(settlement_config.get("source_prefix"), "settlement prefix"),
        text(ids.get("settlement_mapping"), "settlement mapping ID"),
        settlement_bytes,
    )
    bundles = {"baseline": baseline, "correction": correction, "settlement": settlement}
    _, machine_bytes = pinned(obj(inputs.get("machine"), "machine"), "machine")
    _, policy_bytes = pinned(
        obj(inputs.get("policy"), "policy"),
        "policy",
        Path(policy_path) if policy_path else None,
    )
    _, check_bytes = pinned(
        obj(inputs.get("check_contract"), "check"),
        "check",
        Path(check_contract) if check_contract else None,
    )
    entrypoint_id = text(ids.get("entrypoint"), "entrypoint ID")
    check = validate_check(
        check_bytes,
        entrypoint_id=entrypoint_id,
        entrypoint_identity=digest(read(Path(__file__), "entrypoint")),
    )
    policy = PolicyProgram.from_bytes(policy_bytes)
    if policy.required_checks != ((check.identifier, check.identity),):
        raise refuse(
            ShowcaseRefusalReason.IDENTITY_MISMATCH, "policy does not pin check"
        )
    compilation = compile_contract(settlement.mapping, bundles)
    machine = ProtocolMachineProgram.from_bytes(machine_bytes)
    contract = compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=compose_normative_profile(
            protocol_machine_program=machine,
            policy_programs={text(program.get("policy_ref"), "policy ref"): policy},
            capability_refs=(),
        ),
    )
    if program["history_binding"] != {
        "identity": vertical.history_binding.identity,
        "source": "RET010_MAPPING",
    }:
        raise refuse(
            ShowcaseRefusalReason.IDENTITY_MISMATCH, "history binding source differs"
        )
    stages = mapped_stages(program, bundles)
    output.mkdir(parents=True, exist_ok=True)
    history = KnowledgeChangeHistory(
        output / "history.jsonl",
        partial_contract=contract,
        contract_view=compilation.view,
        binding=vertical.history_binding,
    )
    bootstrap(
        history,
        program_bytes,
        program,
        compilation,
        contract,
        vertical.history_binding,
        machine_bytes,
        policy_bytes,
        check_bytes,
        bundles,
    )
    return PreparedShowcase(history, program, policy, check, stages)


def retained_context(
    replay: KnowledgeHistoryReplay,
) -> tuple[Mapping[str, object], SourceMappingCheck, tuple[Stage, ...]]:
    retained = {item.record_id: item for item in replay.retained_inputs}
    programs = []
    for item in retained.values():
        if item.role == "RETAINED_EVIDENCE":
            try:
                programs.append(validate_program(item.content))
            except ShowcaseRefusal:
                pass
    if len(programs) != 1:
        raise refuse(
            ShowcaseRefusalReason.INCOMPATIBLE_HISTORY, "history lacks one run program"
        )
    program = programs[0]
    ids = obj(program.get("artifact_ids"), "artifact IDs")
    bundles = {
        "baseline": retained_bundle(replay, program, "baseline", "baseline_mapping"),
        "correction": retained_bundle(
            replay, program, "correction", "correction_mapping"
        ),
        "settlement": retained_bundle(
            replay, program, "settlement", "settlement_mapping"
        ),
    }
    try:
        check_bytes = retained[text(ids.get("check_contract"), "check ID")].content
        entrypoint = retained[text(ids.get("entrypoint"), "entrypoint ID")]
    except KeyError as error:
        raise refuse(
            ShowcaseRefusalReason.INCOMPATIBLE_HISTORY,
            "history lacks check or entrypoint",
        ) from error
    check = validate_check(
        check_bytes,
        entrypoint_id=entrypoint.record_id,
        entrypoint_identity=entrypoint.identity,
    )
    return program, check, mapped_stages(program, bundles)


def verify_source_mapping_receipts(
    replay: KnowledgeHistoryReplay,
) -> tuple[VerifiedSourceMappingReceipt, ...]:
    """Recompute all five receipts from exact ledger-retained bytes."""
    _, check, stages = retained_context(replay)
    if tuple(change.change_set_id for change in replay.change_sets) != tuple(
        stage.change_set_id for stage in stages
    ):
        raise refuse(
            ShowcaseRefusalReason.INCOMPATIBLE_HISTORY, "accepted change order differs"
        )
    retained = {item.record_id: item for item in replay.retained_inputs}
    checks = {
        record.fields["proposal_id"]: record
        for record in replay.machine_state.records
        if record.record_type == "CheckRecord"
    }
    verified = []
    for stage, change in zip(stages, replay.change_sets, strict=True):
        provenance = verify_stage(stage)
        assert_change(stage, change)
        expected = receipt_bytes(stage, change, check, provenance)
        identity = digest(expected)
        receipt = retained.get(identity)
        check_record = checks.get(stage.declaration["proposal_id"])
        if (
            receipt is None
            or receipt.content != expected
            or check_record is None
            or check_record.fields["receipt_identity"] != identity
        ):
            raise refuse(
                ShowcaseRefusalReason.INCOMPATIBLE_HISTORY,
                f"receipt does not recompute: {stage.change_set_id}",
            )
        verified.append(VerifiedSourceMappingReceipt(stage.change_set_id, identity))
    return tuple(verified)


def write_outputs(output: Path, replay: KnowledgeHistoryReplay) -> ShowcaseRun:
    graph_bytes = canonical(replay.graph.snapshot())
    receipt_bytes = replay.receipt.canonical_bytes
    (output / "graph.json").write_bytes(graph_bytes)
    (output / "receipt.json").write_bytes(receipt_bytes)
    return ShowcaseRun(replay, graph_bytes, receipt_bytes)


def run_showcase(
    output: Path,
    *,
    program_path: Path = PROGRAM,
    correction_fixture: Path | None = None,
    correction_mapping: Path | None = None,
    policy_path: Path | None = None,
    check_contract: Path | None = None,
    settlement_fixture: Path | None = None,
    settlement_mapping: Path | None = None,
) -> ShowcaseRun:
    """Build once, then reopen using the retained ledger alone."""
    output = Path(output)
    history_path = output / "history.jsonl"
    if history_path.exists():
        replay = KnowledgeChangeHistory.reopen(history_path).replay()
        verify_source_mapping_receipts(replay)
        return write_outputs(output, replay)
    prepared = _prepare_showcase(
        output,
        program_path=program_path,
        correction_fixture=correction_fixture,
        correction_mapping=correction_mapping,
        policy_path=policy_path,
        check_contract=check_contract,
        settlement_fixture=settlement_fixture,
        settlement_mapping=settlement_mapping,
    )
    replay = prepared.history.replay()
    for stage in prepared.stages:
        replay = _admit_stage(prepared, stage)
    verify_source_mapping_receipts(replay)
    return write_outputs(output, replay)


def main(argv: tuple[str, ...] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        result = run_showcase(args.output)
    except ShowcaseRefusal as error:
        parser.error(str(error))
    sys.stdout.buffer.write(result.receipt_bytes + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
