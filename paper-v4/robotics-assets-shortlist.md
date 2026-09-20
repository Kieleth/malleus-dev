# Robotics assets shortlist

Date: 2026-09-06. Status: source inspection and design only. No download,
installation, simulator run or dataset binary inspection. Framework and episode
remain Luis's choices. This takes the complete robotics proof, simulator recon
and re-entry plans as its handover. It changes no Shop, PDF or paper evidence.

For the smallest adapter, recommend **Gazebo Harmonic's shipped logical-camera
world, on Linux, with a frustum-only observation episode**. This asset-based
recommendation may supersede the earlier framework-level Webots preference only
if Luis selects it. It does not reproduce an occlusion experiment. Webots remains
the stronger candidate when occlusion is required.

## Ranked assets

### 1. Gazebo: `logical_camera_sensor.sdf`

The inspected [shipped world](https://github.com/gazebosim/gz-sim/blob/gz-sim8/examples/worlds/logical_camera_sensor.sdf)
contains a box, ground plane, static logical camera and primitive geometry.
Physics, LogicalCamera, UserCommands and SceneBroadcaster systems are already
configured. There are no external model or texture references. The camera
publishes on `/logical_camera` at a configured 10 Hz. Source blob inspected:
`a67d7ac6fc423846b0f293960d9e9e343ebae76c`, not a selected runtime pin.

The [message definition](https://github.com/gazebosim/gz-msgs/blob/gz-msgs10/proto/gz/msgs/logical_camera_image.proto)
contains model names, camera-relative model poses, camera pose and a header.
The [sensor implementation](https://github.com/gazebosim/gz-sensors/blob/gz-sensors8/src/LogicalCameraSensor.cc)
adds simulation time, `frame_id` and sequence metadata. It tests whether model
origins lie within the frustum. It does not test occlusion and can report an
object hidden behind another object. This is an idealized sensor, with no
recognition-accuracy claim.

Smallest proposed episode: retain one `box` detection at A, a later sample in
which it is outside the frustum, then a detection at B. The evaluator scripts
the changes; exact placements and sample steps remain unselected. Three
observation checkpoints suffice for the first claim. The middle checkpoint
does not justify B or absence. This exercises last-observed assessment revision;
it does not establish that the agent actively chose a sensing action.

Access: public source; [Apache 2.0](https://github.com/gazebosim/gz-sim/blob/gz-sim8/LICENSE).
Target Ubuntu amd64, the [officially supported Harmonic platform](https://gazebosim.org/docs/harmonic/install/).
macOS/ARM are best-effort. The inspected sensor path computes geometry without
an image renderer, so a server-only run is the proposed minimum, still untested.
Its [system implementation](https://github.com/gazebosim/gz-sim/blob/gz-sim8/src/systems/logical_camera/LogicalCamera.cc)
publishes only when running with subscribers and warns that rewind is unsupported.
Start recording before advancing the episode; use fresh runs for reproduction.
Require and validate nonempty frame metadata rather than guessing it.

### 2. Webots: `camera_recognition.wbt`

The [shipped scene](https://github.com/cyberbotics/webots/blob/master/projects/samples/devices/worlds/camera_recognition.wbt)
already contains a camera-equipped robot and recognizable objects. Its
[controller](https://github.com/cyberbotics/webots/blob/master/projects/samples/devices/controllers/camera_recognition/camera_recognition.c)
rotates the robot and prints model, recognition ID, relative position and
orientation, image position and size. It samples every 64 ms. The
[Recognition contract](https://github.com/cyberbotics/webots/blob/master/docs/reference/recognition.md)
provides configurable occlusion checks. Preserve IDs within one run; the model
string is a category, not a globally unique object identity.

Proposed derivative: stop the demonstration's rotation, retain one identified
object and add a declared occlude/move/reveal schedule. This needs an observation
exporter, simulation timestamps and a separate evaluator Supervisor. Those are
new experiment work, not capabilities already implemented by the sample.

The controller is Apache 2.0, but the world's objects are not uniformly so.
[Can.proto](https://github.com/cyberbotics/webots/blob/master/projects/objects/drinks/protos/Can.proto)
explicitly permits use only with Webots and references textures. Follow the
[per-asset licensing rule](https://github.com/cyberbotics/webots/blob/master/docs/guide/webots-license-agreement.md);
do not transplant these models into Gazebo or MuJoCo. Webots can fetch assets
on demand, so freeze/cache dependencies in configuration before reproduction.
[Asset access](https://www.cyberbotics.com/doc/guide/installation-procedure?version=develop).
Linux Xvfb and graphics requirements, plus unverified native compatibility with
this macOS 15.7.9 arm64 host, remain as recorded in the simulator recon.

### 3. robomimic: smallest recorded simulation alternative

[Lift PH `low_dim_v15.hdf5`](https://huggingface.co/datasets/robomimic/robomimic_datasets/tree/main/v1.5/lift/ph)
is listed at 21.1 MB, smaller than the 106 MB
[`test_v15.hdf5`](https://huggingface.co/datasets/robomimic/robomimic_datasets/tree/main/test)
example. The official dataset card declares MIT. These are public individual
files, not a requirement to acquire the full collection.

The [documented HDF5 structure](https://robomimic.github.io/docs/datasets/overview.html)
groups episodes under `data/demo_*`, with `obs`, `next_obs`, `actions`,
`states`, and environment metadata; robosuite episodes retain MJCF model XML.
Use one episode and exact HDF5 dataset/index locators after inspecting the chosen
binary. The schema does not promise timestamp arrays. Preserve sequence indices;
derive simulation time only from verified environment timing metadata, with its
derivation retained. Low-dimensional object state is privileged simulator data,
not evidence that an object was detected or visible.

The 106 MB example is the candidate for existing image observations; the
[tutorial](https://robomimic.github.io/docs/tutorials/dataset_contents.html)
documents observation playback and reconstruction with robosuite 1.5.1. It is
downloaded by the [test helper](https://github.com/ARISE-Initiative/robomimic/blob/master/robomimic/utils/test_utils.py),
not present in the current GitHub `tests/assets` tree despite the documentation's
packaging wording. This helper must not become an undeclared runtime download.

HDF5 inspection needs no simulator, on macOS or Linux. Rerendering requires the
matching robosuite/MuJoCo stack and a rendering backend. The current
[dataset registry](https://github.com/ARISE-Initiative/robomimic/blob/master/robomimic/__init__.py)
does not supply precomputed image links for the simulation task datasets.
Object identities/assessments from images still need a declared interpretation
method. Thus this is a compact recorded-data probe, not the first recommendation
for the intended visibility boundary.

### 4. TUM RGB-D: recorded physical sensor alternative

[`fr3/walking_static`](https://cvg.cit.tum.de/data/datasets/rgbd-dataset/download)
is listed as a 24.83-second, 0.48 GB sequence with moving people and a mostly
stationary camera. It is a single TGZ or ROS bag, not a simulator world. The
[file format](https://cvg.cit.tum.de/data/datasets/rgbd-dataset/file_formats)
provides timestamped RGB PNGs, registered 16-bit depth PNGs, calibration and
separate camera ground-truth trajectories. Zero depth means missing data.
The [current dataset license](https://cvg.cit.tum.de/data/datasets/rgbd-dataset)
is CC BY 4.0 unless otherwise stated.

Read a small consecutive RGB-D window after choosing the source episode;
retain filename/timestamp locators and freeze RGB/depth association rules.
No simulator or GPU is required to read these files. The documented format
provides no persistent object-instance detection stream. A detector or declared
human annotations would add work and change the producer condition. Camera
ground truth remains evaluator-only. This provides recorded change and
occlusion, not interactive sensing.

## Smallest Malleus boundary

The adapter is an adopter-side mapping into existing concepts, not a new public
API. The current [public-path Shop fixture](/Users/luis/Projects/malleus-dev/research/ontology_driven_kg_realization/experiments/small_shop/public_population/README.md)
demonstrates source-bound population, admission, history, replay, query and
provenance, while explicitly excluding a stable plan wire format and semantic
re-entry. The robotics profile must be checked against a selected Core cut.

1. **Source/evidence:** persist an immutable sensor message before interpretation.
   Bind run, sensor, sample time, coordinate frame, units and configuration;
   identify exact bytes and a field/index locator. The simulator's mutable object
   table, control services, whole-state snapshots and evaluation labels stay
   outside producer access. The narrow published idealized sensor is the only
   simulator-derived observation channel.
2. **Typed proposal:** bind the accepted base and source evidence to one qualified
   last-observed location assessment. Preserve observations and supersede the
   previous assessment explicitly. Missing data, unknown identities or unsupported
   conclusions produce a declared refusal, not filled-in values.
3. **Admission/history:** use ordinary contract/profile checks and retain the
   disposition and prior record. No direct graph mutation or assumed truth check.
4. **Replay/query:** reconstruct from retained evidence and accepted history.
   Return old/current assessments, observation times, supporting locators,
   supersession and unchanged records. Compare the same outputs with a simple
   versioned table plus observation log; test stale base, no detection, mismatched
   evidence, hidden-state leakage and repeated-request no-op.

Offline recordings can support accepted-state-triggered proposal/re-entry tests,
but cannot demonstrate acquisition of a new observation in response to an agent
request. Scripted playback, observation import and supersession alone do not
establish re-entry. Actual re-entry still requires a finding about accepted state
to initiate another bounded proposal through ordinary admission. Knowledge replay
from fixed bytes is separate from physics or pixel reproduction.

Luis's decisions: select Gazebo/frustum-only versus Webots/occlusion or a recorded
probe; select the observation/producer condition; approve the exact episode and
runtime/profile before implementation. The Shop slice remains unchanged. No
perception, safety, control or robotics-novelty claim follows from this shortlist.
