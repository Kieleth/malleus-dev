"""Independent retained observation, never an execution-status shortcut."""

from copy import deepcopy
from importlib import import_module

import pytest

from malleus.assent import make_record
from malleus.compiler import KnowledgeChangeHistory, KnowledgeChangeRefusal
from malleus.execution import outcome_contract_digest
from malleus.ledger import content_digest, record_hash
from research.action_history_contract_freeze.programs import (
    test_execution_history as receipts,
)
from research.action_history_contract_freeze.programs.dispatch_bundle import (
    add_dispatch,
)
from research.action_history_contract_freeze.programs.execution_bundle import (
    add_execution,
)
from research.action_history_contract_freeze.programs.test_initialization_history import (
    reopen,
)
from research.action_history_contract_freeze.programs.test_proposal_history import (
    source,
    preimage,
)
from research.action_history_contract_freeze.programs.test_registration_history import (
    append,
    draft,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api, canonical


TIME = "2026-09-07T00:30:00Z"
SOURCE_BYTES = canonical(
    {"source": "independent synthetic observed state", "changed": True}
)
OBSERVER_BYTES = (
    b"synthetic observer definition for protocol conformance, not executed by Core"
)


def register_source(history, identifier, content):
    value = source(identifier, content, [])
    value["generated_at"] = TIME
    value["content_hash"] = record_hash("SourceArtifact", value)
    append(
        history,
        "source",
        draft("SourceArtifact", value, preimage=preimage(value), content=content),
    )
    return value


def contract_event(history):
    implementation = history.replay().protocol_replay.data["records"][
        "source:observer"
    ]["record"]
    value = make_record(
        "OutcomeContractArtifact",
        id="outcome-contract:1",
        event_id="event:outcome-contract",
        generated_at=TIME,
        actor_id="actor:registrar",
        role="registrar",
        source_record_ids=[implementation["id"]],
        artifact_kind="OUTCOME_CONTRACT",
        artifact_version="v1",
        artifact_hash=outcome_contract_digest(
            schema_version="1",
            contract_id="outcome-contract:1",
            contract_version="v1",
            observation_type="OBSERVED_SOURCE",
            observer_implementation_hash=api().digest(OBSERVER_BYTES),
        ),
        outcome_contract_schema_version="1",
        observation_type="OBSERVED_SOURCE",
        observer_implementation_hash=api().digest(OBSERVER_BYTES),
    )
    pre = {
        "outcome_contract_schema_version": "1",
        "contract_id": value["id"],
        "contract_version": "v1",
        "observation_type": value["observation_type"],
        "observer_implementation_hash": value["observer_implementation_hash"],
    }
    result = draft("OutcomeContractArtifact", value, preimage=pre)
    result["data"]["implementation"] = {
        "id": implementation["id"],
        "record_hash": implementation["content_hash"],
    }
    return result


def observer_inputs(history):
    register_source(history, "source:observer", OBSERVER_BYTES)
    append(history, "outcome-contract", contract_event(history))
    register_source(history, "source:observed", SOURCE_BYTES)
    return history.path.read_bytes()


@pytest.fixture(scope="module")
def executed(tmp_path_factory):
    extend = import_module(
        "research.action_history_contract_freeze.programs.observation_bundle"
    ).add_observation
    bundle = extend(
        add_execution(add_dispatch(receipts.dispatching.authorization.build_bundle()))
    )
    content = receipts.dispatched_prefix(
        tmp_path_factory.mktemp("observation-base"), bundle
    )
    prefixes = {}
    for status in ("SUCCEEDED", "FAILED"):
        history = reopen(tmp_path_factory.mktemp("observation-inputs"), content)
        receipts.execute(history, receipts.event(history, status))
        prefixes[status] = observer_inputs(history)
    return prefixes, content


def event(history):
    values = {
        k: v["record"]
        for k, v in history.replay().protocol_replay.data["records"].items()
    }
    execution, contract, observed = (
        values["execution:1"],
        values["outcome-contract:1"],
        values["source:observed"],
    )
    value = make_record(
        "OutcomeObservation",
        id="observation:1",
        event_id="event:observation",
        generated_at=TIME,
        actor_id="actor:observer",
        role="outcome-observer",
        source_record_ids=[execution["id"], contract["id"], observed["id"]],
        execution_id=execution["id"],
        execution_hash=execution["content_hash"],
        outcome_contract_id=contract["id"],
        outcome_contract_hash=contract["content_hash"],
        observer_id="actor:observer",
        observation_type=contract["observation_type"],
        observation_result="CONFIRMED",
        observed_at=TIME,
        observed_source_artifact_id=observed["id"],
        observed_source_artifact_hash=observed["content_hash"],
    )
    result = draft("OutcomeObservation", value)
    result["event_type"] = "OUTCOME_OBSERVED"
    return result


@pytest.mark.parametrize("status", ["SUCCEEDED", "FAILED"])
def test_independent_observation_after_either_receipt_preserves_domain(
    tmp_path, executed, status
):
    history = reopen(tmp_path, executed[0][status])
    before = history.replay()
    after = append(history, "observation", event(history))
    assert after.protocol_replay.data["state"]["protocol"][
        "observation_by_execution_contract"
    ] == [{"keys": ["execution:1", "outcome-contract:1"], "value": "observation:1"}]
    assert after.graph.export_records() == before.graph.export_records()
    assert after.change_sets == before.change_sets
    assert after.acceptance_head == before.acceptance_head
    assert after.materialization_head == before.materialization_head
    reopened = KnowledgeChangeHistory.reopen(history.path).replay()
    assert reopened.receipt == after.receipt
    assert reopened.retained_bytes("source:observed") == SOURCE_BYTES
    assert reopened.retained_bytes("execution:1") != SOURCE_BYTES


@pytest.mark.parametrize(
    "fault",
    [
        "executor-observer",
        "blank-observer",
        "execution",
        "contract",
        "source",
        "type",
        "result",
        "time",
        "observation-time",
        "provenance",
        "duplicate",
    ],
)
def test_observation_refuses_receipt_or_misbinding_as_independent_evidence(
    tmp_path, executed, fault
):
    history = reopen(tmp_path, executed[0]["SUCCEEDED"])
    candidate = event(history)
    value = candidate["data"]["records"]["value"][0]["record"]
    if fault == "executor-observer":
        value["observer_id"] = value["responsible_actor_id"] = candidate["actor_id"] = (
            "actor:executor"
        )
    elif fault == "blank-observer":
        value["observer_id"] = " "
    elif fault in ("execution", "contract"):
        key = "execution_hash" if fault == "execution" else "outcome_contract_hash"
        value[key] = content_digest("wrong")
    elif fault == "source":
        execution = history.replay().protocol_replay.data["records"]["execution:1"][
            "record"
        ]
        value["observed_source_artifact_id"], value["observed_source_artifact_hash"] = (
            execution["id"],
            execution["content_hash"],
        )
    elif fault == "type":
        value["observation_type"] = "DIFFERENT_CHECK"
    elif fault == "result":
        value["observation_result"] = "SUCCEEDED"
    elif fault == "time":
        value["observed_at"] = value["generated_at"] = candidate["transaction_time"] = (
            "2026-09-07T00:19:00Z"
        )
    elif fault == "observation-time":
        value["observed_at"] = "2026-09-07T00:19:00Z"
    elif fault == "provenance":
        candidate["data"]["dependencies"]["value"] = []
    else:
        append(history, "observation", deepcopy(candidate))
        value["id"] = "observation:duplicate"
        value["generation_event_id"] = candidate["event_id"] = (
            "event:observation:duplicate"
        )
    value["content_hash"] = record_hash("OutcomeObservation", value)
    before = history.path.read_bytes()
    # The owning ledger rejects backward event time before the finite program.
    error = KnowledgeChangeRefusal if fault == "time" else api().ProtocolProgramRefusal
    reason = "transaction_time decreased" if fault == "time" else None
    with pytest.raises(error, match=reason):
        append(history, "observation", candidate)
    assert history.path.read_bytes() == before


@pytest.mark.parametrize("fault", ["preimage", "implementation", "blank-type", "blank-version"])
def test_outcome_contract_requires_its_actual_semantic_and_implementation_identity(
    tmp_path, executed, fault
):
    history = reopen(tmp_path, executed[1])
    register_source(history, "source:observer", OBSERVER_BYTES)
    candidate = contract_event(history)
    value = candidate["data"]["records"]["value"][0]["record"]
    if fault == "preimage":
        candidate["data"]["preimage"]["value"]["observation_type"] = "OTHER"
    elif fault == "implementation":
        value["observer_implementation_hash"] = content_digest("other implementation")
        candidate["data"]["preimage"]["value"]["observer_implementation_hash"] = value[
            "observer_implementation_hash"
        ]
        value["artifact_hash"] = content_digest(candidate["data"]["preimage"]["value"])
    else:
        field = "observation_type" if fault == "blank-type" else "artifact_version"
        pre = "observation_type" if fault == "blank-type" else "contract_version"
        value[field] = candidate["data"]["preimage"]["value"][pre] = " "
        value["artifact_hash"] = content_digest(candidate["data"]["preimage"]["value"])
    value["content_hash"] = record_hash("OutcomeContractArtifact", value)
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal):
        append(history, "outcome-contract", candidate)
    assert history.path.read_bytes() == before
