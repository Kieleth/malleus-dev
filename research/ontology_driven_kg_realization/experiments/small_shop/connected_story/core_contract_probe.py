"""Reproduce the remaining profile-policy question through public Core APIs."""

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import malleus.compiler as api

from research.ontology_driven_kg_realization.experiments.small_shop.connected_story.history_probe import (
    ACTOR,
    HERE,
    run_probe,
)


def probe_event_replacement(path: Path):
    """Can a state-only replacement declaration prevent Event replacement?"""
    replay = run_probe(path)
    history = api.KnowledgeChangeHistory.reopen(path)
    profile = api.DomainHistoryProfile.from_data(
        json.loads((HERE / "proposed_history_profile.json").read_bytes())
    )
    plan = json.loads(replay.retained_bytes("plan:shop-probe:e7"))
    replacements = {
        "e7": "e7:replacement-probe",
        "participation:e7:B": "participation:e7:replacement-probe:B",
    }
    plan["plan_id"] = "plan:shop-probe:replace-event"
    plan["records"]["entities"] = []
    for family in ("events", "event_participations"):
        for record in plan["records"][family]:
            record["id"] = replacements[record["id"]]
    plan["records"]["event_participations"][0]["properties"]["event_id"] = replacements[
        "e7"
    ]
    plan["derivations"] = [
        dict(deepcopy(item), record_id=replacements[item["record_id"]])
        for item in plan["derivations"]
        if item["record_id"] in replacements
    ]
    plan["supersessions"] = [
        {"record_id": new, "supersedes_record_id": old}
        for old, new in replacements.items()
    ]
    before = path.read_bytes()
    try:
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
            transaction_time="2026-09-08T00:03:00Z",
            actor_id=ACTOR,
        )
        result = api.admit_structural_change(
            history=history,
            preparation=prepared,
            transaction_time="2026-09-08T00:03:00Z",
            actor_id=ACTOR,
        )
    except (api.PopulationPlanRefusal, api.KnowledgeChangeRefusal) as error:
        return {
            "outcome": "REFUSED",
            "detail": str(error),
            "history_unchanged": path.read_bytes() == before,
        }
    return {
        "outcome": "ADMITTED",
        "profile_correction": profile.change_semantics["correction"],
        "declared_state_types": list(profile.ontology_roles["state"]),
        "old_event_superseded_by": result.record_history["e7"].superseded_by,
        "old_event_still_retained": "e7" in result.record_history,
        "current_event_ids": [
            row["id"] for row in result.graph.query("SupplierOrderOccurrence")
        ],
        "non_claim": "Profile labels are not assumed to be executable rules. This asks Core where an adopter must enforce the intended restriction.",
    }


if __name__ == "__main__":
    with TemporaryDirectory(prefix="shop-profile-contract-") as directory:
        print(
            json.dumps(
                probe_event_replacement(Path(directory) / "history.jsonl"),
                indent=2,
                sort_keys=True,
            )
        )
