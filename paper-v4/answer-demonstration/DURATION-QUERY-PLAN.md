# Return the recording's instrument connection

E-0311, master 1.5.29. Luis authorizes the duration-query repair.

The accepted graph already connects the continuous-recording duration observation
to the OBS instrument record. The current recording_duration program returns the
observation and its campaign subject but never reads that relation. Fix retrieval,
not capture. The whole source-reviewed three-link amendment remains unchanged.

## Fixed scope

Preserve the existing duration candidate selection. Follow only outgoing
OBSERVED_WITH relations from those candidates to records of the declared Instrument
type. Preserve exact relation direction, identities, endpoint fields and each
endpoint's own subject. No reverse links, campaign detours, unlinked instruments,
substitute observations, field inference or qualification changes. Broken selected
endpoints must fail visibly. If the relation vocabulary is undeclared, report
NOT_EXPRESSIBLE; if declared but unpopulated, keep the known duration row.

Core remains 160878cf14c0d27b11a440e26688708e9b7a7e2b. Accepted history:
sol-acquisition-01/evidence/attempt-01. Source, ontology, 167 graph records, 176
historical versions, 51 ledger events and all thirty questions stay fixed.
Only CQ-T1-05 may change. The count question still needs explicit deployment
meaning; this work does not infer it from campaign membership.

## Sequence

1. RED tests with synthetic identities, quantities and qualifiers. Prove exact
   preservation, direct/directed instrument retrieval, absence and wrong-direction
   controls, isolation of multiple observations, and loud broken-reference refusal.
2. Change only the duration function. Keep the historical count comparison pinned
   to its recorded reader, with a separate AST guard for each query revision.
3. Reuse the query comparison runner with an explicit duration condition. Verify
   the accepted source-review/run identities and reproduce all current answers
   before running the changed reader. Check every unchanged answer, retained row,
   relation projection, path and witness. Refuse wrong/stale method identities
   before writing outputs.
4. Freeze a sibling duration-query-01 method and execute twice. Verify unchanged
   graph/history/receipt, identical output bytes and exact source-trace closure.
   Describe the newly accessible answer in plain English. Any semantic assessment
   by this coordinator is model-assisted and non-independent, pending Luis's
   ratification. Do not update a full thirty-question score or historical reviews.

No new capture, model/reviewer dispatch, ontology revision, Core edit, dependency
change, manuscript edit, commit, push or shared-ref movement. This is not the
separately planned new-run progress comparison.
