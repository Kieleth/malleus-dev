# Paper v4 steer, 2026-09-02

Author decisions taken by Luis in chat with the overseer session on the evening of 2026-09-02, after a read of the "Draft lean Malleus arXiv paper" thread, `paper-v4/`, `private/paper-v4-ocr`, and a run of the experiment suite (121 passed under `.venv`). They supersede plan decision D-0010 and the plan 0.2.0 evaluation choices they contradict. Record them in `paper-ledger.md` as D-0011 to D-0014 with source "Author decision via overseer session, 2026-09-02", bump the plan, and update the manuscript status line.

Four decisions are closed. One, D3, is open. Do not proceed on D3.

## D1 Reading layer: PDF text layer, not raster OCR

Decision: the selected reading is the PDF text layer, extracted by one declared tool at one pinned version and frozen by digest. The raster and Tesseract path leaves the paper. `malleus-ocr` leaves the paper path; one sentence in future work at most.

Why: the raster reading the model saw has `CO2` broken into `CO,` in 42 of 59 occurrences. The text layer has 74 `CO2` and zero `CO,`. Two of the four competency questions are about CO2. The OCR gate measured lineage and coverage, not transcription, so nothing caught it. Faithfulness to the OCR profile was never the ask.

What changes:

- New selected reading and block projection from the text layer. `pdftotext` 26.03.0 is on this host but is a system binary; a pip dependency such as `pypdf` is easier to capture in project configuration. Pick one, pin it, stop.
- Re-bind the sealed oracle locators to the new blocks. Evaluator-only step.
- Retire the OCR precommit, execution receipt, verification, bundle, alignment guard and their tests from the experiment. Keep the retained files under `private/` untouched. Do not delete, do not cite.
- Rendering, Tesseract and trained data leave the dependency set.

## D2 Ontology acceptance: the protocol's loop, not a hand repair

Decision: the ontology run is re-executed on the text-layer reading, since the refused run was built on corrupted text. Same task brief, same fresh-session rules, same one-shot adequacy review. If the review refuses, return its diagnostic (failed criteria plus witness rows) to the same session once, as a typed `DEFER`. The session supersedes its proposal. One more one-shot review. Then stop, whatever the outcome. Report both rounds.

The hand-authored recovery ontology (`controlled-ontology-recovery.yaml`, its precommit, compilation, review and receipt) is retired. Not deleted, not used, not cited as the paper's ontology. The Tesseract-era refused run is retained as history and gets at most one sentence in limitations.

Why: refusal with a diagnostic followed by supersession is what the Malleus protocol is for. Forbidding that loop and then editing the schema by hand, however many precommits wrap it, reads as post-hoc repair. Running the protocol's own loop is both leaner and on thesis.

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

## D3 OPEN: who writes the population

Who proposes the 15 entities and 20 relations that enter the graph? The author has not decided. Two options are on the table:

- (a) A fresh model session, given the selected ontology and the selected reading, proposes the facts with a block locator per value. Malleus compiles, refuses what is malformed, admits the rest, replays, and the four queries run. The exact-match score against the sealed oracle is the result, whatever it is.
- (b) Evaluator-authored population, as decided in the thread at 19:56 PDT.

Until the author decides: build nothing past the recipe library. Do not author population facts.

## Order

D5, then D1, then D2, then D3 once decided, then queries, then fill the result fields, then cut the manuscript.

## Verified facts behind this steer

- Thread "Draft lean Malleus arXiv paper", started 2026-09-02 12:43 PDT in the main worktree, still active at 20:03 PDT.
- `paper-v4/`: 108 files, 8.8 MB of which 6.9 MB is the CC BY-NC-ND PDF. `private/paper-v4-ocr`: 20 MB, ignored.
- Suite: 121 passed under `.venv` on the second run. On the first run one test failed on the `IMPLEMENTATION_STATUS.md` drift; the thread patched it live between the two runs.
- No graph derived from the PDF exists and no query has been executed. The manuscript status line says the same.
