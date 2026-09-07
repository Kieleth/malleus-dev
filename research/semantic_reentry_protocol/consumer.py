"""Pure, research-local policy for the explicitly mapped Shop correction.

This module makes no KCS and grants no writing authority. Core owns composition.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json
from types import MappingProxyType


class Reason(str, Enum):
    MALFORMED_CONTRACT = "MALFORMED_CONTRACT"
    NONCANONICAL_CONTRACT = "NONCANONICAL_CONTRACT"
    UNSUPPORTED_CONTRACT = "UNSUPPORTED_CONTRACT"
    MALFORMED_INPUT = "MALFORMED_INPUT"
    INPUT_IDENTITY_MISMATCH = "INPUT_IDENTITY_MISMATCH"
    SYNTHESIZER_MISMATCH = "SYNTHESIZER_MISMATCH"
    STALE_BASE = "STALE_BASE"
    UNRETAINED_INPUT = "UNRETAINED_INPUT"
    SOURCE_DISAGREEMENT = "SOURCE_DISAGREEMENT"
    UNSUPPORTED_CHANGE = "UNSUPPORTED_CHANGE"
    PRESERVATION_VIOLATION = "PRESERVATION_VIOLATION"
    AMBIGUOUS = "AMBIGUOUS"
    UNREALIZABLE = "UNREALIZABLE"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    STATE_CONFLICT = "STATE_CONFLICT"


class ReentryRefusal(ValueError):
    def __init__(self, reason: Reason, detail: str):
        self.reason = reason
        super().__init__(detail)


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode()


def digest(content):
    return "sha256:" + sha256(content).hexdigest()


def _freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    return value


def _parse(source):
    if type(source) is not bytes:
        raise ValueError("exact bytes are required")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON field: {key}")
            result[key] = value
        return result

    def invalid(value):
        raise ValueError(f"non-finite JSON value: {value}")

    return json.loads(source, object_pairs_hook=pairs, parse_constant=invalid)


def _exact(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise ValueError(f"required fields: {', '.join(sorted(fields))}")


def _text(value):
    if type(value) is not str or not value:
        raise ValueError("a nonempty string is required")


def _is_digest(value):
    return (
        type(value) is str
        and value.startswith("sha256:")
        and len(value) == 71
        and all(c in "0123456789abcdef" for c in value[7:])
    )


_BASE = {
    "ledger_head",
    "ledger_event_count",
    "acceptance_head",
    "materialization_head",
    "graph_state_digest",
    "contract_identity",
    "receipt_identity",
}
_REQUEST = {
    "plan_sha256",
    "source_sha256",
    "mapping_sha256",
    "source_id",
    "mapping_id",
    "occurrence_id",
    "prior_record_id",
    "target_record_id",
}
_POLICY = {
    "grammar": "malleus.semantic-reentry.shop-consumer/research-v0",
    "input_kind": "ViewDelta",
    "output_kind": "KnowledgeChangeSet",
    "update_strategy": "EXPLICIT_MAPPING_SUPERSESSION",
    "preservation": "EXACT_COMPLEMENT",
    "ambiguity_strategy": "REFUSE_IF_NOT_UNIQUE",
    "stopping_rule": "EXACT_TARGET_AND_SUPERSESSION",
}


@dataclass(frozen=True, slots=True)
class ReentryContract:
    canonical_bytes: bytes
    identity: str
    data: Mapping

    @classmethod
    def from_bytes(cls, source):
        try:
            root = _parse(source)
            _exact(
                root,
                {
                    *_POLICY,
                    "base",
                    "request",
                    "projection_sha256",
                    "permitted_operations",
                    "candidate_budget",
                    "synthesizer_identity",
                },
            )
            _exact(root["base"], _BASE)
            _exact(root["request"], _REQUEST)
            for key, value in root["base"].items():
                if key == "ledger_event_count":
                    if type(value) is not int or value < 0:
                        raise ValueError("ledger count must be a nonnegative integer")
                elif not _is_digest(value) and not (
                    key in {"ledger_head", "acceptance_head", "materialization_head"}
                    and value == "GENESIS"
                ):
                    raise ValueError(f"invalid base identity: {key}")
            for key, value in root["request"].items():
                _text(value)
                if key.endswith("sha256") and not _is_digest(value):
                    raise ValueError(f"invalid request identity: {key}")
            for key in ("projection_sha256", "synthesizer_identity"):
                if not _is_digest(root[key]):
                    raise ValueError(f"invalid identity: {key}")
            if (
                type(root["candidate_budget"]) is not int
                or root["candidate_budget"] < 0
            ):
                raise ValueError("candidate budget must be a nonnegative integer")
            for key in _POLICY:
                _text(root[key])
            if type(root["permitted_operations"]) is not list:
                raise ValueError("permitted operations must be an explicit list")
        except (ValueError, TypeError, KeyError, UnicodeError) as error:
            raise ReentryRefusal(Reason.MALFORMED_CONTRACT, str(error)) from error
        if canonical(root) != source:
            raise ReentryRefusal(
                Reason.NONCANONICAL_CONTRACT, "contract bytes are not canonical"
            )
        if any(root[key] != value for key, value in _POLICY.items()) or root[
            "permitted_operations"
        ] != ["CREATE_ENTITY"]:
            raise ReentryRefusal(
                Reason.UNSUPPORTED_CONTRACT,
                "this consumer does not implement the declared policy",
            )
        return cls(source, digest(source), _freeze(root))


class Status(str, Enum):
    READY = "READY"
    SATISFIED = "SATISFIED"


@dataclass(frozen=True, slots=True)
class Assessment:
    status: Status
    changed_fields: tuple[str, ...]
    preserved_record_ids: tuple[str, ...]


def _require(condition, reason, detail):
    if not condition:
        raise ReentryRefusal(reason, detail)


def _one(values, label):
    _require(bool(values), Reason.UNREALIZABLE, f"no {label}")
    _require(
        len(values) == 1, Reason.AMBIGUOUS, f"competing {label}; no implicit ranking"
    )
    return values[0]


def _record(operation):
    return {
        "id": operation["record_id"],
        "type": operation["record_type"],
        "properties": operation["properties"],
    }


def _assess(
    contract, view_bytes, plan_bytes, source_bytes, mapping_bytes, synthesizer_identity
):
    root = _parse(contract.canonical_bytes)
    _require(
        synthesizer_identity == root["synthesizer_identity"],
        Reason.SYNTHESIZER_MISMATCH,
        "invoking synthesizer differs from the bound mechanism",
    )
    view = _parse(view_bytes)
    _exact(view, {"coordinates", "records", "record_history", "retained"})
    for field in ("coordinates", "records", "record_history", "retained"):
        if type(view[field]) is not dict:
            raise ValueError(f"projection {field} must be an object")
    if any(type(members) is not list for members in view["records"].values()):
        raise ValueError("projection record families must be arrays")
    _require(
        digest(view_bytes) == root["projection_sha256"]
        and view["coordinates"] == root["base"],
        Reason.STALE_BASE,
        "supplied projection differs from the pinned accepted base",
    )
    request = root["request"]
    for label, content in (
        ("plan", plan_bytes),
        ("source", source_bytes),
        ("mapping", mapping_bytes),
    ):
        _require(
            digest(content) == request[f"{label}_sha256"],
            Reason.INPUT_IDENTITY_MISMATCH,
            f"{label} bytes differ from the contract",
        )
    for label, role in (
        ("source", "RETAINED_SOURCE"),
        ("mapping", "RETAINED_EVIDENCE"),
    ):
        record_id = request[f"{label}_id"]
        _require(
            record_id in view["retained"],
            Reason.UNRETAINED_INPUT,
            f"unretained {label}",
        )
        retained = view["retained"][record_id]
        _require(
            retained == {"role": role, "sha256": request[f"{label}_sha256"]},
            Reason.UNRETAINED_INPUT,
            f"{label} role or identity differs",
        )
    plan, mapping = _parse(plan_bytes), _parse(mapping_bytes)
    _require(
        canonical(plan) == plan_bytes,
        Reason.MALFORMED_INPUT,
        "plan bytes must be canonical",
    )
    _require(
        plan["contract_identity"] == root["base"]["contract_identity"],
        Reason.STALE_BASE,
        "plan effective contract differs",
    )
    _require(
        plan["sources"]
        == [{"source_id": request["source_id"], "sha256": request["source_sha256"]}]
        and plan["evidence"]
        == [
            {"evidence_id": request["mapping_id"], "sha256": request["mapping_sha256"]}
        ],
        Reason.INPUT_IDENTITY_MISMATCH,
        "plan does not bind the selected source and mapping",
    )
    rows = [_parse(line) for line in source_bytes.splitlines()]
    ordinal, row = _one(
        [
            (index, row)
            for index, row in enumerate(rows)
            if row["event_id"] == request["occurrence_id"]
        ],
        "source occurrence",
    )
    selected = _one(
        [
            change
            for change in mapping["changes"]
            if any(
                op["properties"]["source_occurrence_id"] == request["occurrence_id"]
                for op in change["operations"]
            )
        ],
        "explicit mapping change",
    )
    _require(
        len(selected["operations"]) == 1,
        Reason.UNSUPPORTED_CHANGE,
        "one mapped operation is supported",
    )
    op = selected["operations"][0]
    prior_id, target_id = request["prior_record_id"], request["target_record_id"]
    _require(
        op["operation_type"] == "CREATE_ENTITY"
        and op["record_id"] == target_id
        and op["supersedes_record_id"] == prior_id
        and selected["source_record_ordinal"] == ordinal,
        Reason.UNSUPPORTED_CHANGE,
        "mapping does not declare this exact replacement",
    )
    records = plan["records"]
    _require(
        len(records["entities"]) == 1
        and all(
            not members for family, members in records.items() if family != "entities"
        ),
        Reason.PRESERVATION_VIOLATION,
        "request exceeds its one-record replacement footprint",
    )
    record = records["entities"][0]
    bindings = mapping["state_bindings"]
    if type(bindings) is not list:
        raise ValueError("mapping state bindings must be an array")
    targets, sources, derivations = [], [], []
    for binding in bindings:
        path = binding["target_path"]
        _require(
            len(path) == 2 and path[0] == "properties",
            Reason.UNSUPPORTED_CHANGE,
            "unsupported mapping binding",
        )
        field, value = path[1], row[binding["source_field"]]
        targets.append(field)
        sources.append(binding["source_field"])
        derivations.append(
            {
                "record_id": target_id,
                "source_id": request["source_id"],
                "path": path,
                "locator": f"row:{ordinal}:{binding['source_field']}",
            }
        )
        _require(
            canonical(record["properties"][field]) == canonical(value)
            and canonical(op["properties"][field]) == canonical(value),
            Reason.SOURCE_DISAGREEMENT,
            f"source value disagrees at {field}",
        )
    _require(
        len(targets) == len(set(targets))
        and set(targets) == set(op["properties"])
        and len(sources) == len(set(sources))
        and set(sources) == set(row),
        Reason.SOURCE_DISAGREEMENT,
        "mapping must uniquely cover every selected source field and property",
    )
    _require(
        sorted(map(canonical, plan["derivations"]))
        == sorted(map(canonical, derivations)),
        Reason.SOURCE_DISAGREEMENT,
        "plan lineage must exactly identify each selected row and field",
    )
    _require(
        canonical(record) == canonical(_record(op))
        and plan["valid_time"] == selected["valid_time"]
        and plan["supersessions"]
        == [{"record_id": target_id, "supersedes_record_id": prior_id}]
        and plan["history_profile"]["profile_id"] == "state-version"
        and not plan["gaps"],
        Reason.UNSUPPORTED_CHANGE,
        "plan changes the selected record, time or supersession meaning",
    )
    active = {}
    for members in view["records"].values():
        for member in members:
            _require(
                member["id"] not in active,
                Reason.MALFORMED_INPUT,
                "duplicate projection record ID",
            )
            active[member["id"]] = member
    history = view["record_history"]
    preserved = tuple(sorted(set(active) - {prior_id, target_id}))
    if target_id in active:
        _require(
            canonical(active[target_id]) == canonical(record)
            and prior_id not in active
            and history[target_id]["supersedes_record_id"] == prior_id
            and history[target_id]["superseded_by"] is None
            and history[target_id]["valid_from"] == selected["valid_time"]
            and history[prior_id]["superseded_by"] == target_id,
            Reason.STATE_CONFLICT,
            "current target is not the exact requested accepted replacement",
        )
        return Assessment(Status.SATISFIED, (), preserved)
    _require(
        target_id not in history
        and prior_id in active
        and history[prior_id]["superseded_by"] is None,
        Reason.STATE_CONFLICT,
        "requested predecessor is not current or target is historical",
    )
    prior_change = _one(
        [
            change
            for change in mapping["changes"]
            if any(item["record_id"] == prior_id for item in change["operations"])
        ],
        "predecessor mapping",
    )
    prior_op = _one(
        [item for item in prior_change["operations"] if item["record_id"] == prior_id],
        "predecessor operation",
    )
    _require(
        canonical(active[prior_id]) == canonical(_record(prior_op))
        and history[prior_id]["valid_from"] == prior_change["valid_time"],
        Reason.STATE_CONFLICT,
        "accepted predecessor differs from the explicit mapping",
    )
    _require(
        root["candidate_budget"] > 0,
        Reason.BUDGET_EXHAUSTED,
        "no candidate budget remains",
    )
    changed = tuple(
        sorted(
            field
            for field, value in record["properties"].items()
            if canonical(active[prior_id]["properties"][field]) != canonical(value)
        )
    )
    return Assessment(Status.READY, changed, preserved)


def assess_request(
    *,
    contract,
    view_bytes,
    plan_bytes,
    source_bytes,
    mapping_bytes,
    synthesizer_identity,
):
    """Return a local decision only; no writer, graph, callback or ambient I/O."""
    if type(contract) is not ReentryContract:
        raise ReentryRefusal(Reason.MALFORMED_CONTRACT, "a ReentryContract is required")
    if ReentryContract.from_bytes(contract.canonical_bytes) != contract:
        raise ReentryRefusal(
            Reason.MALFORMED_CONTRACT, "contract fields disagree with canonical bytes"
        )
    if any(
        type(value) is not bytes
        for value in (view_bytes, plan_bytes, source_bytes, mapping_bytes)
    ):
        raise ReentryRefusal(
            Reason.MALFORMED_INPUT, "request inputs must be exact bytes"
        )
    try:
        return _assess(
            contract,
            view_bytes,
            plan_bytes,
            source_bytes,
            mapping_bytes,
            synthesizer_identity,
        )
    except ReentryRefusal:
        raise
    except (ValueError, TypeError, KeyError, IndexError, UnicodeError) as error:
        raise ReentryRefusal(
            Reason.MALFORMED_INPUT, f"malformed request input: {error}"
        ) from error
