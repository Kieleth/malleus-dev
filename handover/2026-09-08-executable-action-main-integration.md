# Executable action history: local main integration

Luis approved integrating the tested candidate into local main. Remote push,
release, downstream edits and new runtime semantics are not included.

## Exact boundary

- Prior main: `2a11240556532c2b6160ac0bfa5ab1165e862fd2`.
- Frozen candidate: `90146c380994621a2f8df25876affd03fc9e57e3`, tree
  `609979f5d356ebb43c1288d80ea8f4f53d1f2613`.
- Tested implementation: `73d1a527dd237e5546d86d5c0470e9e056d41e16`.
- This successor changes status and governance documentation only. Runtime,
  program data, test files, compiler compatibility scripts, package settings
  and frozen evidence remain byte-identical to the candidate.
- Governance: `OVR-000427`, head
  `sha256:618f995fe49d53e193213f0bea9893df6772bd6b557d4a7eebd21b8dfff75d50`.

The prior RED/GREEN history is retained, not squashed. Main preflight found no
overlap with 329 pre-existing edited or untracked files. The final fast-forward
must preserve those files; neither a stash nor a reset is part of this landing.

## Verification

The following two disjoint selectors ran in the isolated integration checkout
using the existing project environment, with `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONPATH=src:.`, and `python -m pytest -q -p no:cacheprovider`:

| Selector | Observed result |
| :--- | :--- |
| `tests/test_contract_compiler_ledger.py tests/test_contract_compiler_integration.py tests/test_docs.py` | 490 passed |
| `tests/test_status.py research/ontology_driven_kg_realization/experiments/graph_recipe/test_cases.py` | 52 passed |

The standalone ledger validates 427 entries. The integration validator passes
75 workstreams, 39 cards and 4 selections. Ruff passes for `src/malleus`,
`tests/contract_compiler`, the action research directory, both compatibility
scripts and their test file. The candidate and integration diffs pass whitespace
checks. No runtime fix or dependency installation was needed for this landing.

The prior executable verification remains separately attributed: 643 tests in
four disjoint invocations and an extracted-wheel replay of the 86-event Shop
history, as recorded in
`research/action_history_contract_freeze/execution-verification.json`.
Re-entry independently reported its final 16-test selection and packaged replay
PASS. Robotics independently reported 74 lifecycle/schema tests plus 17
observation tests and exact source-run history reproduction. These reports are
consumer evidence, not additional tests rerun by this integration turn.

### Full-suite limitation stays visible

A default repository pytest run at the unbound candidate was interrupted after
1,246 passes and 8 failures. Three were already-recorded historical producer
comparisons; five were the missing successor governance bindings. The 490-test
integration run above closes those governance failures. The interrupted run is
not a full-suite result and is not counted as a passing gate.

The approved two-producer gate remains a bounded compatibility result, not a
green default CI run. Its nine historical exact-reproduction comparisons retain
their original tests and evidence. Compiler producer and resulting history
identities changed; the paired probes establish unchanged bounded graph/source
semantics. This integration neither rewrites historical receipts nor hides
their raw current-producer failures. Full repository CI is not claimed green.

## Consumer boundary and next requirement

Use `research/action_history_contract_freeze/EXECUTABLE_HANDOFF.md` for exact
calls and artifact ownership. Under the Malleus development skill's boundary
taxonomy, this is an OPTIONAL_PROFILE with a REFERENCE_IMPLEMENTATION and
CONFORMANCE_FIXTURE, not a new base protocol invariant or released Assent stage.
Default structural history and standalone Assent are not replaced.

Re-entry has verified the candidate and resumed its separate supplier consumer.
Robotics has verified the bounded lifecycle but has not run a robot or rebound
its frozen experiment. Its sequential-action requirement remains outside this
single-action proof. Neither consumer gates the other.

The record contract is explicit input to the research-local
`registration_bundle.build_registration_bundle(record_contract_bytes)`.
The later `add_context_proposal`, assessment, permission and dispatch builders
author the supplied `LocalAction` fixture, not a general domain-action factory.
An adopter may author a different exact compiled record contract and selected
program data. Retained raw bytes are already available to generic hash and
comparison operations; the adopter must declare and test how its payload binds
those bytes. No controller-request contract is inferred by Core.

Simply increasing an index's maximum length is not a sequential-action solution:
`dispatch_bundle.require_indexes` fixes selected indexes to one item, and the
programs compare position zero. Core also permits only one program selection per
history. A sequential-action successor needs an explicit neutral conformance
case and a demonstrated data-only recipe or a bounded Core mechanism change.
This integration selects neither and adds no robot-specific rule.

External effects, authentication, source truth, general retries, a stable wire,
an installed all-in-one action SDK and cross-language parity remain unclaimed.
