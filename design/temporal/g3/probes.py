"""Supporting probes: each isolates one Core mechanism a result above depends on.

Probes are not specimen queries. Each returns a small dict of what Core did.
The two withheld-artifact probes edit a copy of a ledger file and re-chain its
hashes, the same technique Core's own T2 tests use; that edit is outside the
public API, and only the refusal read back is Core's.
"""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import malleus.compiler as api
from malleus.ledger import canonical_json, event_hash

from driver import ACTOR, TX, Run, admit, canonical, compile_contract, encode, operations, source_anchors
from queries import Reader


def _retain(history, sources, evidence_id):
    anchors = [a for s in sources for a in source_anchors(s)]
    anchors.append(api.structural_evidence_anchor(record_id=evidence_id, content=canonical({"probe": evidence_id}), media_type="application/json"))
    history.append_anchors(anchors=tuple(anchors), transaction_time=TX, actor_id=ACTOR)


def _attempt(history, change_set_id, records, sources, evidence, supersedes, valid_time):
    change = history.compose_change_set(
        change_set_id=change_set_id,
        source_record_ids=tuple(sources),
        evidence_record_ids=tuple(evidence),
        operations=operations(records, supersedes),
        valid_time=valid_time,
        supersedes=(),
    )
    return admit(history, change)


def relation_blocks_supersession(run: Run) -> dict:
    """g1-01: the premise link as a typed relation, then K2's transition."""
    history = run.fork("K1b", "P-REL-SUPERSEDE")
    _retain(history, [], "evidence:P-REL-SUPERSEDE")
    link = {
        "operation_type": "CREATE_RELATION", "record_type": "UsesInput", "record_id": "exec:X1#uses-input:r1",
        "properties": {"relation_type": "USES_INPUT"}, "source_id": "exec:X1", "target_id": "r1",
    }
    replay, linked = _attempt(history, "change:probe:link", [link], ["src:r1"], ["evidence:P-REL-SUPERSEDE"], {}, api.KnowledgeValidTime("NONE_STATED", None))
    obj = run.driver.objects
    _retain(history, [obj["src:r2"]], "evidence:P-REL-SUPERSEDE:K2")
    _, transition = _attempt(
        history, "change:probe:K2", encode(obj["r2"], run.positions, run.key), ["src:r2"], ["evidence:P-REL-SUPERSEDE:K2"],
        {"r2": "r1"}, api.KnowledgeValidTime("INSTANT", "2026-05-12T00:00:00Z"),
    )
    return {"link": linked, "transition": transition}


def correction_as_other_target(run: Run) -> dict:
    """g1-01: the K3 correction superseding r2 instead of r1."""
    history = run.fork("K2", "P-K3-TARGET-R2")
    obj = run.driver.objects
    _retain(history, [obj["src:r3"]], "evidence:P-K3-TARGET-R2")
    _, attempt = _attempt(
        history, "change:probe:K3-r2", encode(obj["r3"], run.positions, run.key), ["src:r3"], ["evidence:P-K3-TARGET-R2"],
        {"r3": "r2"}, api.KnowledgeValidTime("INSTANT", "2026-05-01T00:00:00Z"),
    )
    return {"attempt": attempt}


def one_change_r2(run: Run) -> dict:
    """g1-08: R2 as one change set, under each of its two valid times."""
    out = {}
    obj = run.driver.objects
    ids = ["part:X", "assembly:A", "q-partno", "q-price", "q-qty", "rel:part-of"]
    for label, vt in (
        ("INSTANT 2026-05-01", api.KnowledgeValidTime("INSTANT", "2026-05-01T00:00:00Z")),
        ("NONE_STATED", api.KnowledgeValidTime("NONE_STATED", None)),
    ):
        history = run.fork("R1", f"P-R2-ONE-{vt.kind}")
        _retain(history, [obj["src:quote"]], "evidence:P-R2-ONE")
        records = [r for i in ids for r in encode(obj[i], run.positions, run.key)]
        replay, attempt = _attempt(history, "change:probe:R2-one", records, ["src:quote"], ["evidence:P-R2-ONE"], {}, vt)
        reader = Reader(run, "R4", replay)
        out[label] = {
            "attempt": attempt,
            "q-qty": reader.applicability("q-qty"),
            "q-price": reader.applicability("q-price"),
            "part:X": reader.applicability("part:X"),
        }
    return out


def float_loses_lexical(workdir: Path) -> dict:
    """A decimal range does not compile; a float range stores 5.40 as 5.4."""
    base = (Path(__file__).parent / "contracts" / "g1-08.yaml").read_bytes()
    out = {}
    decimal = base.replace(b"slots:\n  label:", b"slots:\n  price_decimal: {range: decimal}\n  label:") + (
        b"  PricedPart:\n    is_a: Entity\n    slots: [price_decimal]\n"
    )
    try:
        compile_contract("decimal", decimal)
        out["decimal"] = "compiled"
    except Exception as error:  # the compiler's own refusal type is private
        out["decimal"] = f"{type(error).__name__}: {error}; {getattr(error, 'diagnostics', '')}"
    source = base.replace(b"slots:\n  label:", b"slots:\n  price_float: {range: float}\n  label:") + (
        b"  PricedPart:\n    is_a: Entity\n    slots: [price_float]\n"
    )
    history = api.create_structural_history(
        workdir / "P-FLOAT.jsonl", compilation=compile_contract("float", source), transaction_time=TX, actor_id=ACTOR
    )
    _retain(history, [{"id": "src:float", "text": "5.40"}], "evidence:P-FLOAT")
    record = {"operation_type": "CREATE_ENTITY", "record_type": "PricedPart", "record_id": "priced", "properties": {"price_float": 5.40}, "source_id": None, "target_id": None}
    replay, attempt = _attempt(history, "change:probe:float", [record], ["src:float"], ["evidence:P-FLOAT"], {}, api.KnowledgeValidTime("NONE_STATED", None))
    out["float_stored"] = replay.graph.get_node("priced")["price_float"]
    out["float_in_change_set_bytes"] = b'"price_float":5.4}' in replay.change_sets[0].canonical_bytes
    return out


def required_admits_empty_list(workdir: Path) -> dict:
    """g1-08's contract without its exactly_one_of: required alone admits []."""
    base = (Path(__file__).parent / "contracts" / "g1-08.yaml").read_bytes()
    clause = b"    exactly_one_of:\n      - slot_conditions:\n          evidence_refs: {required: true}\n"
    assert base.count(clause) == 1
    history = api.create_structural_history(
        workdir / "P-REQUIRED.jsonl", compilation=compile_contract("required-only", base.replace(clause, b"")),
        transaction_time=TX, actor_id=ACTOR,
    )
    _retain(history, [{"id": "src:quote", "text": "quote"}], "evidence:P-REQUIRED")
    record = {
        "operation_type": "CREATE_ENTITY", "record_type": "Assertion", "record_id": "q-empty",
        "properties": {"subject": "part:X", "property": "unit_price", "basis": "CORRECTION", "evidence_refs": [],
                       "assertion_value": {"datatype": "xsd:decimal", "lexical": "5.60", "unit": "EUR"}},
        "source_id": None, "target_id": None,
    }
    replay, attempt = _attempt(history, "change:probe:required", [record], ["src:quote"], ["evidence:P-REQUIRED"], {}, api.KnowledgeValidTime("NONE_STATED", None))
    return {"attempt": attempt, "stored_evidence_refs": list(replay.graph.get_node("q-empty")["evidence_refs"]) if replay else None}


def withheld(run: Run, name: str, drop) -> dict:
    """Remove matching ledger events from a copy, re-chain, then reopen and replay."""
    rows = [json.loads(line) for line in run.snapshots["R4"].splitlines()]
    kept = [row for row in rows if not drop(row)]
    previous = "GENESIS"
    for sequence, row in enumerate(kept, start=1):
        row["sequence"] = sequence
        row["previous_event_hash"] = previous
        row["event_hash"] = event_hash(row)
        previous = row["event_hash"]
    path = run.path.with_name(f"g1-08-{name}.jsonl")
    path.write_bytes(("\n".join(canonical_json(row) for row in kept) + "\n").encode())
    try:
        history = api.KnowledgeChangeHistory.reopen(path)
        history.replay()
        return {"removed": len(rows) - len(kept), "outcome": "REPLAYED"}
    except (api.KnowledgeChangeRefusal, ValueError) as error:
        reason = getattr(getattr(error, "reason", None), "name", type(error).__name__)
        return {"removed": len(rows) - len(kept), "outcome": "REFUSED", "reason": reason, "detail": getattr(error, "detail", str(error))}


def cli_reads(run: Run) -> dict:
    """g1-03: the read command at the head, and with an older position named."""
    out = {}
    for label, extra in (("head", []), ("expect A2", ["--expect-head", run.positions["A2"][0], "--expect-count", str(run.positions["A2"][1])])):
        done = subprocess.run(
            [sys.executable, "-c", "import sys; from malleus.compiler_cli import main; sys.exit(main(sys.argv[1:]))",
             "query", "--ledger", str(run.path), "--type", "Assertion", "--where", "subject=gauge:G", *extra],
            capture_output=True, text=True, check=False,
        )
        text = done.stdout or done.stderr
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = text.strip()
        out[label] = {"exit": done.returncode, "output": data}
    return out


def composed_record_trace(run: Run) -> dict:
    """g1-04: per-record provenance trace on a composed (not planned) change set."""
    try:
        api.trace_population_record(run.history.replay(), "m1")
        return {"outcome": "TRACED"}
    except ValueError as error:
        return {"outcome": "REFUSED", "reason": getattr(error, "reason", None) and error.reason.value, "detail": getattr(error, "detail", str(error))}


def shipped_profile_semantics() -> dict:
    return {
        "state-version change_semantics": dict(api.STATE_VERSION_PROFILE.change_semantics),
        "object-event projection_rule_family": api.OBJECT_EVENT_PROFILE.projection_rule_family,
        "object-event change_semantics": dict(api.OBJECT_EVENT_PROFILE.change_semantics),
    }


def run_probes(runs: dict[str, Run], workdir: Path) -> dict:
    g108 = runs["g1-08"]
    return {
        "P-REL-SUPERSEDE": relation_blocks_supersession(runs["g1-01"]),
        "P-K3-TARGET-R2": correction_as_other_target(runs["g1-01"]),
        "P-R2-ONE-CHANGE": one_change_r2(g108),
        "P-FLOAT": float_loses_lexical(workdir),
        "P-REQUIRED-EMPTY-LIST": required_admits_empty_list(workdir),
        "P-WITHHELD-SOURCE": withheld(
            g108, "withheld-source", lambda row: row["payload"].get("record_id") in {"src:quote", "artifact:src:quote"}
        ),
        "P-WITHHELD-CONTRACT": withheld(
            g108, "withheld-contract", lambda row: row["payload"].get("record_id") == "malleus:bootstrap:validated-contract"
        ),
        "P-CLI": cli_reads(runs["g1-03"]),
        "P-TRACE": composed_record_trace(runs["g1-04"]),
        "P-PROFILES": shipped_profile_semantics(),
        "P-UNTIMED": {
            "product:P valid_from": runs["g1-01"].history.replay().record_history["product:P"].valid_from,
            "valve:V valid_from": runs["g1-07"].history.replay().record_history["valve:V"].valid_from,
        },
    }
