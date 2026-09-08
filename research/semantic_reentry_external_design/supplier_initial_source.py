"""Prepare, never admit, the independently attributed initial supplier source.

Module loading identifies the exact two-file implementation. Invocation uses
only explicit inputs and the owning public Core retention/preparation methods.
"""

from hashlib import sha256
import json
from pathlib import Path

import malleus.compiler as api
from research.semantic_reentry_external_design import supplier_components


ADAPTER_ID = "malleus.reentry.supplier.initial-source/research-v1"
ADAPTER_IDENTITY = (
    "sha256:"
    + sha256(
        ADAPTER_ID.encode()
        + b"\0"
        + Path(supplier_components.__file__).read_bytes()
        + b"\0"
        + Path(__file__).read_bytes()
    ).hexdigest()
)


def _canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def prepare_initial_supplier_change(
    *,
    history,
    source_bytes,
    source_sha256,
    mapping_bytes,
    source_id,
    source_artifact_id,
    mapping_id,
    plan_id,
    history_profile,
    transaction_time,
    actor_id,
):
    """Retain exact source/mapping and return Core's still-unaccepted preparation."""
    if type(history) is not api.KnowledgeChangeHistory:
        raise supplier_components.SupplierInputError(
            "MALFORMED_INPUT", "the owning public Core history is required"
        )
    try:
        if type(mapping_bytes) is not bytes:
            raise ValueError("exact mapping bytes required")
        mapping = json.loads(mapping_bytes)
        if type(mapping) is not dict or _canonical(mapping) != mapping_bytes:
            raise ValueError("canonical mapping object required")
    except (ValueError, TypeError, RecursionError) as error:
        raise supplier_components.SupplierInputError(
            "MALFORMED_INPUT", str(error)
        ) from error
    fragment = json.loads(
        supplier_components.map_initial_source(
            source_bytes,
            source_sha256=source_sha256,
            mapping=mapping,
            source_id=source_id,
        )
    )
    if (
        type(history_profile) is not api.DomainHistoryProfile
        or history_profile.identity != api.STATE_VERSION_PROFILE.identity
    ):
        raise supplier_components.SupplierInputError(
            "UNSUPPORTED_RULE", "explicit state-version profile required"
        )
    for value in (
        source_id,
        source_artifact_id,
        mapping_id,
        plan_id,
        transaction_time,
        actor_id,
    ):
        if type(value) is not str or not value.strip():
            raise supplier_components.SupplierInputError(
                "MALFORMED_INPUT", "all IDs, actor and transaction time are required"
            )

    source_anchors = api.structural_source_anchors(
        source_id=source_id,
        artifact_id=source_artifact_id,
        content=source_bytes,
        media_type="application/x-ndjson",
    )
    mapping_anchor = api.structural_evidence_anchor(
        record_id=mapping_id, content=mapping_bytes, media_type="application/json"
    )
    history.append_anchors(
        anchors=(*source_anchors, mapping_anchor),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    replay = history.replay()
    plan = {
        "grammar": "malleus.population-plan/private-v0",
        "plan_id": plan_id,
        "contract_identity": replay.partial_contract.identity,
        "history_profile": {
            "profile_id": history_profile.profile_id,
            "sha256": history_profile.identity,
        },
        "adapter": {"adapter_id": ADAPTER_ID, "version": ADAPTER_IDENTITY},
        "evidence": [
            {
                "evidence_id": mapping_id,
                "sha256": "sha256:" + sha256(mapping_bytes).hexdigest(),
            }
        ],
        "gaps": [],
        **fragment,
    }
    compiled = api.compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=api.PopulationBaseState.from_replay(replay),
        history_profile=history_profile,
    )
    return api.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(history_profile.canonical_bytes),
        retention_events=api.population_retention_events(
            history=history, compilation=compiled, profile=history_profile
        ),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
