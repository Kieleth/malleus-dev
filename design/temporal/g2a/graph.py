"""G2a Construction A: ordinary graph records, with named subgraphs (Construction D).

Research-local witness code, not a Core proposal. Standard library only.

A graph has three parts:

- nodes: {id, type, payload}. Payload scalars are typed literals
  {"datatype", "lexical", "unit"?} or None for an explicit null.
- edges: {id, class, type, from, to, owner, payload, qualifiers}. class RELATION
  is an accepted RELATION object (its id is the object id, its type the
  relation_type). class LINK is one reference held by an owner object's field;
  its id is "<owner>~<field>~<ordinal>", a structural address, never a value.
  An edge endpoint may be a node id or an edge id: one element namespace.
- subgraphs: {id: [member ids]}. GROUP members, MODEL members, and one
  subgraph per accepted change listing what that change added.

Each accepted change is a ledger node "ledger:<position>" with seq, kind and
LINK edges to its targets. The prefix at a position keeps only what the
changes up to it added; no record is ever modified after it is added.
"""

from __future__ import annotations

import copy
import json

FORMAT = "malleus.temporal-g2a-graph/draft-1"
LEDGER = "ledger:"
SEP = "~"

# field -> encoding kind, per object type. Kinds:
#   str   xsd:string literal      enum  enum literal       lit  typed literal as given
#   dt    xsd:dateTime literal    strs  list of xsd:string ref  one LINK edge
#   refs  ordered LINK edges      app   applicability      qual qualifier map
#   binds binding LINK edges      members  named subgraph
COMMON = {"note": "str", "contract_ref": "ref"}
FIELDS = {
    "SUBJECT": {"label": "str"},
    "ACCOUNT": {"label": "str"},
    "SOURCE": {"source_kind": "enum", "text": "str", "locator": "str", "pointer": "str"},
    "CONTRACT": {"version": "str", "identity": "str"},
    "ASSERTION": {"subject_ref": "ref", "property": "str", "value": "lit", "basis": "enum",
                  "applicability": "app", "evidence_refs": "refs", "qualifiers": "qual",
                  "account_ref": "ref", "corrects_ref": "ref", "revises_ref": "ref"},
    "RELATION": {"relation_type": "edge_type", "from_ref": "edge_from", "to_ref": "edge_to",
                 "qualifiers": "qual", "basis": "enum", "evidence_refs": "refs"},
    "GROUP": {"group_kind": "enum", "member_refs": "members", "evidence_refs": "refs"},
    "ARGUMENT": {"premise_refs": "refs", "conclusion_ref": "ref", "evidence_refs": "refs"},
    "CONTEXT": {"context_kind": "enum", "bindings": "binds", "model_ref": "ref", "basis_refs": "refs"},
    "MODEL": {"version": "str", "implementation": "str", "formula": "str", "parameters": "strs",
              "member_refs": "members"},
    "EXECUTION": {"model_ref": "ref", "input_bindings": "binds", "context_ref": "ref",
                  "implementation": "str"},
    "RESULT": {"execution_ref": "ref", "value": "lit"},
    "RULE": {"semantics": "str", "scope_refs": "refs", "assumptions": "strs"},
    "PLAN": {"subject_ref": "ref", "action": "enum", "planned_for": "dt", "evidence_refs": "refs"},
}
APPLICABILITY_KINDS = {"INTERVAL", "INSTANT", "NONE_STATED"}


class EncodingError(ValueError):
    """An object this encoder cannot represent. Raised, never guessed around."""


def L(datatype: str, lexical: str) -> dict:
    return {"datatype": datatype, "lexical": lexical}


def _int(n: int) -> dict:
    return L("xsd:integer", str(n))


def link_id(owner: str, field: str, i: int) -> str:
    return f"{owner}{SEP}{field}{SEP}{i}"


class Graph:
    def __init__(self):
        self.nodes: dict[str, dict] = {}
        self.edges: dict[str, dict] = {}
        self.subgraphs: dict[str, list[str]] = {}

    # -- element access -------------------------------------------------
    def element(self, i: str) -> dict | None:
        return self.nodes.get(i) or self.edges.get(i)

    def has(self, i: str) -> bool:
        return i in self.nodes or i in self.edges

    def type_of(self, i: str) -> str | None:
        if i in self.nodes:
            return self.nodes[i]["type"]
        if i in self.edges and self.edges[i]["class"] == "RELATION":
            return "RELATION"
        return None

    def links(self, owner: str, field: str) -> list[dict]:
        """LINK edges of one owner field, in ordinal order."""
        out = [e for e in self.edges.values()
               if e["class"] == "LINK" and e["from"] == owner and e["type"] == field]
        return sorted(out, key=lambda e: int(e["qualifiers"]["ordinal"]["lexical"]))

    def ref(self, owner: str, field: str) -> str | None:
        got = self.links(owner, field)
        return got[0]["to"] if got else None

    def refs(self, owner: str, field: str) -> list[str]:
        return [e["to"] for e in self.links(owner, field)]

    def referrers(self, target: str, field: str) -> list[str]:
        return sorted(e["from"] for e in self.edges.values()
                      if e["class"] == "LINK" and e["to"] == target and e["type"] == field)

    def payload(self, i: str) -> dict:
        return self.element(i)["payload"]

    def lex(self, i: str, field: str) -> str | None:
        v = self.payload(i).get(field)
        return v["lexical"] if isinstance(v, dict) else None

    def of_type(self, t: str) -> list[str]:
        if t == "RELATION":
            return sorted(i for i, e in self.edges.items() if e["class"] == "RELATION")
        return sorted(i for i, n in self.nodes.items() if n["type"] == t)

    # -- ledger ---------------------------------------------------------
    def ledger(self) -> list[dict]:
        rows = []
        for i in self.of_type("CHANGE"):
            rows.append({"node": i, "position": self.lex(i, "position"), "kind": self.lex(i, "kind"),
                         "seq": int(self.lex(i, "seq")), "adds": list(self.subgraphs.get(i, [])),
                         "targets": self.refs(i, "target_refs")})
        return sorted(rows, key=lambda r: r["seq"])

    def positions(self) -> list[str]:
        return [r["position"] for r in self.ledger()]

    def head(self) -> str:
        return self.ledger()[-1]["position"]

    def added_at(self) -> dict[str, str]:
        return {m: r["position"] for r in self.ledger() for m in r["adds"]}

    def missing(self) -> list[str]:
        """Ids an accepted change added whose record is not present (withheld)."""
        return sorted(m for r in self.ledger() for m in r["adds"] if not self.has(m))

    # -- derived graphs -------------------------------------------------
    def prefix(self, position: str) -> "Graph":
        """The graph built by the accepted changes up to and including position."""
        rows = self.ledger()
        seqs = {r["position"]: r["seq"] for r in rows}
        if position not in seqs:
            raise KeyError(f"unknown position {position!r}")
        kept_changes = {r["node"] for r in rows if r["seq"] <= seqs[position]}
        kept = set(kept_changes) | {m for r in rows if r["node"] in kept_changes for m in r["adds"]}
        return self._restrict(kept)

    def withhold(self, ids) -> "Graph":
        """The same graph with the records of ids unavailable, as a rebuild without their bytes."""
        ids = set(ids)
        kept = {i for i in self.nodes if i not in ids} | {
            i for i, e in self.edges.items() if e["class"] == "RELATION" and i not in ids}
        return self._restrict(kept)

    def _restrict(self, kept: set) -> "Graph":
        g = Graph()
        g.nodes = {i: copy.deepcopy(n) for i, n in self.nodes.items() if i in kept}
        g.edges = {i: copy.deepcopy(e) for i, e in self.edges.items()
                   if (e["class"] == "RELATION" and i in kept) or (e["class"] == "LINK" and e["owner"] in kept)}
        g.subgraphs = {i: list(m) for i, m in self.subgraphs.items() if i in kept}
        return g

    # -- canonical form -------------------------------------------------
    def to_canonical(self) -> dict:
        return {"format": FORMAT,
                "nodes": [self.nodes[i] for i in sorted(self.nodes)],
                "edges": [self.edges[i] for i in sorted(self.edges)],
                "subgraphs": {i: self.subgraphs[i] for i in sorted(self.subgraphs)}}

    def dumps(self) -> str:
        return json.dumps(self.to_canonical(), sort_keys=True, ensure_ascii=False, separators=(",", ":"))

    @classmethod
    def loads(cls, text: str) -> "Graph":
        data = json.loads(text)
        if data.get("format") != FORMAT:
            raise EncodingError(f"unknown graph format {data.get('format')!r}")
        g = cls()
        for n in data["nodes"]:
            if n["id"] in g.nodes:
                raise EncodingError(f"duplicate node {n['id']!r}")
            g.nodes[n["id"]] = n
        for e in data["edges"]:
            if e["id"] in g.edges or e["id"] in g.nodes:
                raise EncodingError(f"duplicate element {e['id']!r}")
            g.edges[e["id"]] = e
        g.subgraphs = {i: list(m) for i, m in data["subgraphs"].items()}
        return g


# -- encoder ---------------------------------------------------------------

def _add_link(g: Graph, owner: str, source: str, field: str, target, i: int, extra=None, member_owner=None):
    if not isinstance(target, str):
        raise EncodingError(f"{owner}.{field}: reference must be a string id, got {target!r}")
    eid = link_id(source, field, i)
    g.edges[eid] = {"id": eid, "class": "LINK", "type": field, "from": source, "to": target,
                    "owner": member_owner or owner, "payload": {},
                    "qualifiers": {"ordinal": _int(i), **(extra or {})}}
    return eid


def _scalar(kind: str, value, where: str):
    if value is None:
        return None
    if kind == "str":
        if not isinstance(value, str):
            raise EncodingError(f"{where}: expected a string")
        return L("xsd:string", value)
    if kind == "enum":
        return L("enum", value)
    if kind == "dt":
        return L("xsd:dateTime", value)
    if kind == "lit":
        if not isinstance(value, dict) or not isinstance(value.get("lexical"), str):
            raise EncodingError(f"{where}: typed literal needs a string lexical form")
        return dict(value)
    raise EncodingError(f"{where}: not a scalar kind {kind}")


def encode_object(g: Graph, obj: dict) -> None:
    oid, otype = obj["id"], obj["type"]
    if otype not in FIELDS:
        raise EncodingError(f"{oid}: no encoding for object type {otype!r}")
    spec = {**FIELDS[otype], **COMMON}
    unknown = set(obj) - set(spec) - {"id", "type"}
    if unknown:
        raise EncodingError(f"{oid}: fields with no encoding: {sorted(unknown)}")
    if g.has(oid):
        raise EncodingError(f"{oid}: id already present")
    payload: dict = {}
    element: dict
    if otype == "RELATION":
        element = {"id": oid, "class": "RELATION", "type": obj["relation_type"], "from": obj["from_ref"],
                   "to": obj["to_ref"], "owner": oid, "payload": payload, "qualifiers": {}}
        g.edges[oid] = element
    else:
        element = {"id": oid, "type": otype, "payload": payload}
        g.nodes[oid] = element
    for field, kind in spec.items():
        if field not in obj:
            continue
        val = obj[field]
        where = f"{oid}.{field}"
        if kind in {"str", "enum", "dt", "lit"}:
            payload[field] = _scalar(kind, val, where)
        elif kind in {"edge_type", "edge_from", "edge_to"}:
            continue
        elif kind == "strs":
            payload[field] = [_scalar("str", v, where) for v in val]
        elif kind == "ref":
            if val is None:
                payload[field] = None  # explicit null, distinct from an absent field
            else:
                _add_link(g, oid, oid, field, val, 0)
        elif kind == "refs":
            payload[field] = _int(len(val))
            for i, r in enumerate(val):
                _add_link(g, oid, oid, field, r, i)
        elif kind == "qual":
            element["qualifiers"] = {k: _scalar("lit", v, f"{where}.{k}") for k, v in val.items()}
            payload["qualifiers"] = _int(len(val))
        elif kind == "app":
            app_kind = val.get("kind") if isinstance(val, dict) else None
            if app_kind not in APPLICABILITY_KINDS:
                raise EncodingError(f"{where}: applicability kind {app_kind!r} is not encodable")
            payload["applicability_kind"] = L("enum", app_kind)
            if app_kind == "INTERVAL":
                payload["applicability_from"] = _scalar("dt", val["from"], where)
                payload["applicability_until"] = _scalar("dt", val["until"], where)  # None = known open
            elif app_kind == "INSTANT":
                payload["applicability_instant"] = _scalar("dt", val["instant"], where)
        elif kind == "binds":
            payload[field] = _int(len(val))
            for i, b in enumerate(val):
                extra = {"parameter": L("xsd:string", b["parameter"])}
                sel = b.get("selection")
                if sel is not None:
                    extra["selection_at"] = L("xsd:string", sel["at"])
                    if "valid_at" in sel:
                        extra["selection_valid_at"] = _scalar("dt", sel["valid_at"], where)
                eid = _add_link(g, oid, oid, field, b["assertion_ref"], i, extra)
                if sel is not None and "account_ref" in sel:
                    _add_link(g, oid, eid, "selection.account_ref", sel["account_ref"], 0)
        elif kind == "members":
            g.subgraphs[oid] = list(val)
            payload[field] = _int(len(val))
        else:
            raise EncodingError(f"{where}: unhandled kind {kind}")


def encode(objects: list[dict], changes: list[dict], withheld=()) -> Graph:
    """Build the graph by applying the accepted changes in order.

    withheld: ids whose records are unavailable to this rebuild. Their change
    still lists them; the records themselves are not built.
    """
    by_id = {o["id"]: o for o in objects}
    withheld = set(withheld)
    g = Graph()
    for seq, ch in enumerate(changes):
        apply_change(g, ch, [by_id[a] for a in ch["adds_refs"] if a not in withheld], seq)
    return g


def apply_change(g: Graph, change: dict, objs: list[dict], seq: int) -> None:
    node = LEDGER + change["position"]
    if g.has(node):
        raise EncodingError(f"position {change['position']!r} already accepted")
    payload = {"position": L("xsd:string", change["position"]), "kind": L("enum", change["kind"]),
               "seq": _int(seq), "target_refs": _int(len(change.get("target_refs") or []))}
    if "target_refs" not in change:
        payload["target_refs"] = None
    if "note" in change:
        payload["note"] = L("xsd:string", change["note"])
    g.nodes[node] = {"id": node, "type": "CHANGE", "payload": payload}
    g.subgraphs[node] = list(change["adds_refs"])
    for i, t in enumerate(change.get("target_refs") or []):
        _add_link(g, node, node, "target_refs", t, i)
    for o in objs:
        encode_object(g, o)


# -- decoder ---------------------------------------------------------------

def _unscalar(v):
    if v is None:
        return None
    if v["datatype"] in {"xsd:string", "enum", "xsd:dateTime"} and set(v) == {"datatype", "lexical"}:
        return v["lexical"]
    raise EncodingError(f"not a plain scalar: {v!r}")


def decode_object(g: Graph, oid: str) -> dict:
    el = g.element(oid)
    otype = g.type_of(oid)
    obj: dict = {"id": oid, "type": otype}
    p = el["payload"]
    for field, kind in {**FIELDS[otype], **COMMON}.items():
        if kind == "edge_type":
            obj[field] = el["type"]
        elif kind == "edge_from":
            obj[field] = el["from"]
        elif kind == "edge_to":
            obj[field] = el["to"]
        elif kind == "app":
            if "applicability_kind" not in p:
                continue
            k = p["applicability_kind"]["lexical"]
            app = {"kind": k}
            if k == "INTERVAL":
                app["from"] = _unscalar(p["applicability_from"])
                app["until"] = _unscalar(p["applicability_until"])
            elif k == "INSTANT":
                app["instant"] = _unscalar(p["applicability_instant"])
            obj[field] = app
        elif kind == "ref":
            if field in p:
                obj[field] = None
            elif g.links(oid, field):
                obj[field] = g.ref(oid, field)
        elif field not in p:
            continue
        elif kind in {"str", "enum", "dt"}:
            obj[field] = _unscalar(p[field])
        elif kind == "lit":
            obj[field] = dict(p[field])
        elif kind == "strs":
            obj[field] = [_unscalar(v) for v in p[field]]
        elif kind == "refs":
            got = g.refs(oid, field)
            if len(got) != int(p[field]["lexical"]):
                raise EncodingError(f"{oid}.{field}: {len(got)} links, payload says {p[field]['lexical']}")
            obj[field] = got
        elif kind == "qual":
            obj[field] = {k: dict(v) for k, v in el["qualifiers"].items()}
        elif kind == "binds":
            out = []
            for e in g.links(oid, field):
                q = e["qualifiers"]
                b = {"parameter": q["parameter"]["lexical"], "assertion_ref": e["to"]}
                if "selection_at" in q:
                    sel = {"at": q["selection_at"]["lexical"]}
                    if "selection_valid_at" in q:
                        sel["valid_at"] = q["selection_valid_at"]["lexical"]
                    acct = g.ref(e["id"], "selection.account_ref")
                    if acct is not None:
                        sel["account_ref"] = acct
                    b["selection"] = sel
                out.append(b)
            if len(out) != int(p[field]["lexical"]):
                raise EncodingError(f"{oid}.{field}: binding count mismatch")
            obj[field] = out
        elif kind == "members":
            obj[field] = list(g.subgraphs[oid])
    return obj


def decode(g: Graph) -> tuple[list[dict], list[dict]]:
    """Graph back to (objects, changes) in the specimen's own form."""
    objects, changes = [], []
    for row in g.ledger():
        ch = {"position": row["position"], "kind": row["kind"], "adds_refs": row["adds"]}
        if g.payload(row["node"]).get("target_refs") is not None:
            ch["target_refs"] = row["targets"]
        if "note" in g.payload(row["node"]):
            ch["note"] = g.lex(row["node"], "note")
        changes.append(ch)
        objects.extend(decode_object(g, a) for a in row["adds"] if g.has(a))
    return objects, changes
