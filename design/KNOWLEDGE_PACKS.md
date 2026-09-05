# Knowledge packs, typed gaps, and the revision loop

Status: design decided in conversation on 2026-09-03 between Luis and the overseer session, after the three-producer paper runs. The population path, additive revision, domain-history profiles, three optional packs, structural grounding rite, and minimum edited-pack conformance rite are implemented. Decisions 13 and 14, taken on 2026-09-04 after run-02, ship in `metrology` and `research` at version 0.2.0; both are additive. Decisions 15 and 16, taken on 2026-09-05 after run-04 and run-05, ship in the same two packs at version 0.3.0; both are additive. Decision 17, taken on 2026-09-05 after run-04's review RCA, ships in `research` at version 0.4.0 and is additive. Decision 18, taken on 2026-09-05 after the v4.2 RCA of run-04 against run-08, ships in `research` at version 0.5.0 and is additive. Sections marked "open" remain undecided.

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
| `metrology` | The science of measurement; formal and physical sciences in the outline of disciplines | 530.8 Physical measurement | JCGM 200:2012, the International Vocabulary of Metrology (VIM), 3rd edition; QUDT as the ontology precedent | quantity value, measurement unit, measurement uncertainty, kind of quantity |
| `chronology` | Time and its reckoning | 529 Chronology | W3C Time Ontology in OWL (OWL-Time), Recommendation 2017 | temporal entity, instant, interval, beginning, end, duration, temporal reference system |
| `research` | Research and experimental development; the scholarly record | 001.4 Research | Frascati Manual 2015 for research, investigation, and method; SOSA/SSN for Observation and Sample; VIM for measuring instrument; SEPIO for assertion, Data Item, Evidence Line, support, and refute; Micropublications for Claim, Evidence, support, and challenge | observation, sample, claim, evidence, support, challenge, method, investigation |

Why these names and not "algebra", "time" and "science": algebra names operations on quantities, not quantities with units and uncertainty, which is what was missing and what VIM defines; "time" is fine as a word but 529 names the area; "science" is the whole of DDC 500 and would claim far more than a claims-and-evidence vocabulary. If a later reader finds a better-grounded name, the DDC number and the seminal source stay and the file name changes.

## Pack sketches

These are shapes for discussion, not schemas. Slot names follow the borrowed vocabulary.

### metrology

- Mixin `Quantified`: `quantity_kind` (string, open, the source's own wording), `quantity_kind_class` (enum `QuantityKindClass`, optional, fifteen QUDT names plus OTHER), `value_lower` (float), `value_upper` (float, equal to lower for an exact value), `value_qualification` (enum `ValueQualification`, optional, how the source states the number: EXACT, APPROXIMATE, OPEN_LOWER_BOUND, OPEN_UPPER_BOUND, ORDER_OF_MAGNITUDE), `unit` (string, UCUM code where one exists), `uncertainty` (float, optional), `determination` (enum `Determination`: MEASURED, DERIVED, ESTIMATED, MODELLED).
- Mixin `Counted`: `count` (integer), `count_scope` (string).
- Class `Ratio` (Entity): `numerator_kind`, `denominator_kind`, `value`, `uncertainty`.
- Class `QuantityValue` (Entity, wears `Quantified`) for projects that want quantities as nodes.

### chronology

- Mixin `TemporalExtent`: `begins_at` (datetime, optional), `ends_at` (datetime, optional), `precision` (enum mirroring Assent `ValidTimePrecision`), `order_key` (string, for order-only time with no calendar position).
- Class `Instant` and `Interval` (Entity) for projects that need time as nodes, following OWL-Time's two subclasses of temporal entity.
- Mirrors Assent's `ValidTime` rather than importing it. Assent is protocol; this pack is domain. The two must never be conflated.

### research

- Enum `AssertionModality`, shared across every project that loads the pack: STATED, MEASURED, CALCULATED, HYPOTHESISED, CONTESTED, NEGATED. One coarse list so that "which records here are hypotheses" means the same thing in every graph. A project that needs finer distinctions adds a refinement slot beside it and never redefines a coarse value. The three producers' private enums (`ObservationBasis`, `DeterminationMode`, `LocationQuality`) are the evidence that this list must be shared.
- Mixin `Evaluative`: `hypothesis_disposition` (enum `HypothesisDisposition`, optional, what the source does with a hypothesis it raised: PREFERRED, NOT_SUPPORTED, UNDECIDED). Worn by `Claim`. The mixin's slot list is the pack's declaration of which slots are evaluative, read from the compiled contract.
- Mixin `SourceAsserted`: `assertion_modality` (enum above), `assertion_confidence` (float, optional), `subject` (Entity reference, single, optional, the thing the assertion is about), `assertion_locator` (string, optional, an opaque route back to the retained assertion), `statement_sha256` (string, optional, the digest of the exact retained assertion text). Any entity or relation can wear it, so "melt degassing triggers earthquakes" can enter a graph as HYPOTHESISED instead of being left out.
- Class `Claim` (Entity, wears `SourceAsserted`): `statement` (root slot, optional and empty unless the record's `Source` declares a permitting licence), `claim_kind`. Seeded from Recon's `Claim`; the reviewer-workflow slots stay in Recon.
- Class `Observation` (Entity, wears `Quantified`, `TemporalExtent`, `SourceAsserted`).
- Classes `Method`, `Instrument`, `Campaign` (wears `TemporalExtent`, `Counted` for instrument counts), `Sample`, `Source` (a work or document, `licence` as the source declares it), `Evidence` (root `locator`, source digest).
- Mixin `Contribution`: `contribution_role` (enum `ContributorRole`, optional, the fourteen CRediT roles plus OTHER). Class `ContributionRelation` (`ResearchRelation`, wears `Contribution`) carries a credited contribution; one relation per role.
- Relations: CLAIM_CONCERNS (Claim to any entity), OBSERVED_WITH (Observation to Instrument or Method), PART_OF_CAMPAIGN, SAMPLED_FROM, SUPPORTS and CHALLENGES (Evidence or Claim to Claim, after Micropublications), REPORTED_BY (any record to Source), CONTRIBUTED_TO (a contributor to a work, campaign, or dataset).

Two layers of epistemics, kept apart on purpose: `assertion_modality` is what the source says and how strongly, and it lives in the domain graph where a query can read it. Assent's `EpistemicDecision` is whether we accept the record of what the source said, and it lives in the ledger. Neither leaks into the other.

## Grounding is a standing order, not a habit of this document

The naming table above is the first instance of a rule the skill must carry, so that no session invents a close-to-root vocabulary when one already exists in an established body of knowledge. The rule, for the skill's standing orders:

> Before you propose a concept that could belong to a pack, ground it. Name the area of knowledge it comes from in an existing taxonomy (the Dewey Decimal Classification number, or the field in the outline of academic disciplines), name the seminal vocabulary in that area, borrow its terms and their definitions, and record the citation. Invent a term only when the grounding search finds none, and say so in the record.

The record is machine-readable so the inquisitor can check it. A pack, and any project class that extends root directly rather than a pack, carries a `grounding` block:

```yaml
annotations:
  grounding:
    tag: grounding
    value:
      area: "Physical measurement"
      taxonomy: "DDC 530.8"
      vocabularies:
        - vocabulary: "JCGM 200:2012 (VIM), 3rd edition"
          vocabulary_url: "https://www.bipm.org/documents/20126/2071204/JCGM_200_2012.pdf"
          borrowed_terms:
            - quantity value
            - measurement unit
            - measurement uncertainty
            - kind of quantity
      invented_terms: []
```

A new rite, `pack-grounding`, refuses a pack without a grounding block, a grounding block without a taxonomy locator and a vocabulary citation, and a class that extends root directly without either a grounding block or a `grounding: none-found` declaration. The rite checks presence and shape; it cannot judge whether the grounding is apt, and it must not pretend to.

For project classes, direct-root detection covers both bare root names and CURIEs whose declared prefix resolves to the exact Malleus root namespace. An arbitrary prefix ending in `Entity` is not treated as Malleus. Full URI class references remain outside the current compiler profile. A grounding annotation is retained source evidence; it is not an adoption marker and does not enter semantic fact identity.

The separate `pack-conformance` rite checks a copied pack against one exact reference pack. The copy may change documentation, add declarations, and add enum values. Reference imports must remain unique and set-equivalent, although their order may change. The copy may not remove a reference class, slot, or enum; change an existing declaration list; weaken inherited structure; change an existing scalar constraint; or add a new scalar or mapping constraint to an existing declaration. An extension that changes an existing class instead becomes a new subclass. The receipt binds both byte identities. This is a minimum structural substitutability check, not proof that two vocabularies mean the same thing.

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

Consequences already visible: the paper's document experiment is `source-assertion`, under which assertions are capture evidence retained in the ledger and linked field by field to the records they produced (ruling of 2026-09-03 late, `handover/2026-09-03-core-population-v2.md`; Claim entities from the `research` pack are a later, pack-level option, not the base), record-level supersession already exists in the governed path, and no Event materialization is needed. Small Shop uses `state-version` for mutable supplier-order state and a separate `object-event` conformance history for packing occurrence `e27`. The latter admits an Event and qualified Event-to-Entity participation records without widening ordinary Relation endpoints. Event-to-Event ordering remains open.

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
10. A `DomainHistoryProfile` is a separate adopter-owned contract, shipped as grounded reference profiles; the paper runs under `source-assertion`; Small Shop runs `state-version` and a separate `object-event` conformance history. Object-event materialization does not gate the paper.
11. Requirements flow: Core touches Core and receives requirements with reproducers; the paper thread executes and files requirements through the overseer; the overseer verifies every Core deliverable on disk before the paper thread consumes it. Handovers: `handover/2026-09-03-core-requirements.md`, `handover/2026-09-03-paper-executor-plan.md`.
12. Population (after the coverage RCA and Core's evaluation, `handover/2026-09-03-core-population-v2.md`, which supersedes the adapter handover): Core owns a neutral population plan (compiled contract identity, profile artifact, adapter identity, sources, records in the public record shape, supersessions, field-level derivations, typed gaps, valid time) and its deterministic lowering to the existing change-set grammar; a capture with zero records is the typed result NO_DOMAIN_CHANGE. The assertion, a verbatim clause with block, modality and attribution, is the unit of capture inside the optional document-assertion adapter, retained as evidence, never a graph record; the objective is coverage of the reading measured by a two-axis census (blocks reviewed or untouched; assertions fully, partly or unformalized), never "smallest"; competency questions enter only the evaluation loop after population is frozen; every concrete Entity and Relation type is admissible, and a selected profile with an Event role also admits concrete Event types plus EventParticipation types present in the compiled contract; ratification samples blocks. Built by Core, test first, in the order P1 to P4 of that handover.

13. A controlled quantity-kind classification in `metrology`, additive. A fresh
    producer given the packs used the open `quantity_kind` for 137 observations and
    produced 137 distinct strings. Free text alone is readable and not comparable:
    nothing groups two records reporting one kind under different wording, and a
    type-only query binding has no field to sharpen on. The producer refused to coin
    its own enum, correctly, because the skill says reuse before invent, and a private
    list would have made that graph incomparable with the next one. So the pack ships
    the list: enum `QuantityKindClass`, fifteen names taken from the QUDT
    quantity-kind vocabulary at http://qudt.org/vocab/quantitykind/ and spelled as
    QUDT spells them, Length, Time, Temperature, Pressure, Mass, Volume, Area,
    Velocity, Density, Frequency, Energy, Force, MassFraction, Count and Angle, plus a
    local `OTHER` for a quantity none of them fits. QUDT because the naming table
    above already cites it as the ontology precedent for `metrology`, its names are
    minted under a stable namespace, and VIM defines the concept while enumerating no
    kinds. The optional slot `quantity_kind_class` sits beside `quantity_kind` in the
    `Quantified` mixin. `quantity_kind` stays, stays open, and keeps the source's own
    wording, which is never rewritten to fit the class; unset is the honest value when
    the source's kind is unclear. The change is additive, so the pack is version 0.2.0
    and the list grows by adding values rather than by redefining one.
14. Claim text policy: the graph carries a locator and a digest, not the sentence. The
    same producer wrote verbatim source sentences into `Claim.statement` and into root
    `description`, which the accepted ontology permits and which a source-support
    review wants to read. It also put copyrighted prose into the population plan, the
    gaps, the replay receipt, the export records, the query result, the retained
    capture and the ledger, and seven artifacts of that run are withheld with only
    their digests public. The graph now carries `assertion_locator`, the route back to
    the retained assertion, and `statement_sha256`, the digest of the exact retained
    assertion text. Both sit on the `SourceAsserted` mixin, so they reach every
    claim-bearing record and not only `Claim`: `Observation` wears the mixin, and a
    project class that inherits `Claim` gets them without declaring anything.
    `statement` stays and stays optional, and it carries a sentence only where the
    record's `Source` declares a licence that permits reproduction; `Source` gains a
    `licence` slot for that declaration. The locator is opaque and source-agnostic on
    purpose: the pack does not parse it and does not assume a document, because a
    source can be a PDF text layer, a malleus-ocr bundle, a recon record, or a time
    span in a wav file. Retention does not change. The assertion stays where it
    already was, in the retained capture, and the locator is what reaches it.
15. How the source states its number, in `metrology`, additive. A bound pair says
    a value lies between two numbers and says nothing else. 25 of run-04's 61 typed
    gaps are INTERVAL_NOT_EXPRESSIBLE carrying one sentence, that the source marks
    the value as approximate and the records carry the stated number as an exact
    bound pair and cannot carry the approximation. Run-05 declared a gap for a mantle
    temperature the source states only as above 1100 degrees Celsius, because
    `value_lower` and `value_upper` are a closed pair, and a reviewer in the same run
    marked a hedged value PARTIAL for the same reason. Both producers were right to
    declare a gap rather than invent an interval, and both losses are of one fact:
    how the source stated the number. So the pack ships an optional enum,
    `ValueQualification`, whose slot `value_qualification` sits in the `Quantified`
    mixin beside `value_upper`, with five forms, EXACT, APPROXIMATE,
    OPEN_LOWER_BOUND, OPEN_UPPER_BOUND and ORDER_OF_MAGNITUDE. An open bound leaves
    its absent end unset, which the shape already permits and which the qualification
    now explains. The grounding search came back empty. QUDT carries
    standardUncertainty and relativeStandardUncertainty, which quantify a
    measurement's dispersion rather than a source's hedge, and minInclusive and
    maxInclusive, which constrain a datatype rather than describe a stated bound.
    VIM 4.6 defines nominal quantity value as a rounded or approximate value
    characterizing a measuring instrument, not a reported measurement. UCUM codes
    units and discards annotations by definition. ISO 80000-2 supplies the relation
    sign read as is approximately equal to, a mathematical symbol. There is no term
    for how a source qualifies a stated number in any of them, so the enum and its
    five values are local and the pack records that in `invention_search`, the way
    `research` records Campaign and Instrument. What it does not do: it never
    changes the number, the unit or the bounds, it turns no approximation into an
    invented interval and no interval into a point, it makes no claim about the
    value's accuracy, and it does not replace `uncertainty`, which stays for an
    uncertainty the source reports. There is no OTHER: `Determination` has none
    either, unset is the honest value when the form is unclear, and a form the five
    do not cover is a gap to declare, which is how the list grows. The change is
    additive, so the pack is version 0.3.0 and the list grows by adding values
    rather than by redefining one.
16. Contribution roles in `research`, from CRediT, additive. Run-04 declared two
    TYPE_ABSENT gaps saying the source states a specific contribution for each
    author and the accepted ontology carries no contribution-role vocabulary, so
    only the fact of contribution was formalized and the part each person played
    was not. That run's own project ontology had coined a three-value contributor
    role for byline position, author, corresponding author, acknowledged, which
    answers a different question and cannot carry what a person did. The published
    answer exists: the CRediT Contributor Roles Taxonomy, ANSI/NISO Z39.104-2022,
    fourteen roles each with its own definition, at https://credit.niso.org/. The
    pack ships enum `ContributorRole` with those fourteen roles in the pack's enum
    spelling, each carrying the taxonomy's own definition as its description, plus a
    local OTHER for a contribution the taxonomy does not name. No role is coined,
    and the fourteen published names are the borrowed terms in the pack's grounding.
    The role hangs on the contribution and not on the person, because one person is
    credited differently on different works: the optional slot `contribution_role`
    sits on a new `Contribution` mixin, worn by a new `ContributionRelation`, a
    `ResearchRelation` whose `relation_type` is the new `CONTRIBUTED_TO`. A
    contributor credited under several roles carries one relation per role. CRediT
    is a term list with no classes, so `Contribution` and `ContributionRelation`
    are local shapes and the pack's `invention_search` says so. What it does not
    do: it does not model authorship order, corresponding authorship, affiliation
    or degree of contribution, none of which CRediT defines either; it does not
    require a role, so a source that names a contributor without stating the part
    they played is recorded without inventing one; and it makes no claim that the
    role the source states is true. The change is additive, so the pack is version
    0.3.0.
17. Evaluative slots in `research`, additive. The derivation rule binds every
    field to a formalizing assertion and the adapter checks that the target
    exists, never that the formalizing sentence has anything to do with the
    value. In run-04's capture all five of run-04's dispositions derive from
    HYPOTHESISED assertions: `claim:mechanism-magmatic-tectonic` carries
    `hypothesis_disposition: NOT_SUPPORTED` and all six of its fields, the
    disposition included, derive from `c:072`, the sentence introducing the
    possibility, while the rejection sits in the next prose block and no
    assertion there formalizes anything. The reviewer confirmed each value on
    the reading, so this is mis-derivation and not invention, and the rule
    could not see it. A disposition is an evaluative value: the assertion that
    formalizes it must be one that evaluates. So the pack ships the slot and
    the vocabulary, optional enum `HypothesisDisposition` with `PREFERRED`,
    `NOT_SUPPORTED` and `UNDECIDED` on slot `hypothesis_disposition`, and it
    ships the declaration of which slots are evaluative as a new mixin,
    `Evaluative`, worn by `Claim`, where the mixin's slot list is the
    declaration: the compiled contract already exposes a class's effective
    slots, so the
    document-assertion adapter reads `Evaluative`'s slot list from the
    contract it is handed and needs no new compiler surface, no annotation
    grammar and no argument the caller invents. A record carrying an
    evaluative slot must be formalized by at least one assertion whose
    modality is not `HYPOTHESISED`; otherwise the adapter refuses,
    aggregated, naming the record, the slot and the formalizing assertions
    with their modalities. The grounding search came back empty: SEPIO models
    an assertion's evidence lines and their support or refutation and
    Micropublications models one statement supporting or challenging another,
    both relations between two things rather than a source's disposition of
    its own hypothesis, so the enum and the mixin are local and
    `invention_search` says so. What it does not do: it adds no modality, the
    six of `AssertionModality` are unchanged; it does not decide whether the
    disposition is correct, only which sentence may carry it; and it says
    nothing about a slot no pack declares evaluative. The change is additive,
    so the pack is version 0.4.0 and the list of evaluative slots grows by
    adding a slot to the mixin.

18. The subject of a source-asserted record, in `research`, additive. Run-04
    linked its observations and claims to what they were about 27 times, 13
    `CONCERNS_FEATURE`, 3 `LIES_BENEATH` and 11 `LOCATED_WITHIN`, and answered
    240 query rows. Run-08, the same model on the same reading under the same
    eight-input isolation, made no science relation at all and answered 8. The
    attachment did not disappear, it moved into free text: 23 of run-08's 131
    observations carry the feature inside `quantity_kind`, against 2 of
    run-04's 71. One sentence on page 2 carries the whole case. Run-04 made
    three `EarthquakeSet` entities and three LOCAL `LIES_BENEATH` relations
    from it; run-08 made three depth observations whose `quantity_kind` reads
    "depth of deep microseismicity beneath the ridge axis of the segment RC2",
    and no entity and no relation. The value, the hedge, the units and the
    provenance are right in both. Only the attachment is structure in one and
    a substring in the other, and only structure is queryable. The v4.2
    changes did not cause the loss; they removed the hub derivation that had
    hidden the absence of a rule, and 94 of run-04's 240 query rows rested on
    relations whose formalizing sentence names neither endpoint, so 146 rows
    and not 240 are the honest baseline the 8 must be measured against. Nor
    was the producer at fault: its ontology had no entity type for an
    earthquake population, its `GeospatialRelation` is defined as a predicate
    between two named Earth features, an observation is not a named Earth
    feature, and the pack itself offered no slot for "this record is about
    that thing". So the pack ships the attachment as a first-class derived
    element rather than as a producer instruction: optional, single-valued
    `subject` on the `SourceAsserted` mixin, so an observation, a count
    observation, an asserted ratio and a claim all carry it without declaring
    anything. Its range is `Entity`, the same declaration a relation's
    endpoints already carry, and its value is a record id resolvable in the
    same change set or the base state, never the record itself and never an
    Event: relation endpoints stay Entity-to-Entity and so does this. The
    grounding search found SOSA/SSN's feature of interest, which names the
    thing an observation's property belongs to and fits neither a claim nor a
    ratio, and RDF 1.1 Concepts' subject, the position of a statement that
    names what the statement is about, for every statement rather than for a
    measurement. The pack borrows the RDF term and records the narrower one it
    passed over. The document-assertion adapter checks it, aggregated with the
    other derivation defects and typed `SUBJECT_NOT_NAMED`: when a record sets
    `subject`, the subject entity's `name`, whitespace-collapsed and
    case-folded, must occur in the statement of at least one assertion that
    formalizes that record's `["properties", "subject"]` path. The check is a
    name substring and not a semantic judgment on purpose. A substring is
    recomputable by a second implementation from the retained bytes alone, it
    needs no model at admission, and it fails closed on exactly the defect
    run-08 shows, a subject asserted from a sentence that does not mention it.
    Whether a sentence is about a thing in any richer sense is a judgment, and
    `COMMITTED` means the shape was valid. The cost is stated rather than
    hidden: a sentence naming the thing only by a pronoun, an abbreviation or
    a synonym refuses, and the honest answers are to formalize the subject
    from the sentence that does name it, or to leave `subject` unset. The
    census carries the coverage, under `subjects` beside `derivation`: per
    record type the compiled contract declares as carrying `subject`, the
    count with a subject, the count without, and the total, reported and never
    refused. What it does not do: it does not check that the subject is an
    Entity rather than an Event, exactly as nothing checks that today for a
    relation endpoint; the adapter reads the subject's name from the change
    set it is handed, so a subject that resolves only in the base state has
    its name unchecked and only its resolution checked, by the plan compiler's
    `DANGLING_SUBJECT`; it does not decide whether the subject is the right
    one, only that the formalizing sentence names it; it adds no relation and
    removes none, so a project modelling the attachment as a typed relation
    keeps doing so and may do both; and it never rewrites `quantity_kind`,
    which stays the source's own wording. With no compiled contract the
    adapter knows no subject-bearing type and the census axis is empty, while
    the refusal still runs, because `subject` is one fixed name and needs no
    declaration to be read. The change is additive, so the pack is version
    0.5.0 and every fixture and every frozen paper cell pinned at an earlier
    pack keeps compiling.

## Open

- Deeper pack compatibility beyond the shipped structural-substitutability check remains open. The current rite does not prove definition equivalence, behavioral compatibility, or intellectual aptitude.
- Signal population and Event-to-Event ordering remain deferred. The governed `object-event` path now admits Events and qualified Event-to-Entity participation records without treating them as ordinary Relations.
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
- NISO, ANSI/NISO Z39.104-2022, CRediT, Contributor Roles Taxonomy. https://credit.niso.org/
- ISO 80000-2:2019, Quantities and units, Part 2: Mathematics. https://www.iso.org/standard/64973.html
- Regenstrief Institute, The Unified Code for Units of Measure (UCUM). https://ucum.org/
- Wikipedia, Outline of academic disciplines. https://en.wikipedia.org/wiki/Outline_of_academic_disciplines
