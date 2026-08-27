# Graph Realization session checkpoint

Checkpoint ID: `OKG-CP001`

Recorded: 2026-08-17T17:48:31-0700

Updated: 2026-08-17 after author acceptance of `OKG-D007` through `OKG-D012`,
adoption of the Malleus Unix modularity doctrine, and dependency-closed refresh
of the research-local GraphRecipe first-slice evidence

Purpose: preserve the accepted baseline, the larger reinforcement program,
the GraphRecipe TDD evaluation result, and the exact post-evaluation resumption
point.

Authority: resume aid only. Accepted design authority remains the decision
records and canonical design graph. Shipped capability remains code, tests,
and `malleus.IMPLEMENTATION_STATUS`.

## 1. Repository coordinate and live-worktree boundary

Public ancestry base: `27ca54c33fe705827bc845e876cb6ff24293c8f0`.
This is an ancestry base only, not the tested implementation snapshot. The
intended release locator is `v0.11.0`; exact report, file, and checksum
identities are authoritative.

Canonical design graph: [`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl),
revision 17,
`sha256:4198a705992f9062c3fec296cc7115aba5a0ed520b1eff06514076cdec6725ac`

The 0.11.0 consolidation after that baseline adds precision-aware valid time,
the accepted `OKG-D012` maintainer doctrine, explicit release guardrails, and
the versioned package boundary. Private literature substrate, quarantined
concurrent-writer evidence, historical inquisition reports, cost research,
roadmap edits, and paper-bound execution-bundle edits remain outside the
release commit and must not be deleted or published by implication.

The completed first slice added research-local GraphRecipe code, tests, frozen
fixtures, a conformance report, and offline workflow steps. It did not add a
public API, a packaged runtime module, a shipped ontology term, a package
version, or a paper claim. The implementation remains outside the public
Malleus package and release artifacts.

## 2. Accepted decisions at the checkpoint

### `OKG-D000`: ontology-driven KG realization is a Malleus pillar

Accepted: 2026-08-17.

The pillar is named ontology-driven KG realization. Its mechanism is the Graph
Realization Protocol. The name avoids the false claim that an ontology alone
contains source mappings, identities, recipes, instances, or migration intent.

The compiler has no privileged graph write path. It may only produce an exact
plan that enters existing structural staging, monitoring, decision, and
materialization.

### `OKG-D001`: OTTR is the sole GraphRecipe language for v0

Accepted: 2026-08-17.

Selected:

1. stOTTR 0.1.4 as the only authored representation.
2. mOTTR 0.1.2 expansion semantics.
3. rOTTR 0.2.0 RDF term and type model.
4. A restrictive Malleus GraphRecipe Profile v0.
5. A closed Malleus construction base vocabulary.

Rejected:

1. A native Malleus recipe DSL.
2. Multiple authored recipe frontends in v0.
3. An OTTR grammar or expansion-semantics fork.
4. RDF triples as a mandatory intermediate graph-construction language.
5. SPARQL `CONSTRUCT` as the canonical recipe language.

The decision is stable until one of its objective revisit triggers gains
addressable evidence. It is not reopened because another language exists or an
implementation is inconvenient.

### `OKG-D007` through `OKG-D011`: GraphRecipe experiment microdecisions

Accepted by the author on 2026-08-17:

1. `OKG-D007`: terminal members, operation kinds, record types, and properties
   use IRIs; graph record IDs remain strings.
2. `OKG-D008`: assembly spans the complete atomic `PopulationPlan`, and one
   invocation may add properties to a member anchored by exactly one `Record`
   elsewhere in that plan.
3. `OKG-D009`: every reference to a record created in the same plan requires
   `DependsOn`, including relation endpoints, signal bearers, and class-valued
   properties.
4. `OKG-D010`: unordered multivalues canonicalize as semantic sets while all
   derivation paths remain; ordered values preserve contract-declared order.
5. `OKG-D011`: the offline Malleus fixture corpus is the primary CI gate, with
   one separate pinned Lutra differential job after its exact tool lock exists.

These records remain accepted design. The research-local `GE-000` through
`GE-020` slice exercises only their first-slice clauses. It does not implement
the full profile or promote a public capability. Later changes require
addressable counterevidence, superseding decisions, and dependency-closed
impact.

### `OKG-D012`: LinkML is selected behind a replaceable contract boundary

Accepted: 2026-08-17.

Official, execution-identified LinkML is the sole first-party human-authored
contract frontend for v0. It compiles retained source bytes under a versioned,
fail-closed support profile into a frontend-neutral
`ContractCompilationResult`. Runtime graph construction consumes the compiled
effective contract and must not require LinkML.

LinkML receives no privileged graph or admission path. A custom frontend may
replace it if it emits the same normative intermediate, diagnostics, and
lineage and passes the same boundary conformance suite. Direct facts remain an
internal bootstrap and conformance input, not a competing first-party language.

The governing software doctrine adapts Eric S. Raymond's *The Art of Unix
Programming*: small stages, artifact-mediated composition, separation of
policy and mechanism, inspectable state, deterministic generation, and
explicit extension. Malleus rejects permissive semantic guessing. Unsupported
or ambiguous meaning fails before effects.

## 3. Current protocol boundary

```text
contract source bytes
  -> exact frontend, resolver, support profile, and diagnostics
  -> ValidatedContractFactSet
  + NormativeAdmissionProfile
  -> EffectiveContract
  -> LogicalGraphContract

LogicalGraphContract
  + GraphBackendProfile
  -> GraphSchemaProjection + coverage

CompiledGraphRecipe
  + SourceMappingContract
  + TransformationContract
  + IdentityResolutionPolicy
  + SourceConflictPolicy
  -> PopulationPlan

PopulationPlan
  + source artifacts
  + backend projection
  -> GraphConstructionPlan
  -> ordered existing ProposedOperation values
  -> isolated CandidateSubgraph
  -> monitors and epistemic decision
  -> accepted GraphRealization
  -> GraphRealizationAttestation
```

OTTR owns only finite typed topology expansion. It does not own mapping,
transformation, identity, collision handling, provenance, ordering, atomicity,
admission, authorization, or evolution.

Generated LinkML artifacts remain optional projections. A future adopter may
consume a compiled effective-contract artifact without running LinkML. This is
accepted design under `OKG-D012`, not current implementation.

## 4. High-level program for this session

The session is reinforcing Malleus as a library-protocol before allowing the
result to percolate into the active paper. The method is:

1. Reconstruct the exact implemented boundary from code and tests.
2. Reconstruct relevant literature and standards from primary evidence.
3. Separate inherited mechanisms from candidate Malleus composition.
4. Express design objects, decisions, dependencies, statuses, and revisit
   triggers in the canonical graph.
5. Let the author close bounded decisions.
6. Build the smallest research-local experiment that could falsify each
   selected abstraction.
7. Retain inputs, expected outputs, actual outputs, diagnostics, and execution
   identity as evidence.
8. Feed experiment results back into the design graph and literature Recon
   record.
9. Issue versioned downstream adoption packets only after the governing
   profile and conformance fixture stabilize.
10. Update public Malleus documentation and paper claims only after code and
    evidence pass their own authority gates.

This is the dogfooding loop: Malleus design is itself represented as typed,
versioned, dependency-bearing knowledge whose revisions cannot silently erase
prior decisions.

## 5. GraphRecipe TDD evaluation result

Experiment program ID: `OKG-X001`.

Question answered in the affirmative:

> Can the accepted OTTR profile be developed test-first through a ladder of
> ontology, recipe, mapping, planning, staging, and evolution experiments whose
> fixtures are useful both interactively and in CI?

Required evaluation outputs:

1. A minimal ontology-to-empty-instance-graph boundary test.
2. A simple one-entity recipe and exact expected network.
3. A two-entity, one-relation dependency-order test.
4. Property, optional add-on, list, default, identity, and collision tests.
5. Negative profile tests with stable diagnostics.
6. Deterministic source, effective-recipe, invocation, plan, and graph digests.
7. A complex multi-recipe population test.
8. An ontology and recipe evolution impact test.
9. A second-backend projection test.
10. One interactive runner that consumes the same fixtures and assertions as
    CI rather than creating a separate demo path.

The evaluation exposed and the author resolved these design gaps:

1. Ontology-only input must yield a legal logical graph contract and an empty
   instance graph. Any populated node would expose an implicit population
   decision.
2. `OKG-D010` defines canonicalization for unordered and ordered multivalued
   property facts before implementation.
3. `OKG-D008` defines how an add-on recipe contributes properties to a member
   anchored elsewhere in the same atomic plan.
4. `OKG-D007`, `OKG-D009`, and `OKG-D011` fix the terminal ABI, local-reference
   dependency rule, and CI split.

These gaps became explicit test obligations. The completed first slice now
freezes `GE-000` through `GE-020` as 10 case receipts over 149 checksummed
corpus files. Seven declared metamorphic obligations map to executable tests.
The dedicated slice passed 40 tests, the relevant core selection passed 257
tests with 2 skips, and the full configured suite recorded 807 passes with 2
skips.

The conformance report is
[`FIRST_SLICE_CONFORMANCE_REPORT.json`](../research/ontology_driven_kg_realization/experiments/graph_recipe/FIRST_SLICE_CONFORMANCE_REPORT.json),
identified by
`sha256:6d41cd245234dc3b77bbbc5a5c16529d197aa9db2a03f1525c1b1602d17c82a8`.
Its checksum set is identified by
`sha256:aa5c904f79363b68bab9d82a2b6b027748ffe25358ef3fead5c5ba7b3dc7a3f2`.
Each case receipt binds the selected manifest's exact source-byte identity.
The report binds that selected-manifest identity to the complete canonical
receipt identity, which makes case selection part of declared evidence
identity rather than an ambient runner choice. That identity covers exact
declared source bytes, selections, receipts, and recorded observations; it does
not establish complete transitive dependency or execution-environment closure.

Removing one unused runner import changed the bound runner bytes. The hard
identity guard rejected the then-stale report and produced retained identity
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`,
which supersedes
`sha256:41b180b273ecc24e59af769736519c071707134beecf91ae60ce10a1092a1ae0`.
A later bound-source refresh produced
`sha256:9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0`,
which supersedes the retained
`sha256:64a16f2e5089325c433b14dfc683383aeb9592372da012a7ea13babba67a6a97`
identity. The active release-boundary refresh binds the final declared sources,
three relevant-core test files, current observations, and the public-snapshot
privacy guard; its identity above supersedes
`sha256:9790502676caf7279ba42d85ede91c0326b5c99adb4e8f590dcbe8409a061eb0`.
Both dedicated workflow steps run Ruff over the complete research-local
GraphRecipe directory before running the 40-test slice.

The full configured suite is green, but its result is an observation bound by
the report rather than a complete suite-source, transitive-dependency, or
execution-environment identity. The report does not attest a clean commit or
independently reproducible release snapshot.

The author's cross-protocol completeness intuition is retained separately as
the candidate falsifiable `ProtocolCompositionCompleteness` claim. The first
slice supplies partial evidence only for component-boundary conformance, the
ontology-to-population composition seam, and known-exclusion accounting.
Declared-component coverage, full cross-protocol scenarios, and
dependency-closed change conformance remain candidate obligations. GraphRecipe
results can inform other component boundary and conformance experiments, but
they cannot prove universal completeness or discharge tests for those
components. Promotion remains blocked by retained counterevidence until the
claim is narrowed, retracted, or superseded.

## 6. Rabbit-hole non-goals

The experiment does not silently:

1. Promote a public GraphRecipe API.
2. Add a mandatory Java or Lutra runtime dependency.
3. Treat Lutra output as semantic authority.
4. Select the second production backend.
5. Resolve the full contract-kernel object model by fixture accident.
6. Create a second protocol ledger.
7. Modify downstream projects.
8. Rebase the paper from Malleus 0.9.0 to 0.10.0 or later worktree state.
9. Claim improved model reasoning or general graph-construction quality.

The first experiments may use the current `OntologyRegistry` as a temporary
frontend. Expected artifacts must still name the future frontend-neutral
boundary so the fixture does not make LinkML mandatory by accident.

## 7. Exact resumption point after the experiment thread

The next GraphRecipe experiment is `GE-030`, optional-property and anchored
add-on semantics. That branch does not reorder or block the main pillar. The
main reinforcement program resumes at the contract-kernel object model, then
continues through `OKG-D002` to `OKG-D006` in the sequence below. The first
step has partial first-slice evidence, not full coverage.

Resume the main reinforcement program here:

1. Feed `OKG-X001` observations, typed gaps, and
   `GraphRecipeExperimentalLearning` into the component coverage matrix and
   other boundary/conformance experiments, preserving failed hypotheses.
2. Reassess only the `OKG-D001` clauses touched by recorded revisit evidence.
   Otherwise keep the accepted profile fixed.
3. Close the exact contract-kernel object model and seed metamodel decision,
   keeping the `OKG-D012` frontend boundary fixed. The first contract slice
   must include the test-only alternate producer and clean LinkML-free runtime
   check required by that decision.
4. Close `OKG-D002`, the second backend, using experiment evidence rather than
   preference.
5. Close `OKG-D003`, construction-history placement. Current evidence favors a
   content-addressed plan artifact referenced through the existing
   `ProtocolLedger`.
6. Close `OKG-D004`, identity-policy scope. Current evidence favors one
   explicit policy per `PopulationPlan`, with declared sub-policy precedence.
7. Close `OKG-D005`, virtual realization status.
8. Close `OKG-D006`, the bootstrap contract for realization artifacts.
9. Continue the broader packages in dependency order: contract evolution,
   evidence integrity, dependency-closed revision, automated change authority,
   and execution identity. Effect delivery remains a separate downstream
   branch.
10. Generate or refresh downstream adoption packets. Do not edit another
    project until its packet's governing profile and conformance bundle are
    current and the author authorizes that project change.
11. Project stable, implemented behavior into existing public docs and then
    into the paper's own claim-evidence process.

Do not restart literature reconstruction, local fleet inspection, or OTTR
alternatives research when resuming. Those passes are already retained. Begin
from the accepted decisions and experiment evidence.

## 8. Durable artifacts at the checkpoint

Public-safe design and evidence:

1. [`ONTOLOGY_DRIVEN_KG_REALIZATION.md`](ONTOLOGY_DRIVEN_KG_REALIZATION.md)
2. [`GRAPH_RECIPE_OTTR_PROFILE.md`](GRAPH_RECIPE_OTTR_PROFILE.md)
3. [`PROTOCOL_FOUNDATION_GRAPH.md`](PROTOCOL_FOUNDATION_GRAPH.md)
4. [`PROTOCOL_FOUNDATION_GRAPH.ttl`](PROTOCOL_FOUNDATION_GRAPH.ttl)
5. [`OTTR_SUFFICIENCY_AUDIT.md`](../research/ontology_driven_kg_realization/OTTR_SUFFICIENCY_AUDIT.md)
6. [`GRAPH_RECIPE_TDD_EXPERIMENTS.md`](GRAPH_RECIPE_TDD_EXPERIMENTS.md)
7. [`FIRST_SLICE_CONFORMANCE_REPORT.json`](../research/ontology_driven_kg_realization/experiments/graph_recipe/FIRST_SLICE_CONFORMANCE_REPORT.json)
8. [`checksums.json`](../conformance/graph_recipe/v0/checksums.json)

Private local evidence, bound from public design by digest only:

1. Implementation audit:
   `sha256:9b62ed651e0b571a3301da559494d55fd9fe35f7790016a64cb163f43214f47a`
2. Downstream adoption registry:
   `sha256:4b373134bb7af272216cb788c28180e07a333530e5b6caf885f8243d33fd4d41`

The private files are untracked and not durable off-machine. Moving them to a
private repository or encrypted evidence store requires an explicit decision.
Do not preserve them by publishing private workspace paths.

## 9. Checkpoint graph

```turtle
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix mfg: <https://malleus.dev/foundation-graph/> .
@prefix okg: <https://malleus.dev/ontology-kg-realization/> .

okg:OKG-D000 rdf:type mfg:DecisionRecord ;
    mfg:decidedBy mfg:Author ;
    mfg:decisionDate "2026-08-17" ;
    mfg:selects okg:OntologyDrivenKGRealization ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-CP001 rdf:type mfg:DesignObject ;
    mfg:binds okg:OKG-D000 ;
    mfg:binds okg:OKG-D001 ;
    mfg:binds okg:OKG-D007 ;
    mfg:binds okg:OKG-D008 ;
    mfg:binds okg:OKG-D009 ;
    mfg:binds okg:OKG-D010 ;
    mfg:binds okg:OKG-D011 ;
    mfg:binds okg:OKG-D012 ;
    mfg:binds okg:OntologyDrivenKGRealization ;
    mfg:binds okg:MalleusGraphRecipeProfileV0 ;
    mfg:binds okg:GraphRecipeFirstSliceEvidenceBundle ;
    mfg:status mfg:AcceptedDesign .

okg:OKG-X001 rdf:type mfg:TestObligation ;
    mfg:tests okg:MalleusGraphRecipeProfileV0 ;
    mfg:dependsOn okg:OKG-D001 ;
    mfg:produces okg:GraphRecipeConformanceFixture ;
    mfg:produces okg:GraphRecipeExperimentalLearning ;
    mfg:status mfg:Partial .

okg:MainProgramResumption rdf:type mfg:DesignObject ;
    mfg:dependsOn okg:OKG-X001 ;
    mfg:dependsOn okg:OKG-CP001 ;
    mfg:informedBy mfg:ProtocolCompositionCompleteness ;
    mfg:informedBy okg:GraphRecipeExperimentalLearning ;
    mfg:status mfg:Open .
```
