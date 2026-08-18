# Ontology-driven KG realization

Design status: accepted pillar, candidate protocol and completeness claim

Design revision: 6

Decision authority: author

Accepted decision: `OKG-D000`, ontology-driven KG realization is a pillar

Decision date: 2026-08-17

Repository snapshot: `codex/malleus-recon` at
`384ecc37917c8191d17ffa44867024a36dfdd313`

Canonical design graph: [`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl),
revision 7,
`sha256:0a308fa3e3b99b71a677fbc0bec6d3efec455d1d74b693b3a2bfd43d69cee53e`

Evidence cutoff: 2026-08-17

Private implementation-audit snapshot:
`sha256:9b62ed651e0b571a3301da559494d55fd9fe35f7790016a64cb163f43214f47a`

Private adoption-registry snapshot:
`sha256:4b373134bb7af272216cb788c28180e07a333530e5b6caf885f8243d33fd4d41`

Implementation status: the `GE-000` through `GE-020` GraphRecipe slice is
implemented research-locally. No public API or shipped GraphRecipe capability
is asserted here. This document records the evidence, boundary, dependency
graph, accepted GraphRecipe microdecisions, and candidate
protocol-completeness claim. Live edits to `ROADMAP.md`,
`design/EXECUTION_BUNDLE.md`, and the paper-dojo worktree remain outside this
document.

## 1. Decision and scope

Ontology-driven KG realization is a Malleus pillar.

The pillar name keeps the ontology visible. The enclosed mechanism is the
`Graph Realization Protocol`, because “ontology-to-KG” would incorrectly imply
that the ontology alone supplies mappings, identities, recipes, and instances.

The pillar asks a precise question:

> Given an evolving effective domain contract, what additional declared inputs
> are required to deterministically derive a target graph schema, construct a
> candidate instance graph, diagnose every gap, admit the candidate through
> Malleus, and reproduce or migrate the result?

This is a protocol inside the protocol. Its compiler has no privileged write
path. It produces an exact construction plan whose operations pass through the
existing structural gate, staging, monitoring, decision, and materialization
mechanisms.

The pillar is accepted. The object model, wire formats, template formalism,
ledger integration, and public API remain candidate design.

## 2. “KG structure” names four different things

The phrase must not hide four separate outputs:

| Layer | Exact meaning | What the ontology can determine |
|---|---|---|
| Logical graph contract | Permitted record kinds, inheritance, properties, relation signatures, and constraints | Mostly derivable from an effective contract |
| Backend graph schema | Labels or types, fields, endpoint constraints, indexes, and other target-specific declarations | Partly derivable after a backend capability profile is supplied |
| Reusable graph topology | A parameterized pattern of records and relations that must occur together | Constrained by the ontology, but selected and parameterized by a recipe |
| Instance population | Concrete identities, values, relations, provenance, and source evidence | Requires source mappings, identity policy, transformations, and source artifacts |

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

CandidateSubgraph
  = stage(GraphConstructionPlan.proposed_operations)

GraphRealization
  = decide_and_materialize(CandidateSubgraph, EpistemicPolicy)
```

Every function above returns either a content-addressed result or typed gaps.
No phase silently drops a source field, ontology fact, recipe member, proposed
operation, or target capability mismatch.

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
7. Base graph digest and intended construction scope.
8. Ordered operations and their derivation traces.
9. All gaps, exclusions, and warnings.

Deterministic inputs must produce identical canonical plans and digests.
Nondeterministic producers may supply values, but each attempt and exact output
is retained as an observed input before plan compilation.

Output: `GraphConstructionPlan` or a blocked result with typed gaps.

### Phase 6: Stage and verify

The plan is converted to the existing `CandidateSubgraph` path. Structural
refusals remain refusals. The compiler cannot filter or rewrite rejected
operations after observing the gate. A new plan revision must preserve the
failed attempt and its diagnostics.

Logical, temporal, conflict, uncertainty, evidence, and authority monitors are
selected by exact policy. A backend projection check also verifies that the
target artifact and runtime behavior agree for the exercised semantics.

Output: staged candidate, operations, monitor records, and typed witnesses.

### Phase 7: Decide and materialize

Structural validity is not epistemic acceptance. A candidate-bound `ACCEPT`
may produce an accepted graph application through the existing protocol.
`REJECT`, `DEFER`, and `CONTEST` leave the base graph unchanged.

Output: a materialized structural snapshot or accepted temporal graph version,
with exact protocol heads.

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

okg:OntologyDrivenKGRealization rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:status mfg:AcceptedDesign .

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
and runtime conformance tests. LinkML is a reference frontend, not a mandatory
runtime dependency.

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
8. Exact execution identity and replay.
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
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`;
the checksum-set identity is
`sha256:aa5c904f79363b68bab9d82a2b6b027748ffe25358ef3fead5c5ba7b3dc7a3f2`.

Removing an unused runner import changed the report's bound execution bytes.
The hard identity guard rejected the stale report and forced a
dependency-closed refresh. The active report identity supersedes retained
identity
`sha256:41b180b273ecc24e59af769736519c071707134beecf91ae60ce10a1092a1ae0`.
The unchanged checksum-set identity and unchanged 39-test result do not erase
the runner-identity change. Both dedicated CI steps now require a clean Ruff
check over the full GraphRecipe runner directory before the slice tests.

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
   member graphs, proposed operations, graph snapshots, lineage, diagnostics,
   and semantic digests.
5. Seven executable metamorphic obligations test repeated execution,
   formatting, safe prefix aliases, alpha renaming, and pattern permutation at
   the layers each transformation must preserve.
6. Every case receipt binds its selected-manifest source-byte identity. The
   report binds the complete receipt identities, checksum set, runner, direct
   core dependencies, and package-boundary sources.
7. The dedicated slice passed 39 tests. The relevant core selection passed 236
   tests with 2 skips.
8. The full configured suite recorded 743 passes, 3 skips, and one unrelated
   dirty-worktree packaging-guard failure. The report therefore excludes a
   clean-worktree and release attestation.

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

`OKG-D001` and `OKG-D007` through `OKG-D011` are closed. OTTR is sufficient for
the narrowed topology role, and the five experiment-exposed microdecisions are
accepted design. A later change requires addressable counterevidence and a
superseding decision, not an implicit implementation choice.

The literature and local implementation audits are closed for this design
pass. The research-local GraphRecipe first slice now exists, but public runtime
promotion remains open. The main pillar resumes the exact contract-kernel
object-model decision, then `OKG-D002` through `OKG-D006` in order. The
GraphRecipe branch resumes at `GE-030` without changing that main sequence.

## 14. Mechanical validation of this design pass

Performed on 2026-08-17:

1. The 25 Turtle blocks across the foundation, pillar, GraphRecipe profile,
   checkpoint, and TDD experiment projections parsed as
   1,000 RDF triples.
2. [`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl) parsed as
   the same 1,000 triples. Both directed set differences
   were empty.
3. The canonical `dependsOn` graph has 84 nodes and 85 edges, with no directed
   dependency cycle.
4. All 193 subjects carrying `mfg:status` have
   exactly one distinct status.
5. `OKG-D007` through `OKG-D011` each have exactly `DecisionRecord`,
   `decidedBy Author`, `decisionDate "2026-08-17"`, and
   `status AcceptedDesign`.
6. `ProtocolCompositionCompleteness` has exactly `Candidate` status, six
   coverage obligations, an explicit universal-completeness exclusion, and
   addressable counterevidence and revision semantics.
7. The three partially evidenced completeness obligations have exactly
   `Partial` status. The other three remain exactly `Candidate`.
8. The first-slice fixture and offline core CI gate have exactly `Implemented`
   status; the wider TDD program and experimental learning have exactly
   `Partial` status. `GE-030` through `GE-100`, Lutra, second-backend
   conformance, and public promotion remain open.
9. The active report identity supersedes the retained prior identity, and the
   addressable refresh observation binds the runner-byte change to the hard
   identity guard. Both workflow-step nodes bind the Ruff gate and the 39-test
   fixture.
10. The canonical body contains 1,000 unique, lexically sorted N-Triples. Its
   SHA-256 is
   `0a308fa3e3b99b71a677fbc0bec6d3efec455d1d74b693b3a2bfd43d69cee53e`, and every
   owned Markdown graph reference names revision 7 and that digest.
11. All 24 relative Markdown links in the five owned
    Markdown documents resolve locally.
12. None of the five owned Markdown documents or the canonical Turtle artifact
   contains an absolute home-directory or local-file URI locator.
13. Trailing-whitespace checks over all six owned files report no error.

The test results above are retained from the exact conformance report rather
than rerun after this design-graph projection update.
