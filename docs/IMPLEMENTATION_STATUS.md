# Implementation Status

Malleus package version `0.9.0` implements the
`stage-8c-executable-provenance-and-effect-closure` boundary.

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
- Evidence and evidence-assertion proposal members with typed polarity, exact
  claim and evidence references, and decision-local citation checks

## Stage 8a

- Content-addressed `SourceArtifact` records declaring a source digest and length
- Exact `Evidence` binding to an applied source artifact ID and record hash
- Replay validation of source semantic hashes and atomic refusal of tampering

Stage 8a records what the caller declared about the bytes and makes that
declaration immutable and attributable. It does not read the bytes: a digest
and length describing no file are accepted and replay. It does not
authenticate the source, establish its truth, verify that a quotation occurs
within it, or notice that it changed. Those are separate checks, and the first
of them is `citation-byte-verification` below.

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
- `review-report-recording`: an `EventType` that can carry a `ReviewReport`; the type exists in the schema with no protocol door
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
ontology is `0.4.0`; the assent ontology is `0.8.0`.

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
| `0.8.0` | `stage-8c-executable-provenance-and-effect-closure` | Exact source bytes, thin epistemic monitor adapters, authorized dispatch, execution receipts, and independent outcome observations |
| `0.9.0` | `stage-8c-executable-provenance-and-effect-closure` | Same boundary; all LinkML built-in ranges load, the bundled root resolves without a map, and a construction failure names the rites it skipped |
