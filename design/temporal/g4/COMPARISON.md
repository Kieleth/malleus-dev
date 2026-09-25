# G4 comparison: what G1 to G3 established

24 September 2026. Gate G4 of [GEDANKENEXPERIMENTS-01.md](../GEDANKENEXPERIMENTS-01.md).
This file holds the full comparison. [DECISION.md](DECISION.md) is the memo built
from it. Nothing here changes a specimen, a witness or `src/`.

Role: research analysis under the proposed `OPTIONAL_PROFILE` for temporal semantic
history. No `PROTOCOL_INVARIANT` is proposed here; where a witness proposed one, it is
quoted as a proposal.

## Evidence levels used

| Tag | Meaning here |
|---|---|
| INSPECTED | Read in a file or in code at tip 903a1a1c. |
| TRACE | Worked on paper against the specimen objects. No code ran. |
| STORAGE | Observed by a storage witness (G2a graph records, G2b SQLite). Proves these finite cases in that encoding only. |
| CORE | Observed by G3 through Core's public admission path. |

Re-run at 903a1a1c, per directory: g1 9 passed, g2a 38 passed, g2b 40 passed, g3 213
passed. G2a runner: 0 problems. G2b runner, JSON mode, captured for the table below.
Two encoders agreeing proves the meaning is determinate under the specimen. It does
not prove the meaning is right.

## 1. Cross-witness table

Columns: G2a and G2b give the witness status for the query, over every branch they
ran. G3 gives Core's class from `g3/expected_today.py`. Reading:

- **SETTLED**: G2a and G2b both give the specimen's answer. The meaning is
  determinate and representable under this specimen.
- **SETTLED, JUDGED**: both agree, but only because each supplied a rule the specimen
  does not state. The rule is named in section 3.
- **UNDEFINED**: the encoders disagree, or one needed an input the specimen does not
  hold. What is missing is named.
- **CORE AGREES**: G3 answered correctly. A caveat names any encoding workaround it
  depended on.
- **CORE GAP Rn**: G3 answered wrong or could not express it. Rn is G3's request
  number (section "Minimal Core request list" of `g3/RESULTS.md`). "adopter" means
  G3 classed it as adopter work, not a Core request.

### Queries

| Specimen | Query | Kind | G2a | G2b | G3 | Reading |
|---|---|---|---|---|---|---|
| g1-01 | P01 to P10 | SELECT_APPLICABLE | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R3 (no domain-time read). P05, P10 also need r3's end, which G3 kept only in an adopter slot: R2, or the correction-period rule in section 4 item 3. |
| g1-01 | PH-K0, PH-K1 | INSPECT_HISTORY | PASS | PASS | CORRECT | SETTLED. CORE AGREES. |
| g1-01 | PH-K2 | INSPECT_HISTORY | PASS | PASS | WRONG | SETTLED. CORE GAP R1: `a2.knowledge_until` K2, expected null. `visible_refs` and `a1.knowledge_until` not expressible: R4. |
| g1-01 | PH-K3 | INSPECT_HISTORY | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R4. Reached only after G3 re-admitted r3 as a plain addition (encoding choice 5). |
| g1-01 | PH-K3-META | INSPECT_HISTORY | PASS | PASS | WRONG | SETTLED. CORE GAP R1: `a2.knowledge_until` K2, expected K3. Plus R4. |
| g1-01 | PX-r1-K3 | EXACT_LOOKUP | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Caveat: the stated open end is read from the change set's valid time; Core's `valid_to` would give the forbidden answer. |
| g1-01 | C01 | EXPLAIN_EXECUTION | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Caveat: the premise link is a string slot. A typed relation to r1 blocks r1's supersession (probe P-REL-SUPERSEDE). |
| g1-01 | C02, PC-NOT-COMPUTED | COMPARE_PREMISES, RESULT_FOR_SELECTION | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R3. |
| g1-01 | C05 | PREPARE_INPUTS | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R8. |
| g1-02 | OQ01 to OQ05, OQ11 to OQ13 | RESULT_FOR_CONTEXT | PASS | PASS | CORRECT | SETTLED. CORE AGREES. |
| g1-02 | OQ06 | COMPARE_PREMISES | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Weak: an identity comparison of two ids (G2b F10). |
| g1-02 | OQ07 | EXPLAIN_EXECUTION | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Same slot caveat as C01. |
| g1-02 | OQ08 | SELECT_APPLICABLE | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R3. |
| g1-02 | OQ09, OQ10 | SELECT_ACCOUNT | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Works because a NONE_STATED supersession skips Core's later-instant check. |
| g1-02 | OQ14 | INSPECT_HISTORY | PASS | PASS | CORRECT | SETTLED. CORE AGREES. |
| g1-03 | CA01 to CA04, CA07, CA10 | SELECT_APPLICABLE | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R3. |
| g1-03 | CA05 (both branches) | SELECT_APPLICABLE | PASS | PASS | NOT_EXPRESSIBLE | SETTLED per branch. CORE GAP R3. |
| g1-03 | CA06 | COMPARE_PREMISES | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Weak, as OQ06. |
| g1-03 | CA08 branch 1 | SELECT_APPLICABLE | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R3. |
| g1-03 | CA08 branch 2 | SELECT_APPLICABLE | SPECIMEN_ISSUE | PASS | NOT_EXPRESSIBLE | UNDEFINED. No authority record exists and the format has no type for one. G2b passed only by injecting `ctx:flood-model` as a runner parameter (F3). |
| g1-03 | CA09 | INSPECT_HISTORY | PASS | PASS | CORRECT | SETTLED at assertion grain (see defect D13). CORE AGREES. |
| g1-04 | S01 to S03 | SELECT_APPLICABLE | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R3. |
| g1-04 | S04, SQ-ACCOUNT-M1, SQ-ACCOUNT-M2, SQ-EXACT-m1 | various | PASS | PASS | CORRECT | SETTLED. CORE AGREES. |
| g1-04 | C06 | PREPARE_INPUTS | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R8. |
| g1-05 | CC01, CC02 | EXACT_LOOKUP | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Membership is a string list slot in G3. |
| g1-05 | CC03, CC04 | RESULT_FOR_SELECTION | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Weak: no execution exists at all (G2b F10). |
| g1-05 | CC05, CC07 | PREPARE_INPUTS | PASS | PASS | NOT_EXPRESSIBLE | SETTLED, JUDGED: coherence checks and their order are each witness's own (D12). CORE GAP R8. |
| g1-05 | CC06 | PREPARE_INPUTS | PASS | PASS | NOT_EXPRESSIBLE | SETTLED, JUDGED: no parameter mapping exists, so INPUTS_READY is reached without checking that `h2o_content` feeds `h2o_wt_percent` (D11). CORE GAP R8. |
| g1-06 | AJ01 to AJ05, AJ08 | EXACT_LOOKUP, SELECT_ACCOUNT | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Caveat: J1's subject A1 is a string slot; Core's graph refuses a relation whose endpoint is a relation (`kg.py`, "is not an Entity"). |
| g1-06 | AJ06 | INSPECT_HISTORY | PASS | PASS, SPECIMEN_ISSUE under OC-06-FLAG-SOURCE branch 2 | NOT_EXPRESSIBLE | UNDEFINED. G2a passes by adopting a rule the specimen does not state (the review unit is the conclusion). G2b, without that rule, returns NOT_RECORDED under branch 2. Missing: the review unit. G3: adopter. |
| g1-06 | AJ07 (both branches) | INSPECT_HISTORY | PASS | PASS | NOT_EXPRESSIBLE | SETTLED per branch. G3: adopter. |
| g1-06 | AJ09 (both branches) | SELECT_ACCOUNT | PASS | PASS | NOT_EXPRESSIBLE | SETTLED per branch. G3: adopter. |
| g1-07 | VQ01, VQ11 | SELECT_APPLICABLE | PASS | PASS | NOT_EXPRESSIBLE | SETTLED. CORE GAP R3. |
| g1-07 | VQ03 to VQ10 | SELECT_APPLICABLE | PASS | PASS | NOT_EXPRESSIBLE | SETTLED, JUDGED: both witnesses hard-code the `event` to `state` link and OPENED to OPEN, CLOSED to CLOSED from the rule's prose (D9). CORE GAP R3. |
| g1-07 | VQ02, VQ12 | INSPECT_HISTORY | PASS | PASS | CORRECT | SETTLED. CORE AGREES. |
| g1-07 | VQ13 | INSPECT_HISTORY | PASS | PASS | CORRECT | SETTLED, JUDGED: `plan` is not a property of a PLAN object; both witnesses map it (D9). CORE AGREES. |
| g1-08 | ST01 | EXACT_LOOKUP | PASS | PASS | CORRECT | SETTLED. CORE AGREES. Caveat: 5.40 kept only because G3 stores values as strings; `decimal` does not compile (R7). The open end is kept in an adopter slot (R2). |
| g1-08 | ST02, ST04 to ST06 | EXACT_LOOKUP | PASS | PASS | CORRECT | SETTLED. CORE AGREES. |
| g1-08 | ST03 | EXACT_LOOKUP | PASS | PASS | CORRECT | SETTLED. CORE AGREES only because G3 split R2 into two change sets; one change set gives ST03's forbidden answer (probe P-R2-ONE-CHANGE). R2. |
| g1-08 | ST07 | EXPLAIN_EXECUTION | PASS | PASS | CORRECT | SETTLED. CORE AGREES. |
| g1-08 | ST08, ST09, ST10 | EXPLAIN_EXECUTION, EXACT_LOOKUP | PASS | PASS | NOT_EXPRESSIBLE | SETTLED, JUDGED: what a withheld artifact leaves behind is each witness's own (D10). CORE GAP R5. |
| g1-08 | ST11 (both branches) | EXPLAIN_EXECUTION | PASS | PASS | NOT_EXPRESSIBLE | SETTLED per branch. CORE GAP R5. |
| g1-08 | ST12, ST13 | INSPECT_HISTORY, EXACT_LOOKUP | PASS | PASS | CORRECT | SETTLED. CORE AGREES. ST13 is weak (G2b F10). |

Totals over 100 answers (94 queries, six with two branches). G2a: 99 PASS, 1
SPECIMEN_ISSUE (CA08 branch 2). G2b counts 169 runs because it reran unaffected
queries under every branch combination. Each of the 100 authored answers passed in
G2b's run of its own branch; its two SPECIMEN_ISSUE runs are AJ06 under a branch of a
choice that does not list AJ06. G3: 45
CORRECT, 2 WRONG, 53 NOT_EXPRESSIBLE. Every G3 WRONG and NOT_EXPRESSIBLE answer is a
query both encoders settled, except CA08 branch 2 and AJ06, which the encoders
themselves left undefined. [STORAGE, CORE]

### Refusals

| Specimen | Refusal | Expected | G2a | G2b | G3 | Reading |
|---|---|---|---|---|---|---|
| g1-01 | RF-STALE-BASE | STALE_BASE | STALE_BASE | STALE_BASE (also detects UNSUPPORTED_SEMANTICS, MISSING_EVIDENCE) | OBSERVED: supersession refused as a fork, then plain addition refused STALE_BASE at ADMIT | SETTLED, JUDGED on precedence (D5). CORE AGREES. |
| g1-01 | RF-OVERLAP | UNSUPPORTED_SEMANTICS | UNKNOWN_REFERENCE (SPECIMEN_ISSUE) | UNSUPPORTED_SEMANTICS by its own precedence; MISSING_EVIDENCE also detected | NOT OBSERVED: fork refusal as for the valid r3, then plain addition admitted | UNDEFINED: the attempt cites `src:r3`, not accepted at K2 (D2), and precedence is unstated (D5). The dangling evidence reference is UNKNOWN_REFERENCE in G2a and MISSING_EVIDENCE in G2b (D15). CORE GAP R1, and an interval end (R2) before overlap can be judged. |
| g1-02 | RF-STALE-EXEC | STALE_BASE | STALE_BASE | STALE_BASE | OBSERVED at ADMIT | SETTLED. CORE AGREES. |
| g1-02 | RF-BORROWED | PREMISE_MISMATCH | PREMISE_MISMATCH | PREMISE_MISMATCH | NOT OBSERVED: admitted | SETTLED. CORE GAP. G3 classes it as probably catchable by an adopter Prolog rule; not built, so unverified. Close to R8. |
| g1-05 | RF-CITED-MODEL | MISSING_MODEL | MISSING_MODEL | MISSING_MODEL | OBSERVED through a typed relation's range check; the same link as a slot is admitted | SETTLED. CORE AGREES when the link is a typed relation. |
| g1-06 | RF-STALE-REVIEW | STALE_TARGET | STALE_TARGET | STALE_TARGET | OBSERVED as STALE_BASE. Composed fresh at J4p: fork refusal, then the harness's plain-addition fallback was admitted | SETTLED, JUDGED: the two witnesses define STALE_TARGET differently (D6). Core's fork refusal is the stale-target signal, but it is identical to the refusal of the valid g1-01 K3 correction. CORE GAP R1. |
| g1-07 | RF-NO-EVIDENCE | MISSING_EVIDENCE | MISSING_EVIDENCE | MISSING_EVIDENCE | OBSERVED only through an `exactly_one_of` construct | SETTLED. CORE AGREES with a workaround: R6. |
| g1-08 | RF-PARTIAL | UNKNOWN_REFERENCE | UNKNOWN_REFERENCE | UNKNOWN_REFERENCE | OBSERVED | SETTLED. CORE AGREES. |
| g1-08 | RF-MISSING-MODEL | MISSING_MODEL | MISSING_MODEL | MISSING_MODEL | OBSERVED through a typed relation | SETTLED. CORE AGREES when typed. |
| g1-08 | RF-MISSING-EVIDENCE | MISSING_EVIDENCE | MISSING_EVIDENCE | MISSING_EVIDENCE | OBSERVED only through `exactly_one_of` | SETTLED. CORE AGREES with a workaround: R6. |
| g1-08 | RF-UNSUPPORTED | UNSUPPORTED_SEMANTICS | UNSUPPORTED_SEMANTICS | UNSUPPORTED_SEMANTICS | OBSERVED at COMPOSE | SETTLED. CORE AGREES. |
| g1-08 | RF-MISSING-CONTRACT | MISSING_CONTRACT | MISSING_CONTRACT | MISSING_CONTRACT | OBSERVED as STALE_BASE "different effective contract"; a contract named only in a slot is admitted | SETTLED. CORE AGREES in outcome, not in category. |

All three witnesses left bytes unchanged on every refusal they made. For G2a and G2b
that is a rollback of their own store, not Core atomicity. For G3 it is Core's
ledger. [STORAGE, CORE]

### What the table says

1. The encoders never disagree on a determinate answer. They split only on CA08
   branch 2, AJ06 and RF-OVERLAP, and each split traces to something the specimen
   does not hold. [STORAGE]
2. Every Core gap lands on five requests, R1 (correction versus transition), R3
   (domain-time read), R4 (version listing), R5 (withheld artifacts) and R8
   (premise compatibility), except three g1-06 queries (five answers) G3 classed as
   adopter work, and RF-BORROWED. R2, R6 and R7 appear only as workarounds behind
   rows Core got right. Of the 55 answers Core did not get right, 37 need R3. [CORE]
3. Several of Core's correct answers depend on keeping references as string slots.
   Two Core constraints force that, and G3 did not list either as a request:
   a typed relation into a record blocks that record's supersession
   (`KnowledgeGraph._without_records`, `kg.py` lines 181 to 184, probe
   P-REL-SUPERSEDE), and a relation endpoint must be an entity (`kg.py` line 373).
   With slots, Core checks no referential integrity for premises, members or
   assessed subjects. [INSPECTED, CORE]

## 2. Construction C on paper

**Evidence level: TRACE.** No native temporal database was installed or run. Each
point below walks the specimen objects against STORAGE-FLOWS-01's six adapter
conditions for a store whose native key is (subject, property, valid time,
transaction time) and which updates a cell by writing a new valid-time extent at a
new transaction time, as XTDB's documentation describes.

### Where C is strong

g1-01's selection answers fall out of the native model if the K2 transition is
written as 800 from 12 May and the K3 correction as 775 for [1 May, 12 May). The
bitemporal rectangles are then exactly a1, a2, b and c, with a1 ending K2 and a2
ending K3 on the transaction axis. P01 to P10, PH-K1, PH-K2 and PH-K3-META come out
right by construction. These are the answers Core gets wrong or cannot express (R1,
R3, R4). [TRACE]

### Where the four coordinates are not enough

| Distinction | Queries that need it | Why (subject, property, valid time, transaction time) fails |
|---|---|---|
| Account | CA01, CA02, CA03, CA05, CA08, CA10, OQ09, OQ10 | Q1 and Q2 share subject, property and period. Written at A1 and A2, Q2 becomes the next version of Q1's cell, so CA01 at A2 returns 42, not 40, and CA03 cannot be ambiguous. In g1-02, H1 (O4) becomes a version of B1's cell, so OQ10 at O5 returns 800 from the assumption instead of B1. |
| Basis | CA04, CA09, OQ14 | H1 and Q2 have the same value and time; only basis tells assumption from report. |
| Exact assertion as stated, apart from its resolved cells | PX-r1-K3, C01, OQ07, ST07, AJ05 | PX-r1-K3 expects r1 with its stated open end. The native store holds only resolved rectangles; the report as stated is gone once K2 splits it. C01 needs a handle to a1 that survives the split (condition 3). |
| Equal value, distinct premise | OQ06, CA06 | Two writes of 800 for line B with no stated time are one cell in two versions, not two premises (G2b's control shows the same merge in SQL). |
| Unstated time | S02, S03, OQ08, C06, ST01, ST03 | A native valid time defaults to transaction time or to an unbounded range. The first dates m1 by its arrival; the second makes it hold on every date, which is S02's forbidden reading (condition 2). NONE_STATED has to live outside the valid-time axis, and the selector must read it. |
| Group and model membership | CC01, CC02, CC05, CC07, ST05, ST06 | Membership is a set of records, not a property value over time. |
| Assessment of a relation | AJ02 to AJ05 | J1's subject is the relation A1. The store needs addressable edge identity. |
| Declared change kind | RF-OVERLAP, RF-STALE-REVIEW, PH-K2 | A transition and a correction are both writes of a valid-time extent. The store records neither kind, so the declared kind must be kept outside it. An overlapping correction is simply accepted; refusing it is admission's job (condition 5). |
| Derived state | VQ03 to VQ10 | State is derived by a declared rule at read time. Writing it as a stored interval bakes the rule into storage and breaks VQ03, which expects no state without a rule. |

Every specimen has at least one query in this table. [TRACE]

### The six conditions against the specimens

1. **Native transaction positions to ledger checkpoints.** Every query takes a
   position label (K1a, O5, J3p). The adapter needs a table from ledger checkpoint
   to native transaction. The stale-base refusals are ledger checks, not store
   checks. Not met by any native store by default. [TRACE]
2. **Unstated time, uncertainty, known-open periods.** Needs NONE_STATED outside
   the valid axis (g1-04, g1-02, g1-08). `until: null` (known open) and NONE_STATED
   must stay apart through round trip (ST01, ST03). [TRACE]
3. **Exact version references that survive later corrections.** C01 must reach a1
   after K2 and K3 split r1's rectangle. A handle keyed on valid-to changes at K2.
   The handle has to be the assertion id plus the selection coordinates, as in both
   witnesses. [TRACE]
4. **Explicit account precedence.** Native overwrite order would make Q2 win over
   Q1 by arrival. Needs account in the key or the document (g1-03). [TRACE]
5. **Full history and selected views, with evidence and model scope, no second
   admission authority.** Evidence links, group membership and the declared change
   kind live outside the temporal key. RF-OVERLAP must be refused before the write
   reaches the store. [TRACE]
6. **Rebuild from the ledger to the same logical answers.** Both witnesses rebuilt
   from the change list alone. A native adapter owes the same, with its derived
   rectangles as a cache. Not assessed further on paper. [TRACE]

Conclusion on paper: a native temporal store would have to carry assertion
identity, account, basis, NONE_STATED, membership and the declared change kind in its
documents, which are the identified records of Construction A. It could serve as an
index for g1-01-shaped selection under A. It does not replace A. This is a paper
assessment of eight small specimens, not a measurement.

## 3. Specimen defects and judgements made with the answers in view

Proposed fixes are text only. None is applied.

| # | Defect or judgement | Where found | Proposed fix to specimen or format |
|---|---|---|---|
| D1 | CA08 branch 2 expects SELECTED Q2 from "an adopter-declared default authority". No such record exists and the format has no type for one. Its own note says J1 is not that record. | G2a finding; G2b F3 | Add an object type for a declared authority (for example `AUTHORITY` with `scope_refs` and `account_ref`) and a change A5 that accepts one, then re-author CA08 branch 2 at A5. Or mark the branch answer as conditional on a record that does not exist and drop it from the pass count. |
| D2 | RF-OVERLAP cites `src:r3`, accepted only at K3; the attempt is at K2. Two causes for one refusal. | G2a finding; G2b F2 | Let an attempt carry new sources: add a rejected SOURCE `src:r3-overlap` to `would_add_refs`. Have the validator check that every reference in a rejected object resolves at `head` or inside the attempt. |
| D3 | RF-STALE-BASE has the same dangling `src:r3`, masked because staleness is checked first. | G2a finding; G2b F2 | Same fix as D2 (`src:r3-stale`). |
| D4 | AJ06 is not listed as affected by OC-06-FLAG-SOURCE, but its answer depends on it under branch 2. G2a passed by choosing a review unit (the conclusion); G2b did not. | G2b F1; G2a assumption 2 | Either add AJ06 to the choice's `affects_query_refs` with per-branch answers, or state the rule in branch 2: NOT_REQUIRED while no premise of any argument for the conclusion has changed, NOT_RECORDED once one has. |
| D5 | Refusal precedence. Several attempts violate more than one check and the format names one category. Both witnesses chose an order with the expected categories in view. | G2a assumption 1; G2b F6 | State the precedence in SCHEMA.md, or let `category` be the set of violated categories and let a witness pass by reporting any member. The first is a policy decision (section 4); the second removes the need for it in fixtures. |
| D6 | STALE_TARGET is undefined. G2a: a target already revised or corrected at the head. G2b: a target with no open applicability version at the head. Both separate RF-STALE-REVIEW from RF-STALE-BASE; a third definition ("a later change named the same target") would not. | G2a assumption 1; G2b F6 | Define it in SCHEMA.md. The G2a wording is closer to the declared-kind rule: a target already corrected or revised at the head is stale; a target closed by a transition is not. |
| D7 | Refusal attempts carry no change kind. G2b inferred one from the rejected objects, against "the kind is declared input, never inferred". | G2b F4 | Add `kind` to every refusal entry. |
| D8 | Accepted changes carry no base. Both witnesses assume the preceding head. | G2b F7 | Add `base` to every change, or state in SCHEMA.md that an accepted change's base is the preceding position. |
| D9 | g1-07's rule is prose. The link from `event` to `state`, the mapping OPENED to OPEN and CLOSED to CLOSED, and the `plan` pseudo-property in VQ13 are not declared. Both witnesses hard-coded them. | G2a assumptions 3, 4; G2b F5 | Give RULE structured fields: `event_property`, `state_property`, `transitions` (event value to state value), `scope_refs`. Give PLAN a `property` field or answer VQ13 with a PLAN-specific query kind. |
| D10 | A withheld artifact's remainder is unspecified. G2b keeps id and type and drops payload, for SOURCE, MODEL and CONTRACT only. | G2b F8 | State in SCHEMA.md what survives withholding and which object types may be withheld. |
| D11 | CC06 returns INPUTS_READY although no mapping says `h2o_content` feeds `h2o_wt_percent`. | G2a assumption 6 | Give MODEL parameters an explicit `property` or `assertion_property` mapping, and make CC06 fail if the mapping is missing. |
| D12 | PREPARE_INPUTS coherence rules and their order are each witness's own (unit and datum comparability, group membership, when group membership is checked). | G2a assumption 6 and "coherent conditions"; G2b F9 | State the checks and their order in SCHEMA.md, or give each check its own query so order does not matter. |
| D13 | Only g1-01 names derived versions. CA09 and ST12 list assertions although their intervals have versions, so those specimens compare at assertion grain. | G2a "rendering versions" | State in SCHEMA.md that INSPECT_HISTORY answers at assertion grain unless the file declares derived labels. |
| D14 | Some passes discriminate little: OQ06 and CA06 compare two ids; CC03 and CC04 pass with no execution at all; ST13 reads a record no refusal touched. | G2b F10 | Add a forbidden answer to OQ06 and CA06 that a (subject, property, value, time) key would give. Add a positive control where an execution does exist for CC04's model under another subject. |
| D15 | A reference to a source not yet accepted is UNKNOWN_REFERENCE in G2a and MISSING_EVIDENCE in G2b. | RF-OVERLAP rows | Say in SCHEMA.md which category an unresolved `evidence_refs` entry gets. |
| D16 | Computation, comparison and preparation queries do not check closure in G2a; no specimen withholds a record from them. | G2a assumption 8 | Add one withheld case on a RESULT_FOR_CONTEXT or PREPARE_INPUTS query. |
| D17 | Twelve accepted changes cite no source (K1a, K1b, O2, O3, O5, O7, O9, O10, G3, V2, R3, R4). Core requires a nonempty source closure; G3 invented `decl:<position>` sources. g1-08 R1 declares a contract as a change; Core binds the contract at history creation. | G3 encoding choices 4 and 6 | State in SCHEMA.md that a declaration change may cite a retained declaration of its own objects, and that a contract declared at genesis is a legal encoding of R1. |
| D18 | The cell `basis` lists in the reused answer key are not computed by either witness. | G2b "Derived labels" | None needed for G4; note it so a later witness does not read their absence as a pass. |

## 4. Open choices, triaged

Three groups. Group 1 is ordered by dependency, so Luis can take one at a time.

### Group 1: needed before a first Core cut on correction versus transition

1. **How a transition and a correction name their target** (G1 OC-01). Options:
   the change names its target; or closure is inferred from account and start
   time. No G1 answer depends on it; it matters once two open reports share an
   account. Core's supersession already names its target. Recommendation: the
   change names it; nothing is inferred. [INSPECTED]
2. **What a transition does to the prior version** (G3 R1 option a). Today Core
   sets the prior record's `valid_to` to the successor's start, sets
   `superseded_by`, and drops it from the current graph
   (`knowledge.py`, `_apply_change`). The valid-time half is already right: at K2,
   r1 carries 1 May to 12 May, which is a2. What is missing is a record that r1 is
   still believed. Options: (a) record the closing kind with the closure, so a
   transition closes valid time and leaves the knowledge period open; (b) leave the
   prior record in the current graph as well. Option (b) contradicts the shipped
   state-version profile's `CURRENT_NON_SUPERSEDED_RECORDS` projection rule;
   option (a) does not. Recommendation: (a). [INSPECTED, CORE]
3. **What a correction may target and what period it covers** (G3 R1 option b,
   G2a assumption 7, RF-OVERLAP). Options: (a) a correction may target a record
   already closed by a transition, covers exactly that record's current period,
   inherits its successor link, and closes its knowledge period at the correction's
   position; anything else refuses as unsupported. (b) Correction carries its own
   interval end and may overlap, which needs interval ends (R2) and splitting,
   which the cut excludes. Recommendation: (a). It makes r3 cover 1 May to 12 May
   with successor r2, so r2 stays the only current record, without any interval
   grammar. [TRACE]
4. **When a target is stale, and refusal precedence** (D5, D6). Options: a target
   already corrected or revised at the head is stale, a target closed by a
   transition is not (G2a); or a target with no open version is stale (G2b).
   Precedence: Core already refuses by stage (COMPOSE, CHECK, ADMIT); the choice is
   whether a stale target is a CHECK refusal ahead of the ADMIT stale-base refusal.
   Recommendation: the G2a definition, refused at CHECK, so RF-STALE-REVIEW is
   refused for its own reason even when its base is fresh. [INSPECTED, STORAGE]
5. **Persisted-format route for items 2 and 3** (G3 blast radius). Options: A, an
   optional operation field with no identity move, where a Core without it refuses
   "operation fields are not closed" (`knowledge.py` line 412); C, the structural
   builtin goes to version 2, moving four identities and every partial effective
   contract and ledger head, cost larger than the file count and not measured;
   D, the state-version profile, which names correction and transition with the
   same value, changes too (29 and 31 files by full digest and prefix). Under A, two
   Cores holding the same builtin identity would admit and refuse the same bytes
   differently. Recommendation: build RED and GREEN on the branch under A; before
   integration, move to C, and decide D together with C so the shipped profile does
   not say what Core no longer does. This is the cost decision; it waits for items
   2 to 4 because they fix which field is added. [CORE, INSPECTED]

### Group 2: later, not needed for the first cut

Needed for domain-time selection (T4):

- G1 OC-03-ASSUMPTIONS-IN-UNSCOPED (CA05): which accounts are candidates in an
  unscoped read.
- G1 OC-03-USE-SELECTION-SCOPE (CA08): whether a declared default authority
  resolves unscoped reads. Needs D1 first. Which account is the authority is
  adopter policy; whether Core has a record type for a declared authority is Core's.
- G1 OC-07-RULE-SELECTION (VQ04): an accepted persistence rule applies by default
  or only when named.
- G1 OC-07-RULE-ACCEPTANCE: must a rule be accepted in the ledger first. Both
  witnesses implemented only "accepted first", which matches the E-0457 direction
  that making a rule live is a recorded act.
- Valid time per record and interval ends (G3 R2, probes P-UNTIMED and
  P-R2-ONE-CHANGE): an untimed record today gets its change set's valid time.
- Overlapping corrections and interval splitting (RF-OVERLAP beyond the item 3
  refusal).

Needed after T4, not tied to domain time:

- Premise compatibility and PREPARE_INPUTS rules (G3 R8, D11, D12): T5 consumer
  contract.
- A typed relation into a record blocks that record's retirement, and a relation
  cannot be an endpoint (section 1, point 3). The first cut keeps premise links as
  slots, as G3 did. Deciding this is needed before exact old use gets referential
  checks.
- A replay that names the missing artifact (G3 R5, D10).
- Version listing read (G3 R4). A read over data Core already holds; no identity
  moves. It can join the first cut if Luis wants PH-K3 answered by one call.

Independent Core defects the witnesses found, not temporal: an empty list passes a
required multivalued slot in `ContractView.validate_instance` but not in
`OntologyRegistry._missing_required` (R6, both read in code); `decimal` does not
compile (R7).

### Group 3: adopter policy Core should never decide

- G1 OC-06-FLAG-SOURCE (AJ07) and the review unit (D4): whether a reconsideration
  flag is derived or recorded, and over what unit.
- G1 OC-06-SUFFICIENCY (AJ09): whether a remaining argument suffices.
- G1 OC-07-COMPLETENESS-AUTHORITY: who declares completeness, and for which period.
- G1 OC-07-INITIAL-STATE: whether a rule may state a state before the first event.
- G1 OC-08-WITHHELD-SCOPE (ST11): whether only dependent reads refuse. G3 proposes
  that refusing and naming the missing artifact is Core's, and the scope the
  adopter's.
- G1 OC-05-GROUP-OR-MEMBER: whether a member lookup returns its group by default.
  A read presentation choice; no answer depends on it.
- Which account is the authority for a named use or a default (the content of
  OC-03-USE-SELECTION-SCOPE, as opposed to the record type).
- Persistence rule content (D9): event and state vocabulary.
