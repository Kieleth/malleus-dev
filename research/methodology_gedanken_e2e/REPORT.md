# The Gedanken toys, executed

`research/domain_reasoning_controls_recon/GEDANKEN.md` states plainly that its
three Prolog sketches have never been run: "Treat them as shape, not as tested
code" (GEDANKEN.md:30-31). This directory runs them. Three domain ontologies
extending the malleus root, three pinned `LogicContract`s, eleven graphs built
through registry-gated `KnowledgeGraph` writes, and every verdict below is a
value `PrologVerifier` returned on this machine.

Engine: SWI-Prolog 10.0.2 (`swipl` reports version `100002`), fact contract
version 2, five-second subprocess timeout per contract.

## What ran

```
ontologies/kitchen.yaml    sha256:2cbb60d9ae9122a79cefa4966a919ec483f288ef0723e6a6882dd3398cd188f6
ontologies/financial.yaml  sha256:5f69541011784376f1fff53c530adb47499dafac7a780fa3a81353e907372697
ontologies/diagnosis.yaml  sha256:981275212376085c06edb12f62d3f9b25d11c1edfbdb790658f135127c334a07
```

Each hash is pinned in the matching `contracts/*_logic.yaml` and recomputed by
a test, so a schema edit that does not update the contract fails loudly rather
than checking a different ontology than it claims.

Three contracts and not one, because a `LogicContract` pins exactly one
ontology hash and `PrologVerifier.verify_candidate_subgraph` refuses a
candidate whose registry does not verify it
(`src/malleus/prolog_verifier.py:78-79`). Three domains is three contracts.

### Commands

From the repository root:

```bash
PYTHONPATH=src:research/methodology_gedanken_e2e python3 research/methodology_gedanken_e2e/drivers/kitchen.py
PYTHONPATH=src:research/methodology_gedanken_e2e python3 research/methodology_gedanken_e2e/drivers/financial.py
PYTHONPATH=src:research/methodology_gedanken_e2e python3 research/methodology_gedanken_e2e/drivers/diagnosis.py
PYTHONPATH=src python3 -m pytest research/methodology_gedanken_e2e/tests -q
```

`pyproject.toml` lists `testpaths` explicitly, so these tests do not enter the
library suite. Nothing under `src/` was changed.

## Verdicts observed against verdicts expected

| toy | graph | rule / code | expected | observed |
|-----|-------|-------------|----------|----------|
| 1 kitchen | sketch (GEDANKEN table) | MISE_EN_PLACE / UNPREPARED_INGREDIENT `[s6, tomato]` | fires | **fires** |
| 1 kitchen | sketch | MISE_EN_PLACE / UNPREPARED_INGREDIENT `[oil, s3]` | not predicted | **fires** |
| 1 kitchen | sound (added control) | MISE_EN_PLACE | silent | **silent** |
| 2 financial | A | PROVENANCE_PATTERN / MISSING_RISK_STAGE | silent | **silent** |
| 2 financial | A | PROVENANCE_PATTERN / SUPPORT_POSTDATES_CONCLUSION | silent | **silent** |
| 2 financial | B1 | PROVENANCE_PATTERN / MISSING_RISK_STAGE `[rec2]` | fires | **fires** |
| 2 financial | B1 | PROVENANCE_PATTERN / SUPPORT_POSTDATES_CONCLUSION `[o1, rec2]` | not predicted | **fires** |
| 2 financial | B2 | PROVENANCE_PATTERN / MISSING_RISK_STAGE | silent | **silent** |
| 2 financial | B2 | PROVENANCE_PATTERN / SUPPORT_POSTDATES_CONCLUSION `[k3, rec3]` | fires | **fires** |
| 2 financial | B2' (timestamp edited) | PROVENANCE_PATTERN / SUPPORT_POSTDATES_CONCLUSION | silent | **silent** |
| 3 diagnosis | C | DIFFERENTIAL_REQUIRED / SINGLE_HYPOTHESIS `[dx1]` | fires | **fires** |
| 3 diagnosis | C | DIFFERENTIAL_REQUIRED / COMPETITOR_NOT_REFUTED | fires | **silent** |
| 3 diagnosis | C2 (added) | DIFFERENTIAL_REQUIRED / COMPETITOR_NOT_REFUTED `[dx1, h2]`, `[dx1, h3]` | fires | **fires** |
| 3 diagnosis | C2 | DIFFERENTIAL_REQUIRED / SINGLE_HYPOTHESIS | silent | **silent** |
| 3 diagnosis | D | DIFFERENTIAL_REQUIRED (both codes) | silent | **silent** |
| 3 diagnosis | D written as one batch at turn 6 | DIFFERENTIAL_REQUIRED (both codes) | silent | **silent** |

Two rows came out other than expected, and both are findings rather than bugs.

**The kitchen fires twice, not once.** GEDANKEN.md:84 names the tomato as the
single methodological failure. Its own table has step `s3` combining `oil` at
index 3 with no `PrepStep` anywhere touching the oil, which is the identical
shape. The rule the sketch wrote binds twice. The prose read the graph less
carefully than the rule does.

**Graph C cannot fire `COMPETITOR_NOT_REFUTED`.** That rule existentially
requires a rival hypothesis (`m_record(Other, 'Hypothesis', entity), Other \= H`).
Graph C has exactly one hypothesis, so the body has no solution and the code is
silent. The two codes are complementary, not cumulative: no single graph fires
both. Graph C2 was added for that reason, because a violation code that never
fires in any executed case is an untested code.

## Repairs the sketches needed

### R1 - every Event and Signal in the three sketches had to become an Entity

This is the one repair all three toys needed, and it is a load-time refusal,
not a write-time rejection:

```
OntologyError: Concrete relation 'UsesRelation' source_id range 'PrepStep'
must be an Entity subtype
```

`OntologyRegistry` refuses to construct a schema whose concrete relation has a
non-Entity endpoint range (`src/malleus/ontology.py:713-722`). The sketches
declare:

- toy 1: `PrepStep`, `CombineStep`, `CookStep` as `is_a: Event`, all of them
  `UsesRelation` / `IntoRelation` / `YieldsRelation` sources;
- toy 2: `Observation` as `is_a: Event`, `Comparison` and `RiskAssessment` as
  `is_a: Signal`, all three `DerivedFromRelation` endpoints;
- toy 3: `TestOrder` and `TestResult` as `is_a: Event`, both relation sources.

None of those schemas loads. Every one of those classes is an `is_a: Entity`
subtype here. `tests/test_sketch_repairs.py` reconstructs the sketch as written
and asserts that exact error, so the repair is evidence and not a claim.

The cost is not cosmetic. The fact vocabulary's `m_record/3` third argument
carries `entity | event | signal | relation`, and after this repair it reads
`entity` for every node in all three toys. The discriminator that distinguishes
a thing that persists from a thing that happened is unavailable exactly where
the reasoning trajectory lives, because a trajectory is made of steps and steps
need edges.

### R2 - the rule text follows R1

Four lines changed across the three rule files, all the same change:

| file | sketch | executed |
|------|--------|----------|
| `kitchen_rules.pl` | `m_record(Combine, 'CombineStep', event)` | `... entity)` |
| `kitchen_rules.pl` | `m_record(Prep, 'PrepStep', event)` | `... entity)` |
| `financial_rules.pl` | `m_record(K, 'RiskAssessment', signal)` | `... entity)` |
| `diagnosis_rules.pl` | `m_record(R, 'TestResult', event)` | `... entity)` |

Nothing else in any rule body was touched. The sketches' Prolog is otherwise
correct against fact contract version 2, including atom quoting, the `@>`
comparison on ISO-8601 strings, and the arithmetic `<` on integer slots.

### R3 - an abstract supertype per domain, so relation endpoints stay narrowed

The sketches write endpoint ranges as unions: `UsesRelation: Event -> Ingredient`
covers three step types, and `DerivedFromRelation: Entity|Event|Signal ->
Entity|Event|Signal` covers five. A concrete relation declares one class-valued
range per role. Rather than widening to the root `Entity`, which would leave the
endpoints unnarrowed, each domain declares one abstract Entity subtype:
`RecipeStep`, `ProvenanceNode` and `AnalysisStep`, `ReasoningStep`. Abstract
classes are legal ranges and refuse instantiation.

### R4 - graph D's competitors had to be given explicit Explains edges

GEDANKEN.md:308 names `h2` and `h3` and never says which findings they explain.
`SINGLE_HYPOTHESIS` quantifies over *every* finding the concluded hypothesis
explains, so a competitor covering only chest pain and dyspnoea would leave
graph D failing on raised troponin. Here both rivals explain all three
findings. That is also the clinical reading of "raised troponin does not
exclude either" (GEDANKEN.md:303).

The repair exposes the rule's real strength: it does not ask whether a
differential was entertained, it asks whether every single finding has a
competing explanation. That is stronger than the sentence it was written for.

### R5 - the sketches' counts do not match their own tables

Recorded, not corrected; the tables are the operative spec and the graphs are
built from the tables row for row.

| sketch | prose says | table gives |
|--------|-----------|-------------|
| toy 1 | 14 nodes, 11 edges (7 Uses, 3 Into, 1 Yields) | 13 nodes, 12 edges (6 Uses, 5 Into, 1 Yields) |
| toy 2 graph A | 16 nodes | 12 nodes |
| toy 3 graph C | 13 nodes | 8 nodes |

### R6 - no repair, but worth stating: toy 3's rules never read `entered_at`

The sketch declares `entered_at: integer, required` on five classes and writes
two rules, neither of which mentions it. That is the sketch's own shape and it
is kept. `tests/test_toy3_diagnosis.py::test_entered_at_is_compiled_but_unread`
asserts both halves: the ordinal reaches the compiled facts
(`m_property('dx1', 'entered_at', 'integer', 6)`) and the pinned rules never
consult it.

## The self-report trap, demonstrated

Graph B2 is the sketch's sharpest case: a recommendation whose provenance
subgraph has exactly the right shape and whose risk assessment was written the
day after the conclusion it supposedly supports. The rule catches it by
comparing two `asserted_at` strings. Both strings are ordinary domain slots
supplied by the writer.

`drivers/financial.py::graph_b2_writes` takes the risk assessment's
`asserted_at` as its only parameter. Nothing else moves: same records, same
types, same edges, same directions.

```
--- toy 2, graph B2 (post-hoc, honest timestamps) ---
outcome        VIOLATED
facts          153 facts, 23 records
checked rules  PROVENANCE_PATTERN
violation      PROVENANCE_PATTERN / SUPPORT_POSTDATES_CONCLUSION [k3, rec3]

--- toy 2, graph B2' (post-hoc, timestamp edited to lie) ---
outcome        SATISFIED
facts          153 facts, 23 records
checked rules  PROVENANCE_PATTERN
violations     none

--- the self-report trap ---
same record set in both graphs : True
honest B2 violations           : (('PROVENANCE_PATTERN', 'SUPPORT_POSTDATES_CONCLUSION', ('k3', 'rec3')),)
lying  B2 violations           : ()
the only edit was k3.asserted_at, 2026-02-14 -> 2026-02-12; no record, type or edge changed
```

`tests/test_toy2_financial.py::test_the_lie_changes_one_fact_and_nothing_structural`
diffs the two compiled fact sets and pins the result: they differ in exactly
one fact,

```
only in honest : m_property('k3', 'asserted_at', 'string', '2026-02-14')
only in lying  : m_property('k3', 'asserted_at', 'string', '2026-02-12')
```

and every `m_record` and `m_relation` fact is identical between them. The
analyst who decided first and assembled the justification afterwards passes the
methodology check by typing a different date. GEDANKEN.md:240-243 marked this
as an inference it had not tested. It is now tested, and it holds.

The same shape appears in toy 3 without needing a lie at all.
`drivers/diagnosis.py::batch_writes` is graph D with every `entered_at` set to
6, the turn of the conclusion: the clinician who reverse-engineered the
differential after deciding. It returns the same verdict, the same record set
and the same fact count as graph D. There is nothing to lie about, because
nothing reads the slot.

## Two boundaries the executed graphs made visible

**A candidate cannot reference a context graph.** Staging revalidates every
relation endpoint against the candidate's own base
(`src/malleus/kg.py:311-318`), so splitting a graph across the `*context`
parameter and the candidate is only legal where no edge crosses the split:

```
candidate valid: False
reason: Target entity 'onion' does not exist; Target entity 'garlic' does not exist; ...
```

The `*context` parameter carries disjoint graphs, not prior accepted state.

**A negative control is not optional.** Toy 1's sketch has one graph and it
fails; toy 3's `COMPETITOR_NOT_REFUTED` has no graph that fires it. Two graphs
were added (`sound_writes`, `graph_c2_writes`) purely so that every rule is
observed both firing and staying silent. Without them the evidence cannot
distinguish a working rule from one that fires on everything or nothing.

## What this establishes for D0

Everything below is stated from what the runs returned, not from the design
documents.

**1. The candidate/context distinction is needed, and it is measurably absent
from the fact vocabulary.** `tests/test_flattening.py` compiles one 25-record
kitchen graph under three placements of the accepted/proposed boundary: all 25
proposed, 13 accepted and 12 proposed, 24 accepted and 1 proposed. The
`facts_hash` is identical across all three, and so are the violations. It also
compiles the same records once as a materialized context graph and once as a
staged candidate and gets the same fact set and the same hash. A rule cannot
ask "is this the write being proposed right now", because nothing in the ten
predicates answers it.

The distinction is not missing from the protocol. The same test shows
`LogicCheckResult` carrying different `candidate_digest` and
`base_state_digest` values for the two splits while `facts_hash` stays equal.
Malleus knows which records were proposed; the rules are the only layer that
does not. Whatever D0 adds, it does not need to invent the boundary, it needs
to compile the boundary that already exists into a fact the rules can bind.

The concrete cost, observed: in the kitchen toy the same `UNPREPARED_INGREDIENT`
violation on `s6` is returned whether `s6` is the write under consideration or
a step accepted before this session began. A caller cannot attribute the
violation, and cannot admit a candidate incrementally on the grounds that it
introduced no new violation, because "new" is not expressible.

**2. Protocol valid time is needed, and the executed evidence is stronger than
the argument for it.** The toys show three separate failures of the
domain-slot substitute:

- B2 passes when the writer edits one string, with every record, type and edge
  unchanged. A methodology rule reading `asserted_at` checks the writer's
  account of order, not the order.
- Toy 3 declares `entered_at` required on five classes and neither rule reads
  it, so a differential assembled after the conclusion is byte-identical to one
  that was worked through.
- The two domains spell the same concept `asserted_at` and `entered_at`, with
  different ranges (string versus integer). No rule can be written across them,
  and neither name means anything to the protocol.

The protocol's own ordering is real and already recorded: ordered writes in a
candidate, per-write valid-time boundaries, `base_state_digest` and
`candidate_state_digest`, and the ledger's event sequence.
`KnowledgeGraph.snapshot()` returns nodes and relations only, and
`GraphFactCompiler` compiles only snapshots, so none of it reaches a rule. The
fact vocabulary needs a protocol-supplied temporal fact that a writer cannot
set, or every ordering rule built on it is a check on honesty.

**3. Record kind is currently unusable for trajectory facts, which was not
anticipated.** All three sketches typed their trajectory nodes as Events and
Signals, and all three had to demote them to Entities to declare a single edge.
`m_record/3` reads `entity` for every node in every toy. A trajectory is a
sequence of things that happened, connected; malleus lets you have the
happened-ness or the connection, not both. Any D0 vocabulary that intends to
say "this step occurred" has to carry that itself, because the existing kind
argument cannot say it for anything that participates in a relation.

**4. What did *not* need anything new.** Provenance shape is fully reachable
today. `MISSING_RISK_STAGE`, `SINGLE_HYPOTHESIS`, `COMPETITOR_NOT_REFUTED` and
`UNPREPARED_INGREDIENT` are existence conditions over the current ten
predicates, and all four fired correctly on their failing graph and stayed
silent on their sound one with no engine change and no new stage. Two of them
also fired somewhere the sketch's prose did not expect, which is the behaviour
of a rule that works. The blocker for that class of control is that nobody is
asked to write the rule, not that the vocabulary cannot express it. D0 should
not spend vocabulary on what already runs.

**5. One limit the toys did not close.** Nothing here produced or needed a
third verdict. `LogicCheckResult` is `SATISFIED` or `VIOLATED` per state, and
every graph in this directory is a finished state where that is the right
answer. The "not yet, and still possible" case that GEDANKEN.md:372-374 calls
the one that matters mid-session was not exercised by any of these eleven
graphs, so this run establishes nothing about it either way. Recorded as
untested, not as unnecessary.
