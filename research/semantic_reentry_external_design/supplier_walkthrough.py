"""One repository-local supplier episode, using the existing protocol adapters.

Run as a module with a new output directory. Fixed fixture times are protocol
coordinates, not wall-clock claims. This is not a supplier service or planner.
"""

import argparse
from importlib.resources import files
import json
from pathlib import Path
import sys

import malleus.compiler as core
from malleus.assent import make_record
from malleus.ledger import canonical_json, content_digest
from malleus.source import source_artifact_fields, source_bytes_digest
from research.action_history_contract_freeze.programs.check_executor import (
    load_check_executor,
)
from research.action_history_contract_freeze.programs.registration_bundle import (
    SOURCE_PROJECTION,
)
from research.semantic_reentry_external_design import (
    supplier_authorization as authority,
    supplier_components as components,
    supplier_execution as execution,
    supplier_observation as observation,
    supplier_observed_source as observed,
    supplier_proposals as proposals,
    supplier_reentry as reentry,
)
from research.semantic_reentry_external_design.accepted_read_view import (
    freeze_accepted_replay,
)
from research.semantic_reentry_external_design.supplier_initial_source import (
    prepare_initial_supplier_change,
)
from research.semantic_reentry_external_design.supplier_initialization import (
    initialize_supplier_protocol,
)
from research.semantic_reentry_external_design.supplier_program import (
    build_supplier_program,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SHOP = ROOT / "research/ontology_driven_kg_realization"
BASE = SHOP / "fixtures/small_shop_fulfilment/input"
FIXTURE = HERE / "fixtures/supplier_commitment_v1"
TIME = "2026-09-08T06:00:00Z"
POPULATION_TIME = "2026-09-08T06:40:00Z"
ACTOR = "actor:supplier:proposer"
EXECUTOR = "actor:supplier:executor"
SOURCE = "source:reentry:supplier:initial"
INITIALIZATION = "source:supplier:initialization"
CONTEXT = "context:supplier:authored-action"
ACTION = "action:supplier:authored-action"
PROPOSAL = "proposal:supplier:authored-action"
RULE = "source:supplier:reentry-rule"
GOAL = "source:supplier:bound-goal"
IMPLEMENTATION = "source:supplier:reentry-implementation"
EXECUTOR_SOURCE = "source:supplier:executor-implementation"
MAPPER = "source:supplier:observed-mapper-implementation"
OBSERVER = "outcome-contract:supplier:source"
CURRENT = "source:supplier:current-context"
POLICIES = {role: "policy:supplier:" + role for role in ("epistemic", "authorization")}


class WalkthroughError(ValueError):
    """The demonstration refused; any partial ledger is retained for inspection."""


def require(condition, detail):
    if not condition:
        raise WalkthroughError("CHECKPOINT_DISAGREEMENT: " + detail)


def canonical(value):
    return canonical_json(value).encode()


def write_new(path, content):
    with path.open("xb") as stream:
        stream.write(content)


def position(history):
    replay = history.replay()
    return dict(
        expected_head=replay.ledger_head, expected_count=replay.ledger_event_count
    )


def retain_source(history, identifier, content, dependencies):
    """Author an input event, then use the existing validated retention gate."""
    record = make_record(
        "SourceArtifact",
        id=identifier,
        event_id="event:" + identifier,
        generated_at=TIME,
        actor_id=ACTOR,
        role="registrar",
        source_record_ids=dependencies,
        artifact_kind="SOURCE",
        artifact_version="research-v1",
        **source_artifact_fields(
            artifact_id=identifier,
            artifact_version="research-v1",
            source_bytes=content,
            media_type="application/octet-stream",
            locator="urn:retained:" + identifier,
        ),
    )
    history.append_protocol_events(
        transaction="source",
        **position(history),
        events=(
            {
                "event_id": record["generation_event_id"],
                "event_type": "PREREQUISITE_RECORDED",
                "actor_id": ACTOR,
                "transaction_time": TIME,
                "data": {
                    "records": {
                        "value": [{"record_type": "SourceArtifact", "record": record}]
                    },
                    "dependencies": {"value": dependencies},
                    "preimage": {
                        "value": {
                            key: record[field]
                            for key, field in SOURCE_PROJECTION.items()
                        }
                    },
                },
                "retained": {
                    "source": {
                        "record_id": identifier,
                        "content": content,
                        "media_type": record["source_media_type"],
                        "role": "SOURCE_ARTIFACT",
                        "encoding": "BYTES",
                    }
                },
            },
        ),
    )


def accepted_start(directory, case):
    """Compile the accepted Shop schema and populate RET-010 plus e4-only B/Y/1."""
    types = (
        files("linkml_runtime")
        .joinpath("linkml_model/model/schema/types.yaml")
        .read_bytes()
    )
    common = {
        "malleus": (ROOT / "ontology/malleus.yaml").read_bytes(),
        "linkml:types": types,
    }
    compiled = core.compile_linkml_contract(
        root_locator="small-shop-correction",
        sources={
            **common,
            "small-shop": (BASE / "tbox/small-shop.yaml").read_bytes(),
            "small-shop-correction": (
                SHOP
                / "fixtures/small_shop_fulfilment_correction_v1/input/tbox/small-shop-correction.yaml"
            ).read_bytes(),
        },
    )
    action_contract = core.compile_linkml_contract(
        root_locator="supplier-amendment",
        sources={
            **common,
            "supplier-amendment": (HERE / "supplier-action.yaml").read_bytes(),
            "assent": (ROOT / "ontology/assent.yaml").read_bytes(),
        },
    )
    population = dict(
        transaction_time="2026-09-08T04:00:00Z",
        actor_id="actor:reentry:initial-population",
    )
    history = core.create_structural_history(
        directory / "history.jsonl", compilation=compiled, **population
    )
    anchors = [
        core.structural_evidence_anchor(
            record_id="artifact:small-shop:baseline-mapping",
            content=(SHOP / "experiments/small_shop/pareto/mapping.json").read_bytes(),
            media_type="application/json",
        )
    ]
    for name, filename, media in (
        ("warehouse", "warehouse.jsonl", "application/x-ndjson"),
        ("inventory", "inventory-units.csv", "text/csv"),
    ):
        anchors.extend(
            core.structural_source_anchors(
                source_id="source:small-shop:" + name,
                artifact_id="artifact:source:small-shop:" + name,
                content=(BASE / "sources" / filename).read_bytes(),
                media_type=media,
            )
        )
    history.append_anchors(anchors=tuple(anchors), **population)
    plan = json.loads(
        (
            SHOP / "experiments/small_shop/public_population/plans/ret010.json"
        ).read_bytes()
    )
    plan["contract_identity"] = history.partial_contract.identity
    plan["history_profile"]["sha256"] = core.STATE_VERSION_PROFILE.identity
    replay = history.replay()
    compiled_plan = core.compile_population_plan(
        plan,
        partial_contract=replay.partial_contract,
        contract_view=replay.contract_view,
        base_state=core.PopulationBaseState.from_replay(replay),
        history_profile=core.STATE_VERSION_PROFILE,
    )
    prepared = core.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(core.STATE_VERSION_PROFILE.canonical_bytes),
        retention_events=core.population_retention_events(
            history=history,
            compilation=compiled_plan,
            profile=core.STATE_VERSION_PROFILE,
        ),
        **population,
    )
    core.admit_structural_change(history=history, preparation=prepared, **population)
    source = (FIXTURE / "input/supplier-before.jsonl").read_bytes()
    prepared = prepare_initial_supplier_change(
        history=history,
        source_bytes=source,
        source_sha256=case["source"]["sha256"],
        mapping_bytes=canonical(case["mapping"]),
        source_id=SOURCE,
        source_artifact_id="artifact:source:reentry:supplier:initial",
        mapping_id="artifact:reentry:supplier:initial-mapping",
        plan_id="plan:reentry:supplier:initial",
        history_profile=core.STATE_VERSION_PROFILE,
        **population,
    )
    core.admit_structural_change(history=history, preparation=prepared, **population)
    write_new(directory / "supplier.jsonl", source)
    program = build_supplier_program(
        action_contract.artifact.artifact_bytes,
        source_ids={
            role: "source:supplier:selected:" + role
            for role in (
                "profile",
                "record_contract",
                "machine",
                "history_binding",
            )
        },
        policy_ids=POLICIES,
    )
    initialize_supplier_protocol(
        history=history,
        **position(history),
        program_bytes=program,
        program_record_id="artifact:supplier:program",
        selection_event_id="event:supplier:select",
        initialization_id=INITIALIZATION,
        checker=load_check_executor(),
        checker_source_ids={
            role: "source:supplier:checks:" + role
            for role in ("definition", "implementation")
        },
        monitor_ids={
            "epistemic": ["monitor:supplier:type:0", "monitor:supplier:type:1"],
            "authorization": [
                "monitor:supplier:authority:0",
                "monitor:supplier:authority:1",
            ],
        },
        ruleset_id="ruleset:supplier:type",
        epistemic_control_bytes=canonical(
            {
                "schema": "malleus.reentry.supplier.epistemic-control/research-v1",
                "violation_verdicts": ["REJECT", "REJECT"],
                "unknown_verdicts": ["DEFER", "DEFER"],
                "control_precedence": ["REJECT", "DEFER", "CONTEST"],
            }
        ),
        transaction_time="2026-09-08T05:00:00Z",
        actor_id="actor:supplier:registrar",
        artifact_version="research-v1",
    )
    return history


def bind_episode(history, case):
    roles = {
        role: "source:supplier:" + role
        for role in ("mapping", "preservation", "pre_state_source")
    }
    for role, content in (
        ("mapping", canonical(case["mapping"])),
        ("preservation", canonical(case["preservation"])),
        ("pre_state_source", history.replay().retained_bytes(SOURCE)),
    ):
        retain_source(history, roles[role], content, [])
    for identifier, content in (
        (IMPLEMENTATION, reentry.IMPLEMENTATION_BYTES),
        (EXECUTOR_SOURCE, execution.IMPLEMENTATION_BYTES),
        (
            MAPPER,
            observed.ADAPTER_ID.encode()
            + b"\0"
            + Path(components.__file__).read_bytes()
            + b"\0"
            + Path(observed.__file__).read_bytes(),
        ),
    ):
        retain_source(history, identifier, content, [])
    observation.register_supplier_observer(
        history=history,
        **position(history),
        implementation_source_id="source:supplier:observer-implementation",
        outcome_contract_id=OBSERVER,
        actor_id="actor:supplier:observer-registrar",
        generated_at=TIME,
        artifact_version="research-v1",
    )
    stopping = case["stopping"]
    rule = dict(
        schema=reentry.RULE_SCHEMA,
        initialization_id=INITIALIZATION,
        goal_kind=case["goal"]["kind"],
        output_type="SupplierOrderAmendment",
        logical_source_id=SOURCE,
        operator=case["operator"],
        ambiguity=stopping["ambiguity"],
        candidate_budget=stopping["candidate_budget"],
        dispatch_attempt_budget=stopping["dispatch_attempt_budget"],
        automatic_retry=stopping["automatic_retry"],
        stopping="INITIAL_SATISFIED_OR_LINKED_OBSERVED_KCS",
        implementations={
            name: dict(
                source_id=IMPLEMENTATION,
                bytes_sha256=reentry.IMPLEMENTATION_IDENTITY,
                entrypoint=engine.entrypoint,
            )
            for name, engine in (
                ("synthesizer", reentry.SupplierReentrySynthesizer()),
                ("model", reentry.SupplierSourceModel()),
                ("update_strategy", reentry.SupplierActionStrategy()),
            )
        },
        executor=dict(
            source_id=EXECUTOR_SOURCE, bytes_sha256=execution.IMPLEMENTATION_IDENTITY
        ),
        observer=dict(
            outcome_contract_id=OBSERVER,
            observer_implementation_hash=observation.IMPLEMENTATION_IDENTITY,
        ),
        observed_mapper=dict(
            source_id=MAPPER,
            bytes_sha256=observed.ADAPTER_IDENTITY,
            adapter_id=observed.ADAPTER_ID,
        ),
        output=dict(
            proposer_id=ACTOR,
            generated_at=TIME,
            proposal_key="supplier:synthesized:proposal",
        ),
    )
    retain_source(
        history,
        RULE,
        canonical(rule),
        [IMPLEMENTATION, EXECUTOR_SOURCE, MAPPER, OBSERVER],
    )
    retain_source(history, GOAL, canonical(case["goal"]), [RULE])
    view = freeze_accepted_replay(
        replay=history.replay(), context=history.composition_context()
    )
    original = proposals.original_supplier_context(
        view=view,
        initialization_id=INITIALIZATION,
        source_ids=dict(roles, goal=GOAL),
        context_id=CONTEXT,
        action_id=ACTION,
        proposal_id=PROPOSAL,
        episode_key=case["episode"]["id"],
    )
    return original


def evaluate(history, original):
    view = freeze_accepted_replay(
        replay=history.replay(), context=history.composition_context()
    )
    contract = reentry.bind_supplier_reentry(
        view=view, original_context_bytes=original, rule_source_id=RULE
    )
    result = reentry.SupplierReentrySynthesizer().synthesize(
        contract,
        view,
        model=reentry.SupplierSourceModel(),
        update_strategy=reentry.SupplierActionStrategy(),
    )
    return contract, result


def authorize(history, original, candidate):
    proposals.submit_supplier_proposal(
        history=history,
        **position(history),
        original_context_bytes=original,
        action_bytes=candidate,
        proposal_key="supplier:synthesized:proposal",
        context_actor_id=ACTOR,
        artifact_version="research-v1",
    )
    records = history.replay().protocol_replay.data["records"]
    for ordinal, monitor in enumerate(
        records[POLICIES["epistemic"]]["record"]["required_monitor_ids"]
    ):
        proposals.record_supplier_type_check(
            history=history,
            **position(history),
            proposal_id=PROPOSAL,
            context_id=CONTEXT,
            monitor_id=monitor,
            assessment_id=f"assessment:supplier:{ordinal}",
            failure_id=f"failure:supplier:{ordinal}",
            actor_id="actor:supplier:type-checker",
            generated_at=TIME,
        )
    proposals.decide_supplier_proposal(
        history=history,
        **position(history),
        proposal_id=PROPOSAL,
        context_id=CONTEXT,
        assessment_ids=("assessment:supplier:0", "assessment:supplier:1"),
        decision_id="decision:supplier:1",
        transition_id="transition:supplier:1",
        actor_id="actor:supplier:epistemic-controller",
        generated_at=TIME,
    )
    fields = dict(
        grantor_actor_id="actor:supplier:grantor",
        grantee_actor_id=EXECUTOR,
        permitted_action_types=["AMEND_SUPPLIER_ORDER"],
        scope_record_id=GOAL,
        may_subdelegate=False,
        grant_valid_from=TIME,
        grant_valid_to="2026-09-08T08:00:00Z",
    )
    grant = make_record(
        "AuthorityGrant",
        id="grant:supplier:direct",
        event_id="event:grant:supplier:direct",
        generated_at=TIME,
        actor_id=fields["grantor_actor_id"],
        role="registrar",
        source_record_ids=[GOAL],
        artifact_kind="AUTHORITY_GRANT",
        artifact_version="research-v1",
        artifact_hash=content_digest(fields),
        **fields,
    )
    bindings = dict(
        history=history,
        original_context_id=CONTEXT,
        current_context_id=CURRENT,
        scope_association_id="source:supplier:scope-association",
        requested_interval_id="source:supplier:requested-interval",
    )
    authority.prepare_supplier_authority(
        **bindings,
        **position(history),
        grant_bytes=canonical(grant),
        requested_interval_bytes=canonical(
            dict(start=TIME, end="2026-09-08T07:00:00Z")
        ),
        actor_id="actor:supplier:authority-registrar",
        generated_at=TIME,
        artifact_version="research-v1",
    )
    bindings.update(grant_id=grant["id"], executor_id=EXECUTOR)
    for ordinal, monitor in enumerate(
        records[POLICIES["authorization"]]["record"]["required_monitor_ids"]
    ):
        authority.record_supplier_authority_check(
            **bindings,
            **position(history),
            monitor_id=monitor,
            assessment_id=f"authority:supplier:{ordinal}",
            failure_id=f"authority-failure:supplier:{ordinal}",
            actor_id="actor:supplier:authority-checker",
            generated_at=TIME,
        )
    authority.decide_supplier_authorization(
        **bindings,
        **position(history),
        assessment_ids=("authority:supplier:0", "authority:supplier:1"),
        decision_id="authorization:supplier:1",
        transition_id="authorization-transition:supplier:1",
        actor_id="actor:supplier:authorizer",
        generated_at=TIME,
    )


def checkpoint(directory, history, stage, **details):
    replay = history.replay()
    suppliers = [
        r
        for r in replay.graph.export_records()["entities"]
        if r["type"] == "SupplierOrderState"
    ]
    require(len(suppliers) == 1, "expected one current supplier record")
    record = suppliers[0]
    ledger = history.path.read_bytes()
    source = (directory / "supplier.jsonl").read_bytes()
    result = dict(
        stage=stage,
        accepted_record_id=record["id"],
        accepted_quantity=record["properties"]["ordered_quantity"],
        source_quantity=json.loads(source)["quantity"],
        graph_digest=replay.graph.state_digest(),
        acceptance_head=replay.acceptance_head,
        ledger_head=replay.ledger_head,
        ledger_event_count=replay.ledger_event_count,
        ledger_byte_length=len(ledger),
        ledger_sha256=source_bytes_digest(ledger),
        source_sha256=source_bytes_digest(source),
        **details,
    )
    write_new(directory / (stage + ".json"), canonical(result))
    print(
        f"{stage}: supplier-file={result['source_quantity']} accepted={result['accepted_quantity']}",
        flush=True,
    )
    if details:
        print(
            "  " + " ".join(f"{key}={value}" for key, value in details.items()),
            flush=True,
        )
    return result


def run(directory):
    """Execute one fixed local episode. Refuse overwrite; preserve partial runs."""
    directory = Path(directory)
    try:
        directory.mkdir()
    except FileExistsError as error:
        raise WalkthroughError(
            "OUTPUT_EXISTS: choose a new output directory: " + str(directory)
        ) from error
    case = json.loads((FIXTURE / "case.json").read_bytes())
    history = accepted_start(directory, case)
    original = bind_episode(history, case)
    write_new(directory / "original-context.json", original)
    before = history.replay()
    steps = [checkpoint(directory, history, "accepted_start")]
    contract, result = evaluate(history, original)
    require(
        result.status == "CANDIDATES" and len(result.candidates) == 1,
        "expected one pinned proposal",
    )
    require(
        result.finding.current_quantity == 1 and result.finding.shortfall == 1,
        "expected shortfall one",
    )
    write_new(directory / "reentry-contract.json", contract.canonical_bytes)
    write_new(directory / "action-proposal.json", result.candidates[0])
    steps.append(
        checkpoint(
            directory,
            history,
            "proposal_only",
            candidate_count=len(result.candidates),
            shortfall=result.finding.shortfall,
        )
    )
    require(
        steps[0]["ledger_sha256"] == steps[1]["ledger_sha256"]
        and steps[0]["source_sha256"] == steps[1]["source_sha256"],
        "synthesis changed history or supplier file",
    )
    authorize(history, original, result.candidates[0])
    execution.dispatch_and_execute_supplier(
        history=history,
        **position(history),
        original_context_id=CONTEXT,
        current_context_id=CURRENT,
        action_id=ACTION,
        authorization_id="authorization:supplier:1",
        executor_implementation_id=EXECUTOR_SOURCE,
        executor_id=EXECUTOR,
        dispatcher_id="actor:supplier:dispatcher",
        dispatch_id="dispatch:supplier:1",
        execution_id="execution:supplier:1",
        dispatched_at="2026-09-08T06:10:00Z",
        execution_started_at="2026-09-08T06:10:00Z",
        execution_ended_at="2026-09-08T06:20:00Z",
        source_path=directory / "supplier.jsonl",
        logical_source_id=SOURCE,
    )
    receipt = history.replay().protocol_replay.data["records"]["execution:supplier:1"][
        "record"
    ]
    steps.append(
        checkpoint(
            directory,
            history,
            "executed_not_observed",
            execution_status=receipt["execution_status"],
        )
    )
    observation.observe_supplier_execution(
        history=history,
        **position(history),
        execution_id="execution:supplier:1",
        outcome_contract_id=OBSERVER,
        observer_id="actor:supplier:observer",
        observed_source_id="source:supplier:captured:1",
        observation_id="observation:supplier:1",
        observed_at="2026-09-08T06:30:00Z",
        source_path=directory / "supplier.jsonl",
        logical_source_id=SOURCE,
        artifact_version="research-v1",
    )
    captured = history.replay()
    write_new(
        directory / "observed-source.jsonl",
        captured.retained_bytes("source:supplier:captured:1"),
    )
    prepared = observed.prepare_observed_supplier_change(
        history=history,
        **position(history),
        original_context_id=CONTEXT,
        observation_id="observation:supplier:1",
        outcome_contract_id=OBSERVER,
        observer_implementation_identity=observation.IMPLEMENTATION_IDENTITY,
        operator_bytes=canonical(case["operator"]),
        source_id="source:supplier:observed-population:1",
        source_artifact_id="artifact:supplier:observed-population:1",
        evidence_id="evidence:supplier:observation-binding:1",
        plan_id="plan:supplier:observed-population:1",
        history_profile=core.STATE_VERSION_PROFILE,
        transaction_time=POPULATION_TIME,
        actor_id="actor:supplier:observed-population",
    )
    require(
        prepared is not None and type(prepared.change_set) is core.KnowledgeChangeSet,
        "observation produced no KCS",
    )
    write_new(
        directory / "observed-change-set.json", prepared.change_set.canonical_bytes
    )
    steps.append(
        checkpoint(
            directory,
            history,
            "observed_kcs_not_admitted",
            observation_result=captured.protocol_replay.data["records"][
                "observation:supplier:1"
            ]["record"]["observation_result"],
        )
    )
    require(
        all(
            step["accepted_quantity"] == 1
            and step["graph_digest"] == steps[0]["graph_digest"]
            and step["acceptance_head"] == steps[0]["acceptance_head"]
            for step in steps
        ),
        "knowledge changed before KCS admission",
    )
    core.admit_structural_change(
        history=history,
        preparation=prepared,
        transaction_time=POPULATION_TIME,
        actor_id="actor:supplier:observed-population",
    )
    history = core.KnowledgeChangeHistory.reopen(directory / "history.jsonl")
    final = history.replay()
    replacement = case["mapping"]["replacement_record_id"]
    old = case["mapping"]["initial_record_id"]
    require(
        final.graph.get_node(replacement)["ordered_quantity"] == 2,
        "replayed quantity is not two",
    )
    require(
        final.record_history[old].superseded_by == replacement,
        "old fact was not superseded",
    )
    for family, members in before.graph.export_records().items():
        require(
            [r for r in members if r["id"] != old]
            == [
                r
                for r in final.graph.export_records()[family]
                if r["id"] != replacement
            ],
            "complement changed",
        )
    for identifier, record in before.record_history.items():
        if identifier != old:
            require(
                final.record_history[identifier] == record,
                "unmentioned history changed",
            )
    trace = core.trace_population_record(final, replacement)
    require(
        trace.sources[0].content
        == captured.retained_bytes("source:supplier:captured:1"),
        "source lineage differs",
    )
    steps.append(checkpoint(directory, history, "admitted_and_replayed"))
    _, stopped = evaluate(history, original)
    require(
        stopped.status == "SATISFIED"
        and stopped.reason == "LINKED_OBSERVED_KCS"
        and not stopped.candidates,
        "episode did not become quiescent",
    )
    steps.append(
        checkpoint(
            directory,
            history,
            "quiescent",
            candidate_count=len(stopped.candidates),
            reentry_status=stopped.status,
            reentry_reason=stopped.reason,
        )
    )
    require(
        steps[-2]["ledger_sha256"] == steps[-1]["ledger_sha256"]
        and steps[-2]["source_sha256"] == steps[-1]["source_sha256"],
        "fresh evaluation caused a write",
    )
    report = dict(
        schema="malleus.reentry.supplier-walkthrough/research-v1",
        classification="REFERENCE_IMPLEMENTATION",
        complete=True,
        claim="BOUNDED_LOCAL_SUPPLIER_REENTRY",
        goal=case["goal"],
        checkpoints=steps,
    )
    write_new(directory / "walkthrough.json", canonical(report))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output", type=Path, help="new directory under an existing parent"
    )
    args = parser.parse_args()
    try:
        run(args.output)
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(
        "One local episode complete. No supplier delivery or production integration claim."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
