# Robotics and Semantic Re-entry: first seam audit

Status: read-only source inspection, not a new runtime result or a frozen
cross-domain public contract. Proposed transfers are DESIGN_CONSTRAINT uses of
ADOPTER_CHOICE; no second implemented action consumer is claimed.

Inspected robotics commit `f1402ca8930cb8516db233d97f7ddfb6ec3a8437`, tree
`ce6bbc539231f06542c141e418a366d63a7a1d19`, in the Robotics-owned worktree.
Its runtime names Core `79ae2feff7fc59436ef405fd91fe5a38c8253394`. That is not
the repaired compiler/action-contract worktree. No pin was changed.
The active visual pilot's uncommitted files were excluded from this audit.

## Exact inspected seams

All paths below are relative to `research/robotics_simulation/robomme`.

| File | SHA-256 |
| --- | --- |
| assessment.py | 99f43bb7c3293b415d138fc31704079bc57cafee0a56853c25170527769be6e2 |
| stores.py | d2984b38b5244a72c32a4cc4cc99b9721acff97b96da59d12ccdb2409fa11d12 |
| runtime.py | 468c6fa34e3e2c98981e5c30b3a49cd024198c95e1ca0e3ae31069b500db53a9 |
| tests/test_offline.py | 1bef222a9b3d156c19e904ffa24d3a798008cba92cd6c4703c158c4c98664f72 |
| integration-plan.md | 5dcef593f289ed673659333ec2ba721cffa2a08663e84fd0ba205eb402e221b2 |

`assessment.validate` checks a closed proposal shape, task/episode agreement,
support within the observed prefix, exact prefix identity and retained capture
references. Unknown assessments cannot carry a guessed count or container.
These are binding and structural checks, not pixel entailment.

`revision_check` requires an explicit current predecessor and advancing
assessment order. It permits same-capture corrections. Repeating an identical
proposal ID and bytes yields NOOP; reusing its ID for different bytes refuses.

`MalleusStore.apply` checks the current receipt, builds a population plan with
explicit supersession, then calls the existing harness preparation and admission
seams. `snapshot` reads the replayed graph; `reconstruct` reopens the history.
`observe` retains capture/evidence anchors. This is not an ActionProposal path.

The offline tests explicitly include a well-formed but semantically wrong count
of 99 accepted by both Malleus and the transactional event-log arm. This is a
declared limit of the experiment, not evidence of automatic semantic repair.
Tests also specify stale-base refusal after new evidence, atomic refusal of
future-prefix evidence, explicit unknown, supersession and reconstruction.
This audit read those tests; it did not execute them or reinterpret their old
results as a new run.

## What transfers, and what does not

| Boundary | Small Shop | Current Robotics seam | Consequence for the design |
| --- | --- | --- | --- |
| Observation | Exact supplier row bytes | Exact capture prefix and channel bytes | Bind the actual source and selection, not only a derived answer. |
| Internal revision | Explicitly replace e4 with a source-backed fact | Explicitly supersede the current assessment, possibly using the same capture | Evidence-changing and interpretation-changing updates are separate cases. |
| Derived output | Commitment goal/finding | Fixed reader returns continue, stop, container or abstain | A reader answer is not independent KG authority or effect permission. |
| Goal semantics | Commitment equals exactly 2 | Count reader stops when count is at least the target | Goal/operator policy must be explicit, never hard-coded in generic Core. |
| No-op | Fresh satisfied goal emits no candidate or write | Identical proposal ID and bytes yields NOOP | Duplicate suppression alone does not prove semantic quiescence. |
| External control | Proposed supplier amendment composition | Later grounded-subgoal/policy/action-chunk integration | Neither recording nor offline stop constitutes a newly executed action. |

An immediate thought experiment distinguishes the goal policies. With a value
of three and target two, the Shop oracle says the exact goal is unsatisfied and
the one-to-two operator is unrealizable. The current robotics reader would say
stop. This is a prediction from inspected code and the frozen Shop oracle,
not an executed robot trial. Neither policy is selected as a universal rule.

Another thought experiment keeps the same image prefix but changes an authored
assessment from count one to two. Existing revision mechanics can retain that
change and move the reader's answer. They do not prove that another physical
pickup happened. Such a correction must state its evidence and interpretation
policy; an inferred desired count cannot masquerade as a new observation.

## Candidate follow-on experiment, not yet frozen

The useful second-consumer question is whether a derived robotics answer can
enter an explicit goal-to-proposal contract without gaining writer or controller
authority. The target must first be defined by the robotics owner. It is not
valid to import the supplier amendment grammar or to treat stop as task success.

Once real action inputs are available, compare the declared preconditions,
preservation, source prefix, ambiguity, stopping rule and refusal behavior with
the Shop contract. Keep the same action model and reader across the storage
arms. New Core requirements go to Core with a pin and reproducer. A research
adopter mapping is not a new Core type, and prospective reuse is not empirical
replaceability.

The robotics integration plan still separates exploratory assessment, frozen
VLM evaluation and conditional online control. Its model/backend, research
partition, independent label procedure and simulation-host decisions cannot be
chosen by this thread. No extra dataset or simulator run is required for the
current read-only comparison.

## Subsequent retained boundary

Robotics committed its visual pilot at
`5727cc1b97aba1de6060684774c9bef4cf11032f`, tree
`b994c0cc2a906735270412976845c0a3ba535dd5`. The pilot handover was read in full
and these exact file hashes were checked by this thread:

| File under robomme/pilot | SHA-256 |
| --- | --- |
| HANDOVER.md | ee43406dcaead981295c3b23670c17742c367c726141a57810a16476ed20abb6 |
| output/evidence.json | a7b256179d01d6595edf76ff8298dcdff7efcf1b0786499392cc8f0451c93546 |
| core-candidate-audit/result.json | 39578cfc1850445708abbeebeab0af8e89b21f6b1eb09071e881953cec03facc |

The handover reports six fresh-context visual responses across two recorded
demonstrations and four paired replay conditions. Malleus and the transactional
event log both reject four injected stale-base attempts and reconstruct equal
final assessments. The four known responses receive model-assisted support;
the two unknowns remain indeterminate. This is neither human ground truth nor
an advantage over the event log. This thread did not rerun that experiment.

The identical three ontology sources also compile under isolated Core candidate
`1be958e88dce865c8e785638d1c15508c92bd1d2`. Robotics performed the process;
Core verified its receipt. The default robotics pin remains `79ae2fe`. There
is still no integrated ActionProposal, authorization, native dispatch, execution
attestation or independently observed post-command state in the pilot.

## Failed-attempt accounting, subsequent controller audit

Read-only inspection at Robotics commit
`c968bd346aecc3becc4154468adec36b544bd179`, tree
`ec50e79e5ab49f57d76f98c544b3e41d64cf395b`. The controller-audit README,
retained result/review and audit implementation/tests were read. The manifest
and all five retained source byte lengths, SHA-256 and Git blob identities
match. This thread did not fetch upstream, execute the witness or rerun tests.
Robotics' retained output reports four audit tests within 292 research tests.

| File under robomme | SHA-256 |
| --- | --- |
| controller-audit/README.md | 36add06133ee03cbd276ca5d4bcb4e9f3d1df1b38d83e56844f775dca7898542 |
| controller-audit/result.json | 197f10c3a139187c3ffb99cdf8c5e27168b28e93b6d31c0e9a92e6caf5d595a0 |
| controller_audit.py | 36b5bc08f02a08d1650b00c6c874c5144c9585347af5fbc1de0fd1ffa81f2bff |
| tests/test_controller_audit.py | 927bbd56636c2c82ea85c87450abad6613b500ceae824d3ebaf80e6eff82c36c |

The retained authored witness has three episode entries: true, error and false.
The pinned resume function returns and rewrites only the two Boolean entries;
the absent error episode then remains eligible for retry. Separately, the
extracted aggregation expression raises TypeError on Boolean/string results.
The full evaluator catches that exception. Neither permanent denominator loss
nor an uncaught evaluator crash is established. No controller, simulator or
robot ran. These are inspected reference bytes, not an adopted implementation.

The narrow Re-entry consequence is already required by ADOPTER_CONTRACT.md:
absence from a mutable progress summary cannot erase a failed or unresolved
action from the accepted lifecycle view. In this one-attempt supplier case,
mistaking an omitted error for a fresh episode would incorrectly restore the
action budget. Upstream retry behavior is not our stopping policy and must not
be inherited implicitly. Execution outcome and accepted goal satisfaction also
remain separate values, not a shared Boolean success metric.

The future lifecycle tests must reopen the one authoritative history after a
failed receipt, retain that attempt, and emit no replacement action for the
same exhausted episode. A failed receipt followed by the separately permitted
observed/accepted correction may satisfy the goal, but must preserve the failed
receipt and produce no retry. These are existing design obligations, not newly
passing tests or a request for another Core mechanism. The current offline
robotics wrapper's failure-retention tests do not establish online coverage.
