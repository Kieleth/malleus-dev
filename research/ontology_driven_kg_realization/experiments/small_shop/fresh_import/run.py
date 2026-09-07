"""Extend the full Shop with a synthetic supplier file through public Core."""

import argparse
import json
from pathlib import Path

import malleus.compiler as api
from research.ontology_driven_kg_realization.experiments.small_shop.default_admission.run import (
    prepare_plan,
    run_shop,
)
from research.ontology_driven_kg_realization.experiments.small_shop.fresh_import import (
    adapter,
)


HERE = Path(__file__).resolve().parent
SOURCE_ID = "source:small-shop:fresh-suppliers"
PLAN_ID = "plan:small-shop:fresh-suppliers"
IMPLEMENTATION_ID = "artifact:small-shop:fresh-import:adapter"
TIME = "2026-09-06T01:00:00Z"
ACTOR = "actor:small-shop-fresh-import"


def evidence_anchor(record_id: str, content: bytes, media_type: str):
    return api.KnowledgeAnchorInput(
        machine_event=adapter.canonical(
            {
                "event_type": "ARTIFACT_REGISTERED",
                "payload": {
                    "artifact_id": record_id,
                    "artifact_identity": adapter.digest(content),
                },
            }
        ),
        retained_bytes=content,
        role="RETAINED_EVIDENCE",
        media_type=media_type,
    )


def start_existing_shop(output: Path):
    run_shop(output)
    return api.KnowledgeChangeHistory.reopen(output / "history.jsonl")


def prepare_import(history, source: bytes, *, transaction_time: str, actor_id: str):
    """Validate rows and structure before retention, then prepare against history."""
    replay = history.replay()
    plan = adapter.adapt_supplier_rows(
        source_bytes=source,
        source_id=SOURCE_ID,
        plan_id=PLAN_ID,
        contract_identity=replay.partial_contract.identity,
    )
    implementation = Path(adapter.__file__).read_bytes()
    plan["evidence"].append(
        {"evidence_id": IMPLEMENTATION_ID, "sha256": adapter.digest(implementation)}
    )
    api.compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=api.STATE_VERSION_PROFILE,
    )
    artifact_id = "artifact:" + SOURCE_ID
    source_identity = adapter.digest(source)
    source_artifact = api.KnowledgeAnchorInput(
        machine_event=adapter.canonical(
            {
                "event_type": "ARTIFACT_REGISTERED",
                "payload": {
                    "artifact_id": artifact_id,
                    "artifact_identity": source_identity,
                },
            }
        ),
        retained_bytes=source,
        role="SOURCE_ARTIFACT",
        media_type="application/x-ndjson",
    )
    source_record = api.KnowledgeAnchorInput(
        machine_event=adapter.canonical(
            {
                "event_type": "SOURCE_REGISTERED",
                "payload": {
                    "artifact_id": artifact_id,
                    "source_id": SOURCE_ID,
                    "source_identity": source_identity,
                },
            }
        ),
        retained_bytes=source,
        role="RETAINED_SOURCE",
        media_type="application/x-ndjson",
    )
    mapping_id = json.loads(adapter.MAPPING_BYTES)["evidence_id"]
    history.append_anchors(
        anchors=(
            source_artifact,
            source_record,
            evidence_anchor(mapping_id, adapter.MAPPING_BYTES, "application/json"),
            evidence_anchor(IMPLEMENTATION_ID, implementation, "text/x-python"),
        ),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    return prepare_plan(
        history, plan, transaction_time=transaction_time, actor_id=actor_id
    )


def run_import(output: Path):
    """Run the prior Shop, import fresh rows, discard memory, reopen and trace."""
    source = (HERE / "supplier-orders.jsonl").read_bytes()
    output.mkdir(parents=True, exist_ok=False)
    history = start_existing_shop(output / "shop")
    before = history.replay()
    prepared = prepare_import(history, source, transaction_time=TIME, actor_id=ACTOR)
    api.admit_structural_change(
        history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
    )
    path = history.path
    del history
    replay = api.KnowledgeChangeHistory.reopen(path).replay()
    change = replay.change_sets[-1]
    records = []
    for operation in change.operations:
        trace = api.trace_population_record(replay, operation.record_id)
        records.append(
            {
                "record": replay.graph.get_node(operation.record_id),
                "plan_id": trace.population_plan["plan_id"],
                "source_identity": trace.sources[0].identity,
                "derivations": [
                    dict(item, path=list(item["path"])) for item in trace.derivations
                ],
            }
        )
    prior_unchanged = all(
        replay.record_history[key] == value
        for key, value in before.record_history.items()
    )
    before_graph, after_graph = before.graph.snapshot(), replay.graph.snapshot()
    prior_unchanged = prior_unchanged and (
        before_graph["relations"] == after_graph["relations"]
        and all(row in after_graph["nodes"] for row in before_graph["nodes"])
    )
    if not prior_unchanged:
        raise ValueError("fresh supplier import changed a prior Shop record")
    report = {
        "fixture": "synthetic-supplier-import-v1",
        "rows_imported": len(records),
        "rows_gapped": 0,
        "prior_records_unchanged": prior_unchanged,
        "ledger_sha256": adapter.digest(path.read_bytes()),
        "ledger_head": replay.ledger_head,
        "ledger_event_count": replay.ledger_event_count,
        "receipt_identity": replay.receipt.identity,
        "source_identity": adapter.digest(source),
        "records": records,
        "non_claims": [
            "Synthetic inputs, not observed supplier data.",
            "Structural admission, not source truth or epistemic acceptance.",
            "No inferred correction, domain time, external effect, or Semantic Re-entry.",
        ],
    }
    (output / "evidence.json").write_bytes(adapter.canonical(report) + b"\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, required=True, help="new output directory"
    )
    args = parser.parse_args()
    report = run_import(args.output)
    print(
        f"Imported {report['rows_imported']} synthetic supplier rows; {args.output / 'evidence.json'}"
    )


if __name__ == "__main__":
    main()
