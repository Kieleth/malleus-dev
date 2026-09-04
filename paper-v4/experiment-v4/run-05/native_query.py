"""Execute a type-only query binding against the replayed graph and nothing else.

The binding names record types and projected field names. It never names a record
identifier, a graph size, a locator or an answer value, and it is written after
population, admission, disposal, reopen and replay are frozen.

Query execution runs inside a guard that counts and refuses file reads, socket
use and embedding-library imports, so the reported source-free observation is
mechanical rather than asserted. Provenance for every witness comes from
``trace_population_record``. Retained evidence is indexed by ``record_id`` and the
plan's own declared evidence set is resolved by id: list position is not a
capture contract (E-0119).
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


RESULT_SCHEMA = "malleus.paper-v4.query-result/v2"
TRACE_SCHEMA = "malleus.paper-v4.query-trace-summary/v1"
BINDING_SCHEMA = "malleus.paper-v4.native-query-binding/v2"
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
_CASE_FIELDS = {
    "ordinal",
    "source_record_type",
    "relation_record_type",
    "target_record_type",
    "output_fields",
}


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
            if set(case) != _CASE_FIELDS:
                raise NativeQueryRefusal(
                    f"query case fields are not closed: {sorted(case)}"
                )
            if set(case["output_fields"]) != {"source", "relation", "target"}:
                raise NativeQueryRefusal(
                    "output_fields must name source, relation, target"
                )
    return binding


def validate_binding_against_contract(binding: dict[str, object], view) -> None:
    """Refuse a binding naming a type the accepted contract does not define."""

    known = {name.rsplit("/", 1)[-1] for name in view.type_names()}
    for query in binding["queries"]:
        for case in query["cases"]:
            for key in (
                "source_record_type",
                "relation_record_type",
                "target_record_type",
            ):
                if case[key] not in known:
                    raise NativeQueryRefusal(
                        f"query binding names an absent record type: {case[key]}"
                    )


def _project(record: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    return {name: record[name] for name in fields if name in record}


def run_queries(replay, binding: dict[str, object]) -> tuple[list[dict], list[str]]:
    graph = replay.graph
    results: list[dict[str, Any]] = []
    witnesses: list[str] = []
    for query in binding["queries"]:
        rows: list[dict[str, Any]] = []
        for case in query["cases"]:
            fields = case["output_fields"]
            sources = {
                item["id"]: item for item in graph.query(case["source_record_type"])
            }
            targets = {
                item["id"]: item for item in graph.query(case["target_record_type"])
            }
            for relation in graph.query_relations(
                relation_type=case["relation_record_type"]
            ):
                source = sources.get(relation["source_id"])
                target = targets.get(relation["target_id"])
                if source is None or target is None:
                    continue
                rows.append(
                    {
                        "case_ordinal": case["ordinal"],
                        "source": _project(source, fields["source"]),
                        "relation": _project(relation, fields["relation"]),
                        "target": _project(target, fields["target"]),
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
        rows.sort(key=lambda row: (row["case_ordinal"], row["witness"]["relation_id"]))
        results.append(
            {
                "query_id": query["id"],
                "question_id": query["question_id"],
                "rows": rows,
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
