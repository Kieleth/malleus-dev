"""Shop content rules executed as a selected policy check at admission.

Two adopter rules run in trusted local Prolog over the candidate graph:
a quantity disagreement between two current records, and a record carrying no
property at all. A violated outcome refuses the whole atomic admission; the
policy grammar has no verdict that admits a change while recording a violation.
Rule 1 of the original three, "value in cited text", is not here: see README.md.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path

import malleus.compiler as api
from malleus.kg import KnowledgeGraph
from malleus.logic import LogicCheckResult, LogicContract, LogicError
from malleus.prolog_verifier import PrologVerifier
from malleus.staging import ProposedOperation, stage_subgraph

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    run as story,
)


HERE = Path(__file__).resolve().parent
ACTOR = "actor:shop-content-rules"
TIME = story.TIME
LOGIC_ID = "shop:content-rules:logic"
RULES_ID = "shop:content-rules:rules"
POLICY_REFERENCE = "required-check-verdict"


def canonical(value):
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()


def digest(content):
    return "sha256:" + sha256(content).hexdigest()


def event(kind, **payload):
    return canonical({"event_type": kind, "payload": payload})


def anchor(record_id, content, media_type, role="RETAINED_EVIDENCE"):
    return api.KnowledgeAnchorInput(
        machine_event=event(
            "ARTIFACT_REGISTERED",
            artifact_id=record_id,
            artifact_identity=digest(content),
        ),
        retained_bytes=content,
        media_type=media_type,
        role=role,
    )


def load_contract():
    return LogicContract.load(HERE / "logic.yaml")


def load_policy():
    return api.PolicyProgram.from_bytes(
        canonical(json.loads((HERE / "policy.json").read_bytes()))
    )


def start(path: Path):
    """Select the Shop content policy before the first record, in a fresh history."""
    if path.exists():
        raise ValueError("use a fresh history path; reopen existing history explicitly")
    compilation = story.compile_shop()
    profile, program = story.history_configuration()
    logic = load_contract()
    if not compilation.view.verifies(logic.ontology_hash):
        raise LogicError("Shop content rules require their exact compiled ontology")
    policy = load_policy()
    if policy.required_checks != ((logic.contract_id, logic.contract_hash),):
        raise LogicError("policy does not select this exact content-rule contract")
    normative = api.compose_normative_profile(
        protocol_machine_program=program,
        policy_programs={POLICY_REFERENCE: policy},
        capability_refs=(),
    )
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=compilation.artifact.validated_fact_set_sha256,
        normative_profile=normative,
    )
    binding = api.STRUCTURAL_HISTORY_BUNDLE.history_binding
    history = api.KnowledgeChangeHistory(
        path,
        partial_contract=partial,
        contract_view=compilation.view,
        binding=binding,
    )
    bootstrap = (
        anchor(
            "malleus:bootstrap:validated-contract",
            compilation.artifact.artifact_bytes,
            "application/json",
            "VALIDATED_CONTRACT",
        ),
        anchor(
            "malleus:bootstrap:partial-effective-contract",
            partial.canonical_bytes,
            "application/json",
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        anchor(
            "malleus:bootstrap:knowledge-history-binding",
            binding.canonical_bytes,
            "application/json",
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        anchor(LOGIC_ID, (HERE / "logic.yaml").read_bytes(), "application/yaml"),
        anchor(RULES_ID, logic.rules_source.encode(), "text/x-prolog"),
    )
    history.append_anchors(
        anchors=bootstrap + story_anchors(),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    return history, profile


def story_anchors():
    """The connected story's own retained sources and adapter evidence, unchanged."""
    return (
        *api.structural_source_anchors(
            source_id=story.SOURCE_ID,
            artifact_id="artifact:connected-shop:table-1",
            content=(story.HERE / "sources/table-1.jsonl").read_bytes(),
            media_type="application/x-ndjson",
        ),
        *api.structural_source_anchors(
            source_id="source:connected-shop:context",
            artifact_id="artifact:connected-shop:context",
            content=(story.HERE / "sources/context.jsonl").read_bytes(),
            media_type="application/x-ndjson",
        ),
        *(
            api.structural_evidence_anchor(
                record_id=record_id, content=file.read_bytes(), media_type=media
            )
            for record_id, file, media in (
                (story.MAPPING_ID, story.HERE / "mapping.json", "application/json"),
                (
                    "artifact:connected-shop:adapter",
                    story.HERE / "run.py",
                    "text/x-python",
                ),
                (
                    "artifact:connected-shop:source-boundary",
                    story.HERE / "source_boundary.json",
                    "application/json",
                ),
                (
                    "artifact:connected-shop:table-image",
                    story.HERE / "sources/table-1.png",
                    "image/png",
                ),
            )
        ),
    )


def prepare(history, plan, profile):
    """Compile and retain one plan through the public population path."""
    replay = history.replay()
    compiled = api.compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=profile,
    )
    return api.prepare_population_change(
        history=history,
        plan=plan,
        profile=profile,
        retention_events=api.population_retention_events(
            history=history, compilation=compiled, profile=profile
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )


def check_base(replay, change):
    """The accepted graph this candidate applies to, with its retirements removed.

    Core removes superseded records before applying a change. The check must see
    the same base, or an explicit replacement would read as a live disagreement.
    """
    retired = {
        operation.supersedes_record_id
        for operation in change.operations
        if operation.supersedes_record_id is not None
    }
    if not retired:
        return replay.graph
    kept = {
        family: [record for record in records if record["id"] not in retired]
        for family, records in replay.graph.export_records().items()
    }
    return KnowledgeGraph.from_records(replay.graph.registry, kept)


def check_writes(change):
    """Mirror the change's exact operations as proposed graph writes."""
    writes = []
    for operation in change.operations:
        writes.append(
            ProposedOperation(
                op_type=operation.operation_type,
                record_type=operation.record_type,
                record_id=operation.record_id,
                properties=dict(operation.properties),
                source_id=operation.source_id,
                target_id=operation.target_id,
            )
        )
    return writes


@dataclass(frozen=True)
class ContentAdmission:
    replay: api.KnowledgeHistoryReplay
    check: LogicCheckResult
    receipt_identity: str


class ContentRuleRefusal(ValueError):
    def __init__(self, check, refusal):
        self.check = check
        self.refusal = refusal
        super().__init__(f"Shop content policy {check.outcome}: {refusal}")


def admit(history, prepared):
    """Run the selected rules, then atomically admit their receipt and the change."""
    before = history.replay()
    if before.receipt.identity != prepared.retention_replay.receipt.identity:
        raise api.KnowledgeChangeRefusal(
            api.KnowledgeChangeRefusalReason.STALE_BASE,
            "Shop content preparation is stale",
        )
    if prepared.change_set is None:
        raise ValueError("Shop content episode requires a change set")
    change = api.KnowledgeChangeSet.from_bytes(prepared.change_set.canonical_bytes)
    logic = load_contract()
    for identifier, content in (
        (LOGIC_ID, (HERE / "logic.yaml").read_bytes()),
        (RULES_ID, logic.rules_source.encode()),
    ):
        if before.retained_bytes(identifier) != content:
            raise LogicError("rule evidence differs from the selected history")
    policy = before.partial_contract.normative_profile.policy(POLICY_REFERENCE)
    if json.loads(policy.canonical_bytes)["required_checks"] != [
        {
            "check_contract_id": logic.contract_id,
            "check_contract_identity": logic.contract_hash,
        }
    ]:
        raise LogicError("history policy does not select this exact logic contract")
    checked = PrologVerifier(logic).verify_candidate_subgraph(
        stage_subgraph(check_base(before, change), check_writes(change))
    )
    plan_id = prepared.compilation.plan_id
    receipt_bytes = canonical(
        {
            "check": asdict(checked),
            "knowledge_change_set_identity": change.identity,
            "population_plan_identity": digest(before.retained_bytes(plan_id)),
        }
    )
    receipt_identity = digest(receipt_bytes)
    receipt_id = f"receipt:{change.change_set_id}"
    receipt_anchor = anchor(receipt_id, receipt_bytes, "application/json")
    preview = api.execute_event(
        before.partial_contract, before.machine_state, receipt_anchor.machine_event
    )
    if preview.receipt.outcome != "APPLIED":
        raise LogicError("check receipt cannot enter the selected protocol machine")
    proposal = f"proposal:{change.change_set_id}"
    events = (
        event(
            "CHANGE_PROPOSED",
            expected_machine_state_identity=preview.state.identity,
            knowledge_change_set_identity=change.identity,
            policy_id=policy.identifier,
            policy_identity=policy.identity,
            proposal_id=proposal,
        ),
        event(
            "CHECK_RECORDED",
            check_contract_id=logic.contract_id,
            check_contract_identity=logic.contract_hash,
            outcome=checked.outcome,
            policy_identity=policy.identity,
            proposal_id=proposal,
            receipt_id=f"check:{change.change_set_id}",
        ),
        event(
            "VERDICT_RECORDED",
            decision_id=f"decision:{change.change_set_id}",
            proposal_id=proposal,
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
        raise ContentRuleRefusal(checked, error) from error
    return ContentAdmission(replay, checked, receipt_identity)


def honest_plans(history, profile):
    """Interpret every Table 1 row through the connected story's own adapter."""
    rows, boundary = story.load_sources(story.HERE)
    story.inspect_sources(rows, boundary)
    for ordinal, row in enumerate(rows):
        yield story.build_plan(history.replay(), profile, row, ordinal, boundary)


def synthetic_plan(replay, profile, kind: str):
    """One deliberately faulted candidate the structural gate alone admits.

    Both cite retained Table 1 cells, so neither is refused for a missing
    derivation. `conflict` asserts a second live quantity for order O1's X.
    `empty` derives only its `type` from a retained cell and carries no
    property at all, which is what Core's `UNDERIVED_RECORD` leaves for the
    rule layer: a record with a source and nothing said.
    """
    records = {
        "entities": [],
        "relations": [],
        "events": [],
        "event_participations": [],
    }
    derivations = []
    if kind == "conflict":
        record_id = "state:order:O1:X:synthetic-conflict"
        records["entities"].append(
            {
                "id": record_id,
                "type": "SalesOrderState",
                "properties": {
                    "order_id": "order:O1",
                    "product_code": "X",
                    "ordered_quantity": 9,
                    "source_occurrence_id": "e1",
                },
            }
        )
        derivations = [
            {
                "record_id": record_id,
                "path": ["properties", field],
                "source_id": story.SOURCE_ID,
                "locator": f"row:0:{locator}",
            }
            for field, locator in (
                ("order_id", "order_ids[0]"),
                ("product_code", "order_details_text"),
                ("ordered_quantity", "order_details_text"),
                ("source_occurrence_id", "event_id"),
            )
        ]
    elif kind == "empty":
        record_id = "synthetic:empty-record"
        records["entities"].append(
            {
                "id": record_id,
                "type": "https://malleus.dev/schema/Entity",
                "properties": {},
            }
        )
        derivations = [
            {
                "record_id": record_id,
                "path": ["type"],
                "source_id": story.SOURCE_ID,
                "locator": "row:0:event_id",
            }
        ]
    else:
        raise ValueError(f"unknown synthetic candidate: {kind}")
    return {
        "grammar": "malleus.population-plan/private-v0",
        "adapter": json.loads(replay.retained_bytes(story.MAPPING_ID))["adapter"],
        "contract_identity": replay.partial_contract.identity,
        "plan_id": f"plan:shop-content-rules:{kind}",
        "history_profile": {
            "profile_id": profile.profile_id,
            "sha256": profile.identity,
        },
        "sources": [
            {
                "source_id": story.SOURCE_ID,
                "sha256": digest(replay.retained_bytes(story.SOURCE_ID)),
            }
        ],
        "evidence": [
            {
                "evidence_id": story.MAPPING_ID,
                "sha256": digest(replay.retained_bytes(story.MAPPING_ID)),
            }
        ],
        "records": records,
        "derivations": derivations,
        "gaps": [],
        "supersessions": [],
        "valid_time": json.loads(replay.retained_bytes(story.MAPPING_ID))["valid_time"],
    }


def refuse_synthetic(history, profile, kind: str):
    """Submit one faulted candidate and require the ledger to stay where it was."""
    prepared = prepare(
        history, synthetic_plan(history.replay(), profile, kind), profile
    )
    before = history.path.read_bytes()
    try:
        admit(history, prepared)
    except ContentRuleRefusal as error:
        return {
            "kind": kind,
            "outcome": error.check.outcome,
            "violations": [asdict(item) for item in error.check.violations],
            "refusal_reason": error.refusal.reason.name,
            "ledger_unchanged": history.path.read_bytes() == before,
        }
    raise RuntimeError(f"synthetic {kind} candidate was accepted")


def run(path: Path, *, probe: bool = True):
    """Admit the honest Table 1 rows, then optionally submit the faulted candidates.

    A refused candidate appends nothing, but its earlier preparation retains the
    plan bytes, so ``probe=False`` gives the ledger the honest rows alone.
    """
    history, profile = start(path)
    for plan in honest_plans(history, profile):
        admit(history, prepare(history, plan, profile))
    refusals = (
        [refuse_synthetic(history, profile, kind) for kind in ("conflict", "empty")]
        if probe
        else []
    )
    replay = api.KnowledgeChangeHistory.reopen(path).replay()
    return {
        "refusals": refusals,
        "graph": replay.graph.export_records(),
        "history_identity": replay.receipt.identity,
        "ledger_sha256": digest(path.read_bytes()),
        "ledger_events": replay.ledger_event_count,
        "accepted_changes": len(replay.change_sets),
        "historical_records": len(replay.record_history),
        "rule_contract_identity": load_contract().contract_hash,
        "policy_identity": load_policy().identity,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.history), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
