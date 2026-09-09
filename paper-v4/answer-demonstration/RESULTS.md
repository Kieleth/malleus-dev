# Exploratory PDF query findings

2026-09-06. Execution history below. The separate, complete preliminary
source-grounded review is in REVIEW-RESULTS.md: all thirty questions per run,
every central witness, and an independent six-case recheck. Human ratification
remains pending. Historical reviews and ledgers are unchanged.

Current coverage counts are 8 covered, 14 partial and 8 none for run-20;
11 covered, 9 partial and 10 none for run-21. These are not accuracy scores.
Neither run fully covers a composition-tier question. See the complete table
and context-supplement history before interpreting the counts.

## Pilot 03 and source inspection

Pilot 03 executes the same thirty questions on the same two frozen ledgers.
Only the spatial query's candidate selection changes: it now follows the
existing subsection subject link to a stored description. Run-20 still returns
one bounding row. Run-21 returns two, an actual edge and a claim containing
the directional qualifications. It does not construct a directional edge from
that wording. Source inspection informed the revision, so it is exploratory.

Candidate-question counts remain 24 and 25. Run-21's distinct traced-record
count rises from 82 to 83. All other question outputs are unchanged. Replay
matches the frozen results; both ledger and graph remain unchanged, with zero
hooked source reads, network operations or embedding imports during querying.

The six-case diagnostic in SOURCE-INSPECTION.md separates source-supported
readback, missing query reachability, ambiguous scope and omitted population
relationships. It is the query author's inspection, not independent evaluation.
In particular, both captures retain the explicit evidential alignment passage,
but neither proposes a SUPPORTS relation. This is not a lost replay edge.

Private outputs: private/paper-v4-answer-demonstration/pilot-03/run-20/ and
run-21/. Their query-result digests are respectively:

- sha256:a8a158ecf00681a0b1a8bdf78e46984e158247ada9a77cb04e24d64ff5b5fde2
- sha256:0024d2e2f729ce6b9582fc267f747fba9eef37e2cebb2d5f256af7da575f887a

Each output now also retains the local binding.py dependency. A regression
checks that the retained program set includes its local import dependencies.
The focused suite is 43 passed, with Ruff and formatting green.
A separate run-21 execution reproduced pilot 03 query-result.json and
trace-summary.json byte-for-byte under pilot-03-reproduction/run-21/.

## Pilot 02

Both ledgers reopened through their frozen Core package and reproduced their
recorded receipt and exported graph. The guarded query/trace region recorded
zero hooked file reads, network operations and embedding imports. Afterward,
the ledger bytes and graph digest were unchanged.

| Observation | Run-20 | Run-21 |
| --- | ---: | ---: |
| Questions attempted | 30 | 30 |
| Questions returning candidates | 24 | 25 |
| Questions returning no candidate | 5 | 4 |
| Programs requiring undeclared relation vocabulary | 1 | 1 |
| Distinct traced records, including endpoints | 102 | 82 |
| Instrument-count candidates | 2 | 1 |
| Detachment-bounding relation rows | 1 | 1 |
| Primary-melt concentration candidates | 6 | 6 |
| Preferred-hypothesis candidates | 1 | 1 |
| SUPPORTS paths into the preferred hypothesis | 0 | 0 |
| Sulfur/chlorine control candidates | 0 | 0 |
| Recurrence-interval control candidates | 0 | 0 |
| Excluded comparison-site control candidates | 10 | 4 |

Candidate counts are not answer counts. In particular, the comparison-site
control returns generic depth/rate candidates whose site pairing and scope
remain unresolved. This is a query precision finding to inspect, not evidence
that the graph fabricated the requested plotted values.

The instrument-count query now reaches a subject-less record in run-21, which
the historical binding could not reach. That demonstrates a query reachability
improvement on the same graph, without repopulation. The two run-20 candidates
and the one run-21 candidate store the same count. This is a readback, not a new
independent source-support judgment.

The detachment query now returns one actual BOUNDED_BY edge in each graph,
instead of mixing it with records that merely mention detachments. The edge
does not alone settle all the question's eastern-side/core-complex qualifiers.

The preferred-hypothesis query returns a stored disposition and modality in
each graph. The evidence-composition query finds no SUPPORTS edge into that
hypothesis. It therefore cannot demonstrate the requested evidential connection.
The count of paths is not an automated adequacy judgment about every possible
graph representation.

The concentration query preserves several ranges, including distinct scopes
and determinations. Selecting one site or estimate because the evaluator knows
the paper's intended answer would violate the experiment. This remains an
answer-selection/representation question for source-grounded inspection.

The method-order program requires an explicit ordering relation that neither
surface declares under its recognized vocabulary. It reports NOT_EXPRESSIBLE
for that program rather than inventing ordering from two method names.

## Retained evidence

Reproduction check: a separate run-20 execution under the same pinned runtime
produced byte-identical query-result.json and trace-summary.json files. Its
outputs remain in private/paper-v4-answer-demonstration/pilot-02-reproduction/.

Private, source-bearing outputs:

- private/paper-v4-answer-demonstration/pilot-02/run-20/
- private/paper-v4-answer-demonstration/pilot-02/run-21/

Each contains query-result.json, trace-summary.json, summary.json and the exact
query and runner programs. Pilot 01 is retained separately, with its original
programs at private/paper-v4-answer-demonstration/pilot-01/.

Pilot 02 query-result digests:

- run-20: sha256:5f5d2229ff25458fdf67f9d4e2c4734f0875e65397e49a323782baaa75bd78b0
- run-21: sha256:2c1c04e34317f0cec3840f38de391a6aced4d9ad69b2e57a5047107191fb9589

No result above is a prospective replicate or a v3 regrading of a closed run.
No Core capability request follows from this pilot: the observed reads execute
through the existing public API. Capture refinement and new producer runs have
not been started by this task.

## Draft manuscript direction

The paper can distinguish three questions: whether a proposed capture is
admitted and replayed, whether requested information is represented, and whether
a query retrieves it with sufficient scope. The exploratory results separate
these boundaries: a changed query reaches an existing count, an explicit edge
supports a relational read, and a missing evidence link limits a compositional
query. Prospective evaluation must establish how often these outcomes recur;
the present pilot establishes neither answer accuracy nor general reliability.
