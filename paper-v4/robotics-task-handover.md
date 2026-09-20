# Malleus Robotics: independent task handover

Author direction: 2026-09-06. This establishes a separate, ongoing task that can
design, implement and grow the robotics/simulation demonstration. It replaces
the internal research-agent arrangement, not its retained findings.

## Purpose

Maintain an agent's accepted model of its environment. The central question is:
"Show me what it believed, what supported that belief, and what justified
changing it." The intended proof sequence is Shop, existing marine PDF, then
robotics/simulation. A successful simulation would add changing observations
and a justified accepted-state revision, not simply another source format.

Paper owns the manuscript and scientific claim integration. Robotics owns its
experiment, adapters, domain model/history choice, tests and demonstration.
Core owns the protocol/runtime and Small Shop. Re-entry owns the generic
finding-to-proposal work, starting with its bounded Shop slice. No task may
silently take another's files or declare another's unfinished result complete.

## Read before choosing a fixture

These files currently live in the shared paper checkout and may not be in a
new worktree. Read them from /Users/luis/Projects/malleus-dev/paper-v4/ and
retain a task-local handover copy under the robotics-owned research directory.
Do not edit their originals.

1. robotics-proof-plan.md: experiment meaning, proposed episode, evidence
   isolation, ontology/history distinctions, queries, controls and nonclaims.
2. robotics-assets-shortlist.md: newer asset-based recommendation and actual
   source interfaces, access, licenses and integration limits.
3. robotics-simulation-recon.md: framework comparison and prior art.
4. reentry-paper-plan.md: the paper's last verified prerequisite result, not a
   current capability guarantee. Obtain the latest exact status from re-entry.
5. manuscript-v4-working.md: the completed document claim and evidence limits.

## Findings to carry forward

The latest research recommends Gazebo Harmonic's shipped
examples/worlds/logical_camera_sensor.sdf on supported Linux amd64 for the
smallest adapter. It contains primitives and a logical camera; the inspected
source reports model names, relative poses, simulation time and frame metadata.
It checks the frustum, not occlusion. A hidden-behind-an-object episode is not
supported by that sensor. The proposed minimum is observe A, out of view, then
observe B. Simulation execution is untested; no binary or dataset was downloaded.

Webots camera_recognition.wbt is the alternative if occlusion is required.
Recognition is idealized, not learned perception. Asset licenses differ, and
native compatibility with the inspected macOS 15.7.9 arm64 host is unverified.
The smaller recorded option is robomimic Lift PH low_dim_v15.hdf5, listed as
21.1 MB, but its object states are privileged simulator data and its sample-time
meaning needs verification. TUM RGB-D walking_static supplies timestamped
physical RGB-D recordings but no ready persistent object-detection stream.
All exact links and qualifications are in the shortlist. Recheck moving sources
and inspect actual chosen bytes before treating documented shape as observed.

Framework, episode and producer condition are not selected. Present the smallest
concrete implementation recommendation to Luis before committing to a simulator
or taking on downloads/installation. This is not authority to buy hardware or
cloud compute. The separate task is an implementation owner, not another report
that ends without identifying the next executable slice.

## Essential experiment distinctions

Admit seed identities and frame definitions with their origin. Retain observations
with exact evidence, time, frame, units and sensor/configuration identity.
Version qualified assessments, such as last-observed location, preserving their
predecessors. The latest assessment need not equal the current world state.
Missing detection is not proof of absence. Never supply privileged scene state
to the producer as though the robot observed it. Name any idealized sensor.

Keep intended actions, issued commands and observed outcomes distinct. A source
import or scripted supersession is updating, not necessarily semantic re-entry.
For re-entry, a finding about accepted state must initiate the next bounded
proposal through ordinary admission. Query repair is a different intervention.

The first meaningful slice should retain the evidence and proposal/refusal,
admit normally, dispose/reopen/replay, query old and current assessments with
supporting evidence, prove unchanged records are preserved, and test stale
base, mismatched evidence and a repeated satisfied request. Separate exact
knowledge replay from simulator or image reproducibility. No safety, perception,
control, truth, autonomous exploration or physical-world result is inherited.

## Ownership and coordination

Work in the new task's own checkout. Own research/robotics_simulation/** there,
including a short master plan, raw progress log, reproducible configuration,
tests and eventual demo. Do not mutate Core, Small Shop, paper-v4 originals,
other tasks' worktrees or shared main. Coordinate any broader path first.
Use public Malleus interfaces. Send Core only a missing generic capability with
an exact pinned runtime and minimal reproducer. Keep robotics policy, data,
schema, assessment logic and evaluation in this task.

Coordination tasks on host local:

- Paper, Draft lean Malleus arXiv paper: 01a063a6-2b96-7cf1-bb53-1df3c6df63ba.
- Malleus Core: 01a02f71-fec6-7382-9c68-c3efd3dba5d4.
- Malleus-semantic-reentry: 01a05f67-22dc-7043-8174-c24ee9ccb09f.

Use TDD for implementation where possible. Keep the first slice small, declare
dependencies in configuration, preserve refusals, and record author choices.
Do not silently turn research recommendations into accepted decisions. Do not
wait for unrelated Core/Shop work; identify one actual missing seam if blocked.
Return exact result coordinates and bounded claims to paper when a slice passes.
Commits/integration must follow task and Core coordination; no main push is
authorized by this handover.

## Current paper boundary

The review draft is four pages and 2,201 words. It reports two document captures,
thirty retrospective queries and model-assisted review, including failures.
Its eight/eleven covered-question counts are not robot evidence or accuracy
rates. The author likes this abstract and wants the simulation to strengthen
the eventual paper. Keep that ambition separate from a result not yet produced.
