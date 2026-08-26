"""CC-X04 frozen historic-wire measurements."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

import pytest

from scripts.contract_compiler_ledger import verify_evidence_snapshot


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "contract_compiler_historic_wire.py"
CORPUS = (
    ROOT / "conformance" / "contract_compiler" / "v0" / "historic_wire"
)
MANIFEST = CORPUS / "corpus.json"
OBSERVATIONS = CORPUS / "observations.json"
EVIDENCE = (
    ROOT / "conformance" / "contract_compiler" / "v0" / "evidence" / "CC-X04.json"
)

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
INPUTS = {
    "recon-project": (
        "project.json",
        282,
        "sha256:0808d77254479bfedc7b67790182644db22f71c29b90bd61f0356bb232deeb21",
    ),
    "recon-ledger": (
        "recon-ledger.jsonl",
        802,
        "sha256:c3720e2031a51d9f27b22ef0cd4b19438858fa062423d97382b66e3e38ab264e",
    ),
    "graph-snapshot": (
        "graph-snapshot.json",
        118,
        "sha256:8b33574f3ce5fbd67450d414c5e10a4272e1f8abd647104ddd07f7c794b592a6",
    ),
    "protocol-ledger": (
        "protocol-ledger.jsonl",
        4073,
        "sha256:821565b78c3d3c8c744e03781eed8129a7e37a5033aaa97aa01e556d34b5469f",
    ),
}
SUBJECTS = [
    "recon-project",
    "recon-record",
    "empty-knowledge-graph",
    "graph-base-artifact",
    "candidate-subgraph-artifact",
]
FORBIDDEN_POLICY_KEYS = {
    "classification",
    "decision",
    "desired_outcome",
    "migration",
    "recommendation",
    "verdict",
}


def _load_runner():
    spec = importlib.util.spec_from_file_location(
        "contract_compiler_historic_wire", SCRIPT
    )
    if spec is None or spec.loader is None:
        raise AssertionError(f"Cannot load CC-X04 runner: {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


runner = _load_runner()


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def _walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def test_corpus_is_one_exact_copy_bound_to_both_releases():
    document = runner.load_corpus(MANIFEST)

    assert set(document) == {
        "schema",
        "workstream_id",
        "releases",
        "inputs",
        "subjects",
    }
    assert document["schema"] == "malleus.contract-compiler.historic-wire-corpus/v1"
    assert document["workstream_id"] == "CC-X04"
    assert document["releases"] == RELEASES
    assert [item["input_id"] for item in document["inputs"]] == list(INPUTS)

    for item in document["inputs"]:
        filename, length, digest = INPUTS[item["input_id"]]
        assert item["path"] == filename
        assert item["byte_length"] == length
        assert item["sha256"] == digest
        assert item["producer_releases"] == ["v0.11.0", "v0.13.3"]
        assert item["grammar"]


def test_four_physical_inputs_have_the_frozen_bytes_and_no_alias_copies():
    document = runner.load_corpus(MANIFEST)
    declared = {item["path"] for item in document["inputs"]}
    physical = {
        path.name
        for path in CORPUS.iterdir()
        if path.is_file() and path.name not in {"corpus.json", "observations.json"}
    }
    assert physical == declared == {value[0] for value in INPUTS.values()}

    for item in document["inputs"]:
        data = (CORPUS / item["path"]).read_bytes()
        assert len(data) == item["byte_length"]
        assert _sha256(data) == item["sha256"]


def test_corpus_addresses_exactly_five_logical_subjects_and_old_wire_grammar():
    document = runner.load_corpus(MANIFEST)
    assert [item["subject_id"] for item in document["subjects"]] == SUBJECTS

    subjects = {item["subject_id"]: item for item in document["subjects"]}
    assert subjects["recon-record"]["locator"] == {
        "event_type": "RECON_RECORD",
        "sequence": 1,
    }
    assert subjects["graph-base-artifact"]["locator"] == {
        "event_type": "ARTIFACT_RECORDED",
        "record_type": "GraphBaseArtifact",
        "sequence": 2,
    }
    assert subjects["candidate-subgraph-artifact"]["locator"] == {
        "event_type": "ARTIFACT_RECORDED",
        "record_type": "CandidateSubgraphArtifact",
        "sequence": 3,
    }

    protocol = runner.read_jsonl(CORPUS / "protocol-ledger.jsonl")
    assert [event["event_type"] for event in protocol] == [
        "EXTERNAL_SNAPSHOT_ANCHORED",
        "ARTIFACT_RECORDED",
        "ARTIFACT_RECORDED",
    ]
    candidate = protocol[2]["payload"]["artifact"]
    manifest = json.loads(candidate["candidate_manifest"])
    assert manifest["schema_version"] == "2"
    assert len(manifest["writes"]) == 1
    operation = manifest["writes"][0]["operation"]
    assert operation["kind"] == "ENTITY"
    assert operation["record_type"] == "ProtocolActor"


def test_current_reader_observations_are_raw_and_cover_every_subject():
    document = _read(OBSERVATIONS)
    runner.validate_observations(document)

    assert set(document) == {
        "schema",
        "workstream_id",
        "corpus_sha256",
        "reader",
        "observations",
    }
    assert document["reader"]["commit"] == "7178bd0a86ead814ed3ae6525eea8b4e7d9f6417"
    assert document["reader"]["tree"] == "e218f60b6cf2abbe11372965b7feed31b0677183"
    assert [item["subject_id"] for item in document["observations"]] == SUBJECTS
    for mapping in _walk(document):
        assert not FORBIDDEN_POLICY_KEYS & set(mapping)


def test_current_recon_reader_accepts_project_and_record_through_receipt():
    observations = {
        item["subject_id"]: item for item in _read(OBSERVATIONS)["observations"]
    }
    for subject_id in ("recon-project", "recon-record"):
        result = observations[subject_id]["end_to_end"]
        assert result["outcome"] == "ACCEPTED"
        assert result["reader"] == "malleus.recon.store.ReconProject.snapshot"
        assert result["facts"]["verified_ontology_hashes"]
        assert result["facts"]["migration_receipt_count"] == 1
    assert observations["recon-project"]["end_to_end"]["facts"]["event_count"] == 1
    assert observations["recon-record"]["end_to_end"]["facts"]["record_count"] == 1


def test_current_knowledge_graph_reader_refuses_snapshot_with_exact_error():
    item = next(
        item
        for item in _read(OBSERVATIONS)["observations"]
        if item["subject_id"] == "empty-knowledge-graph"
    )
    result = item["end_to_end"]
    assert result["outcome"] == "REFUSED"
    assert result["reader"] == "malleus.kg.KnowledgeGraph.from_records"
    assert result["error"] == {
        "error_type": "ValueError",
        "message": (
            "Record export has unknown families: nodes, ontology_hash; expected exactly "
            "entities, events, relations, signals"
        ),
        "arguments": [
            "Record export has unknown families: nodes, ontology_hash; expected exactly "
            "entities, events, relations, signals"
        ],
    }


def test_protocol_envelope_refusal_keeps_intrinsic_artifact_results_separate():
    observations = {
        item["subject_id"]: item for item in _read(OBSERVATIONS)["observations"]
    }
    expected_error = {
        "error_type": "LedgerError",
        "message": (
            "event 1: ontology_hash does not match this ledger under any payload "
            "grammar it accepts"
        ),
        "arguments": [
            "event 1: ontology_hash does not match this ledger under any payload "
            "grammar it accepts"
        ],
    }
    for subject_id in ("graph-base-artifact", "candidate-subgraph-artifact"):
        item = observations[subject_id]
        assert item["end_to_end"] == {
            "outcome": "NOT_REACHED",
            "blocked_by": "protocol-envelope-event-1",
            "error": expected_error,
        }
        assert item["intrinsic"]["outcome"] == "PASS"
        assert item["intrinsic"]["facts"]


def test_fresh_observation_is_deterministic_and_does_not_rewrite_inputs():
    before = {
        item["input_id"]: (CORPUS / item["path"]).read_bytes()
        for item in runner.load_corpus(MANIFEST)["inputs"]
    }
    first = runner.render_observations(MANIFEST)
    second = runner.render_observations(MANIFEST)
    after = {
        item["input_id"]: (CORPUS / item["path"]).read_bytes()
        for item in runner.load_corpus(MANIFEST)["inputs"]
    }

    assert runner.canonical_json(first) == runner.canonical_json(second)
    assert runner.canonical_json(first) == OBSERVATIONS.read_bytes()
    assert after == before


def test_bad_checksum_and_undeclared_input_fail_loud(tmp_path):
    copied = tmp_path / "historic_wire"
    shutil.copytree(CORPUS, copied)
    manifest = _read(copied / "corpus.json")
    corrupt = deepcopy(manifest)
    corrupt["inputs"][0]["sha256"] = "sha256:" + "0" * 64
    (copied / "corpus.json").write_bytes(runner.canonical_json(corrupt))
    with pytest.raises(runner.HistoricWireError, match="checksum"):
        runner.load_corpus(copied / "corpus.json")

    (copied / "corpus.json").write_bytes(runner.canonical_json(manifest))
    (copied / "undeclared.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(runner.HistoricWireError, match="undeclared"):
        runner.load_corpus(copied / "corpus.json")


def test_evidence_binds_every_owned_artifact():
    report = verify_evidence_snapshot(EVIDENCE, ROOT)
    assert report["workstream_id"] == "CC-X04"
    assert {item["path"] for item in report["artifacts"]} == {
        "conformance/contract_compiler/v0/historic_wire/project.json",
        "conformance/contract_compiler/v0/historic_wire/recon-ledger.jsonl",
        "conformance/contract_compiler/v0/historic_wire/graph-snapshot.json",
        "conformance/contract_compiler/v0/historic_wire/protocol-ledger.jsonl",
        "conformance/contract_compiler/v0/historic_wire/corpus.json",
        "conformance/contract_compiler/v0/historic_wire/observations.json",
        "scripts/contract_compiler_historic_wire.py",
        "tests/test_contract_compiler_historic_wire.py",
    }
