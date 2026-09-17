# Interpretation review coverage: implementation and handoff

## Result and boundary

The approved checker is implemented in this isolated Core candidate. After new
evidence, an adopter can declare which interpretations need another look and
mechanically refuse a completion claim when any review is missing or stale.
An interpretation previously marked complete is not exempt. A current review
may say that a correction is proposed, no change is warranted, a conflict
remains, or the matter is unresolved. The last two finish review without
pretending to settle knowledge. Nothing in this checker admits a correction.

Role: `REFERENCE_IMPLEMENTATION` of an explicitly selected `OPTIONAL_PROFILE`.
Without that selection, existing consumers gain no new completion guarantee.
The contract and stage dependencies are in
`design/INTERPRETATION_REVIEW_COVERAGE.md`; the runnable public example is in
`docs/INTERPRETATION_REVIEW.md`. The predecessor guidance-only handoff remains
historical evidence, not a claim that its earlier commit shipped this runtime.

## Public inputs and mechanisms

`malleus.acquisition` exports exactly `REVIEW_COVERAGE_PROFILE`,
`REVIEW_COVERAGE_PROFILE_IDENTITY`, `ReviewCoverage`, `ReviewCoverageRefusal`,
`ReviewCoverageRefusalReason`, and `check_review_coverage`.

`check_review_coverage(boundary_bytes=..., review_bytes=...)` consumes an exact
declared boundary and an explicit selection of review bytes. The installed
`src/malleus/profiles/interpretation-review.json` defines closed fields, outcome
payload requirements, and report groups. Python validates and compares those
declarations. There is no domain-specific truth rule or arbitrary callback.

The result binds the canonical boundary, profile and selected reviews. Missing
and stale IDs remain distinct from unresolved issues and pending corrections.
`result.require_complete()` refuses incomplete coverage. Required fields have
no guessed defaults. Reference-array and review ordering do not change the
canonical receipt. Consumers must supply the actual current boundary; checking
an old declaration cannot discover evidence omitted from it.

Installed Acolyte guidance names the actual public call and completion method.
It does not equate instruction delivery with enforcement. Existing Assent review,
ontology compilation, capture census and knowledge admission remain unchanged.

## TDD record

1. Runtime RED: `ebfe37522d8889ef9f25e3a202e00b0fe9a21a3a`. The forty cases
   could not set up because the approved module did not exist. These were
   missing-implementation errors, not forty failed behavioral assertions.
2. Runtime GREEN: `4d0fa42cf9c1adae1540a5e111a5072e52fc1a3e`, tree
   `4ba91dc4869fe0037d957ee7236de39b6716e822`. All forty cases pass.
3. Delivery RED: `bd39615ae4c4fe407db8935527807ca55eb8e15a`. Two tests failed
   because installed guidance did not name the checker and the documentation
   policy did not permit its public module.
4. Delivery GREEN: `55c3e3888891ddbacf10ac08ddf5d8c1a8b649cb`. The installed
   guidance, documented example, public-module policy and manifests agree.

The main behavioral fixture starts with two interpretations, one previously
complete and one unresolved. Both become review obligations at a new evidence
boundary. Reviewing only the unresolved item still refuses completion. Reviewing
both can complete coverage while preserving a specific unresolved issue and an
unadmitted correction proposal.

A separate integration case admits a real synthetic record through
`KnowledgeChangeHistory`, appends retained evidence, runs the checker, then
reopens and replays the history. Evidence retention advances the protocol
position without changing the graph. The checker changes neither ledger bytes
nor accepted graph, acceptance head or materialization head. It uses existing
history test helpers to assemble that fixture, not a new public bootstrap API.

## Verification

Run from the isolated checkout with the project's configured test environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -ra --tb=short -p no:cacheprovider tests/contract_compiler/pareto/test_review_coverage.py tests/contract_compiler/pareto/test_adopter_completion_boundary.py tests/test_inquisition.py tests/test_docs.py::test_public_guide_submodule_imports_are_exactly_allowlisted tests/test_docs.py::test_repository_python_examples_are_ast_checked
```

Result: **154 passed, 1 skipped**. The skip is the absent optional private
paper-program doctrine. Changed-file Ruff, formatting, diff checks and the
skill-creator quick validator pass. These include actual installed skill delivery
and API resolution, not a model-behavior trial.

Additional executed selectors, with the same environment prefix:

```sh
python -m pytest -q -ra --tb=short -p no:cacheprovider tests/test_docs.py tests/test_contract_compiler_ledger.py tests/test_contract_compiler_integration.py tests/contract_compiler/pareto/test_review_coverage.py tests/contract_compiler/pareto/test_adopter_completion_boundary.py
python -m pytest -q -ra --tb=short -p no:cacheprovider tests/contract_compiler/pareto/test_knowledge_change_history.py tests/contract_compiler/pareto/test_capture_coverage_boundary.py tests/test_protocol.py::TestLeanReviewProtocol
```

The first passes **535 tests**, including strict source-pure HTML and docs
contracts plus governance and compiler integration. The second passes **112
tests** covering existing history, capture accounting and Assent review.
Selectors overlap; their counts are not a unique-suite total. The complete
repository suite and live-model consumers were not rerun for this isolated cut.
An authorized relay independently reported **45 passed** for review coverage and
completion-boundary tests from an export of the exact delivery commit. That was
a scoped inspection, not release or integration approval.

Strict Sphinx doctest passes **17 examples**, including all **16** in the new
review walkthrough. Local builds used the already configured dependencies and
`python -m build --no-isolation --sdist --wheel`; Twine passed both artifacts.
The existing CI source-archive parity helper rebuilt the same wheel byte for
byte. An offline, no-dependency install into an isolated target, imported from
outside the checkout, exercised all six public exports, profile identity,
missing-review output and unresolved-but-complete coverage. This uses the test
environment's dependencies, not a fresh dependency-resolution or release claim.

| Artifact | SHA-256 |
|---|---|
| Canonical public profile identity | `ffdcaf90e34facf9839b6ce446ce65a915ea5ef854509fd38dd4cdc3484e523d` |
| Built source archive | `68966e3e66cbf782515fc84de222e52d844deeac006687f52f6e7051c500cef7` |
| Direct and source-rebuilt wheel | `5f3fa4dc6f30d3c1cc70834dc8f156123eb3d9749a7675305947225bc11b1dab` |

Validation-command corrections were not product changes: the first combined
delivery run found the new guide untracked; committing it satisfied the existing
tracked-guide guard. An initial ad hoc parity invocation gave the existing CI
Context helper an extra positional argument; the corrected keyword invocation
passed. Neither is counted as a passing run. No dependency policy was relaxed.

## Exclusions and integration ownership

This checks declared coverage and reference binding, not source truth, complete
dependency discovery, authenticated reviewer conduct, rationale quality or
semantic correctness. It fetches no source, opens no history and writes nothing.
Review outcomes are adopter judgments. A caller can omit undeclared information
or supply an obsolete boundary; this is not an adversarial caller attestation.
No model trial, cross-language replacement proof or automatic consumer gate is
claimed. The grammar is experimental `private-v0`, not stable wire.

No new dependency, ontology, admission mechanism, release version or shared
ledger is introduced. This candidate does not integrate, push, release, refresh
global skills, rebind consumers or modify the separate replay/release candidates.
Its local document revision follows OVR-000459. An eventual integrator must
reconcile local governance against the then-current shared head, not copy a
conflicting entry number.

## Separate queued graph-rule requirement

The Shop handoff at `fca9ab3fada6fad7e3bbf673826ccd6ad988beaf` is a different
Core task. Current `machine.py::_validate_admission_rules` admits only
`REQUIRE_TYPES_IN_ROLE` over replacements. `knowledge.py::_validate_transition_rules`
enforces that selected rule while folding a change. It does not provide a
general whole-resulting-graph constraint. `revision.py` explicitly refuses a
normative-profile change during domain contract revision.

The smallest proposed sequence is therefore two separate contracts, not a
reinterpretation of the current checker:

1. A pure, identified graph-state rule enforced by owning admission and replay.
   The motivating rule counts distinct shipment identities per unit over the
   complete resulting active graph. Resolved relation types, endpoint roles,
   grouping, distinct count and limit belong to data, not Shop branches in
   Python. Caller-authored successful check outcomes must not bypass it.
2. An explicit same-history policy activation that preserves earlier selections
   and checks the current accepted state before applying the new selection.
   If that state violates the new rule, activation fails without changing the
   old policy or accepted facts. Old-policy operations are not globally frozen.
   Failure-report persistence needs its own explicit transaction contract.

Both are queued requirements, not implemented capabilities or a selected new
wire format. Recovery, exceptions and migration remain future decisions. Historic
shipment observations must not silently acquire an operational uniqueness rule.
No Shop, paper or consumer file was changed to accommodate this assessment.
