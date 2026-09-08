# Supplier Re-entry integration

Status: ACTIVE IMPLEMENTATION, not an executed supplier E2E.
Core's resume gate passed on 2026-09-08 UTC. The historical PROPOSED and blocked
labels in older documents preserve their original dates; later approvals and
the exact verification below supersede those status labels, not their semantic
constraints.

## Workspace and dependency

Work only in `/private/tmp/malleus-reentry-integration.waW6z7/repo` for this
integration. Branch: `codex/semantic-reentry-e2e`.
Core base: `90146c380994621a2f8df25876affd03fc9e57e3`, tree
`609979f5d356ebb43c1288d80ea8f4f53d1f2613`.
Core implementation: `73d1a527dd237e5546d86d5c0470e9e056d41e16`.
The first integration commit `983629f` carries the unchanged approved Re-entry
directory from `458b999c8f71f068152ca8dd59f4c63c4861a789`. Its tree was
`280877bc03f1740ffa7bafcb1f8223fc9acaee00`. The earlier protocol proof was already
present in Core with the identical tree `1b881da52abeb0fffa34a5b54e5860545fb1f57d`
and was not rewritten.

Core reports 643 passes in four disjoint final runs. Independent Re-entry
verification passed 175 correction tests on the earlier correction, then 16
tests on the final handoff, including both real Shop composition tests. These
counts describe separate runs and are not added. Independent fresh-process
replay from the exact extracted Core wheel reproduced the 86-event history
with research/test imports denied. The consumer resume report is
`/private/tmp/malleus-reentry-handoff-review.oF9XmR/MALLEUS_INQUISITION.md`, SHA-256
`8deaa63fecabb3c2ed298607df308d17b2ec5d86577867a015c0f4acb6f3bc86`.

No Core prerequisite remains open at this gate. A genuinely missing contract
found during integration goes to Core or Luis; no substitute writer or public
change identity may fill it. Robotics is an independent consumer.

## Bounded implementation contract

Claim: the approved exact-two supplier goal can produce a pinned action, pass
the real one-history lifecycle, cause one controlled synthetic file attempt,
and reach accepted B/Y/2 only through separately observed bytes, ordinary KCS
admission and replay. Fresh satisfied reevaluation emits nothing.

Smallest observation: every checkpoint before observed KCS admission retains
B/Y/1; only admission makes B/Y/2 current. O1, X1, their relation and all
unmentioned history survive. Failed receipts remain failed even when separate
observed bytes support a correction. No receipt or prediction is source bytes.

Reuse: the frozen `supplier_commitment_v1` case, exact existing Small Shop TBox
and RET-010 inputs, existing pure model/mapper, public compiler/population/KCS
facade, Core's selected finite-program artifact and actual check producer.
Existing ActionProposal and protocol record identities remain unchanged.

Exclusions: demand fulfilment, delivery, causal proof, external/paid calls,
physical effects, real suppliers, retries, multiple competing solutions,
new Core vocabulary, second ledgers, direct accepted-graph writes, generic
frameworks, main integration, package publication and paper changes.

Lowest affected profile: experimental action attachment plus compiler-enabled
state-version population. Without those selected profiles, this combined
effect-to-observed-KCS claim is not made. The supplier goal/operator/preservation
policy is ADOPTER_CHOICE; executable stages are REFERENCE_IMPLEMENTATION;
frozen inputs and tests are CONFORMANCE_FIXTURE. None is new Core authority.

## First contract freeze: supplier action

`SupplierOrderAmendment` is a research-local concrete subclass of existing
`ActionProposal`, not a new change identity. It adds these required typed slots:
`logical_source_id`, `supplier_order_id`, `product_code`, `expected_quantity`,
`requested_quantity`, `expected_source_digest`, `new_source_occurrence_id`.
Quantities are integers; the other values are strings. `action_type` is the
fixed `AMEND_SUPPLIER_ORDER` literal. Existing provenance, action key/revision,
payload hash and authorization-policy fields remain inherited and checked.

The action schema does not hard-code B, Y, quantity one or quantity two. Those
are the already approved selected goal and sole operator, validated by the
Re-entry contract, model and executor. Source digest syntax and payload/hash
agreement are executable boundary obligations, not a false claim that basic
string typing proves them. The source schema remains unchanged.

Exact supplier YAML plus exact Assent/root/LinkML type bytes are compiled by
the public compiler. No LocalAction import, weakened Assent declaration,
date-to-string workaround or hand-built compiled contract is permitted.
The resulting contract identity must come from that actual compilation.

The schema cut passed 23 focused tests after an initial 23 setup-error RED
named the absent YAML. This is actual exact-source compilation and record
validation, not proposal admission, authority or an effect. Its SHA-256 is
`15bdd3144f853dd874d19b73d02f738cd8a972a8f7f276b497b79c635c56d477`.
RED JUnit SHA-256: `6219b189dfef9d9bb09d080902121a871769d1cffe98bab37e9a607efd408b12`.
GREEN JUnit SHA-256: `a6ad4128830686a8062dc73845e2e3ae6ca3325d4a274b87209ae92f959cc66c`.
Both files are in `/private/tmp/malleus-reentry-integration.waW6z7`.

Next: author a separately identified program variant against the compiled
supplier contract, freeze the pure synthesis inputs/results, and implement
the controlled source attempt and independent observation before full E2E.
No state effect is inferred from the completion of any earlier step.

Pre-action checks: no server or endpoint, no new installation/dependency,
no replacement of a production mechanism, no production incident, and no Core
file edit. Required inputs have no inferred defaults. Tests precede each new
implementation boundary; defects retain a class guard and hard regression.

## Selected program variant contract

The local builder consumes the exact compiled supplier record contract plus
explicit source-role and policy-role IDs. It reuses Core's program authoring
functions and returns canonical bytes of the existing finite protocol bundle.
Only action type references, the fixed action literal and the action's added
field shapes change. Field shapes are read from the compiled contract. A new
bundle identity is computed after authoring and before any retention. No
previously retained bundle is rewritten, and no interpreter is copied.

The first variant preserves Core's two-static-input/two-monitor arity and all
its stage, control, refusal and no-repeat semantics. Repeated TYPE or authority
producer invocations are not independent implementations or stronger truth
evidence. Explicit IDs remain caller data even if an ID happens to spell
LocalAction or LOCAL_ACTION. Unsupported contract or role input refuses; absent
inputs do not acquire neutral fixture defaults. The builder performs no history
creation, check invocation, authorization, source write or observation.
