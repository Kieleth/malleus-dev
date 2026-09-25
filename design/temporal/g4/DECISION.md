# G4 decision memo: representation and the first Core cut

24 September 2026. For Luis. You decide; this memo recommends. It stands alone.
The full tables are in [COMPARISON.md](COMPARISON.md).

Evidence tags on every claim: INSPECTED (read in a file or in code at tip
903a1a1c), TRACE (worked on paper, no code ran), STORAGE (a storage witness ran it:
G2a graph records or G2b SQLite), CORE (G3 ran it through Core's public admission
path). I re-ran all four suites per directory at 903a1a1c: g1 9, g2a 38, g2b 40,
g3 213 passed.

## What the gates found, in five lines

1. Two independent encoders of the eight specimens agree with each other and with
   the specimen on every determinate answer. They split only on CA08 branch 2, AJ06
   and RF-OVERLAP, and each split is a hole in the specimen. [STORAGE]
2. Core as shipped: 45 of 100 answers right, 2 wrong, 53 not expressible; 10 of 12
   refusals observed. Both wrong answers are one fault: Core has one supersession
   for both a correction and a transition. [CORE]
3. That fault has a precise shape in code. On supersession Core sets the old
   record's `valid_to` to the successor's start, sets `superseded_by`, and drops it
   from the current graph (`knowledge.py`, `_apply_change`). For a transition the
   valid-time half is already right. What is missing is any record that the old
   version is still believed, and any way to correct a record a transition already
   closed: that attempt refuses "record supersession forks prior record". [INSPECTED, CORE]
4. 37 of Core's 55 misses need one read Core does not have: select by domain time,
   account, named use or persistence rule. That is T4, not T3. [CORE]
5. Several of Core's right answers rely on references kept as string slots, because
   a typed relation into a record blocks that record's supersession and a relation
   cannot be a relation's endpoint. G3 did not list this as a request. [INSPECTED, CORE]

## (a) The representation question

| Option | What a witness proved | What it lost or could not do | Cost to change Core |
|---|---|---|---|
| **A. Identified assertion records** in one ledger-derived graph, versions derived by replay | G2a: 99 of 100 answers, 0 fail, round trip and rebuild byte-identical, every prefix read equal to a fresh build to that prefix. [STORAGE] G3: Core already stores records by identity with their full history; 45 answers right. [CORE] | G2a could not use Malleus's `KnowledgeGraph`: it refuses a relation whose endpoint is a relation (g1-06 assesses A1). [INSPECTED] Versions exist only when read. Core: the correction/transition fault, no domain-time read, no version listing. [CORE] | The G3 request list, R1 to R8. The first cut needs R1 only (section b). |
| **B. Relational tables** holding the same ids | G2b: every authored answer passed, 12 of 12 refusals, round trip and rebuild equal, a key on (subject, property, value, time) shown to merge distinct premises. [STORAGE] | Nothing inside accepted objects of these eight specimens. 27 tables. It is a physical form of A, not a different meaning. [STORAGE] | A second store and a projection qualification under the skill's "Qualify a projection". It fixes none of Core's gaps. |
| **C. Native temporal store** keyed by (subject, property, valid time, transaction time) | No witness. Paper only. [TRACE] | Gets g1-01's selection and knowledge periods right by construction. Every specimen also has a query needing identity the four coordinates lack: account (CA01, OQ10), basis (CA04), the report as stated (PX-r1-K3, C01), unstated time (S02), membership (CC05), an assessed relation (AJ02), the declared change kind (RF-OVERLAP). [TRACE] | An install, six adapter conditions, and A's identities carried in its documents anyway. |
| **D. Named subgraphs** for groups and models | Used inside both witnesses (subgraphs in G2a, a membership table in G2b); CC01, CC02, CC05, ST05, ST06 pass. [STORAGE] G3 kept groups as a string list and got CC01, CC02, ST05, ST06 right. [CORE] | A grouping convention, not a temporal model. | None for the first cut. |

**Recommendation.** Keep A as the logical representation: identified assertion
records in the one ledger-derived graph, with Core owning what a declared correction
or transition does to them, and D's membership records only where a specimen groups
records. Add no relational or native temporal store now. The reason: two
independently written encoders of identified records reproduced every determinate
answer, and Core's failures come from how one supersession interprets two change
kinds and from missing reads, not from the record shape. A native temporal store
would answer the price history by construction, but on paper every specimen needs
identity it does not key on, so it would sit under A as an index, not replace it.
Relational storage (B) is a proven lossless form of A for these cases and stays a
later option for workload reasons, which nobody has measured.

Evidence limit: eight small synthetic specimens. Agreement proves the answers are
determinate under them, not that they are right, and nothing here measures size or
speed.

## (b) The first Core cut (T3)

**Claim.** A same-period correction and an actual transition leave different
histories. After a transition the old version is still believed for its closed
period. A correction may target a record a transition already closed, and it
replaces that record's account without touching the successor.

**Role.** `OPTIONAL_PROFILE` over compiler-enabled semantic history, as the
workstream README states; histories that do not use it keep today's meaning. G3
labelled the meaning of the knowledge-period end a `PROTOCOL_INVARIANT`. That
conflicts with the README's "no additional mandatory base-protocol rule". I
recommend the optional profile.

**Contents.** G3 request R1 only, in this form:

1. A transition names its target (it already does). It closes the target's valid
   period at its own start, as today, and records that it closed it by transition.
   The target's knowledge period stays open. [TRACE over INSPECTED code]
2. A correction names its target, which may already be closed by a transition. It
   covers exactly the target's current period, inherits the target's successor link,
   and closes the target's knowledge period at its own position. At K3 that makes r3
   cover 1 May to 12 May with successor r2, so r2 stays the only current price, with
   no interval grammar. Any other period refuses as unsupported. [TRACE]
3. A target already corrected or revised at the head is stale and refuses at CHECK.
   A target closed by a transition is not stale. [TRACE, STORAGE for the definition]
4. `record_history` exposes the closing kind and position, so the two histories
   can be told apart through the reads Core has today (`replay_at`, `record_history`).

**Route.** The two history changes need a declared correction field on the
operation. G3 measured three routes. Route A, an optional field: no identity moves;
a Core without the field refuses "operation fields are not closed" (`knowledge.py`
line 412). Route C, structural builtin version 2: moves the check contract, the
structural policy, the normative profile, the history bundle, every partial
effective contract and every structural ledger head; files naming them 0 to 2 by
full digest and 4 to 6 by prefix, real cost larger and not measured (the OVR-000466 precedent). Route
D, the state-version profile: it maps both correction and transition to
`SUPERSEDE_STATE_VERSION`; changing it moves an identity named in 29 files by full
digest and 31 by prefix; nothing executes it today.
[CORE, INSPECTED]

Recommendation: build RED and GREEN on the branch under route A. Before any
integration, move to route C, and take D in the same step, because under A two
Cores with the same builtin identity would admit and refuse the same bytes
differently, and leaving D alone would ship a profile that says correction equals
transition while Core no longer does.

**Explicit exclusions.** Domain-time selection and every account, named-use or
persistence-rule read (R3). Interval ends, valid time per record and untimed
records inheriting a date (R2). Overlapping corrections and interval splitting.
Version listing (R4), unless you want PH-K3 in one call; it moves no identity. A
replay that names a missing artifact (R5). Premise compatibility (R8). The empty
list and `decimal` defects (R6, R7), which are real but not temporal. Typed
relations into retired records: premise links stay slots, as in G3.

**Smallest failing test that starts it.** On the g1-01 history built as G3 builds
it, with K2 declared a transition of r1: compose K3 as a correction of r1 at head K2
and pass it to `check_and_admit_change_set`. Expect it admitted, `replay_at(K3)`'s
current graph to hold r2 and not r1 or r3 for `unit_price`, r3 to cover 1 May to
12 May, and `replay_at(K2)` to read exactly as before. Today it refuses at CHECK:
"record supersession forks prior record: r1". [CORE, observed in G3's K3 row]
Paired with it, a second correction of r1 composed fresh at K3 must refuse as a
stale target. That is RF-STALE-REVIEW's shape, and today Core refuses it with the
same fork message it gives the valid K3, which is why the two tests belong together.

**Promotion residual.** The specimens are fixtures, not consumers. The cut is
checked on two differently shaped fixtures (g1-01 timed, g1-04 and g1-02 with no
stated time), which is not the skill's second independent consumer. Generic
promotion waits for one.

## (c) What stays later

- T4: domain-time selection at a knowledge position (R3), account precedence, named
  use, persistence rules, interval ends (R2), overlap and splitting.
- T5: the consumer contract, premise compatibility (R8), exact old use with typed
  relations that survive retirement.
- Separately filed Core defects: required multivalued slot accepts `[]` in
  `ContractView.validate_instance` but not in `OntologyRegistry` (R6); `decimal`
  does not compile (R7); a replay naming the missing artifact (R5).
- Specimen fixes D1 to D18 in COMPARISON.md section 3, before G5 reuses the
  specimens as a conformance suite.
- Adopter policy Core never decides: reconsideration flags and their review unit,
  argument sufficiency, completeness authority, initial state, withheld-read scope,
  which account is authoritative.

## Your decisions, one at a time, in dependency order

1. Representation: A, with D only for grouping, and no second store now. Yes or no.
2. Target naming (G1 OC-01): a transition and a correction name their target;
   nothing is inferred. Recommended.
3. Transition: closes valid time as today, records its kind, leaves the old version
   believed. Recommended over also keeping the old record in the current graph,
   which contradicts the shipped profile's `CURRENT_NON_SUPERSEDED_RECORDS` rule.
4. Correction: may target a record a transition closed, covers exactly its current
   period, inherits its successor, closes its knowledge period; anything else
   refuses. Recommended over interval-bearing corrections, which need R2.
5. Stale target: already corrected or revised at the head, refused at CHECK.
   Recommended over "no open version at the head".
6. Route: A on the branch, then C with D before integration. The costly one. It
   waits for 3 to 5 because they fix which field is added.
