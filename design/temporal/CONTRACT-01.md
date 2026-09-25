# T2: exact historical knowledge-position read

Version 1. This is an implementation contract, not a new persisted wire grammar.

## Responsibility

`KnowledgeChangeHistory.replay_at` returns the existing `KnowledgeHistoryReplay`
at one exact complete ledger prefix. It reconstructs the contract, evidence,
accepted records and explanations available there, not just an old graph viewed
through today's contract. This is the knowledge-position coordinate only.

## Inputs and outputs

Required keyword arguments:

- `ledger_head`, `ledger_event_count`: exact selected historical prefix.
- `expected_head_hash`, `expected_event_count`: exact containing ledger snapshot.

The second pair prevents a valid old prefix from silently concealing a removed
tail. Neither pair authenticates itself; callers retain/select trusted coordinates.
Equal transaction timestamps do not make different ledger positions ambiguous.

Output: the existing replay object and its canonical receipt. Its `ledger_head`
and count identify the selected prefix. Later retained artifacts, revisions,
check contracts and records are unavailable in that result.

## Invariants and refusals

1. Read and validate one containing ledger snapshot. Do not reread between checks.
2. Verify its full expected head and count and the selected head and count.
3. Validate the complete containing history, including its semantic suffix.
4. Reuse the existing semantic fold for the selected prefix.
5. Require complete bootstrap and no incomplete knowledge admission or finite
   action transaction at the selected boundary.
6. Return no graph on a failed check. Write no file, ledger event or cache.
7. Existing `replay`, admission, artifacts and receipts remain unchanged.

Coordinate mismatch: `KnowledgeChangeRefusalReason.STALE_BASE`.
Invalid/incomplete bootstrap: `MALFORMED_HISTORY`.
Incomplete admission: `INCOMPLETE_ADMISSION`.
Existing typed semantic or finite-program refusals remain intact.

Counts are real positive integers, not booleans, floats or coerced text. A
selected count beyond the containing history refuses. Before-bootstrap queries
do not invent a contract or an empty accepted history.

Logical completeness is not a reconstructed filesystem commit boundary. The
envelope records no generic append-batch identifier. Select checkpoints retained
from completed public calls. An arbitrary internally valid prefix is not proof
that precisely that prefix was ever separately persisted. This cut does not add
batch markers or change the wire to manufacture that stronger guarantee.

## Conformance observations

An older result matches the receipt saved when that prefix was current, including
the old source set and contract. Later evidence is inaccessible; a changed later
record cannot appear. Reopen produces the same result. A wrong selected head,
wrong containing head/count, truncated or corrupt suffix, incomplete admission,
incomplete finite transaction and premature bootstrap all refuse without writes.
The current selected position equals ordinary replay. Caller changes to a
returned graph cannot change the next read.

## Boundary and replacement

Role: `REFERENCE_IMPLEMENTATION` of an optional semantic-history read. No new
profile artifact or serialization format is needed for a read of existing bytes.
Dependencies are recorded in `design.ttl`. A different reader would have to
return the same receipts and refusals from these fixtures; no replaceability
claim is made from the one implementation.

No date-based selector, domain-time filtering, correction semantics, automatic
calculation or performance guarantee. This API is not a complete temporal system.
