# Adopters follow Core: the rule in both skills, the document runner migrated, the door guarded

Overlord (the Core session), 2026-09-21 UTC. Paper ledger context: E-0509, E-0510 and its addendum; the pen for the ledger is the paper session's, so this file is the Core session's durable record of the day.

## What happened

Decision D closed Core's public admission door on 2026-09-20 (OVR-000471 to OVR-000475). One repository runner was left on the old two-step path: the document path, `research/ontology_driven_kg_realization/experiments/document_paper/document_run.py`, which the marine-article reconsideration will go through. On 2026-09-21 a Core agent migrated it to `malleus.compiler.check_and_admit_change_set` (commits 6be96df1, fee18aef, 739666bd; the Overlord moved its import to Core's public surface at fa4c3785). The runner's own event factory, its literal SATISFIED receipts and its private two-check policy are deleted; its retained contract is Core's built-in structural check, byte-identical to the Shop programs' copy; its two recomputes stay as evidence Core does not vouch for. Exported records, graph snapshot, plan bytes and provenance bytes are identical against the last Core where the path ran; the declared moves are one fewer ledger event, one check record instead of two, and the identities that hang off them. The path's stale `private-v0` history binding, present in the production runner and not only in a fixture, was repaired because no history could be constructed without it. Document path suite 7 failed, 150 passed, 7 errors before; 1 failed, 162 passed, 0 errors after, the one a frozen v2 ontology compile digest that fails identically on pre-door Core.

`tests/test_caller_supplied_check_event_scan.py` is new: a static scan over the tracked tree that fails the default suite when any file under `src/`, `research/` or `tests/` hands `admit` or `admit_with_anchors` a caller-built `CHECK_RECORDED` or `VERDICT_RECORDED` event. Core's five own door tests are the named exceptions, with a companion test that fails if one stops exercising the refusal. `paper-v4/` is excluded by declaration and the two paper-side runners are named in the docstring as the paper front's to adapt. One residue is declared: `research/action_history_contract_freeze/programs/test_action_inputs.py`, a blocked research audit frozen at its own base Core 2a112405, kept as historical evidence by the Overlord's decision on Luis's "go with your recs".

Luis, 2026-09-21, on the document path having no reconsideration protocol: "correct, we've moved Core, all protocol adopters need to be adapted, make sure this is part of the skill (before touching anything, check if your current project is aligned with core version, if not go into core and make sure you bring all to date in the project...)". The rule entered both skills at 790198f1: the Core-side sentence in the dev skill's "Implementation sequence" (a Core change that moves a public surface adapts every adopter in this repository in the same branch, with a guard test), and the adopter-side check at the top of the acolyte skill's "Before you build: the gate" (read the pinned Core commit, compare with main, bring the project current first, re-pin; no pin means unknown). The dev skill's still-two-step list and ROADMAP F1 were brought current in the same commit.

## Overseer entry

```json
{
  "actor": {"id": "overseer", "type": "OVERSEER"},
  "data": {
    "affected_ids": ["CC-R11"],
    "documents": [
      {"after_digest": "sha256:527cc1f3b8a45a3a05af176530b4a823184c8884a1d463bd5353f55b7e1ef811", "before_digest": "sha256:4e457d697a79e091f5b86be39b736e678f511f145ee0bc3c1b8062c6c040a9fb", "change": "MODIFIED", "path": ".claude/skills/malleus-acolyte/SKILL.md"},
      {"after_digest": "sha256:75ee7ec845c078fcf9a5df391e624ed15c1ba4f4e6ef476e32ef7910479cffbd", "before_digest": "sha256:b18e426e8e8bfb60217f2dde44cd641dd7b6f53aaf027a820ea20c6a3940d9ab", "change": "MODIFIED", "path": ".claude/skills/malleus-dev/SKILL.md"},
      {"after_digest": "sha256:f063810bcb3944379fa73c66f0f86d1147b80b0c74b54db39eacbc3ffb71a531", "before_digest": "sha256:52e1dc247a8d97535addb5c729f5e7f1d1e84a78fa0ecdfb61e5202ab4cecc83", "change": "MODIFIED", "path": "ROADMAP.md"},
      {"after_digest": "<digest of this file once final>", "change": "CREATED", "path": "handover/2026-09-21-adopters-follow-core.md"},
      {"after_digest": "sha256:55c23cccf2ea94d85eee3bb35cafb777b9e8ba27dd5e6c77de9f70fcbd959618", "change": "CREATED", "path": "tests/test_caller_supplied_check_event_scan.py"}
    ]
  },
  "entry_id": "OVR-000476",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {"relation": "EVIDENCES", "target": "6be96df1cccbec43d42d2ddc9407059e58784236", "type": "COMMIT"},
    {"relation": "EVIDENCES", "target": "fee18aef05f70af9e2509cef40fe5e40c42c5826", "type": "COMMIT"},
    {"relation": "EVIDENCES", "target": "739666bdb09fd6566e5a017aa687af64bec07f42", "type": "COMMIT"},
    {"relation": "EVIDENCES", "target": "fa4c3785be6043fed25a92f4c316811c5ba970b9", "type": "COMMIT"},
    {"relation": "EVIDENCES", "target": "790198f1fb424381b3c72a3c062ea6d4249c777b", "type": "COMMIT"},
    {"relation": "AFFECTS", "target": "CC-R11", "type": "WORKSTREAM"}
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 476,
  "subject": {"id": "adopters-follow-core-2026-09-21", "type": "DOCUMENT"},
  "summary": "Record the rule that adopters follow Core in both skills, the document path runner's migration to Core's own admission, the static guard over the closed door, and the ROADMAP F1 statement brought current.",
  "why": "Decision D closed the two-step admission door and migrated eight research programs; the document path runner, which the marine-article reconsideration will use, was left two-step and unexercised. It is now migrated to check_and_admit_change_set with exported graph, plan and provenance bytes identical, and a static AST scan over the tracked tree fails the default suite on any caller that hands Core its own check or verdict event, Core's five door tests excepted and one blocked historical audit declared. Luis ruled on 2026-09-21 that every protocol adopter follows a Core move and that the skills must enforce checking a project's Core coordinate before any work; the sentence enters the dev skill (Core side) and the acolyte skill (adopter side). The skill's still-two-step list and ROADMAP F1 now name what remains: the two paper-side runners, the paper front's to adapt, and the frozen action-history audit at its Core 2a112405."
}
```

## Sealing note for OVR-000476, 2026-09-21

`entries/OVR-000476.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment,
the previous entry hash where placeholdered, and this file's digest filled in.
