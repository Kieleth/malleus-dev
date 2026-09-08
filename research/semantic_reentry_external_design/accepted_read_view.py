"""Freeze public Core replay into graph-free inputs; consistency, not authority."""

from dataclasses import dataclass
from hashlib import sha256
import json

from malleus import KnowledgeGraph
import malleus.compiler as api


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

    return AcceptedReadView(
        context,
        replay.contract_view,
        replay.receipt.canonical_bytes,
        records_bytes,
        protocol_bytes,
    )
