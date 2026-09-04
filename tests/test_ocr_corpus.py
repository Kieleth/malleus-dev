from __future__ import annotations

import hashlib
import json
import platform
import re
import struct
import subprocess
import sys
import zlib
from io import BytesIO
from importlib.resources import files
from pathlib import Path, PurePosixPath
from typing import Any, Iterator

import pytest
import PIL
import pypdf
import reportlab
from PIL import Image
from pypdf import PdfReader

import malleus
import malleus.compiler as compiler
from malleus.ocr.bundle import PROFILE_ID, PROFILE_VERSION, Bundle
from malleus.ocr.verify import PLANES, VerificationResult, profile_registry, verify_bundle
from malleus.source import source_artifact_fields

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "conformance" / "ocr" / "v0" / "corpus"
MANIFEST = CORPUS / "corpus.json"
CHECKSUMS = CORPUS / "checksums.json"
GENERATOR = CORPUS / "generate.py"
OCR_ONTOLOGY = ROOT / "ontology" / "domains" / "ocr.yaml"
ROOT_ONTOLOGY = ROOT / "ontology" / "malleus.yaml"
REGISTRATION_CASE = (
    ROOT / "src" / "malleus" / "ocr" / "cases" / "registration-is-not-a-reading.json"
)
CONTROL_FILES = {"README.md", "checksums.json", "generate.py"}

REFERENCE_READER = {
    "description": "Fixed readings for self-authored fixtures. No recognition engine is invoked.",
    "id": "malleus.fixture.control_reader@1",
    "kind": "deterministic_control_reader",
    "production_ocr": False,
}
RASTER_BINDINGS = {
    "failed-attempt": (
        (
            "cases/failed-attempt/rasters/image-1.png",
            "fixture:failed-attempt:raster:image-1",
            "image:1",
        ),
    ),
    "region-control": (
        (
            "cases/region-control/rasters/image-1.png",
            "fixture:region-control:raster:image-1",
            "image:1",
        ),
    ),
    "multipage-control": (
        (
            "cases/multipage-control/rasters/page-1.png",
            "fixture:multipage-control:raster:page-1",
            "page:1",
        ),
        (
            "cases/multipage-control/rasters/page-2.png",
            "fixture:multipage-control:raster:page-2",
            "page:2",
        ),
    ),
    "incomplete-sequence": (
        (
            "cases/incomplete-sequence/rasters/page-1.png",
            "fixture:incomplete-sequence:raster:page-1",
            "page:1",
        ),
        (
            "cases/incomplete-sequence/rasters/page-3.png",
            "fixture:incomplete-sequence:raster:page-3",
            "page:3",
        ),
    ),
}
PDF_METADATA = {
    "/Author": "Malleus self-authored fixture corpus",
    "/CreationDate": "D:20000101000000+00'00'",
    "/Creator": "conformance/ocr/v0/corpus/generate.py",
    "/Keywords": "",
    "/ModDate": "D:20000101000000+00'00'",
    "/Producer": "ReportLab PDF Library - (opensource)",
    "/Subject": "Deterministic raster-only OCR control document",
    "/Trapped": "/False",
}
PDF_TITLES = {
    "incomplete-sequence": "Malleus OCR incomplete sequence",
    "multipage-control": "Malleus OCR multipage control",
}
CREDENTIAL_KEYS = {
    "access_key",
    "access_key_id",
    "access_token",
    "api_key",
    "auth_token",
    "authorization",
    "bearer_token",
    "client_secret",
    "cookie",
    "credential",
    "credentials",
    "password",
    "passwd",
    "private_key",
    "refresh_token",
    "secret",
    "secret_access_key",
    "session_cookie",
}
CREDENTIAL_KEY_FORMS = {key.replace("_", "") for key in CREDENTIAL_KEYS}
LOCAL_PATH = re.compile(
    r"(?:^|[\s('=])(?:/(?!/)[^\s]+|[A-Za-z]:[\\/][^\s]*|file:///[^\s]*)",
)

IMPLEMENTED_MUTATIONS = {
    "failed-attempt": {},
    "incomplete-sequence": {
        "observed-without-raster": ((), {"page:2": "NOT_RENDERED"}),
    },
    "multipage-control": {
        "correction-text-digest-mismatch": (("OCR-D015",), {}),
    },
    "region-control": {
        "hypothesis-attempt-cross-region": (("OCR-D003",), {}),
        "selection-hypothesis-cross-region": (("OCR-D003",), {}),
    },
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def _manifest() -> dict[str, Any]:
    return _load(MANIFEST)


def _artifact_path(relative: str) -> Path:
    assert isinstance(relative, str) and relative
    path = PurePosixPath(relative)
    assert not path.is_absolute()
    assert path.as_posix() == relative
    assert "." not in path.parts and ".." not in path.parts
    resolved = (CORPUS / Path(*path.parts)).resolve()
    assert resolved.is_relative_to(CORPUS.resolve())
    return resolved


def _digest(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _canonical(value: object) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _public_ocr_compilation() -> compiler.ValidatedContractCompilation:
    return compiler.compile_linkml_contract(
        root_locator="ocr",
        sources={
            "ocr": OCR_ONTOLOGY.read_bytes(),
            "malleus": ROOT_ONTOLOGY.read_bytes(),
            "linkml:types": files("linkml_runtime")
            .joinpath("linkml_model", "model", "schema", "types.yaml")
            .read_bytes(),
        },
    )


def _structural_partial_contract(
    compiled: compiler.ValidatedContractCompilation,
) -> compiler.PartialEffectiveContract:
    machine = compiler.ProtocolMachineProgram.from_bytes(
        _canonical(
            {
                "capabilities": [],
                "events": {
                    "ARTIFACT_REGISTERED": {
                        "instructions": [
                            {
                                "id_field": "artifact_id",
                                "opcode": "REQUIRE_GLOBAL_ID_ABSENT",
                                "refusal": "GLOBAL_RECORD_ID_EXISTS",
                            },
                            {
                                "opcode": "STORE_EVENT_RECORD",
                                "record_type": "ArtifactRecord",
                            },
                        ],
                        "record_type": "ArtifactRecord",
                    }
                },
                "grammar": "malleus.protocol-machine/private-v0",
                "indexes": {},
                "record_schemas": {
                    "ArtifactRecord": {
                        "fields": {
                            "artifact_id": "STRING",
                            "artifact_identity": "DIGEST",
                        },
                        "id_field": "artifact_id",
                        "input_fields": ["artifact_id", "artifact_identity"],
                    }
                },
            }
        )
    )
    normative = compiler.compose_normative_profile(
        protocol_machine_program=machine,
        policy_programs={},
        capability_refs=(),
    )
    return compiler.compose_partial_effective_contract(
        validated_fact_set_sha256=compiled.artifact.validated_fact_set_sha256,
        normative_profile=normative,
    )


@pytest.fixture(scope="module")
def public_ocr_contract() -> tuple[
    compiler.ValidatedContractCompilation,
    compiler.PartialEffectiveContract,
]:
    compiled = _public_ocr_compilation()
    return compiled, _structural_partial_contract(compiled)


def _population_projection(
    bundle: Bundle,
    *,
    source_id: str,
    source_locator: str,
    bundle_pointer: str,
) -> tuple[dict[str, list[dict[str, object]]], list[dict[str, object]]]:
    records: dict[str, list[dict[str, object]]] = {
        "entities": [],
        "events": [],
    }
    derivations: list[dict[str, object]] = []
    families = {"entity": "entities", "event": "events"}
    for attribute, type_name, family in PLANES:
        if attribute == "bundle":
            values = (bundle,)
            pointers = (bundle_pointer,)
        elif attribute == "source_class":
            values = (bundle.source_class,)
            pointers = (f"{bundle_pointer}/source_class",)
        else:
            values = getattr(bundle, attribute)
            pointers = tuple(
                f"{bundle_pointer}/{attribute}/{index}"
                for index in range(len(values))
            )
        for value, pointer in zip(values, pointers, strict=True):
            flat = value.record()
            record_id = flat["id"]
            properties = {key: item for key, item in flat.items() if key != "id"}
            records[families[family]].append(
                {"id": record_id, "properties": properties, "type": type_name}
            )
            derivations.extend(
                {
                    "locator": f"{source_locator}#{pointer}/{key}",
                    "path": ["properties", key],
                    "record_id": record_id,
                    "source_id": source_id,
                }
                for key in properties
            )
    return records, derivations


def _population_plan(
    *,
    bundle: Bundle,
    bundle_pointer: str,
    bundle_source: bytes,
    bundle_source_id: str,
    bundle_source_locator: str,
    evidence: tuple[tuple[str, bytes], ...],
    partial_contract: compiler.PartialEffectiveContract,
    plan_id: str,
) -> dict[str, object]:
    records, derivations = _population_projection(
        bundle,
        source_id=bundle_source_id,
        source_locator=bundle_source_locator,
        bundle_pointer=bundle_pointer,
    )
    return {
        "adapter": {
            "adapter_id": "malleus.ocr.test-structural-projection",
            "version": "0",
        },
        "contract_identity": partial_contract.identity,
        "derivations": derivations,
        "evidence": [
            {"evidence_id": evidence_id, "sha256": _digest(payload)}
            for evidence_id, payload in evidence
        ],
        "gaps": [],
        "grammar": "malleus.population-plan/private-v0",
        "history_profile": {
            "profile_id": "ocr-domain-history-not-selected",
            "sha256": "sha256:" + "0" * 64,
        },
        "plan_id": plan_id,
        "records": records,
        "sources": [
            {"source_id": bundle_source_id, "sha256": _digest(bundle_source)}
        ],
        "supersessions": [],
        "valid_time": {"kind": "ORDER_ONLY", "value": plan_id},
    }


def _case_paths(case: dict[str, Any]) -> Iterator[str]:
    for key in ("source", "oracle", "bundle", "verification"):
        yield case[key]
    for raster in case["rasters"]:
        yield raster["path"]
    for key in ("requests", "responses", "selected_texts"):
        yield from case[key]
    for mutation in case["mutations"]:
        yield mutation["bundle"]
        yield mutation["verification"]


def _verification_payload(result: VerificationResult) -> dict[str, Any]:
    return {
        "bundle_id": result.bundle_id,
        "capability": result.capability,
        "conforms": result.conforms,
        "diagnostics": [
            {"code": item.code, "subject": item.subject, "detail": item.detail}
            for item in result.diagnostics
        ],
        "account": {
            "kind": result.account.kind,
            "complete": result.account.complete,
            "units": [
                {
                    "unit": item.unit,
                    "outcome": item.outcome,
                    "disposition": item.disposition,
                }
                for item in result.account.units
            ],
            "metrics": [
                {
                    "family": item.family,
                    "denominator": item.denominator,
                    "value": item.value,
                    "threshold": item.threshold,
                    "verdict": item.verdict,
                }
                for item in result.account.metrics
            ],
        },
    }


def _expected_payload(result: VerificationResult) -> dict[str, Any]:
    return {
        "capability": result.capability,
        "conforms": result.conforms,
        "complete": result.account.complete,
        "diagnostic_codes": sorted({item.code for item in result.diagnostics}),
        "units": {
            item.unit: {
                "outcome": item.outcome,
                "disposition": item.disposition,
            }
            for item in result.account.units
        },
        "metrics": {
            item.family: {
                "denominator": item.denominator,
                "value": item.value,
                "threshold": item.threshold,
                "verdict": item.verdict,
            }
            for item in result.account.metrics
        },
    }


def _png_dimensions(payload: bytes) -> tuple[int, int]:
    assert payload[:8] == b"\x89PNG\r\n\x1a\n"
    assert payload[12:16] == b"IHDR"
    assert len(payload) >= 24
    return struct.unpack(">II", payload[16:24])


def _image_pixels(payload: bytes) -> tuple[tuple[int, int], bytes]:
    with Image.open(BytesIO(payload)) as image:
        rgb = image.convert("RGB")
        return rgb.size, rgb.tobytes()


def _json_keys_and_strings(value: Any) -> Iterator[tuple[str, str]]:
    if isinstance(value, dict):
        for key, item in value.items():
            assert isinstance(key, str)
            yield "key", key
            yield from _json_keys_and_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _json_keys_and_strings(item)
    elif isinstance(value, str):
        yield "value", value


def test_manifest_is_closed_and_every_retained_file_is_listed_once() -> None:
    manifest = _manifest()
    assert set(manifest) == {
        "cases",
        "corpus_id",
        "corpus_version",
        "document_policy",
        "generated_by",
        "hash_algorithm",
        "ocr_profile_id",
        "ocr_profile_version",
        "reference_reader",
        "runtime_binding",
    }
    assert {case["id"] for case in manifest["cases"]} == {
        "failed-attempt",
        "region-control",
        "multipage-control",
        "incomplete-sequence",
    }

    listed = [path for case in manifest["cases"] for path in _case_paths(case)]
    assert len(listed) == len(set(listed)), "an artifact is listed more than once"
    retained = {
        path.relative_to(CORPUS).as_posix()
        for path in (CORPUS / "cases").rglob("*")
        if path.is_file()
    }
    assert set(listed) == retained

    checksums = _load(CHECKSUMS)
    assert checksums["algorithm"] == "sha256"
    assert checksums["scope"] == "every generated file except checksums.json"
    assert set(checksums["files"]) == retained | {"corpus.json"}

    every_file = {
        path.relative_to(CORPUS).as_posix()
        for path in CORPUS.rglob("*")
        if path.is_file()
    }
    interpreter_cache = {
        relative
        for relative in every_file
        if "__pycache__" in PurePosixPath(relative).parts and relative.endswith(".pyc")
    }
    assert every_file - interpreter_cache == set(checksums["files"]) | CONTROL_FILES


def test_checksum_inventory_binds_digest_and_byte_length() -> None:
    for relative, identity in _load(CHECKSUMS)["files"].items():
        assert set(identity) == {"sha256", "byte_length"}
        payload = _artifact_path(relative).read_bytes()
        assert identity == {
            "sha256": _digest(payload),
            "byte_length": len(payload),
        }


def test_manifest_binds_the_runtime_and_self_authored_source_policy() -> None:
    manifest = _manifest()
    assert manifest["corpus_id"] == "malleus.ocr.fixture_corpus"
    assert manifest["corpus_version"] == 1
    assert manifest["hash_algorithm"] == "sha256"
    assert manifest["ocr_profile_id"] == PROFILE_ID
    assert manifest["ocr_profile_version"] == PROFILE_VERSION
    assert manifest["generated_by"] == GENERATOR.relative_to(ROOT).as_posix()
    assert GENERATOR.is_file()
    assert manifest["document_policy"] == {
        "authorship": "self-authored deterministic controls",
        "contains_private_material": False,
        "contains_production_material": False,
        "network_required": False,
    }
    assert manifest["reference_reader"] == REFERENCE_READER

    runtime = manifest["runtime_binding"]
    assert set(runtime) == {
        "generator",
        "malleus_version",
        "ocr_ontology_path",
        "ocr_ontology_sha256",
        "ocr_registry_content_hash",
        "root_ontology_path",
        "root_ontology_sha256",
    }
    assert platform.python_implementation() == "CPython"
    assert sys.version_info >= (3, 10)
    assert runtime["generator"] == {
        "contract": "malleus.ocr.fixture_generator.v2",
        "pillow_version": PIL.__version__,
        "png_contract": "Pillow RGB PNG; optimize=false; compress_level=9; strict round-trip",
        "python_contract": "CPython>=3.10",
        "pypdf_version": pypdf.__version__,
        "reportlab_version": reportlab.Version,
        "zlib_contract": "RFC1950+RFC1951",
    }
    probe = b"malleus fixture generator zlib contract"
    assert zlib.decompress(zlib.compress(probe)) == probe
    png = BytesIO()
    Image.new("RGB", (2, 1), (17, 34, 51)).save(
        png, format="PNG", optimize=False, compress_level=9
    )
    assert _image_pixels(png.getvalue()) == ((2, 1), bytes((17, 34, 51)) * 2)
    assert runtime["malleus_version"] == malleus.__version__
    for path_key, digest_key in (
        ("ocr_ontology_path", "ocr_ontology_sha256"),
        ("root_ontology_path", "root_ontology_sha256"),
    ):
        payload = (ROOT / runtime[path_key]).read_bytes()
        assert runtime[digest_key] == _digest(payload)
    assert runtime["ocr_registry_content_hash"] == profile_registry().content_hash()


def test_deterministic_regeneration_matches_every_retained_byte() -> None:
    completed = subprocess.run(
        [sys.executable, str(GENERATOR), "check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert completed.stdout == "verified 52 deterministic corpus artifacts\n"


@pytest.mark.parametrize("case", _manifest()["cases"], ids=lambda case: case["id"])
def test_source_representation_matches_bytes_and_projects_to_core_without_loss(
    case: dict[str, Any],
) -> None:
    document = _load(_artifact_path(case["bundle"]))
    oracle = _load(_artifact_path(case["oracle"]))
    sources = document["bundle"]["sources"]
    assert len(sources) == 1
    source = sources[0]
    source_bytes = _artifact_path(case["source"]).read_bytes()
    locator = f"conformance/ocr/v0/corpus/{case['source']}"

    assert oracle["source"]["path"] == case["source"]
    assert oracle["source"]["origin"].startswith(
        "generated from self-authored literals"
    )
    assert oracle["source"]["license"] == "Apache-2.0"
    assert source == {
        "id": f"fixture:{case['id']}:source",
        "digest": _digest(source_bytes),
        "byte_length": len(source_bytes),
        "media_type": oracle["source"]["media_type"],
        "locator": locator,
    }
    assert oracle["source"]["digest"] == source["digest"]
    assert oracle["source"]["byte_length"] == source["byte_length"]

    projected = source_artifact_fields(
        artifact_id=source["id"],
        artifact_version=str(_manifest()["corpus_version"]),
        source_bytes=source_bytes,
        media_type=source["media_type"],
        locator=source["locator"],
    )
    assert {
        "digest": projected["source_content_digest"],
        "byte_length": projected["source_byte_length"],
        "media_type": projected["source_media_type"],
        "locator": projected["source_locator"],
    } == {
        key: source[key] for key in ("digest", "byte_length", "media_type", "locator")
    }
    assert projected["artifact_hash"].startswith("sha256:")
    assert len(projected["artifact_hash"]) == 71


@pytest.mark.parametrize("case", _manifest()["cases"], ids=lambda case: case["id"])
def test_retained_rasters_have_bound_digests_and_dimensions(
    case: dict[str, Any],
) -> None:
    bundle = _load(_artifact_path(case["bundle"]))["bundle"]
    bindings = RASTER_BINDINGS[case["id"]]
    assert len(case["rasters"]) == len(bundle["rasters"]) == len(bindings)
    source_id = f"fixture:{case['id']}:source"
    retained_payloads = []
    for manifest_raster, bundle_raster, (path, raster_id, unit) in zip(
        case["rasters"], bundle["rasters"], bindings, strict=True
    ):
        assert manifest_raster["path"] == path
        assert set(bundle_raster) == {
            "digest",
            "id",
            "render_contract",
            "source_id",
            "unit",
        }
        assert bundle_raster["id"] == raster_id
        assert bundle_raster["source_id"] == source_id
        assert bundle_raster["unit"] == unit
        payload = _artifact_path(path).read_bytes()
        retained_payloads.append(payload)
        assert bundle_raster["digest"] == _digest(payload)
        assert _png_dimensions(payload) == (
            manifest_raster["width"],
            manifest_raster["height"],
        )

    oracle_source = _load(_artifact_path(case["oracle"]))["source"]
    if oracle_source["media_type"] == "image/png":
        assert len(retained_payloads) == 1
        assert bundle["rasters"][0]["render_contract"] == "fixture-retained-raster:v1"
        assert retained_payloads[0] == _artifact_path(case["source"]).read_bytes()
        dimensions = oracle_source["pixel_dimensions"]
        assert _png_dimensions(_artifact_path(case["source"]).read_bytes()) == (
            dimensions["width"],
            dimensions["height"],
        )
    else:
        reader = PdfReader(_artifact_path(case["source"]))
        assert (
            len(reader.pages) == oracle_source["physical_page_count"] == len(bindings)
        )
        expected_size = oracle_source["physical_page_size_points"]
        runtime = _manifest()["runtime_binding"]["generator"]
        for page_number, (page, retained, raster) in enumerate(
            zip(reader.pages, retained_payloads, bundle["rasters"], strict=True),
            start=1,
        ):
            assert float(page.mediabox.width) == expected_size["width"]
            assert float(page.mediabox.height) == expected_size["height"]
            assert not (page.extract_text() or "").strip()
            page_images = list(page.images)
            assert len(page_images) == 1
            assert getattr(page_images[0], "is_displayed", None) is True
            assert page_images[0].image is not None
            assert _image_pixels(page_images[0].data) == _image_pixels(retained)
            xobjects = page["/Resources"]["/XObject"].get_object()
            image_objects = [
                (name, value.get_object())
                for name, value in xobjects.items()
                if value.get_object().get("/Subtype") == "/Image"
            ]
            assert len(image_objects) == 1
            name, image_object = image_objects[0]
            assert image_object.get("/ColorSpace") == "/DeviceRGB"
            assert raster["render_contract"] == (
                f"fixture-pdf-image-xobject:v1;page={page_number};image=0;"
                f"xobject={name.removeprefix('/')};extractor=pypdf-{runtime['pypdf_version']};"
                "source_colorspace=DeviceRGB;output_mode=RGB;"
                f"png=pillow-{runtime['pillow_version']}"
            )


@pytest.mark.parametrize("case", _manifest()["cases"], ids=lambda case: case["id"])
def test_retained_sidecars_bind_each_attempt_path(case: dict[str, Any]) -> None:
    bundle = _load(_artifact_path(case["bundle"]))["bundle"]
    oracle = _load(_artifact_path(case["oracle"]))
    regions = {item["id"]: item for item in bundle["regions"]}
    rasters = {item["id"]: item for item in bundle["rasters"]}
    hypotheses = {item["id"]: item for item in bundle["hypotheses"]}

    assert (
        oracle["reference_reader"]
        == _manifest()["reference_reader"]
        == REFERENCE_READER
    )
    assert {item["request"] for item in oracle["regions"]} == set(case["requests"])
    assert {item["response"] for item in oracle["regions"]} == set(case["responses"])
    assert {
        item["selected_text"]
        for item in oracle["regions"]
        if "selected_text" in item
    } == set(case["selected_texts"])

    for expected in oracle["regions"]:
        region = regions[expected["id"]]
        assert region["selector"] == expected["selector"]
        attempts = [
            item for item in bundle["attempts"] if item["region_id"] == region["id"]
        ]
        selections = [
            item for item in bundle["selections"] if item["region_id"] == region["id"]
        ]
        assert len(attempts) == 1
        attempt = attempts[0]
        assert attempt["status"] == expected["attempt_status"]

        request_bytes = _artifact_path(expected["request"]).read_bytes()
        response_bytes = _artifact_path(expected["response"]).read_bytes()
        assert attempt["request_digest"] == _digest(request_bytes)
        assert attempt["response_digest"] == _digest(response_bytes)

        request = json.loads(request_bytes)
        response = json.loads(response_bytes)
        assert set(request) == {
            "contract",
            "production_ocr",
            "raster_digest",
            "reader_id",
            "reader_kind",
            "region_id",
            "selector",
            "task",
        }
        assert request["region_id"] == response["region_id"] == region["id"]
        assert request["selector"] == region["selector"]
        assert request["raster_digest"] == rasters[region["raster_id"]]["digest"]
        for sidecar in (request, response):
            assert sidecar["reader_id"] == REFERENCE_READER["id"]
            assert sidecar["reader_kind"] == REFERENCE_READER["kind"]
            assert sidecar["production_ocr"] is REFERENCE_READER["production_ocr"]
        assert request["contract"] == "malleus.fixture.control_request.v1"
        assert attempt["config_identity"] == {
            "production_ocr": "false",
            "reader": REFERENCE_READER["id"],
            "reader_kind": REFERENCE_READER["kind"],
            "response_contract": response["contract"],
        }

        if attempt["status"] == "FAILED":
            assert set(expected) == {
                "attempt_status",
                "failure_class",
                "id",
                "request",
                "response",
                "selector",
                "unit",
            }
            assert set(response) == {
                "contract",
                "failure_class",
                "note",
                "outcome",
                "production_ocr",
                "reader_id",
                "reader_kind",
                "region_id",
                "retryable",
            }
            assert request["task"] == "return the fixed self-authored control failure"
            assert response["contract"] == "malleus.fixture.control_failure_response.v1"
            assert response["outcome"] == "FAILED"
            assert response["failure_class"] == expected["failure_class"]
            assert response["retryable"] is True
            assert attempt["unavailable_reason"] is None
            assert selections == []
            assert [
                item for item in bundle["hypotheses"] if item["region_id"] == region["id"]
            ] == []
            continue

        assert attempt["status"] == "COMPLETED"
        assert len(selections) == 1
        selection = selections[0]
        selected_bytes = _artifact_path(expected["selected_text"]).read_bytes()
        assert set(response) == {
            "contract",
            "note",
            "outcome",
            "production_ocr",
            "reader_id",
            "reader_kind",
            "region_id",
            "text",
        }
        assert request["task"] == "return the fixed self-authored control reading"
        assert response["contract"] == "malleus.fixture.control_response.v1"
        assert (
            response["note"]
            == "Retained fixture response. No recognition engine was invoked."
        )
        assert response["outcome"] == ("BLANK" if response["text"] == "" else "READING")

        machine = [
            item for item in bundle["hypotheses"] if item["attempt_id"] == attempt["id"]
        ]
        assert len(machine) == 1
        assert machine[0]["text_digest"] == _digest(response["text"].encode("utf-8"))
        assert hypotheses[selection["selected_id"]]["text_digest"] == _digest(
            selected_bytes
        )
        assert selected_bytes.decode("utf-8") == expected["expected_text"]

        assert expected["response_text"] == response["text"]
        reviewed = "human_verdict" in expected
        assert selection["human_verified"] is reviewed
        corrections = [
            item
            for item in bundle["corrections"]
            if item["reviewed_hypothesis_id"] == machine[0]["id"]
        ]
        if reviewed:
            assert expected["response_text"] == response["text"]
            assert len(corrections) == 1
            correction = corrections[0]
            assert correction["verdict"] == expected["human_verdict"]
            if correction["verdict"] == "CORRECTED":
                selected = hypotheses[selection["selected_id"]]
                assert selected["correction_id"] == correction["id"]
                assert correction["corrected_text_digest"] == selected["text_digest"]
            else:
                assert correction["verdict"] == "VERIFIED_BLANK"
                assert correction["corrected_text_digest"] is None
                assert selection["selected_id"] == machine[0]["id"]
        else:
            assert corrections == []


def test_multipage_oracle_selects_the_body_without_the_visible_heading() -> None:
    case = next(
        item for item in _manifest()["cases"] if item["id"] == "multipage-control"
    )
    oracle = _load(_artifact_path(case["oracle"]))
    body, blank = oracle["regions"]

    assert body["selector"] == {
        "type": "FragmentSelector",
        "value": "xywh=140,650,720,410",
    }
    assert body["expected_text"] == "The quick brown fox jumps.\nAMBIGUOUS TOKEN\nO0I1l"
    assert body["response_text"] == "The quick brown fox jumps.\nAMBIGUOUS TOKEN\nOOI1l"
    assert blank["selector"] == {
        "type": "FragmentSelector",
        "value": "xywh=0,0,1000,1400",
    }
    assert blank["expected_text"] == blank["response_text"] == ""


def test_failed_attempt_retains_the_failure_without_inventing_a_reading() -> None:
    case = next(item for item in _manifest()["cases"] if item["id"] == "failed-attempt")
    bundle_bytes = _artifact_path(case["bundle"]).read_bytes()
    bundle = Bundle.from_bytes(bundle_bytes)
    oracle = _load(_artifact_path(case["oracle"]))

    assert case["purpose"] == oracle["purpose"] == (
        "Retain a made-but-failed control-reader attempt without inventing a reading."
    )
    assert case["selected_texts"] == []
    assert case["mutations"] == []
    assert len(bundle.rasters) == len(bundle.regions) == len(bundle.attempts) == 1
    assert bundle.hypotheses == bundle.corrections == bundle.selections == ()

    attempt = bundle.attempts[0]
    assert attempt.status == "FAILED"
    assert attempt.unavailable_reason is None
    response_path = _artifact_path(case["responses"][0])
    assert attempt.response_digest == _digest(response_path.read_bytes())
    assert _load(response_path) == {
        "contract": "malleus.fixture.control_failure_response.v1",
        "failure_class": "FIXTURE_CONTROL_FAILURE",
        "note": (
            "The deterministic fixture reader returned this controlled failure. "
            "No OCR engine or provider was invoked."
        ),
        "outcome": "FAILED",
        "production_ocr": False,
        "reader_id": REFERENCE_READER["id"],
        "reader_kind": REFERENCE_READER["kind"],
        "region_id": bundle.regions[0].id,
        "retryable": True,
    }

    result = verify_bundle(bundle)
    assert result.conforms
    assert not result.account.complete
    assert _expected_payload(result) == oracle["expected_verification"] == {
        "capability": "AUDIT_ONLY",
        "complete": False,
        "conforms": True,
        "diagnostic_codes": [],
        "metrics": {
            "coverage": {
                "denominator": "declared_units",
                "threshold": 1.0,
                "value": 0.0,
                "verdict": "UNMET",
            }
        },
        "units": {
            "image:1": {"disposition": "CHECK_FAILED", "outcome": "FAILED"}
        },
    }


def test_failed_attempt_cli_names_the_retry_queue_not_the_fetch_queue(capsys) -> None:
    from malleus.ocr.cli import REFUSED, main

    case = next(item for item in _manifest()["cases"] if item["id"] == "failed-attempt")
    code = main([str(_artifact_path(case["bundle"]))])
    output = capsys.readouterr().out

    assert code == REFUSED
    assert "INCOMPLETE" in output
    assert "never checked: none" in output
    assert "check failed:  image:1" in output


def test_corpus_contains_no_local_paths_credentials_or_private_metadata() -> None:
    for relative in _load(CHECKSUMS)["files"]:
        path = _artifact_path(relative)
        if path.suffix == ".json":
            for kind, text in _json_keys_and_strings(_load(path)):
                assert not LOCAL_PATH.search(text), (
                    f"local path in {relative}: {text!r}"
                )
                if kind == "key":
                    normalized = re.sub(r"[^a-z0-9]", "", text.casefold())
                    assert normalized not in CREDENTIAL_KEY_FORMS, (
                        f"credential-bearing key in {relative}: {text!r}"
                    )
        elif path.suffix == ".txt":
            text = path.read_text(encoding="utf-8")
            assert not LOCAL_PATH.search(text), f"local path in {relative}: {text!r}"

    for case in _manifest()["cases"]:
        source = _artifact_path(case["source"])
        pngs = [_artifact_path(item["path"]) for item in case["rasters"]]
        if source.suffix == ".png":
            pngs.append(source)
        for png in pngs:
            with Image.open(png) as image:
                assert image.info == {}, f"PNG metadata retained in {png}"
                assert len(image.getexif()) == 0, f"PNG EXIF retained in {png}"

        if source.suffix == ".pdf":
            reader = PdfReader(source)
            assert dict(reader.metadata or {}) == {
                **PDF_METADATA,
                "/Title": PDF_TITLES[case["id"]],
            }
            catalog = reader.trailer["/Root"]
            for forbidden in ("/AA", "/AcroForm", "/Metadata", "/Names", "/OpenAction"):
                assert forbidden not in catalog, (
                    f"private or active PDF metadata in {source}"
                )


def test_incomplete_sequence_is_exactly_a_two_page_source_sequence_gap() -> None:
    case = next(
        item for item in _manifest()["cases"] if item["id"] == "incomplete-sequence"
    )
    oracle = _load(_artifact_path(case["oracle"]))
    bundle = _load(_artifact_path(case["bundle"]))["bundle"]

    assert (
        case["purpose"]
        == oracle["purpose"]
        == (
            "Source declares logical pages 1 and 3 against required 1, 2, and 3; "
            "this is a source-sequence gap, not OCR skipping a present physical page."
        )
    )
    assert oracle["fixture_kind"] == "two_physical_pages_three_logical_units"
    assert oracle["source"]["physical_page_count"] == 2
    assert oracle["source"]["logical_page_labels"] == ["1 of 3", "3 of 3"]
    assert oracle["missing_logical_units"] == ["page:2"]
    assert bundle["source_class"]["required_units"] == ["page:1", "page:2", "page:3"]
    assert bundle["observed_units"] == ["page:1", "page:3"]
    assert [item["unit"] for item in bundle["rasters"]] == ["page:1", "page:3"]
    assert oracle["expected_verification"] == {
        "capability": "AUDIT_ONLY",
        "complete": False,
        "conforms": True,
        "diagnostic_codes": [],
        "metrics": {
            "coverage": {
                "denominator": "declared_units",
                "threshold": 1.0,
                "value": 2 / 3,
                "verdict": "UNMET",
            }
        },
        "units": {
            "page:1": {"disposition": "ACCOUNTED", "outcome": "READ"},
            "page:2": {"disposition": "NOT_CHECKED", "outcome": "NOT_OBSERVED"},
            "page:3": {"disposition": "ACCOUNTED", "outcome": "READ"},
        },
    }


@pytest.mark.parametrize("case", _manifest()["cases"], ids=lambda case: case["id"])
def test_required_units_agree_with_oracle_and_are_not_invented_by_regions(
    case: dict[str, Any],
) -> None:
    bundle = _load(_artifact_path(case["bundle"]))["bundle"]
    oracle = _load(_artifact_path(case["oracle"]))
    assert oracle["case_id"] == case["id"]
    assert oracle["purpose"] == case["purpose"]
    required = bundle["source_class"]["required_units"]
    assert len(required) == len(set(required))
    assert set(required) == set(oracle["expected_verification"]["units"])
    assert set(bundle["observed_units"]) <= set(required)
    assert {region["unit"] for region in oracle["regions"]} <= set(required)


@pytest.mark.parametrize("case", _manifest()["cases"], ids=lambda case: case["id"])
def test_reference_bundle_recomputes_to_frozen_verification_and_oracle(
    case: dict[str, Any],
) -> None:
    document = _load(_artifact_path(case["bundle"]))
    result = verify_bundle(Bundle.from_document(document))
    assert _verification_payload(result) == _load(_artifact_path(case["verification"]))
    oracle = _load(_artifact_path(case["oracle"]))
    assert _expected_payload(result) == oracle["expected_verification"]


def test_mutations_recompute_to_declared_current_outcomes() -> None:
    manifest = _manifest()
    declared: dict[str, dict[str, tuple[tuple[str, ...], dict[str, str]]]] = {}
    for case in manifest["cases"]:
        oracle = _load(_artifact_path(case["oracle"]))
        assert oracle["mutations"] == case["mutations"]
        declared[case["id"]] = {}
        for mutation in case["mutations"]:
            result = verify_bundle(
                Bundle.from_document(_load(_artifact_path(mutation["bundle"])))
            )
            label = f"{case['id']}/{mutation['id']}"
            assert _verification_payload(result) == _load(
                _artifact_path(mutation["verification"])
            ), label
            codes = tuple(sorted({item.code for item in result.diagnostics}))
            assert codes == tuple(mutation["expected_diagnostic_codes"]), label
            outcomes = {item.unit: item.outcome for item in result.account.units}
            expected_outcomes = mutation.get("expected_unit_outcome", {})
            assert all(
                outcomes[unit] == value for unit, value in expected_outcomes.items()
            ), label
            declared[case["id"]][mutation["id"]] = (codes, expected_outcomes)
    assert declared == IMPLEMENTED_MUTATIONS


def test_public_compiler_structurally_compiles_registration_without_claiming_a_reading(
    public_ocr_contract: tuple[
        compiler.ValidatedContractCompilation,
        compiler.PartialEffectiveContract,
    ],
) -> None:
    compiled, partial = public_ocr_contract
    case = _load(REGISTRATION_CASE)
    bundle = Bundle.from_document(case["document"])
    verification = verify_bundle(bundle)
    plan_id = "plan:ocr-fixture:registration-only"
    plan = _population_plan(
        bundle=bundle,
        bundle_pointer="/document/bundle",
        bundle_source=REGISTRATION_CASE.read_bytes(),
        bundle_source_id="source:ocr-fixture:registration-case",
        bundle_source_locator=REGISTRATION_CASE.relative_to(ROOT).as_posix(),
        evidence=(),
        partial_contract=partial,
        plan_id=plan_id,
    )

    assert isinstance(compiled.view, compiler.ContractView)
    assert verification.capability == "AUDIT_ONLY"
    assert verification.conforms
    assert not verification.account.complete
    assert bundle.kind == "REGISTRATION"
    assert plan["history_profile"] == {
        "profile_id": "ocr-domain-history-not-selected",
        "sha256": "sha256:" + "0" * 64,
    }
    assert plan["records"]["events"] == []

    population = compiler.compile_population_plan(
        plan,
        partial_contract=partial,
        contract_view=compiled.view,
        base_state=compiler.PopulationBaseState.empty(),
    )

    assert isinstance(population, compiler.PopulationPlanCompilation)
    assert population.status is compiler.PopulationPlanStatus.CHANGE_SET
    assert population.source_record_ids == ("source:ocr-fixture:registration-case",)
    assert population.evidence_record_ids == (
        "profile:ocr-domain-history-not-selected",
        plan_id,
    )
    assert tuple(operation.operation_type for operation in population.operations) == (
        "CREATE_ENTITY",
        "CREATE_ENTITY",
        "CREATE_ENTITY",
    )
    assert tuple(operation.record_type for operation in population.operations) == (
        "SourceClass",
        "SourceRepresentation",
        "EvidenceBundle",
    )


@pytest.mark.parametrize("case", _manifest()["cases"], ids=lambda case: case["id"])
def test_public_compiler_refuses_finished_ocr_event_population(
    case: dict[str, Any],
    public_ocr_contract: tuple[
        compiler.ValidatedContractCompilation,
        compiler.PartialEffectiveContract,
    ],
) -> None:
    compiled, partial = public_ocr_contract
    bundle_path = _artifact_path(case["bundle"])
    bundle = Bundle.from_document(_load(bundle_path))
    verification = verify_bundle(bundle)
    source_path = _artifact_path(case["source"])
    plan = _population_plan(
        bundle=bundle,
        bundle_pointer="/bundle",
        bundle_source=bundle_path.read_bytes(),
        bundle_source_id=f"source:ocr-fixture:{case['id']}:bundle",
        bundle_source_locator=bundle_path.relative_to(ROOT).as_posix(),
        evidence=((f"evidence:ocr-fixture:{case['id']}:document", source_path.read_bytes()),),
        partial_contract=partial,
        plan_id=f"plan:ocr-fixture:{case['id']}",
    )

    assert verification.capability == "AUDIT_ONLY"
    assert verification.conforms
    assert bundle.kind == "FINISHED_READING"
    assert bundle.attempts
    assert len(plan["records"]["events"]) == len(bundle.attempts) + len(
        bundle.corrections
    )

    with pytest.raises(compiler.PopulationPlanRefusal) as refusal:
        compiler.compile_population_plan(
            plan,
            partial_contract=partial,
            contract_view=compiled.view,
            base_state=compiler.PopulationBaseState.empty(),
        )

    assert (
        refusal.value.reason
        is compiler.PopulationPlanRefusalReason.FAMILY_NOT_ADMITTED
    )
    assert refusal.value.detail == "events cannot be admitted by the governed path"
