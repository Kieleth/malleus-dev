# Core adoption path and capability documentation

## Approved slice

Luis approved three parallel lanes on 2026-09-06: make the existing default
Shop admission runner the main walkthrough, correct stale public capability
claims, and let the isolated Re-entry and Robotics consumers report concrete
generic runtime requirements. Core alone owns Core code and governance.

The walkthrough describes a REFERENCE_IMPLEMENTATION of the optional
compiler-enabled semantic-history profile; its Shop checks are
CONFORMANCE_FIXTUREs. Profile choice, source mapping and correction meaning
remain ADOPTER_CHOICEs. No default becomes a protocol invariant. Without the
history profile this slice claims no admitted history or replay.

Claim: a reader can run the documented default path and inspect the rebuilt
graph and exact source trace, while current capability pages describe the
shipped compiler and profile-dependent Event admission accurately.
Observation: execute the documented command and query in a fresh directory;
check five changes, one revision, nine current and ten historical records,
quantity 2, its e4 predecessor and retained source bytes; guard current API
claims against the public surface and existing conformance tests.
Reuse: the existing default Shop runner, structural bundle, public compiler,
history/replay/trace, documentation tests and strict Sphinx build.
Excludes: runtime or ontology changes, new APIs, new source parsing, policy
selection, new fixtures, changed historical evidence, dependencies, packaging,
release work, broad hardening, external effects or completed Re-entry claims.

Pre-action check: local docs and tests only, no server or endpoint changes,
no dependency installation, missing required data remains an error, no runtime
mechanism is replaced. Preserve unrelated dirty paper and research files.

## Parallel ownership and dependency

```text
MainShopWalkthrough describes ExistingDefaultAdmissionRunner
DocumentedCommand consumes ExistingShopSourcesAndPlans
DocumentedCommand produces FreshHistoryAndEvidence
DocumentedQuery consumes ReopenedHistory
DocumentedQuery produces CurrentQuantityAndRetainedSourceTrace
CapabilityGuidance describes PublicCompilerAndSelectedProfileRoles
DocumentationTests verify DocumentedCommandAndCapabilityGuidance
CoreReleaseCoordinate feeds IsolatedReentryAndRoboticsConsumers
ConsumerReproducer proposes FutureCoreRequirement
```

The two documentation lanes write separate files and tests. Core serializes
only commits and the append-only governance entry. Consumers stay on frozen
Core `79ae2feff7fc59436ef405fd91fe5a38c8253394`, tree
`f1b7bbb9b98df036edbbb813b746f97552b47247`, while this documentation changes.
They do not wait for documentation or write shared Core paths. Any proposed
runtime expansion needs a concrete failure and a separately bounded decision.

## Evidence and review

Shop RED `5fb4a19` failed because the first documented command still selected
the older custom-policy runner. Capability RED `2d28043` failed five checks for
the missing default-entry links and stale compiler, retained-byte, public
history and Event-profile claims. GREEN `3c1967de0296f6ae454fdaefd79daac1bd67e6e2`,
tree `829fb2d0775a2a201c2bcf7d8405130c74455a42`, changes documentation and its
approved reference text only, plus moving the old documentation-query test to
the new default-run test. No runtime, source, plan, ontology or recorded
evidence bytes change.

Focused observations:

- New documented-command test, default Shop tests and predecessor public-run
  tests: 9 passed. The new test executes the command and query from the guide,
  verifies the 50-event history, five changes, one revision, nine current and
  ten historical records, quantity 2, e4 predecessor, source bytes and digest.
  Reads and a refused repeated run preserve ledger and evidence bytes.
- Historical walkthrough guard, unstated-time and capture-gap controls:
  23 passed.
- Capability/reference checks, entry-page guard, example AST check and existing
  machine/document/Event behavior selectors: 16 passed.
- Changed Python files pass Ruff and formatting; scoped diff check passes.

The broad compiler/Shop/docs/integration/ledger run produced 1,243 passed and
two failures. Both failures were strict HTML builds reporting the same link:
the research README was linked as a Sphinx source document although it is not
in the published source tree. No runtime or ledger test failed. The focused
link-format RED is `605a971`; the correction marks the README as an explicit
download without relaxing strict Sphinx warnings. The focused link guard now
passes. The corrected strict HTML, autodoc/autosummary, entry-page and example
AST checks all pass: four passed. These observations are not reported as one
uninterrupted all-green suite.

Exact broad command, in the declared project environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto research/ontology_driven_kg_realization/experiments/small_shop tests/test_docs.py tests/test_contract_compiler_integration.py tests/test_contract_compiler_ledger.py --tb=short
```

These focused groups overlap and are not added into one test total. No full
repository, package, release or clean dependency-resolution claim is made.

Exact corrective selector, with the same Python/environment/pytest options:

```text
tests/test_docs.py::test_strict_html_build_is_source_pure
tests/test_docs.py::test_autodoc_and_autosummary_render_the_existing_package_root
tests/test_docs.py::test_current_entrypages_lead_to_default_shop_admission
tests/test_docs.py::test_repository_python_examples_are_ast_checked
```

Consumer coordination: Robotics reported 191 focused checks passing against
the frozen Core coordinate above, with no generic capability request. This is
consumer-reported evidence, not a completed robotics experiment or a new Core
gate. Re-entry was already dispatched to its bounded consumer RED-to-GREEN
work. Both received the approved ownership boundary and continue independently.
Neither is authorized by this slice to expand Core or edit shared files.

Re-entry subsequently reported its bounded consumer GREEN at
`4f98f5ad2c10c421edaca231eed8f1a09be4f74b`, tree
`d526fcf7435aeb9fee1a8e52aea450778007013a`. Core independently read this exact
clean checkout, verified its 13 manifest file hashes and the 14-file diff
restricted to `research/semantic_reentry_protocol`. Its reported gate is
831 passed and one historical strict xfail, not rerun by Core in this slice.
The result is supplied-plan correction, ordinary admission, replay, trace and
fresh no-op over already retained e4/e7 source rows. It is not an observed
external-world change or a general public Re-entry API. No new Core requirement
was found; no consumer code is merged by this slice.

## Scoped self-inquisition

Root ontology rites: NOT RUN, no root schema changes. The development skill
kept defaults and fixtures separate from protocol authority. Its completion
check applies only to the changed documentation and evidence, not a new
capability or release.

| Claim | Role | Observation | Unsupported transfer excluded | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| Main guide runs existing default admission | REFERENCE_IMPLEMENTATION | Exact command and public reopen/query/trace test | Default is not mandatory for every adopter | PASS |
| Shop keeps its correction history | CONFORMANCE_FIXTURE | Source bytes, e4 predecessor, quantity 2 and unchanged reads | No automatic correction inference or domain truth | PASS |
| Capability prose matches shipped surfaces | REFERENCE_IMPLEMENTATION | Public symbols, profile-role checks and existing runtime tests | No stable wire, alternate-interpreter proof or Assent cutover | PASS |
| Consumers supply requirements, Core implements reusable changes | ADOPTER_CHOICE | Separate frozen coordinates and explicit file ownership | No research-local authority promoted into Core | COORDINATED |

Future convenience remains unselected: generic source registration helpers,
concurrent writers, general migration, extra backends and exhaustive hardening.
The current CLI already exposes the end-to-end routes; this slice does not add
commands or claim that the CLI stops at contract compilation.
