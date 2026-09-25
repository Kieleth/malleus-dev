# Historical use 01: revising a record that something points at

24 September 2026. A probe on the real UMR graphs, not an argument. No `src/`
change. Core is T3 at `aadddfe8` on `codex/core-temporal`. The UMR inputs are
read from `codex/umr-thin-slice` at `74ff7a42`.

The risk as the Overlord stated it: Core will not retire a record that a
relation points at. Revising the UMR number would mean moving those relations
onto the new version, and that would claim the RC2 application used the new
reading, which it never did.

Labels: [CODE] file and line read. [PROBE] command run, output quoted.
[INSPECTED] document or file read. [REASONING] my inference, not run.

## Answer in brief

1. The block is real and sits in two places, not one. `admission.py`
   `_check_base` (lines 373 to 405) refuses at CHECK, before the builtin runs,
   because `KnowledgeGraph.from_records` rebuilds every live relation through
   the endpoint check (`kg.py` 364 to 373, message joined at `kg.py` 257).
   `_apply_change` would refuse the same case again in `_without_records`
   (`kg.py` 169 to 184). [CODE, PROBE]
2. For the natural target, the ± node, the RC2 edge is not incident. Its three
   incident edges are arcs of the same annotation. Restating them is honest,
   and Core admits it. [PROBE P2a, P2b]
3. The RC2 application is a relation edge (`MarineReuseHypothesis`,
   `CANDIDATE_REUSE`) in the Marine 02 graph only. It runs from the caption's
   root to the main clause's root, and its status can only be `CANDIDATE`. It is
   an authored hypothesis that one passage applies an estimate the other
   reports. It is not a record of anything that used our reading. The UMR
   graphs contain zero edges that record a use of a specific reading.
   [INSPECTED, PROBE]
4. The risk as stated becomes real in one route. The UMR bridge addresses
   every record by the hash of its UMR bytes. So an honest annotation
   correction arrives as a whole new artifact, and then every main-clause
   record is revised, the root included. Core refuses that on exactly the
   reuse edge. Restated, it is admitted. [PROBE P2i, P2j]
5. A different hazard is real and was not in the risk as stated. After
   revising only the ± node, the untouched reuse edge reaches the refined node
   in the current graph. Nothing refuses. The impact read of T3 does not report
   the edge, because it stops at the arcs. [PROBE P2b]
6. The supplement pattern works through the normal gate. Its best form holds
   the prior reading as its own interpretation record, then revises that
   record with the R32 evidence. That gives a declared REVISION closing. The
   annotation and the reuse edge stay untouched. [PROBE C4]
7. Recommendation. For UMR now: the C4 shape. For Core next: no
   retired-endpoint change yet, because no consumer has a use that must be a
   relation. Instead, rule the carrier convention that Core already follows
   without declaring it, and make two small changes that move no identity: a
   typed refusal, and one more `not_covered` entry. Section 8 has the costs.

## 1. Inputs and identities

| Input | Identity | How read |
|---|---|---|
| Core | `aadddfe881edd763d5aff2adf70ab43c2fe38f54`, tree clean; `tests/contract_compiler/pareto/test_temporal_revision.py` 19 passed | [PROBE] `git rev-parse HEAD`, pytest |
| `malleus.__file__` | `.claude/worktrees/core-temporal/src/malleus/__init__.py` | [PROBE] |
| UMR research inputs | `bridge.py`, `main_clause.py`, `marine.py`, `marine_links.py`, `marine-links.yaml`, `ontology.yaml`, `quantity.py`, `run.py`, and four fixtures, each byte-equal to `74ff7a42` | [PROBE] sha256 of the copy against `git show 74ff7a42:` |
| Main-clause-04 ledger (copy) | sha256 `5ca5f5e6c6ad1f478c0e94689f765afd59fb977686eb86a5f1481a3357f6f0c6`, the hash `MAIN-CLAUSE-RESULTS-04.md` records | [PROBE] |
| Marine 02 ledger (copy) | sha256 `74e161f14f4edebb650b39586f199a3f8987a0db7700453c81c84e15776f7f8f`, the hash `MARINE-02.md` records | [PROBE] |

Both ledgers were written by Core `ebff70f7`. T3 reopens and replays them
without complaint. Every probe ran on a fresh copy of one of them. No
new annotation was captured.

The UMR branch moved to `83014632` during this work. That commit adds
`REFINEMENT-SPEC-05.md` and a journal entry from the other agent. I did not
read either, so the two probes stay independent.

Probe files, in the session scratchpad under `historical-use-probe/`, are not
in git. sha256 prefixes: `probe_lib.py` e9883db9, `inventory.py` 4e5e18f6,
`probe_revision.py` 9a62e369, `probe_supplement.py` 9298fc55,
`probe_artifact.py` 8d5e9bb2, `probe_interpretation.py` fec95c15,
`diag_revision.py` e344e1e8, `refinement-v2.yaml` 7ab51c41,
`refinement-mc04.yaml` 5264acf5. Run each with
`PYTHONPATH=<core-temporal>/src:<probe dir>` and the repository venv.

## 2. The real graph

### Main-clause-04, one change set, 26 ledger events

29 entities: 19 `UmrConcept`, 6 `UmrLiteral`, 3 `UmrAnchor`, 1 `UmrSentence`.
31 relations, all `UmrArc`. Valid time `ORDER_ONLY capture:1`. There is no
cross-annotation edge. [PROBE `inventory.py`]

| Candidate target | Concept | In | Out | Typed slots naming it |
|---|---|---|---|---|
| `s1d` | distribution-range-91 | 1 (`:extent` from s1h) | 2 (`:ARG1` s1q, `:ARG4` s1u) | 0 |
| `s1u` | distance-quantity, the ± radius | 1 (`:ARG4` from s1d) | 2 (`:quant` 0.3, `:unit`) | 0 |
| `s1q` | distance-quantity, the centre | 1 (`:ARG1` from s1d) | 2 | 0 |
| `s1h` | have-mod-91, the proposition | 3 (`:ARG1` SENTENCE, `:unspecified` MODAL, `:contained` TEMPORAL) | 5 | 0 |
| `s1i` | indicate-01, the root | 3 (`:full-affirmative` MODAL, `:modal-predicate`, `:contained` TEMPORAL) | 5 | 1 (`UmrSentence.sentence_root`) |

### Marine 02, one change set, 24 ledger events

40 entities: 24 `UmrConcept`, 9 `UmrLiteral`, 4 `UmrAnchor`, 2 `UmrSentence`,
1 `MarineReference`. 40 relations: 37 `UmrArc`, 2 `MarineCitation`, 1
`MarineReuseHypothesis`. The main clause uses the v1 fixture, where ± is a
generic `uncertainty` node. [PROBE]

| Main-clause target | Concept | In | Out | Slots |
|---|---|---|---|---|
| `s1u` | uncertainty | 1 arc (`:mod` from s1q) | 2 arcs (`:quant` 0.3, `:unit`) | 0 |
| `s1q` | distance-quantity | 1 arc | 3 arcs | 0 |
| `s1h` | have-mod-91 | 1 arc (`:ARG1` from s1i) | 3 arcs | 0 |
| `s1i` | indicate-01, root | 1 arc (MODAL) + **1 `CANDIDATE_REUSE`** from the caption root | 3 arcs + **1 `MarineCitation`** to reference 32 | 1 (`sentence_root`) |

The caption's root, `s1h`, is the source of the reuse edge and of its own
citation. Its `s1u` has the same 1 in and 2 out as the main one.

### What each arc means

A UMR arc (`:mod`, `:quant`, `:ARG1`, the modal and temporal triples) is part
of one annotation of one clause. `CITES_REFERENCE` links a clause to the local
bibliography entry. `CANDIDATE_REUSE` is the authored interpretation of
Marine 02: "the source clause applies an estimate described by the target
clause". Its rationale refers to the two passages and their shared citation,
not to any reading of ±. [INSPECTED `marine-links.yaml`, `fixtures/marine-reuse.json`]

The T3 impact read never goes deeper than 1 on these graphs. From any node it
lists the arcs that touch it, in or out. Nothing names an arc, so the walk
stops there. [PROBE: `version_referrers` maxdepth 1 on all 14 inventoried nodes]

## 3. REVISION as T3 ships it

Every case sends one change set through `check_and_admit_change_set`, with
valid time `ORDER_ONLY capture:1` (a REVISION must carry the target's period,
`knowledge.py` `_revise`). Successor IDs append `@rev1` to the old ID, keeping
the annotation's prefix so the readers can still select it. [PROBE `probe_revision.py`,
`probe_artifact.py`, `probe_supplement.py`]

| Case | What was revised | Verdict |
|---|---|---|
| P2a | Marine 02 `s1u` alone, concept to standard-deviation | REFUSED at CHECK, all 3 arcs named |
| P2b | the same, with its 3 arcs restated | ADMITTED |
| P2c | proposition `s1h` alone | REFUSED, 4 arcs named |
| P2d | `s1h` with its 4 arcs restated | ADMITTED |
| P2e | root `s1i` alone | REFUSED: citation, reuse edge and 4 arcs named |
| P2f | `s1i` with everything restated except the reuse edge | REFUSED on the reuse edge only |
| P2g | `s1i` with every incident relation restated | ADMITTED, with a dangling slot |
| P2h | as P2g, plus the `UmrSentence` | ADMITTED |
| P2i | the whole main annotation as new UMR bytes, 46 operations, reuse edge left | REFUSED on the reuse edge only |
| P2j | as P2i with the reuse edge restated, 47 operations | ADMITTED |
| B1 | main-clause-04: add a standard-deviation node and `:ARG6` arc from `s1d` | ADMITTED, no supersession |

The P2a refusal, verbatim (the long ID prefix shortened to `M:` here only):

```text
CHECK/STRUCTURAL_REFUSAL: Cannot rehydrate graph from records:
relations[9] 'M:arc:14': Target entity 'M:s1u' does not exist;
relations[16] 'M:arc:20': Source entity 'M:s1u' does not exist;
relations[17] 'M:arc:21': Source entity 'M:s1u' does not exist
```

The P2f and P2i refusal, verbatim:

```text
CHECK/STRUCTURAL_REFUSAL: Cannot rehydrate graph from records: relations[1]
'marine:47dab4804db0b632bdcef093e0c1ebf4e6a9ef384102bf4b92adaebbe9d8d355:reuse':
Target entity 'umr:463a2d3be1f3217c69e0acc72a8f90b6f47f8689665a1b3a01a4adc10e5a5b76:s1i' does not exist
```

The text says "does not exist" about a record that exists in history and is
being retired. R-04 lists this category as `HISTORICAL_USE_ENDPOINT`, a
first-cut refusal with its own reason. T3 has no such reason; the case
surfaces as `STRUCTURAL_REFUSAL`. [CODE `knowledge.py` has no member of that name; PROBE]

What the admitted cases returned:

- **P2b.** `record_history` of the old `s1u` has one closing,
  `(REVISION, s1u@rev1, change:probe:P2b...)`. `version_referrers(old s1u)`
  lists the 3 old arcs, not current, and nothing else. At the earlier position
  `replay_at` gives the old reading: `query_pair` and `query_estimate` return
  `model: UNSPECIFIED_IN_ANNOTATION`, and `verify_translation` passes. At the
  new head `query_estimate` refuses `CASE_PATTERN: expected uncertainty, found
  standard-deviation`, and `verify_translation` refuses `TRANSLATION_MISMATCH:
  annotation changed during translation`. **The reuse edge was not touched,
  but in the current graph it now reaches `s1u@rev1 standard-deviation`.
  Before the change it reached `s1u uncertainty`.**
- **P2d.** The readers pass, because nothing a reader reads changed.
  `verify_translation` refuses `TRANSLATION_MISMATCH: entities changed`.
- **P2g.** Admitted with the current `UmrSentence.sentence_root` still naming
  the retired `s1i`. Core does not check that a class-ranged slot resolves (the
  R-05 residual). Then `query_pair` refuses `PAIR_QUERY: each clause must cite
  the reference`. `query_estimate` fails with an untyped `KeyError` on the old
  root ID. `verify_translation` refuses `malformed translated records`.
- **P2h.** Everything restated, the sentence too. The readers pass;
  `verify_translation` refuses `entities changed`.
- **P2j.** The old reuse edge closes `(REVISION, change:probe:P2j...)`. The new
  edge points at the new root. `verify_translation` of the new artifact against
  its new UMR bytes passes. `query_pair` refuses `CASE_PATTERN` on the concept
  name, as in P2b. `version_referrers(old root)` lists the old citation, reuse
  edge, arcs and sentence, none current.
- **B1.** `record_history` of `s1d` shows no supersession and no closing.
  `read_main_clause` returns `deviation_kind: None` at the earlier position
  and `standard-deviation` at the head. It gives no sign that this role came
  from R32 rather than from the clause. `verify_translation` refuses.

Two facts follow for any in-place change to a UMR annotation. [PROBE, REASONING]

- The bridge's invariant is stricter than Core's. The graph must equal the
  translation of the retained UMR bytes (`bridge.py` `verify_translation`).
  Any per-record revision or in-place addition breaks it (P2b, P2d, P2h, B1).
  The only verified route is a whole new artifact (P2j). That is exactly the
  route in which the root is revised and the reuse edge has to move.
- The readers are closed, by design. Each new shape refuses with a typed
  `UmrRefusal`, except the dangling-slot case, which crashes. That the readers
  refuse is correct. It is a read-contract change to make deliberately, not a
  defect.

## 4. Structure and use

Three kinds of incoming edge showed up. The difference decides what restating
means.

| Kind | Example in these graphs | Restating onto the successor | Count at the ± node | Count at the root |
|---|---|---|---|---|
| 1. Constituent of the same annotation | `:mod`, `:quant`, `:ARG1`, modal and temporal triples | Honest: the revised annotation is made of these | 3 | 4 arcs + 1 sentence slot |
| 2. Link about the passage, whose endpoint stands in for the clause | `CITES_REFERENCE`, `CANDIDATE_REUSE` | Honest if the history records it, which REVISION of the edge does (P2j). But it would be unnecessary if the edge named a stable passage identity | 0 | 2 |
| 3. Use of a specific reading, such as a calculation that read ± as a standard deviation | none in either graph | Dishonest: it would claim a use that never happened | 0 | 0 |

The kind-3 example is not in any graph. MARINE-03 locates the earlier
hard-bound inference `s12` in a retained diagnostic answer file. [INSPECTED
`MARINE-03-SOURCE-AUDIT.md`, "Root diagnosis"]

How much of the risk is real:

- **As stated, in its dishonest form: not present.** No UMR edge records a
  use of a reading. The RC2 edge is our candidate hypothesis about two passages,
  and Y25's authors used R32's number, not any reading of ours. Moving the
  candidate onto a corrected annotation of the same clause does not claim a
  use of the new reading. It claims the candidate still relates the two
  passages, and the edge's REVISION closing records that it was moved. [REASONING
  from the inspected rationale; PROBE P2j]
- **As a block: real, in one route.** A genuine annotation correction must be
  a whole new artifact (section 3). That revises the root, and Core refuses
  until the reuse and citation edges are restated (P2i).
- **Not in the stated risk, and real: implicit rebinding.** A use that names a
  composite, such as a root, reads whatever its constituents are now. The
  record-level version of the root does not change when a leaf is revised.
  The use is silently rebound, and the impact read does not see it (P2b). Only
  the ledger position recovers what was read, through `replay_at`.
- **The Shop, inspected and not probed.** `shop.yaml` in both the tracked
  connected story and the private stage C inputs has zero Relation classes.
  References are class-ranged slots (for example `order_id`, range
  `SalesOrder`) and event participations. The quantity sits in
  `RecordedOrderState.ordered_quantity`. Nothing I found names an order state
  through a relation. The Shop's derivations are population-plan field
  derivations, which go from record field to source and never from record to
  record (CORRECTION-RESEARCH-01, A20). So a quantity revision does not meet
  this block as the Shop ontology stands. A revision of a `ShopObject` would
  meet the participation endpoints (`kg.py` 185 to 195); I did not probe that.
  [INSPECTED]

## 5. The supplement pattern

A live additive revision first added the vocabulary. Then records were added
through `check_and_admit_change_set`. [PROBE `probe_supplement.py`,
`probe_interpretation.py`]

The first fragment was refused:
`NON_ADDITIVE_CHANGE: contract revision adds a semantic fact outside the
allowed forms`. `diag_revision.py` names the four uncovered facts. Each is a
new enum type (`StatisticRole`, `InterpretationOrigin`, `RefinementKind`,
`ApplicationStatus` `rdf:type Enum`). `revision.py` `_derive_changes` (841 to
909) covers new classes, new slots, new slot uses and enum values; it does not
cover new enum types. R-07 already names a saved `core/add-enum-revision`
candidate. So the probe fragment `refinement-v2.yaml` uses one value added to
the existing `MarineLinkKind`, the existing `MarineInterpretationStatus`, and
string ranges for the statistic role and the origin. The typing is weaker than
intended.

| Case | What | Result |
|---|---|---|
| C1 | Contract revision (4 classes, 9 slots, 1 enum value), then a `CitedResult` for R32 Figure 5c, two `StatisticInterpretation` records (mean on `s1q`, standard deviation on `s1u`, origin `REVIEWER_INFERENCE`) and a `ResultApplication` naming `[s1q, s1u]` and the caption root, all by class-ranged slots | Admitted. Records at the genesis position unchanged; at the contract revision alone the exported records stay equal while the graph state digest and the contract identity both move (checked on a separate copy). `query_estimate` unchanged (`UNSPECIFIED_IN_ANNOTATION`); `verify_translation` passes; `query_pair` refuses `PAIR_QUERY: unhandled record family or type`. |
| C1, then P2b | Revise `s1u` with its arcs restated, on top of C1 | Admitted. `version_referrers(old s1u)` now lists `ResultApplication` via `applies_readings` and `StatisticInterpretation` via `interprets`, both `current=True`. Both still name the old `s1u`: they stay bound to the version they were written about. |
| C2 | As C1, plus one `RefinesReading` relation from the SD interpretation to `s1u` | The later revision of `s1u` is refused, on that relation: `relations[3] 'probe:refines:sd': Target entity '...:s1u' does not exist`. A supplement linked by relation recreates the block one level up. |
| C3 | The same supplement on main-clause-04 (entities only) | `read_main_clause` passes and ignores the new entities. `verify_translation` refuses `entities changed`, because this reader verifies the whole export. One non-UMR relation added in memory only: `read_main_clause` fails with an untyped `KeyError: 'layer'`. |
| C4 | The prior reading as its own record (`UNSPECIFIED`, origin `SOURCE_WORDING`, evidence the Y25 clause), then R32 arrives as a REVISION of that record | Both admitted. Closing `(REVISION, probe:stat:pm:v2, change:probe:C4-r32)`. The annotation `s1u` is not superseded. At the earlier position the interpretation is `UNSPECIFIED`; at the head it is `STANDARD_DEVIATION`. The application is untouched. |

What the supplement loses, and when that matters:

- The old reading stays in the current graph. That is right in this case.
  The Y25 clause does not define ±, and MARINE-03 says the annotation must not
  absorb R32 wording ("A source-faithful annotation and an evidence-enriched
  scientific interpretation must have distinguishable origins"). What changed
  is our interpretation, not the annotation. [INSPECTED]
- Without C4's prior record, nothing in record history says an account was
  superseded, and two accounts coexist with no declared closing. C4 closes
  that gap without touching the annotation.
- A reader must be taught to prefer the interpretation. That is a read
  contract change, as MARINE-03's table already requires ("Change the declared
  read contract and tests together").
- It is the wrong tool for a genuine annotation error, where the annotation
  itself is no longer the current account. That case is P2j.

## 6. What Core already does, stated plainly

Core already separates structure from use. It does so by carrier, and nothing
declares it: [CODE, PROBE]

- A relation is structural. It must resolve in the current graph, so it
  follows its endpoint (it is restated) or it blocks the retirement.
  `_check_base`, `from_records`, `_without_records`.
- A class-ranged, non-inlined slot names an exact version. It does not block,
  it stays on the version it names, and the impact read finds it
  (`knowledge.py` `version_referrers`; the T3 probe test; C1).

The UMR adopter used a relation for a link that is not structure (the
candidate reuse), and a slot for a link that is (`sentence_root`, which
dangled in P2g). Nothing told it which carrier means what.

## 7. Options for Core

Identity movement uses the G3 scenarios (`g3/RESULTS.md`, "Blast radius"):
A an optional field, B a grammar bump, C structural builtin version 2, D the
state-version profile. The OVR-000466 lesson applies to C and anything larger:
a moved policy digest moves every frozen coordinate, and grep undercounts.

### (i) Leave `kg.py` as is; document when to use which

Supplement for interpretations and uses; REVISION for records whose incident
relations are all structure of the same artifact.

- Failing test: none. This is documentation.
- Identity: none.
- R-05: unchanged.
- UMR: the C4 shape works now (probed).
- Shop: nothing is blocked today (inspected).
- Paper marine graphs: not inspected.
- Leaves: the misleading refusal text; the implicit rebinding in P2b stays
  invisible.

### (ii) A retired version stays a legal endpoint for declared historical-use relations

- Where it lands: `_without_records` (`kg.py` 169 to 184), `_check_base`
  (`admission.py` 373 to 405), and the endpoint check that `from_records`
  replays (`kg.py` 364 to 373). The current graph cannot hold a relation to a
  node it excludes. So this needs a version graph with a current view derived
  from it, or it drops the relation from the current graph. Dropping it would
  hide a current fact about the past. [CODE, REASONING]
- Who declares it: R-01 forbids inference, so the relation type must carry the
  declaration. There are three carriers. A root-ontology mixin moves every
  contract that imports `malleus.yaml`; that is not measured and is larger
  than C. A new contract-fact kind emitted by the compiler moves the compiler
  grammar. A per-adopter list in the policy or normative profile is D-like,
  one adopter at a time. Any carrier also changes what the builtin admits for
  the same bytes, which forces C (DECISION.md: under A two Cores with the same
  builtin identity would disagree).
- Failing test: a relation of a declared historical-use type points at `r1`,
  then `r1` is revised without restating the relation. Expected: admitted, the
  relation is current and names `r1`, `r1` is not current, the current graph
  rehydrates, and `version_referrers(r1)` lists it with `current=True`. Today:
  CHECK `STRUCTURAL_REFUSAL`, "Target entity 'r1' does not exist". A guard
  test: an undeclared relation type still refuses.
- R-05: no gain. The read already follows relation endpoints over history.
- UMR: P2i would pass without moving the reuse edge, but only if
  `CANDIDATE_REUSE` were declared a use. It is a passage-level link (kind 2),
  so that declaration would be a modelling error.
- Shop: no relations, so no effect.
- The promotion gate: there is no consumer with a kind-3 use that must be a
  relation, so there is none to build this for (`CORE_PROMOTION`).

### (iii) Uses are records, not edges

A use is a typed record whose class-ranged slot names the exact version used.
Relations stay structural.

- Failing test: none. C1 passes on today's Core.
- Identity: none in Core.
- R-05: this is the shape the read was built for. It reports these records as
  current referrers of the replaced version.
- UMR: `ResultApplication` in C1 is this shape. `CANDIDATE_REUSE` could be
  redesigned as a record naming the two passages. What the document graph
  loses: `query_relations` over it, and Core's check that an endpoint exists.
  A slot is not checked to resolve (P2g).
- Shop: already this shape (slots).
- Leaves: a structural reference held in a slot can dangle unseen.

### (iv) Restate with a declared marker (`restated_from`, `use_of`)

- `restated_from` duplicates what REVISION of the edge already records: the
  closing and `supersedes_record_id` (P2j).
- `use_of` puts an exact-version reference inside a relation whose endpoint
  says something else. A reader that follows the endpoint gets the new
  reading unless it knows to read the marker. That is two meanings on one
  relation type, which law 12 (`EXECUTOR_ONLY`) exists to prevent when the
  meaning is Core's. When it is adopter vocabulary, it is a trap for every
  reader.
- Dominated by (iii). Not recommended.

### (v) Anchor passage-level links on a stable passage identity

A passage record keyed by reading, block and span, not by the UMR hash. Each
annotation's sentence names it. Citation and candidate reuse name passages.
An annotation correction then never touches them.

- Identity: none in Core. This is adopter modelling.
- It removes the only block the UMR graphs meet (P2i) without restating
  anything.
- Not probed.

### (vi) Two small honesty changes in Core

- A typed refusal for R-04's category. When a supersession retires an endpoint
  of a live relation the change set does not restate, refuse with a reason
  that says so, instead of "does not exist". A name such as
  `INCIDENT_RELATION_NOT_RESTATED` would be honest: Core cannot tell use from
  structure, so it should not claim `HISTORICAL_USE_ENDPOINT`. Failing test:
  the P2e shape on a G3 contract expects the new reason; today it gives
  `STRUCTURAL_REFUSAL` and "Target entity 'r1' does not exist". Identity: none.
  Refusal reasons are appended enum members that no persisted artifact names
  (TEMP-012), and a refusal writes nothing.
- One more `VERSION_REFERRERS_NOT_COVERED` entry, for uses that reach the
  version only through containing structure (P2b). Core cannot know the
  direction of dependency across a relation without a declaration. Failing
  test: `not_covered` includes the new entry. Identity: none; it is a Python
  constant.

The two changes above are small. The convention ruling below is the part
that matters. Rule the carrier convention of section 6: relations are
structure, class-ranged slots name exact versions. Write it into
`CAPABILITIES.md` and the acolyte skill, so the next adopter picks its carrier
knowingly. Record the dangling structural slot (P2g) against the R-05 residual
with its reproducer. Declare a structural slot kind only when a consumer needs
one.

### Smallest and right

- For UMR now, smallest and right are the same: (iii) in the C4 form, with
  (v) when a genuine annotation correction comes.
- For Core, the smallest is (i), nothing. The right cut is (i) with (vi): two
  small changes that move no identity, plus the convention ruling. (ii) is the
  expensive one, and today it has no consumer.

## 8. Guidance for Luis

**UMR now.** Refine ± as an interpretation, not as an annotation revision.

1. Record the prior reading as an interpretation record: unspecified role,
   origin source wording, evidence the Y25 clause, linked to the annotation
   node by a class-ranged slot.
2. When R32 is admitted, revise that record: standard deviation over the
   Segment 3-S profile, origin reviewer inference, evidence a record for the
   R32 result.
3. Leave the annotation and `CANDIDATE_REUSE` as they are.
4. Change the readers deliberately, with tests.

- Cost: one additive contract revision; reader and test changes.
- Until `core/add-enum-revision` lands, new enum types are refused, so the
  role and origin are strings or values on existing enums.
- Unresolved: whether the reuse candidate is better supported is a separate
  review disposition (MARINE-03 I1). The application premises stay open.
  Nothing here says the RC2 transfer is valid.

**Core next.** Do not build the retired-endpoint change now.

1. Rule the carrier convention.
2. Build (vi) RED then GREEN: the typed refusal and the `not_covered` entry.
   No identity moves.
3. Put (ii) on the roadmap, gated on a consumer whose use must be a relation.

- Cost: two small tests and code changes, and one documentation change.
  The documentation change goes through the governed documentation ledger for
  `CAPABILITIES.md`.
- Unresolved: a structural reference held in a slot can still dangle (P2g),
  and the implicit rebinding in P2b stays undetected; after (vi) it is
  declared as not covered instead of silent.

Decisions to rule, one at a time:

1. Is the ± refinement an interpretation beside the annotation (C4), or a
   revision of the annotation (P2j)? Recommendation: C4.
2. The carrier convention: relations are structure, class-ranged slots name
   exact versions. Rule it, or reopen it? Recommendation: rule it.
3. Build (vi) now, and hold (ii) until a consumer needs it? Recommendation: yes.

## 9. Limits

- Two graphs. Both are authored annotations of one article. One refinement
  direction.
- P2i and P2j use mechanical stand-in bytes that only rename the ± concept.
  They test the mechanism, not a source-faithful correction.
- The supplement vocabulary is probe-only and typed more weakly than
  intended, because of the enum refusal. No UMR reader was changed. Every
  reader verdict is today's reader on the new shape.
- These histories run Core's structural builtin only. No Prolog rule layer ran,
  so `CUSTOM_POLICY_HISTORICAL_SCOPE` was not exercised.
- The Shop was inspected, not probed. The paper's marine graphs were not
  inspected. `REFINEMENT-SPEC-05.md` was not read.
- No full Core suite was run; only the 19 T3 tests, to confirm the Core used.
- Probe scripts live in the session scratchpad, identified by hash above, and
  are not in git.
