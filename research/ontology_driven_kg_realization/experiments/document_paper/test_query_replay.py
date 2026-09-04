"""Focused tests for source-free replay-receipt queries."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import socket
from typing import Any, Callable

import pytest

from malleus.kg import KnowledgeGraph, OpStatus
from malleus.ledger import canonical_json, content_digest
from malleus.ontology import OntologyRegistry
from research.ontology_driven_kg_realization.experiments.document_paper import (
    query_replay as subject,
)
from research.ontology_driven_kg_realization.experiments.document_paper.query_replay import (
    QueryReplayRefusal,
    run_query_replay,
    write_query_result,
)


ROOT = Path(__file__).resolve().parents[4]
MALLEUS = ROOT / "paper-v4/experiment/ontology-run/inputs/malleus.yaml"


def _canonical(value: object) -> bytes:
    return canonical_json(value).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _domain_source() -> bytes:
    return b"""id: https://fiction.invalid/source-free-query
name: fictional_source_free_query
version: 1.0.0
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  fictional: https://fiction.invalid/source-free-query/
imports:
  - linkml:types
  - malleus
enums:
  FictionalRelationType:
    permissible_values:
      MEMBER_OF:
classes:
  FictionalPerson:
    is_a: Entity
    slots: [name]
    slot_usage:
      name: {required: true}
  FictionalGroup:
    is_a: Entity
    slots: [name]
    slot_usage:
      name: {required: true}
  FictionalMembership:
    is_a: Relation
    slot_usage:
      relation_type: {range: FictionalRelationType, required: true, equals_string: MEMBER_OF}
      source_id: {range: FictionalPerson, required: true}
      target_id: {range: FictionalGroup, required: true}
"""


def _binding_source() -> bytes:
    case = {
        "ordinal": 1,
        "source_record_type": "FictionalPerson",
        "relation_record_type": "FictionalMembership",
        "relation_type": {
            "enum": "FictionalRelationType",
            "value": "MEMBER_OF",
        },
        "target_record_type": "FictionalGroup",
        "output_fields": {
            "source": ["name"],
            "relation": ["relation_type"],
            "target": ["name"],
        },
    }
    return _canonical(
        {
            "schema": "malleus.paper-v4.native-query-binding/v1",
            "status": "FROZEN_BEFORE_POPULATION",
            "queries": [
                {
                    "id": f"NQ-CQ-0{index}",
                    "question_id": f"CQ-0{index}",
                    "cases": [case],
                }
                for index in range(1, 5)
            ],
        }
    )


@pytest.fixture
def inputs(tmp_path: Path) -> dict[str, Any]:
    ontology = tmp_path / "ontology.yaml"
    ontology.write_bytes(_domain_source())
    registry = OntologyRegistry(ontology, import_map={"malleus": MALLEUS})
    graph = KnowledgeGraph(registry)
    for operation in (
        graph.create_entity(
            "FictionalPerson", "fiction:person:one", {"name": "Person One"}
        ),
        graph.create_entity(
            "FictionalGroup", "fiction:group:one", {"name": "Group One"}
        ),
        graph.create_relation(
            "FictionalMembership",
            "fiction:membership:one",
            "fiction:person:one",
            "fiction:group:one",
            {"relation_type": "MEMBER_OF"},
        ),
    ):
        assert operation.op_status is OpStatus.COMMITTED, operation.rejection_reason
    return {
        "ontology_path": ontology,
        "ontology_source": ontology.read_bytes(),
        "malleus_path": MALLEUS,
        "malleus_source": MALLEUS.read_bytes(),
        "binding_source": _binding_source(),
        "graph": graph,
    }


def _receipt(
    graph: KnowledgeGraph,
    *,
    validated_fact_set_sha256: str | None = None,
) -> bytes:
    snapshot = graph.snapshot()
    contract_hash = validated_fact_set_sha256 or snapshot["ontology_hash"]
    digest_snapshot = dict(snapshot)
    digest_snapshot["ontology_hash"] = contract_hash
    return _canonical(
        {
            "graph_state_digest": content_digest(digest_snapshot),
            "queries": {
                "entities": snapshot["nodes"],
                "relations": snapshot["relations"],
            },
            "validated_fact_set_sha256": contract_hash,
        }
    )


def _run(inputs: dict[str, Any], receipt: bytes) -> dict[str, Any]:
    return json.loads(
        run_query_replay(
            receipt,
            inputs["binding_source"],
            ontology_path=inputs["ontology_path"],
            ontology_source=inputs["ontology_source"],
            malleus_path=inputs["malleus_path"],
            malleus_source=inputs["malleus_source"],
        )
    )


def test_rehydrated_queries_change_only_with_fictional_graph(inputs) -> None:
    graph = inputs["graph"]
    receipt = _receipt(graph)
    first = _run(inputs, receipt)
    assert first["inputs"] == {
        "ontology_sha256": _digest(inputs["ontology_source"]),
        "query_binding_sha256": _digest(inputs["binding_source"]),
        "replay_receipt_sha256": _digest(receipt),
    }
    assert first["graph_state_digest"] == graph.state_digest()
    assert first["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert [len(query["rows"]) for query in first["queries"]] == [1, 1, 1, 1]

    for operation in (
        graph.create_entity(
            "FictionalPerson", "fiction:person:two", {"name": "Person Two"}
        ),
        graph.create_relation(
            "FictionalMembership",
            "fiction:membership:two",
            "fiction:person:two",
            "fiction:group:one",
            {"relation_type": "MEMBER_OF"},
        ),
    ):
        assert operation.op_status is OpStatus.COMMITTED, operation.rejection_reason
    second = _run(inputs, _receipt(graph))
    assert [len(query["rows"]) for query in second["queries"]] == [2, 2, 2, 2]
    assert first["queries"] != second["queries"]


def test_state_digest_drift_refuses_before_query(inputs) -> None:
    receipt = json.loads(_receipt(inputs["graph"]))
    receipt["graph_state_digest"] = "sha256:" + "0" * 64
    with pytest.raises(
        QueryReplayRefusal, match="digest differs after typed rehydration"
    ):
        _run(inputs, _canonical(receipt))


def test_receipt_contract_hash_reproduces_contract_view_graph_identity(inputs) -> None:
    contract_hash = "sha256:" + "a" * 64
    receipt = _receipt(
        inputs["graph"],
        validated_fact_set_sha256=contract_hash,
    )

    result = _run(inputs, receipt)

    expected = json.loads(receipt)["graph_state_digest"]
    assert contract_hash != inputs["graph"].snapshot()["ontology_hash"]
    assert result["graph_state_digest"] == expected


@pytest.mark.parametrize(
    ("mutation", "message"),
    (
        ("missing", "validated_fact_set_sha256 is required"),
        ("malformed", "must be a lowercase sha256 digest"),
    ),
)
def test_receipt_requires_exact_validated_fact_set_identity(
    inputs,
    mutation: str,
    message: str,
) -> None:
    receipt = json.loads(_receipt(inputs["graph"]))
    if mutation == "missing":
        del receipt["validated_fact_set_sha256"]
    else:
        receipt["validated_fact_set_sha256"] = "sha256:not-a-digest"

    with pytest.raises(QueryReplayRefusal, match=message):
        _run(inputs, _canonical(receipt))


def _read_attempt(*args: Any, **kwargs: Any) -> None:
    Path("forbidden.txt").read_bytes()


def _network_attempt(*args: Any, **kwargs: Any) -> None:
    socket.socket()


def _embedding_attempt(*args: Any, **kwargs: Any) -> None:
    __import__("sentence_transformers")


@pytest.mark.parametrize(
    ("attempt", "category"),
    [
        (_read_attempt, "file_read"),
        (_network_attempt, "network"),
        (_embedding_attempt, "embedding_import"),
    ],
)
def test_forbidden_query_access_is_counted_and_blocked(
    inputs,
    monkeypatch: pytest.MonkeyPatch,
    attempt: Callable[..., None],
    category: str,
) -> None:
    monkeypatch.setattr(subject, "run_frozen_queries", attempt)
    with pytest.raises(QueryReplayRefusal, match=f"forbidden {category}") as refusal:
        _run(inputs, _receipt(inputs["graph"]))
    assert refusal.value.attempts[category] == 1


def test_result_writer_never_overwrites(tmp_path: Path) -> None:
    output = tmp_path / "result.json"
    write_query_result(output, b"first")
    with pytest.raises(QueryReplayRefusal, match="already exists"):
        write_query_result(output, b"second")
    assert output.read_bytes() == b"first"
