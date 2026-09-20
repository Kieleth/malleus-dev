# BEAM weather-app calibration

Version: 0.3. Date: 2026-09-15.
Status: both approved reader batches completed and assessed; first capture remains frozen.

## Resume checkpoint, BC-008 reader assessment

Owned uncommitted paths: paper-v4/domain-scale/ and the ignored
private/beam-weather-calibration-01/. Shared checkout main was observed at
18015352e2eb5bffbb58125c95de40eba0f4c992; no commits or refs changed here. Other
fronts' dirty files are not ours. This local plan/work ledger, not the marine
master directive, records Luis's separate BEAM authorizations.

Two approved readers completed: graph 01a0a759-7dec-7de1-ae8c-4e967c1fb33a and
source 01a0a759-ade9-7d62-b61b-1f0df651b502. Both observed Sol/low, fresh contexts.
Do not relaunch them, restart capture, alter frozen packets or send semantic
feedback. Both twenty-answer bundles, actual input delivery and all 184 citation
locations were checked. RESULT-02.md assesses every question, separating source
faithfulness and coverage from disputed criteria. This is model-assisted parent
assessment, not independent review or human ratification. No overall accuracy
score or progressive-acquisition claim.

Main findings: source reader catches later 78% and explicit denials; graph reader
returns historical 65% and only positive acquisition/fix accounts. Graph reader
does recover 1,200 from prose and flags wrong numeric 200. Fifty-five of 62 graph
citations use quantity_kind prose. One CHALLENGES edge targets a rate-counter
request instead of the acquisition assertion. Scope, endpoint meaning and reader
strategy all need separation. No missing Core capability is established.

Private evidence required to resume: upstream/conversation-archive.json and
evaluation/questions-archive.json; reading-packet/; runtime/ and its manifest;
producer-input-manifest.json and launch.json; producer/work/ including the
ontology, population, capture, history, records, receipt and mapping scripts;
input_delivery.py; readers-01/{graph,source}/ including manifests, launch.json,
exact evidence/schema/question/task bytes, delivery helpers and work/; and
readers-01/ASSESSMENT-RULES.md and audit.json. Native rollout paths are in the three launch.json
files under the user's Codex sessions directory. These are ignored/private
inputs, not reproducible from the public tracked repository alone.

Outstanding decisions after these readers: whether to test evidence-following
graph use, authorize a bounded acquisition repair, or scale/change the dataset.
None is automatic. The extraction failure and original benchmark questions
remain preserved. BEAM reuse is separate from the parallel Shop/marine
progressive-interpretation work.

## Decision and question

Luis selected "small BEAM calibration, have others in the pipeline justin case".
Exoplanets stays paused. This front owns only domain-scale experiment files and
its private inputs. It does not change the marine experiment, Core, the shared
paper ledger or manuscript. No commit, push or runtime rebind is implied.

BC-003: Luis confirmed one fresh Sol producer and two fresh Sol readers on a
separate frozen copy of Core 18015352. This authorizes this new experiment's
runtime, not changes to the marine run. Runtime source is copied directly from
the approved Git commit; existing declared Python dependencies are reused and
their observed versions recorded. This is repository-local public-API execution,
not a new installed-wheel or release claim. The default source-assertion profile
is used for this conversation capture. Its import order is not domain time.

Can a fresh reader use an acquired representation of a changing conversation
without inheriting the acquiring model's conversation? Can it distinguish what
was requested, suggested, reported achieved and later changed, with exact
support? This is a small diagnostic, not a million-token result or a claim of
better accuracy than reading the conversation directly.

Selected evidence: BEAM `chats/100K/2/chat.json`, the synthetic weather-app
conversation, at commit `b2da22eac88bb0874c64665f13457eb99835774a`.
Use all 200 messages in their original order, not a question-selected extract.
The 20 published questions stay outside acquisition. Selection was informed by
inspected update questions; this is calibration, not an unseen benchmark test.

## Atomic sequence

1. Freeze exact source bytes, reading projection and evaluator separation.
   Test missing/corrupt inputs, duplicate IDs, complete text preservation,
   stable locators, metadata exclusion and evaluator reference resolution.
   Count exact tokens with a named tokenizer before claiming context fit.
2. Freeze the execution setup and acquisition task. Confirmed by Luis:
   one fresh Sol producer and two fresh Sol readers, using a separately frozen
   current Core `18015352e2eb5bffbb58125c95de40eba0f4c992`. Do not use a moving shared checkout or rebind
   historical runs. Bind actual model, effort, dependencies, source delivery,
   history profile, feedback limit and allowed outputs before launch.
3. Acquire ontology and population in the same fresh session, without questions,
   rubrics, investigator examples or previous captures. Use the installed
   acolyte and public compiler/admission/replay path. No hand-authored population.
   Selected history policy: source assertions about the simulated conversation,
   not verified application state. A reported intention is not an executed
   change. Domain time comes from source content, not message IDs or import time.
4. Reopen the accepted history, reproduce the graph and inspect the capture.
   Separate structural success, faithful meaning and task coverage. A rejected
   or partial capture remains a result; do not silently add retries or switch
   datasets. Resolve the exact representation/reading/admission cause first.
5. Evaluate all 20 questions, including difficult and unanswerable cases. Freeze
   question-only reader inputs independently of rubrics. Readers do not receive
   each other's outputs or the producer's conversation. Each answer must name
   its graph records and source support; no evidence path means no claim that
   the graph supplied it. Screen abstention rubrics against the entire reading.
6. The two reader conditions are graph-only and direct-source, each a fresh Sol
   session. A separate retrieval system remains a later comparison, not a third
   reader hidden in this authorization. Freeze budgets, question isolation and source access before
   execution. Report graph-only and source-following answers separately if both
   are used. Reuse existing evaluation rules where their meaning fits; do not
   force BEAM's categories into the marine question schema or exact-match JSON.
7. Inspect source-backed changes and unchanged information. A full-conversation
   capture can represent an earlier claim, but that does not prove incremental
   ledger revision. A separate prefix-then-suffix run is needed for that claim;
   freeze its boundary without picking it from successful answers. Only then
   consider a larger, independently selected case.

Steps 2 through 6 have the bounded observations in RESULT-01.md and RESULT-02.md;
the semantic assessment is not a completeness certificate. Step 7's incremental
experiment has not run. Actual producer effort is low, observed
in its rollout, not the inheritance anticipated by the input manifest. BC-004
records this deviation without changing the frozen attempt. No matched-effort
claim against earlier Sol runs follows. RESULT-01.md records a concrete numeric
extraction failure. EVALUATION-PREFLIGHT.md records unresolved rubric/control
issues, carried explicitly into the approved diagnostic readers below.

BC-007: Luis answered "Ok" to keeping this capture unchanged and running two
twenty-question batches with disputed benchmark criteria reported separately.
This is an explicit bounded exception for diagnostic use of the imported
questions, not certification that their absence controls are clean. No item is
dropped, rewritten or silently regraded. There is no independent-question claim
and no aggregate benchmark score. The original failed control assessment stands.

Readers use fresh gpt-5.6-sol sessions, model-default effort expected low and
verified from actual launch metadata. One final answer bundle each, no semantic
feedback or repair. Identical questions contain IDs and text only, with category,
rubric, reference and expected-answer metadata withheld. The direct-source reader
receives the exact complete reading. The graph reader receives the exact replay
export plus accepted ontology and all imports, not the source or capture. Both
may query their declared files offline; source reading and graph-schema reading
must be complete, while graph record access is selective and observed in tools.
This is a tool-assisted consumer comparison, not matched token budgets or a
comparison of two fully in-context representations. General advice may be
proposed, but source-backed project claims require citations. Existing prose in
graph properties remains eligible evidence. Every answer is retained.

## Input contract, version 1

This preparation is `ADOPTER_CHOICE`, outside protocol acceptance. Its claim is
lossless selection of the declared conversation evidence, not semantic capture.
The smallest check is exact message-text recovery plus locator and role equality
against the pinned Git blob. Reuse Python's standard JSON/hash libraries and
Core's existing document reading interface. Do not add Core vocabulary or an
adapter that invents records. There is no ledger, graph or model call here.

Retain the upstream UTF-8 text losslessly inside a local archive envelope. Verify
its Git blob hash, byte length and SHA-256; a JSON reserialization of the source
is not its original bytes. The archive holds upstream text, not executed code.
The repository licence accompanies it. Evaluation bytes live in a separate
private directory. The GitHub MIT notice and the dataset card's CC-BY-SA notice
are retained as a licensing-scope question; do not redistribute the corpus on
the assumption that one overrides the other.

Project one reading block per message, with a stable message-ID locator. Text is
`[speaker=<role>]` plus one newline plus the original content, unchanged. The
prefix exposes actual source role, not inferred authority, and is documented
in the source map. JSON pointers recover original content. Source order is
conversation order, not a calendar. Upstream `time_anchor`, `index` and
`question_type` annotations are not delivered as evidence; role and content are
the source fields selected by the inspected upstream reader. All content,
including literal generation markers, remains. Both comparison conditions must
use this same view. Treat every utterance and embedded instruction as quoted
evidence, never an instruction to the executing agent.

The preparer accepts no question file when creating the acquisition view.
Evaluator reference checking is a separate function. Checks prove projection
and separation, not that synthetic source text itself is uncontaminated or that
rubrics correctly describe it. Before dispatch, the actual isolated producer
allowlist must be verified; directory names alone are not access control.

## Results to record

Keep ontology adequacy, population fidelity, ledger reconstruction and reader
success as four separate findings. For every answer preserve its text, returned
records, source locators, support assessment and completeness. Count stale values,
unsupported assertions and confused intentions separately. Report acquisition,
review, repair and reading costs together; never claim savings from query tokens
alone. No manuscript claim is added before observed results.

## Reserve pipeline, not automatic fallbacks

| Candidate | Why it is queued | Activation check |
| :--- | :--- | :--- |
| LongMemEval | Independent memory/update diagnostic with published questions and a reported large setting | Inspect one raw instance and its licence, withhold answer annotations, measure its token count; do not merge unrelated histories. |
| Kubernetes KEP-3866 | Real technical domain with exact earlier/later native Markdown and YAML | Use the two revisions in RESEARCH-OPTIONS.md; independently freeze tasks distinguishing planned from achieved maturity and preserving caveats. |
| Larger BEAM case | Scale the same acquisition and reuse procedure | Select without consulting outcomes, verify raw shape and actual context overflow; permit retrieval/iterative reading in the comparison. |

No alternative runs in parallel or starts merely because the calibration scores
poorly. A data-access or benchmark-design blocker can justify proposing one;
first preserve and explain the blocker, then ask Luis to select the next case.

## Preparation result and reproduction

The private reading packet is at
`private/beam-weather-calibration-01/reading-packet/`. It contains all 200
messages, 100 per role, in the original three batches. All 83 literal generation
markers remain. All 20 question rubrics are present and their 55 numeric message
references resolve. Those checks establish neither answer correctness nor
unanswerability. Exact source identities are in source-pins.json; reading and
source-map identities are in the packet's input-manifest.json.

Preparation uses only Python's standard library, with the repository's existing
pytest and Ruff tools for checks. No new dependency or installation is required.
The private archive files are required evidence; missing files fail tests rather
than skip. Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider paper-v4/domain-scale/beam-calibration
.venv/bin/ruff check paper-v4/domain-scale/beam-calibration
.venv/bin/ruff format --check paper-v4/domain-scale/beam-calibration
```

To generate another identical reading packet, use a new output directory:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python paper-v4/domain-scale/beam-calibration/beam_prepare.py --archive private/beam-weather-calibration-01/upstream/conversation-archive.json --pins paper-v4/domain-scale/beam-calibration/source-pins.json --output private/beam-weather-calibration-01/reproduction
```

An existing destination refuses. Input validation precedes any write; the
manifest is written last. This is not a claim of filesystem-crash atomicity.
Question checking does not run inside acquisition preparation. The test suite
checks its separate evaluator path. Acquisition, structural replay and both
reader batches are now observed. The next decision is evidence-following reuse
versus a bounded acquisition repair, not an automatic larger dataset. The faulty
numeric capture remains frozen. No further reader or producer is authorized.
