# Event programs: obligation map and instruction gap

Status: REVIEW_REQUIRED. This covers every selected lifecycle stage, but is
not a complete executable program. The authorization program has an exact
unexpressible check under the preceding ten-instruction grammar. See
`missing-membership.json` and `NEXT_DECISION.md`. No unknown operation is
implemented here. Completing this map does not close the execution gate.

The accepted context/proposal transaction is fixed by `4cf8efe`. All stages
below are protocol-only, in the same history as KCS admission. They may advance
L and the specified action state, never the domain graph, domain contract,
accepted KCS list, KCS acceptance head or materialization head (collectively D).
Only action-only epistemic ACCEPT advances A. No action stage is a KCS.

## Shared input and introduction contracts

Event-envelope fields come from the owning history: event ID, transaction time,
actor ID, sequence, previous event hash and event hash. Caller expectations bind
the full head and count; they do not construct trusted replay state. Each event
body has an exact selected role and a finite list of existing full record
wrappers `{record_type, record}`. Raw artifact/source bytes are separate typed
retention inputs, not JSON hidden in a record's STRING field.

`VALIDATE_RECORD` must consume the whole record and exact compiled record
contract. `record_type` chooses a concrete Assent type or a permitted concrete
ActionProposal subtype. No field is removed because the program never reads it.
Source records, retained-context anchors and protocol records share the global
ID namespace. Their identity categories stay distinct.

Each introduction checks these explicit bindings before `INTRODUCE_RECORDS`:

| Record field | Required binding |
| :--- | :--- |
| id | explicit nonempty input ID, globally unused |
| generation_event_id | enclosing event ID |
| generated_at | enclosing transaction time, explicit zoned instant |
| responsible_actor_id | enclosing actor ID |
| responsible_role | explicit permitted role for this event variant |
| content_hash | HASH RECORD over exact type and fields except content_hash |
| source_record_ids | unique IDs resolving to prior or explicitly earlier staged introductions, including the dependencies required by this record role |

The enclosing event hash uses the ledger recipe, not HASH RECORD. Raw bytes use
their exact byte digest and declared length. Artifact semantic hashes use the
identified artifact contract's projection; raw-byte, semantic-artifact and
record hashes cannot substitute for one another. Initialization/O/current/scope
content identities hash their complete canonical JSON values with no excluded
self-hash field.

Static specimen inputs are closed JSON Schemas, not actual records or replay
objects. A whole value is wrapped under `value`, a record under `record` when
that path is declared. Every traversed field must be required. Arrays use
zero-based indices that are guaranteed by minItems. Optional fields require a
separate explicit program variant; there is no missing/null coercion. Unknown
schema variants refuse static checking rather than being guessed.

## Full lifecycle requirement and test matrix

The instruction names below identify obligations of the proposed operations.
This is not alternate executable syntax. Each row's runtime tests are
UNEXECUTED, not skipped tests and not part of the passing static-test count.

| Stage and explicit input | Ordered obligations and resulting protocol state | Required runtime observations, all UNEXECUTED |
| :--- | :--- | :--- |
| Initialization: retained checkpoint, full prefix, D, exact profile/record contract/machine/binding/policies | Verify checkpoint contents against actual replay; HASH VALUE checkpoint; REQUIRE_UNIQUE initialization; retain checkpoint; SET_PROTOCOL_STATE initialization and A to checkpoint identity. L advances, D unchanged. | Valid nonempty-history initialization; second initialization refusal; wrong L, D, policy or implementation binding refuses without append. |
| Prerequisite registration: full artifact/grant/source wrapper plus supplied bytes | VALIDATE_RECORD; HASH RECORD and selected artifact/byte recipe; RESOLVE_RECORD dependencies; REQUIRE_UNIQUE global ID; grant grantor equals recording actor; source declared byte identity/length equal supplied bytes; INTRODUCE_RECORDS. | Corrupt bytes, wrong grantor, missing dependency, duplicate ID and wrong hash category refuse. No context or proposal is implied. |
| Original-context registration: O over actual L/D/A, proposal/action IDs, episode and prerequisite references | Compare every O L/D/A/policy/initialization coordinate with current replay; HASH VALUE O; stage retention. This is only the first half of the approved atomic pair. No independently committed state. | Wrong prefix or missing retained O input refuses; invalid second event preserves exact prior bytes and indexes. |
| Proposal: full ProposedSubgraph and one first-revision concrete ActionProposal, exact O association | Validate full records; resolve pinned policies; compare proposal/action IDs and key to O; verify record/member hashes, first revision and closed member categories; check unused IDs/action key; introduce dependencies before dependents; stage proposal PROPOSED, action PENDING, action-to-proposal/key/context indexes. Commit both logical events once. A and D unchanged. | Both events retained together; wrong member, stale O, duplicate root key, extra/unrelated event or missing half refuses. A proposal is not ACCEPT or AUTHORIZE. |
| Epistemic assessment: complete TypeAssessment, or MonitorFailure plus UnavailableAssessment | Resolve applied proposal and selected TYPE monitor; check complete record/provenance/input/monitor bindings and current A/original D; verify completed or paired unavailable variant; require uniqueness per proposal/monitor; introduce exact output(s). | Missing/wrong producer output, replayed record hash, proposal, source ID or monitor version refuses. A real unavailability pair is retained atomically, not converted into SATISFIED. |
| Epistemic decision: exact policy, complete ordered outputs, EpistemicDecision, TransitionRecord | REQUIRE_COVERAGE; SELECT_CONTROL recomputes policy verdict/evaluation/trigger order; compare every decision field; validate transition subject/from/to/trigger/event/sequence/time. ACCEPT introduces both and hashes the existing acceptance_result_head preimage with previous A, proposal/decision hashes and empty revisions. Other verdicts leave A. No application/KCS. | All satisfied, rejected and unavailable variants; missing output refuses; forged verdict/evaluation refuses; ACCEPT changes A only; stale A or original D refuses. |
| Authority assessment: applied ACCEPT, action/proposal, executor, exact grant/policy/scope/interval/O/current context and output | Resolve applied ACCEPT and current A/D; validate real DIRECT_GRANT output with exact action/actor/policy/evaluated grant and monitor; require uniqueness per action/actor/A/monitor/grant; introduce AuthorityAssessment or atomic failure/unavailable pair. | Wrong actor, policy, grant, input closure or stale context refuses; unavailable is UNKNOWN, not omitted. |
| Authorization: applied ACCEPT, policy-ordered authority outputs, AuthorizationDecision, TransitionRecord | REQUIRE_COVERAGE; SELECT_CONTROL computes AUTHORIZE/BLOCK/CLARIFY. For AUTHORIZE compare grantee/executor, require exact action-type membership in grant list (MISSING INSTRUCTION), REQUIRE_INTERVAL authorization within grant, compare assessed grant and exact current A/D. Introduce decision and transition atomically, update action authorization index only. | Accepted knowledge without permission cannot authorize; false supplied verdict refuses; insufficient grant yields retained BLOCK under a real assessment; missing assessments refuse. |
| Dispatch: exact AUTHORIZE, action, declared adapter and executor, ActionDispatch | Resolve action/authorization hashes and current authorization A/D; compare executor and dispatcher role; valid_from <= dispatch time; dispatch time < valid_to when bounded; REQUIRE_UNIQUE action dispatch; introduce dispatch and index. Never invoke adapter in commit. | Wrong executor, stale context, expired interval, absent permission or duplicate dispatch refuses before eligibility. |
| Execution: applied dispatch and exact ActionExecution/result bytes | Resolve dispatch; executor records own receipt; dispatch time <= start < end; end equals generated_at; closed terminal status; verify result byte digest when retaining result bytes; require no terminal receipt for dispatch; introduce receipt/index. | Wrong dispatch/executor/time/hash or duplicate terminal receipt refuses. FAILED and ABORTED may be valid records; no world-state claim. Intervening D change is allowed. |
| Observation: applied execution, exact outcome contract, independently supplied source and OutcomeObservation | Resolve execution and outcome-contract hashes; observer differs from executor; execution end <= observation time; source ID/record hash and retained bytes verified; closed observation type/result; uniqueness by execution/outcome-contract; introduce observation/index. | A receipt alone cannot supply observation; same observer/executor, wrong source/hash/time/contract or duplicate observation refuses. FAILED execution may still have a valid observation. D change is allowed; D is not written. |

Own lifecycle events advance L without automatically staling D. The following
source-to-KCS operation is outside these programs and uses fresh L/D after
observed evidence retention. Goal satisfaction is an adopter judgment over that
accepted knowledge, not an execution status or Core authorization state.

## Empty, absent and null

Preserve the existing canonical full record shape, not a shape reconstructed by
dropping unused fields. First-revision revises fields must not name a
predecessor. Existing absent and explicit-null representations remain distinct
bytes and hashes; do not normalize one into the other. The
action-only variant carries empty claim/revision/request lists where the
existing protocol parser requires those fields. Candidate fields may be absent
or null but must not name an application; retain the exact selected bytes.
The decision event's application is explicitly None where required.
Non-authorizing validity fields retain the existing required null form, not
fabricated dates. BLOCK may cite the exact insufficient grant assessed;
an uncited grant uses the required null fields. Any such finite variant must be
declared before it enters static checking; the checker does not evaluate a
general conditional or collapse null and absence.

For the new interval content, only an absent end means unbounded. Explicit null
is malformed. Both finite ends are timezone-aware and end > start. Scope content
selects equality of exact record ID and record hash, not a hierarchy. Unequal
well-formed scope values are inputs to a VIOLATED check, not malformed content.
Current-context shape validation does not establish that its coordinates come
from a real replay. The owning runtime must independently derive and compare
them; arbitrary digest-shaped values never authenticate a state.

## State targets, dependencies and refusal

Every named index resolves through the profile's explicit target declaration.
Its storage path is exactly `protocol/<declared-name>`; the only other mutable
root is the separate action-acceptance head. No alias can address D. Intended
indexes cover initialization, immutable O/proposal association, proposal state,
global introductions, latest action key, action/proposal association, monitor
output uniqueness, authorization state, dispatch, execution and observation.
They are replay products, never another ledger or external state.

Static introduction names are symbolic program positions, not runtime IDs.
They must be unique and depend only on earlier named introductions. Actual
source_record_ids and object IDs still need the full runtime checks above.
The schema/type catalogs supplied to static validation are part of the reviewed
definition, not authenticated assertions about runtime objects. Concrete record
schemas ultimately come from the retained compiled contract, never a caller
casting a domain head or arbitrary object into another type.

The static validator never runs HASH, SELECT_CONTROL or INTRODUCE_RECORDS.
It checks declared types and references, not their runtime values/effects.
No successful result can authorize an action. Runtime validation refusal must
leave exact previous ledger bytes, A, D and protocol indexes unchanged; valid
negative decisions are persisted judgments. No failure audit append is implied.

## Required successor

Resolve the exact membership operation proposal, then complete the executable
JSON programs and test their full cross-record requirements. This packet has a
complete lifecycle obligation census, not evidence that the ten candidate
instructions suffice. Real check producers and interpreter implementations are
still UNBOUND. No initialization instance or action lifecycle has run.
