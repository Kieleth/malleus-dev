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

(protocol-boundary-taxonomy)=
## Protocol boundary taxonomy

Every substantial Malleus claim or deliverable boundary has one of these
roles. One document or module may contain several roles when each claim and
boundary is labeled clearly:

| Role | Meaning |
|---|---|
| `PROTOCOL_INVARIANT` | A portable guarantee that every implementation claiming the corresponding Malleus base boundary must preserve. The base invariants are an explicit contract, identified inputs and outputs, atomic fail-closed handling, no semantic guessing, and separation of structural conformance, epistemic acceptance, and action authorization. |
| `OPTIONAL_PROFILE` | A named set of additional contracts and guarantees. It is binding only when an adopter claims that profile. Shipping or using a profile by default does not promote it into the base protocol. |
| `REFERENCE_IMPLEMENTATION` | One implementation of an invariant or profile. Its libraries, storage model, wire format, and APIs are evidence and convenience, not requirements for an independent conforming implementation. |
| `CONFORMANCE_FIXTURE` | A bounded input, answer key, or scenario used to test an invariant or profile. Its vocabulary and modeling choices have no authority outside the stated test. |
| `ADOPTER_CHOICE` | A domain ontology, representation, policy, backend, profile selection, or extension that Malleus deliberately leaves to the adopter. |

This vocabulary is closed for protocol-boundary classification. Capability
status is a separate axis: implemented, accepted design, candidate, and future
work say whether something exists, not what authority it has. An optional
profile can be shipped or merely designed; a reference implementation can be
production-ready or experimental.

The five root primitives, `Entity`, `Event`, `Signal`, `Agent`, and `Relation`,
belong to Malleus's default typed-graph profile. They are not universal data
models or base protocol invariants. Assent, semantic-history and replay, and
graph realization are optional profiles. The current LinkML, Python, JSONL,
NetworkX, Prolog, and OTTR paths are reference implementations or selected
profile mechanisms. CYP450, Quiet Bell, Neutral Greenhouse, and Small Shop
Fulfilment are conformance fixtures or examples; none can define a general
protocol rule by itself.

An adopter may stop before an optional profile or replace its implementation.
It may claim only the guarantees of the profiles it actually implements and
passes. For example, bypassing the semantic-history profile gives up Malleus
claims about ledger authority, historical replay, and reconstruction of
accepted state; it does not invalidate a conforming structural-admission use.

## Protocol authority lives in identified artifacts

Within any profile that claims portable machine execution, protocol authority
lives in identified artifacts, not interpreter branches. Contract facts state
the legal nouns and shapes. A strict protocol-machine program states event
types, preconditions, transitions, effects, atomicity, and typed refusals.
Policy and projection programs remain separate and are referenced by exact
identity where used.

Python is one reference executor. A second conforming interpreter in Rust,
Java, or another language must be able to load the same artifacts and produce
the same accepted state or typed refusal. If that result depends on finding a
profile-specific event, record, or field name only in Python, Python still
contains protocol authority.

The executor may implement generic operations such as lookup, type and subtype
checks, equality, ordering, transaction staging, discard of failed staged
changes, canonical hashing, and invocation of declared typed capabilities. It
receives no unrestricted callback or arbitrary-code escape hatch. A capability
adapter has an explicit contract, identity, effects, refusal behavior, and
conformance evidence.

This is an accepted design boundary for the optional compiler-enabled and
machine-executed profiles. It is not a claim that the generic interpreter or
compiled machine artifact ships today, and it does not force adopters to claim
those profiles.

## 1. Encoding is the step you cannot skip

Between a source and a conclusion there has to be an identified, typed
intermediate.

Malleus cannot mechanically gate untyped prose. OD-005 selects a subject,
predicate, and object interpreted under a declared contract as the canonical
contract-fact atom. The production compiler and runtime API do not exist yet,
and a complete semantic change may require several records admitted atomically.
Range checks, endpoint contracts, executable rules, atomic staging, assent,
and bitemporal replay operate on typed records or atomic packages under that
contract. Evidence-bearing records additionally bind their sources. Citations
are not present on every protocol record.

So a system that goes from text to answer with no typed middle has nowhere to
put a semantic commit gate. It can be careful. Malleus cannot check it.

This is also the whole shape of the answer to Shelob inventing things. The gate
does not go on the reasoning, which is free and should stay free. It goes on the
commit. Shelob may reason in sentences and must commit through typed records or
atomic packages. The package either satisfies the bound contract or comes back
rejected with the constraint it violated.

The limit, stated in the same breath: encoding a domain does not make the
encoding correct. Davis, Shrobe, and Szolovits describe a knowledge
representation as a selective surrogate and a set of ontological commitments.
Gruber defines an ontology as an explicit specification of a conceptualization.
The contract therefore selects what Malleus can attend to and infer. Whether
that selection adequately represents the domain is a separate claim needing
separate evidence, and no amount of structural validation supplies it.

## 2. A tuple should point at bytes

Every evidence-bearing assertion should name its source, and the reference
should be byte-exact: the quoted span verified as a verbatim substring of the
named source at write time, with the source content-addressed. Changed bytes
create a new source artifact. Whether the prior source becomes stale or is
superseded requires a separate, explicit policy relation.

That property is what turns "we preserved the original intent" from a claim
about diligence into a statement anyone can recheck. It is also the property
most often faked by accident, because a quote that was hand-copied looks
exactly like a quote that was verified, right up until someone measures.

Malleus now provides part of this property, and the part matters less than the
part it does not. `SourceArtifact` records a **declared** byte identity: a
SHA-256 digest, a length, a media type, and a locator, all supplied by the
caller and hashed together. Nothing in the library reads the bytes, so a
digest and a length that describe no file anywhere are accepted and replay.
What the record gives you is immutability and attribution: the assertion
cannot be edited later without detection, and `Evidence` names exactly which
assertion it was made against.

What it does not give you, stated so nobody has to discover it: malleus does
not verify the digest against any bytes, does not reopen the locator, does not
declare a quoted span, and **does not detect that a source changed**. Register
new bytes and you get a second artifact; the first stays valid for the bytes
it describes and the old evidence keeps pointing at it, unflagged. Nothing
goes stale, because nothing is watching. That boundary is
`citation-byte-verification` in `IMPLEMENTATION_STATUS.md`, and until it
exists both the verification and the supersession check belong to the
adopter's write path.

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

## 6. Contracts are stable; implementations are replaceable

Protocol meaning belongs to an explicit boundary, never to the first engine
that implements it. Each stage should do one job, consume and produce
versioned typed artifacts, declare its effects and refusals, and expose enough
state for an independent conformance suite to judge it. Policy stays separate
from mechanism. Pure compilation and planning stay separate from mutation and
external effects.

For contract sources, the accepted v0 design selects official, execution-pinned
LinkML as the sole first-party human-authored frontend. It does not make LinkML
the protocol. The frontend compiles retained sources under an explicit resolver
and support profile into the frontend-neutral contract facts that Malleus
validates and canonicalizes. A custom frontend may replace it only by producing
the same normative intermediate and passing the same conformance suite. The
compiled runtime must not require LinkML.

That is an accepted architectural constraint, not a shipped plugin claim. The
current `OntologyRegistry` still interprets LinkML-shaped YAML directly, the
public package still declares LinkML dependencies, and no public
`ContractFrontend` or `EffectiveContractArtifact` API exists. The contract
kernel and frontend-neutrality experiment must establish those boundaries
before promotion.

The broader software doctrine adapts Eric S. Raymond's
[*The Art of Unix Programming*](https://www.informit.com/store/art-of-unix-programming-9780131429017):
small modules, clean composition, policy-mechanism separation, inspectable
state, knowledge represented as data, deterministic generation, fail-loud
repair, and explicit extension. Malleus qualifies the tradition in one crucial
way: permissive input handling never licenses semantic guessing. Only a
declared, deterministic, lossless, provenance-recorded normalization may
repair input. Ambiguity and unsupported meaning reject before effects.

The `malleus-dev` maintainer skill turns this principle into a stage-contract
and replacement checklist.

## 7. Within the semantic-history profile, the ledger is authority

When the optional semantic-history and replay profile is selected, the protocol
ledger records the ordered history of what Malleus proposed, checked, decided,
and applied. Within that profile it is the authority for those protocol
commitments. It is not factual truth about the domain, and projects that do not
claim this profile need not use it.

The complete projection contract Malleus is working toward requires identified
inputs, initial state, projector, contract and interpretation profiles, side
inputs, transaction prefix, and valid-time query. The proposed model is:

```text
accepted_history(t) =
  fold(projector, initial_base, verified_protocol_prefix(t), side_inputs)

view(t, v) =
  resolve(accepted_history(t), interpretation_profile, valid_time=v)
```

This is the log-primary lineage articulated by Kreps and Kleppmann, combined
with Malleus's semantic and epistemic boundaries. If a store has an independent
write path, it is another authority and needs reconciliation. A future closure
manifest should refuse a missing replay input and localize divergence rather
than guess. Core does not yet provide that generic mechanism.

The current core supplies the JSONL protocol authority and an in-memory
NetworkX accepted projection. It does not yet ship generic SQLite, central
store, portal, or arbitrary-backend projections. Chain validation detects
changes that violate event identities or hash links. Clean removal of complete
trailing records leaves a valid prefix. Direct `ProtocolLedger.replay()` and
`AcceptedGraphProjector.current()` can compare the complete ledger with an
authentic, independently retained expected head and event count. Historical
`.as_of()` can bind its selected prefix and separately bind the containing
ledger. A selected-prefix checkpoint alone remains valid after removal of a
later tail and therefore does not authenticate that tail. Core retains no
checkpoint itself, and the ledger is not externally witnessed or tamper-proof.

Stronger integrity belongs behind a separate contract boundary. A witness can
consume a committed protocol-ledger head and emit a signed or transparency-
backed attestation without changing domain records, admission, assent,
temporal projection, or graph semantics. Replacing the event-hash or signature
grammar may require a new integrity profile or persisted-wire epoch, but it
should not require a new semantic protocol. Cryptographic strengthening is
therefore an extension behind the integrity boundary, not a change to the
semantic fabric.

## 8. Independent convergence is corroboration

Malleus often reaches a mechanism empirically before the literature pass finds
an earlier formulation or implementation. That is useful evidence. It shows
that the same constraints led independent groups toward similar structures,
supplies techniques and failure cases we can reuse, and reduces the chance that
the mechanism is arbitrary.

The relationship is cumulative. Malleus does not need to be first to an
ingredient. The contribution belongs in the protocol that composes the
ingredients, the boundaries that make them replaceable, and the empirical
results produced by the complete system. Literature should therefore be used
as inherited structure and design feedback, while novelty claims remain scoped
to the composed protocol and measured findings.

## 9. Scale is not a result

A larger graph is not more knowledge, and more infrastructure is not more
progress. The deliverable is the smallest observation that distinguishes the
claim. Everything past that is furniture.

---

## The genome analogy, and exactly where it stops

The analogy is useful only when distributed across the architecture:

- The ontology and effective contract are the alphabet, grammar, and allowed
  commitments.
- Typed records and atomic candidate subgraphs are encoded change units.
- The ledger is the retained historical sequence.
- Readers, projectors, rules, and runtime profiles are the expression
  machinery. Persisting and binding their identities is a target closure
  requirement, not current behavior.
- The accepted temporal KG is one expressed view.

Calling either the ontology or the ledger alone "the DNA" hides the other
dependencies. The contract determines how records can mean; the ledger retains
their order and protocol history; the projector materializes one graph view.

It stops in two places, and both matter more than the resemblance.

**DNA has no protocol arbiter.** Biology has proofreading, repair, and selection;
none is an accountable Malleus decision procedure. The arbiter here is a
designed component, its decisions must be readable, and the escalation queue
only works if a person drains it. The metaphor must never suggest that the
system self-corrects. It does not. See principle 3.

**DNA does not carry evidentiary citations.** Biological material has lineage
and provenance, but it does not cite the observation supporting a domain claim.
Malleus aims for evidence-bearing assertions to point at byte-exact sources.
That citation graph is exactly what the genome analogy does not explain.
Malleus now binds evidence to a content-addressed source record, but it does not
yet verify quoted spans. Keep that boundary central where the analogy is
silent. See principle 2 and `citation-byte-verification` in
`IMPLEMENTATION_STATUS.md`.

Use the analogy to motivate questions. Never cite it as support for a claim.

## What is not claimed

Stated plainly, because the honest version of this design is narrower than the
enthusiastic one:

- RDF supplies a graph data model and formal entailment semantics. It does not
  supply domain correspondence truth, closed-world admission, temporal
  protocol, or epistemic acceptance.
- OWL and RDFS already provide classes, inheritance, and logical entailment.
- Rule systems and modular ontologies already support substantial composition.
- Encoding a structure does not demonstrate that it captures the real world.
- Growing a graph produces neither emergence, nor intelligence, nor
  understanding.

`DELIMITATIONS.md` works through the inherited literature and system boundaries
case by case.

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
it does not condemn. Raise the severity in a copy of the rubric passed with
`malleus-inquisitor --rubric PATH` when your project
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
mid-slice and out of scope. Record it and surface it: not closed silently, not
deferred silently. The human decides whether it enters this slice.

Exploration stays welcome. Negative results are kept. Neither rewrites a
finished result after the fact.
