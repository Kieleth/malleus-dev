"""Write one producer workspace and record what it was given.

The mechanism: fill a stage's procedure text, write the declared files into the
workspace, run the exposure check over every byte of it plus the dispatch
prompt, assemble the input manifest, and write the harness copies beside it.

Three rules the mechanism holds and an adapter cannot opt out of:

- A stage that has launched is not rebuilt. Its workspace holds a producer's
  own work and its manifest is that run's record.
- A rebuild never erases a launch. An existing launch record is carried forward
  verbatim.
- A stage's procedure is refused while it still carries a substitution token,
  so a stage added later cannot inherit a neighbour's filename or identity by a
  substitution that missed.

What the adapter owns and this module never reads: the procedure and spawn
texts, the declared inputs and their bytes, and the extra manifest fields that
say what this run is.
"""

from __future__ import annotations

import json
import re

from .digests import digest, indented


class BuildRefusal(ValueError):
    """The stage has launched. Its workspace is a producer's, not the builder's."""


TOKEN = re.compile(r"__[A-Z][A-Z0-9_]*__")
"""The shape of a substitution token, so an undeclared one is caught too."""


def procedure_for(stage, template, tokens):
    """One stage's procedure, with every stage-dependent string filled in.

    Refuses to return a text that still carries a token. It refuses on any
    token of the declared shape and not only on the ones it was handed, because
    the defect this exists for was a procedure copied from a neighbour whose
    substitution list did not mention the filename that stayed behind: it told
    the producer to write over the input it had just been given.
    """
    text = template
    for token, value in tokens.items():
        text = text.replace(token, value)
    left = sorted(set(TOKEN.findall(text)))
    if left:
        raise ValueError(f"stage {stage}'s procedure still carries {', '.join(left)}")
    return text


def placeholder(fill_with, *, filled_after):
    """One input that does not exist until an earlier stage has produced it.

    It says so in its own bytes, so a workspace built before that stage cannot
    be mistaken for one built after it.
    """
    return (
        json.dumps(
            {"PLACEHOLDER": True, "filled_after": filled_after, "fill_with": fill_with},
            indent=2,
        ).encode()
        + b"\n"
    )


def launched_record(harness):
    """The launch this stage already records, or None."""
    recorded = harness / "producer-input-manifest.json"
    if not recorded.is_file():
        return None
    launch = json.loads(recorded.read_bytes()).get("launch") or {}
    return launch if launch.get("launched") else None


def launch_seed(harness, spawn_message_path):
    """A fresh launch record, or the recorded one carried forward verbatim.

    The record belongs to the run, not to the builder, so an existing launch is
    never overwritten by a rebuild.
    """
    recorded = launched_record(harness)
    if recorded is not None:
        return recorded
    return {
        "launched": False,
        "launched_at": None,
        "spawn_message": spawn_message_path,
        "dispatch": "THE_SPAWN_MESSAGE_VERBATIM_WITH_THE_ABSOLUTE_WORKSPACE_PATH",
    }


def write_workspace(workspace, files):
    """Write every declared file, and the producer's own empty work directory."""
    for relative, (_, data) in files.items():
        target = workspace / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)


def declared_inputs(report, *, packet_target, packet_source_id):
    """Every input as its own record, with the packet's identity on the packet.

    The packet's entry already declares its path, role, byte count and digest,
    so the identity the evidence is retained under is added to that record
    rather than to a second one that could disagree with it.
    """
    return [
        {
            "path": item["path"],
            "role": item["role"],
            "bytes": item["bytes"],
            "sha256": item["sha256"],
            "in_workspace": item["in_workspace"],
            **(
                {"source_id": packet_source_id}
                if packet_source_id is not None and item["path"] == packet_target
                else {}
            ),
        }
        for item in report["files"]
    ]


def build(
    stage,
    *,
    run_id,
    schema,
    harness,
    harness_name,
    workspace,
    root,
    report,
    status,
    packet_target,
    packet_source_id,
    message,
    procedure,
    extras,
):
    """Assemble one stage's input manifest and write the harness copies.

    The caller has already refused a launched stage, cleared the workspace,
    written the declared files and run the exposure check: those four are the
    steps that touch a producer's own directory, and they stay with the adapter
    that owns the layout. What is here is the record.

    ``harness`` and ``workspace`` are paths the caller resolves, never derived
    here, so an adapter can build into a throwaway tree by naming one.
    """
    manifest = {
        "schema": schema,
        "run_id": run_id,
        "stage": stage,
        "status": status,
        "workspace": str(workspace.relative_to(root)),
        "declared_inputs": declared_inputs(
            report,
            packet_target=packet_target,
            packet_source_id=packet_source_id,
        ),
        "spawn_message_is": "THE_DISPATCH_PROMPT_NOT_A_WORKSPACE_FILE",
        "receipt_path": f"producer/{harness_name}/producer-input-receipt.json",
        "receipt_written": "AT_LAUNCH_NOT_NOW",
        "launch": launch_seed(harness, f"producer/{harness_name}/spawn-message.md"),
        "exposure_report": report,
        **extras,
    }
    harness.mkdir(parents=True, exist_ok=True)
    (harness / "producer-input-manifest.json").write_bytes(indented(manifest))
    (harness / "spawn-message.md").write_bytes(message)
    (harness / "PROCEDURE.md").write_bytes(procedure.encode())
    (harness / "exposure-report.json").write_bytes(indented(report))
    return manifest, report


def input_digests(files):
    """Every declared file's digest, by path, for a caller that compares."""
    return {relative: digest(data) for relative, (_, data) in files.items()}
