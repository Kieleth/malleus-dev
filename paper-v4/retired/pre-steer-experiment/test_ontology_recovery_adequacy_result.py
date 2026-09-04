from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "paper-v4" / "experiment"
PRIVATE = ROOT / "private" / "paper-v4-evaluation"


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_bytes())


def test_one_shot_recovery_review_is_exact_valid_and_selected() -> None:
    precommit = (EXPERIMENT / "ontology-recovery-review-precommit.json").read_bytes()
    raw = (PRIVATE / "ontology-recovery-adequacy-review-raw.txt").read_bytes()
    result_bytes = (PRIVATE / "ontology-recovery-adequacy-result.json").read_bytes()
    result = json.loads(result_bytes)
    receipt = _load(EXPERIMENT / "ontology-recovery-adequacy-receipt.json")
    schema = _load(EXPERIMENT / "ontology-recovery-review-output-schema.json")

    assert _digest(precommit) == receipt["review_precommit"]["sha256"]
    assert _digest(raw) == receipt["capture"]["retained_raw_sha256"]
    assert len(raw) == receipt["capture"]["retained_raw_byte_length"]
    assert raw.endswith(b"\n")
    assert _digest(raw[:-1]) == receipt["capture"]["provider_output_sha256"]
    assert len(raw[:-1]) == receipt["capture"]["provider_output_byte_length"]
    assert _digest(result_bytes) == receipt["capture"]["result_sha256"]
    assert len(result_bytes) == receipt["capture"]["result_byte_length"]
    assert raw == (
        b"BEGIN_RECOVERY_ADEQUACY_JSON\n"
        + result_bytes.rstrip(b"\n")
        + b"\nEND_RECOVERY_ADEQUACY_JSON\n"
    )
    Draft202012Validator(schema).validate(result)

    assert result["status"] == receipt["status"] == "SELECTED_CONTROL"
    assert result["eligibility"]["verdict"] == receipt["eligibility"] == "PASS"
    assert result["candidate_sha256"] == receipt["candidate_sha256"]
    assert result["compiled_contract_identity"] == receipt["compiled_contract_identity"]
    assert {item["id"]: item["verdict"] for item in result["criteria"]} == (
        receipt["criteria"]
    )
    assert len(result["criteria"]) == len({item["id"] for item in result["criteria"]})
    assert set(receipt["criteria"]) == {
        "OA-01",
        "OA-02",
        "OA-03",
        "OA-04",
        "OA-05",
        "OA-06",
    }
    assert set(receipt["criteria"].values()) == {"PASS"}
    assert result["unresolved_count"] == receipt["unresolved_count"] == 0
    assert len(result["witness"]) == receipt["witness_count"] == 39
    assert sum(item["judgment"] == "FAIL" for item in result["witness"]) == 0
    assert sum(item["support"] != "SUPPORTED" for item in result["witness"]) == 0
    assert receipt["population_authorization"] == "AUTHORIZED_POST_PRIMARY_CONTROL"
    assert receipt["selected_ontology_sha256"] == result["candidate_sha256"]


def test_recovery_selection_does_not_rewrite_primary_refusal() -> None:
    primary_receipt = _load(EXPERIMENT / "ontology-adequacy-receipt.json")
    recovery_receipt = _load(EXPERIMENT / "ontology-recovery-adequacy-receipt.json")

    assert primary_receipt["status"] == "REFUSED_ADEQUACY"
    assert primary_receipt["population_authorization"] == "DENIED"
    assert primary_receipt["selected_ontology_sha256"] is None
    assert recovery_receipt["classification"] == "POST_PRIMARY_CONTROL"
    assert recovery_receipt["primary_result_changed"] is False
    assert recovery_receipt["primary_result"] == primary_receipt["status"]


def test_every_recovery_review_locator_is_in_the_frozen_question_binding() -> None:
    result = _load(PRIVATE / "ontology-recovery-adequacy-result.json")
    locator = _load(PRIVATE / "oracle-locator-binding.json")
    allowed = {
        binding["question_id"]: {
            (block["id"], block["sha256"]) for block in binding["blocks"]
        }
        for binding in locator["bindings"]
    }
    assert {item["question_id"] for item in result["witness"]} == set(allowed)
    for witness in result["witness"]:
        observed = {
            (block["id"], block["sha256"]) for block in witness["supporting_blocks"]
        }
        assert observed
        assert observed <= allowed[witness["question_id"]]
