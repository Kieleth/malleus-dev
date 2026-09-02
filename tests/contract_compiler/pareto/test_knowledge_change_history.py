"""Pareto RED contract for one private KnowledgeChangeSet history."""

from __future__ import annotations

import ast
from base64 import b64encode
from dataclasses import replace
from hashlib import sha256
import inspect
import json
from pathlib import Path

import pytest

import malleus._contract_pipeline.knowledge as knowledge_module
from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeHistory,
    KnowledgeChangeHistoryBinding,
    KnowledgeChangeRefusal,
    KnowledgeChangeRefusalReason,
    KnowledgeChangeSet,
)
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


def _anchored_history(tmp_path: Path):
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
        _anchor(history, event, retained, role)
    replay = history.replay()
    assert replay.retained_bytes("source-generic") == source_bytes
    assert replay.retained_bytes("evidence-generic") == evidence_bytes
    raw_ledger = history.path.read_bytes()
    assert b64encode(source_bytes) in raw_ledger
    assert b64encode(evidence_bytes) in raw_ledger
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
) -> tuple[bytes, ...]:
    policy = _load_policy()
    proposal_id = "proposal-generic-1"
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
            receipt_id=f"receipt-generic-{index}",
        )
        for index, ((check_id, check_identity), outcome) in enumerate(
            zip(CHECKS, outcomes, strict=True)
        )
    )
    decision = _event(
        "VERDICT_RECORDED",
        decision_id="decision-generic-1",
        proposal_id=proposal_id,
    )
    return (proposal, *checks, decision)


def _load_change(payload: dict[str, object]) -> KnowledgeChangeSet:
    return KnowledgeChangeSet.from_bytes(_canonical(payload))


def _ledger_bytes(history: KnowledgeChangeHistory) -> bytes:
    return history.path.read_bytes() if history.path.exists() else b""


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
