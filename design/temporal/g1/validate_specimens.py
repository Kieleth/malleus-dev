#!/usr/bin/env python3
"""Validate G1 temporal specimens against SCHEMA.md. Standard library only.

Usage: python validate_specimens.py [directory]   (default: this file's directory)
Exit status 0 when every g1-*.json file passes, 1 otherwise.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA_TAG = "malleus.temporal-g1-specimen/draft-1"

OBLIGATIONS = {
    "FULL_GRAPH_ROUND_TRIP", "HISTORICAL_READ", "SAME_VALUE_DIFFERENT_MEANING",
    "UNKNOWN_APPLICABILITY", "EXACT_OLD_USE", "COHERENT_CONDITIONS",
    "ALTERNATE_JUSTIFICATION", "REPLAY_REBUILD", "MISSING_CLOSURE_REFUSES",
    "FAILED_WRITE_NO_PARTIAL_STATE", "DECLARED_PERSISTENCE",
}
ORIGIN_BASES = {"SYNTHETIC", "EXISTING_SYNTHETIC_EXAMPLE", "REAL_SOURCE_POINTER"}
SOURCE_KINDS = {"SYNTHETIC_TEXT", "RETAINED_DECLARATION", "REAL_BLOCK_POINTER"}
BASES = {"REPORTED", "ASSUMPTION", "CORRECTION", "INTERPRETATION"}
DATATYPES = {"xsd:integer", "xsd:decimal", "xsd:string", "xsd:boolean", "xsd:dateTime", "enum"}
APPLICABILITY_KINDS = {"INTERVAL", "INSTANT", "NONE_STATED"}
CHANGE_KINDS = {
    "GENESIS", "REPORT", "TRANSITION", "CORRECTION", "ASSUMPTION", "INTERPRETATION",
    "REASSESSMENT", "ARGUMENT", "MODEL_DEFINITION", "CONTEXT_BINDING",
    "EXECUTION_RECORD", "RULE_DECLARATION", "PLAN", "CONTRACT_DECLARATION",
}
QUERY_KINDS = {
    "SELECT_APPLICABLE", "SELECT_ACCOUNT", "INSPECT_HISTORY", "EXACT_LOOKUP",
    "RESULT_FOR_CONTEXT", "RESULT_FOR_SELECTION", "EXPLAIN_EXECUTION",
    "COMPARE_PREMISES", "PREPARE_INPUTS",
}
STATES = {
    "SELECTED", "NO_ACCEPTED_ACCOUNT", "NO_APPLICABLE_ACCOUNT", "UNRESOLVED_APPLICABILITY",
    "AMBIGUOUS_SELECTION", "QUALIFIED_HISTORY", "EXACT_OBJECT", "COMPUTED", "NOT_COMPUTED",
    "ORIGINAL_PREMISES_PRESERVED", "SELECTED_PREMISES_CHANGED", "SAME_PREMISES",
    "DIFFERENT_PREMISES", "NO_COMMON_APPLICABILITY", "UNRESOLVED_REQUIRED_PREMISE",
    "INPUTS_READY", "INCOMPATIBLE_CONTEXTS", "INCOMPLETE_RECONSTRUCTION",
}
REFUSAL_CATEGORIES = {
    "STALE_BASE", "STALE_TARGET", "MISSING_EVIDENCE", "MISSING_MODEL", "MISSING_CONTRACT",
    "UNKNOWN_REFERENCE", "UNSUPPORTED_SEMANTICS", "PREMISE_MISMATCH",
}

TOP_REQUIRED = {"schema", "specimen_id", "obligation", "origin", "objects", "changes",
                "queries", "forbidden", "refusals", "open_choices"}
TOP_OPTIONAL = {"reused_files", "derived_labels", "rejected_objects", "phantom_ids", "note"}

COMMON_OPTIONAL = {"note", "contract_ref"}
OBJECT_FIELDS = {  # type: (required, optional)
    "SUBJECT": ({"label"}, set()),
    "ACCOUNT": ({"label"}, set()),
    "SOURCE": ({"source_kind", "text"}, {"locator", "pointer"}),
    "CONTRACT": ({"version", "identity"}, set()),
    "ASSERTION": ({"subject_ref", "property", "value", "basis", "applicability", "evidence_refs"},
                  {"qualifiers", "account_ref", "corrects_ref", "revises_ref"}),
    "RELATION": ({"relation_type", "from_ref", "to_ref"}, {"qualifiers", "basis", "evidence_refs"}),
    "GROUP": ({"group_kind", "member_refs"}, {"evidence_refs"}),
    "ARGUMENT": ({"premise_refs", "conclusion_ref"}, {"evidence_refs"}),
    "CONTEXT": ({"context_kind", "bindings"}, {"model_ref", "basis_refs"}),
    "MODEL": ({"version", "implementation", "formula", "parameters"}, {"member_refs"}),
    "EXECUTION": ({"model_ref", "input_bindings"}, {"context_ref", "implementation"}),
    "RESULT": ({"execution_ref", "value"}, set()),
    "RULE": ({"semantics", "scope_refs", "assumptions"}, set()),
    "PLAN": ({"subject_ref", "action", "planned_for", "evidence_refs"}, set()),
}
INPUT_KEYS = {"at", "valid_at", "subject_ref", "property", "account_ref", "context_ref", "target_ref",
              "execution_ref", "model_ref", "premise_refs", "same_time", "withheld_refs",
              "after_refusal_ref", "persistence_rule_ref"}
EXPECTED_KEYS = {"state", "selected_refs", "unresolved_refs", "candidate_refs", "derived_from_refs",
                 "value", "basis", "applicability", "qualifiers", "evidence_refs", "visible_refs",
                 "absent_refs", "metadata", "premise_refs", "cell_refs", "selection_at", "model_ref",
                 "result_ref", "previous_refs", "new_refs", "new_cell_refs", "conflict_refs",
                 "missing_refs", "domain_time"}
POSITION_KEYS = {"at", "position", "head", "base", "head_after", "selection_at",
                 "knowledge_from", "knowledge_until"}
NULLABLE_POSITION_KEYS = {"knowledge_until"}
DATETIME_KEYS = {"valid_at", "from", "until", "instant", "planned_for"}
DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
LEXICAL_RE = {
    "xsd:integer": re.compile(r"^-?(0|[1-9]\d*)$"),
    "xsd:decimal": re.compile(r"^-?(0|[1-9]\d*)\.\d+$|^-?(0|[1-9]\d*)$"),
    "xsd:boolean": re.compile(r"^(true|false)$"),
    "xsd:dateTime": DATETIME_RE,
}
# expected-views keys -> how they are checked against a specimen query
IGNORED_EXTERNAL_KEYS = {"id", "request", "forbidden", "meaning"}


def is_ref_key(key: str) -> bool:
    return key == "ref" or key.endswith("_ref") or key.endswith("_refs")


def walk_refs(node, path=""):
    """Yield (path, id) for every reference in node, by the key-suffix convention."""
    if isinstance(node, dict):
        for key, val in node.items():
            here = f"{path}.{key}" if path else key
            if is_ref_key(key):
                if key.endswith("_refs"):
                    if not isinstance(val, list):
                        yield here, ("__NOT_A_LIST__", val)
                        continue
                    for i, item in enumerate(val):
                        yield f"{here}[{i}]", item
                elif val is not None:
                    yield here, val
            else:
                yield from walk_refs(val, here)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            yield from walk_refs(item, f"{path}[{i}]")


def walk_keys(node, keys, path=""):
    """Yield (path, value) for every dict entry whose key is in keys."""
    if isinstance(node, dict):
        for key, val in node.items():
            here = f"{path}.{key}" if path else key
            if key in keys:
                yield here, key, val
            yield from walk_keys(val, keys, here)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            yield from walk_keys(item, keys, f"{path}[{i}]")


def resolve_pointer(doc, pointer: str):
    cur = doc
    for part in [p for p in pointer.split("/") if p != ""]:
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    return cur


class Checker:
    def __init__(self, path: Path):
        self.path = path
        self.errors: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(f"{self.path.name}: {msg}")

    # -- literals ---------------------------------------------------------
    def literal(self, lit, where: str) -> None:
        if not isinstance(lit, dict) or set(lit) - {"datatype", "lexical", "unit"} or not {"datatype", "lexical"} <= set(lit):
            self.err(f"{where}: typed literal must have datatype, lexical and optional unit")
            return
        dt, lex = lit["datatype"], lit["lexical"]
        if dt not in DATATYPES:
            self.err(f"{where}: datatype {dt!r} not allowed")
        if not isinstance(lex, str):
            self.err(f"{where}: lexical must be a string, got {type(lex).__name__}")
        elif dt in LEXICAL_RE and not LEXICAL_RE[dt].match(lex):
            self.err(f"{where}: lexical {lex!r} is not a valid {dt}")
        if "unit" in lit and not isinstance(lit["unit"], str):
            self.err(f"{where}: unit must be a string")

    def applicability(self, app, where: str) -> None:
        if not isinstance(app, dict) or app.get("kind") not in APPLICABILITY_KINDS:
            self.err(f"{where}: applicability kind must be one of {sorted(APPLICABILITY_KINDS)}")
            return
        kind = app["kind"]
        allowed = {"INTERVAL": {"kind", "from", "until"}, "INSTANT": {"kind", "instant"}, "NONE_STATED": {"kind"}}[kind]
        if set(app) != allowed:
            self.err(f"{where}: {kind} applicability must have exactly {sorted(allowed)}")
            return
        if kind == "INTERVAL" and isinstance(app["from"], str) and isinstance(app["until"], str) and app["from"] >= app["until"]:
            self.err(f"{where}: interval start must precede its end")

    # -- one object -------------------------------------------------------
    def object(self, obj, where: str, strict: bool) -> None:
        if not isinstance(obj, dict) or not isinstance(obj.get("id"), str) or not obj["id"]:
            self.err(f"{where}: object needs a non-empty string id")
            return
        otype = obj.get("type")
        if otype not in OBJECT_FIELDS:
            self.err(f"{where} {obj['id']}: type {otype!r} not allowed")
            return
        if not strict:  # rejected objects carry deliberately invalid content
            return
        required, optional = OBJECT_FIELDS[otype]
        keys = set(obj) - {"id", "type"}
        for miss in sorted(required - keys):
            self.err(f"{where} {obj['id']}: missing field {miss}")
        for extra in sorted(keys - required - optional - COMMON_OPTIONAL):
            self.err(f"{where} {obj['id']}: unknown field {extra}")
        if "value" in obj:
            self.literal(obj["value"], f"{obj['id']}.value")
        for qk, qv in (obj.get("qualifiers") or {}).items():
            self.literal(qv, f"{obj['id']}.qualifiers.{qk}")
        if otype == "ASSERTION":
            self.applicability(obj.get("applicability"), f"{obj['id']}.applicability")
            basis = obj.get("basis")
            if basis not in BASES:
                self.err(f"{obj['id']}: basis {basis!r} not allowed")
            if basis == "CORRECTION" and not obj.get("corrects_ref"):
                self.err(f"{obj['id']}: a CORRECTION needs corrects_ref")
            if basis in {"REPORTED", "CORRECTION"} and not obj.get("evidence_refs"):
                self.err(f"{obj['id']}: {basis} needs non-empty evidence_refs")
        if otype == "RELATION" and "basis" in obj and obj["basis"] not in BASES:
            self.err(f"{obj['id']}: basis {obj['basis']!r} not allowed")
        if otype == "SOURCE" and obj.get("source_kind") not in SOURCE_KINDS:
            self.err(f"{obj['id']}: source_kind {obj.get('source_kind')!r} not allowed")
        for bkey in ("bindings", "input_bindings"):
            for i, b in enumerate(obj.get(bkey) or []):
                if not isinstance(b, dict) or not {"parameter", "assertion_ref"} <= set(b) or set(b) - {"parameter", "assertion_ref", "selection"}:
                    self.err(f"{obj['id']}.{bkey}[{i}]: binding needs parameter and assertion_ref, optional selection")
                elif "selection" in b and (not isinstance(b["selection"], dict) or "at" not in b["selection"]):
                    self.err(f"{obj['id']}.{bkey}[{i}]: selection needs a knowledge position 'at'")

    # -- whole file -------------------------------------------------------
    def run(self) -> dict:
        try:
            spec = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.err(f"cannot read JSON: {exc}")
            return {}
        if not isinstance(spec, dict):
            self.err("top level must be an object")
            return {}
        for miss in sorted(TOP_REQUIRED - set(spec)):
            self.err(f"missing top-level key {miss}")
        for extra in sorted(set(spec) - TOP_REQUIRED - TOP_OPTIONAL):
            self.err(f"unknown top-level key {extra}")
        if self.errors:
            return spec
        if spec["schema"] != SCHEMA_TAG:
            self.err(f"schema must be {SCHEMA_TAG!r}")
        obl = spec["obligation"]
        if not isinstance(obl, list) or not obl or len(set(obl)) != len(obl) or set(obl) - OBLIGATIONS:
            self.err(f"obligation must be a non-empty list of unique codes from {sorted(OBLIGATIONS)}")
        self.check_origin(spec["origin"])

        # id universe
        ids: dict[str, str] = {}

        def define(i, kind):
            if not isinstance(i, str) or not i:
                self.err(f"{kind} with missing id")
                return
            if i in ids:
                self.err(f"duplicate id {i!r} ({ids[i]} and {kind})")
            ids[i] = kind

        objects = spec["objects"]
        rejected = spec.get("rejected_objects", [])
        derived = spec.get("derived_labels", [])
        phantoms = set(spec.get("phantom_ids", []))
        for o in objects:
            if isinstance(o, dict):
                define(o.get("id"), "object")
        for o in rejected:
            if isinstance(o, dict):
                define(o.get("id"), "rejected_object")
        for d in derived:
            if isinstance(d, dict):
                define(d.get("id"), "derived_label")
        for q in spec["queries"]:
            define(q.get("id"), "query")
        for r in spec["refusals"]:
            define(r.get("id"), "refusal")
        for c in spec["open_choices"]:
            define(c.get("id"), "open_choice")
        for p in phantoms:
            if p in ids:
                self.err(f"phantom id {p!r} is also defined")

        for i, o in enumerate(objects):
            self.object(o, f"objects[{i}]", strict=True)
        for i, o in enumerate(rejected):
            self.object(o, f"rejected_objects[{i}]", strict=False)

        # changes and positions
        positions: list[str] = []
        intro: dict[str, int] = {}
        for idx, ch in enumerate(spec["changes"]):
            if not isinstance(ch, dict) or not {"position", "kind", "adds_refs"} <= set(ch) or set(ch) - {"position", "kind", "adds_refs", "target_refs", "note"}:
                self.err(f"changes[{idx}]: needs position, kind, adds_refs; optional target_refs, note")
                continue
            pos = ch["position"]
            if pos in positions:
                self.err(f"duplicate position {pos!r}")
            positions.append(pos)
            if ch["kind"] not in CHANGE_KINDS:
                self.err(f"changes[{idx}]: kind {ch['kind']!r} not allowed")
            if idx == 0 and (ch["kind"] != "GENESIS" or ch["adds_refs"]):
                self.err("the first change must be GENESIS with no additions")
            if idx > 0 and ch["kind"] == "GENESIS":
                self.err(f"changes[{idx}]: GENESIS only at the first position")
            for a in ch["adds_refs"]:
                if ids.get(a) != "object":
                    self.err(f"change {pos}: adds {a!r}, which is not an accepted object")
                elif a in intro:
                    self.err(f"object {a!r} introduced twice")
                else:
                    intro[a] = idx
            for t in ch.get("target_refs", []):
                if t not in intro or intro[t] >= idx:
                    self.err(f"change {pos}: target {t!r} must be introduced at an earlier position")
        pos_index = {p: i for i, p in enumerate(positions)}
        for o in objects:
            if isinstance(o, dict) and o.get("id") not in intro:
                self.err(f"object {o.get('id')!r} is never introduced by a change")

        # every reference resolves; phantoms only inside rejected objects
        for section in ("objects", "derived_labels", "queries", "forbidden", "refusals", "open_choices", "changes"):
            for where, ref in walk_refs(spec.get(section, []), section):
                self.check_ref(where, ref, ids, phantoms, allow_phantom=False)
        for where, ref in walk_refs(rejected, "rejected_objects"):
            self.check_ref(where, ref, ids, phantoms, allow_phantom=True)

        # positions and datetimes wherever they appear
        for where, key, val in walk_keys({k: v for k, v in spec.items() if k != "reused_files"}, POSITION_KEYS):
            if val is None and key in NULLABLE_POSITION_KEYS:
                continue
            if val not in pos_index:
                self.err(f"{where}: {val!r} is not a position of this specimen")
        for where, key, val in walk_keys(spec, DATETIME_KEYS):
            if val is None and key == "until":
                continue
            if not isinstance(val, str) or not DATETIME_RE.match(val):
                self.err(f"{where}: {val!r} is not a UTC dateTime like 2026-05-01T00:00:00Z")

        # an accepted object may only reference what exists at its own position
        for o in objects:
            if not isinstance(o, dict) or o.get("id") not in intro:
                continue
            for where, ref in walk_refs(o, o["id"]):
                if ref in intro and intro[ref] > intro[o["id"]]:
                    self.err(f"{where}: references {ref!r}, introduced later")
                if ids.get(ref) in {"derived_label", "rejected_object"}:
                    self.err(f"{where}: an accepted object cannot reference {ids[ref]} {ref!r}")

        reused = self.check_reused(spec.get("reused_files", []))
        self.check_derived(derived, reused, pos_index)
        choices = {c.get("id"): c for c in spec["open_choices"]}
        self.check_queries(spec["queries"], ids, intro, pos_index, derived, reused, choices)
        self.check_refusals(spec["refusals"], ids, rejected, pos_index)
        self.check_choices(spec["open_choices"], spec["queries"], ids, intro, pos_index, derived)
        self.check_forbidden(spec["forbidden"], spec["queries"], choices, ids)
        return spec

    def check_ref(self, where, ref, ids, phantoms, allow_phantom):
        if isinstance(ref, tuple):
            self.err(f"{where}: a *_refs field must be a list")
        elif not isinstance(ref, str):
            self.err(f"{where}: reference must be a string")
        elif ref in phantoms:
            if not allow_phantom:
                self.err(f"{where}: phantom id {ref!r} used outside rejected_objects")
        elif ref not in ids:
            self.err(f"{where}: undefined id {ref!r}")

    def check_origin(self, origin):
        if not isinstance(origin, dict) or not {"flows", "basis", "note"} <= set(origin) or set(origin) - {"flows", "basis", "note", "pointers"}:
            self.err("origin needs flows, basis, note; optional pointers")
            return
        if not origin["flows"] or any(not re.match(r"^GE-\d{2}$", f) for f in origin["flows"]):
            self.err("origin.flows must list GE-nn flow ids")
        if origin["basis"] not in ORIGIN_BASES:
            self.err(f"origin.basis must be one of {sorted(ORIGIN_BASES)}")

    def check_reused(self, reused_files) -> dict:
        docs = {}
        for i, rf in enumerate(reused_files):
            p = self.path.parent / rf.get("path", "")
            try:
                data = p.read_bytes()
            except OSError:
                self.err(f"reused_files[{i}]: cannot read {rf.get('path')!r}")
                continue
            if hashlib.sha256(data).hexdigest() != rf.get("sha256"):
                self.err(f"reused_files[{i}]: sha256 mismatch for {rf.get('path')!r}")
                continue
            docs[rf["path"]] = json.loads(data)
        return docs

    def external(self, pointer: str, reused: dict, where: str):
        if "#" not in pointer:
            self.err(f"{where}: pointer {pointer!r} needs 'path#/json/pointer'")
            return None
        path, frag = pointer.split("#", 1)
        if path not in reused:
            self.err(f"{where}: {path!r} is not a verified reused file")
            return None
        try:
            return resolve_pointer(reused[path], frag)
        except (KeyError, IndexError, ValueError, TypeError):
            self.err(f"{where}: pointer {pointer!r} does not resolve")
            return None

    def check_derived(self, derived, reused, pos_index):
        for d in derived:
            if set(d) != {"id", "from_assertion_ref", "knowledge_from", "defined_by"}:
                self.err(f"derived label {d.get('id')!r}: needs exactly id, from_assertion_ref, knowledge_from, defined_by")
                continue
            target = self.external(d["defined_by"], reused, f"derived label {d['id']}")
            if target is None:
                continue
            if target.get("id") != d["id"] or target.get("assertion") != d["from_assertion_ref"] or target.get("knowledge_from") != d["knowledge_from"]:
                self.err(f"derived label {d['id']}: does not match {d['defined_by']}")

    def check_expected(self, exp, where, at, ids, intro, pos_index, derived_from, inputs):
        if not isinstance(exp, dict) or exp.get("state") not in STATES:
            self.err(f"{where}: expected answer needs a state from the allowed list")
            return
        for extra in sorted(set(exp) - EXPECTED_KEYS):
            self.err(f"{where}: unknown expected key {extra}")
        state = exp["state"]
        if "value" in exp:
            self.literal(exp["value"], f"{where}.value")
        if "applicability" in exp:
            self.applicability(exp["applicability"], f"{where}.applicability")
        for qk, qv in (exp.get("qualifiers") or {}).items():
            self.literal(qv, f"{where}.qualifiers.{qk}")
        if state == "SELECTED" and ("value" not in exp or not (exp.get("selected_refs") or exp.get("derived_from_refs"))):
            self.err(f"{where}: SELECTED needs value and selected_refs or derived_from_refs")
        if state in {"NO_ACCEPTED_ACCOUNT", "NO_APPLICABLE_ACCOUNT"} and exp.get("selected_refs"):
            self.err(f"{where}: {state} cannot select anything")
        if state == "UNRESOLVED_APPLICABILITY" and not exp.get("unresolved_refs"):
            self.err(f"{where}: UNRESOLVED_APPLICABILITY needs unresolved_refs")
        if state == "COMPUTED" and not ({"result_ref", "value"} <= set(exp)):
            self.err(f"{where}: COMPUTED needs result_ref and value")
        if state == "NOT_COMPUTED" and "result_ref" in exp:
            self.err(f"{where}: NOT_COMPUTED cannot name a result")
        if state == "INCOMPLETE_RECONSTRUCTION":
            missing = exp.get("missing_refs") or []
            if not missing or not set(missing) <= set(inputs.get("withheld_refs") or []):
                self.err(f"{where}: INCOMPLETE_RECONSTRUCTION needs missing_refs drawn from withheld_refs")
        # no expected answer may name something not yet known at its position
        at_i = pos_index.get(at)
        for rwhere, ref in walk_refs({k: v for k, v in exp.items() if k not in {"absent_refs"}}, where):
            if not isinstance(ref, str) or at_i is None:
                continue
            kind = ids.get(ref)
            if kind == "object" and intro.get(ref, 10**9) > at_i:
                self.err(f"{rwhere}: {ref!r} is introduced after {at}")
            elif kind == "derived_label" and pos_index.get(derived_from.get(ref), 10**9) > at_i:
                self.err(f"{rwhere}: derived label {ref!r} starts after {at}")
            elif kind == "rejected_object":
                self.err(f"{rwhere}: a rejected object cannot appear in an answer")
        for ref in exp.get("absent_refs", []) or []:
            if ids.get(ref) == "object" and intro.get(ref, 10**9) <= (at_i or 0):
                self.err(f"{where}.absent_refs: {ref!r} is accepted by {at}, so it is not absent")

    def check_queries(self, queries, ids, intro, pos_index, derived, reused, choices):
        derived_from = {d.get("id"): d.get("knowledge_from") for d in derived}
        for q in queries:
            qid = q.get("id")
            allowed = {"id", "kind", "inputs", "expected", "expected_from", "open_choice_ref", "note"}
            if not {"id", "kind", "inputs", "expected"} <= set(q) or set(q) - allowed:
                self.err(f"query {qid}: needs id, kind, inputs, expected; optional expected_from, open_choice_ref, note")
                continue
            if q["kind"] not in QUERY_KINDS:
                self.err(f"query {qid}: kind {q['kind']!r} not allowed")
            inputs = q["inputs"]
            if not isinstance(inputs, dict) or "at" not in inputs:
                self.err(f"query {qid}: inputs need a knowledge position 'at'")
                continue
            for extra in sorted(set(inputs) - INPUT_KEYS):
                self.err(f"query {qid}: unknown input {extra}")
            if inputs.get("after_refusal_ref") and ids.get(inputs["after_refusal_ref"]) != "refusal":
                self.err(f"query {qid}: after_refusal_ref must name a refusal")
            choice = q.get("open_choice_ref")
            if q["expected"] is None:
                if not choice:
                    self.err(f"query {qid}: expected null requires open_choice_ref")
            elif choice:
                self.err(f"query {qid}: a query with open_choice_ref must have expected null")
            else:
                self.check_expected(q["expected"], f"query {qid}", inputs["at"], ids, intro, pos_index, derived_from, inputs)
            if choice:
                c = choices.get(choice)
                if c is None or qid not in c.get("affects_query_refs", []):
                    self.err(f"query {qid}: open choice {choice!r} must list it in affects_query_refs")
            if "expected_from" in q:
                if q["expected"] is None:
                    self.err(f"query {qid}: expected_from needs an expected answer to compare")
                    continue
                target = self.external(q["expected_from"], reused, f"query {qid}")
                if target is not None:
                    self.compare_external(qid, q, target)

    def compare_external(self, qid, q, target):
        exp, inputs = q["expected"], q["inputs"]

        def mismatch(key):
            self.err(f"query {qid}: {key} differs from {q['expected_from']}")

        seen_visible = []
        for key, val in target.items():
            if key in IGNORED_EXTERNAL_KEYS:
                continue
            if key == "outcome":
                exp.get("state") == val or mismatch(key)
            elif key == "selected":
                exp.get("selected_refs") == val or mismatch(key)
            elif key == "unresolved":
                exp.get("unresolved_refs") == val or mismatch(key)
            elif key == "value_cents":
                v = exp.get("value") or {}
                (v.get("lexical") == str(val) and v.get("unit") == "EUR_cent" and v.get("datatype") == "xsd:integer") or mismatch(key)
            elif key in {"at", "valid_at"}:
                inputs.get(key) == val or mismatch(key)
            elif key in {"assertions", "cells"}:
                seen_visible.extend(val)
            elif key == "metadata":
                ours = [{("cell" if k == "ref" else k): v for k, v in m.items()} for m in exp.get("metadata", [])]
                ours == val or mismatch(key)
            elif key == "assertion":
                val in (exp.get("premise_refs") or []) or mismatch(key)
            elif key == "cell":
                val in (exp.get("cell_refs") or []) or mismatch(key)
            elif key == "selection_at":
                exp.get("selection_at") == val or mismatch(key)
            elif key == "previous_assertion":
                val in (exp.get("previous_refs") or []) or mismatch(key)
            elif key == "new_assertion":
                val in (exp.get("new_refs") or []) or mismatch(key)
            elif key == "new_cell":
                val in (exp.get("new_cell_refs") or []) or mismatch(key)
            elif key == "domain_time":
                exp.get("domain_time") == val or mismatch(key)
            else:
                self.err(f"query {qid}: no comparison rule for external key {key!r}")
        if ("assertions" in target or "cells" in target) and sorted(exp.get("visible_refs", [])) != sorted(seen_visible):
            mismatch("assertions+cells")

    def check_refusals(self, refusals, ids, rejected, pos_index):
        rejected_ids = {o.get("id") for o in rejected if isinstance(o, dict)}
        used = set()
        for r in refusals:
            req = {"id", "head", "category", "head_after", "operation", "would_add_refs"}
            if not req <= set(r) or set(r) - req - {"base", "target_refs", "note"}:
                self.err(f"refusal {r.get('id')}: needs {sorted(req)}; optional base, target_refs, note")
                continue
            if r["category"] not in REFUSAL_CATEGORIES:
                self.err(f"refusal {r['id']}: category {r['category']!r} not allowed")
            if r["head_after"] != r["head"]:
                self.err(f"refusal {r['id']}: head_after must equal head (no partial accepted state)")
            if "base" in r and pos_index.get(r["base"], -1) > pos_index.get(r["head"], -1):
                self.err(f"refusal {r['id']}: base cannot be after head")
            if not r["would_add_refs"]:
                self.err(f"refusal {r['id']}: would_add_refs must name the refused objects")
            for a in r["would_add_refs"]:
                if a not in rejected_ids:
                    self.err(f"refusal {r['id']}: {a!r} is not a rejected object")
                used.add(a)
        for rid in sorted(rejected_ids - used):
            self.err(f"rejected object {rid!r} is not attempted by any refusal")

    def check_choices(self, choices, queries, ids, intro, pos_index, derived):
        derived_from = {d.get("id"): d.get("knowledge_from") for d in derived}
        qmap = {q.get("id"): q for q in queries}
        for c in choices:
            if not {"id", "question", "affects_query_refs", "branches"} <= set(c):
                self.err(f"open choice {c.get('id')}: needs id, question, affects_query_refs, branches")
                continue
            if len(c["branches"]) < 2:
                self.err(f"open choice {c['id']}: needs at least two branches")
            for qid in c["affects_query_refs"]:
                if qmap.get(qid, {}).get("open_choice_ref") != c["id"]:
                    self.err(f"open choice {c['id']}: query {qid} must point back with open_choice_ref")
            for b in c["branches"]:
                if not {"label", "expected"} <= set(b) or set(b) - {"label", "expected", "note"}:
                    self.err(f"open choice {c['id']}: branch needs label and expected, optional note")
                    continue
                exp = b["expected"] or {}
                if set(exp) != set(c["affects_query_refs"]):
                    self.err(f"open choice {c['id']} branch {b['label']!r}: must give an answer for exactly the affected queries")
                for qid, e in exp.items():
                    q = qmap.get(qid)
                    if q:
                        self.check_expected(e, f"open choice {c['id']} -> {qid}", q["inputs"]["at"], ids, intro, pos_index, derived_from, q["inputs"])

    def check_forbidden(self, forbidden, queries, choices, ids):
        qmap = {q.get("id"): q for q in queries}
        for i, f in enumerate(forbidden):
            if set(f) != {"query_ref", "answer", "why"} or not isinstance(f["why"], str) or not f["why"].strip():
                self.err(f"forbidden[{i}]: needs exactly query_ref, answer and a non-empty why")
                continue
            if ids.get(f["query_ref"]) != "query":
                self.err(f"forbidden[{i}]: query_ref must name a query")
                continue
            ans = f["answer"]
            if not isinstance(ans, dict) or not ans:
                self.err(f"forbidden[{i}]: answer must be a non-empty partial answer object")
                continue
            if "state" in ans and ans["state"] not in STATES:
                self.err(f"forbidden[{i}]: state {ans['state']!r} not allowed")
            q = qmap[f["query_ref"]]
            candidates = [q["expected"]] if q["expected"] is not None else [
                (b.get("expected") or {}).get(q["id"]) for b in choices.get(q.get("open_choice_ref"), {}).get("branches", [])]
            for exp in candidates:
                if isinstance(exp, dict) and all(exp.get(k) == v for k, v in ans.items()):
                    self.err(f"forbidden[{i}]: forbidden answer for {q['id']} matches an expected answer")


def validate_file(path: Path) -> tuple[list[str], dict]:
    checker = Checker(path)
    spec = checker.run()
    return checker.errors, spec


def validate_dir(directory: Path) -> tuple[dict[str, list[str]], list[str]]:
    results: dict[str, list[str]] = {}
    specs = {}
    for path in sorted(directory.glob("g1-*.json")):
        errors, spec = validate_file(path)
        results[path.name] = errors
        specs[path.name] = spec
    dir_errors = []
    if not results:
        dir_errors.append("no g1-*.json specimen files found")
    seen: dict[str, str] = {}
    covered: set[str] = set()
    for name, spec in specs.items():
        sid = spec.get("specimen_id") if isinstance(spec, dict) else None
        if sid in seen:
            dir_errors.append(f"specimen_id {sid!r} used by {seen[sid]} and {name}")
        seen[sid] = name
        if isinstance(spec, dict) and isinstance(spec.get("obligation"), list):
            covered.update(spec["obligation"])
    for missing in sorted(OBLIGATIONS - covered):
        dir_errors.append(f"obligation {missing} is covered by no specimen")
    return results, dir_errors


def main(argv: list[str]) -> int:
    directory = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parent
    results, dir_errors = validate_dir(directory)
    failed = 0
    for name, errors in results.items():
        if errors:
            failed += 1
            print(f"FAIL {name}")
            for e in errors:
                print(f"  {e}")
        else:
            print(f"OK   {name}")
    for e in dir_errors:
        print(f"FAIL directory: {e}")
    print(f"{len(results)} specimen files, {failed} failed, {len(dir_errors)} directory errors")
    return 1 if failed or dir_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
