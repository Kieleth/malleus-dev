"""Content-addressed source artifacts for evidence provenance."""

from __future__ import annotations

import hashlib
from typing import Any

from malleus.ledger import LedgerError, content_digest, require_digest


class SourceError(ValueError):
    """A source artifact field or byte binding is invalid."""


def source_bytes_digest(source_bytes: bytes) -> str:
    """Return the SHA-256 identity of exact source bytes."""
    if not isinstance(source_bytes, bytes):
        raise TypeError("source_bytes must be bytes")
    return "sha256:" + hashlib.sha256(source_bytes).hexdigest()


def source_artifact_digest(
    *,
    schema_version: str,
    artifact_id: str,
    artifact_version: str,
    source_content_digest: str,
    source_byte_length: int,
    source_media_type: str,
    source_locator: str,
) -> str:
    """Hash the replay-visible meaning of one source artifact."""
    if schema_version != "1":
        raise SourceError("source_schema_version must be '1'")
    for name, value in (
        ("artifact_id", artifact_id),
        ("artifact_version", artifact_version),
        ("source_media_type", source_media_type),
        ("source_locator", source_locator),
    ):
        if not isinstance(value, str) or not value.strip():
            raise SourceError(f"{name} must be a nonblank string")
    if (
        not isinstance(source_byte_length, int)
        or isinstance(source_byte_length, bool)
        or source_byte_length < 0
    ):
        raise SourceError("source_byte_length must be a nonnegative integer")
    try:
        require_digest(source_content_digest, "source_content_digest")
    except LedgerError as error:
        raise SourceError(str(error)) from error
    return content_digest({
        "source_schema_version": schema_version,
        "artifact_id": artifact_id,
        "artifact_version": artifact_version,
        "source_content_digest": source_content_digest,
        "source_byte_length": source_byte_length,
        "source_media_type": source_media_type,
        "source_locator": source_locator,
    })


def source_artifact_fields(
    *,
    artifact_id: str,
    artifact_version: str,
    source_bytes: bytes,
    media_type: str,
    locator: str,
) -> dict[str, Any]:
    """Build the semantic fields for a SourceArtifact from exact bytes."""
    digest = source_bytes_digest(source_bytes)
    fields = {
        "source_schema_version": "1",
        "source_content_digest": digest,
        "source_byte_length": len(source_bytes),
        "source_media_type": media_type,
        "source_locator": locator,
    }
    fields["artifact_hash"] = source_artifact_digest(
        schema_version=fields["source_schema_version"],
        artifact_id=artifact_id,
        artifact_version=artifact_version,
        source_content_digest=fields["source_content_digest"],
        source_byte_length=fields["source_byte_length"],
        source_media_type=fields["source_media_type"],
        source_locator=fields["source_locator"],
    )
    return fields
