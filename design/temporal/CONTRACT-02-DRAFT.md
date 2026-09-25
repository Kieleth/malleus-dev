# T3 design draft: correction is not transition

Research hold, 2026-09-24: the observations below remain useful, but this draft
does not yet specify the required all-versions KG, temporal selection or check
scope. Do not implement it before resolving
[BITEMPORAL-RESEARCH-01.md](BITEMPORAL-RESEARCH-01.md).

Status: proposed detailed contract. Scope was authorized; persisted grammar and
projection design are not frozen yet. No runtime correction behavior is changed.

## Required observations

The first two situations in `situations.json` are the minimum positive pair:
same inputs and values, different declared change meaning, different answers for
5 May. The historical position from before either second acceptance must remain
reconstructible through T2.

An additional boundary prevents a misleading implementation:

1. Accept 750 cents from 1 May.
2. Accept a transition to 800 cents from 12 May.
3. Accept a correction: the earlier period was 775 cents.

After step 3, a latest-knowledge query for 5 May gives 775; a query for 20 May
still gives 800. A query at the knowledge position before step 3 for 5 May
still gives 750. The correction cannot make the old period current again.

The same mechanics must work with a non-price, differently shaped fixture,
such as a corrected measurement interpretation with explicitly unstated domain
time. Unknown temporal applicability remains unknown after a value correction.

## Smallest intended semantics

- A transition declares a domain boundary and a successor state.
- A correction targets an exact accepted version and replaces our account of
  that version's whole period. It creates no new domain transition.
- In this first cut, correcting the period's bounds, splitting an interval,
  merging intervals and retracting a period are excluded.
- Evidence arrival does not itself select either operation or accept it.
- A second competing correction is not silently selected by arrival order.
- Record payloads, sources and previously returned historical views remain
  immutable and explainable.
- The query must identify both the knowledge position and domain-time selection.
  Unknown applicability cannot be interpreted as absence, truth or timelessness.

## Design work before RED

Separate three identities: the domain subject, one domain-state period, and one
accepted account of that period. Determine which belong to the optional
temporal profile and which remain adopter identifiers. The current record-ID
supersession chain mixes the latter two roles for temporal queries.

Resolve how the exact change artifact declares correction versus transition,
how the replay fold derives period endpoints and correction lineage, and how
relations remain valid when a historical view selects older record versions.
Do not repurpose `supersedes` without a versioned semantic boundary. Do not
change the meaning of existing private-v0 histories to make a new test pass.

Prefer reuse of existing temporal value parsing and relation validation. A
new profile should not turn imported assertion order into state-transition time.
The source-assertion and state-version profiles make different commitments.

## Computation integration requirement

A calculation binds its model identity, selected premise identities and query
coordinates. A correction can change the selected premise without changing the
question's domain date. The old execution remains valid evidence of what ran
under its old premises. Comparing against the newly selected premises reports
change, not a newly computed result. Assumption/report distinctions are not
temporal axes and are not inferred by this profile.
