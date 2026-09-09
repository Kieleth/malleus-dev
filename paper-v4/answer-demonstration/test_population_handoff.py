"""A producer must receive the runner's source namespace, not invent it."""

from copy import deepcopy
from pathlib import Path

import pytest


def test_coordinate_delivery_is_complete_not_only_compiler_diagnostics():
    from population_handoff import coordinates, check_message, message

    run = (
        Path(__file__).parents[2]
        / "private/paper-v4-answer-demonstration/sol-fresh-comparison-01"
    )
    ids = coordinates(run)
    with pytest.raises(ValueError, match="source_id"):
        check_message(
            "Read accepted/diagnostic.json and accepted/population-surface.json", ids
        )
    text = message(run)
    check_message(text, ids)
    assert all(value in text for value in ids.values())
    assert "capture.attribution.source_id" in text


def test_identity_return_cannot_change_capture_semantics():
    from population_handoff import check_identity_only_return

    original = {
        "capture": {
            "attribution": {"source_id": "record:article"},
            "assertions": [{"id": "a", "statement": "source words"}],
        },
        "records": {"entities": [{"id": "r"}]},
        "supersessions": [],
    }
    corrected = deepcopy(original)
    corrected["capture"]["attribution"]["source_id"] = "source:retained"
    check_identity_only_return(original, corrected, "source:retained")
    for key in ("records", "supersessions"):
        wrong = deepcopy(corrected)
        wrong[key] = ["changed"]
        with pytest.raises(ValueError):
            check_identity_only_return(original, wrong, "source:retained")
    wrong = deepcopy(corrected)
    wrong["capture"]["assertions"][0]["statement"] = "changed meaning"
    with pytest.raises(ValueError):
        check_identity_only_return(original, wrong, "source:retained")
    with pytest.raises(ValueError):
        check_identity_only_return(original, original, "source:retained")


def test_changed_semantics_never_reach_the_execution_boundary(tmp_path, monkeypatch):
    import json
    import population_handoff as handoff
    import e2e_execute

    (tmp_path / "attempt-01").mkdir()
    (tmp_path / "producer/work").mkdir(parents=True)
    original = {
        "capture": {"attribution": {"source_id": "old"}},
        "records": {"entities": []},
        "supersessions": [],
    }
    corrected = deepcopy(original)
    corrected["capture"]["attribution"]["source_id"] = "retained"
    original_path = tmp_path / "attempt-01/submitted-population.json"
    path = tmp_path / "producer/work/document-population.json"
    original_path.write_text(json.dumps(original))
    path.write_text(json.dumps(corrected))
    monkeypatch.setattr(handoff, "coordinates", lambda _: {"source_id": "retained"})
    calls = []
    monkeypatch.setattr(e2e_execute, "execute", lambda *args: calls.append(args))
    handoff.execute_return(tmp_path, "2026-09-09T00:13:35Z")
    assert len(calls) == 1
    corrected["records"]["entities"].append({"id": "invented"})
    path.write_text(json.dumps(corrected))
    with pytest.raises(ValueError, match="more than the source identity"):
        handoff.execute_return(tmp_path, "2026-09-09T00:13:35Z")
    assert len(calls) == 1
