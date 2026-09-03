# Paper stream: overseer review

Reviewed 2026-09-01 against `malleus-paper` @ `18b6b47` and `malleus-paper-dojo`
@ `eb3f0cd`. Both are worktrees of `malleus-dev`. No fix was applied; this is the
findings file. The paper is the one stream with no earlier handover.

## State

Stalled since 2026-08-16/17. One edit on 2026-08-26, eleven seconds, appending a
note to `THESIS_CANDIDATES.md` that release-grade environment work had become the
critical path before a working protocol demonstration existed. It changed no gate.

Thesis claim CP-007 has evidence state `FUTURE`. No claim is `AUTHOR_ACCEPTED`.
`MANUSCRIPT.md` is 338 bytes, blocked at gate G8. The governed half, claim ledger,
gates, byte-pinned freeze, withdrawn lost result, verified under adversarial
checking. Do not spend effort defending it.

## The 0.9.0 pin is deliberate and load-bearing

`RESEARCH_TOOLING_REFERENCE.json` pins execution to 0.9.0 at `93644f1` with
`core_migration_authorized: false`, enforced by `verify_handoff.py`. 0.9.0 was
never buggy: `FINGERPRINT_VERSION` was unconditional there; 0.11.0 made it
conditional and created the two regressions that 0.12.0 and 0.13.1 fixed.

Rebasing to v0.13.3 would be safe and pointless (cyp450, attack, malleus hashes
identical). Rebasing to current main would break the pilot: the 2026-08-20 root
promotion of `locator`, `statement`, `reviewer_id` moved cyp450 and attack hashes
with their bytes unchanged, `verifies()` returns False, and the migration receipt
covers only recon. B3's reopen condition (protocol, API, fingerprint, replay all
changed) is met and nobody has reopened it. Fine while parked; negligence the day
someone rebases.

## Risks, most severe first

1. **`paper.md:630` asserts a pre-registration tag `prereg-v1` that does not exist**
   in any repository. Verified: eight tags, all version releases. For a paper
   whose method rests on pre-registration this is the one checkable falsehood.
   Create the tag before any run, or delete the sentence.
2. **A second, ungoverned paper.** `malleus-dev/paper/paper.md`, 59 KB, gitignored,
   different thesis ("Can Ontology-Typed State Transitions Improve Multi-Turn LLM
   Reasoning Coherence?"), edited three days after the freeze, invisible to the
   claim ledger that says it controls the paper. It is the file that looks
   finished and would go out in a hurry.
3. **The measured harness does not exercise malleus.** No ledger, staging or
   assent in the measured path (`paper.md:594-624`, already flagged in
   `handover/2026-08-20-paper.md`, unfixed). Every breaking change since 0.9.0
   sits in modules the harness never touches.
4. **Six of nine harness modules are gitignored** (`.gitignore:39-49`) against a
   promise to open-source all materials. Nothing to release without first
   tracking them.
5. **A firstness claim the estate's own rule forbids.** `paper.md:430` claims no
   analogue in any surveyed system; the dojo's 84-work audit concludes "a bounded
   search result, not a firstness claim."
6. **No citation is byte-verified.** `evidence_ledger.csv` carries no digest,
   no retrieved bytes. Known instance of the failure class: `llm_prep_readiness_recon`
   exists because a design note cited two findings to a file that contains
   neither.
7. 80% of the literature KG is abstract-only, and `T1_CLOSEST_WORK_AUDIT.md`
   asserts section-level inspection for three works whose only KG evidence row is
   the abstract.
8. `§9` implementation table is an April snapshot; `kg.py` row never matched any
   state the file has had.
9. CP-005 and charter boundary 6 say malleus has no governed schema change; true of
   0.9.0, false of the shipped library since `c410f11`.

## Prior art the dojo already found

S2CRA (`paper:openreview:RdfaKpspV5`) resolved `OCCUPIES` at whole-paper level
from the full PDF. Behind it: PVD, "Rethinking LLM Verification", ANNEAL, SkillDAG,
and historically Clark and McCabe 2007. The residual is whether the malleus layer
beats ontology-retrieval-alone under matched budget, plus a replay-completeness
invariant. With no dataset selected and G4 blocked, that residual is unoccupied,
not yet testable.

## Recon projects

Thirteen under `research/`, eleven with ledgers, ~8,000 events. Three reached
tracked code or the roadmap (migration, cost-aware, semantic-log). Three are
orphans (`ontology_change_rules_recon`, `ontology_extension_upstream_recon`,
`git_object_model_recon`). None feeds the paper; the dojo excludes them by design.

## Decision the artifacts cannot make

Two theses exist (`paper.md` multi-turn coherence; CP-007 selective risk at
coverage) and a third framing was proposed 08-26. Nothing states their
relationship. That is the owner's call and it precedes any other work here.
