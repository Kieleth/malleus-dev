"""Stage a run's declared inputs and hold them to their digests.

A packet is what one stage is handed. The mechanism is two steps and no more:
``stage_files`` writes declared bytes at declared paths and returns one record
per file, and ``verify_files`` reads those records back and refuses a file that
is absent, a digest that moved, or a byte count that does not match.

The packet **record** is the adapter's, measured against the two consumers that
exist: one declares a packet as a single file with a row count, the other as a
list of files each carrying its role and where its bytes were read. So this
module returns per-file records and never writes a declaration; the adapter
assembles its own and keeps the labels that say what a packet carries.
"""

from __future__ import annotations

from pathlib import Path

from .digests import digest


class PacketRefusal(ValueError):
    """A packet is missing, changed, or not the shape the declaration names."""


def stage_files(directory, files):
    """Write each ``(relative, bytes)`` and return its record.

    ``files`` is an ordered sequence of ``(relative path, bytes)``. The record
    carries the path, the digest and the byte count, which are the three the
    check on the way back needs; anything else about a file is the adapter's.
    """
    directory = Path(directory)
    records = []
    for relative, data in files:
        target = directory / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        records.append(
            {"path": str(relative), "sha256": digest(data), "bytes": len(data)}
        )
    return records


def verify_files(directory, records, *, check_bytes=True):
    """Refuse the first declared file whose bytes are not the frozen ones."""
    directory = Path(directory)
    for item in records:
        target = directory / item["path"]
        if not target.is_file():
            raise PacketRefusal(f"{item['path']}: declared and not present")
        data = target.read_bytes()
        found = digest(data)
        if found != item["sha256"]:
            raise PacketRefusal(
                f"{item['path']}: {found} is not the frozen {item['sha256']}"
            )
        if check_bytes and "bytes" in item and len(data) != item["bytes"]:
            raise PacketRefusal(
                f"{item['path']}: {len(data)} bytes, not the frozen {item['bytes']}"
            )
    return records


def would_move(directory, records, files):
    """Declared paths whose bytes differ from what is frozen. Writes nothing.

    Freezing overwrites, which is right before a producer has seen anything and
    wrong after. A caller that must not re-freeze asks this first: an empty list
    means freezing again would be a no-op.
    """
    directory = Path(directory)
    declared = {item["path"]: item["sha256"] for item in records}
    current = {str(relative): digest(data) for relative, data in files}
    return sorted(
        path
        for path in set(declared) | set(current)
        if declared.get(path) != current.get(path)
    )


def frozen_digests(records):
    """Every declared digest, the set a ``DATA`` file must be one of."""
    return {item["sha256"] for item in records}
