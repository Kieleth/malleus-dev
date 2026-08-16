# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Fixed three shipped documents claiming a capability the library does not have, found by a sixth inquisition. `PRINCIPLES.md` and `ASSENT_PROTOCOL.md` both stated that changing the registered bytes "invalidates the old evidence binding"; proven false through a real ledger, where both artifacts sit in the projection as equals, the evidence still resolves to the first, and nothing is marked stale. `ASSENT_PROTOCOL.md` conceded four lines below its own claim that replay "does not fetch the locator", which is why the claim could not be true. That sentence is the second clause of the `quotation_is_byte_exact` rite restated as a feature, and it is the third time this exact overclaim has been removed from these files.
- Fixed `SourceArtifact` being described as proving byte identity in the ontology, the implementation status, and the principles. Nothing in the package reads the bytes: a digest and a length describing no file are accepted and replay. The record makes a caller's assertion immutable and attributable, which is worth having and is now what the documents say. A test pins the boundary rather than describing it.
- Fixed `action-execution` being deleted from the not-implemented list while malleus still executes nothing. Stage 8c records a dispatch and hashes an outcome contract; it performs no action and observes no outcome. The entry is restored with that distinction stated.

### Added

- Added a release-artifact allowlist gate. A branch un-gitignored the private research directory and the sdist silently absorbed sixteen files of it, on an irrevocable path to PyPI, while the wheel stayed clean: `twine check` validates metadata and never reads content, and CI smoke-tests only the wheel. The gate builds both artifacts and fails on any path under a forbidden prefix, so the property holds whatever a future `.gitignore` edit forgets. Verified to fire on the branch that carried the leak: 17 forbidden members of 71.
- Added a capability-assertion guard covering the class the previous guard missed. That guard checked a pending capability was *named* nearby and could not see the sentence three lines up asserting the capability exists; naming is not disclaiming. The new one is clause-scoped, because a requirement and a capability claim can share a sentence and the first was clearing the second. Verified to fire on all three relapsed sentences and to stay silent on the norms beside them.

## [0.8.0] - 2026-08-15

### Added

- Added the Stage 8a source-provenance boundary. `SourceArtifact` records bind
  an artifact ID, version, media type, locator, byte length, and SHA-256 digest
  into one replay-validated semantic hash. The standard builder derives this
  record from exact source bytes.
- Added replay and atomic-rejection tests for changed source bytes, altered
  source metadata, generic records pretending to be sources, and evidence
  citing the wrong source record hash.
- Added the optional Stage 8b `AssentPlan`. It verifies one proposal's exact
  epistemic-policy coverage, invokes each declared adapter once, commits valid
  completed outputs, and converts adapter exceptions or refused outputs into
  the existing `MonitorFailure` plus `UNKNOWN` record pair.
- Added failure-atomic multi-event append for one related event group. A
  logical check and its logical assessment now enter together or not at all
  when emitted through `AssentPlan`.
- Added the Stage 8c authorized-effect record path: `ActionDispatch`, terminal
  `ActionExecution`, and independent `OutcomeObservation` events.
- Added content-addressed `OutcomeContractArtifact` records and exact external
  state binding through `SourceArtifact`.

### Changed

- **Breaking:** `Evidence.source_version_id` has been removed. Every `Evidence`
  record must now bind an applied `SourceArtifact` by exact ID and ledger record
  hash. There is no legacy fallback or implicit source record.

### Boundary

- Stage 8a proves which exact bytes were registered and which exact source
  record an evidence item cited. It does not establish authenticity, truth, or
  byte-exact quotation. Resolving a quoted span against the registered bytes
  remains `citation-byte-verification` and is not implemented.
- Stage 8b runs epistemic monitor adapters only. It does not select policy,
  decide epistemic control, run authority monitors, retry work, schedule work,
  or make a whole plan atomic.
- Stage 8c records generic dispatch, execution receipts, and independently
  observed outcomes. Domain adapters still perform effects. The current profile
  records one dispatch per action and one execution per dispatch. A future
  delivery profile can add idempotency, outbox, deduplication, and external
  effect-ledger records without moving domain effects into core Malleus.

## [0.7.0] - 2026-08-14

### Added

- Added `malleus-inquisitor`: a CLI that runs mechanical rites over a malleus-derived schema (construction, root currency against the installed malleus via the strict consumer-side compatibility check, constrained type-slots, bound relation endpoints, derived-Signal shape, formula-shaped slots with no executor). Exit 0 grants the seal; findings are heresies, suspicions, and notes. Semi-serious by design; the findings are not.
- Added the `malleus-inquisitor` agent skill (`.claude/skills/malleus-inquisitor/`) applying the judgment-tier rubric to a whole repository, and the rubric itself (`src/malleus/inquisition/rubric.yaml`) as tunable data. Every rite records the generic field lesson that paid for it; two self-inquisitions of this repository drove the fixes below, and their acceptance criteria are now tests.
- Added `OntologyRegistry.schema_version`, exposing the entry schema's declared `version:`.
- Added `KnowledgeGraph.get_relation()`, `KnowledgeGraph.export_records()`, and all-or-nothing validated rehydration via `KnowledgeGraph.from_records()`, replacing the private-attribute export and string-matched idempotency patterns observed in adopters.
- Added `ResponsibleRole` (closed enum) and `ProtocolActor` (the `Agent`-mixin carrier) to the assent ontology; `responsible_role` is no longer an open string.
- Added protocol test coverage with content for the request and claim-revision arm, `ConflictAssessment`, `UncertaintyAssessment`, and `TemporalAssessment`, `Evidence`/`EvidenceAssertion` proposal members, a candidate-bound `ACCEPT` citing a `LogicalAssessment`, and graph-base supersession lineage.
- Added CI gates: releases require the full test suite and a clean-venv wheel install that invokes every console script; pull requests build and smoke the wheel; a guard test asserts every declared packaging target exists and is tracked.
- Added adoption documentation: `docs/ADOPTION_GUIDE.md`, `docs/DELIMITATIONS.md`, `docs/RECIPES.md`.
- Added `docs/PRINCIPLES.md`: the architectural thesis (typed subgraphs as composable epistemic modules whose dependencies, provenance, temporal state, and conclusions can be executed and governed), the six principles the rites defend, an explicit list of what is not claimed, and the composition question reserved as future work rather than asserted.
- Added five principles rites to the rubric (v5): `encoding_is_load_bearing` (a typed intermediate must exist and must be the thing checked), `quotation_is_byte_exact` (a citation pins verified bytes, and a source hash used only as a cache key is not a gate), `arbiter_is_accountable` (automatic acceptance names its judge, records what it saw, and defers to a queue whose age is measured), `evidence_does_not_transfer` (represent, execute, govern, and assist are separate claims, and a composition is not implied by its parts), and `module_declares_its_interface` (NOTE severity, matching the unproven status of composition). Both skills carry the principles and a scope gate: state the claim, the smallest discriminating observation, the artifact to reuse, and the exclusions before building.
- Added rules 9 and 10 to the Adoption Guide: a citation pins bytes, and nothing self-corrects. Both name the malleus capability that does not exist yet and hand the work to the adopter.
- Added `citation-byte-verification` and `deferral-queue-aging` to the not-implemented list. A third self-inquisition found `PRINCIPLES.md` asserting both as properties of the library: the root declares no citation slot and verifies no quote, and `DEFERRED` is terminal with no aging, no projection, and no blocking threshold. The principles now state the tense and point at the boundary document.
- Added `MonitorFailureCategory` and `MonitorErrorCode` to the assent ontology, closing the arbiter's reason vocabulary.
- Added a scope gate to the inquisitor skill (the CHANGELOG previously claimed both skills had one; only the acolyte did), and a stated tiebreaker in both for the one case where "no half measures" and the scope gate collide: an open gate found out of scope is recorded and surfaced, never closed silently and never deferred silently, and the human decides whether it enters the slice.

### Changed

- **Breaking:** ontology identity is now derived from the resolved constraint table the validator consults, not from declaration syntax (`FINGERPRINT_VERSION` 3). Order-dependent mixin constraint conflicts are rejected at construction, making mixin order unobservable; every effective slot emits a membership fact regardless of attachment route; numeric bounds and inert declaration variants (explicit-false flags, duplicate mixins, no-op `slot_usage` entries) canonicalize. All content hashes and fingerprints change; the bundled CYP450 logic contract is re-pinned.
- **Breaking:** assent ontology `0.7.0`: `responsible_role` narrowed to `ResponsibleRole`, `failure_category` narrowed to `MonitorFailureCategory` and `error_code` to `MonitorErrorCode` (the arbiter's reason vocabulary was an open string, so "how many deferrals came from a timeout" was a substring search; `error_message` stays free text and carries the detail), `MONITOR_FAILURE` removed from `AssessmentKind` (it was dead vocabulary no monitor could declare), `AssessmentKind` pinned by the ledger's registry contract, and the write-only `request_states` projection field removed. A `0.5.0` ledger holding a free-string `failure_category`, `error_code`, or `reason_codes` value outside the new enums does not replay unchanged: the record is refused at validation with the offending value named. There is no implicit migration.
- **Breaking (rubric v7):** the seal has a floor the rubric cannot lower. Round 4 put it on `enabled:` and not on `severity:`, one word apart in the same entry, so a rubric identical to the packaged one except `severity: NOTE` on `construction` sealed a file that is not valid YAML at exit 0, under a header reading 0 rites disabled. `Report.purity` is now false whenever `construction` said anything that was not a commendation, whatever the rubric says about how loudly. The coverage disclosure counts every disabled rite in both tiers (all 24 judgment rites could be switched off under "0 rites disabled"), reports severity downgrades beside disables because a heresy tuned to NOTE narrows the gate exactly as much as switching it off, and carries `rubric_sha256`, because the version is the operator's own word in a file they control and the digest is not.
- Fixed `root_currency` failing open on a reference root that parses and declares no malleus primitives: an empty reference has an empty fingerprint, which makes every subject a trivial superset, so the rite answered "root is current" precisely when it knew least. The reference now gets the same wrong-format refusal the subject already got, and only the currency question is skipped: the other rites still judge a perfectly good subject.
- Fixed `Report.add` raising `RubricError` for a call-site bug, which told operators their rubric was broken when the one file not at fault was the rubric. It is now `RiteContractError`, and the two constants the floor rests on cannot drift apart unnoticed.
- **Breaking (rubric v7):** a seal now states its own coverage. Every run prints the rubric path, its version, and every disabled rite, the JSON carries `rubric`, `rubric_version`, and `disabled`, and a seal granted under a reduced rubric says so on its face. `construction` can no longer be disabled at all: with the rubric made load-bearing, disabling every mechanical rite let a document that does not even parse take the seal at exit 0, which is this tool's own lesson turned against it. The rite table is now validated as a table when it loads, not one rite at a time as they fire, so a deleted entry and a duplicated id are both refusals rather than a quietly changed verdict.
- **Breaking (rubric v7):** added `root_currency_answerable` (HERESY). When the reference root could not be read at all, the currency rite recorded a hardcoded suspicion and the schema took the seal; an unknown condition now refuses. `status: low_stakes` additionally requires `status_reason`, because nobody can check "low stakes" and a sanctioned field is where a softened severity would hide.
- Added `malleus-inquisitor --rubric PATH`. The tuning contract told adopters to tune "your own copy of the rubric" and there was no way to pass one, so the only operator path was editing site-packages, which the next upgrade reverts without warning, taking every raised severity with it. `Report.add` now refuses to raise a heresy at runtime: only a rite's primary verdict may deny the seal, and only that path reads its severity from the rubric.
- **Breaking (rubric v6):** the rites now read their severity and enablement from `rubric.yaml` instead of hardcoding both. The file invited adopters to tune severities and disable rites while the CLI ignored the file entirely: a rite raised to HERESY still printed as a suspicion and still granted the seal, and a deleted rite still fired. Tuning contract, now exact: `severity` sets the rite's primary verdict (secondary findings keep their own and say so), `enabled: false` disables a rite, deleting an entry is a broken instrument rather than a quiet disable, and a rite at NOTE must declare in `status` whether the property is `open_question` or `low_stakes`, because a severity softened for convenience is forbidden by doctrine and must be distinguishable from one that is honestly low.
- **Breaking (rubric v6):** split `root` into `root` (HERESY: the primitives are absent, so nothing downstream can be judged) and `root_has_speakers` (NOTE: a declared primitive nobody extends). The single entry declared NOTE while the code emitted HERESY for the primary condition.
- Changed the inquisitor's root-currency rite to the strict consumer-side check: a vendored root that silently dropped a `required` constraint now loses the seal instead of earning one. The README and the `dependency_pin` lesson still named the producer-side `check_compatibility` for the currency question, which is the confusion `the_rite_survives_its_subject` warns about by name; both now name the strict variant and a test greps for the relapse.
- Changed a corrupt or malformed rubric from a 40-line traceback and exit 1 into a single stderr message (whose first line is actionable; a YAML parser's own multi-line context is carried through when it has one) and exit **2**. Exit 1 means the schema has heresies; a broken instrument must never be reportable as a broken subject, and the rubric is now loaded and structurally validated before any rite runs, so no half-built report is discarded.
- Changed `status.py` to derive both ontology versions from the schema files instead of restating them.

### Fixed

- Fixed lone UTF-16 surrogates committing as valid writes and then crashing the digest, staging, and ledger layers untyped: they are now rejected at validation, and every encoding failure inside `canonical_json` is a `LedgerError` on both the write and the read path.
- Fixed a `KeyError` when a domain schema relaxes `Signal.bearer_id`: the write is now a `REJECTED` operation with a reason.
- Fixed YAML syntax errors and non-UTF-8 schema files raising parser exceptions through `OntologyRegistry`: both are now `OntologyError`, so the inquisitor records a construction finding instead of a traceback.
- Fixed a missing `import_map` target being diagnosed as an absent map entry: the error now names the entry and the resolved path.
- Fixed the mixin-conflict error message prescribing a remedy (the class's own `slot_usage`) that the merge order makes impossible.
- Fixed the version-skew diagnostic being discarded by a silent `except ... pass`. When a schema will not construct, the tool tries to explain it as root drift; every failure of that explanation was swallowed, and the likeliest cause (the mapped root is itself broken or absent) was exactly the case where the hint vanished. It is now a recorded finding.
- Fixed `_rubric()` validating only the `config` block: a rubric with a good config and malformed rites raised `KeyError` downstream instead of `RubricError`.
- Fixed `docs/RECIPES.md` presenting rollback of graph and log, and a proof trace, as "malleus's own loop" in a list of production examples. Malleus has neither: staging never mutates the base graph, so there is nothing to undo, and four other shipped documents deny the proof trace. Recipe 5 now describes the isolated candidate subgraph and the typed `ViolationWitness` records that actually exist.
- Fixed the acolyte skill still stating byte-exact citation and the aging deferral queue as properties malleus provides, one file over from where the previous round corrected the same claim. The guard now reads every shipped prose surface rather than the two documents the finding happened to name.
- Fixed the currency guard being a regression test for two lines rather than a guard against the class: six ordinary rewordings walked past its word list, and it never read the CHANGELOG. It is now section-scoped and semantic, and all six evasions are caught.
- Fixed `UnavailableAssessment.reason_codes` accepting any string while being populated from the freshly closed `MonitorErrorCode` vocabulary; narrowed at the class, since decisions use the shared slot for a different vocabulary.
- Fixed the inquisitor skill naming a rubric path that cannot exist where the skill installs, the CLI printing "heresyies", and `docs/ASSENT_PROTOCOL.md` listing three record categories without noting they are schema only.

## [0.6.0] - 2026-08-12

### Added

- Added typed, content-addressed `AuthorizationPolicyArtifact` records that pin exact `AUTHORITY` monitor records.
- Added proposal-time authorization-policy bindings to every concrete `ActionProposal`.
- Added a pure authorization evaluator with fixed `SATISFIED` to `AUTHORIZE`, `VIOLATED` to `BLOCK`, and `UNKNOWN` to `CLARIFY` control, with `BLOCK` precedence.
- Added replay-bound authority assessment ordering, triggered assessment IDs, and authorization policy-evaluation hashes.
- Added `UnavailableAuthorityAssessment` and `authority_monitor_failure_records()` for atomic authority-monitor failure reporting with exact proposal, action, actor, policy, monitor, and acceptance-head context.
- Added adversarial gates for policy substitution, incomplete monitor coverage, action and actor drift, output ordering, trigger and evaluation-hash tampering, authority failure context drift, grant substitution, and verdict override.

### Changed

- Replaced opaque authorization-policy artifacts with a concrete typed artifact. Generic `ProtocolArtifact` records can no longer carry `AUTHORIZATION_POLICY`.
- Replaced caller-selected authorization verdicts with replay-recomputed control selection.
- Required completed and unavailable authority outputs to bind the exact action content hash and the action's precommitted authorization policy.
- Scoped grant sufficiency checks to `AUTHORIZE`. `BLOCK` may cite an evaluated insufficient grant but receives no authorization validity interval.
- Scoped non-authorizing grant citations to the output that selected control: `BLOCK` requires `VIOLATED`; `CLARIFY` requires `UNKNOWN`.
- Keyed authority outputs by exact action, actor, acceptance head, monitor, and optional evaluated grant, permitting changed-context reevaluation while rejecting same-context competing results.
- Required `AUTHORIZE` to use the same exact grant evaluated by every satisfied authority assessment.
- Required authority-grant action types to be nonempty, canonical, unique, and nonblank.

### Compatibility

- Version 0.6.0 does not replay 0.5.0 action proposals, opaque authorization policies, authority assessments, or authorization decisions unchanged. There is no implicit migration or default authorization policy.
- The assent ontology is version 0.5.0. The root ontology remains version 0.4.0.

### Boundary

- Stage 7c validates recorded authority outputs and derives authorization control. It does not execute authority monitors, establish policy legitimacy or a grantor trust root, or execute actions.
- Authorization policy authority, scope, eligibility, and effective-time selection remain outside this release.

## [0.5.0] - 2026-08-12

### Added

- Added typed `GraphBaseArtifact`, `CandidateSubgraphArtifact`, and `AcceptedGraphApplication` records.
- Added canonical candidate manifests containing exact ordered structural writes, explicit half-open valid-time intervals, and immutable supersession links.
- Added proposal and decision bindings to exact candidate artifact IDs, record hashes, and candidate digests.
- Added atomic accepted graph materialization inside `EPISTEMIC_DECIDED`; candidate-bound `ACCEPT` requires exactly one application and all other verdicts forbid it.
- Added a separate materialization head, cumulative accepted graph projection, and defensive current and bitemporal as-of views.
- Added `bundled_ontology_path()` so source checkouts and installed distributions resolve the exact shipped ontology without stale-environment ambiguity.
- Added adversarial gates for manifest drift, stale graph bases, missing and altered applications, rejected candidates, direct staging bypass, half-open interval boundaries, retroactive supersession, transaction prefixes, and dangling valid-time relations.

### Changed

- Bound candidate-aware logical checks to the exact candidate ontology, pre-state, post-state, and candidate digests.
- Required complete valid-time metadata for every external graph-base record and every candidate write. Valid time is never inferred from transaction time.
- Required full current-ledger verification before historical prefix projection.
- Replaced in-place JSONL append with same-directory failure-atomic file replacement. An interrupted write, file sync, or replacement leaves the last valid ledger unchanged; power-loss durability remains filesystem-dependent.
- Hid the raw storage envelope behind `ProtocolLedger` so callers cannot bypass protocol validation through a public mutator.
- Removed execution-local and potentially rejected `KnowledgeGraph.operations` entries from accepted graph projections; the protocol ledger remains their only accepted audit.
- Required a prior claim's declared `domain_valid_to`, when present, to agree with its atomic replacement boundary.
- Kept direct `CandidateSubgraph.materialize_into()` as a structural API with no effect on the protocol-derived accepted graph.
- Pinned the build backend and core metadata version used by release artifacts so distribution checks are reproducible.

### Compatibility

- Version 0.5.0 requires an explicit `application` field in every `EPISTEMIC_DECIDED` payload. It is `null` when no accepted graph application occurs. No implicit migration is applied.
- Candidate bindings are optional only as an all-or-none group, preserving protocol-only proposals while preventing partial candidate references.

### Boundary

- Accepted graph state is epistemic commitment, not truth, action authorization, or execution.
- The opaque Stage 1 snapshot anchor contributes no graph records. A matching external graph must be supplied for `GraphBaseArtifact` replay.
- Portable graph-base resolution, typed retraction, concurrent-writer serialization, policy authority, monitor orchestration, action execution, and untrusted Prolog sandboxing remain outside this release.

## [0.4.0] - 2026-08-12

### Added

- Added typed `MonitorSpecificationArtifact` records that bind assessment kind, monitor implementation hash, and exact input artifacts.
- Added typed `EpistemicPolicyArtifact` records that declare exact required monitors, outcome-to-control mappings, and deterministic control precedence.
- Added a pure policy evaluator that selects `ACCEPT`, `REJECT`, `DEFER`, or `CONTEST` only from complete, proposal-bound monitor outputs.
- Added replay-bound trigger assessments and a canonical policy-evaluation hash to every epistemic decision.
- Added proposal-time binding to one exact epistemic policy, before any monitor output exists.
- Added `UnavailableAssessment` and `monitor_failure_records()` for atomic, non-logical monitor failure reporting.
- Added adversarial tests for omitted monitors, unrequired monitors, post-output policy replacement, contradictory outputs and logical checks from one monitor, custom assessment-subclass bypass, artifact drift, outcome mapping, precedence, trigger drift, evaluation-hash drift, cross-record ID collisions, and standalone `UNKNOWN` reuse.

### Changed

- Replaced opaque monitor and epistemic-policy artifacts with concrete typed artifacts. The generic artifact path is rejected for both kinds.
- Replaced caller-selected epistemic verdicts with replay-recomputed policy results.
- Replaced incomplete typed assessments with `UnavailableAssessment`; `MONITOR_FAILED` is the only event that may introduce it.
- Required all completed assessments to use `SATISFIED` or `VIOLATED`, bind the exact typed monitor, and include required dependencies in provenance.
- Required one output from each exact monitor per proposal. A retry requires a new proposal or monitor record rather than an uncited competing assessment.
- Required one completed check from each exact logical monitor per proposal. An assessment cannot cherry-pick among contradictory applied checks.
- Rejected ID collisions across every atomic multi-record event before constructing the introduced-object map.
- Closed core assessment kinds to their standard concrete record types. A domain-defined `Assessment` subclass cannot claim a core kind without its required semantic contract.

### Compatibility

- Version 0.4.0 intentionally does not replay 0.3.0 proposal records unchanged. `ProposedSubgraph` now requires `epistemic_policy_id` and `epistemic_policy_hash`; no implicit migration or default policy is applied.

### Boundary

- Stage 6 validates recorded monitor outputs but does not execute domain-specific monitors or independently reproduce their results.
- Omitted required output blocks a decision. A real missing execution must be represented by `MonitorFailure` plus `UnavailableAssessment`.
- `UNKNOWN` may select `DEFER` or `CONTEST`, never `ACCEPT` or `REJECT`.
- Request payload selection, accepted-graph materialization, and bitemporal replay remain outside this release.
- Policy authority, eligibility, scope, and effective-time selection remain outside this release. Coverage is exact relative to the policy precommitted by the proposal, not proof that the policy is legitimate.

## [0.3.0] - 2026-08-12

### Added

- Added a versioned, domain-neutral compiler from public graph snapshots to a fixed typed Prolog fact vocabulary.
- Added strict logic contracts and typed contract artifacts that pin the ontology hash, fact-contract version, trusted local rule bytes, declared rule IDs, artifact versions, and Prolog subprocess wall-clock timeout while keeping record, semantic-contract, and raw-byte hashes distinct.
- Added process-isolated SWI-Prolog checks with exhaustive violation enumeration, canonical witness sets, deterministic fact hashes, and fail-loud malformed-result handling.
- Added immutable `LogicCheckRecord` and `ViolationWitness` protocol records plus the atomic `LOGIC_CHECK_RECORDED` event.
- Added `logic_monitor_failure_records()` so incomplete logic execution becomes `MonitorFailure` plus a logical `UNKNOWN` assessment with no completed-check claim.
- Added adversarial tests for rule injection, state leakage, timeouts, invalid programs, manifest drift, unknown witnesses, artifact mismatch, assessment disagreement, and unrelated ontologies.

### Changed

- Replaced the CYP450-specific graph translator with the generic typed fact compiler. CYP450 rules now consume the same fact vocabulary as every other ontology.
- Replaced in-process `pyswip` state with one fresh SWI-Prolog process per check to prevent cross-check fact and rule leakage.
- Replaced `proof_record_ids` with `logic_check_record_ids`. Logic execution output is no longer described as a formal proof.
- Updated the assent ontology to `0.2.0` and the package capability boundary to Stage 5.

### Removed

- Removed the old `VerificationResult`, `sync_from_kg`, domain query methods, tentative assertion path, first-violation-only result, and `pyswip` dependency.

### Boundary

- Only trusted, pinned local rule programs are supported. Untrusted Prolog sandboxing is not implemented.
- A check binds a proposal identity and candidate digest, but Stage 7b must still bind proposal content mechanically to that exact candidate before assent-gated materialization.
- `LogicCheckRecord` is execution evidence, not an independently checked proof certificate and not a claim of truth.

## [0.2.0] - 2026-08-12

### Added

- Added a separate assent ontology for immutable proposals, assessments, epistemic decisions, authorization decisions, requests, revisions, executions, outcomes, and transition records.
- Added a single-writer hash-linked JSONL protocol ledger with strict event schemas, immutable typed record hashes, contiguous sequencing, deterministic replay, derived state machines, and explicit snapshot genesis.
- Added distinct assessment, epistemic, authorization, and request outcome vocabularies. Requests and claim revisions are records, not decision values.
- Added ordered proposed-subgraph staging on isolated graph copies, deterministic materialized-state digests, stale-base detection, and all-or-nothing structural materialization.
- Added a machine-readable implementation boundary and public status document for the Stage 4 capability set.

### Changed

- Replaced permissive field checks with one closed-world instance validator covering inherited and mixin slots, required values, enum and primitive ranges, collection shape, ISO 8601 datetimes, fixed predicate values, numeric bounds, and identifiers.
- Missing imports, unresolved CURIE or URI imports without an explicit local map, unknown ranges, and imported definition collisions now fail registry construction.
- Replaced generic `DrugRelation` and `AttackRelation` classes with concrete predicate classes whose `source_id` and `target_id` use LinkML class ranges.
- Made identifiers graph-wide across entities, relations, signals, and events. Duplicate and reserved positional identifiers reject before mutation.
- Versioned the structural fingerprint format as version 2. All enforced structural facts now affect ontology identity.
- Prolog verification now consumes a complete isolated candidate overlay. The tentative single-relation assertion and retract API was deleted.

### Fixed

- Required root slots now apply to relations, signals, and events.
- Unknown properties and non-enum scalar mismatches no longer pass validation.
- Relation endpoint types are now checked against declared source and target ranges.
- Signal and event writes can no longer overwrite existing graph nodes.
- Rule-rejected candidate writes no longer require private graph and audit-log rollback because live graph mutation occurs only after verification.

### Boundary

- `Operation.COMMITTED` records structural materialization only. It does not represent epistemic acceptance or action authorization.
- Candidate materialization is an explicit structural operation. It is not gated by assent yet and must not be presented as epistemic acceptance.
- The protocol ledger projects accepted proposal membership, not a materialized accepted knowledge graph. Accepted-graph projection and general domain rule execution remain later boundaries.

## [0.1.0] - 2026-04-12

Initial public release.

### Added
- Root ontology (`ontology/malleus.yaml`) with five primitives — Entity, Event, Signal, Agent (mixin), Relation — and four cross-cutting mixins: Identifiable, Temporal, Describable, Statusable.
- `OntologyRegistry` (`src/malleus/ontology.py`): loads LinkML schemas with recursive import resolution, builds a runtime type registry, validates enum fields and required slots.
- Content-addressable hashing:
  - `OntologyRegistry.content_hash()` — deterministic SHA-256 of the canonical resolved schema.
  - `OntologyRegistry.fingerprint()` — frozenset of atomic facts (types, enums, enum values, slot ranges, inheritance).
  - `OntologyRegistry.check_compatibility(foreign_hash, foreign_fingerprint)` — returns `"identical"`, `"superset"`, `"subset"`, or `"divergent"` for distributed ontology convergence.
- `KnowledgeGraph` (`src/malleus/kg.py`): ontology-typed KG backed by NetworkX MultiDiGraph. Write-time validation (type, inheritance, duplicate, enum, required slot, endpoint). Per-operation audit log with status (COMMITTED/REJECTED) and rejection reason.
- `PrologVerifier` (`src/malleus/prolog_verifier.py`): optional domain rule verification via SWI-Prolog. Accepts multiple KGs (`sync_from_kg(*kgs)`). Tentative assertion + contradiction check + retract pattern.
- Two example domain extensions: `ontology/domains/cyp450.yaml` (CYP450 drug interactions) and `ontology/domains/attack.yaml` (MITRE ATT&CK).
- 95 tests across `test_ontology.py`, `test_kg.py`, `test_prolog_verifier.py`.
