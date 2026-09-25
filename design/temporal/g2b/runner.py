#!/usr/bin/env python3
"""G2b runner: encode every G1 specimen in SQLite, run every query, refusal, round trip and rebuild.

Expected answers come only from the specimen files. Nothing here writes a specimen.
Usage: python runner.py            prints the per-query table and a summary
       python runner.py json       prints the full result structure
"""

from __future__ import annotations

import itertools
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import store  # noqa: E402
from queries import CELLS, HISTORY_CELLS_SQL, Reader  # noqa: E402

G1 = HERE.parent / "g1"

# One policy per branch of each open choice that affects a query. The label prefix
# is checked against the specimen so a reordered branch list cannot pass silently.
BRANCH_POLICY = {
    "OC-03-ASSUMPTIONS-IN-UNSCOPED": [
        ("Assumptions enter only when", {"include_assumptions": False}),
        ("Every accepted account", {"include_assumptions": True})],
    "OC-03-USE-SELECTION-SCOPE": [
        ("A use selection binds only", {"default_authority": None}),
        # The specimen holds no authority record (its own note says J1 is not one).
        # The witness supplies the declared default as a runner parameter. Finding F-CA08-AUTHORITY.
        ("An adopter-declared default", {"default_authority": "ctx:flood-model"})],
    "OC-06-FLAG-SOURCE": [
        ("Derived from declared premises", {"flag_source": "DERIVED"}),
        ("Recorded by a reviewer", {"flag_source": "REVIEWER"})],
    "OC-06-SUFFICIENCY": [
        ("No declared sufficiency rule", {"sufficiency_rule": None}),
        ("Declared rule: any argument", {"sufficiency_rule": "ANY_UNREVISED_ROUTE"})],
    "OC-07-RULE-SELECTION": [
        ("Only when named", {"rule_default": False}),
        ("By default within its scope", {"rule_default": True})],
    "OC-08-WITHHELD-SCOPE": [
        ("Only reads whose closure", {"withheld_scope": "CLOSURE"}),
        ("Any missing retained artifact", {"withheld_scope": "WHOLE"})],
}
# Open choices that affect no query: the witness implements one branch only.
IMPLEMENTED_BRANCH = {
    "OC-01-TRANSITION-CLOSES-REPORT": "Transition names its target (the END effect reads target_refs)",
    "OC-05-GROUP-OR-MEMBER": "Membership always returned (member_of in EXACT_LOOKUP metadata)",
    "OC-07-RULE-ACCEPTANCE": "Accepted first (a named rule not accepted at the read position raises)",
    "OC-07-COMPLETENESS-AUTHORITY": "Not modelled: the rule's assumptions are stored as text only",
    "OC-07-INITIAL-STATE": "No initial-state clause (before the first event: NO_APPLICABLE_ACCOUNT)",
}
# Runs whose mismatch the witness attributes to the specimen, with the reason.
# The test asserts that exactly these runs mismatch.
SPECIMEN_ISSUES = {
    ("AJ06", "OC-06-FLAG-SOURCE=1"): (
        "AJ06 is not declared dependent on OC-06-FLAG-SOURCE, but under the reviewer branch no "
        "reconsideration flag exists until a reviewer records one, so the reader returns NOT_RECORDED "
        "for D1 and D2 at J3p, not NOT_REQUIRED. AJ07's branch 2 answer (D2 NOT_RECORDED although D2 "
        "has no changed premise) shows the branch withholds the flag for unchanged arguments too."),
}


def specimen_issue(qid: str, branch: str) -> str | None:
    """A registered issue applies to every run whose branch label contains its branch token."""
    for (q, token), reason in SPECIMEN_ISSUES.items():
        if q == qid and token in branch.split(","):
            return reason
    return None


def load_specimens() -> dict[str, dict]:
    return {p.name: json.loads(p.read_text(encoding="utf-8")) for p in sorted(G1.glob("g1-*.json"))}


# comparison

def _eq(key, a, b):
    if key.endswith("_refs") and isinstance(a, list) and isinstance(b, list):
        return sorted(a) == sorted(b) and len(a) == len(b)
    return a == b


def compare(expected: dict, actual: dict) -> list[str]:
    """Every key of the expected answer must be present and equal. Ref lists compare as sets.
    Metadata rows are matched by ref and only their listed fields are asserted."""
    out = []
    for key, ev in expected.items():
        if key not in actual:
            out.append(f"{key}: missing (expected {ev!r})")
        elif key == "metadata":
            rows = {r["ref"]: r for r in actual["metadata"]}
            for er in ev:
                ar = rows.get(er["ref"])
                if ar is None:
                    out.append(f"metadata {er['ref']}: no row")
                    continue
                for f, v in er.items():
                    if f not in ar or not _eq(f, v, ar[f]):
                        out.append(f"metadata {er['ref']}.{f}: expected {v!r}, got {ar.get(f, '<absent>')!r}")
        elif not _eq(key, ev, actual[key]):
            out.append(f"{key}: expected {ev!r}, got {actual[key]!r}")
    return out


def forbidden_match(answer: dict, actual: dict) -> str:
    """MATCH if the actual answer equals every listed field; NO_MATCH if some listed field differs;
    NOT_DISCRIMINATED if a listed field is absent from the actual answer and nothing else differs."""
    absent = False
    for key, fv in answer.items():
        if key not in actual:
            absent = True
            continue
        if key == "metadata":
            rows = {r["ref"]: r for r in actual["metadata"]}
            for fr in fv:
                ar = rows.get(fr["ref"])
                if ar is None:
                    absent = True
                    continue
                for f, v in fr.items():
                    if f not in ar:
                        absent = True
                    elif not _eq(f, v, ar[f]):
                        return "NO_MATCH"
        elif not _eq(key, fv, actual[key]):
            return "NO_MATCH"
    return "NOT_DISCRIMINATED" if absent else "MATCH"


# one specimen

def runs_for(spec: dict):
    """(query, branch label, policy, expected) for every run. A query tied to an open choice runs
    once per branch with other choices at branch 0; any other query runs under every combination."""
    choices = {c["id"]: c for c in spec["open_choices"] if c["affects_query_refs"]}
    for cid, c in choices.items():
        policies = BRANCH_POLICY[cid]
        assert len(policies) == len(c["branches"]), cid
        for (prefix, _), b in zip(policies, c["branches"]):
            assert b["label"].startswith(prefix), (cid, b["label"], prefix)
    for c in spec["open_choices"]:
        if not c["affects_query_refs"]:
            assert c["id"] in IMPLEMENTED_BRANCH, c["id"]
    default = {}
    for cid in choices:
        default.update(BRANCH_POLICY[cid][0][1])
    for q in spec["queries"]:
        cid = q.get("open_choice_ref")
        if cid:
            for bi, b in enumerate(choices[cid]["branches"]):
                yield q, f"{cid}={bi}", {**default, **BRANCH_POLICY[cid][bi][1]}, b["expected"][q["id"]]
        else:
            ids = sorted(choices)
            for combo in itertools.product(*(range(len(BRANCH_POLICY[c])) for c in ids)):
                policy = dict(default)
                for c, bi in zip(ids, combo):
                    policy.update(BRANCH_POLICY[c][bi][1])
                label = ",".join(f"{c}={bi}" for c, bi in zip(ids, combo) if bi) or "-"
                yield q, label, policy, q["expected"]


def answer_all(spec: dict, ledger: dict, workdir: Path) -> dict:
    """Build the store(s) from the ledger and answer every run. Returns answers keyed by (qid, branch)."""
    labels = {(d["from_assertion_ref"], d["knowledge_from"]): d["id"] for d in spec.get("derived_labels", [])}
    refusals = {r["id"]: r for r in spec["refusals"]}
    rejected = {o["id"]: o for o in spec.get("rejected_objects", [])}
    main = workdir / "main.db"
    store.build(main, ledger).close()
    before = store.snapshot(store.connect(main, read_only=True), main)
    withheld_dbs: dict[tuple, Path] = {}
    answers, notes = {}, []
    for q, branch, policy, _exp in runs_for(spec):
        inputs = q["inputs"]
        path, absent = main, ()
        if inputs.get("withheld_refs"):
            key = tuple(sorted(inputs["withheld_refs"]))
            if key not in withheld_dbs:
                withheld_dbs[key] = workdir / f"withheld-{len(withheld_dbs)}.db"
                store.build(withheld_dbs[key], ledger, withheld=frozenset(key)).close()
            path = withheld_dbs[key]
        if inputs.get("after_refusal_ref"):
            r = refusals[inputs["after_refusal_ref"]]
            w = store.connect(main)
            res = store.attempt(w, r, rejected)
            w.close()
            if not isinstance(res, store.Refused):
                notes.append(f"{q['id']}: prerequisite attempt {r['id']} was not refused")
            absent = r["would_add_refs"]
        conn = store.connect(path, read_only=True)
        answers[(q["id"], branch)] = Reader(conn, labels, policy).answer(q["kind"], inputs, absent)
        conn.close()
    after = store.snapshot(store.connect(main, read_only=True), main)
    return {"answers": answers, "unchanged_by_queries": before == after, "notes": notes}


def check_refusals(spec, ledger, workdir: Path) -> list[dict]:
    rejected = {o["id"]: o for o in spec.get("rejected_objects", [])}
    out = []
    for r in spec["refusals"]:
        path = workdir / f"refusal-{r['id']}.db"
        conn = store.build(path, ledger, upto=r["head"])
        head_before = store.head(conn)
        before = store.snapshot(conn, path)
        res = store.attempt(conn, r, rejected)
        after = store.snapshot(conn, path)
        leaked = [x for x in r["would_add_refs"] if conn.execute("SELECT 1 FROM record WHERE id=?", (x,)).fetchone()]
        head_after = store.head(conn)
        conn.close()
        got = res.category if isinstance(res, store.Refused) else "ADMITTED"
        ok = (got == r["category"] and head_before == r["head"] and head_after == r["head_after"]
              and before == after and not leaked)
        out.append({"id": r["id"], "expected": r["category"], "got": got,
                    "detected": getattr(res, "detected", []), "detail": getattr(res, "detail", []),
                    "rows_unchanged": before["rows"] == after["rows"],
                    "file_bytes_unchanged": before["file_sha256"] == after["file_sha256"],
                    "head_after": head_after, "leaked": leaked, "status": "PASS" if ok else "FAIL"})
    return out


def check_cells_against_key(spec, workdir: Path) -> dict | None:
    """g1-01 only: the witness's derived cells at K3 against the answer key's cells_at_K3."""
    if not spec.get("derived_labels"):
        return None
    key_path = (G1 / spec["reused_files"][0]["path"]).resolve()
    key = json.loads(key_path.read_text(encoding="utf-8"))["price"]["cells_at_K3"]
    conn = store.connect(workdir / "main.db", read_only=True)
    r = Reader(conn, {}, {})
    at = r.seq["K3"]
    rows = conn.execute(HISTORY_CELLS_SQL, {"at": at, "subject": "product:P", "property": "unit_price"}).fetchall()
    labels = {(d["from_assertion_ref"], d["knowledge_from"]): d["id"] for d in spec["derived_labels"]}
    mine = {}
    for aid, kfrom, _kind, frm, until, kuntil in rows:
        lex = conn.execute("SELECT v_lexical FROM assertion WHERE id=?", (aid,)).fetchone()[0]
        mine[labels.get((aid, r.pos[kfrom]), f"unlabelled:{aid}@{r.pos[kfrom]}")] = {
            "assertion": aid, "value_cents": int(lex), "valid_from": frm, "valid_until": until,
            "knowledge_from": r.pos[kfrom], "knowledge_until": r.pos.get(kuntil)}
    conn.close()
    fields = ("assertion", "value_cents", "valid_from", "valid_until", "knowledge_from", "knowledge_until")
    diffs = []
    for cell in key:
        got = mine.pop(cell["id"], None)
        if got is None:
            diffs.append(f"{cell['id']}: not derived")
            continue
        diffs += [f"{cell['id']}.{f}: key {cell[f]!r}, witness {got[f]!r}" for f in fields if cell[f] != got[f]]
    diffs += [f"extra cell {k}" for k in mine]
    return {"compared_fields": list(fields), "not_compared": ["basis"], "diffs": diffs}


def sizes(path: Path) -> dict[str, int]:
    conn = store.connect(path, read_only=True)
    names = [n for (n,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    out = {n: conn.execute(f"SELECT COUNT(*) FROM {n}").fetchone()[0] for n in names}
    conn.close()
    return out


def run_specimen(name: str, spec: dict) -> dict:
    ledger = store.canonical_ledger(spec)
    with tempfile.TemporaryDirectory(prefix="g2b-") as tmp:
        tmp = Path(tmp)
        first_dir, second_dir = tmp / "first", tmp / "second"
        first_dir.mkdir()
        second_dir.mkdir()
        first = answer_all(spec, ledger, first_dir)
        conn = store.connect(first_dir / "main.db", read_only=True)
        decoded = store.decode(conn)
        conn.close()
        roundtrip = store.same_graph(decoded, ledger)
        size = sizes(first_dir / "main.db")
        cells = check_cells_against_key(spec, first_dir)
        # delete every database file, rebuild from the decoded change list alone
        for p in first_dir.glob("*.db"):
            p.unlink()
        second = answer_all(spec, decoded, second_dir)
        conn = store.connect(second_dir / "main.db", read_only=True)
        redecoded = store.decode(conn)
        conn.close()
        refusals = check_refusals(spec, ledger, tmp)

    forb = {}
    for i, f in enumerate(spec["forbidden"]):
        forb[i] = {"query_ref": f["query_ref"], "why": f["why"],
                   "runs": {b: forbidden_match(f["answer"], a) for (qid, b), a in first["answers"].items() if qid == f["query_ref"]}}
    rows = []
    for q, branch, _policy, exp in runs_for(spec):
        actual = first["answers"][(q["id"], branch)]
        diffs = compare(exp, actual)
        issue = specimen_issue(q["id"], branch)
        status = "PASS" if not diffs else ("SPECIMEN_ISSUE" if issue else "FAIL")
        rows.append({"query": q["id"], "kind": q["kind"], "choice": q.get("open_choice_ref"), "branch": branch, "status": status,
                     "diffs": diffs, "reason": issue if diffs else None,
                     "rebuild_same": first["answers"][(q["id"], branch)] == second["answers"][(q["id"], branch)],
                     "actual": actual})
    return {
        "specimen": name, "rows": rows, "forbidden": forb, "refusals": refusals,
        "roundtrip_diffs": roundtrip, "rebuild_graph_diffs": store.same_graph(redecoded, ledger),
        "rebuild_answers_same": first["answers"] == second["answers"],
        "queries_wrote_nothing": first["unchanged_by_queries"] and second["unchanged_by_queries"],
        "notes": first["notes"] + second["notes"], "sizes": size, "cells_vs_key": cells,
        "implemented_only": {c["id"]: IMPLEMENTED_BRANCH[c["id"]] for c in spec["open_choices"] if not c["affects_query_refs"]},
    }


def run_all() -> list[dict]:
    return [run_specimen(n, s) for n, s in load_specimens().items()]


# report

def summarize(results: list[dict]) -> str:
    lines = ["| Specimen | Query | Kind | Branch runs | Status |", "|---|---|---|---|---|"]
    for r in results:
        by_q: dict[str, list] = {}
        for row in r["rows"]:
            by_q.setdefault(row["query"], []).append(row)
        for qid, rs in by_q.items():
            statuses = sorted({x["status"] for x in rs})
            if rs[0]["choice"] or len(statuses) > 1:
                br = "; ".join(f"{x['branch']}: {x['status']}" for x in rs)
            elif len(rs) == 1:
                br = "single run"
            else:
                br = f"{len(rs)} runs, every branch combination"
            lines.append(f"| {r['specimen'][:5]} | {qid} | {rs[0]['kind']} | {br} | {'/'.join(statuses)} |")
    lines.append("")
    for r in results:
        counts: dict[str, int] = {}
        for row in r["rows"]:
            counts[row["status"]] = counts.get(row["status"], 0) + 1
        fb = [v for f in r["forbidden"].values() for v in f["runs"].values()]
        lines.append(
            f"{r['specimen']}: runs {counts}; forbidden checks {len(fb)} "
            f"(MATCH {fb.count('MATCH')}, NOT_DISCRIMINATED {fb.count('NOT_DISCRIMINATED')}); "
            f"refusals {[(x['id'], x['status']) for x in r['refusals']]}; roundtrip diffs {len(r['roundtrip_diffs'])}; "
            f"rebuild answers same {r['rebuild_answers_same']}; rebuild graph diffs {len(r['rebuild_graph_diffs'])}; "
            f"queries wrote nothing {r['queries_wrote_nothing']}; notes {r['notes']}")
        if r["cells_vs_key"] is not None:
            lines.append(f"  cells vs answer key: diffs {r['cells_vs_key']['diffs']}, not compared {r['cells_vs_key']['not_compared']}")
        for row in r["rows"]:
            if row["status"] != "PASS":
                lines.append(f"  {row['status']} {row['query']} [{row['branch']}]: {row['diffs']}")
        for f in r["forbidden"].values():
            for b, v in f["runs"].items():
                if v != "NO_MATCH":
                    lines.append(f"  forbidden {f['query_ref']} [{b}]: {v}")
    return "\n".join(lines)


if __name__ == "__main__":
    res = run_all()
    if "json" in sys.argv[1:]:
        print(json.dumps(res, indent=1, default=str))
    else:
        print(summarize(res))
