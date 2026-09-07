"""Actual checker inputs from a replayed Shop proposal, no assessment append."""

from copy import deepcopy
from importlib import import_module
import inspect

import pytest

from malleus.ledger import content_digest
from research.action_history_contract_freeze.programs.check_executor import (
    CheckRefusal,
    load_check_executor,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    reopen,
)
from research.action_history_contract_freeze.programs import (
    test_proposal_history as proposal_fixture,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    TIME,
)


inputs = proposal_fixture.inputs


@pytest.fixture(scope="module")
def proposed(tmp_path_factory, inputs):
    runner = import_module(
        "research.action_history_contract_freeze.programs.history_checks"
    )
    content, checkpoint, init_record, sources = inputs
    history = reopen(tmp_path_factory.mktemp("actual-check-prefix"), content)
    proposal_fixture.submit(
        history, proposal_fixture.pair(history, checkpoint, init_record, sources)
    )
    return history.path.read_bytes(), runner


def invocation(replay, ordinal):
    data = replay.protocol_replay.data
    records = data["records"]
    policy = records["policy:epistemic"]["record"]
    monitor = records[policy["required_monitor_ids"][ordinal]]["record"]
    source = records["source:selected:record_contract"]["record"]
    return {
        "kind": "TYPE",
        "event": {
            "id": "event:assessment:" + str(ordinal),
            "generated_at": TIME,
            "responsible_actor_id": "actor:checker",
            "responsible_role": "type-monitor",
        },
        "output_ids": {
            "assessment": "assessment:" + str(ordinal),
            "failure": "failure:" + str(ordinal),
        },
        "monitor": {"id": monitor["id"], "record_hash": monitor["content_hash"]},
        "implementation": load_check_executor().implementation_reference,
        "inputs": [
            *(
                {
                    "role": role,
                    "value": {
                        "id": role + ":1",
                        "record_hash": records[role + ":1"]["record"]["content_hash"],
                    },
                }
                for role in ("proposal", "action")
            ),
            {
                "role": "record_contract",
                "value": {
                    "id": source["id"],
                    "bytes_sha256": source["source_content_digest"],
                },
            },
        ],
    }


def test_real_type_producers_read_owner_records_without_writing_history(
    tmp_path, proposed
):
    content, runner = proposed
    history = reopen(tmp_path, content)
    base = history.replay()
    assert set(inspect.signature(runner.run_history_check).parameters) == {
        "history",
        "invocation",
    }
    outputs = []
    for ordinal in range(2):
        request = invocation(base, ordinal)
        result = runner.run_history_check(history, invocation=request)
        assert (result.ledger_head, result.ledger_event_count) == (
            base.ledger_head,
            base.ledger_event_count,
        )
        assert result == runner.run_history_check(history, invocation=request)
        output = result.execution.data["records"][0]
        assert output["record_type"] == "TypeAssessment"
        record = output["record"]
        assert record["assessment_outcome"] == "SATISFIED"
        assert record["proposal_id"] == "proposal:1"
        assert (
            record["proposal_content_hash"]
            == base.protocol_replay.data["records"]["proposal:1"]["record"][
                "content_hash"
            ]
        )
        assert record["input_record_ids"] == [
            "proposal:1",
            "action:1",
            "source:selected:record_contract",
            request["monitor"]["id"],
            "source:definition",
            "source:implementation",
        ]
        assert record["source_record_ids"] == record["input_record_ids"]
        outputs.append(record)
    assert outputs[0]["monitor_id"] != outputs[1]["monitor_id"]
    assert history.path.read_bytes() == content
    assert history.replay().receipt == base.receipt
    # Outputs are computed but not yet admitted assessments or permissions.
    assert not any(r["id"] in base.protocol_replay.data["records"] for r in outputs)


@pytest.mark.parametrize(
    "fault", ["outcome", "proposal", "monitor", "contract", "implementation"]
)
def test_forged_check_inputs_refuse_without_writes(tmp_path, proposed, fault):
    content, runner = proposed
    history = reopen(tmp_path, content)
    request = deepcopy(invocation(history.replay(), 0))
    if fault == "outcome":
        request["outcome"] = "SATISFIED"
    elif fault == "proposal":
        request["inputs"][0]["value"]["record_hash"] = content_digest("forged")
    elif fault == "contract":
        request["inputs"][2]["value"]["bytes_sha256"] = content_digest("forged")
    else:
        key = "record_hash" if fault == "monitor" else "bytes_sha256"
        request[fault][key] = content_digest("forged")
    with pytest.raises(CheckRefusal):
        runner.run_history_check(history, invocation=request)
    assert history.path.read_bytes() == content
