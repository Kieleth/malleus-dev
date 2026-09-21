# Malleus: From Model Proposals to Replayable Knowledge

Luis Guzman Lorenzo. Author-review draft.

## Abstract

Malleus is a gate between what a language model proposes and what a knowledge
system accepts. A compiled ontology fixes the vocabulary. A source-located
intermediate representation carries every proposed value with the passage it
came from. An identified admission bundle checks the proposal against the exact
prior state. An append-only ledger retains what was admitted, and the graph is a
projection rebuilt by replay. We report the gate running on two kinds of input.
With no model in the loop, a transcribed published example crosses the whole
path as one connected history: 21 table rows, then 13 warehouse observations of
the objects those rows created and a labelled synthetic shipment cohort, each of
the two extensions entering through an additive contract revision and leaving
the earlier ledger as an exact prefix, with a correction retained rather than
rewritten and a candidate that would replace an admitted occurrence refused with
the ledger unchanged. With a model in the loop, six fresh
Claude Opus 5 sessions each proposed an ontology for one marine
geoscience article and populated it from the text layer without seeing any
evaluation question, and a seventh session populated one of those ontologies as
a fixed-ontology control. All seven populations were admitted, every history
reopens to its recorded graph, and 2,353 returned facts were audited against
their cited passages by a fresh Claude Opus 5 session per cell, which found
none unsupported; an
independent judge, Claude Fable 5.1, re-judged a random 200 of them blind and
agreed on 196, moving four to partial and none to unsupported. A
fault-injection control put 55 typed faults into one of those admitted
populations: 35 were refused at admission with a typed diagnostic and 20
admitted, 5 of them exposed afterwards by their own trace and 15 invisible
without reading the source. Of
102 required answer elements over 25 questions, the five graph results reviewed
under the corrected query binder reached 90 to 96; every absence is classified.
The same model answering the questions with the article in context reached
101 of 102. Reusing an unchanged graph for a second question set reached 88 of
102 without another capture, but used more reported tokens when model review
was included. These are bounded measurements of acquisition and reuse, not a
precision advantage or a demonstrated cross-session learning benefit. The public repository holds every pin,
isolation message, compiled ontology, admission and replay record and every
review judgement with its locator; recomputing the judgements needs the
article's text, which its licence keeps private.

## 1. What Malleus does

A language model can write a plausible typed record. Writing it does not make it
part of a system's accepted state. Malleus puts a boundary between the two. The
model proposes. Deterministic code compiles the proposal against a declared
contract, checks it against the exact state it assumes, and either admits it
atomically or refuses it with a typed reason. What is admitted goes into an
append-only ledger together with the evidence it cites. The working graph is
rebuilt from that ledger by replay and can be discarded at any time. What the
accepted vocabulary cannot carry is written down as a typed gap instead of
being dropped.

The gate is content-blind by design. It establishes that a record has the shape
the contract allows, that every value points at retained source bytes, and that
the history it entered can be reconstructed. It does not establish that the
record is true, that the ontology is adequate, or that the graph answers a
question. Those are separate claims, and this paper measures them separately:
structural admission by the compiler and the runner, faithfulness by a
source-grounded review of every returned fact, and sufficiency by coverage of
declared question requirements. Keeping the three apart is what makes a poor
answer diagnosable.

Four questions organize the evidence: can a model construct a useful ontology;
can it faithfully populate that ontology; can Malleus preserve and reconstruct
accepted changes; and can a reader retrieve and compose the information needed
for a task? Compilation answers only a structural part of the first question.
Source review addresses the second, replay tests the third, and declared answer
requirements test the fourth. None can stand in for the others. Persistent
semantic memory across sessions is the intended application; whether its
connections improve with use remains an empirical question.

## 2. The path in six terms

An **ontology** declares the legal record types, properties, relations and
controlled values. A **change set** is an immutable proposal binding ordered
operations to their evidence, their contract and the prior state they assume.
The **ledger** is the append-only history of admitted change sets and protocol
events. **Replay** reconstructs the accepted graph from the ledger under the
pinned implementation; the ledger registers the contract sources, the reading
and the capture as content-addressed artifacts, so nothing else is read, and
evolution of the ledger format itself is not addressed here. A
**locator** names the place in a retained source that a value was read from. A
**query** is a read over the replayed graph that changes nothing.

The ontology alone does not say what a ledger entry means, so the adopter
binds a history profile before population. The document runs use the
source-assertion profile: one capture is one atomic batch of assertions about
a document, declared partial, and neither a ledger timestamp nor a sentence
becomes an event in the world. The structured runs use the state-version
profile: a correction supersedes an older version and replay projects only
current versions.

For a document, the producer proposes a LinkML ontology over identified
domain-independent roots and three shipped vocabulary packs for research,
metrology and chronology. Compilation checks the structural contract and says
nothing about adequacy; one recorded event then accepts the ontology digest for
population. Population pairs proposed records with a capture: every assertion
names a reading block, carries a digest of its source wording and a modality,
and lists the record fields it formalizes; a typed gap records meaning the
producer could not express. The document adapter checks identities, locators,
digests and references between records and emits a neutral population plan,
over which the compiler enforces the ontology.

Admission checks the prepared change against the exact ledger head, the
retained source and evidence identities and structural application; the
outcomes are the runner's, never the model's, and a refused change leaves the
graph as it was. After admission the runner discards its live state, reopens
the ledger, replays it and compares receipt and exported records with what it
admitted. Queries return typed fields, digests and relation witnesses over the
replayed graph, and every returned record traces through its plan to the
assertion and block it was read from.

## 3. Results on the Small Shop

### 3.1 One connected history, with no model

The Small Shop is a controlled transcription of Fahland's chapter on event
knowledge graphs, a multi-object order-fulfilment example we did not design
([Fahland, 2022](https://doi.org/10.1007/978-3-031-08848-3_9)). Table 1 supplies
21 rows covering orders, inventory units, invoices, payments and supplier
orders; Figure 14 supplies 13 warehouse observations of the same units. Both
transcriptions are retained in the history with their exact bytes and with the
published images they were read from, adopter-authored plans map rows to
records, and nothing is generated. A command that reads the source without
populating anything assigns a disposition to each of the 123 nonempty fields in
those 21 rows and reports none unaccounted. The two sources enter one history,
in the stages below. Each stage checks the exact prefix it expects and refuses
before writing if it does not match, so a reader can run the chain twice and
compare bytes.

| Stage | Accepted changes / revisions | Ledger events | What the history holds |
| --- | ---: | ---: | --- |
| Table 1 population | 21 / 0 | 121 | Seventeen enduring objects, 21 occurrences and 62 qualified participations; 107 historical records, of which 106 are current; supplier order B at quantity 1 the one superseded record, quantity 2 current, and both source occurrences e4 and e7 retained; three typed source gaps where the table prints no usable date and no changed invoice value; 895,097 bytes. |
| Figure 14 warehouse extension | 34 / 1 | 193 | The same 17 objects, now carrying 34 occurrences and 75 participations; 133 historical records; one additive contract revision introducing only SCAN, STORE and RETRIEVE; the previous 895,097 bytes an exact prefix; 1,646,836 bytes. |
| Synthetic partial shipments | 37 / 2 | 216 | A separately labelled synthetic order with its own two units and two shipments, admitted into the same history through a second additive revision; 144 historical records; units not yet assigned to a shipment queried after each step as 2, 1, then 0; the previous 1,646,836 bytes an exact prefix. |

Counts are cumulative over the one history. Four properties of the gate are
visible here without any model.

A correction does not rewrite the past. Quantity 1 at source occurrence e4 stays
in the ledger as the one record the history supersedes, only quantity 2 at e7 is
projected, and both occurrences remain current events.

A second source joins the objects the first source created. Figure 14's X1 is
the inventory unit Table 1 unpacked, not a new object with a similar name, and
X1's displayed path becomes Unpack e10 at 04-05 11:00, Scan e12 at 13:00, Store
e13 at 13:15, Retrieve e22 at 07-05 11:15, Pack e27 at 17:00. The earlier bytes
are a prefix of the later ledger, not a regenerated approximation of it.

A vocabulary can grow without a new history. The three warehouse activity values
enter through one contract revision that makes three enum additions and nothing
else, and the four synthetic shipment classes and two slots through a second
that only adds. Each revision names as its base the contract identity the
records before it were admitted under, and it appends rather than rewriting
them.

A refusal costs nothing at admission. A candidate that replaces the
invoice-update occurrence e9 and its two participations, instead of adding to
them, is refused as TRANSITION_RULE_REFUSAL under the rule
REPLACEMENT_OUTSIDE_SHOP_STATE_ROLE, with the three refused record identifiers
named. The ledger bytes are identical from the start of admission to after it,
and the replayed graph and change sets are unchanged. Preparing that candidate
retains its evidence in an earlier separate transaction, and that retention
stays; the refusal rolls back admission, not preparation.

Reads run over the replayed history and append nothing. The per-object reader
returns 17 views over one registry of occurrences: invoice I2 shows creation e5,
update e9 and clearing e30, and that same e30 appears in the I1 and P1 views
rather than being copied into each. The ordering comparison asks, for the five
inventory units, whether the order in which they enter a warehouse stage
survives to the order in which they leave it. Five units make ten unordered
pairs per stage pair. Unpack to Scan preserves the order in 5 pairs, reverses it
in 1 and cannot compare 4; Scan to Store and Store to Retrieve each preserve 6
and cannot compare 4. The single reversal is Y2 over Y1: Y1 was unpacked at
07-05 10:45 and scanned at 15:00, Y2 was unpacked at 11:00 and scanned at 13:00.
Section 6.2 of the chapter reports the same overtake. The four Unpack-to-Scan
pairs that cannot be compared are the four involving X3, whose unpack time is
printed 00-01 10:30 and is unusable under the declared rule; in the other two
stage pairs they are the four involving Y1, which has no retained Store or
Retrieve observation. Every undetermined pair carries its reason, and a unit
with missing observations stays in the denominator.

What the fixture does not show matters as much. Printed times are retained as
text: no year, timezone, calendar instant or elapsed duration is derived, and
row order is a transcription coordinate rather than domain order. That no
comparable pair reverses in the other two stage pairs is not a first-in,
first-out certificate, and no cause of any delay is computed. Structural
admission alone does not reject a duplicate unit assignment, and the synthetic
cohort is labelled synthetic rather than presented as further chapter data.
Reopening any stage under the pinned implementation reproduces that stage's
receipt.

One refusal the connected history cannot express has its own fixture. A Prolog
rule retained in that fixture's own history and executed at admission gives 3
accepted changes and 31 ledger events, and the candidate assigning unit
SYN-PS-X1 to a second shipment is refused as VIOLATED with three witness records
and no admission bytes appended, after which the legitimate second unit is
admitted. That fixture needs SWI-Prolog, which the connected chain does not.

### 3.2 The same history, reconsidered by a model

Section 3.1 populates the Shop from adopter-authored plans. This subsection
answers a different question on the same chapter
([Fahland, 2022](https://doi.org/10.1007/978-3-031-08848-3_9)): when evidence
arrives about records that are already in the history, does a fresh model
session change what the evidence changes, keep what it does not, and say what
it cannot record, and can a reader check afterwards which it did?

Three fresh Claude Opus 5 sessions ran one after another on one growing
history. Each had no inherited context, its own workspace, a procedure naming
the interpreter and the pinned Core export, and the evidence for its own
instalment and no other. None was given a mapping from evidence to the
ontology. The first session populated the graph from the chapter's table; it
carried no obligations, no assessor and no ratification, so nothing below rests
on it, and it appears here only as the state the next two sessions inherited.
The second and third sessions each received a boundary, which is a frozen list
of obligations, an obligation being one declared interpretation the session
must review exactly once and answer CORRECTION, NO_CHANGE, CONFLICT or
UNRESOLVED. One further fresh session per boundary, neither producing the
result nor preparing the run, then judged every review as correctly changed,
correctly preserved, missed or spurious, and the author read each of those two
records in full and ratified it.

| Boundary | Obligations | Correctly changed | Correctly preserved | Missed | Spurious | Review-coverage certificate | Assessment protocol |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| second | 3 | 2 | 1 | 0 | 0 | not produced as run | version 3.3 |
| third | 5 | 1 | 4 | 0 | 0 | complete over the five reviews as written | version 3.4 |

Counts are tallies of judgements over the obligations each boundary declares.
They are not a rate, a score or a percentage: eight judgements exist across the
two boundaries, and there is no denominator that would make them one.

The second session was given three passages and three obligations. It answered
NO_CHANGE once and CORRECTION twice, and declared two gaps, of kinds
TYPE_ABSENT and RELATION_ABSENT, where the accepted vocabulary had no class and
no relation for what the passages state. Its corrections entered as two change
sets of five operations each. The third session was given one withheld passage
and five obligations, three of them re-declared from the second boundary over
records the second session had itself written. It answered NO_CHANGE four times
and CORRECTION once, declared one gap, of kind RELATION_ABSENT, and its
correction entered as one change set of two operations. Neither session rewrote
what it inherited: the first 22 lines of the second boundary's history are the
table population's history byte for byte, and the first 41 lines of the third
boundary's 50 are byte for byte the history it was handed.

Between the two boundaries the author grew the ontology on the live history as
one recorded act: two classes added, one for a correction explanation and one
for the relation from it to a recorded order state; the rule layer's check
contract re-bound in the same act, with the rule bytes unchanged and only the
ontology binding inside the contract moving; the graph byte for byte what it
was, compared against the previously archived export; the ledger going from 38
events to 41; and the four check receipts written before it still reading
SATISFIED and still naming the contract they were written under. That act is
identified by
d2176cc2d2b8c09cd84313bcd4b6926fae03faee4b63a89169b4d4bb72f232b5. It is one
additive revision with the rule layer re-bound, not ontology migration in
general and not policy migration.

Each result above tested one named layer and no wider one. Every SATISFIED
verdict in this run is the structural gate plus the two Prolog rules
NO_CONFLICTING_QUANTITY and NO_EMPTY_RECORD, run at admission over the compiled
facts of the candidate state under the check contract the history required; at
the third boundary's single admission that was 764 compiled facts and zero
violations. Completion is Core's review-coverage checker, which reads the
boundary and the reviews and nothing else, so nothing about the ledger's
contents follows from it. The four counts per boundary are one fresh assessor
session, judging one review per obligation against ground truth. The two
ratifications are the author reading a record in full, with the decision bound
to that record's digest.

The two boundaries differ on the certificate, and the difference is in the
preparation rather than in the checker. The second boundary's reviews carry the
boundary's name in the field where the checker requires the boundary's identity
digest, because the obligations file that session was given carried no such
digest. The checker refused them as written, so that run has no completion
certificate as produced; its counts stand, and its run may not be called
mechanically complete. The third boundary's obligations file carries the
identity beside the boundary. There the checker ran over the five archived
reviews exactly as the session wrote them, nothing corrected, and returned
complete, with nothing missing and nothing stale, one pending correction and
four unchanged.

| What it identifies | Boundary | Access | sha256 |
| --- | ---: | ---: | --- |
| the boundary the reviews had to cover | third | private | db3dc7d06e11cb1211f4c07f5f1ff5408e16deed58600c61795ea0eceef185d3 |
| the completion certificate | third | private | 5114bbb84314289230cab9bbe61cd89ec11d717599ffe2329b098fe06ea81fb7 |
| the recorded ontology revision | third | private | d2176cc2d2b8c09cd84313bcd4b6926fae03faee4b63a89169b4d4bb72f232b5 |
| the change set admitted there | third | private | eb6a47f880116372faca26ea7d4faf56932c1550417f03a4a1a6b7120bee21e7 |
| its check receipt | third | private | 0144c70864e8825efa78883849f4f2e8cef5ad3126b0c665a80fec485bf224ef |
| the archived history | third | private | 10dfda4ea9700390e7c31e2e07b2aee997df9e7b9f79c5fc8ba2f48600a9011e |
| the export replay reproduced | third | private | a175da0ba16d08eff5bc7c93d7100b72d7747099414cf23a6b4b930d6f866af7 |
| the assessor's record | second | private | d35ab5a9c7ec90157be62f4f1a1143afac00a79a8b8b607ad6b744980b92176b |
| the assessor's record | third | private | 90723d8fb9f97e2aeb0c8b0e64c394fc82e6616cd034677bc6225fae378420c5 |
| the author's ratification | second | public | 552592661bae1b4d27eb581f6fdccc91d7348e9c51da88c5a911c2e658d00cbc |
| the author's ratification | third | public | ff172ee78de718330c60f9e8f287fb28dd795695a9324fbd9ad11c5dc2238256 |

The two ratifications are public, for the
[second boundary](evaluation-v4/author-ratification-2026-09-17-shop-staged-review.md)
and for the
[third boundary](evaluation-v4/author-ratification-2026-09-18-shop-third-boundary.md).
Each names the record it ratifies by digest and states that the certificate is
a mechanical result recorded beside it and not ratified by it. The rest of the
table is private. The producer workspaces, the archives with a digest manifest
per file, the assessment packets and the two assessors' records are held under
private/shop-progressive-01 and are available to the author for verification.
They stay out of the repository because the evidence packets carry the
chapter's own sentences; what is printed here is identifiers, slot names,
mechanisms, counts and digests, and no passage of the chapter. The third
boundary ran against Core d5d014ba1d7e3bfe906bc71dc93ded5657a3b424 with
governance head OVR-000464, which the repository holds.

What this does not establish. No comparison with the adopter-authored fixtures
of Section 3.1 was run and none may be drawn from it. Three producer sessions
and two assessor sessions, one model, one domain, one chapter, say nothing
about models in general, and nothing here measures how often any of this
succeeds. Two domain rules are not an oracle: a SATISFIED verdict is shape,
identity, locator, digest and those two rules, not semantic correctness and not
faithfulness to the source. One modelling decision stands recorded rather than
verified, whether the correction relation should target the standing state
record or the one it corrected; the assessor named it as the judgement a human
could reverse, and the author did not reverse it. What the two boundaries
support is bounded: staged review of a model's own earlier records happened
here, and a reader can check that it did.

## 4. Results with a model: six captures and a fixed-ontology control

### 4.1 The condition

The source is Yu et al., *Deep mantle earthquakes linked to CO2 degassing at
the Mid-Atlantic Ridge*, published in *Nature Communications* in 2025
([Yu et al., 2025](https://www.nature.com/articles/s41467-024-55792-9)). One
pinned text-layer reader projects the eleven-page PDF into 186 identified
blocks. Figures, tables and supplements are outside the reading.

Each cell is one fresh Claude Opus 5 session with no inherited context, pinned
to one Malleus commit (c95dba7, contained in release 0.14.0), given eight
declared inputs: the selected reading, the root ontology and LinkML types, the
three packs, the source-assertion profile and the installed Malleus skill. It
never sees the evaluation questions, any earlier run, the repository or the
network. Phase one proposes an ontology; a compilation refusal returns its
diagnostic to the same session at most twice. After one recorded acceptance
event, phase two proposes the population in the same session; the runner may
return a structural refusal at most twice, and a third is terminal. No one
edits the model's output, and a partial or refused result is a valid result.
Six cells ran under this condition: run-20 to run-24 and run-26. Run-25 is a control that
changes one thing: the producer receives run-23's accepted ontology as a ninth
input and starts at population, so the population stage is measured without
ontology authorship; it binds the current question file. Run-26
repeats the record condition and is the first graph cell reviewed under the
protocol's next version, whose absence codes separate a vocabulary that has no
place for an element from a producer that did not use the place it had. A
separate session is
the baseline of Section 4.9: the same model with the article's text in context
and the thirty questions visible, answering in prose with block citations and
no Malleus at all. Eighteen earlier
development cells under changing harness versions are retained in the
repository and are not reported here.

### 4.2 Questions and review

Thirty questions were authored from the article, frozen before run-22, and
never shown to a graph producer. A control-only revision preceded run-24;
the positive questions stayed unchanged. Twenty-five are positive, five in each of five tiers: direct
facts, relationships, quantities, qualifications and composition. Each carries
three to five required answer elements, 102 in all. Three are controls that ask
for information the reading does not carry, and two are paraphrases that must
match their source question. Questions bind to the graph through type sets
named from the accepted ontology alone; a binding cannot name a document
value, a record identifier or a locator.

One fresh Claude Opus 5 session, the same model family as the producers,
reviews each reported query result under its frozen protocol.
Every distinct returned witness is judged once for source support against the
block its locator names and not against the article around it, so support is
block-local: SUPPORTED, PARTIAL, UNSUPPORTED or NOT_EVALUABLE. Every required
element of every question either names a returned row or carries an absence
cause: under v3, NOT_MODELLED combines a missing type or slot with a slot left
unset. Version 3.2 separates these as NOT_MODELLED and NOT_CAPTURED;
run-26 and the baselines use that version. Other causes are WITHHELD_STATEMENT when the answer sits inside a retained sentence the graph
holds only as a digest, UNREACHED_RECORD when the record exists but the query
did not reach it, and NOT_IN_SOURCE for the controls. A question is COVERED
when every element names a row, NONE when none does, PARTIAL otherwise. The
label is derived by a validator from the coverage entries; a reviewer cannot
write it directly. The validator also checks that every locator resolves. The
first two cells were reviewed under an earlier protocol over four questions and
per-row support, and the author ratified those records; the author read the
five later graph-result reviews in full and ratified them
([record](evaluation-v4/author-ratification-2026-09-16.md)). One written clarification, that
a returned row names a required element only for the question's own subject,
was added after the first review of run-22's re-queried result and applied to
its second; both records are retained (Section 4.4).

### 4.3 Admission and replay

| Cell | Ontology facts | Entities / relations | Declared gaps | Runner attempts | Ledger events | Reopen equals admission | Producer tokens |
| --- | ---: | --- | ---: | ---: | ---: | --- | ---: |
| run-20 | 4,314 | 426 / 55 | 77 | 2 | 14 | yes | 433,787 |
| run-21 | 3,780 | 508 / 26 | 94 | 1 | 14 | yes | 387,470 |
| run-22 | 3,664 | 443 / 31 | 15 | 1 | 14 | yes | 567,044 |
| run-23 | 4,152 | 417 / 22 | 20 | 1 | 14 | yes | 382,781 |
| run-24 | 5,032 | 400 / 21 | 153 | 1 | 14 | yes | 390,045 |
| run-25, fixed ontology | 4,152 | 477 / 57 | 14 | 1 | 14 | yes | 384,287 |
| run-26 | 4,219 | 445 / 152 | 11 | 1 | 14 | yes | 461,468 |

All six fresh ontologies compiled at the first attempt, which says that this
producer under this skill writes schemas the compiler accepts, not that the
schemas are adequate. Five fresh populations were admitted at the first runner
attempt; run-20 was refused once on a structural defect, corrected by the same
session, and admitted at the second. The control's population, on run-23's
ontology, was admitted at the first attempt. Refusals are not ledger events: the ledger
is the history of acceptances, and a refused change is retained by the harness
with its typed diagnostic and the state it was refused against, as run-20's is.
In all seven populations, reopening the ledger and replaying it reproduces the admitted
receipt and the exported records exactly. Every one of the 186 reading blocks
was either asserted from or declared to carry nothing assertable, by the
producer's own account. Every admitted record traces to the capture assertion
and the block it was read from. Records of the assertion families (claims,
observations, counts, ratios) also carry the digest of their sentence; entity
records of the other families (a campaign, an instrument, a published work)
carry their locators through their trace derivations and no digest. Tokens are
harness-reported per cell; run-22's figure includes a launch that was set aside
and relaunched.

### 4.4 Review

Columns: elements reached of 102 over the 25 positive questions; witnesses
SUPPORTED / PARTIAL; positive questions covered / partial / none; absences by
cause; controls matched of 5. The fifth column pairs two codes. Five cells were
reviewed under a protocol with one code, NOT_MODELLED, for an element nothing
in the graph carries, and no code at all for the case where the accepted
contract had a place and the producer did not use it, which is why they read
"and no code". Run-26 was reviewed under the next version, which separates
them.

| Cell | Reached | Support | Covered / partial / none | Not modelled or captured | Withheld | Unreached | Controls |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: |
| run-22, v4.12 binder | 82 | 449 / 0 | 12 / 12 / 1 | 7 and no code | 2 | 11 | 4 |
| run-22, v4.13 binder | 90 | 457 / 0 | 14 / 11 / 0 | 7 and no code | 3 | 2 | 5 |
| run-23 | 92 | 422 / 6 | 16 / 9 / 0 | 8 and no code | 2 | 0 | 4 |
| run-24 | 90 | 405 / 11 | 15 / 10 / 0 | 5 and no code | 7 | 0 | 5 |
| run-25, fixed ontology | 93 | 500 / 5 | 16 / 9 / 0 | 5 and no code | 4 | 0 | 5 |
| run-26, under the next protocol | 96 | 545 / 2 | 19 / 6 / 0 | 0 and 5 | 1 | 0 | 5 |

Run-22 appears twice. Its ledger, ontology and type sets are unchanged; the
second row re-queries the same history under the corrected v4.13 binder
(Section 4.7), and a fresh session reviewed the result. Two reviews of that
result are retained. The first counted a required element as named by any
returned row's fields and read three no-answer controls as PARTIAL: 93 of 102,
controls 2 of 5. A written clarification of the protocol, that a row names an
element only for the question's own subject, was then applied by a second
fresh session: 90 of 102, controls 5 of 5. Support was 456 and 457 of 457 in
the two readings. The row reports the second. Run-20 and run-21, reviewed
under the earlier protocol over four questions, returned 417 of 434 rows and
471 of 490 rows SUPPORTED, the remainder PARTIAL and none UNSUPPORTED, with
three and one of the four questions responsive.

The fixed-ontology control probes whether repeating population under one
accepted ontology changes coverage. One such pair cannot isolate a general
causal effect of ontology authorship.
Run-25's producer, given run-23's ontology and nothing else new, proposed 535
records against run-23's 440 and 57 relations against 22, asserted from all 186
blocks and declared 14 gaps against 20. Its review found 500 of 505 witnesses
SUPPORTED and five PARTIAL, at block boundaries and map-legend words, with all
five controls matched. It reached 93 of 102 against run-23's 92. This pair changed the
modelling much more than the observed coverage. Its five NOT_MODELLED absences
are of the kinds run-23 shows: two missing evidence relations, one claim without
a subject, two claims without a disposition, although the ontology declares
those slots and the pack the relation types. Of its 57 relations, 27 are
contribution credits, and none is SUPPORTS or CHALLENGES.

Run-26 separates the two absences that the earlier protocol had to write as
one. Reviewed under the next version, it records NOT_MODELLED nowhere and
NOT_CAPTURED five times: the accepted contract had a type or slot for a
repository name, a source study, a quantity's subject and, twice, a relation
from an observation to the claim it supports, and the producer proposed none of
them. Under the earlier protocol all five would have shared the NOT_MODELLED code,
which combined missing vocabulary with unused vocabulary. The new code makes
the reviewer's distinction explicit. It remains a semantic judgement, not a
compiler proof that every omission has been correctly classified.

The same cell also settles what the missing relations are not. Its producer
proposed 152 relations, seven times run-24's 21 and nearly three times the
fixed-ontology control's 57, and lost the same three composition elements as
every other cell. Run-26 contains 2 SUPPORTS relations, connecting
depth-resolution tests to claims about the reliability of the reported depths.
Both were judged supported. Neither supplies the evidence links requested for
the degassing or cold-lithosphere arguments. This is selective omission, not a
complete failure to capture evidence links. The contrast provides a positive
control for further investigation, not its complete causal explanation.

### 4.5 Faithfulness

Across the graph cells the paper reports, 2,353 distinct witnesses were judged
and 24 were PARTIAL; none was UNSUPPORTED. The partials are of two kinds and
no others: a text-layer block boundary cutting the sentence a record was read
from, so the cited block carries the value but not the words that name it, and
a producer typing a record more specifically than the block warrants, for
instance a fault typed as normal where the block says faults, or a named
volcano narrowed to a volcanic cone the block never describes. Two cells are
nearly free of them: the re-queried run-22 records none at all over 457
witnesses, and run-26 two over 547. Every statement digest recomputed against its block
matched. For the first five fresh ontologies, every cited external vocabulary, 20
URLs in all, was fetched and found to exist and to carry the borrowed terms.

Because the reviewer is the producers' own model, an independent judge of a
different model, Claude Fable 5.1, re-judged a sample blind to the recorded
labels, one fresh session per stratum, under the same block-local rule. The
first stratum is a seeded random draw of 200 witnesses the reviewers had
labelled SUPPORTED, proportional across run-22 under v4.13, run-23, run-24 and
run-25: the judge agreed on 196 and moved four to PARTIAL, one per cell, and
none to UNSUPPORTED. With four of 200, the one-sided 95 percent upper bound on
the rate of witnesses the reviewers over-labelled is 4.5 percent; for
UNSUPPORTED, none found, it is 1.5 percent. The second stratum is every one of
the 22 witnesses the reviewers labelled PARTIAL: the judge agreed on 18 and
moved four to SUPPORTED, none to UNSUPPORTED. Kappa is uninformative on
strata built from one label and is not reported; the sample files, both judge
records and the dispatch log are public. This is a second model opinion on a
sample, not human ratification.

The gate does not enforce this. The digest check proves that the cited
sentence exists in the cited block; it does not prove that the value follows
from it, and a producer could attach a real sentence to a fabricated field and
pass admission. What the locator and digest do is make every value auditable
against one sentence, and the initial reviews labelled none unsupported. Zero UNSUPPORTED is
therefore a property of these producers under this skill, observed through the
gate, not a property of Malleus. The PARTIAL judgements are what the audit
exists for: a qualification lost inside a well-formed record, made visible by
the locator rather than prevented by it.

### 4.6 Injected faults

Seven populations admitted with one structural refusal between them is not on
its own evidence that the gate did anything: a gate that refuses everything and
a gate that refuses nothing both look careful when the producer was careful. To
manufacture the counterfactual, 55 typed faults were injected into run-23's
admitted capture and records, one per trial, and each faulted population was
put through run-23's own runner against the same Malleus commit the cells were
pinned to. Each class is constructed against the mechanism the code designates
for it, and the outcome that mechanism implies was recorded before any trial
ran.

| Injected fault | Designed catcher | Trials | Observed outcome |
| --- | --- | ---: | --- |
| VALUE_NOT_IN_BLOCK | none, review only | 5 | Admitted, invisible |
| LOCATOR_REPOINTED_STALE_DIGEST | digest binding | 5 | Refused, DIGEST_MISMATCH |
| LOCATOR_REPOINTED_COHERENT_DIGEST | trace derivation | 5 | Admitted, exposed by the trace |
| LOCATOR_REPOINTED_COHERENT_DERIVATION | none, review only | 5 | Admitted, invisible |
| DIGEST_MISMATCH | digest binding | 5 | Refused, DIGEST_MISMATCH |
| DANGLING_ENDPOINT | admission structural check | 5 | Refused, DANGLING_ENDPOINT |
| TYPE_OUTSIDE_ONTOLOGY | compiler | 5 | Refused, RECORDS_NOT_REHYDRATABLE |
| SLOT_OUTSIDE_ONTOLOGY | compiler | 5 | Refused, RECORDS_NOT_REHYDRATABLE |
| DUPLICATE_RECORD_ID | admission structural check | 5 | Refused, MALFORMED_CAPTURE |
| RECORD_WITH_NO_SOURCE_WITH_FIELDS | admission structural check | 5 | Refused, UNDERIVED_FIELD |
| RECORD_WITH_NO_SOURCE_NO_FIELDS | none, review only | 5 | Admitted, invisible |

Of the 55, 35 were refused at admission, each with a typed diagnostic. In 30 of
those the refused ledger is a byte-exact prefix of the honest run's, and the
other 5 differ only in the event that retains the evidence, because those
faults mutate the capture the run retains. Twenty were admitted. Five of the
twenty are exposed afterwards by the record's own trace, which derives the
record from an assertion other than the one the record cites; the remaining 15
are invisible to every check a reader can run without going back to the source,
and they are three classes. VALUE_NOT_IN_BLOCK is a well-typed value the cited
sentence does not contain. LOCATOR_REPOINTED_COHERENT_DERIVATION moves a
record's locator, its digest and every formalization of it together onto one
sentence in another block. RECORD_WITH_NO_SOURCE_NO_FIELDS carries no property
at all, so nothing in it is a field for which a derivation is required. The
digest binding that refuses two of the classes is optional: it is declared on
five record types and covers 236 of run-23's 440 records, because this producer
filled both slots wherever its types had them. This is a property of the
structural gate alone, which reads shape, identity, locator and digest; nothing
on the path that gate defines compares a value with the sentence behind it. The measurement is bounded in four further ways. It
faults run-23 and no other cell. It stops at admission: no query and no review
was run over any faulted graph. It exercises the structural gate without Core's
rule layer or any logic check, neither of which was applied to these faults.
And the seven classes are ours, so a fault this catalogue does not construct is
not evidence about anything.

### 4.7 Coverage and its absences

The eleven unreached elements in run-22 under the v4.12 binder were an
evaluator defect: a type set that named a claim type reached only claims
without a subject, and the claims stating the preferred hypothesis all carry
one. The binder was corrected before run-23. Re-querying run-22's unchanged
ledger under it, with a fresh reviewer, moves the cell from 82 to 90 of 102
and its controls from 4 to 5 of 5, and leaves two unreached elements that are
the evaluator's type sets for two questions, not the binder; run-23 through run-26 have none. What remains is the producer's. NOT_MODELLED under this protocol covers more than one case,
so the 25 such absences of the four reported cells were re-derived from the
frozen artifacts, with the records untouched and an evidence pointer per fact:
6 where the accepted contract declares no type or slot, such as a journal
acceptance date; 1 where the slot exists and the graph holds no entity for its
referent; 5 where the slot and the entity both exist and the slot is unset
because the entity's name or tag does not occur in the formalizing sentence,
which the skill's subject rule would have refused; and 13 that the four cases
cannot decide, whole records or relations rather than slot values, an
enum-ranged slot, or a gap the capture declared at a range or block boundary,
where the recorded code stands. All 16 WITHHELD_STATEMENT absences are the
element held only as a digest. The protocol's next version adds a reviewer
code for the second and third cases and a checklist that names, for every
check, its condition, its verifier and where its outcome lands. Because fresh ontology construction was question-blind, a missing slot
measures what this producer chose to represent, not a universal vocabulary
limit. Missing evidence links are different: the research pack offers SUPPORTS
and CHALLENGES. Run-26 uses SUPPORTS for the depth-reliability claims described
above; the other four graph results in this coverage comparison use neither
predicate. Its review identifies two different, unrepresented argument links
as NOT_CAPTURED, not missing vocabulary. WITHHELD_STATEMENT is an answer that exists
in the graph only as the digest of a sentence the producer chose not to
decompose. Where the producer noticed an omission it is a typed gap recorded at
capture; where it did not, nothing marks it, and block coverage is the
producer's own account. Recall is measured only through these 25 authored
questions.

The two not-in-source controls read NONE in every cell. The two paraphrases
matched their originals in every cell. The excluded-surface control asked for
per-site values that live only in a figure and its supplementary table, and
in run-22 and run-23 it read PARTIAL because one sentence in the text names
the compilation those values come from; the question was re-authored to drop
that element before run-24, where it reads NONE. Under the subject-tie
clarification the re-review of run-22 reads it NONE with the v3 wording too.

### 4.8 What varies is the modelling

The gate is stable and the producers are not. The first five sessions under one
condition proposed 55, 26, 31, 22 and 21 relations and declared 77, 94, 15, 20
and 153 gaps. Run-24's producer declared 137 gaps of one kind, type absent, and
gave 48 records a subject where run-23's gave 96; both are honest under the same
skill and they are different modellers. The protocol does not make models agree
on what to represent. It makes what they represent auditable against its
source, replayable, and measurable against declared requirements.

Coverage is also not an assembled answer. In 20 or 21 of the thirty questions
in run-22 under the corrected binder, run-23 and run-24 the elements that answer a question sit in separate rows that nothing
in the graph joins. The composition tier makes this concrete: run-22 under the
corrected binder, run-23 and run-24 all return the preferred mechanism, the
calculated CO2 content and the observed earthquake depths, and none returns a
relation that says one supports the other, because no producer proposed one.
The graph holds the pieces and the reader does the composition. Appendix A.3
prints the rows.

### 4.9 The fresh-context comparison

A baseline prices the path. One fresh Claude Opus 5 session received the same
selected reading and the thirty questions, with no ontology, no skill, no
graph and no admission, and answered each question in prose with the reading
blocks it rested on: 135 cited claims over 30 answers, three of them declaring
that the reading carries no answer. The same review protocol judged it, on a
third evidence surface whose witness is one cited claim rather than a graph
record; support is block-local and coverage is counted over the same 102
required elements.

| Measure | Graph cells | In-context answers | Reading |
| --- | ---: | ---: | --- |
| elements reached of 102 | 90 to 96 | 101 | The answers reach nearly every element; the one they miss is an instrument never named. |
| positive questions covered of 25 | 14 to 19 | 24 | An element unreached in a graph cell is usually a relation or a subject the producer did not propose. |
| witnesses supported / partial | 2,329 / 24 | 130 / 5 | Counts are not comparable: a graph record and a cited claim are different units. |
| controls matched of 5 | 4 or 5 | 5 | Descriptive only: control wording and whole-answer abstention differ. |
| producer tokens | 382,781 to 567,044 | 127,303 | Harness-reported per session. |

The comparison is one-way and we state it plainly: reading the article with the
questions in hand answers more of them, more cheaply, than building a graph
from it question-blind. Where the two differ is not spread evenly over the
questions.

| Question tier | Graph cells | Answers | Where the difference is |
| --- | ---: | ---: | --- |
| direct facts | 12 to 16 of 16 | 15 of 16 | The best graph cell reaches all sixteen; the answers miss an instrument they never name. |
| relationships | 16 to 19 of 20 | 20 of 20 | The graph loses a spatial relation and an ordering it holds only as a sentence. |
| quantities | 21 to 23 of 23 | 23 of 23 | Two of the five graph cells lose nothing at all. |
| qualifications | 17 to 20 of 20 | 20 of 20 | The graph loses a disposition and a subject its own contract declares a slot for. |
| composition | 20 of 23 in every cell | 23 of 23 | True of all five cells, including the one that proposed 152 relations. |

Several persistent gaps concern relationships rather than numerical values.
On quantities two of the five graph cells reach
every element, and on direct facts the best of them reaches one more than the
answers do, question-blind against a baseline holding the questions. In this question set, a recurring loss is the link between values: every cell loses the same
three composition elements, and the relationship and qualification losses are
a spatial relation, an ordering, a disposition and a subject, each of them a
join the producer did not propose rather than a number it got wrong.

The support counts describe different units: 24 PARTIAL judgements among
2,353 graph witnesses and five among 135 prose claims. This does not establish a precision advantage.
The baseline's partials include a misplaced processing order and an incorrect
comparison between a depth and a depth band. Structured fields make scope and
attribution inspectable, but a typed field can still attach a correct value to the wrong subject.
Neither admission nor a matching sentence digest rules that out.

The baseline answer file contains prose and citations, not an admitted history
with replay, supersession or typed capture gaps. Those are differences in the
implemented workflows, not impossibilities for systems built around prose.
The graph producers used roughly three to four times the reported session
tokens of this baseline. This is not an isolated cost of admission: it includes
question-blind ontology construction and population, whereas the baseline saw
the questions. Session totals are not split into input, output, cache and
reasoning tokens, and do not establish monetary cost or a reasoning budget.

### 4.10 Reusing the same graph for new questions

A second source-only author, blind to the graphs and the first question set,
produced another thirty questions with 102 required elements over 25 positive
questions. We supplied manual query bindings against run-23's existing ontology
and queried its unchanged graph. No new ontology or population was produced.
The graph reached 88 of 102 elements and fully covered 15 of 25 positive
questions; a fresh-context baseline reached 101 and fully covered 24. The
original graph's first-set result was 92 of 102. Equal denominators do not make
the question sets equally difficult. These are results of a graph, questions,
reader and assessment together, not a graph's intrinsic accuracy.

| Measure, second question set | Existing graph | Fresh-context answers | Interpretation |
| --- | ---: | ---: | --- |
| elements reached of 102 | 88 | 101 | Model-assisted coverage, no recapture. |
| positive questions covered of 25 | 15 | 24 | Finding required elements, not necessarily linked composition. |
| new producer tokens | 0 | 124,886 | Graph side additionally required manual bindings and query execution. |
| review tokens | 459,121 | 202,886 | Review workloads differ: 429 graph witnesses and 102 prose claims. |
| producer plus review tokens | 459,121 | 327,772 | Graph total is 1.40 times the baseline, excluding shared question authorship. |

The query returned 7,433 rows; 21 of 30 questions had their answer elements in
unlinked rows. All 21 elements in this set's composition tier were reached,
unlike the three missing elements in the first set. This establishes neither
better composition nor a regression: the requirements differ.

Three absence controls mistakenly included a required element present in the
reading. Their partial graph answers are not evidence of fabrication.
The prose grammar also permits whole-question abstention that removes every
claim, whereas the graph can return a valid partial answer. These controls are
retained but excluded from comparative conclusions. Positive-question results
are reported separately. A subsequent pre-freeze check requires a source-bound
assessment of each control element; code checks its completeness and consistency,
not source entailment. Historical questions and reviews are unchanged.

No break-even point was measured. Avoiding recapture saves that stage, but
manual binding remains, and including model review makes this second-set
workflow more costly in reported tokens. A fourth-query-set crossover would
be an extrapolation with incomplete costs and different answer coverage.
This is a demonstrated reuse of accepted state, not a measured cross-session learning benefit.
Growing connections through subsequent use remains future work.

## 5. Check it yourself

The repository is public and the package is on PyPI as malleus-dev 0.14.0.
Every cell in Section 4 has a public directory under paper-v4/experiment-v4
with the harness, the run contract and its Malleus pin, the producer spawn
message and input manifest, the accepted ontology with its validated contract,
and the run result, census, launch log, query bindings, trace summaries, token
usage and the list of withheld files with their digests. The review records are
public under paper-v4/evaluation-v4 and the thirty questions under
paper-v4/experiment-v4. Run-22's re-query under the corrected binder, both of
its review records, the run-25 control and the baseline of Section 4.9, with
its answer grammar, validator, producer task and review record, are public
under the same directories, with the
[clarification](evaluation-v4/review-task-v3-clarification-2026-09-12.md)
applied to the second. The Small Shop runs from the repository with no
private input; Appendix B names the commands.

Eight files are withheld per cell because they reproduce the article's text:
the producer's capture and its retained form, the population plan, the exported
and replayed records, the gap statements, the ledger and the query results. The
article states its licence, CC BY-NC-ND 4.0, in its own text on its last
page, and redistributing a derived text layer needs a rights decision we have not
taken. Each withheld file's digest is public, so a reader who obtains the
article and the pinned reader can regenerate the reading and check the
digests. Source-bearing artifacts remain private; the public files alone do not
replay a document ledger. They let a reader verify that every review label was
derived from its coverage entries, that every locator names an existing block,
that every cell's reopen matched its admission and that no producer saw a
question; they do not let a reader recompute a support judgement, which needs
the sentence.

## 6. Related work

Schema-guided extraction with a language model is established. SPIRES extracts
schema-conforming instances against LinkML schemas fixed by domain experts
([SPIRES](https://arxiv.org/abs/2304.02711)), and OntoLogX validates generated
graphs and returns diagnostics to the model before persisting
([OntoLogX](https://arxiv.org/abs/2510.01409)). Malleus claims neither
structured generation nor the diagnostic loop. The closest priors for the
source-assertion profile are nanopublications, an assertion packaged with its
provenance and publication information under a content-based identifier
([Groth et al.](https://doi.org/10.3233/ISU-2010-0613),
[Kuhn and Dumontier](https://doi.org/10.1007/978-3-319-07443-6_27)).
Micropublications and SEPIO model the claim-to-evidence relation that Appendix
A.3 reports absent, and the research pack's SUPPORTS and CHALLENGES types are
borrowed from them ([Clark et al.](https://doi.org/10.1186/2041-1480-5-28),
[Brush et al.](https://ceur-ws.org/Vol-1747/IT605_ICBO2016.pdf)). Wikidata's
statement ranks are the precedent for the PREFERRED disposition
([Vrandečić and Krötzsch](https://doi.org/10.1145/2629489)). What Malleus adds
is a recorded decision between structural validity and acceptance, a locator
required on every value before admission, and replay from one ledger. OTTR
supplies typed graph-construction templates ([OTTR](https://ottr.xyz/)); Blue
Brain Nexus validates on write, keeps an event log and rebuilds indexes by
replay ([Sy et al.](https://doi.org/10.3233/SW-222974)); ESAA separates agent
intentions from validation, persistence and projection
([ESAA](https://arxiv.org/abs/2602.23193)). PROV-O is the standard provenance
vocabulary ([PROV-O](https://www.w3.org/TR/prov-o/)); the trace derivations
here are not emitted as PROV terms. The support scale follows attribution
studies that use human raters, AIS ([Rashkin et al.](https://doi.org/10.1162/coli_a_00486))
and ALCE ([Gao et al.](https://arxiv.org/abs/2305.14627)); ours is
model-assisted and block-local. There is no matched retrieval baseline
([Lewis et al.](https://arxiv.org/abs/2005.11401)); the query region records
zero source-file reads and zero embedding imports, a mechanical fact about these
executions and not a comparative claim.

## 7. Limits and conclusion

One article, one model family and one skill do not establish general extraction
quality, and six fresh captures plus one control are not a statistical comparison. The
control fixes one model-authored ontology; it does not test an expert-authored
schema. The baseline is one session on one article with the questions visible;
it is a favourable fresh-context reference result, not an estimated maximum
or proof that in-context reading generalises to a larger corpus. Calling it a
calibration ceiling describes this comparison, not a measured upper bound. The review is
model-assisted, by the producers' own model family, which is the setting in
which model judges are known to favour their own outputs; the first two cells
were ratified by the author and the author read the five later graph-result reviews in full and ratified them; the baseline and reuse reviews are not ratified. Control expectations
were visible in some review sessions, including run-26. Run-26's reviewer also recorded
the threshold it applied, counting an element carried in a record's name or
scope field as naming a semantic; a stricter reading requiring the typed slot
would move three of its questions from covered to partial. Two fresh sessions
of that model judged run-22's
re-queried result before and after the protocol's subject-tie rule was written
down: 93 against 90 of 102 elements, 2 against 5 of 5 controls, and 456
against 457 of 457 witnesses SUPPORTED. The written rule, not the model, fixed
the controls. The independent judge of Section 4.5 is a different model from
the producers but the same model as the author's assistant that dispatched it,
and its reasoning effort was the harness default. Coverage of
required elements is not a correct assembled answer. Faithfulness to the
selected reading is not geoscientific truth. The Small Shop transcribes a
published example; its shipment cohort is synthetic and labelled so, and its
rules are an adopter's choice, not a Malleus invariant. Single-process replay
does not demonstrate concurrent writers or cross-language conformance.
Robotics simulation is a candidate application, not evidence in this paper.

Long-context research motivates testing persistent memory, but does not supply
missing Malleus results. Du et al. report degradation with increasing input length
even when relevant information is retrieved ([Du et al.](https://arxiv.org/abs/2510.05381)).
BABILong tests reasoning across facts embedded in long distractor texts
([Kuratov et al.](https://arxiv.org/abs/2406.10149)).
Lost in the Middle demonstrates sensitivity to evidence position
([Liu et al.](https://arxiv.org/abs/2307.03172)).
Laban et al. compare fully specified single-turn tasks with simulated
multi-turn instruction delivery, not repeated questions about one loaded article
([Laban et al.](https://arxiv.org/abs/2505.06120)).
These studies concern their own models and tasks. They do not show that our
baseline deteriorates across sessions, that Malleus avoids such deterioration,
or that document tokens can be subtracted from session totals to measure reasoning.

What the evidence supports is narrow and, we think, useful. A model's
proposals can cross a gate that refuses what it cannot type, binds every value
to the bytes it came from, admits atomically, and reconstructs its accepted
state from its history under a pinned implementation. Under that gate an audit
of every returned fact found none unsupported, and what the producers left out
is classified. The gate guards form and lineage.
Injecting 55 typed faults into one admitted population measures where that
boundary falls: 35 were refused with a typed diagnostic and 20 admitted, 15 of
them invisible to any check that does not read the source. That is the
structural gate alone; Core's rule layer, which the Small Shop exercises, was
not applied to these faults.
Content remains the producer's, and measuring it separately is what lets a
reader see which is which.

## Appendix A. Worked evidence from run-23

Run-23 is the illustrative cell for these exhibits, not the highest-coverage result. JSON exhibits are exact subsets of
its retained query results and review record; keys and values are unchanged and
omitted fields are omitted, not null. Source excerpts are from Yu et al. (2025),
DOI 10.1038/s41467-024-55792-9, under CC BY-NC-ND 4.0, with whitespace collapsed.
Block identifiers name the pinned text layer.

### A.1 A supported count and its trace

**Question CQ-T1-02.** How many ocean-bottom seismometers were deployed? The
count row is:

```json
{
  "kind": "SUBJECT",
  "record": {
    "count": 19,
    "count_scope": "ocean-bottom seismometers in the network that acquired the microseismicity data",
    "assertion_modality": "STATED",
    "assertion_locator": "assertion:039"
  },
  "witness": {"record_id": "cnt:obs-deployed", "subject_id": "instr:obs"}
}
```

The capture binds assertion:039 to block page:2:block:002, whose text reads
“The microseismicity data were acquired by a network of 19 ocean-bottom
seismometers (OBSs) during the SMARTIES cruise in 2019”. The review judged the
witness SUPPORTED and the question COVERED: the count, the instrument and the
cruise each name a row. It also recorded that nothing in the result joins the
three rows; the assembly descriptor is UNLINKED_ROWS.

### A.2 A qualified hypothesis

**Question CQ-T4-01.** Which explanation do the authors prefer, and how strongly
do they claim it? One row carries the answer:

```json
{
  "kind": "SUBJECT",
  "record": {
    "claim_kind": "proposed mechanism",
    "hypothesis_disposition": "PREFERRED",
    "assertion_modality": "HYPOTHESISED",
    "assertion_locator": "assertion:007",
    "subject": "geo:rc2"
  },
  "witness": {"record_id": "claim:co2-degassing-deep-eq", "subject_id": "geo:rc2"}
}
```

Assertion:007 is bound to page:1:block:001, the abstract, which reads “we
suggest that deep earthquakes in the mantle result from the degassing of CO2”.
The modality HYPOTHESISED and the disposition PREFERRED are fields the producer
chose from the research pack's closed vocabulary; they identify the authors'
proposal, not an established cause.

### A.3 The pieces of a composition, unjoined

**Question CQ-T5-01.** Which volatile-content observation and which
earthquake-depth observation are brought together to support the degassing
hypothesis? The result returns the mechanism claim of A.2 and these two
quantities, among others:

```json
{
  "record": {
    "analyte": "CO2",
    "assertion_modality": "CALCULATED",
    "melt_stage": "PRIMARY_MELT",
    "unit": "wt%",
    "value_lower": 0.4,
    "value_upper": 3.0,
    "subject": "geo:rc2",
    "assertion_locator": "assertion:118"
  },
  "witness": {"record_id": "gchem:rc2-co2-primary-calc"}
}
```

```json
{
  "record": {
    "assertion_modality": "MEASURED",
    "unit": "km",
    "value_lower": 16.0,
    "value_upper": 19.0,
    "subject": "geo:rc2",
    "assertion_locator": "assertion:062"
  },
  "witness": {"record_id": "obs:deep-eq-rc2"}
}
```

Block page:5:block:005 gives the calculated content as 0.4 to 3.0 wt% for
segment RC2, and block page:2:block:006 reads “we observed deep earthquakes
(16–19 km) beneath the segment RC2 axis”. The article gives three carbon
dioxide ranges for this segment, from rubidium, from barium and pre-eruptive;
the record carries the range its block states, and support is judged against
that block alone. The review's coverage entry for the fifth element is:

```json
{"semantic": "evidence_relation", "row_index": null, "absent_reason": "NOT_MODELLED"}
```

The graph holds the mechanism and both observations and no relation between
them, because the producer proposed none. The question is PARTIAL, four
elements of five, with assembly UNLINKED_ROWS.

### A.4 A typed gap where the ontology has no slot

**Question CQ-T1-03.** On what date was the article accepted? The result reaches
the article record:

```json
{
  "kind": "ENTITY",
  "record": {
    "doi": "10.1038/s41467-024-55792-9",
    "container_title": "Nature Communications",
    "publication_year": 2025,
    "source_kind": "JOURNAL_ARTICLE"
  },
  "witness": {"record_id": "work:article"}
}
```

The row shows no locator field because a published work is not an
assertion-family record; its locators are in the trace derivations.
Block page:1:block:006 states “Accepted: 30 December 2024”. The producer read
it, retained it as assertion:027, and recorded against it a gap of kind
TYPE_ABSENT: the project ontology declares no type or slot for the editorial
dates of a work, so the assertion formalizes nothing. The review marks the
acceptance event and its date NOT_MODELLED and the question PARTIAL. The gap
is public in the run result's count by kind; its statement is withheld with
the other gap statements.

### A.5 What a PARTIAL witness looks like

The run-23 review found six PARTIAL witnesses among 428. One is:

```json
{
  "witness_key": "claim:acknowledgement-discussions",
  "source_support": "PARTIAL",
  "source_locators": ["page:10:block:043"]
}
```

Block page:10:block:043 ends “We thank P. Cartigny, L.” and the sentence
continues in the next block. The record's name adds the purpose of the thanks,
useful discussions, whose words fall in block 044. The value is in the source;
the cited block carries only part of it. All six PARTIAL witnesses in this cell
are of this kind, a text-layer boundary cutting a sentence, and none is a
contradicted claim.

### A.6 A control that returns nothing

**Question CQ-C-01.** What sulfur and chlorine concentrations are reported? The
review's coverage entries are:

```json
{
  "question_id": "CQ-C-01",
  "question_responsiveness": "NONE",
  "coverage": [
    {"semantic": "bounded_quantity", "row_index": null, "absent_reason": "NOT_IN_SOURCE"},
    {"semantic": "concentration_unit", "row_index": null, "absent_reason": "NOT_IN_SOURCE"},
    {"semantic": "sample_set", "row_index": null, "absent_reason": "NOT_IN_SOURCE"},
    {"semantic": "measurement_status", "row_index": null, "absent_reason": "NOT_IN_SOURCE"}
  ]
}
```

The reading reports carbon dioxide and water as its volatiles and no sulfur or
chlorine value. The query returns 241 rows of the types the question binds,
sample sets among them, and none carries either analyte. NONE here is the
expected result of a control, not a failed positive question.

### A.7 Identities

Every cell's public run result carries the full coordinates. The accepted
ontology, ledger head and replay receipt are, for run-20:
49f0a4d3568740ffb8138d4841015f98adb31fc9865a45d8319641eb2270b6a5,
a2cbdd997a6df09bb2687bd975844cb85a8cc0a0dabf242b41275cfdad4b8c99,
6042d490a8c5c039a0cd3974870ba486edc05590e3e723dfb8a5f5efd955495d. For run-21:
6fbb99a283ddb057a2690e0bf7530a6a16bac7890f36780b4d397588f8592e6a,
a2f3ad2e6ef4b8a33d508ae5eee4d0a654f16e512dc4189fdf043230cab3e217,
2cab922f229d578f183a647e445d0b99348ce2f931fb161a0652547a29a6e832. For run-22:
a4d46211354570aea84919213c8c893dced42362c7d637f13c68b9dc4ace126d,
56e99781e57b0be7e042e22d2ab24f919b0ca7cfcc7f0e6f8e35d714d6eef4b3,
e6b025be41452c4192331cbbf7e5704ef3c344507a2c76efdc4eeb26d9fff4d5. For run-23:
9aa5fdcfb74dc9cad9b36b16b27e8a829b5a71ad1b2bc61892e12a2568b06d21,
9fb776938683d0c5b04666dda13a0711cdd2a78ea99593a2264705a2d825f5ab,
a3abceec58dc93692cbdeabf9a95c03551177ba97d9ee4225fe29198f37f1eec. For run-24:
33bc01eae5ba46b0660b245a48609c41536780ac8832bfa4770e196ee88c02a6,
24482059f4e8650c8e5139d26a5aaa67ee84a67429bcfee1a390f2d9e5439ab4,
23ec9d8abc1998e7d81a1bd75369370a9e2d2f12669a41bdb4c25506b972359e.

The selected reading is
f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17 in every
cell and the source PDF is
7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9. The
review records are at paper-v4/evaluation-v4 and the frozen questions at
paper-v4/experiment-v4, with the [current question file](experiment-v4/competency-questions-v3.1.json)
bound by run-24 and its [predecessor](experiment-v4/competency-questions-v3.json)
bound by run-22 and run-23. Model-assisted judgements in run-22 to run-26
were read in full and ratified by the author; the baseline and reuse
judgements remain HUMAN RATIFICATION PENDING. The compact identity list above covers
run-20 to run-24; run-25 and run-26 carry their full coordinates in their own
public run-result files.

## Appendix B. The Small Shop, run today

The chain runs from the repository root in its configured environment, into a
history path that must not exist yet. The connected runner is the module
research.ontology_driven_kg_realization.experiments.small_shop.connected_story.run
with a history path argument. The warehouse extension is its sibling
warehouse.run in append mode on that exact history, and the read-only ordering
comparison is warehouse.ordering on the same path. The synthetic extension is
partial_shipments.run, also in append mode. Each stage verifies the
digest of the prefix it expects and of its own source bytes before it writes
anything, and a wrong prefix refuses before any write. The whole chain needs no
tool beyond the repository's declared environment. The separate shipment-policy
fixture is shipment_policy.run with a history path argument, and that one needs
SWI-Prolog on the path. The figures in Section 3 were read from runs made while
writing this draft.

Every record carries its derivations back to a retained source row and field.
The reader prints six witnesses for the Scan observation of unit X1. The three
below are the occurrence's own; the other three bind the participation record
participation:e12:item:X1 to the event identifier and item list of the same row:

```json
{
  "e12": {
    "event_type": "SCAN",
    "time_text": "04-05 13:00",
    "units": ["item:X1"],
    "witnesses": [
      {
        "locator": "row:0:event_id",
        "path": ["properties", "source_identifier"],
        "record_id": "e12",
        "source_id": "source:connected-shop:figure-14"
      },
      {
        "locator": "row:0:time_text",
        "path": ["properties", "time_text"],
        "record_id": "e12",
        "source_id": "source:connected-shop:figure-14"
      },
      {
        "locator": "row:0:activity",
        "path": ["properties", "event_type"],
        "record_id": "e12",
        "source_id": "source:connected-shop:figure-14"
      }
    ]
  }
}
```

The refused occurrence replacement changes nothing at admission. Its own
preparation is a separate earlier transaction, and the evidence that transaction
retained stays in the ledger:

```json
{
  "occurrence_replacement": {
    "candidate_plan_id": "plan:hostile:replace-e9",
    "change_sets_unchanged": true,
    "graph_unchanged": true,
    "ledger_unchanged": true,
    "preparation_retained_evidence": true,
    "reason": "TRANSITION_RULE_REFUSAL",
    "refusal_code": "REPLACEMENT_OUTSIDE_SHOP_STATE_ROLE",
    "refused_record_ids": [
      "e9:hostile",
      "participation:e9:actor:R2:hostile",
      "participation:e9:invoice:I2:hostile"
    ]
  }
}
```

The policy runner's report records its own refused candidate:

```json
{
  "duplicate_unit": {
    "ledger_unchanged": true,
    "outcome": "VIOLATED",
    "violations": [
      {
        "rule_id": "ONE_SHIPMENT_PER_UNIT",
        "violation_code": "UNIT_ASSIGNED_TWICE",
        "witness_record_ids": ["SYN-PS-X1", "ships_unit:SYN-S1:SYN-PS-X1", "ships_unit:SYN-S2:SYN-PS-X1"]
      }
    ]
  }
}
```

Reopening any stage with the public history class and replaying it reproduces
that stage's receipt. The Table 1 ledger is
dcd140c5f2456394cfa4c4ea70bf48c3d895dd42d803babed91664f4c01f9eb3, the warehouse
ledger is
0f2cf039b285185df7f8fc42c9647661ea79792806e1abdbb26a526ac818f56b and the
synthetic ledger is
099955003f3274aea590edf1578520540033321cfb3cabcf9aa6b3dff36063bb. The fixtures
are conformance evidence for the structural path over a transcribed published
example and a labelled synthetic cohort; they establish no source truth, no
semantic completeness and no physical delivery.
