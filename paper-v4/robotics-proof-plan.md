# Third proof: an agent's accepted environment model

Version: 0.2.0. Author direction: 2026-09-06.

Status update, 7 September 2026: the design below is historical. The separate
Robotics task has completed a recorded-observation visual pilot at 5727cc1.
Paper's robotics-evidence-assessment.md verifies its bounded retained results
and proposes an optional appendix. No main-paper integration is selected. This
is not the simulated action loop proposed below and does not establish robot
control, semantic Re-entry or an advantage over a transactional event log.

Ownership supersession: Luis explicitly requested a fully separate task that
can work, grow and build. Malleus Robotics takes implementation ownership in
its own worktree; the internal agent's completed research becomes handover
material. robotics-task-handover.md governs this transition. Paper retains
manuscript and claim integration, not the robotics implementation.

The intended sequence is **Shop → existing PDF → robotics simulation**. This
replaces extra PDFs as the next breadth direction, not the marine evidence or
the current re-entry task. Simulation is not yet a submission prerequisite.

## Question

“Show me what it believed, what supported that belief, and what justified
changing it.” Belief here means an explicitly accepted, qualified domain record,
not hidden model reasoning or guaranteed physical truth. Justification means
retained observations, the proposal and recorded admission grounds, not an
explanation invented after acceptance.

Proposed claim: one simulated agent maintains a small environment model from
identified observations. A discrepancy produces a bounded revision proposal.
Ordinary Malleus admission accepts or refuses it; replay recovers the accepted
states and evidence for their difference. This is an integration experiment,
not a new perception, navigation or robot-control method.

## Candidate episode, for author selection

One robot camera, one identified object, two locations. The robot observes the
object at A. The environment moves it while out of view. The latest accepted
observation still says A; the agent cannot learn B from private simulator state.
A later observation at B permits a proposal to supersede the location assessment.
No detection alone does not establish absence. The move is an experiment-driven
intervention, not an LLM action.

Relocation is the smallest bridge from Shop. Inspection is another candidate,
where evidence changes a qualified condition assessment, but needs a defensible
assessment method. Underwater physics, defect diagnosis and autonomous planning
are separate questions, not prerequisites for this first proof.

## Define the ontology and history meaning first

The simulator must not silently choose what a semantic ledger entry means.

| Kind | Proposed treatment | Boundary |
| --- | --- | --- |
| Seed | Admit identified object/sensor identities, frames and vocabulary with their origin. | Do not seed unobserved locations. |
| Observation | Retain sensor output, observation time, frame and acquisition/configuration identity. | Detection is not certain truth; missing detection is not absence. |
| Assessment | Version a last-observed location or qualified condition, linked to observations. Supersede explicitly. | Latest accepted assessment need not equal current world state. |
| Proposal/disposition | Bind change, base, evidence and admission grounds. | Structural acceptance does not prove epistemic correctness. |
| Action, if later added | Distinguish intention, command and observed outcome. | A command is not a successful effect. |

Proposed semantic unit: an assessment revision, not every simulation tick.
Observations remain historical evidence when an assessment changes. Simulation
time and admission order differ. The selected history profile must encode these
choices and be checked against an exact Core cut. No existing profile is declared
sufficient here. An append-only observation cannot silently become replacement.

An authored ontology is acceptable for a controlled protocol test. Model-authored
ontology acquisition would be a separate declared condition. Neither is silently
called a repeat of the question-withheld PDF experiment.

## Observation and evidence boundary

The simulator owns physics, interventions and sensor generation. The adapter
exposes only the declared observation channel. Ground truth stays evaluator-only.
If that channel returns perfect labels or poses, call it an idealized sensor;
claim no recognition accuracy. Retain observations, not just their interpretation.

One run manifest identifies simulator/scene/configuration, input schedule,
seed where applicable, observations, ontology/profile/policy, proposals,
dispositions, ledger/replay and queries. Exact knowledge replay is distinct
from repeatable physics or rendering. Do not assume cross-platform pixel or
floating-point identity; freeze comparison rules before reruns. High-volume
sensor data need not become individual semantic ledger records.

## Milestones

1. **Select the framework and episode.** Read robotics-simulation-recon.md.
   Luis chooses relocation versus inspection and idealized sensor versus a
   measured detector. No installation or scene implementation before selection.
2. **Freeze the experiment.** Define seed knowledge, observation access,
   assessment meaning, exact Core coordinate, producer inputs, unchanged
   queries, preservation checks and stopping rule. Verify the required public
   APIs. Send Core only a minimal generic capability reproducer if a gap exists.
3. **Prove observation isolation.** Build from declared dependencies. Test that
   hidden movement cannot update accepted knowledge and that the producer cannot
   access evaluator ground truth. A scripted mapping proves adapter integration,
   not model extraction.
4. **Exercise ordinary revision.** Establish A, retain B evidence, produce one
   amendment or refusal, admit normally, dispose and reopen/replay. Check changed
   and unchanged records. Repeating a satisfied request at the new head must not
   append a duplicate semantic change. Consume re-entry only after verifying its
   exact result and applicability, not on the strength of its design.
5. **Inspect every outcome.** Query history, current state and evidence. Keep
   failed/ambiguous proposals. Do not substitute evaluator-authored records for a
   failed model attempt. Separate deterministic conformance and model-produced
   arms; no best-of-attempt selection.
6. **Select paper claims.** Report measured behavior and integration limits.
   Keep PDF results unchanged. Simulation proves neither physical-world safety
   nor improved robot performance.

A later observation import or scripted supersession alone proves updating,
not semantic re-entry. For the latter, a finding about accepted state must
actually initiate the next bounded proposal through ordinary admission.

## Queries and controls

The demonstration must answer what was accepted at an earlier checkpoint, what
is accepted now, when its observation occurred, which exact sensor evidence
supports each assessment, what superseded it under which recorded checks, and
what remained unchanged or refused. Return records and evidence references, not
only prose. Checkpoint replay suffices; no general bitemporal API is presumed.

Controls: hidden movement, occlusion/no detection, stale base, mismatched evidence,
and repeated request. Ambiguous observations need explicit adopter policy, not a
presumed Core truth detector. Prefer natural refusals; synthesize only error
classes not exercised by the episode.

Compare with a simple last-observation table plus its raw log. An event log can
retain history too. Identify what typed admission, evidence binding or replay
adds in this implementation, without claiming to have invented robot memory.
No task-success or performance comparison is proposed.

## Prior art and ownership

KnowRob already links pose beliefs to perceptions or inference and represents
perceived and intended states. Its logs separate semantic events from high-volume
data. These are direct precedents. [Pose representation](https://www.knowrob.org/doc/object_pose_representation),
[logged experiences](https://www.knowrob.org/doc/reasoning_about_logged_experiences).
DynaMem studies dynamic spatial-semantic memory for robot manipulation; this
proposal does not reproduce or compete with its perception and task results.
[DynaMem](https://dynamem.github.io/).

Core owns Core and Shop. Re-entry owns its bounded Shop producer/design.
Malleus Robotics owns the simulation experiment, adapter, questions and evaluation
in its own worktree. Paper owns the manuscript and evidence integration. The
internal agent's research is complete and handed over. This ownership change
adds no prerequisites to Shop, selects no framework, rebinds no runtime and
creates no empirical claim.
