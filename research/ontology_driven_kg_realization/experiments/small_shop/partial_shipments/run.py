"""Synthetic partial shipments composed with the existing public Shop run."""

import argparse
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import malleus.compiler as api
from research.ontology_driven_kg_realization.experiments.small_shop.default_admission.run import (
    prepare_plan as prepare_existing_plan,
    run_shop,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ACTOR = "actor:synthetic-partial-shipments"
TIME = "2026-09-08T01:00:00Z"
MAPPING_ID = "artifact:partial-shipments:mapping"


def _canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(content):
    return "sha256:" + sha256(content).hexdigest()


def start(output: Path):
    """Run the prior Shop unchanged and retain this sibling's exact inputs."""
    inputs = {
        name: (HERE / f"{name}.jsonl").read_bytes() for name in ("order", "shipments")
    }
    mapping = (HERE / "mapping.json").read_bytes()
    run_shop(output)
    history = api.KnowledgeChangeHistory.reopen(output / "history.jsonl")
    anchors = [
        api.structural_evidence_anchor(
            record_id=MAPPING_ID, content=mapping, media_type="application/json"
        )
    ]
    for name, content in inputs.items():
        anchors.extend(
            api.structural_source_anchors(
                source_id=f"source:partial-shipments:{name}",
                artifact_id=f"artifact:partial-shipments:{name}",
                content=content,
                media_type="application/x-ndjson",
            )
        )
    history.append_anchors(
        anchors=tuple(anchors), transaction_time=TIME, actor_id=ACTOR
    )
    return history


def plan_for(history, name: str):
    """Build three fixed fixture plans from retained rows, not accepted answers."""
    if name not in {"order", "shipment-1", "shipment-2"}:
        raise ValueError(f"unknown partial-shipment step: {name}")
    replay = history.replay()
    mapping_bytes = replay.retained_bytes(MAPPING_ID)
    mapping = json.loads(mapping_bytes)
    source_id = "source:partial-shipments:" + (
        "order" if name == "order" else "shipments"
    )
    content = replay.retained_bytes(source_id)
    index = 0 if name in {"order", "shipment-1"} else 1
    row = json.loads(content.splitlines()[index])
    entities, relations, derivations = [], [], []

    def derive(record_id, path, field):
        derivations.append(
            {
                "record_id": record_id,
                "path": path,
                "source_id": source_id,
                "locator": f"row:{index}:{field}",
            }
        )

    def relation(role, source, target, source_field, target_field):
        rule = mapping["relations"][role]
        record_id = f"{role}:{source}:{target}"
        relations.append(
            {
                "id": record_id,
                "type": rule["type"],
                "source_id": source,
                "target_id": target,
                "properties": {"relation_type": rule["value"]},
            }
        )
        derive(record_id, ["source_id"], source_field)
        derive(record_id, ["target_id"], target_field)
        derive(record_id, ["properties", "relation_type"], target_field)

    if name == "order":
        entities.append(
            {
                "id": row["order_number"],
                "type": mapping["order_type"],
                "properties": {"order_number": row["order_number"]},
            }
        )
        derive(row["order_number"], ["properties", "order_number"], "order_number")
        for ordinal, unit in enumerate(row["unit_ids"]):
            entities.append(
                {
                    "id": unit,
                    "type": mapping["unit_type"],
                    "properties": {"product_code": row["product_code"]},
                }
            )
            derive(unit, ["properties", "product_code"], "product_code")
            relation(
                "contains",
                row["order_number"],
                unit,
                "order_number",
                f"unit_ids[{ordinal}]",
            )
    else:
        entities.append(
            {
                "id": row["shipment_id"],
                "type": mapping["shipment_type"],
                "properties": {"tracking_id": row["tracking_id"]},
            }
        )
        derive(row["shipment_id"], ["properties", "tracking_id"], "tracking_id")
        relation(
            "has_shipment",
            row["order_number"],
            row["shipment_id"],
            "order_number",
            "shipment_id",
        )
        relation(
            "ships_unit", row["shipment_id"], row["unit_id"], "shipment_id", "unit_id"
        )
    return {
        "adapter": mapping["adapter"],
        "grammar": mapping["plan_grammar"],
        "plan_id": f"plan:partial-shipments:{name}",
        "contract_identity": replay.partial_contract.identity,
        "history_profile": {
            "profile_id": "state-version",
            "sha256": api.STATE_VERSION_PROFILE.identity,
        },
        "records": {"entities": entities, "relations": relations},
        "sources": [{"source_id": source_id, "sha256": _digest(content)}],
        "evidence": [{"evidence_id": MAPPING_ID, "sha256": _digest(mapping_bytes)}],
        "derivations": derivations,
        "supersessions": [],
        "gaps": [],
        "valid_time": mapping["valid_time"],
    }


def prepare_plan(history, plan, *, transaction_time: str, actor_id: str):
    if isinstance(plan, str):
        plan = plan_for(history, plan)
    return prepare_existing_plan(
        history, plan, transaction_time=transaction_time, actor_id=actor_id
    )


def admit_plan(history, name: str, *, transaction_time: str, actor_id: str):
    prepared = prepare_plan(
        history, name, transaction_time=transaction_time, actor_id=actor_id
    )
    if prepared.change_set is None:
        raise ValueError(
            f"partial-shipment step {name} unexpectedly produced no change"
        )
    return api.admit_structural_change(
        history=history,
        preparation=prepared,
        transaction_time=transaction_time,
        actor_id=actor_id,
    )


def revise(history, *, transaction_time: str, actor_id: str):
    target = api.compile_linkml_contract(
        root_locator="small-shop",
        sources={
            "small-shop": (HERE / "small-shop-with-shipments.yaml").read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=api.STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    )
    revision = history.compose_contract_revision(
        revision_id="revision:partial-shipments",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=partial.canonical_bytes,
        reason="synthetic partial shipments with independent tracking and unit membership",
        issued_at=transaction_time,
    )
    history.record_contract_revision(
        revision=revision, transaction_time=transaction_time, actor_id=actor_id
    )
    return revision


def shipment_view(graph, order_id: str):
    """Read this fixture's explicit associations, without claiming delivery."""
    ordered = {
        r["target_id"]
        for r in graph.query_relations("OrderContainsUnit", source_id=order_id)
    }
    shipments, shipped = [], set()
    # Before the revision the graph has no Shipment vocabulary or records.
    links = [
        r
        for r in graph.snapshot()["relations"]
        if r["type"] == "OrderHasShipment" and r["source_id"] == order_id
    ]
    for link in sorted(links, key=lambda row: row["target_id"]):
        shipment = graph.get_node(link["target_id"])
        units = {
            r["target_id"]
            for r in graph.query_relations(
                "ShipmentContainsUnit", source_id=shipment["id"]
            )
        }
        shipments.append(
            {
                "shipment_id": shipment["id"],
                "tracking_id": shipment["tracking_id"],
                "units": sorted(units),
            }
        )
        shipped.update(units)
    return {
        "order_id": order_id,
        "ordered_units": sorted(ordered),
        "shipments": shipments,
        "remaining_units": sorted(ordered - shipped),
    }


def run_shipments(output: Path):
    output.mkdir(parents=True, exist_ok=False)
    history = start(output / "shop")
    before = history.replay()
    baseline = json.loads((output / "shop/evidence.json").read_bytes())
    # The prior runner's report binds the prefix before this extension's anchors.
    baseline_bytes = history.path.read_bytes().splitlines(keepends=True)[
        : baseline["ledger_event_count"]
    ]
    baseline_prefix = b"".join(baseline_bytes)
    if _digest(baseline_prefix) != baseline["ledger_sha256"]:
        raise ValueError("partial-shipment extension changed the original Shop prefix")
    admit_plan(history, "order", transaction_time=TIME, actor_id=ACTOR)
    checkpoints = {"after_order": shipment_view(history.replay().graph, "SYN-PS-ORDER")}
    revision = revise(history, transaction_time=TIME, actor_id=ACTOR)
    for name, label in (
        ("shipment-1", "after_first_shipment"),
        ("shipment-2", "after_second_shipment"),
    ):
        admit_plan(history, name, transaction_time=TIME, actor_id=ACTOR)
        checkpoints[label] = shipment_view(history.replay().graph, "SYN-PS-ORDER")
    path = history.path
    del history
    replay = api.KnowledgeChangeHistory.reopen(path).replay()
    prior_preserved = all(
        replay.record_history[key] == value
        for key, value in before.record_history.items()
    )
    before_graph, after_graph = before.graph.snapshot(), replay.graph.snapshot()
    prior_preserved = prior_preserved and all(
        row in after_graph[plane]
        for plane in ("nodes", "relations")
        for row in before_graph[plane]
    )
    if not prior_preserved:
        raise ValueError("partial shipments changed an earlier Shop record")
    traces = {}
    for shipment in ("SYN-S1", "SYN-S2"):
        trace = api.trace_population_record(replay, shipment)
        traces[shipment] = {
            "plan_id": trace.population_plan["plan_id"],
            "plan_identity": trace.population_plan_identity,
            "contract_identity": trace.change_set.contract_identity,
            "sources": [
                {"record_id": item.record_id, "identity": item.identity}
                for item in trace.sources
            ],
            "derivations": [
                dict(item, path=list(item["path"])) for item in trace.derivations
            ],
        }
    report = {
        "fixture": "synthetic-partial-shipments-v1",
        "checkpoints": checkpoints,
        "baseline_sha256": _digest(baseline_prefix),
        "baseline_byte_count": len(baseline_prefix),
        "prior_records_preserved": prior_preserved,
        "revision_identity": revision.identity,
        "ledger_sha256": _digest(path.read_bytes()),
        "ledger_head": replay.ledger_head,
        "ledger_event_count": replay.ledger_event_count,
        "receipt_identity": replay.receipt.identity,
        "change_count": len(replay.change_sets),
        "contract_revision_count": len(replay.contract_revisions),
        "graph": replay.graph.export_records(),
        "shipments": traces,
        "non_claims": [
            "Synthetic data, not observed shipments.",
            "Structural admission, not epistemic acceptance or source truth.",
            "No activity-to-entity migration, fulfilment policy, external delivery or Semantic Re-entry.",
        ],
    }
    (output / "evidence.json").write_bytes(_canonical(report) + b"\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, required=True, help="new output directory"
    )
    report = run_shipments(parser.parse_args().output)
    print(json.dumps(report["checkpoints"], indent=2))


if __name__ == "__main__":
    main()
