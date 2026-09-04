from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
import subprocess


CONTRACT_PATH = Path(__file__).with_name("run-contract.json")
ROOT = Path(__file__).resolve().parents[2]
ACTIVE_TEST_MANIFEST = ROOT / "paper-v4" / "active-test-manifest.json"
ARXIV_README = ROOT / "paper-v4" / "arxiv" / "README.md"
MASTER_PLAN = ROOT / "paper-v4" / "paper-master-plan.md"
PRODUCER_MANIFEST = ROOT / "paper-v4" / "experiment-v4" / "producer-input-manifest.json"
SPAWN_MESSAGE = ROOT / "paper-v4" / "experiment-v4" / "spawn-message.md"
ONTOLOGY_RESULT = ROOT / "paper-v4" / "experiment-v4" / "ontology-run" / "result.json"


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
        "modality_rule": "REPLAY_RECORD_TO_RETAINED_ASSERTION_TRACE_REQUIRED",
    }


def test_execution_is_bound_to_the_frozen_core_gate() -> None:
    contract = _contract()

    assert contract["status"] == "READY_FOR_PRODUCER"
    gate = contract["core_gate"]
    assert gate["status"] == "P6_P7_P8_VERIFIED"
    assert gate["execution_baseline"] == {
        "core_commit": "6488ddbfc599e8899d269f8794810f352a5d1fe0",
        "core_tree": "6fc5e585e5058e7376ea1aef96fcb49b59107e5e",
        "paper_merge_commit": "f8d96123f86b2af41d9c67353f952d56565cf6af",
        "paper_merge_tree": "c22387313a16b228f0e9c04e88651f42d0ce5bad",
    }
    assert gate["verified_pieces"]["FULL_DOMAIN_HISTORY_PROFILE"] == {
        "core_commit": "573c45b82725d6f444b70e5ff193302dac883e7b",
        "core_tree": "6704031dea824572b4d7163ba477c33175397fe7",
        "profile_id": "source-assertion",
        "profile_sha256": "sha256:2317d88fd236fb63d5f4b68262619de6b5874946ab2ea8144b1b9a2995f471d5",
        "paper_audit": "PASS",
    }
    assert gate["verified_pieces"]["GROUNDED_PACKS_AND_PACK_GROUNDING"] == {
        "core_commit": "465924f3e6b0dee64aafeecaeb68cb5e8beb6b41",
        "core_tree": "5281da97f17905da45e254fd044536cb67d3398e",
        "governance_head": (
            "sha256:ac089e6ecd26c43248f9a32d3a0ee4c089f7f424c30b7f8d7cd85295e34653dc"
        ),
        "grounding_rite_sha256": (
            "sha256:452d7b29ed541db6bb881eae025ea156cce07d6c7f4ec615d8f314f69aba6709"
        ),
        "pack_sha256": {
            "chronology": (
                "sha256:6fbd3b49b32f698d8a9f31dcff770660153d822478a3007d0b8018c2af4439b1"
            ),
            "metrology": (
                "sha256:1050b24720f5e7df10dbf6096d8487b46490099b8066c2048a59ef0fa85fc586"
            ),
            "research": (
                "sha256:c86abede14242c3179d45807ae6461bf8725ed64256971875d9291a85b7c280e"
            ),
        },
        "paper_audit": "PASS",
    }
    assert gate["verified_pieces"]["NASCENT_PROJECT_PLAYBOOK"] == {
        "core_commit": "6488ddbfc599e8899d269f8794810f352a5d1fe0",
        "core_tree": "6fc5e585e5058e7376ea1aef96fcb49b59107e5e",
        "governance_head": (
            "sha256:2410138e81e343e8a1044ffdc58801db1311ed4419aa3b3c89ce1d50693ac8b8"
        ),
        "skill_path": ".claude/skills/malleus-acolyte/SKILL.md",
        "skill_sha256": (
            "sha256:ab0279f7b1bda382e45e490f19580805a150dc9159e5912269f9a38350e3fcc8"
        ),
        "paper_audit": "PASS",
    }


def test_active_gate_cannot_collect_superseded_or_retired_experiments() -> None:
    manifest = json.loads(ACTIVE_TEST_MANIFEST.read_bytes())

    assert manifest["schema"] == "malleus.paper-v4.active-test-manifest/v1"
    assert manifest["python"] == "CPYTHON_3_12_LOCKED"
    assert manifest["pythonpath"] == [".", "src"]
    assert manifest["pytest_args"] == ["--import-mode=importlib", "-q"]
    assert set(manifest["excluded_roots"]) == {
        "research/ontology_driven_kg_realization/experiments/document_paper",
        "paper-v4/experiment",
        "paper-v4/experiment-v2",
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


def test_active_gate_does_not_reinterpret_frozen_runs_under_p8_core() -> None:
    manifest = json.loads(ACTIVE_TEST_MANIFEST.read_bytes())

    assert "paper-v4/experiment-v2" not in manifest["paths"]
    assert (
        "research/ontology_driven_kg_realization/experiments/document_paper"
        not in manifest["paths"]
    )
    assert "paper-v4/experiment-v4" in manifest["paths"]


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


def test_producer_input_set_is_exact_and_question_blind() -> None:
    manifest = json.loads(PRODUCER_MANIFEST.read_bytes())
    declared = {item["name"]: item for item in manifest["declared_inputs"]}

    assert manifest["status"] == "FROZEN"
    assert manifest["core"] == {
        "commit": "6488ddbfc599e8899d269f8794810f352a5d1fe0",
        "tree": "6fc5e585e5058e7376ea1aef96fcb49b59107e5e",
    }
    assert set(declared) == {
        "MALLEUS_NASCENT_PROJECT_SKILL",
        "SELECTED_READING",
        "MALLEUS_ROOT",
        "LINKML_TYPES",
        "METROLOGY_PACK",
        "CHRONOLOGY_PACK",
        "RESEARCH_PACK",
        "SOURCE_ASSERTION_PROFILE",
    }
    assert (
        declared["SELECTED_READING"]["sha256"]
        == _contract()["source"]["selected_reading_sha256"]
    )
    # Run-01 is frozen at its recorded paper merge commit (which carries Core
    # 6488ddb); its inputs are the bytes at that commit, not the live working
    # tree, which has moved since.
    frozen_commit = _contract()["core_gate"]["execution_baseline"]["paper_merge_commit"]
    for item in declared.values():
        if item["name"] == "SELECTED_READING":
            continue
        frozen = subprocess.run(
            ["git", "show", f"{frozen_commit}:{item['source']}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        assert item["sha256"] == "sha256:" + sha256(frozen).hexdigest()
    assert manifest["session"] == {
        "fresh": True,
        "single_session": True,
        "delegation": "FORBIDDEN",
        "max_compiler_diagnostic_returns": 2,
        "max_additive_revision_rounds": 2,
        "fallback": "FORBIDDEN",
    }


def test_producer_message_stages_one_closed_no_fallback_session() -> None:
    message = SPAWN_MESSAGE.read_text(encoding="utf-8")
    plain = " ".join(message.split())

    required = {
        "Start with no inherited task context",
        "read only the eight declared inputs",
        "Do not use the network or delegate",
        "Set status to `ONTOLOGY_READY` and stop",
        "at most twice",
        "phase two in this same session",
        "one `work/document-population.json`",
        "A partial or refused result is valid and triggers no fallback",
    }
    for phrase in required:
        assert phrase in plain
    forbidden = {
        "Which observation network",
        "RC2",
        "CO2 range",
        "preferred causal mechanism",
        "expected answer",
    }
    for phrase in forbidden:
        assert phrase not in message


def test_refused_ontology_run_stops_at_the_frozen_diagnostic_budget() -> None:
    contract = _contract()
    result = json.loads(ONTOLOGY_RESULT.read_bytes())
    attempts = result["attempts"]

    assert result["status"] == "REFUSED_AFTER_DIAGNOSTIC_BUDGET"
    assert result["core"] == {
        "commit": contract["core_gate"]["execution_baseline"]["core_commit"],
        "tree": contract["core_gate"]["execution_baseline"]["core_tree"],
    }
    assert (
        result["producer"]["diagnostic_returns"]
        == (contract["producer"]["max_compiler_diagnostic_returns"])
    )
    assert len(attempts) == result["producer"]["diagnostic_returns"] + 1
    assert [item["attempt"] for item in attempts] == [1, 2, 3]
    assert result["producer"]["questions_visible"] is False
    assert result["producer"]["fallback_used"] is False
    assert result["producer"]["hand_repair_used"] is False
    assert result["accepted_ontology_sha256"] is None
    assert result["population_started"] is False
    for item in attempts:
        diagnostic_path = ROOT / item["diagnostic_path"]
        diagnostic = json.loads(diagnostic_path.read_bytes())
        assert item["diagnostic_sha256"] == _digest(diagnostic_path)
        assert diagnostic["attempt"] == item["attempt"]
        assert diagnostic["ontology_sha256"] == item["ontology_sha256"]
        assert diagnostic["reason"] == "DIRECT_ROOT_GROUNDING_REQUIRED"


def test_publication_instructions_do_not_name_an_ephemeral_host_environment() -> None:
    instructions = ARXIV_README.read_text(encoding="utf-8")

    assert "/private/tmp" not in instructions
    assert (
        '"$malleus_paper_env/bin/python" paper-v4/run_active_tests.py' in instructions
    )


def test_master_plan_describes_only_the_active_v4_execution_boundary() -> None:
    plan = MASTER_PLAN.read_text(encoding="utf-8")
    plain = " ".join(plan.split())

    stale_active_claims = {
        "A separate fresh model later proposes",
        "with those questions visible",
        "fixed after ontology compilation and before population",
        "A **query** is a deterministic graph read fixed before population",
        "GraphRecipe lowering, document validation, queries, and the experiment runner remain paper-local",
    }
    for claim in stale_active_claims:
        assert claim not in plain

    required_v4_claims = {
        "one fresh single-session producer loop",
        "withheld until replay",
        "bound only after replay",
        "one atomic capture batch",
        "trace_population_record",
    }
    for claim in required_v4_claims:
        assert claim in plain
