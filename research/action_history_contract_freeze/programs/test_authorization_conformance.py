"""Independent expectations, not independent authorization implementations."""

from copy import deepcopy
from dataclasses import asdict
from itertools import product
import json
from pathlib import Path

import pytest

from malleus import control as implementation
from malleus.ledger import canonical_json
from research.action_history_contract_freeze.programs.test_control_executor import (
    api,
    control_inputs,
    run,
)
from tests import test_control as fixtures


CASES = json.loads(
    Path(__file__).with_name("authorization_conformance_cases.json").read_bytes()
)
ASSESSMENT_IDS = ["assessment:authority:0", "assessment:authority:1"]


def assert_expected(result, case):
    assert result["verdict"] == case["verdict"]
    assert list(result["assessment_ids"]) == ASSESSMENT_IDS
    assert list(result["triggered_assessment_ids"]) == [
        ASSESSMENT_IDS[index] for index in case["triggers"]
    ]


def standalone_control(args):
    artifacts = args["inputs"]["artifact"]
    return asdict(
        fixtures.evaluate_authority(
            artifacts["policy"]["value"],
            artifacts["context"]["value"]["monitors"],
            args["inputs"]["event"]["outputs"]["value"],
        )
    )


def both_controls(args):
    standalone = standalone_control(args)
    executed = run(args).data
    assert executed["history_authenticated"] is False
    assert executed["introductions"] == []
    assert executed["state"] == args["state"]
    finite = executed["results"]["control"]["value"]
    # Includes the hash recipe, but shared-code agreement is not its oracle.
    assert canonical_json(standalone) == canonical_json(finite)
    return standalone, finite


def test_answer_table_covers_each_two_monitor_outcome_pair_once():
    pairs = [tuple(case["outcomes"]) for case in CASES]
    outcomes = ("SATISFIED", "VIOLATED", "UNKNOWN")
    assert len(pairs) == len(set(pairs)) == 9
    assert set(pairs) == set(product(outcomes, repeat=2))


@pytest.mark.parametrize("case", CASES, ids=lambda case: "+".join(case["outcomes"]))
@pytest.mark.parametrize("reverse", [False, True], ids=["ordered", "reversed"])
def test_authorization_matches_authored_expectations(case, reverse):
    args = control_inputs("AUTHORIZATION", case["outcomes"])
    if reverse:
        args["inputs"]["event"]["outputs"]["value"].reverse()
    before = deepcopy(args)
    for result in both_controls(args):
        assert_expected(result, case)
    assert args == before


@pytest.mark.parametrize(
    "fault",
    [
        "missing",
        "duplicate",
        "base_acceptance_head",
        "action_proposal_id",
        "evaluated_actor_id",
        "authority_policy_hash",
        "monitor_hash",
        "monitor_version",
    ],
)
def test_both_entry_points_refuse_unbound_assessments_without_mutation(fault):
    args = control_inputs("AUTHORIZATION")
    outputs = args["inputs"]["event"]["outputs"]["value"]
    if fault == "missing":
        outputs.pop()
    elif fault == "duplicate":
        outputs.append(deepcopy(outputs[0]))
    else:
        outputs[0][fault] = "sha256:" + "f" * 64
    before = deepcopy(args)
    with pytest.raises(implementation.ControlError):
        standalone_control(args)
    with pytest.raises(api().ExecutionRefusal) as caught:
        run(args)
    assert caught.value.reason == "CHECK_COVERAGE"
    assert args == before


@pytest.mark.parametrize("case_index", [0, 1, 2])
def test_shared_wrong_rule_is_detected_even_when_both_paths_agree(
    monkeypatch, case_index
):
    case = CASES[case_index]
    # Synthetic fault only. No source file or stored history is changed.
    replacements = {
        "AUTHORIZE": "BLOCK",
        "BLOCK": "CLARIFY",
        "CLARIFY": "AUTHORIZE",
    }
    monkeypatch.setattr(
        implementation,
        "_authorization_control",
        lambda outcome: replacements[case["verdict"]],
    )
    args = control_inputs("AUTHORIZATION", case["outcomes"])
    for result in both_controls(args):
        with pytest.raises(AssertionError):
            assert_expected(result, case)
