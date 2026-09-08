# Supplier proposal and epistemic acceptance

REFERENCE_IMPLEMENTATION under the existing experimental one-action attachment.
Tests are CONFORMANCE_FIXTURE. Caller goal, payload, identities and policies remain
ADOPTER_CHOICE. Without the selected profile, this adapter makes no lifecycle claim.

Claim: construct Core's existing immutable original-context value from a verified
graph-free read, submit an already authored SupplierOrderAmendment and its existing
ProposedSubgraph atomically, invoke the actual TYPE producers, and record the actual
epistemic policy result. Only the full ledger and appropriate action state advance.
The smallest observation is the complete accepted KG/history/KCS/domain-head frame
remaining unchanged through proposal, assessments and the action-only decision.

This is an action-entry adapter, not a synthesizer. The tests supply a clearly
authored candidate against actual e4-only accepted state and retained goal, mapping,
preservation and source bytes. They do not substitute a fake synthesizer. An original
context alone is not the complete Semantic Re-entry Contract: that later contract
also needs the identified synthesis/model/executor/observer and stopping closure.
No absent implementation is assigned a placeholder identity here.

The module has four bounded functions:

1. `original_supplier_context` consumes AcceptedReadView and explicit initialization,
   four source-role, context, proposal, action and episode IDs. It returns canonical
   bytes in Core's existing original-context schema without retaining anything.
   It verifies actual retained typed source records, hashes and initialization/policy
   references. It does not inspect a mutable graph, choose a goal, or require output
   IDs to be unused merely to construct an in-memory reevaluation context.
2. `submit_supplier_proposal` consumes the actual owning history, expected L, exact
   original-context and ActionProposal bytes, proposal key, context recording actor
   and artifact version. It preserves the supplied action's record identity, checks
   the seven-field payload hash, constructs the existing ProposedSubgraph and context
   SourceArtifact, and calls the existing atomic context/proposal transaction. It
   does not manufacture a KCS, grant, check outcome or action acceptance.
3. `record_supplier_type_check` consumes actual history, expected L, proposal/context,
   monitor, assessment/failure IDs and checker metadata. It constructs an explicit
   TYPE invocation from the retained proposal/action/contract/monitor, runs the real
   Core producer, and appends its full completed or unavailable output. A change of
   prefix during computation refuses, never silently rebases the result. The caller
   cannot supply an assessment outcome. Missing input or duplicate output refuses.
4. `decide_supplier_proposal` consumes actual history, expected L, proposal/context,
   exact assessment IDs, decision/transition IDs and controller metadata. It calls
   the public epistemic policy evaluator and constructs the existing decision and
   transition in one Core transaction. ACCEPT, REJECT, DEFER and CONTEST remain actual
   policy results. No caller-selected verdict or non-executed success is accepted.

All public arguments are required. Canonical bytes, nonblank IDs, aware times and
closed role maps are required. Event IDs derive as `event:` plus their record ID;
action and proposal share the action's supplied generation event. Context recording
uses the supplied context actor and action time. Records preserve the existing
record-hash, byte-digest and artifact-hash distinctions. Source/policy role IDs derive
from the retained initialization, not neutral Core fixture defaults.

Local malformed/unsupported/stale input uses SupplierProtocolError with an explicit
reason. Core's typed atomic refusals propagate unchanged. Constructors are pure;
the three writer/coordinator functions use only the actual Core owner. A TYPE engine
failure produces the real MonitorFailure/unavailable pair, never a canned outcome.
No producer is called during append or replay. Each transaction is atomic, but the
whole multi-stage sequence is not. There is no implicit retry or verdict fallback.

Dependency edges: context constructor consumes accepted read and retained source
closure; submitter consumes existing ActionProposal and original context; Core
admits their atomic pair; actual check producer consumes retained inputs and returns
existing assessments; public policy evaluation governs the decision; Core replay
derives action state while preserving domain state. Downstream users consume Core
records/replay, not another public identity or an adapter-owned ledger.

Required tests cover canonical pure context construction, actual proposal and TYPE
acceptance, stale original or current prefix, payload/record/source mismatches,
unsupported action type, missing inputs, substitute owner, real engine unavailability,
no producer during replay, and JSONL-only reconstruction. Actual TYPE conformance is
not evidence that an action achieves the goal. Replacement remains unproved until
a deliberately different implementation passes the same boundary suite.

Excluded: pure synthesis, full Re-entry Contract closure, authority, dispatch,
execution, observation, source-to-correction KCS, final quiescence, direct graph
writes, second ledgers, Core or ontology edits, paid/remote effects and full E2E claims.
Pre-action checks: no server/endpoint, installation, dependency, production replacement
or incident. The existing approved one-episode policy and locked fixtures stay intact.
