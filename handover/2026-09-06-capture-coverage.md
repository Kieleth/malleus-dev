# Capture coverage and relationship guidance

## Accepted cut

Luis approved three Core requirements: explain the existing census as structural
mapping with or without declared gaps, clarify proposition identity and
source-supported relationships, and prove the boundary with a neutral Small
Shop example. This branch is isolated from Sol's frozen run and the shared
checkout. Base: `70eec648eb2db62d28fb51a1bb9589fb68bab70b`.

The census explanation is `REFERENCE_IMPLEMENTATION` guidance for the optional
document-assertion adapter. The example is a `CONFORMANCE_FIXTURE` under the
compiler-enabled source-assertion structural-history profile. Domain vocabulary
and interpretation remain `ADOPTER_CHOICE`. Without those profiles, neither the
census nor this admission/replay proof is claimed.

The smallest observation is a synthetic note that states quantities and a
relationship, with a capture mapping only the quantities and claim text. The
existing counter reports FULLY_FORMALIZED when there are mappings and no
declared gaps. A supplied valid relationship survives admission and replay;
a supplied dangling relationship refuses without writing. None of these
checks detects an omitted semantic relationship.

Reuse the public compiler, document adapter, structural history bundle, query,
trace and installed acolyte. No runtime API, receipt field, wire value, ontology
pack, inference, quota, evaluator, regex extraction, or metrology change belongs
in this cut. Historical fixtures and receipt bytes remain untouched.

Pre-action check: local files and tests only, no server interaction or endpoint;
required data is explicit; no authoritative mechanism is replaced. The observed
problem is misleading guidance, not a faulty counter. Behavior tests characterize
the existing counter; guidance tests must fail before the correction.

## Evidence

RED `97baf9636273d15484251e2931fdfeae9e42001d`: the new six-case test file reports
2 failed, 4 passed. The failures are
the public-doc and installed-acolyte guidance guards. The four behavioral
cases already pass and characterize existing behavior, not a runtime fix.
Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest
-q -p no:cacheprovider tests/contract_compiler/pareto/test_capture_coverage_boundary.py`
(the isolated checkout uses the existing project `.venv` by absolute path).
GREEN `2ba6e7c84cf414ed105db1b12cb5c86a6744f81b` changes only the acolyte,
public compiler documentation and its existing Inquisitor wording guard.
`229ab9d65b03fb22a82995a856ee8e96dddd5eb4` additionally checks exact capture
bytes recovered through the public trace, not merely the retained record ID.

The public receipt values remain FULLY_FORMALIZED, PARTLY_FORMALIZED and
UNFORMALIZED. The docs label them mapped fields with no declared gaps, mapped
fields with declared gaps, and no mapped fields. No runtime output changed.
Proposition IDs identify records; optional labels do not replace statements or
retained evidence. Relationship mappings need source support, direction,
endpoints and retained context/attribution, not two names in one sentence.

Verified checks in the isolated project environment:

- New test file: 6 passed, including exact reopened capture bytes.
- New file plus `tests/test_inquisition.py`: 113 passed, 1 skipped. The skip
  requires an untracked doctrine file absent from the clean checkout.
- Complete `tests/contract_compiler/pareto` plus
  `research/ontology_driven_kg_realization/experiments/small_shop`: 699 passed,
  3 failed. Each failure also reproduces on the unchanged base `70eec64`.
- Changed-file Ruff check, new-file format check, skill quick validator and
  `git diff --check`: passed. The existing Inquisitor file has unrelated
  formatting differences; no bulk formatting changes were retained.

## Separate baseline debt

Three existing evidence-regeneration guards fail on both the unchanged base
and this correction:

1. `correction/test_correction_vertical.py::test_checked_in_evidence_is_exactly_regenerated`
2. `object_event/test_run.py::test_ret040_admits_reopens_replays_queries_and_traces`
3. `showcase/test_evidence.py::test_regeneration_is_canonical_byte_identical_and_matches_runner`

Paths above are relative to the Small Shop experiments directory. Regenerated
receipt/explanation identities differ from the committed expected bytes. This
read-only reproduction establishes pre-existing drift, not its introducing
commit. Existing failing guards already expose the class. Reconcile current
versus historical evidence in a separate bounded cut; do not overwrite frozen
receipts to make this correction green. No full-suite-green claim is made.

## Self-audit and exclusions

Self-inquisition used source rubric version 12 and the Malleus development
completion gate. Lowest affected profile remains the optional document adapter
under compiler-enabled structural history. The new public-path fixture proves
composition for this case, not domain completeness, inference, truth, arbitrary
adopter adequacy or cross-language replaceability. The ignored local
`MALLEUS_INQUISITION.md` contains the detailed scope table. No root ontology or
runtime boundary changed, so no root-schema rite is claimed.

All twelve frozen Sol inputs and its accepted ontology were verified unchanged.
Sol's population plans are ready but have not yet passed the parent admission
gate. This correction is not a controlled comparison with that frozen run.

Final scoped gate after governance: 117 passed, 1 skipped. Exact selector:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/contract_compiler/pareto/test_capture_coverage_boundary.py \
  tests/test_inquisition.py \
  tests/test_docs.py::test_strict_html_build_is_source_pure \
  tests/test_docs.py::test_autodoc_and_autosummary_render_the_existing_package_root \
  tests/test_docs.py::test_doctest_builder_executes_an_infrastructure_only_example \
  tests/test_contract_compiler_ledger.py::test_overseer_ledger_and_projection_are_current
```

The isolated checkout used the existing project interpreter by absolute path.
The standalone ledger checker validates all 419 entries at OVR-000419,
`sha256:24801d5f3460666237e790806ce0c5dab5f624994da82003cf46e6da7c169448`.
Governance commit: `672f26aa3f8abe65f7da2a43ff411e5353439f7c`.

A broad repository attempt started before governance and was interrupted after
1,092 passed, 5 failed and 3 deselected. All five failures were the then-pending
document digest revision, not new runtime failures. A larger post-governance
selection was interrupted after 254 passed, with no failures, in favour of the
completed scoped gate above. Neither interrupted run is a full-suite result.
No package/dependency work or cross-task publication was performed.

## Local main integration

The six isolated commits landed through `44e280834a0735be7a6ff3b2f21597e9d3cae48c`.
All eight scoped files match the validated isolated branch exactly. The original
TDD commits remain reachable through the local tag
`evidence/capture-coverage-2026-09-06`, pointing at
`ae71c8a16d1e648fb43d51603d2fbd31b435f11c`. The existing ledger guard requires
this evidence reference because cherry-picking gives the main copies different
IDs. Nothing was rewritten. Any later publication must carry this evidence tag
with the commits; no remote push occurred in this task.

On local main, all 419 ledger entries validate and the six new cases plus the
existing installed-playbook guard pass, 7 passed. Unrelated work remains intact.
