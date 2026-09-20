# Overlord resume, 2026-09-16: Claude Code holds the queue

## State at E-0501, read this block first

Ledger E-0400 to E-0501 and master 1.5.55 carry every ruling and result. A
fresh session resumes from here; nothing below this block is more current.

Where things stand:

- Paper one's candidate is GREEN on the current Core (E-0468): Section 3 on
  the connected Shop, 4.6 injected faults, the five graph-result reviews
  ratified by Luis. Appendix B's two chain digests were re-cut on ff1c6931
  (warehouse 32798a67, synthetic 15c7c1ef); manuscript f3165c9b, PDF 5c686da4,
  archive 62d5a63e, 17 pages; whole gate 659 plus 2, 184, 2,546, exit 0. The
  E-0400 precondition (a model-in-the-loop reconsideration result) is met and
  ratified (E-0455), so the paper may be written further; not yet done. Open:
  a human look at the rebuilt PDF page 17.
- Current Malleus is ON MAIN at ff1c6931 (E-0467; src unchanged since d5d014ba): the hardened Core
  (d867c3ab, E-0437) plus the capability declaration and public vocabularies
  (990a24ae, OVR-000463), check-contract re-binding across an additive
  ontology revision (merge 0becb693, OVR-000464), and the declaration row
  (140967b3, OVR-000465). Overseer head OVR-000466 0eb70a73 (466 the Small Shop successor evidence
  generation forced by the revision policy identity moving, E-0464, E-0466,
  E-0467). Sealing on main:
  scratchpad seal_ovr_main.py <entry> <previous> <handover with the draft
  block>; a durable copy belongs beside private/shop-progressive-01/tools/
  seal_ovr.py. The three frozen Shop evidence tests and the connected chain are green
  again (small_shop 371). Nothing pushed. The paper tree's uncommitted edits remain.
- Experiment runtime: private/shop-progressive-01/runtime, an export of e7937b89
  plus the Shop tree from main 18015352 plus S1; runtime-c78b6b38 and
  runtime-25f94cbf kept beside it; RUNTIME.md and S1-BASELINE.md in each. On
  the current one: S1 32 passed with all eleven evidence files byte-identical to
  the 25f94cbf bytes; D0 140 passed (the Shop rule layer installed on stage A,
  E-0427); content_rules 18; fault-injection-01 30.
- Sealing procedure for further Core governance entries: the agent drafts the
  JSON block in the candidate's handover/2026-09-16-core-gate-hardening.md;
  the Overlord runs private/shop-progressive-01/tools/seal_ovr.py <ENTRY> <PREVIOUS>
  (Core's own tool does hash, render, check; schema validated first; commits by
  explicit path). The auto-mode classifier blocks this; Luis exits auto mode or
  runs it himself. why is capped at 1,200 characters; commit refs full hashes.
- The content rules on the document path failed gate 1 (E-0426, E-0428):
  VALUE_IN_CITED_TEXT refused 216 of 236 honest run-23 records, the conflict
  rule 2, the empty-record rule 0. RCA at E-0430, Luis's rulings there: the
  acceptance criterion for a rule is now "every refusal explained, rule
  defects at zero" (zero refusals only on dimensions the review verified);
  rules are chosen by a read-only census first; the per-slot source relation
  (copied, tallied, authored) is a Core requirement; the suspected citation
  slips in run-23 are learning, not paper narrative; the learnings are in
  .claude/skills/malleus-dev/SKILL.md "Choose an adopter rule" with a pointer
  from malleus-acolyte. The naive rule is dropped; gate 2 is skipped; the Shop
  stage-A rules are unaffected (zero refusals at C1).
- SHOP RECONSIDERATION EXPERIMENT, SECOND HALF COMPLETE (E-0451): the fresh
  session reviewed all three obligations once: distinct-occurrences NO_CHANGE
  with reason; order-relationship-and-delay CORRECTION (shared-customer and
  payment-delay claims bound to the passages, two CUSTOMER_ORDER and one
  DELAY_ORDER relation); shipment-eligibility CORRECTION (shipment-rule claim,
  RULE_CUSTOMER_SCOPE, DELAY_PAYMENT, DELAY_INVOICE); both SATISFIED on both
  Shop rules; gaps TYPE_ABSENT and RELATION_ABSENT declared; export 26f9a842
  (26 entities, 21 events, 62 participations, 7 relations); history 38 events,
  4 change sets, receipt 664d8336. Archived FIRST at
  producer/stage-b/archive/2026-09-17T14:37:05Z (9 files). VERIFIED from the archive (E-0452): every count
  confirmed, first 22 history lines byte-identical to stage A's. The
  review-coverage checker REFUSES the producer's reviews as written on one
  field (boundary_identity carries the boundary id, the packet never gave the
  digest; packet defect) and ACCEPTS complete with that field corrected by the
  evaluator (diagnostic only, not the producer's record). ASSESSED (E-0453): the fresh
  Opus 5 assessor's review-record.json (d35ab5a9) counts correctly changed 2,
  correctly preserved 1, missed 0, spurious 0, PRELIMINARY_COMPLETE; two
  residuals on shipment-eligibility (open_issue null under a CORRECTION token;
  RULE_CUSTOMER_SCOPE narrower than the general rule); the coverage-checker
  defect moves no count. RATIFIED by Luis (E-0455, "1 ratified"), bound at
  paper-v4/evaluation-v4/author-ratification-2026-09-17-shop-staged-review.md.
  The E-0400 precondition is met on the Shop. Open for Luis: the result
  stands as preliminary with the checker defect stated (clean checker
  demonstration from the next case on the fixed procedure), or stage B is
  re-run on a corrected packet.
- Stage A (E-0438 to E-0442, E-0449): finished PARTIAL, verified, destroyed by
  a test fixture, recovered byte for byte from the producer transcript
  (recovery/stage-a/RECOVERY.md), archived at
  producer/stage-a/archive/2026-09-17T04:48:13Z; Luis ruled the
  reconstruction stands; the workspace IS restored (E-0450, 11 of 11 inputs
  match the receipt). Core findings written for the Core session at
  handover/2026-09-17-core-findings-from-the-paper-front.md. Owed after stage
  B reports: run d0/tests/test_history_handoff.py (written, unrun) and
  regenerate D0-MANIFEST.json (two stale entries, nine unindexed files).
- New skill .claude/skills/malleus-paper/SKILL.md (E-0431): the paper as a
  moving front of the project's progress, and every paper directive Luis
  repeats. Read it with malleus-dev on any paper work. Luis speaks in explicit
  names, no codenames or stage letters.
- Rule census done (E-0432), Luis picked (E-0439), rules ADOPTED (E-0445):
  paper-v4/experiment-v4/content-rules-doc-02 holds the four rules as a Prolog
  PolicyProgram on run-23's path (Prolog is Core's only admissible check; the
  formula slots and qualifier lists are declared in rules.pl because
  logic.yaml's fields are closed). Gate 1: honest run-23 admits, 0 refusals,
  rule defects 0, export byte-identical. Gate 2: 55 faults, structural gate
  alone 45 refused 10 admitted, plus the four rules 53 and 2; the two still
  admitted swap quantity_kind, a producer-wording string no rule reads (the
  per-slot source relation, ROADMAP E3). Three-layer table for the paper:
  35/20 at c95dba7b, 45/10 hardened, 53/2 with rules. Registration under the
  e7937b89 pin dispatched to the gate agent.
- THE PAPER GATE IS GREEN (E-0448) on main d867c3ab: 160878cf partition 659
  passed plus 2 subtests; e7937b89 partition 184 (rule-census-01 106,
  content-rules-doc-01 22, content-rules-doc-02 56); unpinned 2,546; exit 0;
  3,389 tests plus two subtests. Every pinned group imports its export in
  process (poisoned-Core test), exports carry src/malleus and ontology, pinned
  cells are collected once, the three hardened-Core cells bind Core by a
  package-byte digest (52 tracked modules d57f3cc9), QA.md's gate paragraph
  states this run and its command. Luis's E-0436 rulings stand: Core is not
  frozen for its own sake; the hardened branch is merged (E-0437).
- NORTH STAR (E-0457): Luis: population must be able to grow the ontology as a
  recorded act; a source can carry evidence, rules and ontology at once; Core's
  unused capabilities in consumers is "plainly wrong". Running: (1) the
  capability audit agent (inventory, consumer survey, CAPABILITIES.md in the
  skills with Luis's use-in-full rule, public accessors for hidden
  vocabularies); (2) CENSUS DONE (E-0458): Core records the additive revision (two
  ADD_CLASS, TOTAL receipt) and the graph replays byte-identical, but the rule
  layer cannot follow: re-pinning the rules to the new ontology changes the
  normative profile and the revision refuses INCOMPATIBLE_CONTRACT; keeping the
  old pin makes every later admission refuse RULE_CHECK_FAILED. Missing Core
  capability: policy re-binding across an additive revision (reproducer at
  private/shop-progressive-01/census/revision-01/tools/test_census.py). Luis
  RULED (E-0459): build it in Core now. A Core agent works in a worktree on
  branch codex/policy-rebinding-across-revision from d867c3ab (RED before
  GREEN, docs, OVR-000463 drafted for the Overlord's seal). Then: merge, seal,
  re-export private/shop-progressive-01/runtime, add to CAPABILITIES.md, rerun
  the census, then build step 3 (gap declared by the producer, recorded
  revision, re-review under a new boundary). WAIT for the agent; nothing else
  starts on the Shop meanwhile.
- (E-0469, E-0470) THE ORDER-B CORRECTION CASE (stage C) IS BUILT AND
  VERIFIED, NOT LAUNCHED. Luis ruled (E-0469): five obligations in the third
  boundary; the correction-explanation class by recorded additive revision with
  Luis the named decider; protocol v3.4 with the ratification clause before
  this case's assessment; no re-run of the second half. Built (E-0470): the
  recorded revision producer/stage-c/revision-receipt.json (revision d2176cc2,
  ADD_CLASS OrderCorrectionClaim, ADD_CLASS CorrectsState,
  REBIND_CHECK_CONTRACT; contract af74ca2a to 2291b57b, required check
  83816c3a to 1bf386c3, history 07496a10 to 1e9c1e91, 41 events, graph
  byte-identical to stage B's export 26f9a842, re-pinned contract retained);
  third boundary db3dc7d0 over knowledge a13be43c, obligations
  distinct-occurrences 6, order-relationship-and-delay 5,
  shipment-eligibility 7, supplier-order-quantity-correction 7,
  inventory-unit-identity 22; packet intro-5-mistake, exposure CLEAN;
  assessment/review-protocol-v3.4.json c2933d97 (RED kept: v3.3 accepts a
  self-asserted ratification); dry run ALREADY_PRESENT_AND_REVISED, 13 inputs.
  Overlord verified: both archives match ARCHIVE.json, ratified record
  d35ab5a9 unchanged, nothing staged, src/malleus untouched. TWO PACKET
  DEFECTS FIXED (E-0471), RED before GREEN: the stage-C isolation message is
  now stage C's (spawn_message raises on an unknown stage); exports keyed by
  stage, stage C to work/stage-c-export.json. Rebuilt from the fixed builder,
  every revision identity reproduced; PROCEDURE.md 0139ddd3, spawn-message.md
  ed346939, dispatch 57ff495c. Overlord's suite run: 308 passed. THIRD
  FINDING, not corrected: producer/stage-a/PROCEDURE.md (06b97a3d) diverges
  from the text stage A's producer was given (9bab3603, three agreeing
  copies) by the added "Declaring a gap" section, overwritten by the
  2026-09-17 rebuild; pinned in d0/tests/test_stage_c.py. LUIS RULED (E-0472): protocol v3.4 wholesale, "lets start clean all
  the time" (done: one GOVERNING protocol in d0/assessment.py, per-stage rule
  deleted, containment for A, B, C against v3.4; his ratification of the
  second half written in v3.4's form as
  assessment/stage-b-packet/review-record-ratified.json 541130a4 beside the
  untouched record d35ab5a9, judgements equal); and "ok, go" on restoring
  producer/stage-a/PROCEDURE.md from the dispatched text 9bab3603 (DONE,
  E-0473: harness, workspace and recovery copies all 9bab3603; the dispatched
  stage-A text carries none of the six gap kinds; suite 322, Overlord's run). SUPERSESSION CLAUSE DONE (E-0474, Luis: "sounds good"): v3.4 now
  d01538fb, names v3.3 dddcc098 as superseded; validator accepts a record
  bound to either; archived record VALID/PENDING and ratified form
  VALID/RATIFIED under v3.4, neither edited; stage C run contract c922b229
  binds d01538fb; dispatch 57ff495c unchanged. Suite 327 (Overlord's run).
  STAGE C COMPLETE AND ARCHIVED FIRST (E-0475 launch 2026-09-19T01:12:08Z,
  E-0476): producer/stage-c/archive/2026-09-19T01:12:08Z (11 files). Five
  reviews: supplier-order-quantity-correction CORRECTION (OrderCorrectionClaim
  + CorrectsState to the e7 state, change eb6a47f8, SATISFIED both rules),
  four NO_CHANGE with reasons; gap RELATION_ABSENT; export a175da0b (27
  entities, 8 relations); history 50 events, first 41 = handed-off 1e9c1e91;
  packet anchored as source:stage-c-context after SOURCE_ALREADY_ANCHORED on
  the procedure's command (packet-naming defect, live). Overlord verified
  archive, prefix, packet digest, five boundary identities db3dc7d0. VERIFIED (E-0477): replay byte-identical on runtime-d5d014ba, admission
  SATISFIED against the re-bound contract 1bf386c3, COVERAGE CERTIFICATE
  COMPLETE over the five reviews as written (1 pending correction, 4
  unchanged; producer/stage-c/review-coverage.json); anchoring refusal = a
  packet-naming defect (source id by file stem), cannot reach the
  certificate, xfail pinned for the next build; status.json lacks a status
  token ("as before" instruction defect). ASSESSED (E-0478): assessment/stage-c-packet/review-record.json
  90723d8f, VALID under v3.4 d01538fb, correctly changed 1, correctly
  preserved 4, missed 0, spurious 0 over five obligations, PRELIMINARY,
  ratification PENDING actor:luis; three residuals (CorrectsState endpoint
  e7 vs e4; shipment limit stated by implication; printed times read as an
  ordering), none moving a count. RATIFIED BY LUIS (E-0479, "ratified", no judgement changed): binding file
  paper-v4/evaluation-v4/author-ratification-2026-09-18-shop-third-boundary.md
  ff172ee7; v3.4 form assessment/stage-c-packet/review-record-ratified.json
  c4d00110 validates RATIFIED, judgements equal the archived record. THE
  SHOP RECONSIDERATION EXPERIMENT HAS THREE RATIFIED-OR-CERTIFIED RESULTS on
  one growing history; the third boundary carries a complete coverage
  certificate. JOURNAL handover/2026-09-18-shop-reconsideration-journal.md 47496fdb and
  RCA handover/2026-09-18-shop-third-case-rca.md f9d8dcbd written (E-0481);
  ten skill learnings P-1 to P-10 proposed, unwritten. Luis: "2", cleanup first (E-0482). CLEANUP DONE (E-0483): protocol v3.5
  bec7c169 governs (supersedes v3.3, v3.4; all records validate unchanged);
  per-stage packet filenames; status shape in every procedure; lessons in
  both skills (uncommitted). Luis's delivery correction (E-0482): plain
  words, one decision at a time, talk before dispatching. Luis: "yes, start the Shop section" (E-0484). SECTION 3.2 WRITTEN (E-0485):
  manuscript-v4-working.md, Section 3 retitled, 3.1 connected story, 3.2 the
  model reconsideration; cell paper-v4/experiment-v4/shop-reconsideration-01
  under a third pin d5d014ba, 12 private outputs pinned in
  test_gate_integration.py; whole gate green 661+2, 184, 32, 2,547, exit 0.
  Luis read 3.2 and did not get it; the Overlord walked the supplier-order-B
  thread end to end with real data and every actor named (chat, 2026-09-19).
  LUIS RULED (E-0486): (1) next run's producer gets the acolyte skill,
  CAPABILITIES.md and an ontology purpose note; mapping and prose stay out;
  design the run to show the behaviour delta (same evidence and obligations
  on a copy of the history, only the packet changed); (2) compile-check-admit
  becomes ONE CORE OPERATION (ROADMAP F1): Luis "go on both" (E-0488); a Core
  agent is BUILDING it in an isolated worktree from ff1c6931, RED first; the
  Overlord merges and seals (seal_ovr_main.py, previous OVR-000466); BLOCKING
  any model run until landed; then re-export the Shop runtime, bump pins,
  re-baseline, migrate the Shop runner template to the new call (D0 agent).
  (3) rules research DONE (E-0487, handover/2026-09-19-rules-inside-the-
  ontology-findings.md 88c9e30a): Option B adopted as design constraint
  RULE_DECLARES_ITS_READS, sequenced after F1; Option D excluded; Option C
  target. "## Rules and the ontology" IS IN .claude/skills/malleus-dev/SKILL.md
  (E-0489, 92 lines, guard tests green, uncommitted). SKILL REVIEW (E-0490, E-0491): handover/2026-09-19-malleus-dev-skill-review.md
  5fa9050b, 32 entries, proposals only; Luis "apply all seven now please",
  the seven must-fix applied (543 guards green); Luis "apply all of them
  please" on the fifteen should-fix and seven could-fix: ALL APPLIED (E-0492,
  malleus-dev 540 lines, malleus-paper, malleus-acolyte step 9, openai.yaml;
  543 guards green, Overlord's run). Open for Luis: the skill's tuple block
  says "Implementation conformsTo ConformanceSuite" and the design graph has
  no conformsTo predicate. Skills uncommitted with the paper tree. F1 LANDED
  (E-0493): main fast-forwarded ff1c6931 to a68d11c9 (five Core commits,
  check_and_admit_population_plan; RED/GREEN reproduced by the Overlord).
  SEALED (E-0494): skills+ROADMAP committed 3b8d49f4; OVR-000467 (skills in
  sync) and OVR-000468 (F1) sealed in one render, commit d89a0c47, head
  OVR-000468 ac90aecc. Main is d89a0c47; src unchanged since a68d11c9. RULE:
  the three skills and ROADMAP.md are GOVERNED documents; any edit blocks the
  next seal until recorded, so batch skill edits with a governed change
  (two one-word statements already stale: "overseer entry to follow" in the
  skill, "Overseer entry pending" in ROADMAP F1). 17 pre-existing failures on
  main = stale reader digest (ROADMAP F6), not F1's. Two-entry seal script:
  scratchpad seal_two.py (durable copy owed). NEXT, ruled: re-export Shop
  runtime onto the new Core; bump paper pins, re-baseline; migrate Shop runner
  to check_and_admit_population_plan (D0 agent); no model run before that.
  Luis (E-0494 follow-up): "migration first, check and evaluate". D0 AGENT
  DISPATCHED 2026-09-19 for: fifth runtime export runtime-d89a0c47, d0/paths.py
  RUNTIME advanced, d0/runner.py admit path replaced by the one call (old path
  deleted, PrologVerifier import gone), RED tests: dead old path, parity on a
  COPY of the stage-C ledger against export a175da0b, CHECK refusal with the
  ledger unchanged; D0 baseline 348. MIGRATION DONE AND VERIFIED (E-0495):
  runtime-d89a0c47 exported (src tree 26df761f), d0 pin moved, runner 635
  lines with one Core call, parity byte-identical on the stage-C admission
  (history 10dfda4e, export a175da0b), CHECK refusal leaves the ledger
  byte-identical (old runner orphaned two anchors), D0 363. Launched
  workspaces untouched. LUIS RULED (E-0496): move all three pins to d89a0c47
  and re-baseline; PAPER-GATE AGENT DISPATCHED 2026-09-19 (manifest core_pins,
  fingerprints old/new/why, Appendix B digests re-cut, whole gate green,
  candidate rebuilt; STOP on any domain artifact not byte-identical). DONE
  IN PART (E-0497): rule cells and Shop cell pinned to d89a0c47 (53 modules,
  digest 34019613), no domain artifact moved, Appendix B digests stand (five
  producer files unchanged), agent's whole gate 661+2, 184, 32, 2,547 exit 0.
  STOP 1: answer-demonstration pin stays 160878cf (frozen run manifests bind
  it; the hardened Core refuses one population, SOURCE_BINDING_REQUIRED).
  STOP 2: candidate will not rebuild, two overfull headers in the 3.2
  boundary table; abstract, 5 and 7 still predate 3.2. Overlord's own gate
  run pending. LUIS RULED (E-0498) "lets fix before paper", "all in
  sequence": FIX 1 DONE (E-0499): three stale measurements re-recorded by
  tool, four test files into testpaths, merged, OVR-000469 sealed; skill and
  ROADMAP statements current, OVR-000470 sealed; main 8933892e, head 470
  c57f0f68. Findings for Luis: research pack re-declares Claim/Evidence
  (CC-D02); CI portability of the re-admitted tests unobserved. Full suite
  on 8933892e: 3735 passed, 0 failed. FIX 2 DONE (E-0500): declared source id
  (PACKET_SOURCE_ID, --source-id on the anchor line, SOURCE_ID_REQUIRED and
  MALFORMED_SOURCE_ID, source_id_for deleted), D0 378, launched untouched.
  FIX 3 STOPPED BEFORE BUILDING (E-0501): the one-call operation can serve
  none of the four live research consumers (three checks are not Prolog and
  use a private grammar with an executor Core never reads; two policies
  require two checks; the machine's CheckRecord has seven fields, the
  operation emits six) and Core's own history tests admit 16 times through
  the public door. DECISION PENDING with Luis: C (close where Core can
  reproduce the check + fill CHECK_RECORDED from the machine's field set) now
  and D (Core runs the declared executor itself) as roadmap, or D now.
  ALSO FOUND: paper-v4/test_shop_connected_calibration.py, research small_shop
  content_rules/, and the two paper-side consumers are UNTRACKED (uncommitted
  work); src/malleus/session.py and five tests/ modules are gitignored by
  design (Assent path), so a clean worktree's suite is 3626 at 8933892e and
  the checkout's is 3735: brief Core agents with the worktree number. The
  commit pass is overdue. FIX 2 was: declared source id in the Shop
  runner (D0 agent, addendum 18 proposal); FIX 3 close Core's two-step door
  (Core refuses caller-supplied CHECK_RECORDED/VERDICT_RECORDED under an
  installed policy; every two-step consumer migrates to the one call in the
  same change: research small_shop correction/content_rules/shipment_policy/
  showcase run.py, methodology_gedanken_e2e/drivers/common.py, paper-v4
  content-rules-doc-01/run_policy.py and content-rules-doc-02/admit.py, and
  Core's own session.py; the connected-chain cell runs on the checkout's Core,
  so Appendix B depends on those research runs migrating). THEN the paper
  task (3.2 table, abstract, 5, 7, rebuild) and the commit pass.
  Then: fourth-round design (informed producer, behaviour delta; open
  question: should the producer write Core's plan grammar directly, E-0496),
  Customer class by recorded revision, declared source id, Core's two-step
  door. The F1 Core agent was
  cut off by a session limit before any change and RESUMED (E-0489) in
  worktree .claude/worktrees/agent-a4dd80e0cc93acb75; (4) ROADMAP F2 gap-as-trigger, F3
  revision impact analysis, F5 automatic rule re-binding. The customer
  TYPE_ABSENT gap from round two is still unaddressed; Luis leans to adding a
  Customer class by recorded revision at the next boundary. PAPER: 3.2 stands;
  abstract, Sections 5 and 7 and the candidate PDF still predate it; the
  worked example for 3.2 is proposed; commit pass for the paper tree still
  owed. the binding file. Open, moot for this case: v3.4 note says three
  obligations (re-word for the next case). The launched workspace
  producer/workspace-stage-c is not to be touched. Launch command
  after his go: cd private/shop-progressive-01 &&
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m d0.launch
  --stage C; dispatch the printed prompt verbatim to one fresh Opus 5 session;
  archive first when it reports (python -m d0.archive --stage C).
- (E-0454) The assessor's record validates (VALID); the D0
  suite is 240 green; the index is re-derived by d0/index.py (98 artifacts);
  the boundary-identity handoff is fixed for the next stage (obligations file
  carries the digest beside the boundary; the archived stage-B packet
  unchanged). Two things wait on Luis: ratification of
  assessment/stage-b-packet/review-record.json, and the checker-defect ruling
  (stands as preliminary with the defect stated, or re-run stage B). A test overwrote a declared input of the launched stage-B
  workspace; the Overlord restored it from the archive (E-0452).
- Then: the adopted rules' gate 1 and gate 2 results come to Luis; Luis's go
  for the second fresh session; the second half of the Shop experiment as a second
  fresh session; a fresh Opus 5 assessor; Luis
  ratifies. Then the order-B correction case (D3), then the PDF stage with the
  CC BY preprint as earlier state. B (reattribution as a slot) held until D
  passes.
- Open for Luis: D0's decisions 2, 5, 6 in private/shop-progressive-01/D0-REPORT.md
  (runner resolves Core's bundled packs; protocol v3.3 location; unused limits
  key); decision 1, the runner filling the binding fields, was confirmed with
  the go;
  whether he read the baseline and reuse reviews; S1 onto main; commit of
  everything since 2026-09-12 (explicit paths only, another session commits to
  this repository); the acolyte skill's one-line profile qualifier for
  LOCATOR_NOT_DERIVED (E-0422); gate registration of bridge-01,
  fault-injection-02 and content-rules-doc-01 in active-test-manifest.json with
  their private dirs pinned (E-0429); whether fault-injection-01's RESULTS.md
  notes that the coordinate is now an argument.

Read this first in a fresh Claude Code or Codex session. It is the current
execution queue and its gates. The Codex Overlord's prior queue is
[2026-09-15-overlord-resume.md](2026-09-15-overlord-resume.md), now historical.
Decisions and results of the day are in the paper ledger E-0400 to E-0405 and
the master plan directive 1.5.48. Decisions come to Luis in chat; this file is
the archive.

## Scope ruled by Luis

Paper one reports the Shop and the PDF only. Robotics and the beyond-context
stratum are out of paper one. The paper is not written until a model-in-the-loop
reconsideration result exists: new evidence arrives, the right earlier records
are reconsidered, what still holds is kept and recorded as reviewed, what changed
is admitted through the gate with its reason, and a fresh reader can see it.
Shop first, then the PDF. The two finished results (connected Shop story, fault
injection) are bound into the manuscript now so they stay frozen.

## Gated sequence, rulings A to E

| Step | What | Gate | State |
| :--- | :--- | :--- | :--- |
| A | Experiment runtime: Core pinned at 25f94cbf (review-coverage checker, nine commits on main HEAD 18015352), exported to private/shop-progressive-01/runtime with the Shop tree from main and S1 from the Codex clone | Checker's 154-test selector passes; connected chain reproduces main's three receipts or differs only in version strings; S1's 28 tests and ten artifacts reproduce; checker example runs | Dispatched |
| B | Reattribution as a slot on the record (same-type replacement), Core withdraw-and-link only on a failing case | A compiled schema fragment and a synthetic test where own-measurement becomes cited-value as a same-type supersession that a reader distinguishes | Held until D's Shop gate |
| C1 | Three content rules as adopter PolicyProgram with Prolog check on the Shop path: value in cited text (whitespace and case only), same-subject same-quantity conflict, empty record refused | RED per rule, GREEN, honest Table 1 admits with zero refusals and identical domain records; a false positive is a STOP | Dispatched |
| C2 | Same rules on the document path under c95dba7b; honest run-23 false-positive count reported first; then the twenty admitted faults rerun | New outcome table; false positives brought to Luis before any tuning | Not yet authorised |
| D0 | Preparation for the Shop stage-B model run: runtime from A, frozen packets and obligations with hashes, exposure checks over schema, helpers, prompts; S1's four residuals fixed under TDD; assessment protocol v3.3 with four counts | Report to Luis; the model run needs its own go | Waits on A |
| D1 | Stage A: fresh Opus 5 producer populates the Table 1 packet against the Shop ontology; admitted; replayed; the three interpretation subjects declared as review obligations over its actual records | Admission and replay receipts; obligations frozen | After D0 go |
| D2 | Stage B: the producer receives the three context passages, its own graph and the obligations; proposes change, no change with reason, conflict or unknown per obligation through the gate; checker refuses completion on missing or stale review; independent assessment against the chapter's prose | Counts: correctly changed, correctly preserved, missed, spurious; both stages replay | After D1 |
| D3 | Second Shop case: the chapter's own correction of order B (quantity 1 at e4, 2 at e7, prose explaining the mistake) | Same counts | Only if D2 passes |
| PDF | The CC BY 4.0 preprint (Research Square, doi:10.21203/rs.3.rs-1945608/v1, 8,546 words) as earlier state by one fresh capture; the published text as later evidence; no-source contamination control; peer review file evaluator-only | Same counts against the four source-documented changes | Only after the Shop stage passes |
| E | Bind Section 3 and Appendix B (draft at paper-v4/drafts/section-3-connected-story.md, Luis's five choices), a fault-injection subsection after 4.5, one abstract sentence each, Section 7 measurement; manifest, access map, rebuild, whole paper gate, QA.md | All tests green, PDF built and inspected, leak check clean | Dispatched |

## What was established today, with pointers

- S2 assessment of S1: five of five PASS, ten artifacts reproduced byte for
  byte; four unreported residuals; two Core findings (research pack accepted by
  compiler and refused by inspector; the Codex Shop branch and main hold
  opposite positions on the empty-list rule). E-0401.
- fault-injection-01: 55 faults, 35 refused, 20 admitted (5 exposed, 15
  invisible), structural gate alone. Three Core findings with reproducers.
  paper-v4/experiment-v4/fault-injection-01/RESULTS.md. E-0402.
- Section 3 draft with every receipt reproduced from HEAD; the connected path's
  refusal is a transition-rule refusal; one false sentence caught. E-0403.
- Paper-two recon: the article's own CC BY preprint with four documented
  changes; sixteen verified references; measurement space empty.
  research/paper-two-recon-2026-09-16.md. E-0404.

## Open for Luis

1. Ratification: settled. Luis read all five later graph-result review
   records in full; the manuscript says so, bound to their digests in
   paper-v4/evaluation-v4/author-ratification-2026-09-16.md (E-0413). Still
   open: whether he also read the baseline-01 and reuse-01 assessments, which
   the paper still names as not ratified.
2. S1 onto main. The session's permission gate refused copying the Codex
   clone's S1 directory into the shared checkout. S1 lives in the clone at
   /private/tmp/shop-combined-showcase.NMFkTZ/repo (uncommitted) and in the
   recovery bundle under ~/.codex/visualizations/2026/09/08/01a08375-.../shop-recovery/2026-09-15/S1/,
   and after step A in the experiment runtime export. Committing it to main is
   Luis's call.
3. Commit. Nothing from 2026-09-12 onward is committed. Stage explicit paths
   only; another session commits to this repository. The paper's do-not-stage
   list is in the 2026-09-12 handover and still applies; add private/ and the
   Codex clone.

## Core items to hand to the Core session, not to fix here

- Empty record with no source and no properties is admitted (fault-injection gn).
- Cited locator never compared with derivation locators (fault-injection b2).
- Digest binding opt-in; 236 of 440 run-23 records covered.
- Research pack ResearchRelation: compiler accepts, inspector refuses.
- Empty-list required-field rule: branch and main disagree; Luis's open
  contract decision from the 2026-09-14 sync.
- Conflict outcome: if the policy grammar can only refuse or admit, "admit and
  record the conflict" needs a Core decision (C1 will report).
- A typed refusal leaves a ledger event: runner.admit registers the plan
  artifact inside prepare_population_change before NO_DOMAIN_CHANGE is raised,
  and the runner's PARTIAL_EFFECT guard skips the RunnerRefusal path (E-0441;
  deterministic nine-line reproducer with the recovery agent's record).
- Per-slot source relation (E-0430, Luis agreed): the compiled ontology must be
  able to say whether a slot's value is copied from the source, tallied from it
  or authored by the producer; without it no value-in-source rule is
  specifiable and every such rule is an adapter.

## Rules that still bind

Every agent reads .claude/skills/malleus-dev/ first. RED before GREEN. No
staging, commit, stash, reset or delete in any checkout. Nothing under
src/malleus edited by paper or Shop work. Frozen Core for paper one's seven
populations stays c95dba7b; the growth experiment runs on 25f94cbf and the paper
states both pins. Nothing sharing a 60-character normalised run with the marine
reading leaves private/. The paper ledger and master plan are written only by
the Overlord. A failed gate returns to Luis in chat; it is not worked around.
