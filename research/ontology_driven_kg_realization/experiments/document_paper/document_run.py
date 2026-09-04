"""Private paper-local path from one GraphRecipe plan to replayed history."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Callable

from malleus._contract_pipeline.knowledge import (
    KnowledgeAnchorInput,
    KnowledgeChangeHistory,
    KnowledgeChangeHistoryBinding,
    KnowledgeChangeSet,
    KnowledgeHistoryReplay,
    KnowledgeValidTime,
)
from malleus._contract_pipeline.machine import PartialEffectiveContract
from malleus._contract_pipeline.view import ContractView
from malleus.ledger import LedgerError, canonical_json

from ..graph_recipe.assembly import AssemblyPlan
from .graph_recipe_change_set import (
    assembly_plan_to_operations,
    canonical_assembly_plan_bytes,
)


_VALIDATED_CONTRACT_ID = "artifact:paper-v4:validated-contract"
_PARTIAL_CONTRACT_ID = "artifact:paper-v4:partial-contract"
_HISTORY_BINDING_ID = "artifact:paper-v4:history-binding"
_CHECK_EVENT = "CHECK_RECORDED"


class DocumentRunError(ValueError):
    """The closed paper-local history run is malformed."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DocumentRunError(f"{label} must be nonblank text")
    return value


def _require_bytes(value: object, label: str) -> bytes:
    if type(value) is not bytes:
        raise DocumentRunError(f"{label} must be exact bytes")
    return value


@dataclass(frozen=True, slots=True)
class RetainedDocumentSource:
    """One source retained as an artifact and as a registered source."""

    artifact_id: str
    source_id: str
    content: bytes
    media_type: str

    def __post_init__(self) -> None:
        _require_text(self.artifact_id, "source artifact_id")
        _require_text(self.source_id, "source source_id")
        _require_bytes(self.content, "source content")
        _require_text(self.media_type, "source media_type")


@dataclass(frozen=True, slots=True)
class RetainedDocumentEvidence:
    """One exact evidence artifact retained before change composition."""

    record_id: str
    content: bytes
    media_type: str

    def __post_init__(self) -> None:
        _require_text(self.record_id, "evidence record_id")
        _require_bytes(self.content, "evidence content")
        _require_text(self.media_type, "evidence media_type")


ProtocolEventFactory = Callable[[KnowledgeChangeSet, str], tuple[bytes, ...]]


@dataclass(frozen=True, slots=True)
class DocumentRun:
    """Exact persisted bytes and the graph reconstructed from those bytes."""

    ledger_bytes: bytes
    replay: KnowledgeHistoryReplay


def _event(event_type: str, **payload: object) -> bytes:
    try:
        return canonical_json({"event_type": event_type, "payload": payload}).encode(
            "utf-8"
        )
    except LedgerError as error:
        raise DocumentRunError("machine event is not canonical JSON") from error


def _artifact_anchor(
    record_id: str,
    content: bytes,
    media_type: str,
    role: str,
) -> KnowledgeAnchorInput:
    from hashlib import sha256

    identity = "sha256:" + sha256(content).hexdigest()
    return KnowledgeAnchorInput(
        machine_event=_event(
            "ARTIFACT_REGISTERED",
            artifact_id=record_id,
            artifact_identity=identity,
        ),
        retained_bytes=content,
        media_type=media_type,
        role=role,
    )


def _source_anchor(source: RetainedDocumentSource) -> KnowledgeAnchorInput:
    from hashlib import sha256

    identity = "sha256:" + sha256(source.content).hexdigest()
    return KnowledgeAnchorInput(
        machine_event=_event(
            "SOURCE_REGISTERED",
            artifact_id=source.artifact_id,
            source_id=source.source_id,
            source_identity=identity,
        ),
        retained_bytes=source.content,
        media_type=source.media_type,
        role="RETAINED_SOURCE",
    )


def _event_type(source: bytes) -> str:
    _require_bytes(source, "protocol event")
    try:
        value = json.loads(source.decode("utf-8"))
        if (
            not isinstance(value, dict)
            or set(value) != {"event_type", "payload"}
            or canonical_json(value).encode("utf-8") != source
        ):
            raise ValueError("event is not closed canonical JSON")
        return _require_text(value["event_type"], "protocol event_type")
    except (KeyError, LedgerError, UnicodeError, ValueError) as error:
        raise DocumentRunError("protocol event is not closed canonical JSON") from error


def _require_lifecycle(
    events: tuple[bytes, ...],
    binding: KnowledgeChangeHistoryBinding,
) -> None:
    if not isinstance(events, tuple):
        raise DocumentRunError("protocol events must be an ordered tuple")
    event_types = tuple(_event_type(event) for event in events)
    proposal = binding.data["proposal"]["event_type"]
    decision = binding.data["decision"]["event_type"]
    if event_types != (proposal, _CHECK_EVENT, _CHECK_EVENT, decision):
        raise DocumentRunError(
            "protocol lifecycle must be one proposal, two checks, and one verdict"
        )


def run_document_history(
    ledger_path: str | Path,
    *,
    plan: AssemblyPlan,
    partial_contract: PartialEffectiveContract,
    contract_view: ContractView,
    binding: KnowledgeChangeHistoryBinding,
    source: RetainedDocumentSource,
    evidence: tuple[RetainedDocumentEvidence, ...],
    plan_evidence_id: str,
    change_set_id: str,
    valid_time: KnowledgeValidTime,
    transaction_time: str,
    actor_id: str,
    protocol_events: ProtocolEventFactory,
) -> DocumentRun:
    """Admit one genesis plan and return only its ledger-rebuilt projection."""

    path = Path(ledger_path)
    if path.exists():
        raise DocumentRunError("genesis ledger path already exists")
    if not isinstance(source, RetainedDocumentSource):
        raise DocumentRunError("source must be a RetainedDocumentSource")
    if not isinstance(evidence, tuple) or not evidence:
        raise DocumentRunError("evidence must be a nonempty ordered tuple")
    if not all(isinstance(item, RetainedDocumentEvidence) for item in evidence):
        raise DocumentRunError("evidence members must be RetainedDocumentEvidence")
    _require_text(plan_evidence_id, "plan_evidence_id")
    _require_text(change_set_id, "change_set_id")
    _require_text(transaction_time, "transaction_time")
    _require_text(actor_id, "actor_id")
    if not callable(protocol_events):
        raise DocumentRunError("protocol_events must be callable")

    plan_bytes = canonical_assembly_plan_bytes(plan)
    plan_members = [item for item in evidence if item.record_id == plan_evidence_id]
    if len(plan_members) != 1 or plan_members[0].content != plan_bytes:
        raise DocumentRunError(
            "plan evidence ID must retain the canonical AssemblyPlan bytes"
        )
    operations = assembly_plan_to_operations(plan)

    record_ids = (
        _VALIDATED_CONTRACT_ID,
        _PARTIAL_CONTRACT_ID,
        _HISTORY_BINDING_ID,
        source.artifact_id,
        source.source_id,
        *(item.record_id for item in evidence),
    )
    if len(record_ids) != len(set(record_ids)):
        raise DocumentRunError("retained record IDs must be globally unique")

    history = KnowledgeChangeHistory(
        path,
        partial_contract=partial_contract,
        contract_view=contract_view,
        binding=binding,
    )
    anchors = (
        _artifact_anchor(
            _VALIDATED_CONTRACT_ID,
            contract_view.artifact_bytes,
            "application/json",
            "VALIDATED_CONTRACT",
        ),
        _artifact_anchor(
            _PARTIAL_CONTRACT_ID,
            partial_contract.canonical_bytes,
            "application/json",
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        _artifact_anchor(
            _HISTORY_BINDING_ID,
            binding.canonical_bytes,
            "application/json",
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        _artifact_anchor(
            source.artifact_id,
            source.content,
            source.media_type,
            "SOURCE_ARTIFACT",
        ),
        _source_anchor(source),
        *(
            _artifact_anchor(
                item.record_id,
                item.content,
                item.media_type,
                "RETAINED_EVIDENCE",
            )
            for item in evidence
        ),
    )
    history.append_anchors(
        anchors=anchors,
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    change_set = history.compose_change_set(
        change_set_id=change_set_id,
        source_record_ids=(source.source_id,),
        evidence_record_ids=tuple(item.record_id for item in evidence),
        operations=operations,
        valid_time=valid_time,
        supersedes=(),
    )
    before = history.replay()
    events = protocol_events(change_set, before.machine_state.identity)
    _require_lifecycle(events, binding)
    admitted = history.admit(
        change_set=change_set,
        machine_events=events,
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    expected_graph = admitted.graph.snapshot()
    expected_receipt = admitted.receipt.canonical_bytes
    expected_machine = admitted.machine_state.canonical_bytes
    del admitted
    del history

    replay = KnowledgeChangeHistory.reopen(path).replay()
    if (
        replay.graph.snapshot() != expected_graph
        or replay.receipt.canonical_bytes != expected_receipt
        or replay.machine_state.canonical_bytes != expected_machine
    ):
        raise DocumentRunError("ledger-only replay differs from admitted state")
    return DocumentRun(path.read_bytes(), replay)


__all__ = [
    "DocumentRun",
    "DocumentRunError",
    "RetainedDocumentEvidence",
    "RetainedDocumentSource",
    "run_document_history",
]
