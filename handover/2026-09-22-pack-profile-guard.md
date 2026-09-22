# The research pack loads under one profile, and a guard says so

Core agent, 2026-09-22 UTC. Base main fd68b757.

## What happened

The paper side reported (`paper-v4/reader-comparison-01/CORE-REQUEST.md`, section 2) that `OntologyRegistry` refuses Core's shipped research pack, and any schema that only imports it, with "Concrete relation 'ResearchRelation' must fix relation_type with equals_string", while `compile_linkml_contract` compiled the same pack for run-23. Luis's decision the same day: leave the pack and the rule unchanged, add a mechanical guard, declare the limit, measure before choosing a fix. This file is the measurement and the guard.

## Measurement, read only, at fd68b757

**(a) Every schema under `ontology/`, both loaders.** Registry: `OntologyRegistry(path)` with its own bundled import resolution. Compiler: `compile_linkml_contract(root_locator=<stem>, sources=...)` with the schema's exact import closure (`linkml:types` from `linkml_runtime`, `malleus`, and `metrology` plus `chronology` for research).

| Schema | Imports | OntologyRegistry | compile_linkml_contract |
|---|---|---|---|
| `malleus.yaml` | linkml:types | loads | compiles |
| `assent.yaml` | linkml:types, malleus | loads | compiles |
| `domains/attack.yaml` | linkml:types, malleus | loads | compiles |
| `domains/cyp450.yaml` | linkml:types, malleus | loads | compiles |
| `domains/ocr.yaml` | linkml:types, malleus | loads | compiles |
| `domains/recon.yaml` | linkml:types, malleus | loads | refuses: `INVALID_RANGE`, slot `source_uri` has range `linkml:uri`, not a compiler seed scalar |
| `packs/chronology.yaml` | linkml:types, malleus | loads | compiles |
| `packs/metrology.yaml` | linkml:types, malleus | loads | compiles |
| `packs/research.yaml` | linkml:types, malleus, metrology, chronology | refuses: `ResearchRelation` must fix `relation_type` with `equals_string` | compiles, fact set `sha256:69155f64…` |
| `profiles/object-event.yaml` | linkml:types, malleus | loads | compiles |

Two schemas load under one profile only. The recon refusal was not reported before; it is recorded here and in the declaration, and not acted on.

**(b) Concrete relation classes that fail the registry rule.** Measured by loading every schema with the rule bypassed in a scratch process and testing each non-abstract `Relation` subtype's effective `relation_type`. 41 concrete relation classes ship. 39 pass: 7 in attack, 5 in cyp450, 27 in recon, each fixing `relation_type` with `equals_string`. 2 fail, both in `packs/research.yaml`: `ResearchRelation` (is_a `Relation`, not abstract, `relation_type` ranged over the enum `ResearchRelationType`, eight values, no `equals_string`) and `ContributionRelation` (is_a `ResearchRelation`, inherits the same unpinned range; its description says it carries `CONTRIBUTED_TO`, but nothing pins it). The registry raises on the first it meets.

**(c) run-23's accepted graph.** Replayed from `private/paper-v4-v4-run-23/ledger/history.jsonl` (sha256 `d5ef64c0…`, 14 events, head `sha256:9fb77693…`, state `sha256:9309b9bc…`) under this Core, and cross-read against `results/export-records.json`. 440 records: 417 entities, 1 event, 22 relations. Records typed exactly `ResearchRelation`: 0. Typed exactly `ContributionRelation`: 8, every one with `relation_type` `CONTRIBUTED_TO` and no `contribution_role`. The other 14 relations are the producer's own classes, `ScholarlyRelation` 9 and `GeologicRelation` 5, and both copy the pack's pattern: `is_a: Relation` with `relation_type` ranged over a project enum and no `equals_string` (`producer/work/ontology-attempt-01.yaml` lines 376 and 415; that file's sha256 `9aa5fdcf…` is inside the ledger's validated contract). The registry refuses run-23's own ontology whatever happens to the pack.

**(d) Why the rule exists.** One concrete relation class is one predicate, so the class's narrowed `source_id` and `target_id` ranges are that predicate's endpoint signature, and `KnowledgeGraph._validate_relation` (`src/malleus/kg.py`, the endpoint loop after `_validate_payload`) checks endpoints per predicate at write time; the Prolog fact compiler follows the same shape, emitting `m_relation(id, class, source, target)` with the class as predicate (`src/malleus/logic.py`, the `m_relation` fact). Evidence: the rule came in with cbceffe3 (2026-08-12, "Add strict graph validation and assent protocol"), whose changelog "Replaced generic `DrugRelation` and `AttackRelation` classes with concrete predicate classes whose `source_id` and `target_id` use LinkML class ranges"; `docs/KNOWLEDGE_GRAPH_PROTOCOL.md` says "A generic relation enum cannot express this contract and is not accepted as a substitute"; `docs/ONTOLOGY_PROTOCOL.md` says "Do not multiplex predicates with different endpoint signatures through one generic relation class"; `tests/test_ontology.py::test_generic_relation_subclass_is_rejected` pins it. The research pack, added 2026-09-03 (6a405b11), post-dates the rule and was only ever compiled, which is why nothing caught it. One inconsistency found on the way: the inquisitor's `constrained_tongues` rite accepts an enum-ranged `relation_type` as constrained, which the registry does not.

## Guard

`tests/contract_compiler/test_shipped_ontology_profiles.py`, with its declaration `tests/contract_compiler/shipped_ontology_profiles.yaml`. Nothing in `ontology/` declares which profile a schema supports, so the declaration sits beside the test and names both profiles for every schema except two: `packs/research.yaml` is `compiler-enabled` only, with a comment citing this defect, and `domains/recon.yaml` is `typed-graph` only, with a comment citing the `INVALID_RANGE` refusal. Three tests: every schema under `ontology/` is declared and every declaration names a shipped schema with known profiles; every declared pair loads, and the failure lists each schema, profile and refusal; a copy of `ontology/` in a temporary directory with one extra pack is reported as undeclared. It lives under `tests/contract_compiler`, which the default selection already collects, so `pyproject.toml` and the two measurements that bind its bytes do not move.

RED, test present and declaration absent: 3 failed, `FileNotFoundError`. RED, declaration claiming both profiles for all ten schemas: 1 failed 2 passed, naming exactly `domains/recon.yaml under compiler-enabled: ElaborationRefusal: INVALID_RANGE ...` and `packs/research.yaml under typed-graph: OntologyError: Concrete relation 'ResearchRelation' must fix relation_type with equals_string`. GREEN with the narrowed declaration: 3 passed.

`CAPABILITIES.md`, row "Closed-world ontology and typed-graph validation", gains one sentence: the research pack is compiler-profile only today, why, and the guard's path.

## Suites

The new file: 3 passed. `tests/contract_compiler` plus `tests/test_capability_declaration.py`: 1403 passed. Full default suite: 24 failed, 3730 passed, 3 skipped. Every failure is the governance digest guard raising `LedgerValidationError: OVR-000479: latest document digest mismatch for CHANGELOG.md`, until this entry is sealed: 7 in `tests/test_contract_compiler_ledger.py`, 14 in `tests/test_contract_compiler_integration.py`, 3 in `tests/test_docs.py` (the Sphinx build renders the ledger and stops on the same error). The validator stops at the first mismatch, so the `CAPABILITIES.md` digest is not separately observed failing. Ruff check clean on the new test.

## The two fixes, measured

Both measured in scratch copies; nothing here was applied.

**Loosen the registry rule**, accepting a concrete relation whose `relation_type` is either fixed by `equals_string` or ranged over an enum. Measured by editing one condition in a copy of `src`. The research pack loads, and so does run-23's own ontology. The compiled fact set does not move (`sha256:69155f64…`, identical), no pack byte moves, and `runtime_equivalence.py compare` between this Core and the loosened copy reads `equivalent: true`, no differences. `tests/test_ontology.py`, `tests/test_kg.py`, `tests/test_inquisition.py` and the knowledge-pack tests run against the copy, with a probe test confirming the copy was the one imported: 450 passed including the probe, 3 skipped, 7 failed, all 7 from the copy living outside the repository (a path-equality assertion and six skill-install comparisons), none from the rule; `test_generic_relation_subclass_is_rejected` still passes because its relation has a string range. What moves is the guarantee: for an enum-ranged class the endpoint ranges belong to the class, not to each predicate, and for `ResearchRelation` they are the root's `Entity` and `Entity`, so the write-time endpoint check says nothing about which predicate joined which things. Two protocol documents state the opposite and would change, and the `m_relation` fact would name the class, with the predicate only in a property fact.

**Change the pack**, the smallest variant: `ResearchRelation` becomes abstract and `ContributionRelation` pins `equals_string: CONTRIBUTED_TO`. The registry loads the pack. The compiled fact set moves to `sha256:2de565e1…`, and Core's revision policy refuses the move from the shipped pack as `NON_ADDITIVE_CHANGE`, so no history on the current pack can cross to it by recorded revision. The pack's sha256 `70e0cfe6…` is named in 73 tracked files (run-09 to run-26 and shop-01 under `paper-v4/experiment-v4`, `conformance/contract_compiler/v0/bundled_declaration_scan.json`, overseer entries OVR-000403 and OVR-000405) and 338 files under `private/`, and `runtime_equivalence.py compare` fails with one difference, `imported ontology packs/research.yaml`, which is the paper's candidate refusal. run-23's 8 `ContributionRelation` records validate against the pinned class. The other seven research predicates lose their only concrete class; keeping them needs seven new classes, each with endpoint ranges someone has to choose. run-23's own ontology is still refused, at `GeologicRelation`.

The pack change fixes one pack and leaves the pattern alive in every producer ontology that copied it; the rule change fixes every such ontology and gives up the per-predicate endpoint guarantee for them. The choice is Luis's.

## Overseer entry

```json
{
  "actor": {"id": "overseer", "type": "OVERSEER"},
  "data": {
    "affected_ids": ["CC-R11"],
    "documents": [
      {"after_digest": "sha256:792109980f2ba01d6fa36295fcfe08b160d1706f9054ce44dc2c0f3352742b3e", "before_digest": "sha256:5fd1e2c4624d8124484fa5144a69cbd1504e41c695a824160cb4c7187b7fc03c", "change": "MODIFIED", "path": ".claude/skills/malleus-dev/references/CAPABILITIES.md"},
      {"after_digest": "sha256:d293853aea4866232e18c25eaac89c7b3df94f56d8969fa24fbd30fd103f0ff7", "before_digest": "sha256:b4caa1c5f57e6a8de5e4727ff563992789552041e89fc7db67888acc035d2766", "change": "MODIFIED", "path": "CHANGELOG.md"},
      {"after_digest": "<digest of this file once final>", "change": "CREATED", "path": "handover/2026-09-22-pack-profile-guard.md"},
      {"after_digest": "sha256:6660a0ea422b79d4ab4038ad2d602808f902843741ab80bc8a2cf5537772efd0", "change": "CREATED", "path": "tests/contract_compiler/shipped_ontology_profiles.yaml"},
      {"after_digest": "sha256:882f3182bd355d5c9a3e9c8c99266f8de11923718dd278a5328fbeed1b4f4006", "change": "CREATED", "path": "tests/contract_compiler/test_shipped_ontology_profiles.py"}
    ]
  },
  "entry_id": "OVR-000480",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {"relation": "EVIDENCES", "target": "7fabf14f665623b590bea23ffbb0bf4932ebca95", "type": "COMMIT"},
    {"relation": "AFFECTS", "target": "CC-R11", "type": "WORKSTREAM"}
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 480,
  "subject": {"id": "pack-profile-guard-2026-09-22", "type": "DOCUMENT"},
  "summary": "Declare the profiles every shipped schema loads under and guard them: the research pack is compiler-enabled only, recon typed-graph only. Measure both fixes for the registry refusal; apply neither.",
  "why": "The registry refuses Core's shipped research pack, and any schema importing it, because ResearchRelation and ContributionRelation range relation_type over an enum with no equals_string; the compiler compiles the same bytes. Luis ruled on 2026-09-22: pack and rule unchanged, a guard, an honest declaration, measure first. Measured at fd68b757: of ten schemas under ontology/, eight load under both loaders, research only under the compiler, recon only under the registry because the compiler refuses its linkml:uri range; 39 of 41 concrete relation classes pin their predicate; run-23 holds 0 ResearchRelation and 8 ContributionRelation records, and its own ontology repeats the pattern twice. The guard declares each schema's profiles beside the test and fails naming each refusal and each undeclared schema: RED on exactly research under typed-graph and recon under compiler-enabled, GREEN 3 passed. Loosening the rule moves no byte and no replay; changing the pack moves a digest named in 73 tracked files and is refused as non-additive. Neither is applied."
}
```

Another Core agent may draft OVR-000480 in parallel; the number is the Overlord's to assign at seal.

## Sealing note for OVR-000480, 2026-09-22

`entries/OVR-000480.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment,
the previous entry hash where placeholdered, and this file's digest filled in.
