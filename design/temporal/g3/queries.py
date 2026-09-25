"""Evaluate every G1 query against Core's public reads.

Per expected field the status is CORE (Core's read equals the expected value),
CORE_WRONG (Core's read gives a different value) or NOT_EXPRESSIBLE (no public
read or contract construct poses it). The query's class is ANSWERED_WRONG if any
field is CORE_WRONG, else NOT_EXPRESSIBLE if any field is, else ANSWERED_CORRECT.
See the harness rule in driver.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import json

from driver import (
    ASSERTION_TYPES,
    CORRECT,
    NOT_EXPRESSIBLE,
    WRONG,
    Run,
)

CORE = "CORE"
CORE_WRONG = "CORE_WRONG"
NE = "NOT_EXPRESSIBLE"


@dataclass
class Field:
    name: str
    status: str
    core: object
    expected: object
    note: str = ""


@dataclass
class QueryOutcome:
    specimen: str
    query_id: str
    kind: str
    branch: str | None
    classification: str
    fields: list[Field]
    core_part: str
    harness_part: str
    notes: list[str] = field(default_factory=list)
    naive: dict = field(default_factory=dict)
    forbidden_hit: list[str] = field(default_factory=list)


def thaw(value):
    if hasattr(value, "items"):
        return {k: thaw(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [thaw(v) for v in value]
    return value


def props(entry) -> dict:
    return thaw(entry.operation.properties)


def parse(instant: str) -> datetime:
    return datetime.fromisoformat(instant.replace("Z", "+00:00"))


def same(core, expected) -> bool:
    if isinstance(expected, list) and isinstance(core, (list, set, tuple)):
        return sorted(map(str, core)) == sorted(map(str, expected))
    return core == expected


def classify(fields: list[Field]) -> str:
    statuses = {f.status for f in fields}
    if CORE_WRONG in statuses:
        return WRONG
    if NE in statuses:
        return NOT_EXPRESSIBLE
    return CORRECT


class Reader:
    """Core reads at one position, plus the label mappings the harness may do."""

    def __init__(self, run: Run, label: str, replay=None):
        self.run = run
        self.label = label
        self.replay = replay if replay is not None else run.at(label)
        self.history = self.replay.record_history
        self.change_sets = {c.change_set_id: c for c in self.replay.change_sets}
        spec = run.driver.spec
        self.derived = {d["id"]: d for d in spec.get("derived_labels", [])}

    def entry(self, record_id):
        return self.history.get(record_id)

    def current_ids(self) -> set[str]:
        graph = self.replay.graph
        ids = {row["id"] for row in graph.query()}
        ids |= {row["key"] for row in graph.query_relations()}
        return ids

    def position_of(self, change_set_id: str) -> str:
        return self.run.label_of_change(change_set_id)

    def superseded_at(self, record_id) -> str | None:
        entry = self.entry(record_id)
        if entry is None or entry.superseded_by is None:
            return None
        return self.position_of(self.entry(entry.superseded_by).change_set_id)

    def sources(self, record_id) -> list[str]:
        change = self.change_sets[self.entry(record_id).change_set_id]
        return sorted(s for s, _ in change.sources if not s.startswith("decl:"))

    def applicability(self, record_id) -> dict:
        entry = self.entry(record_id)
        vt = entry.valid_from
        if entry.operation.operation_type == "CREATE_EVENT":
            return {"kind": "INSTANT", "instant": vt.value}
        if vt.kind == "NONE_STATED":
            return {"kind": "NONE_STATED"}
        if vt.kind == "INSTANT":
            return {"kind": "INTERVAL", "from": vt.value, "until": props(entry).get("stated_until")}
        return {"kind": vt.kind, "value": vt.value}

    def assertions(self, subject, prop=None, account=None, current_only=False):
        ids = self.current_ids() if current_only else set(self.history)
        out = []
        for record_id in sorted(ids):
            entry = self.entry(record_id)
            if entry is None or entry.operation.record_type not in ASSERTION_TYPES:
                continue
            p = props(entry)
            if p.get("subject") != subject or (prop is not None and p.get("property") != prop):
                continue
            if account is not None and p.get("account") != account:
                continue
            out.append(record_id)
        return out

    def records_of(self, record_type, **where):
        out = []
        for record_id, entry in sorted(self.history.items()):
            if entry.operation.record_type != record_type:
                continue
            p = props(entry)
            if all(p.get(k) == v for k, v in where.items()):
                out.append(record_id)
        return out

    def version_here(self, label: str) -> str | None:
        """The record whose entry in this read is that derived version, if any."""
        record = self.derived[label]["from_assertion_ref"]
        if record in self.history and self.label_for(record) == label:
            return record
        return None

    def label_for(self, record_id) -> str:
        """A derived label (a1, a2, b, c) for a record at this position, if any."""
        order = self.run.driver.order
        here = order.index(self.label)
        best = None
        for label, d in self.derived.items():
            if d["from_assertion_ref"] == record_id and order.index(d["knowledge_from"]) <= here:
                if best is None or order.index(d["knowledge_from"]) > order.index(self.derived[best]["knowledge_from"]):
                    best = label
        return best or record_id


def _value_field(name, core, expected, note=""):
    return Field(name, CORE if same(core, expected) else CORE_WRONG, core, expected, note)


def _ne(expected: dict, reason: str, skip=("",)) -> list[Field]:
    return [Field(k, NE, None, v, reason) for k, v in expected.items() if k not in skip]


# --- per kind ---------------------------------------------------------------------


def exact_lookup(reader: Reader, q, expected):
    target = q["inputs"]["target_ref"]
    entry = reader.entry(target)
    fields = []
    core = {}
    notes: list[str] = []
    if entry is None:
        return [Field("state", CORE_WRONG, "NO_RECORD", expected.get("state"))], {}, notes
    p = props(entry)
    for key, value in expected.items():
        if key == "state":
            core[key] = "EXACT_OBJECT"
        elif key == "value":
            core[key] = p.get("assertion_value", p.get("result_value"))
        elif key == "applicability":
            core[key] = reader.applicability(target)
            if entry.valid_to is not None:
                notes.append(
                    f"record_history[{target}].valid_to is {entry.valid_to.kind} {entry.valid_to.value}, "
                    "Core's period end derived from the successor's start. The report's own time is "
                    "the valid time of the change set that added it; reading valid_to as the report's "
                    "end would give the forbidden answer."
                )
        elif key == "evidence_refs":
            core[key] = reader.sources(target)
        elif key == "qualifiers":
            core[key] = {k[2:]: v for k, v in p.items() if k.startswith("q_")}
        elif key == "basis":
            core[key] = p.get("basis")
        elif key == "visible_refs":
            members = list(p.get("member_refs", []))
            relations = [
                rid
                for rid, e in reader.history.items()
                if e.operation.operation_type == "CREATE_RELATION" and e.operation.source_id == target
                and e.operation.record_type != "UsesModel"
            ]
            core[key] = members + relations
        elif key == "metadata":
            core[key] = [metadata_row(reader, row) for row in value]
            for row_core, row in zip(core[key], value):
                for name in row:
                    if name == "ref":
                        continue
                    fields.append(_value_field(f"metadata[{row['ref']}].{name}", row_core.get(name), row[name]))
            continue
        else:
            raise KeyError(f"unhandled EXACT_LOOKUP field {key}")
        fields.append(_value_field(key, core[key], value))
    return fields, core, notes


def metadata_row(reader: Reader, row: dict) -> dict:
    ref = row["ref"]
    entry = reader.entry(ref)
    p = props(entry)
    out = {"ref": ref}
    for name in row:
        if name == "ref":
            continue
        if name in {"approximate", "datum", "role"}:
            out[name] = (p.get(f"q_{name}") or {}).get("lexical")
        elif name == "member_of":
            groups = [g for g in reader.records_of("Group") if ref in props(reader.entry(g))["member_refs"]]
            out[name] = groups[0] if len(groups) == 1 else groups
        elif name == "knowledge_until":
            out[name] = reader.superseded_at(ref)
        elif name == "revised_by_ref":
            out[name] = entry.superseded_by
        elif name == "from_ref":
            out[name] = entry.operation.source_id
        elif name == "to_ref":
            out[name] = entry.operation.target_id
        elif name == "relation_type":
            out[name] = p.get("relation_type")
        elif name == "basis":
            out[name] = p.get("basis")
        elif name == "instant":
            out[name] = entry.valid_from.value
        else:
            out[name] = ("NOT_EXPRESSIBLE", name)
    return out


def inspect_history(reader: Reader, q, expected):
    inputs = q["inputs"]
    if "target_ref" in inputs:
        visible = reader.records_of("Argument", conclusion_ref=inputs["target_ref"])
    elif inputs.get("property") == "plan":
        visible = reader.records_of("Plan", subject=inputs["subject_ref"])
    elif "property" in inputs:
        visible = reader.assertions(inputs["subject_ref"], inputs["property"])
    else:
        subject = inputs["subject_ref"]
        visible = reader.assertions(subject) + [
            rid
            for rid, e in reader.history.items()
            if e.operation.operation_type == "CREATE_RELATION" and e.operation.source_id == subject
        ]
    fields, core = [], {"state": "QUALIFIED_HISTORY", "visible_refs": visible}
    derived = set(reader.derived)
    for key, value in expected.items():
        if key == "state":
            fields.append(Field(key, CORE, "QUALIFIED_HISTORY", value))
        elif key == "visible_refs":
            records = [v for v in value if v not in derived]
            here = [v for v in value if v in derived and reader.version_here(v)]
            older = [v for v in value if v in derived and not reader.version_here(v)]
            core[key] = visible + here
            if not same(visible, records):
                fields.append(Field(key, CORE_WRONG, visible, value))
            elif older:
                fields.append(
                    Field(
                        key, NE, core[key], value,
                        "records and current versions match; older versions " + ", ".join(older)
                        + " are reachable only by replay_at at their own position, and no read lists them",
                    )
                )
            else:
                fields.append(Field(key, CORE, core[key], value, "versions mapped as (record, this position)"))
        elif key == "absent_refs":
            present = [v for v in value if v in reader.history]
            fields.append(Field(key, CORE if not present else CORE_WRONG, present, [], "absent means no record in history"))
        elif key == "domain_time":
            kinds = sorted({reader.entry(v).valid_from.kind for v in visible})
            core[key] = kinds[0] if len(kinds) == 1 else kinds
            fields.append(_value_field(key, core[key], value))
        elif key == "metadata":
            for row in value:
                if row["ref"] in derived:
                    record = reader.version_here(row["ref"])
                    for name in row:
                        if name == "ref":
                            continue
                        label = f"metadata[{row['ref']}].{name}"
                        if record is None:
                            fields.append(Field(label, NE, None, row[name], "older version: not in this read"))
                        elif name == "valid_until":
                            vt = reader.entry(record).valid_to
                            fields.append(_value_field(label, vt.value if vt else None, row[name]))
                        elif name == "knowledge_until":
                            fields.append(
                                _value_field(
                                    label, reader.superseded_at(record), row[name],
                                    f"Core's answer: the position where {record} was superseded, "
                                    "after which only the replacement is current",
                                )
                            )
                        else:
                            fields.append(Field(label, NE, None, row[name]))
                    continue
                core_row = metadata_row(reader, row) if row["ref"] in reader.history else {}
                for name in row:
                    if name == "ref":
                        continue
                    if name == "reconsideration":
                        fields.append(
                            Field(f"metadata[{row['ref']}].{name}", NE, None, row[name], "Core has no reconsideration flag")
                        )
                    elif name == "changed_premise_refs":
                        premises = props(reader.entry(row["ref"]))["premise_refs"]
                        changed = [x for x in premises if reader.entry(x) is not None and reader.entry(x).superseded_by]
                        fields.append(_value_field(f"metadata[{row['ref']}].{name}", changed, row[name]))
                    else:
                        fields.append(_value_field(f"metadata[{row['ref']}].{name}", core_row.get(name), row[name]))
        else:
            raise KeyError(f"unhandled INSPECT_HISTORY field {key}")
    return fields, core


def select_account(reader: Reader, q, expected):
    inputs = q["inputs"]
    candidates = reader.assertions(
        inputs["subject_ref"], inputs["property"], inputs.get("account_ref"), current_only=True
    )
    state = {0: "NO_ACCEPTED_ACCOUNT", 1: "SELECTED"}.get(len(candidates), "AMBIGUOUS_SELECTION")
    core = {"state": state, "selected_refs": candidates if state == "SELECTED" else []}
    if state == "SELECTED":
        p = props(reader.entry(candidates[0]))
        core.update(value=p["assertion_value"], applicability=reader.applicability(candidates[0]), basis=p["basis"])
    fields = []
    for key, value in expected.items():
        if key == "metadata":
            for row in value:
                for name in row:
                    if name != "ref":
                        fields.append(
                            Field(f"metadata[{row['ref']}].{name}", NE, None, row[name], "Core has no support or sufficiency field")
                        )
            continue
        fields.append(_value_field(key, core.get(key), value))
    return fields, core


def naive_select(reader: Reader, q, current_only: bool):
    """Harness work, not Core: interval containment over Core's valid_from/valid_to."""
    inputs = q["inputs"]
    if inputs.get("context_ref") or inputs.get("persistence_rule_ref"):
        return None
    candidates = reader.assertions(
        inputs["subject_ref"], inputs["property"], inputs.get("account_ref"), current_only=current_only
    )
    t = parse(inputs["valid_at"])
    applicable, unresolved = [], []
    for record_id in candidates:
        entry = reader.entry(record_id)
        vf = entry.valid_from
        vt = None if current_only else entry.valid_to
        if vf.kind != "INSTANT":
            unresolved.append(record_id)
            continue
        end = parse(vt.value) if vt is not None and vt.kind == "INSTANT" else None
        if parse(vf.value) <= t and (end is None or t < end):
            applicable.append(record_id)
    if not candidates:
        state = "NO_ACCEPTED_ACCOUNT"
    elif len(applicable) == 1:
        state = "SELECTED"
    elif len(applicable) > 1:
        state = "AMBIGUOUS_SELECTION"
    elif unresolved:
        state = "UNRESOLVED_APPLICABILITY"
    else:
        state = "NO_APPLICABLE_ACCOUNT"
    answer = {
        "state": state,
        "selected_refs": [reader.label_for(r) for r in applicable] if state == "SELECTED" else [],
        "unresolved_refs": unresolved if state == "UNRESOLVED_APPLICABILITY" else [],
        "candidate_refs": applicable if state == "AMBIGUOUS_SELECTION" else [],
    }
    if state == "SELECTED":
        p = props(reader.entry(applicable[0]))
        answer["value"] = p["assertion_value"]
        answer["basis"] = p["basis"]
    return answer


def compare(answer: dict, expected: dict) -> bool:
    return all(same(answer.get(k), v) for k, v in expected.items())


def forbidden_hits(spec, query_id, answer) -> list[str]:
    hits = []
    for entry in spec.get("forbidden", []):
        if entry["query_ref"] == query_id and all(
            same(answer.get(k), v) if k != "metadata" else _meta_hit(answer.get(k), v)
            for k, v in entry["answer"].items()
        ):
            hits.append(entry["why"])
    return hits


def _meta_hit(core_rows, rows) -> bool:
    if not core_rows:
        return False
    by_ref = {r["ref"]: r for r in core_rows}
    return all(
        all(by_ref.get(row["ref"], {}).get(k) == v for k, v in row.items() if k != "ref") for row in rows
    )


# --- dispatch ---------------------------------------------------------------------

REASON_SELECT = "no Core read takes a domain time, account precedence, named-use context or persistence rule"


def evaluate(run: Run, q: dict, expected: dict, branch: str | None, reader: Reader) -> QueryOutcome:
    kind = q["kind"]
    inputs = q["inputs"]
    spec = run.driver.spec
    notes: list[str] = []
    naive: dict = {}
    core: dict = {}
    if kind == "EXACT_LOOKUP":
        if inputs.get("withheld_refs"):
            fields = _ne(expected, "no public API rebuilds a history with a retained artifact withheld")
            core_part, harness_part = "none; see probe P-WITHHELD", "none"
        else:
            fields, core, extra = exact_lookup(reader, q, expected)
            notes.extend(extra)
            core_part = "replay_at(at).record_history[target]; its change set's valid time and source closure"
            harness_part = "label mapping and field projection"
    elif kind == "INSPECT_HISTORY":
        fields, core = inspect_history(reader, q, expected)
        core_part = "replay_at(at).record_history, all accepted records including superseded ones"
        harness_part = "equality filter on subject/property (or conclusion_ref); label mapping"
    elif kind == "SELECT_ACCOUNT":
        fields, core = select_account(reader, q, expected)
        core_part = "replay_at(at).graph, Core's current non-superseded records"
        harness_part = "equality filter on subject/property/account; empty/one/many mapped to state"
    elif kind == "SELECT_APPLICABLE":
        fields = _ne(expected, REASON_SELECT)
        core_part = "none"
        harness_part = "naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately"
        for mode, current in (("H-hist", False), ("H-curr", True)):
            answer = naive_select(reader, q, current)
            if answer is None:
                naive[mode] = {"answer": None, "verdict": "N/A: needs a context or persistence rule"}
                continue
            hits = forbidden_hits(spec, q["id"], answer)
            verdict = "MATCH" if compare(answer, expected) else ("FORBIDDEN" if hits else "DIFFERS")
            naive[mode] = {"answer": {k: answer.get(k) for k in expected}, "verdict": verdict}
    elif kind == "RESULT_FOR_CONTEXT":
        executions = reader.records_of("Execution", context_ref=inputs["context_ref"])
        results = [r for r in reader.records_of("Result") if props(reader.entry(r))["execution_ref"] in executions]
        core = {"state": "COMPUTED" if results else "NOT_COMPUTED"}
        if results:
            core.update(result_ref=results[0], value=props(reader.entry(results[0]))["result_value"])
        fields = [_value_field(k, core.get(k), v) for k, v in expected.items()]
        core_part = "replay_at(at).record_history: Execution and Result records"
        harness_part = "equality filter context_ref, execution_ref; empty mapped to NOT_COMPUTED"
    elif kind == "RESULT_FOR_SELECTION":
        if inputs.get("valid_at"):
            fields = _ne(expected, "the premise must first be selected by domain time and account")
            executions = reader.records_of("Execution", model_ref=inputs["model_ref"])
            results = [r for r in reader.records_of("Result") if props(reader.entry(r))["execution_ref"] in executions]
            naive["model-only"] = {
                "answer": {"state": "COMPUTED" if results else "NOT_COMPUTED", "result_refs": results},
                "verdict": "DIFFERS" if results else "MATCH",
            }
            core_part, harness_part = "none", "a lookup by model alone, reported as naive"
        else:
            executions = [
                e for e in reader.records_of("Execution")
                if inputs.get("model_ref") in (None, props(reader.entry(e))["model_ref"])
            ]
            results = [r for r in reader.records_of("Result") if props(reader.entry(r))["execution_ref"] in executions]
            core = {"state": "COMPUTED" if results else "NOT_COMPUTED"}
            fields = [_value_field(k, core.get(k), v) for k, v in expected.items()]
            core_part = "replay_at(at).record_history: no Result record for that model"
            harness_part = "equality filter; empty mapped to NOT_COMPUTED"
    elif kind == "EXPLAIN_EXECUTION":
        if inputs.get("withheld_refs"):
            fields = _ne(expected, "no public API rebuilds a history with a retained artifact withheld")
            core_part, harness_part = "none; see probe P-WITHHELD", "none"
        else:
            fields, core, extra = explain_execution(reader, q, expected)
            notes.extend(extra)
            core_part = "replay_at(at).record_history of the execution, its result, and replay_at(stored coordinates) for the old premise"
            harness_part = "list projection of bindings; coordinate-to-label mapping"
    elif kind == "COMPARE_PREMISES":
        if inputs.get("premise_refs"):
            a, b = inputs["premise_refs"]
            ea, eb = reader.entry(a), reader.entry(b)
            state = "DIFFERENT_PREMISES" if (ea and eb and a != b) else "SAME_PREMISES"
            core = {"state": state}
            fields = [_value_field("state", state, expected["state"])]
            pa, pb = props(ea), props(eb)
            notes.append(
                f"{a} and {b}: equal value {pa['assertion_value'] == pb['assertion_value']}, "
                f"basis {pa['basis']} vs {pb['basis']}, account {pa.get('account')} vs {pb.get('account')}"
            )
            core_part = "two distinct accepted record identities"
            harness_part = "identity comparison"
        else:
            fields = _ne(expected, "the new premise must be selected by domain time and account")
            core_part, harness_part = "none", "none"
    elif kind == "PREPARE_INPUTS":
        fields = _ne(expected, "Core has no premise-compatibility or common-applicability operation")
        core_part, harness_part = "none", "none"
    else:
        raise KeyError(kind)
    hits = forbidden_hits(spec, q["id"], core) if core else []
    fallback = run.fallback_records
    fallback |= {label for label, d in reader.derived.items() if d["from_assertion_ref"] in fallback}
    mentioned = {token for token in fallback if f'"{token}"' in json.dumps([core, expected], default=str)}
    if mentioned and any(f.status == CORE for f in fields):
        notes.append(
            "Reached through the fallback encoding: " + ", ".join(sorted(mentioned))
            + " was admitted as a plain addition after Core refused the declared correction."
        )
    return QueryOutcome(
        run.key, q["id"], kind, branch, classify(fields), fields, core_part, harness_part, notes, naive, hits
    )


def explain_execution(reader: Reader, q, expected):
    execution = q["inputs"]["execution_ref"]
    entry = reader.entry(execution)
    p = props(entry)
    premises = [b["assertion_ref"] for b in p["input_bindings"]]
    results = [r for r in reader.records_of("Result") if props(reader.entry(r))["execution_ref"] == execution]
    core = {
        "state": "ORIGINAL_PREMISES_PRESERVED" if all(reader.entry(x) for x in premises) else "INCOMPLETE_RECONSTRUCTION",
        "premise_refs": premises,
        "model_ref": p["model_ref"],
        "result_ref": results[0] if results else None,
        "value": props(reader.entry(results[0]))["result_value"] if results else None,
    }
    notes = []
    coords = {
        (b.get("selection_ledger_head"), b.get("selection_ledger_event_count"))
        for b in p["input_bindings"]
        if b.get("selection_ledger_head")
    }
    if coords:
        (head, count), = coords
        labels = [label for label, pos in reader.run.positions.items() if pos == (head, count)]
        core["selection_at"] = labels[0] if len(labels) == 1 else labels
        final = reader.run.history.replay()
        old = reader.run.history.replay_at(
            ledger_head=head,
            ledger_event_count=count,
            expected_head_hash=final.ledger_head,
            expected_event_count=final.ledger_event_count,
        )
        for premise in premises:
            e = old.record_history[premise]
            notes.append(
                f"replay_at(stored selection coordinates) returns {premise} = "
                f"{props(e)['assertion_value']['lexical']}, valid_to {e.valid_to}, superseded_by {e.superseded_by}"
            )
    fields = []
    for key, value in expected.items():
        if key == "cell_refs" and "selection_at" in core:
            at = Reader(reader.run, core["selection_at"])
            core[key] = [at.label_for(x) for x in premises]
            fields.append(_value_field(key, core[key], value, "(premise, stored selection position) mapped to its version label"))
        elif key == "cell_refs":
            fields.append(Field(key, NE, None, value, "no stored position to address the version by"))
        else:
            fields.append(_value_field(key, core.get(key), value))
    return fields, core, notes


def evaluate_specimen(run: Run, after_refusal: dict | None = None) -> list[QueryOutcome]:
    spec = run.driver.spec
    choices = {c["id"]: c for c in spec.get("open_choices", [])}
    outcomes = []
    readers: dict[str, Reader] = {}
    for q in spec["queries"]:
        label = q["inputs"]["at"]
        refusal = q["inputs"].get("after_refusal_ref")
        if refusal:
            history = after_refusal[refusal]
            replay = history.replay()
            at_label = run.at(label)
            # The attempt retained its evidence before the refused admission, so
            # the head moved by retention events; the accepted state must not.
            assert replay.record_history == at_label.record_history
            assert replay.graph.state_digest() == at_label.graph.state_digest()
            reader = Reader(run, label, replay)
        else:
            reader = readers.setdefault(label, Reader(run, label))
        if q["expected"] is None:
            choice = choices[q["open_choice_ref"]]
            for branch in choice["branches"]:
                outcomes.append(evaluate(run, q, branch["expected"][q["id"]], branch["label"], reader))
        else:
            outcomes.append(evaluate(run, q, q["expected"], None, reader))
    return outcomes
