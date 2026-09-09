# Candidate and reconciliation account

Write producer/work/candidate-01.json with exactly capture, records and
supersessions. Records has entities, relations, events, signals and
event_participations arrays, including empty arrays. Each supersession is
{record_id, supersedes_record_id}, with a fresh replacement ID and an existing
prior ID. Use the accepted record shapes and compiled population surface.

The capture grammar is malleus.document-capture/private-v0. Its top-level fields
are schema, reading_sha256, attribution, assertions and nothing_assertable.
Use the supplied reading digest and source_id from coordinates.json. Attribution
has source_id, author and date, identifying the source as required by the shipped
grammar. Assertions have id, block, statement, modality, formalized_by and gaps.
Use the skill's declared modalities and gap shapes. Each formalized_by entry is
{record_id, path}, where path addresses an actual field on a submitted record,
for example ["properties", "description"]. All submitted fields require evidence
mappings, including IDs, types, preserved properties and relation endpoints as
required by the adapter. The retained base capture illustrates the existing
shape, but is not a replacement candidate.

New statements copy the complete text of their chosen block exactly. Several
assertions may map different fields of one record. Every copied block remains
source evidence, not a claim that all of it has one meaning. Empty gaps is allowed
when justified. Leave unexamined blocks untouched, not nothing_assertable.

Write producer/work/candidate-01.report.json with exactly:

* schema: malleus.paper-v4.reconciliation-report/v1.
* assessments: one entry per supplied target, with record_id (old ID), status
  (AMENDMENT, NO_CHANGE or UNRESOLVED) and a nonempty contexts list.
* changes: one entry per added, changed or removed entity property, with
  record_id (old ID), property, reason and evidence. Exclude mechanical relation
  retargeting. Explain why the cited context applies to this record.
* out_of_scope: a list of nonblank textual limitations; an empty list is allowed.

Each context has exactly status, statement, graph_refs and evidence. Status is
REPRESENTED, MISSING, PROPOSED or UNRESOLVED. Each graph_ref has record_id, path
and value, the exact actual value at that dictionary-key path. REPRESENTED needs
accepted graph references. PROPOSED needs proposed graph references and evidence.
MISSING and UNRESOLVED can have empty graph_refs. Distinguish a present field from
a faithful interpretation of it.

Each evidence reference has capture_sha256 and assertion_id. The supplied capture
catalog identifies the original capture. Assertion IDs are scoped by capture,
not globally unique. For the proposed capture compute its digest from compact
canonical JSON: json.dumps(capture, ensure_ascii=False, sort_keys=True,
allow_nan=False, separators=(",", ":")).encode(), without a newline. Prefix its
SHA-256 with sha256:. Do not hash the whole candidate instead. Do not duplicate
source quotes in the report. Every changed property needs evidence.

If no supported amendment is justified, write candidate-01.report.json with no
AMENDMENT entries and no changes, plus refusal.md. Do not submit an empty
candidate. Draft construction and local JSON checks are allowed; submit once,
preserving the submitted bytes. No admission or semantic retry.
