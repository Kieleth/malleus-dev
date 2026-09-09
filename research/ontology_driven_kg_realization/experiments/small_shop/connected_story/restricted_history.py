"""Fresh Shop compatibility witness for explicitly selected Core transition rules.

Both matching modes are tested; neither selects the final connected Shop policy.
The earlier structural-only producer and its bytes remain unchanged.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story import (
    history_probe as original,
)
from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.source_boundary import (
    load_sources,
)


CORE_COMMIT = "2ef5442efec6e43f2b2623a288933f7c62d46d4e"
CORE_TREE = "d7972839f45508f2a13451f4fd21f80e7db5240e"
TIME = "2026-09-08T00:00:00Z"


def proposed_profile():
    return api.DomainHistoryProfile.from_data(
        json.loads((original.HERE / "proposed_history_profile.json").read_bytes())
    )


def transition_program(*, profile, match):
    """Bind the explicit test choice into the exact installed machine extension."""
    data = json.loads(
        api.STRUCTURAL_HISTORY_BUNDLE.protocol_machine_program.canonical_bytes
    )
    instruction = json.loads(
        (original.HERE / "replacement_instruction.json").read_bytes()
    )
    instruction["match"] = match
    data["grammar"] = "malleus.protocol-machine/private-v1"
    data["admission_rules"] = {
        "history_profile_identity": profile.identity,
        "instructions": [instruction],
    }
    return api.ProtocolMachineProgram.from_bytes(original.canonical(data))


def start_history(path: Path, *, profile, match):
    load_sources(original.HERE)
    history = api.create_structural_history(
        path,
        compilation=original.compile_probe(),
        transition_program=transition_program(profile=profile, match=match),
        transaction_time=TIME,
        actor_id=original.ACTOR,
    )
    history.append_anchors(
        anchors=(
            *api.structural_source_anchors(
                source_id=original.SOURCE_ID,
                artifact_id="artifact:shop-probe:table-1",
                content=(original.HERE / "sources/table-1.jsonl").read_bytes(),
                media_type="application/x-ndjson",
            ),
            api.structural_evidence_anchor(
                record_id="artifact:shop-probe:mapping",
                content=Path(original.__file__).read_bytes(),
                media_type="text/x-python",
            ),
        ),
        transaction_time=TIME,
        actor_id=original.ACTOR,
    )
    return history


def prepare_plan(history, *, profile, plan, transaction_time):
    replay = history.replay()
    compilation = api.compile_population_plan(
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
            history=history, compilation=compilation, profile=profile
        ),
        transaction_time=transaction_time,
        actor_id=original.ACTOR,
    )


def admit_row(history, *, profile, event_id, previous):
    rows, _ = load_sources(original.HERE)
    ordinal, row = next(
        (i, row) for i, row in enumerate(rows) if row["event_id"] == event_id
    )
    plan = original._plan(history.replay(), profile, row, ordinal, previous)
    prepared = prepare_plan(history, profile=profile, plan=plan, transaction_time=TIME)
    if prepared.change_set is None:
        raise ValueError(f"Expected the declared change for {event_id}")
    return api.admit_structural_change(
        history=history,
        preparation=prepared,
        transaction_time=TIME,
        actor_id=original.ACTOR,
    )


def run_probe(path: Path, *, profile, match):
    history = start_history(path, profile=profile, match=match)
    admit_row(history, profile=profile, event_id="e4", previous=None)
    admit_row(history, profile=profile, event_id="e7", previous="state:B:e4")
    return api.KnowledgeChangeHistory.reopen(path).replay()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    parser.add_argument("--match", choices=("EXACT", "SUBTYPE"), required=True)
    args = parser.parse_args()
    replay = run_probe(args.history, profile=proposed_profile(), match=args.match)
    print(
        json.dumps(
            {
                "purpose": "SHOP_COMPATIBILITY_NOT_FINAL_POLICY_SELECTION",
                "tested_core_commit": CORE_COMMIT,
                "tested_core_tree": CORE_TREE,
                "match": args.match,
                "history_sha256": original.digest(args.history.read_bytes()),
                "ledger_head": replay.ledger_head,
                "ledger_event_count": replay.ledger_event_count,
                "replay_receipt": replay.receipt.identity,
                "change_count": len(replay.change_sets),
                "record_history_count": len(replay.record_history),
                "graph": replay.graph.export_records(),
            },
            sort_keys=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
