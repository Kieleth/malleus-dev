# First BEAM capture: replay works, meaning needs work

Date: 2026-09-15. One fresh Sol producer, observed low reasoning effort.
This is a calibration result, not a benchmark score or a submission claim.

Historical first-capture checkpoint. The later approved reader comparison is in
[RESULT-02.md](RESULT-02.md). Its results supersede the pending-reader status
below, without changing this capture or its earlier assessment.

## What ran

The model received the complete 200-message weather-app conversation, with no
questions or answer key. It proposed both ontology and population. Two ontology
proposals and one population proposal were retained. The first ontology used a
field rejected by the compiler; the second removed it. Separate command-path
and root-locator mistakes were preserved as execution diagnostics.

The public Malleus path compiled the ontology, bound records to source evidence,
admitted one batch, and reopened its history. Parent verification copied only the
ledger into a temporary directory and called the public replay command with the
frozen runtime. Exported graph and receipt matched the producer's bytes exactly;
neither ledger copy changed. This is an observed storage/reconstruction result.
It is not independent regeneration of the model's ontology or interpretations.

## What the graph contains

There are 4,338 entities and 6,512 relations, including speaker attribution,
topic links, reported quantities and explicitly linked conflicting accounts.
The 14 ledger events represent one admitted population, not successive domain
updates. No incremental-update claim follows.

All source messages are represented in the capture inventory. That inventory
reports 2 fully formalized, 4,187 partly formalized and 198 unformalized
assertions. These are declared coverage categories, not a semantic review score.
Most proposition records contain classification, provenance and a few selected
fields, but no statement text. Their detailed meaning remains in retained
evidence. Quantities sometimes carry longer source text in a property. Therefore
graph-only reading and following the evidence links are materially different
conditions; they must not be mixed silently.

## Concrete checks, with successful controls

| Source statement | Accepted numeric field | Observation |
| :--- | :--- | :--- |
| Message 38 reports fetch latency of 250 ms | 250 ms | Value preserved. |
| Message 80 reports autocomplete response time of 280 ms | 280 ms | Value preserved. |
| Message 128 reports test coverage improving to 78% | Ratio 0.78 | Value preserved. |
| Message 66 states a new quota of 1,200 calls per day | 200 calls per day | Wrong extraction. Original evidence remains intact. |

These are checks of specific fields, not answers from the two planned readers
and not evidence that the surrounding interpretations are all correct.

### Why the quota is wrong

The model wrote a deterministic population script after reading the source.
Its number pattern accepts plain digits and decimals, but not comma-grouped
numbers. Searching the source phrase finds `200 calls per day` inside
`1,200 calls per day`. That suffix becomes the numeric value and both interval
bounds. The wrong value is already in the submitted population. Core did not
truncate it during admission or replay.

Exact chain: message 66, assertion `assertion:beam:1197`, accepted record
`quantity:beam:1178`. The public trace connects that record to the retained
capture and source. The assertion digest is correct. Structural validation
checks an allowed numeric field and its evidence binding; it does not prove
that the field expresses the evidence correctly. A valid locator is not a
numeric entailment check.

This is a producer-owned extraction defect, not an identified missing Core
capability. A future repair needs tests for complete numeric spans, including
grouped thousands, rather than changing this one stored value. This run remains
frozen. No population repair, replacement or extra producer was authorized here.

## What prevents an answer comparison today

No reader has run. [EVALUATION-PREFLIGHT.md](EVALUATION-PREFLIGHT.md) records four
upstream criteria needing adjudication and an unfinished absence assessment.
The questions and answer key remain unchanged. In particular, one supposed
absence question has partially present information. The standing control rule
does not permit silently certifying it as wholly absent.

Luis was asked whether to use two twenty-question batches or forty isolated
answer sessions. Two batches fit the approved small setup but cannot establish
per-question independence. Retaining disputed items with separate source-grounded
judgments is proposed, not silently substituted for the upstream rubric.

## Limits and costs

The source is synthetic. The run uses a frozen source copy of Core 18015352,
not an installed-wheel experiment. Actual producer effort was low, contrary to
the manifest's inheritance assumption. One automatic context compaction occurred.
No claim that either setting caused the extraction defect is established.

The reading is 523,080 bytes; the serialized graph is 2,500,151 bytes; the retained
ledger is 30,403,613 bytes. This is not a storage-compression result. Byte counts
are not token counts. Reported cumulative producer usage is 6,051,621 input
tokens, including 5,751,168 cached input tokens, and 19,177 output tokens. These
include repeated session input and tools, not a measurement of source length or
reasoning alone. No cost saving or million-token demonstration is claimed.

Verification: 42 parent calibration tests and 4 producer regression tests passed.
The tests include the known bad numeric record as preserved failure evidence;
passing them does not turn the capture into a semantically correct result.
No Core, marine experiment, manuscript, shared ref or commit changed.

Exact files are retained under
`private/beam-weather-calibration-01/producer/work/artifacts.json`.
Ledger head: `sha256:7ec922a55a0f1d64d1b4679355a8c5d4dc35df8c9651de3d61364de7c8093a86`.
Graph: `sha256:f5828c2e5066de11ecea93dacacf7a7fb4d3ca5c544bf58d6a277f0c03c809d6`.

LongMemEval and Kubernetes remain queued. No fallback dataset has launched.
