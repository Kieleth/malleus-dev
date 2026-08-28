# Contract compiler decision workbook

Status: operator decision support

This workbook connects design terms to their practical use. It records accepted
directions separately from choices that still require the operator. It does not
supersede the canonical protocol foundation graph.

## OD-001: consumer-bundle manifest

Decision state: ACCEPTED, Option A, 2026-08-24

The operator accepted Option A after reviewing how the identity is used in
practice. This section explains the accepted direction. `OD-013` now supplies
the one-distribution topology and `OD-006` supplies the closed three-role
composition. The exact schema and canonical byte grammar remain with
`CC-D16`.

### Canonical means one exact byte representation

Here, canonical does not mean official, central, or saved in YAML. It means the
same typed information always becomes the same bytes.

```text
typed manifest value
  -> reject unknown or missing fields
  -> normalize values under a named grammar version
  -> sort only collections declared order-insensitive
  -> encode using one exact byte grammar
  -> hash those exact bytes with a named domain and algorithm
```

Two files with different key order or whitespace can therefore describe the
same manifest. They normalize to the same canonical bytes and digest. A changed
reader wheel or changed ontology source produces different bytes and a different
digest.

### A schema is the rulebook; a manifest is one filled record

A schema says which fields a consumer-bundle record may contain, their types,
and which are required. A manifest is one concrete record for one consumer and
one build.

For example, a schema may require `consumer`, `sources`, `import_edges`,
`effective_contract`, `reader`, and `authorization_root`. The Recon manifest is
the filled record that names the exact Recon files and reader artifact.

LinkML can describe the manifest schema. Malleus must still specify the
canonical byte grammar and verification procedure.

### Simple practical example

Assume three source modules:

```text
malleus.yaml
  <- assent.yaml

malleus.yaml
  <- recon.yaml
```

Recon uses `malleus.yaml` plus `recon.yaml`. Porchito uses `malleus.yaml` plus
`assent.yaml`. Each consumer receives a separate bundle record.

The Recon record contains, in simplified form:

```json
{
  "consumer": "malleus:recon",
  "sources": [
    {"module": "malleus", "length": 1234, "sha256": "..."},
    {"module": "recon", "length": 5678, "sha256": "..."}
  ],
  "import_edges": [
    {"parent": "recon", "ordinal": 0, "literal": "malleus", "child": "malleus"}
  ],
  "effective_contract": {
    "grammar": "malleus-effective-contract-v1",
    "sha256": "..."
  },
  "reader": {
    "distribution": "malleus-dev",
    "artifact_sha256": "..."
  },
  "migration_profile": "none",
  "authorization_root_sha256": "...",
  "manifest_grammar": "malleus-consumer-bundle-v1"
}
```

The actual format is not decided. This example explains the shape, not the
wire contract.

On the compiler side, the build verifier:

1. reads the exact source bytes through the explicitly selected resolver;
2. checks their lengths and digests;
3. checks the recorded parent-to-child import edges;
4. recompiles the effective contract and verifies its semantic digest;
5. checks the exact reader artifact and authorization root;
6. canonicalizes the manifest and verifies its outer digest.

On the LinkML-free core side, startup verifies the packaged artifact,
attestation, reader, authority, and bundle digests. It does not recompile LinkML
sources. At normal record-write time, the verified runtime holds the bundle
identity and effective contract. A record or ledger header references the
relevant versioned identity.

### What is sorted

The topology is the import graph, represented as edges. Every edge records the
authored ordinal inside its parent. Canonicalization sorts the serialized edge
records by a declared tuple such as parent module, authored ordinal, literal
import, and child module. It does not reorder import processing or erase parent
relationships. A diamond stays a diamond.

```text
quiet_bell -> archive_foundation
quiet_bell -> common_types
archive_foundation -> common_types
```

The sorted list gives deterministic bytes while preserving all three edges.

### What the semantic hashes mean

An exact source digest answers, “Did we read the same bytes?” It changes for a
comment or description edit.

A validated fact-set digest answers, “Did those sources compile to the same
supported declarative meaning?” It can remain stable when annotation-only prose
changes.

An admission-profile digest answers, “Are those facts interpreted under the
same stateful write rules?”

The effective-contract digest binds the validated fact set and admission
profile under named grammar versions. The hash grammar identifies the exact
canonical byte rules and domain envelope. A bare string saying `sha256` is not
enough because different serializations of the same logical value yield
different digests.

Reader code is deliberately outside the effective-contract digest. A
behavior-preserving reader rebuild should change execution and bundle identity,
not semantic identity.

### Why each consumer gets a bundle

A root-only identity would say Recon and Porchito are identical whenever they
share `malleus.yaml`, even if Recon or Assent differs. That grants too much.

An effective-closure-only identity can prove semantic equality, but it cannot
prove which vendored bytes or reader build produced the behavior. That is too
little for reproducibility.

Separate bundles solve both problems:

* Recon binds root plus Recon sources, Recon semantic contract, Recon reader,
  and Recon authority.
* Porchito binds root plus Assent sources, Assent semantic contract, its reader,
  and its authority.
* A mixed vendored root and Assent set fails source and import verification.
* A Recon compatibility decision cannot silently authorize Porchito or OCR.

This is why the consumer bundle is an attested execution packet around an
effective contract, not a replacement name for the ontology hash.

Option A approves one canonical consumer-bundle manifest per consumer. The
contract roles and packaging topology are now closed; `CC-D16` still decides
the exact fields and bytes.

Option B defers the consumer bundle and ships only semantic artifacts. That is
smaller, but it does not mechanically bind a consumer to exact sources, reader,
authority, and compiler attestation.

Accepted: Option A. Its digest remains separate from semantic and
persisted-wire identities.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-001`. Overseer record:
[`OVR-000002`](overseer/entries/OVR-000002.json). `CC-D15` and `CC-D13` are
complete; `CC-D16` remains a separate exact-schema and byte-grammar workstream.

## OD-012: exact compiler baseline

Decision state: ACCEPTED, release-first baseline R3, 2026-08-25

The selected research baseline is the published LinkML `v1.11.1` release at
provenance commit `a7ed3e4cbb19731f072d0d90b6d52f7d822569ee`. This selects
compiler inputs for Malleus development. It does not publish a Malleus release.

The two published wheels are selected for retention as released, not rebuilt:

| Distribution artifact | SHA-256 |
|---|---|
| `linkml-1.11.1-py3-none-any.whl` | `d1bbb97a8b1ea4a99b145007875733a5e5e89b3acfe3e9d1e369fa4a582990ed` |
| `linkml_runtime-1.11.1-py3-none-any.whl` | `b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da` |

The selected source-retention set consists of only the two matching published
sdists:

| Source artifact | SHA-256 |
|---|---|
| `linkml-1.11.1.tar.gz` | `2f6774e13628270cadaeecda3313db0437ecc15cd44ee35c6c2655dbe31c8524` |
| `linkml_runtime-1.11.1.tar.gz` | `e71300b596c4f35aeccd9dca096806678402213dbdb2c5e8e68f507e21320754` |

That set is the LinkML root-source retention set. It is not the complete set of
transitive build inputs. Resolution against the selected tuple established that
LinkML 1.11.1 requires `antlr4-python3-runtime>=4.9.0,<4.10`, while the official
4.9.3 release supplies no compatible wheel. R3 preserves the R2 separate,
exact transitive build-input set:

| Build input | Bytes | SHA-256 |
|---|---:|---|
| `antlr4-python3-runtime-4.9.3.tar.gz` | 117034 | `f224469b4168294902bb1efa80a8bf7855f24c99aef99cbefc1bcd3cce77881b` |
| `setuptools-83.0.0-py3-none-any.whl` | 1008090 | `29b23c360f22f414dc7336bb39178cc7bcbf6021ed2733cde173f09dba19abb3` |

CC-002 must validate both inputs before use. It must build
`antlr4_python3_runtime-4.9.3-py3-none-any.whl` twice in two fresh children of
the selected OCI runtime, with network denied, umask `022`, `TZ=UTC`,
`PYTHONHASHSEED=0`, `SOURCE_DATE_EPOCH=315532800`, pip 25.0.1, no build
isolation, and backend `setuptools.build_meta:__legacy__` supplied by exactly
setuptools 83.0.0. Both wheel byte streams must be identical. CC-002 retains one
verified output wheel and a build record that binds both build results.

The final runtime closure remains wheel-only. The ANTLR sdist and setuptools
wheel remain provenance and build inputs, outside the runtime wheelhouse unless
setuptools is independently required by the resolved runtime closure. The two
published LinkML root wheels remain retained as released and are not rebuilt.

The first real R2 acquisition then exposed a second upstream packaging defect.
LinkML Runtime requires `prefixcommons>=0.1.12`. The exact selected
`prefixcommons` wheel contains the raw metadata header
`Requires-Dist: pytest-logging (>=2015.11.4,<2016.0.0)`. Its semantic
requirement is `pytest-logging>=2015.11.4,<2016.0.0`, for which PyPI supplies
no wheel. Installing that test plugin and its old undeclared `py` compatibility
surface would put test infrastructure into the compiler runtime. R3 instead
selects a governed packaging derivation with this exact upstream input:

| Derivative input | Bytes | SHA-256 |
|---|---:|---|
| `prefixcommons-0.1.12-py3-none-any.whl` | 29482 | `16dbc0a1f775e003c724f19a694fcfa3174608f5c8b0e893d494cf8098ac7f8b` |

The official locator is
`https://files.pythonhosted.org/packages/31/e8/715b09df3dab02b07809d812042dc47a46236b5603d9d3a2572dbd1d8a97/prefixcommons-0.1.12-py3-none-any.whl`.
CC-002 retains this wheel in `derivative-inputs/`, separate from the existing
ANTLR `build-inputs/` and the runtime wheelhouse. The upstream archive has
exactly 14 members and 109044 expanded bytes. Ten are package code or data
members. Its `LICENSE` is 1500 bytes with SHA-256
`3a9b5b0d46996cdfd82b65429e189904e4ab1908014ce408cbecde9f591f37b4`
and begins exactly `BSD 3-Clause License`.

The derived distribution version is exactly `0.1.12+malleus.1`, and its filename
is exactly `prefixcommons-0.1.12+malleus.1-py3-none-any.whl`. The transform
removes only the exact `pytest-logging` requirement. It preserves every package
code, resource, and license payload byte exactly. It updates only the necessary
`METADATA` version and requirement, derived `.dist-info` paths, the `WHEEL`
generator identity, `RECORD`, and deterministic ZIP metadata. The `METADATA`
input is 1960 bytes with SHA-256
`4c6cf90de54fa4ce46d1235551f75c021bacab34b8c9894fd50a8096441a5303`;
the raw targets are exactly `Version: 0.1.12\n` and the named `Requires-Dist`
line. Its body and field order otherwise remain exact. The `WHEEL` input is 83
bytes with SHA-256
`cb778389a15548d4cf6e0cdf367d27627e6d127d5c5fa5ab75eb43950338c56c`.
Its raw ordered body is `Wheel-Version: 1.0\n`, `Generator: poetry 1.0.7\n`,
`Root-Is-Purelib: true\n`, and `Tag: py3-none-any\n`. Replace only the Generator
line with exactly `Generator: malleus-cc002 (wheel-derivation-v1)\n`.

The derived archive and `RECORD` row order are ascending Unicode code-point
order of final POSIX member names, including the `RECORD` member and its row.
Every final ZIP filename is ASCII. `RECORD` is UTF-8 without a BOM and uses
exactly three fields, comma delimiter, ASCII double-quote quote character,
`doublequote=true`, `QUOTE_MINIMAL`, no escape character, LF line terminator,
and a terminal LF. For every member except `RECORD`, its row contains
`sha256=<URL-safe Base64 of the raw SHA-256 digest without = padding>` and the
decimal payload byte length. The `RECORD` row's own hash and size fields are
empty.

Every `ZipInfo` has the ASCII final filename, `date_time` exactly
`1980-01-01 00:00:00`, `compress_type=ZIP_STORED`, `create_system=3`,
`create_version=20`, `extract_version=20`, `reserved=0`, `flag_bits=0`,
`volume=0`, `internal_attr=0`, `external_attr=(0o100644 << 16)`, and empty
`extra` and `comment`. The archive comment is empty. ZIP64 is disabled, and any
input or output requiring it is rejected. CRC32, compressed and uncompressed
sizes, and local-header offsets are consequences of the exact payloads and
member order, not free inputs. The implementation sets every selected
`RECORD`, `ZipInfo`, and archive field explicitly, then reopens the written
wheel and validates every selected field and byte. It never relies on CPython
defaults. The archive must not impersonate upstream version `0.1.12`.

The [PyPA recording-installed-projects specification](https://packaging.python.org/en/latest/specifications/recording-installed-packages/)
is the factual root for `RECORD` semantics. The
[Python 3.12 `zipfile` documentation](https://docs.python.org/3.12/library/zipfile.html)
is the factual root for the named archive attributes. PyPA permits compatible
choices, and Python exposes defaults and ZIP64 support. The complete grammar
above is a Malleus choice; those sources do not mandate every selected value.

The derivation reads ZIP members only. It never imports, extracts, or executes
`prefixcommons`. Before transformation it verifies the whole-wheel identity,
validates the exact input `RECORD`, and rejects duplicate or unsafe member names
and non-regular member types.

CC-002 performs the stdlib-only transform twice in two fresh children of the
selected OCI runtime, with network denied and the same R2
`SOURCE_DATE_EPOCH`, `TZ`, `PYTHONHASHSEED`, and umask. The two derived wheel
byte streams must be identical. It retains the upstream wheel only at
`derivative-inputs/prefixcommons-0.1.12-py3-none-any.whl`. The derived wheel is
retained under `built/`, and
`/built/prefixcommons-0.1.12+malleus.1-py3-none-any.whl` is the exact direct
resolver root. `derivation-record.json`, using schema
`malleus.cc002.wheel-derivation/v1`, binds both transform results and
adapter/tool provenance. The 1500-byte `BSD 3-Clause License` notice remains a
byte-identical member of both wheel artifacts and is bound by that record; no
separate extracted license file is required. The official `prefixcommons`
wheel must be absent from the runtime wheelhouse.

The public acquisition result becomes `malleus.cc002.acquire-result/v3`, the
public verification result becomes `malleus.cc002.verify-result/v3`, the
environment manifest becomes `malleus.cc002.compiler-environment/v3`, and the
internal verification report becomes
`malleus.cc002.internal-verification/v3`. V3 binds eight retained inputs, two
produced artifacts, and `derivation_record_sha256`. The existing
`malleus.cc002.container-verification/v1` and
`malleus.cc002.source-build/v1` contracts remain unchanged, and only
`malleus.cc002.wheel-derivation/v1` is added. `build-record.json` remains the
ANTLR record and `derivation-record.json` is the new wheel-derivation record.

Offline verification must run `pip check`. With strict contraction enabled,
`prefixcommons` must expand `GO:0008150` to
`http://purl.obolibrary.org/obo/GO_0008150` and contract it back to exactly
[`GO:0008150`]. `linkml_runtime.utils.namespaces.Namespaces` must bind `ex` to
`https://example.org/` and return `ex:item` for
`https://example.org/item`. The existing generic generator smoke also remains
mandatory. `pytest`, `pytest-logging`, and `py` must all be absent from the
installed runtime closure.

Malleus owns maintenance and security review of the derived packaging artifact.
A future clean upstream replacement requires a new governed decision. CC-002
must stop on a non-allowlisted payload change, license loss, unequal transforms,
resolver substitution, presence of a forbidden test package, or any smoke that
requires the removed plugin.

The reproducibility tuple is CPython 3.12.10, Linux x86_64, and `cp312`.
It identifies one environment that must reproduce the compiler. It does not
shrink Malleus's runtime or CI support matrix.

The selected KISS lock profile uses pip 25.0.1 and its published
`pip-25.0.1-py3-none-any.whl`, SHA-256
`c46efd13b6aa8279f33f2864459c8ce587ea6a1a59ee20de055868d8f7688f7f`.
The final requirements manifest must pin every distribution and artifact hash,
the retained wheelhouse must contain the complete closure, and a clean install
must succeed with indexes and network denied. CPython 3.12.10 bundles pip
25.0.1 through `ensurepip`; CC-002 must still retain and verify the selected pip
wheel rather than trusting ambient bootstrap state.

The selected platform is the official `python:3.12.10-slim-bookworm` image for
`linux/amd64`. The tag lookup resolved to OCI index digest
`sha256:fd95fa221297a88e1cf49c55ec1828edd7c5a428187e67b5d1805692d11588db`
and selected child digest
`sha256:97983fa8cc88343512862c62307159a82261c3528dc025f79e5a3f7af43e50b4`.
The child digest is the runtime pin. The index digest is retained as provenance.
No child media type is asserted.

CC-D12 selects those coordinates, identities, separate root-source,
transitive-build-input and derivative-input memberships, transformation
allowlist, ownership, and acceptance policies. CC-002 owns acquisition and byte
retention, deterministic double build and double transform, complete transitive
resolution, runtime wheelhouse, platform verification, and offline installation
proof. This split keeps policy decisions out of materialization code.

A later LinkML fork, source commit, clean upstream `prefixcommons` release, or
derived-wheel change cannot silently replace this baseline. It requires a
separate governed baseline revision, exact source and artifact identities, and
the same acceptance suite before an explicit switch.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-012`. Overseer record:
[`OVR-000072`](overseer/entries/OVR-000072.json), replacing corrected R2 record
[`OVR-000061`](overseer/entries/OVR-000061.json). `CC-D12` is complete; CC-002
materialization remains pending.

## Accepted directions in canonical graph revision 18

| ID | Accepted direction | Important limit |
|---|---|---|
| AD-001 | `EffectiveContract` becomes the public runtime root | Production promotion waits for conformance and wire transition |
| AD-002 | LinkML becomes compiler-only | The distribution currently declares LinkML and LinkML Runtime as mandatory dependencies, although tracked `src/malleus` code does not import them |
| AD-003 | Stage protocols remain experimental | Only named whole-pipeline combinations gain conformance claims |
| AD-004 | Duplicate symbols fail closed absent explicit policy | Current schemas use explicit adoption, so policy must be selected |
| AD-005 | Independent branches for independent upstream units plus one exact integration branch | Intrinsic specification and runtime dependencies remain sequential or explicitly stacked |
| OD-002 | Slot-only, exact, explicit adoption | Only literal Boolean `annotations.adopts: true` can authorize an otherwise identical imported slot redeclaration |
| OD-003 | Pinned LinkML 1.11.1 is the replaceable default first-party frontend adapter | Repeated and conflicting mixins are refused; runtime facts are explicit and frontend-neutral |
| OD-004 | New persisted-wire epoch with a typed hard break | Exact public diagnostic identifier is deferred to CC-W01; no fallback, receipt, migration, translation, rewrite, or reinterpretation of legacy `ontology_hash` |
| OD-005 | Ontology-powered atomic subject-predicate-object facts in canonical JSON | Internal candidate digests are not stable public fact IDs; expression vocabulary, source-field mapping, admission, promotion, bundle bytes, and artifact envelope remain separately governed |
| OD-006 | Three exact semantic roles in one closed composition and one v0 accepted-temporal epoch | No independent role heads, wire grammar, artifact schema, migration, or stable public fact IDs |
| OD-011 | One explicitly selected resolver profile, strict Malleus by default | Resolver capabilities default deny; adapters perform no hidden I/O and no fallback profile is tried |
| OD-013 | One future distribution with compiler and LinkML in the normal installation | This is a target topology, not a claim about current packaging or a LinkML-absent install |
| OD-014 | Quiet Bell Archive is the public working name and themed vocabulary stays fixture-only | The accepted text/data attestation covers no visual asset and creates no publication |

The operator also excluded migration feature development from the foundation
block. That is an execution-scope instruction, not approval to reuse an old
wire field with new meaning.

## Accepted compiler decisions from 2026-08-26

These choices are design authority. They do not implement a compiler, resolver,
wire reader, package split, fixture, or publication.

### OD-002: explicit adoption

Decision state: ACCEPTED, exact explicit adoption, 2026-08-26

Explicit adoption applies only to slot declarations. An adopting slot must
contain literal Boolean `annotations.adopts: true`. The imported ancestor
declaration remains the authoritative owner. Source or import order never
selects a winner.

Before comparison, remove only the declaration's top-level `description`, the
`annotations.adopts` member, and an `annotations` map left empty by that
removal. Compare the remaining typed source structure exactly. Every other
field, value type, collection, and presence state participates. The comparison
happens before LinkML defaults, coercion, or normalization.

Compilation refuses every non-slot duplicate, multiple independent owners, an
absent, null, false, or string `"true"` marker, any structural difference, and
an equal redeclaration without the marker. Description is deliberately the only
non-annotation field excluded from equality. The marker records intentional
reuse; it does not merge or override declarations.

The four CC-X02 groups therefore remain raw evidence, not an automatic global
merge. Only closure-local owner and import relationships determine whether an
occurrence is an adoption candidate.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-002`. `CC-D02` is complete.

### OD-003: semantic source when LinkML and legacy behavior differ

Decision state: ACCEPTED, replaceable LinkML adapter, 2026-08-26

Pinned LinkML 1.11.1 is the default first-party frontend adapter. An adapter is
replaceable behind the same explicit neutral compilation-result contract. Each
adapter identifies its implementation, version, support profile, and default
profile. Every adapter must pass the generic neutral-result metamodel,
canonicalization, artifact, and runtime conformance obligations. Each source
language has its own named, versioned support profile and source corpus. The
LinkML corpus is required only when an adapter claims LinkML compatibility.

Defaults are adapter inputs, like Python parameter defaults. Every default that
affects the result is materialized as an explicit neutral value with provenance.
The artifact-backed runtime never supplies a LinkML or adapter default. V0 does
not emulate legacy `OntologyRegistry` behavior.

The immutable CC-X01 cases are classified exactly:

| Case | Classification | V0 result |
|---|---|---|
| `simple_parity` | `EQUAL` | Preserve the equal meaning |
| `parent_mixin_precedence` | `LINKML` | Use pinned LinkML meaning |
| `repeated_mixin` | `REFUSE` | Unsupported even where the effective value happens to agree |
| `conflicting_mixins_ab` | `REFUSE` | No order-dependent winner |
| `conflicting_mixins_ba` | `REFUSE` | No order-dependent winner |
| `numeric_bounds` | `LINKML` | Use pinned LinkML meaning |
| `explicit_false` | `EQUAL` | Preserve explicit false |
| `default_range` | `LINKML` | Materialize the LinkML default explicitly with provenance |
| `attribute_slot_usage` | `LINKML` | Use pinned LinkML meaning |

`EQUAL` and `LINKML` classify the measured elaboration projection. They do not
promise that the later closed support profile and contract metamodel admit the
whole source. In particular, `explicit_false` still proves that the effective
`SlotUse` preserves authored `false`, while `OD-008` refuses that complete
source because its separate global String-valued `Slot` authors
`inlined=true`, which violates the immutable D05 range invariant.

Future public adapter code must document its supported declarations,
refusals, defaults, neutral outputs, and provenance in docstrings. Sphinx
surfaces those docstrings for developers; prose does not become a second
adapter contract.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-003`. `CC-D03` is complete.

### OD-004: persisted-wire transition

Decision state: ACCEPTED, typed hard break, 2026-08-26

The artifact-backed runtime uses a new persisted-wire epoch. It checks
the epoch before semantic decoding and returns a stable typed refusal for every
legacy input. `CC-W01` and the later diagnostic profile own the exact public
diagnostic identifier. The reader never reinterprets a legacy `ontology_hash`
as an effective-contract, consumer-bundle, or new wire identity.

There is no fallback, migration receipt, translation, replay bridge, or rewrite
in this transition. A historic reader may inspect old bytes as a separate tool;
it is not a fallback path inside the new reader. The frozen bytes stay evidence
and are never rewritten to make a test pass.

The selected CC-X04 outcome matrix is:

| Frozen logical subject | New reader result |
|---|---|
| Recon project | Typed persisted-wire epoch refusal |
| Recon record | Typed persisted-wire epoch refusal |
| Empty knowledge-graph snapshot | Typed persisted-wire epoch refusal |
| Protocol envelope | Typed persisted-wire epoch refusal before event replay |
| Embedded graph-base artifact | `NOT_REACHED` behind the envelope hard break |
| Embedded candidate artifact | `NOT_REACHED` behind the envelope hard break |

This deliberately gives up new-reader replay of the two inputs that the current
Recon reader accepts through its receipt. A later migration need creates a new
governed decision; it does not weaken this epoch boundary silently.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-004`. `CC-D04` is complete.

### OD-005: logical fact record and canonical bytes

Decision state: ACCEPTED, ontology-powered atomic facts, 2026-08-26

The neutral compiler seam is a closed atomic fact record with exactly three
members: `subject`, `predicate`, and `object`. The subject and predicate are
full absolute identifiers. The predicate determines whether the object is an
absolute identifier, Boolean, string, or canonical decimal lexical string.
There is no supplied fact ID and no coercion. Unknown members, unknown
predicates, bare or prefixed symbols, null, arrays, nested objects, and values
of the wrong predicate-declared type refuse.

The versioned `ContractMetamodel` is semantic authority. It defines legal
subject kinds and predicates, predicate object types and target kinds,
cardinalities, required structural relations, acyclicity where declared, and
whole-set invariants. JSON and any future JSON Schema define syntax only. A
syntactically valid JSON record forbidden by the exact metamodel refuses.

#### Exact non-expression seed metamodel

The seed namespace is `https://malleus.dev/contract-facts/`. It defines five
subject kinds: `Class`, `Slot`, `SlotUse`, `Enum`, and `Scalar`. Kind uses
`http://www.w3.org/1999/02/22-rdf-syntax-ns#type`; Class parent uses
`http://www.w3.org/2000/01/rdf-schema#subClassOf`. Malleus-specific predicates
use the seed namespace. The table abbreviates that namespace as `cf:` only for
readability; wire facts always carry the full absolute IRI.

Every fact subject has exactly one `rdf:type` kind fact. The following is the
complete accepted non-expression predicate set and cardinality table:

| Subject kind | Predicate | Object type or target | Cardinality |
|---|---|---|---|
| `Class` | `rdf:type` | exactly `Class` | 1 |
| `Class` | `rdfs:subClassOf` | `Class` | 0..1 |
| `Class` | `cf:isMixin` | Boolean | 1 |
| `Class` | `cf:usesMixin` | distinct `Class` with `isMixin=true` | 0..* |
| `Class` | `cf:abstract` | Boolean | 1 |
| `Slot` | `rdf:type` | exactly `Slot` | 1 |
| `Slot`, `SlotUse` | `cf:valueRange` | `Class`, `Enum`, `Scalar`, or `SeedPrimitive` | 1 |
| `Slot`, `SlotUse` | `cf:required` | Boolean | 1 |
| `Slot`, `SlotUse` | `cf:multivalued` | Boolean | 1 |
| `Slot`, `SlotUse` | `cf:identifier` | Boolean | 1 |
| `Slot`, `SlotUse` | `cf:inlined` | Boolean | 1 |
| `Slot`, `SlotUse` | `cf:equalsString` | string | 0..1 |
| `Slot`, `SlotUse` | `cf:minimum` | canonical decimal lexical string | 0..1 |
| `Slot`, `SlotUse` | `cf:maximum` | canonical decimal lexical string | 0..1 |
| `Slot`, `SlotUse` | `cf:valuePresence` | string `PRESENT` or `ABSENT` | 0..1 |
| `SlotUse` | `rdf:type` | exactly `SlotUse` | 1 |
| `SlotUse` | `cf:onClass` | `Class` | 1 |
| `SlotUse` | `cf:usesSlot` | `Slot` | 1 |
| `Enum` | `rdf:type` | exactly `Enum` | 1 |
| `Enum` | `cf:enumValue` | distinct string | 0..* |
| `Scalar` | `rdf:type` | exactly `Scalar` | 1 |
| `Scalar` | `cf:typeof` | `Scalar` or `SeedPrimitive` | 1 |

The five trusted `SeedPrimitive` target IRIs are exactly `String`, `Integer`,
`Float`, `Boolean`, and `DateTime` under the seed namespace. They are not XSD
aliases and are not fact subjects requiring kind facts.

The parent-plus-`usesMixin` graph is acyclic. Every `usesMixin` target has
`isMixin=true`; repeated authored mixins refuse before facts under `OD-003`.
The Scalar `typeof` graph is acyclic and terminates in exactly one seed
primitive. Every non-seed identifier target resolves in the same fact set.

Bounds are legal only when `valueRange` directly names `Integer` or `Float`, or
resolves through a Scalar chain terminating there, and `minimum` cannot exceed
`maximum`. `equalsString` is legal only when `valueRange` directly names
`String` or an Enum, or resolves through a Scalar chain terminating in
`String`. `inlined=true` is legal only for a Class range.
`valuePresence=ABSENT` conflicts with `required=true` and with `equalsString`.

A `Slot` can be an authoritative module-global declaration or a deterministic
qualified class-local declaration, so the accepted `attribute_slot_usage`
case is representable. The kind-specific predicate sets above are closed.
Metamodel validation proves internal structural completeness. Source-to-fact
completeness is separately proven by support-profile conformance and
independent oracles.

#### Canonical fact bytes

The candidate canonicalization profile emits one compact UTF-8 JSON array.
There is no byte-order mark, insignificant whitespace, or terminal newline.
Each record emits members in lexicographic order, `object`, `predicate`, then
`subject`. Records sort lexicographically by their complete canonical record
bytes. Input member and record order are nonsemantic.

JSON strings use `\"` and `\\` for quotation mark and reverse solidus, the
short escapes `\b`, `\t`, `\n`, `\f`, and `\r`, and lowercase `\u00xx` for
the remaining U+0000 through U+001F code points. Solidus and all other valid
Unicode scalar values remain unescaped and are encoded directly as UTF-8.
Lone surrogates and invalid UTF-8 refuse. Identifier code points are compared
exactly. No Unicode normalization, CURIE expansion, prefix map, base IRI, or
ambient context changes them.

Numeric predicates carry a canonical decimal lexical JSON string, never a raw
JSON number. Zero is `"0"`, including negative zero. Every other value has an
optional `-`, an integer part without leading zero, and, when nonintegral, a
fixed-point fraction with at least one digit and no trailing zero. Plus signs,
exponents, nonfinite values, and lossy rounding refuse. Thus source values `5`,
`5.0`, and `5e0` all produce object `"5"`. Predicate type distinguishes that
lexical value from an ordinary string or identifier. Boolean predicates use
JSON `true` or `false`; string `"true"` refuses.

The following is one complete metamodel-valid positive fact set in exact
canonical bytes. It contains class inheritance and a mixin, module-global slots,
a complete `SlotUse`, an enum value, a Scalar terminating in the String seed
primitive, and a numeric bound normalized to `"5"`:

```json
[{"object":"5","predicate":"https://malleus.dev/contract-facts/minimum","subject":"https://example.malleus.dev/domain/count"},{"object":"OPEN","predicate":"https://malleus.dev/contract-facts/enumValue","subject":"https://example.malleus.dev/domain/State"},{"object":"PRESENT","predicate":"https://malleus.dev/contract-facts/valuePresence","subject":"https://example.malleus.dev/domain/value"},{"object":"PRESENT","predicate":"https://malleus.dev/contract-facts/valuePresence","subject":"urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"},{"object":"https://example.malleus.dev/domain/BaseRecord","predicate":"http://www.w3.org/2000/01/rdf-schema#subClassOf","subject":"https://example.malleus.dev/domain/Record"},{"object":"https://example.malleus.dev/domain/Record","predicate":"https://malleus.dev/contract-facts/onClass","subject":"urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"},{"object":"https://example.malleus.dev/domain/ValueMixin","predicate":"https://malleus.dev/contract-facts/usesMixin","subject":"https://example.malleus.dev/domain/Record"},{"object":"https://example.malleus.dev/domain/value","predicate":"https://malleus.dev/contract-facts/usesSlot","subject":"urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"},{"object":"https://malleus.dev/contract-facts/Class","predicate":"http://www.w3.org/1999/02/22-rdf-syntax-ns#type","subject":"https://example.malleus.dev/domain/BaseRecord"},{"object":"https://malleus.dev/contract-facts/Class","predicate":"http://www.w3.org/1999/02/22-rdf-syntax-ns#type","subject":"https://example.malleus.dev/domain/Record"},{"object":"https://malleus.dev/contract-facts/Class","predicate":"http://www.w3.org/1999/02/22-rdf-syntax-ns#type","subject":"https://example.malleus.dev/domain/ValueMixin"},{"object":"https://malleus.dev/contract-facts/Enum","predicate":"http://www.w3.org/1999/02/22-rdf-syntax-ns#type","subject":"https://example.malleus.dev/domain/State"},{"object":"https://malleus.dev/contract-facts/Integer","predicate":"https://malleus.dev/contract-facts/valueRange","subject":"https://example.malleus.dev/domain/count"},{"object":"https://malleus.dev/contract-facts/Scalar","predicate":"http://www.w3.org/1999/02/22-rdf-syntax-ns#type","subject":"https://example.malleus.dev/domain/TextCode"},{"object":"https://malleus.dev/contract-facts/Slot","predicate":"http://www.w3.org/1999/02/22-rdf-syntax-ns#type","subject":"https://example.malleus.dev/domain/count"},{"object":"https://malleus.dev/contract-facts/Slot","predicate":"http://www.w3.org/1999/02/22-rdf-syntax-ns#type","subject":"https://example.malleus.dev/domain/value"},{"object":"https://malleus.dev/contract-facts/SlotUse","predicate":"http://www.w3.org/1999/02/22-rdf-syntax-ns#type","subject":"urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"},{"object":"https://malleus.dev/contract-facts/String","predicate":"https://malleus.dev/contract-facts/typeof","subject":"https://example.malleus.dev/domain/TextCode"},{"object":"https://malleus.dev/contract-facts/String","predicate":"https://malleus.dev/contract-facts/valueRange","subject":"https://example.malleus.dev/domain/value"},{"object":"https://malleus.dev/contract-facts/String","predicate":"https://malleus.dev/contract-facts/valueRange","subject":"urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"},{"object":false,"predicate":"https://malleus.dev/contract-facts/abstract","subject":"https://example.malleus.dev/domain/BaseRecord"},{"object":false,"predicate":"https://malleus.dev/contract-facts/abstract","subject":"https://example.malleus.dev/domain/Record"},{"object":false,"predicate":"https://malleus.dev/contract-facts/abstract","subject":"https://example.malleus.dev/domain/ValueMixin"},{"object":false,"predicate":"https://malleus.dev/contract-facts/identifier","subject":"https://example.malleus.dev/domain/count"},{"object":false,"predicate":"https://malleus.dev/contract-facts/identifier","subject":"https://example.malleus.dev/domain/value"},{"object":false,"predicate":"https://malleus.dev/contract-facts/identifier","subject":"urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"},{"object":false,"predicate":"https://malleus.dev/contract-facts/inlined","subject":"https://example.malleus.dev/domain/count"},{"object":false,"predicate":"https://malleus.dev/contract-facts/inlined","subject":"https://example.malleus.dev/domain/value"},{"object":false,"predicate":"https://malleus.dev/contract-facts/inlined","subject":"urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"},{"object":false,"predicate":"https://malleus.dev/contract-facts/isMixin","subject":"https://example.malleus.dev/domain/BaseRecord"},{"object":false,"predicate":"https://malleus.dev/contract-facts/isMixin","subject":"https://example.malleus.dev/domain/Record"},{"object":false,"predicate":"https://malleus.dev/contract-facts/multivalued","subject":"https://example.malleus.dev/domain/count"},{"object":false,"predicate":"https://malleus.dev/contract-facts/multivalued","subject":"https://example.malleus.dev/domain/value"},{"object":false,"predicate":"https://malleus.dev/contract-facts/multivalued","subject":"urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"},{"object":false,"predicate":"https://malleus.dev/contract-facts/required","subject":"https://example.malleus.dev/domain/count"},{"object":false,"predicate":"https://malleus.dev/contract-facts/required","subject":"https://example.malleus.dev/domain/value"},{"object":true,"predicate":"https://malleus.dev/contract-facts/isMixin","subject":"https://example.malleus.dev/domain/ValueMixin"},{"object":true,"predicate":"https://malleus.dev/contract-facts/required","subject":"urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b"}]
```

The array contains 38 facts and 6,244 bytes. Its SHA-256 is
`31db4d651f7a90f86466141193d806a5af58f8e09afa20dba838224b9361ca74`.

#### Structural and semantic identity

Structural subjects use a named, versioned, domain-separated SHA-256 URN.
`SlotUse` identity is the SHA-256 of these exact canonical envelope bytes:

```json
{"class":"https://example.malleus.dev/domain/Record","domain":"malleus.contract-structure.slot-use/v0","slot":"https://example.malleus.dev/domain/value"}
```

The resulting example subject is
`urn:malleus:contract-structure:slot-use:v0:sha256:5fc2d89b8614ce6fdc915e0e9fe735e22660e480afab71d26dc1329760b6452b`
in the complete array. The
identity binds only the qualified class, qualified slot, domain, and version,
never mutable constraints. Each `SlotUse` has exactly one `onClass` and one
`usesSlot`. Core v0 emits no redundant inverse `hasUse` fact. Explicitly
adopted slots retain the imported owner's qualified slot identifier; no local
copy fact is created.

An internal candidate fact digest hashes the canonical JSON envelope with
members `canonicalization_profile`, `domain`, `fact`, `metamodel`, and
`symbol_policy`. Its domain is `malleus.contract-fact/candidate-v0`; `fact` is
the canonical three-member record. An internal candidate fact-set digest hashes
the corresponding envelope whose domain is
`malleus.contract-fact-set/candidate-v0` and whose `facts_sha256` member is the
lowercase SHA-256 digest of the exact sorted canonical fact-array bytes. Both
envelopes bind the exact content-addressed metamodel identity, candidate
canonicalization-profile identity, and exact symbol-policy identity. These
digests are computed, never supplied as a fourth fact member. They are internal
candidate identities only. `OD-008` completes their expression-capable
metamodel inputs. Stable public identifiers still require the promotion
decision at `OD-009`.

#### Whole-set validation and provenance

Validation is atomic over the whole fact set. It checks completeness,
predicate cardinality, object and target kind, required structural relations,
declared acyclicity, exact duplicate records, and contradictions. An exact
duplicate subject-predicate-object record refuses. Two distinct values for a
maximum-cardinality-one predicate refuse. A multivalued predicate accepts
distinct values only.

Multiple derivations may converge on one semantic fact. All derivation
provenance remains separately retained. A source default is emitted as an
explicit fact. Equivalent implicit and explicit defaults therefore yield the
same fact and internal candidate digest while retaining different provenance.
Descriptions, source spans, diagnostics, compiler identity, and provenance do
not affect semantic fact-set identity. A description-only edit leaves the
canonical facts unchanged.

A LinkML adapter and an independently owned direct-fact conformance input for
this example must produce the same 38 metamodel-valid facts and the same exact
canonical bytes. The direct form remains bootstrap and conformance input, not
a public or second first-party authoring language and not a bypass around
`OD-009`.

An omitted LinkML range that the accepted adapter default profile resolves to
String and an explicit String range both emit the same ordinary `valueRange`
fact shown above. Their derivation records remain distinct outside the fact
set. There is no generic `defaultValue` fact and no instance-default semantics
in this seed. Changing only a description changes retained source and
annotation provenance, but neither the facts nor canonical fact-array bytes.

Counterexamples refuse a bare symbol, string `"true"` for a Boolean predicate,
a raw JSON number, unknown predicate or member, incomplete `SlotUse`, duplicate
fact, conflicting single-valued facts, null, array, nested object, nonfinite or
noncanonical decimal wire value, a predicate illegal for the subject kind, a
fact that tries to declare a seed primitive as a normal subject, a cycle, a
`usesMixin` target whose `isMixin` fact is false, a bound on a nonnumeric
range, `minimum` greater than `maximum`, `equalsString` on a
non-String/non-Enum range, `inlined=true` on a non-Class range,
`valuePresence=ABSENT` with `required=true` or `equalsString`, and every
unclassified expression. Record and member order canonicalize to the same
bytes. An adapter that cannot preserve an exact supported numeric value refuses
rather than rounding.

`OD-008` now maps source fields to this exact seed and adds one separately
versioned, closed expression extension. It does not change the seed. No
expression predicate outside that exact extension is accepted. Bootstrap
trusts one exact versioned seed `ContractMetamodel` at the boundary; it makes no
recursive self-validation or shipped self-hosting claim.
`NormativeAdmissionProfile` separately owns missing, null, reference, context,
and state-transition behavior. Turtle remains a readable design projection,
never the normative runtime wire.

`OD-006` closes roles and composition; `OD-007` and `OD-010` still own
admission and context; `OD-008` field and expression classification; `OD-009` public
promotion; `CC-D16` consumer-bundle bytes; and `CC-R07` and `CC-W01` the
artifact envelope and persisted epoch. Diagnostic codes, module layout, and
public APIs also remain open. This decision creates no compiler, public
frontend, metamodel file, artifact, reader, package, or dependency.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-005`. `CC-D05` is complete.

### OD-006: closed contract roles and composition

Decision state: ACCEPTED, three roles in one closed composition, 2026-08-26

Protocol records, governed domain data, and governance policy occupy three
different semantic roles. They do not share one indivisible contract and they
do not advance through independent heads in v0. The accepted full composition
has exactly these fixed slots, each with cardinality `1..1`:

| Fixed role | Complete contract governed by the role |
|---|---|
| `ProtocolRecordContract` | Protocol records, events, transitions, and ledger-facing protocol semantics |
| `GovernedGraphContract` | Governed domain records, relations, fields, and structural graph semantics |
| `GovernanceContract` | Authorization and governance-policy semantics |

Each slot binds one complete `EffectiveContract` identity. A role contract is
not a namespace label, overlay, patch, or partial view. Its effective contract
contains its complete validated fact-set and normative admission-profile
identities. Shared foundation declarations may occur independently in more
than one complete closure. No role borrows a declaration, fact, profile,
registry, ambient context, default, or fallback from another role.

#### Logical identity inputs

The role-bound identity is domain-separated by the fixed role. Its logical
input tuple is:

```text
RoleBoundContractIdentity(
  fixed logical token: malleus.contract-role-bound-identity/v0,
  fixed_role_name,
  exact_effective_contract_identity
)
```

The `fixed_role_name` is exactly one of the three names above. It is part of
identity, not presentation metadata. Two roles remain non-interchangeable even
when their underlying effective-contract payloads or identities are equal.
Substituting a valid effective-contract identity therefore creates a different
role-bound identity; supplying only a bare effective-contract hash is
insufficient.

`ContractComposition` is closed. Its logical identity tuple is:

```text
ContractCompositionIdentity(
  fixed logical token: malleus.contract-composition-identity/v0,
  ProtocolRecordContract_role_identity,
  GovernedGraphContract_role_identity,
  GovernanceContract_role_identity
)
```

The two versioned domain tokens are fixed by this decision and are not caller
parameters. Their future lexical encoding inside an artifact, bundle, or
persisted record remains with `CC-D16`, `CC-R07`, and `CC-W01`.

The fixed names make these slots ordered by meaning, not by source or map
iteration order. There is no fourth role, extension role, unknown-member
preservation, inferred current role, or optional slot in the v0 full
composition. These are candidate logical identity inputs, not a persisted
record, consumer-bundle schema, artifact envelope, canonical byte grammar, or
stable public identifier. `CC-D16`, `CC-R07`, and `CC-W01` retain those wire
decisions. `OD-008` completes the candidate fact-identity inputs; `OD-009`
still owns public promotion and identifier publication.

One physical artifact may package all three complete role contracts. The split
is semantic modularity, not three packages, installations, processes, ledgers,
or compiler invocations.

#### One accepted-temporal epoch

The v0 accepted-temporal path binds one exact `ContractComposition` identity
when its protocol ledger epoch begins. A change to any one role-bound identity
changes the composition identity and starts a new epoch. The old epoch cannot
continue under the new composition, and the new composition cannot be treated
as compatible with the old epoch by fallback, inferred latest state, partial
roll-forward, or a cross-bound role head.

On the accepted-temporal path, a new role value is legal only through a newly
constructed composition and a new epoch. It is not legal as an in-place
replacement under an already-bound epoch.

V0 has no independently advancing role heads, synchronization protocol,
cross-head replay, mixed-epoch recovery, migration machinery, or compatibility
relaxation. `CC-W01` later owns persisted epoch fields, exact bytes, and typed
refusal details; it cannot weaken this identity boundary.

The only narrower case is a standalone structural graph. It binds exactly one
`GovernedGraphContract` role identity plus its structural-state identity. It
has no protocol ledger, no accepted-temporal status, no protocol or governance
role slot, and no `ContractComposition` identity. This does not make any slot
optional in a full composition. An accepted-temporal graph bound only to the
governed-graph role refuses, as does a standalone structural graph carrying a
protocol ledger or full composition.

#### Positive delta examples

| Change | Protocol role | Governed-graph role | Governance role | Composition | Accepted-temporal epoch |
|---|---|---|---|---|---|
| Presentation or provenance only | same | same | same | same | same |
| Protocol semantic edit | changed | same | same | changed | new |
| Domain semantic edit | same | changed | same | changed | new |
| Governance semantic edit | same | same | changed | changed | new |

A domain-only edit therefore does not pretend that protocol or governance
semantics changed. It still changes the full composition and starts a new
accepted-temporal epoch. The corresponding standalone structural-graph case
changes only its governed-graph role and structural snapshot; it has no ledger
epoch. One artifact may package all three roles without collapsing their
identities. A future consumer bundle may reference one exact composition, but
`CC-D16` still owns the exact bundle fields and bytes.

#### Refusal examples

Composition refuses atomically when a role is missing, duplicated, unknown,
or supplied more than once; when protocol and governed-graph slots are
swapped; when a role tag, version, or identity domain is wrong; when an
already-bound epoch is continued with a valid replacement role identity but no
new composition is constructed and bound; when roles from different
compositions are mixed without constructing a new composition; or when equal
payload is treated as proof that two roles are interchangeable.

It also refuses an incomplete role closure that relies on ambient declarations
or another role, a protocol contract used to validate governed domain state, a
governed-graph contract used to validate protocol records, an independently
advanced or borrowed role head, continuation of a ledger after composition
change, and any inferred latest or current composition. A structural-only
graph refuses protocol or governance roles, a composition identity, or a
protocol ledger. An accepted-temporal graph refuses a structural-only binding.
Whole-composition validation refuses atomically; no subset is accepted.

`OD-006` defines role and composition structure only. `OD-007` owns governance
storage topology; `OD-010` owns endpoint, reference, context, and stateful
admission semantics; `OD-008` owns source-field and expression classification;
`OD-009` owns public promotion and identifier publication;
`CC-D16` owns the consumer-bundle grammar; `CC-R07` owns the reloadable
artifact envelope; and `CC-W01` owns persisted wire, migration, and exact epoch
encoding. This decision creates no implementation, ontology YAML, package,
artifact, bundle, public API, or migration mechanism.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-006`. `CC-D06` is complete.

### OD-008: closed LinkML v0 support profile

Decision state: ACCEPTED, exact KISS subset and flat exactly-one extension, 2026-08-26

Malleus does not claim general LinkML support. The first compiler adapter accepts
one closed, versioned subset exercised by current Malleus semantics and the
governed conformance corpus. This keeps the neutral facts deterministic, keeps
LinkML semantics out of the runtime, and keeps another frontend replaceable at
the same neutral boundary. Fail-closed classification also makes an upstream
LinkML feature addition visible instead of silently changing a contract.

Every source member is classified by its exact location. The four classes are
exhaustive and disjoint:

* `ENFORCED` changes elaboration or emits ordinary semantic facts.
* `IDENTITY_ONLY` establishes a module, declaration, reference, or authoritative
  owner, but emits no fact solely for that source member.
* `ANNOTATION_ONLY` is retained as queryable projection and provenance metadata
  and is excluded from semantic facts and `EffectiveContract` identity.
* `REJECTED` refuses the whole compilation.

Anything absent from the exact table at its exact location is `REJECTED`.
Moving an accepted field or annotation to another location does not preserve
support. A parser branch alone cannot expand this profile.

#### Exact location classification

The notation `map key` means the authored key identifying one declaration or
condition. Reference values inside an enforcing container remain
`IDENTITY_ONLY`, while the container's structure is `ENFORCED`.

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

At every location, unknown fields and unknown annotations refuse. In
particular, `annotations.retires`, `range_expression`, `rules`, `unique_keys`,
patterns, cardinality constructs outside the exact table, `any_of`, `all_of`,
`none_of`, and all broad or unearned LinkML constructs refuse. Repeated or
conflicting mixins refuse. Duplicate declarations refuse except for the exact
`OD-002` adopted imported global-slot redeclaration.

#### Exact raw source grammar and symbols

The adapter inspects the duplicate-key-preserving typed YAML source before it
constructs any LinkML object. V0 accepts exactly one mapping document and no
YAML directive or document-boundary marker. Its value tree is JSON-shaped.
Duplicate mapping keys, aliases, anchors, merge keys, all explicit YAML tags,
including core tags such as `!!str`, non-string mapping keys, and implicit
LinkML coercion refuse. At a permissible-value body,
only the empty plain scalar after `:` and lowercase plain `null` denote the same
empty declaration. `~`, title-case or uppercase null, and null anywhere else
refuse. These raw value rules are exact:

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

The exact bound lexeme grammar is:

```text
number = ["-"] integer [fraction] [exponent]
integer = "0" | nonzero-digit {digit}
fraction = "." digit {digit}
exponent = ("e" | "E") ["+" | "-"] digit {digit}
```

The token contains no whitespace. It is read from the raw source before YAML
tag resolution, so `5e0` is numeric even though PyYAML 6.0.3 would tag it as a
string. Canonicalization uses D05 arbitrary-precision decimal rules, never a
binary float.

| Lexeme class | Exact examples | Result |
|---|---|---|
| accepted | `0`, `-0`, `5`, `5.0`, `5e0`, `5E-2`, `1e+3`, `-12.34` | parse exactly, then canonicalize under D05 |
| refused | `+1`, `01`, `0x10`, `1_0`, `1:20`, `.5`, `1.`, `.inf`, `.nan`, quoted `"1"` | not in the exact grammar |

Declaration, class-local attribute, and prefix keys use one closed ASCII
grammar: the first character is a letter or underscore and every later
character is a letter, digit, or underscore. A permissible-value key is any
nonempty string and emits that exact string as `cf:enumValue`.

Schema `id` is the semantic module IRI. Schema IDs and prefix values must be
absolute RFC 3987 IRIs with a nonempty scheme. A literal code point whose
Unicode general category is `Cc` or `Cs` refuses before format validation.
Schema `id` additionally has no query, fragment, or trailing slash.
A module-global declaration key `K` has the
qualified symbol `schema-id + "/" + K`. A class-local attribute key `A` on
qualified class `C` has the qualified symbol `C + "/" + A`. These are exact
string joins. There is no escaping, case folding, Unicode normalization, path
normalization, or caller-selected base. The key grammar makes the slash
boundaries unambiguous.

A bare reference resolves to exactly one authoritative declaration in the
retained import closure. A prefixed reference expands by exact concatenation of
the retained prefix value and suffix, then must resolve to that same
authoritative declaration. Unknown, ambiguous, or differently qualified
references refuse. The D02 adopted imported global slot is the only duplicate
ownership exception. `name` and `version` remain module metadata only: changing
either preserves qualified semantic symbols, facts, and candidate fact
identities while changing source attestation. Prefixes affect semantic identity
only when a retained reference uses them.

The exact internal symbol-policy identity bound by D05 candidate fact and
fact-set envelopes is
`urn:malleus:contract-symbol-policy:linkml-v0-slash-qualified:v0`. It covers the
key grammar, slash joins, prefix expansion, authoritative resolution, and D02
ownership exception above. It is an internal v0 identity, not D09 public
namespace or stable-ID promotion.

Each permissible-value key is `ENFORCED` because it emits one `cf:enumValue`
fact. Null means an empty value declaration, not a semantic null. Null is
rejected everywhere else in this profile.

#### Trusted LinkML builtins

The exact authored import `linkml:types` selects one trusted builtin lookup map.
It does not admit upstream `types.yaml` as ordinary user source. The map is
bound to `linkml-runtime==1.11.1`, retained root wheel
`linkml_runtime-1.11.1-py3-none-any.whl` with SHA-256
`b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da`,
member `linkml_runtime/linkml_model/model/schema/types.yaml`, exactly 7,296
member bytes, and member SHA-256
`1c79b264397bec0eadb404d22e9b163458f1b889809b3b482ecc39c98743fe00`.
A mismatch refuses. D11 provenance retains the authored import, exact resolved
source, wheel identity, member path, length, digest, and profile identity.

The case-sensitive map has exactly seven names:

| LinkML source name | Neutral target | Additional facts when referenced |
|---|---|---|
| `string` | `cf:String` | none; trusted D05 seed target |
| `integer` | `cf:Integer` | none; trusted D05 seed target |
| `float` | `cf:Float` | none; trusted D05 seed target |
| `boolean` | `cf:Boolean` | none; trusted D05 seed target |
| `datetime` | `cf:DateTime` | none; trusted D05 seed target |
| `date` | `https://w3id.org/linkml/types/date` | `rdf:type cf:Scalar`; `cf:typeof cf:String` |
| `uri` | `https://w3id.org/linkml/types/uri` | `rdf:type cf:Scalar`; `cf:typeof cf:String` |

`date` and `uri` retain distinct range identities without claiming LinkML
lexical validation. Their two ordinary Scalar facts appear in the same fact set
when referenced. Every other upstream builtin or declaration refuses unless it
is separately declared by valid ordinary source under this profile.

#### Exact neutral mapping

Schema containers and import closure establish the declarations to compile.
The exact v0 omitted-value matrix is:

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

The pinned LinkML identifier-based `inlined` derivation runs during exact
elaboration, before ordinary missing-value fill. More than one effective
identifier slot on the target Class refuses. Explicit `inlined` remains
explicit; D05 still refuses `inlined=true` on a non-Class range.

Defaults apply only after exact LinkML 1.11.1 elaboration. The class-ancestor
closure uses this exact pinned traversal:

```text
ancestors = [class]
stack = [class]
visited = []
while stack is not empty:
  current = stack.pop_last()
  visited.append(current)
  for parent in authored_mixins_then_is_a(current):
    if parent is absent from visited and ancestors:
      stack.append(parent)
      ancestors.append(parent)
apply slot_usage for each class in reverse(ancestors)
```

Every parent resolves first and the closure must be acyclic. A local attribute
is the base instead of a same-named global slot. The base declaration is copied,
then each applicable `slot_usage` source in the exact reversed closure updates
it, ending with the class itself. Explicit `false` is present and overrides.
Repeated authored mixins and distinct explicitly present single-valued
`ENFORCED` values for the same slot field from two applicable mixin sources
refuse before order can pick a winner. Annotation-only differences never cause
that refusal. Every authored description remains separately retained, and no
effective semantic description winner is selected. Numeric bounds are the one
merge exception: elaboration
chooses the greatest minimum and least maximum across base and applicable
sources, then applies D05 range and ordering invariants. Effective `identifier=true` forces
effective `required=true`; an explicit `required=false` on that same effective
slot refuses as a contradiction. Every applied or filled default is
an ordinary D05 fact with separate derivation provenance. Explicit `false` is
preserved. A defaulted value and the equivalent explicit value produce the
same semantic fact and candidate fact identity, but different source and
provenance attestations.

The immutable CC-X01 `explicit_false` vector remains `EQUAL` evidence for its
measured effective `SlotUse`, including all four authored `false` values. The
whole source nevertheless refuses in D08 because its separate global Slot has
String range with `inlined=true`, forbidden by D05. A distinct positive vector
uses a String global Slot and class `slot_usage` with literal `false` for
`required`, `multivalued`, `identifier`, and `inlined`; it compiles to the same
four false facts with exact explicit-value provenance.

The distinct positive vector is exact:

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

The retained conformance corpus has these exact D08 outcomes:

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

Type `typeof`, enum permissible-value keys, class `is_a`, `mixin`, `mixins`,
and `abstract`, and all supported slot constraint fields map to the exact D05
seed predicates and invariants. Class `slots`, local `attributes`, and
`slot_usage` retain distinct lossless declaration evidence before producing
their effective neutral `Slot`, `SlotUse`, and constraint facts. References
resolve to exact qualified identities before facts are emitted. Adoption maps
to the imported authoritative slot owner and emits no adoption fact.

Every distinct applicable class slot produces exactly one `SlotUse`. A local
attribute declares a deterministic qualified class-local `Slot` and its
`SlotUse`. A `slots` reference resolves to an authoritative global, inherited,
or adopted slot and produces its class `SlotUse`. Parent and mixin slots remain
applicable under the selected elaboration rules. A `slot_usage` key must resolve
to an already applicable slot; it can refine that `SlotUse` but cannot introduce
a slot or disappear silently. Duplicate `slots` references, a duplicate
attribute/reference for the same class-local use, and ambiguous applicable
owners refuse.

`title`, every listed `description`, `class_uri`, and type `uri` remain retained
and queryable outside semantic facts. Erasing or changing only those members
preserves the fact set, candidate fact identities, role-bound identity, and
composition identity. It changes retained source and provenance attestation.

#### Versioned exactly-one expression extension

The immutable `ExactNonExpressionSeedContractMetamodel` from D05 is not edited.
`FlatExactlyOneExpressionExtensionV0` is composed with that exact seed to
produce the named combined `ExpressionCapableContractMetamodelV0` identity.
The extension adds exactly three structural kinds:

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

Every group has one class and one or more alternatives. Every alternative
belongs to one group and has one or more conditions. Every condition belongs to
one alternative, uses one authoritative qualified slot that has an applicable
effective `SlotUse` on the group's declaring class, and carries at least one of
the three optional condition predicates. The condition fact points to the
authoritative `Slot`; applicability and range checks use that declaring-class
`SlotUse`. `equalsString` is legal only when the effective range directly names
String or an Enum, or resolves through a Scalar chain terminating in String,
exactly as in D05. Inside one condition,
`valuePresence=ABSENT` conflicts with `required=true` and with any
`equalsString`. No cross-branch or cross-group satisfiability analysis is
performed, and no other base-slot or branch narrowing is declared
contradictory.

Each class has at most one directly declared group. That group is reified
exactly once on its declaring class. A descendant applies every ancestor group
plus its local group conjunctively through the same accepted class-ancestor
closure; inherited groups are not copied or reidentified on the descendant.
There is no source-order winner.

#### Exact internal metamodel identities

The D05 table is immutable. D08 gives that exact table and its already accepted
invariants a content identity without changing either. Metamodel envelope arrays
sort their complete canonical JSON member bytes. Every invariant object binds
both its stable mnemonic `id` and its exact normative `rule`; the mnemonic alone
has no authority. Structural-identity profile objects bind the exact envelope
domain, member set, SHA-256 encoding, output prefix, and any sorted-array rule.
Each member of the envelope's `rules` array is the exact D05 or D08 table row
with Markdown backticks removed and its `cf:`, `rdf:type`, or
`rdfs:subClassOf` predicate cell expanded to the full absolute IRI before
hashing. The invariant propositions remain the exact strings shown in their
`rule` members. The seed envelope is:

```json
{"domain":"malleus.contract-metamodel/non-expression-seed/v0","invariants":[{"id":"absent-conflicts-with-required-true-or-equals-string","rule":"valuePresence=ABSENT refuses when required=true or equalsString is present on the same Slot or SlotUse."},{"id":"atomic-whole-fact-set-validation","rule":"Validation accepts or refuses the complete supplied fact set atomically; it never returns or accepts a valid subset after any violation."},{"id":"class-parent-and-mixin-graph-acyclic","rule":"The union of rdfs:subClassOf and cf:usesMixin edges between Class subjects is acyclic."},{"id":"enforced-kind-predicate-cardinality-and-whole-set-completeness","rule":"Every fact subject has exactly one rdf:type kind fact and exactly the closed kind-specific predicate cardinalities in the active metamodel's rules; no other kind or predicate is legal."},{"id":"equals-string-only-string-resolving-or-enum-range","rule":"On a Slot or SlotUse subject, cf:equalsString is legal only when cf:valueRange directly names cf:String or an Enum, or resolves through a Scalar chain terminating in cf:String."},{"id":"every-non-seed-identifier-target-resolves-in-fact-set","rule":"Every object of rdfs:subClassOf, cf:usesMixin, cf:typeof, cf:valueRange, cf:onClass, or cf:usesSlot resolves to a fact subject in the same whole fact set, except an allowed SeedPrimitive object of cf:typeof or cf:valueRange."},{"id":"exact-duplicate-fact-record-refuses","rule":"An exact duplicate subject-predicate-object fact record refuses the whole fact set; convergent derivation provenance remains outside the fact set."},{"id":"inlined-true-only-class-range","rule":"cf:inlined=true is legal only when cf:valueRange names Class."},{"id":"numeric-bounds-only-integer-or-float-and-minimum-not-greater-than-maximum","rule":"cf:minimum and cf:maximum are legal only when cf:valueRange directly names cf:Integer or cf:Float, or resolves through a Scalar chain terminating in cf:Integer or cf:Float, and minimum cannot exceed maximum."},{"id":"scalar-typeof-acyclic-and-terminates-in-seed-primitive","rule":"The Scalar cf:typeof graph is acyclic and every path terminates in exactly one of the five SeedPrimitive targets."},{"id":"seed-primitives-are-targets-not-fact-subjects","rule":"The five SeedPrimitive IRIs are trusted targets and cannot occur as fact subjects."},{"id":"uses-mixin-target-has-is-mixin-true","rule":"Every cf:usesMixin object resolves to a Class subject in the same whole fact set whose cf:isMixin object is true."}],"primitives":["Boolean","DateTime","Float","Integer","String"],"rules":[["Class","http://www.w3.org/1999/02/22-rdf-syntax-ns#type","exactly Class","1"],["Class","http://www.w3.org/2000/01/rdf-schema#subClassOf","Class","0..1"],["Class","https://malleus.dev/contract-facts/abstract","Boolean","1"],["Class","https://malleus.dev/contract-facts/isMixin","Boolean","1"],["Class","https://malleus.dev/contract-facts/usesMixin","distinct Class with isMixin=true","0..*"],["Enum","http://www.w3.org/1999/02/22-rdf-syntax-ns#type","exactly Enum","1"],["Enum","https://malleus.dev/contract-facts/enumValue","distinct string","0..*"],["Scalar","http://www.w3.org/1999/02/22-rdf-syntax-ns#type","exactly Scalar","1"],["Scalar","https://malleus.dev/contract-facts/typeof","Scalar or SeedPrimitive","1"],["Slot","http://www.w3.org/1999/02/22-rdf-syntax-ns#type","exactly Slot","1"],["Slot, SlotUse","https://malleus.dev/contract-facts/equalsString","string","0..1"],["Slot, SlotUse","https://malleus.dev/contract-facts/identifier","Boolean","1"],["Slot, SlotUse","https://malleus.dev/contract-facts/inlined","Boolean","1"],["Slot, SlotUse","https://malleus.dev/contract-facts/maximum","canonical decimal lexical string","0..1"],["Slot, SlotUse","https://malleus.dev/contract-facts/minimum","canonical decimal lexical string","0..1"],["Slot, SlotUse","https://malleus.dev/contract-facts/multivalued","Boolean","1"],["Slot, SlotUse","https://malleus.dev/contract-facts/required","Boolean","1"],["Slot, SlotUse","https://malleus.dev/contract-facts/valuePresence","string PRESENT or ABSENT","0..1"],["Slot, SlotUse","https://malleus.dev/contract-facts/valueRange","Class, Enum, Scalar, or SeedPrimitive","1"],["SlotUse","http://www.w3.org/1999/02/22-rdf-syntax-ns#type","exactly SlotUse","1"],["SlotUse","https://malleus.dev/contract-facts/onClass","Class","1"],["SlotUse","https://malleus.dev/contract-facts/usesSlot","Slot","1"]],"seed_namespace":"https://malleus.dev/contract-facts/","structural_identity_canonicalization":"malleus.canonical-json/d05-compact-sorted-key-utf8-no-newline/v0","structural_identity_profiles":[{"digest_encoding":"lowercase-hex","domain":"malleus.contract-structure.slot-use/v0","hash":"sha256","members":["class","domain","slot"],"output_prefix":"urn:malleus:contract-structure:slot-use:v0:sha256:"}]}
```

Its 4,819 UTF-8 bytes yield
`urn:malleus:contract-metamodel:non-expression-seed:v0:sha256:1c68a612f3e7a0f80c31965aa5525954921dfbee60d151552d10d61cb0aac71b`.
The expression-extension envelope is:

```json
{"domain":"malleus.contract-metamodel/flat-exactly-one-extension/v0","invariants":[{"id":"alternative-has-one-or-more-conditions","rule":"Every ExactlyOneAlternative belongs to one ExactlyOneGroup and has one or more SlotCondition subjects."},{"id":"condition-equals-string-uses-d05-effective-slot-use-range-rule","rule":"SlotCondition cf:equalsString is legal only when the declaring-class effective SlotUse range directly names cf:String or an Enum, or resolves through a Scalar chain terminating in cf:String."},{"id":"condition-has-one-or-more-enforcing-members","rule":"Every SlotCondition has at least one of cf:required, cf:equalsString, or cf:valuePresence."},{"id":"condition-slot-has-applicable-effective-slot-use-on-declaring-class","rule":"Every SlotCondition cf:usesSlot target has an applicable effective SlotUse on the ExactlyOneGroup declaring Class."},{"id":"declaring-class-group-reified-once-and-inherited-conjunctively-without-copy","rule":"Each Class has at most one directly declared ExactlyOneGroup; that group is reified once on its declaring Class; descendants apply ancestor and local groups conjunctively without copied or reidentified groups."},{"id":"duplicate-semantic-alternatives-and-conditions-refuse","rule":"Duplicate semantic alternatives in one group and duplicate authoritative-slot conditions in one alternative refuse the whole fact set."},{"id":"group-and-alternative-structural-targets-resolve-in-whole-fact-set","rule":"Every cf:inGroup object resolves in the same whole fact set to ExactlyOneGroup, and every cf:inAlternative object resolves there to ExactlyOneAlternative."},{"id":"group-has-one-or-more-alternatives","rule":"Every ExactlyOneGroup names one Class and has one or more ExactlyOneAlternative subjects."},{"id":"only-flat-class-exactly-one-of","rule":"Only flat class exactly_one_of is legal; nested, any_of, all_of, and none_of forms refuse, and no cross-branch or cross-group satisfiability analysis occurs."},{"id":"semantic-order-independent-structural-identities","rule":"Branch, condition, and member order does not change structural envelopes, subjects, or canonical facts; source indexes never enter identity."},{"id":"value-presence-absent-conflicts-with-required-true-or-equals-string","rule":"Within one SlotCondition, cf:valuePresence ABSENT refuses with cf:required true or any cf:equalsString."}],"rules":[["ExactlyOneAlternative","http://www.w3.org/1999/02/22-rdf-syntax-ns#type","exactly ExactlyOneAlternative","1"],["ExactlyOneAlternative","https://malleus.dev/contract-facts/inGroup","ExactlyOneGroup","1"],["ExactlyOneGroup","http://www.w3.org/1999/02/22-rdf-syntax-ns#type","exactly ExactlyOneGroup","1"],["ExactlyOneGroup","https://malleus.dev/contract-facts/onClass","Class","1"],["SlotCondition","http://www.w3.org/1999/02/22-rdf-syntax-ns#type","exactly SlotCondition","1"],["SlotCondition","https://malleus.dev/contract-facts/equalsString","string","0..1"],["SlotCondition","https://malleus.dev/contract-facts/inAlternative","ExactlyOneAlternative","1"],["SlotCondition","https://malleus.dev/contract-facts/required","Boolean","0..1"],["SlotCondition","https://malleus.dev/contract-facts/usesSlot","authoritative qualified Slot","1"],["SlotCondition","https://malleus.dev/contract-facts/valuePresence","string PRESENT or ABSENT","0..1"]],"seed_namespace":"https://malleus.dev/contract-facts/","semantic_member_profiles":[{"minimum_optional_members":1,"name":"slot-condition-semantics","optional_members":["equalsString","required","valuePresence"],"required_members":["slot"]}],"structural_identity_canonicalization":"malleus.canonical-json/d05-compact-sorted-key-utf8-no-newline/v0","structural_identity_profiles":[{"digest_encoding":"lowercase-hex","domain":"malleus.contract-structure.exactly-one-alternative/v0","hash":"sha256","members":["alternative_semantic_digest","domain","group"],"output_prefix":"urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:"},{"digest_encoding":"lowercase-hex","domain":"malleus.contract-structure.exactly-one-group/v0","hash":"sha256","members":["alternative_semantic_digests","class","domain"],"output_prefix":"urn:malleus:contract-structure:exactly-one-group:v0:sha256:","sorted_arrays":{"alternative_semantic_digests":"canonical-json-string-bytes-ascending"}},{"digest_encoding":"lowercase-hex","domain":"malleus.contract-structure.slot-condition/v0","hash":"sha256","members":["alternative","domain","slot"],"output_prefix":"urn:malleus:contract-structure:slot-condition:v0:sha256:"},{"digest_encoding":"lowercase-hex","domain":"malleus.exactly-one-alternative-semantics/v0","hash":"sha256","members":["conditions","domain"],"output_prefix":"sha256:","sorted_arrays":{"conditions":"canonical-json-object-bytes-ascending"}}]}
```

Its 4,762 UTF-8 bytes yield
`urn:malleus:contract-metamodel:flat-exactly-one-extension:v0:sha256:99527d21040cbdda9dd7c579af7f40af8645de9b5f4b1e8ba28b40ddff7d53e6`.
Composition is role-bound, not a commutative component set. The operator makes
the active rules the exact closed union of the base and extension rule rows;
duplicate kind-predicate rows refuse composition. Both invariant sets apply
with their literal subject and whole-set quantifiers. An invariant reference to
active rules means that union, and a kind or predicate outside it refuses. Its
exact envelope is:

```json
{"base":"urn:malleus:contract-metamodel:non-expression-seed:v0:sha256:1c68a612f3e7a0f80c31965aa5525954921dfbee60d151552d10d61cb0aac71b","domain":"malleus.contract-metamodel/composition/v0","extension":"urn:malleus:contract-metamodel:flat-exactly-one-extension:v0:sha256:99527d21040cbdda9dd7c579af7f40af8645de9b5f4b1e8ba28b40ddff7d53e6","operator":"The active rules are the exact closed union of base.rules and extension.rules; duplicate kind-predicate rows refuse composition; both invariant sets apply with their literal subject and whole-set quantifiers; every invariant reference to active rules means that union; no other kind or predicate is legal."}
```

Its 655 UTF-8 bytes yield the combined
`ExpressionCapableContractMetamodelV0` identity
`urn:malleus:contract-metamodel:expression-capable:v0:sha256:65aae23b7a0892a4d2ae2b5adc6888f1ddd39c94ce03f412d50a6a5ccd5d0964`.
These are internal candidate identities used by D05 envelopes, not D09 public
identifiers. Reordering rules or invariants preserves the sorted envelope;
adding, removing, or changing semantic content changes the component and
combined identities.

Structural identity is semantic and order-independent. All envelopes use the
D05 compact, sorted-key UTF-8 canonical JSON grammar with no terminal newline.
A condition-semantics object contains exactly `slot` plus each present neutral
member from `required`, `equalsString`, and `valuePresence`. Conditions sort by
their canonical object bytes. The alternative-semantics envelope contains
exactly `conditions` and domain
`malleus.exactly-one-alternative-semantics/v0`. Its lowercase SHA-256 digest is
written as `sha256:<hex>`.

The group envelope contains exactly `alternative_semantic_digests`, `class`,
and domain `malleus.contract-structure.exactly-one-group/v0`. Alternative
digests sort lexically. The alternative envelope contains exactly
`alternative_semantic_digest`, `domain` equal to
`malleus.contract-structure.exactly-one-alternative/v0`, and `group`. The
condition envelope contains exactly `alternative`, `domain` equal to
`malleus.contract-structure.slot-condition/v0`, and `slot`. Each structural
subject is the lowercase SHA-256 of its exact envelope bytes under these
prefixes:

```text
urn:malleus:contract-structure:exactly-one-group:v0:sha256:<hex>
urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:<hex>
urn:malleus:contract-structure:slot-condition:v0:sha256:<hex>
```

These are internal candidate structural IDs, not published stable IDs.
Reordering branches, conditions, or their members preserves envelopes,
structural IDs, and canonical facts. Source indexes never enter identity. A
duplicate semantic branch, duplicate condition for one authoritative slot,
unknown slot, known but inapplicable slot, incompatible `equalsString` range,
empty group, empty branch, extra member, wrong value type, internal
contradiction, unsupported combinator, or nested expression refuses the whole
compilation.

A neutral positive example is a `ChoiceCarrier` class with one group containing
two alternatives: `left_value` present and `right_value` present. The exact alternative
semantics bytes are:

```json
{"conditions":[{"slot":"https://example.malleus.dev/domain/left_value","valuePresence":"PRESENT"}],"domain":"malleus.exactly-one-alternative-semantics/v0"}
```

```json
{"conditions":[{"slot":"https://example.malleus.dev/domain/right_value","valuePresence":"PRESENT"}],"domain":"malleus.exactly-one-alternative-semantics/v0"}
```

Their digests are respectively
`sha256:10f5b3992c471304ed0382e000f93ff6ef2aa0240bc1501dfae25e834267016a`
and
`sha256:1c8099c0364055a950dd2ff3eaecfbd4554fb8199ff3f0af2be0679d25d1bbb9`.
The exact group envelope is:

```json
{"alternative_semantic_digests":["sha256:10f5b3992c471304ed0382e000f93ff6ef2aa0240bc1501dfae25e834267016a","sha256:1c8099c0364055a950dd2ff3eaecfbd4554fb8199ff3f0af2be0679d25d1bbb9"],"class":"https://example.malleus.dev/domain/ChoiceCarrier","domain":"malleus.contract-structure.exactly-one-group/v0"}
```

It yields
`urn:malleus:contract-structure:exactly-one-group:v0:sha256:7c7fff294828d255018a04f67dfd0d2f86307867882e07866a25c1bfc7cca1f1`.
For the `left_value` branch, the exact alternative and condition envelopes are:

```json
{"alternative_semantic_digest":"sha256:10f5b3992c471304ed0382e000f93ff6ef2aa0240bc1501dfae25e834267016a","domain":"malleus.contract-structure.exactly-one-alternative/v0","group":"urn:malleus:contract-structure:exactly-one-group:v0:sha256:7c7fff294828d255018a04f67dfd0d2f86307867882e07866a25c1bfc7cca1f1"}
```

```json
{"alternative":"urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:15c008ee7b1dc89621e92acf93bb0f2d572102aa5430569af899e656da375b81","domain":"malleus.contract-structure.slot-condition/v0","slot":"https://example.malleus.dev/domain/left_value"}
```

They yield
`urn:malleus:contract-structure:exactly-one-alternative:v0:sha256:15c008ee7b1dc89621e92acf93bb0f2d572102aa5430569af899e656da375b81`
and
`urn:malleus:contract-structure:slot-condition:v0:sha256:7c973812ba4ba438f046cf89fd3038fe41a218c2fc4ebb0dd67b578a5a681e7a`.
The second branch follows the same exact rules. The bundled Assent `ValidTime`
expression is retained as real vertical evidence for the same shape. Its
themed names do not enter the core vocabulary.

#### Identity and expansion boundary

This decision freezes the expression-capable metamodel and exact
source-to-fact mapping needed by the D05 internal candidate digests. A change
to an enforcing field, symbol identity, qualified reference, or expression
semantic changes the affected facts and identities. Annotation-only and
provenance-only edits do not. D06 role and composition tags do not enter an
individual fact digest; role-bound and composition identities still prevent
cross-role interchange.

Expanding support requires one named use case or query, an operator decision,
an exact-location classification, mapping to the unchanged seed or a newly
versioned metamodel extension, explicit default and provenance behavior,
positive and refusal examples, independent source/direct-fact/oracle parity,
metamorphic identity tests, profile and metamodel version review, adapter
support-matrix documentation, and strict Sphinx verification. Unknown input
stays rejected until all gates land atomically.

Future work may construct or inject another frontend adapter at the existing
neutral boundary. D08 does not design a plugin framework, discovery mechanism,
registry, lifecycle, or public injection API. Any future adapter must declare
its implementation and version plus its exact support, default, and resolver
profiles, then pass the same neutral fact, metamodel, canonicalization,
provenance, artifact, runtime, direct-fact, and independent-oracle conformance
contract.

The Sphinx-rendered internal developer guide records that workflow. It is a
repository projection, not public adapter or API promotion. Decision records,
the metamodel, tests, and validated manifests remain authoritative. `CC-R02`
may later implement and characterize the adapter, but public docstrings,
namespace placement, stable public fact identifiers, and public support claims
remain blocked on `OD-009`.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-008`. `CC-D08` is complete.

### OD-011: resolver and import policy

Decision state: ACCEPTED, explicit replaceable resolver, 2026-08-26

Exactly one named and versioned resolver profile is selected for one
compilation. Strict Malleus resolution is the default. LinkML-compatible and
custom resolution are allowed only when the caller explicitly selects their
resolver identity and configuration. Failure never invokes a try-next resolver
chain.

The resolver remains the sole source of bytes. Frontend adapters perform no
hidden file or network I/O. File and network capabilities are separate explicit
resolver configuration and default to denied. A profile may apply its own
locator rules, such as a LinkML suffix rule, but it retains the exact resolved
locator string and, for imports, the separate authored literal.

Within one compilation, `ModuleInstance` identity is the exact retained
resolved locator string. There is no universal locator normalization. Resolver
profile and configuration identity are separate compilation provenance. The
root has one retained locator/source record. Only an import edge carries its
parent module, authored ordinal, literal import, and child resolved locator.
Every retained source also records exact bytes, byte length, digest, and media
type.

The same module locator with different bytes refuses compilation. Different
locators with identical bytes remain distinct module observations, although an
implementation may deduplicate their content blob. Authored order is retained
as provenance only and never selects a semantic winner. Every directed import
cycle refuses with its lineage.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-011`. `CC-D11` is complete.

### OD-013: packaging topology

Decision state: ACCEPTED, one distribution, 2026-08-26

The selected target is one distribution. A normal future
`pip install malleus` includes the compiler and LinkML. V0 introduces no
`core` or `compiler` extra, second distribution, or external compiler package.
A lean installation is deferred to a later governed revision if a real need
earns the extra topology.

Installed dependency presence and runtime semantics are different boundaries.
The artifact-backed runtime path remains LinkML-free: it loads explicit neutral
artifacts and must pass with LinkML imports mechanically blocked, even though
the installed environment may contain LinkML. This decision does not claim that
the current `malleus-dev` distribution already ships the new compiler or that a
LinkML-absent supported installation exists.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-013`. `CC-D13` is complete.

### OD-014: themed fixture and publication boundary

Decision state: ACCEPTED, Quiet Bell Archive boundary, 2026-08-26

`Quiet Bell Archive` is the accepted public working name. Its themed vocabulary
is fixture-only. Core APIs, artifacts, diagnostics, and protocol records use
neutral names.

The operator attests exactly:
`Luis Guzman Lorenzo is the author and rights holder for the original Quiet Bell text/data, licensed Apache-2.0`

That attestation covers no visual asset. A future public asset must have an
exact manifest entry binding path, bytes, digest, media type, author, license,
and origin. `CC-PUB01` human review binds the exact manifest digest; any byte or
manifest change invalidates the review. This decision creates no fixture,
source file, asset, public page, or publication.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-014`. `CC-D14` is complete.

## Remaining decisions after revision 18

These are closed in order, with examples and counterexamples, before their
dependent workstream starts.

| ID | Question | Blocks |
|---|---|---|
| OD-007 | Protected governance partition versus separate governance graph | Normative admission profile |
| OD-009 | Promotion after research CC-R08 versus earlier experimental public package | Production namespace and autodoc |
| OD-010 | Endpoint and generic class-reference semantics | Graph admission profile and operation traces |

Compatibility analysis, partial migration rules, automatic dependency repair,
and external effect delivery remain outside the foundation block.
