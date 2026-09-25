"""G2b relational store: connect, encode accepted changes, attempt refused ones, decode.

Standard library only. One SQLite database per specimen. The encoder never reads
queries, expected answers or derived labels; it reads objects and changes only.
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA_SQL = (HERE / "schema.sql").read_text(encoding="utf-8")

# Refusal categories in the order the witness reports them when an attempt
# violates several checks. The specimens do not define a precedence; this one is
# the witness's own and is stated in RESULTS.md.
PRECEDENCE = [
    "STALE_TARGET", "STALE_BASE", "UNSUPPORTED_SEMANTICS", "MISSING_CONTRACT",
    "MISSING_MODEL", "UNKNOWN_REFERENCE", "MISSING_EVIDENCE", "PREMISE_MISMATCH",
]
FK_PARENT_CATEGORY = {"model": "MISSING_MODEL", "contract": "MISSING_CONTRACT", "source": "MISSING_EVIDENCE"}
WITHHOLDABLE = {"SOURCE", "MODEL", "CONTRACT"}
ENDING_KINDS = ("TRANSITION", "CORRECTION", "REASSESSMENT")


class Refused(Exception):
    def __init__(self, category: str, detected: list[str], detail: list[str]):
        super().__init__(category)
        self.category, self.detected, self.detail = category, detected, detail


class NotEncodable(Exception):
    """Input the witness has no place for. Raised, never silently dropped."""


# connections

def connect(path: str | Path, read_only: bool = False) -> sqlite3.Connection:
    uri = f"file:{Path(path)}?mode={'ro' if read_only else 'rwc'}"
    conn = sqlite3.connect(uri, uri=True, isolation_level=None)
    conn.execute("PRAGMA foreign_keys = ON")
    if conn.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        raise RuntimeError("foreign key enforcement did not switch on for this connection")
    return conn


def create(path: str | Path) -> sqlite3.Connection:
    path = Path(path)
    if path.exists():
        raise FileExistsError(path)
    conn = connect(path)
    conn.executescript(SCHEMA_SQL)
    return conn


def snapshot(conn: sqlite3.Connection, path: str | Path | None = None) -> dict:
    """Row-for-row canonical content of every table, plus the file digest if given."""
    rows = {}
    for (name,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({name})")]
        rows[name] = conn.execute(f"SELECT * FROM {name} ORDER BY {', '.join(str(i + 1) for i in range(len(cols)))}").fetchall()
    out = {"rows": rows}
    if path is not None:
        out["file_sha256"] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return out


def seq_of(conn, position: str) -> int:
    row = conn.execute("SELECT seq FROM change WHERE position = ?", (position,)).fetchone()
    if row is None:
        raise KeyError(f"position {position!r} is not in this store")
    return row[0]


def head(conn) -> str:
    return conn.execute("SELECT position FROM change ORDER BY seq DESC LIMIT 1").fetchone()[0]


# encoding one object

def _lit(value: dict, where: str) -> tuple[str, str, str | None]:
    if set(value) - {"datatype", "lexical", "unit"}:
        raise NotEncodable(f"{where}: literal has fields {sorted(value)}")
    lex = value["lexical"]
    if not isinstance(lex, str):
        raise NotEncodable(f"{where}: lexical must be a string, got {type(lex).__name__}")
    return value["datatype"], lex, value.get("unit")


_KNOWN = {
    "SUBJECT": {"label"}, "ACCOUNT": {"label"},
    "SOURCE": {"source_kind", "text", "locator", "pointer"},
    "CONTRACT": {"version", "identity"},
    "ASSERTION": {"subject_ref", "property", "value", "basis", "applicability", "evidence_refs",
                  "qualifiers", "account_ref", "corrects_ref", "revises_ref"},
    "RELATION": {"relation_type", "from_ref", "to_ref", "qualifiers", "basis", "evidence_refs"},
    "GROUP": {"group_kind", "member_refs", "evidence_refs"},
    "ARGUMENT": {"premise_refs", "conclusion_ref", "evidence_refs"},
    "CONTEXT": {"context_kind", "bindings", "model_ref", "basis_refs"},
    "MODEL": {"version", "implementation", "formula", "parameters", "member_refs"},
    "EXECUTION": {"model_ref", "input_bindings", "context_ref", "implementation"},
    "RESULT": {"execution_ref", "value"},
    "RULE": {"semantics", "scope_refs", "assumptions"},
    "PLAN": {"subject_ref", "action", "planned_for", "evidence_refs"},
}
# Optional collection fields whose presence is recorded in list_field.
OPTIONAL_COLLECTIONS = {
    "ASSERTION": ("qualifiers",), "RELATION": ("qualifiers", "evidence_refs"),
    "GROUP": ("evidence_refs",), "ARGUMENT": ("evidence_refs",),
    "CONTEXT": ("basis_refs",), "MODEL": ("member_refs",),
}


def insert_object(conn, obj: dict, seq: int, add_ord: int, available: bool = True) -> None:
    oid, otype = obj["id"], obj["type"]
    if otype not in _KNOWN:
        raise NotEncodable(f"{oid}: type {otype!r}")
    extra = set(obj) - _KNOWN[otype] - {"id", "type", "note", "contract_ref"}
    if extra:
        raise NotEncodable(f"{oid}: fields {sorted(extra)} have no column")
    if not available and otype not in WITHHOLDABLE:
        raise NotEncodable(f"{oid}: withholding a {otype} is not encoded; only {sorted(WITHHOLDABLE)}")
    x = conn.execute
    x("INSERT INTO record (id, type, added_seq, add_ord, contract_id, note) VALUES (?,?,?,?,?,?)",
      (oid, otype, seq, add_ord, obj.get("contract_ref"), obj.get("note")))
    for field in OPTIONAL_COLLECTIONS.get(otype, ()):
        if field in obj and available:
            x("INSERT INTO list_field VALUES (?,?)", (oid, field))
    for i, src in enumerate(obj.get("evidence_refs", [])):
        x("INSERT INTO evidence VALUES (?,?,?)", (oid, i, src))
    for name, lit in (obj.get("qualifiers") or {}).items():
        x("INSERT INTO qualifier VALUES (?,?,?,?,?)", (oid, name, *_lit(lit, f"{oid}.qualifiers.{name}")))

    if otype in ("SUBJECT", "ACCOUNT"):
        x("INSERT INTO named VALUES (?,?,?)", (oid, otype, obj["label"]))
    elif otype == "SOURCE":
        if available:
            pointer = obj.get("pointer")
            if pointer is not None and not isinstance(pointer, str):
                raise NotEncodable(f"{oid}: non-string pointer")
            x("INSERT INTO source (id, available, source_kind, text, locator, pointer) VALUES (?,1,?,?,?,?)",
              (oid, obj["source_kind"], obj["text"], obj.get("locator"), pointer))
        else:
            x("INSERT INTO source (id, available) VALUES (?,0)", (oid,))
    elif otype == "CONTRACT":
        if available:
            x("INSERT INTO contract (id, available, version, identity) VALUES (?,1,?,?)", (oid, obj["version"], obj["identity"]))
        else:
            x("INSERT INTO contract (id, available) VALUES (?,0)", (oid,))
    elif otype == "MODEL":
        if available:
            x("INSERT INTO model (id, available, version, implementation, formula) VALUES (?,1,?,?,?)",
              (oid, obj["version"], obj["implementation"], obj["formula"]))
            for i, p in enumerate(obj["parameters"]):
                x("INSERT INTO model_parameter VALUES (?,?,?)", (oid, i, p))
            for i, m in enumerate(obj.get("member_refs", [])):
                x("INSERT INTO membership VALUES (?,?,?)", (oid, i, m))
        else:
            x("INSERT INTO model (id, available) VALUES (?,0)", (oid,))
    elif otype == "ASSERTION":
        app = obj["applicability"]
        kind = app.get("kind")
        allowed = {"INTERVAL": {"kind", "from", "until"}, "INSTANT": {"kind", "instant"}, "NONE_STATED": {"kind"}}
        if kind in allowed and set(app) != allowed[kind]:
            raise NotEncodable(f"{oid}: applicability fields {sorted(app)}")
        # An unknown kind is inserted as given; the named CHECK constraint refuses it.
        x("""INSERT INTO assertion (id, subject_id, property, v_datatype, v_lexical, v_unit, basis,
                 account_id, corrects_id, revises_id, app_kind, app_from, app_until, app_instant)
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
          (oid, obj["subject_ref"], obj["property"], *_lit(obj["value"], f"{oid}.value"), obj["basis"],
           obj.get("account_ref"), obj.get("corrects_ref"), obj.get("revises_ref"),
           kind, app.get("from"), app.get("until"), app.get("instant")))
    elif otype == "RELATION":
        x("INSERT INTO relation (id, relation_type, from_id, to_id, basis) VALUES (?,?,?,?,?)",
          (oid, obj["relation_type"], obj["from_ref"], obj["to_ref"], obj.get("basis")))
    elif otype == "GROUP":
        x("INSERT INTO claim_group (id, group_kind) VALUES (?,?)", (oid, obj["group_kind"]))
        for i, m in enumerate(obj["member_refs"]):
            x("INSERT INTO membership VALUES (?,?,?)", (oid, i, m))
    elif otype == "ARGUMENT":
        x("INSERT INTO argument (id, conclusion_id) VALUES (?,?)", (oid, obj["conclusion_ref"]))
        for i, p in enumerate(obj["premise_refs"]):
            x("INSERT INTO premise VALUES (?,?,?)", (oid, i, p))
    elif otype == "CONTEXT":
        x("INSERT INTO context (id, context_kind, model_id) VALUES (?,?,?)", (oid, obj["context_kind"], obj.get("model_ref")))
        for i, b in enumerate(obj.get("basis_refs", [])):
            x("INSERT INTO context_basis VALUES (?,?,?)", (oid, i, b))
        _bindings(conn, oid, obj["bindings"])
    elif otype == "EXECUTION":
        x("INSERT INTO execution (id, model_id, context_id, implementation) VALUES (?,?,?,?)",
          (oid, obj["model_ref"], obj.get("context_ref"), obj.get("implementation")))
        _bindings(conn, oid, obj["input_bindings"])
    elif otype == "RESULT":
        x("INSERT INTO result (id, execution_id, v_datatype, v_lexical, v_unit) VALUES (?,?,?,?,?)",
          (oid, obj["execution_ref"], *_lit(obj["value"], f"{oid}.value")))
    elif otype == "RULE":
        x("INSERT INTO rule (id, semantics) VALUES (?,?)", (oid, obj["semantics"]))
        for i, s in enumerate(obj["scope_refs"]):
            x("INSERT INTO rule_scope VALUES (?,?,?)", (oid, i, s))
        for i, a in enumerate(obj["assumptions"]):
            x("INSERT INTO rule_assumption VALUES (?,?,?)", (oid, i, a))
    elif otype == "PLAN":
        x("INSERT INTO plan (id, subject_id, action, planned_for) VALUES (?,?,?,?)",
          (oid, obj["subject_ref"], obj["action"], obj["planned_for"]))


def _bindings(conn, owner: str, bindings: list) -> None:
    for i, b in enumerate(bindings):
        if set(b) - {"parameter", "assertion_ref", "selection"}:
            raise NotEncodable(f"{owner}: binding fields {sorted(b)}")
        sel = b.get("selection") or {}
        if set(sel) - {"at", "valid_at", "account_ref"}:
            raise NotEncodable(f"{owner}: selection fields {sorted(sel)}")
        conn.execute("INSERT INTO binding VALUES (?,?,?,?,?,?,?)",
                     (owner, i, b["parameter"], b["assertion_ref"], sel.get("at"), sel.get("valid_at"), sel.get("account_ref")))


# temporal effects and admission checks (SQL)

# Cells current just before :seq (the head the change was checked against).
_CURRENT_BEFORE = """
    SELECT o.assertion_id AS aid, o.app_kind, o.valid_from, o.valid_until, o.instant
    FROM temporal_effect o
    WHERE o.op = 'OPEN' AND o.seq < :seq
      AND NOT EXISTS (SELECT 1 FROM temporal_effect e
                      WHERE e.op = 'END' AND e.assertion_id = o.assertion_id AND e.seq > o.seq AND e.seq < :seq)
"""

EFFECT_SQL = [
    # every assertion accepted by this change opens its first cell with its stated applicability
    """INSERT INTO temporal_effect (seq, op, assertion_id, app_kind, valid_from, valid_until, instant)
       SELECT :seq, 'OPEN', a.id, a.app_kind, a.app_from, a.app_until, a.app_instant
       FROM assertion a JOIN record r ON r.id = a.id WHERE r.added_seq = :seq""",
    # a transition, correction or reassessment ends the open cell of each named target
    """INSERT INTO temporal_effect (seq, op, assertion_id)
       SELECT :seq, 'END', t.target_id
       FROM change_target t JOIN change c ON c.seq = t.seq
       JOIN assertion a ON a.id = t.target_id
       WHERE t.seq = :seq AND c.kind IN ('TRANSITION', 'CORRECTION', 'REASSESSMENT')""",
    # a transition re-opens each target, now ending where the new account starts
    f"""INSERT INTO temporal_effect (seq, op, assertion_id, app_kind, valid_from, valid_until, instant)
       SELECT :seq, 'OPEN', t.target_id, cur.app_kind, cur.valid_from,
              (SELECT MIN(n.app_from) FROM assertion n JOIN record nr ON nr.id = n.id
               WHERE nr.added_seq = :seq AND n.app_kind = 'INTERVAL'
                 AND n.subject_id = ta.subject_id AND n.property = ta.property
                 AND n.account_id IS ta.account_id),
              cur.instant
       FROM change_target t JOIN change c ON c.seq = t.seq
       JOIN assertion ta ON ta.id = t.target_id
       JOIN ({_CURRENT_BEFORE}) cur ON cur.aid = t.target_id
       WHERE t.seq = :seq AND c.kind = 'TRANSITION'""",
]

CHECK_SQL = {
    "STALE_TARGET": f"""
        SELECT t.target_id FROM change_target t JOIN assertion a ON a.id = t.target_id
        WHERE t.seq = :seq AND t.target_id NOT IN (SELECT aid FROM ({_CURRENT_BEFORE}))""",
    "STALE_BASE": """
        SELECT position FROM change WHERE seq = :seq AND base_seq IS NOT :seq - 1""",
    # a correction whose period overlaps another open period of the same account
    # would need interval splitting, which this cut does not define
    "UNSUPPORTED_SEMANTICS": f"""
        SELECT n.id || ' overlaps ' || cur.aid
        FROM assertion n JOIN record nr ON nr.id = n.id AND nr.added_seq = :seq
        JOIN ({_CURRENT_BEFORE}) cur
        JOIN assertion o ON o.id = cur.aid
        WHERE n.basis = 'CORRECTION' AND n.app_kind = 'INTERVAL' AND cur.app_kind = 'INTERVAL'
          AND o.subject_id = n.subject_id AND o.property = n.property AND o.account_id IS n.account_id
          AND cur.aid IS NOT n.corrects_id
          AND cur.valid_from < COALESCE(n.app_until, '9999-12-31T23:59:59Z')
          AND n.app_from < COALESCE(cur.valid_until, '9999-12-31T23:59:59Z')""",
    "MISSING_EVIDENCE": """
        SELECT a.id FROM assertion a JOIN record r ON r.id = a.id AND r.added_seq = :seq
        WHERE a.basis IN ('REPORTED', 'CORRECTION')
          AND NOT EXISTS (SELECT 1 FROM evidence v WHERE v.owner_id = a.id)""",
    # an execution that claims a context must use that context's model and exact bindings
    "PREMISE_MISMATCH": """
        SELECT e.id FROM execution e JOIN record r ON r.id = e.id AND r.added_seq = :seq
        JOIN context c ON c.id = e.context_id
        WHERE (c.model_id IS NOT NULL AND e.model_id IS NOT c.model_id)
           OR EXISTS (SELECT parameter, assertion_id FROM binding WHERE owner_id = e.id
                      EXCEPT SELECT parameter, assertion_id FROM binding WHERE owner_id = c.id)
           OR EXISTS (SELECT parameter, assertion_id FROM binding WHERE owner_id = c.id
                      EXCEPT SELECT parameter, assertion_id FROM binding WHERE owner_id = e.id)""",
}


def _fk_categories(conn) -> list[tuple[str, str]]:
    out = []
    for table, rowid, parent, _fkid in conn.execute("PRAGMA foreign_key_check"):
        out.append((FK_PARENT_CATEGORY.get(parent, "UNKNOWN_REFERENCE"), f"{table} row {rowid} -> {parent}"))
    return out


def apply_change(conn, change: dict, objects: dict[str, dict], base: str | None = None,
                 withheld: frozenset = frozenset(), commit: bool = True) -> int:
    """Apply one change in one SQL transaction. Refused changes roll back and raise Refused.

    base: the position the change was prepared against. None means the current head.
    commit=False rolls back even an admissible change (used to probe without writing).
    """
    conn.execute("BEGIN IMMEDIATE")
    try:
        prev = conn.execute("SELECT MAX(seq) FROM change").fetchone()[0]
        seq = 0 if prev is None else prev + 1
        base_seq = None if seq == 0 else (prev if base is None else seq_of(conn, base))
        conn.execute("INSERT INTO change (seq, position, kind, base_seq, note) VALUES (?,?,?,?,?)",
                     (seq, change["position"], change["kind"], base_seq, change.get("note")))
        for i, t in enumerate(change.get("target_refs", [])):
            conn.execute("INSERT INTO change_target VALUES (?,?,?)", (seq, i, t))
        detected: list[tuple[str, str]] = []
        p = {"seq": seq}
        if seq > 0:
            for cat in ("STALE_TARGET", "STALE_BASE"):
                detected += [(cat, str(r[0])) for r in conn.execute(CHECK_SQL[cat], p)]
        try:
            for i, ref in enumerate(change["adds_refs"]):
                insert_object(conn, objects[ref], seq, i, available=ref not in withheld)
        except sqlite3.IntegrityError as exc:
            msg = str(exc)
            if msg.startswith("CHECK constraint failed: UNSUPPORTED_SEMANTICS"):
                detected.append(("UNSUPPORTED_SEMANTICS", msg))
            else:
                raise
        else:
            for sql in EFFECT_SQL:
                conn.execute(sql, p)
            detected += [("UNSUPPORTED_SEMANTICS", r[0]) for r in conn.execute(CHECK_SQL["UNSUPPORTED_SEMANTICS"], p)]
            detected += _fk_categories(conn)
            for cat in ("MISSING_EVIDENCE", "PREMISE_MISMATCH"):
                detected += [(cat, r[0]) for r in conn.execute(CHECK_SQL[cat], p)]
        if detected:
            cats = sorted({c for c, _ in detected}, key=PRECEDENCE.index)
            raise Refused(cats[0], cats, [d for _, d in detected])
        if commit:
            conn.execute("COMMIT")
        else:
            conn.execute("ROLLBACK")
        return seq
    except BaseException:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise


def build(path: str | Path, ledger: dict, upto: str | None = None, withheld=frozenset()) -> sqlite3.Connection:
    """Create a store and apply the ledger's changes in order, up to and including `upto`."""
    conn = create(path)
    objects = {o["id"]: o for o in ledger["objects"]}
    for ch in ledger["changes"]:
        apply_change(conn, ch, objects, withheld=frozenset(withheld))
        if ch["position"] == upto:
            break
    return conn


def infer_attempt_kind(objs: list[dict]) -> str:
    """Refusals in G1 carry no change kind. The witness infers one for the attempt only."""
    if any(o.get("corrects_ref") for o in objs):
        return "CORRECTION"
    if any(o.get("revises_ref") for o in objs):
        return "REASSESSMENT"
    if any(o["type"] == "EXECUTION" for o in objs):
        return "EXECUTION_RECORD"
    return "REPORT"


def attempt(conn, refusal: dict, rejected: dict[str, dict]) -> Refused | int:
    """Run a refusal's write attempt. Returns the Refused exception, or the seq if it was admissible
    (in which case it has been rolled back too; a refusal test must never grow the store)."""
    objs = [rejected[r] for r in refusal["would_add_refs"]]
    change = {"position": f"attempt:{refusal['id']}", "kind": infer_attempt_kind(objs),
              "adds_refs": refusal["would_add_refs"], "target_refs": refusal.get("target_refs", [])}
    try:
        return apply_change(conn, change, rejected, base=refusal.get("base"), commit=False)
    except Refused as exc:
        return exc


# decoding

def _lit_out(dt, lex, unit):
    v = {"datatype": dt, "lexical": lex}
    if unit is not None:
        v["unit"] = unit
    return v


def decode(conn) -> dict:
    """Canonical logical graph: every accepted object in the G1 object format, plus the changes."""
    q = lambda sql, *a: conn.execute(sql, a).fetchall()  # noqa: E731
    present = {(o, f) for o, f in q("SELECT owner_id, field FROM list_field")}
    objects = []
    for oid, otype, contract, note in q("SELECT id, type, contract_id, note FROM record ORDER BY added_seq, add_ord"):
        o = {"id": oid, "type": otype}
        ev = [r[0] for r in q("SELECT source_id FROM evidence WHERE owner_id=? ORDER BY ord", oid)]
        quals = {n: _lit_out(d, l, u) for n, d, l, u in q("SELECT name, datatype, lexical, unit FROM qualifier WHERE owner_id=? ORDER BY name", oid)}
        members = [r[0] for r in q("SELECT member_id FROM membership WHERE graph_id=? ORDER BY ord", oid)]
        if otype in ("SUBJECT", "ACCOUNT"):
            o["label"] = q("SELECT label FROM named WHERE id=?", oid)[0][0]
        elif otype == "SOURCE":
            avail, kind, text, loc, ptr = q("SELECT available, source_kind, text, locator, pointer FROM source WHERE id=?", oid)[0]
            if not avail:
                o["unavailable"] = True
            else:
                o.update(source_kind=kind, text=text)
                if loc is not None:
                    o["locator"] = loc
                if ptr is not None:
                    o["pointer"] = ptr
        elif otype == "CONTRACT":
            avail, ver, ident = q("SELECT available, version, identity FROM contract WHERE id=?", oid)[0]
            o.update({"unavailable": True} if not avail else {"version": ver, "identity": ident})
        elif otype == "MODEL":
            avail, ver, impl, formula = q("SELECT available, version, implementation, formula FROM model WHERE id=?", oid)[0]
            if not avail:
                o["unavailable"] = True
            else:
                o.update(version=ver, implementation=impl, formula=formula,
                         parameters=[r[0] for r in q("SELECT name FROM model_parameter WHERE model_id=? ORDER BY ord", oid)])
                if (oid, "member_refs") in present:
                    o["member_refs"] = members
        elif otype == "ASSERTION":
            (subj, prop, dt, lex, unit, basis, acct, corr, rev, kind, frm, until, inst) = q(
                """SELECT subject_id, property, v_datatype, v_lexical, v_unit, basis, account_id, corrects_id,
                          revises_id, app_kind, app_from, app_until, app_instant FROM assertion WHERE id=?""", oid)[0]
            app = {"kind": kind}
            if kind == "INTERVAL":
                app.update({"from": frm, "until": until})
            elif kind == "INSTANT":
                app["instant"] = inst
            o.update(subject_ref=subj, property=prop, value=_lit_out(dt, lex, unit), basis=basis,
                     applicability=app, evidence_refs=ev)
            for key, val in (("account_ref", acct), ("corrects_ref", corr), ("revises_ref", rev)):
                if val is not None:
                    o[key] = val
            if (oid, "qualifiers") in present:
                o["qualifiers"] = quals
        elif otype == "RELATION":
            rtype, frm, to, basis = q("SELECT relation_type, from_id, to_id, basis FROM relation WHERE id=?", oid)[0]
            o.update(relation_type=rtype, from_ref=frm, to_ref=to)
            if basis is not None:
                o["basis"] = basis
            if (oid, "qualifiers") in present:
                o["qualifiers"] = quals
            if (oid, "evidence_refs") in present:
                o["evidence_refs"] = ev
        elif otype == "GROUP":
            o.update(group_kind=q("SELECT group_kind FROM claim_group WHERE id=?", oid)[0][0], member_refs=members)
            if (oid, "evidence_refs") in present:
                o["evidence_refs"] = ev
        elif otype == "ARGUMENT":
            o.update(premise_refs=[r[0] for r in q("SELECT premise_id FROM premise WHERE argument_id=? ORDER BY ord", oid)],
                     conclusion_ref=q("SELECT conclusion_id FROM argument WHERE id=?", oid)[0][0])
            if (oid, "evidence_refs") in present:
                o["evidence_refs"] = ev
        elif otype == "CONTEXT":
            kind, model = q("SELECT context_kind, model_id FROM context WHERE id=?", oid)[0]
            o.update(context_kind=kind, bindings=_bindings_out(conn, oid))
            if model is not None:
                o["model_ref"] = model
            if (oid, "basis_refs") in present:
                o["basis_refs"] = [r[0] for r in q("SELECT basis_id FROM context_basis WHERE context_id=? ORDER BY ord", oid)]
        elif otype == "EXECUTION":
            model, ctx, impl = q("SELECT model_id, context_id, implementation FROM execution WHERE id=?", oid)[0]
            o.update(model_ref=model, input_bindings=_bindings_out(conn, oid))
            if ctx is not None:
                o["context_ref"] = ctx
            if impl is not None:
                o["implementation"] = impl
        elif otype == "RESULT":
            ex, dt, lex, unit = q("SELECT execution_id, v_datatype, v_lexical, v_unit FROM result WHERE id=?", oid)[0]
            o.update(execution_ref=ex, value=_lit_out(dt, lex, unit))
        elif otype == "RULE":
            o.update(semantics=q("SELECT semantics FROM rule WHERE id=?", oid)[0][0],
                     scope_refs=[r[0] for r in q("SELECT subject_id FROM rule_scope WHERE rule_id=? ORDER BY ord", oid)],
                     assumptions=[r[0] for r in q("SELECT text FROM rule_assumption WHERE rule_id=? ORDER BY ord", oid)])
        elif otype == "PLAN":
            subj, action, when = q("SELECT subject_id, action, planned_for FROM plan WHERE id=?", oid)[0]
            o.update(subject_ref=subj, action=action, planned_for=when, evidence_refs=ev)
        if contract is not None:
            o["contract_ref"] = contract
        if note is not None:
            o["note"] = note
        objects.append(o)
    changes = []
    for seq, pos, kind, note in q("SELECT seq, position, kind, note FROM change ORDER BY seq"):
        ch = {"position": pos, "kind": kind,
              "adds_refs": [r[0] for r in q("SELECT id FROM record WHERE added_seq=? ORDER BY add_ord", seq)]}
        targets = [r[0] for r in q("SELECT target_id FROM change_target WHERE seq=? ORDER BY ord", seq)]
        if targets:
            ch["target_refs"] = targets
        if note is not None:
            ch["note"] = note
        changes.append(ch)
    return {"objects": objects, "changes": changes}


def _bindings_out(conn, owner):
    out = []
    for param, aid, at, valid_at, acct in conn.execute(
            "SELECT parameter, assertion_id, sel_at, sel_valid_at, sel_account_id FROM binding WHERE owner_id=? ORDER BY ord", (owner,)):
        b = {"parameter": param, "assertion_ref": aid}
        if at is not None:
            sel = {"at": at}
            if valid_at is not None:
                sel["valid_at"] = valid_at
            if acct is not None:
                sel["account_ref"] = acct
            b["selection"] = sel
        out.append(b)
    return out


def canonical_ledger(spec: dict) -> dict:
    """The part of a specimen the encoder consumes: objects and ordered changes."""
    return {"objects": sorted(spec["objects"], key=lambda o: o["id"]), "changes": spec["changes"]}


def same_graph(a: dict, b: dict) -> list[str]:
    """Differences between two logical graphs, compared by id, ignoring JSON key order."""
    diffs = []
    ao, bo = {o["id"]: o for o in a["objects"]}, {o["id"]: o for o in b["objects"]}
    for oid in sorted(set(ao) | set(bo)):
        if ao.get(oid) != bo.get(oid):
            diffs.append(f"object {oid}: {ao.get(oid)!r} != {bo.get(oid)!r}")
    if a["changes"] != b["changes"]:
        diffs.append("changes differ")
    return diffs
