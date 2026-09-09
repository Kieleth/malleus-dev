# The answer now names the proposed cause and effect

The fresh Sol graph can now answer: **the authors prefer the hypothesis that CO2
degassing causes the deep axial earthquakes.** Previously the query returned
the claim's preferred/hypothesized status and two event identifiers, without
the event records needed to say what that explanation was.

The events were already in the accepted graph. The fix retrieves their stored
names, classifications, hypothesis status and evidence traces. It does not add
facts, infer a cause or change the graph. The cause/effect roles come from the
claim's existing typed references, not from the wording of record identifiers.

## Before and after

| Question | Before | After |
| --- | --- | --- |
| Which explanation is preferred, and how strongly is it claimed? | Preferred, hypothesized claim about deep earthquakes; the explanation itself is unreadable from the returned fields | CO2 degassing is proposed as the cause of deep axial earthquakes; preference and hypothesis status remain explicit |
| What evidence supports that explanation? | Two observations support a hypothesis whose cause/effect event descriptions are not returned | The same CO2 and depth observations support the now-readable degassing hypothesis |

My source-grounded assessment finds the first answer complete under its existing
four requirements. The evidence answer gains the mechanism, moving from two to
three of its five requirements, but stays partial: the site qualifications and
brief-observation warning remain missing. The answer does not establish physical
causation or return the complete volume-change and pressure mechanism.

I implemented the query and assessed these two changed answers. This is not an
independent review, and human ratification remains pending. The earlier complete
30-question review and its totals are unchanged. The improvement here is retrieval,
not better model capture.

## What stayed fixed

The other 28 answers are identical. Every original row, numerical value, qualifier
and SUPPORTS path is preserved. The graph, ledger, ontology and source are unchanged.
The two referenced events appear once in each relevant answer. Their typed
references are not relabelled as new Relation records or fabricated graph paths.

Both executions produce the same five output files. All 26 returned record traces
resolve to retained evidence, including the 12 newly exposed event-field
derivations. No source file, network or embedding access occurs during querying.
These checks establish reproducibility and evidence binding, not source truth.

The failing tests cover the missing projection and protect cause/effect binding,
event types and subtypes, one-hop scope, duplicate suppression, original fields,
unchanged answers, missing references and method drift. The implementation uses
the existing public Core reads and paper trace machinery. No Core change or model
dispatch was needed.

The selected paper suite passes 647 tests and two subtests. The focused file
passes 31 tests, including a subsequently added check that the assessment quotes
the frozen question exactly. These are mechanical checks, not human ratification.

## Evidence and remaining work

- [Before answers](../../private/paper-v4-answer-demonstration/sol-fresh-comparison-01/attempt-02/query-result.json)
- [After answers](../../private/paper-v4-answer-demonstration/event-query-01/first/query-result.json)
- [Source assessment and all changed requirements](../../private/paper-v4-answer-demonstration/event-query-01/assessment.md)
- [Resolved evidence traces](../../private/paper-v4-answer-demonstration/event-query-01/first/resolved-trace.json)
- [Frozen method](../../private/paper-v4-answer-demonstration/event-query-01/method/method.json)
- [Execution comparison](../../private/paper-v4-answer-demonstration/event-query-01/first/summary.json)

The new read view is event-query-01/first over the unchanged fresh Sol attempt-02.
The separate repaired history still has its duration-query-01 view. Historical
four-case comparison results are not silently replaced with this newer reader.

Next modelling work must address meaning retained only in source evidence, such
as the snapshot warning, and missing scope attached to quantities. This query
fix does not repair those gaps. No recapture, amendment, Core rebind or manuscript
update is included in this cut.
