"""Approved transaction definition, not action-runtime or rollback evidence."""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest

from malleus.ledger import canonical_json


HERE = Path(__file__).parent


def definition():
    schema = json.loads((HERE / "proposal-transaction.schema.json").read_bytes())
    Draft202012Validator.check_schema(schema)
    return (
        Draft202012Validator(schema),
        json.loads((HERE / "proposal-transaction.json").read_bytes()),
    )


def test_selected_transaction_definition_is_closed_and_round_trips():
    validator, value = definition()
    validator.validate(value)
    assert json.loads(canonical_json(value)) == value
    for field in value:
        missing = deepcopy(value)
        del missing[field]
        assert not validator.is_valid(missing), field
    assert not validator.is_valid({**value, "callback": "run_action"})


@pytest.mark.parametrize(
    "batches",
    [
        [],
        [["original-context-registration"]],
        [["proposal-recording"]],
        [["proposal-recording", "original-context-registration"]],
        [["original-context-registration"], ["proposal-recording"]],
        [["original-context-registration", "unrelated", "proposal-recording"]],
        [["original-context-registration", "proposal-recording"], []],
    ],
)
def test_pair_cannot_be_partial_reordered_interleaved_or_split(batches):
    validator, value = definition()
    assert not validator.is_valid({**value, "atomic_batches": batches})


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("context_prefix", "AFTER_REGISTRATION"),
        ("validation", "EACH_EVENT_BEFORE_ITS_COMMIT"),
        ("visibility", "PUBLISH_EACH_EVENT"),
        ("refusal", "RETAIN_CONTEXT_ONLY"),
        ("orphan_context", "RECOVER_LATER"),
        ("success_proposal_state", "ACCEPTED"),
        ("action_acceptance", "ADVANCE"),
        ("domain_state", "APPLY_PROPOSAL"),
        ("runtime_status", "IMPLEMENTED"),
        ("commit_preconditions", ["EXPECTED_FULL_HEAD"]),
    ],
)
def test_definition_cannot_relax_atomicity_or_claim_runtime(field, replacement):
    validator, value = definition()
    assert not validator.is_valid({**value, field: replacement})


def test_decision_is_scoped_and_does_not_rewrite_the_frozen_review():
    text = (HERE / "TRANSACTION_DECISION.md").read_text()
    assert '"yes, transactional for the moment"' in text
    assert "OPTIONAL_PROFILE" in text
    assert "not persistence" in text
    assert "Those frozen files remain historical" in text
    assert "runtime checks remain unexecuted" in text
