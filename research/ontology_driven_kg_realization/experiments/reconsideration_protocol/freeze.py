"""The launched-stage guard. Everything a rebuild must ask before it writes.

A launched stage is never rebuilt: its workspace is where a producer ran and
its manifest is that run's record. One consumer learned this by deleting a
verified producer's output with a rebuild and finding that the record surviving
is not the work surviving. So the guard runs before the first write, and a
refusal leaves every tree exactly as it was.

The guard reads both places a launch can be written, each stage's own producer
manifest and the run index's copy, and either alone stops a rebuild.

The run **index** is not here. Measured against the two consumers, their two
indexes share this guard and nothing else: one records artifact digests,
packets, obligations, per-stage producer rows and the assessment containment,
the other records per-stage rows and four identity digests. Each assembles its
own; ``digests.artifact_digests`` and ``index.is_stale`` are the two pieces
both can use.
"""

from __future__ import annotations

import json
from pathlib import Path


class FreezeRefusal(ValueError):
    """A launch is recorded; rebuilding would overwrite the run's own record."""


def launched(stage, *, harnesses, root):
    """Whether one stage's own producer manifest records a launch."""
    recorded = (
        Path(root) / "producer" / harnesses[stage] / "producer-input-manifest.json"
    )
    if not recorded.is_file():
        return False
    launch = json.loads(recorded.read_bytes()).get("launch") or {}
    return bool(launch.get("launched"))


def launch_records(root, *, stages, harnesses, manifest_name=None):
    """The stages a prepared tree records as launched, in stage order."""
    root = Path(root)
    index = {}
    if manifest_name is not None:
        index_path = root / manifest_name
        if index_path.is_file():
            index = json.loads(index_path.read_bytes()).get("producer", {})
    found = []
    for stage in stages:
        recorded = launched(stage, harnesses=harnesses, root=root) or bool(
            index.get(stage, {}).get("launched")
        )
        if recorded:
            found.append(stage)
    return found


def refuse_if_launched(requested, recorded):
    """Refuse when any stage a rebuild would touch is already launched."""
    collide = [stage for stage in recorded if stage in tuple(requested)]
    if collide:
        raise FreezeRefusal(
            "LAUNCH_RECORDED: a launch is recorded for stage "
            + ", ".join(collide)
            + "; that stage's workspace is where a producer ran and its manifest"
            " is that run's record. Name the other stage to rebuild it."
        )


def refusal_report(refusal, *, recorded, requested):
    """One ``FreezeRefusal`` as the typed object a command prints."""
    return {
        "status": "REFUSED",
        "reason": "LAUNCH_RECORDED",
        "detail": str(refusal),
        "stages": list(recorded),
        "rebuild_requested": list(requested),
    }
