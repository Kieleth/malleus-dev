# Malleus: An Executable Commitment Boundary for Model-Proposed Knowledge Graphs

Version: 1.3.0 working draft

Status: lean engineering draft. The selected knowledge-build and query run and two further producer runs are complete and reproduced byte for byte. Source-grounded human review is pending for all three, so answer quality is not yet claimed. A fourth run under a revised protocol, reported in Section 4.5, is admitted and replayed; its source review is preliminary and not yet ratified.

## Abstract

Language models can propose structured claims from documents, but generation alone does not make those claims accepted system state. We present Malleus as an executable commitment boundary for model-proposed knowledge graphs. A fresh model session proposes a domain ontology without seeing the evaluation questions. Deterministic components compile it. A second fresh session proposes source-located population records after the questions are introduced. Generic construction templates lower those records into an immutable change set; checks and a recorded decision govern atomic ledger admission; replay reconstructs the graph; and an application-side query surface reads only replayed state. We execute this path on one marine-seismology paper. The ontology, 15 entity and 33 relation classes with 16 enums, compiled after one structural correction. The first population proposal compiled into 13 operations with 47 located assertions, producing seven entities and six relations in a 23-event history. Disposal, reopen, and replay reproduced the graph and receipt. Four type-bound queries returned 0, 2, 4, and 0 rows, with zero guarded file, network, or embedding-package import attempts. One query covers its requested typed structure, one weakens a requested spatial relation, and two return nothing. Repeating the protocol unchanged with two other fresh producers, Claude Sonnet 5 and Claude Opus 5, returned 0, 0, 0, 0 and 0, 0, 0, 1 rows: both proposed single-valued fields where the source reports ranges and neither required a name, so the proposed ontology, not the pipeline, decided what could be answered. A fourth run changed the protocol rather than the producer: with the brief removed, the whole reading in scope, and unrepresentable assertions recorded as typed gaps, one fresh Claude Opus 5 session proposed an ontology accepted at 3,515 facts on its third attempt and captured 329 modality-carrying assertions into 419 entity and 170 relation records with 104 typed gaps, admitted over 14 ledger events and reproduced by reopen and replay; a type-only binding written after replay returned 4, 32, 34, and 3 rows. Human source review remains pending. The demonstrated claim is narrow: generated structure can cross a source-bound, replayable commitment protocol, and this fixed query path used no embedding index.

## 1. Problem and contribution

A language model can emit plausible JSON, triples, or graph writes. Fluency is not an admission rule. A durable knowledge system still needs to say which source was read, which schema was in force, what exactly was proposed, which checks ran, who or what accepted the proposal, whether failure was atomic, and whether later state can be reconstructed from accepted history.

Malleus addresses that boundary. Generated output remains a proposal until deterministic compilation and policy admit it. The model does not write the accepted graph. A typed change binds ordered operations to exact evidence and prior state. A decision controls atomic admission of the proposed change and its protocol events into the ledger. The working knowledge graph is a projection rebuilt by replay, not a second source of truth.

This paper tests the smallest useful version of that idea on one document. The source is a 2025 Nature Communications article on deep earthquakes and carbon-dioxide degassing at the Mid-Atlantic Ridge. One fresh session reads the document and proposes a domain ontology without access to the four competency questions. After compilation, the experiment binds the questions to types in that ontology. A different fresh session sees the questions, ontology, source reading, and a generic construction library, then proposes a source-located population. The system compiles, checks, admits, replays, and queries the result without semantic repair or fallback.

The absence of question conditioning matters. An ontology tailored to known questions can make an end-to-end demonstration look stronger than the ontology acquisition method warrants. Here, missing concepts remain missing. The ontology cannot completely represent three questions. Later queries cover one question, partially represent one, and return no rows for two. That uneven result was frozen, not repaired after inspection.

The paper makes three bounded contributions:

1. It states a compact protocol separating model proposal, deterministic compilation, recorded acceptance, immutable change, ledger admission, replay, and query.
2. It connects an ontology and finite construction grammar to a typed change set with per-value source locators and atomic admission.
3. It reports one complete document run, including compiler refusal, incomplete query coverage, replay equality, and guarded query execution, and repeats the run unchanged with two other proposal producers.

The paper does not claim that Malleus discovers true knowledge, induces generally adequate ontologies, answers arbitrary questions, or replaces retrieval-augmented generation. It reports an engineering property of one identified execution. Separate source-grounded human-author review of the query rows is still pending.

## 2. Protocol

Six terms define the boundary. An **ontology** declares legal domain record types, properties, relations, and values. A **change set** is an immutable proposal containing ordered operations plus the source, evidence, contract, and prior-state coordinates required to interpret them. A **ledger** is the append-only accepted history. **Replay** reconstructs accepted graph state from that history. A **locator** names one block in the selected source reading. A **query** is a deterministic graph read whose type binding is fixed before population.

The tested path is:

```text
PDF bytes
  -> pinned text-layer reading with stable block locators
  -> fresh, question-independent ontology proposal
  -> deterministic ontology compilation
  -> one recorded acceptance of the compiled ontology digest
  -> type-bound queries and value-generic construction templates
  -> fresh, question-visible population proposal
  -> typed change set, checks, decision, and atomic admission
  -> disposal, ledger reopen, and replay
  -> application-side reads over the replay-derived graph
  -> source-grounded human review under a separately frozen protocol
```

### 2.1 Reading and locators

The publisher PDF is retained locally, excluded from version control, and identified by digest. One pinned reader, `pypdf==6.16.2`, extracts its text layer without rasterization or OCR. The projector normalizes line endings, groups wrapped lines until a sentence, blank-line, or page boundary, and assigns stable page and block identifiers. The selected reading has 186 blocks across 11 pages. Its full text remains private because redistribution needs a separate rights decision; its digest, source manifest, and extraction code are retained.

Every population-supplied record value must carry a valid block locator. Locators do not prove that a statement is supported or true. They make the model's proposed interpretation inspectable and allow the runner to reject missing or unknown references before admission. Provenance also records the construction emission that produced each operation.

### 2.2 Ontology acquisition

The ontology producer is a new session with no inherited paper conversation. Its declared read set contains the selected reading and generic Malleus ontology inputs. The task forbids access to the competency questions, an answer key, an earlier ontology, the manuscript, source code, tests, or a question-derived semantic checklist. It may return one ontology. If compilation fails, the exact diagnostic may be returned to the same session at most twice. There is no hand edit, restart, best-of selection, semantic reviewer, or recovery ontology in the selected path.

Compilation checks the supported schema profile and produces a deterministic fact set, contract bytes, and a receipt. It establishes structural validity only. After compilation, one recorded evaluator event accepts that exact ontology digest for population. The event authorizes the next stage; it is not an adequacy or truth judgment.

### 2.3 Query binding, recipes, and population

Only after ontology compilation do the four questions enter the pipeline. Each question is bound to direct graph cases using record types, relation types, controlled values, and projected properties. A binding cannot name a document value, population identifier, source locator, result count, or exact graph closure. It is frozen before population and does not enter change-set construction, ledger identity, or replay identity.

Nineteen templates in a restricted syntax derived from OTTR provide nine entity constructors and ten relation constructors for 19 selected concrete ontology record types. They encode legal construction form, ontology types, and controlled relation values. They contain no document value, answer, population id, locator, cardinality, or graph size. This is a finite recipe library, not full OTTR support or a general mapping language.

The population producer is another new session. Its declared read set contains the selected ontology, selected reading, generic recipes, four questions, and a closed population grammar. The task forbids access to the query binding, earlier population, manuscript, ledger, model transcripts, or answer material. Each output id must be opaque and sequential. Names may denote records but may not smuggle counts, locations, causal clauses, epistemic qualifiers, or relationships that the ontology cannot type. One structural retry is allowed; a refusal or semantically sparse graph remains the result. There is no evaluator-authored fallback.

The population compiler validates the outer structure, types, required fields, endpoints, locator membership, and complete mapping for the selected population profile. It expands accepted records into an ordered construction plan and deterministic provenance. Required population information has no default. Missing source coordinates, locators, types, or endpoints cause a typed refusal. The later runner separately refuses stale history coordinates or a missing transaction time.

### 2.4 Commitment, replay, and query

The runner derives two checks: source-locator integrity and structural conformance. The private change-set composer then binds explicit sources and evidence, ordered operations, valid time, the active contract, and current history coordinates into one change set. It does not parse the document, select domain meaning, run policy, admit events, or replay state. Transaction time enters separately at admission. A recorded verdict controls atomic admission of the retained change set and its protocol events. Compiler failure, a non-accepting verdict, stale prior state, or failed application leaves that admission batch unapplied.

After admission, the runner records the live graph, protocol state, and receipt, discards those in-memory objects, reopens the file-backed ledger, and replays it. Equality of graph, protocol state, and canonical receipt is checked. Here, disposal means loss of the derived in-memory projection, not deletion of an external graph database. Replay still depends on the identified Malleus implementation; the ledger is not self-executing.

The paper-owned query adapter receives the replay receipt, selected ontology, retained Malleus ontology input, and frozen binding. It receives no source reading, population file, provenance map, answer material, or manuscript. During the query region, Python guards count file opens, socket and name-resolution calls, and imports of named embedding or vector packages. These are interpreter-level observations, not an operating-system sandbox.

Evaluation is separate from construction and querying. Its protocol was frozen before the query result. An identified reviewer must inspect each exact row against independently selected reading blocks and record narrative judgments. The validator can check identities, coverage, locators, labels, and authorship order, but it cannot choose a judgment. The selected experiment computes no numeric or exact-match result.

## 3. Implementation and experiment

The experiment is pinned to Malleus Core commit `f9052b4783100203318d4a21a0236f3851218af1`, tree `39a1ab48b913abc26f975873792c639ee690e811`. It uses the research ontology compiler, the restricted template grammar, a paper-local population bridge, a private change-set composer, ledger admission, replay, and native graph reads. These are identified research seams, not stable public APIs or wire contracts.

The worked source is Yu et al., [*Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge*](https://doi.org/10.1038/s41467-024-55792-9). The publisher PDF is 11 pages and 6,921,046 bytes. The case uses prose blocks only. Figures, tables, open-ended synthesis, and specialist reinterpretation are outside scope.

Four questions were fixed before this run:

1. Which observation network and campaign produced the microseismicity data, and how many instruments were deployed?
2. Which named ridge subsection is associated with the deep microseismicity, and where are the events relative to its ridge axis?
3. What earthquake-depth range and calculated primary-melt CO2 range are reported for the central association, including units and estimate status?
4. What causal mechanism do the authors prefer for the deep mantle earthquakes, represented explicitly as a hypothesis rather than an established fact?

The ontology session did not see these questions. The population session did, because its task was to populate the already selected ontology for them. This separation tests whether the unconditioned domain language can carry later question-relevant facts without allowing the questions to shape that language.

Before population, the binding exposed the following expressibility limits:

| Question | Expressible in the selected ontology | Missing semantics | Populated |
| --- | --- | --- | --- |
| CQ1 | Method uses instrument | Campaign, observing network, acquisition, instrument count | no |
| CQ2 | Seismic phenomenon occurs at feature; feature part of feature | Relative position such as beneath an axis | yes |
| CQ3 | Quantitative observation, target, constituent, and estimate status | None required by the frozen binding | yes |
| CQ4 | Process components and observations | Hypothesis, author preference, epistemic status, direction of motion | no |

These gaps were recorded and left unchanged. The last column is read from the population after the fact: the session created no method, instrument or process record, so CQ1 and CQ4 are population limits as much as ontology limits.

Fresh-session inputs were copied and digest-frozen before each model run. Both tasks forbade network use and extra repository reads. The ontology task forbade file writes; the population task allowed only `population.json` and also forbade delegation. This was a declared session boundary over a shared workspace and tool surface; the experiment does not claim that an operating-system sandbox enforced it. Observable producer kind, task name, visible files, retry count, and diagnostics are retained. Provider internals that the experiment cannot observe are not inferred.

Focused negative tests cover source digest drift, missing or unknown locators, illegal or abstract record mappings, bad relation endpoints, stale prior state, and failed grouped application. Each class refuses mechanically. Synthetic mutations remain separate from the selected proposal and do not contribute alternative facts.

The published Small Shop correction fixture supplies component evidence that ordered states can preserve a superseded record in history while projecting the later record as current. It is published under research tag `research/small-shop-correction-replay-v1`, a research milestone rather than a package release or second paper experiment.

## 4. Results

### 4.1 Frozen identities

The selected run uses exactly five manuscript identities:

1. Source PDF: `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`.
2. Selected reading: `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`.
3. Selected ontology: `sha256:7c07f94630277edf4aa1be2515e7627e5ebe42c4c9cfddd6c50b867e9c6291ed`.
4. Ledger head `sha256:7117c49b0c4b46dd0b39c872cd4d1b914f8d4ec37a805011030ad3f374fd835b` plus replay receipt `sha256:1a86d1229af04d55275dff9616e50d8686510153241689487a13e5732148b796`.
5. Application-side query binding: `sha256:922e2c628a86bca22d761ebf6d453c9056ead8bdc5301e3c5dfb193db61368c1`.

The fifth identity is not accepted-state evidence. Diagnostics, tests, population, and result files remain retained artifacts without becoming extra manuscript identity chains.

### 4.2 Ontology, population, and admission

Ontology attempt one was refused because the root field `default_prefix` is outside the supported LinkML profile. The exact compiler diagnostic was returned once. Attempt two removed only that field and compiled into 15 entity classes, 33 relation classes and 16 enums; the validated import closure, which also carries the LinkML types and the Malleus root, holds 4,146 facts. No semantic edit or question input intervened.

The nineteen value-generic templates compiled against this ontology. The separate population session returned a valid proposal on its first attempt, so no structural retry occurred. It contained 13 records and compiled unchanged into 13 ordered operations with 47 provenance assertions over four reading blocks. Seven operations create entities and six create relations. Both source-locator and structural checks were `SATISFIED`; policy produced `ACCEPT`.

Eighteen anchor events retaining the contract, sources and evidence, plus a five-event atomic admission batch, produced the 23-event history. The admitted graph contains seven entities and six relations. After the live graph and protocol objects were discarded, ledger reopen and replay reproduced the graph state, protocol state, and receipt.

### 4.3 Query output

The query binding contains 1, 2, 4, and 6 direct one-hop cases for CQ1 through CQ4. The resulting row counts were `[0, 2, 4, 0]`:

| Question | Rows | Exact graph content returned |
| --- | ---: | --- |
| CQ1 | 0 | No method-to-instrument row |
| CQ2 | 2 | Microseismicity occurs at the ridge axis; the ridge axis is part of RC2 |
| CQ3 | 4 | Observed depth 10 to 20 km; calculated primary-melt CO2 concentration 0.4 to 3.0 wt%; constituent and material-location links |
| CQ4 | 0 | No process or hypothesis row |

These are raw replay-derived rows, not reviewed answers. CQ2 encodes neither the deep qualifier nor that events are beneath the axis. The ontology lacks complete semantics for CQ1, CQ2, and CQ4. The sparse model population also left partially expressible cases unrealized in CQ1 and CQ4. The two causes separate cleanly. CQ1 lacks campaign, network and count in the ontology, and the population also created no method or instrument record. CQ4's causal chain is expressible through process relations, and the population created no process record, so that empty row is a population limit, not an ontology limit. Given 186 blocks and 48 classes, the fresh session wrote 13 records from four blocks. The rows are not false successes and were not repaired after query execution. CQ3 returns the requested range values, units, targets, and observed or calculated status, but its source support still awaits separate human-author review.

The guarded query region recorded zero file-read attempts, zero network attempts, and zero imports of the named embedding or vector packages. It received the replay receipt, selected ontology inputs, loaded Malleus implementation, and binding. For this fixed execution, the graph was queried without an embedding index. This says nothing about unseen questions, semantic similarity, other retrieval implementations, or operating-system-level isolation.

For contrast, the earlier run whose ontology session did see the four questions, retained at commit `746a48b` and not selected, returned rows for every question, 1, 1, 2 and 1, from a 14-record population. Its population also differed, so this is an end-to-end contrast, not an ontology-only ablation. It is the reason Section 1 treats question conditioning as a confound rather than a convenience.

A second invocation into new ignored directories, using transaction time `2026-09-03T09:11:42Z`, reproduced the semantic ledger and all five public result files byte for byte. The source-grounded review protocol had been frozen before query output, and its exact input manifest was bound afterward. A separate fresh Codex session then prepared preliminary support and responsiveness judgments for all four questions; that record is explicitly nonhuman. The human author ratified it as recorded on 2026-09-03 after checking every row against the cited blocks, and the ratified record is retained beside it. It labels the two CQ-02 rows supported and partially responsive, the four CQ-03 rows supported and responsive, and the two empty results not evaluable. Support means the row's content is stated in the cited prose; we still make no answer-correctness claim.

### 4.4 Two other proposal producers

The protocol was run twice more with nothing changed but the producer. Each run used the byte-identical ontology brief and the same five inputs, a fresh session with no inherited context, compiler diagnostics returned at most twice, one recorded acceptance event, a type-only binding authored against the accepted ontology, recipes and population brief derived mechanically from that ontology and binding, a fresh population session under the same rules, and the same build, admission, replay and guarded query path. The harness that runs a producer from one manifest was first pointed at the v2 artifacts and reproduced the v2 recipes, brief, acceptance event, five result files and private ledger byte for byte. The v2 producer was gpt-5.6-sol at reasoning effort ultra under Codex; the two new producers were Claude Sonnet 5 and Claude Opus 5 under Claude Code at the harness default effort, which the experiment cannot pin or observe.

| Producer | Ontology attempts | Entity / relation classes | Enums | Facts | Binding cases | Population records | Graph | Rows CQ1 to CQ4 |
| --- | ---: | --- | ---: | ---: | --- | ---: | --- | --- |
| gpt-5.6, selected run | 2 | 15 / 33 | 16 | 4,146 | 1, 2, 4, 6 | 13 | 7 entities, 6 relations | 0, 2, 4, 0 |
| Claude Sonnet 5 | 1 | 8 / 8 | 8 | 1,738 | 1, 1, 2, 1 | 2 | 2 entities, 0 relations | 0, 0, 0, 0 |
| Claude Opus 5 | 2 | 20 / 18 | 16 | 3,869 | 1, 2, 3, 2 | 6 | 5 entities, 1 relation | 0, 0, 0, 1 |

Every run admitted atomically, produced a 23-event history, reproduced its graph and receipt after disposal and replay, and recorded zero guarded file, network or embedding-import attempts. Two of the three ontology sessions hit the same compiler boundary on their first attempt, the unsupported root field `default_prefix`, and both removed only that field when the diagnostic was returned. The Opus session also failed to launch three times on server-side overload before producing anything; those launches are logged and are not attempts.

The differences are in the proposed ontologies. Sonnet proposed eight entity and eight relation classes; Opus proposed twenty and eighteen, with an explicit depth datum, unit, determination mode and an abstract subsection root. Neither required the root `name` slot, so neither can name a ridge subsection; the selected v2 ontology required it. Both gave depth and concentration as one value per event or sample, while the source reports them as ranges over populations, and the population brief forbids inventing a value; so neither population contains an earthquake, a sample or a concentration. The v2 ontology carried lower and upper bounds on one observation record, which is why it alone answers CQ3. Neither Claude ontology has a process or hypothesis class with a typed relation to seismicity, so neither can answer CQ4 as asked. Opus's one row states the saturation condition of a pre-eruptive melt in CO2 at 0.7 GPa and 1250 °C, which is the mechanism's premise, not the authors' claim that it triggers the earthquakes. Asked afterwards, without reopening any file, why records were omitted, both population sessions named these rules; the replies are retained as self-reports, not evidence.

Source-grounded review, by a fresh Claude session under the method of Section 2.4 and ratified as recorded by the human author on 2026-09-03, labelled every Sonnet question and the first three Opus questions not evaluable and not responsive on zero rows, and labelled the single Opus row supported on its content and not responsive to the question.

The finding is narrow. The pipeline behaved identically across producers. What varied was whether the proposed vocabulary could hold what the source says, and that was decided before any fact was proposed. A commitment boundary makes this visible: the two near-empty graphs are refusals to invent, recorded as such, not silent gaps.

### 4.5 One producer under the revised v4 protocol

A fourth run, retained under `paper-v4/experiment-v4/run-02/`, changes the protocol rather than the producer. Five things differ in what the producer was given and what it was required to do. The ontology brief and the question-shaped objective are removed, so the producer's whole instruction is the installed Malleus acolyte skill and an isolation message naming its workspace, its read set and its stopping rule. The constructible set is no longer 19 selected types but every concrete entity and relation type on the accepted ontology's population surface. The three shipped grounded vocabulary packs enter the read set, and the pack-grounding rite requires every project class extending a Malleus root to declare its grounding in one of them. The `source-assertion` domain history profile admits a hedged assertion with its modality instead of dropping it. An assertion the ontology cannot carry is recorded as a typed gap instead of being left silent.

The producer is one fresh Claude Opus 5 session under the Claude Code agent harness at the harness default effort, with no inherited context and no question in view. Its read set is eight digest-pinned inputs: the skill, the selected reading, the Malleus root, the LinkML types, the three packs, and the `source-assertion` profile. The isolation message is retained at `run-02/spawn-message.md`.

Ontology acquisition took three attempts and both permitted diagnostic returns. Attempt one refused at the pack-grounding rite with `DIRECT_ROOT_GROUNDING_REQUIRED`, naming all ten ungrounded root extensions in one sorted diagnostic. Attempt two refused with `GROUNDING_NOT_CLOSED` on one unclosed grounding entry. Attempt three was accepted at 3,515 compiled facts, with a population surface of 26 concrete entity types and 3 relation types.

Population is one capture over the whole reading, carrying 329 verbatim assertions with their modality, 419 entity records, 170 relation records, and 104 typed gaps: 84 `AGGREGATE_ONLY`, 16 `TYPE_ABSENT`, 3 `RELATION_ABSENT`, 1 `INTERVAL_NOT_EXPRESSIBLE`. Its census marks all 186 blocks reviewed, 226 assertions fully formalized, 103 partly formalized, and none unformalized. Two structural refusals preceded admission. The document adapter refused `READING_MISMATCH` because the capture named the reading by a canonical-JSON digest while the runner compares the raw declared bytes; the plan compiler then refused `UNDERIVED_FIELD` on one record property with no formalization target. Each diagnostic was returned to the same producer, which corrected its own file both times. On the second it deleted 41 of its own `claim_kind` labels, which the cited prose does not state, rather than manufacture derivations for them, and kept the 9 that source headings state. There was no hand repair and no fallback.

Every admission step is a call on the public `malleus.compiler` facade and its shipped structural history, not the paper-local composer of Section 2.4. One change set entered a 14-event ledger. After the in-memory handles were discarded, ledger reopen and replay reproduced the admitted receipt and the admitted export. Each of the 589 records traces to the assertion and the block it was read from.

The evaluator wrote a type-only binding after the replay was frozen: 21 cases over the same four questions, naming record types and projected field names and no identifier, locator, or value. Executed inside a guard that counts and refuses file reads, socket calls, and embedding-package imports, it recorded zero of each and returned 4, 32, 34, and 3 rows for CQ1 through CQ4, with 126 witness records each traced. The three producers of Sections 4.2 to 4.4 returned 0, 2, 4, 0 rows from 13 population records, 0, 0, 0, 0 from 2, and 0, 0, 0, 1 from 6, citing four, three, and three of the 186 blocks.

Seven of the 16 `TYPE_ABSENT` gaps state that the population surface holds no Event record type. The accepted ontology declares `SeismicEvent` extending the Malleus `Event` root, the grounding receipt lists it among the grounded subjects, and the `source-assertion` profile admits events, but the surface this harness handed the producer enumerates entity and relation types only, and the skill's capture template shows those two families. The producer emitted no Event record and wrote the gaps instead, which is why the graph holds zero events and zero event participations. That is a limitation of this run's harness, not of the accepted ontology or the profile; it is recorded as finding 3 of paper-ledger entry E-0122.

The producer also wrote source sentences into `statement` and `description` record properties. That is legal under the accepted ontology and it is what a source-support review needs, but it puts reading text into the population plan, the typed gaps, the replay receipt, the exported records, the query rows, the retained capture, and the ledger. Eight files are therefore withheld from this repository and published by digest only, listed in `run-02/results/withheld-artifacts.json`. Every public run-02 artifact was checked against every block of the reading, and none shares a 60-character normalized run with any of them. The corresponding public files of the v2 and v3 runs carried no source text.

<!-- Replace the following sentence when the run-02 human ratification record exists. -->
The review of source support and responsiveness for these rows is preliminary until the human author ratifies it.

This run is pinned to Core commit `4881b3a040aaafc7600d009a16ae910084ae32c2`, tree `f532210148cc43e84dfcd764742ff5cfffda10a4`, not the Section 3 baseline. The public record of this run is `paper-v4/experiment-v4/run-02/`, holding the run contract, the producer input manifest and isolation message, the three ontology candidates with their three diagnostics, the grounding receipt, the validated contract and fact set, the population surface, the census, the launch log, the recorded acceptance event, the record and query trace summaries, the post-replay query binding, the transaction time, and the digest of every withheld file. Retained privately are the producer's capture, the population plan, the typed gaps, the ledger, the replay receipt, the exported records, and the query rows. Reopen and replay are reproduced from the retained ledger, so the repository carries their identities and the counts above, not their contents. This run has no reproducer tag; it lives at the commit that carries `paper-v4/experiment-v4/run-02/`, and `paper-v4-multimodel-v2` remains the coordinate for the v2 and v3 runs.

## 5. Related work

Lewis et al.'s original retrieval-augmented generation formulation combines a generator with a neural retriever over an external dense index and conditions output on retrieved passages [Lewis et al., 2020](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html). Malleus asks a different systems question: when does a proposed typed change become accepted, replayable state? This paper has no matched retrieval baseline and does not show that Malleus replaces or outperforms RAG.

Schema-guided extraction is established. SPIRES recursively extracts schema-conforming instances from text with LinkML and grounds named entities against ontologies [Caufield et al., 2024](https://doi.org/10.1093/bioinformatics/btae104). OntoLogX generates ontology-grounded graphs from cybersecurity logs, checks syntax, SHACL compliance, and higher-level conditions, feeds targeted diagnostics back to the model, and persists only validated graphs [Cotti et al., 2026](https://doi.org/10.1002/aisy.202501381). These systems rule out claims that Malleus is the first model-based extraction pipeline, ontology-guided graph builder, or validate-before-persist design. The narrower object tested here is the identified commitment boundary among proposal, decision, immutable change, accepted ledger, and replayed graph.

PROV-O supplies an interoperable vocabulary for entities, activities, agents, derivation, and attribution [Lebo, Sahoo, and McGuinness, 2013](https://www.w3.org/TR/2013/REC-prov-o-20130430/). Malleus does not claim provenance as new. It requires source and evidence coordinates at admission; formal PROV-O interoperability remains future work.

OTTR provides typed, parameterized templates for repeatable graph construction [Skjæveland and Karlsen, 2024](https://doi.org/10.4230/TGDK.2.2.5). The experiment uses a restricted stOTTR-derived grammar for finite topology expansion. It does not claim full OTTR coverage or differential conformance with Lutra.

Blue Brain Nexus validates RDF metadata with SHACL on resource creation and update, records changes in an append-only event log, and rebuilds indexes by replaying that log [Sy et al., 2023](https://doi.org/10.3233/SW-222974). Zep retains source episodes and temporal semantic edges, combines cosine search, BM25 full-text retrieval, and graph traversal, and uses a model to identify conflicts before timestamp invalidation [Rasmussen et al., 2025](https://arxiv.org/abs/2501.13956). Nakajima's ActiveGraph architecture treats an append-only run log as authoritative and the working graph as a deterministic replay projection [Nakajima, 2026](https://arxiv.org/abs/2605.21997). Malleus does not claim append-only history, temporal graphs, validation, or replayed projections as new. Its contribution is the compact, executable boundary that a generated change must cross before replay.

## References

1. Zhiteng Yu, Satish C. Singh, Cédric Hamelin, Léa Grenet, Marcia Maia, Anne Briais, Lorenzo Petracchini, and Daniele Brunelli. [“Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge.”](https://doi.org/10.1038/s41467-024-55792-9) *Nature Communications* 16, 563 (2025).
2. Patrick Lewis et al. [“Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.”](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) *Advances in Neural Information Processing Systems* 33, 9459-9474 (2020).
3. J. Harry Caufield et al. [“Structured Prompt Interrogation and Recursive Extraction of Semantics (SPIRES): a method for populating knowledge bases using zero-shot learning.”](https://doi.org/10.1093/bioinformatics/btae104) *Bioinformatics* 40(3), btae104 (2024).
4. Luca Cotti, Idilio Drago, Anisa Rula, Devis Bianchini, and Federico Cerutti. [“OntoLogX: Ontology-Guided Knowledge Graph Extraction From Cybersecurity Logs With Large Language Models.”](https://doi.org/10.1002/aisy.202501381) *Advanced Intelligent Systems* 8(6), e202501381 (2026).
5. Timothy Lebo, Satya Sahoo, and Deborah McGuinness, editors. [*PROV-O: The PROV Ontology.*](https://www.w3.org/TR/2013/REC-prov-o-20130430/) W3C Recommendation (2013).
6. Martin Georg Skjæveland and Leif Harald Karlsen. [“The Reasonable Ontology Templates Framework.”](https://doi.org/10.4230/TGDK.2.2.5) *Transactions on Graph Data and Knowledge* 2(2), 5:1-5:54 (2024).
7. Mohameth François Sy et al. [“Blue Brain Nexus: An open, secure, scalable system for knowledge graph management and data-driven science.”](https://doi.org/10.3233/SW-222974) *Semantic Web* 14(4), 697-727 (2023).
8. Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. [“Zep: A Temporal Knowledge Graph Architecture for Agent Memory.”](https://arxiv.org/abs/2501.13956) arXiv:2501.13956 (2025).
9. Yohei Nakajima. [“The Log is the Agent: Event-Sourced Reactive Graphs for Auditable, Forkable Agentic Systems.”](https://arxiv.org/abs/2605.21997) arXiv:2605.21997 (2026).

## 6. Limitations

One document and four questions cannot establish general ontology induction quality, domain robustness, or statistical performance. The producer comparison is one session per producer; it shows what each produced once under this protocol, not what each produces typically. The ontology producer was one model session, not a general Malleus ontology builder. Its proposal was broad, structurally valid, and incomplete for three questions. Compilation cannot establish fitness for the questions.

The population producer saw the questions, so the experiment does not test open-ended graph construction. Conversely, it could not add missing ontology semantics. The query binding consists of direct typed cases, not Cypher, SPARQL, Prolog, arbitrary traversal, or natural-language query generation.

An accepted change is conformant under identified checks and a recorded decision. It may still be incomplete, misleading, or false. Per-value locators aid inspection but do not authenticate the publisher, model provider, evaluator, runtime host, or storage owner. Human source review is pending, so even the nonempty rows are not yet evidence of answer support.

The reading comes from a PDF text layer and may retain spacing or ligature artifacts. Figures and tables were excluded. Replay is file-backed and in-process, not a distributed durability result. The access guards observe selected Python entry points only. The run does not test Semantic Re-entry, temporal correction, effects, actions, or autonomous knowledge revision. The ledger here is a generic commitment history parameterized by the accepted ontology. It carries no domain event vocabulary: each run holds one change over empty state, the first population is an ordinary change set rather than a typed seed, and the private path admits only entity and relation creation. A domain semantic ledger in the sense of event-centred accounting models, which fixes how both initial state and later transitions are represented, is not demonstrated. The paper-specific dependency lock is limited to CPython 3.12 on macOS arm64. It identifies but does not vendor the interpreter or operating system, and reproduction still requires the ignored publisher PDF and the exact checkout because the research seam is not in the distributable package.

## 7. Conclusion

Malleus treats model-generated structure as a candidate state transition, not accepted knowledge. In the worked run, a question-independent ontology proposal compiled after one structural correction. A separate model-authored population crossed typed construction, source and structure checks, recorded acceptance, atomic ledger admission, disposal, and replay. The result was reproduced byte for byte and queried without an embedding index on the guarded path.

The same run preserved its limits. Two questions returned no rows, and the CQ2 rows weakened the requested spatial relation. No fallback filled the gaps, and no automated comparison converted raw rows into a success claim. The evidence supports a narrow engineering result: Malleus can turn a source-located proposal into identified, replayable graph state under an explicit commitment protocol. Answer support awaits separate source-grounded human-author review.

## Appendix A. Reproduction

Core commit `f9052b4` defines the implementation baseline. The executable paper snapshot is the commit tagged `paper-v4-multimodel-v2`, which contains the v2 experiment, the two further producer runs, their human ratification records, this prose revision, the drivers, and the dependency lock. Run the commands below from that snapshot. The PDF must exist at the ignored path named by `paper-v4/source/source-manifest.json`. The commands require CPython 3.12.9 on macOS arm64. They create a fresh environment, install only the hash-checked lock, and run the private research seam from the exact checkout. Both output paths must be absent before execution. The further producer runs use the manifest driver, `research/ontology_driven_kg_realization/experiments/document_paper/multimodel.py`, with each run's `run-manifest.json` and the transaction time retained beside it.

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

The retained lock contains 89 pinned distributions and archive hashes. A clean virtual environment installed from it, reproduced the selected reading, five public result files, and private ledger byte for byte, then passed all 184 document-paper and active v2 paper tests. Existing output directories cause refusal. The lock permits the resolver-listed archives for each pinned release rather than selecting one wheel per package; `paper-v4/environment/environment.json` records the exact platform and remaining limits.

## Appendix B. Artifact index

The source contract is `paper-v4/source/source-manifest.json`. The selected ontology and acquisition record are under `paper-v4/experiment-v2/ontology-run/`. The generic templates, query binding, model-authored population, replay receipt, query output, and build result are under `paper-v4/experiment-v2/`. The explicit driver is `research/ontology_driven_kg_realization/experiments/document_paper/v2_experiment.py`. The review protocol, preliminary record, ratification guide, and human ratification record are under `paper-v4/evaluation-v2/`. The dependency lock and clean-verification record are under `paper-v4/environment/`. The source PDF, selected reading, and source-bearing ledger remain ignored under `private/`.
