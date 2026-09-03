"""Guards for the exact accepted v2 build and replay-query result bundle."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from malleus.ledger import canonical_json


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "paper-v4/experiment-v2"
RESULTS = EXPERIMENT / "results"
EXPECTED_DIGESTS = {
    "experiment-result.json": (
        "sha256:bd0361d7fb01554db87723f725ce01eeeb42739bf556c5f8717c52245408c9bc"
    ),
    "population-plan.json": (
        "sha256:fa1194aa705c36ff6ef06bc3d7bcadbeb4297d44c95a3558e5946fb97dbc09e6"
    ),
    "population-provenance.json": (
        "sha256:2d4ce493d7d757e648cc782ff835e555554bfae73c9876a85170e74948ce5b03"
    ),
    "query-result.json": (
        "sha256:78cc2c8dc42dc10a4f46d41c95e7c751134460bc1147619e067a8f5822b0be7a"
    ),
    "replay-receipt.json": (
        "sha256:1a86d1229af04d55275dff9616e50d8686510153241689487a13e5732148b796"
    ),
}


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _load(name: str) -> dict[str, object]:
    return json.loads((RESULTS / name).read_bytes())


def test_result_bundle_is_exact_canonical_and_has_no_score() -> None:
    assert {path.name for path in RESULTS.iterdir()} == set(EXPECTED_DIGESTS)
    for name, expected in EXPECTED_DIGESTS.items():
        source = (RESULTS / name).read_bytes()
        assert _digest(source) == expected
        assert canonical_json(json.loads(source)).encode("utf-8") == source
    assert not (RESULTS / "score.json").exists()


def test_build_result_and_receipt_bind_the_replayed_graph() -> None:
    result = _load("experiment-result.json")
    receipt = _load("replay-receipt.json")

    assert result == {
        "decision": "ACCEPT",
        "entity_count": 7,
        "ledger_head": (
            "sha256:7117c49b0c4b46dd0b39c872cd4d1b914f8d4ec37a805011030ad3f374fd835b"
        ),
        "ontology_sha256": (
            "sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed"
        ),
        "reading_sha256": (
            "sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17"
        ),
        "relation_count": 6,
        "replay_receipt_sha256": EXPECTED_DIGESTS["replay-receipt.json"],
        "schema": "malleus.paper-v4.knowledge-build-result/v2",
        "source_sha256": (
            "sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9"
        ),
    }
    assert receipt["ledger_event_count"] == 23
    assert receipt["ledger_head"] == result["ledger_head"]
    assert receipt["validated_fact_set_sha256"] == (
        "sha256:bc178b7c9125d5edefd43df45f1a2949e815b17da27668308b0ae728f3f6f4ad"
    )
    assert len(receipt["queries"]["entities"]) == result["entity_count"]
    assert len(receipt["queries"]["relations"]) == result["relation_count"]


def test_population_plan_and_provenance_close_all_model_assertions() -> None:
    plan = _load("population-plan.json")
    provenance = _load("population-provenance.json")

    assert plan["contract_digest"] == (
        "sha256:2a1bed590e9788a5dbf57f2485d7e1fd2b25960ce81a24e70cb59d517d870917"
    )
    assert len(plan["proposed_operations"]["operations"]) == 13
    assertions = provenance["assertions"]
    assert len(assertions) == 47
    assert {
        kind: sum(item["assertion_kind"] == kind for item in assertions)
        for kind in ("PROPERTY", "RECORD", "SOURCE", "TARGET")
    } == {"PROPERTY": 22, "RECORD": 13, "SOURCE": 6, "TARGET": 6}
    assert len({item["block_id"] for item in assertions}) == 4
    assert provenance["ontology_sha256"] == (
        "sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed"
    )
    assert provenance["reading_sha256"] == (
        "sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17"
    )
    assert provenance["plan_sha256"] == EXPECTED_DIGESTS["population-plan.json"]
    assert provenance["schema"] == "malleus.paper-v4.population-provenance/v2"


def test_queries_use_only_the_replay_receipt_and_frozen_binding() -> None:
    query = _load("query-result.json")
    receipt = _load("replay-receipt.json")

    assert query["schema"] == "malleus.paper-v4.query-replay/v1"
    assert query["inputs"] == {
        "ontology_sha256": (
            "sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed"
        ),
        "query_binding_sha256": (
            "sha256:922e2c628a86bca22d761ebf6d453c9056ead8bdc5301e3c5dfb193db61368c1"
        ),
        "replay_receipt_sha256": EXPECTED_DIGESTS["replay-receipt.json"],
    }
    assert query["graph_state_digest"] == receipt["graph_state_digest"]
    assert [len(item["rows"]) for item in query["queries"]] == [0, 2, 4, 0]
    assert query["forbidden_attempts"] == {
        "embedding_import": 0,
        "file_read": 0,
        "network": 0,
    }
    assert all(
        set(item) == {"query_id", "question_id", "rows"}
        for item in query["queries"]
    )


def test_query_binding_never_enters_build_or_replay_identity() -> None:
    result_source = (RESULTS / "experiment-result.json").read_text()
    receipt_source = (RESULTS / "replay-receipt.json").read_text()
    plan_source = (RESULTS / "population-plan.json").read_text()
    provenance_source = (RESULTS / "population-provenance.json").read_text()

    for source in (result_source, receipt_source, plan_source, provenance_source):
        assert "922e2c628a86" not in source
        assert "query_binding" not in source
