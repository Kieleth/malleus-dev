# Contract compiler conformance spine

Status: candidate test and example contract

The conformance spine makes every compiler and runtime stage prove one vertical
slice while preserving all earlier slices. It is not one golden fixture. It has
three independently useful corpora.

## The three corpora

| Corpus | Purpose | Authority |
|---|---|---|
| Themed vertical, working name Quiet Bell Archive | Engaging example and end-to-end smoke test | Independently authored typed oracle plus operation traces |
| Feature isolation | Tiny cases that prove one semantic or refusal at a time | Per-case expected values and diagnostic codes |
| Neutral domain | Structurally different vocabulary that catches theme-specific assumptions | Separate expected facts and traces |

Current bundled Malleus ontologies form a fourth regression set. They remain
authoritative for their consumer behavior, but they are not an independent
oracle for the new fact grammar.

## Themed vertical: Quiet Bell Archive

The working case is an original records-office investigation into a seal discrepancy
in the Ash Meridian survey folio. The setting is austere, readable, and suitable
for technical documentation. Quiet puns live in names such as `NinthQuire`,
`Vella`, and `MargenQuill`. Core artifact types, diagnostics, and APIs remain
neutral.

`OD-014` accepts `Quiet Bell Archive` as the public working name and keeps every
themed term fixture-only. It creates no fixture or publication. Core artifact,
API, diagnostic, and protocol names remain neutral.

Baseline concepts:

| Concept | Role |
|---|---|
| `ArchiveExaminer` | Entity with the Agent mixin |
| `InquiryDossier` | Entity collecting one investigation |
| `EvidenceFolio` | Entity representing a retained document |
| `EvidenceLocator` | Inlined value with exactly one shelfmark or digest |
| `CitesFolioRelation` | Concrete Relation from dossier to folio |
| `SealReviewEvent` | Event recording an examination |
| `SealDiscrepancySignal` | Signal borne by the citation relation |

The baseline operation trace is intentionally small:

1. Create examiner `Vella`.
2. Create dossier `TheQuietBell`.
3. Create folio `NinthQuire`.
4. Create the dossier-to-folio citation relation.
5. Create the seal-review event.
6. Create the discrepancy signal borne by the relation.

This trace exercises required and optional values, enum values, collections,
inlined data, subtype and mixin membership, fixed relation predicates,
references, endpoint existence, signal bearer existence, ordered writes, and
state digests.

### Originality and public boundary

The internal creative brief may draw on gothic investigative atmosphere. Public
metadata must not describe the fixture as tied to another franchise. It uses no
third-party marks, faction or character names, quotations, lore, logos,
heraldry, artwork, fonts, screenshots, or distinctive visual likenesses.

The operator attests exactly:
`Luis Guzman Lorenzo is the author and rights holder for the original Quiet Bell text/data, licensed Apache-2.0`
The attestation covers no visual asset.

Every future public asset manifest entry binds its exact path, bytes, digest,
media type, author, license, and origin. Automated text and metadata scans are
guardrails, not legal clearance. Human review in `CC-PUB01` binds the exact
manifest digest before public web publication. Any asset byte or manifest
change invalidates that review.

## Version axes

Never overload one version string.

| Axis | Example | Meaning |
|---|---|---|
| Corpus protocol | `contract-kernel/v0` | Layout and conformance rules |
| Source version | `1.0.0` | Themed authored ontology version |
| Artifact grammar | candidate identifier | Canonical runtime artifact bytes |
| Support profile | candidate identifier | LinkML constructs accepted by compiler |
| Admission profile | candidate identifier | Runtime interpretation and graph rules |
| Diagnostic profile | candidate identifier | Stable codes, parameters, and ordering |
| Compiler attestation | exact manifest digest | Compiler environment and input provenance |
| Presentation version | docs or web build | Nonsemantic rendering and narrative |

Candidate source cases, finalized only after `OD-008` classifies fields:

| Source | Purpose | Expected semantic relation |
|---|---|---|
| `1.0.0` | Baseline | First vertical oracle |
| `1.0.1` | Description, display-label, and other fields classified annotation-only, explicitly excluding adoption, retirement, governance, and identity-bearing annotations | Same validated facts and effective contract, different source attestation |
| `1.1.0` | Additive optional field | Changed effective contract, baseline trace remains valid |
| `2.0.0` | Reserved for a real breaking experiment | Deferred until CC-W01 authors the new-epoch wire grammar and stable typed refusal profile |

Historic versions are never overwritten. Every semantic change has an expected
delta manifest that lists added, removed, and changed facts.

## Proposed layout

```text
conformance/contract_kernel/v0/
  corpus.json
  corpus.schema.json
  stage-matrix.json
  checksums.json

  themed_fixture/
    requirements/
    sources/
      v1.0.0/
      v1.0.1/
      v1.1.0/
    oracle/
      v1.0.0/
      v1.0.1/
      v1.1.0/
    traces/
      input/
      oracle/
    direct-input/
    public/

  feature_cases/
    source/
    composition/
    elaboration/
    artifact/
    admission/
    decisions/

  neutral_domain/
    sources/
    oracle/
    traces/
```

`corpus.json` lists every normative file. Narrative prose and rendered docs are
explicitly nonnormative. `checksums.json` covers the normative membership. The
integration owner alone publishes membership and checksums after reviewing the
delta.

## Independent oracle rules

1. The source and frontend owner cannot edit `oracle`.
2. The oracle owner cannot edit source or compiler code.
3. Oracle files are hand-authored from accepted contract decisions. They are
   never exported from LinkML, `OntologyRegistry`, or the implementation under
   test.
4. A compiler change and oracle change may share an integration only when a
   predeclared expected-delta manifest explains every fact difference.
5. Semantic scenario requirements, LinkML source input, neutral direct-fact
   input, and expected canonical output have separate owners. The direct-fact
   producer reads only `direct-input`, never `oracle`. It is not a public second
   frontend.
6. The themed operation input owner cannot edit expected trace outcomes. The
   expected-outcome owner cannot edit source, compiler, direct-fact input, or
   operation inputs. Expected decisions, ordered diagnostics, state digests,
   and final records live under `traces/oracle`.
7. Raw snapshot equality is supplemental. Tests parse typed fields and assert
   their meaning.
8. Mutation tests alter every enforcing fact, edge, bound, diagnostic, and
   operation outcome. At least one semantic assertion must fail for each
   mutation.
9. A presentation-erasure transform changes only fields that `OD-008`
   classifies annotation-only, such as display labels and descriptions. Schema
   symbols, identifiers, enforcing annotations, and operation order do not
   change. Alpha-renaming may be tested for graph isomorphism later, but does
   not imply identical canonical bytes or digest.

## OD-005 atomic-fact conformance boundary

The versioned `ContractMetamodel`, not JSON or a JSON Schema, decides semantic
validity. A conforming fact input has exactly `subject`, `predicate`, and
`object`; uses full absolute identifiers and exact Unicode code points; and
canonicalizes to one compact, sorted UTF-8 JSON array with no terminal newline.
The predicate declares the object type. Numeric objects are canonical decimal
lexical strings; Boolean objects are JSON booleans. There is no coercion,
embedded fact ID, provenance member, prefix context, or fallback interpretation.

The positive feature slice covers `rdf:type` kinds, `rdfs:subClassOf`, mixin
classification and use, a module-global or deterministic class-local `Slot`, a
reified `SlotUse` with exactly one `onClass` and `usesSlot` plus `valueRange`,
`required`, `multivalued`, `identifier`, and `inlined` facts, enum values,
Scalar `typeof`, explicit-default and
implicit-default convergence with distinct provenance, `5`/`5.0`/`5e0`
convergence to `"5"`, and exact parity between the LinkML-derived facts and an
independently owned direct-fact input. Direct facts remain bootstrap and
conformance input only. They gain no public authoring or production authority.

The negative slice refuses a bare or prefixed symbol, string `"true"` for a
Boolean predicate, raw JSON numbers, unknown predicates or members, null,
arrays, nested objects, an incomplete `SlotUse`, duplicate records, conflicting
single-valued facts, nonfinite values, exponent or noncanonical decimal wire
forms, an illegal kind/predicate pair, seed primitive used as a fact subject,
invalid mixin or cycle, invalid bound/range pair, reversed bounds,
`equalsString` on the wrong range, `inlined=true` on the wrong range,
`valuePresence=ABSENT` in conflict with `required=true` or `equalsString`, and
every expression pending `OD-008`. It proves that input member and record order
do not change canonical bytes and that a description-only edit does not change
semantic facts. Whole-set validation is atomic: completeness, cardinality,
object and target kind, required structure, declared acyclicity, duplicates,
and contradictions pass or refuse together.

Internal candidate digests bind the exact metamodel, canonicalization profile,
symbol policy, and canonical fact or ordered-fact digest. Stable public fact IDs
remain blocked on `OD-006` and `OD-008`. The direct-fact bytes are not the
persisted artifact envelope selected later by `CC-R07` and `CC-W01`.

## Acceptance-test matrix

Every row defines the assigned themed-vertical slice, focused countercases, and
regression obligation.

| AT | Stage | Themed slice | Countercases | Required result |
|---|---|---|---|---|
| AT-001 | Resolver and closure | Root, nested relative import, diamond | Missing import, network locator, resolver failure, directed import cycle, same locator with different bytes, different locators with identical bytes | Exact retained bytes, lengths, digests, module instances, authored ordinals, every parent edge, deterministic order, no hidden I/O under process and operating-system containment; resolver failure never tries another profile; the same locator with different bytes and every directed cycle refuse with retained lineage; different locators with identical bytes remain distinct module observations |
| AT-002 | Parser and support profile | All baseline declarations | Duplicate key, unknown field, unsupported attribute | Exact declared module or stable typed refusal; every field classified |
| AT-003 | Binder and composition | Root plus domain symbols | Collision, adoption marker/equality refusal matrix, ambiguity | Literal Boolean adoption marker and exact pre-default equality accept only the authorized slot case; every other matrix cell refuses |
| AT-004 | Hierarchy and mixins | Examiner subtype and Agent mixin | Unknown parent, repeated mixin, order conflict | Exact ancestor and mixin facts or stable refusal |
| AT-005 | Slot induction | Baseline and additive source | Bounds, explicit false, missing range, attribute versus slot | Exact effective constraints; every applied default is materialized with provenance |
| AT-006 | Expressions | Locator exactly-one-of | Nested expression, unsupported combinator | Exact normalized expression or stable refusal |
| AT-007 | Canonical facts | Exact seed kinds and predicates, class inheritance and mixin, global and qualified class-local Slot, complete reified SlotUse, enum, Scalar termination, applied defaults, and numeric normalization | Bare symbol, string Boolean, raw number, unknown member or predicate, wrong kind, seed subject, incomplete SlotUse, duplicate, contradiction, cycle, invalid bound or range, null, array, nested object, noncanonical decimal, expression, member order, record order, presentation erasure | LinkML adapter, independent direct facts, and independent oracle yield identical metamodel-valid atomic facts and exact canonical bytes; all invalid whole sets refuse atomically |
| AT-008 | Effective contract | Baseline facts and admission profile | Wrong profile, wrong grammar | Exact domain-separated identities and refusal |
| AT-009 | Artifact loader | Valid packaged artifact | Truncated, corrupt, unknown field, mutable nested value | Deep immutable reload equality and typed refusal without LinkML |
| AT-010 | Record shape | Six valid records | Unknown property, missing required, wrong enum, wrong scalar | Ordered typed violations and selected legacy rendering |
| AT-011 | Graph context | Baseline operation trace | Duplicate ID, relation before endpoint, missing bearer, abstract root | Exact decisions, state digests, and final records |
| AT-012 | Staging | Ordered intra-batch dependency | Invalid member, stale candidate | Whole-batch refusal, no partial mutation, exact visibility |
| AT-013a | Consumer cutover | Themed smoke through each cut-over view | Old import and fallback probes from the cut-over consumer | Existing domain suites pass and that consumer executes only the new path; comparison-only legacy code may still exist elsewhere |
| AT-014 | Packaging | Normal distribution, compiler environment, sdist | LinkML import blocked on the artifact-backed runtime path | Corpus discoverable, artifacts load, fresh compiler output matches packaged files |
| AT-015 | Docs and examples | Themed public trace | Private import and copied fixture probes | Doctests pass using only public APIs and literal fixture inclusion |
| AT-016 | Historic wire | Frozen 0.11 and 0.13 corpus | Unknown identity and grammar | Stable typed epoch refusal for every top-level input before semantic decode; embedded artifacts remain NOT_REACHED |
| AT-017 | Legacy deletion | All public modules and entry points | Repository-wide old import, parser, and fallback probes | Replaced mechanism is absent after CC-P51 |

An implementation stage passes only when its assigned AT, all earlier ATs, its
feature-isolation cases, the neutral-domain slice, and affected current Malleus
tests pass.

## Divergence corpus

The feature-isolation corpus must include at least:

* direct and transitive imports;
* same-named imports under distinct parents;
* explicit adoption and conflicting duplicates;
* parent versus mixin precedence;
* repeated and conflicting mixins;
* widening and narrowing numeric bounds;
* absent versus explicit false;
* missing ranges and schema default range;
* attributes versus global slots and slot usage;
* flat and nested expressions;
* empty, null, absent, scalar, and collection values;
* dangling generic class references;
* Entity, Event, and Signal endpoint decision cases;
* deterministic diagnostic ordering;
* invalid bytes and unknown artifact grammar.

The retained cases keep separate pinned-LinkML and legacy observations.
`OD-003` classifies all nine without changing them: equal cases remain equal;
parent/mixin precedence, numeric bounds, default range, and local attributes use
pinned LinkML meaning; repeated and conflicting mixins refuse. There is no
catch-all normalization category or legacy-emulation path.

## Regression and packaging gates

Before production cutover:

1. Build wheel and sdist and inspect their file manifests.
2. Install the normal distribution, block LinkML imports on the artifact-backed
   runtime path, import every runtime public module and entry point, load each
   packaged contract, and replay the themed trace.
3. From the same distribution, verify the compiler environment against exact
   LinkML and runtime wheel hashes plus the locked transitive environment.
   Recompile every corpus version.
4. Install the sdist outside the checkout and run the conformance suite.
5. Compare fresh compiler output with every packaged built-in artifact.
6. Build Sphinx with warnings fatal, execute doctests, verify links, surface the
   public adapter contract from code docstrings, and prove that the docs build
   leaves the worktree unchanged.
7. Assert public examples import no private stage, LinkML type, or test helper.

The themed vertical makes the architecture understandable. Feature cases and the neutral
domain keep it honest.
