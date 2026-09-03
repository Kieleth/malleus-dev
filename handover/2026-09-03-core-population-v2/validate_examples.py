"""Run the two handover examples through the real governed path.

Small Shop rows (structured source) and a neutral inspection note (document
source) both produce the same neutral population plan shape. Each plan is
checked by a reference validator, lowered by a reference lowering into the
current change-set grammar, admitted through KnowledgeChangeHistory, replayed,
and compared with the public direct path (KnowledgeGraph.from_records). Every
rule the handover pins is then provoked once so that it refuses. Nothing here
is a Core deliverable; it reuses Core's test helpers and is the seed for the
RED tests of P1, P2 and P4.

Run from the repository root:
    PYTHONPATH=src:. .venv/bin/python handover/2026-09-03-core-population-v2/validate_examples.py
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from copy import deepcopy
from dataclasses import fields
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from malleus import KnowledgeGraph, OntologyRegistry  # noqa: E402
from malleus._contract_pipeline.knowledge import (  # noqa: E402
    KnowledgeChangeHistory,
    KnowledgeChangeHistoryBinding,
    KnowledgeChangeRefusal,
    KnowledgeChangeSet,
    KnowledgeOperation,
    KnowledgeValidTime,
)
from tests.contract_compiler.pareto.test_knowledge_change_history import (  # noqa: E402
    TRANSACTION_TIME,
    _anchor,
    _binding_payload,
    _canonical,
    _event,
    _protocol_events,
)
from tests.contract_compiler.pareto.test_protocol_machine import _effective  # noqa: E402
from tests.contract_compiler.pareto.test_validated_contract import (  # noqa: E402
    _binding,
    _compile_binding,
    _trusted_types,
)

OUT = Path(__file__).parent / "examples"
OUT.mkdir(exist_ok=True)
FIX = ROOT / "research/ontology_driven_kg_realization/fixtures"
ROOT_YAML = (ROOT / "ontology/malleus.yaml").read_bytes()


def digest(b: bytes) -> str:
    return "sha256:" + sha256(b).hexdigest()


def is_digest(value: object) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


def log(line: str) -> None:
    print(line)


class PlanRefusal(ValueError):
    """Typed refusal of the reference plan compiler (P1) or document adapter (P4)."""

    def __init__(self, reason: str, detail: str) -> None:
        self.reason = reason
        super().__init__(f"{reason}: {detail}")


def refuse(reason: str, detail: str) -> PlanRefusal:
    return PlanRefusal(reason, detail)


# ---------------------------------------------------------------- sources ---

SHOP_TBOX = (FIX / "small_shop_fulfilment_correction_v1/input/tbox/small-shop-correction.yaml").read_bytes()
SHOP_BASE = (FIX / "small_shop_fulfilment/input/tbox/small-shop.yaml").read_bytes()
SHOP_ROWS = (FIX / "small_shop_fulfilment_correction_v1/input/sources/supplier-order-history.jsonl").read_bytes()

INSPECTION_TBOX = b"""\
id: https://example.malleus.dev/inspection-note
name: inspection_note
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  note: https://example.malleus.dev/inspection-note/
imports:
  - linkml:types
  - malleus
enums:
  InspectionRelationKind:
    permissible_values:
      INSPECTION_OF:
slots:
  inspected_on:
    range: string
  vibration_mm_s:
    range: float
classes:
  Asset:
    is_a: Entity
    slots:
      - name
    slot_usage:
      name:
        required: true
  Inspection:
    is_a: Entity
    slots:
      - inspected_on
    slot_usage:
      inspected_on:
        required: true
  VibrationReading:
    is_a: Entity
    slots:
      - vibration_mm_s
    slot_usage:
      vibration_mm_s:
        required: true
  InspectionOfRelation:
    is_a: Relation
    slot_usage:
      relation_type:
        range: InspectionRelationKind
        required: true
        equals_string: INSPECTION_OF
      source_id:
        range: Inspection
        required: true
      target_id:
        range: Asset
        required: true
"""

READING = {
    "schema": "example.reading/v0",
    "pages": [
        {
            "page": 1,
            "blocks": [
                {"id": "page:1:block:001", "ordinal": 0,
                 "text": "Pump P-7 was inspected on 2026-03-02. Vibration measured between 4.1 and 4.6 mm/s."},
                {"id": "page:1:block:002", "ordinal": 1,
                 "text": "The technician suspects bearing wear."},
                {"id": "page:1:block:003", "ordinal": 2,
                 "text": "Page 1 of 1."},
            ],
        }
    ],
}
READING_BYTES = _canonical(READING)

PROFILE_GRAMMAR = "malleus.domain-history-profile/private-v0"
SEMANTIC_UNITS = {"ASSERTION", "STATE_VERSION", "OCCURRENCE", "COMMITMENT", "COMPOSITION"}
ORIGINS = {"EMPTY", "SNAPSHOT", "PARTIAL_IMPORT", "HISTORICAL_RECONSTRUCTION"}

PROFILE_SOURCE_ASSERTION = {
    "grammar": PROFILE_GRAMMAR,
    "profile_id": "source-assertion",
    "semantic_unit": "ASSERTION",
    "origin": "EMPTY",
    "grounding": {
        "taxonomy": "Micropublications (Clark, Ciccarese, Goble 2014); nanopublications",
        "note": "minimal artifact: identity and unit only; full fields per P6",
    },
}
PROFILE_STATE_VERSION = {
    "grammar": PROFILE_GRAMMAR,
    "profile_id": "state-version",
    "semantic_unit": "STATE_VERSION",
    "origin": "EMPTY",
    "grounding": {
        "taxonomy": "temporal database versioning; Small Shop walkthrough",
        "note": "minimal artifact: identity and unit only; full fields per P6",
    },
}


def check_profile(profile: dict) -> None:
    if set(profile) != {"grammar", "profile_id", "semantic_unit", "origin", "grounding"}:
        raise refuse("FIELDS_NOT_CLOSED", "profile fields are not closed")
    if profile["grammar"] != PROFILE_GRAMMAR:
        raise refuse("UNSUPPORTED_GRAMMAR", profile["grammar"])
    if profile["semantic_unit"] not in SEMANTIC_UNITS:
        raise refuse("UNKNOWN_SEMANTIC_UNIT", profile["semantic_unit"])
    if profile["origin"] not in ORIGINS:
        raise refuse("UNKNOWN_ORIGIN", profile["origin"])
    if not isinstance(profile["grounding"], dict) or not profile["grounding"]:
        raise refuse("GROUNDING_REQUIRED", "a profile without a grounding block is refused")


# ------------------------------------------------------------------ plans ---

PLAN_GRAMMAR = "malleus.population-plan/private-v0"
PLAN_FIELDS = {
    "grammar", "plan_id", "contract_identity", "history_profile", "adapter", "sources",
    "evidence", "records", "supersessions", "derivations", "gaps", "valid_time",
}
PUBLIC_FAMILIES = ("entities", "relations", "signals", "events")  # kg.py RECORD_FAMILIES
ADMITTED_FAMILIES = {"entities", "relations"}  # governed path: CREATE_ENTITY, CREATE_RELATION only
GAP_KINDS = {
    "INTERVAL_NOT_EXPRESSIBLE", "AGGREGATE_ONLY", "MODALITY_NOT_EXPRESSIBLE",
    "REQUIRED_FIELD_ABSENT_IN_SOURCE", "TYPE_ABSENT", "RELATION_ABSENT",
}
MODALITIES = {"STATED", "MEASURED", "CALCULATED", "HYPOTHESISED", "CONTESTED", "NEGATED"}


def shop_plan(event_id: str, quantity: int, supersedes: str | None, contract: str, profile: str) -> dict:
    record = {
        "type": "SupplierOrderState",
        "id": f"supplier-order-state:B:{event_id}",
        "properties": {
            "supplier_order_id": "B",
            "product_code": "Y",
            "ordered_quantity": quantity,
            "source_occurrence_id": event_id,
        },
    }
    row = 0 if event_id == "e4" else 1
    src = "source:supplier-order-history"
    return {
        "grammar": PLAN_GRAMMAR,
        "plan_id": f"plan:shop:B:{event_id}",
        "contract_identity": contract,
        "history_profile": {"profile_id": "state-version", "sha256": profile},
        "adapter": {"adapter_id": "small-shop-row-mapping", "version": "0"},
        "sources": [{"source_id": src, "sha256": digest(SHOP_ROWS)}],
        "evidence": [],
        "records": {"entities": [record], "relations": []},
        "supersessions": (
            [{"record_id": record["id"], "supersedes_record_id": supersedes}] if supersedes else []
        ),
        "derivations": [
            {"record_id": record["id"], "path": ["properties", "supplier_order_id"], "source_id": src,
             "locator": f"row:{row}:supplier_order_id"},
            {"record_id": record["id"], "path": ["properties", "product_code"], "source_id": src,
             "locator": f"row:{row}:product_code"},
            {"record_id": record["id"], "path": ["properties", "ordered_quantity"], "source_id": src,
             "locator": f"row:{row}:quantity"},
            {"record_id": record["id"], "path": ["properties", "source_occurrence_id"], "source_id": src,
             "locator": f"row:{row}:event_id"},
        ],
        "gaps": [],
        "valid_time": {"kind": "ORDER_ONLY", "value": event_id},
    }


CAPTURE = {
    "schema": "malleus.document-capture/private-v0",
    "reading_sha256": digest(READING_BYTES),
    "attribution": {"source_id": "source:inspection-note", "author": "maintenance technician", "date": "2026-03-02"},
    "assertions": [
        {"id": "asr:001", "block": "page:1:block:001",
         "statement": "Pump P-7 was inspected on 2026-03-02.",
         "modality": "STATED",
         "formalized_by": [
             {"record_id": "asset:P-7", "path": ["properties", "name"]},
             {"record_id": "inspection:P-7:2026-03-02", "path": ["properties", "inspected_on"]},
             {"record_id": "inspection-of:P-7:2026-03-02", "path": ["properties", "relation_type"]},
             {"record_id": "inspection-of:P-7:2026-03-02", "path": ["source_id"]},
             {"record_id": "inspection-of:P-7:2026-03-02", "path": ["target_id"]},
         ],
         "gaps": []},
        {"id": "asr:002", "block": "page:1:block:001",
         "statement": "Vibration measured between 4.1 and 4.6 mm/s.",
         "modality": "MEASURED",
         "formalized_by": [],
         "gaps": [{"kind": "INTERVAL_NOT_EXPRESSIBLE",
                   "statement": "VibrationReading.vibration_mm_s is a single float; the source states a range"}]},
        {"id": "asr:003", "block": "page:1:block:002",
         "statement": "The technician suspects bearing wear.",
         "modality": "HYPOTHESISED",
         "formalized_by": [],
         "gaps": [{"kind": "TYPE_ABSENT", "statement": "no type for a suspected fault"},
                  {"kind": "MODALITY_NOT_EXPRESSIBLE", "statement": "no slot carries HYPOTHESISED on any record"}]},
    ],
    "nothing_assertable": ["page:1:block:003"],
}
DOC_RECORDS = {
    "entities": [
        {"type": "Asset", "id": "asset:P-7", "properties": {"name": "P-7"}},
        {"type": "Inspection", "id": "inspection:P-7:2026-03-02", "properties": {"inspected_on": "2026-03-02"}},
    ],
    "relations": [
        {"type": "InspectionOfRelation", "id": "inspection-of:P-7:2026-03-02",
         "source_id": "inspection:P-7:2026-03-02", "target_id": "asset:P-7",
         "properties": {"relation_type": "INSPECTION_OF"}},
    ],
}


# --------------------------------------------- P4: document adapter rules ---

def normalised(text: str) -> str:
    return " ".join(text.split())


def check_capture(capture: dict, reading: dict, reading_bytes: bytes, records: dict) -> None:
    if capture["reading_sha256"] != digest(reading_bytes):
        raise refuse("READING_MISMATCH", "capture names a different reading")
    blocks = {b["id"]: b["text"] for p in reading["pages"] for b in p["blocks"]}
    ids = {r["id"]: r for family in records.values() for r in family}
    for block in capture["nothing_assertable"]:
        if block not in blocks:
            raise refuse("UNKNOWN_BLOCK", block)
    for a in capture["assertions"]:
        if a["block"] not in blocks:
            raise refuse("UNKNOWN_BLOCK", a["block"])
        if normalised(a["statement"]) not in normalised(blocks[a["block"]]):
            raise refuse("NOT_VERBATIM", a["id"])
        if a["modality"] not in MODALITIES:
            raise refuse("UNKNOWN_MODALITY", a["modality"])
        if not a["formalized_by"] and not a["gaps"]:
            raise refuse("GAP_REQUIRED", f"{a['id']} has no formalization and no gap")
        for f in a["formalized_by"]:
            node = ids.get(f["record_id"])
            if node is None:
                raise refuse("UNKNOWN_FORMALIZATION_TARGET", f["record_id"])
            for step in f["path"]:
                if step not in node:
                    raise refuse("UNKNOWN_FORMALIZATION_TARGET", f"{f['record_id']}:{f['path']}")
                node = node[step]
        for g in a["gaps"]:
            if g["kind"] not in GAP_KINDS:
                raise refuse("UNKNOWN_GAP_KIND", g["kind"])


def document_plan(capture: dict, records: dict, contract: str, profile: str, capture_sha: str) -> dict:
    src = capture["attribution"]["source_id"]
    return {
        "grammar": PLAN_GRAMMAR,
        "plan_id": "plan:inspection-note:1",
        "contract_identity": contract,
        "history_profile": {"profile_id": "source-assertion", "sha256": profile},
        "adapter": {"adapter_id": "document-assertion", "version": "0"},
        "sources": [{"source_id": src, "sha256": capture["reading_sha256"]}],
        "evidence": [{"evidence_id": "capture:inspection-note", "sha256": capture_sha}],
        "records": deepcopy(records),
        "supersessions": [],
        "derivations": [
            {"record_id": f["record_id"], "path": f["path"], "source_id": src, "locator": a["id"]}
            for a in capture["assertions"] for f in a["formalized_by"]
        ],
        "gaps": [
            {"kind": g["kind"], "statement": g["statement"], "source_id": src, "locator": a["id"]}
            for a in capture["assertions"] for g in a["gaps"]
        ],
        "valid_time": {"kind": "INSTANT", "value": "2026-03-02T00:00:00Z"},
    }


def census(capture: dict, reading: dict, capture_sha: str) -> dict:
    blocks = [b["id"] for p in reading["pages"] for b in p["blocks"]]
    reviewed = {a["block"] for a in capture["assertions"]} | set(capture["nothing_assertable"])
    formal = {"FULLY_FORMALIZED": 0, "PARTLY_FORMALIZED": 0, "UNFORMALIZED": 0}
    by_kind: dict[str, int] = {}
    for a in capture["assertions"]:
        if a["formalized_by"] and not a["gaps"]:
            formal["FULLY_FORMALIZED"] += 1
        elif a["formalized_by"]:
            formal["PARTLY_FORMALIZED"] += 1
        else:
            formal["UNFORMALIZED"] += 1
        for g in a["gaps"]:
            by_kind[g["kind"]] = by_kind.get(g["kind"], 0) + 1
    return {
        "capture_sha256": capture_sha,
        "blocks": {b: ("REVIEWED" if b in reviewed else "UNTOUCHED") for b in blocks},
        "blocks_reviewed": len(reviewed & set(blocks)),
        "blocks_total": len(blocks),
        "assertions": formal,
        "gaps_by_kind": dict(sorted(by_kind.items())),
    }


# ------------------------------------------------ P1: plan compiler rules ---

def check_plan(plan: dict) -> dict[str, dict]:
    """Structural rules of the neutral plan. Returns records by id."""
    if set(plan) != PLAN_FIELDS:
        raise refuse("FIELDS_NOT_CLOSED", f"{sorted(set(plan) ^ PLAN_FIELDS)}")
    if plan["grammar"] != PLAN_GRAMMAR:
        raise refuse("UNSUPPORTED_GRAMMAR", plan["grammar"])
    if not is_digest(plan["contract_identity"]):
        raise refuse("MALFORMED_IDENTITY", "contract identity must be a compiled-contract digest")
    if set(plan["history_profile"]) != {"profile_id", "sha256"} or not is_digest(plan["history_profile"]["sha256"]):
        raise refuse("MALFORMED_PROFILE_REFERENCE", "history profile needs profile_id and sha256")
    if not plan["sources"] or any(not is_digest(s["sha256"]) for s in plan["sources"]):
        raise refuse("SOURCES_REQUIRED", "sources must be a nonempty list of retained digests")
    if any(not is_digest(e["sha256"]) for e in plan["evidence"]):
        raise refuse("MALFORMED_EVIDENCE_REFERENCE", "evidence members need evidence_id and sha256")
    families = plan["records"]
    if not set(families) <= set(PUBLIC_FAMILIES):
        raise refuse("UNKNOWN_FAMILY", f"{sorted(set(families) - set(PUBLIC_FAMILIES))}")
    for family in set(families) - ADMITTED_FAMILIES:
        if families[family]:
            raise refuse("FAMILY_NOT_ADMITTED",
                         f"{family} cannot be admitted: the governed path lowers entities and relations only")
    ids: dict[str, dict] = {}
    for family in ADMITTED_FAMILIES:
        for record in families.get(family, []):
            if record["id"] in ids:
                raise refuse("DUPLICATE_RECORD_ID", record["id"])
            ids[record["id"]] = record
    sources = {s["source_id"] for s in plan["sources"]}
    derived: set[tuple[str, tuple[str, ...]]] = set()
    for d in plan["derivations"]:
        node = ids.get(d["record_id"])
        if node is None:
            raise refuse("UNKNOWN_RECORD", f"derivation names {d['record_id']}")
        for step in d["path"]:
            if not isinstance(node, dict) or step not in node:
                raise refuse("ABSENT_PATH", f"{d['record_id']}:{d['path']}")
            node = node[step]
        if d["source_id"] not in sources:
            raise refuse("UNLISTED_SOURCE", d["source_id"])
        derived.add((d["record_id"], tuple(d["path"])))
    for record_id, record in ids.items():
        required = [("properties", key) for key in record["properties"]]
        if "source_id" in record:
            required += [("source_id",), ("target_id",)]
        for path in required:
            if (record_id, path) not in derived:
                raise refuse("UNDERIVED_FIELD", f"{record_id}:{list(path)}")
    seen: set[str] = set()
    for s in plan["supersessions"]:
        if s["record_id"] not in ids or s["record_id"] in seen:
            raise refuse("UNKNOWN_RECORD", f"supersession names {s['record_id']}")
        if not isinstance(s["supersedes_record_id"], str) or not s["supersedes_record_id"]:
            raise refuse("MALFORMED_SUPERSESSION", "supersedes_record_id must be a nonblank record id")
        seen.add(s["record_id"])
    for g in plan["gaps"]:
        if g["kind"] not in GAP_KINDS:
            raise refuse("UNKNOWN_GAP_KIND", g["kind"])
        if g["source_id"] not in sources:
            raise refuse("UNLISTED_SOURCE", g["source_id"])
    if plan["valid_time"]["kind"] not in {"INSTANT", "ORDER_ONLY"}:
        raise refuse("UNSUPPORTED_VALID_TIME", plan["valid_time"]["kind"])
    return ids


def lower(plan: dict, base) -> tuple[str, tuple[KnowledgeOperation, ...], tuple[str, ...]]:
    """Deterministic lowering against a base-state view (a replay: existing
    record ids and the change that created each). Reads no ledger, writes nothing.
    Returns (status, operations, change_level_supersedes)."""
    entities = plan["records"].get("entities", [])
    relations = plan["records"].get("relations", [])
    if not entities and not relations:
        return "NO_DOMAIN_CHANGE", (), ()
    existing = set(base.record_history)
    superseded = {s["record_id"]: s["supersedes_record_id"] for s in plan["supersessions"]}
    for old in superseded.values():
        if old not in existing:
            raise refuse("UNKNOWN_SUPERSESSION", old)
    op_of: dict[str, str] = {}
    operations: list[KnowledgeOperation] = []
    ordinal = 0
    for record in entities:
        op_id = f"operation:{plan['plan_id']}:{ordinal}"
        op_of[record["id"]] = op_id
        operations.append(KnowledgeOperation(
            ordinal=ordinal, operation_id=op_id, operation_type="CREATE_ENTITY",
            record_type=record["type"], record_id=record["id"],
            properties=record["properties"], depends_on=(),
            supersedes_record_id=superseded.get(record["id"]),
        ))
        ordinal += 1
    for record in relations:
        op_id = f"operation:{plan['plan_id']}:{ordinal}"
        deps = []
        for endpoint in (record["source_id"], record["target_id"]):
            if endpoint in op_of:
                deps.append(op_of[endpoint])
            elif endpoint not in existing:
                raise refuse("DANGLING_ENDPOINT", f"{record['id']} -> {endpoint}")
        operations.append(KnowledgeOperation(
            ordinal=ordinal, operation_id=op_id, operation_type="CREATE_RELATION",
            record_type=record["type"], record_id=record["id"],
            properties=record["properties"], depends_on=tuple(deps),
            source_id=record["source_id"], target_id=record["target_id"],
            supersedes_record_id=superseded.get(record["id"]),
        ))
        ordinal += 1
    change_ids: list[str] = []
    for old in superseded.values():
        history = base.record_history[old]
        change_id = next(getattr(history, f.name) for f in fields(history) if "change" in f.name)
        if change_id not in change_ids:
            change_ids.append(change_id)
    return "CHANGE_SET", tuple(operations), tuple(change_ids)


# ------------------------------------------------ P2: governed integration ---

def governed_history(tmp: Path, sources: dict[str, bytes], root_locator: str, source_id: str, source_bytes: bytes):
    compiled = _compile_binding(_binding(sources, root_locator))
    partial = _effective(validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256)
    binding = KnowledgeChangeHistoryBinding.from_bytes(_canonical(_binding_payload()))
    history = KnowledgeChangeHistory(
        tmp / "history.jsonl", partial_contract=partial, contract_view=compiled.view, binding=binding,
    )
    anchors = (
        (_event("ARTIFACT_REGISTERED", artifact_id="validated-contract-artifact",
                artifact_identity=digest(compiled.artifact.artifact_bytes)),
         compiled.artifact.artifact_bytes, "VALIDATED_CONTRACT"),
        (_event("ARTIFACT_REGISTERED", artifact_id="contract-artifact",
                artifact_identity=digest(partial.canonical_bytes)),
         partial.canonical_bytes, "PARTIAL_EFFECTIVE_CONTRACT"),
        (_event("ARTIFACT_REGISTERED", artifact_id="history-binding-artifact",
                artifact_identity=digest(binding.canonical_bytes)),
         binding.canonical_bytes, "KNOWLEDGE_HISTORY_BINDING"),
        (_event("ARTIFACT_REGISTERED", artifact_id="source-artifact", artifact_identity=digest(source_bytes)),
         source_bytes, "SOURCE_ARTIFACT"),
        (_event("SOURCE_REGISTERED", artifact_id="source-artifact", source_id=source_id,
                source_identity=digest(source_bytes)),
         source_bytes, "RETAINED_SOURCE"),
    )
    for event, retained, role in anchors:
        _anchor(history, event, retained, role)
    return history, partial


def retained_ids(history: KnowledgeChangeHistory) -> set[str]:
    return {r.record_id for r in history.replay().retained_inputs}


def retain_evidence(history: KnowledgeChangeHistory, record_id: str, content: bytes) -> None:
    _anchor(history, _event("ARTIFACT_REGISTERED", artifact_id=record_id, artifact_identity=digest(content)),
            content, "RETAINED_EVIDENCE")


def admit_plan(history: KnowledgeChangeHistory, plan: dict, profile: dict, suffix: str):
    """Retain profile, plan and gaps; require adapter evidence already retained;
    compose through Core's composer; admit with Core's protocol events."""
    check_profile(profile)
    check_plan(plan)
    plan_bytes = _canonical(plan)
    profile_id = f"profile:{plan['history_profile']['profile_id']}"
    already = retained_ids(history)
    if plan["plan_id"] in already:
        raise refuse("DUPLICATE_PLAN_ID", plan["plan_id"])
    if profile_id not in already:
        retain_evidence(history, profile_id, _canonical(profile))
    for member in plan["evidence"]:
        if member["evidence_id"] not in already:
            raise refuse("UNRETAINED_EVIDENCE", member["evidence_id"])
    retain_evidence(history, plan["plan_id"], plan_bytes)
    evidence_ids = [profile_id, plan["plan_id"], *(m["evidence_id"] for m in plan["evidence"])]
    if plan["gaps"]:
        gaps_id = f"{plan['plan_id']}:gaps"
        retain_evidence(history, gaps_id, _canonical({"plan_id": plan["plan_id"], "gaps": plan["gaps"]}))
        evidence_ids.append(gaps_id)
    before = history.replay()
    status, operations, change_supersedes = lower(plan, before)
    if status == "NO_DOMAIN_CHANGE":
        return status, None
    change = history.compose_change_set(
        change_set_id=f"change:{plan['plan_id']}",
        source_record_ids=tuple(s["source_id"] for s in plan["sources"]),
        evidence_record_ids=tuple(evidence_ids),
        operations=operations,
        valid_time=KnowledgeValidTime(**plan["valid_time"]),
        supersedes=change_supersedes,
    )
    admitted = history.admit(
        change_set=change,
        machine_events=_protocol_events(change, before.machine_state.identity, identifier_suffix=suffix),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:overseer",
    )
    return status, (change, admitted)


def direct_graph(tmp: Path, files: dict[str, bytes], root_file: str, plan: dict) -> KnowledgeGraph:
    tmp.mkdir(exist_ok=True)
    for name, content in files.items():
        (tmp / name).write_bytes(content)
    registry = OntologyRegistry(str(tmp / root_file))
    return KnowledgeGraph.from_records(registry, plan["records"])


def dump(name: str, value: object) -> None:
    (OUT / name).write_bytes(json.dumps(value, indent=2, sort_keys=True).encode() + b"\n")


# ---------------------------------------------------------------- run all ---

def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="population-examples-"))

    # ---- consumer 1: Small Shop rows ----------------------------------------
    shop_dir = tmp / "shop"; shop_dir.mkdir()
    history, partial = governed_history(
        shop_dir,
        {"small-shop-correction": SHOP_TBOX, "small-shop": SHOP_BASE, "malleus": ROOT_YAML,
         "linkml:types": _trusted_types()},
        "small-shop-correction", "source:supplier-order-history", SHOP_ROWS,
    )
    shop_profile_sha = digest(_canonical(PROFILE_STATE_VERSION))
    e4 = shop_plan("e4", 1, None, partial.identity, shop_profile_sha)
    e7 = shop_plan("e7", 2, e4["records"]["entities"][0]["id"], partial.identity, shop_profile_sha)
    status, (change4, admitted4) = admit_plan(history, e4, PROFILE_STATE_VERSION, "-e4")
    log(f"shop e4: {status}; change {change4.change_set_id}; ops {len(change4.operations)}; "
        f"nodes {admitted4.graph.node_count}")
    shop_files = {"small-shop-correction.yaml": SHOP_TBOX, "small-shop.yaml": SHOP_BASE, "malleus.yaml": ROOT_YAML}
    direct4 = direct_graph(shop_dir / "direct", shop_files, "small-shop-correction.yaml", e4)
    assert direct4.export_records() == admitted4.graph.export_records(), "direct != governed (e4)"
    log("shop e4: direct from_records export == governed replay export: True")
    status, (change7, admitted7) = admit_plan(history, e7, PROFILE_STATE_VERSION, "-e7")
    log(f"shop e7: {status}; change {change7.change_set_id}; supersedes {list(change7.supersedes)}; "
        f"op supersedes_record_id {change7.operations[0].supersedes_record_id}")
    current = admitted7.graph.query("SupplierOrderState", supplier_order_id="B")
    log(f"shop e7: current SupplierOrderState rows for B: {[r['ordered_quantity'] for r in current]}")
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    log(f"shop: reopen state digest == admitted: {reopened.graph.state_digest() == admitted7.graph.state_digest()}")
    log(f"shop: ledger events {reopened.ledger_event_count}")
    dump("small-shop-plan-e4.json", e4)
    dump("small-shop-plan-e7.json", e7)
    dump("small-shop-change-e7.json", json.loads(change7.canonical_bytes))
    dump("profile-state-version.json", PROFILE_STATE_VERSION)
    shop_history = history

    # ---- consumer 2: document capture ---------------------------------------
    doc_dir = tmp / "doc"; doc_dir.mkdir()
    history, partial = governed_history(
        doc_dir,
        {"inspection-note": INSPECTION_TBOX, "malleus": ROOT_YAML, "linkml:types": _trusted_types()},
        "inspection-note", "source:inspection-note", READING_BYTES,
    )
    doc_profile_sha = digest(_canonical(PROFILE_SOURCE_ASSERTION))
    check_capture(CAPTURE, READING, READING_BYTES, DOC_RECORDS)
    capture_bytes = _canonical(CAPTURE)
    capture_sha = digest(capture_bytes)
    retain_evidence(history, "capture:inspection-note", capture_bytes)
    plan = document_plan(CAPTURE, DOC_RECORDS, partial.identity, doc_profile_sha, capture_sha)
    status, (change, admitted) = admit_plan(history, plan, PROFILE_SOURCE_ASSERTION, "-doc")
    log(f"doc: {status}; change {change.change_set_id}; ops {len(change.operations)}; "
        f"relation depends_on {list(change.operations[2].depends_on)}")
    log(f"doc: evidence closure ids {[e for e, _ in change.evidence]}")
    direct = direct_graph(doc_dir / "direct", {"inspection-note.yaml": INSPECTION_TBOX, "malleus.yaml": ROOT_YAML},
                          "inspection-note.yaml", plan)
    assert direct.export_records() == admitted.graph.export_records(), "direct != governed (doc)"
    log("doc: direct from_records export == governed replay export: True")
    doc_census = census(CAPTURE, READING, capture_sha)
    log(f"doc census: blocks reviewed {doc_census['blocks_reviewed']}/{doc_census['blocks_total']}, "
        f"untouched {[b for b, s in doc_census['blocks'].items() if s == 'UNTOUCHED']}; "
        f"assertions {doc_census['assertions']}; gaps by kind {doc_census['gaps_by_kind']}; "
        f"capture_sha256 {capture_sha[:19]}...")
    dump("document-capture.json", CAPTURE)
    dump("document-plan.json", plan)
    dump("document-change.json", json.loads(change.canonical_bytes))
    dump("document-census.json", doc_census)
    dump("profile-source-assertion.json", PROFILE_SOURCE_ASSERTION)
    dump("reading.json", READING)
    (OUT / "inspection-note.yaml").write_bytes(INSPECTION_TBOX)

    # ---- capture with zero graph operations ---------------------------------
    empty = dict(plan, plan_id="plan:inspection-note:gaps-only",
                 records={"entities": [], "relations": []}, derivations=[], supersessions=[])
    status, result = admit_plan(history, empty, PROFILE_SOURCE_ASSERTION, "-empty")
    log(f"gaps-only plan: lowering status {status}; change set {result}; "
        f"retained {'plan:inspection-note:gaps-only' in retained_ids(history)}")
    payload = json.loads(change.canonical_bytes)
    payload["operations"] = []
    try:
        KnowledgeChangeSet.from_bytes(_canonical(payload))
    except KnowledgeChangeRefusal as error:
        log(f"grammar on empty operations: {error}")
    payload = json.loads(change.canonical_bytes)
    payload["operations"][0]["supersedes_record_id"] = None
    try:
        KnowledgeChangeSet.from_bytes(_canonical(payload))
    except KnowledgeChangeRefusal as error:
        log(f"grammar on supersedes_record_id null: {error}")

    # ---- every pinned rule, provoked once -----------------------------------
    log("negative cases (each must refuse):")
    base = history.replay()

    def mutate(source: dict, fn) -> dict:
        copy = deepcopy(source); fn(copy); return copy

    plan_cases = [
        ("FIELDS_NOT_CLOSED", mutate(plan, lambda p: p.update(extra=1))),
        ("MALFORMED_IDENTITY", mutate(plan, lambda p: p.update(contract_identity="sha256:not-a-digest"))),
        ("SOURCES_REQUIRED", mutate(plan, lambda p: p.update(sources=[]))),
        ("FAMILY_NOT_ADMITTED", mutate(plan, lambda p: p["records"].update(
            signals=[{"type": "X", "id": "s:1", "properties": {}}]))),
        ("DUPLICATE_RECORD_ID", mutate(plan, lambda p: p["records"]["entities"].append(
            dict(p["records"]["entities"][0])))),
        ("UNKNOWN_RECORD", mutate(plan, lambda p: p["derivations"][0].update(record_id="nope"))),
        ("ABSENT_PATH", mutate(plan, lambda p: p["derivations"][0].update(path=["properties", "colour"]))),
        ("UNLISTED_SOURCE", mutate(plan, lambda p: p["derivations"][0].update(source_id="source:other"))),
        ("UNDERIVED_FIELD", mutate(plan, lambda p: p["derivations"].pop(0))),
        ("MALFORMED_SUPERSESSION", mutate(plan, lambda p: p["supersessions"].append(
            {"record_id": "asset:P-7", "supersedes_record_id": None}))),
        ("UNKNOWN_GAP_KIND", mutate(plan, lambda p: p["gaps"][0].update(kind="SHRUG"))),
        ("UNSUPPORTED_VALID_TIME", mutate(plan, lambda p: p["valid_time"].update(kind="SOMETIME"))),
    ]
    for expected, bad in plan_cases:
        try:
            check_plan(bad)
        except PlanRefusal as error:
            assert error.reason == expected, (expected, error)
            log(f"  plan {error}")
        else:
            raise AssertionError(f"{expected} did not refuse")
    lower_cases = [
        ("DANGLING_ENDPOINT", mutate(plan, lambda p: (
            p["records"]["relations"][0].update(target_id="asset:ghost"),
            [d.update(record_id=d["record_id"]) for d in p["derivations"]]))),
        ("UNKNOWN_SUPERSESSION", mutate(plan, lambda p: p["supersessions"].append(
            {"record_id": "asset:P-7", "supersedes_record_id": "asset:never"}))),
    ]
    for expected, bad in lower_cases:
        try:
            lower(bad, base)
        except PlanRefusal as error:
            assert error.reason == expected, (expected, error)
            log(f"  lowering {error}")
        else:
            raise AssertionError(f"{expected} did not refuse")
    try:
        direct_graph(doc_dir / "direct", {}, "inspection-note.yaml",
                     mutate(plan, lambda p: p["records"]["entities"][0].update(type="Nope")))
    except ValueError as error:
        log(f"  contract (direct path) unknown type: {str(error)[:90]}")
    try:
        admit_plan(shop_history, e7, PROFILE_STATE_VERSION, "-again")
    except PlanRefusal as error:
        log(f"  governed {error}")
    try:
        admit_plan(history, mutate(plan, lambda p: p.update(plan_id="plan:inspection-note:2")),
                   PROFILE_SOURCE_ASSERTION, "-x")
    except KnowledgeChangeRefusal as error:
        log(f"  governed re-admission of the same records: {error.reason.name}: {error.detail[:60]}")
    unretained = mutate(plan, lambda p: (p.update(plan_id="plan:inspection-note:3"),
                                          p["evidence"].append({"evidence_id": "capture:ghost", "sha256": capture_sha})))
    try:
        admit_plan(history, unretained, PROFILE_SOURCE_ASSERTION, "-y")
    except PlanRefusal as error:
        log(f"  governed {error}")
    for expected, bad in [
        ("GROUNDING_REQUIRED", mutate(PROFILE_SOURCE_ASSERTION, lambda p: p.update(grounding={}))),
        ("UNKNOWN_SEMANTIC_UNIT", mutate(PROFILE_SOURCE_ASSERTION, lambda p: p.update(semantic_unit="VIBE"))),
        ("UNKNOWN_ORIGIN", mutate(PROFILE_SOURCE_ASSERTION, lambda p: p.update(origin="SOMEWHERE"))),
    ]:
        try:
            check_profile(bad)
        except PlanRefusal as error:
            assert error.reason == expected, (expected, error)
            log(f"  profile {error}")
        else:
            raise AssertionError(f"{expected} did not refuse")
    capture_cases = [
        ("READING_MISMATCH", mutate(CAPTURE, lambda c: c.update(reading_sha256="sha256:" + "0" * 64))),
        ("UNKNOWN_BLOCK", mutate(CAPTURE, lambda c: c["nothing_assertable"].append("page:9:block:999"))),
        ("NOT_VERBATIM", mutate(CAPTURE, lambda c: c["assertions"][0].update(statement="Pump P-7 was fine."))),
        ("UNKNOWN_MODALITY", mutate(CAPTURE, lambda c: c["assertions"][0].update(modality="VIBES"))),
        ("GAP_REQUIRED", mutate(CAPTURE, lambda c: c["assertions"][1].update(gaps=[]))),
        ("UNKNOWN_FORMALIZATION_TARGET", mutate(CAPTURE, lambda c: c["assertions"][0]["formalized_by"].append(
            {"record_id": "asset:P-7", "path": ["properties", "mass"]}))),
    ]
    for expected, bad in capture_cases:
        try:
            check_capture(bad, READING, READING_BYTES, DOC_RECORDS)
        except PlanRefusal as error:
            assert error.reason == expected, (expected, error)
            log(f"  capture {error}")
        else:
            raise AssertionError(f"{expected} did not refuse")
    whitespace = mutate(CAPTURE, lambda c: c["assertions"][0].update(statement="Pump  P-7 was\ninspected on 2026-03-02."))
    check_capture(whitespace, READING, READING_BYTES, DOC_RECORDS)
    log("  capture verbatim after whitespace normalisation: accepted")
    log(f"examples written to {OUT.relative_to(ROOT)}")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
