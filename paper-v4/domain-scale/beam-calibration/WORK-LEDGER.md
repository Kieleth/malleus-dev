# BEAM calibration work ledger

Append observations and decisions here. PLAN.md is the current plan; this file
preserves what actually happened. No model result is implied by preparation.

## BC-001, 2026-09-15: selection and bounded preparation

Author instruction: "small BEAM calibration, have others in the pipeline
justin case". Selected the previously proposed non-financial weather-app case.
LongMemEval and Kubernetes remain queued, not launched. Read current paper
instructions, handover, next-run checks, malleus-dev and malleus-acolyte. Marine
E-0399 and its frozen runtime remain unchanged. Current shared main is 18015352;
using it for a separate experiment is proposed, not silently adopted.

Before code: classify the offline preparer as ADOPTER_CHOICE. It projects exact
source text and speaker roles with recoverable locators; it neither extracts
knowledge nor writes accepted state. Pure preparation and evaluation-reference
checking are separate. No server interaction in code, no endpoint, no missing
field defaults, no replaced mechanism. Use RED tests before implementation.

The inspected native batch boundaries contain 72, 62 and 66 messages. The two
previously examined update pairs occur within batches, not across a single
natural batch boundary. Therefore a from-empty full capture plus historical
answers must not be reported as an incremental-update experiment.

The exact GitHub LICENSE is MIT (blob 3f9b9d0c86435b02a9867570d765f934a01d4587).
The previously inspected hosted dataset card names CC-BY-SA. Preserve both
notices and defer public corpus redistribution pending scope resolution.
No tokenizer is installed in this project's .venv. No dependency was installed
ad hoc, and the 100K directory label is not reported as a measured token count.

Sent one non-blocking request to select the fresh Sol execution setup and exact
separate Core baseline. No agent or model run has been launched.

## BC-002, 2026-09-15: source freeze and mechanical preparation

Added tests first. Initial RED was a collection error for the missing preparer,
not 32 observed behavioural failures. Implemented the pure offline source
unpacker, reading projection and separate question-reference check. The initial
32 tests passed. Added five selected-source/CLI tests: all 37 pass, including
full source-text recovery, exact packet rebuilding, evaluator reference closure,
corrupt-input refusal before output and refusing to overwrite an earlier packet.
Ruff requested formatting; formatting applied to these three new files only.

Retained exact upstream text inside lossless JSON envelopes because neither
upstream JSON source ends in a newline. SHA-256 and Git-blob checks reproduce
the pinned 535,114-byte conversation and 29,546-byte evaluator file exactly.
This preserves the original bytes without pretending a JSON reserialization
has their identity. Conversation SHA-256 is
3a3bd796f4aa24e8f34e718dc2823ae942663349eb89054f03885051e2daf1c4;
evaluation SHA-256 is
d188e929644c9ef9fcd4520e7b5a3daf2c2e069b1247a324bd13d5aadd1ed96e.

Generated reading: 200 blocks, 100 user and 100 assistant messages, batches
72/62/66, all 83 generation-marker occurrences preserved. Reading SHA-256 is
5fb9e2eb7d491b2726da1c279bcf44290870f8dd0af81382e4a01de6315e374a.
The source-map SHA-256 is
db446576b88a9fd04849a6513c8818a587ffa68a169fe03bbf2359644b365f0f.
All 20 question rubrics and 55 numeric source references pass structural checks;
semantic review is explicitly NOT_PERFORMED. There is no answer score.

The preparer takes no evaluation file. It strips only the explicitly excluded
metadata fields from the view, not from the retained source. It adds a declared
speaker prefix and preserves the entire original content after that prefix.
This is a new matched reading condition, not a claim to reproduce the upstream
benchmark's model-message delivery. The future baseline must use this same view.

Remaining: verify actual model isolation/delivery, name and measure a tokenizer,
freeze the runtime/profile and bounded producer/reader procedure, then acquire.
The standing paper control-screen meaning remains required, but its marine
question schema must not be imposed on BEAM by a compatibility adapter. No
evaluator-authored population, Core edit, runtime adoption, model execution,
graph, manuscript result, commit or ref change occurred.

## BC-003, 2026-09-15: execution setup confirmed

Luis answered "confirmed" to one fresh Sol producer and two fresh Sol readers
against a separately frozen current Core. PLAN.md advances to 0.2. Copied runtime
source, ontology, acolyte and declared docs directly from commit
18015352e2eb5bffbb58125c95de40eba0f4c992, tree
04b6ee7b6a0417e5eb7b31d381625c456bfabe3a, without changing shared refs.
The public compiler resolves inside that copied runtime and its bundled ontology
resolves inside the same copy. Observed declared dependencies: LinkML and its
runtime 1.11.1, NetworkX 3.6.1, PyYAML 6.0.3, tzdata 2026.3.

Use the shipped source-assertion capture-batch profile, identity
sha256:2317d88fd236fb63d5f4b68262619de6b5874946ab2ea8144b1b9a2995f471d5.
Its structural policy checks bytes and graph application, not source truth.
The producer proposes both ontology and population in one fresh session. Two
structural correction returns per stage, no semantic hints or answer-key access.
Retain every submitted attempt; no second producer or hidden sampling.
The two reader roles are graph-only and direct-source. A retrieval implementation
is reserved, not silently added to the approved two-reader budget.

Source tokens remain unmeasured: neither project nor bundled runtime has a named
tokenizer available. Do not install ad hoc or infer exact token count from the
100K label. Exact byte count and observed model input usage remain available;
do not claim a measured context-overflow test. Fresh context will use fork_turns
none, and actual settings plus model-visible delivery must be observed rather
than inferred from a model-authored declaration.

## BC-004, 2026-09-15: first producer launched; settings observed

Launched exactly one worker with fork_turns none and model gpt-5.6-sol. Actual
session is 01a0a73f-16c4-7593-9a5f-073fc37e8dc0. The rollout records effort low.
The launch omitted an effort override; the manifest's expectation of inherited
effort was wrong. Preserve that manifest and this correction. Do not call this
a matched-effort comparison with earlier Sol runs and do not silently relaunch.
The observed metadata is retained in the private launch.json. Reader effort must
be observed too; model names alone do not establish matched settings.

Before launch, added two execution checks. Initial RED was two missing-manifest
failures. With manifests and copied runtime in place, all 39 calibration tests
pass. The new checks require exact declared input bytes, question separation,
and every copied runtime file to match its Git blob at the selected Core commit.
They do not prove semantic comprehension or filesystem isolation.

The producer reads the full input packet using the existing framed-delivery
helper. Exact delivery remains to be verified against its tool outputs. Its
limits are three ontology submissions and three population submissions, with
structural diagnostics only. No question or evaluator observation is returned.

Asked Luis whether the two readers should each answer the twenty-question batch
or whether he wants forty isolated answer sessions. No reader has launched.
Batched execution does not establish question-by-question independence.

## BC-005, 2026-09-15: exact delivery and evaluator preflight

The existing input-delivery verifier finds every declared frame in the producer's
actual tool outputs: 129 frames, including all 88 reading frames, with exact
input digests and the observed Sol/low setting. This establishes delivery, not
comprehension. It does not establish OS-level access isolation.

Evaluator inspection found four criteria needing adjudication before aggregate
scoring: an overbroad ESLint absence rationale, an undefined feature-count scope,
an error-topic ordering not established by the cited source, and a meeting date
treated as the date of scheduling. Exact local locators and boundaries are in
EVALUATION-PREFLIGHT.md. The other absence claim has only a keyword/context check,
not a completed semantic absence assessment. Thus no clean control-screen pass
or reader-question freeze is claimed. Upstream bytes, questions and rubrics
remain unchanged; all twenty cases are retained. No findings went to the
question-blind producer and no evaluator-authored records were introduced.

Correction to the preceding frame total: 119, not 129. The per-input counts and
delivery verification were correct; the manually written sum was not. A new
test calling the actual verifier caught this reporting error (one failed, 39
passed). The test now requires the observed low effort, recorded deviation and
the correct 119-frame total, rather than relying on the prose summary. All 88
reading frames were present throughout. No input or producer execution changed.

## BC-006, 2026-09-15: producer frozen; replay independently reproduced

Producer finished without semantic feedback or a second run. Two ontology
proposals, one population proposal. Its four regression tests passed again under
the frozen runtime. Parent added two read-only evidence checks: public replay
from a ledger copy reproduces graph and receipt byte-for-byte, and the retained
numeric failure remains beside three successful numeric controls. No Core or
producer bytes were edited. These are evidence checks, not a TDD repair claim.

Observed result: one accepted population, 14 ledger events, 4,338 entities,
6,512 relations. Public trace resolves quantity:beam:1178 to assertion:beam:1197
and the retained reading. Source message 66 says 1,200 calls per day; the model's
regex mapping emits 200 before admission. Core preserves that proposed value.
The fault belongs to the acquisition mapping; there is no demonstrated Core
read/replay gap to request. The source and accepted result remain unchanged.

The graph's 4,187 proposition records store classification/provenance and selected
fields, not statement text. Some quantity records do include longer prose.
Do not claim that classification plus a digest captures all meaning or that
graph-only and source-following consumers have the same evidence surface.

Rollout contains one automatic compaction. Its last cumulative token record is
6,051,621 input, of which 5,751,168 cached, and 19,177 output. This is cumulative
session usage, not unique source tokens or a reasoning-token estimate. Recorded
low effort and compaction are conditions, not proven causes of the failure.

RESULT-01.md records observations and limits. No readers launched: source-control
adjudication and the reader-isolation choice remain open. No overall score,
question rewrite, omitted case, hidden retry, alternative dataset, manuscript
claim, Core change, commit or ref update occurred.

## BC-007, 2026-09-15: two batched readers authorized and prepared

Luis answered "Ok" to the exact recommendation: preserve capture 01 and run two
twenty-question reader batches, reporting disputed criteria separately. PLAN
advances to 0.3 at this author decision. This does not repair the upstream key or
certify a clean absence-control instrument. Do not publish aggregate accuracy.

Deliverable classification: ADOPTER_CHOICE, paper-local read-only preparation
and assessment. No protocol/profile, Core API, admission or semantic population
change. Reuse the exact replay export and framed-delivery mechanism. The
observation is fresh answers plus resolvable citations, with source-grounded
assessment separate from matching quotes. Exclude capture repair, source-following
graph access, a new retrieval system, forty independent answer sessions, semantic
retries, alternate models, shared paper edits and commits.

Before code: no server calls or endpoints, no new dependencies or mechanism
replacement; missing inputs refuse. Tests first produced one missing-module
collection error. Twelve reader contract tests then passed. They cover evaluator
metadata removal, missing/duplicate answers, changed inputs, unknown locators and
paths, invented excerpts and unsupported positive-answer structure. They do not
score entailment. Local Ruff caught one unused test import; it is used by the
subsequent exact-packet test, not suppressed.

Both readers receive the same twenty question texts, with neutral sequential
IDs. Source receives the complete reading; graph receives records plus all six
ontology/import sources. No source text is added to graph beyond existing fields.
The graph is searched selectively; the complete source and schema inputs are
displayed through exact frames. This difference is explicit, not a matched
full-context or matched-token-budget claim. One final bundle per reader, no
semantic feedback. Sol model-default effort is expected low, verified at launch
rather than called inherited. OpenAI Docs confirms a model override without an
effort override uses the model default; the actual rollout remains the evidence.

Launched graph reader 01a0a759-7dec-7de1-ae8c-4e967c1fb33a and source reader
01a0a759-ade9-7d62-b61b-1f0df651b502, both with fork_turns none. Both actual
turn_context records confirm gpt-5.6-sol/low. Per-reader launch.json files bind
the rollout paths. The complete local preparation selector passed 55 tests
before launch, including identical question bytes, exact separate evidence
copies and all transitive ontology imports. No reader result exists at launch.

## BC-008, 2026-09-15: both reader bundles assessed without capture repair

Completed the BC-007 authorization, not a new experiment decision. PLAN stays
0.3. Both readers returned all twenty answers, no parent semantic feedback.
Actual model/effort is Sol/low; no reader compactions. Exact delivery observed:
graph 14 task/question/schema frames, source 90 frames including all 88 source
frames. Graph records were selectively queried. All 62 graph and 122 source
citations resolve, which checks location rather than meaning. Actual usage and
answer digests are retained in private readers-01/audit.json. Inspection found
no observed outside-packet evidence access; isolation remains instruction-based,
not an OS sandbox. Graph's outbound status message received no semantic reply.

RESULT-02.md records all twenty paired findings. Source recovers 78% specifically
scoped integration coverage and the key-acquisition/bug-fix contradictions.
Graph returns old 65% and positive reports without the denials. It does recover
1,200 from retained prose and flags numeric 200, a positive control that prevents
misreporting every wrong numeric record as a wrong answer. Both qualify 250/280
ms comparison and decline to identify the other Jira bugs. This is parent
model-assisted assessment, not independent review or human approval.

RCA separates capture from reader: 0.78 is present but measurement scope remains
in evidence; one CHALLENGES edge targets a counter request instead of acquisition
because the producer selects the earlier message's first assertion; the reader
does not inspect CHALLENGES. Fifty-five of 62 graph citations are quantity_kind
prose, 36 from one recap field across ten questions. No all-relations failure,
Core replay defect or universal graph-reader failure is claimed. ResearchClaim
statement text is optional under the pack's licence rule, so graph-only results
cannot stand for the untested evidence-following path.

All four preflight criterion disputes remain separate. The answer review adds
q05's unspecified five-aspect selection as a post-result concern. No question
was dropped or rewritten and no aggregate score was computed. Source answers
also have limitations: early-only q06, partial summary coverage, weak citation
coverage for the investigator-independent twenty-category grouping, and q20's
extra conditional April 6 assumption. Source is a comparison, not an oracle.

Before adding evidence tests: no server interaction, endpoint, new dependency,
legacy replacement or production repair. Missing artifact bytes fail. An initial
inspection guessed capture.json and failed; subsequent inspection and the new
test resolve population through the existing artifact manifest. A documentation
patch refused an unmatched context atomically; exact lines were read before
retry. Neither error changed frozen evidence. Three new observational tests
preserve answer identities, delivery and scope/endpoint/prose-use witnesses.
They do not claim to prevent a producer's semantic errors. Full local calibration
selector: 58 passed. Ruff check and format check passed.

Owned edits remain domain-scale only plus ignored private result evidence. No
Core, marine, shared ledger, manuscript, frozen model output, commit or ref
changed. Next recommendation is one explicitly evidence-following reader on the
same capture before acquisition repair or scaling. That would be a new condition
and requires Luis's decision; it has not launched. LongMemEval and Kubernetes
remain reserves; exoplanets remains parked.

Coordination delivery was not completed: the cross-task messaging permission
check rejected the proposed status handoff because authorization for disclosing
private project details to that destination was not established. No retry or
alternate delivery was attempted. This local checkpoint remains available; a
cross-task send requires explicit authorization. No Core request was sent.
