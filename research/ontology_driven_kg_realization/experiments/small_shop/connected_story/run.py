"""Source-produced connected Shop history through public Malleus APIs only."""

from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

from malleus import bundled_ontology_path
import malleus.compiler as api
from malleus.inquisition.pack_grounding import validate_pack_grounding

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.source_boundary import (
    inspect_sources,
    load_sources,
)


HERE = Path(__file__).resolve().parent
SOURCE_ID = "source:connected-shop:table-1"
MAPPING_ID = "artifact:connected-shop:mapping"
ACTOR = "actor:connected-shop-import"
TIME = "2026-09-08T00:00:00Z"  # Fixed fixture import coordinate, not domain time.


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


def compile_shop():
    source = (HERE / "shop.yaml").read_bytes()
    validate_pack_grounding(source, role="PROJECT")
    return api.compile_linkml_contract(
        root_locator="shop",
        sources={
            "shop": source,
            "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
            "object-event": bundled_ontology_path(
                "profiles", "object-event.yaml"
            ).read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )


def history_configuration():
    profile = api.DomainHistoryProfile.from_data(
        json.loads((HERE / "history_profile.json").read_bytes())
    )
    machine = json.loads(
        api.STRUCTURAL_HISTORY_BUNDLE.protocol_machine_program.canonical_bytes
    )
    machine["grammar"] = "malleus.protocol-machine/private-v1"
    machine["admission_rules"] = {
        "history_profile_identity": profile.identity,
        "instructions": [
            json.loads((HERE / "transition_instruction.json").read_bytes())
        ],
    }
    return profile, api.ProtocolMachineProgram.from_bytes(canonical(machine))


def parse_quantities(text):
    """The retained transcription uses positive decimal quantity · product pairs."""
    pairs = []
    for token in text.split(","):
        quantity, separator, product = token.strip().partition("·")
        if (
            not separator
            or not quantity.isascii()
            or not quantity.isdecimal()
            or int(quantity) <= 0
            or not product
            or any(c.isspace() for c in product)
            or "·" in product
        ):
            raise ValueError(f"Invalid explicit quantity: {text!r}")
        pairs.append((product, int(quantity)))
    if len({product for product, _ in pairs}) != len(pairs):
        raise ValueError(f"Repeated product in quantity declaration: {text!r}")
    return pairs


def build_plan(replay, profile, row, ordinal, boundary):
    """Interpret one verified source row. No independent expected answers are read."""
    mapping = json.loads(replay.retained_bytes(MAPPING_ID))
    activity = mapping["activities"][row["activity"]]
    event_id = row["event_id"]
    records = {
        "entities": [],
        "relations": [],
        "events": [],
        "event_participations": [],
    }
    derivations, supersessions = [], []

    def record(family, record_id, record_type, properties, fields):
        if set(properties) != set(fields):
            raise ValueError(f"Every field requires a source derivation: {record_id}")
        records[family].append(
            {"id": record_id, "type": record_type, "properties": properties}
        )
        derivations.extend(
            {
                "record_id": record_id,
                "path": ["properties", field],
                "source_id": SOURCE_ID,
                "locator": f"row:{ordinal}:{source_field}",
            }
            for field, source_field in fields.items()
        )

    record(
        "events",
        event_id,
        "ShopOccurrence",
        {
            "source_identifier": event_id,
            "event_type": activity["event_type"],
            "time_text": row["time_text"],
        },
        {
            "source_identifier": "event_id",
            "event_type": "activity",
            "time_text": "time_text",
        },
    )
    for field, binding in mapping["object_columns"].items():
        if field not in row:  # Blank optional source columns are absent, not defaults.
            continue
        for index, source_identifier in enumerate(row[field]):
            object_id = f"{binding['prefix']}:{source_identifier}"
            locator = f"{field}[{index}]"
            if object_id not in replay.record_history:
                record(
                    "entities",
                    object_id,
                    binding["type"],
                    {"source_identifier": source_identifier},
                    {"source_identifier": locator},
                )
            record(
                "event_participations",
                f"participation:{event_id}:{object_id}",
                "ShopParticipation",
                {
                    "event_id": event_id,
                    "entity_id": object_id,
                    "qualifier": binding["qualifier"],
                },
                {"event_id": "event_id", "entity_id": locator, "qualifier": locator},
            )

    quantity = activity["quantity"]
    if quantity is not None:
        owner_field = quantity["owner_field"]
        if len(row[owner_field]) != 1:
            raise ValueError(f"Quantity needs exactly one owner: {event_id}")
        owner = (
            f"{mapping['object_columns'][owner_field]['prefix']}:{row[owner_field][0]}"
        )
        for product, value in parse_quantities(row["order_details_text"]):
            prior = replay.graph.query(
                quantity["state_type"], order_id=owner, product_code=product
            )
            mode = quantity["mode"]
            if mode not in ("INITIAL", "REPLACE"):
                raise ValueError(f"Unknown quantity mode: {mode}")
            if (mode == "INITIAL" and prior) or (mode == "REPLACE" and len(prior) != 1):
                raise ValueError(
                    f"Quantity predecessor is missing or ambiguous: {event_id}/{owner}/{product}"
                )
            state_id = f"state:{owner}:{product}:{event_id}"
            record(
                "entities",
                state_id,
                quantity["state_type"],
                {
                    "order_id": owner,
                    "product_code": product,
                    "ordered_quantity": value,
                    "source_occurrence_id": event_id,
                },
                {
                    "order_id": f"{owner_field}[0]",
                    "product_code": "order_details_text",
                    "ordered_quantity": "order_details_text",
                    "source_occurrence_id": "event_id",
                },
            )
            if mode == "REPLACE":
                supersessions.append(
                    {"record_id": state_id, "supersedes_record_id": prior[0]["id"]}
                )
    elif "order_details_text" in row:
        raise ValueError(f"Unmapped quantity source at {event_id}")

    gaps = [
        {
            "kind": gap["kind"],
            "statement": gap["detail"],
            "source_id": SOURCE_ID,
            "locator": f"row:{ordinal}:"
            + (
                "time_text" if gap["kind"] == "INTERVAL_NOT_EXPRESSIBLE" else "activity"
            ),
        }
        for gap in boundary["known_gaps"]
        if gap["event_id"] == event_id
    ]
    return {
        "grammar": "malleus.population-plan/private-v0",
        "adapter": mapping["adapter"],
        "contract_identity": replay.partial_contract.identity,
        "plan_id": f"plan:shop-connected:{event_id}",
        "history_profile": {
            "profile_id": profile.profile_id,
            "sha256": profile.identity,
        },
        "sources": [
            {"source_id": SOURCE_ID, "sha256": digest(replay.retained_bytes(SOURCE_ID))}
        ],
        "evidence": [
            {
                "evidence_id": evidence_id,
                "sha256": digest(replay.retained_bytes(evidence_id)),
            }
            for evidence_id in (
                MAPPING_ID,
                "artifact:connected-shop:adapter",
                "artifact:connected-shop:source-boundary",
            )
        ],
        "records": records,
        "derivations": derivations,
        "gaps": gaps,
        "supersessions": supersessions,
        "valid_time": mapping["valid_time"],
    }


def prepare(history, plan):
    replay = history.replay()
    profile = api.DomainHistoryProfile.from_data(
        json.loads(
            replay.retained_bytes(f"profile:{plan['history_profile']['profile_id']}")
        )
    )
    return _prepare(history, plan, profile)


def _prepare(history, plan, profile):
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


def run_story(path):
    rows, boundary = load_sources(HERE)
    inspect_sources(rows, boundary)
    profile, program = history_configuration()
    history = api.create_structural_history(
        path,
        compilation=compile_shop(),
        transition_program=program,
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    history.append_anchors(
        anchors=(
            *api.structural_source_anchors(
                source_id=SOURCE_ID,
                artifact_id="artifact:connected-shop:table-1",
                content=(HERE / "sources/table-1.jsonl").read_bytes(),
                media_type="application/x-ndjson",
            ),
            *api.structural_source_anchors(
                source_id="source:connected-shop:context",
                artifact_id="artifact:connected-shop:context",
                content=(HERE / "sources/context.jsonl").read_bytes(),
                media_type="application/x-ndjson",
            ),
            *(
                api.structural_evidence_anchor(
                    record_id=record_id, content=file.read_bytes(), media_type=media
                )
                for record_id, file, media in (
                    (MAPPING_ID, HERE / "mapping.json", "application/json"),
                    (
                        "artifact:connected-shop:adapter",
                        Path(__file__),
                        "text/x-python",
                    ),
                    (
                        "artifact:connected-shop:source-boundary",
                        HERE / "source_boundary.json",
                        "application/json",
                    ),
                    (
                        "artifact:connected-shop:table-image",
                        HERE / "sources/table-1.png",
                        "image/png",
                    ),
                )
            ),
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    for ordinal, row in enumerate(rows):
        plan = build_plan(history.replay(), profile, row, ordinal, boundary)
        prepared = _prepare(history, plan, profile)
        if prepared.change_set is None:
            raise ValueError(
                f"Source occurrence unexpectedly produced no change: {row['event_id']}"
            )
        api.admit_structural_change(
            history=history,
            preparation=prepared,
            transaction_time=TIME,
            actor_id=ACTOR,
        )
    return api.KnowledgeChangeHistory.reopen(path).replay()


def explain(replay):
    """Read declared occurrence joins. Do not turn co-participation into causality."""
    mapping = json.loads(replay.retained_bytes(MAPPING_ID))
    graph = replay.graph

    def members(event_id, field):
        return sorted(
            graph.get_node(item["entity_id"])["source_identifier"]
            for item in graph.query_event_participations(
                event_id=event_id,
                qualifier=mapping["object_columns"][field]["qualifier"],
            )
        )

    account = {}
    witnesses = {}
    for name, view in mapping["views"].items():
        grouped, observed = {}, {}
        for event in graph.query(
            "ShopOccurrence",
            event_type=mapping["activities"][view["activity"]]["event_type"],
        ):
            targets = members(event["id"], view["to"])
            for owner in members(event["id"], view["from"]):
                grouped.setdefault(owner, set()).update(targets)
                observed.setdefault(owner, []).append(event["id"])
        account[name] = {key: sorted(value) for key, value in sorted(grouped.items())}
        witnesses[name] = {
            key: sorted(value) for key, value in sorted(observed.items())
        }
    account["packing_witnesses"] = witnesses["packed_units"]
    account["view_witnesses"] = witnesses
    account["invoice_updates"] = [
        {"event_id": event["id"], "invoices": members(event["id"], "invoice_ids")}
        for event in graph.query(
            "ShopOccurrence",
            event_type=mapping["activities"]["Update Invoice"]["event_type"],
        )
    ]
    account["source_gaps"] = [
        gap
        for event in graph.query("ShopOccurrence")
        for gap in json.loads(
            replay.retained_bytes(f"plan:shop-connected:{event['id']}")
        )["gaps"]
    ]
    account["shipment_eligibility"] = "NOT_EVALUATED"
    account["temporal_claim"] = (
        "PRINTED_TIME_RETAINED_NO_CALENDAR_OR_DOMAIN_ORDER_INFERRED"
    )
    return account


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    parser.add_argument(
        "--reopen",
        action="store_true",
        help="Read an existing retained history without writing it.",
    )
    args = parser.parse_args()
    replay = (
        api.KnowledgeChangeHistory.reopen(args.history).replay()
        if args.reopen
        else run_story(args.history)
    )
    print(
        json.dumps(
            {
                "ledger_head": replay.ledger_head,
                "ledger_events": replay.ledger_event_count,
                "history_sha256": digest(args.history.read_bytes()),
                "receipt": replay.receipt.identity,
                "changes": len(replay.change_sets),
                "historical_records": len(replay.record_history),
                "graph": replay.graph.export_records(),
                "account": explain(replay),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
