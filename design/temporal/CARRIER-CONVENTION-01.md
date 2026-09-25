# Carrier convention 01: are uses records and relations structure?

24 September 2026. Research for one decision Luis has not ruled. Nothing here
is ruled. No `src/` change. Core is this branch, `codex/core-temporal` at
`4ffec259`.

The proposed rule, as the Overlord stated it: a relation edge is structure
within one interpretation. It follows the record it touches and blocks that
record's revision until restated. A use of an exact record version by another
interpretation, calculation or application is a record with a class-ranged
reference slot naming that version. It does not block revision, and the impact
read follows it backwards. In short: uses are records with typed references;
relations are structure.

Labels: [CODE] file and line read at `4ffec259`. [DOC] repository document,
path and section. [PROBE] command run, output quoted. [LIT] primary source,
URL and section. [REASONING] my inference, not run.

## Answer in brief

1. The distinction the rule draws is right, and the repository already asks
   for it. A link that must follow its target when the target is revised is a
   different thing from a link that must stay on the exact version it was
   written about. Three documents say so, and none ties the meaning to a
   carrier. [DOC, section A]
2. Tying the meaning to the carrier contradicts an accepted decision. OD-010
   (ACCEPTED 2026-08-27, `design/contract_compiler/decisions.md`) makes every
   non-inlined class-valued slot a strong reference that must resolve, and
   requires every selected temporal view to be referentially closed for slots,
   endpoints and bearers alike: "A view containing a referrer without its
   target refuses as structurally incomplete." The rule works today only
   because OD-010's slot half is not built. Building R-05's resolution gap as
   OD-010 wrote it would make slot uses block, or make the current view
   refuse, exactly as edges do. [DOC, CODE, PROBE Q3]
3. OD-010 predates R-02 (every version its own record). It never considered a
   reference to an exact version. That silence, not the carrier, is the real
   decision. [DOC, REASONING]
4. The repository's own consumers put uses on relations. The live Shop graph
   has a `CorrectsState` relation from a correction claim to the exact state
   version `B:Y:e7`. The computational-graph research records actual input use
   as `ActualInputUse` relations with qualifiers. The re-entry loop links its
   application record to the estimate by a relation. HISTORICAL-USE-01 section
   4 said the Shop had no Relation classes; it read `shop.yaml` only. The
   Shop's `context.yaml` declares six. [CODE, INSPECTED]
5. The implicit rebinding HISTORICAL-USE-01 found (P2b) does not depend on the
   carrier. A use record whose slot names the clause root is as blind to a
   revised leaf as the reuse edge is. [REASONING from `version_referrers`,
   CODE]
6. Recommendation: do not rule the carrier convention as the meaning. Rule the
   distinction as a declared reference kind, STRUCTURAL or VERSION, with the
   ontology as its eventual home, and amend OD-010 so a VERSION reference
   resolves against record history while a STRUCTURAL one stays closed in the
   current view. Until a declaration exists, state today's behaviour as the
   default: a relation is STRUCTURAL, a class-ranged slot is VERSION. Build
   the declaration only when a consumer needs the non-default kind. Section F
   has the costs and what stays open.

## A. What the repository already says

### What a relation is

- The root ontology declares `Relation` as "A typed, directed edge between two
  entities. Reified as a class so relations can carry metadata (strength,
  confidence, temporal validity)." [DOC `ontology/malleus.yaml` 192 to 209]
  `source_id` and `target_id` are ranged `Entity` (283 to 291).
- The ontology protocol names the pattern: "Relation | A typed directed edge
  between entities, reified for metadata | N-ary relation pattern". It asks
  for one concrete class per predicate, fixing `relation_type` with
  `equals_string` and narrowing both endpoints. [DOC `docs/ONTOLOGY_PROTOCOL.md`
  "What Malleus provides" and step 2]
- The five root primitives are the default typed-graph profile, "not universal
  data models or base protocol invariants." [DOC `docs/PRINCIPLES.md`,
  "Protocol boundary taxonomy"] So any carrier rule is at most an
  `OPTIONAL_PROFILE` rule of that profile, and of semantic-history where it
  touches revision.

So in Malleus a relation is already a statement node in the ontology's sense:
it has its own identity, type, properties and versions. It differs from an
entity in three ways only: its endpoints must be current entities, it cannot
itself be an endpoint, and the reference implementation stores it as an edge.
[DOC, CODE below]

### Whether relations carry properties

Yes, by the root ontology (above) and by code: `create_relation` validates the
properties against the relation class and stores them on the edge. [CODE
`kg.py` 570 to 606] Recon relations carry `review_state`, `assertion_status`,
`confidence`, `basis` and `evidence_ids`. [DOC `ontology/domains/recon.yaml`
`ReviewedRelation`, 134 to 153]

### Whether a relation can be an endpoint or be referred to

OD-010, ACCEPTED 2026-08-27, "Endpoints, bearers, identity, and views":

> Relation endpoints remain existing `Entity` records matching the declared
> endpoint class or subtype. ... Event, Signal, Relation, protocol, and
> governance records refuse as endpoints. Relation-as-endpoint still requires
> a different storage model because current relations are edges, not graph
> nodes; D10 does not select such a model.

The same decision's conformance trace allows a class-valued slot to name a
relation: `SealReviewEvent` "with a class-valued reference to that existing
Relation", then a signal borne by the relation. It "proves ... a generic
Event-to-Relation strong reference ... without widening relation endpoints."
[DOC `design/contract_compiler/decisions.md`, OD-010, "Concrete conformance
traces"]. The foundation graph marks
`EntityEventSignalRelationEndpointExpansionV0` as `mfg:Excluded`. [DOC
`design/PROTOCOL_FOUNDATION_GRAPH.md` around 1318]

So the repository already chose the property-graph answer to edge-of-edge: an
intermediate record that names the relation by a class-ranged slot.

### Whether class-ranged references must resolve

OD-010, same decision, first paragraph:

> Every non-inlined class-valued `SlotUse` is a strong graph reference. ... A
> present scalar value and every member of a present multivalue must resolve.
> The concrete target type must equal the declared class range or be its
> `subClassOf` descendant.

and, under views:

> Every selected temporal view must be referentially closed for every visible
> strong reference, relation endpoint, and signal bearer. A view containing a
> referrer without its target refuses as structurally incomplete. Admission
> does not cascade, repair, delete, infer reverse dependencies, propagate
> uncertainty, or prove interval containment.

Implementation belongs to `CC-R06`, not built. [DOC
`design/contract_compiler/program.md` 397, 490] This is the gap R-05 recorded
as "Core does not check that a reference resolves".

**Where the proposed rule contradicts the record.** OD-010 treats a slot
reference and a relation endpoint the same way. The proposed rule makes them
opposite. Under OD-010 as written, a current `Use` naming a retired version
`a1` is a visible referrer with an omitted target in the current view.
[REASONING from the quoted text]

**Where the record is silent.** OD-010 does not distinguish a reference to a
current thing from a reference to an exact version. It was written before R-02
made every version its own record. It speaks of "selected temporal views" and
not of a version graph. Whether a retired version is "visible" for a reference
that names it on purpose is not addressed. [DOC, REASONING]

### How provenance and use are to be modelled

- "Citation, attribution, application, derivation, support and independent
  corroboration are different relationships." And: "This is a representation
  obligation, not a proposed universal record type. Use a property, grouped
  object, relation or qualified proposition according to the distinctions
  required." [DOC `handover/2026-09-23-knowledge-maintenance-plan.md` section 2]
  The carrier is left to the adopter.
- The acolyte skill: "Citation, attribution, support and refinement are
  different relationships." It is silent on carrier and on what a link does
  when its target is revised. [DOC `.claude/skills/malleus-acolyte/SKILL.md`,
  "Maintaining interpretations as evidence accumulates"]
- "The dependency index needs typed edges because different edges propagate
  differently: STRUCTURAL_REFERENCE, PROVENANCE, EPISTEMIC_JUSTIFICATION,
  TEMPORAL_SUPERSESSION, CONTRACT_VALIDATION_FOOTPRINT ... Each dependency kind
  therefore declares its resolution, cycle, invalidation, and revalidation
  semantics." Status Candidate, package `ReferenceDependencySemantics`,
  informed by Doyle 1979. [DOC `design/PROTOCOL_FOUNDATION_GRAPH.md` 5.3, and
  around 1947, 2195] This is a declared-kind design, not a carrier rule.
- "A temporal edge also needs a declared meaning. A relationship describing
  two coexisting domain objects differs from a correction or provenance link
  between accounts. Imposing temporal overlap on every edge would break
  legitimate historical explanations." [DOC
  `design/temporal/REPRESENTATION-OPTIONS-01.md`, after the comparison table]
- Guardrail for claims work: engage "Wikidata ranks/supersession, SEPIO/VA-Spec,
  DISK, and RDF 1.2 reifiers" first; "Malleus claim design must answer 'why
  not RDF 1.2 reifiers': packaging of multi-record units, typing, and the
  write gate." PROV-O is "Reuse (map onto)". [DOC `docs/DELIMITATIONS.md`,
  "Semantic web standards" and "Guardrails for future design"]
- "Relation-level modality reaches only relations, not relations about
  relations. A hypothesis about a causal chain needs the chain reified as
  entities, which the packs allow but do not force." [DOC
  `design/KNOWLEDGE_PACKS.md`, "Open"]
- A history profile may admit qualified `EventParticipation` records, "not an
  ordinary Relation, so Relation endpoints remain Entity-to-Entity." [DOC
  `docs/KNOWLEDGE_GRAPH_PROTOCOL.md` 2A] This is a precedent for a qualified
  link as its own record family with its own endpoint rule.

### How executions bind their inputs

`research/computational_graphs` records planned use as `InputUseBinding` and
`ChargeUseBinding` and actual use as `ActualInputUse` and `ActualChargeUse`,
all relations from the execution or context to the assertion, with the
qualifiers `parameter_iri` and `binding_id` as relation properties.
`binding_id` names another relation by a string. [CODE
`research/computational_graphs/context_model.py` 59 to 81,
`model_records.py` 39 to 52, `contextual.py` 438 to 447] RESULTS-03 corrects a
price by a new assertion plus a `CorrectsReport` relation, never by
superseding a used assertion, so the use edges never had to move. [DOC
`research/computational_graphs/RESULTS-03.md`, "One concrete evidence chain"]
The PROV-O view it exports has "twelve qualified usages". [same, "Where the
three components fit"]

### What the Shop, the re-entry loop and UMR actually do

| Consumer | Use or link | Carrier | Kind by HISTORICAL-USE-01's table |
|---|---|---|---|
| Shop stage C (private) | `CorrectsState`: `OrderCorrectionClaim` to `SupplierOrderState` `B:Y:e7`, the corrected version | relation | 3: about one exact version |
| Shop stage C | `CustomerOrder`, `DelayOrder`, `DelayPayment`, `DelayInvoice`, `RuleCustomerScope`: claims to enduring `SalesOrder`, `Payment`, `Invoice` | relation | 2: about an enduring identity |
| Shop | `SupplierOrderState.order_id` to `SupplierOrder` | class-ranged slot | structure: version to its enduring identity |
| Re-entry loop | `EstimateApplication` (a `Claim` record) plus `ApplicationUsesEstimate` relation to the estimate; `ApplicabilityAssessment.subject` slot plus `AssessmentOfApplication` relation, the same link twice | record and relation | 3 and 2 |
| Computational graphs | `ActualInputUse`, `ActualChargeUse` with qualifiers | relation | 3 |
| UMR | `MarineCitation`, `MarineReuseHypothesis` (`CANDIDATE_REUSE`) | relation | 2 |
| UMR | `UmrSentence.sentence_root` | class-ranged slot | structure |
| UMR probe C1/C4 | `StatisticInterpretation.interprets`, `ResultApplication.applies_readings` | class-ranged slot | 3 |
| Recon | `Work.evidence_ids`; relations with review qualifiers | slot and relation | references by stable ID, latest version wins |

Sources: [CODE `private/shop-progressive-01/producer/workspace-stage-c/inputs/context.yaml`
classes `ContextRelation` to `CorrectsState`; `shop.yaml` 94 to 125;
`work/plan-order-correction.json`, one entity and one `CorrectsState`
relation; `work/stage-c-export.json`, relation census `CustomerOrder` 2,
`DelayInvoice` 2, `CorrectsState` 1, `DelayOrder` 1, `DelayPayment` 1,
`RuleCustomerScope` 1]. [CODE `research/kg_reentry_loop/application-addition.yaml`].
[CODE `.claude/worktrees/umr-thin-slice/research/umr_thin_slice/marine-links.yaml`
at `83014632`]. [CODE `src/malleus/recon/store.py` 83 to 128, 915 to 939]

Two readings follow. [REASONING]

- No consumer follows the proposed rule consistently. Both carriers carry both
  kinds. The re-entry loop carries one link on both carriers at once.
- The Shop's stable-identity pattern already avoids the problem where it
  applies: structure points at `SupplierOrder`, which is not revised; the
  versions point at it. HISTORICAL-USE-01 option (v), a stable passage
  identity for UMR, is the same pattern.

### Summary of section A

| Question | Record's position | Proposed rule |
|---|---|---|
| Is a relation a reified record with properties? | Yes (root ontology, n-ary pattern) | Agrees |
| May a relation be an endpoint? | No; use a class-valued slot to the relation (OD-010) | Agrees |
| Must a class-valued slot resolve? | Yes, strong, class ancestry (OD-010) | Silent; relies on it not being built |
| May a current record name a retired version? | Current view must be closed for slots and edges (OD-010) | Contradicts for slots |
| Is link behaviour on revision tied to carrier? | No; declared per dependency kind (foundation graph 5.3, Candidate; REPRESENTATION-OPTIONS-01) | Contradicts |
| Which carrier for a use? | Adopter's choice (maintenance plan section 2) | Would decide it |

## B. What the code enforces today

| # | Fact | Evidence | Role |
|---|---|---|---|
| B1 | A relation endpoint must exist and be of kind ENTITY, and match the declared range. | [CODE `kg.py` 364 to 382, messages at 370 and 373] | OD-010 accepted design under the default typed-graph `OPTIONAL_PROFILE`; this is its `REFERENCE_IMPLEMENTATION` |
| B2 | Retiring a record refuses while a non-retired relation touches it at either end, and while an event participation or signal names it. | [CODE `kg.py` 169 to 195] | Reference implementation of OD-010's closed-view rule, for edges, participations and bearers only |
| B3 | The same refusal fires first at CHECK, because the check base is rebuilt through `from_records`. | [CODE `admission.py` 374 to 405] | Reference implementation |
| B4 | Relations carry properties, validated against the relation class. | [CODE `kg.py` 570 to 606, `_validate_payload` 521] | Default typed-graph profile |
| B5 | A signal may bear a relation. | [CODE `kg.py` 403 to 412] | OD-010 accepted design |
| B6 | A class-ranged, non-inlined slot is checked only for a nonblank string. Existence and class are not checked. | [CODE `ontology.py` 1436 to 1446; `_contract_pipeline/view.py` 584 to 591] | A gap against OD-010, not a design choice |
| B7 | The population-plan path checks relation endpoints, participation endpoints and one slot by name, `subject`, against records in the plan and current records only. A plan whose `subject` names a retired version refuses `DANGLING_SUBJECT`. | [CODE `population.py` 53, 1190 to 1236; base state from active history only, 299 to 334] Not probed. | Reference implementation; the slot name is a literal in code, not a contract fact |
| B8 | `version_referrers` follows class-ranged non-inlined slots (also inside inlined values), relation endpoints and participation endpoints, over every version in history. It does not follow `bearer_id`. | [CODE `knowledge.py` 691 to 712, 1056 to 1130; no `bearer` in the file] | Reference implementation, this branch only |
| B9 | `version_referrers` states `UNRECORDED_USES`, `RULE_READS`, `QUERY_SCOPES`, `STRING_RANGED_SLOTS` as not covered. | [CODE `knowledge.py` 646 to 658] | Same |
| B10 | The rule layer sees relations as `m_relation/4` facts and slot values as `m_property/4`. | [DOC `handover/2026-09-19-rules-inside-the-ontology-findings.md`, fact contract v3; CODE `logic.py` 44 to 46, 495 to 505] | Logic-monitoring profile |

### Probe on today's Core

Contract `contract.yaml` (sha256 `fbe78cbc…`): `Assertion`, `Use` with
`premise` ranged `Assertion`, `Review` with `reviewed` ranged on the relation
class `Cites`, and `Cites` from `Use` to `Assertion`. Script `probe.py`
(sha256 `6c3cfea9…`), output `output.txt` (sha256 `f3e16e1d…`), in the session
scratchpad under `carrier-probe/`, not in git. Every step is one change set
through `check_and_admit_change_set` under the structural history, valid time
`NONE_STATED`; revisions declare `REVISION`. Run with
`PYTHONPATH=<core-temporal>/src <repo>/.venv/bin/python probe.py <core-temporal> <out dir>`.

Output, verbatim:

```text
Q1-seed-slot-to-relation: ADMITTED
Q1 version_referrers(c1): [('v1', 'reviewed', 'c1', 1, True)]
Q2-revise-relation-c1-not-restating-review: ADMITTED
Q2 current ids: ['a1', 'c1b', 'u1', 'v1']
Q2 v1.reviewed: c1
Q2 version_referrers(c1): [('v1', 'reviewed', 'c1', 1, True)]
Q4-revise-a1-alone-with-live-relation: REFUSED CHECK/STRUCTURAL_REFUSAL: Cannot rehydrate graph from records: relations[0] 'c1b': Target entity 'a1' does not exist (ledger unchanged: True)
Q3-seed: ADMITTED
Q3-revise-a1-alone-with-slot-use: ADMITTED
Q3 u1.premise: a1 a1 current: False
Q3 version_referrers(a1): [('u1', 'premise', 'a1', 1, True)]
Q5-slot-names-nonexistent: ADMITTED
Q6-new-slot-use-of-retired-a1: ADMITTED
Q6 version_referrers(a1): [('u1', 'premise', 'a1', 1, True), ('u3', 'premise', 'a1', 1, True)]
Q7-new-relation-to-retired-a1: REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: Target entity 'a1' does not exist (ledger unchanged: True)
```

What it shows:

- Q1, Q2: a record can name a relation by a class-ranged slot, the impact read
  finds it, and revising the relation does not block the record. Edge-of-edge
  already works through the OD-010 shape.
- Q3, Q4: the asymmetry HISTORICAL-USE-01 section 6 described, on a minimal
  contract.
- Q5: a slot naming a record that never existed is admitted (B6).
- Q6, Q7: a use recorded after the fact can name a retired version by slot,
  and cannot by relation. The slot route is the only way today to record late
  that something used an older version.

Nothing in Q2, Q3 or Q6 checks that the current graph is closed, which OD-010
requires. [PROBE, DOC]

## C. Failure modes each way

### If uses stay edges

| Failure | Evidence | Fixable by |
|---|---|---|
| The block recurs one level up when a supplement is linked by relation | C2 in HISTORICAL-USE-01; Q4 here | A declared VERSION relation kind, with retired versions legal endpoints (option 2 or 3) |
| Restating a use edge onto the successor claims a use that never happened | CORRECTION-RESEARCH-01 D | Same |
| The refusal says "does not exist" about a record in history | P2a, Q4, Q7 | A typed refusal (HISTORICAL-USE-01 (vi)); moves no identity |
| The live Shop `CorrectsState` edge will block the first revision of `B:Y:e7` | [CODE Shop context and plan, REASONING] not probed | Remodel, or option 2 or 3 |

### If uses become records with reference slots

| Failure | Evidence | Fixable by |
|---|---|---|
| A dangling or wrong-class reference is admitted | Q5; P2g; REFINEMENT-SPEC-05 P3 | Resolve at admission (OD-010). Which set it resolves against is the decision: current records breaks the rule (Q3 would refuse); record history keeps it |
| A wrong version is admitted: nothing distinguishes naming `a1` on purpose from naming it by mistake after `a1b` exists | Q6 | Not by resolution. Only a declared kind, or a reader's check, can say "this reference must name a current version" |
| A structural reference held in a slot dangles unseen: `sentence_root` kept naming the retired root | P2g | Only by a declared STRUCTURAL slot kind that blocks like B2 |
| The current graph is not referentially closed, against OD-010 | Q2, Q3, Q6 | Amend OD-010 for version references, or refuse |
| One node per use; readers must learn new record types; `query_relations` and `m_relation/4` do not return uses | Probe C1 and C3 in HISTORICAL-USE-01; B10 | Reader and rule changes, per adopter. Not fixable in Core |
| The plan path refuses a `subject` naming a retired version | B7, not probed | Change the plan check to the chosen resolution set, and read the slot list from the contract instead of a literal |
| The impact read does not follow `bearer_id` | B8 | One more link kind in `version_referrers` |

### Failures that do not depend on the carrier

- **Implicit rebinding through a composite (P2b).** `version_referrers(s1u)`
  finds the arcs that name `s1u` and stops, because nothing names an arc. A use
  that names the root `s1i`, by relation or by slot, is not reached, because
  the walk would have to go from the arc to its source, then to the source's
  users. Nothing tells Core which end of an arc is the whole. [CODE
  `knowledge.py` 1097 to 1117; REASONING] The fix is a declared containment
  direction, or composite versioning (a new root version whenever a
  constituent changes, as P2j did), or a stable identity the use can name.
- **Membership and absence uses, rule reads, query scopes.** Already listed
  as not covered (B9). No carrier choice changes them.

## D. The alternatives

G3's identity routes: A an optional field, B a grammar bump, C structural
builtin version 2, D the state-version profile. [DOC `g3/RESULTS.md`,
"Blast radius"] Anything that changes what the builtin admits for the same
bytes forces C at merge (R-07; DECISION.md).

### (1) Rule the convention as stated

A relation is structural; a class-ranged slot names an exact version.

- Rulings: fits R-01, R-05 (the read was built for it), R-06, R-10 (the UMR
  interpretation record is this shape). R-04's `HISTORICAL_USE_ENDPOINT`
  becomes a permanent refusal, not a roadmap item.
- Law 8: holds only once slot resolution is built; until then a dangling
  reference is silent (Q5). Law 12: the meaning sits in the carrier kind, a
  generic rule, and must be written into an identified artifact so a second
  interpreter applies it. Law 13: unaffected.
- OD-010: must be amended. Class-valued slots resolve against record history
  (any version, exact class), and are exempt from current-view closure.
  Otherwise building R-05 breaks the rule.
- What moves: the builtin at merge once resolution is built (Q5 flips from
  admitted to refused), which can travel with R-07's route C so evidence is
  regenerated once. Shop: `CorrectsState` is on the wrong carrier by this
  rule; an additive revision can add a slot, and the relation stays in
  history. Computational-graph and re-entry research: frozen evidence, stays
  as it is, labelled as written before the rule. UMR: `CANDIDATE_REUSE` is
  kind 2 and correct as a relation; `sentence_root` loses any hope of
  protection, since every class-ranged slot is by rule a version reference.
  Recon: its own store and latest-version semantics; unaffected.
- Second interpreter needs: every non-inlined class-valued slot resolves in
  history with class ancestry and never blocks; relation endpoints resolve in
  the current view and block; the impact read follows both.
- Failing test that starts it: `Use.premise` naming `nope` refuses at CHECK
  with a typed reason (today admitted, Q5); `Use.premise` naming a record of
  the wrong class refuses; Q3 and Q6 stay admitted and the current view
  replays without refusal.
- Cost of the rule itself: no structural slot is expressible. A slot that is
  structure, like `sentence_root` or `SupplierOrderState.order_id`, silently
  keeps naming an old version when its target is revised.

### (2) The other way round: uses are edges

Core lets a retired version stay a legal endpoint for relation classes the
ontology declares as uses. The version graph and the current view split.

- Rulings: fits R-01, R-06. R-02 allows it only as a view derived inside Core
  from the ledger, not a second store. R-04's `HISTORICAL_USE_ENDPOINT` is
  lifted.
- OD-010: amended for declared use relations (endpoint may be a retired
  version) and for closure (the current view keeps the edge while excluding
  its target, or drops it and hides a current fact about the past).
  HISTORICAL-USE-01 7(ii) states the same dilemma.
- What moves: `_without_records`, `_check_base`, the endpoint check replayed by
  `from_records` (B1 to B3); a declaration carrier (root mixin moves every
  contract importing `malleus.yaml`, unmeasured; a compiler fact kind moves the
  compiler grammar; an optional profile vocabulary moves only its importers);
  route C always. Fits existing practice: Shop `CorrectsState`, computational
  graphs, re-entry loop. Maps directly to PROV `prov:used` with the relation's
  properties as `prov:Usage` attributes.
- Second interpreter needs: the list of use relation classes and the rule for
  what the current view shows of their edges.
- Failing test: HISTORICAL-USE-01 7(ii): a declared use relation names `r1`,
  `r1` is revised without restating it; expected admitted, relation current,
  `r1` not current, current view rehydrates, `version_referrers(r1)` lists it
  current. Today: Q4. Guard: an undeclared relation still refuses.
- Does not solve: structural slots (P2g); a use that must be recorded after the
  fact (Q7) needs the same endpoint rule.

### (3) Both carriers; the reference kind is declared

Each relation class and each class-ranged slot is STRUCTURAL or VERSION. Core
acts on the declaration, not on the carrier. STRUCTURAL: resolves in the
current view, blocks retirement until restated, current view closed. VERSION:
resolves in record history with class ancestry, never blocks, impact read
follows it. Defaults while nothing is declared: relation STRUCTURAL, slot
VERSION, which is today's behaviour.

- Rulings: fits all of R-01 to R-10. R-05 said dependencies are "not declared
  per use"; this declares per slot or class, once in the ontology, which is the
  reasoning R-05 itself gives ("the ontology marks it once"). It is the shape
  foundation graph 5.3 (Candidate) and REPRESENTATION-OPTIONS-01 already
  describe.
- Law 12: the meaning lives in contract facts, which is where it belongs. Law
  8: nothing is inferred from the carrier once declared; the defaults must be
  written into the builtin's identified contract.
- Where the declaration lives, and what it moves. It must be inside the
  contract identity: two ontologies that differ only in reference kind admit
  different histories. An annotation outside the hash would violate law 8;
  adoption annotations are outside it (`docs/ONTOLOGY_PROTOCOL.md`,
  "Adoption"). Candidates: an optional profile vocabulary, as
  `profiles/object-event.yaml` is, imported only by adopters that need it,
  carrying a mixin for VERSION relation classes (mixins are already contract
  facts); for slots, a LinkML construct not yet chosen. I did not check which
  slot-level construct the compiler binds. A kind change on a used slot is not
  additive and must refuse under the revision policy.
- Phasing, each phase a separate ruling:
  1. Now: rule the distinction, the vocabulary and the defaults; amend OD-010
     so VERSION references resolve in history; document the defaults in the
     acolyte skill and `CAPABILITIES.md`. Build slot resolution against
     history (Q5 refuses, Q3 and Q6 stay admitted). Route C at merge, with R-07.
  2. When a consumer needs a STRUCTURAL slot (UMR `sentence_root` is a
     candidate; P2g): declared structural slots block retirement as
     participations do (`kg.py` 185 to 195).
  3. When a consumer needs a VERSION relation (the Shop `CorrectsState` is one,
     once `B:Y:e7` is revised): option 2's storage change, for declared classes
     only.
- Second interpreter needs: the declared kind per slot use and relation class,
  the defaults, and the two resolution sets.
- Failing tests: phase 1 as in (1). Phase 2: a slot declared STRUCTURAL whose
  target is revised without restating the referrer refuses with a typed
  reason; today admitted, P2g. Phase 3: a relation class declared VERSION whose
  target is revised without restating it is admitted; today Q4.

### (4) Reify every relation as a record

Relations become nodes with two class-ranged slots; edges disappear as a
carrier.

- The root ontology already reifies relations in the n-ary sense. What changes
  is storage and the admission rules. The structural-or-use question does not
  go away: it moves to the two endpoint slots, so (4) reduces to (1) or (3) at
  the slot level.
- What moves: every ledger's record families, `query_relations`, `m_relation/4`
  and every rule written against it, OD-010's endpoint rule, `from_records`,
  every adopter's export and reader. Route C and more.
- Literature does not require it: PROV keeps both `prov:used` and
  `prov:qualifiedUsage`; Wikidata keeps the primary relation inside the
  statement; RDF 1.2 keeps the asserted triple beside its reifier (section E
  below).
- Failing test: a relation admitted as a node is returned by
  `query_relations` and replays byte-identically. Not worth writing.
- Not recommended.

### (5) Leave it undeclared and document the pattern

- Moves nothing. The next adopter still picks a carrier by accident, as all
  four did. The OD-010 conflict stays latent and returns the day R-05's
  resolution is built. The Shop edge blocks its first revision with the "does
  not exist" message.
- No failing test.

### Side by side

| | (1) rule as stated | (2) uses are edges | (3) declared kind | (4) all records | (5) document |
|---|---|---|---|---|---|
| Contradicts OD-010 | yes, amend | yes, amend | amend once, explicitly | yes, rewrite | latent |
| Structural slot expressible | no | no | yes, phase 2 | via slots | no |
| Use as relation expressible | no | yes | yes, phase 3 | n/a | no |
| Identity moves | route C when resolution lands | route C plus a declaration carrier | route C at phase 1; declaration carrier at phase 2 or 3 | largest | none |
| Kg.py storage change | none | yes | only at phase 3 | yes | none |
| Existing adopters | Shop edge on wrong carrier | fits practice | fits practice | all move | unchanged |

## E. Literature, inherited not invented

Retained in this repository before this pass, cited rather than refetched:

- PROV-O: `standard:w3c-prov-o-2013` in
  `research/malleus_library_protocol_recon/ledger.jsonl`; `work:prov-o`,
  `evidence:prov-o` (section 4.2) and `claim:prov-o-revision-no-delta` in
  `research/ontology_migration_recon/ledger.jsonl`.
- de Kleer's ATMS: `claim:dekleer1986:atms` in the library-protocol recon and
  `claim:dekleer-atms1986:assumption-contexts` in
  `research/semantic_log_knowledge_projection_recon/ledger.jsonl`;
  CORRECTION-RESEARCH-01 section E read section 4.9.
- Doyle 1979: `claim:doyle1979:tms`, library-protocol recon.
- W3C n-ary note, Rost et al. and Anselma et al. on bitemporal property graphs:
  `design/temporal/BITEMPORAL-RESEARCH-01.md` items 1 to 3.
- Wikidata, RDF 1.2, TypeDB, Neo4j: verdicts in `docs/DELIMITATIONS.md`, not as
  Recon records.

No Recon ledger holds a record for Wikidata's statement model, RDF 1.2
reifiers, RDF 1.1 reification or the property-graph model. I fetched those and
wrote no Recon record, since this brief permits only this file and the
journal.

| Source | Mechanism read | Transfers | Does not transfer | Use |
|---|---|---|---|---|
| PROV-O, W3C Rec 2013, https://www.w3.org/TR/prov-o/ section 3.3 | "The Qualification Pattern restates an unqualified influence relation by using an intermediate class that represents the influence between two resources." `prov:qualifiedUsage` "references an instance of prov:Usage, which in turn provides attributes of the prov:used relation". PROV keeps both. | A use is an occurrence that can carry attributes. The binary shortcut and the qualified node coexist; neither replaces the other. A Malleus relation with properties is already a qualified influence. | PROV is descriptive vocabulary: no admission, no blocking, no resolution. | IMPLEMENTATION_CANDIDATE for export (DELIMITATIONS already says map onto); DESIGN_CONSTRAINT: keep occurrence identity |
| PROV-DM, https://www.w3.org/TR/prov-dm/ 5.1.1, 5.1.4, 5.1.8, 5.5.1 | An entity is "a physical, digital, conceptual, or other kind of thing with some fixed aspects". Usage has "an OPTIONAL identifier". Specialization links a more specific entity to a general one. Invalidation: "no longer available for use". | A use names an entity with fixed aspects, which in Malleus is an exact version. `specializationOf` is the Shop's pattern: versions point at an enduring identity. Invalidation is not falsity. | Invalidation forbids later use; Malleus may record a late use of an old version on purpose (Q6). | DESIGN_CONSTRAINT |
| RDF 1.1 Semantics, https://www.w3.org/TR/rdf11-mt/ appendix D.1 | "A reification of a triple does not entail the triple, and is not entailed by it." The subject of a reification refers "to a concrete realization of an RDF triple ... rather than a triple considered as an abstract object." | The occurrence-versus-type distinction. | Four triples per statement and no link between the statement and the asserted triple. A Malleus relation is asserted and identified in one record. | EXPLICIT_EXCLUSION as a carrier |
| RDF-star CG report, 17 Dec 2021, https://www.w3.org/2021/12/rdf-star.html section 2.3 | "there is exactly and only one RDF-star triple with subject s, predicate p, and object o." Distinguishing occurrences "requires additional nodes", with `:occurrenceOf`. | Annotating a triple by its content annotates the type, every occurrence. Malleus relations have their own IDs, so they are occurrences. Never key a relation or its annotations by (source, type, target). | Quoted-triple syntax. | DESIGN_CONSTRAINT |
| RDF 1.2 Concepts, CR Snapshot 7 Apr 2026, https://www.w3.org/TR/rdf12-concepts/ | A reifying triple has predicate `rdf:reifies` and a triple term as object; its subject is a reifier. Triple terms are not asserted. "There can be multiple, distinct reifiers related to the same abstract proposition". | A Malleus relation is close to an asserted triple plus one reifier. A record naming a relation by slot (Q1) is close to a statement about a reifier. This answers DELIMITATIONS' "why not RDF 1.2 reifiers" in part: Malleus already has reifier identity; what it adds is the typed gate. | Unasserted propositions are not a Malleus relation; they are a claim record. The standard is not final. | BASELINE_OR_ORACLE for an export mapping |
| Wikibase data model, https://www.mediawiki.org/wiki/Wikibase/DataModel, "Statements", "Ranks"; Wikidata Help:Statements | A statement is a main claim with qualifiers, references and a rank; deprecated means "may not be considered reliable or ... known to contain errors". Values are entities or data values; the data model page shows no statement-as-value. Help:Statements: each statement has a GUID. | Statement nodes with identity, qualifiers and references, kept not deleted: what Malleus relations plus supersession already do. Wikidata also has no edge-of-edge. | Rank is changed in place on one statement; Malleus makes a new version. Soft constraints. | DESIGN_CONSTRAINT (corroboration) |
| Hernández, Hogan, Krötzsch, "Reifying RDF: What Works Well With Wikidata?", SSWS 2015, https://ceur-ws.org/Vol-1457/SSWS2015_paper3.pdf sections 1, 2 | Compares standard reification, n-ary relations, singleton properties and named graphs for Wikidata. Section 2: one primary relation can appear in distinct statements (two non-consecutive terms of one president), so quins keyed by the primary relation fail. | Occurrence identity is required as soon as the same relation holds twice with different qualifiers. | Their query-time benchmark. I read pages 1 to 3 only. | DESIGN_CONSTRAINT |
| Neo4j, "Modeling designs", "Intermediate nodes", https://neo4j.com/docs/getting-started/data-modeling/modeling-designs/ | Hyperedges and relationship-to-relationship links are "not supported in Neo4j but can be solved by using an intermediary node". | The standard property-graph answer to edge-of-edge is an intermediate node: OD-010's Quiet Bell shape and Q1 here. | Neo4j's own storage. | DESIGN_CONSTRAINT |
| TypeDB, "Data and query model", https://typedb.com/docs/typeql-reference/data-model/ | "Relation types can also have capabilities, i.e. play roles or own attribute types. This ... allows the creation of nested relations". "Relations without role players will be removed (no 'dangling relations')." | Edge-of-edge is a storage-model choice, as OD-010 says. | Cascade removal. OD-010 excludes cascade and deletion. | BASELINE_OR_ORACLE (nested relations); EXPLICIT_EXCLUSION (cascade) |
| W3C, Defining N-ary Relations on the Semantic Web, WG Note 12 Apr 2006, https://www.w3.org/TR/swbp-n-aryRelations/ use case 1, pattern 1 | Use case 1 is a binary relation needing attributes. Pattern 1: "We create an individual that represents the relation instance itself, with links to all participants." | Already inherited: the root ontology names this pattern for `Relation`. | OWL restriction considerations. | DESIGN_CONSTRAINT (held) |
| Rost et al.; Anselma et al., bitemporal property graphs (retained, BITEMPORAL-RESEARCH-01 items 1, 2) | Rost imposes endpoint-period containment on edges; Anselma permits relationships between entities with different valid periods, for ancestry and causation. | An edge to a past version is legitimate modelling. Whether it is allowed is a declared modelling decision, not a universal rule. Supports (3). | Their storage. | DESIGN_CONSTRAINT |
| de Kleer, ATMS, 1986 (retained) | Justifications are kept as their own records linking antecedents to a consequent; retraction adds, never removes (section 4.9). | A justification is a use reified as a record, naming exact nodes. Supports keeping uses addressable. | Automatic label propagation. R-06 excludes it. | DESIGN_CONSTRAINT |
| Ontology design patterns (Gangemi and Presutti, Situation and n-ary comparison) | Not read. The ODP portal refused the connection and the comparison paper returned 403. | Nothing claimed. | | not established |

What the literature says about the decision, in one line: every mature model
gives a qualified link its own identity and lets other statements refer to it
through an intermediate node, and none of them decides what happens on
revision by the carrier. That is a declared modelling choice in each.
[REASONING over the rows above]

## F. What "edge" and "entity" should mean after this

Proposed sentence set for the acolyte skill, not written there:

> In Malleus every record is one identified version. Replacing it makes a new
> version and the old one stays in history. An entity is a thing the graph
> talks about. A relation is also a record, reified so it can carry
> qualifiers, but it joins two current entities: it is structure of the
> current account, so when either end is revised you restate or revise the
> relation in the same change set, or Core refuses. A link that must keep
> naming the exact version it was written about, such as a calculation's
> input, an interpretation of a node, or an explanation of why a version
> exists, is a version reference. Today its only carrier is a record with a
> class-ranged slot: it stays on the version it names, it never blocks a
> revision, and the impact read finds it. Choose the carrier by what the link
> must do when its target is revised: follow the target, or stay on it.
> Citation, attribution, support and application can each need either, so
> decide per link, not per word. Point structure at an enduring identity where
> you can, so revising a version never touches it. A relation cannot point at
> a relation; to say something about a relation, make a record whose
> class-ranged slot names it.

If (3) is ruled, the sentence "Today its only carrier" becomes "Without a
declaration", and the declaration is added.

## G. Recommendation

**Rule (3) phase 1.** Rule the distinction as two declared reference kinds,
STRUCTURAL and VERSION, with today's carriers as the stated defaults. Amend
OD-010 so a VERSION reference resolves in record history with class ancestry
and is exempt from current-view closure. Put the paragraph in section F into
the acolyte skill and `CAPABILITIES.md`. Build slot resolution against history
RED then GREEN on the branch, and take its builtin version with R-07's route C
so the evidence is regenerated once. Add HISTORICAL-USE-01's typed refusal and
`not_covered` entry, and `bearer_id` to the impact read.

Why not (1) as stated:

1. It contradicts OD-010, and only holds while OD-010's slot half is unbuilt.
   R-05 already records that gap as something to close.
2. It removes the structural slot. P2g showed one in the UMR graph and the Shop
   has one in `order_id`.
3. It rules against the carrier choice of the live Shop and two research
   consumers, all with a different shape.
4. The repository's own design (foundation graph 5.3, REPRESENTATION-OPTIONS-01)
   and the literature both declare link behaviour by kind, not by carrier.

Why not (2) or (4) now: they change storage for consumers that can wait. The
Shop edge becomes urgent only when `B:Y:e7` is revised.

Costs:

- One OD-010 amendment, ruled by Luis.
- Builtin version 2 at merge; it moves the check contract, structural policy,
  normative profile, history bundle and every structural ledger head
  (OVR-000466 blast radius). Bundled with R-07, not added to it.
- The declaration construct for slots is not chosen and needs a probe against
  the compiler before phase 2.
- Two documentation changes through their governed paths.

What stays unresolved:

- Implicit rebinding through composites (P2b). No carrier fixes it. It needs a
  declared containment direction, composite versioning, or a stable identity.
- Whether the plan path's `subject` check (B7) moves to history resolution and
  reads its slot list from the contract. It must, under any option that lets a
  claim name an old version.
- The Shop `CorrectsState` edge: remodel as a slot by additive revision, or
  wait for phase 3. Luis's call when `B:Y:e7` is next revised.
- UMR option (v), a stable passage identity: adopter modelling, not probed.
- Membership, absence, rule reads and query scopes (B9).
- Whether defaults belong in the builtin or in the profile. Both are
  identified artifacts; the choice decides which identity moves.

Decisions for Luis, one at a time:

1. Is link behaviour on revision tied to the carrier (option 1), or a declared
   kind with carrier defaults (option 3)? Recommendation: 3.
2. Amend OD-010 so a reference to an exact version resolves in record history
   and is exempt from current-view closure? Recommendation: yes. Any option
   except (5) needs some amendment.
3. Build slot resolution against history now, with R-07's route C?
   Recommendation: yes.

## Limits

- One minimal probe contract; structural policy only; no Prolog rule layer.
  B7 (plan-path `subject`) is read from code, not probed.
- The Shop was inspected, not probed: I did not revise `B:Y:e7`.
- Paper graphs: 42 ontology files under `paper-v4` declare `Relation` or
  `ResearchRelation` subclasses (grep count). None was read.
- ODP guidance was not reached. Hernández et al. read to page 3. The
  Wikidata statement GUID comes from Help:Statements; the data model page
  I fetched did not state it.
- The OD-010 contradiction is read from its text. OD-010 has no
  implementation to probe.
- Probe files live in the session scratchpad, hashed above, not in git.
