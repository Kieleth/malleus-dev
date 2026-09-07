"""Current execution proof, independent of historical receipt equality tests.

Run identically inside each selected archive. Fixture runners consume only
their archive's data. Document admission below uses the public default bundle
so historical helper assertions cannot stop admission/reopen/trace coverage.
"""

from importlib.resources import files
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import malleus.compiler as api


def state(replay, *, population_plans=True):
    traces = {}
    retained = {}
    check_receipts = []
    for item in replay.retained_inputs:
        if item.role not in {"RETAINED_SOURCE", "RETAINED_EVIDENCE"}:
            continue
        if item.record_id == "sha256:" + sha256(item.content).hexdigest():
            # The two pre-population fixtures address check receipts by their
            # bytes. Keep every field and the original ID, but pair receipts
            # by stable check/change names for field-level comparison.
            value = json.loads(item.content)
            grammar = value["grammar"]
            assert grammar in {
                "malleus.check-receipt/private-v0",
                "malleus.small-shop.source-mapping-receipt/private-v0",
            }
            change_id = (
                value["change"]["change_set_id"]
                if grammar == "malleus.check-receipt/private-v0"
                else value["change_set_id"]
            )
            check_receipts.append(
                {
                    "key": [change_id, value["check_contract_id"]],
                    "record_id": item.record_id,
                    "value": value,
                }
            )
        else:
            retained[item.record_id] = {
                "role": item.role,
                "content": item.content.hex(),
            }
    for record_id in sorted(replay.record_history) if population_plans else ():
        trace = api.trace_population_record(replay, record_id)
        traces[record_id] = {
            "plan": json.loads(trace.population_plan_bytes),
            "sources": {item.record_id: item.content.hex() for item in trace.sources},
            "evidence": {item.record_id: item.content.hex() for item in trace.evidence},
            "supersedes": trace.record_history.supersedes_record_id,
            "superseded_by": trace.record_history.superseded_by,
            "valid_time": {
                "kind": trace.change_set.valid_time.kind,
                "value": trace.change_set.valid_time.value,
            },
        }
    return {
        "graph": replay.graph.export_records(),
        "state_digest": replay.graph.state_digest(),
        "traces": traces,
        "population_plan_traces": population_plans,
        "retained": retained,
        "check_receipts": sorted(check_receipts, key=lambda row: row["key"]),
        "record_links": {
            key: [value.supersedes_record_id, value.superseded_by]
            for key, value in replay.record_history.items()
        },
    }


def document(path):
    root = Path.cwd()
    examples = (
        root
        / "research/ontology_driven_kg_realization/fixtures/inspection_note_capture_v1"
    )
    compiled = api.compile_linkml_contract(
        root_locator="inspection-note",
        sources={
            "inspection-note": (examples / "inspection-note.yaml").read_bytes(),
            "malleus": (root / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )
    time = "2026-09-07T00:00:00Z"
    actor = "actor:compiler-compatibility"
    history = api.create_structural_history(
        path, compilation=compiled, transaction_time=time, actor_id=actor
    )
    reading = (examples / "reading.json").read_bytes()
    capture = (examples / "document-capture.json").read_bytes()
    history.append_anchors(
        anchors=(
            *api.structural_source_anchors(
                source_id="source:inspection-note",
                artifact_id="source-artifact",
                content=reading,
                media_type="application/json",
            ),
            api.structural_evidence_anchor(
                record_id="capture:inspection-note",
                content=capture,
                media_type="application/json",
            ),
        ),
        transaction_time=time,
        actor_id=actor,
    )
    template = json.loads((examples / "document-plan.json").read_bytes())
    adapted = api.adapt_document_assertions(
        reading_bytes=reading,
        capture_bytes=capture,
        capture_id="capture:inspection-note",
        plan_id=template["plan_id"],
        contract_identity=history.partial_contract.identity,
        records=template["records"],
        supersessions=template["supersessions"],
    )
    plan = json.loads(adapted.canonical_plan_bytes)
    replay = history.replay()
    compilation = api.compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=api.SOURCE_ASSERTION_PROFILE,
    )
    prepared = api.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(api.SOURCE_ASSERTION_PROFILE.canonical_bytes),
        retention_events=api.population_retention_events(
            history=history,
            compilation=compilation,
            profile=api.SOURCE_ASSERTION_PROFILE,
        ),
        transaction_time=time,
        actor_id=actor,
    )
    admitted = api.admit_structural_change(
        history=history, preparation=prepared, transaction_time=time, actor_id=actor
    )
    del history
    replay = api.KnowledgeChangeHistory.reopen(path).replay()
    assert replay.receipt == admitted.receipt
    trace = api.trace_population_record(replay, "inspection-of:P-7:2026-03-02")
    assert (
        next(
            item.content
            for item in trace.evidence
            if item.record_id == "capture:inspection-note"
        )
        == capture
    )
    assertions = {item["id"]: item for item in json.loads(capture)["assertions"]}
    assert assertions["asr:001"]["domain_time"] == "2026-03-02"
    assert assertions["asr:002"]["domain_time"] == "2026-03-01"
    assert "domain_time" not in assertions["asr:003"]
    assert trace.change_set.valid_time == api.KnowledgeValidTime(
        "ORDER_ONLY", "capture:inspection-note"
    )
    return state(replay)


def probe():
    from tests.contract_compiler.pareto.test_public_compiler import _compiled_shop
    from research.ontology_driven_kg_realization.experiments.small_shop.fresh_import.run import (
        run_import,
    )
    from research.ontology_driven_kg_realization.experiments.small_shop.object_event.run import (
        run_object_event,
    )
    from research.ontology_driven_kg_realization.experiments.small_shop.public_population.run import (
        run_full_shop,
    )
    from research.ontology_driven_kg_realization.experiments.small_shop.showcase.run import (
        run_showcase,
    )
    from research.ontology_driven_kg_realization.experiments.small_shop.correction.run import (
        run_correction,
    )

    with TemporaryDirectory(prefix="compiler-parity-") as temporary:
        root = Path(temporary)
        report = run_import(root / "fresh")
        fresh = api.KnowledgeChangeHistory.reopen(
            root / "fresh/shop/history.jsonl"
        ).replay()
        assert (
            report["rows_imported"] == 2 and report["prior_records_unchanged"] is True
        )
        assert len(fresh.record_history) == 12 and fresh.ledger_event_count == 59
        assert (
            fresh.graph.state_digest()
            == "sha256:ac6bc4c2a6be7ee851e0229b49276b11a8e0dbf91ed203705d611093c783e998"
        )
        results = {"fresh": state(fresh), "document": document(root / "document.jsonl")}
        for name, runner in (
            ("object_event", run_object_event),
            ("public_population", run_full_shop),
            ("showcase", run_showcase),
            ("correction", run_correction),
        ):
            output = root / name
            first = runner(output)
            second = runner(output)
            assert first.replay.receipt == second.replay.receipt
            # These two older fixtures predate population plans. Their graph,
            # source/evidence bytes and supersession links are compared, not a
            # population-trace capability they never claimed.
            results[name] = state(
                second.replay, population_plans=name not in {"showcase", "correction"}
            )
        return {
            "artifact": json.loads(_compiled_shop(api).artifact.artifact_bytes),
            "fresh_report": report,
            "semantics": results,
        }
