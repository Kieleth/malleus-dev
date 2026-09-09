# What the fresh capture preserves and loses

E-0328 forward result: the separate [event-reference query fix](EVENT-QUERY-RESULTS.md)
now returns the stored cause/effect records. The diagnosis below remains correct
for its frozen original reader. It does not claim the source-only propositions
or missing qualifications were repaired.

2026-09-08. Read-only diagnosis of sol-fresh-comparison-01, accepted attempt-02.
This is coordinator analysis of frozen artifacts, not another producer run or
an independent assessment of the whole graph. Complete answer assessment is
reported separately in FRESH-COMPARISON-RESULTS.md. Human ratification is pending.

## Finding

Sol did produce a substantial graph with its own ontology: 126 entities,
76 relations and two events. Three relations express SUPPORTS; two of those
reach its preferred hypothesis and are returned by the frozen reader. The
earlier zero-relation result is not reproduced in this condition. This does not
identify why the outcomes differ: effort and the capture procedure changed,
and there is only one new sample.

The remaining failures have different causes. Several facts lose their context
when turned into graph records. Some propositions remain only in retained source
assertions. Other content is represented through fields or references that the
fixed reader does not follow. Admission and replay preserve what was submitted;
they do not explain these losses.

## Five discriminating examples

| Example | Retained source or assertion | Graph representation | Frozen answer boundary |
| --- | --- | --- | --- |
| Instrument count | Page 2, block 002 distinguishes a network of 19 instruments from 17 useful instruments | Count 19, scope “ocean-bottom seismometers,” subject OBSs; no network-role qualification or incident relation | The count selector requires explicit local network/deployment meaning. It returns nothing. The number exists, but its role was lost. |
| Observation-window limitation | Page 2, block 004 says the record is a brief snapshot and activity may vary over years | `claim:snapshot-limit` carries locator, digest, STATED and LIMITATION, but no proposition or semantic links | A citation and a claim category do not express what the limitation says. Query expansion cannot recover it from graph fields alone. |
| Preferred mechanism | The abstract presents CO2 degassing as a suggested cause of deep earthquakes | A HYPOTHESISED/PREFERRED claim references typed cause/effect events; two observations SUPPORT it | The query returns the claim and evidence links but does not expand the event references. Those event meanings exist in the graph, unlike the missing snapshot proposition. |
| Site-specific concentrations | Page 8, block 006 gives calculated concentrations in pre-eruptive melts, separately for RC2 and RC3 | Four records retain site, numbers, units and calculated status, but not the pre-eruptive material role or a link to that material | The selector needs that stage meaning. Widening numerical selection could mix primary and pre-eruptive quantities. |
| Funding | The source identifies several awards, including an ERC grant agreement attributed to an author | Three other FundingAward entities carry `grant_number`; associations connect them to the article. The requested ERC grant is missing. | The program selects relations carrying `award_identifier`, a declaration mismatch detected before population. Fixing that mismatch cannot recover the missing grant or attribution. |

None of the full-graph findings above fills an answer retrospectively. A changed
reader would produce a new answer view requiring its own comparison. A changed
population would be a separate amendment, not a correction hidden inside this run.

## Why counting claims or relations is insufficient

All 37 ScientificClaim records omit `statement`, `description` and `name`.
Every one carries an assertion locator, statement digest, modality and claim
kind. Twenty-six also have a subject, four have cause/effect event references,
and one has comparison references. Therefore “37 claims without statements”
does not mean 37 meaningless records. Structured references can express a
proposition without repeating prose. But the snapshot record has neither form.

The new ontology describes ScientificClaim as a proposition whose content is
traceable to its retained assertion. That is exactly what the snapshot record
provides: access to source evidence, not the proposition inside the graph. The
capture marks its four metadata fields as formalizations and declares no gap.
The mechanical census consequently labels the assertion fully formalized. That
label does not establish complete representation of its meaning.

Likewise, 44 of the 76 relations are contributor-credit relations. Only three
are SUPPORTS. Total graph size is not a measure of scientific argument coverage.
No relation quota or mandatory prose field follows from these observations.

## What is established, and what is not

The producer's first ontology compiled. Its population has the same semantic
content before and after one disclosed source-ID correction. From-empty
execution with identical transaction inputs produces byte-identical ledger,
receipt, graph and query outputs. The accepted graph retains these limitations;
Core did not erase previously submitted proposition text, context or relations.

The source-ID refusal was our handoff defect. The coordinator retained one
source ID but omitted it from the producer's delivered configuration. Core
correctly refused the other ID. The preserved structural return supplied the
missing identifier; a guard permits only that field to change. This is not a
clean first-attempt execution, and it is not a failed semantic proposal.

No generic Core read, relation or replay defect is established. In particular,
Core's subtype-aware Campaign query already returns StudyCampaign. An exact
Instrument-type filter does exist in the duration reader, but the fresh graph
also lacks its required OBSERVED_WITH edge. That filter is not established as
the cause of this run's missing instrument linkage.

We have located losses in representation and retrieval. We have not proved a
single causal explanation of model behavior, nor tested whether the checklist
reliably prevents those losses. Complete input delivery and structural acceptance
do not imply semantic completeness. The source is a known development article,
not a held-out document.

## Next interventions to choose, not execute automatically

A reader-only check could expand the already stored cause/effect event references,
with exact trace closure and preservation of unrelated answers. It would test
whether those references supply the missing mechanism meaning without recapture.
It cannot restore the snapshot warning, network role or material-stage scope.

A separate modelling intervention could require a captured proposition to be
recoverable through meaningful fields and links, or explicitly recorded as
retained-only with a gap. The requirement need not mandate duplicate prose:
a typed predicate with resolved arguments can be sufficient. Evidence that a
passage was retained must not silently stand for its useful representation.
This requires an author-selected adopter condition and source assessment, not
an automatic Core truth check or an answer-shaped mandatory schema.

The administrative guard should also be incorporated into the next condition's
initial delivery contract. The frozen condition here is not silently changed.

## Exact evidence locations

All paths below are beneath
`private/paper-v4-answer-demonstration/sol-fresh-comparison-01/`:

- `producer/work/ontology-attempt-01.yaml`: accepted modelling choices.
- `attempt-01/submitted-population.json`: original refused submission.
- `population-return-01/`: exact diagnostic and missing configuration.
- `attempt-02/submitted-population.json`: source-ID-only correction.
- `attempt-02/public/export-records.json`: graph fields and relations.
- `attempt-02/ledger/retained-capture.json`: assertions and formalization paths.
- `attempt-02/query-result.json`: actual returned answers.
- `reproduction-01/`: identical execution from empty history.
- `reviews/case-d/`: source, graph vocabulary, traces and answer assessment.

Key record IDs are `observation:obs-count`, `claim:snapshot-limit`,
`claim:co2-mechanism`, `event:co2-degassing`, `event:deep-earthquakes`,
`observation:rc2-pre-rb`, `observation:rc2-pre-ba`, `observation:rc3-pre-rb`
and `observation:rc3-pre-ba`. The common reader is frozen under
`private/paper-v4-answer-demonstration/duration-query-01/method/`.
E-0323 and E-0324 record the administrative failure and exact accepted identities.
