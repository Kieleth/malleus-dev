"""G2a query layer over the Construction A graph. Research-local, not a Core proposal.

Every query first takes the graph prefix at its knowledge position `at` and
replays the accepted changes of that prefix to derive versions. Nothing later
than `at` is in the prefix, so no later closure can leak into an old read.

Version ids are "version:<assertion>@<position>": one exact assertion as known
from one knowledge position. The runner renders them into the specimen's own
labels; this module never reads a specimen's derived labels.

Selector policy that the specimens leave open is an explicit parameter
(DEFAULT_PARAMS); no ambient default fills a caller input.
"""

from __future__ import annotations

from graph import Graph

DEFAULT_PARAMS = {
    "transition_closure": "NAMED_TARGET",   # OC-01: NAMED_TARGET | INFERRED
    "unscoped_assumptions": "EXCLUDE",      # OC-03 assumptions: EXCLUDE | INCLUDE
    "use_selection": "USE_ONLY",            # OC-03 use selection: USE_ONLY | DEFAULT_AUTHORITY
    "include_groups": "ALWAYS",             # OC-05: ALWAYS | ON_REQUEST
    "flag_source": "DERIVED",               # OC-06 flag: DERIVED | REVIEWER
    "sufficiency": "NONE",                  # OC-06 sufficiency: NONE | ANY_UNREVISED_ROUTE
    "rule_selection": "NAMED_ONLY",         # OC-07: NAMED_ONLY | DEFAULT_IN_SCOPE
    "withheld_scope": "CLOSURE",            # OC-08: CLOSURE | WHOLE
}

# Research-local conventions the specimen format does not declare in data.
# Each is listed in RESULTS.md as a loss or an assumption of this witness.
STATE_EVIDENCE_PROPERTY = {"state": "event"}      # a state is read from event assertions
EVENT_STATE = {"OPENED": "OPEN", "CLOSED": "CLOSED"}  # the one persistence semantics implemented
PLAN_PROPERTY = "plan"                            # PLAN records answer a history under this name
FRAME_QUALIFIERS = ("datum",)                     # qualifiers that make two values incomparable


class QueryError(ValueError):
    """A query this layer cannot answer. Raised, never guessed around."""


def vid(assertion: str, position: str) -> str:
    return f"version:{assertion}@{position}"


def covers(v: dict, t: str) -> bool:
    if v["kind"] == "INTERVAL":
        return v["from"] <= t and (v["until"] is None or t < v["until"])
    if v["kind"] == "INSTANT":
        return v["instant"] == t
    return False


class View:
    """The accepted graph at one knowledge position, with derived versions."""

    def __init__(self, graph: Graph, at: str, params: dict | None = None):
        self.at = at
        self.params = {**DEFAULT_PARAMS, **(params or {})}
        unknown = set(self.params) - set(DEFAULT_PARAMS)
        if unknown:
            raise QueryError(f"unknown selector parameters {sorted(unknown)}")
        self.g = graph.prefix(at)
        self.added_at = self.g.added_at()
        self.versions: dict[str, dict] = {}
        self.superseded_by: dict[str, tuple[str, str, str]] = {}
        self._replay()

    # -- replay ---------------------------------------------------------
    def _stated(self, a: str) -> dict:
        p = self.g.payload(a)
        k = p["applicability_kind"]["lexical"]
        out = {"kind": k, "from": None, "until": None, "instant": None}
        if k == "INTERVAL":
            out["from"] = p["applicability_from"]["lexical"]
            u = p["applicability_until"]
            out["until"] = u["lexical"] if u else None
        elif k == "INSTANT":
            out["instant"] = p["applicability_instant"]["lexical"]
        return out

    def _open(self, a: str, pos: str, app: dict) -> None:
        i = vid(a, pos)
        if i in self.versions:
            raise QueryError(f"two versions of {a} from one position {pos}")
        self.versions[i] = {"id": i, "assertion": a, "knowledge_from": pos, "knowledge_until": None, **app}

    def current(self, a: str) -> list[dict]:
        return [v for v in self.versions.values() if v["assertion"] == a and v["knowledge_until"] is None]

    def _close(self, a: str, pos: str) -> list[dict]:
        closed = self.current(a)
        for v in closed:
            v["knowledge_until"] = pos
        return closed

    def _replay(self) -> None:
        g = self.g
        for row in g.ledger():
            pos = row["position"]
            added = [a for a in row["adds"] if g.has(a) and g.type_of(a) == "ASSERTION"]
            for a in added:
                self._open(a, pos, self._stated(a))
            for a in added:
                for field in ("corrects_ref", "revises_ref"):
                    t = g.ref(a, field)
                    if t is not None:
                        self._close(t, pos)
                        self.superseded_by[t] = (a, pos, field)
            if row["kind"] == "TRANSITION":
                for n in added:
                    new = self._stated(n)
                    if new["kind"] != "INTERVAL":
                        raise QueryError(f"transition {pos} adds {n} without an interval")
                    for t in self._transition_targets(row, n, new):
                        for v in self._close(t, pos):
                            if v["kind"] != "INTERVAL":
                                raise QueryError(f"transition {pos} targets {t}, which has no interval")
                            until = new["from"] if v["until"] is None or v["until"] > new["from"] else v["until"]
                            self._open(t, pos, {"kind": "INTERVAL", "from": v["from"], "until": until,
                                                "instant": None})

    def _transition_targets(self, row: dict, n: str, new: dict) -> list[str]:
        if self.params["transition_closure"] == "NAMED_TARGET":
            return list(row["targets"])
        if self.params["transition_closure"] == "INFERRED":
            g = self.g
            return sorted({v["assertion"] for v in self.versions.values()
                           if v["knowledge_until"] is None and v["assertion"] != n and v["kind"] == "INTERVAL"
                           and v["until"] is None and v["from"] < new["from"]
                           and g.ref(v["assertion"], "subject_ref") == g.ref(n, "subject_ref")
                           and g.lex(v["assertion"], "property") == g.lex(n, "property")
                           and g.ref(v["assertion"], "account_ref") == g.ref(n, "account_ref")})
        raise QueryError(f"transition_closure {self.params['transition_closure']!r} has no branch")

    # -- record access ----------------------------------------------------
    def assertions(self, subject: str, prop: str | None = None) -> list[str]:
        g = self.g
        return [a for a in g.referrers(subject, "subject_ref")
                if g.type_of(a) == "ASSERTION" and (prop is None or g.lex(a, "property") == prop)]

    def accepted(self, i: str, typ: str | None = None) -> bool:
        return self.g.has(i) and (typ is None or self.g.type_of(i) == typ)

    def value(self, i: str):
        v = self.g.payload(i).get("value")
        return dict(v) if v else None

    def stated_applicability(self, a: str) -> dict:
        s = self._stated(a)
        if s["kind"] == "INTERVAL":
            return {"kind": "INTERVAL", "from": s["from"], "until": s["until"]}
        if s["kind"] == "INSTANT":
            return {"kind": "INSTANT", "instant": s["instant"]}
        return {"kind": "NONE_STATED"}

    def qualifiers(self, i: str) -> dict:
        return {k: dict(v) for k, v in self.g.element(i).get("qualifiers", {}).items()}

    def groups_of(self, i: str) -> list[str]:
        return sorted(s for s, members in self.g.subgraphs.items()
                      if i in members and self.g.type_of(s) == "GROUP")

    def changed_premises(self, arg: str) -> list[str]:
        return [p for p in self.g.refs(arg, "premise_refs") if p in self.superseded_by]

    # -- metadata rows ----------------------------------------------------
    def row(self, i: str, include_groups: bool) -> dict:
        g = self.g
        t = g.type_of(i)
        r: dict = {"ref": i, "type": t}
        if t in {"ASSERTION", "RELATION"}:
            r["basis"] = g.lex(i, "basis")
            r.update({k: v["lexical"] for k, v in self.qualifiers(i).items()})
        if t == "RELATION":
            e = g.edges[i]
            r.update(relation_type=e["type"], from_ref=e["from"], to_ref=e["to"])
        if t == "ASSERTION":
            s = self._stated(i)
            r.update(property=g.lex(i, "property"), account_ref=g.ref(i, "account_ref"),
                     valid_from=s["from"], valid_until=s["until"], instant=s["instant"],
                     knowledge_from=self.added_at.get(i))
            mine = [v for v in self.versions.values() if v["assertion"] == i]
            r["knowledge_until"] = None if any(v["knowledge_until"] is None for v in mine) else max(
                (v["knowledge_until"] for v in mine), key=self.g.positions().index)
            if i in self.superseded_by:
                by, _, field = self.superseded_by[i]
                r["revised_by_ref" if field == "revises_ref" else "corrected_by_ref"] = by
        if include_groups:
            groups = self.groups_of(i)
            if groups:
                r["member_of"] = groups[0] if len(groups) == 1 else groups
        return r

    def version_row(self, v: dict) -> dict:
        return {"ref": v["id"], "type": "VERSION", "assertion_ref": v["assertion"],
                "valid_from": v["from"], "valid_until": v["until"], "instant": v["instant"],
                "knowledge_from": v["knowledge_from"], "knowledge_until": v["knowledge_until"]}


# -- closure ------------------------------------------------------------------

def _closure_check(view: View, closure: set) -> dict | None:
    missing = view.g.missing()
    if not missing:
        return None
    if view.params["withheld_scope"] == "WHOLE":
        hit = missing
    elif view.params["withheld_scope"] == "CLOSURE":
        hit = sorted(set(missing) & closure)
    else:
        raise QueryError(f"withheld_scope {view.params['withheld_scope']!r} has no branch")
    return {"state": "INCOMPLETE_RECONSTRUCTION", "missing_refs": hit} if hit else None


def _evidence_closure(view: View, ids) -> set:
    g, out = view.g, set()
    for i in ids:
        out.add(i)
        out.update(g.refs(i, "evidence_refs"))
        c = g.ref(i, "contract_ref")
        if c:
            out.add(c)
    return out


# -- selection ----------------------------------------------------------------

def _candidates(view: View, subject: str, prop: str, account: str | None, context: str | None) -> list[dict]:
    g = view.g
    if context is not None:
        if not view.accepted(context, "CONTEXT"):
            raise QueryError(f"context {context!r} is not accepted at {view.at}")
        bound = [e["to"] for e in g.links(context, "bindings")
                 if e["qualifiers"]["parameter"]["lexical"] == prop and g.ref(e["to"], "subject_ref") == subject]
        return [v for a in bound for v in view.current(a)]
    out = []
    for a in view.assertions(subject, prop):
        if account is not None and g.ref(a, "account_ref") != account:
            continue
        if account is None and g.lex(a, "basis") == "ASSUMPTION":
            mode = view.params["unscoped_assumptions"]
            if mode == "EXCLUDE":
                continue
            if mode != "INCLUDE":
                raise QueryError(f"unscoped_assumptions {mode!r} has no branch")
        out.extend(view.current(a))
    return out


def _default_authority(view: View, subject: str, prop: str) -> str | None:
    """An accepted record declaring a default account for unscoped reads.

    The G1 format has no object type for such a record, so none can exist in
    any specimen graph. A use selection (J1) is scoped to its use and is not one.
    """
    return None


def select_applicable(view: View, inp: dict) -> dict:
    subject, prop, t = inp["subject_ref"], inp["property"], inp["valid_at"]
    account, context = inp.get("account_ref"), inp.get("context_ref")
    if prop in STATE_EVIDENCE_PROPERTY and not view.assertions(subject, prop):
        return _state_from_events(view, inp)
    cands = _candidates(view, subject, prop, account, context)
    if not cands:
        return {"state": "NO_ACCEPTED_ACCOUNT", "selected_refs": [], "unresolved_refs": []}
    covering = [v for v in cands if covers(v, t)]
    unresolved = [v for v in cands if v["kind"] == "NONE_STATED"]
    if account is None and context is None and len({v["assertion"] for v in covering}) > 1:
        if view.params["use_selection"] == "DEFAULT_AUTHORITY":
            chosen = _default_authority(view, subject, prop)
            if chosen is not None:
                covering = [v for v in covering if view.g.ref(v["assertion"], "account_ref") == chosen]
        elif view.params["use_selection"] != "USE_ONLY":
            raise QueryError(f"use_selection {view.params['use_selection']!r} has no branch")
    if len({v["assertion"] for v in covering}) > 1:
        return {"state": "AMBIGUOUS_SELECTION", "candidate_refs": [v["id"] for v in covering],
                "selected_refs": [], "unresolved_refs": []}
    if covering:
        v = covering[0]
        if len(covering) > 1:
            raise QueryError(f"{v['assertion']} has two current versions covering {t}")
        return {"state": "SELECTED", "selected_refs": [v["id"]], "unresolved_refs": [],
                "assertion_refs": [v["assertion"]], "value": view.value(v["assertion"]),
                "basis": view.g.lex(v["assertion"], "basis"),
                "applicability": view.stated_applicability(v["assertion"])}
    if unresolved:
        return {"state": "UNRESOLVED_APPLICABILITY", "selected_refs": [],
                "unresolved_refs": [v["id"] for v in unresolved]}
    return {"state": "NO_APPLICABLE_ACCOUNT", "selected_refs": [], "unresolved_refs": []}


def _state_from_events(view: View, inp: dict) -> dict:
    subject, t = inp["subject_ref"], inp["valid_at"]
    events = [v for a in view.assertions(subject, STATE_EVIDENCE_PROPERTY[inp["property"]]) for v in view.current(a)]
    if not events:
        return {"state": "NO_ACCEPTED_ACCOUNT", "selected_refs": [], "unresolved_refs": []}
    rule = inp.get("persistence_rule_ref")
    if rule is not None:
        if not view.accepted(rule, "RULE"):
            raise QueryError(f"persistence rule {rule!r} is not accepted at {view.at} (OC-07 acceptance: accepted first)")
    elif view.params["rule_selection"] == "DEFAULT_IN_SCOPE":
        in_scope = [r for r in view.g.of_type("RULE") if subject in view.g.refs(r, "scope_refs")]
        if len(in_scope) > 1:
            raise QueryError(f"two accepted rules in scope for {subject}")
        rule = in_scope[0] if in_scope else None
    elif view.params["rule_selection"] != "NAMED_ONLY":
        raise QueryError(f"rule_selection {view.params['rule_selection']!r} has no branch")
    if rule is None or subject not in view.g.refs(rule, "scope_refs"):
        return {"state": "UNRESOLVED_APPLICABILITY", "selected_refs": [], "unresolved_refs": [v["id"] for v in events]}
    if any(v["kind"] != "INSTANT" for v in events):
        raise QueryError("the persistence semantics implemented here reads instant events only")
    before = sorted((v for v in events if v["instant"] <= t), key=lambda v: v["instant"])
    if not before:
        return {"state": "NO_APPLICABLE_ACCOUNT", "selected_refs": [], "unresolved_refs": []}
    last = before[-1]
    if len(before) > 1 and before[-2]["instant"] == last["instant"]:
        raise QueryError("two events at one instant")
    event_value = view.g.lex(last["assertion"], "value")
    if event_value not in EVENT_STATE:
        raise QueryError(f"no state for event value {event_value!r}")
    return {"state": "SELECTED", "selected_refs": [], "unresolved_refs": [],
            "derived_from_refs": [last["assertion"], rule],
            "value": {"datatype": "enum", "lexical": EVENT_STATE[event_value]}}


def _support(view: View, a: str) -> dict | None:
    args = [x for x in view.g.referrers(a, "conclusion_ref") if view.g.type_of(x) == "ARGUMENT"]
    if not args:
        return None
    mode = view.params["sufficiency"]
    if mode == "NONE":
        return {"ref": a, "support_sufficiency": "NOT_ASSESSED"}
    if mode == "ANY_UNREVISED_ROUTE":
        ok = [x for x in args if not view.changed_premises(x)]
        return {"ref": a, "support_sufficiency": "SUPPORTED" if ok else "NOT_SUPPORTED", "supporting_refs": ok}
    raise QueryError(f"sufficiency {mode!r} has no branch")


def select_account(view: View, inp: dict) -> dict:
    subject, prop, account = inp["subject_ref"], inp["property"], inp.get("account_ref")
    cands = _candidates(view, subject, prop, account, None)
    names = sorted({v["assertion"] for v in cands})
    if not cands:
        return {"state": "NO_ACCEPTED_ACCOUNT", "selected_refs": [], "unresolved_refs": []}
    if len(names) > 1:
        return {"state": "AMBIGUOUS_SELECTION", "candidate_refs": [v["id"] for v in cands], "selected_refs": []}
    a = names[0]
    out = {"state": "SELECTED", "selected_refs": [v["id"] for v in cands], "assertion_refs": [a],
           "value": view.value(a), "basis": view.g.lex(a, "basis"),
           "applicability": view.stated_applicability(a), "metadata": []}
    s = _support(view, a)
    if s:
        out["metadata"].append(s)
    return out


# -- inspection -----------------------------------------------------------------

def inspect_history(view: View, inp: dict) -> dict:
    g = view.g
    if _closure_check(view, set(g.missing())):
        return _closure_check(view, set(g.missing()))
    if inp.get("target_ref") is not None:
        return _arguments_for(view, inp["target_ref"])
    subject, prop = inp["subject_ref"], inp.get("property")
    if prop == PLAN_PROPERTY:
        plans = [p for p in g.referrers(subject, "subject_ref") if g.type_of(p) == "PLAN"]
        return {"state": "QUALIFIED_HISTORY", "visible_refs": plans,
                "metadata": [view.row(p, True) for p in plans]}
    found = view.assertions(subject, prop)
    rels = [] if prop is not None else sorted(
        i for i, e in g.edges.items() if e["class"] == "RELATION" and subject in (e["from"], e["to"]))
    versions = [v for v in view.versions.values() if v["assertion"] in found]
    kinds = {view._stated(a)["kind"] for a in found}
    out = {"state": "QUALIFIED_HISTORY", "visible_refs": found + rels + [v["id"] for v in versions],
           "metadata": [view.row(i, True) for i in found + rels] + [view.version_row(v) for v in versions],
           "domain_time": None if not kinds else (kinds.pop() if len(kinds) == 1 else "MIXED")}
    if inp.get("attempted_refs") is not None:
        out["absent_refs"] = [i for i in inp["attempted_refs"] if not g.has(i)]
    return out


def _arguments_for(view: View, target: str) -> dict:
    g = view.g
    args = [x for x in g.referrers(target, "conclusion_ref") if g.type_of(x) == "ARGUMENT"]
    changed = {x: view.changed_premises(x) for x in args}
    mode, rows = view.params["flag_source"], []
    for x in args:
        if mode == "DERIVED":
            flag = "REQUIRED" if changed[x] else "NOT_REQUIRED"
        elif mode == "REVIEWER":
            # Reading chosen here (see RESULTS.md): the review unit is the conclusion.
            # With no changed premise under any argument nothing awaits review;
            # once one exists, every argument for it awaits a recorded review.
            flag = "NOT_RECORDED" if any(changed.values()) else "NOT_REQUIRED"
        else:
            raise QueryError(f"flag_source {mode!r} has no branch")
        rows.append({"ref": x, "type": "ARGUMENT", "reconsideration": flag, "changed_premise_refs": changed[x],
                     "premise_refs": g.refs(x, "premise_refs")})
    return {"state": "QUALIFIED_HISTORY", "visible_refs": args, "metadata": rows}


def exact_lookup(view: View, inp: dict) -> dict:
    g, target = view.g, inp["target_ref"]
    members = list(g.subgraphs.get(target, [])) if g.type_of(target) in {"GROUP", "MODEL"} else []
    fail = _closure_check(view, _evidence_closure(view, [target]) | set(members))
    if fail:
        return fail
    if not g.has(target):
        return {"state": "NO_ACCEPTED_ACCOUNT"}
    groups_on = view.params["include_groups"] == "ALWAYS" or inp.get("include_groups") is True
    if view.params["include_groups"] not in {"ALWAYS", "ON_REQUEST"}:
        raise QueryError(f"include_groups {view.params['include_groups']!r} has no branch")
    out: dict = {"state": "EXACT_OBJECT", "type": g.type_of(target)}
    p = g.payload(target)
    if "value" in p:
        out["value"] = view.value(target)
    if g.type_of(target) == "ASSERTION":
        out["applicability"] = view.stated_applicability(target)
    if "basis" in p:
        out["basis"] = g.lex(target, "basis")
    if "evidence_refs" in p:
        out["evidence_refs"] = g.refs(target, "evidence_refs")
    if g.element(target).get("qualifiers") is not None and "qualifiers" in p:
        out["qualifiers"] = view.qualifiers(target)
    visible = []
    if members:
        visible = members + sorted(i for i, e in g.edges.items() if e["class"] == "RELATION" and e["from"] == target)
        out["visible_refs"] = visible
    out["metadata"] = [view.row(i, groups_on) for i in [target] + visible if g.has(i)]
    return out


# -- computation ----------------------------------------------------------------

def _results_of(view: View, execution: str) -> list[str]:
    return [r for r in view.g.referrers(execution, "execution_ref") if view.g.type_of(r) == "RESULT"]


def _bindings(g: Graph, owner: str, field: str) -> dict:
    return {e["qualifiers"]["parameter"]["lexical"]: e["to"] for e in g.links(owner, field)}


def result_for_context(view: View, inp: dict) -> dict:
    g, ctx = view.g, inp["context_ref"]
    if not view.accepted(ctx, "CONTEXT"):
        raise QueryError(f"context {ctx!r} is not accepted at {view.at}")
    want_model, want = g.ref(ctx, "model_ref"), _bindings(g, ctx, "bindings")
    for x in g.of_type("EXECUTION"):
        if (g.ref(x, "context_ref") == ctx and g.ref(x, "model_ref") == want_model
                and _bindings(g, x, "input_bindings") == want):
            results = _results_of(view, x)
            if len(results) > 1:
                raise QueryError(f"execution {x} has two results")
            if results:
                return {"state": "COMPUTED", "execution_ref": x, "result_ref": results[0], "value": view.value(results[0])}
    return {"state": "NOT_COMPUTED"}


def _reselect(view: View, assertion: str, valid_at: str | None, account: str | None) -> dict:
    g = view.g
    inp = {"subject_ref": g.ref(assertion, "subject_ref"), "property": g.lex(assertion, "property"),
           "account_ref": account if account is not None else g.ref(assertion, "account_ref")}
    if valid_at is None:
        return select_account(view, inp)
    return select_applicable(view, {**inp, "valid_at": valid_at})


def result_for_selection(view: View, inp: dict) -> dict:
    g, model = view.g, inp.get("model_ref")
    if model is None:
        return {"state": "NOT_COMPUTED", "reason": "no executable model named"}
    if not view.accepted(model, "MODEL"):
        return {"state": "NOT_COMPUTED", "reason": f"{model} is not an accepted executable model"}
    for x in g.of_type("EXECUTION"):
        if g.ref(x, "model_ref") != model:
            continue
        same = all(_reselect(view, a, inp.get("valid_at"), inp.get("account_ref")).get("assertion_refs") == [a]
                   for a in _bindings(g, x, "input_bindings").values())
        results = _results_of(view, x)
        if same and results:
            return {"state": "COMPUTED", "execution_ref": x, "result_ref": results[0], "value": view.value(results[0])}
    return {"state": "NOT_COMPUTED", "reason": "no accepted execution of this model over the selected premises"}


def explain_execution(view: View, inp: dict, graph: Graph) -> dict:
    g, x = view.g, inp["execution_ref"]
    links = g.links(x, "input_bindings") if g.has(x) else []
    premises = [e["to"] for e in links]
    model = g.ref(x, "model_ref") if g.has(x) else None
    results = _results_of(view, x)
    closure = _evidence_closure(view, [x] + premises + results) | {model} | set(g.subgraphs.get(model, []))
    closure.discard(None)
    fail = _closure_check(view, closure)
    if fail:
        return fail
    out = {"state": "ORIGINAL_PREMISES_PRESERVED", "premise_refs": premises, "model_ref": model,
           "result_ref": results[0] if results else None,
           "value": view.value(results[0]) if results else None}
    selections = [(e, e["qualifiers"]) for e in links if "selection_at" in e["qualifiers"]]
    if selections:
        ats = {q["selection_at"]["lexical"] for _, q in selections}
        out["selection_at"] = ats.pop() if len(ats) == 1 else sorted(ats)
        cells, reproduced = [], True
        for e, q in selections:
            old = View(graph, q["selection_at"]["lexical"], view.params)
            valid_at = q["selection_valid_at"]["lexical"] if "selection_valid_at" in q else None
            got = _reselect(old, e["to"], valid_at, g.ref(e["id"], "selection.account_ref"))
            cells.extend(got.get("selected_refs", []))
            reproduced &= got.get("assertion_refs") == [e["to"]]
        out["cell_refs"] = cells
        out["selection_reproduced"] = reproduced
    return out


def compare_premises(view: View, inp: dict) -> dict:
    g = view.g
    if inp.get("execution_ref") is not None:
        previous, new, cells = [], [], []
        for e in g.links(inp["execution_ref"], "input_bindings"):
            account = inp.get("account_ref") or g.ref(e["id"], "selection.account_ref")
            got = _reselect(view, e["to"], inp.get("valid_at"), account)
            previous.append(e["to"])
            new.extend(got.get("assertion_refs", []))
            cells.extend(got.get("selected_refs", []))
        if previous == new:
            return {"state": "SAME_PREMISES", "previous_refs": previous, "new_refs": new, "new_cell_refs": cells}
        return {"state": "SELECTED_PREMISES_CHANGED", "previous_refs": previous, "new_refs": new, "new_cell_refs": cells}
    refs = inp["premise_refs"]
    for r in refs:
        if not g.has(r):
            raise QueryError(f"premise {r!r} is not accepted at {view.at}")
    rows = [view.row(r, True) for r in refs]
    if len(set(refs)) == 1:
        return {"state": "SAME_PREMISES", "metadata": rows}
    return {"state": "DIFFERENT_PREMISES", "metadata": rows}


def prepare_inputs(view: View, inp: dict) -> dict:
    g, refs = view.g, inp["premise_refs"]
    for r in refs:
        if not view.accepted(r, "ASSERTION"):
            raise QueryError(f"premise {r!r} is not an accepted assertion at {view.at}")
    if inp.get("model_ref") is not None and not view.accepted(inp["model_ref"], "MODEL"):
        raise QueryError(f"model {inp['model_ref']!r} is not an accepted model at {view.at}")
    apps = {r: (view.current(r) or [view.versions[vid(r, view.added_at[r])]]) for r in refs}
    if inp.get("valid_at") is not None:
        unresolved = [r for r in refs if any(v["kind"] == "NONE_STATED" for v in apps[r])]
        if unresolved:
            return {"state": "UNRESOLVED_REQUIRED_PREMISE", "unresolved_refs": unresolved}
    if inp.get("same_time"):
        lo, hi = None, None
        for r in refs:
            if len(apps[r]) != 1 or apps[r][0]["kind"] != "INTERVAL":
                return {"state": "UNRESOLVED_REQUIRED_PREMISE", "unresolved_refs": [r]}
            v = apps[r][0]
            lo = v["from"] if lo is None or v["from"] > lo else lo
            if v["until"] is not None:
                hi = v["until"] if hi is None or v["until"] < hi else hi
        if hi is not None and lo >= hi:
            return {"state": "NO_COMMON_APPLICABILITY"}
    by_prop: dict[str, list[str]] = {}
    for r in refs:
        by_prop.setdefault(g.lex(r, "property"), []).append(r)
    for same in by_prop.values():
        frames = {(view.value(r).get("unit"),) + tuple(
            (view.qualifiers(r).get(q) or {}).get("lexical") for q in FRAME_QUALIFIERS) for r in same}
        if len(frames) > 1:
            return {"state": "INCOMPATIBLE_CONTEXTS", "conflict_refs": same}
    conditions = [r for r in refs if (view.qualifiers(r).get("role") or {}).get("lexical") == "CONDITION"]
    groups = sorted({grp for r in conditions for grp in view.groups_of(r)})
    if len(groups) > 1:
        return {"state": "INCOMPATIBLE_CONTEXTS", "conflict_refs": groups}
    return {"state": "INPUTS_READY"}


def run_query(graph: Graph, kind: str, inputs: dict, params: dict | None = None) -> dict:
    """Answer one query. graph is the accepted graph; nothing is written to it."""
    view = View(graph, inputs["at"], params)
    if kind == "SELECT_APPLICABLE":
        fail = _closure_check(view, set(view.g.missing()))
        return fail or select_applicable(view, inputs)
    if kind == "SELECT_ACCOUNT":
        fail = _closure_check(view, set(view.g.missing()))
        return fail or select_account(view, inputs)
    if kind == "INSPECT_HISTORY":
        return inspect_history(view, inputs)
    if kind == "EXACT_LOOKUP":
        return exact_lookup(view, inputs)
    if kind == "RESULT_FOR_CONTEXT":
        return result_for_context(view, inputs)
    if kind == "RESULT_FOR_SELECTION":
        return result_for_selection(view, inputs)
    if kind == "EXPLAIN_EXECUTION":
        return explain_execution(view, inputs, graph)
    if kind == "COMPARE_PREMISES":
        return compare_premises(view, inputs)
    if kind == "PREPARE_INPUTS":
        return prepare_inputs(view, inputs)
    raise QueryError(f"no query kind {kind!r}")
