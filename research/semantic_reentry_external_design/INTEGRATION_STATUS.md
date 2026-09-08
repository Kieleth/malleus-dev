# Supplier Re-entry integration

Status: ACTIVE IMPLEMENTATION, not an executed supplier E2E.
Latest verified boundary: actual independent capture, followed by a retained-prefix
probe through ordinary observed-source KCS preparation, admission and JSONL replay.
The probe reaches accepted B/Y/2 only after admission, including failed-after-write
without rewriting the failed receipt. It is not a fresh complete supplier E2E.
Separate completed runs: action entry 141 passes, authorization 99, corrected focused
execution 22, first focused observation 11. Expanded observation and the fresh 98-test
observed-population gate are running. Full pure synthesis, immutable Re-entry Contract
closure and fresh satisfied episode quiescence remain unfinished. No Core wait.
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

## Accepted read input, GREEN

`freeze_accepted_replay` now consumes actual public Core replay/context values
outside the synthesizer and returns immutable, graph-free inputs. It compares
all seven context coordinates, validates the receipt and protocol identity
chain, reconstructs a disposable graph for complete digest comparison, and
checks exact retained bytes/metadata. The returned value keeps no graph,
writer, replay object, path or callback. It is not a new public context or
checkpoint and does not authenticate arbitrary forged Python objects.

The first 20 tests passed after a 20-error absent-module RED. Three additional
tests cover no file/process/network I/O, Boolean count refusal and no imports
from private Core or research helpers. The combined read/schema/program gate
passed 57 tests with zero failures, errors or skips. Counts overlap with prior
runs and are not added. This is not full repository CI or the supplier E2E.
Exact implementation, test selections and hashes are in
[accepted-read-result.json](accepted-read-result.json). Implementation GREEN:
`9b8128cca2f11672e3487b53c614c23b88160479`, tree
`014267899c20e75b2029787b218b6883559e6729`.

The read test uses the real historical Shop only to exercise read consistency.
It includes historical e7 and must not become the new effect experiment's
initial state. Source agreement, initial e4-only population, goal-contract
binding, synthesis and acted-on episode closure remain separate work.

The initial-source cut below now establishes the one-row supplier source and
RET-010 complement through ordinary public source/population/KCS admission.
Next, register the actual supplier program and prerequisites before taking its original
context. Freeze the static goal/rule input before binding that context, so a
later retention does not silently stale the proposed base. Use the existing
Core original-context artifact as the immutable contract root, with its
already-defined references to retained goal, preservation, mapping, pre-state
source, initialization and policies. Exact implementation identities belong
in that retained input closure; no placeholder or extra Core object is needed.
Tests must establish that binding before candidate synthesis is claimed.

Core's separately proposed one-active-action extension and Robotics' repeated
action requirement do not gate this single-episode implementation. The current
dependency stays pinned to the verified base above.

## Initial source ingress, verified; broad gate has one baseline failure

The synthetic e4-only source now produces an ordinary KCS candidate with its
full source ID/digest pair. Preparation retains evidence but leaves only the
RET-010 complement accepted. Separate public admission creates B/Y/1 at
`supplier-order-state:B:e4`. JSONL-only reopen reproduces the complete graph,
record history and exact one-row source trace. The test forbids reads of the
historical supplier-order-history file or amendment oracle and confirms that
no e7 source occurrence or accepted e7 state enters this prefix.

The initial and observed-replacement mappers share the existing closed parser
and field projection. Initial mapping does not evaluate the goal or rewrite
quantities. The old model and replacement tests still pass. Each implementation
has a new exact code identity after the shared helper change; older result
files continue to identify their historical implementation, not this one.

SI-1, fixed: preparation initially invoked `append_anchors` before validating
the owning history object. A substitute-writer regression reproduced that call.
An entry-point type guard now refuses before any such call. This closes that
reference coordinator's callback boundary, not arbitrary Python execution.
Required source, mapping, profile and metadata checks also refuse before
retention. The earlier wrong `source_record_ids` test assertion was corrected
to the actual KCS `sources` ID/digest pairs and canonical round-trip; no Core
alias or runtime workaround was introduced.

The final initial-source module has 34 passes in the broader run. That run has
512 passes and one failure, so it is NOT fully green. The failure is the
unchanged document-trace test's expected `base_ledger_head`; it reproduces
identically in the clean pinned Core checkout, with 13 other KCS fields
matching. Core has the exact reproduction and owns its diagnosis/correction.
Re-entry has neither edited nor waived that fixture. This does not block
continued supplier implementation or reopen the passed one-action gate.
Do not rerun this unchanged baseline repeatedly or silently exclude it.

Exact selections, RED/GREEN, baseline reproduction and file hashes are in
[supplier-initial-result.json](supplier-initial-result.json). Implementation:
`9e04851827a48c162fd3b76c0ee052f60db9afe3`, tree
`ad737520b70a81f6e4e3eb88ef4dd3ca699086a2`. All code remains confined to this
Re-entry directory. No Core, ontology, canonical fixture or paper file changed.

Next is actual supplier-profile initialization and retained goal-contract
binding, then pure candidate synthesis. The source-to-initial-KG leg is now
proved; proposal, execution, observation-derived correction and final episode
quiescence are still unfinished.

Core subsequently confirmed this exact failure is already recorded in
`research/action_history_contract_freeze/GATE.md`. The compiler repair changed
its recorded implementation identity and therefore the retained-history hash;
the frozen example identifies the older history. Core's proposed narrow fix is
a separately versioned current-compiler example and current test binding,
preserving the original and its historical reproduction check. That fixture
change requires operator approval. No assertion is skipped or hash field
ignored, and no runtime/fixture correction has been adopted here.

## Supplier initialization, verified

The initializer contract and 23 initial tests were frozen at `b97e99d`. The RED
run had 23 missing-module failures. The first implementation run had 21 passes
and two failures, both refusing the supposedly identical supplier program before
any retention. No initialized supplier lifecycle or full E2E is claimed yet.

SP-2, reproduced: supplier program authoring inherited dictionary traversal order
when Core's builders generated ordered schema arrays. Reusing the named role maps
after canonical JSON serialization therefore produced different program bytes.
The earlier determinism test used the same map insertion order and missed this
class. The dedicated serialization regression failed before the repair. The
initializer and regression RED are retained at `ce0e00c`.

The supplier builder now chooses canonical role order before lowering either map.
This authors a new program identity; it never renames an already retained program.
The initializer still compares the complete generated program bytes before
retention. Cheap static checks now precede that expensive validation. The targeted
run passed the serialization regression and actual supplier initialization, two
tests with 34 deselected. Implementation: `23b67ba5b6a402331c42869cb1e889f33869123b`,
tree `8fa5ba926d063a38e36a52d09ab4323b400a7722`. The nine-file gate subsequently
passed all 173 tests with zero failures, errors or skips. Counts overlap with the
focused and earlier runs and are not added. This is not the full supplier E2E.

The verified initialization appends 14 protocol records and preserves all domain
coordinates and accepted history at each step. Its 39-event JSONL file independently
reopens in a fresh process with only B/Y/1 and the O1/X1/relation complement accepted.
The selected supplier bundle has the new identity
`sha256:86c44748ab4ce43c864b8130bfa01b27630aece3a90406f3ada6bf6039af9eb3`.
No assessments, proposal, grant, authorization, dispatch, execution, observation or
supplier correction are inferred from registration. Exact evidence is in
`supplier-initialization-result.json`. The targeted and unified runs independently
produced byte-identical 39-event histories with SHA-256
`1df1c990e54bab9300414c3f8caa8db02c158d5fb9ae0a27a538351216b42d29`.

The initialization-specific gate is `supplier-initialization-gate.json`. It covers
the new coordinator and the existing supplier source/schema/program/read and Core
registration/initialization/check/finite-history boundaries. It does not replace
or waive the broader population gate's known historical-example failure.

The scoped self-review is `SUPPLIER_INITIALIZATION_REVIEW.md`. No new Core blocker
was found. Next is the retained goal/implementation/source closure, existing
original-context binding and pure synthesizer, then the real authorized supplier
attempt, independent capture and observation-linked KCS/episode closure. Core's
unchanged sequential-action proposal and Robotics' separate work do not gate this
one-episode implementation. The recurring loop remains active.

## Supplier action entry, verified

The actual supplier path now constructs Core's immutable original context from
the graph-free accepted read, admits an explicitly authored SupplierOrderAmendment
and its existing proposal atomically, runs actual TYPE producers and records the
public epistemic policy result. ACCEPT advances the action head, never the domain
head or KG. Real checker unavailability records failure/UNKNOWN and causes DEFER.
The authored action is not a fake synthesizer and is not attributed to one.

The eight-file selection passed 141 tests with no failure, error or skip, including
all 32 supplier proposal tests. Two independently built positive runs produced the
same 48-event JSONL bytes. Independent fresh-process reopen recovered 25 protocol
records, an ACCEPTED proposal, PENDING authorization, two accepted KCSs and B/Y/1.
O1, X1, their relation, all domain heads and record history remain unchanged. No
dispatch, execution, observation, correction or satisfied episode is inferred.

SP-3 was an adopter exception-surface defect. Deferred lookup of an unexported
Core exception name masked actual refusals. The public machine exception is a
different type and was not substituted. Local parsing failures are now translated
at their own boundary; native upstream typed ValueErrors propagate unchanged.
A failed class regression and structural handler guard precede the repair. Actual
late atomic refusals and prefix movement before/after check computation also pass.
No Core error contract or runtime was changed.

The implementation is `940ff15d4bc1ba2e0b8a6f380f0bdacc4b6bad77`, tree
`d85714e15e3f8912c8666bb2d1a1cadbc144b9ca`. Exact selections, counts, hashes and
limitations are in `supplier-proposal-result.json` and `SUPPLIER_PROPOSAL_REVIEW.md`.
The prior broader population gate's known failure remains recorded, not waived.

The next independent cut freezes real supplier direct-grant AUTHORIZE/BLOCK/CLARIFY
tests in `SUPPLIER_AUTHORIZATION.md` and `test_supplier_authorization.py`, RED
`430dc3379b5f6d772cf7468b4b3bece282f93d2e`. First implementation:
`1ec94392ba2b8084761302c8949444b21c7e8f6f`. The first focused run passed its API
check but failed in test setup before invoking authority preparation: deepcopy
cannot copy immutable mappings inside Core KCS values. The test snapshot now uses
public canonical bytes and frozen history entries, with dedicated representation
and no-deepcopy guards. No permission result is claimed before the rerun.
The 141-test gate does not cover those new authorization files. Dispatch and
identified executor/observer, full synthesis closure, observed correction and
fresh quiescence remain unfinished. No Core or Robotics wait is required.

## Supplier authorization, focused GREEN

The corrected 16-test authorization module passed with no failure, error or skip.
Actual DIRECT_GRANT execution yields AUTHORIZE for the matching grant and BLOCK
for a mismatched grantee. Controlled engine unavailability records the native
failure/UNKNOWN pair and yields CLARIFY. Decision and JSONL-only reopen do not
invoke the producer. Each step preserves the complete accepted domain frame,
including B/Y/1, both accepted KCSs, temporal history and the RET-010 complement.
Permission introduces no dispatch, execution, observation or corrected fact.

This result binds implementation `1ec94392ba2b8084761302c8949444b21c7e8f6f`
and corrected tests `8413a7bd50ed0fba525d022aa877d8df99c6c116`.
Exact selection, earlier RED, file hashes and exclusions are recorded in
`supplier-authority-focused-result.json`. It is a focused result, not the
authorization unified gate, full repository CI or full supplier Re-entry E2E.
The 141-test action-entry count is separate and is not added to this count.

The five-minute heartbeat remains active. The Core/adopter contracts, frozen
supplier case and replay non-invertibility witness were checked against this
implementation status. The exact-two goal, immutable original context, distinct
ledger/domain/action coordinates, one attempt, actual observation requirement
and unchanged complement remain the approved obligations. Core's passed gate
is not reopened by its separate multi-action proposal or the known historical
document-example failure. Next work remains local: complete authorization
boundary coverage and its relevant gate, then identified dispatch/execution,
independent observation, full synthesis input closure, observation-linked KCS
and fresh satisfied/no-output/no-retention/no-effect closure.

## Controlled supplier execution, first focused GREEN

The existing action now crosses real dispatch into one controlled synthetic file
attempt and an existing ActionExecution receipt. All 15 initial execution tests
passed. A successful write changes the file to B/Y/2 at reentry-amendment-1, while
the accepted KG stays B/Y/1. Injected failures before/after write remain FAILED;
success with unchanged source stays distinct from observation. Stale source yields
ABORTED. Static ineligibility and repeated output IDs invoke no further attempt.
All cases preserve the complete domain frame and JSONL-only receipt replay.

The implementation is `f621afd79a1d9c9e402a2e9d35a47e6365a2508d`, tree
`7def7eb853dfc38db6efcb95afe9c0e860834d13`. The initial 15-test file is bound to
`22ada0ebd81c737c52240323de3787d6bd55c147`. Exact results and exclusions are in
`supplier-execution-focused-result.json`. This source effect is not an accepted
correction, independent capture, synthesis result or satisfied goal episode.

Additional tests cover fresh output IDs attempting to retry the same action and
receipt-retention failure after a real write, followed by JSONL-only reopen. The
expanded execution/receipt gate is running at `de1a69c3202023accb92251e014f7fa5bff464c4`.
The expanded six-file authorization gate is separately running at
`20f5a8cb82326e494dc676eed3d7ef092ade94d2`. Do not duplicate these unchanged runs.
No final result is inferred from progress output.

Independent observation has its own contract/API RED at
`63e06e226a74d50b7c7db2de001c636e8ec3afd8` and first implementation at
`b2caa982f161ca57e17f84237aac43af4e955cd6`. Its two fast API/actual-source-identity
checks pass. Actual lifecycle capture, expanded negative coverage and its relevant
gate have not yet run. `SUPPLIER_OBSERVATION.md` also records the ordinary
SOURCE_ARTIFACT-to-RETAINED_SOURCE bridge needed by the later population adapter.
The exact captured bytes and observation linkage must survive that bridge.

## Supplier authorization, unified GREEN

All 99 tests in the six-file authorization selection passed, including 35 supplier
tests. This binds test commit `20f5a8cb82326e494dc676eed3d7ef092ade94d2` and unchanged
implementation `1ec94392ba2b8084761302c8949444b21c7e8f6f`. Expanded stale-computation,
late atomic-refusal, current-context authenticity, monitor and exception-surface
checks required no production repair. No Core ownership expansion was needed.

An independently reopened saved 55-event positive history recovers 33 protocol
records, AUTHORIZE, both accepted KCSs and B/Y/1 with the complete RET-010 complement.
Exact counts, file/commit/tree identities, replay coordinates and exclusions are in
`supplier-authority-result.json`. Counts overlap earlier runs and are not added.

The separate expanded execution/receipt selection completed with 31 passes and one
failure. The fresh-output-ID retry test expected a finite-runtime duplicate refusal
but received a native KnowledgeChangeRefusal. A copied-history probe established
the cause: the retry reused 06:10 after its receipt at 06:20, correctly triggering
MALFORMED_HISTORY for decreasing transaction time. A fresh 06:21 retry reaches the
native DUPLICATE_DISPATCH_BY_ACTION refusal. Both preserve the file and ledger.
The class regression now explicitly checks valid versus backdated retry timestamps,
exact refusal types and no effect in both cases. Production remains unchanged.
Receipt-retention failure and its no-retry test passed. This is not a GREEN execution
gate and does not yet establish a Core blocker.

## Controlled observation and retained-prefix observed correction

The corrected 22-test execution module passed at `043ea37873973fad86d6ea5f71f82240e611072b`.
The earlier failed expanded run remains evidence of a fixture timestamp defect, not
a runtime repair. Both backdated and otherwise-valid retry cases now test the exact
intended guard, including unchanged ledger/source and no second attempt.

The initial 11-test independent-observer module passed with production
`b2caa982f161ca57e17f84237aac43af4e955cd6`. Actual capture distinguishes changed,
unchanged and malformed bytes, preserves failure after write and leaves accepted
knowledge unchanged. The expanded two-file observation gate runs at
`d3ec9fb22ae4cc1c9bfd3f491c823a5688faf057`, covering 22 supplier observer cases and
the native Core observation neighbors. No expanded GREEN is inferred yet.

The new observed-source coordinator has contract/API RED `e94bedc0e3dfb977d07c5037192aa6e76a6931d6`
and implementation `4d4f29fed69cb7e862ab237acd9e2bf1f0b88bcc`. It consumes applied
observation closure, never a caller's file or receipt payload; retains the exact
SOURCE_ARTIFACT-to-RETAINED_SOURCE bridge and binding evidence; and prepares only the
existing KCS. Four fast API/identity/no-admission checks pass.

A separate consumer probe ran the actual positive test-function assertions on
JSONL histories from the completed observer cases. Both successful and failed writes
reach B/Y/2 only through normal admission, preserve complement/supersession history
and replay to exact observed-source lineage. An unchanged capture emits no candidate
or retention. Those three cases are not a newly built pytest suite or synthesized
action loop. The fresh three-file 98-test population/mapper gate runs at
`3519d83fcf7be1e26195d36991d30bff449b41d2` and is not yet GREEN.

Exact separate counts, RED, commits/trees, implementation/JUnit/retained-history
hashes and limitations are in `supplier-effect-observation-result.json`. The remaining
contract must bind the real synthesizer/model/update policy and acted-episode observed
KCS closure; a receipt, retained-but-unaccepted KCS or unrelated quantity-two fact
cannot close that episode. Fresh reevaluation must preserve the immutable original
proposal context while explicitly binding the new current head, not silently rebase
an old contract. These are existing approved obligations, not new Core prerequisites.
