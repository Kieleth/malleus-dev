# The Shop reconsideration experiment: results as they stand

The durable record of what this experiment produced, what binds each result,
and what each result may and may not be quoted for. Written on the Overlord's
close-out of the third case (paper ledger E-0480). Nothing here is a proposal
and nothing here asks for a decision.

Public file. It carries record ids, slot names, mechanisms, counts and digests.
It reproduces no passage of the Shop chapter's prose.

## Names

The harness names the three producer sessions stages A, B and C, and those
letters appear here only inside file paths. In prose they are:

| harness name | what it is |
| :-- | :-- |
| stage A | the **table population**: one fresh session builds a graph from the chapter's table |
| stage B | the **second boundary**: a fresh session reviews three declared interpretations against a second instalment of evidence |
| stage C | the **third boundary**: a fresh session reviews five declared interpretations against a third instalment, over an ontology Luis grew between the two |

A *boundary* is a frozen list of obligations. An *obligation* is one declared
interpretation the producer must review exactly once, answering `CORRECTION`,
`NO_CHANGE`, `CONFLICT` or `UNRESOLVED`. An *assessor* is a fresh session that
neither produced the result nor prepared the run, and it judges each review as
`correctly_changed`, `correctly_preserved`, `missed` or `spurious`.

## Core coordinates

| coordinate | value |
| :-- | :-- |
| repository main at close-out | `ff1c69315f68de949a223aedd3175e0319802807` (Seal OVR-000466) |
| Core for the table population and the second boundary | export `private/shop-progressive-01/runtime`, Core `e7937b89917c8da7ee4a08acc22e99ad12b9985b`, governance head OVR-000462 |
| Core for the third boundary | export `private/shop-progressive-01/runtime-d5d014ba`, Core `d5d014ba1d7e3bfe906bc71dc93ded5657a3b424`, governance head OVR-000464 |

The third boundary's replay verification records those two Core values in its
own file (`producer/stage-c/replay-verification.json`, `core_commit`,
`core_governance_head`). A runner selects its export by matching two markers
against its own pin, not by directory name, so the two launched workspaces keep
the export they launched against (D0-REPORT.md addendum 10).

## The three producer sessions, on one growing history

Each session was a fresh Opus 5 session with no inherited context, given a
workspace, a procedure naming the interpreter and the Core export, and the
evidence for its own instalment and no other. None was given the mapping from
evidence to ontology.

| | table population | second boundary | third boundary |
| :-- | :-- | :-- | :-- |
| launched | 2026-09-17T04:48:13Z | 2026-09-17T14:37:05Z | 2026-09-19T01:12:08Z |
| dispatch digest | `9018e0dd` | (E-0449) | `57ff495c` |
| evidence given | the chapter's table | three passages, anchored `ed3ee738`, 3 rows | one withheld passage, `d2ff1c6d`, 1 row |
| obligations | none | 3 | 5 |
| result | PARTIAL | COMPLETE | COMPLETE |
| reviews written | — | 1 `NO_CHANGE`, 2 `CORRECTION` | 4 `NO_CHANGE`, 1 `CORRECTION` |
| gaps declared | 9, in the session log only | 2, permitted kinds | 1, `RELATION_ABSENT` |
| ledger events after | 22 | 38 | 50 |
| export | `b92d3c08` | `26f9a842` | `a175da0b` |
| replay receipt | `30a211de` | `664d8336` | `67b088fe` |
| graph after | 23 entities, 21 events, 62 participations, 0 relations | 26 entities, 21 events, 62 participations, 7 relations | 27 entities, 21 events, 62 participations, 8 relations |
| ledger entries | E-0433, E-0438, E-0441 | E-0449, E-0451, E-0452 | E-0475, E-0476, E-0477 |

The table population admitted 107 records in two change sets, both `SATISFIED`
on both Shop rules (receipts `abfe76c3`, `8dbeb70d`). It declared nine gaps in
its session log rather than in the plan, because the plan compiler refuses
every gap kind it does not recognise and the permitted vocabulary appeared in no
file the session was given (E-0438). The session's output was then destroyed by
the preparation agent's own test suite after verification and recovered byte for
byte from the producer session's transcript (E-0440, E-0441); archive-on-report
dates from that incident.

The second boundary appended and rewrote nothing: the first 22 lines of its
history are byte-identical to the table population's archived history. It
admitted two change sets of five operations each, identities `a9cbc6ed` and
`f534e394`, receipts `317870ef` and `972bff7b`, both `SATISFIED` with zero
violations on both rules (E-0452).

The third boundary appended and rewrote nothing: the first 41 lines of its
50-event history hash `1e9c1e91`, the handed-off revised history byte for byte
(`replay-verification.json`, `history.inherited_prefix_sha256`). It admitted one
change set of two operations, identity `eb6a47f8`, adding
`shop:claim:order-correction:B-Y` of the class Luis's revision introduced and
`shop:relation:corrects-state:B:Y:e7` binding that claim to the current state
record rather than to the retired one.

## Luis's recorded additive ontology revision

Before the third boundary's session started, and after the second boundary had
finished, Luis's decision was recorded on the history as one act. Its receipt is
`producer/stage-c/revision-receipt.json`, status `RECORDED`.

| field | value |
| :-- | :-- |
| revision id | `revision:shop:0.1.0-to-0.2.0` |
| actor | `actor:luis` |
| reason | names his 2026-09-18 ruling and paper ledger E-0469 |
| issued at | `2026-09-16T00:00:00Z`, the runner's fixed transaction time |
| changes | `ADD_CLASS` (`OrderCorrectionClaim` is_a `ShopContextClaim`), `ADD_CLASS` (`CorrectsState` is_a `ContextRelation`, source `OrderCorrectionClaim`, target `SupplierOrderState`), `REBIND_CHECK_CONTRACT` |
| revision identity | `sha256:d2176cc2d2b8c09c…` |
| migration receipt | `sha256:8298d68114929313…` |
| ontology | `sha256:6ef56157c86a9a25…` → `sha256:7234304992304c2a…` |
| contract identity | `sha256:af74ca2ac6963e30…` → `sha256:2291b57bd7d4b56c…` |
| required check contract | `sha256:83816c3abbd408c6…` → `sha256:1bf386c30725d6e0…` |
| ledger events | 38 → 41 |
| history | `sha256:07496a1083e63e26…` → `sha256:1e9c1e9177c6100d…` |
| replay receipt | `sha256:664d833613fa8293…` → `sha256:a13be43c9ec0ae2c…` |
| graph unchanged | `true`, against the second boundary's archived export `26f9a842` |
| re-pinned contract retained as | `shop-run-d-content-rules:logic:1bf386c30725`, rules `…:rules:ae8de5879af5` |

Three facts about this act matter for what it may be quoted for. The rule bytes
are identical on both sides (`ruleset_hash sha256:ae8de5879af52113…`): only the
ontology binding inside the check contract moved. The graph records are
byte-identical across the revision, while the replay receipt and the accepted
state digest do move, because they bind the contract and the contract changed.
And the four check receipts recorded before the revision still read `SATISFIED`
and still name the old check contract `83816c3a`, while the history's
`required_checks` names the new one (D0-REPORT.md addenda 10 and 11).

The capability this act uses was built in Core for this run (E-0459, E-0462) and
sealed as OVR-000464; the census that established the path and its stopping
point is E-0458 and E-0465.

## What the third boundary's producer did, by obligation

| obligation | bound records | outcome |
| :-- | :-- | :-- |
| `obligation:supplier-order-quantity-correction` | 7 | `CORRECTION` |
| `obligation:distinct-occurrences` | 6 | `NO_CHANGE` |
| `obligation:order-relationship-and-delay` | 5 | `NO_CHANGE` |
| `obligation:shipment-eligibility` | 7 | `NO_CHANGE` |
| `obligation:inventory-unit-identity` | 22 | `NO_CHANGE` |

Boundary identity `sha256:db3dc7d06e11cb12…`, carried beside the boundary in the
obligations file and equal to what the checker computes. The three obligations
of the second boundary were re-declared here; one of them now binds the two
`CustomerOrder` relations and the `DelayOrder` relation the second boundary's
producer itself wrote, so a re-declared obligation is not the same question
twice (D0-REPORT.md addendum 11).

The single admission was checked and recorded:

| | |
| :-- | :-- |
| change set | `change:shop-context-order-correction-v1`, identity `sha256:eb6a47f880116372…` |
| operations | 2 |
| contract it was recorded against | `sha256:2291b57bd7d4b56c…`, the post-revision one |
| check receipt | `sha256:0144c70864e8825e…` |
| outcome | `SATISFIED`, violations `[]` |
| rules checked | `NO_CONFLICTING_QUANTITY`, `NO_EMPTY_RECORD` |
| facts | 764 |
| check contract | `sha256:1bf386c30725d6e0…` on ontology `sha256:7234304992304c2a…` |
| engine | SWI-Prolog |

Those values are read from the receipt's retained bytes inside the archived
history, not from the producer's own report.

One gap, `RELATION_ABSENT`: the source ties the correction to what the two sales
orders require, and the ontology relates an order-correction claim only to a
recorded order state, so that link cannot be recorded. Kind permitted, source
retained at `d2ff1c6d`, locator `row:0:text` resolves (E-0477).

## The two review-coverage certificates

The checker is `malleus.acquisition.check_review_coverage`. It reads the
boundary and the reviews, and nothing else.

**Second boundary: refused.** All three reviews carried the boundary's id string
`reading:shop-context-stage-b` where the checker requires the boundary's
identity digest, so it returned `REFUSED`, `MALFORMED_INPUT`,
`review.boundary_identity`. The procedure had told the producer to write "the
identity the obligations file gives" and the staged obligations file contained
no identity digest. With that one field corrected by the evaluator and nothing
else changed, the checker ACCEPTED: complete, nothing missing, nothing stale,
two pending corrections and one unchanged, receipt `9827ac04`. That corrected
run is recorded as the evaluator's diagnostic; the archived reviews stand as
written and the run has no certificate as produced (E-0452).

**Third boundary: complete.** The checker ran over the five archived reviews
exactly as the producer wrote them, nothing corrected
(`producer/stage-c/review-coverage.json`, `e240d837`):

| | |
| :-- | :-- |
| `complete` | `true` |
| `missing` | `[]` |
| `stale` | `[]` |
| `require_complete()` | returned without raising |
| boundary identity | `sha256:db3dc7d06e11cb12…`, equal to the declared one |
| coverage identity | `sha256:5114bbb843142892…` |
| profile identity | `sha256:ffdcaf90e34facf9…` |
| `groups.pending_corrections` | `obligation:supplier-order-quantity-correction` |
| `groups.unchanged` | the other four |
| `groups.conflicts`, `groups.unresolved` | `[]`, `[]` |

## The two assessors

Each was one fresh Opus 5 session that neither produced the result nor prepared
the run, dispatched with the packet's `DISPATCH.md` verbatim preceded by one
line giving the packet's absolute path.

| | second boundary | third boundary |
| :-- | :-- | :-- |
| record | `assessment/stage-b-packet/review-record.json` | `assessment/stage-c-packet/review-record.json` |
| record digest | `sha256:d35ab5a9c7ec9015…` | `sha256:90723d8fb9f97e2a…` |
| protocol bound | v3.3, `sha256:dddcc098e65e51e6…` | v3.4, `sha256:d01538fbf6b4cbf5…` |
| dispatch | `6a38dee3`, dispatched text `373aa292` | `2aebfe6d`, dispatched text `b360055d` |
| packet | 21 files, 1,797,970 bytes | 26 files, 3,349,130 bytes, containment CONTAINED over 23 |
| obligations | 3 | 5 |
| correctly changed | **2** | **1** |
| correctly preserved | **1** | **4** |
| missed | **0** | **0** |
| spurious | **0** | **0** |
| validator | VALID, 19 locators, no forbidden field | VALID, 22 locators, no forbidden field |
| residuals for the ratifier | 2, neither moving a count | 3, none moving a count |
| ledger | E-0453, E-0454 | E-0478 |

The third boundary's assessor recorded three residuals: the `CorrectsState`
relation targets the standing state record while the passage describes the
placement that was corrected, and the ontology's wording does not settle the
endpoint; the shipment-eligibility review states the standing
`NOT_ESTABLISHED` limit by implication rather than asserting a permission; and
the inventory review reads printed times as an ordering, which the ground truth
refuses, while the load-bearing reason is the recorded supersession. It weighed
the anchoring packet defect (below) and did not let it decide a count.

## The two author ratifications

| | second boundary | third boundary |
| :-- | :-- | :-- |
| Luis's words | "1 ratified" | "ratified" |
| judgements changed | none | none |
| binding file | `paper-v4/evaluation-v4/author-ratification-2026-09-17-shop-staged-review.md` | `paper-v4/evaluation-v4/author-ratification-2026-09-18-shop-third-boundary.md` |
| binding file digest | `sha256:552592661bae1b4d…` | `sha256:ff172ee78de71833…` |
| record ratified | `d35ab5a9` | `90723d8f` |
| protocol in force at ratification | v3.3 | v3.4 |
| ratified form of the record | `review-record-ratified.json`, `sha256:541130a46b541650…` | `review-record-ratified.json`, `sha256:c4d001108edc5773…` |
| `record_sha256` in the block | `sha256:b93a5cd940e95ac9…` | `sha256:afb68483b954fc86…` |
| ledger | E-0455 | E-0479 |

Protocol v3.3 defined no ratification write at all: its validator never read the
ratification block and accepted a record that called itself `HUMAN_RATIFIED`
with the block pending, emptied or nonsense (measured, D0-REPORT.md addendum 9).
So under v3.3 the binding file *is* the ratification and the record was not
edited. Protocol v3.4 adds the clause: a `HUMAN_RATIFIED` record carries a block
with `status`, `actor_id` equal to the protocol's declared ratifier, `at`,
`binding_file`, `binding_file_sha256`, `record_sha256` over the record with the
block removed, and a one-sentence `scope`; the block is written by the holder of
the binding file and `never_written_by` the assessor or the harness. Because
`record_sha256` is taken over the record minus its own block, ratifying cannot
alter a judgement.

Both archived records are unedited. The second boundary's record binds v3.3's
digest and validates under v3.4 because v3.4's `supersedes` block declares
`superseded_digests` `[dddcc098…]` and `records_may_bind`
`THE_GOVERNING_DIGEST_OR_ANY_DIGEST_IN_superseded_digests`, which the validator
reads from the protocol bytes rather than from a constant (E-0474). The third
boundary's two records bind v3.4 directly; no supersession is in play for them
(E-0480).

Scope, stated in both binding files: each ratification covers one record, its
judgements and their counts. The review-coverage certificate is a mechanical
result recorded separately and is not ratified.

## Which layer each result tested

Say this exactly, and do not let a narrower test read as the whole gate.

| result | layer it tested |
| :-- | :-- |
| every `SATISFIED` verdict in this run | the **structural gate plus the two Prolog rules** `NO_CONFLICTING_QUANTITY` and `NO_EMPTY_RECORD`, at admission, under the check contract the history requires. Nothing else ran. |
| the third boundary's complete certificate | the **review-coverage checker**, over the boundary and the five reviews. It never reads the ledger, so nothing about the ledger's contents is established by it. |
| the counts 2/1/0/0 and 1/4/0/0 | the **assessor**, one fresh session per boundary, judging one review per obligation against ground truth. |
| the two ratifications | a **human author** reading each record in full, bound to that record's digest. |
| the revision's `graph_unchanged` and byte-identical replay | **replay**, on the pinned Core export, against the previously archived export. |

One clarification on the third boundary's `SATISFIED`. The rules ran once, at
the admission of the single change set, over the compiled facts of the candidate
state: 764 facts, zero violations. The four receipts recorded before the
ontology revision are archival verification of verdicts recorded earlier, still
naming the old check contract `83816c3a`. Nothing re-ran the rules over the
whole graph under the new contract.

## Everything that binds a claim

| what | digest |
| :-- | :-- |
| third boundary's archived work | `producer/stage-c/archive/2026-09-19T01:12:08Z`, 11 files, 3,235,181 bytes, every file equal to `ARCHIVE.json` |
| archived history | `sha256:10dfda4ea9700390…`, 50 lines; first 41 lines `sha256:1e9c1e9177c6100d…` |
| evidence packet | `packet:stage-c:context`, `sha256:d2ff1c6dcbe95709…` |
| export | `sha256:a175da0ba16d08ef…` |
| replay verification | `producer/stage-c/replay-verification.json`, `sha256:b8ef9477…` |
| coverage certificate | `producer/stage-c/review-coverage.json`, `sha256:e240d837…`, identity `sha256:5114bbb843142892…` |
| change set admitted | `sha256:eb6a47f880116372…` |
| check receipt | `sha256:0144c70864e8825e…` |
| revision receipt | `producer/stage-c/revision-receipt.json`; revision identity `sha256:d2176cc2d2b8c09c…`, migration receipt `sha256:8298d68114929313…` |
| assessor's record | `sha256:90723d8fb9f97e2a…` |
| ratified form | `sha256:c4d001108edc5773…` |
| binding file | `sha256:ff172ee78de71833…` |
| governing protocol | `assessment/review-protocol-v3.4.json`, `sha256:d01538fbf6b4cbf5…` |
| superseded protocol | `assessment/review-protocol-v3.3.json`, `sha256:dddcc098e65e51e6…` |
| second boundary's archived work | `producer/stage-b/archive/2026-09-17T14:37:05Z`, 9 files, all matching |
| second boundary's record and ratified form | `sha256:d35ab5a9c7ec9015…`, `sha256:541130a46b541650…` |
| second boundary's binding file | `sha256:552592661bae1b4d…` |
| run manifest at close-out | `D0-MANIFEST.json`, `sha256:e32b0910…`, 177 artifacts, launched stages A, B and C |
| harness suite at close-out | 340 passed, 1 xfailed (the pinned packet defect) |

## One live refusal, and what it does not touch

The third boundary's producer ran the anchor command exactly as its procedure
writes it and was refused `SOURCE_ALREADY_ANCHORED` on `source:context`. The
runner names a retained source after the packet file's stem, and the builder had
staged the second and third boundaries' evidence under the same filename, so the
second anchor collided on the shared history. The refusal is typed and wrote
nothing. The producer copied the packet byte for byte inside its own workspace
and anchored it as `source:stage-c-context`; both files hash `d2ff1c6d`.

It is classified as a packet defect, not a producer deviation, and it cannot
reach the certificate: the boundary binds evidence by packet id and digest, and
the checker reads only the boundary and the reviews. That is proven by the run
above, not assumed. The one real consequence is that the id in the ledger
differs from the id in the boundary while the bytes are identical, so a reader
tracing the claim back must know that (E-0477, D0-REPORT.md addendum 16
section 3).

## What each result may be quoted for

**The third boundary's complete certificate.** May be quoted as: a
bounded demonstration that staged review happens and can be checked
mechanically, over five declared obligations, on the producer's own bytes with
nothing corrected. May **not** be quoted as a completion rate, a success rate,
or evidence that the checker accepts arbitrary producer output. One boundary,
one run.

**The counts 2/1/0/0 and 1/4/0/0.** May be quoted as: tallies of judgements,
three and five, with the obligations named. May **not** be quoted as an accuracy
score, a rate, a percentage, or a comparison against any other system. Protocol
v3.4 states this in terms: "A count is a tally of judgements, not a rate and not
a score." Eight judgements exist in total across two boundaries. There is no
denominator that makes them a rate.

**The `SATISFIED` verdicts.** May be quoted as: the structural gate and the two
named Prolog rules passed, with zero violations, on the facts each admission
produced. May **not** be quoted as semantic correctness, as faithfulness to the
source, or as evidence that the graph is right. Two domain rules are not an
oracle.

**The recorded ontology revision.** May be quoted as: a live history crossed one
explicit additive ontology revision by a named human decider, adding two classes
and re-binding the check contract with identical rule bytes, with the graph
byte-identical across it, the earlier check receipts intact, and a later
admission checked against the re-bound contract and recorded. May **not** be
quoted as general ontology migration, as policy migration, or as narrowing
support: narrowing and removal refuse with `NON_ADDITIVE_CHANGE`, and Core's own
status declares general policy migration absent (E-0458, E-0465).

**The two ratifications.** May be quoted as: the author read each record in full
and changed no judgement, with his decision bound to the record's digest. May
**not** be quoted as independent verification of the producer's graph, nor as
covering the certificate, which both binding files explicitly exclude.

**The replay results.** May be quoted as: the archived histories replay to their
recorded receipts and the exports come out byte-identical on the pinned Core
export. May **not** be quoted as model regeneration. Replay is replay.

## What this experiment does not establish

- **No comparison with authored fixtures.** Nothing here was run against a
  hand-authored expected graph as a baseline, and no such comparison may be
  reported from it.
- **No rate of any kind**, for the reason above.
- **Nothing about models in general.** Three producer sessions and two assessor
  sessions, one model, one domain, one chapter.
- **The first session is not a reviewed result.** The table population is
  PARTIAL, had no obligations, no assessor and no ratification, and its nine
  gaps are in a session log because the plan compiler would have refused them.
- **The second boundary has no certificate as produced.** Its reviews were
  refused by the checker on a packet defect. Quoting that boundary's counts is
  fine; quoting the run as mechanically complete at that boundary is not.
- **One modelling decision stands unresolved by evidence**: whether the
  correction relation should target the standing state record or the one it
  corrected. The assessor recorded it as the one judgement a human could
  reverse, and Luis ratified without reversing it. That is a recorded choice,
  not a verified one.
- **Three defects are carried, unfixed and pinned**, into any next case: packet
  filenames colliding per stage, the "as before" status instruction, and v3.4's
  explanatory note still counting three obligations. None of them affects the
  results above; the root-cause analysis is in
  `handover/2026-09-18-shop-third-case-rca.md`.

## Where the evidence lives

- Paper ledger `paper-v4/paper-ledger.md`, entries E-0433 to E-0480.
- Run report `private/shop-progressive-01/D0-REPORT.md`, addenda 1 to 17.
- Archived producer work, per boundary, under
  `private/shop-progressive-01/producer/stage-*/archive/`.
- Assessment packets and records under
  `private/shop-progressive-01/assessment/`.
- Binding files under `paper-v4/evaluation-v4/`.
- `private/` never enters git. The two binding files and this document do.
