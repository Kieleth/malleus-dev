# Document fixture producer repair

Operator-approved CONFORMANCE_FIXTURE correction for the optional
compiler-enabled, source-assertion profile. No runtime or protocol change.

## Contract

The document trace test must compare a current execution with a recorded
example from its exact compiler producer. The earlier inspection-note fixture
and the fixed two-producer compatibility audit remain byte-identical.

The observed failure at main `816eb2a` occurs before document admission:
`base_ledger_head` differs, while the other thirteen change-set fields agree.
The date/class-alternative compiler repair changed the retained producer
evidence. Its history hash must change; its domain meaning must not.

Reuse the existing document adapter, preparation, admission, reopen and trace
test path. Add only a separately versioned change-set example and a binding to
the compiler artifact, producer and unchanged historical input manifest.
Normal tests never regenerate their expected output or ignore hash fields.

RED must demonstrate the current failure and the absent producer/fixture
guard. GREEN must enforce exact producer and artifact identity, exact output,
unchanged input bytes, graph records, capture attribution, modality, assertion
time, domain time and batch valid time. Corrupted output or a different
producer must fail. The historical document tests also run at their recorded
producer, not against current runtime bytes.

Excluded: the other historical Shop comparisons, sequential actions, runtime
changes, package work, dependency installation, downstream edits, remote push
and a full-repository GREEN claim. This is independently consumable test and
evidence maintenance, not a new fixture framework.

## Evidence

Before edits, both the document trace and its dependent assertion-time test
failed at the same exact-output comparison. Their observed heads were
`sha256:9510c232e487d0b791b1984e7e75f2b0ab1cb38696600c7733096da795a1b105`
and historical
`sha256:5f52eeecdc80479f6b3a0133fd0390d67f39733c12b88fe0c4946790b405c390`.

RED `51e9bb20cfad221217588bc3ddeafa91c7be4715` adds ten tests. All ten
failed before the correction: the current fixture and producer guard were
absent, and the actual admission/replay path reached the original mismatch.

Initial GREEN `4601f6c1175f740d0b440475fe1becce05da2714` adds
`inspection_note_execution_v2` beside the unchanged fixture, and
29 lines to the existing trace helper in place of its three-line historical
comparison. There is no production change. The new change-set bytes were
captured from the real preparation result at RED, not produced by replacing
a hash in the old expected file. Their SHA-256 is
`059fb6a1843a91ffd931e3b79264a9d9a47c505e32718e8d6b027cd035ca8656`.

The binding checks the complete compiled artifact, its producer, the old input
manifest and every retained fixture member before comparing the complete
change set. Wrong producer/artifact, corrupted expected bytes and changed
operation/source/evidence/time/history fields all have refusing tests.
The live public path admits, reopens, compares all graph records against the
unchanged plan, and recovers exact source, capture and plan bytes for every
record. Existing tests additionally check modality and distinct or absent
assertion/domain times.

Initial validation in the configured `.venv` environment:

- Ten new guards plus existing document trace/time tests: **20 passed**.
- Complete affected population/document/history/public-facade/KG seam:
  **430 passed**, no skips, in 31.75 seconds.
- Changed-file Ruff, formatting and scoped diff checks passed.

Final self-review found that decoded Python JSON equality treats boolean
`false` and integer `0` as equal. Corrective RED
`529f2667d44ed3bf95af2da63fdf65a7daad2021` changes an operation ordinal to
`false`: **1 failed, 10 passed**. The comparison now uses canonical JSON bytes,
preserving JSON types while ignoring presentation whitespace. No expected
artifact changed. Final affected-suite rerun: **431 passed**, no skips, in
32.04 seconds. The final guard and existing trace/time subset contains 21 tests.

The existing governance mechanisms also passed at initial GREEN: **162 ledger
tests** and **199 integration tests**. Those broader runs preceded the final
type-comparison follow-up; they are not reported as full-suite execution at
the final tip. Final ledger/current-projection and integration checks run again
after binding the final file bytes.

Exact affected-suite selector, with bytecode/cache writes disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_document_fixture_producer.py tests/contract_compiler/pareto/test_document_assertion_adapter.py tests/contract_compiler/pareto/test_document_assertion_time.py tests/contract_compiler/pareto/test_population_trace.py tests/contract_compiler/pareto/test_population_plan.py tests/contract_compiler/pareto/test_governed_population.py tests/contract_compiler/pareto/test_knowledge_change_history.py tests/contract_compiler/pareto/test_public_compiler.py tests/contract_compiler/pareto/test_repository_guards.py tests/test_kg.py
```

Historical validation ran from a fresh local detached clone at
`9ec32d40634c927f9c7c160e226152c3782f4c84`, tree
`be66144387617da1d1044401b8389ab1ae17b9fb`. The two original trace/time
tests passed unchanged, with imports verified inside that checkout and its
compiler producer verified as
`sha256:5eb3ca2ba74e8cee3d8e7f5d4710ae026f728ffa5923d215a00c40716c03edcf`.
The checkout remained clean. No dependency installation or network access was
used. The exact selector was:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_population_trace.py::test_document_trace_reaches_assertion_locator_and_retained_capture tests/contract_compiler/pareto/test_document_assertion_time.py::test_public_trace_reaches_each_assertions_own_time_or_absence
```

The old fixture manifest is still
`sha256:229db892765e9005b1a3f5c767a102c13e28a9ba00c5fe989e7488c7f95774fc`;
its original change set is still
`sha256:d7ea99a463195fdaf20c7bfb5d1f63736ea48f2252a5651d7d3266a015048673`.
All archived handover examples, fixed compatibility-gate files, `src`,
ontology and package configuration are byte-identical to `816eb2a`.

## Scope result

This closes the document comparison shared by two current tests. It does not
close the other historical Shop comparisons or claim full repository GREEN.
Re-entry can consume this correction without sequential-action work. No paper
or downstream file is included. The old compatibility audit remains a statement
about its exact historical and repaired commits, not today's current suite.
