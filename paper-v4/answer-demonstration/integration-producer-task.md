# Integrate quantitative assertions with their source context

This is one integration pass over an accepted graph, not fresh extraction. Read
the complete selected document, ontology, existing records and all five retained
captures. Identify quantities whose interpretation depends on definitions,
captions, methods or other passages beyond their initial assertion. Revisit earlier
records when relevant context qualifies or contradicts them. Do not treat an
earlier capture or an accepted record as independent evidence. Do not transfer
context between different subjects, populations, stages or methods without source
support. Preserve distinctions between observations, calculations and hypotheses.

Use only the existing ontology and legal fields. Propose fresh same-type versions
of existing quantified entities, with all changed incident relations retargeted
atomically. No new standalone entities or independent relations, no schema edits,
no merging records, no in-place modification. Report a representation limitation
if this boundary cannot express the necessary context. Existing values stay exact
unless you identify source evidence justifying a change; every property addition,
change or removal needs an explicit reason and exact quote/block witness. Keep
old qualifications unless the source justifies correcting them. Nothing forces
an amendment, a field, a relation or a successful outcome.

Return producer/work/candidate-01.json with exactly capture, records, supersessions,
using the supplied capture grammar. The five record arrays are explicit. Only
entities and dependent relations may be nonempty. Use fresh record/assertion IDs
prefixed integration:evidence:. Map every submitted property and both endpoints
to retained source assertions, including preserved content. Do not invent evidence
or block dispositions. Unexamined blocks remain UNTOUCHED. Do not run admission.

Also return producer/work/candidate-01.report.json with exactly schema (value
malleus.paper-v4.integration-report/v1), assessments and changes. Assessments has
one entry per existing entity with a numeric value_lower, value_upper, count or
ratio_value: {record_id, status, reason, evidence}. Status is AMENDMENT, NO_CHANGE,
UNRESOLVED or ONTOLOGY_LIMITATION. State the actual conclusion, not a claim that
every possible qualification was found. Each evidence item is {block, quote},
with a nonempty verbatim quote from that selected-reading block. Evidence may
be empty only for non-amendment assessments where no source basis was resolved.
Changes has exactly one entry per changed entity property, including additions
or removals: {record_id, property, reason, evidence}, using the OLD record ID.
Each change requires evidence. No changes entries for mechanical relation
retargeting. Explain why the cited context applies to this quantity specifically.
The machine checks exact witnesses and scope, not the truth of your reasoning.

If no scoped amendment is justified, still return the report with no AMENDMENT
entries and an empty changes list, plus producer/work/refusal.md. Do not create
an empty candidate merely to force admission. At most two exact structural
diagnostics can be returned. Retain each attempt separately, no semantic coaching
or extra sampling. Stop after your first submitted result.

Read only this task and declared inputs. No questions, query code, earlier reviews,
other runs, network or delegation. You are not alone in the workspace. Write only
producer/work in this packet. Before authoring, read every frame of every input:
skill first, selected reading next, then remaining inputs. List counts with:
`/Users/luis/Projects/malleus-dev/.venv/bin/python {RUN}/evidence/input_delivery.py --run {RUN}/evidence --phase initial`
Invoke once per part with --target TARGET --part N, one frame per tool output,
at least 9000 output tokens. Re-read truncation. The helper is permitted execution
infrastructure only; do not inspect its source. Notify the coordinator after all
frames are read, before authoring, without waiting. Actual delivery is checked.
