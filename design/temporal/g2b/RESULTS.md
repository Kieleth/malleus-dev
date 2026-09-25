# G2b: the G1 specimens in a relational store

24 September 2026. Construction B of [STORAGE-FLOWS-01.md](../STORAGE-FLOWS-01.md):
a relational projection of the same logical graph, in SQLite through the Python
standard library. Evidence level 3 of GEDANKENEXPERIMENTS-01.md, a storage witness.

Role: a `CONFORMANCE_FIXTURE` run under the `OPTIONAL_PROFILE` for temporal semantic
history. Nothing here is Core, a public schema or a storage decision. No file outside
`design/temporal/g2b/` was changed. Malleus graph classes are not imported.

## What was run

```sh
export PYTHONPATH=$PWD/src:$PWD
/Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider design/temporal/g2b/test_g2b.py
/Users/luis/Projects/malleus-dev/.venv/bin/python design/temporal/g2b/runner.py
```

Result on this branch: 40 passed. Python 3.12.9, SQLite 3.45.3. Databases are
created in temporary directories and deleted.

| Count | Value |
|---|---|
| Specimens | 8 |
| Authored queries | 94 |
| Query runs (branches and branch combinations) | 169 |
| PASS runs | 167 |
| SPECIMEN_ISSUE runs | 2 (AJ06, both combinations with OC-06-FLAG-SOURCE branch 2) |
| FAIL, NOT_ENCODABLE | 0, 0 |
| Forbidden entries / checks against actual answers | 56 / 99, no match, none undiscriminated |
| Refusals attempted | 12, all with the authored category |
| Round trip, rebuild, queries write nothing | holds for all 8 |

## Files

| File | Role |
|---|---|
| `schema.sql` | 27 STRICT tables, every foreign key deferred |
| `store.py` | connection with `foreign_keys=ON` verified, encoder, admission checks, refused attempts, decoder |
| `queries.py` | SQL for every query kind; Python assembles answers |
| `runner.py` | runs every query, branch, forbidden check, refusal, round trip and rebuild |
| `test_g2b.py` | pytest over the runner plus negative controls |

## How it works

**Encoding.** Each accepted change is one SQL transaction: insert the `change` row,
its targets, its records, then derive `temporal_effect` rows from the declared change
kind (`TRANSITION`, `CORRECTION` and `REASSESSMENT` end the named target's open
version; a transition re-opens it ending where the new account starts). Then the
admission checks run as SQL, `PRAGMA foreign_key_check` names missing parents, and
the transaction commits or rolls back. The encoder reads `objects` and `changes`
only; never queries, expected answers or derived labels.

**Reading at a position.** Every read takes a knowledge position. A record is visible
when `added_seq <= :at`. Applicability versions ("cells") and their knowledge ends
are computed from `temporal_effect` rows with `seq <= :at`. Effects are append-only,
so no older row is ever updated with a later closure.

**Derived labels.** The answer key names the price cells a1, a2, b, c. The witness
derives cells by (assertion, opening position) and uses `derived_labels` only to name
them in outputs. The derived cells at K3 were also compared with the answer key's
`cells_at_K3` on assertion, value, valid_from, valid_until, knowledge_from and
knowledge_until: no difference. The key's `basis` lists were not compared; the
witness does not compute them.

**Queries write nothing.** Queries run on `mode=ro` connections. A write on such a
connection raises (tested). Row content and file digest are compared before and after
all queries.

**Branches.** A query tied to an open choice runs once per branch, other choices at
their first branch. Every other query runs under every combination of the specimen's
query-affecting choices, which tests the specimen's claim that its answer does not
depend on them.

**Refusals.** The store is built up to the refusal's `head`, then the attempt runs as
one transaction and is rolled back. Row-for-row content and the database file's
sha256 were identical before and after for all 12, the head stayed at `head_after`,
and no `would_add_refs` id reached `record`. This shows a SQLite transaction rolled
back. It is not proof of Core admission atomicity.

## Per-specimen, per-query results

| Specimen | Query | Kind | Branch runs | Status |
|---|---|---|---|---|
| g1-01 | P01 to P10 | SELECT_APPLICABLE | single run each | PASS (10) |
| g1-01 | PH-K0, PH-K1, PH-K2, PH-K3, PH-K3-META | INSPECT_HISTORY | single run each | PASS (5) |
| g1-01 | PX-r1-K3 | EXACT_LOOKUP | single run | PASS |
| g1-01 | C01 | EXPLAIN_EXECUTION | single run | PASS |
| g1-01 | C02 | COMPARE_PREMISES | single run | PASS |
| g1-01 | PC-NOT-COMPUTED | RESULT_FOR_SELECTION | single run | PASS |
| g1-01 | C05 | PREPARE_INPUTS | single run | PASS |
| g1-02 | OQ01 to OQ05, OQ11 to OQ13 | RESULT_FOR_CONTEXT | single run each | PASS (8) |
| g1-02 | OQ06 | COMPARE_PREMISES | single run | PASS |
| g1-02 | OQ07 | EXPLAIN_EXECUTION | single run | PASS |
| g1-02 | OQ08 | SELECT_APPLICABLE | single run | PASS |
| g1-02 | OQ09, OQ10 | SELECT_ACCOUNT | single run each | PASS (2) |
| g1-02 | OQ14 | INSPECT_HISTORY | single run | PASS |
| g1-03 | CA01, CA02, CA03, CA04, CA07, CA10 | SELECT_APPLICABLE | 4 runs each, every branch combination | PASS (24) |
| g1-03 | CA05 | SELECT_APPLICABLE | OC-03-ASSUMPTIONS-IN-UNSCOPED 0: PASS; 1: PASS | PASS |
| g1-03 | CA06 | COMPARE_PREMISES | 4 runs | PASS |
| g1-03 | CA08 | SELECT_APPLICABLE | OC-03-USE-SELECTION-SCOPE 0: PASS; 1: PASS (see F3) | PASS |
| g1-03 | CA09 | INSPECT_HISTORY | 4 runs | PASS |
| g1-04 | S01, S02, S03 | SELECT_APPLICABLE | single run each | PASS (3) |
| g1-04 | S04 | INSPECT_HISTORY | single run | PASS |
| g1-04 | SQ-ACCOUNT-M2, SQ-ACCOUNT-M1 | SELECT_ACCOUNT | single run each | PASS (2) |
| g1-04 | SQ-EXACT-m1 | EXACT_LOOKUP | single run | PASS |
| g1-04 | C06 | PREPARE_INPUTS | single run | PASS |
| g1-05 | CC01, CC02 | EXACT_LOOKUP | single run each | PASS (2) |
| g1-05 | CC03, CC04 | RESULT_FOR_SELECTION | single run each | PASS (2) |
| g1-05 | CC05, CC06, CC07 | PREPARE_INPUTS | single run each | PASS (3) |
| g1-06 | AJ01, AJ02, AJ05, AJ08 | EXACT_LOOKUP | 4 runs each | PASS (16) |
| g1-06 | AJ03, AJ04 | SELECT_ACCOUNT | 4 runs each | PASS (8) |
| g1-06 | AJ06 | INSPECT_HISTORY | base: PASS; SUFFICIENCY 1: PASS; FLAG-SOURCE 1: SPECIMEN_ISSUE; FLAG-SOURCE 1 with SUFFICIENCY 1: SPECIMEN_ISSUE | PASS/SPECIMEN_ISSUE |
| g1-06 | AJ07 | INSPECT_HISTORY | OC-06-FLAG-SOURCE 0: PASS; 1: PASS | PASS |
| g1-06 | AJ09 | SELECT_ACCOUNT | OC-06-SUFFICIENCY 0: PASS; 1: PASS | PASS |
| g1-07 | VQ01, VQ03, VQ05 to VQ11 | SELECT_APPLICABLE | 2 runs each | PASS (18) |
| g1-07 | VQ04 | SELECT_APPLICABLE | OC-07-RULE-SELECTION 0: PASS; 1: PASS | PASS |
| g1-07 | VQ02, VQ12, VQ13 | INSPECT_HISTORY | 2 runs each | PASS (6) |
| g1-08 | ST01 to ST06, ST10, ST13 | EXACT_LOOKUP | 2 runs each | PASS (16) |
| g1-08 | ST07, ST08, ST09 | EXPLAIN_EXECUTION | 2 runs each | PASS (6) |
| g1-08 | ST11 | EXPLAIN_EXECUTION | OC-08-WITHHELD-SCOPE 0: PASS; 1: PASS | PASS |
| g1-08 | ST12 | INSPECT_HISTORY | 2 runs | PASS |

`runner.py` prints the same table one row per query.

Refusals, all PASS with rows and file bytes unchanged:

| Refusal | Expected | Got | Also detected |
|---|---|---|---|
| RF-STALE-BASE | STALE_BASE | STALE_BASE | UNSUPPORTED_SEMANTICS, MISSING_EVIDENCE |
| RF-OVERLAP | UNSUPPORTED_SEMANTICS | UNSUPPORTED_SEMANTICS | MISSING_EVIDENCE (F2) |
| RF-STALE-EXEC | STALE_BASE | STALE_BASE | PREMISE_MISMATCH |
| RF-BORROWED | PREMISE_MISMATCH | PREMISE_MISMATCH | |
| RF-CITED-MODEL | MISSING_MODEL | MISSING_MODEL | |
| RF-STALE-REVIEW | STALE_TARGET | STALE_TARGET | STALE_BASE |
| RF-NO-EVIDENCE | MISSING_EVIDENCE | MISSING_EVIDENCE | |
| RF-PARTIAL | UNKNOWN_REFERENCE | UNKNOWN_REFERENCE | |
| RF-MISSING-MODEL | MISSING_MODEL | MISSING_MODEL | |
| RF-MISSING-EVIDENCE | MISSING_EVIDENCE | MISSING_EVIDENCE | |
| RF-UNSUPPORTED | UNSUPPORTED_SEMANTICS | UNSUPPORTED_SEMANTICS | |
| RF-MISSING-CONTRACT | MISSING_CONTRACT | MISSING_CONTRACT | |

## Findings

**F1, SPECIMEN_ISSUE, AJ06.** AJ06 has a fixed expected answer (D1 and D2
`NOT_REQUIRED` at J3p) and is not tied to OC-06-FLAG-SOURCE. Under that choice's
second branch, "recorded by a reviewer; none recorded yet", the reader has no flag to
report, so it returns `NOT_RECORDED` for both. AJ07's own branch 2 answer gives D2
`NOT_RECORDED` although D2 has no changed premise, which is the same rule. So AJ06
depends on the choice. One reading would reconcile both: `NOT_REQUIRED` while no
premise of any argument for the conclusion has changed, `NOT_RECORDED` once one has.
The witness does not implement that reading, because the specimen does not state it.
Options: tie AJ06 to OC-06-FLAG-SOURCE with per-branch answers, or state the
reconciling rule in branch 2.

**F2, RF-OVERLAP has a second cause.** Its rejected object `r3-overlap` cites
`src:r3`, which is accepted only at K3. At head K2 that is a missing evidence
reference as well as an overlap. The witness reports `UNSUPPORTED_SEMANTICS` because
its precedence puts semantic checks before reference checks. With references first it
would report `MISSING_EVIDENCE`. RF-STALE-BASE cites `src:r3` too; staleness masks it.
Option: add `src:r3` to the attempt, or accept that the precedence decides.

**F3, CA08 branch 2 needs an input outside the ledger.** The branch answer (SELECTED
Q2) needs a declared default authority. The specimen's note says J1 is not that
record, and no other record is one. The witness passes the authority
(`ctx:flood-model`) as a runner parameter. The PASS shows the store can apply a
declared authority; it does not show the authority was declared.

**F4, refusals carry no change kind.** The format gives `category` but not `kind` for
an attempt. The witness infers one from the rejected objects (`corrects_ref` gives
CORRECTION, `revises_ref` REASSESSMENT, an EXECUTION gives EXECUTION_RECORD, else
REPORT). This affects no accepted state, since every attempt rolls back. It departs
from "the kind is declared input, never inferred".

**F5, persistence is hard-coded.** `RULE.semantics` is prose. The witness stores it and
cannot execute it. The step function (OPENED gives OPEN, CLOSED gives CLOSED, latest
event at or before the time wins, instant included) is fixed SQL, applied only when
the named or default rule is accepted and has the subject in scope. The format also
declares no link between property `state` and property `event`, and none for the
`plan` pseudo-property in VQ13; both are hard-coded.

**F6, refusal precedence and STALE_TARGET are the witness's own.** The specimens name
one category per attempt and several attempts violate more than one check. Order
used: STALE_TARGET, STALE_BASE, UNSUPPORTED_SEMANTICS, MISSING_CONTRACT, MISSING_MODEL,
UNKNOWN_REFERENCE, MISSING_EVIDENCE, PREMISE_MISMATCH. STALE_TARGET means a named
target has no open applicability version at the head. That separates RF-STALE-REVIEW
(J1 already revised) from RF-STALE-BASE (r1 still open, re-opened by the transition).
A definition based on "a later change named the same target" would classify
RF-STALE-BASE as STALE_TARGET, against the specimen.

**F7, bases of accepted changes.** Accepted changes record no base. The witness
assumes each was prepared against the preceding head.

**F8, what a withheld artifact leaves behind.** SCHEMA.md says withheld objects are
"made unavailable before a rebuild" but not what remains. The witness keeps the id
and type from the ledger and drops the payload, for SOURCE, MODEL and CONTRACT only.
Withholding any other type raises `NotEncodable`. The OC-08 branches then differ only
in whether the closure of the read or the whole store is checked.

**F9, PREPARE_INPUTS coherence rules are the witness's.** Same-property premises with
a different `datum` qualifier or unit conflict (CC07). Group membership is checked
only when a model is named, because one execution takes one coherent group (CC05,
CC06). The datum check runs first. The specimens state neither rule nor the order.

**F10, some PASS results discriminate little.** OQ06 and CA06 compare two ids; any
id-keyed store passes. CC03 and CC04 pass because no execution exists at all. ST13
reads a result a refused attempt never touched. The control test below shows that a
key on subject, property, value and times would merge the premises OQ06 and CA06
compare.

**F11, witness vocabulary in answers.** Answers carry keys the specimens do not assert
(`differences`, `executions_considered`, `domain_time` values `STATED` and `MIXED`,
per-row `account_ref` and `applicability_kind`). Comparison asserts only the expected
keys; forbidden checks report NOT_DISCRIMINATED when a listed field is absent, and
none was.

## Distinctions that needed care

| Distinction | How the schema keeps it | Checked by |
|---|---|---|
| Equal value, different claim | Assertion key is the id alone; value, basis, account and times are payload | OQ06, CA04, CA06; control: grouping by subject, property, value and times merges B2 with H1 (g1-02) and Q2 with H1 (g1-03) |
| Lexical form and datatype | Datatype, lexical, unit in TEXT columns of STRICT tables | ST01, ST02; control: a NUMERIC column turns `0750` into 750 and `5.40` into 5.4 |
| Open end, unstated time, instant | `app_kind` with a CHECK on the shape; `until` NULL only inside INTERVAL | ST01, ST03, S02, S03, VQ09, VQ10 |
| No future closure in old reads | Append-only `temporal_effect`; knowledge ends bounded by `:at` | PH-K1, P02, VQ06; control: dropping the bound makes PH-K1 return the forbidden K2 end |
| Report kept as stated | Assertion rows are never updated; closure lives in effects | PX-r1-K3 |
| Correction, transition, reassessment | Effects follow the declared change kind and `target_refs` | P03 to P10, S03, AJ04, AJ05 |
| Edge direction | `relation.from_id`, `relation.to_id` | ST04 |
| Shared terms, separate models | `membership` keyed by (graph, member) | ST05, ST06 |
| Coherent conditions | `claim_group` plus `membership`; datum as qualifier | CC01, CC02, CC05, CC07 |
| Exact old use | Bindings keep the exact assertion and its selection coordinates; the selection is re-run at its own position | C01, OQ07, ST07 |
| Cited name is not a model | `execution.model_id` references `model`, not `record` | RF-CITED-MODEL |
| No partial write | One transaction per change, deferred keys, rollback | RF-PARTIAL; a probe shows `q-weight` alone is admissible |
| Explicit empty list | `list_field` records present optional collections | C1's `evidence_refs: []` round-trips |
| Foreign keys per connection | `store.connect` sets and reads back `PRAGMA foreign_keys` | test: a raw connection reports 0 |

## Round trip and rebuild

`store.decode` turns the database back into the G1 object format and the ordered
changes. For all 8 specimens the decoded graph equals the specimen's objects and
changes, compared per id with key order ignored: ids, types, typed literals,
qualifiers, direction, membership, bindings, evidence order, notes and contract
references. Then every database file was deleted, the store rebuilt from the decoded
change list alone, all 169 runs repeated and the result decoded again. Answers and
decoded graph were identical.

## Losses

- None inside accepted objects of these 8 specimens.
- Not encoded, because they are not ledger content: queries, expected answers,
  forbidden answers, refusals, open choices, origin, reused files, derived labels.
- Rejected objects are never stored.
- Order of the specimen's `objects` array: decoding returns change order; comparison
  is per id.
- Cell provenance lists (`basis` in the answer key's cells) are not computed.
- A withheld artifact keeps only id and type (F8).
- Rule prose and assumptions are stored as text, not executable (F5).
- No table for reviewer flags; OC-06 branch 2 therefore always reads `NOT_RECORDED`.
- A SOURCE `pointer` must be a string; anything else raises `NotEncodable`. No
  specimen uses one.

## Rows per table, per specimen

| Table | g1-01 | g1-02 | g1-03 | g1-04 | g1-05 | g1-06 | g1-07 | g1-08 |
|---|---|---|---|---|---|---|---|---|
| argument | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 |
| assertion | 3 | 7 | 4 | 2 | 7 | 6 | 2 | 3 |
| binding | 1 | 34 | 1 | 0 | 0 | 0 | 0 | 2 |
| change | 6 | 11 | 5 | 3 | 4 | 5 | 5 | 5 |
| change_target | 2 | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| claim_group | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 |
| context | 0 | 4 | 1 | 0 | 0 | 0 | 0 | 0 |
| context_basis | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| contract | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| evidence | 3 | 7 | 4 | 2 | 10 | 6 | 3 | 4 |
| execution | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 1 |
| list_field | 0 | 0 | 1 | 0 | 10 | 3 | 0 | 3 |
| membership | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 5 |
| model | 1 | 2 | 0 | 0 | 1 | 0 | 0 | 2 |
| model_parameter | 1 | 9 | 0 | 0 | 3 | 0 | 0 | 5 |
| named | 2 | 5 | 4 | 2 | 3 | 3 | 2 | 5 |
| plan | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| premise | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 |
| qualifier | 0 | 0 | 0 | 0 | 11 | 3 | 0 | 0 |
| record | 11 | 30 | 13 | 6 | 16 | 15 | 9 | 15 |
| relation | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
| result | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 1 |
| rule | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| rule_assumption | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| rule_scope | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| source | 3 | 4 | 4 | 2 | 2 | 3 | 3 | 1 |
| temporal_effect | 6 | 8 | 4 | 3 | 7 | 7 | 2 | 3 |
| total | 41 | 130 | 42 | 21 | 84 | 59 | 31 | 57 |

27 tables is more than the brief's seven roles. Most are one-to-many children
(parameters, premises, scope, assumptions) that a JSON column would absorb at the
cost of SQL joins and foreign keys on their members. g1-02's 34 binding rows are its
four contexts and four executions each repeating their premises; nothing is shared.

## Open choices with one branch implemented

These affect no query, so only one branch exists in code: OC-01 (the transition names
its target), OC-05 (membership always returned), OC-07-RULE-ACCEPTANCE (a named rule
not accepted at the read position raises), OC-07-INITIAL-STATE (no initial state),
OC-07-COMPLETENESS-AUTHORITY (not modelled; assumptions are text).

## What this cannot establish

- Core admission, Core atomicity or Core replay. The refusals are SQLite checks the
  witness wrote to reach the authored categories; a rolled-back transaction is not
  Core admission atomicity.
- That the answers are the right meaning. They match an authored key; F1 to F9 list
  where the witness supplied a rule the key did not state.
- Replaceability. That needs the other G2 witnesses compared on the same suite.
- Other specimens or general temporal behaviour: interval splitting, uncertain
  transition windows, retraction, recurrence, two open reports in one account,
  clock mappings, concurrent writers, crash recovery.
- Performance, volume or workload behaviour. Sizes above are row counts of eight tiny
  specimens.
