# Core: population v2. Neutral plan, governed integration, facade, document adapter.

From the overseer session. Decided by Luis in chat on 2026-09-03 (late). Executor: Core. This document supersedes `handover/2026-09-03-core-population-adapter-tdd.md` in full and replaces R1 of `handover/2026-09-03-core-requirements.md`; R2 to R6 are reordered at the end. Core's evaluation of the previous handover (at commit 3b35476) is accepted in full, the split included. The corrections it asked for are listed in the last section so nothing is silently absorbed. This version also went through one cold adversarial read before dispatch; its seventeen findings are folded in.

Standing order unchanged: Core touches Core; receives requirements with reproducers from the overseer; reads no paper file, question, schema or evaluation; reports commit, tree, symbols, tests and a non-claims paragraph per piece; the overseer verifies each piece on disk before the next starts.

## Rulings

1. Split accepted. Core owns a neutral population plan and everything below it. A document-assertion adapter ships with Core as an optional layer under the `source-assertion` profile. It does not define population. This is `docs/PRINCIPLES.md`, protocol boundary taxonomy: an optional profile or a fixture never defines the base protocol.
2. Assertions are capture evidence. They are retained in the ledger and named in the change set's evidence closure through the plan's `evidence` field. They are not graph records. Field-level derivations link every property and every relation endpoint of a record to the assertion (or row, or path) it came from. Claim entities in the graph are a later, pack-level choice, not this work.
3. Packs (old R3) are an offered layer and are not on the population path or on the paper rerun's critical path.
4. `source-assertion` and `state-version` ship now as minimal profile artifacts (`grammar`, `profile_id`, `semantic_unit`, `origin`, `grounding`), retained as evidence and named by the plan and the change set. The full profile contract (old R2) follows.

Carried over unchanged: competency questions never enter ontology construction or population; no brief; no fallback population; capture covers the whole source; gaps are typed and visible; strict validation with no guessed defaults; deterministic lowering; RED then GREEN; neutral fixtures only; the paper's frozen runs are the overseer's downstream check, never Core's fixture.

## The chain

```text
source bytes  →  adapter (source-specific)  →  population plan (neutral, Core)
              →  KnowledgeChangeSet (existing grammar)  →  ledger  →  replayed graph
```

Two consumers with different shapes were first executed at HEAD a7ccf3b
(section "Evidence"): Small Shop rows through a row mapping, and a three-block
inspection note through the document adapter. P6 later refreshed the runnable
examples to the full shipped profiles and public compiler facade. The exact
example bytes are now exercised without test-time rewriting. Both consumers
still use the same plan grammar, lowering, admission, and replay. Small Shop
has no prose and no verbatim clause; the plan does not ask for one.

## The population plan

One plan is one change set. The adapter decides plan boundaries by the profile's semantic unit (one state version, one set of assertions, one occurrence). Core does not.

Fields, closed, twelve:

| Field | Value | Where the constraint already lives |
| --- | --- | --- |
| `grammar` | `malleus.population-plan/private-v0` (Core names the final) | |
| `plan_id` | text; also the retained evidence record id of the plan bytes | a plan id already retained refuses `DUPLICATE_PLAN_ID`; independently, the governed path refuses re-creating an existing record id (`STRUCTURAL_REFUSAL: record ID already exists in history`, executed below) |
| `contract_identity` | the `PartialEffectiveContract` digest | the change set binds the same digest as `contract_identity` with `contract_kind` `PRIVATE_PARTIAL_EFFECTIVE_CONTRACT_V0` (`knowledge.py:31,54-71`); composed by `compose_partial_effective_contract` (`machine.py:784-810`). Never a raw ontology digest. |
| `history_profile` | `{profile_id, sha256}` of a retained profile artifact | retained with role `RETAINED_EVIDENCE`, named in the evidence closure; no grammar change (`_EVIDENCE_ROLES`, `knowledge.py:50`) |
| `adapter` | `{adapter_id, version}` | |
| `sources` | `[{source_id, sha256}]`, nonempty | must be retained before composition (`UNRETAINED_INPUT`, `knowledge.py:1118`) |
| `evidence` | `[{evidence_id, sha256}]`, adapter-declared retained artifacts (the capture document, for the document adapter); may be empty | each must already be retained, else `UNRETAINED_EVIDENCE` at compile |
| `records` | `{entities, relations}` in the public record shape exactly: `type`, `id`, `properties`, and `source_id`, `target_id` for relations; no other key. The keys `signals` and `events` are accepted as names (they are public families, `kg.py:30`) and refuse when nonempty | `KnowledgeGraph.from_records` refuses unexpected keys (`kg.py:183-230`); `plan.records` is a valid `from_records` input unchanged, which is what makes the agreement property cheap |
| `supersessions` | `[{record_id, supersedes_record_id}]` | lowers to the per-operation `supersedes_record_id`; omitted when absent, never null (`knowledge.py:340-344`, "superseded record ID is required") |
| `derivations` | `[{record_id, path, source_id, locator}]` | `path` is a key path into the record (`["properties","name"]`, `["source_id"]`); `locator` is opaque text to Core |
| `gaps` | `[{kind, statement, source_id, locator}]` | kinds: INTERVAL_NOT_EXPRESSIBLE, AGGREGATE_ONLY, MODALITY_NOT_EXPRESSIBLE, REQUIRED_FIELD_ABSENT_IN_SOURCE, TYPE_ABSENT, RELATION_ABSENT (`design/KNOWLEDGE_PACKS.md`, typed gaps). Gap kinds name what the contract cannot express, not the shape of the source; a structured source with a status column hedges too, so MODALITY_NOT_EXPRESSIBLE stays generic |
| `valid_time` | `{kind, value}` | `INSTANT` (aware) or `ORDER_ONLY` (`knowledge.py:459`) |

Rules the tests pin, each with the compiler's own typed refusal reason (the plan compiler is new code and carries its own reason enum; it wraps, and does not extend, the governed path's reasons):

| Rule | Refusal |
| --- | --- |
| fields closed; grammar known | `FIELDS_NOT_CLOSED`, `UNSUPPORTED_GRAMMAR` |
| `contract_identity`, profile, source and evidence digests are `sha256:` plus 64 hex | `MALFORMED_IDENTITY`, `MALFORMED_PROFILE_REFERENCE`, `MALFORMED_EVIDENCE_REFERENCE` |
| sources nonempty | `SOURCES_REQUIRED` |
| record family keys are a subset of the four public families; `signals` or `events` nonempty refuse | `UNKNOWN_FAMILY`, `FAMILY_NOT_ADMITTED` (the governed path admits `CREATE_ENTITY` and `CREATE_RELATION` only, `knowledge.py:309-315`, where an unknown type reads "operation type is unsupported"; this refusal is the reproducer for Event materialization, old R6) |
| record ids unique across families | `DUPLICATE_RECORD_ID` |
| every derivation names an existing record, an existing path, a listed source | `UNKNOWN_RECORD`, `ABSENT_PATH`, `UNLISTED_SOURCE` |
| every key under `properties` and both endpoints of every relation have at least one derivation; `type` and `id` are the plan's own identifiers and are not derived | `UNDERIVED_FIELD` |
| supersession names a plan record once, with a nonblank superseded id | `UNKNOWN_RECORD`, `MALFORMED_SUPERSESSION` |
| gap kind known; gap source listed | `UNKNOWN_GAP_KIND`, `UNLISTED_SOURCE` |
| valid time kind supported | `UNSUPPORTED_VALID_TIME` |
| records validate against the compiled contract view exactly as the governed path validates operations; closed world; no defaults | the contract's own refusal, surfaced unchanged (executed below on the direct path: "Unknown entity type") |
| a plan may carry gaps and zero records | result `NO_DOMAIN_CHANGE`, below |

Note the asymmetry the agreement property does not cover: `from_records` accepts `signals` and `events` (`kg.py:30-35,198-206`); the governed path does not. The plan compiler refuses them before either path sees them.

## Lowering: deterministic, adds order and identity, adds no meaning

The lowering takes the plan and a base-state view: the replay's existing record ids and, per record, the change set that created it. It reads no ledger and writes nothing.

- Entities in plan order, then relations in plan order; ordinals 0..n-1. Family order is `RECORD_FAMILIES` (`kg.py:30`).
- `operation_id` = `operation:{plan_id}:{ordinal}`.
- A relation's `depends_on` = the operations of its endpoints inside the same plan, source then target. An endpoint absent from the plan must exist in the base view, else `DANGLING_ENDPOINT` at compile.
- `supersedes_record_id` copied per record from `supersessions`; omitted otherwise. A superseded record absent from the base view refuses `UNKNOWN_SUPERSESSION` at compile; the governed path keeps its own `UNKNOWN_SUPERSESSION` at admission (`knowledge.py`, refusal reasons) as the second line.
- Change-level `supersedes` = the change set ids that created the superseded records, from the base view, in first-occurrence order, unique.
- The compiler returns: the status, the operations, the change-level supersedes, and the record ids the closures need (sources, profile, plan, `evidence`, gaps). It does not build the closures; `KnowledgeChangeHistory.compose_change_set` does, from retained anchors, and refuses anything unretained.
- Sources closure = `plan.sources`. Evidence closure = the profile artifact, the plan bytes, every `plan.evidence` member, and the gaps artifact when gaps are nonempty. Retention order: adapter evidence (the capture) before the plan; the plan and gaps before composition. `UNRETAINED_EVIDENCE` at compile catches an `evidence` member that was never retained.
- Zero records → typed result `NO_DOMAIN_CHANGE`: profile, plan, evidence and gaps are retained; no change set is composed. The grammar refuses an empty operation list (`knowledge.py:469`, "a change set must contain an operation"), so this is a result, not an error.
- `valid_time` passes through.

## The minimal profile artifact

P1 initially used a closed five-field `private-v0` bootstrap. P6 superseded it
with the full `malleus.domain-history-profile/private-v1` contract covering
genesis, time, change, ontology roles, projection, and grounding. The runnable
examples now use the full shipped profile bytes. The old grammar is refused,
not retained as a fallback.

## Pieces, in order, each RED then GREEN

Each piece: a failing test committed first, then the implementation, then a report. Small slices. The overseer verifies on disk before the next piece.

**P1. Plan grammar and compiler.** Parse and validate the plan against a compiled contract view and a base-state view; lower to `KnowledgeOperation` values, change-level supersedes and the closure record ids; `NO_DOMAIN_CHANGE` on zero records; every refusal in the two tables above, each provoked by one test. The agreement property: for a valid plan against an empty base, `KnowledgeGraph.from_records(registry, plan.records).export_records()` equals the governed replay's `export_records()` after admission. Supersession is tested on the governed side only; the direct path has no notion of it.

**P2. Governed integration.** The minimal profile artifact; retention of adapter evidence, profile, plan and gaps before composition, in that order; compose with closures through the existing composer; admit; reopen; replay; `NO_DOMAIN_CHANGE` leaves retained evidence and no change set; the two-plan supersession pair (Small Shop e4 then e7) replays to one current state and one record history; a repeated plan id refuses; a repeated record id refuses at admission.

**P3. Public facade and CLI.** The private path becomes public: compile a contract from retained sources; propose (compile receipt or typed diagnostics); populate (plan → change set, `NO_DOMAIN_CHANGE`, or typed refusal); admit; replay; query. The CLI accepts ontology sources as a convenience, compiles them internally, and passes the compiled identity down; it never accepts a raw ontology digest as the identity. Acceptance: an adopter admits the two example plans without importing anything under `_contract_pipeline` or `research/`.

**P4. Document-assertion adapter.** Optional, ships with Core, profile `source-assertion`. Input: a reading (pages, blocks with `id`, `ordinal`, `text`) and a capture document:

```json
{"schema": "malleus.document-capture/private-v0",
 "reading_sha256": "sha256:...",
 "attribution": {"source_id": "source:...", "author": "...", "date": "..."},
 "assertions": [{"id": "asr:001", "block": "page:1:block:001",
                 "statement": "verbatim clause", "modality": "STATED",
                 "formalized_by": [{"record_id": "...", "path": ["properties", "name"]}],
                 "gaps": []}],
 "nothing_assertable": ["page:1:block:003"]}
```

Rules, each with its refusal: `reading_sha256` equals the digest of the reading bytes (`READING_MISMATCH`); every block id named by an assertion or by `nothing_assertable` exists in the reading (`UNKNOWN_BLOCK`); `statement` is a substring of the named block after whitespace normalisation, both sides collapsed to single spaces (`NOT_VERBATIM`); `modality` in STATED, MEASURED, CALCULATED, HYPOTHESISED, CONTESTED, NEGATED (`UNKNOWN_MODALITY`); an assertion with empty `formalized_by` carries at least one gap (`GAP_REQUIRED`); every `formalized_by` target exists in the records at that path (`UNKNOWN_FORMALIZATION_TARGET`); gap kinds as above. The adapter retains the capture as evidence, then emits the plan with `evidence` naming it, `derivations` pointing at assertion ids as locators, and `gaps` carrying the assertion locator.

Census, two axes, derived not declared except `nothing_assertable`, carrying the digest of the capture it was computed from: per block REVIEWED (cited by an assertion or declared nothing-assertable) or UNTOUCHED; per assertion FULLY_FORMALIZED (formalizations, no gaps), PARTLY_FORMALIZED (formalizations and gaps), UNFORMALIZED (no formalizations); gap counts by kind. What the two axes buy, stated exactly: block review no longer implies formalization, and formalization is counted per assertion. A block with one captured statement out of twelve still reads REVIEWED; what it no longer reads is formalized. The eleven statements nobody wrote down are invisible to any census. That is human sampling, outside Core.

**Then, Core's, after P4 and in this order:** P5 replay across an ontology supersession plus the revision policy (old R4: ADD_SLOT, ADD_ENUM_VALUE, ADD_CLASS admitted; ADD_IMPORT refused by policy, kept in the grammar). P6 the full `DomainHistoryProfile` contract and the three shipped profiles (old R2). P7 packs and the `pack-grounding` rite (old R3). P8 the skill's nascent-project playbook (old R5), which names the capture document, the plan and the CLI; needed before the paper rerun. P9 Event materialization (old R6), when Small Shop schedules `object-event`.

## Not Core

Query binding isolation, competency questions, human sampling, paper reruns, the three frozen paper runs. The former S5 and S6 (binding after population; a digest cannot prove precedence) move to the paper executor plan as harness checks (its E9).

## Evidence: both consumers, refreshed through P6

`handover/2026-09-03-core-population-v2/validate_examples.py` builds both
example ontologies through public `malleus.compiler.compile_linkml_contract`,
checks both plans with a reference validator of the rules above, lowers them
with a reference lowering, admits them through `KnowledgeChangeHistory`,
reopens, compares with `KnowledgeGraph.from_records`, and then provokes every
pinned rule once. It reuses Core's test helpers and is not a library
deliverable; it is the executable seed for the P1, P2, P4, and P6 tests. The
files it writes sit beside it under `examples/`. Output, verbatim:

```text
shop e4: CHANGE_SET; change change:plan:shop:B:e4; ops 1; nodes 1
shop e4: direct from_records export == governed replay export: True
shop e7: CHANGE_SET; change change:plan:shop:B:e7; supersedes ['change:plan:shop:B:e4']; op supersedes_record_id supplier-order-state:B:e4
shop e7: current SupplierOrderState rows for B: [2]
shop: reopen state digest == admitted: True
shop: ledger events 18
doc: CHANGE_SET; change change:plan:inspection-note:1; ops 3; relation depends_on ['operation:plan:inspection-note:1:1', 'operation:plan:inspection-note:1:0']
doc: evidence closure ids ['profile:source-assertion', 'plan:inspection-note:1', 'capture:inspection-note', 'plan:inspection-note:1:gaps']
doc: direct from_records export == governed replay export: True
doc census: blocks reviewed 3/3, untouched []; assertions {'FULLY_FORMALIZED': 1, 'PARTLY_FORMALIZED': 0, 'UNFORMALIZED': 2}; gaps by kind {'INTERVAL_NOT_EXPRESSIBLE': 1, 'MODALITY_NOT_EXPRESSIBLE': 1, 'TYPE_ABSENT': 1}; capture_sha256 sha256:503bb11d61c6...
gaps-only plan: lowering status NO_DOMAIN_CHANGE; change set None; retained True
grammar on empty operations: MALFORMED_CHANGE_SET: a change set must contain an operation
grammar on supersedes_record_id null: MALFORMED_CHANGE_SET: superseded record ID is required
negative cases (each must refuse):
  plan FIELDS_NOT_CLOSED: ['extra']
  plan MALFORMED_IDENTITY: contract identity must be a compiled-contract digest
  plan SOURCES_REQUIRED: sources must be a nonempty list of retained digests
  plan FAMILY_NOT_ADMITTED: signals cannot be admitted: the governed path lowers entities and relations only
  plan DUPLICATE_RECORD_ID: asset:P-7
  plan UNKNOWN_RECORD: derivation names nope
  plan ABSENT_PATH: asset:P-7:['properties', 'colour']
  plan UNLISTED_SOURCE: source:other
  plan UNDERIVED_FIELD: asset:P-7:['properties', 'name']
  plan MALFORMED_SUPERSESSION: supersedes_record_id must be a nonblank record id
  plan UNKNOWN_GAP_KIND: SHRUG
  plan UNSUPPORTED_VALID_TIME: SOMETIME
  lowering DANGLING_ENDPOINT: inspection-of:P-7:2026-03-02 -> asset:ghost
  lowering UNKNOWN_SUPERSESSION: asset:never
  contract (direct path) unknown type: Cannot rehydrate graph from records: entities[0] 'asset:P-7': Unknown entity type: 'Nope';
  governed DUPLICATE_PLAN_ID: plan:shop:B:e7
  governed re-admission of the same records: STRUCTURAL_REFUSAL: record ID already exists in history: asset:P-7
  governed UNRETAINED_EVIDENCE: capture:ghost
  profile GROUNDING_REQUIRED: domain-history grounding must not be empty
  profile UNKNOWN_SEMANTIC_UNIT: unknown domain-history semantic unit: VIBE
  profile UNKNOWN_ORIGIN: unknown domain-history origin: SOMEWHERE
  capture READING_MISMATCH: capture names a different reading
  capture UNKNOWN_BLOCK: page:9:block:999
  capture NOT_VERBATIM: asr:001
  capture UNKNOWN_MODALITY: VIBES
  capture GAP_REQUIRED: asr:002 has no formalization and no gap
  capture UNKNOWN_FORMALIZATION_TARGET: asset:P-7:['properties', 'mass']
  capture verbatim after whitespace normalisation: accepted
examples written to handover/2026-09-03-core-population-v2/examples
```

Consumer 1, Small Shop, plan for the e7 correction (`examples/small-shop-plan-e7.json`). The e4 plan (`examples/small-shop-plan-e4.json`) has the same shape with e4 in its plan id, record id, `source_occurrence_id` and valid time, row 0 in its locators, quantity 1, and no supersessions:

```json
{
  "grammar": "malleus.population-plan/private-v0",
  "plan_id": "plan:shop:B:e7",
  "contract_identity": "sha256:01470c0b41aa26720fb33c82fd65d3d00a5c26354db85b527fa6d7a79dc9beb2",
  "history_profile": {"profile_id": "state-version", "sha256": "sha256:b18f3129942761e03ce754af6cec8c689c94b91468aa105a423f5b27ddf20dc3"},
  "adapter": {"adapter_id": "small-shop-row-mapping", "version": "0"},
  "sources": [{"source_id": "source:supplier-order-history", "sha256": "sha256:a441c49f325670e09d9fc09fd8e6510669258bed1d5532cfb2b1104c4eceb081"}],
  "evidence": [],
  "records": {
    "entities": [{"type": "SupplierOrderState", "id": "supplier-order-state:B:e7",
                  "properties": {"supplier_order_id": "B", "product_code": "Y", "ordered_quantity": 2, "source_occurrence_id": "e7"}}],
    "relations": []
  },
  "supersessions": [{"record_id": "supplier-order-state:B:e7", "supersedes_record_id": "supplier-order-state:B:e4"}],
  "derivations": [
    {"record_id": "supplier-order-state:B:e7", "path": ["properties", "supplier_order_id"], "source_id": "source:supplier-order-history", "locator": "row:1:supplier_order_id"},
    {"record_id": "supplier-order-state:B:e7", "path": ["properties", "product_code"], "source_id": "source:supplier-order-history", "locator": "row:1:product_code"},
    {"record_id": "supplier-order-state:B:e7", "path": ["properties", "ordered_quantity"], "source_id": "source:supplier-order-history", "locator": "row:1:quantity"},
    {"record_id": "supplier-order-state:B:e7", "path": ["properties", "source_occurrence_id"], "source_id": "source:supplier-order-history", "locator": "row:1:event_id"}
  ],
  "gaps": [],
  "valid_time": {"kind": "ORDER_ONLY", "value": "e7"}
}
```

The source is the fixture's own `sources/supplier-order-history.jsonl` (two rows, 148 bytes). The lowered e7 change set (`examples/small-shop-change-e7.json`) carries `supersedes ["change:plan:shop:B:e4"]` derived from the base view and one operation with `supersedes_record_id`, as in the existing `correction/mapping.json`.

Consumer 2, the inspection note. Reading (`examples/reading.json`), three
blocks: "Pump P-7 was inspected on 2026-03-02. Vibration measured between 4.1
and 4.6 mm/s on 2026-03-01." / "The technician suspects bearing wear." / "Page
1 of 1." Ontology (`examples/inspection-note.yaml`): `Asset` (root `name`
required), `Inspection` (`inspected_on` required), `VibrationReading`
(`vibration_mm_s` single float), `InspectionOfRelation` (Inspection → Asset).
Capture (`examples/document-capture.json`):

```json
{
  "schema": "malleus.document-capture/private-v0",
  "reading_sha256": "sha256:7dbc2661468cfcd93b4ac43f77206f68e8a521ef95cf3865937333ebc1259745",
  "attribution": {"source_id": "source:inspection-note", "author": "maintenance technician", "date": "2026-03-02"},
  "assertions": [
    {"id": "asr:001", "block": "page:1:block:001", "statement": "Pump P-7 was inspected on 2026-03-02.", "modality": "STATED",
     "assertion_time": "2026-03-03T09:00:00Z", "domain_time": "2026-03-02",
     "formalized_by": [{"record_id": "asset:P-7", "path": ["properties", "name"]},
                       {"record_id": "inspection:P-7:2026-03-02", "path": ["properties", "inspected_on"]},
                       {"record_id": "inspection-of:P-7:2026-03-02", "path": ["properties", "relation_type"]},
                       {"record_id": "inspection-of:P-7:2026-03-02", "path": ["source_id"]},
                       {"record_id": "inspection-of:P-7:2026-03-02", "path": ["target_id"]}],
     "gaps": []},
    {"id": "asr:002", "block": "page:1:block:001", "statement": "Vibration measured between 4.1 and 4.6 mm/s on 2026-03-01.", "modality": "MEASURED",
     "assertion_time": "2026-03-03T09:05:00Z", "domain_time": "2026-03-01",
     "formalized_by": [],
     "gaps": [{"kind": "INTERVAL_NOT_EXPRESSIBLE", "statement": "VibrationReading.vibration_mm_s is a single float; the source states a range"}]},
    {"id": "asr:003", "block": "page:1:block:002", "statement": "The technician suspects bearing wear.", "modality": "HYPOTHESISED",
     "assertion_time": "2026-03-03T09:10:00Z",
     "formalized_by": [],
     "gaps": [{"kind": "TYPE_ABSENT", "statement": "no type for a suspected fault"},
              {"kind": "MODALITY_NOT_EXPRESSIBLE", "statement": "no slot carries HYPOTHESISED on any record"}]}
  ],
  "nothing_assertable": ["page:1:block:003"]
}
```

The plan the adapter emits from it (`examples/document-plan.json`) has two
entities, one relation, `evidence` naming the retained capture
(`capture:inspection-note`, `sha256:503bb11d61c6…`), five derivations all with
locator `asr:001`, three gaps with locators `asr:002` and `asr:003`, and the
shipped `source-assertion` profile
(`sha256:2317d88fd236…`). Its change-level valid time is `ORDER_ONLY` with value
`capture:inspection-note`; the two different domain dates and the third absent
domain date remain in the retained assertions. The lowered change set
(`examples/document-change.json`) has three operations, the relation depending
on both endpoint operations, and an evidence closure of the profile artifact,
the plan, the capture, and the gaps artifact. The census
(`examples/document-census.json`) carries the capture digest. A range the
vocabulary cannot hold and a hypothesis with no type become visible gaps
instead of silence, while the formalized records can still be admitted.

## Fixtures

Small Shop `small_shop_fulfilment_correction_v1` (Core's own) for the row consumer. The inspection note above for the document consumer; it is synthetic and may be copied into Core's tests as is. No paper file enters Core.

## Corrections to the previous handover, all taken

- Universal assertion format withdrawn; assertions are the document adapter's capture, not Core's contract.
- Binds the compiled contract identity, not `ontology_sha256`.
- Census has two axes, and the sentence above says exactly what that buys and what it cannot.
- Provenance is field-level (`derivations` with `path`, one per property and endpoint), matching what the paper's private format already had.
- Assertions are evidence outside the graph; the design record's sentence that said claims are graph entities under `source-assertion` is corrected in the same commit.
- "Every concrete type" is now every concrete Entity and Relation type; Signal and Event refuse with the compiler's typed reason.
- `NO_DOMAIN_CHANGE` is the typed result for a capture with zero operations.
- Evidence is retained before composition; the order in the old S4 was wrong.
- The old S5 and S6 leave Core.
- Eight of eleven pages were unreferenced by the three paper runs, not nine. The example's record ids all resolve. `supersedes` is omitted, never null. Attribution is a field.

## Reporting

Per piece: commit, tree, public symbols, tests run and what they discriminate, one usage example, and a paragraph of what the piece does not do. The paper thread receives coordinates only after the overseer has verified them on disk.
