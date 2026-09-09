# What the two captures reveal about Core

2026-09-06. Read-only diagnosis of run-20/run-21 at Core
c95dba7b86bb61487bda9a52458e1ea47cce20ab. No graph repair, producer rerun, Core
edit or replacement of a review. The author has requested LLM verification as
the working review mechanism. It already exists for all sixty question/run
cases and every central witness, plus the independent six-case recheck. Those
records remain model-authored; their untouched human fields are not a claim
of human verification or a blocker to this analysis.

## Correction to the previous conclusion

"No Core change is required" was too broad. The demonstrated fact is narrower:
Core did not lose a submitted SUPPORTS edge. Neither population proposed one.
That does not establish that Core's generic adoption guidance, optional packs
and diagnostics are sufficient. Those are legitimate Core investigation topics.
The author requested that investigation, and the exact evidence was sent to
the Malleus Core task. Evaluation and document-specific judgments remain here.

## Structural completion is not semantic completion

These counts were read directly from each frozen population-plan.json and
census.json, not inferred from the review labels.

| Observation | Run-20 | Run-21 |
| --- | ---: | ---: |
| Source blocks accounted for | 186/186 | 186/186 |
| Untouched blocks | 0 | 0 |
| Entities / events / relations | 426 / 1 / 55 | 508 / 1 / 26 |
| SUPPORTS relations | 0 | 0 |
| CHALLENGES relations | 0 | 0 |
| CONTRIBUTED_TO relations | 39 | 6 |
| FUNDS relations | 0 | 4 |
| Census records with locator and digest | 235/235 | 314/314 |
| Subject-eligible records without subject | 118/235 | 237/314 |
| Heuristically attachable missing subjects | 33 | 46 |
| Census FULLY_FORMALIZED assertions | 317 | 306 |
| Census PARTLY_FORMALIZED assertions | 21 | 93 |
| Census UNFORMALIZED assertions | 55 | 0 |

The provenance denominator covers the types carrying the relevant slots, not
every graph record. An attachable subject is a lexical diagnostic, not a
semantically verified attachment. The producer still chooses the subject.

Both graphs contain real relationships, but their structure differs substantially
and neither represents evidential support or challenge with those predicates.
The larger second graph has fewer relationships and more missing subjects.
Two runs establish a concrete representation fork, not a statistical trend or
the cause of that fork. More captured entities are not evidence of better
argument coverage.

## The SUPPORTS chain

Both accepted surfaces expose ResearchRelation with SUPPORTS. The public graph
read already supports relation traversal; the pilot returns actual BOUNDED_BY
edges. The missing support path is therefore not explained by a missing relation
read API or an undeclared SUPPORTS token.

The same evidential alignment in page:5:block:006 appears as assertion:0142 in
run-20 and assertion:152 in run-21. Each maps to a model/artifact and four
quantity records, no relation and no gap. The population and replay contain no
SUPPORTS relation. The query cannot create that absent relationship.

A fresh read-only reopen at the frozen Core pin reproduced each recorded replay
receipt and graph-export digest. Every relation-predicate count in each input
plan matched the replayed graph, and both ledger files remained byte-identical.
This rules out predicate loss in these two histories. It does not establish
semantic completeness of their inputs or of arbitrary histories.

At this pin, document.py labels any captured assertion with nonempty
formalized_by and no reported gaps FULLY_FORMALIZED. It checks the declared
mapping, not whether every proposition in the retained sentence survives.
Mapping five records is compatible with dropping their stated evidential
connection. The algorithm matches its documented structural rule; the label
can still invite a stronger semantic reading than the mechanism warrants.

The acolyte skill requires both relation endpoints to be named in an assertion
and disallows deriving an implied relation from a neighbouring sentence. That
protects against invented edges, but explicit arguments often refer to earlier
propositions or observations without repeating their names. The open question
is how an adopter should represent those references with exact evidence. We
have not established that this instruction caused either omission.

Requested Core cut: identify an existing public representation for a
source-attributed evidence relation, with direction and independently grounded
endpoints, and show a tiny synthetic conformance example. If a rule or artifact
is missing, propose the smallest optional correction. Do not automatically
infer SUPPORTS from co-occurrence, require a nonzero edge count, or claim that
an accepted edge proves its scientific conclusion.

## Recurring patterns and ownership

| Pattern | Concrete evidence | Appropriate next investigation |
| --- | --- | --- |
| Claims vary between labels and propositions | All 75 run-20 claims have name but no statement or claim_kind. All 145 run-21 claims have statement and claim_kind but no name. Both use the same research pack; the domain restrictions differ. | Core's optional research profile can explain proposition identity, body, source attribution and relation endpoints consistently. Do not silently require verbatim text when reproduction is not permitted. |
| Isolated quantities lose their joint context | Saturation pressure, temperature, depth and initial-content condition are separate records from one assertion. Neither returned view assembles the complete condition. | Show a generic composite observation/condition pattern with role-labelled values and scope, using existing APIs if sufficient. The adopter chooses domain roles. A shared source digest is not an evidential join. |
| Qualification axes are collapsed | Run-21's approximate maximum loses approximation; run-20's category-D interval loses its strict-lower/inclusive-upper distinction. | Clarify existing composition before proposing new fields: APPROXIMATE plus only an upper value may already express a one-sided approximation. Independent endpoint inclusivity is not explicit. OPEN_* means an absent opposite bound, not strict exclusion. The latter confusion was a review-input defect already corrected. |
| Attribution can be wrong despite local provenance | Run-21 attaches the ANR award to an ERC funding relation. The cited paragraph contains both awards. | Exact spans and role-specific derivations can help inspection, but neither co-occurrence nor locality proves attribution. Source-support review remains necessary. |
| Missing retrieval is mistaken for missing knowledge | The declined-mechanism query misses stored claims in both runs; run-21's assumption is captured but missed. | Paper-owned lexical query selection needs a separately versioned test if changed. This does not justify a new Core query engine or a fresh ontology. |
| Coverage labels hide answer ambiguity | Proxy-specific values count as covered although alternatives remain; run-21's joint-condition question is covered with unlinked rows. | Paper-owned evaluation and presentation must report candidate resolution and assembly separately. Do not send a scoring contract to Core. |

The strongest shared gap is semantic structure: how claims, observations,
conditions and evidence relations are represented together. A new model or
larger context alone is not a demonstrated remedy. The existing trace makes
these losses visible, which is useful, but tracing a sentence is not the same
as capturing all of its meaning.

## Evidence and reproduction

For each run, use private/paper-v4-v4-run-NN/results/population-plan.json,
census.json, export-records.json and ledger/retained-capture.json. The accepted
surface is paper-v4/experiment-v4/run-NN/ontology-run/population-surface.json.
Question and witness findings are the unchanged review-01 records and their
separate metrology supplements. REVIEW-STATUS.md lists exact review identities;
the original pilot binds the Core and replay coordinates.

Minimal read-only census inspection:

```sh
jq '.assertions, .subject_coverage, .provenance_coverage' private/paper-v4-v4-run-20/results/census.json
jq '[.records.relations[].properties.relation_type] | group_by(.) | map({predicate:.[0], count:length})' private/paper-v4-v4-run-20/results/population-plan.json
jq '.assertions[] | select(.id=="assertion:0142") | {id,block,modality,formalized_by,gaps}' private/paper-v4-v4-run-20/ledger/retained-capture.json
```

For run-21, substitute run-21 and assertion:152. These commands expose existing
artifacts only. They neither author missing relations nor grade source truth.

Core has been asked to distinguish shipped capability, reproducible defect,
optional improvement and Fable-owned work. Its response belongs below as a
coordination finding, not a retroactive change to the frozen experiment.

Initial Core response, investigation still open: the supplied evidence hashes
match. Core confirms that FULLY_FORMALIZED denotes a nonempty mapping with no
declared gap, not complete semantic capture. It also confirms that the endpoint
restriction is guidance rather than a semantic-coverage check. Fable's concurrent
structured row/field-locator work does not address relation selection or this
document census. These are interim findings, not an agreed correction or a new
Core coordinate. No Core implementation is authorized by this inquiry.

## Final Core RCA received

Core reports a completed read-only audit at c95dba7b86bb61487bda9a52458e1ea47cce20ab,
tree 39a9b9da7dcd41660b8b10fb20b1b1d8e2261082. These are Core's independent
findings, separate from the paper-side replay checks above.

Both captured statements themselves include the agreement with observed
microseismicity. They map 43 and 41 fields across five records respectively,
with no relation formalization and no declared gap. The same-sentence endpoint
guidance is therefore not an established explanation for these omissions.
Whether SUPPORTS is the appropriate predicate, its direction and its endpoints
remain adopter-owned source interpretation.

Core reproduced both censuses byte-for-byte through the exact frozen public
adapter. A neutral in-memory example also returned FULLY_FORMALIZED when only
a Claim name was mapped from a statement containing an explicit support
sentence, with no relation or declared gap. This demonstrates the structural
counter's limit. It is not evidence that Core attempted and failed semantic
inference. Compiled subtype inspection confirms both claim representations fit
the current pack; synthetic proposition names are not the remedy.

Core proposes three bounded changes, none yet authorized or shipped by this
report: explain census results as mapped fields with or without declared gaps;
clarify source-supported relation capture and claim endpoint identity with
retained context; and demonstrate mapped quantities with an absent stated
relationship in a neutral Small Shop example. Historical receipts must remain
unchanged. Any wire rename is a separate decision. Declared-versus-used
predicate reporting could be a later diagnostic, never a quota or a generic
zero-use refusal.

No automatic semantic repair, regex relation detector, Core evaluator or new
extraction framework follows. Metrology composition and endpoint inclusivity
remain a separate optional pack question. Fable's locator implementation
1324cccf56f6a6e712140d804d3f1e0a1dab4a2d had landed at Core's inspection boundary,
with governance unfinished; shared skill edits require coordination. There is
no evidence that locator or pending time work resolves these issues.

The paper can use this bounded RCA and the unchanged reviewed runs now. A
producer rerun under revised guidance would be a new condition, not repair of
the historical graphs. Selection of that condition remains Luis's decision.
