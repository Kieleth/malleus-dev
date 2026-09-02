# Contract compiler documentation

The contract compiler documentation renders validated state. Executable
schemas, source code, tests, and validated manifests remain the authorities for
their respective claims.

No public frontend adapter or adapter docstring exists yet. Pinned LinkML
1.11.1 is the selected v0 target adapter. CC-R02 may implement and characterize
that adapter under research authority, but it cannot authorize public exposure.
Public namespace placement, autodoc, and Sphinx-rendered public documentation
remain governed by open CC-D09/OD-009. If CC-D09/OD-009 permits promotion, the
promoted adapter's code docstrings must document implementation and
support-profile versions, supported declarations, refusals, applied defaults,
neutral outputs, and provenance. Sphinx must surface that contract without
redefining it. Another adapter may replace LinkML only behind the same explicit
neutral output contract.

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

```{toctree}
:maxdepth: 1

manifests
support_profile
```
