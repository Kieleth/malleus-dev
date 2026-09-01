---
name: malleus-dev
description: Maintain and evolve the Malleus library itself. Use for malleus-dev architecture, protocol stages, contract frontends, graph backends, adapters, generated projections, artifact formats, dependency boundaries, public APIs, research-to-core promotion, and decisions about modularity, composability, replaceability, or conformance.
---

# Malleus development

Work on the library and protocol, not on one adopter. Route adopter-side
schema and graph work to `malleus-acolyte`, repository audits to
`malleus-inquisitor`, and literature forensics to `malleus-recon`.

In the Malleus checkout, read `docs/IMPLEMENTATION_STATUS.md` before capability
claims and `docs/PRINCIPLES.md` before architectural changes. For any new
boundary, adapter, plugin, artifact, or public API, also read the complete
[`references/UNIX_DESIGN_DOCTRINE.md`](references/UNIX_DESIGN_DOCTRINE.md).

## MCP preflight

Skills do not install or register MCP servers. Before CC-002 work, confirm that
server `cc002` and tools `cc002_acquire` and `cc002_verify_offline` are loaded
in the current task. If any are absent, stop and point to
[`../../../.codex/README.md`](../../../.codex/README.md). Do not replace a
missing MCP tool with shell, package-manager, direct-network, or legacy access.

Any change that adds an MCP dependency to a shipped skill must add its exact
server and tool IDs, setup pointer, missing-tool refusal, and regression test
in the same change.

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
   second independent consumer. Replaceability remains a separate empirical
   claim and requires a deliberately different implementation to pass the same
   conformance suite.

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
   missing identity, unsupported semantics, or an undeclared extension.
9. Generate repetitive projections from the authoritative contract. Never
   hand-edit a generated artifact or promote a projection into authority.
10. Add an extension point only with a concrete role, version rule, capability
    declaration, and rejection behavior. Avoid generic plugin machinery.
11. `LITERATURE_INHERITANCE`: Treat independently convergent literature and
    products as inherited foundations, empirical corroboration, and sources of
    techniques and baselines. Do not organize the work around being first to
    an ingredient. Locate contribution claims in the composed protocol,
    component interactions, and measured results.
12. `MODULAR_INTEGRITY`: Keep cryptographic witnessing behind a replaceable
    integrity contract over the committed protocol-ledger head. Stronger
    signatures, checkpoints, transparency receipts, or timestamps must not
    couple into ontology, admission, assent, temporal projection, or KG
    semantics. A changed event-hash or signature grammar may require a new
    integrity profile or persisted-wire epoch, not a new semantic protocol.
13. `EXECUTOR_ONLY`: Put profile-specific event, record, field, precondition,
    transition, effect, atomicity, and refusal semantics in exact identified
    artifacts. The executor implements only generic operations and declared
    typed capabilities. A second conforming interpreter must consume the same
    artifact and produce the same accepted state or typed refusal without
    copying private branches from the first implementation. Never add an
    unrestricted callback or arbitrary-code escape hatch.

Unix modularity here is not dependency-injection theatre. A stage is
replaceable only when a deliberately different implementation crosses the
same boundary without downstream changes. An adversarial fixture can establish
refusal behavior, but not replaceability.

For graph work, do not conflate the backend capability and schema profile,
runtime storage adapter, admission gate, or canonical logical graph artifact.
Specify and test each as a separate role.

## Qualify a projection

Before calling a materialized graph or other derived store a conforming Malleus
projection, verify all of these:

- `AUTHORITY`: It has no independent governed write path. If it does, define
  explicit reconciliation and stop treating it as a mere projection.
- `DERIVATION_CLOSURE`: Bind the accepted canonical graph-state identity; exact
  initial-base identity and digest; verified selected-prefix identity and
  checkpoint; effective contract and composition; reader identity; projector
  implementation and projection profile; interpretation profile; declared
  side inputs; transaction-time and valid-time coordinates; and output digest.
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

Represent the dependency in the design graph. At minimum, record tuples
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

For v0, LinkML is the sole first-party human-authored ontology frontend. A
LinkML source must be interpreted by an exact, execution-identified official
LinkML compiler under a versioned, fail-closed Malleus support profile.

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
