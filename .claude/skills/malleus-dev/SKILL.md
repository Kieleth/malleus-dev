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

Record these four items before writing code:

1. The exact claim or requirement being satisfied.
2. The smallest observation that would show it holds or fails.
3. The existing artifact or mechanism to reuse.
4. What the slice explicitly excludes.

Stop if any item is missing. A new abstraction found during implementation is
not automatically part of the slice. Record it and ask the human when it would
change the claim, boundary, or public contract.

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

Unix modularity here is not dependency-injection theatre. A stage is
replaceable only when a deliberately different implementation crosses the
same boundary without downstream changes. An adversarial fixture can establish
refusal behavior, but not replaceability.

For graph work, do not conflate the backend capability and schema profile,
runtime storage adapter, admission gate, or canonical logical graph artifact.
Specify and test each as a separate role.

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

## Accepted contract-frontend boundary

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
second first-party authoring language. Runtime graph construction,
GraphRecipe, admission, replay, and migration consume the compiled contract
and must run without LinkML installed.

Generated JSON Schema, SHACL, OWL, RDF, Python, or other schemas are optional
projections. Each binds its generator and profile and reports semantic
coverage and loss. No projection can bypass the effective contract.

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
