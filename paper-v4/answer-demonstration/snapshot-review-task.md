# Review all thirty current PDF answers

Use only this packet. Verify manifest.json and every material digest first.
Read review-criteria.md, qualification-criteria.json, the complete selected
reading, accepted ontology/import definitions, review-docket.json, query-result.json
and resolved-trace.json. The graph inventory is diagnostic evidence, not another
answer surface. Do not inspect previous reviews, producer sessions, manuscript,
other runs, the PDF, raster figures, supplements or outside sources. No network,
delegation, graph/query changes or repair proposals written as population facts.

This is a current snapshot of an iteratively refined history. It is neither
first-pass capture quality nor an assessment of the underlying scientific truth.
The fixed reader returned candidates. Review determines whether their represented
claims are source-faithful and whether they answer the fixed questions.

Assess every central witness once across the union of its projections. Include
the inline subject and endpoint fields. Resolve every relevant record through
its capture-scoped derivations and complete source blocks. Check each carried
statement_sha256 against the exact statement bytes. Do not assume an enum's
meaning from its spelling. Use accepted definitions. In each rationale identify
supported content and any unsupported field or implication, not just missing
requested fields. Missing information is not automatically a false claim.
Record unresolvable chains explicitly. The packet's mechanical closure is not
a semantic source-support judgment.

For every question, assess every required_semantics item in the existing order.
Read the entire question. Name answering fields and exact zero-based row and/or
path indices. Only source-supported returned content contributes. A PARTIAL
witness can supply a supported field; identify that field explicitly. Never
disqualify a supported field merely because another qualification is absent,
and never credit an unsupported field because its row contains a correct number.
Qualifiers can be stored prose; disclose that rather than calling them typed
relations or graph deductions. An evidential path records the authors' argument,
not established physical causation. Follow the prospective interpretation in
review-criteria.md and the existing CQ-T5-01 qualification requirements exactly.

Source or full-graph inspection can explain a missing answer, never fill it.
For an absence, distinguish unreturned content, unsupported candidates, source
limits, inexpressibility and unresolved evidence. Do not infer that the entire
graph lacks information just because a query is empty. All questions, including
controls and paraphrases, receive the same semantic accounting. Do not consult
an expected-answer key or invent a source-absence answer from an empty output.

Write review.json with exactly these top-level fields:

- schema: malleus.paper-v4.current-snapshot-review/v1
- manifest_sha256: SHA-256 of exact manifest.json bytes, prefixed sha256:
- status: PRELIMINARY_COMPLETE only after all work is done
- ratification: PENDING_HUMAN
- reviewer: actor_id, method MODEL_ASSISTED, independence matching the manifest,
  completed_at as the actual aware UTC completion time
- witnesses: one object per docket witness_key, with witness_key,
  source_support (SUPPORTED/PARTIAL/UNSUPPORTED/NOT_EVALUABLE), source_locators
  (selected-reading block IDs), and rationale
- questions: one object per docket question in order, with question_id,
  responsiveness, assembly, answer, and coverage

Each coverage item has semantic, row_indices, path_indices, source_locators,
absent_reason and note. Cite source blocks even for empty answers. A covered
semantic names at least one answering row/path and uses absent_reason null.
Otherwise both index lists are empty and absent_reason is UNRETURNED,
UNSUPPORTED, NOT_IN_SOURCE, LOCATOR_NOT_RESOLVABLE, NOT_EXPRESSIBLE or UNRESOLVED.
The note names the actual supported answering fields, or the missing requirement
and evidence of its absence. Do not introduce new requirements during review.

Responsiveness is COVERED for all supported requirements, PARTIAL for a nonempty
proper subset, NONE for none. Assembly is NO_ANSWER when none is covered;
otherwise ONE_ROW, LINKED_ROWS or UNLINKED_ROWS describes the answering content.
LINKED_ROWS needs a relevant returned connection. The answer is a concise plain
English rendering of supported returned content only; if none answers, state
that explicitly. Do not add a full answer from the source to an incomplete view.

Also write review.md with the full thirty-row table, representative supported,
partial and absent answers, and concrete limitations. Report positive questions,
expected-absence controls and paraphrases separately. Do not supply a truth or
accuracy score, claim human annotation, overwrite historical grades or assert
that a new snapshot total is a longitudinal improvement.

Run the packet's validator, which checks accounting, not the science:

```sh
/Users/luis/Projects/malleus-dev/.venv/bin/python snapshot_review.py validate --packet . --record review.json
```

Only review.json and review.md may be created in this packet. If a completed
submission is structurally malformed, retain it under a numbered filename before
correcting your own output. Never change frozen inputs or the validator. Return
the two output paths, validation result and unresolved substantive uncertainties.
