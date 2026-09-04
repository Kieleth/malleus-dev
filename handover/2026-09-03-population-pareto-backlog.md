# Population path: Pareto cut and deferred hardening

This note records the cut selected by Luis on 2026-09-03. It is not another implementation gate.

## Ship now

Finish the neutral population path from retained source evidence to a `KnowledgeChangeSet`, one append-only history, and a replay-derived graph. Retention bindings declare which ledger roles each event type may carry. The current Small Shop fixture uses that binding. Previously published evidence remains immutable; current evidence gets a new version when an identity changes.

After this invariant passes its focused tests and the active Small Shop suite, move to the public facade. Do not expand this piece with general migration or adversarial machinery.

## Defer until a real consumer earns it

- Reading or migrating the old private history-binding grammar in a new runtime.
- Same-file ontology evolution and historical-schema replay.
- Concurrent-writer compare-and-swap across population preparation, retention, and admission.
- Fuzzing and pathological JSON depth, size, or custom Python mapping objects.
- Exhaustive permutations of otherwise valid event, role, and artifact combinations.
- The full `DomainHistoryProfile`, including domain-time, completeness, change-kind, and projection semantics.
- Operation-level provenance, generic fan-out, Event-to-Event ordering, Signal population, and Semantic Re-entry.

Promote one of these items only when a public contract needs it or a concrete reproducer shows that the current path cannot serve an adopter. Until then, preserve it as roadmap work rather than blocking the executable end-to-end path.

## Promoted out of this list on 2026-09-04

Event materialization was deferred here on 2026-09-03 and implemented on 2026-09-04 under Luis's overnight relay instruction, not because a public contract or a concrete reproducer earned it. `af176fe` admits the `events` and `event_participations` families when the bound domain-history profile declares an Event ontology role, `6990658` restricts that admission to the declared role, and `13f11aa` restores the canonical operation dependency order that the new family had disturbed. Event-to-Event ordering, Signal population, operation-level provenance, generic fan-out, and Semantic Re-entry stay deferred.
