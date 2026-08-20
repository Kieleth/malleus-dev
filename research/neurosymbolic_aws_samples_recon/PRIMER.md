# Primer: the four repos in plain English

Companion to SYNTHESIS.md. No jargon without grounding. Each concept here is
also a typed Claim in the ledger (claim_kind: concept_definition,
recon-events 000138-000178), attached to the Work it comes from.

## The two kinds of thinking machines

**Gedankenexperiment: the intern and the notary.** You employ two people. The
intern read the whole library once, years ago. Ask anything and you get an
instant, fluent, usually-right answer, but the intern cannot show where it
came from, and when wrong, is wrong in the same confident voice. The notary
knows nothing until you hand over documents, but everything the notary stamps
traces back line by line, and the notary will not stamp a contradiction.

Neural = the intern (an LLM). Symbolic = the notary (logic, math, databases,
simulators: rigid, laborious to set up, but exact and checkable).
**Neurosymbolic** is any scheme that makes them one office: the intern drafts,
the notary checks. The four repos are four different answers to one question:
how much power does the notary actually get?

**"LLM proposes, symbolic disposes"** adapts the proverb "man proposes, God
disposes": you may suggest whatever you like; something else decides what
happens. The LLM suggests (an answer, a code file, a query step) and a
mechanical component decides (a prover, a simulator, a schema check). The
whole recon reduces to: when the mechanical thing says NO, does anything stop?

## Repo 1: the kinetics research agent

"Kinetics of biochemical pathways" means: how fast the chemistry inside a
cell runs. A pathway is a supply chain of molecules; enzymes are the machines
on the line. Biologists have published mathematical models of these lines
(the BioModels library), and **COPASI** is the standard open-source calculator
that runs them: give it the model, it computes every concentration over time.
Not an AI. A calculator.

The repo's four "analysis types" are the four classic experiments a biologist
runs on such a model, and they are worth knowing because they are a
pre-registered menu of moves:

- **Knockout**: remove one component entirely (fix its concentration at zero
  and hold it), run the line with and without it, diff the results. Unplug
  one machine on the factory floor and watch which shelves go empty.
- **Metabolic control analysis (MCA)**: for every machine on the line, ask
  "if this one ran 1% faster, how much more would the whole line produce?"
  It finds the bottleneck quantitatively instead of by intuition.
- **Sensitivity analysis**: nudge each dial slightly, measure output movement
  per unit of nudge. Big ratio: a dial that matters. Small: decoration.
- **Pulse response**: kick the system once (inject a burst of a substance)
  and read its character from how it rings and recovers.

Pipeline: your question goes to an LLM that picks a model and one of those
four experiments from a fixed menu. Then **kiro-cli** (AWS's terminal coding
agent, their Claude Code) writes the COPASI simulation code. The code runs.
A multimodal LLM looks at the numbers and the plots and critiques. Another
LLM call decides whether the critique demands rework. Loop until satisfied,
then an LLM writes the report.

Honest verdict: the only component that cannot lie is the simulator's
arithmetic. Every judgment about meaning is an LLM judging an LLM. The loop
closes over the report ("does this answer the question?"), never over the
biology ("does the model match reality?"): there is no hypothesis object, no
prediction compared against observation. And nothing survives a run: each run
is a fresh uuid, no memory.

**About kinets**: the name collides but the domain does not. Your kinets is
liquid neural networks and connectomics, ontology-first, "the ontology is the
journal, nothing gets lost." The real link, now recorded in the ledger
(relation:contrast:kinets:aws-kinetics), is that kinets does exactly what
this research agent lacks: durable, typed capture of what was learned.

## Repo 2: the "description logics" framework

An **ontology** here is a formal family tree of concepts: "a Labrador is a
dog, a dog is a mammal", plus typed relations ("the heart has-part the left
ventricle"). **Description logic (DL)** is the deliberately restricted grammar
these trees are written in. Restricted on purpose: stay inside it and a
program called a **reasoner** can mechanically infer everything the tree
implies and catch every contradiction. SNOMED CT, the giant medical
vocabulary, is written this way.

Gedankenexperiment: a family tree on parchment. Written on it: only parents.
A reasoner is the clerk who can tell you, for any two people, whether they
are cousins, and can spot that someone is listed as their own grandfather.
Owning the parchment without the clerk means you can only read what is
literally written.

What the repo does: it evolves a Python program that answers questions
against such an ontology. Start from a program that always says "I don't
know". Run it on a handful of questions with hand-written gold answers. An
LLM judge marks each answer right or wrong. The failures become a task file;
kiro-cli rewrites the program; repeat. In the shipped example the program
went 0%, 0%, 50%, 100% in four rounds for $0.59.

The finding that matters: **the clerk is never hired.** No reasoner is ever
invoked; the evolved programs walk only the literally-written arrows in a
SQLite copy of the tree. The README says "provably correct"; no proof of any
kind exists in the code. The harness even has a rule saying the reasoning
must go through the proper ontology library, but the rule lives in a prompt,
nothing enforces it, and every shipped program ignores it. The genuinely good
part is the evolution loop itself: domain-blind, cheap, and it converged.

## Repo 3: the clinical chatbot (the one to compare with malleus)

Reading your "we have coder to compare" as "we have code to compare", meaning
malleus. If that is wrong, say so.

Setup: a chatbot answers questions about one patient's record.
Gedankenexperiment: a courtroom stenographer and a judge. Every sentence the
chatbot utters is transcribed into a formal statement and handed to a judge.
The judge is **cvc5**, a theorem prover: hand it statements and it PROVES
whether one follows from the others, or produces a concrete counter-example.
A proof, not a vibe. The patient's record is "the theory": ten facts plus
axioms, written out formally.

The three ideas you asked about, which are the repo's best work:

- **TFU** is a three-valued truth: true, false, unknown. "We do not know
  whether the patient had this diagnosis" is a real stored value, not a
  missing row. A three-position switch instead of a yes/no toggle forced to
  guess.
- **NaN as unknown**: unknown measurements are stored as the floating-point
  value NaN, picked deliberately because ordinary real numbers have no such
  marker. The form has "N/A" printed on it instead of a blank the reader
  must interpret.
- **Explicit closed-world assumption (CWA)**: databases usually treat "not
  recorded" as silently false. This system writes the assumption down as
  axioms: everything not explicitly asserted maps to the unknown value.
  Silence becomes data. Absence has been given a name.

That trio is the same instinct as malleus's crash-loud-on-missing and
explicit indeterminacy_reason, done well at the logic level.

Now the two holes, and this is where malleus is the finished version of
their sketch:

1. **The judge's verdict changes nothing.** When the prover finds a
   contradiction, the wrong answer is still shown to the clinician, with a
   red X emoji next to it. The README admits enforcement is imagined future
   work. A verdict that never gates anything is a label, not a control.
   Malleus's core rule is exactly the missing piece: structural commitment,
   epistemic acceptance, and action authorization are three separate states,
   and acceptance is bound to a policy committed BEFORE the check runs.
   This is directly suggestible to him.
2. **The transcription is done by the intern.** The translation from English
   to logic is one unverified LLM call. The whole chain of custody starts
   with a paraphrase nobody checks. (The reverse direction, theory to
   English for the chatbot's context, is deterministic code, the one honest
   translation in the system.)

Bonus finding: the judge's written reasoning (the "unsat core", the exact
facts that clinched the verdict) is computed on every contradiction and then
thrown away before it reaches the user. The citation trail exists and is
discarded. Plumbing it through is a small, concrete gift you can hand him.

## Repo 4: the text-to-SQL planner (the one that meets your paper)

Confirmed against the internal docs: BIRD text-to-SQL is autoresearch-et's
second domain. EB02 ran the full BIRD Mini-Dev 500: 223/500 = 44.6% execution
accuracy, below the pre-registered 50% bar and below the ~57% naive baseline,
an honestly reported null. The diagnosis was architectural: the seven-slot
clause-by-clause decomposition commits to early clauses (the SELECT) before
later constraints (the WHERE) are visible, and SQL clauses constrain each
other. The ledger already links the two works
(relation:contrast:autoresearch-et:sql).

His system is a direct attack on exactly that failure. Plain story:

1. Instead of asking the LLM to write SQL and hoping, first ask it to write
   down the MEANING of the question: a **Domain Relational Calculus (DRC)**
   sentence, math for "exactly these rows, computed however you like". Two
   very different queries can then be compared by meaning alone.
2. The LLM then assembles a query step by step from 11 legal building blocks
   (join, filter, project...). The menu is enforced mechanically: the LLM
   physically cannot name a move outside it.
3. After each step, cvc5 is asked: does what we have built mean exactly the
   target sentence, in EVERY possible database, not just this one? Only a
   proved construction terminates the loop.
4. SQL is then derived mechanically from the proved construction. The LLM
   never writes SQL at any point.

Where our loop committed early and paid for it, his refuses to accept
anything until the whole meaning is proved at once. That is the honest
comparison for the paper and for the email: mechanism against mechanism,
because he publishes no score (the "near-SOTA" claim has no number anywhere
in the repo) and our score is a pre-registered null with a diagnosis.

Two caveats found in his code: an escape hatch emits SQL from an unproven
construction when the prover keeps timing out (the README's "unsat or
nothing" is not literally true), and rejected proposals are forgotten between
runs, so the system never learns.

What you can share from our side, all already public-quality in
MILESTONE-bird-sql.md: the 44.6% with difficulty split (62.2% simple, 39.1%
moderate, 31.4% challenging), the $0.032/query cost against a $0.51/query
baseline, the early-commitment diagnosis, and that the infrastructure claim
held (3,310 audit events, zero grounding failures, every solved path
reconstructable). Where we got stuck: EB05 through EB09 did not recover the
gap, EB09 regressed into a pre-registered halt, and the later audit found the
holistic-reseed mechanism was unmeasurable because materialized terminals
were never gold-executed.

## TFU/NaN/CWA into malleus: options

Recorded in the ledger as concept slices already. For the literature
grounding work, the options, cost-ordered:

1. **Nothing to build at the review level.** Recon already treats absence as
   data: NOT_ESTABLISHED, NOT_APPLICABLE, UNRESOLVED are exactly the
   three-position switch, and they are preserved rather than promoted.
2. **The genuine import: explicit CWA for the Prolog layer.** Prolog's
   negation-as-failure silently reads "not provable" as "false". Importing
   the clinical repo's move means compiling explicit unknown-facts into the
   fact vocabulary so rules can distinguish "the source states this is
   false" from "the source is silent". Small-to-medium change in
   GraphFactCompiler plus rule conventions plus conformance cases.
3. **Distinguished unknown values for Statusable slots** across the malleus
   root, the general form of the same idea. Larger, touches the ontology
   root, needs an inquisition pass.

Decision is the operator's; 2 is the sharp one.
