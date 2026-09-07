# Small Shop evidence and readable proof

## Approved cut

Role: CONFORMANCE_FIXTURE for the optional compiler-enabled semantic-history
profile. Domain mapping, replacement and time choices remain ADOPTER_CHOICE.
This is not a protocol, compiler, ontology or package change.

Claim: current runners reproduce their exact recorded evidence, while earlier
evidence remains byte-identical. The walkthrough explains what the complete
five-plan run proves and distinguishes it from the separate no-correction,
unstated-time and declared-gap controls.

Observation: exact regeneration of all three failing Shop outputs, immutable
historical hashes, unchanged graph results, and public-path replay/trace tests.
Reuse: the existing correction, object-event, showcase and public-population
runners, plus the existing Shop time and capture tests. No new runner or
evidence framework is needed.

Excludes: new domain facts, automatic correction inference, semantic
completeness, model comparison, pure re-entry composition, paper work, package
changes, release and remote publication. No historical ledger is rewritten.

Pre-action check: local fixtures/tests/docs only, no server or endpoint;
no dependencies or missing-input defaults. Existing byte equality stays strict.

## Root cause and RED

Base: `7c5fdb491721122b6e0c7243862935acc8303a1f`.
The three failing nodes are:

- correction/test_correction_vertical.py::test_checked_in_evidence_is_exactly_regenerated
- object_event/test_run.py::test_ret040_admits_reopens_replays_queries_and_traces
- showcase/test_evidence.py::test_regeneration_is_canonical_byte_identical_and_matches_runner

These paths are relative to
`research/ontology_driven_kg_realization/experiments/small_shop/`.
The declared project environment reproduces 3 failures at the base. An archive
of `ca0d121ab81dcefb06e20f06a83ac1da3d1a1ab8`, the direct parent of
`e4fa5fd340100a62f1d6470d1c9c579b48289d05`, reproduces 3 passes.

That successor improved the INVALID_RANGE diagnostic in `elaborate.py` without
changing the accepted schema set. `_evidence` hashes five producer files,
including `elaborate.py`. Changed producer bytes change the retained validated
artifact, hence the history and downstream receipt identities. Both graph
files remain exact; object-event observations, contract, source, plan, profile
and graph identity remain exact. The differing explanation/query fields are
artifact, change, check and history identities, not changed shop answers.

Correction and showcase retain their last historical generation at the existing
paths. Object-event also retains its original `evidence.json`. New current
expectations live together in `evidence_2026_09_06/`. Tests compare current
outputs exactly and separately guard the historical hashes. A later producer
change must be reconciled explicitly, not masked by dropping identity fields.

The showcase evidence command's existing default points at frozen files.
Move that default to `build/`, with a hard test. Explicit output paths remain
caller-controlled.

## Validation and disposition

Evidence RED: `f4148ae3de0d25b0653e10d3fb681647df61b06b`, 7 failed and 8
passed. Six failures require the separate current evidence; one proves the
unsafe default output. GREEN: `8097c489f82cc6a0673f198ab1e6a81d74b96281`,
15 passed. The only research runtime change is the output default; an unused
historical-expectation constant was removed from the object-event runner.
No file under `src/`, ontology, source fixture, mapping or package configuration
changed.

Walkthrough RED: `2fcf08fdbea02922ad01e1e223eb09c9ef822115`, 1 failed and
1 passed. The missing documented query failed; the extended existing gap
test passed admission, reopen and trace without a production fix. The exact
query now reads the generated public history, prints quantity `2`, the `e4`
predecessor and `row:1:quantity`, and preserves ledger bytes.

Checks use `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=src:.`, and
`.venv/bin/python -m pytest -q -p no:cacheprovider --tb=short`:

- All eleven `test_evidence_archive.py` cases, the three original failing
  nodes, and `showcase/test_evidence.py::test_evidence_command_defaults_to_build_not_frozen_results`:
  15 passed.
- `public_population/test_run.py` under the Shop directory,
  `tests/contract_compiler/pareto/test_unstated_valid_time.py` and
  `tests/contract_compiler/pareto/test_capture_coverage_boundary.py`, plus
  `tests/test_docs.py::test_public_small_shop_walkthrough_matches_recorded_showcase`
  and `tests/test_docs.py::test_repository_python_examples_are_ast_checked`:
  27 passed. The three files in the documented command account for 25 of these.
- `tests/contract_compiler/pareto` plus
  `research/ontology_driven_kg_realization/experiments/small_shop`:
  **731 passed, no failures or skips**. This closes the three recorded failures.
- Changed Python Ruff checks, new/changed focused test formatting and diff
  checks pass. All 31 local Markdown links in the three touched guides resolve.

A separate fresh public run and reopen reproduced 48 ledger events, five
changes, one revision, ten historical and nine current records. Its ledger
bytes are `sha256:b471008f63e320456f4f42d5170780fac95e173cfe57156c8e345e054e39cec8`.
The existing public-run evidence already matched and remains unchanged.

This is a focused compiler/Shop result, not a whole-repository, package-build,
release or remote-publication claim. A final isolated docs and governance check
is recorded with the committed handoff rather than changing these results.

## Scoped self-inquisition

Rubric 12. The lowest affected profile is optional compiler-enabled semantic
history. No root ontology changed, so root schema rites are NOT RUN.

| Claim | Role | Direct evidence | Unsupported transfer | Verdict |
| --- | --- | --- | --- | --- |
| Current outputs reproduce without rewriting history | CONFORMANCE_FIXTURE | Exact regeneration and eight archived hashes | No claim that fresh history must retain an old producer fingerprint | PASS |
| Shop answers are unchanged by the evidence refresh | CONFORMANCE_FIXTURE | Exact graphs, occurrence observations, existing independent oracles and 731 tests | No universal semantic-equivalence claim | PASS |
| The walkthrough runs, not merely names APIs | CONFORMANCE_FIXTURE | Unmodified code snippet executed against a from-empty public run; no ledger mutation | No new API or public wire | PASS |
| Correction and time choices remain explicit | ADOPTER_CHOICE | Existing supplier controls with/without supersession and NONE_STATED | Later append is not correction or domain chronology | PASS |
| A declared gap survives the full route | OPTIONAL_PROFILE | Synthetic capture, admission, reopen, exact gap artifact and source trace | No automatic discovery of omitted semantics | PASS |

## Separate next requirement, not implemented

The isolated Re-entry task requests a pure KCS composer over an immutable
replay/base context. Current `compile_population_plan` returns operations;
`prepare_population_change` retains evidence; the pure `compose_change_set`
method still requires a writable history receiver. That is an explicit
capability-boundary request, not a defect in the three repaired tests. Core
must select its scope before implementation. No new composer, Re-entry object,
source-value verifier, or quiescence layer is claimed here.
