# Malleus

[![PyPI](https://img.shields.io/pypi/v/malleus-dev.svg)](https://pypi.org/project/malleus-dev/)
[![Python](https://img.shields.io/pypi/pyversions/malleus-dev.svg)](https://pypi.org/project/malleus-dev/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

A root ontology in LinkML, and the opinion that words have power.

## Why this exists

I believe words have power. The closer we work with them, the more carefully we pin down what they mean and how they relate, the closer we get to something a machine can use without guessing. An ontology is that pinning-down, made explicit and machine-readable. Borges and Le Guin understood this long before software did: to name something precisely is to begin controlling it.

The practical bet: if you define your domain once, in an ontology, you can propagate that definition through every layer of a system. LinkML can project a schema into JSON Schema, Pydantic, SQL DDL, OWL, SHACL, TypeScript, and other targets. Generated-schema parity is neither tested nor enforced in 0.11. `OntologyRegistry` is authoritative for the structural union used by `ValidTime`, and `ValidTime.from_value` is authoritative for lexical and cross-field temporal semantics. Treat a generated artifact as an equivalent validator only after a conformance test proves it preserves the relevant constraints.

When that actually happens across a codebase, something unexpectedly useful shows up. Components stop drifting apart. The frontend and backend stop disagreeing about what a "Drug" is. A new contributor learns one vocabulary instead of five. Whole classes of bugs (the ones caused by definitions sliding between modules) just stop existing. Adding a new concept becomes one change in one file, flowing outward through whatever code generators you've wired up.

That's malleus: a small, stable root vocabulary, plus the mechanics to keep everything built on top of it honest.

Current package boundary: `0.12.0`, `stage-8c-executable-provenance-and-effect-closure`. See
[docs/IMPLEMENTATION_STATUS.md](docs/IMPLEMENTATION_STATUS.md) for implemented
and explicitly pending capabilities. Code can inspect the same boundary through
`malleus.IMPLEMENTATION_STATUS`.

## The core primitives

Everything in malleus is one of five things:

- **Entity**: something that persists through time. A drug, a server, a person, a concept.
- **Event**: something that happens. A click, a deployment, an interaction detected.
- **Signal**: a derived quality computed from patterns. A risk score, a health status, a trend.
- **Agent**: a mixin capturing the capability to act or decide. Not a class, a trait.
- **Relation**: a typed, directed, reified edge between entities.

Plus four cross-cutting mixins so every typed thing can carry basics without reinventing them: `Identifiable` (id, name), `Temporal` (created_at, updated_at), `Describable` (description, tags), `Statusable` (ACTIVE, INACTIVE, DESTROYED).

Domains extend this root. CYP450 drug interactions, MITRE ATT&CK threat models, both come with examples in this repo. Writing your own is a YAML file.

## Install

```bash
pip install malleus-dev
```

The Python package contains the logic compiler and verifier. Executing logic checks also requires a `swipl` executable on `PATH`; absence fails explicitly at check time.

Recon's core recording and export code ships with Malleus. Install its optional
dependency set for the interactive graph view:

```bash
pip install 'malleus-dev[recon]'
```

## Quick start

```python
from malleus import (
    KnowledgeGraph,
    OntologyRegistry,
    ProposedOperation,
    bundled_ontology_path,
    stage_subgraph,
)

reg = OntologyRegistry(bundled_ontology_path("domains", "cyp450.yaml"))
kg = KnowledgeGraph(reg)

kg.create_entity("Enzyme", "enz-cyp3a4", {"name": "CYP3A4", "cyp_isoform": "CYP3A4"})
kg.create_entity("Drug", "drug-sim", {"name": "Simvastatin"})

candidate = stage_subgraph(kg, [
    ProposedOperation.relation(
        "SubstrateOfRelation", "rel-001", "drug-sim", "enz-cyp3a4",
        {"relation_type": "SUBSTRATE_OF"},
    )
])
assert candidate.valid
assert kg.edge_count == 0             # staging never mutates the base graph
print(candidate.candidate_digest)     # binds ontology, base state, and ordered writes
candidate.materialize_into(kg)        # explicit structural materialization

# Write-time validation. No structurally invalid write materializes.
op = kg.create_entity("NotAType", "x", {})
assert op.op_status.value == "REJECTED"
print(op.rejection_reason)   # "Unknown entity type: 'NotAType'"
```

The `OntologyRegistry` is the constructor parameter for the `KnowledgeGraph`. No registry, no KG. That's the rule, and it's the whole point: the graph can only ever hold things the ontology says exist.

`STAGED` means an operation passed validation inside an isolated candidate. `COMMITTED` means it was structurally materialized. Neither means the record is true, epistemically accepted, or authorized for action.

## Distributed convergence

Every `OntologyRegistry` has a deterministic content hash and a fingerprint of atomic facts. Two peers running the same schema produce the same hash, no coordination needed. Two peers running different versions can verify compatibility without exchanging full schemas.

```python
reg = OntologyRegistry(bundled_ontology_path("domains", "cyp450.yaml"))
print(reg.content_hash())        # 64-char SHA-256, deterministic
print(len(reg.fingerprint()))    # frozenset of atomic facts

result = reg.check_compatibility(foreign_hash, foreign_fingerprint)
# "identical" | "superset" | "subset" | "divergent"
```

Within one fingerprint format, adding represented types, enum values, or slots makes the newer fingerprint a strict superset of the older one. Fingerprint-format changes fail closed: version 3 and version 4 carry different format facts and compare as `divergent`, even when the schema change would otherwise be additive. Peers can tag every write with the hash they used, but the set-relation label is input to caller policy, not an automatic accept decision.

This matters in fleets running rolling updates. An application can combine the
label with validation and its own policy to hold data an older node does not
understand. Malleus returns the label; it does not accept, quarantine, store, or
replay peer writes.

Required facts are deliberately absent from the default fingerprint. Relaxing a slot from required to optional therefore leaves the lax fact sets equal, so `check_compatibility()` cannot identify that removal. Use `strict_fingerprint()` and `check_compatibility_strict()` when field presence matters. For a required-to-optional change, the old required side reports `superset` when it compares itself with the relaxed side, and the relaxed side reports `subset` in the reverse comparison. It is not `divergent`. Caller policy must interpret every non-`identical` strict result in the direction data will flow; the labels alone do not prove writer-to-reader safety.

## Domain extensions

Two examples ship with the library. Write your own the same way:

```yaml
# your_domain.yaml
id: https://example.org/schema/your_domain
name: your_domain
imports:
  - malleus
  - linkml:types

classes:
  YourEntity:
    is_a: Entity
    slot_usage:
      your_slot:
        required: true
        range: YourEnum

  YourRelation:
    is_a: Relation
    slot_usage:
      relation_type:
        range: YourRelationType
        required: true
        equals_string: CONNECTS
      source_id:
        range: YourEntity
      target_id:
        range: YourEntity

enums:
  YourEnum:
    permissible_values:
      VALUE_A: {}
      VALUE_B: {}

  YourRelationType:
    permissible_values:
      CONNECTS: {}

slots:
  your_slot:
    range: YourEnum
```

Relations use concrete classes with explicit source and target ranges. Malleus rejects unknown properties, missing required fields, malformed values, duplicate identifiers, mismatched predicates, and invalid endpoint types before graph mutation.

## Pinned Prolog verification

`GraphFactCompiler` converts any Malleus graph into a fixed typed fact vocabulary. A `LogicContract` pins the ontology hash, exact trusted rule bytes, declared rule IDs, versions, and subprocess wall-clock timeout. `PrologVerifier` evaluates caller-supplied context plus an isolated candidate in a fresh SWI-Prolog process. Stage 5 does not claim that the context is protocol-accepted state.

```python
from malleus import LogicContract, PrologVerifier, ProposedOperation, stage_subgraph

contract = LogicContract.load("your_logic_contract.yaml")
verifier = PrologVerifier(contract)
candidate = stage_subgraph(kg, [
    ProposedOperation.relation(
        "InhibitsRelation", "rel-002", "drug-sim", "enz-cyp3a4",
        {"relation_type": "INHIBITS", "inhibition_strength": "STRONG"},
    )
])
result = verifier.verify_candidate_subgraph(candidate)
if not result.valid:
    for violation in result.violations:
        print(violation.rule_id, violation.violation_code, violation.witness_record_ids)
else:
    # Structural materialization only. This is not epistemic acceptance.
    candidate.materialize_into(kg)
```

The rule program exposes only two required predicates:

```prolog
malleus_rule(RuleId).
malleus_violation(RuleId, ViolationCode, WitnessRecordIds).
```

The verifier enumerates every violation, rejects malformed or unknown witnesses, and never mutates the base graph. Consult errors, timeouts, manifest mismatches, and malformed results raise `LogicExecutionError`; they never become `SATISFIED`. `logic_monitor_failure_records()` converts such a failure into an atomic `MonitorFailure` and `UnavailableAssessment` pair bound to the logical contract and ruleset. Completed checks can be serialized as content-addressed `LogicCheckRecord` and `ViolationWitness` records.

The package ships the CYP450 contract and rules as an example. Stage 5 accepts only trusted, pinned local rule programs. The timeout bounds the Prolog subprocess wall clock, not graph compilation, output size, memory, or CPU. It does not sandbox untrusted Prolog or issue formal proof certificates.

## Policy-selected monitoring and control

Stage 6 replaces opaque monitor and epistemic-policy artifacts with typed,
content-addressed records. A monitor specification binds its assessment kind,
implementation hash, and input artifacts. An epistemic policy names the exact
monitors it requires and maps each `VIOLATED` or `UNKNOWN` result to an
epistemic control. Each proposal binds one exact policy before monitoring
begins, so a controller cannot choose a favorable policy after seeing outputs.

`evaluate_epistemic_policy()` requires exactly one assessment from every
selected monitor. It returns the ordered assessment IDs, control-triggering
assessment IDs, selected verdict, and canonical evaluation hash. Protocol
replay recomputes those values before accepting an `EpistemicDecision`.

The control rules are intentionally small:

- All required assessments `SATISFIED` selects `ACCEPT`.
- `VIOLATED` selects the monitor-specific `REJECT`, `DEFER`, or `CONTEST` mapping.
- `UNKNOWN` selects only `DEFER` or `CONTEST`.
- Explicit policy precedence resolves multiple triggered controls.
- Omitted, duplicate, or unrequired monitor outputs block the decision.
- An exact monitor can produce only one output per proposal. A logical monitor can also record only one completed check for that proposal.

A monitor that did not complete is not silently omitted. The caller records
`MonitorFailure` plus `UnavailableAssessment` atomically, using
`monitor_failure_records()` for non-logical monitors or
`logic_monitor_failure_records()` for logical execution. Stage 6 validates
these outputs and controls; it does not execute every domain-specific monitor
or claim to reproduce its result.

Recording assessments without appending an epistemic decision leaves the
proposal open. This separates monitoring-only C3 from monitoring-plus-control
C4 without maintaining two code paths.

Core assessment kinds use their declared concrete record types. Domain-defined
assessment subclasses cannot claim a core kind while omitting that kind's
required evidence. Version 0.4.0 therefore does not replay 0.3.0 proposals
unchanged: each proposal must explicitly name and source its policy record.
This precommitment prevents ex-post selection. It does not prove that the
proposer had authority to choose that policy or that the policy applies to the
proposal's domain; those checks remain outside Stage 6.

## Accepted graph and bitemporal replay

Stage 7b makes the proposed graph mutation replayable and binds it to assent.
A `GraphBaseArtifact` commits an externally supplied base graph. A
`CandidateSubgraphArtifact` stores ordered writes, precision-aware valid-time
boundaries for every write, supersession links, ontology hash, acceptance and
materialization heads, and pre-state and post-state digests. `ProposedSubgraph`
and `EpistemicDecision` both bind that candidate by ID, record hash, and
candidate digest.

A candidate-bound `ACCEPT` requires exactly one `AcceptedGraphApplication` in
the same decision event. `REJECT`, `DEFER`, and `CONTEST` require no application.
Replay restages the writes and recomputes every binding before it updates the
derived graph. Direct use of `CandidateSubgraph.materialize_into()` remains a
structural operation and cannot change the ledger's accepted projection.

```python
from malleus import AcceptedGraphProjector

projector = AcceptedGraphProjector(protocol_ledger)
current = projector.current(valid_as_of="2026-08-12T08:00:00+00:00")
historical = projector.as_of(
    transaction_as_of="2026-08-12T09:00:00+00:00",
    valid_as_of="2026-01-01T00:00:00+00:00",
)
```

`ValidTime` supports an exact timestamp, a calendar day, a bounded interval,
an order-only transition, or an unresolved prior boundary. Calendar days
require an IANA timezone and embed the timezone database version. Malleus loads
the pinned `tzdata==2026.3` rules, IANA release `2026c`, directly instead of
relying on the host operating system. The database release is a semantic input:
version 0.12.0 replays only `2026c`, and provides no cross-version timezone
migration. Every non-exact value requires the caller's extracted
`indeterminacy_reason`; Malleus commits that reason but does not infer it from
transaction, invoice, authorization, or payment time.

Exact intervals remain half-open. Before the earliest possible transition an
as-of view returns the prior record, at or after the latest possible transition
it returns the replacement, and inside the window it returns `INDETERMINATE`.
When the definite records form a structurally complete graph, an indeterminate
view exposes that graph, three-valued record states, the prior and replacement
IDs, machine reason code, extracted reason, bounds, and a resolution digest.
Its `graph` property fails loudly so an incomplete definite graph cannot be
mistaken for the complete state. Projection also refuses if selected records
lose a required endpoint; dependency-closed temporal projection remains open.

A later retroactive supersession affects only transaction views that include
the later event. The JSONL ledger is the authority; NetworkX is rebuilt as a
defensive projection. Accepted projections omit the local
`KnowledgeGraph.operations` audit because those operation timestamps are
execution-local and are not ledger commitments.

This is an accepted knowledge commitment, not a truth guarantee or action
authorization. The caller must supply the exact graph committed by the graph
base artifact. Remote graph-base resolution, typed retraction, and multi-writer
serialization remain outside version 0.12.0.

## Architecture

For the layer-by-layer walkthrough (vocabulary, typed graph, ground truth loading, logic engine, distributed convergence), see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

Adoption guides:
- [docs/PRINCIPLES.md](docs/PRINCIPLES.md): what malleus claims and what it does not, the six principles the rites defend, and the future work that is reserved rather than asserted
- [docs/ADOPTION_GUIDE.md](docs/ADOPTION_GUIDE.md): start here. How to adopt malleus from any project and keep it alive, written for a human and their coding assistant together
- [docs/IMPLEMENTATION_STATUS.md](docs/IMPLEMENTATION_STATUS.md): the current machine-checked capability boundary
- [docs/ONTOLOGY_PROTOCOL.md](docs/ONTOLOGY_PROTOCOL.md): how to add malleus to an existing project
- [docs/KNOWLEDGE_GRAPH_PROTOCOL.md](docs/KNOWLEDGE_GRAPH_PROTOCOL.md): how the ontology shapes the KG
- [docs/ASSENT_PROTOCOL.md](docs/ASSENT_PROTOCOL.md): how proposals, assessments, decisions, authorization, and replay remain separate
- [docs/ASSENT_PLAN.md](docs/ASSENT_PLAN.md): the thin adapter runner for policy-declared epistemic monitors
- [docs/EFFECT_PROTOCOL.md](docs/EFFECT_PROTOCOL.md): the generic authorization-to-external-observation path and its composable delivery profiles
- [docs/DELIMITATIONS.md](docs/DELIMITATIONS.md): what malleus reuses, rejects, and can honestly claim against OWL, SHACL, TypeDB, XTDB, nanopublications, and the rest of the field
- [docs/RECIPES.md](docs/RECIPES.md): six recipes for capturing and using domain knowledge in a KG, each grounded in working code from a surveyed fleet of adopting projects
- [docs/RECON_CONTRACT.md](docs/RECON_CONTRACT.md): the claim, evidence, comparison, revision, and export boundaries for Malleus Recon

## Malleus Recon

Recon is the literature-forensics part of Malleus. It records a bounded review
as typed works, claims, results, evidence, search events, comparison axes, and
relations in an append-only ledger. It can then rebuild the graph, exact set
comparisons, matrix, bibliography, readable report, and checksum manifest.

```bash
malleus-recon init research/recon \
  --title "Closest work to typed graph admission" \
  --target target:typed-graph-admission \
  --actor reviewer
malleus-recon record research/recon ReviewTarget target.json --actor reviewer
malleus-recon validate research/recon
malleus-recon build research/recon
```

`RECORDED` means the candidate passed the ontology and local ledger rules. It
does not mean the claim is true. Recon reports union, intersection, directional
differences, partial coverage, and unresolved axes. It does not turn those
facts into an automatic novelty, plagiarism, truth, or paper-quality verdict.

The `malleus-recon` skill carries the research procedure: claim-first search,
bounded citation recursion, source inspection, cautious negative findings, and
human-reviewed conclusions. The Python module is provider-independent and
makes no remote calls.

## The value is prevention

Be clear-eyed about what malleus buys you, because it is easy to
underestimate. The value is prevention: whole classes of bugs (definitions
sliding between modules, invalid records entering the store, a rule silently
citing an axiom that no longer exists) stop being possible. Prevention is
invisible by nature; you never see the bug that could not happen, so the
investment is hard to quantify from inside a healthy project. It becomes
visible in exactly two places: in projects that adopted the vocabulary but
not the enforcement and paid a measured cost for the gap, and in rebuilding
a stuck project with these recipes and watching the difference. The recipes
and delimitations documents exist to make that argument with evidence
instead of conviction.

## The Ordo Malleus

Discipline decays without an auditor, so malleus ships its own inquisition.
(An ontology named after a hammer was always going to attract inquisitors;
we let it, within reason.)

Three tiers:

- `malleus-inquisitor <schema.yaml>`: the mechanical rites, a CLI that any
  machine can judge. Does the schema construct, is the imported root current
  against the installed malleus (staleness is detected via
  `check_compatibility_strict`, whose direction-sensitive result exposes
  `required` drift that `check_compatibility` cannot see), are the type-slots
  constrained, are relation endpoints narrowed, are Signals genuinely derived,
  are formula-shaped slots backed by an executor. Exit 0 grants the purity
  seal, 1 records heresies, 2 means the instrument itself is broken and nothing
  was judged.
  Severities are data: copy `rubric.yaml`, tune it, and pass
  `--rubric PATH`. Every run prints the rubric it used and how many rites
  were disabled, because a seal is only as wide as the rubric that granted it.
- The `malleus-inquisitor` skill (`.claude/skills/malleus-inquisitor/`): the
  judgment rites a coding assistant applies to a whole repo: write-path
  enforcement, reader census, citation integrity, provenance quality,
  fail-closed rules. It writes a ranked `MALLEUS_INQUISITION.md` into the
  inspected project.
- The rubric (`src/malleus/inquisition/rubric.yaml`): the single source both
  tiers read. Every rite records the generic field lesson that paid for it,
  no project named. It is data on purpose: tune it, extend it, and send
  generic lessons back as issues or PRs. That is how the Ordo learns.

Every project can also install the adopter, maintainer, and Recon procedures:
`malleus-inquisitor install-skills --project .` preserves the existing Claude
default. Add `--agent codex` for Codex or `--agent all` for both. The acolyte
carries the adoption playbook and can fix its own project's findings.
`malleus-dev` governs library architecture through small, replaceable,
conformance-tested protocol stages. Recon carries the evidence-first literature
workflow. Generic lessons flow upstream as issues and PRs; releases carry the
grown rubric and skills back down. Re-run the installer after upgrading.

## Tests

```bash
pip install -e '.[dev]'
pytest tests/ -v
```

## License

Apache-2.0. See [LICENSE](LICENSE).

## A note on the name

Malleus is the Latin for "hammer". The tool that shapes. Use it to shape your own domains.
