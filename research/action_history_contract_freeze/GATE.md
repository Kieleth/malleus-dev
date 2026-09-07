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

## Run the bounded gate

Use the repository's existing configured development environment, declared in
`pyproject.toml`. Both producers run under that same interpreter. No extra setup
or dependency install is performed by the gate. The local Git object store must
contain both exact commits in `gate.json`; missing objects refuse, never fetch.

```sh
python scripts/check_compiler_compatibility.py --output /tmp/malleus-compatibility-result
```

The output directory must be new. This one command exports both immutable Git
trees, runs the nine historical tests, runs the whole relevant candidate suite,
and executes independent probes under both producers. Temporary archives and
generated histories are discarded; raw pytest reports/logs, probe outputs and
the final bounded receipt remain under the requested output directory.
Ambient Python paths and pytest options/plugins are removed in each worker.
Imported Malleus, test and research modules must resolve inside its archive.

`gate.json` identifies the historical runtime via `9ec32d4` (unchanged from
`2a11240`) and repaired runtime via `1be958e`. It binds all nine test names,
the current selectors/collection identity, raw outcomes and exact failed
assertion operands. This is a fixed repair audit, not a claim to test later
unbound working-tree edits. Changing a producer requires a reviewed new binding,
not a growing list of tests permitted to fail.

The candidate's expected raw result remains **1165 passed, 9 failed, 1 xfailed**.
The xfail is the retained old pure-preparation prerequisite, not a new exemption.
The bounded gate succeeds only when the historical result is **9 passed** and
both additional behavior probes also satisfy exact semantic parity. It never
reports the raw candidate suite as green.

The independent probe covers fresh supplier import, document admission and
assertion times, object-event admission, full public Shop population, and the
earlier correction/showcase runners. The last two predate population plans;
they prove graph/source/check/supersession parity, not population-plan tracing.
Their generated check receipts are paired by check/change names while retaining
their actual IDs and every value. Only explicit producer-derived receipt ID,
acceptance/materialization head and verification identity leaves may differ.
No domain value, source hash, modality, plan, time or graph-state digest is
exempted. The read-only Re-entry workflow is also executed by the raw suite;
its behavior assertions precede its final bound historical-receipt comparison.

The receipt binds both gate Python files, the manifest, selected commits/trees,
actual producer identities, output hashes and observed environment. Editing the
probe changes the gate-code identity. Code and binding must remain unchanged
throughout the run. Existing receipt files and equality tests remain untouched.
