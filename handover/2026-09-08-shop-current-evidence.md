# Current Shop evidence repair

Operator-approved CONFORMANCE_FIXTURE maintenance for the optional compiler
and history profiles. No new protocol or runtime capability.

## Contract

Current Shop runs must compare their complete outputs against evidence bound
to their actual compiler artifacts and producer. Earlier receipts and their
fixed two-producer compatibility audit remain byte-identical. Historical
receipts are evidence of their original runs, not a demand that a changed
compiler impersonate the earlier producer.

The smallest witness is the existing correction, object-event, public
population, showcase and fresh-import integration tests. Reuse those runners,
their independent source/graph/trace assertions and the separately proven
sequential-action run. Add one test-only evidence assertion shared by these
five cases, not a production fixture registry or a new comparison policy.

RED must expose the current failures and require explicit compiler-artifact
binding, immutable old receipts, exact output-file closure, and refusal of a
wrong producer, corrupt expected bytes or changed output. GREEN records one
new evidence generation from real temporary histories. No output field is
ignored; no test generates its own expected answer. Compare unchanged domain
facts, source inputs and provenance separately from changed history identities.

Then rerun the full Shop selection with compilation, population, contract
revision, correction, occurrence participation, fresh import, two action
lifecycles, reopen, queries and retained-source trace. Synthetic actions and
observations do not prove real external effects or cause the Shop correction.

Excluded: runtime and ontology changes, package/dependency work, new action
instructions, consumer edits, historical receipt rewrites, remote push, and
claims about tests that were not run. The document-fixture repair and fixed
historical compatibility gate remain untouched.

## Pre-action checks

No server interaction, endpoint, dependency installation or external effect.
Required evidence has no defaults or legacy fallback. The replacement is only
the current tests' stale output comparison, not a production mechanism. Tests
will guard the producer/output mismatch class and preserve the old evidence.

## Root cause and implementation

At starting main `fa71c42`, the full Shop directory plus fresh-import tests
reported **216 passed, 6 failed**. All failures were exact-output comparisons:
correction, object-event, two public-population tests, showcase and fresh import.
The observed differences are compiler-dependent history/artifact fingerprints.
Both graph files, domain records, source fields, time values and operation
meaning remain unchanged. No refusal, admission or replay defect was found.

RED `f65a5ec` added the producer-bound fixture contract and eleven failing
guard tests. GREEN `8d88e49` adds one 47-line test-only assertion and a separate
`evidence_2026_09_08` generation. It checks every retained validated compiler
artifact, including ontology-revision targets, before comparing complete output
bytes. It also checks all ten predecessor-file digests. Tests never regenerate
expectations or discard changed identity fields.

The generation was captured by the unchanged real runners in fresh temporary
histories at `f65a5ec`, with compiler producer
`sha256:51c019d49c3cd7d75330e02c5d728a873254cc4b56ca122dda078b15c25bcb3f`.
Its binding lists all output hashes and the exact differing fingerprint paths.
These describe one observed historical transition, not general exclusions for
future comparisons. Existing source, graph, correction and trace assertions
remain active after the corrected comparisons.

All **14 final evidence guards passed**. They cover wrong producer/artifact,
an unbound revision target, missing/extra output files, changed history/source/
record fields, boolean-versus-integer distinction, changed historical files and
corrupted expected bytes even when supplied as matching observed output.
Self-review corrected one negative witness that initially treated a recorded
two-element Entity row as a dictionary; it now mutates the actual row ID. The
output mutations first prove unchanged serialization matches the real bytes,
so a formatting mismatch cannot stand in for the intended rejection.

## Historical reproduction

A separate local detached checkout at
`9ec32d40634c927f9c7c160e226152c3782f4c84` used the same configured interpreter,
with its imports checked to resolve inside that checkout. The six Shop selectors
in the unchanged `research/action_history_contract_freeze/gate.json` all passed,
including the fresh import. No skip, xfail, dependency installation or network
access. The checkout remained clean. Document and consumer selectors were not
part of this historical rerun.

## Current integration selection

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto research/ontology_driven_kg_realization/experiments/small_shop research/action_history_contract_freeze/programs/test_sequential_profile.py research/action_history_contract_freeze/programs/test_sequential_history.py research/action_history_contract_freeze/programs/test_shop_action_composition.py research/action_history_contract_freeze/programs/test_keyed_effect.py tests/test_kg.py --tb=short
```

This exercises the selected state-version and object-event fixtures separately,
and the sequential-action fixture's two lifecycles and intervening correction
in one log. It does not imply that every optional profile was selected in the
same history, or that synthetic execution records prove external effects.

The expanded selection completed **1,054 passed**, no skips, in 674.09 seconds.
It collected before the final additional historical-file mutation guard and
the serializer-discrimination refinement. The final 14-guard selection was
rerun separately and passed; it is not added to 1,054 as a disjoint total.
No runner, compiler, runtime, ontology or action-profile code changed during
either run. A later invocation of the expanded selector collects one more
test because of that additional guard.

The fresh sequential run produced 106 events and the exact log digest
`sha256:cb66165b694d7939a88621a7c275f3a964c15d192abe223a7045bfd32d508477`,
matching the prior sequential proof byte-for-byte. It includes five knowledge
change sets, one ontology revision, two recorded action lifecycles, the e4/e7
correction and replay after authoring-process disposal. The historical receipt
was compared explicitly for this unchanged producer, not made a live golden
for later producers.

Repository CI's scoped Ruff command passes, as does the source diff check.
Formatting was checked on the six new or already-formatted changed test files;
unrelated pre-existing formatting in the correction test was preserved. The
fixed historical compatibility gate, old evidence, source inputs, runtime,
ontology and package configuration are unchanged from `fa71c42`. Unrelated
paper and research work stays outside this commit. This is a completed Shop
conformance correction, not a full-repository, package, release or push claim.
