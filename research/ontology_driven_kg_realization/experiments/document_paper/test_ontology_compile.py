"""Hard tests for the exact paper-local ontology compiler harness."""

from __future__ import annotations

from hashlib import sha256
from importlib.resources import files
import json
from pathlib import Path

import pytest

from malleus._contract_linkml_adapter import LinkMLRefusalReason
from malleus._contract_pipeline import load_validated_contract_artifact
from malleus._contract_source import RefusalReason
from research.ontology_driven_kg_realization.experiments.document_paper import (
    ontology_compile as harness,
)
from research.ontology_driven_kg_realization.experiments.document_paper.ontology_compile import (
    COMPILE_RECEIPT_FILENAME,
    VALIDATED_CONTRACT_FILENAME,
    CompileStage,
    ExactSource,
    HarnessRefusalReason,
    OntologyCompileRefusal,
    compile_exact_ontology,
    publish_compilation,
)


ROOT = Path(__file__).resolve().parents[4]
ROOT_LOCATOR = "paper-v4:marine-ontology"
VALID_ROOT = b"""\
id: https://example.malleus.dev/marine
name: marine
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
  marine: https://example.malleus.dev/marine/
imports:
  - linkml:types
  - malleus
slots:
  observation_code:
    range: string
classes:
  MarineObservation:
    is_a: Entity
    slots:
      - observation_code
    slot_usage:
      observation_code:
        required: true
"""


def _digest(source: bytes) -> str:
    return "sha256:" + sha256(source).hexdigest()


def _source(locator: str, source: bytes) -> ExactSource:
    return ExactSource(locator, source, _digest(source))


def _inputs(root: bytes = VALID_ROOT) -> dict[str, ExactSource]:
    malleus = (ROOT / "ontology/malleus.yaml").read_bytes()
    linkml_types = (
        files("linkml_runtime")
        .joinpath("linkml_model", "model", "schema", "types.yaml")
        .read_bytes()
    )
    return {
        "root": _source(ROOT_LOCATOR, root),
        "malleus": _source("malleus", malleus),
        "linkml_types": _source("linkml:types", linkml_types),
    }


def _compile(root: bytes = VALID_ROOT):
    return compile_exact_ontology(**_inputs(root))


def test_compiles_imported_malleus_to_canonical_retained_outputs() -> None:
    first = _compile()
    second = _compile()

    assert first.validated_contract_bytes == second.validated_contract_bytes
    assert first.receipt_bytes == second.receipt_bytes
    assert first.validated_contract_bytes == first.compilation.artifact.artifact_bytes
    assert (
        json.dumps(
            json.loads(first.receipt_bytes),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode()
        == first.receipt_bytes
    )
    receipt = json.loads(first.receipt_bytes)
    assert receipt["status"] == "ACCEPTED"
    assert receipt["root"]["source_sha256"] == _digest(VALID_ROOT)
    assert [source["module_id"] for source in receipt["sources"]] == [
        "linkml:types",
        "malleus",
        ROOT_LOCATOR,
    ]
    assert load_validated_contract_artifact(first.validated_contract_bytes)


def test_paper_v4_acceptance_event_binds_the_compilable_ontology() -> None:
    run = ROOT / "paper-v4/experiment/ontology-run"
    ontology = (run / "ontology.yaml").read_bytes()
    event_source = (run / "acceptance.jsonl").read_bytes()

    assert event_source.count(b"\n") == 1
    event = json.loads(event_source)
    assert event == {
        "actor_id": "actor:paper-v4-evaluator",
        "decision": "ACCEPT_FOR_POPULATION",
        "event_type": "ONTOLOGY_DECISION",
        "ontology_sha256": _digest(ontology),
        "ordinal": 1,
        "schema": "malleus.paper-v4.ontology-decision/v1",
    }

    inputs = _inputs(ontology)
    copied_malleus = (run / "inputs/malleus.yaml").read_bytes()
    inputs["malleus"] = _source("malleus", copied_malleus)
    receipt = json.loads(compile_exact_ontology(**inputs).receipt_bytes)
    assert receipt["status"] == "ACCEPTED"
    assert receipt["root"]["source_sha256"] == event["ontology_sha256"]


def test_input_digest_drift_refuses_before_compilation() -> None:
    inputs = _inputs()
    inputs["root"] = ExactSource(
        ROOT_LOCATOR,
        VALID_ROOT + b"\n",
        _digest(VALID_ROOT),
    )

    with pytest.raises(OntologyCompileRefusal) as caught:
        compile_exact_ontology(**inputs)

    assert caught.value.stage is CompileStage.INPUT
    assert caught.value.reason is HarnessRefusalReason.SHA256_MISMATCH
    assert caught.value.diagnostics == ()


def test_unknown_import_refuses_at_closed_source_boundary() -> None:
    source = VALID_ROOT.replace(
        b"  - malleus\n",
        b"  - malleus\n  - https://example.test/uncommitted-import\n",
    )

    with pytest.raises(OntologyCompileRefusal) as caught:
        _compile(source)

    refusal = caught.value
    assert refusal.stage is CompileStage.SOURCE_CLOSURE
    assert refusal.reason is RefusalReason.RESOLUTION_REFUSED
    assert refusal.__cause__ is not None
    assert refusal.diagnostics[0]["type"] == "SourceBoundaryRefusal"
    assert refusal.diagnostics[0]["request"]["literal_import"] == (
        "https://example.test/uncommitted-import"
    )
    assert refusal.diagnostics[1]["type"] == "CollaboratorRefusal"


def test_known_default_prefix_field_retains_nested_adapter_diagnostic() -> None:
    source = VALID_ROOT.replace(
        b"name: marine\n",
        b"name: marine\ndefault_prefix: marine\n",
    )

    with pytest.raises(OntologyCompileRefusal) as caught:
        _compile(source)

    refusal = caught.value
    assert refusal.stage is CompileStage.SOURCE_CLOSURE
    assert refusal.reason is RefusalReason.IMPORT_READER_REFUSED
    assert refusal.diagnostics[-1]["type"] == "LinkMLAdapterRefusal"
    assert refusal.diagnostics[-1]["reason"] == LinkMLRefusalReason.REJECTED_SOURCE.name
    assert refusal.diagnostics[-1]["path"] == ["default_prefix"]
    receipt = json.loads(refusal.canonical_receipt_bytes())
    assert receipt["stage"] == "SOURCE_CLOSURE"
    assert receipt["reason"] == "IMPORT_READER_REFUSED"
    assert receipt["diagnostics"][-1]["reason"] == "REJECTED_SOURCE"


def test_publication_refuses_overwrite_without_changing_existing_output(
    tmp_path: Path,
) -> None:
    result = _compile()
    destination = tmp_path / "compiled"
    destination.mkdir()
    marker = destination / "marker"
    marker.write_bytes(b"keep")

    with pytest.raises(OntologyCompileRefusal) as caught:
        publish_compilation(result, destination)

    assert caught.value.stage is CompileStage.PUBLICATION
    assert caught.value.reason is HarnessRefusalReason.OUTPUT_EXISTS
    assert marker.read_bytes() == b"keep"
    assert tuple(destination.iterdir()) == (marker,)


def test_publication_is_all_or_nothing_when_second_staged_write_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result = _compile()
    destination = tmp_path / "compiled"
    real_write = harness._write_exclusive

    def fail_receipt(path: Path, source: bytes) -> None:
        if path.name == COMPILE_RECEIPT_FILENAME:
            raise OSError("injected write refusal")
        real_write(path, source)

    monkeypatch.setattr(harness, "_write_exclusive", fail_receipt)

    with pytest.raises(OntologyCompileRefusal) as caught:
        publish_compilation(result, destination)

    assert caught.value.stage is CompileStage.PUBLICATION
    assert caught.value.reason is HarnessRefusalReason.PUBLICATION_FAILED
    assert not destination.exists()
    assert not any(tmp_path.glob(".compiled.*"))


def test_successful_publication_contains_only_the_two_exact_outputs(
    tmp_path: Path,
) -> None:
    result = _compile()
    destination = publish_compilation(result, tmp_path / "compiled")

    assert {path.name for path in destination.iterdir()} == {
        VALIDATED_CONTRACT_FILENAME,
        COMPILE_RECEIPT_FILENAME,
    }
    assert (destination / VALIDATED_CONTRACT_FILENAME).read_bytes() == (
        result.validated_contract_bytes
    )
    assert (destination / COMPILE_RECEIPT_FILENAME).read_bytes() == (
        result.receipt_bytes
    )
