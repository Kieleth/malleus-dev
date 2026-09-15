# Warehouse extension self-check

Scope: Shop adopter code and its three additive activity values only. The
Malleus acolyte skill, adoption guide and rubric v12 were read completely.
This is not a Core, paper or package audit.

- Authority: the Shop YAML owns activity values; the retained mapping owns
  source-label translation. Core still owns compilation, contract revision,
  admission and replay. No default profile or Shop vocabulary is promoted into
  protocol authority.
- One history: the original ledger is preserved as an exact prefix. Revision
  and warehouse changes are appended to it. The graph is obtained by replay,
  never directly populated by a second write path.
- Source: the publisher image was inspected visually. All 13 rows and 52
  nonempty fields are transcribed. Every new populated property has a derivation.
  Digests catch byte drift, not transcription truth. Source trust is Luis's
  stated experiment assumption; no independent human transcription audit is
  claimed.
- No silent fill: no actors, machines, unit identities, missing warehouse
  steps, calendar years or timezones are fabricated. Extra row fields and
  unknown units refuse. The three original source gaps remain intact.
- Reader: all new occurrences are reached through per-object views, with
  public record-to-source traces. The display does not certify causality,
  duration or a complete queue. Old one-source reader bytes remain frozen.
- Transaction boundary: individual Core admissions remain atomic. This
  fixture driver does not claim whole-import rollback or interrupted-run
  resume. A non-baseline prefix refuses before writing.
- Reuse: no dependency, Core runtime, general interpreter or public package
  changes. Existing public contract-revision and maintained-replay surfaces
  suffice. No upstream requirement was needed.

The executable test runs the schema inspector with absolute root/import paths
and checks its exact success verdict. Final command receipts are recorded in
the parent [validation journal](../VALIDATION.md).

## Read-side ordering comparison

The acolyte skill was reloaded before this continuation. Its scope boundary
keeps the comparison in Shop: existing source, schema, history and Core stay
unchanged. A separate JSON specification selects units and stage pairs but
contains no expected answers. Eleven controlled test cases distinguish the
read rule; three integration cases exercise the actual history and trace.

All five units remain visible in the denominator. Missing or repeated
observations, unusable times, ties and non-forward stage pairs cannot become
proof of order. The result establishes one recorded reversal, not complete
FIFO behavior or a cause of delay. Every selected occurrence and unit link
carries the existing public source derivations. Reopen and maintained replay
agree, and reads preserve all ledger bytes. No new graph, authority, generic
inference engine or protocol API is introduced.

This is an implementation self-check, not an independent review. Exact
commands and immutable regression evidence belong to the validation journal.
