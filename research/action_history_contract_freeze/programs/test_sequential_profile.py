"""An optional sequential profile must preserve history, not widen slot zero."""

from copy import deepcopy
from importlib import import_module

from research.action_history_contract_freeze.programs.test_keyed_effect import fixture


def test_current_pointer_projection_preserves_the_cumulative_index():
    module = import_module(
        "research.action_history_contract_freeze.programs.sequential_bundle"
    )
    program, profile = fixture()
    bundle = {
        "profile": profile,
        "constants": {},
        "transactions": {"write": {"program": program}},
    }
    before = deepcopy(bundle)
    result = module.with_current_indexes(bundle, {"entries": None})
    assert bundle == before
    steps = result["transactions"]["write"]["program"]["steps"]
    assert steps[0] == program["steps"][0]
    assert [s["name"] for s in steps[1:]] == [
        "current_entries_key_0", "current_entries_value"
    ]
    assert all(s["opcode"] == "SET_PROTOCOL_STATE" for s in steps)
    assert result["profile"]["targets"]["entries"] == profile["targets"]["entries"]
