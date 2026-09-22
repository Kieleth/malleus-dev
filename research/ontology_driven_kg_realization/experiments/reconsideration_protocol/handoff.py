"""What crosses a stage boundary, read from the predecessor's output alone.

Two things cross: the graph the producer exported, and the frozen obligations
bound to the record ids in that graph. Both are read from the predecessor's own
output and from nothing else. Ground truth is not read here and could not
change a binding if it were: the binding selects by type and role over the
export alone.

A finished stage's output is read from its archive, never from its live
workspace, and the export's file name comes from the stage's own declaration,
so a reader asks for stage X's export and cannot be handed its predecessor's by
a copied literal.
"""

from __future__ import annotations

import json
from pathlib import Path

from .adapter import Adapter
from .digests import digest


class HandoffRefusal(ValueError):
    """A stage's output is absent, or is not what its own history replays to."""


def predecessor_of(stage, predecessors):
    """The stage whose history this one continues, or None for a first stage."""
    if stage not in predecessors:
        raise HandoffRefusal(f"no predecessor is declared for stage {stage!r}")
    return predecessors[stage]


def predecessor_history(stage, *, predecessors, histories):
    """The history a stage inherits, as (path, verified digest).

    ``histories`` maps a stage to the location and verified digest of the
    history it wrote. A stage that continues another's history must be given
    it; this is where the placing step reads it from.
    """
    previous = predecessor_of(stage, predecessors)
    if previous is None:
        return None, None
    if previous not in histories:
        raise HandoffRefusal(
            f"stage {stage} inherits from {previous}, whose history location is"
            " not declared here"
        )
    path, verified = histories[previous]
    if not Path(path).is_file():
        raise HandoffRefusal(f"{path} does not exist; stage {previous} has no history")
    found = digest(Path(path).read_bytes())
    if found != verified:
        raise HandoffRefusal(
            f"stage {previous}'s history is {found}, not the verified {verified}"
        )
    return Path(path), found


def archived_export(stage, *, adapter: Adapter, root=None):
    """Where a finished stage's own export is read from, keyed by stage."""
    if stage not in adapter.names:
        raise HandoffRefusal(f"unknown stage: {stage!r}")
    harness = adapter.harness_of(stage, root)
    recorded = harness / "producer-input-manifest.json"
    if not recorded.is_file():
        raise HandoffRefusal(
            f"stage {stage} is not launched; {recorded} does not exist, so there"
            " is no launch to read an archive from"
        )
    launch = json.loads(recorded.read_bytes())["launch"]
    if not launch["launched"]:
        raise HandoffRefusal(
            f"stage {stage} is not launched; it has no archived export"
        )
    path = (
        harness
        / "archive"
        / launch["launched_at"]
        / adapter.layout.work_dir
        / adapter.stage(stage).export_file
    )
    if not path.is_file():
        raise HandoffRefusal(f"{path} does not exist; stage {stage} exported nothing")
    return path


def checked_export(export_path, history_path, *, verified_export, verified_history):
    """One stage's export, checked three ways before it crosses the boundary.

    Against its own verified digest, against a fresh replay of the history
    beside it, and the history against its own verified digest. Any one of the
    three failing means the next stage would be handed something other than
    what this stage actually produced.
    """
    import malleus.compiler as api

    export_path, history_path = Path(export_path), Path(history_path)
    if not export_path.is_file():
        raise HandoffRefusal(f"{export_path} does not exist; there is no export")
    data = export_path.read_bytes()
    if digest(data) != verified_export:
        raise HandoffRefusal(
            f"the export is {digest(data)}, not the verified {verified_export}"
        )
    if verified_history is not None and (
        digest(history_path.read_bytes()) != verified_history
    ):
        raise HandoffRefusal("the history beside the export is not the verified one")
    replayed = (
        api.KnowledgeChangeHistory.reopen(history_path).replay().graph.export_records()
    )
    if json.loads(data) != replayed:
        raise HandoffRefusal(
            "the exported graph is not what the history replays to; the next"
            " stage would be handed something the ledger does not support"
        )
    return data


def archived_work(stage, name, *, adapter, root=None):
    """One named file of a finished stage's archived work directory."""
    export = archived_export(stage, adapter=adapter, root=root)
    path = export.parent / name
    if not path.is_file():
        raise HandoffRefusal(f"{path} does not exist; stage {stage} wrote no {name}")
    return path


def replay_receipt(history_path, *, verified=None):
    """The replay receipt identity of one history, optionally checked."""
    import malleus.compiler as api

    identity = (
        api.KnowledgeChangeHistory.reopen(Path(history_path)).replay().receipt.identity
    )
    if verified is not None and identity != verified:
        raise HandoffRefusal(
            f"the replay receipt is {identity}, not the verified {verified}"
        )
    return identity
