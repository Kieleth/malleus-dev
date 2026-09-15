"""Append a labelled synthetic shipment cohort to the frozen warehouse history."""

import argparse
from importlib.resources import files
import json
from pathlib import Path

from malleus import bundled_ontology_path
import malleus.compiler as api
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    run as base,
)
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.warehouse import (
    run as warehouse,
)
from research.ontology_driven_kg_realization.experiments.small_shop.partial_shipments.run import (
    shipment_view,
)


HERE = Path(__file__).resolve().parent
TIME = "2026-09-14T01:00:00Z"  # Fixed import time, not a source domain date.
ACTOR = "actor:connected-shop-synthetic-shipments"
MAPPING_ID = "artifact:connected-shop:shipment-mapping"
BOUNDARY_ID = "artifact:connected-shop:shipment-boundary"
ADAPTER_ID = "artifact:connected-shop:shipment-adapter"


def source_id(name):
    return json.loads((HERE / "input_boundary.json").read_bytes())["sources"][name][
        "source_id"
    ]


def start(path, *, directory=HERE):
    """Check exact inputs first; append an additive revision and retained inputs.

    Each Core write is atomic. This fixture is not a whole-import transaction
    or a resume mechanism, and it does not install another admission policy.
    """
    boundary_bytes = (directory / "input_boundary.json").read_bytes()
    boundary = json.loads(boundary_bytes)
    sources = {}
    for name, spec in boundary["sources"].items():
        content = (directory / spec["path"]).read_bytes()
        if base.digest(content) != spec["sha256"]:
            raise ValueError(f"Synthetic source digest differs: {name}")
        sources[name] = content
    path = Path(path)
    prefix = path.read_bytes()
    if (
        len(prefix) != boundary["baseline_history_bytes"]
        or base.digest(prefix) != boundary["baseline_history_sha256"]
    ):
        raise ValueError("Synthetic extension requires the exact warehouse history")
    target = api.compile_linkml_contract(
        root_locator="shop",
        sources={
            "shop": (directory / "shop.yaml").read_bytes(),
            "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
            "object-event": bundled_ontology_path(
                "profiles", "object-event.yaml"
            ).read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )
    # Read the complete input closure before any mutation.
    anchors = [
        api.structural_evidence_anchor(record_id=key, content=content, media_type=media)
        for key, content, media in (
            (MAPPING_ID, (directory / "mapping.json").read_bytes(), "application/json"),
            (BOUNDARY_ID, boundary_bytes, "application/json"),
            (ADAPTER_ID, Path(__file__).read_bytes(), "text/x-python"),
        )
    ]
    for name, content in sources.items():
        anchors.extend(
            api.structural_source_anchors(
                source_id=boundary["sources"][name]["source_id"],
                artifact_id=f"artifact:connected-shop:synthetic-{name}",
                content=content,
                media_type="application/x-ndjson",
            )
        )
    history = api.KnowledgeChangeHistory.reopen(path)
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=history.partial_contract.normative_profile,
    )
    revision = history.compose_contract_revision(
        revision_id="revision:shop:synthetic-shipments-v1",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=partial.canonical_bytes,
        reason="Add a separate synthetic order and tracked shipments without changing chapter records or admission policy.",
        issued_at=TIME,
    )
    history.record_contract_revision(
        revision=revision, transaction_time=TIME, actor_id=ACTOR
    )
    history.append_anchors(
        anchors=tuple(anchors), transaction_time=TIME, actor_id=ACTOR
    )
    return history


def _profile(replay, profile_id):
    return api.DomainHistoryProfile.from_data(
        json.loads(replay.retained_bytes(f"profile:{profile_id}"))
    )


def plan_for(replay, name, *, source_id=None):
    """Copy the three declared source rows into the connected ontology.

    The optional source ID supports an explicitly retained negative control.
    Neither expected query results nor chapter identities enter this mapper.
    """
    mapping = json.loads(replay.retained_bytes(MAPPING_ID))
    boundary = json.loads(replay.retained_bytes(BOUNDARY_ID))
    step = mapping["steps"][name]
    if source_id is None:
        source_id = boundary["sources"][step["source"]]["source_id"]
    content = replay.retained_bytes(source_id)
    row = json.loads(content.splitlines()[step["row"]])
    entities, relations, derivations = [], [], []

    def derive(record_id, path, field):
        derivations.append(
            {
                "record_id": record_id,
                "path": path,
                "source_id": source_id,
                "locator": f"row:{step['row']}:{field}",
            }
        )

    def entity(record_id, record_type, values):
        entities.append(
            {
                "id": record_id,
                "type": record_type,
                "properties": {key: pair[0] for key, pair in values.items()},
            }
        )
        for key, (_, field) in values.items():
            derive(record_id, ["properties", key], field)

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

    identifier = mapping["identifier_slot"]
    if step["source"] == "order":
        entity(
            row["order_number"],
            mapping["order_type"],
            {identifier: (row["order_number"], "order_number")},
        )
        for ordinal, unit in enumerate(row["unit_ids"]):
            field = f"unit_ids[{ordinal}]"
            entity(
                unit,
                mapping["unit_type"],
                {
                    identifier: (unit, field),
                    mapping["unit_product_slot"]: (row["product_code"], "product_code"),
                },
            )
            relation("contains", row["order_number"], unit, "order_number", field)
    else:
        entity(
            row["shipment_id"],
            mapping["shipment_type"],
            {
                identifier: (row["shipment_id"], "shipment_id"),
                mapping["tracking_slot"]: (row["tracking_id"], "tracking_id"),
            },
        )
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
    profile = _profile(replay, mapping["history_profile_id"])
    return {
        "grammar": mapping["plan_grammar"],
        "adapter": mapping["adapter"],
        "contract_identity": replay.partial_contract.identity,
        "plan_id": f"plan:shop-connected:partial:{name}",
        "history_profile": {
            "profile_id": profile.profile_id,
            "sha256": profile.identity,
        },
        "sources": [{"source_id": source_id, "sha256": base.digest(content)}],
        "evidence": [
            {"evidence_id": key, "sha256": base.digest(replay.retained_bytes(key))}
            for key in (MAPPING_ID, BOUNDARY_ID, ADAPTER_ID)
        ],
        "records": {"entities": entities, "relations": relations},
        "derivations": derivations,
        "supersessions": [],
        "gaps": [],
        "valid_time": mapping["valid_time"],
    }


def prepare(history, plan):
    replay = history.replay()
    profile = _profile(replay, plan["history_profile"]["profile_id"])
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


def admit(history, prepared):
    if prepared.change_set is None:
        raise ValueError("A declared synthetic row produced no change")
    return api.admit_structural_change(
        history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
    )


def append_shipments(path):
    history = start(path)
    mapping = json.loads(history.replay().retained_bytes(MAPPING_ID))
    for name in mapping["step_order"]:
        admit(history, prepare(history, plan_for(history.replay(), name)))
    return api.KnowledgeChangeHistory.reopen(path).replay()


def report(replay):
    """Read each accepted checkpoint and its exact source-field witnesses."""
    mapping = json.loads(replay.retained_bytes(MAPPING_ID))
    boundary = json.loads(replay.retained_bytes(BOUNDARY_ID))
    order_rows = replay.retained_bytes(boundary["sources"]["order"]["source_id"])
    order_id = json.loads(order_rows.splitlines()[0])["order_number"]
    checkpoints, witnesses = {}, {}
    for name in mapping["step_order"]:
        step = mapping["steps"][name]
        content = replay.retained_bytes(
            boundary["sources"][step["source"]]["source_id"]
        )
        record_id = json.loads(content.splitlines()[step["row"]])[step["record_field"]]
        change = api.trace_population_record(replay, record_id).change_set
        checkpoints[step["checkpoint"]] = shipment_view(
            replay.graph_at_change(change.change_set_id), order_id
        )
        for operation in change.operations:
            witnesses[operation.record_id] = [
                {**d, "path": list(d["path"])}
                for d in api.trace_population_record(
                    replay, operation.record_id
                ).derivations
            ]
    return {
        "kind": mapping["kind"],
        "admission": mapping["admission"],
        "duplicate_assignment_rule": mapping["duplicate_assignment_rule"],
        "query_scope": mapping["query_scope"],
        "checkpoints": checkpoints,
        "witnesses": witnesses,
        "limits": boundary["limits"],
    }


def receipt(replay, history_bytes):
    boundary = json.loads(replay.retained_bytes(BOUNDARY_ID))
    prefix = history_bytes[: boundary["baseline_history_bytes"]]
    return {
        "id": boundary["id"],
        "kind": boundary["kind"],
        "baseline_history_sha256": boundary["baseline_history_sha256"],
        "baseline_prefix_preserved": base.digest(prefix)
        == boundary["baseline_history_sha256"],
        "history_sha256": base.digest(history_bytes),
        "history_bytes": len(history_bytes),
        "history_head": replay.ledger_head,
        "replay_receipt": replay.receipt.identity,
        "graph_sha256": replay.graph.state_digest(),
        "contract_identity": replay.partial_contract.identity,
        "contract_revisions": len(replay.contract_revisions),
        "changes": len(replay.change_sets),
        "protocol_events": replay.ledger_event_count,
        "historical_records": len(replay.record_history),
        "sources": {name: spec["sha256"] for name, spec in boundary["sources"].items()},
        "report_sha256": base.digest(base.canonical(report(replay))),
        "checkpoints": report(replay)["checkpoints"],
        "duplicate_assignment_rule": "NOT_SELECTED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--from-empty", action="store_true")
    mode.add_argument("--append", action="store_true")
    mode.add_argument("--reopen", action="store_true")
    args = parser.parse_args()
    if args.reopen:
        result = report(api.KnowledgeChangeHistory.reopen(args.history).replay())
    else:
        if args.from_empty:
            base.run_story(args.history)
            warehouse.append_warehouse(args.history)
        replay = append_shipments(args.history)
        result = receipt(replay, args.history.read_bytes())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
