# Core population piece 7: optional grounded knowledge packs

Status: implemented in Core, awaiting independent overseer verification.

## Coordinates

- Initial RED: `636befa7e42f7c7dd56360c11f0b83f37058472e`
- Term-specific grounding RED: `3db80bcf276445a192a564931b55769a25fac4e5`
- Accepted campaign-surface RED: `101c6bf5c7f8ad0b9ebada20c48ec6dbece16b20`
- Initial GREEN: `6a405b11ad60bec8b73a17d149f8b8801dd27d33`
- Honest-attribution RED: `76b56dfaa9f2ab6b3a90d291be2a271d19e021f0`
- Attribution GREEN: `a559252e014f3605b2c0d6bfe981f31f3e17361e`
- Exact VIM wording RED: `75856c9de5da30aa0bfe2728001d2d35a17a3b69`
- Final GREEN: `5460c8f90e2dc06ad244d9ebc88d444628755e95`
- Final GREEN tree: `be4cb0d53e4a65ace034ee9894e22e88fd57ad22`

## What changed

Core now ships three optional LinkML knowledge packs: `metrology`,
`chronology`, and `research`. They sit between the five-primitives ontology
and a project's domain ontology. A project may import them, copy and alter
them, replace them, or use none of them.

The packs supply reusable mixins, reference classes, and enums. The research
pack carries the shared `AssertionModality` values `STATED`, `MEASURED`,
`CALCULATED`, `HYPOTHESISED`, `CONTESTED`, and `NEGATED`. It matches the
accepted vocabulary sketch: the existing root `Agent` mixin remains imported
rather than redefined; `Campaign` wears `TemporalExtent` and `Counted`; and
the relation vocabulary includes `PART_OF_CAMPAIGN`.

Each pack has one closed `grounding` annotation. Every borrowed term group
names the vocabulary and locator that grounds it. In the research pack,
`Observation` and `Sample` are explicitly grouped under W3C SOSA/SSN;
`measuring instrument` is grouped under VIM; research, investigation, and
method are grouped under the Frascati Manual; and claim and evidence terms are
grouped under SEPIO and Micropublications. The accepted shorter class names
`Instrument` and `Campaign` are declared as local inventions with the bounded
search recorded. The research pack does not claim to borrow `Agent`; it imports
the existing root mixin.

These annotations are retained source provenance. Changing them changes exact
source attestation and compiled artifact bytes, but does not change the
validated semantic fact-set identity.

## Public surface

`malleus.inquisition` exports:

- `validate_pack_grounding`
- `PackGroundingReceipt`
- `PackGroundingRefusal`
- `PackGroundingRefusalReason`
- `PACK_GROUNDING_RITE_IDENTITY`

The installed command is:

```console
malleus-inquisitor pack-grounding ontology/packs/research.yaml --role PACK --json
```

The rite consumes exact UTF-8 YAML bytes. It checks the closed citation shape
and returns a content-addressed receipt or typed refusal. For a project
ontology, each class that directly extends `Entity`, `Event`, `Signal`, or
`Relation` must carry the same grounding shape or a bounded `none_found`
record. Extending a pack class does not duplicate that requirement.

The packs are available through `malleus.ontology.bundled_ontology_path` in a
checkout and installed package. `malleus.compiler.compile_linkml_contract`
continues to require an explicit exact source map, so an authored import such
as `research` never resolves through ambient network or filesystem state.

## Exact artifacts

| Artifact | SHA-256 |
| --- | --- |
| `ontology/packs/metrology.yaml` | `1050b24720f5e7df10dbf6096d8487b46490099b8066c2048a59ef0fa85fc586` |
| `ontology/packs/chronology.yaml` | `6fbd3b49b32f698d8a9f31dcff770660153d822478a3007d0b8018c2af4439b1` |
| `ontology/packs/research.yaml` | `cea850266bd301519061fc741d4c235909d3fd041b50f41b93cece69e6dbd638` |
| grounding rite | `1f642cffadd71e0dc4aabe3f9fdf48b0c0068e2ff4a5e5b8ea588a18de8b3a3e` |

The LinkML support profile advances from `malleus.linkml/private-v0` to
`malleus.linkml/private-v1` because schema and class grounding annotations are
now accepted and retained. There is no v0 fallback. Existing runnable
document and Small Shop change examples were regenerated because their exact
history prefixes bind the compiler implementation profile. Their semantic
contract and accepted graph content remain unchanged.

The original RET-010 research receipt remains byte-identical at SHA-256
`7aaaf6257e2d8e4306356f8660f6f181ac4bfdcb018378baabee398193a6f0d1`.
It records an earlier implementation coordinate, so Core does not rewrite it
with a newer compiler and call that history. The current full public-path
evidence is regenerated and tested separately.

## Mechanical evidence

- The final focused pack suite passes 20 tests.
- All 783 contract-compiler tests pass.
- The full Small Shop integration slice passes 215 tests after regenerating
  current evidence under the new compiler profile.
- The three shipped packs compile through the public compiler.
- One project importing both `research` and `metrology` compiles through the
  same public path.
- Tests reject absent grounding, unknown fields, missing URLs, empty borrowed
  term groups, and an ungrounded project class that extends a root directly.
- Tests bind `Observation` and `Sample` specifically to SOSA/SSN, VIM to
  `measuring instrument`, and the supported Frascati terms to Frascati. They
  also prove that `Agent`, `Campaign`, and `Instrument` are not misreported as
  borrowed terms, and that inventions without a search record refuse.
- The metrology pack records VIM's canonical `kind of quantity` term while the
  local LinkML implementation slot remains `quantity_kind`.
- Another test binds the accepted `Campaign` and `PART_OF_CAMPAIGN` surface.
- The example generator reproduces the committed source-assertion and Small
  Shop change bytes under the new compiler profile.

## Non-claims

The rite does not decide whether a cited vocabulary is intellectually apt,
fetch or authenticate a URL, compare definitions, or prove that a term was
used correctly. The packs are not protocol invariants, domain ontologies, or
mandatory imports. They do not choose a domain-history profile, populate a
graph, admit Events, implement Semantic Re-entry, or stabilize the private
LinkML support profile. This cut proves a small optional vocabulary layer and
its inspectable citation contract, nothing more.
