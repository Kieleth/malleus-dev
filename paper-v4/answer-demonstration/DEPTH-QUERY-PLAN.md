# Retrieve depth quantities without accepting arbitrary numbers

E-0277, master 1.5.21. Luis approves the proposed query-only TDD fix.

1. RED: synthetic microseismicity depth must be retrieved with its original
   fields and subject. Require explicit quantity_kind_class Length and a numeric
   value_lower or value_upper. Reject non-length, count-only, ratio-only, unknown
   dimension and nonnumeric candidates. Preserve zero and one-sided bounds.
   Do not infer dimensions from units, identities or source text. Do not widen
   matching globally or change any other question program.
2. GREEN: replace only earthquake_depth's selection. Reuse quantified with the
   two bound fields, add the explicit microseismicity term and Length check.
   Projection, subject handling and all twenty-nine other programs remain fixed.
   Frozen historical readers stay evidence, not a runtime fallback.
3. Extend the existing relation_query comparison executor with one explicit
   depth-selection condition. Bind the accepted sol-qualification-01 result and
   replay identity. Historical scope-only tests must use their historical query
   bytes rather than accidentally inheriting today's selector. Freeze new query
   bytes before executing; reproduce the old queries from their frozen reader.
4. Requery all thirty without source/network/embedding reads. Check the sole
   authorised question delta, unchanged shared rows/paths, exact graph projection
   and trace closure, unchanged ledger/receipt/graph and byte-identical repeated
   outputs. Record added and excluded candidates, not just total counts.
5. Report remaining source and selection limits. Candidate retrieval is not a
   semantic answer grade. No missing seafloor datum, observational origin or other
   qualifier may be invented. No historical review or full-suite score changes.

This is a paper-owned read-instrument correction, not a new capture, general
query planner or missing Core capability. No new producer/reviewer dispatch,
Core code, manuscript, dependencies or Git changes are part of this cut.
