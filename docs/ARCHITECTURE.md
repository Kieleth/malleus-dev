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
└── DrugRelation is_a Relation
    └── relation_type ∈ {SUBSTRATE_OF, INHIBITS, INDUCES, PRODUCES, INTERACTS_WITH}
    └── inhibition_strength ∈ {WEAK, MODERATE, STRONG}
```

**The key idea:** the ontology is a TYPE SYSTEM. Just like `int` and `string` in a programming language, `Drug` and `Enzyme` are types. If you try to create something that isn't a valid type, it's rejected. Period.

```
OntologyRegistry (ontology.py)
┌─────────────────────────────────────────────────────────┐
│  Loads YAML → builds runtime registry of:               │
│    • All valid types (Drug, Enzyme, ...)                │
│    • All valid enums (CYP3A4, STRONG, ...)              │
│    • Inheritance chains (Drug is_a Entity is_a ...)     │
│    • Required slots (Enzyme requires cyp_isoform)       │
│    • Enum constraints (cyp_isoform must be in CYPEnzyme)│
│                                                         │
│  This registry is the CONSTRUCTOR PARAMETER of the KG.  │
│  No registry → no KG. That's the rule.                  │
└─────────────────────────────────────────────────────────┘
```

**26 tests** verify: schemas load, types exist, enums have the right values, required slots enforced.

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
│  │ Enum values   │──No──→ REJECTED: "Invalid value"     │
│  │ valid?        │                                       │
│  └──────┬───────┘                                       │
│         │ Yes                                           │
│         ▼                                               │
│     COMMITTED → node added to NetworkX graph            │
│     + Operation logged (turn, type, data, status)       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Every** operation (committed or rejected) is logged. The log is the audit trail. You can ask: "at turn 15, what did the LLM try to write, and what happened?"

**38 tests** verify: valid writes commit, invalid types/enums/slots reject, duplicates reject, endpoints verified, strength range checked, queries work, domain isolation works (Drug rejected in ATT&CK KG).

---

## Layer 2: The Ground Truth (Static Data)

Before any LLM runs, we load curated pharmacological data into the KG.

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
│  The LLM can QUERY it but never WRITE to it.       │
│                                                    │
└────────────────────────────────────────────────────┘
```

The Fluconazole dual-axis pattern is the key test case: it inhibits CYP3A4 (moderate) AND CYP2C9 (strong). Any drug metabolized by either enzyme is at risk. This tests multi-hop reasoning.

**12 tests** verify: clean loading, correct counts, data integrity, and that the multi-step reasoning patterns (single interaction chain, multi-enzyme inhibitor, cascading scenario) are traversable.

---

## Layer 3: The Logic Engine (Domain Rules)

Prolog rules encode what FOLLOWS from the facts in the KG.

```
cyp450_rules.pl
┌────────────────────────────────────────────────────┐
│                                                    │
│  % If Drug A inhibits an enzyme that metabolizes   │
│  % Drug B, then A increases B's exposure.          │
│                                                    │
│  interaction(A, B, increased_exposure, Enz, Str) :-│
│      inhibits(A, Enz, Str),                        │
│      substrate_of(B, Enz),                         │
│      A \= B.                                       │
│                                                    │
│  % Also: combined inhibition, polypharmacy risk,   │
│  % contradiction detection (can't be strong         │
│  % inhibitor AND strong inducer of same enzyme)    │
│                                                    │
└────────────────────────────────────────────────────┘
```

The PrologVerifier bridges Python to SWI-Prolog:

```
PrologVerifier (prolog_verifier.py)
┌────────────────────────────────────────────────────┐
│                                                    │
│  sync_from_kg(static_kg, dynamic_kg)               │
│       │                                            │
│       ▼                                            │
│  KG nodes → Prolog facts:                          │
│    drug('drug-sim', 'Simvastatin', 'statin').      │
│    enzyme('enz-cyp3a4', 'CYP3A4', 'CYP3A4').      │
│    substrate_of('drug-sim', 'enz-cyp3a4').         │
│    inhibits('drug-cla', 'enz-cyp3a4', strong).     │
│                                                    │
│  Then query:                                       │
│    ?- interaction('drug-cla', X, Effect, Enz, Str).│
│    X = 'drug-sim'                                  │
│    Effect = increased_exposure                     │
│    Enz = 'enz-cyp3a4'                              │
│    Str = strong                                    │
│                                                    │
│  verify_proposed_relation(static_kg, dynamic_kg,   │
│      source_id, target_id, relation_type, props)   │
│       │                                            │
│       ▼                                            │
│  Syncs all facts → tentatively asserts proposed    │
│  fact → checks for contradictions → retracts →     │
│  returns valid/invalid with proof trace             │
│                                                    │
└────────────────────────────────────────────────────┘
```

**12 tests** verify: known drug-drug interactions detected (inhibitor + substrate on the same enzyme), induction detected (inducer + substrate), multi-enzyme effects detected, combined inhibition detected, contradictions caught (same drug as strong inhibitor and strong inducer), and that verification is read-only (never mutates the KG).

The Prolog rule file shown here is an example. The library ships only the generic `PrologVerifier` class. You bring your own `.pl` rules for your domain.

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
         │ validates against                    │ optionally syncs into
         ▼                                      ▼
┌────────────────────────┐            ┌──────────────────────┐
│  OntologyRegistry      │            │   PrologVerifier     │
│    (ontology.py)       │            │ (prolog_verifier.py) │
│                        │            │                      │
│  Loads LinkML YAML     │            │  SWI-Prolog bridge   │
│  Types, enums, slots   │            │  sync_from_kg(*kgs)  │
│  is_subtype_of()       │            │  verify_proposed_    │
│  content_hash()        │            │    relation(...)     │
│  fingerprint()         │            │  (you supply .pl)    │
│  check_compatibility() │            │                      │
└────────────────────────┘            └──────────────────────┘
```

The library is three classes and three LinkML files. The root ontology (`malleus.yaml`) is mandatory; the domain extensions (`cyp450.yaml`, `attack.yaml`) are examples. The Prolog verifier is optional (requires `pip install malleus-dev[prolog]` and SWI-Prolog on the system).

---

## Test Coverage

```
tests/test_ontology.py      45 tests   Schema loading, types, enums, mixins,
                                       hash, fingerprint, compatibility check.
tests/test_kg.py            38 tests   Write-time validation (invalid types,
                                       enums, slots, duplicates, endpoints),
                                       operation log, queries, domain isolation.
tests/test_prolog_verifier.py 12 tests Prolog sync, interaction detection,
                                       contradiction catching, read-only
                                       verification.
                           ─────
                           95 tests    ~3 seconds, all green.
```

---

## Public API

```python
from malleus import OntologyRegistry, KnowledgeGraph, PrologVerifier

reg = OntologyRegistry("path/to/your_schema.yaml")
print(reg.content_hash())              # deterministic 64-char hex
print(len(reg.fingerprint()))          # set of atomic facts
print(reg.check_compatibility(other_hash, other_fingerprint))  # identical|superset|subset|divergent

kg = KnowledgeGraph(reg)
op = kg.create_entity("Drug", "drug-001", {"name": "Simvastatin"})
# op.op_status ∈ {COMMITTED, REJECTED}; op.rejection_reason if rejected

verifier = PrologVerifier("path/to/your_rules.pl")  # optional
result = verifier.verify_proposed_relation(
    kg, source_id="drug-001", target_id="enz-001",
    relation_type="INHIBITS", properties={"strength": "strong"},
)
# result.valid, result.rule_violated, result.proof_trace
```

