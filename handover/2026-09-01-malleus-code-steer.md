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

**The lab does not use malleus.** Zero imports from `malleus.*` in `src/`. `code.yaml`
imports the root ontology, which is right. Everything under it, about 2,500 lines,
reimplements the ledger, canonical JSON, exact-field checks and atomic writes.
`_exact_fields` and `_unique_object` in `store.py` are near-verbatim copies of
`malleus/ledger.py`. This is the third hand-rolled malleus ledger found in the
estate today, and none of the three recorded why.

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

Do not build a second ledger. There are already three.

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
