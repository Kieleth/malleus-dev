"""Author a fresh supplier variant using Core's unchanged finite interpreter.

Core builders load their declared research definitions before selection. This
module specializes type positions, never persisted history or arbitrary strings.
It performs no check invocation, history operation, supplier effect or observation.
"""

from copy import deepcopy

from malleus.compiler import load_validated_contract_artifact
from malleus._contract_pipeline.protocol_runtime import canonical, load_bundle
from research.action_history_contract_freeze.programs.registration_bundle import (
    build_registration_bundle,
)
from research.action_history_contract_freeze.programs.initialization_bundle import (
    add_initialization,
)
from research.action_history_contract_freeze.programs.proposal_bundle import (
    add_context_proposal,
)
from research.action_history_contract_freeze.programs.assessment_bundle import (
    add_type_assessment,
)
from research.action_history_contract_freeze.programs.decision_bundle import (
    add_epistemic_decision,
)
from research.action_history_contract_freeze.programs.current_bundle import (
    add_current_context,
)
from research.action_history_contract_freeze.programs.authority_bundle import (
    add_authority_assessment,
)
from research.action_history_contract_freeze.programs.authorization_bundle import (
    add_authorization,
)
from research.action_history_contract_freeze.programs.dispatch_bundle import (
    add_dispatch,
)
from research.action_history_contract_freeze.programs.execution_bundle import (
    add_execution,
)
from research.action_history_contract_freeze.programs.observation_bundle import (
    add_observation,
)


RECORD_TYPE = "SupplierOrderAmendment"
ACTION_TYPE = "AMEND_SUPPLIER_ORDER"
PAYLOAD_FIELDS = frozenset(
    {
        "logical_source_id",
        "supplier_order_id",
        "product_code",
        "expected_quantity",
        "requested_quantity",
        "expected_source_digest",
        "new_source_occurrence_id",
    }
)


def _payload_schemas(contract):
    if (
        not contract.is_subtype_of(RECORD_TYPE, "ActionProposal")
        or contract.get_type(RECORD_TYPE).abstract
    ):
        raise ValueError("compiled concrete SupplierOrderAmendment contract required")
    slots = contract.effective_slots(RECORD_TYPE)
    added = slots.keys() - contract.effective_slots("ActionProposal").keys()
    if added != PAYLOAD_FIELDS:
        raise ValueError(
            "supplier action payload must match the declared seven-field boundary"
        )
    action_type = slots["action_type"]
    if action_type.equals_string != ACTION_TYPE:
        raise ValueError("supplier action must fix AMEND_SUPPLIER_ORDER")
    ranges = {
        "https://malleus.dev/contract-facts/String": "string",
        "https://malleus.dev/contract-facts/Integer": "integer",
    }
    result = {}
    for name in sorted(added):
        slot = slots[name]
        if (
            slot.range_id not in ranges
            or not slot.required
            or slot.multivalued
            or slot.inlined
            or slot.identifier
            or slot.equals_string is not None
            or slot.minimum is not None
            or slot.maximum is not None
            or slot.value_presence is not None
        ):
            raise ValueError("unsupported supplier payload declaration: " + name)
        result[name] = {"type": ranges[slot.range_id]}
    return result


def _specialize(value, payload):
    if type(value) is list:
        return [_specialize(item, payload) for item in value]
    if type(value) is not dict:
        return value
    value = {key: _specialize(item, payload) for key, item in value.items()}
    # These are semantic positions in Core's declared authoring grammar. A
    # source/policy ID with the same spelling is not a type and stays unchanged.
    for key, old, new in (
        ("record_type", "LocalAction", RECORD_TYPE),
        ("action_type", "LOCAL_ACTION", ACTION_TYPE),
    ):
        if value.get(key) == old:
            value[key] = new
        elif type(value.get(key)) is dict and value[key].get("const") == old:
            value[key]["const"] = new
    if type(value.get("types")) is dict:
        types = value["types"]
        if types.get("action") == "LocalAction":
            types["action"] = RECORD_TYPE
        if type(types.get("properties")) is dict:
            action = types["properties"].get("action")
            if type(action) is dict and action.get("const") == "LocalAction":
                action["const"] = RECORD_TYPE
    if type(value.get("record_schemas")) is dict:
        catalog = value["record_schemas"]
        if "LocalAction" in catalog:
            catalog[RECORD_TYPE] = catalog.pop("LocalAction")
    properties = value.get("properties")
    if (
        type(properties) is dict
        and {"action_type", "action_payload_hash", "authorization_policy_hash"}
        <= properties.keys()
    ):
        if properties["action_type"].get("const") != ACTION_TYPE:
            raise ValueError("unexpected action schema variant")
        properties.update(deepcopy(payload))
        value["required"] += sorted(payload)
    return value


def build_supplier_program(record_contract_bytes, *, source_ids, policy_ids):
    """Return new canonical program bytes; all supplied role IDs are required."""
    contract = load_validated_contract_artifact(record_contract_bytes)
    payload = _payload_schemas(contract)
    bundle = add_initialization(
        build_registration_bundle(record_contract_bytes),
        source_ids=source_ids,
        policy_ids=policy_ids,
    )
    for extend in (
        add_context_proposal,
        add_type_assessment,
        add_epistemic_decision,
        add_current_context,
        add_authority_assessment,
        add_authorization,
        add_dispatch,
        add_execution,
        add_observation,
    ):
        bundle = extend(bundle)
    result = canonical(_specialize(bundle, payload))
    load_bundle(result)
    return result
