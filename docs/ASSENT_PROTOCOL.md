# Assent Protocol

Malleus separates structural graph materialization, epistemic acceptance, and
action authorization. These are different operations with different records
and state machines.

The assent schema is `ontology/assent.yaml`. It imports the minimal Malleus
root ontology rather than expanding that root with protocol-specific concepts.

## Record categories

`ProtocolRecord` is the abstract root for immutable protocol records. Each
record binds its content hash to the event that generated it, the responsible
actor and role, generation time, and referenced source records.

The main categories are proposals and first-order members; assessments and
monitor failures; epistemic and authorization decisions; requests, reports,
and revisions; transition, execution, and outcome records; and versioned
monitor, policy, rule, contract, and authority-grant artifacts.

Stage 6 makes two previously opaque artifacts concrete.
`MonitorSpecificationArtifact` binds one assessment kind, implementation hash,
and exact input artifacts. `EpistemicPolicyArtifact` binds the complete required
monitor set, per-monitor handling for `VIOLATED` and `UNKNOWN`, and precedence
when several controls fire.

`ProposedSubgraph` binds the exact epistemic-policy ID and record hash before
monitoring. The proposal cites that policy in `source_record_ids`. A decision
using any other policy fails replay, including a policy registered after the
monitor outputs were observed.

Precommitment does not establish policy legitimacy. Any applied typed policy
can currently be selected by a proposal. Policy authority, domain scope,
eligibility, and effective-time rules remain unimplemented. Exact monitor
coverage is therefore relative to the precommitted policy, not system-wide.

`ActionProposal` is abstract. A domain ontology must define a concrete action
class and its typed parameters.

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

`UNKNOWN` cannot support `ACCEPT` or `AUTHORIZE`.

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
`UNKNOWN` assessments are valid only in the same atomic `MONITOR_FAILED` event
as their cited failure. A later standalone assessment cannot reuse a failure.
Replay verifies the typed contract artifact, its semantic digest, the separate
rule-set record and raw-byte hashes, and agreement between the contract, check,
and assessment. Candidate, state, and fact digests remain monitor attestations
until Stage 7b binds protocol proposals to canonical graph materialization.

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

The grantor must be the actor that records the grant. This authenticates the
ledger attribution only. Whether that grantor is itself entitled to delegate
authority remains an external trust-root and policy question.

Authorization remains a record. This stage does not execute the action.

## JSONL ledger

`ProtocolLedger` uses one JSON object per line and one writer. Every event has a
contiguous sequence, timezone-aware nondecreasing transaction time, ontology
hash, previous hash, and event hash. Duplicate keys, nonfinite numbers, unknown
fields, sequence gaps, broken hashes, blank lines, and partial final records are
fatal.

The ledger validates the complete candidate history before appending a line.
Replay revalidates the same event sequence and reconstructs all state from
scratch. Callers may retain the expected event count and head hash outside the
ledger to detect complete truncation or replacement.

One ledger is frozen to one ontology hash. Replaying across ontology upgrades
requires an explicit migration into a new ledger.

The first event is `EXTERNAL_SNAPSHOT_ANCHORED`. It binds a digest and record
count for an external accepted snapshot, but does not import or reinterpret its
records. The Stage 1 research graph therefore remains unchanged and does not
silently become protocol-accepted knowledge.

`acceptance_head` commits to the ordered sequence of accepted proposal,
decision, and revision content. It is not a digest of a materialized current
knowledge graph.

`stage_subgraph()` now provides a separate structural boundary. It validates an
ordered candidate on an isolated graph copy, records the exact ontology and
base-state digests, and rejects stale materialization targets. This mechanism
is not coupled to assent replay yet. Calling `materialize_into()` therefore
does not mean that a proposal was epistemically accepted or authorized.

## Current claim boundary

This implementation supports a narrow claim: Malleus has an executable,
structurally enforced protocol ontology and replay-derived state machine that
separate proposals, monitor failures, assessments, epistemic decisions, and
action authorization. It also has non-mutating proposed-subgraph staging and
stale-checked, all-or-nothing structural materialization.

It does not yet establish assent-gated materialization, domain-specific monitor
execution orchestration, action execution safety,
bitemporal as-of reconstruction, formal PROV-O interoperability, or an
empirical metacognitive effect.

Version 0.4.0 changes the required `ProposedSubgraph` shape. Ledgers written by
0.3.0 do not replay unchanged because they lack the proposal's policy ID and
hash. Malleus applies no implicit policy and supplies no silent migration.

General logical verification currently accepts only trusted, pinned local rule
programs. It does not sandbox untrusted Prolog. A logic check identifies both a
proposal and a candidate digest, but Stage 7b must still prove that the proposal
was compiled into exactly that candidate before accepted-graph materialization.
