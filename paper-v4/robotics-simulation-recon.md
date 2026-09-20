# Robotics simulation reconnaissance

Date: 2026-09-06. Status: research and proposal only. No simulator installed,
assets downloaded, experiment run, framework selected, or result claimed.

The framework-level comparison favors **Webots**, subject to Luis choosing the
framework and experiment scope. Its separate robot sensor and Supervisor
interfaces suit a small test of accepted environmental knowledge. MuJoCo is the
strongest alternative when minimal runtime dependencies matter more than packaged
observation semantics. The integration judgments below are engineering estimates,
not measured results.

Subsequent [asset inspection](robotics-assets-shortlist.md) recommends Gazebo's
shipped primitive logical-camera world for the narrower Linux, frustum-only
episode. That recommendation may supersede this Webots preference only if Luis
selects it. It does not cover occlusion. Webots remains the occlusion candidate;
neither framework is selected or installed.

The intended evidence chain is **Shop → existing marine PDF → robotics
simulation**. Robotics replaces extra-PDF probes as the next breadth direction;
it preserves the existing PDF evidence. The immediate re-entry work remains the
source-backed Shop `e4` quantity 1 to `e7` quantity 2 proposal, admission,
replay, and repeated-request no-op slice. Robotics neither expands nor blocks
that slice. The common question is: “Show me what it believed, what supported
that belief, and what justified changing it.” Here, “believed” means accepted
records with their qualifications, not access to a model's internal beliefs.
Core semantic re-entry remains pending. The simulator APIs establish candidate
integration points, not a ready Malleus integration seam.

## Framework comparison

### Webots: recommended for the proposed scene

Established research use is concrete: the [SoccerSim paper](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2022.915322/full)
reports a Webots-based RoboCupJunior environment; the [RoboCup Humanoid League](https://humanoid.robocup.org/hl-2021/v-hsc/)
also identifies Webots as its virtual competition simulator. These establish
research use, not suitability or accuracy for Malleus.

A Python robot controller can obtain camera Recognition objects, while a
separate Supervisor can modify scene fields, including object placement, and
reload worlds. Recognition supplies an idealized structured observation
interface: range and occlusion settings govern visibility, and objects need
explicit recognition metadata. It is not a learned perception system. Its
occlusion setting must be explicit; disabling occlusion permits recognition
through obstacles. [Camera API](https://github.com/cyberbotics/webots/blob/master/docs/reference/camera.md),
[Recognition semantics](https://github.com/cyberbotics/webots/blob/master/docs/reference/recognition.md),
[Supervisor API](https://github.com/cyberbotics/webots/blob/master/docs/reference/supervisor.md).

The [requirements](https://github.com/cyberbotics/webots/blob/master/docs/guide/system-requirements.md)
list macOS 12 to 14 and Ubuntu 22.04/24.04, with Linux packages for x86-64.
Local read-only checks found macOS 15.7.9, build 24G830, arm64. Therefore native
execution on this host remains unverified. Official [installation documentation](https://github.com/cyberbotics/webots/blob/master/docs/guide/installation-procedure.md)
provides Ubuntu Docker images with Xvfb for headless execution. A Linux x86-64
reproduction target does not establish native Linux arm64 support or equivalent
graphics behavior in a Mac container.

Cost: moderate. Own one world, a robot observation exporter, an evaluator
Supervisor, and a Malleus adapter. ROS is unnecessary for this experiment.
Reproducibility requires synchronized controllers, one physics thread, fixed
seeds, deterministic controllers, and full reloads. Versions, OS and graphics
configuration can affect equality. [Webots reproducibility guidance](https://www.cyberbotics.com/doc/guide/modeling?version=omichel%3Amaster).

### MuJoCo: smallest runtime, more observation design

The primary [dm_control paper](https://arxiv.org/abs/2006.12983) describes
MuJoCo-backed control benchmarks, locomotion and manipulation tasks. Its
documented interfaces include MJCF scene definitions, explicit physical
stepping, native Python bindings and sensors. An experiment can modify joint
state and recompute derived quantities, but must respect simulation-stage
semantics: changing positions does not automatically refresh every derived
value. [Overview](https://mujoco.readthedocs.io/en/stable/overview.html),
[Python API](https://mujoco.readthedocs.io/en/stable/python.html),
[state consistency](https://mujoco.readthedocs.io/en/stable/computation/index.html#consistency-in-mjdata).

Native binaries cover macOS and Linux on x86-64 and arm64. Physics stepping
can run without rendering; Linux rendered sensors can use EGL or OSMesa.
[Platform and rendering documentation](https://mujoco.readthedocs.io/en/3.7.0/programming/).
Cost: low for a CPU scene using declared range observations, higher for the
proposed object-identity and visibility interface. Exporting unrestricted body
positions would collapse the observation/evaluator boundary. A custom adapter
must declare which sensor outputs support identity and location assessments.

Exact simulation reproduction requires the same version and architecture and
all required integration state, including warmstarts when needed. Cross-OS
trajectory equality is not guaranteed. [Reproducibility](https://mujoco.readthedocs.io/en/stable/computation/index.html#reproducibility).

### Gazebo Harmonic: strongest ecosystem fit, larger integration surface

Research use includes the [DARPA SubT virtual competition](https://www.openrobotics.org/blog/2021/9/27/darpa-subt-final-competition)
and a primary [cave-world study](https://arxiv.org/abs/2004.08452). These concern
historical Gazebo environments, not validation of a current Harmonic setup.

Harmonic offers SDF worlds, sensor systems and transport. The documented
LogicalCamera reports objects in its frustum. Subsequent inspection of the
[sensor source](https://github.com/gazebosim/gz-sensors/blob/gz-sensors8/src/LogicalCameraSensor.cc)
confirms a model-origin frustum test, without occlusion testing. UserCommands
exposes entity creation, removal and pose
changes. [LogicalCamera](https://gazebosim.org/api/sim/8/classgz_1_1sim_1_1systems_1_1LogicalCamera.html),
[UserCommands](https://gazebosim.org/api/sim/8/classgz_1_1sim_1_1systems_1_1UserCommands.html).

Official support targets Ubuntu Jammy/Noble amd64; macOS and ARM receive
best-effort support. The macOS guide also warns of GUI instability.
[Supported platforms](https://gazebosim.org/docs/harmonic/install/),
[macOS caveats](https://gazebosim.org/docs/harmonic/getstarted/).
Server-only execution is available; headless rendered sensors use EGL with
OGRE2, retaining renderer/driver requirements. [Headless rendering](https://gazebosim.org/api/sim/8/headless_rendering.html).
Cost: highest of these three for this scene because world systems, transport
messages and process synchronization add integration work. Pin the library
collection, physics engine, sensor plugins and renderer. The cited sources do
not establish byte-identical cross-platform trajectories.

## Proposed smallest experiment

Use one stationary inspection robot, one identifiable crate, two marked bays
and an occluder made from simple primitives. The evaluator relocates the crate
between observations. No navigation, grasping, autonomous control or downloaded
warehouse assets are needed. The simulator owns physical stepping and sensors;
Malleus owns typed proposals, admission, accepted history, replay and provenance.

Keep four meanings separate. An observation is the exact sensor payload with
run, sensor, step, timestamp, frame and units. An assessment is a qualified
interpretation, such as “crate observed within bay B at step 30”, citing that
payload and the declared bay mapping. An intended inspection is a request.
Its outcome requires a subsequent observation. The first slice need not
populate action records or execute an agent request.

The producer receives only allowlisted observation bytes, the declared sensor
contract, immutable accepted base and permitted amendment. Evaluator-only
artifacts contain complete simulator state, relocation commands and scoring
labels. Webots Recognition is explicitly an idealized sensor oracle restricted
by the configured observation channel. Its use supports no perception-accuracy
claim. Test that hidden-state canaries never enter producer inputs or evidence.

Freeze this sequence before execution:

1. Observe the crate in A; admit a qualified location assessment with evidence.
2. Occlude and relocate it to B. An empty recognition result supports
   “not observed in this sample”, not “absent” or “now in B”. Preserve the last
   observation's time qualification and expose lack of fresh support.
3. Reveal B and record a new observation. A query over accepted assessments and
   admitted observations identifies the bounded revision need. Give that
   state-pinned finding to the producer; retain its amendment or refusal.
4. Apply ordinary admission, preserve the previous assessment, reopen and
   replay. Repeat the satisfied request and check that no duplicate amendment
   is admitted.

Step 3 is semantic re-entry only if the accepted-state finding actually
initiates another proposal through the ordinary gate. Merely importing a later
sensor sample or applying a scripted supersession establishes an update.
Changing query code establishes neither. Record which path actually executes.

## Evaluation and approval boundary

Testable claim: this episode preserves qualified accepted assessments and
their evidence across a source-supported revision, refusals and replay.
Queries must return the last supported location and observation time, current
versus historical assessments, the exact evidence and decision justifying the
change, and the result of repeating the satisfied request.

Compare with an ordinary SQLite observation log plus versioned assessment
table, transactions and source references, using identical observations and
candidate proposals. Measure retained answers, provenance completeness,
refusals, duplicate handling and reconstruction, and document the custom checks
each path needs. This baseline may match Malleus; no superiority follows from
design alone.

Negative cases require executable guards and tests: missing required frame or
timestamp, unknown evidence digest, stale accepted base, unsupported relocation,
empty visibility mistaken for absence, duplicate satisfied request, and an
intended action mistaken for success. Admission alone does not verify an
assessment's truth; independently check fixture evidence support and retain
failures.

After approval, capture dependencies, simulator/image digests, world bytes,
controller configuration and runtime setup in reproducible configuration.
Freeze sensor evidence separately: Malleus ledger replay from retained bytes
must be distinguished from rerunning physics. This reconnaissance ran neither.
No real-time, safety, SLAM, physical-world validation, robotics novelty or
correctness-of-belief claim is proposed. Luis chooses framework and scene scope
before implementation.
