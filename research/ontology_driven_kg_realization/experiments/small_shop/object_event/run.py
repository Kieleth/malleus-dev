"""Run the Small Shop e27 occurrence through governed object-event history."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import malleus.compiler as compiler

from research.ontology_driven_kg_realization.experiments.small_shop.public_population.run import (
    _artifact_anchor,
    _canonical,
    _digest,
    _event,
    _protocol_events,
    _source_anchors,
)


ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
FIXTURE = (
    ROOT
    / "research/ontology_driven_kg_realization/fixtures"
    / "small_shop_fulfilment_object_event_v1"
)
PLAN_PATH = FIXTURE / "input/population/ret-040.json"
SOURCE_PATH = FIXTURE / "input/sources/warehouse.jsonl"
TIME_CONTEXT_PATH = FIXTURE / "input/configuration/time-context.json"
MAPPING_PATH = FIXTURE / "input/configuration/mapping.json"
SCHEMA_PATH = FIXTURE / "input/tbox/small-shop-object-event.yaml"
ORACLE_PATH = FIXTURE / "oracle/ret-040.json"
EXPECTED_EVIDENCE_PATH = HERE / "evidence.json"
OBJECT_EVENT_SCHEMA_PATH = ROOT / "ontology/profiles/object-event.yaml"
SHOP = ROOT / "research/ontology_driven_kg_realization/experiments/small_shop"
MACHINE_PATH = SHOP / "pareto/machine.json"
POLICY_PATH = SHOP / "pareto/policy.json"
BINDING_PATH = SHOP / "pareto/mapping.json"

ACTOR = "actor:small-shop-object-event"
BOOTSTRAP_TIME = "2026-09-04T01:00:00Z"
ADMISSION_TIME = "2026-09-04T01:01:00Z"


@dataclass(frozen=True, slots=True)
class ObjectEventRun:
    replay: compiler.KnowledgeHistoryReplay
    evidence_bytes: bytes


def _compile_contract():
    return compiler.compile_linkml_contract(
        root_locator="small-shop-object-event",
        sources={
            "small-shop-object-event": SCHEMA_PATH.read_bytes(),
            "object-event": OBJECT_EVENT_SCHEMA_PATH.read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": (
                files("linkml_runtime")
                .joinpath("linkml_model", "model", "schema", "types.yaml")
                .read_bytes()
            ),
        },
    )


def _runtime(history_path: Path):
    compiled = _compile_contract()
    machine = compiler.ProtocolMachineProgram.from_bytes(MACHINE_PATH.read_bytes())
    policy = compiler.PolicyProgram.from_bytes(POLICY_PATH.read_bytes())
    normative = compiler.compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={"required-check-verdict": policy},
        capability_refs=(),
    )
    partial = compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
        normative_profile=normative,
    )
    binding = compiler.KnowledgeChangeHistoryBinding.from_bytes(
        _canonical(json.loads(BINDING_PATH.read_bytes())["history_binding"])
    )
    history = compiler.KnowledgeChangeHistory(
        history_path,
        partial_contract=partial,
        contract_view=compiled.view,
        binding=binding,
    )
    return history, compiled, partial, policy


def _bootstrap(
    history: compiler.KnowledgeChangeHistory,
    compiled,
    partial: compiler.PartialEffectiveContract,
) -> None:
    anchors = [
        _artifact_anchor(
            "artifact:small-shop:object-event-contract",
            compiled.artifact.artifact_bytes,
            "VALIDATED_CONTRACT",
        ),
        _artifact_anchor(
            "artifact:small-shop:object-event-partial-contract",
            partial.canonical_bytes,
            "PARTIAL_EFFECTIVE_CONTRACT",
        ),
        _artifact_anchor(
            "artifact:small-shop:object-event-history-binding",
            history.binding.canonical_bytes,
            "KNOWLEDGE_HISTORY_BINDING",
        ),
        _artifact_anchor(
            "artifact:small-shop:object-event-mapping",
            MAPPING_PATH.read_bytes(),
            "RETAINED_EVIDENCE",
        ),
        _artifact_anchor(
            "artifact:small-shop:object-event-time-context",
            TIME_CONTEXT_PATH.read_bytes(),
            "RETAINED_EVIDENCE",
        ),
        *_source_anchors(
            "source:small-shop:object-event:warehouse",
            SOURCE_PATH.read_bytes(),
            "application/x-ndjson",
        ),
    ]
    history.append_anchors(
        anchors=tuple(anchors),
        transaction_time=BOOTSTRAP_TIME,
        actor_id=ACTOR,
    )


def _build(history_path: Path) -> compiler.KnowledgeHistoryReplay:
    history, compiled, partial, policy = _runtime(history_path)
    _bootstrap(history, compiled, partial)
    plan = json.loads(PLAN_PATH.read_bytes())
    plan_bytes = _canonical(plan)
    prepared = compiler.prepare_population_change(
        history=history,
        plan=plan,
        profile=compiler.OBJECT_EVENT_PROFILE,
        retention_events={
            "profile:object-event": _event(
                "ARTIFACT_REGISTERED",
                artifact_id="profile:object-event",
                artifact_identity=compiler.OBJECT_EVENT_PROFILE.identity,
            ),
            plan["plan_id"]: _event(
                "ARTIFACT_REGISTERED",
                artifact_id=plan["plan_id"],
                artifact_identity=_digest(plan_bytes),
            ),
        },
        transaction_time=ADMISSION_TIME,
        actor_id=ACTOR,
    )
    if prepared.change_set is None:
        raise RuntimeError("Small Shop object-event plan produced no change")
    history.admit(
        change_set=prepared.change_set,
        machine_events=_protocol_events(
            policy,
            prepared.change_set,
            prepared.retention_replay.machine_state.identity,
            "ret-040-object-event",
        ),
        transaction_time=ADMISSION_TIME,
        actor_id=ACTOR,
    )
    return compiler.KnowledgeChangeHistory.reopen(history_path).replay()


def _evidence(
    replay: compiler.KnowledgeHistoryReplay, history_bytes: bytes
) -> bytes:
    oracle = json.loads(ORACLE_PATH.read_bytes())
    event = replay.graph.query("PackShipmentEvent")
    participations = replay.graph.query_event_participations(event_id="e27")
    entities = [
        [record["id"], record["type"]]
        for record in replay.graph.query("Entity")
    ]
    expected = oracle["expected"]
    observed_participations = [
        [
            record["id"],
            record["event_id"],
            record["entity_id"],
            record["qualifier"],
        ]
        for record in participations
    ]
    oracle_matches = (
        entities == expected["entities"]
        and event
        == [
            {
                **expected["event"],
                "is_event": True,
            }
        ]
        and observed_participations == expected["participations"]
        and len(replay.graph.query_relations()) == expected["relation_count"]
    )
    return _canonical(
        {
            "claim": (
                "One controlled packing occurrence passed from ontology and source "
                "through a governed change set, ledger admission, reopen, replay, "
                "and qualified Event-to-Entity queries."
            ),
            "contract_identity": replay.partial_contract.identity,
            "graph_state_digest": replay.graph.state_digest(),
            "history": {
                "change_set_count": len(replay.change_sets),
                "ledger_event_count": replay.ledger_event_count,
                "ledger_head": replay.ledger_head,
                "ledger_sha256": "sha256:" + sha256(history_bytes).hexdigest(),
                "receipt_identity": replay.receipt.identity,
            },
            "history_profile": {
                "profile_id": compiler.OBJECT_EVENT_PROFILE.profile_id,
                "sha256": compiler.OBJECT_EVENT_PROFILE.identity,
            },
            "limitations": [
                "No Event-to-Event ordering is represented.",
                "No source-to-plan mapping language is claimed.",
                "The fixture ontology is not Malleus protocol vocabulary.",
            ],
            "observed": {
                "entities": entities,
                "event": event,
                "participations": observed_participations,
                "relation_count": len(replay.graph.query_relations()),
            },
            "oracle_matches": oracle_matches,
            "plan_identity": _digest(replay.retained_bytes("plan:small-shop:ret-040-object-event")),
            "schema": "malleus.small-shop.object-event-evidence/private-v0",
            "source_identity": _digest(SOURCE_PATH.read_bytes()),
        }
    ) + b"\n"


def run_object_event(output: Path) -> ObjectEventRun:
    """Build once or reopen, then return deterministic evidence."""

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    history_path = output / "history.jsonl"
    replay = (
        compiler.KnowledgeChangeHistory.reopen(history_path).replay()
        if history_path.exists()
        else _build(history_path)
    )
    evidence_bytes = _evidence(replay, history_path.read_bytes())
    (output / "evidence.json").write_bytes(evidence_bytes)
    return ObjectEventRun(replay, evidence_bytes)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    print(run_object_event(arguments.output).evidence_bytes.decode("utf-8"))


if __name__ == "__main__":
    main()
