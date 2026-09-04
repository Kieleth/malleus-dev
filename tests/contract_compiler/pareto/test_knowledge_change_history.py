"""Pareto RED contract for one private KnowledgeChangeSet history."""

from __future__ import annotations

import ast
from base64 import b64encode
from copy import deepcopy
from dataclasses import replace
from hashlib import sha256
import inspect
import json
from pathlib import Path

import pytest

import malleus._contract_pipeline.knowledge as knowledge_module
from malleus._contract_pipeline.knowledge import (
    KnowledgeAnchorInput,
    KnowledgeChangeHistory,
    KnowledgeChangeHistoryBinding,
    KnowledgeChangeRefusal,
    KnowledgeChangeRefusalReason,
    KnowledgeChangeSet,
    KnowledgeOperation,
    KnowledgeValidTime,
)
from malleus._contract_pipeline.machine import execute_event
from malleus.ledger import GENESIS, JsonlLedger
from tests.contract_compiler.pareto.test_protocol_machine import (
    CHECKS,
    POLICY_ID,
    _canonical,
    _effective,
    _event,
    _load_policy,
)
from tests.contract_compiler.pareto.test_validated_contract import (
    ROOT,
    _binding,
    _compile_binding,
    _trusted_types,
)


KCS_GRAMMAR = "malleus.knowledge-change-set/private-v0"
BINDING_GRAMMAR = "malleus.knowledge-history-binding/private-v0"
ROLE_BOUND_BINDING_GRAMMAR = "malleus.knowledge-history-binding/private-v1"
ARTIFACT_RETENTION_ROLES = [
    "KNOWLEDGE_HISTORY_BINDING",
    "PARTIAL_EFFECTIVE_CONTRACT",
    "RETAINED_EVIDENCE",
    "SOURCE_ARTIFACT",
    "VALIDATED_CONTRACT",
]
CONTRACT_KIND = "PRIVATE_PARTIAL_EFFECTIVE_CONTRACT_V0"
TRANSACTION_TIME = "2026-09-01T00:00:00Z"


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _generic_compilation():
    source = b"""\
id: https://example.malleus.dev/pareto-history
name: pareto_history
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  test: https://example.malleus.dev/pareto-history/
imports:
  - linkml:types
  - malleus
enums:
  LinkKind:
    permissible_values:
      LINKS:
slots:
  label:
    range: string
classes:
  LeftObject:
    is_a: Entity
    slots:
      - label
    slot_usage:
      label:
        required: true
  RightObject:
    is_a: Entity
    slots:
      - label
    slot_usage:
      label:
        required: true
  ObjectLink:
    is_a: Relation
    slot_usage:
      relation_type:
        range: LinkKind
        required: true
        equals_string: LINKS
      source_id:
        range: LeftObject
        required: true
      target_id:
        range: RightObject
        required: true
"""
    return _compile_binding(
        _binding(
            {
                "generic": source,
                "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
                "linkml:types": _trusted_types(),
            },
            "generic",
        )
    )


def _binding_payload() -> dict[str, object]:
    return {
        "accept_verdict": "ACCEPT",
        "decision": {
            "event_type": "VERDICT_RECORDED",
            "proposal_id_field": "proposal_id",
            "record_type": "DecisionRecord",
            "verdict_field": "verdict",
        },
        "grammar": BINDING_GRAMMAR,
        "proposal": {
            "change_set_identity_field": "knowledge_change_set_identity",
            "event_type": "CHANGE_PROPOSED",
            "proposal_id_field": "proposal_id",
            "record_type": "ProposalRecord",
        },
        "retention_events": {
            "ARTIFACT_REGISTERED": {
                "identity_field": "artifact_identity",
                "record_id_field": "artifact_id",
            },
            "SOURCE_REGISTERED": {
                "identity_field": "source_identity",
                "record_id_field": "source_id",
            },
        },
    }


def _role_bound_binding_payload() -> dict[str, object]:
    payload = deepcopy(_binding_payload())
    payload["grammar"] = ROLE_BOUND_BINDING_GRAMMAR
    retention = payload["retention_events"]
    assert isinstance(retention, dict)
    artifact = retention["ARTIFACT_REGISTERED"]
    source = retention["SOURCE_REGISTERED"]
    assert isinstance(artifact, dict)
    assert isinstance(source, dict)
    artifact["allowed_roles"] = list(ARTIFACT_RETENTION_ROLES)
    source["allowed_roles"] = ["RETAINED_SOURCE"]
    return payload


def _history(tmp_path: Path):
    compiled = _generic_compilation()
    partial = _effective(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256
    )
    binding = KnowledgeChangeHistoryBinding.from_bytes(_canonical(_binding_payload()))
    history = KnowledgeChangeHistory(
        tmp_path / "history.jsonl",
        partial_contract=partial,
        contract_view=compiled.view,
        binding=binding,
    )
    return history, compiled, partial, binding


def _anchor(
    history: KnowledgeChangeHistory,
    event: bytes,
    retained: bytes,
    role: str,
) -> None:
    result = history.append_anchor(
        machine_event=event,
        retained_bytes=retained,
        media_type="application/octet-stream",
        role=role,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    assert result.machine_receipt.outcome == "APPLIED"


def _anchored_history(tmp_path: Path, *, omit_bootstrap_role: str | None = None):
    history, compiled, partial, binding = _history(tmp_path)
    contract_bytes = partial.canonical_bytes
    source_bytes = b"generic retained source\n"
    evidence_bytes = b"generic retained evidence\n"
    source_identity = _digest(source_bytes)
    evidence_identity = _digest(evidence_bytes)
    anchors = (
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="validated-contract-artifact",
                artifact_identity=_digest(compiled.artifact.artifact_bytes),
            ),
            compiled.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="contract-artifact",
                artifact_identity=_digest(contract_bytes),
            ),
            contract_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="history-binding-artifact",
                artifact_identity=_digest(binding.canonical_bytes),
            ),
            binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="source-artifact",
                artifact_identity=source_identity,
            ),
            source_bytes,
            "SOURCE_ARTIFACT",
        ),
        (
            _event(
                "SOURCE_REGISTERED",
                artifact_id="source-artifact",
                source_id="source-generic",
                source_identity=source_identity,
            ),
            source_bytes,
            "RETAINED_SOURCE",
        ),
        (
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id="evidence-generic",
                artifact_identity=evidence_identity,
            ),
            evidence_bytes,
            "RETAINED_EVIDENCE",
        ),
    )
    for event, retained, role in anchors:
        if role != omit_bootstrap_role:
            _anchor(history, event, retained, role)
    replay = history.replay()
    assert replay.retained_bytes("source-generic") == source_bytes
    assert replay.retained_bytes("evidence-generic") == evidence_bytes
    raw_ledger = history.path.read_bytes()
    assert b64encode(source_bytes) in raw_ledger
    assert b64encode(evidence_bytes) in raw_ledger
    if omit_bootstrap_role != "VALIDATED_CONTRACT":
        assert b64encode(compiled.artifact.artifact_bytes) in raw_ledger
    assert tuple(history.path.parent.iterdir()) == (history.path,)
    return (
        history,
        compiled,
        partial,
        binding,
        source_identity,
        evidence_identity,
    )


@pytest.mark.parametrize(
    "missing_role",
    [
        "VALIDATED_CONTRACT",
        "PARTIAL_EFFECTIVE_CONTRACT",
        "KNOWLEDGE_HISTORY_BINDING",
    ],
)
def test_admission_requires_complete_jsonl_bootstrap(
    tmp_path: Path, missing_role: str
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(
        tmp_path, omit_bootstrap_role=missing_role
    )
    before = history.replay()
    change_set = _load_change(_base_payload(history, partial, source, evidence))
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        history.admit(
            change_set=change_set,
            machine_events=_protocol_events(change_set, before.machine_state.identity),
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert refusal.value.reason is KnowledgeChangeRefusalReason.MALFORMED_HISTORY
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == before.graph.snapshot()


def _base_payload(
    history: KnowledgeChangeHistory,
    partial,
    source_identity: str,
    evidence_identity: str,
) -> dict[str, object]:
    replay = history.replay()
    return {
        "base_acceptance_head": replay.acceptance_head,
        "base_accepted_state_digest": replay.graph.state_digest(),
        "base_ledger_event_count": replay.ledger_event_count,
        "base_ledger_head": replay.ledger_head,
        "base_materialization_head": replay.materialization_head,
        "change_set_id": "change-generic-1",
        "contract_identity": partial.identity,
        "contract_kind": CONTRACT_KIND,
        "evidence": [
            {
                "evidence_id": "evidence-generic",
                "sha256": evidence_identity,
            }
        ],
        "grammar": KCS_GRAMMAR,
        "operations": [
            {
                "depends_on": [],
                "operation_id": "operation-left",
                "operation_type": "CREATE_ENTITY",
                "ordinal": 0,
                "properties": {"label": "left"},
                "record_id": "left-1",
                "record_type": "LeftObject",
            },
            {
                "depends_on": [],
                "operation_id": "operation-right",
                "operation_type": "CREATE_ENTITY",
                "ordinal": 1,
                "properties": {"label": "right"},
                "record_id": "right-1",
                "record_type": "RightObject",
            },
            {
                "depends_on": ["operation-left", "operation-right"],
                "operation_id": "operation-link",
                "operation_type": "CREATE_RELATION",
                "ordinal": 2,
                "properties": {"relation_type": "LINKS"},
                "record_id": "link:left-1:right-1",
                "record_type": "ObjectLink",
                "source_id": "left-1",
                "target_id": "right-1",
            },
        ],
        "sources": [{"sha256": source_identity, "source_id": "source-generic"}],
        "supersedes": [],
        "valid_time": {
            "kind": "INSTANT",
            "value": "2026-09-01T00:00:00Z",
        },
    }


def _protocol_events(
    change_set: KnowledgeChangeSet,
    machine_state_identity: str,
    *,
    outcomes: tuple[str, str] = ("SATISFIED", "SATISFIED"),
    proposed_identity: str | None = None,
    identifier_suffix: str = "",
) -> tuple[bytes, ...]:
    policy = _load_policy()
    proposal_id = f"proposal-generic-1{identifier_suffix}"
    proposal = _event(
        "CHANGE_PROPOSED",
        expected_machine_state_identity=machine_state_identity,
        knowledge_change_set_identity=proposed_identity or change_set.identity,
        policy_id=POLICY_ID,
        policy_identity=policy.identity,
        proposal_id=proposal_id,
    )
    checks = tuple(
        _event(
            "CHECK_RECORDED",
            check_contract_id=check_id,
            check_contract_identity=check_identity,
            outcome=outcome,
            policy_identity=policy.identity,
            proposal_id=proposal_id,
            receipt_id=f"receipt-generic-{index}{identifier_suffix}",
        )
        for index, ((check_id, check_identity), outcome) in enumerate(
            zip(CHECKS, outcomes, strict=True)
        )
    )
    decision = _event(
        "VERDICT_RECORDED",
        decision_id=f"decision-generic-1{identifier_suffix}",
        proposal_id=proposal_id,
    )
    return (proposal, *checks, decision)


def _load_change(payload: dict[str, object]) -> KnowledgeChangeSet:
    return KnowledgeChangeSet.from_bytes(_canonical(payload))


def _ledger_bytes(history: KnowledgeChangeHistory) -> bytes:
    return history.path.read_bytes() if history.path.exists() else b""


def _compose(
    history: KnowledgeChangeHistory,
    partial,
    source_identity: str,
    evidence_identity: str,
    **replacements: object,
) -> KnowledgeChangeSet:
    manual = _load_change(
        _base_payload(history, partial, source_identity, evidence_identity)
    )
    values = {
        "change_set_id": manual.change_set_id,
        "source_record_ids": ("source-generic",),
        "evidence_record_ids": ("evidence-generic",),
        "operations": manual.operations,
        "valid_time": manual.valid_time,
        "supersedes": manual.supersedes,
    }
    values.update(replacements)
    return history.compose_change_set(**values)


def _evidence_anchor(record_id: str, content: bytes) -> KnowledgeAnchorInput:
    return KnowledgeAnchorInput(
        machine_event=_event(
            "ARTIFACT_REGISTERED",
            artifact_id=record_id,
            artifact_identity=_digest(content),
        ),
        retained_bytes=content,
        media_type="application/json",
        role="RETAINED_EVIDENCE",
    )


def _record_change(
    history: KnowledgeChangeHistory,
    partial,
    source_identity: str,
    evidence_identity: str,
    *,
    change_set_id: str,
    record_id: str,
    label: str,
    order: str,
    valid_time_kind: str = "ORDER_ONLY",
    supersedes_record_id: str | None = None,
) -> KnowledgeChangeSet:
    payload = _base_payload(history, partial, source_identity, evidence_identity)
    payload["change_set_id"] = change_set_id
    operation = {
        "depends_on": [],
        "operation_id": f"operation:{record_id}",
        "operation_type": "CREATE_ENTITY",
        "ordinal": 0,
        "properties": {"label": label},
        "record_id": record_id,
        "record_type": "LeftObject",
    }
    if supersedes_record_id is not None:
        operation["supersedes_record_id"] = supersedes_record_id
    payload["operations"] = [operation]
    payload["valid_time"] = {"kind": valid_time_kind, "value": order}
    return _load_change(payload)


def _admit_record_change(
    history: KnowledgeChangeHistory,
    change: KnowledgeChangeSet,
    *,
    suffix: str,
):
    before = history.replay()
    return history.admit(
        change_set=change,
        machine_events=_protocol_events(
            change,
            before.machine_state.identity,
            identifier_suffix=suffix,
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )


def test_change_set_is_closed_canonical_immutable_and_content_addressed(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    payload = _base_payload(history, partial, source, evidence)
    source_bytes = _canonical(payload)
    change_set = KnowledgeChangeSet.from_bytes(source_bytes)

    assert change_set.canonical_bytes == source_bytes
    assert change_set.identity == _digest(source_bytes)
    assert change_set.contract_kind == CONTRACT_KIND
    assert change_set.contract_identity == partial.identity
    assert [operation.ordinal for operation in change_set.operations] == [0, 1, 2]
    assert change_set.operations[2].depends_on == (
        "operation-left",
        "operation-right",
    )
    with pytest.raises(AttributeError):
        change_set.identity = "sha256:" + "0" * 64
    with pytest.raises(TypeError):
        change_set.data["extra"] = True


def test_history_composes_exact_current_change_without_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    expected = _load_change(_base_payload(history, partial, source, evidence))
    before = history.replay()
    ledger_before = _ledger_bytes(history)
    replay_calls = 0
    replay = history.replay

    def counted_replay():
        nonlocal replay_calls
        replay_calls += 1
        return replay()

    monkeypatch.setattr(history, "replay", counted_replay)

    composed = history.compose_change_set(
        change_set_id=expected.change_set_id,
        source_record_ids=("source-generic",),
        evidence_record_ids=("evidence-generic",),
        operations=expected.operations,
        valid_time=expected.valid_time,
        supersedes=expected.supersedes,
    )

    assert composed.canonical_bytes == expected.canonical_bytes
    assert composed == expected
    assert replay_calls == 1
    assert _ledger_bytes(history) == ledger_before
    assert replay().graph.snapshot() == before.graph.snapshot()
    assert replay().machine_state.identity == before.machine_state.identity


@pytest.mark.parametrize(
    ("replacement", "reason"),
    [
        (
            {"source_record_ids": ("source-absent",)},
            KnowledgeChangeRefusalReason.UNRETAINED_INPUT,
        ),
        (
            {"source_record_ids": ("evidence-generic",)},
            KnowledgeChangeRefusalReason.UNRETAINED_INPUT,
        ),
        (
            {"evidence_record_ids": ("evidence-absent",)},
            KnowledgeChangeRefusalReason.UNRETAINED_INPUT,
        ),
        (
            {"evidence_record_ids": ("source-generic",)},
            KnowledgeChangeRefusalReason.UNRETAINED_INPUT,
        ),
        (
            {"source_record_ids": ["source-generic"]},
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
        (
            {"source_record_ids": (1,)},
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
        (
            {"operations": []},
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
        (
            {"operations": (object(),)},
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
        (
            {"valid_time": "event-1"},
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
        (
            {"supersedes": ["change-before"]},
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
        (
            {"supersedes": (1,)},
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
    ],
)
def test_history_composer_refuses_bad_closures_and_shapes(
    tmp_path: Path,
    replacement: dict[str, object],
    reason: KnowledgeChangeRefusalReason,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        _compose(history, partial, source, evidence, **replacement)

    assert refusal.value.reason is reason
    assert _ledger_bytes(history) == ledger_before


def test_history_composer_preserves_explicit_order_and_identity_inputs(
    tmp_path: Path,
) -> None:
    history, compiled, partial, _, source, evidence = _anchored_history(tmp_path)
    second_source = b"second retained source\n"
    second_evidence = b"second retained evidence\n"
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="source-artifact-2",
            artifact_identity=_digest(second_source),
        ),
        second_source,
        "SOURCE_ARTIFACT",
    )
    _anchor(
        history,
        _event(
            "SOURCE_REGISTERED",
            artifact_id="source-artifact-2",
            source_id="source-generic-2",
            source_identity=_digest(second_source),
        ),
        second_source,
        "RETAINED_SOURCE",
    )
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="evidence-generic-2",
            artifact_identity=_digest(second_evidence),
        ),
        second_evidence,
        "RETAINED_EVIDENCE",
    )
    baseline = _compose(history, partial, source, evidence)
    reordered = tuple(
        replace(operation, ordinal=index)
        for index, operation in enumerate(
            (baseline.operations[1], baseline.operations[0], baseline.operations[2])
        )
    )

    variants = (
        _compose(
            history,
            partial,
            source,
            evidence,
            change_set_id="change-generic-2",
        ),
        _compose(
            history,
            partial,
            source,
            evidence,
            operations=reordered,
        ),
        _compose(
            history,
            partial,
            source,
            evidence,
            valid_time=KnowledgeValidTime("ORDER_ONLY", "event-1"),
        ),
        _compose(
            history,
            partial,
            source,
            evidence,
            supersedes=("change-before",),
        ),
        _compose(
            history,
            partial,
            source,
            evidence,
            source_record_ids=("source-generic-2", "source-generic"),
            evidence_record_ids=(
                "evidence-generic-2",
                "validated-contract-artifact",
                "evidence-generic",
            ),
        ),
    )

    assert all(candidate.identity != baseline.identity for candidate in variants)
    assert variants[1].operations == reordered
    assert variants[3].supersedes == ("change-before",)
    assert variants[4].sources == (
        ("source-generic-2", _digest(second_source)),
        ("source-generic", source),
    )
    assert variants[4].evidence == (
        ("evidence-generic-2", _digest(second_evidence)),
        (
            "validated-contract-artifact",
            _digest(compiled.artifact.artifact_bytes),
        ),
        ("evidence-generic", evidence),
    )


def test_history_composer_routes_invalid_operations_through_strict_parser(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    invalid = KnowledgeOperation(
        ordinal=0,
        operation_id="operation-invalid",
        operation_type="UNKNOWN",
        record_type="LeftObject",
        record_id="left-invalid",
        properties={"label": "invalid"},
        depends_on=(),
    )

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        _compose(
            history,
            partial,
            source,
            evidence,
            operations=(invalid,),
        )

    assert refusal.value.reason is KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET


def test_composed_change_goes_stale_after_an_intervening_event(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    composed = _compose(history, partial, source, evidence)
    later = b'{"outcome":"SATISFIED","receipt":"later"}'
    _anchor(
        history,
        _event(
            "ARTIFACT_REGISTERED",
            artifact_id="evidence-later",
            artifact_identity=_digest(later),
        ),
        later,
        "RETAINED_EVIDENCE",
    )
    before = history.replay()
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        history.admit(
            change_set=composed,
            machine_events=_protocol_events(
                composed, before.machine_state.identity, identifier_suffix="-stale"
            ),
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert refusal.value.reason is KnowledgeChangeRefusalReason.STALE_BASE
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == before.graph.snapshot()


def test_composed_change_admits_and_reopens_with_exact_parity(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    before = history.replay()
    composed = _compose(history, partial, source, evidence)

    admitted = history.admit(
        change_set=composed,
        machine_events=_protocol_events(composed, before.machine_state.identity),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()

    assert admitted.change_sets == (composed,)
    assert reopened.change_sets == admitted.change_sets
    assert reopened.graph.snapshot() == admitted.graph.snapshot()
    assert reopened.receipt.canonical_bytes == admitted.receipt.canonical_bytes


def test_composer_binds_and_replays_a_superseding_second_change(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-1",
        record_id="left-version-1",
        label="before",
        order="event-1",
    )
    _admit_record_change(history, first, suffix="-version-1")
    base = history.replay()
    assert base.acceptance_head != GENESIS
    assert base.materialization_head != GENESIS
    operation = KnowledgeOperation(
        ordinal=0,
        operation_id="operation:left-version-2",
        operation_type="CREATE_ENTITY",
        record_type="LeftObject",
        record_id="left-version-2",
        properties={"label": "after"},
        depends_on=(),
        supersedes_record_id="left-version-1",
    )

    second = history.compose_change_set(
        change_set_id="change-version-2",
        source_record_ids=("source-generic",),
        evidence_record_ids=("evidence-generic",),
        operations=(operation,),
        valid_time=KnowledgeValidTime("ORDER_ONLY", "event-2"),
        supersedes=(first.change_set_id,),
    )
    expected = {
        "base_acceptance_head": base.acceptance_head,
        "base_accepted_state_digest": base.graph.state_digest(),
        "base_ledger_event_count": base.ledger_event_count,
        "base_ledger_head": base.ledger_head,
        "base_materialization_head": base.materialization_head,
        "change_set_id": "change-version-2",
        "contract_identity": partial.identity,
        "contract_kind": CONTRACT_KIND,
        "evidence": [{"evidence_id": "evidence-generic", "sha256": evidence}],
        "grammar": KCS_GRAMMAR,
        "operations": [
            {
                "depends_on": [],
                "operation_id": "operation:left-version-2",
                "operation_type": "CREATE_ENTITY",
                "ordinal": 0,
                "properties": {"label": "after"},
                "record_id": "left-version-2",
                "record_type": "LeftObject",
                "supersedes_record_id": "left-version-1",
            }
        ],
        "sources": [{"sha256": source, "source_id": "source-generic"}],
        "supersedes": [first.change_set_id],
        "valid_time": {"kind": "ORDER_ONLY", "value": "event-2"},
    }
    assert second.canonical_bytes == _canonical(expected)

    admitted = _admit_record_change(history, second, suffix="-version-2")
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()

    assert admitted.change_sets == (first, second)
    assert reopened.change_sets == admitted.change_sets
    assert reopened.graph.snapshot() == admitted.graph.snapshot()
    assert reopened.record_history == admitted.record_history
    assert reopened.receipt.canonical_bytes == admitted.receipt.canonical_bytes


def test_history_composer_remains_private() -> None:
    import malleus
    import malleus._contract_pipeline as contract_pipeline

    assert "compose_change_set" not in knowledge_module.__all__
    assert not hasattr(malleus, "compose_change_set")
    assert not hasattr(contract_pipeline, "compose_change_set")
    assert not hasattr(malleus, "KnowledgeChangeHistory")
    assert not hasattr(contract_pipeline, "KnowledgeChangeHistory")


@pytest.mark.parametrize(
    "field",
    [
        "base_acceptance_head",
        "base_accepted_state_digest",
        "base_ledger_event_count",
        "base_ledger_head",
        "base_materialization_head",
        "change_set_id",
        "contract_identity",
        "evidence",
        "operations",
        "sources",
        "supersedes",
        "valid_time",
    ],
)
def test_every_governed_field_changes_change_set_identity(
    tmp_path: Path, field: str
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    baseline_payload = _base_payload(history, partial, source, evidence)
    changed = json.loads(_canonical(baseline_payload))
    replacements: dict[str, object] = {
        "base_acceptance_head": "sha256:" + "1" * 64,
        "base_accepted_state_digest": "sha256:" + "2" * 64,
        "base_ledger_event_count": changed["base_ledger_event_count"] + 1,
        "base_ledger_head": "sha256:" + "3" * 64,
        "base_materialization_head": "sha256:" + "4" * 64,
        "change_set_id": "change-generic-2",
        "contract_identity": "sha256:" + "5" * 64,
        "evidence": [{"evidence_id": "evidence-other", "sha256": "sha256:" + "6" * 64}],
        "sources": [{"sha256": "sha256:" + "7" * 64, "source_id": "source-other"}],
        "supersedes": ["change-before"],
        "valid_time": {"kind": "ORDER_ONLY", "value": "event-1"},
    }
    if field == "operations":
        changed["operations"][0]["properties"]["label"] = "changed"
    else:
        changed[field] = replacements[field]

    assert _load_change(changed).identity != _load_change(baseline_payload).identity


def test_unknown_missing_tampered_noncanonical_and_cycles_refuse(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    payload = _base_payload(history, partial, source, evidence)

    unknown = json.loads(_canonical(payload))
    unknown["extra"] = True
    missing = json.loads(_canonical(payload))
    del missing["base_ledger_head"]
    wrong_grammar = json.loads(_canonical(payload))
    wrong_grammar["grammar"] = "unknown"
    wrong_contract_kind = json.loads(_canonical(payload))
    wrong_contract_kind["contract_kind"] = "OTHER_CONTRACT_KIND"
    dangling = json.loads(_canonical(payload))
    dangling["operations"][2]["depends_on"] = ["operation-absent"]
    cyclic = json.loads(_canonical(payload))
    cyclic["operations"][0]["depends_on"] = ["operation-link"]
    cases = (
        (
            _canonical(unknown),
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
        (
            _canonical(missing),
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
        (
            json.dumps(payload, indent=2, sort_keys=True).encode(),
            KnowledgeChangeRefusalReason.NONCANONICAL_CHANGE_SET,
        ),
        (
            _canonical(wrong_grammar),
            KnowledgeChangeRefusalReason.UNSUPPORTED_GRAMMAR,
        ),
        (
            _canonical(wrong_contract_kind),
            KnowledgeChangeRefusalReason.UNSUPPORTED_CONTRACT_KIND,
        ),
        (
            _canonical(dangling),
            KnowledgeChangeRefusalReason.MALFORMED_CHANGE_SET,
        ),
        (
            _canonical(cyclic),
            KnowledgeChangeRefusalReason.CYCLIC_OPERATION_DEPENDENCY,
        ),
    )
    for source_bytes, reason in cases:
        with pytest.raises(KnowledgeChangeRefusal) as refusal:
            KnowledgeChangeSet.from_bytes(source_bytes)
        assert refusal.value.reason is reason

    valid = _load_change(payload)
    forged = replace(valid, identity="sha256:" + "0" * 64)
    before = _ledger_bytes(history)
    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        history.admit(
            change_set=forged,
            machine_events=_protocol_events(
                valid, history.replay().machine_state.identity
            ),
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert refusal.value.reason is KnowledgeChangeRefusalReason.IDENTITY_MISMATCH
    assert _ledger_bytes(history) == before


def test_genesis_change_is_retained_then_accepted_and_replayed_from_empty(
    tmp_path: Path,
) -> None:
    history, compiled, partial, binding, source, evidence = _anchored_history(tmp_path)
    before = history.replay()
    assert before.graph.node_count == 0
    assert before.graph.edge_count == 0
    change_set = _load_change(_base_payload(history, partial, source, evidence))
    events = _protocol_events(change_set, before.machine_state.identity)

    admitted = history.admit(
        change_set=change_set,
        machine_events=events,
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    ledger = JsonlLedger(
        history.path,
        compiled.artifact.validated_fact_set_sha256,
    ).read()
    assert [event["event_type"] for event in ledger[-5:]] == [
        "KNOWLEDGE_CHANGE_SET_RETAINED",
        "CHANGE_PROPOSED",
        "CHECK_RECORDED",
        "CHECK_RECORDED",
        "VERDICT_RECORDED",
    ]
    assert ledger[-5]["payload"]["change_set_identity"] == change_set.identity
    assert b64encode(change_set.canonical_bytes) in history.path.read_bytes()
    assert ledger[-4]["payload"]["knowledge_change_set_identity"] == (
        change_set.identity
    )
    assert admitted.graph.query("LeftObject", label="left") == [
        {"id": "left-1", "label": "left", "type": "LeftObject"}
    ]
    assert admitted.graph.query("RightObject", label="right") == [
        {"id": "right-1", "label": "right", "type": "RightObject"}
    ]
    assert admitted.graph.query_relations(
        "ObjectLink", source_id="left-1", target_id="right-1"
    ) == [
        {
            "key": "link:left-1:right-1",
            "relation_type": "LINKS",
            "source_id": "left-1",
            "target_id": "right-1",
            "type": "ObjectLink",
        }
    ]
    assert admitted.acceptance_head != GENESIS
    assert admitted.materialization_head != GENESIS
    assert admitted.receipt.identity == _digest(admitted.receipt.canonical_bytes)

    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    rebuilt = KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.graph.snapshot() == admitted.graph.snapshot()
    assert rebuilt.graph.state_digest() == admitted.graph.state_digest()
    assert (
        reopened.machine_state.canonical_bytes == admitted.machine_state.canonical_bytes
    )
    assert reopened.receipt.canonical_bytes == rebuilt.receipt.canonical_bytes
    assert reopened.partial_contract.identity == partial.identity
    assert reopened.contract_view.content_hash() == compiled.view.content_hash()
    assert reopened.binding.identity == binding.identity

    copied_path = tmp_path / "copied/history.jsonl"
    copied_path.parent.mkdir()
    copied_path.write_bytes(history.path.read_bytes())
    copied = KnowledgeChangeHistory.reopen(copied_path).replay()
    assert copied.graph.snapshot() == admitted.graph.snapshot()
    assert copied.machine_state.identity == admitted.machine_state.identity
    assert tuple(copied_path.parent.iterdir()) == (copied_path,)


def test_later_record_closes_prior_record_and_replay_answers_both_orders(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-1",
        record_id="left-version-1",
        label="before",
        order="event-1",
    )
    first_replay = _admit_record_change(history, first, suffix="-version-1")
    second = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-2",
        record_id="left-version-2",
        label="after",
        order="event-2",
        supersedes_record_id="left-version-1",
    )

    current = _admit_record_change(history, second, suffix="-version-2")
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()

    assert first_replay.graph.query("LeftObject") == [
        {"id": "left-version-1", "label": "before", "type": "LeftObject"}
    ]
    assert current.graph.query("LeftObject") == [
        {"id": "left-version-2", "label": "after", "type": "LeftObject"}
    ]
    assert current.graph_at_change(first.change_set_id).snapshot() == (
        first_replay.graph.snapshot()
    )
    assert current.graph_at_change(second.change_set_id).snapshot() == (
        current.graph.snapshot()
    )
    assert reopened.graph.snapshot() == current.graph.snapshot()
    assert reopened.graph_at_change(first.change_set_id).snapshot() == (
        first_replay.graph.snapshot()
    )

    prior = current.record_history["left-version-1"]
    replacement = current.record_history["left-version-2"]
    assert prior.valid_from == first.valid_time
    assert prior.valid_to == second.valid_time
    assert prior.supersedes_record_id is None
    assert prior.superseded_by == "left-version-2"
    assert replacement.valid_from == second.valid_time
    assert replacement.valid_to is None
    assert replacement.supersedes_record_id == "left-version-1"
    assert replacement.superseded_by is None

    with pytest.raises(KeyError, match="unknown accepted change"):
        current.graph_at_change("change-absent")
    with pytest.raises(TypeError):
        current.record_history["left-version-1"] = replacement


@pytest.mark.parametrize("failure", ["unknown", "self", "fork", "reuse"])
def test_record_supersession_refuses_atomically(tmp_path: Path, failure: str) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-1",
        record_id="left-version-1",
        label="before",
        order="event-1",
    )
    _admit_record_change(history, first, suffix="-version-1")
    if failure == "fork":
        second = _record_change(
            history,
            partial,
            source,
            evidence,
            change_set_id="change-version-2",
            record_id="left-version-2",
            label="after",
            order="event-2",
            supersedes_record_id="left-version-1",
        )
        _admit_record_change(history, second, suffix="-version-2")

    target = {
        "unknown": "left-absent",
        "self": "left-version-3",
        "fork": "left-version-1",
        "reuse": None,
    }[failure]
    candidate = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-3",
        record_id="left-version-1" if failure == "reuse" else "left-version-3",
        label="candidate",
        order="event-3",
        supersedes_record_id=target,
    )
    before = history.replay()
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        _admit_record_change(history, candidate, suffix="-version-3")

    assert refusal.value.reason in {
        KnowledgeChangeRefusalReason.UNKNOWN_SUPERSESSION,
        KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL,
    }
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == before.graph.snapshot()
    assert history.replay().record_history == before.record_history


@pytest.mark.parametrize(
    "replacement_time",
    ["2026-09-01T00:00:00Z", "2026-08-31T23:59:59Z"],
)
def test_instant_replacement_must_follow_prior_valid_time(
    tmp_path: Path, replacement_time: str
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-1",
        record_id="left-version-1",
        label="before",
        order="2026-09-02T00:00:00Z",
        valid_time_kind="INSTANT",
    )
    _admit_record_change(history, first, suffix="-version-1")
    earlier = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-2",
        record_id="left-version-2",
        label="earlier",
        order=replacement_time,
        valid_time_kind="INSTANT",
        supersedes_record_id="left-version-1",
    )
    before = history.replay()
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        _admit_record_change(history, earlier, suffix="-version-2")

    assert refusal.value.reason is KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == before.graph.snapshot()


@pytest.mark.parametrize(
    ("initial_kind", "initial_value", "replacement_kind", "replacement_value"),
    [
        ("INSTANT", "2026-09-01T00:00:00Z", "ORDER_ONLY", "event-2"),
        ("ORDER_ONLY", "event-1", "INSTANT", "2026-09-02T00:00:00Z"),
    ],
)
def test_record_replacement_cannot_mix_valid_time_kinds(
    tmp_path: Path,
    initial_kind: str,
    initial_value: str,
    replacement_kind: str,
    replacement_value: str,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-1",
        record_id="left-version-1",
        label="before",
        order=initial_value,
        valid_time_kind=initial_kind,
    )
    _admit_record_change(history, first, suffix="-version-1")
    mixed = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-2",
        record_id="left-version-2",
        label="after",
        order=replacement_value,
        valid_time_kind=replacement_kind,
        supersedes_record_id="left-version-1",
    )
    before = history.replay()
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        _admit_record_change(history, mixed, suffix="-version-2")

    assert refusal.value.reason is KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL
    assert "valid-time kind differs" in refusal.value.detail
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == before.graph.snapshot()
    assert history.replay().record_history == before.record_history


def test_record_supersession_cannot_change_record_type(tmp_path: Path) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-1",
        record_id="left-version-1",
        label="before",
        order="event-1",
    )
    _admit_record_change(history, first, suffix="-version-1")
    payload = _base_payload(history, partial, source, evidence)
    payload["change_set_id"] = "change-version-2"
    payload["operations"] = [
        {
            "depends_on": [],
            "operation_id": "operation:right-version-2",
            "operation_type": "CREATE_ENTITY",
            "ordinal": 0,
            "properties": {"label": "after"},
            "record_id": "right-version-2",
            "record_type": "RightObject",
            "supersedes_record_id": "left-version-1",
        }
    ]
    payload["valid_time"] = {"kind": "ORDER_ONLY", "value": "event-2"}
    candidate = _load_change(payload)
    before = history.replay()
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        _admit_record_change(history, candidate, suffix="-version-2")

    assert refusal.value.reason is KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == before.graph.snapshot()


def test_entity_and_its_relation_can_be_replaced_together(tmp_path: Path) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _load_change(_base_payload(history, partial, source, evidence))
    before_first = history.replay()
    history.admit(
        change_set=first,
        machine_events=_protocol_events(first, before_first.machine_state.identity),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    payload = _base_payload(history, partial, source, evidence)
    payload["change_set_id"] = "change-generic-2"
    payload["operations"] = [
        {
            "depends_on": [],
            "operation_id": "operation-left-2",
            "operation_type": "CREATE_ENTITY",
            "ordinal": 0,
            "properties": {"label": "left-2"},
            "record_id": "left-2",
            "record_type": "LeftObject",
            "supersedes_record_id": "left-1",
        },
        {
            "depends_on": ["operation-left-2"],
            "operation_id": "operation-link-2",
            "operation_type": "CREATE_RELATION",
            "ordinal": 1,
            "properties": {"relation_type": "LINKS"},
            "record_id": "link:left-2:right-1",
            "record_type": "ObjectLink",
            "source_id": "left-2",
            "supersedes_record_id": "link:left-1:right-1",
            "target_id": "right-1",
        },
    ]
    payload["valid_time"] = {
        "kind": "INSTANT",
        "value": "2026-09-02T00:00:00Z",
    }
    replacement = _load_change(payload)

    replay = _admit_record_change(history, replacement, suffix="-replacement")

    assert replay.graph.query("LeftObject") == [
        {"id": "left-2", "label": "left-2", "type": "LeftObject"}
    ]
    assert replay.graph.query_relations("ObjectLink") == [
        {
            "key": "link:left-2:right-1",
            "relation_type": "LINKS",
            "source_id": "left-2",
            "target_id": "right-1",
            "type": "ObjectLink",
        }
    ]


def test_historical_graph_results_are_defensive_copies(tmp_path: Path) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    first = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-version-1",
        record_id="left-version-1",
        label="before",
        order="event-1",
    )
    replay = _admit_record_change(history, first, suffix="-version-1")
    expected = replay.graph_at_change(first.change_set_id).snapshot()

    caller_copy = replay.graph_at_change(first.change_set_id)
    assert (
        caller_copy.create_entity(
            "RightObject", "caller-only", {"label": "caller-only"}
        ).op_status.value
        == "COMMITTED"
    )

    assert replay.graph_at_change(first.change_set_id).snapshot() == expected


def test_admit_with_anchors_commits_receipts_and_change_in_one_batch(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    before = history.replay()
    receipt = _evidence_anchor("receipt-evidence", b'{"outcome":"SATISFIED"}')
    after_anchor = execute_event(
        partial, before.machine_state, receipt.machine_event
    ).state
    change = _load_change(_base_payload(history, partial, source, evidence))

    replay = history.admit_with_anchors(
        anchors=(receipt,),
        change_set=change,
        machine_events=_protocol_events(change, after_anchor.identity),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    assert replay.change_sets == (change,)
    assert replay.retained_bytes("receipt-evidence") == receipt.retained_bytes


def test_admit_with_anchors_refuses_the_whole_batch_when_admission_is_incomplete(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    before = history.replay()
    receipt = _evidence_anchor("receipt-evidence", b'{"outcome":"SATISFIED"}')
    after_anchor = execute_event(
        partial, before.machine_state, receipt.machine_event
    ).state
    change = _load_change(_base_payload(history, partial, source, evidence))
    proposal_only = _protocol_events(change, after_anchor.identity)[:1]
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        history.admit_with_anchors(
            anchors=(receipt,),
            change_set=change,
            machine_events=proposal_only,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )

    assert refusal.value.reason is KnowledgeChangeRefusalReason.INCOMPLETE_ADMISSION
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == before.graph.snapshot()
    with pytest.raises(KeyError, match="unknown retained record"):
        history.replay().retained_bytes("receipt-evidence")


def test_entity_replacement_with_live_relation_refuses_atomically(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    before_first = history.replay()
    first = _load_change(_base_payload(history, partial, source, evidence))
    history.admit(
        change_set=first,
        machine_events=_protocol_events(first, before_first.machine_state.identity),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    replacement = _record_change(
        history,
        partial,
        source,
        evidence,
        change_set_id="change-generic-2",
        record_id="left-2",
        label="left-2",
        order="2026-09-02T00:00:00Z",
        valid_time_kind="INSTANT",
        supersedes_record_id="left-1",
    )
    before = history.replay()
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        _admit_record_change(history, replacement, suffix="-version-2")

    assert refusal.value.reason is KnowledgeChangeRefusalReason.STRUCTURAL_REFUSAL
    assert "does not exist" in refusal.value.detail
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == before.graph.snapshot()
    assert history.replay().record_history == before.record_history


def test_admit_requires_one_complete_accepted_lifecycle(tmp_path: Path) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    before = history.replay()
    change_set = _load_change(_base_payload(history, partial, source, evidence))
    proposal_only = _protocol_events(change_set, before.machine_state.identity)[:1]
    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        history.admit(
            change_set=change_set,
            machine_events=proposal_only,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert refusal.value.reason is KnowledgeChangeRefusalReason.INCOMPLETE_ADMISSION
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == before.graph.snapshot()


@pytest.mark.parametrize("entrypoint", ["anchor", "admit"])
def test_persistence_envelope_refusals_are_typed_and_atomic(
    tmp_path: Path, entrypoint: str
) -> None:
    if entrypoint == "anchor":
        history, _, _, _ = _history(tmp_path)
        retained = b"retained bytes"

        def invoke():
            return history.append_anchor(
                machine_event=_event(
                    "ARTIFACT_REGISTERED",
                    artifact_id="artifact-invalid-time",
                    artifact_identity=_digest(retained),
                ),
                retained_bytes=retained,
                media_type="application/octet-stream",
                role="RETAINED_EVIDENCE",
                transaction_time="not-a-time",
                actor_id="actor:test",
            )

    else:
        history, _, partial, _, source, evidence = _anchored_history(tmp_path)
        before = history.replay()
        change_set = _load_change(_base_payload(history, partial, source, evidence))

        def invoke():
            return history.admit(
                change_set=change_set,
                machine_events=_protocol_events(
                    change_set, before.machine_state.identity
                ),
                transaction_time="not-a-time",
                actor_id="actor:test",
            )

    ledger_before = _ledger_bytes(history)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        invoke()
    assert refusal.value.reason is KnowledgeChangeRefusalReason.MALFORMED_HISTORY
    assert _ledger_bytes(history) == ledger_before


@pytest.mark.parametrize("self_supersedes", [False, True])
def test_change_set_ids_are_unique_and_cannot_self_supersede(
    tmp_path: Path, self_supersedes: bool
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    before = history.replay()
    first = _load_change(_base_payload(history, partial, source, evidence))
    history.admit(
        change_set=first,
        machine_events=_protocol_events(first, before.machine_state.identity),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    before_second = history.replay()
    payload = _base_payload(history, partial, source, evidence)
    payload["operations"] = [
        {
            "depends_on": [],
            "operation_id": "operation-left-2",
            "operation_type": "CREATE_ENTITY",
            "ordinal": 0,
            "properties": {"label": "left-2"},
            "record_id": "left-2",
            "record_type": "LeftObject",
        }
    ]
    if self_supersedes:
        payload["supersedes"] = [first.change_set_id]
    second = _load_change(payload)
    assert second.change_set_id == first.change_set_id
    assert second.identity != first.identity

    ledger_before = _ledger_bytes(history)
    graph_before = before_second.graph.snapshot()
    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        history.admit(
            change_set=second,
            machine_events=_protocol_events(
                second,
                before_second.machine_state.identity,
                identifier_suffix="-second",
            ),
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert refusal.value.reason is KnowledgeChangeRefusalReason.IDENTITY_MISMATCH
    assert _ledger_bytes(history) == ledger_before
    assert history.replay().graph.snapshot() == graph_before


@pytest.mark.parametrize(
    "failure",
    [
        "malformed",
        "rejected",
        "stale_ledger_head",
        "stale_ledger_count",
        "stale_acceptance_head",
        "stale_materialization_head",
        "stale_state",
        "wrong_contract",
        "wrong_contract_kind",
        "dangling_supersession",
        "structural",
        "unregistered",
        "unretained_source",
        "unretained_evidence",
        "role_swapped",
        "source_digest_mismatch",
        "evidence_digest_mismatch",
    ],
)
def test_refused_change_never_changes_ledger_or_replayed_graph(
    tmp_path: Path, failure: str
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    before = history.replay()
    payload = _base_payload(history, partial, source, evidence)
    change_set = _load_change(payload)
    events = _protocol_events(change_set, before.machine_state.identity)

    if failure == "malformed":
        change_set = replace(change_set, canonical_bytes=b"{}")
    elif failure == "rejected":
        events = _protocol_events(
            change_set,
            before.machine_state.identity,
            outcomes=("SATISFIED", "VIOLATED"),
        )
    elif failure == "stale_ledger_head":
        payload["base_ledger_head"] = "sha256:" + "9" * 64
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "stale_ledger_count":
        payload["base_ledger_event_count"] += 1
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "stale_acceptance_head":
        payload["base_acceptance_head"] = "sha256:" + "9" * 64
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "stale_materialization_head":
        payload["base_materialization_head"] = "sha256:" + "9" * 64
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "stale_state":
        payload["base_accepted_state_digest"] = "sha256:" + "9" * 64
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "wrong_contract":
        payload["contract_identity"] = "sha256:" + "9" * 64
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "wrong_contract_kind":
        change_set = replace(
            change_set,
            contract_kind="OTHER_CONTRACT_KIND",
        )
    elif failure == "dangling_supersession":
        payload["supersedes"] = ["change-absent"]
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "structural":
        payload["operations"][2]["properties"]["relation_type"] = "INVALID"
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "unregistered":
        events = _protocol_events(
            change_set,
            before.machine_state.identity,
            proposed_identity="sha256:" + "8" * 64,
        )
    elif failure == "unretained_source":
        payload["sources"] = [
            {"sha256": "sha256:" + "8" * 64, "source_id": "source-absent"}
        ]
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "unretained_evidence":
        payload["evidence"] = [
            {
                "evidence_id": "evidence-absent",
                "sha256": "sha256:" + "8" * 64,
            }
        ]
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "role_swapped":
        payload["sources"] = [{"sha256": evidence, "source_id": "evidence-generic"}]
        payload["evidence"] = [{"evidence_id": "source-generic", "sha256": source}]
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    elif failure == "source_digest_mismatch":
        payload["sources"][0]["sha256"] = "sha256:" + "8" * 64
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)
    else:
        payload["evidence"][0]["sha256"] = "sha256:" + "8" * 64
        change_set = _load_change(payload)
        events = _protocol_events(change_set, before.machine_state.identity)

    ledger_before = _ledger_bytes(history)
    graph_before = before.graph.snapshot()
    with pytest.raises(KnowledgeChangeRefusal):
        history.admit(
            change_set=change_set,
            machine_events=events,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    after = history.replay()
    assert _ledger_bytes(history) == ledger_before
    assert after.graph.snapshot() == graph_before
    assert after.machine_state.identity == before.machine_state.identity


def test_anchor_refuses_bytes_that_do_not_match_machine_identity(
    tmp_path: Path,
) -> None:
    history, _, _, _ = _history(tmp_path)
    before = history.replay()
    expected = b"expected retained bytes\n"
    event = _event(
        "ARTIFACT_REGISTERED",
        artifact_id="artifact-generic",
        artifact_identity=_digest(expected),
    )

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        history.append_anchor(
            machine_event=event,
            retained_bytes=b"different retained bytes\n",
            media_type="application/octet-stream",
            role="SOURCE_ARTIFACT",
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert refusal.value.reason is KnowledgeChangeRefusalReason.RETAINED_BYTES_MISMATCH
    assert _ledger_bytes(history) == b""
    assert history.replay().graph.snapshot() == before.graph.snapshot()


@pytest.mark.parametrize(
    "role",
    [
        "VALIDATED_CONTRACT",
        "PARTIAL_EFFECTIVE_CONTRACT",
        "KNOWLEDGE_HISTORY_BINDING",
    ],
)
def test_bootstrap_anchor_bytes_must_match_the_active_history(
    tmp_path: Path, role: str
) -> None:
    history, _, _, _ = _history(tmp_path)
    retained = b"self-hashed but unrelated bootstrap bytes"
    event = _event(
        "ARTIFACT_REGISTERED",
        artifact_id=f"wrong:{role}",
        artifact_identity=_digest(retained),
    )

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        history.append_anchor(
            machine_event=event,
            retained_bytes=retained,
            media_type="application/octet-stream",
            role=role,
            transaction_time=TRANSACTION_TIME,
            actor_id="actor:test",
        )
    assert refusal.value.reason is KnowledgeChangeRefusalReason.IDENTITY_MISMATCH
    assert _ledger_bytes(history) == b""


def test_returned_graph_and_queries_are_disposable_replay_views(
    tmp_path: Path,
) -> None:
    history, _, partial, _, source, evidence = _anchored_history(tmp_path)
    before = history.replay()
    change_set = _load_change(_base_payload(history, partial, source, evidence))
    admitted = history.admit(
        change_set=change_set,
        machine_events=_protocol_events(change_set, before.machine_state.identity),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    query = admitted.graph.query("LeftObject")
    query[0]["label"] = "mutated-query"
    extra = admitted.graph.create_entity(
        "LeftObject", "caller-only", {"label": "caller-only"}
    )
    assert extra.op_status.value == "COMMITTED"

    replayed = history.replay()
    assert replayed.graph.get_node("caller-only") is None
    assert replayed.graph.get_node("left-1")["label"] == "left"
    assert replayed.graph.state_digest() != admitted.graph.state_digest()


def test_private_epoch_has_no_legacy_fallback_or_graph_writer_surface() -> None:
    source = inspect.getsource(knowledge_module)
    tree = ast.parse(source)
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports.update(
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    )
    assert {
        "malleus.accepted",
        "malleus.assent",
        "malleus.staging",
    }.isdisjoint(imports)
    assert all(
        name not in source
        for name in (
            "AcceptedGraphApplication",
            "CandidateSubgraphArtifact",
            "GraphBaseArtifact",
            "GraphRecipe",
            "SemanticReentry",
            "accepted_graph_base",
        )
    )
    assert not hasattr(knowledge_module, "GraphWriter")
    assert not hasattr(knowledge_module, "SecondChangeIdentity")
    for method in (
        KnowledgeChangeHistory.__init__,
        KnowledgeChangeHistory.admit,
        KnowledgeChangeHistory.replay,
    ):
        assert {
            "accepted_graph_base",
            "graph",
            "graph_writer",
        }.isdisjoint(inspect.signature(method).parameters)


def test_history_binding_is_canonical_and_data_owns_machine_vocabulary() -> None:
    payload = _binding_payload()
    source = _canonical(payload)
    binding = KnowledgeChangeHistoryBinding.from_bytes(source)

    assert binding.canonical_bytes == source
    assert binding.identity == _digest(source)
    assert binding.data["proposal"]["change_set_identity_field"] == (
        "knowledge_change_set_identity"
    )
    noncanonical = json.dumps(payload, indent=2, sort_keys=True).encode()
    with pytest.raises(KnowledgeChangeRefusal):
        KnowledgeChangeHistoryBinding.from_bytes(noncanonical)

    production = inspect.getsource(knowledge_module)
    for literal in (
        "ARTIFACT_REGISTERED",
        "SOURCE_REGISTERED",
        "CHANGE_PROPOSED",
        "VERDICT_RECORDED",
        "ProposalRecord",
        "DecisionRecord",
        "knowledge_change_set_identity",
    ):
        assert literal not in production


def test_role_bound_history_binding_is_canonical_and_closed() -> None:
    payload = _role_bound_binding_payload()
    source = _canonical(payload)

    binding = KnowledgeChangeHistoryBinding.from_bytes(source)

    assert binding.canonical_bytes == source
    assert binding.identity == _digest(source)
    assert binding.data["retention_events"]["ARTIFACT_REGISTERED"][
        "allowed_roles"
    ] == tuple(ARTIFACT_RETENTION_ROLES)
    assert binding.data["retention_events"]["SOURCE_REGISTERED"]["allowed_roles"] == (
        "RETAINED_SOURCE",
    )


@pytest.mark.parametrize(
    "mutation",
    ["missing", "extra", "empty", "duplicate", "unsorted", "unknown", "not-list"],
)
def test_role_bound_history_binding_refuses_ambiguous_role_sets(
    mutation: str,
) -> None:
    payload = _role_bound_binding_payload()
    retention = payload["retention_events"]
    assert isinstance(retention, dict)
    artifact = retention["ARTIFACT_REGISTERED"]
    assert isinstance(artifact, dict)
    if mutation == "missing":
        del artifact["allowed_roles"]
    elif mutation == "extra":
        artifact["extra"] = True
    elif mutation == "empty":
        artifact["allowed_roles"] = []
    elif mutation == "duplicate":
        artifact["allowed_roles"] = ["RETAINED_EVIDENCE", "RETAINED_EVIDENCE"]
    elif mutation == "unsorted":
        artifact["allowed_roles"] = ["VALIDATED_CONTRACT", "RETAINED_EVIDENCE"]
    elif mutation == "unknown":
        artifact["allowed_roles"] = ["SOMETHING_ELSE"]
    elif mutation == "not-list":
        artifact["allowed_roles"] = "RETAINED_EVIDENCE"
    else:
        raise AssertionError(mutation)

    with pytest.raises(KnowledgeChangeRefusal) as refusal:
        KnowledgeChangeHistoryBinding.from_bytes(_canonical(payload))

    assert refusal.value.reason is KnowledgeChangeRefusalReason.MALFORMED_BINDING
