"""G2a: the G1 specimens as ordinary graph records answer every authored query.

Each check is shown to discriminate: a deliberately broken variant turns it red.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import admission  # noqa: E402
import graph as graph_mod  # noqa: E402
import runner  # noqa: E402
from graph import Graph, decode, encode  # noqa: E402

SPECIMENS = {s["specimen_id"]: s for s in runner.load_specimens()}


@pytest.fixture(scope="module")
def report():
    return runner.run_all()


def _spec(report, sid):
    return next(s for s in report["specimens"] if s["id"] == sid)


def test_eight_specimens_loaded():
    assert len(SPECIMENS) == 8


def test_no_problems(report):
    assert runner.problems(report) == []


def test_every_non_pass_is_a_listed_finding(report):
    observed = {(s["id"], r["query"], r["branch"]): r["status"]
                for s in report["specimens"] for r in s["rows"] if r["status"] != "PASS"}
    assert observed == {k: v[0] for k, v in runner.FINDINGS.items()}
    refusals = {(s["id"], r["refusal"]): r["status"]
                for s in report["specimens"] for r in s["refusals"] if r["status"] != "PASS"}
    assert refusals == {k: v[0] for k, v in runner.REFUSAL_FINDINGS.items()}


def test_answer_counts(report):
    rows = [r for s in report["specimens"] for r in s["rows"]]
    assert len(rows) == 100
    assert sum(r["status"] == "PASS" for r in rows) == 99


def test_rf_overlap_diagnostic_reaches_the_expected_category(report):
    row = next(r for r in _spec(report, "G1-01-PRICE-HISTORY")["refusals"] if r["refusal"] == "RF-OVERLAP")
    assert row["got"] == "UNKNOWN_REFERENCE" and row["diagnostic_category"] == "UNSUPPORTED_SEMANTICS"


@pytest.mark.parametrize("sid", sorted(SPECIMENS))
def test_round_trip_and_rebuild(report, sid):
    st = _spec(report, sid)["storage"]
    assert st["reserialize_identical"] and st["changes_identical"] and st["object_diffs"] == []
    assert st["roundtrip_answers_identical"] and st["rebuild_identical"] and st["rebuild_answers_identical"]
    assert st["prefix_mismatches"] == [] and st["queries_wrote_nothing"]


@pytest.mark.parametrize("sid", sorted(SPECIMENS))
def test_refusals_leave_graph_unchanged(report, sid):
    for r in _spec(report, sid)["refusals"]:
        assert r["got"] is not None and r["unchanged"] and not r["new_graph_returned"]
        assert r["head_after"] == r["want_head_after"]


@pytest.mark.parametrize("sid", sorted(SPECIMENS))
def test_accepted_changes_admit(report, sid):
    assert _spec(report, sid)["positive_control"] == []


# -- discrimination: each broken variant must be caught -------------------------

def test_reading_the_final_graph_leaks_future_closure(monkeypatch):
    """Filtering the final state instead of the prefix is caught by the specimen answers."""
    monkeypatch.setattr(Graph, "prefix", lambda self, position: self)
    spec = SPECIMENS["G1-01-PRICE-HISTORY"]
    rows = runner.Runner(spec).run_queries(encode(spec["objects"], spec["changes"]))
    failed = {r["query"] for r in rows if r["status"] == "FAIL"}
    assert {"P02", "P03", "P09", "PH-K1", "PH-K2"} <= failed


def test_lossy_literal_is_caught():
    spec = SPECIMENS["G1-08-STORAGE-CLOSURE"]
    text = encode(spec["objects"], spec["changes"]).dumps()
    assert '"lexical":"5.40"' in text
    objs, _ = decode(Graph.loads(text.replace('"lexical":"5.40"', '"lexical":"5.4"')))
    assert {o["id"]: o for o in objs}["q-price"] != {o["id"]: o for o in spec["objects"]}["q-price"]


def test_reversed_edge_is_caught():
    spec = SPECIMENS["G1-08-STORAGE-CLOSURE"]
    g = encode(spec["objects"], spec["changes"])
    e = g.edges["rel:part-of"]
    e["from"], e["to"] = e["to"], e["from"]
    rows = runner.Runner(spec).run_queries(g)
    assert next(r for r in rows if r["query"] == "ST04")["status"] == "FAIL"


def test_merged_model_membership_is_caught():
    spec = SPECIMENS["G1-08-STORAGE-CLOSURE"]
    g = encode(spec["objects"], spec["changes"])
    g.subgraphs["model:m1"] = list(g.subgraphs["model:m2"])
    rows = runner.Runner(spec).run_queries(g)
    assert next(r for r in rows if r["query"] == "ST05")["status"] == "FAIL"


def _leaky_admit(mode):
    real = admission.admit

    def leaky(graph, change, objs, base, params=None):
        new, refused = real(graph, change, objs, base, params)
        if refused and objs[0]["type"] == "ASSERTION" and objs[0].get("applicability", {}).get("kind") == "NONE_STATED":
            first = objs[0]
            if mode == "new_position":  # the valid half becomes its own accepted change
                graph_mod.apply_change(graph, {**change, "adds_refs": [first["id"]]}, [first], len(graph.ledger()))
            else:  # the valid half is merged silently into the head's change
                graph_mod.encode_object(graph, first)
                graph.subgraphs[graph_mod.LEDGER + graph.head()].append(first["id"])
        return new, refused
    return leaky


def test_valid_half_as_new_position_is_caught(monkeypatch):
    monkeypatch.setattr(runner, "admit", _leaky_admit("new_position"))
    spec = SPECIMENS["G1-08-STORAGE-CLOSURE"]
    rows = runner.Runner(spec).run_refusals(encode(spec["objects"], spec["changes"]))
    bad = next(x for x in rows if x["refusal"] == "RF-PARTIAL")
    assert not bad["unchanged"] and bad["head_after"] != bad["want_head_after"]


def test_valid_half_merged_into_head_is_caught(monkeypatch):
    monkeypatch.setattr(runner, "admit", _leaky_admit("merge"))
    spec = SPECIMENS["G1-08-STORAGE-CLOSURE"]
    r = runner.Runner(spec)
    assert not next(x for x in r.run_refusals(encode(spec["objects"], spec["changes"]))
                    if x["refusal"] == "RF-PARTIAL")["unchanged"]
    rows = r.run_queries(encode(spec["objects"], spec["changes"]))
    assert next(x for x in rows if x["query"] == "ST12")["status"] == "FAIL"


def test_value_keyed_identity_would_merge_distinct_premises():
    """Equal value, equal applicability: H1 and B2 stay two records with their own bases."""
    spec = SPECIMENS["G1-02-ORDER-PREMISES"]
    g = encode(spec["objects"], spec["changes"])
    assert g.payload("H1")["value"] == g.payload("B2")["value"]
    assert g.lex("H1", "basis") == "ASSUMPTION" and g.lex("B2", "basis") == "CORRECTION"
    assert g.ref("H1", "account_ref") != g.ref("B2", "account_ref")


def test_unencodable_applicability_is_refused_by_the_encoder():
    obj = next(o for o in SPECIMENS["G1-08-STORAGE-CLOSURE"]["rejected_objects"] if o["id"] == "q-recurring")
    with pytest.raises(graph_mod.EncodingError):
        graph_mod.encode_object(Graph(), obj)


def test_ca08_note_combination():
    """CA08 branch 1 note: under the second assumptions branch, H1 joins the candidates."""
    spec = SPECIMENS["G1-03-COMPETING-ACCOUNTS"]
    r = runner.Runner(spec)
    q = r.queries["CA08"]
    got = r.render(r.answer(encode(spec["objects"], spec["changes"]), q,
                            {"use_selection": "USE_ONLY", "unscoped_assumptions": "INCLUDE"}))
    assert runner.matches(got, {"state": "AMBIGUOUS_SELECTION", "candidate_refs": ["Q1", "Q2", "H1"]}) == []
