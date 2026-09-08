"""Freeze public Core replay into graph-free inputs; consistency, not authority."""

from dataclasses import dataclass
from hashlib import sha256
import json

from malleus import KnowledgeGraph
import malleus.compiler as api
from malleus.ledger import GENESIS


class AcceptedViewRefusal(ValueError):
    def __init__(self, reason, detail):
        self.reason = reason
        super().__init__(detail)


def _require(condition, reason, detail):
    if not condition:
        raise AcceptedViewRefusal(reason, detail)


def _canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def _digest(content):
    _require(type(content) is bytes, "MALFORMED_INPUT", "exact bytes required")
    return "sha256:" + sha256(content).hexdigest()


def _object(content):
    _digest(content)
    data = json.loads(content)
    _require(
        type(data) is dict and _canonical(data) == content,
        "MALFORMED_INPUT",
        "canonical JSON object required",
    )
    return data


@dataclass(frozen=True, slots=True)
class AcceptedReadView:
    context: api.KnowledgeChangeContext
    contract_view: api.ContractView
    receipt_bytes: bytes
    records_bytes: bytes
    protocol_bytes: bytes
    accepted_change_sets: tuple[api.KnowledgeChangeSet, ...]
    record_history: tuple[tuple[str, api.KnowledgeRecordHistory], ...]

    @property
    def receipt_identity(self):
        return self.context.receipt_identity

    @property
    def records(self):
        return json.loads(self.records_bytes)

    @property
    def protocol(self):
        return json.loads(self.protocol_bytes)

    @property
    def receipt(self):
        return json.loads(self.receipt_bytes)


def freeze_accepted_replay(*, replay, context):
    """Read a caller's actual Core replay/context; never retain the graph handle.

    Obtain both inputs from the owning history. Arbitrary Python constructors
    are not authenticated checkpoints. A later proposal still checks fresh L.
    """
    try:
        return _freeze(replay, context)
    except AcceptedViewRefusal:
        raise
    except (ValueError, TypeError, KeyError, AttributeError, RecursionError) as error:
        raise AcceptedViewRefusal("MALFORMED_INPUT", str(error)) from error


def _freeze(replay, context):
    _require(
        type(replay) is api.KnowledgeHistoryReplay
        and type(context) is api.KnowledgeChangeContext,
        "MALFORMED_INPUT",
        "public Core replay and composition context required",
    )
    _require(
        replay.protocol_replay is not None,
        "MALFORMED_INPUT",
        "selected action attachment is required",
    )
    _require(
        type(replay.contract_view) is api.ContractView,
        "MALFORMED_INPUT",
        "immutable compiled domain contract required",
    )
    _require(
        type(context.base_ledger_event_count) is int,
        "MALFORMED_INPUT",
        "ledger event count must be an integer",
    )

    coordinates = {
        "base_ledger_head": replay.ledger_head,
        "base_ledger_event_count": replay.ledger_event_count,
        "base_acceptance_head": replay.acceptance_head,
        "base_materialization_head": replay.materialization_head,
        "base_accepted_state_digest": replay.graph.state_digest(),
        "contract_identity": replay.partial_contract.identity,
        "receipt_identity": replay.receipt.identity,
    }
    _require(
        all(getattr(context, name) == value for name, value in coordinates.items()),
        "STALE_BASE",
        "Core replay and composition context differ",
    )

    _require(
        _digest(replay.receipt.canonical_bytes) == context.receipt_identity,
        "STALE_BASE",
        "receipt bytes differ from Core's receipt identity",
    )
    receipt = _object(replay.receipt.canonical_bytes)
    _require(
        all(
            receipt[name] == value
            for name, value in {
                "ledger_head": context.base_ledger_head,
                "ledger_event_count": context.base_ledger_event_count,
                "contract_identity": context.contract_identity,
                "graph_state_digest": context.base_accepted_state_digest,
            }.items()
        ),
        "STALE_BASE",
        "receipt and accepted coordinates differ",
    )

    protocol_bytes = replay.protocol_replay.canonical_bytes
    _require(
        _digest(protocol_bytes) == receipt["protocol_replay_identity"],
        "STALE_BASE",
        "protocol bytes differ from the accepted receipt",
    )
    _object(protocol_bytes)

    records_bytes = _canonical(replay.graph.export_records())
    projection = KnowledgeGraph.from_records(
        replay.contract_view, _object(records_bytes)
    )
    _require(
        projection.state_digest() == context.base_accepted_state_digest,
        "STALE_BASE",
        "exported graph differs from the accepted state",
    )

    _require(
        type(context.retained_inputs) is tuple,
        "MALFORMED_INPUT",
        "immutable retained inputs required",
    )
    expected = tuple(sorted(replay.retained_inputs, key=lambda item: item.record_id))
    _require(
        context.retained_inputs == expected,
        "STALE_BASE",
        "retained inputs differ from the owning replay",
    )
    identifiers = []
    for item in context.retained_inputs:
        _require(
            type(item) is api.KnowledgeRetainedInput
            and all(
                type(value) is str and bool(value)
                for value in (item.record_id, item.identity, item.media_type, item.role)
            ),
            "MALFORMED_INPUT",
            "typed retained input with explicit metadata required",
        )
        _require(
            _digest(item.content) == item.identity,
            "MALFORMED_INPUT",
            "retained content does not match its identity",
        )
        identifiers.append(item.record_id)
    _require(
        len(identifiers) == len(set(identifiers)),
        "MALFORMED_INPUT",
        "duplicate retained identity",
    )

    changes, record_history = _accepted_lineage(replay, receipt, _object(records_bytes))
    return AcceptedReadView(
        context,
        replay.contract_view,
        replay.receipt.canonical_bytes,
        records_bytes,
        protocol_bytes,
        changes,
        record_history,
    )


def _accepted_lineage(replay, receipt, records):
    """Cross-check public accepted values, not replay or admit their operations."""
    _require(
        type(replay.change_sets) is tuple,
        "MALFORMED_INPUT",
        "accepted KCS tuple required",
    )
    changes = []
    for value in replay.change_sets:
        _require(
            type(value) is api.KnowledgeChangeSet,
            "MALFORMED_INPUT",
            "typed accepted KCS required",
        )
        parsed = api.KnowledgeChangeSet.from_bytes(value.canonical_bytes)
        _require(
            parsed == value,
            "STALE_BASE",
            "accepted KCS value differs from canonical bytes",
        )
        changes.append(parsed)
    _require(
        len({c.change_set_id for c in changes}) == len(changes)
        and len({c.identity for c in changes}) == len(changes),
        "STALE_BASE",
        "duplicate accepted change identity",
    )
    field = replay.binding.data["proposal"]["change_set_identity_field"]
    _require(
        receipt[field] == (changes[-1].identity if changes else GENESIS),
        "STALE_BASE",
        "accepted KCS order differs from the replay receipt",
    )
    operations = {}
    for change in changes:
        for operation in change.operations:
            _require(
                operation.record_id not in operations,
                "STALE_BASE",
                "duplicate historical record ID",
            )
            operations[operation.record_id] = change, operation
    history = replay.record_history
    _require(
        set(history) == set(operations),
        "STALE_BASE",
        "accepted operations and record history differ",
    )
    result = []
    for identifier, member in sorted(history.items()):
        _require(
            type(member) is api.KnowledgeRecordHistory,
            "MALFORMED_INPUT",
            "typed record history required",
        )
        change, operation = operations[identifier]
        _require(
            member.change_set_id == change.change_set_id
            and member.operation == operation
            and member.valid_from == change.valid_time
            and member.supersedes_record_id == operation.supersedes_record_id,
            "STALE_BASE",
            "record history differs from its accepted KCS operation",
        )
        valid_to = None
        if member.superseded_by is not None:
            _require(
                member.superseded_by in history
                and history[member.superseded_by].supersedes_record_id == identifier,
                "STALE_BASE",
                "record successor link is not reciprocal",
            )
            valid_to = operations[member.superseded_by][0].valid_time
        if member.supersedes_record_id is not None:
            _require(
                member.supersedes_record_id in history
                and history[member.supersedes_record_id].superseded_by == identifier,
                "STALE_BASE",
                "record predecessor link is not reciprocal",
            )
        _require(
            member.valid_to == valid_to,
            "STALE_BASE",
            "record validity interval differs from successor",
        )
        result.append(
            (
                identifier,
                api.KnowledgeRecordHistory(
                    operation=operation,
                    change_set_id=change.change_set_id,
                    valid_from=change.valid_time,
                    valid_to=valid_to,
                    supersedes_record_id=operation.supersedes_record_id,
                    superseded_by=member.superseded_by,
                ),
            )
        )
    active = {
        identifier for identifier, member in result if member.superseded_by is None
    }
    exported = {member["id"] for family in records.values() for member in family}
    _require(
        active == exported,
        "STALE_BASE",
        "active record history differs from graph exports",
    )
    return tuple(changes), tuple(result)
