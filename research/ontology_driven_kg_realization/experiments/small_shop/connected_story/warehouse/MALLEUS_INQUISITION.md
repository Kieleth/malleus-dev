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
