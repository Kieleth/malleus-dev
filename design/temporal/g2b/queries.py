"""G2b queries over the relational store. Selection logic is SQL; Python assembles answers.

Every read is parameterised by a knowledge position :at (a change seq). Visibility is
`record.added_seq <= :at`; applicability versions ("cells") and their knowledge ends
are computed from temporal_effect rows with seq <= :at only. No query writes.

Policy branches for the G1 open choices arrive in `policy` (see runner.BRANCH_POLICY).
"""

from __future__ import annotations

import json

# A cell is one version of an assertion's applicability, opened by an OPEN effect.
# kuntil is the first END for that assertion after the cell opened and at or before :at.
CELLS = """
cell AS (
    SELECT o.assertion_id AS aid, o.seq AS kfrom, o.app_kind, o.valid_from, o.valid_until, o.instant,
           (SELECT MIN(e.seq) FROM temporal_effect e
            WHERE e.op = 'END' AND e.assertion_id = o.assertion_id AND e.seq > o.seq AND e.seq <= :at) AS kuntil
    FROM temporal_effect o WHERE o.op = 'OPEN' AND o.seq <= :at),
cur AS (SELECT * FROM cell WHERE kuntil IS NULL),
vis AS (SELECT id, type FROM record WHERE added_seq <= :at)
"""

SELECT_APPLICABLE_SQL = f"""
WITH {CELLS},
cand AS (
    SELECT cur.*, a.basis FROM cur JOIN assertion a ON a.id = cur.aid
    WHERE a.subject_id = :subject AND a.property = :property
      AND (:account IS NULL OR a.account_id = :account)
      AND (:context IS NULL OR a.id IN (
            SELECT b.assertion_id FROM binding b JOIN vis ON vis.id = b.owner_id WHERE b.owner_id = :context))
      AND (:account IS NOT NULL OR :context IS NOT NULL OR :include_assumptions OR a.basis <> 'ASSUMPTION')),
cls AS (
    SELECT aid, kfrom, CASE
        WHEN :valid_at IS NULL THEN 'COVERS'
        WHEN app_kind = 'INTERVAL' AND valid_from <= :valid_at AND (valid_until IS NULL OR :valid_at < valid_until) THEN 'COVERS'
        WHEN app_kind = 'INSTANT' AND instant = :valid_at THEN 'COVERS'
        WHEN app_kind = 'NONE_STATED' THEN 'UNRESOLVED'
        ELSE 'MISSES' END AS status
    FROM cand),
agg AS (SELECT COUNT(*) AS n, TOTAL(status = 'COVERS') AS nc, TOTAL(status = 'UNRESOLVED') AS nu FROM cls)
SELECT CASE
        WHEN n = 0 THEN 'NO_ACCEPTED_ACCOUNT'
        WHEN nc = 1 AND nu = 0 THEN 'SELECTED'
        WHEN nc >= 1 THEN 'AMBIGUOUS_SELECTION'
        WHEN nu >= 1 THEN 'UNRESOLVED_APPLICABILITY'
        ELSE 'NO_APPLICABLE_ACCOUNT' END AS state,
       cls.aid, cls.kfrom, cls.status
FROM agg LEFT JOIN cls ON 1 = 1
ORDER BY cls.aid
"""

# Declared persistence. The witness knows one rule shape only: an event property
# 'event' with OPENED/CLOSED values becomes a step function on property 'state'.
# It does not read the rule's prose; see RESULTS.md, finding F-RULE-PROSE.
STATE_PROPERTY, EVENT_PROPERTY = "state", "event"
PERSISTENCE_SQL = f"""
WITH {CELLS},
map(event, state) AS (VALUES ('OPENED', 'OPEN'), ('CLOSED', 'CLOSED')),
ev AS (
    SELECT cur.aid, cur.instant, a.v_lexical FROM cur JOIN assertion a ON a.id = cur.aid
    WHERE a.subject_id = :subject AND a.property = '{EVENT_PROPERTY}' AND cur.app_kind = 'INSTANT'),
rule_ok AS (
    SELECT r.id FROM rule r JOIN vis ON vis.id = r.id JOIN rule_scope s ON s.rule_id = r.id
    WHERE r.id = :rule AND s.subject_id = :subject),
prior AS (SELECT * FROM ev WHERE instant <= :valid_at),
latest AS (SELECT * FROM prior WHERE instant = (SELECT MAX(instant) FROM prior))
SELECT (SELECT COUNT(*) FROM ev) AS n_events,
       (SELECT COUNT(*) FROM rule_ok) AS rule_applies,
       (SELECT COUNT(*) FROM latest) AS n_latest,
       latest.aid, map.state,
       (SELECT json_group_array(aid) FROM (SELECT aid FROM ev ORDER BY aid)) AS all_events
FROM (SELECT 1) LEFT JOIN latest ON 1 = 1 LEFT JOIN map ON map.event = latest.v_lexical
"""

DEFAULT_RULE_SQL = """
SELECT r.id FROM rule r JOIN record rr ON rr.id = r.id AND rr.added_seq <= :at
JOIN rule_scope s ON s.rule_id = r.id WHERE s.subject_id = :subject ORDER BY r.id
"""

SELECT_ACCOUNT_SQL = f"""
WITH {CELLS}
SELECT cur.aid, cur.kfrom FROM cur JOIN assertion a ON a.id = cur.aid
WHERE a.subject_id = :subject AND a.property = :property
  AND (:account IS NULL OR a.account_id = :account)
  AND (:account IS NOT NULL OR :include_assumptions OR a.basis <> 'ASSUMPTION')
ORDER BY cur.aid
"""

ARGUMENTS_SQL = """
SELECT g.id, p.premise_id,
       EXISTS (SELECT 1 FROM assertion x JOIN record xr ON xr.id = x.id AND xr.added_seq <= :at
               WHERE x.revises_id = p.premise_id OR x.corrects_id = p.premise_id) AS changed
FROM argument g JOIN record r ON r.id = g.id AND r.added_seq <= :at
JOIN premise p ON p.argument_id = g.id
WHERE g.conclusion_id = :conclusion
ORDER BY g.id, p.ord
"""

HISTORY_RECORDS_SQL = f"""
WITH {CELLS}
SELECT a.id, 'ASSERTION' FROM assertion a JOIN vis ON vis.id = a.id
 WHERE a.subject_id = :subject AND (:property IS NULL OR a.property = :property)
UNION ALL
SELECT p.id, 'PLAN' FROM plan p JOIN vis ON vis.id = p.id
 WHERE p.subject_id = :subject AND (:property IS NULL OR :property = 'plan')
UNION ALL
SELECT r.id, 'RELATION' FROM relation r JOIN vis ON vis.id = r.id
 WHERE :property IS NULL AND (r.from_id = :subject OR r.to_id = :subject)
"""

HISTORY_CELLS_SQL = f"""
WITH {CELLS}
SELECT cell.aid, cell.kfrom, cell.app_kind, cell.valid_from, cell.valid_until, cell.kuntil
FROM cell JOIN assertion a ON a.id = cell.aid
WHERE a.subject_id = :subject AND (:property IS NULL OR a.property = :property)
"""

UNAVAILABLE = """(SELECT id FROM source WHERE available = 0
                  UNION SELECT id FROM model WHERE available = 0
                  UNION SELECT id FROM contract WHERE available = 0)"""

CLOSURE_TAIL = f"""
visible(id) AS (SELECT id FROM base WHERE id IN (SELECT id FROM record WHERE added_seq <= :at)),
closure(id) AS (
    SELECT id FROM visible
    UNION SELECT source_id FROM evidence WHERE owner_id IN visible
    UNION SELECT contract_id FROM record WHERE id IN visible AND contract_id IS NOT NULL)
SELECT id FROM closure WHERE id IN {UNAVAILABLE} ORDER BY id
"""
EXECUTION_CLOSURE_SQL = """
WITH base(id) AS (
    SELECT :x UNION SELECT model_id FROM execution WHERE id = :x
    UNION SELECT context_id FROM execution WHERE id = :x AND context_id IS NOT NULL
    UNION SELECT id FROM result WHERE execution_id = :x
    UNION SELECT assertion_id FROM binding WHERE owner_id = :x),
""" + CLOSURE_TAIL
LOOKUP_CLOSURE_SQL = """
WITH base(id) AS (SELECT :x UNION SELECT member_id FROM membership WHERE graph_id = :x),
""" + CLOSURE_TAIL
WHOLE_STORE_UNAVAILABLE_SQL = f"""
SELECT id FROM record WHERE added_seq <= :at AND id IN {UNAVAILABLE} ORDER BY id
"""

RESULT_FOR_CONTEXT_SQL = """
SELECT e.id, r.id, r.v_datatype, r.v_lexical, r.v_unit
FROM context c
JOIN execution e ON e.context_id = c.id
JOIN record er ON er.id = e.id AND er.added_seq <= :at
JOIN result r ON r.execution_id = e.id
JOIN record rr ON rr.id = r.id AND rr.added_seq <= :at
WHERE c.id = :context
  AND (c.model_id IS NULL OR e.model_id = c.model_id)
  AND NOT EXISTS (SELECT parameter, assertion_id FROM binding WHERE owner_id = e.id
                  EXCEPT SELECT parameter, assertion_id FROM binding WHERE owner_id = c.id)
  AND NOT EXISTS (SELECT parameter, assertion_id FROM binding WHERE owner_id = c.id
                  EXCEPT SELECT parameter, assertion_id FROM binding WHERE owner_id = e.id)
ORDER BY e.id
"""

COMPARE_TWO_SQL = """
SELECT a.id = b.id AS same,
       json_array(
         CASE WHEN a.basis IS NOT b.basis THEN 'basis' END,
         CASE WHEN a.account_id IS NOT b.account_id THEN 'account' END,
         CASE WHEN a.subject_id IS NOT b.subject_id OR a.property IS NOT b.property THEN 'subject_property' END,
         CASE WHEN a.v_datatype IS NOT b.v_datatype OR a.v_lexical IS NOT b.v_lexical OR a.v_unit IS NOT b.v_unit THEN 'value' END,
         CASE WHEN a.app_kind IS NOT b.app_kind OR a.app_from IS NOT b.app_from OR a.app_until IS NOT b.app_until
                   OR a.app_instant IS NOT b.app_instant THEN 'applicability' END,
         CASE WHEN a.corrects_id IS NOT b.corrects_id OR a.revises_id IS NOT b.revises_id THEN 'revision_link' END)
FROM assertion a, assertion b WHERE a.id = :a AND b.id = :b
"""

PREMISE_CELLS_SQL = f"""
WITH {CELLS}
SELECT p.value AS aid, cur.app_kind, cur.valid_from, cur.valid_until, cur.instant
FROM json_each(:premises) p LEFT JOIN cur ON cur.aid = p.value
"""
COMMON_INTERVAL_SQL = f"""
WITH {CELLS}, c AS (SELECT * FROM cur WHERE aid IN (SELECT value FROM json_each(:premises)))
SELECT MAX(valid_from) < MIN(COALESCE(valid_until, '9999-12-31T23:59:59Z')) FROM c WHERE app_kind = 'INTERVAL'
"""
VALUE_CONFLICT_SQL = """
SELECT DISTINCT a.id FROM assertion a JOIN assertion b ON b.property = a.property AND b.id <> a.id
LEFT JOIN qualifier qa ON qa.owner_id = a.id AND qa.name = 'datum'
LEFT JOIN qualifier qb ON qb.owner_id = b.id AND qb.name = 'datum'
WHERE a.id IN (SELECT value FROM json_each(:premises)) AND b.id IN (SELECT value FROM json_each(:premises))
  AND (qa.lexical IS NOT qb.lexical OR a.v_unit IS NOT b.v_unit)
ORDER BY a.id
"""
GROUP_CONFLICT_SQL = """
SELECT DISTINCT m.graph_id FROM membership m JOIN claim_group g ON g.id = m.graph_id
JOIN record r ON r.id = g.id AND r.added_seq <= :at
WHERE m.member_id IN (SELECT value FROM json_each(:premises))
ORDER BY m.graph_id
"""


class Reader:
    """Answers G1 queries against one store. `labels` maps (assertion id, position) of a
    cell to the specimen's derived label; it only names outputs, it never selects."""

    def __init__(self, conn, labels: dict[tuple[str, str], str], policy: dict):
        self.conn, self.labels, self.policy = conn, labels, policy
        self.pos = dict(conn.execute("SELECT seq, position FROM change"))
        self.seq = {v: k for k, v in self.pos.items()}

    # helpers
    def rows(self, sql, **p):
        return self.conn.execute(sql, p).fetchall()

    def visible(self, rid, at) -> bool:
        return bool(self.rows("SELECT 1 FROM record WHERE id = :id AND added_seq <= :at", id=rid, at=at))

    def ref(self, aid, kfrom):
        return self.labels.get((aid, self.pos[kfrom]), aid)

    def value(self, table, rid):
        dt, lex, unit = self.rows(f"SELECT v_datatype, v_lexical, v_unit FROM {table} WHERE id = :id", id=rid)[0]
        v = {"datatype": dt, "lexical": lex}
        if unit is not None:
            v["unit"] = unit
        return v

    def cell_app(self, aid, kfrom):
        kind, frm, until, inst = self.rows(
            "SELECT app_kind, valid_from, valid_until, instant FROM temporal_effect WHERE op='OPEN' AND assertion_id=:a AND seq=:s",
            a=aid, s=kfrom)[0]
        return {"INTERVAL": {"kind": kind, "from": frm, "until": until},
                "INSTANT": {"kind": kind, "instant": inst}}.get(kind, {"kind": kind})

    def assertion(self, aid):
        return dict(zip(("subject", "property", "account", "basis"), self.rows(
            "SELECT subject_id, property, account_id, basis FROM assertion WHERE id = :id", id=aid)[0]))

    # selection
    def select_applicable(self, at, subject, prop, valid_at, account=None, context=None, rule=None):
        if prop == STATE_PROPERTY and not self.rows("SELECT 1 FROM assertion WHERE property = :p", p=prop):
            return self.select_state(at, subject, valid_at, rule)
        if account is None and context is None and self.policy.get("default_authority"):
            if self.visible(self.policy["default_authority"], at):
                context = self.policy["default_authority"]
        rows = self.rows(SELECT_APPLICABLE_SQL, at=at, subject=subject, property=prop, valid_at=valid_at,
                         account=account, context=context,
                         include_assumptions=int(bool(self.policy.get("include_assumptions"))))
        state = rows[0][0]
        covers = [(a, k) for _, a, k, s in rows if s == "COVERS"]
        unres = [(a, k) for _, a, k, s in rows if s == "UNRESOLVED"]
        ans = {"state": state, "selected_refs": [], "unresolved_refs": []}
        if state == "SELECTED":
            (aid, kfrom), = covers
            ans.update(selected_refs=[self.ref(aid, kfrom)], value=self.value("assertion", aid),
                       basis=self.assertion(aid)["basis"], applicability=self.cell_app(aid, kfrom))
            ans["_cell"] = (aid, kfrom)
        elif state == "AMBIGUOUS_SELECTION":
            ans["candidate_refs"] = [self.ref(a, k) for a, k in covers + unres]
        elif state == "UNRESOLVED_APPLICABILITY":
            ans["unresolved_refs"] = [self.ref(a, k) for a, k in unres]
        return ans

    def select_state(self, at, subject, valid_at, rule):
        if rule is None and self.policy.get("rule_default"):
            found = [r for (r,) in self.rows(DEFAULT_RULE_SQL, at=at, subject=subject)]
            rule = found[0] if len(found) == 1 else None
        if rule is not None and not self.visible(rule, at):
            raise ValueError(f"rule {rule} is not accepted at this position (OC-07-RULE-ACCEPTANCE branch 1)")
        n_ev, rule_ok, n_latest, aid, state, all_ev = self.rows(
            PERSISTENCE_SQL, at=at, subject=subject, valid_at=valid_at, rule=rule)[0]
        base = {"selected_refs": [], "unresolved_refs": []}
        if n_ev == 0:
            return {"state": "NO_ACCEPTED_ACCOUNT", **base}
        if not rule_ok:
            return {"state": "UNRESOLVED_APPLICABILITY", **base, "unresolved_refs": json.loads(all_ev)}
        if n_latest == 0:
            return {"state": "NO_APPLICABLE_ACCOUNT", **base}
        if n_latest > 1:
            return {"state": "AMBIGUOUS_SELECTION", **base, "candidate_refs": json.loads(all_ev)}
        return {"state": "SELECTED", **base, "derived_from_refs": [aid, rule],
                "value": {"datatype": "enum", "lexical": state}}

    def select_account(self, at, subject, prop, account=None):
        rows = self.rows(SELECT_ACCOUNT_SQL, at=at, subject=subject, property=prop, account=account,
                         include_assumptions=int(bool(self.policy.get("include_assumptions"))))
        if not rows:
            return {"state": "NO_ACCEPTED_ACCOUNT", "selected_refs": []}
        if len(rows) > 1:
            return {"state": "AMBIGUOUS_SELECTION", "selected_refs": [], "candidate_refs": [self.ref(a, k) for a, k in rows]}
        (aid, kfrom), = rows
        ans = {"state": "SELECTED", "selected_refs": [self.ref(aid, kfrom)], "value": self.value("assertion", aid),
               "basis": self.assertion(aid)["basis"], "applicability": self.cell_app(aid, kfrom), "_cell": (aid, kfrom)}
        args = self.arguments(at, aid)
        if args:
            ok = [g for g, changed in args.items() if not changed]
            if self.policy.get("sufficiency_rule") == "ANY_UNREVISED_ROUTE":
                meta = {"ref": aid, "support_sufficiency": "SUPPORTED" if ok else "NOT_SUPPORTED", "supporting_refs": ok}
            else:
                meta = {"ref": aid, "support_sufficiency": "NOT_ASSESSED"}
            ans["metadata"] = [meta]
        return ans

    def reselect(self, at, aid, valid_at=None, account=None):
        a = self.assertion(aid)
        account = account if account is not None else a["account"]
        if valid_at is not None:
            ans = self.select_applicable(at, a["subject"], a["property"], valid_at, account=account)
        else:
            ans = self.select_account(at, a["subject"], a["property"], account=account)
        return ans.get("_cell")

    def arguments(self, at, conclusion) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for g, p, changed in self.rows(ARGUMENTS_SQL, at=at, conclusion=conclusion):
            out.setdefault(g, [])
            if changed:
                out[g].append(p)
        return out

    # closure
    def missing(self, at, x, execution: bool):
        if self.policy.get("withheld_scope") == "WHOLE":
            return [r for (r,) in self.rows(WHOLE_STORE_UNAVAILABLE_SQL, at=at)]
        return [r for (r,) in self.rows(EXECUTION_CLOSURE_SQL if execution else LOOKUP_CLOSURE_SQL, at=at, x=x)]

    # query kinds
    def answer(self, kind: str, inputs: dict, absent_candidates=()) -> dict:
        at = self.seq[inputs["at"]]
        ans = getattr(self, "q_" + kind.lower())(at, inputs, absent_candidates)
        ans.pop("_cell", None)
        return ans

    def q_select_applicable(self, at, i, _):
        return self.select_applicable(at, i["subject_ref"], i["property"], i.get("valid_at"), account=i.get("account_ref"),
                                      context=i.get("context_ref"), rule=i.get("persistence_rule_ref"))

    def q_select_account(self, at, i, _):
        return self.select_account(at, i["subject_ref"], i["property"], account=i.get("account_ref"))

    def q_inspect_history(self, at, i, absent_candidates):
        if i.get("target_ref"):
            args = self.arguments(at, i["target_ref"])
            meta = []
            for g, changed in args.items():
                if self.policy.get("flag_source", "DERIVED") == "DERIVED":
                    flag = "REQUIRED" if changed else "NOT_REQUIRED"
                else:
                    flag = "NOT_RECORDED"  # the store has no reviewer-flag records
                meta.append({"ref": g, "reconsideration": flag, "changed_premise_refs": changed})
            return {"state": "QUALIFIED_HISTORY", "visible_refs": list(args), "metadata": meta}
        p = dict(at=at, subject=i["subject_ref"], property=i.get("property"))
        recs = self.rows(HISTORY_RECORDS_SQL, **p)
        visible, meta, kinds = [], [], []
        for rid, rtype in recs:
            visible.append(rid)
            if rtype == "ASSERTION":
                a = self.rows("SELECT basis, account_id, app_kind, app_from, app_until, app_instant FROM assertion WHERE id=:id", id=rid)[0]
                kinds.append(a[2])
                row = {"ref": rid, "basis": a[0], "account_ref": a[1], "applicability_kind": a[2]}
                if a[2] == "INTERVAL":
                    row.update(valid_from=a[3], valid_until=a[4])
                if a[2] == "INSTANT":
                    row["instant"] = a[5]
                meta.append(row)
            else:
                meta.append({"ref": rid, "type": rtype})
        for aid, kfrom, kind, frm, until, kuntil in self.rows(HISTORY_CELLS_SQL, **p):
            label = self.labels.get((aid, self.pos[kfrom]))
            if label is None:
                continue  # the specimen gives this cell no name; it is not reportable
            visible.append(label)
            meta.append({"ref": label, "assertion_ref": aid, "valid_from": frm, "valid_until": until,
                         "knowledge_from": self.pos[kfrom], "knowledge_until": self.pos.get(kuntil)})
        ans = {"state": "QUALIFIED_HISTORY", "visible_refs": visible, "metadata": meta}
        if kinds:
            ans["domain_time"] = ("NONE_STATED" if set(kinds) == {"NONE_STATED"}
                                  else "STATED" if "NONE_STATED" not in kinds else "MIXED")
        if absent_candidates:
            present = {r for (r,) in self.rows("SELECT id FROM record")}
            ans["absent_refs"] = [r for r in absent_candidates if r not in present]
        return ans

    def q_exact_lookup(self, at, i, _):
        x = i["target_ref"]
        if not self.visible(x, at):
            return {"state": "NO_ACCEPTED_ACCOUNT"}
        miss = self.missing(at, x, execution=False)
        if miss:
            return {"state": "INCOMPLETE_RECONSTRUCTION", "missing_refs": miss}
        otype = self.rows("SELECT type FROM record WHERE id=:id", id=x)[0][0]
        ans = {"state": "EXACT_OBJECT"}
        ev = [r for (r,) in self.rows("SELECT source_id FROM evidence WHERE owner_id=:id ORDER BY ord", id=x)]
        quals = {n: ({"datatype": d, "lexical": l} | ({"unit": u} if u is not None else {}))
                 for n, d, l, u in self.rows("SELECT name, datatype, lexical, unit FROM qualifier WHERE owner_id=:id", id=x)}
        groups = [g for (g,) in self.rows(
            "SELECT m.graph_id FROM membership m JOIN claim_group g ON g.id=m.graph_id JOIN record r ON r.id=g.id "
            "AND r.added_seq<=:at WHERE m.member_id=:id ORDER BY m.graph_id", id=x, at=at)]
        meta = {"ref": x, **{n: q["lexical"] for n, q in quals.items()}}
        if groups:
            meta["member_of"] = groups[0] if len(groups) == 1 else groups
        if otype == "ASSERTION":
            kind, frm, until, inst, basis = self.rows(
                "SELECT app_kind, app_from, app_until, app_instant, basis FROM assertion WHERE id=:id", id=x)[0]
            app = {"INTERVAL": {"kind": kind, "from": frm, "until": until}, "INSTANT": {"kind": kind, "instant": inst}}.get(kind, {"kind": kind})
            ans.update(value=self.value("assertion", x), applicability=app, basis=basis, evidence_refs=ev, qualifiers=quals)
            last = self.rows(f"WITH {CELLS} SELECT kuntil FROM cell WHERE aid=:id ORDER BY kfrom DESC LIMIT 1", at=at, id=x)
            meta["knowledge_until"] = self.pos.get(last[0][0]) if last else None
            for key, col in (("revised_by_ref", "revises_id"), ("corrected_by_ref", "corrects_id")):
                by = [r for (r,) in self.rows(f"SELECT a.id FROM assertion a JOIN record r ON r.id=a.id AND r.added_seq<=:at "
                                              f"WHERE a.{col}=:id ORDER BY a.id", at=at, id=x)]
                meta[key] = by[0] if len(by) == 1 else (by or None)
        elif otype == "RELATION":
            rtype, frm, to, basis = self.rows("SELECT relation_type, from_id, to_id, basis FROM relation WHERE id=:id", id=x)[0]
            ans.update(basis=basis, evidence_refs=ev, qualifiers=quals)
            meta.update(relation_type=rtype, from_ref=frm, to_ref=to)
        elif otype == "GROUP":
            members = [m for (m,) in self.rows("SELECT member_id FROM membership WHERE graph_id=:id ORDER BY ord", id=x)]
            rels = [r for (r,) in self.rows("SELECT r.id FROM relation r JOIN record rr ON rr.id=r.id AND rr.added_seq<=:at "
                                            "WHERE r.from_id=:id OR r.to_id=:id ORDER BY r.id", at=at, id=x)]
            ans.update(visible_refs=members + rels, evidence_refs=ev)
            rows = []
            for m in members:
                mq = self.rows("SELECT name, lexical FROM qualifier WHERE owner_id=:id", id=m)
                rows.append({"ref": m, **dict(mq)})
            ans["metadata"] = rows
            return ans
        elif otype == "MODEL":
            ans["visible_refs"] = [m for (m,) in self.rows("SELECT member_id FROM membership WHERE graph_id=:id ORDER BY ord", id=x)]
        elif otype == "RESULT":
            ans["value"] = self.value("result", x)
        ans["metadata"] = [meta]
        return ans

    def q_explain_execution(self, at, i, _):
        x = i["execution_ref"]
        if not self.visible(x, at):
            return {"state": "NO_ACCEPTED_ACCOUNT"}
        miss = self.missing(at, x, execution=True)
        if miss:
            return {"state": "INCOMPLETE_RECONSTRUCTION", "missing_refs": miss}
        model = self.rows("SELECT model_id FROM execution WHERE id=:id", id=x)[0][0]
        binds = self.rows("SELECT assertion_id, sel_at, sel_valid_at, sel_account_id FROM binding WHERE owner_id=:id ORDER BY ord", id=x)
        ans = {"state": "ORIGINAL_PREMISES_PRESERVED", "premise_refs": [b[0] for b in binds], "model_ref": model}
        res = self.rows("SELECT r.id FROM result r JOIN record rr ON rr.id=r.id AND rr.added_seq<=:at WHERE r.execution_id=:id", at=at, id=x)
        if len(res) == 1:
            ans.update(result_ref=res[0][0], value=self.value("result", res[0][0]))
        cells, sel_ats = [], set()
        for aid, sel_at, sel_valid, sel_acct in binds:
            if sel_at is None:
                continue
            sel_ats.add(sel_at)
            cell = self.reselect(self.seq[sel_at], aid, sel_valid, sel_acct)
            if cell is None or cell[0] != aid:
                raise AssertionError(f"{x}: recorded selection of {aid} at {sel_at} does not reproduce: {cell}")
            cells.append(self.ref(*cell))
        if sel_ats:
            ans["cell_refs"] = cells
            ans["selection_at"] = sel_ats.pop() if len(sel_ats) == 1 else sorted(sel_ats)
        return ans

    def q_compare_premises(self, at, i, _):
        if i.get("premise_refs"):
            a, b = i["premise_refs"]
            same, diffs = self.rows(COMPARE_TWO_SQL, a=a, b=b)[0]
            return {"state": "SAME_PREMISES" if same else "DIFFERENT_PREMISES",
                    "differences": [d for d in json.loads(diffs) if d]}
        x = i["execution_ref"]
        prev, new, new_cells = [], [], []
        for aid, sel_valid, sel_acct in self.rows(
                "SELECT assertion_id, sel_valid_at, sel_account_id FROM binding WHERE owner_id=:id ORDER BY ord", id=x):
            cell = self.reselect(at, aid, i.get("valid_at", sel_valid), i.get("account_ref", sel_acct))
            if cell is None:
                return {"state": "UNRESOLVED_REQUIRED_PREMISE", "unresolved_refs": [aid]}
            if cell[0] != aid:
                prev.append(aid)
                new.append(cell[0])
                new_cells.append(self.ref(*cell))
        if not prev:
            return {"state": "SAME_PREMISES"}
        return {"state": "SELECTED_PREMISES_CHANGED", "previous_refs": prev, "new_refs": new, "new_cell_refs": new_cells}

    def q_result_for_context(self, at, i, _):
        if not self.visible(i["context_ref"], at):
            return {"state": "NO_ACCEPTED_ACCOUNT"}
        rows = self.rows(RESULT_FOR_CONTEXT_SQL, at=at, context=i["context_ref"])
        if not rows:
            return {"state": "NOT_COMPUTED"}
        if len(rows) > 1:
            return {"state": "AMBIGUOUS_SELECTION", "candidate_refs": [r[1] for r in rows]}
        ex, rid, dt, lex, unit = rows[0]
        return {"state": "COMPUTED", "result_ref": rid, "value": self.value("result", rid), "execution_ref": ex}

    def q_result_for_selection(self, at, i, _):
        model = i.get("model_ref")
        if model is None or not self.visible(model, at):
            return {"state": "NOT_COMPUTED", "reason": "no executable model named" if model is None else "model not accepted"}
        execs = [e for (e,) in self.rows(
            "SELECT e.id FROM execution e JOIN record r ON r.id=e.id AND r.added_seq<=:at WHERE e.model_id=:m ORDER BY e.id", at=at, m=model)]
        for e in execs:
            binds = self.rows("SELECT assertion_id, sel_account_id FROM binding WHERE owner_id=:id", id=e)
            if i.get("subject_ref") and not any(self.assertion(a)["subject"] == i["subject_ref"] for a, _ in binds):
                continue
            if all((self.reselect(at, a, i.get("valid_at"), i.get("account_ref", acct)) or (None,))[0] == a for a, acct in binds):
                res = self.rows("SELECT r.id FROM result r JOIN record rr ON rr.id=r.id AND rr.added_seq<=:at WHERE r.execution_id=:e", at=at, e=e)
                if res:
                    return {"state": "COMPUTED", "result_ref": res[0][0], "value": self.value("result", res[0][0])}
        return {"state": "NOT_COMPUTED", "executions_considered": execs}

    def q_prepare_inputs(self, at, i, _):
        prem = json.dumps(i["premise_refs"])
        for p in i["premise_refs"]:
            if not self.visible(p, at):
                return {"state": "NO_ACCEPTED_ACCOUNT", "missing_refs": [p]}
        conflicts = [r for (r,) in self.rows(VALUE_CONFLICT_SQL, premises=prem)]
        if conflicts:
            return {"state": "INCOMPATIBLE_CONTEXTS", "conflict_refs": conflicts}
        if i.get("model_ref"):
            groups = [g for (g,) in self.rows(GROUP_CONFLICT_SQL, at=at, premises=prem)]
            if len(groups) > 1:
                return {"state": "INCOMPATIBLE_CONTEXTS", "conflict_refs": groups}
        cells = self.rows(PREMISE_CELLS_SQL, at=at, premises=prem)
        va = i.get("valid_at")
        if va is not None or i.get("same_time"):
            unresolved = [a for a, kind, *_ in cells if kind in (None, "NONE_STATED")]
            if unresolved:
                return {"state": "UNRESOLVED_REQUIRED_PREMISE", "unresolved_refs": unresolved}
        if va is not None:
            for a, kind, frm, until, inst in cells:
                covers = (kind == "INTERVAL" and frm <= va and (until is None or va < until)) or (kind == "INSTANT" and inst == va)
                if not covers:
                    return {"state": "NO_COMMON_APPLICABILITY", "conflict_refs": [a]}
        if i.get("same_time"):
            (ok,), = self.rows(COMMON_INTERVAL_SQL, at=at, premises=prem)
            if not ok:
                return {"state": "NO_COMMON_APPLICABILITY"}
        return {"state": "INPUTS_READY"}
