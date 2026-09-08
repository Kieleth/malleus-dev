"""One fresh Core dispatch, one controlled file attempt, one terminal receipt."""

from functools import wraps
from hashlib import sha256
import json
import os
from pathlib import Path
import stat

import malleus.compiler as core
from malleus.assent import make_record
from malleus.ledger import aware_datetime, canonical_json, content_digest, record_hash


class SupplierExecutionError(ValueError):
    def __init__(self, reason, detail):
        self.reason, self.detail = reason, detail
        super().__init__(f"{reason}: {detail}")


def _guarded(function):
    @wraps(function)
    def invoke(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (TypeError, KeyError, AttributeError, RecursionError) as error:
            raise SupplierExecutionError("MALFORMED_INPUT", str(error)) from error

    return invoke


def _need(condition, reason, detail):
    if not condition:
        raise SupplierExecutionError(reason, detail)


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
        raise SupplierExecutionError("MALFORMED_INPUT", str(error)) from error


def _digest(content):
    return "sha256:" + sha256(content).hexdigest()


def _object(content):
    _need(type(content) is bytes, "MALFORMED_INPUT", "exact canonical bytes required")
    try:
        value = json.loads(content)
    except ValueError as error:
        raise SupplierExecutionError("MALFORMED_INPUT", str(error)) from error
    _need(
        type(value) is dict and _canonical(value) == content,
        "MALFORMED_INPUT",
        "canonical JSON object required",
    )
    return value


def _instant(value):
    try:
        return aware_datetime(value, "supplier execution time")
    except ValueError as error:
        raise SupplierExecutionError("MALFORMED_INPUT", str(error)) from error


def _record(replay, identifier, kind):
    entry = replay.protocol_replay.data["records"][identifier]
    value = entry["record"]
    _need(
        entry["record_type"] == kind
        and value["id"] == identifier
        and record_hash(kind, value) == value["content_hash"],
        "MALFORMED_INPUT",
        "wrong record kind or identity: " + identifier,
    )
    return value


def _source(replay, identifier):
    value = _record(replay, identifier, "SourceArtifact")
    content = replay.retained_bytes(identifier)
    _need(
        _digest(content) == value["source_content_digest"]
        and len(content) == value["source_byte_length"],
        "MALFORMED_INPUT",
        "retained source bytes differ",
    )
    return value, content


def _row(content):
    _need(
        type(content) is bytes and content.endswith(b"\n"),
        "UNSUPPORTED_SOURCE",
        "canonical one-row JSONL required",
    )
    row = _object(content[:-1])
    _need(
        set(row) == {"event_id", "supplier_order_id", "product_code", "quantity"},
        "UNSUPPORTED_SOURCE",
        "closed supplier row required",
    )
    _text(row["event_id"], row["supplier_order_id"], row["product_code"])
    _need(
        type(row["quantity"]) is int,
        "UNSUPPORTED_SOURCE",
        "integer source quantity required",
    )
    return row


def _write_source(stream, content):
    stream.seek(0)
    written = stream.write(content)
    if written != len(content):
        raise OSError("incomplete controlled supplier write")
    stream.truncate()
    stream.flush()
    os.fsync(stream.fileno())


def _attempt(source_path, action):
    try:
        descriptor = os.open(source_path, os.O_RDWR | os.O_NOFOLLOW)
        with os.fdopen(descriptor, "r+b") as stream:
            _need(
                stat.S_ISREG(os.fstat(stream.fileno()).st_mode),
                "UNSUPPORTED_SOURCE",
                "regular controlled source file required",
            )
            before = stream.read()
            _need(
                _digest(before) == action["expected_source_digest"],
                "STALE_SOURCE",
                "actual source differs from accepted pre-state",
            )
            row = _row(before)
            _need(
                row["quantity"] == action["expected_quantity"]
                and all(
                    row[f] == action[f] for f in ("supplier_order_id", "product_code")
                ),
                "SOURCE_DISAGREEMENT",
                "actual source differs from the authorized target",
            )
            after = (
                _canonical(
                    {
                        **row,
                        "quantity": action["requested_quantity"],
                        "event_id": action["new_source_occurrence_id"],
                    }
                )
                + b"\n"
            )
            _write_source(stream, after)
        result = {
            "status": "SUCCEEDED",
            "reason": "WRITE_COMPLETED",
            "detail": "The write operation completed; no independent observation is asserted.",
        }
    except SupplierExecutionError as error:
        result = {"status": "ABORTED", "reason": error.reason, "detail": error.detail}
    except OSError as error:
        result = {"status": "FAILED", "reason": "SOURCE_IO_ERROR", "detail": str(error)}
    return _canonical(result)


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


@_guarded
def dispatch_and_execute_supplier(
    *,
    history,
    expected_head,
    expected_count,
    original_context_id,
    current_context_id,
    action_id,
    authorization_id,
    executor_implementation_id,
    executor_id,
    dispatcher_id,
    dispatch_id,
    execution_id,
    dispatched_at,
    execution_started_at,
    execution_ended_at,
    source_path,
    logical_source_id,
):
    """Only a newly admitted dispatch reaches the private source attempt."""
    _need(
        type(history) is core.KnowledgeChangeHistory,
        "MALFORMED_INPUT",
        "actual owning Core history required",
    )
    _text(
        expected_head,
        original_context_id,
        current_context_id,
        action_id,
        authorization_id,
        executor_implementation_id,
        executor_id,
        dispatcher_id,
        dispatch_id,
        execution_id,
        logical_source_id,
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
        "UNSUPPORTED",
        "selected action attachment required",
    )
    _need(
        _instant(dispatched_at)
        <= _instant(execution_started_at)
        < _instant(execution_ended_at),
        "MALFORMED_INPUT",
        "dispatch/start/end interval is invalid",
    )
    _need(
        isinstance(source_path, Path) and source_path.is_absolute(),
        "MALFORMED_INPUT",
        "explicit absolute controlled source path required",
    )
    _need(
        not source_path.is_symlink() and source_path.is_file(),
        "UNSUPPORTED_SOURCE",
        "existing nonsymlink regular source file required",
    )
    _need(hasattr(os, "O_NOFOLLOW"), "UNSUPPORTED", "no-follow file open is required")
    records = replay.protocol_replay.data["records"]
    used = set(records) | {item.record_id for item in replay.retained_inputs}
    _need(
        dispatch_id != execution_id
        and not {dispatch_id, execution_id}.intersection(used),
        "DUPLICATE_OUTPUT",
        "fresh distinct dispatch/execution IDs required",
    )
    event_ids = {item["record"]["generation_event_id"] for item in records.values()}
    _need(
        not {"event:" + dispatch_id, "event:" + execution_id}.intersection(event_ids),
        "DUPLICATE_OUTPUT",
        "fresh dispatch/execution event IDs required",
    )
    implementation, content = _source(replay, executor_implementation_id)
    _need(
        content == IMPLEMENTATION_BYTES
        and implementation["source_content_digest"] == IMPLEMENTATION_IDENTITY,
        "UNSUPPORTED_IMPLEMENTATION",
        "retained bytes do not identify this loaded executor",
    )
    action = _record(replay, action_id, "SupplierOrderAmendment")
    permission = _record(replay, authorization_id, "AuthorizationDecision")
    context_record, current_bytes = _source(replay, current_context_id)
    current = _object(current_bytes)
    _, original_bytes = _source(replay, original_context_id)
    original = _object(original_bytes)
    protocol = replay.protocol_replay.data["state"]["protocol"]
    _need(
        original["action_id"] == action_id
        and {"keys": [original["proposal_id"]], "value": original_context_id}
        in protocol["context_by_proposal"]
        and {"keys": [original["proposal_id"]], "value": "ACCEPTED"}
        in protocol["proposal_states"],
        "NOT_ACCEPTED",
        "the action requires its applied original context and proposal ACCEPT",
    )
    _, goal_bytes = _source(replay, original["goal"]["id"])
    goal = _object(goal_bytes)
    _, before = _source(replay, original["pre_state_source"]["id"])
    row = _row(before)
    _need(
        set(goal)
        == {"kind", "supplier_order_id", "product_code", "operator", "quantity"}
        and goal["kind"] == "GoalPredicate"
        and goal["operator"] == "EQUALS"
        and type(goal["quantity"]) is int
        and goal["quantity"] == 2,
        "UNSUPPORTED",
        "retained exact-two supplier goal required",
    )
    payload = {
        field: action[field]
        for field in (
            "logical_source_id",
            "supplier_order_id",
            "product_code",
            "expected_quantity",
            "requested_quantity",
            "expected_source_digest",
            "new_source_occurrence_id",
        )
    }
    _need(
        content_digest(payload) == action["action_payload_hash"],
        "MALFORMED_INPUT",
        "action payload hash differs",
    )
    _need(
        action["action_type"] == "AMEND_SUPPLIER_ORDER"
        and type(action["expected_quantity"]) is int
        and action["expected_quantity"] == row["quantity"] == 1
        and type(action["requested_quantity"]) is int
        and action["requested_quantity"] == 2
        and all(
            action[f] == row[f] == goal[f]
            for f in ("supplier_order_id", "product_code")
        ),
        "UNSUPPORTED",
        "only the bound supplier 1-to-2 amendment is supported",
    )
    _text(action["new_source_occurrence_id"])
    _need(
        action["new_source_occurrence_id"] != row["event_id"],
        "UNSUPPORTED",
        "a distinct source occurrence is required",
    )
    _need(
        action["logical_source_id"] == logical_source_id
        and replay.retained_bytes(logical_source_id) == before
        and action["expected_source_digest"] == _digest(before),
        "SOURCE_DISAGREEMENT",
        "logical source and exact accepted pre-state must agree",
    )
    dispatch = make_record(
        "ActionDispatch",
        id=dispatch_id,
        event_id="event:" + dispatch_id,
        generated_at=dispatched_at,
        actor_id=dispatcher_id,
        role="dispatcher",
        source_record_ids=[action_id, authorization_id],
        action_proposal_id=action_id,
        action_content_hash=action["content_hash"],
        authorization_decision_id=authorization_id,
        authorization_decision_hash=permission["content_hash"],
        executor_id=executor_id,
        dispatch_adapter_id=executor_implementation_id,
        base_acceptance_head=replay.protocol_replay.data["state"][
            "action_acceptance_head"
        ],
        dispatched_at=dispatched_at,
    )
    event = _event("ActionDispatch", dispatch, "ACTION_DISPATCHED")
    event["data"]["context"] = {
        "id": current_context_id,
        "record_hash": context_record["content_hash"],
        "value": current,
    }
    after_dispatch = history.append_protocol_events(
        transaction="dispatch",
        events=(event,),
        expected_head=expected_head,
        expected_count=expected_count,
    )
    # No replay-only or already-dispatched resume branch reaches this point.
    result_bytes = _attempt(source_path, action)
    result = _object(result_bytes)
    execution = make_record(
        "ActionExecution",
        id=execution_id,
        event_id="event:" + execution_id,
        generated_at=execution_ended_at,
        actor_id=executor_id,
        role="executor",
        source_record_ids=[dispatch_id],
        dispatch_id=dispatch_id,
        dispatch_hash=dispatch["content_hash"],
        executor_id=executor_id,
        execution_started_at=execution_started_at,
        execution_ended_at=execution_ended_at,
        execution_status=result["status"],
        execution_result_hash=_digest(result_bytes),
    )
    event = _event("ActionExecution", execution, "ACTION_EXECUTED")
    event["retained"]["result"] = {
        "record_id": execution_id,
        "content": result_bytes,
        "media_type": "application/json",
        "role": "RETAINED_EVIDENCE",
        "encoding": "BYTES",
    }
    return history.append_protocol_events(
        transaction="execution",
        events=(event,),
        expected_head=after_dispatch.ledger_head,
        expected_count=after_dispatch.ledger_event_count,
    )


# Capture actual implementation bytes at module load, outside any pure stage.
# This is trusted-process source identity, not an in-memory/OS attestation.
IMPLEMENTATION_BYTES = Path(__file__).read_bytes()
IMPLEMENTATION_IDENTITY = _digest(IMPLEMENTATION_BYTES)
