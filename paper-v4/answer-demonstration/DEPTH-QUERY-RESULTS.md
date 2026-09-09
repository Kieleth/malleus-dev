# Typed depth selection recovers the qualified observation

E-0277/E-0278. The query-only TDD correction is complete. It retrieves the
existing qualified RC2 observation and excludes a count and a temperature.
No knowledge was added or changed, and no new semantic grade is assigned.

## What changed

Only earthquake_depth changes in the active answer program. It recognises
microseismicity and requires an explicit quantity_kind_class of Length plus
a numeric value_lower or value_upper. Zero and one-sided bounds remain valid
candidates. Missing dimension is not inferred from units, names or identifiers;
missing bounds are not extracted from prose. No unit conversion is performed.
The other question programs, shared matching and projections are unchanged.

The source of the earlier miss is concrete: the qualified record uses
microseismicity, which the old whole-word seismicity match did not recognise.
The earlier numeric filter also admitted count and temperature fields when
their descriptive text mentioned earthquake depth. Both classes have synthetic
regression tests, not document-specific answer values in the implementation.

| CQ-T3-01 change | Exact record |
| --- | --- |
| Added to the answer | qualification:evidence:observation:rc2-deep-depth:v1 |
| Excluded from this answer | count:forced-depth-subset |
| Excluded from this answer | observation:bdb-temperature |
| Preserved | All seven other depth rows, with identical fields and subjects |

The answer now includes the existing approximate 10 to 20 km RC2 range, its
MEASURED observational status, axial description and short-window qualification.
The observation's properties and subject match the graph exactly. Its source
faithfulness was assessed in the preceding qualification review; this retrieval
correction does not create a new source-truth judgment.

## Verification

The existing comparison executor first reproduces all thirty historical query
objects from their frozen code. It then executes the new frozen method on the
same replayed history. A guard permits only depth selection changes, forbids
changes to shared rows or paths and checks typed candidates and witness closure.

- Only CQ-T3-01 changes: nine candidate rows become eight, one gained and two excluded.
- All 29 other query objects, including the completed composition answer, are identical.
- The full suite returns 60 row occurrences, six paths and 55 distinct traced records.
- All traces resolve through the five retained capture artifacts, with exact source locators.
- All four output files reproduce byte for byte on the repeated read.
- The 164-record graph, 166-version record history, 39-event ledger and replay receipt stay unchanged.
- Queries make zero source-file, network or embedding accesses.

Historical text-binding and projection tests now bind their historical program
bytes explicitly. They no longer inherit the live selector while claiming to
measure a previous intervention. An AST guard verifies the old projection-only
change and permits only earthquake_depth to differ in the current program.

Final focused paper gate: 413 passed, two subtests, including 19 depth-query
tests. Changed Python Ruff and formatting checks and the scoped tracked diff
check pass. This does not claim a Core full-suite run.

## Remaining limits

These are typed candidates, not a general semantic query planner or a new
coverage score. Other sites and expected-depth values remain visible rather
than being silently assigned to RC2. The recovered observation still has no
explicit below-seafloor reference field or full location-method/uncertainty
representation. The query does not invent these from the source or from the
question's wording. Historical grades and the model-assisted qualification
review remain unchanged; human ratification remains pending.

## Coordinates

Private base: private/paper-v4-answer-demonstration/sol-qualification-01.
New method: depth-method-01. Outputs: depth-query-01 and depth-query-reproduction-01.
Core remains 160878cf14c0d27b11a440e26688708e9b7a7e2b.

- Method: sha256:2b3e52b4952b394a10813a426e27efa56ea7891811a0350efcc71e62cc6379a7.
- Query: sha256:af325d88662ec2aee0fd29fb2cfcd37c5f9bd47e65375a9498fb9c1522e930aa.
- Trace: sha256:2d585000bde92590a3388d8db2a97467afaedbb1dff3b9a2195916c283cdc3b7.
- Unchanged ledger head: sha256:f33fd9a6410c1085b6384ee446224e244b15ff81321f1c3a7ccefd76f4d041fc.
- Unchanged replay receipt: sha256:eb9bcac22da1c1a61912f8b08e2201975d93216c935734b77c110fbbc9f40167.

No producer, new capture, review dispatch, Core, manuscript, dependency or Git
mutation was performed. This is not a Core full-suite run or a paper release.
