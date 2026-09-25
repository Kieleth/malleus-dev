"""G2a admission witness: one proposed change is accepted whole or refused whole.

Research-local. This is not Core admission and runs no Core check; it shows
that this graph encoding can refuse the specimens' write attempts before any
record is added, and that a refused attempt leaves the graph byte-identical.

Check order, and why it is this order:
1. STALE_TARGET: a target the change revises or corrects was already revised
   or corrected at the head. Checked first: the change's premise is gone.
2. STALE_BASE: the change was prepared against a position behind the head.
3. Per object, over every object of the change: MISSING_CONTRACT, MISSING_MODEL,
   UNSUPPORTED_SEMANTICS (applicability kind), MISSING_EVIDENCE, then
   UNKNOWN_REFERENCE for any other reference that resolves to nothing accepted
   and nothing in the same change.
4. Change semantics: PREMISE_MISMATCH (an execution's inputs differ from the
   bindings of the context it claims), UNSUPPORTED_SEMANTICS (a correction whose
   period is not exactly the current period of its target: splitting excluded).
"""

from __future__ import annotations

import copy

from graph import APPLICABILITY_KINDS, COMMON, FIELDS, EncodingError, Graph, apply_change
from query import View


def object_refs(obj: dict):
    """(field, id) for every reference an object holds, by its field kinds."""
    spec = {**FIELDS.get(obj["type"], {}), **COMMON}
    for field, kind in spec.items():
        val = obj.get(field)
        if val is None:
            continue
        if kind in {"ref", "edge_from", "edge_to"}:
            yield field, val
        elif kind in {"refs", "members"}:
            for r in val:
                yield field, r
        elif kind == "binds":
            for b in val:
                yield field, b.get("assertion_ref")
                sel = b.get("selection") or {}
                if "account_ref" in sel:
                    yield field + ".selection.account_ref", sel["account_ref"]


def admit(graph: Graph, change: dict, objs: list[dict], base: str | None, params: dict | None = None):
    """Return (new_graph, None) when accepted, or (None, (category, detail)) when refused.

    Never mutates graph. change: {position, kind, adds_refs, target_refs?}.
    """
    head = graph.head()
    view = View(graph, head, params)
    here = {o["id"] for o in objs}
    targets = list(change.get("target_refs") or [])
    for o in objs:
        targets += [o[f] for f in ("corrects_ref", "revises_ref") if o.get(f)]
    for t in targets:
        if t in view.superseded_by:
            by, pos, _ = view.superseded_by[t]
            return None, ("STALE_TARGET", f"{t} was already superseded by {by} at {pos}")
    if base is not None and base != head:
        return None, ("STALE_BASE", f"prepared at {base}, head is {head}")

    def accepted_type(i):
        return graph.type_of(i) if graph.has(i) else None

    for o in objs:
        c = o.get("contract_ref")
        if c is not None and accepted_type(c) != "CONTRACT":
            return None, ("MISSING_CONTRACT", f"{o['id']} names {c}, not an accepted contract")
        if o.get("type") == "EXECUTION" and accepted_type(o.get("model_ref")) != "MODEL":
            return None, ("MISSING_MODEL", f"{o['id']} names {o.get('model_ref')}, not an accepted model")
        app = o.get("applicability")
        if o.get("type") == "ASSERTION" and (not isinstance(app, dict) or app.get("kind") not in APPLICABILITY_KINDS):
            return None, ("UNSUPPORTED_SEMANTICS", f"{o['id']} applicability {app!r} is not in the profile")
        if o.get("basis") in {"REPORTED", "CORRECTION"} and not o.get("evidence_refs"):
            return None, ("MISSING_EVIDENCE", f"{o['id']} is {o['basis']} with no retained source")
    for o in objs:
        for field, r in object_refs(o):
            if not (graph.has(r) or r in here):
                return None, ("UNKNOWN_REFERENCE", f"{o['id']}.{field} names {r!r}, which does not exist")

    for o in objs:
        if o.get("type") == "EXECUTION" and o.get("context_ref"):
            ctx = o["context_ref"]
            want = {e["qualifiers"]["parameter"]["lexical"]: e["to"] for e in graph.links(ctx, "bindings")}
            got = {b["parameter"]: b["assertion_ref"] for b in o["input_bindings"]}
            if got != want or graph.ref(ctx, "model_ref") not in (None, o["model_ref"]):
                return None, ("PREMISE_MISMATCH", f"{o['id']} inputs {got} differ from {ctx} bindings {want}")
        if o.get("type") == "ASSERTION" and o.get("basis") == "CORRECTION":
            t = o["corrects_ref"]
            current = view.current(t)
            stated = {k: o["applicability"].get(k) for k in ("kind", "from", "until", "instant")}
            if not any({k: v[k] for k in ("kind", "from", "until", "instant")} == stated for v in current):
                return None, ("UNSUPPORTED_SEMANTICS",
                              f"{o['id']} period differs from the current period of {t}; interval splitting is excluded")

    new = copy.deepcopy(graph)
    try:
        apply_change(new, change, objs, len(new.ledger()))
    except EncodingError as exc:
        return None, ("UNSUPPORTED_SEMANTICS", str(exc))
    return new, None
