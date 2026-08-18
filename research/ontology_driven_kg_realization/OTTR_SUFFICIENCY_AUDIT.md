# OTTR sufficiency audit for Malleus GraphRecipe

Status: reviewer evidence supporting accepted decision `OKG-D001`

Inspected: 2026-08-17

Evidence cutoff: 2026-08-17

Public ancestry base: `27ca54c33fe705827bc845e876cb6ff24293c8f0`.
The reviewed GraphRecipe source bytes are identified by the conformance report
and checksum set, not by a self-referential release commit.

## 1. Result

OTTR is sufficient for the deliberately narrow GraphRecipe role: typed,
finite, reusable topology expansion. It is not a complete ontology-to-KG
protocol and should not be made into one.

The recommended decision is:

> Use stOTTR 0.1.4 as the only authored GraphRecipe representation in v0,
> interpreted under mOTTR 0.1.2 and the rOTTR 0.2.0 term and type model. Define
> a restrictive Malleus profile and a closed Malleus construction base
> vocabulary. Do not create a native recipe DSL, support multiple recipe
> frontends, or fork OTTR.

The author accepted `OKG-D001` on 2026-08-17. The exact selected profile is in
[`design/GRAPH_RECIPE_OTTR_PROFILE.md`](../../design/GRAPH_RECIPE_OTTR_PROFILE.md).

## 2. What the primary sources establish

The 2024 OTTR resource paper defines templates as typed parameterized patterns
expanded recursively by term substitution. Template dependencies must be
acyclic. Expansion terminates in base templates, whose instances are
interpreted by an implementation in a target representation. The paper uses
RDF triples, but explicitly gives RDF quads, OWL expressions, tabular rows,
and SQL inserts as possible alternative base-template interpretations.

That last point matters. Malleus can define terminal construction facts and
interpret them as a target-neutral operation plan without changing OTTR's
grammar or expansion semantics.

The stable stOTTR 0.1.4 syntax supplies:

1. Named templates and base templates.
2. Typed parameters.
3. Optional and non-blank modifiers.
4. Explicit defaults.
5. Lists and list expansion.
6. Template annotations.
7. Nested template instances.

The mOTTR model supplies validity conditions for template libraries and
datasets: consistent typing, variable safety, referential integrity,
acyclicity, and well-foundedness. rOTTR supplies the RDF term and type model.
The standard rOTTR terminal is `ottr:Triple`; the Malleus profile deliberately
uses the abstract base-template extension point instead.

Primary sources:

1. [OTTR 2024 resource paper](https://drops.dagstuhl.de/entities/document/10.4230/TGDK.2.2.5)
2. [OTTR paper, HTML text](https://drops.dagstuhl.de/storage/08tgdk/tgdk-vol002/tgdk-vol002-issue002/html/TGDK.2.2.5/TGDK.2.2.5.html)
3. [stOTTR 0.1.4](https://spec.ottr.xyz/stOTTR/0.1.4/)
4. [mOTTR 0.1.2](https://spec.ottr.xyz/mOTTR/0.1.2/)
5. [rOTTR 0.2.0](https://spec.ottr.xyz/rOTTR/0.2.0/)

## 3. Requirement test

| Requirement | OTTR supplies | Malleus must supply | Verdict |
|---|---|---|---|
| Typed parameters | Basic, list, and least-upper-bound types with compatibility checks | Effective-contract type and slot binding | Sufficient with a thin binding |
| Reusable topology | Nested template composition and recursive expansion | Locked dependency closure and expansion budget | Sufficient |
| Finite expansion | Valid libraries are acyclic and well-founded | Resource limits and fail-loud diagnostics | Sufficient |
| Optional values and defaults | `none`, optional parameters, and declared defaults | Restrictions that prevent silent removal of required members; retained default provenance | Sufficient with restrictions |
| Repeatable collections | `cross`, `zipMin`, and `zipMax` list expansion | v0 permits bounded `cross` only; canonical output ordering | Sufficient with restrictions |
| Stable recipe identity | Template IRIs and library lifecycle metadata | Source digest, canonical effective digest, profile identity, and locked closure | Thin binding required |
| Stable invocation identity | A named template call with typed arguments | A content-addressed identity formula | Thin binding required |
| Relation topology | Terminal parameterized statements can describe records and endpoints | Closed construction base vocabulary and endpoint validation | Sufficient |
| Non-RDF graph backends | Abstract base templates admit other interpretations | Malleus operation assembly and backend projection | Sufficient for recipes, not direct backend output |
| Deterministic operation order | Expansion denotes a set, not execution order | Explicit dependencies and stable topological sorting | Outside OTTR by design |
| Source binding | Separate OTTR batch formats exist | `SourceMappingContract` and `PopulationPlan` | Outside GraphRecipe by design |
| Identity and collisions | No domain identity policy | `IdentityResolutionPolicy` | Outside GraphRecipe by design |
| Provenance | Definition metadata and annotations | Source, invocation, expansion-path, and operation derivation records | Thin binding required |
| Atomicity and admission | No graph transaction semantics | Complete plan, staging, monitors, assent, and materialization | Outside GraphRecipe by design |
| General conditions | Presence-driven omission, not a business-rule language | Population selection records value-dependent decisions | Sufficient for narrowed v0 |
| Mutation, retirement, merge | No mutation semantics | Companion recipes and `EvolutionPlan` | Outside GraphRecipe by design |
| Ontology evolution | Template lifecycle metadata only | Dependency-closed impact, replanning, and migration | Outside GraphRecipe by design |

The exclusions are boundaries, not open choices. OTTR becomes sufficient only
because GraphRecipe is not asked to perform mapping, identity resolution,
admission, or migration.

## 4. Why the alternatives are rejected for v0

### Native Malleus recipe language

Rejected. It would duplicate typed parameters, template nesting, expansion,
annotations, and library lifecycle before Malleus has evidence that OTTR is
missing a load-bearing topology feature.

### Multiple authored frontends

Rejected. More frontends would multiply parsing, canonicalization, diagnostic,
and conformance work before one recipe path is demonstrated. A compiled model
remains an internal derived artifact, not another authored format.

### OTTR fork

Rejected. Malleus needs a profile, terminal interpretation, identities,
diagnostics, and protocol envelopes. None requires new OTTR grammar or altered
macro-expansion semantics.

### RDF triples as the terminal construction language

Rejected for v0. The Malleus graph gate consumes typed record operations,
including relation endpoints and record properties. Translating every recipe
through RDF triples would add an unnecessary reconstruction step and could
hide operation identity or atomic grouping. RDF remains a backend projection.

### SPARQL `CONSTRUCT` as the canonical recipe language

Rejected for v0. It is valuable for graph-to-graph transformation, but it
couples recipe execution to an input graph and query semantics. GraphRecipe
needs reusable typed topology independent of a particular source-query model.

## 5. Tooling boundary

The specifications are normative. Lutra is a differential oracle, not the
semantic authority and not a mandatory dependency for adopters that consume
compiled recipes.

The research fixture should pin
`xyz.ottr.lutra:lutra-cli:0.6.20` by artifact checksum in reproducible
configuration. Maven Central identifies it as the OTTR reference
implementation. No manual download or mutable `latest` resolution is allowed.

Sources:

1. [Lutra CLI 0.6.20 on Maven Central](https://central.sonatype.com/artifact/xyz.ottr.lutra/lutra-cli/0.6.20)
2. [Lutra core 0.6.20 Javadocs](https://javadoc.io/doc/xyz.ottr.lutra/lutra-core/0.6.20)

The language decision does not select Lutra as a shipped runtime dependency.
That requires a separate implementation and licensing decision after the
profile fixture exists.

## 6. Required conformance evidence

The first implementation must demonstrate all of the following:

1. Positive fixtures have OTTR-equivalent expansion under the pinned Lutra
   oracle and the Malleus compiler for their shared semantics.
2. Malleus may reject valid general OTTR outside the profile. It never accepts
   a document invalid under the pinned specifications.
3. Cycles, unknown templates, arity errors, type errors, mandatory `none`,
   blank-node output, unlocked dependencies, unsupported base templates,
   duplicate member identities, unresolved contract symbols, and cyclic
   operation dependencies fail with stable codes.
4. Whitespace, comments, prefix aliases, declaration order, and safe variable
   alpha-renaming do not change the effective recipe digest.
5. Any source-byte change still changes the source-artifact digest.
6. Repeated locked compilation produces the same effective recipe, invocation,
   terminal-member set, derivation traces, proposed-operation sequence, and
   construction-plan digest.
7. Every proposed operation traces to one invocation, recipe member,
   effective contract, and expansion path.
8. Duplicate derivations produce either a declared idempotence result or a
   typed diagnostic. They cannot disappear silently through set semantics.
9. Expansion and plan validation finish before staging begins.
10. A failed staged operation leaves the base graph unchanged.
11. A recipe revision classifies every dependent invocation and plan for
    revalidation or replanning.
12. One logical recipe projects through the in-memory backend and one second
    backend without changing its logical topology.

The OTTR paper itself lists a formal conformance suite as future work. Malleus
therefore retains its own profile fixtures and differential results as evidence
rather than treating one tool's output as proof.

## 7. Objective revisit triggers

Reopen `OKG-D001` only when evidence satisfies at least one trigger:

1. Two accepted use cases require value-dependent branching inside a recipe,
   and population-level selection causes measured duplication or semantic loss.
2. An accepted domain requires tuple, map, struct, or term-function values that
   cannot be represented without distorting its effective contract.
3. An intended consumer must execute recipes against a non-RDF target without
   the Malleus operation adapter.
4. A required use case needs deletion, mutation, reverse matching, or merge as
   recipe semantics rather than as evolution semantics.
5. Differential tests find an irreconcilable disagreement among the pinned
   specification, Lutra, and the Malleus compiler.
6. Profile annotations or base templates begin to add grammar, arbitrary
   expressions, or control flow. That would constitute a language fork.
7. A pinned real workload exceeds its declared expansion or determinism budget.
8. A stable OTTR release adds a relevant missing facility, including named
   arguments, tuples, formal module locks, non-RDF expansion, term functions,
   conformance tests, or incremental updates.
9. Positional invocation causes repeated measured binding defects despite
   signature validation.
10. The Malleus terminal vocabulary prevents required reuse by an external
    OTTR ecosystem consumer.

An idea, preference, or newly available language is not enough. The decision
is stable until a trigger is backed by an addressable observation.
