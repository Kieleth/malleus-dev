# Capture regression RCA

2026-09-07. Read-only diagnosis requested by Luis after E-0243. No new producer
run, input rebind, runtime fix or semantic repair was performed.

## Verdict

There is a confirmed regression in the instructions selected by the paper
experiment: later runs reused a Core snapshot from before a correction that
this task had already accepted and consumed. Current Core did not lose that
correction. The paper stager deliberately loaded the older snapshot's skill,
and the paper's identity checks accepted it. I failed to compare its semantics
with the accepted correction before treating these runs as further project
progress.

This establishes an input-selection regression, not that the instruction
rollback alone caused every missing relation. The successful Opus run used the
old instructions too. It is still not a controlled model regression, and the
complete causal explanation of the producer behavior remains open.

## The sequence that exposes it

| Boundary | Selected input and observed behavior |
| --- | --- |
| Original Opus run-21 | Core c95dba7, old skill. Own ontology, then 508 entities, one event and 26 relations. |
| Core correction 723a4f9, integrated through 160878c | Replaced the overly narrow relation instruction; explained proposition identity/content and the census's semantic limits. No document runtime change. |
| followup-sol-01 | Core 160878c, corrected skill, original run-20 ontology. Fresh Sol at low effort produced 41 entities and five PART_OF relations. Partial capture, not a successful complete extraction. |
| E-0226 and E-0227 overnight selection | Returned to Core c95dba7 and run-21's ontology. The stager also restored the old skill. Two fresh Sol populations produced zero relations. |
| E-0241 and E-0242 end-to-end correction | Restored own-ontology construction and same-session population, but kept run-21's old Core and skill. Both Sol runs again produced zero relations, with 74 and 81 metadata-only claims. |

The earlier Sol population prompt and the overnight prompt are byte-identical
after replacing the administrative run ID. But the skill and project ontology
changed. Source reading, root definitions, packs and canonical history-profile
bytes did not change between those fixed-ontology runs. They were not repeated
samples of one fixed input condition.

The five-relation Sol run and both own-ontology Sol runs all record the same
model, gpt-5.6-sol, and low reasoning effort. Thus neither low effort nor using
another model's ontology establishes an inability to produce relations. The
older Sol result was itself sparse, and later answer counts do not fall
monotonically: the first overnight prose-heavy graph covers four questions
despite having no relations. Record counts, relationship capture and answer
coverage are separate observations, with different ontologies and query versions
in parts of this history.

## What was rolled back

Exact corrective main commit:
723a4f92c4a11d695547d21d3bc213ef80a6b503, Clarify capture accounting and proposition
relationships. Core's handover is handover/2026-09-06-capture-coverage.md.

The old skill requires an assertion naming both relation endpoints and tells
the producer not to derive the relation from a neighbouring sentence. The
correction explicitly allows retained contextual reference to a proposition
without both labels appearing in one sentence. It states that interpreting
source-supported relationships belongs to the producer, while co-occurrence
alone proves none. It also distinguishes proposition identity, optional label
and content, and says the census does not assess semantic completeness.

Those changes matter directly to the reported reluctance to interpret paragraph
context and to the tendency to mistake mapping counts for meaningful capture.
The corrected skill still permits retained evidence references and does not
guarantee useful graph content. It is not an extraction algorithm or a proof
that restoring it will solve the result.

Skill SHA-256 identities:

- Earlier Sol, exactly matching 723a4f9 and 160878c:
  ddc28bbc894dbcd5996bb668d2a72c1534070098394756144095b570c2eacb9d.
- Both overnight and both end-to-end Sol packets, exactly matching c95dba7:
  8278753a08ff8fdbd867c9da212f160f049378b63d55663ed29e5ce73ccd0a81.

The correction remains in the inspected current Core HEAD
2a11240556532c2b6160ac0bfa5ab1165e862fd2. There is no evidence that Core reverted
it. E-0212 and answer-demonstration/HANDOFF.md already recorded acceptance of
the corrected 160878c boundary before the overnight plan selected c95dba7.
This was not a missing Core delivery or a compiler silently loading the wrong
file. The requested older bytes were faithfully staged.

## Mechanical confirmation

Applied Core's existing _assert_guidance check from exact commit 160878c to
the actual five retained producer skill files. Its test source is
tests/contract_compiler/pareto/test_capture_coverage_boundary.py, SHA-256
3a49d670fce7de4eb42da4e2d6b3d01b966cefd77fe88344c9f64308ccc02bf2.

Result: followup-sol-01 passes; overnight-sol-01, overnight-sol-02,
sol-e2e-01 and sol-e2e-02 fail. The guard already tests the removed misleading
rule and the replacement guidance. No new assertion was written to manufacture
this distinction. These are deliberate compatibility checks against the later
accepted guidance contract, not claims that the historical runs violated their
own frozen input manifests.

The first diagnostic correctly stopped when the working-tree test file differed
from its 160878c version. The actual comparison then loaded the exact committed
test bytes in memory. No working-tree or fixture substitution was used.

Retained tool outputs also confirm that the difference was model-visible. The
earlier Sol saw the producer-owns-interpretation and semantic-completeness
warnings. Both end-to-end Sol sessions saw the old endpoint rule, not those
warnings. All three saw the named-subject, census-inspection and stopping
instructions. This is an exposure check, not a claim about comprehension.

## Why the paper checks missed it

followup.py selects every skill file with git show at the requested core_commit.
The overnight plan selects c95dba7 to preserve original B's historical baseline.
e2e.py and test_e2e_condition.py then require the original run-21 input closure.
They prove exact identity and same-session sequencing, not that the selected
version includes corrections already accepted elsewhere in this task.
Reran test_e2e_condition.py and test_e2e.py: three tests and two subtests pass
against those same old-skill packets. The missing regression check is observable,
not inferred from the overall green test count.

Historical replication and testing the improved project became conflated.
Preserving old results is necessary; forcing every new adoption run back onto
their old instructions is not. The explicit historical pin made the regression
reproducible rather than preventing it. Existing Core guidance guards were not
applied to the new staged producer packet. My previous RCA compared the new
Sol runs mainly with Opus's historical inputs and missed the intervening
corrected Sol condition.

That is the root cause of the confirmed input-selection regression. It does
not by itself establish the root cause of the zero-relation model outputs.

## What the runtime checks rule out

Verified every installed source-package blob against exact Core c95dba7 before
the diagnostic. Reopened the earlier Sol, original Opus run-21 and both new
end-to-end ledgers through its public KnowledgeChangeHistory API. All four graph
exports exactly match their retained exports, all receipts reproduce, and the
ledger bytes remain unchanged.

Re-adapted the earlier Sol's exact retained capture and records on c95dba7.
The resulting population-plan bytes exactly match its original plan from
160878c. Public population compilation returns CHANGE_SET with all 41 entities
and five relations. This was a pure compilation/replay check, not a new admission
or producer run. The older runtime can carry the known-good relation records.

Between these two Core commits, the only changed file under src/malleus is
population.py, adding structured CSV/JSONL locator resolution. The document
adapter, ontology compiler, graph and history/replay code are unchanged. The
new locator check is outside this application/json document-reading path.
The guidance correction itself changes only skill, docs and a wording test.

Together these checks rule out a dropped-edge or missing document-runtime
capability as the explanation of these particular outputs. They do not claim
that all Core behavior or all future inputs are regression-free.

## Why these populations contain no useful scientific graph content

The immediate loss precedes the runtime: the producers submitted no edges and
no endpoint entities. Every new end-to-end graph entity carries only an
assertion locator, modality and statement digest. Source paragraphs survive in
retained capture evidence, but their names, values and relationships do not
survive as graph fields. Neither description nor statement was removed from
the allowed Claim surface; both remain optional and available in all compared
surfaces. The ontology did not force metadata-only records.

The discriminator remains page:1:block:005. Both new producers saw the complete
paragraph, and both authored a BOUNDED_BY-capable ontology. Both still represented
the paragraph only by a metadata claim. The old endpoint instruction is therefore
not a sufficient explanation for every omission. The producer logs describe a
broader reluctance to decompose source language into records without risking
invention. This is the recorded strategy, not an isolated causal result.
02 also cites the reading's licence when explaining why it withheld claim text.
That is an additional producer-reported rationale, not an endorsed legal
interpretation and not an explanation of both runs.

The harness then accepts the first structurally valid submission without a
census-guided capture continuation. The skill requests such inspection, but
no semantic feedback phase occurs in this condition. Mapping metadata fields
with no declared gaps reports FULLY_FORMALIZED, which does not certify scientific
capture. This is a latent workflow weakness shared with the successful Opus
condition, not a newly demonstrated runtime regression.

There is also a delivery defect: nested tool-output truncation. 01 recovered
all 186 full source blocks; 02's displayed outputs only establish 166, and its
skill read did not reach the final portion. Both had a truncated population
surface response and later made narrower surface reads. Matching input hashes
does not prove all instructions reached the model. The all-blocks-received 01
result prevents assigning the entire failure to truncation.

Sol's low effort is observed in session metadata, not guessed from its output.
Current OpenAI documentation confirms that selecting a subagent model without
an effort override can choose that model's default instead of inheriting the
parent's effort. This explains why model and effort need separate recording;
it does not prove a low-effort failure here. The earlier five-relation Sol run
was low too. [Official subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Corrective options, not implemented

1. Separate a historical replication baseline from the baseline for testing
   accepted project improvements. Keep every prior run unchanged. Have the
   author select the next improvement coordinate explicitly; do not silently
   move to current main or assume the old pin carries later fixes.
2. Before a new current-adoption dispatch, validate the staged skill with the
   existing applicable Core guidance guard as well as its digest. A historical
   comparison using older guidance must be explicitly labelled, not silently
   count as testing the corrected project. Pin and check actual model/effort.
3. Verify complete bounded delivery of source and required instructions, not
   merely presence on disk. Preserve the tool-output truncation evidence.
4. For causal confirmation, compare old versus corrected guidance under one
   otherwise fixed producer condition. Do not simultaneously change ontology,
   model effort, query selection and feedback. Richer records must still pass
   source-grounded review; more relations alone is not success. If correction
   does not help, test task-purpose interpretation separately.

No new Core semantic evaluator, relation quota, paper-specific Core schema or
training requirement follows from this RCA. Core already shipped the identified
guidance repair. The remaining selection and experiment controls belong here.
Cross-model purpose handoff remains a separate deferred research question.

Evidence roots: private/paper-v4-answer-demonstration/{followup-sol-01,
overnight-sol-01, overnight-sol-02, sol-e2e-01, sol-e2e-02};
private/paper-v4-v4-run-21; the exact commits and test above; ledger entries
E-0212, E-0226, E-0227, E-0241 and E-0242. Producer session IDs and metadata
are retained with the run packets and in the Codex transcripts. No source
truth, human ratification or new experiment result is implied.
