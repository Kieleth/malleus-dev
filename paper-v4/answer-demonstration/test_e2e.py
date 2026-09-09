"""A full run cannot silently import an ontology or change producer sessions."""

import pytest


def test_population_requires_the_ontology_producer_and_an_accepted_gate():
    from e2e import phase_two_guard

    accepted = {"status": "ACCEPTED"}
    phase_two_guard("agent:a", "agent:a", accepted, False)
    with pytest.raises(ValueError, match="same producer"):
        phase_two_guard("agent:a", "agent:b", accepted, False)
    with pytest.raises(ValueError, match="accepted ontology"):
        phase_two_guard("agent:a", "agent:a", {"status": "REFUSED"}, False)
    with pytest.raises(ValueError, match="before population"):
        phase_two_guard("agent:a", "agent:a", accepted, True)


def test_missing_producer_identity_is_not_same_session_evidence():
    from e2e import phase_two_guard

    for value in (None, "", " "):
        with pytest.raises(ValueError, match="producer identity"):
            phase_two_guard(value, value, {"status": "ACCEPTED"}, False)
