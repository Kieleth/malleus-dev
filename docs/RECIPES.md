# Recipes

Six ways to capture and use domain knowledge in a malleus-shaped knowledge
graph, each grounded in working code from a fleet of adopting projects
surveyed in August 2026. The fleet spans a game engine, a DevOps platform, a
clinical-records coding pipeline, a household-finance platform, a fitness
product, a decision-modeling app, a hardware-attestation system, a
knowledge/insight system, and an autonomous research loop. Some are public
(the Logosphere engine, the kieleth.com knowledge site, the Silk graph
store); the rest are private products and are described here without
identifying detail. The survey's full evidence, with file-and-line
citations, is private; the patterns and the lessons are not.

Read this together with `DELIMITATIONS.md`: each recipe names the prior art
it must not reinvent. A recipe here is a pattern with evidence, not yet an
API; the closing section lists the design decisions still open.

The survey verdict in one paragraph: five of the six recipes already have at
least one production-grade implementation in the fleet. The sixth, formulas,
is the fleet-wide gap: five projects independently wrote the formula down as
data and none of them execute it. And the pattern malleus's assent protocol
formalizes, a lifecycle between "recorded" and "accepted," was hand-rebuilt
at least six times across the fleet, each time incompletely. The fleet is
the argument for malleus.

---

## Recipe 0: Depending on the root ontology

Not one of the six, but the most repeated failure, so it comes first.
Observed failure modes across the fleet:

- A symlink to an absolute path, broken by a directory rename; codegen dead
  for months and nothing noticed.
- Vendored copies of `malleus.yaml` frozen at an old version while upstream
  moved on with non-cosmetic changes; no pin, no drift detection. One
  project had two stale copies.
- A content-hash pin in a test, making any upstream release a hard stop
  with no migration path.
- A path dependency several directories up, a Docker build context with
  sed-rewrites of the package name, and a PyPI name collision where
  `pip install malleus` fetches an unrelated squatter package.

What good looks like, assembled from the fleet:

1. Resolve the root from the installed package, never a sibling checkout:
   `bundled_ontology_path("malleus.yaml")`, or copy from the installed
   share/ directory at codegen time.
2. Gate generation on a version floor (major exact, minor at least).
3. Verify compatibility at load with `check_compatibility_strict()` and
   assert the expected verdict in a test. The strict variant is the consumer
   question ("does this root still validate like the reference?"); the
   non-strict `check_compatibility()` answers the producer question and is
   blind to a dropped `required` constraint, the most silent drift there is.
4. Regenerate in CI and fail on a dirty diff.

The `malleus-inquisitor` CLI checks root currency mechanically: a schema
whose imported root has drifted from the installed malleus reports
`divergent` and fails the rite.

---

## Recipe 1: Capture a domain in a KG

The pattern: a LinkML schema imports malleus, every domain concept extends
one of the five primitives, the loaded registry is a required constructor
parameter, and invalid writes never materialize.

**The deepest adoption, and the correction that made it the sharpest
lesson**: a clinical-records pipeline built a 65-class domain ontology over
the primitives and ran production case graphs in the hundreds of nodes and
thousands of operations with zero rejections, under real regulatory stakes.
An earlier version of this document cited that zero as evidence the gate
scales. A mechanical audit then found the root ontology had never loaded:
an early import resolver silently skipped the unresolvable import, so the
registry never held the root's constraints, and once the root actually
loads, roughly a quarter of the largest production graph fails validation.
A rejection rate of zero is indistinguishable, from inside the system,
between a perfect gate and an absent one. That is the recipe's real first
rule: verify the gate mechanically (the root-currency and construction
rites exist for exactly this); never infer it from a clean audit log. The
pipeline's other discipline stands and is worth copying, above all its
backward-compatibility gate: after any schema bump, the registry must still
construct, legacy-shaped writes must still validate, and a deprecated class
alias must still write.

**Enforcement has two architectures, and they fail differently.** Malleus
validates registry-side in Python, before I/O, with a legible reason. One
fleet project instead compiles LinkML `slot_usage` into storage-engine
constraints (typed FROM/TO tables) and lets the database enforce. The
second looks equivalent and is not: a property-name filter ran before the
engine ever saw the bad data, silently dropped an unknown column, and cost
that project its entire learning channel for months. Rule: whichever side
enforces, unknown or renamed properties must reject loudly, never filter.

**The anti-pattern is the advisory registry**, the most common defect in
the fleet: a registry that defaults to None with dead validation methods;
edges validated at write time while node payloads are not; a schema
imported and never loaded by any tool; entity creation gated while property
writes go unchecked (documented against itself in one engine's comments).
Every one of these projects wrote the constitutive-ontology docstring and
shipped a descriptive ontology. The recipe must make the gate the easy
path, not the aspiration.

**Adapter variant**: when the store is an external engine, compile the
malleus ontology into its schema at boot. The fleet has two working
examples of a small adapter that maps malleus categories onto an engine's
parent types and declares only the fields it wants type-enforced. The
caveat from one of them: if edge types are hardcoded in the generator
rather than the schema, half the ontology bypasses the source of truth.

---

## Recipe 2: The KG as living state

The pattern: the graph holds current state; events are the record; signals
are derived, never asserted; projections are rebuildable.

- **Signals computed by traversal**: the fitness product computes per-muscle
  recovery signals by walking events to sessions to exercises to muscles,
  and stamps each Signal with `algorithm` and `computed_at`. Self-describing
  derivation: "computed lazily at graph load time, not eagerly on event
  write."
- **Ledger plus rebuildable projection**: the clinical pipeline keeps human
  decisions in an append-only segment; the current verdict is the node with
  no supersession edge; SQLite is a cache proven wipeable by test. The
  attestation system runs the same shape in production with measured
  numbers and an on-record rationale for why its graph is a read-model.
- **Fold, don't accumulate**: the DevOps platform's state promoter never
  creates nodes, only updates entities from the event stream ("the database
  is a cache of the log"), and keeps raw observations out of the graph
  entirely; only significant deviations become Signals.

Two hazards with measured evidence:

1. **An incremental projection cannot see behind its own cursor.** One
   system's forward tail reported an intact hash chain while a full replay
   found the break. Incremental projection and periodic full replay are a
   required pair; pin both with tests so nobody deletes the sweep.
2. **Re-deriving history with today's inputs is a latent bug.** The same
   system re-checks old records against current trust roots; rotate a root
   and history silently re-derives differently. This is the concrete
   motivation for the bitemporal accepted graph: "what did we believe at T,
   as known at T'" must be a query, not a re-run.

---

## Recipe 3: Claims, assumptions, and axioms as data

The richest category in the fleet, and the one where the assent protocol
earns its keep: **the structural/epistemic split was hand-rebuilt at least
six times**, none completely. The fleet's versions: a three-level
candidate/owner-confirmed/verified ladder whose client path structurally
cannot reach verified; a proposed/confirmed lifecycle where an LLM can only
propose and the engine executes only confirmed constructs; a claims model
where every candidate is kept and a named-algorithm Signal records the
choice; knowledge-to-wisdom promotion expressed as a typed edge rather than
a status flag; append-only claims with supersession edges; and a research
loop where a claim commits only if its citations resolve. Each rebuilt the
same idea; each is missing a piece the others have.

Showcase-grade fragments to lift:

- **Axioms with sources, one file, three consumers**: each axiom carries a
  statement, a formal expression, and a real citation; rules cite axioms by
  id, the LLM prompt quotes them, and the user-facing API serves them as
  "why" chips. "The LLM never authors a citation; the server resolves it
  from this one source of truth."
- **Cite-or-fail**: an LLM's claim writes only if every cited node id
  resolves; the ungrounded case becomes a queryable failure node. "If it's
  not in the KG, it didn't happen."
- **Keep the losing claims**: one pipeline found a clinical decision being
  made by an `or` operator, "no node, no provenance, no name." Now every
  candidate is a node, the selection is a Signal naming its algorithm, and
  "how much of our accuracy is guesswork" is a re-score of stored claims,
  not a fresh experiment.
- **Epistemic stances as data**: the original malleus research scenarios
  encoded three acceptable answers per hard question: the confident claim,
  the hedged claim traced to its assumption, and the explicit refusal.
  These map directly onto ACCEPT / DEFER / CONTEST.
- **Measured axiom tables**: per-feature comparability verdicts derived
  from a measured sensitivity experiment, with the evidence document cited
  in the data and the model versioned.

Prior-art guardrail (full mapping in DELIMITATIONS.md): claims packaging is
nanopublications territory; contradiction and supersession is Wikidata's
rank model; evidence structure is SEPIO/VA-Spec; referring without
asserting is RDF 1.2 `rdf:reifies`. Adopt or map; the write gate and the
typed lifecycle are the contribution. Assumptions specifically have no
established primitive anywhere. The cautionary tale: one platform
accumulated three generations of assumption storage (a YAML file, untyped
graph nodes, typed claims) that coexist today, with the live graph holding
two contradictory values for one fact and a fallback path that can never be
reached. A malleus assumption primitive should be designed against exactly
that history.

---

## Recipe 4: Mathematical formulas in the KG

**The fleet-wide gap.** Five projects wrote the formula down as data and do
not execute it: a formula string stored on a template node while the real
math lives in a service; `formal_expression` fields on axioms that nothing
reads, next to thresholds duplicated in three disagreeing places; algorithm
strings on Signal types implemented separately in code and synced only by
test; threshold-policy classes generated into an ontology with zero runtime
consumers; a scoring-algorithm description that promises every factor as a
recomputable node and remains a plan.

**The one working implementation** is the decision-modeling app: a
RecipeStep ontology class holds a named variable and an arithmetic
expression; steps evaluate in order through a whitelisted parser (no eval,
four operators); the LLM authors recipes as proposals, the human confirms,
the engine executes only confirmed constructs; and a `compute_tier` slot on
the recipe decides where it runs, "declared in the ontology, not in code."
Its binding idea is the part to steal: **semantic roles join formulas to
graph data**. The recipe says "I need sale_price," the assumption says "I
am sale_price," and provenance, gap detection ("this recipe needs a role no
assumption fills"), and scenario overrides all fall out of one field. Its
weakness defines the malleus work: roles are free-text validated by
nothing, which is precisely a registry job.

The composed recipe: a typed Formula node (encoding chosen from OpenMath or
Content MathML, not invented; see DELIMITATIONS), symbol bindings that are
ontology-validated roles, an engine contract where the executor reads
formula plus bound KG state, and results returning to the graph as Signals
with derivation provenance. Wikidata's defining-formula properties and
Wikifunctions are the named neighbors; nobody closes this loop today.

---

## Recipe 5: Reusable subgraph patterns

The pattern: a named shape stamped out per instance, declared once.

- **One shape, three call sites**: the clinical pipeline instantiates the
  same candidate-claims/selection-Signal/chosen-edge shape for text
  recognition, dates, and concept verification. The proof a pattern is real
  is its third caller.
- **One pattern, three encodings**: the original malleus research encoded
  its key interaction shape as a test fixture with structural assertions,
  as a Prolog rule, and as a scenario evaluation target. The triple
  encoding is the recipe: the same subgraph as fixture, rule, and rubric.
- **Declarative edge minting**: the fitness product derives nine edge types
  from `mint:` blocks in its vocabulary file instead of hardcoded loader
  code, with a behavior-equivalence test. Template nodes projected into
  per-user instances are the same idea one level up.
- **Fork and merge as subgraph operations**: the finance platform clones
  entity subgraphs per scenario with instance-of edges and copy-on-write
  claims, then three-way merges with typed conflicts. Hand-built against
  untyped dicts, which is the gap.
- **Facets as selection contracts** (Logosphere): free-form schema
  annotations select which types an LLM ever sees; the motivating incident
  was a splash screen's fake entities leaking into every prompt as ~150
  phantom walls. Facet selection made the leak unrepresentable.
- **The counter-example**: one project's schema migration forced
  hand-duplication of six near-identical edge families because relations
  cannot be parameterized. A relation template is the missing malleus
  feature this points at.

Prior-art guardrail: this is OTTR's territory (typed, parameterized,
recursively expanded graph templates, industrial use). Differentiate on
gated, digest-addressed instantiation validated against the materialized
store, or compile malleus recipes to OTTR. Do not build a template engine
before answering that question.

---

## Recipe 6: An external engine executes KG fragments

The pattern: behavior lives in the graph as data; a bounded engine reads,
executes, and writes results back with provenance.

Production examples, in increasing ambition:

1. **Parameters from the graph**: kieleth.com's simulation reads every
   behavioral constant from the KG, compiled into the engine and exposed as
   a live-tunable rules node.
2. **Dispatch from the graph**: the DevOps platform routes deployments via
   a graph query (service strategy x installed capabilities x adapter
   priority) resolving to an import path stored as a node property. Adding
   a backend is a new node, not a new branch. Its unconverted twin (a
   hardcoded strategy ladder with silent defaults, in the same codebase) is
   the control group.
3. **Execution from the graph**: the same platform verifies capabilities by
   executing shell strings stored as entity properties on a fixed cadence,
   with the graph declaring privilege, environment, and success criteria.
4. **Rules as entities** (Logosphere): a live engine behavior is a 7-line
   entity declaration; the trigger enum parses through generated code so
   schema and loader cannot drift.
5. **Verdicts without a write**: malleus's own loop: stage into an isolated
   candidate subgraph that never touches the base, verify against a
   pinned logic contract, and on violation return exhaustive typed
   `ViolationWitness` records naming the rule and the bindings that tripped
   it. Nothing is undone, because nothing was applied; the witnesses are
   execution attestations, not proof certificates.
6. **The write loop closed** (Logosphere): the one place in the fleet where
   a graph write demonstrably changes a running physical simulation. Its
   lever discipline is the safety recipe: expose the honest lever, refuse
   the dishonest one, because "make the wrong lever unavailable and the
   wrong choice becomes unmakeable."
7. **LLM as the engine's client** (Logosphere): the ontology slice, with
   the validator's own min/max, is serialized as the LLM's spec sheet, and
   every refusal feeds back into the conversation, because "silent theater
   announced a redwood that never grew." The measured caution from the
   original malleus calibration: tool-call propensity varied 25x across
   models on identical prompts; any recipe with an LLM writer must state
   its prompt style.

Operational rules extracted from incidents:

- **Flag, never delete**: an error-severity rule fed a correction loop that
  silently deleted valid records on every run. A rule sees one item and one
  predicate; the truth needs the record around it. No severity level may
  produce a deletion.
- **Fail closed by severity**: one evaluator catches all exceptions and
  returns no alerts, so a broken critical safety rule silently stops
  firing. A critical rule that cannot evaluate must block, not pass.
- **Declare the dispatch, not just the rule**: rules in YAML mean nothing
  if the evaluator branches on literal rule ids; the rule must declare its
  evaluation scope and bindings.
- **Every writer needs a named reader**: one research loop audited itself
  and found "a carefully-logged passive pipeline": the KG accumulated
  provenance no producer ever read. A node type with no reader is an
  expensive log.

---

## Cross-cutting lessons

- **Make the graph provably load-bearing.** The original malleus
  calibration is blunt: a no-tools, no-memory baseline beat the full
  architecture because the task was recall. Every recipe demo needs
  entities the model cannot know or state it cannot reconstruct.
- **Derive the fingerprint from the validator.** Verified in the field: a
  hand-maintained fingerprint emitter covered only one constraint kind, so
  two peers with incompatible constraints read "identical" while one
  silently quarantined the other's data. A compatibility fingerprint must
  cover every enforced constraint or be generated from the validation code
  itself.
- **Trusted bypasses must be explicit op properties.** A replay path that
  skips validation by context laundered unvalidated data through
  compaction; two consecutive releases shipped bugs on that fork.
- **Rejections must carry diagnosis as data.** A quarantine that returns
  bare hashes with the rich error discarded forces operators to re-derive
  the why by hand. Malleus carries `rejection_reason`; every layer built on
  it must keep that property.
- **Let the mechanism carry the story.** The strongest fleet code documents
  its own incidents inline, with dates, in the config and code that
  resulted. Recipes should ship with their motivating failure.

## What the fleet asks of malleus (API backlog from real usage)

From the heaviest adopter: relation lookup by id (idempotency is currently
string-matching rejection text), a public export and rehydration API,
upsert, cross-segment or deferred-target edges, enforcement of class slot
lists (an undeclared slot family shipped unseen for six schema versions),
and schema-version exposure on the registry. From the dependency survey: a
pinning and upgrade story (Recipe 0) and a resolution for the PyPI naming
collision. From the schema-migration case: guidance on Relation
domain/range scoping so consumers can specialize instead of cloning edge
types.

## Open design decisions (not taken here)

1. Formula encoding: OpenMath vs Content MathML vs a LinkML-native
   expression class that compiles to them.
2. Whether Claim, Assumption, Axiom, and Formula become root primitives or
   ship as a bundled domain extension beside cyp450 and attack.
3. Whether the assent protocol is extracted as the canonical replacement
   for the fleet's hand-rolled lifecycles, and what the minimal adoptable
   subset is (the smallest field version is ~50 lines; malleus's full
   machinery is several stages deep).
4. Recipes-as-templates: differentiate from OTTR or compile to it.
5. Which of the API backlog items gate the next release.
