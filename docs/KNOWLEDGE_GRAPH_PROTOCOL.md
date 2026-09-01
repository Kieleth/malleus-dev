# Knowledge Graph Protocol

How to build a governed Knowledge Graph under a bound ontology and admission
contract.

This document defines an `OPTIONAL_PROFILE`: the default typed-graph structural
admission profile. An adopter can preserve Malleus protocol invariants with a
different data model or without materializing a knowledge graph. The
LinkML-shaped registry, Python `KnowledgeGraph`, and NetworkX store described
below are the current reference implementation, not universal wire or storage
requirements.

---

## Core principle: the ontology is the KG's constitutive grammar

The current `KnowledgeGraph` binds an `OntologyRegistry`, and current protocol
events bind that registry's ontology hash. The registry defines which records
the governed graph can admit and how their structural vocabulary is
interpreted. The ontology is not reality and the graph is not truth by
construction. It expresses scoped ontological commitments. Without a bound
registry, a current Malleus governed graph cannot be constructed.

The accepted contract-compiler design introduces a frontend-neutral
`EffectiveContract` composed from validated contract facts and interpreted
under normative admission profiles. OD-006 defines a separate
`ContractComposition` containing exactly one `ProtocolRecordContract`, one
`GovernedGraphContract`, and one `GovernanceContract`; each role is an
`EffectiveContract`. That composition is not bound by the current runtime or
ledger. `EffectiveContract` is the accepted future runtime root; a reloadable
`EffectiveContractArtifact` remains a Candidate and has no implemented public
API.

This is the TBox/ABox split from Description Logic:

- **TBox** (terminological box): the schema. Defines concepts, relationships, and constraints. Stable, versioned, changes rarely.
- **ABox** (assertional box): the instances. Contains the actual data. Dynamic, changes constantly.

Within the current runtime, ABox writes use the vocabulary and constraints in
the bound registry. In the accepted future design they use the exact effective
contract composition and admission profiles. A semantic change to an
accepted-temporal contract role requires a new composition and ledger epoch
under OD-006. A nonsemantic source edit that preserves effective-contract
identity does not. Current records retain their bytes, content identity, and
recorded ontology hash. They do not retain a complete reader, interpretation-
profile, or effective-contract identity.

## Two architectures and this profile's choice

**Architecture A: Ontology defines KG (constitutive)**
```
Ontology (YAML) --> OntologyRegistry
                           |
                           v
                 KnowledgeGraph(registry)
                           |
                           v
                 Every write checked as a precondition
                 Nonconforming writes rejected at the call
```

The registry is a constructor parameter. The KG is born with its type system.
Writes nonconforming to the configured structural contract are rejected before
this governed materialization changes. The type system is constitutive for the
records Malleus admits in that contract epoch.

**Architecture B: KG validates against ontology (descriptive)**
```
KG exists (freeform) <-- writes data freely
         |
         v (periodic or on-query)
Ontology consulted as external reference
         |
         v
Validation report (after the fact)
```

The KG is independent. The ontology is an external document. Non-conforming
data may remain materialized while a validator reports it.

This profile selects Architecture A for its governed graph. Architecture B
is valid for diagnostics, migration analysis, and systems whose contract is to
report rather than gate. It cannot provide Malleus's pre-materialization
invariant by itself. Store-specific SHACL gates and other validating databases
also implement variants of Architecture A; write gating is not a Malleus
invention.

## Principles

### 1. A governed KG in this profile cannot be constructed without an ontology

The registry loaded from the ontology is a required constructor parameter. No
registry, no governed `KnowledgeGraph`.

```python
registry = OntologyRegistry("path/to/domain.yaml")
kg = KnowledgeGraph(registry)
```

### 2. Every write is validated as a precondition, not a post-hoc check

When you create an entity, its type must exist in the registry. When you create
a relation, the relation type must exist and the source and target entity types
must match its endpoint constraints. Properties supplied during record creation
must be declared for that record type and satisfy their constraints.

This happens at the point of the call. Writes nonconforming to the configured
structural contract are rejected immediately and do not materialize in the
governed graph. This establishes structural conformance, not factual validity.

Relation predicates with different endpoint signatures use different LinkML classes. A concrete relation fixes `relation_type` with `equals_string` and narrows `source_id` and `target_id` to class ranges. A generic relation enum cannot express this contract and is not accepted as a substitute.

`COMMITTED` is the result of this structural boundary only. It does not establish truth, epistemic acceptance, policy approval, or authorization to execute an action.

### 2A. Stage related writes as one isolated candidate

Some structural claims require several records at once. A relation may depend on entities introduced by the same proposal. Validating and committing each write separately creates partial state when a later member fails.

`stage_subgraph()` applies an ordered batch to an isolated graph copy. Members can depend on earlier members in the same batch. The `candidate_digest` binds the ontology hash, base-state digest, and exact ordered writes for later provenance records. Successful candidate operations report `STAGED`; the base graph and its audit log remain unchanged. If any member fails, the candidate exposes the rejection but has no usable overlay and cannot be materialized.

`CandidateSubgraph.materialize_into()` checks that the ontology and base-state digest still match, rebuilds the candidate on a fresh copy, and replaces materialized state only after the full batch succeeds. A stale candidate cannot overwrite intervening graph changes.

This is a structural transaction boundary. It does not decide truth, epistemic acceptance, or action authorization. Stage 7b can record the exact writes in a `CandidateSubgraphArtifact` and couple an accepted protocol decision to a separate replay-derived graph projection. Direct structural materialization still has no protocol effect.

Under the optional semantic-history profile, the accepted target packages the
complete proposed state change as one immutable, frontend-neutral
`KnowledgeChangeSet`. Every lifecycle event references that exact identity.
The ledger, not the candidate store or materialized graph, is the state
authority; the accepted temporal graph is replay-derived. Initial governed
state is empty and its first knowledge arrives through retained genesis change
set data. Directly persisted or materialized structural candidates remain
non-governed and non-accepted as Malleus knowledge until admitted through that
history. An adopter may omit semantic history and keep the structural
guarantees in this document, but cannot then claim Malleus accepted-state
provenance or reconstruction.

### 3. A constructed graph does not swap registries in place

A current `KnowledgeGraph` keeps the `OntologyRegistry` it was constructed with;
it does not bind or mutate a complete effective-contract identity. Ledger epochs
belong to the accepted-temporal protocol design, not every standalone graph.

Additive changes may be compatible with old records, but compatibility is a
property to compute, not assume. Removing a type, making a field required,
narrowing a range, changing admission semantics, or changing an identifier can
require reinterpretation or refusal.

Current source beyond the released `0.13.3` package boundary contains a generic
`MigrationReceipt`. It can record an asserted old and new ontology-hash
transition, declared grade, reason, timestamp, chain link, and optional delta
digest. It does not carry a transform, reader, record mapping, or query rewrite.
`TOTAL` and `PARTIAL` are declared grades but currently make
`accepted_hashes()` accept prior hashes identically. Current source therefore
establishes neither total interpretation nor record-level indeterminacy.
`HARD_BREAK` alone stops backward hash acceptance.

An ontology-identity change does not universally create a ledger epoch. A
standalone structural `KnowledgeGraph` has no ledger epoch. In accepted design,
a new composition and ledger epoch are required when the change affects an
accepted-temporal semantic role. A source-only change preserving the effective-
contract identity does not require one.

Receipts do not rewrite retained records. Recon is their only current source
consumer; core `ProtocolLedger` does not consume them. OD-004 selected a hard
break for the new persisted wire with no receipt or replay bridge. A canonical
cross-contract `MigrationPlan`, including interpretation and impact, remains
Candidate work and may result in refusal.

### 4. Current admission uses one runtime registry

Current core constructs `OntologyRegistry` directly from LinkML-shaped YAML and
resolves declared imports while loading that registry. It does not execute
official LinkML semantics. `KnowledgeGraph` accepts exactly one registry. There
is no repository generator that emits a runtime registry source file.

Generated Python models, C++ types, schemas, or editor metadata may be useful
projections of a retained contract source, but they are optional projections,
not the accepted runtime contract boundary. Accepted future design pins LinkML
1.11.1 as the first-party frontend, compiles sources into frontend-neutral
contract facts, validates those facts, and builds the `EffectiveContract` used
at runtime.

### 5. The shipped graph API uses runtime string identifiers

Current `KnowledgeGraph` exposes these write families:

```python
create_entity(entity_type, entity_id, properties=None)
create_relation(relation_type, relation_id, source_id, target_id, properties=None)
create_signal(signal_type_class, signal_id, properties=None)
create_event(event_type_class, event_id, properties=None)
```

Every type identifier is a string checked through the bound registry. Required
properties are supplied during creation. Core has no typed-enum overload and no
`setProperty` method. An adopter may generate typed wrappers, but those wrappers
must preserve the same runtime gate and refusal semantics.

### 6. The bound runtime contract governs admission semantics

The current runtime uses `OntologyRegistry` for admission. The accepted
contract-compiler design replaces that syntax-bound path with a
frontend-neutral `EffectiveContract`; it is not implemented yet. A reloadable
`EffectiveContractArtifact` representation remains Candidate work.
Use the registry for runtime introspection rather than duplicating vocabulary
and endpoint rules in application code. Generated typed wrappers may improve
authoring safety, but they are not the current Malleus API or authority.

## Current implementation pattern

### Step 1: Define and load one ontology registry

Per `ONTOLOGY_PROTOCOL.md`, define domain types in LinkML-shaped YAML, resolve
imports explicitly, and construct one `OntologyRegistry` from the retained
source.

```python
registry = OntologyRegistry("path/to/domain.yaml")
kg = KnowledgeGraph(registry)
```

### Step 2: Send all writes through the registry-bound graph

Use `create_entity`, `create_relation`, `create_signal`, and `create_event`.
Each method validates the type, required properties, and any relation or signal
endpoint constraints before materializing the write.

### Step 3: Stage dependent records atomically

Use `stage_subgraph()` for an ordered multi-record candidate, then bind and
apply that candidate through the protocol path when epistemic acceptance is
required. Direct graph creation remains a structural operation only.

### Step 4: Resolve imports now; compose effective contracts later

Current `KnowledgeGraph` takes one `OntologyRegistry`. Base and extension YAML
are combined through registry import resolution, not by passing multiple
registries to the graph constructor.

For the accepted-temporal protocol, an incompatible semantic change requires a
new effective-contract composition and ledger epoch. Compatibility
classification, impact analysis, and an executable `MigrationPlan` remain
Candidate work, so a reader may have to refuse rather than cross the boundary.

## Reference implementations

- **Silk** (Rust): `GraphStore(instance_id, ontology_json())` — ontology as constructor param, write-time validation, quarantine for invalid ops in CRDT sync
- **TypeDB**: `define` block creates the schema, `insert` block creates instances — schema-first, insert fails if type undefined
- **Shelob**: `ONTOLOGY` dict in `store.py` → passed to Silk → all node/edge creation validated against it

## What this is NOT

- It is not OWL reasoning. OWL's Open World Assumption infers rather than rejects. We use Closed World.
- It is not merely a post-hoc validation report. SHACL can also be wired into
  store-specific commit gates; those are real prior art for write gating.
- It is not an unpinned runtime query to a mutable ontology service. Admission
  uses the exact registry or effective contract bound at construction.

Write gating itself is not unique to Malleus: TypeDB, Stardog's ICV guard mode,
GraphDB's on-commit SHACL, and TerminusDB all reject structurally nonconforming
commits.
The full formalism-by-formalism mapping, including what malleus can and cannot
claim against each, is in DELIMITATIONS.md.

---

*See also: ONTOLOGY_PROTOCOL.md for how to define the ontology. This document covers how to use it to construct a Knowledge Graph.*
