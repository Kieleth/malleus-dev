# Knowledge packs, typed gaps, and the revision loop

Status: design decided in conversation on 2026-09-03 between Luis and the overseer session, after the three-producer paper runs. The population path, additive revision, domain-history profiles, three optional packs, structural grounding rite, and minimum edited-pack conformance rite are implemented. Sections marked "open" remain undecided.

## Why

Three fresh producer sessions ran the same document protocol on the same source under the same brief: gpt-5.6-sol, Claude Sonnet 5, Claude Opus 5. All three compiled, admitted and replayed cleanly. Their answerability differed because each invented its own vocabulary for the same five ideas: a quantity with bounds, a unit, a measured-versus-calculated basis, a time datum, an instrument deployment. gpt gave one observation record lower and upper bounds and answered the range question; the two Claude producers gave one value per record, the source reports ranges, the population rule forbids inventing a point, and their graphs stayed near empty. None of the three could carry "the authors prefer this mechanism" because no vocabulary for a hedged assertion was offered, and the brief read as forbidding one.

The skill's own promotion rule says a concept reinvented by independent consumers moves down a layer. Three producers reinvented five concepts in one afternoon. The layer they belong to does not exist yet: it sits between the five-primitive root and the project ontology.

## The layering

The adoption guide already describes a stack where each layer imports the one below and only adds, and a concept moves down only when a second consumer needs it. This design adds one rung and names it with the guide's own word, pack.

```
malleus.yaml              five primitives, four mixins. Never edited.
  packs/metrology.yaml    quantities: value with bounds, unit, uncertainty, determination, ratio, count
  packs/chronology.yaml   instants, intervals, order-only time, precision, reference system
  packs/research.yaml     claim, assertion modality, observation, method, instrument, campaign, sample, source, evidence
    <project>.yaml        the project's own terms, extending pack concepts
```

Rules:

- A pack imports the root, and may import another pack. `research` imports `metrology` and `chronology`.
- A project imports the packs it wants, or copies one and edits the copy, or replaces one with its own behind the same names. Malleus ships packs; it does not require them.
- Packs are generic capability vocabularies. Malleus ships no domain pack (no geoscience, no finance). Domain terms live in the project ontology. The existing files under `ontology/domains/` are fleet and research ontologies at the project rung, not packs.
- Each pack follows root style: slot bundles as mixins that any record class can wear, plus a small set of reference classes that wear them, plus enums. Mixins keep a graph small (one node carries its quantity); reference classes make records findable by type.
- The promotion rule applies in both directions: a project concept used by a second project is a pack candidate; a pack concept used by every pack is a root candidate. Nothing moves before the second consumer exists.

## Naming, grounded

Luis asked for names taken from an existing taxonomy of areas of knowledge rather than invented. Each pack is named after the body of knowledge whose vocabulary it borrows, located in the Dewey Decimal Classification (DDC) and the Wikipedia outline of academic disciplines, and its terms are taken from one seminal vocabulary in that area.

| Pack | Area of knowledge | DDC | Seminal vocabulary the terms follow | Terms borrowed |
| --- | --- | --- | --- | --- |
| `metrology` | The science of measurement; formal and physical sciences in the outline of disciplines | 530.8 Physical measurement | JCGM 200:2012, the International Vocabulary of Metrology (VIM), 3rd edition; QUDT as the ontology precedent | quantity, quantity value, measurement unit, measurement uncertainty, measured versus derived value, quantity kind |
| `chronology` | Time and its reckoning | 529 Chronology | W3C Time Ontology in OWL (OWL-Time), Recommendation 2017 | temporal entity, instant, interval, beginning, end, duration, temporal reference system |
| `research` | Research and experimental development; the scholarly record | 001.4 Research | Frascati Manual 2015 for research, investigation, and method; SOSA/SSN for Observation and Sample; VIM for measuring instrument; SEPIO for assertion, Data Item, Evidence Line, support, and refute; Micropublications for Claim, Evidence, support, and challenge | observation, sample, claim, evidence, support, challenge, method, investigation |

Why these names and not "algebra", "time" and "science": algebra names operations on quantities, not quantities with units and uncertainty, which is what was missing and what VIM defines; "time" is fine as a word but 529 names the area; "science" is the whole of DDC 500 and would claim far more than a claims-and-evidence vocabulary. If a later reader finds a better-grounded name, the DDC number and the seminal source stay and the file name changes.

## Pack sketches

These are shapes for discussion, not schemas. Slot names follow the borrowed vocabulary.

### metrology

- Mixin `Quantified`: `quantity_kind` (string, open), `value_lower` (float), `value_upper` (float, equal to lower for an exact value), `unit` (string, UCUM code where one exists), `uncertainty` (float, optional), `determination` (enum `Determination`: MEASURED, DERIVED, ESTIMATED, MODELLED).
- Mixin `Counted`: `count` (integer), `count_scope` (string).
- Class `Ratio` (Entity): `numerator_kind`, `denominator_kind`, `value`, `uncertainty`.
- Class `QuantityValue` (Entity, wears `Quantified`) for projects that want quantities as nodes.

### chronology

- Mixin `TemporalExtent`: `begins_at` (datetime, optional), `ends_at` (datetime, optional), `precision` (enum mirroring Assent `ValidTimePrecision`), `order_key` (string, for order-only time with no calendar position).
- Class `Instant` and `Interval` (Entity) for projects that need time as nodes, following OWL-Time's two subclasses of temporal entity.
- Mirrors Assent's `ValidTime` rather than importing it. Assent is protocol; this pack is domain. The two must never be conflated.

### research

- Enum `AssertionModality`, shared across every project that loads the pack: STATED, MEASURED, CALCULATED, HYPOTHESISED, CONTESTED, NEGATED. One coarse list so that "which records here are hypotheses" means the same thing in every graph. A project that needs finer distinctions adds a refinement slot beside it and never redefines a coarse value. The three producers' private enums (`ObservationBasis`, `DeterminationMode`, `LocationQuality`) are the evidence that this list must be shared.
- Mixin `SourceAsserted`: `assertion_modality` (enum above), `assertion_confidence` (float, optional). Any entity or relation can wear it, so "melt degassing triggers earthquakes" can enter a graph as HYPOTHESISED instead of being left out.
- Class `Claim` (Entity, wears `SourceAsserted`): `statement` (root slot), `claim_kind`. Seeded from Recon's `Claim`; the reviewer-workflow slots stay in Recon.
- Class `Observation` (Entity, wears `Quantified`, `TemporalExtent`, `SourceAsserted`).
- Classes `Method`, `Instrument`, `Campaign` (wears `TemporalExtent`, `Counted` for instrument counts), `Sample`, `Source` (a work or document), `Evidence` (root `locator`, source digest).
- Relations: CLAIM_CONCERNS (Claim to any entity), OBSERVED_WITH (Observation to Instrument or Method), PART_OF_CAMPAIGN, SAMPLED_FROM, SUPPORTS and CHALLENGES (Evidence or Claim to Claim, after Micropublications), REPORTED_BY (any record to Source).

Two layers of epistemics, kept apart on purpose: `assertion_modality` is what the source says and how strongly, and it lives in the domain graph where a query can read it. Assent's `EpistemicDecision` is whether we accept the record of what the source said, and it lives in the ledger. Neither leaks into the other.

## Grounding is a standing order, not a habit of this document

The naming table above is the first instance of a rule the skill must carry, so that no session invents a close-to-root vocabulary when one already exists in an established body of knowledge. The rule, for the skill's standing orders:

> Before you propose a concept that could belong to a pack, ground it. Name the area of knowledge it comes from in an existing taxonomy (the Dewey Decimal Classification number, or the field in the outline of academic disciplines), name the seminal vocabulary in that area, borrow its terms and their definitions, and record the citation. Invent a term only when the grounding search finds none, and say so in the record.

The record is machine-readable so the inquisitor can check it. A pack, and any project class that extends root directly rather than a pack, carries a `grounding` block:

```yaml
annotations:
  grounding:
    area: "Physical measurement"
    taxonomy: "DDC 530.8"
    vocabulary: "JCGM 200:2012 (VIM), 3rd edition"
    vocabulary_url: "https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf"
    borrowed_terms: [quantity value, measurement unit, measurement uncertainty]
    invented_terms: []
```

A new rite, `pack-grounding`, refuses a pack without a grounding block, a grounding block without a taxonomy locator and a vocabulary citation, and a class that extends root directly without either a grounding block or a `grounding: none-found` declaration. The rite checks presence and shape; it cannot judge whether the grounding is apt, and it must not pretend to.

The separate `pack-conformance` rite checks a copied pack against one exact reference pack. The copy may change documentation, add declarations, and add enum values. It may not remove a reference class, slot, or enum; change an existing declaration list; weaken inherited structure; change an existing scalar constraint; or add a new scalar or mapping constraint to an existing declaration. An extension that changes an existing class instead becomes a new subclass. The receipt binds both byte identities. This is a minimum structural substitutability check, not proof that two vocabularies mean the same thing.

Why this is a rule and not advice: the three producers did not lack skill, they lacked a reflex. Each built a competent private vocabulary in minutes. The reflex the skill installs is to look first, borrow second, invent last, and leave a trail either way.

## Domain-history profiles

Decided 2026-09-03, after the Core and paper threads independently reached the same object. Packs give a project its nouns. They do not say what a change means. That is a second, adopter-owned contract, and it is the "which semantic ledger" decision Luis makes in domain projects (REA in a personal-finance project). Core's proposed `CompleteProjectionClosure` (`design/SEMANTIC_LOG_KNOWLEDGE_PROJECTION.md`) answers a different question, how one exact history became one exact graph, and the two must not merge.

A `DomainHistoryProfile` freezes, and only freezes: the semantic unit of a change (assertion, occurrence, state version, commitment, or a declared composition); origin semantics (empty start, snapshot, partial import, historical reconstruction) and the genesis boundary and completeness scope; which time is which (domain time, assertion time, transaction time); what addition, correction, retraction and real-world transition mean; which ontology types play Entity, Event, Claim and State roles; the projection rule family. One physical ledger remains; the profile adds meaning, not a second authority. The change set's evidence closure binds a profile id; projection closure references it.

Malleus ships profiles the way it ships packs: grounded, optional, replaceable.

| Profile | Semantic unit | Grounding |
| --- | --- | --- |
| `source-assertion` | a dated, attributed claim from an identified source; correction and retraction are superseding claims | Micropublications (Clark, Ciccarese, Goble 2014); SEPIO; nanopublications |
| `state-version` | a versioned state record; later versions supersede earlier ones | what Small Shop implements today; temporal database versioning |
| `object-event` | immutable domain events with qualified event-to-object relations; state is derived | OCEL 2.0 |
| `commitment-exchange` | economic resources, events, agents, commitments | REA (McCarthy 1982). Documented, not shipped until a second consumer exists |

Consequences already visible: the paper's document experiment is `source-assertion`, under which assertions are capture evidence retained in the ledger and linked field by field to the records they produced (ruling of 2026-09-03 late, `handover/2026-09-03-core-population-v2.md`; Claim entities from the `research` pack are a later, pack-level option, not the base), record-level supersession already exists in the governed path, and no Event materialization is needed. Small Shop is `state-version` and now says so. `object-event` needs Event materialization and event-to-object correlation in the governed path, which is Core's own track and not on the paper's critical path.

## Typed gaps

The population producer gets a third output beside records and total refusal: a list of gap declarations. Each names a source block, a question id or none, a kind, and one sentence.

Gap kinds: INTERVAL_NOT_EXPRESSIBLE, AGGREGATE_ONLY, MODALITY_NOT_EXPRESSIBLE, REQUIRED_FIELD_ABSENT_IN_SOURCE, TYPE_ABSENT, RELATION_ABSENT.

A gap becomes a ledger event of DEFER shape, bound to the population proposal. Gaps are the only input the revision round may consume from the population stage. This is the skill's standing order 7 made mechanical: "log what the schema cannot express and grow the schema where those cluster."

## The revision round

- Input: the accepted ontology, the typed gaps, the reading. Never the competency questions. Never the query binding.
- Output: an add-only ontology supersession, compiled, recorded as a schema change with a migration receipt, followed by a population change set that supersedes the first, and replay across both ontology versions.
- Change kinds in the revision record: ADD_SLOT, ADD_ENUM_VALUE, ADD_CLASS, ADD_IMPORT. Policy admits the first three now. ADD_IMPORT exists in the grammar and is refused by policy, so opening it later changes one policy line and not the receipt format. Whether Core's adoption and migration receipt already express an added import is to be verified in the code before that line moves.
- Termination is typed: a fixed maximum number of rounds, two to start. "Nothing self-corrects" means no round may be justified by how the last one felt.

## Who owns what

- **The skill owns modelling and the protocol.** Two entry playbooks: nascent project (no schema yet: choose packs, propose the project schema, run the rites, populate with locators, declare gaps, extend, repeat) and ongoing project (the current standing orders). The skill names the packs and the rule: reach for a pack before inventing, extend a pack concept before extending root. The skill is identical for every user and every model; it is the product surface, not priming.
- **The library owns the interface.** Proposing, populating with gaps, admitting and replaying become a public command or API with typed refusals. A session never hand-writes an envelope from a spec. Today this path is research-local code; making it public is the Core work item that gates every rerun.
- **The experimenter owns isolation only.** The spawn message states that the skill is loaded, where the reading is, that the graph of what the document reports is to be built under the protocol, and to stop when nothing remains that can be added without invention. Read nothing else. Competency questions never enter. Queries are bound by the evaluator after the session stops.
- **The loop is one session by default.** Propose, populate, hit refusals and gaps, extend, repopulate, all in one session joined to the evaluator only through the ledger. Separate stage sessions, joined only by typed ledger events, remain the strict variant and the strongest statement of the thesis, because then the ledger is demonstrably the only thing the sessions share.

## Decisions taken

1. Add a pack rung between root and project; three generic packs, no domain packs from Malleus.
2. Names: `metrology`, `chronology`, `research`, grounded as tabled above.
3. Packs follow root style: mixins plus reference classes plus enums.
4. One shared `AssertionModality` in `research`, with optional per-project refinement slots.
5. Typed gaps as a third population output; gaps are DEFER-shaped ledger events.
6. Revision round is slots, enum values and classes first; imports reserved in the grammar, refused by policy.
7. The skill owns modelling, the library owns the interface, the experimenter owns isolation only; briefs are retired.
8. Never prime a session with the questions.
9. Grounding is a standing order in the skill and a machine-checkable `grounding` block on packs and root-extending classes, enforced by a `pack-grounding` rite. An adopter claiming that an edited copy preserves a shipped pack runs `pack-conformance` against the exact reference bytes.
10. A `DomainHistoryProfile` is a separate adopter-owned contract, shipped as grounded reference profiles; the paper runs under `source-assertion`, Small Shop under `state-version`; Event materialization is Core's `object-event` track and does not gate the paper.
11. Requirements flow: Core touches Core and receives requirements with reproducers; the paper thread executes and files requirements through the overseer; the overseer verifies every Core deliverable on disk before the paper thread consumes it. Handovers: `handover/2026-09-03-core-requirements.md`, `handover/2026-09-03-paper-executor-plan.md`.
12. Population (after the coverage RCA and Core's evaluation, `handover/2026-09-03-core-population-v2.md`, which supersedes the adapter handover): Core owns a neutral population plan (compiled contract identity, profile artifact, adapter identity, sources, records in the public record shape, supersessions, field-level derivations, typed gaps, valid time) and its deterministic lowering to the existing change-set grammar; a capture with zero records is the typed result NO_DOMAIN_CHANGE. The assertion, a verbatim clause with block, modality and attribution, is the unit of capture inside the optional document-assertion adapter, retained as evidence, never a graph record; the objective is coverage of the reading measured by a two-axis census (blocks reviewed or untouched; assertions fully, partly or unformalized), never "smallest"; competency questions enter only the evaluation loop after population is frozen; the admissible set is every concrete Entity and Relation type of the compiled contract; ratification samples blocks. Built by Core, test first, in the order P1 to P4 of that handover.

## Open

- Deeper pack compatibility beyond the shipped structural-substitutability check remains open. The current rite does not prove definition equivalence, behavioral compatibility, or intellectual aptitude.
- Whether the private admission path should accept root `Event` and `Signal` operations. Deferred until packs and the loop show demand.
- Whether `research` owns the reading locator structure or the OCR domain ontology does. Current lean: the root `locator` slot is the only coupling; `research.Evidence` carries a locator string and a source digest; OCR keeps ownership of reading structure.
- Relation-level modality reaches only relations, not relations about relations. A hypothesis about a causal chain needs the chain reified as entities, which the packs allow but do not force.

## Sources

- JCGM 200:2012, International vocabulary of metrology, basic and general concepts and associated terms (VIM), 3rd edition. https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf
- QUDT, Quantities, Units, Dimensions and Types. https://www.qudt.org/pages/QUDToverviewPage.html
- W3C, Time Ontology in OWL, Recommendation 2017. https://www.w3.org/TR/owl-time/
- OCLC, Dewey Decimal Classification summaries (001 Knowledge, 529 Chronology, 530.8 Physical measurement). https://www.oclc.org/content/dam/oclc/dewey/resources/summaries/deweysummaries.pdf
- OECD, Frascati Manual 2015, Guidelines for Collecting and Reporting Data on Research and Experimental Development, including the Fields of Research and Development classification. https://www.oecd.org/en/publications/frascati-manual-2015_9789264239012-en.html
- Brush, Shefchek, Haendel, SEPIO: A Semantic Model for the Integration and Analysis of Scientific Evidence, ICBO 2016. https://ceur-ws.org/Vol-1747/IT605_ICBO2016.pdf
- Clark, Ciccarese, Goble, Micropublications: a semantic model for claims, evidence, arguments and annotations in biomedical communications, Journal of Biomedical Semantics 5:28, 2014. https://link.springer.com/article/10.1186/2041-1480-5-28
- Wikipedia, Outline of academic disciplines. https://en.wikipedia.org/wiki/Outline_of_academic_disciplines
