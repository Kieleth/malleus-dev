# Sol end-to-end comparison and population diagnosis

2026-09-07. Both new Sol sessions designed their own ontology, passed the
compiler gate, populated in that same session, and reached admission, replay
and thirty queries. Neither inherited Opus's project ontology. Both retain only
assertion metadata in the graph, not the scientific content of their retained
passages. This corrects the earlier experiment's scope, but does not improve
the capture result.

## Condition and observed result

The original run-21 initial prompt is unchanged except for run ID and path.
All eight initial input files match exactly: reading, root ontology, LinkML
types, three packs, history profile and acolyte skill. Queries were bound to
each accepted ontology before population and were never given to its producer.
Core remains c95dba7b86bb61487bda9a52458e1ea47cce20ab, tree
39a9b9da7dcd41660b8b10fb20b1b1d8e2261082.

Actual session metadata records gpt-5.6-sol at low reasoning effort for every
phase. No effort override was supplied. Opus's effort was not recorded. The
vendors' agent environments also differ. These are matched declared inputs and
two-phase tasks, not an equal-resource or isolated model-weights experiment.

| Observation | sol-e2e-01 | sol-e2e-02 |
| --- | ---: | ---: |
| Accepted ontology attempt | 1 | 2 |
| Validated ontology facts | 3,858 | 3,336 |
| Proposed and replayed entities | 74 | 81 |
| Proposed and replayed relations | 0 | 0 |
| Proposed and replayed events | 0 | 0 |
| Retained assertions | 74 | 81 |
| Blocks declared nothing assertable | 112 | 105 |
| Declared gaps | 0 | 0 |
| Ledger events | 13 | 13 |
| Returned rows across thirty queries | 0 | 0 |
| Questions COVERED / PARTIAL / NONE | 0 / 0 / 30 | 0 / 0 / 30 |

Two independent, source-grounded model reviews each assess all thirty questions
and 121 required semantics. Both pass the packet validator and the coordinator's
rerun. There are no returned witnesses to judge for support. These are coverage
findings, not fidelity scores. Three controls deliberately ask for unavailable
information; their NONE labels are not three failed positive questions. Human
ratification remains pending.

02's first ontology refused INVALID_RANGE for resource_url with range uri.
The exact diagnostic went back to the same producer. Its second attempt changes
only that range to string and compiles. Both populations admit on the first
submission. No semantic feedback or hand-authored fact was supplied.

Each independent from-empty reproduction matches all sixteen attempt files
byte-for-byte, including ledger, retained capture, public runner, graph export,
replay receipt, census and query results. Both query executions report twenty-nine
NO_CANDIDATE and one NOT_EXPRESSIBLE. They report no forbidden file, network
or named embedding-import attempt and leave the graph and ledger unchanged.

The reference Opus run-21 contains 508 entities, one event and 26 relations.
Its existing complete review finds eleven questions covered, nine partial and
ten none. That comparison uses the same thirty-question method, not a newly
selected question set. The reference is retained in REVIEW-RESULTS.md and
REPAIR-RESULTS.md. The older population-only Sol runs remain a separate condition
in OVERNIGHT-RESULTS.md; they are not the new end-to-end results.

## Where the scientific content disappears from the graph

Every new entity has exactly three properties: assertion_locator,
assertion_modality and statement_sha256. None has a name, description, quantity,
subject reference or scientific relationship. Each source block is copied into
a retained assertion statement; only that statement's identity and modality are
projected. The paragraph is recoverable through evidence tracing, but scientific
facts have not been represented in the source-free graph queried here.

One discriminating witness is page:1:block:005. It names RC1, describes the
detachment fault bounding it, and reports ridge dimensions. Both producer tool
histories display this complete block. Both accepted ontologies explicitly
declare BOUNDED_BY on a relation type. Yet 01 represents this block only as
claim:yu-2025:005 and 02 as claim:page:1:block:005, each with the three metadata
properties above. Neither proposes the named feature, the fault or their edge.
The unchanged bounding query therefore has no candidate. A query-name mismatch,
an absent relation family or a replay-dropped edge cannot explain this witness.

The producers' own written logs explain their chosen strategy. 01 says finer
decomposition without a compiler census and iterative feedback would risk
inventing identity boundaries or relation endpoints. 02 says decomposing mixed
blocks into semantic spans requires further editorial judgment. These are
recorded producer explanations, not independently established psychological
causes. At the witness above, the source supplies the names and relationship;
representing those facts does require interpretation, but not inventing them.

The supplied skill already directs producers to represent named subjects,
quantities and explicit relations, and to separate assertions with different
modalities. 01 instead marks ten whole blocks HYPOTHESISED and sixty-four STATED;
02 marks all eighty-one STATED. Neither decomposes paragraph-level mixed claims.
Both exclude bibliography blocks on the grounds that they concern other works.
That does not establish an absence of assertable bibliographic facts in this
source. 02 also cites a licence concern when withholding claim text; this report
records that rationale without endorsing its legal interpretation.

## What is established, and what remains unresolved

The failure is already present in the population submission. The compiler
accepts a relation-capable ontology, the producer chooses metadata-only records,
and admission and replay preserve them. The omission is not a missing Core
read or admission capability. Restoring ontology construction and same-session
continuity did not eliminate it in either new run. It was therefore wrong to
treat the missing ontology phase as the sufficient explanation of the earlier
Sol result.

Input availability is not the same as complete model-visible delivery. A
read-only audit of retained tool outputs found all 186 complete blocks displayed
for 01 after it paged past an initially truncated response. For 02, only 166
complete blocks could be matched; twenty blocks on pages three through five
were not recovered in full after truncation. Its skill read calls also did not
cover the final portion of the file. These are execution-compliance limitations,
not changes to the frozen input bytes. Complete-block matching checks normalized
raw and JSON-escaped text in tool outputs, not whether a model understood it.
Full source delivery in 01 rules out truncation as a sufficient explanation for
both zero-relation graphs. It does not make 02 a fully compliant source-reading
replicate.

The census calls all seventy-four or eighty-one declared assertions
FULLY_FORMALIZED. The pinned document adapter computes that category from
nonempty formalized_by and empty gaps. It does not test whether those targets
express the assertion's scientific meaning. Likewise, zero attachable subjects
is computed over proposed named candidates; neither run proposes those names.
These counters cannot certify semantic completeness. The first structurally
valid submission completes this harness condition, so no census-guided semantic
continuation occurred. Opus also succeeded without a structural return, which
prevents treating absent feedback alone as the cause of the model difference.

The best-supported behavioral diagnosis is an overly restrictive interpretation
of invention, followed by metadata-only block accounting. It is not yet a causal
explanation of why Sol chose that strategy and Opus did not. Low effort,
agent environment, instruction interpretation and source-reading behavior have
not been isolated. No model ranking follows from these two runs.

## Next discriminating improvement, proposed and not executed

Test the observed interpretation directly before another broad replicate or a
Core change. A separately labelled continuation of 01 could change only the
instruction distinguishing source-supported decomposition from invention, with
no questions, answer values, edge quota or expected records. Keep its own
ontology, source, model and effort. Ask for the scientific content of explicit
source assertions using that ontology, and preserve justified omissions. Retain
the original result unchanged.

If supported domain records and relations appear, the producer can perform that
decomposition under explicit clarification; source-grounded review must still
test whether it did so faithfully. If it remains metadata-only, that probe does
not support clarification as a sufficient repair. A separate effort-controlled
end-to-end comparison would then address a different hypothesis. Neither result
would retroactively become an unassisted replicate. The author has not selected
either new condition. No Core evaluator, relation quota or source-specific Core
rule is proposed.

## Evidence and verification

Each run is retained under private/paper-v4-answer-demonstration/sol-e2e-01 or
sol-e2e-02. Initial manifests and receipts bind the exact inputs; launch.json
identifies the actual producer session; manifest.json binds its own accepted
ontology and the same agent at both phases. producer/work/session-log.md records
the producer's decisions. gate/ retains every compiler attempt. attempt-01/
and reproduction-01/ retain execution evidence. review-01/ binds the complete
review packet. Full ledger heads, replay receipts, graph and query digests are
in each run-result.json; no living shared document substitutes for these bytes.

The new condition guard checks exact initial file closure and prompt identity.
The phase-two guard rejects an unaccepted ontology, a different or missing
producer identity, or population already visible before query binding. Review
validation now names FRESH_END_TO_END explicitly and checks its acceptance-time
binding, rather than mislabelling it as fixed-ontology population. Existing
review packets remain unchanged. Focused paper tests: 255 passed, two subtests
passed. The completed review-record digests are
8cd2f856e6d7cdce1570a2534027fe459a5dd6509be6e4efe2b75f796f2f7431 for 01 and
3ed0ba0fba04b6ae80c1e28b81ee28c41c0c2cb85c6980f0ed5ec0c21462f28d for 02.
Core received the bounded diagnostic and confirmation that no Core capability
request follows from it. No manuscript, PDF, Core code, shared ref, commit or
push was changed by this experiment.
