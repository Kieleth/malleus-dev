# Execution bundle design

Status: design only, no core implementation authorized

## Problem

A package version, Git commit, model name, or experiment contract does not
identify an executable system. Malleus experiments combine core code, harness
code, ontologies, policies, data, producer configuration, prompts, tools,
runtime dependencies, and budgets. Today those identities exist in separate
records. Nothing commits the combination under one portable identity.

The bundle must not collapse distinct meanings of `version`. Package version,
Git object identity, schema version, ontology version, producer snapshot, and
contract version remain separate fields. The bundle digest identifies their
exact combination.

## Decision

The current adoption path uses a canonical `ExecutionBundleManifest`. Its
SHA-256 digest is the portable identity of one declared executable
combination. Any material input change creates a new manifest and digest.

One manifest belongs to one executable stage. A feasibility pilot and a final
paper experiment must never share or mutate one root identity. Each stage
creates its own immutable bundle.

The first paper implementation remains research-local and uses Malleus 0.9.0
unchanged. The harness records the canonical manifest bytes as a
`SourceArtifact`, registers every component record first, and includes the
bundle source record in the proposal's existing source lineage.

The active paper uses a split version policy. Its feasibility and experiment
execution bundles keep Malleus 0.9.0 as `CORE_CODE`. Malleus 0.10.0 Recon is
separate, preparation-only literature tooling. Recon does not enter
`CORE_CODE`, `EXECUTOR_CODE`, `RUNTIME`, or any other execution-bundle role
unless a later stage actually imports or invokes those bytes. A research-tool
version never upgrades an execution substrate by implication.

This is a declared-input commitment. It is not proof that the declared bytes
were authentic, available, complete, or actually used. The harness owns those
checks.

## Required roles

Each bundle contains exactly one role manifest for every role below. A role
manifest can enumerate multiple files and protocol artifacts.

| Role | Required content |
|---|---|
| `CORE_CODE` | Exact Malleus source tree or distribution, package version, commit, tree, archive digest, and dirty-state result |
| `EXECUTOR_CODE` | Harness, bridge, adapters, checker, scorer, retriever, renderer, and other executing research code |
| `SCHEMA_ONTOLOGY` | Root, assent, domain, request, response, case, result, and import-closure identities |
| `GOVERNANCE` | Controlling contract, rights and attestation records, capture policy, policies, monitors, registered rules, logic contracts, reconciliation rules, and selection rules |
| `CORPUS` | Corpus bytes, source manifest, ordering, splits, exclusions, generator lineage, and seed commitments |
| `PRODUCER` | Producer implementation, provider transport, requested model, permitted resolved model, client version, and settings |
| `INTERACTION` | Prompt bytes, output contract, retrieval configuration and index, tool schemas, and tool allowlist |
| `RUNTIME` | Interpreter, dependency lock and installed snapshot, operating system, architecture, external engines, locale, and timezone |
| `BUDGET` | Calls, revisions, retries, tokens, latency, cost, concurrency, run count, and stopping rules |

Secrets never enter the bundle. A bundle may commit a non-secret secret
interface identifier, never a credential value.

## Canonical manifest

The outer manifest has this closed field set:

```text
schema
schema_version
bundle_kind
bundle_id
bundle_version
protocol_ontology_sha256
protocol_ontology_semantic_hash
components
required_authorization_gate
```

Every component has exactly:

```text
role
artifact_id
content_sha256
byte_length
```

Rules:

1. `schema` is `malleus.execution-bundle-manifest`; `schema_version` is `1`.
2. `bundle_kind` is `FEASIBILITY_PILOT` or `FINAL_EXPERIMENT`.
3. IDs and versions are nonempty strings. Byte hashes are bare lowercase
   64-character SHA-256 hex unless an explicit `{algorithm, value}` object
   identifies a Git object. Malleus semantic and record hashes are lowercase
   `sha256:<64 hex>` strings.
4. Strict validation rejects duplicate JSON keys, unknown fields, missing
   fields, nonfinite numbers, non-UTF-8 input, and wrong scalar types.
5. After validation, canonical bytes are exactly
   `malleus.ledger.canonical_json(value).encode("utf-8")` from the frozen
   Malleus 0.9.0 substrate: lexicographically sorted object keys, compact
   separators `,` and `:`, Unicode preserved, nonfinite values forbidden, and
   no trailing newline. A research-local helper that appends a newline must not
   be reused for this manifest.
6. `components` contains exactly nine rows, one for each required role, sorted
   by `(role, artifact_id)`. Roles and artifact IDs are each unique.
7. P2 must freeze a machine-readable JSON Schema and positive and negative
   canonicalization fixtures before it may materialize a bundle.
8. Every `content_sha256` and byte length matches one retained role-manifest
   byte set authenticated by the harness.
9. `protocol_ontology_sha256` is the bare SHA-256 of the exact top-level
   protocol-ontology source bytes listed in the `SCHEMA_ONTOLOGY` role.
   `protocol_ontology_semantic_hash` is the prefixed semantic registry hash and
   equals the Malleus ledger `ontology_hash`. They bind different byte domains,
   can differ, and must never be substituted by adding or removing `sha256:`.
10. The manifest does not contain ledger record IDs or hashes. Those depend on
    registration provenance and would make identical declared bytes acquire a
    different portable digest.
11. The manifest does not contain its own digest, authorization, run ID, or
   result.
12. A sidecar, gate record, authorization, and run record point inward to the
   bundle digest. The bundle never points outward to them.

File bindings inside role manifests use exactly:

```text
path
sha256
byte_length
```

Git object IDs must identify their algorithm. A Git tree OID is not a file
SHA-256. Dirty executable source is inadmissible for the paper lane. Freeze a
clean tree before creating either execution bundle.

## Governance JSON profile

Every canonical experiment contract, gate record, authorization, review
record, qualification record, execution realization, and run manifest uses the
same serialization profile. Each record type has a closed JSON Schema and a
schema-specific fixture manifest with at least one valid fixture and one
invalid fixture for every closed-field, type, digest-format, ordering, and
self-reference rule. An upstream frozen record binds the schema and fixture
manifest before the target record can exist.

Canonical record bytes are exactly
`malleus.ledger.canonical_json(value).encode("utf-8")` from Malleus 0.9.0.
Schemas and fixture manifests use the same encoding. A valid canonical fixture
must be byte-identical after parse, validation, and reserialization. Invalid
fixtures may intentionally be noncanonical or invalid JSON and must be
rejected before any digest is trusted.

Every fixture manifest has exactly:

```text
schema_version
target_schema_path
target_schema_sha256
files
```

Its `files` rows are sorted by `path` and contain exactly:

```text
path
sha256
byte_length
expected_valid
```

The fixture manifest excludes itself and its sidecar. A target record binds
its schema and fixture set through record-specific fields ending in
`_schema_path`, `_schema_sha256`, `_fixtures_manifest_path`, and
`_fixtures_manifest_sha256`. The target never contains its own digest or
sidecar digest.

Every `.sha256` sidecar contains exactly the bare lowercase SHA-256 of the
target's exact bytes followed by one LF. It contains no path or filename. A
sidecar is never part of the bytes it authenticates.

## Authorization and runtime binding

One P3 or G6 authorization authorizes exactly one immutable run ID and one run
root. Each authorization is canonical JSON with a schema, fixtures, and
sidecar. It contains `authorized_run_count: 1`, an authorization sequence, the
previous authorization sidecar digest or `GENESIS`, the cumulative authorized
run count, and the contract's `maximum_authorizable_run_count`.

The cumulative count covers every authorization in the applicable contract
lineage, including authorizations under superseded P2 attempt roots. A new P2
attempt does not reset the count. The current cumulative count must equal the
previous count plus one and must not exceed the frozen maximum. A new run
always requires a new authorization, even when no executable byte changed.

Every runtime record contains both:

```text
authorized_run_id
authorization_sha256
```

`authorization_sha256` is the bare digest of the exact copied P3 or G6
authorization JSON, not its schema or sidecar. The values must match the run
root and authorization before the record is accepted. This rule covers every
request, response, proposal envelope, case record, execution realization,
environment and source record, score, terminal record, ledger index or anchor,
and raw or final manifest. When a closed Malleus 0.9.0 protocol record cannot
accept the two fields, its canonical harness envelope carries them and the
ledger's first execution anchor binds an authorization `SourceArtifact`.
Unwrapped core records are not sufficient runtime evidence.

## Raw and final run manifests

Every run freezes `RAW_MANIFEST.schema.json`, `MANIFEST.schema.json`, their
schema fixture manifests, and their digests before authorization. The run
writes canonical `raw_manifest.json` plus `raw_manifest.sha256` before scoring,
then canonical `manifest.json` plus `manifest.sha256` after the terminal record.

The raw manifest has exactly:

```text
schema_version
status
authorized_run_id
authorization_sha256
execution_bundle_sha256
execution_bundle_source_artifact_hash
execution_bundle_record_hash
files
```

`status` is `RAW_CAPTURE_SEALED`. The final manifest has exactly the same
fields plus `raw_manifest_sha256`; its status is `COMPLETED` or `HALTED`.
`raw_manifest_sha256` is the bare digest of `raw_manifest.json`, or `null` only
when execution halted before a raw manifest could be sealed.
Every `files` row has exactly `{path, sha256, byte_length}` and rows are sorted
by UTF-8 POSIX `path`. Paths are relative, unique, traversal-free regular-file
paths. Symlinks are forbidden.

The raw inventory equals every pre-score regular file except
`raw_manifest.json`, its sidecar, scores, the terminal record,
`manifest.json`, and its sidecar. The final inventory equals every retained
regular file except `manifest.json` and its sidecar, so it includes the raw
manifest and sidecar, scores when present, and exactly one terminal record.
Unlisted, duplicated, additional, missing, or modified files fail closed. A
run that cannot form a complete raw inventory cannot be scored; it writes a
halt record and a final failure manifest only.

These manifest exclusions are the only self-reference exceptions. Schemas,
fixture manifests, contracts, bundles, gate records, authorizations, runtime
records, reviews, and qualifications point only to already frozen upstream
bytes. No record contains its own digest, its own sidecar digest, or a digest
of a downstream record.

## Declared and realized producer identity

A pre-run bundle can bind only information available before execution. It
records the provider, requested model or snapshot, client/API identity, and
all settings.

If the provider reports a resolved model only in the response, the run writes
a separate `ExecutionRealizationManifest`. That receipt binds the authorized
bundle digest to observed resolved model identities, runtime observations,
requests, responses, usage, cost, and terminal status. It does not mutate the
pre-run bundle.

If an immutable model snapshot is unavailable, the bundle records that limit.
A mutable alias cannot be described as an exact model version. A response
outside the bundle's permitted resolution policy invalidates the run.

## Malleus 0.9.0 adoption

The paper lane does not change the frozen Malleus 0.9.0 protocol:

1. The harness authenticates and retains every component byte set.
2. It records one `SourceArtifact` for each role manifest.
3. It creates and validates the canonical outer manifest.
4. It records that manifest as another `SourceArtifact` whose source lineage
   names every role record.
5. Every proposal names the bundle source record in its source lineage.
6. Requests, responses, case records, ledger anchors, replay inputs, and the
   pre-score raw manifest repeat the bundle digest and ledger record hash.
7. Scoring starts only after those pre-score identities and raw bytes verify.
   Scores, the terminal record, and the final manifest then repeat the same
   identity and must verify before results are inspected.

The portable bundle digest hashes declared role-manifest bytes. A separate
stage gate record binds that digest to the exact bundle and role
`SourceArtifact` record IDs and record hashes used in one ledger. Re-registering
identical bytes can change ledger record hashes but cannot change the portable
bundle digest. Run records retain both identities.

Core still does not retrieve or authenticate source bytes, inspect provider
execution, schedule calls, detect hidden inputs, validate licenses, or prove
hermetic reproduction.

## Typed core promotion

The reserved public name is `ExecutionBundleArtifact`. Promotion is a separate
core change, not part of the paper's current P2 work.

A minimal typed artifact would add:

```text
execution_bundle_schema_version
protocol_ontology_sha256
protocol_ontology_semantic_hash
component_roles
component_record_ids
component_record_hashes
source_record_ids
```

It would reuse `ARTIFACT_RECORDED`. It would not add a run event or claim that
recording a bundle proves execution. The validator would enforce equal-length
parallel lists, exact role coverage, canonical order, unique records, applied
`SourceArtifact` members, exact record hashes, and source-lineage equality.

Typed promotion changes the assent ontology hash. The paper stays pinned to
0.9.0 unless the author separately authorizes a new core substrate and G3
revalidates protocol, API, fingerprint, replay, and mechanism behavior.

Direct proposal fields for a typed bundle are a later question. The minimal
paper path continues to bind the canonical bundle through its manifest
`SourceArtifact`.

## Required tests

Before the first producer call, tests must reject:

- a missing, extra, duplicated, unknown, or unsorted role;
- a missing, extra, malformed, or noncanonical field;
- a wrong artifact type, record ID, record hash, ontology hash, file hash, or
  byte length;
- substitution between the bare protocol-ontology byte SHA-256 and the
  prefixed semantic ontology hash;
- a changed code, schema, policy, corpus, producer, prompt, tool, runtime, or
  budget byte;
- an unresolved dependency range, mutable model alias at a gate requiring an
  immutable snapshot, or dirty executable tree;
- a bundle that contains its own digest or an authorization/result;
- mixed bundle identities across requests, responses, proposals, case
  records, ledgers, scores, and manifests;
- replay under a different valid bundle;
- a runtime record whose authorized run ID or authorization SHA differs from
  its exact P3 or G6 authorization;
- an authorization that covers more than one run, breaks the authorization
  chain, resets the cumulative count at a new attempt, or exceeds the frozen
  maximum;
- a contract, gate, authorization, review, qualification, or manifest without
  its closed schema and positive and negative canonicalization fixtures;
- scoring before bundle, raw-manifest, ledger-head, and event-count checks.

Recording a valid bundle must create no proposal, execution, or outcome by
itself. A fabricated but structurally valid source declaration must remain
accepted by core, preserving the public SourceArtifact non-authentication
boundary.
