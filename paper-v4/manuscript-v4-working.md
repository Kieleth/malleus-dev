# Malleus: An Executable Commitment Boundary for Model-Proposed Knowledge Graphs

Status: v4 working manuscript. Stable method prose is drafted. Bracketed result
fields remain unselected until the corrected run is frozen and reproduced.

## Abstract

Language models can propose structured claims from documents, but a plausible
graph is not yet accepted system state. Malleus places an executable commitment
boundary between generation and use. A model proposes an ontology and a
source-located population. Deterministic components compile the ontology,
validate a neutral intermediate representation, retain exact evidence, admit an
immutable change under an explicit policy, and rebuild the working graph by
replaying an append-only ledger. We exercise this path on one marine-seismology
paper. The model sees the complete selected reading but not the four evaluation
questions during ontology construction or population. The questions enter only
after replay, when an evaluator binds them to types in the graph. [TERMINAL RUN
COUNTS AND QUERY OUTCOME.] Every reported graph value can be traced to a
retained source assertion, block locator, modality, and attribution. The query
path reads only replayed graph state and uses no embedding index. This is a
bounded engineering result, not evidence that the graph is complete or true,
or that Malleus replaces retrieval-augmented generation.

## 1. Problem and contribution

A language model can emit JSON, triples, or database writes that look
reasonable. Fluency does not answer the systems questions that matter after
generation. Which source bytes were read? Which schema was in force? What did
the model propose? Which checks ran? What was accepted? Did a failed change
leave partial state? Can the accepted graph be reconstructed later?

Malleus treats generated structure as a proposed state transition. The model
does not write the accepted graph. It proposes records tied to exact source
evidence. A compiler checks those records against an identified ontology and
turns them into an immutable change. A policy controls atomic admission to an
append-only ledger. The queryable graph is rebuilt from that ledger by replay.

This paper tests the smallest useful form of that boundary on one document. A
fresh model session receives a selected text-layer reading, the Malleus
playbook, one history rule, and three reusable knowledge packs. It first
proposes the document's domain ontology. After structural compilation, the same
session captures what the document reports as source-located records and typed
gaps. It never sees the evaluation questions. After admission and replay, an
evaluator binds four frozen questions to the types that actually exist and runs
native graph reads. A separate source-grounded review checks whether the
returned records support responsive answers.

The paper makes three narrow contributions.

1. It separates the domain vocabulary, the meaning of one history entry, and
   the rule for accepting a proposed change. These choices are often collapsed
   into one graph-loading step.
2. It connects document assertions to a typed intermediate representation,
   immutable change, accepted ledger, replayed graph, and record-level source
   trace.
3. It reports one end-to-end execution with its refusals, replay evidence,
   query rows, and missing semantics preserved rather than repaired after the
   result is known.

The experiment cannot establish general ontology induction quality, factual
truth, or retrieval performance. It asks whether a model-proposed graph can
cross an identified and replayable commitment protocol without giving the
model control of accepted state.

## 2. Protocol

Six terms are enough for the main argument. An **ontology** declares legal
domain records, properties, relations, and controlled values. A **change set**
is an immutable proposal that binds ordered record operations to exact source,
evidence, contract, and prior-state coordinates. A **ledger** is the append-only
accepted history. **Replay** reconstructs graph state from that history. A
**locator** names one block in the selected source reading. A **query** is a
deterministic read over the replayed graph.

The path is:

```text
PDF -> selected reading -> model proposal -> compiled ontology
                                   |
history rule + source capture -> neutral plan -> checked change
                                   |
                         decision -> ledger -> replayed graph
                                                   |
                    frozen questions -> typed reads -> source trace -> review
```

Questions enter at the last line. They cannot shape the ontology, capture, or
accepted state.

### 2.1 Vocabulary is not history semantics

An ontology says which domain statements can be represented. It does not say
what one ledger entry means. Ledger mechanics say how bytes are retained,
admitted, and replayed. They do not decide whether a change represents an
observation, a source assertion, a version of world state, an economic event,
or a commitment.

Malleus records that choice in a domain history profile. In this experiment the
selected `source-assertion` profile defines one change as one atomic composition
captured from an identified document. The first change is a partial import, not
a claim that the graph exhausts the document or domain. Its ordering coordinate
is the capture identifier. Dates and periods mentioned by individual
assertions remain attached to the retained assertions instead of being
mistaken for the admission time of the batch.

The Small Shop reference data uses the same ledger machinery with a different
history rule. There, one change represents a version of a domain state record.
A supplier-order quantity at `e7` can supersede its earlier value at `e4`; both
remain in history while only the later record appears in the current graph.
The contrast matters more than the examples: an accounting ontology such as
REA may define resources, events, agents, and commitments, while the history
profile still decides whether an admitted entry is an object event, a state
version, a source-capture batch, or another explicit unit. Domain meaning and
ledger meaning are related but not interchangeable.

### 2.2 From assertions to a typed proposal

The selected PDF is identified by digest and kept outside the repository. One
pinned text-layer reader projects it into stable page and block locators. The
model receives that reading as data. It proposes an ontology after inspecting
the reusable research, metrology, and chronology packs. Project concepts extend
pack concepts where possible and the Malleus root only when necessary. Schema
symbols cannot encode document instances, answer values, locators, policy, or
query logic.

After compilation, the same model session returns one document capture and one
set of proposed Entity and Relation records. Each captured assertion names a
reading block, contains source wording, records a modality such as `STATED`,
`MEASURED`, `CALCULATED`, `HYPOTHESISED`, `NEGATED`, or `CONTESTED`, and points
to the exact record fields it supports. An assertion that cannot be formalized
must state a typed gap, a recorded reason such as a missing type, missing
relation, unrepresentable interval, aggregate-only statement, or absent
modality. Gaps expose loss; they do not authorize guessed facts.

The public document adapter checks the reading and capture digests, locator
membership, verbatim source wording after whitespace normalization, modalities,
record references, and property paths. It emits a neutral PopulationPlan. The
population compiler then checks each record type, property, scalar value,
controlled value, relation direction, endpoint, derivation, and source
coordinate against the compiled contract. Event records remain outside the
tested population boundary.

### 2.3 Commitment and replay

The plan remains a proposal. Malleus retains the exact compiled contract,
history profile, reading, capture, plan, typed gaps, and protocol artifacts.
It composes the plan into a change set bound to the current accepted state. The
default Core policy checks only mechanical properties: retained input identity
and whether applying the proposed operations under the active contract can be
replayed structurally. It does not decide that a source is trustworthy, that a
statement is true, or that the ontology is adequate. A domain adopter may
replace or extend that policy with separately identified checks.

Admission appends the decision and change atomically. A malformed input,
failed check, stale prior state, or invalid grouped application leaves accepted
state unchanged. After admission, the experiment discards the in-memory graph
and history objects, reopens the ledger from disk, and replays it. It compares
the replay receipt and graph with the state observed at admission. The ledger
is authoritative; the graph is a disposable projection.

The graph alone does not carry every epistemic qualification. A relation
licensed by a `HYPOTHESISED` assertion could otherwise look like an unqualified
fact. The public trace operation follows a replayed record through its accepted
change and plan to the exact retained assertion, modality, locator, and source
bytes. Any query result that reports epistemic status must include this trace.

### 2.4 Query and review

The four competency questions and review protocol are frozen before the run,
but the query binding is intentionally created only after replay. The evaluator
cannot know which types a question-blind ontology will contain in advance. A
binding may therefore name existing record types, relation types, controlled
values, directions, and projected fields. It may not name population record
identifiers, source phrases, locators, expected rows, answer values, or graph
size.

Queries execute through public reads on the replay-derived graph. During that
region the harness records attempts to read the source, open network
connections, or import named embedding and vector packages. Zero attempts is a
property of this identified Python execution, not an operating-system sandbox.

Returned rows are not automatically scored. A human review compares each row
and its trace with exact source evidence, recording source support and question
responsiveness separately. Structural admission means that the protocol ran;
it does not turn the model's interpretation into truth.

## 3. Worked experiment

The source is Yu et al., *Deep mantle earthquakes linked to CO2 degassing at
the Mid-Atlantic Ridge*, published in *Nature Communications* in 2025. The
publisher PDF contains 11 pages. The selected reading contains 186 stable text
blocks. Figures, raster OCR, tables, supplementary files, and external domain
sources are outside the declared input closure.

The producer is one fresh session with no inherited paper context. Its closed
read set contains the selected reading, installed Malleus playbook, Malleus and
LinkML roots, three grounded packs, and the `source-assertion` profile. It has
no network access by instruction, cannot delegate, and may write only its run
directory. The session receives no question, query binding, answer material,
earlier ontology, earlier population, result, or manuscript.

The session first proposes an ontology. The parent returns exact typed compiler
diagnostics at most twice. There is no hand correction, second producer, or
best-of selection. Once an ontology compiles, one evaluator event records
acceptance of that exact ontology digest for the experiment. This is a stage
authorization, not an adequacy review.

The same session then receives only the compiler-derived population surface and
the public capture interface. It captures the whole reading, returning proposed
records, relations, source assertions, formalization paths, and gaps. The
adapter reports both block coverage and assertion formalization. At least one
`UNTOUCHED` block is allowed and must remain visible. A source-located cluster
of typed gaps may justify at most two additive ontology revisions. No question
or query result enters that loop, and no fallback supplies missing facts.

Only after the terminal capture is adapted, compiled, admitted, reopened, and
replayed does the evaluator open the four questions:

1. Which observation network and campaign produced the microseismicity data,
   and how many instruments were deployed?
2. Which named ridge subsection is associated with the deep microseismicity,
   and where are the events relative to its ridge axis?
3. What earthquake-depth range and calculated primary-melt CO2 range are
   reported for the central association, including units and estimate status?
4. What mechanism do the authors prefer for the deep mantle earthquakes,
   represented explicitly as a hypothesis rather than an established fact?

The first preregistered no-brief execution exposed a workflow defect before
population. Project grounding reported one ungrounded direct-root class per
call. The producer corrected only the named class in each round, so three
successive attempts refused on `GeologicFeature`, `EarthMaterial`, and
`GeologicOccurrence`. The two-diagnostic budget was then exhausted. The run is
frozen as a structural refusal, not an ontology-quality result. It also exposed
that a fresh governed-history adopter had no neutral packaged machine, binding,
or check executor and would otherwise need to copy fixture policy or assert
successful checks by hand. Core classified both as generic gaps. The corrected
rerun starts only from a new frozen Core coordinate and retains the failed run.

## 4. Results

### 4.1 Corrected ontology and capture

[FINAL CORE COORDINATE. ONTOLOGY ATTEMPTS, DIAGNOSTICS, FACT COUNT, CAPTURE
ASSERTION COUNTS, REVIEWED AND UNTOUCHED BLOCKS, RECORDS, RELATIONS, TYPED GAPS,
AND ADDITIVE REVISION ROUNDS.]

### 4.2 Admission and replay

[LEDGER EVENT COUNT AND HEAD, CHANGE-SET COUNT, ACCEPTED RECORD COUNTS, REPLAY
RECEIPT, GRAPH EQUALITY, NATURAL AND SYNTHETIC REFUSALS.]

### 4.3 Query output and source review

[ONE TABLE: QUESTION, BOUND TYPES, ROW COUNT, COMPACT RETURNED CONTENT, SOURCE
SUPPORT, RESPONSIVENESS. REPORT QUERY-TIME SOURCE, NETWORK, AND EMBEDDING ACCESS
COUNTS. HUMAN JUDGMENTS REQUIRE LUIS RATIFICATION.]

The bounded observation is only that these fixed queries ran over replayed
typed graph state without an embedding index. The experiment has no matched RAG
baseline and says nothing about unseen questions or semantic search.

## 5. Related work

Retrieval-augmented generation combines a generator with retrieval from an
external corpus, commonly through a learned dense index. Malleus asks a
different question: when does proposed structured content become accepted,
replayable state? This experiment neither replaces nor compares itself with
RAG.

Schema-guided extraction is established. SPIRES uses LinkML schemas to extract
structured instances from text. OntoLogX generates ontology-grounded knowledge
graphs, applies structural checks, returns diagnostics, and persists accepted
output. These systems rule out a claim that Malleus is the first model-based
extraction or validate-before-persist pipeline.

PROV-O provides a standard vocabulary for entities, activities, agents,
derivation, and attribution. OTTR provides typed templates for repeatable graph
construction. Blue Brain Nexus combines schema validation, append-only event
history, and replayable projections. Zep and ActiveGraph also use temporal or
event-sourced graphs for agent memory. Malleus does not claim provenance,
templates, validation, temporal graphs, or event sourcing as new. The object
tested here is their composition into one explicit boundary between a model
proposal and accepted graph state.

## 6. Limitations

One document and one producer session cannot establish general ontology or
extraction quality. The query binding is adapted to the vocabulary available
after replay, although it cannot use result values or record identities.
Compilation checks structure, not truth, completeness, or fitness for the four
questions. The capture and plan formats are research contracts, not stable wire
standards. Governed population currently admits Entity and Relation records,
not Event records. The PDF path uses its text layer and excludes figures,
tables, and supplementary material. Query guards observe selected Python entry
points and do not provide operating-system isolation. The experiment has no RAG
baseline, no Semantic Re-entry, and no test of distributed durability. Human
source review remains required before any answer-support claim.

## 7. Conclusion

[FINAL OBSERVED OUTCOME.] Malleus separates model proposal from accepted state
with a typed plan, explicit history meaning, mechanical checks, atomic ledger
admission, and replay. The worked document demonstrates only the properties
recorded by its receipts and source review. Missing rows, typed gaps, refusals,
and incomplete semantics remain part of the result rather than being filled by
a fallback.

## Artifact note

The repository retains the run contract, producer input manifest, failed and
accepted ontology diagnostics, accepted ontology, capture census, neutral plan,
typed gaps, ledger receipt, post-replay query binding, query output, source
traces, review record, reproduction receipt, and publication checks. The
publisher PDF, selected reading text, source-bearing capture, and ledger remain
private. The final version will name five identity groups only: source, reading,
ontology, ledger plus replay receipt, and query binding.
