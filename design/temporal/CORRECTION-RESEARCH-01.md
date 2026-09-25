# Correction research 01: the general shape and the impact half

24 September 2026. Research for direction D-04 in [g4/RULINGS.md](g4/RULINGS.md).
Nothing here is ruled. Luis decides; section F holds the options.

Code base: branch `codex/core-temporal` at `b54a6f1c`. No `src/` file was changed.

Evidence tags:

| Tag | Meaning |
|---|---|
| CODE | Read in the file at the line given, at `b54a6f1c`. |
| PROBE | Ran through Core's public admission path in a temporary directory. The script and its full output are in the appendix. |
| DOC | Read in one of our own design or results documents, named at the claim. |
| LIT | Read in the primary source at the section given. |
| PROPOSAL | This document's proposal. No code ran. |

## Answer in brief

1. Today a correction can only be a supersession: a new record with a new id
   replaces one old record of the same operation type and record type. Its
   properties may differ in any way the contract allows, and a relation's
   endpoints may move. The record type cannot change, a record has at most one
   successor, and a timed record cannot be corrected for its own period. [CODE, PROBE]
2. Retiring a record that a live typed relation touches, at either end, is
   refused unless the same change set also supersedes that relation. A reference
   held in a string slot is not checked at all and dangles silently. [CODE, PROBE]
3. Core records dependencies upstream only: record fields to source locators,
   change sets to retained sources and evidence. The only reverse read is one hop
   over typed relations in the current graph. No read answers "what depends on
   this record or field". [CODE, PROBE]
4. Proposed shape: a correction is a change set of kind CORRECTION that names each
   target, gives each a successor version in which any field may differ, and is
   admitted only if the resulting state passes Core's checks. The first cut narrows
   by refusing results Core cannot yet reconcile, each with its own typed refusal
   and roadmap item. It does not narrow by listing permitted fields. [PROPOSAL]
5. The impact half needs one Core change before anything else: a retired version
   must stay a legal endpoint for relations that record historical use. Today the
   graph refuses that (`kg.py` 181 to 184), and restating the relation onto the
   successor would record a use that never happened. [CODE, PROBE, PROPOSAL]
6. Recomputation stays inside the ledger: Core finds and reports the affected set,
   a separate execution produces a result, and that result enters as an ordinary
   change set. Old results stay, bound to their old premises. Affected is not
   false. [DOC, PROPOSAL]

## A. Today's facts, from code

### What a supersession can change

| # | Fact | Evidence |
|---|---|---|
| A1 | There are four operation types, all creations: `CREATE_ENTITY`, `CREATE_EVENT`, `CREATE_EVENT_PARTICIPATION`, `CREATE_RELATION`. There is no update, delete or retract operation. Any other type raises "operation type is unsupported". | CODE `knowledge.py` 397 to 405 |
| A2 | Operation fields are closed. The only optional field is `supersedes_record_id`. Anything else raises "operation fields are not closed". | CODE `knowledge.py` 406 to 412 |
| A3 | A supersession creates a new record with a new id. Reusing an id refuses "record ID already exists in history". | CODE `knowledge.py` 3346 to 3350 |
| A4 | Properties may all change. Subject, value and an optional slot were changed or dropped in one supersession and admitted. | PROBE P4 |
| A5 | The successor must satisfy the contract. Dropping a required slot refuses "Required slot 'lexical' missing for Assertion". | PROBE P6 |
| A6 | A relation's endpoints may change: superseding relation `u1c` with one whose target is a different record was admitted. Nothing in `_apply_change` compares endpoints. | CODE `knowledge.py` 3340 to 3453; PROBE P5 |
| A7 | Record type and operation type cannot change: "record supersession type differs from prior record". The population path refuses the same case earlier as `SUPERSESSION_TYPE_MISMATCH`. | CODE `knowledge.py` 3370 to 3377, `population.py` 1300 to 1311; PROBE P3 |
| A8 | A record has at most one successor. A second correction of the same record refuses "record supersession forks prior record". | CODE `knowledge.py` 3365 to 3369; PROBE P7 |
| A9 | Valid time belongs to the change set, not to the record. The successor's valid-time kind must equal the prior's. For INSTANT the successor must start strictly later, so a correction of the same period is refused "record replacement contradicts prior valid time". | CODE `knowledge.py` 3378 to 3389; PROBE P9, Q1, Q2 |
| A10 | On supersession Core sets the prior record's `valid_to` to the change set's valid time and its `superseded_by`, and removes it from the current graph. It stays in `record_history`. | CODE `knowledge.py` 3390 to 3421; PROBE P2 |
| A11 | Ontology revisions are additive only. Removing or changing an existing semantic fact refuses `NON_ADDITIVE_CHANGE`. So no correction of a class definition, and no reclassification path through the ontology. | CODE `revision.py` 858 to 868 |
| A12 | The shipped state-version profile maps both correction and transition to `SUPERSEDE_STATE_VERSION` and declares retraction `NOT_ADMITTED`. | CODE `profiles/state-version.json` 2 to 7 |

### What blocks it

| # | Fact | Evidence |
|---|---|---|
| A13 | Retiring a record refuses if any non-retired relation has it as source or target: "Target entity 'a1' does not exist", "Source entity 'd1' does not exist". The docstring states the intent: "No dependent record may disappear as a side effect of node removal. Its explicit replacement must retire it in the same change set." | CODE `kg.py` 169 to 184; PROBE P1, P8; DOC g3 P-REL-SUPERSEDE |
| A14 | The same applies to an event participation's `event_id` and `entity_id`, and to a signal's `bearer_id`. | CODE `kg.py` 185 to 195 |
| A15 | Superseding the record and every incident relation in one change set, with the new relations pointing at the successor, is admitted. The earlier KG re-entry loop used exactly this pair replacement for its assessment and its connecting relation. | PROBE P2; DOC `research/kg_reentry_loop/RESULTS-01.md` |
| A16 | A relation endpoint must be an entity: "is not an Entity". A relation cannot point at a relation. | CODE `kg.py` 366 to 373 |
| A17 | A reference held in a string slot is not checked. After `a1` was retired, `d1.premise_refs` still named `a1`, and admission did not object. | PROBE P2 |

### What Core checks on the resulting state

| # | Fact | Evidence |
|---|---|---|
| A18 | Required checks run over the whole candidate state: the accepted graph with the retired records removed, plus the new writes. A Prolog rule therefore sees the corrected state everywhere, not only the changed records. | CODE `admission.py` 373 to 404 (`_check_base`), 586 to 588 (`stage_subgraph`) |
| A19 | Checks see only the current graph, not historical periods. A correction of a period a transition already closed would be checked against today's state only. This is the open question in CHECK-SCOPE-02, recommendation not ruled. | DOC `CHECK-SCOPE-02.md` lines 15 to 30, 80 to 100 |

### What dependency information Core records

| # | Kind | What it records | Direction | Evidence |
|---|---|---|---|---|
| A20 | Field derivation | For each record field (`path`), one retained `source_id` and `locator`. Every property and both relation endpoints must have one. | Record field to source. Never record to record. | CODE `population.py` 1321 to 1330, 1383 to 1399 |
| A21 | Change-set closure | Retained sources, evidence, and `supersedes` change ids. | Change set to retained inputs. | CODE `knowledge.py` 100 to 116, 3232 to 3254 |
| A22 | Operation `depends_on` | Order inside one change set. | Local to the change set. | CODE `knowledge.py` 451 to 490 |
| A23 | Typed relation | A source and target entity. | Both ends, current graph only. | CODE `kg.py` 570 to 606 |
| A24 | Check reads | Nothing. A check contract names its executor and outcomes; no field declares the classes and slots a rule reads. `RULE_DECLARES_ITS_READS` is adopted (2026-09-19) and not built. | None. | CODE `check_contract.py` 60, 85 to 92; DOC malleus-dev SKILL "Rules and the ontology" |
| A25 | Review boundary | `dependencies` and `affected_uses` as caller-declared references in the interpretation-review profile. Core checks coverage of a declared set; it discovers nothing. | Declared by the caller. | CODE `profiles/interpretation-review.json`; `acquisition.py` 150 to 160, 274 |

`trace_population_record` reads A20 upstream for one record and refuses on a
change set composed without a population plan (G3 probe P-TRACE). [CODE
`population.py` 2150 to 2217; DOC g3 RESULTS]

### Whether any reverse read exists

- `KnowledgeGraph.query_relations(target_id=...)` returns the relations that point
  at a record, one hop, over the current graph only. It returned `u1b` from `d1`
  for `a1b`. [CODE `kg.py` 710 to 725; PROBE P2]
- There is no transitive read, no reverse read over string slots, over field
  derivations, over check reads, or over retired versions.
- The only reverse index in the repository is in the Recon store:
  `relations_by_endpoint` and `records_by_evidence`, used to re-check records
  affected when an evidence attachment is retired. It lives in the Recon ledger,
  not in Core's knowledge history. It is a precedent for a replay-derived reverse
  index, nothing more. [CODE `recon/store.py` 83 to 128, 921 to 939]

## B. What a correction can target

Columns: what the correction changes; the specimen or flow it comes from; what it
disturbs; whether Core can express it today.

| Target | From | Disturbs | Today |
|---|---|---|---|
| Literal value | GE-04 B price 7.50 to 8; kg_reentry assessment | Calculations that used it (C01, RESULTS-03); rules reading the slot; nothing in the graph structure | Yes for NONE_STATED and ORDER_ONLY records. No for a timed record's own period (A9). |
| Unit or datatype, held as a slot | g1-08 lexical values | Same as a value, plus premise compatibility of every calculation that used it (G3 R8) | Yes, as a property change. A change of a slot's range is an ontology change and refuses (A11). |
| Valid-time start | g1-01 K3 corrects r1 | Neighbour periods; the target's successor link; every selection by domain time | No. Start is per change set; the kind cannot change (P9); the same start refuses (Q1). |
| Valid-time end, or "unstated" | g1-08, G3 R2 | Neighbour periods; applicability reads | No. There is no end field; G3 kept ends in an adopter slot. |
| A relation's endpoint | GE-03 application moved to a different subject | Reverse reads over the old and the new endpoint | Yes (A6). |
| A relation that should not exist | GE-10 withdrawal | Everything reached through it | No. Retraction is `NOT_ADMITTED` (A12) and no operation removes a record without a successor (A1). |
| Qualifier (uncertainty kind, scope) | Maintenance plan G4a | Numerical uses that read the qualifier | Yes, as a property change. |
| Record type or classification | An estimate that was really an application | Every rule and check keyed on type; every relation whose range names the type | No (A7). |
| An interpretation's basis (report, assumption, assessment) | GE-03 J1 to J2; GE-04 report versus assumption | Every argument and calculation citing it; its alternative justifications | Yes as a property change, if basis is a slot. The kg_reentry run did this. |
| Group membership | g1-05 CC05; maintenance plan §6 kind 3 | Any use that selected "all members" or "none present" | As a string list slot: yes, and unchecked. As relations: one supersession per relation. Absence claims are not findable either way. |
| Evidence link | Maintenance plan G3 citation resolution | Attribution and display uses; derivation trace | Record-level `evidence_refs` slot: yes. Change-set closure: fixed per change set; a correction brings its own. |
| Identity: two records are one thing, or one is two | Not in our specimens; it follows from R-02 | Every relation to either record | No. One `supersedes_record_id` per operation (A2), one successor per record (A8). |
| The ontology itself | ROADMAP F3 | All records of the type; all rules reading it | No (A11). |
| A calculation model | GE-05 M1 to M2 | Every execution under the old model | Yes, as new model records. RESULTS-04 did it with an additive revision. |

Pattern: what Core can already express is a property or endpoint change inside one
record type. What it cannot express is anything touching time extent, type,
identity, removal, or the ontology. None of the cannot rows is blocked by the
record shape; each is blocked by a specific check listed in A.

## C. The general correction shape

### Proposal

A correction is one change set of kind CORRECTION. [PROPOSAL]

1. It names every target record explicitly (R-01).
2. For each target it gives one successor version. The successor is its own
   identified record in the one KG (R-02). Any field may differ from the target:
   properties, endpoints, qualifiers, basis, and later type and time extent.
3. It cites its evidence, as every change set does today.
4. It records its kind, and the target's history records that it was closed by a
   correction at this ledger position (R-03). The target stays in the version
   graph.
5. Core admits it only if the resulting state passes Core's checks: the contract
   on every successor, every live reference resolving, temporal integrity of the
   periods involved, and every required check the policy names.
6. Core refuses a result it cannot yet reconcile with a refusal naming that
   category. It does not restrict which fields a correction may touch.

Point 6 is the whole difference from DECISION.md decision 4 as written. Decision 4
defined a correction as covering exactly its target's period. Under this shape,
"covers exactly its target's period" is the only valid-time outcome the first cut
supports. A correction that would change the period is refused as
`UNSUPPORTED_CORRECTION: VALID_TIME_EXTENT`, not ruled out of the design.

Later, point 2 gains a second form: a withdrawal, a target with no successor. It
is a separate record that names what it withdraws and why, the shape nanopublications
use (section E). It needs the retraction semantics the shipped profile refuses
today (A12), so it is not in the first cut.

### The first cut, as a strict subset

Supported: [PROPOSAL]

- One or more named targets of any entity or relation type.
- A same-type successor per target, with any properties and any endpoints.
- The successor covers exactly the target's period and inherits its successor link
  (DECISION.md item 4, the g1-01 K3 case), including a target already closed by a
  transition.
- Incident relations handled as today: the change set restates each one (A13, A15).
- Admission under Core's structural policy.

Refused in the first cut, each with its own reason and a roadmap item:

| Refusal | Why Core cannot reconcile it yet | Roadmap item |
|---|---|---|
| `TYPE_CHANGE` | Type decides which rules, ranges and checks apply; A7 refuses it and no rule says how relations typed against the old class survive. | Reclassification correction, with a rule for incident relations whose range names the old type. |
| `VALID_TIME_EXTENT` | No per-record valid time, no end, no splitting (A9, G3 R2). | T4 with R2: interval ends, splitting, overlap. |
| `WITHDRAWAL` | Retraction is `NOT_ADMITTED` in the shipped profile; no operation removes without replacement. | Withdrawal as its own record (GE-10), with its effect on the current graph. |
| `IDENTITY_MERGE_OR_SPLIT` | One successor per record and one target per operation (A2, A8). | Identity correction. |
| `HISTORICAL_USE_ENDPOINT` | A relation recording a past use would have to move onto the successor (A13). | The retired-endpoint change in section D. Prerequisite of the impact half. |
| `CUSTOM_POLICY_HISTORICAL_SCOPE` | Custom Prolog checks see the current graph only (A19). | CHECK-SCOPE-02 option 2: define each rule's historical scope. |
| `ONTOLOGY_FACT` | Revisions are additive only (A11). | F3. |

One refusal is permanent, not roadmap: a target that is not the latest version of
its line is stale (DECISION.md item 5). Today it shares the fork message with the
valid K3 correction (G3 RF-STALE-REVIEW); the cut gives it its own reason.

Why this is not a dead end: every later item removes one refusal row. None of
them changes the operation's shape, the kind field, or what "the resulting state
passes Core's checks" means. The alternative, one change kind per correctable
field, would add a kind each time, and each new kind moves the structural builtin
identity (G3 blast radius scenario C). [PROPOSAL, DOC g3 RESULTS]

## D. The impact half

### Three dependency kinds, mapped onto Malleus

From the maintenance plan §6. [DOC `handover/2026-09-23-knowledge-maintenance-plan.md`]

| Kind | Question | What Malleus has | What is missing |
|---|---|---|---|
| Representation | Which records and checks use a changed class, slot, range or enum? | The compiled revision diff (`revision.py` 841 to 900); records by type (`kg.py` `query`). | Declared rule reads (A24). This is F3 and F5, not correction. |
| Knowledge use | Which interpretations, arguments or calculations use a changed value, qualifier or basis? | Typed relations with a one-hop reverse read (A23). In research: `ChargeUseBinding` names the claim, the parameter and the field; `ActualChargeUse` links an execution to the claim it used (RESULTS-04). | Uses held as slots have no reverse read and no integrity (A17). Derivations never point record to record (A20). Retiring a used version is blocked (A13). |
| Membership or absence | Which uses depend on the set of matching records, or on none being present, in a declared scope? | Nothing. No selection or query scope is recorded. | A recorded scope: the selection rule and the ledger position it ran at. A new record can matter without touching any old one, so traversal from the changed record cannot find it. |

### What a deterministic "what depends on X" read needs recorded at admission

[PROPOSAL, built on the DOC and CODE rows above]

1. Every use is a typed record or relation naming the exact version it used, not a
   string slot. RESULTS-03 and RESULTS-04 already model this in research.
2. Field granularity where it matters: the use names the field it read, as
   `ChargeUseBinding` names `numeric_value`. Whole-record dependency is the honest
   default the maintenance plan allows.
3. Rule reads declared (`RULE_DECLARES_ITS_READS`), so a correction to slot S
   reaches every rule that reads S.
4. Selection scopes recorded as records, so a membership or absence use can be
   re-run at the new position and compared.
5. Record-to-record derivation, where one record was computed from others.

With those, the read is a reverse closure over recorded dependencies, computed from
the ledger at replay. That is an index derived inside Core, which R-02 allows; it
is not a second store. Its output is a set of affected records, each with the
dependency that reached it, plus an explicit coverage statement: which dependency
kinds were not recorded (slots, undeclared rules, unrecorded scopes). An empty
set with unrecorded kinds is "none found", never "none exist".

### How re-derivation stays inside the ledger

The sequence already proven in research is: model stored, model selected, executed,
result admitted, each a separate step; before admission the reader answers
"not computed", even when an equal value exists elsewhere. [DOC
`research/computational_graphs/RESULTS-03.md`, `RESULTS-04.md`]

Applied to a correction: [PROPOSAL]

1. The correction is admitted. Nothing downstream changes.
2. Core's impact read lists the affected uses. Each is flagged for
   reconsideration, not retracted. Affected is not false: another justification
   may still hold (GE-03 D2).
3. A consumer decides what to recompute. A recomputation is an execution against
   the new premise versions. Its result is a change set, admitted through
   `check_and_admit_change_set` like any other. This is the Semantic Re-entry
   pattern: a finding produces a proposal, never graph-writing authority.
4. The old result stays, bound to the old premises. A new result with an equal
   value is still a new execution with its own identity.
5. Nothing is silently rewritten. A review that ends in no change is recorded as
   such (the review-coverage profile's `NO_CHANGE`).

### The collision with the incoming-relation block

This is the load-bearing Core question for the impact half. [CODE, PROBE, PROPOSAL]

- A use must be a typed relation to the exact version used, or the reverse read
  cannot find it and Core cannot check it (A17, A23).
- When that version is corrected, Core refuses to retire it while the relation is
  live (A13, P1).
- The only admitted route is to restate the relation onto the successor (A15, P2).
  For a relation recording a past use, that writes something false: execution X1
  did not use the corrected value. G3 avoided this by keeping premise links as
  string slots, which gives up the reverse read and the integrity check.

So two kinds of incoming relation need different treatment:

- A structural relation, such as a line belonging to an order, follows the
  successor. The change set restates it, as today.
- A historical-use relation, such as an execution using a premise, stays on the
  version it used. The retired version must remain a legal endpoint in the version
  graph, while the current graph excludes it.

That second case needs `_without_records` (`kg.py` 169 to 204) to accept a live
relation into a retired record when the relation is declared historical, or the
graph to hold the version graph and the current view separately. Either is a Core
change. COMPARISON.md group 2 already parked it: "Deciding this is needed before
exact old use gets referential checks." The impact read cannot be built honestly
before it.

A16 is a second, smaller limit: a relation cannot point at a relation, so an
assessment of an application (g1-06 J1 on A1) is a slot, and the reverse read
cannot reach it.

## E. Literature, inherited not invented

Every row is `PROPOSED`. Classification per the promotion gate in the malleus-dev
skill.

| Source | Mechanism read | What transfers | What does not | Use |
|---|---|---|---|---|
| Mokhov, Mitchell, Peyton Jones, "Build Systems à la Carte", ICFP 2018. https://www.microsoft.com/en-us/research/wp-content/uploads/2018/03/build-systems.pdf, §2.1 Def. 2.1, §2.2, §2.3, §4.2.1, §4.2.2 | Minimality: execute tasks "only if they transitively depend on inputs that changed". Excel's static over-approximation: "safe for it to make more cells dirty than necessary, but not vice versa". Verifying traces record, at build time, the hashes of the dependencies actually used. Early cutoff stops propagation when a result is unchanged. | Record the exact version used at execution time: that is a verifying trace, and Malleus's premise bindings are one. The safe direction: an impact read may over-flag, never under-flag. Minimality is the measure to compare a selective read against full review, as the maintenance plan §6 asks. | A build system overwrites the stored value; Malleus keeps the old result. Early cutoff by equal value conflicts with RESULTS-03: equal values are not interchangeable. Cutoff can only mean "this use was reviewed and needs no further propagation", recorded as a review. | DESIGN_CONSTRAINT (record used versions; over-approximate); BASELINE_OR_ORACLE (minimality against full review) |
| Doyle, "A Truth Maintenance System", MIT AIM-521, 1979, https://dspace.mit.edu/handle/1721.1/5733. Read: the abstract, and de Kleer's description in §3.1 below. I did not read Doyle's full text. | Nodes are IN when some justification is valid; justifications are kept; beliefs are re-derived when support changes. | A use has one or more justifications; losing one does not remove the use if another holds (GE-03 D2). | A TMS flips belief automatically. Malleus flags and a review decides. | DESIGN_CONSTRAINT |
| de Kleer, "An Assumption-based TMS", Artificial Intelligence 28, 1986. https://www.dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf, §3.1, §4.3, §4.9 | Labels are sets of assumption sets, so contexts coexist. §4.9: to retract a justification, "the problem solver contradicts the conjoined assumption"; direct removal requires "invalidating the labels of all the consequents (recursively)" and "is a bad idea". | Retraction by adding a record, never by removal: the append-only ledger already does this. Context labels match GE-04: report, assumption and correction coexist as distinct premise sets. | Nogood databases and automatic inference. Malleus runs no general reasoner. | DESIGN_CONSTRAINT |
| W3C PROV-O, https://www.w3.org/TR/prov-o/, §4.2 Expanded Terms (via fetch summary) | `prov:wasRevisionOf`: a derived entity with substantial content of the original. `prov:wasInvalidatedBy`: the entity is "no longer usable". Invalidation is not falsity. | Vocabulary for exporting correction lineage and flagged uses. Supports "affected is not false". | No correction authority, no temporal eligibility, no statement that an executor was honest (GEDANKENEXPERIMENTS-01 already says so). | IMPLEMENTATION_CANDIDATE, for an export projection only |
| Budiu, Chajed, McSherry, Ryzhyk, Tannen, "DBSP: Automatic Incremental View Maintenance for Rich Query Languages", PVLDB 16(7), 2023. https://www.vldb.org/pvldb/vol16/p1601-budiu.pdf, §3 Def. 3.1, §4 | The incremental version of a query is `Q^Δ = D ∘ ↑Q ∘ I`. Z-sets are tables with integer weights, "possibly negative", so a change is a delta. | A correction is a delta on the current view: minus the target, plus the successor. The current graph is the integral of admitted deltas, which is already what replay computes. A reverse index or incremental read derived from replay fits R-02. Obligation: incremental result equals full recompute, which Core's replay equality already tests. | DBSP maintains query views automatically. Derived knowledge here (a calculation, an interpretation) needs an execution and an admission; that is not view maintenance. | IMPLEMENTATION_CANDIDATE (replay-derived reads, later); BASELINE_OR_ORACLE (incremental equals full) |
| Wikidata, Help:Ranking, https://www.wikidata.org/wiki/Help:Ranking, sections on deprecated rank and query use | Deprecated rank marks statements "known to include errors ... or that represent outdated knowledge". Not deleted. A qualifier, "reason for deprecated rank" (P2241), records why. Deprecated statements "will never be used unless that is specifically requested". | The pattern Core already has: the current graph excludes superseded records, `record_history` keeps them. Transfer the reason: a correction records why. | Wikidata changes a rank on the same statement in place. Malleus makes a new identified version. | DESIGN_CONSTRAINT (corroboration) |
| Kuhn et al., "Semantic micro-contributions with decentralized nanopublication services", PeerJ Computer Science 7:e387, 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC7959648, section "Identities and Updates" | Nanopublications are immutable. A new version declares `npx:supersedes`. A withdrawal without update is "a separate retraction nanopublication" with `npx:retracts`. Both valid only if signed with the same key. | Withdrawal as its own published record, not a deletion: the shape for the `WITHDRAWAL` roadmap item. | Key-based authority. Who may correct is adopter policy; integrity sits behind `MODULAR_INTEGRITY` (law 11). | DESIGN_CONSTRAINT (withdrawal shape); EXPLICIT_EXCLUSION (key authority in this cut) |

Differential dataflow is represented here through DBSP, which McSherry co-authored;
I did not read the differential dataflow paper separately.

## F. Options for Luis, one decision at a time

### Decision 1: the correction operation shape

- **(a) One general correction, checked on its result.** A change set of kind
  CORRECTION names its targets and gives each a successor in which any field may
  differ. Core checks the resulting state. The first cut refuses named result
  categories (section C table), each a roadmap item.
  Cost: one kind field, the same persisted-format routes as DECISION.md decision 6
  (route A on the branch, route C before integration); one typed refusal per
  unsupported category.
- **(b) One change kind per correctable thing.** VALUE_CORRECTION,
  ENDPOINT_CORRECTION, RECLASSIFY and so on, added as needed.
  Cost: every new kind is a new builtin version, which moves the check contract,
  structural policy, normative profile, history bundle and every ledger head
  (G3 scenario C). It also constrains by default, which D-04 rejects.

Recommendation: (a).

### Decision 2: does the first cut include the impact read?

- **(a) Correction only.** The cut states plainly that it computes no affected set.
  The impact half goes on the roadmap in the order below.
  Cost: none beyond decision 1.
- **(b) Correction plus a one-hop impact read over typed use relations.** Needs the
  retired-endpoint change (section D) first, because otherwise the use relations
  that the read would follow block the correction itself.
  Cost: a change to `kg.py` `_without_records` semantics or a split between the
  version graph and the current view, with its own RED tests; the relations must
  declare whether they are historical or structural.
- **(c) Correction plus the full declared-dependency read.** Needs rule reads
  declared, scopes recorded and record-to-record derivations.
  Cost: `RULE_DECLARES_ITS_READS` (one contract field, re-pinning every frozen
  coordinate, the OVR-000466 blast radius) and new record types for scopes.

Recommendation: (a) now, and rule that the retired-endpoint change is the next cut,
so (b) is planned, not discovered. Proposed roadmap order:

1. Retired versions stay legal endpoints for historical-use relations.
2. One-hop impact read over typed use relations, with its coverage statement.
3. Declared rule reads (`RULE_DECLARES_ITS_READS`), which also serves F3 and F5.
4. Recorded selection scopes for membership and absence uses.
5. Record-to-record derivations.
6. Then the section C refusals, in whatever order consumers need them.

### Decision 3: recomputation and the earlier "no automatic recompute" decision

The workstream README records an author decision: "Calculations consume identified
temporal premises; this work does not automatically recompute them." D-04 says a
correction "might need to query the kg for 'what things affect this specific
correction here' and go and recalculate/compute that part of the KG". These can
be read together or as an amendment. This document does not resolve that.

- **(a) Keep the earlier decision.** Core finds and reports. Recomputation is
  always a separately invoked execution whose result is admitted as a new change
  set. D-04's "go and recalculate" is met by Core producing the affected set, not
  by Core executing.
  Cost: none now; consumers do the execution step, as RESULTS-04 does.
- **(b) Core proposes recomputation for declared formal derivations.** Where a use
  is a declared model with bound premises, Core builds the recomputation request;
  its result still goes through admission, never auto-admitted.
  Cost: a Core computation contract that does not exist yet. The research
  consumer is one consumer, so by the promotion gate this waits for a second.
- **(c) Automatic recompute and admit.** Rejected by law 5 (stage first, commit
  only through the owning gate) and law 13 (no independent write path).

Recommendation: (a) for this workstream; (b) as a roadmap item gated on a second
calculation consumer. If Luis reads D-04 as amending the README decision toward
(b), the README line should be updated by his ruling, not by this document.

## Evidence limits

- The probes use one small contract, NONE_STATED and INSTANT only, and the
  structural policy. No Prolog check ran. A19 comes from code and CHECK-SCOPE-02,
  not from a probe.
- Section B's disturbance column is traced on paper against our specimens.
- The taxonomy comes from our specimens and flows. A domain we have not modelled
  could add a row.
- PROV-O was read through a fetch summary, not by reading the page myself line by
  line. Doyle was read through its abstract and de Kleer's description.

## Appendix: probe

Run from a temporary directory with
`PYTHONPATH=$PWD/src:$PWD /Users/luis/Projects/malleus-dev/.venv/bin/python probe.py`
from the worktree root, with `contract.yaml` beside the script.

`contract.yaml`:

```yaml
id: https://example.malleus.dev/correction-probe
name: correction_probe
prefixes:
  linkml: https://w3id.org/linkml/
  malleus: https://malleus.dev/schema/
imports:
  - linkml:types
  - malleus
slots:
  label: {range: string, required: true}
  subject: {range: string, required: true}
  lexical: {range: string, required: true}
  unit: {range: string}
  premise_refs: {range: string, multivalued: true}
classes:
  Subject:
    is_a: Entity
    slots: [label]
  Assertion:
    is_a: Entity
    slots: [subject, lexical, unit]
  Argument:
    is_a: Entity
    slots: [label, premise_refs]
  UsesPremise:
    is_a: Relation
```

`probe.py`, the operative part (helpers: each attempt retains one source and one
evidence anchor, composes with `compose_change_set`, admits with
`check_and_admit_change_set`, and compares ledger bytes on refusal):

```python
seed: s1 Subject; a1, a2 Assertion; d1 Argument(premise_refs=[a1]); u1 UsesPremise d1->a1
P1: a1b supersedes a1, alone
P2: a1b supersedes a1, and u1b (d1->a1b) supersedes u1
P3: a1c of type Subject supersedes a1b (with u1c)
P4: a1c supersedes a1b, subject s9, lexical 8.10, unit dropped (with u1c)
P5: u1d (d1->a2) supersedes u1c
P6: a1d supersedes a1c without required lexical
P7: a1x supersedes a1 a second time
P8: d1b supersedes d1, source of live u1d
P9: a2b INSTANT supersedes a2 NONE_STATED (with u1e)
Q0: r1 INSTANT 2026-05-01;  Q1: r3 supersedes r1 at 2026-05-01;  Q2: r2 supersedes r1 at 2026-05-12
```

Output, verbatim:

```text
P0 seed: ADMITTED
P1 supersede a1 alone, typed relation u1 points at it: REFUSED CHECK STRUCTURAL_REFUSAL: Cannot rehydrate graph from records: relations[0] 'u1': Target entity 'a1' does not exist (ledger unchanged: True)
P2 supersede a1 and u1 together, u1b points at a1b: ADMITTED
P2 current graph ids: ['a1b', 'a2', 'd1', 's1']
P2 reverse read query_relations(target_id=a1b): [('u1b', 'd1')]
P2 d1.premise_refs still names retired a1 (string slot, unchecked): ['a1']
P2 record_history a1: {'superseded_by': 'a1b', 'valid_to': "KnowledgeValidTime(kind='NONE_STATED', value=None)"}
P3 supersede a1b with a different record type: REFUSED CHECK CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: record supersession type differs from prior record: a1b (ledger unchanged: True)
P4 supersede a1b changing subject, lexical and dropping unit: ADMITTED
P5 supersede relation u1c, moving its target to a2: ADMITTED
P6 supersede a1c omitting required lexical: REFUSED CHECK CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: Required slot 'lexical' missing for Assertion (ledger unchanged: True)
P7 second correction of already-superseded a1: REFUSED CHECK CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: record supersession forks prior record: a1 (ledger unchanged: True)
P8 supersede d1, the source of live relation u1d: REFUSED CHECK STRUCTURAL_REFUSAL: Cannot rehydrate graph from records: relations[0] 'u1d': Source entity 'd1' does not exist (ledger unchanged: True)
P9 supersede a2 with INSTANT valid time (prior NONE_STATED): REFUSED CHECK CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: record replacement valid-time kind differs from prior record: a2 (ledger unchanged: True)
Q0 seed timed: ADMITTED
Q1 same-start correction of r1 (INSTANT 1 May): REFUSED CHECK CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: record replacement contradicts prior valid time: r1 (ledger unchanged: True)
Q2 later-start replacement of r1 (INSTANT 12 May): ADMITTED
```

Every refusal left the ledger byte-identical. The full script was not committed;
this document is the only file this research writes.
