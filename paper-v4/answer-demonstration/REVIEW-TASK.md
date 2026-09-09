# Independent source-grounded review of a frozen selective query

This is a new retrospective review, not a revision of a historical evaluation.
You are a fresh model-assisted reviewer. Use CODEX_PRELIMINARY and an actor ID
identifying your task and run. Only Luis can ratify; leave ratification pending.
Do not inspect the other reviewer's output or any previous conclusions.

## Inputs and output

Use only your assigned packet directory. Verify every material digest in
review-input-manifest.json before judging. Read review-protocol.json and
review-extension.md, then review-docket.json. The docket carries all thirty
questions, every row, and every distinct central witness with all projections
and occurrences. Read the whole selected-reading.json as needed, the retained
capture, both traces, the population surface and the exact query programs.
For future packets, also read vocabulary-closure.json and its exact accepted
ontology/import definitions before interpreting fields or enum tokens. A token
name alone does not establish its semantics. Missing declared definition bytes
must stop packet preparation. The first review-01 packets predate this guard;
their definition-context supplements are separate, never retroactive inputs.
Do not read expected_outcome in the separately retained competency question
file before judging. The docket deliberately omits it.

Do not inspect the manuscript, historical reviews, source-inspection notes,
results summaries, producer transcripts, answer keys or external sources.
No network. The PDF, supplements and raster figures are not evidence inputs.
The selected text is the evidence surface, not scientific ground truth.

Copy review-record.blank.md into your assigned output. Edit only its JSON block.
Set PRELIMINARY_COMPLETE after finishing, fill your actor ID and actual UTC
completion timestamp, and bind the exact review-input-manifest.json digest.
Never fill the ratification fields or present this as human annotation.

## One judgment per central witness

The central key is record_id for ENTITY/SUBJECT and relation_id for RELATION.
Judge once across the union of its projected fields in all questions. Include
subject/endpoint fields carried by those projections. Trace each record ID
through query-trace-summary.json: derivation.locator names an assertion in
retained-capture.json; assertion.block names a selected-reading block.

Choose SUPPORTED, PARTIAL, UNSUPPORTED or NOT_EVALUABLE. SUPPORTED means every
material claim in the projection has source support. A correct number cannot
make a wrong subject, unit, interpretation or strength of claim supported.
Missing requested information is not automatically an unsupported record.
Identifiers, trace digests and field names are metadata, not scientific claims.

Cite block IDs, and give a compact rationale in your own words. Do not quote
source passages. Recompute each carried statement_sha256 from the exact
assertion statement. Begin those rationales with DIGEST_OK or DIGEST_MISMATCH.
For SUBJECT/ENTITY, also use SUBJECT_IN_BLOCK, SUBJECT_NOT_IN_BLOCK or
NO_SUBJECT_IN_ROW as appropriate. For relations use DERIVATION_LOCAL or
DERIVATION_NON_LOCAL based on whether an endpoint and the relation share a
derivation block. Locality alone never changes source support. If a locator
cannot resolve, report NOT_EVALUABLE and describe the exact unresolved chain.

## Every question and every required semantic

List every returned row in its original order with its row_index and central
witness_key. For each required_semantics item, in order, name an answering
row_index whose witness is SUPPORTED, or null plus one of NOT_MODELLED,
WITHHELD_STATEMENT, UNREACHED_RECORD, NOT_IN_SOURCE, LOCATOR_NOT_RESOLVABLE.
Give a concise note identifying the answering fields or explaining the absence.
Do not infer a missing fact from the source to fill the graph's answer. Where
the reason is uncertain, state that uncertainty rather than claiming proof
that the entire graph lacks a fact.

Keep quantity subject, site, stage, bounds, units and determination together.
Do not silently pick the intended value from several unresolved candidates.
If stored prose carries a semantic, name its field and say it is prose, not
a typed relation or graph deduction. Evidence links require an actual relevant
connection, not co-occurrence or the mere presence of a preferred hypothesis.
In particular, a missing subject slot does not alone make claim_subject absent.
Inspect the meaning actually stated in the returned fields. This does not permit
using external source context to fill a missing or ambiguous subject.

Derive question_responsiveness: COVERED if every semantic names a row, NONE if
none does, PARTIAL otherwise. No accuracy score. Record ambiguity separately
in responsiveness_rationale, even where individual fields have support.

Assembly is descriptive: NO_ANSWER iff no semantic names a row; otherwise
ONE_ROW if the covered semantics reside in one row, LINKED_ROWS if relevant
returned relations connect the answering rows, UNLINKED_ROWS otherwise.
Uncovered semantics remain uncovered. Do not invent relations to connect them.

Cite source blocks for every question, including empty results. For an absence
claim, cite the relevant source context and describe the bounded search. Treat
controls exactly like the other questions. An unrelated candidate is not by
itself fabrication; empty output is not by itself proof of source absence.

## Record structure and checking

Each witness has exactly witness_key, source_support, source_locators, rationale.
Each question has exactly question_id, question_responsiveness,
responsiveness_rationale, assembly, coverage, source_locators, rows.
Each coverage item has semantic, row_index, absent_reason, note. Exactly one of
row_index and absent_reason is non-null. Each row reference has row_index and
witness_key. Do not introduce answers, scores or other record fields.

Validate with the packet's selective_review.py using --packet and --record.
It checks identities, completeness, enums, cited block membership and coverage
consistency. It does not judge the science or assign labels. Correct only your
own record if malformed, retaining any first completed submission as a separate
file before revision. Do not change packet inputs or the validator.
Return the output path, validation result and any substantive uncertainty.
