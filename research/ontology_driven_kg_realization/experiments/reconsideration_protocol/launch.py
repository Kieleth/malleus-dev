"""The checks a launch runs before it prints a prompt, as separate refusals.

A launch prints a dispatch prompt and dispatches nothing. Before it prints
anything it re-reads every declared input and refuses if one byte differs from
the frozen manifest, refuses a file in the workspace the manifest does not
declare, refuses a stage that is still a template, refuses a stage already
launched, refuses when a receipt already exists, and refuses when the stage's
packet record declares a source id the frozen procedure's anchor line does not
carry, so the identity the run records and the identity the producer types
cannot drift apart.

These are exported as separate functions rather than as one call, because the
two consumers compose them differently and record different receipts. One
places the predecessor's history into the producer's directory at launch and
records what it placed; the other has its builder seed the history and its
launch verify the seed and refuse a leftover. One updates its run index here;
the other does not. A monolith would have to take both as options, which is
two adapters in one function.

A launch imports no Core of its own: it reads bytes and compares digests. The
producer's runner is the thing that needs a Core, and it pins its own.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from .adapter import PLACEHOLDER
from .digests import digest, indented


class LaunchRefusal(ValueError):
    """The prepared inputs are not what the manifest froze, or this already ran."""


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def refuse_unknown_stage(stage, stages):
    if stage not in tuple(stages):
        raise LaunchRefusal(
            f"unknown stage: {stage!r}; expected one of {sorted(stages)}"
        )


def refuse_not_launchable(stage, manifest, *, statuses=("FROZEN",)):
    """A template has inputs that do not exist yet and cannot be launched."""
    if manifest["status"] not in tuple(statuses):
        raise LaunchRefusal(
            f"stage {stage} is {manifest['status']}; a TEMPLATE has inputs that do"
            " not exist yet and cannot be launched"
        )


def refuse_already_launched(stage, manifest):
    if manifest["launch"]["launched"]:
        raise LaunchRefusal(
            f"stage {stage} is already recorded as launched at"
            f" {manifest['launch']['launched_at']}"
        )


def refuse_existing_receipt(receipt_path):
    if Path(receipt_path).exists():
        raise LaunchRefusal(f"{receipt_path} already exists; this stage already ran")


def checked_inputs(manifest, workspace, harness):
    """Every declared input, held to its frozen digest. Returns the receipt rows.

    The second value is the set of resolved workspace paths the closure check
    compares against, so the two never disagree about what was declared.
    """
    rows, declared = [], set()
    for item in manifest["declared_inputs"]:
        source = (
            Path(workspace) / item["path"]
            if item["in_workspace"]
            else Path(harness) / "spawn-message.md"
        )
        if not source.is_file():
            raise LaunchRefusal(f"{item['path']}: declared and not present")
        found = digest(source.read_bytes())
        if found != item["sha256"]:
            raise LaunchRefusal(
                f"{item['path']}: {found} is not the frozen {item['sha256']}"
            )
        if item["in_workspace"]:
            declared.add(source.resolve())
        rows.append({"path": item["path"], "role": item["role"], "sha256": found})
    return rows, declared


def refuse_undeclared_files(workspace, declared, *, work_dir):
    """The producer's own directory is excluded: an inherited history lives there.

    The closure check covers the declared inputs, which is everything the
    producer reads.
    """
    workspace = Path(workspace)
    present = {
        path.resolve()
        for path in workspace.rglob("*")
        if path.is_file() and work_dir not in path.relative_to(workspace).parts
    }
    for extra in sorted(present - declared):
        raise LaunchRefusal(
            f"{extra.relative_to(workspace)}: in the workspace and not declared"
        )


def declared_source_id(manifest, *, noun="packet"):
    """The identity this stage's evidence is retained under, from its own record.

    The builder writes it into the evidence's declared-input entry, which is
    that stage's packet record. A manifest frozen before the declaration
    existed carries none, and this returns None rather than inventing one.
    """
    found = [
        item["source_id"]
        for item in manifest["declared_inputs"]
        if item.get("source_id") is not None
    ]
    if len(found) > 1:
        raise LaunchRefusal(
            f"{len(found)} declared inputs carry a source id: {', '.join(found)};"
            f" one stage stages one {noun}"
        )
    return found[0] if found else None


def refuse_procedure_disagreement(procedure, packet_source_id, *, refuse_extra=False):
    """The record and the line the producer copies must say the same thing.

    Both have been checked against their frozen digests before this runs, so
    this compares two verified halves of one declaration rather than trusting
    either alone. ``refuse_extra`` also refuses an anchor line on a stage that
    declares no source id, which is a stage whose record and procedure disagree
    about whether there is evidence to retain.
    """
    if packet_source_id is not None:
        if f"--source-id {packet_source_id}" not in procedure:
            raise LaunchRefusal(
                f"the packet record declares {packet_source_id} and PROCEDURE.md"
                f" carries no `--source-id {packet_source_id}` on its anchor line"
            )
    elif refuse_extra and "--source-id" in procedure:
        raise LaunchRefusal(
            "this stage declares no source id and its procedure carries an anchor"
            " line; the two disagree about whether there is evidence to retain"
        )


def dispatch_of(harness, workspace, *, placeholder=PLACEHOLDER):
    """The spawn message with the one token filled by the absolute path."""
    spawn = (Path(harness) / "spawn-message.md").read_text()
    if placeholder not in spawn:
        raise LaunchRefusal(f"the spawn message carries no {placeholder}")
    return spawn.replace(placeholder, str(workspace))


def record(receipt, receipt_path, manifest, manifest_path, launched_at):
    """Write the receipt and stamp the stage manifest. The launch is now a fact."""
    receipt_path, manifest_path = Path(receipt_path), Path(manifest_path)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_bytes(indented(receipt))
    manifest["launch"]["launched"] = True
    manifest["launch"]["launched_at"] = launched_at
    manifest_path.write_bytes(indented(manifest))
    return manifest


def record_in_index(index_path, stage, paths, launched_at, *, root):
    """Keep a run index a true index after the launch moved two files.

    Writing the receipt and stamping the stage manifest changes two artifacts
    the index already names, so the index is updated here rather than left to
    go stale. It is the run's record from this point.
    """
    index_path, root = Path(index_path), Path(root)
    if not index_path.is_file():
        return None
    index = json.loads(index_path.read_bytes())
    for path in paths:
        index["artifacts"][str(Path(path).relative_to(root))] = digest(
            Path(path).read_bytes()
        )
    index["artifacts"] = dict(sorted(index["artifacts"].items()))
    index["producer"][stage]["launched"] = True
    index["producer"][stage]["launched_at"] = launched_at
    index["launched"] = True
    index["status"] = "LAUNCH_RECORDED"
    index_path.write_bytes(indented(index))
    return index


def verify_launched(receipt, harness):
    """Every launched file, held to its receipt's digest. Returns the mismatches.

    The receipt is the authority for what a producer was given, never what the
    builder would write today, so a file drifted to a later build is caught as
    drift rather than reported as a property of the record.
    """
    workspace = Path(receipt["workspace"])
    mismatched = []
    for item in receipt["inputs"]:
        source = (
            workspace / item["path"]
            if item["path"] != "spawn-message.md"
            else Path(harness) / "spawn-message.md"
        )
        found = digest(source.read_bytes()) if source.is_file() else None
        if found != item["sha256"]:
            mismatched.append(
                {"path": item["path"], "receipt": item["sha256"], "found": found}
            )
    return mismatched
