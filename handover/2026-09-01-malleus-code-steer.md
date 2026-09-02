# Malleus-code: steer

Owner decisions, 2026-09-01, after an overseer review of the lab at
`malleus-code-lab` (241 commits, HEAD `51c23eb`, 2,690 ledger entries, 9,520 src
lines, 430 tests). The review confirmed the Codex distillation's diagnosis on every
point tested and found three things it did not say. Both are below. The decisions
are the owner's. The sequencing is dependency order, not time.

---

## The four decisions

1. **Reuse malleus.** The lab's `store.py`, `transaction.py`, `validation.py` and
   `shacl.py` are replaced by `malleus.kg.KnowledgeGraph`, `malleus.staging`,
   `malleus.ledger.JsonlLedger` and `malleus.assent.ProtocolLedger`. No parallel
   ledger implementation survives.

2. **Two tiers, one graph.** A staged tier for intents, hypotheses, deliverables,
   dependencies, observations and learnings, validated for shape at write time and
   revisable by supersession. An accepted tier holding exactly two kinds of fact:
   a deliverable is done, backed by evidence, and code merged to main. The gate
   lives at the accepted tier only, because that is where the side effects are.

3. **Cut the ceremony from the default skill and park it behind a dojo mode.** The
   default skill is the method. Dispatch, input freezing, launch packets, closure
   receipts and ATGR become a mode an operator switches on for a controlled
   comparison and nobody meets by accident.

4. **Another dispatched run**, under the new skill and the new graph. Not Run 09 of
   the old apparatus.

---

## Why, grounded

**Correction, 2026-09-02.** The steer as first written said the lab had zero
imports from `malleus.*`. That was a grep error on the reviewer's side: the filter
excluded every path containing `malleus_code_lab`, which is all of them. The lab
imports malleus in twelve modules; `store.py` alone imports six names from
`malleus.ledger`. What remains true and narrower: `_exact_fields` and
`_unique_object` in `store.py` duplicate functions that `malleus/ledger.py` already
exports, beside imports of that same module. Partial reuse with local copies, not
a parallel implementation. The "third hand-rolled ledger" claim is withdrawn for
this lab; it stands for the core overseer scripts, which were checked separately
and do not import malleus at all.

**The graph is 1 percent intention.** Of 2,690 entries: 3 `Intent`, 11
`SoftwareChangeHypothesis`, 35 `Deliverable`. Against 305
`EvidenceForArtifactRelation`, 232 `AssessesRelation`, 197 `ArtifactVersion`. The
thing the graph was for is the thing it holds least of.

**The single tier is the cause, not a symptom.** Every write today goes through the
strict transaction path with frozen inputs and receipts. So writing a hypothesis
costs what merging code costs, and the graph fills with what was already expensive.
Malleus's design is two tiers precisely to avoid this. The lab copied the ledger and
did not copy the split.

**There is no frontier.** No function in 9,520 lines computes readiness, eligibility
or blocked state. The living DAG has no code behind it. `query.py` is 1,200 lines and
answers other questions.

**The method is buried.** `SKILL.md` is 587 lines. The method sections start at line
288. The first thing an agent reads, at line 114, is that prompt-rendered text is
not the controlled byte artifact.

**The hypothesis has no edge to the deliverable.** `code.yaml:787-855` relates
`Hypothesis` to Requirement, Attempt and Learning. Not to Deliverable. The
engineering argument is unrepresentable in the current ontology.

**Run 01 worked.** Its own learnings: a single agent voluntarily planned, built,
repaired a material learning, and stopped before acceptance. Its two P1 findings,
clause-coverage overclaim and manual authoring cost, became the product centre for
the next seven runs. Run 08 forbids `parent_repository_discovery` and requires a
fresh git, fresh ledger and absent output directory. That is a controlled
experiment. Nobody develops software that way.

---

## The work, in dependency order

### 1. One relation and one query. Nothing else first.

Add `DeliverableOperationalizesHypothesisRelation` to `code.yaml`. Hypothesis is the
source, Deliverable the target. Without it the graph cannot say why a deliverable
exists.

Write the frontier query over the staged graph:

```
frontier(graph) -> deliverables in the staged tier
                   whose every DependsOn target is accepted
                   and which are themselves not yet accepted
```

About fifty lines. It should also return, per deliverable, why it is or is not on
the frontier: which dependency blocks it, or which evidence is stale. This is the
living DAG. It is the deliverable of this step and the thing the next run uses.

### 2. Replace the store with malleus.

Map the lab's records onto malleus primitives:

| Lab today | Malleus |
|---|---|
| `store.py` write path | `KnowledgeGraph.create_entity / create_relation / create_event`, which refuse on shape |
| `transaction.py` strict transaction | staged tier: `malleus.staging.stage_subgraph(graph, writes)`; accepted tier: `ProtocolLedger` with `PROPOSAL_RECORDED` then `EPISTEMIC_DECIDED` |
| hand-rolled ledger file | `JsonlLedger(path, ontology_hash)` with the hash of `code.yaml` |
| `validation.py`, `shacl.py` | `OntologyRegistry.validate_instance`, closed-world, already enforced by `KnowledgeGraph` |

The accepted tier uses assent's own verdicts, `ACCEPT / REJECT / DEFER / CONTEST`,
and proposal states, `PROPOSED / ACCEPTED / REJECTED / DEFERRED / CONTESTED`. Do not
invent a parallel vocabulary; the ontology in `assent.yaml` already has one and the
inquisitor's rites already know it.

Migrate the 2,690 entries by replay into the new store. They are history; they do
not get edited. If replay refuses some, record which and why. That is a finding.

### 3. Split the skill.

Default `SKILL.md` becomes the three method sections, lines 288 to 564 today,
rewritten against the two tiers: structure work before coding, declare the delivery
contract, build one thin slice. Add the frontier as the thing an agent consults at
every work boundary, replacing "recheck the DAG" prose with one command.

Everything from line 12 to 287, plus `launch_packet.py`, `pilot_closure.py` and
`formalization.py`, moves to `dojo` mode. Loaded only when an operator asks for a
controlled comparison. Kept in git. Not deleted.

### 4. Demote the code index.

`code_index.py` and `python_extractor.py`, 2,061 lines, are the code-structure view.
Useful later, not the product. Leave them, stop building on them until a
deliverable needs impact analysis.

### 5. Run the dispatched pilot.

Conditions, stated so the run measures the method and not the apparatus:

- One agent, the new default skill, the new store, a real repository it may read.
- The task brief is a desired outcome, not a deliverable list. The agent writes the
  intents and hypotheses itself, into the staged tier, and decomposes.
- The agent consults the frontier at every boundary and records why it picked what
  it picked.
- Acceptance of a deliverable goes through the epistemic gate with evidence. Nothing
  else is gated.
- No frozen inputs, no launch packet, no closure receipt. Git is the source of truth
  for bytes; the graph is the source of truth for meaning.
- The measure is one question: **could a second agent, given only the graph, pick up
  the work where the first stopped?** Not whether the bookkeeping was obeyed.

Record what the agent wrote into the staged tier that turned out to be wrong. That
is not a defect. A wrong hypothesis written and superseded is the method working.

---

## What not to do

Do not design a new ontology before step 1. `code.yaml` is the best artifact in the
lab. It needs one relation.

Do not write a method oracle before running the method. The proposed "end-to-end
method oracle that proves this exact recursive cycle before implementation resumes"
is another design phase in front of the work. Run the pilot; the oracle is what the
pilot's frontier query already checks.

Do not add a gate when the next pilot finds a gap. Record the gap as a learning in
the staged tier and decide at the following boundary whether it needs a gate. The
last seven runs each added a gate the moment a gap appeared. That is the loop this
steer exists to break.

Do not build a second ledger. The core overseer already did, and it is the reason that rig cannot answer the question its program is about.

---

## Kept, demoted, cut, replaced

| | |
|---|---|
| **Kept** | `code.yaml` plus one relation. The 2,690-entry ledger as history. Entries 1 to 12, which are the vision and are still right. |
| **Demoted** | `code_index.py`, `python_extractor.py`. |
| **Cut from default, parked in dojo** | `SKILL.md` lines 12 to 287. `launch_packet.py`, `pilot_closure.py`, `formalization.py`. |
| **Replaced by malleus** | `store.py`, `transaction.py`, `validation.py`, `shacl.py`. |

---

## Context

`handover/2026-09-01-malleus-core-review.md` in `malleus-dev` for the core review
that found the same reinvention in the contract-compiler overseer. The pattern is
identical across three codebases: a small good idea, a large careful apparatus, and
the apparatus aimed slightly away from the idea.

---

# Addendum, 2026-09-02: bootstrap accepted, acceptance authority decided

## Bootstrap slice

Accepted. Verified independently: `frontier.py` on `CandidateSubgraph` against
`AcceptedGraphView`, `accepted.jsonl` beside `ledger.jsonl`,
`test_fresh_project_enters_the_two_tier_frontier_loop_once`, the skill at 182 lines
with the method as its headings, 472 passed.

## Acceptance authority

Not a choice between self-accept and another actor. **Acceptance authority is a
tree of grants, recorded in the graph, walked by `decide()`.**

Malleus already has the primitive. `AuthorityGrant` in `assent.yaml` carries
`grantor_actor_id`, `grantee_actor_id`, `permitted_action_types`,
`grant_valid_from`, `grant_valid_to`, and core implements
`verdict-scoped-authority-grant-validation`. The lab's `accepted_tier.py::decide()`
takes `reviewer_actor_id` as a free string and consults no grant. That is the
defect to fix, and it is a reuse, not a design.

### The model

Each grant names who granted, to whom, what they may accept, over which part of
the work, and whether they may grant further down. Authority attenuates: a grantee
never holds more than its grantor gave. At any one level the builder is not the
acceptor; a level below, the same actor may accept its own steps if its grant says
so. The root grant, product acceptance, is held by the human and cannot be
delegated.

```
human   grants  <top-agent>   accept: DELIVERABLE   scope: <project>   may sub-delegate: yes
<top>   grants  <sub-agent>   accept: TDD_STEP      scope: <deliverable>   may sub-delegate: no
human   retains               accept: PRODUCT       scope: <project>   may sub-delegate: no
```

Every acceptance in the accepted tier names the grant it was made under. A reader
walks the tree.

### Two slots `AuthorityGrant` lacks, both required

1. **Scope narrower than an action type.** Today a grant says "may ACCEPT." It must
   be able to say "may accept this deliverable and its descendants." One slot, a
   record id, on the existing class.
2. **Whether the grantee may sub-delegate.** Attenuation needs a boolean on the
   grant. One slot.

These belong in core `assent.yaml`, not in `code.yaml`, because the OCR profile's
mandate B3 needs the same two. Raise them upstream as one change; do not fork the
class locally.

### What `decide()` must do

Refuse any verdict whose actor holds no grant covering that verdict, that scope,
and that time. Record the grant id on the decision. A self-acceptance is legitimate
exactly when the actor's grant covers that level, and is refused everywhere else.
No unmarked self-accept survives.

### For the single-agent pilot

At bootstrap, write the grants:

```
human    grants  agent-1  accept: TDD_STEP, DELIVERABLE   scope: project   may sub-delegate: no
human    retains          accept: PRODUCT                 scope: project
```

The agent accepts its own deliverables under a grant that says it may. The graph
shows `PRODUCT: pending`. The second-agent continuation test starts from that
state. This is the honest single-agent configuration, written down instead of
assumed.

### Standing limit

`protocol-actor-registration` is pending in core, so grantor and grantee are
strings. The tree can be recorded and walked. It cannot yet be checked against a
registry of who exists. State that in the pilot's handoff rather than around it.

## Sequence, confirmed

1. Bootstrap accepted, above.
2. Grants: two slots upstream, `decide()` consults `AuthorityGrant`, bootstrap
   writes the pilot's grants. If this grows past that, stop and say so.
3. One fresh pilot, under the default skill, brief as a desired outcome.
4. Second agent, repository and graph only. The measure is whether it knows what
   to do next and why. Nothing else is measured.
5. That run is the acceptance evidence for the default skill.

Runs 01 through 08 are sunk. They predate the two tiers and do not bear on this
version. Written once, here, so nobody reaches for them later.

---

# Addendum 2, 2026-09-02: no to the widening

Codex's correction is right about the fact and wrong about the fix.

## The fact, verified

`AuthorityGrant` is consumed by `AuthorizationDecision` (`authority_grant_id`,
`authority_grant_hash`, `authorized_actor_id`, validity interval) and by
`AuthorityAssessment`. `EpistemicDecision` carries no grant slot. The lab's
`accepted_tier.py` emits `EPISTEMIC_DECIDED` and applies the graph, and emits no
`AuthorizationDecision`. So a grant cannot bind to what the lab currently calls
acceptance.

## Why that is the lab's error and not core's gap

`docs/ASSENT_PROTOCOL.md`, first sentence: "Malleus separates structural graph
materialization, epistemic acceptance, and action authorization. These are
different operations with different records and state machines."

Accepting a deliverable is two of those, and the lab collapsed them into one.

- **Epistemic**: the evidence shows the contract is met. TDD green, invariants hold,
  acceptance tests pass. A belief about evidence. Policy-driven, monitor-driven,
  and identity has no bearing on it. Whether the tests passed does not depend on
  who is looking.
- **Authorization**: given that belief, advance the frontier past this deliverable.
  An act with consequences. This is what `AuthorityGrant` governs, and
  `AuthorizationDecision` already requires `epistemic_decision_ids` as input. The
  chain is native: believe first, then authorize under a grant.

The owner's example maps onto it exactly. "TDD is working fine" is epistemic.
"Continue to the next slice" is authorization under the sub-agent's grant.
"Product approved" is authorization at the root under the human's grant. The grant
tree lives entirely in the authorization layer, where core already put it.

## Decision

**No widening of the core contract. Two slots on `AuthorityGrant` and nothing
else upstream:** a scope narrower than an action type, and whether the grantee may
sub-delegate.

Acceptance in the lab becomes two events, not one:

1. `EPISTEMIC_DECIDED` over the deliverable's evidence. No grant. Unchanged in
   meaning from today.
2. `AUTHORIZATION_DECIDED` over a concrete `ActionProposal` that `code.yaml`
   defines, `AdvanceDeliverableAction`, referencing the epistemic decision in
   `epistemic_decision_ids`. The grant binds here. Core validates actor, grant,
   interval; the new scope slot narrows it to the deliverable subtree.

Everything else on Codex's list is lab-side and mostly reuse:

| Codex asked for | What it is |
|---|---|
| grant enforcement for acceptance | emit the second event; core already validates grants on `AuthorizationDecision` |
| parent-grant lineage and attenuation | the two upstream slots, then a walk the lab writes over the grant records |
| replay refusal for wrong actor, scope, time, delegation | `verdict-scoped-authority-grant-validation` is implemented in core; scope and delegation need the two slots |
| explicit mapping for TDD-step, deliverable, product | three `action_type` values on the concrete `ActionProposal`, in `code.yaml` |
| product-pending projection | a query over `AuthorizationState`, which already has `PENDING`, `AUTHORIZED`, `BLOCKED`, `CLARIFICATION_REQUIRED` |
| bootstrap grants and grant-aware `decide()` | `decide()` becomes two steps; bootstrap writes the grants |

`ActionProposal` is abstract in `assent.yaml` with the note "Domain ontologies
define concrete action payload types." That is the invitation core already
extends. Accept it rather than growing `EpistemicDecision`.

## What the widening would have cost

Identity in the belief layer, so whether evidence is believed depends on who is
looking, which the epistemic stage exists to make impossible. Grant fields on every
adopter's epistemic decision. And a second authorization mechanism beside the one
that exists, which is the pattern now found five times in three days across this
estate.

## The honest cost of this answer

More lab work than "two slots and one refusal": acceptance is restructured from one
event to two, and one concrete action class is defined. Less core work, and it is
the design malleus is built on rather than a fork of it.

## The bootstrap slice

Still accepted. Do not materialize it through the free-string reviewer path, as
Codex correctly declined to. Materialize it as the first two-event acceptance once
the second event exists. Until then it is accepted in the handover and pending in
the graph, and that gap is stated, not hidden.
