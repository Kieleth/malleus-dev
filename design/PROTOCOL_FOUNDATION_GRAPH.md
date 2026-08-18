# Candidate protocol foundation graph

Status: human-readable projection of candidate and accepted design

Snapshot: `codex/malleus-recon` at
`1657e6564c1f8ab872d56b9ec97e34a015fce765`, inspected on 2026-08-17

Canonical design graph: [`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl),
revision 9,
`sha256:046d20def4c127afecd82811fd19ad8adf2a06e9247373e1fbf7a5dde47a3905`

Authority: the canonical graph records author-accepted and candidate design
states. It has no authority over shipped capability. This note does not change
the public API, ontology, roadmap, implementation status, paper contract, or
execution-bundle design.

The live edits to `ROADMAP.md`, `design/EXECUTION_BUNDLE.md`, and the paper-dojo
worktree were treated as read-only parallel work.

## 1. Candidate conclusion

The first package should be the **contract kernel**.

The missing root object is not another version field. It is a backend-neutral,
content-addressed statement of the semantics that Malleus actually enforces.
This note calls that object an `EffectiveContract`:

```text
EffectiveContract
  = ValidatedContractFactSet
  + NormativeAdmissionProfile
```

`ValidatedContractFactSet` contains normalized, addressable declarative facts
validated under an exact contract metamodel, canonicalization profile, and
symbol-identity policy. `NormativeAdmissionProfile` states the operational
meaning of those facts and the stateful write rules that facts alone do not
express. A separately identified `AdmissionImplementation` executes that
profile and is assessed for conformance through tests. Its code identity belongs in
execution identity, not in the effective contract.

This separation resolves the current ambiguity around ontology, generated
schema, validator, and graph:

```text
contract source bytes
  -> resolver and frontend
  -> ContractCompilationResult
  -> ContractFactSet
  -> metamodel validation and canonicalization
  -> ValidatedContractFactSet
          + NormativeAdmissionProfile
          -> EffectiveContract
              +-> optional schema projections
              +-> conforming admission implementations
              +-> contract-bound graph versions
```

Generated schemas are optional projections. They are not an obligatory stage
between ontology and graph. `OKG-D012` accepts official, execution-identified
LinkML as the sole first-party human-authored frontend for v0, but not as the
runtime contract itself. The `ContractFrontend` boundary remains
language-neutral: a custom implementation may replace LinkML only by producing
the same normative intermediate, diagnostics, and lineage under the same
conformance suite. An adopter should load a compiled
`EffectiveContractArtifact` without installing or invoking LinkML. That is not
current behavior: LinkML packages are mandatory dependencies and
`KnowledgeGraph` requires a concrete `OntologyRegistry`.

This package comes first because every other requested reinforcement needs it:

1. Contract revision needs stable facts to say exactly what changed.
2. Evidence audit needs typed, extensible input and output contracts.
3. Automated authority needs addressable objects and operations to govern.
4. Execution identity needs exact contract identities to freeze.
5. Schema generation needs one semantic source from which to project.
6. Graph storage modularity needs a contract independent of NetworkX.

Effect delivery is downstream of authorization and is unrelated to producer
retry. It should not block this work.

## 2. What exists now

The implemented Python path is:

```text
LinkML-shaped YAML
  -> OntologyRegistry
  -> effective private tables
  -> string-based instance validation
  -> KnowledgeGraph contextual validation
  -> NetworkX materialization
```

The same YAML can also be passed to external LinkML generators, but the graph
does not consume those generated schemas. There is no bound lineage from a
generated JSON Schema, Python model, TypeScript type, or SHACL shape back to
the runtime registry.

`OntologyRegistry` currently combines six jobs:

1. Loading sources and resolving imports.
2. Parsing a bounded LinkML-shaped language.
3. Resolving inheritance, mixins, slot use, enums, and scalar aliases.
4. Building the effective constraint tables.
5. Computing semantic identity and structural fingerprints.
6. Validating instance shape and values.

`KnowledgeGraph` adds stateful admission rules that are not separately
represented in the registry hash. The hash includes relevant classes,
inheritance, slots, endpoint ranges, and the bearer declaration. It does not
identify the operational rules that map named roots to write categories,
enforce one global ID namespace, resolve endpoints against materialized state,
apply the endpoint subtype test, or require an existing signal bearer.
Validation failures are free-text strings.

The current semantic hash is useful but incomplete as a general contract
identity. It hashes enforced registry facts. It intentionally does not hash
source bytes, declared version, descriptions, paths, generated artifacts, or
the additional admission behavior in `KnowledgeGraph`.

The current fingerprints classify set inclusion as `identical`, `superset`,
`subset`, or `divergent`. They do not establish directional writer-to-reader
compatibility, replay compatibility for a concrete graph, affected records, or
a migration.

The implemented facts above are grounded in:

* `src/malleus/ontology.py`, especially registry construction, effective slot
  resolution, `content_hash()`, `fingerprint()`, and `strict_fingerprint()`.
* `src/malleus/kg.py`, especially construction, contextual write validation,
  export, rehydration, and state replacement.
* `src/malleus/staging.py` and `src/malleus/ledger.py`, which require an exact
  ontology hash.
* `docs/IMPLEMENTATION_STATUS.md`, which controls the shipped boundary.

The older generated-registry and multi-backend material in
`docs/KNOWLEDGE_GRAPH_PROTOCOL.md` is design lineage where no matching Python
implementation exists.

## 3. The graph carried by this note

The tuples in this note are a logical design graph. Turtle notation makes each
claim addressable and keeps dependencies explicit. It does not select Turtle,
RDF, an RDF store, or any exact wire format for the future public API.

The graph uses standard RDF terms only where their meaning fits. Malleus terms
carry protocol-specific semantics.

Abstraction kinds such as `EffectiveContract` are declared `rdfs:Class`.
Named candidates such as `SeedMetaContract` are instances. A dependency edge
whose subject is a class states a dependency of that abstraction kind. The
contract-fact example intentionally treats a domain class as both an RDFS class
and an instance of the `ContractClass` metaclass. The seed metamodel must permit
only these declared metamodeling patterns, not arbitrary class-instance
punning.

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .

mfg:Observation rdf:type rdfs:Class .
mfg:Boundary rdf:type rdfs:Class .
mfg:Requirement rdf:type rdfs:Class .
mfg:DesignObject rdf:type rdfs:Class .
mfg:Invariant rdf:type rdfs:Class .
mfg:Package rdf:type rdfs:Class .
mfg:TestObligation rdf:type rdfs:Class .
mfg:ComponentBoundaryConformanceExperiment rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:TestObligation .
mfg:FalsifiableClaim rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .
mfg:DecisionCandidate rdf:type rdfs:Class .
mfg:DecisionRecord rdf:type rdfs:Class .
mfg:DecisionAuthority rdf:type rdfs:Class .
mfg:OpenQuestion rdf:type rdfs:Class .
mfg:DesignStatus rdf:type rdfs:Class .

mfg:Author rdf:type mfg:DecisionAuthority .

mfg:Implemented rdf:type mfg:DesignStatus .
mfg:Partial rdf:type mfg:DesignStatus .
mfg:AcceptedDesign rdf:type mfg:DesignStatus .
mfg:Candidate rdf:type mfg:DesignStatus .
mfg:Open rdf:type mfg:DesignStatus .
mfg:Excluded rdf:type mfg:DesignStatus .

mfg:dependsOn rdf:type rdf:Property .
mfg:motivatedBy rdf:type rdf:Property .
mfg:informedBy rdf:type rdf:Property .
mfg:compiledBy rdf:type rdf:Property .
mfg:produces rdf:type rdf:Property .
mfg:consumes rdf:type rdf:Property .
mfg:composedOf rdf:type rdf:Property .
mfg:derivedFrom rdf:type rdf:Property .
mfg:identifiedBy rdf:type rdf:Property .
mfg:interpretedUnder rdf:type rdf:Property .
mfg:validatedBy rdf:type rdf:Property .
mfg:governedBy rdf:type rdf:Property .
mfg:binds rdf:type rdf:Property .
mfg:tests rdf:type rdf:Property .
mfg:coverageObligation rdf:type rdf:Property .
mfg:counterevidenceFor rdf:type rdf:Property .
mfg:optionalExtensionOf rdf:type rdf:Property .
mfg:distinctFrom rdf:type rdf:Property .
mfg:supersedes rdf:type rdf:Property .
mfg:migratesFrom rdf:type rdf:Property .
mfg:migratesTo rdf:type rdf:Property .
mfg:requiresDecision rdf:type rdf:Property .
mfg:requiredBy rdf:type rdf:Property .
mfg:decidedBy rdf:type rdf:Property .
mfg:decisionDate rdf:type rdf:Property .
mfg:selects rdf:type rdf:Property .
mfg:rejects rdf:type rdf:Property .
mfg:governs rdf:type rdf:Property .
mfg:status rdf:type rdf:Property .
mfg:implements rdf:type rdf:Property .
mfg:subject rdf:type rdf:Property .
mfg:predicate rdf:type rdf:Property .
mfg:object rdf:type rdf:Property .
mfg:valueRange rdf:type rdf:Property .
mfg:onClass rdf:type rdf:Property .
mfg:usesSlot rdf:type rdf:Property .
mfg:required rdf:type rdf:Property .
mfg:multivalued rdf:type rdf:Property .
mfg:sourceContract rdf:type rdf:Property .
mfg:targetContract rdf:type rdf:Property .
mfg:sourceGraphVersion rdf:type rdf:Property .
mfg:targetGraphVersion rdf:type rdf:Property .
mfg:transformationRuleSet rdf:type rdf:Property .
mfg:transformationImplementation rdf:type rdf:Property .
mfg:temporalScope rdf:type rdf:Property .
mfg:outcomePolicy rdf:type rdf:Property .
mfg:targetValidation rdf:type rdf:Property .
mfg:targetLedgerAnchor rdf:type rdf:Property .
```

Status values in this graph mean:

| Status | Meaning |
|---|---|
| `mfg:Implemented` | Present in the pinned code boundary |
| `mfg:Partial` | Some required mechanics exist, but not the named abstraction |
| `mfg:AcceptedDesign` | Author-accepted design direction, not a shipped capability |
| `mfg:Candidate` | Reviewer proposal awaiting author decision |
| `mfg:Open` | Material choice not made |
| `mfg:Excluded` | Deliberately outside the package |

The current pipeline can therefore be recorded without pretending the
candidate design already exists:

```turtle
mfg:CurrentLinkMLShapedSource rdf:type mfg:DesignObject ;
    mfg:compiledBy mfg:CurrentOntologyRegistry ;
    mfg:status mfg:Implemented .

mfg:CurrentOntologyRegistry rdf:type mfg:DesignObject ;
    mfg:produces mfg:CurrentImplicitConstraintTable ;
    mfg:identifiedBy mfg:CurrentRegistryContentHash ;
    mfg:status mfg:Implemented .

mfg:CurrentKnowledgeGraph rdf:type mfg:DesignObject ;
    mfg:consumes mfg:CurrentOntologyRegistry ;
    mfg:validatedBy mfg:CurrentOntologyRegistry ;
    mfg:validatedBy mfg:CurrentGraphAdmissionRules ;
    mfg:status mfg:Implemented .

mfg:CurrentNetworkXMaterialization rdf:type mfg:DesignObject ;
    mfg:status mfg:Implemented .

mfg:CurrentKnowledgeGraph mfg:consumes mfg:CurrentNetworkXMaterialization .

mfg:GeneratedSchemaLineage rdf:type mfg:Boundary ;
    mfg:status mfg:Open .

mfg:CrossContractMigration rdf:type mfg:Boundary ;
    mfg:status mfg:Open .

mfg:CurrentProtocolLedger rdf:type mfg:DesignObject ;
    mfg:binds mfg:ExactOntologyHash ;
    mfg:interpretedUnder mfg:CurrentOntologyRegistry ;
    mfg:status mfg:Implemented .

mfg:CurrentProtocolLedger mfg:distinctFrom mfg:CrossContractMigration .
```

## 4. Contract kernel

### 4.1 Objects and boundaries

| Object | Exact role | Excludes |
|---|---|---|
| `ContractSourceDescriptor` | Digest, length, media type, and locator declared for source bytes | Proof that bytes exist or were read |
| `RetainedContractSource` | Exact bytes read by compilation, retained directly or through a verified blob resolver | Effective semantics |
| `DeclaredModuleMetadata` | Declared name, version, namespace, and stable module IRI | Content identity by itself |
| `ImportClosure` | Entry module, exact resolved source artifacts, and import-label-to-artifact edges | Effective semantics |
| `ContractFrontend` | Compiler from a declared source language | Admission or graph storage |
| `SupportProfile` | Versioned classification and translation of every source construct | Silent acceptance of unknown semantics |
| `ContractCompilationResult` | Entry module, closure, resolver, frontend, support profile, diagnostics, and produced facts | Admission decision |
| `ContractMetamodel` | Legal fact vocabulary and well-formedness rules | Source syntax |
| `FactCanonicalizationProfile` | Canonical fact-record and fact-set serialization | Symbol meaning |
| `SymbolIdentityPolicy` | Qualified symbol and namespace identity | Source-byte identity |
| `ContractFactSet` | Normalized addressable declarative facts | Claim that the facts are well formed |
| `ValidatedContractFactSet` | Fact set accepted under exact metamodel, canonicalization, and symbol policy | Stateful admission behavior |
| `ContractAnnotationSet` | Descriptions, URIs, aliases, and other non-enforcing projection metadata | Admission identity |
| `NormativeAdmissionProfile` | Versioned operational meaning and state-transition rules | One implementation artifact |
| `AdmissionImplementation` | Code implementing one normative profile | Authority to change the profile |
| `DiagnosticProfile` | Violation identity, ordering, and serialization | Graph admissibility |
| `EffectiveContract` | Validated facts interpreted under one normative profile | Source provenance and implementation bytes |
| `EffectiveContractArtifact` | Reloadable canonical runtime artifact for one effective contract | Proof of producer execution |
| `SchemaProjection` | Optional generated consumer artifact plus coverage report | Runtime authority over the graph |
| `StructuralGraphSnapshot` | Immutable structural records under one exact effective contract | Accepted temporal history |
| `AcceptedTemporalGraphVersion` | Contract-bound structural state, temporal metadata, and exact ledger heads | Rewriting old transaction history |

The central tuples are:

```turtle
mfg:ContractSourceDescriptor rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:RetainedContractSource rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:ContractFrontend rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:governedBy mfg:SupportProfile ;
    mfg:status mfg:Candidate .

mfg:SupportProfile rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:DeclaredModuleMetadata rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:ImportClosure rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:ContractMetamodel rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:identifiedBy mfg:ContractMetamodelHash ;
    mfg:status mfg:Candidate .

mfg:FactCanonicalizationProfile rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:identifiedBy mfg:FactCanonicalizationProfileHash ;
    mfg:status mfg:Candidate .

mfg:SymbolIdentityPolicy rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:identifiedBy mfg:SymbolIdentityPolicyHash ;
    mfg:status mfg:Candidate .

mfg:ContractAnnotationSet rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:interpretedUnder mfg:SymbolIdentityPolicy ;
    mfg:status mfg:Candidate .

mfg:ImportResolver rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:CompilationDiagnostics rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:ProjectionProfile rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:ProjectionImplementation rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:ProjectionCoverageReport rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:ContractFactSet rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:ContractCompilationResult rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:binds mfg:DeclaredModuleMetadata ;
    mfg:binds mfg:ImportClosure ;
    mfg:binds mfg:ContractFrontend ;
    mfg:binds mfg:SupportProfile ;
    mfg:binds mfg:ImportResolver ;
    mfg:binds mfg:RetainedContractSource ;
    mfg:binds mfg:CompilationDiagnostics ;
    mfg:produces mfg:ContractFactSet ;
    mfg:produces mfg:ContractAnnotationSet ;
    mfg:status mfg:Candidate .

mfg:ValidatedContractFactSet rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:ContractFactSet ;
    mfg:derivedFrom mfg:ContractCompilationResult ;
    mfg:validatedBy mfg:ContractMetamodel ;
    mfg:interpretedUnder mfg:FactCanonicalizationProfile ;
    mfg:interpretedUnder mfg:SymbolIdentityPolicy ;
    mfg:identifiedBy mfg:ValidatedContractFactSetHash ;
    mfg:status mfg:Candidate .

mfg:LinkMLFrontend rdf:type mfg:ContractFrontend ;
    mfg:status mfg:AcceptedDesign .

mfg:DirectFactFrontend rdf:type mfg:ContractFrontend ;
    mfg:status mfg:Candidate .

mfg:EffectiveContract rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:composedOf mfg:ValidatedContractFactSet ;
    mfg:interpretedUnder mfg:NormativeAdmissionProfile ;
    mfg:identifiedBy mfg:EffectiveContractHash ;
    mfg:status mfg:Candidate .

mfg:AdmissionImplementation rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:implements mfg:NormativeAdmissionProfile ;
    mfg:validatedBy mfg:AdmissionConformanceResult ;
    mfg:identifiedBy mfg:ImplementationArtifactHash ;
    mfg:status mfg:Candidate .

mfg:EffectiveContractArtifact rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:derivedFrom mfg:EffectiveContract ;
    mfg:identifiedBy mfg:EffectiveContractArtifactHash ;
    mfg:status mfg:Candidate .

mfg:SchemaProjection rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:derivedFrom mfg:EffectiveContract ;
    mfg:derivedFrom mfg:ContractAnnotationSet ;
    mfg:governedBy mfg:ProjectionProfile ;
    mfg:compiledBy mfg:ProjectionImplementation ;
    mfg:produces mfg:ProjectionCoverageReport ;
    mfg:identifiedBy mfg:ProjectionArtifactHash ;
    mfg:status mfg:Candidate .

mfg:GraphVersion rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:StructuralGraphSnapshot rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:GraphVersion ;
    mfg:governedBy mfg:GovernedGraphContract ;
    mfg:identifiedBy mfg:StructuralGraphSnapshotHash ;
    mfg:status mfg:Candidate .

mfg:AcceptedTemporalGraphVersion rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:GraphVersion ;
    mfg:governedBy mfg:ContractComposition ;
    mfg:identifiedBy mfg:AcceptedTemporalGraphVersionHash ;
    mfg:status mfg:Candidate .
```

### 4.1.1 Accepted frontend and modularity policy

`OKG-D012` closes the source-policy choice without collapsing the protocol
onto LinkML. The first-party v0 authoring surface is deliberately narrow:
LinkML source, interpreted by an exact official compiler under a versioned,
fail-closed Malleus support profile. Direct facts remain an independently
authored bootstrap and conformance input, not a second first-party authoring
language.

The protocol boundary is deliberately broader than the first-party product
surface. A `ContractFrontend` receives retained source bytes, an explicit
resolver, and a support profile. It emits a `ContractCompilationResult` with
contract facts, annotations, typed diagnostics, and complete lineage. It
receives no graph handle and performs no admission. A custom frontend may
replace LinkML only if the frontend-neutrality suite establishes identical
normative output and downstream behavior for the claimed profile. The default
implementation receives no bypass or hidden semantic privilege.

The accepted Malleus Unix modularity doctrine governs the whole library-protocol
architecture; this frontend boundary is its first concrete application. The
doctrine adapts Eric S. Raymond's *The Art of Unix Programming*: small stages,
artifact-mediated composition, policy-mechanism separation, inspectable state,
knowledge represented as data, deterministic generation, fail-loud repair, and
explicit extension. For Malleus, permissive repair never means semantic
guessing. Only declared, deterministic, lossless, provenance-recorded
normalization is admissible; unknown or ambiguous meaning rejects before
effects.

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .
@prefix okg: <https://malleus.dev/ontology-kg-realization/> .

mfg:TheArtOfUnixProgramming rdf:type mfg:Observation ;
    rdfs:seeAlso <https://www.catb.org/esr/writings/taoup/html/> .

mfg:MalleusLibraryProtocolArchitecture rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

mfg:UnixModularProtocolDoctrine rdf:type mfg:DesignObject ;
    mfg:informedBy mfg:TheArtOfUnixProgramming ;
    mfg:governs mfg:MalleusLibraryProtocolArchitecture ;
    mfg:governs mfg:ContractFrontend ;
    mfg:governs mfg:AdmissionImplementation ;
    mfg:status mfg:AcceptedDesign .

mfg:ReplaceableContractFrontendBoundary rdf:type mfg:Boundary ;
    mfg:governedBy mfg:UnixModularProtocolDoctrine ;
    mfg:tests mfg:FrontendParity ;
    mfg:status mfg:AcceptedDesign .

mfg:MalleusLinkMLSupportProfileV0 rdf:type mfg:SupportProfile ;
    mfg:status mfg:Candidate .

mfg:FrontendConformanceSuite rdf:type mfg:TestObligation ;
    mfg:tests mfg:FrontendParity ;
    mfg:status mfg:Candidate .

mfg:LinkMLFrontend
    mfg:governedBy mfg:MalleusLinkMLSupportProfileV0 ;
    mfg:validatedBy mfg:FrontendConformanceSuite .

mfg:CustomContractFrontend rdf:type mfg:ContractFrontend ;
    mfg:optionalExtensionOf mfg:ReplaceableContractFrontendBoundary ;
    mfg:validatedBy mfg:FrontendConformanceSuite ;
    mfg:status mfg:Candidate .

mfg:DirectFactBootstrapUse rdf:type mfg:Boundary ;
    mfg:governs mfg:DirectFactFrontend ;
    mfg:status mfg:AcceptedDesign .

mfg:LinkMLFreeCompiledContractRuntime rdf:type mfg:Invariant ;
    mfg:dependsOn mfg:EffectiveContractArtifact ;
    mfg:status mfg:AcceptedDesign .

mfg:PrivilegedContractFrontend rdf:type mfg:DesignObject ;
    mfg:status mfg:Excluded .

okg:OKG-D012 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:selects mfg:LinkMLFrontend ;
    mfg:selects mfg:ReplaceableContractFrontendBoundary ;
    mfg:selects mfg:DirectFactBootstrapUse ;
    mfg:selects mfg:LinkMLFreeCompiledContractRuntime ;
    mfg:selects mfg:UnixModularProtocolDoctrine ;
    mfg:rejects mfg:PrivilegedContractFrontend ;
    mfg:status mfg:AcceptedDesign .
```

Current `KnowledgeGraph.state_digest()` is closest to the structural-snapshot
role: it hashes the ontology identity plus materialized nodes and relations.
It does not hash accepted valid-time metadata, supersession links, transaction
coordinates, acceptance head, or materialization head. Those appear in
separate accepted-view structures today. The two candidate graph-version
classes make that split explicit rather than assigning bitemporal meaning to
the current state digest.

`ContractSourceDescriptor` deliberately differs from the current meaning of a
core `SourceArtifact`. A descriptor records caller-declared digest and length.
A compilation result must additionally bind the exact retained bytes it read
and the resolver that supplied them.

The support profile classifies every field at every supported source-language
location as `ENFORCED`, `ANNOTATION_ONLY`, `IDENTITY_ONLY`, or `REJECTED`.
Unknown fields reject. This allows descriptions to remain useful without
silently dropping fields such as patterns, unions, cardinality, inlining, or
URIs whose semantics an adopter may reasonably expect to be enforced.

The contract metamodel owns legal fact kinds, well-formedness, acyclicity,
known ranges, mixin resolution, relation signatures, scalar kinds, and legal
role assignments. The symbol policy owns qualified identity. Current imports
merge bare names into one global namespace and reject duplicates, which is not
enough for neutral module composition. Declared name plus version remains
metadata; stable module IRI plus qualified local symbol forms the candidate
symbol key.

Annotations remain linked to their compilation and symbols but do not enter
admission identity. A projection consumes the effective contract, optional
annotations, a projection profile, and a projection implementation. Its
coverage report states which normative admission rules cannot be expressed in
the target artifact.

The validated fact-set hash envelope covers the exact contract-metamodel hash,
fact-canonicalization-profile hash, symbol-identity-policy hash, and ordered
canonical fact-record digest. Annotation bytes are excluded from this semantic
hash and remain bound through compilation and projection lineage.

### 4.2 Why normative admission is separate

The fact set should contain every data-independent declarative constraint. It
can state that a slot is required, has a range, is multivalued, or belongs to a
class. It cannot, by itself, settle all operational meaning.

The fact set owns contract-selectable declarations:

1. Which classes occupy entity, relation, signal, and event roles.
2. Which slots are references and which target types they permit.
3. Relation endpoint and signal bearer constraints.
4. Contract-selected operation repertoire and namespace policy.

The normative admission profile owns evaluation semantics:

1. Whether records are closed to unknown fields.
2. Missing, null, and empty-value semantics.
3. Primitive lexical and numeric evaluation.
4. When references are resolved and which prestate is consulted.
5. Create-only, staging, atomicity, and state-transition rules.
6. How subtype and reference checks use the fact set.

For parity with current behavior, its first conformance profile must cover at
least these mechanics: absent, `None`, empty string, and empty list handling;
optional `None`; UTF-8 keys and strings; boolean exclusion from numeric kinds;
finite floats; datetime values with a time component; lexical LinkML kinds
currently treated as base strings; reserved positional fields; abstract-class
instantiation; global ID uniqueness; contextual endpoint and bearer lookup;
and candidate atomicity.

Violation ordering and serialization belong to a separate
`DiagnosticProfile`. A diagnostic-format change must not force a graph contract
migration when admission semantics are unchanged.

An opaque normative profile would only move the current ambiguity. It needs
addressable rules and a conformance suite. Implementations identify the exact
code that executed those rules. The effective contract hash binds the
validated fact-set hash and normative-profile hash, not implementation bytes.

```turtle
mfg:NormativeAdmissionProfile rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:composedOf mfg:AdmissionRuleSet ;
    mfg:identifiedBy mfg:NormativeAdmissionProfileHash ;
    mfg:status mfg:Candidate .

mfg:AdmissionConformanceResult rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:binds mfg:AdmissionImplementation ;
    mfg:binds mfg:NormativeAdmissionProfile ;
    mfg:binds mfg:AdmissionConformanceSuite ;
    mfg:status mfg:Candidate .

mfg:DiagnosticProfile rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:identifiedBy mfg:DiagnosticProfileHash ;
    mfg:status mfg:Candidate .

mfg:ValidationAttestation rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:binds mfg:EffectiveContract ;
    mfg:binds mfg:AdmissionImplementation ;
    mfg:binds mfg:AdmissionConformanceResult ;
    mfg:binds mfg:DiagnosticProfile ;
    mfg:status mfg:Candidate .

mfg:EffectiveContractHash mfg:binds mfg:ValidatedContractFactSetHash .
mfg:EffectiveContractHash mfg:binds mfg:NormativeAdmissionProfileHash .
mfg:ValidatedContractFactSetHash mfg:binds mfg:ContractMetamodelHash .
mfg:ValidatedContractFactSetHash mfg:binds mfg:FactCanonicalizationProfileHash .
mfg:ValidatedContractFactSetHash mfg:binds mfg:SymbolIdentityPolicyHash .
mfg:ValidatedContractFactSetHash mfg:binds mfg:OrderedCanonicalFactsDigest .
mfg:StructuralGraphSnapshotHash mfg:binds mfg:GovernedGraphContractHash .
mfg:StructuralGraphSnapshotHash mfg:binds mfg:CanonicalStructuralStateHash .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:ContractCompositionHash .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:CanonicalStructuralStateHash .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:TemporalMetadataDigest .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:SourceProtocolLedgerHead .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:AcceptanceHead .
mfg:AcceptedTemporalGraphVersionHash mfg:binds mfg:MaterializationHead .
```

### 4.3 Contract facts

Facts require stable identities because diagnostics, changes, authority, and
migrations must cite them. Class slot use is reified because a global slot and
its class-specific use can enforce different constraints.

The candidate identity rule is a reified `ContractFact` record with canonical
subject, predicate, and object fields. Its ID is a domain-separated digest over
the contract-metamodel identity, fact-canonicalization profile, symbol-identity
policy, and canonical fact record. The Turtle shown here is a readable
projection. Bare triple bytes alone are not the identity rule.

The following is an example of logical meaning, not the selected wire format:

```turtle
mfg:ContractClass rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .

mfg:ContractSlot rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .

mfg:SlotUse rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .

mfg:ContractFact rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .

mfg:Claim rdf:type rdfs:Class .
mfg:Claim rdf:type mfg:ContractClass .
mfg:Claim rdfs:subClassOf mfg:Entity .

mfg:ClaimSubclassFact rdf:type mfg:ContractFact .
mfg:ClaimSubclassFact mfg:subject mfg:Claim .
mfg:ClaimSubclassFact mfg:predicate rdfs:subClassOf .
mfg:ClaimSubclassFact mfg:object mfg:Entity .

mfg:text rdf:type mfg:ContractSlot .
mfg:text mfg:valueRange mfg:String .

mfg:ClaimTextUse rdf:type mfg:SlotUse .
mfg:ClaimTextUse mfg:onClass mfg:Claim .
mfg:ClaimTextUse mfg:usesSlot mfg:text .
mfg:ClaimTextUse mfg:required true .
mfg:ClaimTextUse mfg:multivalued false .
```

Required invariants:

```turtle
mfg:FactCompleteness rdf:type mfg:Invariant ;
    mfg:status mfg:Candidate .

mfg:FactCompleteness mfg:requiresDecision mfg:UnsupportedSemanticsPolicy .

mfg:UnsupportedSemanticsPolicy rdf:type mfg:DecisionCandidate ;
    mfg:status mfg:Candidate .

mfg:StableFactIdentity rdf:type mfg:Invariant ;
    mfg:status mfg:Candidate .

mfg:FrontendParity rdf:type mfg:Invariant ;
    mfg:tests mfg:EquivalentFrontendConformance ;
    mfg:status mfg:Candidate .

mfg:ProjectionNonAuthority rdf:type mfg:Invariant ;
    mfg:status mfg:Candidate .
```

Their meanings are:

1. Every enforced declarative semantic appears in the fact set.
2. Every source construct is explicitly classified by its support profile.
   Unknown or rejected constructs fail compilation.
3. Equivalent validated fact sets have one canonical identity regardless of
   frontend.
4. Two frontends producing the same validated fact set under the same
   normative profile produce the same effective contract identity and
   admission behavior through conforming implementations.
5. A generated projection cannot add a runtime semantic absent from its source
   effective contract. Its projection profile, implementation, annotations,
   and coverage report remain separately bound.

### 4.4 Identities that must not collapse

```text
declared module metadata and stable module IRI
source descriptor hash
retained source byte hash
resolved import-closure hash
frontend implementation identity
support-profile identity
contract-metamodel identity
fact-canonicalization-profile identity
symbol-identity-policy identity
validated-contract-fact-set hash
normative-admission-profile hash
effective-contract hash
effective-contract-artifact hash
admission-implementation artifact hash
diagnostic-profile hash
projection artifact hash
structural-graph-snapshot hash
accepted-temporal-graph-version hash
protocol-ledger head
```

Equal digest payloads never imply equal roles or substitutability. Hash
envelopes must be domain-separated by artifact kind and identity version. For
example, a description-only YAML edit changes source bytes and annotations but
can leave the effective contract unchanged. A normative validator-semantic
change changes the profile and effective contract. A conforming implementation
replacement changes execution identity but not the effective contract.

### 4.5 Typed violations

Free-text errors are insufficient for dependency analysis, correction, or
migration. Typed violations span these phases:

```text
SOURCE_PARSE
IMPORT_RESOLUTION
PROFILE_CONFORMANCE
CONTRACT_WELL_FORMEDNESS
RECORD_SHAPE
GRAPH_CONTEXT
MIGRATION
```

A violation should carry the applicable subset of:

```text
violation ID
stable code
severity
phase
source artifact, module, source path, and location
operation and write position
focus record ID and property path
offending value or value digest
expected constraint
source contract fact ID, optional
source admission rule ID, optional
admission prestate or graph-version ID
effective contract ID
```

At least one governing contract fact or admission rule is required for record
admission failures. Compilation failures can instead bind source location,
support-profile rule, metamodel rule, or import-resolution rule. Human text
remains a projection from the typed record.

```turtle
mfg:TypedViolation rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:binds mfg:ContractFact ;
    mfg:binds mfg:AdmissionRule ;
    mfg:binds mfg:EffectiveContract ;
    mfg:status mfg:Candidate .

mfg:TypedViolationProtocol rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:status mfg:Candidate .
```

### 4.6 Contract composition boundary

Current Assent uses one resolved registry for both protocol records and the
accepted domain graph. A domain-only ontology change therefore changes the
same identity that gates protocol replay. Modular evolution needs distinct
roles even if the first implementation composes them into one artifact:

```turtle
mfg:ProtocolRecordContract rdf:type mfg:EffectiveContract ;
    mfg:status mfg:Candidate .

mfg:GovernedGraphContract rdf:type mfg:EffectiveContract ;
    mfg:status mfg:Candidate .

mfg:GovernanceContract rdf:type mfg:EffectiveContract ;
    mfg:status mfg:Candidate .

mfg:ContractComposition rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:binds mfg:ProtocolRecordContract ;
    mfg:binds mfg:GovernedGraphContract ;
    mfg:binds mfg:GovernanceContract ;
    mfg:identifiedBy mfg:ContractCompositionHash ;
    mfg:status mfg:Open .

mfg:GovernedGraphContract mfg:identifiedBy mfg:GovernedGraphContractHash .
mfg:GovernedGraphContractHash mfg:binds mfg:EffectiveContractHash .
mfg:ContractCompositionHash mfg:binds mfg:ProtocolRecordContractHash .
mfg:ContractCompositionHash mfg:binds mfg:GovernedGraphContractHash .
mfg:ContractCompositionHash mfg:binds mfg:GovernanceContractHash .
```

The open decision is whether one ledger epoch continues to bind one composed
contract hash, or whether protocol and governed-graph evolution receive
separate but cross-bound heads. The current exact-hash invariant must not be
weakened implicitly while making that split.

Contract evolution is blocked on this choice. The migration design below uses
`GovernedGraphContract` for a structural-only graph and `ContractComposition`
for an accepted temporal graph plus protocol ledger. It does not assume that a
domain-only change must always replace the protocol-record contract in the
future split topology.

## 5. Contract and graph revision

Revision is several different transitions. Treating all of them as “ontology
versioning” hides the required work.

| Change | Effective contract | Required action |
|---|---|---|
| Non-semantic source edit classified by the support profile, such as formatting, comments, or non-enforcing descriptions | Unchanged | Record new source, closure, annotations, and compilation provenance; no graph migration |
| Declared module metadata only | Unchanged | Record module lineage; no graph migration |
| Projection generator or output only | Unchanged | Regenerate and validate that projection |
| Direct structural append under the same contract | Unchanged | Use the create-only structural gate; no Assent decision is implied |
| Accepted graph append under the same contract | Unchanged | Use candidate, epistemic decision, and accepted application |
| Proposal revision | Unchanged | Create proposal lineage only; it does not replace a claim or graph record |
| Accepted claim replacement | Unchanged | Use `ClaimRevision` and the current-claim pointer |
| Accepted graph-record replacement | Unchanged | Use temporal supersession with the same operation family and exact record type |
| Contract facts change | Changed | Compute a typed change set, compatibility, impact, and migration plan |
| Normative admission semantics change | Changed | Revalidate all affected graph state, even if facts match |
| Any governed-graph contract identity change | Changed | Create a new structural graph version; compatibility controls reuse or transformation |
| Any contract-composition identity change on the accepted-temporal path | Changed | Start a new ledger epoch under the exact-hash boundary; compatibility does not relax ledger admissibility |
| Evidence, policy, rules, producer, or runtime change | Maybe unchanged | Create new bound artifacts and execution identity |

Today the ledger binds one combined registry ontology hash, not the candidate
contract composition. A code change to currently hardcoded admission behavior
can therefore alter semantics without changing the bound hash. The candidate
identity closes that seam. On the accepted-temporal path, any bound
contract-composition hash change starts a new ledger epoch. A standalone
structural graph has no protocol-ledger requirement. A behavior-preserving
admission-implementation change affects execution identity and conformance
evidence, not the effective contract.

Current Malleus already supplies useful substrate:

1. Semantic ontology hashes.
2. Narrow structural fingerprint comparisons.
3. Deterministic structural export plus all-or-nothing structural rehydration
   under a supplied registry.
4. Isolated candidate staging and stale-base refusal.
5. Distinct immutable claim, proposal, action, and graph-record revision
   lineages with different fork rules.
6. Half-open valid-time intervals and transaction-time projection.
7. Exact ontology binding within one protocol ledger.

`KnowledgeGraph.export_records()` carries structural records only. It does not
carry accepted temporal metadata, applications, acceptance or materialization
heads, audit history, or protocol events. Rehydration can test structural
replay compatibility. It is not accepted-graph migration or protocol-ledger
migration.

Current revision ancestry is not uniform. Accepted claim replacement follows
the current-claim pointer. Action and graph-record revision prevent lineage
forks under their own rules. Proposal revision requires a terminal direct
predecessor and contiguous revision number, but does not maintain a
latest-by-key pointer that prevents two direct successors. A future generic
`RevisionAncestry` cannot erase these differences.

It does not supply contract diffs, impact analysis, transforms, cross-contract
graph lineage, typed retraction, dependency-closed invalidation, migration
records, or a migrated ledger.

### 5.1 Migration objects

```turtle
mfg:ContractChangeSet rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:sourceContract mfg:EffectiveContract ;
    mfg:targetContract mfg:EffectiveContract ;
    mfg:status mfg:Candidate .

mfg:DependencyIndex rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:dependsOn mfg:StableFactIdentity ;
    mfg:dependsOn mfg:TypedDependencyKind ;
    mfg:dependsOn mfg:ContractValidationFootprint ;
    mfg:status mfg:Candidate .

mfg:ImpactSet rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:derivedFrom mfg:ContractChangeSet ;
    mfg:derivedFrom mfg:DependencyIndex ;
    mfg:status mfg:Candidate .

mfg:MigrationPlan rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:sourceGraphVersion mfg:GraphVersion ;
    mfg:sourceContract mfg:EffectiveContract ;
    mfg:targetContract mfg:EffectiveContract ;
    mfg:transformationRuleSet mfg:TransformationRuleSet ;
    mfg:transformationImplementation mfg:TransformationImplementation ;
    mfg:temporalScope mfg:MigrationTemporalScope ;
    mfg:outcomePolicy mfg:MigrationOutcomePolicy ;
    mfg:dependsOn mfg:ImpactSet ;
    mfg:status mfg:Candidate .

mfg:MigrationResult rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:binds mfg:MigrationPlan ;
    mfg:targetValidation mfg:MigrationValidationResult ;
    mfg:status mfg:Candidate .

mfg:StructuralMigrationResult rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:MigrationResult ;
    mfg:targetGraphVersion mfg:StructuralGraphSnapshot ;
    mfg:status mfg:Candidate .

mfg:AcceptedTemporalMigrationResult rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:MigrationResult ;
    mfg:targetGraphVersion mfg:AcceptedTemporalGraphVersion ;
    mfg:targetLedgerAnchor mfg:ProtocolLedgerAnchor ;
    mfg:status mfg:Candidate .

mfg:TransformationRuleSet rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .

mfg:TransformationImplementation rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .

mfg:MigrationTemporalScope rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .

mfg:MigrationOutcomePolicy rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .

mfg:MigrationValidationResult rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .

mfg:ProtocolLedgerAnchor rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject .
```

Every source record in a migration must receive one explicit outcome:

```text
RETAINED
TRANSFORMED
RETIRED_AT_CUTOVER
QUARANTINED
REJECTED
```

Source disposition and pre-migration temporal state are separate. A source
record already superseded before migration is not thereby
`RETIRED_AT_CUTOVER`.

The mapping is bidirectionally accountable:

1. Every source record has exactly one disposition.
2. `RETAINED` names one byte-equivalent target record. `TRANSFORMED` names one
   or more target records and field-level transforms or omissions.
   `RETIRED_AT_CUTOVER`, `QUARANTINED`, and `REJECTED` name no target record.
3. Every target record names one or more source records or an explicit,
   authorized introduction.
4. Quarantine and rejection name a reason, retained artifact identity, and
   whether the outcome policy permits migration success.
5. No missing required value is invented. No record or field disappears
   without a disposition and reason.

The migration plan declares one temporal scope:

```text
STRUCTURAL_SNAPSHOT
CUTOVER_VALID_VIEW
COMPLETE_VALID_TIME_HISTORY
```

For complete-history migration, every valid-time interval and supersession
edge is transformed and validated. A result cannot claim
`COMPLETE_VALID_TIME_HISTORY` if any in-scope record, interval, or lineage edge
lacks a target representation. Such a result is partial, quarantined, or
failed according to the outcome policy.

For cutover migration, every target valid-time interval begins at or after the
cutover. Original pre-cutover intervals remain only in the source binding and
source ledger. A target ledger never rewrites source transaction times as its
own history. It anchors the exact source ledger head, source graph heads,
migration result, and cutover event.

Target validation includes structural replay, temporal-interval and
supersession-lineage checks when applicable, referential closure for every
declared valid-time view or cutover, structural and temporal digests, and a
protocol binding to the migration result for accepted-temporal migration.

The target is built in isolation and committed as a new graph version.
Structural migration produces a structural snapshot and does not require an
Assent ledger. Accepted-temporal migration additionally starts a target ledger
epoch and binds its anchor. The old graph and any old ledger remain immutable.
Historical projection of the old version is implemented. Making an old version
current again would require a new recorded and authorized transition; that
selector is candidate behavior, not current rollback support.

### 5.2 Compatibility is directional and use-specific

At least three questions must remain distinct:

1. **Contract relation:** which facts were added, removed, or changed?
2. **Writer-to-reader compatibility:** can values written under contract A be
   consumed under contract B for a declared operation and direction?
3. **Structural replay compatibility:** do these exact structural records
   revalidate under B?
4. **Accepted-history compatibility:** do the declared temporal scope,
   supersession lineage, and referential views revalidate under B?

An abstract inclusion label cannot answer all four. A result must bind its
direction, purpose, algorithm, source and target identities, result, reasons,
and counterexample or affected facts when available.

### 5.3 Dependency-closed change

`ClaimVersion.dependency_ids` exists today, but core does not resolve those
IDs, reject cycles, build reverse dependencies, mark dependents stale, or
schedule revalidation. Relation endpoints and source lineage are stronger but
still do not form a general repair graph.

The dependency index needs typed edges because different edges propagate
differently:

```text
STRUCTURAL_REFERENCE
PROVENANCE
EPISTEMIC_JUSTIFICATION
TEMPORAL_SUPERSESSION
CONTRACT_VALIDATION_FOOTPRINT
```

Superseding evidence does not automatically invalidate every provenance
descendant. A structural endpoint failure and an epistemic justification
failure also require different states and repair policies. Each dependency
kind therefore declares its resolution, cycle, invalidation, and revalidation
semantics.

Accepted records need a contract-validation footprint that either stores or
deterministically reconstructs the exact facts and admission rules used to
admit them. Typed violations cover rejected writes only. Without footprints
for valid records, a changed slot rule cannot yield a complete impact set.

Each dependency kind must either be acyclic or declare strongly-connected
component behavior. Closure over an allowed cycle operates on the whole
component. A cycle cannot be left to traversal accident.

The first revision work should therefore build dependency identity and impact
analysis before automatic repair. A local retry without dependency closure can
leave accepted downstream records semantically stale.

```turtle
mfg:ContractEvolution rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:dependsOn mfg:ContractComposition ;
    mfg:dependsOn mfg:TypedViolationProtocol ;
    mfg:dependsOn mfg:ReferenceDependencySemantics ;
    mfg:status mfg:Candidate .

mfg:DependencyClosedRevision rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractEvolution ;
    mfg:status mfg:Candidate .
```

## 6. Optional evidence-integrity audit

Evidence integrity is not one check. It contains deterministic and
producer-mediated stages with different claims.

```text
source locator
  -> byte resolution
  -> byte digest and length verification
  -> quote or span verification
  -> typed extraction
  -> separately identified adversarial review
  -> policy-selected evidence state
```

The user’s existing extractor plus adversarial checker pattern fits as one
`AuditWorkflowProfile`. It should be configurable, not built into the base
protocol. Other profiles may use deterministic checks only, more witnesses, a
human reviewer, or a domain-specific verifier.

Each audit stage must bind:

1. Exact input and output contracts.
2. Source artifact and, when available, verified source bytes.
3. Actor or implementation identity.
4. Prompt, tool, producer, rule, and budget identities where applicable.
5. Result and typed failures.
6. Predecessor stage and workflow profile.

The stages establish different properties:

* Digest verification establishes that inspected bytes match a digest.
* Span verification establishes that a cited span occurs in those bytes.
* Extraction review assesses whether a structured claim is grounded and
  whether material qualifiers were lost.
* None of these establishes that the source claim is true.

The audit emits typed stage results. They cannot silently become core
assessments. Core assessment kinds are currently closed to `TYPE`,
`EVIDENCE_COMPLETENESS`, `CONFLICT`, `UNCERTAINTY`, `LOGICAL`, `TEMPORAL`, and
`AUTHORITY`. Extraction grounding and adversarial review are not automatically
equivalent to `EVIDENCE_COMPLETENESS`. Integration therefore requires an
explicit mapping into a concrete existing monitor contract or an authorized
new assessment kind.

Core epistemic verdicts are exactly `ACCEPT`, `REJECT`, `DEFER`, and `CONTEST`.
A declared epistemic policy maps complete core assessments to one of those
verdicts. Audit-profile workflow states remain a separate layer. The checker
does not approve its own result.

Resolver failure, unavailable bytes, checker failure, timeout, and malformed
output are unavailable observations, not negative evidence. An Assent adapter
must record the applicable `MonitorFailure` and `UnavailableAssessment`, which
drives the precommitted `UNKNOWN` mapping.

```turtle
mfg:EvidenceIntegrityProfile rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:optionalExtensionOf mfg:AssentProtocol ;
    mfg:status mfg:Candidate .

mfg:TwoActorAuditWorkflow rdf:type mfg:EvidenceIntegrityProfile ;
    mfg:dependsOn mfg:TypedExtractionStage ;
    mfg:dependsOn mfg:AdversarialReviewStage ;
    mfg:dependsOn mfg:AuditStageExecutionIdentity ;
    mfg:status mfg:Candidate .

mfg:EvidenceChangePropagation rdf:type mfg:Package ;
    mfg:dependsOn mfg:EvidenceIntegrityPackage ;
    mfg:dependsOn mfg:DependencyClosedRevision ;
    mfg:status mfg:Candidate .
```

Current core records caller-declared source digest and length. `SourceArtifact`
can be constructed from exact bytes, but protocol replay does not retrieve or
authenticate those bytes and does not verify quote spans. The optional audit
must state where bytes came from and what the resolver is trusted to do.

“Separately identified” is deliberate. Bare actor IDs, implementation IDs,
prompts, and executions make separation inspectable. They do not authenticate
actors or prove organizational, provider, or implementation independence.

## 7. Automated authority, not enterprise identity

The in-scope policy question is:

> Which recorded automated actor may propose, approve, migrate, or apply which
> typed change to which governed object, under which contract and time scope?

This is not enterprise IAM, login, organization membership, or proof that a
caller really controls an actor ID.

Current policy substrate must remain visible. Malleus implements typed
authorization-policy artifacts, deterministic authorization evaluation, and
validation of an assessed sufficient grant on `AUTHORIZE`. It does not run
authority monitors through `AssentPlan`, establish policy legitimacy or
applicability, authenticate actors, or establish a grantor trust root.

Current policies are ontology-typed protocol-ledger artifacts. They are not
derived from or materialized as records in the accepted domain graph. A
protected governance partition or separate governance graph is a new
topology, not a description of current behavior.

A graph-carried authority policy needs at least:

```text
policy identity and version
governed operation
governed contract facts, modules, graph partitions, or predicates
actor or actor class
allowed transition
effective interval
authorizing policy or trust root
supersession lineage
```

Policy representation in a KG is feasible. Policy legitimacy does not emerge
from representation. If the same graph can freely change the policy that
authorizes graph changes, it can authorize its own takeover.

Two topologies remain open:

| Topology | Benefit | Required guardrail |
|---|---|---|
| Protected governance partition in the accepted graph | One graph and query surface | Non-self-amendment rule enforced outside ordinary writes |
| Separate governance graph | Cleaner trust and change boundary | Explicit synchronization and binding to governed graph heads |

Both require a bootstrap trust root or genesis policy outside ordinary policy
amendment. Malleus currently records actor IDs and authorization decisions but
does not authenticate actors or establish grantor legitimacy.

```turtle
mfg:AutomatedChangeAuthority rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:dependsOn mfg:GovernedChangeOperation ;
    mfg:dependsOn mfg:GovernanceBootstrap ;
    mfg:status mfg:Candidate .

mfg:TypedAuthorizationPolicy rdf:type mfg:DesignObject ;
    mfg:status mfg:Implemented .

mfg:DeterministicAuthorizationEvaluation rdf:type mfg:DesignObject ;
    mfg:status mfg:Implemented .

mfg:AuthorityGrantValidation rdf:type mfg:DesignObject ;
    mfg:status mfg:Implemented .

mfg:AuthorityMonitorOrchestration rdf:type mfg:Boundary ;
    mfg:status mfg:Open .

mfg:PolicyAuthorityScope rdf:type mfg:Boundary ;
    mfg:status mfg:Open .

mfg:ActorAuthentication rdf:type mfg:Boundary ;
    mfg:status mfg:Excluded .

mfg:GovernancePolicyGraph rdf:type mfg:DesignObject ;
    mfg:governedBy mfg:GovernanceBootstrap ;
    mfg:status mfg:Open .

mfg:GovernanceTopology rdf:type mfg:OpenQuestion ;
    mfg:status mfg:Open .
```

## 8. Three correction mechanisms and one unrelated delivery mechanism

The following must not share one “retry” abstraction:

| Mechanism | Repeats logical payload? | New recorded attempt? | New epistemic proposal? | Changes accepted knowledge? |
|---|---:|---:|---:|---:|
| Transport retry | Yes | Yes | No | No |
| Producer revision from diagnostics | No | Yes | Yes | Not by itself |
| Knowledge revision | No | Yes | Yes | Yes, after decision and application |
| External effect redelivery or reconciliation | Maybe | Yes | No | Concerns external state |

The reusable producer-revision path is:

```text
GenerationAttempt
  -> ProducerResponse
  -> TypedDiagnosticPacket
  -> RevisionProposal
  -> Recheck
  -> TerminalOutcome
```

Each revision is a new attempt with ancestry and budget consumption. Transport
retry repeats an interrupted call and needs its own identity and count.

Core implements immutable proposal revision lineage plus typed assessments,
checks, and witnesses. Research adapters serialize those records into
diagnostic feedback packets. Earlier research-local experiments show that a
bounded second producer call can use diagnostics to repair residual proposals.
The active paper’s current P1 path is offline and receives authored revisions
as input. These facts support the abstraction but do not establish a generic
current end-to-end producer loop.

Effect delivery means the crash and duplication boundary after an authorized
external action:

```text
AuthorizationDecision
  -> ActionDispatch
  -> ActionExecution
  -> OutcomeObservation
```

It is unrelated to extraction retry or producer correction. Core records this
path but executes and observes nothing. Delivery reliability can remain an
optional adopter profile once an adopter states its external delivery and
recovery assumptions.

The `Partial` status means that dispatch, one terminal receipt per dispatch,
and separately attributed outcome-observation records are implemented.
External idempotency, durable outbox, target-side deduplication, reconciliation,
and exactly-once delivery remain open.

```turtle
mfg:ProducerCorrection rdf:type mfg:Package ;
    mfg:dependsOn mfg:TypedViolationProtocol ;
    mfg:dependsOn mfg:ProposalRevisionLineage ;
    mfg:status mfg:Partial .

mfg:ProposalRevisionLineage rdf:type mfg:DesignObject ;
    mfg:status mfg:Implemented .

mfg:CurrentActionAuthorization rdf:type mfg:DesignObject ;
    mfg:status mfg:Implemented .

mfg:EffectDelivery rdf:type mfg:Package ;
    mfg:dependsOn mfg:CurrentActionAuthorization ;
    mfg:optionalExtensionOf mfg:AssentProtocol ;
    mfg:status mfg:Partial .

mfg:ProducerCorrection mfg:distinctFrom mfg:EffectDelivery .
```

## 9. Execution identity

The existing execution-bundle design already separates nine roles:

```text
CORE_CODE
EXECUTOR_CODE
SCHEMA_ONTOLOGY
GOVERNANCE
CORPUS
PRODUCER
INTERACTION
RUNTIME
BUDGET
```

The current paper-local P2 preparation pins the Malleus 0.9 `CORE_CODE`
distribution and keeps the Malleus 0.10 Recon research tool outside the paper
execution substrate. It does not yet contain a P2 attempt, complete nine-role
bundle, role-manifest set, gate record, authorization, execution realization,
or run. The general protocol object remains design-only.

The contract kernel makes the `SCHEMA_ONTOLOGY` role precise. A realization
can separately bind:

```text
source artifacts and import closure
compilation result, frontend, and support profile
contract metamodel, canonicalization, and symbol policy
validated contract fact set
normative admission profile and admission implementation
diagnostic profile and validation attestation
effective contract
effective-contract artifact actually loaded
schema projections actually consumed
source and target graph versions
migration plan and result, when present
```

Execution identity packages these identities. It cannot define their meaning,
which is why it follows the contract kernel.

```turtle
mfg:ExecutionIdentity rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractIdentity ;
    mfg:binds mfg:EffectiveContract ;
    mfg:status mfg:Candidate .

mfg:ExecutionBundleDesign rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

mfg:CoreExecutionBundleCapability rdf:type mfg:Boundary ;
    mfg:status mfg:Open .

mfg:PaperP2CoreCodePin rdf:type mfg:DesignObject ;
    mfg:status mfg:Partial .

mfg:ExecutionRealization rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:DesignObject ;
    mfg:status mfg:Candidate .

mfg:ExecutionRealization mfg:binds mfg:ExecutionIdentity .
mfg:ExecutionRealization mfg:binds mfg:GraphVersion .
```

Neither a declared bundle nor a realization proves that all hidden inputs were
captured, that recorded bytes are authentic, or that execution was hermetic.

## 10. Dependency order

This is the candidate package graph:

```turtle
@prefix okg: <https://malleus.dev/ontology-kg-realization/> .

mfg:ContractKernel rdf:type mfg:Package ;
    mfg:status mfg:Candidate .

mfg:ContractIdentity rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:status mfg:Candidate .

mfg:ReferenceDependencySemantics rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:status mfg:Candidate .

okg:OntologyDrivenKGRealization rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:dependsOn mfg:TypedViolationProtocol ;
    mfg:dependsOn mfg:ArtifactIdentity ;
    mfg:status mfg:AcceptedDesign .

okg:MalleusGraphRecipeProfileV0 rdf:type mfg:DesignObject ;
    mfg:dependsOn okg:OntologyDrivenKGRealization ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-D001 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:selects okg:MalleusGraphRecipeProfileV0 ;
    mfg:rejects okg:NativeMalleusRecipeLanguage ;
    mfg:rejects okg:MultipleRecipeFrontendsV0 ;
    mfg:rejects okg:OTTRFork ;
    mfg:status mfg:AcceptedDesign .

mfg:GraphRealizationEvolution rdf:type mfg:Package ;
    mfg:dependsOn okg:OntologyDrivenKGRealization ;
    mfg:dependsOn mfg:ContractEvolution ;
    mfg:status mfg:Candidate .

mfg:EvidenceIntegrityPackage rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:status mfg:Candidate .

mfg:GovernanceBootstrap rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:status mfg:Candidate .

mfg:GovernedChangeOperation rdf:type mfg:Package ;
    mfg:dependsOn mfg:ContractEvolution ;
    mfg:status mfg:Candidate .

mfg:AuditStageExecutionIdentity rdf:type mfg:Package ;
    mfg:dependsOn mfg:ArtifactIdentity ;
    mfg:status mfg:Candidate .

mfg:ArtifactIdentity rdf:type mfg:DesignObject ;
    mfg:status mfg:Implemented .

mfg:TypedViolationProtocol mfg:dependsOn mfg:ContractKernel .
mfg:ContractEvolution mfg:dependsOn mfg:TypedViolationProtocol .
mfg:ContractEvolution mfg:dependsOn mfg:ReferenceDependencySemantics .
mfg:ContractEvolution mfg:dependsOn mfg:ContractComposition .
mfg:DependencyClosedRevision mfg:dependsOn mfg:ContractEvolution .
mfg:GraphRealizationEvolution mfg:dependsOn mfg:DependencyClosedRevision .
mfg:EvidenceIntegrityPackage mfg:dependsOn mfg:ContractKernel .
mfg:EvidenceIntegrityPackage mfg:dependsOn mfg:TypedViolationProtocol .
mfg:EvidenceIntegrityPackage mfg:dependsOn mfg:AuditStageExecutionIdentity .
mfg:EvidenceChangePropagation mfg:dependsOn mfg:DependencyClosedRevision .
mfg:EvidenceChangePropagation mfg:dependsOn mfg:EvidenceIntegrityPackage .
mfg:AutomatedChangeAuthority mfg:dependsOn mfg:ContractKernel .
mfg:AutomatedChangeAuthority mfg:dependsOn mfg:GovernedChangeOperation .
mfg:AutomatedChangeAuthority mfg:dependsOn mfg:GovernanceBootstrap .
mfg:ExecutionIdentity mfg:dependsOn mfg:ContractIdentity .
mfg:EffectDelivery mfg:dependsOn mfg:CurrentActionAuthorization .

mfg:DeclaredProtocolComponentCoverage rdf:type mfg:TestObligation ;
    mfg:status mfg:Candidate .

mfg:ComponentBoundaryConformance rdf:type mfg:TestObligation ;
    mfg:informedBy okg:OntologyToPopulationCompositionSeamEvidence ;
    mfg:status mfg:Partial .

mfg:CompositionSeamConformance rdf:type mfg:TestObligation ;
    mfg:informedBy okg:OntologyToPopulationCompositionSeamEvidence ;
    mfg:status mfg:Partial .

mfg:CrossProtocolScenarioConformance rdf:type mfg:TestObligation ;
    mfg:status mfg:Candidate .

mfg:DependencyClosedChangeConformance rdf:type mfg:TestObligation ;
    mfg:status mfg:Candidate .

mfg:KnownExclusionAccounting rdf:type mfg:TestObligation ;
    mfg:informedBy okg:GraphRecipeFirstSliceEvidenceBoundary ;
    mfg:status mfg:Partial .

mfg:ProtocolCompositionCompleteness rdf:type mfg:FalsifiableClaim ;
    mfg:coverageObligation mfg:DeclaredProtocolComponentCoverage ;
    mfg:coverageObligation mfg:ComponentBoundaryConformance ;
    mfg:coverageObligation mfg:CompositionSeamConformance ;
    mfg:coverageObligation mfg:CrossProtocolScenarioConformance ;
    mfg:coverageObligation mfg:DependencyClosedChangeConformance ;
    mfg:coverageObligation mfg:KnownExclusionAccounting ;
    mfg:informedBy okg:GraphRecipeExperimentalLearning ;
    mfg:distinctFrom mfg:UniversalProtocolCompleteness ;
    mfg:status mfg:Candidate .

mfg:UniversalProtocolCompleteness rdf:type mfg:Boundary ;
    mfg:status mfg:Excluded .

mfg:ProtocolCompositionCounterevidence rdf:type rdfs:Class ;
    rdfs:subClassOf mfg:Observation ;
    mfg:counterevidenceFor mfg:ProtocolCompositionCompleteness .

mfg:ProtocolCompositionCompletenessRevisionRule rdf:type mfg:Invariant ;
    mfg:dependsOn mfg:ProtocolCompositionCounterevidence ;
    mfg:governs mfg:ProtocolCompositionCompleteness ;
    mfg:status mfg:Candidate .
```

The dependency-respecting work waves are:

1. Contract kernel and contract-composition decision.
2. Contract identity, typed violations, reference/dependency semantics,
   minimal audit-stage identity, governance bootstrap, and the materialized
   Graph Realization Protocol research slice.
3. In parallel where useful: contract evolution, optional evidence-integrity
   profiles, execution-identity integration, and additional realization
   profiles.
4. Dependency-closed revision, graph-realization evolution, and
   governed-change operations.
5. Evidence-change propagation and automated change authority.

Effect delivery is a separate optional branch downstream of current action
authorization, not of the change-authority DAG. The graph tuples above control
exact dependencies; the waves state a practical order without inventing extra
edges.

The 0.11 temporal slice is also dependency-addressable. These graph statuses
record the release-boundary observation; `src/malleus/status.py` and tests
remain authoritative for shipped capability.

```turtle
mfg:PrecisionAwareValidTime rdf:type mfg:DesignObject ;
    mfg:status mfg:Implemented .

mfg:ThreeValuedAcceptedGraphProjection rdf:type mfg:DesignObject ;
    mfg:dependsOn mfg:PrecisionAwareValidTime ;
    mfg:status mfg:Implemented .

mfg:HistoricalTimezoneDatabaseMigration rdf:type mfg:DesignObject ;
    mfg:dependsOn mfg:PrecisionAwareValidTime ;
    mfg:status mfg:Open .

mfg:DependencyClosedValidTimeProjection rdf:type mfg:DesignObject ;
    mfg:dependsOn mfg:ThreeValuedAcceptedGraphProjection ;
    mfg:status mfg:Open .

mfg:Malleus011ReleaseBoundaryObservation rdf:type mfg:Observation ;
    mfg:binds mfg:DependencyClosedValidTimeProjection ;
    mfg:binds mfg:HistoricalTimezoneDatabaseMigration ;
    mfg:binds mfg:PrecisionAwareValidTime ;
    mfg:binds mfg:ThreeValuedAcceptedGraphProjection ;
    mfg:status mfg:Implemented .
```

The author elevated ontology-driven KG realization to a pillar on 2026-08-17.
`design/ONTOLOGY_DRIVEN_KG_REALIZATION.md` carries its detailed candidate
protocol and evidence. `mfg:AcceptedDesign` applies to the pillar and its
no-privileged-writer boundary. The author accepted `OKG-D001`, the pinned OTTR
profile, and `OKG-D007` through `OKG-D011`, the GraphRecipe ABI, assembly,
dependency, canonicalization, and CI decisions, on 2026-08-17. Backend profiles,
ledger integration, and the public API remain unselected. The author also
accepted `OKG-D012`: LinkML is the sole first-party contract frontend for v0,
the compiled runtime is LinkML-free, and any custom frontend must cross the
same language-neutral artifact boundary without semantic privilege.

### 10.1 Candidate composition-completeness claim

`ProtocolCompositionCompleteness` records a bounded intuition, not a proof. For
one pinned protocol revision it claims completeness only relative to the
declared components, profiles, backends, workloads, composition seams, and
known exclusions. It depends on explicit component coverage, independent
boundary conformance, producer-consumer seam conformance, cross-protocol
scenarios, dependency-closed change behavior, and exclusion accounting.

GraphRecipe experiments contribute reusable evidence about how to test those
obligations. The completed research-local `GE-000` through `GE-020` slice gives
partial evidence only to component-boundary conformance, the
ontology-to-population composition seam, and known-exclusion accounting. It
binds 149 checksummed corpus files, 10 case receipts, 7 executable metamorphic
obligations, the selected manifest for each receipt, and the exact execution
identity recorded by the conformance report. The report identity is
`sha256:9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0`;
the checksum-set identity is
`sha256:aa5c904f79363b68bab9d82a2b6b027748ffe25358ef3fead5c5ba7b3dc7a3f2`.
Declared-component coverage, full cross-protocol scenarios, and
dependency-closed change conformance remain candidate obligations.

An unused-import removal changed the bound runner bytes. The hard identity
guard rejected the stale report and produced retained report identity
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`,
which supersedes
`sha256:41b180b273ecc24e59af769736519c071707134beecf91ae60ce10a1092a1ae0`.
The current refresh binds the changed `ontology.py`, `pyproject.toml`,
`status.py`, and implementation-status bytes plus package version `0.11.0`.
Its active identity above supersedes the retained
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`
identity. Both
dedicated CI steps run Ruff over the full research-local runner directory before
the 39-test slice. These changes refresh evidence identity; they do not change
any status conclusion.

The broader `GraphRecipeTDDProgram` and `GraphRecipeExperimentalLearning` are
therefore `Partial`. The fixture and offline CI gate are `Implemented` only at
the frozen research-local first-slice boundary. `GE-030` and later experiments,
the Lutra lock and differential gate, second-backend conformance, and public
promotion remain open. Their learning may inform other component boundary and
conformance experiments, but it does not prove those components correct and is
not a hard implementation-order dependency.

The claim excludes universal completeness. A hidden input or decision, an
untested legal composition, undeclared divergence, silent failure, privileged
bypass, nondeterministic meaning, or incomplete revision impact set is
counterevidence. Counterevidence blocks promotion for that pinned revision and
must remain addressable. A later claim must add an experiment, narrow its
scope, retract the claim, or supersede it while retaining the earlier evidence,
counterevidence, coverage matrix, and dependency closure.

## 11. Intellectual lineage

These edges mean “informed by,” not “equivalent to” or “implements the full
theory.” Exact sources and caveats remain in the private evidence record and
its Recon package. Neither is a shipped authority.

```turtle
mfg:ContractFactSet mfg:informedBy mfg:LinkMLDerivedSchemaModel .
mfg:ContractFactSet mfg:informedBy mfg:LaiEtAl2020TypedKG .
mfg:TypedViolation mfg:informedBy mfg:SHACLValidationResults .
mfg:DirectionalCompatibility mfg:informedBy mfg:AvroResolution .
mfg:ReferenceDependencySemantics mfg:informedBy mfg:Doyle1979TMS .
mfg:KnowledgeRevisionPolicy mfg:informedBy mfg:AGM1985 .
mfg:AlternativeCandidateContexts mfg:informedBy mfg:DeKleer1986ATMS .
mfg:AcceptedTemporalGraphVersion mfg:informedBy mfg:SnodgrassAhn1986Bitemporality .
mfg:AutomatedChangeAuthority mfg:informedBy mfg:AgentBuildingShell .
mfg:AutomatedChangeAuthority mfg:informedBy mfg:KeyNoteAndSPKI .
mfg:EvidenceArtifactLineage mfg:informedBy mfg:PROVO .
mfg:DependencyClosedRevision mfg:informedBy mfg:EviGraph .
mfg:ProducerCorrection mfg:informedBy mfg:VerifierGuidedRevisionWork .
```

Lai et al. provide a formal lineage for typed facts and witness-bearing
relations. Malleus remains ontology-typed, not dependently typed. Doyle, AGM,
and de Kleer ground justification retention, rational revision, and alternate
contexts. They do not make Malleus revision-correct by citation. The protocol
must expose those mechanisms and test their consequences.

## 12. First research-local slice

No public API should be designed from prose alone. The smallest discriminating
slice is a frontend-boundary neutrality fixture outside `src/malleus/`. It
tests the selected LinkML frontend against an independently authored,
test-only contract-fact producer through one admission implementation. The
direct-fact producer is a bootstrap and conformance oracle, not a second
first-party source language. The slice does not yet test graph-backend
neutrality.

**Claim**

A LinkML source and a test-only direct-fact producer that express the same
supported semantics produce the same independently expected
`ValidatedContractFactSet`, the same `EffectiveContract` under one
`NormativeAdmissionProfile`, and the same ordered typed validation results
through one conforming `AdmissionImplementation`.

**Required artifacts**

1. Candidate contract metamodel and logical fact vocabulary.
2. Candidate fact canonicalization and qualified-symbol policy.
3. Versioned LinkML support profile for the exercised subset.
4. Exact retained source bytes, import closure, and compilation-result record.
5. LinkML frontend adapter over the current parser behavior.
6. Independently authored direct-fact conformance input and frozen expected
   fact set. Neither may be copied or generated from LinkML frontend output.
7. Normative admission profile for current runtime semantics.
8. One identified admission implementation and conformance result.
9. Diagnostic profile and typed violation vocabulary.
10. Initial graph snapshots plus ordered operation traces covering valid,
    invalid, repeated, contextual, and stale operations.
11. A reloadable effective-contract artifact.
12. A manifest binding sources, compilers, profiles, implementations, outputs,
    operation traces, and results.

**Discriminating observations**

1. Byte-identical canonical validated fact-set output from both frontends and
   equality with the independently frozen expected fact set.
2. Identical effective-contract hash.
3. Identical ordered violation records for shared invalid inputs.
4. Identical accepted operations, refused operations, violations, and final
   structural-graph-snapshot hash for shared ordered traces.
5. Loud compilation failure for every exercised unsupported semantic field.
6. Serialize, reload, and recompute the same effective-contract hash.
7. Refuse unknown artifact fields, malformed facts, wrong profile hashes, and
   corrupted canonical bytes.
8. Construct and execute the runtime in a clean environment where LinkML is
   not installed. The package dependency split must make that environment
   reproducible rather than relying on an unused installed dependency.

**Reuse**

Reuse the current `TypeDef`, `SlotConstraint`, `EnumDef`, effective-slot
resolution, content-hash fixtures, graph fixtures, and inquisition guardrails.
Do not duplicate their semantics in a second untested implementation.

**Excluded from the first slice**

1. Public API promotion.
2. Full LinkML conformance.
3. OWL, SHACL, or dependent-type equivalence.
4. General graph-store abstraction.
5. Cross-contract migration implementation.
6. Automatic dependency repair.
7. Enterprise identity.
8. External effect delivery.

```turtle
mfg:FrontendNeutralityExperiment rdf:type mfg:TestObligation ;
    mfg:tests mfg:FrontendParity ;
    mfg:tests mfg:UnsupportedSemanticsPolicy ;
    mfg:dependsOn mfg:ContractKernel ;
    mfg:status mfg:Candidate .
```

## 13. Self-hosting and bootstrap

This note uses graph principles before the candidate graph protocol exists.
That creates an explicit bootstrap boundary, not a paradox.

1. The tuples in this note are candidate design data, not accepted Malleus
   records.
2. The first slice defines a seed meta-contract for these node and predicate
   kinds.
3. The same seed graph is expressed through the LinkML frontend and the
   test-only direct-fact conformance producer.
4. Parity requires the same effective contract identity and validation result.
5. Only after author acceptance can a versioned graph become authority for
   later design decisions.
6. A later design revision creates a new graph version with explicit lineage.
   It never edits the historical decision silently.

```turtle
mfg:ThisDesignGraph rdf:type mfg:DesignObject ;
    mfg:governedBy mfg:SeedMetaContract ;
    mfg:status mfg:Candidate .

mfg:SeedMetaContract rdf:type mfg:EffectiveContract ;
    mfg:status mfg:Candidate .

mfg:AcceptedFoundationGraph rdf:type mfg:DesignObject ;
    mfg:dependsOn mfg:AuthorAcceptance ;
    mfg:status mfg:Open .
```

## 14. Decisions required before implementation

The reconstruction supports the contract kernel as the dependency root.
`OKG-D012` closes the source-policy decision: use LinkML as the sole
first-party v0 frontend, keep the runtime contract frontend-neutral and
LinkML-free, and admit custom frontends only through conformance at the same
artifact boundary. These author choices remain open:

1. **Root abstraction.** Accept `EffectiveContract =
   ValidatedContractFactSet + NormativeAdmissionProfile`, or keep
   `OntologyRegistry` as the public root.
2. **Logical vocabulary.** Accept the object boundaries in section 4 before
   selecting an exact JSON, YAML, or Turtle wire encoding.
3. **Contract composition.** Keep one combined protocol and domain contract,
   or define `ProtocolRecordContract`, `GovernedGraphContract`, and
   `GovernanceContract` as separately evolving roles in one explicit
   composition.
4. **Compatibility scope.** Start with concrete graph replay compatibility, or
   also define schema-theoretic writer-to-reader analysis in the first package.
5. **Governance topology.** Protected partition in one accepted graph, or a
   separate governance graph.
6. **Promotion boundary.** Keep the first slice research-local until the
   canonical intermediate and frontend conformance fixture are demonstrated,
   or authorize an immediate core API. A third-party frontend is not required
   for v0 promotion, but the test-only alternate producer must prove that
   downstream stages do not import LinkML internals.

No core or public-package implementation follows from these unclosed
contract-kernel decisions. The separate GraphRecipe research slice does not
close them. The main pillar resumes the contract-kernel object model and then
`OKG-D002` through `OKG-D006`; `GE-030` is the next GraphRecipe experiment.
