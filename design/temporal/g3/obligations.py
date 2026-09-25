"""The two obligations every specimen carries: rebuild and round trip.

Rebuild: a reopened history replays every recorded position to the same
receipt. Round trip: every specimen object decodes back from Core's retained
records with the fields the specimen states.
"""

from __future__ import annotations

import malleus.compiler as api

from driver import Run
from queries import Reader, props


def rebuild(run: Run) -> dict:
    reopened = api.KnowledgeChangeHistory.reopen(run.path)
    final = reopened.replay()
    same = {}
    for label in run.positions:
        head, count = run.positions[label]
        again = reopened.replay_at(
            ledger_head=head, ledger_event_count=count,
            expected_head_hash=final.ledger_head, expected_event_count=final.ledger_event_count,
        )
        same[label] = again.receipt == run.at(label).receipt and again.record_history == run.at(label).record_history
    return same


def _decode(reader: Reader, obj: dict) -> dict:
    entry = reader.entry(obj["id"])
    p = props(entry)
    op = entry.operation
    kind = obj["type"]
    q = {k[2:]: v for k, v in p.items() if k.startswith("q_")}
    if kind == "SUBJECT":
        return {"label": p["label"], **({"contract_ref": p["contract_ref"]} if "contract_ref" in p else {})}
    if kind == "ACCOUNT":
        return {"label": p["label"]}
    if kind == "ASSERTION":
        out = {"subject_ref": p["subject"], "property": p["property"], "value": p["assertion_value"], "basis": p["basis"],
               "applicability": reader.applicability(obj["id"])}
        for slot, key in (("account", "account_ref"), ("evidence_refs", "evidence_refs"), ("corrects", "corrects_ref"),
                          ("revises", "revises_ref"), ("contract_ref", "contract_ref")):
            if slot in p:
                out[key] = p[slot]
        if q:
            out["qualifiers"] = q
        return out
    if kind == "RELATION":
        out = {"relation_type": p["relation_type"], "from_ref": op.source_id, "to_ref": op.target_id}
        for key in ("basis", "evidence_refs", "contract_ref"):
            if key in p:
                out[key] = p[key]
        if q:
            out["qualifiers"] = q
        return out
    if kind == "GROUP":
        return {k: p[k] for k in ("group_kind", "member_refs", "evidence_refs") if k in p}
    if kind == "ARGUMENT":
        return {"premise_refs": p["premise_refs"], "conclusion_ref": p["conclusion_ref"]}
    if kind == "CONTEXT":
        out = {"context_kind": p["context_kind"], "bindings": p["bindings"]}
        for key in ("model_ref", "basis_refs"):
            if key in p:
                out[key] = p[key]
        return out
    if kind == "MODEL":
        return {k: p[k] for k in ("version", "implementation", "formula", "parameters", "member_refs") if k in p}
    if kind == "EXECUTION":
        bindings = []
        for b in p["input_bindings"]:
            out = {"parameter": b["parameter"], "assertion_ref": b["assertion_ref"]}
            if "selection_ledger_head" in b:
                at = [l for l, pos in reader.run.positions.items() if pos == (b["selection_ledger_head"], b["selection_ledger_event_count"])]
                out["selection"] = {"at": at[0]}
                if "selection_valid_at" in b:
                    out["selection"]["valid_at"] = b["selection_valid_at"]
                if "selection_account" in b:
                    out["selection"]["account_ref"] = b["selection_account"]
            bindings.append(out)
        out = {"model_ref": p["model_ref"], "input_bindings": bindings}
        if "context_ref" in p:
            out["context_ref"] = p["context_ref"]
        return out
    if kind == "RESULT":
        return {"execution_ref": p["execution_ref"], "value": p["result_value"]}
    if kind == "RULE":
        return {k: p[k] for k in ("semantics", "scope_refs", "assumptions")}
    if kind == "PLAN":
        return {"subject_ref": p["subject"], "action": p["action"], "planned_for": p["planned_for"], "evidence_refs": p["evidence_refs"]}
    raise KeyError(kind)


def round_trip(run: Run) -> dict:
    """Per object: MATCH, or the fields that differ; sources and contracts separately."""
    reader = Reader(run, run.driver.order[-1])
    result = {"match": [], "differ": {}, "not_carried": {}}
    for obj in run.driver.spec["objects"]:
        if obj["type"] == "SOURCE":
            if reader.replay.retained_bytes(obj["id"]) == obj["text"].encode():
                result["match"].append(obj["id"])
            else:
                result["differ"][obj["id"]] = ["text"]
            lost = [k for k in ("source_kind", "locator", "pointer") if k in obj]
            if lost:
                result["not_carried"][obj["id"]] = lost
            continue
        if obj["type"] == "CONTRACT":
            result["not_carried"][obj["id"]] = ["a record: Core binds the history's contract at creation"]
            continue
        decoded = _decode(reader, obj)
        expected = {k: v for k, v in obj.items() if k not in {"id", "type", "note"}}
        differ = [k for k in expected if decoded.get(k) != expected[k]]
        if differ:
            result["differ"][obj["id"]] = {k: (decoded.get(k), expected[k]) for k in differ}
        else:
            result["match"].append(obj["id"])
    return result
