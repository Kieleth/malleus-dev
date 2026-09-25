# Retain versions, select their use

2026-09-24. Research and proposed design, not implemented temporal semantics.
This note supersedes the recommendation in CHECK-SCOPE-02.md. Implementation is
paused at the author's request. No new backend, policy or grammar is selected.

## Correction to our reasoning

Keeping earlier and corrected values in the same KG is not a semantic error.
Using them as interchangeable, simultaneously applicable values is the error.
A graph holding all versions and a graph view selecting applicable versions
serve different purposes. Neither can substitute for the other.

The existing project vision already states this distinction. In
`docs/PRINCIPLES.md:280-301`, accepted history is reconstructed from a verified
ledger prefix; a further resolution uses an interpretation profile and valid
time. It explicitly names one replay-derived accepted temporal graph. Our T3
discussion narrowed that target to the existing current-record projection and
treated historical values mainly as check inputs. That was premature.

Reread the complete malleus-dev, malleus-acolyte and malleus-recon skills, plus
the Unix doctrine. They support one accepted write authority, explicit projection
inputs, and separation of additional detail, corrected interpretation and change
in the world. None licenses treating arrival order as domain time. Skill bytes
match those in the main checkout at this reading. No skill edit is made here.

## What the inspected literature establishes

These are bounded source findings, not claims of a complete survey.

1. **Rost et al., Bitemporal Property Graphs to Organize Evolving Systems.**
   Sections 3 and 4.2 attach valid and transaction periods to vertices, edges and
   property values. Their queries can retrieve complete histories or select
   particular times. Section 4.2 explicitly returns multiple values of one
   university property, then selects by applicability. Section 6 describes a
   graph implementation over relational storage. Thus this logical model does
   not itself mandate a particular physical graph backend.
   [Author manuscript](https://dbs.uni-leipzig.de/files/research/publications/2021-11/pdf/Rost_2021_Bitemporal%20Property%20Graphs%20to%20Organize.pdf).

2. **Anselma et al., Bitemporal Property Graphs: Dealing with Both Valid and
   Transaction Time.** Sections 2 and 3 retain earlier accounts and distinguish
   their database lifetime from domain applicability. Section 2.1 deliberately
   permits relationships between entities with different valid-time periods,
   illustrating ancestry and causation. This differs from the endpoint-period
   containment imposed by Rost's model. Edge-time integrity is therefore a
   modelling decision, not a universal overlap test.
   [Inspected author manuscript](https://iris.unito.it/retrieve/f899a7bb-e315-4e57-84f1-9908713d1192/BiTemporalGraphDB_final.pdf).
   A [publisher correction notice](https://link.springer.com/chapter/10.1007/978-3-032-05281-0_21)
   exists, but its full text was not accessible. We do not assert that this
   manuscript equals the corrected publisher version or what the correction
   changes. Resolve that before copying its precise formal constraints.

3. **W3C, Defining N-ary Relations on the Semantic Web, Working Group Note.**
   Pattern 1 represents a relation instance as an identifiable object with
   links to its participants and qualifiers. This offers a representation
   technique for an assertion carrying value, subject, time and provenance.
   It does not supply bitemporal query or admission semantics.
   [Note, pattern 1](https://www.w3.org/TR/swbp-n-aryRelations/#pattern1).

4. **XTDB time documentation.** Valid time and system time support effective
   periods and the evolution of the database's account. Its documented queries
   distinguish the present account of a past period from an account held then.
   This is an operational comparison, not a recommendation to replace Malleus
   storage. Database timestamp defaults must not fill missing scientific dates.
   [Official documentation](https://docs.xtdb.com/about/time-in-xtdb.html).

The two coded graph works overlap both selected requirements: queryable versions
and independent time selection. This establishes relevant prior art, not Malleus
conformance or system equivalence. Ontology changes, unknown temporal precision,
epistemic status and Malleus admission guarantees were not covered by this small
comparison.

## Two axes, and what neither axis means

**Valid time:** when an account says a proposition applies in the domain. It is
not a certificate that the proposition is true.

**Knowledge position, corresponding to transaction/system time:** when that
account became accepted and when another account replaced it. For Malleus, use
the exact accepted ledger position as the authoritative ordering coordinate.
Two wall-clock timestamps can coincide. Retaining a source or proposal is not
the same as accepting its assertions.

Closing an account's selected lifetime must not delete its audit identity or
evidence links. A full-history query still reaches it. A selected-state query
may exclude it from the facts currently applicable to the requested context.

A hypothesis versus a report, different source accounts, an assumption scenario,
measurement procedure and calculation version are separate context. Bitemporal
selection cannot choose between these by itself. Likewise observation time,
publication time and import time are not interchangeable with valid time.

## Controlled price example: expected meaning, not an executed result

Assume one product and one explicitly selected reported-price account. Dates
below are synthetic and exact within this control. On 2 May, accept a report
that price is 750 cents from 1 May, with no end yet known. On 12 May, accept an
actual transition to 800 cents from 12 May. On 20 May, accept a correction: the
earlier period was 775 cents, not 750. Nothing says the price changed on 20 May.

One possible logical history representation is:

| Account version | Value | Domain applicability | Selected at knowledge positions |
|---|---|---|---|
| A1 | 750 cents | [1 May, open) | [2 May, 12 May) |
| A2 | 750 cents | [1 May, 12 May) | [12 May, 20 May) |
| B | 800 cents | [12 May, open) | [12 May, open) |
| C | 775 cents | [1 May, 12 May) | [20 May, open) |

All four remain queryable from the full history. `[a,b)` includes a and excludes
b. Open means no accepted end in that account, not certainty about forever.
A1 and A2 can be two versions of one assertion's applicability, not two
independent source observations. This table does not choose storage layout.

The often missed requirement is **versioning the boundary itself**. Before
12 May we did not know the earlier account ended then. Overwriting A1's end
without preserving its earlier form would leak later knowledge into an old read.
Append-only ledger events can derive these periods without rewriting old bytes.

| Question | Expected selection |
|---|---|
| Price for 5 May, using knowledge available on 10 May? | A1, 750 cents |
| Price for 5 May, using knowledge available on 15 May? | A2, 750 cents |
| Price for 5 May, using knowledge available on 21 May? | C, 775 cents |
| Price for 15 May, using knowledge available on 21 May? | B, 800 cents |
| What versions and corrections have ever been accepted? | A1, A2, B, C, qualified |

Retrieving the history is not claiming all four prices apply on 5 May.
Selecting C does not erase A1 or change the inputs of an earlier execution.

## What the KG must let consumers distinguish

**Stable subject reference:** a query about the product resolves its price under
the selected times and context.

**Exact version reference:** an execution that used A1 continues to point to A1.
It must not silently point to C after correction. We can separately ask whether
its premises still match our corrected account of the requested period.

**Relationship time:** a price-applicability edge and a derivation edge do not
make the same temporal assertion. A derivation may connect an execution to an
earlier premise. Keeping that edge valid does not extend the premise's domain
period. Whether an edge requires overlap, succession or only audit visibility
must follow the predicate's declared meaning.

**Temporal joins:** ordinary co-temporal reasoning must use facts sharing the
requested context. For example, combining a price valid only before 12 May with
a delivery fee valid only afterward invents a state that never applied.
Historical comparisons and causal paths may intentionally cross periods, but
must say so. A single blanket graph-wide filter is insufficient.

**Unknown time:** unstated applicability must remain explicit. A point selection
cannot silently include it as timeless or discard it as false. The query needs
to distinguish selected, excluded and unresolved records without fabricating a
date. Exact return types are not designed here.

**Rules and ontology:** structural validation of versioned records differs from
a rule over a selected state and from a rule over history. "One price" must say
for which subject, property, account/context and temporal scope. Past records
also retain their governing ontology identity; testing a historical record
against today's schema is a choice, not automatic compatibility.

## Where current Core stands

Inspected isolated base `ebff70f72dc4cd67b2f910b88575e558a2824728` plus our local T2
changes, not every live Core branch:

- `KnowledgeHistoryReplay.record_history` retains accepted record operations
  and supersession information. `graph_at_change` reconstructs a graph at an
  accepted change. These are useful components, not a full temporal query model.
- `KnowledgeChangeHistory._apply_change` closes the prior interval and removes
  superseded records from its ordinary graph. It refuses already superseded
  targets and non-later instant replacements. Our same-period correction is
  outside those semantics.
- Local `replay_at` adds a verified knowledge-prefix read. It supplies the
  knowledge axis, not selection by domain time.
- The separate Assent path already contains temporal machinery. It must be
  assessed for reuse rather than claiming Malleus has no temporal code. Its
  current replacement constraints do not implement this correction control.
- The prior 32-test observation shows what current checks receive. It does not
  establish that historical versions should be excluded from the KG.

The missing design is a **version-aware graph and selection contract integrated
with accepted change history**, including what checks inspect. Adding timestamp
fields or exposing the old record dictionary alone does not establish it.

## Candidate transfer and decisions still open

Proposed disposition: **COMPOSE**, not yet adopted.

- **SOURCE_MECHANISM:** qualified versions and two-axis selection, evidenced by
  the precise model/query sections above. No external performance result is
  reproduced or claimed here.
- **ASSUMPTIONS_AND_THREAT_MODEL:** ordered known coordinates in the synthetic
  control, one selected account, stable identities. Neither source truth nor
  trustworthy external clocks follows from structural replay.
- **REUSABLE_TECHNIQUE:** reconstruct a complete version graph, then derive
  declared selected views without destroying historical references.
- **FAILURE_BASELINE_OR_ORACLE:** manually authored table above; current Core
  refuses the required same-period correction. External papers supply examples,
  not an independent Malleus test oracle.
- **TARGET_BOUNDARY:** optional compiler-enabled temporal history profile,
  its graph projection/query interface and admission check inputs. Calculations
  are consumers, not new accepted-state writers.
- **EXCLUDED_TRANSFER:** no automatic adoption of all endpoint constraints,
  database timestamp defaults, SQL backend, source truth claims or arbitrary
  historical Prolog policy. No silent change to existing history semantics.
- **SMALLEST_EMPIRICAL_TEST:** one from-empty history reproduces the five table
  answers, preserves exact execution references, and refuses an unqualified
  mixed-period calculation. This test has not run.

Two representation options deserve a concrete comparison before implementation:

| Option | Advantage | Cost to establish |
|---|---|---|
| Explicit assertion/state-version nodes and typed context links | Addressable evidence and computation premises; can use ordinary graph structure | Must define version ontology, selected views, joins and validation |
| Native versioned vertex, edge and property values | Temporal properties directly express changing values | Extends graph model and query/check APIs; premise versions still need identities |

My candidate for the first control is explicit addressable versions, because
evidence and calculations already need exact premise identities. This is a
proposal, not authorization or evidence that native versioning is unnecessary.
Either option must meet the same observable temporal contract. A new database
is not a prerequisite established by this investigation.

## Proposed next design checkpoint

Before another runtime RED, agree the full version graph and selected views for
this control. Include one stable-subject edge, one exact-premise edge, a
cross-period join refusal, an unknown-time scientific assertion and a separate
what-if premise. Specify which graph/view each rule consumes and what happens
when selection is ambiguous. Then choose the representation and write TDD
against those expectations. No custom-rule exclusion is assumed in advance.

Keep interval splitting, uncertain bounds, multiple authorities and temporal
ontology evolution visible as later controls. Deciding the first control is not
declaring those unsupported forever.

## Research record and limits

The ignored `private/temporal-bitemporal-recon/` holds 16 typed research records,
validated and exported through public Recon APIs. Its two-axis comparisons are
reviewer coding of requirements and source definitions, not runtime validation.
Input is `private/temporal-bitemporal-recon-input.json`. Primary PDFs were read
through the web tool; local archived PDF bytes and authenticated digests were
not retained or claimed. The repository memo carries the usable conclusions;
private working notes are not staged or promoted into accepted Core knowledge.

No runtime, API, tests, checks, skills, package, Core governance or shared tree
changed during this research pause. Earlier local T2 work remains unintegrated.
