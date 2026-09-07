# Semantic Re-entry: observed Shop correction

Status: design and executable prerequisite audit. Producer implementation is
blocked on a Core-owned pure composition boundary. No Semantic Re-entry
implementation, new public Core object or stable wire format is claimed.

## Bound slice

Core baseline: `7c5fdb491721122b6e0c7243862935acc8303a1f`, tree
`155ac29b6fd87709f4d765c00d6c340411f9441c`. The user authorized resuming
implementation on 2026-09-06. Core agreed to this first internal correction
case. Only this directory belongs to the Re-entry task.

The claim is narrow: a pure, pinned Re-entry Synthesizer can translate an
explicit source-backed correction request into the existing KnowledgeChangeSet,
without changing accepted knowledge. Ordinary Core admission and JSONL-only
replay then realize the correction. Repeating the request at the new head
produces no candidate. Replaying the original contract against a newer head
refuses; quiescence requires a freshly bound contract, not silent rebasing.

The smallest observation is accepted B/Y/1 at e4, a pending e7 correction,
unchanged ledger and KG during synthesis, an admitted B/Y/2 at e7 after replay,
and an empty result at that new head. O1, X1 and contains:O1:X1 are the
independently checked complement. All initial facts enter through Core, from
empty history. No hand-built accepted graph is used.

Classification:

| Deliverable | Role | Lowest selected profile |
| :--- | :--- | :--- |
| Pure producer and local contract | REFERENCE_IMPLEMENTATION | Compiler-enabled semantic history plus state-version |
| Shop adapter and tests | CONFORMANCE_FIXTURE | Same |
| Explicit e7 replacement, ORDER_ONLY time and exact-request stopping | ADOPTER_CHOICE | Same |
| Proposal-only authority boundary | PROTOCOL_INVARIANT | Semantic-history capability claimed here |

Without semantic history this experiment claims no accepted-state authority,
admission or replay. Without this local Re-entry contract it claims no
automatic correction, preservation policy, proposal selection or stopping.

## Stage contract, before implementation

The input is a source-backed writable `ViewDelta`, not a supply-gap
`GoalPredicate`. It binds old accepted state, the requested replacement view,
and an explicit complement. The request is a retained neutral population plan;
that plan is not a second change identity.

The immutable, addressable local Re-entry Contract must bind:

1. Exact ledger head/count, acceptance/materialization heads, graph digest,
   effective contract and replay receipt.
2. Exact canonical plan and history profile, retained source and mapping
   evidence, and the initiating discrepancy in the accepted projection.
3. Existing KCS output only; permitted operations, replacement footprint and
   preservation of every other record.
4. Exact synthesizer implementation identity. No unbound callback or ambient
   source, filesystem, network, clock or ledger handle enters the pure stage.
5. An explicit ambiguity strategy, finite candidate budget and one invocation.
   No implicit ranking, retries, rebasing or fixed-point loop.
6. Typed refusal for stale base, malformed contract, unsupported input/operator,
   evidence mismatch, undeclared ambiguity, preservation failure or exhausted
   budget. Refusal produces no candidate and no effects.
7. Stop with zero candidates when the exact replacement view and supersession
   are already realized. Equal quantity alone is not enough.

For an unsatisfied request, required caller-owned source/plan retention precedes
final contract binding. It may append protocol evidence but cannot change the
domain graph. Already-retained request artifacts are reused. A satisfied
request returns without new retention or admission events; the caller must not
prepare a duplicate plan merely to discover that it is a no-op. Synthesis is pure;
admission is a separate caller-owned Core operation. Every candidate keeps
Core's sole KCS identity. The synthesizer cannot authorize or dispatch an
external action.

Dependency graph:

```text
Shop adapter implements source-backed request construction
Shop adapter consumes retained source + explicit correction mapping
Shop adapter produces PopulationPlan
Re-entry Synthesizer implements constrained ViewDelta translation
Re-entry Synthesizer consumes Re-entry Contract + immutable accepted base
Re-entry Synthesizer produces KnowledgeChangeSet or no candidate/refusal
Re-entry Synthesizer governedBy local correction contract
KnowledgeChangeSet derivedFrom accepted base + retained plan/source/mapping
Core admission consumes KnowledgeChangeSet
Core replay produces accepted KG
Reference implementation conformsTo this directory's tests
```

Replacement means a deliberately different producer passes the same boundary
suite with no downstream change. One implementation alone will not be called
replaceable. Adversarial callbacks are negative tests, not replacement proof.

The proposed first contract supports one explicit replacement request, only
`CREATE_ENTITY` with its declared record supersession, a candidate budget of
one, and `REFUSE_IF_NOT_UNIQUE`. These are proposed local policy values, not
Core vocabulary or accepted defaults. Alternative operations, strategies and
budgets require a new explicit contract, not an implicit engine choice.

## Exact Shop mapping

Canonical inputs remain Core-owned under
`research/ontology_driven_kg_realization/`:

| Input | SHA-256 |
| :--- | :--- |
| `fixtures/small_shop_fulfilment_correction_v1/input/sources/supplier-order-history.jsonl` | `a441c49f325670e09d9fc09fd8e6510669258bed1d5532cfb2b1104c4eceb081` |
| `experiments/small_shop/correction/mapping.json` | `77bcc53ef39b301a940ee051c1afd6d3e08e90ba6e8bd344a7ba14ff6f101795` |
| `fixtures/small_shop_fulfilment_correction_v1/input/tbox/small-shop-correction.yaml` | `54e4e170d704056008296c91d1398b024d3a3c3897aba2640599375bf6f42b62` |

e4 and e7 are already present in the same retained source file. e7 is newly
processed evidence, not a newly executed effect. The mapping explicitly maps
e4 to `supplier-order-state:B:e4`, quantity 1, and e7 to
`supplier-order-state:B:e7`, quantity 2. Its e7 operation explicitly supersedes
e4. ORDER_ONLY e4/e7 is selected by that mapping, not inferred from line order.

The existing public population templates supply record and lineage structure.
Only the effective-contract and history-profile coordinates are rebound to
this experiment's compiled correction ontology and Core structural admission
bundle. Template bytes and instantiated plan bytes have separate identities.
The public plan's KCS IDs differ from the older correction runner's IDs;
supersession is resolved through the actual accepted record history by Core.
Record IDs, source occurrences, properties and replacement meaning stay fixed.

## Laws and exclusions

Canonical contract/KCS round-trip is serialization, not semantic re-entry.
Log replay is interpretation, not decoding a graph back into its history.
The future producer must pass no-op, forward agreement after admission,
complement preservation, deterministic result/refusal, stale-base refusal and
quiescence tests. The current audit establishes only the Core prerequisites
and limitations described below.
It must not claim an external ActionProposal changes the world.

Excluded: new Core APIs authored here, ontology/fixture edits, generic mapping
DSL, demand facts, supply-gap/action vocabulary, authorization, executor,
observer, source authenticity, source truth, epistemic assent, domain adequacy,
contract revision, production wire stability, arbitrary goal search, paid or
external calls, paper work and shared-main integration.

Core's structural admission checks conformance. The fixture adapter must
separately compare selected source values with the explicit mapping and plan.
Neither check proves that supplier order B is true in the external world.

## Reserved Re-entry tests

These are obligations for the future producer, not current passing results.

| Boundary | Required guard and hard negative |
| :--- | :--- |
| Source agreement | Compare every selected `state_bindings` value with retained bytes. Valid locator plus quantity 999, wrong product, wrong order or wrong occurrence must refuse. |
| Immutable input | No writer or mutable replay graph enters synthesis. Nested mutation attempts cannot affect a bound snapshot, ledger or fresh replay. |
| Stale state | Any head/count/contract/state mismatch refuses, including an evidence-only append. Check staleness before the satisfied-goal shortcut. |
| Exact operation set | Extra valid entity creation, changed record type, unsupported operation, wrong predecessor or altered valid time must refuse. |
| Complement | Every unmentioned record, property and relation endpoint is unchanged after accepted application. Count equality is insufficient. |
| Ambiguity and budget | Multiple admissible candidates without the declared strategy refuse. Exhaustion is typed; ordering cannot silently choose one. |
| Canonical identity | Missing/unknown fields, noncanonical bytes and substituted synthesizer identity refuse; valid contract and KCS bytes round-trip exactly. |
| No-op and quiescence | Exact e7 content and supersession already realized gives no candidate and no retention. Equal quantity with wrong provenance, or e7 superseded later, is not success. |
| External-world boundary | Action dispatch, attempt, failure or execution receipt is not observed source state. This fixture has no action path; an external-action test remains excluded until Core supplies that domain seam. |

Replay graphs are disposable mutable projections in the current API. Core
does not refuse all local projection mutations. The current test mutates one,
then proves the ledger and a fresh replay are unchanged. A future pure
synthesizer needs a stricter input boundary than that mutable object.

The non-invertibility witness remains reserved: two distinct accepted histories
can yield the same current KG. This audit does not fabricate a second genesis
or reinterpret the selected correction mapping to claim that witness passed.

## Current executable evidence

`test_prerequisites.py` exercises existing public Core boundaries only. It
contains no Re-entry producer and no substitute composition API. Its strict
expected failure registers the missing requirement. Running with
`--runxfail -k pure_stage` produces the explicit RED result. The other tests
measure existing Core behavior, including the absence of source-value checking
and semantic no-op. They are not passing Re-entry guardrails.

The ledger-only reopen test copies just JSONL to a new directory and compares
receipt, query, complement and source trace. Installed runtime code is still
required. This is not a no-filesystem sandbox claim.

## Open Core dependency

At the frozen baseline, pure population compilation produces operations but
KCS composition is a method of the writable history object. Re-entry will not
copy private KCS wire grammar or receive that writer. Core has been asked for
the smallest snapshot-only composition seam. Tests may be prepared, but the
source-to-KCS claim cannot be marked GREEN until that exact seam is available.
Core acknowledged the reproducer and kept this request separate from its
already approved Shop evidence cleanup. No generic seam has been authorized
or promised. Resume requires an approved exact Core commit, not moving main.
