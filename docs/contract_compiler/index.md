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

The first executable compiler seam is deliberately smaller than the formal
compiler runway. It accepts retained source bytes plus an explicit locator and
first adapts them into an explicit neutral contract, then encodes that contract
as immutable canonical facts. Its LinkML shapes, field classifications,
defaults, terms, constraints, lowering operations, and structural identity
domains live in one closed machine-readable profile. Python validates and
dispatches those operations. Another implementation can execute the same
profile and neutral contract without importing Python policy or the legacy
ontology registry.

The bootstrap proves only the six neutral Greenhouse cases: explicit defaults,
numeric lexical equivalence, presentation changes, source reordering, one real
constraint change, and atomic refusal of an unknown root field. It does not
claim recursive authored imports, the complete edge-case corpus, direct-fact
parity, an `EffectiveContract`, a protocol-machine program, a reloadable
artifact, complete dependency identity, packaging, or public API stability. It
remains excluded from the
wheel until the formal stages harden those boundaries and the promotion gate
accepts them. A later implementation must replace or extend this seam directly,
not add a fallback to the legacy registry.

## Local CI and compiler TDD

Run the repository's complete local gate with one fixed command:

```console
python scripts/ci.py
```

The default `all` profile runs Ruff over the governed Python boundaries, the
full configured pytest suite, the overseer-ledger and integration validators,
the GraphRecipe conformance slice, strict Sphinx HTML, doctest, and linkcheck
builds, then a real package build, metadata check, clean-environment install,
and console-script smoke tests. It reads no command from a card, manifest, or
ledger. A governance record is evidence, never executable CI input.

The same runner exposes fixed `test`, `docs`, and `package` profiles so the
Python-version matrix can share work without repeating the full suite. GitHub
Actions calls these profiles with `--require-clean`. Local runs tolerate
pre-existing edits but mechanically refuse any tracked or untracked change
caused by a check. A future local merge hook or merge
queue must call this runner rather than copy its commands. No hook installer is
part of this scaffold.

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
