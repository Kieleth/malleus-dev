# Frozen Shop validation, 2026-09-08

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
