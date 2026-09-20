---
name: malleus-dev
description: Maintain and evolve the Malleus library itself. Use for Malleus architecture and protocol stages, ontology contracts and their compilation, rule design and rule binding (adopter rules, check contracts, re-binding across an ontology revision), graph backends, adapters, generated projections, artifact formats, dependency boundaries, public APIs, Core's declared capabilities, research-to-core promotion, and decisions about modularity, composability, replaceability, or conformance.
---

# Malleus development

Work on the library and protocol, not on one adopter. Route adopter-side
schema and graph work to `malleus-acolyte`, repository audits to
`malleus-inquisitor`, literature forensics to `malleus-recon`, and the paper
front, its cells, manuscript and gate to `malleus-paper`, whose work these
rules bind.

## What Core can do

[`references/CAPABILITIES.md`](references/CAPABILITIES.md) is the declaration of
Core's shipped capabilities, each with its public entry point and its status.
Read it whenever a limitation is encountered, in this repository or in any
consumer project, and use the capability in full **before declaring a gap**,
writing adopter code, or working around it. A gap is declared only when the
declaration says the capability does not exist, and then it is filed as a Core
requirement.

Luis, 2026-09-17: "That core has capabilities we're not using in shop is just
plainly wrong, we work on core so that we can use them." That day a staged run
planned to accept an ontology gap while additive contract revision was shipped
and exercised, a producer probed about 5,700 values for a vocabulary that lived
in a private set, and a checker's required boundary identity reached nobody
preparing the run. None of the three was a missing capability.

A declared typed gap is retained as an artifact and nothing consumes it: no
revision proposal, no report of open gaps against open proposals. That is
today's behaviour, not a design. Whether a declared gap should trigger ontology
growth is ROADMAP F2, open (E-0486).

In the Malleus checkout, read `docs/IMPLEMENTATION_STATUS.md` before capability
claims and `docs/PRINCIPLES.md` before architectural changes. For any new
boundary, adapter, plugin, artifact, or public API, also read the complete
[`references/UNIX_DESIGN_DOCTRINE.md`](references/UNIX_DESIGN_DOCTRINE.md).

## Before you build: bind the slice

Before writing code, classify every deliverable and every capability claim.
Use exactly one role for each claim:

- `PROTOCOL_INVARIANT`: a domain-, fixture-, adapter-, and backend-independent
  rule of the base protocol.
- `OPTIONAL_PROFILE`: an additional set of guarantees that becomes normative
  only when an adopter claims that profile.
- `REFERENCE_IMPLEMENTATION`: one shipped way to realize a claimed profile.
- `CONFORMANCE_FIXTURE`: frozen evidence that tests a boundary. A fixture is
  never protocol vocabulary or authority.
- `ADOPTER_CHOICE`: a domain, representation, storage, workflow, or policy
  decision outside the guarantees of the claimed profiles.

For each deliverable, name the lowest affected profile and the guarantees
omitted when that profile is not selected. Stop if the classification or
profile is unclear. A shipped default does not become a protocol invariant by
being convenient, and a fixture does not become one by catching a real bug.

Then record these four items:

1. The exact claim or requirement being satisfied.
2. The smallest observation that would show it holds or fails.
3. The existing artifact or mechanism to reuse.
4. What the slice explicitly excludes.

Stop if any item is missing. A new abstraction found during implementation is
not automatically part of the slice. Record it and ask the human when it would
change the claim, boundary, or public contract.

Before dispatching bounded capture, reconciliation or repair, read the shared
[outcome and permission check](../malleus-acolyte/SKILL.md#outcome-and-permission-check).
Check the promised outcome against permitted changes and feedback before
launching, not only when reviewing the result. A finished attempt need not mean
the wider objective is complete.
For evidence-driven acquisition and its completion report, route to the shared
[progressive review rule](../malleus-acolyte/SKILL.md#maintaining-interpretations-as-evidence-accumulates).
Keep instruction delivery separate from behavioral enforcement; do not claim a
missing completion check exists because the installed skill names the rule.

A dispatched agent knows only what its brief carries and what it reads itself.
A brief that says 'as before', or that points at another agent's worktree,
hands it nothing. Name the path and state the shape you want where you ask for
it, every time (E-0477; the paper skill carries the producer-session form of
this rule).

## Research-to-core promotion gate

Relevant literature can constrain a design, supply a test, or suggest an
implementation. It does not authorize core expansion. Before acting on a
research finding:

1. `EVIDENCE_BINDING`: Bind the finding to inspected evidence and state the
   mechanism, assumptions, and threat model that support the proposed transfer.
2. `ROLE_AND_CONSUMER`: Name the existing protocol role or boundary it serves
   and its current concrete consumer. If neither exists, keep the finding
   proposed and defer it rather than creating generic machinery.
3. `USE_CLASSIFICATION`: Classify its intended use as a `DESIGN_CONSTRAINT`,
   `BASELINE_OR_ORACLE`, `CONFORMANCE_FIXTURE`, `IMPLEMENTATION_CANDIDATE`, or
   `EXPLICIT_EXCLUSION`. The classification describes use, not maturity.
4. `MATURITY`: Preserve `PROPOSED`, `ACCEPTED`, and `IMPLEMENTED` as distinct
   states. The human accepts or refuses the transfer. Implementation requires
   the bounded slice, observations, and status evidence demanded elsewhere in
   this skill.
5. `PLACEMENT`: Apply the result at the narrowest surface. Constraints shape
   contracts; baselines, oracles, and fixtures shape tests; implementation
   candidates enter the normal build sequence; exclusions retain what was
   rejected and why.
6. `CORE_PROMOTION`: One current consumer can justify a research-local
   implementation. Promotion to shared vocabulary or generic core waits for a
   second independent consumer with a different shape. Replaceability remains a
   separate empirical claim and requires a deliberately different implementation
   to pass the same conformance suite.
7. `LITERATURE_INHERITANCE`: Treat independently convergent literature and
   products as inherited foundations, empirical corroboration, and sources of
   techniques and baselines. Do not organize the work around being first to an
   ingredient. Locate contribution claims in the composed protocol, component
   interactions, and measured results.

## Rules and the ontology

Read this before proposing any change to where rules live, how they bind, or
what an ontology revision does to them. It settles a debate that surfaced four
times.

**What a rule is today.** A rule layer is a `LogicContract`: a small YAML file
naming a Prolog rules file and pinned to the hash of the ontology those rules
were written against. A `PolicyProgram` in the normative profile selects it by
contract id and contract identity. `PrologVerifier` runs the rules over the
compiled facts of the candidate state. Until 2026-09-19 that call lived in each
adopter's runner and Core checked the receipt rather than the rule: it refused
a check the policy did not require, a wrong check identity and a violated
verdict, and it accepted a `CHECK_RECORDED` event asserting SATISFIED that no
engine had produced. That measured fact is what ROADMAP F1 was built against;
since F1 landed, Core runs the check itself inside one operation, under "What
was built for F1" below, and the two-step path remains public. Prolog is the
only admissible check implementation, and the reason is mechanical, not a
preference: the contract names no engine and closes its fields, so a second
engine would need a contract field that does not exist. Read the two live rule
layers before designing here, with their `logic.yaml` files:
`private/shop-progressive-01/producer/workspace-stage-c/inputs/rules.pl`, local
only because `private/` never enters git, and
`paper-v4/experiment-v4/content-rules-doc-02/rules.pl`.

**The hash chain that must travel together**, as measured at E-0458
(2026-09-17) on nine copies of the live Shop history: ontology bytes, the
ontology hash, the check contract hash, the policy's check identity, the
normative profile, the partial effective contract. One byte moving in the
ontology moves five identities with the rule bytes untouched. Adding one
change kind to the revision policy moved that policy's content-addressed
identity and broke frozen evidence three layers away (overseer entry
OVR-000466, sealed at commit `ff1c6931`; the re-baseline is E-0467). Across an
additive ontology revision the rule layer follows only by
`REBIND_CHECK_CONTRACT`, a declared change kind decided by a person. Core
re-points identities, runs no rule and decides nothing. The adopter retains the
re-pinned contract in the same act, or its own runner refuses at the next
admission: `CHECK_CONTRACT_NOT_RETAINED` is the Shop runner's typed refusal,
not one of Core's closed reasons (E-0458, E-0465).

**What already lives inside the ontology.** Use it first. The compiled LinkML
constraints become contract facts, hold closed-world at write time, and travel
inside the ontology hash with no second identity and nothing to re-bind:
`required`, ranges, `minimum_value`, `maximum_value`, `equals_string`,
`value_presence`, and `exactly_one_of` over slot conditions. LinkML is the
Linked Data Modeling Language, the YAML schema language Malleus compiles. They
reach about half of one of our six live rules, because four of the six join
two records or parse free text and no schema language expresses that. The six
are the census any proposal is read against: the Shop's
`NO_CONFLICTING_QUANTITY` and `NO_EMPTY_RECORD`, and the document path's own
`NO_CONFLICTING_QUANTITY`, which reads `assertion_modality` and is a different
rule body under the same id, plus `INTERVAL_SANITY`, `NUMBER_IN_CITED_TEXT` and
`FORMULA_IN_SOURCE`.

**What was decided before.** `docs/DELIMITATIONS.md`, standing order "Axioms
and domain rules as data": the contribution is "the pinned-contract lifecycle
(rules as gated, versioned, hash-identified KG citizens whose acceptance is
itself ontology-checked), not the rule formalism". KG is the knowledge graph.
That order predates the question being asked again, and it was never built.
Then E-0457 (2026-09-17), Luis's North Star: a rule found in a source is
knowledge about a rule, not a live check; making it live is a deliberate
recorded act by a named decider; the separation of contract and tuple stays,
because a check reads the contract. The Shop's `ShipmentRuleClaim` is that
already, a rule held as a typed record with its threshold as a slot, stored and
not run
(`private/shop-progressive-01/producer/workspace-stage-c/inputs/context.yaml`,
admitted at E-0451).

**What was decided on 2026-09-19** (E-0486 to E-0488; Luis, reading the
findings: "go on both", meaning the one-call admission of ROADMAP F1 and this
constraint, in that order).
`RULE_DECLARES_ITS_READS`: every rule declares the classes and slots it reads,
with an explicit reads-all-types marker for a rule that quantifies over every
type. Core will check the declaration against the compiled contract and, across
a revision, intersect each declaration with the compiled diff, re-bind
automatically when nothing a rule reads moved, and flag the rule with what
moved when something did. Why this and not moving rules into the ontology: the
pain is a missing dependency, not the language. A rule records no dependency
finer than a hash of the whole ontology, and Core already computes the revision
diff as a set difference over semantic facts, so the intersection lacks only
its other half. Cost: one contract field, paid once, re-pinning every frozen
coordinate, which is the OVR-000466 blast radius. Residual: Core cannot read
Prolog, so the declaration is an adopter assertion until rules move to a
grammar Core parses. Sequenced after the one-call admission (ROADMAP F1). It
is the design constraint for F3, the impact of a revision, and for F5,
re-binding derived instead of decided (E-0488).

**What was built for F1.** ROADMAP F1 made compile, check and admit one Core
operation, `malleus.compiler.check_and_admit_population_plan`, on main
`a68d11c9` (2026-09-19; overseer entry OVR-000468). A semantic ledger and plan
bytes go in. Core compiles against the contract the ledger requires, loads the
Prolog check contract the ledger retains and runs it, then appends the retained
plan, gaps, change set, receipt and the three protocol events; or it refuses,
naming the stage (`COMPILE`, `CHECK`, `ADMIT`), the witness records and the
violated rule ids, and a compile or check refusal writes nothing. No parameter
takes an outcome. Built RED first, both measurements kept as tests on the
untouched Core: an admission with no check event refuses
`MISSING_REQUIRED_CHECK`, and a fabricated SATISFIED check event is admitted
with no engine run. Its two consumers of different shape are the Shop runner
and the document path; neither is migrated yet, so the Shop's own 700-line
sequence still runs until the migration lands, and no model run happens before
it. Residual, undecided: `admit` and `admit_with_anchors` stay public and read
a caller-supplied outcome, so the two-step door is still open (E-0486, E-0488,
`handover/2026-09-19-core-atomic-admission.md`).

**What is excluded.** `EXPLICIT_EXCLUSION`: a second check engine, either
SHACL-SPARQL or the SPARQL 1.2 Rule Language, as an alternative to Prolog.
SHACL is the Shapes Constraint Language, SPARQL is the W3C query language for
RDF, and RDF is the Resource Description Framework triple model. Three reasons,
recorded so the question is not re-asked from scratch: zero consumers today, a
second identity scheme, and a reversal of SHACL's standing classification in
this repository as a projection. Note what the standards did in September 2026,
as reported by the findings and fetched on 2026-09-19: SHACL 1.2 Rules became
the SPARQL 1.2 Rule Language, a text language, and the rules-as-RDF mechanisms
are off the standards track.

**The target, held.** Rules as records in the knowledge graph with a recorded
activation act, the shape E-0457 already ruled. Specify only the activation
act, and only when it is needed. The rule grammar stays `PROPOSED` until a
second consumer with a different shape exists, because one consumer makes it an
adapter, which is `CORE_PROMOTION` above.

The research is `handover/2026-09-19-rules-inside-the-ontology-findings.md`,
sha256 `88c9e30a1cb9a0a0335d3437852861a92c138693fe1968fe7835d2f2445510f4`. It
answers ROADMAP F4 and this section is its result. F1 landed on 2026-09-19; the
open work is ROADMAP F3 and F5.

## Choose an adopter rule

An adopter rule is one clause in a pinned Prolog rule file, required by the
admission policy and run over the compiled facts of the candidate state.
"Rules and the ontology" above says exactly what carries it and what moves
when the ontology does. It is `ADOPTER_CHOICE`. Choosing one wrongly cost two
measurement cycles, 2026-09-16 on the Shop path and 2026-09-17 on the document
path (E-0406, E-0426, E-0430): "every value must appear in the sentence it
cites" refused 145 of 294 honest Shop derivations and 216 of 236 honest
document records, because it was designed from the fault it should catch and
never read against the records it would govern. Before proposing any rule:

1. `CENSUS_FIRST`: Run the rule as a read-only query over every honest
   population it would govern, on at least two consumers with different
   shapes, before any Prolog, test, or gate. Bring the refusal count and the
   mechanism of every refusal. A proposal without this table is not a
   proposal.
2. `TYPED_COMPARISON`: Compare like with like. A numeric slot compares against
   numbers parsed from text (digits, number words, plus-or-minus and range
   forms), never against a spelling: `991.0` is `991`. A string slot compares
   after the reading's declared extraction normalisation (ligatures, spaced
   digits and subscripts, hyphenation), declared once per reading, never per
   rule.
3. `DECLARED_DISTINCTIONS_ONLY`: A rule reads only what the compiled ontology
   declares. If it needs a distinction the ontology lacks (a value copied from
   the source, tallied from it, or authored by the producer, such as a record's
   `name`), the rule is out of reach. Record the Core requirement; do not
   approximate it with a slot list. That is what a rule may read. What a rule
   must declare it reads is `RULE_DECLARES_ITS_READS` under "Rules and the
   ontology", adopted 2026-09-19 and not yet built.
4. `EVERY_REFUSAL_EXPLAINED`: The acceptance gate is that every refusal on an
   honest population is classified as a rule defect or a graph defect, with
   rule defects at zero. Zero refusals is required only on dimensions the
   review protocol already verified. A rule that finds graph defects in an
   honest population is a result, not a failure.
5. `SAMPLE_BEFORE_RELOCATING`: When a rule fails on one consumer, read the
   other consumer's records before moving the rule there.
6. `MEASURE_WHAT_CAN_BE_MEASURED`: Before recommending a rerun or a gate, read
   what the catalogue holds that the rule could catch.

Worked case, with the mechanism of every refusal in each cell's own write-up:
`research/ontology_driven_kg_realization/experiments/small_shop/content_rules`
(Shop, in `README.md`) and `paper-v4/experiment-v4/content-rules-doc-01`
(document, in `RESULTS.md`).

## Architectural law

Build Malleus as small, replaceable stages connected by versioned artifact
contracts. Depend on protocol meaning, never on one implementation.

1. Give each stage one bounded responsibility.
2. Keep policy separate from mechanism, and interfaces separate from engines.
3. Pass explicit typed artifacts. Do not communicate through ambient state,
   implicit globals, log scraping, or a neighbour's private objects.
4. Bind every semantic input, output, profile, implementation, and diagnostic
   needed to replay or audit the stage.
5. Keep pure compilation and planning separate from mutation and external
   effects. Stage first; commit only through the owning gate.
6. Make the default implementation ordinary. It receives no bypass, hidden
   field, or semantic privilege unavailable to another conforming adapter.
7. Define replacement by a conformance suite over the boundary, not by class
   inheritance, branding, or method-name similarity.
8. Emit typed diagnostics and fail before partial effects. Never guess at
   missing identity, unsupported semantics, or an undeclared extension. A
   dispatcher keyed by a declared value raises on a key it has no branch for,
   and keys every literal that depends on that key. An identity is declared by
   its owner or derived from the bytes it identifies, never from a path.
9. Generate repetitive projections from the authoritative contract. Never
   hand-edit a generated artifact or promote a projection into authority.
10. Add an extension point only with a concrete role, version rule, capability
    declaration, and rejection behavior. Avoid generic plugin machinery.
11. `MODULAR_INTEGRITY`: Keep cryptographic witnessing behind a replaceable
    integrity contract over the committed protocol-ledger head. Stronger
    signatures, checkpoints, transparency receipts, or timestamps must not
    couple into ontology, admission, assent, temporal projection, or KG
    semantics. A changed event-hash or signature grammar may require a new
    integrity profile or persisted-wire epoch, not a new semantic protocol.
12. `EXECUTOR_ONLY`: Put profile-specific event, record, field, precondition,
    transition, effect, atomicity, and refusal semantics in exact identified
    artifacts. The executor implements only generic operations and declared
    typed capabilities. A second conforming interpreter must consume the same
    artifact and produce the same accepted state or typed refusal without
    copying private branches from the first implementation. Never add an
    unrestricted callback or arbitrary-code escape hatch.
13. `SINGLE_LEDGER_CHANGE_SET`: Every persisted governed domain-state change
    enters one authoritative ordered ledger as one immutable
    `KnowledgeChangeSet`. Its ordered primitive operations and dependencies are
    local to that change set. The accepted temporal graph is replay-derived
    only, begins from an empty graph plus a retained genesis change set, and
    has no independent write path. Persisted structural candidates remain
    non-governed and non-accepted until ledger admission. Machine effects may
    produce, validate, or admit change-set and receipt data, never mutate
    accepted state directly.

Unix modularity here is not dependency-injection theatre. A stage is
replaceable only when a deliberately different implementation crosses the
same boundary without downstream changes. An adversarial fixture can establish
refusal behavior, but not replaceability.

For graph work, do not conflate the backend capability and schema profile,
runtime storage adapter, admission gate, or canonical logical graph artifact.
Specify and test each as a separate role.

Point 8 failed twice in one staged run on 2026-09-18, silently both times. A
stage-keyed message generator with a fall-through `else` served the third
boundary's producer the second boundary's body: right shape, wrong stage, and
no refusal anywhere (E-0470). A runner that named a retained source after its
packet file's stem refused a legitimate second anchor with its own
`SOURCE_ALREADY_ANCHORED`, another runner refusal and not one of Core's,
because two instalments of evidence had been staged under the same filename
and the ledger read them as one source (E-0476, E-0477).

## Qualify a projection

Before calling a materialized graph or other derived store a conforming Malleus
projection, verify all of these:

- `AUTHORITY`: It has no independent governed write path. If it does, define
  explicit reconciliation and stop treating it as a mere projection.
- `DERIVATION_CLOSURE`: Bind:
  - the accepted canonical graph-state identity;
  - exact initial-empty-state identity and retained genesis change-set-set
    digest;
  - verified selected-prefix identity and checkpoint;
  - effective contract and composition;
  - reader identity;
  - projector implementation and projection profile;
  - interpretation profile;
  - declared side inputs;
  - transaction-time and valid-time coordinates;
  - and output digest.
  The graph-state identity identifies accepted semantic state. The output
  digest identifies the derived projection result. Keep them distinct.
- `REFUSAL`: Missing, stale, malformed, or unsupported closure input produces
  a typed refusal before any derived state is returned or committed.
- `REPLAY_CONVERGENCE`: Full replay and incremental replay converge on the same
  canonical logical state under the declared profile.
- `REBUILD_CONVERGENCE`: Deleting the derived store and rebuilding it from the
  bound closure produces that same state.
- `REPLACEABILITY`: A deliberately different conforming projector passes the
  same fixtures without downstream changes before claiming projector
  replaceability.

A second projector demonstrates replacement at this boundary. It does not by
itself justify a generic backend abstraction or another authority.

## Specify every stage

Before implementing a stage, define an addressable contract containing:

1. Role and single responsibility.
2. Accepted input artifact kinds and their identities.
3. Produced output artifact kinds and their identities.
4. Normative semantics and invariants.
5. Typed diagnostics, refusal conditions, and atomicity boundary.
6. Declared side effects, or an explicit statement that it is pure.
7. Version, capability, and extension negotiation.
8. Conformance fixtures and independent expected outputs.
9. Replacement criterion.
10. Explicit exclusions.

Represent the dependency in the design graph,
`design/PROTOCOL_FOUNDATION_GRAPH.ttl`, whose Markdown tuple blocks are
projections of it. Its recorded evidence cutoff is 2026-09-01, so it does not
yet carry the rule decisions of this skill. At minimum, record tuples
equivalent to:

```text
Stage implements ProtocolRole
Stage consumes InputArtifact
Stage produces OutputArtifact
Stage governedBy NormativeProfile
Implementation conformsTo ConformanceSuite
Output derivedFrom InputArtifact
```

The graph records the dependency. Tests establish that the implementation
obeys it.

## Accepted compiler-enabled profile boundary

This section applies only when the compiler-enabled profile is claimed. It
does not make the compiler, LinkML, or an EffectiveContract mandatory for the
base protocol or for adopters that select other profiles.

The names below are roles in the accepted design, recorded in
`design/PROTOCOL_FOUNDATION_GRAPH.ttl`, not Python surfaces. The compiler
ships `compile_linkml_contract`, `ValidatedContractArtifact` and
`ContractView`, the first row of `references/CAPABILITIES.md`. The package has
no `ContractFrontend`, no `ContractCompilationResult` and no
`EffectiveContractArtifact`, and no GraphRecipe runtime ships
(`docs/PRINCIPLES.md`, principle 6; `docs/DELIMITATIONS.md`, "Recipes").

Under the accepted v0 design (`docs/PRINCIPLES.md`, "Contracts are stable;
implementations are replaceable"), LinkML is the sole first-party
human-authored ontology frontend. A LinkML source must be interpreted by an
exact, execution-identified official LinkML compiler under a versioned,
fail-closed Malleus support profile.

LinkML is not the protocol and has no privileged path into the graph. A
`ContractFrontend` consumes retained source bytes, an explicit resolver, and a
support profile. It produces a `ContractCompilationResult` containing
canonical contract facts, annotations, typed diagnostics, and complete
lineage. Malleus validates and canonicalizes that result into an
`EffectiveContractArtifact`.

Any custom frontend may replace LinkML at this boundary if it emits the same
normative intermediate and passes the same frontend conformance suite. Direct
contract facts remain an internal bootstrap and conformance input, not a
second first-party authoring language. Within integrations that claim this
profile, runtime graph construction, GraphRecipe, admission, replay, and
migration consume the compiled contract and must run without LinkML installed.

Generated JSON Schema, SHACL, OWL, RDF, Python, or other schemas are optional
projections of this profile. Each binds its generator and profile and reports
semantic coverage and loss. While the compiler-enabled profile is claimed, no
projection can bypass the effective contract.

## Implementation sequence

1. Reconstruct the current boundary from code, tests, status, and retained
   evidence. Do not infer it from aspirational documentation.
2. Define the stage contract and add it to the design graph.
3. Freeze positive, negative, determinism, corruption, and replacement
   fixtures before implementation.
4. Implement the smallest clear component that satisfies the contract.
5. Run the component alone, through a deliberately different conforming
   fixture, and end to end with its neighbours.
6. Test that unsupported input fails loudly, no partial effect escapes, and
   downstream code imports no concrete adapter internals.
7. Bind the implementation, dependencies, profiles, fixtures, and results in
   execution identity.
8. Update implementation status only for what the observations establish.

When replacing an authoritative production mechanism, remove its old
production path. Adding a conforming implementation at an explicit adapter
boundary is not a fallback: every implementation is explicitly selected and
passes the same suite. Never retain an implicit fallback or two authoritative
interpretations of the same source language.

Two steps an adopter misses exactly once, both from the Shop staged run of
2026-09-18:

- A contract revision that declares a re-bound check contract records an
  identity; it does not retain bytes. Retain the re-pinned contract in the same
  act, and have the act load it back through the history's own selector before
  it returns. Otherwise the history requires a check contract it does not hold
  and the adopter's own runner refuses at the next admission,
  `CHECK_CONTRACT_NOT_RETAINED` in the Shop's. That is not a Core defect, and
  it is not a Core refusal reason either (E-0458, E-0465).
- When a record carries a digest of itself, the contract names exactly which
  version is digested: the object as it will be stored, minus the field holding
  the digest. Anything looser is uncheckable, and the easy mistake is to digest
  the version you started from (E-0479).

## MCP preflight

Skills do not install or register MCP servers. Before work on CC-002, the
reproducible compiler-environment workstream
(`design/contract_compiler/program.md`), confirm that server `cc002` and tools
`cc002_acquire` and `cc002_verify_offline` are loaded in the current task.
If any are absent, stop and point to
[`../../../.codex/README.md`](../../../.codex/README.md). Do not replace a
missing MCP tool with shell, package-manager, direct-network, or legacy access.

Any change that adds an MCP dependency to a shipped skill must add its exact
server and tool IDs, setup pointer, missing-tool refusal, and regression test
in the same change.

## Completion gate

Before declaring completion, perform a self-inquisition over the changed
claims and boundaries. Apply `protocol_role_is_explicit` and
`optional_profile_stays_optional`, record the lowest affected profile and its
omitted guarantees, and correct any fixture or default that acquired normative
authority. Run the mechanical schema rites only when the root ontology profile
is in scope. A root ontology profile purity seal is not repository or protocol
conformance.

A modularity claim is supported only when all applicable checks pass:

- The stage runs independently from frozen inputs.
- Every normative output artifact is deterministic and content-addressed.
  Backend-private physical bytes may differ, but must decode to the same
  canonical logical state under the declared backend profile.
- When replaceability is claimed, a second implementation passes the same
  conformance suite without downstream changes. Adversarial fixtures provide
  additional negative evidence.
- Missing, unknown, malformed, stale, and corrupt inputs refuse mechanically.
- Mutation and external effects remain outside pure compilation stages.
- A clean runtime excludes build-only dependencies where the contract says it
  can.
- Package, installer, documentation, status, and design-graph projections
  agree.
- The result preserves both its evidence and its exclusions.

Do not call a single implementation "pluggable" because an interface exists.
Do not call stages "composable" because their types line up. Replacement and
composition are empirical claims with their own fixtures.
