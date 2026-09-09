"""Public-only Shop model probe. Not approval of the proposed history semantics."""

from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

from malleus import bundled_ontology_path
import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.source_boundary import (
    load_sources,
)


HERE = Path(__file__).resolve().parent
SHOP_SCHEMA = (
    HERE.parents[2]
    / "fixtures/small_shop_fulfilment_full_public_v1/input/tbox/small-shop.yaml"
)
SOURCE_ID = "source:connected-shop:table-1"
ACTOR = "actor:shop-history-probe"


def canonical(value):
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()


def digest(value):
    return "sha256:" + sha256(value).hexdigest()


def compile_probe():
    return api.compile_linkml_contract(
        root_locator="probe",
        sources={
            "probe": (HERE / "probe.yaml").read_bytes(),
            "small-shop": SHOP_SCHEMA.read_bytes(),
            "object-event": bundled_ontology_path(
                "profiles", "object-event.yaml"
            ).read_bytes(),
            "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )


def _plan(replay, profile, row, ordinal, previous):
    event_id = row["event_id"]
    quantity, separator, product = row["order_details_text"].partition("·")
    if (
        not separator
        or not quantity.isdecimal()
        or product != "Y"
        or row["supplier_order_ids"] != ["B"]
    ):
        raise ValueError("This bounded probe accepts only the declared B/Y rows")
    activity = {"Place SO": "PLACE_SO", "Update SO": "UPDATE_SO"}[row["activity"]]
    state_id = f"state:B:{event_id}"
    records = {
        "entities": [],
        "relations": [],
        "events": [],
        "event_participations": [],
    }
    derivations = []

    def record(family, record_id, record_type, properties, field_sources):
        if set(properties) != set(field_sources):
            raise ValueError(f"Every proposed field needs a derivation: {record_id}")
        records[family].append(
            {"id": record_id, "type": record_type, "properties": properties}
        )
        for field, source_field in field_sources.items():
            derivations.append(
                {
                    "record_id": record_id,
                    "path": ["properties", field],
                    "source_id": SOURCE_ID,
                    "locator": f"row:{ordinal}:{source_field}",
                }
            )

    if previous is None:
        record(
            "entities",
            "supplier-order:B",
            "SupplierOrder",
            {"supplier_order_id": "B"},
            {"supplier_order_id": "supplier_order_ids[0]"},
        )
    record(
        "entities",
        state_id,
        "SupplierOrderState",
        {
            "supplier_order_id": "B",
            "product_code": product,
            "ordered_quantity": int(quantity),
            "source_occurrence_id": event_id,
        },
        {
            "supplier_order_id": "supplier_order_ids[0]",
            "product_code": "order_details_text",
            "ordered_quantity": "order_details_text",
            "source_occurrence_id": "event_id",
        },
    )
    record(
        "events",
        event_id,
        "SupplierOrderOccurrence",
        {"event_type": activity, "time_text": row["time_text"]},
        {"event_type": "activity", "time_text": "time_text"},
    )
    record(
        "event_participations",
        f"participation:{event_id}:B",
        "SupplierOrderParticipation",
        {
            "entity_id": "supplier-order:B",
            "event_id": event_id,
            "qualifier": "SUPPLIER_ORDER",
        },
        {
            "entity_id": "supplier_order_ids[0]",
            "event_id": "event_id",
            "qualifier": "supplier_order_ids[0]",
        },
    )
    return {
        "grammar": "malleus.population-plan/private-v0",
        "adapter": {"adapter_id": "shop-history-probe", "version": "1"},
        "contract_identity": replay.partial_contract.identity,
        "plan_id": f"plan:shop-probe:{event_id}",
        "history_profile": {
            "profile_id": profile.profile_id,
            "sha256": profile.identity,
        },
        "sources": [
            {"source_id": SOURCE_ID, "sha256": digest(replay.retained_bytes(SOURCE_ID))}
        ],
        "evidence": [
            {
                "evidence_id": "artifact:shop-probe:mapping",
                "sha256": digest(replay.retained_bytes("artifact:shop-probe:mapping")),
            }
        ],
        "records": records,
        "derivations": derivations,
        "gaps": [],
        "supersessions": []
        if previous is None
        else [{"record_id": state_id, "supersedes_record_id": previous}],
        "valid_time": {"kind": "NONE_STATED", "value": None},
    }


def run_probe(path: Path, *, profile=None):
    rows, _ = load_sources(HERE)
    selected = (
        api.DomainHistoryProfile.from_data(
            json.loads((HERE / "proposed_history_profile.json").read_bytes())
        )
        if profile is None
        else profile
    )
    compiled = compile_probe()
    history = api.create_structural_history(
        path,
        compilation=compiled,
        transaction_time="2026-09-08T00:00:00Z",
        actor_id=ACTOR,
    )
    history.append_anchors(
        anchors=(
            *api.structural_source_anchors(
                source_id=SOURCE_ID,
                artifact_id="artifact:shop-probe:table-1",
                content=(HERE / "sources/table-1.jsonl").read_bytes(),
                media_type="application/x-ndjson",
            ),
            api.structural_evidence_anchor(
                record_id="artifact:shop-probe:mapping",
                content=Path(__file__).read_bytes(),
                media_type="text/x-python",
            ),
        ),
        transaction_time="2026-09-08T00:00:00Z",
        actor_id=ACTOR,
    )
    previous = None
    for minute, event_id in enumerate(("e4", "e7"), 1):
        ordinal, row = next(
            (i, row) for i, row in enumerate(rows) if row["event_id"] == event_id
        )
        replay = history.replay()
        plan = _plan(replay, selected, row, ordinal, previous)
        time = f"2026-09-08T00:0{minute}:00Z"
        compilation = api.compile_population_plan(
            plan,
            partial_contract=replay.partial_contract,
            contract_view=replay.contract_view,
            base_state=api.PopulationBaseState.from_replay(replay),
            history_profile=selected,
        )
        prepared = api.prepare_population_change(
            history=history,
            plan=plan,
            profile=selected,
            retention_events=api.population_retention_events(
                history=history, compilation=compilation, profile=selected
            ),
            transaction_time=time,
            actor_id=ACTOR,
        )
        if prepared.change_set is None:
            raise ValueError(f"Expected the declared change for {event_id}")
        api.admit_structural_change(
            history=history, preparation=prepared, transaction_time=time, actor_id=ACTOR
        )
        previous = f"state:B:{event_id}"
    return api.KnowledgeChangeHistory.reopen(path).replay()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    args = parser.parse_args()
    replay = run_probe(args.history)
    print(
        json.dumps(
            {
                "ledger_head": replay.ledger_head,
                "ledger_event_count": replay.ledger_event_count,
                "change_count": len(replay.change_sets),
                "graph": replay.graph.export_records(),
            },
            sort_keys=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
