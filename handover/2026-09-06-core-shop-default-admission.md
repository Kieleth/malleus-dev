# Small Shop through shipped structural admission

Date: 2026-09-06. Status: implemented and tested on the isolated branch
`codex/shop-default-admission`; not integrated into shared main or pushed.

## Result

The existing five Shop plans now have a successor demonstration using Core's
shipped structural admission bundle. The example no longer supplies check
outcomes or builds its own admission policy. No Core runtime change was needed.

The run compiles the base ontology, admits O1/X1 and their relation, records an
additive ontology revision, admits invoices and their payment, then admits
supplier order B at quantity 1 and its correction to quantity 2. It disposes
of the live history handle, reopens the retained ledger, queries the graph,
and traces every current and superseded record to its plan and source bytes.

Observed: five change sets, one contract revision, 50 ledger events, nine
current records and ten historical records. Payment P1 settles I1 and I2.
Only B/e7 is current; B/e4 remains retained. Unrelated records survive the
correction unchanged. Two independent runs produce identical output bytes.

## Accepted cut and ownership

Classification: `CONFORMANCE_FIXTURE`. Lowest affected selection: the optional
compiler-enabled, state-version path with Core's structural admission bundle.
This fixture does not make that selection mandatory for other adopters.

The operator approved the isolated TDD slice. Its completion contract was
committed with RED, before the runner existed. Reuse takes precedence here:
existing source bytes, five existing plan templates, public compiler/history
operations, and the shipped bundle. The only edit to each derived plan is its
contract identity. Original templates and resulting plans are both retained.
Mapping files are evidence, not runtime policy configuration.

Owned paths are the new `small_shop/default_admission/` directory, the new
`tests/contract_compiler/pareto/test_small_shop_default_admission.py`, and this
report. No old fixture, runtime, ontology, package configuration, skill, paper,
or shared governance file changed. Fable's locator/time work is not duplicated.

## TDD coordinates

- Base: `8233b771a4f6ae8d248274fdda0185920f99421b`.
- RED: `defbacca7d73270513072d3e5a499cba95a49038`.
  Five tests failed because the new example module did not exist.
- GREEN: `87e71fa8209730630dd0085725288fafe1e50f99`.
- GREEN tree: `15d1ca90c6898faca8114f16861538d453182562`.
- Subsequent report/README edits do not change executable bytes.

The tests prove the public helper boundary, the full replay/query/trace story,
template preservation, stale-preparation refusal, and missing-endpoint refusal.
The negative cases compare exact ledger bytes plus replay receipt and graph.
The stale case preserves already-retained preparation evidence; it does not
claim that preparation never wrote anything. The missing-endpoint case refuses
before its preparation evidence is retained. The whole runner is multi-step,
not globally failure-atomic.

## Reproduced validation

All commands ran from the isolated worktree using the existing configured
project environment, with `PYTHONDONTWRITEBYTECODE=1` and `PYTHONPATH=src:.`.
No dependencies were installed. Interpreter:
`/Users/luis/Projects/malleus-dev/.venv/bin/python`.

Focused command, after that interpreter:

```sh
-m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_small_shop_default_admission.py
```

RED: 5 failed. GREEN: 5 passed.

Broader command, after that interpreter:

```sh
-m pytest -q -p no:cacheprovider tests/contract_compiler/pareto tests/test_kg.py tests/test_staging.py tests/test_accepted.py research/ontology_driven_kg_realization/experiments/small_shop
```

Result: **882 passed, 3 failed**. This is not a green full-repository gate.
The same three failures independently reproduce against a clean `git archive`
of the untouched base, using the same interpreter and import configuration:

1. `small_shop/correction/test_correction_vertical.py::test_checked_in_evidence_is_exactly_regenerated`.
2. `small_shop/object_event/test_run.py::test_ret040_admits_reopens_replays_queries_and_traces`.
3. `small_shop/showcase/test_evidence.py::test_regeneration_is_canonical_byte_identical_and_matches_runner`.

All three compare current generated evidence with older committed evidence.
The correction and showcase reports differ in identity-bearing fields; the
object-event report also differs from its expected bytes. The base rerun
establishes that this slice did not introduce them. It does not establish which
earlier change caused the drift. Their existing hard tests remain enabled;
no golden bytes or expectations were changed to hide the failures. Reconcile
them with their current owner before claiming a unified green repository.

Other gates:

- Ruff check and format check for the new runner and tests: passed.
- `git diff --check 8233b77..HEAD`: passed.
- `scripts/contract_compiler_ledger.py check`: 417 entries valid,
  head `OVR-000417`,
  `sha256:9127d5a1352123e7017ffafae4474f49cc2b03e4a345b8b74b6a8ceadd2a98fa`.
- `scripts/contract_compiler_integration.py check`: 75 workstreams,
  39 cards, 4 selections valid.
- Existing pytest discovery includes the new test. No CI configuration change.
- No package gate run: there is no packaged-code or dependency change.

## Standalone evidence

The module command in the fixture README ran successfully. Its generated
directory contains `history.jsonl` and `evidence.json`. These are reproducible
outputs, not replacements for any frozen predecessor receipt.

| Artifact | SHA-256 |
| --- | --- |
| Input manifest | `9b35af4b70f4e727b4e443c30500e731a8d48e6ac9a2e1526a2fc2942caa20b0` |
| Shipped structural bundle | `0ef377d965638263810edbac1047102facb2b2367c77498aba43b50ec32a884f` |
| History bytes | `f4d279bdc0860fc127fa220ae002f3ec2926e254703749155a605749a9c9848b` |
| Evidence bytes | `b5af1698df01e93d788a04c0ba8442d8f7710814be73ede5bf722ed9215f45ea` |
| Replay receipt | `1de243dc5aaf31588ce70a27b20d42ef93b829b4e3f1f861453169fed982cdd3` |
| Ledger head | `c5a007eaf6bbb91e2cbe7510311208a9363210273eb6b83259898dc46e38d9b6` |

## Boundary review and integration

The Malleus development skill's role/profile review is satisfied: the bundle
remains a selected default, the Shop remains an example, and the implementation
adds no protocol authority. Composition is tested for this exact path only.

Structural admission does not establish source truth, domain adequacy,
epistemic acceptance, or action authorization. Mapping and domain-time choices
remain the existing fixture's adopter choices. Source registration still uses
explicit anchor events. This slice does not implement source-locator resolution,
a new time kind, Event population, Semantic Re-entry, a stable wire, or a second
interpreter/projector. No replacement claim is made.

The branch is isolated because the shared checkout and index have active
Fable/paper work. No shared ledger sequence is reserved. Integration should
take the three slice commits, rerun the five contract tests against the chosen
Core tip, and preserve any independently accepted locator/time changes. Existing
governance validates without this fixture acquiring a new shared authority.
