"""RED contract for one governed ontology revision in one knowledge history."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from malleus.compiler import (
    KnowledgeChangeHistory,
    KnowledgeChangeHistoryBinding,
    KnowledgeOperation,
    KnowledgeValidTime,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _anchor,
    _binding_payload,
    _digest,
    _protocol_events,
)
from tests.contract_compiler.pareto.test_protocol_machine import (
    _canonical,
    _effective,
    _event,
)
from tests.contract_compiler.pareto.test_validated_contract import (
    ROOT,
    _binding,
    _compile_binding,
    _trusted_types,
)


BASE_SOURCE = b"""\
id: https://example.malleus.dev/revision
name: revision
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  test: https://example.malleus.dev/revision/
imports:
  - linkml:types
  - malleus
enums:
  Stage:
    permissible_values:
      OLD:
slots:
  label:
    range: string
  stage:
    range: Stage
classes:
  LeftObject:
    is_a: Entity
    slots: [label, stage]
    slot_usage:
      label:
        required: true
      stage:
        required: true
  RightObject:
    is_a: Entity
    slots: [label]
    slot_usage:
      label:
        required: true
"""

ADD_CLASS_SOURCE = BASE_SOURCE.replace(
    b"  RightObject:\n",
    b"  ExtraObject:\n"
    b"    is_a: Entity\n"
    b"    slots: [label]\n"
    b"    slot_usage:\n"
    b"      label:\n"
    b"        required: true\n"
    b"  RightObject:\n",
)
ADD_ENUM_VALUE_SOURCE = BASE_SOURCE.replace(
    b"      OLD:\n",
    b"      OLD:\n      NEW:\n",
)
ADD_SLOT_SOURCE = BASE_SOURCE.replace(
    b"  stage:\n    range: Stage\n",
    b"  stage:\n    range: Stage\n  note:\n    range: string\n",
).replace(
    b"    slots: [label, stage]\n",
    b"    slots: [label, stage, note]\n",
)
REVISED_SOURCE = (
    ADD_CLASS_SOURCE.replace(
        b"      OLD:\n",
        b"      OLD:\n      NEW:\n",
    )
    .replace(
        b"  stage:\n    range: Stage\n",
        b"  stage:\n    range: Stage\n  note:\n    range: string\n",
    )
    .replace(
        b"    slots: [label, stage]\n",
        b"    slots: [label, stage, note]\n",
    )
)


def _revision_api():
    import malleus.compiler as compiler

    return (
        compiler.CONTRACT_REVISION_POLICY,
        compiler.ContractRevision,
        compiler.ContractRevisionRefusal,
        compiler.ContractRevisionRefusalReason,
    )


def _compile(source: bytes, *, extra_sources: dict[str, bytes] | None = None):
    sources = {
        "revision": source,
        "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
        "linkml:types": _trusted_types(),
    }
    sources.update(extra_sources or {})
    return _compile_binding(_binding(sources, "revision"))


def _history(tmp_path: Path):
    compiled = _compile(BASE_SOURCE)
    partial = _effective(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256
    )
    binding = KnowledgeChangeHistoryBinding.from_bytes(_canonical(_binding_payload()))
    history = KnowledgeChangeHistory(
        tmp_path / "revision-history.jsonl",
        partial_contract=partial,
        contract_view=compiled.view,
        binding=binding,
    )
    source = b"retained revision source\n"
    evidence = b"retained revision evidence\n"
    anchors = (
        (
            "validated-contract-artifact",
            compiled.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        (
            "contract-artifact",
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        (
            "history-binding-artifact",
            binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        ("source-artifact", source, "SOURCE_ARTIFACT"),
        ("evidence-revision", evidence, "RETAINED_EVIDENCE"),
    )
    for record_id, retained, role in anchors:
        _anchor(
            history,
            _event(
                "ARTIFACT_REGISTERED",
                artifact_id=record_id,
                artifact_identity=_digest(retained),
            ),
            retained,
            role,
        )
    _anchor(
        history,
        _event(
            "SOURCE_REGISTERED",
            artifact_id="source-artifact",
            source_id="source-revision",
            source_identity=_digest(source),
        ),
        source,
        "RETAINED_SOURCE",
    )
    return history, compiled, partial


def _admit(
    history: KnowledgeChangeHistory,
    *,
    change_set_id: str,
    operations: tuple[KnowledgeOperation, ...],
    order: str,
    supersedes: tuple[str, ...] = (),
    suffix: str,
):
    before = history.replay()
    change = history.compose_change_set(
        change_set_id=change_set_id,
        source_record_ids=("source-revision",),
        evidence_record_ids=("evidence-revision",),
        operations=operations,
        valid_time=KnowledgeValidTime("ORDER_ONLY", order),
        supersedes=supersedes,
    )
    replay = history.admit(
        change_set=change,
        machine_events=_protocol_events(
            change,
            before.machine_state.identity,
            identifier_suffix=suffix,
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    return change, replay


def _compose_revision(history: KnowledgeChangeHistory, source: bytes):
    compiled = _compile(source)
    partial = _effective(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256
    )
    revision = history.compose_contract_revision(
        revision_id="revision:1",
        target_validated_contract_bytes=compiled.artifact.artifact_bytes,
        target_partial_contract_bytes=partial.canonical_bytes,
        reason="additive fixture revision",
        issued_at="2026-09-03T00:00:00Z",
    )
    return revision, compiled, partial


def test_revision_policy_keeps_import_in_grammar_but_refuses_it() -> None:
    policy, _, _, _ = _revision_api()

    assert policy.grammar == "malleus.contract-revision-policy/private-v0"
    assert policy.change_kinds == (
        "ADD_CLASS",
        "ADD_ENUM_VALUE",
        "ADD_IMPORT",
        "ADD_SLOT",
    )
    assert policy.admitted_change_kinds == (
        "ADD_CLASS",
        "ADD_ENUM_VALUE",
        "ADD_SLOT",
    )
    assert policy.refused_change_kinds == ("ADD_IMPORT",)


@pytest.mark.parametrize(
    ("source", "expected_kind"),
    [
        (ADD_CLASS_SOURCE, "ADD_CLASS"),
        (ADD_ENUM_VALUE_SOURCE, "ADD_ENUM_VALUE"),
        (ADD_SLOT_SOURCE, "ADD_SLOT"),
    ],
)
def test_each_admitted_revision_kind_is_derived_from_compiled_facts(
    tmp_path: Path, source: bytes, expected_kind: str
) -> None:
    history, _, _ = _history(tmp_path)

    revision, _, _ = _compose_revision(history, source)

    assert {change.kind for change in revision.changes} == {expected_kind}
    assert revision.policy_identity == _revision_api()[0].identity


def test_add_import_is_typed_policy_refusal_without_a_write(tmp_path: Path) -> None:
    _, _, refusal_type, reason_type = _revision_api()
    history, _, _ = _history(tmp_path)
    before = history.path.read_bytes()
    imported = b"""\
id: https://example.malleus.dev/revision-extension
name: revision_extension
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  ImportedObject:
"""
    source = BASE_SOURCE.replace(
        b"  - malleus\n",
        b"  - malleus\n  - extension\n",
    )
    target = _compile(source, extra_sources={"extension": imported})
    target_partial = _effective(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256
    )

    with pytest.raises(refusal_type) as refusal:
        history.compose_contract_revision(
            revision_id="revision:import",
            target_validated_contract_bytes=target.artifact.artifact_bytes,
            target_partial_contract_bytes=target_partial.canonical_bytes,
            reason="new import",
            issued_at="2026-09-03T00:00:00Z",
        )

    assert refusal.value.reason is reason_type.POLICY_REFUSAL
    assert refusal.value.change_kind == "ADD_IMPORT"
    assert history.path.read_bytes() == before


def test_non_additive_contract_change_refuses_without_a_write(tmp_path: Path) -> None:
    _, _, refusal_type, reason_type = _revision_api()
    history, _, _ = _history(tmp_path)
    before = history.path.read_bytes()
    changed = BASE_SOURCE.replace(
        b"        required: true\n", b"        required: false\n", 1
    )

    with pytest.raises(refusal_type) as refusal:
        _compose_revision(history, changed)

    assert refusal.value.reason is reason_type.NON_ADDITIVE_CHANGE
    assert history.path.read_bytes() == before


def test_one_history_replays_records_across_one_contract_revision(
    tmp_path: Path,
) -> None:
    _, revision_type, _, _ = _revision_api()
    history, _, initial = _history(tmp_path)
    first, _ = _admit(
        history,
        change_set_id="change:v1",
        operations=(
            KnowledgeOperation(
                ordinal=0,
                operation_id="operation:left:v1",
                operation_type="CREATE_ENTITY",
                record_type="LeftObject",
                record_id="left:v1",
                properties={"label": "before", "stage": "OLD"},
                depends_on=(),
            ),
            KnowledgeOperation(
                ordinal=1,
                operation_id="operation:right:v1",
                operation_type="CREATE_ENTITY",
                record_type="RightObject",
                record_id="right:v1",
                properties={"label": "from v1"},
                depends_on=(),
            ),
        ),
        order="event:1",
        suffix="-v1",
    )
    revision, revised, revised_partial = _compose_revision(history, REVISED_SOURCE)

    after_revision = history.record_contract_revision(
        revision=revision,
        transaction_time="2026-09-03T00:01:00Z",
        actor_id="actor:test",
    )
    second, admitted = _admit(
        history,
        change_set_id="change:v2",
        operations=(
            KnowledgeOperation(
                ordinal=0,
                operation_id="operation:left:v2",
                operation_type="CREATE_ENTITY",
                record_type="LeftObject",
                record_id="left:v2",
                properties={"label": "after", "note": "new slot", "stage": "NEW"},
                depends_on=(),
                supersedes_record_id="left:v1",
            ),
            KnowledgeOperation(
                ordinal=1,
                operation_id="operation:extra:v2",
                operation_type="CREATE_ENTITY",
                record_type="ExtraObject",
                record_id="extra:v2",
                properties={"label": "new class"},
                depends_on=(),
            ),
        ),
        order="event:2",
        supersedes=(first.change_set_id,),
        suffix="-v2",
    )
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()

    assert isinstance(revision, revision_type)
    assert {change.kind for change in revision.changes} == {
        "ADD_CLASS",
        "ADD_ENUM_VALUE",
        "ADD_SLOT",
    }
    assert after_revision.partial_contract.identity == revised_partial.identity
    assert after_revision.contract_view.content_hash() == revised.view.content_hash()
    assert admitted.change_sets == (first, second)
    assert tuple(change.contract_identity for change in admitted.change_sets) == (
        initial.identity,
        revised_partial.identity,
    )
    assert admitted.graph.query("RightObject") == [
        {"id": "right:v1", "label": "from v1", "type": "RightObject"}
    ]
    assert admitted.graph.query("LeftObject") == [
        {
            "id": "left:v2",
            "label": "after",
            "note": "new slot",
            "stage": "NEW",
            "type": "LeftObject",
        }
    ]
    assert admitted.graph.query("ExtraObject") == [
        {"id": "extra:v2", "label": "new class", "type": "ExtraObject"}
    ]
    assert admitted.record_history["left:v1"].superseded_by == "left:v2"
    assert reopened.graph.snapshot() == admitted.graph.snapshot()
    assert reopened.record_history == admitted.record_history
    assert reopened.contract_revisions == (revision,)
    assert reopened.partial_contract.identity == revised_partial.identity


def test_revision_staleness_and_forgery_refuse_atomically(tmp_path: Path) -> None:
    _, _, refusal_type, reason_type = _revision_api()
    history, _, _ = _history(tmp_path)
    revision, _, _ = _compose_revision(history, REVISED_SOURCE)
    later = b"later evidence\n"
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
    before = history.path.read_bytes()

    with pytest.raises(refusal_type) as stale:
        history.record_contract_revision(
            revision=revision,
            transaction_time="2026-09-03T00:01:00Z",
            actor_id="actor:test",
        )
    assert stale.value.reason is reason_type.STALE_BASE
    assert history.path.read_bytes() == before

    forged = replace(revision, identity="sha256:" + "0" * 64)
    with pytest.raises(refusal_type) as mismatch:
        history.record_contract_revision(
            revision=forged,
            transaction_time="2026-09-03T00:01:00Z",
            actor_id="actor:test",
        )
    assert mismatch.value.reason is reason_type.IDENTITY_MISMATCH
    assert history.path.read_bytes() == before
