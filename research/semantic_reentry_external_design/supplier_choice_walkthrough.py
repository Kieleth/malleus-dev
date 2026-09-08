"""Runnable two-alternative Shop experiment, no tests or outcome oracle imported."""

import argparse
from hashlib import sha256
import json
from pathlib import Path

import malleus.compiler as core
from research.semantic_reentry_external_design import supplier_choice as choice
from research.semantic_reentry_external_design import supplier_reentry as child
from research.semantic_reentry_external_design import supplier_walkthrough as single
from research.semantic_reentry_external_design import supplier_execution as execution
from research.semantic_reentry_external_design import (
    supplier_observation as observation,
)
from research.semantic_reentry_external_design import (
    supplier_observed_source as observed,
)
from research.semantic_reentry_external_design import supplier_components as components
from research.semantic_reentry_external_design.accepted_read_view import (
    freeze_accepted_replay,
)
from research.semantic_reentry_external_design.supplier_initial_source import (
    prepare_initial_supplier_change,
)


FIXTURE = Path(__file__).parent / "fixtures/supplier_choice_v1"
RULE = "source:supplier:choice-rule"
CHOICE_IMPLEMENTATION = "source:supplier:choice-implementation"
SOURCE_C = "source:choice:supplier:C:initial"
C_INITIAL = "supplier-order-state:C:choice-C-initial-1"
C_REPLACEMENT = "supplier-order-state:C:choice-C-amendment-1"


def read(history, projection):
    context = history.composition_context()
    replay = projection.refresh(
        expected_head_hash=context.base_ledger_head,
        expected_event_count=context.base_ledger_event_count,
    )
    return freeze_accepted_replay(replay=replay, context=context)


def base_case():
    return json.loads((single.FIXTURE / "case.json").read_bytes())


def c_mapping():
    return dict(
        base_case()["mapping"],
        initial_record_id=C_INITIAL,
        supersedes_record_id=C_INITIAL,
        replacement_record_id=C_REPLACEMENT,
    )


def child_rule(case, source_id):
    return dict(
        schema=child.RULE_SCHEMA,
        initialization_id=single.INITIALIZATION,
        goal_kind="GoalPredicate",
        output_type="SupplierOrderAmendment",
        logical_source_id=source_id,
        operator=case["operator"],
        ambiguity="REFUSE_IF_NOT_UNIQUE",
        candidate_budget=1,
        dispatch_attempt_budget=1,
        automatic_retry=False,
        stopping="INITIAL_SATISFIED_OR_LINKED_OBSERVED_KCS",
        implementations={
            role: dict(
                source_id=single.IMPLEMENTATION,
                bytes_sha256=child.IMPLEMENTATION_IDENTITY,
                entrypoint=engine.entrypoint,
            )
            for role, engine in (
                ("synthesizer", child.SupplierReentrySynthesizer()),
                ("model", child.SupplierSourceModel()),
                ("update_strategy", child.SupplierActionStrategy()),
            )
        },
        executor=dict(
            source_id=single.EXECUTOR_SOURCE,
            bytes_sha256=execution.IMPLEMENTATION_IDENTITY,
        ),
        observer=dict(
            outcome_contract_id=single.OBSERVER,
            observer_implementation_hash=observation.IMPLEMENTATION_IDENTITY,
        ),
        observed_mapper=dict(
            source_id=single.MAPPER,
            bytes_sha256=observed.ADAPTER_IDENTITY,
            adapter_id=observed.ADAPTER_ID,
        ),
        output=dict(
            proposer_id=single.ACTOR,
            generated_at=single.TIME,
            proposal_key="supplier:synthesized:proposal",
        ),
    )


def install_rule(history, *, identifier, spec, suffix, reverse_alternatives):
    """Retain explicit rule and child inputs. This is setup, never synthesis."""
    alternatives = []
    for order in ("B", "C"):
        alternative = dict(
            order_id=order,
            rule_source_id=f"source:choice:{order}:rule:{suffix}",
            source_ids={
                role: f"source:choice:{order}:{role}:{suffix}"
                for role in child.SOURCE_ROLES
            },
            context_id=single.CONTEXT if order == "B" else "context:choice:C",
            action_id=single.ACTION if order == "B" else "action:choice:C",
            proposal_id=single.PROPOSAL if order == "B" else "proposal:choice:C",
            episode_key="choice:" + order + ":episode-1",
        )
        # B uses the existing runnable authorization scope and IDs.
        if order == "B" and suffix == "base":
            alternative["source_ids"]["goal"] = single.GOAL
        alternatives.append(alternative)
    if reverse_alternatives:
        alternatives.reverse()
    rule = dict(
        schema=choice.RULE_SCHEMA,
        **{
            key: spec[key]
            for key in (
                "goal",
                "selection",
                "evaluation_budget",
                "candidate_budget",
                "dispatch_attempt_budget",
                "automatic_retry",
                "stopping",
            )
        },
        alternatives=alternatives,
        implementation=dict(
            source_id=CHOICE_IMPLEMENTATION,
            bytes_sha256=choice.IMPLEMENTATION_IDENTITY,
            entrypoint=choice.SupplierChoiceSynthesizer.entrypoint,
        ),
    )
    single.retain_source(
        history, identifier, single.canonical(rule), [CHOICE_IMPLEMENTATION]
    )
    for alternative in alternatives:
        order = alternative["order_id"]
        case = base_case()
        if order == "C":
            case["goal"]["supplier_order_id"] = "C"
            case["operator"]["new_source_occurrence_id"] = "choice-C-amendment-1"
            case["mapping"] = c_mapping()
        source_id = single.SOURCE if order == "B" else SOURCE_C
        rule_bytes = single.canonical(child_rule(case, source_id))
        single.retain_source(
            history,
            alternative["rule_source_id"],
            rule_bytes,
            [
                single.IMPLEMENTATION,
                single.EXECUTOR_SOURCE,
                single.MAPPER,
                single.OBSERVER,
            ],
        )
        for role, content, dependencies in (
            ("goal", single.canonical(case["goal"]), [alternative["rule_source_id"]]),
            ("mapping", single.canonical(case["mapping"]), []),
            ("pre_state_source", history.replay().retained_bytes(source_id), []),
            (
                "preservation",
                single.canonical(
                    dict(
                        mode="ALL_OTHER_ACCEPTED_RECORDS_AND_HISTORY",
                        required_ids=[
                            "O1",
                            "X1",
                            "contains:O1:X1",
                            C_INITIAL
                            if order == "B"
                            else base_case()["mapping"]["initial_record_id"],
                        ],
                    )
                ),
                [identifier],
            ),
        ):
            single.retain_source(
                history, alternative["source_ids"][role], content, dependencies
            )
    return identifier


def prepare(directory):
    """Populate real accepted B and C facts, then retain the two-choice inputs."""
    directory = Path(directory)
    single.require(
        directory.is_dir() and not any(directory.iterdir()),
        "new empty output directory required",
    )
    history = single.accepted_start(directory, base_case())
    spec = json.loads((FIXTURE / "case.json").read_bytes())
    source_c = (FIXTURE / spec["additional_source"]).read_bytes()
    population = dict(
        transaction_time="2026-09-08T05:10:00Z",
        actor_id="actor:choice:initial-population",
    )
    prepared = prepare_initial_supplier_change(
        history=history,
        source_bytes=source_c,
        source_sha256=choice.digest(source_c),
        mapping_bytes=single.canonical(c_mapping()),
        source_id=SOURCE_C,
        source_artifact_id="artifact:choice:C:initial",
        mapping_id="artifact:choice:C:initial-mapping",
        plan_id="plan:choice:C:initial",
        history_profile=core.STATE_VERSION_PROFILE,
        **population,
    )
    core.admit_structural_change(history=history, preparation=prepared, **population)
    single.write_new(directory / "supplier-C.jsonl", source_c)
    for identifier, content in (
        (single.IMPLEMENTATION, child.IMPLEMENTATION_BYTES),
        (single.EXECUTOR_SOURCE, execution.IMPLEMENTATION_BYTES),
        (
            single.MAPPER,
            observed.ADAPTER_ID.encode()
            + b"\0"
            + Path(components.__file__).read_bytes()
            + b"\0"
            + Path(observed.__file__).read_bytes(),
        ),
        (CHOICE_IMPLEMENTATION, choice.IMPLEMENTATION_BYTES),
    ):
        single.retain_source(history, identifier, content, [])
    observation.register_supplier_observer(
        history=history,
        **single.position(history),
        implementation_source_id="source:supplier:observer-implementation",
        outcome_contract_id=single.OBSERVER,
        actor_id="actor:supplier:observer-registrar",
        generated_at=single.TIME,
        artifact_version="research-v1",
    )
    install_rule(
        history, identifier=RULE, spec=spec, suffix="base", reverse_alternatives=False
    )
    # Both policies are retained before either pure evaluation. No ex-post rewrite.
    variant(
        history, selection=dict(strategy="REFUSE_IF_NOT_UNIQUE", order_preference=[])
    )
    return history


def variant(history, *, selection=None, reverse_alternatives=False, changes=None):
    """Explicit conformance intervention: retain a separate immutable rule."""
    spec = json.loads(history.replay().retained_bytes(RULE))
    if selection is not None:
        spec["selection"] = selection
    if changes is not None:
        spec.update(changes)
    suffix = sha256(
        single.canonical(dict(spec=spec, reversed=reverse_alternatives))
    ).hexdigest()[:16]
    identifier = "source:choice:variant:" + suffix
    # Reusing an already retained identical test policy performs no append.
    if identifier in history.replay().protocol_replay.data["records"]:
        return identifier
    if reverse_alternatives:
        spec["alternatives"].reverse()
    preservations = []
    for alternative in spec["alternatives"]:
        prior = alternative["source_ids"]["preservation"]
        content = history.replay().retained_bytes(prior)
        current = prior + ":" + suffix
        alternative["source_ids"]["preservation"] = current
        preservations.append((current, content))
    single.retain_source(
        history, identifier, single.canonical(spec), [CHOICE_IMPLEMENTATION]
    )
    for current, content in preservations:
        single.retain_source(history, current, content, [identifier])
    return identifier


def evaluate(history, identifier, *, projection):
    view = read(history, projection)
    contract = choice.bind_supplier_choice(view=view, rule_source_id=identifier)
    result = choice.SupplierChoiceSynthesizer().synthesize(
        contract,
        view,
        synthesizer=child.SupplierReentrySynthesizer(),
        model=child.SupplierSourceModel(),
        update_strategy=child.SupplierActionStrategy(),
    )
    return contract, result


def quantities(replay):
    return {
        r["properties"]["supplier_order_id"]: r["properties"]["ordered_quantity"]
        for r in replay.graph.export_records()["entities"]
        if r["type"] == "SupplierOrderState"
    }


def finish(directory):
    directory = Path(directory)
    history = core.KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    projection = core.KnowledgeHistoryProjection.open(history.path)
    before = history.replay()
    initial_ledger = history.path.read_bytes()
    complement_source = (directory / "supplier-C.jsonl").read_bytes()
    ambiguity_id = variant(
        history, selection=dict(strategy="REFUSE_IF_NOT_UNIQUE", order_preference=[])
    )
    _, ambiguous = evaluate(history, ambiguity_id, projection=projection)
    single.require(
        (ambiguous.status, ambiguous.reason, ambiguous.candidates)
        == ("REFUSED", "AMBIGUOUS", ()),
        "undeclared choice must refuse",
    )
    contract, result = evaluate(history, RULE, projection=projection)
    single.require(
        result.status == "CANDIDATES" and result.selected_order == "B",
        "explicit B preference must select B",
    )
    single.require(
        history.path.read_bytes() == initial_ledger, "pure selection changed ledger"
    )
    original = single.canonical(
        json.loads(contract.canonical_bytes)["original_contexts"]["B"]
    )
    single.write_new(directory / "choice-contract.json", contract.canonical_bytes)
    single.write_new(directory / "action-proposal.json", result.candidates[0])
    single.authorize(history, original, result.candidates[0])
    _, pending = evaluate(history, RULE, projection=projection)
    single.require(
        pending.status == "PENDING" and not pending.candidates,
        "authorization reissued an action",
    )
    execution.dispatch_and_execute_supplier(
        history=history,
        **single.position(history),
        original_context_id=single.CONTEXT,
        current_context_id=single.CURRENT,
        action_id=single.ACTION,
        authorization_id="authorization:supplier:1",
        executor_implementation_id=single.EXECUTOR_SOURCE,
        executor_id=single.EXECUTOR,
        dispatcher_id="actor:supplier:dispatcher",
        dispatch_id="dispatch:supplier:1",
        execution_id="execution:supplier:1",
        dispatched_at="2026-09-08T06:10:00Z",
        execution_started_at="2026-09-08T06:10:00Z",
        execution_ended_at="2026-09-08T06:20:00Z",
        source_path=directory / "supplier.jsonl",
        logical_source_id=single.SOURCE,
    )
    executed = dict(
        source={
            "B": json.loads((directory / "supplier.jsonl").read_bytes())["quantity"],
            "C": json.loads((directory / "supplier-C.jsonl").read_bytes())["quantity"],
        },
        accepted=quantities(history.replay()),
    )
    _, pending = evaluate(history, RULE, projection=projection)
    single.require(
        pending.status == "PENDING" and not pending.candidates,
        "receipt falsely satisfied goal",
    )
    single.require(
        history.replay().graph.export_records() == before.graph.export_records(),
        "action changed graph",
    )
    observation.observe_supplier_execution(
        history=history,
        **single.position(history),
        execution_id="execution:supplier:1",
        outcome_contract_id=single.OBSERVER,
        observer_id="actor:supplier:observer",
        observed_source_id="source:supplier:captured:1",
        observation_id="observation:supplier:1",
        observed_at="2026-09-08T06:30:00Z",
        source_path=directory / "supplier.jsonl",
        logical_source_id=single.SOURCE,
        artifact_version="research-v1",
    )
    prepared = observed.prepare_observed_supplier_change(
        history=history,
        **single.position(history),
        original_context_id=single.CONTEXT,
        observation_id="observation:supplier:1",
        outcome_contract_id=single.OBSERVER,
        observer_implementation_identity=observation.IMPLEMENTATION_IDENTITY,
        operator_bytes=single.canonical(base_case()["operator"]),
        source_id="source:supplier:observed-population:1",
        source_artifact_id="artifact:supplier:observed-population:1",
        evidence_id="evidence:supplier:observation-binding:1",
        plan_id="plan:supplier:observed-population:1",
        history_profile=core.STATE_VERSION_PROFILE,
        transaction_time=single.POPULATION_TIME,
        actor_id="actor:supplier:observed-population",
    )
    single.require(
        prepared is not None and type(prepared.change_set) is core.KnowledgeChangeSet,
        "observed KCS required",
    )
    _, pending = evaluate(history, RULE, projection=projection)
    single.require(
        pending.status == "PENDING" and not pending.candidates,
        "unadmitted observation falsely satisfied goal",
    )
    single.require(
        history.replay().graph.export_records() == before.graph.export_records(),
        "preparation changed graph",
    )
    core.admit_structural_change(
        history=history,
        preparation=prepared,
        transaction_time=single.POPULATION_TIME,
        actor_id="actor:supplier:observed-population",
    )
    history = core.KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    final = history.replay()
    old, new = (
        base_case()["mapping"]["initial_record_id"],
        base_case()["mapping"]["replacement_record_id"],
    )
    for family, members in before.graph.export_records().items():
        single.require(
            [r for r in members if r["id"] != old]
            == [r for r in final.graph.export_records()[family] if r["id"] != new],
            "complement changed",
        )
    for identifier, record in before.record_history.items():
        if identifier != old:
            single.require(
                final.record_history[identifier] == record,
                "unmentioned history changed",
            )
    trace = core.trace_population_record(final, new)
    single.require(
        trace.sources[0].content == final.retained_bytes("source:supplier:captured:1"),
        "observed lineage differs",
    )
    ledger = history.path.read_bytes()
    _, stopped = evaluate(history, RULE, projection=projection)
    single.require(
        (stopped.status, stopped.reason, stopped.candidates)
        == ("SATISFIED", "LINKED_OBSERVED_KCS", ()),
        "not quiescent",
    )
    single.require(history.path.read_bytes() == ledger, "reevaluation wrote ledger")
    single.require(
        (directory / "supplier-C.jsonl").read_bytes() == complement_source,
        "unselected source bytes changed",
    )
    report = dict(
        accepted_initial=quantities(before),
        predicted_totals={a.order_id: a.predicted_total for a in result.alternatives},
        without_preference=dict(
            status=ambiguous.status,
            reason=ambiguous.reason,
            candidates=len(ambiguous.candidates),
        ),
        with_preference=dict(
            selected_order=result.selected_order, candidates=len(result.candidates)
        ),
        executed_not_observed=executed,
        accepted_final=quantities(final),
        final=dict(
            status=stopped.status,
            reason=stopped.reason,
            candidates=len(stopped.candidates),
        ),
        dispatch_attempts=sum(
            r["record_type"] == "ActionDispatch"
            for r in final.protocol_replay.data["records"].values()
        ),
        ledger_head=final.ledger_head,
        ledger_event_count=final.ledger_event_count,
        ledger_sha256=choice.digest(ledger),
        graph_digest=final.graph.state_digest(),
        change_set_identity=prepared.change_set.identity,
        contract_identity=contract.identity,
    )
    single.write_new(directory / "choice-result.json", single.canonical(report))
    return report


def run(directory):
    directory = Path(directory)
    directory.mkdir()
    prepare(directory)
    return finish(directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    print(json.dumps(run(parser.parse_args().output), indent=2))
