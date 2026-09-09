# Frozen Shop validation, 2026-09-08

This file is chronological evidence. Earlier pending statuses describe their
frozen boundary; the connected-run successor at the end records current work.

Source and probe implementation:
`5ea6c9031604916472a5402724bd09968de70905`, tree
`685e09249865b924fb0e5477a4c4763587b71bbe`.

Final behavioral validation used an isolated export of released Core
`v0.14.0`, commit `e2b9e77912f9b36fdbfe2fca310548a789bffb4d`, overlaid with
only that commit's `connected_story/` and `CONNECTED_STORY_PLAN.md`. This
excluded concurrent Core, paper and Re-entry work. The Python import path was
verified to resolve to the isolated export. Dependencies came from the
repository's existing declared development environment; no installation or
package change was made.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story tests/contract_compiler/pareto/test_domain_history_profile.py tests/contract_compiler/pareto/test_object_event_population.py tests/contract_compiler/pareto/test_small_shop_default_admission.py
```

Result: **35 passed in 26.37s**, zero skips. The same selector in the live
checkout previously returned 35 passed in 26.55s. The new Shop-only tests
account for ten of these: seven source-boundary and three integration tests.
Scoped Ruff lint, format and whitespace checks pass. The proposed schema's
public PROJECT grounding check passes. None of these is human ratification of
the source or the proposed profile.

The independent source denominator is the retained publisher image, not an
image regenerated from our transcription. Its SHA-256 is
`d553b5bd5f9ecf3d0051a685c0bbe30cf99055f8dd09f712a6cf3ca302ed58e8`.

The isolated positive probe produces 18 ledger events, two KCS, seven
historical records and six current records. Repeated runs reproduce:

- History bytes: `sha256:72be0178fc066f2dbb36ab76bfc580c50755251f499593aaa50be6a0ddab6181`.
- Ledger head: `sha256:86bf7cbc723b37d68f7b02b472621e6371161c3f53bda2e63fd1f20615f529f8`.
- Replay receipt: `sha256:979edce122f566e38530c12662442b0976abfbd2136f008b1d4d73a2534b60be`.

The contract probe independently reproduces Event replacement as `ADMITTED`,
with the old event retained and its replacement current. That observation is
the open Core classification question in [CORE_REQUIREMENT.md](CORE_REQUIREMENT.md),
not a passing test of the proposed state-only correction guarantee.

The request was delivered to the separate **Malleus Core** task
`01a02f71-fec6-7382-9c68-c3efd3dba5d4`. Shop has not implemented an upstream
fix, selected the final profile, populated all 21 events, or published a release.
The next dependent action is to resolve the enforceable history contract,
then complete the joined Shop runner with its independent expectations.

## Source answer-key addition

The later Shop-only addition follows test-data RED `50b7df40`, seven failures
for the absent `source_expectations.json`. The hand-authored file supplies nine
source questions and exact witnesses. Seven tests pass, including four mutated
copies with a missing row, missing field, false value or duplicate case. These
are source-accounting checks, not graph-query correctness or human ratification.
The future producer must not read the expectation file.

The combined selector above, now including these seven tests, returns **42
passed**, zero skips, in the live declared environment. No installed-package,
full-repository or release gate was run for this test-data addition. The frozen
35-test release-baseline result above remains its own separate receipt.

Core has acknowledged that custom correction text is descriptive, not a
state-type admission restriction, and is investigating the execution contract.
Shop has not selected that profile or implemented an upstream workaround.

## Restricted-history successor

Core later delivered the optional transition rule at
`2ef5442efec6e43f2b2623a288933f7c62d46d4e`. Shop consumer RED `0f793c54` and
GREEN `04794b4d6a14ebd9237311d77dc1a26ca8dd9a4e` verify the narrow replacement
restriction in a fresh history. Eight consumer cases pass. An isolated
detached Core checkout with only the Shop successor files passes **283 tests,
zero skips**, covering the whole Shop directory and Core's transition suite.
This is not a full repository or release test. The initial archive-only setup
failed the existing historical-Git journal check; the final checkout retains
those objects and passes without changing the guard.

[The consumer report](RESTRICTED_HISTORY.md) records exact rules, source/history
identities, replay parity, matching controls, refusal atomicity and limitations.
The earlier structural-only evidence stays frozen. The missing Core capability
is closed; final Shop history semantics and the full connected population are
still pending selection and implementation respectively.

## Ontology-led connected run

The user selected the ontology-led approach after rejecting the exact-concrete-
type recommendation. RED `dd36af1e` commits the modeling decision and eleven
expected missing-module errors. GREEN is
`90c3aeee0b04335a6eb6e9bf11f93c200b2d7dc4`; its runtime, ontology, profile,
mapping and instruction are all Shop-owned. Guard commit
`f53b48c16931003c691d46d79eca60bb0acdf159`, tree
`0fc7a4e871b456a1adfed3401a3f538e5824fbcc`, adds tests without runtime changes.
Core's unrelated closing documentation commit falls between RED and GREEN;
it is not a Shop change. No old probe bytes were replaced.

The frozen implementation uses the delivered Core transition mechanism,
unchanged since `2ef5442e`. A local detached clone of exact `f53b48c1` retained
its Git object history and excluded all shared worktree dirt. Python imports
resolved under that clone via `PYTHONPATH=src:.`; dependencies came from the
existing repository `.venv`, with no installation. Bytecode and pytest cache
writes were disabled. The exact command was:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q --tb=short -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop tests/contract_compiler/pareto/test_transition_admission.py
```

Result: **296 passed, zero skips**, 122.83 seconds. The selector includes the
13 connected-run tests at that commit. The detached checkout remained clean.
This is a Shop/transition regression gate, not the full repository or package
gate. Scoped Ruff and format checks pass. The public schema check and its
intentional notes are recorded in [MALLEUS_INQUISITION.md](MALLEUS_INQUISITION.md).

A separate run from the same detached source produced 895,225 ledger bytes,
121 protocol events, 21 domain changes, 107 historical records and 106 current
records. Formatting-only successor `88f8889d` wraps the retained-profile lookup;
no behavior changes. Its detached rerun produces 895,257 bytes with the same
domain results. Source attestation changes because the adapter itself is
retained. Those final identities and output joins are in
[run_receipt.json](run_receipt.json). Repetition and reopen tests agree. The
maintained reader was opened at the final checkpoint, so this result does not
claim incremental advancement across every row. That broader observation is
still distinct from the earlier two-row incremental probe.

All 21 retained table rows and 123 nonempty fields have plan derivations or
declared gaps. Every historical record traces back to the retained table.
The source mapper is tested with independent answer-file reads forbidden.
The test suite separately specifies quantities, physical identity, invoice and
payment joins, missing invoice values, malformed quantity inputs and same-owner
predecessor selection. A synthetic occurrence replacement is refused after
successful preparation with the admission-boundary bytes unchanged.

The final documentation/receipt addition also exercises the documented read-only
CLI against that exact history and binds the receipt to input bytes. It changes
no implementation. Test counts for overlapping selectors must not be summed.

No source authenticity, human semantic ratification, universal identity policy,
business-rule eligibility, domain event ordering, authorization, action,
incremental performance, installed-package or release result is claimed.

Final detached gate at `7bdef4105518f8960bf417782e5e35104a02b20e`, tree
`5c7df14a87403e628a080257c0e93fc2065a13e3`: the same Shop/transition selector
returns **297 passed, zero skips**, 123.44 seconds. This includes 14 connected
tests and the read-only CLI/committed-receipt guard. Ruff lint, format and diff
checks pass; the detached checkout remains clean. The final commit after this
coordinate only appends this validation result, with no implementation or
receipt-byte change.
