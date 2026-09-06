"""Execute the existing Shop data through Core's structural admission bundle."""

from __future__ import annotations

import argparse
from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import malleus.compiler as api


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
INPUT_BYTES = (HERE / "inputs.json").read_bytes()
INPUTS = json.loads(INPUT_BYTES)


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(content: bytes) -> str:
    return "sha256:" + sha256(content).hexdigest()


def _artifact(record_id: str, content: bytes, role: str, media_type: str):
    return api.KnowledgeAnchorInput(
        machine_event=_canonical(
            {
                "event_type": "ARTIFACT_REGISTERED",
                "payload": {
                    "artifact_id": record_id,
                    "artifact_identity": _digest(content),
                },
            }
        ),
        retained_bytes=content,
        role=role,
        media_type=media_type,
    )


def _compile(which: str):
    return api.compile_linkml_contract(
        root_locator="small-shop",
        sources={
            "small-shop": (ROOT / INPUTS["ontologies"][which]).read_bytes(),
            "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model/model/schema/types.yaml")
            .read_bytes(),
        },
    )


def start_shop(path: Path, *, transaction_time: str, actor_id: str):
    """Bootstrap Core's bundle, then retain the exact fixture inputs."""

    # Read every input before creating history. Required data never gets a default.
    sources = {
        key: (ROOT / item["path"]).read_bytes()
        for key, item in INPUTS["sources"].items()
    }
    evidence = {
        key: (ROOT / value).read_bytes() for key, value in INPUTS["evidence"].items()
    }
    templates = {
        key: (ROOT / value).read_bytes() for key, value in INPUTS["plans"].items()
    }
    base = _compile("base")
    anchors = [
        _artifact(
            "artifact:small-shop:default-inputs",
            INPUT_BYTES,
            "RETAINED_EVIDENCE",
            "application/json",
        ),
        *(
            _artifact(key, value, "RETAINED_EVIDENCE", "application/json")
            for key, value in sorted(evidence.items())
        ),
        *(
            _artifact(
                f"template:small-shop:{key}",
                value,
                "RETAINED_EVIDENCE",
                "application/json",
            )
            for key, value in sorted(templates.items())
        ),
    ]
    for source_id, content in sorted(sources.items()):
        artifact_id = f"artifact:{source_id}"
        media_type = INPUTS["sources"][source_id]["media_type"]
        anchors.append(_artifact(artifact_id, content, "SOURCE_ARTIFACT", media_type))
        anchors.append(
            api.KnowledgeAnchorInput(
                machine_event=_canonical(
                    {
                        "event_type": "SOURCE_REGISTERED",
                        "payload": {
                            "artifact_id": artifact_id,
                            "source_id": source_id,
                            "source_identity": _digest(content),
                        },
                    }
                ),
                retained_bytes=content,
                role="RETAINED_SOURCE",
                media_type=media_type,
            )
        )
    history = api.create_structural_history(
        path, compilation=base, transaction_time=transaction_time, actor_id=actor_id
    )
    history.append_anchors(
        anchors=tuple(anchors), transaction_time=transaction_time, actor_id=actor_id
    )
    return history


def plan_for(history, name: str) -> dict[str, object]:
    """Rebind only the template's contract identity to the selected runtime."""

    replay = history.replay()
    plan = json.loads(replay.retained_bytes(f"template:small-shop:{name}"))
    plan["contract_identity"] = replay.partial_contract.identity
    return plan


def prepare_plan(history, plan, *, transaction_time: str, actor_id: str):
    """Validate before retaining the plan, using the public retention helper."""

    replay = history.replay()
    profile = api.STATE_VERSION_PROFILE
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
        profile=json.loads(profile.canonical_bytes),
        retention_events=api.population_retention_events(
            history=history, compilation=compilation, profile=profile
        ),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )


def accept_plan(history, name: str, *, transaction_time: str, actor_id: str):
    prepared = prepare_plan(
        history,
        plan_for(history, name),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    # These five named fixture plans all promise a change, not a gaps-only result.
    if prepared.change_set is None:
        raise ValueError(f"Shop plan {name} unexpectedly produced no domain change")
    return api.admit_structural_change(
        history=history,
        preparation=prepared,
        transaction_time=transaction_time,
        actor_id=actor_id,
    )


def revise_shop(history, *, transaction_time: str, actor_id: str):
    target = _compile("target")
    partial = api.compose_partial_effective_contract(
        validated_fact_set_sha256=target.artifact.validated_fact_set_sha256,
        normative_profile=api.STRUCTURAL_HISTORY_BUNDLE.normative_profile,
    )
    revision = history.compose_contract_revision(
        revision_id="revision:small-shop:default-admission",
        target_validated_contract_bytes=target.artifact.artifact_bytes,
        target_partial_contract_bytes=partial.canonical_bytes,
        reason="add the existing full Shop fixture vocabulary",
        issued_at=transaction_time,
    )
    return history.record_contract_revision(
        revision=revision, transaction_time=transaction_time, actor_id=actor_id
    )


def _report(replay, history_bytes: bytes) -> dict[str, object]:
    records = []
    for record_id in sorted(replay.record_history):
        trace = api.trace_population_record(replay, record_id)
        records.append(
            {
                "record_id": record_id,
                "change_set_id": trace.change_set.change_set_id,
                "plan_id": trace.population_plan["plan_id"],
                "plan_identity": trace.population_plan_identity,
                "contract_identity": trace.change_set.contract_identity,
                "supersedes": trace.record_history.supersedes_record_id,
                "superseded_by": trace.record_history.superseded_by,
                "sources": [
                    {"record_id": item.record_id, "identity": item.identity}
                    for item in trace.sources
                ],
                "derivations": [
                    dict(item, path=list(item["path"])) for item in trace.derivations
                ],
            }
        )
    return {
        "fixture": "small-shop-default-admission",
        "structural_bundle_identity": api.STRUCTURAL_HISTORY_BUNDLE.identity,
        "input_identity": _digest(
            replay.retained_bytes("artifact:small-shop:default-inputs")
        ),
        "ledger_sha256": _digest(history_bytes),
        "ledger_head": replay.ledger_head,
        "ledger_event_count": replay.ledger_event_count,
        "receipt_identity": replay.receipt.identity,
        "change_count": len(replay.change_sets),
        "contract_revision_count": len(replay.contract_revisions),
        "graph": replay.graph.export_records(),
        "queries": {
            "supplier_order_B": replay.graph.query(
                "SupplierOrderState", supplier_order_id="B"
            ),
            "payment_P1": replay.graph.query_relations(
                "PaymentSettlesInvoiceRelation", source_id="payment:P1"
            ),
        },
        "records": records,
        "non_claims": [
            "Structural admission does not establish source truth or epistemic acceptance.",
            "Mappings and times are the existing fixture's adopter choices.",
            "Source registration is explicit; row locators are not resolved by this example.",
            "No Event population, new time kind, stable wire, or Semantic Re-entry is claimed.",
        ],
    }


def run_shop(output: Path):
    """Create a fresh demonstration, then reopen its only state authority."""

    output.mkdir(parents=True, exist_ok=False)
    path = output / "history.jsonl"
    actor = INPUTS["actor_id"]
    history = start_shop(
        path, transaction_time=INPUTS["bootstrap_time"], actor_id=actor
    )
    for step in INPUTS["steps"]:
        if "plan" in step:
            accept_plan(
                history,
                step["plan"],
                transaction_time=step["transaction_time"],
                actor_id=actor,
            )
        elif step["revision"] == "target":
            revise_shop(
                history, transaction_time=step["transaction_time"], actor_id=actor
            )
        else:
            raise ValueError(f"unknown Shop step: {step}")
    del history
    replay = api.KnowledgeChangeHistory.reopen(path).replay()
    (output / "evidence.json").write_bytes(
        _canonical(_report(replay, path.read_bytes())) + b"\n"
    )
    return replay


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, required=True, help="new output directory"
    )
    args = parser.parse_args()
    replay = run_shop(args.output)
    print(
        f"Shop replayed: {len(replay.change_sets)} changes, "
        f"{len(replay.record_history)} historical records; {args.output / 'evidence.json'}"
    )


if __name__ == "__main__":
    main()
