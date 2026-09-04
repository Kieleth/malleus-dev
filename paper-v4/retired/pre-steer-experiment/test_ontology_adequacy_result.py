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


def test_one_shot_review_result_is_exact_valid_and_refused() -> None:
    precommit = (EXPERIMENT / "ontology-review-precommit.json").read_bytes()
    raw = (PRIVATE / "ontology-adequacy-review-raw.txt").read_bytes()
    result_bytes = (PRIVATE / "ontology-adequacy-result.json").read_bytes()
    result = json.loads(result_bytes)
    receipt = _load(EXPERIMENT / "ontology-adequacy-receipt.json")
    schema = _load(EXPERIMENT / "ontology-review-output-schema.json")

    assert _digest(precommit) == receipt["review_precommit"]["sha256"]
    assert _digest(raw) == receipt["capture"]["retained_raw_sha256"]
    assert len(raw) == receipt["capture"]["retained_raw_byte_length"]
    assert _digest(result_bytes) == receipt["capture"]["result_sha256"]
    assert len(result_bytes) == receipt["capture"]["result_byte_length"]
    assert raw == (
        b"BEGIN_ADEQUACY_JSON\n" + result_bytes.rstrip(b"\n") + b"\nEND_ADEQUACY_JSON\n"
    )
    Draft202012Validator(schema).validate(result)

    assert result["status"] == receipt["status"] == "REFUSED_ADEQUACY"
    assert result["eligibility"]["verdict"] == receipt["eligibility"] == "PASS"
    assert result["candidate_sha256"] == receipt["candidate_sha256"]
    assert result["compiled_contract_identity"] == receipt["compiled_contract_identity"]
    assert {item["id"]: item["verdict"] for item in result["criteria"]} == (
        receipt["criteria"]
    )
    assert len(result["criteria"]) == len({item["id"] for item in result["criteria"]})
    assert result["unresolved_count"] == receipt["unresolved_count"] == 1
    assert len(result["witness"]) == receipt["witness_count"] == 32
    assert sum(item["judgment"] == "FAIL" for item in result["witness"]) == 1
    assert sum(item["support"] != "SUPPORTED" for item in result["witness"]) == 0
    failed = [item for item in result["witness"] if item["judgment"] == "FAIL"]
    assert failed[0]["semantic_atom"] == "usable_instrument_count = 17"
    assert receipt["population_authorization"] == "DENIED"
    assert receipt["selected_ontology_sha256"] is None


def test_every_review_locator_is_in_the_frozen_question_binding() -> None:
    result = _load(PRIVATE / "ontology-adequacy-result.json")
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
