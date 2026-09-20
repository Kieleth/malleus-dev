# Run-22's ledger queried again under harness v4.13

Run-22 is frozen and nothing in it moved. This directory holds a second query
of the same ledger under a later binder, and a comparison of the two.

## Why

Run-22 was bound by harness v4.12. That binder reached a listed subject-bearing
type two ways: `ENTITY_NO_SUBJECT`, which returns the type's records whose
subject slot is absent, and `SUBJECT`, which pairs the type with the subject
types the question's own set lists. A record of a listed type whose subject is
of an unlisted type was reached by neither. Eleven of the cell's 102 required
semantics were read UNREACHED_RECORD at review for that reason, and the review
named the cause: CQ-T4-01's set lists the claim type alone, and the question
returned the 61 subject-less claims out of 124 (E-0342).

Harness v4.13 added a fifth case kind, `SUBJECT_ANY`: one case per
subject-bearing type in the set paired with every entity type the accepted
surface declares, answered by the same row builder the typed `SUBJECT` case
uses (E-0343). Run-23 was the first cell bound under it.

A query reads a ledger and writes nothing into it, so run-22's ledger can be
queried again under the later binder and the cell reported under both. That is
all that happened here. No producer ran, the ontology was not re-accepted, the
ledger was not reopened for writing, and the evaluator's thirty type sets are
run-22's own bytes: the binder is the single difference between the two
columns below.

## What was run

Every command ran with `src/malleus` exported from the pinned Core commit
`c95dba7b86bb61487bda9a52458e1ea47cce20ab` first on `PYTHONPATH`, followed by
the repository root, as `paper-v4/run_active_tests.py:export_core` does it.
The repository's `src/` at HEAD has moved past the pin and was not used.

```
git archive c95dba7b86bb61487bda9a52458e1ea47cce20ab src/malleus | tar -x -C <tempdir>
export PYTHONPATH=<tempdir>/src:<repository root>

.venv/bin/python paper-v4/experiment-v4/run-23/bind_from_surface.py \
  --surface paper-v4/experiment-v4/run-22/ontology-run/population-surface.json \
  --contract paper-v4/experiment-v4/run-22/ontology-run/validated-contract.json \
  --type-sets paper-v4/experiment-v4/run-22/results/query-type-sets.json \
  --replay-receipt sha256:e6b025be41452c4192331cbbf7e5704ef3c344507a2c76efdc4eeb26d9fff4d5 \
  --output paper-v4/experiment-v4/run-22/rebind-v4.13/native-query-binding.json

.venv/bin/python paper-v4/experiment-v4/run-23/native_query.py \
  --ledger private/paper-v4-v4-run-22/ledger/history.jsonl \
  --binding paper-v4/experiment-v4/run-22/rebind-v4.13/native-query-binding.json \
  --results private/paper-v4-v4-run-22/rebind-v4.13

.venv/bin/python paper-v4/experiment-v4/run-22/rebind-v4.13/compare_bindings.py
```

The replay receipt passed to the binder is `replay_receipt_sha256` of
`paper-v4/experiment-v4/run-22/results/run-result.json`, and the executor read
the same digest off its own replay of the ledger: `comparison.json` records
both and they agree.

### The harness files, which are run-23's own bytes

Both were last written at commit `b06a02833c0c6359523b76deda74a5448a103420`,
the GREEN commit of harness v4.13, and the working tree has not touched them.

| file | sha256 |
| --- | --- |
| `paper-v4/experiment-v4/run-23/bind_from_surface.py` | `389856e069dacdf02748eaec0b04d2ff63ad7dee04afcda831c70e848fec9c96` |
| `paper-v4/experiment-v4/run-23/native_query.py` | `2d8befd7b37fad2bea9e30586f9a418270a07e9668ca6806bd58ff8f865bf869` |

### The inputs, all frozen and all read only

| file | sha256 |
| --- | --- |
| `paper-v4/experiment-v4/run-22/ontology-run/population-surface.json` | `206120fc7bc053664e950eaa32e8fc0c88fecc43d0f3feaaa261958cdf4a8a56` |
| `paper-v4/experiment-v4/run-22/ontology-run/validated-contract.json` | `76de7c5cb65d673de3685bd3d721f9db2657d6d70693e772a2708e9410270063` |
| `paper-v4/experiment-v4/run-22/results/query-type-sets.json` | `afeafe4f96661d83127b2f391ea869cdc871fdc19f2423994f4772b185f7d526` |
| `private/paper-v4-v4-run-22/ledger/history.jsonl` | `1bbd9876c797f46732ef642d8e898c38a135ad1563b5775b10604b8f178f314f` |

The ledger's digest was taken before and after the query and is the same
digest; that is the evidence that the re-query wrote nothing into it.

## What is here, and what is private

Public, this directory:

- `native-query-binding.json`, the v4.13 binding, schema
  `malleus.paper-v4.native-query-binding/v6`.
- `comparison.json`, every figure below.
- `compare_bindings.py`, which writes `comparison.json`. No count in this file
  was typed by hand.
- this README.

Private, `private/paper-v4-v4-run-22/rebind-v4.13/`:

- `query-result.json`, the rows, withheld because projected row fields quote
  the reading.
- `trace-summary.json`, provenance for every witness the rows use.

## Leak check on the public files

The rule the cells use: no public file may share a 60-character normalized run
with any block of `private/paper-v4-text-layer/selected-reading.json`
(`paper-v4/experiment-v4/run-23/results/withheld-artifacts.json`, method
`SHARED_NORMALIZED_CHARACTER_RUN_AGAINST_EVERY_READING_BLOCK`, normalization
`UNICODE_WHITESPACE_COLLAPSED_TO_SINGLE_SPACE`, ladder 40/60/80/120/200/320).
The check was run with the repository's own implementation,
`paper-v4/evaluation-v4/sample/sample_common.py` (`normalized`, `runs`,
`reading_run_index`), over every public file written by this task: the four
files above, the four of `paper-v4/evaluation-v4/run-22-v413/`, and the three
of the CQ-C-03 v3.1 derivation. Every one measures **0** on the ladder, so
none is refused. That implementation file was untracked at the time of this
check, another session's work in flight; it was read and not modified, and the
method is stated above in full so the measurement does not depend on it.

The same check run over `private/paper-v4-v4-run-22/rebind-v4.13/query-result.json`
returns 120, which is why the rows stay private, and over the private
`trace-summary.json` returns 0. That file is kept private not because it
carries text but because the executor writes it into the private results
directory and nothing copies it out; run-23's equivalent is public at 0.

## The two columns

The v4.12 column is run-22's frozen binding and its frozen query result. The
v4.13 column is this directory's binding and the query it produced. Same
ledger head, same graph state digest, same replay receipt, same population
surface; `compare_bindings.py` refuses if any of those four differ.

Cases emitted by the binder:

| kind | v4.12 | v4.13 |
| --- | ---: | ---: |
| ENTITY | 65 | 65 |
| ENTITY_NO_SUBJECT | 65 | 65 |
| RELATION | 3190 | 3190 |
| SUBJECT | 297 | 297 |
| SUBJECT_ANY | 0 | 1300 |
| total | 3617 | 4917 |

`cases_sha256` v4.12 `sha256:9dd3c2a7071f8d6900c353eeef363252d501897998bb911a859d24115d4850ef`,
v4.13 `sha256:709c5b8e1b26d463eec5570acf7c86b20d0626183593dc5f6b1d2ae1ba556b92`.

Rows by kind, and the cell totals:

| | v4.12 | v4.13 |
| --- | ---: | ---: |
| ENTITY rows | 4140 | 4140 |
| SUBJECT rows | 1169 | 2715 |
| RELATION rows | 105 | 105 |
| rows, all questions | 5414 | 6960 |
| witnesses traced | 449 | 457 |

Nothing the v4.12 binding returned was lost: the four carried case kinds emit
the same cases, and every entity and relation row count is unmoved. The whole
difference is `SUBJECT` rows, 1,169 to 2,715.

Per question. "Rows" is one row per distinct witness in that question.
"Witness ids" is the number of distinct record ids the question's rows name,
which is larger than the row count when a row's subject or a relation's
endpoint is not itself a row of that question; summed and deduplicated over
the cell it is `witnesses_traced` in the trace summary, and
`compare_bindings.py` refuses if it is not.

| question | rows v4.12 | rows v4.13 | rows Δ | witness ids v4.12 | witness ids v4.13 | Δ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CQ-C-01 | 153 | 270 | +117 | 153 | 302 | +149 |
| CQ-C-02 | 144 | 264 | +120 | 144 | 298 | +154 |
| CQ-C-03 | 385 | 400 | +15 | 385 | 406 | +21 |
| CQ-C-04 | 85 | 142 | +57 | 85 | 160 | +75 |
| CQ-C-05 | 309 | 322 | +13 | 309 | 327 | +18 |
| CQ-T1-01 | 85 | 142 | +57 | 85 | 160 | +75 |
| CQ-T1-02 | 85 | 142 | +57 | 85 | 160 | +75 |
| CQ-T1-03 | 147 | 209 | +62 | 147 | 238 | +91 |
| CQ-T1-04 | 147 | 209 | +62 | 147 | 238 | +91 |
| CQ-T1-05 | 83 | 140 | +57 | 83 | 158 | +75 |
| CQ-T2-01 | 178 | 185 | +7 | 178 | 190 | +12 |
| CQ-T2-02 | 75 | 137 | +62 | 75 | 166 | +91 |
| CQ-T2-03 | 299 | 315 | +16 | 299 | 322 | +23 |
| CQ-T2-04 | 252 | 261 | +9 | 252 | 267 | +15 |
| CQ-T2-05 | 24 | 24 | 0 | 24 | 24 | 0 |
| CQ-T3-01 | 300 | 316 | +16 | 300 | 323 | +23 |
| CQ-T3-02 | 309 | 322 | +13 | 309 | 327 | +18 |
| CQ-T3-03 | 309 | 322 | +13 | 309 | 327 | +18 |
| CQ-T3-04 | 149 | 269 | +120 | 149 | 303 | +154 |
| CQ-T3-05 | 148 | 268 | +120 | 148 | 302 | +154 |
| CQ-T4-01 | 61 | 124 | +63 | 61 | 154 | +93 |
| CQ-T4-02 | 61 | 124 | +63 | 61 | 154 | +93 |
| CQ-T4-03 | 66 | 129 | +63 | 66 | 159 | +93 |
| CQ-T4-04 | 299 | 315 | +16 | 299 | 322 | +23 |
| CQ-T4-05 | 62 | 125 | +63 | 62 | 155 | +93 |
| CQ-T5-01 | 143 | 263 | +120 | 143 | 297 | +154 |
| CQ-T5-02 | 309 | 322 | +13 | 309 | 327 | +18 |
| CQ-T5-03 | 300 | 316 | +16 | 300 | 323 | +23 |
| CQ-T5-04 | 148 | 268 | +120 | 148 | 302 | +154 |
| CQ-T5-05 | 299 | 315 | +16 | 299 | 322 | +23 |

Twenty-nine of the thirty questions return more rows; none returns fewer.
CQ-T2-05 is unmoved at 24. CQ-T4-01, the question whose review named the
defect, goes from 61 rows to 124, which is the 124 claims the export carries.

What this is not: whether the extra rows answer the questions is the review's
to say, and the review has not run. Nothing here is a coverage figure, a
semantics count or a responsiveness label, and nothing here is ratified.

## The review package

`paper-v4/evaluation-v4/run-22-v413/` holds the protocol v3 package for this
query, written by its own copy of run-23's builder at `--stage open` and then
`--stage freeze`. It binds `paper-v4/experiment-v4/competency-questions-v3.json`,
the file run-22 bound. The cell's identity comes from run-22's frozen public
record (accepted ontology digest, ledger head, replay receipt, population trace
summary); the query materials are this rebind's. The manifest validates under
`review.validate_review_input_manifest` against `review-protocol-v3.json`:
30 questions, 6,960 rows, 457 witnesses, manifest
`sha256:3103248045b7bb89725528bb30715e5148b7863516213aa8605dada928756196`.

Two deviations from run-23's procedure, both recorded here because the
validator would not take them as fields:

1. `run_id` in the manifest is `run-22`, not a variant. The v3 manifest takes
   exactly twelve keys and `review.py` refuses a thirteenth, so there is no
   field in which to say "this is the v4.13 rebind". The package directory is
   named `run-22-v413`, the builder's docstring says what it is, and the
   instantiated task and blank record carry the rebind paths, which is the
   smallest deviation available.
2. `query_trace_summary` is declared `PRIVATE` where run-23 declared it
   `PUBLIC`, because this rebind's trace summary lives in the private results
   directory. It measures 0 on the leak ladder either way.

Two debts, neither of them acted on here. Nothing written by this task is
registered in `paper-v4/active-test-manifest.json`, so
`paper-v4/evaluation-v4/test_derive_cq_c_03_v31.py` is not in the gate; it was
run directly and is 8 passed. And the instantiated review task names the cell
`run-22-v413` in its paths but carries no sentence saying that the query is the
v4.13 rebind of a v4.12 cell; whoever dispatches the review should say so.

## What is not claimed

No review has run against this query. The eleven UNREACHED_RECORD absences of
E-0342 are not shown here to be resolved: what is shown is that the records
those absences named are now returned. Whether the returned rows answer the
questions is the reviewer's judgement, and whether any of this is evidence is
Luis's.
