# Five-front review, 2026-09-09

Overseer review (Claude session 264ec7c2) of the five Codex-driven fronts, read from the rollout files on disk and the repo. Every count below was checked against a receipt, a ledger entry, PyPI, or a git command; the Codex dumps and the per-front reader reports live in this session's scratchpad. Nothing here is a decision; decisions are Luis's and are listed at the end.

## Ruling (Luis, 2026-09-09, in chat)

"Lets take over 1-2-3, store 4 through 9 for after we've finished. Make sure is in the ledger/journal/documented we're taking over from now."

Taken over by the Claude overseer session from this point: (1) this session is the engine for paper and Core work while the Codex threads are stopped; (2) the 62 unpushed commits are pushed after one full-suite run at HEAD; (3) the Codex paper thread's working tree is checkpoint-committed by pathspec after the paper gate. Decisions 4 to 9 below are stored, not acted on, until the taken-over work is finished. Execution record: the 62 commits pushed at 82b33967 after the full default suite (3428 passed, 2 skipped); the Codex paper working tree checkpointed on the local branch paper-checkpoint-2026-09-09 (not main, not pushed) because its gate is red under the manifest environment (answer-demonstration pins Core to 160878cf and refuses HEAD src) and its manuscript and submission appendix carry four verbatim 60-to-67-character runs of the withheld reading; paper ledger E-0338 on that branch; overseer journal (2026-09-09 section) and Core overseer ledger OVR-000456 on main.

## The blocker

All Codex threads are stopped on the account usage limit. Last error in the paper, Core and Robotics rollouts: "You've hit your usage limit ... try again at Sep 14th, 2026 6:26 PM" (paper 2026-09-09T04:17:09Z after Luis's "Go"; Core fork 03:32:29Z; Robotics 15:56:18Z, retrying every 5 minutes since 14:38Z with 142 failures). The unnamed thread opened 2026-09-09 08:42 PDT is a `codex-auto-review` thread with no turns.

## Repo exposure at HEAD 82b33967

- 62 commits on main not on origin (all 2026-09-08 after 13:21 PDT): 17 Core, 20 Shop exercise (`research/ontology_driven_kg_realization`), 25 semantic re-entry (incl. 5 merges). Only two carry runtime: a7c54fa8 (`src/malleus/_control_rules.py`, `authorization-control-v1.json`) and 1385223e (transition rules in the owning history fold). Neither is in the released 0.14.0 wheel.
- Paper working tree uncommitted since dfa367a (2026-09-06): ledger E-0212..E-0337 (+5268 lines, committed prefix through E-0211 unaltered, 0 deleted lines), manuscript +1056/-…, master plan +1088 (1.3.2 to 1.5.35), test manifest +9 (adds `private_fixture_patterns`).
- Robotics branch `codex/robomme-offline` (worktree ~/.codex/worktrees/8ce0): 37 ahead, 346 behind main, not on origin, 198.8 MB tracked under `research/robotics_simulation` (18.7 MB history.jsonl, 4.2 MB GIF), 83 GB gitignored on disk, 24 dirty paths (the observer stage).
- 34 clones under /private/tmp/malleus-reentry-* hold evidence that re-entry receipts reference by path; not durable.
- Untracked PDFs are our own rendered drafts (output/pdf, tmp/pdfs); no source PDF untracked. `private/` ignored.

## Core (Codex 01a02f71; Shop fork 01a08375 opened 2026-09-09T00:01Z "just shop")

- Released 0.14.0: tag v0.14.0 at e2b9e779 on origin; PyPI wheel e99ca688… and sdist e6cc4e1a… uploaded 2026-09-08T23:32Z, hashes equal to `handover/2026-09-08-core-release.md:168-169`; gate 3,359 passed, 3 skipped on a clean checkout. No GitHub Release page.
- After the tag: declarative authorization rule artifact (a7c54fa8); transition rules RED 29508f3b/57537d20, GREEN 1385223e; maintained ledger-fed projection 851913c0 (469 tests); Shop shipment explanation on existing Core APIs (Shop reports 318 passing); adopter completion guidance (the "we finished looking is not we finished representing" rule).
- HEAD collects 3,430 tests (not run this review).
- Open: `AuthorizationDecision.relied_on_claim_version_ids` is required in assent.yaml; standalone `_missing_required` treats an empty list as missing, compiled `validate_instance` accepts it, the finite authorization program constrains it to maxItems=0. Backlog: "Resolve that contract choice before any cutover" (`handover/2026-09-08-core-backlog.md:120`; detail `2026-09-08-authorization-lifecycle-comparison.md:70-81`).
- Core-23 (valid-time kind for "none stated", from the 2026-09-06 paper handover) was never dispatched by the overseer, but its substance landed on 09-06 through the Codex Core thread on Luis's approval: RED 32804a0b, GREEN 5c8b0cc9 (NONE_STATED kind in src/malleus/valid_time.py, the skill and the docs; OVR-000420 and OVR-000425; handover/2026-09-06-unstated-valid-time.md). Verified 2026-09-09: tests/contract_compiler/pareto/test_unstated_valid_time.py 16 passed at HEAD. Nothing to dispatch.
- Last turn: idle after answering Luis's "Too abstract, bring it to an example" (2026-09-09T03:05Z).

## Paper (Codex 01a063a6)

- Since 09-06: E-0212 declares "no run-22 restart, no Core-23 dispatch, no Shop re-review"; fresh gpt-5.6-sol producers on the thirty questions, gpt-6-astra reviewers; E-0302 thirty-answer assessment (25 positive: 5 COVERED, 12 PARTIAL, 8 NONE; 41 witnesses SUPPORTED); E-0325 four-way comparison complete/partial/none: earlier fresh 0/2/23, supplied ontology 3/15/7, repaired graph 7/11/7, new fresh 1/10/14; paper gate 617 passed in 281.92 s; count, context, duration and causal-event query repairs (E-0303..E-0328); E-0337 Core prevention guidance verified.
- Manuscript rewritten: "Malleus: From Model Proposals to Replayable Knowledge", 5,170 words (ruling D4 of 2026-09-02 said about 3,500).
- Protocol v3 is never named in the added entries; the v3 replicates (run-22 continuation, run-23/24) are unstarted, not contradicted.
- Last assistant turn proposes the four questions (adequate ontology from a document; faithful population; preserve and reconstruct accepted changes; reader retrieval and composition) as "the work structure and completion criteria" with three milestones; Luis's "Go" at 04:17Z hit the quota.

## Semantic re-entry (Codex 01a05f67, worktree 3eda)

- Thin slice complete and integrated: a derived finding may affect accepted knowledge or the world only through a proposal pinned to accepted state; never mutates the graph or dispatches an effect. Receipts: single-action loop 388 (`supplier-reentry-final-result.json`), undesired observation 452, two-alternative choice 485, with transition rules 650 = 205+112+193+140 plus 12 guards (`supplier-choice-transition-result.json`). Merged 62655e44; journal OVR-000454 (a8636baf).
- Last turn 02:41Z: "Integration is closed, with no runtime change or release. The proposed next step remains the second, independent proposal generator ... it awaits your approval." Alternative stated: ground the target in accepted customer demand instead of the supplied goal "two" (needs a Shop fixture decision).
- Unanswered since 2026-09-07T08:32Z: "do you approve requiring a proposal to immediately follow registration of its pinned context, with any intervening event causing refusal?"

## Robotics (Codex 01a079a5, branch codex/robomme-offline)

- RoboMME (16 memory tasks) on the ManiSkill fork over SAPIEN 3.0.3, MPlib 0.1.1, tasks PickXtimes and VideoUnmaskSwap, policy checkpoint Yinpei/mme_vla_suite, dataset Yinpei/robomme_data_h5.
- Landed: Core-governed recorded dispatch (65 tests, stale-domain refusal with zero executor calls); MPlib built on Mac; policy loads in 4.0 s and returns 20 command rows; 422e6304 first native governed batch, 16 commands through Core into the live simulator; uncommitted observer stage, 46 events replayed.
- Not shown: task success (success=false), accepted task memory used (false), any advantage over an event log (one head-to-head, a tie with SQLite).
- Open (loop-state.json pending_decisions): external VLM model/backend and spend; research partition and annotation; comparison boundary; primary endpoint. Licensing of RoboMME assets not audited.

## Malleus-code (Codex 01a0357c, lab repo, silent since 2026-09-04)

- Two pilots on RET-010 (O1, X1, OrderContainsUnit) both recorded failed; lab suite 524 passed (reproduced this review, 354 s).
- RCA (2026-09-04T03:35Z): "the system recorded provenance and freshness, but had no machine-readable notion of evidence applicability. It could prove which commit the tests ran against, but not that those tests exercised the exact RET-010 thing named by the requirement." Chain: requirement weakened in the contract to "any successfully replayed accepted Core history"; builder invented fulfilment:42; tests green; evidence SATISFIED; staged delivery ACTIONABLE; independent review ran real RET-010 and the evidence became VIOLATED.
- Steer implemented: AuthorityGrant slots (Core 5e4ec73e), EPISTEMIC_DECIDED then AUTHORIZATION_DECIDED, AdvanceDeliverableAction, frontier, dojo mode. Not as written: store/transaction/validation/shacl wrap malleus rather than being replaced.
- Unanswered: "Approve designing that slice next?" (exact product-boundary evidence). "applicability" appears nowhere in ontology/ or assent.

## Decisions for Luis (put in chat 2026-09-09)

1. Engine until Sep 14: wait, buy Codex credits, or run paper and Core work from the Claude session.
2. Push the 62 commits (three fronts in one linear history) after one full-suite run, or hold.
3. Checkpoint-commit the paper working tree by pathspec after the 617-test gate, or leave it for Codex.
4. Paper direction: v3 replicates as ruled 09-06, Codex's four-question milestones, or write now with 7/11/7; and whether D4 (about 3,500 words) still holds.
5. Core empty-claims contract: required = present (empty allowed, cardinality per profile), required = non-empty, or slot optional.
6. Re-entry: adjacency rule yes/no; next slice second generator, demand grounding, or stop.
7. Robotics: continue after quota with the four decisions, or park; branch weight before any merge.
8. Malleus-code: evidence applicability as a Core requirement, and the product-boundary evidence slice.
9. Housekeeping: copy referenced evidence out of /private/tmp; robotics branch weight.
