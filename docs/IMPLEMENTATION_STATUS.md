# Implementation Status

Malleus package version `0.7.0` implements the
`stage-7c-policy-selected-authorization-control` boundary.

This is a capability boundary, not a claim that the research program is
complete. The machine-readable source is `malleus.IMPLEMENTATION_STATUS`.

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
- Stage 7b: content-addressed external graph bases, exact temporal candidate
  manifests, proposal and decision binding, atomic accepted applications,
  derived accepted-graph projection, and transaction-time plus valid-time replay
- Stage 7c: typed authorization policies, proposal-time action-policy commitment, exact
  required authority-monitor coverage, deterministic `AUTHORIZE`, `BLOCK`, or
  `CLARIFY` selection, and verdict-scoped grant validation

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
base graph. `CandidateSubgraphArtifact` stores the exact ordered structural
writes, their explicit half-open valid-time intervals, supersession links, and
pre-state and post-state digests. `AcceptedGraphApplication` binds one accepted
decision to that exact candidate in the same `EPISTEMIC_DECIDED` event.

Replay restages every candidate against the reconstructed accepted graph. A
candidate-bound `ACCEPT` requires exactly one application; every other verdict
requires none. Replay keeps `acceptance_head`, `materialization_head`, cumulative
accepted graph digest, and valid-time view digest separate. `AcceptedGraphProjector`
rebuilds current or historical views from the verified ledger and requires an
explicit valid-time query. NetworkX remains a derived projection, not a second
authority.

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

## Not implemented

- `portable-graph-base-resolution`: retrieving graph bytes from an artifact locator rather than requiring the caller to supply the matching base graph
- `typed-retraction-semantics`: removing a record without replacing it with a new immutable record
- `multi-writer-ledger-serialization`: safe concurrent append coordination
- `action-execution`: execution after authorization
- `review-report-recording`: an `EventType` that can carry a `ReviewReport`; the type exists in the schema with no protocol door
- `outcome-observation-recording`: recording what an executed action actually did; `OutcomeObservation` exists in the schema with no protocol door
- `protocol-actor-registration`: registering `ProtocolActor` records so `responsible_actor_id` can range over actors instead of bare strings
- `evidence-assertion-recording`: proposals carrying `Evidence` and `EvidenceAssertion` members with content, including `EvidencePolarity`
- `untrusted-rule-program-sandboxing`: safe execution of uploaded or otherwise untrusted rule programs
- `monitor-execution-orchestration`: executing every selected monitor rather than validating its recorded output
- `citation-byte-verification`: verifying at write time that a quoted span is a verbatim substring of the source it cites, and invalidating the citation when the source hash changes. `Evidence.locator` and `Evidence.source_version_id` are unverified strings today. Principle 2 of `PRINCIPLES.md` states this as a property a malleus-shaped system must have; malleus does not yet provide it
- `deferral-queue-aging`: measuring how long a `DEFERRED` proposal has been waiting and blocking past a threshold. `DEFERRED` is a terminal state with no aging, so a deferral is indistinguishable from a decision nobody revisited. Principle 3 of `PRINCIPLES.md` and the `arbiter_is_accountable` rite both require this of an adopter's application layer; malleus supplies the decision record, not the queue
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

Stage 6 selects control from recorded monitor outputs. It does not orchestrate
type, evidence, conflict, uncertainty, temporal, or logical monitor execution,
and it does not choose request payloads or recipients. Stage 5's logical
verifier remains an explicitly invoked component. Monitor implementation and
input hashes make these dependencies inspectable without pretending that
Malleus independently reproduced their results. Numeric confidence remains
excluded until a calibration contract exists.

Core assessment kinds are closed to their declared concrete types. Extensible
assessment kinds require a future explicit capability contract; a domain class
cannot reuse a core kind while dropping its evidence fields. Version 0.4.0 also
adds required policy ID and hash fields to `ProposedSubgraph`, so 0.3.0 ledgers
do not replay unchanged. There is no implicit migration or default policy.
Proposal-time pinning prevents ex-post policy selection but does not establish
authority, eligibility, domain scope, or effective time for that policy. Exact
coverage is relative to the proposal's precommitted policy, not system-wide.

Stage 7c selects authorization control from recorded authority outputs. It does
not execute authority monitors, establish a grantor trust root, decide which
authorization policy is legitimate, or execute an authorized action. The
fixed outcome-to-control mapping is protocol behavior, not proof that an input
authority assessment is correct.

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
ontology is `0.4.0`; the assent ontology is `0.7.0`.

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
