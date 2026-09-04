"""Private, paper-v4-specific document experiment orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeHistoryBinding,
    KnowledgeChangeSet,
    KnowledgeValidTime,
)
from malleus._contract_pipeline.machine import (
    PolicyProgram,
    ProtocolMachineProgram,
    compose_normative_profile,
    compose_partial_effective_contract,
)
from malleus.kg import OpType
from malleus.ledger import LedgerError, aware_datetime, canonical_json

from .compiled_graph_recipe_contract import (
    derive_compiled_logical_contract,
    require_plan_contract_alignment,
)
from .document_run import (
    RetainedDocumentEvidence,
    RetainedDocumentSource,
    run_document_history,
)
from .graph_recipe_change_set import canonical_assembly_plan_bytes
from .ontology_compile import ExactSource, compile_exact_ontology
from .population_compile import PopulationRecipeProfile, compile_population


_XSD = "http://www.w3.org/2001/XMLSchema#"
_FACT_ORDER = {
    "Record": 0,
    "Property": 1,
    "RelationSource": 2,
    "RelationTarget": 3,
    "DependsOn": 4,
}
_POLICY_ID = "paper-v4-two-check-policy"
_ACTOR_ID = "actor:paper-v4-evaluator"
_PROPOSAL_ID = "proposal:paper-v4:population"
_DECISION_ID = "decision:paper-v4:population"
_PLAN_ID = "evidence:paper-v4:assembly-plan"
_PROVENANCE_ID = "evidence:paper-v4:population-provenance"
_SOURCE_ID = "source:paper-v4:selected-reading"
_EVIDENCE_IDS = {
    "ontology": "evidence:paper-v4:ontology-source",
    "malleus": "evidence:paper-v4:malleus-import",
    "linkml": "evidence:paper-v4:linkml-types",
    "compile": "evidence:paper-v4:ontology-compilation-receipt",
    "acceptance": "evidence:paper-v4:ontology-acceptance",
    "population": "evidence:paper-v4:population",
    "recipes": "evidence:paper-v4:generic-recipes",
}


class ExperimentRunError(ValueError):
    """The closed paper experiment cannot be admitted as requested."""


def _require_sha256(value: object, label: str) -> str:
    if (
        type(value) is not str
        or not value.startswith("sha256:")
        or len(value) != 71
        or any(character not in "0123456789abcdef" for character in value[7:])
    ):
        raise ExperimentRunError(f"{label} must be one lowercase sha256 digest")
    return value


def _require_nonblank(value: object, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise ExperimentRunError(f"{label} must be nonblank text")
    return value


@dataclass(frozen=True, slots=True)
class PaperExperimentConfiguration:
    """Every external coordinate required to build one document history."""

    result_schema: str
    source_sha256: str
    ontology_sha256: str
    reading_sha256: str
    malleus_import_sha256: str
    linkml_types_sha256: str
    population_sha256: str
    generic_recipe_sha256: str
    ontology_acceptance_sha256: str
    protocol_machine_sha256: str
    population_recipe_profile: PopulationRecipeProfile
    record_type_iris: tuple[str, ...]
    contract_id: str
    transaction_time: str
    ontology_locator: str
    malleus_import_locator: str
    linkml_types_locator: str

    def __post_init__(self) -> None:
        if type(self.population_recipe_profile) is not PopulationRecipeProfile:
            raise TypeError(
                "population_recipe_profile must be one PopulationRecipeProfile"
            )
        for field in (
            "result_schema",
            "contract_id",
            "transaction_time",
            "ontology_locator",
            "malleus_import_locator",
            "linkml_types_locator",
        ):
            _require_nonblank(getattr(self, field), field)
        try:
            aware_datetime(self.transaction_time, "transaction_time")
        except LedgerError as error:
            raise ExperimentRunError(str(error)) from error
        for field in (
            "source_sha256",
            "ontology_sha256",
            "reading_sha256",
            "malleus_import_sha256",
            "linkml_types_sha256",
            "population_sha256",
            "generic_recipe_sha256",
            "ontology_acceptance_sha256",
            "protocol_machine_sha256",
        ):
            _require_sha256(getattr(self, field), field)
        if (
            type(self.record_type_iris) is not tuple
            or not self.record_type_iris
            or any(
                type(value) is not str or not value.strip()
                for value in self.record_type_iris
            )
            or len(self.record_type_iris) != len(set(self.record_type_iris))
        ):
            raise ExperimentRunError(
                "record_type_iris must be one nonempty tuple of unique IRIs"
            )

    def input_identities(self) -> dict[str, str]:
        return {
            "acceptance": self.ontology_acceptance_sha256,
            "linkml": self.linkml_types_sha256,
            "malleus": self.malleus_import_sha256,
            "machine": self.protocol_machine_sha256,
            "ontology": self.ontology_sha256,
            "population": self.population_sha256,
            "reading": self.reading_sha256,
            "recipes": self.generic_recipe_sha256,
        }


@dataclass(frozen=True, slots=True)
class PaperExperimentRun:
    canonical_plan_bytes: bytes
    provenance_bytes: bytes
    replay_receipt_bytes: bytes
    result_bytes: bytes


@dataclass(frozen=True, slots=True)
class _Check:
    check_id: str
    contract_record_id: str
    contract_bytes: bytes
    receipt_record_id: str
    receipt_bytes: bytes


@dataclass(frozen=True, slots=True)
class _Verification:
    check_id: str
    predicate: str
    inputs: tuple[tuple[str, str], ...]


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _json_bytes(value: object) -> bytes:
    return canonical_json(value).encode("utf-8")


def _strict_json(source: bytes, label: str, *, newline: bool = False) -> dict[str, Any]:
    if type(source) is not bytes:
        raise ExperimentRunError(f"{label} must be exact bytes")
    try:
        value = json.loads(source.decode("utf-8"))
    except (UnicodeError, ValueError) as error:
        raise ExperimentRunError(f"{label} must be strict UTF-8 JSON") from error
    if type(value) is not dict:
        raise ExperimentRunError(f"{label} must be a JSON object")
    canonical = _json_bytes(value)
    allowed = (canonical, canonical + b"\n") if newline else (canonical,)
    if source not in allowed:
        raise ExperimentRunError(f"{label} must be canonical JSON")
    return value


def _require_build_inputs(
    configuration: PaperExperimentConfiguration,
    inputs: dict[str, bytes],
) -> None:
    if type(configuration) is not PaperExperimentConfiguration:
        raise TypeError("configuration must be one PaperExperimentConfiguration")
    if any(type(source) is not bytes for source in inputs.values()):
        raise ExperimentRunError("knowledge-build inputs must be exact bytes")
    expected = configuration.input_identities()
    observed = {name: _digest(source) for name, source in inputs.items()}
    drift = sorted(
        name
        for name in set(observed) | set(expected)
        if observed.get(name) != expected.get(name)
    )
    if drift:
        raise ExperimentRunError(f"knowledge-build input drift: {drift}")


def _acceptance(source: bytes, ontology_identity: str) -> None:
    value = _strict_json(source, "ontology acceptance", newline=True)
    expected = {
        "actor_id": _ACTOR_ID,
        "decision": "ACCEPT_FOR_POPULATION",
        "event_type": "ONTOLOGY_DECISION",
        "ontology_sha256": ontology_identity,
        "ordinal": 1,
        "schema": "malleus.paper-v4.ontology-decision/v1",
    }
    if value != expected:
        raise ExperimentRunError(
            "ontology acceptance must bind this ontology and the fixed evaluator event"
        )


def _history_binding() -> KnowledgeChangeHistoryBinding:
    return KnowledgeChangeHistoryBinding.from_bytes(
        _json_bytes(
            {
                "accept_verdict": "ACCEPT",
                "decision": {
                    "event_type": "VERDICT_RECORDED",
                    "proposal_id_field": "proposal_id",
                    "record_type": "DecisionRecord",
                    "verdict_field": "verdict",
                },
                "grammar": "malleus.knowledge-history-binding/private-v0",
                "proposal": {
                    "change_set_identity_field": "knowledge_change_set_identity",
                    "event_type": "CHANGE_PROPOSED",
                    "proposal_id_field": "proposal_id",
                    "record_type": "ProposalRecord",
                },
                "retention_events": {
                    "ARTIFACT_REGISTERED": {
                        "identity_field": "artifact_identity",
                        "record_id_field": "artifact_id",
                    },
                    "SOURCE_REGISTERED": {
                        "identity_field": "source_identity",
                        "record_id_field": "source_id",
                    },
                },
            }
        )
    )


def _rdf_term(value: object) -> dict[str, str]:
    if type(value) is int:
        return {
            "datatype": _XSD + "integer",
            "kind": "literal",
            "lexical_form": str(value),
        }
    if type(value) is float:
        return {
            "datatype": _XSD + "float",
            "kind": "literal",
            "lexical_form": json.dumps(value, allow_nan=False),
        }
    if type(value) is str:
        return {
            "datatype": _XSD + "string",
            "kind": "literal",
            "lexical_form": value,
        }
    raise ExperimentRunError("population property has no supported RDF term")


def _verify_source_provenance(
    population_bytes: bytes,
    reading: dict[str, Any],
    reading_bytes: bytes,
    provenance_bytes: bytes,
    plan: Any,
    contract: Any,
    provenance_schema: str,
) -> _Verification:
    population = json.loads(population_bytes)
    provenance = _strict_json(provenance_bytes, "population provenance")
    reading_identity = _digest(reading_bytes)
    if (
        set(provenance)
        != {"assertions", "ontology_sha256", "plan_sha256", "reading_sha256", "schema"}
        or provenance["schema"] != provenance_schema
        or population["reading_sha256"] != reading_identity
        or provenance["reading_sha256"] != reading_identity
        or provenance["ontology_sha256"] != population["ontology_sha256"]
        or provenance["plan_sha256"] != plan.plan_digest
    ):
        raise ExperimentRunError("population provenance does not bind its inputs")

    records = population["records"]
    record_ids = [record["record_id"] for record in records]
    members = {member.record_id: member for member in plan.members}
    operations = dict(zip(plan.operation_members, plan.operations, strict=True))
    lineage_items = dict(plan.member_emissions)
    member_ids = {member.member for member in plan.members}
    if (
        len(record_ids) != len(set(record_ids))
        or len(members) != len(plan.members)
        or set(record_ids) != set(members)
        or len(operations) != len(plan.operations)
        or set(operations) != member_ids
        or len(lineage_items) != len(plan.member_emissions)
        or set(lineage_items) != member_ids
    ):
        raise ExperimentRunError("population records and plan members differ")
    lineage = {}
    for member, pairs in lineage_items.items():
        if len(pairs) != len(set(pairs)):
            raise ExperimentRunError("assembly plan repeats an emission lineage")
        lineage[member] = set(pairs)

    expected: dict[tuple[str, str, str | None], dict[str, Any]] = {}
    plan_facts: dict[str, list[dict[str, Any]]] = {member: [] for member in member_ids}
    for record in records:
        record_id = record["record_id"]
        record_contract = contract.record_for_symbol(record["record_type"])
        member = members[record_id]
        operation = operations[member.member]
        supplied = {
            name: located["value"] for name, located in record["properties"].items()
        }
        operation_properties = {
            slot.runtime_symbol: (
                slot.constraints.equals_string
                if slot.constraints.equals_string is not None
                else supplied[slot.runtime_symbol]
            )
            for slot in record_contract.operation_properties
            if slot.constraints.equals_string is not None
            or slot.runtime_symbol in supplied
        }
        source = record.get("source")
        target = record.get("target")
        operation_type = {
            "ENTITY": OpType.CREATE_ENTITY,
            "RELATION": OpType.CREATE_RELATION,
        }.get(record_contract.role)
        if (
            member.record_type != record_contract.type_iri
            or member.operation_kind != record_contract.legal_operation_kind
            or operation.op_type is not operation_type
            or operation.record_id != record_id
            or operation.record_type != record["record_type"]
            or canonical_json(operation.properties)
            != canonical_json(operation_properties)
            or operation.source_id
            != (source["record_id"] if source is not None else None)
            or operation.target_id
            != (target["record_id"] if target is not None else None)
        ):
            raise ExperimentRunError("population record and plan operation differ")

        record_fact = {
            "kind": "Record",
            "member": member.member,
            "operation_kind": member.operation_kind,
            "record_id": record_id,
            "record_type": member.record_type,
        }
        expected[("RECORD", record_id, None)] = {
            "block_id": record["record_block_id"],
            "fact": record_fact,
            "member": member.member,
        }
        plan_facts[member.member].append(record_fact)
        for name, value in operation_properties.items():
            plan_facts[member.member].append(
                {
                    "kind": "Property",
                    "member": member.member,
                    "property": contract.symbol_bindings.property_iri(name),
                    "value": _rdf_term(value),
                }
            )
        for name, located in record["properties"].items():
            expected[("PROPERTY", record_id, name)] = {
                "block_id": located["block_id"],
                "fact": {
                    "kind": "Property",
                    "member": member.member,
                    "property": contract.symbol_bindings.property_iri(name),
                    "value": _rdf_term(located["value"]),
                },
                "member": member.member,
            }
        for role, endpoint in (("SOURCE", source), ("TARGET", target)):
            if endpoint is not None:
                endpoint_fact = {
                    "kind": "Relation" + role.title(),
                    "member": member.member,
                    "record_id": endpoint["record_id"],
                }
                expected[(role, record_id, None)] = {
                    "block_id": endpoint["block_id"],
                    "fact": endpoint_fact,
                    "member": member.member,
                }
                plan_facts[member.member].extend(
                    (
                        endpoint_fact,
                        {
                            "kind": "DependsOn",
                            "member": member.member,
                            "prerequisite_member": members[
                                endpoint["record_id"]
                            ].member,
                        },
                    )
                )

    fact_by_lineage = {}
    for member, facts in plan_facts.items():
        ordered_facts = sorted(
            facts,
            key=lambda fact: (_FACT_ORDER[fact["kind"]], canonical_json(fact)),
        )
        ordered_emissions = sorted(lineage[member])
        if len(ordered_facts) != len(ordered_emissions):
            raise ExperimentRunError("assembly plan emission lineage is incomplete")
        for emission, fact in zip(ordered_emissions, ordered_facts, strict=True):
            fact_by_lineage[(member, *emission)] = fact

    observed = set()
    used_lineage = set()
    block_ids = {block["id"] for page in reading["pages"] for block in page["blocks"]}
    for assertion in provenance["assertions"]:
        kind = assertion.get("assertion_kind")
        fields = {
            "assertion_kind",
            "block_id",
            "emission_id",
            "emitted_fact",
            "expansion_path_id",
            "record_id",
        }
        fields |= {"property"} if kind == "PROPERTY" else set()
        fields |= {"endpoint_record_id"} if kind in {"SOURCE", "TARGET"} else set()
        if (
            kind not in {"RECORD", "PROPERTY", "SOURCE", "TARGET"}
            or set(assertion) != fields
        ):
            raise ExperimentRunError("population provenance claim is not closed")
        key = (
            kind,
            assertion["record_id"],
            assertion.get("property") if kind == "PROPERTY" else None,
        )
        if assertion["block_id"] not in block_ids:
            raise ExperimentRunError(
                "population provenance names an unknown reading block"
            )
        claim = expected.get(key)
        if claim is None or assertion["block_id"] != claim["block_id"]:
            raise ExperimentRunError("population and provenance locator claims differ")
        if (
            kind in {"SOURCE", "TARGET"}
            and assertion["endpoint_record_id"] != (claim["fact"]["record_id"])
        ):
            raise ExperimentRunError("population and provenance endpoint claims differ")
        if assertion["emitted_fact"] != claim["fact"]:
            raise ExperimentRunError("population and provenance semantic claims differ")
        emission = (assertion["emission_id"], assertion["expansion_path_id"])
        member_lineage = (claim["member"], *emission)
        if (
            emission not in lineage[claim["member"]]
            or fact_by_lineage.get(member_lineage) != claim["fact"]
            or member_lineage in used_lineage
        ):
            raise ExperimentRunError("population provenance emission lineage differs")
        observed.add(key)
        used_lineage.add(member_lineage)
    if observed != set(expected) or len(observed) != len(provenance["assertions"]):
        raise ExperimentRunError("population and provenance claims differ")
    return _Verification(
        "source-locator-integrity",
        "EVERY_POPULATION_CLAIM_JOINS_READING_PLAN_AND_EMISSION_LINEAGE",
        (
            (_SOURCE_ID, reading_identity),
            (_EVIDENCE_IDS["population"], _digest(population_bytes)),
            (_PLAN_ID, plan.plan_digest),
            (_PROVENANCE_ID, _digest(provenance_bytes)),
        ),
    )


def _verify_structure(
    plan: Any,
    contract: Any,
    compilation: Any,
    inputs: tuple[tuple[str, str], ...],
) -> _Verification:
    require_plan_contract_alignment(plan, contract, compilation)
    return _Verification(
        "structural-conformance",
        "ASSEMBLY_PLAN_ALIGNS_WITH_THE_VALIDATED_SELECTED_TYPE_CONTRACT",
        inputs,
    )


def _make_check(verification: _Verification) -> _Check:
    if type(verification) is not _Verification:
        raise ExperimentRunError("SATISFIED requires a completed verification")
    check_id = verification.check_id
    contract = _json_bytes(
        {
            "check_contract_id": check_id,
            "grammar": "malleus.paper-v4.check-contract/v1",
            "predicate": verification.predicate,
        }
    )
    receipt_id = f"receipt:paper-v4:{check_id}"
    receipt = _json_bytes(
        {
            "check_contract_id": check_id,
            "check_contract_identity": _digest(contract),
            "grammar": "malleus.paper-v4.check-result/v1",
            "inputs": [
                {"record_id": record_id, "sha256": identity}
                for record_id, identity in verification.inputs
            ],
            "outcome": "SATISFIED",
            "receipt_id": receipt_id,
        }
    )
    return _Check(
        check_id,
        f"evidence:paper-v4:check-contract:{check_id}",
        contract,
        f"evidence:paper-v4:check-result:{check_id}",
        receipt,
    )


def _policy(checks: tuple[_Check, ...]) -> PolicyProgram:
    return PolicyProgram.from_bytes(
        _json_bytes(
            {
                "grammar": "malleus.policy-program/private-v0",
                "outcome_verdicts": {
                    "SATISFIED": "ACCEPT",
                    "UNKNOWN": "DEFER",
                    "VIOLATED": "REJECT",
                },
                "policy_id": _POLICY_ID,
                "precedence": ["REJECT", "DEFER", "ACCEPT"],
                "required_checks": [
                    {
                        "check_contract_id": check.check_id,
                        "check_contract_identity": _digest(check.contract_bytes),
                    }
                    for check in checks
                ],
            }
        )
    )


def _event(event_type: str, **payload: object) -> bytes:
    return _json_bytes({"event_type": event_type, "payload": payload})


def _protocol_events(
    policy: PolicyProgram,
    checks: tuple[_Check, ...],
):
    def produce(
        change_set: KnowledgeChangeSet, machine_state_identity: str
    ) -> tuple[bytes, ...]:
        retained = dict((*change_set.sources, *change_set.evidence))
        events = [
            _event(
                "CHANGE_PROPOSED",
                expected_machine_state_identity=machine_state_identity,
                knowledge_change_set_identity=change_set.identity,
                policy_id=_POLICY_ID,
                policy_identity=policy.identity,
                proposal_id=_PROPOSAL_ID,
            )
        ]
        for check in checks:
            contract_identity = _digest(check.contract_bytes)
            if retained.get(check.contract_record_id) != contract_identity:
                raise ExperimentRunError("check contract is absent from KCS evidence")
            if retained.get(check.receipt_record_id) != _digest(check.receipt_bytes):
                raise ExperimentRunError("check result is absent from KCS evidence")
            receipt = _strict_json(check.receipt_bytes, "check result")
            if (
                receipt["check_contract_id"] != check.check_id
                or receipt["check_contract_identity"] != contract_identity
                or receipt["outcome"] != "SATISFIED"
                or any(
                    retained.get(item["record_id"]) != item["sha256"]
                    for item in receipt["inputs"]
                )
            ):
                raise ExperimentRunError(
                    "check result does not bind its contract and inputs"
                )
            events.append(
                _event(
                    "CHECK_RECORDED",
                    check_contract_id=receipt["check_contract_id"],
                    check_contract_identity=receipt["check_contract_identity"],
                    outcome=receipt["outcome"],
                    policy_identity=policy.identity,
                    proposal_id=_PROPOSAL_ID,
                    receipt_id=receipt["receipt_id"],
                )
            )
        events.append(
            _event(
                "VERDICT_RECORDED",
                decision_id=_DECISION_ID,
                proposal_id=_PROPOSAL_ID,
            )
        )
        return tuple(events)

    return produce


def run_paper_experiment(
    ledger_path: str | Path,
    *,
    configuration: PaperExperimentConfiguration,
    selected_ontology: ExactSource,
    malleus_import: ExactSource,
    linkml_types: ExactSource,
    selected_reading_bytes: bytes,
    population_bytes: bytes,
    generic_recipe_bytes: bytes,
    ontology_acceptance_bytes: bytes,
    protocol_machine_bytes: bytes,
) -> PaperExperimentRun:
    """Compile and admit one exact knowledge build without querying it."""

    path = Path(ledger_path)
    if path.exists():
        raise ExperimentRunError("ledger_path must be new")
    _require_build_inputs(
        configuration,
        {
            "acceptance": ontology_acceptance_bytes,
            "linkml": linkml_types.source_bytes,
            "malleus": malleus_import.source_bytes,
            "machine": protocol_machine_bytes,
            "ontology": selected_ontology.source_bytes,
            "population": population_bytes,
            "reading": selected_reading_bytes,
            "recipes": generic_recipe_bytes,
        },
    )
    reading = _strict_json(selected_reading_bytes, "selected reading", newline=True)
    if reading.get("source_sha256") != configuration.source_sha256:
        raise ExperimentRunError(
            "selected reading does not bind the configured source identity"
        )
    ontology_identity = _digest(selected_ontology.source_bytes)
    _acceptance(ontology_acceptance_bytes, ontology_identity)

    ontology = compile_exact_ontology(
        root=selected_ontology,
        malleus=malleus_import,
        linkml_types=linkml_types,
    )
    contract = derive_compiled_logical_contract(
        ontology.compilation,
        record_type_iris=configuration.record_type_iris,
        contract_id=configuration.contract_id,
    )
    population = compile_population(
        population_bytes,
        compiled_ontology=ontology.compilation,
        logical_contract=contract,
        generic_recipe_bytes=generic_recipe_bytes,
        selected_reading_bytes=selected_reading_bytes,
        recipe_profile=configuration.population_recipe_profile,
    )
    plan_bytes = canonical_assembly_plan_bytes(population.plan)
    entities = sum(
        op.op_type is OpType.CREATE_ENTITY for op in population.plan.operations
    )
    relations = sum(
        op.op_type is OpType.CREATE_RELATION for op in population.plan.operations
    )

    evidence = [
        RetainedDocumentEvidence(_EVIDENCE_IDS[name], content, media_type)
        for name, content, media_type in (
            ("ontology", selected_ontology.source_bytes, "application/yaml"),
            ("malleus", malleus_import.source_bytes, "application/yaml"),
            ("linkml", linkml_types.source_bytes, "application/yaml"),
            ("compile", ontology.receipt_bytes, "application/json"),
            ("acceptance", ontology_acceptance_bytes, "application/jsonl"),
            ("population", population_bytes, "application/json"),
            ("recipes", generic_recipe_bytes, "text/plain"),
        )
    ]
    evidence.extend(
        (
            RetainedDocumentEvidence(_PLAN_ID, plan_bytes, "application/json"),
            RetainedDocumentEvidence(
                _PROVENANCE_ID,
                population.provenance_map_bytes,
                "application/json",
            ),
        )
    )
    refs = {item.record_id: _digest(item.content) for item in evidence}
    source_check = _make_check(
        _verify_source_provenance(
            population_bytes,
            reading,
            selected_reading_bytes,
            population.provenance_map_bytes,
            population.plan,
            contract,
            configuration.population_recipe_profile.provenance_schema,
        )
    )
    structure_check = _make_check(
        _verify_structure(
            population.plan,
            contract,
            ontology.compilation,
            (
                (_EVIDENCE_IDS["ontology"], refs[_EVIDENCE_IDS["ontology"]]),
                (_EVIDENCE_IDS["compile"], refs[_EVIDENCE_IDS["compile"]]),
                (_EVIDENCE_IDS["recipes"], refs[_EVIDENCE_IDS["recipes"]]),
                (_PLAN_ID, refs[_PLAN_ID]),
            ),
        )
    )
    checks = (source_check, structure_check)
    evidence.extend(
        RetainedDocumentEvidence(record_id, content, "application/json")
        for check in checks
        for record_id, content in (
            (check.contract_record_id, check.contract_bytes),
            (check.receipt_record_id, check.receipt_bytes),
        )
    )

    policy = _policy(checks)
    machine = ProtocolMachineProgram.from_bytes(protocol_machine_bytes)
    profile = compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={"required-check-verdict": policy},
        capability_refs=(),
    )
    partial = compose_partial_effective_contract(
        validated_fact_set_sha256=ontology.compilation.artifact.validated_fact_set_sha256,
        normative_profile=profile,
    )
    run = run_document_history(
        path,
        plan=population.plan,
        partial_contract=partial,
        contract_view=ontology.compilation.view,
        binding=_history_binding(),
        source=RetainedDocumentSource(
            artifact_id="artifact:paper-v4:selected-reading",
            source_id=_SOURCE_ID,
            content=selected_reading_bytes,
            media_type="application/json",
        ),
        evidence=tuple(evidence),
        plan_evidence_id=_PLAN_ID,
        change_set_id="change:paper-v4:population",
        valid_time=KnowledgeValidTime("ORDER_ONLY", "population-1"),
        transaction_time=configuration.transaction_time,
        actor_id=_ACTOR_ID,
        protocol_events=_protocol_events(policy, checks),
    )
    decision = run.replay.machine_state.get_record("DecisionRecord", _DECISION_ID)
    if decision is None or decision.get("verdict") != "ACCEPT":
        raise ExperimentRunError("policy did not compute ACCEPT")
    if (run.replay.graph.node_count, run.replay.graph.edge_count) != (
        entities,
        relations,
    ):
        raise ExperimentRunError("replayed graph count differs from the admitted plan")
    result = _json_bytes(
        {
            "decision": "ACCEPT",
            "entity_count": entities,
            "ledger_head": run.replay.ledger_head,
            "ontology_sha256": ontology_identity,
            "reading_sha256": _digest(selected_reading_bytes),
            "relation_count": relations,
            "replay_receipt_sha256": run.replay.receipt.identity,
            "schema": configuration.result_schema,
            "source_sha256": configuration.source_sha256,
        }
    )
    return PaperExperimentRun(
        plan_bytes,
        population.provenance_map_bytes,
        run.replay.receipt.canonical_bytes,
        result,
    )


__all__ = [
    "ExperimentRunError",
    "PaperExperimentConfiguration",
    "PaperExperimentRun",
    "run_paper_experiment",
]
