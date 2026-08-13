"""Ontology-preserving graph facts, pinned rule contracts, and logic-check records."""

from __future__ import annotations

import hashlib
import json
import math
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import yaml

from malleus.kg import KnowledgeGraph
from malleus.control import build_monitor_failure_records
from malleus.ledger import (
    LedgerError,
    content_digest,
    require_digest,
    with_content_hash,
)
from malleus.ontology import OntologyError, UniqueKeyLoader


CONTRACT_FIELDS = {
    "schema_version",
    "contract_id",
    "contract_version",
    "ontology_hash",
    "fact_contract_version",
    "ruleset_id",
    "ruleset_version",
    "rules_file",
    "rule_ids",
    "timeout_seconds",
}
FACT_PREDICATES = {
    "m_ontology_hash": 1,
    "m_type": 1,
    "m_mixin": 1,
    "m_subtype": 2,
    "m_has_mixin": 2,
    "m_record": 3,
    "m_relation": 4,
    "m_property": 4,
    "m_list": 3,
    "m_list_item": 5,
}
FACT_CONTRACT_VERSION = "2"


def fact_declarations() -> str:
    """Declare the complete input vocabulary, including predicates with no facts."""
    return "\n".join(
        f":- dynamic {predicate}/{arity}."
        for predicate, arity in sorted(FACT_PREDICATES.items())
    )


def logic_contract_digest(
    *,
    schema_version: str,
    contract_id: str,
    contract_version: str,
    ontology_hash: str,
    fact_contract_version: str,
    ruleset_id: str,
    ruleset_version: str,
    rule_ids: tuple[str, ...] | list[str],
    timeout_seconds: int,
    ruleset_hash: str,
) -> str:
    """Hash the canonical semantic contract represented in protocol replay."""
    return content_digest({
        "schema_version": schema_version,
        "contract_id": contract_id,
        "contract_version": contract_version,
        "ontology_hash": ontology_hash,
        "fact_contract_version": fact_contract_version,
        "ruleset_id": ruleset_id,
        "ruleset_version": ruleset_version,
        "rule_ids": sorted(rule_ids),
        "timeout_seconds": timeout_seconds,
        "ruleset_hash": ruleset_hash,
    })


class LogicError(ValueError):
    """A logic contract, graph compilation, or check record is invalid."""


class LogicExecutionError(LogicError):
    """The logic monitor did not complete and must not report a clean result."""


@dataclass(frozen=True)
class LogicContract:
    schema_version: str
    contract_id: str
    contract_version: str
    ontology_hash: str
    fact_contract_version: str
    ruleset_id: str
    ruleset_version: str
    rules_path: Path
    rules_source: str
    rule_ids: tuple[str, ...]
    timeout_seconds: int
    ruleset_hash: str
    contract_hash: str

    def validate_integrity(self) -> None:
        """Reject an in-memory contract whose pinned content was changed."""
        try:
            rules_bytes = self.rules_source.encode("utf-8")
        except UnicodeError as error:
            raise LogicError(f"rules_source is not valid UTF-8: {error}") from error
        ruleset_hash = "sha256:" + hashlib.sha256(rules_bytes).hexdigest()
        if self.ruleset_hash != ruleset_hash:
            raise LogicError("logic contract rules_source does not match ruleset_hash")
        expected = logic_contract_digest(
            schema_version=self.schema_version,
            contract_id=self.contract_id,
            contract_version=self.contract_version,
            ontology_hash=self.ontology_hash,
            fact_contract_version=self.fact_contract_version,
            ruleset_id=self.ruleset_id,
            ruleset_version=self.ruleset_version,
            rule_ids=self.rule_ids,
            timeout_seconds=self.timeout_seconds,
            ruleset_hash=self.ruleset_hash,
        )
        if self.contract_hash != expected:
            raise LogicError("logic contract fields do not match contract_hash")

    def to_protocol_artifact(
        self,
        *,
        event_id: str,
        generated_at: str,
        actor_id: str,
        role: str,
        ruleset_record_hash: str,
    ) -> dict[str, Any]:
        """Create the replay-visible artifact for this exact loaded contract."""
        self.validate_integrity()
        try:
            require_digest(ruleset_record_hash, "ruleset_record_hash")
        except LedgerError as error:
            raise LogicError(str(error)) from error
        for name, value in (
            ("event_id", event_id),
            ("generated_at", generated_at),
            ("actor_id", actor_id),
            ("role", role),
        ):
            _nonblank(value, name)
        return with_content_hash(
            "LogicContractArtifact",
            {
                "id": self.contract_id,
                "generation_event_id": event_id,
                "generated_at": generated_at,
                "responsible_actor_id": actor_id,
                "responsible_role": role,
                "source_record_ids": [self.ruleset_id],
                "artifact_kind": "LOGIC_CONTRACT",
                "artifact_version": self.contract_version,
                "artifact_hash": self.contract_hash,
                "logic_contract_schema_version": self.schema_version,
                "ontology_hash": self.ontology_hash,
                "fact_contract_version": self.fact_contract_version,
                "ruleset_id": self.ruleset_id,
                "ruleset_version": self.ruleset_version,
                "ruleset_record_hash": ruleset_record_hash,
                "ruleset_artifact_hash": self.ruleset_hash,
                "rule_ids": sorted(self.rule_ids),
                "timeout_seconds": self.timeout_seconds,
            },
        )

    @classmethod
    def load(cls, path: str | Path) -> "LogicContract":
        source_path = Path(path)
        try:
            document = yaml.load(source_path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
        except (OSError, UnicodeError, yaml.YAMLError, OntologyError) as error:
            raise LogicError(f"Cannot load logic contract '{source_path}': {error}") from error
        _exact_fields(document, CONTRACT_FIELDS, "logic contract")
        for name in (
            "schema_version",
            "contract_id",
            "contract_version",
            "ontology_hash",
            "fact_contract_version",
            "ruleset_id",
            "ruleset_version",
            "rules_file",
        ):
            _nonblank(document[name], name)
        if document["schema_version"] != "1":
            raise LogicError(
                f"Unsupported logic contract schema_version '{document['schema_version']}'"
            )
        if document["fact_contract_version"] != FACT_CONTRACT_VERSION:
            raise LogicError(
                "Unsupported logic fact_contract_version "
                f"'{document['fact_contract_version']}'"
            )
        try:
            require_digest(document["ontology_hash"], "logic contract ontology_hash")
        except LedgerError as error:
            raise LogicError(str(error)) from error
        rule_ids = document["rule_ids"]
        if not isinstance(rule_ids, list) or not rule_ids:
            raise LogicError("logic contract rule_ids must be a nonempty list")
        if any(not isinstance(rule_id, str) or not rule_id.strip() for rule_id in rule_ids):
            raise LogicError("logic contract rule_ids must be nonblank strings")
        if len(rule_ids) != len(set(rule_ids)):
            raise LogicError("logic contract rule_ids must be unique")
        timeout_seconds = document["timeout_seconds"]
        if (
            not isinstance(timeout_seconds, int)
            or isinstance(timeout_seconds, bool)
            or timeout_seconds <= 0
        ):
            raise LogicError("logic contract timeout_seconds must be a positive integer")

        rules_path = source_path.parent / document["rules_file"]
        try:
            rules_bytes = rules_path.read_bytes()
            rules_source = rules_bytes.decode("utf-8")
        except (OSError, UnicodeError) as error:
            raise LogicError(f"Cannot load rules file '{rules_path}': {error}") from error
        if not rules_source.strip():
            raise LogicError("rules file must not be empty")
        ruleset_hash = "sha256:" + hashlib.sha256(rules_bytes).hexdigest()
        canonical_rule_ids = tuple(sorted(rule_ids))
        contract = cls(
            schema_version=document["schema_version"],
            contract_id=document["contract_id"],
            contract_version=document["contract_version"],
            ontology_hash=document["ontology_hash"],
            fact_contract_version=document["fact_contract_version"],
            ruleset_id=document["ruleset_id"],
            ruleset_version=document["ruleset_version"],
            rules_path=rules_path.resolve(),
            rules_source=rules_source,
            rule_ids=canonical_rule_ids,
            timeout_seconds=timeout_seconds,
            ruleset_hash=ruleset_hash,
            contract_hash=logic_contract_digest(
                schema_version=document["schema_version"],
                contract_id=document["contract_id"],
                contract_version=document["contract_version"],
                ontology_hash=document["ontology_hash"],
                fact_contract_version=document["fact_contract_version"],
                ruleset_id=document["ruleset_id"],
                ruleset_version=document["ruleset_version"],
                rule_ids=canonical_rule_ids,
                timeout_seconds=timeout_seconds,
                ruleset_hash=ruleset_hash,
            ),
        )
        contract.validate_integrity()
        return contract


@dataclass(frozen=True)
class CompiledFacts:
    ontology_hash: str
    state_digests: tuple[str, ...]
    record_ids: tuple[str, ...]
    facts: tuple[str, ...]
    facts_hash: str


class GraphFactCompiler:
    """Compile any Malleus graph into a fixed typed Prolog fact vocabulary."""

    contract_version = FACT_CONTRACT_VERSION

    def compile(self, *graphs: KnowledgeGraph) -> CompiledFacts:
        if not graphs:
            raise LogicError("At least one KnowledgeGraph is required")
        if any(not isinstance(graph, KnowledgeGraph) for graph in graphs):
            raise TypeError("All compiler inputs must be KnowledgeGraph values")
        ontology_hashes = {f"sha256:{graph.registry.content_hash()}" for graph in graphs}
        if len(ontology_hashes) != 1:
            raise LogicError("Cannot compile graphs with different ontologies")
        ontology_hash = next(iter(ontology_hashes))
        registry = graphs[0].registry

        facts = {_fact("m_ontology_hash", ontology_hash)}
        type_names = registry.type_names()
        mixin_names = tuple(
            name for name in type_names if registry.get_type(name).is_mixin
        )
        for type_name in type_names:
            facts.add(_fact("m_type", type_name))
            if registry.get_type(type_name).is_mixin:
                facts.add(_fact("m_mixin", type_name))
            if not registry.get_type(type_name).is_mixin:
                for mixin_name in mixin_names:
                    if registry.has_mixin(type_name, mixin_name):
                        facts.add(_fact("m_has_mixin", type_name, mixin_name))
            for ancestor in type_names:
                if ancestor != type_name and registry.is_subtype_of(type_name, ancestor):
                    facts.add(_fact("m_subtype", type_name, ancestor))

        snapshots = tuple(graph.snapshot() for graph in graphs)
        records: dict[str, tuple[str, dict[str, Any]]] = {}
        for snapshot in snapshots:
            for node in snapshot["nodes"]:
                self._add_record(records, node["id"], "node", node)
            for relation in snapshot["relations"]:
                self._add_record(records, relation["key"], "relation", relation)

        for record_id, (kind, record) in sorted(records.items()):
            if kind == "node":
                node_kind = (
                    "signal" if record.get("is_signal") else
                    "event" if record.get("is_event") else
                    "entity"
                )
                facts.add(_fact("m_record", record_id, record["type"], node_kind))
                properties = {
                    key: value
                    for key, value in record.items()
                    if key not in {"id", "type", "is_signal", "is_event"}
                }
            else:
                facts.add(_fact("m_record", record_id, record["type"], "relation"))
                facts.add(_fact(
                    "m_relation",
                    record_id,
                    record["type"],
                    record["source_id"],
                    record["target_id"],
                ))
                properties = {
                    key: value
                    for key, value in record.items()
                    if key not in {"key", "type", "source_id", "target_id"}
                }
            facts.update(_property_facts(record_id, properties))

        ordered = tuple(sorted(facts))
        return CompiledFacts(
            ontology_hash=ontology_hash,
            state_digests=tuple(content_digest(snapshot) for snapshot in snapshots),
            record_ids=tuple(sorted(records)),
            facts=ordered,
            facts_hash=content_digest(list(ordered)),
        )

    @staticmethod
    def _add_record(
        records: dict[str, tuple[str, dict[str, Any]]],
        record_id: str,
        kind: str,
        record: dict[str, Any],
    ) -> None:
        if record_id in records:
            raise LogicError(f"Duplicate graph record '{record_id}' across compiler inputs")
        records[record_id] = (kind, record)


@dataclass(frozen=True, order=True)
class Violation:
    rule_id: str
    violation_code: str
    witness_record_ids: tuple[str, ...]


@dataclass(frozen=True)
class LogicCheckResult:
    candidate_digest: str
    base_state_digest: str
    candidate_state_digest: str
    context_state_digests: tuple[str, ...]
    ontology_hash: str
    fact_contract_version: str
    contract_id: str
    contract_version: str
    contract_hash: str
    ruleset_id: str
    ruleset_version: str
    ruleset_hash: str
    engine_name: str
    engine_version: str
    timeout_seconds: int
    facts_hash: str
    fact_count: int
    translated_record_ids: tuple[str, ...]
    checked_rule_ids: tuple[str, ...]
    violations: tuple[Violation, ...]

    @property
    def valid(self) -> bool:
        return not self.violations

    @property
    def outcome(self) -> str:
        return "SATISFIED" if self.valid else "VIOLATED"

    @property
    def violated_rule_ids(self) -> tuple[str, ...]:
        return tuple(sorted({violation.rule_id for violation in self.violations}))

    def to_protocol_records(
        self,
        *,
        check_id: str,
        event_id: str,
        generated_at: str,
        actor_id: str,
        role: str,
        proposal_id: str,
        proposal_content_hash: str,
        base_acceptance_head: str,
        monitor_id: str,
        monitor_version: str,
        monitor_hash: str,
        logic_contract_record_hash: str,
        ruleset_record_hash: str,
        source_record_ids: tuple[str, ...] = (),
    ) -> tuple[dict[str, Any], tuple[dict[str, Any], ...]]:
        _nonblank(check_id, "check_id")
        check_sources = tuple(sorted({
            *source_record_ids,
            proposal_id,
            monitor_id,
            self.contract_id,
            self.ruleset_id,
        }))
        witnesses = []
        for index, violation in enumerate(self.violations, start=1):
            witness_id = f"{check_id}:witness:{index}"
            witness = with_content_hash(
                "ViolationWitness",
                {
                    "id": witness_id,
                    "generation_event_id": event_id,
                    "generated_at": generated_at,
                    "responsible_actor_id": actor_id,
                    "responsible_role": role,
                    "source_record_ids": [check_id],
                    "logic_check_id": check_id,
                    "rule_id": violation.rule_id,
                    "violation_code": violation.violation_code,
                    "witness_record_ids": list(violation.witness_record_ids),
                    "witness_binding_hash": content_digest({
                        "rule_id": violation.rule_id,
                        "violation_code": violation.violation_code,
                        "witness_record_ids": list(violation.witness_record_ids),
                    }),
                },
            )
            witnesses.append(witness)
        check = with_content_hash(
            "LogicCheckRecord",
            {
                "id": check_id,
                "generation_event_id": event_id,
                "generated_at": generated_at,
                "responsible_actor_id": actor_id,
                "responsible_role": role,
                "source_record_ids": list(check_sources),
                "proposal_id": proposal_id,
                "proposal_content_hash": proposal_content_hash,
                "base_acceptance_head": base_acceptance_head,
                "monitor_id": monitor_id,
                "monitor_version": monitor_version,
                "monitor_hash": monitor_hash,
                "candidate_digest": self.candidate_digest,
                "base_state_digest": self.base_state_digest,
                "candidate_state_digest": self.candidate_state_digest,
                "context_state_digests": list(self.context_state_digests),
                "ontology_hash": self.ontology_hash,
                "fact_contract_version": self.fact_contract_version,
                "logic_contract_id": self.contract_id,
                "logic_contract_version": self.contract_version,
                "logic_contract_record_hash": logic_contract_record_hash,
                "logic_contract_artifact_hash": self.contract_hash,
                "ruleset_id": self.ruleset_id,
                "ruleset_version": self.ruleset_version,
                "ruleset_record_hash": ruleset_record_hash,
                "ruleset_artifact_hash": self.ruleset_hash,
                "engine_name": self.engine_name,
                "engine_version": self.engine_version,
                "timeout_seconds": self.timeout_seconds,
                "facts_hash": self.facts_hash,
                "fact_count": self.fact_count,
                "translated_record_ids": list(self.translated_record_ids),
                "checked_rule_ids": list(self.checked_rule_ids),
                "violated_rule_ids": list(self.violated_rule_ids),
                "violation_witness_ids": [witness["id"] for witness in witnesses],
                "check_outcome": self.outcome,
            },
        )
        return check, tuple(witnesses)


def logic_monitor_failure_records(
    *,
    error: LogicError,
    failure_id: str,
    assessment_id: str,
    event_id: str,
    generated_at: str,
    actor_id: str,
    role: str,
    proposal_id: str,
    proposal_content_hash: str,
    base_acceptance_head: str,
    monitor_id: str,
    monitor_version: str,
    monitor_hash: str,
    logic_contract_id: str,
    logic_contract_record_hash: str,
    ruleset_id: str,
    ruleset_record_hash: str,
    failure_category: str,
    error_code: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build the only valid protocol outcome for an incomplete logic check."""
    if not isinstance(error, LogicError):
        raise TypeError("error must be a LogicError")
    for name, value in (
        ("logic_contract_record_hash", logic_contract_record_hash),
        ("ruleset_record_hash", ruleset_record_hash),
    ):
        try:
            require_digest(value, name)
        except LedgerError as digest_error:
            raise LogicError(str(digest_error)) from digest_error
    return build_monitor_failure_records(
        error=error,
        failure_id=failure_id,
        assessment_id=assessment_id,
        event_id=event_id,
        generated_at=generated_at,
        actor_id=actor_id,
        role=role,
        proposal_id=proposal_id,
        proposal_content_hash=proposal_content_hash,
        base_acceptance_head=base_acceptance_head,
        monitor_id=monitor_id,
        monitor_version=monitor_version,
        monitor_hash=monitor_hash,
        assessment_kind="LOGICAL",
        failure_category=failure_category,
        error_code=error_code,
        additional_source_record_ids=(logic_contract_id, ruleset_id),
        failure_fields={
            "logic_contract_id": logic_contract_id,
            "logic_contract_record_hash": logic_contract_record_hash,
            "ruleset_id": ruleset_id,
            "ruleset_hash": ruleset_record_hash,
        },
        assessment_fields={
            "logic_contract_id": logic_contract_id,
            "logic_contract_record_hash": logic_contract_record_hash,
            "ruleset_id": ruleset_id,
            "ruleset_hash": ruleset_record_hash,
        },
    )


def _property_facts(owner_id: str, properties: Mapping[str, Any]) -> set[str]:
    facts = set()
    for key, value in sorted(properties.items()):
        if isinstance(value, list):
            facts.add(_fact("m_list", owner_id, key, len(value)))
            for index, item in enumerate(value):
                kind, encoded = _scalar(item, f"{owner_id}.{key}[{index}]")
                facts.add(_fact("m_list_item", owner_id, key, index, kind, encoded, encoded=True))
        else:
            kind, encoded = _scalar(value, f"{owner_id}.{key}")
            facts.add(_fact("m_property", owner_id, key, kind, encoded, encoded=True))
    return facts


def _scalar(value: Any, context: str) -> tuple[str, str]:
    if value is None:
        return "null", "null"
    if isinstance(value, bool):
        return "boolean", "true" if value else "false"
    if isinstance(value, int):
        return "integer", str(value)
    if isinstance(value, float) and math.isfinite(value):
        return "float", json.dumps(value, allow_nan=False)
    if isinstance(value, str):
        return "string", _atom(value)
    raise LogicError(f"Unsupported property value at {context}: {type(value).__name__}")


def _fact(predicate: str, *values: Any, encoded: bool = False) -> str:
    arguments = []
    for index, value in enumerate(values):
        if encoded and index == len(values) - 1:
            arguments.append(value)
        elif isinstance(value, int) and not isinstance(value, bool):
            arguments.append(str(value))
        else:
            arguments.append(_atom(str(value)))
    return f"{predicate}({', '.join(arguments)})"


def _atom(value: str) -> str:
    safe = frozenset(string.ascii_letters + string.digits + " _-.:/@+")
    encoded = []
    for character in value:
        codepoint = ord(character)
        if character in safe:
            encoded.append(character)
        elif codepoint <= 0xFFFF:
            encoded.append(f"\\u{codepoint:04x}")
        else:
            encoded.append(f"\\U{codepoint:08x}")
    return "'" + "".join(encoded) + "'"


def _exact_fields(value: Any, expected: set[str], context: str) -> None:
    if not isinstance(value, Mapping):
        raise LogicError(f"{context} must be an object")
    if any(not isinstance(key, str) for key in value):
        raise LogicError(f"{context} keys must be strings")
    missing = sorted(expected - set(value))
    unknown = sorted(set(value) - expected)
    if missing:
        raise LogicError(f"{context} missing required fields: {', '.join(missing)}")
    if unknown:
        raise LogicError(f"{context} has unknown fields: {', '.join(unknown)}")


def _nonblank(value: Any, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise LogicError(f"{name} must be a nonblank string")
