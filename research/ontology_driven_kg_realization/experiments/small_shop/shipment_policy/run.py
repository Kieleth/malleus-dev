"""Bounded Shop policy consumer. Core executes the declared rule and policy.

Trusted local Prolog, insert-only candidates, no policy migration. Replay
preserves check attestations; it does not independently prove execution or truth.
"""

import argparse
from dataclasses import asdict, dataclass
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import malleus.compiler as api
from malleus.logic import LogicCheckResult, LogicContract, LogicError
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, stage_subgraph
from research.ontology_driven_kg_realization.experiments.small_shop.partial_shipments import (
    run as shipments,
)


HERE = Path(__file__).resolve().parent
ACTOR = "actor:shop-shipment-policy"
TIME = "2026-09-08T02:00:00Z"


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(content):
    return "sha256:" + sha256(content).hexdigest()


def event(kind, **payload):
    return canonical({"event_type": kind, "payload": payload})


def anchor(record_id, content, role="RETAINED_EVIDENCE"):
    return api.KnowledgeAnchorInput(
        machine_event=event(
            "ARTIFACT_REGISTERED",
            artifact_id=record_id,
            artifact_identity=digest(content),
        ),
        retained_bytes=content,
        media_type="application/octet-stream",
        role=role,
    )


def start(path: Path):
    """Select the Shop policy before the first record, never migrate old history."""
    if path.exists():
        raise ValueError("use a fresh history path; reopen existing history explicitly")
    compilation = api.compile_linkml_contract(
        root_locator="small-shop",
        sources={
            "small-shop": (
                shipments.HERE / "small-shop-with-shipments.yaml"
            ).read_bytes(),
            "malleus": (shipments.ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )
    logic = LogicContract.load(HERE / "logic.yaml")
    if not compilation.view.verifies(logic.ontology_hash):
        raise LogicError("Shop rule contract requires its exact compiled ontology")
    policy = api.PolicyProgram.from_bytes(
        canonical(json.loads((HERE / "policy.json").read_bytes()))
    )
    machine = api.ProtocolMachineProgram.from_bytes(
        (HERE.parent / "correction/machine.json").read_bytes()
    )
    profile = api.compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={"required-check-verdict": policy},
        capability_refs=(),
    )
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=profile,
    )
    binding = api.STRUCTURAL_HISTORY_BUNDLE.history_binding
    history = api.KnowledgeChangeHistory(
        path,
        partial_contract=partial,
        contract_view=compilation.view,
        binding=binding,
    )
    anchors = [
        anchor(
            "shop:validated-contract",
            compilation.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        anchor(
            "shop:partial-contract",
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        anchor(
            "shop:history-binding", binding.canonical_bytes, "KNOWLEDGE_HISTORY_BINDING"
        ),
        anchor("shop:logic", (HERE / "logic.yaml").read_bytes()),
        anchor("shop:rules", logic.rules_source.encode()),
        anchor(shipments.MAPPING_ID, (shipments.HERE / "mapping.json").read_bytes()),
    ]
    for name, source in (
        ("order", shipments.HERE / "order.jsonl"),
        ("shipments", shipments.HERE / "shipments.jsonl"),
        ("duplicate-unit", HERE / "duplicate-unit.jsonl"),
    ):
        anchors.extend(
            api.structural_source_anchors(
                source_id=f"source:partial-shipments:{name}",
                artifact_id=f"artifact:partial-shipments:{name}",
                content=source.read_bytes(),
                media_type="application/x-ndjson",
            )
        )
    history.append_anchors(
        anchors=tuple(anchors), transaction_time=TIME, actor_id=ACTOR
    )
    return history


def prepare(history, name: str):
    """Retain a truthful plan, including the deliberately conflicting source."""
    if name == "duplicate-unit":
        plan = shipments.plan_for(
            history, "shipment-2", source_id="source:partial-shipments:duplicate-unit"
        )
        plan["plan_id"] += ":duplicate-unit"
    else:
        plan = shipments.plan_for(history, name)
    replay = history.replay()
    for identifier in ("shop:logic", "shop:rules"):
        plan["evidence"].append(
            {
                "evidence_id": identifier,
                "sha256": digest(replay.retained_bytes(identifier)),
            }
        )
    return shipments.prepare_plan(history, plan, transaction_time=TIME, actor_id=ACTOR)


@dataclass(frozen=True)
class ShipmentAdmission:
    replay: api.KnowledgeHistoryReplay
    check: LogicCheckResult
    receipt_identity: str


class ShipmentPolicyRefusal(ValueError):
    def __init__(self, check, refusal):
        self.check = check
        self.refusal = refusal
        super().__init__(f"Shop policy {check.outcome}: {refusal}")


def admit(history, prepared):
    """Run the selected rule, then atomically admit its receipt and exact KCS.

    No caller-supplied check outcome. Only this fixture's insert-only Entity and
    Relation operations are supported. Preparation is a prior retention step.
    """
    before = history.replay()
    if before.receipt.identity != prepared.retention_replay.receipt.identity:
        raise api.KnowledgeChangeRefusal(
            api.KnowledgeChangeRefusalReason.STALE_BASE, "Shop preparation is stale"
        )
    if prepared.change_set is None:
        raise ValueError("Shop episode requires a change set, not NO_DOMAIN_CHANGE")
    change = api.KnowledgeChangeSet.from_bytes(prepared.change_set.canonical_bytes)
    logic = LogicContract.load(HERE / "logic.yaml")
    for identifier, content in (
        ("shop:logic", (HERE / "logic.yaml").read_bytes()),
        ("shop:rules", logic.rules_source.encode()),
    ):
        if (identifier, digest(content)) not in change.evidence:
            raise LogicError("change does not bind the selected rule evidence")
        if before.retained_bytes(identifier) != content:
            raise LogicError("rule evidence differs from the selected history")
    policy = before.partial_contract.normative_profile.policy("required-check-verdict")
    if json.loads(policy.canonical_bytes)["required_checks"] != [
        {
            "check_contract_id": logic.contract_id,
            "check_contract_identity": logic.contract_hash,
        }
    ]:
        raise LogicError("history policy does not select this exact logic contract")
    writes = []
    for op in change.operations:
        if op.supersedes_record_id is not None or op.operation_type not in {
            "CREATE_ENTITY",
            "CREATE_RELATION",
        }:
            raise LogicError(
                "Shop rule episode supports insert-only Entity/Relation operations"
            )
        writes.append(
            ProposedOperation(
                op_type=op.operation_type,
                record_type=op.record_type,
                record_id=op.record_id,
                properties=dict(op.properties),
                source_id=op.source_id,
                target_id=op.target_id,
            )
        )
    checked = PrologVerifier(logic).verify_candidate_subgraph(
        stage_subgraph(before.graph, writes)
    )
    plan_id = prepared.compilation.plan_id
    plan_bytes = before.retained_bytes(plan_id)
    if (plan_id, digest(plan_bytes)) not in change.evidence:
        raise LogicError("change does not bind its retained population plan")
    receipt_bytes = canonical(
        {
            "knowledge_change_set_identity": change.identity,
            "population_plan_identity": digest(plan_bytes),
            "check": asdict(checked),
        }
    )
    receipt_identity = digest(receipt_bytes)
    receipt_anchor = anchor(receipt_identity, receipt_bytes)
    preview = api.execute_event(
        before.partial_contract, before.machine_state, receipt_anchor.machine_event
    )
    if preview.receipt.outcome != "APPLIED":
        raise LogicError("check receipt cannot enter the selected protocol machine")
    proposal = "proposal:" + change.identity
    events = (
        event(
            "CHANGE_PROPOSED",
            proposal_id=proposal,
            expected_machine_state_identity=preview.state.identity,
            knowledge_change_set_identity=change.identity,
            policy_id=policy.identifier,
            policy_identity=policy.identity,
        ),
        event(
            "CHECK_RECORDED",
            proposal_id=proposal,
            check_contract_id=logic.contract_id,
            check_contract_identity=logic.contract_hash,
            outcome=checked.outcome,
            policy_identity=policy.identity,
            receipt_id="check:" + change.identity,
            receipt_identity=receipt_identity,
        ),
        event(
            "VERDICT_RECORDED",
            proposal_id=proposal,
            decision_id="decision:" + change.identity,
        ),
    )
    try:
        replay = history.admit_with_anchors(
            anchors=(receipt_anchor,),
            change_set=change,
            machine_events=events,
            transaction_time=TIME,
            actor_id=ACTOR,
        )
    except api.KnowledgeChangeRefusal as error:
        raise ShipmentPolicyRefusal(checked, error) from error
    return ShipmentAdmission(replay, checked, receipt_identity)


def run(path: Path):
    history = start(path)
    for step in ("order", "shipment-1"):
        admit(history, prepare(history, step))
    rejected = prepare(history, "duplicate-unit")
    before = path.read_bytes()
    try:
        admit(history, rejected)
    except ShipmentPolicyRefusal as error:
        refusal = {
            "outcome": error.check.outcome,
            "violations": [asdict(v) for v in error.check.violations],
            "ledger_unchanged": path.read_bytes() == before,
        }
        if (
            not refusal["ledger_unchanged"]
            or error.check.outcome != "VIOLATED"
            or error.refusal.reason
            is not api.KnowledgeChangeRefusalReason.REJECTED_CHANGE
        ):
            raise RuntimeError(
                "duplicate-unit refusal did not preserve the admission prefix"
            ) from error
    else:
        raise RuntimeError("duplicate-unit assignment was accepted")
    result = admit(history, prepare(history, "shipment-2"))
    reopened = api.KnowledgeChangeHistory.reopen(path).replay()
    if reopened.receipt.identity != result.replay.receipt.identity:
        raise RuntimeError("reopen changed the history receipt")
    return {
        "duplicate_unit": refusal,
        "shipments": shipments.shipment_view(reopened.graph, "SYN-PS-ORDER"),
        "history_identity": reopened.receipt.identity,
        "ledger_sha256": digest(path.read_bytes()),
        "event_count": reopened.ledger_event_count,
        "accepted_changes": len(reopened.change_sets),
        "check_receipt_identity": result.receipt_identity,
        "rule_contract_identity": result.check.contract_hash,
        "rule_bytes_identity": result.check.ruleset_hash,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.history), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
