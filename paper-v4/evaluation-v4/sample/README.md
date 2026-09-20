# Independent judgement of a sampled witness set

The faithfulness figures in the paper come from model-assisted reviews under
protocol v3 (`paper-v4/evaluation-v4/review-protocol-v3.json`), recorded per
cell in `review-record.preliminary.md`. The producers of run-22, run-23, run-24
and run-25 each record `model_id` `claude-opus-5` in their `launch-log.json`; the
reviewer is recorded as the kind `CLAUDE_PRELIMINARY`, with no model id in
either the record or the review input manifest. A model reviewing a producer of
its own kind is a reliability question the record cannot answer by itself.

These scripts draw a random sample of those witnesses, hand it blind to a
different judge, and put that judge's labels beside the recorded ones. They
dispatch nobody. The judging session is launched by the parent session with
`judge-task.template.md`; nothing here calls a model, and nothing here writes a
paper figure.

## The five steps

**1. Draw the sample.** Public output.

```
.venv/bin/python paper-v4/evaluation-v4/sample/sample_witnesses.py \
    --cells run-22-v413 run-23 run-24 run-25 --size 200 --seed <SEED> \
    --only-label SUPPORTED --output paper-v4/evaluation-v4/sample
```

Writes a sample file: the seed, the per-cell counts, and per sampled witness its
cell, `witness_key`, `source_locators`, the `source_support` the review
recorded, and the digest of the record file it came from. A draw is stratified
proportionally by largest-remainder apportionment, never gives a cell zero, and
is a function of the seed alone: the population is ordered by `witness_key`
first, so a record whose witnesses are rewritten in another order draws the same
sample when the keys and the count are unchanged. No reading text is written.

A cell is a directory under `paper-v4/evaluation-v4/`, not a run id. `run-22-v413`
is a cell whose manifest carries `run_id` `run-22`; every material is resolved
through that directory's own `review-input-manifest.json`, so a query result at a
path outside the `run-NN` pattern is found and digest-checked like any other.

Three strata, one per invocation, each with its own file name:

| options | file | population |
| --- | --- | --- |
| neither | `sample-<SEED>.json` | every witness of every named cell |
| `--only-label LABEL --size N` | `sample-<SEED>-<label>.json` | the witnesses recorded with that label, drawn proportionally |
| `--all-label LABEL` | `sample-<SEED>-<label>-all.json` | every witness with that label, no sampling, no size |

`--only-label` refuses a cell that holds no witness of that label, because a
stratum that silently drops a cell is not the stratum that was asked for.
`--all-label` reports such a cell as zero and continues. The two options are not
combinable; run the script twice. The seed is recorded in a complete stratum and
changes nothing in it.

Why strata: the recorded labels are lopsided, so kappa on a draw from the whole
population is arithmetic about a constant. A random stratum inside `SUPPORTED`
asks whether an independent judge finds anything the first reviewer waved
through; a complete `PARTIAL` stratum is small enough to be judged whole.

`--cells` is required and has no default. A default would name a cell set that
goes stale the moment a cell is rebound or a run is added, and a stale default
draws from a superseded record without saying so.

**2. Build the packet.** Private output, because it reproduces reading text.

```
.venv/bin/python paper-v4/evaluation-v4/sample/build_packet.py \
    --sample paper-v4/evaluation-v4/sample/sample-<SEED>-supported.json
```

Writes `private/paper-v4-evaluation-sample/packet-<SEED>-<8 digest chars>.json`.
Per sampled witness: the fields the query returned for it, taken from the cell's
private query result by `witness_key`, and the full text of every block its
recorded locators cite, taken from the selected reading. Both files are located
through the cell's `review-input-manifest.json` and are refused if their bytes
differ from the digest that manifest binds. The builder also refuses if a review
record changed after the sample was drawn, and refuses to write outside
`private/`.

The packet carries **no** recorded `source_support`, **no** recorded
`rationale`, and **no** stratum label. Its `judgement` slot is
`{"source_support": null, "rationale": null}`. The stratum is left out on
purpose: naming it would tell the judge the label every witness in the packet
carries, which is the whole quantity under test. That is also why the file is
named after eight characters of the sample digest and not after the label: two
strata at one seed need two names, and the judging session reads the name.

One caveat on checking blindness by searching for label words: a record field may
legitimately hold a domain value that contains one. The 200-witness `SUPPORTED`
packet contains the string twice, both times inside `NOT_SUPPORTED` as the value
of `hypothesis_disposition` on a run-25 record. The check that means something is
structural: no `recorded_source_support` key, null judgement slots, no `stratum`.

**3. Dispatch the judge.** The parent session instantiates
`judge-task.template.md`, substituting the packet path, the record path, the
sample **digest**, the witness count, and the judge's `model_id`, `actor_id` and
`reasoning_effort`. The sample's path is deliberately not among them: its name
says which stratum this is. The judge copies `judge-record.blank.md`, judges each
witness's source support against its cited blocks only, writes one rationale per
witness in its own words, records its kind as `INDEPENDENT_MODEL_JUDGE`, and
computes no aggregate. The four label definitions in the template are verbatim
from the frozen v3 review task
(`paper-v4/evaluation-v4/review-task-protocol-v3.template.md`), which
instantiates the `judgments.source_support` set of `review-protocol-v3.json`.

**4. Validate the judge's record.** The parent runs this, not the judge, because
it needs the sample file. A refusal names no recorded label, so it can be handed
back to the judge verbatim.

```
.venv/bin/python paper-v4/evaluation-v4/sample/validate_judge_record.py \
    --sample paper-v4/evaluation-v4/sample/sample-<SEED>-supported.json \
    --record private/paper-v4-evaluation-sample/judge-record-<NAME>.md
```

Refuses with one named reason: the schema string is not
`malleus.paper-v4.independent-judge-record/v1`; the record's `sample_sha256` is
not the sample file's digest; the judgements do not cover exactly the sampled
witnesses once each; a label is outside the four; a rationale is empty; a
rationale shares a 60-character normalized run with a reading block. That last
check is the method
`paper-v4/experiment-v4/run-23/results/withheld-artifacts.json` describes,
`SHARED_NORMALIZED_CHARACTER_RUN_AGAINST_EVERY_READING_BLOCK` with unicode
whitespace collapsed to a single space, at its frozen threshold of 60. It reads
the selected reading from `private/paper-v4-text-layer/selected-reading.json`;
`--reading` points it elsewhere.

**5. Report agreement.**

```
.venv/bin/python paper-v4/evaluation-v4/sample/agreement.py \
    --sample paper-v4/evaluation-v4/sample/sample-<SEED>-supported.json \
    --judge-record private/paper-v4-evaluation-sample/judge-record-<NAME>.md
```

Validates each record first, then prints per-cell and overall percent agreement,
Cohen's kappa over the four-label space, and the confusion counts in both
directions. Passing `--judge-record` twice adds the agreement between the two
judges. Generalised from `paper-v4/evaluation-v4/reliability.py`, which reads one
hardwired question of one cell from an absolute path; nothing is imported from
it. When both sides use a single label everywhere, expected agreement is 1 and
kappa is undefined; the script says so rather than printing a number.

With `--judge-record` omitted it prints the composition and prevalence only: the
per-cell drawn counts, the stratum they came from, and the recorded labels of
what was drawn. No judge record is read and no agreement is computed. That is
the mode to run right after a draw.

## Public and private

Public, in this directory: the scripts, `judge-task.template.md`,
`judge-record.blank.md`, `README.md`, `test_sample_tooling.py`, and the sample
files. A sample file carries block ids, never block text, and it does carry the
recorded labels, which is why the judging session is never given one.

Private, under `private/paper-v4-evaluation-sample/` (gitignored by the `/private/`
rule in `.gitignore`): the packet, the judge records, and anything else that
reproduces reading text. `build_packet.py` refuses a destination outside
`private/`.

## Tests

Registered in `paper-v4/active-test-manifest.json` under `paths` as
`paper-v4/evaluation-v4/sample`, in the unpinned group: these scripts bind no
Core version. The tests build synthetic v3-shaped records in `tmp_path` and open
no private file, so they run wherever the gate runs.

```
.venv/bin/python paper-v4/run_active_tests.py
```

The full gate ran green on 2026-09-11 with this directory registered: `630
passed, 2 subtests passed` for the pinned group, `1998 passed` for the unpinned
one, exit 0. After the label-stratification changes, the unpinned group, which
is the one holding this directory, was rerun on its own and reported `2115
passed in 327.68s`, exit 0; the pinned group was not rerun, because nothing here
is in it. Or this module alone:

```
PYTHONPATH=.:src .venv/bin/python -m pytest --import-mode=importlib -q \
    paper-v4/evaluation-v4/sample
```

which reported `38 passed`.

## The drawn sample

Cells `run-22-v413`, `run-23`, `run-24`, `run-25`, seed `20260912`. Two strata,
both public files here, both packets private. No judge has been dispatched.

Stratum one, `--only-label SUPPORTED --size 200`:

| cell | drawn | in the stratum | in the record |
| --- | --- | --- | --- |
| run-22-v413 | 51 | 457 | 457 |
| run-23 | 47 | 422 | 428 |
| run-24 | 46 | 405 | 416 |
| run-25 | 56 | 500 | 505 |
| all | 200 | 1784 | 1806 |

Stratum two, `--all-label PARTIAL`, complete, not sampled:

| cell | drawn | in the stratum | in the record |
| --- | --- | --- | --- |
| run-22-v413 | 0 | 0 | 457 |
| run-23 | 6 | 6 | 428 |
| run-24 | 11 | 11 | 416 |
| run-25 | 5 | 5 | 505 |
| all | 22 | 22 | 1806 |

`run-22-v413` holds no `PARTIAL` witness: its record is 457 of 457 `SUPPORTED`.
Across the four cells the recorded labels are 1784 `SUPPORTED` and 22 `PARTIAL`
over 1806 witnesses, with no `UNSUPPORTED` and no `NOT_EVALUABLE`. That is the
lopsidedness the two strata exist to work around.

Files and digests:

| file | sha256 |
| --- | --- |
| `paper-v4/evaluation-v4/sample/sample-20260912-supported.json` | `f573af6bea6d425b72918d39923e3ca14aff9fe2c9bf03b6510b4cf25fd88338` |
| `paper-v4/evaluation-v4/sample/sample-20260912-partial-all.json` | `ce1e451cc0c8059e25207ab2c3a4ac661a98eddc55761158274002da89fec518` |
| `private/paper-v4-evaluation-sample/packet-20260912-f573af6b.json` | `e15e967936d754ecd7a8674b2208c0a1cd0dc947bb5e4d842c78e9dcf8aa8d4d` |
| `private/paper-v4-evaluation-sample/packet-20260912-ce1e451c.json` | `0c746e4a4efb1185eb435d283705a3f1ed2dd22fdda2595d5071fb6b52d53113` |

The 200-witness packet covers 153 `ENTITY`, 40 `SUBJECT` and 7 `RELATION`
witnesses; the 22-witness packet covers 20 `ENTITY` and 2 `SUBJECT`.

An earlier trial at seed 999001 over the pre-rebind cells is under
`private/paper-v4-evaluation-sample/trial/`. It is superseded by the draw above
and is not evidence; its two judge records carry labels assigned by position and
are not judgements of anything.
