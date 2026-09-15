"""Append the chapter's warehouse observations to the exact connected Shop history."""

from __future__ import annotations

import argparse
from importlib.resources import files
import json
from pathlib import Path

from malleus import bundled_ontology_path
import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    object_timelines,
    run as base,
)
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.source_boundary import (
    inspect_sources,
)


HERE = Path(__file__).resolve().parent
SOURCE_ID = "source:connected-shop:figure-14"
MAPPING_ID = "artifact:connected-shop:warehouse-mapping"
BOUNDARY_ID = "artifact:connected-shop:warehouse-boundary"
ADAPTER_ID = "artifact:connected-shop:warehouse-adapter"
IMAGE_ID = "artifact:connected-shop:figure-14-image"
TIME = "2026-09-14T00:00:00Z"  # Fixed fixture import time, not domain time.
ACTOR = "actor:connected-shop-import"


def load_source(directory=HERE):
    boundary = json.loads((directory / "source_boundary.json").read_bytes())
    for relative, expected in boundary["artifacts"].items():
        if base.digest((directory / relative).read_bytes()) != expected:
            raise ValueError(f"Warehouse source digest differs: {relative}")
    rows = list(
        map(
            json.loads,
            (directory / "sources/figure-14.jsonl").read_bytes().splitlines(),
        )
    )
    inspect_sources(rows, boundary)
    return rows, boundary


def compile_target():
    return api.compile_linkml_contract(
        root_locator="shop",
        sources={
            "shop": (HERE / "shop.yaml").read_bytes(),
            "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
            "object-event": bundled_ontology_path(
                "profiles", "object-event.yaml"
            ).read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )


def build_plan(replay, row, ordinal):
    """Map only the four supplied columns, requiring an already known unit."""
    if set(row) != {"event_id", "activity", "time_text", "item_ids"}:
        raise ValueError("Warehouse rows require exactly the four source fields")
    mapping = json.loads(replay.retained_bytes(MAPPING_ID))
    if len(row["item_ids"]) != 1:
        raise ValueError("One existing InventoryUnit is required per warehouse row")
    item_id = f"{mapping['item_prefix']}:{row['item_ids'][0]}"
    item = replay.graph.get_node(item_id)
    if item is None or item["type"] != mapping["item_type"]:
        raise ValueError(f"An existing InventoryUnit is required: {item_id}")
    event_id = row["event_id"]
    records = {
        "entities": [],
        "relations": [],
        "events": [],
        "event_participations": [],
    }
    derivations = []
    for family, identifier, record_type, values in (
        (
            "events",
            event_id,
            mapping["event_type"],
            {
                "source_identifier": (event_id, "event_id"),
                "time_text": (row["time_text"], "time_text"),
                "event_type": (mapping["activities"][row["activity"]], "activity"),
            },
        ),
        (
            "event_participations",
            f"participation:{event_id}:{item_id}",
            mapping["participation_type"],
            {
                "event_id": (event_id, "event_id"),
                "entity_id": (item_id, "item_ids[0]"),
                "qualifier": (mapping["participation_role"], "item_ids[0]"),
            },
        ),
    ):
        records[family].append(
            {
                "id": identifier,
                "type": record_type,
                "properties": {key: pair[0] for key, pair in values.items()},
            }
        )
        derivations.extend(
            {
                "record_id": identifier,
                "path": ["properties", key],
                "source_id": SOURCE_ID,
                "locator": f"row:{ordinal}:{pair[1]}",
            }
            for key, pair in values.items()
        )
    profile = api.DomainHistoryProfile.from_data(
        json.loads(replay.retained_bytes(f"profile:{mapping['history_profile_id']}"))
    )
    return {
        "grammar": "malleus.population-plan/private-v0",
        "adapter": mapping["adapter"],
        "contract_identity": replay.partial_contract.identity,
        "plan_id": f"plan:shop-warehouse:{event_id}",
        "history_profile": {
            "profile_id": profile.profile_id,
            "sha256": profile.identity,
        },
        "sources": [
            {
                "source_id": SOURCE_ID,
                "sha256": base.digest(replay.retained_bytes(SOURCE_ID)),
            }
        ],
        "evidence": [
            {"evidence_id": key, "sha256": base.digest(replay.retained_bytes(key))}
            for key in (MAPPING_ID, BOUNDARY_ID, ADAPTER_ID, IMAGE_ID)
        ],
        "records": records,
        "derivations": derivations,
        "supersessions": [],
        "gaps": [],
        "valid_time": mapping["valid_time"],
    }


def append_warehouse(path):
    """Extend only the frozen prefix; each admission is atomic, not the whole run."""
    rows, boundary = load_source()
    path = Path(path)
    if base.digest(path.read_bytes()) != boundary["baseline_history_sha256"]:
        raise ValueError("Warehouse extension requires the exact Table 1 baseline")
    history = api.KnowledgeChangeHistory.reopen(path)
    target = compile_target()
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=history.partial_contract.normative_profile,
    )
    revision = history.compose_contract_revision(
        revision_id="revision:shop:warehouse-v1",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=partial.canonical_bytes,
        reason="Add Figure 14 Scan, Store and Retrieve without changing prior Shop declarations.",
        issued_at=TIME,
    )
    history.record_contract_revision(
        revision=revision, transaction_time=TIME, actor_id=ACTOR
    )
    history.append_anchors(
        anchors=(
            *api.structural_source_anchors(
                source_id=SOURCE_ID,
                artifact_id="artifact:connected-shop:figure-14",
                content=(HERE / "sources/figure-14.jsonl").read_bytes(),
                media_type="application/x-ndjson",
            ),
            *(
                api.structural_evidence_anchor(
                    record_id=key, content=file.read_bytes(), media_type=media
                )
                for key, file, media in (
                    (MAPPING_ID, HERE / "mapping.json", "application/json"),
                    (BOUNDARY_ID, HERE / "source_boundary.json", "application/json"),
                    (ADAPTER_ID, Path(__file__), "text/x-python"),
                    (IMAGE_ID, HERE / "sources/figure-14.png", "image/png"),
                )
            ),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    for ordinal, row in enumerate(rows):
        replay = history.replay()
        plan = build_plan(replay, row, ordinal)
        profile = api.DomainHistoryProfile.from_data(
            json.loads(
                replay.retained_bytes(
                    f"profile:{plan['history_profile']['profile_id']}"
                )
            )
        )
        compiled = api.compile_population_plan(
            plan,
            partial_contract=replay.partial_contract,
            contract_view=replay.contract_view,
            base_state=api.PopulationBaseState.from_replay(replay),
            history_profile=profile,
        )
        prepared = api.prepare_population_change(
            history=history,
            plan=plan,
            profile=profile,
            retention_events=api.population_retention_events(
                history=history, compilation=compiled, profile=profile
            ),
            transaction_time=TIME,
            actor_id=ACTOR,
        )
        if prepared.change_set is None:
            raise ValueError(
                f"Warehouse occurrence produced no change: {row['event_id']}"
            )
        api.admit_structural_change(
            history=history, preparation=prepared, transaction_time=TIME, actor_id=ACTOR
        )
    return api.KnowledgeChangeHistory.reopen(path).replay()


def read_warehouse(replay):
    """Reuse the object display, with a separate two-source report boundary."""
    boundary = json.loads(replay.retained_bytes(BOUNDARY_ID))
    source = replay.retained_bytes(SOURCE_ID)
    if base.digest(source) != boundary["artifacts"]["sources/figure-14.jsonl"]:
        raise ValueError("Warehouse read requires the retained Figure 14 bytes")
    mapping = json.loads(replay.retained_bytes(base.MAPPING_ID))
    result = object_timelines.inspect_object_views(replay.graph, mapping)
    for row in map(json.loads, source.splitlines()):
        event_id = row["event_id"]
        event = result["events"][event_id]
        event["witnesses"] = [
            {**d, "path": list(d["path"])}
            for d in api.trace_population_record(replay, event_id).derivations
        ]
    spec_bytes = (base.HERE / "timeline_read_spec.json").read_bytes()
    result.update(
        {
            "interpretation": json.loads(spec_bytes)["interpretation"],
            "limits": boundary["limits"] + json.loads(spec_bytes)["limits"],
            "history_head": replay.ledger_head,
            "history_receipt": replay.receipt.identity,
            "source_sha256": base.digest(source),
            "display_spec_sha256": base.digest(spec_bytes),
            "display_implementation_sha256": base.digest(
                Path(object_timelines.__file__).read_bytes()
            ),
        }
    )
    return result


def receipt(replay, history_bytes, prefix):
    return {
        "id": "shop-warehouse-extension-v1",
        "baseline_history_sha256": base.digest(prefix),
        "baseline_prefix_preserved": history_bytes.startswith(prefix),
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
        "warehouse_source_sha256": base.digest(replay.retained_bytes(SOURCE_ID)),
        "report_sha256": base.digest(base.canonical(read_warehouse(replay))),
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
        print(
            json.dumps(
                read_warehouse(
                    api.KnowledgeChangeHistory.reopen(args.history).replay()
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return
    if args.from_empty:
        base.run_story(args.history)
    prefix = args.history.read_bytes()
    replay = append_warehouse(args.history)
    print(
        json.dumps(
            receipt(replay, args.history.read_bytes(), prefix), indent=2, sort_keys=True
        )
    )


if __name__ == "__main__":
    main()
