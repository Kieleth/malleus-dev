# Fresh capture comparison

E-0325, 2026-09-08. The bounded fresh Sol run and all four complete assessments
are finished. Sol built its own ontology and captured the article in the same
fresh session, without questions or previous outputs. It produced 126 entities,
76 relations and two events, including two returned evidence paths into its
preferred hypothesis. Execution from empty history reproduces exactly.

This is a richer relational capture than the earlier fresh run, but not a recovery
of the useful answer coverage achieved with the supplied ontology or subsequent
repairs. Some meaning remains only in retained source assertions. Some exists in
graph references that the fixed reader does not expand. These are different
improvement targets. The [detailed diagnosis](FRESH-COMPARISON-RCA.md) separates
them, with exact records and source blocks.

## What the reference answers establish

The repaired graph can now return the authors' preferred explanation together
with the geochemical and seismic evidence they use to support it. It preserves
the distinction between calculated concentrations, measured earthquakes and a
hypothesis. It also carries the seismic study's limited observation window.
The fixed-ontology capture returns the hypothesis but not that supporting path.

The repaired graph also connects the SMARTIES cruise, its instrument network
and its recording period. Its duration answer now identifies the instruments.
Those are useful answers with inspectable evidence, not just isolated numbers.

The remaining gaps are substantial. A crustal-thickness answer gives the number
but omits the study and geographic scope. The catalogue exists in the graph but
the query does not assemble its deposit information. Separate site measurements
do not yet answer the requested comparison. These are different problems, not
one generic extraction failure.

## One reader and one interpretation

All four histories were reopened without changing their bytes and queried with
the same frozen reader. One fresh reviewer assessed their answers against the full
selected text under the same rules. Human ratification remains pending. The table
measures returned answers under this reader, not everything present in each graph.

| Reference | Main questions answered completely | Partly answered | No supported answer |
| --- | ---: | ---: | ---: |
| Earlier fresh Sol, own ontology, low effort | 0 | 2 | 23 |
| Sol with supplied ontology, ultra effort | 3 | 15 | 7 |
| Current graph after targeted amendments, same reader | 7 | 11 | 7 |
| New fresh Sol, own ontology, ultra effort and reconciliation checklist | 1 | 10 | 14 |

Each row concerns the 25 main questions. The three absence controls return no
supported answers in every case. Empty output is not an answer establishing
absence. One control returns unrelated local candidates, which receive no credit.
The two paraphrases are separate: neither is answered in the earlier fresh run;
both are partial with the supplied ontology; one is complete and one partial in
the repaired graph; one is partial and one absent in the new fresh capture.
They are not extra main-question evidence.

The reviewer labels all returned central witnesses source-supported under the
declared field-level interpretation. This is not a whole-graph fidelity result,
an accuracy score or a claim that incomplete records are sufficient. Missing
information counts against coverage without automatically making an existing
field false. The coarse meaning of MEASURED remains an explicit human-review
question: the label does not establish direct measurement or who located events.

These are distinct conditions, not a controlled causal sequence. The earlier
fresh and supplied-ontology runs differ in both ontology acquisition and effort.
The repaired graph includes additional model proposals, source review and query
work. It cannot stand for first-pass capture quality. The new fresh run changes
both effort and the capture procedure relative to the earlier fresh run. One
sample cannot separate their effects or estimate reliability. This is a known
development article, not a held-out source. None of these totals should be
subtracted from historical totals produced with different readers or interpretations.

## Concrete examples

| Question | Supplied-ontology capture | Repaired graph |
| --- | --- | --- |
| What supports the preferred mechanism? | Returns the CO2-degassing hypothesis, no supporting path | Returns that hypothesis, linked geochemical and seismic evidence, below-seafloor depth and the brief observation-window qualification |
| How long did recording last, using what? | Approximately 21 days, continuous recording during SMARTIES; instrument absent | Same duration and context, now linked to ocean-bottom seismometers |
| What crustal thickness was reported, where and by whom? | 5.4 ± 0.3 km; study, western-flank scope and crustal age absent | Same partial answer |
| Where was the catalogue deposited? | No answer, although a catalogue resource exists elsewhere in the graph | Same retrieval/assembly gap |

The hypothesis path records the authors' argument. It does not establish that
degassing caused the earthquakes. Some scope and time qualifications are stored
prose; they are not typed spatial deductions.

## What the new run returns

The acceptance date is its one complete answer. Partial answers include the
approximately 21-day recording period, calculated primary-melt CO2 concentration,
earthquake depth ranges and linked evidence supporting a preferred hypothesis.
The limits matter:

| Question | What comes back | What still prevents a complete answer |
| --- | --- | --- |
| What supports the preferred mechanism? | Two SUPPORTS paths from separate CO2 and earthquake-depth observations to a HYPOTHESISED/PREFERRED claim | The query does not expand the stored cause/effect event references. Site scope and the observation-window warning are also missing from the answer. |
| How many instruments were in the network? | Nothing | The graph stores 19 OBSs, but not the count's network role. The strict count selector will not infer it. |
| What were the pre-eruptive concentrations? | Nothing | Site-specific values exist, but their graph records omit the pre-eruptive material role. |
| What is the final catalogue's horizontal uncertainty? | An earlier uncertainty value is selected | That candidate belongs to an earlier processing stage and cannot answer the final-catalogue question. The requested final value is not captured. |

All 37 claim records lack statement text. Some still express meaning through
structured references, notably the cause/effect events. Others, such as the
brief-snapshot limitation, retain only a claim category, modality and citation.
For those records, the retained source tells us what the claim says, but the
graph does not. Merely widening a query cannot supply that missing proposition.

There are 77 retained assertions. Their mechanical fully-formalized census labels
are not evidence of complete semantic representation. Similarly, 44 of the 76
relations concern contributor credits, not scientific supporting evidence.

## Execution and the disclosed correction

The own ontology compiled on its first submission. Population received no semantic
feedback or hand repair. Its first execution refused an unretained source reference:
the coordinator had omitted the identifier its runner registers. The original
submission is retained. One structural return supplied that missing configuration;
the same producer corrected only capture.attribution.source_id. A complete parsed
JSON comparison confirms every assertion and graph value stayed fixed. This is
a corrected administrative handoff, not a clean first-attempt execution.

The corrected capture admits to a 13-event ledger. Reopening reproduces its graph
and receipt. A second from-empty execution with identical population and transaction
inputs matches the ledger, complete result, query output and traces byte-for-byte.
This tests execution reproducibility, not model regeneration. The query guard
records no source-file reads, network calls or embedding imports. That is a bounded
observation about this execution, not a comparison proving embeddings unnecessary
for every retrieval task.

The fixed reader already has two declaration gaps: method ordering and funding.
Those must not be reported as proof that the new capture omits the corresponding
source facts. The remaining declarations passing their checks does not guarantee
that every selector will retrieve the intended content. The whole graph may be
inspected to diagnose missed content, never to fill an incomplete query answer.

The bounded run, reproduction, thirty-question source review and four-case
comparison are complete. The earlier graph and current read view stay unchanged.
No Core capability gap has been established at this boundary. No additional sample,
reader repair or population amendment has launched.

The next proposed cut is a query-only test of the already stored cause/effect
event references. It would expose existing content before asking a model to add
anything. A separate representation improvement is needed for propositions and
qualifications retained only in source evidence. Neither intervention is approved
by completion of this comparison.

## Evidence

Private packets are under
`private/paper-v4-answer-demonstration/sol-fresh-comparison-01/reviews/`.
Case A is the supplied-ontology capture, B the earlier fresh run, C the repaired
graph, D the new fresh capture. Each includes the exact answers, full source and
vocabulary, resolved capture traces, complete review.json and a readable
thirty-question review.md.
E-0320 records packet identities; E-0322 records completed review identities.
E-0324 records the admitted/reproduced graph; E-0325 records the fourth review.
The reviewer saw anonymized query envelopes, not this condition key or old grades.
Artifacts may still reveal origin; no perfect blinding is claimed. One reviewer
assessed all four views, not four independent reviewer replicates. The new packet
accounts for all 30 questions, 121 required semantic items, 20 central witnesses,
24 traced records and 183 capture-scoped derivations. Accounting validation passes;
it does not establish scientific correctness.

The final combined paper selection passes 617 tests and two subtests. These test
execution and evidence accounting. They do not mechanically certify source meaning.
No manuscript, Core, dependency or repository-ref change accompanies these results.
