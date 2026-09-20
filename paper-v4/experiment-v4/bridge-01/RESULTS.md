# bridge-01: the seven frozen populations through the hardened gate

The paper's seven model-produced populations were admitted on Core
`c95dba7b86bb61487bda9a52458e1ea47cce20ab`. Four changes have since been made
to Core in an isolated candidate, three of them new refusals on the population
admission path. The question this cell answers is whether the seven still
admit, and if they do, whether what came back is the same graph.

Each cell is replayed through its own unmodified `run-NN/run.py`, with
`src/malleus` exported by `git archive` from the named commit first on
`PYTHONPATH`. Every other argument is read back out of that cell's own frozen
record rather than written down here: the source closure and the reading by
digest, the population by the capture digest it canonicalizes to, the capture
and plan identifiers from `run-result.json`, the source and artifact
identifiers from the cell's own ledger. run-25 populated run-23's ontology
from `inputs/`, not `work/`, and is resolved by that rule with no exception
written for it.

Nothing under `private/paper-v4-v4-run-NN/` is opened for writing. The files
the runner reads are copied out first and the copies are what it is given.

## Coordinates

- Frozen Core: `c95dba7b86bb61487bda9a52458e1ea47cce20ab`, in this checkout.
- Candidate Core: `e7937b89917c8da7ee4a08acc22e99ad12b9985b`, in
  `/private/tmp/malleus-progressive-guidance.uxhila/repo`, the clone where
  `UNDERIVED_RECORD`, `LOCATOR_NOT_DERIVED`, `SOURCE_BINDING_REQUIRED` and
  fact contract version 3 were added.
- Private outputs: `private/paper-v4-bridge-01/`.

## The control: the harness reproduces all seven before anything is measured

Replayed at the frozen coordinate, each of the seven gives back its own
receipt, export, trace summary, plan, census **and ledger, byte for byte**.
Until that holds a difference at the candidate coordinate could be the
harness rather than Core. It holds for all seven, so it is Core.

## The seven cells on `e7937b89`

All seven admit. In every one the exported records, the trace summary, the
population plan and the census are byte-identical to the frozen ones, and the
graph counts are unchanged. The replay receipt and the ledger move, and the
validated contract they hang off differs at exactly two leaves in all seven:
`/evidence/producer/sha256` and `/evidence_sha256`.

| cell | outcome | byte identity | contract difference |
| :-- | :-- | :-- | :-- |
| `run-20` | ADMITTED | export, trace, plan, census identical; receipt `6042d490…` -> `9d92d7bb…` | producer digest only |
| `run-21` | ADMITTED | export, trace, plan, census identical; receipt `2cab922f…` -> `78275d70…` | producer digest only |
| `run-22` | ADMITTED | export, trace, plan, census identical; receipt `e6b025be…` -> `5c01aafa…` | producer digest only |
| `run-23` | ADMITTED | export, trace, plan, census identical; receipt `a3abceec…` -> `f3a014b1…` | producer digest only |
| `run-24` | ADMITTED | export, trace, plan, census identical; receipt `23ec9d8a…` -> `024e1fbe…` | producer digest only |
| `run-25` | ADMITTED | export, trace, plan, census identical; receipt `e6febc38…` -> `2915f85d…` | producer digest only |
| `run-26` | ADMITTED | export, trace, plan, census identical; receipt `e7271cb7…` -> `9d9b5b9e…` | producer digest only |

### The producer digest, before and after

| | sha256 |
| :-- | :-- |
| on `c95dba7b` | `sha256:5eb3ca2ba74e8cee3d8e7f5d4710ae026f728ffa5923d215a00c40716c03edcf` |
| on `e7937b89` | `sha256:683df284eaf8bb20d8872583bb2f73a9ea316b37d13f5282be934702e846d0da` |

`_contract_pipeline/elaborate.py` hashes five Core source files
(`_contract_compiler.py`, `_contract_pipeline/__init__.py`, `elaborate.py`,
`model.py`, `view.py`) into every validated contract as `evidence.producer`.
Three of the five changed between the two commits, so the digest moves, the
evidence block that carries it digests differently, the contract identity
follows, and the receipt and every event hash after it follow that. The value
above is recomputed from each Core export's own bytes and checked against the
digest each frozen ledger independently declares, so it is not taken on the
word of the artifact under question.

Nothing else in the contract moves. Not a fact, not a slot, not an annotation,
not the validated fact set digest.

## Seven admissions are not evidence unless the gate can refuse

A gate that fires on nothing and a gate that is never reached produce the same
table. One probe separates them, on `run-20` and on the construction none of
fault-injection-01's eleven classes builds: one record keeps its
`assertion_locator` and loses its `statement_sha256`, and the assertion that
formalized that slot drops that entry with it. The same population file, digest
for digest, goes through both Cores.

| coordinate | outcome | diagnostic |
| :-- | :-- | :-- |
| `c95dba7b` | ADMITTED | - |
| `e7937b89` | REFUSED | `SOURCE_BINDING_REQUIRED`, naming `claim:axis-relocating` |

Verbatim: `records do not bind the assertion behind them:
claim:axis-relocating of type Claim does not set statement_sha256; under the
source-assertion profile a record whose type declares assertion_locator must
set assertion_locator and statement_sha256`.

So the reading of the seven-row table is that the new gate is live on this path
and the seven populations satisfy it, not that it was skipped. run-23's
producer bound 236 of 236 eligible records, and on this evidence the other six
producers did the same for their own.

`UNDERIVED_RECORD` and `LOCATOR_NOT_DERIVED` are shown live on the same path by
`fault-injection-02`, which refuses ten trials the frozen Core admitted.

## What this cell does not establish

- **Admission, not meaning.** Byte-identical exports say the same records came
  back. They say nothing about whether those records are faithful to the
  document; that is the review protocol's question, and no query and no review
  was run here.
- **Change 4 is untouched.** No cell loads a Prolog contract. Fact contract
  version 3 is not exercised by this path at all.
- **One probe, one cell, one construction.** The source-binding probe was run
  on `run-20`. It establishes that the refusal fires; it is not a census of
  what else would trip it.
- **The candidate is not merged.** `e7937b89` is a separate clone whose Core
  differs from `c95dba7b` by far more than the four gate changes. This cell
  measures the pair of endpoints, not the four changes in isolation.
- **Nothing frozen was written.** No file under `private/paper-v4-v4-run-NN/`
  was modified, and no paper artifact was re-pinned.

## Reproducing

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
      paper-v4/experiment-v4/bridge-01/replay.py \
      --core FROZEN /Users/luis/Projects/malleus-dev c95dba7b86bb61487bda9a52458e1ea47cce20ab \
      --core CANDIDATE /private/tmp/malleus-progressive-guidance.uxhila/repo e7937b89 \
      --probe run-20 \
      --private private/paper-v4-bridge-01

    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
      paper-v4/experiment-v4/bridge-01/test_bridge.py
