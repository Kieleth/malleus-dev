#!/usr/bin/env python3
"""G2a runner: every G1 query, branch, forbidden answer, refusal, round trip and rebuild.

Usage: python runner.py [--markdown]
Exit 0 when every outcome equals its recorded status, 1 otherwise.

Expected answers come only from the specimen files. The runner renders this
witness's version ids into a specimen's own vocabulary before comparing: a
version whose (assertion, knowledge position) the specimen labels in
derived_labels becomes that label; any other version becomes its assertion id.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from admission import admit  # noqa: E402
from graph import Graph, decode, encode  # noqa: E402
from query import run_query  # noqa: E402

G1 = HERE.parent / "g1"

# Open choice branches as explicit selector parameters, matched by label.
# None: no parameter in this witness, and no query is affected.
BRANCH_PARAMS = {
    "OC-01-TRANSITION-CLOSES-REPORT": [({"transition_closure": "NAMED_TARGET"}, "Transition names its target"),
                                       ({"transition_closure": "INFERRED"}, "Closure inferred from account")],
    "OC-03-ASSUMPTIONS-IN-UNSCOPED": [({"unscoped_assumptions": "EXCLUDE"}, "Assumptions enter only"),
                                      ({"unscoped_assumptions": "INCLUDE"}, "Every accepted account")],
    "OC-03-USE-SELECTION-SCOPE": [({"use_selection": "USE_ONLY"}, "A use selection binds only"),
                                  ({"use_selection": "DEFAULT_AUTHORITY"}, "An adopter-declared default")],
    "OC-05-GROUP-OR-MEMBER": [({"include_groups": "ALWAYS"}, "Membership always returned"),
                              ({"include_groups": "ON_REQUEST"}, "Membership returned on request")],
    "OC-06-FLAG-SOURCE": [({"flag_source": "DERIVED"}, "Derived from declared premises"),
                          ({"flag_source": "REVIEWER"}, "Recorded by a reviewer")],
    "OC-06-SUFFICIENCY": [({"sufficiency": "NONE"}, "No declared sufficiency rule"),
                          ({"sufficiency": "ANY_UNREVISED_ROUTE"}, "Declared rule: any argument")],
    "OC-07-RULE-SELECTION": [({"rule_selection": "NAMED_ONLY"}, "Only when named"),
                             ({"rule_selection": "DEFAULT_IN_SCOPE"}, "By default within its scope")],
    "OC-07-RULE-ACCEPTANCE": None,
    "OC-07-COMPLETENESS-AUTHORITY": None,
    "OC-07-INITIAL-STATE": None,
    "OC-08-WITHHELD-SCOPE": [({"withheld_scope": "CLOSURE"}, "Only reads whose closure"),
                             ({"withheld_scope": "WHOLE"}, "Any missing retained artifact")],
}

# Branch-note instructions for query inputs, quoted from the specimen notes.
BRANCH_INPUTS = {("OC-05-GROUP-OR-MEMBER", 1): {"CC02": {"include_groups": True}}}

# Outcomes that are not PASS, each with its reason. A listed outcome that turns
# into a PASS, or any unlisted mismatch, fails the run.
FINDINGS = {
    ("G1-03-COMPETING-ACCOUNTS", "CA08", "OC-03-USE-SELECTION-SCOPE[1]"): (
        "SPECIMEN_ISSUE",
        "The branch expects SELECTED Q2, but its own note says this needs an explicit declared authority "
        "record and that J1 is not that record. The specimen contains no such record, and the G1 format has "
        "no object type for one. This witness returns AMBIGUOUS_SELECTION [Q1, Q2]. Reaching Q2 would mean "
        "treating J1 as the authority, which the note excludes."),
}

# Refusals whose observed category differs from the specimen's, with the reason
# and an optional diagnostic: the same attempt with extra accepted-object ids added.
REFUSAL_FINDINGS = {
    ("G1-01-PRICE-HISTORY", "RF-OVERLAP"): (
        "SPECIMEN_ISSUE",
        "The attempted correction r3-overlap cites src:r3 as evidence, but src:r3 is accepted only at K3 and "
        "the attempt is made at head K2 without it. The format cannot add src:r3 to the attempt, because "
        "would_add_refs names rejected objects only. This witness refuses the whole change, head unchanged, "
        "with UNKNOWN_REFERENCE, which it checks before interval semantics.",
        ["src:r3"]),
}


def load_specimens() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(G1.glob("g1-*.json"))]


# -- rendering and comparison ----------------------------------------------------

def renderer(spec: dict):
    labels = {(d["from_assertion_ref"], d["knowledge_from"]): d["id"] for d in spec.get("derived_labels", [])}

    def one(i):
        if isinstance(i, str) and i.startswith("version:"):
            a, pos = i[len("version:"):].rsplit("@", 1)
            return labels.get((a, pos), a), (a, pos) in labels
        return i, True

    def render(ans):
        out = {}
        for k, v in ans.items():
            if k == "metadata":
                rows = []
                for r in v:
                    ref, labelled = one(r["ref"])
                    if labelled:
                        rows.append({**{kk: _render_value(kk, vv, one) for kk, vv in r.items()}, "ref": ref})
                out[k] = rows
            else:
                out[k] = _render_value(k, v, one)
        return out
    return render


def _render_value(k, v, one):
    if k.endswith("_refs") and isinstance(v, list):
        seen = []
        for i in v:
            r = one(i)[0]
            if r not in seen:
                seen.append(r)
        return seen
    if (k == "ref" or k.endswith("_ref")) and isinstance(v, str):
        return one(v)[0]
    return v


def _ids(node) -> set:
    """Every id held under a ref key, anywhere in an answer."""
    out = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if (k == "ref" or k.endswith("_ref")) and isinstance(v, str):
                out.add(v)
            elif k.endswith("_refs") and isinstance(v, list):
                out.update(i for i in v if isinstance(i, str))
            else:
                out |= _ids(v)
    elif isinstance(node, list):
        for v in node:
            out |= _ids(v)
    return out


def _eq(k, mine, want):
    if k.endswith("_refs") and isinstance(want, list):
        return isinstance(mine, list) and sorted(set(mine)) == sorted(set(want)) and len(mine) == len(set(mine))
    return mine == want


def matches(answer: dict, partial: dict) -> list[str]:
    """Fields of partial that answer does not equal. Empty list: every field matches."""
    diffs = []
    for k, want in partial.items():
        if k == "metadata":
            rows = {r["ref"]: r for r in answer.get("metadata", [])}
            for w in want:
                mine = rows.get(w["ref"])
                if mine is None:
                    diffs.append(f"metadata row {w['ref']} absent")
                    continue
                for f, fv in w.items():
                    if f != "ref" and not _eq(f, mine.get(f), fv):
                        diffs.append(f"metadata {w['ref']}.{f}: got {mine.get(f)!r}, want {fv!r}")
        elif not _eq(k, answer.get(k), want):
            diffs.append(f"{k}: got {answer.get(k)!r}, want {want!r}")
    return diffs


# -- execution --------------------------------------------------------------------

class Runner:
    def __init__(self, spec: dict):
        self.spec = spec
        self.render = renderer(spec)
        self.objects = {o["id"]: o for o in spec["objects"] + spec.get("rejected_objects", [])}
        self.refusals = {r["id"]: r for r in spec["refusals"]}
        self.queries = {q["id"]: q for q in spec["queries"]}

    def attempt(self, graph: Graph, refusal: dict, params=None, extra_adds=()):
        head_graph = graph.prefix(refusal["head"])
        adds = list(extra_adds) + refusal["would_add_refs"]
        change = {"position": f"attempt-{refusal['id']}", "kind": "ATTEMPT", "adds_refs": adds}
        if refusal.get("target_refs"):
            change["target_refs"] = refusal["target_refs"]
        before = head_graph.dumps()
        new, refused = admit(head_graph, change, [self.objects[i] for i in adds],
                             refusal.get("base"), params)
        return head_graph, before, new, refused

    def answer(self, graph: Graph, q: dict, params=None, extra_inputs=None) -> dict:
        inputs = {**q["inputs"], **(extra_inputs or {})}
        if inputs.get("withheld_refs"):
            objs, changes = decode(graph)
            graph = encode(objs, changes, withheld=inputs["withheld_refs"])
        if inputs.get("after_refusal_ref"):
            head_graph, _, _, refused = self.attempt(graph, self.refusals[inputs["after_refusal_ref"]], params)
            if refused is None:
                raise AssertionError(f"{inputs['after_refusal_ref']} was admitted")
            graph = head_graph
            inputs["attempted_refs"] = self.refusals[inputs["after_refusal_ref"]]["would_add_refs"]
        return run_query(graph, q["kind"], inputs, params)

    def cases(self):
        """(query, branch label, params, extra inputs, expected) for every expected answer."""
        choices = {c["id"]: c for c in self.spec["open_choices"]}
        for q in self.spec["queries"]:
            if q["expected"] is not None:
                yield q, None, {}, None, q["expected"]
                continue
            c = choices[q["open_choice_ref"]]
            table = BRANCH_PARAMS[c["id"]]
            for bi, b in enumerate(c["branches"]):
                params, label = table[bi]
                assert b["label"].startswith(label), (c["id"], b["label"], label)
                yield (q, f"{c['id']}[{bi}]", params, BRANCH_INPUTS.get((c["id"], bi), {}).get(q["id"]),
                       b["expected"][q["id"]])

    def run_queries(self, graph: Graph) -> list[dict]:
        rows = []
        for q, branch, params, extra, expected in self.cases():
            raw = self.answer(graph, q, params, extra)
            got = self.render(raw)
            diffs = matches(got, expected)
            key = (self.spec["specimen_id"], q["id"], branch)
            status = "PASS" if not diffs else "FAIL"
            reason = "; ".join(diffs)
            if key in FINDINGS:
                listed, why = FINDINGS[key]
                status = listed if diffs else "FINDING_NOT_REPRODUCED"
                reason = why + (" Observed: " + "; ".join(diffs) if diffs else "")
            unlabelled = sorted({i for i in _ids(raw) if i.startswith("version:") and _ids(got).isdisjoint({i})
                                 and self.render({"x_ref": i})["x_ref"] == i[len("version:"):].rsplit("@", 1)[0]})
            rows.append({"specimen": self.spec["specimen_id"], "query": q["id"], "kind": q["kind"],
                         "unlabelled_versions": unlabelled,
                         "branch": branch, "status": status, "reason": reason, "answer": got, "raw": raw})
        return rows

    def branch_invariance(self, graph: Graph) -> list[dict]:
        """Every query not affected by an open choice gives its expected answer under every branch."""
        out = []
        for c in self.spec["open_choices"]:
            table = BRANCH_PARAMS[c["id"]]
            if table is None:
                out.append({"choice": c["id"], "branch": None, "checked": 0, "deviations": [],
                            "note": "no selector parameter in this witness; no query affected"})
                continue
            for bi, (params, _) in enumerate(table):
                checked, dev = 0, []
                for q in self.spec["queries"]:
                    if q["expected"] is None or q["id"] in c["affects_query_refs"]:
                        continue
                    extra = BRANCH_INPUTS.get((c["id"], bi), {}).get(q["id"])
                    diffs = matches(self.render(self.answer(graph, q, params, extra)), q["expected"])
                    checked += 1
                    if diffs:
                        dev.append((q["id"], diffs))
                out.append({"choice": c["id"], "branch": bi, "checked": checked, "deviations": dev})
        return out

    def forbidden(self, rows: list[dict]) -> list[dict]:
        out = []
        for f in self.spec["forbidden"]:
            for r in rows:
                if r["query"] == f["query_ref"]:
                    hit = not matches(r["answer"], f["answer"])
                    out.append({"query": f["query_ref"], "branch": r["branch"], "hit": hit, "why": f["why"]})
        return out

    def run_refusals(self, graph: Graph) -> list[dict]:
        out = []
        full_before = graph.dumps()
        for r in self.spec["refusals"]:
            head_graph, before, new, refused = self.attempt(graph, r)
            row = {"refusal": r["id"], "expected": r["category"], "got": refused[0] if refused else None,
                   "detail": refused[1] if refused else "ADMITTED",
                   "unchanged": head_graph.dumps() == before and graph.dumps() == full_before,
                   "head_after": head_graph.head(), "want_head_after": r["head_after"],
                   "new_graph_returned": new is not None, "status": "PASS", "reason": ""}
            if row["got"] != row["expected"]:
                row["status"] = "FAIL"
            finding = REFUSAL_FINDINGS.get((self.spec["specimen_id"], r["id"]))
            if finding:
                listed, why, extra = finding
                _, before2, new2, refused2 = self.attempt(graph, r, extra_adds=extra)
                diag = f" Diagnostic: with {extra} added to the attempt, the witness refuses {refused2[0] if refused2 else 'nothing (ADMITTED)'}."
                row["status"] = listed if row["got"] != row["expected"] else "FINDING_NOT_REPRODUCED"
                row["reason"] = why + diag
                row["diagnostic_category"] = refused2[0] if refused2 else None
            out.append(row)
        return out

    def positive_control(self) -> list[str]:
        """Every accepted change admits against the graph built by the changes before it."""
        failures = []
        changes = self.spec["changes"]
        for k in range(1, len(changes)):
            before = encode(self.spec["objects"], changes[:k])
            new, refused = admit(before, changes[k], [self.objects[i] for i in changes[k]["adds_refs"]], None)
            if refused:
                failures.append(f"{changes[k]['position']}: {refused}")
            elif new.dumps() != encode(self.spec["objects"], changes[:k + 1]).dumps():
                failures.append(f"{changes[k]['position']}: admitted graph differs from the encoder's")
        return failures

    def storage(self) -> dict:
        """Round trip through canonical JSON, and rebuild from the change list alone."""
        spec = self.spec
        g = encode(spec["objects"], spec["changes"])
        text = g.dumps()
        g2 = Graph.loads(text)
        objs2, changes2 = decode(g2)
        want = {o["id"]: o for o in spec["objects"]}
        got = {o["id"]: o for o in objs2}
        object_diffs = sorted(i for i in set(want) | set(got) if want.get(i) != got.get(i))
        answers = self._all_answers(g)
        rebuilt = encode(spec["objects"], spec["changes"])  # fresh, from the change list
        rebuilt_from_decoded = encode(objs2, changes2)
        leaks = self._prefix_equivalence(g)
        after_queries = g.dumps()
        return {
            "nodes": len(g.nodes), "edges": len(g.edges), "subgraphs": len(g.subgraphs), "bytes": len(text),
            "reserialize_identical": g2.dumps() == text,
            "object_diffs": object_diffs,
            "changes_identical": changes2 == spec["changes"],
            "roundtrip_answers_identical": self._all_answers(g2) == answers,
            "rebuild_identical": rebuilt.dumps() == text and rebuilt_from_decoded.dumps() == text,
            "rebuild_answers_identical": self._all_answers(rebuilt) == answers,
            "answers_compared": len(answers),
            "prefix_mismatches": leaks,
            "queries_wrote_nothing": after_queries == text,
        }

    def _all_answers(self, graph: Graph) -> list:
        return [(q["id"], b, self.answer(graph, q, p, x)) for q, b, p, x, _ in self.cases()]

    def _prefix_equivalence(self, g: Graph) -> list[str]:
        """A read at position P on the full graph equals the read on a graph that never saw later changes."""
        index = {c["position"]: k for k, c in enumerate(self.spec["changes"])}
        bad = []
        for q, b, p, x, _ in self.cases():
            if q["inputs"].get("after_refusal_ref"):
                continue
            k = index[q["inputs"]["at"]]
            only_prefix = encode(self.spec["objects"], self.spec["changes"][:k + 1])
            if self.answer(g, q, p, x) != self.answer(only_prefix, q, p, x):
                bad.append(f"{q['id']} {b}")
        return bad


def run_all() -> dict:
    report = {"specimens": []}
    for spec in load_specimens():
        r = Runner(spec)
        g = encode(spec["objects"], spec["changes"])
        rows = r.run_queries(g)
        report["specimens"].append({
            "id": spec["specimen_id"], "rows": rows, "forbidden": r.forbidden(rows),
            "refusals": r.run_refusals(g), "positive_control": r.positive_control(),
            "branch_invariance": r.branch_invariance(g), "storage": r.storage()})
    return report


def problems(report: dict) -> list[str]:
    out = []
    for s in report["specimens"]:
        for row in s["rows"]:
            if row["status"] == "FAIL" or row["status"] == "FINDING_NOT_REPRODUCED":
                out.append(f"{s['id']} {row['query']} {row['branch']}: {row['status']} {row['reason']}")
        for f in s["forbidden"]:
            if f["hit"]:
                out.append(f"{s['id']} {f['query']} {f['branch']}: forbidden answer given ({f['why']})")
        for r in s["refusals"]:
            if r["status"] in {"FAIL", "FINDING_NOT_REPRODUCED"} or r["got"] is None or not r["unchanged"] or r["head_after"] != r["want_head_after"] or r["new_graph_returned"]:
                out.append(f"{s['id']} {r['refusal']}: {r}")
        out += [f"{s['id']} positive control {p}" for p in s["positive_control"]]
        for b in s["branch_invariance"]:
            for qid, d in b["deviations"]:
                out.append(f"{s['id']} {qid} changes under {b['choice']}[{b['branch']}]: {d}")
        st = s["storage"]
        for k in ("reserialize_identical", "changes_identical", "roundtrip_answers_identical",
                  "rebuild_identical", "rebuild_answers_identical", "queries_wrote_nothing"):
            if not st[k]:
                out.append(f"{s['id']} storage {k} is false")
        if st["object_diffs"]:
            out.append(f"{s['id']} storage objects differ after round trip: {st['object_diffs']}")
        if st["prefix_mismatches"]:
            out.append(f"{s['id']} prefix mismatches: {st['prefix_mismatches']}")
    return out


def summary(report: dict) -> str:
    lines = []
    for s in report["specimens"]:
        counts = {}
        for row in s["rows"]:
            counts[row["status"]] = counts.get(row["status"], 0) + 1
        st = s["storage"]
        lines.append(f"{s['id']}: {len(s['rows'])} answers {counts}; forbidden {len(s['forbidden'])} checked, "
                     f"{sum(f['hit'] for f in s['forbidden'])} hit; refusals {len(s['refusals'])}, "
                     f"{sum(r['got'] == r['expected'] and r['unchanged'] for r in s['refusals'])} as expected and unchanged; "
                     f"graph {st['nodes']} nodes {st['edges']} edges {st['subgraphs']} subgraphs; "
                     f"branch-invariance checks {sum(b['checked'] for b in s['branch_invariance'])}; "
                     f"unlabelled versions rendered to their assertion {sum(len(r['unlabelled_versions']) for r in s['rows'])}")
        for row in s["rows"]:
            if row["status"] != "PASS":
                lines.append(f"  {row['query']} {row['branch']}: {row['status']}: {row['reason']}")
        for r in s["refusals"]:
            lines.append(f"  refusal {r['refusal']}: expected {r['expected']}, got {r['got']}, graph unchanged "
                         f"{r['unchanged']}, head {r['head_after']}: {r['status']} {r['reason']}")
    return "\n".join(lines)


def markdown_table(report: dict) -> str:
    lines = ["| Specimen | Query | Kind | Branch | Status |", "|---|---|---|---|---|"]
    for s in report["specimens"]:
        for row in s["rows"]:
            lines.append(f"| {s['id']} | {row['query']} | {row['kind']} | {row['branch'] or ''} | {row['status']} |")
    return "\n".join(lines)


def main(argv) -> int:
    report = run_all()
    print(markdown_table(report) if "--markdown" in argv else summary(report))
    bad = problems(report)
    for p in bad:
        print("PROBLEM", p)
    print(f"{len(bad)} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
