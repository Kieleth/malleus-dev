# Ontology-driven KG realization

Design status: accepted pillar, candidate protocol and completeness claim

Design revision: 8

Decision authority: author

Accepted decisions: `OKG-D000`, ontology-driven KG realization is a pillar;
`OKG-D012`, LinkML is the replaceable first-party contract frontend for v0;
`OKG-D013`, Small Shop Fulfilment is the selected primary vertical fixture;
contract compiler `AD-001`, `AD-003` through `AD-005`, `OD-001` through
`OD-008`, and `OD-010` through `OD-014`

Decision dates: 2026-08-17, 2026-08-24, 2026-08-25, 2026-08-26, 2026-08-27,
and 2026-08-28

Primary vertical-fixture decision: `OKG-D013` selects fixture object
`OKG-FX001`, **Small Shop Fulfilment**

Public ancestry base: `27ca54c33fe705827bc845e876cb6ff24293c8f0`.
This is an ancestry base only, not the tested implementation snapshot. The
intended release locator is `v0.11.0`; exact report, file, and checksum
identities are authoritative.

Canonical design graph: [`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl),
revision 23,
`sha256:4019f07fdebb5a9e10acd087ca5b940a578a79bdebf5112314720efcc498410a`

Protocol-design evidence cutoff: 2026-08-27

Running-fixture evidence cutoff: 2026-08-28

Private implementation-audit snapshot:
`sha256:9b62ed651e0b571a3301da559494d55fd9fe35f7790016a64cb163f43214f47a`

Private adoption-registry snapshot:
`sha256:4b373134bb7af272216cb788c28180e07a333530e5b6caf885f8243d33fd4d41`

Implementation status: the `GE-000` through `GE-020` GraphRecipe slice is
implemented research-locally. No public API or shipped GraphRecipe capability
is asserted here. This document records the evidence, boundary, dependency
graph, accepted GraphRecipe microdecisions, and candidate
protocol-completeness claim. Parallel roadmap, execution-bundle, and
paper/research worktrees remain outside this document.

## 1. Decision and scope

Ontology-driven KG realization is a Malleus pillar.

Graph Realization is an `OPTIONAL_PROFILE`. It defines deterministic
construction and structural admission boundaries without requiring Assent, a
protocol ledger, or an accepted temporal projection. Those mechanisms belong
to separately claimable profiles.

The pillar name keeps the ontology visible. The enclosed mechanism is the
`Graph Realization Protocol`, because “ontology-to-KG” would incorrectly imply
that the ontology alone supplies mappings, identities, recipes, and instances.

The pillar asks a precise question:

> Given an evolving effective domain contract, what additional declared inputs
> are required to deterministically derive a target graph schema, construct a
> candidate instance graph, diagnose every gap, pass structural admission, and
> reproduce or migrate the result? When governance profiles are selected, what
> additional inputs bind that result to an accepted projection?

This is an optional profile inside the protocol. Its compiler has no privileged
write path. It produces an exact construction plan whose operations pass
through the existing structural gate and staging mechanism. Monitoring,
epistemic decision, semantic history, and accepted projection are optional
governance extensions to that structural result.

The pillar, OTTR recipe formalism, and replaceable LinkML frontend boundary are
accepted. The exact contract object model, backend profiles, mapping artifacts,
ledger integration, and public API remain candidate design.

### 1.1 Primary vertical fixture: Small Shop Fulfilment

`OKG-D013` selects `OKG-FX001`, **Small Shop Fulfilment**, as the canonical
running domain for this pillar. Here, canonical means the first maintained
end-to-end example, not a normative domain model. `OKG-D013` is the accepted
decision; `OKG-FX001` is the fixture object it selects. The program uses this
fixture to keep one vertical explanation and regression thread coherent.
Independent fixtures remain separate controls and do not require Small Shop
vocabulary or topology. Replacing the primary program fixture requires a
superseding decision and dependency-impact analysis.

No fixture has protocol authority. A rule suggested by Small Shop remains
fixture-local until a structurally independent fixture exercises the same
boundary and independent justification and conformance evidence show that the
rule is domain-neutral. A vocabulary rename or another retailer scenario is
not structurally independent. Only then may the rule be proposed as a
`PROTOCOL_INVARIANT`; repetition does not promote it automatically.

`OKG-FX001` is synthetic and informed by Fahland's published example. It is not
copied source data. Its retail vocabulary remains fixture-local and does not
enter the Malleus protocol ontology. The decision changes no shipped capability
and does not claim that fixture bytes, a LinkML ontology, mappings, recipes, or
expected artifacts already exist. Exact fixture bytes and independently
authored oracles remain separate work. Existing `GE-000` through `GE-020`
fixtures remain frozen historical evidence; they are not retroactively rethemed
or regenerated. `OKG-D013` also does not override contract-compiler `OD-010` or
its current Entity-only relation endpoint boundary.

#### Literature ancestry and Malleus composition

The fixture takes its event fabric from Dirk Fahland's
[Event Knowledge Graph chapter](https://doi.org/10.1007/978-3-031-08848-3_9):
customer orders, supplier orders, physical items, actors, invoices, payments,
corrections, shipment activities, and later integration of warehouse events.
The chapter establishes the usefulness of representing one event against
multiple participating entities and retaining per-entity order. It does not
establish Malleus's contract compilation, evidence admission, epistemic
decision, protocol-ledger authority, bitemporal projection, or migration
semantics.

Three other systems contribute bounded techniques around that domain:

1. [SLOGERT](https://doi.org/10.1007/978-3-030-77385-4_38) contributes
   heterogeneous log-template extraction, semantic annotation, and OTTR-based
   graph construction.
2. [Blue Brain Nexus](https://doi.org/10.3233/SW-222974) contributes
   append-only resource evolution and replayed materialized projections.
3. [OntoLogX](https://doi.org/10.1002/aisy.202501381) contributes
   ontology-guided generation, explicit validation, targeted correction, and
   persist-only-valid gating.

Malleus composes those independently established pieces with identified source
closure, replaceable contract compilation, declared mapping and identity
contracts, atomic candidate identity, evidence checks, review and assent,
valid-time interpretation, protocol-ledger replay, and dependency-closed
evolution. Novelty, if established later, belongs to that composition and its
results, not to the retail pieces themselves.

#### Fixed conceptual closure

The minimal fixture contains:

| Kind | Fixed conceptual members |
|---|---|
| Actors | `R1` through `R5` |
| Customer orders | `O1`, `O2` |
| Supplier orders | `A`, `B`; `e4` records `B` as `1Y` and `e7` updates it to `2Y` |
| Product kinds | `X`, `Y` |
| Physical inventory units | `X1`, `X2`, `X3`, `Y1`, `Y2` |
| Invoices | `I1`, `I2`; `e9` records an update to `I2` without exposing the changed value |
| Payment | `P1`, settling `I1` and `I2` |
| Domain occurrences | create, place, receive, unpack, update, pack, ship, receive payment, and clear invoice |

The first retained source closure should expose heterogeneous but deterministic
inputs with roles equivalent to:

```text
orders.csv
supplier-orders.json
warehouse.jsonl
invoices.csv
payments.csv
```

Those filenames are explanatory until exact corpus bytes are independently
authored and bound. Their separation is normative: the realization design must
show how the same domain is composed from several sources rather than hiding
all population behind one already-clean graph file.

#### One occurrence carried to the current representation boundary

Use the warehouse's packing occurrence as the primary discriminating path:

```json
{
  "event_id": "e27",
  "activity": "PACK_SHIPMENT",
  "time": "07-05 17:00",
  "actor": "R4",
  "order": "O1",
  "items": ["X1", "X2", "Y1"]
}
```

This JSON is an explanatory source shape, not an accepted public wire and not a
claim that the occurrence happened. The paper supplies no year or timezone for
this value. An executable fixture must separately declare its calendar year,
source format, timezone database and version, and refusal behavior for ambiguous
or nonexistent local times. A normalized timestamp is fixture-derived, not a
paper claim. The occurrence should travel through retained source,
transformation, mapping, and identity handling until the current `OD-010`
endpoint boundary returns a typed construction gap. The self-contained
`O1` plus `X1` topology below is the first green path. The `P1` settlement is
the second green path after its invoice dependencies exist. The layers must
remain distinct:

| Object | Concrete meaning for `e27` | What it is not |
|---|---|---|
| Source occurrence | One retained warehouse record says `R4` packed `O1` using `X1`, `X2`, and `Y1` at a stated time | Accepted knowledge |
| Semantic proposal | The desired identified patch would interpret the record under exact mapping, transformation, identity, recipe, evidence, and contract identities; current construction stops before emitting it as stageable operations | A ledger event or accepted patch |
| Protocol event | A future governed run can record the source, typed gap, review, or decision in transaction order; it cannot record an accepted application for an unrepresentable candidate | The warehouse occurrence itself |
| Accepted temporal KG | The graph remains unchanged when the typed construction gap blocks the candidate | A lossy property encoding of the missing event correlations |

The protocol ledger and accepted KG therefore encode different orderings. The
ledger orders Malleus transitions. The KG represents accepted domain meaning,
including domain-valid time, identity, relations, provenance, and supersession.

#### What controls each boundary

| Concern | `OKG-FX001` example | Authority |
|---|---|---|
| Human authoring syntax | `SalesOrder`, `InventoryUnit`, fields, constraints, and relation signatures | LinkML v0 frontend |
| Governed contract meaning | Frontend-neutral facts and their effective constraints | `EffectiveContract` |
| Observed bytes | The exact retained `warehouse.jsonl` record | Source artifact identity |
| Source interpretation | `order` maps to the order symbol and `items` maps to physical-unit symbols | `SourceMappingContract` |
| Normalization | Timestamp, quantity, money, and code normalization | `TransformationContract` plus named implementation |
| Stable ABox identity | `O1` becomes an order identity while `X` and `X1` remain product-kind and physical-unit identities | `IdentityResolutionPolicy` |
| Reusable topology | Required records, relations, properties, and construction dependencies | OTTR `GraphRecipe` |
| Construction intent | Ordered existing `ProposedOperation` values | GraphRecipe assembler |
| Structural legality | Types, fields, endpoints, references, and atomic staging | Effective contract plus Malleus runtime |
| Evidential acceptability | Required warehouse, invoice, or payment evidence and conflict handling | Named evidence and epistemic policy |
| Transaction order and replay | Proposal, check, decision, and application history | `ProtocolLedger` |
| Read representation | Accepted NetworkX view now; additional conformant projections later | Projector plus `GraphBackendProfile` |

LinkML is the replaceable source language. Contracts are identified rule and
policy data. Named code compiles or enforces those contracts. OTTR expands only
finite topology. None of those parts may silently assume the responsibilities
of another.

#### Deterministic compiler and optional proposal producer

The accepted compiler boundary is a deterministic partial function. Exact,
closed inputs produce exact compiled artifacts or an exact typed refusal.
Producer identity is irrelevant: the compiler applies the same rules to the
same bytes whether a person, a program, or an optional Malleus skill authored
them. It does not infer what an incomplete ontology probably meant.

An optional Malleus ontology-builder/corrector skill may propose exact ontology
or patch bytes from an existing ontology or from retained project evidence when
no ontology exists. That skill is outside the trusted compiler. Its output is a
content-addressed proposal that enters ordinary evidence, review, and decision
handling. Only accepted exact bytes become compiler input. The compiler never
calls the skill, and replay uses retained bytes and recorded artifacts without
calling it again.

#### GREEN 1: self-contained order and physical unit

The first positive topology creates order `O1`, distinct physical item `X1`,
and one fixture-defined `OrderContainsUnit` relation in an empty graph base.
Fahland's example supports the `O1` and `X1` association through the packing
occurrence. The direct predicate name, direction, and any standalone allocation
source record are fixture decisions. They must be declared and evidenced rather
than attributed to the paper or inferred from the earlier create-order event.
This derived Entity-to-Entity view does not satisfy or erase the separate RED
obligation to represent `e27` and its correlations. One recipe invocation can
emit:

```text
Record(shop:member/order-o1,
       mgrp:CreateEntity,
       shop:SalesOrder,
       "order:O1")
Property(shop:member/order-o1,
         shop:orderNumber,
         "O1")

Record(shop:member/unit-x1,
       mgrp:CreateEntity,
       shop:InventoryUnit,
       "unit:X1")
Property(shop:member/unit-x1,
         shop:productCode,
         "X")

Record(shop:member/contains-x1,
       mgrp:CreateRelation,
       shop:OrderContainsUnit,
       "relation:O1:X1")
RelationSource(shop:member/contains-x1, "order:O1")
RelationTarget(shop:member/contains-x1, "unit:X1")
DependsOn(shop:member/contains-x1, shop:member/order-o1)
DependsOn(shop:member/contains-x1, shop:member/unit-x1)
```

The qualified `member` is a construction-local handle. The string `record_id`
is the ABox identity that survives in the graph. `DependsOn` determines safe
construction order; it is not a domain relation. The assembler must lower the
complete fact set to this ordered intent:

```text
1. CREATE_ENTITY SalesOrder order:O1 {"order_number":"O1"}
2. CREATE_ENTITY InventoryUnit unit:X1 {"product_code":"X"}
3. CREATE_RELATION OrderContainsUnit relation:O1:X1
   source=order:O1 target=unit:X1
```

#### GREEN 2: payment settlement against an existing base

The second positive topology uses the paper's payment `P1`, which settles
invoices `I1` and `I2`. Both invoices must already exist in the verified graph
base. The first fixture recipe is fixed at two invoice arguments. It does not
claim generic collection expansion, arbitrary fan-out, or cardinality
enforcement. One invocation can emit:

```text
Record(shop:member/payment-p1,
       mgrp:CreateEntity,
       shop:Payment,
       "payment:P1")
Property(shop:member/payment-p1,
         shop:paymentNumber,
         "P1")

Record(shop:member/settles-i1,
       mgrp:CreateRelation,
       shop:PaymentSettlesInvoiceRelation,
       "relation:P1:I1")
RelationSource(shop:member/settles-i1, "payment:P1")
RelationTarget(shop:member/settles-i1, "invoice:I1")
DependsOn(shop:member/settles-i1, shop:member/payment-p1)

Record(shop:member/settles-i2,
       mgrp:CreateRelation,
       shop:PaymentSettlesInvoiceRelation,
       "relation:P1:I2")
RelationSource(shop:member/settles-i2, "payment:P1")
RelationTarget(shop:member/settles-i2, "invoice:I2")
DependsOn(shop:member/settles-i2, shop:member/payment-p1)
```

The assembler must lower the complete fact set to this ordered intent:

```text
1. CREATE_ENTITY Payment payment:P1 {"payment_number":"P1"}
2. CREATE_RELATION PaymentSettlesInvoiceRelation relation:P1:I1
   source=payment:P1 target=invoice:I1
3. CREATE_RELATION PaymentSettlesInvoiceRelation relation:P1:I2
   source=payment:P1 target=invoice:I2
```

The direct settlement predicate and its direction are fixture-derived from the
published `e30` co-occurrence of `P1`, `I1`, and `I2`. They are not native EKG
correlation edges. All names above remain fixture-local explanatory vocabulary
until independent source and oracle work fixes exact qualified symbols. They
are not public Malleus identifiers.

#### GREEN 3: actual corrections without identity collapse

The temporal thread uses the corrections present in the paper:

```text
e4  Supplier order B records 1 unit of product Y
e7  Supplier order B is updated to 2 units of product Y
e9  Invoice I2 is updated
```

An executable fixture must define the versioned state or claim identity that
`e7` supersedes. The paper does not expose the changed invoice value at `e9`, so
the fixture must either retain only the occurrence of an update or independently
author and identify the corrected invoice details. It may not invent those
details as a paper claim.

`Y1` and `Y2` are two distinct physical items. Both arrive in `e19`, are unpacked
separately in `e20` and `e21`, and are later packed with different orders. One
must never supersede the other. If an allocation relation were corrected in a
future synthetic case, the relation version would change while both item
identities remained intact. GraphRecipe emits `ProposedOperation` values only;
a separate temporal binding supplies valid time, supersession, acceptance, and
ledger application.

#### Concrete phase map

| Phase | `OKG-FX001` object |
|---|---|
| 0. Effective contract | Compile the exact accepted shop ontology sources into one reloadable contract; a root `instances` field must refuse rather than become population or disappear |
| 1. Logical contract | Derive the legal order, unit, invoice, payment, event, and relation record roles and constraints |
| 2. Backend projection | State exactly what the NetworkX gate enforces and what remains an external admission check |
| 3. Recipes | Compile self-contained `OrderContainsUnit`, fixed-arity `PaymentSettlementTwoInvoices`, correction-state, and packing-event topology under the narrowed OTTR profile |
| 4. Population policy | Bind each source path, transformation, identity rule, recipe selection, evidence requirement, and collision behavior |
| 5. Construction plan | Produce one content-addressed operation-dependency plan with ordered operations and derivation traces for a selected source closure |
| 6. Close and verify | Bind the plan, contract, source/evidence closure, base ledger/state, valid time, supersession, and operations into one immutable `KnowledgeChangeSet`; refuse the whole change set on a missing unit, invalid endpoint, identity collision, unsupported event correlation, or failed evidence check |
| 7. Decide and project | Apply only a change-set-bound `ACCEPT` through ledger replay; every other decision leaves the accepted graph unchanged |
| 8. Attest | Bind source, contract, mapping, identity, recipe, implementation, plans, change set, checks, decision, heads, and resulting graph identity |
| 9. Evolve | Supersede the declared state of supplier order `B` at `e7`, retain the bounded `I2` update at `e9`, then test an ontology revision that introduces first-class `Shipment` records and partial shipments |

#### Required RED boundaries

The fixture is valuable because it exposes present limits rather than adapting
the story to whatever the code already happens to support:

1. **Ontology is not population.** The shop ontology alone must produce zero
   orders, items, invoices, payments, events, and relations.
2. **Unknown source-language fields refuse.** A root `instances` member and any
   arbitrary unlisted root member must refuse the entire contract compilation.
3. **The upper ABox seam is absent.** No shipped frontend-neutral source
   occurrence, mapping, identity, recipe-invocation, or semantic graph-patch API
   currently produces `ProposedOperation` values.
4. **Event correlation is not currently representable as an ordinary Malleus
   relation.** The accepted `OD-010` profile permits Entity-only relation
   endpoints, while Fahland's event graph correlates `e27` to an order, several
   units, and, when the actor layer is included, `R4`, and relates events through
   per-entity order. The first
   experiment must expose this mismatch and refuse or report a typed gap. It may
   not invent an implicit property edge or broaden endpoint semantics.
5. **Semantic and source identity differ.** A description-only ontology edit
   changes exact source attestation while preserving effective semantic facts.
   A required-field, range, identity, or used-prefix change affects the
   appropriate semantic contract identity.
6. **Evolution is dependency-closed.** Introducing first-class `Shipment`
   records must identify affected ontology facts, mappings, recipes, plans,
   existing ABox records, projections, and readers before migration is accepted.
7. **Physical identity is not revision identity.** `Y1` and `Y2` are distinct
   items. No mapping, recipe, temporal write, or repair may model either as a
   version, alias, or superseding record of the other.

Physics and chemistry remain desirable independent stress domains, especially
for units, uncertainty, instrument observations, competing models, and ontology
evolution. They follow this baseline. They do not delay or replace it.

## 2. “KG structure” names four different things

The phrase must not hide four separate outputs:

| Layer | Exact meaning | `OKG-FX001` example | What the ontology can determine | Controlling input |
|---|---|---|---|---|
| Logical graph contract | Permitted record kinds, inheritance, properties, relation signatures, and constraints | `SalesOrder`, `InventoryUnit`, and a legal Entity-to-Entity `OrderContainsUnit` signature; later `PaymentSettlesInvoiceRelation` | Mostly derivable from an effective contract | `EffectiveContract` plus the logical-contract compiler |
| Backend graph schema | Labels or types, fields, endpoint constraints, indexes, and other target-specific declarations | NetworkX node attributes for `O1` and `X1`, and one keyed relation record between them | Partly derivable after a backend capability profile is supplied | `GraphBackendProfile` plus projection code |
| Reusable graph topology | A parameterized pattern of records and relations that must occur together | First `OrderWithUnit(O1, X1)`; then fixed-arity `PaymentSettlementTwoInvoices(P1, I1, I2)` after its base exists | Constrained by the ontology, but selected and parameterized by a recipe | OTTR `GraphRecipe` plus invocation |
| Instance population | Concrete identities, values, relations, provenance, and source evidence | Retained fixture sources identify `O1` and `X1` and explicitly support the fixture-derived relation; later sources identify `P1`, `I1`, and `I2` | Requires source mappings, identity policy, transformations, and source artifacts | Source closure plus mapping, transformation, identity, conflict, and evidence contracts |

An optional fifth projection represents the ontology itself as graph data. That
is useful for introspection, but it is not the domain instance graph and does
not replace any layer above.

The ontology therefore supplies more than documentation, but less than a
populated KG. A compiler that pretends otherwise must guess. Malleus should
make each missing choice an addressable contract or a typed gap.

## 3. Current implemented boundary

The shipped Python path is:

```text
LinkML-shaped YAML
  -> OntologyRegistry
  -> resolved effective constraints
  -> KnowledgeGraph structural admission
  -> NetworkX MultiDiGraph
```

`OntologyRegistry` already resolves local imports, inheritance, mixins, slot
use, enums, scalar aliases, and relation signatures. Its public introspection
can enumerate resolved types, type definitions, effective slots, enums, and
subtype relationships. `KnowledgeGraph` requires a registry, validates every
create operation, and refuses invalid writes before they materialize.
`ProposedOperation` and `stage_subgraph()` can already represent and validate
an ordered candidate construction without changing the base graph.

These are load-bearing implemented pieces. They do not yet form an
ontology-driven realization protocol. The public package has no named logical
graph contract, backend profile, schema projection, source mapping, identity
resolution policy, reusable graph recipe, construction plan, coverage report,
or realization attestation. It also has no typed generated Python writer API.
The generated-registry and typed-API material in
`docs/KNOWLEDGE_GRAPH_PROTOCOL.md` is design lineage where no equivalent Python
implementation exists.

A separate research-local GraphRecipe runner now implements the frozen
`GE-000` through `GE-020` slice. It derives the narrowed logical contract,
expands and assembles the exercised recipe subset, lowers exact proposed
operations, stages and materializes through existing Malleus seams, and emits
bound conformance receipts. This is experiment evidence, not a packaged
runtime module. It does not change the public boundary described above.

Generated LinkML artifacts are optional projections. The graph does not consume
them today. An adopter that only needs the runtime gate should not need to run
LinkML generation. The intended contract-kernel boundary is a compiled
`EffectiveContractArtifact` that can be consumed without LinkML at runtime.

## 4. Derived, supplied, and observed inputs

The realization protocol must label the origin of every material decision.

### 4.1 Derived from the effective contract

These outputs can be compiled without domain guessing:

1. Concrete and abstract type inventory.
2. Entity, relation, signal, and event role candidates.
3. Inheritance and mixin closure.
4. Effective property constraints.
5. Relation endpoint signatures and reference targets.
6. The structurally legal operation repertoire.
7. Target-neutral validation schemas for construction operations.
8. A dependency graph from contract facts to generated artifacts.

Role classification is only derivable when the effective contract states it.
The current Malleus root hierarchy supplies that information. A different
metamodel may need an explicit role binding.

### 4.2 Supplied as separate contracts

These choices cannot be inferred safely from the ontology alone:

1. Backend capabilities and physical layout preferences.
2. Source field or path mappings to ontology symbols.
3. Unit, normalization, and value transformation rules.
4. Stable identity generation, equivalence, merge, and collision policy.
5. Which reusable graph recipe to instantiate.
6. Recipe parameters and optional branches.
7. Source precedence and conflict policy.
8. Evidence requirements and epistemic acceptance policy.
9. Evolution disposition for affected existing records.
10. Realization mode: materialized, virtual, or hybrid.

Defaults are permitted only when the governing profile declares them. Missing
required data never receives an implicit default.

### 4.3 Observed and retained

Execution supplies facts that cannot be declared in advance:

1. Exact source artifact identities and bytes or caller-declared boundaries.
2. Exact compiler, adapter, transformation, and producer identities.
3. Generated target artifacts and their digests.
4. Accepted and refused construction operations.
5. Typed gaps and violations.
6. Monitor results and evidence audits.
7. The resulting structural graph digest and accepted graph coordinates.

This three-way split is a core invariant. A generated result must never be
recorded as though it were source-declared, and a reviewer or producer choice
must never be recorded as ontology-derived.

## 5. Candidate protocol

The shortest complete formulation is:

```text
LogicalGraphContract
  = derive(EffectiveContract)

GraphSchemaProjection
  = project(LogicalGraphContract, GraphBackendProfile)

PopulationPlan
  = compose(
      GraphRecipeSet,
      SourceMappingSet,
      TransformationContract,
      IdentityResolutionPolicy,
      SourceAndConflictPolicy,
    )

GraphConstructionPlan
  = compile(
      LogicalGraphContract,
      GraphSchemaProjection,
      PopulationPlan,
      SourceArtifacts,
      RealizationMode,
      ConstructionProfile,
    )

KnowledgeChangeSet
  = close_change(
      EffectiveContract,
      SourceAndEvidenceClosure,
      BaseLedgerAndAcceptedState,
      GraphConstructionPlan,
      OperationDependencyPlan,
      ValidTimeAndSupersession,
    )

CandidateSubgraph
  = stage(KnowledgeChangeSet.ordered_operations)

StructuralGraphRealization
  = structurally_materialize(CandidateSubgraph)

GovernedAcceptedRealization
  = record_and_project(
      KnowledgeChangeSet,
      EpistemicPolicy,
      ProtocolLedger,
    )
```

Every function above returns either a content-addressed result or typed gaps.
No phase silently drops a source field, ontology fact, recipe member, proposed
operation, or target capability mismatch.

`StructuralGraphRealization` is the profile's sufficient structural output. It
claims contract-bound construction, not truth or acceptance, and remains
non-governed and non-accepted even when persisted. `GovernedAcceptedRealization`
exists only when the adopter also selects the Assent and semantic-history
profiles. It is derived by replay after ledger admission of the exact
`KnowledgeChangeSet`; no structural materializer writes it directly.

### Phase 0: Resolve the effective contract

Compile retained source bytes through an exact frontend, resolver, support
profile, metamodel, canonicalization profile, symbol policy, and normative
admission profile. This is the contract-kernel dependency, not a second
ontology parser invented for graph construction.

Output: one exact `EffectiveContract` and reloadable
`EffectiveContractArtifact`.

### Phase 1: Derive the logical graph contract

Compile the target-neutral meaning required to construct graphs:

1. Record roles and abstractness.
2. Effective fields and value constraints.
3. Reference and relation endpoint signatures.
4. Identity-bearing declarations, if present.
5. Legal construction operation kinds.
6. Contract-fact dependencies for every derived item.

Output: `LogicalGraphContract` plus `LogicalCoverageReport`.

### Phase 2: Project a backend graph schema

Bind a `GraphBackendProfile` that declares which semantics the target can
enforce. Compile target types, properties, endpoint restrictions, indexes only
when declared, and adapter-facing operation schemas. Each source semantic is
classified as:

```text
DIRECT
APPROXIMATED
EXTERNAL_GATE
UNSUPPORTED
NOT_APPLICABLE
```

`UNSUPPORTED` blocks unless an explicit profile routes that semantic to a
named external gate. Approximation must state the semantic loss.

Output: `GraphSchemaProjection`, target artifact, and
`ProjectionCoverageReport`.

An in-memory or otherwise dynamic backend may emit no external schema artifact.
It still produces a `GraphSchemaProjection` stating that admission remains in
the named runtime gate, plus a coverage report. The projection phase is not
silently omitted.

### Phase 3: Compile reusable graph recipes

A `GraphRecipe` declares a named, parameterized topology:

1. Parameter types and semantic roles.
2. Required and optional record members.
3. Required relations and endpoint bindings.
4. Construction dependencies and deterministic ordering.
5. Presence conditions represented by explicit add-on recipe invocation.
6. Expected postconditions and named readers.

Recipe validity is checked against the logical graph contract before any
instance is planned. Recipe instantiation has a digest over the recipe,
parameters, logical contract, and expansion profile.

The author accepted `OKG-D001` on 2026-08-17: use stOTTR 0.1.4 as the only
authored GraphRecipe representation under the restrictive
[Malleus GraphRecipe Profile v0](GRAPH_RECIPE_OTTR_PROFILE.md). Do not create a
native recipe DSL, accept multiple recipe frontends, or fork OTTR.

The profile narrows GraphRecipe to finite topology expansion. It terminates in
a closed Malleus construction-fact vocabulary, then assembles an explicit
member-dependency graph and lowers it deterministically to existing
`ProposedOperation` values. Mapping, transformation, identity, collision,
provenance, atomic planning, admission, and evolution remain outside OTTR and
inside their named Malleus contracts.

Output: `CompiledGraphRecipe` and `RecipeCoverageReport`.

### Phase 4: Bind mappings, transformations, and identity

A `SourceMappingContract` binds exact source shapes and paths to ontology
symbols. An `IdentityResolutionPolicy` binds key construction, namespaces,
equivalence, merge behavior, and collisions. A `TransformationContract` binds
normalization, units, coercion, and exact implementation identity.

Every required recipe parameter and required target field must have one of:

1. An explicit source mapping.
2. An explicit recipe parameter.
3. A contract-declared derived value.
4. A profile-declared default.
5. A typed construction gap.

The validated bindings compose one `PopulationPlan`. It states source
precedence, conflict behavior, missing-target behavior, and which recipe each
source record may invoke. It is distinct from the later execution plan because
it contains reusable policy rather than one run's exact source values and
operations.

Output: validated mapping, transformation, and identity bindings plus one
`PopulationPlan`.

### Phase 5: Compile the construction plan

The compiler resolves dependencies and emits ordered `ProposedOperation`
values for a materialized realization. `RealizationMode` is separately
identified as `MATERIALIZED`, `VIRTUAL`, or `HYBRID`. The first implementation
slice supports only `MATERIALIZED`; the other modes remain explicit rather than
being misreported as materialized graphs. The plan binds:

1. Effective and logical contract identities.
2. Backend profile and schema projection identities.
3. Recipe and recipe-instance identities.
4. Mapping, transformation, identity, and source identities.
5. Population-plan and realization-mode identities.
6. Compiler and adapter implementation identities.
7. Detached base-graph digest for structural work, or base ledger head and
   accepted-state digest for a governed change set, plus intended scope.
8. Ordered operations and their derivation traces.
9. All gaps, exclusions, and warnings.

Deterministic inputs must produce identical canonical plans and digests.
External proposal producers may supply values, but each attempt and exact
output is retained as an observed input before plan compilation. The compiler
never invokes those producers.

Output: `GraphConstructionPlan` or a blocked result with typed gaps.

### Research-local consumer handoff

The Small Shop vertical must publish the neutral seam it exercises, not a
fixture-shaped API. The research-local handoff retains planning inputs but
culminates in two canonical data values:

1. `KnowledgeChangeSet`, binding the effective contract; source and evidence
   closure; base ledger head and accepted-state digest; ordered primitive
   operations; valid time; supersession; operation-local dependencies; and its
   canonical digest.
2. `CandidateValidationReceipt`, binding that change set, its retained planning
   inputs, executor identity, ordered typed results or refusals, and result or
   output digest.

`PopulationPlan`, `GraphConstructionPlan`, and `OperationDependencyPlan` remain
retained derivation inputs. They are not accepted state, domain identity, or an
alternative consumer authority. These shapes are frontend-neutral and contain
no Small Shop or Malleus Code term. Small Shop is their first conformance
fixture. The receipt is not a migration receipt, protocol-ledger event,
accepted-KG identity, or future projection-closure record. This research
boundary makes no stable public API claim; open graph-realization promotion
decisions still apply.

### Phase 6: Stage and verify

The change set's ordered operations are converted to the existing
`CandidateSubgraph` path. Structural
refusals remain refusals. The compiler cannot filter or rewrite rejected
operations after observing the gate. A new plan revision must preserve the
failed attempt and its diagnostics.

The structural branch verifies admission plus the exercised backend projection
semantics. Logical, temporal, conflict, uncertainty, evidence, and authority
monitors are selected only when their optional profiles and exact policies are
claimed.

Output: staged candidate, operations, structural diagnostics, and, when
selected, profile-specific monitor records and typed witnesses.

### Phase 7: Materialize structurally, optionally govern

Structural materialization produces a `StructuralGraphRealization` and makes no
epistemic claim. If the Assent and semantic-history profiles are also selected,
a change-set-bound `ACCEPT` may carry the atomic application in the same ledger
event. The projector then derives `GovernedAcceptedRealization` by replay.
`REJECT`, `DEFER`, and `CONTEST` leave accepted domain state unchanged.

Output: a materialized structural snapshot, or, under the optional governance
profiles, an accepted temporal graph version with exact protocol heads.

### Phase 8: Attest the realization

A `GraphRealizationAttestation` binds the complete derivation chain and result:

```text
effective contract
logical graph contract
backend profile and projection
recipe instances
mappings, transformations, and identity policy
source artifacts
construction plan
staging and monitor results
decision and materialization heads
resulting graph identity
execution identity
```

Decision and protocol-head fields are present only for a
`GovernedAcceptedRealization`. A structural attestation binds the construction
and structural result without inventing ledger coordinates.

The attestation proves replay of the recorded construction under the declared
implementation boundary. It does not prove source truth, producer honesty, or
external artifact authenticity.

### Phase 9: Propagate evolution

An effective-contract change triggers dependency-closed impact analysis. The
result classifies every dependent artifact and graph record into an explicit
outcome:

```text
UNCHANGED
REGENERATE
REVALIDATE
REPLAN
MIGRATE
SUPERSEDE
RETRACT
BLOCKED
```

Annotation-only changes may leave the effective contract unchanged. Additive
contract changes may only require regeneration and revalidation. A rename,
required-field addition, range narrowing, role change, relation-signature
change, or identity-policy change can invalidate mappings, recipes, plans, and
existing instances. The change result must identify those dependents before a
new graph version is accepted.

Migration creates a new realization with lineage. It does not rewrite old
transaction history.

## 6. Dependency graph carried by this document

The tuples below are the machine-readable design account. They reuse the
foundation graph vocabulary. They do not select RDF as a public wire format.

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .
@prefix okg: <https://malleus.dev/ontology-kg-realization/> .
@prefix cc: <https://malleus.dev/contract-compiler/> .

okg:OntologyDrivenKGRealization rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-FX001 rdf:type mfg:DesignObject ;
    mfg:dependsOn cc:OD-010 ;
    mfg:governedBy okg:SmallShopFixtureOnlyBoundary ;
    mfg:governedBy okg:FrozenGE000ThroughGE020Boundary ;
    mfg:governedBy okg:CorrectedSmallShopExperimentLadderBoundary ;
    mfg:governedBy okg:DistinctPhysicalItemsNeverSupersedeBoundary ;
    mfg:status mfg:AcceptedDesign .

okg:SmallShopFixtureOnlyBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

okg:FrozenGE000ThroughGE020Boundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

okg:CorrectedSmallShopExperimentLadderBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

okg:DistinctPhysicalItemsNeverSupersedeBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-D013 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-28" ;
    mfg:selects okg:OKG-FX001 ;
    mfg:status mfg:AcceptedDesign .

okg:OntologyDrivenKGRealization mfg:governedBy okg:OKG-D013 .

okg:DeterministicCompilerOptionalProposalProducerArchitecture
    rdf:type mfg:DesignObject ;
    mfg:binds okg:DeterministicCompilerExactOutputOrTypedRefusalBoundary ;
    mfg:binds okg:OntologyBuilderCorrectorOutsideTrustedCompilerBoundary ;
    mfg:binds okg:OntologyBuilderCorrectorProtocolReviewBoundary ;
    mfg:binds okg:ReplayNeverCallsOntologyBuilderCorrectorBoundary ;
    mfg:status mfg:AcceptedDesign .

okg:DeterministicCompilerExactOutputOrTypedRefusalBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

okg:OntologyBuilderCorrectorOutsideTrustedCompilerBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

okg:OntologyBuilderCorrectorProtocolReviewBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

okg:ReplayNeverCallsOntologyBuilderCorrectorBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

okg:OntologyDrivenKGRealization
    mfg:governedBy okg:DeterministicCompilerOptionalProposalProducerArchitecture .

okg:LogicalGraphContract rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:derivedFrom mfg:EffectiveContract ;
    mfg:status mfg:Candidate .

okg:LogicalCoverageReport rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:LogicalGraphContract mfg:produces okg:LogicalCoverageReport .

okg:GraphBackendProfile rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:GraphSchemaProjection rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:SchemaProjection ;
    mfg:derivedFrom okg:LogicalGraphContract ;
    mfg:governedBy okg:GraphBackendProfile ;
    mfg:produces okg:ProjectionCoverageReport ;
    mfg:status mfg:Candidate .

okg:ProjectionCoverageReport rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:GraphRecipe rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:interpretedUnder okg:LogicalGraphContract ;
    mfg:status mfg:Candidate .

okg:MalleusGraphRecipeProfileV0 rdf:type mfg:DesignObject ;
    mfg:dependsOn okg:OTTRFramework2024 ;
    mfg:governs okg:GraphRecipe ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-D001 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:selects okg:MalleusGraphRecipeProfileV0 ;
    mfg:rejects okg:NativeMalleusRecipeLanguage ;
    mfg:rejects okg:MultipleRecipeFrontendsV0 ;
    mfg:rejects okg:OTTRFork ;
    mfg:status mfg:AcceptedDesign .

okg:CompiledGraphRecipe rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:derivedFrom okg:GraphRecipe ;
    mfg:derivedFrom okg:LogicalGraphContract ;
    mfg:produces okg:RecipeCoverageReport ;
    mfg:status mfg:Candidate .

okg:RecipeCoverageReport rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:SourceMappingContract rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:interpretedUnder okg:LogicalGraphContract ;
    mfg:status mfg:Candidate .

okg:TransformationContract rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:IdentityResolutionPolicy rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:SourceConflictPolicy rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:PopulationPlan rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:composedOf okg:CompiledGraphRecipe ;
    mfg:composedOf okg:SourceMappingContract ;
    mfg:composedOf okg:TransformationContract ;
    mfg:composedOf okg:IdentityResolutionPolicy ;
    mfg:composedOf okg:SourceConflictPolicy ;
    mfg:status mfg:Candidate .

okg:RealizationMode rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:ConstructionProfile rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:GraphConstructionPlan rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:dependsOn okg:LogicalGraphContract ;
    mfg:dependsOn okg:GraphSchemaProjection ;
    mfg:dependsOn okg:PopulationPlan ;
    mfg:dependsOn okg:RealizationMode ;
    mfg:governedBy okg:ConstructionProfile ;
    mfg:produces okg:ProposedOperationSequence ;
    mfg:produces okg:ConstructionGapSet ;
    mfg:status mfg:Candidate .

okg:ProposedOperationSequence rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Partial .

okg:ConstructionGapSet rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:GraphConstructionPlan mfg:compiledBy okg:ConstructionCompiler .

okg:ConstructionCompiler rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

okg:StagedRealizationCandidate rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:derivedFrom okg:GraphConstructionPlan ;
    mfg:validatedBy mfg:CurrentKnowledgeGraph ;
    mfg:status mfg:Partial .

okg:GraphRealization rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:GraphVersion ;
    mfg:derivedFrom okg:StagedRealizationCandidate ;
    mfg:binds mfg:PersistedStructuralCandidateNonGovernedBoundary ;
    mfg:status mfg:Partial .

okg:GraphRealizationAttestation rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:binds okg:GraphConstructionPlan ;
    mfg:binds okg:GraphRealization ;
    mfg:binds mfg:ExecutionIdentity ;
    mfg:status mfg:Candidate .

okg:ConstructionEvolutionImpact rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:dependsOn mfg:ContractEvolution ;
    mfg:dependsOn okg:OntologyDrivenKGRealization ;
    mfg:status mfg:Candidate .

okg:NoPrivilegedWriter rdf:type mfg:Invariant ;
    mfg:status mfg:AcceptedDesign .

okg:NoSilentSemanticLoss rdf:type mfg:Invariant ;
    mfg:status mfg:AcceptedDesign .

okg:DerivedSuppliedObservedSeparation rdf:type mfg:Invariant ;
    mfg:status mfg:AcceptedDesign .

okg:DependencyClosedEvolution rdf:type mfg:Invariant ;
    mfg:status mfg:Candidate .

okg:LogicalDerivationConformance rdf:type mfg:TestObligation ;
    mfg:tests okg:LogicalGraphContract ;
    mfg:status mfg:Candidate .

okg:ProjectionRuntimeBite rdf:type mfg:TestObligation ;
    mfg:tests okg:GraphSchemaProjection ;
    mfg:tests okg:ProjectionCoverageReport ;
    mfg:status mfg:Candidate .

okg:PopulationCompleteness rdf:type mfg:TestObligation ;
    mfg:tests okg:PopulationPlan ;
    mfg:tests okg:ConstructionGapSet ;
    mfg:status mfg:Candidate .

okg:PlanDeterminism rdf:type mfg:TestObligation ;
    mfg:tests okg:GraphConstructionPlan ;
    mfg:status mfg:Candidate .

okg:NoBypassConformance rdf:type mfg:TestObligation ;
    mfg:tests okg:NoPrivilegedWriter ;
    mfg:tests okg:StagedRealizationCandidate ;
    mfg:status mfg:Candidate .

okg:EvolutionImpactClosure rdf:type mfg:TestObligation ;
    mfg:tests okg:ConstructionEvolutionImpact ;
    mfg:status mfg:Candidate .

okg:FullReconstructionEquivalence rdf:type mfg:TestObligation ;
    mfg:tests okg:IncrementalMaintenanceProfile ;
    mfg:status mfg:Candidate .
```

`ProposedOperationSequence`, `StagedRealizationCandidate`, and
`GraphRealization` are marked partial because current operations, staging, and
materialization supply mechanics but do not bind the complete realization
lineage described here.

## 7. Required invariants

1. Every contract fact that can affect graph construction has one derivation
   edge into the logical graph contract or an explicit exclusion.
2. Every concrete class has one declared construction role or a typed
   `UNCLASSIFIED_TYPE` gap.
3. Every concrete relation has a resolved endpoint signature.
4. Every target constraint is traced to a source contract fact and target
   profile rule.
5. Every unsupported target semantic is visible in the coverage report.
6. Every required recipe parameter and field has an explicit value origin.
7. Unknown source fields, target fields, and mapping symbols reject. They are
   never filtered.
8. Identity generation is exact, versioned, collision-aware, and separate from
   ontology symbol identity.
9. Every planned operation records its recipe, mapping, source, and identity
   derivation.
10. The construction compiler cannot write a graph directly.
11. Every planned operation is staged through the same admission contract as
    hand-authored operations.
12. Every rejection remains evidence for the next plan revision.
13. Every writer and generated artifact has a named reader or consumer.
14. Same deterministic inputs produce the same plan and digest.
15. Contract evolution traverses all projections, recipes, mappings, plans,
    attestations, and affected graph records before migration can succeed.
16. A fixture-derived rule remains local until a structurally independent
    fixture and independent justification support the same boundary.

Minimum typed gap codes are:

```text
UNCLASSIFIED_TYPE
UNSUPPORTED_CONSTRAINT
TARGET_CAPABILITY_GAP
UNMAPPED_REQUIRED_FIELD
UNBOUND_RECIPE_PARAMETER
UNKNOWN_MAPPING_SYMBOL
IDENTITY_POLICY_MISSING
IDENTITY_COLLISION
AMBIGUOUS_SOURCE_MATCH
TRANSFORMATION_FAILURE
STALE_DERIVATION
PLAN_GATE_REJECTION
```

Free text may explain a gap. It cannot replace the stable code and subject
identity.

## 8. Local implementation evidence

The current mechanical audit inspected first-party Malleus and Recon plus the
fleet implementations behind `docs/RECIPES.md`. The exact snapshots, paths,
mechanisms, failures, corrections, and scope boundary are retained in an
ignored private evidence appendix. This public-safe design binds that appendix
only by the digest in the header. It does not expose a private locator.

The implementations divide cleanly by concern:

| Concern | Strongest recovered mechanism | Missing piece |
|---|---|---|
| Contract compiler | Import closure, collision provenance, two generated projections, runtime registry, CI regeneration, and ontology self-materialization | No ABox migration or population mapping |
| Backend ontology lineage | Genesis contract, deterministic hash, additive evolution in the oplog, and ontology-relative quarantine | Monotonic changes only, no frontend compiler or ABox transform |
| Consumer evolution gate | Declared-versus-live comparison, replayed extension lineage, additive deployment, destructive refusal | Projection is lossy and destructive change means a new instance |
| Backend DDL projection | Inherited slots, endpoint tables, enums, bitemporal columns, and backend endpoint enforcement | Effective-contract identity and semantic registry are lost during composition |
| Declarative population | Source selectors and nine edge-mint families as data, checked by graph-equivalence tests | Missing targets are skipped and much population remains bespoke |
| Replayable population | Typed append-only records, atomic batches, deterministic rematerialization, and exact ontology binding | Record roles are not a general mapping or recipe language |
| Application compatibility | Root-load checks, inherited constraints, legacy writes, aliases, roundtrip, and deterministic IDs | Population remains hand-coded and no ontology migration exists |
| Reusable instance operations | Bounded subgraph fork, copy-on-write state, and three-way merge with conflicts | Inputs are not governed by one effective graph contract |
| Non-LinkML frontend | Custom JSON lowered to the same native backend contract | Adapter code splits authority and silently erases some values |
| Negative control | Ontology file and runtime database schema maintained independently | The ontology is descriptive, not load-bearing |

The audit corrects several older survey statements. The clinical zero-rejection
result was invalid because the root contract had not loaded. Current Logosphere
and MuevElCulo implementations have hardened since their original survey. The
fleet-wide counts in `docs/RECIPES.md` cannot all be regenerated from one
checked-in script and remain historical survey conclusions, not current
mechanical metrics.

Five objects repeatedly collapse into one another in local code:

1. `SourceOntology`, including exact import closure and frontend syntax.
2. `EffectiveContract`, the backend-neutral enforced meaning.
3. `BackendProjection`, including semantic coverage and target identity.
4. `PopulationPlan`, including selectors, transforms, identity, authority,
   missing-target behavior, ordered operations, and postconditions.
5. `EvolutionPlan`, including old and new contracts, target regeneration, ABox
   impact, transformation, supersession, refusal, validation, and rollback.

The pillar standardizes their boundaries and composition. It does not replace
the working compilers, adapters, mint rules, ledgers, or merge algorithms.

Four failure classes recur:

1. A descriptive schema is mistaken for a load-bearing gate.
2. A compiler or adapter silently drops semantics or source values.
3. Mappings, relation families, and identity rules escape into hardcoded code.
4. A generated artifact has no named runtime consumer.

Every one becomes a typed, testable protocol failure.

The local evidence enters the design graph without exposing private project
identities:

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .
@prefix okg: <https://malleus.dev/ontology-kg-realization/> .

okg:LocalCompilerEvidence rdf:type mfg:Observation .
okg:LocalPopulationEvidence rdf:type mfg:Observation .
okg:LocalReplayEvidence rdf:type mfg:Observation .
okg:LocalEvolutionEvidence rdf:type mfg:Observation .
okg:LocalSilentLossEvidence rdf:type mfg:Observation .

okg:LogicalGraphContract mfg:informedBy okg:LocalCompilerEvidence .
okg:GraphSchemaProjection mfg:informedBy okg:LocalCompilerEvidence .
okg:PopulationPlan mfg:informedBy okg:LocalPopulationEvidence .
okg:GraphRealizationAttestation mfg:informedBy okg:LocalReplayEvidence .
okg:ConstructionEvolutionImpact mfg:informedBy okg:LocalEvolutionEvidence .
okg:NoSilentSemanticLoss mfg:motivatedBy okg:LocalSilentLossEvidence .
```

## 9. Literature and standards boundary

The literature rejects a universal `ontology -> populated KG` function. It
supports a composition of contract derivation, target projection, authored
mapping, typed construction, identity policy, validation, provenance, and
evolution.

### 9.1 Contract derivation and target projections

The [LinkML derived-schema
specification](https://linkml.io/linkml-model/latest/docs/specification/04derived-schemas/)
defines derivation over imports, inheritance, mixins, and slot use. The
[validation
specification](https://linkml.io/linkml-model/latest/docs/specification/05validation/)
validates instances against the derived schema, and LinkML provides many
[target generators](https://linkml.io/linkml/schemas/generators.html).

Reuse: effective-schema derivation and target generation.

Malleus composition: a frontend-independent contract identity, a declared
support profile, fail-closed unsupported semantics, target coverage and loss,
and runtime conformance tests. `OKG-D012` selects official,
execution-identified LinkML as the sole first-party v0 frontend, not as a
mandatory runtime dependency. A custom frontend may replace it only by
emitting the same normative intermediate and passing the same conformance
boundary.

### 9.2 Source mapping and population

The W3C [Direct Mapping](https://www.w3.org/TR/rdb-direct-mapping/) reflects a
relational schema into RDF mechanically. It preserves database structure; it
does not discover a domain model. [R2RML](https://www.w3.org/TR/r2rml/) exists
for authored logical tables, subject maps, predicate-object maps, templates,
joins, and target classes. [RML 1.0](https://rml.io/specs/rml/v/1.0.0/)
generalizes this mapping pattern to heterogeneous logical sources.

Reuse: source iterators, term maps, transformations, joins, and mapping test
fixtures.

Malleus composition: exact source binding, mapping acceptance, identity policy,
content-addressed plan and run identity, staged admission, and promotion.

### 9.3 Virtual realization

[Ontop](https://ghxiao.org/publications/2020-iswc-ontop-v4.pdf) makes the
separation explicit: ontology, sources, mappings, and queries are distinct
components. Query rewriting and unfolding expose a virtual KG without first
materializing every triple.

Reuse: ontology-based data access and virtual graph realization.

Malleus composition: an explicit `RealizationMode`, freshness and query-engine
contracts, exact backend identity, and a defined relationship between virtual
results and versioned graph publications.

### 9.4 Reusable graph construction

[OTTR](https://doi.org/10.4230/TGDK.2.2.5) defines typed, parameterized,
recursively expanded templates. Its abstract base templates may be interpreted
in representations other than RDF. A template call and exact arguments
determine an expansion. [SPARQL 1.1
`CONSTRUCT`](https://www.w3.org/TR/sparql11-query/#construct) substitutes query
solutions into an authored graph template.

Selected reuse for `OKG-D001`: the pinned OTTR model and stOTTR 0.1.4 syntax,
restricted by the candidate
[GraphRecipe Profile v0](GRAPH_RECIPE_OTTR_PROFILE.md). SPARQL remains useful
for graph-to-graph transformations but is not the canonical recipe language.

Malleus composition: recipe selection, exact input retention, identity and
collision policy, gated digest-addressed instantiation, provenance, and assent.
The OTTR profile supplies topology only; the surrounding Malleus protocol owns
those other responsibilities.

### 9.5 Identity resolution

[`owl:sameAs`](https://www.w3.org/TR/owl-ref/#sameAs-def) asserts that two
references denote one individual. It does not discover that identity. The
[SSSOM model](https://mapping-commons.github.io/sssom/1.0/spec-model/) separates
mapping predicates and records justification and provenance. Link-discovery
systems such as [Silk](https://ceur-ws.org/Vol-538/ldow2009_paper13.pdf)
implement configurable discovery rather than deriving identity from the
ontology alone.

Reuse: mapping predicates, evidence, provenance, and configurable link
discovery.

Malleus composition: a separate, versioned `IdentityResolutionPolicy` covering
keys, normalization, identifier minting, equivalence predicates, thresholds,
collisions, merge and split behavior, evidence, and approval. Class mapping
never silently implies instance identity.

### 9.6 Ontology evolution and migration

Stojanovic et al.'s [user-driven ontology evolution
process](https://www.cs.ox.ac.uk/boris.motik/pubs/smms02userdriven.pdf) covers
change capture, representation, semantics, implementation, propagation, and
validation. Klein and Noy's [component-based
framework](https://ceur-ws.org/Vol-71/Klein.pdf) separates versions, change
logs, structural differences, conceptual changes, operational transforms,
approval, and coexistence.

Reuse: elementary and composite changes, change logs, dependency propagation,
coexisting versions, and validation.

Malleus composition: exact dependency closure across contract facts,
projections, mappings, recipes, identity policy, APIs, consumers, materialized
data, and accepted graph versions. A structural rename candidate is evidence,
not migration intent, until accepted.

[Functorial data migration](https://arxiv.org/abs/1009.1166) and
[BiDEL/InVerDa](https://arxiv.org/abs/1608.05564) supply formal accounts of
schema mappings and coexisting versions. They are formal analogies unless a
Malleus profile implements their prerequisites. Malleus migration is not
automatically functorial, invertible, or bidirectional.

### 9.7 Incremental maintenance

Counting, DRed, and later Datalog materialization algorithms establish
dependency-aware deletion and selective rederivation. The relevant ontology
application is described by [Volz, Staab, and
Motik](https://www.cs.ox.ac.uk/boris.motik/pubs/vsm03incremental.pdf), with a
later Datalog treatment by [Motik et
al.](https://ojs.aaai.org/index.php/AAAI/article/view/9409).

Reuse: supported incremental invalidation and rederivation algorithms.

Malleus composition: an exact supported change class, pinned rule profile,
cache boundary, invalidation policy, and clean reconstruction as the
correctness oracle. An incremental result must equal full reconstruction for
the profile that claims support. Otherwise the system rebuilds.

### 9.8 Provenance and validation

[PROV-DM](https://www.w3.org/TR/prov-dm/) models entities, activities, agents,
use, generation, and derivation. It does not prove a transformation correct.
[SHACL](https://www.w3.org/TR/shacl/) defines structured validation reports and
distinguishes validation failure from ordinary graph nonconformance.

Reuse: interoperable run provenance and structured validation results.

Malleus composition: exact source and implementation identities, declared
provenance granularity, typed failures, projection coverage, and a separate
promotion decision.

The resulting boundary is:

```text
ontology source and frontend
  -> effective contract
  -> target projection

exact sources plus mappings plus identity plus recipes
  -> realization plan
  -> isolated candidate graph
  -> validation and provenance
  -> authorization and epistemic decision
  -> immutable graph version
```

Each arrow is a named, identified activity. No arrow is licensed to infer the
missing inputs of the next.

The primary-source lineage is also recorded as graph edges:

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .
@prefix okg: <https://malleus.dev/ontology-kg-realization/> .
@prefix work: <https://malleus.dev/ontology-kg-realization/work/> .

okg:PriorWork rdf:type rdfs:Class .

work:LinkMLDerivedSchemas rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://linkml.io/linkml-model/latest/docs/specification/04derived-schemas/> .
work:R2RML rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://www.w3.org/TR/r2rml/> .
work:RML rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://rml.io/specs/rml/v/1.0.0/> .
work:Ontop rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://ghxiao.org/publications/2020-iswc-ontop-v4.pdf> .
work:OTTR rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://doi.org/10.4230/TGDK.2.2.5> .
work:SPARQLConstruct rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://www.w3.org/TR/sparql11-query/#construct> .
work:SSSOM rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://mapping-commons.github.io/sssom/1.0/spec-model/> .
work:SilkLinkDiscovery rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://ceur-ws.org/Vol-538/ldow2009_paper13.pdf> .
work:StojanovicEvolution rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://www.cs.ox.ac.uk/boris.motik/pubs/smms02userdriven.pdf> .
work:KleinNoyEvolution rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://ceur-ws.org/Vol-71/Klein.pdf> .
work:FunctorialDataMigration rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://arxiv.org/abs/1009.1166> .
work:BiDEL rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://arxiv.org/abs/1608.05564> .
work:DRedMaterialization rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://ojs.aaai.org/index.php/AAAI/article/view/9409> .
work:PROVDM rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://www.w3.org/TR/prov-dm/> .
work:SHACL rdf:type okg:PriorWork ;
    rdfs:seeAlso <https://www.w3.org/TR/shacl/> .

okg:LogicalGraphContract mfg:informedBy work:LinkMLDerivedSchemas .
okg:GraphSchemaProjection mfg:informedBy work:LinkMLDerivedSchemas .
okg:SourceMappingContract mfg:informedBy work:R2RML, work:RML, work:Ontop .
okg:CompiledGraphRecipe mfg:informedBy work:OTTR, work:SPARQLConstruct .
okg:IdentityResolutionPolicy mfg:informedBy work:SSSOM, work:SilkLinkDiscovery .
okg:ConstructionEvolutionImpact mfg:informedBy
    work:StojanovicEvolution, work:KleinNoyEvolution,
    work:FunctorialDataMigration, work:BiDEL .
okg:IncrementalMaintenanceProfile rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:informedBy work:DRedMaterialization ;
    mfg:status mfg:Candidate .
okg:GraphRealizationAttestation mfg:informedBy work:PROVDM, work:SHACL .
```

## 10. Durable design and downstream feedback

This work has four authority layers. They must not collapse:

```text
private implementation evidence
  -> opaque observations and evidence digests
  -> candidate or author-accepted design objects
  -> public-safe conformance fixtures
  -> implemented capability and existing public documentation
```

Private evidence may inform design. It cannot set design status. A candidate
design becomes `AcceptedDesign` only through an author decision. An accepted
design becomes `Implemented` only when code, machine-readable capability
status, and hard tests agree. Generated prose and graph projections never
promote themselves.

The local fleet audit now has eleven stable adoption records. Each record pins
one repository snapshot, one primary protocol role, one first patch, one hard
test, and the evidence it must return. Exact project identities and paths stay
in the ignored private registry whose digest appears in this document's
header. No downstream repository has been edited.

The reusable feedback cycle is:

```text
ProjectAssessment
  -> AdoptionPacket
  -> ProjectImplementation
  -> ConformanceReceipt + ConstructionGapSet
  -> Malleus Recon evidence
  -> ProtocolRevision
  -> superseding AdoptionPacket
```

Every future adopter carries one machine-readable conformance manifest. It
pins the protocol bundle, repository snapshot, declared seam-file digests,
consumed and produced artifact kinds, contract and profile identities,
generated artifacts, hard-test identity, result digest, and typed gaps. A
receipt is `CURRENT` only while every pin matches. Any changed seam, governing
profile, compiler, contract, artifact, or hard test makes it `STALE`.

A protocol revision computes reverse dependency closure. Every affected
consumer receives a `FeedbackObligation` with one required disposition:

```text
UNCHANGED
REGENERATE
REVALIDATE
REPLAN
MIGRATE
SUPERSEDE
RETRACT
BLOCKED
```

The change does not edit another repository automatically. It makes the
required work visible and prevents stale guidance from presenting itself as
current.

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .
@prefix okg: <https://malleus.dev/ontology-kg-realization/> .

okg:ProjectAssessment rdf:type mfg:DesignObject ;
    mfg:produces okg:AdoptionPacket .

okg:AdoptionPacket rdf:type mfg:DesignObject ;
    mfg:dependsOn okg:MalleusGraphRecipeProfileV0 ;
    mfg:dependsOn okg:GraphRealizationConformanceBundle ;
    mfg:targets okg:RepositorySnapshot .

okg:ProjectImplementation
    mfg:derivedFrom okg:AdoptionPacket ;
    mfg:produces okg:ConformanceReceipt ;
    mfg:produces okg:ConstructionGapSet .

okg:ProtocolRevision
    mfg:invalidates okg:ConformanceReceipt ;
    mfg:produces okg:FeedbackObligation .

okg:FeedbackObligation rdf:type mfg:DesignObject ;
    mfg:targets okg:RepositorySnapshot ;
    mfg:requiresDisposition okg:ImpactDisposition ;
    mfg:status mfg:Open .
```

Public documentation is projected only after the public-safe conformance slice
passes and implementation promotion is authorized. At that point the existing
ontology, graph, recipe, adoption, implementation-status, README, changelog,
and release surfaces change together. A new skill or submodule is not proposed
yet. The repeatable unit is first the profile plus conformance bundle. Revisit
mechanism extraction after a second independent pillar repeats the workflow
without changing it.

## 11. Defensible Malleus contribution

Malleus should concede schema generation, declarative mappings, graph
templates, graph construction queries, validation, provenance, and ontology
evolution as established work.

The candidate contribution is their executable composition under one
protocol:

1. An effective contract with stable semantic identity.
2. Explicit separation of derived, supplied, and observed decisions.
3. Target projection with machine-readable semantic coverage and loss.
4. Content-addressed recipe instantiation and construction planning.
5. Fail-closed typed gaps instead of silent generator behavior.
6. Pre-materialization staging through the same structural gate as every other
   write.
7. Optional evidence audit and epistemic decision before accepted graph state.
8. Declared evidence identity and replay with explicit dependency and
   environment boundaries.
9. Dependency-closed contract evolution and graph migration without rewriting
   history.

The novelty claim, if later supported empirically, concerns this composition
and its measured failure behavior. It does not concern any component in
isolation.

### 11.1 Candidate composition-completeness claim

The author proposed the intuition that experimental learning across component
boundaries could make the composed protocol complete. This design records that
intuition as `ProtocolCompositionCompleteness`, a candidate falsifiable claim.
It is not proof and is not an accepted design status.

Completeness is relative to one pinned protocol revision and an explicit
coverage matrix. The matrix must inventory every declared component, contract,
profile, backend, workload envelope, producer-consumer seam, cross-protocol
scenario, and known exclusion. Every component boundary needs independent
positive, negative, and metamorphic conformance evidence. Every composed path
needs deterministic identity, typed failure, lineage, atomicity, and change
propagation evidence. Dependency-closed revision must identify every affected
artifact and adopter.

The implemented `GE-000` through `GE-020` GraphRecipe slice contributes
boundary-first fixtures, independently frozen expected artifacts, layer-local
diagnostics, deterministic semantic identities, selected-manifest receipt
binding, metamorphic cases, lineage projections, and explicit exclusions. It
provides partial evidence only for `ComponentBoundaryConformance`,
`CompositionSeamConformance`, and `KnownExclusionAccounting` at the
ontology-to-population boundary. `DeclaredProtocolComponentCoverage`, full
`CrossProtocolScenarioConformance`, and
`DependencyClosedChangeConformance` remain candidate obligations.

The results may inform frontend-neutrality, logical-derivation, no-bypass,
evidence, governance, and execution-identity experiments. They do not discharge
those experiments. The report binds 149 checksummed corpus files, 10 case
receipts, and 7 executable metamorphic obligations. Its identity is
`sha256:6d41cd245234dc3b77bbbc5a5c16529d197aa9db2a03f1525c1b1602d17c82a8`;
the checksum-set identity is
`sha256:aa5c904f79363b68bab9d82a2b6b027748ffe25358ef3fead5c5ba7b3dc7a3f2`.

Removing an unused runner import changed the report's bound execution bytes.
The hard identity guard rejected the stale report and produced retained identity
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`,
which supersedes
`sha256:41b180b273ecc24e59af769736519c071707134beecf91ae60ce10a1092a1ae0`.
A later bound-source refresh produced
`sha256:9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0`,
which supersedes the retained
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`
identity. The active release-boundary refresh binds the final declared sources,
three relevant-core test files, current observations, and the non-enumerating
public-snapshot guard. Its identity above supersedes
`sha256:9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0`.
Both dedicated CI steps require a clean Ruff check over the full GraphRecipe
runner directory before the 40-test slice.

The superseding declared-evidence identity covers exact declared source bytes,
selected manifests, receipts, and recorded observation objects. It does not
establish complete transitive dependency or execution-environment closure.
Generated-schema parity with the runtime registry also remains open; neither
limitation is promoted to shipped capability.

The claim is expressly not universal. It does not cover undeclared protocols,
arbitrary future components, all profile versions, all backends, all workloads,
or untested interactions. A hidden input or decision, uncovered legal path,
semantic divergence, silent failure, privileged bypass, nondeterminism, or
incomplete impact set is counterevidence. Such evidence blocks promotion for
the pinned revision and must remain in lineage. Revision requires a new
experiment, narrowed scope, retraction, or a superseding claim that retains the
prior claim, evidence, counterevidence, coverage matrix, and dependency closure.

## 12. First discriminating research-local slice

The first GraphRecipe slice is complete at its bound research snapshot. It
tests the boundary before defining a public API:

1. `GE-000` derives a narrowed logical contract from ontology input and proves
   that ontology alone produces no population.
2. `GE-010` expands one typed entity recipe, lowers it to existing
   `ProposedOperation` values, and stages and materializes the candidate through
   current Malleus seams.
3. `GE-020` assembles two nodes and one relation independently of recipe pattern
   order, with explicit local-reference dependencies and structural admission.
4. Ten positive and negative cases freeze logical contracts, terminal facts,
   `OperationDependencyPlan` data, proposed operations, graph snapshots,
   lineage, diagnostics, and semantic digests. Their retained v0 research wire
   label is "member graph"; it does not denote another knowledge graph.
5. Seven executable metamorphic obligations test repeated execution,
   formatting, safe prefix aliases, alpha renaming, and pattern permutation at
   the layers each transformation must preserve.
6. Every case receipt binds its selected-manifest source-byte identity. The
   report binds the complete receipt identities, checksum set, runner, direct
   core dependencies, and package-boundary sources.
7. The dedicated slice passed 40 tests. The relevant core selection passed 257
   tests with 2 skips.
8. The full configured suite recorded 807 passes and 2 skips. That result is a
   report-bound observation, not complete suite-source, dependency, or
   execution-environment identity.

The result is bounded. It does not establish optional add-ons or multivalue
expansion, mappings and identity collisions, all record families,
dependency-closed evolution, Recon dogfood, Lutra equivalence, a second
backend, broad workload quality, or public capability. Those remain in
`GE-030` through `GE-100`; `GE-030` is next.

## 13. Decisions required before implementation

1. `OKG-D001`, recipe representation, was **accepted on 2026-08-17**. The
   selected design is the pinned stOTTR profile in
   [`GRAPH_RECIPE_OTTR_PROFILE.md`](GRAPH_RECIPE_OTTR_PROFILE.md). A native
   recipe DSL, multiple v0 frontends, and an OTTR fork are rejected. Objective
   revisit triggers are part of the decision.
2. `OKG-D002`, second backend, remains open. Select one generated validation,
   RDF, or typed graph-store profile after `OKG-D001`. The current
   in-memory graph is the first profile.
3. `OKG-D003`, construction-history placement, remains open. The current
   evidence favors a content-addressed plan artifact referenced through the
   existing `ProtocolLedger`, not a second ledger, but this is not accepted.
4. `OKG-D004`, identity-policy scope, remains open. The current evidence favors
   one explicit policy per `PopulationPlan`, with composed sub-policies and
   declared precedence where needed.
5. `OKG-D005`, virtual-realization status, remains open. Decide whether a
   mapping-backed query view is a first-class `GraphRealization` or a separate
   nonmaterializing profile.
6. `OKG-D006`, bootstrap contract, remains open. Select the minimal seed
   contract that defines realization artifacts before Malleus represents them
   through its own ontology.
7. `OKG-D007`, terminal ABI, was **accepted on 2026-08-17**. Member, operation
   kind, record type, and property symbols are IRIs; graph record IDs remain
   strings.
8. `OKG-D008`, assembly scope, was **accepted on 2026-08-17**. Terminal facts
   assemble across the complete atomic `PopulationPlan`, including anchored
   property-only add-ons across invocations.
9. `OKG-D009`, local reference dependencies, was **accepted on 2026-08-17**.
   Every reference to a record created in the same plan requires `DependsOn`.
10. `OKG-D010`, multivalue canonicalization, was **accepted on 2026-08-17**.
    Unordered multivalues canonicalize as semantic sets with full derivation
    lineage; ordered values preserve contract-declared order.
11. `OKG-D011`, CI split, was **accepted on 2026-08-17**. The offline Malleus
    corpus is primary and a separate pinned Lutra job is the required
    differential oracle once its tool lock exists.
12. `OKG-D012`, contract frontend and modularity policy, was **accepted on
    2026-08-17**. Official, execution-identified LinkML is the sole first-party
    v0 authoring frontend. The compiled runtime remains LinkML-free, direct
    facts remain bootstrap and conformance inputs, and a custom frontend may
    replace LinkML only through the same normative artifact boundary and
    conformance suite.
13. `OKG-D013`, running-domain fixture policy, was **accepted on 2026-08-28**.
    It selects fixture object `OKG-FX001`, Small Shop Fulfilment, for pillar
    explanations, research-local experiments, and future conformance work.
    Shop vocabulary remains fixture-local. The fixture is synthetic and
    literature-informed rather than copied source data. Existing `GE-000`
    through `GE-020` fixtures remain frozen historical evidence. Replacement
    requires a superseding decision and impact analysis. The decision does not
    override contract-compiler `OD-010`.

`OKG-D013` and `OKG-FX001` are deliberately distinct. The former records the
author's accepted selection and replacement rule. The latter is the governed
fixture object against which explanations and experiments can bind exact
sources, symbols, mappings, recipes, and independently authored oracles. This
is a design and test-governance change, not a new runtime protocol semantic.

Separately on 2026-08-28, the author accepted
`DeterministicCompilerOptionalProposalProducerArchitecture`. The trusted
compiler is deterministic and fail-closed. An optional ontology-builder or
corrector skill may produce exact candidate bytes, but remains outside the
compiler, enters through ordinary protocol review, and is never called during
replay. This architecture boundary is not another object selected by
`OKG-D013`.

The author accepted the contract compiler directions on 2026-08-24, the exact
compiler baseline on 2026-08-25, nine blocking policies on 2026-08-26, and the
governance topology on 2026-08-27:

1. `AD-001` selects `EffectiveContract` as the public runtime root. The API may
   break before 1.0, but implementation promotion remains gated by conformance.
2. `AD-002` is already represented by `OKG-D012`; no duplicate decision record
   is created.
3. `AD-003` keeps stage protocols experimental and places compatibility claims
   on named, conformant whole-pipeline combinations.
4. `AD-004` rejects implicit duplicate-symbol precedence. Composition fails
   closed unless a versioned symbol policy authorizes it.
5. `AD-005` separates independent upstream units and binds their integration
   to exact commits, while intrinsic dependencies remain sequential or stacked.
6. `OD-001` selects one canonical consumer-bundle manifest per consumer.
   `OD-006` now supplies the closed three-role composition and `OD-013` the
   one-distribution topology; `CC-D16` still owns exact bundle fields and
   canonical bytes.
7. `OD-012` selects the published LinkML 1.11.1 release, exact wheel and sdist
   identities, the CPython 3.12.10 Linux x86_64 `cp312` reproducibility tuple,
   pip 25.0.1, and the exact slim Bookworm OCI identities. CC-002 materializes
   and attests those bytes; a future fork requires a new governed revision.
8. `OD-002` selects slot-only exact explicit adoption with a literal Boolean
   marker, authoritative imported owner, pre-normalization equality, and no
   order winner.
9. `OD-003` selects pinned LinkML 1.11.1 as the replaceable default adapter,
   materializes defaults explicitly, refuses repeated and conflicting mixins,
   and classifies all nine CC-X01 observations.
10. `OD-004` selects a new persisted-wire epoch and stable typed hard break,
    with no fallback, receipt, migration, translation, or rewrite.
11. `OD-005` selects ontology-powered atomic subject-predicate-object facts,
    exact canonical JSON bytes, whole-set validation, provenance separation,
    and internal candidate digests without promoting public fact IDs.
12. `OD-011` selects exactly one explicit resolver profile per compilation,
    strict Malleus resolution by default, default-denied capabilities, retained
    exact provenance, no fallback chain, and cycle refusal.
13. `OD-013` selects one future distribution whose normal installation includes
    the compiler and LinkML while the artifact-backed runtime remains unable to
    import LinkML.
14. `OD-014` accepts Quiet Bell Archive as the public working name, keeps its
    vocabulary fixture-only, records the text/data authorship and Apache-2.0
    attestation, excludes visual assets, and makes public review digest-bound.
15. `OD-006` selects exactly three semantic roles in one closed composition,
    fixed conceptual v0 identity constructors, one accepted-temporal
    composition per ledger epoch, and a governed-graph-only structural case.
    Independent role heads, wire encodings, migration, and stable public fact
    IDs remain deferred.
16. `OD-008` selects one closed exact-location LinkML v0 support profile,
    strict JSON-shaped YAML, a pinned seven-name builtin map, explicit
    defaults and provenance, the immutable D05 seed plus one flat exactly-one
    extension, and internal content identities. Public compiler promotion
    remains with `OD-009`.
17. `OD-007` selects one protected, replay-derived governance partition inside
    the full accepted-temporal graph. ProtocolLedger remains sole write
    authority; authorization uses pre-event authority state seeded by one
    external root and otherwise derived from accepted governance state; policy
    instances under the same governance contract stay in the same epoch; no
    governance-specific head, graph, or query surface is added.
18. `OD-010` selects strong same-role and same-partition non-inlined class
    references over accepted prestate plus earlier ordered writes, Entity-only
    relation endpoints, Entity-or-Relation signal bearers, one global record-ID
    namespace, and referentially closed temporal views. Runtime sorting,
    cross-role borrowing, cascade, repair, deletion, migration, and read-access
    policy remain outside the decision.

`OKG-D001` and `OKG-D007` through `OKG-D013` are closed. OTTR is sufficient for
the narrowed topology role, the five experiment-exposed microdecisions are
accepted design, and LinkML is selected without becoming a privileged protocol
dependency. `OKG-FX001` now anchors explanation and empirical work across those
decisions. A later fixture replacement requires a superseding decision,
preserved lineage, and dependency-impact analysis. A protocol-design change
still requires addressable counterevidence and a superseding decision, not an
implicit implementation choice.

The literature and local implementation audits are closed for the prior design
pass. The research-local GraphRecipe first slice now exists, but public runtime
promotion remains open. Before further abstract expansion, the main pillar and
its compiler dependency must restate their next claims against `OKG-FX001` and
show the exact concrete object at every boundary. That grounding does not erase
the accepted dependency graph: the exact contract-kernel object model remains
the first unresolved protocol dependency, followed by `OKG-D002` through
`OKG-D006`; the GraphRecipe experiment branch remains open at `GE-030`.

## 14. Mechanical validation of this design pass

`OKG-D013` and `OKG-FX001` were accepted after the revision 20 validation
recorded below. Their tuples are now present in this source document. Canonical
foundation-graph revision 21, its digest, the renewed aggregate counts, and the
overseer `DOCUMENT_REVISION` belong to the compiler-lane reanchoring
transaction. The revision 20 report remains historical evidence and must not be
read as covering this decision.

The accepted contract compiler directions are projected through one dedicated
block:

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .
@prefix cc: <https://malleus.dev/contract-compiler/> .

mfg:ExperimentalStageProtocolWholePipelineConformanceBoundary
    rdf:type mfg:Boundary ;
    mfg:governedBy mfg:UnixModularProtocolDoctrine ;
    mfg:status mfg:AcceptedDesign .

mfg:FailClosedDuplicateSymbolComposition
    rdf:type mfg:Invariant ;
    mfg:governedBy mfg:SymbolIdentityPolicy ;
    mfg:status mfg:AcceptedDesign .

mfg:IndependentUpstreamUnitsExactCommitIntegrationTopology
    rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

mfg:PerConsumerCanonicalBundleManifest
    rdf:type mfg:Requirement ;
    mfg:dependsOn mfg:ContractComposition ;
    mfg:dependsOn mfg:EffectiveContractArtifact ;
    mfg:status mfg:AcceptedDesign .

cc:AD-001 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-24" ;
    mfg:selects mfg:EffectiveContract ;
    mfg:status mfg:AcceptedDesign .

cc:AD-003 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-24" ;
    mfg:selects mfg:ExperimentalStageProtocolWholePipelineConformanceBoundary ;
    mfg:status mfg:AcceptedDesign .

cc:AD-004 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-24" ;
    mfg:selects mfg:FailClosedDuplicateSymbolComposition ;
    mfg:status mfg:AcceptedDesign .

cc:AD-005 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-24" ;
    mfg:selects mfg:IndependentUpstreamUnitsExactCommitIntegrationTopology ;
    mfg:status mfg:AcceptedDesign .

cc:OD-001 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-24" ;
    mfg:selects mfg:PerConsumerCanonicalBundleManifest ;
    mfg:status mfg:AcceptedDesign .

cc:OD-002 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-26" ;
    mfg:selects mfg:ExactSlotOnlyExplicitAdoptionProfile ;
    mfg:status mfg:AcceptedDesign .

cc:OD-003 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-26" ;
    mfg:selects mfg:LinkML1_11_1ReplaceableDefaultFrontendAdapterProfile ;
    mfg:status mfg:AcceptedDesign .

cc:OD-004 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-26" ;
    mfg:selects mfg:TypedPersistedWireEpochHardBreakProfile ;
    mfg:status mfg:AcceptedDesign .

cc:OD-005 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-26" ;
    mfg:selects mfg:AtomicOntologyPoweredCanonicalFactContract ;
    mfg:status mfg:AcceptedDesign .

cc:OD-006 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-26" ;
    mfg:selects mfg:ThreeRoleClosedContractCompositionProfile ;
    mfg:status mfg:AcceptedDesign .

cc:OD-007 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-27" ;
    mfg:rejects mfg:GovernancePolicyGraphR2 ;
    mfg:selects mfg:ProtectedReplayDerivedGovernancePartitionTopologyV0 ;
    mfg:status mfg:AcceptedDesign .

cc:OD-008 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-26" ;
    mfg:selects mfg:MalleusLinkMLSupportProfileV0 ;
    mfg:status mfg:AcceptedDesign .

cc:OD-011 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-26" ;
    mfg:selects mfg:ExplicitSingleResolverProfileSelection ;
    mfg:status mfg:AcceptedDesign .

cc:OD-013 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-26" ;
    mfg:selects mfg:SingleDistributionCompilerIncludedPackagingTopology ;
    mfg:status mfg:AcceptedDesign .

cc:OD-014 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-26" ;
    mfg:selects mfg:QuietBellArchiveFixturePublicationBoundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactSlotOnlyExplicitAdoptionProfile rdf:type mfg:SupportProfile ;
    mfg:binds mfg:SlotDeclarationsOnlyAdoptionBoundary ;
    mfg:binds mfg:LiteralBooleanAdoptsTrueRequiredBoundary ;
    mfg:binds mfg:ImportedAncestorOwnerAuthoritativeBoundary ;
    mfg:binds mfg:ExactTypedSourceStructureBeforeDefaultsBoundary ;
    mfg:binds mfg:RemoveOnlyDescriptionAdoptsAndEmptyAnnotationsComparisonBoundary ;
    mfg:binds mfg:AdoptionDifferenceOrInvalidMarkerRefusalBoundary ;
    mfg:binds mfg:SourceOrderNeverCompositionWinnerBoundary ;
    mfg:status mfg:AcceptedDesign .

mfg:GenericNeutralResultConformanceBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:SourceLanguageSpecificNamedVersionedProfileAndCorpusBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkMLCorpusOnlyForLinkMLCompatibilityClaimBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkML1_11_1ReplaceableDefaultFrontendAdapterProfile
    rdf:type mfg:SupportProfile ;
    mfg:binds mfg:ReplaceableAdapterNeutralOutputContract ;
    mfg:binds mfg:GenericNeutralResultConformanceBoundary ;
    mfg:binds mfg:SourceLanguageSpecificNamedVersionedProfileAndCorpusBoundary ;
    mfg:binds mfg:LinkMLCorpusOnlyForLinkMLCompatibilityClaimBoundary ;
    mfg:binds mfg:NamedVersionedAdapterSupportAndDefaultProfileBoundary ;
    mfg:binds mfg:AppliedDefaultsExplicitWithProvenanceBoundary ;
    mfg:binds mfg:RuntimeNeverInfersFrontendDefaultsBoundary ;
    mfg:binds mfg:NoLegacyOntologyRegistryEmulationV0Boundary ;
    mfg:binds mfg:CCX01SimpleParityEqual ;
    mfg:binds mfg:CCX01ParentMixinPrecedenceLinkML ;
    mfg:binds mfg:CCX01RepeatedMixinRefused ;
    mfg:binds mfg:CCX01ConflictingMixinsABRefused ;
    mfg:binds mfg:CCX01ConflictingMixinsBARefused ;
    mfg:binds mfg:CCX01NumericBoundsLinkML ;
    mfg:binds mfg:CCX01ExplicitFalseEqual ;
    mfg:binds mfg:CCX01DefaultRangeLinkMLExplicit ;
    mfg:binds mfg:CCX01AttributeSlotUsageLinkML ;
    mfg:status mfg:AcceptedDesign .

mfg:AtomicOntologyPoweredCanonicalFactContract rdf:type mfg:Boundary ;
    mfg:binds mfg:ExactNonExpressionSeedContractMetamodel ;
    mfg:binds mfg:AtomicCanonicalJSONFactProfileV0 ;
    mfg:binds mfg:AbsoluteIdentifierExactUnicodeSymbolPolicyV0 ;
    mfg:binds mfg:LinkMLV0SlashQualifiedSymbolPolicy ;
    mfg:binds mfg:ContractMetamodelSemanticAuthorityOverJSONBoundary ;
    mfg:binds mfg:ClosedThreeMemberCanonicalJSONFactWireBoundary ;
    mfg:binds mfg:CanonicalDecimalLexicalNumericObjectBoundary ;
    mfg:binds mfg:InternalCandidateDigestNotPublicIdentityBoundary ;
    mfg:binds mfg:StructuralIdentityAndExternalProvenanceBoundary ;
    mfg:binds mfg:FrontendDirectFactConformanceOnlyParityBoundary ;
    mfg:binds mfg:ExactSeedMetamodelBootstrapTrustBoundary ;
    mfg:binds mfg:ExpressionCapableContractMetamodelV0 ;
    mfg:binds mfg:AdmissionArtifactBundleAndPromotionSeparateAuthorityBoundary ;
    mfg:binds mfg:NoGenericDefaultValueOrRuntimeDefaultBoundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactNonExpressionSeedContractMetamodel rdf:type mfg:ContractMetamodel ;
    mfg:binds mfg:ExactClassSeedFactRule ;
    mfg:binds mfg:ExactSlotAndSlotUseSeedFactRule ;
    mfg:binds mfg:ExactEnumSeedFactRule ;
    mfg:binds mfg:ExactScalarAndSeedPrimitiveFactRule ;
    mfg:binds mfg:ExactWholeSetSeedFactInvariant ;
    mfg:binds mfg:SourceToFactCompletenessSeparateConformanceBoundary ;
    mfg:identifiedBy <urn:malleus:contract-metamodel:non-expression-seed:v0:sha256:1c68a612f3e7a0f80c31965aa5525954921dfbee60d151552d10d61cb0aac71b> ;
    mfg:status mfg:AcceptedDesign .

mfg:FlatExactlyOneExpressionExtensionV0 rdf:type mfg:ContractMetamodel ;
    mfg:binds mfg:ExactlyOneGroupFactRule ;
    mfg:binds mfg:ExactlyOneAlternativeFactRule ;
    mfg:binds mfg:SlotConditionFactRule ;
    mfg:binds mfg:FlatExactlyOneWholeSetInvariant ;
    mfg:identifiedBy <urn:malleus:contract-metamodel:flat-exactly-one-extension:v0:sha256:99527d21040cbdda9dd7c579af7f40af8645de9b5f4b1e8ba28b40ddff7d53e6> ;
    mfg:status mfg:AcceptedDesign .

mfg:ExpressionCapableContractMetamodelV0 rdf:type mfg:ContractMetamodel ;
    mfg:binds mfg:ExactNonExpressionSeedContractMetamodel ;
    mfg:binds mfg:FlatExactlyOneExpressionExtensionV0 ;
    mfg:binds mfg:ClosedSeedExpressionRuleUnionCompositionV0 ;
    mfg:identifiedBy <urn:malleus:contract-metamodel:expression-capable:v0:sha256:65aae23b7a0892a4d2ae2b5adc6888f1ddd39c94ce03f412d50a6a5ccd5d0964> ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactlyOneGroupFactRule rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactlyOneAlternativeFactRule rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:SlotConditionFactRule rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:FlatExactlyOneWholeSetInvariant rdf:type mfg:Invariant ;
    mfg:status mfg:AcceptedDesign .

mfg:ClosedSeedExpressionRuleUnionCompositionV0 rdf:type mfg:Boundary ;
    mfg:supersedes mfg:ExpressionVocabularyDeferredToOD008Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ClosedExactLocationClassificationV0 rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:StrictJSONShapedYAMLSourceGrammarV0 rdf:type mfg:SupportProfile ;
    mfg:status mfg:AcceptedDesign .

mfg:TrustedLinkML1_11_1SevenBuiltinMapV0 rdf:type mfg:SupportProfile ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkML1_11_1ElaborationAndDefaultProfileV0 rdf:type mfg:SupportProfile ;
    mfg:status mfg:AcceptedDesign .

mfg:LosslessSourceDeclarationAndProvenanceProfileV0 rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkMLV0SlashQualifiedSymbolPolicy rdf:type mfg:SymbolIdentityPolicy ;
    mfg:identifiedBy <urn:malleus:contract-symbol-policy:linkml-v0-slash-qualified:v0> ;
    mfg:status mfg:AcceptedDesign .

mfg:RetainedCorpusWholeSourceClosureV0 rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:FrontendAdapterConstructionInjectionDeferredBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:NoGeneralLinkMLSupportClaimBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:AtomicCanonicalJSONFactProfileV0 rdf:type mfg:FactCanonicalizationProfile ;
    mfg:status mfg:AcceptedDesign .

mfg:AbsoluteIdentifierExactUnicodeSymbolPolicyV0
    rdf:type mfg:SymbolIdentityPolicy ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactClassSeedFactRule rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactSlotAndSlotUseSeedFactRule rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactEnumSeedFactRule rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactScalarAndSeedPrimitiveFactRule rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactWholeSetSeedFactInvariant rdf:type mfg:Invariant ;
    mfg:status mfg:AcceptedDesign .

mfg:SourceToFactCompletenessSeparateConformanceBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ContractMetamodelSemanticAuthorityOverJSONBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ClosedThreeMemberCanonicalJSONFactWireBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:CanonicalDecimalLexicalNumericObjectBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:InternalCandidateDigestNotPublicIdentityBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:StructuralIdentityAndExternalProvenanceBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:FrontendDirectFactConformanceOnlyParityBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ExactSeedMetamodelBootstrapTrustBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ExpressionVocabularyDeferredToOD008Boundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:AdmissionArtifactBundleAndPromotionSeparateAuthorityBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:NoGenericDefaultValueOrRuntimeDefaultBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:TypedPersistedWireEpochHardBreakProfile rdf:type mfg:SupportProfile ;
    mfg:binds mfg:PersistedWireEpochCheckedBeforeSemanticDecodeBoundary ;
    mfg:binds mfg:ExactPublicDiagnosticIdentifierDeferredToCCW01Boundary ;
    mfg:binds mfg:LegacyOntologyHashNeverReinterpretedBoundary ;
    mfg:binds mfg:NoPersistedWireFallbackReceiptMigrationTranslationOrRewriteBoundary ;
    mfg:binds mfg:ReconProjectTypedHardBreak ;
    mfg:binds mfg:ReconRecordTypedHardBreak ;
    mfg:binds mfg:KnowledgeGraphSnapshotTypedHardBreak ;
    mfg:binds mfg:ProtocolEnvelopeTypedHardBreakBeforeReplay ;
    mfg:binds mfg:EmbeddedGraphBaseAndCandidateNotReached ;
    mfg:status mfg:AcceptedDesign .

mfg:ExplicitSingleResolverProfileSelection rdf:type mfg:SupportProfile ;
    mfg:binds mfg:StrictMalleusResolverDefaultBoundary ;
    mfg:binds mfg:ExplicitNamedVersionedResolverAndConfigurationBoundary ;
    mfg:binds mfg:ResolverSoleByteSourceAdapterNoHiddenIOBoundary ;
    mfg:binds mfg:ResolverFileAndNetworkCapabilitiesDefaultDenyBoundary ;
    mfg:binds mfg:ResolverNeverTryNextFallbackBoundary ;
    mfg:binds mfg:ExactResolvedSourceAndImportEdgeProvenanceBoundary ;
    mfg:binds mfg:ExactResolvedLocatorStringModuleInstanceIdentityBoundary ;
    mfg:binds mfg:NoUniversalLocatorNormalizationBoundary ;
    mfg:binds mfg:RootRetainedSourceSeparateFromImportEdgeBoundary ;
    mfg:binds mfg:ImportEdgeCarriesParentOrdinalLiteralAndChildResolvedLocatorBoundary ;
    mfg:binds mfg:ResolvedIdentityDifferentBytesRefusalBoundary ;
    mfg:binds mfg:DifferentLocatorSameBytesDistinctObservationBoundary ;
    mfg:binds mfg:ImportOrderProvenanceOnlyBoundary ;
    mfg:binds mfg:AllImportCyclesRefusedWithLineageBoundary ;
    mfg:status mfg:AcceptedDesign .

mfg:SingleDistributionCompilerIncludedPackagingTopology rdf:type mfg:DesignObject ;
    mfg:binds mfg:NormalMalleusInstallIncludesCompilerAndLinkMLBoundary ;
    mfg:binds mfg:NoCoreCompilerExtraOrSecondDistributionV0Boundary ;
    mfg:binds mfg:LeanInstallDeferredGovernedRevisionBoundary ;
    mfg:binds mfg:ArtifactBackedRuntimeLinkMLImportBlockedBoundary ;
    mfg:binds mfg:TargetTopologyNotCurrentPackagingClaimBoundary ;
    mfg:status mfg:AcceptedDesign .

mfg:QuietBellArchiveFixturePublicationBoundary rdf:type mfg:Boundary ;
    mfg:workingName "Quiet Bell Archive" ;
    mfg:attestationText "Luis Guzman Lorenzo is the author and rights holder for the original Quiet Bell text/data, licensed Apache-2.0" ;
    mfg:binds mfg:QuietBellVocabularyFixtureOnlyCoreNeutralBoundary ;
    mfg:binds mfg:QuietBellAttestationExcludesVisualAssetsBoundary ;
    mfg:binds mfg:FuturePublicAssetExactManifestBoundary ;
    mfg:binds mfg:CCPUB01ReviewBindsExactManifestDigestBoundary ;
    mfg:binds mfg:AssetOrManifestChangeInvalidatesPublicReviewBoundary ;
    mfg:binds mfg:DecisionCreatesNoFixtureAssetOrPublicationBoundary ;
    mfg:status mfg:AcceptedDesign .

cc:OD-012 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-25" ;
    mfg:selects mfg:LinkMLV1_11_1ReleaseCompilerBaselineR3 ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkMLV1_11_1ReleaseCompilerBaselineR3 rdf:type mfg:DesignObject ;
    mfg:supersedes mfg:LinkMLV1_11_1ReleaseCompilerBaselineR2 ;
    mfg:binds mfg:LinkMLV1_11_1ReleaseCoordinate ;
    mfg:binds mfg:LinkMLV1_11_1ProvenanceCommit-a7ed3e4cbb19731f072d0d90b6d52f7d822569ee ;
    mfg:binds mfg:LinkMLV1_11_1PublishedWheelRetentionSet ;
    mfg:binds mfg:LinkMLV1_11_1PublishedSdistRetentionSet ;
    mfg:binds mfg:CPython3_12_10LinuxX86_64Cp312ReproducibilityTuple ;
    mfg:binds mfg:Pip25_0_1HashPinnedRequirementsWheelhouseOfflineInstallProfile ;
    mfg:binds mfg:OfficialPython3_12_10SlimBookwormLinuxAmd64PlatformProfile ;
    mfg:binds mfg:Antlr4Python3Runtime4_9_3DeterministicWheelBuildProfile ;
    mfg:binds mfg:Prefixcommons0_1_12Malleus1WheelDerivationProfile ;
    mfg:binds mfg:CC002CompilerEnvironmentMaterializationAndAttestationBoundaryR3 ;
    mfg:binds mfg:FinalRuntimeClosureRemainsWheelOnlyBoundary ;
    mfg:binds mfg:RootSourceRetentionSeparateFromTransitiveBuildInputBoundary ;
    mfg:binds mfg:DerivativeInputSeparateFromBuildAndRuntimeBoundary ;
    mfg:binds mfg:NetworkDeniedSourceBuildBoundary ;
    mfg:binds mfg:TwoFreshBuildsByteIdenticalBoundary ;
    mfg:binds mfg:TwoFreshTransformsByteIdenticalBoundary ;
    mfg:binds mfg:DerivedWheelDirectResolverInputBoundary ;
    mfg:binds mfg:OfficialPrefixcommonsAbsentFromRuntimeWheelhouseBoundary ;
    mfg:binds mfg:RuntimeClosureExcludesPytestPytestLoggingAndPyBoundary ;
    mfg:binds mfg:MalleusDerivedPackagingMaintenanceAndSecurityOwnershipBoundary ;
    mfg:binds mfg:FutureCleanUpstreamReplacementRequiresGovernedDecisionBoundary ;
    mfg:binds mfg:FutureForkSeparateGovernedBaselineRevisionBoundary ;
    mfg:binds mfg:PublishedReleaseWheelsRetainedNotRebuiltBoundary ;
    mfg:binds mfg:ReproducibilityTupleNotRuntimeSupportPolicyBoundary ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkMLV1_11_1ReleaseCompilerBaselineR2 rdf:type mfg:DesignObject ;
    mfg:supersedes mfg:LinkMLV1_11_1ReleaseCompilerBaseline ;
    mfg:binds mfg:LinkMLV1_11_1ReleaseCoordinate ;
    mfg:binds mfg:LinkMLV1_11_1ProvenanceCommit-a7ed3e4cbb19731f072d0d90b6d52f7d822569ee ;
    mfg:binds mfg:LinkMLV1_11_1PublishedWheelRetentionSet ;
    mfg:binds mfg:LinkMLV1_11_1PublishedSdistRetentionSet ;
    mfg:binds mfg:CPython3_12_10LinuxX86_64Cp312ReproducibilityTuple ;
    mfg:binds mfg:Pip25_0_1HashPinnedRequirementsWheelhouseOfflineInstallProfile ;
    mfg:binds mfg:OfficialPython3_12_10SlimBookwormLinuxAmd64PlatformProfile ;
    mfg:binds mfg:Antlr4Python3Runtime4_9_3DeterministicWheelBuildProfile ;
    mfg:binds mfg:CC002CompilerEnvironmentMaterializationAndAttestationBoundaryR2 ;
    mfg:binds mfg:FinalRuntimeClosureRemainsWheelOnlyBoundary ;
    mfg:binds mfg:RootSourceRetentionSeparateFromTransitiveBuildInputBoundary ;
    mfg:binds mfg:NetworkDeniedSourceBuildBoundary ;
    mfg:binds mfg:TwoFreshBuildsByteIdenticalBoundary ;
    mfg:binds mfg:FutureForkSeparateGovernedBaselineRevisionBoundary ;
    mfg:binds mfg:PublishedReleaseWheelsRetainedNotRebuiltBoundary ;
    mfg:binds mfg:ReproducibilityTupleNotRuntimeSupportPolicyBoundary ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkMLV1_11_1ReleaseCompilerBaseline rdf:type mfg:DesignObject ;
    mfg:binds mfg:LinkMLV1_11_1ReleaseCoordinate ;
    mfg:binds mfg:LinkMLV1_11_1ProvenanceCommit-a7ed3e4cbb19731f072d0d90b6d52f7d822569ee ;
    mfg:binds mfg:LinkMLV1_11_1PublishedWheelRetentionSet ;
    mfg:binds mfg:LinkMLV1_11_1PublishedSdistRetentionSet ;
    mfg:binds mfg:CPython3_12_10LinuxX86_64Cp312ReproducibilityTuple ;
    mfg:binds mfg:Pip25_0_1HashPinnedRequirementsWheelhouseOfflineInstallProfile ;
    mfg:binds mfg:OfficialPython3_12_10SlimBookwormLinuxAmd64PlatformProfile ;
    mfg:binds mfg:CC002CompilerEnvironmentMaterializationAndAttestationBoundary ;
    mfg:binds mfg:FutureForkSeparateGovernedBaselineRevisionBoundary ;
    mfg:binds mfg:PublishedReleaseWheelsRetainedNotRebuiltBoundary ;
    mfg:binds mfg:ReproducibilityTupleNotRuntimeSupportPolicyBoundary ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkMLV1_11_1ReleaseCoordinate rdf:type mfg:DesignObject ;
    mfg:binds mfg:LinkMLV1_11_1ProvenanceCommit-a7ed3e4cbb19731f072d0d90b6d52f7d822569ee ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkMLV1_11_1ProvenanceCommit-a7ed3e4cbb19731f072d0d90b6d52f7d822569ee
    rdf:type mfg:ArtifactIdentity .

mfg:LinkMLV1_11_1PublishedWheelRetentionSet rdf:type mfg:DesignObject ;
    mfg:binds <https://malleus.dev/foundation-graph/linkml-1.11.1-py3-none-any.whl-sha256-d1bbb97a8b1ea4a99b145007875733a5e5e89b3acfe3e9d1e369fa4a582990ed> ;
    mfg:binds <https://malleus.dev/foundation-graph/linkml_runtime-1.11.1-py3-none-any.whl-sha256-b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da> ;
    mfg:status mfg:AcceptedDesign .

<https://malleus.dev/foundation-graph/linkml-1.11.1-py3-none-any.whl-sha256-d1bbb97a8b1ea4a99b145007875733a5e5e89b3acfe3e9d1e369fa4a582990ed>
    rdf:type mfg:ArtifactIdentity .

<https://malleus.dev/foundation-graph/linkml_runtime-1.11.1-py3-none-any.whl-sha256-b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da>
    rdf:type mfg:ArtifactIdentity .

mfg:LinkMLV1_11_1PublishedSdistRetentionSet rdf:type mfg:DesignObject ;
    mfg:binds <https://malleus.dev/foundation-graph/linkml-1.11.1.tar.gz-sha256-2f6774e13628270cadaeecda3313db0437ecc15cd44ee35c6c2655dbe31c8524> ;
    mfg:binds <https://malleus.dev/foundation-graph/linkml_runtime-1.11.1.tar.gz-sha256-e71300b596c4f35aeccd9dca096806678402213dbdb2c5e8e68f507e21320754> ;
    mfg:status mfg:AcceptedDesign .

<https://malleus.dev/foundation-graph/linkml-1.11.1.tar.gz-sha256-2f6774e13628270cadaeecda3313db0437ecc15cd44ee35c6c2655dbe31c8524>
    rdf:type mfg:ArtifactIdentity .

<https://malleus.dev/foundation-graph/linkml_runtime-1.11.1.tar.gz-sha256-e71300b596c4f35aeccd9dca096806678402213dbdb2c5e8e68f507e21320754>
    rdf:type mfg:ArtifactIdentity .

mfg:CPython3_12_10LinuxX86_64Cp312ReproducibilityTuple
    rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

mfg:Pip25_0_1HashPinnedRequirementsWheelhouseOfflineInstallProfile
    rdf:type mfg:SupportProfile ;
    mfg:binds <https://malleus.dev/foundation-graph/pip-25.0.1-py3-none-any.whl-sha256-c46efd13b6aa8279f33f2864459c8ce587ea6a1a59ee20de055868d8f7688f7f> ;
    mfg:dependsOn mfg:CC002Pip25_0_1ResolverAndTransitiveClosureAttestation ;
    mfg:status mfg:AcceptedDesign .

<https://malleus.dev/foundation-graph/pip-25.0.1-py3-none-any.whl-sha256-c46efd13b6aa8279f33f2864459c8ce587ea6a1a59ee20de055868d8f7688f7f>
    rdf:type mfg:ArtifactIdentity .

mfg:OfficialPython3_12_10SlimBookwormLinuxAmd64PlatformProfile
    rdf:type mfg:SupportProfile ;
    mfg:binds mfg:Python3_12_10SlimBookwormTagLookup2026_08_25 ;
    mfg:binds mfg:Python3_12_10SlimBookwormLinuxAmd64Child-sha256-97983fa8cc88343512862c62307159a82261c3528dc025f79e5a3f7af43e50b4 ;
    mfg:binds mfg:OCIChildDigestRuntimePinAndIndexProvenanceBoundary ;
    mfg:dependsOn mfg:CC002OCIIndexAndLinuxAmd64ChildDigestAttestation ;
    mfg:status mfg:AcceptedDesign .

mfg:Python3_12_10SlimBookwormTagLookup2026_08_25 rdf:type mfg:DesignObject ;
    mfg:binds mfg:Python3_12_10SlimBookwormOCIIndex-sha256-fd95fa221297a88e1cf49c55ec1828edd7c5a428187e67b5d1805692d11588db ;
    mfg:binds mfg:Python3_12_10SlimBookwormLinuxAmd64Child-sha256-97983fa8cc88343512862c62307159a82261c3528dc025f79e5a3f7af43e50b4 .

mfg:Python3_12_10SlimBookwormOCIIndex-sha256-fd95fa221297a88e1cf49c55ec1828edd7c5a428187e67b5d1805692d11588db
    rdf:type mfg:ArtifactIdentity .

mfg:Python3_12_10SlimBookwormLinuxAmd64Child-sha256-97983fa8cc88343512862c62307159a82261c3528dc025f79e5a3f7af43e50b4
    rdf:type mfg:ArtifactIdentity .

mfg:OCIChildDigestRuntimePinAndIndexProvenanceBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:CC002Pip25_0_1ResolverAndTransitiveClosureAttestation
    rdf:type mfg:TestObligation ;
    mfg:status mfg:Candidate .

mfg:CC002OCIIndexAndLinuxAmd64ChildDigestAttestation
    rdf:type mfg:TestObligation ;
    mfg:status mfg:Candidate .

mfg:CC002CompilerEnvironmentMaterializationAndAttestationBoundary
    rdf:type mfg:Boundary ;
    mfg:dependsOn mfg:CC002Pip25_0_1ResolverAndTransitiveClosureAttestation ;
    mfg:dependsOn mfg:CC002OCIIndexAndLinuxAmd64ChildDigestAttestation ;
    mfg:status mfg:AcceptedDesign .

mfg:Antlr4Python3Runtime4_9_3DeterministicWheelBuildProfile
    rdf:type mfg:SupportProfile ;
    mfg:binds <https://malleus.dev/foundation-graph/antlr4-python3-runtime-4.9.3.tar.gz-bytes-117034-sha256-f224469b4168294902bb1efa80a8bf7855f24c99aef99cbefc1bcd3cce77881b> ;
    mfg:binds <https://malleus.dev/foundation-graph/setuptools-83.0.0-py3-none-any.whl-bytes-1008090-sha256-29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3> ;
    mfg:binds mfg:SetuptoolsBuildMetaLegacyBackend ;
    mfg:binds mfg:SourceDateEpoch315532800 ;
    mfg:binds mfg:NetworkDeniedSourceBuildBoundary ;
    mfg:binds mfg:TwoFreshBuildsByteIdenticalBoundary ;
    mfg:status mfg:AcceptedDesign .

<https://malleus.dev/foundation-graph/antlr4-python3-runtime-4.9.3.tar.gz-bytes-117034-sha256-f224469b4168294902bb1efa80a8bf7855f24c99aef99cbefc1bcd3cce77881b>
    rdf:type mfg:ArtifactIdentity .

<https://malleus.dev/foundation-graph/setuptools-83.0.0-py3-none-any.whl-bytes-1008090-sha256-29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3>
    rdf:type mfg:ArtifactIdentity .

mfg:SetuptoolsBuildMetaLegacyBackend rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

mfg:SourceDateEpoch315532800 rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

mfg:CC002Antlr4Python3Runtime4_9_3DoubleBuildAttestation
    rdf:type mfg:TestObligation ;
    mfg:status mfg:Candidate .

mfg:CC002CompilerEnvironmentMaterializationAndAttestationBoundaryR2
    rdf:type mfg:Boundary ;
    mfg:supersedes mfg:CC002CompilerEnvironmentMaterializationAndAttestationBoundary ;
    mfg:dependsOn mfg:CC002Pip25_0_1ResolverAndTransitiveClosureAttestation ;
    mfg:dependsOn mfg:CC002OCIIndexAndLinuxAmd64ChildDigestAttestation ;
    mfg:dependsOn mfg:CC002Antlr4Python3Runtime4_9_3DoubleBuildAttestation ;
    mfg:status mfg:AcceptedDesign .

mfg:Prefixcommons0_1_12Malleus1WheelDerivationProfile
    rdf:type mfg:SupportProfile ;
    mfg:binds <https://malleus.dev/foundation-graph/prefixcommons-0.1.12-py3-none-any.whl-bytes-29482-sha256-16dbc0a1f775e003c724f19a694fcfa3174608f5c8b0e893d494cf8098ac7f8b> ;
    mfg:binds <https://malleus.dev/foundation-graph/prefixcommons-LICENSE-bytes-1500-sha256-3a9b5b0d46996cdfd82b65429e189904e4ab1908014ce408cbecde9f591f37b4> ;
    mfg:binds mfg:Prefixcommons0_1_12Malleus1DerivedVersionIdentity ;
    mfg:binds mfg:Prefixcommons0_1_12UpstreamInventory14Members109044ExpandedBytesBoundary ;
    mfg:binds mfg:PrefixcommonsPayloadAndLicenseIdentityBoundary ;
    mfg:binds mfg:PrefixcommonsPytestLoggingRequirementOnlyRemovalBoundary ;
    mfg:binds mfg:MalleusCC002WheelDerivationV1GeneratorIdentity ;
    mfg:binds mfg:WheelDerivationV1RecordProfile ;
    mfg:binds mfg:ZipStoredFixedMetadataBoundary ;
    mfg:binds mfg:TwoFreshTransformsByteIdenticalBoundary ;
    mfg:status mfg:AcceptedDesign .

<https://malleus.dev/foundation-graph/prefixcommons-0.1.12-py3-none-any.whl-bytes-29482-sha256-16dbc0a1f775e003c724f19a694fcfa3174608f5c8b0e893d494cf8098ac7f8b>
    rdf:type mfg:ArtifactIdentity .

<https://malleus.dev/foundation-graph/prefixcommons-LICENSE-bytes-1500-sha256-3a9b5b0d46996cdfd82b65429e189904e4ab1908014ce408cbecde9f591f37b4>
    rdf:type mfg:ArtifactIdentity .

mfg:Prefixcommons0_1_12Malleus1DerivedVersionIdentity
    rdf:type mfg:ArtifactIdentity .

mfg:Prefixcommons0_1_12UpstreamInventory14Members109044ExpandedBytesBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:PrefixcommonsPayloadAndLicenseIdentityBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:PrefixcommonsPytestLoggingRequirementOnlyRemovalBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:MalleusCC002WheelDerivationV1GeneratorIdentity rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

mfg:WheelDerivationV1RecordProfile rdf:type mfg:SupportProfile ;
    mfg:status mfg:AcceptedDesign .

mfg:ZipStoredFixedMetadataBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:TwoFreshTransformsByteIdenticalBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:DerivativeInputSeparateFromBuildAndRuntimeBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:DerivedWheelDirectResolverInputBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:OfficialPrefixcommonsAbsentFromRuntimeWheelhouseBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:RuntimeClosureExcludesPytestPytestLoggingAndPyBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:MalleusDerivedPackagingMaintenanceAndSecurityOwnershipBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:FutureCleanUpstreamReplacementRequiresGovernedDecisionBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:CC002Prefixcommons0_1_12Malleus1DoubleTransformAttestation
    rdf:type mfg:TestObligation ;
    mfg:status mfg:Candidate .

mfg:CC002CompilerEnvironmentV3EvidenceProfile rdf:type mfg:SupportProfile ;
    mfg:binds mfg:WheelDerivationV1RecordProfile ;
    mfg:status mfg:AcceptedDesign .

mfg:CC002CompilerEnvironmentMaterializationAndAttestationBoundaryR3
    rdf:type mfg:Boundary ;
    mfg:supersedes mfg:CC002CompilerEnvironmentMaterializationAndAttestationBoundaryR2 ;
    mfg:dependsOn mfg:CC002Pip25_0_1ResolverAndTransitiveClosureAttestation ;
    mfg:dependsOn mfg:CC002OCIIndexAndLinuxAmd64ChildDigestAttestation ;
    mfg:dependsOn mfg:CC002Antlr4Python3Runtime4_9_3DoubleBuildAttestation ;
    mfg:dependsOn mfg:CC002Prefixcommons0_1_12Malleus1DoubleTransformAttestation ;
    mfg:binds mfg:CC002CompilerEnvironmentV3EvidenceProfile ;
    mfg:status mfg:AcceptedDesign .

mfg:FinalRuntimeClosureRemainsWheelOnlyBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:RootSourceRetentionSeparateFromTransitiveBuildInputBoundary
    rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:NetworkDeniedSourceBuildBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:TwoFreshBuildsByteIdenticalBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:PublishedReleaseWheelsRetainedNotRebuiltBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:ReproducibilityTupleNotRuntimeSupportPolicyBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .

mfg:FutureForkSeparateGovernedBaselineRevisionBoundary rdf:type mfg:Boundary ;
    mfg:status mfg:AcceptedDesign .
```

Performed on 2026-08-27:

1. The 28 Turtle blocks across the foundation, pillar, GraphRecipe profile,
   checkpoint, and TDD experiment projections parsed as
   1,716 RDF triples.
2. [`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl) parsed as
   the same 1,716 triples. Both directed set differences
   were empty.
3. The canonical `dependsOn` graph has 107 nodes and 108 edges, with no directed
   dependency cycle.
4. All 357 subjects carrying `mfg:status` have exactly one distinct status.
   The 0.11 temporal slice has the required three dependency edges, two
   implemented capabilities, two open obligations, and one implemented
   observation binding all four.
5. `OKG-D007` through `OKG-D012` each have exactly `DecisionRecord`,
   `decidedBy Author`, `decisionDate "2026-08-17"`, and
   `status AcceptedDesign`.
6. Contract compiler `AD-001`, `AD-003` through `AD-005`, and `OD-001` each
   have exactly `DecisionRecord`, `decidedBy Author`, `decisionDate
   "2026-08-24"`, one selected object, and `status AcceptedDesign`. `AD-002`
   remains represented only by `OKG-D012`. `OD-012` has the same invariants
   with `decisionDate "2026-08-25"` and selects exactly the R3 release baseline.
7. `OD-002` through `OD-006`, `OD-008`, `OD-011`, `OD-013`, and `OD-014` have
   the same decision invariants with `decisionDate "2026-08-26"` and select
   exactly the nine accepted policy objects. Those objects bind the exact
   adoption, divergence classification, hard-break, atomic-fact,
   closed-composition, closed support profile, resolver, packaging, and themed
   publication boundaries recorded by the decision workbook.
8. `OD-007` has the same decision invariants with `decisionDate "2026-08-27"`,
   selects the protected replay-derived governance-partition topology, and
   rejects the separate-governance-graph alternative.
9. `OD-010` has the same decision invariants with `decisionDate "2026-08-27"`,
   selects the strong local contextual-reference admission profile, rejects
   Entity/Event/Signal relation endpoints, and binds the exact role, partition,
   ancestry, ordering, endpoint, bearer, identity, temporal-closure, and
   zero-implementation boundaries.
10. The `OD-012` R3 baseline retains the exact R2 release, Python, pip, OCI,
   ANTLR, and setuptools coordinates. It additionally binds the exact
   `prefixcommons` input and local-version derivation, package and BSD 3-Clause
   license payload identity, two byte-identical network-denied transforms, v3
   evidence boundary, direct derived-wheel resolver input, runtime test-package
   exclusions, Malleus maintenance ownership, and governed future-replacement
   boundary.
11. `ProtocolCompositionCompleteness` has exactly `Candidate` status, six
   coverage obligations, an explicit universal-completeness exclusion, and
   addressable counterevidence and revision semantics.
12. The three partially evidenced completeness obligations have exactly
   `Partial` status. The other three remain exactly `Candidate`.
13. The first-slice fixture and offline core CI gate have exactly `Implemented`
   status; the wider TDD program and experimental learning have exactly
   `Partial` status. `GE-030` through `GE-100`, Lutra, second-backend
   conformance, public promotion, generated-schema parity, and execution-
   environment closure remain open.
14. The active report identity supersedes three retained identities. Each
   addressable refresh observation binds adjacent identities to the hard guard.
   Both workflow-step nodes bind the Ruff gate and the 40-test fixture.
15. The canonical body contains 1,716 unique, lexically sorted N-Triples. Its
   SHA-256 is
   `16eda5d16adfee5f54fa651a7b13ac18baff7fcaf4d6cd133ab82846b3fa169a`, and every
   owned Markdown graph reference names revision 20 and that digest.
16. All 24 relative Markdown links in the five owned
    Markdown documents resolve locally.
17. None of the five owned Markdown documents or the canonical Turtle artifact
   contains an absolute home-directory or local-file URI locator.
18. Trailing-whitespace checks over the seven identity files and the privacy
    regression test report no error.

The graph projection, invariant, link, privacy, and whitespace checks were
rerun before revision 20 was frozen. Existing GraphRecipe implementation
evidence was not reissued by this design-only promotion.
