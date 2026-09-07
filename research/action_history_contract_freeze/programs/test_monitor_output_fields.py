"""Static field origins and compiled record shapes, never actual monitor outputs."""

from copy import deepcopy
import json
from pathlib import Path

import pytest

from malleus.ledger import content_digest, record_hash
from tests.contract_compiler.pareto.test_assent_contract_compatibility import _compile


HERE = Path(__file__).parent
VARIANTS = (
    "type_result",
    "authority_result",
    "type_failure",
    "authority_failure",
    "type_unavailable",
    "authority_unavailable",
)
AUTHORITY_FIELDS = {
    "action_proposal_id",
    "action_content_hash",
    "evaluated_actor_id",
    "authority_policy_id",
    "authority_policy_hash",
    "evaluated_authority_grant_id",
    "evaluated_authority_grant_hash",
}


def census():
    return json.loads((HERE / "monitor-output-fields.json").read_bytes())


def fields(definition, name):
    """Flatten documentation groups without permitting implicit overrides."""
    variant = definition["variants"][name]
    result = {}
    for group in [
        *(definition["groups"][key] for key in variant["groups"]),
        variant["fields"],
    ]:
        assert not result.keys() & group.keys()
        result.update(group)
    assert not result.keys() & variant["constants"].keys()
    return result


def witness(name):
    """Labeled lexical inputs, not resolved history or a producer result."""
    digest = lambda label: content_digest({"field-witness": label})  # noqa: E731
    authority = name.startswith("authority")
    return {
        "invocation": {
            "event": {
                "id": "event:check",
                "generated_at": "2026-09-07T00:00:00Z",
                "responsible_actor_id": "actor:check",
                "responsible_role": "authority-monitor"
                if authority
                else "type-monitor",
            },
            "output_ids": {
                "assessment": "assessment:check",
                "failure": "failure:check",
            },
        },
        "records": {
            "proposal": {
                "id": "proposal:check",
                "content_hash": digest("proposal"),
                "base_acceptance_head": digest("proposal-head"),
            },
            "monitor": {
                "id": "monitor:check",
                "content_hash": digest("monitor-record"),
                "artifact_version": "monitor-v1",
                "artifact_hash": digest("monitor-artifact"),
                "monitor_implementation_hash": digest("implementation"),
            },
            "action": {"id": "action:check", "content_hash": digest("action")},
            "authorization_policy": {
                "id": "policy:check",
                "content_hash": digest("policy"),
            },
            "grant": {"id": "grant:check", "content_hash": digest("grant")},
        },
        "inputs": {"executor_id": "actor:executor"},
        "current": {"action_acceptance_head": digest("current-action-head")},
        "implementation": {
            "version": "producer-v9",
            "bytes_sha256": digest("implementation"),
        },
        "closure": {
            "input_record_ids": ["proposal:check", "action:check"],
            "source_record_ids": ["proposal:check", "monitor:check"],
        },
        "computed": {
            "completed": {
                "outcome": "SATISFIED",
                "reason_codes": ["MATCH"],
                "rationale": "Static witness, no predicate was executed.",
                "checked_predicates": ["scope"],
                "violated_predicates": [],
            },
            "failure": {
                "category": "DEPENDENCY",
                "error_code": "FAILED",
                "error_message": "Static unavailable witness.",
                "reason_codes": ["FAILED"],
                "rationale": "Static failure witness, not an execution failure.",
            },
        },
    }


def specimen(definition, name, inputs):
    """Test-only field lookup. Does not verify inputs, compute checks, or append."""
    variant = definition["variants"][name]
    record = deepcopy(variant["constants"])
    for field, path in fields(definition, name).items():
        value = inputs
        for key in path:
            value = value[key]
        record[field] = deepcopy(value)
    record["content_hash"] = record_hash(variant["record_type"], record)
    return record


@pytest.fixture(scope="module")
def view():
    return _compile().view


@pytest.mark.parametrize("name", VARIANTS)
def test_every_selected_field_is_real_and_every_required_field_is_bound(view, name):
    definition = census()
    variant = definition["variants"][name]
    record = specimen(definition, name, witness(name))
    slots = view.effective_slots(variant["record_type"])
    assert set(record) <= set(slots)
    required = {key for key, value in slots.items() if value.required}
    assert required <= set(record)
    assert view.validate_instance(variant["record_type"], record) == []
    for field in required:
        missing = deepcopy(record)
        del missing[field]
        assert view.validate_instance(variant["record_type"], missing), field
    assert record["content_hash"] == record_hash(variant["record_type"], record)
    changed = {**record, "source_record_ids": ["another:source"]}
    assert record_hash(variant["record_type"], changed) != record["content_hash"]


@pytest.mark.parametrize("name", VARIANTS)
def test_identity_domains_heads_and_metadata_have_exact_origins(name):
    definition, inputs = census(), witness(name)
    origins = fields(definition, name)
    record = specimen(definition, name, inputs)
    assert origins["monitor_hash"] == ["records", "monitor", "content_hash"]
    assert origins["monitor_version"] == ["records", "monitor", "artifact_version"]
    assert record["monitor_hash"] not in {
        inputs["records"]["monitor"]["artifact_hash"],
        inputs["implementation"]["bytes_sha256"],
    }
    assert record["monitor_version"] != inputs["implementation"]["version"]
    assert origins["proposal_content_hash"] == ["records", "proposal", "content_hash"]
    head = (
        ["current", "action_acceptance_head"]
        if name.startswith("authority")
        else ["records", "proposal", "base_acceptance_head"]
    )
    assert origins["base_acceptance_head"] == head
    for field, source in {
        "generation_event_id": "id",
        "generated_at": "generated_at",
        "responsible_actor_id": "responsible_actor_id",
        "responsible_role": "responsible_role",
    }.items():
        assert origins[field] == ["invocation", "event", source]
    assert origins["id"] == [
        "invocation",
        "output_ids",
        "failure" if name.endswith("failure") else "assessment",
    ]
    assert origins["source_record_ids"] == ["closure", "source_record_ids"]
    # Closure values are still unbound producer obligations, not caller metadata.
    if not name.endswith("failure"):
        assert origins["input_record_ids"] == ["closure", "input_record_ids"]


@pytest.mark.parametrize("prefix", ["type", "authority"])
def test_failure_pair_shares_context_but_not_ids(prefix):
    definition = census()
    failed, unavailable = f"{prefix}_failure", f"{prefix}_unavailable"
    left, right = fields(definition, failed), fields(definition, unavailable)
    shared = {
        "generation_event_id",
        "generated_at",
        "responsible_actor_id",
        "responsible_role",
        "proposal_id",
        "proposal_content_hash",
        "base_acceptance_head",
        "monitor_id",
        "monitor_hash",
        "monitor_version",
    }
    if prefix == "authority":
        shared |= AUTHORITY_FIELDS
    for field in shared:
        assert left[field] == right[field]
    inputs = witness(unavailable)
    failure = specimen(definition, failed, inputs)
    inputs["closure"]["source_record_ids"].append(failure["id"])
    assessment = specimen(definition, unavailable, inputs)
    assert assessment["monitor_failure_id"] == failure["id"] != assessment["id"]
    assert assessment["assessment_outcome"] == "UNKNOWN"
    assert assessment["assessment_kind"] == failure["failed_assessment_kind"]
    assert assessment["reason_codes"] == [failure["error_code"]]
    assert not any(
        key.startswith("logic_") or key.startswith("ruleset_") for key in left | right
    )
    if prefix == "type":
        assert not AUTHORITY_FIELDS & (left | right).keys()


@pytest.mark.parametrize("name", VARIANTS)
def test_computed_fields_never_come_from_invocation(name):
    definition = census()
    origins = fields(definition, name)
    computed = {
        "assessment_outcome",
        "reason_codes",
        "rationale",
        "failure_category",
        "error_code",
        "error_message",
        "checked_policy_predicates",
        "violated_policy_predicates",
    }
    for field in computed & origins.keys():
        assert origins[field][0] == "computed"
    inputs = witness(name)
    del inputs["computed"]
    with pytest.raises(KeyError, match="computed"):
        specimen(definition, name, inputs)


def test_authority_binds_the_evaluated_grant_even_on_violation(view):
    definition, inputs = census(), witness("authority_result")
    inputs["computed"]["completed"].update(
        outcome="VIOLATED", violated_predicates=["scope"]
    )
    record = specimen(definition, "authority_result", inputs)
    assert view.validate_instance("AuthorityAssessment", record) == []
    assert record["evaluated_authority_grant_id"] == inputs["records"]["grant"]["id"]
    assert (
        record["evaluated_authority_grant_hash"]
        == inputs["records"]["grant"]["content_hash"]
    )
    assert record["evaluated_actor_id"] == inputs["inputs"]["executor_id"]
    assert (
        record["authority_policy_id"] == inputs["records"]["authorization_policy"]["id"]
    )
    assert record["action_content_hash"] == inputs["records"]["action"]["content_hash"]


def test_census_is_not_an_executable_producer_or_retained_input_closure():
    definition = census()
    assert tuple(definition["variants"]) == VARIANTS
    assert definition["status"] == "STATIC_FIELD_CENSUS"
    assert (
        definition["content_hash"]
        == "record_hash(record_type, every field except content_hash)"
    )
    assert definition["unbound"] == [
        "producer_implementation",
        "retained_input_wrappers",
        "input_closure_order",
        "source_closure_order",
        "lifecycle_validation_and_atomic_persistence",
    ]
