# Storage constructions for the worked flows

24 September 2026. Theoretical mapping and next witness specification. No backend
has been implemented, installed or selected. Read GEDANKENEXPERIMENTS-01.md first.

## What "would work in theory" means here

For a finite specimen, name every relevant object and relation, give a concrete
place to store it, describe how each required query reaches it, and show that
decoding does not merge distinctions. That is a constructive representation
argument. It is not a formal proof of arbitrary histories, crash consistency,
correct admission, performance or scientific truth.

Compare a logical representation separately from a storage implementation:

| Logical representation | Plausible physical realizations | Main unresolved obligation |
|---|---|---|
| Identified qualified assertions and relations | Existing in-memory graph; relational node/edge tables; RDF statements | Shared Core temporal selection, typed qualifiers and check scope |
| Versioned properties and edges with exact handles | Temporal graph layer over relational tables; specialized temporal engine | Full qualification/identity mapping, explicit unknowns and contexts |
| Named assertion/model subgraphs | RDF dataset or graph-ID membership tables | Explicit scope semantics; no accidental union of models or assumptions |

These can be combined in one logical graph. They are not three authoritative
histories. Formula scope is a real need even if scalar assertions are ordinary
records. The authority remains the Malleus ledger; every derived store is rebuilt
from it and has no separate accepted-state write path.

## Construction A: ordinary graph records

Stable subjects link to exact assertions. Assertions link to source evidence,
application/interpretation records and coherent qualification objects where
needed. Context bindings name selected assertions. Executions name actual inputs
and an exact model; results name the execution. Temporal applications/changes
carry their relation to accepted ledger positions.

For GE-04, store B1 (report 750), H1 (assumption 800) and B2 (corrected report
800) as separate exact assertions. Contexts O, H and C select them respectively.
Execution X1 uses B1; XH uses H1; XC exists only after execution using B2.
No entity or edge is identified merely by the number 800.

Required traversals are explicit:

- Explain old result: result -> execution X1 -> actual input B1 -> source.
- Inspect correction: B2 -> correction relation -> B1.
- Ask corrected context before XC: C -> B2 and M1, but no matching admitted
  execution/result; answer not computed.
- Inspect all price assertions: subject -> B1/H1/B2, retaining their bases and
  scope. This traversal does not itself choose an applicable physical price.

For GE-01, E1 stays distinct from I1/I2 and A1. For GE-03, D1 and D2 have separate
premise sets. For GE-05, M1/M2 select exact model statement sets. This construction
therefore provides places for the needed distinctions without requiring a node
per scalar. It still needs an executable temporal selector and rule scopes.

## Construction B: a relational projection of the same graph

The following are schematic table roles, not proposed public schemas:

| Table role | Key and information retained |
|---|---|
| Records | Exact record ID; type; typed payload; defining contract identity |
| Relations | Exact relation ID; type; exact endpoint IDs; typed qualifiers |
| Graph membership | Exact model/assertion-graph ID and member record ID |
| Acceptance bindings | Exact accepted change/record and ledger position |
| Temporal effects | Exact operation, target assertion/account, applicability kind/value, declared correction/transition relation |
| Evidence links | Exact assertion/field, source identity and locator |
| Selection/execution bindings | Exact context, premise version, model, knowledge position and actual execution/result references |

An implementation can consolidate some tables. This table list is not a mandate
for eight independent authorities or copies of payloads. Composite primary keys
and foreign keys can preserve membership and exact references. SQLite documents
these mechanisms, but their presence does not implement temporal semantics;
foreign-key enforcement must be explicitly enabled and checked per connection.
[SQLite keys](https://sqlite.org/withoutrowid.html),
[SQLite foreign keys](https://sqlite.org/foreignkeys.html).

**Decode:** records become graph records, relations become typed edges and
membership reconstructs the exact scoped model/claim graph. Preserve literal
type, identifier scope and ordering wherever meaningful. Never silently turn
numeric strings into numbers or confuse an open period with unstated time.

**Query:** the GE-04 paths become joins on exact IDs. A compound key including
assertion identity preserves B2 and H1 even though their values are equal. A
key based only on subject/property/value/times would collapse them and fails.

**Temporal projection:** GE-06 can be represented by the four logical cells in
NEXT-STAGE.md or by the three accepted operations from which those cells derive.
The latter avoids making the producer maintain derived ends. Materialized cells
are caches bound to a projector/profile and selected history. Historical metadata
must reconstruct the selected prefix, not expose later closing positions.

**Theory boundary:** this construction identifies a finite lossless mapping and
the joins needed by the specimens. We have not executed its schema, proved every
temporal operator or measured a workload. A future witness must compare decoded
meaning and query answers, not physical database bytes or only row counts.

## Construction C: native temporal property/version interface

Use the same logical identities. A native engine may store each exact assertion
as a document or expose its property version through a stable handle. Keep a
separate logical account/selection key rather than overwriting assertion identity
when the preferred version changes.

For GE-06, a dated account has versions selected by knowledge and valid time.
For GE-09, separate accounts can coexist at those same times. GE-04's assumption
must not be another update to the reported account. Source/evidence bindings and
model membership still need representable relations, not only hidden timestamps.

Important adapter conditions before claiming it works:

1. Map native transaction positions to exact Malleus accepted checkpoints. A
   database commit timestamp is not automatically the Malleus knowledge axis.
2. Preserve NONE_STATED, uncertainty, source/event clocks and known-open periods
   distinctly. A database's default valid time must not invent domain time.
3. Provide exact version references that remain valid after another correction.
   A handle based on a later-modified end timestamp needs special scrutiny.
4. Make account precedence explicit. Database overwrite order is not scientific
   authority or permission to promote an assumption.
5. Expose both full history and selected views, including evidence and model
   scope. Do not treat the native database as an independent admission authority.
6. Rebuild the native store from the Malleus ledger and recover the same logical
   answers. Native physical identity may differ; logical identity must not.

Rost et al. show temporal property/query semantics over relational storage;
XTDB documents temporal resolution from retained updates. They establish useful
mechanisms, not that these six Malleus conditions have been met by an adapter.
See the inspected sources in REPRESENTATION-OPTIONS-01.md.

## Construction D: named subgraphs, where grouping matters

For a conditional scientific claim or formula, identify a graph and its exact
members. The context/acceptance record states whether it is reported, hypothetical,
selected or actually used. Time and evidence qualify that application.

This directly addresses the observed M1/M2 model-scope problem: shared terms
are allowed; membership in one model does not imply membership in another.
It also groups the conditions in the saturation claim. A named graph alone
provides neither their scientific meaning nor a bitemporal selector. RDF's
dataset semantics do not silently confer those meanings on graph names.
[RDF dataset concepts](https://www.w3.org/TR/rdf11-concepts/#section-dataset).

This is a grouping option across A/B/C, not a demand for a fourth backend.

## What must be compared empirically

Keep one independently authored meaning/answer fixture, then encode it through
two deliberately different storage constructions. Do not let either encoder
generate the expected answers. Compare these observations:

| Witness | Required equality or refusal |
|---|---|
| Full graph round trip | Exact assertion, relation and scoped-model identities; typed values and qualifiers preserved |
| Historical read | GE-06 old value and metadata, including no future closure leakage |
| Same value, different meaning | GE-04/09 report and assumption remain distinct |
| Unknown applicability | Account inspectable, dated use unresolved; date-free quote calculation still possible |
| Exact old use | Prior calculation reaches its actual old premise and model |
| Coherent conditions | No cross-context mixing of value/unit/datum or conditional scientific inputs |
| Alternate justification | Removing one supporting route does not erase the other |
| Replay/rebuild | Fresh projection has the same independently expected meaning and reads |
| Missing closure | Missing evidence/model/contract or unsupported semantics refuses explicitly |
| Failed write | No partial accepted mutation; a storage transaction is not by itself proof of Core admission atomicity |

Only after correctness, compare storage volume, number of copied payloads, read
work, rebuild work and relevant latency on declared workloads. No performance
advantage is established by this memo. No cloud service or native engine needs
to be installed merely to make the first comparison.

## Decision status

All four constructions have a plausible representational route for the named
finite specimens. That is not a PASS for their runtime semantics. C has explicit
adapter questions; A/B need a shared temporal selector; D needs scope semantics.
No inspected source settles every required distinction automatically.

The earlier A-first recommendation is held, not rejected or accepted. Complete
the G1/G2 witnesses before asking Luis to select representation and initial
storage. The decision should name demonstrated losses, failures and integration
costs, not infer a universal winner from a favourable price example.
