"""A causal reference must expose the stored event, never infer its meaning."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from answers import answer
from test_answers import view

PRIVATE = Path(__file__).resolve().parents[2] / "private/paper-v4-answer-demonstration"


def example():
    raw = view(
        [
            {
                "id": "claim",
                "type": "Claim",
                "hypothesis_disposition": "PREFERRED",
                "assertion_modality": "HYPOTHESISED",
                "cause_event": "r-19",
                "effect_event": "r-04",
            },
            {
                "id": "r-19",
                "type": "Episode",
                "name": "valve opening",
                "event_type": "OPENING",
                "assertion_modality": "HYPOTHESISED",
            },
            {
                "id": "r-04",
                "type": "Episode",
                "name": "pressure drop",
                "event_type": "PRESSURE_CHANGE",
                "assertion_modality": "HYPOTHESISED",
                "subject": "vessel",
                "caused_by": "r-19",
            },
            {"id": "vessel", "type": "Vessel", "name": "test vessel"},
            {"id": "evidence", "type": "Observation", "name": "test evidence"},
        ],
        [
            {
                "key": "link",
                "type": "EvidenceRelation",
                "source_id": "evidence",
                "target_id": "claim",
                "relation_type": "SUPPORTS",
            }
        ],
    )
    for name, item in raw.types.items():
        item["qualified_name"] = "https://example.test/" + name
    raw.types["Episode"]["family"] = "EVENT"
    for slot in raw.types["Claim"]["slots"]:
        if slot["name"] in {"cause_event", "effect_event"}:
            slot.update(range_id="https://example.test/Episode", multivalued=False)
    return raw


def test_frozen_reader_exposes_references_but_not_the_events():
    result = answer(example(), "CQ-T4-01")
    assert len(result["rows"]) == 1
    assert result["rows"][0]["record"]["cause_event"] == "r-19"
    assert result["witness_ids"] == ["claim"]


@pytest.mark.parametrize("question", ["CQ-T4-01", "CQ-T4-02", "CQ-T5-01"])
def test_direct_events_are_returned_once_with_roles_fields_and_modality(question):
    from event_query import expand

    reads = example()
    if question == "CQ-T4-02":
        reads.graph.nodes[0]["hypothesis_disposition"] = "NOT_SUPPORTED"
    before = answer(reads, question)
    protected = deepcopy((reads.graph.nodes, reads.graph.edges, before))
    result = expand(reads, before)
    assert result["rows"][: len(before["rows"])] == before["rows"]
    assert result["rows"][len(before["rows"]) :] == [
        reads.row(reads.graph.get_node(key)) for key in ["r-04", "r-19"]
    ]
    assert result["paths"] == before["paths"]
    assert result["witness_ids"] == sorted(
        set(before["witness_ids"]) | {"r-04", "r-19", "vessel"}
    )
    assert protected == (reads.graph.nodes, reads.graph.edges, before)


def test_absent_references_do_not_invent_events_from_names_ids_or_neighbours():
    from event_query import expand

    reads = example()
    del reads.graph.nodes[0]["cause_event"], reads.graph.nodes[0]["effect_event"]
    reads.graph.nodes[0]["name"] = "valve opening causes pressure drop"
    before = answer(reads, "CQ-T4-01")
    assert expand(reads, before) == before


def test_only_direct_references_are_followed_and_duplicate_targets_appear_once():
    from event_query import expand

    reads = example()
    reads.graph.nodes[0]["effect_event"] = "r-19"
    reads.graph.nodes[1]["caused_by"] = "r-04"
    before = answer(reads, "CQ-T4-01")
    result = expand(reads, before)
    assert [r["witness"]["record_id"] for r in result["rows"]] == ["claim", "r-19"]
    assert "r-04" not in result["witness_ids"]


def test_already_returned_event_is_not_duplicated():
    from event_query import expand

    reads = example()
    before = answer(reads, "CQ-T4-01")
    row = reads.row(reads.graph.get_node("r-19"))
    before["rows"].append(row)
    before["witness_ids"].append("r-19")
    result = expand(reads, before)
    assert result["rows"].count(row) == 1


def test_unrelated_question_stays_exact_even_with_causal_references():
    from event_query import expand

    reads = example()
    before = answer(reads, "CQ-T4-01")
    before["question_id"] = "CQ-T1-01"
    assert expand(reads, before) == before


def test_public_range_query_can_resolve_an_event_subtype():
    from event_query import expand

    reads = example()
    reads.types["BaseEvent"] = {
        "family": "EVENT",
        "name": "BaseEvent",
        "qualified_name": "https://example.test/BaseEvent",
        "slots": [],
    }
    for slot in reads.types["Claim"]["slots"]:
        if slot["name"] in {"cause_event", "effect_event"}:
            slot["range_id"] = "https://example.test/BaseEvent"
    original = reads.graph.query
    reads.graph.query = lambda entity_type=None: original(
        "Episode" if entity_type == "BaseEvent" else entity_type
    )
    result = expand(reads, answer(reads, "CQ-T4-01"))
    assert [r["witness"]["record_id"] for r in result["rows"]] == [
        "claim",
        "r-04",
        "r-19",
    ]


def test_live_projection_drift_refuses_before_method_directory_is_written(
    tmp_path, monkeypatch
):
    import event_query

    (tmp_path / "answers.py").write_text("changed projection")
    monkeypatch.setattr(event_query, "HERE", tmp_path)
    monkeypatch.setattr(event_query.fresh, "verify_packet", lambda run: None)
    target = PRIVATE / "must-not-create-event-projection-drift"
    assert not target.exists()
    with pytest.raises(ValueError, match="projection source"):
        event_query.inputs()
    assert not target.exists()


def test_runtime_mismatch_refuses_before_method_directory_is_written(monkeypatch):
    import event_query

    def refuse(*args):
        raise ValueError("runtime differs")

    monkeypatch.setattr(event_query.fresh, "verify_packet", refuse)
    target = PRIVATE / "must-not-create-event-runtime-drift"
    assert not target.exists()
    with pytest.raises(ValueError, match="runtime differs"):
        event_query.freeze(target)
    assert not target.exists()


@pytest.mark.parametrize(
    "fault",
    [
        "missing",
        "wrong_family",
        "wrong_range",
        "string_range",
        "multiple",
        "list",
        "empty",
        "undeclared",
        "missing_range",
        "missing_cardinality",
        "unbound_role",
        "wrong_target_type",
    ],
)
def test_invalid_declared_or_resolved_reference_refuses(fault):
    from event_query import expand

    reads = example()
    before = answer(reads, "CQ-T4-01")
    slot = next(s for s in reads.types["Claim"]["slots"] if s["name"] == "cause_event")
    if fault == "missing":
        reads.graph.nodes = [n for n in reads.graph.nodes if n["id"] != "r-19"]
    elif fault == "wrong_family":
        reads.types["Episode"]["family"] = "ENTITY"
    elif fault == "wrong_range":
        reads.types["OtherEvent"] = {
            "family": "EVENT",
            "name": "OtherEvent",
            "qualified_name": "https://example.test/OtherEvent",
            "slots": [],
        }
        slot["range_id"] = "https://example.test/OtherEvent"
    elif fault == "string_range":
        slot["range_id"] = "https://malleus.dev/contract-facts/String"
    elif fault == "multiple":
        slot["multivalued"] = True
    elif fault == "list":
        before["rows"][0]["record"]["cause_event"] = ["r-19"]
    elif fault == "empty":
        before["rows"][0]["record"]["cause_event"] = ""
    elif fault == "undeclared":
        reads.types["Claim"]["slots"].remove(slot)
    elif fault == "missing_range":
        del slot["range_id"]
    elif fault == "missing_cardinality":
        del slot["multivalued"]
    elif fault == "unbound_role":
        before["rows"][0]["record"]["cause_event"] = "r-04"
    elif fault == "wrong_target_type":
        reads.graph.nodes[1]["type"] = "Vessel"
    with pytest.raises(ValueError, match="causal event reference"):
        expand(reads, before)


@pytest.mark.parametrize(
    "fault", ["original", "event", "path", "witness", "extra", "unrelated"]
)
def test_delta_guard_rejects_changes_outside_exact_event_projection(fault):
    from event_query import expand, check_delta

    reads = example()
    before = [answer(reads, q) for q in ["CQ-T4-01", "CQ-T1-03"]]
    after = [expand(reads, q) for q in before]
    check_delta(reads, before, after)
    if fault == "original":
        after[0]["rows"][0]["record"]["assertion_modality"] = "STATED"
    elif fault == "event":
        after[0]["rows"][-1]["record"]["name"] = "invented event"
    elif fault == "path":
        after[0]["paths"].append(["claim", "cause_event", "r-19"])
    elif fault == "witness":
        after[0]["witness_ids"].remove("r-19")
    elif fault == "extra":
        after[0]["rows"].append(deepcopy(after[0]["rows"][-1]))
    elif fault == "unrelated":
        after[1]["note"] = "changed"
    with pytest.raises(ValueError, match="event projection"):
        check_delta(reads, before, after)


def test_pinned_execution_reproduces_and_preserves_all_history():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from test_event_query import check_execution; check_execution()",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_assessment_quotes_the_frozen_question_without_rewording():
    folder = PRIVATE / "event-query-01"
    questions = json.loads((folder / "first/review-docket.json").read_bytes())[
        "questions"
    ]
    question = next(q["question"] for q in questions if q["question_id"] == "CQ-T4-01")
    assessment = " ".join((folder / "assessment.md").read_text().split())
    assert f"Question: “{question}”" in assessment


def check_execution():
    from tempfile import TemporaryDirectory
    from event_query import BASE, freeze, execute

    assert BASE.is_absolute(), (
        "frozen producer task identity requires its absolute coordinate"
    )

    def tree(path):
        return {
            str(p.relative_to(path)): p.read_bytes()
            for p in path.rglob("*")
            if p.is_file()
        }

    protected = tree(BASE)
    with TemporaryDirectory(dir=PRIVATE, prefix="event-query-test-") as name:
        root = Path(name)
        freeze(root / "method")
        summary = execute(root / "method", root / "first")
        assert summary["changed_questions"] == ["CQ-T4-01", "CQ-T5-01"]
        assert summary["added_record_ids"] == [
            "event:co2-degassing",
            "event:deep-earthquakes",
        ]
        assert (
            summary["ledger_bytes_unchanged"] and summary["original_queries_reproduced"]
        )
        execute(root / "method", root / "repeat")
        assert tree(root / "first") == tree(root / "repeat")
        queries = json.loads((root / "first/query-result.json").read_bytes())["queries"]
        for q in queries:
            assert (
                q["paths"]
                == next(
                    x
                    for x in json.loads(
                        (BASE / "attempt-02/query-result.json").read_bytes()
                    )["queries"]
                    if x["question_id"] == q["question_id"]
                )["paths"]
            )
        (root / "method/event_query.py").write_bytes(b"drift")
        with pytest.raises(ValueError):
            execute(root / "method", root / "drift")
        assert not (root / "drift").exists()
    assert tree(BASE) == protected
