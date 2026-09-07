"""One pure, source-backed correction producer using the public Core composer.

Module loading records this local implementation's exact two-file identity.
Invocation receives only immutable values and performs no ambient I/O.
"""

import json
from pathlib import Path

import malleus.compiler as api
from malleus import KnowledgeGraph
from research.semantic_reentry_protocol import consumer
from research.semantic_reentry_protocol.consumer import (
    Reason,
    ReentryRefusal,
    Status,
    assess_request,
    canonical,
    digest,
)


SYNTHESIZER_IDENTITY = digest(
    b"malleus.semantic-reentry.synthesizer/research-v0\0"
    + Path(consumer.__file__).read_bytes()
    + b"\0"
    + Path(__file__).read_bytes()
)

_COORDINATES = {
    "ledger_head": "base_ledger_head",
    "ledger_event_count": "base_ledger_event_count",
    "acceptance_head": "base_acceptance_head",
    "materialization_head": "base_materialization_head",
    "graph_state_digest": "base_accepted_state_digest",
    "contract_identity": "contract_identity",
    "receipt_identity": "receipt_identity",
}


def synthesize(
    *,
    contract,
    context,
    view_bytes,
    plan_bytes,
    source_bytes,
    mapping_bytes,
    partial_contract,
    contract_view,
    base_state,
    history_profile,
):
    """Return one existing KCS, no candidate, or typed refusal. Never admit."""
    assessment = assess_request(
        contract=contract,
        view_bytes=view_bytes,
        plan_bytes=plan_bytes,
        source_bytes=source_bytes,
        mapping_bytes=mapping_bytes,
        synthesizer_identity=SYNTHESIZER_IDENTITY,
    )
    for value, expected_type in (
        (context, api.KnowledgeChangeContext),
        (partial_contract, api.PartialEffectiveContract),
        (contract_view, api.ContractView),
        (base_state, api.PopulationBaseState),
        (history_profile, api.DomainHistoryProfile),
    ):
        if type(value) is not expected_type:
            raise ReentryRefusal(
                Reason.MALFORMED_INPUT, f"expected immutable {expected_type.__name__}"
            )
    view, plan = json.loads(view_bytes), json.loads(plan_bytes)
    coordinates = {
        field: getattr(context, attribute) for field, attribute in _COORDINATES.items()
    }
    retained = {
        member.record_id: {"sha256": member.identity, "role": member.role}
        for member in context.retained_inputs
    }
    if (
        coordinates != view["coordinates"]
        or retained != view["retained"]
        or partial_contract.identity != context.contract_identity
    ):
        raise ReentryRefusal(
            Reason.STALE_BASE, "read input and Core composition context differ"
        )
    # Reconstruct a disposable validation graph, never the accepted graph.
    # Matching copied headers alone cannot authenticate the supplied body.
    try:
        projection = KnowledgeGraph.from_records(contract_view, view["records"])
    except (ValueError, TypeError) as error:
        raise ReentryRefusal(
            Reason.MALFORMED_INPUT, f"projection records are invalid: {error}"
        ) from error
    if projection.state_digest() != context.base_accepted_state_digest:
        raise ReentryRefusal(
            Reason.STALE_BASE,
            "projection body differs from Core's accepted-state digest",
        )
    if plan["history_profile"] != {
        "profile_id": history_profile.profile_id,
        "sha256": history_profile.identity,
    }:
        raise ReentryRefusal(
            Reason.INPUT_IDENTITY_MISMATCH,
            "selected history profile differs from the plan",
        )
    if assessment.status is Status.SATISFIED:
        return ()

    compiled = api.compile_population_plan(
        plan,
        partial_contract=partial_contract,
        contract_view=contract_view,
        base_state=base_state,
        history_profile=history_profile,
    )
    if (
        compiled.canonical_plan_bytes != plan_bytes
        or compiled.status is not api.PopulationPlanStatus.CHANGE_SET
        or len(compiled.operations) != 1
    ):
        raise ReentryRefusal(
            Reason.PRESERVATION_VIOLATION,
            "compiled output exceeds the assessed footprint",
        )
    operation = compiled.operations[0]
    expected = plan["records"]["entities"][0]
    # Check the primitive footprint independently of the selected compiler.
    if (
        operation.operation_type != "CREATE_ENTITY"
        or operation.record_id != expected["id"]
        or operation.record_type != expected["type"]
        or canonical(dict(operation.properties)) != canonical(expected["properties"])
        or operation.supersedes_record_id != contract.data["request"]["prior_record_id"]
        or operation.depends_on != ()
        or operation.source_id is not None
        or operation.target_id is not None
        or compiled.valid_time != api.KnowledgeValidTime.from_data(plan["valid_time"])
    ):
        raise ReentryRefusal(
            Reason.PRESERVATION_VIOLATION,
            "compiled primitive differs from the assessed replacement",
        )
    candidate = api.compose_change_set(
        context=context,
        change_set_id=f"change:{compiled.plan_id}",
        source_record_ids=compiled.source_record_ids,
        evidence_record_ids=compiled.evidence_record_ids,
        operations=compiled.operations,
        valid_time=compiled.valid_time,
        supersedes=compiled.supersedes,
    )
    return (candidate,)
