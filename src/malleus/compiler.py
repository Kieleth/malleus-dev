"""Public compiler-to-ledger-to-knowledge-graph facade.

The convenience compiler accepts exact, caller-supplied LinkML source bytes.
Protocol programs, policies, population plans, and history bindings remain data.
This module only exposes and connects the existing deterministic executors.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path
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
    OBJECT_EVENT_PROFILE,
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
_RESOLVER_PROFILE = "malleus.linkml/private-v1"
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


def _profile_resource(name: str) -> tuple[bytes, dict[str, object]]:
    try:
        value = json.loads(files("malleus").joinpath("profiles", name).read_bytes())
    except (OSError, TypeError, UnicodeError, ValueError) as error:
        raise RuntimeError(f"installed Malleus profile is invalid: {name}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"installed Malleus profile is not an object: {name}")
    return _canonical(value), value


@dataclass(frozen=True, slots=True)
class StructuralHistoryBundle:
    """Core's exact mechanical-admission artifacts.

    This bundle admits structural changes. It does not establish source truth,
    domain adequacy, or epistemic correctness. Projects may instead compose
    their own identified machine, policy, binding, and check executor.
    """

    canonical_bytes: bytes
    identity: str
    protocol_machine_program: ProtocolMachineProgram
    policy_program: PolicyProgram
    normative_profile: NormativeAdmissionProfile
    history_binding: KnowledgeChangeHistoryBinding
    check_contract_id: str
    check_contract_identity: str
    check_contract_bytes: bytes
    success_outcome: str


def _load_structural_history_bundle() -> StructuralHistoryBundle:
    machine_source, _ = _profile_resource("structural-history-machine.json")
    policy_source, _ = _profile_resource("structural-admission-policy.json")
    binding_source, _ = _profile_resource("structural-history-binding.json")
    check_source, check = _profile_resource("structural-admission-check.json")
    expected_check_fields = {
        "check_contract_id",
        "checks",
        "executor",
        "grammar",
        "non_claims",
        "success_outcome",
    }
    if set(check) != expected_check_fields:
        raise RuntimeError("installed structural-admission check fields are not closed")
    check_id = check["check_contract_id"]
    success_outcome = check["success_outcome"]
    if (
        check["grammar"] != "malleus.admission-check/private-v0"
        or not isinstance(check_id, str)
        or not check_id
        or not isinstance(success_outcome, str)
        or not success_outcome
    ):
        raise RuntimeError("installed structural-admission check is malformed")
    machine = ProtocolMachineProgram.from_bytes(machine_source)
    policy = PolicyProgram.from_bytes(policy_source)
    binding = KnowledgeChangeHistoryBinding.from_bytes(binding_source)
    check_identity = _digest(check_source)
    if policy.required_checks != ((check_id, check_identity),):
        raise RuntimeError("structural admission policy does not bind its exact check")
    if success_outcome not in policy.outcome_verdicts:
        raise RuntimeError("structural admission success outcome is not in policy")
    normative = compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={"required-check-verdict": policy},
        capability_refs=(),
    )
    source = _canonical(
        {
            "check_contract": check,
            "check_contract_identity": check_identity,
            "grammar": "malleus.structural-history-bundle/private-v0",
            "history_binding": json.loads(binding.canonical_bytes),
            "history_binding_identity": binding.identity,
            "normative_profile": json.loads(normative.canonical_bytes),
            "normative_profile_identity": normative.identity,
        }
    )
    return StructuralHistoryBundle(
        canonical_bytes=source,
        identity=_digest(source),
        protocol_machine_program=machine,
        policy_program=policy,
        normative_profile=normative,
        history_binding=binding,
        check_contract_id=check_id,
        check_contract_identity=check_identity,
        check_contract_bytes=check_source,
        success_outcome=success_outcome,
    )


STRUCTURAL_HISTORY_BUNDLE = _load_structural_history_bundle()


def _machine_event(event_type: str, **payload: object) -> bytes:
    return _canonical({"event_type": event_type, "payload": payload})


def create_structural_history(
    path: str | Path,
    *,
    compilation: ValidatedContractCompilation,
    transaction_time: str,
    actor_id: str,
) -> KnowledgeChangeHistory:
    """Create and bootstrap a history under Core's structural policy."""

    if not isinstance(compilation, ValidatedContractCompilation):
        raise TypeError("compilation must be a ValidatedContractCompilation")
    ledger_path = Path(path)
    if ledger_path.exists() and ledger_path.stat().st_size:
        raise KnowledgeChangeRefusal(
            KnowledgeChangeRefusalReason.MALFORMED_HISTORY,
            "structural history path already contains ledger bytes",
        )
    partial = compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    )
    history = KnowledgeChangeHistory(
        ledger_path,
        partial_contract=partial,
        contract_view=compilation.view,
        binding=STRUCTURAL_HISTORY_BUNDLE.history_binding,
    )
    artifacts = (
        (
            "malleus:bootstrap:validated-contract",
            compilation.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        (
            "malleus:bootstrap:partial-effective-contract",
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            "malleus:bootstrap:knowledge-history-binding",
            STRUCTURAL_HISTORY_BUNDLE.history_binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        (
            "malleus:structural-admission-check/v1",
            STRUCTURAL_HISTORY_BUNDLE.check_contract_bytes,
            "RETAINED_EVIDENCE",
        ),
    )
    history.append_anchors(
        anchors=tuple(
            KnowledgeAnchorInput(
                machine_event=_machine_event(
                    "ARTIFACT_REGISTERED",
                    artifact_id=record_id,
                    artifact_identity=_digest(content),
                ),
                retained_bytes=content,
                media_type="application/json",
                role=role,
            )
            for record_id, content, role in artifacts
        ),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    return history


def population_retention_events(
    *,
    history: KnowledgeChangeHistory,
    compilation: PopulationPlanCompilation,
    profile: DomainHistoryProfile,
) -> Mapping[str, bytes]:
    """Name the exact retention events one compiled plan still needs.

    ``prepare_population_change`` retains the bound profile artifact when the
    history does not hold it yet, the canonical plan bytes, and the generated
    gaps artifact when the plan carries gaps. It refuses any event set that is
    not exactly those records, and the gaps artifact bytes are not otherwise
    reachable, so a caller cannot name them without restating this. The helper
    decides nothing: a change to what the governed path retains refuses here
    with ``MALFORMED_RETENTION_EVENT`` instead of retaining the wrong bytes.
    """

    if not isinstance(history, KnowledgeChangeHistory):
        raise TypeError("history must be a KnowledgeChangeHistory")
    if not isinstance(compilation, PopulationPlanCompilation):
        raise TypeError("compilation must be a PopulationPlanCompilation")
    if not isinstance(profile, DomainHistoryProfile):
        raise TypeError("profile must be a DomainHistoryProfile")
    plan = json.loads(compilation.canonical_plan_bytes)
    retained = {member.record_id for member in history.replay().retained_inputs}
    artifacts: list[tuple[str, bytes]] = []
    profile_record_id = f"profile:{profile.profile_id}"
    if profile_record_id not in retained:
        artifacts.append((profile_record_id, profile.canonical_bytes))
    artifacts.append((compilation.plan_id, compilation.canonical_plan_bytes))
    if plan["gaps"]:
        artifacts.append(
            (
                f"{compilation.plan_id}:gaps",
                _canonical({"gaps": plan["gaps"], "plan_id": compilation.plan_id}),
            )
        )
    return MappingProxyType(
        {
            record_id: _machine_event(
                "ARTIFACT_REGISTERED",
                artifact_id=record_id,
                artifact_identity=_digest(content),
            )
            for record_id, content in artifacts
        }
    )


def admit_structural_change(
    *,
    history: KnowledgeChangeHistory,
    preparation: PopulationPreparation,
    transaction_time: str,
    actor_id: str,
) -> KnowledgeHistoryReplay:
    """Atomically validate and admit one prepared structural change.

    The successful check event is generated here and is persisted only if the
    same candidate batch passes base, retained-closure, and graph application
    validation. The caller cannot supply a check outcome.
    """

    if not isinstance(history, KnowledgeChangeHistory):
        raise TypeError("history must be a KnowledgeChangeHistory")
    if not isinstance(preparation, PopulationPreparation):
        raise TypeError("preparation must be a PopulationPreparation")
    change = preparation.change_set
    if change is None:
        raise PopulationPlanRefusal(
            PopulationPlanRefusalReason.MALFORMED_PLAN,
            "NO_DOMAIN_CHANGE has no change set to admit",
        )
    if (
        history.partial_contract.normative_profile.identity
        != STRUCTURAL_HISTORY_BUNDLE.normative_profile.identity
        or history.binding.identity
        != STRUCTURAL_HISTORY_BUNDLE.history_binding.identity
    ):
        raise KnowledgeChangeRefusal(
            KnowledgeChangeRefusalReason.IDENTITY_MISMATCH,
            "history does not use the shipped structural admission bundle",
        )
    current = history.replay()
    if current.receipt.identity != preparation.retention_replay.receipt.identity:
        raise KnowledgeChangeRefusal(
            KnowledgeChangeRefusalReason.STALE_BASE,
            "population preparation is stale against the current history",
        )
    policy = STRUCTURAL_HISTORY_BUNDLE.policy_program
    proposal_id = f"proposal:{change.change_set_id}:structural-admission"
    events = (
        _machine_event(
            "CHANGE_PROPOSED",
            expected_machine_state_identity=current.machine_state.identity,
            knowledge_change_set_identity=change.identity,
            policy_id=policy.identifier,
            policy_identity=policy.identity,
            proposal_id=proposal_id,
        ),
        _machine_event(
            "CHECK_RECORDED",
            check_contract_id=STRUCTURAL_HISTORY_BUNDLE.check_contract_id,
            check_contract_identity=STRUCTURAL_HISTORY_BUNDLE.check_contract_identity,
            outcome=STRUCTURAL_HISTORY_BUNDLE.success_outcome,
            policy_identity=policy.identity,
            proposal_id=proposal_id,
            receipt_id=f"receipt:{change.change_set_id}:structural-admission",
        ),
        _machine_event(
            "VERDICT_RECORDED",
            decision_id=f"decision:{change.change_set_id}:structural-admission",
            proposal_id=proposal_id,
        ),
    )
    return history.admit(
        change_set=change,
        machine_events=events,
        transaction_time=transaction_time,
        actor_id=actor_id,
    )


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
    "OBJECT_EVENT_PROFILE",
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
    "STRUCTURAL_HISTORY_BUNDLE",
    "StructuralHistoryBundle",
    "SourceBoundaryRefusal",
    "SourceRefusalReason",
    "ValidatedContractArtifact",
    "ValidatedContractCompilation",
    "adapt_document_assertions",
    "admit_structural_change",
    "compile_linkml_contract",
    "compile_contract_revision",
    "compile_population_plan",
    "compose_normative_profile",
    "compose_partial_effective_contract",
    "create_structural_history",
    "execute_event",
    "load_validated_contract_artifact",
    "population_retention_events",
    "prepare_population_change",
    "replay_events",
    "trace_population_record",
)
