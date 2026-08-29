# Contract compiler execution program

Status: operator-approved execution program, implementation remains gated

Base repository coordinate: `c410f11229e7c33a4fab9ebdfc9e2e109f18cbf7`

The base commit predates these governance records. The sealed authority snapshot
in [`integration.json`](integration.json) identifies the result commit and exact
source bytes that introduced them.

Current progress is the bounded projection in
[`overseer/status.md`](overseer/status.md). Append-only history is stored as
schema-valid blocks under [`overseer/entries/`](overseer/entries/), governed by
[`overseer/README.md`](overseer/README.md) and
[`overseer/ledger.schema.json`](overseer/ledger.schema.json). The former
handover ledger is a frozen pointer, not a second event store.

CC-000 is the machine gate for parallel work. The complete 69-workstream DAG,
reserved scopes, owner-separation rules, active card digests, ledger checkpoint,
and selected results live in [`integration.json`](integration.json), validated
against [`integration.schema.json`](integration.schema.json). Active cards under
[`workstreams/`](workstreams/) say who may edit which exact FILE or TREE paths,
what kind of work is authorized, and whether a candidate is absent,
quarantined, eligible, or integrated. This gate is repository governance. It is
not the OD-001 runtime consumer-bundle format.

The first acceptance example is intentionally a refusal. The final diff of the
local CC-X03 exploration contains only two generic source-boundary files, but
an intermediate commit introduced four unapproved themed files and later
deleted them. CC-000 inspects every commit's touched paths, quarantines that
history, and keeps CC-R01 blocked. A worker cannot erase an ownership violation
by deleting the file before handoff.

Semantic authority remains the canonical graph referenced by
[`PROTOCOL_FOUNDATION_GRAPH.md`](../PROTOCOL_FOUNDATION_GRAPH.md). This program
orders work, tests, ownership, and decision gates. It does not replace that
graph, the implementation status, or code contracts. Accepted decisions are
promoted into the canonical graph before production implementation relies on
them.

## Outcome

Malleus will use LinkML as its first-party compiler frontend and will execute
from a deterministic, LinkML-free contract artifact. The public runtime root
will eventually be an `EffectiveContract`, not an `OntologyRegistry`.

The work begins as a research-local conformance slice. Production cutover waits
for the remaining semantic decisions, independent expected facts, the selected
hard-break reader, packaging, and an artifact-backed runtime path that cannot
import LinkML.

The target boundary is:

```text
retained sources + one explicitly selected resolver profile
  -> ContractFrontend
  -> ContractCompilationResult
       facts
       annotations
       diagnostics
       provenance
  -> metamodel validation and canonical fact encoding
  -> ValidatedContractFactSet
       + NormativeAdmissionProfile
  -> EffectiveContract
  -> EffectiveContractArtifact
  -> runtime views
       identity
       type system
       record shape validation
       graph admission
  -> KnowledgeGraph, Staging, Logic, Assent, Recon, OCR
```

No public object after `ContractFrontend` may contain a LinkML class. Every
frontend must pass the same generic neutral-result metamodel, canonicalization,
artifact, and runtime conformance obligations. Each source language has its own
named and versioned source support profile and source corpus. A custom frontend
need not pass the LinkML-specific corpus unless it claims that LinkML profile.
Stage protocols alone do not imply that arbitrary implementations can be mixed
safely.

## Accepted direction

The operator accepted these directions in the planning conversation. Revision
15 of the canonical graph records them, with AD-002 mapped to the existing
`OKG-D012` decision. They remain design authority, not claims about shipped
code.

| ID | Direction |
|---|---|
| AD-001 | Replace `OntologyRegistry` as the public root with `EffectiveContract`. A pre-1.0 API break is acceptable. |
| AD-002 | LinkML is a compiler dependency, not a core runtime dependency. |
| AD-003 | Expose experimental stage protocols, while named whole-pipeline conformance is the compatibility claim. |
| AD-004 | Fail closed on duplicate imported symbols unless a versioned Malleus policy explicitly authorizes the composition. Never inherit implicit last-wins behavior. |
| AD-005 | Use independent upstream PR branches for independent units. Intrinsic specification-to-runtime dependencies use declared sequential or stacked bases. Maintain one exact-commit integration branch. |

`OD-001` accepts one canonical consumer-bundle manifest per consumer. `OD-013`
supplies the one-distribution topology and `OD-006` supplies the closed
three-role composition; `CC-D16` still owns exact fields and byte grammar. Its practical
meaning is explained in
[`decisions.md`](decisions.md#od-001-consumer-bundle-manifest).

Revision 20 also accepts `OD-002` through `OD-008`, `OD-010`, `OD-011`,
`OD-013`, and `OD-014`: exact slot-only adoption; pinned LinkML 1.11.1 as the replaceable
default adapter; a typed persisted-wire hard break; ontology-powered atomic
facts in canonical JSON; three roles in one closed composition and one v0
accepted-temporal epoch; one protected replay-derived governance partition in
the accepted graph with prior-state authorization and no governance-specific
head or query surface; one closed exact-location LinkML v0 support profile and flat
exactly-one expression extension; strong same-role and same-partition class
references, Entity-only relation endpoints, Entity-or-Relation signal bearers,
ordered candidate visibility, and referentially closed temporal views; one
explicit resolver profile with strict
Malleus defaults; one normal distribution including the compiler and LinkML;
and the Quiet Bell Archive fixture/publication boundary. The exact rules and
limitations are in [`decisions.md`](decisions.md).

The operator excluded migration feature development from this foundation block.
`OD-004` now selects a new wire epoch and typed hard break. It forbids a replay
bridge or a new meaning for the old persisted identity field in v0.

## Corrections from independent review

The initial plan was rejected as non-executable. The corrected plan incorporates
these findings.

1. Import resolution is recursive. Parsing reveals more imports, so resolver,
   byte retention, parsing, and graph construction form one controlled loop.
2. Current bundled schemas intentionally redeclare adopted slots. AD-004 therefore
   requires a decision on explicit `adopts: true`, not a blanket duplicate ban
   applied by accident.
3. LinkML and `OntologyRegistry` differ on mixin conflict handling, constraint
   precedence, default ranges, and other cases. Recon parity over 47 classes is
   evidence, not a general semantic proof.
4. `EffectiveContract` identity cannot replace `ontology_hash` inside ledger
   schema version 1. Existing snapshots, candidates, graph bases, logic facts,
   migration receipts, and Recon ledgers bind the old identity grammar.
5. Frozen artifact bytes require the logical vocabulary, symbol identity,
   composition roles, and admission profile to be decided first.
6. Frozen Python dataclasses are not deeply immutable when they contain mutable
   collections. Immutability, purity, determinism, and lack of I/O need
   mechanical tests.
7. Sphinx is a rendered view. The canonical graph, code, tests, validated
   manifests, and implementation status remain the authorities for their
   respective claims.
8. The themed fixture is one vertical demonstration, not its own oracle. The
   conformance suite uses three independent corpora.
9. Adoption is decided from lossless per-module declarations before any LinkML
   global merge can erase duplicate evidence or normalize absent values.
10. The persisted-wire envelope precedes every consumer write-path cutover.

## Recursive compiler topology

The source side is not a row of independent boxes. It is this loop:

```text
root request
  -> resolver returns retained bytes
  -> parser returns one lossless declared module and ordered literal imports
  -> each unseen import returns to the resolver
  -> closure completes only when every import is resolved or refused
  -> deterministic module graph
  -> symbol binding
  -> inheritance, mixins, slot induction, expressions
  -> neutral contract facts
```

The resolver is the only source of bytes. One named, versioned resolver profile
is selected explicitly; strict Malleus resolution is the default and no failure
tries another profile. File and network capabilities are separate explicit
configuration and default deny. The LinkML adapter may use LinkML objects
internally, but it receives bytes from the resolver and emits neutral values.
Tests deny sockets and direct file reads around the frontend and prove that no
hidden loader bypass exists.

Resolver and closure orchestration stay one workstream until this control loop
is proven. Parser, binder, and elaborator seams may be exposed for observation
and testing, but no compatibility claim is made for arbitrary combinations.

The source boundary keeps five identities distinct:

```text
ImportRequest
  parent module instance
  parent import ordinal
  literal import
  base locator

ResolvedSource
  resolved locator
  exact bytes, length, digest, media type
  resolver identity, profile version, configuration identity

ModuleInstance
  exact retained resolved locator string as module instance ID
  source blob ID
  lossless declared module

RootResolution
  requested root locator
  retained resolved locator and source
  resolver identity, profile version, configuration identity

ResolvedImportEdge
  parent module instance
  parent import ordinal
  literal import
  child retained resolved locator
  resolver identity, profile version, configuration identity
```

Within one compilation, module-instance identity is the exact retained resolved
locator string. There is no universal locator normalization. Resolver profile
and configuration identity remain separate compilation provenance. A root has
one retained source record and no invented import ordinal, literal, or edge.
Only an authored import creates a `ResolvedImportEdge`.

The same content at two locators may share a source blob identity while
remaining two module observations. A diamond records both import edges even
when parsing of the shared child is deduplicated. The same module locator with
different bytes refuses. Authored order is provenance only, never a semantic
winner. Every cycle refuses with its complete lineage.

## Identity layers

One hash cannot answer five different questions.

| Identity | Question answered | Typical inputs |
|---|---|---|
| Source identity | Which exact bytes were read? | Byte length, SHA-256, locator as provenance |
| Semantic identity | Which contract meaning was compiled? | Validated facts, canonicalization profile, symbol policy, admission profile |
| Compiler execution identity | Which compiler environment produced it? | LinkML and runtime distributions, exact commits, wheel hashes, dependency lock |
| Consumer bundle identity | Which semantic contract, reader, authority, and migration profile is this consumer running? | Canonical consumer manifest |
| Persisted-wire identity | Which record and replay grammar wrote this data? | Ledger schema, epoch, identity field grammar |

Diagnostics and source spans belong to compilation results and attestations
unless a later decision explicitly makes them semantic. Two frontends may have
different provenance while producing identical validated facts and the same
effective contract.

## Artifact and capability boundaries

The research slice may define experimental neutral values for:

| Boundary | Required content |
|---|---|
| Root retained source | Requested root locator, exact retained resolved locator, bytes, length, digest, media type, resolver profile and configuration identity |
| Imported retained source | Exact retained resolved locator, bytes, length, digest, media type, resolver profile and configuration identity |
| Module instance | Module identity, source blob identity, lossless declarations, ordered imports |
| Resolved import edge | Parent module instance, authored ordinal, literal import, child retained resolved locator, resolver profile and configuration identity |
| Declared module | Supported LinkML declarations before composition, including explicit presence and raw annotations |
| Bound symbols | Qualified identities and explicit composition decisions |
| Elaborated schema | Hierarchy, mixins, induced slots, normalized supported expressions |
| Compilation result | Facts, annotations, diagnostics, provenance, implementation attestation |
| Validated fact set | Canonical neutral facts under exact metamodel and symbol profiles |
| Effective contract | Validated facts plus normative admission profile |
| Runtime artifact | Reloadable, deeply immutable, LinkML-free effective contract |

The runtime consumes narrow views instead of a compiler object:

| Runtime view | Current consumers |
|---|---|
| Contract identity | KG snapshots, candidates, ledger and replay adapters |
| Type system | KG, Logic, Assent, Recon, OCR |
| Record shape validator | KG, Recon, OCR, Assent |
| Graph admission | KG and Staging |
| Compilation provenance | Compiler, Inquisition, audit tooling only |

## Workstream graph

```text
decision gates
  -> documentation and manifest infrastructure
  -> three-corpus conformance authority
  -> recursive source boundary
  -> parser and support profile
  -> binding and elaboration
  -> canonical facts and effective contract
  -> artifact loader and core packaging
  -> versioned persisted-wire envelope
  -> internal consumer cutover
  -> legacy deletion

whole-pipeline conformance
  -> upstream contribution train

release cutover
  -> external adopters
```

Work may run in parallel only where the dependency column permits it.

### Evidence before decisions

| ID | Deliverable | Depends on | Completion evidence |
|---|---|---|---|
| CC-X00 | Inventory reproducible compiler baseline candidates | none | Release and source candidates list Python, both distributions, source archives, and lock feasibility |
| CC-X01 | Lossless observed divergence corpus for selected LinkML baseline and current `OntologyRegistry` | CC-002 | Each case records both outputs without selecting a winner or editing an oracle |
| CC-X02 | Bundled declaration and duplicate scan before global merge | none | Exact module, symbol, raw fields, and adoption marker for every duplicate |
| CC-X03 | Exploratory generic source-boundary RED with isolated microfixtures | none | Findings are nonintegrable until CC-000 registers scope and evidence |
| CC-X04 | Freeze historic 0.11 and 0.13 wire inputs and current-reader observations | none | Immutable membership, checksums, old grammar, and current outcomes without selecting future behavior |

These are measurements, not normative fixtures. They may proceed while
decisions remain open.

### Gate D: operator decisions

| ID | Deliverable | Depends on | Completion evidence |
|---|---|---|---|
| CC-D01 | Promote AD-001 to AD-005 into the canonical design graph | none | Parsed graph, updated digest, projection parity |
| CC-D02 | Close OD-002 explicit adoption policy | CC-X02 | Bundled closure scan and collision matrix agree with policy |
| CC-D03 | Close OD-003 LinkML versus legacy behavior | CC-X01 | Every observed case is classified without changing the measurements |
| CC-D04 | Close OD-004 persisted-wire transition | CC-X04 | Operator-selected outcome matrix for every frozen input, before implementation |
| CC-D05 | Close OD-005 logical fact vocabulary and wire encoding | CC-D01, CC-D02, CC-D03 | Ontology authority, atomic fact and byte grammar, internal candidate identity envelopes, examples, counterexamples, and decision record accepted |
| CC-D06 | Close OD-006 contract roles | CC-D05 | Exact three-role closure, fixed conceptual v0 identity constructors, composition and epoch deltas, structural-only exception, refusal matrix, and deferred wire boundaries accepted |
| CC-D07 | Close OD-007 governance topology | CC-D06 | Protected replay-derived governance partition, pre-event authorization, one external genesis root, direct policy self-amendment refusal, no governance-specific graph/head/query surface, epoch boundary, refusals, and deferred representation accepted |
| CC-D08 | Close OD-008 field classification | CC-D02, CC-D03, CC-D05 | Closed exact-location LinkML v0 profile, exact defaults and source-to-fact mapping, immutable D05 seed plus flat exactly-one extension, deterministic structural IDs, retained-corpus closure, refusals, and expansion workflow accepted |
| CC-D09 | Close OD-009 promotion boundary | CC-D01, CC-D05 | Named evidence gate and namespace policy accepted |
| CC-D10 | Close OD-010 endpoint and generic class-reference semantics | CC-D07 | Strong same-role and same-partition class references, Entity-only endpoints, Entity-or-Relation bearer, ordered candidate visibility, referentially closed temporal views, and exact refusal boundaries accepted |
| CC-D11 | Close OD-011 import identity, order, cycle, resolver, and fallback policy | CC-X03 | Import observations, examples, counterexamples, and exact policy accepted |
| CC-D12 | Close OD-012 exact compiler baseline | CC-X00 | Release coordinate and provenance, Python reproducibility tuple, published root wheel and root-sdist identities, exact transitive build and derivative inputs, deterministic double-build and double-transform profiles, payload and license identity boundary, derived-version and ownership policy, resolver and platform identities, v3 wheel-only runtime closure, offline acceptance suite, and future-replacement boundary selected without materializing bytes |
| CC-D13 | Close OD-013 packaging topology | CC-D01 | Core and compiler installation and verification responsibilities accepted |
| CC-D14 | Close OD-014 themed fixture and publication boundary | none | Working name, vocabulary boundary, authorship/license record, and public gate accepted |
| CC-D15 | Close OD-001 consumer-bundle direction | none | Operator approves one bundle per consumer or explicitly defers it |
| CC-D16 | Close exact consumer-bundle schema and canonical grammar | CC-D06, CC-D13, CC-D15 | Accepted fields, examples, counterexamples, and grammar, or a typed not-applicable record when OD-001 is deferred |

CC-D05 permits computed internal candidate fact and fact-set digests only.
CC-D06 closes the three semantic roles and logical composition identity inputs;
it does not create public identifiers or bytes. CC-D08 completes the candidate
expression-capable fact-identity inputs; public identifier publication still
waits for CC-D09. D10 closes admission design only; normative runtime admission
implementation and diagnostics remain with CC-R06.
No production implementation begins before CC-D09. Research characterization
may proceed without deciding outcomes.

### Wave 0: authority, docs, and conformance infrastructure

| ID | Deliverable | Exclusive scope | Depends on |
|---|---|---|---|
| CC-000 | Validated workstream and integration manifests, ledger schema, DAG and ownership checks | `design/contract_compiler/integration.schema.json`, `integration.json`, `workstreams/`, validation tests | none |
| CC-001 | Sphinx with MyST, autodoc, doctest, strict links, rendered manifests | Docs configuration and docs CI | CC-000 |
| CC-002 | Reproducible selected compiler environment | Materialized selected published root wheels and sdists, exact resolver artifact, unchanged deterministic ANTLR source-build proof, retained upstream `prefixcommons` derivative input, two byte-identical network-denied derived `0.1.12+malleus.1` wheels, payload and license identity proof, v3 derivation record, complete hash-pinned wheel-only runtime closure excluding test packages, retained wheelhouse, immutable OCI identities, platform verification, `pip check`, package and LinkML smokes, and clean offline-install attestation | CC-000, CC-D12 |
| CC-010 | Three-corpus protocol and independent oracle process | `conformance/contract_kernel/v0` manifests and checks | CC-000, CC-D02, CC-D03, CC-D05, CC-D06, CC-D07, CC-D08, CC-D10, CC-D11 |
| CC-011 | Themed vertical source corpus | Themed source files only | CC-010, CC-D14, CC-018 |
| CC-012 | Independently authored themed expected compilation artifacts | Themed source descriptors, import graph, declarations, bindings, elaboration, facts, and artifact oracle only | CC-010, CC-D02, CC-D03, CC-D05, CC-D06, CC-D08, CC-011, CC-021, CC-022 |
| CC-013 | Feature-isolation inputs | Feature-case sources and direct inputs only | CC-010, CC-X01, CC-X02, CC-018 |
| CC-014 | Independently authored feature-case oracles | Feature-case expected values only | CC-010, CC-D02, CC-D03, CC-D05, CC-D08, CC-013, CC-021, CC-022 |
| CC-015 | Neutral-domain source and operation inputs | Neutral-domain sources and inputs only | CC-010, CC-D05, CC-D08, CC-018 |
| CC-016 | Independently authored neutral-domain oracles | Neutral-domain expected values only | CC-010, CC-D05, CC-D06, CC-D08, CC-015, CC-021, CC-022 |
| CC-017 | Independently authored direct-fact conformance input | Direct-fact input only | CC-010, CC-D05, CC-D06, CC-D08, CC-018 |
| CC-018 | Semantic scenario requirements shared by source, direct-input, and oracle owners | Scenario requirements only | CC-010, CC-D05, CC-D06, CC-D08 |
| CC-019 | Themed operation-trace inputs | Themed ordered operations only | CC-010, CC-011, CC-018 |
| CC-020 | Independently authored themed trace outcomes | Expected decisions, diagnostics, state digests, and final records only | CC-010, CC-D07, CC-D10, CC-019 |
| CC-021 | Controlled Small Shop Fulfilment inputs | Exact ontology and domain input bytes only; no expected values, mappings, recipes, operations, outcomes, compiler, runtime, protocol, or accepted graph state | CC-010, CC-D03, CC-D08, CC-D11 |
| CC-022 | Independently authored Small Shop Fulfilment oracle | Expected values only, independently derived after the controlled inputs are complete | CC-010, CC-D02, CC-D03, CC-D05, CC-D06, CC-D08, CC-D10, CC-D11, CC-021 |
| CC-PUB01 | Themed fixture authorship, license, and public-review record | Public fixture text and asset manifest only | CC-011, CC-D14 |

Every source or direct-input workstream has a different owner from its oracle.
The direct-fact owner reads accepted decisions and the metamodel, not oracle
files. One change may not alter compiler code and expected facts unless an
independently reviewed expected-delta manifest explains every semantic change.

Small Shop Fulfilment is the canonical end-to-end consumer. It does not replace
the three independent compiler controls.
Quiet Bell, feature-isolation, and Greenhouse remain independent conformance controls.
CC-021 owns controlled
input bytes only. CC-022 independently authors the Small Shop oracle only after
CC-021 completes. The first research-local realization waits for both.

The running ladder is fixed:

| Case | Required boundary |
|---|---|
| RET-000 | Ontology alone produces no ABox. |
| RET-010 | Create `O1`, distinct physical item `X1`, and `OrderContainsUnit(O1, X1)`. |
| RET-020 | After `I1` and `I2` exist, create `P1` and two invoice-settlement relations. |
| RET-030 | Preserve the supplier-order `B` correction at `e7` and bounded invoice `I2` correction at `e9`. |
| RET-040 | Refuse the `e27` Event-to-Entity correlation with a typed gap. |
| RET-050 | Refuse per-entity Event ordering with a typed gap. |
| RET-060 | Reproduce the accepted result deterministically under later source integration. |

A future ontology-builder/corrector is only a future external proposal producer.
It supplies exact attested candidate bytes to normal review
and protocol handling. The deterministic compiler never invokes it.
Replay never invokes it. It has no dependency edge in this graph, and this program authorizes no skill implementation.

### Wave 1: research-local compiler proof

| ID | Deliverable | Depends on | Mandatory AT slice |
|---|---|---|---|
| CC-R01 | Controlled retained-source and recursive import boundary | CC-000, CC-X03, CC-D11, CC-010, CC-011, CC-012, CC-013, CC-014, CC-015, CC-016, CC-021, CC-022 | Nested import, diamond, missing import, network refusal, no try-next profile, every import ordinal and edge, same-locator/different-bytes refusal, different-locator/same-bytes distinction, directed-cycle lineage refusal, deterministic byte observations |
| CC-R02 | LinkML parser adapter and support-profile classifier emitting lossless per-module declarations before any global merge | CC-002, CC-R01, CC-D03, CC-D08, CC-D11, CC-010, CC-011, CC-012, CC-013, CC-014, CC-015, CC-016, CC-021, CC-022 | Duplicate key, unknown field, supported field, unsupported construct, explicit-presence and raw adoption evidence |
| CC-R03 | Qualified binder and explicit composition result over per-module declarations | CC-R02, CC-D02, CC-D05, CC-D06, CC-D11, CC-010, CC-011, CC-012, CC-013, CC-014, CC-015, CC-016, CC-021, CC-022 | Collision, explicit adoption, ambiguous name, deterministic diagnostics |
| CC-R04 | Hierarchy, mixin, slot, and expression elaboration | CC-R03, CC-D03, CC-D08, CC-010, CC-011, CC-012, CC-013, CC-014, CC-015, CC-016, CC-021, CC-022 | Baseline, conflicting mixins, bounds, missing range, flat expression, nested refusal |
| CC-R05 | Canonical neutral facts and validated fact set | CC-R04, CC-D05, CC-D06, CC-D08, CC-010, CC-011, CC-012, CC-013, CC-014, CC-015, CC-016, CC-017, CC-018, CC-021, CC-022 | Frontend, direct-fact input, and each independent oracle match exactly |
| CC-R06 | Admission profile and effective contract | CC-R05, CC-D07, CC-D10, CC-010, CC-011, CC-012, CC-013, CC-014, CC-015, CC-016, CC-019, CC-020, CC-021, CC-022 | Valid and invalid records plus contextual operation traces |
| CC-R07 | Reloadable experimental artifact | CC-R06, CC-010, CC-012, CC-014, CC-016, CC-021, CC-022 | Deep immutability, corruption refusal, unknown grammar refusal, deterministic reload |
| CC-R08 | Whole-pipeline conformance attestation | CC-R01, CC-R02, CC-R03, CC-R04, CC-R05, CC-R06, CC-R07 | All three corpora, prior slices, current bundled ontologies, mutation adequacy |
| CC-R09 | Research-local Small Shop source-to-ABox vertical | CC-R08, CC-D07, CC-D10, CC-021, CC-022 | Retained occurrence through mapping, transformation, identity, recipe, ordered ProposedOperations, candidate, evidence, review, ProtocolLedger, accepted temporal KG, replay receipt, and private research journal |

The first foundation block is complete only at CC-R08. Passing one stage does not
authorize production use.

### Wave 2: production boundary and cutover

| ID | Deliverable | Depends on | Mandatory AT slice |
|---|---|---|---|
| CC-P01 | Artifact-backed runtime views under an experimental boundary | CC-R08, CC-D09 | No LinkML object crosses the runtime boundary |
| CC-PKG01 | One-distribution compiler and runtime-path isolation boundary | CC-P01, CC-D13 | One normal installation includes compiler and LinkML; artifact-backed runtime probes block LinkML imports; compiler environment is exact and reproducible |
| CC-W01 | New-epoch persisted-wire reader and writer | CC-PKG01, CC-D04 | Epoch is checked before semantic decode; stable typed refusal and its public diagnostic identifier are defined; no fallback or bridge is reachable |
| CC-W02 | Frozen historic-wire hard-break proof | CC-W01, CC-X04 | Every frozen 0.11 and 0.13 top-level input receives the selected typed hard break without rewriting; embedded artifacts remain NOT_REACHED |
| CC-P10 | KnowledgeGraph cutover | CC-P01, CC-W02 | Existing KG suite plus themed record and graph traces |
| CC-P11 | Staging cutover | CC-P10 | Existing staging suite plus batch traces |
| CC-P12 | Logic cutover | CC-P10 | Existing logic suite and fact identity checks |
| CC-P13 | Prolog verifier cutover | CC-P11, CC-P12 | Existing verifier and isolation suites |
| CC-P19 | Neutral projection and ledger protocols remove the concrete Accepted-to-Assent type cycle | CC-P10, CC-P11, CC-P12 | Concrete runtime import and type check are absent; protocol conformance tests pass |
| CC-P20 | Accepted projection cutover | CC-P19 | Existing projection and graph-base suites |
| CC-P21 | Assent cutover | CC-P12, CC-P19, CC-P20 | Existing decision, replay, and authorization suites |
| CC-P22 | Orchestration and Protocol cutover | CC-P21 | Existing orchestration and protocol suites |
| CC-P30 | Recon cutover | CC-P10, CC-W02, CC-P42 | Recon consumer suite and frozen typed hard-break outcome |
| CC-P31 | OCR cutover | CC-P10, CC-W02 | OCR profile and evidence-integrity suites |
| CC-P40 | Inquisition compiler and provenance cutover | CC-P01, CC-PKG01 | Source-side checks use compiler boundary only |
| CC-P41 | Status from packaged artifact metadata | CC-P01, CC-PKG01 | Core status imports without raw schema parsing or LinkML |
| CC-P42 | Historic-reader isolation and production hard-break disposition | CC-W02 | Only the new-epoch reader is reachable in production; any historic reader remains a separate tool and never a fallback |
| CC-P45 | Known-client inventory, repair branches, and bundle candidates | CC-D15, CC-D16, CC-P22, CC-P30, CC-P31, CC-P40, CC-P41, CC-P42 | Each known client is ready or an operator-approved outage is recorded; bundles exist only if OD-001 was accepted |
| CC-PKG02 | Wheel, sdist, corpus, entry-point, and docs audit | CC-P13, CC-P22, CC-P30, CC-P31, CC-P40, CC-P41, CC-P42 | Selected topology installs cleanly and all packaged artifacts reproduce |
| CC-P50 | Promote `EffectiveContract` as public root | CC-P45, CC-PKG02 | Public API and release candidate pass all client and package probes |
| CC-P51 | Delete `OntologyRegistry` and replaced mechanisms | CC-P50 | Repository-wide AST, import, entry-point, and fallback bans pass |
| CC-P52 | Reissue built-in artifacts and release records | CC-P45, CC-P51, CC-PUB01 | Fresh compile equals packaged artifacts, status and changelog agree |

Dual execution is allowed only inside comparison tests. Production never falls
back from the new path to `OntologyRegistry`. CC-P51 deletes the old parser,
import, elaboration, fingerprint, and public export paths that it replaces.

### Wave 3: upstream and adopter work

The upstream train is specified in [`upstream.md`](upstream.md). It starts after
CC-R08 as an operator-selected scheduling gate, not a technical dependency for U1
or the import-map documentation unit. Experimental conformance builds may use
exact fork commits before review. Production and released builds require an
upstream merge or an explicit maintained-fork governance decision.

Known client readiness precedes CC-P52. If OD-001 is accepted, each adopter gets
its own consumer-bundle manifest and conformance trace. Recon migration does not
authorize Assent, Porchito, OCR, or methodology consumers implicitly.

## TDD contract for every workstream

Every implementation workstream must produce this evidence in order:

1. **RED:** a mechanical test fails for the missing behavior or known defect.
2. **GREEN:** the minimum implementation passes that test.
3. **SLICE:** the assigned themed-vertical acceptance trace passes.
4. **DISPROOF:** the assigned feature-isolation and neutral-domain cases pass.
5. **REGRESSION:** all prior stage slices and affected existing consumer suites
   pass.
6. **PACKAGE:** affected wheel, sdist, or docs boundaries are inspected where
   relevant.
7. **ATTEST:** the workstream manifest records exact commits, file digests,
   dependency lock, commands, results, and mutation inventory.

Snapshot equality alone is insufficient. Tests parse typed artifacts and assert
semantic fields, stable diagnostic codes, ordered decisions, and digests.
The finite mutation manifest names each operator, target, expected detector,
result, and survivor disposition. CI reports the tested denominator and proves
that every listed mutation is detected or explicitly rejected from scope.
Resolver isolation has two layers: in-process denial for precise failure tests
and an operating-system sandbox that denies network and undeclared files.

## Session ownership

The overseer owns:

* this dependency program;
* canonical decision promotion;
* the validated integration manifest;
* corpus membership and checksum publication;
* shared packaging and CI files;
* final integration and release gates.

Each worker owns one bounded file set and a workstream ledger. Its manifest
records exact evidence. Typed immutable blocks record observations, verified
facts, decisions, corrections, and coordination without copying raw logs or
long design arguments. Sphinx renders those records; it does not become their
source.

Workers do not edit another worker's expected artifacts. Oracle owners do not
run a compiler to generate expectations. Source owners do not approve their own
semantic oracle. Integration alone updates checksums after reviewing the exact
delta.

## Documentation contract

Executable schemas, typed definitions, canonicalization specifications, and
tests own public stage and artifact contracts. Code docstrings explain those
objects. Sphinx extracts docstrings and renders validated manifests with
autodoc and autosummary. Doctests execute public examples after CC-D09 permits
promotion. Existing Markdown enters Sphinx through MyST. The root README links
to a packaged or rendered guide only after that link is tested in built
artifacts.

Cross-stage composition, dependency state, and decisions remain data in the
validated manifests and canonical graph. Generated pages render that data.
No stage worker writes a parallel README that repeats its docstrings.

The themed examples use the public compiler and runtime entry points. Docs
must not import private stage modules, LinkML classes, or test helpers.

## Parked work

During CC-R01 through CC-R09, do not merge unrelated foundation changes:

* the D0 methodology candidate at `7d913ed`;
* the O2 endpoint feasibility commit at `20d883f`;
* migration grades beyond the existing narrow Recon TOTAL bridge;
* methodology controls, GraphRecipe expansion outside CC-R09, LLM preparation,
  OCR C2, SMT measurement, and paper integration.

These remain preserved decision or research artifacts. The three empty Claude
worktrees contain nothing to incorporate. Current ontology promotion on `main`
is authoritative for the compiler baseline.

## Program completion

The program is complete when all of the following are mechanically true:

1. A clean compiler environment builds the three corpora into independently
   expected neutral facts under an exact support profile.
2. The artifact-backed runtime loads packaged artifacts and passes all runtime
   traces with LinkML imports blocked. The normal selected installation may
   still contain LinkML.
3. Every internal consumer uses the artifact-backed views.
4. The selected persisted-wire transition is proven against frozen historic
   data.
5. The legacy production mechanism and public exports are absent, with no
   fallback.
6. Wheel, sdist, docs, manifests, canonical graph, implementation status, and
   release records agree.
7. Every incorporated upstream patch is reconstructable from retained source
   or patch artifacts, exact commits, ordered integration metadata, conflict
   resolutions, locked build inputs, exact commands, retained wheels, and their
   hashes.
8. Every public example is a projection of a tested fixture and uses only
   public APIs.

Until then, the work is an experimental conformance program, not a shipped
contract-compiler claim.
