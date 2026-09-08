# Supplier action entry: scoped implementation review

Date: 2026-09-08 UTC. REFERENCE_IMPLEMENTATION under the experimental one-action
attachment. Tests and recorded histories are CONFORMANCE_FIXTURE. The selected
supplier goal, actor identities and policies remain ADOPTER_CHOICE.

This adapter submits an authored action, not a synthesized one. It constructs
Core's existing original-context value, submits the context/action/proposal pair,
runs the actual TYPE producer and records the public epistemic policy result.
It does not authorize or execute an effect, produce a KCS, or complete Re-entry.

## Observed result

The explicit eight-file action-entry gate passed all 141 tests with no failure,
error or skip. It includes all 32 supplier proposal tests. The exact selection,
run coordinates and hashes are in `supplier-proposal-result.json`. This is not
the supplier authorization gate or the full Re-entry E2E gate.

The first focused run passed three tests: API shape, pure canonical original
context, and real supplier proposal/TYPE/ACCEPT with JSONL-only reopen. The saved
48-event history also reopened in a separate process. It contains an ACCEPTED
proposal and PENDING authorization, 25 protocol records, two accepted KCSs and
the unchanged O1/X1/relation/e4 supplier record history. Supplier quantity is one.
The graph digest remains
`sha256:8e4bc9cbbbcd68463cd2bbb94db8a8aa8be2255fa09b4bce7a4828423dc7e93f`.

That run alone did not establish the refusal path. The expanded focused run had
five passes and 21 failures. All failures expose the adapter's exception-surface
mistake described below, including test handlers with the same mistaken name.
Do not report the first three successes as a green complete module.

The dedicated corrected class regression had five failures before repair. After
repair the fast selection passed 12 tests, covering exact exception propagation,
no deferred dependency-attribute resolution in handlers, required arguments,
imports and actual checkout/gate binding. These runs overlap and are not added.
The complete eight-file gate then passed as stated above. Its independently built
positive history is byte-identical to the first focused history, SHA-256
`fee9b3304fa65f7e2d1c838023ae9aa181d83caa2dc706f1c1ecc029525e0fc4`.

## SP-3: refusal masking, fixed with a class guard

The first implementation looked up `compiler.ProtocolProgramRefusal` inside its
exception handler. The facade does not export that name. Python evaluated the
lookup while handling a failure, so AttributeError replaced the real refusal.
The successful execution path never evaluated the bad lookup.

Inspection also ruled out the facade's `ProtocolMachineProgramRefusal`: it is
a distinct exception for a different interpreter, not an alias for the finite
action-history runtime's refusal. The first tiny diagnostic regression included
that wrong substitution and failed during one exception's construction. Its raw
result is retained, but it is not the final class regression.

The repair removes the blanket upstream ValueError handler. Only local shape
errors and local JSON/time parsing errors are translated. Core and check-producer
typed ValueErrors propagate unchanged, without imports from private Core or a new
public exception alias. The regression checks identical exception objects, not
just equal strings. A structural test forbids dependency-attribute lookup in this
module's exception handlers. Real late-transaction negatives additionally check
the actual emitted finite-runtime exception class and unchanged ledger bytes.

The stale-check tests distinguish two boundaries. Movement before the actual
producer reads is a local STALE_BASE refusal. Movement after computation reaches
Core's STALE_PROTOCOL_BASE guard. Both retain only the deliberately intervening
evidence event, not an assessment or a guessed rebase. No outcome is supplied to
the producer. Its actual engine-unavailable path yields MonitorFailure plus an
UNKNOWN assessment and actual DEFER control, never a canned success.

## Boundaries and residual work

The original-context constructor receives no graph/writer/path capability and
performs no retention. Its graph-free read comes from the already verified Core
factory boundary; arbitrary forged Python objects are not authenticated history.
The original context alone is not the full Re-entry Contract. Synthesis, model,
executor/observer identities, budget and stopping/evidence closure remain to bind.

Submission retains the exact supplied action record identity and checks its seven
payload fields against the payload digest. Compiled shape/TYPE validity does not
prove source agreement, model agreement, goal satisfaction or legitimate authority.
Those obligations remain in their declared stages. No oracle or historical e7
supplies this prefix's source. Test setup calls actual public source/KCS admission;
production code imports no test helper or private Core implementation.

Only the owning Core append gate writes protocol records. The whole workflow is
not one transaction. Each declared pair or decision/transition has its existing
atomic boundary, and no implicit retry is added. The complete domain frame stays
unchanged across proposal, checks and action-only acceptance. JSONL-only replay
does not invoke check producers.

The Malleus development/adopter boundary rules keep this research-local. Root
ontology profile and shared API promotion are not claimed; root schema rites are
not applicable to this cut. One implementation establishes no empirical replacement
or independent-monitor claim. No Core, ontology, locked Shop fixture or paper changed.

The known broader population gate still has 512 passes and one Core-confirmed
historical-example failure. The action-entry selection neither waives that failure
nor replaces the final supplier E2E gate. No new Core prerequisite has been found.

Next: actual direct-grant checks and authorization, the identified controlled
executor/observer, full pure synthesis input closure, observed-source KCS admission
and fresh linked SATISFIED reevaluation without a candidate, append or effect.

## Landing coordinates

On the verified Core base `90146c3`, this cut is `8d110ab` contract/API RED,
`97b9ebc` implementation, `04cbfb4` refusal-class RED and expanded conformance,
then `940ff15` narrow error handling and verified GREEN. The implementation tree
is `d85714e15e3f8912c8666bb2d1a1cadbc144b9ca`. Its four changed files are confined
to the Re-entry research directory. The larger base-to-head diff also contains
the previously carried and independently tested Re-entry work, not Core edits.

Supplier authorization is a separate subsequent cut at `430dc33` contract/API RED
and `1ec9439` first implementation. Those new files were not selected by the
141-test action-entry gate and are not certified by its result. Ruff, formatting,
exact checkout checks and the base-to-head whitespace/scope audit pass for the
action-entry cut. Neither cut is merged, pushed or published.
