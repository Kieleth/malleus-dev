# Query repair and census continuation

2026-09-07. E-0247 authorized two separate changes. E-0248 records execution.
These are engineering results, not a manuscript revision. Original evidence
remains intact. Both independent reviews are complete; human ratification is
pending for every model-assisted review.

## Result

The query repair retrieves existing typed quantities that the old text filter
missed. The capture continuation adds proposition text but removes those typed
quantities. More assertions and records did not produce a uniformly better graph.

| Condition | Entities | Typed quantity records | Asserted blocks | Questions returning rows | Preliminary FULL / PARTIAL / NONE |
| --- | ---: | ---: | ---: | ---: | --- |
| Original capture, original queries | 9 | 2 | 5 | 2 | 0 / 1 / 29 |
| Same capture, corrected text binding | 9 | 2 | 5 | 6 | 0 / 5 / 25 |
| Census continuation, same corrected binding | 20 | 0 | 14 | 2 | 1 / 1 / 28 |

All three graphs have zero Relation records. The first two rows are the same
graph and ledger, not independent capture runs. Coverage counts describe the
returned answer view, not accuracy or the whole graph's semantic quality.
Full coverage corresponds to the review protocol's `COVERED` label.

## What changed

Core stays at `160878cf14c0d27b11a440e26688708e9b7a7e2b`, tree
`d946a7550dee247a371889f5eadf1cfecc964450`. Reading, accepted ontology and
Sol/low settings stay fixed. The original fresh producer continued in the same
session. It received its own prior population, census and a generic worklist,
not questions, query code, answers or scores. All six new feedback frames verify
in its actual tool outputs. This is a continuation, not another fresh E2E sample.

The query method froze before that continuation. It classifies text slots from
all 36 accepted record types and refuses unknown string slots. It preserves the
exact historical query functions, normalization, numeric requirements,
projections and relation traversal. It adds no joins, inferred edges or numbers
parsed from prose. The original query control reproduced exactly. Candidate
rows rose from two to six, representing three distinct central witnesses.

The new binding makes the earthquake-depth and primary-melt quantity records
reachable. Independent review supports their bounded projected fields, but
does not supply missing site scope or depth datum from source context. Both
remain partial answers. A preferred-status witness is also supported, without
establishing the mechanism or its evidence chain. All thirty questions and 121
required semantics were reviewed; the frozen validator passes.

## Capture execution

One semantic feedback dispatch was followed by exactly two structural returns.
Candidate 01 refused `NOT_VERBATIM` for three statements whose source
line-break hyphenation had been removed. Candidate 02 restored those exact
statements and their graph properties. It refused `SUBJECT_NOT_NAMED` for three
subject references. Candidate 03 added source-written subject aliases and their
derivations. Mechanical diffs confirm no other changes across these corrections.
No hand repair, semantic grading or additional producer dispatch occurred.

Candidate 03 admits and replays: twenty entities, sixteen assertions, one KCS
and thirteen ledger events. A separate from-empty execution reproduces all
twelve files byte-for-byte. Fourteen blocks are asserted, 33 are declared
nothing assertable and 139 remain untouched, out of 186. All sixteen assertions
are structurally `FULLY_FORMALIZED`; that is mapping accounting, not a semantic
endorsement. No declared gap or Relation record is present.

The consolidated file contains sixteen claim records, now with proposition
text, plus four domain objects. It contains no quantitative Observation record
and no scalar numeric property. Quantity ranges appear in claim prose, which
the frozen numeric queries deliberately do not parse. The same query method
therefore returns two rows for one distinct central witness.

Independent review supports that witness and finds CQ-T4-01 fully covered in
one row: the returned statement identifies the authors' preferred CO2-degassing
explanation, its RC2 subject and its qualified status. This is a useful gain over
the original category-only claim. CQ-T5-01 is partial: the row states the
mechanism but supplies neither supporting quantitative observations nor an
evidence connection. It is not a composed evidence argument or causal proof.
The remaining 28 questions have no covered semantics in their returned views.

The final reviewer checked all thirty questions, 121 required semantics and
both row occurrences; all packet and reading-block digests match. The frozen
validator passes without correction. Human ratification must settle whether
the qualitative depth wording in the preferred claim also counts as supporting
seismic evidence. The reviewer treats it as the phenomenon being explained.
Unreturned claims were not silently added to answers or certified wholesale.

## Root cause and limits

The failure is visible before admission. Candidate 01 already has zero numeric
fields. Candidates 02 and 03 preserve that state. The original graph had four
numeric fields across two typed observations. Core faithfully admits and replays
each submitted representation; the query method is unchanged between the last
two conditions. Neither structural retries, replay loss nor a query rollback
explains this particular regression.

The paper workflow is also responsible. I chose a complete consolidated capture
in a separate from-empty history to isolate capture continuation from semantic
re-entry. The task asked the producer to retain or correct prior records where
the source warranted them, but no mechanical rule required it to account for
each removal or changed value. The producer replaced typed observations with
narrative claims, and structural admission had no declared preservation
obligation to enforce. This establishes the observable failure path, not the
model's internal reason for choosing that representation.

The new read-only `capture_delta.py` makes such changes explicit, with tests for
lost quantities hidden in prose, changed values under the same identity and
malformed exports. Here it finds seven removed IDs, eighteen added, one changed
and one unchanged. Renamed claims may retain content, so seven removed IDs are
not seven proven semantic losses. The absence of any typed numeric replacement
is directly testable. This diagnostic does not repair the capture or impose a
new admission policy retrospectively.

Relation capture remains unresolved. The producer reports ambiguity in finer
process and proposition identities. That does not explain every omission:
the accepted ontology also permits a simpler explicit bounding relation, and
the previously identified source block remains untouched. No relation was
submitted or dropped. `UNTOUCHED` means unaccounted in the capture, not proof
that a block was unread. This one continuation does not establish a general
model capability limit or a missing Core API.

## Next decision, not executed

The smallest proposed next condition is incremental capture against the retained
accepted graph, with an explicit account of additions, corrections and any
retirement. Test preservation mechanically before accepting a replacement;
source-grounded review must still judge whether a correction is justified.
Existing Core history/KCS mechanisms are the starting point, not a new Core
evaluation contract. No additional run or automatic merge is authorized here.

## Retained evidence

Private root: `private/paper-v4-answer-demonstration/sol-census-01/`.
Original source, reading and ontology identities remain those in
[the corrected E2E report](CORRECTED-E2E-RESULTS.md). Exact continuation source
and code closure is retained in `manifest.json` and `query-method/method.json`.

| Artifact | SHA-256 |
| --- | --- |
| Frozen query method | `a4cf93c6650b4177b809cf38e6ff93c7ffc276f3b91fc5a9652b1a42b4e1208e` |
| Query-only answers | `a7b5174b9b35fd65e0239cef665f5d578afd2ab3a383bc8e164da49353cdcfd0` |
| Accepted capture | `25af4d61598c5297f532568f0f9454fc80fb85bbfb80b0e5b6a368c9570acd94` |
| Continuation ledger head | `22c60bb986e86db7abf1652a3e4b876ec3ed984bbc45837279ff25c5a39c4184` |
| Replay receipt | `1dba92596558599a486590df7c0e1e4f3a0f1f11dd5855c48fc873a3ba93b5ab` |
| Continuation answers | `967c33085eab22be5e829c637028ca438c61162582476e1b09737c26b2a1dd3a` |

Query-only review is in `before-review/`; continuation review is in
`after-review/`. Each contains the exact answer rows, source locators, retained
assertions, derivations, judgment record and qualifications. Capture attempts,
both exact structural returns, reproduction, producer limitations and
`capture-delta.json` are retained separately. No PDF, private source text or
population bytes were added to public paper evidence.

Final focused gate: 293 tests and two subtests pass. Both review validators pass;
eight changed Python files pass Ruff and formatting. No Core change, manuscript
edit, commit, push, shared ref movement or heartbeat restart. No producer or
reviewer remains active. Master stays 1.5.13; another condition needs a decision.
