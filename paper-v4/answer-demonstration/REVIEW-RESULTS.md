# Complete preliminary answer review

2026-09-06. Two historical captures, thirty questions each, all returned
witnesses reviewed. One fresh Codex reviewer per run and a third fresh reviewer
for the six preselected examples. Human ratification is pending. This is a
retrospective experiment, not a prospective replicate or a human annotation
study. Historical reviews, source captures, ledgers and query outputs remain
unchanged.

## Result and paper claim

The evidence supports an inspectable engineering case study: the replayed graph
returns scoped facts, a real bounding relation and a preferred explanation
retained as a hypothesis. It does not support complete capture of the article's
argument. Neither run fully covers any of the five composition questions.

My recommendation is to use these results as the paper's exploratory answer
demonstration, including failures. Do not describe them as reliable arbitrary
question answering, rich argument reconstruction or evidence against RAG.
Prospective replication and the author's claim decision remain separate.

| Observation | Run-20 | Run-21 |
| --- | ---: | ---: |
| Questions reviewed | 30 | 30 |
| Returned row occurrences | 108 | 83 |
| Distinct central witnesses reviewed | 78 | 63 |
| Questions with every listed semantic covered | 8 | 11 |
| Questions with some semantics covered | 14 | 9 |
| Questions with none covered | 8 | 10 |
| Covered non-control questions | 6/25 | 9/25 |
| Fully covered composition questions | 0/5 | 0/5 |

These are coverage counts, not accuracy scores. Three controls deliberately
request information unavailable on the selected evidence surface. Their NONE
labels are not three failed positive questions. The two paraphrase controls
agree with their originals in both runs.

COVERED means each listed semantic has a reviewer-accepted row. It does not
mean the output is uniquely resolved, concise or fully joined. Primary-melt
queries retain different proxies and sites; the reviewers identify an explicitly
scoped candidate without establishing a unique answer. Run-21's saturation
question is COVERED but assembled from UNLINKED_ROWS. Neither result should be
presented as a single fully resolved scientific conclusion.

Support is judged across all fields projected for one central witness, including
its carried endpoint or subject fields. A partly unsupported witness cannot
supply coverage even for its correct subfields under this instrument. Therefore
NONE need not mean the output contains no correct information. This affects
run-21's campaign and named-grant questions, and run-20's vent-absence question.

## All questions

C = every listed semantic covered; P = some; N = none. Question labels below
are short descriptions, not replacements for the frozen question text.

| Question | Subject | Run-20 | Run-21 |
| --- | --- | --- | --- |
| CQ-T1-01 | Cruise and acquisition | P | N |
| CQ-T1-02 | Deployed instrument count | C | C |
| CQ-T1-03 | Acceptance date | C | C |
| CQ-T1-04 | Data repository and identifier | N | C |
| CQ-T1-05 | Recording duration and scope | P | N |
| CQ-T2-01 | Bounding feature and direction | P | C |
| CQ-T2-02 | Method sequence | N | N |
| CQ-T2-03 | Extinct vent location | N | P |
| CQ-T2-04 | Prior crustal thickness and attribution | P | P |
| CQ-T2-05 | Named grant and recipient | C | N |
| CQ-T3-01 | Earthquake depths and reference | P | P |
| CQ-T3-02 | Primary-melt concentration | C | C |
| CQ-T3-03 | Pre-eruptive concentration | C | C |
| CQ-T3-04 | Relocation uncertainty and event set | P | P |
| CQ-T3-05 | Saturation conditions | P | C |
| CQ-T4-01 | Preferred hypothesis | C | C |
| CQ-T4-02 | Rejected explanation | N | N |
| CQ-T4-03 | Estimation assumption | P | N |
| CQ-T4-04 | Qualified absence of active vents | N | C |
| CQ-T4-05 | Long-period interpretation and hedge | P | N |
| CQ-T5-01 | Seismic and geochemical support | P | P |
| CQ-T5-02 | Comparison between segments | P | P |
| CQ-T5-03 | Observed versus expected depths | P | P |
| CQ-T5-04 | Quality categories and interpretation | P | P |
| CQ-T5-05 | Morphology and off-axis evidence | P | P |
| CQ-C-01 | Absent sulfur/chlorine values | N | N |
| CQ-C-02 | Absent recurrence interval | N | N |
| CQ-C-03 | Unavailable plotted comparison pairs | N | N |
| CQ-C-04 | Instrument-count paraphrase | C | C |
| CQ-C-05 | Primary-melt paraphrase | C | C |

## Six independently rechecked examples

The primary and recheck reviewers agree on all twelve question-level coverage
labels and assembly descriptors. This small, selected recheck is not an estimate
of general reviewer reliability. They sometimes choose different equivalent
count rows and differ on absence reasons. The records retain those differences.

The examples establish four concrete capabilities: recovering the deployment
count with its scope, reading an actual BOUNDED_BY edge, retaining concentration
bounds with units and determination, and preserving a preferred explanation as
HYPOTHESISED. Directional details in run-21 and the causal proposal in both runs
are stored prose, not inferred edges. The primary-melt alternatives remain
visible. The support-composition example is only PARTIAL, and the sulfur/chlorine
control has no answer on the selected text layer.

One of twenty central-witness support judgments initially differed between the
primary reviewers and the independent recheck. The review packets listed
metrology enum tokens without their definitions. In a separately recorded second
reading, all reviewers received the exact frozen metrology source used by both
runs. OPEN_LOWER_BOUND means a stated lower bound with no stated upper bound;
it does not assert exclusion of the lower endpoint. The recheck revised both
minimum-concentration witnesses to SUPPORTED. Run-20's primary reviewer revised
four one-sided-bound witnesses; run-21 clarified two rationales without changing
labels. All twenty rechecked support labels then agree. No question's coverage
or assembly changes. Original records remain untouched.

Primary support judgments were initially 72 SUPPORTED and 6 PARTIAL for run-20,
58 SUPPORTED and 5 PARTIAL for run-21. The proposed contextual amendments make
run-20's counts 76 and 2; run-21 stays 58 and 5. No witness was labelled
UNSUPPORTED or NOT_EVALUABLE. PARTIAL still records material problems; it is not
a clean bill of health. The amendments are model-authored proposals awaiting
the same human ratification as the original reviews.

## Failure locations

| Boundary | Evidence | Consequence |
| --- | --- | --- |
| Query selection | Both rejected-mechanism queries miss captured claims; run-21 misses the captured trace-element assumption. | Fixing reachability need not require a new ontology or population. |
| Missing relationship | Both captures retain the evidential alignment passage, but propose no SUPPORTS relation; replay also has none. | A query cannot recover an edge never submitted. No Core replay-loss reproducer exists. |
| Incomplete scope | Depths, estimators, stages and saturation conditions appear as competing or unlinked records. | Supported components do not establish a resolved comparison or joint condition. |
| Source-support error | Run-21's ERC relation also assigns it the ANR award associated with ISblue. | Structural admission does not certify source attribution. |
| Strength of assertion | Run-20's vent label drops the source's restriction to observations available to date. | NEGATED alone does not preserve epistemic and temporal qualification. |
| Evaluation context | Missing enum definitions caused uncertain support judgments. | Future packet construction now requires every accepted ontology/import definition by digest. |

Exact examples remain in each review's witness and question records. The funding
finding resolves to page:10:block:044; the vent qualification to
page:3:block:002; the evidential connection to page:5:block:006; the primary-melt
proxies to page:8:block:007. Source text is available to evaluation only, never
used to complete a missing query answer. These are statements about the selected
text, not independently verified geoscience.

The original absence vocabulary also lacks a direct reason for a returned
witness rejected by the support gate. Reviewers explain their bounded use of
NOT_MODELLED in prose. Do not tally those reason codes as proof that the graph
lacks the fields. No protocol relabelling was performed to conceal this limit.

## Evidence and remaining decision

Original packets and completed reviews are under
private/paper-v4-answer-demonstration/review-01/run-20/ and run-21/. Each binds
nineteen original material files and leaves human ratification PENDING. The
six-case recheck and its context supplement sit in the parent directory.
Each run has its own metrology-context-supplement.json. Exact record identities
are listed in REVIEW-STATUS.md. No source-bearing artifact is committed.

Both original reviews pass the frozen selective validator. The six-case subset
passes the same witness, locator, coverage and assembly checks with its declared
subset. Supplement checks verify original records, additional material digests,
exact amendment targets and resulting structural consistency without writing
replacement reviews. The owned suite passes 80 tests; combined with the unchanged
v3 review tests, 143 pass. Ruff and formatting pass.

The next author decision is between freezing this bounded demonstration for
prospective attempts and authorizing a separate, predicted improvement. A query
correction could test missed captured claims. A population intervention could
test omitted evidence relationships. They answer different questions and should
not be bundled into an untraceable before/after improvement. Neither has been
started. No missing Core relation-read capability or replay-loss defect was
demonstrated at this boundary.

Forward clarification after the author's investigation request: that finding
does not establish that Core's generic adoption guidance and optional profiles
are sufficient. PATTERN-AUDIT.md records evidence sent to Core about omitted
support relations, semantic coverage, claim representation and qualifications.
Existing complete LLM reviews are the requested working verification; their
pending human fields remain untouched. No source-support judgment is thereby
converted into a human annotation.
