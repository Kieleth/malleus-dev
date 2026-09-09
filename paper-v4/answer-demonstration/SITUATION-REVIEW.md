# Paper and capture regression review

2026-09-07. E-0249. Read-only investigation requested by Luis after the census
continuation. No new generation, query retuning, Core rebind or code change.

Forward status: E-0250 adopts this review as a standing directive and selects
the [controlled calibration](CALIBRATION-PLAN.md). The later
[question-loss audit](THIRTY-QUESTION-RCA.md) refines the retrieval diagnosis.
The E-0249 findings and then-unselected recommendations below are retained.

## Conclusion

The record does not show one controlled experiment steadily regressing. It
shows several materially different capture tasks, three confirmed paper
workflow defects, and unresolved variability in model-produced representations.
Earlier useful Sol results are real. My recent RCA was incomplete because it
concentrated on the five-relation follow-up and omitted the earlier ultra-effort
v2 result and the successful bounded composition amendment as positive controls.

We can locate the observed losses before admission and explain why the selected
contracts permit them. We cannot yet assign the difference between broad Sol
captures to one cause. Restoring guidance, delivering every input and restoring
same-session ontology construction did not restore broad relational capture.
Calling any one of those the complete explanation was not warranted.

## Vision and where the experiment moved

Luis's original objective was a lean demonstration: a fresh model constructs
an ontology, captures a document through an enforced representation and semantic
ledger, and queries a replayed KG. Small Shop supplies a second, operational
example. Later Re-entry and Robotics extend the question to what an agent
believed, what supported it and what justified changing it. The aim is useful
governed knowledge, not merely well-formed output or a catalogue of failures.

Malleus's current [principles](../../docs/PRINCIPLES.md) agree: typed subgraphs
are composable epistemic modules; encoding, execution, acceptance and assistance
are different claims. Ontology chooses legal structure, history profile chooses
change semantics, and identified checks govern commitment. None alone establishes
source faithfulness or use-specific sufficiency. Core now ships the three-promise
distinction that Luis endorsed. The paper should test all three without pretending
that deterministic structural checks certify source meaning.

The experiment became substantially broader. The early population had four
visible questions, explicit constructible types and required scalar fields.
The [v4 migration map](../experiment-v4/brief-to-skill-map.md) deliberately removed
question-shaped selection and the paper-specific construction list, moved
modelling guidance into the generic skill, introduced packs and partial-import
accounting, and retained one session across ontology and population. Evaluation
later expanded to thirty questions. These are defensible design changes, but
their results are not replications of the earlier task.

## Positive controls that must not be forgotten

| Condition | Actual retained result | Comparison limit |
| --- | --- | --- |
| v2 Sol | 7 entities, 6 relations, 2 bounded quantities; four-query review finds one responsive and one partial answer | Ultra effort; population sees four questions and exact construction rules; separate ontology/population sessions |
| followup-sol-01 | 41 entities, 5 PART_OF relations, 7 Observation records | Low effort, no questions, fixed run-20 ontology; still a partial capture and no SUPPORTS path |
| composition-01 | Sol adds 2 supported SUPPORTS relations; one answer changes from partial to covered through linked rows | Explicit question and requirements; existing rich Opus graph; additions only, not fresh acquisition |
| corrected own-ontology Sol | 9 entities, 2 quantitative observations, no relations | Restored skill, complete delivery, low effort, question-withheld E2E |
| same producer's census continuation | 20 entities, proposition text, no typed quantities or relations | Complete replacement in a separate history; one feedback pass, not an incremental update |

V2 counts were recomputed with the retained summary program and inspected against
population bytes. Its ontology and population rollouts both record
`gpt-5.6-sol`, `ultra`; this is not inferred from the output. The actual population
rollout is `rollout-2026-09-03T02-01-15-01a06680-3b9f-7951-b550-ef2f85f159c8.jsonl`.
The reference producer record's population timestamp hint is inaccurate; its
model/effort claim is confirmed by the located transcript. No token-budget or
equal-resource comparison is established. Later low-effort settings are also
recorded, not guessed. Official OpenAI documentation distinguishes explicit
model and effort selection; it does not explain these particular outcomes.

The successful amendment is especially important. Sol can interpret source
context and propose an evidence link when asked a bounded question over existing
records. It does not establish that it will discover the same links while also
choosing identities, selecting assertions and building a whole document graph.
Conversely, the question-withheld five-relation follow-up means neither seeing
questions nor ultra effort is necessary for any relation generation.

## Demonstrated failure paths

### 1. A real instruction-selection regression

The paper returned from corrected Core 160878c to the older c95dba7 skill while
treating later runs as project progress. Its identity checks correctly verified
the wrong historical condition. The accepted guidance conformance guard detects
that rollback. This is a coordinator defect, now repaired for current adoption.
The [earlier RCA](REGRESSION-RCA.md) establishes the exact commits and checks.
The corrected fresh run still lacks relations, so that repair was not sufficient
to restore the desired capture behavior.

### 2. Representation requirements changed, not just the model

V2's population task requires a QuantitativeObservation to have bounds, a unit
and an observation basis. It prohibits putting relations or untyped facts in
names. Its explicit construction list contains domain records and links, not a
generic metadata-only Claim alternative.

The later compiled surfaces are different. For the Claim types actually used
in the follow-up, overnight, two failed E2E and corrected runs, `id` is the only
required slot. `statement`, `description`, `name` and `subject` are available
but optional. The restored skill explicitly permits either a statement field
or an exact retained evidence reference. The source-assertion adapter validates
the supplied mappings and retained bytes, not semantic decomposition.

This is not proof that optional fields caused the model's choice. It establishes
why a source paragraph represented only by locator, digest and modality can pass.
The E2E producer logs explicitly elect that representation and describe finer
decomposition as an invention risk. Those are recorded strategies, not privileged
access to the model's causal process. The source and ontology support a concrete
counterexample: both failed E2E sessions saw the bounding passage and declared
BOUNDED_BY, yet submitted neither its domain objects nor its relation.

The contract being enforced therefore permits a weaker result than the useful
domain graph the paper aims to demonstrate. Generic partial-import acceptance
is not intrinsically wrong; treating it as a sufficient completion condition for
our capture objective leaves a gap. The three-promise distinction identifies
that gap but does not implement the missing capture procedure.

### 3. Query misses are not capture omissions

The follow-up stores a quantity whose primary-melt qualifier lives on its subject.
Its original query looks only at the observation. A subject-aware query recovers
it without a population change. The corrected E2E stores a qualifier in
`observation_kind`; the old query's fixed text-slot list ignores it. The new
text binding recovers both quantities on the identical graph and ledger.

The thirty-query harness is a specific read instrument, not a universal KG
question-answering agent. Its full/partial/none labels concern returned fields.
Prose can cover a question without graph composition, and a typed value can exist
without being selected. The `ontology-aware` correction fixes one selection
defect, not arbitrary ontologies, vocabulary or query planning.

### 4. The continuation used replacement without preservation enforcement

All three census candidates lack the prior numeric fields before admission.
The two structural returns change only exact statement text and subject aliases.
The query method is unchanged between the old and revised graphs. Core did not
remove quantities. The new capture replaced their typed representation with prose.

I chose a consolidated from-empty condition and did not require an explicit
account of each removed record. The original remains safe, but the revised graph
can be less useful. Importantly, the earlier repair/composition harness already
has `check_preservation` and exact delta/history closure. Preservation is not a
new missing Core capability. Moving to that workflow could prevent this loss
class; it would not explain why the initial broad capture was sparse.

## Fresh checks in this review

Verified the runtime's entire package against Core 160878c, then reopened five
retained histories: followup-sol-01, composition-01, sol-e2e-01,
sol-e2e-corrected-01 and sol-census-01. Every exported graph matches the retained
export, every receipt matches byte-for-byte, and every ledger remains unchanged.
This independently reproduces the five-relation and two-SUPPORTS positive
controls alongside the sparse and metadata-only cases on the same runtime.
It rules out replay loss for these records, not every possible Core defect.

Input hashes, actual model/effort metadata, emitted record types, required slots,
numeric fields, original briefs and the brief-to-skill migration were inspected.
No producer was resumed, no new graph was constructed by hand, and no historical
review was changed. Source-grounded judgments remain model-assisted with their
recorded ratification status. Graph/receipt reproduction is not regenerated LLM
output and cannot prove model determinism.

## What would resolve the remaining causal question

Another broad rerun that changes several conditions will not do it. Neither
will adding incremental capture and declaring the original failure understood.
The recommended next investigation is an explicit positive-control crossover:

1. Use the exact question-withheld followup-sol-01 population packet as the
   closest relation-bearing control. Verify complete delivery and actual settings;
   hold ontology, source, skill, task and query method fixed. A fresh producer
   replay tests whether its behavior is repeatable, not whether the runtime works.
2. Compare that same task at low and ultra effort. If only one improves, it
   supports an effort effect in that condition; it does not prove a universal
   model explanation. One sample per arm is a pilot, not a reliability estimate.
3. Only then isolate task/representation changes against that fixed baseline.
   Keep question exposure separate from question-independent capture obligations.
   Any stronger obligations need an explicit adopter contract, not hidden expected
   answer values or a global mandatory relation quota.

Keep a source-to-record witness for quantities, a named spatial relation and an
evidential link. Inspect whether the producer delivered the source, represented
its content, proposed a link, preserved it through admission and exposed it to
the query. Review all relevant proposed values and endpoints. This distinguishes
the failed stage rather than grading a total and guessing its cause afterward.

These are recommendations, not launched conditions. The user must select the
next intervention. Core remains owner of generic mechanisms and skills; paper
owns this experiment and its semantic assessment. Current Core/Re-entry/Robotics
action-runtime design work is separate and is not a prerequisite for this PDF
diagnosis. We should retain the already useful historical results while improving
the general adoption path, not replace them with the latest run merely because
it is newest.
