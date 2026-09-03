"""Compact evidence projection for the private Small Shop showcase.

This module is research-local. Its JSON shapes are evidence views, not a stable
Malleus API, wire format, ledger, or state authority.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile
from typing import Mapping

from malleus._contract_pipeline.knowledge import (
    KnowledgeChangeSet,
    KnowledgeHistoryReplay,
    KnowledgeRecordHistory,
    KnowledgeValidTime,
)
from research.ontology_driven_kg_realization.experiments.small_shop.showcase.query import (
    QueryError,
    current_supplier_order,
    order_contents,
    payment_settlements,
    query_state_coordinates,
    record_change_provenance,
    state_after_change,
    supplier_order_history,
)
from research.ontology_driven_kg_realization.experiments.small_shop.showcase.run import (
    ShowcaseRefusal,
    array,
    canonical,
    decode,
    integer,
    obj,
    plain,
    retained_context,
    run_showcase,
    text,
    verify_source_mapping_receipts,
)


EXPLANATION_SCHEMA = "malleus.small-shop.showcase-evidence/private-v0"
QUERY_SCHEMA = "malleus.small-shop.showcase-queries/private-v0"
RUN_PROGRAM_ID = "artifact:small-shop-showcase:run-program"
VALIDATED_CONTRACT_ID = "artifact:small-shop-showcase:validated-contract"
E4_CHANGE = "change:SHOP-SUPPLIER-ORDER-CORRECTION:B:e4"

_RDFS_SUBCLASS = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
_ENTITY = "https://malleus.dev/schema/Entity"
_RELATION = "https://malleus.dev/schema/Relation"
_REPRESENTATIVE_CLASSES = (
    (
        "https://malleus.dev/schema/small-shop-fulfilment/SalesOrder",
        _ENTITY,
    ),
    (
        "https://malleus.dev/schema/small-shop-fulfilment-correction/SupplierOrderState",
        _ENTITY,
    ),
    (
        "https://malleus.dev/schema/small-shop-fulfilment-settlement/Invoice",
        _ENTITY,
    ),
    (
        "https://malleus.dev/schema/small-shop-fulfilment-settlement/Payment",
        _ENTITY,
    ),
    (
        "https://malleus.dev/schema/small-shop-fulfilment-settlement/PaymentSettlesInvoiceRelation",
        _RELATION,
    ),
)


class EvidenceError(ValueError):
    """The verified history cannot produce the requested evidence projection."""


def _time(value: KnowledgeValidTime | None) -> dict[str, str] | None:
    if value is None:
        return None
    return {"kind": value.kind, "value": value.value}


def _base_coordinates(change: KnowledgeChangeSet) -> dict[str, object]:
    return {
        "acceptance_head": change.base_acceptance_head,
        "accepted_state_digest": change.base_accepted_state_digest,
        "ledger_event_count": change.base_ledger_event_count,
        "ledger_head": change.base_ledger_head,
        "materialization_head": change.base_materialization_head,
    }


def _operation_summary(raw: object) -> dict[str, object]:
    operation = obj(raw, "knowledge operation")
    required = (
        "depends_on",
        "operation_id",
        "operation_type",
        "ordinal",
        "properties",
        "record_id",
        "record_type",
    )
    for field in required:
        if field not in operation:
            raise EvidenceError(f"knowledge operation lacks {field}")
    optional = {
        field: operation[field]
        for field in ("source_id", "supersedes_record_id", "target_id")
        if field in operation
    }
    return {
        "depends_on": list(array(operation["depends_on"], "operation dependencies")),
        "operation_id": text(operation["operation_id"], "operation ID"),
        "operation_type": text(operation["operation_type"], "operation type"),
        "ordinal": integer(operation["ordinal"], "operation ordinal"),
        "properties": plain(obj(operation["properties"], "operation properties")),
        "record_id": text(operation["record_id"], "record ID"),
        "record_type": text(operation["record_type"], "record type"),
        **optional,
    }


def _change_summary(ordinal: int, change: KnowledgeChangeSet) -> dict[str, object]:
    data = obj(change.data, "knowledge change set")
    if "operations" not in data:
        raise EvidenceError("knowledge change set lacks operations")
    return {
        "base_coordinates": _base_coordinates(change),
        "change_set_id": change.change_set_id,
        "contract_identity": change.contract_identity,
        "evidence_record_ids": [identifier for identifier, _ in change.evidence],
        "identity": change.identity,
        "operations": [
            _operation_summary(item)
            for item in array(data["operations"], "knowledge operations")
        ],
        "ordinal": ordinal,
        "source_record_ids": [identifier for identifier, _ in change.sources],
        "supersedes": list(change.supersedes),
        "valid_time": _time(change.valid_time),
    }


def _record_history(
    record_id: str, history: KnowledgeRecordHistory
) -> dict[str, object]:
    return {
        "change_set_id": history.change_set_id,
        "record_id": record_id,
        "superseded_by": history.superseded_by,
        "supersedes_record_id": history.supersedes_record_id,
        "valid_from": _time(history.valid_from),
        "valid_to": _time(history.valid_to),
    }


def _representative_facts(contract: Mapping[str, object]) -> list[dict[str, object]]:
    if "facts" not in contract:
        raise EvidenceError("validated contract lacks facts")
    facts = []
    for ordinal, raw in enumerate(array(contract["facts"], "validated facts")):
        fact = obj(raw, f"validated fact {ordinal}")
        if set(fact) != {"object", "predicate", "subject"}:
            raise EvidenceError(f"validated fact {ordinal} has the wrong shape")
        text(fact["predicate"], f"validated fact {ordinal} predicate")
        text(fact["subject"], f"validated fact {ordinal} subject")
        facts.append(dict(fact))

    selected = []
    for subject, object_value in _REPRESENTATIVE_CLASSES:
        matches = [
            fact
            for fact in facts
            if fact["subject"] == subject
            and fact["predicate"] == _RDFS_SUBCLASS
            and fact["object"] == object_value
        ]
        if len(matches) != 1:
            raise EvidenceError(f"expected one representative fact for {subject}")
        selected.append(matches[0])
    return selected


def _validated_contract(
    replay: KnowledgeHistoryReplay,
) -> tuple[object, Mapping[str, object]]:
    matches = [
        item
        for item in replay.retained_inputs
        if item.record_id == VALIDATED_CONTRACT_ID and item.role == "VALIDATED_CONTRACT"
    ]
    if len(matches) != 1:
        raise EvidenceError("history lacks one validated-contract artifact")
    artifact = matches[0]
    contract = decode(artifact.content, "validated contract", require_canonical=True)
    required = (
        "fact_count",
        "facts",
        "facts_sha256",
        "validated_fact_set_sha256",
    )
    for field in required:
        if field not in contract:
            raise EvidenceError(f"validated contract lacks {field}")
    if integer(contract["fact_count"], "validated fact count") != len(
        array(contract["facts"], "validated facts")
    ):
        raise EvidenceError("validated contract fact count differs")
    return artifact, contract


def _explanation(replay: KnowledgeHistoryReplay) -> bytes:
    program, _, _ = retained_context(replay)
    retained = {item.record_id: item for item in replay.retained_inputs}
    try:
        run_program = retained[RUN_PROGRAM_ID]
    except KeyError as error:
        raise EvidenceError("history lacks the retained run program") from error
    if run_program.role != "RETAINED_EVIDENCE":
        raise EvidenceError("run program has the wrong retained role")
    artifact, contract = _validated_contract(replay)
    graph = replay.graph.snapshot()
    current_count = len(array(graph["nodes"], "graph nodes")) + len(
        array(graph["relations"], "graph relations")
    )
    receipts = verify_source_mapping_receipts(replay)
    oracle_named_inputs = sorted(
        item.record_id
        for item in replay.retained_inputs
        if "oracle" in item.record_id.lower()
    )
    if oracle_named_inputs:
        raise EvidenceError("history unexpectedly retains an oracle-named input")
    return canonical(
        {
            "accepted_changes": [
                _change_summary(ordinal, change)
                for ordinal, change in enumerate(replay.change_sets)
            ],
            "coordinates": {
                "contract": {
                    "effective_contract_identity": replay.partial_contract.identity,
                    "fact_count": contract["fact_count"],
                    "facts_identity": text(contract["facts_sha256"], "facts identity"),
                    "validated_contract_artifact_id": artifact.record_id,
                    "validated_contract_artifact_identity": artifact.identity,
                    "validated_fact_set_identity": text(
                        contract["validated_fact_set_sha256"],
                        "validated fact-set identity",
                    ),
                },
                "graph": {
                    "current_record_count": current_count,
                    "ontology_identity": text(
                        graph["ontology_hash"], "graph ontology identity"
                    ),
                    "state_digest": replay.graph.state_digest(),
                },
                "history": {
                    "acceptance_head": replay.acceptance_head,
                    "binding_identity": replay.binding.identity,
                    "event_count": replay.ledger_event_count,
                    "ledger_head": replay.ledger_head,
                    "materialization_head": replay.materialization_head,
                    "receipt_identity": replay.receipt.identity,
                },
            },
            "record_history": [
                _record_history(record_id, history)
                for record_id, history in sorted(replay.record_history.items())
            ],
            "representative_contract_facts": _representative_facts(contract),
            "run_program": {
                "decisions": plain(program["decisions"]),
                "identity": run_program.identity,
                "limitations": plain(program["limitations"]),
                "record_id": run_program.record_id,
            },
            "runtime_oracle_named_inputs": oracle_named_inputs,
            "schema": EXPLANATION_SCHEMA,
            "scope": "RESEARCH_LOCAL_NO_STABLE_API_OR_WIRE",
            "source_mapping_receipts": [
                {
                    "change_set_id": item.change_set_id,
                    "receipt_identity": item.receipt_identity,
                }
                for item in receipts
            ],
        }
    )


def _queries(replay: KnowledgeHistoryReplay) -> bytes:
    sources = (
        order_contents(replay, "O1"),
        payment_settlements(replay, "P1"),
        current_supplier_order(replay, "B"),
        supplier_order_history(replay, "B"),
        state_after_change(replay, E4_CHANGE),
        record_change_provenance(replay, "relation:P1:I1"),
        record_change_provenance(replay, "supplier-order-state:B:e4"),
        query_state_coordinates(replay),
    )
    return canonical(
        {
            "answers": [
                decode(source, f"query answer {ordinal}", require_canonical=True)
                for ordinal, source in enumerate(sources)
            ],
            "schema": QUERY_SCHEMA,
            "scope": "READ_ONLY_REPLAY_DERIVED_RESEARCH_EVIDENCE",
        }
    )


def _write(output: Path, values: Mapping[str, bytes]) -> None:
    targets = {name: output / name for name in values}
    for name, target in targets.items():
        if target.is_symlink():
            raise EvidenceError(f"refusing symlink output: {name}")
    for name, source in values.items():
        target = targets[name]
        target.write_bytes(source)


def generate_evidence(output: str | Path) -> dict[str, bytes]:
    """Regenerate four compact files from one ledger-only verified replay."""
    destination = Path(output)
    if destination.is_symlink():
        raise EvidenceError("evidence output must not be a symlink")
    if destination.exists() and not destination.is_dir():
        raise EvidenceError("evidence output must be a directory")
    destination.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=".showcase-run-", dir=destination) as raw:
        run_directory = Path(raw)
        first = run_showcase(run_directory)
        replayed = run_showcase(run_directory)
        if (
            first.receipt_bytes != replayed.receipt_bytes
            or first.graph_bytes != replayed.graph_bytes
            or first.replay.receipt != replayed.replay.receipt
        ):
            raise EvidenceError("ledger-only replay differs from the original run")
        values = {
            "explanation.json": _explanation(replayed.replay),
            "graph.json": replayed.graph_bytes,
            "queries.json": _queries(replayed.replay),
            "receipt.json": replayed.receipt_bytes,
        }
    _write(destination, values)
    return values


def main(argv: tuple[str, ...] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("evidence"),
    )
    arguments = parser.parse_args(argv)
    try:
        values = generate_evidence(arguments.output)
    except (EvidenceError, QueryError, ShowcaseRefusal) as error:
        parser.error(str(error))
    print(
        json.dumps(
            {name: len(source) for name, source in sorted(values.items())},
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
