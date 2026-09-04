"""Guards for the exact post-query source-grounded review inputs."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVALUATION = ROOT / "paper-v4/evaluation-v2"
EXPERIMENT = ROOT / "paper-v4/experiment-v2"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def test_frozen_manifest_binds_only_the_precommitted_review_surface() -> None:
    manifest = json.loads((EVALUATION / "review-input-manifest.json").read_bytes())
    protocol = json.loads((EVALUATION / "review-protocol.json").read_bytes())

    assert manifest["schema"] == "malleus.paper-v4.source-grounded-review-inputs/v1"
    assert manifest["status"] == "FROZEN_FOR_REVIEW"
    assert manifest["review_protocol_sha256"] == _digest(
        EVALUATION / "review-protocol.json"
    )
    assert manifest["fixed_identities"] == protocol["fixed_identities"]
    assert set(manifest["stage_identities"]) == {
        "ledger_head",
        "query_binding_sha256",
        "query_result_sha256",
        "replay_receipt_sha256",
        "selected_ontology_sha256",
    }
    assert protocol["review_materials"] == [
        "selected_reading",
        "competency_questions",
        "query_binding",
        "query_result",
    ]


def test_every_stage_identity_resolves_to_the_frozen_result() -> None:
    manifest = json.loads((EVALUATION / "review-input-manifest.json").read_bytes())
    stage = manifest["stage_identities"]
    receipt = json.loads((EXPERIMENT / "results/replay-receipt.json").read_bytes())
    query = json.loads((EXPERIMENT / "results/query-result.json").read_bytes())

    assert stage == {
        "selected_ontology_sha256": _digest(
            EXPERIMENT / "ontology-run/ontology-02.yaml"
        ),
        "ledger_head": receipt["ledger_head"],
        "replay_receipt_sha256": _digest(
            EXPERIMENT / "results/replay-receipt.json"
        ),
        "query_binding_sha256": _digest(EXPERIMENT / "native-query-binding.json"),
        "query_result_sha256": _digest(EXPERIMENT / "results/query-result.json"),
    }
    assert query["inputs"] == {
        "ontology_sha256": stage["selected_ontology_sha256"],
        "query_binding_sha256": stage["query_binding_sha256"],
        "replay_receipt_sha256": stage["replay_receipt_sha256"],
    }


def test_review_input_set_has_no_oracle_score_or_population() -> None:
    protocol = json.loads((EVALUATION / "review-protocol.json").read_bytes())

    assert {
        "answer_oracle",
        "automated_score",
        "canonical_answer",
        "population_proposal",
        "population_provenance",
        "score_result",
    }.issubset(protocol["withheld_materials"])
    assert not (EXPERIMENT / "results/score.json").exists()
