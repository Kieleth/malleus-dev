# Close answer gaps without losing accepted knowledge

E-0303, master 1.5.26. Luis requests TDD preparation after the complete current
review. This document proposes the repair sequence. It authorizes no new model
run, query change, population amendment, ontology revision or Core rebind.
The first recommended implementation is the count-only retrieval cut below.

E-0304 forward decision: Luis approves that first cut and adds a fourth milestone,
another run comparing progress. Execute count retrieval now; retain the other
repairs as separately bounded steps. The new-run comparison below must not be
confused with repeatedly reading the same accepted history.

E-0306 forward result: the count-only comparison is retained twice with identical
outputs. CQ-T1-02/CQ-C-04 now return the network count and instrument; deployment
context remains absent. All other answers and accepted graph/history stay fixed.
The new read view is count-query-01/first; the old depth-method-01 remains frozen.
See [count results](COUNT-QUERY-RESULTS.md). No later capture step is dispatched.

E-0307 forward decision: Luis authorizes one fresh Sol experiment-context proposal
and one separate source review. The precise scope is now frozen in
[experiment-context plan](ACQUISITION-PLAN.md): new relations among four existing
records, no replacements, ontology changes or reader changes. The catalogue and
depth-origin questions remain outside this amendment. The current count-query-01
reader and accepted reconciliation-feedback history are its comparison baseline.

E-0313 forward decision: acquisition links and the separate duration query repair
are complete at E-0310/E-0312. Luis now approves preparation of milestone four,
the fresh-run comparison, without launch. The proposed own-ontology condition,
reference distinctions and reader-compatibility checks are in
[fresh comparison plan](FRESH-COMPARISON-PLAN.md). Deployment meaning remains
partial and does not block preparation. Historical sections below are unchanged.

## Fixed baseline and success rule

Use sol-reconciliation-feedback-01, Core
160878cf14c0d27b11a440e26688708e9b7a7e2b and depth-method-01. The accepted graph
has 164 records, 173 historical versions and 45 ledger events. Exact inputs and
current answers are bound by the
[snapshot manifest](../../private/paper-v4-answer-demonstration/current-thirty-review-01/manifest.json).
The [complete review](CURRENT-SNAPSHOT-RESULTS.md) remains a separate, unchanged
assessment: five covered, twelve partial and eight none among 25 positive
questions. Human ratification is pending.

Fix a demonstrated loss at one stage, preserve everything outside the declared
change, then inspect the result. A passing test proves its mechanical assertion,
not that a proposed scientific interpretation is true. Query retrieval, source
faithfulness and complete answer coverage stay separate. Do not relax the fixed
questions, award coverage in tests, or add facts just to increase totals.

## Gap inventory

Every currently incomplete positive question is assigned below. A missing answer
does not establish missing graph content. Entries after the first are follow-up
investigations, not ready-made replacement facts or commitments to run them all.

| Group | Questions | Located limitation and next bounded check |
| --- | --- | --- |
| Instrument count | CQ-T1-02 | Whole-network count exists but is filtered out. Distinguish it from useful-instrument and detection-threshold counts before widening retrieval. |
| Catalogue | CQ-T1-04 | Repository and DOI exist, but dataset role and deposition connection are absent from this record. Separate candidate retrieval from role completion. |
| Acquisition and origin | CQ-T1-01, CQ-T1-05, CQ-T3-01 | Campaign, duration and depth exist; observing-system links and study attribution are not returned. Trace the existing records before proposing one connected context repair. |
| Quantitative context | CQ-T2-04, CQ-T3-04, CQ-T3-05 | Missing study/flank/age, final catalogue/derivation, and shared melt conditions. Assess each quantity's own context across the source. |
| Spatial and comparative context | CQ-T2-01, CQ-T2-03, CQ-T5-02, CQ-T5-03 | Missing placements or comparisons. Separate existing endpoints from absent relationships; do not infer a relation from two nearby numbers. |
| Method and category structure | CQ-T2-02, CQ-T5-04 | Requested method-order predicates are undeclared; category/selection content is unreturned. Check faithful existing prose routes before proposing schema additions. |
| Qualifications and counterarguments | CQ-T4-02, CQ-T4-03, CQ-T4-04, CQ-T4-05, CQ-T5-05 | Missing grounds, assumptions, limited absence, hedges or counterevidence. Scope and modality must survive capture and querying. |
| Funding | CQ-T2-05 | FundingRelation is declared, but attribution is not populated. Keep as a separate, lower-priority capture slice. |

Keep the five covered questions as preservation controls. Keep the three
expected-absence controls separate; do not populate missing concentrations,
recurrence or excluded figure/table values. The count paraphrase CQ-C-04 must
continue to share its program with CQ-T1-02, not become an extra independent gain.

## First cut: retrieve the network count, preserve its scope

Observed facts: count:obs-network stores an integer count, instrument subject
and network-membership wording. count:useful-obs stores a different integer for
the useful subset, with the same instrument subject. No relation connects either
to the campaign. Both source scopes are explicit in page:2:block:002 and
page:6:block:002. The current instrument_count program requires deployed or
deployment wording and misses the network record. Its existing tests correctly
reject the minimum number of instruments needed to detect an event.

The proposed selector admits explicit deployment counts or explicit whole-network
membership counts as candidates. An instrument mention, a subject reference or
the word network alone is insufficient. Useful/recovered/operational subsets
and per-event detection thresholds must remain distinct and excluded from this
query. The selector must not manufacture a deployment event or relabel a network
count as deployed. Freeze the exact bounded wording rule in the RED tests before
implementation. If it cannot distinguish these cases without inventing context,
record that limit and return the choice to Luis, rather than broadening further.

### Milestone 1: RED, then the minimum reader change

Add focused tests, proposed in test_count_query.py, using synthetic numbers and
identities rather than the article's values:

1. A scoped whole-network count is returned unchanged even without deployed
   wording; its existing one-hop instrument subject is preserved. This must fail
   on the current reader for the demonstrated reason, not an import/setup error.
2. Different useful/recovered/operational and minimum-detection counts are not
   substituted, including when their wording mentions the same network. Keep the
   existing deployed-count, zero-count and subjectless-count positive controls.
3. Counts are read from explicit numeric count fields. No Boolean/string value,
   number in prose, identifier or locator can supply a count. No neighboring
   record supplies a missing subject or scope; a broken explicit reference fails
   visibly rather than being interpreted as an empty answer.
4. Renaming IDs and changing synthetic count values must not change selection.
   Missing deployment fields remain absent. No new path or graph property is
   created, and existing projections retain every field.
5. Only CQ-T1-02 and its paraphrase CQ-C-04 may change. Reject changed unrelated
   answers, altered projected values, invented paths and incomplete trace closure.

Record the actual RED failures, then replace only instrument_count's selection
rule and explanatory note. Do not widen global text matching, alter subject
traversal or modify the other query programs. Historical frozen readers remain
evidence, never a fallback when the new reader refuses.

### Milestone 2: replay, compare, then assess

Reproduce all thirty old query objects on the exact accepted current history
before executing the new reader. Reuse repair.preflight, frozen_queries, the
read guard and the existing comparison/trace checks. The older relation_query
entry point accepts different experiment schemas; do not pass the current run
through a historical condition or silently choose an old baseline. Add a direct
guard for the current condition before adapting the comparison entry point.

Freeze the new reader in a sibling method directory. Query only the replayed
graph, with source/network access blocked during answer execution. Verify all
28 unrelated query objects exactly, including the complete SUPPORTS argument,
then verify affected rows against stored properties and trace their evidence.
Graph, ledger and replay receipt must remain byte-identical. A second execution
must reproduce the output bytes. Run focused tests, then the existing full paper
harness under the verified pinned Core runtime and configured dependencies.

Report candidate recovery first. Assess the two changed answers under the same
frozen requirements, disclosing model-assisted authorship and pending human
ratification. No automatic promotion to COVERED: deployment context may remain
missing. If a fresh independent reviewer is needed, obtain explicit dispatch
authorization. Evaluate this cut with Luis before another repair.

## Subsequent cuts, proposed order

**Catalogue context, not every DOI.** DataResource denotes either data drawn from
or deposited in a resource. The graph contains four such resources, including an
input database, raw-data/cruise material, supplementary information and the sparse
repository record. Type plus identifier does not distinguish their roles. A
query candidate may expose the missing qualification, but must not imply that
all four are the requested catalogue. First specify source-backed dataset and
deposition context. The source statement crosses page:8:block:008 and
page:8:block:009; it must be read together, not split into unrelated assertions.

**One context-repair pilot.** Recommend acquisition/study origin next because
campaign, instrument, duration, catalogue and earthquake observation concern a
connected source account. Before dispatch, freeze exact target records, permissible
new links or fields, incident-relation closure and the unchanged reader. Use one
model-produced proposal with complete source context and actual graph fields,
not evaluator-authored population. A source block is an evidence address, not a
unit of meaning. Existing attribution must not be inferred from equal numbers,
shared labels or the article's mere presence in the graph.

**Comparison and qualifications.** After the context pilot, select one comparative
or argumentative slice. Preserve observations, calculations and hypotheses as
different assertions. ADJACENT_TO alone does not express southward direction;
two values do not encode comparison; no observations to date does not mean
nonexistence. Typed links or faithful stored prose must express the missing
meaning explicitly. An ontology extension needs its own decision and tests,
not a quiet change to an enum or overloaded existing predicate.

For each population cut, write preservation, supersession, exact source/capture
binding and review-bound admission tests first. Test that stale approval,
unresolved references, missing incident replacements and unrelated deletions
refuse before retention. Mechanical tests check identity and permitted changes;
source-grounded assessment checks meaning. An unsupported or unresolved asserted
change withholds the atomic batch. Keep every proposal and refusal, no hand repair,
passing-subset selection or unapproved extra sample. Run unchanged queries after
admission. If the reader also needs repair, isolate that as a separate contrast.

## Fourth milestone: another run comparing progress

Luis requires a new run after the repair sequence. Before dispatch, select and
freeze the exact condition: fresh acquisition or operation of an existing
ontology/history, producer model/effort, source and input delivery, permitted
feedback, stopping rule and comparison baseline. Do not quietly substitute an
Opus-built ontology for an end-to-end Sol condition or compare a fresh capture
as though it had received the iterative history's targeted amendments.

Use the same fixed questions and declared review criteria across the comparison.
Apply the same final query instrument to both graph snapshots as a separate
read-only contrast, preserving their original outputs. Also retain the old-reader
versus repaired-reader comparison on the identical old graph. This distinguishes
query recovery from new captured content. Compare source-supported quantities,
context, relations and complete answers, with losses and refusals alongside gains.
Report the 25 positive questions separately from controls and paraphrases.
No model output determinism or causal progress claim follows from one sample.

This milestone is on the approved roadmap. Its exact generation condition and
dispatch are not selected by the count-only implementation approval.

## Ownership and completion

Paper owns readers, adopter ontology, capture procedure and assessment. Core owns
generic runtime/protocol behavior. No new Core defect is established here. If a
valid declared record cannot be admitted, replayed, read or traced, isolate the
failure on the pinned public API and send Core a domain-neutral minimal reproducer.
Do not send answer targets or ask Core to implement paper evaluation.

This preparation changes only the plan, master directive and journal. No RED
test has been written or run for these proposed repairs. No implementation,
producer/reviewer dispatch, population mutation, manuscript edit, dependency
change, commit, push or ref movement occurs. Results precede manuscript work.

Recommended next author decision: approve only the count-retrieval cut, including
its preservation/reproduction checks, then evaluate its observed result before
selecting a context amendment. This is not approval to execute the whole inventory.
