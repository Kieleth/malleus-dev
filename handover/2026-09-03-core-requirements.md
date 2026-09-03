# Core requirements from the paper runs, 2026-09-03

From the overseer session. Decided by Luis in chat on 2026-09-03. Standing order restated: Core touches Core. Core receives requirements with reproducers, reports coordinates and tests, and does not read the paper, its questions, its schemas or its evaluation. The paper thread is an executor and files requirements only through the overseer. The overseer verifies each deliverable on disk before the paper thread is allowed to consume it.

Design record for everything below: `design/KNOWLEDGE_PACKS.md` on main (packs, grounding rule, domain-history profiles, typed gaps, revision round). Your own boundary clarification for Small Shop (commits 1a84bc0, 9c86988, ab96bd6) is on origin/main; it was carried by the design-doc push, not by a separate decision.

## Context in five lines

Three fresh producer sessions ran the same document protocol on the same source: gpt-5.6-sol, Claude Sonnet 5, Claude Opus 5. Every run compiled, admitted atomically, replayed byte for byte, and recorded zero guarded access attempts. Their answerability differed only because each invented its own vocabulary for the same five concepts, and none had a way to say what a change means. Core, the paper thread and the overseer independently reached the same object: an adopter-owned domain-history contract distinct from projection closure. The runs are frozen at tag `paper-v4-multimodel-v1` (commit fdbd1ea, branch `paper-v4-multimodel`) and serve as conformance fixtures below.

## Requirements, in dependency order

Each requirement lands as: commit and tree, the exact public symbols, tests, one minimal usage example, and a one-paragraph statement of what it does not do. Nothing below asks Core to evaluate answers, read competency questions, or hold paper schemas.

### R1. Public propose, populate, admit, replay, query

What: a library API and a CLI through which a session proposes an ontology and receives a compile receipt or typed diagnostics; submits a population and receives a construction plan with provenance, or a typed refusal; admits a change set to a ledger; replays; and queries the replayed graph. A session must never hand-write an envelope from a specification.

Why: today this path is research-local (`research/ontology_driven_kg_realization/experiments/document_paper/*`, `_contract_pipeline`). The paper's briefs existed mainly to describe that private envelope. Retiring the briefs requires the interface.

Acceptance: the three frozen runs reproduce byte for byte through the public interface, driven from their retained `run-manifest.json` and transaction times (`paper-v4/experiment-v3/runs/*/` on the tagged branch; results, replay receipts and ledger digests are in the README there). Typed refusals for every error class the current private path refuses.

Unblocks: everything else.

### R2. DomainHistoryProfile

What: a typed contract that freezes the semantic unit of a change, origin semantics and genesis boundary, which time is which, what addition, correction, retraction and transition mean, which ontology types play Entity, Event, Claim and State roles, and the projection rule family. Three shipped profiles with grounding blocks: `source-assertion`, `state-version`, `object-event`. `commitment-exchange` (REA) documented, not shipped. The change set's evidence closure binds a profile id. `CompleteProjectionClosure` references the profile id. The two contracts never merge.

Why: Small Shop's own walkthrough now states that Core supplies the generic history laws and does not choose domain change semantics, and that making change categories portable would require a separately identified domain-level contract. This is that contract.

Acceptance: a change set that binds no profile refuses; Small Shop binds `state-version` explicitly and its tests still pass; a profile without a grounding block refuses under the `pack-grounding` rite (R3).

Unblocks: the paper rerun, Small Shop's own next milestone.

### R3. Packs

What: `ontology/packs/metrology.yaml`, `chronology.yaml`, `research.yaml` per the sketches in the design record: mixins plus reference classes plus enums, each with a `grounding` annotation block; loader support for importing packs by name; the `pack-grounding` rite (presence and shape of the grounding block on packs and on project classes that extend root directly; it does not judge aptness); pack conformance rites for edited copies, which Core designs since the overseer left it open.

Why: three producers reinvented quantity with bounds, unit, determination basis, time datum and instrument deployment in one afternoon. The promotion rule says that is the signal for the layer below.

Acceptance: the rites pass on the shipped packs; a project ontology importing `research` and `metrology` compiles through R1; a pack with no grounding block is refused; `research` carries one shared `AssertionModality` enum.

Unblocks: the paper rerun.

### R4. Typed gaps and the revision round

What: a gap record of DEFER shape attached to a population proposal (kinds: interval not expressible, aggregate only, modality not expressible, required field absent in source, type absent, relation absent); replay across an ontology supersession, meaning a contract identity that changes mid-history with a migration receipt, producing one graph carrying records from both versions; a revision policy that admits ADD_SLOT, ADD_ENUM_VALUE and ADD_CLASS and refuses ADD_IMPORT while keeping it in the grammar.

Why: the skill's standing order 7 already says "log what the schema cannot express and grow the schema where those cluster". The governed path carries change-level `supersedes` and record-level `supersedes_record_id`; what it lacks is a second contract identity in one history and a typed home for the gap.

Acceptance: a two-version history replays; gaps are queryable from replay; an ADD_IMPORT revision is refused by policy with the grammar unchanged.

Unblocks: the loop.

### R5. Skill

What: the acolyte skill gains a nascent-project playbook (choose packs and a profile, propose the project schema, run the rites, populate with locators, declare gaps, extend, repeat) beside the ongoing-project standing orders; names the packs and profiles; carries the grounding standing order verbatim from the design record; describes gap declaration and the loop. Installable through `malleus-inquisitor install-skills`.

Why: the skill is the only instruction a fresh session will receive beyond isolation. It is identical for every user and every model; it is the product surface.

Acceptance: the paper thread's rerun uses no brief.

Unblocks: the paper rerun.

### R6. Event materialization and event-to-object correlation

What: `CREATE_EVENT` in the governed path plus a correlation model for Event-to-Entity participation, since relations currently require Entity endpoints.

Why: required by the `object-event` profile for Small Shop. Not required by the paper, which runs under `source-assertion` with claims as entities.

Timing: starts when Small Shop schedules the `object-event` profile, not before, unless Luis says otherwise. Not on the paper's critical path.

## Reporting

Report each requirement to the overseer with commit, tree, symbols, tests and the non-claims paragraph. The paper thread receives coordinates only after the overseer has verified them on disk. Coordination messages to the paper thread carry coordinates and nothing about evaluation.
