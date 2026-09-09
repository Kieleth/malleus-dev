# One connected Shop story

Status: execution approved by Luis on 2026-09-08. Shop owns the example only.
Any missing Core contract must be requested from Core and delivered there.
The ontology-led history choice is selected in `connected_story/MODEL.md`.
Connected Table 1 population and a bounded read-only payment explanation are
implemented. The reader preserves the source's stated reason for O2's delay,
shows invoice clearing at accepted import checkpoints and returns unknown for
unprovided account completeness. Per-object domain ordering and a broader
shipment-eligibility claim remain separate. See
[`connected_story/SHIPMENT_EXPLANATION.md`](connected_story/SHIPMENT_EXPLANATION.md).

This task owns the Shop example as a Malleus adopter. It does not own Core,
the paper task, Robotics, or Semantic Re-entry. This is one Shop planning
document, not another Core program, governance ledger, or protocol specification.

## Outcome

Build one inspectable run that answers:

> What happened to the orders, what changed, what recorded conditions blocked
> shipment, and which sources and rules explain the result?

Then demonstrate the Malleus contribution separately:

> Can those representations and checks be bound to explicit contracts, admitted
> atomically, corrected without erasing history, and reconstructed with their
> evidence?

The first question concerns the represented business process. The second
concerns the protocol handling that representation. Passing the second does
not establish that the first is a faithful or complete interpretation.

## Baseline and ownership

The original source/probe baseline was released Core `v0.14.0`:

- Commit: `e2b9e77912f9b36fdbfe2fca310548a789bffb4d`.
- Tree: `162325eb0048816654d2df5b6b0f00270d06385d`.
- Planning checkout observed at `55c038438ed67197b7e3345b9c80a885a7b6cf17`.

The ontology-led connected successor uses the exact later coordinate in
[`connected_story/run_receipt.json`](connected_story/run_receipt.json), including
Core's delivered state-category restriction. Earlier release receipts are not
rebound. The later local Re-entry integration is not part of that release and
is not a dependency of this plan. Runtime version changes require an explicit rebind.
This planning pass inspected documents, source artifacts and tests; it did not
rerun the release or Shop suites.

Shop owns new versioned fixture bytes, domain schema, mappings, selected rules,
consumer queries, tests and the walkthrough. Core owns public runtime contracts,
compiler and interpreter code, packages and its governance. Missing Core behavior
gets a minimal public-API reproducer and an upstream requirement. Shop must not
patch `src/malleus`, import private compiler modules as a workaround, invent a
second change identity, or write the accepted graph directly.

Preserve existing fixtures, source bytes, independent expected results, histories
and receipts. Build a versioned sibling. Each new run has one authoritative
history from empty accepted state. Do not concatenate predecessor JSONL files
or silently convert their selected policies.

## Source and original intent

The source is Dirk Fahland, [Process Mining over Multiple Behavioral Dimensions
with Event Knowledge Graphs](https://link.springer.com/chapter/10.1007/978-3-031-08848-3_9),
2022. Sections 1 and 4 describe the retailer and event representation; section 5
connects related objects to process analysis; section 6 adds warehouse behavior.
Those are inherited techniques, not Malleus inventions.

Our [original selection](../../../../design/GRAPH_REALIZATION_RUNNING_DOMAIN_CHECKPOINT.md)
chose this domain to exercise source mapping, identity, corrections, multi-entity
events and ontology evolution through one maintained example. The
[charter](CHARTER.md) preserves the original obligations. It is historical:
its Event-correlation refusal has a separately implemented successor.

The first connected milestone covers the original retailer lifecycle and shared
dependencies. The additional warehouse-analysis layer is a later milestone,
not silently counted as completed by the first one. Synthetic partial shipments
remain separately labeled extensions, not additional observations from the chapter.

## A. What exists, and what is missing

| Original obligation | Current evidence | Missing from the connected story |
|---|---|---|
| Ontology without invented instances | Compiler and baseline fixtures | Reuse, do not rebuild. |
| Order and physical unit | [Default admission](default_admission/README.md) | Extend coverage beyond the selected order/unit pair. |
| Payment linked to two existing invoices | Same default run | Connect invoice ownership, settlement and the relevant shipment conditions. Payment settlement itself is not missing. |
| Supplier and invoice corrections | Supplier replacement passes; [charter](CHARTER.md) explicitly leaves the invoice half open | Represent the invoice-update occurrence without inventing its unknown changed value. |
| Event with several participating objects | [Object-event fixture](../../fixtures/small_shop_fulfilment_object_event_v1/README.md) | Integrate occurrences with the rest of the chosen history semantics. |
| Per-object event order | Not a shipped Event-to-Event relation capability | Specify and test a read-side ordering rule; request Core support only for a demonstrated missing public capability. |
| Later sources and richer schema | [Fresh import](fresh_import/README.md), [partial shipments](partial_shipments/README.md) | Prove their effect on the connected interpretation, not merely that more rows admit. |
| Checks and replay | [Shipment rule](shipment_policy/README.md), public trace and maintained projection | Exercise them at the same connected checkpoints under one declared policy selection. |

### Deliverable 1: a source-complete boundary for the selected story

**Output:** a versioned Shop source pack and a compact coverage table linking
each selected source row or passage to its records, declared gap, or explicit
exclusion. Include the original conceptual inventory: both orders and suppliers,
the distinct inventory units, actors, invoices, payment and relevant occurrences.
The denominator is the declared source boundary, not an evolving list of queries.

Reuse the existing controlled transcriptions. Add only missing supported inputs.
Label each addition as source transcription, fixture-defined interpretation, or
synthetic test data. Record the chapter/table/figure convention for every locator;
resolve inconsistencies before freezing, never silently renumber events.

**Proof:** an independently reviewed inventory accounts for every selected input;
tests detect omitted rows, unresolved locators and undeclared fields. Keep invoice
amounts and any unstated time components unknown. Preserve physical identity:
distinct units do not become versions of each other.

**Excludes:** source truth, automatic semantic-coverage scoring and invented
observations. Structured-row coverage is not the document adapter's census.

**Dependency:** none beyond the retained sources and proposed baseline.

### Deliverable 2: one explicit Shop model and history contract

**Output:** the Shop ontology plus a short modeling decision defining enduring
objects, immutable domain occurrences, replaceable state records, evidence,
protocol events and read-only derived conclusions as distinct things.

The shipped `state-version` profile has no Event role. The `object-event`
profile has one, but its declarations do not implement an arbitrary state
projection program. The two existing demonstrations therefore cannot be joined
by relabeling their profiles.

**Recommendation for review:** select one explicit Shop history configuration
that admits the required occurrences and state replacements without conflating
them. First test whether the existing public profile/program contracts suffice.
A custom Shop profile, if needed, stays adopter-owned and must describe only
semantics the executor actually enforces. If the combination cannot be expressed,
stop that integration and send Core the smallest missing contract, not a Python
branch that silently supplies it. Do not assume profile migration is available.

Specify domain identity, replacement rules, source scope, temporal precision and
the source of every ordering decision. Ledger order records what was accepted
when; it is never evidence of domain event order. An update occurrence with no
new value is not permission to fabricate a replacement value.

**Proof:** a tiny public-only test admits one object, a related occurrence and
an explicit state replacement, then reopens with all three meanings preserved.
An unsupported combination refuses. The exact profile choice returns to Luis
before implementation if it changes the existing adopted semantics.

**Excludes:** universal retail vocabulary, generic profile composition and any
Core API or ontology edit in this task.

**Dependency:** deliverable 1's source boundary.

### Deliverable 3: one connected history, produced from sources

**Output:** one runner consuming the frozen ontology, sources, mappings and
selected admission configuration. It follows the recorded retailer lifecycle,
including shared dependencies between procurement, inventory, invoices,
settlement and shipment. All accepted knowledge enters through public
`KnowledgeChangeSet` preparation/admission and is queried after replay.

Reuse `compile_linkml_contract`, source/evidence constructors, neutral population
plans, public history APIs and record traces. Keep business mappings outside Core.
Use ordinary plans for fixed topology; do not introduce OTTR plumbing merely to
tick a box. Any later recipe use must have a concrete repeated topology to serve.

**Proof:** RED first for the missing connected records and joins. GREEN must
reproduce the independently authored expectations from empty state, preserve
previously admitted facts across each change, and expose every selected record's
source trace. Broken endpoints and stale preparations refuse at their named
transaction boundary. Never roll back or claim to roll back earlier successful
source retention when only a later admission refuses.

**Excludes:** direct graph writes, caller-authored successful check outcomes,
oracle-fed population and one giant transaction for the whole business process.

**Dependency:** deliverables 1 and 2.

### Deliverable 4: the explanation and its counterexamples

**Output:** a small read-only query/check layer producing an evidence-backed
account of order contents, supply changes, invoice/payment relationships,
shipment assignments and eligibility at named checkpoints.

Start with explicit questions a user can inspect:

1. What is recorded for this order, and what changed since the earlier checkpoint?
2. Which participating objects and source occurrences support that account?
3. Which declared condition is satisfied, violated or not decidable from the
   retained evidence, and what changed its result?
4. Which exact source, mapping, rule and accepted checkpoint support each answer?

These are acceptance observations, not a filter permitting the producer to omit
the rest of deliverable 1's declared source coverage.

Implement per-object timelines as read-only derived results first, using explicit
source ordering and typed ambiguity when ordering is unsupported. Do not encode
Event-to-Event edges as ordinary Entity relations. A path or temporal succession
alone is not proof of causation. Bind the query/rule version and input checkpoint
in the Shop report without claiming Core's future generic projection closure.

Reuse the trusted Prolog checker for a selected Shop eligibility rule where it
fits. Freeze the required evidence and completeness scope before evaluating it:
an absent payment record is not automatically proof of an unpaid invoice, and a
missing invoice must not reduce the count and manufacture eligibility.

**Proof:** independently specified before/after and missing-input cases show
exactly why the result changes. Add a wrong-unit or wrong-invoice control and
an unrelated-update control. Keep hypothetical variants separate from the source
history. No successful outcome is entered by hand.

**Excludes:** action authorization, effect execution and counterfactual causal
proof. A recorded historical shipment remains evidence even if it violated a
rule; do not suppress inconvenient observations to make the policy pass.

**Dependency:** deliverable 3; expectation authoring can begin after 1 and 2.

### Deliverable 5: a replayable public showcase

**Output:** one maintained walkthrough and its inspectable evidence bundle:
sources, ontology, compiled facts/contract, selected profile and rules, plans,
ledger, graph excerpt, query witnesses, tests, limitations and exact baseline.
One configured command runs the selected story; a second read-only entry point
inspects its retained history. Use existing dependency configuration.

**Proof:** dispose of the in-memory graph, reopen from retained JSONL, and obtain
the same records, supersession links, traces and query/check results. Compare
full and maintained replay at the selected checkpoints. Repeat from identical
inputs in the same pinned environment. The example's producer cannot read its
independent expected results. A reader follows at least one answer back to an
exact retained source without inspecting private compiler code.

**Excludes:** full chapter replication, universal correctness, constant-time
updates, release automation and new packaging work. Publication remains a
separate approval; preparing this plan does not push or release anything.

**Dependency:** deliverables 3 and 4.

## B. What Malleus can demonstrate on top, and how

The chapter already supplies multi-object modeling, construction, querying and
analysis. Do not claim graphs, queries, source integration or awareness of
incompleteness as Malleus inventions. The proposal is to compose those ideas
with the following tested obligations, not claim historical priority.

| Proposed added guarantee | Mechanism to reuse | Distinguishing Shop observation | Current maturity |
|---|---|---|---|
| Explicit meaning before population | Compiled ontology and identified profile/mapping | Schema alone creates no orders; an unsupported declaration refuses | Existing Core capability; reuse in deliverables 2 and 3 |
| Explain how a fact entered knowledge | Retained sources, field derivations, KCS and trace | An answer reaches its exact row and mapping, including the older corrected record | Existing capability; connected coverage still to prove |
| Govern an admissible change | Executed checks, selected policy, atomic admission | Invalid candidate refuses without accepted-state mutation; valid candidate succeeds | Existing structural and selected-rule examples; no general epistemic-verification claim |
| Preserve changing knowledge | Explicit state replacement and transaction history | Earlier and current answers both reconstruct; missing values remain missing | Existing supplier proof; invoice occurrence and joined story pending |
| Evolve the representation | Additive contract revision | Add first-class shipment structure without erasing older records or reinterpretation by stealth | Existing synthetic sibling; activity-to-entity migration not established |
| Reconstruct rather than trust a saved graph | Full replay, maintained projection, source trace | The same selected answers and evidence survive disposal/reopen and incremental advancement | Existing pieces; one combined receipt required |
| Demonstrate reuse rather than just an interface | Two deliberately different Shop input adapters for equivalent controlled information | Same semantic records, different honest source provenance | Later bounded experiment; not proof of universal replaceability |

The actual contribution claim is about the composition and its observed behavior.
No inspected comparison here establishes that other systems lack these properties.
A head-to-head empirical comparison with the chapter's implementation would
require an exact baseline, identical scope and its own measurement contract.

### Later milestones, not prerequisites for the first connected run

1. **Warehouse enrichment:** add the chapter's later source layer, recompute
   affected per-object views, and inspect how the explanation changes. Only then
   attempt its richer delay analysis, with explicit time and ordering semantics.
2. **Representation growth:** connect the existing synthetic partial-shipment
   and duplicate-assignment proofs to the maintained story. Preserve their
   synthetic status and separate policy selection; no silent policy migration.
3. **Adapter replacement:** use a second controlled source representation and
   compare the declared semantic output while retaining different source identity.
4. **Action consumption:** hand the read-only eligibility/evidence boundary to
   an action or Re-entry consumer. Authorization, grants, execution, independent
   observation and new knowledge remain separate. Re-entry owns its strategy
   experiments; this task does not reproduce them.

Generic Event-ordering artifacts, non-additive migrations, a second interpreter,
generic projection closure and stronger delivery guarantees stay Core-owned
roadmap items unless a Shop test demonstrates a concrete missing dependency.

## Sequence, TDD and review

```text
Source boundary -> Shop model/history choice -> Connected history
                                             -> Explanation + counterexamples
                                             -> Replay evidence + walkthrough
```

Deliverables 1 through 5 define the first milestone. Later milestones are not
required to call that selected milestone complete, and must not be counted as
delivered with it. They preserve the remaining original ambitions visibly.

For each implementation piece: name the expected behavior, write a discriminating
RED, implement the minimum GREEN, run the affected integration path, and record
the exact result and non-claims. Expected semantic results are authored separately
from the producer. A documentation check is not behavioral TDD, and a passing
suite is not human ratification of source interpretation.

Keep a short append-only decision/change section in this Shop plan while it is
being executed, linking source decisions and RED/GREEN receipts. This is project
planning provenance, not accepted domain knowledge or Core's overseer ledger.
An upstream handoff contains only the public reproducer, expected contract,
actual refusal, exact Core baseline and minimum dependency. Do not implement
around an unresolved Core refusal here.

Before implementation, Luis reviews the first milestone and the recommended
history-model direction. Exact semantics are settled in deliverable 2, before
population, not chosen opportunistically to make a test pass.

## Planning record

- 2026-09-08: Shop-only task requested a deliverable plan for the connected story
  and the additional Malleus guarantees. This draft records the proposed scope
  and dependencies. It changes no source fixture, runtime, policy, ledger,
  expectation or previously recorded result.
- 2026-09-08: Luis approved proceeding and explicitly separated Shop from Core.
  Start with retained source coverage, then a public-only history compatibility
  probe. The new work lives in `connected_story/`; predecessor fixtures remain
  unchanged. Core receives requirements, not edits from this task.
- 2026-09-08: Source-boundary RED `9268617e` and GREEN `5383647e` retain the
  selected Table 1 image, 21 rows, 123 nonempty fields and four context excerpts.
  Seven checks pass. Independent human source ratification remains pending.
- 2026-09-08: History compatibility RED `cacc2e4e`; the proposed mixed record
  profile passes the two-row public integration probe, with three tests. The
  profile does not yet have adopted status. A separate probe shows its declared
  state-only correction wording does not itself prohibit Event supersession.
  [Core receives this exact contract question](connected_story/CORE_REQUIREMENT.md).
  Hold final model selection and the full connected population, not unrelated
  source work. No Core runtime, ontology or governance file was edited.
- 2026-09-08: Continue independent source work while Core investigates the
  history restriction. Test-data RED `50b7df40` fails for the missing answer
  file; the [hand-authored expectations](connected_story/EXPECTED_STORY.md)
  make seven source-accounting tests pass. The combined Shop/profile selector
  passes 42 tests. Nine questions are inspection cases, not a smaller source
  boundary, population inputs, a selected graph response format or evidence of
  the finished connected run. No new modeling decision was taken. Core confirms
  custom correction labels alone are descriptive; the enforcement response and
  final Shop history choice remain pending.
- 2026-09-08: Core delivered selected transition-rule enforcement at
  `2ef5442efec6e43f2b2623a288933f7c62d46d4e`. New consumer RED `0f793c54` and
  GREEN `04794b4d6a14ebd9237311d77dc1a26ca8dd9a4e` close the original
  occurrence-replacement counterexample in a fresh restricted history, while
  preserving the original structural-only result. Eight consumer tests and
  the isolated 283-test Shop/transition gate pass. Both matching modes are
  demonstrated, not selected as final policy. This is an explicit successor
  compatibility baseline, not a rebind of released `v0.14.0` receipts.
  [Evidence and remaining choice](connected_story/RESTRICTED_HISTORY.md).
  Core's missing executor dependency is resolved. The recommended first Shop
  rule allows only explicitly named state types; Luis's selection remains
  pending before the final connected ontology/profile and full population.
- 2026-09-08: Luis requested reconsideration against the original goals, then
  accepted the ontology-led recommendation. This supersedes the immediately
  preceding exact-concrete-type recommendation. One abstract Shop recorded-state
  category owns the distinction, and the selected program uses subtype matching.
  The earlier profiles and probes remain unchanged. No new Core behavior was
  requested or implemented.
- 2026-09-08: RED `dd36af1e` records the model and 11 missing-consumer errors.
  GREEN `90c3aeee` builds the new source-produced history over all 21 retained
  Table 1 occurrences; guard commit `f53b48c1` adds same-owner predecessor and
  executable schema-command checks. The [run receipt](connected_story/run_receipt.json)
  binds 123 accounted fields, 21 admitted changes, current and historical state,
  participant joins and exact reconstruction. This is the connected table
  population, not completion of the whole five-deliverable milestone.
  Context remains retained evidence. Next is the declared customer/payment
  explanation and its incomplete-evidence controls; no unpaid balance, shipment
  eligibility, authorization or domain order is inferred by this run.
