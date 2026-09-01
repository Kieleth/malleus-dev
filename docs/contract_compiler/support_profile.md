# LinkML v0 support profile

This is the internal developer guide for the selected LinkML 1.11.1 adapter
target. It is rendered by Sphinx so compiler contributors see the current
boundary in the same documentation build as the integration manifest.

It is not a public API or adapter support claim. The authoritative contract is
the accepted `OD-008` decision in `design/contract_compiler/decisions.md`, its
versioned metamodel, mechanical tests, and validated manifests. `CC-R02` may
implement and characterize the adapter. Public namespace placement, public
adapter docstrings, stable public fact identifiers, and public documentation
remain blocked on `CC-D09` and `OD-009`.

The private Greenhouse bootstrap keeps executable policy in
`src/malleus/_contract_compiler_profile.json`. That JSON is an internal
research input, not a public artifact grammar. It declares the accepted source
shapes and the small lowering plan that produces a frontend-neutral contract.
The adjacent private Python module validates and executes those declarations
from caller-supplied bytes and has no source resolver or legacy-registry
fallback. Injected profiles and other frontend adapters remain future work,
not a compatibility promise. Both files remain outside the built distribution
until the full resolver, parser, binder, elaborator, validator, dependency
identity, artifact, and promotion gates are satisfied.

### Private lowering instruction set

The JSON profile is the authority for this bootstrap's semantic choices. The
Python module implements a closed eight-operation instruction set:

| Operation | Exact effect |
|---|---|
| `validate_imports` | Accept only the declared retained import token. Never resolve a path or network resource. |
| `validate_shared_namespace` | Refuse a declaration key repeated across any named source collection. |
| `declare_direct_seed_scalars` | Declare each custom scalar and bind it directly to one declared trusted builtin. |
| `declare_enums` | Declare each enum and emit its ordered set of permissible values. |
| `declare_slots` | Declare global slots and class-local attributes, then apply profile defaults, rules, constraints, resolvers, and predicates. |
| `declare_shallow_classes` | Declare classes and the bounded parent and mixin relations selected by the profile. Refuse unproved inherited semantics. |
| `lower_slot_uses` | Create profile-identified slot-use declarations with profile-selected kinds, predicates, and structural identity roles. |
| `lower_flat_exactly_one` | Create the one-level exactly-one group, alternatives, and conditions selected by the profile. All kinds, predicates, range spaces, and structural identity roles are operands. |

The profile also declares the ASCII key parser, symbol join operation and
separator, ordered range-resolution spaces, resolved kinds and predicates,
field classifications, canonical defaults, and structural hash domains,
prefixes, and member-role maps. An interpreter may contain dispatch and data
structure code, but changing any of those choices requires changing the
profile and therefore its digest. Unknown operations, operands, policy members,
or non-executable combinations refuse before source coverage can hide them.

This instruction set is internal evidence, not a public extension API. A future
frontend adapter or injected profile must either execute this same neutral
contract boundary or introduce a separately versioned, documented instruction
set and conformance suite. Sphinx will surface that public developer contract
only after the promotion decision.

## Why this is a subset

Malleus needs the LinkML constructs used by its current semantics and governed
corpus. It does not need an accidental promise to interpret all of LinkML.
Keeping one closed profile gives us six useful properties:

1. Unknown input fails instead of acquiring hidden upstream semantics.
2. The adapter emits deterministic, frontend-neutral facts.
3. The LinkML-free runtime never infers LinkML defaults or reads LinkML objects.
4. Another frontend can target the same neutral contract without emulating
   LinkML.
5. Reviews can audit every accepted source location and every semantic effect.
6. The implementation stays small until a named use case earns an extension.

Parser acceptance is not compiler support. A parser branch that reads a new
member while the profile does not classify that exact location is a bug. The
compiler must refuse it.

## Four exact classifications

Every field or annotation at every source location has exactly one class:

* `ENFORCED` changes elaboration or emits ordinary semantic facts.
* `IDENTITY_ONLY` establishes identity, reference, closure, or authoritative
  ownership and emits no fact solely for that member.
* `ANNOTATION_ONLY` is retained as queryable projection and provenance metadata
  but does not affect semantic facts or `EffectiveContract` identity.
* `REJECTED` refuses the complete compilation.

Unlisted input is `REJECTED`. Moving a listed field or annotation to another
location does not preserve support.

| Exact source location | ENFORCED | IDENTITY_ONLY | ANNOTATION_ONLY | REJECTED |
|---|---|---|---|---|
| schema root | `types`, `enums`, `slots`, `classes`, `imports`, `default_range` | `id`, `prefixes`; each prefix key and value; each import reference; the `default_range` reference | `name`, `version`, `title`, `description` | every other field; every annotation |
| `types.<type>` | `typeof` | declaration map key; `typeof` reference | `uri`, `description` | every other field; every annotation |
| `enums.<enum>` | `permissible_values` | declaration map key | `description` | every other field; every annotation |
| `enums.<enum>.permissible_values.<value>` | permissible-value map key | none | `description` | every other field; every annotation |
| `slots.<slot>` global declaration | `range`, `required`, `multivalued`, `identifier`, `inlined`, `equals_string`, `minimum_value`, `maximum_value`, `value_presence` | declaration map key; `range` reference; `annotations.adopts` only for the exact imported global-slot redeclaration authorized by `OD-002` | `description` | every other field; every other annotation, including `annotations.retires` |
| `classes.<class>` | `is_a`, `mixin`, `mixins`, `abstract`, `slots`, `attributes`, `slot_usage`, `exactly_one_of` | declaration map key; references in `is_a`, `mixins`, and `slots` | `class_uri`, `description` | every other field; every annotation |
| `classes.<class>.attributes.<slot>` | `range`, `required`, `multivalued`, `identifier`, `inlined`, `equals_string`, `minimum_value`, `maximum_value`, `value_presence` | local declaration map key; `range` reference | `description` | every other field; every annotation |
| `classes.<class>.slot_usage.<slot>` | `range`, `required`, `multivalued`, `identifier`, `inlined`, `equals_string`, `minimum_value`, `maximum_value`, `value_presence` | authoritative slot reference map key; `range` reference | `description` | every other field; every annotation |
| `classes.<class>.exactly_one_of` | flat nonempty alternative sequence | none | none | empty sequence; `any_of`, `all_of`, `none_of`; nesting; every other expression field |
| one `exactly_one_of` alternative | one nonempty `slot_conditions` map | each `slot_conditions` map key is an authoritative qualified slot reference | none | empty alternative; every other field; every annotation |
| one `slot_conditions.<slot>` condition | `required`, `equals_string`, `value_presence`, with at least one present | the authoritative slot reference inherited from its map key | none | every other field; every annotation; nested expression |

Unknown fields and annotations refuse at every location. The explicit refusal
set includes `annotations.retires`, `range_expression`, `rules`, `unique_keys`,
patterns, unsupported cardinalities, `any_of`, `all_of`, `none_of`, nested
expressions, repeated or conflicting mixins, and duplicate declarations. The
only duplicate-declaration exception is the exact adopted imported global-slot
redeclared under `OD-002`. `annotations.adopts` is identity-only there, is
rejected everywhere else, and never emits an adoption fact.

Schema `id` is the semantic module IRI. Schema `name` and `version` remain
annotation and provenance metadata, not qualified-symbol inputs. Prefixes
affect semantic identity only when a reference uses them. Each
permissible-value key is enforcing because it emits one `cf:enumValue` fact.
Its body accepts only null, an empty map, or a map containing only a string
`description`. Null means an empty value declaration and is not semantic null.
Null refuses everywhere else.

## Raw source grammar and symbol identity

The adapter classifies raw YAML tokens and the duplicate-key-preserving typed
tree before it constructs LinkML objects. V0 accepts exactly one implicit
mapping document, with no directive or document-boundary marker, and only
JSON-shaped values. Duplicate mapping keys, aliases, anchors, merge keys, all
explicit YAML tags, including core tags such as `!!str`, non-string mapping
keys, and implicit LinkML coercion refuse. At a
permissible-value body, only the empty plain scalar after `:` and lowercase
plain `null` denote the same empty declaration. `~`, title-case or uppercase
null, and null anywhere else refuse.

| Exact source member | Required raw value |
|---|---|
| document and every declaration, attribute, slot-usage, alternative, condition, annotation, or description-bearing body | mapping; never null |
| schema `id` and `name` | required nonempty strings |
| `version`, `title`, every `description`, `class_uri`, type `uri`, and `equals_string` | string when present |
| `prefixes` | mapping from an ASCII identifier key to a nonempty absolute-IRI string |
| `imports`, class `mixins`, and class `slots` | sequence of nonempty reference strings; a scalar is not promoted to a sequence |
| `types`, `enums`, `slots`, `classes`, `attributes`, `slot_usage`, `permissible_values`, and `slot_conditions` | mapping with the location-specific key and body rules |
| `default_range`, `typeof`, `range`, and `is_a` | one nonempty reference string |
| `mixin`, `abstract`, `required`, `multivalued`, `identifier`, and `inlined` | raw lowercase `true` or `false`; quoted, title-case, and YAML-only Boolean spellings refuse |
| `minimum_value` and `maximum_value` | one finite JSON-number lexical scalar under the grammar below; retain the exact source lexeme |
| `value_presence` | string exactly `PRESENT` or `ABSENT` |
| `exactly_one_of` | nonempty sequence of alternative mappings |
| `annotations` at the one adopted-slot location | mapping exactly `adopts: true`, with literal Boolean `true` |
| one permissible-value body | raw empty scalar or lowercase `null`, empty mapping, or mapping exactly `description: <string>` |

The bound lexeme grammar is exact:

```text
number = ["-"] integer [fraction] [exponent]
integer = "0" | nonzero-digit {digit}
fraction = "." digit {digit}
exponent = ("e" | "E") ["+" | "-"] digit {digit}
```

The token has no whitespace and is classified before YAML tag resolution.
Canonicalization then uses the D05 arbitrary-precision decimal rules, never a
binary float.

| Lexeme class | Exact examples | Result |
|---|---|---|
| accepted | `0`, `-0`, `5`, `5.0`, `5e0`, `5E-2`, `1e+3`, `-12.34` | parse exactly, then canonicalize under D05 |
| refused | `+1`, `01`, `0x10`, `1_0`, `1:20`, `.5`, `1.`, `.inf`, `.nan`, quoted `"1"` | not in the exact grammar |

Declaration, class-local attribute, and prefix keys use the exact ASCII grammar
letter-or-underscore first, followed only by letters, digits, or underscores.
Permissible-value keys are nonempty strings.

Schema IDs and prefix values must be absolute RFC 3987 IRIs with a nonempty
scheme. A literal code point whose Unicode general category is `Cc` or `Cs`
refuses before format validation. Schema `id` additionally has no query,
fragment, or trailing slash. A global key `K` becomes exactly
`schema-id + "/" + K`. A local attribute key
`A` on qualified class `C` becomes exactly `C + "/" + A`. There is no escaping,
case folding, Unicode normalization, path normalization, or ambient base.

A bare reference resolves to exactly one authoritative declaration in the
retained import closure. A prefixed reference uses exact prefix-value and suffix
concatenation, then must resolve to that same declaration. Unknown, ambiguous,
or differently qualified references refuse. D02 adoption remains the only
duplicate ownership exception.

D05 candidate fact and fact-set envelopes bind the internal symbol-policy
identity
`urn:malleus:contract-symbol-policy:linkml-v0-slash-qualified:v0`. It covers the
key grammar, slash joins, prefix expansion, authoritative resolution, and D02
ownership exception. This is not D09 public namespace or stable-ID promotion.

## Trusted LinkML builtins

The exact import `linkml:types` invokes a seven-name trusted lookup map. It does
not run upstream `types.yaml` as ordinary user source. The map binds
`linkml-runtime==1.11.1`, retained root wheel
`linkml_runtime-1.11.1-py3-none-any.whl` with SHA-256
`b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da`,
member `linkml_runtime/linkml_model/model/schema/types.yaml`, 7,296 member bytes,
and member SHA-256
`1c79b264397bec0eadb404d22e9b163458f1b889809b3b482ecc39c98743fe00`.
Any mismatch refuses and remains visible through D11 provenance.

| LinkML source name | Neutral target | Additional facts when referenced |
|---|---|---|
| `string` | `cf:String` | none; trusted D05 seed target |
| `integer` | `cf:Integer` | none; trusted D05 seed target |
| `float` | `cf:Float` | none; trusted D05 seed target |
| `boolean` | `cf:Boolean` | none; trusted D05 seed target |
| `datetime` | `cf:DateTime` | none; trusted D05 seed target |
| `date` | `https://w3id.org/linkml/types/date` | `rdf:type cf:Scalar`; `cf:typeof cf:String` |
| `uri` | `https://w3id.org/linkml/types/uri` | `rdf:type cf:Scalar`; `cf:typeof cf:String` |

`date` and `uri` are distinct Scalar identities based on String. This profile
does not claim their upstream lexical validation. Every other builtin refuses.

## Neutral mapping and defaults

Supported class, slot, enum, scalar, inheritance, mixin, and constraint members
map to the exact D05 seed vocabulary. In this guide, `cf:` abbreviates
`https://malleus.dev/contract-facts/` for readability only; canonical facts
always use the full absolute IRI. Source references first resolve to exact
qualified identities. Global slots, local attributes, and `slot_usage` retain
distinct lossless declaration evidence before elaboration produces their
effective neutral meaning.

The exact omitted-value profile is:

| Effective location | Omitted field | Materialized result |
|---|---|---|
| class declaration | `mixin` | `cf:isMixin=false` |
| class declaration | `abstract` | `cf:abstract=false` |
| global slot, local attribute, or effective `SlotUse` | `range` | schema `default_range`; if that is absent, seed `String` |
| global slot, local attribute, or effective `SlotUse` | `required` | `cf:required=false` |
| global slot, local attribute, or effective `SlotUse` | `multivalued` | `cf:multivalued=false` |
| global slot, local attribute, or effective `SlotUse` | `identifier` | `cf:identifier=false` |
| supported `Slot` or `SlotUse` with non-Class range | `inlined` | `cf:inlined=false` |
| supported `Slot` or `SlotUse` with Class range whose target has exactly one effective identifier slot | `inlined` | `cf:inlined=false` |
| supported `Slot` or `SlotUse` with Class range whose target has no effective identifier slot | `inlined` | `cf:inlined=true` |
| type declaration | `typeof` | no default; refuse incomplete Scalar |
| any supported constraint location | `equals_string`, `minimum_value`, `maximum_value`, `value_presence` | no fact |
| class declaration | `is_a`, `mixins`, `slots`, `attributes`, `slot_usage`, `exactly_one_of` | no relation or expression fact |

The pinned LinkML identifier-based `inlined` derivation runs before default
fill. More than one effective identifier slot on the target Class refuses.
Explicit `inlined` remains explicit, and D05 rejects `inlined=true` for a
non-Class range.

Defaults fill only after LinkML 1.11.1 elaboration. Its exact supported
ancestor traversal starts with the class, treats authored mixins followed by
`is_a` as each node's direct parents, discovers the closure with a last-in,
first-out depth-first stack, and applies `slot_usage` in reverse discovery
order. The closure must be acyclic. A local attribute is the base instead of a
same-named global slot. Repeated authored mixins and distinct explicit
single-valued `ENFORCED` values from two applicable mixin sources refuse before
order can pick a winner. Annotation-only differences do not refuse. Every
authored description is retained separately without an effective semantic
description winner. Explicit `false` is present and overrides. Numeric bounds
are the one merge exception: they intersect by choosing the greatest minimum and
least maximum. Adapter defaults then become ordinary facts with separate
derivation provenance. Effective `identifier=true` forces effective
`required=true`; an explicit `required=false` for that effective slot refuses.
An implicit default and its equivalent explicit value
produce the same fact and candidate identity. Their source and provenance
attestations differ. Explicit `false` remains explicit. The runtime never
reapplies an adapter default.

Bounds are legal for a direct `cf:Integer` or `cf:Float` range, or a Scalar
chain terminating in one of them. `equalsString` is legal for a direct
`cf:String` or Enum range, or a Scalar chain terminating in `cf:String`.

The immutable CC-X01 `explicit_false` source remains `EQUAL` evidence for its
effective `SlotUse`, but the whole source refuses because its separate global
String Slot has `inlined=true`, forbidden by D05. A separate positive vector
uses literal false for `required`, `multivalued`, `identifier`, and `inlined`
on the String Slot and its class use, producing the four false facts with
explicit-value provenance.

That separate positive vector is exact:

```yaml
id: https://example.malleus.dev/d08-explicit-false
name: d08_explicit_false
imports:
  - linkml:types
slots:
  value:
    range: string
    required: false
    multivalued: false
    identifier: false
    inlined: false
classes:
  Record:
    slots:
      - value
    slot_usage:
      value:
        required: false
        multivalued: false
        identifier: false
        inlined: false
```

| Governed source vector | D08 outcome | Exact reason |
|---|---|---|
| `ontology/malleus.yaml` | ACCEPT | closed non-expression profile and trusted seven-name builtin map |
| `ontology/assent.yaml` | ACCEPT | closed profile plus flat `exactly_one_of` ValidTime evidence |
| `ontology/domains/attack.yaml` | ACCEPT | closed non-expression profile |
| `ontology/domains/cyp450.yaml` | ACCEPT | closed non-expression profile |
| `ontology/domains/ocr.yaml` | ACCEPT | closed non-expression profile |
| `ontology/domains/recon.yaml` | ACCEPT | closed non-expression profile |
| `CC-X01/simple_parity` | ACCEPT | supported direct slot use |
| `CC-X01/parent_mixin_precedence` | ACCEPT | exact pinned ancestor traversal |
| `CC-X01/repeated_mixin` | REFUSE | repeated authored mixin reference |
| `CC-X01/conflicting_mixins_ab` | REFUSE | conflicting ENFORCED mixin values |
| `CC-X01/conflicting_mixins_ba` | REFUSE | same conflict after source-order reversal |
| `CC-X01/numeric_bounds` | ACCEPT | supported numeric-bound intersection |
| `CC-X01/explicit_false` | REFUSE | measured SlotUse remains EQUAL, but global String Slot has illegal `inlined=true` |
| `CC-X01/default_range` | ACCEPT | supported `default_range` materialization with provenance |
| `CC-X01/attribute_slot_usage` | ACCEPT | supported local attribute plus applicable `slot_usage` |
| `D08/valid_explicit_false` | ACCEPT | separate valid String Slot and SlotUse with four explicit false values |

Every distinct applicable class slot produces one `SlotUse`. A local attribute
declares a deterministic class-local `Slot` and its use. A `slots` reference
resolves to one authoritative global, inherited, or adopted slot and creates
its use. A `slot_usage` key must refine a slot already applicable to the class;
it cannot introduce a slot or disappear silently. Duplicate references,
duplicate attribute/reference uses, and ambiguous owners refuse.

`title`, listed `description` members, `class_uri`, and type `uri` remain
queryable outside semantic facts. A presentation-erasure change touching only
those fields preserves facts, candidate fact identities, role-bound identity,
and composition identity. It changes source and provenance attestation.

## Exactly-one expression boundary

The profile supports only flat class-level `exactly_one_of`. Its separately
versioned `FlatExactlyOneExpressionExtensionV0` composes with, but never edits,
the immutable D05 `ExactNonExpressionSeedContractMetamodel`. The named
`ExpressionCapableContractMetamodelV0` identity binds both component identities.
The extension has exactly three reified kinds:

| Subject kind | Predicate | Object type or target | Cardinality |
|---|---|---|---|
| `ExactlyOneGroup` | `rdf:type` | exactly `ExactlyOneGroup` | 1 |
| `ExactlyOneGroup` | `cf:onClass` | `Class` | 1 |
| `ExactlyOneAlternative` | `rdf:type` | exactly `ExactlyOneAlternative` | 1 |
| `ExactlyOneAlternative` | `cf:inGroup` | `ExactlyOneGroup` | 1 |
| `SlotCondition` | `rdf:type` | exactly `SlotCondition` | 1 |
| `SlotCondition` | `cf:inAlternative` | `ExactlyOneAlternative` | 1 |
| `SlotCondition` | `cf:usesSlot` | authoritative qualified `Slot` | 1 |
| `SlotCondition` | `cf:required` | Boolean | 0..1 |
| `SlotCondition` | `cf:equalsString` | string | 0..1 |
| `SlotCondition` | `cf:valuePresence` | string `PRESENT` or `ABSENT` | 0..1 |

A group has one class and at least one alternative. An alternative belongs to
one group and has at least one condition. A condition belongs to one
alternative, uses one authoritative qualified slot with an applicable effective
`SlotUse` on the group's declaring class, and has at least one of `required`,
`equals_string`, or `value_presence`. `equalsString` uses the declaring-class
`SlotUse` and is legal for a direct String or Enum range, or a Scalar chain
terminating in String, under D05.
Inside one condition, `valuePresence=ABSENT` conflicts only with
`required=true` or a present `equalsString`. No cross-branch or cross-group
satisfiability analysis is performed.

Each class has at most one directly declared group, reified once on that class.
Descendants apply ancestor and local groups conjunctively through the same
class-ancestor closure. Inherited groups are not copied or reidentified on a
descendant.

All identity envelopes use D05 compact sorted-key UTF-8 canonical JSON with no
terminal newline. A condition-semantics object has exactly `slot` plus the
present neutral `required`, `equalsString`, and `valuePresence` members.
Conditions sort by canonical bytes. An alternative-semantics envelope has
exactly `conditions` and domain
`malleus.exactly-one-alternative-semantics/v0`; its lowercase SHA-256 is a
`sha256:<hex>` digest. A group envelope has exactly
`alternative_semantic_digests`, `class`, and domain
`malleus.contract-structure.exactly-one-group/v0`. An alternative envelope has
exactly `alternative_semantic_digest`, `group`, and domain
`malleus.contract-structure.exactly-one-alternative/v0`. A condition envelope
has exactly `alternative`, `slot`, and domain
`malleus.contract-structure.slot-condition/v0`.

The lowercase SHA-256 of each structural envelope is appended respectively to
these exact prefixes:

```text
urn:malleus:contract-structure:exactly-one-group:v0:sha256:<hex>
urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:<hex>
urn:malleus:contract-structure:slot-condition:v0:sha256:<hex>
```

These remain internal candidate structural IDs. Branch, condition, and member
reordering preserves facts and identities. Source indexes never enter identity.

Empty groups or branches, duplicate semantic alternatives, duplicate
conditions, unknown or inapplicable slots, incompatible `equalsString` ranges,
extra fields, wrong types, contradictions, nested expressions, and `any_of`,
`all_of`, or `none_of` refuse atomically. The
bundled Assent `ValidTime` case remains real vertical evidence. Core kinds and
predicates stay neutral.

## Internal metamodel identities

The D05 rules, primitives, exact invariant propositions, SlotUse identity
profile, and structural canonicalization token form a sorted compact canonical
JSON seed envelope. The expression rules, exact invariant propositions,
condition-member profile, four structural identity profiles, and the same
canonicalization token form a separate sorted extension envelope. The profiles
bind every domain, member set, array sort, SHA-256 encoding, and output prefix.
A role-bound composition envelope names the seed as `base` and the expression
component as `extension`. Its operator makes active rules the exact closed union
of both rule sets, applies each invariant with its literal subject or whole-set
quantifier, and refuses any unlisted kind or predicate. The exact canonical
bytes are in the authoritative OD-008 decision; this guide freezes their
results:

| Component | Canonical byte length | Internal content identity |
|---|---:|---|
| `ExactNonExpressionSeedContractMetamodel` | 4,819 | `urn:malleus:contract-metamodel:non-expression-seed:v0:sha256:1c68a612f3e7a0f80c31965aa5525954921dfbee60d151552d10d61cb0aac71b` |
| `FlatExactlyOneExpressionExtensionV0` | 4,762 | `urn:malleus:contract-metamodel:flat-exactly-one-extension:v0:sha256:99527d21040cbdda9dd7c579af7f40af8645de9b5f4b1e8ba28b40ddff7d53e6` |
| `ExpressionCapableContractMetamodelV0` | 655 | `urn:malleus:contract-metamodel:expression-capable:v0:sha256:65aae23b7a0892a4d2ae2b5adc6888f1ddd39c94ce03f412d50a6a5ccd5d0964` |

Rule or invariant order is nonsemantic because each array sorts canonical
member bytes. Adding, removing, or changing semantic content changes the
component and combined identities. These are D05 internal candidate inputs,
not D09 public identifiers.

## How to expand the profile

Do not start with a parser change. One expansion lands atomically through this
checklist:

1. State a named Malleus use case or query that the current profile cannot
   express.
2. Obtain the operator decision that authorizes the new semantic boundary.
3. Name the source field or annotation at its exact location and choose exactly
   one of the four classifications with a written reason.
4. Map an enforcing member to the existing D05 seed, or propose a separately
   versioned metamodel extension. Review the D05 seed explicitly. Never change
   it silently.
5. Specify omitted, explicit, defaulted, and wrong-type behavior. State which
   source and derivation provenance is retained.
6. Add a smallest positive example plus unknown-field, wrong-location,
   wrong-type, duplicate, contradiction, and unsupported-form refusals.
7. Add independent source, direct-fact, and oracle parity. The oracle must not
   be generated from adapter output.
8. Add metamorphic tests for source order, member order, annotation erasure,
   explicit/default convergence, and every identity consequence.
9. Bump or rebind the support-profile and metamodel-extension versions as the
   semantic change requires.
10. Update the exact support matrix, decision projection, conformance spine,
    adapter implementation documentation, and this guide in the same change.
11. Run strict Sphinx HTML, doctest, and linkcheck builds plus governance,
    profile, adapter, direct-fact, and oracle checks.
12. Obtain independent evidence review before declaring the expansion
    complete.

Future work may create or inject another frontend adapter at this neutral seam.
This decision does not design a plugin framework, discovery registry, lifecycle,
or public injection API. Any future adapter must declare its implementation and
version plus its exact support, default, and resolver profiles, then pass the
same neutral fact, metamodel, canonicalization, provenance, artifact, runtime,
direct-fact, and independent-oracle conformance contract.

Unknown input remains rejected until all gates pass together. After `OD-009`
permits public promotion, adapter docstrings must name the implementation and
support-profile versions, accepted locations, refusals, applied defaults,
neutral outputs, and provenance. Sphinx may render those docstrings then. This
internal guide does not grant that authority.

See the [compiler documentation boundary](index.md) and the
[validated manifest projection](manifests.md) for the current repository view.
