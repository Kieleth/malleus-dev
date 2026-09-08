# Semantic Re-entry contract review

Status: PROPOSED semantic draft. The operator authorized definition only.
Nothing here authorizes implementation, promotion, integration or publication.

Read the [Core contract](CORE_CONTRACT.md) for persistence, validation and
replay, and the [adopter contract](ADOPTER_CONTRACT.md) for the goal, action,
check producers, observation and test obligations. The earlier README and
three executable/evidence files remain frozen at `2da25941d5c2a55b43fb925a7b812939a8b7158a`.

## What the draft settles for review

One log records the action lifecycle and accepted KCSs. Four coordinates remain
distinct: full log position L, accepted domain context D, accepted protocol
proposal head A, and immutable original proposal context O. They are derived
views or bindings of that one history, not separate histories or new KCS IDs.

Accepting an action proposal advances A but not D. Dispatch advances L and
action state, not D. Recording execution or observation also leaves D alone.
Only ordinary KCS acceptance changes accepted supplier knowledge. Receipts
may be recorded after intervening domain change; authorizing another effect
still requires current context. Old action pins are never silently replaced.

The synthetic case proposes one first-revision action to amend B/Y/1 to B/Y/2,
one dispatch attempt and no automatic retry. The proposed goal is equality to
two, not at-least-two, delivery or customer fulfilment. Check producers compute
structural and direct-grant assessments from bound inputs. A separate observer
captures actual new bytes. Pre-retained e7 never counts as that observation.
Pending, refused, satisfied and execution-success claims remain distinct.

## Actual decisions remaining

The draft is not yet an executable grammar. The next approval must cover:

1. A separate protocol-acceptance coordinate A and its explicitly retained
   initialization checkpoint. Reusing the KCS head by name would change
   existing action semantics. The closed checkpoint/context shapes and digest
   recipe must then be frozen before RED.
2. This one-action subset, conservative stale/no-repeat/refusal rules, exact
   equality goal and proposed structural/direct-grant check producers. All
   concrete fixture IDs, artifacts and expected results remain explicit freeze
   inputs. No current code is claimed to produce these new checks.
3. The scope of the necessary interpreter/persistence work. Current machine
   records and policy grammar cannot express the required existing action
   records and checks. The proposed capability list is bounded, but it is more
   than an append wrapper. Exact grammar/instruction mappings need review and
   mechanical closure before implementation; no generic language is approved.
4. Shared promotion authority. There is only one demonstrated consumer of this
   proposed composition. Shared generic API/vocabulary work needs a second
   consumer or an explicit bounded operator exception. A research-local
   substitute writer cannot satisfy the original public-seam E2E requirement.

Approving a semantic direction does not approve unknown implementation
semantics. If the frozen grammar requires a further capability, changed record
meaning or wider claim, surface it before code. A fresh implementation baseline
must be bound after the agreed Core contract exists; this isolated design
commit is not a runtime rebind or merge with current main.

## Evidence and exclusions

Audited Core: `2a11240556532c2b6160ac0bfa5ab1165e862fd2`, tree
`2f376922f108601d871361d9a7b53e4b5e156ad5`. The nine source hashes in the frozen
evidence packet still match this checkout. The interpreter, effect handlers,
effect ontology and landed consumer are unchanged from the prior audit base.
Core independently reported eight seam probes passing against this baseline.

The current-main compatibility run after drafting passed 36 tests in 15.31
seconds: the eight seam probes, existing generic-effect lifecycle tests and
landed Re-entry integration and guardrail cases. That proves existing
boundaries independently, not their proposed composition. All three Markdown
files parse and the staged diff passes whitespace checks. The full runtime
gate was not repeated for these documentation-only additions.

Core read both contract files completely and reported no material transcription
error or impossible existing-record requirement. It confirmed the proposed
check-producer semantics and the explicit residual bootstrap, grammar,
capability and promotion decisions. That review does not establish executable
contract conformance or authorize implementation.

No new runtime, conformance result, ontology, source
fixture, paper file, shared main change, installation or external-domain call is part of
this design. This packet does not prove replaceability, world truth or a full
external-action E2E.
