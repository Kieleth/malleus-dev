"""Public compiler-to-ledger-to-knowledge-graph facade.

The convenience compiler accepts exact, caller-supplied LinkML source bytes.
Protocol programs, policies, population plans, and history bindings remain data.
This module only exposes and connects the existing deterministic executors.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
import json
from types import MappingProxyType

from malleus._contract_binder import (
    BindingRefusal,
    BindingRefusalReason,
    bind_contract,
)
from malleus._contract_linkml_adapter import (
    LinkMLAdapterRefusal,
    LinkMLImportReader,
    LinkMLRefusalReason,
    adapt_linkml_closure,
)
from malleus._contract_pipeline import (
    ArtifactRefusal,
    ArtifactRefusalReason,
    ContractView,
    ElaborationRefusal,
    ElaborationRefusalReason,
    ValidatedContractArtifact,
    ValidatedContractCompilation,
    compile_binding,
    load_validated_contract_artifact,
)
from malleus._contract_pipeline.document import (
    DOCUMENT_ASSERTION_ADAPTER,
    DOCUMENT_CAPTURE_GRAMMAR,
    DocumentAssertionCompilation,
    DocumentAssertionRefusal,
    DocumentAssertionRefusalReason,
    adapt_document_assertions,
)
from malleus._contract_pipeline.knowledge import (
    KnowledgeAnchorInput,
    KnowledgeAnchorResult,
    KnowledgeChangeHistory,
    KnowledgeChangeHistoryBinding,
    KnowledgeChangeRefusal,
    KnowledgeChangeRefusalReason,
    KnowledgeChangeSet,
    KnowledgeHistoryReceipt,
    KnowledgeHistoryReplay,
    KnowledgeOperation,
    KnowledgeRecordHistory,
    KnowledgeRetainedInput,
    KnowledgeValidTime,
)
from malleus._contract_pipeline.machine import (
    MachineArtifactRefusal,
    MachineArtifactRefusalReason,
    MachineExecutionResult,
    MachineReceipt,
    MachineReplayResult,
    MachineState,
    NormativeAdmissionProfile,
    PartialEffectiveContract,
    PolicyProgram,
    ProtocolMachineProgram,
    ProtocolMachineProgramRefusal,
    ProtocolMachineProgramRefusalReason,
    compose_normative_profile,
    compose_partial_effective_contract,
    execute_event,
    replay_events,
)
from malleus._contract_pipeline.population import (
    DomainHistoryProfile,
    PopulationBaseState,
    PopulationPlanCompilation,
    PopulationPlanRefusal,
    PopulationPlanRefusalReason,
    PopulationPlanStatus,
    PopulationPreparation,
    PopulationRecordTrace,
    PopulationTraceRefusal,
    PopulationTraceRefusalReason,
    SOURCE_ASSERTION_PROFILE,
    STATE_VERSION_PROFILE,
    compile_population_plan,
    prepare_population_change,
    trace_population_record,
)
from malleus._contract_pipeline.revision import (
    CONTRACT_REVISION_POLICY,
    ContractRevision,
    ContractRevisionChange,
    ContractRevisionPolicy,
    ContractRevisionRefusal,
    ContractRevisionRefusalReason,
    compile_contract_revision,
)
from malleus._contract_source import (
    CollaboratorRefusal,
    ImportRequest,
    RefusalReason as SourceRefusalReason,
    ResolvedSource,
    ResolverSelection,
    RootRequest,
    SourceBoundaryRefusal,
    build_source_closure,
)


_RESOLVER_ID = "malleus.compiler.exact-linkml-source-set/v1"
_RESOLVER_PROFILE = "malleus.linkml/private-v0"
_MEDIA_TYPE = "application/yaml"


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


@dataclass(frozen=True, slots=True)
class _ExactSourceResolver:
    sources: Mapping[str, bytes]

    def resolve(self, request: RootRequest | ImportRequest) -> ResolvedSource:
        if isinstance(request, RootRequest):
            locator = request.requested_locator
        elif isinstance(request, ImportRequest):
            locator = request.literal_import
        else:
            raise CollaboratorRefusal("unsupported source request")
        try:
            source = self.sources[locator]
        except KeyError as error:
            raise CollaboratorRefusal(f"source was not supplied: {locator}") from error
        return ResolvedSource(locator, source, _MEDIA_TYPE)


def _source_snapshot(sources: Mapping[str, bytes]) -> Mapping[str, bytes]:
    if not isinstance(sources, Mapping):
        raise TypeError("sources must be a mapping of locator to exact bytes")
    try:
        items = tuple(sources.items())
    except (KeyError, RuntimeError, TypeError, ValueError) as error:
        raise TypeError("sources must provide one stable mapping snapshot") from error
    if not items:
        raise ValueError("at least one LinkML source is required")
    snapshot: dict[str, bytes] = {}
    for locator, source in items:
        if not isinstance(locator, str) or not locator:
            raise TypeError("each source locator must be a nonempty string")
        if type(source) is not bytes:
            raise TypeError(f"source must be exact bytes: {locator}")
        if locator in snapshot:
            raise ValueError(f"source locator is repeated: {locator}")
        snapshot[locator] = source
    return MappingProxyType(snapshot)


def compile_linkml_contract(
    *,
    root_locator: str,
    sources: Mapping[str, bytes],
) -> ValidatedContractCompilation:
    """Compile one LinkML root and its exact named import sources.

    Import literals are looked up directly in ``sources``. The strict packaged
    Malleus LinkML adapter and contract profiles define the accepted subset.
    Source bytes and their deterministic resolver configuration are retained in
    the compilation evidence. No filesystem, network, or LLM access occurs.
    """

    if not isinstance(root_locator, str) or not root_locator:
        raise TypeError("root_locator must be a nonempty string")
    snapshot = _source_snapshot(sources)
    configuration = _digest(
        _canonical(
            [
                {
                    "locator": locator,
                    "media_type": _MEDIA_TYPE,
                    "sha256": _digest(source),
                }
                for locator, source in sorted(snapshot.items())
            ]
        )
    )
    closure = build_source_closure(
        requested_locator=root_locator,
        selection=ResolverSelection(
            resolver_id=_RESOLVER_ID,
            profile_version=_RESOLVER_PROFILE,
            configuration_id=configuration,
        ),
        resolver=_ExactSourceResolver(snapshot),
        import_reader=LinkMLImportReader(),
    )
    return compile_binding(bind_contract(adapt_linkml_closure(closure)))


__all__ = (
    "ArtifactRefusal",
    "ArtifactRefusalReason",
    "BindingRefusal",
    "BindingRefusalReason",
    "CONTRACT_REVISION_POLICY",
    "ContractView",
    "ContractRevision",
    "ContractRevisionChange",
    "ContractRevisionPolicy",
    "ContractRevisionRefusal",
    "ContractRevisionRefusalReason",
    "DomainHistoryProfile",
    "DOCUMENT_ASSERTION_ADAPTER",
    "DOCUMENT_CAPTURE_GRAMMAR",
    "DocumentAssertionCompilation",
    "DocumentAssertionRefusal",
    "DocumentAssertionRefusalReason",
    "ElaborationRefusal",
    "ElaborationRefusalReason",
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
    "LinkMLAdapterRefusal",
    "LinkMLRefusalReason",
    "MachineArtifactRefusal",
    "MachineArtifactRefusalReason",
    "MachineExecutionResult",
    "MachineReceipt",
    "MachineReplayResult",
    "MachineState",
    "NormativeAdmissionProfile",
    "PartialEffectiveContract",
    "PolicyProgram",
    "PopulationBaseState",
    "PopulationPlanCompilation",
    "PopulationPlanRefusal",
    "PopulationPlanRefusalReason",
    "PopulationPlanStatus",
    "PopulationPreparation",
    "PopulationRecordTrace",
    "PopulationTraceRefusal",
    "PopulationTraceRefusalReason",
    "ProtocolMachineProgram",
    "ProtocolMachineProgramRefusal",
    "ProtocolMachineProgramRefusalReason",
    "SOURCE_ASSERTION_PROFILE",
    "STATE_VERSION_PROFILE",
    "SourceBoundaryRefusal",
    "SourceRefusalReason",
    "ValidatedContractArtifact",
    "ValidatedContractCompilation",
    "adapt_document_assertions",
    "compile_linkml_contract",
    "compile_contract_revision",
    "compile_population_plan",
    "compose_normative_profile",
    "compose_partial_effective_contract",
    "execute_event",
    "load_validated_contract_artifact",
    "prepare_population_change",
    "replay_events",
    "trace_population_record",
)
