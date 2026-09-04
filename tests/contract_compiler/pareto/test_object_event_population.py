"""P9 RED contract for governed object-event population."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from malleus import KnowledgeGraph, OpStatus, ProposedOperation, stage_subgraph
from malleus import compiler as api
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    TRANSACTION_TIME,
    _anchor,
    _binding_payload,
    _event,
    _protocol_events,
)
from tests.contract_compiler.pareto.test_protocol_machine import (
    _canonical,
    _effective,
)
from tests.contract_compiler.pareto.test_validated_contract import (
    ROOT,
    _trusted_types,
)


OBJECT_EVENT_ONTOLOGY = ROOT / "ontology/profiles/object-event.yaml"


PROJECT_SOURCE = b"""\
id: https://example.malleus.dev/object-event-test
name: object_event_test
version: 0.1.0
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  object_event: https://malleus.dev/schema/profiles/object-event/
  test: https://example.malleus.dev/object-event-test/
imports:
  - linkml:types
  - object-event
enums:
  TestEventKind:
    permissible_values:
      PACK:
  TestParticipationQualifier:
    permissible_values:
      ITEM:
slots:
  label:
    range: string
classes:
  TestObject:
    is_a: Entity
    slots:
      - label
    slot_usage:
      label:
        required: true
  TestEvent:
    is_a: Event
    slot_usage:
      event_type:
        range: TestEventKind
        required: true
        equals_string: PACK
      occurred_at:
        required: true
  TestParticipation:
    is_a: EventParticipation
    slot_usage:
      qualifier:
        range: TestParticipationQualifier
        required: true
        equals_string: ITEM
"""


SOURCE_BYTES = b"event e1 packed object o1 at 2026-09-04T00:00:00Z\n"


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _compiled():
    return api.compile_linkml_contract(
        root_locator="project",
        sources={
            "project": PROJECT_SOURCE,
            "object-event": OBJECT_EVENT_ONTOLOGY.read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": _trusted_types(),
        },
    )


def _plan(contract_identity: str) -> dict[str, object]:
    return {
        "adapter": {"adapter_id": "test-object-event", "version": "1"},
        "contract_identity": contract_identity,
        "derivations": [
            {
                "locator": "object",
                "path": ["properties", "label"],
                "record_id": "o1",
                "source_id": "source:test-object-event",
            },
            {
                "locator": "activity",
                "path": ["properties", "event_type"],
                "record_id": "e1",
                "source_id": "source:test-object-event",
            },
            {
                "locator": "time",
                "path": ["properties", "occurred_at"],
                "record_id": "e1",
                "source_id": "source:test-object-event",
            },
            *(
                {
                    "locator": locator,
                    "path": ["properties", field],
                    "record_id": "participation:e1:o1:item",
                    "source_id": "source:test-object-event",
                }
                for field, locator in (
                    ("event_id", "event"),
                    ("entity_id", "object"),
                    ("qualifier", "role"),
                )
            ),
        ],
        "evidence": [],
        "gaps": [],
        "grammar": "malleus.population-plan/private-v0",
        "history_profile": {
            "profile_id": "object-event",
            "sha256": api.OBJECT_EVENT_PROFILE.identity,
        },
        "plan_id": "plan:test-object-event",
        "records": {
            "entities": [
                {"id": "o1", "properties": {"label": "Object 1"}, "type": "TestObject"}
            ],
            "event_participations": [
                {
                    "id": "participation:e1:o1:item",
                    "properties": {
                        "entity_id": "o1",
                        "event_id": "e1",
                        "qualifier": "ITEM",
                    },
                    "type": "TestParticipation",
                }
            ],
            "events": [
                {
                    "id": "e1",
                    "properties": {
                        "event_type": "PACK",
                        "occurred_at": "2026-09-04T00:00:00Z",
                    },
                    "type": "TestEvent",
                }
            ],
            "relations": [],
            "signals": [],
        },
        "sources": [
            {"sha256": _digest(SOURCE_BYTES), "source_id": "source:test-object-event"}
        ],
        "supersessions": [],
        "valid_time": {"kind": "INSTANT", "value": "2026-09-04T00:00:00Z"},
    }


def _history(tmp_path: Path, compiled):
    partial = _effective(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256
    )
    binding = api.KnowledgeChangeHistoryBinding.from_bytes(
        _canonical(_binding_payload())
    )
    history = api.KnowledgeChangeHistory(
        tmp_path / "object-event-history.jsonl",
        partial_contract=partial,
        contract_view=compiled.view,
        binding=binding,
    )
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
                artifact_identity=_digest(partial.canonical_bytes),
            ),
            partial.canonical_bytes,
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
                artifact_identity=_digest(SOURCE_BYTES),
            ),
            SOURCE_BYTES,
            "SOURCE_ARTIFACT",
        ),
        (
            _event(
                "SOURCE_REGISTERED",
                artifact_id="source-artifact",
                source_id="source:test-object-event",
                source_identity=_digest(SOURCE_BYTES),
            ),
            SOURCE_BYTES,
            "RETAINED_SOURCE",
        ),
    )
    for event, content, role in anchors:
        _anchor(history, event, content, role)
    return history, partial


def _retention_events(plan: dict[str, object]) -> dict[str, bytes]:
    plan_bytes = _canonical(plan)
    return {
        "profile:object-event": _event(
            "ARTIFACT_REGISTERED",
            artifact_id="profile:object-event",
            artifact_identity=api.OBJECT_EVENT_PROFILE.identity,
        ),
        "plan:test-object-event": _event(
            "ARTIFACT_REGISTERED",
            artifact_id="plan:test-object-event",
            artifact_identity=_digest(plan_bytes),
        ),
    }


def test_object_event_population_admits_reopens_replays_and_queries(
    tmp_path: Path,
) -> None:
    compiled = _compiled()
    history, partial = _history(tmp_path, compiled)
    plan = _plan(partial.identity)

    prepared = api.prepare_population_change(
        history=history,
        plan=plan,
        profile=api.OBJECT_EVENT_PROFILE,
        retention_events=_retention_events(plan),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )

    assert prepared.change_set is not None
    assert [
        operation.operation_type for operation in prepared.change_set.operations
    ] == [
        "CREATE_ENTITY",
        "CREATE_EVENT",
        "CREATE_EVENT_PARTICIPATION",
    ]
    assert prepared.change_set.operations[2].depends_on == (
        "operation:plan:test-object-event:0",
        "operation:plan:test-object-event:1",
    )

    admitted = history.admit(
        change_set=prepared.change_set,
        machine_events=_protocol_events(
            prepared.change_set,
            prepared.retention_replay.machine_state.identity,
            identifier_suffix="-object-event",
        ),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    reopened = api.KnowledgeChangeHistory.reopen(history.path).replay()

    assert reopened.receipt == admitted.receipt
    assert reopened.graph.query(entity_type="TestEvent") == [
        {
            "event_type": "PACK",
            "id": "e1",
            "is_event": True,
            "occurred_at": "2026-09-04T00:00:00Z",
            "type": "TestEvent",
        }
    ]
    assert reopened.graph.query_event_participations(event_id="e1") == [
        {
            "entity_id": "o1",
            "event_id": "e1",
            "id": "participation:e1:o1:item",
            "qualifier": "ITEM",
            "type": "TestParticipation",
        }
    ]
    assert reopened.graph.query_relations() == []
    assert reopened.graph.get_relation("participation:e1:o1:item") is None


def test_event_participation_is_staged_without_widening_relation_endpoints() -> None:
    compiled = _compiled()
    graph = KnowledgeGraph(compiled.view)
    candidate = stage_subgraph(
        graph,
        (
            ProposedOperation.entity("TestObject", "o1", {"label": "Object 1"}),
            ProposedOperation.event(
                "TestEvent",
                "e1",
                {
                    "event_type": "PACK",
                    "occurred_at": "2026-09-04T00:00:00Z",
                },
            ),
            ProposedOperation.event_participation(
                "TestParticipation",
                "participation:e1:o1:item",
                {"entity_id": "o1", "event_id": "e1", "qualifier": "ITEM"},
            ),
        ),
    )

    assert candidate.valid
    candidate.materialize_into(graph)
    invalid_relation = graph.create_relation(
        "TestParticipation",
        "not-a-relation",
        "e1",
        "o1",
        {"qualifier": "ITEM"},
    )

    assert invalid_relation.op_status is OpStatus.REJECTED
    assert "not a Relation subtype" in (invalid_relation.rejection_reason or "")
    assert graph.query_event_participations(entity_id="o1", qualifier="ITEM")


def test_event_participation_refuses_wrong_endpoint_kinds_atomically() -> None:
    compiled = _compiled()
    graph = KnowledgeGraph(compiled.view)
    graph.create_entity("TestObject", "o1", {"label": "Object 1"})
    graph.create_event(
        "TestEvent",
        "e1",
        {"event_type": "PACK", "occurred_at": "2026-09-04T00:00:00Z"},
    )
    before = graph.snapshot()

    wrong_event = graph.create_event_participation(
        "TestParticipation",
        "participation:o1:o1:item",
        {"entity_id": "o1", "event_id": "o1", "qualifier": "ITEM"},
    )
    wrong_entity = graph.create_event_participation(
        "TestParticipation",
        "participation:e1:e1:item",
        {"entity_id": "e1", "event_id": "e1", "qualifier": "ITEM"},
    )

    assert wrong_event.op_status is OpStatus.REJECTED
    assert "Event 'o1' is not an Event" in (wrong_event.rejection_reason or "")
    assert wrong_entity.op_status is OpStatus.REJECTED
    assert "Entity 'e1' is not an Entity" in (wrong_entity.rejection_reason or "")
    assert graph.snapshot() == before
