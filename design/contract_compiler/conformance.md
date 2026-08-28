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

Accepted source cases under the exact `OD-008` field classification:

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
   classifies annotation-only: schema name, version, title, and description;
   class, slot, type, enum, permissible-value, and slot-usage descriptions;
   class URI; and type URI. Schema
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
every expression outside the exact OD-008 extension. It proves that input member and record order
do not change canonical bytes and that a description-only edit does not change
semantic facts. Whole-set validation is atomic: completeness, cardinality,
object and target kind, required structure, declared acyclicity, duplicates,
and contradictions pass or refuse together.

Internal candidate digests bind the exact metamodel, canonicalization profile,
symbol policy, and canonical fact or ordered-fact digest. OD-008 completes the
candidate metamodel inputs; stable public fact identifiers remain blocked on
`OD-009`. The direct-fact bytes are not the
persisted artifact envelope selected later by `CC-R07` and `CC-W01`.

## OD-006 closed-composition conformance boundary

A full composition has exactly three distinct fixed role slots with cardinality
`1..1`: `ProtocolRecordContract`, `GovernedGraphContract`, and
`GovernanceContract`. Each role-bound identity uses the fixed conceptual v0
role-identity token, the exact fixed role tag, and one complete
`EffectiveContract` identity. The composition identity uses its separate fixed
conceptual v0 token and exactly the three named role-bound identities. These
logical constructors do not define artifact, bundle, or persisted bytes.

The positive delta matrix is exact:

| Change | P | D | G | Composition | Accepted-temporal epoch |
|---|---|---|---|---|---|
| Presentation or provenance only | same | same | same | same | same |
| Protocol semantics only | changed | same | same | changed | new |
| Governed-domain semantics only | same | changed | same | changed | new |
| Governance semantics only | same | same | changed | changed | new |

On the accepted-temporal path, a new role value is legal only inside a newly
constructed and bound composition and a new epoch. One physical artifact may
package all three complete roles without collapsing them. A future consumer
bundle references one composition; `CC-D16` retains its fields and bytes.

A standalone structural graph is separate from that matrix. It binds one
`GovernedGraphContract` and structural-state identity, has no protocol ledger,
and is not an accepted-temporal composition. A domain semantic change there
changes the governed-graph role and structural snapshot only; there is no
ledger epoch. This exception never makes a full-composition role optional.

The refusal corpus covers a missing, duplicate, extra, or unknown role; wrong
role token, role tag, or composition token; protocol/domain swap; bare
effective-contract hash; incomplete role closure; ambient borrowing; equal
payload treated as cross-role identity; a valid replacement role used to
continue an existing epoch without a new bound composition; mixed-composition
roles; independently advanced or inferred-current role heads; protocol
validation by the domain role or domain validation by the protocol role;
accepted-temporal state bound only to the domain role; ledger continuation
after a composition change; and a standalone structural graph carrying a
protocol or governance role, composition, accepted-temporal marker, or ledger.
Whole-composition validation refuses atomically.

No conformance case may infer governance topology, endpoint or stateful
admission behavior, source-field or expression classification, public
promotion, stable public fact identifiers, consumer-bundle bytes, artifact
bytes, persisted epoch bytes, compatibility, migration, or multi-head recovery.

## OD-007 protected-partition conformance boundary

The conformance model is a replay trace, not a proposed wire format or runtime
API. It contains one protocol event sequence, one accepted graph lineage, and
one query surface over ordinary domain and protected governance records.
Existing source-ledger, acceptance, and materialization head components remain
part of accepted-graph identity. The topology adds no governance-specific head,
graph, snapshot, digest, or query API.

Each conceptual operation carries the contract path produced by admission
evaluation, never a requested partition. Replay derives governance membership
only from the `GovernanceContract` path. The abstract trace accepts no partition
input and uses no record-type classification rule. A standalone structural
graph has no governance role and refuses every governance-partition record.

The minimum positive trace is ordered:

1. Genesis supplies one explicit bootstrap authority root outside both logical
   partitions. Zero or two roots refuse before state exists. Neither graph path
   can create, replace, or delete the root. No later event can introduce another
   root or bypass pre-event authorization; the seeded root remains prior
   authority.
2. An ordinary write accepted through `GovernedGraphContract` becomes queryable
   in the domain partition without changing governance state or epoch.
3. The bootstrap authority submits a governance update under the current
   `GovernanceContract`. Authorization reads pre-event authority state seeded
   by the external root and otherwise derived from accepted governance state.
   The accepted update becomes queryable only after the event.
4. Authority introduced by that update can authorize the following event, but
   not the event that introduced it. When the authority source is a policy, its
   identity must differ from the directly mutated policy identity; a different
   prior policy or the external root must authorize it.
5. A later policy-instance update under the same `GovernanceContract` advances
   the accepted-graph lineage without starting a new composition epoch.

Invalid genesis creates no accepted state. Every post-genesis transition
refusal asserts identical pre-state and post-state queries, accepted event
projection, authority set, partitions, and epoch. The test-only event sequence
represents lineage without replacing or collapsing the existing accepted-graph
identity components. The negative trace covers missing or ambiguous bootstrap,
graph mutation of the external root, same-event
self-authorization, direct policy self-amendment, ordinary direct mutation of a
governance identity, wrong role or admission path, and a `GovernanceContract`
semantic change under the old epoch. Exact endpoint,
reference, context, operation, authentication, policy-language, and
materialization semantics remain outside this trace. Cross-partition
references, read authorization, filtering, confidentiality, and query-access
policy also remain deferred.

## OD-008 closed support-profile conformance boundary

The LinkML v0 adapter profile classifies each exact source location as
`ENFORCED`, `IDENTITY_ONLY`, `ANNOTATION_ONLY`, or `REJECTED`. The classes are
closed, exhaustive, and disjoint. An unlisted field or annotation, or a listed
member at the wrong location, refuses. `annotations.adopts` is identity-only at
the exact imported global-slot redeclaration authorized by OD-002 and emits no
semantic fact. `annotations.retires` and every unlisted annotation refuse.

The classified source slice covers all six bundled ontology shapes and all nine
CC-X01 sources, retaining each accepted or refusal outcome instead of treating
the inventory as nine positive compilations. It includes null permissible-value
bodies as exact empty value declarations, explicit false, applied default
range, parent and mixin precedence, restrictive numeric-bound intersection,
distinct global slot, attribute, and slot-usage evidence, one SlotUse per
applicable class slot, and the exact retained Assent flat `ValidTime`
expression. Presentation erasure
preserves facts and candidate identities while changing source attestation.

The immutable D05 seed composes with exactly
`FlatExactlyOneExpressionExtensionV0` to form
`ExpressionCapableContractMetamodelV0`. The extension has only
`ExactlyOneGroup`, `ExactlyOneAlternative`, and `SlotCondition`; its exact
predicates, cardinalities, typed values, canonical structural envelopes, SHA-256
URNs, and whole-set invariants are frozen. Branch, condition, and member order
are nonsemantic. Inherited and local groups are conjunctive.

The refusal slice covers an extra or wrong-location field, unknown annotation,
retirement marker, malformed adoption marker, duplicate declaration or slot
reference, unresolved or ambiguous slot use, repeated or conflicting mixin,
wrong reference kind, unlisted builtin, null outside a permissible-value body,
wrong permissible-value body, empty group or branch, duplicate semantic branch
or condition, unknown condition slot, wrong condition type, internal
`ABSENT`/required/equals contradiction, nested expression, and every unsupported
combinator. Each refusal is atomic. Parser acceptance alone never expands the
profile.

An expansion case is incomplete until the exact location classification,
seed-or-versioned-extension mapping, default and provenance behavior, positive
and refusal cases, independent source/direct-fact/oracle parity, metamorphic
identity tests, profile and metamodel versioning, internal guide, strict Sphinx
builds, and independent evidence review land together. Public adapter
docstrings and stable public identifiers remain under OD-009.

## Acceptance-test matrix

Every row defines the assigned themed-vertical slice, focused countercases, and
regression obligation.

| AT | Stage | Themed slice | Countercases | Required result |
|---|---|---|---|---|
| AT-001 | Resolver and closure | Root, nested relative import, diamond | Missing import, network locator, resolver failure, directed import cycle, same locator with different bytes, different locators with identical bytes | Exact retained bytes, lengths, digests, module instances, authored ordinals, every parent edge, deterministic order, no hidden I/O under process and operating-system containment; resolver failure never tries another profile; the same locator with different bytes and every directed cycle refuse with retained lineage; different locators with identical bytes remain distinct module observations |
| AT-002 | Parser and support profile | All six bundled shapes, nine divergence sources, exact location classes, retained builtins, null enum body | Duplicate key, unknown or moved field, unknown annotation, retires, wrong body, unsupported builtin | Exact declared module or typed atomic refusal; exact closed classification and source inventory; parser acceptance alone changes nothing |
| AT-003 | Binder and composition | Root plus domain symbols | Collision, adoption marker/equality refusal matrix, ambiguity | Literal Boolean adoption marker and exact pre-default equality accept only the authorized slot case; every other matrix cell refuses |
| AT-004 | Hierarchy and mixins | Examiner subtype and Agent mixin | Unknown parent, repeated mixin, order conflict | Exact ancestor and mixin facts or stable refusal |
| AT-005 | Slot induction | Baseline and additive source | Bounds, explicit false, missing range, attribute versus slot | Exact effective constraints; every applied default is materialized with provenance |
| AT-006 | Expressions | Generic flat exactly-one and retained Assent ValidTime | Empty or duplicate branch, duplicate or unknown condition, internal contradiction, nesting, any/all/none | Exact three-kind normalized expression, order-independent internal structural IDs and facts, or typed atomic refusal |
| AT-007 | Canonical facts | Immutable D05 seed plus exact expression extension, class inheritance and mixin, global and qualified class-local Slot, complete reified SlotUse, enum, Scalar termination, applied defaults, and numeric normalization | Bare symbol, string Boolean, raw number, unknown member or predicate, wrong kind, seed subject, incomplete SlotUse, duplicate, contradiction, cycle, invalid bound or range, null outside enum body, array, nested object, noncanonical decimal, unsupported expression, member order, record order, presentation erasure | LinkML adapter, independent direct facts, and independent oracle yield identical metamodel-valid atomic facts and exact canonical bytes; all invalid whole sets refuse atomically |
| AT-008 | Effective contract and closed composition | Complete P/D/G role closures, fixed conceptual v0 role tags and constructors, one composition, one accepted-temporal epoch, and standalone D-only structural graph | Missing, duplicate, extra, unknown, swapped, incomplete, ambient, equal-payload, unbound replacement, mixed-composition, independent-head, wrong-use, structural/full-path confusion, wrong fixed role tag, domain, version, or composition constructor | Exact domain-separated role and composition identities; delta matrix; new composition and epoch for any semantic role change; exact atomic refusal |
| AT-008a | Protected replay-derived governance partition | One accepted graph lineage, single external bootstrap root, pre-event authority, ordinary write, authorized governance update, following-event visibility, same-contract policy update | Missing or ambiguous root, root graph mutation, same-event self-authorization, direct policy self-amendment, ordinary write directly mutates governance identity, wrong role or admission path, GovernanceContract semantic change under old epoch | Admission-path-only membership with no type/name/namespace/storage inference, no governance-specific head or query surface, exact pre-state/post-state queries, same epoch for policy instances under the same contract, new epoch boundary for contract change, atomic refusal |
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
