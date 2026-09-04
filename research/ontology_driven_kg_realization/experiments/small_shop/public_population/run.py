"""Run the complete Small Shop fixture through the public Malleus facade."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import malleus.compiler as compiler


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[5]
PLAN_PATHS = tuple(
    HERE / "plans" / name
    for name in (
        "ret010.json",
        "invoice-base.json",
        "payment-e30.json",
        "supplier-e4.json",
        "supplier-e7.json",
    )
)

BASE_SCHEMA = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment/input/tbox/small-shop.yaml"
)
TARGET_SCHEMA = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment_full_public_v1/input/tbox/small-shop.yaml"
)
SHOP = ROOT / "research/ontology_driven_kg_realization/experiments/small_shop"
MACHINE_PATH = SHOP / "pareto/machine.json"
POLICY_PATH = SHOP / "pareto/policy.json"
BINDING_PATH = SHOP / "pareto/mapping.json"

SOURCE_PATHS = {
    "source:small-shop:inventory": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment/input/sources/inventory-units.csv"
    ),
    "source:small-shop:invoices": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment_settlement_v1/input/sources/invoices.csv"
    ),
    "source:small-shop:payments": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment_settlement_v1/input/sources/payments.jsonl"
    ),
    "source:small-shop:supplier-orders": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment_correction_v1/input/sources"
        / "supplier-order-history.jsonl"
    ),
    "source:small-shop:warehouse": (
        ROOT
        / "research/ontology_driven_kg_realization/fixtures"
        / "small_shop_fulfilment/input/sources/warehouse.jsonl"
    ),
}
EVIDENCE_PATHS = {
    "artifact:small-shop:baseline-mapping": BINDING_PATH,
    "artifact:small-shop:correction-mapping": SHOP / "correction/mapping.json",
    "artifact:small-shop:settlement-mapping": SHOP / "showcase/settlement-mapping.json",
}

ACTOR = "actor:small-shop-public-population"
TIMES = (
    "2026-09-04T00:00:00Z",
    "2026-09-04T00:01:00Z",
    "2026-09-04T00:02:00Z",
    "2026-09-04T00:03:00Z",
    "2026-09-04T00:04:00Z",
    "2026-09-04T00:05:00Z",
    "2026-09-04T00:06:00Z",
)


@dataclass(frozen=True, slots=True)
class FullShopRun:
    replay: compiler.KnowledgeHistoryReplay
    evidence_bytes: bytes


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _event(event_type: str, **payload: object) -> bytes:
    return _canonical({"event_type": event_type, "payload": payload})


def _artifact_anchor(
    record_id: str,
    content: bytes,
    role: str,
    media_type: str = "application/json",
) -> compiler.KnowledgeAnchorInput:
    return compiler.KnowledgeAnchorInput(
        machine_event=_event(
            "ARTIFACT_REGISTERED",
            artifact_id=record_id,
            artifact_identity=_digest(content),
        ),
        retained_bytes=content,
        media_type=media_type,
        role=role,
    )


def _source_anchors(
    source_id: str, content: bytes, media_type: str
) -> tuple[compiler.KnowledgeAnchorInput, compiler.KnowledgeAnchorInput]:
    artifact_id = source_id.replace("source:", "artifact:source:", 1)
    return (
        _artifact_anchor(artifact_id, content, "SOURCE_ARTIFACT", media_type),
        compiler.KnowledgeAnchorInput(
            machine_event=_event(
                "SOURCE_REGISTERED",
                artifact_id=artifact_id,
                source_id=source_id,
                source_identity=_digest(content),
            ),
            retained_bytes=content,
            media_type=media_type,
            role="RETAINED_SOURCE",
        ),
    )


def _compile_contract(schema: Path):
    return compiler.compile_linkml_contract(
        root_locator="small-shop",
        sources={
            "small-shop": schema.read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": (
                files("linkml_runtime")
                .joinpath("linkml_model", "model", "schema", "types.yaml")
                .read_bytes()
            ),
        },
    )


def _runtime(history_path: Path):
    base = _compile_contract(BASE_SCHEMA)
    target = _compile_contract(TARGET_SCHEMA)
    machine = compiler.ProtocolMachineProgram.from_bytes(MACHINE_PATH.read_bytes())
    policy = compiler.PolicyProgram.from_bytes(POLICY_PATH.read_bytes())
    normative = compiler.compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={"required-check-verdict": policy},
        capability_refs=(),
    )
    base_partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=base.artifact.validated_fact_set_sha256,
        normative_profile=normative,
    )
    target_partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=normative,
    )
    binding_data = json.loads(BINDING_PATH.read_bytes())["history_binding"]
    binding = compiler.KnowledgeChangeHistoryBinding.from_bytes(
        _canonical(binding_data)
    )
    history = compiler.KnowledgeChangeHistory(
        history_path,
        partial_contract=base_partial,
        contract_view=base.view,
        binding=binding,
    )
    return history, base, target, base_partial, target_partial, policy


def _bootstrap(
    history: compiler.KnowledgeChangeHistory,
    base,
    base_partial: compiler.PartialEffectiveContract,
) -> None:
    anchors = [
        _artifact_anchor(
            "artifact:small-shop:base-contract",
            base.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        _artifact_anchor(
            "artifact:small-shop:base-partial-contract",
            base_partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        _artifact_anchor(
            "artifact:small-shop:history-binding",
            history.binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
    ]
    anchors.extend(
        _artifact_anchor(record_id, path.read_bytes(), "RETAINED_EVIDENCE")
        for record_id, path in sorted(EVIDENCE_PATHS.items())
    )
    for source_id, path in sorted(SOURCE_PATHS.items()):
        media_type = "text/csv" if path.suffix == ".csv" else "application/x-ndjson"
        anchors.extend(_source_anchors(source_id, path.read_bytes(), media_type))
    results = history.append_anchors(
        anchors=tuple(anchors),
        transaction_time=TIMES[0],
        actor_id=ACTOR,
    )
    if any(result.machine_receipt.outcome != "APPLIED" for result in results):
        raise RuntimeError("Small Shop bootstrap was not applied")


def _load_plan(path: Path) -> dict[str, object]:
    try:
        source = path.read_bytes()
        plan = json.loads(source)
    except (OSError, UnicodeDecodeError, ValueError) as error:
        raise ValueError(f"population plan cannot be read: {path}") from error
    if not isinstance(plan, dict) or _canonical(plan) != source:
        raise ValueError(f"population plan must be strict canonical JSON: {path}")
    return plan


def _retention_events(
    plan: Mapping[str, object], *, include_profile: bool
) -> dict[str, bytes]:
    plan_id = plan["plan_id"]
    if not isinstance(plan_id, str) or not plan_id:
        raise ValueError("population plan ID is required")
    events = {
        plan_id: _event(
            "ARTIFACT_REGISTERED",
            artifact_id=plan_id,
            artifact_identity=_digest(_canonical(plan)),
        )
    }
    if include_profile:
        events["profile:state-version"] = _event(
            "ARTIFACT_REGISTERED",
            artifact_id="profile:state-version",
            artifact_identity=compiler.STATE_VERSION_PROFILE.identity,
        )
    return events


def _protocol_events(
    policy: compiler.PolicyProgram,
    change: compiler.KnowledgeChangeSet,
    state_identity: str,
    suffix: str,
) -> tuple[bytes, ...]:
    proposal_id = f"proposal:small-shop:{suffix}"
    checks = tuple(
        _event(
            "CHECK_RECORDED",
            check_contract_id=check_id,
            check_contract_identity=check_identity,
            outcome="SATISFIED",
            policy_identity=policy.identity,
            proposal_id=proposal_id,
            receipt_id=f"receipt:small-shop:{suffix}:{ordinal}",
        )
        for ordinal, (check_id, check_identity) in enumerate(policy.required_checks)
    )
    return (
        _event(
            "CHANGE_PROPOSED",
            expected_machine_state_identity=state_identity,
            knowledge_change_set_identity=change.identity,
            policy_id=policy.identifier,
            policy_identity=policy.identity,
            proposal_id=proposal_id,
        ),
        *checks,
        _event(
            "VERDICT_RECORDED",
            decision_id=f"decision:small-shop:{suffix}",
            proposal_id=proposal_id,
        ),
    )


def _admit_plan(
    history: compiler.KnowledgeChangeHistory,
    policy: compiler.PolicyProgram,
    path: Path,
    transaction_time: str,
) -> compiler.KnowledgeHistoryReplay:
    plan = _load_plan(path)
    prepared = compiler.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(compiler.STATE_VERSION_PROFILE.canonical_bytes),
        retention_events=_retention_events(
            plan,
            include_profile=not any(
                item.record_id == "profile:state-version"
                for item in history.replay().retained_inputs
            ),
        ),
        transaction_time=transaction_time,
        actor_id=ACTOR,
    )
    if prepared.change_set is None:
        raise RuntimeError(f"Small Shop plan produced no change: {path.name}")
    return history.admit(
        change_set=prepared.change_set,
        machine_events=_protocol_events(
            policy,
            prepared.change_set,
            prepared.retention_replay.machine_state.identity,
            path.stem,
        ),
        transaction_time=transaction_time,
        actor_id=ACTOR,
    )


def _build_history(history_path: Path) -> compiler.KnowledgeHistoryReplay:
    history, base, target, base_partial, target_partial, policy = _runtime(history_path)
    _bootstrap(history, base, base_partial)
    _admit_plan(history, policy, PLAN_PATHS[0], TIMES[1])
    revision = history.compose_contract_revision(
        revision_id="revision:small-shop:full-public-v1",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=target_partial.canonical_bytes,
        reason="add the full Small Shop conformance-fixture vocabulary",
        issued_at=TIMES[2],
    )
    history.record_contract_revision(
        revision=revision,
        transaction_time=TIMES[2],
        actor_id=ACTOR,
    )
    for path, transaction_time in zip(PLAN_PATHS[1:], TIMES[3:], strict=True):
        _admit_plan(history, policy, path, transaction_time)
    return compiler.KnowledgeChangeHistory.reopen(history_path).replay()


def _plain(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _trace_record(
    replay: compiler.KnowledgeHistoryReplay, record_id: str
) -> dict[str, object]:
    trace = compiler.trace_population_record(replay, record_id)
    history = trace.record_history
    return {
        "change_set_id": trace.change_set.change_set_id,
        "contract_identity": trace.change_set.contract_identity,
        "derivations": [_plain(item) for item in trace.derivations],
        "evidence": [
            {"record_id": item.record_id, "sha256": item.identity}
            for item in trace.evidence
        ],
        "history_profile": {
            "profile_id": trace.history_profile.profile_id,
            "sha256": trace.history_profile.identity,
        },
        "population_plan": {
            "plan_id": trace.population_plan["plan_id"],
            "sha256": trace.population_plan_identity,
        },
        "record_id": record_id,
        "record_type": history.operation.record_type,
        "sources": [
            {"record_id": item.record_id, "sha256": item.identity}
            for item in trace.sources
        ],
        "superseded_by": history.superseded_by,
        "supersedes_record_id": history.supersedes_record_id,
        "valid_from": {
            "kind": history.valid_from.kind,
            "value": history.valid_from.value,
        },
        "valid_to": (
            None
            if history.valid_to is None
            else {"kind": history.valid_to.kind, "value": history.valid_to.value}
        ),
    }


def _evidence(replay: compiler.KnowledgeHistoryReplay) -> bytes:
    graph = replay.graph.snapshot()
    contract_identities = tuple(
        dict.fromkeys(change.contract_identity for change in replay.change_sets)
    )
    traces = [
        _trace_record(replay, record_id) for record_id in sorted(replay.record_history)
    ]
    return (
        _canonical(
            {
                "claim": (
                    "The public Malleus facade deterministically compiles, admits, "
                    "reopens, replays, queries, and traces the complete Small Shop fixture."
                ),
                "contract_revision": {
                    "count": len(replay.contract_revisions),
                    "identities": list(contract_identities),
                    "revision_identity": replay.contract_revisions[0].identity,
                },
                "grammar": "malleus.small-shop.full-public-population-evidence/private-v0",
                "graph": graph,
                "history": {
                    "acceptance_head": replay.acceptance_head,
                    "change_set_count": len(replay.change_sets),
                    "ledger_event_count": replay.ledger_event_count,
                    "ledger_head": replay.ledger_head,
                    "materialization_head": replay.materialization_head,
                    "receipt_identity": replay.receipt.identity,
                },
                "limitations": [
                    "This is a conformance fixture, not a domain-independent protocol rule.",
                    "The five population plans are adopter-authored; no mapping DSL or source-to-plan compiler is claimed.",
                    "The state-version history profile is a fixture choice, not a universal domain-history model.",
                    "Event population, Semantic Re-entry, external effects, and a stable wire format remain out of scope.",
                ],
                "queries": {
                    "invoices": replay.graph.query("Invoice"),
                    "payment_settlements": replay.graph.query_relations(
                        "PaymentSettlesInvoiceRelation"
                    ),
                    "supplier_order_B": replay.graph.query(
                        "SupplierOrderState", supplier_order_id="B"
                    ),
                },
                "record_counts": {
                    "current": len(graph["nodes"]) + len(graph["relations"]),
                    "historical": len(replay.record_history),
                },
                "records": traces,
            }
        )
        + b"\n"
    )


def run_full_shop(output: Path) -> FullShopRun:
    """Run once, or reopen the retained history, then emit verified evidence."""

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    history_path = output / "history.jsonl"
    replay = (
        compiler.KnowledgeChangeHistory.reopen(history_path).replay()
        if history_path.exists()
        else _build_history(history_path)
    )
    evidence_bytes = _evidence(replay)
    (output / "evidence.json").write_bytes(evidence_bytes)
    return FullShopRun(replay, evidence_bytes)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    print(run_full_shop(arguments.output).evidence_bytes.decode("utf-8"))


if __name__ == "__main__":
    main()
