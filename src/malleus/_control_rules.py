"""Private, pure execution of identified finite outcome-control data.

No authorization vocabulary, policy selection, callbacks or persistence live
here. The owning profile selects exact content and supplies its identity.

Identity is the digest of the artifact's canonical JSON, the same grammar
`malleus.ledger.canonical_json` uses: compact separators, sorted keys, no
NaN, UTF-8. Raw-byte identity would make the artifact's acceptance depend on
the checkout's line-ending policy, which is not part of its meaning.
"""

from dataclasses import dataclass
from hashlib import sha256
import json


class OutcomeRuleError(ValueError):
    """An identified rule artifact or its invocation is invalid."""


def _object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise OutcomeRuleError(f"duplicate rule key: {key}")
        value[key] = item
    return value


def _labels(values, *, nonempty=True):
    if (
        not isinstance(values, list)
        or (nonempty and not values)
        or any(type(value) is not str or not value.strip() for value in values)
        or len(values) != len(set(values))
    ):
        raise OutcomeRuleError("distinct nonblank rule labels required")
    return tuple(values)


def _canonical_identity(value):
    """Digest the artifact's meaning, not one serialization of it."""
    try:
        blob = json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as error:
        raise OutcomeRuleError("noncanonical rule content") from error
    return "sha256:" + sha256(blob).hexdigest()


@dataclass(frozen=True)
class OutcomeControlRules:
    """Immutable lookup, highest-first precedence and explicit trigger set."""

    identity: str
    outcome_controls: tuple[tuple[str, str], ...]
    precedence: tuple[str, ...]
    triggering_controls: tuple[str, ...]

    @classmethod
    def from_bytes(cls, data, *, expected_identity):
        if type(data) is not bytes:
            raise OutcomeRuleError("exact rule bytes required")
        try:
            value = json.loads(data, object_pairs_hook=_object)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise OutcomeRuleError("invalid rule JSON") from error
        identity = _canonical_identity(value)
        if identity != expected_identity:
            raise OutcomeRuleError("rule artifact identity differs")
        if type(value) is not dict or set(value) != {
            "schema",
            "outcome_controls",
            "control_precedence",
            "triggering_controls",
        }:
            raise OutcomeRuleError("closed outcome-control artifact required")
        if value["schema"] != "malleus.outcome-controls/private-v0":
            raise OutcomeRuleError("unsupported outcome-control grammar")
        mapping = value["outcome_controls"]
        if type(mapping) is not dict or not mapping:
            raise OutcomeRuleError("nonempty outcome mapping required")
        _labels(list(mapping))
        if any(
            type(label) is not str or not label.strip() for label in mapping.values()
        ):
            raise OutcomeRuleError("nonblank control labels required")
        precedence = _labels(value["control_precedence"])
        triggers = _labels(value["triggering_controls"], nonempty=False)
        if set(precedence) != set(mapping.values()) or not set(triggers) <= set(
            precedence
        ):
            raise OutcomeRuleError(
                "precedence and triggers must cover declared controls"
            )
        return cls(identity, tuple(sorted(mapping.items())), precedence, triggers)

    def control(self, outcome):
        if type(outcome) is not str:
            raise OutcomeRuleError("undeclared outcome")
        try:
            return dict(self.outcome_controls)[outcome]
        except KeyError as error:
            raise OutcomeRuleError("undeclared outcome") from error

    def is_trigger(self, control):
        if control not in self.precedence:
            raise OutcomeRuleError("undeclared control")
        return control in self.triggering_controls

    def select(self, controls):
        if isinstance(controls, (str, bytes, dict)):
            raise OutcomeRuleError("control collection required")
        try:
            selected = tuple(controls)
        except TypeError as error:
            raise OutcomeRuleError("control collection required") from error
        if not selected or any(control not in self.precedence for control in selected):
            raise OutcomeRuleError("nonempty declared controls required")
        return next(control for control in self.precedence if control in selected)
