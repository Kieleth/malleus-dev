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

RED: the new six-case test file reports 2 failed, 4 passed. The failures are
the public-doc and installed-acolyte guidance guards. The four behavioral
cases already pass and characterize existing behavior, not a runtime fix.
Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest
-q -p no:cacheprovider tests/contract_compiler/pareto/test_capture_coverage_boundary.py`
(the isolated checkout uses the existing project `.venv` by absolute path).
GREEN and final validation remain pending.
