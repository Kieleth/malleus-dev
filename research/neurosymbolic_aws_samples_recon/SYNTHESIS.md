# Synthesis: four aws-samples neurosymbolic repos vs the autoresearch-et thesis

Date: 2026-08-19. Target: `target:autoresearch-et-thesis` (recon-event:000001).
Sources: five Opus subagent inspections, raw findings in `intake/`. Every claim
below carries a basis mark in the intake files; this document interprets, it
does not add evidence.

## Declared claim and verdict on the falsifier

Claim: the autoresearch-et thesis (typed bitemporal KG as reasoning medium +
telemetry-gated meta-agents) is distinct from but adjacent to the neurosymbolic
verification line in these four repos.

Falsifier declared before search: one of the four already persists a typed,
temporally-versioned search/research trajectory queryable at
prompt-construction time.

Verdict: NOT triggered. None of the four persists any state across runs.
The SQL planner's negative memory resets every iteration; the kinetics agent
mints a fresh uuid per run with no index; the DL framework versions code, not
knowledge; the clinical chatbot rebuilds its ten-fact theory from scratch on
every query. Novelty claim 1 of POSITIONING-2026-04-24 stands against these
works. Additionally, RELATED-WORK-2026-04-24.md contains zero coverage of the
neurosymbolic line (DL, theorem provers, symbolic planners, SMT): these four
repos and their genre are net-new related-work territory for the paper.

## What each repo actually is (code-verified, not README-verified)

1. **Kinetics research agent** (~2.9k LOC, sample). LLM selects a curated
   BioModels model and a pre-committed analysis protocol; kiro-cli writes
   COPASI simulation code; execution produces numbers and plots; multimodal
   LLM critique loops until an LLM classifier says done. The simulator is an
   evidence producer, not a verifier. "Provably correct" (README) is
   unsupported: every gate is an LLM verdict except exit-code/stderr.
   Loop closes over the artifact, never over the biology: no hypothesis
   object, no predicted-vs-observed, no comparison against data.

2. **DL framework** (~3.4k LOC, sample). Evolves a Python query program
   against gold Q&A using an LLM judge and kiro-cli as the mutation operator.
   Headline finding: NO DL reasoner is ever invoked. The symbolic operation is
   BFS over asserted subclass edges plus set intersection in SQLite. The
   harness rule "core reasoning must use owlready2" is prompt-stated,
   enforced by nothing, violated by all four shipped programs. Real
   contribution: the domain-blind program-evolution loop (0% -> 100% in 4
   iterations, $0.59, on 4 questions judged against hand-written prose).

3. **Clinical chatbot** (~3.1k LOC Python, sample). The most genuinely formal:
   cvc5 FOL entailment of one extracted formula against a hand-built theory,
   CWA as explicit axioms, three-valued unknowns (TFU), NaN for unknown
   numerics. Two structural gaps: the verdict is a LABEL, never a gate (the
   contradicted answer is still displayed, README concedes enforcement is
   future work), and the NL->FOL translation is a single unverified LLM call
   the whole guarantee is conditional on. The unsat core, the exact axioms
   that did the work, is computed on every UNSAT and discarded before the API.

4. **Text-to-SQL planner** (42.5k LOC, framework-scale, 723 tests). The
   strongest of the four. The LLM never emits SQL: question -> DRC formal
   intermediate -> LLM proposes RA operators under a forced tool-enum ->
   cvc5 proves logical equivalence to the target -> SQL derived
   deterministically from the proven tree. Typed rejected-proposal negative
   memory. Dual-signal BIRD evaluation (proof + execution) with the
   disagreement cells as the diagnostic. Caveats: "unsat or nothing" is
   contradicted by the indeterminate-fallback exit path (planner.py:513-531);
   "near-SOTA on BIRD" is claimed with zero numbers committed anywhere;
   everything is within-run, no cross-run learning.

## The cross-cutting pattern

All four are LLM-proposes / symbolic-disposes, but the symbolic layer sits in
four different places: answer source (DL), evidence producer (kinetics),
post-hoc label (clinical), generation-replacing prover-in-the-loop (SQL).
Only the SQL planner makes the formal verdict load-bearing; in the other three
the symbolic result is computed and then either narrated by an LLM or shown
next to an unmodified answer.

Second pattern: README-vs-code drift is systematic. "Provably correct" twice
without a proof object; "the LLM never sees the answer" contradicted by the
shipped program; "unsat or nothing" contradicted by the exit path; near-SOTA
with no number; specs and task lists marking tests done that do not exist;
CI that never runs (tests.tml, inert pytest.ini). Three of the four were
partly authored by a coding agent (kiro-cli) under a no-look-at-the-code
experiment, and these are exactly the defect classes that mode produces:
rule-in-prompt instead of mechanism-in-code, dead scaffolding, drifting docs.

Third pattern: zero persistence. The entire genre, as sampled here, is
amnesiac. That is the exact gap the autoresearch-et thesis occupies.

## Concept links to internal work

- Closed loop with judge (DL repo) <-> the autoresearch-et orchestrator loop.
  Difference: their stop criterion is an LLM verdict against prose; ours is
  measured telemetry plus typed PromotionDecision/AuditEvent records.
- Pre-committed analysis protocol (kinetics analysis-types.yaml) <->
  hypothesis.md pre-registration. Same instinct: commit the method before
  spending, judge fidelity to the committed protocol. They lack the
  falsification band and the hypothesis entity.
- Typed negative memory (SQL RejectedProposal) <-> ADR-005 dedup-on-failure.
  Theirs resets per iteration; ours persists as KG nodes with edges.
- Grounded audit trails (SQL SMT transcripts with lhs/rhs labels; kinetics
  report appendices) <-> the provenance invariant. Their trails are for human
  post-mortem; ours are queryable at prompt-construction time (when the
  channels work; see AUDIT-2026-05-06).
- Vocabulary gate on LLM output (clinical declared-function table; SQL forced
  tool enum) <-> malleus ontology-as-admission-gate. Their rejections are
  swallowed (exception -> 'unknown') or retried silently; malleus preserves
  typed rejections. The clinical repo's "computed but never enforced" verdict
  is the structural/epistemic separation malleus insists on, minus the policy
  layer that makes it a control.
- Explicit absence (TFU, NaN, CWA-as-axioms) <-> malleus explicit
  indeterminacy and crash-loud-on-missing. Genuinely well done there, then
  flattened one layer up.
- BIRD: direct benchmark overlap. EB02's diagnosed failure was early clause
  commitment before later constraints are visible. Their planner is a direct
  attack on exactly that failure: prove global equivalence of the whole
  query, never commit clause-by-clause. The honest comparison is mechanism
  vs mechanism, not score vs score (they publish no score; ours is a
  pre-registered null).

## Paper implications (for the operator to decide, not decided here)

1. RELATED-WORK gains a neurosymbolic-verification section; these four are
   citable exemplars of the "verdict without persistence" and "verdict without
   enforcement" quadrants. No published-paper survey was done in this pass
   (declared boundary); a follow-up recon could chase the academic line
   (LINC, CRANE, GCR are already in malleus paper.md's table).
2. Novelty claim 1 survives this sample. Claim language should still be
   scoped to "search/research trajectories" as POSITIONING already does.
3. The axis "does the symbolic verdict gate anything" (from the clinical
   finding) is a sharp discriminator the paper could adopt; autoresearch-et
   itself gates citation resolution but not semantic content, which is worth
   stating honestly.

## Instrument gap observed (malleus-recon relating to internal projects)

What worked with zero code: internal projects recorded as Works with path:
identifiers and local_path EvidenceAttachments; the ReviewTarget is the
internal thesis. What is missing: (a) a typed link from a recon Work/Claim to
another internal graph's identity (an ET node id, a malleus ledger record id),
today only expressible as a string in identifiers; (b) any discovery aid that
proposes which internal projects a new recon relates to; (c) an exporter that
projects recon records into ET so connections become queryable from where the
thinking happens. Options, cost-ordered: convention-only (now), recon.yaml
extension with a CorrespondsToRelation (small), recon->ET bridge exporter
(larger). Decision is the operator's.
