# Synthetic supplier commitment: proposed adopter contract

Status: PROPOSED, for operator review. Luis authorized contract definition,
not implementation or acceptance of the choices below. This document adds no
runtime, ontology terms, fixture bytes, public API, or accepted demand fact.
The four-file audit packet at `2da25941d5c2a55b43fb925a7b812939a8b7158a`
remains unchanged. Core baseline is `2a11240556532c2b6160ac0bfa5ab1165e862fd2`.

## Claim and boundary

Claim: a pure GoalPredicate synthesizer may propose one supplier amendment;
only the separately authorized executor may change the synthetic supplier
source; only an independently captured, checked and accepted KCS may revise
the accepted supplier state. Reassessment distinguishes satisfaction, pending
work and refusal. No component equates those three outcomes.

Smallest observation: accepted B/Y/1 remains B/Y/1 through proposal,
authorization, execution, capture and KCS preparation. Accepted B/Y/2 appears
only after admission. The RET-010 complement survives unchanged. Reopening
from the single JSONL history reconstructs the action records and the KG.

Reuse: existing ActionProposal and effect record identities, the public KCS,
population compilation, retained-byte checks, admission, replay and trace;
canonical B/Y/e4 values and the RET-010 records. The original e7 is a semantic
comparator only, never a fresh observation caused by the experiment.

These are proposed ADOPTER_CHOICE requirements on top of a separately reviewed
OPTIONAL_PROFILE for action/history composition. Later code would be a
REFERENCE_IMPLEMENTATION and frozen tests a CONFORMANCE_FIXTURE. Without that
profile, no combined authorization-to-observed-KCS claim is made. This is one
consumer, not evidence for promoting shared action vocabulary or machinery.

## Explicit scenario parameters

All identities, actor IDs, times, source locators, policy/monitor artifacts,
canonicalization rules and implementation identities are required inputs to
the eventual frozen case. This document's symbols are parameters, not default
runtime values or fabricated source facts. Missing inputs refuse before work.

- `S0` is a separately attributed synthetic source with the canonical e4 row:
  order B, product Y, quantity 1, occurrence e4. It does not contain e7.
- `S1` is the independent capture after the execution attempt. On an actual
  amendment, its occurrence ID is supplied explicitly and differs from both
  e4 and e7. An unchanged capture retains e4 and its byte identity; a new
  observation does not manufacture a changed source.
- The initial accepted supplier record reuses `supplier-order-state:B:e4`.
  The new record ID and exact mapping from S1 are fixture inputs; they must
  not reuse the original e7 record/source identity.
- The complement is every accepted record except that initial supplier state,
  including O1, X1 and `contains:O1:X1`, their properties and temporal lineage.
- Protocol timestamps are explicitly supplied timezone-aware instants.
  Supplier valid time remains ORDER_ONLY over the declared occurrences.
  No calendar date is inferred from e4, e7, dispatch or observation time.
- The synthetic source has one controlled writer. This excludes concurrent
  external edits, network calls, payments, retries and exactly-once delivery.

Proposed goal semantics for approval: the unique eligible current B/Y record
has quantity **equal to 2**, not merely a positive quantity and not a claim of
delivered inventory or customer demand satisfaction. If an at-least-two goal
is wanted instead, its predicate and oracle must change explicitly before RED.
The optional shortfall finding `max(2 - quantity, 0)` does not itself decide
satisfaction: quantity 3 has zero shortfall but fails this equality goal.
Missing or competing eligible records never become quantity zero.

## Re-entry Contract and pure synthesis

The immutable addressable local Re-entry Contract binds:

1. The original verified full history head/count, accepted KCS context,
   effective domain contract, action profile and validated projection digest.
   Core must define their distinct coordinate domains, not alias equal names.
2. The exact scenario goal, its declared issuer and authority, eligibility
   scope, source/interpretation mapping and preservation complement. An explicit
   stable goal-episode identifier maps to the existing action key; it is not
   derived from the changing full ledger head or a fresh contract digest.
3. Exactly one permitted concrete ActionProposal subtype and operator:
   change B/Y quantity from 1 to 2 with an exact S0 precondition and a declared
   fresh occurrence. The subtype definition remains research-local.
4. Exact synthesizer, action-model, executor and observation-contract
   identities; the existing authorization policy and required monitors.
5. A candidate budget of one, one dispatch attempt for this goal episode,
   no automatic retry, refusal on competing solutions, and the stopping and
   evidence rules below. These choices are data, not hidden defaults.

The synthesizer consumes those closed immutable inputs and a verified
read-only lifecycle view. It receives no graph, history writer, mutable store,
file path to write or effect capability. It performs no retention. Repeated
invocations of identical inputs return identical canonical results.

Its internal result is one of `CANDIDATES`, `SATISFIED`, `PENDING` or `REFUSED`.
These are local result discriminants, not new Core records or change identity.
Only CANDIDATES contains output, a tuple with one existing ActionProposal.
SATISFIED, PENDING and REFUSED each contain zero candidates and an explicit
reason and relevant input identities. They do not persist themselves.

Evaluation order is fixed:

1. Validate closed grammar, capability declarations, implementation identity,
   authentic-to-this-history context binding and all required inputs. A local
   digest is not an independently authenticated checkpoint. Staleness refuses
   before any satisfaction shortcut; do not silently rebind an old contract.
2. Require exactly one eligible current supplier state and exact provenance
   agreement with the selected source/mapping. Reject malformed, missing,
   competing or unsupported meaning, never select by enumeration order.
3. Reconcile the bound goal episode with its replay-derived lifecycle. An
   unresolved prior action yields PENDING, including after a receipt while
   observation/admission remains unresolved. It never causes redispatch.
4. Return SATISFIED when the goal holds and no episode obligation remains
   unresolved. An initially satisfied goal needs no invented execution.
   Closing an acted-on episode as observed satisfaction additionally requires
   the linked observed correction, not an unrelated quantity-two fact or a
   successful receipt. A failed execution stays failed even when that evidence
   supports satisfaction; this is not an action-success or causality verdict.
5. An exhausted or terminally failed episode refuses further synthesis.
   A human may authorize a new identified episode; this slice creates none.
6. For a fresh unsatisfied episode require quantity 1, the sole operator and
   remaining budget. Another well-formed quantity yields UNREALIZABLE under
   this operator grammar. Zero budget yields BUDGET_EXHAUSTED.
7. Model-check the sole candidate's precondition, quantity-two postcondition
   and complete frame condition. A failed model check returns refusal.

Other local refusal categories include MALFORMED_INPUT, STALE_BASE,
SOURCE_DISAGREEMENT, UNSUPPORTED and AMBIGUOUS. Their eventual serialized
spelling must be frozen with the research contract; they are not new public
Core enums. No fallback strategy or implicit ranking is permitted.

## Action, observation and source-to-KCS adapters

The action payload binds the logical source, B, Y, expected quantity 1,
requested quantity 2, exact pre-state source digest and fresh occurrence ID.
The concrete subtype carries existing ActionProposal fields unchanged,
including its action key/revision and authorization-policy ID/hash. It cannot
smuggle a KCS, graph operations, an alternative supplier or a relaxed goal.
Canonical payload and full record hashes retain their distinct meanings.

The symbolic model transforms a copy of S0's decoded row. Only quantity and
the explicitly declared occurrence may differ. The conformance test compares
that result with an independent oracle, not merely the executor's output.
The model itself consumes the declared precondition, goal and frame policy,
not the test oracle.
This is model agreement, not PutGet about the world or proof of causality.

The caller submits the action through Core's proposed protocol path, including
the existing proposal epistemic-acceptance prerequisite, authority assessment
and authorization decision. No raw synthesizer output authorizes execution.
The executor requires the exact replay-verified dispatch and its actor/adapter
binding. Immediately before its controlled write it checks the authorized
external S0 precondition. A mismatch refuses the effect; no hidden rebase.

The executor writes only the synthetic source and returns an existing terminal
ActionExecution receipt with exact result identity. A separate observer reads
the actual source after execution under the identified observation contract;
it does not accept the executor's result payload as captured source bytes.
Its actor differs from the executor. Actor separation alone does not establish
independent implementation, trustworthiness or source authenticity.

The observer binds the exact execution and newly retained SourceArtifact,
using existing CONFIRMED, CONTRADICTED or INDETERMINATE outcomes. Successful
execution with unchanged source is not CONFIRMED. Failure followed by observed
quantity two does not turn the execution into success or establish causality.

The source adapter separately validates exact captured bytes, closed source
shape, selected occurrence, B/Y identity, integer quantity, every mapped field,
new record identity, explicit supersession and ORDER_ONLY valid time. It
returns ordinary population inputs, then the existing KCS through the public
compiler/composer. No mutation occurs through the mapper or synthesizer.
This bounded adapter supports unchanged S0 or the declared quantity-two
replacement. Other captured values remain evidence but produce UNSUPPORTED,
not a guessed correction or a claim that the source is false.
The caller retains inputs and obtains a fresh verified KCS context before
composition. Admission rechecks that context; a stale candidate is refused.

Observed state may justify a KCS even after a failed execution when the
declared evidence policy supports it. Execution failure remains recorded.
Unchanged observed bytes supply no quantity-two correction. A refused KCS
leaves accepted state unchanged; no second attempt is inferred automatically.

## Proposed check producers, not canned assessments

The first cut proposes two deterministic local producers. Their implementation
bytes, configuration, actor and input identities must be frozen and retained
through existing MonitorSpecificationArtifact references before any run. No
producer implementation or hash is invented in this design.

The epistemic producer emits existing TypeAssessment from validation of the
exact action/proposal records against the retained record contract. It checks
the declared concrete subtype, required fields and closed shapes, not source
truth or usefulness. The proposed policy requires this monitor, maps a
completed violation to REJECT and unavailability to DEFER, with REJECT before
DEFER. It accepts only the required completed SATISFIED result. All ruleset
references required by EpistemicPolicyArtifact must resolve; no empty or
invented ruleset identity fills a required field. Source agreement, goal
eligibility and model/frame checks remain separately bound synthesis evidence,
not stronger claims smuggled into TYPE.

The authority producer emits existing AuthorityAssessment after checking the
exact proposal/action, intended executor, grant, authorization policy and
requested interval. For this proposed direct-grant case it checks exact
grantee/action-type agreement, an explicitly bound scope record for the
synthetic target, no subdelegation, and interval containment. Scope matching
is equality against the declared target association, not an undeclared
hierarchy or inferred grantor legitimacy. Checked and violated predicate
identities are recorded. Known mismatch yields VIOLATED, not UNKNOWN.

Unavailable execution of either check records existing MonitorFailure paired
atomically with the corresponding UnavailableAssessment or
UnavailableAuthorityAssessment. It never fabricates a completed negative or
positive result. Core recomputes control from the recorded outputs; replay
does not run these producers. Tests must invoke real producer logic on both
matching and mismatching inputs, not use the existing test helpers whose
caller supplies an outcome. Monitor invocation remains explicit, outside the
pure synthesizer and outside Core append/replay.

## Conformance obligations, not current passing tests

| Obligation | Required observation |
| :--- | :--- |
| Representation round-trip | Canonical valid contract/action values parse to the same values; invalid or unknown required meaning refuses. |
| Pure and deterministic synthesis | Same exact inputs produce same candidate bytes/status; no writer authority or external calls. |
| No-op and explicit ambiguity | Initially satisfied goal writes nothing; missing/competing eligible states do not silently become a solution. |
| Goal versus shortfall | Quantity 3 does not pass the equality goal merely because shortfall is zero. |
| Stale and tampered projection | Rebound fake contents or old coordinates refuse even if they appear satisfied. |
| Model/frame agreement | Independent expected quantity/occurrence and all unmentioned source fields agree; simulation changes no accepted state. |
| Authorization | Unaccepted proposal, missing assessment, BLOCK, CLARIFY, expiry, wrong actor/hash or stale semantic context cannot dispatch. |
| Own progress | Valid protocol-only appends advance full history without invalidating themselves merely through head movement. |
| Pending/repeat | Same goal episode cannot issue a second action or dispatch; PENDING is not SATISFIED. |
| Receipt is not evidence | Success/attempt/failure without independent supporting source leaves accepted B/Y/1. |
| Failure after write | New observed bytes can support a fact while the failed receipt and uncertain causality remain intact; no automatic retry. |
| Source agreement | Wrong source, row, field, product, occurrence or omitted structure cannot pass by structural validity alone. |
| Atomic refusal | Invalid protocol batch or KCS changes no authoritative ledger bytes or KG state. |
| Observed correction | Only ordinary acceptance yields B/Y/2; full complement, history and exact trace survive JSONL-only reopen. |
| Episode closure | Fresh reassessment after linked observed correction returns SATISFIED with no candidate, retention or effect. |

Reopening and rechecking uses retained contracts, profiles, sources and machine
inputs, not ambient fixture/oracle files. Independent expected outputs stay
outside execution. Two different histories yielding the same current graph
may supply a separate non-invertibility witness; graph equality must not be
misreported as equality of histories, state heads or lineage.

Replacement remains unproved until a deliberately different synthesizer or
adapter passes the same boundary suite without downstream changes. This
single controlled implementation would establish neither world truth nor
general semantic repair. Structural validity, source faithfulness and
adequacy for this exact goal require separate evidence.

Dependency tuples: synthesis implements local GoalPredicate putback; synthesis
consumes Re-entry Contract and verified views; synthesis produces ActionProposal;
Core admission governs protocol records; dispatch gates executor; observer
produces source-bound OutcomeObservation; source adapter produces population
inputs; composer produces KCS; KCS admission governs the only KG change; replay
produces both accepted KG and protocol lifecycle views from one history.

## Approval and implementation gate

The operator must approve this equality goal, one-operator/one-episode policy,
synthetic source attribution and the exact Core composition contract together.
Before RED, freeze concrete parameter values, subtype schema, all governing
artifact identities and independent expected outputs. Missing Core semantics
or an unsupported declared capability blocks execution; no fixture substitute
may make the E2E green. No generic API, shared ontology promotion, paid call,
paper change, remote publication or implementation is authorized by this file.
