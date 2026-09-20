# Where the argument connections were lost

2026-09-13. E-0374. Read-only audit of frozen run-26. No new population,
review, score, Core change or manuscript claim. Semantic interpretations below
are this investigator's source readings, not a new independent assessment.

## Conclusion

The stored representation preserves observations and hypothesis status more
consistently than the argument connecting them. In the cold-lithosphere case,
the producer used the contrary observation to set NOT_SUPPORTED, so it did not
simply overlook that passage. The derivation of that status still reaches the
passage. What is absent is an explicit graph relationship between the evidence
records and the hypothesis.

The loss is already in the submitted population. Core preserves all its records
and reproduces all thirty queries. The schema and query binding can carry the
missing relationship kinds. This rules out record loss in this run, not every
possible runtime or reading defect.

There is also a concrete task-design conflict. The exact skill delivered to
run-26 requires one assertion to name both relation endpoints and says an
implied relationship from neighbouring text is a gap, not a derivation. We want
contextual argument capture, yet this frozen condition discourages part of it.
Core already changed that guidance at 723a4f92. Run-26 used the older c95dba7
condition intentionally for comparison; it is not a test of the corrected skill.
This instruction conflict is demonstrated. Its causal contribution to each
model omission is not measured.

## The source-to-record contrasts

| Case | Captured mapping | First demonstrated omission |
| --- | --- | --- |
| Successful depth evidence | Assertions 0072 and 0208 each formalize a SUPPORTS record's predicate and both endpoints. Their source blocks are p2b006 and p8b001. | None in the examined chain: both links survive, are returned by five questions, and were labelled supported in the frozen review. |
| Cold-lithosphere argument | Assertion 0082 maps the morphology passage to claim:rc2-magmatic-origin and to claim:h-cold-lithosphere's NOT_SUPPORTED status. | It maps no argumentative relation. The status has source provenance, but the observation-to-hypothesis edge is absent. |
| Off-axis evidence in that argument | One source sentence is split into assertion 0084, the seismic observation, and 0085, beginning with indicates and carrying the inferred boundary depth. | Both sets of quantities are formalized; the evidential connection between them is not. This is within p3b001, not a cross-block reading failure. |
| Degassing argument | Assertion 0119 maps the preferred-mechanism passage to the hypothesis's PREFERRED status and subject. Assertions 0123 and 0124 separately capture a pressure-trigger premise and the proposed earthquake explanation. | The premise and conclusion are mapped separately without an argument edge. The capture retains the wording but does not expose that relationship as a graph link. |
| Uncertainty subject | Assertion 0187 creates dataset:final-catalog. The next assertion, 0188, captures the updated horizontal uncertainty but leaves its subject unset. | The referent exists in adjacent retained context but is not assigned. The exact formalizing sentence names geographic counts, not the catalogue. The single-sentence subject rule is relevant; deciding the proper population still needs source review. |

Here p3b001 means selected-reading block page:3:block:001, and assertion 0082
means assertion:0082. IDs and numbers identify existing records, not proposed
population facts. No edge or subject is authored by this audit.

The successful statements use support and indicate. The failed cold-lithosphere
passage also uses indicates. Missing cue words are therefore not a sufficient
explanation. Nor does one missing cross-block connection explain every case.
The records show selective mapping choices, not access to the model's internal
reason for making them.

## What the graph and reader can already do

ResearchRelation declares SUPPORTS and CHALLENGES with Entity endpoints.
The relevant observation and claim types are on the accepted surface. The two
question bindings contain 100 and 64 ResearchRelation type-pair cases,
respectively, including Observation-to-ReportedClaim,
DepthObservation-to-ReportedClaim and ReportedClaim-to-ReportedClaim. Those
connections would not be hidden solely by an omitted type-pair case.

The two existing method-to-claim links appear under CQ-T2-02, CQ-T3-04,
CQ-T3-05, CQ-T4-03 and CQ-T5-04. They do not appear in the two target questions,
whose type sets omit Method. They concern different claims, so including them
there would not answer the missing scientific arguments anyway.

Public trace_population_record on the replayed cold-lithosphere claim returns
the status derivation at assertion:0082; the degassing status reaches 0119.
Thus some explanation is accessible through evidence tracing already. A reader
could inspect that source context under a declared provenance-aware condition.
That is distinct from storing a typed argument path. Shared provenance alone
must not be silently converted into SUPPORTS or CHALLENGES, or retrospectively
credited as the missing graph relationship in the frozen evaluation.

## Why the current checks did not demand the connection

The frozen skill explicitly explains how to derive hypothesis status and how to
split modalities. It separately restricts relation derivation to one assertion
naming both endpoints. Every examined missing-link assertion has mapping targets
and no declared gap. Those checks can establish supplied-field coverage while
leaving an unrepresented connection unreported. They do not compare the full
meaning of a source argument with its representation.

Core's correction, commit 723a4f92c4a11d695547d21d3bc213ef80a6b503,
tree 64df70da371159e92af470cda1efff12c06571d1, changes the skill, documentation
and tests, not runtime code. It distinguishes proposition identity from a source
label, permits enough retained context without both endpoint labels in one
sentence, and warns that mapping counters do not measure semantic completeness.
The live skill contains that relationship correction. Its separate subject
naming rule remains; do not assume the relationship correction fixes subjects.

## Recommended next action

Do not design another generic relation mechanism or restart the same frozen
capture and call it progress. First approve a controlled input contrast using
Core's already-landed relationship guidance, with the old condition retained
as a control. Keep execution code, source, model/settings, reader and evaluation
fixed; identify the exact instruction difference. Do not silently replace all
Core bytes or mix a changed model into the claimed treatment effect.

The treatment should ask for contextual relationships and an explicit unresolved
reason where needed, not mandate particular edges or a quota. Compare source
faithfulness and actual argument paths, preserving the successful depth links.
A guided repair remains useful for measuring accepted-state improvement, but
cannot by itself establish better ordinary acquisition. The subject case is a
separate follow-up, not an unannounced second treatment.

No new Core implementation request is established. The existing correction must
be deliberately consumed and tested before asking Core to fix it again. Launch
scope and input identities still require approval; this audit launches nothing.

## Mechanical verification

Core c95dba7b86bb61487bda9a52458e1ea47cce20ab was exported from Git into a
temporary directory using the existing paper pin helper. The audit imported
its public compiler, reopened the existing ledger, replayed, and ran the frozen
reader without writing new query files. Results:

- All 445 entities, 3 events and 152 relations equal their submitted values.
- Replayed export and receipt equal the retained bytes.
- All thirty query objects and the graph-state digest match exactly.
- File-read, network and embedding-import counters are all zero during querying.
- The ledger remains byte-identical, SHA-256
  a9da942f9190ddb9b5eb256bf9151973302de7e52b4fbf9e2dd938072c90d0b9.

The first diagnostic invocation incorrectly expected a list from the guard,
which actually exposes three named integer counters. It failed that audit
assertion after the export/receipt/query comparisons, not a Core operation.
The corrected invocation checks exact counter keys, equality with the retained
result and integer zeros. The existing test_pipeline.py source-free guard test
already fixes this counter shape and verifies an attempted read is refused.
No runtime or frozen artifact was changed to accommodate the diagnostic.

Exact inputs and source locators remain in the run-26 review manifest. Detailed
paths: producer/work/document-population.json, ledger/retained-capture.json,
results/export-records.json and query/query-result.json under
private/paper-v4-v4-run-26; the installed skill in that producer's .claude/skills
tree; the public run-26 population surface and native query binding.
