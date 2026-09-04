# Implementation Status

Malleus package version `0.13.3` implements the
`stage-8c-executable-provenance-and-effect-closure` boundary.

This is a capability boundary, not a claim that the research program is
complete. The machine-readable source is `malleus.IMPLEMENTATION_STATUS`.

## Public compiler and population facade

One Small Shop research experiment runs retained source bytes through the
LinkML adapter, neutral contract facts, an identified declarative machine and
policy, one immutable `KnowledgeChangeSet`, one append-only JSONL history, and
replay from an empty accepted graph. The output is a canonical receipt and a
queryable graph containing `O1`, `X1`, and their order-to-unit relation. The
same ledger reopens without ambient fixture or program files.

A separate bounded run now adds supplier-order state `B/Y/1` at source
occurrence `e4`, then `B/Y/2` at `e7` as its explicit replacement. It executes
and retains exact source-and-mapping plus structural check receipts, preserves
both versions in record history, and derives only the `e7` version into the
current graph. Its answer key remains outside execution.

A private, domain-neutral composer removes the repeated mechanical assembly of
those change sets. It binds an explicit operation list and valid-time decision
to the current contract, ledger, accepted-state, and retained-input identities,
then returns an immutable `KnowledgeChangeSet` carrying canonical bytes without
writing anything. Admission and replay remain separate. Source parsing, domain
mapping, checks, policy, and protocol-event construction remain outside the
helper.

Packages built from this source expose the reusable pieces through
`malleus.compiler`: exact-source LinkML contract compilation, population-plan
compilation, governed admission, reopen, replay, and the replayed graph's query
methods. The installed `malleus-compiler contract` command covers contract
compilation. It accepts exact named ontology files and never accepts a raw
ontology digest in their place. The sdist and direct wheel must contain the
same compiler runtime bytes.

The optional document-assertion adapter is also public through
`malleus.compiler`. It checks exact reading and capture bytes, verbatim
captured clauses, field-level formalisation targets, supported modalities, and
typed representation gaps. It emits the same neutral population-plan grammar
as structured-source adapters plus a two-axis review/formalisation census.
Assertions remain retained evidence and are not added to the graph.

The public facade also exposes a read-only population trace. Given one
accepted record ID, it resolves and verifies the record history, accepted
change set, canonical population plan, selected history profile, field
derivations, and retained source and evidence bytes. It refuses changes that
did not retain a population plan. The trace writes nothing and creates no new
authority or artifact.

The same knowledge history can now cross one explicit additive ontology
revision. The revision artifact embeds the next validated and partial contract,
derives its change kinds from compiled facts, binds the exact prior history
coordinates, and carries a migration receipt. The shipped policy admits added
classes, slots, and enum values. It refuses an added import while retaining
`ADD_IMPORT` in the policy grammar. Replay rebuilds the current graph under the
new contract and later change sets bind the new contract identity; earlier
records and change sets remain in the same ledger.

This facade does not replace the shipped Assent runtime, stabilize any
`private-v0` wire grammar, or turn a domain's source mapping into Core policy.
It proves the reusable seam on one controlled initial-population case and one
controlled record correction. General correction semantics, mapping syntax,
stable change-set wire, Event population, external effects, Semantic Re-entry,
cross-language parity, and release work remain outside this cut.

Three full, content-addressed domain-history profile artifacts now ship through
`malleus.compiler`: `state-version`, `source-assertion`, and `object-event`.
They declare origin and genesis scope, semantic unit, time semantics, change
semantics, ontology roles, projection-rule family, and grounding. Small Shop
executes the `state-version` profile. The document adapter executes a
capture-batch `source-assertion` profile whose assertion modality and domain
time remain reachable through retained evidence and the public trace. The
`object-event` profile is declarative only because Event population remains
unsupported. The runtime validates and binds these declarations but does not
yet interpret arbitrary projection programs from them. Contract revision is
additive only; it is not a general ontology migration or import-admission
mechanism. See `contract_compiler/index.md`.

Three optional, grounded knowledge packs also ship: `metrology`, `chronology`,
and `research`. They provide reusable mixins, reference classes, and enums
between the root primitives and a project ontology. A closed, content-addressed
grounding rite checks that borrowed term groups name their vocabulary and
locator, or that a root-extending project class records a bounded unsuccessful
search. The rite checks structure only; it does not judge a citation's quality.
An edited pack can be checked against exact reference bytes with the separate
`pack-conformance` rite. It permits documentation and additive vocabulary
changes through new declarations or enum values. It refuses removal or
strengthening of the existing structural surface; an extension that changes an
existing class uses a new subclass instead.
Pack grounding is retained provenance and does not alter semantic fact
identity. Packs remain adopter choices and are never required by the base
protocol.

The installable `malleus-acolyte` skill now carries a separate nascent-project
playbook beside its ongoing-project standing orders. It starts from retained
source bytes, keeps evaluation questions out of ontology construction and
population, chooses optional packs and a domain-history profile explicitly,
names the real grounding and compiler commands, routes document captures and
structured sources into the same neutral population plan, preserves typed
gaps, checks the capture census for untouched source blocks, and repeats only
through additive contract revision. It treats every concrete Entity and
Relation type as eligible, calls the public history admit and reopen boundaries,
keeps the loop in one session by default, and caps it at two revision rounds.
Admission runs only when `PopulationPreparation.change_set` is present;
`NO_DOMAIN_CHANGE` retains its evidence without an admission call.
The census keeps block review separate from assertion formalisation and states
that uncaptured assertions remain invisible. With a current installation and
exact inputs supplied, the procedure forbids ambient checkout, home-directory,
network, or undeclared-document discovery and fails when an input is absent.
It adds no compiler command or runtime capability. It documents how a fresh
adopter uses the public boundaries already listed above.

## Implemented

- Stage 2: closed-world ontology and typed-graph validation
- Stage 3: separate assessment, epistemic-decision, and authorization state machines
- Stage 7a: strict single-writer protocol ledger and deterministic replay
- Stage 4: isolated proposed-subgraph staging and failure-atomic structural materialization
- Stage 5: domain-neutral typed graph compilation, pinned trusted rules,
  isolated logical execution, exhaustive violation witnesses, and immutable
  logic-monitoring records
- Stage 6: typed monitor specifications, typed epistemic policies, exact
  required-monitor coverage, and deterministic epistemic control selection
- Stage 7b: content-addressed external graph bases, precision-aware temporal
  candidate manifests, proposal and decision binding, atomic accepted
  applications, derived accepted-graph projection, and transaction-time plus
  three-valued valid-time replay
- Stage 7c: typed authorization policies, proposal-time action-policy commitment, exact
  required authority-monitor coverage, deterministic `AUTHORIZE`, `BLOCK`, or
  `CLARIFY` selection, and verdict-scoped grant validation
- Evidence and evidence-assertion proposal members with typed polarity, exact
  claim and evidence references, and decision-local citation checks
- `review-report-recording`: one exact review request target, one atomic report
  with zero or more immutable findings, one immutable disposition per finding,
  and independent requests for re-review or multiple reviewers

## Stage 8a

- Content-addressed `SourceArtifact` records declaring a source digest and length
- Exact `Evidence` binding to an applied source artifact ID and record hash
- Replay validation of source semantic hashes and atomic refusal of tampering

Stage 8a records what the caller declared about the bytes and makes that
declaration immutable and attributable. It does not read the bytes: a digest
and length describing no file are accepted and replay.
`source_artifact_fields_from_bytes` derives the declared fields when a caller
does supply bytes, but the ledger cannot prove that helper was used. It does
not authenticate the source, establish its truth, verify that a quotation
occurs within it, or notice that it changed. Those are separate checks, and the
first of them is `citation-byte-verification` below.

## Stage 8b

- Optional immutable `AssentPlan` over exact policy-declared epistemic monitor
  records and caller-supplied adapters
- One invocation per required monitor, with exact preflight coverage and hash
  checks before the first adapter runs
- Adapter exceptions and refused outputs recorded as typed `UNKNOWN` monitor
  failures, without retry
- Failure-atomic paired commit of a logical check and its logical assessment

Stage 8b does not select policy or verdicts, orchestrate authority monitors,
schedule or retry work, or provide whole-plan atomicity. See
`docs/ASSENT_PLAN.md`.

## Stage 8c

- `ActionDispatch` gated by an exact applied `AUTHORIZE` decision, executor,
  acceptance head, and validity interval
- Terminal `ActionExecution` receipts bound to one exact dispatch and adapter
  result digest
- Independent `OutcomeObservation` records bound to an exact execution,
  content-addressed observation contract, and content-addressed external-state
  snapshot
- Replay indexes for the complete authorization-to-observation path

Core Malleus records this path but performs no domain effect. The research
adapter owns `payments.jsonl`; a separate observer owns the outcome check. One
recorded dispatch per action and one execution per dispatch define the current
profile. A future delivery profile may add idempotency, outbox, deduplication,
and external effect-ledger records without changing the core boundary. See
`docs/EFFECT_PROTOCOL.md`.

## Recon structural-capture tooling

The package also ships Malleus Recon without advancing the core assent stage:

- a typed literature-review ontology and append-only, replay-validated ledger;
- evidence-linked works, claims, results, searches, review boundaries, and
  claim-level comparison relations;
- exact intersection, union, directional difference, partial, unresolved, and
  contested comparison views;
- JSON, ontology-derived JSON-LD, GraphML, CSV, BibTeX, Markdown, manifest, and
  ZIP outputs that are byte-deterministic for identical inputs and the
  declared generator and runtime closure;
- an immutable public `OntologyRegistry.source_closure()` with exact parsed
  bytes, canonical source locators, all authored import resolutions, and
  retained definition ownership;
- strict manifest v3, manifest-last staged builds bound to the
  structural-capture profile, exact project bytes, complete ontology source and
  import closure, retained definition owners, derived term-map identity,
  separated grammar and migration verification evidence, ledger head and
  count, and the listed generator source closure;
- incremental replay with project-level exclusion of overlapping current
  Recon writers and initializers, plus per-output exclusion for builders;
- a narrow `windows-latest` Recon CI job, declared as an expandable matrix
  profile without claiming full Windows suite coverage or a completed remote
  run;
- an atomic typed importer for the existing literature-forensics graph v1.x;
  and
- the `malleus-recon` agent skill, installable for Claude, Codex, or both.

`RECORDED` establishes structural and ledger validity, not truth or novelty.
Recon has no crawler, provider integration, automatic novelty adjudicator, or
multi-writer protocol. Its source digests preserve caller declarations and do
not independently authenticate source bytes. Governed promotion is specified
as a one-way, identity-bound boundary, but no promotion adapter is implemented.
See `docs/RECON_CONTRACT.md`.

The Stage 5 boundary compiles public graph snapshots through one versioned fact
contract, binds ontology and exact rule bytes through a pinned logic contract,
runs every check in a fresh SWI-Prolog process, and validates the complete rule
manifest and violation set. A concrete `LogicContractArtifact` lets replay
verify ontology, fact-contract, rule manifest, timeout, and separate ruleset
record, raw-byte, and semantic-contract hashes. Completed executions produce
content-addressed `LogicCheckRecord` and `ViolationWitness` records. Translation, execution,
timeout, and malformed-result failures cannot report `SATISFIED`. Stage 6
records them atomically as `MonitorFailure` plus `UnavailableAssessment`, bound
to the exact logical contract and ruleset.

The Stage 6 boundary replaces opaque monitor and epistemic-policy artifacts
with concrete records. A monitor specification binds its assessment kind,
implementation hash, and input artifacts. An epistemic policy names exact
monitor records and maps each `VIOLATED` or `UNKNOWN` outcome to `REJECT`,
`DEFER`, or `CONTEST`, with explicit precedence when several controls fire.
Each proposal pins one exact policy before monitoring. Replay permits one
output per exact proposal-monitor pair and one completed logical check per
exact proposal-monitor pair, requires every selected monitor, and
recomputes the verdict, trigger assessments, and policy-evaluation hash.

The Stage 7b boundary adds three concrete records. `GraphBaseArtifact` commits
the ontology, state digest, and valid-time metadata for an externally supplied
base graph. `CandidateSubgraphArtifact` stores the ordered structural writes,
their precision-aware valid-time boundaries, supersession links, and
pre-state and post-state digests. `AcceptedGraphApplication` binds one accepted
decision to that exact candidate in the same `EPISTEMIC_DECIDED` event.

Replay restages every candidate against the reconstructed accepted graph. A
candidate-bound `ACCEPT` requires exactly one application; every other verdict
requires none. Replay keeps `acceptance_head`, `materialization_head`, cumulative
accepted graph digest, visible definite-graph digest, and valid-time resolution
digest separate. `AcceptedGraphProjector` rebuilds current or historical views
from the verified ledger and requires an explicit timezone-aware query. Exact
timestamps, zoned calendar days, bounded intervals, order-only transitions,
and unresolved prior boundaries share one inlined variant-shaped representation
in graph writes and claims. Protocol serialization and replay require that form
to be canonical. Non-exact boundaries require a committed extracted reason.
When the definite records remain structurally closed, views expose
`INDETERMINATE` record membership and its cause instead of selecting an
unsupported state. A projection whose selected relation loses a required
endpoint refuses as structurally incomplete. Propagating endpoint uncertainty
through dependent records is not implemented. NetworkX remains a derived
projection, not a second authority.

Version 0.11.0 accepts only graph-base and candidate schema version 2 and the
inlined `ValidTime` form in claims and claim revisions. Version 1 temporal
artifacts and scalar claim timestamps do not replay through an implicit
fallback. Existing ledgers require an explicit migration or a new ledger under
assent ontology 0.9.0. No migration utility is provided. Calendar-day replay is
also bound to pinned `tzdata==2026.3`, IANA release `2026c`; a later database
version requires an explicit migration rather than silent reinterpretation.

The assent LinkML source declares `ValidTime` as a closed five-way structural
union with class-level `exactly_one_of` and `slot_conditions`.
`OntologyRegistry` enforces that union at graph write time, including required
fields, forbidden fields, forbidden nulls, and the pinned timezone-database
identifier. The exercised LinkML runtime loads this declaration and official
JSON Schema generation is smoke-tested, but generated-schema parity for the
class-level union is neither tested nor enforced. Generated JSON Schema is not
an enforcement substitute. Canonical date and datetime encoding, timezone
existence, timezone-aware timestamps, and interval ordering remain runtime
semantics enforced by `ValidTime.from_value` during protocol serialization and
replay. Direct `OntologyRegistry` and `KnowledgeGraph` enforce structure,
not those runtime semantics.

Protocol commits use same-directory failure-atomic replacement. Interrupted
writes, file syncs, and replacements preserve the last valid ledger. This does
not claim multi-writer safety or filesystem-independent power-loss durability.

`UNKNOWN` never maps to `ACCEPT` or `REJECT`. A missing execution must be
recorded atomically as `MonitorFailure` plus `UnavailableAssessment`; simply
omitting a required monitor blocks the decision. Recording assessments without
an `EPISTEMIC_DECIDED` event leaves the proposal open, which keeps experimental
conditions C3 and C4 mechanically separable.

The Stage 7c boundary replaces opaque authorization-policy artifacts and
caller-selected authorization verdicts. Each action proposal now pins one
typed, content-addressed `AuthorizationPolicyArtifact` before epistemic
acceptance. That policy names the exact `AUTHORITY` monitor records required
for the action. Replay requires one output from each selected monitor and
recomputes the ordered assessment set, triggered assessments, evaluation hash,
and verdict. All `SATISFIED` outputs select `AUTHORIZE`; any `VIOLATED` output
selects `BLOCK`; otherwise any `UNKNOWN` output selects `CLARIFY`. `BLOCK` has
precedence over `CLARIFY`.

Completed and unavailable authority outputs bind the exact proposal, action,
action hash, evaluated actor, authorization policy, monitor, and acceptance
head. Authority-monitor failure is atomic: a `MonitorFailure` and an
`UnavailableAuthorityAssessment` must carry the same context. Only
`AUTHORIZE` validates grant actor, action type, and interval sufficiency.
`BLOCK` may cite the exact insufficient grant evaluated by a triggered
`VIOLATED` assessment, without treating it as sufficient. Authority outputs
are unique per action, actor, acceptance head, monitor, and optional evaluated
grant, so an exact changed context can be re-evaluated while competing output
for the same context remains forbidden. Non-authorizing verdicts carry
no authorization validity interval.

## OCR evidence-integrity profile

Capability `AUDIT_ONLY`. The package ships a profile that verifies a document
evidence bundle and writes nothing to a protocol ledger. Core Assent now has a
lean review request, report, finding, and disposition path, but the OCR profile
does not submit its reviewer results through that path.

The profile's vocabulary is `ontology/domains/ocr.yaml`, a LinkML domain schema
importing the root, and every identity plane is a typed record under a root
primitive: nine classes, two of them Events. `verify_bundle` validates every
plane through `KnowledgeGraph` before it runs a single profile check, so an
unknown property, a missing required slot, a value outside a closed enum, or a
range violation is refused as `OCR-D013`. Seventeen typed diagnostics, each
with a negative case.

The Python dataclasses in `malleus.ocr.bundle` are a carrier, not the
authority. Each answers `record()` with the graph record the registry
validates, and a test compares every dataclass field against the schema's
slots, so the two cannot separate again without something noticing.

What the profile proves: source-to-reading lineage, separation of identity
planes, declared coverage and policy precommitment, and that every plane is
typed under the root. What it does not prove: source authenticity, the factual
truth of a reading, quote fairness, or downstream consequence.

The portable artifact is the bundle document: `Bundle.document()` and
`Bundle.from_document()`, fail-closed on an unrecognised profile, either
direction of version drift, an undeclared key and a missing required key. The
`malleus-ocr` command verifies a document (exit 0 conforms, 1 refused, 2
unreadable, so a malformed file is never reported as failed evidence) and
`malleus-ocr --conformance` runs the seven cases shipped inside the package.
An emitter that imports no plane class and touches no dataclass conforms,
which establishes the emitter role as replaceable; no production OCR stack has
crossed it yet.

Verification returns two answers, not one. Integrity is a bit: the paperwork
either holds together or it does not. Coverage is a census and cannot be one.
`Account` reports what became of every unit the source class declared, in the
mandate B2 vocabulary, and measures each precommitted metric family against the
threshold frozen before ingest. A unit read and found blank is `VERIFIED_BLANK`
and counts as accounted for; a failed call is `FAILED` and does not. The three
ways to go unaccounted stay distinct: never fetched, held and never rendered,
rendered and never looked at.

The census vocabulary is the schema's, not the module's. `UnitDisposition` and
three outcome enums in `ontology/domains/ocr.yaml` declare which outcomes count
as looked-at, `outcome_dispositions` reads the mapping back, and `account_for`
takes the same registry the record validation ran under, so replacing the
profile ontology replaces the census with it. `terminal_verdicts` derives which
reviewer verdicts speak for a unit by intersecting `ReviewVerdict` with the
declared unit outcomes: `CONFIRMED` and `CORRECTED` are answers about a reading
and never displace a unit's, and mandate B2's "a reviewer never inherits an
attempt state" is a consequence of the schema rather than a sentence in a
description. The order is policy, published as `unit_verdict_precedence`.

What that order may and may not do is decision C9. A unit's several regions are
summarised worst-first, with `ABSENT` leading because it is the only verdict
whose subject is the unit. Two live verdicts about the same region are refused
as `OCR-D016` instead, because either choice converts the other reviewer's
answer. `predecessor_id` is now read, so a superseded verdict no longer
outranks the review that replaced it, and a chain that never reaches an
earliest review is refused as `OCR-D017` so the new reader cannot drop a record
quietly.

Completeness is judged against the adopter's own thresholds and nothing else.
A source class declaring a denominator this profile cannot compute reports
`UNMEASURED` and blocks completeness rather than passing. A source class
declaring no measure is never complete. A bundle declaring itself a
`REGISTRATION` is never complete and may never count as adapter conformance.

Not built: decision C2, dependency-closed partial claims, which is the rule for
promoting a claim whose evidence does not depend on a missing unit. The account
says which units are missing; it does not decide what may be promoted despite
them. No adapter has passed the conformance suite, so the profile is designed
from two audited adopters and is not yet established as portable. No Signal
subtype is declared because coverage is computed on demand rather than
recorded.

## Content hash and payload grammar

The content hash includes the payload grammar version, and 0.11.0 made that
version conditional: `3` unconditionally before, `4` afterwards for a schema
using `exactly_one_of`, `inlined` or `value_presence`. A feature-using schema's
content hash therefore changed between releases without one ontology byte
changing, and a ledger anchored under the earlier hash could not replay.

A hash written into an accepted append-only ledger is a public contract. The
ledger cannot be rewritten to match a new rule, so the rule verifies what the
ledger already holds. `content_hashes()` gives this schema's identity under
every grammar in `KNOWN_PAYLOAD_GRAMMARS`; `verifying_grammar()` answers which
one makes a recorded hash match, or `None` for a real mismatch.

A ledger accepts an earlier grammar only when the caller declares it, never by
assumption, and `verified_ontology_hashes` reports which were encountered so a
replay under an earlier grammar is a fact the caller can act on. Nothing is
silently recomputed and nothing is silently accepted.

Implemented, with a narrower boundary: `MigrationReceipt` records one asserted
old and new ontology hash, grade, reason, issue time, prior-receipt digest, and
optional delta digest. `MigrationChain` validates a gapless, acyclic sequence,
persists it as JSON, checks its live head, and stops backward hash acceptance at
a declared `HARD_BREAK`.

The receipt is not a protocol-ledger boundary event. It carries no transform,
record mapping, query rewrite, or verified delta. The public
`MigrationVerifier` and `MigrationAwareJsonlLedger` provide the narrower reader
that was previously missing: current-byte payload grammars verify without a
receipt; an exact older identity verifies only across a gapless, all-`TOTAL`
path; and `PARTIAL`, `HARD_BREAK`, unknown, or category-collision cases refuse.
The receipt ontology must match the live registry entry name, and sidecar
discovery remains anchored to the registry's retained absolute entry locator.
`MigrationVerification` reports the separated grammar identities, migrated
identities, and exact receipts crossed by a read.

The base `JsonlLedger` remains grammar-only. Recon uses the migration-aware
ledger and exposes only current-byte grammar aliases through
`historical_ontology_hashes`, so migration identities no longer enter that
parameter. Core `ProtocolLedger` still does not consume migration chains, and
the new reader does not establish a generic record transform or cross-contract
interpretation.

## Not implemented

- `portable-graph-base-resolution`: retrieving graph bytes from an artifact locator rather than requiring the caller to supply the matching base graph
- `typed-retraction-semantics`: removing a record without replacing it with a new immutable record
- `historical-timezone-database-migration`: moving a stored calendar-day
  boundary to a different IANA timezone database while retaining the old
  interpretation, lineage, and an explicit migration result
- `dependency-closed-valid-time-projection`: propagating an indeterminate
  endpoint or referenced record through dependent relations and properties
  instead of refusing a structurally incomplete definite projection
- `multi-writer-ledger-serialization`: safe concurrent append coordination
- `lexical-format-validation`: checking that a value declared `uri`, `date`,
  `curie` or another lexical built-in actually has that form. All of LinkML's
  built-in ranges are accepted and each is validated as its base kind
  (`double` and `decimal` as numbers, the rest as strings), so `"not a uri"`
  in a `uri` slot commits. Accepting the declaration and checking the base
  kind is strictly more than refusing the schema, which is what happened
  before, and the finer form is not enforced
- `action-execution`: performing an authorized action. Stage 8c records a
  dispatch and hashes an outcome contract (`src/malleus/execution.py`), which
  is a commitment about how an outcome would be checked. Malleus executes
  nothing and observes nothing. This entry was removed at 0.8.0 while the
  capability remained absent; it is restored
- `protocol-actor-registration`: registering `ProtocolActor` records so `responsible_actor_id` can range over actors instead of bare strings
- `untrusted-rule-program-sandboxing`: safe execution of uploaded or otherwise untrusted rule programs
- `monitor-execution-orchestration`: general orchestration beyond the optional
  Stage 8b epistemic `AssentPlan`, including authority monitors, retries,
  scheduling, resume, and cross-plan coordination
- `citation-byte-verification`: resolving registered source bytes and verifying
  at write time that a quoted span is a verbatim substring. Stage 8a binds
  `Evidence` to a content-addressed source record, but declares no quoted-span
  slot and performs no substring check
- `deferral-queue-aging`: measuring how long a `DEFERRED` proposal has been waiting and blocking past a threshold. `DEFERRED` is a terminal state with no aging, so a deferral is indistinguishable from a decision nobody revisited. Principle 3 of `PRINCIPLES.md` and the `arbiter_is_accountable` rite both require this of an adopter's application layer; malleus supplies the decision record, not the queue
- `exactly-once-effect-delivery-profile`: an optional stronger profile binding
  idempotency, outbox, adapter deduplication, and external effect-ledger records
  to the Stage 8c dispatch. The current profile records dispatch, terminal
  receipt, and outcome observation without selecting external delivery
  semantics
- `epistemic-policy-authority-and-scope`: deciding which policy is legitimate and applicable to a proposal
- `authorization-policy-authority-and-scope`: deciding which authorization policy is legitimate and applicable to an action

Stage 5 accepts only trusted, pinned local rule programs. Logic-check records
are content-addressed execution attestations with replay-validated bindings,
not formal proof certificates or guarantees of engine-level reproducibility.
A candidate-bound logical check must match the proposal's exact candidate,
pre-state, post-state, and ontology commitments. Stage 4 direct materialization
remains a structural API and has no effect on protocol replay. Stage 7b accepted
materialization is still single-writer. It records epistemic commitment, not
truth, authorization, external-world currency, or multi-writer correctness.

Stage 6 selects control from recorded monitor outputs. Stage 8b can
invoke caller-supplied epistemic monitor adapters, including a logical adapter,
but still does not choose request payloads or recipients. Monitor
implementation and input hashes make these dependencies inspectable without
pretending that Malleus independently reproduced their results. Numeric
confidence remains excluded until a calibration contract exists.

Core assessment kinds are closed to their declared concrete types. Extensible
assessment kinds require a future explicit capability contract; a domain class
cannot reuse a core kind while dropping its evidence fields. Version 0.4.0 also
adds required policy ID and hash fields to `ProposedSubgraph`, so 0.3.0 ledgers
do not replay unchanged. There is no implicit migration or default policy.
Proposal-time pinning prevents ex-post policy selection but does not establish
authority, eligibility, domain scope, or effective time for that policy. Exact
coverage is relative to the proposal's precommitted policy, not system-wide.

Stage 7c selects authorization control from recorded authority outputs. It does
not execute authority monitors, establish a grantor trust root, or decide which
authorization policy is legitimate. Stage 8c can record the later generic
dispatch, receipt, and observation path, but domain adapters still execute the
action. The fixed outcome-to-control mapping is protocol behavior, not proof
that an input authority assessment is correct.

The graph base is intentionally explicit. The opaque Stage 1 snapshot anchor
contributes no graph records. A `GraphBaseArtifact` is usable only when the
caller supplies a graph whose ontology, state digest, record count, and complete
valid-time metadata match the artifact. Version 0.5.0 does not provide a remote
resolver or silently treat the research graph as accepted knowledge.

## Release boundary rule

Every completed implementation stage must update all of these in the same
commit:

1. `IMPLEMENTATION_STATUS` in `src/malleus/status.py`
2. The package version in `pyproject.toml`
3. This document
4. `CHANGELOG.md`
5. Status and stage guardrail tests

The distribution build and installed-wheel smoke test must pass before that
stage is published.

Package versions and ontology versions are independent. The current root
ontology is `0.4.0`; the assent ontology is `0.9.0`.

## History

| Package | Boundary | Included work |
|---|---|---|
| `0.1.0` | Initial typed graph | Root ontology, typed graph, compatibility hashing, optional domain verifier |
| `0.2.0` | `stage-4-structural-staging` | Stages 2, 3, 7a, and 4 |
| `0.3.0` | `stage-5-general-logic-monitoring` | Stage 5 generic compilation, isolated execution, and replay-validated records |
| `0.4.0` | `stage-6-policy-selected-monitoring-control` | Typed monitor coverage and deterministic epistemic control selection |
| `0.5.0` | `stage-7b-assent-gated-bitemporal-accepted-graph` | Exact proposed mutations, atomic accepted applications, and bitemporal replay |
| `0.6.0` | `stage-7c-policy-selected-authorization-control` | Typed action-bound policy, exact authority coverage, and deterministic authorization control |
| `0.7.0` | `stage-7c-policy-selected-authorization-control` | Same boundary, hardened: ontology identity from the resolved constraint table, closed arbiter vocabularies, and the inquisition toolchain |
| `0.8.0` | `stage-8c-executable-provenance-and-effect-closure` | Caller-declared source byte identity, thin epistemic monitor adapters, authorized dispatch, execution receipts, and independent outcome observations |
| `0.9.0` | `stage-8c-executable-provenance-and-effect-closure` | Same boundary; all LinkML built-in ranges load, the bundled root resolves without a map, and a construction failure names the rites it skipped |
| `0.10.0` | `stage-8c-executable-provenance-and-effect-closure` | Same core boundary; adds typed, replayable literature forensics, deterministic comparison artifacts, the v1 literature-KG importer, and the Recon agent skill |
| `0.11.0` | `stage-8c-executable-provenance-and-effect-closure` | Same core boundary; adds precision-aware valid time, three-valued temporal projection, the maintainer stage-contract doctrine, and research-local GraphRecipe conformance evidence |
