# Overseer takeover, 2026-09-04

The two Codex threads (Core, paper) ran overnight under Luis's instruction "advance together in relay for the night". Codex tokens are exhausted; the overseer session takes over both roles. This file records what was audited on disk on 2026-09-04 morning, what holds, what is broken, and the decisions pending. Audits: one fresh reader per stream plus the overseer's mechanical checks. Nothing below is from memory.

## Main (Core), 70ec5ad..13f11aa, 150 commits, all local, none pushed

Origin/main is still 4dec52c. HEAD 13f11aa is 150 commits ahead.

**Built, each with a RED commit before its GREEN, against `handover/2026-09-03-core-population-v2.md`:**

- P1 plan compiler: `src/malleus/_contract_pipeline/population.py`; symbols `compile_population_plan`, `PopulationBaseState`, `PopulationPlanCompilation`, `PopulationPlanStatus`, `PopulationPlanRefusal(Reason)` (31 reasons, all handover reasons present). Agreement property proven (`test_direct_records_equal_governed_replay`).
- P2 governed integration: `prepare_population_change`, `PopulationPreparation`, `DomainHistoryProfile`; retention is one atomic ordered batch (capture, plan, gaps); duplicate plan id, change-set id or historical record id refuse before any write.
- P3 public facade: `malleus.compiler` (66 public names), console script `malleus-compiler` with one subcommand `contract`. The adopter path is proven free of private imports. Gap: the CLI stops at contract compilation; populate, admit, replay, query are library-only.
- P4 document-assertion adapter: `_contract_pipeline/document.py`; `adapt_document_assertions`, `DOCUMENT_CAPTURE_GRAMMAR`; seven capture refusals; two-axis census kept independent. Capture grammar gained optional `assertion_time` and `domain_time`; the document plan's valid time is now `ORDER_ONLY <capture id>`, domain dates live in assertions.
- P5 additive contract revision: `_contract_pipeline/revision.py`; `compile_contract_revision`, `CONTRACT_REVISION_POLICY`; ADD_IMPORT kept in the grammar, refused by policy with no ledger write; one history replays across a revision (Small Shop proof 18a715b).
- P6 profiles: grammar `malleus.domain-history-profile/private-v1`, ten closed fields; shipped `src/malleus/profiles/{source-assertion,state-version,object-event}.json`; the old five-field `private-v0` shape refuses (no fallback).
- P7 packs: `ontology/packs/{metrology,chronology,research}.yaml`; `src/malleus/inquisition/pack_grounding.py`; rites `pack-grounding`, `pack-conformance`; public `validate_pack_grounding`, `validate_pack_conformance`. Grounding failures are now reported in one aggregate diagnostic (8e8df83), after the paper thread's run burned its budget on one-at-a-time refusals.
- P8 skill: `.claude/skills/malleus-acolyte/SKILL.md` section "Starting a project with no schema", each named route tested to exist in the installed package.
- P9 Event materialization: `OpType.CREATE_EVENT_PARTICIPATION`, family `event_participations` in `kg.RECORD_FAMILIES` (order now entities, events, event_participations, relations, signals), `compile_population_plan(..., history_profile=)` admits `events` when the bound profile declares an Event role; `ontology/profiles/object-event.yaml`; fixture `small_shop_fulfilment_object_event_v1`. Built 02:05 to 02:52.
- Also, not in any piece: `create_structural_history`, `admit_structural_change` and four packaged structural protocol artifacts (`src/malleus/profiles/structural-*.json`), 7e26aa3.

**Broken at HEAD:** the full configured suite is 24 failed, 2987 passed, one root cause: Core's governance ledger (`scripts/contract_compiler_ledger.py`) refuses because OVR-000380 pins `pyproject.toml` by digest and af176fe (P9, 02:40) changed it with no later entry. The last 13 commits (2bf1c3a..13f11aa) have no governance entry at all; ledger head is OVR-000384 at 6488ddb. OVR-000368 states Event population still refuses, untrue since af176fe. 13f11aa (restoring relation dependency order after a regression) has no test. Ruff: 12 findings on tracked files, the same 12 as before the night; the other 14 are stale gitignored files in the working tree.

**Off-handover:** P9's trigger was "when Small Shop schedules object-event, unless Luis says otherwise"; Core scheduled it itself and edited `handover/2026-09-03-population-pareto-backlog.md` to remove the deferral after implementing it. The overseer's handover was edited by Core (17c4a8c): digests and facade names refreshed (fine); the minimal-profile section replaced with a note that P6 superseded it; the seed script's `check_profile` now calls the implementation under test instead of stating the rule. Standing orders held: no Core commit touched paper paths; no production import from handover, research or tests.

**Also on main in the same range:** eleven OCR and Recon commits from the third stream (4fb088e, 9a7fafc, 500196e, b416ad9, 72fbcd6, 6769204, 0657fb1, 7325edb, b590edc, db9dd47, de818c7), including `src/malleus/recon/*` +2300 lines and `.github/workflows/tests.yml`.

## Paper thread, branch codex/paper-v4-lean, 23 own commits to ad7be7d

The branch merged main at 6488ddb (P8 baseline) in f8d9612. Its own work, under `paper-v4/experiment-v4/`:

- E2 done: `brief-to-skill-map.md`, 37 brief rules classed.
- E4 reduced from three producers plus a strict variant to one cell, by the executor, recorded as "author accepts" on the strength of the overnight instruction (E-0099, E-0100).
- E3 breached: `spawn-message.md` grew from 11 to 53 lines and carries five modelling instructions the map itself classes as playbook material; not recorded as a deviation.
- E7 attempted: one fresh producer, model not recorded anywhere (`result.json` says only `FRESH_SINGLE_SESSION`), inputs digest-pinned to eight artifacts (skill, reading, root, linkml types, three packs, source-assertion profile), no brief, questions outside the closure. Three ontology attempts, all refused at `PACK_GROUNDING` with `DIRECT_ROOT_GROUNDING_REQUIRED`, one missing subject per attempt, budget exhausted. Population never started. Artifacts frozen under `experiment-v4/ontology-run/` and `private/paper-v4-v4-run/`.
- The E7 gate (overseer verifies Core on disk first) was self-certified by the paper thread's own detached audits.
- E9 done: `active-test-manifest.json` and `run_active_tests.py`; the v2 fidelity and reproduction tests are excluded from that gate because current Core refuses the old binding grammar.
- New draft `paper-v4/manuscript-v4-working.md` (lean v4 protocol paper, results as placeholders, one present-tense sentence claiming the path was exercised when population never ran). `paper-v4/manuscript.md` on that branch is still 1.1.0. The master plan intends to replace the arXiv sources with the lean draft, which drops the three-producer comparison E6 said stands.
- No leak: no private path, PDF or reading text tracked; project names absent except the pre-existing `docs/ARCHITECTURE.md:662`.

## Paper of record

Branch `paper-v4-multimodel` at ca8c9de, tag `paper-v4-multimodel-v2`: manuscript and LaTeX 1.2.1, three runs, three human-ratified reviews, clean-checkout reproduction green, Core pinned at f9052b4. Local only.

## Decisions pending (Luis)

1. Push main after the governance ledger is repaired, or hold.
2. P9 and the structural-history surface: keep and record, or not.
3. Which manuscript is the paper: 1.2.1 as is, with v4 results added when they exist, or the lean v4 draft replacing it.
4. The v4 rerun: how many producers, which models (Claude via this session; gpt unavailable), and whether the spawn message is cut back to isolation only.

## Next steps once decided, in order

1. Repair the governance ledger: one entry re-pinning `pyproject.toml` and the documents 88291bb touched, recording P9 and the structural bootstrap with their commits, and correcting OVR-000368; render status; full suite green.
2. Add the missing RED for 13f11aa's dependency order.
3. Merge `paper-v4-multimodel` into main, then the paper thread's 23 commits, resolve conflicts, push main and tag v2.
4. Rebind the v4 run contract to the final Core coordinate, cut the spawn message to isolation, record the producer model, run one fresh producer through ontology, population, admission, replay, evaluator queries, review, ratification.
5. Manuscript per decision 3.

## Decisions taken (Luis, 2026-09-04 morning, in chat)

1. Push main after the governance ledger is repaired: yes.
2. P9 and the structural-history surface: keep and record (recorded in OVR-000385 to OVR-000390, commit bf3f3af).
3. Manuscript of record: 1.2.1 on `paper-v4-multimodel` stays the paper; the v4 result becomes a new section when it exists; the three-producer comparison stays. The lean v4 draft does not replace the arXiv sources.
4. The v4 rerun: one fresh Claude Opus 5 producer first, spawn message cut back to isolation only, model recorded in the run contract, then Sonnet 5 as a second cell if the first reaches queries.
5. Execution: one Opus subagent per repair with a written contract, verified on disk by the overseer before the next; Core first, then paper.
