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

## TDD proof

Tests first: exact object membership and printed sequences, one shared clearing,
the two retained `00-01` dates, tied and unusable synthetic clocks, independence
from graph iteration order, public traces, read-only CLI and reopen parity.
A second from-empty run compares full replay with the maintained projection
after each of the 21 real admissions. This is not a second business history or
a claim that arbitrary admission permutations are valid.

Initial RED execution: 12 errors, all `ModuleNotFoundError` for the absent
`object_timelines` reader. No existing runner was changed to manufacture RED.

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
