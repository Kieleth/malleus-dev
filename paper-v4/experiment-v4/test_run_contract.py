from __future__ import annotations

import json
from pathlib import Path


CONTRACT_PATH = Path(__file__).with_name("run-contract.json")


def _contract() -> dict[str, object]:
    return json.loads(CONTRACT_PATH.read_bytes())


def test_v4_is_one_kiss_loop_with_no_fallback() -> None:
    contract = _contract()

    assert contract["scope"] == {
        "documents": 1,
        "producer_loops": 1,
        "staged_session_variant": False,
        "new_multi_producer_matrix": False,
    }
    assert contract["producer"]["fallback"] == "FORBIDDEN"
    assert contract["producer"]["max_ontology_revision_rounds"] == 2


def test_questions_and_answers_cannot_condition_construction() -> None:
    contract = _contract()
    producer = contract["producer"]

    assert "COMPETENCY_QUESTIONS" not in producer["inputs"]
    assert "QUERY_BINDING" not in producer["inputs"]
    assert "ANSWER_ORACLE" not in producer["inputs"]
    assert contract["population"]["questions_visible"] is False
    assert contract["evaluation"]["questions_enter_at"] == ("POST_REPLAY_QUERY_BINDING")


def test_query_is_post_replay_and_outside_accepted_state() -> None:
    query = _contract()["query"]

    assert query["binding_time"] == "AFTER_POPULATION_AND_REPLAY_FREEZE"
    assert query["execution_state"] == "REPLAY_DERIVED_GRAPH_ONLY"
    assert query["source_reads"] == "FORBIDDEN"
    assert query["network"] == "FORBIDDEN"
    assert query["embedding_index"] == "FORBIDDEN"
    assert query["knowledge_state_identity"] == "EXCLUDED"


def test_source_assertion_profile_preserves_modality_or_refuses() -> None:
    history = _contract()["history"]

    assert history == {
        "profile_id": "source-assertion",
        "semantic_unit": "ASSERTION",
        "origin": "PARTIAL_IMPORT",
        "modality_rule": "QUERYABLE_OR_TYPED_REFUSAL",
    }


def test_execution_remains_blocked_until_core_gate_is_bound() -> None:
    contract = _contract()

    assert contract["status"] == "WAITING_FOR_CORE_GATE"
    assert contract["core_gate"]["status"] == "REQUIRED_UNBOUND"
