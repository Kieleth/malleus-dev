# Malleus Recon contract

Malleus Recon is a local, evidence-first structural-capture profile for
inspecting a paper, technical claim, or research theme against its literature.
It records what a source says, what a reviewer infers, how works overlap, and
what remains unresolved. It does not decide novelty or truth.

This boundary follows the
[Malleus protocol taxonomy](PRINCIPLES.md):

| Boundary | Role |
|---|---|
| Separation of structural conformance, epistemic acceptance, and action authorization | `PROTOCOL_INVARIANT` inherited from Malleus |
| The Recon record meanings and structural guarantees in this document | `OPTIONAL_PROFILE` |
| The bundled Recon ontology, Python module, CLI, JSONL wire, and generated views | `REFERENCE_IMPLEMENTATION` |
| The synthetic miniature review and its answer key | `CONFORMANCE_FIXTURE` |
| Which migrated literature corpus to inspect and what conclusions to draw from it | `ADOPTER_CHOICE`; a supplied corpus is migration and usability data, not a conformance fixture |
| Which Recon records to promote, under which evidence and acceptance policy | `ADOPTER_CHOICE` until bound by a named profile |

Recon does not claim the Assent or semantic-history profiles. Its ledger is the
authority for its own structural capture history only. Its current graph is a
replay-derived structural view, not a Malleus accepted temporal graph.

## Exact claim

Given a declared review target and a bounded set of inspected sources, Recon
can preserve evidence-linked works, claims, results, comparison axes, search
events, and review boundaries in a typed append-only ledger. It can rebuild a
current graph, reject malformed or unsupported records, and generate
deterministic comparison artifacts from the recorded state under one declared
generator and runtime closure.

## Smallest observation

A valid miniature review must be able to:

1. record one target, two works, their source evidence, and shared axes;
2. reject an unsupported comparison without changing current graph state;
3. revise a recorded comparison while preserving the earlier event;
4. rebuild identical JSON, JSON-LD, GraphML, CSV, and Markdown outputs under
   the same declared generator and runtime closure; and
5. report intersection, union, target difference, work difference, and
   symmetric difference without calling any of them a novelty verdict.

## Existing artifact reused

The local literature-forensics package is the reference corpus. Its generic
ideas are reused: atomic works, claims, results and concepts; evidence-bearing
relations; priority-date provenance; bounded recursive exploration; matrices;
set comparison; deterministic exports; and a manifest. Its paper-specific
axes, conclusions, prose, and hard-coded compiler are not library behavior.

## Explicit exclusions

The first release does not:

- crawl the web or require a particular search provider;
- download or redistribute paper full text;
- infer novelty, plagiarism, copying, intent, or paper quality;
- treat `NOT_ESTABLISHED` as proof of absence;
- treat a structurally recorded claim as true;
- treat `RECORDED` as `ACCEPT`, `ACCEPTED`, or authorization;
- map a Recon `review_state` to an Assent verdict;
- write a governed accepted graph or core protocol ledger;
- rank papers with a single novelty score;
- provide a database server or multi-writer protocol; or
- externally notarize the local ledger.

The shared Malleus ledger detects inconsistent local history, including broken
hash links, sequence gaps, reordered retained events, and removal of an
interior event while its original suffix remains. A clean removal of complete
trailing events leaves a valid prefix and is not detectable from the remaining
ledger alone. Detecting that case requires an authentic expected head hash and
event count retained outside the ledger. Without such an anchor, a party with
filesystem access can also replace the ledger and recompute its hashes.

## Two layers

The `malleus-recon` skill carries the research procedure: claim-conditioned
search, source inspection, recursion rules, cautious comparison language, and
stopping criteria. The `malleus.recon` module carries deterministic mechanics:
typed recording, replay, validation, graph projection, set algebra, matrices,
reports, and exports.

The skill may use whatever research tools are available in its environment.
The Python module remains provider-independent and makes no remote calls.

## Record meanings

`RECORDED` means the candidate passed the Recon ontology and local structural
integrity rules. It is Recon's counterpart to the narrow Malleus rule that
[`COMMITTED` means the shape was valid](PRINCIPLES.md).
It does not mean the candidate is empirically true, epistemically accepted, or
safe to act on. `REJECTED` means the candidate and its exact validation errors
remain in the Recon ledger but do not change the current structural graph. It
is not an Assent `REJECT` decision.

The `review_state` field records workflow state inside the Recon domain. Values
such as `REVIEWED`, `CONTESTED`, and `RETIRED` are not acceptance decisions.
They may be inputs to an explicitly identified future selection policy, but
none has an implicit mapping to an Assent verdict.

Every reviewed relation distinguishes:

- `SOURCE_EXPLICIT`: the inspected source states or directly links it;
- `REVIEWER_INFERENCE`: the reviewer derived the comparison from evidence; or
- `NEGATIVE_AUDIT`: the reviewer inspected a named bounded artifact and did
  not find the item there.

`Claim` and `Result` records can name evidence but do not currently carry
`assertion_status` or `basis`. Put a provenance-qualified analytical assertion
on a reviewed relation. Extending those entity records with the same fields is
a persisted-ontology migration, not a property the current schema provides.

Comparison coverage uses `CENTRAL`, `MATERIAL`, `PARTIAL`, `ADJACENT`,
`NOT_ESTABLISHED`, `CONTRADICTED`, or `NOT_APPLICABLE`. Only `CENTRAL` and
`MATERIAL` enter the default set comparison. Partial and unresolved findings
remain visible alongside it.

The absence of a current coverage relation means the subject has not been
assessed against that axis. It is not an implicit `NOT_ESTABLISHED` result.
`NOT_ESTABLISHED` appears only when a reviewer records that exact assessment
with its basis and evidence. Comparisons, matrices, and metrics preserve this
distinction.

## Revision

A record identifier is stable. A later event may replace its current value
only when it names the latest recorded event for that identifier. The ledger
keeps both events. A rejected revision leaves the earlier current value
unchanged.

This is transaction history, not publication history. Work records preserve
first-public, issue, revision, or other date evidence separately. An unknown
first-public date remains absent with an explicit basis; Recon does not invent
a calendar value to make sorting easier.

## Source boundary

An evidence attachment records a URI or local path, an in-source locator, a
description, source class, access state, and access date. When a local artifact
digest and length are supplied, Recon preserves those values. A future ingest
adapter may compute them from bytes it reads. Merely recording caller-supplied
values does not authenticate remote content.

This is narrower than the Malleus target that
[an evidence-bearing tuple should point at exact bytes](PRINCIPLES.md).
A future promotion policy must preserve the difference between caller-declared
source identity and byte-verified source identity. It must refuse any target
contract that requires evidence properties the selected Recon closure does not
provide.

## Governed promotion boundary

Recording and promotion are separate operations. Recording changes only the
Recon ledger and its structural projection. It never appends a proposal,
decision, or application to a core protocol ledger.

The selected integration direction is an explicit, one-way adapter from one
validated Recon snapshot to one governed Malleus change candidate. This is
accepted design, not an implemented adapter or public API claim. The flow is:

```text
Recon ledger
  -> validated snapshot and dependency closure
  -> identified selection and promotion mapping
  -> immutable governed change candidate and promotion receipt
  -> target structural checks and Assent
  -> target authoritative ledger
  -> replay-derived accepted graph
```

One promotion attempt must bind, at minimum:

1. the structural-capture profile, project schema, shared ledger wire, Recon
   record-event payload, and replay-validator identities;
2. the digest of the exact project configuration bytes, the current ontology
   hash, the separated grammar and migrated identities verified during the
   read, and every migration-receipt identity crossed for historical events;
3. the validated source ledger head and event count;
4. each selected current event ID, event hash, record type, record ID, and
   candidate record hash;
5. the complete referenced dependency closure, including evidence attachments
   and relation endpoints, with their event and record hashes;
6. an explicit selection-context bundle containing the `ReviewTarget` scope,
   cutoff, and method plus every applicable `ReviewBoundary` and `SearchEvent`;
7. the identities of the selection policy and source-to-target mapping;
8. the target contract and admission-profile identities;
9. for the current public Assent path, the target graph ontology hash,
   `GraphBaseArtifact` ID and content hash, `base_acceptance_head`,
   `base_materialization_head`, and `base_state_digest`; and
10. the exact `EpistemicPolicyArtifact` ID and content hash plus the identities
    of its required monitor artifacts.

The reference graph does not currently type which standalone
`ReviewBoundary` and `SearchEvent` records apply to a particular negative or
unresolved assessment. A promotion policy must enumerate that context instead
of pretending ordinary endpoint and evidence traversal found it. Adding typed
applicability links would require a Recon ontology migration.

The current public Assent runtime checks the selected epistemic policy and its
monitor closure, but it does not establish that the policy is legitimate or
applicable to this domain, actor, or time. The adopter remains responsible for
that applicability decision and must identify it in the promotion profile.

Migration-aware replay now has a separate public contract.
`MigrationVerifier` derives current-byte grammar identities from one live
registry and verifies exact older ontology identities only through a gapless
path of `TOTAL` receipts. It refuses `PARTIAL`, `HARD_BREAK`, unknown, and
grammar-versus-migration collision cases. `MigrationAwareJsonlLedger` reports
the grammar identities, migrated identities, and exact crossed receipts for
one read through `MigrationVerification`. The base `JsonlLedger` remains
grammar-only, and Recon's `historical_ontology_hashes` compatibility surface
contains only alternate payload-grammar identities for the current bytes.
This closes the prior parameter-reuse mismatch. It does not make a receipt a
record transform, authorize promotion, or give core `ProtocolLedger` a
migration reader.

The adapter reads these values from one snapshot and refuses if they change
during derivation. Its only outputs are one immutable target change candidate
and one immutable receipt mapping source records to proposed target records.
The candidate must bind the receipt record as source provenance; a detached
receipt is not sufficient. In the current public Assent representation, the
receipt `SourceArtifact` ID enters the candidate's `source_record_ids`, and the
proposal binds the `CandidateSubgraphArtifact.content_hash`. That content hash
is the receipt-bound candidate identity. `candidate_digest` and the candidate's
semantic `artifact_hash` do not include `source_record_ids` and are not
sufficient identities for this purpose. Producing those artifacts has no
accepted-state effect. Core admission and Assent make separate typed decisions,
and only the target authoritative ledger may change its replay-derived accepted
graph.

Evidence retains its recorded strength across the boundary. A caller-declared
digest and length remain caller-declared. The adapter must not invent byte
verification, media type, source spans, extraction provenance, valid time, or
other missing target data. If the target contract requires absent information,
promotion refuses instead of filling defaults.

A later Recon revision requires a new promotion attempt bound to the new event.
Sharing a stable Recon record identifier does not silently revise an earlier
governed record. Supersession in the target history must be explicit under the
target contract.

There is no dual write. Recon recording writes only the Recon ledger;
promotion derivation writes no authoritative ledger; governed admission writes
only the target ledger; and target outcomes do not rewrite Recon. The current
Recon ontology has no typed record for observing a promotion outcome. Reverse
outcome capture is outside this profile until a named record and mapping
contract exist; it must not be improvised with an unrelated Recon type.

Promotion returns a typed refusal with no partial target candidate when the
source project or ledger does not validate; an expected identity differs; a
selected record is not its current recorded revision; its dependency closure
is incomplete or inconsistent; the mapping assigns unsupported meaning; a
required target field is absent; the target contract or promotion profile is
unknown; or the target base changes during derivation. Refusal leaves both
authorities unchanged.

The current core already exposes `source_artifact_fields`,
`candidate_artifact_fields`, `candidate_artifact_digest`, `make_record`,
`ProtocolLedger`, and `AcceptedGraphProjector`. A target-specific adapter can
use those public primitives. It does not need the private contract compiler,
binder, effective-contract artifact, or generic protocol-machine experiments.
`EXTERNAL_SNAPSHOT_ANCHORED` is a governed genesis mechanism, not a shortcut
for importing a Recon snapshot.

What remains unspecified is the Recon-to-target mapping profile, the target
contract, and how the promotion receipt is made required provenance of the
candidate. One available core representation computes a `SourceArtifact` from
the exact receipt bytes, records that artifact, and names its ID in the
candidate's `source_record_ids`. A `SourceArtifact` records byte identity,
length, media type, and locator. It does not contain or retain the bytes. The
promotion profile must retain the exact receipt bytes at the bound locator and
state whether later verification requires retrieving them. Current core replay
requires the `SourceArtifact` record but does not fetch those bytes. Another
representation is a future first-class change-set or receipt artifact. The
selected promotion profile must choose and enforce one representation before
an adapter ships. Recon revision, valid time, evidence strength, and context
closure must then pass cross-profile conformance.

This is a mapping boundary, not direct schema composition. The Recon and Assent
ontologies currently give the global slot `evidence_ids` different ranges, so
loading Recon as an Assent extension is correctly rejected as an undeclared
collision. A promotion adapter creates target records under the target
ontology; it does not import the Recon ontology into that registry.

Mechanical promotion conformance must show that identical closed inputs yield
identical candidate and receipt identities; stale or incomplete closures
refuse before effects; a later Recon revision cannot mutate an earlier target
version; target rejection or deferral leaves both Recon and accepted graph
state unchanged; acceptance changes state only through one verified target
ledger application; replay reconstructs the same result; and no parallel
accepted-state writer exists. These observations establish integration
behavior, not the truth or usefulness of the promoted claims.

## Recursive exploration

Recon follows a citation or concept branch only when it bears on an active
target claim or comparison axis. Each search event records the query, reason,
and outcome. Exploration stops when a declared boundary is reached, a survey
provides an explicit landscape boundary, a direct predecessor closes the
lineage, or additional sources no longer change the active comparison.

Unsuccessful searches, inaccessible sources, aliases, and unresolved branches
are data. They must not disappear from the research account.

## Set comparison

For target axis set `T` and work axis set `W`, where set membership means
`CENTRAL` or `MATERIAL`, Recon reports:

- intersection: `T ∩ W`;
- union: `T ∪ W`;
- target difference: `T − W`;
- work difference: `W − T`; and
- symmetric difference: `(T − W) ∪ (W − T)`.

These are exact statements about the reviewer-coded profile. They are not
statements about everything a paper could contain.

## Files and commands

A Recon project's authoritative files are `project.json` and, after the first
recording attempt, `ledger.jsonl`. The reference implementation also keeps the
reserved `.recon-writer.lock` file in the project and `.recon-build.lock` in
each output directory. Generated files go under `build/`; the ledger remains
the authority and neither lock file is an evidence or state record. Each
reserved lock path must be a single-link regular file; symbolic and hard-link
aliases are refused.

Project initialization and ledger append use same-directory temporary files,
file sync, and atomic replacement. They fail closed for process-visible write
errors. If project publication reports an error after replacement,
initialization tries to remove `project.json`; if that removal also fails and
the marker remains, it reports an indeterminate outcome. Like the shared core
ledger, these operations do not claim filesystem-independent power-loss
durability for the containing directory entry because they do not sync the
parent directory.

`build` acquires the canonical output directory lock before reading one
validated ledger snapshot and the exact `project.json` bytes that configure
it. It stages on the destination filesystem, verifies the complete output set,
and publishes `manifest.json` last as the commit marker. On a first build, a
failed precommit leaves no marker. On a rebuild, a staging failure leaves the
previous verified marker and build untouched. A publication or final-sync
failure after the old marker is removed triggers marker removal.
If that independent marker-removal attempt also fails and the marker remains,
the builder raises a distinct indeterminate-outcome error instead of claiming
failure atomicity. Recovery may replace or delete only names in Recon's closed
generated-output set. Only a complete, strictly valid manifest v3 from the
current declared generator and runtime grants that deletion authority. A
version 2 or other prior, partial, unknown-version, or forged manifest cannot
authorize deletion of an arbitrary user file.

The first CLI surface is:

```text
malleus-recon init DIRECTORY --title TITLE --target TARGET --actor ACTOR
malleus-recon record DIRECTORY TYPE RECORD.json --actor ACTOR
malleus-recon record DIRECTORY TYPE RECORD.json --actor ACTOR --supersedes EVENT_ID
malleus-recon validate DIRECTORY
malleus-recon build DIRECTORY
malleus-recon compare DIRECTORY TARGET_ID WORK_ID
malleus-recon visualize DIRECTORY
malleus-recon import-v1 DIRECTORY literature_kg.json --actor ACTOR
```

`build` emits canonical JSON, JSON-LD, GraphML, node and edge CSV files, an
evidence table, a work-by-axis matrix, exact per-work comparisons, metrics, a
BibTeX bibliography, a Markdown report, a checksum manifest, and a
deterministic ZIP. Manifest v3 binds the structural-capture profile, exact
project bytes, ontology identity, ledger head and count, separated grammar and
migration verification evidence, the complete ontology source and import
closure, retained definition ownership, the derived JSON-LD term map, the
listed generator source files, and the Python, NetworkX, PyYAML, and zlib
runtime versions. Byte identity is promised only when the validated inputs and
that declared closure match.

`OntologyRegistry.source_closure()` returns the immutable construction closure:
the exact bytes supplied to the parser, canonical absolute locator and role of
every byte-bearing source, every authored import edge including duplicate and
builtin edges, and the source that owns every retained type, enum, slot, and
class definition. Recon derives JSON-LD terms from those real owners instead of
assuming a bundled root plus one entry file. It re-reads every byte-bearing
ontology source before commit and refuses if any changed.

Canonical absolute locators are part of manifest v3. Moving unchanged ontology
files to another directory therefore changes exact manifest and build identity
by design. The registry's structural `content_hash()` remains independent of
filesystem location.

The generator source closure is captured when `malleus.recon.analysis` loads
and is rechecked before commit. A normal CLI invocation starts a fresh process.
In a long-lived library process, editing a dependency after that dependency
loaded but before importing `malleus.recon.analysis` is outside the current
proof: the manifest can then bind newer source bytes while older code remains
in memory. Closing that gap still requires either per-module loaded-source
identities or an isolated fresh-process builder. Generator identity
architecture has not changed in this revision. Interactive HTML visualization
requires the `recon` optional dependency set.

The workflow now declares a narrow native `windows-latest` Recon job through
the expandable `scripts/ci.py recon` profile. It covers the Recon and Recon
ontology tests, not the full repository suite. Local portable tests validate
the profile definition; a successful remote Actions run is not claimed here.

`import-v1` is a typed adapter for the canonical literature-forensics graph
schema used to derive Recon. It requires an empty ledger and maps every known
node and relationship family before committing one atomic batch. An unknown
endpoint pattern blocks the whole import unless the operator explicitly uses
`--allow-unmapped`; the resulting boundary and exact unmapped counts then enter
the ledger.

## Acceptance boundary for version 0.1

The release is complete only when a synthetic fixture demonstrates recording,
rejection, revision, replay, comparison, and deterministic generation. The
larger local literature graph then serves as a migration and usability corpus,
not as a package test fixture or as an encoded conclusion.

This acceptance boundary establishes only the Recon structural-capture
profile. It is not evidence that governed promotion, epistemic acceptance, or
cross-profile composition has been implemented.
