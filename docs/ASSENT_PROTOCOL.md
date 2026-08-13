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
2. An assessment for the required monitor whose outcome is `UNKNOWN` and whose
   `monitor_failure_id` identifies that failure.

`UNKNOWN` cannot support `ACCEPT` or `AUTHORIZE`.

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

`ACCEPT` requires every cited assessment to be `SATISFIED`. This does not yet
decide which assessment kinds a policy requires. Executing a versioned policy
and proving monitor coverage belong to the later monitoring and control stage.

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

It does not yet establish assent-gated materialization, general logical
verification, policy-selected monitor completeness, action execution safety,
bitemporal as-of reconstruction, formal PROV-O interoperability, or an
empirical metacognitive effect.
