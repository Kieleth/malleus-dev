# Malleus Principles

Why the system is shaped this way.

`ARCHITECTURE.md` says what the parts are. `DELIMITATIONS.md` says what already
exists elsewhere and what malleus does not attempt. This file says what is
claimed, what is not, and which properties the rites exist to defend.

## The thesis

> Malleus treats typed subgraphs as composable epistemic modules whose
> dependencies, provenance, temporal state, and conclusions can be executed and
> governed.

That sentence is the stable center. It does not imply that a graph is true,
that every domain is representable, or that composition preserves correctness
without explicit interfaces and checks. Everything below is either a
consequence of it or a limit on it.

---

## 1. Encoding is the step you cannot skip

Between a source and a conclusion there has to be something typed.

You cannot check a sentence. You can check a tuple: a subject in a declared
class, a predicate from a declared enum, an object in a declared range, and a
citation. Every guarantee malleus offers operates on that typed intermediate.
Range checks, endpoint contracts, executable rules, atomic staging, assent,
bitemporal replay: none of them can operate on prose.

So a system that goes text to answer with no typed middle has nowhere to put a
gate. It can be careful. It cannot be checked.

This is also the whole shape of the answer to a model that invents things. The
gate does not go on the reasoning, which is free and should stay free. It goes
on the commit. A model may think in sentences and must commit in tuples, and
the tuple either satisfies the schema or comes back rejected with the
constraint it violated.

The limit, stated in the same breath: encoding a domain does not make the
encoding correct. Whether the schema captures the world is a separate claim
needing separate evidence, and no amount of validation supplies it.

## 2. A tuple points at bytes

Every asserted tuple should name its source, and the reference should be
byte-exact: the quoted span verified as a verbatim substring of the named
source at write time, and the source content-addressed so that a changed
source invalidates the citation rather than refreshing a cache.

That property is what turns "we preserved the original intent" from a claim
about diligence into a statement anyone can recheck. It is also the property
most often faked by accident, because a quote that was hand-copied looks
exactly like a quote that was verified, right up until someone measures.

The limit, stated in the same breath: **malleus does not provide this.** The
root declares no citation slot, no quoted span, and no source hash;
`Evidence.locator` and `Evidence.source_version_id` in the assent ontology are
unverified strings. This is a property a malleus-shaped system must have and
that the library has not built, tracked as `citation-byte-verification` in
`IMPLEMENTATION_STATUS.md`. Until it exists, the verification belongs to the
adopter's write path, and the rite exists to ask whether anyone built it.

Rite: `quotation_is_byte_exact`, with `citation_integrity` as its companion.
One checks that the cited id resolves. The other checks that the cited bytes
do.

## 3. Nothing here self-corrects

Every acceptance decision has a named decider, and the decider is a designed
component, not an emergent property of the system running for a long time.

If a machine decides, its decision must be a typed record carrying the inputs
it saw, the verdict, the reason, and the identity and version of the judge.
Malleus provides this half: the assent protocol records decisions as immutable
typed records bound to the exact revision, policy, and monitor outputs that
produced them.

If it declines to decide, the case must land in a queue whose age is measured
and which past a threshold blocks, because a queue nobody drains is silent
acceptance wearing a process. **Malleus does not provide this half.**
`DEFERRED` is a terminal state: there is no open-deferral projection, no age,
and no blocking threshold, so a deferral in a bare malleus system is
indistinguishable from a decision nobody revisited, which is the exact
condition the rite was written against. Tracked as `deferral-queue-aging` in
`IMPLEMENTATION_STATUS.md`; until it exists, the queue is the adopter's to
build and the rite is there to ask whether they did.

Rite: `arbiter_is_accountable`.

## 4. Evidence does not transfer

The claims are separate and each needs its own observation:

```text
Represent -> Execute -> Govern -> Assist
```

Representing a domain is not executing it. Executing rules is not governing
what gets accepted. Governing acceptance does not help anybody do anything.
A result for one tier is not evidence for the next, and the validity of a
composed module is not implied by the validity of its parts, because two sound
modules can compose into an unsound one at the interface.

Rite: `evidence_does_not_transfer`.

## 5. `COMMITTED` means the shape was valid

Nothing more. Whether the record is true, trusted, or safe to act on is a
different question, answered by rules, by assent, or by a person. Never let "it
is in the graph" mean "it is true" in code or in prose. This is rule 8 of the
Adoption Guide and it is repeated here because it is the rule most often lost
first.

## 6. Scale is not a result

A larger graph is not more knowledge, and more infrastructure is not more
progress. The deliverable is the smallest observation that distinguishes the
claim. Everything past that is furniture.

---

## The genome analogy, and exactly where it stops

The analogy is useful, and it shaped three decisions:

- The ledger is the genome, non-coding regions included. Flavour text, examples,
  and asides are kept rather than deleted, because which parts express is not
  knowable in advance.
- Tuples are the coding regions.
- Extraction is transcription, instantiation is translation, and the same tuple
  expresses differently per instance. A dimension of 600 in one context and 900
  in another is the same encoded intent, resolved twice.

It stops in two places, and both matter more than the resemblance.

**DNA has no arbiter.** Biology corrects by proofreading and by selection across
generations, and it tolerates enormous error rates because it has deep time. We
have neither. The arbiter here is a designed component, its decisions must be
readable, and the escalation queue only works if a person drains it. The
metaphor must never be allowed to suggest that the system self-corrects. It does
not. See principle 3.

**DNA has no provenance.** A genome carries no citation to anything. The
property this project is aiming at is the opposite one: every tuple points at
bytes in a source, byte-exact. That is a citation graph, it is exactly what the
genome analogy has nothing to say about, and it is the half of principle 2 the
library has not built yet. Keep it central where the analogy is silent, and
keep it honest about its tense. See principle 2 and
`citation-byte-verification` in `IMPLEMENTATION_STATUS.md`.

Use the analogy to motivate questions. Never cite it as support for a claim.

## What is not claimed

Stated plainly, because the honest version of this design is narrower than the
enthusiastic one:

- RDF supplies a graph encoding, not semantics.
- OWL and RDFS already provide classes, inheritance, and logical entailment.
- Rule systems and modular ontologies already support substantial composition.
- Encoding a structure does not demonstrate that it captures the real world.
- Growing a graph produces neither emergence, nor intelligence, nor
  understanding.

`DELIMITATIONS.md` works through the prior art case by case.

## Reserved future work

> Can a small set of well-designed epistemic primitives compose into
> increasingly rich domain models without losing checkability?

Open question. Not a current claim.

The shape it would take, if it holds: a typed graph is `G = (V, E, t, p)` with
`V` typed entities, claims, evidence, and operations, `E` typed dependencies,
`t` the type assignment, and `p` the properties including provenance and time.
A reusable module is `M = (G_M, I_M, O_M, C_M)`: an internal subgraph, typed
inputs, typed outputs, and executable constraints. Composition `M3 = M1 . M2` is
defined only where the interfaces are compatible, and it needs its own check.

Malleus ships the pieces this would be built from. It does not demonstrate
composition across abstraction levels, so it does not claim it. The rite
`module_declares_its_interface` carries severity NOTE for that reason: it asks,
it does not condemn. Raise the severity in your own rubric when your project
depends on composition.

## The working rule

Before building anything, record four items:

1. The exact claim being tested.
2. The smallest observation that could support or falsify it.
3. The existing artifact to reuse.
4. What is explicitly excluded from this slice.

Build only what changes the interpretation of a claim or is needed to audit the
result. The default exclusions are new databases, orchestration layers,
generalized proof engines, scale infrastructure, security machinery, extra case
families, duplicated executions, and artifact ceremony beyond the identity,
provenance, and reproducibility the claim needs. An exclusion is lifted only by
an explicit recorded decision from the person you are working for.

A slice is complete when the smallest registered evidence distinguishes its
claim, the relevant guardrails pass, and the result and its limitations are
preserved. All three. More cases and more machinery are not progress by
themselves.

If the work reveals a broader idea, a bug, or a possible experiment, record it
as a finding or a pending action; do not silently widen the slice. If the
widening materially changes the claim, the denominator, the intervention, or
the interpretation, stop before implementation and obtain a decision.

One case needs naming because the two doctrines meet there: an open gate found
mid-slice and out of scope. Do not close it silently and do not defer it
silently. Record it and surface it immediately, and let the human decide
whether it enters this slice.

Exploration stays welcome. Negative results are kept. Neither rewrites a
finished result after the fact.
