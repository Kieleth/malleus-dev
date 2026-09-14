# Shop object views and printed-time ordering

## Selected scope before implementation

The chapter is trusted input for this experiment, as Luis confirmed on
2026-09-14. Its supplier-order correction is the accepted successor. Checking
external source truth is not a prerequisite or a new subsystem in this slice.
Trust does not supply absent fields or repair unusable printed dates.

Reuse the existing connected history, retained mapping, public graph queries,
maintained projection and record traces. Build read-only per-object views with
shared occurrence identifiers. The distinguishing observation is that e30 is
one clearing occurrence in the I1, I2 and P1 views, while A's receipt and B's
update never become successive events on one supplier order.

The read-side display convention parses `DD-MM HH:MM` into month, day, hour and
minute coordinates within this selected source. It creates no year, timezone,
calendar instant, duration or cross-year chronology. This is printed-coordinate
order, not proof of causal or complete domain order. Equal coordinates form an
unordered group. Unusable dates, absent stated times, and February 29 without
a year stay unplaced. A missing required `time_text` field is an input error,
not permission to invent one.

Every object keeps its own sequence. Order views only reference related object
views through the existing invoice, payment, packing and receipt joins. These
are retrospective relationships observed by the selected accepted checkpoint,
not assertions that an item belonged to an order before it was packed. Actors
remain available in their own views but do not enlarge order scope. Unplaced
events are not discarded, and adjacent displayed groups do not establish
directly-follows when an unplaced event could intervene. Event ID order inside
a tie or inventory is only deterministic presentation, never a tiebreaker.

No source, ontology, population, historical receipt or Core file changes.
No new Event-to-Event graph relation, generic ordering framework, source repair,
shipment authorization, external effect, package work, push or release.

## Read the result

The reader references one registry of 21 occurrences from 17 object views:
2 orders, 2 supplier orders, 5 physical units, 2 invoices, 1 payment and 5
actors. State versions are not additional enduring objects.

I2's printed sequence is creation (`e5`), update (`e9`), clearing (`e30`). That
same `e30` is referenced by I1 and P1. B has placement, update, receipt and its
two unpacking occurrences. A keeps its receipt (`e6`) and one unpacking (`e8`)
unplaced, never repaired with B's dates.

O1 references I1, P1, X1, X2, Y1, A and B; O2 references I2, P1, X3, Y2, A and
B. Each also has its own direct order view. These are object references, not
another merged sequence. Every occurrence and each object's participation
links expose public trace witnesses.

Use the existing declared repository environment. If the connected history
already exists, only run the second command. The first requires a new path:

```bash
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.run /tmp/shop-connected-history.jsonl
PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.object_timelines /tmp/shop-connected-history.jsonl
```

In Python, reopen with public `KnowledgeChangeHistory.reopen(path).replay()`,
then call this Shop module's `read_timelines(replay)`. Inspect
`report["objects"]["invoice:I2"]["printed_sequence"]` or
`report["order_views"]["O2"]["objects"]`.

This is a Shop research reader using public Core APIs, not a new installed Core
command. `timeline_receipt.json` binds its output and read specification to the
existing history. It is not a new semantic transition or protocol record.

## TDD proof

Tests first: exact object membership and printed sequences, one shared clearing,
the two retained `00-01` dates, tied and unusable synthetic clocks, independence
from graph iteration order, public traces, read-only CLI and reopen parity.
A second from-empty run compares full replay with the maintained projection
after each of the 21 real admissions. This is not a second business history or
a claim that arbitrary admission permutations are valid.

Initial RED execution: 12 errors, all `ModuleNotFoundError` for the absent
`object_timelines` reader. No existing runner was changed to manufacture RED.
The first implementation run passed 11 cases and exposed a mistaken test count
of 18 objects. The retained identifier columns enumerate 17; the test now names
that entire independent set. A subsequent test-only receipt lookup was
corrected to the existing `ledger_sha256` key. Neither correction changes
population or accepted state.

The source accounting and expected object paths are authored in tests, not read
by the producer or the new reader. Synthetic controls do not enter the trusted
source history. Exact results are recorded in `VALIDATION.md` after execution.

## Relation to the chapter

[Fahland 2022](https://link.springer.com/chapter/10.1007/978-3-031-08848-3_9),
sections 2.2, 2.3 and 3, motivates separate per-object views and shared events.
This slice reproduces that distinction through Malleus reads. It does not yet
reproduce the chapter's complete directly-follows graph, process discovery,
warehouse analysis or performance measurements. Next, expand the retained
chapter data, then compare matching questions and supported results. Keep the
source results distinct from Malleus's tested admission, correction and replay
guarantees; no comparative superiority is established here.
