# One-history action composition: proposed Core contract

Status: PROPOSED design for operator review, not an accepted contract or
implementation-ready wire specification. Core supplied this definition after
inspection of main `2a11240556532c2b6160ac0bfa5ab1165e862fd2`, tree
`2f376922f108601d871361d9a7b53e4b5e156ad5`. No public API name is selected.
The approval and grammar gates at the end are substantive, not editorial.

## Scope and authority

The proposed OPTIONAL_PROFILE records existing proposal, assessment, epistemic
decision, authorization, dispatch, execution and observation roles in the
same authoritative history that admits KnowledgeChangeSets. Protocol-only
transitions advance that history and derived protocol state. They cannot
change the domain KG, accepted KCS list, KCS acceptance head or materialization
head. The existing KCS remains the sole governed domain-change identity.

Core owns approved persistence/interpreter mechanisms. The first action
profile and supplier scenario remain research-local. Nothing is added to the
default STRUCTURAL_HISTORY_BUNDLE. No global Assent replacement, old-ledger
migration, CandidateSubgraphArtifact application, dummy KCS, second log,
private writer, domain executor, observer or arbitrary callback is permitted.
One consumer does not satisfy the shared-promotion gate. Existing standalone
Assent use is not a second consumer of this new KCS composition.

## Append inputs, outputs and identity

The proposed operation consumes the existing history, explicit expected full
ledger head/count, a nonempty immutable ordered batch of typed event bodies
with explicit event IDs/actors/transaction times, and exact newly registered
artifact/source bytes. Required identities resolve to the verified prefix or
an earlier introduction explicitly allowed by the staged batch contract.
No ambient file, registry, current time, outcome or monitor callback is used.
Actual coordinates are replay-derived and compared with caller expectations.

Success returns the committed ledger receipt, reconstructed protocol state
and existing KG replay. Refusal returns a typed reason and preserves exact
prior file bytes and replay state. Proposal, authorization, dispatch and
receipt outputs are not KCSs and cannot cause graph application.

Retain the existing full typed ActionProposal subtype, ProposedSubgraph,
assessments, EpistemicDecision, AuthorizationDecision, TransitionRecord,
AuthorityGrant, ActionDispatch, ActionExecution, OutcomeObservation,
SourceArtifact and policy/monitor artifact roles. Preserve nested values,
integers, booleans, enums, optional/null distinctions and ordered arrays.
Hiding a serialized record in an unchecked STRING is not conformance.

Record identity remains `ledger.record_hash(record_type, record)`, canonical
record type plus every field except content_hash. Event identity remains the
selected ledger-envelope hash. Record hash, raw-byte digest, artifact semantic
hash, compiled contract identity and KCS identity stay distinct. Each record
validates under its exact retained record contract and binds generation event,
generation time and responsible actor to its enclosing event. Provenance and
source_record_ids are validated, not merely retained. Same-event introductions
must declare their dependency set; other references resolve backward to
applied records. Derived indexes do not become authority.

## Four coordinate domains

These symbols explain semantics; they are not new public type names.

| Coordinate | Meaning | What advances it |
| :--- | :--- | :--- |
| L | Verified full ledger head and event count | Every committed history append |
| D | Effective domain contract, KCS acceptance head, materialization head and accepted graph digest | The corresponding governed KCS or contract transition |
| A | Derived Assent epistemic-acceptance head for protocol proposals | An action-only epistemic ACCEPT |
| O | Immutable original L, D, A, action contract, policies and goal/preservation inputs for one proposal | Never rewritten |

At this baseline, Assent advances A even for an action-only ACCEPT with no
graph application (`assent.py:1632-1735`). The compiler advances its acceptance
head only for admitted KCSs (`knowledge.py:1918`). Existing Assent record
`base_acceptance_head` fields continue to name A, never D. The profile binds O
to each exact action/proposal through retained typed context data. A name
collision does not license identity substitution or hidden rebase.

**New profile choice requiring approval:** initialize A from the content
identity of one explicitly retained, closed action-profile checkpoint over a
verified prefix, its D and exact record/machine/policy identities. It introduces
no knowledge. It is not an EXTERNAL_SNAPSHOT_ANCHORED claim or second history.
Its exact shape and digest recipe must be frozen before RED. This explicitly
changes standalone Assent bootstrap, not the bytes or interpretation of old
ProtocolLedger histories. If not approved, composition remains blocked.

After initialization, action-only ACCEPT updates A with the existing
acceptance_result_head formula using previous A, exact proposal/decision
hashes and an empty claim-revision list. Other protocol transitions leave A
unchanged. O remains available with the original input context.

Every write checks expected L against actual L at the owning single-writer
commit boundary. Proposal recording checks O against its designated current
prefix. Epistemic acceptance checks current A and unchanged original D.
Authority assessment and authorization bind current post-ACCEPT A, exact
action/proposal identities and still-current D. Dispatch binds that
authorization's A and D. Ordinary protocol-only log progress does not stale
the action by itself. Another epistemic ACCEPT may change A and invalidate an
old authorization. A domain KCS or revision may change D and invalidate it.
These are conservative profile guards, not automatic rebasing.

Execution and observation attest what followed an applied dispatch. They do
not require today's D to equal O: domain knowledge may change while an action
is in flight. Exact dispatch/execution, actor, source and time bindings still
apply. The resulting KCS uses fresh L and D after evidence retention.
External pre-state validation occurs in the adopter immediately before its
effect, not inside Core's persistence transaction.

## Selected transitions

1. **Registration.** Type/hash-check actual retained artifacts, grants and
   sources. Grantor matches the recording actor. SourceArtifact byte digest
   and length bind supplied retained bytes, not just a declared locator.
   Preserve artifact_hash versus content_hash semantics.
2. **Proposal.** One ProposedSubgraph contains one concrete first-revision
   ActionProposal, complete member IDs/hashes, exact epistemic/authorization
   policy references, unique global IDs and action-key lineage. No ClaimVersion
   members, action revisions, candidate application or automatic replacement
   in this first profile. Preserve required empty fields under the existing
   record contract. Duplicate root/action key refuses. One exact O association
   is mandatory. The result is PROPOSED/PENDING, not accepted or authorized.
3. **Epistemic assessment and decision.** Require exact monitor coverage,
   identities, inputs, results, ordering and policy mapping. Replay recomputes
   verdict and evaluation hash. ACCEPT atomically introduces EpistemicDecision
   and TransitionRecord, marks the proposal accepted and advances A only.
   No KCS or AcceptedGraphApplication is created; application is None and
   candidate fields retain the precise absent/null form of the existing
   schema. A negative decision is a valid event, not a failed append.
   Requests or claim revisions outside this subset refuse rather than vanish.
4. **Authority.** Require applied ACCEPT, at least one exact required AUTHORITY
   assessment, exact action/actor/policy/evaluated grant and current A/D.
   Preserve existing control: all required SATISFIED yields AUTHORIZE; any
   VIOLATED yields BLOCK; otherwise UNKNOWN yields CLARIFY. Missing outcomes
   do not become SATISFIED. Check grantee/action type, assessed-grant identity
   and authorization interval contained within grant interval. Scope and
   subdelegation declarations remain explicit. Existing Core stores
   scope_record_id/may_subdelegate but does not interpret a domain scope
   hierarchy; identified scope assessment remains adopter-owned. Decision and
   TransitionRecord are atomic. Only AUTHORIZE carries a validity interval.
   No proposal-time policy replacement. This cut refuses active profile or
   policy migration rather than supplying revocation machinery.
5. **Dispatch.** Require applied AUTHORIZE, exact action/decision hashes,
   authorized executor, declared adapter, dispatcher role, current A/D, time
   within validity and no prior dispatch for that action. KG presence is not
   permission. The event records the gate; only the adopter performs an effect.
6. **Execution.** Require applied dispatch ID/hash, matching executor recording
   its own receipt, start no earlier than dispatch, end strictly after start
   under the existing interval rule and equal to generated_at, closed terminal
   status, exact result hash and no previous terminal receipt. Retain result
   bytes if reconstruction of them is claimed. A digest alone is not bytes.
   The record does not assert that external state changed.
7. **Observation.** Require applied execution ID/hash, exact outcome contract
   and observation type, observer distinct from executor, observation time no
   earlier than execution end, exact SourceArtifact ID/record hash, verified
   retained source bytes, closed outcome and one observation per
   execution/contract. SUCCEEDED is not required: failed execution may have
   changed the source. Recording observation does not map source, compose KCS
   or change the KG.

Check producers and their inputs remain separately identified. These rules
validate recorded judgments and recompute control; they do not execute
arbitrary monitors, manufacture SATISFIED or establish judgment truth,
legitimacy, source faithfulness or adequacy for a use.

## Staging, refusal and replay

Decode, validate retained closure, stage all record/index/head transitions and
compute receipts before writing. A protocol-only batch refuses KCS
retention/admission, graph application and contract revision. Verify unchanged
domain graph digest, accepted KCS list and both KCS heads. Commit once through
the owning failure-atomic mechanism. No callback performs an effect during
validation or replay. Single-writer and filesystem failure-atomic scope remain;
no multi-writer, power-loss or exactly-once guarantee is added.

Malformed, unknown, stale, duplicate or unauthorized appends return typed
refusal without appending an audit event in this first cut. Valid REJECT,
BLOCK, CLARIFY and failed execution records do persist. Storage failure is
distinct from validation refusal. After uncertain acknowledgement, reopen
and inspect exact IDs. Do not automatically resubmit or infer success.

Pending is derived from open proposal, accepted-awaiting-authority,
authorized-awaiting-dispatch and dispatched-awaiting-receipt/observation
states. It is not goal satisfaction. Existing uniqueness rules prevent repeated
recording; the first experiment allows one action/dispatch attempt. Read-only
pending assessment requires no append. No queue, scheduler, cancellation or
retry protocol is implied. The adopter separately tracks observation-to-KCS
completion and the goal; Core's terminal receipt is not that goal verdict.

JSONL-only reopen recovers compiled record/domain contracts, exact
machine/profile/policy/binding artifacts, initialization and O contexts, full
protocol records, required source/evidence/result bytes, retained genesis KCS
and later changes. No sidecar, source path, callback or network is consulted.
Replay reproduces L, D, A, records, lifecycle indexes and KG. The identified
runtime remains an installed dependency, not code fetched from ledger data.

## Necessary execution capabilities, not a selected language

Current machine.py supports STRING/DIGEST/epistemic VERDICT fields, one stored
record type per event, eight closed opcodes and an empty capabilities list.
Current PolicyProgram cannot encode AUTHORIZE/BLOCK/CLARIFY. Configuration
alone cannot express this contract.

The bounded declarative execution obligations are:

- Structured contract-derived record validation and canonical record/artifact
  hashing, including existing nested types and missing/null distinctions.
- Trusted enclosing-event and replayed-context operands.
- Typed references and exact field/hash/actor equality or inequality.
- Required/optional fields, closed enums, finite list coverage, unique or
  composite keys and deterministic ordering.
- Timezone-aware ordering and interval containment.
- Deterministic policy precedence/mapping and evaluation-hash derivation.
- Multiple immutable introductions and index/head updates in one staged event.

Reuse existing lookup, absence checks and staging where they suffice. Names,
paths, verdict maps and refusals belong to identified optional artifacts.
An interpreter must not hard-code ActionDispatch or call an opaque Assent
handler while claiming portable execution. No unbounded expression language,
arbitrary Python, executor or observer capability is proposed. The exact
versioned grammar, initialization/context shapes and opcode mappings remain
to be frozen and mechanically checked, not guessed during implementation.

## Discriminating conformance obligations

- Valid protocol-only events advance L and appropriate action state, not D,
  accepted KCS list or domain KG. Action ACCEPT advances A only.
- Wrong original/current coordinate domain, stale A/D, wrong actor/hash/time,
  missing acceptance/assessment, duplicate IDs/dispatch or unknown capability
  refuses atomically. Valid own-lifecycle L movement is not a stale-D failure.
- Replay recomputes control, never trusts caller-selected authorization.
- Execution/observation can be recorded after intervening D movement without
  authorizing another effect. A newly composed KCS still checks fresh L/D.
- Full and reopened replay recover exact action records and accepted graph
  solely from JSONL plus the identified installed interpreter.
- A different interpreter must eventually pass the same retained artifact
  suite before claiming execution replacement or portability demonstrated.

These are proposed test obligations, not tests already passing. The previous
eight seam probes establish the existing refusals only.

## Decisions and prerequisites before RED

Operator approval must explicitly cover:

1. Separate A from D and adopt a fresh retained action-profile initialization
   checkpoint with a frozen shape/digest recipe, not an old-head alias.
2. The action-only, first-revision, no-claims/no-application subset and its
   conservative stale, no-repeat and refusal-persistence rules.
3. A research-local execution/profile experiment with these typed validation
   obligations. Public API/wire names and generic language expansion are not
   selected by this semantic draft.
4. Exact epistemic and authority check producers and inputs supplied by the
   adopter. No fake success or implied policy authority may fill that gap.
5. A second independent consumer before shared generic API/vocabulary promotion,
   or an explicit bounded operator exception. This packet supplies neither.

After those choices, freeze the exact record/profile contracts, context and
initialization grammar, supported instructions and independent expected
results before RED. If a required existing record cannot be expressed, stop
rather than stringify it. Until then, this document is a precise semantic
proposal with explicit residual decisions, not an executable contract or
evidence of the requested full external-action E2E.
