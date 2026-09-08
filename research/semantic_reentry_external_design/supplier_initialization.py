"""Register supplier prerequisites through the existing one-history owner.

This coordinator does not run checks or effects. Static validation precedes
retention; each subsequent append has Core's atomicity, not workflow atomicity.
"""

from datetime import datetime
from hashlib import sha256
import json

import malleus.compiler as api
from malleus.assent import make_record
from malleus.control import (
    authorization_policy_digest,
    authorization_policy_requirements,
    epistemic_policy_digest,
    monitor_specification_digest,
    policy_requirements,
)
from malleus.ledger import canonical_json, content_digest
from malleus.source import source_artifact_fields
from malleus._contract_pipeline.protocol_runtime import raw
from research.action_history_contract_freeze.programs.check_executor import (
    CheckExecutor,
)
from research.action_history_contract_freeze.programs.registration_bundle import (
    SOURCE_PROJECTION,
)
from research.semantic_reentry_external_design.supplier_program import (
    build_supplier_program,
)


CONTROL_SCHEMA = "malleus.reentry.supplier.epistemic-control/research-v1"


class SupplierInitializationError(ValueError):
    def __init__(self, reason, detail):
        self.reason, self.detail = reason, detail
        super().__init__(f"{reason}: {detail}")


def _canonical(value):
    return canonical_json(value).encode()


def _closed(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise ValueError("required closed fields: " + ", ".join(sorted(fields)))


def _draft(kind, value, *, preimage=None, content=None, encoding="BYTES"):
    data = {
        "records": {"value": [{"record_type": kind, "record": value}]},
        "dependencies": {"value": value["source_record_ids"]},
    }
    if preimage is not None:
        data["preimage"] = {"value": preimage}
    if kind == "SourceArtifact":
        data["preimage"] = {
            "value": {k: value[v] for k, v in SOURCE_PROJECTION.items()}
        }
    retained = {}
    if content is not None:
        retained["source"] = {
            "record_id": value["id"],
            "content": content,
            "media_type": "application/json",
            "role": "SOURCE_ARTIFACT"
            if kind == "SourceArtifact"
            else "RETAINED_EVIDENCE",
            "encoding": encoding,
        }
    return {
        "event_id": value["generation_event_id"],
        "event_type": "PREREQUISITE_RECORDED",
        "actor_id": value["responsible_actor_id"],
        "transaction_time": value["generated_at"],
        "data": data,
        "retained": retained,
    }


def initialize_supplier_protocol(
    *,
    history,
    expected_head,
    expected_count,
    program_bytes,
    program_record_id,
    selection_event_id,
    initialization_id,
    checker,
    checker_source_ids,
    monitor_ids,
    ruleset_id,
    epistemic_control_bytes,
    transaction_time,
    actor_id,
    artifact_version,
):
    """Return Core's replay after one explicit supplier-profile initialization."""
    if type(history) is not api.KnowledgeChangeHistory:
        raise SupplierInitializationError(
            "MALFORMED_INPUT", "owning public Core history required"
        )
    before = history.replay()
    if type(expected_count) is not int or expected_count < 0:
        raise SupplierInitializationError(
            "MALFORMED_INPUT", "explicit integer event count required"
        )
    if (expected_head, expected_count) != (
        before.ledger_head,
        before.ledger_event_count,
    ):
        raise SupplierInitializationError(
            "STALE_BASE", "initial history head/count differ"
        )
    if before.protocol_replay is not None:
        raise SupplierInitializationError(
            "ALREADY_SELECTED", "this initializer never replaces a selected program"
        )

    try:
        if type(checker) is not CheckExecutor:
            raise ValueError("actual identified Core CheckExecutor required")
        # Revalidate its declared bytes before reading its implementation reference.
        checker = CheckExecutor(checker.definition_bytes, checker.implementation_bytes)
        implementation_hash = checker.implementation_reference["bytes_sha256"]
        _closed(checker_source_ids, ("definition", "implementation"))
        _closed(monitor_ids, ("epistemic", "authorization"))
        for ids in monitor_ids.values():
            if (
                type(ids) is not list
                or len(ids) != 2
                or any(type(i) is not str for i in ids)
                or ids != sorted(set(ids))
            ):
                raise ValueError("two unique canonical monitor IDs per policy required")
        if type(program_bytes) is not bytes:
            raise ValueError("exact canonical supplier program bytes required")
        bundle = json.loads(program_bytes)
        if _canonical(bundle) != program_bytes:
            raise ValueError("canonical supplier program bytes required")
        selected = bundle["constants"]["initialization"]
        source_ids, policy_ids = selected["sources"], selected["policies"]
        _closed(
            source_ids, ("profile", "record_contract", "machine", "history_binding")
        )
        _closed(policy_ids, ("epistemic", "authorization"))
        contract_bytes = raw(bundle["record_contract_base64"])
        view = api.load_validated_contract_artifact(contract_bytes)
        if type(epistemic_control_bytes) is not bytes:
            raise ValueError("exact canonical epistemic control bytes required")
        control = json.loads(epistemic_control_bytes)
        _closed(
            control,
            ("schema", "violation_verdicts", "unknown_verdicts", "control_precedence"),
        )
        if (
            control["schema"] != CONTROL_SCHEMA
            or _canonical(control) != epistemic_control_bytes
        ):
            raise ValueError("unsupported or noncanonical epistemic control")
        for key in ("violation_verdicts", "unknown_verdicts", "control_precedence"):
            if type(control[key]) is not list:
                raise ValueError("epistemic control arrays required")
        identifiers = [
            program_record_id,
            initialization_id,
            ruleset_id,
            *checker_source_ids.values(),
            *source_ids.values(),
            *policy_ids.values(),
            *monitor_ids["epistemic"],
            *monitor_ids["authorization"],
        ]
        for value in (
            *identifiers,
            selection_event_id,
            transaction_time,
            actor_id,
            artifact_version,
        ):
            if type(value) is not str or not value.strip():
                raise ValueError(
                    "nonblank identities, time, actor and version required"
                )
        instant = datetime.fromisoformat(transaction_time)
        if instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError("timezone-aware transaction time required")
        used = {item.record_id for item in before.retained_inputs} | set(
            before.record_history
        )
        if len(set(identifiers)) != len(identifiers) or used.intersection(identifiers):
            raise SupplierInitializationError(
                "DUPLICATE_ID", "distinct unused record IDs required"
            )
        if selection_event_id in {"event:" + i for i in identifiers}:
            raise SupplierInitializationError(
                "DUPLICATE_ID", "selection and generated record events must differ"
            )

        def record(kind, identifier, sources, **fields):
            value = make_record(
                kind,
                id=identifier,
                event_id="event:" + identifier,
                generated_at=transaction_time,
                actor_id=actor_id,
                role="registrar",
                source_record_ids=sorted(sources),
                **fields,
            )
            errors = view.validate_instance(kind, value)
            if errors:
                raise ValueError(
                    f"{kind} does not conform to selected compiled contract: {errors}"
                )
            return value

        def source(identifier, content, sources):
            return record(
                "SourceArtifact",
                identifier,
                sources,
                artifact_kind="SOURCE",
                artifact_version=artifact_version,
                **source_artifact_fields(
                    artifact_id=identifier,
                    artifact_version=artifact_version,
                    source_bytes=content,
                    media_type="application/json",
                    locator="urn:retained:" + identifier,
                ),
            )

        drafts, checks = [], []
        for role in ("definition", "implementation"):
            content = getattr(checker, role + "_bytes")
            value = source(checker_source_ids[role], content, [])
            checks.append(value)
            drafts.append(("source", _draft("SourceArtifact", value, content=content)))
        checks.sort(key=lambda value: value["id"])
        ruleset = record(
            "ProtocolArtifact",
            ruleset_id,
            [],
            artifact_kind="RULE_SET",
            artifact_version=artifact_version,
            artifact_hash="sha256:" + sha256(epistemic_control_bytes).hexdigest(),
        )
        drafts.append(
            (
                "ruleset",
                _draft("ProtocolArtifact", ruleset, content=epistemic_control_bytes),
            )
        )
        policies = {}
        for role, assessment_kind in (
            ("epistemic", "TYPE"),
            ("authorization", "AUTHORITY"),
        ):
            monitors = []
            for identifier in monitor_ids[role]:
                semantics = dict(
                    schema_version="1",
                    monitor_id=identifier,
                    monitor_version=artifact_version,
                    assessment_kind=assessment_kind,
                    implementation_hash=implementation_hash,
                    input_artifact_ids=[r["id"] for r in checks],
                    input_artifact_record_hashes=[r["content_hash"] for r in checks],
                )
                value = record(
                    "MonitorSpecificationArtifact",
                    identifier,
                    semantics["input_artifact_ids"],
                    artifact_kind="MONITOR_SPECIFICATION",
                    artifact_version=artifact_version,
                    artifact_hash=monitor_specification_digest(**semantics),
                    monitor_schema_version="1",
                    assessment_kind=assessment_kind,
                    monitor_implementation_hash=implementation_hash,
                    input_artifact_ids=semantics["input_artifact_ids"],
                    input_artifact_record_hashes=semantics[
                        "input_artifact_record_hashes"
                    ],
                )
                preimage = {
                    k: v
                    for k, v in semantics.items()
                    if not k.startswith("input_artifact_")
                }
                preimage["input_artifacts"] = [
                    {"id": r["id"], "record_hash": r["content_hash"]} for r in checks
                ]
                drafts.append(
                    (
                        "monitor",
                        _draft(
                            "MonitorSpecificationArtifact", value, preimage=preimage
                        ),
                    )
                )
                monitors.append(value)
            semantics = dict(
                schema_version="1",
                policy_id=policy_ids[role],
                policy_version=artifact_version,
                required_monitor_ids=[r["id"] for r in monitors],
                required_monitor_record_hashes=[r["content_hash"] for r in monitors],
            )
            fields = {
                "artifact_version": artifact_version,
                "policy_schema_version": "1",
                "required_monitor_ids": semantics["required_monitor_ids"],
                "required_monitor_record_hashes": semantics[
                    "required_monitor_record_hashes"
                ],
            }
            provenance = fields["required_monitor_ids"][:]
            preimage = {
                k: semantics[k]
                for k in ("schema_version", "policy_id", "policy_version")
            }
            if role == "epistemic":
                extra = {
                    "ruleset_id": ruleset_id,
                    "ruleset_record_hash": ruleset["content_hash"],
                    "ruleset_artifact_hash": ruleset["artifact_hash"],
                    **{
                        k: control[k]
                        for k in (
                            "violation_verdicts",
                            "unknown_verdicts",
                            "control_precedence",
                        )
                    },
                }
                fields.update(
                    extra,
                    artifact_kind="EPISTEMIC_POLICY",
                    artifact_hash=epistemic_policy_digest(**semantics, **extra),
                )
                preimage.update(
                    {
                        k: extra[k]
                        for k in (
                            "ruleset_id",
                            "ruleset_record_hash",
                            "ruleset_artifact_hash",
                            "control_precedence",
                        )
                    }
                )
                preimage["requirements"] = policy_requirements(fields)
                provenance.append(ruleset_id)
                kind = "EpistemicPolicyArtifact"
            else:
                fields.update(
                    artifact_kind="AUTHORIZATION_POLICY",
                    artifact_hash=authorization_policy_digest(**semantics),
                )
                preimage.update(
                    requirements=authorization_policy_requirements(fields),
                    outcome_controls={
                        "SATISFIED": "AUTHORIZE",
                        "VIOLATED": "BLOCK",
                        "UNKNOWN": "CLARIFY",
                    },
                    control_precedence=["BLOCK", "CLARIFY", "AUTHORIZE"],
                )
                kind = "AuthorizationPolicyArtifact"
            value = record(kind, policy_ids[role], provenance, **fields)
            policies[role] = value
            drafts.append((role, _draft(kind, value, preimage=preimage)))
        sources = {}
        for role, content in {
            "profile": _canonical(bundle["profile"]),
            "record_contract": contract_bytes,
            "machine": program_bytes,
            "history_binding": history.binding.canonical_bytes,
        }.items():
            value = source(source_ids[role], content, [])
            sources[role] = value
            drafts.append(("source", _draft("SourceArtifact", value, content=content)))
        anchor = api.structural_evidence_anchor(
            record_id=program_record_id,
            content=program_bytes,
            media_type="application/json",
        )
        # Full finite-program validation happens inside the builder. Defer this
        # expensive check until malformed static inputs have already refused.
        if (
            build_supplier_program(
                contract_bytes, source_ids=source_ids, policy_ids=policy_ids
            )
            != program_bytes
        ):
            raise SupplierInitializationError(
                "UNSUPPORTED", "exact reviewed supplier program variant required"
            )
    except SupplierInitializationError:
        raise
    except (ValueError, KeyError, TypeError, RecursionError) as error:
        raise SupplierInitializationError("MALFORMED_INPUT", str(error)) from error

    # One writer. No validation callback, check execution or source effect here.
    history.append_anchors(
        anchors=(anchor,), transaction_time=transaction_time, actor_id=actor_id
    )
    base = history.replay()
    current = history.select_protocol_programs(
        record_id=program_record_id,
        identity=content_digest(bundle),
        expected_head=base.ledger_head,
        expected_count=base.ledger_event_count,
        event_id=selection_event_id,
        transaction_time=transaction_time,
        actor_id=actor_id,
    )
    for transaction, draft in drafts:
        current = history.append_protocol_events(
            transaction=transaction,
            events=(draft,),
            expected_head=current.ledger_head,
            expected_count=current.ledger_event_count,
        )
    checkpoint = {
        "schema": "malleus.action-history.initialization/research-v1",
        "id": initialization_id,
        "prefix": {
            "head": current.ledger_head,
            "event_count": current.ledger_event_count,
        },
        "domain": {
            "effective_contract_identity": current.partial_contract.identity,
            "kcs_acceptance_head": current.acceptance_head,
            "materialization_head": current.materialization_head,
            "accepted_graph_digest": current.graph.state_digest(),
        },
        **{
            role: {"id": value["id"], "bytes_sha256": value["source_content_digest"]}
            for role, value in sources.items()
        },
        **{
            role + "_policy": {"id": value["id"], "record_hash": value["content_hash"]}
            for role, value in policies.items()
        },
    }
    content = _canonical(checkpoint)
    value = source(
        initialization_id,
        content,
        [v["id"] for v in (*sources.values(), *policies.values())],
    )
    draft = _draft("SourceArtifact", value, content=content, encoding="CANONICAL_JSON")
    draft["data"]["references"] = {
        role: {"id": v["id"], "record_hash": v["content_hash"]}
        for role, v in sources.items()
    }
    return history.append_protocol_events(
        transaction="initialize",
        events=(draft,),
        expected_head=current.ledger_head,
        expected_count=current.ledger_event_count,
    )
