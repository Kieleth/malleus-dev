# Next-run preparation, 2026-09-13

These checks repair the known preparation defects without changing historical
producer inputs, question files, captures, graphs or review judgements. No new
producer or reviewer is authorized by this file. Frozen v3.2 remains historical.
E-0395 supersedes its inherited blanket figure/table exclusion for future
preparation. A successor measurement must declare the corrected scope; these
checks do not rewrite an old protocol, regrade results or prove complete capture.

## Document scope and modelling responsibilities, E-0395

Figures and tables, including captions and legends, are legitimate document
evidence. Do not impose a body-text-only or text-recoverable-only scope in place
of the rejected blanket exclusion. The current text reading is one retained
view of the document, not proof that all its information has been captured.
When layout, table associations or visual relationships are missing or ambiguous,
record the evidence gap and retain the exact additional artifact and locators
before claiming its interpretation. Never infer unseen content or label that
capture gap absent from the source. Any changed input view is a new identified
condition, not a silent substitution into a frozen run.

Run `next_run.py check-document-scope --questions PATH` before new document
preparation. The future question scope must explicitly mark `figures` and
`tables` as `INCLUDED`; missing fields and the old exclusion refuse. The same
check runs inside baseline preparation before writing and inside semantic graph
review preflight against digest-checked question bytes. It checks eligibility,
not whether figures or tables were actually extracted. Historical question
files intentionally fail and must not be edited to pass.

The next modelling cut uses the author's three responsibilities:

1. Evidence: keep each original block/source artifact unchanged and locatable.
2. Meaning: identify coherent propositions or metadata, preserving their context
   and qualifications. A block can support several units; a unit can need several
   blocks. Retain those links, including context needed to finish a fragment.
3. Classification: define the scope and meaning of categories actually used,
   with a distinguishing example or counterexample. Apply a category to the
   content it qualifies, not to every item sharing a page or source locator.

Atomic next deliverable: a bounded representation proposal for the already
identified mixed-content cases, showing evidence/context, proposed semantic
units and applicable definitions separately. Do not supply expected answers,
hand-author replacement population or broaden labels just to pass review.
Define the representation before another repair. Any generated amendment still
needs explicit scope, independent source assessment and preservation checks.
This file launches no model and changes no accepted ontology or record.

## Before freezing questions

Assess every required element of every NOT_IN_SOURCE or EXCLUDED_SURFACE
control against the whole selected reading. Paraphrases instead require exactly
the same semantics as their positive question. Do not reject them for being
answerable. Record an identified human or model assessor, exact question/reading
digests, and one entry per absence-control element: question_id, semantic,
finding (IN_READING, NOT_IN_READING or UNCERTAIN), blocks and reason.

Run evaluation-v4/control_screen.py with the questions, reading and assessment.
Presence, uncertainty, missing elements, bad identities or contradictory
locators refuse. Passing means the assessment is complete and consistent, not
that code proved natural-language absence. The assessor must search the full
selected reading and explain the subject and scope of each element. An empty
graph result is never evidence that the reading lacks it. An independent
assessment is preferred; no independent new assessment was launched in this cut.

The existing set-B freezer now requires this assessment before writing and
refuses overwriting its existing frozen file. It is not a generic new-set
authoring tool. A future set requires a newly identified destination and its
own authorship metadata. Do not re-freeze set B or alter old scores. The
read-only audit_controls.py command derives the existing set A, revised set A
and set B assessments from their retained reviews. Derived assessments are
explicitly not independent judgements.

## Before another baseline or graph review

Use next_run.py as the current preparation/check implementation. Old per-cell
scripts are historical reproducer bytes, not templates for new launches.

The prepare-baseline command requires reading, questions, answer schema,
control assessment, declared model and a new output directory below private/.
It places producer-input-receipt.json at the path its generated TASK.md names.
The task states the exact declared model string, rather than asking the producer
to guess a display-name alias. The check-answer command checks the answer's
model, task and input digests against that receipt and rechecks the staged bytes.
It does not judge answer grammar or meaning; the answer validator and source
review remain separate required steps. Launcher model/settings metadata must
also be retained, since an output field is not execution attestation.

For graph reviews use count-witnesses on the exact query result. It counts
distinct witnesses of returned rows, not all records visited during provenance
tracing. Run-25 is the regression: 505 judged witnesses, 506 traced records.
A subject reached only for tracing must not add an unjudged witness.

Before a future graph semantic review, run `next_run.py check-review-context
--manifest PATH`. The manifest must supply `accepted_ontology` and
`ontology_import:<import locator>` materials for every transitive import, using
the source's exact import strings. Their paths are repository-relative or
absolute, their digests bind exact bytes, and `stage_identities` must identify
the same accepted ontology. The check performs no network resolution. A
structural surface alone is insufficient: it omits descriptions and meanings.
The reviewer must actually read these sources; a passing preflight does not
prove delivery to the model, comprehension or semantic adequacy. Do not change
old review manifests to make them pass this prospective check.

Before treating different grades as a capture gain, inspect every earlier
returned field, including statement prose, for the supposedly new information.
Separate presence, correct classification and source-surface eligibility.
Six credits citing new records do not prove six previously absent elements.
Retain individual source-grounded support decisions; a block-ID prefix and a
verbatim text match must not default to supported. The RCA counterexample in
test_relationship_repair.py shows why. This remains an assessment obligation,
not automatic semantic validation or permission to launch another reviewer.

No model aliases, historical task fixes, changed source locators or manufactured
claims are smuggled into old runs. The existing valid-time and Core pins stay
unchanged. Broader launch orchestration remains a future experiment decision.
