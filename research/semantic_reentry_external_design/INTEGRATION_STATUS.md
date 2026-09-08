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

Next: freeze the pure synthesis inputs/results, then implement the controlled
source attempt and independent observation before full E2E. The supplier
program definition is now authored and checked as described below.
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

The program definition passed 11 focused tests, with no failure, error or skip.
These establish executable bundle validation, exact compiled field projection,
determinism, caller-ID preservation and refusal of missing roles. They do not
establish that a supplier lifecycle event has been admitted or executed.

SP-1, fixed: the first field projection looked for source-language LinkML range
identities after compilation. The actual compiler emits neutral contract-facts
String and Integer identities. The closed range guard now consumes those exact
neutral identities, with no fallback. A dedicated regression checks all seven
compiled payload fields before asserting their schema projection. Its RED
failed at the wrong range boundary; all 11 program tests then passed.

The JUnit files are under `/private/tmp/malleus-reentry-integration.waW6z7`:

- `supplier-program-red.xml`, absent module, six failures and four errors:
  `e79971a8cb424ecdc02422ed2f30bf2cc339627b4641095af32e09c31b98d8c0`.
- `supplier-program-first.xml`, wrong range IDs, one failure, five passes and
  four errors: `9b3e8334e413b2658cb12555053039c6fd46734e588d84231f8de15bc374968e`.
- `supplier-program-neutral-range-red.xml`, dedicated failing regression:
  `ff3fcf8080209f457f53b0f81b8a066358fc10e014c4584ee1ababf45aa3c511`.
- `supplier-program-green.xml`, 11 passes:
  `988797f3b19e5cf41536f3f759caf4c3b92bc377ee36f335bddc0595ddc4b4cc`.

The subsequent combined action-schema/program run passed 34 tests, with no
failure, error or skip. It also verifies that the explicitly named shared
pytest fixture is discovered in both modules after correcting imported-name
shadowing flagged by Ruff F811. Ruff check, formatting and diff checks pass.
Combined JUnit SHA-256 (`supplier-contract-program-green.xml`):
`683546388f880b0e4d2afa51299bf94b2748af9aaed41f142af9ed40fcbd1fff`.
This is the relevant gate for these two definition modules, not the future
unified supplier E2E gate or full repository CI. The earlier 11-test result is
not added to it. Implementation GREEN:
`2eaa1208555975e6615bc6db1b48f2c5dac4a1ba`, tree
`4d02171c21b9af9b5c3f9ad928c6bf7a0500e823`.
Exact GREEN file SHA-256 values:

- `supplier_program.py`:
  `5ba6751ac425929dc74c84742adbff54b082a0a38d2f87768537cbdb0ef3f15f`.
- `test_supplier_program.py`:
  `3281682d26be683cd09ae671f2240a359c0f7cfc6f3a44d447f2f6cc2baf09a6`.
- `test_supplier_action_contract.py`:
  `9ac86d5d0c35be6be70928829b833cbef0598f26300a0bce36f646ec71a46b61`.

## Proof alignment check

On 2026-09-08 UTC the Core handoff, both semantic contracts, frozen source
case, pure-component report and replay non-invertibility witness were reread.
The active five-minute heartbeat continues authorized integration. It is not
waiting for another Core release or Robotics' separate repeated-action work.

The claim remains an exact-two GoalPredicate, not a writable SupplyGap view,
demand fulfilment or delivery. Re-entry is synthesis from pinned accepted state
and an explicit preservation policy, not inverse replay or source decoding.
Internal epistemic changes may propose an existing KCS; this external goal
must propose an existing ActionProposal subtype first. Symbolic model agreement
does not prove a world change. The old e7 correction and the expected-output
oracle must never be used as this experiment's captured source.

The full proof is unfinished. Synthesis and its immutable input closure, actual
check producers and lifecycle submission, controlled execution, independent
capture, observed-source KCS admission, JSONL-only replay and fresh episode
closure must still run together. Every pre-admission checkpoint must retain
B/Y/1. Only the admitted observed correction may make B/Y/2 current, and the
final linked, satisfied evaluation must produce no candidate, append or effect.
