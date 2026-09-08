"""Finite outcome-contract and independent-observation admission, no effects."""

from copy import deepcopy

from malleus._contract_pipeline.protocol_runtime import canonical, load_bundle
from research.action_history_contract_freeze.programs.assessment_bundle import (
    TEXT,
    DIGEST,
    array,
)
from research.action_history_contract_freeze.programs.dispatch_bundle import (
    add_record_stage,
    supplied,
    record,
    resolved,
    state,
    resolve_step,
    require_indexes,
    compare_time,
    introduction,
)
from research.action_history_contract_freeze.programs.registration_bundle import (
    obj,
    compare,
)


def _metadata(bundle, count):
    fields = bundle["profile"]["record_schemas"]["SourceArtifact"]["properties"]
    return {
        **{
            k: deepcopy(fields[k])
            for k in (
                "id",
                "content_hash",
                "generation_event_id",
                "generated_at",
                "responsible_actor_id",
                "responsible_role",
            )
        },
        "source_record_ids": {**array(TEXT, count), "uniqueItems": True},
    }


def _add_contract(bundle):
    schema = obj(
        **_metadata(bundle, 1),
        artifact_kind={**TEXT, "const": "OUTCOME_CONTRACT"},
        artifact_version={**TEXT, "format": "nonblank"},
        artifact_hash=DIGEST,
        outcome_contract_schema_version={**TEXT, "const": "1"},
        observation_type={**TEXT, "format": "nonblank"},
        observer_implementation_hash=DIGEST,
    )
    inputs, steps, setting = add_record_stage(
        bundle,
        "outcome_contract",
        "OutcomeContractArtifact",
        schema,
        role="registrar",
        references={"implementation": "SourceArtifact"},
        indexes={"outcome_contracts": 1},
    )
    fields = {
        "outcome_contract_schema_version": "outcome_contract_schema_version",
        "contract_id": "id",
        "contract_version": "artifact_version",
        "observation_type": "observation_type",
        "observer_implementation_hash": "observer_implementation_hash",
    }
    data = inputs["event"]["0"]["properties"]["data"]
    data["properties"].update(
        preimage=obj(
            value=obj(
                **{k: deepcopy(schema["properties"][v]) for k, v in fields.items()}
            )
        ),
        implementation=obj(id=TEXT, record_hash=DIGEST),
    )
    data["required"] += ["preimage", "implementation"]
    steps.append(
        resolve_step(
            "implementation",
            supplied("implementation", "id"),
            supplied("implementation", "record_hash"),
            setting,
        )
    )
    for pre, field in fields.items():
        steps.append(
            compare(
                supplied("preimage", "value", pre),
                record(field),
                "MISBOUND_OUTCOME_CONTRACT_PREIMAGE",
            )
        )
    steps += [
        {
            "opcode": "HASH",
            "recipe": "VALUE",
            "value": supplied("preimage", "value"),
            "result": "artifact-hash",
            "refusal": "INVALID_OUTCOME_CONTRACT_PREIMAGE",
        },
        compare(
            resolved("artifact-hash"),
            record("artifact_hash"),
            "WRONG_OUTCOME_CONTRACT_HASH",
            "DIGEST",
        ),
        compare(
            record("observer_implementation_hash"),
            resolved("implementation", "source_content_digest"),
            "WRONG_OBSERVER_IMPLEMENTATION",
            "DIGEST",
        ),
        compare(
            record("source_record_ids", 0),
            resolved("implementation", "id"),
            "MISSING_OBSERVER_IMPLEMENTATION",
        ),
    ]
    steps += introduction("outcome_contracts", ("id",))
    bundle["transactions"]["outcome-contract"] = {
        "event_types": ["PREREQUISITE_RECORDED"],
        "program": {
            "name": "retain-outcome-contract",
            "inputs": inputs,
            "required_capabilities": [],
            "introductions": [{"name": "outcome-contract", "depends_on": []}],
            "steps": steps,
        },
    }


def add_observation(bundle):
    bundle = deepcopy(bundle)
    _add_contract(bundle)
    schema = obj(
        **_metadata(bundle, 3),
        execution_id=TEXT,
        execution_hash=DIGEST,
        outcome_contract_id=TEXT,
        outcome_contract_hash=DIGEST,
        observer_id={**TEXT, "format": "nonblank"},
        observation_type={**TEXT, "format": "nonblank"},
        observation_result={
            **TEXT,
            "enum": ["CONFIRMED", "CONTRADICTED", "INDETERMINATE"],
        },
        observed_at={**TEXT, "format": "aware-instant"},
        observed_source_artifact_id=TEXT,
        observed_source_artifact_hash=DIGEST,
    )
    inputs, steps, setting = add_record_stage(
        bundle,
        "observation",
        "OutcomeObservation",
        schema,
        role="outcome-observer",
        references={
            "execution": "ActionExecution",
            "contract": "OutcomeContractArtifact",
            "source": "SourceArtifact",
        },
        indexes={"observation_by_execution_contract": 2},
    )
    require_indexes(inputs, ("execution_by_dispatch", "outcome_contracts"))
    for name, identifier, identity in (
        ("execution", "execution_id", "execution_hash"),
        ("contract", "outcome_contract_id", "outcome_contract_hash"),
        ("source", "observed_source_artifact_id", "observed_source_artifact_hash"),
    ):
        steps.append(resolve_step(name, record(identifier), record(identity), setting))
        steps.append(
            {
                "opcode": "REQUIRE_MEMBER",
                "value_kind": "STRING",
                "value": resolved(name, "id"),
                "members": record("source_record_ids"),
                "refusal": "MISSING_OBSERVATION_SOURCE",
            }
        )
    steps += [
        compare(
            state("execution_by_dispatch", 0, "keys", 0),
            resolved("execution", "dispatch_id"),
            "UNAPPLIED_EXECUTION",
        ),
        compare(
            state("execution_by_dispatch", 0, "value"),
            resolved("execution", "id"),
            "UNAPPLIED_EXECUTION",
        ),
        compare(
            state("outcome_contracts", 0, "keys", 0),
            resolved("contract", "id"),
            "UNAPPLIED_OUTCOME_CONTRACT",
        ),
        compare(
            state("outcome_contracts", 0, "value"),
            resolved("contract", "id"),
            "UNAPPLIED_OUTCOME_CONTRACT",
        ),
        compare(
            record("observation_type"),
            resolved("contract", "observation_type"),
            "WRONG_OBSERVATION_TYPE",
        ),
        compare(
            record("observer_id"),
            record("responsible_actor_id"),
            "OBSERVER_MUST_RECORD",
        ),
        {
            **compare(
                record("observer_id"),
                resolved("execution", "executor_id"),
                "OBSERVER_NOT_INDEPENDENT",
            ),
            "comparison": "NE",
        },
        compare_time(
            record("observed_at"),
            record("generated_at"),
            "EQ",
            "WRONG_OBSERVATION_TIME",
        ),
        compare_time(
            resolved("execution", "execution_ended_at"),
            record("observed_at"),
            "LE",
            "OBSERVATION_BEFORE_EXECUTION",
        ),
    ]
    steps += introduction(
        "observation_by_execution_contract", ("execution_id", "outcome_contract_id")
    )
    bundle["transactions"]["observation"] = {
        "event_types": ["OUTCOME_OBSERVED"],
        "program": {
            "name": "record-independent-observation",
            "inputs": inputs,
            "required_capabilities": [],
            "introductions": [{"name": "observation", "depends_on": []}],
            "steps": steps,
        },
    }
    return load_bundle(canonical(bundle))
