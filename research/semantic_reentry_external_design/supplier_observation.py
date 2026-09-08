"""Read actual supplier bytes and record observation, never change the domain."""

from functools import wraps
from hashlib import sha256
import json
import os
from pathlib import Path
import stat

import malleus.compiler as core
from malleus.assent import make_record
from malleus.execution import outcome_contract_digest
from malleus.ledger import aware_datetime, canonical_json, record_hash
from malleus.source import source_artifact_fields
from research.action_history_contract_freeze.programs.registration_bundle import (
    SOURCE_PROJECTION,
)


OBSERVATION_TYPE = "OBSERVED_SOURCE"


class SupplierObservationError(ValueError):
    def __init__(self, reason, detail):
        self.reason, self.detail = reason, detail
        super().__init__(f"{reason}: {detail}")


def _guarded(function):
    @wraps(function)
    def invoke(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (TypeError, KeyError, AttributeError, RecursionError) as error:
            raise SupplierObservationError("MALFORMED_INPUT", str(error)) from error

    return invoke


def _need(condition, reason, detail):
    if not condition:
        raise SupplierObservationError(reason, detail)


def _text(*values):
    _need(
        all(type(v) is str and v.strip() for v in values),
        "MALFORMED_INPUT",
        "explicit nonblank identifiers required",
    )


def _canonical(value):
    try:
        return canonical_json(value).encode()
    except ValueError as error:
        raise SupplierObservationError("MALFORMED_INPUT", str(error)) from error


def _digest(content):
    return "sha256:" + sha256(content).hexdigest()


def _instant(value):
    try:
        return aware_datetime(value, "supplier observation time")
    except ValueError as error:
        raise SupplierObservationError("MALFORMED_INPUT", str(error)) from error


def _owner(history, expected_head, expected_count):
    _need(
        type(history) is core.KnowledgeChangeHistory,
        "MALFORMED_INPUT",
        "actual owning Core history required",
    )
    _text(expected_head)
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
        "UNSUPPORTED",
        "selected action attachment required",
    )
    return replay


def _record(replay, identifier, kind):
    entry = replay.protocol_replay.data["records"][identifier]
    value = entry["record"]
    _need(
        entry["record_type"] == kind
        and value["id"] == identifier
        and record_hash(kind, value) == value["content_hash"],
        "MALFORMED_INPUT",
        "wrong typed record or identity: " + identifier,
    )
    return value


def _fresh(replay, identifiers):
    used = set(replay.protocol_replay.data["records"]) | {
        m.record_id for m in replay.retained_inputs
    }
    _need(
        len(set(identifiers)) == len(identifiers)
        and not used.intersection(identifiers),
        "DUPLICATE_OUTPUT",
        "fresh distinct output IDs required",
    )


def _event(kind, value, event_type):
    return {
        "event_id": value["generation_event_id"],
        "event_type": event_type,
        "actor_id": value["responsible_actor_id"],
        "transaction_time": value["generated_at"],
        "data": {
            "records": {"value": [{"record_type": kind, "record": value}]},
            "dependencies": {"value": value["source_record_ids"]},
        },
        "retained": {},
    }


def _source_event(
    identifier, content, media_type, locator, dependencies, actor, time, version
):
    value = make_record(
        "SourceArtifact",
        id=identifier,
        event_id="event:" + identifier,
        generated_at=time,
        actor_id=actor,
        role="registrar",
        source_record_ids=dependencies,
        artifact_kind="SOURCE",
        artifact_version=version,
        **source_artifact_fields(
            artifact_id=identifier,
            artifact_version=version,
            source_bytes=content,
            media_type=media_type,
            locator=locator,
        ),
    )
    event = _event("SourceArtifact", value, "PREREQUISITE_RECORDED")
    event["data"]["preimage"] = {
        "value": {k: value[v] for k, v in SOURCE_PROJECTION.items()}
    }
    event["retained"]["source"] = {
        "record_id": identifier,
        "content": content,
        "media_type": media_type,
        "role": "SOURCE_ARTIFACT",
        "encoding": "BYTES",
    }
    return value, event


def _append(history, replay, transaction, event):
    return history.append_protocol_events(
        transaction=transaction,
        events=(event,),
        expected_head=replay.ledger_head,
        expected_count=replay.ledger_event_count,
    )


@_guarded
def register_supplier_observer(
    *,
    history,
    expected_head,
    expected_count,
    implementation_source_id,
    outcome_contract_id,
    actor_id,
    generated_at,
    artifact_version,
):
    """Retain actual observer code and its existing outcome contract, not a result."""
    replay = _owner(history, expected_head, expected_count)
    _text(implementation_source_id, outcome_contract_id, actor_id, artifact_version)
    _instant(generated_at)
    _fresh(replay, (implementation_source_id, outcome_contract_id))
    implementation, source_event = _source_event(
        implementation_source_id,
        IMPLEMENTATION_BYTES,
        "text/x-python",
        "urn:retained:" + implementation_source_id,
        [],
        actor_id,
        generated_at,
        artifact_version,
    )
    value = make_record(
        "OutcomeContractArtifact",
        id=outcome_contract_id,
        event_id="event:" + outcome_contract_id,
        generated_at=generated_at,
        actor_id=actor_id,
        role="registrar",
        source_record_ids=[implementation_source_id],
        artifact_kind="OUTCOME_CONTRACT",
        artifact_version=artifact_version,
        artifact_hash=outcome_contract_digest(
            schema_version="1",
            contract_id=outcome_contract_id,
            contract_version=artifact_version,
            observation_type=OBSERVATION_TYPE,
            observer_implementation_hash=IMPLEMENTATION_IDENTITY,
        ),
        outcome_contract_schema_version="1",
        observation_type=OBSERVATION_TYPE,
        observer_implementation_hash=IMPLEMENTATION_IDENTITY,
    )
    event = _event("OutcomeContractArtifact", value, "PREREQUISITE_RECORDED")
    event["data"].update(
        implementation={
            "id": implementation_source_id,
            "record_hash": implementation["content_hash"],
        },
        preimage={
            "value": {
                "outcome_contract_schema_version": "1",
                "contract_id": outcome_contract_id,
                "contract_version": artifact_version,
                "observation_type": OBSERVATION_TYPE,
                "observer_implementation_hash": IMPLEMENTATION_IDENTITY,
            }
        },
    )
    after_source = _append(history, replay, "source", source_event)
    return _append(history, after_source, "outcome-contract", event)


def _capture(source_path):
    try:
        descriptor = os.open(source_path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(descriptor, "rb") as stream:
            _need(
                stat.S_ISREG(os.fstat(stream.fileno()).st_mode),
                "CAPTURE_UNAVAILABLE",
                "regular controlled source required",
            )
            return stream.read()
    except OSError as error:
        raise SupplierObservationError("CAPTURE_UNAVAILABLE", str(error)) from error


def _classify(content, action):
    """An independent, closed observation predicate, not the action model."""
    try:
        if type(content) is not bytes or not content.endswith(b"\n"):
            return "INDETERMINATE"
        row = json.loads(content)
        if (
            type(row) is not dict
            or set(row) != {"event_id", "supplier_order_id", "product_code", "quantity"}
            or type(row["quantity"]) is not int
            or not all(
                type(row[f]) is str and row[f].strip()
                for f in ("event_id", "supplier_order_id", "product_code")
            )
            or _canonical(row) + b"\n" != content
        ):
            return "INDETERMINATE"
    except (ValueError, TypeError, RecursionError):
        return "INDETERMINATE"
    agrees = (
        row["event_id"] == action["new_source_occurrence_id"]
        and row["quantity"] == action["requested_quantity"]
        and all(row[f] == action[f] for f in ("supplier_order_id", "product_code"))
    )
    return "CONFIRMED" if agrees else "CONTRADICTED"


@_guarded
def observe_supplier_execution(
    *,
    history,
    expected_head,
    expected_count,
    execution_id,
    outcome_contract_id,
    observer_id,
    observed_source_id,
    observation_id,
    observed_at,
    source_path,
    logical_source_id,
    artifact_version,
):
    """Capture actual bytes under the applied outcome contract; never compose KCS."""
    replay = _owner(history, expected_head, expected_count)
    _text(
        execution_id,
        outcome_contract_id,
        observer_id,
        observed_source_id,
        observation_id,
        logical_source_id,
        artifact_version,
    )
    moment = _instant(observed_at)
    _fresh(replay, (observed_source_id, observation_id))
    execution = _record(replay, execution_id, "ActionExecution")
    dispatch = _record(replay, execution["dispatch_id"], "ActionDispatch")
    action = _record(replay, dispatch["action_proposal_id"], "SupplierOrderAmendment")
    contract = _record(replay, outcome_contract_id, "OutcomeContractArtifact")
    state = replay.protocol_replay.data["state"]["protocol"]
    _need(
        {"keys": [dispatch["id"]], "value": execution_id}
        in state["execution_by_dispatch"],
        "UNAPPLIED_EXECUTION",
        "an applied execution is required",
    )
    _need(
        {"keys": [outcome_contract_id], "value": outcome_contract_id}
        in state["outcome_contracts"],
        "UNAPPLIED_CONTRACT",
        "an applied outcome contract is required",
    )
    if "observation_by_execution_contract" in state:
        _need(
            not any(
                row["keys"] == [execution_id, outcome_contract_id]
                for row in state["observation_by_execution_contract"]
            ),
            "DUPLICATE_OBSERVATION",
            "this execution/contract already has an observation",
        )
    _need(
        observer_id != execution["executor_id"],
        "OBSERVER_NOT_INDEPENDENT",
        "observer and executor actors must differ",
    )
    _need(
        moment >= _instant(execution["execution_ended_at"]),
        "OBSERVATION_BEFORE_EXECUTION",
        "observation must follow execution end",
    )
    _need(
        logical_source_id == action["logical_source_id"],
        "SOURCE_DISAGREEMENT",
        "logical source differs from the action target",
    )
    _need(
        contract["observation_type"] == OBSERVATION_TYPE
        and contract["observer_implementation_hash"] == IMPLEMENTATION_IDENTITY
        and len(contract["source_record_ids"]) == 1,
        "UNSUPPORTED_IMPLEMENTATION",
        "outcome contract does not name this observer",
    )
    implementation = _record(replay, contract["source_record_ids"][0], "SourceArtifact")
    _need(
        implementation["source_content_digest"] == IMPLEMENTATION_IDENTITY
        and replay.retained_bytes(implementation["id"]) == IMPLEMENTATION_BYTES,
        "UNSUPPORTED_IMPLEMENTATION",
        "retained observer bytes differ from the loaded implementation",
    )
    _need(
        isinstance(source_path, Path) and source_path.is_absolute(),
        "MALFORMED_INPUT",
        "explicit absolute controlled source path required",
    )
    _need(
        not source_path.is_symlink() and source_path.is_file(),
        "CAPTURE_UNAVAILABLE",
        "existing nonsymlink regular source required",
    )
    _need(
        hasattr(os, "O_NOFOLLOW"), "UNSUPPORTED", "no-follow source capture is required"
    )
    content = _capture(source_path)
    outcome = _classify(content, action)
    source, source_event = _source_event(
        observed_source_id,
        content,
        "application/x-ndjson",
        "urn:controlled:" + logical_source_id,
        [execution_id, outcome_contract_id],
        observer_id,
        observed_at,
        artifact_version,
    )
    observation = make_record(
        "OutcomeObservation",
        id=observation_id,
        event_id="event:" + observation_id,
        generated_at=observed_at,
        actor_id=observer_id,
        role="outcome-observer",
        source_record_ids=[execution_id, outcome_contract_id, observed_source_id],
        execution_id=execution_id,
        execution_hash=execution["content_hash"],
        outcome_contract_id=outcome_contract_id,
        outcome_contract_hash=contract["content_hash"],
        observer_id=observer_id,
        observation_type=OBSERVATION_TYPE,
        observation_result=outcome,
        observed_at=observed_at,
        observed_source_artifact_id=observed_source_id,
        observed_source_artifact_hash=source["content_hash"],
    )
    event = _event("OutcomeObservation", observation, "OUTCOME_OBSERVED")
    after_source = _append(history, replay, "source", source_event)
    return _append(history, after_source, "observation", event)


# Source identity is loaded before any capture, not inferred from an outcome.
# Installed Core/Python and trusted-process execution remain explicit limits.
IMPLEMENTATION_BYTES = Path(__file__).read_bytes()
IMPLEMENTATION_IDENTITY = _digest(IMPLEMENTATION_BYTES)
