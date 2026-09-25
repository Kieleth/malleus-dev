# G3: the G1 temporal specimens through Malleus Core as shipped

Base: branch `temporal/g3` at e7020879, which carries the branch-local `KnowledgeChangeHistory.replay_at`. Nothing under `src/` was changed. Every change was composed with `compose_change_set` and admitted by `check_and_admit_change_set` under Core's structural policy. Its one required check is the CORE_BUILTIN `malleus.core.operations-apply-atomically` v1, which Core runs itself. No outcome was supplied by the harness. Expected answers come only from the G1 specimen files, read and never edited.

Reproduce:

    export PYTHONPATH=$PWD/src:$PWD
    python -m pytest design/temporal/g3/test_g3.py -q          # 213 passed
    python design/temporal/g3/report.py                       # the tables below
    python design/temporal/g3/blast_radius.py                 # the blast-radius numbers

## Result in one paragraph

Core answered 45 of 100 query answers correctly, answered 2 wrong, and could not express 53. It refused 10 of the 12 expected refusals and admitted the other 2. Both wrong answers are the same fault. Core's supersession ends the prior record's knowledge period at the new record's position, whether the new record is a correction or a transition. A transition does not make the old state wrong, so the old version should still be believed. A correction that arrives after a transition cannot be recorded as a correction at all: Core refuses it as a fork, because the corrected record is already superseded. The 53 inexpressible answers fall into seven groups. The largest has 35 answers: any query that selects by domain time, account, named use or persistence rule. Core has no read that takes those. Reconstruction obligations hold: every position replays to the same state, and every carried field round-trips.

## Files

| File | What it is |
|---|---|
| `contracts/g1-01.yaml` … `g1-08.yaml` | The smallest LinkML contract per specimen. All eight compile. |
| `driver.py` | Encodes specimen objects into Core operations and drives each specimen change through composition and admission. Records every attempt with ledger bytes before and after. |
| `queries.py` | Evaluates every query against Core reads under the harness rule in `driver.py`'s docstring. |
| `refusals.py` | Attempts every expected refusal and records the stage, reason, detail and ledger bytes. |
| `probes.py` | Ten probes, each isolating one Core mechanism a result depends on. |
| `obligations.py` | Rebuild at every position, and round trip of every specimen object. |
| `blast_radius.py` | Recomputes the identities a persisted-format change would move and counts the tracked files that name them at e7020879. |
| `report.py` | Runs everything once and prints the tables. |
| `expected_today.py` | Today's behaviour, one row per query answer, change and refusal, asserted by the test. |
| `test_g3.py` | 213 tests reproducing every observation. |

## Encoding choices that shape the results

These are adopter choices made here. A different encoding could move individual rows.

1. Assertions are entities carrying `subject`, `property`, `assertion_value` (datatype, lexical string, unit), `basis`, `account` and `evidence_refs`. Values are string lexicals, because the `decimal` range does not compile (probe P-FLOAT).
2. Specimen applicability goes to Core's change-set valid time. An INTERVAL maps to INSTANT at its start. Its end goes only into an adopter slot (`stated_until`), because Core's valid time has no end. RECURRING passes through raw and is refused (RF-UNSUPPORTED).
3. A specimen change whose records state different domain times is split into one change set per valid time (g1-08 R2 became 2 change sets).
4. A specimen change that cites no source names a retained declaration `decl:<position>`. Core requires a nonempty source closure. This applies to 12 changes: K1a, K1b, O2, O3, O5, O7, O9, O10, G3, V2, R3, R4.
5. A declared supersession is sent as Core supersession. When Core refuses it, the records are admitted again as plain additions, and the declared lineage stays only in an adopter slot (`corrects` or `revises`). This happened once, at g1-01 K3, marked ADMITTED_WITHOUT_SUPERSESSION. Every answer that depends on it carries a note.
6. The contract declaration of g1-08 R1 is not a change. Core binds the contract when the history is created, so R1 collapses into genesis.
7. Executions link to their model through a `UsesModel` relation in g1-01, g1-02, g1-05 and g1-08. That makes Core check the range type (RF-CITED-MODEL) and the target's existence (RF-MISSING-MODEL).
8. g1-07 `ReportedEvent` and g1-08 `Assertion` carry `exactly_one_of` with `evidence_refs` required. `required` alone admits an empty list (probe P-REQUIRED-EMPTY-LIST). Without this construct RF-NO-EVIDENCE and RF-MISSING-EVIDENCE would be NOT_OBSERVED.

## What Core gave and what the harness did

Every query row below names both. The rule, from `driver.py`: the harness may map labels to Core ids and ledger coordinates, project fields, filter by field equality or list membership, compare sets, and map an empty or single result to the specimen's answer words. It may not select by domain time, choose between accounts, interpret correction lineage, judge premise compatibility, compute, or decide completeness. A query that needs any of those is NOT_EXPRESSIBLE. For SELECT_APPLICABLE the harness's own naive answer is reported beside it, labelled as harness work. H-hist is interval containment over `record_history`. H-curr is the same over the current graph only. Neither is Core.

The naive column shows why the selection cannot be left to a simple filter. H-hist matches the transition queries (P03) and fails the correction ones. H-curr matches the correction ones (P04, P06, P07, S03, OQ08) and fails the transition ones. P05 and P10 fail both, because r3's end lives only in the adopter slot. No Core answer matched a forbidden answer.

## Outcome counts

| Category | Count |
|---|---|
| ANSWERED_CORRECT | 45 |
| ANSWERED_WRONG | 2 |
| REFUSED | 0 |
| NOT_EXPRESSIBLE | 53 |
| EXPECTED_REFUSAL_OBSERVED | 10 |
| EXPECTED_REFUSAL_NOT_OBSERVED | 2 |

There are 94 queries. Six have two open branches, so there are 100 answers. No read query was refused by Core. The refusals Core made fell on changes: g1-01 K3's declared correction, and every step listed in the refusal table.

### ANSWERED_WRONG

| Query | Field | Core | Specimen | Why |
|---|---|---|---|---|
| g1-01 PH-K2 | `metadata[a2].knowledge_until` | K2 | null | K2 is a transition. Core's supersession retires r1's version at K2, so its knowledge period ends there. The specimen says the old state is still believed. |
| g1-01 PH-K3-META | `metadata[a2].knowledge_until` | K2 | K3 | K3 corrects r1. Core refused that supersession as a fork, so K3 does not appear in r1's history. The only end Core has is K2. |

### NOT_EXPRESSIBLE, by reason

| Reason | Answers |
|---|---|
| No Core read takes a domain time, account precedence, named-use context or persistence rule | 35: g1-01 P01 to P10; g1-02 OQ08; g1-03 CA01, CA02, CA03, CA04, CA05 (2 branches), CA07, CA08 (2 branches), CA10; g1-04 S01, S02, S03; g1-07 VQ01, VQ03, VQ04 (2 branches), VQ05 to VQ11 |
| The premise must first be selected by domain time and account | 2: g1-01 C02, PC-NOT-COMPUTED |
| Core has no premise-compatibility or common-applicability operation | 5: g1-01 C05; g1-04 C06; g1-05 CC05, CC06, CC07 |
| Older versions are reachable only by `replay_at` at their own position, and no read lists them | 1 as the whole answer: g1-01 PH-K3 (`visible_refs`). The same gap is a field inside PH-K2 and PH-K3-META (`visible_refs`, `metadata[a1].knowledge_until`). |
| Core has no reconsideration flag | 3: g1-06 AJ06, AJ07 (2 branches) |
| Core has no support or sufficiency field | 2: g1-06 AJ09 (2 branches) |
| No public API rebuilds a history with a retained artifact withheld | 5: g1-08 ST08, ST09, ST10, ST11 (2 branches) |

The reconsideration and sufficiency rows are probably adopter work: a slot plus a declared rule. They were not built here, so this is unverified.

### Expected refusals

| Refusal | Expected | Class | What Core did |
|---|---|---|---|
| g1-01 RF-STALE-BASE | STALE_BASE | OBSERVED | Supersession: CHECK refused, "record supersession forks prior record: r1". Plain: ADMIT refused STALE_BASE. |
| g1-01 RF-OVERLAP | UNSUPPORTED_SEMANTICS | NOT_OBSERVED | Supersession refused as a fork, which is the same refusal the valid r3 gets. Plain addition admitted. Core cannot tell an overlapping correction from a valid one. |
| g1-02 RF-STALE-EXEC | STALE_BASE | OBSERVED | ADMIT refused STALE_BASE. |
| g1-02 RF-BORROWED | PREMISE_MISMATCH | NOT_OBSERVED | Admitted. The structural check has no premise rule. A Prolog rule check might catch it; that route was not built here. |
| g1-05 RF-CITED-MODEL | MISSING_MODEL | OBSERVED | Relation range check: "Target 'work:SM' has type 'Subject', expected ...Model". The same link as a plain slot is admitted. |
| g1-06 RF-STALE-REVIEW | STALE_TARGET | OBSERVED | Fork refusal, then STALE_BASE. Composed fresh at J4p: fork refusal, then the plain addition is admitted. So the refusal comes from the stale base, not from the stale target. |
| g1-07 RF-NO-EVIDENCE | MISSING_EVIDENCE | OBSERVED | Refused through the contract's `exactly_one_of`. With no source at all, COMPOSE refuses MALFORMED_CHANGE_SET "source closure must be nonempty and unique". |
| g1-08 RF-PARTIAL | UNKNOWN_REFERENCE | OBSERVED | "Target entity 'phantom:subject' does not exist". |
| g1-08 RF-MISSING-MODEL | MISSING_MODEL | OBSERVED | "Target entity 'phantom:model' does not exist". The slot-only link is admitted. |
| g1-08 RF-MISSING-EVIDENCE | MISSING_EVIDENCE | OBSERVED | Supersession: "record replacement contradicts prior valid time: q-price". Plain: `exactly_one_of` refusal. |
| g1-08 RF-UNSUPPORTED | UNSUPPORTED_SEMANTICS | OBSERVED | COMPOSE refused MALFORMED_CHANGE_SET "unsupported valid-time kind: RECURRING". |
| g1-08 RF-MISSING-CONTRACT | MISSING_CONTRACT | OBSERVED | ADMIT refused STALE_BASE "change set names a different effective contract". A contract named only in a record slot is admitted. |

Ledger bytes (sha256 and length) were identical before and after every refused admission. The refusal table below gives the digests. COMPOSE refusals never reach the ledger.

## Probes

| Probe | Result |
|---|---|
| P-K3-TARGET-R2 | The g1-01 correction superseding r2 instead of r1 is refused: "record replacement contradicts prior valid time: r2". Core rejects both possible encodings of a correction after a transition. |
| P-REL-SUPERSEDE | Link the execution to r1 with a typed relation, then supersede r1 (the K2 transition). Core refuses: "Cannot rehydrate graph from records: ... Target entity 'r1' does not exist". A record that a relation points to cannot be superseded. That is why the premise link is a slot here. |
| P-R2-ONE-CHANGE | g1-08 R2 as one change set. INSTANT 2026-05-01 dates q-qty from 2026-05-01, which is ST03's forbidden answer. NONE_STATED leaves q-price undated, which is ST01's forbidden answer. |
| P-UNTIMED | Records whose specimen gives no applicability get their change set's valid time: product:P INSTANT 2026-05-01, valve:V INSTANT 2026-06-03T09:00. |
| P-FLOAT | Range `decimal` fails to compile: BindingRefusal UNKNOWN_REFERENCE. With range `float`, 5.40 is stored and hashed as 5.4. |
| P-REQUIRED-EMPTY-LIST | A required multivalued slot admits `[]`. `ContractView.validate_instance` counts an empty list as present. `OntologyRegistry._missing_required` and `exactly_one_of` count it as missing. |
| P-WITHHELD-SOURCE | Removing src:quote from a copy of the ledger and re-chaining the hashes: replay refuses STALE_BASE "change-set base ledger head is stale". The refusal does not name src:quote. It comes from the moved base head, before any closure check. |
| P-WITHHELD-CONTRACT | Removing the bootstrap contract gives MALFORMED_HISTORY "ledger lacks one exact retained bootstrap artifact". |
| P-CLI | `malleus-compiler query` reads only the head: Q1, Q2 and H1 at 36 events. Naming A2's head and count exits 2 with STALE_BASE. |
| P-TRACE | `trace_population_record` refuses POPULATION_PLAN_NOT_BOUND on a composed change set. |
| P-PROFILES | The shipped STATE_VERSION_PROFILE maps both correction and transition to SUPERSEDE_STATE_VERSION. OBJECT_EVENT_PROFILE declares CURRENT_STATE_DERIVED_FROM_EVENTS. Nothing executes it; it is only parsed. |

Both withheld probes edit a ledger copy outside the public API, the same technique Core's T2 tests use. Only the refusal they read back is Core's.

## Obligations

Rebuild: reopening each ledger and running `replay_at` at every position gives the same receipt and `record_history` as when that position was written. This holds at all 44 positions in the 8 specimens. Round trip: every specimen object decodes from Core's graph with every carried field equal. No field differs. Two things are not carried. The first is `source_kind` (and `locator` for g1-02 src:table), because the encoder does not write them. The second is g1-08 `contract:c1`: Core binds the contract when the history is created, so it is not a record. Reads wrote nothing: the ledger bytes of every specimen are identical before and after all query evaluation.

## Blast radius of a persisted-format change

Identities are read from Core objects (`blast_radius.shipped()`). Each scenario recomputes them in memory from Core's shipped profile JSON. The recomputation first reproduces the shipped bundle identity unchanged. File counts are `git grep -l -F <string> e7020879 --`, over the full digest and over its 8-hex prefix, so files written by this gate are not counted.

| Scenario | What moves | Files naming the moved identity at e7020879 (full / 8-hex prefix) | Today's Core on the new bytes |
|---|---|---|---|
| A. One optional operation field, for example a correction link. It is written only when set. Grammar string and builtin version stay the same. | No identity. Existing change-set bytes do not change. The bundle bytes name neither the grammar nor any operation field. | none | Refuses: MALFORMED_CHANGE_SET "operation fields are not closed". An older Core cannot read a ledger that uses the field. |
| B. Change-set grammar bump (`malleus.knowledge-change-set/private-v0` to `v1`) | Every newly composed change-set identity, and every ledger head derived from it. Example: sha256:46be7459… becomes sha256:5f9a21ec…. | Grammar string: 18 (handover 2, research 14, src 1, tests 1) | Refuses: UNSUPPORTED_GRAMMAR |
| C. The structural builtin learns the new field or op kind, and its version goes from 1 to 2 | Check contract b923c279… → 9c25c6db… | 2 / 6 | Registry: "Core holds no builtin check … at version '2'" |
| | Structural admission policy c1d696f2… → 8239b685… | 0 / 4 | |
| | Normative profile a39681c4… → b704e7fb… | 0 / 4 | |
| | Structural history bundle 8a994ed0… → 5a5e0aca… | 0 / 6 | |
| | Partial effective contract of g1-01: dc824f99… → cf4689a8…. The same happens for every contract. | not counted | |
| | Every structural history's bootstrap bytes, so every ledger head and every policy_identity recorded in CHANGE_PROPOSED and CHECK_RECORDED | see limits | |
| D. The state-version profile tells correction from transition | State-version profile b18f3129… → e2c8e163… | 29 / 31 (.claude 1, handover 5, paper-v4 11, research 13, tests 1) | not tested |

These never move in any scenario: protocol machine ad4d7153… (15 files), history binding 87d653d3… (36), contract revision policy e129b6e8… (1 / 5), source-assertion profile 2317d88f… (114 / 115), object-event profile 38bb0e40… (8).

The OVR-000466 precedent: when a content-addressed policy digest moves, every frozen artifact that records a ledger coordinate moves with it, and the only real check is regenerating the family. Grepping undercounts. The counts above find files that spell an identity. They cannot find a frozen ledger whose head was derived from it. At e7020879 no tracked ledger contains a change set under this grammar, but frozen evidence directories do record heads and policy identities in other forms. Scenario C's real cost is therefore larger than its file count and was not measured.

## Minimal Core request list

Each request is tied to the answers it would unblock. Roles use the brief's vocabulary. Identity movement refers to the scenarios above. Every request is presented as options. None is decided.

| # | Request | Unblocks | Role | Moves persisted identities? |
|---|---|---|---|---|
| 1 | Correction as a change kind separate from transition supersession. Two options. (a) Supersession by a transition leaves the prior version's knowledge period open. (b) A correction can target a record that is already superseded, and it closes that record's knowledge period at the correction's position. | PH-K2, PH-K3-META (both wrong today); g1-01 K3 admitted without supersession; P-K3-TARGET-R2; RF-OVERLAP, which needs the correction lineage before overlap can be judged | PROTOCOL_INVARIANT for what knowledge_until means. OPTIONAL_PROFILE for which changes are corrections: the state-version profile already names both, with the same semantics. | Yes. An op field without a version bump is scenario A: no identity moves, but older Cores cannot read the bytes. With a builtin bump it is scenario C. Changing the profile semantics is scenario D. |
| 2 | Valid time per record, or a valid-time interval with an end | g1-08 R2 split; P-R2-ONE-CHANGE forbidden answers; P-UNTIMED (untimed records given a date); P05 and P10, whose end exists only in an adopter slot | OPTIONAL_PROFILE for interval semantics. PROTOCOL_INVARIANT only for "a record gets no valid time it did not state", if Luis wants that. | Yes. Valid time is in the change-set bytes, so B at least, and C, because the builtin applies it. |
| 3 | A read that selects accepted records applicable at a domain time, at a named ledger position | 35 SELECT_APPLICABLE answers, C02, PC-NOT-COMPUTED; also the CLI's head-only read (P-CLI) | REFERENCE_IMPLEMENTATION for the read itself. Account precedence, named-use context and persistence rules stay ADOPTER_CHOICE, or OPTIONAL_PROFILE if Core ships a default. | No, if it is a read. Yes, if selection rules become persisted policy, in the same way as C. |
| 4 | A read listing every version of a record with its knowledge period at a position | PH-K3; `visible_refs` and `metadata[a1].knowledge_until` inside PH-K2 and PH-K3-META | REFERENCE_IMPLEMENTATION. `record_history` plus `replay_at` already hold the data. | No |
| 5 | A replay that names the missing retained artifact, and says which reads depend on it | ST08, ST09, ST10, ST11 (both branches); P-WITHHELD-SOURCE | PROTOCOL_INVARIANT: refuse and name what is missing. ADOPTER_CHOICE: whether only dependent reads refuse (ST11's open choice). | No |
| 6 | An empty list does not satisfy a required multivalued slot, the same rule in `ContractView.validate_instance` as in `OntologyRegistry` | RF-NO-EVIDENCE and RF-MISSING-EVIDENCE without the `exactly_one_of` workaround; P-REQUIRED-EMPTY-LIST | PROTOCOL_INVARIANT (contract semantics) | Changed silently, nothing moves, but existing ledgers holding `[]` in a required slot would stop replaying. Changed with a builtin bump, it is scenario C. |
| 7 | A `decimal` range that keeps the lexical form | P-FLOAT; every price in g1-02 and g1-08, stored here as strings | REFERENCE_IMPLEMENTATION (compiler trusted ranges) | Not measured. It adds a trusted builtin to the compiler. Whether that moves any contract or profile identity was not checked. |
| 8 | Premise compatibility across inputs | C05, C06, CC05, CC06, CC07 | OPTIONAL_PROFILE or ADOPTER_CHOICE. The specimens do not settle which. | No, if it is a read. |

These items are left off the list, because the specimens show they are adopter work or not blocking. Reconsideration flags and support sufficiency (AJ06, AJ07, AJ09) are ADOPTER_CHOICE: a slot plus a rule. RF-BORROWED is probably catchable by an adopter Prolog rule check (ADOPTER_CHOICE); that was not built here. The `decl:` source for changes that cite no source is an adopter workaround, and it works. `trace_population_record` on composed change sets (P-TRACE) is a REFERENCE_IMPLEMENTATION gap, and no specimen query needs it.

## What this cannot establish

1. Only the structural check ran. No Prolog rule check or SHACL check was built, so the refusals rule checks might add (RF-BORROWED, RF-OVERLAP, premise compatibility) are untested.
2. The specimens are synthetic and small, with 94 queries in total. A pass here says nothing about scale, or about documents that do not look like them.
3. The contracts and the encoding are one adopter's choices (see "Encoding choices"). A different encoding might turn some NOT_EXPRESSIBLE rows into harness work, or produce different refusal paths.
4. The naive harness answers are one possible naive rule each. They show that neither simple filter is enough. They do not show what the right rule is.
5. File counts undercount. Frozen artifacts that derive from a moved identity without spelling it are not found. Regenerating the affected families was not attempted.
6. `source_kind` and `locator` are not carried, so no query about source metadata was tested.
7. The withheld-artifact probes edit ledger copies outside the public API. Their STALE_BASE result reflects the re-chained base head, not a closure check.
8. `replay_at` is branch-local on `temporal/g3`. Every INSPECT_HISTORY, EXPLAIN_EXECUTION and rebuild result depends on it, and it is not on main.

## Tables

Generated by `report.py`, which is asserted row by row by `test_g3.py` through `expected_today.py`.

### Changes

| Specimen | Position | Declared kind | Core outcome | Notes |
|---|---|---|---|---|
| g1-01 | K0 | GENESIS | GENESIS |  |
| g1-01 | K1 | REPORT | ADMITTED | Records with no specimen applicability (product:P, account:reported-price) receive this change set's valid time INSTANT 2026-05-01T00:00:00Z in record_history. |
| g1-01 | K1a | MODEL_DEFINITION | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:K1a, a retained declaration of its own objects. |
| g1-01 | K1b | EXECUTION_RECORD | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:K1b, a retained declaration of its own objects. |
| g1-01 | K2 | TRANSITION | ADMITTED |  |
| g1-01 | K3 | CORRECTION | ADMITTED_WITHOUT_SUPERSESSION | CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: record supersession forks prior record: r1; Core refused the explicit supersession; the records were then admitted as plain additions, with the declared lineage kept only in an adopter slot. |
| g1-02 | O0 | GENESIS | GENESIS |  |
| g1-02 | O1 | REPORT | ADMITTED |  |
| g1-02 | O2 | MODEL_DEFINITION | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:O2, a retained declaration of its own objects. |
| g1-02 | O3 | EXECUTION_RECORD | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:O3, a retained declaration of its own objects. |
| g1-02 | O4 | ASSUMPTION | ADMITTED |  |
| g1-02 | O5 | EXECUTION_RECORD | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:O5, a retained declaration of its own objects. |
| g1-02 | O6 | CORRECTION | ADMITTED |  |
| g1-02 | O7 | EXECUTION_RECORD | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:O7, a retained declaration of its own objects. |
| g1-02 | O8 | MODEL_DEFINITION | ADMITTED |  |
| g1-02 | O9 | CONTEXT_BINDING | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:O9, a retained declaration of its own objects. |
| g1-02 | O10 | EXECUTION_RECORD | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:O10, a retained declaration of its own objects. |
| g1-03 | A0 | GENESIS | GENESIS |  |
| g1-03 | A1 | REPORT | ADMITTED | Records with no specimen applicability (gauge:G, account:S1) receive this change set's valid time INSTANT 2026-05-01T00:00:00Z in record_history. |
| g1-03 | A2 | REPORT | ADMITTED | Records with no specimen applicability (account:S2) receive this change set's valid time INSTANT 2026-05-01T00:00:00Z in record_history. |
| g1-03 | A3 | ASSUMPTION | ADMITTED | Records with no specimen applicability (account:scenario-1) receive this change set's valid time INSTANT 2026-05-01T00:00:00Z in record_history. |
| g1-03 | A4 | INTERPRETATION | ADMITTED |  |
| g1-04 | M0 | GENESIS | GENESIS |  |
| g1-04 | M1 | REPORT | ADMITTED |  |
| g1-04 | M2 | CORRECTION | ADMITTED |  |
| g1-05 | G0 | GENESIS | GENESIS |  |
| g1-05 | G1 | REPORT | ADMITTED |  |
| g1-05 | G2 | REPORT | ADMITTED |  |
| g1-05 | G3 | MODEL_DEFINITION | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:G3, a retained declaration of its own objects. |
| g1-06 | J0 | GENESIS | GENESIS |  |
| g1-06 | J1p | REPORT | ADMITTED |  |
| g1-06 | J2p | INTERPRETATION | ADMITTED |  |
| g1-06 | J3p | ARGUMENT | ADMITTED |  |
| g1-06 | J4p | REASSESSMENT | ADMITTED |  |
| g1-07 | V0 | GENESIS | GENESIS |  |
| g1-07 | V1 | REPORT | ADMITTED | Records with no specimen applicability (valve:V) receive this change set's valid time INSTANT 2026-06-03T09:00:00Z in record_history. |
| g1-07 | V2 | RULE_DECLARATION | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:V2, a retained declaration of its own objects. |
| g1-07 | V3 | REPORT | ADMITTED |  |
| g1-07 | V4 | PLAN | ADMITTED |  |
| g1-08 | R0 | GENESIS | GENESIS |  |
| g1-08 | R1 | CONTRACT_DECLARATION | COLLAPSED_INTO_GENESIS | Core binds the governing contract when the history is created, not in an accepted change; this position is the genesis position. |
| g1-08 | R2 | REPORT | SPLIT | Records in this change state different domain times; Core's valid time is one per change set, so the change is admitted as 2 change sets. |
| g1-08 | R3 | MODEL_DEFINITION | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:R3, a retained declaration of its own objects. |
| g1-08 | R4 | EXECUTION_RECORD | ADMITTED | No specimen source is cited; Core requires a nonempty source closure, so the change names decl:R4, a retained declaration of its own objects. |

### Queries

| Specimen | Query | Kind | Branch | Class | Wrong (Core vs expected) | Not expressible | Reason | Core gave | Harness did | Harness naive | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| g1-01 | P01 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-01 | P02 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-01 | P03 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr DIFFERS |  |
| g1-01 | P04 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr MATCH |  |
| g1-01 | P05 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr DIFFERS |  |
| g1-01 | P06 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr MATCH |  |
| g1-01 | P07 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr MATCH |  |
| g1-01 | P08 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-01 | P09 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-01 | P10 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr DIFFERS |  |
| g1-01 | PH-K0 | INSPECT_HISTORY |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-01 | PH-K1 | INSPECT_HISTORY |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-01 | PH-K2 | INSPECT_HISTORY |  | ANSWERED_WRONG | metadata[a2].knowledge_until: K2 vs null | visible_refs, metadata[a1].knowledge_until | records and current versions match; older versions a1 are reachable only by replay_at at their own position, and no read lists them; older version: not in this read; Core's answer: the position where r1 was superseded, after which only the replacement is current | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-01 | PH-K3 | INSPECT_HISTORY |  | NOT_EXPRESSIBLE |  | visible_refs | records and current versions match; older versions a1 are reachable only by replay_at at their own position, and no read lists them | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  | Reached through the fallback encoding: c, r3 was admitted as a plain addition after Core refused the declared correction. |
| g1-01 | PH-K3-META | INSPECT_HISTORY |  | ANSWERED_WRONG | metadata[a2].knowledge_until: K2 vs K3 | visible_refs, metadata[a1].knowledge_until | records and current versions match; older versions a1 are reachable only by replay_at at their own position, and no read lists them; older version: not in this read; Core's answer: the position where r1 was superseded, after which only the replacement is current | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  | Reached through the fallback encoding: c, r3 was admitted as a plain addition after Core refused the declared correction. |
| g1-01 | PX-r1-K3 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  | record_history[r1].valid_to is INSTANT 2026-05-12T00:00:00Z, Core's period end derived from the successor's start. The report's own time is the valid time of the change set that added it; reading valid_to as the report's end would give the forbidden answer. |
| g1-01 | C01 | EXPLAIN_EXECUTION |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history of the execution, its result, and replay_at(stored coordinates) for the old premise | list projection of bindings; coordinate-to-label mapping |  | replay_at(stored selection coordinates) returns r1 = 750, valid_to None, superseded_by None |
| g1-01 | C02 | COMPARE_PREMISES |  | NOT_EXPRESSIBLE |  | state, previous_refs, new_refs, new_cell_refs | the new premise must be selected by domain time and account | none | none |  |  |
| g1-01 | PC-NOT-COMPUTED | RESULT_FOR_SELECTION |  | NOT_EXPRESSIBLE |  | state | the premise must first be selected by domain time and account | none | a lookup by model alone, reported as naive | model-only DIFFERS |  |
| g1-01 | C05 | PREPARE_INPUTS |  | NOT_EXPRESSIBLE |  | state | Core has no premise-compatibility or common-applicability operation | none | none |  |  |
| g1-02 | OQ01 | RESULT_FOR_CONTEXT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: Execution and Result records | equality filter context_ref, execution_ref; empty mapped to NOT_COMPUTED |  |  |
| g1-02 | OQ02 | RESULT_FOR_CONTEXT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: Execution and Result records | equality filter context_ref, execution_ref; empty mapped to NOT_COMPUTED |  |  |
| g1-02 | OQ03 | RESULT_FOR_CONTEXT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: Execution and Result records | equality filter context_ref, execution_ref; empty mapped to NOT_COMPUTED |  |  |
| g1-02 | OQ04 | RESULT_FOR_CONTEXT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: Execution and Result records | equality filter context_ref, execution_ref; empty mapped to NOT_COMPUTED |  |  |
| g1-02 | OQ05 | RESULT_FOR_CONTEXT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: Execution and Result records | equality filter context_ref, execution_ref; empty mapped to NOT_COMPUTED |  |  |
| g1-02 | OQ06 | COMPARE_PREMISES |  | ANSWERED_CORRECT |  |  |  | two distinct accepted record identities | identity comparison |  | H1 and B2: equal value True, basis ASSUMPTION vs CORRECTION, account account:what-if vs account:order-reported |
| g1-02 | OQ07 | EXPLAIN_EXECUTION |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history of the execution, its result, and replay_at(stored coordinates) for the old premise | list projection of bindings; coordinate-to-label mapping |  |  |
| g1-02 | OQ08 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr MATCH |  |
| g1-02 | OQ09 | SELECT_ACCOUNT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).graph, Core's current non-superseded records | equality filter on subject/property/account; empty/one/many mapped to state |  |  |
| g1-02 | OQ10 | SELECT_ACCOUNT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).graph, Core's current non-superseded records | equality filter on subject/property/account; empty/one/many mapped to state |  |  |
| g1-02 | OQ11 | RESULT_FOR_CONTEXT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: Execution and Result records | equality filter context_ref, execution_ref; empty mapped to NOT_COMPUTED |  |  |
| g1-02 | OQ12 | RESULT_FOR_CONTEXT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: Execution and Result records | equality filter context_ref, execution_ref; empty mapped to NOT_COMPUTED |  |  |
| g1-02 | OQ13 | RESULT_FOR_CONTEXT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: Execution and Result records | equality filter context_ref, execution_ref; empty mapped to NOT_COMPUTED |  |  |
| g1-02 | OQ14 | INSPECT_HISTORY |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-03 | CA01 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-03 | CA02 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-03 | CA03 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, candidate_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-03 | CA04 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value, basis | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-03 | CA05 | SELECT_APPLICABLE | Assumptions enter only when their account is named | NOT_EXPRESSIBLE |  | state, candidate_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr DIFFERS |  |
| g1-03 | CA05 | SELECT_APPLICABLE | Every accepted account is a candidate | NOT_EXPRESSIBLE |  | state, candidate_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-03 | CA06 | COMPARE_PREMISES |  | ANSWERED_CORRECT |  |  |  | two distinct accepted record identities | identity comparison |  | Q2 and H1: equal value True, basis REPORTED vs ASSUMPTION, account account:S2 vs account:scenario-1 |
| g1-03 | CA07 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist N/A: needs a context or persistence rule; H-curr N/A: needs a context or persistence rule |  |
| g1-03 | CA08 | SELECT_APPLICABLE | A use selection binds only that use | NOT_EXPRESSIBLE |  | state, candidate_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr DIFFERS |  |
| g1-03 | CA08 | SELECT_APPLICABLE | An adopter-declared default authority resolves unscoped requests | NOT_EXPRESSIBLE |  | state, selected_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr DIFFERS |  |
| g1-03 | CA09 | INSPECT_HISTORY |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-03 | CA10 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-04 | S01 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-04 | S02 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-04 | S03 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, selected_refs, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr MATCH |  |
| g1-04 | S04 | INSPECT_HISTORY |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-04 | SQ-ACCOUNT-M2 | SELECT_ACCOUNT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).graph, Core's current non-superseded records | equality filter on subject/property/account; empty/one/many mapped to state |  |  |
| g1-04 | SQ-ACCOUNT-M1 | SELECT_ACCOUNT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).graph, Core's current non-superseded records | equality filter on subject/property/account; empty/one/many mapped to state |  |  |
| g1-04 | SQ-EXACT-m1 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  | record_history[m1].valid_to is NONE_STATED None, Core's period end derived from the successor's start. The report's own time is the valid time of the change set that added it; reading valid_to as the report's end would give the forbidden answer. |
| g1-04 | C06 | PREPARE_INPUTS |  | NOT_EXPRESSIBLE |  | state, unresolved_refs | Core has no premise-compatibility or common-applicability operation | none | none |  |  |
| g1-05 | CC01 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-05 | CC02 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-05 | CC03 | RESULT_FOR_SELECTION |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: no Result record for that model | equality filter; empty mapped to NOT_COMPUTED |  |  |
| g1-05 | CC04 | RESULT_FOR_SELECTION |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history: no Result record for that model | equality filter; empty mapped to NOT_COMPUTED |  |  |
| g1-05 | CC05 | PREPARE_INPUTS |  | NOT_EXPRESSIBLE |  | state, conflict_refs | Core has no premise-compatibility or common-applicability operation | none | none |  |  |
| g1-05 | CC06 | PREPARE_INPUTS |  | NOT_EXPRESSIBLE |  | state | Core has no premise-compatibility or common-applicability operation | none | none |  |  |
| g1-05 | CC07 | PREPARE_INPUTS |  | NOT_EXPRESSIBLE |  | state, conflict_refs | Core has no premise-compatibility or common-applicability operation | none | none |  |  |
| g1-06 | AJ01 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-06 | AJ02 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-06 | AJ03 | SELECT_ACCOUNT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).graph, Core's current non-superseded records | equality filter on subject/property/account; empty/one/many mapped to state |  |  |
| g1-06 | AJ04 | SELECT_ACCOUNT |  | ANSWERED_CORRECT |  |  |  | replay_at(at).graph, Core's current non-superseded records | equality filter on subject/property/account; empty/one/many mapped to state |  |  |
| g1-06 | AJ05 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-06 | AJ06 | INSPECT_HISTORY |  | NOT_EXPRESSIBLE |  | metadata[D1].reconsideration, metadata[D2].reconsideration | Core has no reconsideration flag | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-06 | AJ07 | INSPECT_HISTORY | Derived from declared premises | NOT_EXPRESSIBLE |  | metadata[D1].reconsideration, metadata[D2].reconsideration | Core has no reconsideration flag | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-06 | AJ07 | INSPECT_HISTORY | Recorded by a reviewer; none recorded yet | NOT_EXPRESSIBLE |  | metadata[D1].reconsideration, metadata[D2].reconsideration | Core has no reconsideration flag | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-06 | AJ08 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-06 | AJ09 | SELECT_ACCOUNT | No declared sufficiency rule | NOT_EXPRESSIBLE |  | metadata[C1].support_sufficiency | Core has no support or sufficiency field | replay_at(at).graph, Core's current non-superseded records | equality filter on subject/property/account; empty/one/many mapped to state |  |  |
| g1-06 | AJ09 | SELECT_ACCOUNT | Declared rule: any argument with no revised premise suffices | NOT_EXPRESSIBLE |  | metadata[C1].support_sufficiency, metadata[C1].supporting_refs | Core has no support or sufficiency field | replay_at(at).graph, Core's current non-superseded records | equality filter on subject/property/account; empty/one/many mapped to state |  |  |
| g1-07 | VQ01 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-07 | VQ02 | INSPECT_HISTORY |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-07 | VQ03 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr DIFFERS |  |
| g1-07 | VQ04 | SELECT_APPLICABLE | Only when named by the caller | NOT_EXPRESSIBLE |  | state, unresolved_refs | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr DIFFERS |  |
| g1-07 | VQ04 | SELECT_APPLICABLE | By default within its scope | NOT_EXPRESSIBLE |  | state, derived_from_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist DIFFERS; H-curr DIFFERS |  |
| g1-07 | VQ05 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, derived_from_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist N/A: needs a context or persistence rule; H-curr N/A: needs a context or persistence rule |  |
| g1-07 | VQ06 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, derived_from_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist N/A: needs a context or persistence rule; H-curr N/A: needs a context or persistence rule |  |
| g1-07 | VQ07 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, derived_from_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist N/A: needs a context or persistence rule; H-curr N/A: needs a context or persistence rule |  |
| g1-07 | VQ08 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, derived_from_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist N/A: needs a context or persistence rule; H-curr N/A: needs a context or persistence rule |  |
| g1-07 | VQ09 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist N/A: needs a context or persistence rule; H-curr N/A: needs a context or persistence rule |  |
| g1-07 | VQ10 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state, derived_from_refs, value | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist N/A: needs a context or persistence rule; H-curr N/A: needs a context or persistence rule |  |
| g1-07 | VQ11 | SELECT_APPLICABLE |  | NOT_EXPRESSIBLE |  | state | no Core read takes a domain time, account precedence, named-use context or persistence rule | none | naive interval containment over record_history (H-hist) and over the current graph (H-curr), reported separately | H-hist MATCH; H-curr MATCH |  |
| g1-07 | VQ12 | INSPECT_HISTORY |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-07 | VQ13 | INSPECT_HISTORY |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-08 | ST01 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-08 | ST02 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-08 | ST03 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-08 | ST04 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-08 | ST05 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-08 | ST06 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |
| g1-08 | ST07 | EXPLAIN_EXECUTION |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history of the execution, its result, and replay_at(stored coordinates) for the old premise | list projection of bindings; coordinate-to-label mapping |  |  |
| g1-08 | ST08 | EXPLAIN_EXECUTION |  | NOT_EXPRESSIBLE |  | state, missing_refs | no public API rebuilds a history with a retained artifact withheld | none; see probe P-WITHHELD | none |  |  |
| g1-08 | ST09 | EXPLAIN_EXECUTION |  | NOT_EXPRESSIBLE |  | state, missing_refs | no public API rebuilds a history with a retained artifact withheld | none; see probe P-WITHHELD | none |  |  |
| g1-08 | ST10 | EXACT_LOOKUP |  | NOT_EXPRESSIBLE |  | state, missing_refs | no public API rebuilds a history with a retained artifact withheld | none; see probe P-WITHHELD | none |  |  |
| g1-08 | ST11 | EXPLAIN_EXECUTION | Only reads whose closure needs it refuse | NOT_EXPRESSIBLE |  | state, premise_refs, model_ref, result_ref, value | no public API rebuilds a history with a retained artifact withheld | none; see probe P-WITHHELD | none |  |  |
| g1-08 | ST11 | EXPLAIN_EXECUTION | Any missing retained artifact refuses the whole rebuild | NOT_EXPRESSIBLE |  | state, missing_refs | no public API rebuilds a history with a retained artifact withheld | none; see probe P-WITHHELD | none |  |  |
| g1-08 | ST12 | INSPECT_HISTORY |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history, all accepted records including superseded ones | equality filter on subject/property (or conclusion_ref); label mapping |  |  |
| g1-08 | ST13 | EXACT_LOOKUP |  | ANSWERED_CORRECT |  |  |  | replay_at(at).record_history[target]; its change set's valid time and source closure | label mapping and field projection |  |  |

### Refusals

| Specimen | Refusal | Expected category | Class | Procedure steps (stage/reason: detail) | Alternatives | Ledger bytes around each admission |
|---|---|---|---|---|---|---|
| g1-01 | RF-STALE-BASE | STALE_BASE | EXPECTED_REFUSAL_OBSERVED | supersede REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: record supersession forks prior record: r1; REFUSED ADMIT/STALE_BASE: change-set base ledger head is stale |  | sha256:10875563d9bbf48bc0f83c0695c7ba78e7c7bf67cffdfc5427f7d54346d0aa03 (448076 bytes) -> same; sha256:10875563d9bbf48bc0f83c0695c7ba78e7c7bf67cffdfc5427f7d54346d0aa03 (448076 bytes) -> same |
| g1-01 | RF-OVERLAP | UNSUPPORTED_SEMANTICS | EXPECTED_REFUSAL_NOT_OBSERVED | supersede REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: record supersession forks prior record: r1; ADMITTED /:  |  | sha256:61eee42a78c8fe2faa718bc994be20927c97de76a483bc1103247d34d44e72ea (448035 bytes) -> same; sha256:61eee42a78c8fe2faa718bc994be20927c97de76a483bc1103247d34d44e72ea (448035 bytes) -> sha256:5bb48afebcf22536286f052a8a7461e5129d9e6375334dd799dc2e4fd1e86b23 (454741 bytes) |
| g1-02 | RF-STALE-EXEC | STALE_BASE | EXPECTED_REFUSAL_OBSERVED | REFUSED ADMIT/STALE_BASE: change-set base ledger head is stale |  | sha256:25bff80ad31f6e5a08e5d0f7de8091263b346e61de99e42a22f7a6c4cf069414 (463920 bytes) -> same |
| g1-02 | RF-BORROWED | PREMISE_MISMATCH | EXPECTED_REFUSAL_NOT_OBSERVED | ADMITTED /:  |  | sha256:3660ac04026289ca3d0f08d95a295c7503463f837b55c79a489439547e4f74fb (463924 bytes) -> sha256:8c1b241fa3c5c238888eadbe734ca23c9c9740837a51a7153a97ef6e4c3a151b (471435 bytes) |
| g1-05 | RF-CITED-MODEL | MISSING_MODEL | EXPECTED_REFUSAL_OBSERVED | REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: Target 'work:SM' has type 'Subject', expected 'https://example.malleus.dev/temporal-g3/g1-05/Model' for UsesModel | model link as a slot only: ADMITTED / | sha256:4ee817ef935a703ea992445fda25623e490f86de6271a345150a1917e5ce2a5b (406526 bytes) -> same |
| g1-06 | RF-STALE-REVIEW | STALE_TARGET | EXPECTED_REFUSAL_OBSERVED | supersede REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: record supersession forks prior record: J1; REFUSED ADMIT/STALE_BASE: change-set base ledger head is stale | composed fresh at J4p (base not stale): REFUSED CHECK/CONTENT_RULE_VIOLATED, ADMITTED / | sha256:cccc28ed4b7c1b039a5204b0e77f561f052ac356d3c3ec96a82825c26b32f675 (339587 bytes) -> same; sha256:cccc28ed4b7c1b039a5204b0e77f561f052ac356d3c3ec96a82825c26b32f675 (339587 bytes) -> same |
| g1-07 | RF-NO-EVIDENCE | MISSING_EVIDENCE | EXPECTED_REFUSAL_OBSERVED | REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: Class 'https://example.malleus.dev/temporal-g3/g1-07/ReportedEvent' must satisfy exactly one declared alternative; matched 0; Required slot 'evidence_refs' missing | change set names no source at all: REFUSED COMPOSE/MALFORMED_CHANGE_SET | sha256:a31cad5426563f337c883f6b70db6916b72c6dfc83d8a263f7319d0e4c01a678 (334174 bytes) -> same |
| g1-08 | RF-PARTIAL | UNKNOWN_REFERENCE | EXPECTED_REFUSAL_OBSERVED | REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: Target entity 'phantom:subject' does not exist |  | sha256:f7fec490d47e9785b63816be7f2a38eb224a2c90a52cec60356a7f5a61643eaf (425925 bytes) -> same |
| g1-08 | RF-MISSING-MODEL | MISSING_MODEL | EXPECTED_REFUSAL_OBSERVED | REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: Target entity 'phantom:model' does not exist | model link as a slot only: ADMITTED / | sha256:55b42114bdc3e6f284b1a5179b8c6884001eba12d96d25f5b6685f2a65146ca8 (428205 bytes) -> same |
| g1-08 | RF-MISSING-EVIDENCE | MISSING_EVIDENCE | EXPECTED_REFUSAL_OBSERVED | supersede REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: record replacement contradicts prior valid time: q-price; REFUSED CHECK/CONTENT_RULE_VIOLATED: VIOLATED: STRUCTURAL_REFUSAL: Class 'https://example.malleus.dev/temporal-g3/g1-08/Assertion' must satisfy exactly one declared alternative; matched 0; Required slot 'evidence_refs' missing |  | sha256:5eb7d4101e52f1b20409655104d0dbf1d98c99d81bc8e7c16e25b2094efa7191 (428743 bytes) -> same; sha256:5eb7d4101e52f1b20409655104d0dbf1d98c99d81bc8e7c16e25b2094efa7191 (428743 bytes) -> same |
| g1-08 | RF-UNSUPPORTED | UNSUPPORTED_SEMANTICS | EXPECTED_REFUSAL_OBSERVED | REFUSED COMPOSE/MALFORMED_CHANGE_SET: unsupported valid-time kind: RECURRING |  | sha256:0ed961a991ba23e5a39b1176896cb66822a2a3cb5607a1c4014150aaac893143 (425945 bytes) -> same |
| g1-08 | RF-MISSING-CONTRACT | MISSING_CONTRACT | EXPECTED_REFUSAL_OBSERVED | REFUSED ADMIT/STALE_BASE: change set names a different effective contract | contract named only in the record's contract_ref slot: ADMITTED / | sha256:af910b87fadbec118c7a545936d51bb2f5c1353611ecf8a0392242c011786f60 (425038 bytes) -> same |

