"""A read-only copy of a launched stage's work, taken the moment it reports.

The first step after any producer reports, before anything else reads or
rebuilds. The archive is named for the launch, never overwritten, and its files
are made read-only. A second run refuses rather than replacing the first.

This is the mechanical answer to a producer's output being deleted by a rebuild
with no copy anywhere, not a commandment about being careful.
"""

from __future__ import annotations

import json
from pathlib import Path

from .adapter import Adapter
from .digests import digest, indented


READ_ONLY = 0o444


class ArchiveRefusal(ValueError):
    """The stage has not launched, or an archive of that launch already exists."""


def archive(stage, *, adapter: Adapter, source=None, root=None):
    """Copy one launched stage's work into its archive, once."""
    if stage not in adapter.names:
        raise ArchiveRefusal(
            f"unknown stage: {stage!r}; expected one of {sorted(adapter.names)}"
        )
    root = adapter.layout.root if root is None else Path(root)
    harness = root / "producer" / adapter.stage(stage).harness
    manifest = json.loads((harness / "producer-input-manifest.json").read_bytes())
    launched_at = manifest["launch"]["launched_at"]
    if not manifest["launch"]["launched"]:
        raise ArchiveRefusal(
            f"stage {stage} is not launched; there is no producer work to archive"
        )
    source = (
        Path(root / manifest["workspace"] / adapter.layout.work_dir)
        if source is None
        else Path(source)
    )
    if not source.is_dir():
        raise ArchiveRefusal(f"{source} does not exist")
    files = sorted(path for path in source.rglob("*") if path.is_file())
    if not files:
        raise ArchiveRefusal(f"{source} holds no files; there is nothing to archive")
    target = harness / "archive" / launched_at
    if target.exists():
        raise ArchiveRefusal(
            f"{target} already exists; this launch is already archived and an"
            " archive is never replaced"
        )

    entries = []
    for path in files:
        relative = path.relative_to(source)
        destination = target / adapter.layout.work_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        destination.write_bytes(data)
        entries.append(
            {"path": str(relative), "bytes": len(data), "sha256": digest(data)}
        )
    record = {
        "schema": adapter.schemas.archive,
        "stage": stage,
        "run_id": manifest["run_id"],
        "launched_at": launched_at,
        "source": str(source),
        "archived_from_workspace": source
        == root / manifest["workspace"] / adapter.layout.work_dir,
        "files": entries,
        "file_count": len(entries),
        "total_bytes": sum(item["bytes"] for item in entries),
    }
    (target / "ARCHIVE.json").write_bytes(indented(record))
    for path in sorted(target.rglob("*")):
        if path.is_file():
            path.chmod(READ_ONLY)
    return {
        "status": "ARCHIVED",
        "stage": stage,
        "launched_at": launched_at,
        "archive": str(target.relative_to(root)),
        "files": len(entries),
        "total_bytes": record["total_bytes"],
    }
