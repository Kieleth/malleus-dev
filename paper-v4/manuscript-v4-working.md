# Malleus: From Model Proposals to Replayable Knowledge

Luis Guzman Lorenzo. Author-review draft.

## Abstract

Language models can produce structured records, but well-formed output is not
yet accepted knowledge. Malleus connects a compiled ontology, a source-located
intermediate representation, an admission policy and an append-only semantic
ledger. A knowledge graph is reconstructed from that ledger and queried with
its evidence trace. We demonstrate this path with two model-produced captures
of one marine geoscience article and thirty graph queries. Both histories
reproduce their recorded graphs. Complete model-assisted review finds eight
and eleven questions fully covered, respectively, but neither initial capture
fully covers a composition question. The graph returns scoped counts, quantities, a spatial
relationship and a qualified hypothesis, while preserving inspectable omissions
and attribution errors. Separate amendments correct a funding attribution and
add a qualified evidence link that remains insufficient. A task-directed amendment
then connects two existing observations to the hypothesis, covering one composition
question under source-grounded model review. The result is an executable boundary between proposals
and accepted state, not a guarantee of source truth or complete extraction.

## 1. What becomes accepted

An agent maintaining a domain model needs more than plausible output. A reader
must be able to inspect what the system accepted, which evidence it cites and
which rules admitted it. This applies to a document's assertions as well as
operational state. The accepted model is a record of commitments, not an
unqualified description of reality.

Malleus separates proposing knowledge from accepting it. The ontology defines
the permitted structure. A history profile defines what a change means. An
identified policy governs admission. Accepted changes and their evidence are
retained; the graph is a replaceable projection rebuilt by replay.

This paper contributes an implemented composition of those boundaries and a
worked account of what survives them. Compiler and admission checks establish
structural and evidence-binding compliance. Source-grounded assessment examines
faithfulness. Explicit use requirements determine what counts as sufficient
coverage. None establishes the others. Replay separately checks reconstruction.
Keeping these distinctions visible makes a failure actionable instead of
treating every poor answer as the same problem.

## 2. Protocol

### 2.1 Ontology and history meaning

An **ontology** declares legal record types, properties, relations and controlled
values. A **change set** is an immutable proposal binding ordered operations to
their evidence, contract and prior state. A **ledger** retains semantic and
protocol history. **Replay** reconstructs accepted state under that contract.
A **locator** identifies evidence within a declared source reading. A **query**
reads the replayed graph without changing accepted state.

The ontology does not alone define what a ledger entry means. A source assertion,
an observation and a state replacement can have similar fields but different
semantics. Seed knowledge also needs an identified origin and admission. The
adopter chooses a history profile before population, including the unit of
change, time interpretation and allowed replacement.

Here the source-assertion profile treats one document capture as an atomic
assertion batch. The import is explicitly partial. Batch valid time denotes
capture/import order; assertion and domain times remain in retained assertions
when stated. Neither a ledger timestamp nor a sentence in an article becomes
an observed event in the physical world. Correcting a document representation
would therefore differ from recording a changed-world observation.

### 2.2 From proposed structure to a typed change

The producer proposes a LinkML ontology using identified domain-independent
roots and reusable research, metrology and chronology vocabulary. Compilation
resolves the declared sources and checks the supported structural contract.
It does not assess scientific adequacy.

Population pairs proposed records with a document capture. Each assertion
identifies a reading block, source wording, modality and the record fields it
formalizes. Typed gaps describe meaning the producer cannot represent. The
document adapter checks reading and capture identities, locators, source wording
under the declared normalization, and references into proposed records.

The adapter emits a PopulationPlan, the neutral intermediate representation.
Its grammar specifies record families, properties, relationships, derivations
and gaps. The compiler enforces the ontology over that representation.
Preparation retains the evidence package and composes a KnowledgeChangeSet
for admission. Source assertions remain retained evidence, not automatically
graph nodes. Record tracing joins the projected record to its plan, capture,
locator and modality.

The grammar makes interpretation inspectable; it does not invent it. One
sentence can map to several legal records while losing the relationship
between them. A valid locator establishes where to inspect a value, not that
the value follows from the cited passage.

### 2.3 Admission, replay and querying

The structural admission bundle checks the prepared change against the exact
base state, retained source/evidence identities and structural application.
Its outcomes are derived mechanically, not supplied as successful checks by
the model. Grouped admission is atomic: a refused application cannot leave a
partially accepted graph. Evidence retained during preparation may remain
after a later refusal; retained evidence and accepted state are distinct.

The experiment then discards live state, reopens the ledger and replays it.
Equality of the receipt and exported records checks reconstruction. Replay
does not regenerate model output: it reproduces an accepted omission or wrong
attribution as faithfully as a correct record.

Queries use public graph reads and return typed fields, stored prose and actual
relationship witnesses. Shared provenance does not create a semantic join.
Reading a qualification in a text field does not create a typed edge. A missing
answer remains missing rather than being completed from the source during
query execution.

## 3. Experiment

### 3.1 Source and captures

The source is Yu et al., [*Deep mantle earthquakes linked to CO2 degassing at the
Mid-Atlantic Ridge*](https://www.nature.com/articles/s41467-024-55792-9),
published in *Nature Communications* in 2025. One pinned text-layer reader
projects the eleven-page PDF into 186 identified blocks. Figures, raster
images, tabular layout and supplements are excluded from interpretation.

Captures A and B use independently proposed ontologies and populations from
fresh Opus 5 sessions. The producer inputs contain the selected reading and
identified Malleus instructions, not evaluation questions or previous answers.
Isolation is a declared task boundary over shared tools and files, not an
operating-system sandbox. These are author-selected engineering cases from
a development series, not a random sample of model performance.

### 3.2 Queries and source review

Thirty questions cover direct facts, relationships, quantities, qualifications
and composition, five each, plus three unavailable-information controls and two
paraphrases. They were frozen after the captures. Query programs were developed
retrospectively with access to the graphs. This is an exploratory demonstration,
not a prospective accuracy benchmark.

Selectors use declared fields and vocabulary, never expected answer values,
population identifiers or source locators. Quantities come from numeric fields;
alternative candidates remain separate. Each query run first reopens its
history and checks graph and receipt equality. The guarded query region
records zero source-file reads, network operations and named embedding imports.
This describes those Python executions, not every possible host operation.

One fresh model-assisted reviewer per capture inspects every question and
distinct central witness, the record or relation carrying an answer. Review
checks source support, coverage of required semantics, and whether answering
rows are linked. A third reviewer independently rechecks six preselected
examples. Reviewers can inspect exact source blocks and ontology definitions;
queries cannot use that evidence to supply missing answers.

COVERED means every listed semantic has a source-supported answering row;
PARTIAL means some do; NONE means none do. These are coverage labels, not
accuracy scores. COVERED can coexist with several candidates or unlinked rows.
Support is assessed over the complete projected witness. A PARTIAL witness
contributes none of its fields to coverage, even when some are correct. NONE
therefore need not mean an empty output or absence of information in the source.
The validator checks review consistency and locator resolution, not scientific
judgment. The review is model-assisted, not an expert annotation study.

## 4. Results

### 4.1 Reconstructed graphs and answer coverage

Both histories reopen to their recorded graphs and receipts. The first four
numeric columns describe graph and ledger structure; the last three summarize
each complete thirty-question review.

| Capture | Entities | Events | Relations | Ledger events | COVERED | PARTIAL | NONE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Capture A | 426 | 1 | 55 | 14 | 8 | 14 | 8 |
| Capture B | 508 | 1 | 26 | 14 | 11 | 9 | 10 |

Reviews inspect 78 and 63 distinct central witnesses, respectively. Both
captures account for all reading blocks, but neither fully covers any of the
five composition questions. Block accounting is not semantic completeness.

Three controls deliberately request information unavailable in the selected
reading. Their NONE labels are not failed positive questions. Both paraphrases
agree with their originals. Excluding controls, six of twenty-five questions
are fully covered in A and nine in B. The counts describe these captures and
reviews, not a statistical comparison.

### 4.2 Questions, returned facts and missing information

These six examples were selected before review. Questions are shortened below;
the [frozen question set](experiment-v4/competency-questions-v3.json) preserves
their full wording. A and B refer to the original captures, before amendments.
Source references use PDF page and text-layer block: p6/b2 means page 6, block 2.
Displayed answers summarize returned fields, not a separate generated answer.
Appendix A prints selected record extracts, source excerpts and review evidence.

| Question, shortened | A | B | Returned facts and coverage boundary |
| --- | --- | --- | --- |
| How many seismometers were deployed? (CQ-T1-02) | COVERED | COVERED | Count 19, with ocean-bottom instrument and deployment scope. All three requested items are present. The 17 useful instruments are a different population (p6/b2). |
| Which subsection is bounded by the fault, and where is its core complex? (CQ-T2-01) | PARTIAL | COVERED | Both return RC1 BOUNDED_BY detachment fault. A omits the core complex's side of the axis; B's returned statement places it east of the axis (p1/b5). |
| How much CO2 is in RC2 primary melts, in what unit, measured or calculated? (CQ-T3-02) | COVERED | COVERED | One Ba-based estimate supplies 0.4 to 3.0 wt%, RC2 primary-melt scope and CALCULATED status (p8/b7). Six candidates remain, not one unique estimate. |
| Which earthquake explanation is preferred, and how certain is it? (CQ-T4-01) | COVERED | COVERED | CO2 degassing from ascending melt beneath RC2; PREFERRED and HYPOTHESISED. These fields identify the authors' proposal, not an established cause (p5/b2). |
| Which volatile-content and earthquake-depth observations support degassing? (CQ-T5-01) | PARTIAL | PARTIAL | Only the preferred mechanism returns. No supporting observation, volatile estimate, observed depth or SUPPORTS edge is returned, although the source discusses them (p2/b6, p5/b5-b6). |
| What sulfur and chlorine concentrations are reported? (CQ-C-01) | NONE | NONE | No sulfur/chlorine values are returned. Source review finds none on the selected text surface. This is an unavailable-information control, not a failed positive question. |

**A covered answer with limits.** In B, the count record has count=19 and
count_scope identifying the deployed OBS network. The scope supplies the
instrument and deployment meaning in prose; there is no reconstructed deployment
event. Likewise, the CO2 answer preserves a separate Rb-based estimate of 0.5 to
2.8 wt%. COVERED means a supported, properly scoped answer is available, not that
the query resolved all six candidates to one concentration.

**Same record, different question.** B's preferred-hypothesis record supplies
the explanation, RC2 subject, PREFERRED disposition and HYPOTHESISED modality.
That covers CQ-T4-01. Returning the same record for CQ-T5-01 covers only the
mechanism, not the observations or their evidential connection. A correct claim
can therefore answer one question completely and another only partially.

### 4.3 What fails, and where

Both captures retain the passage connecting the degassing calculation to deep
microseismicity, but neither proposes its evidential relationship. Predicate
counts agree between population plans and replayed graphs. In these cases,
the missing SUPPORTS path is a representation omission, not a lost replay edge.

Source faithfulness can fail even when values have locators. At p3/b2, the
authors report that no active hydrothermal vents have been observed on RC2's
axis to date. A's claim name instead asserts their absence, with NEGATED modality
but no observation-to-date restriction. Review marks that witness PARTIAL:
absence of observations has become absence of vents. A valid locator and a
negative token do not preserve that distinction. Funding supplies a second
example below, where correct and incorrect attributions share one relation.

Query reachability is a different limitation: a correctly stored value may be
missed when its subject is on a linked record. Query-only corrections can
recover such content without changing the ledger, but cannot supply absent
relationships. The evidence distinguishes these causes rather than treating
all missing answers as extraction failures.

### 4.4 Two repairs through the same path

Two fresh Sol producers receive separate findings about Capture B, its accepted
records, reading and ontology, but no queries or evaluation answers. This is
feedback-guided repair, not a matched model comparison. Each case starts from
a copy of B's history; source, ontology and queries stay fixed.

**Funding: an admitted error becomes a supported answer.** CQ-T2-05 asks which
named grant agreement is attributed to which author. B originally returns an
ERC-to-Satish C. Singh FUNDS relation carrying both 339442_TransAtlanticILAB and
an ANR award. The source assigns the ANR award to ISblue, not this ERC relation
(p10/b44). The relation is PARTIAL, and the question is NONE despite returning
three rows: its one relevant witness mixes correct and incorrect attribution;
the other two rows concern different awards. The amendment supersedes that
relation with the same endpoints and only 339442_TransAtlanticILAB. Independent
review now finds the funding record, identifier, person and attribution covered.
The previous relation remains in history. This repairs the named agreement,
not all funding mentioned in the paragraph.

**Evidence: a supported addition still leaves a partial answer.** The second
amendment adds a SUPPORTS relation from approximately 25 km modelled saturation
depth to the preferred hypothesis (p5/b6). This is not an observed earthquake
depth. Independent review accepts it as the authors' qualified argument, not
proof of the cause. The unchanged CQ-T5-01 query reaches the model result and
hypothesis, but not the volatile-content estimates or observed earthquake
depths. Appendix A.3 gives the exact fields and requirement-level assessment.

The evidence query still does not assemble the geochemical and seismic evidence,
so its coverage remains PARTIAL. Both amendments pass ordinary admission and
ledger-only replay, preserving unrelated records and prior history. In each
case, 29 of 30 query outputs remain identical. Each producer's second assessment
requests no further change within its narrow finding; the incomplete composition
answer shows why that is not completeness. Original review counts remain unchanged.

### 4.5 One task-directed composition test

A separate fresh Sol producer receives CQ-T5-01 and its five requirements,
but no expected values or query code. Starting again from original B, it may
only add relations between existing entities and the existing hypothesis.
Source, ontology and queries remain fixed. Its first proposal adds two SUPPORTS
edges; no structural retry or semantic-review feedback is needed.

The unchanged query now links calculated RC2 melt CO2 of 0.4 to 3.0 wt% and
approximately 10 to 20 km observed microseismicity to the preferred hypothesis.
An independent model-assisted review finds both relations SUPPORTED and all
five requirements COVERED. Observation here includes a reported derivation,
not only direct measurement. The target remains PREFERRED and HYPOTHESISED;
SUPPORTS expresses the authors' argument, not established causality.

All 29 other outputs remain identical. The amendment admits, reopens and
reproduces its complete ledger and artifacts. Appendix B prints both paths,
the requirement-level assessment and omitted qualifications. This is one
bounded sufficiency gain, not a controlled test of question conditioning,
general completeness or a replacement for the original review totals.

## 5. Related work

Schema-guided extraction is established in SPIRES; OntoLogX combines
ontology-grounded extraction with retrieval and iterative correction.
Malleus claims neither structured generation nor diagnostic loops as new.
[SPIRES](https://arxiv.org/abs/2304.02711),
[OntoLogX](https://arxiv.org/abs/2510.01409).

PROV-O standardizes provenance relationships, OTTR supplies reusable graph
patterns, and Nexus combines validation, provenance, revisions and indexed
views. ESAA separates agent intentions from validation, event persistence and
state projection. These are direct precedents for the ingredients composed
here. The demonstrated contribution is the typed proposal-to-evidence-to-replay
path and its measured failure boundaries, not priority over those mechanisms.
[PROV-O](https://www.w3.org/TR/prov-o/), [OTTR](https://ottr.xyz/),
[Nexus](https://bluebrainnexus.io/products/nexus-delta/),
[ESAA](https://arxiv.org/abs/2602.23193).

The experiment has no matched RAG baseline. An embedding-free query execution
does not establish better answers, cost or scale. Retrieval could locate
evidence for a proposal without determining whether it becomes accepted state.
[Lewis et al.](https://arxiv.org/abs/2005.11401).

## 6. Limits and conclusion

One article and two selected captures do not establish general extraction
quality. Retrospective queries and model-assisted review limit causal and
scientific interpretation. Agreement on six rechecked examples does not estimate
reviewer reliability. Source support concerns the selected reading, not
independent geoscientific truth.

Single-process replay does not demonstrate distributed durability, concurrent
writers or cross-language conformance. Accepted interpretation is inspectable,
not guaranteed correct.

The amendment loop is not a general semantic repair system. Its unchanged source
establishes neither changed-world reasoning nor a reliable general stopping rule.
Robotics simulation is a candidate application, not evidence in this paper.

The present result is a complete document-to-graph path that returns useful
scoped facts and exposes missing arguments. Reproducibility, source support
and answer sufficiency remain separate, testable properties.

## Evidence and supplementary experiments

Capture A is run-20 and B is run-21, pinned to Core c95dba7. The
[complete review](answer-demonstration/REVIEW-RESULTS.md) binds all results.
Human ratification of these selective reviews is pending. The
[amendment record](answer-demonstration/REPAIR-RESULTS.md) includes the corrected
coordinator instruction, producer refusal, exact replays and preliminary review.
The [task-directed composition record](answer-demonstration/COMPOSITION-RESULTS.md)
retains its separate condition and independent assessment. Its Codex-authored
Markdown review uses v3 judgment meanings, not the primary review's full
validator-certified record format.

Separate [query corrections](answer-demonstration/QUERY-CORRECTION.md),
[subject-query tests](answer-demonstration/SUBJECT-QUERY.md) and an
[unmatched Sol-01 capture](answer-demonstration/FOLLOWUP-RESULTS.md), with
0/4/26 coverage, do not replace primary results.

Two further question-blind Sol populations used B's fixed ontology and unchanged
queries. Complete reviews yield 4/0/26 and 0/3/27 (COVERED/PARTIAL/NONE).
The first covers one composition question through stored prose despite having
no relations. These [fixed-schema executions](answer-demonstration/OVERNIGHT-RESULTS.md)
test a separate condition, not ontology-acquisition replicates or a model ranking.

Source, reading, ontology, ledger with replay receipt, and query binding are the
five identity groups. Source-bearing artifacts remain private: public files
alone cannot reproduce the experiment. Replaying retained output is distinct
from generating it again.

## Appendix A. Evidence for the worked claims

JSON exhibits select fields from retained query results or the identified
capture. Keys, values and identifiers are unchanged; unshown fields are omitted, not null.
Row indices are zero-based within each question. B supplies most exhibits;
A shows contrasting failures. Additional candidates and complete reviews remain retained.

Source excerpts are from Yu et al. (2025), DOI 10.1038/s41467-024-55792-9,
under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).
Only whitespace is collapsed in quotations. Locators identify the selected PDF
text layer, not figures or supplements. Model-assisted judgments remain
HUMAN RATIFICATION PENDING, not ratified publication evidence.

### A.1 A supported count and its evidence trace

**Question CQ-T1-02, B, row 0.** How many ocean-bottom seismometers were deployed?
The returned observation is:

```json
{
  "record_type": "ReportedObservation",
  "witness": {"record_id": "obs:obs-network-size-methods"},
  "record": {
    "count": 19,
    "count_scope": "OBSs deployed in the network",
    "assertion_modality": "STATED",
    "assertion_locator": "assertion:175"
  }
}
```

The public trace binds count and count_scope to assertion:175. This retained
capture excerpt connects that assertion to the source block; it is evidence
behind the graph, not a graph node:

```json
{
  "id": "assertion:175",
  "block": "page:6:block:002",
  "modality": "STATED"
}
```

**Source excerpt, page:6:block:002:** "A network of 19 OBSs was deployed,"

**Retained judgment.** Witness SUPPORTED; question COVERED. Its required
instrument_count, observing_system and deployment_event all cite row 0. The
last two are expressed by count_scope, not separate instrument or event nodes.
The same source block uses 17 for useful instruments; substituting that count
would change the population being counted. This exhibit establishes a scoped
answer, not a complete deployment model.

### A.2 Spatial and quantitative answers retain their scope

**Spatial question CQ-T2-01.** A returns the path feature:rc1 through
rel:rc1-bounded-by-detachment to feature:detachment-fault. Its relation_type is
BOUNDED_BY; the endpoints are named RC1 and detachment fault. There is no
returned side-of-axis qualifier. B also returns that kind of edge, but adds
claim:rti-amagmatic with subject feat:rc1. Its statement contains the following
source wording, including the core complex's position.

**Source excerpt, page:1:block:005:** "The RTI segment is amagmatic and bounded to the east by a westward dipping detachment fault with a prominent oceanic core complex (OCC) on the eastern side of the ridge axis"

**Retained judgment.** A is PARTIAL; B is COVERED. In B, named_subsection,
structural_feature, bounding_relation and side_of_axis cite its statement row 0.
The eastern qualifier is readable prose. Neither this judgment nor the explicit
BOUNDED_BY edge establishes a typed east-of relation.

**Quantity question CQ-T3-02, B, row 0 of six.** The Ba-based candidate is:

```json
{
  "witness": {"record_id": "obs:co2-ba90-rc2"},
  "record": {
    "quantity_kind": "CO2 (Ba90) in the primary melts for the segment RC2",
    "subject": "feat:rc2",
    "value_lower": 0.4, "value_upper": 3.0, "unit": "wt%",
    "assertion_modality": "CALCULATED",
    "determination": "ESTIMATED",
    "assertion_locator": "assertion:259"
  }
}
```

**Source comparison, page:8:block:007.** Primary-melt CO2 estimates for RC2 are
0.4 to 3.0 wt% from Ba and 0.5 to 2.8 wt% from Rb. The latter returns separately
as obs:co2-rb90-rc2, alongside RC3 estimates, an abstract-level estimate and a
lower-bound record.

**Retained judgment.** Row 0 covers bounded_quantity, concentration_unit,
quantity_subject and calculated_or_measured_status. The question is COVERED,
not uniquely resolved across all six candidates. Neither CALCULATED nor
ESTIMATED means directly measured undegassed primary melt.

### A.3 One supported hypothesis, two different coverage results

**Questions CQ-T4-01 and CQ-T5-01, B.** Both original outputs return this record:

```json
{
  "record_type": "ReportedClaim",
  "witness": {"record_id": "claim:hyp-co2-degassing"},
  "record": {
    "subject": "feat:rc2",
    "claim_kind": "MECHANISM_HYPOTHESIS",
    "hypothesis_disposition": "PREFERRED",
    "assertion_modality": "HYPOTHESISED",
    "assertion_locator": "assertion:133"
  }
}
```

The record's returned statement preserves this sentence:

**Source excerpt, page:5:block:002:** "The fourth possibility, and our preferred, is that the observed deep microseismicity beneath the segment RC2 is related to CO 2 degassing from the ascending melt."

**Retained judgment.** The witness is SUPPORTED. For CQ-T4-01 it supplies all
four requirements: causal_claim, preferred_disposition, epistemic_modality and
claim_subject. The question is COVERED. For CQ-T5-01 it supplies only the
causal_mechanism. The original composition output explicitly has no path:

```json
{
  "question_id": "CQ-T5-01",
  "paths": []
}
```

**After the evidence amendment, row 1.** A new relation reaches that same
hypothesis. The following selects its relation, endpoints and quantity fields:

```json
{
  "witness": {
    "relation_id": "repair:evidence:saturation-depth-supports-co2-degassing",
    "source_id": "obs:saturation-depth",
    "target_id": "claim:hyp-co2-degassing"
  },
  "relation": {"relation_type": "SUPPORTS"},
  "source": {
    "value_lower": 25.0, "value_upper": 25.0, "unit": "km",
    "determination": "MODELLED",
    "value_qualification": "APPROXIMATE",
    "assertion_modality": "HYPOTHESISED"
  },
  "target": {
    "hypothesis_disposition": "PREFERRED",
    "assertion_modality": "HYPOTHESISED"
  }
}
```

**Source excerpt, page:5:block:006:** "would start degassing CO2, in agreement with the observed deep microseismicity."

The preceding source conditions are melt above 0.7 wt% CO2, approximately
0.7 GPa and 1250 degrees C. The approximately 25 km value is predicted saturation
depth, not the observed earthquake depths. The edge alone carries SUPPORTS;
the conditional, source-attributed interpretation requires its endpoints and trace.

The retained reviews give this requirement-level account. A row reference means
supported coverage; the uppercase absence codes are the original review terms.

| Required semantic | Before | After | Evidence or remaining gap |
| --- | --- | --- | --- |
| causal_mechanism | Row 0 | Row 0 | Hypothesis, not established cause. |
| supporting_observation | Absent | Row 1 | Before: UNREACHED_RECORD. After: a model result in the ontology's broad observation sense, not an empirical earthquake measurement. |
| geochemical_evidence | Absent | Absent | UNREACHED_RECORD. Volatile-content estimates remain outside this output. |
| seismic_evidence | Absent | Absent | UNREACHED_RECORD. The observed RC2 depths in page:2:block:006 are not returned. |
| evidence_relation | Absent | Row 1 | Before: NOT_MODELLED. After: the new model-result-to-hypothesis relation, not a join of both requested evidence types. |

Coverage stays PARTIAL. Assembly changes from ONE_ROW to LINKED_ROWS, not a
higher grade. Requiring an empirical supporting observation would leave that
requirement absent too; the full composition question remains incomplete.

### A.4 Nonempty does not mean supported: funding before and after

**Question CQ-T2-05, B, original row 0 of three.** The relevant named agreement
appears on this ERC-to-Singh relation, together with a second award:

```json
{
  "witness": {"relation_id": "rel:erc-funds-singh"},
  "source": {"name": "European Research Council"},
  "target": {"name": "Satish C. Singh"},
  "relation": {
    "relation_type": "FUNDS",
    "award_identifier": ["339442_TransAtlanticILAB", "ANR--17-EURE-0015"]
  }
}
```

**Source excerpt, page:10:block:044:** "Grant agreement no. 339442_TransAtlanticILAB to S.C.S."

The same paragraph assigns the ANR award to ISblue. The byline and correspondence
identify S.C.S. as Satish C. Singh. The displayed ANR spelling is retained output,
not a correction of the source's text-layer punctuation.

**Retained judgment before.** Witness PARTIAL; question NONE under the support
gate. funding_record, grant_identifier, person and attribution_relation lack a
fully supported answering witness, despite correct subfields. The other two
rows concern NSFC and Zhejiang funding to Yu, not this named agreement.

**After amendment, row 2 of three.** The replacement keeps the endpoints and
only the supported agreement:

```json
{
  "witness": {"relation_id": "repair:funding:erc-funds-singh"},
  "source": {"name": "European Research Council"},
  "target": {"name": "Satish C. Singh"},
  "relation": {
    "relation_type": "FUNDS",
    "award_identifier": ["339442_TransAtlanticILAB"]
  }
}
```

**Retained judgment after.** Witness SUPPORTED; all four requirements cite row 2;
question COVERED. The original relation remains in history, superseded by the
replacement. The two other funding paths are unchanged but occupy rows 0 and 1.
This is a correction of one attribution, not full capture of the funding paragraph.

### A.5 An admitted statement can lose a source qualification

**Capture A, CQ-T4-04 witness.** This is a source-support failure, not a
compiler or replay refusal:

```json
{
  "witness": {"record_id": "claim:no-active-vents-rc2"},
  "record": {
    "name": "absence of active hydrothermal vents on the RC2 axis",
    "assertion_modality": "NEGATED",
    "assertion_locator": "assertion:0087",
    "subject": "feature:rc2"
  }
}
```

**Source excerpt, page:3:block:002:** "To date, there are no observations of active hydrothermal vents on the segment RC2 axis."

**Retained judgment.** Witness PARTIAL. The site and negative polarity match,
but the returned name asserts absence of vents instead of the absence of
observations available to date. The correct locator makes that loss inspectable;
it does not prevent it. No amendment of this witness is reported here.

### A.6 An empty unavailable-information control

**Question CQ-C-01, B.** The sulfur/chlorine query returns:

```json
{
  "question_id": "CQ-C-01",
  "outcome": "NO_CANDIDATE",
  "rows": [],
  "paths": [],
  "witness_ids": []
}
```

**Retained judgment.** NONE. bounded_quantity, concentration_unit and
measurement_status carry NOT_IN_SOURCE. sample_set carries UNREACHED_RECORD:
the graph has sample:morb, but this output returns no sample record. The review
checked page:5:block:004 and page:8:block:005 through page:8:block:007 and the
retained assertion inventory. No single quotation proves document-wide absence.
This is a model-assisted negative finding on the selected text surface, not a
claim about figures, supplements or all available geochemical data. Unlike A.4,
this is an unavailable-information control, not rejected mixed attribution.

### A.7 Artifact coordinates and limits of this appendix

SHA-256 coordinates for Capture B. Source PDF:
7d3d42bf17cbf1280a63cbb164254b5b839f4e380d458086065cb309caf1a2a9.
Selected reading:
f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17.
Ontology:
6fbb99a283ddb057a2690e0bf7530a6a16bac7890f36780b4d397588f8592e6a.

B's original ledger head is
a2f3ad2e6ef4b8a33d508ae5eee4d0a654f16e512dc4189fdf043230cab3e217;
admitted and reopened receipt:
2cab922f229d578f183a647e445d0b99348ce2f931fb161a0652547a29a6e832.
The retained result reports equal records and receipts after reopen. Query binding:
d73119a074c4cef1f8f5750c4c57116a8c74e4c03682429ad7c280a3b31374a4;
answer program:
389c4ff9565304be63caf432ece17ef108f3a0b2f229fbc53be70caf962dc698.
Both repairs reuse those programs.

Original excerpts come from the retained pilot-03/run-20 and pilot-03/run-21
query-result.json files; the amendments come from repair-02/funding/attempt-01
and repair-02/evidence/attempt-01. Original judgments are in the complete
review-01 records, not inferred from the query's candidate status. The independent
amendment review is repair-02/review-01/review.md. It assesses source support
and changed answers; the coordinator's separate admission/reproduction checks
establish the replay claims. These are different evidence roles.

All paths in the preceding paragraph are relative to the retained private
paper-v4-answer-demonstration directory. The appendix exposes selected evidence,
but is not a complete reproduction package. Full source-bearing material remains
private, and a publication-accessible package and human ratification remain open.

## Appendix B. Task-directed composition evidence

This separate amendment starts from original B, not the evidence repair in A.3.
The producer receives CQ-T5-01 and its five requirements, but no expected answer
values or query code. Its first candidate adds only the two relations shown
below. The unchanged query returns the original hypothesis as row 0 and these
two additional witnesses as rows 1 and 2. Field selections follow Appendix A's
transcription and source-attribution rules.

### B.1 Two observations reach one qualified hypothesis

**CQ-T5-01, amended row 1.** Calculated volatile content:

```json
{
  "witness": {
    "relation_id": "repair:evidence:co2-enrichment-supports-degassing",
    "source_id": "obs:co2-calculated-rc2",
    "target_id": "claim:hyp-co2-degassing"
  },
  "relation": {"relation_type": "SUPPORTS"},
  "source": {
    "value_lower": 0.4, "value_upper": 3.0, "unit": "wt%",
    "determination": "DERIVED",
    "assertion_modality": "CALCULATED",
    "subject": "feat:rc2", "assertion_locator": "assertion:147"
  },
  "target": {
    "hypothesis_disposition": "PREFERRED",
    "assertion_modality": "HYPOTHESISED"
  }
}
```

**CQ-T5-01, amended row 2.** Observed earthquake depth:

```json
{
  "witness": {
    "relation_id": "repair:evidence:deep-microseismicity-supports-degassing",
    "source_id": "obs:deep-microseismicity-rc2",
    "target_id": "claim:hyp-co2-degassing"
  },
  "relation": {"relation_type": "SUPPORTS"},
  "source": {
    "value_lower": 10.0, "value_upper": 20.0, "unit": "km",
    "value_qualification": "APPROXIMATE",
    "assertion_modality": "MEASURED",
    "subject": "feat:rc2", "assertion_locator": "assertion:055"
  },
  "target": {
    "hypothesis_disposition": "PREFERRED",
    "assertion_modality": "HYPOTHESISED"
  }
}
```

**Source comparison.** page:5:block:005 reports calculated RC2 melt CO2 of
0.4 to 3.0 wt%, compared with less enriched RC3 melts. page:2:block:004 reports
approximately 10 to 20 km microseismicity beneath the RC2 axis and calls the
record a brief time snapshot. This is the returned broad observed range, not
the 16 to 19 km range discussed in page:2:block:006 or the modelled 25 km in A.3.
The new relation assertions cite page:5:block:005 and page:5:block:002;
their existing endpoints trace separately to the quantitative source assertions.

### B.2 Source support and question coverage

Independent review judges row 0 and both added relation witnesses SUPPORTED.
The SUPPORTS direction requires context across page 5, blocks 2 through 6;
the relation's short assertion excerpt alone does not establish the argument.
The table preserves the five frozen requirements and zero-based row references.

| Required semantic | Before | After | What the answering witness establishes |
| --- | --- | --- | --- |
| causal_mechanism | Row 0 | Row 0 | The preferred, hypothesised explanation remains qualified. |
| supporting_observation | Absent | Rows 1, 2 | Calculated volatile content and observed seismic depth, with different bases. |
| geochemical_evidence | Absent | Row 1 | RC2 melt CO2, 0.4 to 3.0 wt%, CALCULATED and DERIVED. |
| seismic_evidence | Absent | Row 2 | RC2 microseismicity, approximately 10 to 20 km, MEASURED. |
| evidence_relation | Absent | Rows 1, 2 | Two actual SUPPORTS records share the same hypothesis target. |

Coverage changes from PARTIAL to COVERED, with assembly ONE_ROW to LINKED_ROWS.
The review accepts the ontology's broad reported-observation meaning, including
calculation from geochemical data. It does not treat calculated melt CO2 as
directly measured or seismically located depth as a direct instrument reading.

**Remaining qualifications.** The returned rows omit the geochemical proxy
assumptions, RC3 comparison, an explicit primary-melt stage field, the seismic
time-snapshot caveat, acquisition duration and depth reference surface. These
remain inspectable in source context. The review finds no unsupported addition
or semantic regression, but does not claim a complete causal argument. Source
faithfulness is preserved; intended-use sufficiency improves for this question.

### B.3 Replay coordinates

The added relations admit in one change set. The ledger grows from 14 to 20
events, preserving its baseline byte prefix and all existing records. The
graph has 537 current records. Only CQ-T5-01 changes; the other 29 outputs are
identical. A separate execution reproduces the complete ledger and all seven
result artifacts byte-for-byte. Model-assisted judgments remain
HUMAN RATIFICATION PENDING.

The source, reading, ontology and query identities are those in A.7. This
condition's ledger head is
562c8173fbfde84cbca9070a747eb4d201a58043d2796424d5fcaa5dab22a0ca;
its reopened receipt is
6ce3de3fd09dec3310d279a18c51fe445bc76af540e507a575f78bf8aa527013.
The retained output is composition-01/evidence/attempt-01/query-result.json;
the separate review is composition-01/review-01/review.md, under the same
private evidence root as A.7. Original review totals remain unchanged.
