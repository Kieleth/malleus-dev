# Explicit absence of valid time

Luis approved this Core slice after the completed structured-source and locator
work. The evidence is the Shop source adapter's need to invent an ORDER_ONLY
token when no domain time was stated. This is not a paper or evaluator change.

## Bound contract before implementation

- Role: REFERENCE_IMPLEMENTATION of the optional compiler-enabled semantic
  history profile. The Shop case is a CONFORMANCE_FIXTURE; selecting domain
  time and replacement meaning remains an ADOPTER_CHOICE.
- Claim: an explicit `{"kind":"NONE_STATED","value":null}` survives plan
  compilation, change-set encoding, admission, reopen and record tracing.
  It asserts neither an instant nor relative domain order nor timeless truth.
  Ledger transaction order remains intact and means only recording order.
- Observation: admit the two retained supplier rows without supersession and
  recover both quantities, both source traces, and null valid-time values.
  An explicitly supplied same-kind replacement is separate from that case.
- Reuse: KnowledgeValidTime, the neutral PopulationPlan, the installed structural
  bundle, KnowledgeChangeHistory and the public record trace. One parser must
  serve the plan and change-set boundaries.
- Refusal: null or missing valid_time is not shorthand. NONE_STATED requires
  explicit null, INSTANT and ORDER_ONLY retain their required nonempty strings,
  and replacement across kinds continues to refuse before writes.
- Exclusions: no timestamp inference, new temporal query engine, cross-kind
  migration, changed document capture order, historical receipt rewrite, model
  comparison, package release, or Assent ValidTime change. Existing private-v0
  values keep their bytes and meaning; this is no stable-wire claim.

Pre-action check: local source/test/doc changes only; no server, endpoint or
dependency change. Required input stays explicit. Replace duplicated parsing
with one shared implementation, with hard tests at both consumers. No new
production mechanism or parallel ledger is introduced.

## RED, GREEN and evidence

Base: `160878cf14c0d27b11a440e26688708e9b7a7e2b`.
RED: `32804a0bfc7d18f207be4f8b254c87a6693aba6c`, 7 failed and 9 passed.
GREEN: `5c8b0cc9d7bdb9668df2d0c96e821ca635ea3e26`, tree
`2bfa0cd3cc691e21021cce64406fa1396d7a5e62`.

Public symbols: existing KnowledgeValidTime now accepts `str | None` as its
explicit value and supplies `from_data`; compile_population_plan and
KnowledgeChangeSet.from_bytes share that parser. No new module, export,
dependency, profile, callback or ledger was added. The two production files
have 32 insertions and 35 deletions. The new kind is a grammar capability,
not a truth assessment or a time-inference policy.

The first wider run found the older installed-skill guard's hardcoded two-kind
assumption. Its worked-plan check now calls the real parser, and the new test
executes the missing-time JSON fragment through compilation and admission.

Checks in the declared project environment, with `PYTHONPATH=src:.`,
`PYTHONDONTWRITEBYTECODE=1`, `.venv/bin/python -m pytest -q -p no:cacheprovider`:

- `tests/contract_compiler/pareto/test_unstated_valid_time.py`: 16 passed.
- That file plus `test_population_plan.py`, `test_governed_population.py`,
  `test_knowledge_change_history.py`, `test_public_compiler.py` in the same
  directory, and `tests/test_inquisition.py`: 358 passed in the live checkout.
- `tests/contract_compiler/pareto` plus
  `research/ontology_driven_kg_realization/experiments/small_shop`:
  715 passed, 3 failed. The five-plan public_population run passes its exact
  evidence comparison. Both new supplier-row scenarios pass replay and trace.
- Changed-file Ruff and diff checks, new test formatting, and the skill quick
  validator passed. No broad formatting rewrite was retained.

The three failures are the same correction, object-event and showcase
receipt-regeneration mismatches reproduced before this slice and recorded in
`handover/2026-09-06-capture-coverage.md`. This is not a full-suite-green claim.
No historical receipt, source, ontology, document adapter, Assent time model,
or frozen model run was changed. A separate attempted narrower selector named
a nonexistent `test_assertion_time.py` and collected no tests; it supplies no
evidence. The completed full Pareto selector includes the actual time tests.

## Scoped self-inquisition

Rubric 12; lowest affected profile is optional compiler-enabled semantic
history. Root schema rites: NOT RUN, no root-ontology change. No claim of
another interpreter, temporal query semantics, or factual correctness.

| Claim | Role | Evidence | Unsupported transfer | Verdict |
|---|---|---|---|---|
| Explicit absent time stays explicit | REFERENCE_IMPLEMENTATION | Plan/change-set, replay and trace tests | No timelessness or inferred chronology | PASS |
| Invalid encodings fail before writes | REFERENCE_IMPLEMENTATION | Nine malformed cases at both parsers, exact ledger bytes preserved | No arbitrary grammar extension | PASS |
| Replacement is an explicit input | ADOPTER_CHOICE | Both reports retained without replacement; separate explicit replacement case | Later append is not a source correction | PASS |
| Existing profile boundaries stay separate | OPTIONAL_PROFILE | Domain profiles, document adapter and Assent time source unchanged; cumulative tests | No mandatory semantic-history adoption | PASS |
| Shop demonstrates this boundary | CONFORMANCE_FIXTURE | Same retained source rows, public-only Core calls, current graph and historical source trace | No semantic completeness or model ranking | PASS |

Same-ledger cross-kind migration and time-query semantics remain future work.
The three pre-existing evidence drifts remain a separately bounded repair, not
an excuse to overwrite frozen bytes or broaden this slice.
