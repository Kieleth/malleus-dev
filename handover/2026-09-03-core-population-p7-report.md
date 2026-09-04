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
- Exact VIM wording GREEN: `5460c8f90e2dc06ad244d9ebc88d444628755e95`
- Initial documentation and integration: `9a33e645f0be4f19d4e9f0df89cd9fcfbb6ab501`
- Typed-refusal and SEPIO citation RED: `afe7a69b5eb3617d7c2d53a95df7a2df6cbb90b8`
- Typed-refusal and SEPIO citation GREEN: `6d93b26884a0f65934f79e1b7113a8b4f32244be`
- Edited-pack conformance RED: `c9b964b6152f4dab039fefd60247f05506230159`
- Edited-pack conformance GREEN: `653c47926d4d81bb73e5866464bd8d15988fcced`
- Stronger-declaration RED: `8a0cb78b001370b3f5e1bed7d7f83ad9b27e9a75`
- Stronger-declaration GREEN: `b5625b58ed274ab6734fc28e215910fcefc13479`
- Strengthening-list RED: `9ff72d098e7f3b635888ec40141f16975a7cfb18`
- Strengthening-list GREEN: `7a78406e7473cf49dee3901d221ffa5c5bd3655e`
- Duplicate-list RED: `32aaf89b2954814d0b38972422abf48b8d678fa2`
- Duplicate-list GREEN: `978d6bd2071b35d6319d9a59e8ab43f4a2ccb6ba`
- Reference-import RED: `33f915b722000811fe142be69c00d865fdf746e6`
- Final implementation GREEN: `b37c59708a4ed03eab89d0d3f8dda60912a4ee53`
- Final implementation GREEN tree: `ea2d724638f3a72fabe3d32a05f04502b814551c`

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
method are grouped under the Frascati Manual; SEPIO contributes `assertion`,
`Data Item`, `Evidence Line`, `support`, and `refute`; and Micropublications
contributes `Claim`, `Evidence`, `support`, and `challenge`. The accepted
shorter class names `Instrument` and `Campaign` are declared as local
inventions with the bounded search recorded. The research pack does not claim
to borrow `Agent`; it imports the existing root mixin.

These annotations are retained source provenance. Changing them changes exact
source attestation and compiled artifact bytes, but does not change the
validated semantic fact-set identity.

## Public surface

`malleus.inquisition` exports:

- `validate_pack_grounding`
- `validate_pack_conformance`
- `PackConformanceReceipt`
- `PackGroundingReceipt`
- `PackGroundingRefusal`
- `PackGroundingRefusalReason`
- `PACK_GROUNDING_RITE_IDENTITY`

The installed command is:

```console
malleus-inquisitor pack-grounding ontology/packs/research.yaml --role PACK --json
malleus-inquisitor pack-conformance edited.yaml --against ontology/packs/research.yaml --json
```

The rite consumes exact UTF-8 YAML bytes. It checks the closed citation shape
and returns a content-addressed receipt or typed refusal. For a project
ontology, each class that directly extends `Entity`, `Event`, `Signal`, or
`Relation` must carry the same grounding shape or a bounded `none_found`
record. Extending a pack class does not duplicate that requirement.

Malformed or duplicate-key YAML becomes the typed `MALFORMED_SOURCE` refusal
at both the API and CLI boundary. It never escapes as an ontology-loader
traceback.

The separate conformance call compares an edited pack with one exact reference
pack. Documentation, new declarations, and enum values may be added. Existing
classes, slots, enums, scalar constraints, mapping constraints, and declaration
lists must remain structurally substitutable. Preserved declaration lists may
be reordered but cannot contain duplicates. Reference imports likewise remain
one unique, set-equivalent list. A project extends an existing class through a
new subclass rather than making old instances invalid. The receipt binds both
source identities.

The packs are available through `malleus.ontology.bundled_ontology_path` in a
checkout and installed package. `malleus.compiler.compile_linkml_contract`
continues to require an explicit exact source map, so an authored import such
as `research` never resolves through ambient network or filesystem state.

## Exact artifacts

| Artifact | SHA-256 |
| --- | --- |
| `ontology/packs/metrology.yaml` | `1050b24720f5e7df10dbf6096d8487b46490099b8066c2048a59ef0fa85fc586` |
| `ontology/packs/chronology.yaml` | `6fbd3b49b32f698d8a9f31dcff770660153d822478a3007d0b8018c2af4439b1` |
| `ontology/packs/research.yaml` | `c86abede14242c3179d45807ae6461bf8725ed64256971875d9291a85b7c280e` |
| grounding rite | `1f642cffadd71e0dc4aabe3f9fdf48b0c0068e2ff4a5e5b8ea588a18de8b3a3e` |
| grounding and conformance executor | `37df23e72a764c6ceb8b03797811c67586412698a2d6c0272e394d660b7bf838` |

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

- The final focused pack suite passes 32 tests.
- The complete contract-compiler and inquisitor suites pass 895 tests.
- The Small Shop plus pack integration slice passes 247 tests after
  regenerating current evidence under the new compiler profile.
- The three shipped packs compile through the public compiler.
- One project importing both `research` and `metrology` compiles through the
  same public path.
- Tests reject absent grounding, unknown fields, missing URLs, empty borrowed
  term groups, and an ungrounded project class that extends a root directly.
- Duplicate YAML keys refuse through the API and CLI without a traceback.
- An edited copy may change documentation, add a class, and add an enum value.
  It refuses if the copy deletes the reference surface, makes a concrete class
  abstract, makes an existing slot required, or adds a requirement-bearing
  mixin to an existing class. It also refuses repeated existing mixins,
  repeated existing slots, and missing or duplicate reference imports.
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

The rites do not decide whether a cited vocabulary is intellectually apt,
fetch or authenticate a URL, compare definitions, prove that a term was used
correctly, or prove semantic or behavioral equivalence between edited packs.
The packs are not protocol invariants, domain ontologies, or mandatory imports.
They do not choose a domain-history profile, populate a graph, admit Events,
implement Semantic Re-entry, or stabilize the private LinkML support profile.
This cut proves a small optional vocabulary layer, an inspectable citation
contract, and minimum structural substitutability for edited copies, nothing
more.
