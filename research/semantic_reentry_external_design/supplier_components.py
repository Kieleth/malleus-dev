"""Research-local pure model and mapper. Neither executes nor observes an action."""

from hashlib import sha256
import json


_SOURCE_FIELDS = {"event_id", "supplier_order_id", "product_code", "quantity"}
_PROPERTY_SOURCES = {
    "source_occurrence_id": "event_id",
    "ordered_quantity": "quantity",
    "product_code": "product_code",
    "supplier_order_id": "supplier_order_id",
}


class SupplierInputError(ValueError):
    """Local component refusal, not an accepted protocol record."""

    def __init__(self, reason: str, detail: str):
        super().__init__(detail)
        self.reason = reason


def _refuse(reason, detail):
    raise SupplierInputError(reason, detail)


def _shape(value, fields, reason):
    if type(value) is not dict or set(value) != set(fields):
        _refuse(reason, f"Expected exactly these fields: {sorted(fields)}")


def _text(value):
    if type(value) is not str or not value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeError:
        return False
    return True


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate source key: {key}")
        result[key] = value
    return result


def _nonfinite(value):
    raise ValueError(f"Non-finite source number: {value}")


def _row(content):
    if type(content) is not bytes:
        _refuse("MALFORMED_INPUT", "Supply source bytes, not a receipt or object")
    try:
        # JSONL frames on LF, not Unicode separators inside JSON strings.
        lines = content.decode("utf-8").removesuffix("\n").split("\n")
        rows = [
            json.loads(line, object_pairs_hook=_unique, parse_constant=_nonfinite)
            for line in lines
        ]
    except (UnicodeError, ValueError, RecursionError) as error:
        raise SupplierInputError(
            "MALFORMED_INPUT", "Source must be UTF-8 JSONL"
        ) from error
    if not rows:
        _refuse("MALFORMED_INPUT", "A source row is required")
    for row in rows:
        _shape(row, _SOURCE_FIELDS, "MALFORMED_INPUT")
        if type(row["quantity"]) is not int or not all(
            _text(row[field]) for field in _SOURCE_FIELDS - {"quantity"}
        ):
            _refuse(
                "MALFORMED_INPUT",
                "Source IDs must be nonempty text and quantity an integer",
            )
    if len(rows) != 1:
        _refuse(
            "AMBIGUOUS",
            "Exactly one source row is permitted; no selection strategy exists",
        )
    return rows[0]


def _canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(content):
    return "sha256:" + sha256(content).hexdigest()


def _policy(goal, operator):
    _shape(
        goal,
        {"kind", "supplier_order_id", "product_code", "operator", "quantity"},
        "UNSUPPORTED_RULE",
    )
    _shape(
        operator,
        {
            "kind",
            "expected_quantity",
            "requested_quantity",
            "new_source_occurrence_id",
            "precondition",
            "changed_fields",
        },
        "UNSUPPORTED_RULE",
    )
    if not (
        goal["kind"] == "GoalPredicate"
        and goal["operator"] == "EQUALS"
        and _text(goal["supplier_order_id"])
        and _text(goal["product_code"])
        and type(goal["quantity"]) is int
        and goal["quantity"] == 2
        and operator["kind"] == "AMEND_SUPPLIER_ORDER"
        and type(operator["expected_quantity"]) is int
        and operator["expected_quantity"] == 1
        and type(operator["requested_quantity"]) is int
        and operator["requested_quantity"] == 2
        and _text(operator["new_source_occurrence_id"])
        and operator["precondition"] == "EXACT_CAPTURED_PRESTATE_BYTES"
        and operator["changed_fields"] == ["event_id", "quantity"]
    ):
        _refuse(
            "UNSUPPORTED_RULE",
            "Only the declared equality-to-two, integer 1 to 2 amendment is supported",
        )


def _before(before_bytes, source_sha256, goal, operator):
    _policy(goal, operator)
    if not (
        type(before_bytes) is bytes
        and type(source_sha256) is str
        and source_sha256.startswith("sha256:")
        and len(source_sha256) == 71
        and all(char in "0123456789abcdef" for char in source_sha256[7:])
    ):
        _refuse(
            "MALFORMED_INPUT",
            "Explicit pre-state bytes and lowercase SHA-256 identity are required",
        )
    if _digest(before_bytes) != source_sha256:
        _refuse(
            "STALE_SOURCE",
            "Pre-state bytes do not match the declared exact source identity",
        )
    row = _row(before_bytes)
    if any(
        row[field] != goal[field] for field in ("supplier_order_id", "product_code")
    ):
        _refuse("UNREALIZABLE", "Source order/product do not match the goal")
    if row["quantity"] == goal["quantity"]:
        return row
    if (
        row["quantity"] != operator["expected_quantity"]
        or row["event_id"] == operator["new_source_occurrence_id"]
    ):
        _refuse(
            "UNREALIZABLE",
            "Source does not permit the declared amendment with a new occurrence",
        )
    return row


def model_amendment(
    before_bytes: bytes, *, source_sha256: str, goal: dict, operator: dict
) -> bytes | None:
    """Predict source bytes under the declared model, never world state."""
    before = _before(before_bytes, source_sha256, goal, operator)
    if before["quantity"] == goal["quantity"]:
        return None
    return (
        _canonical(
            {
                **before,
                "event_id": operator["new_source_occurrence_id"],
                "quantity": operator["requested_quantity"],
            }
        )
        + b"\n"
    )


def _mapping(mapping):
    _shape(
        mapping,
        {
            "type",
            "initial_record_id",
            "replacement_record_id",
            "supersedes_record_id",
            "valid_time_kind",
            "fields",
        },
        "UNSUPPORTED_RULE",
    )
    if not (
        mapping["type"] == "SupplierOrderState"
        and mapping["valid_time_kind"] == "ORDER_ONLY"
        and all(
            _text(mapping[key])
            for key in (
                "initial_record_id",
                "replacement_record_id",
                "supersedes_record_id",
            )
        )
        and mapping["initial_record_id"] == mapping["supersedes_record_id"]
        and mapping["replacement_record_id"] != mapping["initial_record_id"]
        and type(mapping["fields"]) is dict
        and mapping["fields"] == _PROPERTY_SOURCES
    ):
        _refuse(
            "UNSUPPORTED_RULE",
            "Require complete SupplierOrderState mapping and explicit distinct ORDER_ONLY replacement",
        )


def map_observation(
    observed_bytes: bytes,
    *,
    before_bytes: bytes,
    source_sha256: str,
    goal: dict,
    operator: dict,
    mapping: dict,
    source_id: str,
) -> bytes | None:
    """Map supplied bytes, not authenticated capture, to existing plan fields."""
    before = _before(before_bytes, source_sha256, goal, operator)
    _mapping(mapping)
    if not _text(source_id):
        _refuse(
            "MALFORMED_INPUT",
            "A source ID is required; capture/retention belong to the caller",
        )
    observed = _row(observed_bytes)
    if observed == before:
        return None
    if not (
        before["quantity"] == operator["expected_quantity"]
        and observed["quantity"] == operator["requested_quantity"]
        and observed["event_id"] == operator["new_source_occurrence_id"]
        and all(
            observed[field] == before[field]
            for field in ("supplier_order_id", "product_code")
        )
    ):
        _refuse(
            "UNSUPPORTED_CHANGE",
            "Supplied row disagrees with the declared replacement or source frame",
        )
    record_id = mapping["replacement_record_id"]
    fields = sorted(mapping["fields"].items())
    return _canonical(
        {
            "records": {
                "entities": [
                    {
                        "id": record_id,
                        "type": mapping["type"],
                        "properties": {
                            target: observed[source] for target, source in fields
                        },
                    }
                ],
                "relations": [],
            },
            "sources": [{"source_id": source_id, "sha256": _digest(observed_bytes)}],
            "derivations": [
                {
                    "record_id": record_id,
                    "path": ["properties", target],
                    "source_id": source_id,
                    "locator": f"row:0:{source}",
                }
                for target, source in fields
            ],
            "supersessions": [
                {
                    "record_id": record_id,
                    "supersedes_record_id": mapping["supersedes_record_id"],
                }
            ],
            "valid_time": {
                "kind": mapping["valid_time_kind"],
                "value": observed["event_id"],
            },
        }
    )
