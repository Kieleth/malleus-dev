# Malleus: How It Works (From the Code Up)

A Feynman-style walkthrough of the system. No jargon without explanation. Building blocks first, then assembly.

---

## Layer 0: The Vocabulary (What CAN Exist)

Everything starts with a YAML file that says what things are allowed in this universe.

```
malleus.yaml (the root vocabulary)
├── Entity    "a thing that persists"
├── Event     "something that happens"
├── Signal    "a derived quality (computed, not asserted)"
├── Agent     "capability of acting" (mixin, not a class)
└── Relation  "a typed edge between two entities"
```

This is the root. It doesn't know about drugs or hackers. It just knows: things exist, things happen, things relate.

Then a domain extension adds specifics:

```
cyp450.yaml (imports malleus.yaml)
├── Drug      is_a Entity     "a pharmaceutical compound"
├── Enzyme    is_a Entity     "a CYP450 isoform"   [requires: cyp_isoform ∈ {CYP3A4, CYP2D6, ...}]
├── Metabolite is_a Entity    "a product of metabolism"
├── SubstrateOfRelation  Drug → Enzyme
├── InhibitsRelation     Drug → Enzyme
├── InducesRelation      Drug → Enzyme
├── ProducesRelation     Drug → Metabolite
└── InteractsWithRelation Drug → Drug
```

**The key idea:** the ontology is a TYPE SYSTEM. Just like `int` and `string` in a programming language, `Drug` and `Enzyme` are types. If you try to create something that isn't a valid type, it's rejected. Period.

```
OntologyRegistry (ontology.py)
┌─────────────────────────────────────────────────────────┐
│  Loads YAML → builds runtime registry of:               │
│    • All valid types (Drug, Enzyme, ...)                │
│    • All valid enums (CYP3A4, STRONG, ...)              │
│    • Inheritance chains (Drug is_a Entity is_a ...)     │
│    • Effective inherited and mixin slots                │
│    • Required, range, collection, and value constraints │
│    • Concrete relation source and target ranges         │
│    • Strict imports and collision detection             │
│                                                         │
│  This registry is the CONSTRUCTOR PARAMETER of the KG.  │
│  No registry → no KG. That's the rule.                  │
└─────────────────────────────────────────────────────────┘
```

Tests verify strict imports, collision rejection, inherited and mixin slots, schema identity, concrete relation signatures, and closed-world record validation.

---

## Design questions that come up fast

Two distinctions in the vocabulary look clean in the schema and get tested within the first real domain. Here's how they hold under pressure.

### Signal vs Event

The definitions:

- **Event** is an occurrent. It IS the happening. A click, a deployment, an interaction detected. Events have a time (instant or interval) and participants. They don't persist as states; they're records of something that happened.
- **Signal** is a dependent continuant. It's a derived quality that exists as a property of a bearer. A risk score on a user, a health status on a service, a severity on a drug pair. Signals persist, they get recomputed, they have a current value.

The distinction holds even in cases that feel like one thing.

**Case 1: "The risk score updates when the user clicks."**

```
Click happens at T1.
┌──────────────────────────────┐
│ ClickEvent                   │  ← this IS the click
│   occurred_at: T1            │
│   source: user-42            │
│   target: button-pay         │
│   event_type: BUTTON_CLICK   │
└──────────────────────────────┘

Risk recomputation triggered by T1.
┌──────────────────────────────┐
│ RiskSignal                   │  ← this is the user's risk RIGHT NOW
│   bearer: user-42            │
│   value: 0.73                │
│   signal_type: FRAUD_RISK    │
│   computed_at: T1            │
└──────────────────────────────┘
```

The click is an event; it happened at T1 and is done. The risk score is a signal on `user-42`; it had some prior value and now has `0.73` as of `T1`. Next click at T2, the event is a new `ClickEvent` instance, and the signal gets a new `computed_at` and `value`. Same signal entity, new reading.

**Case 2: "An interaction is detected between two drugs."**

```
┌──────────────────────────────┐
│ InteractionDetected          │  ← Event: the moment we noticed
│   occurred_at: T             │
│   source: drug-simvastatin   │
│   target: drug-clarithromycin│
│   event_type: INTERACTION... │
└──────────────────────────────┘

┌──────────────────────────────┐
│ InteractionRiskSignal        │  ← Signal: the risk carried by the pair
│   bearer: pair-sim-cla       │
│   value: 0.9                 │
│   signal_type: INTERACTION...│
│   computed_at: T             │
└──────────────────────────────┘
```

"We found the interaction" is an event. "This pair is risky right now" is a signal. You can have the event without the signal (informational log), the signal without an event (computed at startup from static rules), or both linked.

The shape of the test, whenever the call is close: **if you ask "when did it happen?", it's an Event. If you ask "what's the current value?", it's a Signal.** BFO formalizes this as Occurrent vs Dependent Continuant; the names are optional, the distinction is real.

### Agent as mixin, and how to query for agents anyway

Agent-hood is a capability, not a kind. A Person can act. A Service can act. A Script can act. A Drug cannot. An Enzyme does catalysis (arguably a form of action, in a biological sense) but it doesn't plan or decide. The set of things that can act cross-cuts the set of things that exist.

If Agent were a class, you'd have two bad options:

1. Force multiple inheritance: `Person(Entity, Agent)`, `Service(Entity, Agent)`. Works in Python, breaks LinkML's single-is_a tree and makes the type hierarchy harder to reason about.
2. Put Agent as an Entity subtype and subclass from it. Now you can't model a Person who is also an Agent without making Person is_a Agent (inverting the intent) or inventing `ActingPerson`, `ActingService`, `ActingScript`, which multiplies types along an orthogonal axis. Ugly.

Mixin avoids both. Any Entity subtype can opt into Agent:

```yaml
classes:
  Person:
    is_a: Entity
    mixins: [Agent]
  Service:
    is_a: Entity
    mixins: [Agent]
  Drug:
    is_a: Entity
    # no Agent mixin; drugs don't act
```

The legitimate pushback: you can no longer write `SELECT * WHERE type = Agent`. For a system whose whole point is one-vocabulary queries, that's a real cost. The library pays it back two ways:

- `OntologyRegistry.types_with_mixin("Agent")` returns every type that carries the mixin, including subtypes of types that do. Use it to enumerate schema-level "what can act?"
- `KnowledgeGraph.query(mixin="Agent")` returns every node whose concrete type carries the mixin. The filter is AND with `entity_type` and any property filters, so `kg.query(entity_type="Person", mixin="Agent")` works.

```python
>>> reg.types_with_mixin("Agent")
['Person', 'Service']

>>> kg.query(mixin="Agent")
[{'id': 'alice', 'type': 'Person', ...},
 {'id': 'svc-1', 'type': 'Service', ...}]
```

You get the queryability back without giving up the ontological correctness.

---

## Layer 1: The Graph (What DOES Exist)

The Knowledge Graph is a NetworkX MultiDiGraph (directed, allows multiple edges between the same pair) wrapped with write-time validation.

```
KnowledgeGraph (kg.py)
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  constructor: KnowledgeGraph(registry: OntologyRegistry) │
│                                                         │
│  Every write goes through validation:                   │
│                                                         │
│  create_entity("Drug", "drug-sim", {name: "Simvastatin"}) │
│       │                                                 │
│       ▼                                                 │
│  ┌──────────────┐                                       │
│  │ Is "Drug" a   │──No──→ REJECTED: "Unknown type"      │
│  │ valid type?   │                                       │
│  └──────┬───────┘                                       │
│         │ Yes                                           │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │ Is "Drug" an  │──No──→ REJECTED: "Not Entity subtype"│
│  │ Entity sub?   │                                       │
│  └──────┬───────┘                                       │
│         │ Yes                                           │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │ All required  │──No──→ REJECTED: "Missing slot X"    │
│  │ slots present?│                                       │
│  └──────┬───────┘                                       │
│         │ Yes                                           │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │ Fields, ranges,│──No──→ REJECTED: exact violation     │
│  │ IDs, endpoints │                                      │
│  └──────┬───────┘                                       │
│         │ Yes                                           │
│         ▼                                               │
│     COMMITTED → structurally valid graph materialization │
│     + Operation logged (turn, type, data, status)       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Every** operation (committed or rejected) is logged. The log is the audit trail. You can ask: "at turn 15, what did Shelob try to write, and what happened?"

Tests verify that invalid types, properties, values, identifiers, predicates, and endpoints reject without graph mutation. `COMMITTED` means structural materialization only. It does not mean true, epistemically accepted, or authorized for action.

The separate [Assent Protocol](ASSENT_PROTOCOL.md) defines immutable protocol
records, disjoint assessment and decision outcomes, replay-derived transition
state, and a strict hash-linked JSONL envelope. It does not change the meaning
of `Operation.COMMITTED`.

Related writes can be staged as one isolated candidate:

```text
base KnowledgeGraph + ordered ProposedOperation values
                         |
                         v
                  stage_subgraph()
                         |
          +--------------+---------------+
          |                              |
       invalid                        valid
          |                              |
 no overlay, no base write      CandidateSubgraph overlay
                                         |
                         ontology and base digest still match?
                                         |
                                         v
                               materialize_into(base)
```

Staging supports dependencies inside the candidate, such as a relation whose
endpoints are introduced earlier in the same batch. Materialization rebuilds
on a fresh copy and swaps state only after every operation succeeds. The base
graph and its operation log remain unchanged on validation failure, rule
rejection, stale-base rejection, or an exception before the swap.

Each candidate has a deterministic digest over its ontology, base state, and
exact ordered writes. Later assessment and decision records can cite this
digest without treating the candidate as accepted state.

This is structural materialization, not assent-gated accepted-graph projection.

---

## Layer 2: The Ground Truth (Static Data)

Before Shelob runs, we load curated pharmacological data into the KG.

```
cyp450_seed.yaml → load_cyp450_data() → KnowledgeGraph
┌────────────────────────────────────────────────────┐
│                                                    │
│  3 Enzymes: CYP3A4, CYP2D6, CYP2C9               │
│  14 Drugs:  Simvastatin, Clarithromycin, ...       │
│  15 Relations:                                      │
│                                                    │
│  drug-simvastatin ──SUBSTRATE_OF──→ enz-cyp3a4     │
│  drug-clarithromycin ──INHIBITS(STRONG)──→ enz-cyp3a4 │
│  drug-fluconazole ──INHIBITS(MODERATE)──→ enz-cyp3a4  │
│  drug-fluconazole ──INHIBITS(STRONG)──→ enz-cyp2c9    │
│  drug-rifampin ──INDUCES(STRONG)──→ enz-cyp3a4     │
│  ...                                               │
│                                                    │
│  This is the STATIC layer. Read-only. Never changes.│
│  Shelob can QUERY it but never WRITE to it.         │
│                                                    │
└────────────────────────────────────────────────────┘
```

The Fluconazole dual-axis pattern is the key test case: it inhibits CYP3A4 (moderate) AND CYP2C9 (strong). Any drug metabolized by either enzyme is at risk. This tests multi-hop reasoning.

**12 tests** verify: clean loading, correct counts, data integrity, and that the multi-step reasoning patterns (single interaction chain, multi-enzyme inhibitor, cascading scenario) are traversable.

---

## Layer 3: The Logic Engine (Domain Rules)

`GraphFactCompiler` reads public graph snapshots and emits a closed, domain-neutral vocabulary:

```prolog
m_ontology_hash(OntologyHash).
m_type(OntologyType).
m_mixin(MixinType).
m_subtype(ConcreteType, AncestorType).
m_has_mixin(ConcreteType, EffectiveMixinType).
m_record(RecordId, ConcreteType, RecordKind).
m_relation(RecordId, ConcreteType, SourceId, TargetId).
m_property(RecordId, PropertyName, ScalarKind, Value).
m_list(RecordId, PropertyName, Length).
m_list_item(RecordId, PropertyName, Index, ScalarKind, Value).
```

The compiler does not infer domain predicate names. CYP450, security, and toy ontologies use the same facts. A trusted domain rule program reads those facts and exposes a fixed interface:

```prolog
malleus_rule(RuleId).
malleus_violation(RuleId, ViolationCode, WitnessRecordIds).
```

`LogicContract` pins the resolved ontology hash, fact-contract version, exact rule-program bytes, manifest of rule IDs, artifact versions, and Prolog subprocess wall-clock timeout. `LogicContractArtifact` exposes the canonical semantic fields to replay while retaining separate content-record, semantic-contract, and raw-rule-byte hashes. `PrologVerifier` compiles caller-supplied context and the candidate overlay, starts a fresh SWI-Prolog process, enumerates all violations, validates every rule ID and witness, and returns a canonicalized `LogicCheckResult`. A fresh process prevents facts or rules from leaking between checks. The timeout does not bound graph compilation, output size, memory, or CPU, and the process is not an untrusted-code sandbox. Stage 5 does not establish that caller-supplied context is assent-accepted state.

A completed check has exactly two outcomes. `SATISFIED` means the exhaustive query completed with no violations. `VIOLATED` means it completed with at least one validated witness. Missing entrypoints, syntax errors, manifest mismatches, malformed witnesses, timeouts, and unavailable SWI-Prolog raise `LogicExecutionError`. They are incomplete monitoring, never clean results.

Completed execution evidence becomes an immutable `LogicCheckRecord` plus zero or more `ViolationWitness` records. Failed execution becomes an atomic `MonitorFailure` and `UnavailableAssessment` pair bound to the logical contract and ruleset. These are content-addressed execution attestations with replay-validated bindings, not formal proof certificates or guarantees that another engine run will reproduce the result.

The package ships one CYP450 contract and rule program as a worked example. Stage 5 accepts only trusted, pinned local rules. Sandboxing uploaded or otherwise untrusted Prolog is outside this boundary.

## Layer 3b: Monitoring Policy and Epistemic Control

Stage 6 operates on recorded assessment outputs. It does not run the domain
monitors itself.

```text
MonitorSpecificationArtifact
  assessment kind
  implementation hash
  input artifact IDs and record hashes
            |
            v
EpistemicPolicyArtifact
  exact required monitor records
  VIOLATED control per monitor
  UNKNOWN control per monitor
  explicit control precedence
            |
            v
ProposedSubgraph
  exact policy ID and record hash
            |
            v
PolicyEvaluation
  exact coverage check
  proposal and monitor binding
  selected verdict
  trigger assessment IDs
  canonical evaluation hash
            |
            v
EpistemicDecision
```

All required monitors must contribute exactly one assessment. `SATISFIED`
contributes no control. `VIOLATED` uses the policy's declared `REJECT`, `DEFER`,
or `CONTEST` mapping. `UNKNOWN` can only use `DEFER` or `CONTEST`. If several
controls fire, the policy's stored precedence resolves them deterministically.
Replay recomputes the result and rejects a changed verdict, trigger list, or
evaluation hash.

The proposal pins the policy before monitoring. Replay permits one output from
an exact monitor for that proposal, one completed logical check from an exact
logical monitor, and rejects later competing records. Core
assessment kinds are closed to their standard concrete types, so an ontology
extension cannot claim a core result while omitting its semantic evidence.
The pinned policy is not thereby legitimate. Stage 6 has no policy-authority,
scope, eligibility, or effective-time selection mechanism.

Monitor absence is not treated as an implicit outcome. The failed attempt and
its `UnavailableAssessment` must be recorded atomically. An omitted required
monitor prevents a decision. This preserves provenance and distinguishes an
execution failure from negative evidence.

The same assessment events can exist without an epistemic decision. That is
the code-level boundary between experimental condition C3, monitoring recorded
with control disabled, and C4, the same monitoring followed by explicit policy
control.

## Layer 3c: Assent-Gated Accepted Graph

Stage 7b connects the Stage 4 structural candidate to the Stage 6 epistemic
decision without collapsing their meanings.

```text
Externally supplied graph
  + GraphBaseArtifact
            |
            v
CandidateSubgraphArtifact
  exact ordered writes
  valid-time interval per write
  optional supersession link
  ontology, heads, pre-state, post-state digests
            |
            v
ProposedSubgraph -> monitor outputs -> EpistemicDecision
  exact candidate binding             ACCEPT only
            |                              |
            +------------------------------+
                           |
                           v
              AcceptedGraphApplication
              same event, exact P/D/C binding
                           |
                           v
              replay-derived NetworkX graph
```

The JSONL ledger is authoritative. Candidate registration and accepted
application replay both restage the exact writes against the reconstructed
accepted graph and recompute all digests. A candidate-bound `ACCEPT` requires
one application in the same event. Non-accepting verdicts require none. The
graph is swapped only after the complete event validates.

Four commitments remain distinct: `acceptance_head` for accepted protocol
content, `materialization_head` for ordered graph applications, cumulative
accepted graph state digest, and valid-time view digest. None stands for truth.
Authorization remains a separate state machine and cannot cause accepted graph
materialization or action execution.

Every graph-base record and candidate write has an explicit half-open valid
interval. Supersession creates a new record and closes the prior interval; it
never mutates the ledger history. `AcceptedGraphProjector` selects a verified
transaction prefix and then a valid-time view. A later retroactive correction
therefore changes past valid-time views only for transaction prefixes that
include the correction.

---

## Layer 4: Distributed Convergence (Ontology Hashing)

The `OntologyRegistry` is content-addressable. Two instances that load the same resolved schema produce the same 256-bit hash, regardless of file paths or load order.

```
OntologyRegistry.content_hash() → "a3f7b9c2..." (SHA-256 hex)
OntologyRegistry.fingerprint()  → frozenset{
    "type:Entity",
    "type:Drug:parent:Entity",
    "enum:CYPEnzyme:CYP3A4",
    ...
}
```

**Why this exists.** In a fleet of peers that share a typed KG, different nodes may run different ontology versions during rolling updates. Without a compatibility check, a node can receive data it doesn't understand and silently drop properties. The content hash and fingerprint make the ontology part of the protocol: every write can be tagged with the hash it was produced under, and receivers can verify compatibility before merging.

```
check_compatibility(foreign_hash, foreign_fingerprint) →
  "identical"  same resolved state
  "superset"   I contain everything the foreign registry has (+ more)
  "subset"     they contain everything I have (+ more)
  "divergent"  neither is a superset (incompatible fork)
```

Under additive-only evolution (adding types, enum values, slots, or relaxing required constraints), a newer ontology's fingerprint is always a strict superset of an older one's. The check is a set-membership test: `foreign_fingerprint ⊆ my_fingerprint`.

```
Node A (ontology v2)          Node B (ontology v1)
                                     
h_A = "a3f7..."               h_B = "c9d2..."
fp_A = {type:Drug,            fp_B = {type:Drug,
         type:Enzyme,                  type:Enzyme,
         type:Metabolite,              enum:CYPEnzyme:CYP3A4,
         enum:CYPEnzyme:CYP3A4,        ...}
         enum:CYPEnzyme:CYP1A2,
         ...}
                                      
         B sends data to A:
         A.check_compatibility(h_B, fp_B) = "superset"
         → A accepts: B's data validates against older fp, A's ontology supports it.
         
         A sends data to B:
         B.check_compatibility(h_A, fp_A) = "subset"
         → B quarantines entries using types it doesn't know yet,
           replays them when B upgrades to v2.
```

**What's excluded from the default fingerprint, and why that matters.** Required/optional flags are deliberately left out, because additive-only evolution permits relaxation (required → optional) and the default check is meant to answer the producer question: "can data produced under their schema flow safely into mine?" Under relaxation, yes, a newer producer can send data without a field the older schema marked required, and the sync doesn't care (the consumer's validator will).

That's the soft spot. Relaxation is additive for the producer and subtractive for the consumer, because code written against the old schema may have hardcoded the field's presence. The library surfaces this through a second pair of APIs:

- `OntologyRegistry.strict_fingerprint()` includes required-constraint facts (one per required slot usage).
- `OntologyRegistry.check_compatibility_strict()` uses it.

A relaxation breaks the strict superset check: the schema that relaxed has fewer required-facts, so its strict fingerprint is no longer a superset. The strict check returns "divergent" where the lax check would have returned "superset". Use the strict variant when your downstream code relies on presence assumptions.

Tightening (optional → required) is not an additive change and isn't supported under either guarantee.

**Tests** verify: hash determinism, SHA-256 format, distinct schemas produce distinct hashes, caching, fingerprint content (types, mixins, enum values, serialization), strict-superset relationships (root ⊂ cyp450, root ⊂ attack), divergence (cyp450 and attack share root but diverge on domain types), all four `check_compatibility` outcomes, and that strict fingerprints catch constraint relaxation.

---

## The Full Stack (Library)

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Application                         │
│              (Claro, Shelob, Colibri, ...)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   KnowledgeGraph (kg.py)                    │
│  MultiDiGraph wrapper. Write-time validation.               │
│  create_entity / create_relation / create_signal / ...      │
│  Every operation logged (turn, type, status, data).         │
└────────┬──────────────────────────────────────┬─────────────┘
         │                                      │
         │ validates against                    │ compiles typed facts for
         ▼                                      ▼
┌────────────────────────┐            ┌──────────────────────┐
│  OntologyRegistry      │            │   PrologVerifier     │
│    (ontology.py)       │            │ (prolog_verifier.py) │
│                        │            │                      │
│  Loads LinkML YAML     │            │  SWI-Prolog bridge   │
│  Types, enums, slots   │            │  LogicContract       │
│  is_subtype_of()       │            │  verify_candidate_   │
│  content_hash()        │            │    subgraph(...)     │
│  fingerprint()         │            │  LogicCheckResult    │
│  check_compatibility() │            │                      │
└────────────────────────┘            └──────────────────────┘
```

The root ontology (`malleus.yaml`) is mandatory; the domain extensions (`cyp450.yaml`, `attack.yaml`) are examples. Logic execution requires a `swipl` executable on `PATH` and fails explicitly when it is absent.

---

## Test Coverage

- `tests/test_ontology.py`: strict loading, imports, collisions, effective slots, instance validation, hashing, fingerprints, and compatibility.
- `tests/test_kg.py`: mutation-free rejection of invalid types, properties, ranges, collections, identifiers, predicates, and endpoints, plus operation logging and queries.
- `tests/test_staging.py`: isolated candidate validation, intra-candidate dependencies, stale-base rejection, and atomic structural materialization.
- `tests/test_logic.py`: pinned contract loading, domain-neutral fact compilation, deterministic hashes, and protocol-record construction.
- `tests/test_control.py`: exact monitor coverage, outcome mappings, precedence, evaluation hashing, and explicit unavailable-monitor records.
- `tests/test_prolog_verifier.py`: process isolation, exhaustive violations, malformed-result rejection, injection resistance, timeout handling, and mutation-free candidate verification.
- `tests/test_protocol.py`: atomic check and witness recording, artifact binding, assessment agreement, and failure-to-`UNKNOWN` replay.

---

## Public API

```python
from malleus import (
    KnowledgeGraph,
    LogicContract,
    OntologyRegistry,
    PrologVerifier,
    ProposedOperation,
    stage_subgraph,
)

reg = OntologyRegistry("path/to/your_schema.yaml")
print(reg.content_hash())              # deterministic 64-char hex
print(len(reg.fingerprint()))          # set of atomic facts
print(reg.check_compatibility(other_hash, other_fingerprint))  # identical|superset|subset|divergent

kg = KnowledgeGraph(reg)
op = kg.create_entity("Drug", "drug-001", {"name": "Simvastatin"})
# op.op_status ∈ {COMMITTED, REJECTED}; op.rejection_reason if rejected

contract = LogicContract.load("path/to/your_logic_contract.yaml")
verifier = PrologVerifier(contract)
candidate = stage_subgraph(kg, [
    ProposedOperation.relation(
        "InhibitsRelation", "relation-001", "drug-001", "enz-001",
        {"relation_type": "INHIBITS", "inhibition_strength": "STRONG"},
    )
])
result = verifier.verify_candidate_subgraph(candidate)
# result.valid, result.outcome, result.violations
if result.valid:
    candidate.materialize_into(kg)
```
