"""Re-deriving a run's index, and asking whether the one on disk is current.

A consumer's index writes only while a stage is being built and refuses for a
launched one, so once every stage has launched the index cannot be brought up
to date at all: it stops being maintainable exactly when the run finishes. The
reader that fixes that builds nothing and refuses nothing.

The index **record** is the consumer's, so what is here is the two pieces both
can use: the digest of every file under the declared roots, and whether the
file on disk is the bytes a fresh derivation produces.
"""

from __future__ import annotations

from pathlib import Path

from .digests import artifact_digests, indented

__all__ = ["artifact_digests", "derived_bytes", "is_stale"]


def derived_bytes(manifest):
    """One index record as the bytes it is written as."""
    return indented(manifest)


def is_stale(path, manifest):
    """Whether the index on disk is not what a fresh derivation would write."""
    path = Path(path)
    if not path.is_file():
        return True
    return path.read_bytes() != derived_bytes(manifest)
