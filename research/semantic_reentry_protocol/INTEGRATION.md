# Semantic Re-entry: bounded Shop integration

Current result: implemented internal, retained-observation correction. The
earlier prerequisite packet and consumer RED specification remain historical
and byte-identical. Their blocked wording is not the current integration status.

Core prerequisite: `79ae2feff7fc59436ef405fd91fe5a38c8253394`, tree
`f1b7bbb9b98df036edbbb813b746f97552b47247`.
Executable consumer GREEN: `195cdcb70838f6701b014018b9bd1faaa14db36c`, tree
`a42f6842f1a6d167ab6a6a9cb7fed0f1d6369f18`.

## What actually happens

```text
empty accepted graph
  -> ordinary Core genesis and population: O1, X1, contains:O1:X1, B/e4
  -> caller requests the explicitly mapped e7 correction
  -> pure assessment: READY, accepted graph unchanged
  -> caller retains required plan evidence, ledger advances, graph unchanged
  -> caller binds fresh Re-entry Contract and immutable Core context
  -> pure synthesis: one existing KnowledgeChangeSet, no writes
  -> ordinary Core admission: e7 supersedes e4
  -> JSONL-only reopen: B/Y/2, source trace, unchanged RET-010 complement
  -> newly bound invocation: zero candidates and zero writes
```

The first correction is not an external-world request. The source already
contains e4 and e7. Processing e7 supplies new evidence to this accepted state;
the experiment does not observe a supplier system changing during execution.
There is no demand record, SupplyGap finding, ActionProposal, authorization,
executor or observer in this slice. It does not complete the original external
order-amendment ladder.

## Exact fixture mapping

The existing correction fixture is
`research/ontology_driven_kg_realization/fixtures/small_shop_fulfilment_correction_v1`.
It extends the Shop fixture; the locked original fixture is not redefined.
The source is `input/sources/supplier-order-history.jsonl`. The explicit mapping
is `experiments/small_shop/correction/mapping.json` under the same research root.

| Accepted source occurrence | Current record | Properties | Explicit time |
| :--- | :--- | :--- | :--- |
| e4 | supplier-order-state:B:e4 | B, Y, quantity 1, occurrence e4 | ORDER_ONLY e4 |
| e7 | supplier-order-state:B:e7 | B, Y, quantity 2, occurrence e7 | ORDER_ONLY e7 |

The mapping, not row order, declares e7 supersedes e4. The baseline complement
is O1, X1 and contains:O1:X1. Tests compare the complete non-supplier record
families after replay, not just their count. Existing population templates are
instantiated with the current effective-contract and history-profile identities;
their source, record, derivation, valid-time and supersession data are unchanged.
The fixture's independent oracle is read only by tests, never by synthesis.
The consumer validates a supplied population plan against these source and
mapping bytes. It does not discover observations or implement a general
source-to-plan adapter.

## Boundaries and authority

`consumer.ReentryContract.from_bytes` binds a closed canonical local contract.
`consumer.assess_request` returns immutable READY or SATISFIED, or typed refusal.
`synthesis.synthesize` receives immutable artifacts and returns a tuple containing
zero or one `malleus.compiler.KnowledgeChangeSet`, or raises a typed refusal.
There is no second KCS identity or serializer.

The producer uses the public `compile_population_plan` and `compose_change_set`
functions. The caller gets `KnowledgeChangeContext` through
`KnowledgeChangeHistory.composition_context()`. Preparation, retention and
admission remain caller work. No prepared KCS is passed to synthesis. Tests use
Core's separately prepared KCS only as an independent byte-equivalence check.

The exact local synthesizer identity hashes consumer.py and synthesis.py with
a versioned separator at module loading. Invocation performs no ambient I/O.
The Core commit separately identifies the compiler, composer and replay runtime.
The contract and exact observed result are retained in
[integration-result.json](integration-result.json), not as a new Core record.
Core's accepted KCS retains its normal source, mapping, plan and profile closure.
This does not claim that the local Re-entry Contract is reachable from Core's
trace, or that these research-local names are a public package contract.

The coordinator is trusted to extract record history from public replay and
supply the corresponding immutable compiler inputs. Synthesis validates active
projection records against Core's accepted-state digest using a disposable
graph. That validation graph cannot change accepted state. The copied history
is not an independently authenticated history proof. Neither the local digest
nor Core's context fingerprint authenticates a hostile caller or sandboxes
arbitrary Python code.

## Laws and counterexamples

| Boundary | Observation |
| :--- | :--- |
| Representation round-trip | Canonical local contract and existing KCS parse back to the same value. |
| Forward agreement | Ordinary admission and replay yield the exact requested e7 record and trace. |
| Complement preservation | Every other active record and relation remains unchanged. |
| No-op and quiescence | Exact current e7 plus supersession yields no candidate, retention or write. |
| Stale base | Old contracts and evidence-only intervening appends refuse, even if graph contents match. |
| Choice and budget | Competing matches refuse AMBIGUOUS, unsupported policy refuses, zero budget refuses an unsatisfied request. |
| No writing authority | Invocation works while file I/O, history writers and original live-graph mutation are guarded. |

These are source-backed ViewDelta results. Semantic replay is interpretation,
not decoding, and this producer is typed putback, not inverse replay. Generic
GoalPredicate search, reverse-history reconstruction, a second-history
non-invertibility witness, and external ActionProposal model laws are not
established by this slice. No symbolic result is presented as a world change.

Adversarial review found four concrete counterexamples after initial GREEN.
They were committed RED at `fd09ffbd386513d5986771cac4490ffda005beb8`:

| Defect class | Guard and hard test in test_guardrails.py |
| :--- | :--- |
| Valid locator cites the wrong source row | Exact source ID, row ordinal, field and target-path derivation equality. |
| Missing mapping binding hides an invented property | Unique, complete coverage of selected row fields and output properties. |
| Rebound projection fabricates satisfaction | Validate the active projection body against the Core state digest before no-op. |
| Nested malformed projection leaks AttributeError | Validate object/array shapes and return MALFORMED_INPUT. |

The RED run failed all four cases. An independent read-only reviewer reproduced
the defects and reran all four after the guards; all passed. No additional Core
requirement was identified.

## Verification and landing

The declared project Python environment ran 76 local tests successfully, with
one strict historical xfail. The combined compiler Pareto, complete Small Shop
and Re-entry gate passed 831 tests, with that same xfail. It preserves the old
demonstration that population preparation writes retention anchors. It does not
mark the new pure composer as blocked. Changed-file Ruff check and format pass.

From the repository root, using the declared project environment:

```sh
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider research/semantic_reentry_protocol
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto research/ontology_driven_kg_realization/experiments/small_shop research/semantic_reentry_protocol
```

The integration test recomputes and compares the complete retained result JSON.
No network, paid calls, new dependency or ad hoc installation is required.
This is not a full-repository, clean dependency-resolution or release claim.
The implementation was also checked from a separate clean detached checkout;
its result and the file hashes are recorded in integration-evidence.json.

Landing order is the exact Core prerequisite first, followed by this isolated
consumer series: `da90d8e`, `59083b5`, `925a90b`, `7948da2`, `fd09ffb`,
`195cdcb`, then the evidence-only handoff. The first two copy the original
prerequisite and consumer RED commits without changing their files. No merge,
shared branch update, push or publication is performed here. The base-to-head
diff is confined to research/semantic_reentry_protocol.

## Scoped self-inquisition

The local contract and producer are REFERENCE_IMPLEMENTATION. The tests and
retained result are CONFORMANCE_FIXTURE. Mapping, exact complement, budget,
stopping and ambiguity policy are ADOPTER_CHOICE. The lowest affected profiles
are compiler-enabled semantic history and state-version. Without this consumer,
Core still offers structural composition and admission, but not these local
source-agreement and stopping rules. No profile becomes mandatory for Malleus.

Dependency tuples: assessment consumes bound source/mapping/plan/projection;
assessment implements local ViewDelta policy; synthesis consumes the local
contract and Core context; synthesis produces existing KCS; admission consumes
KCS; replay produces accepted KG. No new shared protocol role is promoted.

Root ontology rites: not run, no root ontology change. No source truth,
epistemic assent, external success, stable wire, public Re-entry API, hostile-code
isolation or empirical replaceability is claimed. A second independently
implemented producer must pass the same boundary before claiming replacement.
