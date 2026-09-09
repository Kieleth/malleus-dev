"""Pure aggregate-goal selection over existing per-order Re-entry contracts.

Research-local, single attempt. No history owner, graph, path or effect input.
"""

from base64 import b64encode
from dataclasses import dataclass
from functools import wraps
from hashlib import sha256
import json
from pathlib import Path

from malleus.ledger import canonical_json, record_hash
from research.semantic_reentry_external_design import supplier_components as components
from research.semantic_reentry_external_design import supplier_proposals as proposals
from research.semantic_reentry_external_design import supplier_reentry as child
from research.semantic_reentry_external_design.accepted_read_view import (
    AcceptedReadView,
)


RULE_SCHEMA = "malleus.reentry.supplier-choice-rule/research-v1"
CONTRACT_SCHEMA = "malleus.reentry.supplier-choice-contract/research-v1"


class ChoiceRefusal(ValueError):
    def __init__(self, reason, detail):
        self.reason = reason
        super().__init__(f"{reason}: {detail}")


def require(condition, reason, detail):
    if not condition:
        raise ChoiceRefusal(reason, detail)


def guarded(function):
    @wraps(function)
    def invoke(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (
            child.ReentryRefusal,
            components.SupplierInputError,
            proposals.SupplierProtocolError,
        ) as error:
            raise ChoiceRefusal(error.reason, str(error)) from error
        except (
            KeyError,
            TypeError,
            AttributeError,
            ValueError,
            RecursionError,
        ) as error:
            if isinstance(error, ChoiceRefusal):
                raise
            raise ChoiceRefusal("MALFORMED_INPUT", str(error)) from error

    return invoke


def canonical(value):
    return canonical_json(value).encode()


def digest(content):
    require(type(content) is bytes, "MALFORMED_INPUT", "exact bytes required")
    return "sha256:" + sha256(content).hexdigest()


def closed(value, fields):
    require(
        type(value) is dict and set(value) == set(fields),
        "MALFORMED_INPUT",
        "required closed fields: " + ", ".join(sorted(fields)),
    )


def text(*values):
    require(
        all(type(v) is str and v.strip() for v in values),
        "MALFORMED_INPUT",
        "explicit nonblank identifiers required",
    )


def object_bytes(content):
    digest(content)
    value = json.loads(content)
    require(
        type(value) is dict and canonical(value) == content,
        "MALFORMED_INPUT",
        "canonical JSON object required",
    )
    return value


def source(view, identifier):
    members = [m for m in view.context.retained_inputs if m.record_id == identifier]
    require(
        len(members) == 1,
        "SOURCE_DISAGREEMENT",
        "retained source required: " + identifier,
    )
    member = members[0]
    entry = view.protocol["records"][identifier]
    record = entry["record"]
    require(
        entry["record_type"] == "SourceArtifact"
        and record["content_hash"] == record_hash("SourceArtifact", record)
        and member.role == "SOURCE_ARTIFACT"
        and member.identity == record["source_content_digest"] == digest(member.content)
        and record["source_byte_length"] == len(member.content),
        "SOURCE_DISAGREEMENT",
        "source bytes or record differ",
    )
    return record, member.content


def position(view):
    require(
        type(view) is AcceptedReadView,
        "MALFORMED_INPUT",
        "verified graph-free read required",
    )
    return {key: getattr(view.context, key) for key in child.COORDINATES}


@guarded
def rule_value(view, identifier):
    record, content = source(view, identifier)
    rule = object_bytes(content)
    closed(
        rule,
        (
            "schema",
            "goal",
            "alternatives",
            "selection",
            "evaluation_budget",
            "candidate_budget",
            "dispatch_attempt_budget",
            "automatic_retry",
            "stopping",
            "implementation",
        ),
    )
    require(rule["schema"] == RULE_SCHEMA, "UNSUPPORTED", "unknown choice rule")
    goal = rule["goal"]
    closed(goal, ("kind", "operator", "product_code", "quantity", "order_ids"))
    require(
        goal["kind"] == "GoalPredicate" and goal["operator"] == "AT_LEAST",
        "UNSUPPORTED",
        "aggregate at-least goal required",
    )
    text(goal["product_code"])
    require(
        type(goal["quantity"]) is int and goal["quantity"] > 0,
        "MALFORMED_INPUT",
        "positive integer goal required",
    )
    orders = goal["order_ids"]
    require(
        type(orders) is list and len(orders) == 2 and len(set(orders)) == 2,
        "MALFORMED_INPUT",
        "exactly two distinct explicitly scoped orders required",
    )
    text(*orders)
    selection = rule["selection"]
    closed(selection, ("strategy", "order_preference"))
    require(
        selection["strategy"] in ("REFUSE_IF_NOT_UNIQUE", "ORDER_PREFERENCE"),
        "UNSUPPORTED",
        "selection strategy is undeclared or unsupported",
    )
    preference = selection["order_preference"]
    require(
        type(preference) is list
        and (
            (selection["strategy"] == "REFUSE_IF_NOT_UNIQUE" and preference == [])
            or (
                selection["strategy"] == "ORDER_PREFERENCE"
                and len(preference) == 2
                and set(preference) == set(orders)
            )
        ),
        "MALFORMED_INPUT",
        "preference must explicitly order every scoped alternative once",
    )
    require(
        rule["automatic_retry"] is False
        and type(rule["dispatch_attempt_budget"]) is int
        and rule["dispatch_attempt_budget"] == 1
        and rule["stopping"] == "INITIAL_SATISFIED_OR_LINKED_OBSERVED_KCS",
        "UNSUPPORTED",
        "one attempt, no retry, observed closure required",
    )
    for name, maximum in (("candidate_budget", 1), ("evaluation_budget", 2)):
        require(
            type(rule[name]) is int and 0 <= rule[name] <= maximum,
            "UNSUPPORTED",
            "unsupported " + name,
        )
    implementation = rule["implementation"]
    closed(implementation, ("source_id", "bytes_sha256", "entrypoint"))
    text(*implementation.values())
    _, implementation_bytes = source(view, implementation["source_id"])
    require(
        digest(implementation_bytes) == implementation["bytes_sha256"]
        and record["source_record_ids"] == [implementation["source_id"]],
        "SOURCE_DISAGREEMENT",
        "choice rule implementation closure differs",
    )
    alternatives = rule["alternatives"]
    require(
        type(alternatives) is list and len(alternatives) == 2,
        "MALFORMED_INPUT",
        "exactly two alternatives required",
    )
    for alternative in alternatives:
        closed(
            alternative,
            (
                "order_id",
                "rule_source_id",
                "source_ids",
                "context_id",
                "action_id",
                "proposal_id",
                "episode_key",
            ),
        )
        text(*(alternative[k] for k in alternative if k != "source_ids"))
        closed(alternative["source_ids"], child.SOURCE_ROLES)
        text(*alternative["source_ids"].values())
    require(
        {a["order_id"] for a in alternatives} == set(orders),
        "MALFORMED_INPUT",
        "alternative coverage differs from goal scope",
    )
    for key in ("context_id", "action_id", "proposal_id", "episode_key"):
        require(
            len({a[key] for a in alternatives}) == 2,
            "MALFORMED_INPUT",
            "alternative identities must be distinct: " + key,
        )
    return rule, content


@guarded
def contract_value(content):
    value = object_bytes(content)
    closed(value, ("schema", "current", "rule", "original_contexts"))
    require(
        value["schema"] == CONTRACT_SCHEMA, "UNSUPPORTED", "unknown choice contract"
    )
    closed(value["current"], child.COORDINATES)
    for key, coordinate in value["current"].items():
        if key == "base_ledger_event_count":
            require(
                type(coordinate) is int and coordinate >= 0,
                "MALFORMED_INPUT",
                "integer count required",
            )
        else:
            text(coordinate)
    closed(value["rule"], ("id", "bytes_sha256"))
    text(*value["rule"].values())
    require(
        type(value["original_contexts"]) is dict
        and len(value["original_contexts"]) == 2,
        "MALFORMED_INPUT",
        "two original contexts required",
    )
    for order, original in value["original_contexts"].items():
        text(order)
        require(
            type(original) is dict,
            "MALFORMED_INPUT",
            "original context object required",
        )
    return value


@dataclass(frozen=True, slots=True)
class SupplierChoiceContract:
    canonical_bytes: bytes

    def __post_init__(self):
        contract_value(self.canonical_bytes)

    @classmethod
    def from_bytes(cls, content):
        return cls(content)

    @property
    def identity(self):
        return digest(self.canonical_bytes)


@guarded
def bind_supplier_choice(*, view, rule_source_id):
    current = position(view)
    rule, content = rule_value(view, rule_source_id)
    originals = {}
    for alternative in rule["alternatives"]:
        _, child_rule = source(view, alternative["rule_source_id"])
        child_rule = object_bytes(child_rule)
        preservation, _ = source(view, alternative["source_ids"]["preservation"])
        require(
            preservation["source_record_ids"] == [rule_source_id],
            "SOURCE_DISAGREEMENT",
            "original context must bind this aggregate rule",
        )
        if alternative["context_id"] in view.protocol["records"]:
            _, original = source(view, alternative["context_id"])
        else:
            original = proposals.original_supplier_context(
                view=view,
                initialization_id=child_rule["initialization_id"],
                **{
                    key: alternative[key]
                    for key in (
                        "source_ids",
                        "context_id",
                        "action_id",
                        "proposal_id",
                        "episode_key",
                    )
                },
            )
        value = object_bytes(original)
        require(
            all(
                value[key] == alternative[key]
                for key in ("action_id", "proposal_id", "episode_key")
            )
            and all(
                value[role]["id"] == alternative["source_ids"][role]
                for role in child.SOURCE_ROLES
            ),
            "SOURCE_DISAGREEMENT",
            "applied context belongs to a different choice rule",
        )
        child.bind_supplier_reentry(
            view=view,
            original_context_bytes=original,
            rule_source_id=alternative["rule_source_id"],
        )
        originals[alternative["order_id"]] = value
    return SupplierChoiceContract(
        canonical(
            dict(
                schema=CONTRACT_SCHEMA,
                current=current,
                rule=dict(id=rule_source_id, bytes_sha256=digest(content)),
                original_contexts=originals,
            )
        )
    )


def accepted_quantities(view, rule, originals):
    quantities = {}
    for alternative in rule["alternatives"]:
        order = alternative["order_id"]
        original = originals[order]
        _, before = source(view, original["pre_state_source"]["id"])
        _, mapping = source(view, original["mapping"]["id"])
        _, goal = source(view, original["goal"]["id"])
        _, child_rule = source(view, alternative["rule_source_id"])
        child_rule, goal = object_bytes(child_rule), object_bytes(goal)
        require(
            goal
            == dict(
                kind="GoalPredicate",
                operator="EQUALS",
                quantity=2,
                supplier_order_id=order,
                product_code=rule["goal"]["product_code"],
            ),
            "SOURCE_DISAGREEMENT",
            "child goal does not describe this alternative",
        )
        initial = object_bytes(
            components.map_initial_source(
                before,
                source_sha256=original["pre_state_source"]["bytes_sha256"],
                mapping=object_bytes(mapping),
                source_id=child_rule["logical_source_id"],
            )
        )["records"]["entities"][0]
        history = dict(view.record_history)
        member = history[initial["id"]]
        operation = member.operation
        require(
            initial
            == dict(
                id=operation.record_id,
                type=operation.record_type,
                properties=dict(operation.properties),
            ),
            "SOURCE_DISAGREEMENT",
            "initial accepted record differs from source",
        )
        changes = [
            c
            for c in view.accepted_change_sets
            if c.change_set_id == member.change_set_id
        ]
        require(
            len(changes) == 1
            and changes[0].sources
            == ((child_rule["logical_source_id"], digest(before)),),
            "SOURCE_DISAGREEMENT",
            "initial accepted source closure differs",
        )
        matching = [
            r
            for r in view.records["entities"]
            if r["type"] == initial["type"]
            and r["properties"]["supplier_order_id"] == order
            and r["properties"]["product_code"] == rule["goal"]["product_code"]
        ]
        require(
            len(matching) == 1,
            "AMBIGUOUS" if matching else "UNREALIZABLE",
            "exactly one accepted state required for " + order,
        )
        quantity = matching[0]["properties"]["ordered_quantity"]
        require(
            type(quantity) is int and quantity >= 0,
            "MALFORMED_INPUT",
            "nonnegative accepted quantity required",
        )
        quantities[order] = quantity
    return quantities


@dataclass(frozen=True, slots=True)
class ChoiceAlternative:
    order_id: str
    predicted_total: int


@dataclass(frozen=True, slots=True)
class SupplierChoiceResult:
    status: str
    reason: str
    contract_identity: str
    selected_order: str | None
    alternatives: tuple[ChoiceAlternative, ...]
    candidates: tuple[bytes, ...]


class SupplierChoiceSynthesizer:
    entrypoint = "SupplierChoiceSynthesizer.synthesize"

    @property
    def implementation_identity(self):
        return IMPLEMENTATION_IDENTITY

    def synthesize(self, contract, view, *, synthesizer, model, update_strategy):
        require(
            type(contract) is SupplierChoiceContract,
            "MALFORMED_INPUT",
            "immutable choice contract required",
        )
        try:
            return self.evaluate(contract, view, synthesizer, model, update_strategy)
        except ChoiceRefusal as error:
            return SupplierChoiceResult(
                "REFUSED", error.reason, contract.identity, None, (), ()
            )

    @guarded
    def evaluate(self, contract, view, synthesizer, model, update_strategy):
        value = contract_value(contract.canonical_bytes)
        require(
            value["current"] == position(view), "STALE_BASE", "choice contract is stale"
        )
        rebound = bind_supplier_choice(view=view, rule_source_id=value["rule"]["id"])
        require(rebound == contract, "SOURCE_DISAGREEMENT", "choice closure differs")
        rule, _ = rule_value(view, value["rule"]["id"])
        require(
            rule["implementation"]["bytes_sha256"] == self.implementation_identity
            and rule["implementation"]["entrypoint"] == self.entrypoint,
            "UNSUPPORTED_IMPLEMENTATION",
            "unselected choice synthesizer",
        )
        originals = value["original_contexts"]
        quantities = accepted_quantities(view, rule, originals)
        total = sum(quantities.values())
        ordered = sorted(rule["alternatives"], key=lambda a: a["order_id"])
        active = [a for a in ordered if a["context_id"] in view.protocol["records"]]
        require(
            len(active) <= 1, "BUDGET_EXHAUSTED", "more than one applied alternative"
        )

        # Check all selected engines before any satisfied/pending shortcut.
        for alternative in ordered:
            _, selected = source(view, alternative["rule_source_id"])
            implementations = object_bytes(selected)["implementations"]
            for role, engine in (
                ("synthesizer", synthesizer),
                ("model", model),
                ("update_strategy", update_strategy),
            ):
                require(
                    engine.implementation_identity
                    == implementations[role]["bytes_sha256"]
                    and engine.entrypoint == implementations[role]["entrypoint"],
                    "UNSUPPORTED_IMPLEMENTATION",
                    "unselected child " + role,
                )

        def child_result(alternative):
            child_contract = child.bind_supplier_reentry(
                view=view,
                original_context_bytes=canonical(originals[alternative["order_id"]]),
                rule_source_id=alternative["rule_source_id"],
            )
            try:
                result = synthesizer.synthesize(
                    child_contract, view, model=model, update_strategy=update_strategy
                )
            except (child.ReentryRefusal, components.SupplierInputError) as error:
                raise ChoiceRefusal(error.reason, str(error)) from error
            except Exception as error:
                # The selected engine is a boundary, not permission to leak an
                # untyped failure or silently continue with the other order.
                raise ChoiceRefusal("ENGINE_FAILURE", str(error)) from error
            require(
                type(result) is child.SupplierReentryResult,
                "MALFORMED_INPUT",
                "typed child Re-entry result required",
            )
            require(
                result.contract_identity == child_contract.identity
                and result.status in ("CANDIDATES", "SATISFIED", "PENDING", "REFUSED")
                and type(result.reason) is str
                and bool(result.reason.strip())
                and type(result.candidates) is tuple
                and all(type(candidate) is bytes for candidate in result.candidates)
                and (
                    (
                        result.status == "CANDIDATES"
                        and len(result.candidates) == 1
                        and type(result.model_prediction) is bytes
                    )
                    or (result.status != "CANDIDATES" and not result.candidates)
                ),
                "MALFORMED_INPUT",
                "child result must obey its bound contract and output grammar",
            )
            return result

        if active:
            result = child_result(active[0])
            require(
                not result.candidates,
                "EVIDENCE_DISAGREEMENT",
                "applied episode attempted reissue",
            )
            if result.status == "SATISFIED":
                require(
                    total >= rule["goal"]["quantity"],
                    "GOAL_UNSATISFIED",
                    "observed action did not satisfy aggregate",
                )
            return SupplierChoiceResult(
                result.status,
                result.reason,
                contract.identity,
                active[0]["order_id"],
                (),
                (),
            )
        if total >= rule["goal"]["quantity"]:
            return SupplierChoiceResult(
                "SATISFIED", "INITIAL_SATISFIED", contract.identity, None, (), ()
            )
        require(
            rule["evaluation_budget"] >= len(ordered) and rule["candidate_budget"] == 1,
            "BUDGET_EXHAUSTED",
            "complete alternative evaluation and one output require budget",
        )
        alternatives = []
        candidates = {}
        for alternative in ordered:
            result = child_result(alternative)
            require(
                result.status in ("CANDIDATES", "SATISFIED"),
                result.reason,
                "child alternative refused; never silently drop an unknown alternative",
            )
            if result.status == "SATISFIED":
                require(
                    quantities[alternative["order_id"]] == 2,
                    "MODEL_DISAGREEMENT",
                    "child satisfaction differs from accepted state",
                )
                continue
            require(
                len(result.candidates) == 1 and type(result.model_prediction) is bytes,
                "MODEL_DISAGREEMENT",
                "one modeled child candidate required",
            )
            order = alternative["order_id"]
            action = object_bytes(result.candidates[0])
            predicted = json.loads(result.model_prediction)
            require(
                action["supplier_order_id"] == order
                and predicted["supplier_order_id"] == order
                and action["requested_quantity"] == predicted["quantity"] == 2,
                "MODEL_DISAGREEMENT",
                "candidate and predicted alternative differ",
            )
            predicted_total = total - quantities[order] + predicted["quantity"]
            if predicted_total >= rule["goal"]["quantity"]:
                alternatives.append(ChoiceAlternative(order, predicted_total))
                candidates[order] = result.candidates[0]
        require(
            alternatives,
            "UNREALIZABLE",
            "no single permitted amendment reaches the goal",
        )
        alternatives = tuple(alternatives)
        if (
            len(alternatives) > 1
            and rule["selection"]["strategy"] == "REFUSE_IF_NOT_UNIQUE"
        ):
            return SupplierChoiceResult(
                "REFUSED", "AMBIGUOUS", contract.identity, None, alternatives, ()
            )
        if len(alternatives) == 1:
            selected = alternatives[0]
        else:
            preference = rule["selection"]["order_preference"]
            selected = min(alternatives, key=lambda a: preference.index(a.order_id))
        return SupplierChoiceResult(
            "CANDIDATES",
            "DECLARED_SELECTION",
            contract.identity,
            selected.order_id,
            alternatives,
            (candidates[selected.order_id],),
        )


# Trusted-process execution identity. Read once at module load, never during synthesis.
IMPLEMENTATION_BYTES = canonical(
    dict(
        schema="malleus.reentry.choice-source-capsule/research-v1",
        source_base64=b64encode(Path(__file__).read_bytes()).decode("ascii"),
        child_implementation=child.IMPLEMENTATION_IDENTITY,
    )
)
IMPLEMENTATION_IDENTITY = digest(IMPLEMENTATION_BYTES)
