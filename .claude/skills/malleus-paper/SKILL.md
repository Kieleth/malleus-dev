---
name: malleus-paper
description: The paper front of the Malleus project. Use for any work under paper-v4 or a private paper cell, for experiment cells, the manuscript, the paper gate, the paper ledger and master plan, model runs and their assessment, and for deciding what a result means for the paper. Complementary to malleus-dev (the library) and malleus-acolyte (an adopter).
---

# The Malleus paper front

Read `.claude/skills/malleus-dev/SKILL.md` first; its rules bind here,
including "Rules and the ontology" and "Choose an adopter rule". Then read
`paper-v4/AGENTS.md`, the governing directive at the top of
`paper-v4/paper-master-plan.md`, the resume handover it names, and the last
entries of `paper-v4/paper-ledger.md`.
Historical entries and handovers are evidence, not current authorization.

## What Core can do

`.claude/skills/malleus-dev/references/CAPABILITIES.md` declares every shipped
Malleus capability with its public entry point and its status. A cell, a runner,
a launch packet or a producer procedure that meets a limitation reads that
declaration and uses the capability in full **before declaring a gap**, writing
adopter code, or working around it. A gap is declared only when the declaration
says the capability does not exist, and then it is filed as a Core requirement
and goes to the Core session with a pinned reproducer.

Luis, 2026-09-17: "That core has capabilities we're not using in shop is just
plainly wrong, we work on core so that we can use them." A procedure is not
allowed to be silent about a capability a producer needs: the permitted gap
kinds and a checker's boundary identity both reached a launched producer only
after the run (E-0438, E-0452).

## What the paper is

The paper is a moving front of the project's progress, not its history.
Malleus advances as a protocol; when a result arrives, Luis decides what enters
the paper and what stays out. The paper presents the best results reached
within the time and the goals, and a reader can check every one of them.

Luis, 2026-09-11: "I do not want the paper to be a 'historical' paper where we
relate our failures, I want the paper to be, here, here are the results of how
it works, check them out yourself." Luis, 2026-09-16: "this is not a historical
we did this and this and this paper, we're presenting as best results as we
can arrive in our limited time and goals."

Consequences:

1. Advance Malleus first; write the paper when results support it. A failed
   measurement is learning: it enters the ledger and the skills, not the
   paper's narrative.
2. Paper one reports the Shop and the PDF only. It is not written further
   until a model-in-the-loop reconsideration result exists: new evidence
   arrives, the right earlier records are reconsidered, what holds is kept and
   recorded as reviewed, what changed is admitted with its reason, and a fresh
   reader can see it. Luis: "this is core to malleus, if we write the paper
   without this, we have very little to show."
3. Every figure printed in the manuscript binds to a frozen file under the
   paper gate: the cell is in `paper-v4/active-test-manifest.json`, its
   private outputs are pinned in
   `paper-v4/answer-demonstration/test_gate_integration.py`, and a test reads
   the number from the file. A result not under the gate is not in the paper.
4. Say which layer a result tested. Write "structural gate alone" when no rule
   or logic layer ran. Never let a narrower test read as the whole gate.

## Before you build: bind the cell

Paper work goes wrong by growing. State four things before writing a cell, a
runner, a launch packet or a manuscript paragraph, and stop if you cannot:

1. The exact claim the cell would put in the paper, in plain English.
2. The smallest observation that would support or falsify it, with its counts
   and the layer it tests. Write "structural gate alone" when no rule or logic
   layer ran.
3. The existing artifact to reuse: a registered cell, a frozen packet, a Core
   capability from
   `.claude/skills/malleus-dev/references/CAPABILITIES.md`.
4. What this cell explicitly excludes, and therefore what its result may never
   be quoted for.

A cell is complete when the evidence distinguishes its claim, the paper gate is
green on it, and the result and its limitations are both preserved. A broader
idea found along the way is a finding for Luis, not a silent widening. A model
run is paid once, so the preparation gate closes before the launch, never after.

## Deciding with Luis

- Decisions come to Luis in chat, whole: what it is, the options, the
  recommendation, the cost of each. A pointer to a file is not a decision.
  Write the file as the archive and state its conclusions inline in full.
- Plain English first. Explicit names, no codenames or shorthand: "the first
  half of the Shop reconsideration experiment, where a fresh model builds the
  graph from Table 1", not a stage letter or a run id. Numbers bare. Explain a
  result as what became accessible, what stayed unchanged, what is missing.
- No time estimates. Sequence and dependencies only.
- Do not agree to be pleasant. Restate an instruction in your own words and
  name what it changes before acting. Luis asked for a voice that keeps the
  scope small: push back on doing everything.
- A failed gate returns to Luis in chat and is not worked around. A refusal of
  an honest population is a STOP until every refusal is explained.
- Every agent reads malleus-dev first and works RED before GREEN. An agent's
  report reaches Luis digested by the Overlord, never as a file pointer.

## Runs with a model

- Producer sessions are fresh: one per stage, no inherited context, evidence
  treated as data, the mapping withheld when the mapping is the work. The
  assessor is a fresh session that neither produced the result nor prepared
  the run. Then Luis ratifies by reading the records in full, and the
  ratification is bound to their digests. Until then a review is preliminary.
- Nothing launches on its own. A model run needs Luis's explicit go after its
  preparation gate is green, and it is paid once: harden first, then run.
- A launch packet names the interpreter and the Core the runner imports, and
  the runner refuses a wrong Core. A procedure that says `python` names
  nothing.
- Before a launch, read the exact bytes the producer will receive: the
  isolation message, the procedure, every instruction that names a file. A dry
  run returning `DRY_RUN` says the inputs check out, not that the text is true.
  On 2026-09-18 a stage-keyed message generator served the third boundary's
  producer the second boundary's body, wrong stage, wrong predecessor, wrong
  history, and a procedure told it to export over its own input; both were in
  the bytes a paid run would have consumed, and both were caught by reading the
  printed prompt and the generator's code (E-0470).
- An instruction may only name what the addressee can reach. A producer session
  is fresh by design and exposure forbids it any other stage's workspace, so
  "as before", or a filename from an earlier stage, names something it cannot
  open. State the shape you want where you ask for it, every time. The third
  boundary's `status.json` came back with no status token because two
  procedures said "as before" about a shape only the first had ever stated
  (2026-09-18, E-0477).
- A launched workspace is precious. The first action after a producer reports
  is a read-only archive of its work with a digest manifest, outside the reach
  of any builder. No builder, freeze step or test fixture may delete or rewrite
  a launched workspace; a builder refuses a launched stage. On 2026-09-17 a
  test fixture that called the builder deleted a verified producer output;
  it was recovered byte for byte only because the producer session's
  transcript held its authored files and the runner pins transaction time.
  Guard the work, not only the record of the work, and read a builder's code
  before calling its guard sufficient.
- The authority for what a producer was given is its launch receipt, never what
  the builder would write today. Hold every launched file to its receipt's
  digest in a test, and keep the two questions in two tests: the generator's
  output checked against the generator, the launched record checked against its
  receipt. On 2026-09-18 the first stage's harness procedure was found drifted
  to the builder's later text, and a vocabulary test had been passing only
  because of the drift: it read the mutable copy and reported a property of the
  builder as a property of the record (E-0471, E-0473).
- Every new version of the review protocol is exercised by one full graph cell
  before the paper claims it, and every sentence in it is read against the next
  boundary, not only the current one. A note states the rule and never an
  instance: v3.4's explanatory note counted the obligations of the boundary it
  was written for, and then went to an assessor judging five. The rule it
  illustrated was right and the validator enforced the tally, so nothing
  refused; the dispatch had to carry the correction by hand (2026-09-18,
  E-0477).

## Pins, records, leaks

- Core is not frozen for its own sake. Luis, 2026-09-17: "if we need to fix
  something, lets do it and bump Core for the paper, lets not make a big deal
  out of this unless we're in the final stages of proving the paper,
  bulletproofing it." When Core needs a fix, fix it, move the paper's Core pin
  to the new commit, re-run the cells on it and take the new fingerprints as
  the baseline; a bridge replay of the earlier populations is the evidence
  they reproduce. A replay receipt moving by the producer digest alone is
  expected under any Core change, because the contract binds the compiler's
  own source; domain artifacts byte-identical is the test. Freeze hard only in
  the final bulletproofing stage before submission.
- Core coordinates are stated exactly, as commits. The paper gate reproduces a
  cell by `git archive` of a commit this repository holds; a Core developed in
  an isolated clone must be fetched into this repository before the gate can
  pin it, and a pinned group must import its export in process, not only in
  subprocesses. An export under `private/` is for experiment runtimes, not
  for the gate's pin.
- A review record binds the digest of the protocol it was graded under. That is
  what makes the grading checkable, and it is also what strands the record the
  first time the protocol is corrected. So every protocol version lists, in its
  own bytes, the digests of the files it replaces, and states that a record may
  bind the governing digest or any digest in that list; the validator reads the
  list from the protocol, never from a constant in code. Accepting an older
  binding is not a re-grade: no judgement and no count is touched. Without the
  list, one protocol for every stage means refusing every record written before
  today (2026-09-18, E-0472, E-0474).
- The paper ledger and the master plan are written only by the Overlord. Check
  the next free entry for other writers. An entry carries the result with its
  counts and Luis's rulings in his words.
- Every document carries the current state so a fresh or compacted session
  resumes without loss: the ledger, the resume handover's state block, the
  master plan directive and the project memory, refreshed together.
- `private/` never enters git. Nothing sharing a 60-character normalised run
  with a copyrighted reading leaves `private/`; public files carry ids, slots,
  mechanisms and counts.
- Never `git add -A` or `git add .`. Stage explicit paths; another session
  commits to this repository. Never revert, stash, reset or delete; a failed
  experiment is evidence.
- Core defects go to the Core session with a pinned reproducer. Paper work
  never edits `src/malleus`.
