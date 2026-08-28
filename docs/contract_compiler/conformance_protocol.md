# Three-corpus conformance protocol

Status: internal `contract-kernel/v0` protocol

This protocol gives `CC-R01` through `CC-R08` one small, fixed test spine. It
defines membership, integrity, stage coverage, and ownership boundaries. It
does not contain a compiler, a runtime contract, generated expectations, or a
public API.

## Why exactly three corpora

One example cannot prove a general compiler. V0 therefore fixes three distinct
corpora:

| Corpus | Root | Purpose |
|---|---|---|
| `themed_vertical` | `themed_fixture/` | One readable end-to-end example |
| `feature_isolation` | `feature_cases/` | Small positive and refusal cases that isolate one rule |
| `neutral_domain` | `neutral_domain/` | A different vocabulary that exposes theme-specific assumptions |

The set is deliberately closed. Three corpora are enough to start the research
pipeline while preserving independent counterexamples. Adding a fourth corpus
changes the protocol and requires a new protocol version. Adding cases inside
one of the three fixed roots does not.

The bootstrap manifests are intentionally empty. `CC-010` does not invent
source files, expected values, or scenarios for downstream owners. Empty roots
mean “the contract is ready to receive reviewed members,” not “the stage
passed.” A research stage cannot pass until its required cases are listed.

## Files and authority

`corpus.schema.json` is the strict Draft 2020-12 grammar for all protocol
documents. It is closed with no implicit defaults. `corpus.json` is normative
membership. `checksums.json` binds every listed member to its raw stored byte
length and SHA-256 digest. `stage-matrix.json` fixes the ordered
`CC-R01` through `CC-R08` coverage.

The internal guide is in the governed candidate, but Sphinx wiring is deferred.
CC-010 does not widen the existing documentation build or make a public support
claim.

The integration manifest remains the ownership authority. Corpus data contains
no owner, actor, or workstream field. Integration cards assign the input and
oracle trees, and `owner_separations` keeps `CC-011/CC-012`,
`CC-013/CC-014`, `CC-015/CC-016`, and operation trace pair
`CC-019/CC-020` independent. Changing an assignment changes integration state,
not corpus semantics.

The integration owner alone publishes changes to `corpus.json` and
`checksums.json` after reviewing the source and oracle candidates. Source
owners cannot edit oracle files. Oracle owners cannot edit sources or compiler
code. Oracles are written by hand from accepted decisions, never exported from
LinkML, `OntologyRegistry`, or the implementation under test.

## Membership and bytes

Every case has one stable `case_id`, one or more sorted `scenario_ids`, one or
more sorted input paths, and one or more sorted oracle paths. Cases are sorted
by ID. Paths are normalized repository-relative POSIX paths and must remain
strictly below one of the exact prefixes for their corpus and role:

| Corpus | Input prefixes | Oracle prefixes |
|---|---|---|
| Themed | `themed_fixture/direct-input`, `themed_fixture/sources`, `themed_fixture/traces/input` | `themed_fixture/oracle`, `themed_fixture/traces/oracle` |
| Feature | `feature_cases/inputs` | `feature_cases/oracle` |
| Neutral | `neutral_domain/sources`, `neutral_domain/traces/input` | `neutral_domain/oracle`, `neutral_domain/traces/oracle` |

These prefixes cover the planned source, direct-fact, and operation-trace roles
without letting an input masquerade as an oracle. Absolute paths, backslashes,
empty or repeated members, `.` and `..`, cross-prefix or cross-role paths, and
unsorted lists refuse.

`corpus.json` always lists `corpus.json`, `corpus.schema.json`, and
`stage-matrix.json` as protocol controls. Checksum records are sorted by path
and form an exact bijection with those controls plus every listed requirement,
input, and oracle member. The validator accepts only regular, non-symlink files
that resolve inside the repository, then hashes their stored bytes without
newline, Unicode, JSON, YAML, or other normalization. A missing file, extra
checksum, missing checksum, wrong size, wrong digest, link, resolved escape, or
byte mutation refuses.

`checksums.json` excludes itself. Including its own digest would create a
recursive document with no fixed final bytes. The schema, membership, matrix,
and every later corpus member are checksummed. The checksum manifest itself,
tests, guide, and verification report are bound by the governed Git candidate
and its exact artifact digests.

## Shared semantic requirements

The one reserved shared member is
`conformance/contract_kernel/v0/requirements/scenarios.json`. It remains absent
and `OPTIONAL_UNTIL_LISTED` in the bootstrap. `CC-018` may create it under its
own future card. Before the first corpus case is published, the integration
owner changes its state to `LISTED`, adds its checksum, and verifies every case
references a declared scenario.

Each scenario has a stable `scenario_id` and sorted requirements. Each
requirement has a globally unique stable `requirement_id`, one exact kind from
`POSITIVE`, `REFUSAL`, `METAMORPHIC`, `PARITY`, or `COMPOSITION_DELTA`, at least
one sorted decision anchor, and one nonempty statement. Scenario IDs,
requirement IDs, and decision anchors use the same narrow ASCII identifier
grammar as case IDs. The file states semantic obligations only. It owns no
source syntax, expected artifact, implementation choice, or result.

## Stage coverage

The matrix's `assigned_acceptance_tests` map each research stage to its direct
accepted test slices:

| Stage | Direct slice |
|---|---|
| `CC-R01` | `AT-001` |
| `CC-R02` | `AT-002` |
| `CC-R03` | `AT-003` |
| `CC-R04` | `AT-004`, `AT-005`, `AT-006` |
| `CC-R05` | `AT-007` |
| `CC-R06` | `AT-008`, `AT-008a`, `AT-010`, `AT-011`, `AT-012` |
| `CC-R07` | `AT-009` |
| `CC-R08` | all prior slices through `AT-012` |

Every row requires all three corpora. Stage-specific tests may focus on the
members relevant to that stage, but no stage may silently drop a corpus. The
cumulative rule also makes every stage rerun all prior slices. `CC-R08` replays
the complete matrix, verifies mutation adequacy, and runs current bundled
ontologies as a separate regression set. Bundled ontologies are not a fourth
independent corpus or an oracle for the new fact grammar.

## Expanding a corpus

Expansion is one reviewable transaction:

1. The scenario owner adds or extends the shared requirements file under its
   own card.
2. The input owner adds files only below the fixed input root.
3. A different oracle owner writes expected values only below the fixed oracle
   root, using accepted decisions and the scenario requirements.
4. When semantics intentionally change, an independently reviewed
   expected-delta manifest explains every expected difference before compiler
   and oracle changes share an integration.
5. The integration owner reviews both sides, adds the sorted case membership,
   recomputes raw-byte checksums, and runs the fixed protocol validator and
   affected research slices.

A new case, version, or file inside an existing root keeps
`contract-kernel/v0` only when its fields, ownership, stage meaning, and
validation rules already fit this grammar. A new corpus identity, root role,
requirement kind, path rule, checksum algorithm, stage, acceptance mapping, or
meaning of an existing field requires a new protocol version. Historic
manifests and member bytes are never overwritten.
