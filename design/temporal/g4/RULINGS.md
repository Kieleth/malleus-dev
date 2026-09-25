# Temporal first cut: Luis's rulings

One ruling per entry, in the order taken. DECISION.md holds the options.

## R-01, 2026-09-24: target naming (G1 OC-01, DECISION.md decision 2)

A transition and a correction always name the record they act on. Core infers
no target from subject, property or start time.

Luis: "correct, always explicit, enables full provenance/traceability, even in
the temporal domain."

## R-02, 2026-09-24: representation (DECISION.md decision 1)

Option A: every version is its own identified record in the one graph that the
semantic ledger produces. Grouping by membership records only where a case needs
a group. No second store: not SQLite, not a native temporal store, and not an
external index kept beside the KG. Anything Malleus holds is stored in the KG and
enters as semantic ledger transactions.

Luis: "yes, A, no second store, truly, anything needs to be stored in the KG
itself and as semantic ledger transactions, no external tools, otherwise keeping
them in sync is going to be a total nightmare"

Consequence: G2b (SQLite) stays as research evidence only. The "index under A"
option in DECISION.md is withdrawn as an external tool; any future speed-up must
be derived inside Core from the ledger.

## R-03, 2026-09-24: what a transition records (DECISION.md decision 3)

A transition closes its target's valid period at its own start, as Core does
today, and the history records that the closing kind was TRANSITION. The target
stays believed for its closed period. A correction records kind CORRECTION. The
current graph keeps today's meaning: records not replaced.

Luis: "correct, fully, indeed, next"
