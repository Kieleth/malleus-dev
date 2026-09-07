# Contract compiler documentation

The contract compiler documentation renders validated state. Executable
schemas, source code, tests, and validated manifests remain the authorities for
their respective claims.

The public `malleus.compiler` facade exposes the selected LinkML 1.11.1
frontend and the compiler-to-history executors described below. LinkML remains
one adapter, not the protocol. Another frontend may replace it only behind the
same explicit neutral output contract and conformance suite.

## Private Greenhouse bootstrap

The first executable compiler seam was deliberately smaller than the formal
compiler runway. It accepted retained source bytes plus an explicit locator and
adapted them into an explicit neutral contract, then encoded that contract as
immutable canonical facts. Its LinkML shapes, field classifications,
defaults, terms, constraints, lowering operations, and structural identity
domains live in one closed machine-readable profile. Python validates and
dispatches those operations. Another implementation can execute the same
profile and neutral contract without importing Python policy or the legacy
ontology registry.

The bootstrap proved only the six neutral Greenhouse cases: explicit defaults,
numeric lexical equivalence, presentation changes, source reordering, one real
constraint change, and atomic refusal of an unknown root field. It does not
claim recursive authored imports, the complete edge-case corpus, direct-fact
parity, an `EffectiveContract`, a protocol-machine program, a reloadable
artifact, complete dependency identity, packaging, or public API stability. It
remains excluded from the wheel until the formal stages harden those boundaries
and the promotion gate accepts them. The validated-contract slice below replaces
its semantic lowerer directly. No legacy lowering or registry fallback remains.

## Private validated-contract slice

The active private compiler now follows one path:

```text
retained source closure
  -> LinkML adapter
  -> contract binder
  -> elaborated contract
  -> canonical contract facts
  -> ValidatedContractArtifact
  -> ContractView
```

The elaborator consumes only bound declarations and references. It does not
reparse imports or borrow declarations from `OntologyRegistry`. The artifact
retains the complete rooted import closure, including the foundation classes
and slots used by the Small Shop fixture. Its semantic hash binds the validated
fact set, metamodel, canonicalization rules, and symbol policy. Source bytes,
annotations, resolver coordinates, and compiler coordinates remain separately
bound evidence, so a description-only edit changes attestation without changing
the semantic fact-set hash.

`ContractView` loads from canonical artifact bytes without LinkML, source files,
or the ontology registry. It provides structural type, inheritance, mixin, slot,
enum, and instance-validation queries. The artifact capability is explicitly
`VALIDATED_FACTS_AND_STRUCTURAL_VIEW_ONLY`. It is not an `EffectiveContract`:
the admission machine and its identity arrive in the next compiler milestone.
It also does not admit protocol events, write an accepted graph, or produce a
`KnowledgeChangeSet`.

The private LinkML convenience entry accepts only the packaged canonical
support profile. Its compatibility-shaped `profile` parameter accepts `None` or
an exact copy of that profile and refuses modified mappings. A future adapter or
profile can be injected only as an explicit, separately identified artifact
behind the same neutral binding contract, never as an arbitrary Python
dictionary that silently changes meaning.

This slice materializes the five canonical seed primitives needed by its
accepted controls: Boolean, DateTime, Float, Integer, and String. Lowering the
LinkML `date` and `uri` builtins into explicit scalar facts is deferred. Inputs
that need unimplemented constructs must refuse rather than guess or borrow
ambient semantics. Public API promotion and packaging remain separate governed
work.

## Private protocol-machine slice

The next private slice makes one protocol machine reloadable and executable as
data. It keeps four identities separate:

```text
ValidatedContractFactSet
  + ProtocolMachineProgram
  + PolicyProgram
  -> NormativeAdmissionProfile
  -> PartialEffectiveContract
```

`ProtocolMachineProgram` declares record shapes, events, ordered instructions,
unique indexes, effects, and typed refusal identifiers. `PolicyProgram`
separately declares the exact required checks, their identities, outcome-to-
verdict controls, and precedence. The normative profile binds the machine and
policy identities. The partial effective-contract identity binds that profile
to the exact validated fact-set hash from the preceding compiler slice.

Python now supplies one generic interpreter for this measured event and verdict
boundary. It validates the complete instruction-reference closure before
execution, stages every effect, and returns either the complete next state or a
typed refusal with unchanged state. It contains no fixture event, record,
field, check, policy, index, or refusal names. It accepts no callbacks, arbitrary
code, I/O capabilities, ledger writer, or graph mutation capability.

The strict example policy used by the conformance fixture is not a universal
Malleus default. Its explicit `SATISFIED`, `VIOLATED`, and `UNKNOWN` outputs map
to `ACCEPT`, `REJECT`, and `DEFER`. A missing required check is different from
an explicit `UNKNOWN` result and refuses the decision. Other adopters may use a
different identified policy program within the accepted outcome and verdict
rules.

At this milestone, this remained a partial, private mechanism. The next private
slice connects it to a final-identity `KnowledgeChangeSet`, semantic history,
and a replay-derived graph. The full three-role contract composition, Assent
no-fallback cutover, external capabilities, and cross-language parity remain
unimplemented. `ContractView` also still implements part of structural instance
admission in Python. Those limits prevent the experiment from being mistaken
for the finished protocol.

Future frontends and interpreters extend these seams rather than adding hidden
Python parameters. A frontend adapter emits the same neutral contract. A new
policy is a separately content-addressed `PolicyProgram`. A future named
capability is an explicit profile reference with its own conformance contract.
Another language may load the same canonical artifacts and is conforming only
when it produces the same state or typed refusal.

## Private source-to-history slice

The third Pareto slice now proves one narrow end-to-end path with the frozen
Small Shop `RET-010` input:

```text
retained source bytes
  -> LinkML adapter
  -> neutral contract representation
  -> canonical contract facts and ContractView
  -> identified machine, policy, and partial EffectiveContract
  -> fixture-local source mapping
  -> immutable KnowledgeChangeSet
  -> one append-only JSONL semantic/protocol history
  -> replay from an empty accepted graph
  -> accepted Small Shop entities, relation, and canonical receipt
```

The machine and policy JSON own the protocol names, shapes, checks, transitions,
effects, refusals, and verdict mapping used by this example. The mapping JSON
owns the fixture-specific source selection, explicit one-based source ordinal,
zero-based operation order, source-field bindings, record templates, and valid
time. Python validates and executes those artifacts. The generic history layer
contains no Small Shop names or values and receives no graph writer.

The complete bootstrap is one atomic append. The history retains the exact
contract, machine, policy, mapping, source bytes, source registrations,
change-set bytes, and lifecycle events needed to reopen it. A completed run can
therefore delete its disposable graph and rebuild the same accepted state and
receipt from JSONL alone. The `ACCEPT` decision and application are one atomic
ledger event, while proposal, checks, and decision remain separate protocol
events bound to the same change-set identity.

Run the private example with:

```console
python -m research.ontology_driven_kg_realization.experiments.small_shop.pareto.ret010 \
  --ledger /path/to/history.jsonl
```

The result contains the exact contract, machine, policy, binding, source,
change-set, ledger-head, and graph-state identities, plus a query view with
sales order `O1`, inventory unit `X1`, and their `OrderContainsUnit` relation.
Running the command again against the same ledger reopens retained bytes instead
of consulting the ambient fixture or program files.

This is a proof, not the public Malleus compiler. It covers one initial
`CREATE_ENTITY` and `CREATE_RELATION` population, not corrections, update or
delete operations, general mapping syntax, richer valid-time queries,
GraphRecipe or OTTR, Prolog policies, external effects, Semantic Re-entry,
legacy-ledger migration, package inclusion, or another-language interpreter.
The mapping file is deliberately fixture-local. Generalizing it before another
real consumer needs the seam would turn this bounded proof into a speculative
DSL.

## Read-only change-set composition

The Small Shop population and correction proofs repeated one mechanical step:
assembling a `KnowledgeChangeSet` from the current history coordinates and
already retained inputs. One composer owns only that repetition. Given
an explicit change-set ID, retained source record IDs, retained evidence record
IDs, ordered operations, valid time, and superseded change-set IDs, it returns
the canonical immutable change set. Every input is required, including an empty
supersession list.

The coordinator calls `history.composition_context()` after retaining needed
source and plan evidence. This reads and verifies history once and returns a
`KnowledgeChangeContext`: immutable base coordinates, contract and receipt
identities, and retained input bytes and roles. No graph, writer, path or
callback enters this value. The factory accepts no caller-supplied replay graph.

The public `malleus.compiler.compose_change_set` takes `context` plus the six
existing composition arguments listed above. It resolves IDs against that
context, preserves the existing KCS bytes and refuses missing or wrong-role
inputs. Context field substitution refuses with `IDENTITY_MISMATCH`. Its
consistency fingerprint is not an authenticated checkpoint or a sandbox.
Composition performs no I/O and changes neither history nor accepted state.
The history method delegates to this same composer rather than a second
serializer. Admission remains separate, and replay derives accepted state.
An intervening append, including evidence-only retention, makes admission
refuse the stale change. The pure composer cannot discover later writes.

This removes boilerplate, not responsibility. Domain adapters still parse
source bytes and choose record IDs, properties, operations, valid-time meaning,
and supersession. Checks and policy still decide whether the proposed change is
acceptable. Protocol events still record that lifecycle. The Python API is
exported through `malleus.compiler`, not the package root. Its KCS grammar
remains `private-v0`; the in-memory context adds no persisted wire. This is a
reference implementation of the optional compiler-enabled semantic-history
profile, not a mandatory protocol tool or a Semantic Re-entry implementation.

## Local CI and compiler TDD

Run the repository's complete local gate with one fixed command:

```console
python scripts/ci.py
```

The default `all` profile runs Ruff over the governed Python boundaries, the
full configured pytest suite, the overseer-ledger and integration validators,
the GraphRecipe and Small Shop conformance slices, and strict Sphinx HTML,
doctest, and linkcheck builds. It reads no command from a card, manifest, or
ledger. A governance record is evidence, never executable CI input.

The same runner exposes fixed `test`, `docs`, and explicit `package` profiles.
Package construction, metadata checking, clean installation, and console smoke
tests run only under `package`; normal research work does not pay that cost.
GitHub Actions calls the selected profiles with `--require-clean`. Local runs
tolerate pre-existing edits but mechanically refuse any tracked or untracked
change caused by a check. A future local merge hook or merge queue must call
this runner rather than copy its commands. No hook installer is part of this
scaffold.

Compiler work keeps the failing RED observation in its immutable worker ledger
and commit history. Live CI does not keep a deliberately failing test on the
branch head. It runs the corrected GREEN test plus the cumulative SLICE,
DISPROOF, REGRESSION, PACKAGE, and ATTEST checks. The integration validator
requires one active result per phase, in that exact order, before a `CC-R`
candidate can become eligible, integrated, complete, or selected.

Place each future research compiler and interpreter test module under
`tests/contract_compiler/`. The fixed `compiler-tests` runner stage executes
that directory after the configured full suite, so a new R stage enters both
local and remote CI without changing `pyproject.toml`, a workflow, a marker, or
a command registry. Keeping this research-local path out of the package-wide
pytest configuration also avoids rebinding unrelated GraphRecipe identities.

The accepted machine boundary keeps protocol meaning in the reloadable
effective-contract artifact. Python is the first generic interpreter, not the
authority for event names, state transitions, effects, or refusal identifiers.
The Lean Review slice proves the interpreter boundary before the later Assent
hard cutover removes handwritten transition paths.

The accepted downstream handoff is one frontend-neutral
`KnowledgeChangeSet`, not a second graph or a Python mutation callback. Source
population and operation-dependency plans are derivation inputs to that
artifact. The ordered protocol ledger admits the exact change set, and an
identified projector derives the accepted temporal graph by replay. This is a
governed compiler target, not a claim that a public artifact class or generic
runtime cutover ships today.

## When the source states no valid time

The public population/history path accepts an explicit absent-time value:

```json
{"valid_time":{"kind":"NONE_STATED","value":null}}
```

This means no domain time is stated, not that the record is true forever or
that a row number establishes temporal order. `valid_time` and both inner keys
remain required. `INSTANT` still needs a timezone-aware timestamp; `ORDER_ONLY`
still needs a nonempty token with meaning chosen by the history profile.
Missing keys, bare null, or a non-null NONE_STATED value refuse.

For example, the Shop source reports supplier order B with quantity 1 in e4
and quantity 2 in e7. Without a declared replacement, both reports remain in
the replayed graph. With an explicit replacement, e4 remains in record history
and e7 becomes current, but no replacement date is invented. Replacements
across valid-time kinds remain unsupported. Ledger recording order is separate
from domain time in both cases.

`KnowledgeValidTime.from_data` parses this shape for both population plans and
change sets. Reopen and `trace_population_record` retain the same value and
source bytes. The document adapter continues to declare ORDER_ONLY capture
import order; this does not change its per-assertion time evidence. The optional
history implementation's current private wire is not a stable public grammar,
and this addition does not change Assent's separate `ValidTime` model or add
valid-time queries.

The executable Shop witness is
`tests/contract_compiler/pareto/test_unstated_valid_time.py`.

## What the capture census proves

The optional document adapter counts mappings the producer supplied. It does
not decide whether the graph expresses everything the source says. Read the
existing receipt values this way; the values and receipt format are unchanged:

| Receipt value | Meaning |
|---|---|
| `FULLY_FORMALIZED` | Mapped fields, no declared gaps |
| `PARTLY_FORMALIZED` | Mapped fields and declared gaps |
| `UNFORMALIZED` | No mapped fields |

Semantic completeness is not assessed. The classification depends on whether
an assertion has `formalized_by` targets and declared `gaps`. Even a
`FULLY_FORMALIZED` assertion may have an omitted relationship. The separate
block axis counts assertions, declarations that nothing is assertable, and
untouched blocks. Uncaptured assertions are invisible to this accounting.

For example, our synthetic Shop note says:

> The clerk reports stock of 2 units and a request for 2 units.
> This stock count supports the claim that the request can be filled.

Mapping the two quantities and the claim text, with no declared gap, produces
`FULLY_FORMALIZED` even if the producer omits the support relationship. Add the
source-supported relationship and it survives admission, reopening, and replay.
Supply a relationship with a missing endpoint and compilation refuses before
writing. Checking a supplied edge is different from discovering a missing one.

Distinguish a proposition identity, an optional label, and its statement or
retained evidence reference. The example's claim has an ID and statement but
no invented name. A relationship needs explicit direction and endpoints plus
retained context and attribution. A source can refer back to a proposition
without repeating two endpoint labels in one sentence. Co-occurrence alone
does not justify an edge, and structural admission does not establish truth.
The adopter supplies the interpretation; Core validates the declared structure
and provenance paths, not semantic entailment or completeness.

The executable conformance fixture uses public compiler, document-adapter,
structural-history, query, and trace APIs:

```bash
python -m pytest -q tests/contract_compiler/pareto/test_capture_coverage_boundary.py
```

This is a synthetic boundary test, not an extension of the frozen Small Shop
source dataset or historical receipts, and not an automatic semantic evaluator.

## Optional grounded knowledge packs

Malleus ships three small LinkML packs under `ontology/packs`: `metrology`,
`chronology`, and `research`. They are offered vocabulary layers, not required
protocol modules. A project can import the packs it needs or supply its own
ontology through the same compiler boundary.

Pack bytes are available with the top-level public
`bundled_ontology_path("packs", "research.yaml")` helper. The public compiler
still receives an explicit source map:

```python
from collections.abc import Mapping

from malleus.compiler import compile_linkml_contract
from malleus.inquisition import validate_pack_conformance, validate_pack_grounding


def compile_research(exact_sources: Mapping[str, bytes]):
    validate_pack_grounding(exact_sources["research"], role="PACK")
    return compile_linkml_contract(
        root_locator="research",
        sources=exact_sources,
    )
```

Here `exact_sources` contains the caller-selected bytes for `research`,
`metrology`, `chronology`, `malleus`, and `linkml:types`. Nothing resolves from
the network or an undeclared filesystem location.

The separate `validate_pack_grounding` rite checks exact source bytes. It
requires each borrowed term group to identify its source vocabulary and
locator. The research pack therefore ties `Observation` explicitly to W3C
SOSA/SSN rather than hiding several intellectual sources behind one citation.
The rite is deliberately modest: it checks citation shape offline and returns
a deterministic receipt or typed refusal. It does not judge whether the
chosen source is good scholarship. For projects, bare Malleus roots and CURIEs
resolved through the schema's exact prefix map trigger the same direct-root
grounding requirement. Unrelated prefixes and unsupported full URI references
do not masquerade as Malleus roots.

If a project copies and edits a pack while claiming compatibility with it,
`validate_pack_conformance(edited_bytes, reference=shipped_bytes)` binds both
byte identities and checks the reference declaration surface. Documentation
and additive declarations or enum values may change. Reference imports remain
one unique, order-independent set. Removing a reference declaration, changing
an existing declaration list, or adding a stronger constraint to one refuses.
Extend an existing class through a new subclass. This is a structural check,
not a claim that the edited vocabulary is semantically equivalent.

```{toctree}
:maxdepth: 1

manifests
support_profile
```
