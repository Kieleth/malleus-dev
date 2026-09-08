# Semantic Re-entry supplier slice: landing audit

Date: 2026-09-08. Instrument: malleus-inquisitor skill, rubric v12 resolved from
this checkout's `src/malleus/inquisition/rubric.yaml`. Scope is this research
slice, not a repository-wide conformance or root-ontology purity claim.

Audited implementation and fresh unified runtime:
`dc74a6ded9bc1928cacd50eb53b4d9f1becc2b71`, tree
`28f4b35c3109649e1cf82c8edd5109aa22957460`.
The unchanged manifest was selected at `0d0773e`; the later runtime includes
the additional type-binding lifecycle regression and its canonical repair.
Core base: `90146c380994621a2f8df25876affd03fc9e57e3`.

Claimed profiles: compiler-enabled state-version population and experimental
single-action history attachment. Without those profiles the composed
source/action/observation/KCS claim is not made. Root ontology profile review,
public API promotion, package release, real suppliers and robotics are NOT CLAIMED.
Mechanical root-ontology rites: NOT RUN, profile not claimed by this audit.

## Current verdict

Earlier focused synthesized E2E: PASS, 35 tests. Current-bound replay/epoch
correction: PASS, 3 tests. Repaired four-case lifecycle: PASS, 4 tests.
Fresh unified gate: RUNNING, 388 tests collected across 15 modules.
No final landing verdict is issued until that run and the retained evidence
audit complete. These counts are separate observations and are not added.

## Closed findings

### H1. Incompatible historical witness in the unified gate

Rubric: `evidence_does_not_transfer`, `dependency_pin`.
Where: `supplier-reentry-gate.json:19`, historical witness runtime fixture in
`test_replay_noninvertibility.py:35`.
The old witness requires Core `2af45e0`; silently running it under `90146c3`
would either refuse correctly or require invalidating its original binding.
RED `fed017a` reproduced the exact incompatible-epoch refusal. Correction
`0d0773e` preserves its bytes and required identity, lists it separately as
historical evidence, and selects the current supplier witness instead.
`test_supplier_replay_laws.py` guards the explicit CORE_COMMIT convention,
current Core source tree/origin, historical file hash and disjoint selection.
Its three tests pass, including unknown/historical-pin refusal and two real
JSONL histories with the same accepted graph but different log/receipt identities.
This is not a universal dependency resolver or a waiver of the historical run.

### H2. Replaceable strategy output escaped the bound goal

Rubric: `gate_integrity`, `fail_closed`, `module_declares_its_interface`.
Where: `supplier_reentry.py:989`, regressions in
`test_supplier_reentry_boundaries.py:53`.
A schema-valid different target, or a faulty model hidden by the strategy,
previously yielded a candidate. The current synthesizer independently validates
model/frame agreement and the exact permitted payload, and gives the strategy
defensive copies. The focused 35-test run closes the target, prediction and
input-alias cases. Adversarial implementations prove refusal, not replacement.

### H3. Declared lifecycle index absence was mistaken for malformed input

Rubric: `fail_closed`, `protocol_authority_is_data`.
Where: `supplier_reentry.py:622`.
The selected bundle declares indexes before any transition populates them.
The reader now checks the exact retained bundle declaration before treating
an absent entry as pending progress. An undeclared index still refuses.
Both direct cases and post-proposal pending evaluation pass. No Core
interpreter or state-transition program was copied into the reader.

### H4. Implementation-role grammar was not closed at binding

Rubric: `silent_drop`, `citation_integrity`.
Where: `supplier_reentry.py:354`.
Required entrypoints and the different executor/mapper role shapes are now
checked before binding. Missing entrypoints, extra role fields and unknown
ambiguity strategy refuse in the focused suite.

## Finding repaired, final unified verification pending

### H5. Type-changing observed binding falsely closes the episode

Rubric: `gate_integrity`, `encodable_at_the_gate`, `evidence_does_not_transfer`.
Where: `supplier_reentry.py:784`.
The complete observed-source binding uses Python object equality. Integer one
and Boolean true compare equal. The `binding-type` full-lifecycle regression
at `0bb35dc` injects faulty mapper serialization, then uses actual public
preparation/admission/replay. RED: one failure, SATISFIED instead of the required
REFUSED/EVIDENCE_DISAGREEMENT. No accepted view or KCS boundary was substituted.
The source-derived quantity-two fact is not disputed; the exact episode-binding
claim is false. Repair `dc74a6d` compares canonical bytes of the whole binding,
preserving JSON types recursively. The corrected four-case lifecycle passes:
this case refuses closure, and ordinary and failed-after-write closure still pass.
Final closure still requires the fresh unified gate. Corrected JUnit SHA-256:
`1fd98559ce110cefa5adc55aecb4fc56335686193f14935964311e2a88a55054`.

## Claim-by-claim judgment

| Claim | Role | Direct evidence | Unsupported transfer excluded | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| One log, KCS-only accepted knowledge | PROTOCOL_INVARIANT | Actual Core admission and replay; graph unchanged through every pre-admission checkpoint | No direct KG writer or substitute change identity | PASS for this consumer |
| Single-action lifecycle | OPTIONAL_PROFILE | Exact retained supplier bundle, actual Core transition owner and native refusal tests | Not default Assent cutover or multiple-action support | Focused PASS; unified pending |
| Exact-two goal and full complement | ADOPTER_CHOICE | Frozen case, quantity-three refusal, complete record/history comparison | Shortfall zero is not equality, delivery or demand fulfilment | PASS |
| Pure pinned synthesis | REFERENCE_IMPLEMENTATION | Graph-free immutable view, canonical contract, source closure, stale-before-model and no-I/O tests | No effect, retention or admission capability | PASS |
| Typed candidate and real checks | REFERENCE_IMPLEMENTATION | Existing SupplierOrderAmendment; actual TYPE and DIRECT_GRANT producers and policy decisions | TYPE does not prove usefulness; grant checks do not prove grantor legitimacy | Focused PASS; unified pending |
| One controlled source attempt | REFERENCE_IMPLEMENTATION | Fresh dispatch before `_attempt`; no repeat path; exact pre-state bytes checked | Not crash recovery, concurrency, exactly-once delivery or real supplier integration | Focused PASS; unified pending |
| Independent observed-source correction | REFERENCE_IMPLEMENTATION | Observer reads the file; adapter binds capture, execution, contract and population trace | Receipt/model/oracle bytes do not become observed state | PASS |
| Fresh episode closure | REFERENCE_IMPLEMENTATION | Linked accepted KCS required; retained-only and unrelated corrections refuse closure | Quantity two alone cannot close an acted episode | PASS |
| Non-invertible replay | CONFORMANCE_FIXTURE | Distinct valid histories, equal current graph, unequal history/receipt identities | Not decoding, ViewDelta PutGet or reconstruction of the past from the graph | PASS |
| Replaceable implementations | ADOPTER_CHOICE | Explicit engine/adapter identity and boundary contracts | No second conforming implementation was exercised | NOT DEMONSTRATED |

## Write-path and dependency census

The synthesizer and model own no history or effect capability. The immutable
read factory constructs a disposable graph only to validate the public replay
digest; it does not retain that graph or write accepted state.
`supplier_proposals.py` and `supplier_authorization.py` run actual check
producers and submit their records to Core. They do not accept caller-selected
positive assessments. `supplier_execution.py` is the sole controlled source
writer, downstream of a newly applied dispatch. `supplier_observation.py`
captures separately and never composes KCS. `supplier_observed_source.py`
retains ordinary source/plan evidence and prepares the existing KCS, stopping
before admission. The caller uses the public admission boundary.

Each append has Core's atomicity; the whole workflow is not one transaction.
For example, a capture may remain retained if the subsequent observation
append refuses. Missing receipts remain pending and never authorize retry.
The temporal history is preserved, not deleted when the goal is satisfied.

There are two deliberate private Core imports in research-local authoring:
`supplier_program.py:11` uses canonicalization/bundle validation and
`supplier_initialization.py:22` uses the raw artifact digest helper. Actual
check producers and finite-program builders are also repository-local Core
experiment boundaries. This follows the pinned experimental handoff, not a
stable packaged SDK. The pure synthesizer and observed-KCS adapter use no
private accepted-state writer. A blanket claim that all adapters use only
public stable APIs would be false.

Syntax-aware inspection found no Core imports from research/tests, and root
ontology imports only `linkml:types`. The base-to-head diff at the selected
commit contains 88 new files, all under this Re-entry directory. It includes
previously approved design/history and earlier stages, not 88 new runtime
components. Core source, shared ontology, locked Shop bytes and papers are
unchanged. Ruff check and formatting check pass for all 31 Python files.

## Evidence and limits

The focused histories were independently reopened in a new Python process
with research/test imports refused. Ordinary and failed-after-write cases each
contain 74 events and three accepted KCSs; unchanged-success contains 66 events
and two accepted KCSs. The failed receipt remains FAILED. Both observed
corrections yield the same current graph, not the same history.

A second fresh process refused test/effect-module imports and evaluated only
the retained goal/rule/context through the pure API. File opens and model
invocation were forbidden during binding/evaluation. Results were SATISFIED,
SATISFIED and REFUSED, all with zero candidates and unchanged ledger bytes.

The repaired four-case run was also independently replayed and evaluated in
fresh processes with the same import/I/O restrictions. It adds a fourth
CONFIRMED observation and valid quantity-two fact whose corrupted binding now
refuses episode closure. Exact current identities and environment observations
are in `supplier-reentry-replay-evidence.json`; the earlier three-case results
above are distinct historical observations, not substituted current hashes.

Source identities assume this identified Python/Core process. Hashes are not
proof of actor legitimacy, source truth or protection against arbitrary
in-process monkeypatching. Distinct observer/executor actors do not prove
organizational independence. The selected one-attempt policy has no deferred
review queue or automatic repair claim. Canonical source retention supplies
byte lineage, not an inverse semantic mapping.

The older full population gate's historical document-example mismatch is
recorded at the pinned Core base and is not covered or waived here. Core later
reported a separate fixture-only correction; it is not silently incorporated
into this checkout. Full repository CI and release conformance remain outside
this bounded landing verdict.
