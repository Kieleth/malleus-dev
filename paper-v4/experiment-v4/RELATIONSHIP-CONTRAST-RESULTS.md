# Contextual guidance: more useful answers, with specific losses

2026-09-14 local date, E-0382. Two fresh Sol captures are complete. Both
source-grounded assessments pass the existing review validator. All semantic
judgments below are model-assisted, not human-ratified.

## Result

The contextual condition exposes more of the article's arguments and answers
more questions completely. It also omits a useful quantity captured by the
control and introduces relationships with the wrong subject. This is a promising
paired observation, not proof of a repeatable improvement or a complete capture.

| Twenty-five substantive questions | Old guidance | Contextual guidance |
| --- | ---: | ---: |
| Fully covered | 7 | 15 |
| Partly covered | 14 | 8 |
| No credited coverage | 4 | 2 |
| Covered requirements, out of 102 | 60 | 78 |

Ten questions gain credited requirements, one loses them, and fourteen keep
the same count. These counts are derived from the reviewers' judgments, not
JSON exact-match scoring. The five controls are separate: two source-absence
controls and two paraphrases produce their expected labels. The already-known
defective third absence control remains recorded but supplies no comparative
evidence, even though its recorded label matches its expected value.

## What changed in practical terms

| Question or source meaning | Old guidance | Contextual guidance |
| --- | --- | --- |
| Why is carbon-dioxide degassing a candidate explanation? | The mechanism and observations are returned, but no supporting link expresses their argumentative role. Four of five requirements. | A reviewed SUPPORTS edge connects the RC2 carbon-dioxide observation to the hypothesis. All five requirements are credited. |
| Why is the cold, thick lithosphere explanation declined? | Candidate and disposition are returned; its counter-evidence stays outside the projected fields. Two of five requirements. | All five requirements appear in one retained paragraph exposed as a hypothesis statement. This gain is prose access, not a complete decomposition into observation-to-hypothesis edges. |
| What conditions produce carbon-dioxide saturation? | Modelled pressure and temperature refer to carbon dioxide, not explicitly to the melt becoming saturated. Four of five requirements. | Both observations name the same melt subject and preserve modelled status. Five of five requirements. |
| What is the final horizontal location uncertainty? | A scoped observation exposes the approximate 2.1 km estimate for the final located-event population. Five of five requirements. | The passage survives as retained evidence, but no returned uncertainty field exposes it. Zero of five requirements. |

The old control has 22 relationships, without SUPPORTS or CHALLENGES. The
contextual graph has 40 relationships, including two SUPPORTS and four
CHALLENGES. Its reviewer judges all six evidence links supported by their cited
source and endpoint evidence. The saturation-depth link describes a model
result; it must not be relabelled a measured earthquake depth.

Two other contextual relationships are only partly supported. The source says
RC1 is bounded by the detachment fault; the proposed edge instead makes the
oceanic core complex the bounded feature. Another edge makes ascending melt
the direct trigger of earthquakes, whereas the source identifies a pressure
increase caused by degassing. Its free-text context retains that intermediate
step, but its endpoint does not. These are capture-meaning defects, not lost
ledger records. Neither was hand-repaired.

Both runs still miss deployment context and method ordering. The contextual
run also fails to capture the trace-element assumption qualifying the
carbon-dioxide estimate. Complete answers to other questions do not erase these
omissions.

## What the comparison does and does not establish

Each fresh gpt-5.6-sol/ultra session constructed its own ontology and population.
Neither producer saw the questions, previous captures or desired relationships.
The only selected scientific instruction difference was the contextual
relationship paragraph. Source, runtime and other inputs stayed fixed. The
same reader and review rules were used, with type bindings frozen separately
against each accepted ontology before population. See the
[design](RELATIONSHIP-CONTRAST.md) and [measurement identities](relationship-measurement.json).

The contextual graph exposes statement text in 146 claim records; the control
exposes no statement fields. Several answer gains therefore reflect accessible
prose rather than structured composition. Bibliography and administrative text
are among records incorrectly classified as scientific claims. Review marks
116 contextual witnesses PARTIAL, versus 28 control witnesses; the corresponding
SUPPORTED counts are 166 and 188. These are different record sets and semantic
units, not a comparative precision estimate. A partly supported witness can
still contain correct fields, but those fields do not receive coverage credit
under the frozen whole-witness rule.

One producer and one fresh assessor per condition cannot separate instruction
effects from model variability or assessor differences. The two assessors ran
as fresh Sol/ultra sessions with identical review instructions and no other
condition's outputs. Their actual session metadata was checked. Different
ontology choices, exposed prose and structural feedback are retained parts of
the observed executions. No reliability, causal-effect size or general model
ranking is claimed.

The earlier successful fresh Sol/ultra capture remains a positive control: 126
entities, two events and 76 relations, including three SUPPORTS and five
CHALLENGES. It used another Core coordinate, reconciliation guidance and an
older reader/review method. Its coverage totals are not subtracted from this
pair's totals. The new result does not establish that Sol previously lacked the
ability to connect evidence. Historical evidence is in
[FRESH-COMPARISON-RESULTS.md](../answer-demonstration/FRESH-COMPARISON-RESULTS.md).

## Execution and assessment evidence

Both histories reproduce their graph and receipt after reopening. All thirty
queries and their evidence traces repeat byte-for-byte without changing either
ledger. The control admits its first population; the contextual producer uses
two bounded structural returns before admission. All forty original contextual
relationships survive unchanged. Failed attempts and their retained evidence
remain available; they contain no accepted domain changes.

Private evidence root: `private/paper-v4-relationship-contrast-01/`.
Control: `a/attempts/attempt-01/`. Contextual: `b/attempts/attempt-03/`.
Each contains `public/run-result.json`, `public/export-records.json`,
`public/replay-receipt.json`, `query/`, `query-repeat/`, and
`review/output/review-record.preliminary.md`. These private captures and the PDF
are not publication artifacts.

| Identity | Old guidance | Contextual guidance |
| --- | --- | --- |
| Graph SHA-256 | `e0db18b21c1bde96765deba1841bceed1204b5ad0cd370903ef0c7beb9e5075c` | `69b907855a28437351eddd682eac2190891723b96c523537ac92f3a97bd8f4c3` |
| Query SHA-256 | `ec5495ae5fc73c44956060ae773df20e10828b9c311dc62864335de99111921d` | `2d0c0b9d8b0be7174c2eebef9237377ddbe2997a64f2bd846244a5b0b794de76` |
| Final preliminary review SHA-256 | `619a5ca14960c9f436e80661ba333743a43dc08650bfab4c2194ac30b4006e7f` | `85c34b219f18663d3bceef903407d050af2e672682e0d796b68d5f04f889f6f3` |

Parent validation covers all 216 and 282 witnesses, all thirty questions and
every declared material digest. Both first review handoffs needed structural
corrections: a timestamp format and source citations for absence controls.
Original files are preserved under `review/output/returned-01/`. Corrections
change completion timestamps and the first two control locator lists only,
not witness judgments, coverage or labels. Rationales, coverage notes, findings
and checklists pass the existing 60-normalized-character source-copy check.
Passing these checks establishes record integrity, not semantic truth.

## Recommended next decision, not launched

Use one bounded, preservation-checked semantic repair on the contextual graph.
Start from the source passages and their surrounding argument, not expected
answer values. Resolve the wrong bounded feature and direct causal subject;
account explicitly for the omitted uncertainty and the source's distinctions
between observations, hypotheses and metadata. Permit the model to identify a
representation limit rather than force a cosmetic edge change. Preserve all
unaffected records and old history, then assess with the unchanged reader and
rules. A later fresh capture would test transfer separately.

No missing generic Core capability has been demonstrated. The existing Core
correction enabled this experiment; no new Core request, capture, repair,
manuscript rewrite, commit or submission follows from this report.
