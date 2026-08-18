# Unix design doctrine for Malleus

This is a Malleus-specific adaptation of Eric S. Raymond's
[*The Art of Unix Programming*](https://www.catb.org/esr/writings/taoup/html/),
especially [Basics of the Unix
Philosophy](https://www.catb.org/esr/writings/taoup/html/ch01s06.html). It is a
design policy, not a claim that Malleus is a Unix command suite.

## The rules, adapted

| Unix rule | Malleus application |
|---|---|
| Modularity | Give every protocol stage one bounded responsibility and a narrow contract. |
| Clarity | Prefer explicit artifacts, states, identities, and diagnostics to clever inference. |
| Composition | Make each stage independently invokable through stable inputs and outputs. Do not expose neighbour internals. |
| Separation | Keep source language from contract meaning, policy from mechanism, planning from effects, and interface from engine. |
| Simplicity | Add only semantics required by a demonstrated obligation. |
| Parsimony | Do not merge compilation, validation, planning, storage, governance, and audit until evidence shows separation cannot work. |
| Transparency | Make inputs, outputs, decisions, state transitions, lineage, and refusals inspectable. |
| Robustness | Use simple visible invariants and deterministic refusal, not forgiving magic. |
| Representation | Put domain knowledge, dependencies, policy, and recipes into versioned data interpreted by small generic code. |
| Least surprise | A declared language follows that language's actual semantics. Never market a subtly different subset under the same name. |
| Silence | Keep successful human output terse and keep artifact, diagnostic, and progress channels separate. |
| Repair | Apply only declared, lossless recovery. Reject early when meaning cannot be preserved. |
| Economy | Spend machine work to remove repeated human work through validators, generators, and conformance suites. |
| Generation | Compile repetitive schemas, bindings, and projections from a simpler authority and retain generation lineage. |
| Optimization | Establish correct semantics with the simplest implementation, then measure before tuning. |
| Diversity | Ship a strong default without making its implementation the only possible protocol participant. |
| Extensibility | Version interfaces and artifact envelopes before accidental compatibility freezes an early mistake. |

Raymond's [modularity
chapter](https://www.catb.org/esr/writings/taoup/html/modularitychapter.html)
develops the relation between simple modules and stable interfaces. His
[transparency
discussion](https://www.catb.org/esr/writings/taoup/html/ch06s02.html) grounds
the requirement that a system expose enough state to demonstrate and debug its
behavior.

## Malleus qualifications

### Silence does not erase evidence

Silence governs human-facing noise. Every material transition still produces
its required structured audit artifact. Data, diagnostics, audit evidence, and
progress are separate channels.

### Repair does not authorize guessing

Normalize only when the transformation is declared by the governing profile,
deterministic, lossless for the relevant meaning, and recorded in provenance.
Reject missing required data, ambiguous identity, unsupported semantics,
failed invariants, and unknown required extensions before effects occur.

### Robust refusal is robustness

Continuing with uncertain or corrupted meaning is not resilience. A refusal is
robust when it is deterministic, typed, explanatory, and leaves no partial
effect.

### Diversity permits implementations, not meanings

LinkML, a custom compiler, and future frontends may implement one
`ContractFrontend` role. They do not define private versions of the protocol.
Every implementation emits the same normative intermediate and faces the same
conformance suite for the declared profile.

### Extensibility is negotiated

An extension has a namespace, version, declared capability, owner, and
failure rule. Unknown meaning is not ignored. Optional meaning may be carried
only when the artifact contract explicitly permits opaque preservation.

### Composition does not require literal text streams

Prefer deterministic, documented, inspectable formats such as canonical JSON,
JSONL, RDF tuples, and stable typed records. A binary artifact is acceptable
when justified and content-addressed. The requirement is an open and testable
boundary, not text as ritual.

### Generation preserves authority and lineage

A generated schema or binding is a projection. Bind its source contract,
compiler, support profile, configuration, output bytes, and coverage report.
Never hand-edit it and never treat generator success as semantic equivalence.

## Boundary test

For every proposed stage, answer these questions mechanically:

1. Can it run from declared artifacts without constructing the whole system?
2. Can its result be inspected without its implementation?
3. Can another implementation produce the same normative result under one
   conformance profile?
4. Can downstream stages consume that result without importing adapter code?
5. Are policy choices explicit data rather than branches hidden in the engine?
6. Do malformed and unsupported inputs produce typed failures before effects?
7. Are dependencies and outputs exact execution identities?
8. Can a future version coexist or migrate without silently changing old
   meaning?

If any answer is no, the boundary is not yet modular. Either narrow it, expose
the hidden contract, or record why this component must remain fused.

## LinkML example

The first-party path is:

```text
LinkML source bytes + locked resolver + Malleus LinkML support profile
  -> official LinkML ContractFrontend
  -> ContractCompilationResult
  -> ValidatedContractFactSet + NormativeAdmissionProfile
  -> EffectiveContractArtifact
  -> GraphRecipe, admission, replay, and KG
```

A custom frontend replaces only the first arrow. It receives no graph handle,
cannot admit records, and cannot alter the normative profile. Replacement is
accepted only when the frontend-neutrality corpus yields the same canonical
fact set, effective contract identity, diagnostics, and downstream behavior.

The official LinkML compiler is therefore the selected implementation, not a
constitutional dependency of the protocol.
