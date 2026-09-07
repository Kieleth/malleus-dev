# Two-producer compatibility gate

Operator-approved CONFORMANCE_FIXTURE for the optional compiler-enabled
profile. This is repository-local verification, not a new runtime, wire,
release policy or replacement for the full repository gate.

Claim: preserve the nine frozen exact-reproduction tests under their original
producer, run the entire relevant suite under the repaired producer, and
independently compare the resulting Shop and document semantics.

Observation: all nine historical tests actually pass. The raw candidate suite
retains its real outcome. A known failure is classified only by its exact test,
AssertionError location and comparison operands, never by test name alone.
Unexpected failures, skips, collection changes, producer mixing or semantic
differences fail this bounded gate. No assertion, fixture or receipt is edited.

Reuse: local immutable Git archives, the configured project interpreter and
pyproject dependencies, pytest report hooks, existing public compiler and Shop
runners. Each subprocess imports only its selected archive. No download,
dependency installation or alternate environment is introduced.

The semantic comparison executes current admission/reopen/query/trace paths
independently of the historical equality assertions. It compares full graph
records and retained source/capture/plan meaning, not just pass counts. Only
enumerated producer-evidence and resulting history identity differences are
permitted. No general equivalence or truth claim follows.

TwoProducerGate consumes OriginalProducerAndFrozenTests
TwoProducerGate consumes RepairedProducerAndRelevantSuite
TwoProducerGate consumes IndependentSemanticComparison
TwoProducerGate produces BoundedCompatibilityEvidence
TwoProducerGate conformsTo GateRefusalTests

Excluded: action runtime, ontology changes, receipt rewriting, hidden skip or
deselection, broad CI replacement, governance append, merge, push and release.
