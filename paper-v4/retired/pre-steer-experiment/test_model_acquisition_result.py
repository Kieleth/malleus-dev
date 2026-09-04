from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "paper-v4" / "experiment"
PRIVATE = ROOT / "private" / "paper-v4-evaluation"


def _digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def _extract(response_path: Path) -> bytes:
    response = response_path.read_text(encoding="utf-8")
    start = "BEGIN_ONTOLOGY_YAML\n"
    end = "END_ONTOLOGY_YAML\n"

    assert response.startswith(start)
    assert response.endswith(end)
    assert response.count("BEGIN_ONTOLOGY_YAML") == 1
    assert response.count("END_ONTOLOGY_YAML") == 1
    return response.removeprefix(start).removesuffix(end).encode("utf-8")


def test_retained_responses_extract_without_repair() -> None:
    first = _extract(PRIVATE / "model-ontology-response-01.txt")
    assert len(first) == 5463
    assert sha256(first).hexdigest() == (
        "defe0c91e90326eb44e06480a20234ffc153ccba81e3a3f6837cbfab64a4dbeb"
    )

    candidate = (EXPERIMENT / "model-ontology-proposal.yaml").read_bytes()
    assert _extract(PRIVATE / "model-ontology-response-02.txt") == candidate
    assert sha256(candidate).hexdigest() == (
        "5abfa4774d932ed79e637c82396538620ee7fe8e460e59ad17ecf812fa44f4df"
    )


def test_acquisition_receipt_binds_the_precommit_response_and_candidate() -> None:
    receipt = json.loads((EXPERIMENT / "model-acquisition-receipt.json").read_bytes())

    assert receipt["status"] == "CANDIDATE_02_COMPILED"
    assert receipt["precommit"]["sha256"] == _digest(
        EXPERIMENT / "model-acquisition-precommit.json"
    )
    attempts = receipt["attempts"]
    assert [item["attempt"] for item in attempts] == [1, 2]
    assert attempts[0]["response"]["sha256"] == _digest(
        PRIVATE / "model-ontology-response-01.txt"
    )
    assert attempts[0]["compiler"] == {
        "status": "REFUSED",
        "stage": "SOURCE_CLOSURE_IMPORT_READER",
        "diagnostic": (
            "REJECTED_SOURCE: schema root contains rejected field 'default_prefix'"
        ),
    }
    assert attempts[1]["response"]["sha256"] == _digest(
        PRIVATE / "model-ontology-response-02.txt"
    )
    assert attempts[1]["extracted_candidate"]["sha256"] == _digest(
        EXPERIMENT / "model-ontology-proposal.yaml"
    )
    assert attempts[1]["compiler"] == {
        "status": "ACCEPTED",
        "official_run": 2,
        "precommit_sha256": _digest(EXPERIMENT / "ontology-compile-precommit-02.json"),
        "validated_fact_set_sha256": (
            "sha256:8b1aca802746ab7fe487af92a286e1242ae105adda9665ba68388688838ffce2"
        ),
        "fact_count": 1632,
        "validated_contract_sha256": _digest(
            EXPERIMENT / "ontology-compilation-02" / "validated-contract.json"
        ),
        "receipt_sha256": _digest(
            EXPERIMENT / "ontology-compilation-02" / "compile-receipt.json"
        ),
    }
    invalid = receipt["invalid_retained_compiler_runs"]
    assert len(invalid) == 1
    assert invalid[0]["precommit_sha256"] == _digest(
        EXPERIMENT / "ontology-compile-precommit.json"
    )
    assert receipt["trace_audit"] == {
        "input_identity_check": "PASS",
        "allowed_input_count": 7,
        "task_contract_read": True,
        "only_allowed_repository_paths_read": True,
        "network_used": False,
        "file_writes": False,
        "subtasks": False,
        "prior_conversation": "NONE",
        "correction_feedback_count": 1,
        "correction_feedback_kind": "EXACT_COMPILER_DIAGNOSTIC_ONLY",
        "isolation_note": (
            "The restriction was an explicit task contract audited from the retained "
            "task trace, not an operating-system read sandbox."
        ),
    }


def test_corrected_compile_precommit_matches_the_retained_resolver_and_outputs() -> (
    None
):
    precommit = json.loads(
        (EXPERIMENT / "ontology-compile-precommit-02.json").read_bytes()
    )
    receipt = json.loads(
        (EXPERIMENT / "ontology-compilation-02" / "compile-receipt.json").read_bytes()
    )
    selection = precommit["resolver_selection"]
    assert receipt["resolver_selection"] == {
        key: selection[key]
        for key in ("configuration_id", "profile_version", "resolver_id")
    }
    assert (
        receipt["validated_fact_set_sha256"]
        == precommit["success"]["expected_validated_fact_set_sha256"]
    )
    assert receipt["fact_count"] == precommit["success"]["expected_fact_count"]
    assert (
        _digest(EXPERIMENT / "ontology-compilation-02" / "validated-contract.json")
        == precommit["success"]["expected_validated_contract_sha256"]
    )
    assert (
        _digest(EXPERIMENT / "ontology-compilation-02" / "compile-receipt.json")
        == precommit["success"]["expected_receipt_sha256"]
    )

    first_precommit = json.loads(
        (EXPERIMENT / "ontology-compile-precommit.json").read_bytes()
    )
    first_receipt = json.loads(
        (EXPERIMENT / "ontology-compilation" / "compile-receipt.json").read_bytes()
    )
    assert (
        first_precommit["resolver"]["resolver_id"]
        != first_receipt["resolver_selection"]["resolver_id"]
    )
