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

Pending RED, GREEN and combined validation. No completion claim yet.

Consumer coordination: Robotics reported 191 focused checks passing against
the frozen Core coordinate above, with no generic capability request. This is
consumer-reported evidence, not a completed robotics experiment or a new Core
gate. Re-entry was already dispatched to its bounded consumer RED-to-GREEN
work. Both received the approved ownership boundary and continue independently.
Neither is authorized by this slice to expand Core or edit shared files.
