"""A malformed submission or replay mismatch cannot become a successful run."""

import pytest


def test_population_envelope_is_closed_and_required():
    from capture import population_parts

    value = {"capture": {}, "records": {}, "supersessions": []}
    assert population_parts(value) == value
    for malformed in ({}, {**value, "answers": []}, [value]):
        with pytest.raises(ValueError, match="capture, records and supersessions"):
            population_parts(malformed)


@pytest.mark.parametrize("change", ["receipt", "graph"])
def test_replay_must_match_both_receipt_and_graph(change):
    from capture import verify_replay

    verify_replay(
        b"receipt",
        {"entities": []},
        b"receipt",
        {"entities": []},
        admission_occurred=True,
    )
    after_receipt = b"different" if change == "receipt" else b"receipt"
    after_graph = {"entities": ["different"]} if change == "graph" else {"entities": []}
    with pytest.raises(ValueError, match="replay differs"):
        verify_replay(
            b"receipt",
            {"entities": []},
            after_receipt,
            after_graph,
            admission_occurred=True,
        )


@pytest.mark.parametrize("admitted", [False, True])
def test_replay_evidence_does_not_call_no_change_an_admission(admitted):
    from capture import verify_replay

    result = verify_replay(b"receipt", {}, b"receipt", {}, admission_occurred=admitted)
    assert result == {"replay_matches_preclose": True, "admission_occurred": admitted}
    assert "replay_matches_admission" not in result


def test_execution_time_is_explicit_and_timezone_aware():
    from capture import execution_time

    assert execution_time("2026-09-07T08:00:00Z") == "2026-09-07T08:00:00Z"
    for value in (None, "", "2026-09-07", "2026-09-07T08:00:00", "tomorrow"):
        with pytest.raises((TypeError, ValueError)):
            execution_time(value)
