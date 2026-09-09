# Preserve relation endpoint scope

E-0263. Luis requests the fix in TDD. Master 1.5.18.

1. RED: synthetic relations with distinct endpoint subjects must return each
   subject separately and trace its exact ID. Test absent subjects, missing
   references, one-hop limits, field preservation and review-docket identity
   closure. No paper answer values in implementation tests.
2. GREEN: reuse the existing entity-row subject projection inside the active
   relation projection. Preserve source/target properties and relation paths.
   Add source_subject/target_subject only for explicit subject references, with
   matching witness IDs. No fallback to the incomplete active projection.
   Frozen historical code stays untouched as experimental evidence.
3. Freeze the new query bytes before executing on sol-argument-01's accepted
   162-record history. Reproduce all thirty original query objects using their
   frozen bytes. Requery with the new projection and unchanged subject-aware
   selectors. Check that stripping only the new context fields reproduces each
   old row, that selections/paths are unchanged, and that every context has a
   public provenance trace. Never read source text during querying.
4. Repeat the read, check exact outputs and unchanged graph/ledger/receipt, then
   document the mechanical result. Do not infer full coverage or overwrite the
   prior independent review. The current broad subjects contain no RC2 label;
   the fix must not manufacture it from the hypothesis.

This is a query-only correction. A later model-authored amendment may select
existing scoped observations, but no producer or graph mutation is part of
this TDD fix. No Core, manuscript, dependency or Git mutation.
