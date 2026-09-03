"""Extract one digest-frozen PDF text-layer reading for paper v4."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from typing import Any, Mapping, Sequence

try:
    import pypdf
except ImportError as error:  # pragma: no cover - exercised by environment setup
    raise RuntimeError(
        "paper v4 requires pypdf==6.16.2; install the project research extra"
    ) from error


READING_SCHEMA = "malleus.paper-v4.text-layer-reading/v1"
PINNED_PYPDF_VERSION = "6.16.2"
_BLANK = re.compile(r"^[ \t]*$")


class TextLayerReadingError(ValueError):
    """The selected reading cannot be produced without guessing."""


def _digest(value: bytes) -> str:
    return "sha256:" + sha256(value).hexdigest()


def _canonical_json(value: Any) -> bytes:
    try:
        return (
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
            + "\n"
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        raise TextLayerReadingError(f"reading is not canonical JSON: {error}") from error


def _require_pypdf_version(installed: str) -> None:
    if installed != PINNED_PYPDF_VERSION:
        raise TextLayerReadingError(
            "pypdf version drift: "
            f"expected {PINNED_PYPDF_VERSION}, found {installed}"
        )


def _load_manifest(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise TextLayerReadingError(f"cannot read source manifest {path}: {error}") from error
    if not isinstance(value, Mapping):
        raise TextLayerReadingError("source manifest must be a JSON object")
    try:
        artifact = value["artifact"]
        artifact["path"]
        artifact["sha256"]
        artifact["page_count"]
    except (KeyError, TypeError) as error:
        raise TextLayerReadingError(
            f"source manifest is missing required artifact field: {error}"
        ) from error
    if not isinstance(artifact, Mapping):
        raise TextLayerReadingError("source manifest artifact must be an object")
    return value


def _source_path(repo_root: Path, locator: Any) -> Path:
    if not isinstance(locator, str) or not locator:
        raise TextLayerReadingError("source artifact path must be a nonempty string")
    relative = Path(locator)
    if relative.is_absolute() or ".." in relative.parts:
        raise TextLayerReadingError("source artifact path must stay inside the repository")
    path = (repo_root / relative).resolve()
    root = repo_root.resolve()
    if not path.is_relative_to(root):
        raise TextLayerReadingError("source artifact path escapes the repository")
    return path


def _blocks(text: str, page: int) -> list[dict[str, Any]]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = []
    lines = (line for line in normalized.split("\n") if not _BLANK.fullmatch(line))
    for ordinal, line in enumerate(lines, start=1):
        payload = (line + "\n").encode("utf-8")
        blocks.append(
            {
                "id": f"page:{page}:block:{ordinal:03d}",
                "ordinal": ordinal,
                "sha256": _digest(payload),
                "text": payload.decode("utf-8"),
            }
        )
    return blocks


def build_reading(repo_root: Path, source_manifest_path: Path) -> bytes:
    """Return the canonical selected-reading bytes without writing them."""

    _require_pypdf_version(pypdf.__version__)
    manifest = _load_manifest(source_manifest_path)
    artifact = manifest["artifact"]
    source = _source_path(repo_root, artifact["path"])
    try:
        source_bytes = source.read_bytes()
    except OSError as error:
        raise TextLayerReadingError(f"cannot read source PDF {source}: {error}") from error
    observed_source_digest = _digest(source_bytes)
    if observed_source_digest != artifact["sha256"]:
        raise TextLayerReadingError(
            "source PDF digest drift: "
            f"expected {artifact['sha256']}, found {observed_source_digest}"
        )

    try:
        reader = pypdf.PdfReader(source, strict=True)
    except Exception as error:
        raise TextLayerReadingError(f"pypdf refused source PDF {source}: {error}") from error
    if reader.is_encrypted:
        raise TextLayerReadingError("source PDF is encrypted")
    if len(reader.pages) != artifact["page_count"]:
        raise TextLayerReadingError(
            "source PDF page-count drift: "
            f"expected {artifact['page_count']}, found {len(reader.pages)}"
        )

    pages = []
    total_blocks = 0
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text()
        except Exception as error:
            raise TextLayerReadingError(
                f"pypdf refused text extraction on page {page_number}: {error}"
            ) from error
        if not text:
            raise TextLayerReadingError(
                f"pypdf returned no text for required page {page_number}"
            )
        blocks = _blocks(text, page_number)
        if not blocks:
            raise TextLayerReadingError(
                f"text projection returned no blocks for required page {page_number}"
            )
        total_blocks += len(blocks)
        pages.append({"page": page_number, "blocks": blocks})

    return _canonical_json(
        {
            "schema": READING_SCHEMA,
            "source_sha256": observed_source_digest,
            "extractor": {
                "distribution": "pypdf",
                "version": PINNED_PYPDF_VERSION,
                "call": "PdfReader(strict=True); PageObject.extract_text()",
            },
            "projection": {
                "line_endings": "CRLF_AND_CR_TO_LF",
                "blank_line": "ZERO_OR_MORE_SPACE_OR_TAB_CHARACTERS",
                "block_rule": "EACH_NONBLANK_EXTRACTED_LINE",
                "block_text": "EXTRACTED_LINE_WITH_ONE_TERMINAL_LF",
                "text_correction": "NONE",
            },
            "page_count": len(pages),
            "block_count": total_blocks,
            "pages": pages,
        }
    )


def write_reading(output_path: Path, reading: bytes) -> None:
    """Write once; an existing path is a refusal, not an overwrite."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output_path.open("xb") as stream:
            stream.write(reading)
    except FileExistsError as error:
        raise TextLayerReadingError(
            f"selected reading already exists at {output_path}"
        ) from error
    except OSError as error:
        raise TextLayerReadingError(
            f"cannot write selected reading {output_path}: {error}"
        ) from error


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    reading = build_reading(args.repo_root, args.source_manifest)
    write_reading(args.output, reading)
    document = json.loads(reading)
    print(
        json.dumps(
            {
                "selected_reading_sha256": _digest(reading),
                "page_count": document["page_count"],
                "block_count": document["block_count"],
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
