"""Pure, research-local GoalPredicate synthesis. No retention or effect authority."""

from base64 import b64encode
from dataclasses import dataclass
from functools import wraps
from hashlib import sha256
import json
from pathlib import Path

import malleus.compiler as core
from malleus.assent import make_record
from malleus.ledger import aware_datetime, canonical_json, content_digest, record_hash
from research.semantic_reentry_external_design import supplier_components
from research.semantic_reentry_external_design.accepted_read_view import (
    AcceptedReadView,
)
from research.semantic_reentry_external_design.supplier_proposals import (
    original_supplier_context,
)


RULE_SCHEMA = "malleus.reentry.supplier-rule/research-v1"
CONTRACT_SCHEMA = "malleus.reentry.supplier-contract/research-v1"
COORDINATES = (
    "base_ledger_head",
    "base_ledger_event_count",
    "base_acceptance_head",
    "base_materialization_head",
    "base_accepted_state_digest",
    "contract_identity",
    "receipt_identity",
)
SOURCE_ROLES = ("goal", "mapping", "preservation", "pre_state_source")


class ReentryRefusal(ValueError):
    def __init__(self, reason, detail):
        self.reason, self.detail = reason, detail
        super().__init__(f"{reason}: {detail}")


def _need(condition, reason, detail):
    if not condition:
        raise ReentryRefusal(reason, detail)


def _guarded(function):
    @wraps(function)
    def invoke(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (TypeError, KeyError, AttributeError, RecursionError) as error:
            raise ReentryRefusal("MALFORMED_INPUT", str(error)) from error

    return invoke


def _canonical(value):
    try:
        return canonical_json(value).encode()
    except ValueError as error:
        raise ReentryRefusal("MALFORMED_INPUT", str(error)) from error


def _digest(content):
    _need(type(content) is bytes, "MALFORMED_INPUT", "exact bytes required")
    return "sha256:" + sha256(content).hexdigest()


def _object(content):
    _digest(content)
    try:
        value = json.loads(content)
    except ValueError as error:
        raise ReentryRefusal("MALFORMED_INPUT", str(error)) from error
    _need(
        type(value) is dict and _canonical(value) == content,
        "MALFORMED_INPUT",
        "canonical JSON object required",
    )
    return value


def _closed(value, fields):
    _need(
        type(value) is dict and set(value) == set(fields),
        "MALFORMED_INPUT",
        "required closed fields: " + ", ".join(sorted(fields)),
    )


def _text(*values):
    _need(
        all(type(v) is str and v.strip() for v in values),
        "MALFORMED_INPUT",
        "explicit nonblank text required",
    )


def _hash(value):
    _need(
        type(value) is str
        and value.startswith("sha256:")
        and len(value) == 71
        and all(c in "0123456789abcdef" for c in value[7:]),
        "MALFORMED_INPUT",
        "lowercase SHA-256 identity required",
    )


def _reference(value):
    _closed(value, ("id", "bytes_sha256"))
    _text(value["id"])
    _hash(value["bytes_sha256"])


def _retained(view, identifier):
    members = [m for m in view.context.retained_inputs if m.record_id == identifier]
    _need(
        len(members) == 1,
        "MALFORMED_INPUT",
        "unique retained input required: " + identifier,
    )
    member = members[0]
    _need(
        member.identity == _digest(member.content),
        "SOURCE_DISAGREEMENT",
        "retained bytes differ",
    )
    return member


def _record(view, identifier, kind):
    entry = view.protocol["records"][identifier]
    record = entry["record"]
    _need(
        entry["record_type"] == kind
        and record["id"] == identifier
        and record["content_hash"] == record_hash(kind, record),
        "SOURCE_DISAGREEMENT",
        "typed record or hash differs: " + identifier,
    )
    return record


def _source(view, identifier):
    record = _record(view, identifier, "SourceArtifact")
    member = _retained(view, identifier)
    _need(
        member.role == "SOURCE_ARTIFACT"
        and member.identity == record["source_content_digest"]
        and type(record["source_byte_length"]) is int
        and len(member.content) == record["source_byte_length"],
        "SOURCE_DISAGREEMENT",
        "source bytes or metadata differ",
    )
    return record, member.content


def _bound_source(view, reference):
    _reference(reference)
    record, content = _source(view, reference["id"])
    _need(
        _digest(content) == reference["bytes_sha256"],
        "SOURCE_DISAGREEMENT",
        "bound source differs",
    )
    return record, content


def _position(view):
    _need(
        type(view) is AcceptedReadView,
        "MALFORMED_INPUT",
        "verified graph-free Core read required",
    )
    return {key: getattr(view.context, key) for key in COORDINATES}


def _contract_value(content):
    value = _object(content)
    _closed(value, ("schema", "current", "original_context", "rule"))
    _need(
        value["schema"] == CONTRACT_SCHEMA,
        "UNSUPPORTED",
        "unknown Re-entry Contract grammar",
    )
    _closed(value["current"], COORDINATES)
    for name, coordinate in value["current"].items():
        if name == "base_ledger_event_count":
            _need(
                type(coordinate) is int and coordinate >= 0,
                "MALFORMED_INPUT",
                "integer ledger count required",
            )
        else:
            _text(coordinate)
    _original(value["original_context"])
    _reference(value["rule"])
    return value


def _original(value):
    _closed(
        value,
        (
            "schema",
            "id",
            "prefix",
            "domain",
            "action_acceptance_head",
            "initialization_identity",
            "epistemic_policy",
            "authorization_policy",
            "proposal_id",
            "action_id",
            "episode_key",
            *SOURCE_ROLES,
        ),
    )
    _need(
        value["schema"] == "malleus.action-history.original-context/research-v1",
        "UNSUPPORTED",
        "unknown original-context grammar",
    )
    _closed(value["prefix"], ("head", "event_count"))
    _closed(
        value["domain"],
        (
            "effective_contract_identity",
            "kcs_acceptance_head",
            "materialization_head",
            "accepted_graph_digest",
        ),
    )
    _need(
        type(value["prefix"]["event_count"]) is int
        and value["prefix"]["event_count"] >= 0,
        "MALFORMED_INPUT",
        "integer original count required",
    )
    _text(*(value[k] for k in ("id", "action_id", "proposal_id", "episode_key")))
    for role in SOURCE_ROLES:
        _reference(value[role])
    for role in ("epistemic_policy", "authorization_policy"):
        _closed(value[role], ("id", "record_hash"))
        _text(value[role]["id"])
        _hash(value[role]["record_hash"])


@dataclass(frozen=True, slots=True)
class SupplierReentryContract:
    canonical_bytes: bytes

    def __post_init__(self):
        _contract_value(self.canonical_bytes)

    @classmethod
    def from_bytes(cls, content):
        return cls(content)

    @property
    def identity(self):
        return _digest(self.canonical_bytes)


@dataclass(frozen=True, slots=True)
class SupplyGapFinding:
    current_quantity: int
    required_quantity: int
    shortfall: int


@dataclass(frozen=True, slots=True)
class SupplierReentryResult:
    status: str
    reason: str
    contract_identity: str
    finding: SupplyGapFinding | None
    candidates: tuple[bytes, ...]
    model_prediction: bytes | None


def _rule(view, identifier):
    record, content = _source(view, identifier)
    value = _object(content)
    _closed(
        value,
        (
            "schema",
            "initialization_id",
            "goal_kind",
            "output_type",
            "logical_source_id",
            "operator",
            "ambiguity",
            "candidate_budget",
            "dispatch_attempt_budget",
            "automatic_retry",
            "stopping",
            "implementations",
            "executor",
            "observer",
            "observed_mapper",
            "output",
        ),
    )
    _need(
        value["schema"] == RULE_SCHEMA
        and value["goal_kind"] == "GoalPredicate"
        and value["output_type"] == "SupplierOrderAmendment",
        "UNSUPPORTED",
        "unsupported input or output kind",
    )
    _text(value["initialization_id"], value["logical_source_id"])
    _need(
        value["ambiguity"] == "REFUSE_IF_NOT_UNIQUE",
        "UNSUPPORTED",
        "declared ambiguity behavior unsupported",
    )
    _need(
        type(value["candidate_budget"]) is int
        and value["candidate_budget"] in (0, 1)
        and type(value["dispatch_attempt_budget"]) is int
        and value["dispatch_attempt_budget"] == 1
        and value["automatic_retry"] is False
        and value["stopping"] == "INITIAL_SATISFIED_OR_LINKED_OBSERVED_KCS",
        "UNSUPPORTED",
        "unsupported budget, retry or stopping rule",
    )
    operator = value["operator"]
    _closed(
        operator,
        (
            "kind",
            "expected_quantity",
            "requested_quantity",
            "new_source_occurrence_id",
            "precondition",
            "changed_fields",
        ),
    )
    _need(
        operator["kind"] == "AMEND_SUPPLIER_ORDER"
        and type(operator["expected_quantity"]) is int
        and operator["expected_quantity"] == 1
        and type(operator["requested_quantity"]) is int
        and operator["requested_quantity"] == 2
        and operator["precondition"] == "EXACT_CAPTURED_PRESTATE_BYTES"
        and operator["changed_fields"] == ["event_id", "quantity"],
        "UNSUPPORTED",
        "only explicit integer 1-to-2 amendment supported",
    )
    _text(operator["new_source_occurrence_id"])
    _closed(value["implementations"], ("synthesizer", "model", "update_strategy"))
    dependencies = set()
    for reference, extra in (
        *(
            (reference, ("entrypoint",))
            for reference in value["implementations"].values()
        ),
        (value["executor"], ()),
        (value["observed_mapper"], ("adapter_id",)),
    ):
        _closed(reference, ("source_id", "bytes_sha256", *extra))
        _text(reference["source_id"], *(reference[k] for k in extra))
        _, implementation = _source(view, reference["source_id"])
        _need(
            _digest(implementation) == reference["bytes_sha256"],
            "UNSUPPORTED_IMPLEMENTATION",
            "implementation source differs",
        )
        dependencies.add(reference["source_id"])
    _closed(value["observer"], ("outcome_contract_id", "observer_implementation_hash"))
    observer = _record(
        view, value["observer"]["outcome_contract_id"], "OutcomeContractArtifact"
    )
    _need(
        observer["observation_type"] == "OBSERVED_SOURCE"
        and observer["observer_implementation_hash"]
        == value["observer"]["observer_implementation_hash"]
        and len(observer["source_record_ids"]) == 1,
        "UNSUPPORTED_IMPLEMENTATION",
        "observer contract differs",
    )
    _, observer_bytes = _source(view, observer["source_record_ids"][0])
    _need(
        _digest(observer_bytes) == observer["observer_implementation_hash"],
        "UNSUPPORTED_IMPLEMENTATION",
        "observer implementation differs",
    )
    dependencies.add(observer["id"])
    _need(
        set(record["source_record_ids"]) == dependencies,
        "SOURCE_DISAGREEMENT",
        "rule dependency closure differs",
    )
    _closed(value["output"], ("proposer_id", "generated_at", "proposal_key"))
    _text(*value["output"].values())
    try:
        aware_datetime(value["output"]["generated_at"], "proposal time")
    except ValueError as error:
        raise ReentryRefusal("MALFORMED_INPUT", str(error)) from error
    return value, content


@_guarded
def bind_supplier_reentry(*, view, original_context_bytes, rule_source_id):
    current = _position(view)
    original = _object(original_context_bytes)
    _original(original)
    rule, rule_bytes = _rule(view, rule_source_id)
    goal_record, _ = _bound_source(view, original["goal"])
    _need(
        goal_record["source_record_ids"] == [rule_source_id],
        "SOURCE_DISAGREEMENT",
        "goal must bind the exact retained rule",
    )
    for role in SOURCE_ROLES:
        _bound_source(view, original[role])
    if original["id"] in view.protocol["records"]:
        _, retained = _source(view, original["id"])
        _need(
            retained == original_context_bytes,
            "STALE_BASE",
            "original context cannot be rewritten",
        )
    else:
        expected = original_supplier_context(
            view=view,
            initialization_id=rule["initialization_id"],
            source_ids={role: original[role]["id"] for role in SOURCE_ROLES},
            context_id=original["id"],
            action_id=original["action_id"],
            proposal_id=original["proposal_id"],
            episode_key=original["episode_key"],
        )
        _need(
            expected == original_context_bytes,
            "STALE_BASE",
            "original context differs from accepted prefix",
        )
    return SupplierReentryContract(
        _canonical(
            dict(
                schema=CONTRACT_SCHEMA,
                current=current,
                original_context=original,
                rule=dict(id=rule_source_id, bytes_sha256=_digest(rule_bytes)),
            )
        )
    )


class SupplierSourceModel:
    entrypoint = "SupplierSourceModel.predict"

    @property
    def implementation_identity(self):
        return IMPLEMENTATION_IDENTITY

    def predict(self, *, before_bytes, source_sha256, goal, operator):
        return supplier_components.model_amendment(
            before_bytes, source_sha256=source_sha256, goal=goal, operator=operator
        )


class SupplierActionStrategy:
    entrypoint = "SupplierActionStrategy.payload"

    @property
    def implementation_identity(self):
        return IMPLEMENTATION_IDENTITY

    def payload(
        self,
        *,
        before_bytes,
        prediction,
        source_sha256,
        goal,
        operator,
        mapping,
        logical_source_id,
    ):
        fragment = supplier_components.map_observation(
            prediction,
            before_bytes=before_bytes,
            source_sha256=source_sha256,
            goal=goal,
            operator=operator,
            mapping=mapping,
            source_id=logical_source_id,
        )
        _need(
            fragment is not None,
            "MODEL_DISAGREEMENT",
            "model did not predict an amendment",
        )
        return _canonical(
            _permitted_payload(goal, operator, source_sha256, logical_source_id)
        )


def _permitted_payload(goal, operator, source_sha256, logical_source_id):
    return dict(
        logical_source_id=logical_source_id,
        supplier_order_id=goal["supplier_order_id"],
        product_code=goal["product_code"],
        expected_quantity=operator["expected_quantity"],
        requested_quantity=operator["requested_quantity"],
        expected_source_digest=source_sha256,
        new_source_occurrence_id=operator["new_source_occurrence_id"],
    )


def _engines(rule, synthesizer, model, strategy):
    for name, engine in (
        ("synthesizer", synthesizer),
        ("model", model),
        ("update_strategy", strategy),
    ):
        selected = rule["implementations"][name]
        _need(
            engine.implementation_identity == selected["bytes_sha256"]
            and engine.entrypoint == selected["entrypoint"],
            "UNSUPPORTED_IMPLEMENTATION",
            "unselected " + name,
        )


def _inputs(view, original, rule):
    sources = {role: _bound_source(view, original[role])[1] for role in SOURCE_ROLES}
    goal, mapping, preservation = (
        _object(sources[role]) for role in ("goal", "mapping", "preservation")
    )
    _closed(goal, ("kind", "supplier_order_id", "product_code", "operator", "quantity"))
    _need(
        goal["kind"] == "GoalPredicate"
        and goal["operator"] == "EQUALS"
        and type(goal["quantity"]) is int
        and goal["quantity"] == 2,
        "UNSUPPORTED",
        "only equality-to-two goal supported",
    )
    _text(goal["supplier_order_id"], goal["product_code"])
    _closed(preservation, ("mode", "required_ids"))
    _need(
        preservation["mode"] == "ALL_OTHER_ACCEPTED_RECORDS_AND_HISTORY"
        and type(preservation["required_ids"]) is list
        and len(set(preservation["required_ids"])) == len(preservation["required_ids"])
        and all(i in dict(view.record_history) for i in preservation["required_ids"]),
        "UNSUPPORTED",
        "preservation policy or required complement differs",
    )
    initial = _object(
        supplier_components.map_initial_source(
            sources["pre_state_source"],
            source_sha256=original["pre_state_source"]["bytes_sha256"],
            mapping=mapping,
            source_id=rule["logical_source_id"],
        )
    )["records"]["entities"][0]
    eligible = [
        r
        for r in view.records["entities"]
        if r["type"] == mapping["type"]
        and all(
            r["properties"][key] == goal[key]
            for key in ("supplier_order_id", "product_code")
        )
    ]
    _need(
        len(eligible) == 1,
        "AMBIGUOUS" if eligible else "UNREALIZABLE",
        "exactly one eligible accepted supplier required",
    )
    target = eligible[0]
    quantity = target["properties"]["ordered_quantity"]
    _need(
        type(quantity) is int, "MALFORMED_INPUT", "integer accepted quantity required"
    )
    history = dict(view.record_history)
    _need(
        initial["id"] in history,
        "SOURCE_DISAGREEMENT",
        "accepted pre-state lineage missing",
    )
    initial_history = history[initial["id"]]
    operation = initial_history.operation
    _need(
        initial
        == dict(
            id=operation.record_id,
            type=operation.record_type,
            properties=dict(operation.properties),
        ),
        "SOURCE_DISAGREEMENT",
        "original source and accepted operation differ",
    )
    changes = [
        c
        for c in view.accepted_change_sets
        if c.change_set_id == initial_history.change_set_id
    ]
    _need(
        len(changes) == 1
        and changes[0].sources
        == ((rule["logical_source_id"], _digest(sources["pre_state_source"])),),
        "SOURCE_DISAGREEMENT",
        "accepted initial source closure differs",
    )
    _need(
        _retained(view, rule["logical_source_id"]).content
        == sources["pre_state_source"],
        "SOURCE_DISAGREEMENT",
        "accepted source bytes differ",
    )
    return goal, mapping, sources["pre_state_source"], target


def _index(view, name, keys):
    """Read an optional lifecycle entry, never execute its transition program."""
    protocol = view.protocol
    contents = {
        m.content
        for m in view.context.retained_inputs
        if m.role == "RETAINED_EVIDENCE" and m.identity == protocol["bundle_identity"]
    }
    _need(len(contents) == 1, "MALFORMED_INPUT", "selected program bytes must resolve")
    content = next(iter(contents))
    _need(
        _digest(content) == protocol["bundle_identity"],
        "SOURCE_DISAGREEMENT",
        "selected program bytes differ",
    )
    targets = _object(content)["profile"]["targets"]
    _need(name in targets, "UNSUPPORTED", "lifecycle index is not declared: " + name)
    declaration = targets[name]
    _need(
        declaration["target"] == "PROTOCOL_INDEX"
        and declaration["storage_path"] == ["protocol", name]
        and len(declaration["key_schemas"]) == len(keys),
        "UNSUPPORTED",
        "incompatible lifecycle index declaration",
    )
    state = protocol["state"]["protocol"]
    # The selected profile declares this index, but no transition has populated it.
    if name not in state:
        return None
    matches = [r["value"] for r in state[name] if r["keys"] == keys]
    _need(len(matches) <= 1, "AMBIGUOUS", "competing lifecycle entries: " + name)
    return matches[0] if matches else None


def _record_ref(record):
    return dict(id=record["id"], record_hash=record["content_hash"])


def _accepted_plan(view, target):
    member = dict(view.record_history)[target["id"]]
    changes = [
        c for c in view.accepted_change_sets if c.change_set_id == member.change_set_id
    ]
    _need(
        len(changes) == 1, "EVIDENCE_DISAGREEMENT", "target has no unique accepted KCS"
    )
    change = changes[0]
    evidence = []
    plans = []
    for identifier, identity in change.evidence:
        retained = _retained(view, identifier)
        _need(
            retained.identity == identity,
            "EVIDENCE_DISAGREEMENT",
            "accepted evidence identity differs",
        )
        evidence.append(retained)
        try:
            value = json.loads(retained.content)
        except (ValueError, UnicodeError):
            continue  # Ordinary evidence may be non-JSON; it cannot be the required plan.
        if (
            type(value) is dict
            and "grammar" in value
            and value["grammar"] == "malleus.population-plan/private-v0"
        ):
            _need(
                _canonical(value) == retained.content
                and value["plan_id"] == identifier,
                "EVIDENCE_DISAGREEMENT",
                "population plan bytes or identity differ",
            )
            plans.append(value)
    _need(
        len(plans) == 1,
        "EVIDENCE_DISAGREEMENT",
        "one accepted population plan required",
    )
    return change, plans[0], evidence


def _linked_update(
    view, original, rule, goal, mapping, before, target, observation, outcome
):
    """Check accepted evidence links. Admission and temporal replay remain Core's."""
    captured, actual = _source(view, observation["observed_source_artifact_id"])
    _need(
        captured["content_hash"] == observation["observed_source_artifact_hash"]
        and captured["source_record_ids"]
        == [observation["execution_id"], outcome["id"]]
        and captured["source_locator"] == "urn:controlled:" + rule["logical_source_id"],
        "EVIDENCE_DISAGREEMENT",
        "capture is not bound to this execution and source",
    )
    change, plan, evidence = _accepted_plan(view, target)
    _need(
        plan["adapter"]
        == dict(
            adapter_id=rule["observed_mapper"]["adapter_id"],
            version=rule["observed_mapper"]["bytes_sha256"],
        ),
        "EVIDENCE_DISAGREEMENT",
        "accepted correction was not mapped by the selected adapter",
    )
    _need(
        len(plan["sources"]) == 1 and len(plan["evidence"]) == 1,
        "EVIDENCE_DISAGREEMENT",
        "one observed source and binding required",
    )
    source_ref = plan["sources"][0]
    mapped_source = _retained(view, source_ref["source_id"])
    _need(
        mapped_source.role == "RETAINED_SOURCE"
        and mapped_source.content == actual
        and source_ref["sha256"] == mapped_source.identity
        and change.sources == ((mapped_source.record_id, mapped_source.identity),),
        "EVIDENCE_DISAGREEMENT",
        "accepted population source is not the actual capture",
    )
    evidence_ref = plan["evidence"][0]
    bindings = [e for e in evidence if e.record_id == evidence_ref["evidence_id"]]
    _need(
        len(bindings) == 1 and bindings[0].identity == evidence_ref["sha256"],
        "EVIDENCE_DISAGREEMENT",
        "accepted observation binding is missing",
    )
    binding = _object(bindings[0].content)
    original_record, original_bytes = _source(view, original["id"])
    population_source = binding["population_source"]
    _closed(population_source, ("source_id", "artifact_id", "bytes_sha256"))
    population_artifact = _retained(view, population_source["artifact_id"])
    _need(
        population_artifact.role == "SOURCE_ARTIFACT"
        and population_artifact.content == actual,
        "EVIDENCE_DISAGREEMENT",
        "ordinary source artifact differs from capture",
    )
    expected_binding = dict(
        schema="malleus.reentry.observed-source-binding/research-v1",
        original_context={
            **_record_ref(original_record),
            "bytes_sha256": _digest(original_bytes),
        },
        observation=_record_ref(observation),
        outcome_contract={
            **_record_ref(outcome),
            "observer_implementation_hash": rule["observer"][
                "observer_implementation_hash"
            ],
        },
        observed_source={**_record_ref(captured), "bytes_sha256": _digest(actual)},
        population_source=dict(
            source_id=mapped_source.record_id,
            artifact_id=population_artifact.record_id,
            bytes_sha256=_digest(actual),
        ),
        goal=original["goal"],
        mapping=original["mapping"],
        preservation=original["preservation"],
        operator=rule["operator"],
    )
    _need(
        binding == expected_binding,
        "EVIDENCE_DISAGREEMENT",
        "accepted KCS belongs to different observation closure",
    )
    fragment_bytes = supplier_components.map_observation(
        actual,
        before_bytes=before,
        source_sha256=original["pre_state_source"]["bytes_sha256"],
        goal=goal,
        operator=rule["operator"],
        mapping=mapping,
        source_id=mapped_source.record_id,
    )
    _need(
        fragment_bytes is not None,
        "EVIDENCE_DISAGREEMENT",
        "capture contains no correction",
    )
    fragment = _object(fragment_bytes)
    _need(
        all(plan[k] == v for k, v in fragment.items())
        and fragment["records"]["entities"] == [target]
        and len(change.operations) == 1
        and change.operations[0].record_id == target["id"]
        and change.operations[0].supersedes_record_id == mapping["initial_record_id"],
        "EVIDENCE_DISAGREEMENT",
        "accepted correction differs from the exact observed mapping",
    )
    domain = original["domain"]
    _need(
        change.base_acceptance_head == domain["kcs_acceptance_head"]
        and change.base_materialization_head == domain["materialization_head"]
        and change.base_accepted_state_digest == domain["accepted_graph_digest"]
        and change.contract_identity == domain["effective_contract_identity"]
        and view.context.contract_identity == change.contract_identity
        and view.accepted_change_sets[-1].identity == change.identity,
        "PRESERVATION_VIOLATION",
        "only the declared single correction may change the original domain frame",
    )


def _episode(view, original, rule, goal, mapping, before, target):
    associated = _index(view, "context_by_proposal", [original["proposal_id"]])
    if associated is None:
        return "PENDING", "ORIGINAL_CONTEXT_RETAINED"
    _need(
        associated == original["id"], "EVIDENCE_DISAGREEMENT", "episode context differs"
    )
    action = _record(view, original["action_id"], "SupplierOrderAmendment")
    _need(
        action["action_key"] == original["episode_key"]
        and original["id"] in action["source_record_ids"]
        and action["logical_source_id"] == rule["logical_source_id"]
        and action["expected_source_digest"] == _digest(before)
        and action["action_type"] == rule["operator"]["kind"]
        and all(action[k] == goal[k] for k in ("supplier_order_id", "product_code"))
        and all(
            action[k] == rule["operator"][k]
            for k in (
                "expected_quantity",
                "requested_quantity",
                "new_source_occurrence_id",
            )
        ),
        "EVIDENCE_DISAGREEMENT",
        "episode action differs from the bound goal and operator",
    )
    proposed = _index(view, "proposal_states", [original["proposal_id"]])
    if proposed in ("REJECTED", "DEFERRED"):
        return "REFUSED", "EPISODE_TERMINAL"
    _need(
        proposed in ("PROPOSED", "ACCEPTED"),
        "EVIDENCE_DISAGREEMENT",
        "unknown episode state",
    )
    authorization = _index(view, "authorization_states", [action["id"]])
    if authorization in ("BLOCKED", "CLARIFICATION_REQUIRED"):
        return "REFUSED", "EPISODE_TERMINAL"
    dispatch_id = _index(view, "dispatch_by_action", [action["id"]])
    if dispatch_id is None:
        return "PENDING", "AWAITING_DISPATCH"
    dispatch = _record(view, dispatch_id, "ActionDispatch")
    _need(
        dispatch["action_proposal_id"] == action["id"]
        and dispatch["action_content_hash"] == action["content_hash"]
        and dispatch["dispatch_adapter_id"] == rule["executor"]["source_id"],
        "EVIDENCE_DISAGREEMENT",
        "dispatch action or executor binding differs",
    )
    execution_id = _index(view, "execution_by_dispatch", [dispatch_id])
    if execution_id is None:
        return "PENDING", "AWAITING_RECEIPT"
    execution = _record(view, execution_id, "ActionExecution")
    _need(
        execution["dispatch_id"] == dispatch_id
        and execution["dispatch_hash"] == dispatch["content_hash"],
        "EVIDENCE_DISAGREEMENT",
        "execution dispatch binding differs",
    )
    observation_id = _index(
        view,
        "observation_by_execution_contract",
        [execution_id, rule["observer"]["outcome_contract_id"]],
    )
    if observation_id is None:
        return "PENDING", "AWAITING_OBSERVATION"
    observation = _record(view, observation_id, "OutcomeObservation")
    outcome = _record(
        view, rule["observer"]["outcome_contract_id"], "OutcomeContractArtifact"
    )
    _need(
        observation["execution_id"] == execution_id
        and observation["execution_hash"] == execution["content_hash"]
        and observation["outcome_contract_id"] == outcome["id"]
        and observation["outcome_contract_hash"] == outcome["content_hash"],
        "EVIDENCE_DISAGREEMENT",
        "observation execution or contract binding differs",
    )
    if observation["observation_result"] != "CONFIRMED":
        return "REFUSED", "EPISODE_TERMINAL"
    if target["id"] == mapping["initial_record_id"]:
        return "PENDING", "AWAITING_OBSERVED_KCS"
    _need(
        target["id"] == mapping["replacement_record_id"]
        and target["properties"]["ordered_quantity"] == goal["quantity"],
        "EVIDENCE_DISAGREEMENT",
        "current target is not this episode's observed correction",
    )
    _linked_update(
        view, original, rule, goal, mapping, before, target, observation, outcome
    )
    return "SATISFIED", "LINKED_OBSERVED_KCS"


class SupplierReentrySynthesizer:
    entrypoint = "SupplierReentrySynthesizer.synthesize"

    @property
    def implementation_identity(self):
        return IMPLEMENTATION_IDENTITY

    def synthesize(self, contract, view, *, model, update_strategy):
        _need(
            type(contract) is SupplierReentryContract,
            "MALFORMED_INPUT",
            "immutable Re-entry Contract required",
        )
        try:
            return self._evaluate(contract, view, model, update_strategy)
        except (ReentryRefusal, supplier_components.SupplierInputError) as error:
            return SupplierReentryResult(
                "REFUSED", error.reason, contract.identity, None, (), None
            )

    @_guarded
    def _evaluate(self, contract, view, model, update_strategy):
        value = _contract_value(contract.canonical_bytes)
        _need(
            value["current"] == _position(view),
            "STALE_BASE",
            "contract and accepted read differ",
        )
        original = value["original_context"]
        rebound = bind_supplier_reentry(
            view=view,
            original_context_bytes=_canonical(original),
            rule_source_id=value["rule"]["id"],
        )
        _need(rebound == contract, "SOURCE_DISAGREEMENT", "contract closure differs")
        rule, _ = _rule(view, value["rule"]["id"])
        _engines(rule, self, model, update_strategy)
        goal, mapping, before, target = _inputs(view, original, rule)
        quantity = target["properties"]["ordered_quantity"]
        finding = SupplyGapFinding(
            quantity, goal["quantity"], max(goal["quantity"] - quantity, 0)
        )
        if original["id"] in view.protocol["records"]:
            status, reason = _episode(
                view, original, rule, goal, mapping, before, target
            )
            return SupplierReentryResult(
                status, reason, contract.identity, finding, (), None
            )
        _need(
            target["id"] == mapping["initial_record_id"],
            "SOURCE_DISAGREEMENT",
            "unacted target differs from original source",
        )
        if quantity == goal["quantity"]:
            return SupplierReentryResult(
                "SATISFIED", "INITIAL_SATISFIED", contract.identity, finding, (), None
            )
        _need(
            quantity == rule["operator"]["expected_quantity"],
            "UNREALIZABLE",
            "no operator for current quantity",
        )
        _need(
            rule["candidate_budget"] == 1,
            "BUDGET_EXHAUSTED",
            "no candidate budget remains",
        )
        prediction = model.predict(
            before_bytes=before,
            source_sha256=original["pre_state_source"]["bytes_sha256"],
            goal=_object(_canonical(goal)),
            operator=_object(_canonical(rule["operator"])),
        )
        modeled = supplier_components.map_observation(
            prediction,
            before_bytes=before,
            source_sha256=original["pre_state_source"]["bytes_sha256"],
            goal=goal,
            operator=rule["operator"],
            mapping=mapping,
            source_id=rule["logical_source_id"],
        )
        _need(
            modeled is not None,
            "MODEL_DISAGREEMENT",
            "prediction must satisfy the goal and source frame",
        )
        payload = _object(
            update_strategy.payload(
                before_bytes=before,
                prediction=prediction,
                source_sha256=original["pre_state_source"]["bytes_sha256"],
                goal=_object(_canonical(goal)),
                operator=_object(_canonical(rule["operator"])),
                mapping=_object(_canonical(mapping)),
                logical_source_id=rule["logical_source_id"],
            )
        )
        _need(
            payload
            == _permitted_payload(
                goal,
                rule["operator"],
                original["pre_state_source"]["bytes_sha256"],
                rule["logical_source_id"],
            ),
            "MODEL_DISAGREEMENT",
            "strategy output differs from the bound permitted action",
        )
        action = make_record(
            "SupplierOrderAmendment",
            id=original["action_id"],
            event_id="event:" + original["proposal_id"],
            generated_at=rule["output"]["generated_at"],
            actor_id=rule["output"]["proposer_id"],
            role="proposer",
            source_record_ids=[original["id"], original["authorization_policy"]["id"]],
            action_type=rule["operator"]["kind"],
            action_payload_hash=content_digest(payload),
            action_key=original["episode_key"],
            revision=1,
            authorization_policy_id=original["authorization_policy"]["id"],
            authorization_policy_hash=original["authorization_policy"]["record_hash"],
            **payload,
        )
        _, checkpoint_bytes = _source(view, rule["initialization_id"])
        checkpoint = _object(checkpoint_bytes)
        _, record_contract_bytes = _bound_source(view, checkpoint["record_contract"])
        errors = core.load_validated_contract_artifact(
            record_contract_bytes
        ).validate_instance("SupplierOrderAmendment", action)
        _need(
            not errors,
            "UNSUPPORTED",
            "candidate violates compiled action contract: " + str(errors),
        )
        return SupplierReentryResult(
            "CANDIDATES",
            "UNIQUE_MODELED_AMENDMENT",
            contract.identity,
            finding,
            (_canonical(action),),
            prediction,
        )


# Read implementation bytes only at module load, never during bind/evaluation.
IMPLEMENTATION_BYTES = _canonical(
    {
        "schema": "malleus.reentry.source-capsule/research-v1",
        "files": {
            name: b64encode(Path(__file__).with_name(name).read_bytes()).decode("ascii")
            for name in (
                "supplier_reentry.py",
                "supplier_components.py",
                "supplier_proposals.py",
                "accepted_read_view.py",
            )
        },
    }
)
IMPLEMENTATION_IDENTITY = _digest(IMPLEMENTATION_BYTES)
