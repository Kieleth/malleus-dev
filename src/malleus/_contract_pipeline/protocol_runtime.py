"""Private finite-program attachment to the owning knowledge history.

No writer, graph mutation, check producer or arbitrary callback runs here.
The owner supplies verified envelopes and derives the domain coordinates.
"""

from base64 import b64decode, b64encode
from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json

from .finite_executor import (
    ExecutionRefusal,
    execute_program,
    validate_instruction_schema,
    _contract_view,
)
from .finite_program import PacketRefusal, validate_program
from malleus.ledger import GENESIS, canonical_json, content_digest


SELECTION_EVENT = "FINITE_PROTOCOL_SELECTED"
PROGRAM_EVENT = "FINITE_PROTOCOL_EVENT"
BUNDLE_GRAMMAR = "malleus.finite-protocol-bundle/private-v0"
_DRAFT_FIELDS = {
    "event_id",
    "event_type",
    "actor_id",
    "transaction_time",
    "data",
    "retained",
}
_PAYLOAD_FIELDS = {
    "bundle_identity",
    "transaction",
    "transaction_identity",
    "ordinal",
    "expected_head",
    "expected_count",
    "data",
    "retained",
    "logical_event_type",
}


class ProtocolProgramRefusal(ValueError):
    def __init__(self, reason, detail):
        self.reason, self.detail = reason, detail
        super().__init__(f"{reason}: {detail}")


def refuse(detail, reason="PROTOCOL_PROGRAM_REFUSAL"):
    raise ProtocolProgramRefusal(reason, detail)


def canonical(value):
    return canonical_json(value).encode()


def digest(source):
    return "sha256:" + sha256(source).hexdigest()


def closed(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        refuse(f"expected exact fields: {sorted(fields)}")


def text(value):
    if type(value) is not str or not value.strip():
        refuse("explicit nonblank string required")
    return value


def decode(source):
    try:
        if type(source) is not bytes:
            refuse("exact canonical bytes required")
        value = json.loads(source)
        if canonical(value) != source:
            refuse("noncanonical program bytes")
        return value
    except (ValueError, TypeError) as error:
        if isinstance(error, ProtocolProgramRefusal):
            raise
        raise ProtocolProgramRefusal("MALFORMED_PROGRAM", str(error)) from error


def raw(value):
    try:
        if type(value) is not str:
            refuse("base64 bytes required")
        return b64decode(value.encode("ascii"), validate=True)
    except (UnicodeError, ValueError) as error:
        raise ProtocolProgramRefusal("MALFORMED_PROGRAM", str(error)) from error


def load_bundle(source):
    bundle = decode(source)
    closed(
        bundle,
        {
            "grammar",
            "record_contract_base64",
            "instruction_schema",
            "profile",
            "constants",
            "transactions",
        },
    )
    if bundle["grammar"] != BUNDLE_GRAMMAR:
        refuse("unsupported finite protocol grammar")
    try:
        validate_instruction_schema(bundle["instruction_schema"])
        _contract_view(raw(bundle["record_contract_base64"]))
        if type(bundle["transactions"]) is not dict or not bundle["transactions"]:
            refuse("nonempty transaction declarations required")
        if type(bundle["constants"]) is not dict:
            refuse("explicit constant object required")
        for name, transaction in bundle["transactions"].items():
            text(name)
            closed(transaction, {"event_types", "program"})
            kinds = transaction["event_types"]
            if type(kinds) is not list or not kinds:
                refuse("ordered logical event types required")
            for kind in kinds:
                text(kind)
            program = transaction["program"]
            validate_program(
                program,
                profile=bundle["profile"],
                instruction_schema=bundle["instruction_schema"],
            )
            bindings = program["inputs"]
            if (
                set(bindings) != {"event", "current", "artifact"}
                or set(bindings["event"]) != {str(i) for i in range(len(kinds))}
                or set(bindings["current"]) not in ({"context"}, {"context", "state"})
                or set(bindings["artifact"])
                not in ({"constants"}, {"constants", "selection"})
            ):
                refuse("program requires the fixed owner input frame")
    except (KeyError, TypeError, ValueError, PacketRefusal) as error:
        if isinstance(error, ProtocolProgramRefusal):
            raise
        raise ProtocolProgramRefusal("MALFORMED_PROGRAM", str(error)) from error
    return bundle


@dataclass(frozen=True)
class ProtocolReplay:
    canonical_bytes: bytes

    @property
    def identity(self):
        return digest(self.canonical_bytes)

    @property
    def data(self):
        return json.loads(self.canonical_bytes)


def _base(expected_head, expected_count):
    text(expected_head)
    if type(expected_count) is not int or expected_count < 0:
        refuse("exact nonnegative expected event count required")


def selection_entry(
    *,
    record_id,
    identity,
    expected_head,
    expected_count,
    event_id,
    actor_id,
    transaction_time,
):
    _base(expected_head, expected_count)
    return {
        "event_id": event_id,
        "event_type": SELECTION_EVENT,
        "actor_id": actor_id,
        "transaction_time": transaction_time,
        "payload": {
            "record_id": text(record_id),
            "identity": text(identity),
            "expected_head": expected_head,
            "expected_count": expected_count,
        },
    }


def transaction_entries(
    *, bundle_identity, transaction, events, expected_head, expected_count
):
    _base(expected_head, expected_count)
    if type(events) is not tuple or not events:
        refuse("nonempty ordered event tuple required")
    drafts = deepcopy(events)
    for event in drafts:
        closed(event, _DRAFT_FIELDS)
        if type(event["data"]) is not dict or type(event["retained"]) is not dict:
            refuse("explicit event data and retention maps required")
        for name, value in event["retained"].items():
            text(name)
            closed(value, {"record_id", "content", "media_type", "role", "encoding"})
            text(value["record_id"])
            if type(value["content"]) is not bytes:
                refuse("retention input requires exact bytes")
            value["content_base64"] = b64encode(value.pop("content")).decode("ascii")
    identity = content_digest(
        {
            "bundle_identity": bundle_identity,
            "transaction": transaction,
            "expected_head": expected_head,
            "expected_count": expected_count,
            "events": drafts,
        }
    )
    return tuple(
        {
            "event_id": event["event_id"],
            "event_type": PROGRAM_EVENT,
            "actor_id": event["actor_id"],
            "transaction_time": event["transaction_time"],
            "payload": {
                "bundle_identity": bundle_identity,
                "transaction": transaction,
                "transaction_identity": identity,
                "ordinal": ordinal,
                "expected_head": expected_head,
                "expected_count": expected_count,
                "data": event["data"],
                "retained": event["retained"],
                "logical_event_type": event["event_type"],
            },
        }
        for ordinal, event in enumerate(drafts)
    )


class ProtocolFold:
    """Ephemeral fold state owned exclusively by one verified replay traversal."""

    def __init__(self):
        self.bundle = None
        self.bundle_identity = None
        self.state = {"protocol": {}, "action_acceptance_head": GENESIS}
        self.records = {}
        self.receipts = []
        self.pending = []
        self.context = None

    def snapshot(self):
        if self.bundle is None:
            return None
        if self.pending:
            refuse("incomplete logical transaction")
        return ProtocolReplay(
            canonical(
                {
                    "bundle_identity": self.bundle_identity,
                    "state": self.state,
                    "records": self.records,
                    "receipts": self.receipts,
                }
            )
        )

    def select(self, event, retained):
        if self.bundle is not None:
            refuse("finite program set already selected")
        payload = event["payload"]
        closed(payload, {"record_id", "identity", "expected_head", "expected_count"})
        self._expected(event, payload)
        member = retained.get(payload["record_id"])
        if (
            member is None
            or member.role != "RETAINED_EVIDENCE"
            or member.identity != payload["identity"]
        ):
            refuse("selected exact program set is not retained evidence")
        self.bundle = load_bundle(member.content)
        self.bundle_identity = member.identity

    @staticmethod
    def _expected(event, payload):
        _base(payload["expected_head"], payload["expected_count"])
        if (
            payload["expected_head"] != event["previous_event_hash"]
            or payload["expected_count"] != event["sequence"] - 1
        ):
            refuse("stale full ledger head/count", "STALE_PROTOCOL_BASE")

    def consume(self, event, *, context, reserved_ids, history_binding_identity):
        if self.bundle is None:
            refuse("finite program set is not selected")
        payload = event["payload"]
        closed(payload, _PAYLOAD_FIELDS)
        name = payload["transaction"]
        if type(name) is not str or name not in self.bundle["transactions"]:
            refuse("transaction is not declared")
        transaction = self.bundle["transactions"][name]
        if (
            payload["bundle_identity"] != self.bundle_identity
            or type(payload["ordinal"]) is not int
            or payload["ordinal"] != len(self.pending)
            or len(self.pending) >= len(transaction["event_types"])
            or payload["logical_event_type"]
            != transaction["event_types"][len(self.pending)]
        ):
            refuse("logical transaction sequence differs from selected program")
        if not self.pending:
            self._expected(event, payload)
            self.context = deepcopy(context)
        else:
            first = self.pending[0]["payload"]
            if any(
                payload[k] != first[k]
                for k in (
                    "transaction",
                    "transaction_identity",
                    "expected_head",
                    "expected_count",
                )
            ):
                refuse("logical events do not belong to the same transaction")
        self.pending.append(deepcopy(event))
        if len(self.pending) != len(transaction["event_types"]):
            return ()
        frames, encoded_drafts, retained = {}, [], {}
        for index, member in enumerate(self.pending):
            data = member["payload"]
            if type(data["retained"]) is not dict or type(data["data"]) is not dict:
                refuse("explicit data and retention objects required")
            metadata = {}
            for name, binding in data["retained"].items():
                text(name)
                closed(
                    binding,
                    {"record_id", "content_base64", "media_type", "role", "encoding"},
                )
                identifier = text(binding["record_id"])
                if (
                    identifier in reserved_ids
                    or identifier in self.records
                    or identifier in retained
                ):
                    refuse("retained record ID is reused")
                content = raw(binding["content_base64"])
                if binding["role"] not in {
                    "RETAINED_EVIDENCE",
                    "RETAINED_SOURCE",
                    "SOURCE_ARTIFACT",
                }:
                    refuse("unsupported retained role")
                encoding = binding["encoding"]
                if encoding not in {"BYTES", "CANONICAL_JSON"}:
                    refuse("explicit supported retention encoding required")
                metadata[name] = {
                    "record_id": identifier,
                    "identity": digest(content),
                    "byte_length": len(content),
                    "media_type": text(binding["media_type"]),
                    "role": binding["role"],
                    "encoding": encoding,
                }
                if encoding == "CANONICAL_JSON":
                    metadata[name]["value"] = decode(content)
                retained[identifier] = (
                    identifier,
                    content,
                    digest(content),
                    binding["media_type"],
                    binding["role"],
                )
            header = {
                k: member[k]
                for k in (
                    "event_id",
                    "actor_id",
                    "transaction_time",
                    "sequence",
                    "previous_event_hash",
                    "event_hash",
                )
            }
            frames[str(index)] = {
                "header": header,
                "data": data["data"],
                "retained": metadata,
            }
            encoded_drafts.append(
                {
                    **{
                        k: header[k]
                        for k in ("event_id", "actor_id", "transaction_time")
                    },
                    "event_type": data["logical_event_type"],
                    "data": data["data"],
                    "retained": data["retained"],
                }
            )
        preimage = {
            k: payload[k]
            for k in (
                "bundle_identity",
                "transaction",
                "expected_head",
                "expected_count",
            )
        }
        if (
            content_digest({**preimage, "events": encoded_drafts})
            != payload["transaction_identity"]
        ):
            refuse("transaction identity differs from exact event drafts")
        artifacts = {"constants": {"value": self.bundle["constants"]}}
        if "selection" in transaction["program"]["inputs"]["artifact"]:
            artifacts["selection"] = {
                "value": {
                    "bundle_identity": self.bundle_identity,
                    "record_contract_identity": digest(
                        raw(self.bundle["record_contract_base64"])
                    ),
                    "profile_identity": content_digest(self.bundle["profile"]),
                    "instruction_schema_identity": content_digest(
                        self.bundle["instruction_schema"]
                    ),
                    "history_binding_identity": history_binding_identity,
                }
            }
        current = {"context": {"value": self.context}}
        if "state" in transaction["program"]["inputs"]["current"]:
            current["state"] = {"value": deepcopy(self.state)}
        try:
            execution = execute_program(
                program=transaction["program"],
                profile=self.bundle["profile"],
                instruction_schema=self.bundle["instruction_schema"],
                inputs={
                    "event": frames,
                    "current": current,
                    "artifact": artifacts,
                },
                applied_records=self.records,
                state=self.state,
                record_contract_bytes=raw(self.bundle["record_contract_base64"]),
            ).data
        except ExecutionRefusal as error:
            raise ProtocolProgramRefusal(error.reason, error.detail) from error
        introduced = {w["record"]["id"]: w for w in execution["introductions"]}
        if set(introduced) & (set(reserved_ids) | self.records.keys()):
            refuse("introduced ID collides with history namespace")
        if retained.keys() - introduced.keys():
            refuse("retained bytes lack an introduction in their transaction")
        self.records.update(introduced)
        self.state = execution["state"]
        self.receipts.append(
            {
                "transaction_identity": payload["transaction_identity"],
                "program_identity": execution["program_identity"],
                "first_sequence": self.pending[0]["sequence"],
                "last_sequence": event["sequence"],
                "last_event_hash": event["event_hash"],
            }
        )
        self.pending = []
        self.context = None
        return tuple(retained.values())
