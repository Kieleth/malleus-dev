# Persistent domain knowledge beyond one context window

Version: 0.2. Date: 2026-09-15.
Status: BEAM weather-app capture and replay complete; answer comparison pending.

Latest author decision, DS-003: "small BEAM calibration, have others in the
pipeline justin case". The [calibration plan](beam-calibration/PLAN.md) and
[work ledger](beam-calibration/WORK-LEDGER.md) now govern this bounded front.
LongMemEval and Kubernetes remain alternatives, not concurrent runs or automatic
fallbacks. The research and unselected proposals below retain their original
scope; the earlier no-selection statements are historical, superseded by DS-003.

## What we are trying to establish

Can one explicit, evidence-linked domain model survive its acquiring session,
serve different consumers, and change responsibly when new evidence arrives?
The corpus should eventually exceed the selected reader's context window.
That is a scale condition, not the contribution by itself.

For a concrete example, a first model reads a technical project's documentation,
design decisions and release material. A fresh model checks a configuration;
another explains the finding and its source. Later material changes a relevant
rule. The system must distinguish a new version from a mistaken earlier reading,
review affected interpretations, preserve unaffected ones, and reproduce the
earlier accepted state. This is a proposed test, not a delivered capability or
a claim that every later document supersedes earlier evidence.

The four fronts test different things, not four levels of increasing prestige:

| Front | Intended question |
| :--- | :--- |
| Small Shop, Core-owned | Can structured domain changes be admitted and reconstructed? |
| Marine PDF, paper-owned | Can acquired meaning preserve source context and support useful queries? |
| Robotics, separately owned | Can observations and actions update an agent's accepted environment model? |
| Proposed large domain | Can acquired meaning be reused and maintained across sessions, consumers and source updates at scale? |

This table describes purposes, not a fresh audit of those fronts' results.
The [exoplanet plan](../exoplanets/experiment-plan.md) is paused at version 0.6;
its reading and source-preparation findings remain retained. No astronomy model
experiment ran. We are not transferring its unresolved ingestion work here.

Five properties need separate evidence: source-faithful representation, useful
cross-source connections, reuse without the creator's conversation, justified
updates with historical reconstruction, and total acquisition/maintenance/use
cost. Compiler success establishes none of the semantic properties by itself.
Large-scale QA alone does not establish the protocol's contribution either.

## What the related work changes

The existing [intellectual-substrate review](../../design/MALLEUS_INTELLECTUAL_SUBSTRATE.md)
already places Malleus among typed knowledge representation, truth maintenance,
belief revision, provenance and replay. Its empirical-program section requires
matched controls and separate correctness, coverage, revision and recovery
measurements. Historical implementation coordinates in that review are not
current capability evidence.

Primary-source inspection in this pass adds the following practical constraints:

| Work | Relevant mechanism or evaluation | Implication for our test |
| :--- | :--- | :--- |
| [GraphRAG, sections 3 and 4.1](https://arxiv.org/html/2404.16130v2) | Graph communities and summaries; podcast and news corpora around 1M and 1.7M tokens | Large-corpus graph retrieval is established. Include cross-source tasks, but do not mistake preferred summaries for verified facts. |
| [HippoRAG 2, abstract and evaluation overview](https://arxiv.org/html/2502.14802v1) | Factual, associative and sense-making memory | Test exact retrieval as well as connected reasoning. A graph must not sacrifice simple facts for a more impressive narrative. |
| [Zep/Graphiti, sections 2 and 2.2.3](https://arxiv.org/html/2501.13956v1) | Episodic sources, temporal facts and invalidation of contradictory edges | Updating a graph while retaining history is prior art. Compare declared acceptance and update policies, including when later information should not replace earlier information. |
| [LongMemEval, sections 3.1 to 3.3](https://arxiv.org/html/2410.10813v2) | Extraction, multi-session reasoning, updates, time and abstention; approximately 1.5M-token M setting | Reuse published diagnostic categories and independently supplied questions. Its constructed histories are not a real technical-domain corpus. |
| [BEAM, sections 2.2 and 2.3](https://arxiv.org/html/2510.27246v2) | Synthetic conversations up to 10M tokens, 20 validated questions per conversation and criterion-level assessment | Multiple tasks can reuse one acquired history. Synthetic coherence and model-assisted judging remain limitations. |

The recent local [INDRA investigation](../../private/kg-representation-recon-2026-09-15/indra/INDRA-TRANSFER.md)
is especially relevant to representation rather than length: retain incomplete,
qualified meaning separately from the assumptions needed by a consumer.
Current [INDRA statement documentation](https://indra.readthedocs.io/en/latest/modules/statements.html)
confirms typed mechanisms, context, evidence and exchangeable JSON. It is a
precedent to inherit, not evidence of a Malleus integration.

Reviewer conclusion: the shared goal overlaps substantially with graph memory
and knowledge-representation work. The candidate Malleus contribution is the
tested composition of explicit meaning, acceptance, evidence and reconstructible
change across consumers. This pass does not establish novelty or a missing
capability in any entire competing system.

## Dataset options, not selections

### A. Published memory benchmark first

[LongMemEval](https://github.com/xiaowu0162/LongMemEval) provides JSON histories,
dates, questions and supporting-session labels. Its M setting is reported around
1.5M tokens per instance. Each problem has its own history; unrelated instances
must not be merged into one person's domain. The cleaned release exists, but
the hosted preview failed on a mixed-type answer column during this inspection.
That does not establish malformed raw JSON. No raw LongMemEval instance was
downloaded or validated in either inspection pass.

[BEAM](https://github.com/mohammadtavakoli78/BEAM) better supports repeated use of
one acquired history because each conversation has several questions. Its
[dataset card](https://huggingface.co/datasets/Mohammadta/BEAM) includes chat,
generation plans, profiles and evaluation material together. Only the declared
conversation evidence may reach acquisition. Plans, answer criteria and question
labels must remain evaluator-only. The [10M card](https://huggingface.co/datasets/Mohammadta/BEAM-10M)
reports a working-data viewer size limit, not corrupt conversation bytes.
DS-002 checks two small native GitHub examples. The 10M case remains unparsed;
its hosted-viewer limitation does not establish malformed underlying data.

Benefit: existing questions, readable native data, known baselines and size
settings. Limit: conversational memory, not a real scientific or engineering
domain, and length partly reflects constructed material. Dataset labels are
author reports until we count the exact selected evidence with a named tokenizer.
This is the preferred option for a bounded diagnostic before creating an eval.

### B. Versioned technical domain

Candidate: Kubernetes English documentation, enhancement proposals, release
material and selected structured configuration/API records. Use one coherent
topic scope and two exact repository snapshots, not a pile of unrelated code
or repeated versions counted as novel knowledge.

Inspected a real native pair: the [nftables proposal](https://github.com/kubernetes/enhancements/blob/master/keps/sig-network/3866-nftables-proxy/README.md)
has design rationale, caveats, compatibility and test plans; its
[YAML metadata](https://raw.githubusercontent.com/kubernetes/enhancements/master/keps/sig-network/3866-nftables-proxy/kep.yaml)
names the owning group, feature gate and release milestones. These mutable
sources establish a usable source family, not a frozen corpus. The selected
domain's token count and complete license closure are unmeasured.

A concrete interpretation trap already exists: the
[PodDisruptionBudget migration guidance](https://kubernetes.io/docs/reference/using-api/deprecation-guide/)
distinguishes an empty selector from an absent selector, with different empty-
selector behaviour across API versions. A configuration checker and an
explanatory model could consume the same version-qualified representation.
Recognizing this example alone is only a local lookup. The large test must also
require evidence across documents and verify that unaffected findings survive
an update. Public pretraining knowledge is a confound, so include a no-source
control and demand exact frozen-source support.

Benefit: a convincing non-financial changing-domain use case with native text
and structured artifacts. Limit: we must author and independently verify the
evaluation cases. We have not demonstrated that the chosen coherent subset
exceeds 1M tokens. This is the preferred option for the full application story,
not an instruction to select Kubernetes or build a cluster.

### C. Native scientific literature

Candidate: one biological mechanism across a licensed subset of PMC articles,
with explicit evidence and disagreements. [PMC](https://pmc.ncbi.nlm.nih.gov/tools/openftlist/)
requires per-article license checks and approved retrieval services;
[BioC](https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PMC/) supplies XML/JSON
article representations. This avoids making PDF text extraction the input
format. It does not eliminate figure interpretation, scientific qualifications
or expert assessment. Corpus size, reading fidelity and answer cases are not
established. Keep this behind the two options above if acquisition overhead is
the immediate concern.

GraphRAG's news/podcast collections remain useful comparison corpora. They are
less direct tests of changing domain rules than B. Raw telescope samples,
giant generated logs and concatenated PDFs are poor choices merely to cross a
token threshold. Structured data should stay structured, not be inflated into
text to manufacture a context-window limitation.

## Proposed milestones after the author chooses

1. **Freeze the claim and evidence packet.** Check one raw sample, license,
   exact version, source-to-evaluator separation and token count. Define the
   semantic unit, source authority and update policy before constructing an
   ontology. State how uncertainty, conflict and version scope remain visible.
   Deliver a packet that a fresh producer can use without investigator help.
2. **Establish a small working control.** Acquire a bounded case without the
   evaluation questions. Test both ontology expressiveness and populated
   meaning. Fresh consumers receive the ontology, accepted graph and documented
   read interfaces, not the creator's conversation. Keep creation and operating
   conditions explicit. Check ordinary retrieval, composition and abstention.
3. **Test a meaningful update.** Add source evidence in declared order. Review
   the bounded interpretation set, including previously completed items. Separate
   detail, interpretation correction and actual domain change. Require a
   supported correction, justified no-change, conflict or specific unresolved
   explanation. Replay the older state and check unaffected results too.
4. **Scale and test reuse.** Use a coherent, measured corpus beyond the chosen
   context limit, then repeat with fresh consumers and held-out tasks. Compare
   against a tool-enabled reader with the same raw sources, hybrid retrieval,
   and the closest appropriate graph-memory system. Start with the cheapest
   informative control; do not run every baseline by default.

Fairness requires matched source access, producer/reader models, context limits
and inference opportunities. A full-context control belongs on the small case;
the large baseline must be allowed retrieval or iterative reading, not artificial
truncation. If a model can inspect raw sources from graph evidence links, report
that access and its cost. A graph-only ablation can separately test what was
actually captured. A normalized database is also a serious baseline when the
domain facts are already structured.

Report task success and source-faithfulness separately from stale answers,
unsupported changes, missed affected interpretations, preserved valid results,
replay agreement, cost and latency. Cost includes acquisition, review, repair,
updates and repeated queries for every condition. Saving query tokens alone is
not evidence of overall savings. Fresh-model transfer is not cross-language
protocol conformance. Passing a semantic rubric is not source truth.

**Historical DS-001 choice, resolved by DS-003:** published benchmark first, or the custom
versioned-domain demonstration. Recommendation: benchmark first if the immediate
priority is diagnostic results without another data-preparation project;
Kubernetes if the priority is the strongest concrete application of shared,
changing domain knowledge. No choice is made by this document.

## Research record and scope

The bounded Recon notebook is under
`private/malleus-domain-scale-recon-2026-09-15/`. It preserves inspected sources,
claim-level comparison and access limits. It is structural research capture,
not accepted domain knowledge. No benchmark, model comparison, source ingestion,
new Core requirement or manuscript result was produced in this pass.

DS-001, 2026-09-15: recorded the author-requested pause in EXO-012, reread the
prior research and current paper scope, inspected the primary sources above,
and wrote this decision brief. Recon validation and generation passed for 68
records; the generated report and exact Zep comparison were inspected. Its
unassessed axes remain unknown, not alleged Zep omissions. No runtime code was
changed and no model or benchmark was run. The two dataset-viewer errors are
access findings, not defects diagnosed in their underlying data. No shared
plan, manuscript, Core path, commit or branch/ref was changed by this work.

## DS-002: native-source probe, 2026-09-15

The authorized resume continues research only. Exoplanets remains paused and
the marine experiment remains separately governed. No runtime pin changes.

### Observed evidence

Retrieved and parsed two BEAM conversations and their question files at commit
`b2da22eac88bb0874c64665f13457eb99835774a`. The first numeric `100K` case was
a format probe. The second followed its official non-financial weather-app
topic. Neither was selected as an experimental condition. No upstream code or
pickle was executed and no source was edited.

| Mechanical check | Case 1 | Weather-app case 2 |
| :--- | ---: | ---: |
| JSON batches | 3 | 3 |
| Messages, all with unique IDs | 188 | 200 |
| Questions with nonempty rubrics | 20 | 20 |
| Numeric evidence references, all resolving | 55 | 55 |
| User-content characters | 108,293 | 91,696 |
| Assistant-content characters | 414,722 | 401,476 |

The full message shape and numeric reference closure pass. Semantic inspection
is limited to named examples, not all forty answers. These are source checks,
not model scores or token counts. Source strings include generation markers;
the inspected upstream reader projects role/content rather than full objects.
Any future reading must be declared and identical across compared systems.
Generation plans, profiles, evaluation labels and rubrics are not extra evidence
for the producer. Assistant advice is not evidence of completed user action.

The weather-app [conversation](https://github.com/mohammadtavakoli78/BEAM/blob/b2da22eac88bb0874c64665f13457eb99835774a/chats/100K/2/chat.json)
contains a reported quota change, 1,000 to 1,200 calls per day, in messages 32
and 66. Messages 114 and 128 distinguish 65% achieved test coverage, a 100%
goal, and later 78% achieved coverage. These concern a simulated project, not
the real weather service's current terms or an application we measured.
Its separate [questions](https://github.com/mohammadtavakoli78/BEAM/blob/b2da22eac88bb0874c64665f13457eb99835774a/chats/100K/2/probing_questions/probing_questions.json)
include the corresponding update questions. This is useful calibration material,
not a new held-out evaluation created here.

The real-domain probe inspected KEP-3866 YAML and design prose at the
[beta update](https://github.com/kubernetes/enhancements/tree/c386ddbdded0adf1fe0f6769cf4894bee339ea7a/keps/sig-network/3866-nftables-proxy)
and [GA update](https://github.com/kubernetes/enhancements/tree/9c3c33231caaa328690354acfa0cd87b0deb682b/keps/sig-network/3866-nftables-proxy).
Current maturity changes from beta to stable, while both already name v1.33 as
the stable milestone. The YAML comments allow milestones to be targets: that
field alone cannot prove a release happened. The inspected rollback and version-
skew qualifications persist. This gives an update-plus-preservation example,
not a live cluster observation or a measured million-token corpus.

Raw files were inspected through the GitHub connector and not retained locally.
Exact repository paths and GitHub-declared blob IDs are in
`private/malleus-domain-scale-recon-2026-09-15/source-probe.json`. This is not
an experiment byte-freeze. Neither a directory label nor JSON character count
establishes the eventual source-token count.

### Bounded proposals, awaiting author choice

**Benchmark-first:** one weather-app calibration. Acquire only the declared
conversation evidence without test questions; give the resulting representation
to two fresh readers; run the twenty existing questions; inspect current and
historical support for the two updates. Each question starts independently,
without earlier test answers. Preserve goals separately from reported results.
Stale values, unsupported acceptance, lost history and promoted goals are
distinct failures. A correct answer without a captured evidence path does not
establish that the representation supplied it.

Compare the small case with direct-context reading and retrieval under matched
conditions. No accuracy victory is assumed. A later, separately chosen case
must actually exceed the selected context limit and repeat the reuse test.
The calibration cannot establish benchmark-wide or >1M performance. Choose the
larger case independently of which calibration answers succeeded.

**Technical-domain-first:** one version-qualified feature and its explanatory
constraints at the two exact revisions. A checking consumer and an explaining
consumer must distinguish a milestone target from achieved maturity and preserve
unchanged rollback caveats. Existing pretrained knowledge remains a confound;
include a no-source control and require exact source support. A large corpus
and independent evaluation set would still need preparation.

Both proposals are paper-owned. The optional Core checker can account for a
declared set of reviews if selected; it neither chooses that set nor decides
meaning. No concrete missing Core mechanism was established by this probe.
No model, accepted change, new runtime, commit or integration was launched.
Recon validation and rebuild passed for 80 current research records. The report
and BEAM comparison were inspected; unassessed axes remain unknown. Local links,
recorded inspection counts and the unchanged exoplanet pause were checked.

## DS-003: author selects small BEAM calibration, 2026-09-15

Selected the non-financial weather-app case proposed in DS-002. Retained the
exact conversation and evaluator source bytes separately under ignored private
storage, verifying both against their pinned Git blobs and byte lengths. The
reading preserves all 200 messages and source order; all 55 evaluator message
references resolve. A 37-test preparation suite checks corruption refusal,
text/role/locator preservation, annotation exclusion, deterministic rebuilding
and no overwrite. These are input checks, not semantic assessment or model scores.

The private packet is not yet a verified isolated model workspace. Token count,
execution setup, source-assertion policy and reader/evaluation conditions still
need their launch preflight. A fresh Sol setup with separate current-Core pin
was proposed to Luis without changing any historical run. No model, population,
ledger, manuscript, Core path, shared ref or commit was changed. The natural
source batches do not isolate the inspected update pairs, so incremental change
will require its own declared prefix/suffix boundary rather than retrospective
answers being relabelled as an update experiment.

GitHub's pinned repository licence is MIT; the hosted dataset card reports
CC-BY-SA. Preserve that scope uncertainty before distributing corpus bytes.
LongMemEval and Kubernetes have explicit activation checks in the plan.

## DS-004: execution approved and first capture observed, 2026-09-15

Luis confirmed one fresh Sol producer and two fresh Sol readers on a separate
frozen current Core. The producer ran from scratch on Core 18015352. Its observed
effort was low, not the inherited effort anticipated in the input manifest.
The complete declared inputs reached the model. It proposed ontology and records,
admitted one population through the public API, and reopened the history. Parent
replay reproduced the exact graph and receipt from a ledger copy.

[RESULT-01.md](beam-calibration/RESULT-01.md) separates this structural success
from a concrete acquisition error: a comma-grouped quota of 1,200 became 200 in
the model-generated mapping. The original source remains intact and traceable.
The result also exposes the difference between classified source pointers and
meaning available directly in graph fields. No semantic completeness is claimed.

Reader execution has not started. Four upstream evaluation criteria require
adjudication, and the absence-control screen is incomplete. The choice between
two batched readers and forty independent answer sessions is also open. No
rubric was repaired silently, no case removed and no overall score reported.
LongMemEval and Kubernetes remain in reserve. Core, the marine experiment and
the manuscript remain unchanged by this front.
