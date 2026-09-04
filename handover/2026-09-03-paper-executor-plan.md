# Paper thread: executor plan, 2026-09-03

From the overseer session. Decided by Luis in chat on 2026-09-03. Your proposed cut is approved with four amendments, below. Role restated: the paper thread executes; it touches no Core code; it files Core requirements with minimal reproducers through the overseer, never to Core directly; the overseer verifies every Core deliverable on disk before you consume it.

Design record: `design/KNOWLEDGE_PACKS.md` on main. Core's live instruction: `handover/2026-09-03-core-population-v2.md` (neutral population plan, governed integration, public facade and CLI, document-assertion adapter, then the remaining requirements in order). `handover/2026-09-03-core-requirements.md` stays the requirement list. Two population decisions taken after this plan was written and binding on the rerun: competency questions never enter population either, they enter only the evaluation loop; and the constructible set is every concrete type of the accepted ontology, so no binding closure before population.

## The approved cut

Approved: a pre-ontology domain-history profile; `source-assertion` history for the paper; reopen from the ontology boundary rather than retrofit; every current run retained as baseline.

Amended:

1. The profile is not a form the author fills. Malleus ships grounded reference profiles (`source-assertion`, `state-version`, `object-event`; `commitment-exchange` documented). The paper selects `source-assertion`.
2. The paper does not need the Event seam. Under `source-assertion`, assertions are capture evidence in the ledger, not graph records (ruling of 2026-09-03 late, `handover/2026-09-03-core-population-v2.md`), supersession is record-level and already exists, retraction is a superseding assertion with modality NEGATED and a superseding record where one was formalized. The one Core seam the loop needs is replay across an ontology supersession (Core R4). Event materialization is Small Shop's `object-event` track. Do not couple the paper to it.
3. Reopen only after Core's R1 to R5 exist and are verified. A rerun before that would need a hand-written brief again, and we would be measuring the brief.
4. SOSA/SSN grounds the `research` pack's Observation. It is not a fourth pack and not a paper-local schema.

## Baselines, untouched

- v2 selected run: branch `codex/paper-v4-lean`, commit 52af154, Core pin f9052b4.
- Three-producer runs and manuscript 1.2.0: branch `paper-v4-multimodel`, tag `paper-v4-multimodel-v1` (commit fdbd1ea). Runs under `paper-v4/experiment-v3/runs/`, comparison from artifacts via `paper-v4/experiment-v3/summarize_runs.py`, clean-checkout reproduction of all three runs recorded in the README.

Nothing in either is rewritten. The next version of the experiment is v4 and starts from the ontology boundary.

## Tasks that do not wait for Core

E1. Ratification package. Put the three preliminary review records (v2, Sonnet, Opus) beside the cited reading blocks in one document so Luis ratifies all three in one sitting. Human ratification is Luis's act; you prepare, you do not ratify.

E2. Brief to skill mapping. You know the briefs best. Produce one table: each brief rule, whether it is modelling (goes to the skill playbook), interface (goes to Core R1), isolation (stays in the spawn message), or question-shaped (deleted). The two population bullets about aggregate instrument counts and preferred mechanisms are question-shaped and are deleted. This table is input to Core R5, delivered through the overseer.

E3. Spawn message for v4. Isolation only: the skill is loaded; the reading is at this path; build the knowledge graph of what the document reports under the protocol; stop when nothing remains that you can add without invention; read nothing else. No questions. No modelling instruction. Retain it beside the run as before.

E4. Run matrix for v4. Three producers under the single-session loop: skill, packs, `source-assertion` profile, typed gaps, at most two revision rounds, terminal by count. One producer additionally under the stage-session strict variant, sessions joined only by ledger events. One session per cell, stated as such. Queries bound by the evaluator after each session stops. Preliminary review by a fresh Claude session under the frozen method, Luis ratifies. Explicit transaction time and clean-checkout reproduction as before.

E5. Withdrawn on 2026-09-03 (late). Core refused paper artifacts as Core fixtures, and the overseer agreed: Core tests its own neutral fixture; the overseer runs the frozen paper runs through Core's shipped adapter as the overseer's own downstream check.

E6. Manuscript 1.3 plan, prose only, no results. The domain-history profile becomes a design element in the protocol section. The three-producer comparison stays framed as what it is: vocabulary breadth under a shared constraint. The Section 4.4 finding stands.

## After Core R1 to R5 are verified

E7. Rerun the matrix. Per run, report: ontology attempts and diagnostics; packs and profile selected by the session; gaps declared, by kind; revision rounds and what each added; population records and relations; graph counts; ledger events including supersessions; rows per question; guard attempts; reproduction. Then bind queries, run, review, hand to Luis.

E8. Manuscript 1.3 results, then the same gates as 1.2.0: publication guard, fidelity tests, clean-checkout reproduction, PDF with zero warnings, tag.

E9. Harness isolation checks, moved here from Core on 2026-09-03 (late) because a digest cannot prove precedence and Core does not own the experiment: the run driver refuses a query binding whose digest predates the population freeze; a run with an empty binding still produces a census and a replay receipt; queries run only against the replayed graph. These are tests in the paper harness, beside the fidelity tests.

## Rules that do not bend

No brief. No fallback population. No question priming, in any stage, including the revision round. Every deviation from the protocol is recorded beside the run before the next step. Anything Core-side goes to the overseer as a requirement with a reproducer, not to Core.
