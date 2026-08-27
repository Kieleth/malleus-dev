# GraphRecipe TDD and Gedankenexperiment program

Program ID: `OKG-X001`

Status: partial, with a complete research-local `GE-000` through `GE-020`
slice and open `GE-030` through `GE-100` obligations

Recorded: 2026-08-17

Depends on:

1. Accepted pillar `OKG-D000`.
2. Accepted OTTR selection `OKG-D001`.
3. Resume checkpoint
   [`OKG-CP001`](GRAPH_REALIZATION_SESSION_CHECKPOINT.md).

Public ancestry base: `27ca54c33fe705827bc845e876cb6ff24293c8f0`.
This is an ancestry base only, not the tested implementation snapshot. The
intended release locator is `v0.11.0`; exact report, file, and checksum
identities are authoritative.

Canonical design graph: [`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl),
revision 16,
`sha256:9ef32e1dcf7bbfea737f9b2beea3764d1fb369c2b0a485b1ea5384e8318d7d8a`

Shipped capability: none

## 1. Evaluation result

The completed first slice confirms that GraphRecipe can be developed through
TDD at the current research boundary. The protocol has strong observable
seams: effective ontology resolution, `ProposedOperation`, isolated staging,
canonical graph snapshots, graph-state digests, atomic materialization, and
accepted-graph artifacts. The fixture asserts each intermediate object and the
final graph rather than testing a vague “ontology in, network out” function.

The first experiment must establish the boundary:

> An ontology alone derives a legal logical graph contract and produces zero
> graph instances. A recipe, invocation, identity policy, and values are needed
> to construct an instance network.

Without that test, an implementation could hide population guesses inside the
ontology compiler and violate the pillar's derived, supplied, and observed
separation.

## 2. What “network” means in these experiments

Three graphs must remain distinct:

1. `LogicalGraphContract`: legal record roles, properties, references,
   relation signatures, and construction operations derived from the effective
   contract.
2. `ConstructionMemberGraph`: recipe members and explicit operation
   dependencies assembled from terminal facts.
3. `GraphRealization`: the materialized Malleus graph. Entities, signals, and
   events are nodes. Relations are keyed directed edges.

Every positive fixture freezes:

1. Logical contract.
2. Terminal construction facts.
3. Construction-member dependency graph.
4. Ordered `ProposedOperation.as_dict()` values.
5. Public `KnowledgeGraph.snapshot()`.
6. `KnowledgeGraph.canonical_operations()`.
7. Source, effective-recipe, invocation, plan, candidate, and final-state
   digests.
8. Per-operation recipe-member and expansion-path lineage.

Only asserting node and edge counts is insufficient. A wrong expansion can
produce an accidentally equivalent final graph.

## 3. Canonical fixture contract

The public-safe corpus is tracked at this boundary:

```text
conformance/graph_recipe/v0/
  profile.json
  diagnostics.json
  base/
    malleus-base-v0.stottr
    recipe.lock.json
  experiments/
    <experiment-id>/
      experiment.yaml
      input/
        ontology.yaml
        recipe.stottr
        recipe.lock.json
        invocations.json
        identity-policy.json
        mapping.yaml
        source.jsonl
        prior-graph.json
      expected/
        logical-contract.json
        terminal-facts.json
        member-graph.json
        proposed-operations.json
        graph.json
        lineage.json
        diagnostics.json
      negative/
        <negative-case>/
          input/
          expected/
```

Only relevant input files are present in a case. Every negative case contains
complete changed artifacts and expected diagnostics. It does not inherit an
implicit patch from its parent case.

`experiment.yaml` pins every input and expected-artifact digest. Expected files
are authored or reviewed independently of the implementation under test.
Golden outputs never update automatically.

The interactive and pytest paths call one pure runner:

```text
run_experiment(fixture_path, case_id) -> ConformanceReceipt
```

The runner returns the first divergent layer plus all completed earlier
artifacts. A separate explicit `propose-golden` action may write candidate
outputs beside a scratch copy. It cannot overwrite accepted fixtures.

## 4. Accepted terminal ABI

The author accepted `OKG-D007` on 2026-08-17. The first fixture must encode and
test this exact terminal base vocabulary:

```text
Record(
  member: IRI,
  operation_kind: closed Malleus operation IRI,
  record_type: effective-contract type IRI,
  record_id: string,
)

Property(
  member: IRI,
  property: effective-contract property IRI,
  value: RDF term or finite list,
)

RelationSource(member: IRI, record_id: string)
RelationTarget(member: IRI, record_id: string)
DependsOn(member: IRI, prerequisite_member: IRI)
```

Operation kinds are closed IRIs such as `mgrp:CreateEntity`, not free strings.
Record types and properties are ontology IRIs. The assembler resolves those
IRIs to the local string symbols currently consumed by `ProposedOperation`.
Graph record IDs remain strings because that is the existing graph contract.

This closes an encoding detail deliberately left open in the accepted profile.
It does not reopen OTTR selection. A later ABI change requires a superseding
decision and dependency-closed impact over profiles, fixtures, recipes, plans,
and adopters.

## 5. Experiment ladder

### `GE-000-ONTOLOGY-IS-NOT-POPULATION`

Input: minimal ontology with concrete `Person is_a Entity` and required
`name`. No recipe, invocation, mapping, or identity policy.

Expected logical contract:

```text
Person
  role: ENTITY
  required: id, name
  legal operation: CREATE_ENTITY
```

Expected instance network: zero nodes and zero relations.

Expected operations: `[]`.

Negative realization request without `GraphRecipeSet`:
`RECIPE_SELECTION_MISSING`. The graph remains unchanged.

Falsifies: “The ontology determines which instances and topology must exist.”

Tests: contract derivation and the ontology-to-population boundary.

### `GE-010-ONE-ENTITY`

Input: the same ontology, `Person/1.0.0` recipe, one invocation for Alice.

Expected network:

```text
person:alice : Person
person:alice.name = "Alice"
```

Expected operations:

```text
1. CREATE_ENTITY Person person:alice {"name":"Alice"}
```

Metamorphic positive: alpha-renamed variables, formatting changes, and prefix
aliases change the source digest but not the effective recipe, plan, or graph.

Negative cases:

1. Required `name = none`: `MANDATORY_RECIPE_VALUE_MISSING`.
2. Integer supplied for `name`: `RECIPE_ARGUMENT_TYPE_MISMATCH`.
3. Blank-node member identity: `FORBIDDEN_BLANK_NODE`.

Falsifies: “Malleus needs an RDF graph intermediate to lower OTTR into one
typed graph operation.”

Tests: parsing, type binding, expansion, assembly, lowering, and staging.

### `GE-020-TWO-NODES-ONE-RELATION`

Input: `Person`, `Organization`, and concrete `WorksForRelation`. The source
recipe intentionally declares its relation before both endpoint records.

Expected member graph:

```text
person-member       -> employment-member
organization-member -> employment-member
```

Expected network:

```text
person:alice : Person
org:acme : Organization
employment:alice-acme : WorksForRelation
person:alice -> org:acme
```

Expected operations:

```text
1. CREATE_ENTITY Person person:alice {"name":"Alice"}
2. CREATE_ENTITY Organization org:acme {"name":"Acme"}
3. CREATE_RELATION WorksForRelation employment:alice-acme
   person:alice -> org:acme {"relation_type":"WORKS_FOR"}
```

Recipe pattern permutation must not alter operation order.

Negative cases:

1. Missing local endpoint dependency:
   `LOCAL_REFERENCE_DEPENDENCY_MISSING`.
2. Wrong endpoint role: `PLAN_GATE_REJECTION`, retaining the exact endpoint
   diagnostic.
3. Dependency cycle: `CONSTRUCTION_DEPENDENCY_CYCLE`.

Falsifies: “OTTR source order determines execution order or deterministic
writes are impossible.”

Tests: global terminal assembly, dependency graph, stable topological sort,
and structural admission.

### `GE-030-OPTIONAL-PROPERTY-AND-ADD-ON`

Input: required `Person.name`, optional `Person.nickname`, a core recipe, and a
property-only add-on recipe.

Expected present operation:

```text
CREATE_ENTITY Person person:alice {"name":"Alice","nickname":"Al"}
```

Expected absent operation:

```text
CREATE_ENTITY Person person:alice {"name":"Alice"}
```

The complete atomic invocation set contains exactly one anchoring `Record` for
the member. The add-on contributes properties to that member before operation
lowering.

Negative cases:

1. Optional value used in identity, type, record ID, endpoint, or dependency:
   `OPTIONAL_STRUCTURAL_USE`.
2. Add-on without an anchored record: `ORPHAN_MEMBER_FACT`.
3. Conflicting scalar values: `CONFLICTING_MEMBER_PROPERTY`.

Falsifies: “Optionality needs a business-rule language or may silently remove
the required record.”

Tests: optional OTTR semantics and PopulationPlan-wide assembly.

### `GE-040-MULTIVALUED-CROSS`

Input: unordered, multivalued `Person.tags`; invocation values `research` and
`graph`; bounded `cross` expansion.

Expected operation:

```text
CREATE_ENTITY Person person:alice
{"name":"Alice","tags":["graph","research"]}
```

Reversing the input list produces the same semantic plan and digest because
the contract declares the slot unordered. Every duplicate derivation remains
in lineage even if semantic values deduplicate.

Negative cases:

1. `zipMin` or `zipMax`: `FORBIDDEN_LIST_EXPANDER`.
2. Declared expansion bound exceeded: `EXPANSION_BUDGET_EXCEEDED`.
3. Multiple values for scalar slot: `MULTIPLICITY_CONTRACT_VIOLATION`.

Falsifies: “List expansion necessarily introduces truncation or nondeterminism.”

Tests: bounded `cross`, contract-aware canonicalization, and lineage retention.

### `GE-050-CYP450-ALL-RECORD-FAMILIES`

Input: current CYP450 ontology plus one nested interaction-observation recipe.

Expected network:

```text
drug:simvastatin : Drug
enzyme:CYP3A4 : Enzyme
drug:simvastatin -[rel:simvastatin:CYP3A4]-> enzyme:CYP3A4
signal:risk:simvastatin:CYP3A4 : DrugSignal
event:detected:simvastatin:CYP3A4 : DrugEvent
```

Expected materialization: four nodes and one relation edge. Entity, signal,
and event records are graph nodes. The substrate relation is the edge.

Expected order: drug, enzyme, relation, signal, event, subject to the explicit
member dependencies frozen by the fixture.

Negative cases:

1. Signal missing dependency on in-plan bearer:
   `LOCAL_REFERENCE_DEPENDENCY_MISSING`.
2. Missing bearer: `MEMBER_REQUIRED_PROPERTY_MISSING`.
3. Signal-event dependency cycle: `CONSTRUCTION_DEPENDENCY_CYCLE`.

Falsifies: “GraphRecipe supports only ordinary entities and relations.”

Tests: nested recipes, all record families, reference dependencies, and full
staging.

### `GE-060-SOURCE-MAPPING-IDENTITY-COLLISION`

Input: two drug rows pointing to the same CYP3A4 enzyme, strict source mapping,
and explicit identity policy.

Expected network: two drugs, one enzyme, and two substrate relations.

The identical enzyme derivations are explicitly idempotent. Both derivation
paths remain visible even though one create operation results.

Negative cases:

1. Shared identity with conflicting properties: `IDENTITY_COLLISION`.
2. Unknown strict-mapping field: `UNKNOWN_MAPPING_SYMBOL`.
3. Two matching source mappings: `AMBIGUOUS_SOURCE_MATCH`.
4. Missing identity policy: `IDENTITY_POLICY_MISSING`.

Falsifies: “Mapping, identity, deduplication, and collision behavior may remain
implicit inside recipes.”

Tests: population selection, mapping, identity, conflict policy, and global
assembly.

### `GE-070-ATOMIC-FAILURE-AND-STALE-BASE`

Input: one invalid CYP450 member, followed by one valid candidate staged over a
base graph that changes before materialization.

Expected invalid result: full expansion and plan assembly complete, staging
rejects, base graph is byte-identical, and no overlay is exposed.

Diagnostics:

1. Invalid member: `PLAN_GATE_REJECTION`, retaining the original ontology
   validation reason.
2. Changed base: `STALE_DERIVATION`.

Falsifies: “The compiler needs a privileged write path or partial writes are an
acceptable failure mode.”

Tests: complete OTTR-to-staging path, atomicity, and base binding.

### `GE-080-ONTOLOGY-AND-RECIPE-EVOLUTION`

Input: `Person` contract and recipe v1, compatible optional-email contract v2,
breaking required-email contract v3, and a v1 graph.

Expected v2 disposition: `REVALIDATE`. Logical network remains unchanged even
if contract-bound hashes change.

Expected v3 result:

```text
STALE_DERIVATION
UNMAPPED_REQUIRED_FIELD(Person.email)
```

The old graph remains unchanged. After mapping and recipe revision, rebuilding
the v3 graph requires `MIGRATE`. Applying the new recipe as a create operation
to the old graph is forbidden.

Falsifies: “Schema regeneration is ontology evolution or recipes may mutate
accepted graph state directly.”

Tests: reverse dependency closure, revalidation, replanning, and the migration
boundary.

### `GE-090-RECON-DOGFOOD`

Input: actual Recon ontology, an evidence recipe, and one invocation describing
the primary OTTR evidence supporting `OKG-D001`.

Expected network includes a work, evidence attachment, claim, and reviewed
relation. Any in-plan class-valued evidence reference has an explicit
dependency.

Negative case: omit `claim_kind` or a required reviewed-relation field.
Compilation fails with `MEMBER_REQUIRED_PROPERTY_MISSING` before staging.

Falsifies: “The protocol works only on toy ontologies and cannot satisfy
Malleus's own imported ontology and mixin constraints.”

Tests: full dogfood path under an actual project ontology.

### `GE-100-DIFFERENTIAL-AND-BACKEND-CONFORMANCE`

Input: semantically equivalent recipe variants, an `ottr:Triple` mirror for the
shared expansion subset, pinned Lutra 0.6.20, the in-memory backend, and one
separately selected backend profile.

Expected:

1. Different source digests where exact bytes differ.
2. Identical effective recipe identities.
3. Identical normalized expansion for shared OTTR semantics.
4. Identical logical member graph and operation sequence.
5. Backend-specific physical representations that decode to one logical record
   set.

Injected disagreement: `OTTR_DIFFERENTIAL_MISMATCH`.

Falsifies: “An implementation assertion proves conformance or one backend's
physical representation defines recipe meaning.”

Tests: effective identity, independent OTTR evidence, and backend independence.

The second backend is selected by `OKG-D002`. This experiment must not select
one implicitly.

## 6. Automatic metamorphic tests

Every positive case also runs:

1. Repeated execution.
2. Recipe pattern permutation.
3. Template declaration permutation.
4. Invocation permutation where the semantic input is an unordered set.
5. Harmless formatting and prefix changes.
6. Safe variable alpha-renaming.
7. Serialize, reload, and rerun.
8. Stage without base mutation.
9. Materialize and export-reload equivalence.
10. Mutation of one identity-bearing input, which must change the relevant
    downstream digests.

These tests expose accidental dependence on source order, parser spelling,
object insertion order, or in-memory aliases.

## 7. TDD sequence

The first implementation slice was limited to `GE-000` through `GE-020`:

1. Write `GE-000` as a failing contract-boundary test.
2. Add the smallest logical-contract projection needed to pass it.
3. Write `GE-010` as a failing terminal-expansion and lowering test.
4. Add only the parser, profile validation, expansion, and one-record assembler
   behavior needed to pass it.
5. Write `GE-020` as a failing dependency-order test.
6. Add explicit dependency assembly and stable topological sorting.
7. Refactor only after all three remain green under their metamorphic cases.

That slice is complete at its declared evidence boundary. The checksum set
covers 149 corpus files. Ten cases emit canonical receipts, and seven declared
metamorphic obligations map to executable tests. The dedicated slice passed 40
tests, the relevant core selection passed 257 tests with 2 skips, and the full
configured suite recorded 807 passes with 2 skips. Exact evidence lives in
[`FIRST_SLICE_CONFORMANCE_REPORT.json`](../research/ontology_driven_kg_realization/experiments/graph_recipe/FIRST_SLICE_CONFORMANCE_REPORT.json),
identified by
`sha256:6d41cd245234dc3b77bbbc5a5c16529d197aa9db2a03f1525c1b1602d17c82a8`.
The checksum set is identified by
`sha256:aa5c904f79363b68bab9d82a2b6b027748ffe25358ef3fead5c5ba7b3dc7a3f2`.

An unused-import removal changed `assembly.py` bytes without changing the
bounded semantic result. The hard identity test correctly rejected the stale
report and produced retained identity
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`,
which supersedes
`sha256:41b180b273ecc24e59af769736519c071707134beecf91ae60ce10a1092a1ae0`.
A later bound-source refresh produced
`sha256:9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0`,
which supersedes `sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`.
The active release-boundary refresh adds the final ontology and status-document
bytes, three relevant-core test sources, current observations, and the
non-enumerating public-snapshot guard. Its identity above supersedes
`sha256:9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0`.
The checksum-set identity did not change.

Each receipt's canonical identity covers its complete serialized value,
including the exact selected-manifest path and source-byte digest. This binds
manifest discovery to the result: selecting different case bytes cannot retain
the same conforming receipt. The report also binds declared runner, direct-core,
package-boundary, and relevant-core test sources. Declared evidence identity
here means those exact source bytes, selected manifests, receipts, and recorded
observation objects. It does not establish complete transitive dependency or
execution-environment closure. The public ancestry base and intended release
locator do not identify the tested implementation bytes.

Red tests live on the active implementation branch. Main CI remains green;
future unimplemented cases stay in this experiment contract until their TDD
step begins. Do not merge permanent `xfail` placeholders or silently omit a
declared promoted test from pytest collection.

Then progress in order:

```text
GE-030 optional/add-on semantics
  -> GE-040 collections and canonicalization
  -> GE-050 all graph record families
  -> GE-060 mappings and identity
  -> GE-070 atomic failure
  -> GE-080 evolution
  -> GE-090 Recon dogfood
  -> GE-100 differential and second backend
```

## 8. Interactive path

The research runner and pytest must call the same `run_experiment()` and
assertion library. A proposed interactive surface is:

```text
python -m malleus.graph_recipe.experiment \
  conformance/graph_recipe/v0/experiments/ge-050-cyp450 \
  --show logical-contract,terminal-facts,member-graph,operations,graph,lineage
```

Before public API promotion, the research-local wrapper lives under:

```text
research/ontology_driven_kg_realization/experiments/graph_recipe/
  README.md
  case_harness.py
  run_cases.py
  test_cases.py
  results/
```

The runner may render a graph for inspection, but visualization is a projection
of `graph.json`. It is never the oracle. A user may copy a fixture to an ignored
scratch directory, edit inputs, and compare the result without changing the
accepted corpus.

## 9. CI architecture

The offline first-slice gate is implemented in both
[`tests.yml`](../.github/workflows/tests.yml) and
[`release.yml`](../.github/workflows/release.yml). Each workflow invokes the
same research-local `test_cases.py` suite. This implements the core offline
gate for `GE-000` through `GE-020`; it does not implement the planned Lutra
differential lane or authorize public promotion.

Each dedicated step first runs `python -m ruff check` over the complete
research-local GraphRecipe directory, then runs the 40-test conformance slice.

The complete promotion design has two required lanes.

### 9.1 Primary offline Malleus gate

The existing Python 3.10 through 3.13 matrix runs the complete internal corpus:

1. Profile acceptance and rejection.
2. Canonicalization and deterministic identity.
3. Terminal facts and lineage.
4. Member-graph assembly and operation ordering.
5. `ProposedOperation` lowering.
6. Isolated staging and materialization.
7. Exact graph postconditions.
8. Remote template refusal before any socket access.

This lane has no Java, Lutra, Maven, or runtime network requirement.

### 9.2 Independent OTTR differential gate

One separate `ottr-conformance` job uses pinned Java 17 and
`xyz.ottr.lutra:lutra-cli:0.6.20` as a differential oracle over the shared OTTR
subset. It does not run once per Python version.

Normative authority order is:

1. Pinned OTTR specifications.
2. Accepted Malleus GraphRecipe Profile.
3. Reviewed frozen Malleus fixtures.
4. Actual graph postconditions.
5. Lutra as independent differential evidence, not authority.

A disagreement fails without rewriting goldens. It is classified as a Malleus
defect, Lutra divergence, specification ambiguity, or deliberate profile
exclusion.

The Lutra tool lock must record its coordinate, repository, filename, byte
size, exact SHA-256, version output, SPDX license, upstream source identity,
Java distribution and exact runtime, architecture, and allowed arguments. The
artifact checksum has not yet been acquired and therefore blocks promotion of
this job.

Lutra remains an unmodified, separately invoked CLI. Its JAR is not committed,
included in Python dependencies, packaged in a wheel or sdist, or redistributed
in a published container during this experiment. This keeps the implementation
and release boundary clear. It is an engineering boundary, not legal advice.

## 10. Current repository seams and constraints

Reusable clean seams:

1. `src/malleus/kg.py`: snapshots, canonical operations, graph digests, and
   materialization.
2. `src/malleus/staging.py`: `ProposedOperation`, candidate staging, atomicity,
   and stale-base refusal.
3. `tests/test_staging.py`: current structural guardrails.
4. Existing domain ontologies.
5. Both GitHub workflows.

Promotion targets after the research slice stabilizes:

```text
src/malleus/graph_recipe.py
tests/test_graph_recipe.py
```

The pytest configuration is an explicit file allowlist. A new test is invisible
to bare `pytest` until `pyproject.toml` lists it. Package contents are also
allowlisted. Runtime module, test file, corpus, package manifest, and tracking
guard must therefore promote together.

The shared worktree has parallel changes in `pyproject.toml`, core protocol
modules, ontology, docs, and tests. The GraphRecipe slice adds research-local
runner code, frozen fixtures, executable tests, a conformance report, and the
two workflow steps. It does not add a packaged runtime module or public API.

The recorded evidence is:

1. GraphRecipe first slice: 40 passed.
2. Relevant core, `tests/test_staging.py`, `tests/test_ontology.py`, and
   `tests/test_kg.py`: 257 passed, 2 skipped.
3. Full configured suite: 807 passed, 2 skipped.

The first two selections bind their declared test and directly exercised source
bytes. The full configured result is an observation bound by the report, not a
claim of complete suite-source, transitive-dependency, or environment identity.

## 11. Promotion gates

GraphRecipe remains research-local until:

1. `GE-000` through `GE-020` pass with frozen terminal signatures and stable
   diagnostics.
2. Repetition and permitted input permutations yield the expected identities.
3. Every operation has complete recipe-member and expansion-path lineage.
4. Remote dependencies fail before network access.
5. One invalid member proves whole-candidate atomicity.
6. `GE-030` through `GE-070` pass before public compiler promotion.
7. Recon dogfood passes before claiming complex imported-ontology support.
8. The Lutra differential corpus agrees or records a reviewed profile
   exclusion.
9. A second backend passes before claiming backend-independent conformance.
10. The built wheel proves no Java or Lutra dependency shipped.
11. `IMPLEMENTATION_STATUS`, exports, package version, changelog, public docs,
    and wheel smoke tests advance together.

Gate 1 is complete only for the frozen `GE-000` through `GE-020` corpus. The
remaining gates stay open. `GE-030` is the next GraphRecipe experiment.

## 12. Accepted microdecisions exposed by the tests

The author accepted all five decisions on 2026-08-17. They remain accepted
design. The first slice implements only the clauses exercised by `GE-000`
through `GE-020`, and does not create a public or shipped capability:

1. `OKG-D007`, terminal ABI: member, operation kind, record type, and property
   names use IRIs; graph record IDs remain strings.
2. `OKG-D008`, assembly scope: terminal facts assemble across the complete
   atomic `PopulationPlan`. A property-only add-on may target a member anchored
   by exactly one `Record` in another invocation in the same plan.
3. `OKG-D009`, reference dependencies: every reference to a record created in
   the same plan requires `DependsOn`, including relation endpoints, signal
   bearers, and class-valued properties.
4. `OKG-D010`, multivalue canonicalization: unordered multivalued slots
   canonicalize as semantic sets while retaining all derivation paths; ordered
   slots preserve contract-declared order.
5. `OKG-D011`, CI split: the offline Malleus fixture corpus is the primary gate;
   one separate pinned Lutra job is a required differential oracle after its
   tool lock is complete.

The offline half of `OKG-D011` is implemented for the first slice. The Lutra
half remains open. Anchored add-ons and multivalue canonicalization first enter
the executable ladder at `GE-030` and `GE-040`, so acceptance of `OKG-D008` and
`OKG-D010` is not evidence that those behaviors have passed.

No compiler code may substitute different choices implicitly. A change requires
a superseding decision with addressable counterevidence and dependency-closed
impact.

## 13. Candidate protocol-composition completeness claim

The author's intuition that learning across these experiments could make the
protocol complete is retained as the falsifiable candidate claim
`ProtocolCompositionCompleteness`. It is not an accepted design decision or a
proof of universal completeness.

For one pinned protocol revision, declared component inventory, profile set,
backend set, and workload envelope, the claim requires all of these coverage
obligations:

1. `DeclaredProtocolComponentCoverage`: every component names its inputs,
   outputs, authority, identity, failure contract, and exclusions. No required
   decision remains hidden in an implementation.
2. `ComponentBoundaryConformance`: every component boundary has independent
   positive, negative, and metamorphic tests with deterministic artifacts and
   typed diagnostics.
3. `CompositionSeamConformance`: every declared producer-consumer seam tests
   ordering, identity, lineage, atomicity, and failure propagation.
4. `CrossProtocolScenarioConformance`: end-to-end scenarios cross the contract,
   recipe, mapping, staging, evidence, decision, revision, and execution
   boundaries that the declared composition actually uses.
5. `DependencyClosedChangeConformance`: changes and counterexamples identify
   every affected artifact, fixture, implementation, and adopter before a
   revised claim can advance.
6. `KnownExclusionAccounting`: unsupported profiles, backends, workloads, and
   unexercised combinations remain explicit, addressable, and excluded from the
   claim's scope.

The GraphRecipe ladder contributes evidence without discharging the whole
claim. The implemented `GE-000` through `GE-020` slice supplies partial
evidence for `ComponentBoundaryConformance`, `CompositionSeamConformance`, and
`KnownExclusionAccounting`. Its ontology-only case, typed negative cases,
deterministic identities, explicit dependency ordering, lineage projections,
selected-manifest receipt binding, and recorded exclusions support those three
obligations at this boundary. `DeclaredProtocolComponentCoverage`,
`CrossProtocolScenarioConformance`, and
`DependencyClosedChangeConformance` remain candidate obligations.

The open `GE-030` through `GE-070` experiments cover add-on assembly,
canonicalization, all record families, mapping and identity, and atomic
failure. `GE-080` covers dependency-closed change, `GE-090` a non-toy internal
workload, and `GE-100` differential and backend conformance. The implemented
fixtures, diagnostic discipline, metamorphic cases, and layer-by-layer receipts
can inform the frontend-neutrality, logical-derivation, no-bypass, and other
component-boundary experiments. That evidence relationship is `informedBy`,
not a hard requirement that unrelated experiments wait for GraphRecipe.

The claim is deliberately non-universal. Passing a finite corpus says nothing
about undeclared protocols, arbitrary future components, untested profile
versions, every backend, every workload, or every interaction. Passing tests is
evidence relative to the declared coverage matrix, not proof that no unknown
counterexample exists.

An addressable observation is counterevidence if it exposes a hidden input or
decision, an untested legal composition path, an undeclared semantic divergence,
an untyped or silent failure, a privileged bypass, nondeterministic meaning, or
an incomplete revision impact set. Counterevidence blocks promotion for the
pinned revision. It must be retained and must lead to a new experiment, a
narrower scope, or a superseding or retracted claim. Goldens and exclusions
cannot be changed merely to erase the failure. A superseding claim must preserve
the prior claim, evidence, counterevidence, coverage matrix, and affected
dependency closure.

## 14. Experiment dependency graph

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .
@prefix okg: <https://malleus.dev/ontology-kg-realization/> .

okg:GraphRecipeTDDProgram rdf:type mfg:TestObligation ;
    rdf:type mfg:ComponentBoundaryConformanceExperiment ;
    mfg:dependsOn okg:OKG-D001 ;
    mfg:tests mfg:DeclaredProtocolComponentCoverage ;
    mfg:tests mfg:ComponentBoundaryConformance ;
    mfg:tests mfg:CompositionSeamConformance ;
    mfg:tests mfg:CrossProtocolScenarioConformance ;
    mfg:tests mfg:DependencyClosedChangeConformance ;
    mfg:tests mfg:KnownExclusionAccounting ;
    mfg:tests okg:MalleusGraphRecipeProfileV0 ;
    mfg:produces okg:GraphRecipeConformanceFixture ;
    mfg:produces okg:GraphRecipeExperimentalLearning ;
    mfg:status mfg:Partial .

okg:GE-000 mfg:dependsOn okg:LogicalGraphContract ;
    mfg:status mfg:Implemented .
okg:GE-010 mfg:dependsOn okg:GE-000 ;
    mfg:status mfg:Implemented .
okg:GE-020 mfg:dependsOn okg:GE-010 ;
    mfg:status mfg:Implemented .
okg:GE-030 mfg:dependsOn okg:GE-020 ;
    mfg:status mfg:Open .
okg:GE-040 mfg:dependsOn okg:GE-030 ;
    mfg:status mfg:Open .
okg:GE-050 mfg:dependsOn okg:GE-040 ;
    mfg:status mfg:Open .
okg:GE-060 mfg:dependsOn okg:GE-050 ;
    mfg:status mfg:Open .
okg:GE-070 mfg:dependsOn okg:GE-060 ;
    mfg:status mfg:Open .
okg:GE-080 mfg:dependsOn okg:GE-070 ;
    mfg:status mfg:Open .
okg:GE-090 mfg:dependsOn okg:GE-080 ;
    mfg:status mfg:Open .
okg:GE-100 mfg:dependsOn okg:GE-090 ;
    mfg:status mfg:Open .

okg:GraphRecipeExperimentalLearning rdf:type mfg:DesignObject ;
    mfg:derivedFrom okg:GE-000 ;
    mfg:derivedFrom okg:GE-010 ;
    mfg:derivedFrom okg:GE-020 ;
    mfg:derivedFrom okg:GraphRecipeFirstSliceConformanceResult ;
    mfg:derivedFrom okg:GraphRecipeDeclaredEvidenceIdentityLearning ;
    mfg:derivedFrom okg:OntologyToPopulationCompositionSeamEvidence ;
    mfg:status mfg:Partial .

<https://fixtures.malleus.dev/graph-recipe/v0/report/first-slice-conformance>
    rdf:type mfg:DesignObject ;
    mfg:identifiedBy okg:GraphRecipeFirstSliceConformanceReport-sha256-6d41cd245234dc3b77bbbc5a5c16529d197aa9db2a03f1525c1b1602d17c82a8 ;
    mfg:status mfg:Implemented .

okg:GraphRecipeFirstSliceConformanceReport-sha256-41b180b273ecc24e59af769736519c071707134beecf91ae60ce10a1092a1ae0
    rdf:type mfg:DesignObject .

okg:GraphRecipeFirstSliceConformanceReport-sha256-64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97
    rdf:type mfg:DesignObject ;
    mfg:supersedes okg:GraphRecipeFirstSliceConformanceReport-sha256-41b180b273ecc24e59af769736519c071707134beecf91ae60ce10a1092a1ae0 .

okg:GraphRecipeFirstSliceConformanceReport-sha256-9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0
    rdf:type mfg:DesignObject ;
    mfg:supersedes okg:GraphRecipeFirstSliceConformanceReport-sha256-64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97 .

okg:GraphRecipeFirstSliceConformanceReport-sha256-6d41cd245234dc3b77bbbc5a5c16529d197aa9db2a03f1525c1b1602d17c82a8
    rdf:type mfg:DesignObject ;
    mfg:supersedes okg:GraphRecipeFirstSliceConformanceReport-sha256-9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0 .

okg:GraphRecipeFirstSliceReportIdentityGuard rdf:type mfg:Invariant ;
    mfg:governs <https://fixtures.malleus.dev/graph-recipe/v0/report/first-slice-conformance> ;
    mfg:status mfg:Implemented .

okg:GraphRecipeRunnerByteChangeObservation rdf:type mfg:Observation ;
    mfg:identifiedBy okg:GraphRecipeAssembly-sha256-ca2286a4277318f71094db08f7e86c9b8d4e44a7b28df9ebf62e0aec9de4cd5b ;
    mfg:status mfg:Implemented .

okg:GraphRecipeReportDependencyClosedRefreshObservation rdf:type mfg:Observation ;
    mfg:binds okg:GraphRecipeFirstSliceConformanceReport-sha256-41b180b273ecc24e59af769736519c071707134beecf91ae60ce10a1092a1ae0 ;
    mfg:binds okg:GraphRecipeFirstSliceConformanceReport-sha256-64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97 ;
    mfg:dependsOn okg:GraphRecipeFirstSliceReportIdentityGuard ;
    mfg:derivedFrom okg:GraphRecipeRunnerByteChangeObservation ;
    mfg:produces okg:GraphRecipeFirstSliceConformanceReport-sha256-64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97 ;
    mfg:status mfg:Implemented .

okg:GraphRecipeReportBoundSourceRefreshObservation rdf:type mfg:Observation ;
    mfg:binds okg:GraphRecipeFirstSliceConformanceReport-sha256-64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97 ;
    mfg:binds okg:GraphRecipeFirstSliceConformanceReport-sha256-9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0 ;
    mfg:dependsOn okg:GraphRecipeFirstSliceReportIdentityGuard ;
    mfg:produces okg:GraphRecipeFirstSliceConformanceReport-sha256-9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0 ;
    mfg:status mfg:Implemented .

okg:GraphRecipeReportReleaseBoundaryRefreshObservation rdf:type mfg:Observation ;
    mfg:binds okg:GraphRecipeFirstSliceConformanceReport-sha256-9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0 ;
    mfg:binds okg:GraphRecipeFirstSliceConformanceReport-sha256-6d41cd245234dc3b77bbbc5a5c16529d197aa9db2a03f1525c1b1602d17c82a8 ;
    mfg:dependsOn okg:GraphRecipeFirstSliceReportIdentityGuard ;
    mfg:produces okg:GraphRecipeFirstSliceConformanceReport-sha256-6d41cd245234dc3b77bbbc5a5c16529d197aa9db2a03f1525c1b1602d17c82a8 ;
    mfg:status mfg:Implemented .

okg:GraphRecipeFirstSliceChecksumSet rdf:type mfg:DesignObject ;
    mfg:identifiedBy okg:GraphRecipeFirstSliceChecksumSet-sha256-aa5c904f79363b68bab9d82a2b6b027748ffe25358ef3fead5c5ba7b3dc7a3f2 ;
    mfg:status mfg:Implemented .

okg:GraphRecipeFirstSliceSelectedManifestSet rdf:type mfg:DesignObject ;
    mfg:derivedFrom <https://fixtures.malleus.dev/graph-recipe/v0/report/first-slice-conformance> ;
    mfg:status mfg:Implemented .

okg:GraphRecipeFirstSliceReceiptSet rdf:type mfg:DesignObject ;
    mfg:derivedFrom <https://fixtures.malleus.dev/graph-recipe/v0/report/first-slice-conformance> ;
    mfg:status mfg:Implemented .

okg:GraphRecipeSelectedManifestReceiptBinding rdf:type mfg:Invariant ;
    mfg:binds okg:GraphRecipeFirstSliceSelectedManifestSet ;
    mfg:binds okg:GraphRecipeFirstSliceReceiptSet ;
    mfg:dependsOn okg:GraphRecipeFirstSliceChecksumSet ;
    mfg:status mfg:Implemented .

okg:GraphRecipeFirstSliceExecutionIdentity rdf:type mfg:DesignObject ;
    mfg:binds <https://fixtures.malleus.dev/graph-recipe/v0/report/first-slice-conformance> ;
    mfg:binds okg:GraphRecipeFirstSliceChecksumSet ;
    mfg:dependsOn okg:GraphRecipeSelectedManifestReceiptBinding ;
    mfg:status mfg:Implemented .

okg:GraphRecipeFirstSliceDeclaredEvidenceIdentity rdf:type mfg:DesignObject ;
    mfg:binds <https://fixtures.malleus.dev/graph-recipe/v0/report/first-slice-conformance> ;
    mfg:binds okg:GraphRecipeFirstSliceChecksumSet ;
    mfg:dependsOn okg:GraphRecipeSelectedManifestReceiptBinding ;
    mfg:status mfg:Implemented ;
    mfg:supersedes okg:GraphRecipeFirstSliceExecutionIdentity .

okg:GraphRecipeFirstSliceConformanceObservation rdf:type mfg:Observation ;
    mfg:derivedFrom okg:GraphRecipeFirstSliceDeclaredEvidenceIdentity ;
    mfg:produces okg:GraphRecipeFirstSliceConformanceResult ;
    mfg:status mfg:Implemented .

okg:GraphRecipeFirstSliceConformanceResult rdf:type mfg:DesignObject ;
    mfg:binds <https://fixtures.malleus.dev/graph-recipe/v0/report/first-slice-conformance> ;
    mfg:binds okg:GE-000 ;
    mfg:binds okg:GE-010 ;
    mfg:binds okg:GE-020 ;
    mfg:binds okg:GraphRecipeFirstSliceChecksumSet ;
    mfg:binds okg:GraphRecipeFirstSliceEvidenceBoundary ;
    mfg:binds okg:GraphRecipeFirstSliceDeclaredEvidenceIdentity ;
    mfg:dependsOn okg:GraphRecipeConformanceFixture ;
    mfg:status mfg:Implemented .

okg:GraphRecipeFirstSliceEvidenceBoundary rdf:type mfg:Boundary ;
    mfg:binds mfg:CrossProtocolScenarioConformance ;
    mfg:binds mfg:DependencyClosedChangeConformance ;
    mfg:binds okg:GE-030 ;
    mfg:binds okg:GraphRecipeImplementationPromotion ;
    mfg:binds okg:LutraDifferentialGate ;
    mfg:binds okg:SecondBackendConformance ;
    mfg:status mfg:Implemented .

okg:GraphRecipeFirstSliceEvidenceBundle rdf:type mfg:DesignObject ;
    mfg:binds <https://fixtures.malleus.dev/graph-recipe/v0/report/first-slice-conformance> ;
    mfg:binds okg:GraphRecipeFirstSliceChecksumSet ;
    mfg:binds okg:GraphRecipeFirstSliceEvidenceBoundary ;
    mfg:binds okg:GraphRecipeFirstSliceDeclaredEvidenceIdentity ;
    mfg:binds okg:GraphRecipeIncompleteExecutionEnvironmentClosureObservation ;
    mfg:binds okg:GraphRecipeReportBoundSourceRefreshObservation ;
    mfg:binds okg:GraphRecipeReportDependencyClosedRefreshObservation ;
    mfg:binds okg:GraphRecipeReportReleaseBoundaryRefreshObservation ;
    mfg:dependsOn okg:GraphRecipeFirstSliceConformanceResult ;
    mfg:status mfg:Implemented .

okg:GraphRecipeExactExecutionIdentityLearning rdf:type mfg:Observation ;
    mfg:binds okg:GraphRecipeFirstSliceExecutionIdentity ;
    mfg:derivedFrom okg:GraphRecipeFirstSliceConformanceResult ;
    mfg:derivedFrom okg:GraphRecipeReportBoundSourceRefreshObservation ;
    mfg:derivedFrom okg:GraphRecipeReportDependencyClosedRefreshObservation ;
    mfg:informedBy okg:GraphRecipeSelectedManifestReceiptBinding ;
    mfg:status mfg:Partial .

okg:GraphRecipeDeclaredEvidenceIdentityLearning rdf:type mfg:Observation ;
    mfg:binds okg:GraphRecipeFirstSliceDeclaredEvidenceIdentity ;
    mfg:derivedFrom okg:GraphRecipeFirstSliceConformanceResult ;
    mfg:derivedFrom okg:GraphRecipeReportBoundSourceRefreshObservation ;
    mfg:derivedFrom okg:GraphRecipeReportDependencyClosedRefreshObservation ;
    mfg:derivedFrom okg:GraphRecipeReportReleaseBoundaryRefreshObservation ;
    mfg:informedBy okg:GraphRecipeSelectedManifestReceiptBinding ;
    mfg:status mfg:Partial ;
    mfg:supersedes okg:GraphRecipeExactExecutionIdentityLearning .

okg:GraphRecipeIncompleteExecutionEnvironmentClosureObservation
    rdf:type mfg:Observation ;
    mfg:binds okg:GraphRecipeFirstSliceDeclaredEvidenceIdentity ;
    mfg:status mfg:Open .

okg:OntologyToPopulationCompositionSeamEvidence rdf:type mfg:Observation ;
    mfg:derivedFrom okg:GraphRecipeFirstSliceConformanceResult ;
    mfg:tests mfg:ComponentBoundaryConformance ;
    mfg:tests mfg:CompositionSeamConformance ;
    mfg:status mfg:Partial .

mfg:FrontendNeutralityExperiment
    rdf:type mfg:ComponentBoundaryConformanceExperiment ;
    mfg:informedBy okg:GraphRecipeExperimentalLearning .

okg:LogicalDerivationConformance
    rdf:type mfg:ComponentBoundaryConformanceExperiment ;
    mfg:informedBy okg:GraphRecipeExperimentalLearning .

okg:NoBypassConformance
    rdf:type mfg:ComponentBoundaryConformanceExperiment ;
    mfg:informedBy okg:GraphRecipeExperimentalLearning .

okg:GraphRecipeTerminalABI rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

okg:PopulationPlanAssemblyScope rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

okg:LocalReferenceDependencyRule rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

okg:MultivalueCanonicalizationRule rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

okg:GraphRecipeCISplit rdf:type mfg:DesignObject ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-D007 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:requiredBy okg:GE-010 ;
    mfg:selects okg:GraphRecipeTerminalABI ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-D008 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:requiredBy okg:GE-030 ;
    mfg:selects okg:PopulationPlanAssemblyScope ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-D009 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:requiredBy okg:GE-020 ;
    mfg:requiredBy okg:GE-050 ;
    mfg:selects okg:LocalReferenceDependencyRule ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-D010 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:requiredBy okg:GE-040 ;
    mfg:selects okg:MultivalueCanonicalizationRule ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-D011 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:requiredBy okg:GE-100 ;
    mfg:selects okg:GraphRecipeCISplit ;
    mfg:status mfg:AcceptedDesign .

okg:GraphRecipeCoreCIGate
    rdf:type mfg:TestObligation ;
    mfg:binds okg:GraphRecipeReleaseWorkflowStep ;
    mfg:binds okg:GraphRecipeTestsWorkflowStep ;
    mfg:dependsOn okg:GraphRecipeConformanceFixture ;
    mfg:informedBy okg:GraphRecipeFirstSliceConformanceResult ;
    mfg:status mfg:Implemented .

okg:GraphRecipeRuffGate rdf:type mfg:TestObligation ;
    mfg:tests okg:GraphRecipeResearchRunner ;
    mfg:status mfg:Implemented .

okg:GraphRecipeTestsWorkflowStep rdf:type mfg:DesignObject ;
    mfg:binds okg:GraphRecipeConformanceFixture ;
    mfg:binds okg:GraphRecipeRuffGate ;
    mfg:status mfg:Implemented .

okg:GraphRecipeReleaseWorkflowStep rdf:type mfg:DesignObject ;
    mfg:binds okg:GraphRecipeConformanceFixture ;
    mfg:binds okg:GraphRecipeRuffGate ;
    mfg:status mfg:Implemented .

okg:GraphRecipeNextExperiment rdf:type mfg:DesignObject ;
    mfg:binds okg:GE-030 ;
    mfg:dependsOn okg:GraphRecipeFirstSliceConformanceResult ;
    mfg:status mfg:Open .

okg:LutraToolLock rdf:type mfg:DesignObject ;
    mfg:status mfg:Open .

okg:LutraDifferentialGate
    rdf:type mfg:TestObligation ;
    mfg:dependsOn okg:GraphRecipeConformanceFixture ;
    mfg:dependsOn okg:LutraToolLock ;
    mfg:status mfg:Open .

okg:SecondBackendConformance rdf:type mfg:TestObligation ;
    mfg:status mfg:Open .

okg:GraphRecipeImplementationPromotion
    mfg:dependsOn okg:GraphRecipeCoreCIGate ;
    mfg:dependsOn okg:LutraDifferentialGate ;
    mfg:dependsOn okg:SecondBackendConformance ;
    mfg:status mfg:Open .
```
