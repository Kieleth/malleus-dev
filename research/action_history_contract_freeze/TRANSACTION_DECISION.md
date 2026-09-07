# Context and proposal: one transaction

Status: ACCEPTED design decision, 2026-09-07. Not implemented runtime behavior.

Luis approved the recommendation "together, both succeed or neither does"
with: "yes, transactional for the moment".

This selects the transaction choice left open in `DEFINITION.md` and
`DEFINITION_REPORT.md` at `ae434b5`. Those frozen files remain historical
definition evidence. For this question, this decision supersedes their
unselected status. It does not approve the remaining instruction vocabulary,
complete event programs, check producers or runtime activation.

## Bounded claim before construction

Role: OPTIONAL_PROFILE. This applies to the proposed one-history action
profile, not to every Malleus adopter or the default structural bundle.
The research-local CONFORMANCE_FIXTURE checks the definition, not persistence.

Claim: original-context registration and proposal recording form one ordered,
failure-atomic transaction. The exact pair succeeds together or neither is
retained. Separate commits are not a supported variant of this cut.

Smallest observation: the machine-readable definition accepts that pair and
refuses either half, reversal, an intervening event, separate commit boundaries
or a rule that publishes a partially validated batch.

Reuse: the frozen original-context shape, existing explicit full-prefix
head/count, stage-before-commit discipline and failure-atomic history owner.
The definition uses the already-declared JSON Schema validator. No executor,
new storage mechanism or public wire is introduced.

Exclusions: actual persistence proof, monitor execution, effects, retries,
cancellation, orphan recovery, multi-writer safety, new public API, migration,
compiler changes, shared main, paper, packaging, merge and push.

## Selected meaning

Retain prerequisite artifacts before constructing the original context. That
context pins the verified full prefix immediately before this transaction,
plus the current domain and action-acceptance coordinates.

Within the transaction, stage context registration first and proposal recording
second. These are two ordered logical events, not one collapsed lifecycle
event. The second event may resolve the context from the first staged event.
There is no intermediate committed prefix. No unrelated event may occur
between them. The event names and full event wrappers remain part of the
successor program definition; the role names in this fixture are not opcodes.

Validate the complete batch, references, records, current prefix and unchanged
original domain/action context before the owning commit publishes anything.
Check expected head and count against actual history at that boundary. A
validation refusal retains neither event, no new context bytes, no introduced
record and no derived index update. Previously retained prerequisites remain.
No refusal audit event is added in this first cut.

Success publishes both events and their introduced records/index updates in
one commit. The proposal is only PROPOSED, not accepted or authorized. Both
domain state and action-acceptance head remain unchanged by this transaction.
The committed full ledger advances through both event hashes.

Same-directory failure-atomic persistence is the intended implementation reuse,
not a new claim of power-loss durability or multi-writer safety. An uncertain
acknowledgement requires reopen and inspection of exact IDs, not an automatic
retry. Those runtime checks remain unexecuted here.

## Next dependency and evidence boundary

`proposal-transaction.schema.json` fixes the approved transaction obligations;
`proposal-transaction.json` is its explicit instance. Their tests validate
definition data and reject incompatible edits. They do not append, authorize,
dispatch, simulate a successful action or prove file rollback.

Next, complete event programs and the static/content/check-producer contracts
against this rule. Runtime conformance must independently exercise success,
invalid second event, stale head/count, duplicate IDs, interrupted persistence
and reopen. A passing definition test cannot satisfy any of those obligations.

ProposalTransaction governedBy OneHistoryActionProfile
ProposalTransaction consumes VerifiedOriginalContext
ProposalTransaction consumes TypedProposalAndAction
ProposalTransaction requires OneFailureAtomicCommit
DefinitionFixture conformsTo ApprovedTransactionDecision
FutureActionRuntime conformsTo TransactionPersistenceTests
