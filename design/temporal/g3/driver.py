"""G3: drive the G1 specimens through Malleus Core's public API.

Every specimen change is composed with ``compose_change_set`` and admitted by
``check_and_admit_change_set`` under Core's structural policy, whose required
check is the CORE_BUILTIN ``operations-apply-atomically`` that Core itself runs.
Reads use ``replay_at``, ``record_history``, ``change_sets``, ``graph`` and
``retained_bytes``. No ``src/`` file is touched and no outcome is supplied.

Harness rule, applied to every query. The harness may (i) map specimen labels to
Core ids and ledger coordinates, (ii) project fields, (iii) filter records Core
returned by field equality or list membership, (iv) compare sets and map an
empty or singular result onto the specimen's answer vocabulary. It may not
select by domain time, choose between accounts, interpret correction lineage,
judge premise compatibility, compute, or decide completeness. A query whose
answer needs one of those is NOT_EXPRESSIBLE for Core, and the harness's own
naive derivation is reported beside it, labelled as harness work.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path
from typing import Callable

import malleus.compiler as api

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
G1 = HERE.parent / "g1"
TX = "2026-09-24T00:00:00+00:00"
ACTOR = "actor:temporal-g3"

SPECIMENS = {
    "g1-01": "g1-01-price-history.json",
    "g1-02": "g1-02-order-premises.json",
    "g1-03": "g1-03-competing-accounts.json",
    "g1-04": "g1-04-unknown-time-diameter.json",
    "g1-05": "g1-05-conditional-statement.json",
    "g1-06": "g1-06-alternate-justification.json",
    "g1-07": "g1-07-valve-persistence.json",
    "g1-08": "g1-08-storage-closure.json",
}
RELATION_CLASSES = {
    "FOLLOWS_CITED_MODEL": "FollowsCitedModel",
    "REPORTED_APPLICATION": "ReportedApplication",
    "PART_OF": "PartOf",
}
# Every execution's model link is also a typed relation, so Core checks that the
# model exists and is a Model. Premise links stay slots: probe P-REL-SUPERSEDE
# shows that a relation into a record blocks that record's supersession.
MODEL_RELATION = {"g1-01", "g1-02", "g1-05", "g1-08"}
ASSERTION_TYPES = ("Assertion", "ReportedEvent")

CORRECT = "ANSWERED_CORRECT"
WRONG = "ANSWERED_WRONG"
NOT_EXPRESSIBLE = "NOT_EXPRESSIBLE"
OBSERVED = "EXPECTED_REFUSAL_OBSERVED"
NOT_OBSERVED = "EXPECTED_REFUSAL_NOT_OBSERVED"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(content: bytes) -> str:
    return "sha256:" + sha256(content).hexdigest()


def load_specimen(key: str) -> dict:
    return json.loads((G1 / SPECIMENS[key]).read_bytes())


_COMPILED: dict[str, object] = {}


def compile_contract(key: str, source: bytes | None = None):
    """Compile a specimen contract from exact bytes, cached per key."""
    if source is None and key in _COMPILED:
        return _COMPILED[key]
    compiled = api.compile_linkml_contract(
        root_locator="contract",
        sources={
            "contract": source
            if source is not None
            else (HERE / "contracts" / f"{key}.yaml").read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model", "model", "schema", "types.yaml")
            .read_bytes(),
        },
    )
    if source is None:
        _COMPILED[key] = compiled
    return compiled


# --- encoding ------------------------------------------------------------------


def core_valid_time(obj: dict) -> api.KnowledgeValidTime | None:
    """Map a specimen applicability onto Core's change-set valid time.

    INTERVAL maps to its start: Core closes a record's period only through a
    successor, so a stated finite end has no Core field (see stated_until).
    """
    if obj["type"] != "ASSERTION":
        return None
    applicability = obj["applicability"]
    kind = applicability["kind"]
    if kind == "NONE_STATED":
        return api.KnowledgeValidTime("NONE_STATED", None)
    if kind == "INTERVAL":
        return api.KnowledgeValidTime("INSTANT", applicability["from"])
    if kind == "INSTANT":
        return api.KnowledgeValidTime("INSTANT", applicability["instant"])
    # An applicability kind Core does not define is passed through unchanged,
    # so Core, not the harness, decides whether it is refused.
    rest = {k: v for k, v in applicability.items() if k != "kind"}
    return api.KnowledgeValidTime(kind, json.dumps(rest, sort_keys=True))


def is_event(obj: dict) -> bool:
    return (
        obj["type"] == "ASSERTION"
        and obj["property"] == "event"
        and obj["applicability"]["kind"] == "INSTANT"
    )


def _qualifiers(obj: dict) -> dict:
    return {f"q_{name}": value for name, value in obj.get("qualifiers", {}).items()}


def _optional(obj: dict, **names: str) -> dict:
    return {slot: obj[key] for slot, key in names.items() if key in obj}


def encode(obj: dict, positions: dict[str, tuple[str, int]], key: str) -> list[dict]:
    """One specimen object as Core operation fields, in dependency order."""
    kind = obj["type"]
    if kind == "SUBJECT":
        return [
            _entity("Subject", obj["id"], {"label": obj["label"], **_optional(obj, contract_ref="contract_ref")})
        ]
    if kind == "ACCOUNT":
        return [_entity("Account", obj["id"], {"label": obj["label"]})]
    if kind == "ASSERTION":
        props = {
            "subject": obj["subject_ref"],
            "property": obj["property"],
            "assertion_value": obj["value"],
            "basis": obj["basis"],
            **_optional(
                obj,
                account="account_ref",
                evidence_refs="evidence_refs",
                corrects="corrects_ref",
                revises="revises_ref",
                contract_ref="contract_ref",
            ),
            **_qualifiers(obj),
        }
        until = obj["applicability"].get("until")
        if obj["applicability"]["kind"] == "INTERVAL" and until is not None:
            props["stated_until"] = until
        if is_event(obj):
            props.pop("account", None)
            props["event_type"] = obj["property"]
            props["occurred_at"] = obj["applicability"]["instant"]
            return [_record("CREATE_EVENT", "ReportedEvent", obj["id"], props)]
        return [_entity("Assertion", obj["id"], props)]
    if kind == "RELATION":
        props = {
            "relation_type": obj["relation_type"],
            **_optional(obj, basis="basis", evidence_refs="evidence_refs", contract_ref="contract_ref"),
            **_qualifiers(obj),
        }
        return [
            _record(
                "CREATE_RELATION",
                RELATION_CLASSES[obj["relation_type"]],
                obj["id"],
                props,
                source_id=obj["from_ref"],
                target_id=obj["to_ref"],
            )
        ]
    if kind == "GROUP":
        return [
            _entity(
                "Group",
                obj["id"],
                {"group_kind": obj["group_kind"], "member_refs": obj["member_refs"], **_optional(obj, evidence_refs="evidence_refs")},
            )
        ]
    if kind == "ARGUMENT":
        return [
            _entity(
                "Argument",
                obj["id"],
                {"premise_refs": obj["premise_refs"], "conclusion_ref": obj["conclusion_ref"]},
            )
        ]
    if kind == "CONTEXT":
        return [
            _entity(
                "Context",
                obj["id"],
                {
                    "context_kind": obj["context_kind"],
                    "bindings": [_binding(b, positions) for b in obj["bindings"]],
                    **_optional(obj, model_ref="model_ref", basis_refs="basis_refs"),
                },
            )
        ]
    if kind == "MODEL":
        return [
            _entity(
                "Model",
                obj["id"],
                {
                    "version": obj["version"],
                    "implementation": obj["implementation"],
                    "formula": obj["formula"],
                    "parameters": obj["parameters"],
                    **_optional(obj, member_refs="member_refs"),
                },
            )
        ]
    if kind == "EXECUTION":
        records = [
            _entity(
                "Execution",
                obj["id"],
                {
                    "model_ref": obj["model_ref"],
                    "input_bindings": [_binding(b, positions) for b in obj["input_bindings"]],
                    **_optional(obj, context_ref="context_ref"),
                },
            )
        ]
        if key in MODEL_RELATION:
            records.append(
                _record(
                    "CREATE_RELATION",
                    "UsesModel",
                    f"{obj['id']}#uses-model",
                    {"relation_type": "USES_MODEL"},
                    source_id=obj["id"],
                    target_id=obj["model_ref"],
                )
            )
        return records
    if kind == "RESULT":
        return [
            _entity(
                "Result",
                obj["id"],
                {"execution_ref": obj["execution_ref"], "result_value": obj["value"]},
            )
        ]
    if kind == "RULE":
        return [
            _entity(
                "PersistenceRule",
                obj["id"],
                {"semantics": obj["semantics"], "scope_refs": obj["scope_refs"], "assumptions": obj["assumptions"]},
            )
        ]
    if kind == "PLAN":
        return [
            _entity(
                "Plan",
                obj["id"],
                {
                    "subject": obj["subject_ref"],
                    "action": obj["action"],
                    "planned_for": obj["planned_for"],
                    "evidence_refs": obj["evidence_refs"],
                },
            )
        ]
    raise ValueError(f"no Core encoding for specimen type {kind}")


def _binding(binding: dict, positions: dict[str, tuple[str, int]]) -> dict:
    out = {"parameter": binding["parameter"], "assertion_ref": binding["assertion_ref"]}
    selection = binding.get("selection")
    if selection:
        head, count = positions[selection["at"]]
        out["selection_ledger_head"] = head
        out["selection_ledger_event_count"] = count
        if selection.get("valid_at"):
            out["selection_valid_at"] = selection["valid_at"]
        if selection.get("account_ref"):
            out["selection_account"] = selection["account_ref"]
    return out


def _entity(record_type: str, record_id: str, props: dict) -> dict:
    return _record("CREATE_ENTITY", record_type, record_id, props)


def _record(operation_type, record_type, record_id, props, source_id=None, target_id=None) -> dict:
    return {
        "operation_type": operation_type,
        "record_type": record_type,
        "record_id": record_id,
        "properties": props,
        "source_id": source_id,
        "target_id": target_id,
    }


def operations(records: list[dict], supersedes: dict[str, str]) -> tuple[api.KnowledgeOperation, ...]:
    ordered = [r for r in records if r["operation_type"] != "CREATE_RELATION"] + [
        r for r in records if r["operation_type"] == "CREATE_RELATION"
    ]
    return tuple(
        api.KnowledgeOperation(
            ordinal=ordinal,
            operation_id=f"operation:{record['record_id']}",
            operation_type=record["operation_type"],
            record_type=record["record_type"],
            record_id=record["record_id"],
            properties=record["properties"],
            depends_on=(),
            source_id=record["source_id"],
            target_id=record["target_id"],
            supersedes_record_id=supersedes.get(record["record_id"]),
        )
        for ordinal, record in enumerate(ordered)
    )


# --- driving changes -------------------------------------------------------------


@dataclass
class Attempt:
    change_set_id: str
    valid_time: api.KnowledgeValidTime
    supersedes: dict[str, str]
    record_ids: tuple[str, ...]
    outcome: str  # ADMITTED or REFUSED
    stage: str | None = None
    reason: str | None = None
    detail: str | None = None
    bytes_before: str | None = None
    bytes_after: str | None = None


@dataclass
class ChangeLog:
    position: str
    kind: str
    outcome: str  # ADMITTED, ADMITTED_WITHOUT_SUPERSESSION, SPLIT, COLLAPSED_INTO_GENESIS, GENESIS
    attempts: list[Attempt] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    fallback_records: tuple[str, ...] = ()


def retain(history, anchors) -> None:
    if anchors:
        history.append_anchors(anchors=tuple(anchors), transaction_time=TX, actor_id=ACTOR)


def source_anchors(obj: dict):
    return api.structural_source_anchors(
        source_id=obj["id"],
        artifact_id=f"artifact:{obj['id']}",
        content=obj["text"].encode(),
        media_type="text/plain",
    )


def ledger_state(history) -> tuple[str, int]:
    content = Path(history.path).read_bytes()
    return digest(content), len(content)


def admit(history, change) -> tuple[object | None, Attempt]:
    """Check and admit through Core; a refusal is recorded, never bypassed."""
    before = ledger_state(history)
    ops = change.operations
    attempt = Attempt(
        change.change_set_id,
        change.valid_time,
        {op.record_id: op.supersedes_record_id for op in ops if op.supersedes_record_id},
        tuple(op.record_id for op in ops),
        "ADMITTED",
        bytes_before=f"{before[0]} ({before[1]} bytes)",
    )
    try:
        admitted = api.check_and_admit_change_set(
            history=history, change_set=change, transaction_time=TX, actor_id=ACTOR
        )
    except api.PopulationAdmissionRefusal as refusal:
        after = ledger_state(history)
        attempt.outcome = "REFUSED"
        attempt.stage = refusal.stage.value
        attempt.reason = refusal.reason
        attempt.detail = refusal.detail
        attempt.bytes_after = f"{after[0]} ({after[1]} bytes)"
        return None, attempt
    after = ledger_state(history)
    attempt.bytes_after = f"{after[0]} ({after[1]} bytes)"
    return admitted.replay, attempt


def compose(history, change_set_id, sources, evidence, records, supersedes, valid_time):
    return history.compose_change_set(
        change_set_id=change_set_id,
        source_record_ids=tuple(sources),
        evidence_record_ids=tuple(evidence),
        operations=operations(records, supersedes),
        valid_time=valid_time,
        supersedes=(),
    )


class SpecimenDriver:
    def __init__(self, key: str):
        self.key = key
        self.spec = load_specimen(key)
        self.objects = {o["id"]: o for o in self.spec["objects"]}
        self.rejected = {o["id"]: o for o in self.spec.get("rejected_objects", [])}
        self.order = [c["position"] for c in self.spec["changes"]]

    def index(self, label: str) -> int:
        return self.order.index(label)

    def supersessions(self, change: dict, added: list[dict]) -> dict[str, str]:
        """Which added record replaces which target, from the declared change."""
        if change["kind"] not in {"TRANSITION", "CORRECTION", "REASSESSMENT"}:
            return {}
        out = {}
        for target in change.get("target_refs", []):
            prior = self.objects[target]
            for obj in added:
                if obj["type"] != "ASSERTION":
                    continue
                if obj.get("corrects_ref") == target or obj.get("revises_ref") == target or (
                    change["kind"] == "TRANSITION"
                    and obj["subject_ref"] == prior["subject_ref"]
                    and obj["property"] == prior["property"]
                ):
                    out[obj["id"]] = target
        return out

    def apply_change(self, history, change: dict, positions: dict) -> tuple[object, ChangeLog]:
        """Retain, compose and admit one specimen change. Returns the replay."""
        position = change["position"]
        log = ChangeLog(position, change["kind"], "ADMITTED")
        added = [self.objects[i] for i in change["adds_refs"]]
        sources = [o for o in added if o["type"] == "SOURCE"]
        contracts = [o for o in added if o["type"] == "CONTRACT"]
        graph_objects = [o for o in added if o["type"] not in {"SOURCE", "CONTRACT"}]
        if contracts and not graph_objects:
            log.outcome = "COLLAPSED_INTO_GENESIS"
            log.notes.append(
                "Core binds the governing contract when the history is created, not in an "
                "accepted change; this position is the genesis position."
            )
            return history.replay(), log
        cited = sorted({ref for o in graph_objects for ref in o.get("evidence_refs", [])})
        held = {m.record_id for m in history.replay().retained_inputs}
        anchors = [a for s in sources if s["id"] not in held for a in source_anchors(s)]
        source_ids = list(cited)
        if not source_ids:
            declaration = {"specimen": self.spec["specimen_id"], "position": position, "objects": graph_objects}
            anchors.extend(
                api.structural_source_anchors(
                    source_id=f"decl:{position}",
                    artifact_id=f"artifact:decl:{position}",
                    content=canonical(declaration),
                    media_type="application/json",
                )
            )
            source_ids = [f"decl:{position}"]
            log.notes.append(
                f"No specimen source is cited; Core requires a nonempty source closure, so the "
                f"change names decl:{position}, a retained declaration of its own objects."
            )
        evidence_id = f"evidence:{position}"
        anchors.append(
            api.structural_evidence_anchor(
                record_id=evidence_id,
                content=canonical(
                    {
                        "specimen": self.spec["specimen_id"],
                        "position": position,
                        "declared_kind": change["kind"],
                        "target_refs": change.get("target_refs", []),
                    }
                ),
                media_type="application/json",
            )
        )
        retain(history, anchors)

        # Core's valid time belongs to a change set, so group by it.
        groups: list[tuple[api.KnowledgeValidTime, list[dict]]] = []
        for obj in graph_objects:
            vt = core_valid_time(obj)
            if vt is None:
                continue
            for existing, members in groups:
                if existing == vt:
                    members.append(obj)
                    break
            else:
                groups.append((vt, [obj]))
        if not groups:
            groups = [(api.KnowledgeValidTime("NONE_STATED", None), [])]
        untimed = [o for o in graph_objects if core_valid_time(o) is None]
        groups[0][1][:0] = untimed
        if len(groups) > 1:
            log.outcome = "SPLIT"
            log.notes.append(
                "Records in this change state different domain times; Core's valid time is one "
                f"per change set, so the change is admitted as {len(groups)} change sets."
            )
        elif untimed and groups[0][0].value is not None:
            log.notes.append(
                "Records with no specimen applicability ("
                + ", ".join(o["id"] for o in untimed)
                + f") receive this change set's valid time {groups[0][0].kind} "
                f"{groups[0][0].value} in record_history."
            )
        supersedes = self.supersessions(change, graph_objects)
        replay = None
        for number, (vt, members) in enumerate(groups):
            suffix = "" if len(groups) == 1 else f":{chr(ord('a') + number)}"
            change_set_id = f"change:{self.key}:{position}{suffix}"
            records = [r for o in members for r in encode(o, positions, self.key)]
            member_supersedes = {k: v for k, v in supersedes.items() if k in {o["id"] for o in members}}
            cited_here = sorted({ref for o in members for ref in o.get("evidence_refs", [])}) or source_ids
            built = compose(history, change_set_id, cited_here, [evidence_id], records, member_supersedes, vt)
            replay, attempt = admit(history, built)
            log.attempts.append(attempt)
            if replay is None and member_supersedes:
                # Core refused the declared replacement. Keep the refusal and
                # admit the same records without supersession, so later reads can
                # still be measured. The deviation is part of the result.
                log.outcome = "ADMITTED_WITHOUT_SUPERSESSION"
                log.notes.append(
                    "Core refused the explicit supersession; the records were then admitted "
                    "as plain additions, with the declared lineage kept only in an adopter slot."
                )
                built = compose(history, change_set_id, cited_here, [evidence_id], records, {}, vt)
                replay, attempt = admit(history, built)
                log.attempts.append(attempt)
                log.fallback_records += attempt.record_ids
            if replay is None:
                raise RuntimeError(f"{self.key} {position}: Core refused {attempt}")
        return replay, log


@dataclass
class Run:
    key: str
    driver: SpecimenDriver
    history: object
    path: Path
    positions: dict[str, tuple[str, int]] = field(default_factory=dict)
    snapshots: dict[str, bytes] = field(default_factory=dict)
    logs: list[ChangeLog] = field(default_factory=list)

    @property
    def fallback_records(self) -> set[str]:
        return {r for log in self.logs for r in log.fallback_records}

    @property
    def final(self):
        return self.history.replay()

    def at(self, label: str, history=None):
        history = history or self.history
        head, count = self.positions[label]
        final = history.replay()
        return history.replay_at(
            ledger_head=head,
            ledger_event_count=count,
            expected_head_hash=final.ledger_head,
            expected_event_count=final.ledger_event_count,
        )

    def label_of_change(self, change_set_id: str) -> str:
        return change_set_id.split(":", 2)[2].split(":")[0]

    def fork(self, label: str, name: str):
        path = self.path.with_name(f"{self.key}-{name}.jsonl")
        path.write_bytes(self.snapshots[label])
        return api.KnowledgeChangeHistory.reopen(path)


def build(
    key: str,
    workdir: Path,
    *,
    stop_after: str | None = None,
    hooks: dict[str, Callable[[Run], None]] | None = None,
    name: str = "main",
) -> Run:
    driver = SpecimenDriver(key)
    path = workdir / f"{key}-{name}.jsonl"
    history = api.create_structural_history(
        path, compilation=compile_contract(key), transaction_time=TX, actor_id=ACTOR
    )
    run = Run(key, driver, history, path)
    for change in driver.spec["changes"]:
        label = change["position"]
        if change["kind"] == "GENESIS":
            replay = history.replay()
            run.logs.append(ChangeLog(label, "GENESIS", "GENESIS"))
        else:
            replay, log = driver.apply_change(history, change, run.positions)
            run.logs.append(log)
        run.positions[label] = (replay.ledger_head, replay.ledger_event_count)
        run.snapshots[label] = path.read_bytes()
        if hooks and label in hooks:
            hooks[label](run)
        if label == stop_after:
            break
    return run
