"""Prepare existing population/KCS from an applied capture, never admit it."""

from functools import wraps
from hashlib import sha256
import json
from pathlib import Path

import malleus.compiler as core
from malleus.ledger import aware_datetime, canonical_json, record_hash
from research.semantic_reentry_external_design import supplier_components


class SupplierObservationMappingError(ValueError):
    def __init__(self, reason, detail):
        self.reason, self.detail = reason, detail
        super().__init__(f"{reason}: {detail}")


def _guarded(function):
    @wraps(function)
    def invoke(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (TypeError, KeyError, AttributeError, RecursionError) as error:
            raise SupplierObservationMappingError(
                "MALFORMED_INPUT", str(error)
            ) from error

    return invoke


def _need(condition, reason, detail):
    if not condition:
        raise SupplierObservationMappingError(reason, detail)


def _digest(content):
    return "sha256:" + sha256(content).hexdigest()


def _canonical(value):
    try:
        return canonical_json(value).encode()
    except ValueError as error:
        raise SupplierObservationMappingError("MALFORMED_INPUT", str(error)) from error


def _object(content):
    _need(type(content) is bytes, "MALFORMED_INPUT", "exact canonical bytes required")
    try:
        value = json.loads(content)
    except ValueError as error:
        raise SupplierObservationMappingError("MALFORMED_INPUT", str(error)) from error
    _need(
        type(value) is dict and _canonical(value) == content,
        "MALFORMED_INPUT",
        "canonical JSON object required",
    )
    return value


def _record(replay, identifier, kind):
    entry = replay.protocol_replay.data["records"][identifier]
    value = entry["record"]
    _need(
        entry["record_type"] == kind
        and value["id"] == identifier
        and record_hash(kind, value) == value["content_hash"],
        "EVIDENCE_DISAGREEMENT",
        "wrong typed record or hash: " + identifier,
    )
    return value


def _source(replay, identifier):
    record = _record(replay, identifier, "SourceArtifact")
    content = replay.retained_bytes(identifier)
    _need(
        _digest(content) == record["source_content_digest"]
        and len(content) == record["source_byte_length"],
        "EVIDENCE_DISAGREEMENT",
        "retained source bytes differ",
    )
    return record, content


def _bound_source(replay, reference):
    _, content = _source(replay, reference["id"])
    _need(
        _digest(content) == reference["bytes_sha256"],
        "EVIDENCE_DISAGREEMENT",
        "original source binding differs",
    )
    return content


def _ref(record):
    return {"id": record["id"], "record_hash": record["content_hash"]}


@_guarded
def prepare_observed_supplier_change(
    *,
    history,
    expected_head,
    expected_count,
    original_context_id,
    observation_id,
    outcome_contract_id,
    observer_implementation_identity,
    operator_bytes,
    source_id,
    source_artifact_id,
    evidence_id,
    plan_id,
    history_profile,
    transaction_time,
    actor_id,
):
    """Retain the exact observation-to-population bridge; return before admission."""
    _need(
        type(history) is core.KnowledgeChangeHistory,
        "MALFORMED_INPUT",
        "actual owning Core history required",
    )
    _need(
        all(
            type(v) is str and v.strip()
            for v in (
                expected_head,
                original_context_id,
                observation_id,
                outcome_contract_id,
                observer_implementation_identity,
                source_id,
                source_artifact_id,
                evidence_id,
                plan_id,
                transaction_time,
                actor_id,
            )
        ),
        "MALFORMED_INPUT",
        "explicit nonblank metadata required",
    )
    _need(
        type(expected_count) is int and expected_count >= 0,
        "MALFORMED_INPUT",
        "nonnegative integer event count required",
    )
    replay = history.replay()
    _need(
        (expected_head, expected_count)
        == (replay.ledger_head, replay.ledger_event_count),
        "STALE_BASE",
        "expected ledger head/count differ",
    )
    _need(
        replay.protocol_replay is not None,
        "UNSUPPORTED_RULE",
        "selected action attachment required",
    )
    _need(
        type(history_profile) is core.DomainHistoryProfile
        and history_profile.identity == core.STATE_VERSION_PROFILE.identity,
        "UNSUPPORTED_RULE",
        "explicit state-version profile required",
    )
    fresh = (source_id, source_artifact_id, evidence_id, plan_id)
    used = {r.record_id for r in replay.retained_inputs} | set(
        replay.protocol_replay.data["records"]
    )
    _need(
        len(set(fresh)) == len(fresh) and not used.intersection(fresh),
        "DUPLICATE_OUTPUT",
        "distinct fresh population IDs required",
    )

    observation = _record(replay, observation_id, "OutcomeObservation")
    contract = _record(replay, outcome_contract_id, "OutcomeContractArtifact")
    execution = _record(replay, observation["execution_id"], "ActionExecution")
    dispatch = _record(replay, execution["dispatch_id"], "ActionDispatch")
    action = _record(replay, dispatch["action_proposal_id"], "SupplierOrderAmendment")
    original_record, original_bytes = _source(replay, original_context_id)
    original = _object(original_bytes)
    state = replay.protocol_replay.data["state"]["protocol"]
    _need(
        original["schema"] == "malleus.action-history.original-context/research-v1"
        and original["id"] == original_context_id
        and original["action_id"] == action["id"]
        and {"keys": [original["proposal_id"]], "value": original_context_id}
        in state["context_by_proposal"]
        and {"keys": [original["proposal_id"]], "value": "ACCEPTED"}
        in state["proposal_states"],
        "EVIDENCE_DISAGREEMENT",
        "original context is not applied to this accepted action",
    )
    _need(
        observation["execution_hash"] == execution["content_hash"]
        and execution["dispatch_hash"] == dispatch["content_hash"]
        and dispatch["action_content_hash"] == action["content_hash"]
        and observation["outcome_contract_id"] == outcome_contract_id
        and observation["outcome_contract_hash"] == contract["content_hash"]
        and {"keys": [execution["id"], outcome_contract_id], "value": observation_id}
        in state["observation_by_execution_contract"]
        and {"keys": [dispatch["id"]], "value": execution["id"]}
        in state["execution_by_dispatch"],
        "EVIDENCE_DISAGREEMENT",
        "applied observation/execution/action binding differs",
    )
    _need(
        contract["observation_type"]
        == observation["observation_type"]
        == "OBSERVED_SOURCE"
        and contract["observer_implementation_hash"] == observer_implementation_identity
        and len(contract["source_record_ids"]) == 1,
        "UNSUPPORTED_OBSERVATION",
        "selected observer contract differs",
    )
    _, implementation_bytes = _source(replay, contract["source_record_ids"][0])
    _need(
        _digest(implementation_bytes) == observer_implementation_identity,
        "UNSUPPORTED_OBSERVATION",
        "observer implementation bytes differ",
    )
    try:
        current_time = aware_datetime(transaction_time, "population time")
        observed_time = aware_datetime(observation["observed_at"], "observation time")
    except ValueError as error:
        raise SupplierObservationMappingError("MALFORMED_INPUT", str(error)) from error
    _need(
        current_time >= observed_time, "MALFORMED_INPUT", "population predates capture"
    )

    captured, content = _source(replay, observation["observed_source_artifact_id"])
    _need(
        captured["content_hash"] == observation["observed_source_artifact_hash"]
        and captured["source_record_ids"] == [execution["id"], outcome_contract_id]
        and captured["source_locator"]
        == "urn:controlled:" + action["logical_source_id"],
        "SOURCE_DISAGREEMENT",
        "capture provenance or logical source differs",
    )
    goal = _object(_bound_source(replay, original["goal"]))
    mapping = _object(_bound_source(replay, original["mapping"]))
    preservation = _object(_bound_source(replay, original["preservation"]))
    before = _bound_source(replay, original["pre_state_source"])
    operator = _object(operator_bytes)
    _need(
        operator["kind"] == action["action_type"]
        and all(
            operator[k] == action[k]
            for k in (
                "expected_quantity",
                "requested_quantity",
                "new_source_occurrence_id",
            )
        ),
        "UNSUPPORTED_RULE",
        "operator differs from accepted action",
    )
    _need(
        set(preservation) == {"mode", "required_ids"}
        and preservation["mode"] == "ALL_OTHER_ACCEPTED_RECORDS_AND_HISTORY"
        and type(preservation["required_ids"]) is list
        and len(set(preservation["required_ids"])) == len(preservation["required_ids"])
        and all(i in replay.record_history for i in preservation["required_ids"]),
        "UNSUPPORTED_RULE",
        "declared complement must remain available",
    )
    expected_initial = _object(
        supplier_components.map_initial_source(
            before,
            source_sha256=action["expected_source_digest"],
            mapping=mapping,
            source_id=action["logical_source_id"],
        )
    )["records"]["entities"][0]
    expected_record = {
        "id": expected_initial["id"],
        "type": expected_initial["type"],
        **expected_initial["properties"],
    }
    _need(
        replay.graph.query(
            mapping["type"],
            supplier_order_id=goal["supplier_order_id"],
            product_code=goal["product_code"],
        )
        == [expected_record],
        "SOURCE_DISAGREEMENT",
        "unique current target must match accepted pre-state",
    )
    initial_trace = core.trace_population_record(replay, mapping["initial_record_id"])
    _need(
        tuple((s.record_id, s.content) for s in initial_trace.sources)
        == ((action["logical_source_id"], before),),
        "SOURCE_DISAGREEMENT",
        "accepted target source trace differs",
    )
    _need(
        observation["observation_result"] != "INDETERMINATE",
        "UNSUPPORTED_OBSERVATION",
        "indeterminate evidence cannot prepare a replacement",
    )
    fragment = supplier_components.map_observation(
        content,
        before_bytes=before,
        source_sha256=action["expected_source_digest"],
        goal=goal,
        operator=operator,
        mapping=mapping,
        source_id=source_id,
    )
    _need(
        observation["observation_result"]
        == ("CONTRADICTED" if fragment is None else "CONFIRMED"),
        "EVIDENCE_DISAGREEMENT",
        "mapped source and recorded observation disagree",
    )
    if fragment is None:
        return None

    binding = _canonical(
        {
            "schema": "malleus.reentry.observed-source-binding/research-v1",
            "original_context": {
                **_ref(original_record),
                "bytes_sha256": _digest(original_bytes),
            },
            "observation": _ref(observation),
            "outcome_contract": {
                **_ref(contract),
                "observer_implementation_hash": observer_implementation_identity,
            },
            "observed_source": {**_ref(captured), "bytes_sha256": _digest(content)},
            "population_source": {
                "source_id": source_id,
                "artifact_id": source_artifact_id,
                "bytes_sha256": _digest(content),
            },
            "goal": original["goal"],
            "mapping": original["mapping"],
            "preservation": original["preservation"],
            "operator": operator,
        }
    )
    current = history.replay()
    _need(
        (expected_head, expected_count)
        == (current.ledger_head, current.ledger_event_count),
        "STALE_BASE",
        "history moved during observation mapping",
    )
    history.append_anchors(
        anchors=(
            *core.structural_source_anchors(
                source_id=source_id,
                artifact_id=source_artifact_id,
                content=content,
                media_type="application/x-ndjson",
            ),
            core.structural_evidence_anchor(
                record_id=evidence_id, content=binding, media_type="application/json"
            ),
        ),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    retained = history.replay()
    plan = {
        "grammar": "malleus.population-plan/private-v0",
        "plan_id": plan_id,
        "contract_identity": retained.partial_contract.identity,
        "history_profile": {
            "profile_id": history_profile.profile_id,
            "sha256": history_profile.identity,
        },
        "adapter": {"adapter_id": ADAPTER_ID, "version": ADAPTER_IDENTITY},
        "evidence": [{"evidence_id": evidence_id, "sha256": _digest(binding)}],
        "gaps": [],
        **_object(fragment),
    }
    compiled = core.compile_population_plan(
        plan,
        partial_contract=retained.partial_contract,
        contract_view=retained.contract_view,
        base_state=core.PopulationBaseState.from_replay(retained),
        history_profile=history_profile,
    )
    return core.prepare_population_change(
        history=history,
        plan=plan,
        profile=json.loads(history_profile.canonical_bytes),
        retention_events=core.population_retention_events(
            history=history, compilation=compiled, profile=history_profile
        ),
        transaction_time=transaction_time,
        actor_id=actor_id,
    )


ADAPTER_ID = "malleus.reentry.supplier.observed-source/research-v1"
ADAPTER_IDENTITY = _digest(
    ADAPTER_ID.encode()
    + b"\0"
    + Path(supplier_components.__file__).read_bytes()
    + b"\0"
    + Path(__file__).read_bytes()
)
