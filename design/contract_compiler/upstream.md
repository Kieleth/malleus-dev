# LinkML upstream contribution train

Status: verified planning record, no issue or PR created

Audit date: 2026-08-24

Verified upstream coordinate: LinkML main commit
[`38737179`](https://github.com/linkml/linkml/commit/38737179acd92a7ee644357096583c77c01aed72)

Latest stable release at audit time:
[`v1.11.1`](https://github.com/linkml/linkml/releases/tag/v1.11.1)

Runtime contributions now belong in `linkml/linkml` under
`packages/linkml_runtime`. The old
[`linkml-runtime`](https://github.com/linkml/linkml-runtime/blob/main/README.md)
repository is archived for contribution purposes.

## Boundary

Good upstream candidates are generic LinkML capabilities: import-map
correctness, observable import resolution, exact loaded-byte provenance,
closed resolver hooks, typed import diagnostics, canonical schema
specifications, and structured-import mechanics.

Malleus keeps EffectiveContract, admission rules, `adopts: true`, graph
endpoints, global identifiers, atomic staging, authorization, ledger identity,
migration grades, consumer composition, and bundle policy.

## Verified blockers and overlap

* The `materialize_derived_schema()` import-map defect is present at the audited
  LinkML main commit. A fresh `SchemaView` drops the original map.
* Duplicate import semantics remain unsettled in
  [issue 3912](https://github.com/linkml/linkml/issues/3912): the specification,
  `SchemaLoader`, and `SchemaView` implement different policies.
* Import provenance work overlaps
  [issue 2913](https://github.com/linkml/linkml/issues/2913),
  [issue 3499](https://github.com/linkml/linkml/issues/3499), and draft
  [PR 3855](https://github.com/linkml/linkml/pull/3855).
* Closed-resolver design must coordinate with
  [PR 3706](https://github.com/linkml/linkml/pull/3706), which adds dict-valued
  `SchemaView` import maps, and draft
  [PR 3707](https://github.com/linkml/linkml/pull/3707), which threads import
  maps through Validator and CLI paths. Neither implements a closed or offline
  resolver policy.
* Exact source metadata intersects
  [issue 3699](https://github.com/linkml/linkml/issues/3699).
* Import-map documentation is tracked by
  [issue 3844](https://github.com/linkml/linkml/issues/3844).
* `linkml-model` declares `structured_imports` and `ImportExpression` as
  `testing`, but `schema_definition.slots` omits `structured_imports`. Generated
  runtime `SchemaDefinition` therefore cannot parse or round-trip the field.
  Representation exposure and resolution semantics are separate work.
* [Issue 3402](https://github.com/linkml/linkml/issues/3402) records
  incompatible merge mechanisms and missing class-level composition. It is a
  blocker for structured-import composition, not an agreed design.

## Dependency graph

```text
U0 minimal defect issue
  -> U1 preserve import map during materialization, with regression test

UD1 import-map documentation

UR0 coordinate import-observation API and draft PR overlap
  -> UR1 behavior-neutral successful-resolution observations
  -> UR2 deterministic resolved edges
      -> UR3A retained-byte loader or resolver boundary
          -> UR3B length and algorithm-tagged digest observations
          -> UR4 closed resolver policy
              -> UR5 typed import diagnostics and complete failure lineage

UC0 maintainer decision on duplicate composition
  -> UC1 specification alignment
  -> UC2 implementation alignment

US0 approve inert structured-import representation
  -> US1 metamodel representation in linkml/linkml-model
  -> US2 generated runtime synchronization and inert round-trip tests

UC1 + US2 + structured-composition decision from issue 3402
  -> US3 normative resolution semantics in linkml/linkml-model
  -> US4 runtime resolution in linkml/linkml

UR3B + US3
  -> UI1 expected-content digest syntax and verification specification

UI1 + US4
  -> UI2 runtime digest verification

UR2 + UR3B + UI2
  -> UL0 portable lock-manifest format

UL0 + UR4
  -> UL1 lock writer and offline verifier

UC1 + US3 + source-metadata decision
  -> UK1 canonical derived-schema specification
  -> UK2 canonical serializer
  -> UK3 versioned digest API

UC1 + US3
  -> UN1 qualified-symbol and alias specification
  -> UN2 runtime implementation

US4 ordering remains open:
  option A: support import_from only and reject import_as and import_map
  option B: depend on UN2 before supporting aliases
```

## Independent PR units

### U1: materialization preserves import map

Repository: `linkml/linkml`

This is the first bounded bug unit. It remains blocked on U0, a minimal issue
owned by the upstream workstream. U0 must record the audited base, reproduction,
expected behavior, overlap search, and issue URL. The test and fix then belong
in the same U1 PR.

RED fixture:

* root imports a logical name;
* the import map points outside the root directory;
* ordinary closure succeeds;
* materialization fails on current main.

GREEN acceptance:

* ordinary closure and materialization both succeed;
* imported classes and induced slots agree;
* materialized imports are cleared;
* no unrelated resolver or composition behavior changes.

If PR 3706 merges first, U1 also covers a dict-valued import map or explains why
the reproduction remains path-only.

### UD1: import-map documentation

Repository: `linkml/linkml`

Independent of U1. Document YAML and JSON mapping forms, exact and prefix keys,
relative value resolution, and extension handling. The documentation build and
strict link checks must pass. If docs CI does not execute snippets, mirror each
documented mapping form in a focused runtime unit test. This can close issue
3844.

### UR1: behavior-neutral resolution observations

Repository: `linkml/linkml`

Starts only after coordination with issues 2913 and 3499 and draft PR 3855. The
first PR records successful resolution only: parent schema, literal import,
mapped candidate, observed resolved locator, and loaded schema. The locator is
an observation, not canonical schema identity. Failure records belong to UR5.

Acceptance covers direct, transitive, relative, CURIE, and import-map cases.
Existing closure contents, merged results, exception types, and exception
messages remain unchanged for current fixtures.

### UR2: deterministic resolved edges

Depends on UR1. Preserve distinct same-named relative imports under different
parents. Repeated runs produce the same observation order. This does not claim
canonical schema identity.

### UR3A: retained-byte loader or resolver boundary

Repository: `linkml/linkml`

Depends on UR2 and agreement on issue 3699. One byte-bearing resolver result is
passed to parsing without rereading or refetching. Resolution behavior remains
unchanged.

### UR3B: exact byte observations

Repository: `linkml/linkml`

Depends on UR3A. Record byte length and an algorithm-tagged digest of exactly
the retained bytes. In-memory schema objects explicitly report that no source
bytes exist.

### UR4: closed resolver policy

Repository: `linkml/linkml`

Depends on UR2. Coordinate PRs 3706 and 3707. Reject network locators before
I/O, allow explicit local maps and package-local `linkml:types`, and forbid
silent network fallback. Failure lineage belongs to UR5.

### UR5: typed import diagnostics

Repository: `linkml/linkml`

Depends on UR4. Begin with import resolution only. Records contain parent,
literal import, attempted locator, category, complete failure lineage, and a
preserved `__cause__`. Define compatibility for callers that currently receive
loader or `FileNotFoundError` exceptions. Parse and composition diagnostics
remain separate PRs.

## Specification tracks

The following are not implementation-ready.

| Track | First required decision | Why blocked |
|---|---|---|
| Duplicate composition | Issue 3912 maintainer resolution | Three current semantics conflict |
| Structured imports | Inert metamodel representation and exact meanings | Generated runtime `SchemaDefinition` lacks the field and semantics are undefined |
| Content pins | Exact-byte observation plus structured-import syntax | No agreed place or verification rule |
| Lock manifest | Resolved edges, exact bytes, and pins | Inputs are not all exposed yet |
| Canonical schema bytes | Composition and source metadata policy | Field inclusion and semantic annotations are unsettled |
| Stable digest | Canonical byte specification | `SchemaView.__hash__` is object identity, not semantic identity |
| Qualified symbols | Composition plus structured imports | Lookup and serialization semantics are undefined |

Each specification change belongs first in `linkml/linkml-model` when it changes
the metamodel or normative schema semantics. Generated runtime synchronization
follows in `linkml/linkml`.

The UC, US, UI, UL, UK, and UN labels above are design umbrellas, not dispatch
authority. Before work starts, each node gets its own card with repository,
exact prerequisite, normative fixture, RED observation, supported fields, and
acceptance. In particular:

* UC implementation alignment is split by affected loader, view, and generator
  behavior after one specification matrix exists.
* US4 names every supported testing field and rejects every unsupported one.
  It never ignores `import_as` or `import_map`.
* UI1 belongs in `linkml/linkml-model` if it changes `ImportExpression`; UI2
  belongs in `linkml/linkml`.
* UL0 decides the portable format before UL1 adds a writer and offline verifier.
* UK1 specifies exact field inclusion and grammar version without assuming that
  annotations are nonsemantic.
* UK3 adds a new digest API and never changes `SchemaView.__hash__`.

## Branch and integration policy

Each public PR branch starts from the same recorded upstream base where
possible. A branch contains one behavior or specification unit and its tests.
It does not depend on another unmerged public branch unless the dependency is
intrinsic and declared.

A dependent PR waits for its prerequisite to merge or explicitly targets the
prerequisite branch as a stacked PR. It is never presented as independent.

Malleus maintains one private integration branch that selects exact commits.
Its validated manifest records:

* upstream base commit;
* each PR head commit and status;
* integration commit;
* ordered patch application;
* patch ancestry and changed-file ownership;
* any conflict-resolution commit and diff;
* status snapshot timestamp;
* LinkML and LinkML runtime wheel hashes;
* exact build toolchain and locked environment;
* transitive dependency-lock digest;
* retained source archive or patch bundle and digest;
* retained built wheels, not only their hashes;
* Malleus conformance profile and corpus version;
* exact test commands and results.

Experimental Malleus conformance builds may use the integration branch before
upstream review. Production or released artifacts require either the upstream
merge commit or an explicit maintained-fork governance decision. Import-ban and
frontend-conformance tests enforce that fork-specific objects and APIs do not
cross the neutral boundary.

When a PR merges, the integration owner replaces the fork commit with the exact
merge commit, rebuilds both distributions, and reruns semantic fact and
diagnostic parity. Branch deletion never removes the only reproducible source.

## Contribution gate

The current official
[`linkml/linkml` guide](https://github.com/linkml/linkml/blob/38737179acd92a7ee644357096583c77c01aed72/docs/maintainers/contributing.md)
directs bug contributors to search issues, provide a repeatable report, and add
a minimal regression test. PRs must remain draft until ready and must have an
assignee. PRs should link an issue, and automated tests should pass before
review. This Malleus workstream imposes the stronger local rule that every
planned bug PR has an issue and recorded RED result. Bug regressions normally
live in an issue-numbered test module.

Before any public submission, the workstream ledger must contain:

1. the current upstream coordinate and overlap search;
2. the RED result on that coordinate;
3. the smallest GREEN change;
4. targeted and full upstream results;
5. the independent Malleus conformance result;
6. an explicit statement of Malleus-specific behavior excluded from the PR.
