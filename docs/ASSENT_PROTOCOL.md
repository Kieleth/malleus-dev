# Assent Protocol

Malleus separates structural graph materialization, epistemic acceptance, and
action authorization. These are different operations with different records
and state machines.

The assent schema is `ontology/assent.yaml`. It imports the minimal Malleus
root ontology rather than expanding that root with protocol-specific concepts.


A note on primitives, so the inquisitor's output reads as intent rather than
omission: every protocol record extends `Entity` deliberately. The records
are the durable commitments; occurrences live in the ledger's event
envelopes, and graph content (including Event, Signal, and Relation
subtypes) comes from the domain schema, not from the protocol.

## Record categories

`ProtocolRecord` is the abstract root for immutable protocol records. Each
record binds its content hash to the event that generated it, the responsible
actor and role, generation time, and referenced source records.

The main categories are proposals and first-order members; assessments and
monitor failures; epistemic and authorization decisions; requests, reports,
and revisions; transition, dispatch, execution, and outcome records; and
versioned monitor, policy, rule, contract, and authority-grant artifacts.
`ReviewReport` remains schema only, with no protocol event door.

Stage 6 makes two previously opaque artifacts concrete.
`MonitorSpecificationArtifact` binds one assessment kind, implementation hash,
and exact input artifacts. `EpistemicPolicyArtifact` binds the complete required
monitor set, per-monitor handling for `VIOLATED` and `UNKNOWN`, and precedence
when several controls fire.

`ProposedSubgraph` binds the exact epistemic-policy ID and record hash before
monitoring. The proposal cites that policy in `source_record_ids`. A decision
using any other policy fails replay, including a policy registered after the
monitor outputs were observed.

Stage 7b adds `GraphBaseArtifact`, `CandidateSubgraphArtifact`, and
`AcceptedGraphApplication`. The graph base commits the external graph used to
seed replay. The candidate artifact contains the exact ordered structural
writes and an explicit valid-time envelope for each write. The proposal and
decision bind the candidate by ID, record hash, and candidate digest. An
accepted application binds that proposal, decision, candidate, ontology,
acceptance heads, materialization heads, and graph state digests in one event.

Stage 7c adds `AuthorizationPolicyArtifact` and
`UnavailableAuthorityAssessment`. Each concrete `ActionProposal` binds one
exact authorization policy by ID and record hash before it can enter a
proposal. The policy pins a canonical, nonempty set of exact `AUTHORITY`
monitor records. The policy depends on those monitor records; the monitors do
not depend on the composed policy, which avoids a content-hash cycle.

Unreleased Stage 8a adds `SourceArtifact`. Its semantic hash binds the artifact
ID and version to the SHA-256 digest and length of the exact source bytes, plus
their media type and locator. `Evidence` must name that applied source record
and its exact ledger record hash. A changed source therefore requires a new
source record and invalidates the old evidence binding.

This is source identity, not source truth. Replay validates the recorded
commitment but does not fetch the locator, authenticate its publisher, or
verify a quoted span against the bytes.

Precommitment does not establish policy legitimacy. Any applied typed policy
can currently be selected by a proposal. Policy authority, domain scope,
eligibility, and effective-time rules remain unimplemented. Exact monitor
coverage is therefore relative to the precommitted policy, not system-wide.

`ActionProposal` is abstract. A domain ontology must define a concrete action
class and its typed parameters. Every concrete action also inherits required
authorization-policy ID and hash fields.

## Disjoint outcomes

```text
AssessmentOutcome    = SATISFIED | VIOLATED | UNKNOWN
EpistemicVerdict     = ACCEPT | REJECT | DEFER | CONTEST
AuthorizationVerdict = AUTHORIZE | BLOCK | CLARIFY
RequestState         = OPEN | FULFILLED | CANCELLED
```

`SEEK_EVIDENCE` and `SEEK_HUMAN` are request records. `SUPERSEDE` is an atomic
claim-revision record attached to acceptance of a replacement. None is a
decision value.

A failed monitor produces two distinct records in one event:

1. `MonitorFailure`, describing the failed monitoring attempt.
2. `UnavailableAssessment`, whose outcome is `UNKNOWN` and whose
   `monitor_failure_id` identifies that failure.

`UNKNOWN` cannot support `ACCEPT` or `AUTHORIZE`. An unavailable authority
monitor produces `MonitorFailure` plus `UnavailableAuthorityAssessment` and
selects `CLARIFY` when authorization control runs.

A completed logic monitor first records one `LogicCheckRecord` and zero or more
`ViolationWitness` records atomically. The check binds the proposal, candidate
and state digests, ontology, monitor, logic contract, rule-set bytes, engine,
timeout, compiled facts, complete checked-rule set, and complete violation set.
A subsequent `LogicalAssessment` must cite exactly that applied check and agree
with its proposal, base head, monitor, rules, violations, and outcome.

`SATISFIED` requires a completed check with no violations. `VIOLATED` requires
at least one witness whose record IDs occur in the translated input scope. A
timeout, unavailable engine, invalid program, bad manifest, or malformed result
does not create a completed check. It creates `MonitorFailure` plus an
`UnavailableAssessment` bound to the logical monitor, logic contract, and
ruleset. The records are execution evidence, not formal proof certificates.
For a candidate-bound proposal, the check's candidate, pre-state, post-state,
and ontology commitments must match the exact candidate artifact.
`UNKNOWN` assessments are valid only in the same atomic `MONITOR_FAILED` event
as their cited failure. A later standalone assessment cannot reuse a failure.
Replay verifies the typed contract artifact, its semantic digest, the separate
rule-set record and raw-byte hashes, and agreement between the contract, check,
assessment, and bound candidate.

## Policy-selected monitoring and control

An epistemic policy lists exact monitor IDs and record hashes. Each required
monitor has two declared controls: one for `VIOLATED`, and one for `UNKNOWN`.
Violation controls may be `REJECT`, `DEFER`, or `CONTEST`. Unknown controls may
only be `DEFER` or `CONTEST`. `ACCEPT` is selected only when every required
monitor reports `SATISFIED`.

Replay requires exactly one assessment per required monitor, bound to the same
proposal, proposal hash, and acceptance head. It rejects missing monitors,
unrequired monitors, duplicate monitor outputs, monitor-version drift, and
assessment-kind drift. When several controls fire, the policy's explicit
precedence chooses one. The decision records every assessment, the subset that
triggered control, and a canonical hash of the complete policy evaluation.

An exact monitor may produce only one output for a proposal. A logical monitor
may also produce only one completed check for that proposal. A later
contradictory output or check cannot be recorded and then hidden from the
decision. A retry uses a new proposal or a new immutable monitor record. For core kinds,
the assessment record must also be the declared concrete type. A custom
`Assessment` subclass cannot claim `LOGICAL`, for example, without a
`LogicalAssessment` and its required check, contract, and ruleset evidence.
Atomic multi-record events require distinct IDs across all introduced records,
so one record cannot overwrite another during replay projection.

Malleus validates these recorded outputs but does not execute all monitor
implementations in Stage 6. A missing execution is never inferred from absence.
It must be reported as `MonitorFailure` plus `UnavailableAssessment`; otherwise
the decision fails for incomplete coverage.

Unreleased Stage 8b adds the optional `AssentPlan` described in
`ASSENT_PLAN.md`. It replays one proposal's exact epistemic policy, verifies a
canonical adapter step for every required monitor, invokes each once, and
records either its completed assessment or the existing typed failure plus
`UNKNOWN` pair. A logical adapter supplies its check and assessment as one
failure-atomic event batch. The whole plan remains non-atomic.

`AssentPlan` does not select the policy or epistemic verdict and does not run
authority monitors. The existing deterministic evaluator still selects
control only after the required outputs exist.

Assessments can be recorded while a proposal remains `PROPOSED`. Adding the
policy-derived decision is a separate event. This gives the empirical design a
mechanical C3 condition with monitoring recorded and control disabled, and a C4
condition with the same monitoring plus explicit control.

## Replay-derived state

Proposals and action proposals do not carry mutable state fields. Replay
derives their states from validated transition records:

```text
PROPOSED -> ACCEPTED | REJECTED | DEFERRED | CONTESTED
PENDING  -> AUTHORIZED | BLOCKED | CLARIFICATION_REQUIRED
```

One immutable revision receives at most one terminal decision. Continuing
after rejection, deferral, contestation, or clarification requires a new
proposal or action revision with a direct lineage link. The previous record
remains in history.

`ACCEPT` requires every policy-selected assessment to be `SATISFIED`. Replay
derives the required set and verdict from the typed policy rather than trusting
the caller's selection.

`AUTHORIZE` requires an accepted proposal containing the exact action revision,
an applied acceptance decision, current supporting claim versions, applied
`SATISFIED` authority assessments bound to the action and actor, and an
`AuthorityGrant` for that actor and action type. The authorization interval
must remain within the grant interval.

The caller does not select the authorization verdict. Replay evaluates the
action's precommitted authorization policy against exact authority outputs.
All `SATISFIED` outputs select `AUTHORIZE`; any `VIOLATED` output selects
`BLOCK`; otherwise any `UNKNOWN` output selects `CLARIFY`. `BLOCK` precedes
`CLARIFY`. The decision must reproduce the policy-ordered assessment IDs,
triggered IDs, evaluation hash, and verdict exactly.

Grant sufficiency is checked only for `AUTHORIZE`. A `BLOCK` may cite the exact
grant evaluated by a triggered `VIOLATED` assessment, even when that grant is
insufficient, but it receives no authorization interval. `CLARIFY` likewise
receives no authorization interval. A satisfied assessment cannot authorize
under a different grant from the one it evaluated.

Authority output uniqueness is scoped to the exact action, evaluated actor,
acceptance head, monitor, and optional evaluated grant. The same context cannot
produce competing outputs. A changed head, actor, or grant can produce a fresh
output instead of leaving the action permanently bound to a stale assessment.

The grantor must be the actor that records the grant. This authenticates the
ledger attribution only. Whether that grantor is itself entitled to delegate
authority remains an external trust-root and policy question.

Authorization remains a record. Stage 7c validates recorded authority outputs;
it does not execute authority monitors, determine policy legitimacy or grantor
trust, or execute the action.

Unreleased Stage 8c opens three later event doors. `ActionDispatch` requires an
exact applied `AUTHORIZE` decision, its authorized executor, acceptance head,
and a dispatch time inside the authorization interval. `ActionExecution`
records the domain adapter's terminal receipt. `OutcomeObservation` records a
different actor's result under a pinned `OutcomeContractArtifact` and binds the
exact external-state bytes through `SourceArtifact`.

Malleus records and validates these events. The domain adapter performs the
effect and the external observer applies the outcome contract. See
`EFFECT_PROTOCOL.md` for the trust and exactly-once boundaries.

## JSONL ledger

`ProtocolLedger` uses one JSON object per line and one writer. Every event has a
contiguous sequence, timezone-aware nondecreasing transaction time, ontology
hash, previous hash, and event hash. Duplicate keys, nonfinite numbers, unknown
fields, sequence gaps, broken hashes, blank lines, and partial final records are
fatal.

The ledger validates the complete candidate history before committing a line.
It writes a complete same-directory temporary file, syncs that file, and then
replaces the prior ledger. Interrupted writes, file syncs, and replacements
leave the last valid ledger unchanged. Power-loss durability of the directory
entry remains filesystem-dependent. Replay revalidates the same event sequence
and reconstructs all state from scratch. Callers may retain the expected event
count and head hash outside the ledger to detect complete truncation or
replacement.

One ledger is frozen to one ontology hash. Replaying across ontology upgrades
requires an explicit migration into a new ledger.

The first event is `EXTERNAL_SNAPSHOT_ANCHORED`. It binds a digest and record
count for an external accepted snapshot, but does not import or reinterpret its
records. The Stage 1 research graph therefore remains unchanged and does not
silently become protocol-accepted knowledge.

`acceptance_head` commits to the ordered sequence of accepted proposal,
decision, and revision content. It is not a digest of a materialized current
knowledge graph.

`materialization_head` separately commits the graph base and ordered accepted
applications. The cumulative accepted graph digest commits all structurally
materialized records. A valid-time view has its own digest. These values are
not interchangeable.

The opaque snapshot anchor contributes no graph records. Accepted graph replay
starts only after a `GraphBaseArtifact` matches an externally supplied graph's
ontology and state digest and provides valid-time metadata for every base
record. Candidate artifacts then store replayable writes rather than digest-only
attestations.

A candidate-bound `ACCEPT` and its single `AcceptedGraphApplication` occur in
the same event. Replay validates the proposal, decision, candidate, logical
checks, heads, and pre-state and post-state digests before swapping the derived
graph. Non-accepting verdicts forbid applications. Epistemic acceptance can
therefore change accepted knowledge, but it cannot authorize or execute an
action.

`AcceptedGraphProjector.current()` and `.as_of()` require explicit valid time.
Intervals use `valid_from <= query < valid_to`; a missing end is unbounded.
Transaction-time views use the ledger event prefix, with sequence as the tie
breaker. A retroactive revision affects only transaction prefixes that include
the later revision. Active relations whose endpoints are not active fail
loudly rather than producing a dangling view.

Accepted graph views omit the local `KnowledgeGraph.operations` audit. That
audit contains execution-local timestamps and may contain rejected writes made
while constructing the externally supplied base. The ledger application
records, candidate manifests, and temporal metadata are the accepted audit.

`stage_subgraph()` remains a separate structural boundary. It validates an
ordered candidate on an isolated graph copy, records the exact ontology and
base-state digests, and rejects stale materialization targets. Directly calling
`materialize_into()` does not affect the ledger projection and does not mean
that a proposal was epistemically accepted or authorized.

## Current claim boundary

This implementation supports a narrow claim: Malleus has an executable,
structurally enforced protocol ontology and replay-derived state machine that
separate proposals, monitor failures, assessments, epistemic decisions, and
action authorization. Exact proposed mutations can be bound to acceptance,
materialized atomically, and reconstructed by transaction time and valid time.

It does not establish truth, source authenticity, quoted-span correctness,
policy legitimacy, authority-monitor orchestration, general workflow
orchestration, domain-effect correctness, exactly-once external execution,
concurrent-writer safety, formal PROV-O interoperability, or an empirical
metacognitive effect.

Version 0.5.0 changes the `EPISTEMIC_DECIDED` event shape by requiring an
explicit `application` field, which is `null` when no accepted graph application
occurs. Candidate bindings are optional as a group so protocol-only proposals
remain representable. Malleus supplies no silent migration.

General logical verification currently accepts only trusted, pinned local rule
programs. It does not sandbox untrusted Prolog. The graph base must be supplied
by the caller; portable resolution from an artifact locator is not implemented.

## Design lineage and claim limits

The components are established prior work. Clark and McCabe's 2007
[ontology schema for an agent belief store](https://doi.org/10.1016/j.ijhcs.2007.03.004)
uses ontology constraints, logic rules, justifications, and revision for an
agent belief store. [PROV-O](https://www.w3.org/TR/prov-o/) supplies the standard
provenance vocabulary that motivates explicit entities, activities, agents,
sources, and responsibility, although Malleus does not yet claim formal PROV-O
interoperability. [Sentinel](https://arxiv.org/abs/2604.12177) independently
uses proposed graph mutations, counterfactual state, invariant checks, and
allow, block, or clarify control. [TOKI](https://arxiv.org/abs/2606.06240)
independently develops typed bitemporal contradiction operators and retained
provenance.

Stage 7b does not claim novelty for any of those components. Its research use
is the mechanically testable composition of ontology-typed candidate
subgraphs, explicit monitoring, policy-selected epistemic control, exact logic
bindings, atomic knowledge commitment, bitemporal replay, and a separate action
authorization boundary. Whether that composition produces a measurable
metacognitive effect remains an empirical question.
