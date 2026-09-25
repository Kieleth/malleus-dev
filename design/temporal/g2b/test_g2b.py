"""G2b: the G1 specimens in SQLite answer every authored query, refuse every authored write,
round-trip and rebuild. Negative controls show the checks can fail."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import queries  # noqa: E402
import runner  # noqa: E402
import store  # noqa: E402

SPECIMENS = runner.load_specimens()


@pytest.fixture(scope="module")
def results():
    return {name: runner.run_specimen(name, spec) for name, spec in SPECIMENS.items()}


@pytest.mark.parametrize("name", sorted(SPECIMENS))
def test_every_query_matches_or_is_a_registered_specimen_issue(results, name):
    r = results[name]
    fails = [(x["query"], x["branch"], x["diffs"]) for x in r["rows"] if x["status"] == "FAIL"]
    assert fails == []
    issues = {(x["query"], x["branch"]) for x in r["rows"] if x["status"] == "SPECIMEN_ISSUE"}
    registered = {q for q, _ in runner.SPECIMEN_ISSUES}
    assert {q for q, _ in issues} <= registered
    for q, token in runner.SPECIMEN_ISSUES:
        if any(x["query"] == q for x in r["rows"]):
            assert any(i[0] == q and token in i[1].split(",") for i in issues), (q, token, "registered issue no longer mismatches")


@pytest.mark.parametrize("name", sorted(SPECIMENS))
def test_no_answer_equals_a_forbidden_answer(results, name):
    verdicts = [(f["query_ref"], b, v) for f in results[name]["forbidden"].values() for b, v in f["runs"].items()]
    assert verdicts, "no forbidden answer was checked"
    assert [v for v in verdicts if v[2] != "NO_MATCH"] == []


@pytest.mark.parametrize("name", sorted(SPECIMENS))
def test_refusals_leave_the_store_unchanged(results, name):
    for x in results[name]["refusals"]:
        assert x["got"] == x["expected"], x
        assert x["rows_unchanged"] and x["file_bytes_unchanged"] and not x["leaked"], x
        assert x["status"] == "PASS"


@pytest.mark.parametrize("name", sorted(SPECIMENS))
def test_round_trip_rebuild_and_read_only_queries(results, name):
    r = results[name]
    assert r["roundtrip_diffs"] == []
    assert r["rebuild_graph_diffs"] == []
    assert r["rebuild_answers_same"] is True
    assert r["queries_wrote_nothing"] is True
    assert r["notes"] == []
    if r["cells_vs_key"] is not None:
        assert r["cells_vs_key"]["diffs"] == []


def test_foreign_keys_must_be_enabled_per_connection(tmp_path):
    path = tmp_path / "s.db"
    store.create(path).close()
    raw = sqlite3.connect(path)
    assert raw.execute("PRAGMA foreign_keys").fetchone()[0] == 0  # SQLite default
    raw.close()
    for ro in (False, True):
        conn = store.connect(path, read_only=ro)
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        conn.close()


def test_read_only_connection_refuses_writes(tmp_path):
    path = tmp_path / "s.db"
    store.build(path, store.canonical_ledger(SPECIMENS["g1-08-storage-closure.json"])).close()
    conn = store.connect(path, read_only=True)
    with pytest.raises(sqlite3.OperationalError):
        conn.execute("DELETE FROM evidence")


def test_typed_literals_keep_lexical_form(tmp_path):
    path = tmp_path / "s.db"
    conn = store.build(path, store.canonical_ledger(SPECIMENS["g1-08-storage-closure.json"]))
    rows = dict(conn.execute("SELECT id, typeof(v_lexical) || ':' || v_lexical FROM assertion").fetchall())
    assert rows["q-partno"] == "text:0750"
    assert rows["q-price"] == "text:5.40"
    # control: a NUMERIC-affinity column would have turned both into numbers
    ctl = sqlite3.connect(":memory:")
    ctl.execute("CREATE TABLE t (v NUMERIC)")
    ctl.executemany("INSERT INTO t VALUES (?)", [("0750",), ("5.40",)])
    assert ctl.execute("SELECT typeof(v), v FROM t ORDER BY rowid").fetchall() == [("integer", 750), ("real", 5.4)]


@pytest.mark.parametrize("name, expected_collapse", [
    ("g1-02-order-premises.json", {"B2", "H1"}),
    ("g1-03-competing-accounts.json", {"Q2", "H1"}),
])
def test_a_value_key_would_collapse_distinct_claims(tmp_path, name, expected_collapse):
    """Control for SAME_VALUE_DIFFERENT_MEANING: grouping by subject, property, value and times
    merges claims that this schema keeps apart by id."""
    conn = store.build(tmp_path / "s.db", store.canonical_ledger(SPECIMENS[name]))
    groups = conn.execute("""
        SELECT group_concat(id) FROM assertion
        GROUP BY subject_id, property, v_datatype, v_lexical, v_unit, app_kind, app_from, app_until, app_instant
        HAVING COUNT(*) > 1""").fetchall()
    assert [set(g[0].split(",")) for g in groups] == [expected_collapse]


def test_leaky_history_read_is_caught(tmp_path, monkeypatch):
    """Control for HISTORICAL_READ: drop the ':at' bound on knowledge ends (filter the final
    table) and PH-K1 returns the forbidden K2 closure."""
    spec = SPECIMENS["g1-01-price-history.json"]
    path = tmp_path / "s.db"
    store.build(path, store.canonical_ledger(spec)).close()
    leaky = queries.HISTORY_CELLS_SQL.replace("AND e.seq <= :at", "")
    assert leaky != queries.HISTORY_CELLS_SQL
    monkeypatch.setattr(queries, "HISTORY_CELLS_SQL", leaky)
    q = next(x for x in spec["queries"] if x["id"] == "PH-K1")
    labels = {(d["from_assertion_ref"], d["knowledge_from"]): d["id"] for d in spec["derived_labels"]}
    ans = queries.Reader(store.connect(path, read_only=True), labels, {}).answer(q["kind"], q["inputs"])
    forbidden = [f for f in spec["forbidden"] if f["query_ref"] == "PH-K1"]
    assert "MATCH" in {runner.forbidden_match(f["answer"], ans) for f in forbidden}
    assert runner.compare(q["expected"], ans) != []


def test_partial_write_refusal_rolls_back_the_valid_half(tmp_path):
    """RF-PARTIAL: q-weight is valid on its own; the change also carries rel:bad. Neither survives."""
    spec = SPECIMENS["g1-08-storage-closure.json"]
    path = tmp_path / "s.db"
    conn = store.build(path, store.canonical_ledger(spec))
    rejected = {o["id"]: o for o in spec["rejected_objects"]}
    r = next(x for x in spec["refusals"] if x["id"] == "RF-PARTIAL")
    alone = dict(r, id="probe", would_add_refs=["q-weight"])
    assert store.attempt(conn, alone, rejected) == 5  # admissible alone, rolled back by the probe
    res = store.attempt(conn, r, rejected)
    assert isinstance(res, store.Refused) and res.category == "UNKNOWN_REFERENCE"
    assert conn.execute("SELECT COUNT(*) FROM record WHERE id IN ('q-weight', 'rel:bad')").fetchone()[0] == 0
    assert store.head(conn) == "R4"


def test_encoder_input_is_objects_and_changes_only():
    for spec in SPECIMENS.values():
        assert set(store.canonical_ledger(spec)) == {"objects", "changes"}
