# Reconcile six quantities with source context and actual accepted fields

This is one RCA-guided amendment of an accepted graph, not fresh acquisition or
a question-blind comparison. Read the whole selected document. Interpret earlier
assertions in light of later definitions, captions, methods and qualifications.
Do not transfer context across subjects, populations, methods or stages without
evidence. The existing graph and captures are representations to inspect, not
independent evidence that their meanings are correct.

The six targets are listed in inputs/reconciliation-context.json. That view copies
actual target records, existing one-hop subjects and schema declarations without
paraphrasing them. The full graph and five historical captures are also supplied.
Examine subject identity and definitions, cited interpretation versus measurement,
existing field presence versus missing context, summary versus specifically
identified estimate, and depth reference across passages. These categories expose
known problem areas, not expected replacement values. Nothing requires a change.

Propose only fresh same-type versions of these six existing entities. All numeric
value_lower/value_upper/count/ratio_value and unit fields must remain byte-equivalent
as JSON values. Report a necessary numerical correction out of scope, do not make
it. Other contextual properties may be added, corrected or removed if the source
supports that exact change. Do not keep an unsupported classification just to pass
a check. Preserve unaffected qualifiers. Use only the existing ontology's fields.

For every replaced entity, replace all incident relations atomically. Relation
records may change only their ID and the explicitly replaced endpoint IDs. Preserve
their exact type, predicate, other endpoint and properties. No new independent
entities, relations, events or ontology edits. No in-place edits, merging, no-op
versions or evaluator-suggested values. A representation limitation is a possible
result, but check the actual schema before claiming a missing expressive capacity.

Return work/candidate-01.json with exactly capture, records and supersessions.
Use the supplied existing capture grammar, five explicit record arrays and fresh
record/assertion IDs prefixed reconciliation:evidence:. Map all submitted fields,
including preserved properties and relation endpoints, to source assertions.
Every assertion in this new capture must copy the COMPLETE text of its selected
reading block verbatim. You choose the blocks and formalized_by mappings. You may
copy their bytes programmatically from the declared selected reading. Do not
shorten them, normalize whitespace or invent quotes. Multiple blocks can support
one interpretation. A full block is an evidence address, not a claim that every
sentence shares one modality or describes one semantic object. Distinguish the
particular meaning being represented in the records and reconciliation account.
Unexamined blocks stay UNTOUCHED; do not manufacture nothing_assertable entries.

Return work/candidate-01.report.json with exactly:

- schema: malleus.paper-v4.reconciliation-report/v1
- assessments: exactly one entry per target, with record_id (old ID), status
  (AMENDMENT, NO_CHANGE or UNRESOLVED), contexts (nonempty list).
- changes: exactly one entry per added, changed or removed entity property,
  with record_id (old ID), property, reason and evidence. No entries for mechanical
  relation retargeting. Explain why each cited passage applies to this quantity.
- out_of_scope: a list of explicit textual limitations or required changes outside
  this scope. Empty is permitted. Do not hide uncertainty as a completed result.

Each contexts entry has exactly status, statement, graph_refs and evidence.
Status is REPRESENTED, MISSING, PROPOSED or UNRESOLVED. State the concrete meaning,
not merely that you read a record. A REPRESENTED claim requires one or more exact
existing graph references; a PROPOSED claim requires exact proposed references
and source evidence. MISSING and UNRESOLVED may have empty references. Distinguish
presence of a field from faithfulness of its meaning. An existing value may itself
need correction. Do not assert an existing property or subject from memory.

Each graph reference is {record_id, path, value}, using a nonempty array path such
as ["properties", "subject"] and the exact actual JSON value at that path.
References in REPRESENTED/MISSING/UNRESOLVED resolve against accepted records;
PROPOSED references resolve against your candidate. An absent path cannot support
a claim of existing representation. Use MISSING to report absence honestly.

Each evidence reference is {capture_sha256, assertion_id}. Historical capture
digests are in inputs/capture-catalog.json. Assertion IDs are scoped by the capture
digest, never globally unique. For your proposed capture, compute SHA-256 of its
compact canonical JSON bytes: json.dumps(capture, ensure_ascii=False,
sort_keys=True, allow_nan=False, separators=(",", ":")).encode(), no newline.
Prefix the digest with sha256:. Use that digest in the report, not a filename or
the digest of the whole candidate. Do not duplicate quotes in the report. Every
changed property needs one or more evidence references. Historical evidence may
also be cited; all newly captured assertion statements must be complete blocks.

If no amendment is justified, return the report with no AMENDMENT entries and an
empty changes list, plus work/refusal.md. Do not create an empty candidate. Stop
after the first submitted result. At most two exact structural returns are allowed,
each as a separate retained candidate/report. No semantic feedback or extra sample.
Do not run admission. Independent assessment may withhold the whole batch.

Read only this task and declared inputs. No questions, query code, earlier reviews,
other runs, network or delegation. You are not alone in the workspace. Write only
producer/work here. Read every input frame before authoring: skill first, selected
reading next, then the rest. List counts with:
`/Users/luis/Projects/malleus-dev/.venv/bin/python {RUN}/evidence/input_delivery.py --run {RUN}/evidence --phase initial`
Invoke once per part with --target TARGET --part N, one frame per tool output,
at least 9000 output tokens. Re-read truncation. The helper is execution
infrastructure only; do not inspect its source. Notify the coordinator after all
frames are read, before authoring, without waiting. Actual delivery is verified.
