# Contract compiler decision workbook

Status: operator decision support

This workbook connects design terms to their practical use. It records accepted
directions separately from choices that still require the operator. It does not
supersede the canonical protocol foundation graph.

## OD-001: consumer-bundle manifest

Decision state: ACCEPTED, Option A, 2026-08-24

The operator accepted Option A after reviewing how the identity is used in
practice. This section explains the accepted direction. The exact schema and
canonical byte grammar remain open until OD-006 and OD-013 close.

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

1. reads the exact source bytes through the closed resolver;
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
[`OVR-000002`](overseer/entries/OVR-000002.json). `CC-D15` is complete;
`CC-D16` remains gated by OD-006 and OD-013.

## OD-012: exact compiler baseline

Decision state: ACCEPTED, release-first baseline R2, 2026-08-25

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
4.9.3 release supplies no compatible wheel. The accepted R2 correction therefore
adds this separate, exact transitive build-input set:

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

CC-D12 selects those coordinates, identities, the separate root-source and
transitive-build-input memberships, and acceptance policies. CC-002 owns
acquisition and byte retention, the deterministic double build, complete
transitive resolution, runtime wheelhouse, platform verification, and offline
installation proof. This split removes the former cycle in which CC-D12
required material that only CC-002 was assigned to create.

A later LinkML fork or source commit cannot silently replace this baseline. It
requires a separate governed baseline revision, exact source and built-artifact
identities, and the same acceptance suite before an explicit switch.

Canonical decision record:
`https://malleus.dev/contract-compiler/OD-012`. Overseer record:
[`OVR-000061`](overseer/entries/OVR-000061.json), replacing corrected historical
record [`OVR-000050`](overseer/entries/OVR-000050.json). `CC-D12` is complete;
CC-002 materialization remains pending.

## Accepted directions in canonical graph revision 13

| ID | Accepted direction | Important limit |
|---|---|---|
| AD-001 | `EffectiveContract` becomes the public runtime root | Production promotion waits for conformance and wire transition |
| AD-002 | LinkML becomes compiler-only | The distribution currently declares LinkML and LinkML Runtime as mandatory dependencies, although tracked `src/malleus` code does not import them |
| AD-003 | Stage protocols remain experimental | Only named whole-pipeline combinations gain conformance claims |
| AD-004 | Duplicate symbols fail closed absent explicit policy | Current schemas use explicit adoption, so policy must be selected |
| AD-005 | Independent branches for independent upstream units plus one exact integration branch | Intrinsic specification and runtime dependencies remain sequential or explicitly stacked |

The operator also excluded migration feature development from the foundation
block. That is an execution-scope instruction, not approval to reuse an old
wire field with new meaning.

## Immediate operator decisions

These choices block stable artifacts. No worker may infer them.

### OD-002: explicit adoption

Current fact: `assent.yaml` explicitly adopts `reviewer_id`; `ocr.yaml`
explicitly adopts `locator` and `reviewer_id`. Current `OntologyRegistry`
accepts only an identical redeclaration marked `adopts: true`.

Option A keeps explicit identical adoption as the sole duplicate composition
rule. Conflicts, missing adoption markers, and order-dependent overrides fail.
This preserves the deliberate domain prose and current bundled structure.

Option B removes all downstream redeclarations. Every duplicate fails, and
domain-specific prose must move to a separate annotation mechanism or disappear.

Required proof for either option: compile every bundled closure and assert that
each duplicate is either absent or authorized by the exact versioned policy.

Recommendation: Option A is the smallest policy consistent with the current
promotions and fail-closed intent. It still needs normalized equality rules for
absent versus explicit `false`, default ranges, and annotations.

Decision: OPEN

### OD-003: semantic source when LinkML and legacy behavior differ

Current fact: measured Recon classes agree for the exercised fields. They do
not prove general parity. Known differences include conflicting mixins, parent
and mixin precedence, numeric bound combination, explicit false values, and
missing default ranges.

Option A makes exact pinned LinkML semantics authoritative for standard LinkML
fields. Malleus classifies unsupported or unsettled constructs and refuses them.
Malleus retains only its own graph and governance semantics.

Option B preserves legacy `OntologyRegistry` behavior through adapter rules,
even where LinkML differs. This reduces immediate semantic change but retains a
second interpretation layer and weakens the reason to delegate compilation.

Required proof for either option: the divergence corpus must classify every
case as equal, intentionally changed, or unsupported. No unexplained difference
may be normalized away.

Recommendation: Option A matches the stated goal of delegating LinkML meaning
to LinkML. It should be adopted only with an exact compiler lock and explicit
support-profile refusals.

Decision: OPEN

### OD-004: persisted-wire transition

Current fact: existing ledgers, snapshots, graph bases, candidates, and logic
facts bind the current ontology hash grammar. Internal Recon data includes
historic records that current tests require to replay. Renaming a new semantic
digest to `ontology_hash` inside ledger schema version 1 would silently change
the protocol.

Option A declares a new ledger schema or epoch and a typed hard break. Historic
corpora remain frozen evidence and are read only by the historic reader or
receive an explicit refusal from the new reader. This avoids migration feature
work.

Option B implements a versioned, attested translation or replay bridge from the
old identities to the new contract and bundle identities. This preserves
current-reader replay but brings migration into the critical path.

Required proof for either option: frozen 0.11 and 0.13 projects, ledger events,
snapshots, graph bases, and candidates must receive the exact documented result.
Rewriting the historic fixtures is not proof.

Recommendation: Option A matches the instruction to move quickly without
building migration now, but it deliberately gives up replay through the new
reader. That consequence requires explicit approval.

Decision: OPEN

## Decisions after OD-002 to OD-004

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
| OD-011 | Module-instance identity, resolver precedence, import-order meaning, cycle behavior, and bundled fallback | Recursive source boundary and binder ordering |
| OD-013 | One distribution with compiler extra, two distributions, or external locked compiler environment | Packaging and installation tests |
| OD-014 | Themed fixture name, vocabulary, authorship/license manifest, and public-clearance gate | Normative corpus membership and publication |

Compatibility analysis, partial migration rules, automatic dependency repair,
and external effect delivery remain outside the foundation block.
