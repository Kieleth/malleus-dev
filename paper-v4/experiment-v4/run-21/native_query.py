"""Execute a type-only query binding against the replayed graph and nothing else.

The binding names record types and projected field names. It never names a record
identifier, a graph size, a locator or an answer value, and it is written at
ontology acceptance, before population, admission, disposal, reopen and replay
exist.

Three case kinds execute here, all type-only. A RELATION case names a source
type, a relation type and a target type and returns one row per relation whose
endpoints are of those types. An ENTITY case names one record type and returns
every admitted record of it, each row witnessed by itself. A SUBJECT case names
a source-asserted record type and a subject entity type and returns every record
of the first whose ``subject`` reference resolves to a record of the second,
projecting both. Run-08 could execute the first kind only, so an observation or
a claim that carried no relation was unreachable however well it was derived
(E-0138, and the v4.2 RCA sections 2 and 4).

Query execution runs inside a guard that counts and refuses file reads, socket
use and embedding-library imports, so the reported source-free observation is
mechanical rather than asserted. Provenance for every witness comes from
``trace_population_record``. Retained evidence is indexed by ``record_id`` and the
plan's own declared evidence set is resolved by id: list position is not a
capture contract (E-0119).

A witness is a row's kind and its record ids, and inside one question it is
one row. Run-13's 515 rows carried 152 repeats of a witness within a
question, 93 of them identical and 59 the same record projected under an
ancestor's case with fewer fields, which hid three records' digests from the
reviewers; run-14's 919 carried 44. v4.9's only harness delta is the removal:
rows with one witness are one row, projecting the fields of the witness
record's own type as the surface declares them and never the case's, and
recording every case ordinal that produced it in ``case_ordinals``. The
projections are read back out of the binding, where the binder wrote one per
record type off the accepted surface, so the binder does not move. Rows keep
the order of the first case that produced them. A witness returned by more
than one question is untouched: that is the evaluator's type-set judgement at
acceptance and not the executor's.
"""

from __future__ import annotations

import argparse
import builtins
from contextlib import ExitStack
from hashlib import sha256
import importlib
import io
import json
import os
from pathlib import Path
import socket
import sys
from typing import Any, Callable
from unittest.mock import patch

import malleus.compiler as api


RESULT_SCHEMA = "malleus.paper-v4.query-result/v3"
TRACE_SCHEMA = "malleus.paper-v4.query-trace-summary/v1"
BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v4"
FORBIDDEN_ATTEMPTS = ("embedding_import", "file_read", "network")
_EMBEDDING_PACKAGES = frozenset(
    {
        "annoy",
        "chromadb",
        "faiss",
        "hnswlib",
        "langchain",
        "llama_index",
        "milvus",
        "openai",
        "pinecone",
        "pymilvus",
        "qdrant_client",
        "sentence_transformers",
        "transformers",
        "weaviate",
    }
)
SUBJECT_SLOT = "subject"
# Projected on a SUBJECT row beside the fields the subject record's own
# type declares, wherever the subject record carries it. v4.7's only
# harness delta.
SUBJECT_TAGS_SLOT = "tags"
CASE_KINDS = ("ENTITY", "RELATION", "SUBJECT")
# The closed field set of a case and the closed output-field set that goes with
# it, per kind. Every kind names record types and projected field names only.
_CASE_FIELDS = {
    "ENTITY": {"kind", "ordinal", "output_fields", "record_type"},
    "RELATION": {
        "kind",
        "ordinal",
        "output_fields",
        "relation_record_type",
        "source_record_type",
        "target_record_type",
    },
    "SUBJECT": {
        "kind",
        "ordinal",
        "output_fields",
        "record_type",
        "subject_record_type",
    },
}
_OUTPUT_FIELDS = {
    "ENTITY": {"record"},
    "RELATION": {"relation", "source", "target"},
    "SUBJECT": {"record", "subject"},
}
_TYPE_FIELDS = {
    "ENTITY": ("record_type",),
    "RELATION": (
        "source_record_type",
        "relation_record_type",
        "target_record_type",
    ),
    "SUBJECT": ("record_type", "subject_record_type"),
}
# Which declared type each projected field of a case belongs to. The binder
# writes one projection per record type, that type's non-housekeeping slots
# off the accepted surface, and repeats it in every case that names the type.
# This is how the executor reads that map back without reading the surface.
_PROJECTED_TYPES = {
    "ENTITY": (("record_type", "record"),),
    "RELATION": (
        ("source_record_type", "source"),
        ("relation_record_type", "relation"),
        ("target_record_type", "target"),
    ),
    "SUBJECT": (("record_type", "record"), ("subject_record_type", "subject")),
}
# The key the graph carries a record's own type under, on a node and on a
# relation alike. A row projects through this and never through its case.
RECORD_TYPE_SLOT = "type"


class NativeQueryRefusal(ValueError):
    """The binding, the graph or the source-free boundary refused."""


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


class _SourceFreeGuard:
    """Count and refuse every file, socket and embedding reach inside the region."""

    def __init__(self) -> None:
        self.attempts = {name: 0 for name in FORBIDDEN_ATTEMPTS}
        self._stack = ExitStack()
        self._import: Callable[..., Any] = builtins.__import__
        self._import_module = importlib.import_module

    def _block(self, category: str, detail: str) -> None:
        self.attempts[category] += 1
        raise NativeQueryRefusal(f"forbidden {category} during query: {detail}")

    def _file(self, *args: Any, **kwargs: Any) -> None:
        self._block("file_read", str(args[0]) if args else "unspecified path")

    def _network(self, *args: Any, **kwargs: Any) -> None:
        self._block("network", "socket access")

    def _guarded_import(self, name: str, *args: Any, **kwargs: Any) -> Any:
        if name.split(".", 1)[0] in _EMBEDDING_PACKAGES:
            self._block("embedding_import", name)
        return self._import(name, *args, **kwargs)

    def _guarded_import_module(self, name: str, package: str | None = None) -> Any:
        if name.lstrip(".").split(".", 1)[0] in _EMBEDDING_PACKAGES:
            self._block("embedding_import", name)
        return self._import_module(name, package)

    def __enter__(self) -> "_SourceFreeGuard":
        for owner, name, replacement in (
            (builtins, "open", self._file),
            (io, "open", self._file),
            (os, "open", self._file),
            (socket, "socket", self._network),
            (socket, "create_connection", self._network),
            (socket, "getaddrinfo", self._network),
            (builtins, "__import__", self._guarded_import),
            (importlib, "import_module", self._guarded_import_module),
        ):
            self._stack.enter_context(patch.object(owner, name, replacement))
        return self

    def __exit__(self, *error: object) -> None:
        self._stack.close()


def load_binding(source: bytes) -> dict[str, object]:
    binding = json.loads(source)
    if not isinstance(binding, dict) or binding.get("schema") != BINDING_SCHEMA:
        raise NativeQueryRefusal(f"query binding must declare {BINDING_SCHEMA}")
    queries = binding.get("queries")
    if not isinstance(queries, list) or not queries:
        raise NativeQueryRefusal("query binding must carry at least one query")
    for query in queries:
        cases = query.get("cases")
        if not isinstance(cases, list) or not cases:
            raise NativeQueryRefusal(f"query {query.get('id')} carries no case")
        for case in cases:
            kind = case.get("kind")
            if kind not in _CASE_FIELDS:
                raise NativeQueryRefusal(f"query case kind is unknown: {kind}")
            if set(case) != _CASE_FIELDS[kind]:
                raise NativeQueryRefusal(
                    f"query case fields are not closed: {sorted(case)}"
                )
            if set(case["output_fields"]) != _OUTPUT_FIELDS[kind]:
                raise NativeQueryRefusal(
                    "output_fields must name"
                    f" {', '.join(sorted(_OUTPUT_FIELDS[kind]))} for a {kind} case"
                )
    return binding


def validate_binding_against_contract(binding: dict[str, object], view) -> None:
    """Refuse a binding naming a type the accepted contract does not define."""

    known = {name.rsplit("/", 1)[-1] for name in view.type_names()}
    for query in binding["queries"]:
        for case in query["cases"]:
            for key in _TYPE_FIELDS[case["kind"]]:
                if case[key] not in known:
                    raise NativeQueryRefusal(
                        f"query binding names an absent record type: {case[key]}"
                    )


def _project(record: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    return {name: record[name] for name in fields if name in record}


def surface_projections(binding: dict[str, object]) -> dict[str, list[str]]:
    """Each record type's projected fields, as the binder read them off the surface.

    A case names record types and the fields projected for each of them, and
    the binder writes the same list wherever a type is named, because a
    projection is a property of the surface and not of the question. The
    executor reads that map back out of the binding and projects a row by the
    witness record's own type, so a record returned under an ancestor's case
    shows what its own type declares rather than the ancestor's fewer fields.
    A type projected two ways is a binding this refuses rather than choose
    between.
    """

    projections: dict[str, list[str]] = {}
    for query in binding["queries"]:
        for case in query["cases"]:
            for type_key, field_key in _PROJECTED_TYPES[case["kind"]]:
                declared = list(case["output_fields"][field_key])
                name = str(case[type_key])
                if projections.setdefault(name, declared) != declared:
                    raise NativeQueryRefusal(
                        f"the binding projects {name} two ways:"
                        f" {projections[name]} and {declared}"
                    )
    return projections


def _own_fields(
    record: dict[str, Any], projections: dict[str, list[str]]
) -> list[str]:
    """The fields the surface declares for this record's own type.

    The executor refuses rather than falling back to the case's type. A row
    projected through an ancestor is the defect this cell removes, and a type
    the binding never names is one no question's type set reaches, which is
    the evaluator's judgement to correct and not something to guess past here.
    """

    name = record.get(RECORD_TYPE_SLOT)
    if name not in projections:
        raise NativeQueryRefusal(
            f"the binding declares no projection for the record's own type:"
            f" {name}"
        )
    return projections[str(name)]


def _without_ordinals(row: dict[str, Any]) -> dict[str, Any]:
    """A row without the ordinals that produced it, which is the row itself."""

    return {
        name: value for name, value in row.items() if name != "case_ordinals"
    }


def _entity_rows(
    graph,
    case: dict[str, Any],
    witnesses: list[str],
    projections: dict[str, list[str]],
) -> list[dict]:
    """Every admitted record of one type, each row witnessed by itself."""

    rows: list[dict[str, Any]] = []
    for item in graph.query(case["record_type"]):
        rows.append(
            {
                "case_ordinals": [case["ordinal"]],
                "kind": "ENTITY",
                "record": _project(item, _own_fields(item, projections)),
                "witness": {"record_id": item["id"]},
            }
        )
        witnesses.append(item["id"])
    return rows


def _relation_rows(
    graph,
    case: dict[str, Any],
    witnesses: list[str],
    projections: dict[str, list[str]],
) -> list[dict]:
    """Run-08's kind: one row per relation with typed endpoints.

    The case still selects by the three types it names. What it no longer
    decides is the projection, which each of the three records takes from its
    own type.
    """

    sources = {item["id"]: item for item in graph.query(case["source_record_type"])}
    targets = {item["id"]: item for item in graph.query(case["target_record_type"])}
    rows: list[dict[str, Any]] = []
    for relation in graph.query_relations(
        relation_type=case["relation_record_type"]
    ):
        source = sources.get(relation["source_id"])
        target = targets.get(relation["target_id"])
        if source is None or target is None:
            continue
        rows.append(
            {
                "case_ordinals": [case["ordinal"]],
                "kind": "RELATION",
                "source": _project(source, _own_fields(source, projections)),
                "relation": _project(
                    relation, _own_fields(relation, projections)
                ),
                "target": _project(target, _own_fields(target, projections)),
                "witness": {
                    "relation_id": relation["key"],
                    "source_id": relation["source_id"],
                    "target_id": relation["target_id"],
                },
            }
        )
        witnesses.extend(
            (relation["key"], relation["source_id"], relation["target_id"])
        )
    return rows


def _subject_rows(
    graph,
    case: dict[str, Any],
    witnesses: list[str],
    projections: dict[str, list[str]],
) -> list[dict]:
    """Records whose ``subject`` resolves to a record of the subject type.

    The reference is followed by identifier and nothing else. A record whose
    subject is absent, is not a string, or names a record of another type is not
    a row: the case is type-only and resolution is the whole test.

    The subject side projects ``tags`` beside the fields its own record
    type declares, wherever the subject record carries them. The binder drops
    ``tags`` as housekeeping, so a row showed the entity's ``name`` where
    the block wrote the abbreviation the entity's tag carries, and
    run-11's review tokened nine SUBJECT rows SUBJECT_NOT_IN_BLOCK for
    that reason alone. Nothing else moves: the reference is still
    followed by identifier, no case field changes, and a subject that
    carries no ``tags`` projects exactly what it projected before.
    """

    subjects = {item["id"]: item for item in graph.query(case["subject_record_type"])}
    rows: list[dict[str, Any]] = []
    for item in graph.query(case["record_type"]):
        reference = item.get(SUBJECT_SLOT)
        subject = subjects.get(reference) if isinstance(reference, str) else None
        if subject is None:
            continue
        rows.append(
            {
                "case_ordinals": [case["ordinal"]],
                "kind": "SUBJECT",
                "record": _project(item, _own_fields(item, projections)),
                "subject": _project(
                    subject,
                    [*_own_fields(subject, projections), SUBJECT_TAGS_SLOT],
                ),
                "witness": {"record_id": item["id"], "subject_id": subject["id"]},
            }
        )
        witnesses.extend((item["id"], subject["id"]))
    return rows


_ROWS_BY_KIND = {
    "ENTITY": _entity_rows,
    "RELATION": _relation_rows,
    "SUBJECT": _subject_rows,
}


def run_queries(replay, binding: dict[str, object]) -> tuple[list[dict], list[str]]:
    """One row per distinct witness per question, in first-producing-case order.

    A witness is the row's kind and its record ids. Two cases that reach it
    build the same row, now that the projection comes from the record's own
    type, so the second is not a second row: it adds its ordinal to
    ``case_ordinals`` and nothing else. If it is not the same row, something
    other than the surface decided a projection and the executor refuses.
    """

    graph = replay.graph
    projections = surface_projections(binding)
    results: list[dict[str, Any]] = []
    witnesses: list[str] = []
    for query in binding["queries"]:
        rows: dict[tuple[str, bytes], dict[str, Any]] = {}
        for case in query["cases"]:
            for row in _ROWS_BY_KIND[case["kind"]](
                graph, case, witnesses, projections
            ):
                key = (row["kind"], _canonical(row["witness"]))
                seen = rows.get(key)
                if seen is None:
                    rows[key] = row
                    continue
                if _without_ordinals(seen) != _without_ordinals(row):
                    raise NativeQueryRefusal(
                        "one witness projects two ways in"
                        f" {query['question_id']}: {row['witness']}"
                    )
                seen["case_ordinals"] = sorted(
                    {*seen["case_ordinals"], *row["case_ordinals"]}
                )
        results.append(
            {
                "query_id": query["id"],
                "question_id": query["question_id"],
                "rows": sorted(
                    rows.values(),
                    key=lambda row: (
                        row["case_ordinals"][0],
                        _canonical(row["witness"]),
                    ),
                ),
            }
        )
    return results, witnesses


def trace_witnesses(replay, witnesses: list[str]) -> list[dict[str, Any]]:
    """Resolve every witness to retained inputs, selecting evidence by record id."""

    traced: dict[str, dict[str, Any]] = {}
    for record_id in witnesses:
        if record_id in traced:
            continue
        trace = api.trace_population_record(replay, record_id)
        evidence = {item.record_id: item.identity for item in trace.evidence}
        sources = {item.record_id: item.identity for item in trace.sources}
        declared_evidence = {
            str(item["evidence_id"]): str(item["sha256"])
            for item in trace.population_plan["evidence"]
        }
        declared_sources = {
            str(item["source_id"]): str(item["sha256"])
            for item in trace.population_plan["sources"]
        }
        for declared, resolved, subject in (
            (declared_evidence, evidence, "evidence"),
            (declared_sources, sources, "source"),
        ):
            for declared_id, declared_digest in declared.items():
                if resolved.get(declared_id) != declared_digest:
                    raise NativeQueryRefusal(
                        f"declared {subject} is not retained at its id: {declared_id}"
                    )
        traced[record_id] = {
            "record_id": record_id,
            "record_type": trace.record_history.operation.record_type,
            "plan_id": str(trace.population_plan["plan_id"]),
            "plan_sha256": trace.population_plan_identity,
            "history_profile": {
                "profile_id": trace.history_profile.profile_id,
                "sha256": trace.history_profile.identity,
            },
            "evidence": evidence,
            "sources": sources,
            "declared_evidence_ids": sorted(declared_evidence),
            "declared_evidence_resolved": True,
            "derivations": [
                {
                    "path": list(item["path"]),
                    "locator": item["locator"],
                    "source_id": item["source_id"],
                }
                for item in trace.derivations
            ],
        }
    return [traced[record_id] for record_id in sorted(traced)]


def execute(arguments: argparse.Namespace) -> dict[str, object]:
    results = Path(arguments.results)
    if results.exists():
        raise NativeQueryRefusal(f"results directory already exists: {results}")
    binding_source = Path(arguments.binding).read_bytes()
    binding = load_binding(binding_source)

    replay = api.KnowledgeChangeHistory.reopen(arguments.ledger).replay()
    validate_binding_against_contract(binding, replay.contract_view)

    guard = _SourceFreeGuard()
    with guard:
        rows, witnesses = run_queries(replay, binding)
        traces = trace_witnesses(replay, witnesses)

    result = {
        "schema": RESULT_SCHEMA,
        "inputs": {
            "query_binding_sha256": _digest(binding_source),
            "replay_receipt_sha256": _digest(replay.receipt.canonical_bytes),
            "ledger_head": replay.ledger_head,
        },
        "graph_state_digest": replay.graph.state_digest(),
        "queries": rows,
        "forbidden_attempts": guard.attempts,
    }
    summary = {
        "schema": TRACE_SCHEMA,
        "evidence_selection": "BY_RECORD_ID_NEVER_BY_POSITION",
        "witnesses_traced": len(traces),
        "records": traces,
    }
    results.mkdir(parents=True)
    (results / "query-result.json").write_bytes(_canonical(result))
    (results / "trace-summary.json").write_bytes(_canonical(summary))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", required=True, help="structural history path")
    parser.add_argument("--binding", required=True, help="type-only query binding")
    parser.add_argument("--results", required=True, help="new results directory")
    arguments = parser.parse_args(argv)
    try:
        execute(arguments)
    except (OSError, TypeError, ValueError) as error:
        print(f"native-query: {type(error).__name__}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
