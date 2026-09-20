# fault-injection-02: the same 55 faults through the hardened gate

fault-injection-01 measured what Core `c95dba7b86bb61487bda9a52458e1ea47cce20ab`
refuses, exposes and lets through, on run-23's own admitted capture. Four
changes have since been made to Core in an isolated candidate. This cell runs
the same catalog again, from the same seed, against
`e7937b89917c8da7ee4a08acc22e99ad12b9985b`, and puts the two columns side by
side. Nothing in the catalog changed: same eleven constructions, same five
instances each, same faulted population bytes, trial for trial.

Not a new experiment. The harness is fault-injection-01's, with the Core
coordinate turned into an argument that defaults to the frozen pin, so the
first cell's thirty tests and its `outcomes.json` are untouched.

## Coordinates

- Core under measurement: `e7937b89917c8da7ee4a08acc22e99ad12b9985b`, exported
  with `git archive --format=tar <commit> src/malleus` from
  `/private/tmp/malleus-progressive-guidance.uxhila/repo` and put first on
  `PYTHONPATH`. That clone is where the four gate changes were made; the
  commit is `Seal OVR-000462`.
- Core compared against: `c95dba7b86bb61487bda9a52458e1ea47cce20ab` in this
  checkout, the pin run-23 itself ran on.
- Catalog: `fault-injection-01/faults.py`, seed 23, unchanged. Every trial's
  `population_sha256` equals the first cell's, which `test_rerun.py` checks
  trial by trial rather than by count.
- Runner: `paper-v4/experiment-v4/run-23/run.py`, unmodified, one process per
  trial.
- Private outputs: `private/paper-v4-fault-injection-02/`.

## The honest control comes first

The measurement is only legitimate if the unfaulted population still lands
where it landed. On the hardened Core it does, with one difference and a
known cause:

| | frozen run-23 | control on `e7937b89` |
| :-- | :-- | :-- |
| exported records | `sha256:0634e069…a286` | `sha256:0634e069…a286`, identical |
| replay receipt | `sha256:a3abceec…1eec` | `sha256:f3a014b1…1f75` |
| validated contract, differing leaves | | `/evidence/producer/sha256`, `/evidence_sha256` |

`evidence.producer.sha256` is the canonical digest of five Core source files
that `_contract_pipeline/elaborate.py` hashes into every validated contract.
It moves from `sha256:5eb3ca2b…0edc` to `sha256:683df284…d0da` because Core
moved. `evidence_sha256` is the digest of the block that carries it. Those two
leaves are the whole difference in the contract, so the receipt and every
event hash downstream of it move and nothing about what Core accepted does.
The run is refused outright if any third leaf differs; that check is in
`run_faults.py`, not in this note.

After all 55 trials the honest population was run again and returned the
control's receipt.

## The two columns

| # | class | construction | n | on `c95dba7b` | on `e7937b89` |
| :-- | :-- | :-- | --: | :-- | :-- |
| 1 | `VALUE_NOT_IN_BLOCK` | one property value replaced; locator and digest untouched | 5 | ADMITTED_INVISIBLE | ADMITTED_INVISIBLE |
| 2 | `LOCATOR_REPOINTED_STALE_DIGEST` | locator moved, digest left behind | 5 | REFUSED, `DIGEST_MISMATCH` | REFUSED, `DIGEST_MISMATCH` |
| 3 | `LOCATOR_REPOINTED_COHERENT_DIGEST` | locator and digest moved, formalizations left | 5 | ADMITTED_EXPOSED | REFUSED, `LOCATOR_NOT_DERIVED` |
| 4 | `LOCATOR_REPOINTED_COHERENT_DERIVATION` | locator, digest and formalizations moved together | 5 | ADMITTED_INVISIBLE | ADMITTED_INVISIBLE |
| 5 | `DIGEST_MISMATCH` | digest replaced with the digest of synthetic bytes | 5 | REFUSED, `DIGEST_MISMATCH` | REFUSED, `DIGEST_MISMATCH` |
| 6 | `DANGLING_ENDPOINT` | a relation endpoint pointed at an absent record | 5 | REFUSED, `DANGLING_ENDPOINT` | REFUSED, `DANGLING_ENDPOINT` |
| 7 | `TYPE_OUTSIDE_ONTOLOGY` | record type replaced with an undeclared type | 5 | REFUSED, `RECORDS_NOT_REHYDRATABLE` | REFUSED, `RECORDS_NOT_REHYDRATABLE` |
| 8 | `SLOT_OUTSIDE_ONTOLOGY` | an undeclared property added and cited | 5 | REFUSED, `RECORDS_NOT_REHYDRATABLE` | REFUSED, `RECORDS_NOT_REHYDRATABLE` |
| 9 | `DUPLICATE_RECORD_ID` | one record carried twice in its own family | 5 | REFUSED, `MALFORMED_CAPTURE` | REFUSED, `MALFORMED_CAPTURE` |
| 10 | `RECORD_WITH_NO_SOURCE_WITH_FIELDS` | a new record with one property and no source | 5 | REFUSED, `UNDERIVED_FIELD` | REFUSED, `UNDERIVED_FIELD` |
| 11 | `RECORD_WITH_NO_SOURCE_NO_FIELDS` | the same record carrying no property at all | 5 | ADMITTED_INVISIBLE | REFUSED, `UNDERIVED_RECORD` |

35 refused and 20 admitted becomes **45 refused and 10 admitted**. The rows
are rendered from the two `outcomes.json` files by `compare.py`; `test_rerun.py`
re-renders them and fails if this table disagrees.

### Ten trials moved, all in one direction

**admitted_to_refused: 10.** `b2-01`, `b2-02`, `b2-03`, `b2-04`, `b2-05`,
`gn-01`, `gn-02`, `gn-03`, `gn-04`, `gn-05`.

**refused_to_admitted: 0.** No fault the frozen gate refused is admitted by
the hardened one, and no trial changed in any other way.

The two new diagnostics, verbatim from the runner's stderr:

- `LOCATOR_NOT_DERIVED` (`b2-01`): `records cite an assertion they are not
  derived from: claim:deep-events-not-artifacts cites assertion:118, derived
  from assertion:178; a record's assertion_locator must be the locator of one
  of that record's own derivations`
- `UNDERIVED_RECORD` (`gn-01`): `records carry no derivation:
  fault:g:no_fields:01; every record needs at least one derivation naming a
  source it came from, and a record with no properties and no endpoints is not
  exempt`

Both are gaps fault-injection-01 recorded with reproducers and left alone.
Gap 2, "a record's own locator is never compared with the locators it is
derived from", is closed: the class that was ADMITTED-exposed, visible only to
a reader cross-checking the export against the trace summary, is now refused on
the admission path. Gap 4, "a record with no properties has no derivation
required of it", is closed the same way.

Each of the 45 refusals wrote a seven-event ledger with none of the four
admission events in it. Forty are a byte-exact prefix of the control's
fourteen-event ledger; the five that are not are the `SLOT_OUTSIDE_ONTOLOGY`
trials, which retain different capture bytes, exactly as in the first cell.

### What did not move

Gap 1 and gap 3 are open, and this rerun is the evidence:

- **`VALUE_NOT_IN_BLOCK` is still admitted, five for five, invisibly.** No
  mechanism on the admission path reads a property value against the sentence
  the record cites. Fact contract version 3 gives a Prolog rule the two
  predicates it would need to make that comparison, but nothing in this cell
  runs a rule: the runner's path is the structural gate, and the structural
  gate does not read values.
- **`LOCATOR_REPOINTED_COHERENT_DERIVATION` is still admitted, five for five,
  invisibly.** Moving the locator, the digest and every formalization to one
  sentence in another block leaves nothing inside the change set disagreeing
  with anything else. `LOCATOR_NOT_DERIVED` compares a cited locator with the
  record's own derivation locators, and in this construction they agree.
  Only reading the source finds it.

## What this cell does not establish

- **Change 3 is not exercised here.** `SOURCE_BINDING_REQUIRED` fires on no
  trial, because no construction in this catalog removes a binding slot. The
  liveness of that refusal is measured in `bridge-01`, on run-20, not here.
- **Change 4 is not exercised here.** No trial loads a Prolog contract; the
  fact-contract version the runner's path uses is not read at all.
- **Only run-23.** The other six populations are bridge-01's subject. This
  cell says nothing about them.
- **No effect on answers.** The table is about admission. No query and no
  review was run.
- **Nothing was changed to make a fault pass or fail.** The catalog, the
  seeds, the constructions and the runner are the first cell's.

## Inputs and outputs, by digest

| artifact | sha256 |
| :-- | :-- |
| Core under measurement | `e7937b89917c8da7ee4a08acc22e99ad12b9985b` |
| Core compared against | `c95dba7b86bb61487bda9a52458e1ea47cce20ab` |
| selected reading | `sha256:f3885c7b50292cd2dea05b540abe68464b089767e478eca74cd37149900a8a17` |
| accepted ontology | `sha256:9aa5fdcfb74dc9cad9b36b16b27e8a829b5a71ad1b2bc61892e12a2568b06d21` |
| honest population | `sha256:9d608bffe7cb1259d1f397e6d272290a5e21073744847b6d32a0994543416fd3` |
| control export records | `sha256:0634e0696a34bc2cc736f84dbeadf6b65416ebcd9f84f0e67eeb11bb9a44a286` |
| control replay receipt | `sha256:f3a014b1e347f093fd06be722b41c112705d60fbd32ffcb9e5d1aa27be501f75` |
| control ledger bytes | `sha256:3e9135031ed2f28b27914ddcbc2015633d6e529465e895a1df45d93c531a0f3d` |
| producer digest, `c95dba7b` | `sha256:5eb3ca2ba74e8cee3d8e7f5d4710ae026f728ffa5923d215a00c40716c03edcf` |
| producer digest, `e7937b89` | `sha256:683df284eaf8bb20d8872583bb2f73a9ea316b37d13f5282be934702e846d0da` |

## Reproducing

    # all 55 trials against the hardened Core
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
      paper-v4/experiment-v4/fault-injection-01/run_faults.py \
      --producer private/paper-v4-v4-run-23/producer \
      --private private/paper-v4-fault-injection-02 \
      --core-repo /private/tmp/malleus-progressive-guidance.uxhila/repo \
      --core-commit e7937b89 \
      --outcomes paper-v4/experiment-v4/fault-injection-02/outcomes.json

    # the side-by-side table
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
      paper-v4/experiment-v4/fault-injection-02/compare.py

    # the contract
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
      paper-v4/experiment-v4/fault-injection-02/test_rerun.py
