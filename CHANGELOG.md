# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-08-12

### Added

- Added a separate assent ontology for immutable proposals, assessments, epistemic decisions, authorization decisions, requests, revisions, executions, outcomes, and transition records.
- Added a single-writer hash-linked JSONL protocol ledger with strict event schemas, immutable typed record hashes, contiguous sequencing, deterministic replay, derived state machines, and explicit snapshot genesis.
- Added distinct assessment, epistemic, authorization, and request outcome vocabularies. Requests and claim revisions are records, not decision values.
- Added ordered proposed-subgraph staging on isolated graph copies, deterministic materialized-state digests, stale-base detection, and all-or-nothing structural materialization.
- Added a machine-readable implementation boundary and public status document for the Stage 4 capability set.

### Changed

- Replaced permissive field checks with one closed-world instance validator covering inherited and mixin slots, required values, enum and primitive ranges, collection shape, ISO 8601 datetimes, fixed predicate values, numeric bounds, and identifiers.
- Missing imports, unresolved CURIE or URI imports without an explicit local map, unknown ranges, and imported definition collisions now fail registry construction.
- Replaced generic `DrugRelation` and `AttackRelation` classes with concrete predicate classes whose `source_id` and `target_id` use LinkML class ranges.
- Made identifiers graph-wide across entities, relations, signals, and events. Duplicate and reserved positional identifiers reject before mutation.
- Versioned the structural fingerprint format as version 2. All enforced structural facts now affect ontology identity.
- Prolog verification now consumes a complete isolated candidate overlay. The tentative single-relation assertion and retract API was deleted.

### Fixed

- Required root slots now apply to relations, signals, and events.
- Unknown properties and non-enum scalar mismatches no longer pass validation.
- Relation endpoint types are now checked against declared source and target ranges.
- Signal and event writes can no longer overwrite existing graph nodes.
- Rule-rejected candidate writes no longer require private graph and audit-log rollback because live graph mutation occurs only after verification.

### Boundary

- `Operation.COMMITTED` records structural materialization only. It does not represent epistemic acceptance or action authorization.
- Candidate materialization is an explicit structural operation. It is not gated by assent yet and must not be presented as epistemic acceptance.
- The protocol ledger projects accepted proposal membership, not a materialized accepted knowledge graph. Accepted-graph projection and general domain rule execution remain later boundaries.

## [0.1.0] - 2026-04-12

Initial public release.

### Added
- Root ontology (`ontology/malleus.yaml`) with five primitives — Entity, Event, Signal, Agent (mixin), Relation — and four cross-cutting mixins: Identifiable, Temporal, Describable, Statusable.
- `OntologyRegistry` (`src/malleus/ontology.py`): loads LinkML schemas with recursive import resolution, builds a runtime type registry, validates enum fields and required slots.
- Content-addressable hashing:
  - `OntologyRegistry.content_hash()` — deterministic SHA-256 of the canonical resolved schema.
  - `OntologyRegistry.fingerprint()` — frozenset of atomic facts (types, enums, enum values, slot ranges, inheritance).
  - `OntologyRegistry.check_compatibility(foreign_hash, foreign_fingerprint)` — returns `"identical"`, `"superset"`, `"subset"`, or `"divergent"` for distributed ontology convergence.
- `KnowledgeGraph` (`src/malleus/kg.py`): ontology-typed KG backed by NetworkX MultiDiGraph. Write-time validation (type, inheritance, duplicate, enum, required slot, endpoint). Per-operation audit log with status (COMMITTED/REJECTED) and rejection reason.
- `PrologVerifier` (`src/malleus/prolog_verifier.py`): optional domain rule verification via SWI-Prolog. Accepts multiple KGs (`sync_from_kg(*kgs)`). Tentative assertion + contradiction check + retract pattern.
- Two example domain extensions: `ontology/domains/cyp450.yaml` (CYP450 drug interactions) and `ontology/domains/attack.yaml` (MITRE ATT&CK).
- 95 tests across `test_ontology.py`, `test_kg.py`, `test_prolog_verifier.py`.
