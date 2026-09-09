# Corrected Sol end-to-end run

2026-09-07. E-0245 authorized one corrected run, not repeated sampling until
success. This report concerns `sol-e2e-corrected-01`. Historical runs remain
unchanged. Independent model-assisted review is complete; human ratification
remains pending.

## What is fixed, and what is not

The paper input-selection regression is fixed for current adoption. The new
stager requires the accepted Core correction and checks the actual staged
skill with Core's existing conformance test. It cannot silently select the
older historical packet. Complete initial and accepted-input frames are
observed in the producer's tool outputs, with the requested model and effort.

The capture problem is not solved. Sol produced nine entities, no Relation
records, and six assertions from five blocks. Two entities carry quantitative
values, and three records carry subject references. This is no longer a graph
of assertion metadata alone, but 148 of 186 blocks are untouched. The producer
explicitly called the capture partial. The unchanged query instrument returns
one preferred-disposition witness for two questions, and nothing for the other
28. Independent review supports that narrow preference witness, but finds only
one partially covered question and no fully covered question.

## Condition and execution

Core: `160878cf14c0d27b11a440e26688708e9b7a7e2b`, tree
`d946a7550dee247a371889f5eadf1cfecc964450`. This is the previously accepted
corrected cut, not latest main. Runtime package bytes were checked against its
entire `src/malleus` tree before staging and execution. No dependency install,
Core modification, shared ref change or package release occurred.

Producer: fresh `gpt-5.6-sol`, explicit `low` effort, no inherited conversation.
Task identity `01a07ccb-4a1c-70b1-89bd-5c457dad0c54`; the same task designed
the ontology and populated it. Actual turn metadata matches across resumes.
The source, root, LinkML types, three packs and history profile match run-21.
Only the skill differs among the eight initial data/instruction artifacts.

There is also a disclosed delivery intervention: the unchanged initial task
has an administrative appendix requiring bounded exact reads. All 36 initial
frames and 23 accepted-input frames verify, including the full reading, skill
and compiled surface. This proves recorded delivery, not comprehension. The
phase-two dispatch supplies acceptance and coordinates, not modelling advice.
Its exact text is retained; historical continuation text was not available as
plaintext for a byte-for-byte comparison. This is not a single-factor skill
experiment or an isolated comparison of model weights.

Ontology attempt 01 refused `REJECTED_SOURCE` for `default_prefix`. One exact
diagnostic returned to the same producer. Attempt 02 compiled with 4,582 facts.
Its class, slot and enum names are unchanged, but the producer also removed
34 descriptions and shortened other text while changing version 0.1.0 to
0.1.1. The log's statement that it removed only the rejected field is inaccurate.
Both attempts remain intact. No hand repair or semantic feedback was supplied.

The query binding froze at 17:05:13 UTC, before population existed. The sole
population submission admits on the first attempt. One KCS produces a 14-event
history. Reopen reproduces the accepted graph and receipt. A separate from-empty
execution with identical transaction inputs reproduces all 16 files exactly,
including the complete ledger. No population correction return was used.

## Capture and query observations

| Observation | Retained result |
| --- | --- |
| Graph | 9 entities, 0 events, 0 relations |
| Quantities | 2 observations with numerical bounds and units |
| Subjects | 3 references on 5 subject-bearing records |
| Assertions | 6, all labelled STATED by the producer |
| Block accounting | 5 asserted, 33 declared nothing assertable, 148 untouched |
| Mapping accounting | 5 FULLY_FORMALIZED, 1 UNFORMALIZED |
| Declared gaps | 1 TYPE_ABSENT, for a split-block availability statement |
| Queries | 27 NO_CANDIDATE, 1 NOT_EXPRESSIBLE, 2 with one candidate each |
| Preliminary answer coverage | 0 FULL, 1 PARTIAL, 29 NONE across 30 questions |
| Preliminary witness support | 1 SUPPORTED distinct witness, used in 2 returned rows |
| Query mutation and forbidden access attempts | None observed by the existing bounded read guard |

Two source-to-graph distinctions matter.

First, values now survive as domain fields. The graph contains an earthquake
depth observation with 10 and 20 km bounds, and an approximate primary-melt
CO2 concentration with 0.4 and 3.0 wt% bounds. The former has a subject; the
latter does not. Source fidelity, datum, scope and usefulness must still be
assessed. These values alone do not establish good document coverage.

Second, the proposition still does not survive in the preferred-claim row.
`claim:preferred-degassing-mechanism` contains `claim_kind: preferred mechanism`,
`hypothesis_disposition: PREFERRED`, and `assertion_modality: STATED`. Its ID is
not an answer field. It has no subject, description or statement. The source
mechanism remains in retained evidence, with no graph relation connecting it.
Returning that status for CQ-T4-01 or CQ-T5-01 does not identify the mechanism
or supply an evidence path. The metadata/content problem persists for claims.

## What the additional probes establish

### The missing relation is upstream of Core

The submitted Relation array is empty, as is the replayed graph's. The accepted
ontology permits BOUNDED_BY and SUPPORTS. The fully delivered source includes
the previously identified bounding passage at page:1:block:005, but this run
leaves that block untouched and creates no bounding endpoints. No edge was
dropped by admission or replay. Correct guidance and complete recorded delivery
are therefore not sufficient to produce the requested broad relational capture
in this one run.

The six retained assertions are concentrated in five blocks. There is no
explicit account of why the remaining substantive blocks require invention.
The harness still ends at the first structurally valid population and does not
return the census for a capture continuation. That workflow boundary is now
concrete, but its causal effect remains untested. No post-submission semantic
feedback was sent in this condition.

### Some stored knowledge is missed by the paper query code

Read-only public Core calls retrieve both quantitative observations and their
derivation traces. The frozen query program's `TEXT_FIELDS` inspects only
`name`, `description`, `statement`, `quantity_kind`, and `count_scope`. The new
ontology puts qualifying text in `observation_kind`, which the filter ignores.

For `observation:deep-earthquake-depth`, the filter sees only `depth`, not the
stored `earthquake depth` qualifier or the subject's name. For
`observation:primary-melt-co2`, it sees `CO2 concentration`, not the stored
`primary melt CO2 concentration`. Consequently both scoped quantity filters
miss these records. Their values are in the graph; empty output is not proof
that the producer captured no quantities.

This is a paper query-binding limitation, not a missing Core read API. The
frozen queries and results were not changed or rescored. A future query condition
must bind relevant slots from the accepted ontology before population, rather
than silently assuming the historical field list is adequate for every ontology.

### Review preparation exposed a separate paper bug

The first review-packet attempt refused a source span because its retained
assertion used spaces where the reading has line breaks. Core's document
contract matches spans after whitespace collapse. Paper's trace check instead
required a raw substring, an unintended stronger requirement.

The exact failure is retained in `review-preparation-01-refusal.json`. Four
positive RED cases reproduced it. The check now uses the declared whitespace
rule without changing either input. Four negative cases still reject changed
words, joined words, case and punctuation. All 28 packet tests pass. No graph,
source, capture, digest, coverage judgment or source-support label was repaired
or converted. The same retained bytes now reach independent review.

## Independent assessment

The independent review packet contains the exact reading, accepted vocabulary,
capture, traces, query inputs and outputs, and the established thirty-question
instrument. One fresh reviewer assessed all thirty questions, all 121 required
semantics and the one distinct returned witness. All 27 material digests and
186 block digests verified. The completed record passes the frozen validator
without a structural correction. This is CODEX_PRELIMINARY, not human review.

CQ-T4-01 is PARTIAL: the row supplies preferred disposition and coarse modality,
two of its four required semantics. It supplies neither the causal proposition
nor its earthquake subject. CQ-T5-01 returns the same row but covers none of its
five evidence requirements. A supported preference classification is not a
supported evidence chain. No other question has a covered semantic in the
returned view. The controls retain their source-absence and evidence-surface
limits; these counts are coverage labels, not an accuracy score.

The reviewer explicitly separates traced but unreturned observations from
capture omissions. Its packet does not expose the values of unreturned records,
so it does not independently certify their scope or our query-filter diagnosis.
The additional public-graph probes above establish the stored values and filter
mismatch separately. Coarse STATED/PREFERRED interpretation remains a judgment
for human ratification. Do not read witness support as proof of the mechanism.

Record: `review-01/review-record.md`, SHA-256
`fe85d346e105d7616a4226191e8f2edd9ddbd75f35ff8ffa304d93d2e2f3aa07`.
Report: `review-01/review-report.md`, SHA-256
`99d274de213252f91ed09cadce06e608d1fe38a8fad084e8723b0dabde8a956b`.
Both are under the private run root below. Human ratification remains pending.

## Next decision

The next proposed improvement is not another unassisted fresh sample. It is
to complete the capture loop on retained evidence, with bounded source-grounded
feedback, and separately correct ontology-aware query binding. Neither change
has been selected or executed here. No new Core seam is required by the observed
failures. Do not claim that restoring the skill solved relational capture or
that this run demonstrates a broad model-capability regression.

## Evidence and reproduction

Private root: `private/paper-v4-answer-demonstration/sol-e2e-corrected-01/`.
`producer-input-manifest.json` and `staging-check.json` freeze the selected
condition; `launch.json` binds the producer; `gate/` retains both compilation
attempts and delivery checks; `manifest.json` binds acceptance before population.
`attempt-01/`, `reproduction-01/`, and `review-01/` retain execution and assessment.

The five paper identities, with the ledger receipt beside its head:

| Identity | SHA-256 |
| --- | --- |
| Source PDF | 7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9 |
| Selected reading | f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17 |
| Accepted ontology | 96b9b75ccf7a935b0d9b89f4aa5ae13d0f9c530fc4276fc18ccc0e94f22ec8ff |
| Ledger head | 21dbad0458764e5d1983be8195e9f009a8948e7d0c60a7eb052ae083f75717d0 |
| Replay receipt | 4643ce3f9ac7bee24dd186ebaae48d39c838ac571498c8dbb829728208e4d933 |
| Query binding | b45e36f7d256ad02f1a7e2c206bd9cbd4f1e0b083054f494b52076123ede64d9 |

Focused tests at this boundary: 279 passed, two subtests. This is the
answer-demonstration, appendix, evaluation-v4 and candidate-source selector,
not a full Core CI claim. The manuscript and submission PDF were not changed.
