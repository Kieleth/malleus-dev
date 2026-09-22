"""The two byte operations every module here shares.

One canonical encoding and one digest, in one place, so two artifacts of the
same run cannot disagree about what a digest is taken over.
"""

from __future__ import annotations

from hashlib import sha256
import json


def digest(data: bytes) -> str:
    """The prefixed SHA-256 of exact bytes."""
    return "sha256:" + sha256(data).hexdigest()


def canonical(value) -> bytes:
    """Canonical JSON bytes: UTF-8, sorted keys, no insignificant whitespace."""
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def indented(value) -> bytes:
    """The readable encoding this protocol writes its own records in."""
    return json.dumps(value, indent=2, sort_keys=True).encode() + b"\n"


def reference(identifier: str, data: bytes) -> dict:
    """One ``{id, sha256}`` reference, the shape Core's boundary grammar reads."""
    return {"id": identifier, "sha256": digest(data)}


def artifact_digests(root, roots) -> dict:
    """Every file under the named roots, by path relative to ``root``."""
    artifacts = {}
    for directory in roots:
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                artifacts[str(path.relative_to(root))] = digest(path.read_bytes())
    return dict(sorted(artifacts.items()))
