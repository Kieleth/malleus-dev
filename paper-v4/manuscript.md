# Malleus: An Executable Commitment Boundary for Model-Proposed Knowledge Graphs

Version: 1.4.0 working draft

Status: engineering draft. The main text states what was found. Section 4.2 is the current run and Section 4.3 is the earlier contrast. Source review of the current run's rows is preliminary and not yet ratified by the human author, so answer quality is not claimed. Attempt histories, diagnostics, event counts and receipts are in Appendix B. Every commit, tree and digest is in Appendix A.

## Abstract

A language model can write plausible structured claims about a document. Writing them does not make them part of a system's accepted state. Malleus puts a gate between the two. The model proposes, deterministic code compiles and checks the proposal, a recorded decision admits it or refuses it, an append-only ledger keeps what was admitted, and the working graph is rebuilt by replaying that ledger. Nothing the model writes reaches the graph except through the gate, and an assertion the accepted vocabulary cannot carry is written down as a typed gap instead of being dropped. We first calibrate the path on a small logistics fixture that uses no model at all: five accepted change sets and one additive contract revision over five source files, 48 ledger events, nine current and ten historical records, every record traced back to the plan, source and evidence it came from, reproduced byte for byte. We then send one document, a 2025 marine-seismology article, through the same path. One fresh model session, given no questions and no brief, read the paper and proposed an ontology accepted at 3,515 facts on its third attempt. A second phase captured 329 assertions with their hedging into 419 entity records and 170 relation records, and recorded 104 places where the accepted vocabulary could not carry what the source said. That went in as one change, reopen and replay reproduced it, every one of the 589 records traces to the assertion and the block it was read from, and a type-only binding written after replay returned 4, 32, 34, and 3 rows for four questions the producer never saw. Under an earlier protocol that showed the population session the four questions and gave the ontology session a written brief, three producers returned 0, 2, 4, 0 rows, then 0, 0, 0, 0, then 0, 0, 0, 1. We do not claim the rows are right: human review of them is preliminary. We do not claim the ontology is adequate, that one document generalizes, or that this competes with retrieval. The claim is narrower. Model-proposed structure can cross a source-bound, replayable commitment gate, and this fixed query path used no embedding index.

## 1. Problem and contribution

### 1.1 The problem

A language model can emit plausible JSON, triples, or graph writes. Fluency is not an admission rule. A durable knowledge system still has to answer, for every fact it holds: which source was read, which schema was in force, what exactly was proposed, which checks ran, who or what accepted the proposal, whether a failed proposal left anything behind, and whether current state can be rebuilt from accepted history alone. Pipelines that put model output into a graph answer some of those questions and leave the rest to convention.

Malleus draws that boundary explicitly. Generated output stays a proposal until deterministic compilation and a recorded decision admit it. The model never writes the accepted graph. A typed change binds ordered operations to exact evidence and to the prior state it assumes. One decision controls atomic admission of that change and its protocol events into an append-only ledger. The working knowledge graph is a projection rebuilt by replay, not a second source of truth. What the model cannot say in the accepted vocabulary is recorded as a typed gap rather than left silent.

### 1.2 What this paper reports

This paper tests the smallest useful version of that idea in two settings.

The first is a calibration. A small logistics fixture, five source files describing orders, inventory, invoices, payments and supplier orders, runs the whole public path with no model anywhere in it: compilation, admission, an additive contract revision, replay, query, and a provenance trace for every record. It fixes what the mechanism does before any generated content enters, and it exercises supersession, which the document case does not.

The second is one document. The source is a 2025 *Nature Communications* article on deep earthquakes and carbon-dioxide degassing at the Mid-Atlantic Ridge ([Yu et al., 2025](https://doi.org/10.1038/s41467-024-55792-9)). A fresh model session reads it and proposes a domain ontology without seeing the evaluation questions. Deterministic components compile it. A second fresh session proposes source-located population records. The system compiles, checks, admits, replays, and queries the result without semantic repair or fallback. The paper reports two protocol variants of that path: the current one, in which the producer receives no brief, works over the whole reading, and records typed gaps; and an earlier one, in which the ontology session received a written brief and the population session saw the four questions.

The absence of question conditioning matters in both. An ontology tailored to known questions can make an end-to-end demonstration look stronger than the ontology acquisition method warrants. Here, missing concepts stay missing and the uneven result was frozen, not repaired after inspection.

The paper makes three bounded contributions.

1. It states a compact protocol separating model proposal, deterministic compilation, recorded acceptance, immutable change, ledger admission, replay, and query, and it runs that protocol to completion.
2. It connects an ontology and a finite construction grammar to a typed change set with per-value source locators, atomic admission, and typed gaps for what the vocabulary cannot carry.
3. It reports one calibrated fixture and four document runs from retained artifacts, including compiler refusals, incomplete query coverage, replay equality, and guarded query execution.

The paper does not claim that Malleus discovers true knowledge, induces generally adequate ontologies, answers arbitrary questions, or replaces retrieval-augmented generation. It reports an engineering property of identified executions. Source-grounded human review of the current run's rows is preliminary.

### 1.3 State of the art

Each ingredient of this protocol has independent prior work. The novelty claim is scoped accordingly: to the composition and to the measured findings, not to any ingredient.

**Model-based extraction into schemas.** Schema-guided extraction with a language model is established. SPIRES recursively extracts schema-conforming instances from text using LinkML schemas and grounds named entities against ontologies ([Caufield et al., 2024](https://doi.org/10.1093/bioinformatics/btae104)). OntoLogX generates ontology-grounded graphs from cybersecurity logs, checks syntax, SHACL compliance and higher-level conditions, feeds targeted diagnostics back to the model, and persists only validated graphs ([Cotti et al., 2026](https://doi.org/10.1002/aisy.202501381)). These rule out any claim that Malleus is the first model-based extraction pipeline, the first ontology-guided graph builder, or the first validate-before-persist design. The diagnostic-return loop used here is the same technique. What differs is that a model also proposes the ontology, that the proposal never becomes state without a recorded decision, and that what the schema cannot express is written down rather than dropped.

**Closed-world validation of typed graphs.** SHACL defines validation of an RDF data graph against shapes and a validation report ([Knublauch and Kontokostas, 2017](https://www.w3.org/TR/shacl/)). It says nothing about when validation runs or what happens afterwards, so validating stores place it where they like, commonly at commit. LinkML supplies the schema shape this experiment's compiler accepts a profile of. Rejecting writes that do not conform to a configured structural contract is established engineering. Malleus adds identity for the candidate, a protocol state between structural validity and acceptance, and replay from the accepted history.

**Provenance and claim packaging.** PROV-O supplies an interoperable vocabulary for entities, activities, agents, derivation, and attribution ([Lebo, Sahoo, and McGuinness, 2013](https://www.w3.org/TR/2013/REC-prov-o-20130430/)). Nanopublications package a minimal scientific assertion with its provenance and publication information ([Groth, Gibson, and Velterop, 2010](https://doi.org/10.3233/ISU-2010-0613)), and trusty URIs give such artifacts verifiable content-based identifiers ([Kuhn and Dumontier, 2014](https://doi.org/10.1007/978-3-319-07443-6_27)). Micropublications model claims with their supporting and challenging evidence down to methods and data ([Clark, Ciccarese, and Goble, 2014](https://doi.org/10.1186/2041-1480-5-28)). Malleus claims none of this as new. It differs in where the structure sits: source and evidence coordinates are a condition of admission enforced by a compiler, not a publication convention, and the per-value locator is required before a value can be admitted at all.

**Event-sourced and log-primary designs.** Treating an append-only log as the authority and the queryable state as a rebuilt projection is the Event Sourcing pattern ([Fowler, 2005](https://www.martinfowler.com/eaaDev/EventSourcing.html)). Blue Brain Nexus validates RDF metadata with SHACL on resource creation and update, records changes in an append-only event log, and rebuilds indexes by replaying that log ([Sy et al., 2023](https://doi.org/10.3233/SW-222974)). ActiveGraph treats an append-only agent run log as authoritative and the working graph as a deterministic replay projection ([Nakajima, 2026](https://arxiv.org/abs/2605.21997)). The ledger and replay used here are that architecture, reused deliberately. The addition is the gate in front of it and the typed change that has to cross it.

**Retrieval-augmented generation.** The original formulation combines a generator with a neural retriever over an external dense index and conditions output on retrieved passages ([Lewis et al., 2020](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)). Zep retains source episodes and temporal semantic edges and combines cosine search, full-text retrieval and graph traversal for agent memory ([Rasmussen et al., 2025](https://arxiv.org/abs/2501.13956)). Malleus asks a different systems question: when does a proposed typed change become accepted, replayable state? This paper has no matched retrieval baseline and does not show that Malleus replaces or outperforms retrieval-augmented generation. The one retrieval-adjacent observation it does make is mechanical, not comparative: the query region here executed with no file read, no socket call, and no embedding-package import.

**Templates.** OTTR provides typed, parameterized templates for repeatable graph construction ([Skjæveland and Karlsen, 2024](https://doi.org/10.4230/TGDK.2.2.5)). The question-primed runs use a restricted grammar derived from stOTTR for finite topology expansion. No claim of full OTTR coverage or of differential conformance with Lutra is made.

No exact match was found in the reviewed set for the complete composition tested here: a portable contract injected at construction, a content-addressed candidate that is not yet state, a recorded decision separating structural validity from acceptance, atomic admission, and replay from one ledger authority. That is a bounded audit of published mechanisms, not evidence that the space is unoccupied.

## 2. Protocol

Six terms define the boundary. An **ontology** declares legal domain record types, properties, relations, and values. A **change set** is an immutable proposal containing ordered operations plus the source, evidence, contract, and prior-state coordinates required to interpret them. A **ledger** is the append-only accepted history. **Replay** reconstructs accepted graph state from that history. A **locator** names one block in the selected source reading. A **query** is a deterministic graph read whose type binding is fixed before population, or, in the current protocol, after replay and without seeing any value.

The tested path is:

```text
PDF bytes
  -> pinned text-layer reading with stable block locators
  -> fresh, question-independent ontology proposal
  -> deterministic ontology compilation
  -> one recorded acceptance of the compiled ontology digest
  -> fresh population proposal with typed gaps for what the ontology cannot carry
  -> typed change set, checks, decision, and atomic admission
  -> disposal, ledger reopen, and replay
  -> application-side reads over the replay-derived graph
  -> source-grounded human review under a separately frozen protocol
```

This section describes what both protocol variants share. Section 4.4 states exactly what differs between them.

### 2.1 Reading and locators

The publisher PDF is retained locally, excluded from version control, and identified by digest. One pinned reader, `pypdf==6.16.2`, extracts its text layer without rasterization or OCR. The projector normalizes line endings, groups wrapped lines until a sentence, blank-line, or page boundary, and assigns stable page and block identifiers. The selected reading has 186 blocks across 11 pages. Its full text remains private because redistribution needs a separate rights decision; its digest, source manifest, and extraction code are retained.

Every population-supplied record value must carry a valid block locator. Locators do not prove that a statement is supported or true. They make the model's proposed interpretation inspectable and allow the runner to reject missing or unknown references before admission. Provenance also records the construction emission that produced each operation.

### 2.2 Ontology acquisition

The ontology producer is a new session with no inherited paper conversation. Its declared read set contains the selected reading and generic Malleus ontology inputs. The task forbids access to the competency questions, an answer key, an earlier ontology, the manuscript, source code, tests, or a question-derived semantic checklist. It may return one ontology. If compilation fails, the exact diagnostic may be returned to the same session at most twice. There is no hand edit, restart, best-of selection, semantic reviewer, or recovery ontology in any selected path.

Compilation checks the supported schema profile and produces a deterministic fact set, contract bytes, and a receipt. It establishes structural validity only. After compilation, one recorded evaluator event accepts that exact ontology digest for population. The event authorizes the next stage; it is not an adequacy or truth judgment.

### 2.3 Query binding, recipes, and population

Questions enter the pipeline only after ontology compilation. Each question is bound to direct graph cases using record types, relation types, controlled values, and projected properties. A binding cannot name a document value, population identifier, source locator, result count, or exact graph closure. It does not enter change-set construction, ledger identity, or replay identity.

Under the question-primed protocol, nineteen templates in a restricted syntax derived from OTTR provide nine entity constructors and ten relation constructors for 19 selected concrete ontology record types. They encode legal construction form, ontology types, and controlled relation values, and contain no document value, answer, population id, locator, cardinality, or graph size. This is a finite recipe library, not full OTTR support or a general mapping language.

The population producer is another new session. Under the question-primed protocol its declared read set contains the selected ontology, selected reading, generic recipes, the four questions, and a closed population grammar; the task forbids access to the query binding, earlier population, manuscript, ledger, model transcripts, or answer material. Each output id must be opaque and sequential. Names may denote records but may not smuggle counts, locations, causal clauses, epistemic qualifiers, or relationships that the ontology cannot type. One structural retry is allowed; a refusal or semantically sparse graph remains the result. There is no evaluator-authored fallback.

The population compiler validates the outer structure, types, required fields, endpoints, locator membership, and complete mapping for the selected population profile. It expands accepted records into an ordered construction plan and deterministic provenance. Required population information has no default. Missing source coordinates, locators, types, or endpoints cause a typed refusal. The runner separately refuses stale history coordinates or a missing transaction time.

### 2.4 Commitment, replay, query, and review

Two checks are derived before admission: source-locator integrity and structural conformance. A composer then binds explicit sources and evidence, ordered operations, valid time, the active contract, and current history coordinates into one change set. It does not parse the document, select domain meaning, run policy, admit events, or replay state. Transaction time enters separately at admission. A recorded verdict controls atomic admission of the retained change set and its protocol events. Compiler failure, a non-accepting verdict, stale prior state, or failed application leaves that admission batch unapplied.

After admission, the runner records the live graph, protocol state, and receipt, discards those in-memory objects, reopens the file-backed ledger, and replays it. Equality of graph, protocol state, and canonical receipt is checked. Disposal here means loss of the derived in-memory projection, not deletion of an external graph database. Replay still depends on the identified Malleus implementation; the ledger is not self-executing.

The query adapter receives the replay receipt, selected ontology, retained Malleus ontology input, and frozen binding. It receives no source reading, population file, provenance map, answer material, or manuscript. During the query region, Python guards count file opens, socket and name-resolution calls, and imports of named embedding or vector packages. These are interpreter-level observations, not an operating-system sandbox.

Evaluation is separate from construction and querying. Its protocol was frozen before the query result. An identified reviewer must inspect each exact row against independently selected reading blocks and record narrative judgments. The validator can check identities, coverage, locators, labels, and authorship order, but it cannot choose a judgment. The experiment computes no numeric or exact-match result.

## 3. Implementation and experiment

The runs use the research ontology compiler, a restricted template grammar, a paper-local population bridge, a change-set composer, ledger admission, replay, and native graph reads. The current run uses the public `malleus.compiler` facade and its shipped structural history instead of the paper-local composer. These are identified research seams, not stable public APIs or wire contracts. Pinned commits, trees and digests for every run are in [Appendix A](#appendix-a-frozen-identities-and-coordinates).

The worked source is Yu et al., [*Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge*](https://doi.org/10.1038/s41467-024-55792-9). The publisher PDF is 11 pages and 6,921,046 bytes. The case uses prose blocks only. Figures, tables, open-ended synthesis, and specialist reinterpretation are outside scope.

Four questions were fixed before the first run and reused unchanged in all four:

1. Which observation network and campaign produced the microseismicity data, and how many instruments were deployed?
2. Which named ridge subsection is associated with the deep microseismicity, and where are the events relative to its ridge axis?
3. What earthquake-depth range and calculated primary-melt CO2 range are reported for the central association, including units and estimate status?
4. What causal mechanism do the authors prefer for the deep mantle earthquakes, represented explicitly as a hypothesis rather than an established fact?

No ontology session saw these questions. Under the question-primed protocol the population session did, because its task was to populate an already selected ontology for them; under the current protocol neither session saw them. This separation tests whether unconditioned domain language can carry later question-relevant facts without allowing the questions to shape that language.

Fresh-session inputs were copied and digest-frozen before each model run. Every task forbade network use and extra repository reads. This was a declared session boundary over a shared workspace and tool surface; the experiment does not claim that an operating-system sandbox enforced it. Observable producer kind, task name, visible files, retry count, and diagnostics are retained. Provider internals that the experiment cannot observe are not inferred.

Focused negative tests cover source digest drift, missing or unknown locators, illegal or abstract record mappings, bad relation endpoints, stale prior state, and failed grouped application. Each class refuses mechanically. Synthetic mutations remain separate from the selected proposals and do not contribute alternative facts.

## 4. Results

### 4.1 Calibration: the logistics shop fixture

Before any model output enters, the same public path is run end to end on a small logistics shop whose domain choices are visible as data. Five canonical population plans state which source bytes support which records, where each field came from, which history profile applies, and what the last plan supersedes. One runner executes them. The inputs are five source files: a warehouse JSONL, an inventory CSV, an invoice CSV, a payment JSONL, and a supplier-order JSONL.

The run exercises every mechanical property the document case depends on, and one it does not. Compilation, atomic admission, and replay behave as in the document runs. In addition, an additive contract revision extends the ontology mid-history with supplier orders, invoices, payments and settlement relations; a later change supersedes an earlier record; and a provenance trace resolves every current and superseded record back to its retained plan, derivations, sources, and evidence. The recorded result is five accepted change sets and one additive contract revision, 48 ledger events, nine current and ten historical records. Supplier order `B@e4` stays in history with quantity 1, and `B@e7` supersedes it as the only current supplier-order state, with quantity 2.

Rerunning the fixture reopens the same history and emits byte-identical evidence without changing the ledger. That reproduction holds at the commit carrying this manuscript revision, and no file under the shipped `malleus` package or under the fixture changed between that commit and the coordinate the document run is pinned to, so the calibration and the document run exercise the same implementation.

The fixture is a conformance case, not a protocol rule. The plans are adopter-authored and their format is private. The state-version history profile is a fixture choice. Event population, semantic re-entry, external effects and a stable wire format are out of its scope.

### 4.2 The current run: one producer, no brief, the whole reading

The current document run is retained under `paper-v4/experiment-v4/run-02/`. One fresh Claude Opus 5 session under the Claude Code agent harness, with no inherited context and no question in view, received eight digest-pinned inputs and one isolation message naming its workspace, its read set and its stopping rule. Its whole instruction was the installed Malleus acolyte skill; there was no ontology brief and no question-shaped objective. Section 4.4 lists what else differed from the earlier protocol; the attempt history, the diagnostics it drew, and the two structural returns it corrected are in [Appendix B.3](#b3-the-current-run).

The ontology was accepted on the third attempt. Population is one capture over the whole reading, carrying 329 verbatim assertions with their modality, 419 entity records, 170 relation records, and 104 typed gaps: 84 `AGGREGATE_ONLY`, 16 `TYPE_ABSENT`, 3 `RELATION_ABSENT`, 1 `INTERVAL_NOT_EXPRESSIBLE`. Its census marks all 186 blocks reviewed, 226 assertions fully formalized, 103 partly formalized, and none unformalized. The capture entered the ledger as one change. After the in-memory handles were discarded, ledger reopen and replay reproduced the admitted receipt and the admitted export. Each of the 589 records traces to the assertion and the block it was read from.

The evaluator wrote the query binding after the replay was frozen: 21 cases over the same four questions, naming record types and projected field names, and no identifier, locator, or value. Executed inside a guard that counts and refuses file reads, socket calls, and embedding-package imports, it recorded zero of each and returned 4, 32, 34, and 3 rows for CQ1 through CQ4, with 126 witness records each traced.

The typed gaps are part of the result, not an aside. Each names the kind of loss and the assertion it came from, so a reader can see what the accepted vocabulary refused to carry. Under the earlier protocol a producer facing the same limit either invented nothing and left the graph sparse or wrote a weaker record; neither leaves a machine-readable trace of what was lost.

<!-- Replace the following sentence when the run-02 human ratification record exists. -->
The review of source support and responsiveness for these rows is preliminary until the human author ratifies it.

### 4.3 The earlier producers under the question-primed protocol

Three earlier runs used the question-primed protocol: a byte-identical ontology brief and the same five inputs, a fresh session with no inherited context, compiler diagnostics returned at most twice, one recorded acceptance event, a type-only binding authored against the accepted ontology before population, recipes and a population brief derived mechanically from that ontology and binding, a fresh population session that saw the four questions, and the same build, admission, replay and guarded query path. The harness that runs a producer from one manifest was first pointed at the earliest run's artifacts and reproduced its recipes, brief, acceptance event, five result files and private ledger byte for byte.

| Run | Producer | Protocol | Ontology attempts | Facts | Binding cases | Population records | Graph | Rows CQ1 to CQ4 |
| --- | --- | --- | ---: | ---: | --- | ---: | --- | --- |
| v2 | gpt-5.6-sol | question-primed | 2 | 4,146 | 1, 2, 4, 6 | 13 | 7 entities, 6 relations | 0, 2, 4, 0 |
| v3 | Claude Sonnet 5 | question-primed | 1 | 1,738 | 1, 1, 2, 1 | 2 | 2 entities, 0 relations | 0, 0, 0, 0 |
| v3 | Claude Opus 5 | question-primed | 2 | 3,869 | 1, 2, 3, 2 | 6 | 5 entities, 1 relation | 0, 0, 0, 1 |
| run-02 | Claude Opus 5 | skill, no brief | 3 | 3,515 | 5, 4, 5, 7 | 589 | 419 entities, 170 relations | 4, 32, 34, 3 |
| run-03 | Claude Sonnet 5 | skill, no brief | in progress | in progress | in progress | in progress | in progress | in progress |

The first producer was gpt-5.6-sol at reasoning effort ultra under Codex; the three Claude producers ran under Claude Code at the harness default effort, which the experiment cannot pin or observe. Facts are the compiled fact count of the accepted ontology including its import closure. Binding cases are per question, CQ1 to CQ4. Population records for run-02 are the admitted records; for the question-primed runs they are the records the producer proposed, all of which were admitted.

Run-03 changes only the producer model relative to run-02. When this revision was written its ontology phase had used all three permitted attempts and been refused at the pack-grounding rite each time, so no ontology was accepted, population never started, and there is no query result. That is the state on disk and not a verdict on the cell; no count is pinned for it.

Every run admitted atomically, reproduced its graph and receipt after disposal and replay, and recorded zero guarded file, network or embedding-import attempts. The pipeline behaved identically across all four. What varied was whether the proposed vocabulary could hold what the source says, and that was decided before any fact was proposed.

Under the question-primed protocol the two Claude ontologies could not name a ridge subsection and gave depth and concentration as one value per event or sample where the source reports ranges over populations, so their populations contain no earthquake, sample or concentration at all. The class counts, the exact refusals, and the producers' own accounts of what they omitted are in [Appendix B.2](#b2-the-question-primed-claude-runs). Source-grounded review, ratified by the human author on 2026-09-03, labelled every Sonnet question and the first three Opus questions not evaluable and not responsive on zero rows, and labelled the single Opus row supported on its content and not responsive to the question.

Two near-empty graphs are the informative part of that contrast. They are refusals to invent, recorded as such, not silent gaps.

### 4.4 What changed between the two protocols

Five things differ between the question-primed protocol of Section 4.3 and the current one of Section 4.2. Nothing here isolates any of them. One run under each protocol cannot separate five simultaneous edits, and one of the two producers also differs from two of the three earlier ones. What follows is what each change was designed to do and where its evidence sits.

1. **The ontology brief and the question-shaped objective were removed.** The producer's whole instruction became the installed skill and an isolation message. The intent was to stop the paper's own vocabulary from reaching the producer through the brief. The cost is visible: the ontology took three attempts instead of one or two, and both refusals were at the pack-grounding rite ([Appendix B.3](#b3-the-current-run)).
2. **The constructible set became the accepted ontology's whole population surface.** Under the earlier protocol it was 19 selected concrete types with hand-written templates. This is the change most directly consistent with the jump from 13, 2 and 6 population records to 589, because it removed a cap the evaluator had chosen ([Appendix B.1](#b1-the-first-document-run), [Appendix B.3](#b3-the-current-run)).
3. **Three shipped grounded vocabulary packs entered the read set.** The pack-grounding rite now requires every project class extending a Malleus root to declare its grounding in one of them. The intent was to keep invented terms attributable to a published vocabulary. Both refused attempts were refusals of this rite ([Appendix B.3](#b3-the-current-run)).
4. **The domain history profile changed.** The `source-assertion` profile admits a hedged assertion with its modality, where under the earlier protocol a hedged statement had to be dropped or flattened. The capture records each assertion's modality, 194 of the 589 admitted records carry an assertion-modality derivation, and the preliminary review of CQ4 rests on rows that carry a hypothesised modality and a preferred appraisal ([Appendix B.3](#b3-the-current-run)).
5. **An assertion the ontology cannot carry is recorded as a typed gap.** Under the earlier protocol such losses were invisible; the earlier producers' own accounts of what they omitted had to be collected afterwards as self-reports ([Appendix B.2](#b2-the-question-primed-claude-runs)). The current run recorded 104 of them mechanically, and seven of those gaps exposed a defect in the harness itself, described in Section 4.5.

### 4.5 Limitations

**One document, one producer per cell.** One document and four questions cannot establish general ontology induction quality, domain robustness, or statistical performance. Each cell is one session; it shows what one producer produced once under one protocol, not what it produces typically. The second cell of the current protocol was still running when this revision was written.

**Answer quality is not established.** An accepted change is conformant under identified checks and a recorded decision. It may still be incomplete, misleading, or false. Per-value locators aid inspection but do not authenticate the publisher, model provider, evaluator, runtime host, or storage owner. The current run's human review is preliminary, so even the nonempty rows are not yet evidence of answer support.

**The Event surface gap.** Seven of the 16 `TYPE_ABSENT` gaps state that the population surface holds no Event record type. The accepted ontology declares `SeismicEvent` extending the Malleus `Event` root, the grounding receipt lists it among the grounded subjects, and the `source-assertion` profile admits events, but the surface this harness handed the producer enumerates entity and relation types only, and the skill's capture template shows those two families. The producer emitted no Event record and wrote the gaps instead, which is why the graph holds zero events and zero event participations. That is a limitation of this run's harness, not of the accepted ontology or the profile.

**Free-text quantity kinds.** The accepted ontology's reported-observation type keeps "the source's own name for the reported quantity or count, retained without normalization". Nothing controls that value, so a type-only query cannot ask for depths as distinct from concentrations, and every reported quantity of the same record type comes back together. The preliminary review's CQ3 finding follows directly: both requested quantities are present with units and status, but several competing ranges return side by side with nothing marking which one the question means.

**Most records are unreachable from the binding.** The 21 cases name 13 record types and reach 126 of the 589 admitted records as witnesses. The remaining 463 are in the graph and no case names their type. Coverage of the graph by this binding is partial by construction.

**The binding is coarse.** A type-only binding written after replay cannot filter by value, so a question about one ridge subsection returns rows about other subsections at the same level, and a question about one association returns competing quantities from the whole reading. That is the price of a binding that cannot see any value; it is not a retrieval result.

**Withheld source text.** The current run's producer wrote source sentences into `statement` and `description` record properties. That is legal under the accepted ontology and it is what a source-support review needs, but it puts reading text into the population plan, the typed gaps, the replay receipt, the exported records, the query rows, the retained capture, and the ledger. Eight files are therefore withheld from this repository and published by digest only. Every public artifact of that run was checked against every block of the reading and none shares a 60-character normalized run with any of them. The corresponding public files of the earlier runs carried no source text.

**Isolation is declared, not enforced.** Producer isolation is a declared session boundary over a shared workspace and tool surface. The access guards observe selected Python entry points only. Neither is an operating-system sandbox.

**Scope of the mechanism.** The reading comes from a PDF text layer and may retain spacing or ligature artifacts. Figures and tables were excluded. Replay is file-backed and in-process, not a distributed durability result. The runs do not test semantic re-entry, temporal correction, effects, actions, or autonomous knowledge revision. In the document runs the ledger is a generic commitment history parameterized by the accepted ontology: each holds one change over empty state and admits only entity and relation creation. Supersession and contract revision are exercised only by the calibration fixture of Section 4.1. A domain semantic ledger in the sense of event-centred accounting models, which fixes how both initial state and later transitions are represented, is not demonstrated. The paper-specific dependency lock is limited to CPython 3.12 on macOS arm64; it identifies but does not vendor the interpreter or operating system, and reproduction still requires the ignored publisher PDF and the exact checkout because the research seam is not in the distributable package.

## 5. Conclusion

Malleus treats model-generated structure as a candidate state transition, not accepted knowledge. A calibration fixture runs the whole public path with no model in it, including an additive contract revision, supersession, and a provenance trace for every record. On one document, a model-proposed ontology compiled after refusals it corrected itself, a model-authored population crossed typed construction, source and structure checks, a recorded decision, atomic admission, disposal, and replay, and every admitted record traces to the assertion and the block it came from. Assertions the vocabulary could not carry were written down as typed gaps rather than dropped, and one group of those gaps found a defect in the experiment's own harness.

The runs preserved their limits. Most of the graph is unreachable from the frozen binding, the binding cannot filter by value, the graph holds no events because the surface offered none, and human review of the rows is preliminary. No fallback filled a gap, and no automated comparison converted raw rows into a success claim. The evidence supports a narrow engineering result: Malleus can turn a source-located proposal into identified, replayable graph state under an explicit commitment protocol. Answer support awaits ratified source-grounded human review.

## References

1. Zhiteng Yu, Satish C. Singh, Cédric Hamelin, Léa Grenet, Marcia Maia, Anne Briais, Lorenzo Petracchini, and Daniele Brunelli. [“Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge.”](https://doi.org/10.1038/s41467-024-55792-9) *Nature Communications* 16, 563 (2025).
2. Patrick Lewis et al. [“Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.”](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) *Advances in Neural Information Processing Systems* 33, 9459-9474 (2020).
3. J. Harry Caufield et al. [“Structured Prompt Interrogation and Recursive Extraction of Semantics (SPIRES): a method for populating knowledge bases using zero-shot learning.”](https://doi.org/10.1093/bioinformatics/btae104) *Bioinformatics* 40(3), btae104 (2024).
4. Luca Cotti, Idilio Drago, Anisa Rula, Devis Bianchini, and Federico Cerutti. [“OntoLogX: Ontology-Guided Knowledge Graph Extraction From Cybersecurity Logs With Large Language Models.”](https://doi.org/10.1002/aisy.202501381) *Advanced Intelligent Systems* 8(6), e202501381 (2026).
5. Holger Knublauch and Dimitris Kontokostas, editors. [*Shapes Constraint Language (SHACL).*](https://www.w3.org/TR/shacl/) W3C Recommendation (2017).
6. Timothy Lebo, Satya Sahoo, and Deborah McGuinness, editors. [*PROV-O: The PROV Ontology.*](https://www.w3.org/TR/2013/REC-prov-o-20130430/) W3C Recommendation (2013).
7. Paul Groth, Andrew Gibson, and Jan Velterop. [“The Anatomy of a Nanopublication.”](https://doi.org/10.3233/ISU-2010-0613) *Information Services & Use* 30(1-2) (2010).
8. Tobias Kuhn and Michel Dumontier. [“Trusty URIs: Verifiable, Immutable, and Permanent Digital Artifacts for Linked Data.”](https://doi.org/10.1007/978-3-319-07443-6_27) *The Semantic Web: Trends and Challenges (ESWC 2014)*, 395-410 (2014).
9. Tim Clark, Paolo Ciccarese, and Carole A. Goble. [“Micropublications: A Semantic Model for Claims, Evidence, Arguments and Annotations in Biomedical Communications.”](https://doi.org/10.1186/2041-1480-5-28) *Journal of Biomedical Semantics* 5, 28 (2014).
10. Martin Fowler. [“Event Sourcing.”](https://www.martinfowler.com/eaaDev/EventSourcing.html) martinfowler.com (2005).
11. Martin Georg Skjæveland and Leif Harald Karlsen. [“The Reasonable Ontology Templates Framework.”](https://doi.org/10.4230/TGDK.2.2.5) *Transactions on Graph Data and Knowledge* 2(2), 5:1-5:54 (2024).
12. Mohameth François Sy et al. [“Blue Brain Nexus: An open, secure, scalable system for knowledge graph management and data-driven science.”](https://doi.org/10.3233/SW-222974) *Semantic Web* 14(4), 697-727 (2023).
13. Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. [“Zep: A Temporal Knowledge Graph Architecture for Agent Memory.”](https://arxiv.org/abs/2501.13956) arXiv:2501.13956 (2025).
14. Yohei Nakajima. [“The Log is the Agent: Event-Sourced Reactive Graphs for Auditable, Forkable Agentic Systems.”](https://arxiv.org/abs/2605.21997) arXiv:2605.21997 (2026).

## Appendix A. Frozen identities and coordinates

### A.1 The first document run

The question-primed run of [Appendix B.1](#b1-the-first-document-run) is pinned to Malleus Core commit `f9052b4783100203318d4a21a0236f3851218af1`, tree `39a1ab48b913abc26f975873792c639ee690e811`. It uses exactly five manuscript identities:

1. Source PDF: `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`.
2. Selected reading: `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`.
3. Selected ontology: `sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed`.
4. Ledger head `sha256:7117c49b0c4b46dd0b39c872cd4d1b914f8d4ec37a805011030ad3f374fd835b` plus replay receipt `sha256:1a86d1229af04d55275dff9616e50d8686510153241689487a13e5732148b796`.
5. Application-side query binding: `sha256:922e2c628a86bca22d761ebf6d453c9056ead8bdc5301e3c5dfb193db61368c1`.

The fifth identity is not accepted-state evidence. Diagnostics, tests, population, and result files remain retained artifacts without becoming extra manuscript identity chains.

The earlier, unselected run whose ontology session did see the four questions is retained at commit `746a48b`.

### A.2 The question-primed Claude runs

The two further producer runs are reproduced from the same Core coordinate as the first run, through the manifest driver, with each run's `run-manifest.json` and the transaction time retained beside it. Their private ledgers are `sha256:ce5e890439f93a15daa26c63f54b71fbb044c688ab990ba31f5e7af21d9bbde3` for Claude Sonnet 5 and `sha256:ba49c06348d02da215665666109c62c0adc2ca43cc922aa9d3fa9537dec4173a` for Claude Opus 5.

### A.3 The reproducer tag

The executable snapshot for the first run and the two question-primed Claude runs is the commit tagged `paper-v4-multimodel-v2`, which contains those experiments, their human ratification records, the drivers, and the dependency lock. This reproduction coordinate is outside the five experiment identities. The calibration fixture of Section 4.1 also carries the earlier research tag `research/small-shop-correction-replay-v1`, a research milestone rather than a package release.

### A.4 The current run

The current run is pinned to Core commit `4881b3a040aaafc7600d009a16ae910084ae32c2`, tree `f532210148cc43e84dfcd764742ff5cfffda10a4`, not the Section A.1 baseline. This run has no reproducer tag; it lives at the commit that carries `paper-v4/experiment-v4/run-02/`, and `paper-v4-multimodel-v2` remains the coordinate for the earlier runs.

The three ontology candidates are `sha256:164417a5…`, `sha256:9dfaa95b…` and, accepted, `sha256:56f3e00d…`. The validated fact set is `sha256:c67acb93…`, the validated contract `sha256:8b81f3d8…`, the grounding receipt `sha256:8f977b60…`, the population surface `sha256:6eb4afc3…`. Transaction time is `2026-09-04T19:05:41Z`, the plan is `sha256:3a1c7131…`, the capture `sha256:bfe75992…`, the ledger head `sha256:673e1085…`, and the admitted receipt `sha256:19b274f6…`, reproduced byte for byte by the reopened replay, with export records `sha256:d23aad40…` likewise.

The eight withheld files are listed with their digests in `run-02/results/withheld-artifacts.json`: the producer capture `document-population.json`, the retained capture, `population-plan.json`, `gaps.json`, the ledger `history.jsonl`, `replay-receipt.json`, `export-records.json`, and `query-result.json`. Nothing else publishes their contents.

### A.5 The calibration fixture

The fixture's ontology hash is `sha256:5ecd871dd62bcd3e4feb653ceb50d52f23f934779dd7bd76b1f4f1c138cd17f1`, its base and revised contracts are `sha256:ed170fd1434eb247c2b098a136f2b050021f9d1677d0477be9a69be5d6b63a17` and `sha256:0e1f03bc16861a2cfbca6879a40a8329448ba44a436ddff421458906aa92c5c7`, its ledger head and acceptance head are `sha256:40aef4714385eba826aadde4c7291d41bcf6434c40c20ab002a1252fd7de49f5`, its receipt is `sha256:125062cf210a2ac98035550f2cf9b7f0a3a17f5babfefac04a4c62de5578ecf1`, and the ledger file is `sha256:eb0cb36db45800f133181f13c16d29b18fed55461889105c3057fbf15b64fe94`.

## Appendix B. Run narratives

### B.1 The first document run

Ontology attempt one was refused because the root field `default_prefix` is outside the supported LinkML profile. The exact compiler diagnostic was returned once. Attempt two removed only that field and compiled into 15 entity classes, 33 relation classes and 16 enums; the validated import closure, which also carries the LinkML types and the Malleus root, holds 4,146 facts. No semantic edit or question input intervened.

Before population, the binding exposed the following expressibility limits:

| Question | Expressible in the selected ontology | Missing semantics | Populated |
| --- | --- | --- | --- |
| CQ1 | Method uses instrument | Campaign, observing network, acquisition, instrument count | no |
| CQ2 | Seismic phenomenon occurs at feature; feature part of feature | Relative position such as beneath an axis | yes |
| CQ3 | Quantitative observation, target, constituent, and estimate status | None required by the frozen binding | yes |
| CQ4 | Process components and observations | Hypothesis, author preference, epistemic status, direction of motion | no |

These gaps were recorded and left unchanged. The last column is read from the population after the fact: the session created no method, instrument or process record, so CQ1 and CQ4 are population limits as much as ontology limits.

The nineteen value-generic templates compiled against this ontology. The separate population session returned a valid proposal on its first attempt, so no structural retry occurred. It contained 13 records and compiled unchanged into 13 ordered operations with 47 provenance assertions over four reading blocks. Seven operations create entities and six create relations. Both source-locator and structural checks were `SATISFIED`; policy produced `ACCEPT`.

Eighteen anchor events retaining the contract, sources and evidence, plus a five-event atomic admission batch, produced the 23-event history. The admitted graph contains seven entities and six relations. After the live graph and protocol objects were discarded, ledger reopen and replay reproduced the graph state, protocol state, and receipt.

The query binding contains 1, 2, 4, and 6 direct one-hop cases for CQ1 through CQ4. The resulting row counts were `[0, 2, 4, 0]`:

| Question | Rows | Exact graph content returned |
| --- | ---: | --- |
| CQ1 | 0 | No method-to-instrument row |
| CQ2 | 2 | Microseismicity occurs at the ridge axis; the ridge axis is part of RC2 |
| CQ3 | 4 | Observed depth 10 to 20 km; calculated primary-melt CO2 concentration 0.4 to 3.0 wt%; constituent and material-location links |
| CQ4 | 0 | No process or hypothesis row |

CQ2 encodes neither the deep qualifier nor that events are beneath the axis. The ontology lacks complete semantics for CQ1, CQ2, and CQ4. The sparse population also left partially expressible cases unrealized in CQ1 and CQ4, and the two causes separate cleanly: CQ1 lacks campaign, network and count in the ontology and the population created no method or instrument record, while CQ4's causal chain is expressible through process relations and the population created no process record, so that empty row is a population limit only. Given 186 blocks and 48 classes, the fresh session wrote 13 records from four blocks.

The guarded query region recorded zero file-read attempts, zero network attempts, and zero imports of the named embedding or vector packages. A second invocation into new ignored directories, using transaction time `2026-09-03T09:11:42Z`, reproduced the semantic ledger and all five public result files byte for byte.

For contrast, the earlier run whose ontology session did see the four questions returned rows for every question, 1, 1, 2 and 1, from a 14-record population. Its population also differed, so this is an end-to-end contrast, not an ontology-only ablation. It is the reason Section 1 treats question conditioning as a confound rather than a convenience.

The source-grounded review protocol had been frozen before query output, and its exact input manifest was bound afterwards. A fresh Codex session prepared preliminary support and responsiveness judgments for all four questions; that record is explicitly nonhuman. The human author ratified it as recorded on 2026-09-03 after checking every row against the cited blocks. It labels the two CQ-02 rows supported and partially responsive, the four CQ-03 rows supported and responsive, and the two empty results not evaluable. Support means the row's content is stated in the cited prose; no answer-correctness claim follows.

### B.2 The question-primed Claude runs

The protocol was run twice more with nothing changed but the producer. The first run's producer was gpt-5.6-sol at reasoning effort ultra under Codex; the two new producers were Claude Sonnet 5 and Claude Opus 5 under Claude Code at the harness default effort, which the experiment cannot pin or observe.

| Producer | Ontology attempts | Entity / relation classes | Enums | Facts | Binding cases | Population records | Graph | Rows CQ1 to CQ4 |
| --- | ---: | --- | ---: | ---: | --- | ---: | --- | --- |
| gpt-5.6, first run | 2 | 15 / 33 | 16 | 4,146 | 1, 2, 4, 6 | 13 | 7 entities, 6 relations | 0, 2, 4, 0 |
| Claude Sonnet 5 | 1 | 8 / 8 | 8 | 1,738 | 1, 1, 2, 1 | 2 | 2 entities, 0 relations | 0, 0, 0, 0 |
| Claude Opus 5 | 2 | 20 / 18 | 16 | 3,869 | 1, 2, 3, 2 | 6 | 5 entities, 1 relation | 0, 0, 0, 1 |

Every run produced a 23-event history. Two of the three ontology sessions hit the same compiler boundary on their first attempt, the unsupported root field `default_prefix`, and both removed only that field when the diagnostic was returned. The Opus session also failed to launch three times on server-side overload before producing anything; those launches are logged and are not attempts.

The differences are in the proposed ontologies. Sonnet proposed eight entity and eight relation classes; Opus proposed twenty and eighteen, with an explicit depth datum, unit, determination mode and an abstract subsection root. Neither required the root `name` slot, so neither can name a ridge subsection; the first run's ontology required it. Both gave depth and concentration as one value per event or sample, while the source reports them as ranges over populations, and the population brief forbids inventing a value; so neither population contains an earthquake, a sample or a concentration. The first run's ontology carried lower and upper bounds on one observation record, which is why it alone answers CQ3. Neither Claude ontology has a process or hypothesis class with a typed relation to seismicity, so neither can answer CQ4 as asked. Opus's one row states the saturation condition of a pre-eruptive melt in CO2 at 0.7 GPa and 1250 °C, which is the mechanism's premise, not the authors' claim that it triggers the earthquakes. Asked afterwards, without reopening any file, why records were omitted, both population sessions named these rules; the replies are retained as self-reports, not evidence.

### B.3 The current run

The producer's read set is eight digest-pinned inputs: the skill, the selected reading, the Malleus root, the LinkML types, the three grounded vocabulary packs, and the `source-assertion` profile. The isolation message is retained at `run-02/spawn-message.md`.

Ontology acquisition took three attempts and both permitted diagnostic returns. Attempt one refused at the pack-grounding rite with `DIRECT_ROOT_GROUNDING_REQUIRED`, naming all ten ungrounded root extensions in one sorted diagnostic. Attempt two refused with `GROUNDING_NOT_CLOSED` on one unclosed grounding entry, and that diagnostic named the entry without listing the closed field set it required. Attempt three was accepted at 3,515 compiled facts, with a population surface of 26 concrete entity types and 3 relation types.

Two structural refusals preceded admission. The document adapter refused `READING_MISMATCH` because the capture named the reading by a canonical-JSON digest while the runner compares the raw declared bytes; the producer had itself flagged that ambiguity in its working status file. The plan compiler then refused `UNDERIVED_FIELD` on one record property with no formalization target, and it reports one field per refusal. Each diagnostic was returned to the same producer, which corrected its own file both times. On the second it deleted 41 of its own `claim_kind` labels, which the cited prose does not state, rather than manufacture derivations for them, and kept the 9 that source headings state. There was no hand repair and no fallback. Nothing was admitted by the refused attempts; their ledgers are retained privately.

Every admission step is a call on the public `malleus.compiler` facade and its shipped structural history, not the paper-local composer of Section 2.4. One change set entered a 14-event ledger. After the in-memory handles were discarded, ledger reopen and replay reproduced the admitted receipt and the admitted export.

The public record of this run is `paper-v4/experiment-v4/run-02/`, holding the run contract, the producer input manifest and isolation message, the three ontology candidates with their three diagnostics, the grounding receipt, the validated contract and fact set, the population surface, the census, the launch log, the recorded acceptance event, the record and query trace summaries, the post-replay query binding, the transaction time, and the digest of every withheld file. Retained privately are the producer's capture, the population plan, the typed gaps, the ledger, the replay receipt, the exported records, and the query rows. Reopen and replay are reproduced from the retained ledger, so the repository carries their identities and the counts of Section 4.2, not their contents.

## Appendix C. Reproduction and artifact index

### C.1 The calibration fixture

The fixture runs from the repository root and needs no private input:

```sh
python -m research.ontology_driven_kg_realization.experiments.small_shop.public_population.run \
  --output build/small-shop-public-population
```

It writes `history.jsonl` and `evidence.json`. Running it again reopens the same history and emits byte-identical evidence. The committed `evidence.json` beside the runner is the expected result of a fresh run, and the fixture's own test asserts that equality along with the current and historical record sets.

### C.2 The document runs

Core commit `f9052b4` defines the implementation baseline for the first three runs. The executable snapshot is the commit tagged `paper-v4-multimodel-v2`. Run the commands below from that snapshot. The PDF must exist at the ignored path named by `paper-v4/source/source-manifest.json`. The commands require CPython 3.12.9 on macOS arm64. They create a fresh environment, install only the hash-checked lock, and run the private research seam from the exact checkout. Both output paths must be absent before execution.

```sh
malleus_paper_root="$PWD"
malleus_paper_env="$malleus_paper_root/private/paper-v4-cp312"
malleus_paper_scratch="$malleus_paper_root/private/paper-v4-v2-reproduction"

test ! -e "$malleus_paper_env"
test ! -e "$malleus_paper_scratch"
python3.12 -m venv "$malleus_paper_env"
test "$("$malleus_paper_env/bin/python" -c 'import platform; print(platform.python_version())')" = '3.12.9'
"$malleus_paper_env/bin/python" -m pip install --require-hashes \
  -r "$malleus_paper_root/paper-v4/environment/requirements-cp312-macos-arm64.lock"

PYTHONPATH="$malleus_paper_root:$malleus_paper_root/src" \
"$malleus_paper_env/bin/python" -m research.ontology_driven_kg_realization.experiments.document_paper.text_layer_reading \
  --repo-root "$malleus_paper_root" \
  --source-manifest "$malleus_paper_root/paper-v4/source/source-manifest.json" \
  --output "$malleus_paper_scratch/selected-reading.json"

PYTHONPATH="$malleus_paper_root:$malleus_paper_root/src" \
"$malleus_paper_env/bin/python" -m research.ontology_driven_kg_realization.experiments.document_paper.v2_experiment \
  --repository-root "$malleus_paper_root" \
  --selected-reading "$malleus_paper_scratch/selected-reading.json" \
  --private-run "$malleus_paper_scratch/run" \
  --results "$malleus_paper_scratch/results" \
  --transaction-time '2026-09-03T09:11:42Z'

diff -rq "$malleus_paper_scratch/results" "$malleus_paper_root/paper-v4/experiment-v2/results"
test "$(shasum -a 256 "$malleus_paper_scratch/run/semantic-ledger.jsonl" | cut -d ' ' -f 1)" = \
  'df5327be6abfabfb49342a0663185d81b8a8056211108ca759ea7cac2901e828'
```

The two question-primed Claude runs use the manifest driver, `research/ontology_driven_kg_realization/experiments/document_paper/multimodel.py`, with each run's `run-manifest.json` and the transaction time retained beside it. The full loop, including the ledger digests of Appendix A.2, is in `paper-v4/arxiv/README.md`.

The retained lock contains 89 pinned distributions and archive hashes. A clean virtual environment installed from it reproduced the selected reading, five public result files, and private ledger byte for byte, then passed all 184 document-paper and active paper tests. Existing output directories cause refusal. The lock permits the resolver-listed archives for each pinned release rather than selecting one wheel per package; `paper-v4/environment/environment.json` records the exact platform and remaining limits.

The current run cannot be reproduced from this repository alone. Its reopen and replay run from a retained private ledger, and eight of its artifacts are withheld, so the repository carries their identities and the reported counts, not their contents.

### C.3 Artifact index

The source contract is `paper-v4/source/source-manifest.json`. The first run's ontology and acquisition record are under `paper-v4/experiment-v2/ontology-run/`; its templates, query binding, model-authored population, replay receipt, query output, and build result are under `paper-v4/experiment-v2/`, and its explicit driver is `research/ontology_driven_kg_realization/experiments/document_paper/v2_experiment.py`. Its review protocol, preliminary record, ratification guide, and human ratification record are under `paper-v4/evaluation-v2/`. The two question-primed Claude runs, each with ontology run, binding, recipes, population run, results, and evaluation, are under `paper-v4/experiment-v3/runs/`. The current run is under `paper-v4/experiment-v4/run-02/` and its review record under `paper-v4/evaluation-v4/`. The calibration fixture is `research/ontology_driven_kg_realization/experiments/small_shop/public_population/`. The dependency lock and clean-verification record are under `paper-v4/environment/`. The source PDF, selected reading, and source-bearing ledgers remain ignored under `private/`.
