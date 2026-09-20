# Robotics evidence: optional paper addendum

7 September 2026. Paper inspection of Robotics commit
5727cc1b97aba1de6060684774c9bef4cf11032f, tree
b994c0cc2a906735270412976845c0a3ba535dd5. Not selected for the main manuscript.
The marine candidate, its runtime pin and all original claims remain unchanged.

## What this adds

This is a second source modality and an explicit assessment-update example.
The producer sees recorded camera prefixes rather than article text. The accepted
record retains its observation scope and supersedes an earlier assessment. A
fixed reader responds to accepted state, including after refusal. That supports
the question, "What did it accept, from which observations, and what changed?"

It is not yet the third simulation/action proof. The robot trajectories were
already recorded. No policy chose a motor command, no simulator executed one,
and no independent post-command observation closed an action loop. The same
proposals are replayed across storage arms, not generated independently by each.
The ontology and adapter are authored, not another ontology-acquisition study.

## Proposed paragraph, pending author selection

We also tested assessment updates from sampled prefixes of two released RoboMME
demonstrations. Six fresh-context Codex observers proposed qualified counts or
container descriptions, including two unknown responses. The same values were
replayed through typed mutable state, a transactional event log and Malleus,
under natural and injected stale-base conditions. All three stores reconstructed
equal final assessments in each of the four task-condition runs. Malleus and
the event log each rejected four stale-base attempts and accepted the same
values on fresh bases; mutable state accepted the stale attempts. Separate
model-assisted source reviews labelled four responses supported and the two
unknowns indeterminate. These labels are not human ground truth. This exploratory
pilot demonstrates retained visual assessments and controlled state updates,
not an advantage over the event log, improved perception or robot task success.
No live simulation or action execution occurred.

## One concrete witness

In PickXtimes, the natural prefixes end at native timesteps 0, 264 and 528.
Accepted counts are unknown, one and two. The fixed reader abstains, then returns
continue, then stop. Its rule is count greater than or equal to the explicit
target. Stop is a returned symbol, not a pressed button or achieved robot goal.

The injected-stale condition exposes the acceptance boundary:

| Attempt | Proposed count | Malleus disposition | Reader after attempt |
| --- | ---: | --- | --- |
| checkpoint-1, old base | 1 | REFUSED | abstain |
| checkpoint-1, fresh base | 1 | ACCEPTED | continue |
| checkpoint-2, old base | 2 | REFUSED | continue |
| checkpoint-2, fresh base | 2 | ACCEPTED | stop |

The proposal-value digest is identical within each stale/fresh pair. Refusal
preserves the preceding state digest. The transactional event log has the same
refusal behavior. These are deliberately injected base errors, not observed
perceptual errors or evidence that the mutable store caused a bad robot action.

For the last pair, the retained reader selections are:

```json
[
  {
    "event_id": "query:checkpoint-2:stale",
    "reader": {"answer": "continue", "disposition": "answered"},
    "state_sha256": "sha256:e57005a80423fcdadb5d1d4cecfc37ea2a82d541df24db79d9f657100083d77c"
  },
  {
    "event_id": "query:checkpoint-2:fresh",
    "reader": {"answer": "stop", "disposition": "answered"},
    "state_sha256": "sha256:2d2454e8220d9596fc720074579237c68a7e42f760e204cedf99520fc4643a7f"
  }
]
```

Selection: output/evidence.json, the run with task PickXtimes and condition
injected_stale_base, result.arms.malleus.events, those exact event IDs. Fields
are selected without changing values. Response prose and uncertainty remain in
retained evidence; admission did not execute the later source reviewer.

## Inspection and limitations

Paper checked the commit/tree, clean worktree and supplied handover/result hashes,
read the report, response/review records, replay mapping and runtime binding,
and reran the three committed pilot-evidence tests. All pass. They check result
digests, assigned-run closure, final-state equality, response/review binding,
prefix limits, refusal counts and unchanged state after refusal. Independent
aggregation found 756 arm-event outcomes, four supported labels and two
indeterminate labels. These 756 events are not 756 model trials.

Paper did not regenerate observations, rerun all storage executions, re-judge
the visual evidence, audit every agent access or rerun the reported 288-test
research suite. The latter is Robotics' retained result. No human ratification
or frozen provider snapshot exists. The two episode-zero demonstrations were
previously inspected development material; sparse sampling can miss events.
Container descriptions and image centers are not validated motor coordinates.
Neither semantic admission nor task-success evaluation ran.

Evidence root:
/Users/luis/.codex/worktrees/8ce0/malleus-dev/research/robotics_simulation/robomme/pilot.
HANDOVER.md SHA-256:
ee43406dcaead981295c3b23670c17742c367c726141a57810a16476ed20abb6.
output/evidence.json SHA-256:
a7b256179d01d6595edf76ff8298dcdff7efcf1b0786499392cc8f0451c93546.
Executing Core stays 79ae2feff7fc59436ef405fd91fe5a38c8253394, not the paper's
c95dba7 or the separately checked action-ontology compiler candidate.

## Recommendation, not a selection

Use this as a short optional appendix example, not an abstract-level third
proof. It broadens the source modality and makes stale-base refusal concrete.
It does not improve the marine coverage numbers, establish semantic Re-entry
or supply comparative novelty over a transactional event log. The existing
paper can proceed without it. Adding this paragraph to the submission candidate
requires Luis's selection and an evidence-access decision for the visual inputs.
Core's unfinished action contract remains a separate dependency, not a reason
to reinterpret this completed pilot as an action result.
