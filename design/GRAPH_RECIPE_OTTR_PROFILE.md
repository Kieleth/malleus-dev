# Malleus GraphRecipe Profile v0

Decision ID: `OKG-D001`

Decision status: accepted by the author on 2026-08-17

Binding microdecisions: `OKG-D007` through `OKG-D011`, accepted by the author
on 2026-08-17

Profile status: accepted design with a research-local implementation of the
`GE-000` through `GE-020` conformance slice

Opened: 2026-08-17

Decision authority: author

Repository snapshot: `codex/malleus-recon` at
`1657e6564c1f8ab872d56b9ec97e34a015fce765`

Canonical design graph: [`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl),
revision 9,
`sha256:046d20def4c127afecd82811fd19ad8adf2a06e9247373e1fbf7a5dde47a3905`

Evidence:
[`OTTR_SUFFICIENCY_AUDIT.md`](../research/ontology_driven_kg_realization/OTTR_SUFFICIENCY_AUDIT.md)
and
[`FIRST_SLICE_CONFORMANCE_REPORT.json`](../research/ontology_driven_kg_realization/experiments/graph_recipe/FIRST_SLICE_CONFORMANCE_REPORT.json)

Shipped capability: none

## 1. Accepted decision

`OKG-D001` selects OTTR as the canonical GraphRecipe language.

Malleus GraphRecipe v0 uses stOTTR 0.1.4 as its only authored
representation, interpreted under mOTTR 0.1.2 and the rOTTR 0.2.0 RDF term and
type model. Malleus defines a restrictive GraphRecipe Profile over OTTR. It
does not define a second recipe language, accept multiple recipe frontends, or
fork OTTR.

A GraphRecipe expresses a finite, reusable graph topology. It expands to
Malleus target-neutral construction facts, not directly to a graph backend.
Source selection, transformation, domain identity, collision behavior,
provenance, atomic planning, admission, authorization, and evolution remain
separate required protocol artifacts.

`CompiledGraphRecipe` is a derived, canonicalized OTTR model with validation
and lineage. It is not another authored source of truth.

The rejected options are:

1. A native Malleus recipe DSL.
2. Multiple authored recipe frontends in v0.
3. An OTTR grammar or expansion-semantics fork.
4. RDF triples as the mandatory intermediate representation.
5. SPARQL `CONSTRUCT` as the canonical recipe language.

## 2. Exact boundary

```text
GraphRecipeArtifact
  + locked template-library closure
  + GraphRecipe Profile v0
  + LogicalGraphContract binding
  -> CompiledGraphRecipe

CompiledGraphRecipe
  + typed invocation arguments
  + expansion budget
  -> terminal Malleus construction facts
  -> canonical operation-member graph
  -> ordered ProposedOperation values

SourceMappingContract
  + TransformationContract
  + IdentityResolutionPolicy
  + SourceConflictPolicy
  + selected recipe invocations
  -> PopulationPlan

PopulationPlan
  + CompiledGraphRecipe outputs
  + source artifacts
  + backend projection
  -> GraphConstructionPlan
  -> existing staging and assent path
```

GraphRecipe owns topology expansion. It does not own the complete graph
realization.

## 3. Normative references

The profile pins:

1. [stOTTR 0.1.4](https://spec.ottr.xyz/stOTTR/0.1.4/) for authored syntax.
2. [mOTTR 0.1.2](https://spec.ottr.xyz/mOTTR/0.1.2/) for the abstract template
   model and expansion validity.
3. [rOTTR 0.2.0](https://spec.ottr.xyz/rOTTR/0.2.0/) for RDF terms and types.
4. [The 2024 OTTR framework paper](https://drops.dagstuhl.de/entities/document/10.4230/TGDK.2.2.5)
   for the published base-template and library framework.

Mutable development specifications are not normative. A later profile revision
may update these pins through a superseding decision.

## 4. Normative v0 restrictions

### 4.1 Input and dependency closure

1. stOTTR 0.1.4 is the only accepted authored input. wOTTR, tabOTTR, and bOTTR
   are outside v0.
2. Every library must be valid, well-founded, referentially complete,
   consistently typed, variable-safe, and acyclic under the pinned semantics.
3. Every dependency resolves from a content-addressed lock. Compilation never
   fetches a mutable network resource.
4. Every public recipe has a versioned template IRI, semantic version, source
   digest, effective digest, and profile identity.
5. The compiler rejects an undeclared template, base template, type, prefix,
   annotation, or dependency.
6. The profile declares a maximum template depth, invocation count, list size,
   cross-product size, terminal-member count, and output-byte budget. Exceeding
   any limit is a typed failure, not a partial result.

### 4.2 Identity

1. Source bytes and effective recipe meaning have separate identities.
2. Formatting, comments, safe prefix aliases, declaration order, and variable
   alpha-renaming may change the source digest without changing the effective
   digest.
3. Invocation identity is the digest of the effective recipe identity,
   canonical typed arguments, effective contract identity, and expansion
   profile identity.
4. Blank-node constants and fresh blank nodes are forbidden in effective
   topology.
5. Every terminal record member has a unique recipe-member IRI.
6. Every graph record ID is supplied by `IdentityResolutionPolicy` or is
   derived deterministically from invocation identity and recipe-member IRI
   under that policy. A recipe cannot choose a competing mint rule.

### 4.3 Values, defaults, and conditions

1. `none` is forbidden for a mandatory parameter. OTTR's empty expansion for
   a missing mandatory value cannot suppress a required member silently.
2. Defaults are allowed only when the recipe or governing contract declares
   them. The applied default and its origin remain in the derivation trace.
3. v0 permits scalar RDF terms, references, and finite lists that bind to
   Malleus scalar, reference, or multivalued slots. Unordered multivalued slots
   canonicalize as semantic sets while retaining every derivation path.
   Ordered slots preserve contract-declared order. Arbitrary maps, structs,
   tuples, and term functions are outside v0.
4. `cross` is the only list expander allowed in v0, and only under the declared
   expansion budget. `zipMin` and `zipMax` are forbidden because truncation and
   padding can hide cardinality errors.
5. v0 has no value-dependent branch language.
6. An optional parameter may add or omit property bindings on an already
   required member. It cannot determine member identity, record type, relation
   endpoints, or operation dependencies.
7. Optional record groups use explicit add-on recipes. `PopulationPlan` records
   whether and why it invoked each add-on recipe.

### 4.4 Expansion and operation assembly

1. Expansion terminates only in the closed Malleus base vocabulary in section
   5. `ottr:Triple` is not a terminal construction operation in v0.
2. OTTR pattern order has no execution meaning.
3. The compiler retains every expansion path before set normalization.
   Duplicate paths to one member produce either declared idempotence or a
   typed duplicate-member diagnostic.
4. The compiler gathers and validates the complete atomic `PopulationPlan`
   terminal expansion before it emits an operation. Assembly crosses invocation
   boundaries within that plan.
5. A property-only add-on may target a member anchored by exactly one `Record`
   in another invocation in the same plan. A member without exactly one
   plan-wide anchor is invalid.
6. Terminal facts assemble into a member dependency graph. Dependencies must
   be acyclic and every referenced member must resolve. Every reference to a
   record created in the same plan requires `DependsOn`, including relation
   endpoints, signal bearers, and class-valued properties.
7. A stable topological sort uses canonical member IRI as the only tie-breaker.
8. Each assembled member lowers to exactly one existing `ProposedOperation`.
9. The compiler never writes a graph. `GraphConstructionPlan` is its only
   executable output, and that plan enters the normal staging and assent path.

### 4.5 Metadata and diagnostics

1. A closed Malleus annotation vocabulary binds effective-contract
   preconditions, expected postconditions, named readers, lifecycle state, and
   optional inverse, retirement, or merge recipe references.
2. An annotation can reference policy or a companion recipe. It cannot grant
   mutation, identity, collision, migration, authorization, or admission
   semantics.
3. Every OTTR and profile error maps to a stable Malleus diagnostic code while
   retaining the original tool diagnostic as evidence.
4. Unknown annotations fail in v0. They are not ignored as comments.

## 5. Closed construction base vocabulary

`OKG-D007` through `OKG-D010` fix the terminal ABI and assembler behavior. v0
admits only these terminal kinds:

| Terminal kind | Meaning |
|---|---|
| `Record` | Declares one operation member, operation kind, effective-contract record type, and graph record ID |
| `Property` | Binds one effective-contract property and typed value to a member |
| `RelationSource` | Binds the source graph record ID for a relation member |
| `RelationTarget` | Binds the target graph record ID for a relation member |
| `DependsOn` | Requires one member to precede another |

The terminal signatures are:

```text
Record(member: IRI, operation_kind: closed Malleus operation IRI,
       record_type: effective-contract type IRI, record_id: string)
Property(member: IRI, property: effective-contract property IRI,
         value: RDF term or finite list)
RelationSource(member: IRI, record_id: string)
RelationTarget(member: IRI, record_id: string)
DependsOn(member: IRI, prerequisite_member: IRI)
```

Member, operation-kind, record-type, and property symbols are IRIs. Graph record
IDs remain strings because that is the existing graph contract.

The assembler applies these rules:

1. Exactly one `Record` exists for every member.
2. `Record` operation kind is one of the four existing create operations:
   entity, relation, signal, or event.
3. A property symbol resolves in the bound `LogicalGraphContract` and occurs at
   most once per member unless the slot is multivalued.
4. A relation has exactly one source and target. Other record roles have none.
5. An endpoint may refer to an existing graph record. Every reference to a
   record created in the same atomic plan declares a dependency on that member.
   The same rule applies to signal bearers and class-valued properties.
6. Every required effective-contract property is bound before lowering.
7. Unknown, conflicting, or incomplete terminal facts block the plan.

The conformance fixture freezes the accepted signatures and exact argument
serialization. Prose cannot create a second wire format.

## 6. Illustrative recipe

This example shows the intended division and accepted terminal types. It
remains non-normative until the conformance fixture freezes exact stOTTR bytes
and expected expansions.

```stottr
@prefix ex: <https://example.org/recipe/> .
@prefix mgrp: <https://malleus.dev/graph-recipe/base/> .
@prefix ottr: <http://ns.ottr.xyz/0.4/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

mgrp:Record [
  ! ottr:IRI ?member,
  ! ottr:IRI ?operationKind,
  ! ottr:IRI ?recordType,
  ! xsd:string ?recordId
] :: BASE .

mgrp:Property [
  ! ottr:IRI ?member,
  ! ottr:IRI ?property,
  ?value
] :: BASE .

mgrp:RelationSource [
  ! ottr:IRI ?member,
  ! xsd:string ?recordId
] :: BASE .

mgrp:RelationTarget [
  ! ottr:IRI ?member,
  ! xsd:string ?recordId
] :: BASE .

mgrp:DependsOn [
  ! ottr:IRI ?member,
  ! ottr:IRI ?prerequisite
] :: BASE .

<https://example.org/recipe/DrugEnzymeInteraction/1.0.0> [
  ! ottr:IRI ?drugMember,
  ! xsd:string ?drugId,
  ! xsd:string ?drugName,
  ! ottr:IRI ?enzymeMember,
  ! xsd:string ?enzymeId,
  ! ottr:IRI ?relationMember,
  ! xsd:string ?relationId
] :: {
  mgrp:Record(?drugMember, mgrp:CreateEntity, ex:Drug, ?drugId),
  mgrp:Property(?drugMember, ex:name, ?drugName),
  mgrp:Record(?enzymeMember, mgrp:CreateEntity, ex:Enzyme, ?enzymeId),
  mgrp:Record(?relationMember, mgrp:CreateRelation, ex:InteractsWith, ?relationId),
  mgrp:RelationSource(?relationMember, ?drugId),
  mgrp:RelationTarget(?relationMember, ?enzymeId),
  mgrp:DependsOn(?relationMember, ?drugMember),
  mgrp:DependsOn(?relationMember, ?enzymeMember)
} .
```

`IdentityResolutionPolicy` supplies the three record IDs and member IRIs.
`SourceMappingContract` supplies the name and determines which source row
invokes the recipe. OTTR expands the topology. The assembler orders the two
entities before the relation. The existing structural gate validates all
three writes. No layer silently assumes another layer's responsibility.

## 7. Artifact identities

The protocol keeps these objects distinct:

```text
GraphRecipeSourceArtifact
  = exact stOTTR bytes + media type + source digest

GraphRecipeLibraryLock
  = ordered dependency identities + exact digests

EffectiveGraphRecipe
  = selected root + canonical semantic template closure
    + profile identity + closed terminal ABI

CompiledGraphRecipe
  = EffectiveGraphRecipe + LogicalGraphContract + type binding
    + static validation result

GraphRecipeInvocation
  = CompiledGraphRecipe + canonical typed arguments + expansion profile

RecipeExpansionResult
  = invocation + terminal facts + derivation traces + diagnostics

GraphConstructionPlan
  = expansion results + mappings + transforms + identity + conflict policy
    + sources + backend projection + ordered ProposedOperation values
```

The source digest protects exact evidence. The effective digest identifies
equivalent meaning under the pinned profile. Neither substitutes for the
other. Exact source artifacts and the library lock bind the execution input
set, but source locators, source digests, and lock metadata are deliberately
excluded from `EffectiveGraphRecipe`. This lets byte-level evidence change
without changing semantic identity when the parsed recipe remains equivalent.

The first-slice research runner uses a narrowed `GraphConstructionPlan`
identity containing the logical-contract digest, sorted invocation digests,
complete member graph, and ordered proposed operations. Mapping, transform,
conflict, source, and backend-projection identities enter later experiments.
Until then, the first-slice digest is not the identity of the complete protocol
plan described above.

## 8. Conformance gate before implementation promotion

`OKG-D011` fixes the gate split. The offline Malleus fixture corpus is the
primary required gate. One separate job, after its exact tool lock exists, runs
the pinned Lutra differential oracle. Lutra does not enter the primary Python
matrix or the shipped dependency set.

The complete promotion fixture must include:

1. A pinned positive and negative stOTTR corpus.
2. A frozen effective-recipe canonicalization corpus.
3. Differential expansion results against Lutra 0.6.20 for shared semantics.
4. Hand-authored expected terminal facts for the Malleus base vocabulary.
5. Stable diagnostics for every excluded or invalid construct.
6. Repeated-compilation and permutation tests.
7. Full lineage from source bytes to each proposed operation.
8. Atomic staging tests over the existing graph implementation.
9. One recipe projected to the in-memory graph and one second backend.
10. A recipe revision that forces dependency-closed revalidation and
    replanning.

The research-local offline fixture now implements the bounded `GE-000` through
`GE-020` slice. Its report binds 149 checksummed corpus files, 10 case receipts,
and 7 executable metamorphic obligations. The dedicated slice passed 39 tests.
The relevant core selection passed 236 tests with 2 skips. The report is
identified by
`sha256:9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0`,
and its checksum set is identified by
`sha256:aa5c904f79363b68bab9d82a2b6b027748ffe25358ef3fead5c5ba7b3dc7a3f2`.

Removal of an unused runner import changed the bound runner bytes. The hard
identity guard rejected the stale report and produced retained report identity
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`,
which supersedes
`sha256:41b180b273ecc24e59af769736519c071707134beecf91ae60ce10a1092a1ae0`.
The current refresh binds the changed direct-core and package-boundary bytes and
package version `0.11.0`; its active identity above supersedes the retained
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`
identity. Both dedicated GraphRecipe workflow steps run Ruff over
the complete research-local runner directory before running the 39-test slice.

Each receipt includes the exact selected-manifest source-byte identity in its
canonical payload. Selection is therefore bound to the case result and exact
execution identity. A runner cannot substitute a different manifest while
retaining the same conforming receipt. The report and checksum set bind the
evidence bytes, while semantic digests continue to identify the canonical
logical contract, effective recipe, invocation, plan, candidate, and final
state at their declared boundaries.

This result does not cover `GE-030` or later experiments, Lutra equivalence, a
second backend, dependency-closed evolution, unrestricted OTTR, or public
promotion. The profile remains accepted design, and no GraphRecipe capability
is shipped.

Lutra is a pinned differential oracle, not a shipped dependency decision. Any
tool acquisition must be declared in reproducible project configuration.

## 9. Revisit contract

An accepted `OKG-D001` remains in force until an addressable observation meets
one of these triggers:

1. Two accepted cases require internal value-dependent branching and
   population-level selection causes measured duplication or semantic loss.
2. A required domain needs tuple, map, struct, or term-function semantics that
   scalar, reference, and list values cannot represent faithfully.
3. A required independent consumer must execute recipes on a non-RDF backend
   without the Malleus operation adapter.
4. Mutation, deletion, reverse matching, or merge becomes load-bearing recipe
   behavior rather than evolution behavior.
5. Differential tests expose an irreconcilable semantic disagreement.
6. The profile starts adding grammar, arbitrary expressions, or control flow.
7. A pinned real workload violates its declared scale or determinism budget.
8. A stable OTTR release supplies a relevant missing facility.
9. Positional calls cause repeated measured binding defects.
10. The Malleus base vocabulary blocks a required external OTTR consumer.

A superseding decision must name the trigger evidence, preserve this decision,
and classify every dependent recipe, plan, fixture, public document, and
downstream adoption packet.

## 10. Decision and dependency tuples

These tuples project the accepted `OKG-D001` decision into the Malleus
foundation graph.

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .
@prefix okg: <https://malleus.dev/ontology-kg-realization/> .

okg:OKG-D001 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:selects okg:MalleusGraphRecipeProfileV0 ;
    mfg:rejects okg:NativeMalleusRecipeLanguage ;
    mfg:rejects okg:MultipleRecipeFrontendsV0 ;
    mfg:rejects okg:OTTRFork ;
    mfg:status mfg:AcceptedDesign .

okg:MalleusGraphRecipeProfileV0 rdf:type mfg:NormativeProfile ;
    mfg:dependsOn okg:OTTRFramework2024 ;
    mfg:dependsOn okg:StOTTR-0.1.4 ;
    mfg:dependsOn okg:MOTTR-0.1.2 ;
    mfg:dependsOn okg:ROTTR-0.2.0 ;
    mfg:governs okg:GraphRecipe ;
    mfg:status mfg:AcceptedDesign .

okg:CompiledGraphRecipe
    mfg:dependsOn okg:MalleusGraphRecipeProfileV0 ;
    mfg:dependsOn okg:LogicalGraphContract .

okg:RecipeExpansionResult
    mfg:derivedFrom okg:CompiledGraphRecipe ;
    mfg:dependsOn okg:GraphRecipeInvocation ;
    mfg:produces okg:ConstructionMemberGraph .

okg:ConstructionMemberGraph
    mfg:dependsOn okg:MalleusConstructionBaseVocabulary ;
    mfg:produces okg:ProposedOperationSequence .

okg:GraphRecipeConformanceFixture
    rdf:type mfg:TestObligation ;
    mfg:tests okg:MalleusGraphRecipeProfileV0 ;
    mfg:tests okg:GE-000 ;
    mfg:tests okg:GE-010 ;
    mfg:tests okg:GE-020 ;
    mfg:identifiedBy okg:GraphRecipeFirstSliceChecksumSet ;
    mfg:status mfg:Implemented .

okg:GraphRecipeAdoptionPacket
    mfg:dependsOn okg:MalleusGraphRecipeProfileV0 ;
    mfg:dependsOn okg:GraphRecipeConformanceFixture ;
    mfg:status mfg:Open .
```
