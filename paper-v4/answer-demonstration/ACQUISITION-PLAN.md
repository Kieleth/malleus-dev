# Connect the experiment's existing records

E-0307, master 1.5.28. Luis approved one fresh Sol proposal and one separate
source review. The graph already stores the cruise, instruments, network count
and recording duration, but no relations connect these four records. The count
has an instrument subject; the duration has a campaign subject. Those facts alone
do not establish that the instrument network belongs to this experiment.

One model will inspect the complete article and propose justified connections.
One separate reviewer will inspect every proposed connection against the article
before the whole batch can be accepted. Unsupported or unresolved assertions
withhold the batch. Human ratification remains pending even after model review.

## Fixed scope

Existing endpoints: campaign:smarties (Campaign), instrument:obs (Instrument),
count:obs-network (CountObservation), observation:recording-duration (Observation).
The useful-instrument count is read-only contrasting context, not an endpoint.
Only new ResearchRelation records are permitted. PART_OF_CAMPAIGN runs from
the count or duration to the campaign. OBSERVED_WITH runs from the campaign or
duration to the instrument. These are permitted shapes, not mandated facts.
The source must justify each precise meaning and direction. No edge count target.

No entity edits, supersession, new events, quantities, qualifications, ontology,
catalogue attribution or depth-origin repair. Report required changes outside
this scope. Every accepted old record must remain exactly unchanged.

## Sequence and checks

1. Write failing scope and preservation tests. Reuse public Core admission and
   replay; add no protocol behavior. Missing, swapped or stale review identities
   must prevent acceptance. A valid shape is not a scientific assessment.
2. Freeze the accepted reconciliation-feedback history, current count-query-01
   reader, full reading, ontology/imports, actual graph and six retained captures.
   Supply no questions, query code, answer expectations, prior review or feedback
   to the producer. Record fresh Sol with the existing ultra effort condition
   and verify actual settings plus complete model-visible input delivery.
3. Retain one proposed batch and its explanation. Every new assertion copies a
   complete selected block; its mapped meaning can depend on multiple blocks.
   At most two structural diagnostic returns, each retained separately. No
   semantic retry, fallback, extra sample or evaluator-authored relation.
4. Review every proposed relation and its endpoints against exact source context.
   Retain the full assessment, including inherited limitations. Accept only the
   whole supported batch through the frozen public runtime. Reopen, preserve all
   old records and ledger bytes, and reproduce the new result independently.
5. Run the unchanged thirty-query reader before and after. Separate new graph
   connections from information the reader actually returns. Count and duration
   queries currently do not traverse these new relations; do not quietly change
   them or promise complete answers. Any reader repair is a separate comparison.

Core stays at 160878cf14c0d27b11a440e26688708e9b7a7e2b. Work is paper-local, no
Core edits, shared refs, commits, dependency changes or manuscript edits. This
is not milestone four's new-run progress comparison. Results determine the next
choice. Explain results in plain English; put identifiers and checks in evidence.
