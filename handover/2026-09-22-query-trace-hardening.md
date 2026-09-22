# The command-line reads name their position, refuse undeclared vocabulary, and trace in batches

Core agent, 2026-09-22 UTC. Branch work in an isolated worktree started from
main `fd68b757e7873007ba1bb007f464d8595cac553c` and rebased onto main
`321053936383b4c5e0c4093c7a8d86b152effdee` (OVR-000480 sealed); the one
conflict, in `CHANGELOG.md`, keeps both entries. Implementation commit
`b2fd90c27daaf77360d86dd41db6e6f44d7fef3a` (before the rebase it was
`5a1846c97520172dfec6a6947d683ec53c2183fd`, same `src` and `ontology` trees).

## What was asked

The paper's reader-comparison cell needs a documented read surface for a fresh
model working from a command line (`paper-v4/reader-comparison-01/CORE-REQUEST.md`
section 1). Luis decided on 2026-09-22 that Core ships no new reader layer: it
hardens the existing `malleus-compiler query` and `trace` commands and
documents them. The paper's current experiment runs on `fd68b757` unchanged, so
no frozen coordinate and no replay of a frozen ledger may move.

## The slice

`REFERENCE_IMPLEMENTATION` under `OPTIONAL_PROFILE` semantic-history. An
adopter that does not claim semantic-history gives up nothing here: the
commands read a governed history and nothing else.

1. Claim: `replay`, `query` and `trace` name the ledger position they read and
   can refuse a moved ledger; `query` refuses vocabulary the replayed contract
   does not declare, compares by declared range or refuses, reads relations
   with stated matching, and never presents a truncated set as complete;
   `trace` gives one status per record in a batch, and an unavailable trace
   never looks like absent evidence.
2. Smallest observation: the command-line tests on two histories of different
   shape, a governed document-path history (the inspection-note capture) and
   the Shop's structural history (five plans, one contract revision, one
   supersession), both from existing fixtures.
3. Reuse: `KnowledgeHistoryProjection.current` for the position check,
   `ContractView` for vocabulary, subtype, mixin and range, `KnowledgeGraph.query`
   and `query_relations` for selection, `trace_population_record` for every
   trace. No selection, check or trace logic is reimplemented.
4. Excluded: a describe or guide command, a new query language, inference, a
   persistent service, and source resolution beyond what `trace` does today.

Nothing in `malleus.compiler` changed. `src/malleus/_contract_pipeline/view.py`
is untouched on purpose: `elaborate.py` hashes it into the producer identity
every compiled contract artifact carries, so a new public method there would
have moved every frozen artifact. The command line calls the view's private
`_terminal` for range resolution instead, with a comment saying why.

## Behaviours, RED then GREEN

All new tests are in `tests/contract_compiler/pareto/test_compiler_cli.py`.
Before the implementation the file read **13 failed, 13 passed**: the twelve
new tests and the updated existing query test failed, the thirteen untouched
tests passed. After: **26 passed**.

1. **Position.** Every `replay`, `query` and `trace` result carries
   `ledger_head` and `ledger_event_count`. `--expect-head` with
   `--expect-count` reads through `KnowledgeHistoryProjection.current`, which
   refuses `STALE_BASE` once the ledger has moved; `replay` then writes neither
   output file. One flag without the other refuses `MALFORMED_REQUEST`. RED:
   the fields were absent and the flags unknown (argparse exit 2). The
   projection binds head and count together, so both are required.
2. **Query completeness and vocabulary.** `--limit N` returns at most N
   records; the result carries `returned`, `matched` and `complete`. An
   undeclared type, mixin or field refuses `UNDECLARED_TYPE`,
   `UNDECLARED_MIXIN` or `UNDECLARED_FIELD`, naming it; a mixin given as the
   type refuses `MALFORMED_REQUEST`. RED: `--type Nonesuch` printed `[]` with
   exit 0.
3. **Relations and subtypes.** `query` now reads relation types through
   `query_relations`. RED: it read nodes only, so every relation type returned
   `[]`. `--match exact` or `subtypes` is explicit, stated in the result's
   `match` field and in `--help`.
4. **Batch trace.** `trace --batch` takes repeated `--record-id` and a JSON
   array in `--record-ids-file`, traces them in request order against one
   replay, and returns one entry per ID: `TRACED` with the trace, or the
   `PopulationTraceRefusalReason` value with `detail` and no `sources`,
   `evidence` or `derivations` keys. Without `--batch` the old single-record
   form stands, with three added fields. RED: `--record-id` repeated silently
   traced only the last ID.
5. **Documentation.** `docs/index.md`, section "Read a governed history from
   the command line", one subsection per command: arguments, result shape,
   completeness and limits, exact versus subtype matching, refusals. It carries
   no domain content (a test checks for the fixtures' domain words), and a
   test holds each subsection's flags equal to that command's `--help`.

## Decisions taken inside the brief

- **Default matching.** Node types (entities, events, signals, event
  participations) default to `subtypes`, relation types to `exact`. That is
  what `KnowledgeGraph.query` and `query_relations` do, so every existing
  caller keeps its result. The only existing command-line caller of `query`
  reads an entity type.
- **Typed comparison.** A filter is read by its field's declared range: text
  for a string or record reference, a canonical integer, `true` or `false`, a
  canonical `YYYY-MM-DD` date, or a permitted enum value. A value that does not
  read as its range refuses `INVALID_FILTER_VALUE`. Float and datetime fields
  refuse `UNSUPPORTED_COMPARISON`, as do multivalued, inlined and identifier
  fields. Float needs a decision: numeric equality after parsing (so `1.50`
  matches a stored `1.5`) or equality of spelling. Datetime has the same
  question for instants written in different zones. Multivalued needs
  membership or whole-list equality. The identifier is held as the record's
  identity, never as a field, so a filter on it could only return nothing.
  None of this was coerced.
- **Output shape.** `query` printed a bare JSON list and now prints one object
  whose `records` field is that list. A list cannot carry the position or
  completeness. `replay` and single-record `trace` only gain fields.

## Frozen evidence

- No test or research program in this repository parses `query` output except
  `test_compiler_cli.py`, updated here. Paper runs 02 to 26 and `shop-01` call
  only `retain`; `meaning_run.py` and `relationship_repair.py` call only
  `retain`; the beam-calibration test runs `replay` from its own frozen runtime
  and compares files, not stdout. Read-only check outside git: the private
  paper runners call only `capture` and `retain`, and the reader-comparison
  cells' `core_reader.py` passes command output through unparsed.
- `paper-v4/reader-comparison-01/runtime_equivalence.py project` against a
  `git archive` of `src` and `ontology` at `b2fd90c2` (and before that at
  `5a1846c9`, same result), then `compare` against
  the retained `projection-160878cf.json` and `projection-fd68b757.json`:
  `{"equivalent": true, "differences": []}` both times. Head
  `sha256:9fb776938683d0c5b04666dda13a0711cdd2a78ea99593a2264705a2d825f5ab`,
  14 events, graph state
  `sha256:9309b9bcf98613bc194756e13fd06c9c2436469adb3c2c12d56be88e8bb7af5f`,
  traces `sha256:f3d0d88aac5dd3997af44e0be0b7607a64c3e3dd4a587c0cd99de9cb52d067ae`.
  The script was run from the main checkout and not edited.

Suites at `b2fd90c2`, interpreter `.venv/bin/python`, `PYTHONPATH` set to the
worktree's `src` and root:

- `tests/contract_compiler/pareto/test_compiler_cli.py`: 26 passed.
- `research/ontology_driven_kg_realization/experiments/small_shop` with
  `.../document_paper`: 1 failed, 524 passed. The failure is the expected
  pre-existing
  `test_v2_experiment.py::test_driver_recompiles_the_exact_accepted_ontology_coordinate`.
- Full default suite: 24 failed, 3742 passed, 3 skipped. All 24 stop at the
  overseer ledger's governed-document check, `latest document digest mismatch`
  for `docs/IMPLEMENTATION_STATUS.md`, the first governed file this change
  edits that the check reaches; they clear when the entry below is sealed. By
  file: `tests/test_contract_compiler_ledger.py` 7,
  `tests/test_contract_compiler_integration.py` 14, `tests/test_docs.py` 3 (the
  Sphinx build validates the ledger). No other failure.

An earlier full-suite count taken before the rebase was discarded: the
scratchpad is shared with other agents and its output file had been written by
another worktree's run. Every count above comes from files under a directory
only this agent wrote.

## Residuals

- `.claude/skills/malleus-acolyte/SKILL.md` step 8 still says `query` filters
  are "compared as text". That is now true only for string fields. The skill
  is outside this brief.
- `query` has no lookup by record ID; a filter on the identifier refuses. A
  reader reaches one record by its type and a field, or through `trace`.
- No test builds a history whose change binds no population plan, so
  `POPULATION_PLAN_NOT_BOUND` in a batch is exercised by substituting the trace
  function in one test, not by a real ledger.
- `CORE-REQUEST.md` section 2, the research-pack registry defect, is not
  addressed here; main `7fabf14f` declared the pack compiler-profile only.

## Overseer entry

Numbered OVR-000481 because OVR-000480 is sealed on main `32105393`. Every
`before_digest` equals both the ledger's latest recorded digest for that path
(OVR-000480 for `CHANGELOG.md` and `CAPABILITIES.md`, OVR-000477, OVR-000472,
OVR-000442, OVR-000426 and OVR-000397 for the others) and the bytes at
`32105393`. Probe: the block validates against
`design/contract_compiler/overseer/ledger.schema.json` with
`Draft202012Validator` and a `FormatChecker`, with `sha256:0000...0000` for the
placeholdered hashes and digest and a real UTC time for the sealing moment:
0 errors. `why` is 970 characters, `summary` 205, eight documents.

```json
{
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "after_digest": "sha256:a1e4dbde0df8e340d8a69117ebe9308a7b998b1b80a7e731cefc2f8b3940fd34",
        "before_digest": "sha256:792109980f2ba01d6fa36295fcfe08b160d1706f9054ce44dc2c0f3352742b3e",
        "change": "MODIFIED",
        "path": ".claude/skills/malleus-dev/references/CAPABILITIES.md"
      },
      {
        "after_digest": "sha256:8ec694ecb535553d6082cad08baa31a672866ee1ed83163ed32fd82609ae23d6",
        "before_digest": "sha256:d293853aea4866232e18c25eaac89c7b3df94f56d8969fa24fbd30fd103f0ff7",
        "change": "MODIFIED",
        "path": "CHANGELOG.md"
      },
      {
        "after_digest": "sha256:64d186048711ce94598e921f2f0d9ddd13858aacd389ae8a7a4497ec6c7f6dda",
        "before_digest": "sha256:56c227a60407eadf0675fe293b8dec6a658a28092bf9c6ba10f10203f7fb7225",
        "change": "MODIFIED",
        "path": "README.md"
      },
      {
        "after_digest": "sha256:9af12ce6efd46ab9891059176ab464bd54f05d916b11adb5bd77122eb45f4789",
        "before_digest": "sha256:1f97126796b8b1420805c4d4e05703f12629650f1650325253e232493da7dca2",
        "change": "MODIFIED",
        "path": "docs/IMPLEMENTATION_STATUS.md"
      },
      {
        "after_digest": "sha256:1c19166b86eb56a74f8a3e07701a899b57f7d44d02dc047698206ee0ce728a75",
        "before_digest": "sha256:d5a38750b98118cb26cd68ffdacf9cc4a49892f0f57a8388ff8bb02856d19160",
        "change": "MODIFIED",
        "path": "docs/index.md"
      },
      {
        "after_digest": "<digest of this file once final>",
        "change": "CREATED",
        "path": "handover/2026-09-22-query-trace-hardening.md"
      },
      {
        "after_digest": "sha256:4d8fcf4637eb929ece69670cabaa8d2a709f22756d58e80362f9d84f152a4278",
        "before_digest": "sha256:221d5c35e2f971fb0cbd51411d862d2ef91b71e7a45accf8ffef3088a7b78f73",
        "change": "MODIFIED",
        "path": "src/malleus/compiler_cli.py"
      },
      {
        "after_digest": "sha256:a3545236065d570b522063b1e0a4ff7b90745de79c3d02049d13330294abebc3",
        "before_digest": "sha256:5c3f3a97e6ba40d3e3f447bd048f029f94269c54a0c341545525c4b6d0d219a7",
        "change": "MODIFIED",
        "path": "tests/contract_compiler/pareto/test_compiler_cli.py"
      }
    ]
  },
  "entry_id": "OVR-000481",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {
      "relation": "EVIDENCES",
      "target": "b2fd90c27daaf77360d86dd41db6e6f44d7fef3a",
      "type": "COMMIT"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-R11",
      "type": "WORKSTREAM"
    }
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 481,
  "subject": {
    "id": "query-trace-hardening-2026-09-22",
    "type": "DOCUMENT"
  },
  "summary": "Harden malleus-compiler replay, query and trace into a documented read surface: named position with a stale refusal, declared vocabulary and typed comparison, stated matching and completeness, batch trace.",
  "why": "The paper's reader-comparison cell needs a documented command-line read surface; Luis ruled on 2026-09-22 that Core hardens the existing commands instead of adding a reader layer. Measured on fd68b757: query returned [] for an undeclared type and for every relation type, compared an integer field as text so ordered_quantity=2 matched nothing, printed no position, and trace silently kept only the last of repeated --record-id. Now every read names its ledger head and count, --expect-head with --expect-count refuses STALE_BASE through KnowledgeHistoryProjection, query refuses undeclared vocabulary, compares by declared range and refuses float, datetime, multivalued, inlined and identifier comparisons, states its matching and completeness, and trace --batch gives one status per ID. RED 13 failed 13 passed; GREEN 26 passed. malleus.compiler and view.py are untouched, and runtime_equivalence reproduces run-23 against both retained projections with no difference."
}
```

## Sealing note

`entries/OVR-000481.json` is sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment, the
previous entry hash where placeholdered, and this file's digest filled in. If
another entry is sealed first, the Overlord renumbers at seal and re-reads each
`before_digest` against the ledger's latest.

## Sealing note for OVR-000481, 2026-09-22

`entries/OVR-000481.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment,
the previous entry hash where placeholdered, and this file's digest filled in.
