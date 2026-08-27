# Contract compiler decision workbook

Status: operator decision support

This workbook connects design terms to their practical use. It records accepted
directions separately from choices that still require the operator. It does not
supersede the canonical protocol foundation graph.

## OD-001: consumer-bundle manifest

Decision state: ACCEPTED, Option A, 2026-08-24

The operator accepted Option A after reviewing how the identity is used in
practice. This section explains the accepted direction. `OD-013` now supplies
the one-distribution topology; the exact schema and canonical byte grammar
remain open until `OD-006` closes.

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

Option A approves one canonical consumer-bundle manifest per consumer, with
exact fields decided only after OD-006 contract roles and OD-013 packaging
topology close.

Option B defers the consumer bundle and ships only semantic artifacts. That is
smaller, but it does not mechanically bind a consumer to exact sources, reader,
authority, and compiler attestation.

Accepted: Option A. Its digest remains separate from semantic and
persisted-wire identities.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-001`. Overseer record:
[`OVR-000002`](overseer/entries/OVR-000002.json). `CC-D15` and `CC-D13` are
complete; `CC-D16` remains gated by `OD-006` and its downstream integration
dependencies.

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

## Accepted directions in canonical graph revision 15

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

## Remaining decisions after revision 15

These are closed in order, with examples and counterexamples, before their
dependent workstream starts.

| ID | Question | Blocks |
|---|---|---|
| OD-005 | Exact logical fact vocabulary and wire encoding | Canonical facts and identifiers |
| OD-006 | One combined contract versus explicit protocol, domain, and governance roles | Consumer composition and bundle fields |
| OD-007 | Protected governance partition versus separate governance graph | Normative admission profile |
| OD-008 | Exact fields that are enforcing, identity-only, annotation-only, or rejected | Support profile and metamorphic tests |
| OD-009 | Promotion after research CC-R08 versus earlier experimental public package | Production namespace and autodoc |
| OD-010 | Endpoint and generic class-reference semantics | Graph admission profile and operation traces |

Compatibility analysis, partial migration rules, automatic dependency repair,
and external effect delivery remain outside the foundation block.
