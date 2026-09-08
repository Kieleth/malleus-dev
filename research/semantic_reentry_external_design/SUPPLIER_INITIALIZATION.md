# Supplier protocol initialization

Classification: REFERENCE_IMPLEMENTATION of the already selected experimental
one-action profile. Caller identities and epistemic control are ADOPTER_CHOICE;
the tests are CONFORMANCE_FIXTURE. Without that profile this initializer makes
no action-history claim. It adds no public protocol object or Core semantics.

Claim: from the actual e4-only accepted supplier state and RET-010 complement,
register the exact supplier program, real check producer, four monitors, two
policies and the existing Core initialization checkpoint in the owning history.
The smallest observation is unchanged domain contract, KCS heads, accepted KCSs,
graph and record history after every append, while the full ledger advances and
the action head becomes the checkpoint's content identity.

`initialize_supplier_protocol` requires the actual public KnowledgeChangeHistory,
expected full head/count, exact canonical supplier program bytes, program record
and selection event IDs, initialization ID, actual CheckExecutor, its definition
and implementation source IDs, two sorted monitor IDs per policy, ruleset ID,
canonical epistemic-control bytes, actor, timezone-aware time and artifact version.
All arguments are required. Definition-source and policy IDs come from the program's
existing initialization declaration. No fixture IDs or missing metadata default.

Epistemic-control bytes have the closed local schema
`malleus.reentry.supplier.epistemic-control/research-v1` and the three required
arrays `violation_verdicts`, `unknown_verdicts`, `control_precedence`. They are
retained as the actual ruleset artifact; policy fields derive from those bytes.
Core's existing digest functions validate their meaning. This is authored policy
data, not executable producer code or evidence of policy legitimacy. Authorization
control stays the existing Core v1 mapping, not a second supplied interpretation.

The initializer validates its complete static input closure before retention.
It only accepts the exact supplier program produced by the reviewed builder from
its embedded compiled contract and declared role IDs. It refuses a substitute
writer/checker, malformed or unknown input, stale initial position, duplicate or
already retained IDs, and any previously selected program. It never repairs,
retries, replaces a selection or silently rebases the starting position.
Local refusals use SupplierInitializationError with an explicit reason. Core
append/refusal errors remain Core errors and are not converted into success.

Source and policy semantic hashes are computed before record construction using
the existing public source, monitor and policy functions. No placeholder hash,
test helper, caller-selected assessment outcome or copied interpreter is used.
Two monitor invocations per kind do not establish implementation independence.
Registering the real producer does not run it or manufacture any assessment.

Side effects: retain one program anchor, select it once, append nine prerequisite
records, four selected-definition SourceArtifacts and one initialization
SourceArtifact. Every protocol transaction uses the owning expected-head/count
gate. The first evidence anchor uses Core's existing single-writer API, which has
no expected-head argument. This coordinator is not a multi-writer transaction.
Individual appends are failure-atomic; the whole multi-append workflow is not.
After an I/O error the committed prefix remains inspectable. No automatic retry
or rollback is claimed. Invocation performs no source-file effect or network call.

Output is the existing Core KnowledgeHistoryReplay, not a new public checkpoint.
JSONL-only reopen must reproduce it without consulting fixture, oracle, check
producer, source or program files. Exact implementation identity and executed
results are recorded separately. A second implementation consuming these inputs
and passing the same suite is required before claiming empirical replacement.

Dependencies: initializer consumes supplier program and actual check artifacts;
initializer produces existing SourceArtifact, ProtocolArtifact, monitor and policy
records; existing initialization program governs the checkpoint; owning Core
history admits records; replay derives domain and protocol state. Tests establish
the edges, not schema compatibility alone.

Excluded: proposal synthesis, goal-contract binding, assessments, epistemic action
acceptance, grants, authorization, dispatch, execution, observation, a supplier
correction KCS, direct graph writes, historical e7, paid/external calls, Core edits,
shared vocabulary promotion, a packaged API and a full supplier E2E claim.

Pre-action checks: no server or endpoint, no new dependency/install, no production
mechanism replacement or incident. Required inputs are explicit. The approved
one-episode semantics and frozen source fixture stay unchanged. RED precedes code.
