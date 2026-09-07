"""Register real identified prerequisites through the owning finite history."""

from importlib import import_module

import pytest

from malleus.assent import make_record
from malleus.compiler import KnowledgeChangeHistory
from malleus.ledger import content_digest, record_hash
from malleus.source import source_artifact_fields
from research.action_history_contract_freeze.programs.check_executor import (
    load_check_executor,
)
from research.action_history_contract_freeze.programs.lifecycle.test_prerequisites import (
    compiled,
    existing_digest,
)
from tests.contract_compiler.pareto.test_finite_protocol_history import api, canonical
from tests.contract_compiler.pareto.test_knowledge_change_history import (
    _anchored_history,
    _evidence_anchor,
    TRANSACTION_TIME,
)


TIME = "2026-09-07T00:00:00Z"


def builder():
    return import_module(
        "research.action_history_contract_freeze.programs.registration_bundle"
    )


def record(kind, identifier, sources, **fields):
    return make_record(
        kind,
        id=identifier,
        event_id="event:" + identifier,
        generated_at=TIME,
        actor_id="actor:registrar",
        role="registrar",
        source_record_ids=sorted(sources),
        **fields,
    )


def append(history, transaction, draft):
    replay = history.replay()
    return history.append_protocol_events(
        transaction=transaction,
        events=(draft,),
        expected_head=replay.ledger_head,
        expected_count=replay.ledger_event_count,
    )


def draft(kind, value, *, preimage=None, content=None):
    data = {
        "records": {"value": [{"record_type": kind, "record": value}]},
        "dependencies": {"value": value["source_record_ids"]},
    }
    retained = {}
    if preimage is not None:
        data["preimage"] = {"value": preimage}
    if content is not None:
        retained["source"] = {
            "record_id": value["id"],
            "content": content,
            "media_type": "application/json",
            "role": "SOURCE_ARTIFACT"
            if kind == "SourceArtifact"
            else "RETAINED_EVIDENCE",
            "encoding": "BYTES",
        }
    return {
        "event_id": value["generation_event_id"],
        "event_type": "PREREQUISITE_RECORDED",
        "actor_id": value["responsible_actor_id"],
        "transaction_time": value["generated_at"],
        "data": data,
        "retained": retained,
    }


def setup(tmp_path):
    history = _anchored_history(tmp_path)[0]
    bundle = builder().build_registration_bundle(compiled().artifact_bytes)
    history.append_anchors(
        anchors=(_evidence_anchor("registered-programs", canonical(bundle)),),
        transaction_time=TRANSACTION_TIME,
        actor_id="actor:test",
    )
    base = history.replay()
    history.select_protocol_programs(
        record_id="registered-programs",
        identity=content_digest(bundle),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
        event_id="event:select-programs",
        transaction_time=TIME,
        actor_id="actor:registrar",
    )
    return history, bundle


def source_inputs(history):
    engine = load_check_executor()
    records = []
    for identifier, content in (
        ("source:definition", engine.definition_bytes),
        ("source:implementation", engine.implementation_bytes),
    ):
        value = record(
            "SourceArtifact",
            identifier,
            [],
            artifact_kind="SOURCE",
            artifact_version="v1",
            **source_artifact_fields(
                artifact_id=identifier,
                artifact_version="v1",
                source_bytes=content,
                media_type="application/json",
                locator="urn:retained:" + identifier,
            ),
        )
        projection = builder().SOURCE_PROJECTION
        append(
            history,
            "source",
            draft(
                "SourceArtifact",
                value,
                preimage={k: value[v] for k, v in projection.items()},
                content=content,
            ),
        )
        records.append(value)
    return engine, records


def monitor(identifier, kind, engine, sources):
    value = record(
        "MonitorSpecificationArtifact",
        identifier,
        [s["id"] for s in sources],
        artifact_kind="MONITOR_SPECIFICATION",
        artifact_version="v1",
        artifact_hash=content_digest("pending"),
        monitor_schema_version="1",
        assessment_kind=kind,
        monitor_implementation_hash=engine.implementation_reference["bytes_sha256"],
        input_artifact_ids=[s["id"] for s in sources],
        input_artifact_record_hashes=[s["content_hash"] for s in sources],
    )
    value["artifact_hash"] = existing_digest("monitor", value)
    value["content_hash"] = record_hash("MonitorSpecificationArtifact", value)
    return value


def monitor_preimage(value):
    return {
        "schema_version": value["monitor_schema_version"],
        "monitor_id": value["id"],
        "monitor_version": value["artifact_version"],
        "assessment_kind": value["assessment_kind"],
        "implementation_hash": value["monitor_implementation_hash"],
        "input_artifacts": [
            {"id": i, "record_hash": h}
            for i, h in zip(
                value["input_artifact_ids"],
                value["input_artifact_record_hashes"],
                strict=True,
            )
        ],
    }


def policy(history, name, monitors, ruleset):
    fields = {
        "artifact_kind": "EPISTEMIC_POLICY"
        if name == "epistemic"
        else "AUTHORIZATION_POLICY",
        "artifact_version": "v1",
        "artifact_hash": content_digest("pending"),
        "policy_schema_version": "1",
        "required_monitor_ids": [r["id"] for r in monitors],
        "required_monitor_record_hashes": [r["content_hash"] for r in monitors],
    }
    sources = fields["required_monitor_ids"][:]
    preimage = {
        "schema_version": "1",
        "policy_id": "policy:" + name,
        "policy_version": "v1",
        "requirements": [
            {"monitor_id": r["id"], "monitor_record_hash": r["content_hash"]}
            for r in monitors
        ],
    }
    if name == "epistemic":
        extra = {
            "ruleset_id": ruleset["id"],
            "ruleset_record_hash": ruleset["content_hash"],
            "ruleset_artifact_hash": ruleset["artifact_hash"],
            "control_precedence": ["REJECT", "DEFER", "CONTEST"],
        }
        fields.update(
            extra,
            violation_verdicts=["REJECT", "REJECT"],
            unknown_verdicts=["DEFER", "DEFER"],
        )
        preimage.update(extra)
        for requirement in preimage["requirements"]:
            requirement.update(violation_verdict="REJECT", unknown_verdict="DEFER")
        sources.append(ruleset["id"])
    else:
        preimage.update(
            outcome_controls={
                "SATISFIED": "AUTHORIZE",
                "VIOLATED": "BLOCK",
                "UNKNOWN": "CLARIFY",
            },
            control_precedence=["BLOCK", "CLARIFY", "AUTHORIZE"],
        )
    kind = (
        "EpistemicPolicyArtifact"
        if name == "epistemic"
        else "AuthorizationPolicyArtifact"
    )
    value = record(kind, "policy:" + name, sources, **fields)
    value["artifact_hash"] = existing_digest(name, value)
    value["content_hash"] = record_hash(kind, value)
    append(history, name, draft(kind, value, preimage=preimage))
    return value


def prerequisites(history):
    engine, sources = source_inputs(history)
    content = canonical(
        {"rule": "selected monitors determine policy control, not source truth"}
    )
    ruleset = record(
        "ProtocolArtifact",
        "ruleset:1",
        [],
        artifact_kind="RULE_SET",
        artifact_version="v1",
        artifact_hash=api().digest(content),
    )
    append(history, "ruleset", draft("ProtocolArtifact", ruleset, content=content))
    policies = {}
    for name, kind in (("epistemic", "TYPE"), ("authorization", "AUTHORITY")):
        monitors = [
            monitor(f"monitor:{name}:{i}", kind, engine, sources) for i in range(2)
        ]
        for value in monitors:
            append(
                history,
                "monitor",
                draft(
                    "MonitorSpecificationArtifact",
                    value,
                    preimage=monitor_preimage(value),
                ),
            )
        policies[name] = policy(history, name, monitors, ruleset)
    return policies


def test_prerequisites_are_real_applied_records_bound_to_retained_bytes(tmp_path):
    history, bundle = setup(tmp_path)
    before = history.replay()
    policies = prerequisites(history)
    replay = KnowledgeChangeHistory.reopen(history.path).replay()
    assert replay.receipt == history.replay().receipt
    assert replay.graph.export_records() == before.graph.export_records()
    assert replay.acceptance_head == before.acceptance_head
    assert replay.protocol_replay.data["state"]["action_acceptance_head"] == "GENESIS"
    assert len(replay.protocol_replay.data["records"]) == 9
    for value in policies.values():
        assert replay.protocol_replay.data["records"][value["id"]]["record"] == value
    assert (
        replay.retained_bytes("source:implementation")
        == load_check_executor().implementation_bytes
    )
    assert set(bundle["transactions"]) == {
        "source",
        "ruleset",
        "grant",
        "monitor",
        "epistemic",
        "authorization",
    }


@pytest.mark.parametrize(
    "fault", ["unapplied", "hash", "semantic_hash", "preimage", "provenance"]
)
def test_real_monitor_registration_rejects_misbound_prerequisites(tmp_path, fault):
    history, _ = setup(tmp_path)
    engine, sources = source_inputs(history)
    value = monitor("monitor:bad", "TYPE", engine, sources)
    preimage = monitor_preimage(value)
    if fault == "unapplied":
        value["input_artifact_ids"][0] = "source:absent"
    elif fault == "hash":
        value["input_artifact_record_hashes"][0] = content_digest("wrong")
    elif fault == "semantic_hash":
        value["artifact_hash"] = content_digest("wrong")
    elif fault == "preimage":
        preimage["implementation_hash"] = content_digest("wrong")
    else:
        value["source_record_ids"] = []
    value["content_hash"] = record_hash("MonitorSpecificationArtifact", value)
    before = history.path.read_bytes()
    with pytest.raises(api().ProtocolProgramRefusal):
        append(
            history,
            "monitor",
            draft("MonitorSpecificationArtifact", value, preimage=preimage),
        )
    assert history.path.read_bytes() == before
