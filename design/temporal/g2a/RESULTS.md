# G2a results: Construction A over the eight G1 specimens

24 September 2026. Witness level 3 of GEDANKENEXPERIMENTS-01.md: encode,
query, decode and rebuild against an independently authored answer key. It
proves only these specimens, in this encoding, with this selector.

## What was run

```sh
export PYTHONPATH=$PWD/src:$PWD
/Users/luis/Projects/malleus-dev/.venv/bin/python design/temporal/g2a/runner.py        # 0 problems
/Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider design/temporal/g2a/test_g2a.py   # 38 passed
/Users/luis/Projects/malleus-dev/.venv/bin/python design/temporal/g1/validate_specimens.py   # 8 files, 0 failed (specimens untouched)
```

Counts, all from the runner:

- 94 queries, 100 compared answers (six queries have two branches each). 99 PASS, 1 SPECIMEN_ISSUE, 0 FAIL, 0 NOT_ENCODABLE.
- 59 forbidden answers checked against every answer of their query, branches included. 0 given.
- 12 refusals. All 12 refuse the whole attempt and leave the graph byte-identical, with the head unchanged. 11 give the specimen's category; 1 gives another category and is a SPECIMEN_ISSUE.
- 36 accepted changes, each admitted by the same admission code against the graph built from the changes before it, and each producing the same graph as the encoder.
- 162 branch-invariance answers: every query that no open choice affects was rerun under every branch of every choice with a parameter, and kept its expected answer.
- Round trip, per specimen: graph to canonical JSON, parsed back, re-serialized to identical bytes, decoded to objects equal field for field to the specimen objects, and changes equal to the specimen changes. All 100 answers identical on the decoded graph.
- Rebuild, per specimen: a fresh encode from the change list, and a second one from the decoded change list, both give byte-identical canonical JSON and the same 100 answers.
- Prefix check: every answer at position P on the full graph equals the answer on a graph built only from the changes up to P (98 answers; the two read after a refusal are excluded because they read the refused attempt).
- Queries write nothing: canonical bytes are unchanged after all queries.

Broken variants that the tests show going red: reading the final graph instead
of the prefix (P02, P03, P09, PH-K1, PH-K2 fail), a decimal lexical "5.40"
turned into "5.4" (round trip differs), a reversed PART_OF edge (ST04 fails),
model m1 given m2's members (ST05 fails), and a refused change whose valid half
is kept, either as a new position (head moves) or merged into the head (ST12
fails). Equal-valued H1 and B2 are checked to stay two records with different
basis and account.

## Findings

**SPECIMEN_ISSUE, G1-03 CA08, branch OC-03-USE-SELECTION-SCOPE[1].** The branch
expects SELECTED Q2. Its own note says this needs an explicit declared
authority record and that J1 is not that record. The specimen has no such
record, and the G1 format has no object type for one. This witness returns
AMBIGUOUS_SELECTION with candidates Q1 and Q2. The only way to reach Q2 from
this specimen is to treat J1 as the authority, which the note excludes. Either
the specimen needs an authority record (and a format type for it), or the
branch answer is conditional on a record that does not exist.

**SPECIMEN_ISSUE, G1-01 RF-OVERLAP.** Expected UNSUPPORTED_SEMANTICS. The
attempted correction r3-overlap cites src:r3 as evidence, but src:r3 is
accepted only at K3, and the attempt is made at head K2 without it. The format
cannot put src:r3 in the attempt, because `would_add_refs` names rejected
objects only. This witness refuses the whole change with UNKNOWN_REFERENCE,
graph unchanged. Diagnostic run: with src:r3 added to the same attempt, it
refuses UNSUPPORTED_SEMANTICS. RF-STALE-BASE has the same dangling src:r3, but
STALE_BASE is checked first, so its category is unaffected. The validator does
not check references of rejected objects against the attempt's head position.

No query was NOT_ENCODABLE.

## Per-query table

Every non-PASS row is explained under Findings.

| Specimen | Query | Kind | Branch | Status |
|---|---|---|---|---|
| G1-01-PRICE-HISTORY | P01 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | P02 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | P03 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | P04 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | P05 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | P06 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | P07 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | P08 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | P09 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | P10 | SELECT_APPLICABLE |  | PASS |
| G1-01-PRICE-HISTORY | PH-K0 | INSPECT_HISTORY |  | PASS |
| G1-01-PRICE-HISTORY | PH-K1 | INSPECT_HISTORY |  | PASS |
| G1-01-PRICE-HISTORY | PH-K2 | INSPECT_HISTORY |  | PASS |
| G1-01-PRICE-HISTORY | PH-K3 | INSPECT_HISTORY |  | PASS |
| G1-01-PRICE-HISTORY | PH-K3-META | INSPECT_HISTORY |  | PASS |
| G1-01-PRICE-HISTORY | PX-r1-K3 | EXACT_LOOKUP |  | PASS |
| G1-01-PRICE-HISTORY | C01 | EXPLAIN_EXECUTION |  | PASS |
| G1-01-PRICE-HISTORY | C02 | COMPARE_PREMISES |  | PASS |
| G1-01-PRICE-HISTORY | PC-NOT-COMPUTED | RESULT_FOR_SELECTION |  | PASS |
| G1-01-PRICE-HISTORY | C05 | PREPARE_INPUTS |  | PASS |
| G1-02-ORDER-PREMISES | OQ01 | RESULT_FOR_CONTEXT |  | PASS |
| G1-02-ORDER-PREMISES | OQ02 | RESULT_FOR_CONTEXT |  | PASS |
| G1-02-ORDER-PREMISES | OQ03 | RESULT_FOR_CONTEXT |  | PASS |
| G1-02-ORDER-PREMISES | OQ04 | RESULT_FOR_CONTEXT |  | PASS |
| G1-02-ORDER-PREMISES | OQ05 | RESULT_FOR_CONTEXT |  | PASS |
| G1-02-ORDER-PREMISES | OQ06 | COMPARE_PREMISES |  | PASS |
| G1-02-ORDER-PREMISES | OQ07 | EXPLAIN_EXECUTION |  | PASS |
| G1-02-ORDER-PREMISES | OQ08 | SELECT_APPLICABLE |  | PASS |
| G1-02-ORDER-PREMISES | OQ09 | SELECT_ACCOUNT |  | PASS |
| G1-02-ORDER-PREMISES | OQ10 | SELECT_ACCOUNT |  | PASS |
| G1-02-ORDER-PREMISES | OQ11 | RESULT_FOR_CONTEXT |  | PASS |
| G1-02-ORDER-PREMISES | OQ12 | RESULT_FOR_CONTEXT |  | PASS |
| G1-02-ORDER-PREMISES | OQ13 | RESULT_FOR_CONTEXT |  | PASS |
| G1-02-ORDER-PREMISES | OQ14 | INSPECT_HISTORY |  | PASS |
| G1-03-COMPETING-ACCOUNTS | CA01 | SELECT_APPLICABLE |  | PASS |
| G1-03-COMPETING-ACCOUNTS | CA02 | SELECT_APPLICABLE |  | PASS |
| G1-03-COMPETING-ACCOUNTS | CA03 | SELECT_APPLICABLE |  | PASS |
| G1-03-COMPETING-ACCOUNTS | CA04 | SELECT_APPLICABLE |  | PASS |
| G1-03-COMPETING-ACCOUNTS | CA05 | SELECT_APPLICABLE | OC-03-ASSUMPTIONS-IN-UNSCOPED[0] | PASS |
| G1-03-COMPETING-ACCOUNTS | CA05 | SELECT_APPLICABLE | OC-03-ASSUMPTIONS-IN-UNSCOPED[1] | PASS |
| G1-03-COMPETING-ACCOUNTS | CA06 | COMPARE_PREMISES |  | PASS |
| G1-03-COMPETING-ACCOUNTS | CA07 | SELECT_APPLICABLE |  | PASS |
| G1-03-COMPETING-ACCOUNTS | CA08 | SELECT_APPLICABLE | OC-03-USE-SELECTION-SCOPE[0] | PASS |
| G1-03-COMPETING-ACCOUNTS | CA08 | SELECT_APPLICABLE | OC-03-USE-SELECTION-SCOPE[1] | SPECIMEN_ISSUE |
| G1-03-COMPETING-ACCOUNTS | CA09 | INSPECT_HISTORY |  | PASS |
| G1-03-COMPETING-ACCOUNTS | CA10 | SELECT_APPLICABLE |  | PASS |
| G1-04-UNKNOWN-TIME-DIAMETER | S01 | SELECT_APPLICABLE |  | PASS |
| G1-04-UNKNOWN-TIME-DIAMETER | S02 | SELECT_APPLICABLE |  | PASS |
| G1-04-UNKNOWN-TIME-DIAMETER | S03 | SELECT_APPLICABLE |  | PASS |
| G1-04-UNKNOWN-TIME-DIAMETER | S04 | INSPECT_HISTORY |  | PASS |
| G1-04-UNKNOWN-TIME-DIAMETER | SQ-ACCOUNT-M2 | SELECT_ACCOUNT |  | PASS |
| G1-04-UNKNOWN-TIME-DIAMETER | SQ-ACCOUNT-M1 | SELECT_ACCOUNT |  | PASS |
| G1-04-UNKNOWN-TIME-DIAMETER | SQ-EXACT-m1 | EXACT_LOOKUP |  | PASS |
| G1-04-UNKNOWN-TIME-DIAMETER | C06 | PREPARE_INPUTS |  | PASS |
| G1-05-CONDITIONAL-STATEMENT | CC01 | EXACT_LOOKUP |  | PASS |
| G1-05-CONDITIONAL-STATEMENT | CC02 | EXACT_LOOKUP |  | PASS |
| G1-05-CONDITIONAL-STATEMENT | CC03 | RESULT_FOR_SELECTION |  | PASS |
| G1-05-CONDITIONAL-STATEMENT | CC04 | RESULT_FOR_SELECTION |  | PASS |
| G1-05-CONDITIONAL-STATEMENT | CC05 | PREPARE_INPUTS |  | PASS |
| G1-05-CONDITIONAL-STATEMENT | CC06 | PREPARE_INPUTS |  | PASS |
| G1-05-CONDITIONAL-STATEMENT | CC07 | PREPARE_INPUTS |  | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ01 | EXACT_LOOKUP |  | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ02 | EXACT_LOOKUP |  | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ03 | SELECT_ACCOUNT |  | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ04 | SELECT_ACCOUNT |  | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ05 | EXACT_LOOKUP |  | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ06 | INSPECT_HISTORY |  | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ07 | INSPECT_HISTORY | OC-06-FLAG-SOURCE[0] | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ07 | INSPECT_HISTORY | OC-06-FLAG-SOURCE[1] | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ08 | EXACT_LOOKUP |  | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ09 | SELECT_ACCOUNT | OC-06-SUFFICIENCY[0] | PASS |
| G1-06-ALTERNATE-JUSTIFICATION | AJ09 | SELECT_ACCOUNT | OC-06-SUFFICIENCY[1] | PASS |
| G1-07-VALVE-PERSISTENCE | VQ01 | SELECT_APPLICABLE |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ02 | INSPECT_HISTORY |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ03 | SELECT_APPLICABLE |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ04 | SELECT_APPLICABLE | OC-07-RULE-SELECTION[0] | PASS |
| G1-07-VALVE-PERSISTENCE | VQ04 | SELECT_APPLICABLE | OC-07-RULE-SELECTION[1] | PASS |
| G1-07-VALVE-PERSISTENCE | VQ05 | SELECT_APPLICABLE |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ06 | SELECT_APPLICABLE |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ07 | SELECT_APPLICABLE |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ08 | SELECT_APPLICABLE |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ09 | SELECT_APPLICABLE |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ10 | SELECT_APPLICABLE |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ11 | SELECT_APPLICABLE |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ12 | INSPECT_HISTORY |  | PASS |
| G1-07-VALVE-PERSISTENCE | VQ13 | INSPECT_HISTORY |  | PASS |
| G1-08-STORAGE-CLOSURE | ST01 | EXACT_LOOKUP |  | PASS |
| G1-08-STORAGE-CLOSURE | ST02 | EXACT_LOOKUP |  | PASS |
| G1-08-STORAGE-CLOSURE | ST03 | EXACT_LOOKUP |  | PASS |
| G1-08-STORAGE-CLOSURE | ST04 | EXACT_LOOKUP |  | PASS |
| G1-08-STORAGE-CLOSURE | ST05 | EXACT_LOOKUP |  | PASS |
| G1-08-STORAGE-CLOSURE | ST06 | EXACT_LOOKUP |  | PASS |
| G1-08-STORAGE-CLOSURE | ST07 | EXPLAIN_EXECUTION |  | PASS |
| G1-08-STORAGE-CLOSURE | ST08 | EXPLAIN_EXECUTION |  | PASS |
| G1-08-STORAGE-CLOSURE | ST09 | EXPLAIN_EXECUTION |  | PASS |
| G1-08-STORAGE-CLOSURE | ST10 | EXACT_LOOKUP |  | PASS |
| G1-08-STORAGE-CLOSURE | ST11 | EXPLAIN_EXECUTION | OC-08-WITHHELD-SCOPE[0] | PASS |
| G1-08-STORAGE-CLOSURE | ST11 | EXPLAIN_EXECUTION | OC-08-WITHHELD-SCOPE[1] | PASS |
| G1-08-STORAGE-CLOSURE | ST12 | INSPECT_HISTORY |  | PASS |
| G1-08-STORAGE-CLOSURE | ST13 | EXACT_LOOKUP |  | PASS |
0 problems

Refusals: RF-STALE-BASE STALE_BASE, RF-OVERLAP (finding above), RF-STALE-EXEC
STALE_BASE, RF-BORROWED PREMISE_MISMATCH, RF-CITED-MODEL MISSING_MODEL,
RF-STALE-REVIEW STALE_TARGET, RF-NO-EVIDENCE MISSING_EVIDENCE, RF-PARTIAL
UNKNOWN_REFERENCE, RF-MISSING-MODEL MISSING_MODEL, RF-MISSING-EVIDENCE
MISSING_EVIDENCE, RF-UNSUPPORTED UNSUPPORTED_SEMANTICS, RF-MISSING-CONTRACT
MISSING_CONTRACT.

Open choices with no parameter here, and no affected query: OC-07-RULE-ACCEPTANCE
(the witness implements "accepted first" only: naming an unaccepted rule raises),
OC-07-COMPLETENESS-AUTHORITY and OC-07-INITIAL-STATE. They were not exercised.
OC-01 was run both ways; the 20 G1-01 answers are the same under both, as its
note says. The CA08 note's cross case (use selection bound to its use, and
assumptions admitted) was also run: candidates Q1, Q2, H1, as the note says.

## Distinctions that were hard to keep, and how they were kept

**Old reads without future closure.** Every query takes the graph prefix at
`at` and replays those changes to derive versions. No record is ever modified
after it is added, so a later closure has nowhere to be stored except in a
later change, which the prefix does not contain. The prefix check above
confirms this for every answer rather than trusting the argument.

**Derived versions versus the report.** A version is one assertion as known
from one position: `version:r1@K1` is a1. The transition at K2 closes a1 and
opens a2 (r1 until 12 May); the correction at K3 closes a2 and opens c. r1's
own record still says "from 1 May, no end", so PX-r1-K3 returns the stated
period while the versions carry the closure.

**Rendering versions into the specimen's vocabulary.** Only G1-01 labels its
versions (derived_labels a1, a2, b, c). The runner renders a labelled version
as its label and any other version as its assertion id, and drops unlabelled
version rows from metadata. The query layer never reads derived_labels. This
matters because G1-03 CA09 and G1-08 ST12 list only assertions although their
interval assertions also have versions; the format can only name ids defined
in the file. The runner counts the renderings: 41 occurrences across G1-02 to
G1-08, 0 in G1-01. So those specimens compare at assertion grain, not version
grain.

**Equal value, different meaning.** H1 and B2 (800 cents, no stated time) and
Q2 and H1 (42 m3/s, same day) are separate nodes with their own basis and
account links. COMPARE_PREMISES over two premise refs is identity comparison:
two ids are two premises. That is the point of the specimen, and it is also
why that check is weak evidence on its own; the stronger evidence is CA04,
CA09, OQ14 and the forbidden answers, which read basis and account back.

**Unknown time versus no time.** NONE_STATED is stored as an applicability kind
with no dates; an open interval stores `until` as an explicit null. A dated
read of NONE_STATED returns UNRESOLVED_APPLICABILITY; a date-free read selects
it. ST01 and ST03 check the two stay apart through the round trip.

**Coherent conditions.** GROUP and MODEL members are named subgraphs, so m1 and
m2 share term nodes without sharing membership. PREPARE_INPUTS checks, in
order: an unresolved premise for a dated read, common applicability for
same-time inputs, comparability of values of one property (unit, and the
`datum` qualifier), then that all premises with role CONDITION come from one
conditional group. CC07 (two depths, two datums) fails the third check and
names the depths; CC05 (conditions from two statements) fails the fourth and
names the groups.

**An assessment about a relation.** A1 is an edge. J1's subject and D1's
premise point at A1's edge id. This is why the stdlib graph lets an edge be an
endpoint (see README.md).

**Exact old use.** An execution's input bindings are LINK edges carrying the
parameter and the selection coordinates; the selection account is a LINK edge
from the binding edge. EXPLAIN_EXECUTION re-runs the recorded selection on the
prefix at its recorded position and returns the version it reaches (C01 a1).

## Assumptions this witness adds, and where it had to choose

Each of these is research-local code, not specimen data. Luis may rule any of
them.

1. **STALE_TARGET before STALE_BASE.** SCHEMA.md names both categories and no
   precedence. RF-STALE-REVIEW (J4p, base J3p) and RF-STALE-BASE (K2, base K1)
   both have a stale base and a target touched after the base. The rule used:
   STALE_TARGET when a target was already revised or corrected at the head;
   otherwise STALE_BASE when base is behind head. A transition closing r1 does
   not make r1 a stale target. This rule reproduces both categories; it was
   chosen with the expected categories in view.
2. **Reviewer branch of OC-06-FLAG-SOURCE.** AJ06 (J3p) is not listed as affected
   by that choice and expects NOT_REQUIRED for both arguments; the reviewer
   branch of AJ07 (J4p) expects NOT_RECORDED for both, including D2, whose
   premises did not change. A per-argument reading ("no flag until a reviewer
   records one") would make AJ06 NOT_RECORDED under that branch, contradicting
   its declared independence. The reading implemented: the review unit is the
   conclusion; with no changed premise under any of its arguments nothing
   awaits review (NOT_REQUIRED); once one exists, every argument awaits a
   recorded review (NOT_RECORDED). It was chosen because it is the one reading
   consistent with both queries.
3. **State from events.** VQ03 expects the OPENED event as the unresolved
   evidence for a `state` read with no rule. The format declares no link
   between property `state` and property `event`; the witness hard-codes it,
   and hard-codes OPENED to OPEN and CLOSED to CLOSED. The rule's semantics
   stay prose in its record; the witness implements that one semantics in code
   and applies it only to subjects in the rule's scope.
4. **Plans in a history.** VQ13 reads property `plan`. A PLAN object has no
   property field; the witness answers `plan` with PLAN records about the
   subject.
5. **Membership reads.** EXACT_LOOKUP of a GROUP or MODEL returns its members
   plus RELATION edges leaving it (CC01 includes rel:p1-cites-SM). INSPECT_HISTORY
   with only a subject returns its assertions and incident relations (ST12).
   INSPECT_HISTORY with a target returns the arguments concluding it (AJ06).
6. **Model parameter mapping.** RESULT_FOR_SELECTION matches a model parameter
   to an assertion property by name (PC-NOT-COMPUTED). CC06 returns INPUTS_READY
   without checking that `h2o_content` feeds `h2o_wt_percent`: the specimen
   gives no parameter mapping, and the witness does not invent one.
7. **Correction periods.** A correction must state exactly the current period of
   its target; otherwise UNSUPPORTED_SEMANTICS (interval splitting excluded, as
   RF-OVERLAP says).
8. **Closure.** EXPLAIN_EXECUTION's closure is the execution, its model and the
   model's members, its premises, their evidence and contracts, and its
   result. EXACT_LOOKUP's is the target, its evidence and contract, and its
   members. SELECT_APPLICABLE, SELECT_ACCOUNT and INSPECT_HISTORY return
   INCOMPLETE_RECONSTRUCTION on any missing record. The computation, comparison
   and preparation kinds do not check closure at all. No specimen withholds a
   record from those kinds, so this gap is untested.
9. **Comparison.** Every key an expected answer names is compared exactly; keys
   it does not name are not asserted. `_refs` lists compare as sets (with no
   duplicates in the answer); metadata rows compare only the listed fields.

## Losses

- The rule's semantics, a CONTRACT's meaning and a MODEL's formula are stored
  as strings and not executed or parsed. Round trip preserves the bytes, not an
  executable meaning.
- LINK edges carry an `ordinal` qualifier the specimen does not have; it keeps
  list order and is stripped on decode. Payload list fields carry a count
  literal that decode checks against the links.
- Version ids exist only in query answers. They are derived on every read,
  not stored, so the canonical JSON has no version records. That is by
  design (Core, not the producer, maintains derived ends), and it means a store
  of this JSON alone cannot serve a version read without the replay code.

## What this witness cannot establish

- Core admission, Core checks, ledger integrity or replay. Admission here is a
  small research function with its own check order; a refused attempt leaving
  bytes unchanged is not Core atomicity.
- That any other encoding or backend gives these answers. G2b (relational) and
  G3 (Core composition) are separate witnesses and were not read.
- That the answers are the right meaning. They are the G1 author's answers,
  reproduced; the choices listed above were needed to reproduce some of them.
- Anything beyond these eight specimens: uncertain transition windows, interval
  splitting, retraction and withdrawal, recurrence, clock mappings, episodes,
  GE-01, GE-08, and two open reports on one account (where OC-01's branches
  would differ).
- Performance, volume or workload behaviour. The full run takes well under a
  second on these graphs (9 to 41 nodes, 7 to 73 edges); that says nothing
  about scale.
