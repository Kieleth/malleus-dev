# Malleus: An Executable Commitment Boundary for Model-Proposed Knowledge Graphs

Version: 1.0.0 working draft

Status: lean engineering draft with one completed document run. The five experiment identities and public result artifacts are frozen. Strict scoring stopped with a typed oracle-schema mismatch, so answer correctness is not claimed.

## Abstract

Language models can turn documents into structured claims, but generation alone does not explain when those claims become accepted system state. We present Malleus as an executable commitment boundary for model-proposed knowledge graphs. A model proposes an ontology and a source-located population. Deterministic components compile the ontology, validate an immutable change, record a decision, append accepted events to a ledger, and reconstruct the graph by replay. We evaluate this path on one marine-seismology paper and four questions fixed before population. Separate fresh sessions produced an ontology that compiled on its first attempt and a population of 8 entities, 6 relations, and 51 located assertions. Malleus produced a 24-event history with an atomic five-event admission suffix, then reproduced the graph and receipt after disposal and reopen. Four type-bound queries returned 1, 1, 2, and 1 raw rows, with zero Python-level guarded file, network, or embedding-import attempts. Strict scoring returned `UNSCORABLE_ORACLE_SCHEMA_MISMATCH` and a null score because the sealed answer objects and raw query rows have different shapes. We therefore report graph execution, provenance, admission, replay, and isolation, but not query correctness, general retrieval quality, or source truth.

## 1. Introduction

A language model can emit plausible JSON, triples, or graph writes, but fluency is not an admission rule. A durable knowledge system still needs traceable sources, a legal schema, recorded checks and decisions, atomic failure, and reproducible state. Malleus addresses that boundary: the model proposes, while deterministic compilation and policy govern commitment. A typed change binds ordered operations to evidence and prior state; a recorded decision controls ledger entry; and replay, not a second graph writer, produces the working graph.

This engineering paper demonstrates the boundary on a 2025 Nature Communications article about deep earthquakes and carbon-dioxide degassing at the Mid-Atlantic Ridge. Four questions cover the observation campaign, earthquake location, two reported ranges, and the preferred causal hypothesis. Separate fresh sessions propose the ontology and source-located facts. The observed result stands without hand repair or evaluator fallback.

The graph must be load-bearing. The query process receives the replay receipt's graph snapshot, the selected ontology and retained import needed for typed rehydration, and the frozen query binding. It does not receive the PDF, extracted reading, model transcripts, population proposal, or answer key. Python-level guards count attempted file access, network access, and imports of common embedding or vector packages while the four queries run. A separate scorer receives the frozen query output and sealed key. The observed zero counters establish only that this fixed path executed without an embedding index. They do not establish that the returned rows match the intended answers or that Malleus replaces retrieval-augmented generation.

The paper makes three bounded contributions:

1. It states a small commitment protocol that separates model proposal, deterministic compilation, recorded decision, accepted history, replay, and query.
2. It connects an ontology and finite construction grammar to an enforced change-set representation with source locators and atomic admission.
3. It reports one end-to-end document run, including failures and a replay-state query test, without claiming answer correctness, general retrieval superiority, or source truth.

## 2. Boundary and terms

An **ontology** defines legal record types, properties, relations, and controlled values. A **change set** is an immutable proposal containing ordered graph operations and the source, evidence, contract, and prior-state coordinates needed to interpret them. A **ledger** is the append-only accepted history. **Replay** reconstructs graph state from that history. A **locator** names the selected-reading block supporting one proposed value. A **query** is a deterministic graph read fixed before population.

These objects separate concerns that a direct graph write collapses. The ontology limits expression; the construction grammar expands typed inputs; the change set fixes one transition; checks and a decision control entry; and replay produces queryable state.

The path requires five invariants: model output stays outside accepted state until authorized; admitted records conform to the ontology; a failed or stale group leaves no partial admission; disposal and replay reproduce the graph and receipt; and query rows come from graph records without source or answer-key access.

Malleus conformance is not truth. A structurally valid, source-located claim can still be incomplete, misleading, or false. The experiment trusts the exact local implementation and declared artifacts within its environment. It does not authenticate the publisher, model provider, runtime host, evaluator, or storage owner. Those limits are part of the claim, not implementation trivia.

## 3. Protocol

The tested path is:

```text
PDF bytes
  -> pinned text-layer reader and stable blocks
  -> fresh model ontology proposal
  -> ontology compiler
  -> recorded evaluator acceptance of the compiled digest
  -> type-bound query definitions
  -> fresh model population with a locator per value
  -> generic construction recipes
  -> immutable change set and checks
  -> recorded decision and ledger admission
  -> disposal, reopen, and replay
  -> replay-state queries
  -> separate strict scoring
```

### 3.1 Reading

The publisher PDF is retained locally, excluded from version control, and identified by digest. One pinned reader extracts its text layer without rasterization or OCR. The projector normalizes line endings, groups wrapped lines through sentence, blank, or page boundaries, and assigns stable page and block identifiers. The complete reading remains private; its digest and extraction code are public.

Locators are part of the experimental contract. The population producer must attach a valid block identifier to every population-supplied value. A locator does not prove support or truth, but it makes the proposed interpretation inspectable and lets the runner refuse missing or unknown block references before admission.

### 3.2 Ontology proposal and compilation

A new model session receives the selected reading, four questions, a narrow task, and retained Malleus inputs. It returns one ontology file. If compilation fails, the exact diagnostic may be returned to that session at most twice. There is no hand repair, restart, best-of selection, or adequacy reviewer. After compilation, one evaluator event records the ontology digest and actor id used for population. This authorizes the next stage; it does not certify meaning or truth.

### 3.3 Query binding before population

Each competency question is translated into a native graph query after ontology compilation and before any population file exists. The binding may name record types, relation types, enum values, legal joins, and output fields. It may not name answer values, document phrases, block locators, entity counts, relation counts, or an exact graph closure. This prevents query authorship from deciding in advance how many records the population model must produce.

### 3.4 Population and construction

A separate fresh session receives the selected ontology and reading, generic recipes, four questions, and population task. It returns one machine-readable file with a block locator for each value. One structural retry is allowed. There is no content review, evaluator population, or fallback.

The eight recipes encode reusable entity and relation shapes. They contain ontology types and enums, but no document name, answer value, record identifier, graph size, or causal chain. Expansion produces an ordered plan, which a small adapter converts into the change set used by admission.

The change set is the enforced intermediate representation between generated population and accepted graph state. It binds ontology, evidence, prior state, operation order, dependencies, and content identity. A canonical provenance map associates each record and property with a reading locator and recipe emission, and enters the evidence closure by digest. Missing data causes refusal; the runner does not invent locators, types, endpoints, times, base state, or answers.

### 3.5 Decision, ledger, and replay

The two checks cover source and locator integrity plus structural conformance, including dependency order and endpoints. Composition and admission bind the prior state. A change is admitted as one ordered group. Compiler refusal, a non-accepting decision, stale state, or failed application leaves no partial admitted change.

After admission, the runner captures the graph, receipt, and protocol state; disposes of the in-memory history and graph; reopens the ledger; and replays it. Here, deletion means disposal of that derived projection, not deletion of an external graph database. All three canonical values must match. Replay depends on the identified implementation; the ledger is not self-executing.

### 3.6 Query isolation and scoring

The query process receives the public replay receipt, selected ontology, retained Malleus ontology import, and frozen query binding. The receipt contains the replayed entities, relations, validated contract coordinate, and graph-state coordinate needed to reconstruct a typed in-memory graph. It contains no source text or locators. During query execution, Python-level guards replace file-open and socket entry points and count imports of common embedding and vector packages. These guards are instrumentation within the interpreter, not an operating-system sandbox. The process returns canonical raw rows and graph witnesses. A separate scorer receives those rows, the binding, and the sealed key.

## 4. Implementation and experiment

The isolated experiment is bound to Malleus Core commit `f9052b4783100203318d4a21a0236f3851218af1`, tree `39a1ab48b913abc26f975873792c639ee690e811`. It uses the research ontology compiler, a restricted stOTTR-derived grammar, a paper-local plan bridge, private change-set composition, ledger admission, replay, and native graph filters. The composer binds explicit inputs to current history coordinates; it does not parse, judge, admit, or replay. None of these research seams is a stable public API or general mapping language.

The worked source is Yu et al., [*Deep mantle earthquakes linked to CO2 degassing at the Mid-Atlantic Ridge*](https://doi.org/10.1038/s41467-024-55792-9), published in Nature Communications in 2025. The publisher PDF has 11 pages and 6,921,046 bytes. The case uses prose only; figures, tables, open-ended synthesis, and specialist reinterpretation are excluded.

The four frozen questions are:

1. Which observation network and campaign produced the microseismicity data, and how many instruments were deployed?
2. Which ridge subsection is associated with deep microseismicity, and where are the events relative to its ridge axis?
3. What earthquake-depth and calculated primary-melt CO2 ranges are reported, including units and estimate status?
4. What causal mechanism do the authors prefer, represented as a hypothesis rather than established fact?

The evaluator sealed the answer values before the new run. D1 then replaced the retired OCR reading with the selected PDF text layer and issued a version 2 private oracle whose answer objects were unchanged and whose 22 value locators resolve to the new blocks. Neither model session could access the oracle.

Each session's visible inputs are copied once into a retained directory. Its task forbids network access and any write outside the requested output. The record names the observable model, service date, files, and diagnostic returns; unexposed provider internals remain unknown.

Measures cover compiler returns, retry counts, locator completeness, admitted graph size, refusal outcomes, equality after reopen, raw query rows, scoring status, and guarded query-time access. Natural refusals count as results. For predeclared classes not observed naturally, focused mutations test source drift, locator failure, illegal type or endpoint, stale prior state, and failed grouped application.

The research milestone `research/small-shop-correction-replay-v1`, tag object `449ba25964a88ead86cc1aec337be1631cad9471` at commit `e94f45c74475948dfebdc89247bfb070de0b778d`, supplies component evidence for ordered correction, supersession, and replay. It is not a package release, second evaluation, or answer source.

## 5. Results

### 5.1 Frozen inputs and reading

The experiment uses five identity groups:

1. Source PDF: `sha256:7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9`.
2. Selected reading: `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17`.
3. Selected ontology: `sha256:df483285ede9820e25e17215d18ee089d9faeff8d7afaf02365083e19671c941`.
4. Ledger head `sha256:a069c3ded48b3da1c6f022bab8601b16173ac90c64c812a4c74435b3085e43b6` and replay receipt `sha256:6fccc6048d3444b9cbe4ea2bdca3101a7642a4e036a852d26e8fa21fbe03fb29`.
5. Query binding: `sha256:115009ff737600d63eb9761bfc11f69ee62cd11f41d60682772556f5fa56c6d9`.

The selected reader is `pypdf==6.16.2`, called with strict parsing and default text extraction. Two independent in-memory builds produced equal bytes. The final projection contains 186 blocks across 11 pages and none of the `CO,` corruption found in the retired reading. The sealed answers were unchanged when their locators were rebound.

One evaluator-only coordinate was corrected before scoring. After the query result was frozen, but before oracle bytes were opened, preflight found that the scorer still named the retired version 1 envelope rather than D1's rebound version 2 envelope. Their ordered question-and-answer projections are byte-identical; version 2 adds 22 locators over six reading blocks. Only the expected private coordinate changed. The query binding and result remained frozen, and no answer adapter was added.

### 5.2 Ontology and population

The fresh ontology session produced one proposal. It compiled on the first attempt into 1,401 validated facts, so no compiler diagnostic was returned to the model.

One event by `actor:paper-v4-evaluator` accepted that exact digest for population. The event records authorization to continue, not an adequacy judgment. No reviewer, hand repair, restart, or alternate ontology contributed to the result.

The query binding represents each question as typed source-relation-target cases. It fixes record and relation types, enums, and output fields, but no record id, answer value, graph size, singleton result, or closure.

The fresh population session also produced one proposal. Its first structural compilation passed, so the allowed retry was not used. The proposal contains 8 entities and 6 relations. The provenance map contains 51 assertions: 14 record assertions, 25 property assertions, and 12 relation-endpoint assertions. Every assertion carries a valid locator, and the set covers seven unique selected-reading blocks. Each provenance row also binds the exact recipe emission and emitted fact that produced the operation.

Neither model stage produced a natural refusal: 0 were observed. Five predeclared synthetic classes, kept separate from the run, test source digest drift, missing or unknown locators, illegal types or endpoints, stale prior state, and failed grouped application. The selected outputs were not replaced by hand-authored or evaluator-authored alternatives.

### 5.3 Admission, replay, and queries

The ledger begins with 19 bootstrap anchors: 18 artifacts and one source. Admission then adds an atomic five-event suffix: retained change set, proposal, two `SATISFIED` checks for source-locator integrity and structural conformance, and verdict. Policy derives `ACCEPT`, applying all 14 ordered creates as a group. The 24-event result has 8 entities and 6 relations; its head and receipt form the fourth identity group.

The runner released the in-memory history and graph, reopened the ledger, and replayed it. The graph, protocol state, and receipt equaled their admitted values. A second focused reopen also reproduced the ledger bytes and change set. This is a file-backed, in-process demonstration, not an external-service durability claim.

The first query rehydration attempt refused because a local ontology registry hash was compared with the receipt's compiled contract hash. The fix requires and reapplies the receipt's validated fact-set coordinate before comparison; missing, malformed, or inconsistent values now refuse. Query selectors and records did not change. The frozen run returned row counts `[1, 1, 2, 1]`. CQ-01 projects the SMARTIES 2019 campaign, ocean-bottom seismometer network, microseismicity data, and 19 instruments. CQ-02 projects deep microseismicity at segment RC2 beneath the ridge axis. CQ-03 projects 10 to 20 km as a reported observation and 0.4 to 3.0 wt% primary-melt CO2 as a calculated estimate. CQ-04 projects the preferred ascending-melt and CO2-degassing mechanism, including its pressure, stress, and earthquake-outcome fields.

Each row includes source, relation, and target identifiers as witnesses. The Python guards recorded zero file reads, zero network calls, and zero named embedding or vector-package imports. The process had received the replay receipt, ontology and import, and binding. The counters do not prove operating-system isolation or cover every retrieval implementation.

Strict scoring produced no correctness score. The sealed answer objects and raw rows differ in fields and case structure, and no total adapter had been frozen. The scorer therefore returned `UNSCORABLE_ORACLE_SCHEMA_MISMATCH`, no per-question results, and `score: null`. It did not coerce types, score a subset, parse prose, or report `0/4`. The run measures construction, admission, replay, query execution, and guarded access, not agreement with the sealed answer semantics.

## 6. Related work

Retrieval-augmented generation combines a generator with a neural retriever over a dense external index and conditions generation on retrieved passages [Lewis et al., 2020](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html). Malleus addresses a different systems question: whether a proposed typed change becomes accepted, replayable state. This experiment has no matched retrieval baseline and cannot show that Malleus replaces or outperforms RAG.

Schema-guided extraction is established. SPIRES recursively extracts schema-conforming instances from text using LinkML and grounds named entities against ontologies [Caufield et al., 2024](https://doi.org/10.1093/bioinformatics/btae104). OntoLogX generates ontology-grounded graphs from cybersecurity logs, checks syntax, SHACL, and semantic conditions, and may ask the model to revise an invalid candidate for up to three rounds before persistence or an empty-graph result [Cotti et al., 2026](https://doi.org/10.1002/aisy.202501381). These systems rule out claims that Malleus is the first model-based extraction system, ontology-guided pipeline, or validate-before-persist design. The narrower contribution here is an identified boundary among proposal, recorded decision, immutable change, accepted ledger, and replayed state.

PROV-O provides an interoperable vocabulary for entities, activities, agents, derivation, and attribution [Lebo, Sahoo, and McGuinness, 2013](https://www.w3.org/TR/2013/REC-prov-o-20130430/). Malleus does not claim provenance as new. It makes source and evidence coordinates mandatory inputs to admission; formal PROV-O interoperability remains future work.

OTTR provides typed, parameterized templates for repeatable graph construction [Skjæveland and Karlsen, 2024](https://doi.org/10.4230/TGDK.2.2.5). The current construction grammar implements a restricted stOTTR-derived form for finite topology expansion. It does not claim full OTTR support or differential conformance with Lutra.

Blue Brain Nexus validates RDF metadata against SHACL before primary storage, records changes in an append-only event log, and rebuilds projections by replay [Sy et al., 2023](https://doi.org/10.3233/SW-222974). Zep retains raw source episodes and temporal semantic edges, combines vector and term retrieval with graph traversal, and uses a model to identify conflicts before timestamp invalidation [Rasmussen et al., 2025](https://arxiv.org/abs/2501.13956). The 2026 ActiveGraph preprint treats an append-only run log as authoritative and the working graph as a deterministic replay projection [Nakajima, 2026](https://arxiv.org/abs/2605.21997). Malleus therefore does not claim append-only histories, temporal graphs, or replayed projections as novel. It tests a smaller executable commitment boundary before graph reconstruction.

## 7. Limitations

One document and four fixed questions cannot establish general ontology induction quality, domain robustness, or statistical performance. Questions whose answers the ontology does not represent will fail, even when a semantic search system might retrieve useful text.

The selected reading comes from a PDF text layer and still contains spacing and ligature artifacts. An earlier Tesseract reading corrupted question-critical `CO2` tokens; that reading and its ontology run are retained as history but excluded from evidence.

Strict scoring depends on a compatible evaluator-authored key. Sealing the key before the run and hiding it from both model sessions reduces adaptation, but does not authenticate the evaluator or make the key infallible. In this run the key and query result used different schemas, and refusing to invent a post-result adapter left correctness unmeasured. A later experiment may freeze a total row-to-answer mapping before population, but that would be a new evaluation.

An accepted change is structurally valid under identified checks and a recorded decision. It may still be incomplete or false. The current compiler, construction bridge, and history seam are research-local, create-only for this case, and not a stable cross-language contract.

The query test covers a deliberately narrow interface and Python-level instrumentation. Zero guarded attempts say nothing about exploratory search, semantic similarity, unseen questions, operating-system isolation, or other documents. Semantic Re-entry, temporal correction, external effects, and autonomous follow-up changes remain future work.

## 8. Conclusion

Malleus treats generated structure as a candidate state transition, not as knowledge merely because a model emitted it. The ontology defines legal meaning, the change set fixes one proposed transition, a recorded decision controls ledger admission, replay reconstructs the graph, and fixed queries inspect only accepted state.

The worked run crossed that boundary. Two fresh sessions produced a first-pass ontology and population; the latter compiled into 8 entities, 6 relations, and locators for all 51 population-supplied claims. Malleus admitted one grouped change to a 24-event history, then reproduced the same graph, protocol state, and receipt after disposal and reopen. Four prebound queries executed from the replay receipt with zero guarded file, network, or embedding-import attempts.

The final evaluation also exposed its own limit. The frozen raw rows and sealed answer objects had incompatible schemas, so the scorer returned a typed unscorable result rather than adapting the answers after seeing them. The experiment therefore supports a narrow engineering claim: model-proposed structure can cross an explicit, source-bound commitment protocol into replayable graph state, and fixed queries can run over that state without an embedding index on this path. It does not establish answer correctness, truth, arbitrary retrieval, or replacement of RAG.

## Appendix A. Reproduction coordinates

The five identities are listed in Section 5.1. The Core commit, tree, and dependencies in `pyproject.toml` define the environment. From a clean checkout, choose output paths that do not exist and run:

```sh
malleus_paper_root="$PWD"
python3.12 -m venv "$malleus_paper_root/.venv"
malleus_paper_python="$malleus_paper_root/.venv/bin/python"
malleus_paper_scratch="$malleus_paper_root/private/paper-v4-reproduction-01"

"$malleus_paper_python" -m pip install -e '.[research]'
"$malleus_paper_python" -m research.ontology_driven_kg_realization.experiments.document_paper.text_layer_reading --repo-root "$malleus_paper_root" --source-manifest "$malleus_paper_root/paper-v4/source/source-manifest.json" --output "$malleus_paper_scratch/selected-reading.json"
"$malleus_paper_python" -m research.ontology_driven_kg_realization.experiments.document_paper.frozen_experiment --repository-root "$malleus_paper_root" --reading "$malleus_paper_scratch/selected-reading.json" --private-run "$malleus_paper_scratch/run" --results "$malleus_paper_scratch/results"
"$malleus_paper_python" -m research.ontology_driven_kg_realization.experiments.document_paper.query_replay --receipt "$malleus_paper_scratch/results/replay-receipt.json" --binding "$malleus_paper_root/paper-v4/experiment/native-query-binding.json" --ontology "$malleus_paper_root/paper-v4/experiment/ontology-run/ontology.yaml" --malleus "$malleus_paper_root/paper-v4/experiment/ontology-run/inputs/malleus.yaml" --output "$malleus_paper_scratch/results/query-result.json"
"$malleus_paper_python" -m research.ontology_driven_kg_realization.experiments.document_paper.query_score --query-result "$malleus_paper_scratch/results/query-result.json" --oracle "$malleus_paper_root/private/paper-v4-evaluation/answer-oracle.json" --binding "$malleus_paper_root/paper-v4/experiment/native-query-binding.json" --output "$malleus_paper_scratch/results/score.json"

diff -rq "$malleus_paper_scratch/results" "$malleus_paper_root/paper-v4/experiment/results"
cmp "$malleus_paper_scratch/run/semantic-ledger.jsonl" "$malleus_paper_root/private/paper-v4-run/semantic-ledger.jsonl"
```

The byte-equal retained rerun used Python 3.12.9, LinkML 1.11.1, LinkML Runtime 1.11.1, NetworkX 3.6.1, PyYAML 6.0.3, tzdata 2026.3, and pypdf 6.16.2. The PDF is ignored beside its public manifest under `paper-v4/source/`. The selected reading, oracle, and source-bearing semantic ledger remain under `private/` and are not committed. Reproducing the score requires the evaluator-only oracle. Existing run or result paths cause refusal. `pyproject.toml` declares the dependencies, but a complete paper-specific transitive lock remains part of the arXiv bundle work.

## Appendix B. Claim-to-artifact index

The source and reading contract is in `paper-v4/source/source-manifest.json` and `research/ontology_driven_kg_realization/experiments/document_paper/text_layer_reading.py`. The selected ontology and acceptance are in `paper-v4/experiment/ontology-run/`. The binding, population, and grammar are `paper-v4/experiment/native-query-binding.json`, `population-run/population.json`, and `generic-recipes.stottr`.

Under `paper-v4/experiment/results/`, `experiment-result.json` records counts and decision; `population-plan.json` and `population-provenance.json` retain construction and locator lineage; `replay-receipt.json` records the graph and history; `query-result.json` records raw rows and access counters; and `score.json` records the unscorable outcome. Focused guards live beside the executable modules in Appendix A.
