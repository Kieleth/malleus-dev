#!/usr/bin/env python3
"""Record current-reader outcomes for the frozen CC-X04 wire corpus."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any, Mapping

from malleus.accepted import (
    candidate_artifact_digest,
    graph_base_artifact_digest,
    parse_candidate_manifest,
    parse_graph_base_metadata,
)
from malleus.assent import ProtocolLedger
from malleus.kg import KnowledgeGraph
from malleus.ledger import JsonlLedger, LedgerError, content_digest, record_hash
from malleus.ontology import OntologyRegistry
from malleus.recon import ReconProject


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "conformance" / "contract_compiler" / "v0" / "historic_wire"
MANIFEST_PATH = CORPUS / "corpus.json"
OBSERVATIONS_PATH = CORPUS / "observations.json"
ASSENT_SCHEMA = ROOT / "ontology" / "assent.yaml"

RELEASES = [
    {
        "release": "v0.11.0",
        "tag_object": "8ed921e4454f9898a0de2239c4de512d797b25fc",
        "commit": "58741cc7285f9c2c3023d49b8ae3036699449d44",
    },
    {
        "release": "v0.13.3",
        "tag_object": "91633c0e37762f3325daef6e99ba0a9947b82657",
        "commit": "b5a72a6d741c066d1441fbe2d5b5d8319670c05f",
    },
]
INPUTS = [
    {
        "input_id": "recon-project",
        "path": "project.json",
        "byte_length": 282,
        "sha256": "sha256:0808d77254479bfedc7b67790182644db22f71c29b90bd61f0356bb232deeb21",
        "producer_releases": ["v0.11.0", "v0.13.3"],
        "grammar": {
            "format": "JSON",
            "kind": "RECON_PROJECT",
            "schema_version": "1",
        },
    },
    {
        "input_id": "recon-ledger",
        "path": "recon-ledger.jsonl",
        "byte_length": 802,
        "sha256": "sha256:c3720e2031a51d9f27b22ef0cd4b19438858fa062423d97382b66e3e38ab264e",
        "producer_releases": ["v0.11.0", "v0.13.3"],
        "grammar": {
            "event_count": 1,
            "event_type": "RECON_RECORD",
            "format": "HASH_LINKED_JSONL",
            "schema_version": "1",
        },
    },
    {
        "input_id": "graph-snapshot",
        "path": "graph-snapshot.json",
        "byte_length": 118,
        "sha256": "sha256:8b33574f3ce5fbd67450d414c5e10a4272e1f8abd647104ddd07f7c794b592a6",
        "producer_releases": ["v0.11.0", "v0.13.3"],
        "grammar": {
            "fields": ["nodes", "ontology_hash", "relations"],
            "format": "JSON",
            "kind": "KNOWLEDGE_GRAPH_SNAPSHOT",
        },
    },
    {
        "input_id": "protocol-ledger",
        "path": "protocol-ledger.jsonl",
        "byte_length": 4073,
        "sha256": "sha256:821565b78c3d3c8c744e03781eed8129a7e37a5033aaa97aa01e556d34b5469f",
        "producer_releases": ["v0.11.0", "v0.13.3"],
        "grammar": {
            "event_count": 3,
            "event_types": [
                "EXTERNAL_SNAPSHOT_ANCHORED",
                "ARTIFACT_RECORDED",
                "ARTIFACT_RECORDED",
            ],
            "format": "HASH_LINKED_JSONL",
            "schema_version": "1",
        },
    },
]
SUBJECTS = [
    {
        "subject_id": "recon-project",
        "input_id": "recon-project",
        "locator": {"document": "project.json"},
    },
    {
        "subject_id": "recon-record",
        "input_id": "recon-ledger",
        "locator": {"event_type": "RECON_RECORD", "sequence": 1},
    },
    {
        "subject_id": "empty-knowledge-graph",
        "input_id": "graph-snapshot",
        "locator": {"document": "graph-snapshot.json"},
    },
    {
        "subject_id": "graph-base-artifact",
        "input_id": "protocol-ledger",
        "locator": {
            "event_type": "ARTIFACT_RECORDED",
            "record_type": "GraphBaseArtifact",
            "sequence": 2,
        },
    },
    {
        "subject_id": "candidate-subgraph-artifact",
        "input_id": "protocol-ledger",
        "locator": {
            "event_type": "ARTIFACT_RECORDED",
            "record_type": "CandidateSubgraphArtifact",
            "sequence": 3,
        },
    },
]
READER = {
    "commit": "7178bd06e83cb5850afea5af6747e53c03730eec",
    "tree": "e218f60b6cf2abbe11372965b7feed31b0677183",
    "implementations": [
        {
            "path": "src/malleus/recon/store.py",
            "sha256": "sha256:089021ce3134e010e61eebd1f23640e35f7416ffb70e93c89372f5563be84277",
        },
        {
            "path": "src/malleus/kg.py",
            "sha256": "sha256:110b0eea5791c8b1b4495c55b65ab746d10fdc3bd308a7ea24a55612f128e316",
        },
        {
            "path": "src/malleus/assent.py",
            "sha256": "sha256:7b12202f9dcdffd220e23fe5a365a6789b7934bc53d0a638b36e779d3816cf21",
        },
        {
            "path": "src/malleus/accepted.py",
            "sha256": "sha256:dbb0bb88ad7e226211501afaff4466153b7f9632b1ba023f4f0ebb6947eb1d62",
        },
        {
            "path": "src/malleus/ledger.py",
            "sha256": "sha256:f9ef7a53f01ffba150240d8c0f8f3cbe1cfeba04ba216289df39a3e622eb3c7f",
        },
        {
            "path": "src/malleus/ontology.py",
            "sha256": "sha256:665ce9e3ff881f541d00a29cd1ce6c7a0f6b9a96570eb3e48a72fcb141332fd8",
        },
        {
            "path": "src/malleus/migration.py",
            "sha256": "sha256:10964c5328fc4c92a1a3a5fa29f5e62e1a12ed4aebf5a122f60d586866467f4c",
        },
    ],
}
READER_MODULES = {
    "src/malleus/recon/store.py": "malleus.recon.store",
    "src/malleus/kg.py": "malleus.kg",
    "src/malleus/assent.py": "malleus.assent",
    "src/malleus/accepted.py": "malleus.accepted",
    "src/malleus/ledger.py": "malleus.ledger",
    "src/malleus/ontology.py": "malleus.ontology",
    "src/malleus/migration.py": "malleus.migration",
}
FORBIDDEN_POLICY_KEYS = {
    "classification",
    "decision",
    "desired_outcome",
    "migration",
    "recommendation",
    "verdict",
}


class HistoricWireError(RuntimeError):
    """The frozen corpus or its current-reader observation cannot be trusted."""


def canonical_json(value: Any) -> bytes:
    try:
        text = json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        return (text + "\n").encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise HistoricWireError(f"Value is not canonical UTF-8 JSON: {error}") from error


def _digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _digest_file(path: Path) -> str:
    try:
        return _digest(path.read_bytes())
    except OSError as error:
        raise HistoricWireError(f"Cannot read required CC-X04 input '{path}': {error}") from error


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise HistoricWireError(f"Duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _decode_json(text: str, subject: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise HistoricWireError(f"{subject} is not valid UTF-8 JSON: {error}") from error


def _read_json(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise HistoricWireError(f"Cannot read required CC-X04 JSON '{path}': {error}") from error
    return _decode_json(text, str(path))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        data = path.read_bytes()
    except OSError as error:
        raise HistoricWireError(f"Cannot read required CC-X04 JSONL '{path}': {error}") from error
    if not data or not data.endswith(b"\n"):
        raise HistoricWireError(f"{path} must be nonempty newline-terminated JSONL")
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeError as error:
        raise HistoricWireError(f"{path} is not UTF-8: {error}") from error
    result = []
    for number, line in enumerate(lines, start=1):
        if not line:
            raise HistoricWireError(f"{path} line {number} is blank")
        value = _decode_json(line, f"{path} line {number}")
        if not isinstance(value, dict):
            raise HistoricWireError(f"{path} line {number} must be an object")
        result.append(value)
    return result


def _mapping(value: Any, subject: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise HistoricWireError(f"{subject} must be a mapping")
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str], subject: str) -> None:
    actual = set(value)
    if actual != expected:
        raise HistoricWireError(
            f"{subject} keys differ; missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )


def _walk_mappings(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_mappings(child)


def _reject_policy(value: Any, subject: str) -> None:
    for mapping in _walk_mappings(value):
        forbidden = sorted(FORBIDDEN_POLICY_KEYS & set(mapping))
        if forbidden:
            raise HistoricWireError(f"{subject} contains policy keys: {forbidden}")


def _validate_wire_grammar(directory: Path) -> None:
    project = _mapping(_read_json(directory / "project.json"), "project.json")
    _exact_keys(
        project,
        {
            "created_at",
            "creator_id",
            "ontology_hash",
            "schema_version",
            "target_id",
            "title",
        },
        "project.json",
    )
    if project["schema_version"] != "1":
        raise HistoricWireError("project.json schema_version is not 1")

    recon = read_jsonl(directory / "recon-ledger.jsonl")
    if len(recon) != 1 or recon[0].get("sequence") != 1:
        raise HistoricWireError("recon-ledger.jsonl must contain exactly event 1")
    if recon[0].get("event_type") != "RECON_RECORD":
        raise HistoricWireError("recon-ledger.jsonl event 1 is not RECON_RECORD")
    payload = _mapping(recon[0].get("payload"), "RECON_RECORD payload")
    if payload.get("record_type") != "ReviewTarget":
        raise HistoricWireError("RECON_RECORD does not contain the frozen ReviewTarget")
    try:
        JsonlLedger(directory / "recon-ledger.jsonl", recon[0]["ontology_hash"]).read(
            expected_event_count=1
        )
    except LedgerError as error:
        raise HistoricWireError(f"recon ledger envelope is invalid: {error}") from error

    snapshot = _mapping(_read_json(directory / "graph-snapshot.json"), "graph snapshot")
    _exact_keys(snapshot, {"nodes", "ontology_hash", "relations"}, "graph snapshot")
    if snapshot["nodes"] != [] or snapshot["relations"] != []:
        raise HistoricWireError("graph snapshot is not the frozen empty graph")

    protocol = read_jsonl(directory / "protocol-ledger.jsonl")
    if [event.get("sequence") for event in protocol] != [1, 2, 3]:
        raise HistoricWireError("protocol ledger sequences are not exactly 1, 2, 3")
    if [event.get("event_type") for event in protocol] != [
        "EXTERNAL_SNAPSHOT_ANCHORED",
        "ARTIFACT_RECORDED",
        "ARTIFACT_RECORDED",
    ]:
        raise HistoricWireError("protocol ledger event order differs from the frozen grammar")
    if protocol[1]["payload"].get("artifact_type") != "GraphBaseArtifact":
        raise HistoricWireError("protocol event 2 is not GraphBaseArtifact")
    if protocol[2]["payload"].get("artifact_type") != "CandidateSubgraphArtifact":
        raise HistoricWireError("protocol event 3 is not CandidateSubgraphArtifact")
    try:
        JsonlLedger(
            directory / "protocol-ledger.jsonl", protocol[0]["ontology_hash"]
        ).read(expected_event_count=3)
    except LedgerError as error:
        raise HistoricWireError(f"protocol ledger envelope is invalid: {error}") from error
    candidate = protocol[2]["payload"]["artifact"]
    manifest = _mapping(
        _decode_json(candidate["candidate_manifest"], "candidate_manifest"),
        "candidate_manifest",
    )
    writes = manifest.get("writes")
    if not isinstance(writes, list) or len(writes) != 1:
        raise HistoricWireError("candidate manifest must contain exactly one write")
    operation = _mapping(writes[0].get("operation"), "candidate operation")
    if operation.get("record_type") != "ProtocolActor":
        raise HistoricWireError("candidate operation is not ProtocolActor")


def load_corpus(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    document = _mapping(_read_json(path), "CC-X04 corpus")
    _exact_keys(
        document,
        {"schema", "workstream_id", "releases", "inputs", "subjects"},
        "CC-X04 corpus",
    )
    if document["schema"] != "malleus.contract-compiler.historic-wire-corpus/v1":
        raise HistoricWireError("CC-X04 corpus schema is not v1")
    if document["workstream_id"] != "CC-X04":
        raise HistoricWireError("CC-X04 corpus workstream_id is not CC-X04")
    if document["releases"] != RELEASES:
        raise HistoricWireError("CC-X04 producing release coordinates differ")
    if isinstance(document["inputs"], list):
        for actual, expected in zip(document["inputs"], INPUTS, strict=False):
            if isinstance(actual, dict) and actual.get("sha256") != expected["sha256"]:
                raise HistoricWireError(
                    f"{expected['input_id']} declared checksum differs from the frozen checksum"
                )
    if document["inputs"] != INPUTS:
        raise HistoricWireError("CC-X04 input membership or metadata differs")
    if document["subjects"] != SUBJECTS:
        raise HistoricWireError("CC-X04 logical subjects or locators differ")
    _reject_policy(document, "CC-X04 corpus")

    directory = path.parent
    declared = {item["path"] for item in INPUTS}
    physical = {
        item.name
        for item in directory.iterdir()
        if item.is_file() and item.name not in {path.name, "observations.json"}
    }
    undeclared = sorted(physical - declared)
    missing = sorted(declared - physical)
    if undeclared:
        raise HistoricWireError(f"CC-X04 corpus contains undeclared inputs: {undeclared}")
    if missing:
        raise HistoricWireError(f"CC-X04 corpus is missing declared inputs: {missing}")
    for item in INPUTS:
        source = directory / item["path"]
        try:
            data = source.read_bytes()
        except OSError as error:
            raise HistoricWireError(f"Cannot read declared input '{source}': {error}") from error
        if len(data) != item["byte_length"]:
            raise HistoricWireError(f"{item['input_id']} byte length differs")
        if _digest(data) != item["sha256"]:
            raise HistoricWireError(f"{item['input_id']} checksum differs")
    _validate_wire_grammar(directory)
    return deepcopy(dict(document))


def _reader() -> dict[str, Any]:
    for item in READER["implementations"]:
        expected_path = (ROOT / item["path"]).resolve()
        module = importlib.import_module(READER_MODULES[item["path"]])
        origin_value = getattr(module, "__file__", None)
        if not isinstance(origin_value, str) or Path(origin_value).resolve() != expected_path:
            raise HistoricWireError(
                f"Current reader module origin differs for {READER_MODULES[item['path']]}"
            )
        actual = _digest_file(expected_path)
        if actual != item["sha256"]:
            raise HistoricWireError(
                f"Current reader source differs at {item['path']}; record a fresh measurement"
            )
    return deepcopy(READER)


def _input_ref(corpus: Mapping[str, Any], input_id: str) -> dict[str, Any]:
    item = next(value for value in corpus["inputs"] if value["input_id"] == input_id)
    return {
        "input_id": item["input_id"],
        "path": item["path"],
        "byte_length": item["byte_length"],
        "sha256": item["sha256"],
    }


def _error(error: Exception) -> dict[str, Any]:
    return {
        "error_type": type(error).__name__,
        "message": str(error),
        "arguments": list(error.args),
    }


def _recon_observations(
    corpus: Mapping[str, Any], directory: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    with tempfile.TemporaryDirectory(prefix="malleus-ccx04-recon-") as temporary:
        project_dir = Path(temporary)
        shutil.copyfile(directory / "project.json", project_dir / "project.json")
        shutil.copyfile(directory / "recon-ledger.jsonl", project_dir / "ledger.jsonl")
        project = ReconProject(project_dir)
        events, records = project.snapshot()
        common = {
            "current_ontology_hash": project.ontology_hash,
            "event_count": len(events),
            "migration_receipt_count": len(project.migrations.receipts),
            "record_count": len(records),
            "record_ids": sorted(records),
            "verified_ontology_hashes": list(project.ledger.verified_ontology_hashes),
        }
        project_result = {
            "subject_id": "recon-project",
            "input": _input_ref(corpus, "recon-project"),
            "end_to_end": {
                "outcome": "ACCEPTED",
                "reader": "malleus.recon.store.ReconProject.snapshot",
                "facts": common,
            },
            "intrinsic": {"outcome": "NOT_APPLICABLE"},
        }
        record = records["target:historic-wire"]
        record_result = {
            "subject_id": "recon-record",
            "input": _input_ref(corpus, "recon-ledger"),
            "end_to_end": {
                "outcome": "ACCEPTED",
                "reader": "malleus.recon.store.ReconProject.snapshot",
                "facts": {
                    **common,
                    "record_id": record.record["id"],
                    "record_type": record.record_type,
                },
            },
            "intrinsic": {"outcome": "NOT_APPLICABLE"},
        }
        return project_result, record_result


def _graph_observation(corpus: Mapping[str, Any], directory: Path) -> dict[str, Any]:
    snapshot = _read_json(directory / "graph-snapshot.json")
    registry = OntologyRegistry(ASSENT_SCHEMA)
    try:
        graph = KnowledgeGraph.from_records(registry, snapshot)
    except (TypeError, ValueError) as error:
        end_to_end = {
            "outcome": "REFUSED",
            "reader": "malleus.kg.KnowledgeGraph.from_records",
            "error": _error(error),
        }
    else:
        end_to_end = {
            "outcome": "ACCEPTED",
            "reader": "malleus.kg.KnowledgeGraph.from_records",
            "facts": {"node_count": graph.node_count, "edge_count": graph.edge_count},
        }
    return {
        "subject_id": "empty-knowledge-graph",
        "input": _input_ref(corpus, "graph-snapshot"),
        "end_to_end": end_to_end,
        "intrinsic": {"outcome": "NOT_APPLICABLE"},
    }


def _graph_base_intrinsic(
    registry: OntologyRegistry,
    artifact: dict[str, Any],
    snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    semantic_hash = graph_base_artifact_digest(
        artifact_id=artifact["id"],
        artifact_version=artifact["artifact_version"],
        graph_ontology_hash=artifact["graph_ontology_hash"],
        base_state_digest=artifact["base_state_digest"],
        base_record_metadata=artifact["base_record_metadata"],
    )
    base_record_count = len(parse_graph_base_metadata(artifact["base_record_metadata"]))
    content_hash_matches = (
        record_hash("GraphBaseArtifact", artifact) == artifact["content_hash"]
    )
    ontology_instance_errors = registry.validate_instance("GraphBaseArtifact", artifact)
    semantic_hash_matches = semantic_hash == artifact["artifact_hash"]
    record_count_matches = artifact["base_record_count"] == base_record_count
    snapshot_ontology_matches = artifact["graph_ontology_hash"] == snapshot["ontology_hash"]
    snapshot_state_matches = artifact["base_state_digest"] == content_digest(snapshot)
    facts = {
        "base_record_count": base_record_count,
        "content_hash_matches": content_hash_matches,
        "ontology_instance_errors": ontology_instance_errors,
        "record_count_matches": record_count_matches,
        "semantic_hash_matches": semantic_hash_matches,
        "snapshot_ontology_matches": snapshot_ontology_matches,
        "snapshot_state_matches": snapshot_state_matches,
    }
    passed = (
        content_hash_matches
        and not ontology_instance_errors
        and record_count_matches
        and semantic_hash_matches
        and snapshot_ontology_matches
        and snapshot_state_matches
    )
    return {
        "outcome": "PASS" if passed else "FAIL",
        "call_path": [
            "malleus.ontology.OntologyRegistry.validate_instance",
            "malleus.ledger.record_hash",
            "malleus.accepted.graph_base_artifact_digest",
        ],
        "facts": facts,
    }


def _candidate_intrinsic(
    registry: OntologyRegistry,
    artifact: dict[str, Any],
    graph_base: Mapping[str, Any],
) -> dict[str, Any]:
    names = (
        "candidate_schema_version",
        "graph_base_id",
        "graph_base_hash",
        "graph_ontology_hash",
        "base_acceptance_head",
        "base_materialization_head",
        "base_state_digest",
        "candidate_manifest",
        "candidate_manifest_hash",
        "candidate_write_count",
        "candidate_digest",
        "candidate_state_digest",
    )
    semantic_hash = candidate_artifact_digest(
        artifact_id=artifact["id"],
        artifact_version=artifact["artifact_version"],
        **{name: artifact[name] for name in names},
    )
    content_hash_matches = (
        record_hash("CandidateSubgraphArtifact", artifact) == artifact["content_hash"]
    )
    manifest_write_count = len(parse_candidate_manifest(artifact["candidate_manifest"]))
    ontology_instance_errors = registry.validate_instance(
        "CandidateSubgraphArtifact", artifact
    )
    semantic_hash_matches = semantic_hash == artifact["artifact_hash"]
    base_record_matches = (
        artifact["graph_base_id"] == graph_base["id"]
        and artifact["graph_base_hash"] == graph_base["content_hash"]
    )
    base_state_matches = artifact["base_state_digest"] == graph_base["base_state_digest"]
    ontology_matches = artifact["graph_ontology_hash"] == graph_base["graph_ontology_hash"]
    source_matches = artifact["source_record_ids"] == [graph_base["id"]]
    write_count_matches = artifact["candidate_write_count"] == manifest_write_count
    facts = {
        "base_record_matches": base_record_matches,
        "base_state_matches": base_state_matches,
        "content_hash_matches": content_hash_matches,
        "manifest_write_count": manifest_write_count,
        "ontology_matches": ontology_matches,
        "ontology_instance_errors": ontology_instance_errors,
        "semantic_hash_matches": semantic_hash_matches,
        "source_matches": source_matches,
        "write_count_matches": write_count_matches,
    }
    passed = (
        base_record_matches
        and base_state_matches
        and content_hash_matches
        and ontology_matches
        and not ontology_instance_errors
        and semantic_hash_matches
        and source_matches
        and write_count_matches
    )
    return {
        "outcome": "PASS" if passed else "FAIL",
        "call_path": [
            "malleus.ontology.OntologyRegistry.validate_instance",
            "malleus.ledger.record_hash",
            "malleus.accepted.candidate_artifact_digest",
        ],
        "facts": facts,
    }


def _protocol_observations(
    corpus: Mapping[str, Any], directory: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    events = read_jsonl(directory / "protocol-ledger.jsonl")
    graph_base = events[1]["payload"]["artifact"]
    candidate = events[2]["payload"]["artifact"]
    snapshot = _mapping(_read_json(directory / "graph-snapshot.json"), "graph snapshot")
    registry = OntologyRegistry(ASSENT_SCHEMA)
    try:
        ProtocolLedger(
            directory / "protocol-ledger.jsonl",
            registry,
            accepted_graph_base=KnowledgeGraph(registry),
        ).replay()
    except LedgerError as error:
        refusal = _error(error)
    else:
        raise HistoricWireError("Current protocol reader unexpectedly accepted the frozen ledger")
    blocked = {
        "outcome": "NOT_REACHED",
        "reader": "malleus.assent.ProtocolLedger.replay",
        "blocked_by": "protocol-envelope-event-1",
        "error": refusal,
    }
    return (
        {
            "subject_id": "graph-base-artifact",
            "input": _input_ref(corpus, "protocol-ledger"),
            "end_to_end": blocked,
            "intrinsic": _graph_base_intrinsic(registry, graph_base, snapshot),
        },
        {
            "subject_id": "candidate-subgraph-artifact",
            "input": _input_ref(corpus, "protocol-ledger"),
            "end_to_end": deepcopy(blocked),
            "intrinsic": _candidate_intrinsic(registry, candidate, graph_base),
        },
    )


def render_observations(path: Path = MANIFEST_PATH) -> dict[str, Any]:
    corpus = load_corpus(path)
    reader = _reader()
    directory = path.parent
    recon_project, recon_record = _recon_observations(corpus, directory)
    graph_base, candidate = _protocol_observations(corpus, directory)
    result = {
        "schema": "malleus.contract-compiler.historic-wire-observations/v1",
        "workstream_id": "CC-X04",
        "corpus_sha256": _digest_file(path),
        "reader": reader,
        "observations": [
            recon_project,
            recon_record,
            _graph_observation(corpus, directory),
            graph_base,
            candidate,
        ],
    }
    validate_observations(result)
    return result


def _valid_digest(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith("sha256:"):
        return False
    hexadecimal = value.removeprefix("sha256:")
    if len(hexadecimal) != 64:
        return False
    try:
        int(hexadecimal, 16)
    except ValueError:
        return False
    return hexadecimal == hexadecimal.lower()


def validate_observations(document: Any) -> None:
    root = _mapping(document, "CC-X04 observations")
    _exact_keys(
        root,
        {"schema", "workstream_id", "corpus_sha256", "reader", "observations"},
        "CC-X04 observations",
    )
    if root["schema"] != "malleus.contract-compiler.historic-wire-observations/v1":
        raise HistoricWireError("CC-X04 observations schema is not v1")
    if root["workstream_id"] != "CC-X04":
        raise HistoricWireError("CC-X04 observations workstream_id is not CC-X04")
    if not _valid_digest(root["corpus_sha256"]):
        raise HistoricWireError("CC-X04 observations corpus_sha256 is invalid")
    if root["reader"] != READER:
        raise HistoricWireError("CC-X04 reader binding differs")
    values = root["observations"]
    if not isinstance(values, list):
        raise HistoricWireError("CC-X04 observations must be a list")
    if [item.get("subject_id") if isinstance(item, dict) else None for item in values] != [
        item["subject_id"] for item in SUBJECTS
    ]:
        raise HistoricWireError("CC-X04 observation subjects or order differs")
    for index, item in enumerate(values):
        item = _mapping(item, f"CC-X04 observation {index}")
        _exact_keys(
            item,
            {"subject_id", "input", "end_to_end", "intrinsic"},
            f"CC-X04 observation {index}",
        )
        source = _mapping(item["input"], f"CC-X04 observation {index} input")
        _exact_keys(
            source,
            {"input_id", "path", "byte_length", "sha256"},
            f"CC-X04 observation {index} input",
        )
        if not _valid_digest(source["sha256"]):
            raise HistoricWireError(f"CC-X04 observation {index} input checksum is invalid")
        for stage in ("end_to_end", "intrinsic"):
            value = _mapping(item[stage], f"CC-X04 observation {index} {stage}")
            if value.get("outcome") not in {
                "ACCEPTED",
                "FAIL",
                "NOT_APPLICABLE",
                "NOT_REACHED",
                "PASS",
                "REFUSED",
            }:
                raise HistoricWireError(
                    f"CC-X04 observation {index} {stage} outcome is invalid"
                )
    _reject_policy(root, "CC-X04 observations")


def check_observations(
    corpus_path: Path = MANIFEST_PATH,
    observations_path: Path = OBSERVATIONS_PATH,
) -> None:
    retained = _read_json(observations_path)
    validate_observations(retained)
    if retained["corpus_sha256"] != _digest_file(corpus_path):
        raise HistoricWireError("Retained observations name a different corpus checksum")
    fresh = render_observations(corpus_path)
    if canonical_json(retained) != canonical_json(fresh):
        raise HistoricWireError("Fresh current-reader observations differ from retained bytes")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        nargs="?",
        choices=("check", "render"),
        default="check",
    )
    arguments = parser.parse_args(argv)
    if arguments.action == "render":
        sys.stdout.buffer.write(canonical_json(render_observations()))
    else:
        check_observations()
        print("CC-X04 retained observations match current readers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
