"""Hard guards for the model-population acquisition envelope."""

from __future__ import annotations

import json

import pytest

from research.ontology_driven_kg_realization.experiments.document_paper.population_acquisition import (
    PopulationAcquisitionError,
    PopulationCandidateKind,
    classify_population_candidate,
)


SUCCESS = "malleus.paper-v4.population/v2"
REFUSAL = "malleus.paper-v4.population-refusal/v2"
PREFIX = "urn:malleus:paper-v4:v2:record:"


def _source(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode()


def _classify(source: bytes) -> PopulationCandidateKind:
    return classify_population_candidate(
        source,
        success_schema=SUCCESS,
        refusal_schema=REFUSAL,
        record_id_prefix=PREFIX,
        ordinal_width=3,
    )


def _proposal(*record_ids: str) -> dict[str, object]:
    return {
        "schema": SUCCESS,
        "ontology_sha256": "sha256:" + "1" * 64,
        "reading_sha256": "sha256:" + "2" * 64,
        "records": [{"record_id": record_id} for record_id in record_ids],
    }


def test_accepts_only_ordered_opaque_proposal_ids() -> None:
    assert _classify(
        _source(_proposal(PREFIX + "001", PREFIX + "002"))
    ) is PopulationCandidateKind.PROPOSAL


@pytest.mark.parametrize(
    "record_ids",
    (
        ("answer-bearing-id",),
        (PREFIX + "002",),
        (PREFIX + "001", PREFIX + "003"),
        (PREFIX + "001", PREFIX + "001"),
    ),
)
def test_refuses_any_nonsequential_or_answer_bearing_identity(
    record_ids: tuple[str, ...],
) -> None:
    with pytest.raises(PopulationAcquisitionError) as caught:
        _classify(_source(_proposal(*record_ids)))

    assert caught.value.code == "POPULATION_RECORD_ID_POLICY_VIOLATION"
    assert json.loads(caught.value.canonical_diagnostic_bytes()) == {
        "code": "POPULATION_RECORD_ID_POLICY_VIOLATION",
        "detail": caught.value.detail,
        "stage": "POPULATION_ACQUISITION",
        "status": "REFUSED",
        "subject": caught.value.subject,
    }


def test_model_refusal_is_terminal_and_not_a_population_proposal() -> None:
    assert _classify(
        _source({"schema": REFUSAL, "reason": "No faithful nonempty graph."})
    ) is PopulationCandidateKind.MODEL_REFUSAL


@pytest.mark.parametrize(
    "value",
    (
        {"schema": REFUSAL, "reason": ""},
        {"schema": REFUSAL, "reason": "No graph.", "records": []},
        {"schema": "unknown", "records": []},
    ),
)
def test_malformed_or_unknown_envelopes_are_structural_refusals(
    value: dict[str, object],
) -> None:
    with pytest.raises(PopulationAcquisitionError):
        _classify(_source(value))


def test_duplicate_json_keys_are_a_structural_refusal() -> None:
    with pytest.raises(PopulationAcquisitionError) as caught:
        _classify(b'{"schema":"one","schema":"two"}')

    assert caught.value.code == "POPULATION_CANDIDATE_JSON_INVALID"
