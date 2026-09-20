"""Synthetic API diagnostic, not an astronomy schema or producer fixture."""

from hashlib import sha256
from importlib.resources import files
import json

import pytest

from malleus import bundled_ontology_path
from malleus import compiler as api


SCHEMA = b"""\
id: https://example.org/history-feasibility
name: history_feasibility
default_range: string
imports: [linkml:types, malleus]
classes:
  SourceStatement:
    is_a: Entity
  AnalysisChoice:
    is_a: Entity
"""
TIME = "2026-09-14T00:00:00Z"  # Synthetic fixture time, not an observation.
ACTOR = "actor:synthetic-history-probe"
SOURCE = b'{"name":"statement"}\n{"name":"choice A"}\n{"name":"choice B"}\n'


def plan(history, record_id, record_type, row, profile, prior):
    return {
        "grammar": "malleus.population-plan/private-v0",
        "plan_id": f"plan:{record_id}",
        "contract_identity": history.partial_contract.identity,
        "adapter": {"adapter_id": "synthetic-history-probe", "version": "1"},
        "history_profile": {
            "profile_id": profile.profile_id,
            "sha256": profile.identity,
        },
        "sources": [
            {
                "source_id": "source:probe",
                "sha256": "sha256:" + sha256(SOURCE).hexdigest(),
            }
        ],
        "evidence": [],
        "records": {
            "entities": [
                {
                    "id": record_id,
                    "type": record_type,
                    "properties": {
                        "name": json.loads(SOURCE.splitlines()[row])["name"]
                    },
                }
            ],
            "relations": [],
        },
        "derivations": [
            {
                "record_id": record_id,
                "path": ["properties", "name"],
                "source_id": "source:probe",
                "locator": f"row:{row}:name",
            }
        ],
        "gaps": [],
        "supersessions": (
            []
            if prior is None
            else [{"record_id": record_id, "supersedes_record_id": prior}]
        ),
        "valid_time": (
            {"kind": "ORDER_ONLY", "value": "capture:synthetic"}
            if profile is api.SOURCE_ASSERTION_PROFILE
            else {"kind": "NONE_STATED", "value": None}
        ),
    }


def test_separate_batch_profiles_preserve_statement_and_replay_choice(tmp_path):
    compiled = api.compile_linkml_contract(
        root_locator="probe",
        sources={
            "probe": SCHEMA,
            "malleus": bundled_ontology_path("malleus.yaml").read_bytes(),
            "linkml:types": (
                files("linkml_runtime")
                .joinpath("linkml_model", "model", "schema", "types.yaml")
                .read_bytes()
            ),
        },
    )
    path = tmp_path / "history.jsonl"
    history = api.create_structural_history(
        path, compilation=compiled, transaction_time=TIME, actor_id=ACTOR
    )
    history.append_anchors(
        anchors=api.structural_source_anchors(
            source_id="source:probe",
            artifact_id="artifact:probe",
            content=SOURCE,
            media_type="application/x-ndjson",
        ),
        transaction_time=TIME,
        actor_id=ACTOR,
    )
    stages = (
        ("statement", "SourceStatement", 0, api.SOURCE_ASSERTION_PROFILE, None),
        ("choice:A", "AnalysisChoice", 1, api.STATE_VERSION_PROFILE, None),
        ("choice:B", "AnalysisChoice", 2, api.STATE_VERSION_PROFILE, "choice:A"),
    )
    snapshots = []
    prefixes = []
    for stage in stages:
        proposal = plan(history, *stage)
        profile = stage[3]
        wrong_profile = (
            api.STATE_VERSION_PROFILE
            if profile is api.SOURCE_ASSERTION_PROFILE
            else api.SOURCE_ASSERTION_PROFILE
        )
        before = path.read_bytes()
        with pytest.raises(api.PopulationPlanRefusal) as refusal:
            api.compile_population_plan(
                proposal,
                partial_contract=history.partial_contract,
                contract_view=compiled.view,
                base_state=api.PopulationBaseState.from_replay(history.replay()),
                history_profile=wrong_profile,
            )
        assert refusal.value.reason is api.PopulationPlanRefusalReason.IDENTITY_MISMATCH
        assert path.read_bytes() == before
        compilation = api.compile_population_plan(
            proposal,
            partial_contract=history.partial_contract,
            contract_view=compiled.view,
            base_state=api.PopulationBaseState.from_replay(history.replay()),
            history_profile=profile,
        )
        preparation = api.prepare_population_change(
            history=history,
            plan=proposal,
            profile=profile,
            retention_events=api.population_retention_events(
                history=history, compilation=compilation, profile=profile
            ),
            transaction_time=TIME,
            actor_id=ACTOR,
        )
        admitted = api.admit_structural_change(
            history=history,
            preparation=preparation,
            transaction_time=TIME,
            actor_id=ACTOR,
        )
        snapshots.append(admitted)
        prefixes.append(path.read_bytes())

    final = api.KnowledgeChangeHistory.reopen(path).replay()
    assert len(final.change_sets) == 3
    assert final.receipt == snapshots[-1].receipt
    assert final.graph.export_records() == snapshots[-1].graph.export_records()
    assert final.graph.get_node("statement") == snapshots[0].graph.get_node("statement")
    assert snapshots[1].graph.get_node("choice:A") is not None
    assert snapshots[1].graph.get_node("choice:B") is None
    assert final.graph.get_node("choice:A") is None
    assert final.graph.get_node("choice:B") is not None
    assert final.record_history["choice:A"].superseded_by == "choice:B"
    for record_id, _, _, profile, _ in stages:
        trace = api.trace_population_record(final, record_id)
        assert trace.history_profile.identity == profile.identity
        assert trace.sources[0].content == SOURCE
        assert trace.derivations[0]["source_id"] == "source:probe"

    # Exercise exact historical prefix replay, without truncating the live ledger.
    for index, prefix in enumerate(prefixes):
        assert prefixes[-1].startswith(prefix)
        historical_path = tmp_path / f"prefix-{index}.jsonl"
        historical_path.write_bytes(prefix)
        earlier = api.KnowledgeChangeHistory.reopen(historical_path).replay()
        assert earlier.receipt == snapshots[index].receipt
        assert earlier.graph.export_records() == snapshots[index].graph.export_records()
