# Paper v4 steer, 2026-09-02

Author decisions taken by Luis in chat with the overseer session on the evening of 2026-09-02, after a read of the "Draft lean Malleus arXiv paper" thread, `paper-v4/`, `private/paper-v4-ocr`, and a run of the experiment suite (121 passed under `.venv`). They supersede plan decision D-0010 and the plan 0.2.0 evaluation choices they contradict. Record them in `paper-ledger.md` as D-0011 to D-0016 with source "Author decision via overseer session, 2026-09-02", bump the plan, and update the manuscript status line.

All six decisions are closed. D3 and D6 were closed after D1, D2, D4 and D5, in the same session. D6 replaces the review loop in D2; read D2 in the light of D6.

## D1 Reading layer: PDF text layer, not raster OCR

Decision: the selected reading is the PDF text layer, extracted by one declared tool at one pinned version and frozen by digest. The raster and Tesseract path leaves the paper. `malleus-ocr` leaves the paper path; one sentence in future work at most.

Why: the raster reading the model saw has `CO2` broken into `CO,` in 42 of 59 occurrences. The text layer has 74 `CO2` and zero `CO,`. Two of the four competency questions are about CO2. The OCR gate measured lineage and coverage, not transcription, so nothing caught it. Faithfulness to the OCR profile was never the ask.

What changes:

- New selected reading and block projection from the text layer. `pdftotext` 26.03.0 is on this host but is a system binary; a pip dependency such as `pypdf` is easier to capture in project configuration. Pick one, pin it, stop.
- Re-bind the sealed oracle locators to the new blocks. Evaluator-only step.
- Retire the OCR precommit, execution receipt, verification, bundle, alignment guard and their tests from the experiment. Keep the retained files under `private/` untouched. Do not delete, do not cite.
- Rendering, Tesseract and trained data leave the dependency set.

## D2 Ontology acceptance: no hand repair

Decision: the ontology run is re-executed on the text-layer reading, since the refused run was built on corrupted text. Same task brief, same fresh-session rules. Compiler diagnostics are returned to the session up to twice, as already precommitted. The compiled ontology is then accepted for population under D6; there is no adequacy review and no supersession round.

The hand-authored recovery ontology (`controlled-ontology-recovery.yaml`, its precommit, compilation, review and receipt) is retired. Not deleted, not used, not cited as the paper's ontology. The Tesseract-era refused run is retained as history and gets at most one sentence in limitations.

Why: editing the schema by hand and presenting it as a control, however many precommits wrap it, reads as post-hoc repair. The earlier draft of this steer replaced the hand repair with a DEFER-and-supersede round; D6 removes the reviewer that round would have answered to, so the round goes with it.

## D4 Ceremony budget: five identities

Decision: the experiment freezes five identities and no more.

1. Source PDF digest.
2. Selected reading digest.
3. Selected ontology digest.
4. Ledger head and replay receipt.
5. Query binding digest.

Stop:

- Precommit plus receipt plus test triples per step. One retained artifact per step where the step produces something; a test only where a real error class was found.
- Pinning sha256 of living shared docs (`SKILL.md`, `ADOPTION_GUIDE.md`, `IMPLEMENTATION_STATUS.md`, `ontology/malleus.yaml`). The Core session edits those concurrently; `IMPLEMENTATION_STATUS.md` had already drifted at review time. Copy the exact bytes the model saw into the experiment's retained input directory once, and pin those copies.
- Sub-agent hostile reviews of each other's work.
- New guard artifacts for harness-internal mistakes.
- Plan version bumps per step. Bump at author decisions only.

Manuscript: target about 3,500 words. Section 2.2 terms becomes one paragraph. Section 4.7, the April pilot, goes to one sentence in limitations or out. Each term is defined once, on first use, and the set is small: ontology, change set, ledger, replay, locator, query. Retire "final-identity", "private semantic-history profile", "AUDIT_ONLY", "frontend-neutral", "one-chain-per-page". The non-claims section and the related-work list stay as they are; they are the strongest part.

## D5 Isolation: a clean checkout, and the PDF stays out of git

Decision: the experiment runs against a clean checkout of Core `1611944` in its own worktree or branch, not the main worktree. Today the tests import `src/malleus/_contract_pipeline/knowledge.py` from a working tree where the Core session has that file modified and uncommitted, so "pinned to 1611944" is true of one YAML file and false of the code under test.

- Move `paper-v4/` into that worktree or branch. It is currently untracked and un-ignored in the main worktree, where another session commits.
- The PDF is never committed. Manifest, URL and digest are enough; the plan already says so. Add `paper-v4/source/*.pdf` and `__pycache__/` to the ignore rules.
- Keep ignoring the Core thread's Small Shop temporal-correction delegations, as E-0064 already does.

## D3 Population: the model writes the facts, no fallback

Decision: a fresh model session, given the selected ontology and the selected reading, proposes the facts that enter the graph, with a block locator per value. Malleus compiles, refuses what is malformed, admits the rest, replays, and the four queries run. The exact-match score against the sealed oracle is the result, whatever it is.

Evaluator-authored population, as chosen in the thread at 19:56 PDT, is withdrawn. There is no fallback to it. If the model's population fails structurally or scores badly, that is the paper's result, reported as such.

Why: the thesis is that a model's reading of a document can be captured in a governed graph and retrieved without embeddings. Facts written by the party holding the answer key cannot fail on content and therefore test nothing about that thesis. Small Shop already covers the plumbing-only case.

What changes:

- One population task brief for a fresh session: inputs are the selected ontology, the selected reading, the recipe library and the competency questions. Output is one machine-readable population file, each value carrying a block locator. Same fresh-session rules as the ontology stage. Retry policy: structural compiler diagnostics only, one retry, no adequacy review at this stage.
- The recipe library (`document-control-recipes.stottr`) may stay as the construction vocabulary the model populates against, if it is generic. Any recipe that encodes an answer value is retired.
- Refusals during population are the negative cases. Synthetic mutations are added only for error classes the run did not produce naturally, and only from the list already in the plan.

## D6 No LLM adequacy reviewer: the compiler is the gate, the questions are the judge

Decision: the one-shot adequacy review stage is removed. No rubric, no reviewer session, no `SELECTED` or `REFUSED_ADEQUACY` outcome. The stages become:

1. The fresh session proposes the ontology. Compiler diagnostics returned up to twice.
2. The compiled ontology is accepted for population by one recorded evaluator decision event carrying the ontology digest and the evaluator actor id. One ledger event, nothing else.
3. Queries are bound before population to the ontology's record types, relation types and enum values only. The binding must not pin a graph closure. The current binding fixes an exact 15-entity, 20-relation closure; a model-populated graph cannot have its size decided in advance. Rebind.
4. Population under D3, ledger, replay, four queries, score against the sealed oracle.

Whether the ontology was adequate is measured, not judged: a schema with one count slot where the source has two returns one number for CQ-01 and mismatches the key. That mismatch, with its locator, is the result.

Retire: `ontology-review-task.md`, `ontology-review-precommit.json`, `ontology-review-output-schema.json`, `ontology-review-input-manifest.json`, the adequacy receipts and their tests, and the review-input package under `document_paper/ontology_review_inputs.py` if nothing else uses it. Keep the files, stop citing them.

Why: the adequacy reviewer is not a Malleus mechanism. It was added by the experiment, its rubric was written by the experimenter, and it produced both the refusal and the hand repair. Malleus governs commitment with a compiler, typed checks and recorded decisions. The competency questions already exist to judge semantic adequacy. Removing the reviewer deletes one stage, one rubric, one model session and the largest remaining risk of ending with no graph.

## Framing

The paper is an engineering paper about a commitment boundary, demonstrated on one document with four questions. Title and abstract say that. Prior art is conceded as the related-work section already does: SPIRES for LLM extraction into LinkML-typed knowledge bases, OntoLogX for validate-before-persist, Nexus for append-only replayed projections. What this paper adds is the explicit executable boundary with proposal, recorded decision, ledger and replay as separate identified steps, and a model on both sides of it. "No embedding index" stays a bounded observation about the tested path, never the headline.

## Order

D5, then D1, then D2 with D6, then D3, then queries, then fill the result fields, then cut the manuscript.

## Verified facts behind this steer

- Thread "Draft lean Malleus arXiv paper", started 2026-09-02 12:43 PDT in the main worktree, still active at 20:03 PDT.
- `paper-v4/`: 108 files, 8.8 MB of which 6.9 MB is the CC BY-NC-ND PDF. `private/paper-v4-ocr`: 20 MB, ignored.
- Suite: 121 passed under `.venv` on the second run. On the first run one test failed on the `IMPLEMENTATION_STATUS.md` drift; the thread patched it live between the two runs.
- No graph derived from the PDF exists and no query has been executed. The manuscript status line says the same.
