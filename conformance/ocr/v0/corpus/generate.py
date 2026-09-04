#!/usr/bin/env python3
"""Generate the self-authored OCR fixture corpus deterministically."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
import sys
import zlib
from dataclasses import asdict
from io import BytesIO
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import PIL
import pypdf
import reportlab
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[4]
CORPUS_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from malleus import __version__  # noqa: E402
from malleus.ocr.bundle import (  # noqa: E402
    DOCUMENT_VERSION,
    PROFILE_ID,
    PROFILE_VERSION,
    Bundle,
)
from malleus.ocr.verify import (  # noqa: E402
    VerificationResult,
    profile_registry,
    verify_bundle,
)

FIXED_TIME = "2026-09-02T00:00:00+00:00"
SOURCE_ORIGIN = "generated from self-authored literals in conformance/ocr/v0/corpus/generate.py"
SOURCE_LICENSE = "Apache-2.0"
PILLOW_VERSION = "12.3.0"
REPORTLAB_VERSION = "4.4.9"
PYPDF_VERSION = "6.16.2"
PYTHON_CONTRACT = "CPython>=3.10"
ZLIB_CONTRACT = "RFC1950+RFC1951"
PNG_CONTRACT = "Pillow RGB PNG; optimize=false; compress_level=9; strict round-trip"
GENERATOR_CONTRACT = "malleus.ocr.fixture_generator.v2"
READER = {
    "id": "malleus.fixture.control_reader@1",
    "kind": "deterministic_control_reader",
    "production_ocr": False,
    "description": "Fixed readings for self-authored fixtures. No recognition engine is invoked.",
}
CONFIG_IDENTITY = {
    "reader": READER["id"],
    "reader_kind": READER["kind"],
    "production_ocr": "false",
    "response_contract": "malleus.fixture.control_response.v1",
}
CONTROL_FILES = frozenset({"README.md", "generate.py"})


class CorpusError(RuntimeError):
    """The fixture declaration or retained corpus is inconsistent."""


def _relative_path(raw: str) -> str:
    """Return one normalized corpus-relative POSIX path or refuse it."""
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise CorpusError(f"artifact path must be a nonblank POSIX string: {raw!r}")
    path = PurePosixPath(raw)
    if (
        path.is_absolute()
        or path.as_posix() != raw
        or not path.parts
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise CorpusError(f"artifact path must be normalized and relative: {raw!r}")
    return raw


def _target(root: Path, relative: str) -> Path:
    """Resolve a managed path without permitting traversal or symlink writes."""
    relative = _relative_path(relative)
    if relative in CONTROL_FILES:
        raise CorpusError(f"control file is not a generated artifact: {relative}")
    root = root.resolve()
    target = root.joinpath(*PurePosixPath(relative).parts)
    cursor = target
    while cursor != root:
        if cursor.is_symlink():
            raise CorpusError(f"managed artifact path is a symlink: {relative}")
        cursor = cursor.parent
    if not target.resolve(strict=False).is_relative_to(root):
        raise CorpusError(f"managed artifact escapes corpus root: {relative}")
    return target


def _json_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(value, allow_nan=False, indent=2, sort_keys=True)
    except (TypeError, ValueError) as error:
        raise CorpusError(f"fixture value is not strict JSON: {error}") from error
    return (text + "\n").encode("utf-8")


def _digest(payload: bytes) -> str:
    if not isinstance(payload, bytes):
        raise CorpusError(f"digest input must be bytes, got {type(payload).__name__}")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


class Artifacts:
    """Closed in-memory artifact set with path and byte collision checks."""

    def __init__(self) -> None:
        self.files: dict[str, bytes] = {}

    def add(self, path: str, payload: bytes) -> bytes:
        path = _relative_path(path)
        if not isinstance(payload, bytes):
            raise CorpusError(f"artifact {path} must be bytes, got {type(payload).__name__}")
        if path in self.files:
            raise CorpusError(f"artifact declared twice: {path}")
        self.files[path] = payload
        return payload

    def add_json(self, path: str, value: Any) -> bytes:
        return self.add(path, _json_bytes(value))

    def add_text(self, path: str, value: str) -> bytes:
        if not isinstance(value, str):
            raise CorpusError(f"text artifact {path} must be a string")
        return self.add(path, value.encode("utf-8"))


def _assert_generator_runtime() -> None:
    observed = {
        "python": platform.python_implementation(),
        "pillow": PIL.__version__,
        "pypdf": pypdf.__version__,
        "reportlab": reportlab.Version,
    }
    expected = {
        "python": "CPython",
        "pillow": PILLOW_VERSION,
        "pypdf": PYPDF_VERSION,
        "reportlab": REPORTLAB_VERSION,
    }
    zlib_probe = b"malleus fixture generator zlib contract"
    if observed != expected or sys.version_info < (3, 10):
        raise CorpusError(
            f"generator runtime differs from {PYTHON_CONTRACT}, Pillow {PILLOW_VERSION}, "
            f"pypdf {PYPDF_VERSION}, ReportLab {REPORTLAB_VERSION}: {observed}"
        )
    if zlib.decompress(zlib.compress(zlib_probe)) != zlib_probe:
        raise CorpusError(f"generator runtime does not satisfy {ZLIB_CONTRACT}")
    png = _png_bytes(Image.new("RGB", (2, 1), (17, 34, 51)))
    with Image.open(BytesIO(png)) as image:
        image.load()
        if image.mode != "RGB" or image.size != (2, 1) or image.getpixel((0, 0)) != (17, 34, 51):
            raise CorpusError(f"generator runtime does not satisfy {PNG_CONTRACT}")


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return ImageFont.load_default(size=size)


def _centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    *,
    fill: str = "#152238",
    spacing: int = 18,
) -> None:
    left, top, right, bottom = box
    bounds = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align="center")
    width, height = bounds[2] - bounds[0], bounds[3] - bounds[1]
    point = (left + (right - left - width) / 2, top + (bottom - top - height) / 2)
    draw.multiline_text(point, text, font=font, fill=fill, spacing=spacing, align="center")


def _png_bytes(image: Image.Image) -> bytes:
    output = BytesIO()
    image.save(output, format="PNG", optimize=False, compress_level=9)
    return output.getvalue()


def _region_control_png() -> bytes:
    image = Image.new("RGB", (1200, 800), "#f7f5ef")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1200, 112), fill="#152238")
    _centered_text(
        draw, (0, 0, 1200, 112), "MALLEUS OCR FIXTURE | REGION CONTROL", _font(42),
        fill="#ffffff",
    )
    boxes = (
        ((80, 180, 580, 600), "REGION A\nALPHA 123\nLEFT BOX", "#dcecff"),
        ((620, 180, 1120, 600), "REGION B\nBRAVO 789\nRIGHT BOX", "#e8f4de"),
    )
    for box, text, fill in boxes:
        draw.rounded_rectangle(box, radius=24, fill=fill, outline="#152238", width=6)
        _centered_text(draw, box, text, _font(54))
    _centered_text(
        draw, (80, 650, 1120, 750), "The boxes are separate evidence regions.",
        _font(30), fill="#39465b",
    )
    return _png_bytes(image)


def _attempt_control_png(kind: str, target: str, footer: str, fill: str) -> bytes:
    image = Image.new("RGB", (1000, 700), "#f7f5ef")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1000, 112), fill="#152238")
    _centered_text(
        draw, (0, 0, 1000, 112), f"MALLEUS OCR FIXTURE | {kind}", _font(38),
        fill="#ffffff",
    )
    box = (100, 180, 900, 570)
    draw.rounded_rectangle(box, radius=24, fill=fill, outline="#152238", width=6)
    _centered_text(draw, box, target, _font(48))
    _centered_text(
        draw,
        (100, 610, 900, 675),
        footer,
        _font(26),
        fill="#39465b",
    )
    return _png_bytes(image)


def _failed_attempt_png() -> bytes:
    return _attempt_control_png(
        "FAILED ATTEMPT",
        "CONTROL TARGET\nTHIS REGION WILL NOT BE READ",
        "The failed call remains evidence, not a reading.",
        "#f8e1dd",
    )


def _unavailable_attempt_png() -> bytes:
    return _attempt_control_png(
        "UNAVAILABLE ATTEMPT",
        "CONTROL TARGET\nTHE CALL WILL NOT START",
        "No response is evidence that no call was made.",
        "#fff1cc",
    )


def _document_page(
    logical_page: str,
    heading: str,
    body: str,
    *,
    blank: bool = False,
) -> bytes:
    image = Image.new("RGB", (1000, 1400), "#ffffff")
    if blank:
        return _png_bytes(image)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1000, 132), fill="#152238")
    _centered_text(draw, (0, 0, 1000, 132), "MALLEUS OCR FIXTURE", _font(46), fill="#ffffff")
    _centered_text(draw, (80, 180, 920, 290), logical_page, _font(42))
    draw.rounded_rectangle(
        (100, 350, 900, 1160), radius=24, fill="#f7f5ef", outline="#152238", width=5
    )
    _centered_text(draw, (140, 400, 860, 620), heading, _font(48))
    _centered_text(draw, (140, 650, 860, 1060), body, _font(40), spacing=24)
    _centered_text(
        draw, (100, 1230, 900, 1320), "SELF-AUTHORED CONTROL DOCUMENT", _font(28),
        fill="#546176",
    )
    return _png_bytes(image)


def _raster_pdf(title: str, pages: tuple[bytes, ...]) -> tuple[bytes, tuple[dict[str, Any], ...]]:
    if not pages:
        raise CorpusError(f"{title}: a raster-only PDF needs at least one page")
    output = BytesIO()
    canvas = Canvas(output, pagesize=(500, 700), pageCompression=1, invariant=1)
    canvas.setAuthor("Malleus self-authored fixture corpus")
    canvas.setCreator("conformance/ocr/v0/corpus/generate.py")
    canvas.setSubject("Deterministic raster-only OCR control document")
    canvas.setTitle(title)
    for page in pages:
        canvas.drawImage(ImageReader(BytesIO(page)), 0, 0, width=500, height=700)
        canvas.showPage()
    canvas.save()
    payload = output.getvalue()
    rasters = _pdf_rasters(title, payload)
    if len(rasters) != len(pages):
        raise CorpusError(f"{title}: expected {len(pages)} pages, found {len(rasters)}")
    return payload, rasters


def _pdf_rasters(title: str, payload: bytes) -> tuple[dict[str, Any], ...]:
    """Extract each retained raster from the exact final source PDF bytes."""
    reader = PdfReader(BytesIO(payload))
    if reader.is_encrypted:
        raise CorpusError(f"{title}: generated PDF is unexpectedly encrypted")
    rasters = []
    for page_number, page in enumerate(reader.pages, start=1):
        if (page.extract_text() or "").strip():
            raise CorpusError(f"{title}: page {page_number} contains a text layer")
        resources = page.get("/Resources")
        xobjects = resources.get_object().get("/XObject") if resources else None
        if xobjects is None:
            raise CorpusError(f"{title}: page {page_number} has no image XObject")
        xobjects = xobjects.get_object()
        image_objects = [
            (name, value.get_object())
            for name, value in xobjects.items()
            if value.get_object().get("/Subtype") == "/Image"
        ]
        if len(image_objects) != 1 or len(page.images) != 1:
            raise CorpusError(
                f"PDF page {page_number} must carry exactly one image XObject, found "
                f"{len(image_objects)} objects and {len(page.images)} extractable images"
            )
        xobject_name, xobject = image_objects[0]
        extracted = page.images[xobject_name]
        if getattr(extracted, "is_displayed", None) is not True or extracted.image is None:
            raise CorpusError(
                f"PDF page {page_number} extractor lacks displayed image metadata; "
                f"pypdf {PYPDF_VERSION} is required"
            )
        image = extracted.image
        image.load()
        expected_size = (xobject.get("/Width"), xobject.get("/Height"))
        if image.size != expected_size:
            raise CorpusError(
                f"PDF page {page_number} decoded size {image.size} differs from {expected_size}"
            )
        source_mode = image.mode
        colorspace = xobject.get("/ColorSpace")
        if source_mode != "RGB" or colorspace != "/DeviceRGB":
            raise CorpusError(
                f"PDF page {page_number} must extract as DeviceRGB/RGB, got "
                f"{colorspace}/{source_mode}"
            )
        raster = _png_bytes(image.copy())
        rasters.append({
            "payload": raster,
            "width": image.width,
            "height": image.height,
            "render_contract": (
                f"fixture-pdf-image-xobject:v1;page={page_number};image=0;"
                f"xobject={xobject_name.removeprefix('/')};extractor=pypdf-{PYPDF_VERSION};"
                f"source_colorspace=DeviceRGB;output_mode=RGB;png=pillow-{PIL.__version__}"
            ),
        })
    return tuple(rasters)


def _id(case_id: str, *parts: str) -> str:
    values = (case_id, *parts)
    if any(not isinstance(value, str) or not value or ":" in value for value in values):
        raise CorpusError(f"fixture identity components must be nonblank colon-free strings: {values!r}")
    return "fixture:" + ":".join(values)


def _closed_merge(
    base: Mapping[str, Any], extra: Mapping[str, Any] | None, label: str
) -> dict[str, Any]:
    overlap = set(base) & set(extra or {})
    if overlap:
        raise CorpusError(f"{label}: extra fields replace fixed fields: {sorted(overlap)}")
    return {**base, **(extra or {})}


def _document(bundle: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "profile": PROFILE_ID,
        "profile_version": PROFILE_VERSION,
        "document_version": DOCUMENT_VERSION,
        "bundle": bundle,
    }


def _bundle_base(case_id: str, required: list[str], observed: list[str]) -> dict[str, Any]:
    return {
        "id": _id(case_id, "bundle"),
        "source_class": {
            "id": _id(case_id, "source-class"),
            "required_units": required,
            "metric_families": {
                "coverage": {"denominator": "declared_units", "threshold": 1.0}
            },
            "temporal_policy": "self_authored_fixture_has_no_source_time_claim",
            "frozen_at": FIXED_TIME,
            "inventory_basis": "fixture_declared_before_reading",
        },
        "kind": "FINISHED_READING",
        "sources": [],
        "rasters": [],
        "regions": [],
        "attempts": [],
        "hypotheses": [],
        "corrections": [],
        "selections": [],
        "observed_units": observed,
        "data_handling_policy_id": "policy:fixture:local-self-authored",
        "hostile_content_policy_id": "policy:fixture:text-is-untrusted-data",
        "transport_metadata": {
            "fixture_corpus": "malleus.ocr.fixture_corpus.v1",
            "network_access": False,
        },
    }


def _verification_payload(result: VerificationResult) -> dict[str, Any]:
    payload = asdict(result)
    payload["conforms"] = result.conforms
    payload["account"]["complete"] = result.account.complete
    return payload


def _expected(
    units: Mapping[str, tuple[str, str]], *, complete: bool = True,
    metric_value: float = 1.0, metric_verdict: str = "MET",
    diagnostic_codes: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "capability": "AUDIT_ONLY",
        "conforms": not diagnostic_codes,
        "complete": complete,
        "diagnostic_codes": list(diagnostic_codes),
        "units": {
            unit: {"outcome": outcome, "disposition": disposition}
            for unit, (outcome, disposition) in units.items()
        },
        "metrics": {"coverage": {
            "denominator": "declared_units", "value": metric_value,
            "threshold": 1.0, "verdict": metric_verdict,
        }},
    }


def _refusal(expected: Mapping[str, Any], *codes: str) -> dict[str, Any]:
    refused = copy.deepcopy(expected)
    refused["conforms"] = False
    refused["diagnostic_codes"] = list(codes)
    return refused


def _verify(
    document: Mapping[str, Any],
    expected: Mapping[str, Any],
    label: str,
    expected_diagnostics: tuple[tuple[str, str], ...] = (),
) -> dict[str, Any]:
    result = verify_bundle(Bundle.from_document(document))
    payload = _verification_payload(result)
    observed_diagnostics = sorted((item.code, item.subject) for item in result.diagnostics)
    if observed_diagnostics != sorted(expected_diagnostics):
        raise CorpusError(
            f"{label}: diagnostic identities disagree; "
            f"expected={sorted(expected_diagnostics)!r}; observed={observed_diagnostics!r}"
        )
    expected_codes = sorted({code for code, _subject in expected_diagnostics})
    if sorted(expected["diagnostic_codes"]) != expected_codes:
        raise CorpusError(f"{label}: diagnostic code and identity oracles disagree")
    account = payload["account"]
    observed = {
        "capability": payload["capability"],
        "conforms": payload["conforms"],
        "complete": account["complete"],
        "diagnostic_codes": expected_codes,
        "units": {
            item["unit"]: {key: item[key] for key in ("outcome", "disposition")}
            for item in account["units"]
        },
        "metrics": {
            item["family"]: {
                key: item[key] for key in ("denominator", "value", "threshold", "verdict")
            }
            for item in account["metrics"]
        },
    }
    if observed != expected:
        raise CorpusError(
            f"{label}: verifier disagrees with oracle\n"
            f"expected={json.dumps(expected, sort_keys=True)}\n"
            f"observed={json.dumps(observed, sort_keys=True)}"
        )
    return payload


def _write_verified_document(
    artifacts: Artifacts,
    *,
    bundle_path: str,
    verification_path: str,
    document: Mapping[str, Any],
    expected: Mapping[str, Any],
    label: str,
    expected_diagnostics: tuple[tuple[str, str], ...] = (),
) -> dict[str, Any]:
    document_bytes = artifacts.add_json(bundle_path, document)
    serialized = json.loads(document_bytes.decode("utf-8"))
    verification = _verify(serialized, expected, label, expected_diagnostics)
    artifacts.add_json(verification_path, verification)
    return serialized


class Case:
    """One fixture case assembled from explicit raster and reading declarations."""

    def __init__(
        self, artifacts: Artifacts, *, case_id: str, purpose: str, source_name: str,
        source: bytes, media_type: str, required_units: list[str],
        observed_units: list[str], source_details: Mapping[str, Any],
    ) -> None:
        self.artifacts, self.id, self.purpose = artifacts, case_id, purpose
        self.prefix = f"cases/{case_id}"
        self.source_path = f"{self.prefix}/source/{source_name}"
        self.bundle = _bundle_base(case_id, required_units, observed_units)
        self.raster_manifest: list[dict[str, Any]] = []
        self.exchanges: list[dict[str, Any]] = []
        self.oracle_regions: list[dict[str, Any]] = []
        self.readings: dict[str, dict[str, Any]] = {}
        artifacts.add(self.source_path, source)
        self.bundle["sources"] = [{
            "id": _id(case_id, "source"), "digest": _digest(source),
            "byte_length": len(source), "media_type": media_type,
            "locator": f"conformance/ocr/v0/corpus/{self.source_path}",
        }]
        common_source = {
            "path": self.source_path, "media_type": media_type,
            "origin": SOURCE_ORIGIN, "license": SOURCE_LICENSE,
            "byte_length": len(source), "digest": _digest(source),
        }
        self.source_oracle = _closed_merge(common_source, source_details, case_id)
        self.document: dict[str, Any] | None = None
        self.bundle_path = f"{self.prefix}/bundle.json"
        self.verification_path = f"{self.prefix}/verification.json"

    def add_raster(
        self, name: str, unit: str, payload: bytes, *, width: int, height: int,
        render_contract: str = "fixture-retained-raster:v1",
    ) -> dict[str, Any]:
        path = f"{self.prefix}/rasters/{name}.png"
        self.artifacts.add(path, payload)
        record = {
            "id": _id(self.id, "raster", name), "source_id": _id(self.id, "source"),
            "unit": unit, "digest": _digest(payload), "render_contract": render_contract,
        }
        self.bundle["rasters"].append(record)
        self.raster_manifest.append({"path": path, "width": width, "height": height})
        return record

    def add_reading(
        self, name: str, raster: Mapping[str, Any], xywh: tuple[int, int, int, int],
        selected_text: str, *, response_text: str | None = None,
        outcome: str = "READING",
    ) -> dict[str, Any]:
        if name in self.readings:
            raise CorpusError(f"{self.id}: reading declared twice: {name}")
        if response_text is None:
            response_text = selected_text
        if not isinstance(response_text, str) or not isinstance(selected_text, str):
            raise CorpusError(f"{self.id}/{name}: reading texts must be strings")
        region = self._add_region(name, raster, xywh)
        exchange = self._exchange(name, raster, region, response_text, selected_text, outcome)
        attempt = {
            "id": _id(self.id, "attempt", name), "region_id": region["id"],
            "request_digest": exchange["request_digest"], "config_identity": CONFIG_IDENTITY,
            "status": "COMPLETED", "response_digest": exchange["response_digest"],
            "unavailable_reason": None,
        }
        machine = {
            "id": _id(self.id, "hypothesis", name, "machine"), "region_id": region["id"],
            "text_digest": _digest(response_text.encode("utf-8")),
            "attempt_id": attempt["id"], "correction_id": None, "confidence": None,
        }
        selection = {
            "id": _id(self.id, "selection", name), "region_id": region["id"],
            "candidate_ids": [machine["id"]], "selected_id": machine["id"],
            "reason": "single deterministic control reading",
            "human_verified": False,
        }
        self.bundle["attempts"].append(attempt)
        self.bundle["hypotheses"].append(machine)
        self.bundle["selections"].append(selection)
        oracle = {
            "id": region["id"], "unit": raster["unit"], "selector": region["selector"],
            "request": exchange["request_path"], "response": exchange["response_path"],
            "selected_text": exchange["selected_text_path"],
            "response_text": response_text, "expected_text": selected_text,
            "attempt_status": "COMPLETED",
        }
        self.oracle_regions.append(oracle)
        reading = {
            "region": region, "exchange": exchange, "machine": machine,
            "selection": selection, "oracle": oracle,
        }
        self.readings[name] = reading
        return reading

    def add_failed_attempt(
        self, name: str, raster: Mapping[str, Any], xywh: tuple[int, int, int, int]
    ) -> dict[str, Any]:
        region = self._add_region(name, raster, xywh)
        request_path, request_digest = self._request(
            name,
            raster,
            region,
            task="return the fixed self-authored control failure",
        )
        response_path = f"{self.prefix}/responses/{name}.json"
        response = {
            "contract": "malleus.fixture.control_failure_response.v1",
            "reader_id": READER["id"],
            "reader_kind": READER["kind"],
            "production_ocr": False,
            "region_id": region["id"],
            "outcome": "FAILED",
            "failure_class": "FIXTURE_CONTROL_FAILURE",
            "retryable": True,
            "note": (
                "The deterministic fixture reader returned this controlled failure. "
                "No OCR engine or provider was invoked."
            ),
        }
        response_bytes = self.artifacts.add_json(response_path, response)
        exchange = {
            "request_path": request_path,
            "request_digest": request_digest,
            "response_path": response_path,
            "response_digest": _digest(response_bytes),
        }
        self.exchanges.append(exchange)
        attempt = {
            "id": _id(self.id, "attempt", name),
            "region_id": region["id"],
            "request_digest": request_digest,
            "config_identity": {
                **CONFIG_IDENTITY,
                "response_contract": response["contract"],
            },
            "status": "FAILED",
            "response_digest": exchange["response_digest"],
            "unavailable_reason": None,
        }
        self.bundle["attempts"].append(attempt)
        oracle = {
            "id": region["id"],
            "unit": raster["unit"],
            "selector": region["selector"],
            "request": request_path,
            "response": response_path,
            "attempt_status": "FAILED",
            "failure_class": response["failure_class"],
        }
        self.oracle_regions.append(oracle)
        return {"region": region, "exchange": exchange, "attempt": attempt, "oracle": oracle}

    def add_unavailable_attempt(
        self, name: str, raster: Mapping[str, Any], xywh: tuple[int, int, int, int]
    ) -> dict[str, Any]:
        region = self._add_region(name, raster, xywh)
        request_path, request_digest = self._request(
            name,
            raster,
            region,
            task="record the fixed unavailable control-reader call",
        )
        exchange = {
            "request_path": request_path,
            "request_digest": request_digest,
        }
        self.exchanges.append(exchange)
        reason = "fixture reader disabled before invocation"
        attempt = {
            "id": _id(self.id, "attempt", name),
            "region_id": region["id"],
            "request_digest": request_digest,
            "config_identity": CONFIG_IDENTITY,
            "status": "UNAVAILABLE",
            "response_digest": None,
            "unavailable_reason": reason,
        }
        self.bundle["attempts"].append(attempt)
        oracle = {
            "id": region["id"],
            "unit": raster["unit"],
            "selector": region["selector"],
            "request": request_path,
            "attempt_status": "UNAVAILABLE",
            "unavailable_reason": reason,
        }
        self.oracle_regions.append(oracle)
        return {"region": region, "exchange": exchange, "attempt": attempt, "oracle": oracle}

    def _add_region(
        self, name: str, raster: Mapping[str, Any], xywh: tuple[int, int, int, int]
    ) -> dict[str, Any]:
        if len(xywh) != 4 or any(type(value) is not int or value < 0 for value in xywh):
            raise CorpusError(f"{self.id}/{name}: xywh must contain four nonnegative integers")
        region_id = _id(self.id, "region", name)
        if any(item["id"] == region_id for item in self.bundle["regions"]):
            raise CorpusError(f"{self.id}: region declared twice: {name}")
        region = {
            "id": region_id, "raster_id": raster["id"],
            "selector": {
                "type": "FragmentSelector",
                "value": "xywh=" + ",".join(str(value) for value in xywh),
            },
            "selector_profile": "w3c-web-annotation+iiif",
        }
        self.bundle["regions"].append(region)
        return region

    def _request(
        self,
        name: str,
        raster: Mapping[str, Any],
        region: Mapping[str, Any],
        *,
        task: str,
    ) -> tuple[str, str]:
        request_path = f"{self.prefix}/requests/{name}.json"
        request = {
            "contract": "malleus.fixture.control_request.v1", "reader_id": READER["id"],
            "reader_kind": READER["kind"], "production_ocr": False,
            "raster_digest": raster["digest"], "region_id": region["id"],
            "selector": region["selector"], "task": task,
        }
        request_bytes = self.artifacts.add_json(request_path, request)
        return request_path, _digest(request_bytes)

    def _exchange(
        self, name: str, raster: Mapping[str, Any], region: Mapping[str, Any],
        response_text: str, selected_text: str, outcome: str,
    ) -> dict[str, Any]:
        response_path = f"{self.prefix}/responses/{name}.json"
        selected_path = f"{self.prefix}/selected/{name}.txt"
        request_path, request_digest = self._request(
            name,
            raster,
            region,
            task="return the fixed self-authored control reading",
        )
        response = {
            "contract": "malleus.fixture.control_response.v1", "reader_id": READER["id"],
            "reader_kind": READER["kind"], "production_ocr": False,
            "region_id": region["id"], "outcome": outcome, "text": response_text,
            "note": "Retained fixture response. No recognition engine was invoked.",
        }
        response_bytes = self.artifacts.add_json(response_path, response)
        selected_bytes = self.artifacts.add_text(selected_path, selected_text)
        exchange = {
            "request_path": request_path, "request_digest": request_digest,
            "response_path": response_path, "response_digest": _digest(response_bytes),
            "selected_text_path": selected_path,
            "selected_text_digest": _digest(selected_bytes),
        }
        self.exchanges.append(exchange)
        return exchange

    def review(self, name: str, verdict: str, reason: str) -> None:
        reading = self.readings[name]
        machine = reading["machine"]
        selection = reading["selection"]
        correction_id = _id(self.id, "correction", name)
        corrected_digest = None
        if verdict == "CORRECTED":
            corrected_digest = reading["exchange"]["selected_text_digest"]
            corrected = {
                "id": _id(self.id, "hypothesis", name, "corrected"),
                "region_id": reading["region"]["id"], "text_digest": corrected_digest,
                "attempt_id": None, "correction_id": correction_id, "confidence": None,
            }
            self.bundle["hypotheses"].append(corrected)
            selection["candidate_ids"].append(corrected["id"])
            selection["selected_id"] = corrected["id"]
        elif verdict != "VERIFIED_BLANK":
            raise CorpusError(f"{self.id}/{name}: unsupported fixture review verdict {verdict!r}")
        self.bundle["corrections"].append({
            "id": correction_id, "reviewed_hypothesis_id": machine["id"],
            "reviewer_id": "fixture:reviewer:human-control",
            "verdict": verdict, "corrected_text_digest": corrected_digest, "predecessor_id": None,
        })
        selection["reason"] = reason
        selection["human_verified"] = True
        reading["oracle"]["human_verdict"] = verdict

    def write_reference(self, expected: Mapping[str, Any]) -> dict[str, Any]:
        self.document = _write_verified_document(
            self.artifacts, bundle_path=self.bundle_path,
            verification_path=self.verification_path, document=_document(self.bundle),
            expected=expected, label=self.id,
        )
        return self.document

    def write_mutation(
        self, *, mutation_id: str, purpose: str, document: Mapping[str, Any],
        expected: Mapping[str, Any],
        expected_diagnostics: tuple[tuple[str, str], ...] = (),
        extra: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        prefix = f"{self.prefix}/mutations/{mutation_id}"
        bundle_path = f"{prefix}.bundle.json"
        verification_path = f"{prefix}.verification.json"
        _write_verified_document(
            self.artifacts, bundle_path=bundle_path, verification_path=verification_path,
            document=document, expected=expected, expected_diagnostics=expected_diagnostics,
            label=f"{self.id}/{mutation_id}",
        )
        record = {
            "id": mutation_id, "purpose": purpose, "bundle": bundle_path,
            "verification": verification_path,
            "expected_diagnostic_codes": list(expected["diagnostic_codes"]),
        }
        return _closed_merge(record, extra, f"{self.id}/{mutation_id}")

    def finish(
        self, *, fixture_kind: str, expected: Mapping[str, Any],
        mutations: list[Mapping[str, Any]],
        oracle_extra: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self.document is None:
            raise CorpusError(f"{self.id}: reference bundle was not written")
        oracle = {
            "case_id": self.id, "fixture_kind": fixture_kind, "purpose": self.purpose,
            "source": self.source_oracle, "reference_reader": READER,
            "regions": self.oracle_regions, "expected_verification": expected,
            "mutations": mutations,
        }
        oracle = _closed_merge(oracle, oracle_extra, self.id)
        oracle_path = f"{self.prefix}/oracle.json"
        self.artifacts.add_json(oracle_path, oracle)
        return {
            "id": self.id, "purpose": self.purpose, "source": self.source_path,
            "oracle": oracle_path, "bundle": self.bundle_path,
            "verification": self.verification_path, "rasters": self.raster_manifest,
            "requests": [item["request_path"] for item in self.exchanges],
            "responses": [
                item["response_path"]
                for item in self.exchanges
                if "response_path" in item
            ],
            "selected_texts": [
                item["selected_text_path"]
                for item in self.exchanges
                if "selected_text_path" in item
            ],
            "mutations": mutations,
        }


def _region_control(artifacts: Artifacts) -> dict[str, Any]:
    source = _region_control_png()
    case = Case(
        artifacts,
        case_id="region-control",
        purpose="Keep two visible regions and every reading path spatially separate.",
        source_name="region-control.png",
        source=source,
        media_type="image/png",
        required_units=["image:1"],
        observed_units=["image:1"],
        source_details={"pixel_dimensions": {"width": 1200, "height": 800}},
    )
    raster = case.add_raster("image-1", "image:1", source, width=1200, height=800)
    case.add_reading("a", raster, (80, 180, 500, 420), "REGION A\nALPHA 123\nLEFT BOX")
    case.add_reading("b", raster, (620, 180, 500, 420), "REGION B\nBRAVO 789\nRIGHT BOX")
    expected = _expected({"image:1": ("READ", "ACCOUNTED")})
    document = case.write_reference(expected)
    mutation_expected = _refusal(expected, "OCR-D003")
    crossed_attempt = copy.deepcopy(document)
    crossed_attempt["bundle"]["hypotheses"][0]["attempt_id"] = (
        crossed_attempt["bundle"]["attempts"][1]["id"]
    )
    mutations = [case.write_mutation(
        mutation_id="hypothesis-attempt-cross-region",
        purpose="A hypothesis cannot cite an attempt over the other region.",
        document=crossed_attempt,
        expected=mutation_expected,
        expected_diagnostics=(("OCR-D003", _id(case.id, "hypothesis", "a", "machine")),),
    )]
    crossed_selection = copy.deepcopy(document)
    other = crossed_selection["bundle"]["hypotheses"][1]["id"]
    crossed_selection["bundle"]["selections"][0]["candidate_ids"] = [other]
    crossed_selection["bundle"]["selections"][0]["selected_id"] = other
    mutations.append(case.write_mutation(
        mutation_id="selection-hypothesis-cross-region",
        purpose="A selection cannot select a hypothesis over the other region.",
        document=crossed_selection,
        expected=mutation_expected,
        expected_diagnostics=(("OCR-D003", _id(case.id, "selection", "a")),),
    ))
    return case.finish(
        fixture_kind="single_image_two_regions",
        expected=expected,
        mutations=mutations,
    )


def _failed_attempt(artifacts: Artifacts) -> dict[str, Any]:
    source = _failed_attempt_png()
    purpose = "Retain a made-but-failed control-reader attempt without inventing a reading."
    case = Case(
        artifacts,
        case_id="failed-attempt",
        purpose=purpose,
        source_name="failed-attempt.png",
        source=source,
        media_type="image/png",
        required_units=["image:1"],
        observed_units=["image:1"],
        source_details={"pixel_dimensions": {"width": 1000, "height": 700}},
    )
    raster = case.add_raster("image-1", "image:1", source, width=1000, height=700)
    case.add_failed_attempt("main", raster, (100, 180, 800, 390))
    expected = _expected(
        complete=False,
        units={"image:1": ("FAILED", "CHECK_FAILED")},
        metric_value=0.0,
        metric_verdict="UNMET",
    )
    case.write_reference(expected)
    return case.finish(
        fixture_kind="single_image_failed_attempt",
        expected=expected,
        mutations=[],
    )


def _unavailable_attempt(artifacts: Artifacts) -> dict[str, Any]:
    source = _unavailable_attempt_png()
    purpose = (
        "Retain an unavailable control-reader call without inventing a response or reading."
    )
    case = Case(
        artifacts,
        case_id="unavailable-attempt",
        purpose=purpose,
        source_name="unavailable-attempt.png",
        source=source,
        media_type="image/png",
        required_units=["image:1"],
        observed_units=["image:1"],
        source_details={"pixel_dimensions": {"width": 1000, "height": 700}},
    )
    raster = case.add_raster("image-1", "image:1", source, width=1000, height=700)
    case.add_unavailable_attempt("main", raster, (100, 180, 800, 390))
    expected = _expected(
        complete=False,
        units={"image:1": ("UNAVAILABLE", "CHECK_FAILED")},
        metric_value=0.0,
        metric_verdict="UNMET",
    )
    document = case.write_reference(expected)
    missing_reason = copy.deepcopy(document)
    missing_reason["bundle"]["attempts"][0]["unavailable_reason"] = None
    mutations = [case.write_mutation(
        mutation_id="missing-unavailable-reason",
        purpose="An unavailable attempt must state why the call could not be made.",
        document=missing_reason,
        expected=_refusal(expected, "OCR-D015"),
        expected_diagnostics=(("OCR-D015", _id(case.id, "attempt", "main")),),
    )]
    return case.finish(
        fixture_kind="single_image_unavailable_attempt",
        expected=expected,
        mutations=mutations,
    )


def _multipage_control(artifacts: Artifacts) -> dict[str, Any]:
    selected = "The quick brown fox jumps.\nAMBIGUOUS TOKEN\nO0I1l"
    response = "The quick brown fox jumps.\nAMBIGUOUS TOKEN\nOOI1l"
    page_1 = _document_page(
        "PAGE 1 OF 2", "KNOWN TEXT", "The quick brown fox jumps.\n\nAMBIGUOUS TOKEN\nO0I1l"
    )
    page_2 = _document_page("", "", "", blank=True)
    source, pages = _raster_pdf("Malleus OCR multipage control", (page_1, page_2))
    case = Case(
        artifacts,
        case_id="multipage-control",
        purpose="Retain a corrected ambiguous token and an independently verified blank page.",
        source_name="multipage-control.pdf",
        source=source,
        media_type="application/pdf",
        required_units=["page:1", "page:2"],
        observed_units=["page:1", "page:2"],
        source_details={
            "physical_page_count": 2,
            "physical_page_size_points": {"width": 500, "height": 700},
            "raster_only": True,
        },
    )
    raster_1 = case.add_raster("page-1", "page:1", **pages[0])
    raster_2 = case.add_raster("page-2", "page:2", **pages[1])
    # This selector covers only the body. The visible KNOWN TEXT heading sits
    # above y=650 and is deliberately outside the retained reading.
    case.add_reading(
        "page-1-body", raster_1, (140, 650, 720, 410), selected,
        response_text=response,
    )
    case.add_reading("page-2-blank", raster_2, (0, 0, 1000, 1400), "", outcome="BLANK")
    case.review(
        "page-1-body", "CORRECTED", "human correction resolves the intentionally ambiguous token"
    )
    case.review(
        "page-2-blank", "VERIFIED_BLANK", "human review confirms the retained empty response"
    )
    expected = _expected({
        "page:1": ("READ", "ACCOUNTED"),
        "page:2": ("VERIFIED_BLANK", "ACCOUNTED"),
    })
    document = case.write_reference(expected)
    mutated = copy.deepcopy(document)
    mutated["bundle"]["corrections"][0]["corrected_text_digest"] = (
        mutated["bundle"]["hypotheses"][0]["text_digest"]
    )
    mutation_expected = _refusal(expected, "OCR-D015")
    correction_id = _id(case.id, "correction", "page-1-body")
    mutations = [case.write_mutation(
        mutation_id="correction-text-digest-mismatch",
        purpose="The correction digest must equal the corrected hypothesis digest.",
        document=mutated,
        expected=mutation_expected,
        expected_diagnostics=(("OCR-D015", correction_id),),
    )]
    return case.finish(
        fixture_kind="two_page_raster_only_pdf",
        expected=expected,
        mutations=mutations,
    )


def _incomplete_sequence(artifacts: Artifacts) -> dict[str, Any]:
    text_1 = "CONTROL START\nLogical page 2 is absent from this source."
    text_3 = "CONTROL END\nThe source sequence jumps from 1 to 3."
    page_1 = _document_page(
        "SEQUENCE PAGE 1 OF 3", "CONTROL START", "Logical page 2 is absent from this source."
    )
    page_3 = _document_page(
        "SEQUENCE PAGE 3 OF 3", "CONTROL END", "The source sequence jumps from 1 to 3."
    )
    source, pages = _raster_pdf("Malleus OCR incomplete sequence", (page_1, page_3))
    case = Case(
        artifacts,
        case_id="incomplete-sequence",
        purpose=(
            "Source declares logical pages 1 and 3 against required 1, 2, and 3; "
            "this is a source-sequence gap, not OCR skipping a present physical page."
        ),
        source_name="incomplete-sequence.pdf",
        source=source,
        media_type="application/pdf",
        required_units=["page:1", "page:2", "page:3"],
        observed_units=["page:1", "page:3"],
        source_details={
            "physical_page_count": 2,
            "physical_page_size_points": {"width": 500, "height": 700},
            "logical_page_labels": ["1 of 3", "3 of 3"],
            "raster_only": True,
        },
    )
    raster_1 = case.add_raster("page-1", "page:1", **pages[0])
    raster_3 = case.add_raster("page-3", "page:3", **pages[1])
    case.add_reading("page-1-body", raster_1, (100, 350, 800, 810), text_1)
    case.add_reading("page-3-body", raster_3, (100, 350, 800, 810), text_3)
    expected = _expected(
        complete=False,
        units={
            "page:1": ("READ", "ACCOUNTED"),
            "page:2": ("NOT_OBSERVED", "NOT_CHECKED"),
            "page:3": ("READ", "ACCOUNTED"),
        },
        metric_value=2 / 3,
        metric_verdict="UNMET",
    )
    document = case.write_reference(expected)
    mutated = copy.deepcopy(document)
    mutated["bundle"]["observed_units"] = ["page:1", "page:2", "page:3"]
    mutation_expected = _expected(
        complete=False,
        units={
            "page:1": ("READ", "ACCOUNTED"),
            "page:2": ("NOT_RENDERED", "NOT_CHECKED"),
            "page:3": ("READ", "ACCOUNTED"),
        },
        metric_value=2 / 3,
        metric_verdict="UNMET",
    )
    mutations = [case.write_mutation(
        mutation_id="observed-without-raster",
        purpose="An observed-unit assertion cannot replace a missing raster and reading.",
        document=mutated,
        expected=mutation_expected,
        extra={"expected_unit_outcome": {"page:2": "NOT_RENDERED"}},
    )]
    return case.finish(
        fixture_kind="two_physical_pages_three_logical_units",
        expected=expected,
        mutations=mutations,
        oracle_extra={"missing_logical_units": ["page:2"]},
    )


def build_artifacts() -> dict[str, bytes]:
    _assert_generator_runtime()
    artifacts = Artifacts()
    builders = (
        _region_control,
        _multipage_control,
        _incomplete_sequence,
        _failed_attempt,
        _unavailable_attempt,
    )
    cases = [builder(artifacts) for builder in builders]
    root_ontology = ROOT / "ontology" / "malleus.yaml"
    ocr_ontology = ROOT / "ontology" / "domains" / "ocr.yaml"
    for required in (root_ontology, ocr_ontology):
        if not required.is_file():
            raise CorpusError(f"required ontology input is missing: {required}")
    manifest = {
        "corpus_id": "malleus.ocr.fixture_corpus",
        "corpus_version": 1,
        "ocr_profile_id": PROFILE_ID,
        "ocr_profile_version": PROFILE_VERSION,
        "generated_by": "conformance/ocr/v0/corpus/generate.py",
        "hash_algorithm": "sha256",
        "document_policy": {
            "authorship": "self-authored deterministic controls",
            "contains_private_material": False,
            "contains_production_material": False,
            "network_required": False,
        },
        "reference_reader": READER,
        "runtime_binding": {
            "malleus_version": __version__,
            "root_ontology_path": "ontology/malleus.yaml",
            "root_ontology_sha256": _digest(root_ontology.read_bytes()),
            "ocr_ontology_path": "ontology/domains/ocr.yaml",
            "ocr_ontology_sha256": _digest(ocr_ontology.read_bytes()),
            "ocr_registry_content_hash": profile_registry().content_hash(),
            "generator": {
                "contract": GENERATOR_CONTRACT,
                "python_contract": PYTHON_CONTRACT,
                "pillow_version": PILLOW_VERSION,
                "png_contract": PNG_CONTRACT,
                "pypdf_version": PYPDF_VERSION,
                "reportlab_version": REPORTLAB_VERSION,
                "zlib_contract": ZLIB_CONTRACT,
            },
        },
        "cases": cases,
    }
    artifacts.add_json("corpus.json", manifest)
    checksums = {
        "algorithm": "sha256",
        "scope": "every generated file except checksums.json",
        "files": {
            path: {"sha256": _digest(payload), "byte_length": len(payload)}
            for path, payload in sorted(artifacts.files.items())
        },
    }
    artifacts.add_json("checksums.json", checksums)
    return dict(sorted(artifacts.files.items()))


def _managed_files(root: Path) -> set[str]:
    paths = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise CorpusError(f"corpus member is a symlink: {relative}")
        parts = PurePosixPath(relative).parts
        if "__pycache__" in parts:
            cache = root.joinpath(*parts[: parts.index("__pycache__") + 1])
            if cache.is_dir():
                continue
        if path.is_file() and relative not in CONTROL_FILES:
            paths.add(relative)
    return paths


def write_artifacts(expected: Mapping[str, bytes]) -> None:
    retained = _managed_files(CORPUS_ROOT)
    undeclared = sorted(retained - set(expected))
    if undeclared:
        raise CorpusError("refusing to leave undeclared generated files: " + ", ".join(undeclared))
    for relative, payload in expected.items():
        target = _target(CORPUS_ROOT, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
    verify_retained(expected)


def verify_retained(expected: Mapping[str, bytes]) -> None:
    retained = _managed_files(CORPUS_ROOT)
    missing = sorted(set(expected) - retained)
    undeclared = sorted(retained - set(expected))
    changed = sorted(
        path
        for path in set(expected) & retained
        if _target(CORPUS_ROOT, path).read_bytes() != expected[path]
    )
    problems = []
    if missing:
        problems.append("missing: " + ", ".join(missing))
    if undeclared:
        problems.append("undeclared: " + ", ".join(undeclared))
    if changed:
        problems.append("byte drift: " + ", ".join(changed))
    if problems:
        raise CorpusError("retained corpus differs from deterministic generation; " + "; ".join(problems))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        nargs="?",
        choices=("write", "check"),
        default="write",
        help="write artifacts or compare retained bytes with a fresh in-memory generation",
    )
    arguments = parser.parse_args()
    expected = build_artifacts()
    if arguments.mode == "check":
        verify_retained(expected)
        print(f"verified {len(expected)} deterministic corpus artifacts")
    else:
        write_artifacts(expected)
        print(f"wrote {len(expected)} deterministic corpus artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
