"""Rehydrate a replay receipt and run the four frozen source-free queries."""

from __future__ import annotations

import argparse
import builtins
from contextlib import ExitStack
from copy import deepcopy
from hashlib import sha256
import importlib
import io
import json
import os
from pathlib import Path
import socket
from typing import Any, Callable, Mapping, Sequence
from unittest.mock import patch

from malleus.kg import KnowledgeGraph
from malleus.ledger import LedgerError, canonical_json, content_digest
from malleus.ontology import OntologyRegistry
from research.ontology_driven_kg_realization.experiments.document_paper.native_query import (
    NativeQueryRefusal,
    load_query_binding,
    run_frozen_queries,
    validate_query_binding_against_ontology,
)


RESULT_SCHEMA = "malleus.paper-v4.query-replay/v1"
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


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


class QueryReplayRefusal(ValueError):
    """The retained inputs or source-free execution boundary are invalid."""

    def __init__(
        self,
        detail: str,
        *,
        attempts: Mapping[str, int] | None = None,
    ) -> None:
        self.attempts = dict(attempts or {})
        super().__init__(detail)


def _refuse(detail: str) -> None:
    raise QueryReplayRefusal(detail)


def _object(value: object, subject: str) -> dict[str, Any]:
    if type(value) is not dict:
        _refuse(f"{subject} must be an object")
    return value


def _array(value: object, subject: str) -> list[Any]:
    if type(value) is not list:
        _refuse(f"{subject} must be an array")
    return value


def _sha256(value: object, subject: str) -> str:
    if (
        type(value) is not str
        or not value.startswith("sha256:")
        or len(value) != 71
        or any(character not in "0123456789abcdef" for character in value[7:])
    ):
        _refuse(f"{subject} must be a lowercase sha256 digest")
    return value


def _canonical_object(source: bytes, subject: str) -> dict[str, Any]:
    if type(source) is not bytes:
        raise TypeError(f"{subject} source must be bytes")
    try:
        value = json.loads(source)
        canonical = canonical_json(value).encode("utf-8")
    except (UnicodeDecodeError, json.JSONDecodeError, LedgerError) as error:
        raise QueryReplayRefusal(f"{subject} must be canonical UTF-8 JSON") from error
    if canonical != source:
        _refuse(f"{subject} bytes are not canonical JSON")
    return _object(value, subject)


def _exact_file(path: Path, source: bytes, subject: str) -> None:
    if not isinstance(path, Path) or type(source) is not bytes:
        raise TypeError(f"{subject} requires one Path and exact bytes")
    try:
        observed = path.read_bytes()
    except OSError as error:
        raise QueryReplayRefusal(f"cannot read {subject} at {path}: {error}") from error
    if observed != source:
        _refuse(f"{subject} path bytes differ from the retained input")


def _snapshot_records(receipt: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    if "graph_state_digest" not in receipt:
        _refuse("receipt.graph_state_digest is required")
    _sha256(receipt["graph_state_digest"], "receipt.graph_state_digest")
    if "validated_fact_set_sha256" not in receipt:
        _refuse("receipt.validated_fact_set_sha256 is required")
    _sha256(
        receipt["validated_fact_set_sha256"],
        "receipt.validated_fact_set_sha256",
    )
    queries = _object(receipt.get("queries"), "receipt.queries")
    if set(queries) != {"entities", "relations"}:
        _refuse("receipt.queries must contain exactly entities and relations")

    entities = []
    for index, value in enumerate(
        _array(queries["entities"], "receipt.queries.entities")
    ):
        record = _object(value, f"receipt.queries.entities[{index}]")
        if "id" not in record or "type" not in record:
            _refuse(f"receipt.queries.entities[{index}] requires id and type")
        entities.append(
            {
                "type": record["type"],
                "id": record["id"],
                "properties": {
                    key: deepcopy(item)
                    for key, item in record.items()
                    if key not in {"id", "type"}
                },
            }
        )

    relations = []
    required = {"key", "type", "source_id", "target_id"}
    for index, value in enumerate(
        _array(queries["relations"], "receipt.queries.relations")
    ):
        record = _object(value, f"receipt.queries.relations[{index}]")
        missing = sorted(required - set(record))
        if missing:
            _refuse(
                f"receipt.queries.relations[{index}] is missing required keys: {missing}"
            )
        relations.append(
            {
                "type": record["type"],
                "id": record["key"],
                "source_id": record["source_id"],
                "target_id": record["target_id"],
                "properties": {
                    key: deepcopy(item)
                    for key, item in record.items()
                    if key not in required
                },
            }
        )
    return {"entities": entities, "relations": relations}


class _SourceFreeGuard:
    def __init__(self) -> None:
        self.attempts = {name: 0 for name in FORBIDDEN_ATTEMPTS}
        self._stack = ExitStack()
        self._import: Callable[..., Any] = builtins.__import__
        self._import_module = importlib.import_module

    def _block(self, category: str, detail: str) -> None:
        self.attempts[category] += 1
        raise QueryReplayRefusal(
            f"forbidden {category} during query execution: {detail}",
            attempts=self.attempts,
        )

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
        replacements = (
            (builtins, "open", self._file),
            (io, "open", self._file),
            (os, "open", self._file),
            (socket, "socket", self._network),
            (socket, "create_connection", self._network),
            (socket, "getaddrinfo", self._network),
            (builtins, "__import__", self._guarded_import),
            (importlib, "import_module", self._guarded_import_module),
        )
        for owner, name, replacement in replacements:
            self._stack.enter_context(patch.object(owner, name, replacement))
        return self

    def __exit__(self, *error: object) -> None:
        self._stack.close()


def run_query_replay(
    receipt_source: bytes,
    binding_source: bytes,
    *,
    ontology_path: Path,
    ontology_source: bytes,
    malleus_path: Path,
    malleus_source: bytes,
) -> bytes:
    """Validate declared inputs, reconstruct graph state, and query in memory."""

    receipt = _canonical_object(receipt_source, "receipt")
    _exact_file(ontology_path, ontology_source, "selected ontology")
    _exact_file(malleus_path, malleus_source, "retained Malleus import")
    try:
        registry = OntologyRegistry(
            ontology_path,
            import_map={"malleus": malleus_path},
        )
        graph = KnowledgeGraph.from_records(registry, _snapshot_records(receipt))
    except (OSError, ValueError) as error:
        raise QueryReplayRefusal(f"cannot rehydrate receipt graph: {error}") from error
    snapshot = graph.snapshot()
    snapshot["ontology_hash"] = receipt["validated_fact_set_sha256"]
    observed_digest = content_digest(snapshot)
    if observed_digest != receipt["graph_state_digest"]:
        _refuse(
            "receipt graph state digest differs after typed rehydration: "
            f"expected {receipt['graph_state_digest']}, observed {observed_digest}"
        )

    try:
        binding = load_query_binding(binding_source)
        validate_query_binding_against_ontology(binding, registry)
    except NativeQueryRefusal as error:
        raise QueryReplayRefusal(f"query binding refused: {error}") from error

    guard = _SourceFreeGuard()
    with guard:
        results = run_frozen_queries(graph, binding)
    if len(results) != 4:
        _refuse("frozen query runner did not return exactly four results")
    return canonical_json(
        {
            "schema": RESULT_SCHEMA,
            "inputs": {
                "ontology_sha256": _digest(ontology_source),
                "query_binding_sha256": _digest(binding_source),
                "replay_receipt_sha256": _digest(receipt_source),
            },
            "graph_state_digest": observed_digest,
            "queries": list(results),
            "forbidden_attempts": guard.attempts,
        }
    ).encode("utf-8")


def write_query_result(path: Path, source: bytes) -> None:
    """Write one result without creating or replacing any existing path."""

    if not isinstance(path, Path) or type(source) is not bytes:
        raise TypeError("query result requires one Path and exact bytes")
    try:
        with path.open("xb") as stream:
            stream.write(source)
    except FileExistsError as error:
        raise QueryReplayRefusal(f"query result already exists at {path}") from error
    except OSError as error:
        raise QueryReplayRefusal(
            f"cannot write query result {path}: {error}"
        ) from error


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--binding", required=True, type=Path)
    parser.add_argument("--ontology", required=True, type=Path)
    parser.add_argument("--malleus", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    result = run_query_replay(
        args.receipt.read_bytes(),
        args.binding.read_bytes(),
        ontology_path=args.ontology,
        ontology_source=args.ontology.read_bytes(),
        malleus_path=args.malleus,
        malleus_source=args.malleus.read_bytes(),
    )
    write_query_result(args.output, result)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
