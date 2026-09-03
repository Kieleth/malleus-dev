# Population redesign: assertions, coverage, no questions in production. TDD plan.

From the overseer session, decided by Luis in chat on 2026-09-03 (late). Executor: the Codex paper thread. Build slowly, test first, one slice at a time; the overseer verifies each slice on disk before the next starts. This work is research-local: it touches the paper harness and nothing under `src/malleus`. Core is not involved until the result is promoted (see the last section).

## The discovery, in five lines

Across three producers the populations cited 4, 3 and 3 of 186 reading blocks and left nine of eleven pages untouched. Not reading, not capability, not vocabulary: block 1:005 alone asserts a dozen things the v2 ontology could express and the population wrote one. The producers did what the brief said: "the smallest ontology-conforming population ... useful for the four competency questions". The competency questions, a validation instrument, were handed to the production stage as its target, twice: in the brief's objective, and through the evaluator's binding closure that decided which types were constructible (19 of 48 for v2). The protocol had no notion of capture, so the only measured thing was rows for four queries, and selection optimised to it.

## Decisions

1. The population objective is coverage of the reading, never "smallest". Every block ends in exactly one state: asserted, unformalised, nothing assertable, or untouched. Untouched is a defect the census exposes.
2. The unit of capture is the assertion: a verbatim clause from one block, with modality and attribution. Typed records are formalizations of assertions (Micropublications; Wikidata's statement plus references). An assertion with no formalization is retained, with a typed gap; nothing is lost when the vocabulary is short, and later work formalizes existing assertions instead of starting over.
3. Competency questions never enter ontology or population. They enter only the evaluation loop, when the evaluator binds queries against the accepted ontology after population is frozen.
4. The constructible set is every concrete type of the accepted ontology. No binding closure before population. Recipes are optional; the plain path is records to operations.
5. Human ratification samples blocks; the graph is not shrunk to make review cheap.
6. The brief is retired. The only producer instruction beyond isolation is the skill (Core R5). Until R5 ships, the harness carries a machine-readable population document schema that the skill will later point at; no prose brief is written.

## The population document, draft for the executor to test into shape

Grounded in Malleus's own public record format (`KnowledgeGraph.from_records`: entities, relations, signals, events; type, id, properties, endpoints), plus one new family, assertions, plus gaps, plus declared coverage.

```json
{
  "schema": "malleus.population/v3",
  "ontology_sha256": "sha256:...",
  "reading_sha256": "sha256:...",
  "assertions": [
    {"id": "asr:001", "block": "page:1:block:005",
     "statement": "It can be subdivided into four 20–50 km-long subsections (Fig. 1b): the RTI segment (named RC1), the first NTD (NTD1), a short ridge segment (named RC2), and the second NTD (NTD2)",
     "modality": "STATED",
     "formalized_by": ["rec:001", "rec:002", "rec:003", "rec:004", "rec:010"],
     "gaps": [{"kind": "TYPE_ABSENT", "statement": "no type for the act of naming a subdivision"}]},
    {"id": "asr:002", "block": "page:1:block:005",
     "statement": "The MAR here spreads at a half-spreading rate of 16 mm/yr",
     "modality": "STATED",
     "formalized_by": [],
     "gaps": [{"kind": "TYPE_ABSENT", "statement": "no quantity type available in this ontology for spreading rate"}]}
  ],
  "entities": [
    {"type": "GeologicFeature", "id": "rec:001",
     "properties": {"name": "RC2", "geologic_feature_kind": "RIDGE_SEGMENT"}}
  ],
  "relations": [
    {"type": "FeaturePartOfRelation", "id": "rec:010",
     "source_id": "rec:001", "target_id": "rec:005", "properties": {},
     "supersedes": null}
  ],
  "nothing_assertable": ["page:1:block:001", "page:9:block:040"]
}
```

Rules the tests must pin:

- `statement` is verbatim text from the named block; the adapter checks containment after whitespace normalisation, and refuses otherwise.
- `modality` is one of STATED, MEASURED, CALCULATED, HYPOTHESISED, CONTESTED, NEGATED (the shared enum from `design/KNOWLEDGE_PACKS.md`).
- Every record id in `formalized_by` exists; every record is named by at least one assertion; a record named by no assertion is refused.
- Gap kinds: INTERVAL_NOT_EXPRESSIBLE, AGGREGATE_ONLY, MODALITY_NOT_EXPRESSIBLE, REQUIRED_FIELD_ABSENT_IN_SOURCE, TYPE_ABSENT, RELATION_ABSENT. An assertion with an empty `formalized_by` must carry at least one gap.
- `nothing_assertable` lists block ids explicitly; a block absent from assertions and from this list is UNTOUCHED.
- Records validate through `OntologyRegistry.validate_instance` exactly as `from_records` does; closed world; no defaults.
- `signals` and `events` families are refused with `FAMILY_NOT_ADMITTED_UNDER_PROFILE` under the current governed path; never dropped silently. This refusal is evidence for Core R6.
- `supersedes` is optional and maps to the governed path's `supersedes_record_id`.

## The coverage census

Derived, never declared except for `nothing_assertable`:

| Block state | Rule |
| --- | --- |
| ASSERTED | at least one assertion cites the block and has a non-empty `formalized_by` |
| UNFORMALISED | assertions cite the block, none has a formalization; each carries a gap |
| NOTHING_ASSERTABLE | declared by the producer |
| UNTOUCHED | none of the above |

The census output is one JSON document: per-block state, totals, gap counts by kind, and the digest of the population it was computed from. It is retained beside the results and reported per run. Applied to the three frozen runs it must show the RCA symptom mechanically: v2 four asserted and the rest untouched.

## The adapter

Input: the population document above, the reading, the accepted ontology. Output: governed operations in the change set's own grammar (record type, record id, properties, endpoints, ordinal, operation id, depends_on, optional supersedes_record_id), plus retained evidence artifacts (the population document, the assertions with their block digests, the gaps, the census), plus typed refusals. It adds order, dependency, digests and refusals. It adds no meaning.

Downstream it calls what exists at Core `f9052b4`: the private change-set composer, admission, reopen, replay, and the graph query surface, exactly as `multimodel.py` does today. No Core code changes.

## TDD slices, in order

Each slice: a failing test committed first (`RED:` commit), then the implementation (`GREEN:` commit), then a refactor if needed. Slices are small, under two hundred lines of implementation. After each slice, report the test output and the commit; the overseer verifies on disk before the next slice.

- S1. Population document validation. Tests: schema fields closed; verbatim statement containment; modality enum; formalized_by integrity; orphan record refused; gap required on unformalised assertion; signals and events refused with the typed reason. Fixture: hand-written population for block 1:005 with five assertions, following the example above.
- S2. Coverage census. Tests: the four states on a synthetic reading; totals; the three frozen runs reproduce their known block counts (4, 3, 3 asserted) when their populations are lifted into the v3 document with one assertion per cited block.
- S3. Records to operations. Tests: family order and endpoint dependencies; typed refusals for unknown type, enum violation, dangling endpoint, missing required property; the v2 population, lifted into the v3 document, replays to the same graph state digest as the frozen v2 result (`graph_state_digest` in its query result). Byte identity of operation ids is not required; graph state equality is.
- S4. Evidence closure. Tests: the population document, assertion sidecar, gaps and census are retained as evidence artifacts on the proposal and are absent from the domain graph; a run with gaps still admits.
- S5. Constructible set is every concrete type. Tests: a population using a type outside any binding admits; the binding validator still refuses a binding naming a type absent from the ontology.
- S6. Binding after population. Tests: the run driver refuses a binding whose digest predates the population freeze; queries run against the replayed graph as before; a run with an empty binding still produces a census and a replay receipt.
- S7. Reporting. `summarize_runs.py` gains the census columns. Tests on the frozen runs.

Not in scope here: the skill text (Core R5), packs (Core R3), profiles (Core R2), Event admission (Core R6), any change under `src/malleus`.

## Where to work

Branch `paper-v4-multimodel` in this repository, which holds the manifest-driven harness and its eight fidelity tests. Create a Codex worktree from that local branch; do not touch the overseer's worktree at `.claude/worktrees/paper-v4-multimodel`. Keep the fidelity tests green throughout; the v2 reference manifest and the three frozen runs are immutable fixtures. Use the hash-locked environment from `paper-v4/environment/`.

## Relation to Core R1

This adapter, once green and verified, is the research prototype of the reference adapter named in `handover/2026-09-03-core-requirements.md` R1. Promotion into the package is Core's decision after the overseer hands it over with its tests; nothing here presumes it.
