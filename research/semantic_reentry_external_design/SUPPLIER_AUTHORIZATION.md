# Supplier direct-grant authorization

REFERENCE_IMPLEMENTATION under the existing experimental one-action attachment.
Supplier scope, grant, actors and requested interval remain ADOPTER_CHOICE.
Tests are CONFORMANCE_FIXTURE, not real-world authority or supplier execution.

Claim: after actual supplier proposal ACCEPT, retain explicit direct-grant inputs,
capture Core's current context, run the actual DIRECT_GRANT producers and record
the public authorization policy result. The smallest observation is permission
changing only according to those recorded checks while the complete accepted
domain frame remains unchanged. Existing Core records, producer and atomic
append/replay are reused; no new Core type, checker or authorization semantics.

Three research-local coordinator functions have required keyword-only arguments:

1. `prepare_supplier_authority` takes owning history, expected full head/count,
   original-context ID, exact authored AuthorityGrant bytes, scope-association,
   requested-interval and current-context IDs, exact requested-interval bytes,
   recording actor/time and artifact version. It validates all static inputs and
   actual proposal ACCEPT before any write. The scope association records the
   declared EXACT_RECORD_ID_AND_HASH comparison between the grant's retained scope
   and the original context's retained goal. It does not assume they match. The
   grant retains its exact identity and recording actor. Source records use the
   explicitly supplied metadata. It registers the sources and grant through the
   existing transactions, then captures current L/D/A, initialization and policy
   identities using Core's existing current-context schema. It returns Core replay.
2. `record_supplier_authority_check` takes history and expected head/count, original
   and current context IDs, grant/scope-association/requested-interval IDs, intended
   executor ID, monitor ID, assessment/failure IDs and checker actor/time. It builds
   an explicit DIRECT_GRANT invocation from the retained records and source bytes,
   invokes the actual identified Core check producer, and appends that producer's
   completed or unavailable output. The caller supplies no outcome. Prefix movement
   during computation refuses without retaining a stale result or rebasing it.
3. `decide_supplier_authorization` takes the same history/context/grant/association/
   interval/executor bindings, exact assessment IDs, decision/transition IDs and
   authorizer actor/time. It runs the public authorization policy evaluator and
   submits the existing decision/transition pair atomically. AUTHORIZE alone has
   the requested validity interval. BLOCK and CLARIFY retain the existing null
   interval representation. Applied epistemic ACCEPT, required monitor coverage,
   action identity, current A/D and grant/time bindings remain Core's guards.

The output of every coordinator is existing Core replay, not an adapter ledger or
permission token. Required identifiers are nonblank, times aware, source JSON
canonical and shapes closed. Event IDs derive as `event:` plus record ID; paired
transition records share their governing decision's event. Policy/source IDs come
from actual retained contexts, never neutral Core fixture names. Native Core and
producer refusals pass through unchanged; local malformed/stale input has an
explicit SupplierAuthorityError reason. No fallback verdict or retry is provided.

Static preparation checks precede retention. Each Core append remains atomic, but
the complete preparation workflow is not one transaction. Storage interruption may
leave a valid prefix of completed prerequisite registrations. It does not create
permission or authorize resubmission. Assessment computation is outside append and
replay; policy control is recomputed from its actual recorded inputs.

Tests use the real e4-only supplier ingress, actual supplier initialization and
the action-entry adapter's actual TYPE/ACCEPT path. Their action is explicitly
authored, not attributed to a missing synthesizer. Their synthetic grants declare
actor/scope/time choices, not grantor legitimacy. Two monitor IDs invoking one
implementation do not demonstrate independent judgments or replaceability.

Required observations: matching direct grant gives AUTHORIZE; grantee mismatch
gives actual VIOLATED/BLOCK; engine unavailability gives the existing failure/UNKNOWN
pair and CLARIFY; absent ACCEPT, missing inputs, stale head, bad record/byte hashes,
duplicate IDs and substitute owner refuse at their declared boundary. Every step
preserves graph, record history, accepted KCSs and domain heads. JSONL-only reopen
recovers permission and its exact inputs without running a producer. No dispatch,
execution or observation may be inferred from permission.

Dependency edges: accepted supplier proposal and retained original context feed
authority preparation; retained scope/grant/interval and current context feed the
actual DIRECT_GRANT producer; recorded assessments feed public policy evaluation;
Core's existing authorization transaction governs the decision and transition.
Downstream execution consumes that Core record, never a coordinator-owned flag.

Excluded: dispatch, executor/observer identity placeholders, source effects,
synthesis, full Re-entry Contract closure, observation-linked KCS, episode closure,
real authority, shared API/ontology promotion, physical/paid/remote effects and
full supplier E2E claims. Replacement needs a different implementation and is not
proved here. Pre-action checks: no server, endpoint, dependency installation,
production replacement, Core/ontology/locked-fixture/paper edit or new policy choice.
