# Pure supplier Semantic Re-entry

REFERENCE_IMPLEMENTATION of the approved GoalPredicate ADOPTER_CHOICE under the
compiler-enabled state-version and experimental one-action profiles. The local
Re-entry Contract, result and SupplyGapFinding are immutable in-memory values, not
Core records, accepted facts or a second public change identity. The only candidate
is canonical bytes of the existing SupplierOrderAmendment ActionProposal subtype.

Claim: accepted B/Y/1 plus the exact-two goal produces one pinned amendment; a fresh
acted-episode evaluation becomes SATISFIED only after the matching observed KCS was
accepted. The smallest observations are a real ActionProposal accepted by the existing
submission path, no accepted graph change during synthesis, and zero output/retention/
effect after the linked observed correction. All prior stage gates remain required.

## Addressable rule and current contract

Retain one canonical rule as an ordinary SourceArtifact before the initiating goal
SourceArtifact. The goal keeps its existing five-field predicate bytes; its
source_record_ids names the rule. The original Core context O binds that goal and
the verified prefix, making the rule part of the proposal's retained closure. There
is no new Core field, event or contract object. Existing technical fixture record
IDs may be reused in a fresh isolated history; synthesis provenance comes from the
actual implementation and retained context, not from English words in an ID.

The closed rule grammar is `malleus.reentry.supplier-rule/research-v1`. Required fields:

- `initialization_id`, `goal_kind` = GoalPredicate, `output_type` = SupplierOrderAmendment,
  and `logical_source_id`.
- `operator`: the existing complete six-field operator object. It declares the
  exact-byte precondition, 1-to-2 amendment, new occurrence and changed source fields.
- `ambiguity` = REFUSE_IF_NOT_UNIQUE; `candidate_budget` is integer zero or one;
  `dispatch_attempt_budget` = 1; `automatic_retry` = false;
  `stopping` = INITIAL_SATISFIED_OR_LINKED_OBSERVED_KCS.
- `implementations`: synthesizer, model and update_strategy references, each with
  source_id, bytes_sha256 and entrypoint. Each role is explicitly selected, not a
  fallback. Different implementations must satisfy the same contracts; this first
  implementation is not an empirical replacement demonstration.
- `executor`: source_id and bytes_sha256; `observer`: outcome_contract_id and
  observer_implementation_hash; `observed_mapper`: source_id, bytes_sha256 and adapter_id.
- `output`: proposer_id, generated_at and proposal_key. Action/proposal/context IDs
  and the stable episode key come from O; revision one is the selected Core profile.

Implementation source capsules contain exact identified source files as canonical
base64 data. They are ordinary retained evidence, never code loaded by replay. Each
engine also declares its exact entrypoint. The installed Python/Core dependency and
trusted-process assumption remain explicit; source hashes do not attest arbitrary
monkeypatching, actor legitimacy, sandboxing or source truth. The existing observed
mapper's capsule is its exact declared two-file identity preimage, not an invented hash.

`bind_supplier_reentry(*, view, original_context_bytes, rule_source_id)` takes only a
verified graph-free AcceptedReadView and explicit bytes/ID. It returns a local
SupplierReentryContract binding all seven current Core context coordinates, the
unchanged O bytes, exact rule/goal/mapping/preservation/pre-state references and
implementation closure. It performs no retention. The contract has canonical bytes,
an identity and strict parse/serialize round-trip. Unknown or absent required fields
refuse; no missing evidence becomes a default.

Before initial proposal, O must equal the existing original_supplier_context result
for that exact current view. After O is retained, it must equal the applied retained
context and remain associated with the same episode/action. A new evaluation explicitly
binds a new current contract without rewriting O. Evaluation never rebinds a stale
contract automatically, even if its apparent goal is already satisfied.

## Replaceable pure stages

SupplierSourceModel.predict consumes pre-state bytes/digest, goal and operator and
returns predicted canonical source bytes or None. The first implementation calls
the existing pure model_amendment. No world change is inferred from this output.

SupplierActionStrategy.payload consumes pre-state and prediction bytes, their explicit
goal/operator/mapping and logical source. It validates model agreement and the frame
through the existing independent map_observation predicate, then returns the seven
canonical amendment payload fields. It produces no KCS, retention or effect.

SupplierReentrySynthesizer.synthesize takes the bound contract and current accepted
view plus explicitly selected model and update_strategy. Their implementation and
entrypoint identities must match the retained rule before invocation. The synthesizer
receives no graph, owner, path, clock or executor/observer capability. Its standard
implementation produces the existing record with make_record and validates it against
the exact retained compiled action contract. No manually authored candidate substitutes
for this output in the full proof.

The immutable local result has status, reason, contract identity, optional finding,
candidate tuple and optional model prediction. Status is CANDIDATES, SATISFIED, PENDING
or REFUSED. Only CANDIDATES contains one candidate. Same exact inputs return identical
canonical output. Repeated pure evaluation is not a new accepted candidate or dispatch.

SupplyGapFinding reports the unique current target quantity, required quantity and
max(required-current, 0). Equality to two remains the goal: quantity three has no
shortfall but is not satisfied. Missing or competing targets refuse, never become zero
or a selection by enumeration order. Findings remain contract-local derived values.

## Evaluation and stopping

Validate grammar, implementations, all current coordinates and source/record closure
before goal shortcuts. Require unique eligible target and accepted lineage. A fresh
unacted goal already at two returns SATISFIED with no model call or candidate.
A fresh unsatisfied target requires quantity one, the declared sole operator and a
remaining candidate budget. Otherwise return UNREALIZABLE or BUDGET_EXHAUSTED.
Unsupported operations or ambiguity behavior return explicit refusal.

Use the stable action key to reconcile existing work. Partial context/proposal/check/
authorization/dispatch/receipt progress returns PENDING, not another candidate.
Terminal rejection or unsupported/contradictory terminal observation cannot restore
the attempt budget. Missing observation or missing admitted correction remains pending.
A successful receipt never proves the goal; a failed receipt remains failed.

For acted satisfaction, locate the current target's accepted KCS through the view's
accepted change sets and record history. Verify its ordinary population plan and exact
binding evidence against O, the selected mapper, the applied observation, selected
outcome contract and captured source bytes. Retained-only candidates, unrelated
quantity-two facts, model output and receipt bytes cannot close the episode.
Only linked observed admission plus the equality goal returns SATISFIED. A supporting
observation may close the goal after FAILED without rewriting failure or asserting cause.

Conformance: canonical contract/value round-trip; pure deterministic candidate and
independent model/frame agreement; real subtype/submission; complete accepted-state
preservation; missing/unsupported/operator/ambiguity/budget/implementation refusal;
stale-before-satisfied refusal; pending without reissue; initially satisfied no-op;
real observed admission followed by fresh quiescence; failed-after-write closure;
and unrelated/retained-only corrections cannot falsely close the acted episode.

This is GoalPredicate synthesis, not ViewDelta putback, reverse replay or decoding.
No external ActionProposal establishes PutGet about the world. Existing source mapping
and replay proofs provide their separate evidence. No public contract promotion,
second interpreter, retries, concurrency, external calls, paper edits or publication.
