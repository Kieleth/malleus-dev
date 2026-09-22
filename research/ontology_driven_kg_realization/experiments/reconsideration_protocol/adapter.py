"""What an adapter declares so the reconsideration protocol can run over it.

Pure data. Nothing in this module reads a file, imports a consumer, or names a
domain. The protocol modules beside it hold the mechanism and take these
declarations as arguments; the per-call behaviour an adapter owns (its exposure
measure, its obligation selector, its record shapes) is passed at the call
site rather than hung on this object, so this stays a declaration and does not
become a service.

The seven groups an adapter fills:

1. ``stages``: the stage names in order, and for each one its workspace, its
   harness, the file it exports, the packet it is handed, where that packet is
   staged, the identity that packet is retained under, and which stage it
   continues. A stage graph need not be a chain: two stages may continue one
   predecessor, which is what a control arm is.
2. ``layout``: where the run keeps its artifacts, and what the producer's own
   directory and history file are called.
3. ``schemas``: the grammar strings this run's own records carry. Only the four
   records this package writes are named here; every other record a consumer
   writes is its own.
4. ``pin``: the Core export this run replays on, and this package's own bytes.
5. ``run_id`` and ``outcomes``: the run's identity, and the outcomes one
   declared interpretation may be reviewed with.

What is deliberately **not** here, measured against the two consumers that
exist (the Shop's structured-row harness and the marine document harness):

- The packet record's shape. One consumer's packet is one file with a row
  count; the other's is a list of files each with a role and where it was read.
  The mechanism stages bytes and checks digests; the record is the adapter's.
- The obligation subject grammar and its selector. One selects by declared
  event and entity type over an export; the other walks a compiled contract
  for subtypes and mixins and filters by reading block, unit and slot. Both
  hand their selector to ``obligations.bind``.
- The exposure measure. One refuses evaluator-only files, withheld passages and
  case identifiers; the other refuses any 60-character run the later document
  carries and the earlier one lacks. Both hand their measure to
  ``exposure.check``.
- The assessment rulebook. The two protocol files are different versions with
  different sections and different check ids. What this package holds is the
  ratification clause and the record tally.
- The run index. The two indexes share their launched-stage guard and nothing
  else.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


OUTCOMES = ("CORRECTION", "NO_CHANGE", "CONFLICT", "UNRESOLVED")
"""The four outcomes one declared interpretation may be reviewed with."""

EXPORT_GROUPS = ("entities", "events", "event_participations", "relations", "signals")
"""The record families a graph export carries."""

ROLES = ("DATA", "TEXT", "PRODUCER_OWN")
"""What a producer reads one workspace file as."""

BOUNDARY_GRAMMAR = "malleus.interpretation-review-boundary/private-v0"
"""Core's own boundary grammar, the one ``check_review_coverage`` parses."""

PLACEHOLDER = "<PRODUCER_WORKSPACE>"
"""The one token a spawn message must carry, filled with the absolute path."""


@dataclass(frozen=True, slots=True)
class Stage:
    """One stage of a run, and everything about it that is a name or a path."""

    name: str
    workspace: str
    harness: str
    export_file: str | None = None
    packet: str | None = None
    packet_target: str | None = None
    packet_source_id: str | None = None
    predecessor: str | None = None


@dataclass(frozen=True, slots=True)
class Layout:
    """Where one prepared run keeps its artifacts."""

    root: Path
    producer: Path
    packets: Path
    obligations: Path
    assessment: Path
    manifest: Path
    work_dir: str = "work"
    history_file: str = "history.jsonl"

    @property
    def history_path(self) -> str:
        return f"{self.work_dir}/{self.history_file}"


@dataclass(frozen=True, slots=True)
class Schemas:
    """The grammar strings of the four records this package writes."""

    producer_manifest: str
    receipt: str
    archive: str
    exposure_report: str


@dataclass(frozen=True, slots=True)
class RuntimePin:
    """The Core export a run replays on, and this package's own bytes.

    ``runtime`` is an export, never a checkout: ``markers`` are the files a
    runner reads to decide an export is the Core it is pinned to. That
    mechanism stays in each consumer's runner, which is staged standalone into
    a producer workspace and imports nothing from here.

    ``package`` is this protocol package's directory. It is tracked code in a
    checkout rather than an export, so a launch receipt records a digest over
    its module bytes and the run is reproducible from its receipt without the
    export carrying a copy. The marine consumer already pins Core the same way
    beside its markers, as ``core_package_sha256``.
    """

    core_commit: str
    runtime: Path
    package: Path
    markers: Sequence[str] = ()
    governance_head: str | None = None


@dataclass(frozen=True, slots=True)
class Adapter:
    """One consumer's declaration."""

    run_id: str
    stages: Sequence[Stage]
    layout: Layout
    schemas: Schemas
    pin: RuntimePin
    outcomes: Sequence[str] = OUTCOMES

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(stage.name for stage in self.stages)

    def stage(self, name: str) -> Stage:
        for stage in self.stages:
            if stage.name == name:
                return stage
        raise KeyError(name)

    @property
    def harnesses(self) -> dict:
        return {stage.name: stage.harness for stage in self.stages}

    @property
    def predecessors(self) -> dict:
        return {stage.name: stage.predecessor for stage in self.stages}

    def harness_of(self, name: str, root=None) -> Path:
        producer = self.layout.producer if root is None else Path(root) / "producer"
        return producer / self.stage(name).harness

    def workspace_of(self, name: str, root=None) -> Path:
        producer = self.layout.producer if root is None else Path(root) / "producer"
        return producer / self.stage(name).workspace
