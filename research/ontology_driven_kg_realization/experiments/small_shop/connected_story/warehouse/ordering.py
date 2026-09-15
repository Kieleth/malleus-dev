"""Read bounded pairwise ordering without writing queue edges or repairing time."""

from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path

import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    object_timelines,
    run as base,
)
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.warehouse import (
    run,
)


def _order(left, right, events):
    if left == right:
        return "TIED"
    result = object_timelines.order_printed_events(
        [{"id": key, "time_text": events[key]["time_text"]} for key in (left, right)]
    )
    if result["unplaced_events"]:
        return "UNPLACED"
    if len(result["printed_sequence"]) == 1:
        return "TIED"
    return "BEFORE" if result["printed_sequence"][0] == [left] else "AFTER"


def inspect_ordering(view, spec):
    """Inspect the declared cohort. Hypothetical views carry no history receipt."""
    units = sorted(spec["units"])
    if len(units) < 2 or len(set(units)) != len(units):
        raise ValueError("Comparison requires at least two unique unit IDs")
    events = view["events"]
    observations, queues = {}, {}
    for queue in spec["queues"]:
        name = queue["entry"] + ":" + queue["exit"]
        if queue["entry"] == queue["exit"] or name in queues:
            raise ValueError("Comparison stages must differ and queue names be unique")
        routes = {}
        for unit in units:
            route = {"entry": [], "exit": [], "issues": []}
            routes[unit] = route
            if unit not in view["objects"]:
                route["issues"].append({"unit": unit, "reason": "MISSING_UNIT"})
                continue
            lane = view["objects"][unit]
            if lane["type"] != spec["unit_type"]:
                raise ValueError(f"Expected {spec['unit_type']} for {unit}")
            for identifier in sorted(lane["event_ids"]):
                event = events[identifier]
                for stage in ("entry", "exit"):
                    if event["event_type"] != queue[stage]:
                        continue
                    role = spec["participation_role"]
                    if (
                        role not in event["participants"]
                        or unit not in event["participants"][role]
                    ):
                        raise ValueError(
                            f"Inconsistent participation: {identifier}, {unit}"
                        )
                    route[stage].append(identifier)
                    observations[identifier] = {
                        "event_type": event["event_type"],
                        "time_text": event["time_text"],
                        "units": sorted(event["participants"][role]),
                    }
            for stage in ("entry", "exit"):
                selected = route[stage]
                reason = None
                if not selected:
                    reason = "MISSING_OBSERVATION"
                elif len(selected) > 1:
                    reason = "REPEATED_ACTIVITY"
                elif object_timelines.order_printed_events(
                    [{"id": selected[0], "time_text": events[selected[0]]["time_text"]}]
                )["unplaced_events"]:
                    reason = "UNPLACED_TIME"
                if reason:
                    route["issues"].append(
                        {"unit": unit, "stage": stage, "reason": reason}
                    )
            if (
                not route["issues"]
                and _order(route["entry"][0], route["exit"][0], events) != "BEFORE"
            ):
                route["issues"].append(
                    {"unit": unit, "reason": "NON_FORWARD_STAGE_PAIR"}
                )
        pairs = []
        counts = {"PRESERVED": 0, "REVERSED": 0, "UNDETERMINED": 0}
        for left, right in combinations(units, 2):
            issues = [*routes[left]["issues"], *routes[right]["issues"]]
            pair = {
                "units": [left, right],
                "entry_order": None,
                "exit_order": None,
                "issues": issues,
            }
            if not issues:
                for stage in ("entry", "exit"):
                    order = _order(
                        routes[left][stage][0], routes[right][stage][0], events
                    )
                    pair[stage + "_order"] = order
                    if order == "TIED":
                        issues.append({"stage": stage, "reason": "TIED_PRINTED_TIMES"})
            pair["outcome"] = (
                "UNDETERMINED"
                if issues
                else "PRESERVED"
                if pair["entry_order"] == pair["exit_order"]
                else "REVERSED"
            )
            counts[pair["outcome"]] += 1
            pairs.append(pair)
        queues[name] = {
            "routes": routes,
            "pairs": pairs,
            "counts": counts,
            "coverage": "PARTIAL"
            if counts["UNDETERMINED"]
            else "ALL_DECLARED_PAIRS_COMPARABLE",
            "conclusion": (
                "OBSERVED_REVERSAL"
                if counts["REVERSED"]
                else "NO_REVERSAL_IN_COMPARABLE_PAIRS"
                if counts["PRESERVED"]
                else "NO_COMPARABLE_PAIRS"
            ),
        }
    return {
        "scope": "SELECTED_RECORDED_OBSERVATIONS",
        "units": units,
        "queues": queues,
        "observations": dict(sorted(observations.items())),
        "not_claimed": ["FULL_FIFO", "ELAPSED_TIME", "CAUSALITY"],
    }


def read_ordering(replay):
    """Bind this Shop comparison to the replay and both exact retained sources."""
    spec_bytes = (run.HERE / "ordering_spec.json").read_bytes()
    spec = json.loads(spec_bytes)
    time_spec_bytes = (base.HERE / "timeline_read_spec.json").read_bytes()
    time_spec = json.loads(time_spec_bytes)
    if base.digest(replay.retained_bytes(base.SOURCE_ID)) != time_spec["source_sha256"]:
        raise ValueError("Ordering comparison requires the exact retained Table 1")
    result = inspect_ordering(run.read_warehouse(replay), spec)
    for identifier, observation in result["observations"].items():
        links = replay.graph.query_event_participations(
            event_id=identifier, qualifier=spec["participation_role"]
        )
        observation["witnesses"] = [
            {**derivation, "path": list(derivation["path"])}
            for record_id in [identifier, *sorted(link["id"] for link in links)]
            for derivation in api.trace_population_record(replay, record_id).derivations
        ]
    result["binding"] = {
        "history_head": replay.ledger_head,
        "event_count": replay.ledger_event_count,
        "replay_receipt": replay.receipt.identity,
        "graph_sha256": replay.graph.state_digest(),
        "sources": {
            key: base.digest(replay.retained_bytes(key))
            for key in (base.SOURCE_ID, run.SOURCE_ID)
        },
        "spec_sha256": base.digest(spec_bytes),
        "implementation_sha256": base.digest(Path(__file__).read_bytes()),
        "time_spec_sha256": base.digest(time_spec_bytes),
        "object_reader_sha256": base.digest(
            Path(object_timelines.__file__).read_bytes()
        ),
        "warehouse_reader_sha256": base.digest(Path(run.__file__).read_bytes()),
    }
    return result


def receipt(report):
    return {
        "id": "shop-warehouse-ordering-v1",
        "binding": report["binding"],
        "report_sha256": base.digest(base.canonical(report)),
        "counts": {key: queue["counts"] for key, queue in report["queues"].items()},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    args = parser.parse_args()
    report = read_ordering(api.KnowledgeChangeHistory.reopen(args.history).replay())
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
