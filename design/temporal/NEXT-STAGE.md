# Next stage: a version-aware temporal KG

2026-09-24. Design packet ready for author review. Implementation remains paused.
This prepares T3 through T5; it does not approve a representation, policy or wire.
Latest author direction: GEDANKENEXPERIMENTS-01.md adds cross-flow research gates
before selecting this path. The earlier recommendation remains on hold while
storage mappings and shared semantic obligations are challenged.
Forward note, 2026-09-24: the author requested evidence before the A/B choice.
[REPRESENTATION-OPTIONS-01.md](REPRESENTATION-OPTIONS-01.md) supersedes that
binary framing with a researched separation of assertion identity, temporal
query semantics and physical storage. Its recommendation remains unapproved.
It follows [BITEMPORAL-RESEARCH-01.md](BITEMPORAL-RESEARCH-01.md) and supersedes
the implementation sequence in CONTRACT-02-DRAFT.md where they differ.

## The result we want

One accepted history retains every version as queryable graph content. A caller
can ask what applied at a domain time, according to an exact knowledge position
and declared context, without losing prior accounts or their evidence. An old
calculation remains connected to the precise premises it used.

The earliest falsifier is simple: correcting the account of 5 May either erases
the earlier account, changes the price for 15 May, or changes an earlier
calculation's inputs. Any of those means the temporal design failed.

This is an `OPTIONAL_PROFILE` over compiler-enabled semantic history. Python
work would be a `REFERENCE_IMPLEMENTATION`; the authored controls below are
`CONFORMANCE_FIXTURE` candidates. Domain subject types, price authority,
scientific interpretation and hypothesis selection remain `ADOPTER_CHOICE`.
Without this profile, no new bitemporal guarantee is claimed and existing
histories keep their explicit interpretation. No base-protocol change is proposed.

## Three controls, with expected answers written before runtime changes

[expected-views-v1.json](expected-views-v1.json) is a draft answer key, not a
population grammar, a public API or a generated execution result. Its labels
will bind to actual ledger checkpoints and record identities in the tests.
Its date-time values are authored UTC instants, not dates inferred from prose.

| Control | Input | Required observation |
|---|---|---|
| Price history | Original report, actual transition, then correction of the ended period | All versions accessible; old knowledge gives 750, corrected knowledge gives 775 for the same earlier date; later period stays 800 |
| Scientific account | Correct a synthetic pipe-diameter report with no stated measurement/applicability time | Both versions accessible; source correction changes the account but supplies no domain date |
| Calculation context | An execution used the original price; a separate hypothetical execution used 800 | Old exact inputs remain explainable; changed reported premises are detected; the hypothetical result cannot stand in for an unperformed reported calculation |

The third is a consumer contract over the first, not a new formula engine. The
scientific control is a different record shape, not a claim of marine extraction.
Neither proves replaceability; that needs a deliberately different interpreter.

## What the full graph and selected views must expose

For the price control, define knowledge positions K0 through K3. K0 is completed
empty genesis. K1 accepts report r1, 750 from 1 May. K2 accepts transition r2,
800 from 12 May. K3 accepts correction r3, 775 for 1 May to 12 May.

The graph must distinguish the stable product, exact source assertions and their
versioned applicability. r1 is one report, not two independent measurements
because its end becomes known later. The answer key calls its applicability
versions a1 and a2; those are logical labels, not prescribed storage nodes.

| Full history at K3 | Value in cents | Valid period | Selected knowledge period |
|---|---|---|---|
| a1, account based on r1 | 750 | [1 May, open) | [K1, K2) |
| a2, account based on r1 after r2 fixes its end | 750 | [1 May, 12 May) | [K2, K3) |
| b, account based on r2 | 800 | [12 May, open) | [K2, open) |
| c, corrected account based on r3 | 775 | [1 May, 12 May) | [K3, open) |

All remain graph-queryable at K3. A selected view for 5 May at K3 uses c, while
an explanation of an execution under K1 still reaches r1 and a1. The full graph
has not asserted that all four values apply simultaneously.

**Historical reads must not leak later metadata.** At K1, a1 has no known end
on either axis. At K2, a2 has no known knowledge-period end. Simply filtering
the final table would expose K3's later correction unless that information is
also bounded. Fold the selected prefix, or prove an equivalent reconstruction.
Preserving values but leaking their future closure is still a failed old read.

An exact-assertion reference must not be silently redirected by a correction.
A stable-subject reference is different: it may resolve through the declared
selection. A provenance relation can join different periods; a same-time
calculation cannot accidentally join disjoint ones. Relation semantics must
declare which meaning applies rather than impose overlap on every edge.

## Query obligations

Names in this section describe design roles, not proposed Python identifiers.

1. **History inspection:** return qualified versions and links available at the
   selected knowledge position. It is not a bag of currently applicable facts.
2. **Domain-time selection:** require the knowledge checkpoint, domain-time
   request, property/subject scope and account/context selection. No ambient
   "now", "latest" or preferred source can silently fill a required input.
3. **Exact-version lookup:** return the identified assertion and its evidence
   under a declared audit context, even when it is no longer selected.
4. **Premise comparison:** compare a consumer's bound selection with a newly
   requested selection. Report differences, not a recomputed result.

Results must distinguish no accepted account, an applicable account, unresolved
applicability and an ambiguous choice. The draft answer-key labels are not new
Core refusal enums. Unstated time is not forever, falsehood or ingestion time.
An unknown-time assertion can still be inspected without being selected as a
fact applicable on an arbitrary date.

With several accounts, retain their qualified assertions. Do not choose the last
arrival as authority. An unqualified request needing one premise must ask for
the missing context or report ambiguity. Selection and acceptance are separate.

## How the stages compose

These are responsibilities in the existing pipeline, not a mandate for five
new services or files.

| Stage role | Inputs and outputs | Effect and check |
|---|---|---|
| Temporal proposal compilation | Retained evidence, contract, base checkpoint, declared correction/transition, targets and applicability -> immutable candidate change | Pure; refuse malformed, stale or unsupported meaning |
| Admission | Candidate, selected policy/check contracts, relevant staged history/views -> accepted change plus Core-produced check evidence, or refusal | Existing owning gate; caller supplies no outcome; no partial accepted state |
| Replay | Verified prefix, retained contracts and temporal interpretation -> full version-aware graph | Derived only; no independent accepted write path |
| Selection | Full temporal state, explicit coordinates/context -> qualified view and unresolved cases | Pure; bind inputs, selector semantics and output identity |
| Consumer comparison | Prior execution's exact premises plus new selection -> unchanged/changed/unresolved comparison | Pure; no arithmetic execution or external effect implied |

A stage's exact schema, version, diagnostics, identities and executable fixtures
must be completed before its RED tests, not inferred from this prose. Required
unsupported semantics refuse. No fallback interpreter for a new grammar.
Schema evolution during these controls is excluded: retain a fixed identified
ontology and policy so we can isolate temporal semantics. This does not select
the policy for a later cross-ontology correction.

## Checks must say what they inspect

Retaining all versions does not mean feeding their unqualified union to every
existing Prolog rule. Nor does it justify silently dropping a required rule.

| Obligation | Input scope | Discriminating control |
|---|---|---|
| Record shape and reference integrity | Versioned representation and its governing ontology | Missing exact referenced version refuses |
| Temporal operation integrity | Prior history plus proposed change | Stale correction target or unexplained overlapping replacement refuses |
| A domain rule about one applicable state | Explicitly selected affected domain views under one context | Disjoint old/new prices do not conflict; a forbidden simultaneous selection does |
| A rule comparing successive accounts | Qualified history and named relation semantics | May inspect different periods without pretending they are simultaneous |
| Computation input eligibility | Exact premise identities and compatible selection context | Disjoint applicability or unresolved required time cannot produce a ready input set |

For the proposed exact-interval control, a candidate checking strategy is to
partition affected time by all relevant endpoints and inspect every constant
state region, including the open tail when affected. Checking only "today" or
only one supplied date is insufficient. This strategy is **proposed**, not a
general theorem for arbitrary Prolog: a rule may itself depend on time or
history, and then must declare a different check scope. Unknown-time membership
must not yield a fabricated SATISFIED outcome.

Before selecting a domain rule, follow the skill's census requirement on both
control populations and classify every refusal. This packet chooses no new rule
body. A required check with no supported scope must refuse explicitly, not be
replaced by a structural check. Byte preservation on preflight/check refusal,
the exact retention boundary, and accepted-state atomicity need separate tests.

## Representation decision before implementation

Historical proposal, not selected. Read REPRESENTATION-OPTIONS-01.md before
acting on the A/B recommendation below; the author found this choice insufficiently
explained and requested research rather than approving implementation.

Both candidates owe the same answers and provenance; neither changes the sole
ledger authority.

| Candidate | Representation | Main tradeoff |
|---|---|---|
| A, explicit versions | Version/assertion objects reachable from a stable subject, with qualified applicability and evidence links | Fits addressable premises; needs profile-owned representation and selection semantics, not an adopter workaround |
| B, native temporal properties | Multiple qualified property/edge values on stable graph elements | Compact property access; expands graph storage, query and fact-compilation contracts; exact premise versions still need addresses |

Recommendation for the first Core control: **A**, keeping storage replaceable.
The four applicability labels do not require four copies of every payload.
Core-owned temporal metadata must not silently add domain ontology classes or
force all adopters into this profile. The compiler/graph contract must declare
where those records live and how ordinary queries distinguish them.

This is the one immediate author decision. After it, we can draft the precise
profile and rule-input contract. Any further change to policy meaning is a
separate decision, not implied by choosing nodes over temporal properties.

## Atomic milestones and evidence

| Order | Deliverable | Completion criterion |
|---|---|---|
| P0 | This review packet and authored expectations | Choices visible; no runtime claim. Prepared, pending author decision |
| P1 | Exact temporal representation, selection and check-input contract | Each control mapped to accepted writes, version graph, query results and refusal; author approves remaining semantics |
| P2 | Failing Core conformance tests | Independent answer key; failures identify the missing capability, not harness setup; no expected answer generated by Core |
| P3 | Smallest Core implementation through the existing admission/replay path | Both price and scientific controls pass; real checks run; no consumer-supplied verdict; no independent writer |
| P4 | Consumer and replay verification | Old calculation references stable, changed premises detected, hypothetical result not reused; reopen/full/incremental/rebuild agree |
| P5 | Integration review | Relevant old suites, package and installed public path checked; coordinates and governance reconciled before any shared integration |

P0 -> representation decision -> P1 -> semantic approval -> P2 -> P3 -> P4 -> P5.
Preparation is not completion of T3. All runtime milestones remain pending.
No commit, push, shared-tree mutation or external model execution is implied.

## Test inventory for P2, not results

The wider thought-experiment pass also found under-specified persistence in the
old valve examples and a required date-free quote use. These must be resolved
in the new specimen contract, not silently copied into temporal Core guarantees.

- Match every authored query and each old prefix's available metadata.
- Refuse stale targets, missing sources, altered identities, unsupported profile
  versions and ambiguous required selection before partial accepted effects.
- Keep both temporal boundary equalities correct: start included, end excluded.
- Preserve exact links to old assertions, even when their applicability changes.
- Distinguish unknown time from absence and from an unbounded known period.
- Keep equal numerical values in different premise contexts distinct.
- Observe actual rule inputs and outcomes, not a supplied SATISFIED stub.
- Detect byte tampering and missing replay closure; no writes during queries.
- Compare full replay, maintained replay and rebuild against the same expected
  graph, not only against each other.

Late reports, future-effective transitions and uncertain boundary windows remain
in situations.json for T4. Interval splitting, retraction, multiple-authority
resolution, temporal ontology/policy changes, UMR mapping and automatic
recomputation remain explicit later work, not guarantees of this first control.
