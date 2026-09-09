# The duration answer now identifies the instruments

The answer now supports: **continuous seismic recording during SMARTIES lasted
approximately 21 days, using ocean-bottom seismometers.** Previously it returned
the same recording duration and campaign, but omitted the instruments.

The instrument connection was already accepted in the graph after the previous
source-reviewed amendment. This repair makes the query follow that connection.
No new facts were captured and no numbers or qualifiers changed.

The other 29 answers and the entire graph and history are unchanged. Both query
executions returned identical results. This isolates a retrieval improvement
from a capture improvement: the graph knew the connection; the query missed it.

## What the answer establishes

The returned records now supply all four existing requirements for this question:
the recording activity, approximate duration, unit and observing system. My
source-grounded assessment changes this one answer from partial to covered,
pending human ratification. I wrote the query and this assessment; this is not a
new independent review or an updated thirty-question total.

The article states the acquisition and recording facts together in
page:2:block:002. A separate reviewer already checked the exact instrument link
against that paragraph, the Methods and the Figure 1 caption. The answer does
**not** establish that all 19 deployed instruments recorded for the whole period,
or that the cruise itself lasted 21 days.

## Evidence

Failing tests first exposed the omitted instrument paths and missing safeguards.
The repair preserves the old observation rows and allows only direct, correctly
directed instrument links. Tests reject borrowed context, changed qualifiers,
broken references, invented paths and changes to unrelated answers. Historical
query comparisons keep their frozen programs.

The full paper selection passes 599 tests and two subtests. The focused query
selection passes 92 tests. Both output directories contain the same four files;
all 59 returned record traces resolve to retained evidence, with 301 field
derivations. These checks establish binding and reproducibility, not truth.

- [Before answer records](../../private/paper-v4-answer-demonstration/sol-acquisition-01/evidence/attempt-01/query-result.json)
- [After answer records and paths](../../private/paper-v4-answer-demonstration/duration-query-01/first/query-result.json)
- [Source assessment and requirement accounting](../../private/paper-v4-answer-demonstration/duration-query-01/assessment.md)
- [Prior separate review of the instrument link](../../private/paper-v4-answer-demonstration/sol-acquisition-01/source-review-01/review.md)
- [Frozen query method](../../private/paper-v4-answer-demonstration/duration-query-01/method/method.json)
- [Execution summary](../../private/paper-v4-answer-demonstration/duration-query-01/first/summary.json)

Core remains 160878cf14c0d27b11a440e26688708e9b7a7e2b. The accepted history remains
sol-acquisition-01/evidence/attempt-01. The current read view is
duration-query-01/first. No Core, ontology, capture or manuscript changes were
needed. The count answer's explicit deployment meaning and the separate new-run
progress comparison remain open; this repair does not silently solve either.
