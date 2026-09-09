# Query-only correction, pilot 04

2026-09-06. Milestone 2 is complete on the unchanged run-20/run-21 graphs.
This is retrospective query development, not improved population or a fresh
ontology experiment. Original programs, outputs and reviews remain retained.

## Change and execution

The rejected-mechanism query had required both NOT_SUPPORTED and the literal
word melt. It now returns every explicitly declined candidate, preserving
ambiguity instead of selecting an answer by its name. The caveat query missed
CO 2 and a word split by a line-end hyphen. Candidate matching now accepts the
spaced chemical spelling and a dehyphenated line-break alternative, while
preserving normal compound matching and word boundaries. Returned text is
unchanged. No number, missing subject, rejection ground or relation is supplied.

Four new focused cases first failed; after correction all six focused cases
passed, including existing-format and negative controls. All thirty questions
then ran on each frozen ledger. Only three question/run outputs changed:

| Question | Run-20 | Run-21 |
| --- | --- | --- |
| CQ-T4-02, rejected explanation | Zero rows to four declined candidates | Zero rows to four declined candidates |
| CQ-T4-03, estimation caveat | One row, unchanged | Zero rows to one stored claim |

The other 57 question/run outputs are unchanged. Every path output is unchanged.
Both replay receipts and graph exports match the originals. Ledger bytes remain
unchanged; the guarded query/trace phase records zero source reads, network
operations and embedding imports. These checks do not judge answer quality.

Private outputs are under pilot-04/run-20 and pilot-04/run-21. Query-result
identities are respectively sha256:d318a31e34d287283e3a17a7792c59b36e5a8cef5e1d4f37f3baeb41485a1783
and sha256:e87b35704324df6e3eb1d5da40e207abb162d8e8e3f21b9dc12dc4cbbdc3e4c2.
The query source selected for the follow-up is
sha256:1ace62715e813125fce9ec5b38278faae25018468069b22c52bf2d87ea1bbdb1.

## Independent model review and its correction

One fresh Sol reviewer checked both questions in both runs, five distinct
witnesses per run. Each packet contains the full accepted definition closure;
all 26 declared material hashes per packet verified. All ten witness projections
were judged source-supported. Candidate relevance and missing answer semantics
remain separate from that judgment.

The first review incorrectly treated a missing subject slot as sufficient for
claim_subject to be absent. The frozen instrument permits stored prose to carry
a semantic. A separate protocol-consistency check corrected that interpretation
without adding source evidence or changing the instrument. The original record
is unchanged; the supplement identifies each original and proposed judgment.
Both the original subset and the proposed amended subset validate mechanically.

| Question | Run-20 working judgment | Run-21 working judgment |
| --- | --- | --- |
| CQ-T4-02 | PARTIAL, ONE_ROW | PARTIAL, ONE_ROW |
| CQ-T4-03 | PARTIAL, ONE_ROW | COVERED, ONE_ROW |

For the rejected explanation, the newly covered meaning is the shared subject
of the claims, carried in graph prose. The reviewer does not resolve which
candidate meets the melt-movement qualifier, and the query still does not
return the rejection ground. PARTIAL does not mean a useful resolved answer.

For the run-21 caveat, the stored statement carries the estimation claim, its
assumption and subject matter, while claim_kind supplies LIMITATION. This is
reading a graph's stored statement, not deriving a relation. Run-20 still lacks
the assumption content and limitation classification in its returned row.

Review files are review-02/query-correction-recheck.json and
review-02/query-correction-prose-check.json under the private answer-demonstration
directory. They are Sol-authored, not human annotations. No new aggregate
sixty-question score or model ranking is reported. The 57 unchanged outputs
retain their original review context; this is a separately identified subset
review with an explicit correction, not a fresh review of every pilot-04 row.

## Remaining boundary

Retrieval repair recovered a complete caveat in one graph but did not create
the missing evidential relations or resolve all candidates. The next approved
experiment is one fixed-ontology Sol capture after the generic Core clarification
is frozen. It must use this query source before its population is visible.
No further result-driven query changes are authorized within that attempt.
