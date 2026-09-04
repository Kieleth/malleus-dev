from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path


CONTRACT_PATH = Path(__file__).with_name("run-contract.json")
ROOT = Path(__file__).resolve().parents[2]
ACTIVE_TEST_MANIFEST = ROOT / "paper-v4" / "active-test-manifest.json"
ARXIV_README = ROOT / "paper-v4" / "arxiv" / "README.md"


def _contract() -> dict[str, object]:
    return json.loads(CONTRACT_PATH.read_bytes())


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


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
        "profile_sha256": "sha256:2317d88fd236fb63d5f4b68262619de6b5874946ab2ea8144b1b9a2995f471d5",
        "semantic_unit": "COMPOSITION",
        "origin": "PARTIAL_IMPORT",
        "composition": "ONE_ATOMIC_CAPTURE_BATCH",
        "knowledge_valid_time": "ORDER_ONLY_CAPTURE_ID",
        "assertion_and_domain_time": "OPTIONAL_PER_ASSERTION_RETAINED_EVIDENCE",
        "modality_rule": "QUERYABLE_OR_TYPED_REFUSAL",
    }


def test_execution_remains_blocked_until_core_gate_is_bound() -> None:
    contract = _contract()

    assert contract["status"] == "WAITING_FOR_CORE_GATE"
    gate = contract["core_gate"]
    assert gate["status"] == "P6_VERIFIED_P7_P8_REQUIRED"
    assert gate["verified_pieces"]["FULL_DOMAIN_HISTORY_PROFILE"] == {
        "core_commit": "573c45b82725d6f444b70e5ff193302dac883e7b",
        "core_tree": "6704031dea824572b4d7163ba477c33175397fe7",
        "profile_id": "source-assertion",
        "profile_sha256": "sha256:2317d88fd236fb63d5f4b68262619de6b5874946ab2ea8144b1b9a2995f471d5",
        "paper_audit": "PASS",
    }


def test_active_gate_cannot_collect_superseded_or_retired_experiments() -> None:
    manifest = json.loads(ACTIVE_TEST_MANIFEST.read_bytes())

    assert manifest["schema"] == "malleus.paper-v4.active-test-manifest/v1"
    assert manifest["python"] == "CPYTHON_3_12_LOCKED"
    assert manifest["pythonpath"] == [".", "src"]
    assert manifest["pytest_args"] == ["--import-mode=importlib", "-q"]
    assert set(manifest["excluded_roots"]) == {
        "paper-v4/experiment",
        "paper-v4/retired",
    }
    assert "paper-v4/experiment-v4" in manifest["paths"]

    excluded = [(ROOT / value).resolve() for value in manifest["excluded_roots"]]
    for value in manifest["paths"]:
        candidate = (ROOT / value).resolve()
        assert candidate.exists()
        assert candidate == ROOT or ROOT in candidate.parents
        assert all(
            candidate != root and root not in candidate.parents for root in excluded
        )


def test_v4_questions_and_human_review_are_frozen_but_producer_blind() -> None:
    evaluation = _contract()["evaluation"]
    question_binding = evaluation["competency_questions"]
    protocol_binding = evaluation["review_protocol"]
    question_path = ROOT / question_binding["path"]
    protocol_path = ROOT / protocol_binding["path"]
    questions = json.loads(question_path.read_bytes())
    protocol = json.loads(protocol_path.read_bytes())

    assert question_binding["producer_visibility"] == "WITHHELD"
    assert questions["visibility"] == "WITHHELD_FROM_PRODUCER_UNTIL_POST_REPLAY"
    assert question_binding["sha256"] == _digest(question_path)
    assert protocol_binding["sha256"] == _digest(protocol_path)
    assert protocol["fixed_identities"]["competency_questions_sha256"] == _digest(
        question_path
    )
    assert protocol["question_ids"] == [
        question["id"] for question in questions["questions"]
    ]
    assert protocol["authorship"]["ratifier_actor_id"] == "actor:luis"
    assert "numeric_score" in protocol["forbidden_record_fields"]


def test_publication_instructions_do_not_name_an_ephemeral_host_environment() -> None:
    instructions = ARXIV_README.read_text(encoding="utf-8")

    assert "/private/tmp" not in instructions
    assert (
        '"$malleus_paper_env/bin/python" paper-v4/run_active_tests.py' in instructions
    )
