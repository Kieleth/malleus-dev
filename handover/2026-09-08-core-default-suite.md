# Core baseline verification and next consumer requirement

## Verified baseline

The complete default pytest selection configured in `pyproject.toml` passed
against commit `386bb427b72daa04793a2aa3b2198bcdfd810fe9`, tree
`53454c70ef4a5749175e1aef07fdea4c8ecb3edb`:

**3,327 passed, 3 skipped, zero failures or errors, one warning.** Pytest
reported 1,153.72 seconds. No code or test change was needed during this run.

The run used a clean detached local clone at
`/tmp/malleus-core-verification.6dm1aW/repo`. Imports were checked to resolve
inside that clone. Its status and diff remained clean after the run. Main's
unrelated paper and research edits were not inputs.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider --tb=short --junitxml=/tmp/malleus-core-verification.6dm1aW/pytest.xml
```

The command ran from the clone root using the existing configured environment:
Python 3.12.9, pytest 9.1.1, LinkML and LinkML runtime 1.11.1, NetworkX 3.6.1,
PyYAML 6.0.3, tzdata 2026.3 and jsonschema 4.26.0. No installation or dependency
configuration change was made.

The local JUnit artifact is 629,148 bytes, SHA-256
`5241a319775c00ae897f92588c8434dfae2b8e3e6bf7daf8b47dd8777584210c`.
It records 3,330 cases, including the three skips. The XML is retained at the
temporary path above, not included in this commit.

The skips are explicit existing tests, not newly excluded failures:

- `TestCYP450Schema.test_generates_json_schema` and
  `TestAttackSchema.test_generates_json_schema` in `tests/test_ontology.py`:
  the LinkML CLI import resolver does not use the registry's resolver.
- `TestShippedGuidanceSaysWhatTheCodeDoes.test_public_and_private_doctrine_do_not_diverge`
  in `tests/test_inquisition.py`: the private doctrine is absent from a clean
  committed tree.

The warning is RDFLib's `ConjunctiveGraph` deprecation in
`test_jsonld_uses_owned_terms_stable_iris_references_and_datatypes`. It is not
a failed assertion.

This closes the default-suite verification gap left by the
[Shop evidence repair](2026-09-08-shop-current-evidence.md). It does not replace
that repair's broader research/action selection: the default configuration
does not discover every research test. The earlier 236-test Shop run and
1,054-test expanded selection retain their own exact scope and attribution.

This is a pytest receipt, not a `scripts/ci.py all`, package-build, external
linkcheck, release, remote-push or consumer-integration receipt. Synthetic
action records still do not prove real external effects.

## Measured test-performance debt

JUnit's per-case timings, grouped by module, attribute 424.025 seconds to
`tests.test_contract_compiler_integration` and 374.867 seconds to
`tests.test_contract_compiler_ledger`. Together they account for about 69% of
this run. `tests.test_docs` accounts for another 89.468 seconds.

These are observations from one run, not a benchmark or a diagnosed algorithmic
cause. A later optimization should measure repeated validation work while
preserving every negative guard. No cache, weaker validator, skipped check or
test reorganization was introduced here. Keep normal TDD focused on the changed
behavior; use the full suite at an integration boundary.

## Next concrete Core requirement: action setup on an adopter-owned history

Robotics requested reuse of the existing action lifecycle on its own
`KnowledgeChangeHistory`, with explicit source, policy and clock inputs. Its
16-command action choice and Robotics domain model remain consumer-owned.

Read-only Core inspection confirms the boundary:

- `KnowledgeChangeHistory.append_anchors`, `select_protocol_programs` and
  `append_protocol_events` already operate on the owning history. Selection
  and complete finite transactions use expected ledger head/count. This is
  the existing research-local action attachment, not a new stable SDK.
- `programs/initialization_bundle.py::add_initialization` authors the finite
  program from explicit source and policy IDs. It does not construct the
  checkpoint or initialize a caller's history.
- `programs/test_initialization_history.py::initialization_prefix` creates
  Shop history unconditionally and then creates fixture prerequisites.
- `programs/test_proposal_history.py::proposal_prefix` also supplies the
  neutral fixture goal, preservation, mapping and pre-state source. Its
  `pair` helper constructs `LocalAction` and uses fixture actors and time.

The `programs` paths above are under
`research/action_history_contract_freeze/`. No ready constructor was found
that accepts an existing owning history and all those explicit inputs without
the Shop setup. This is a producer-composition gap, not evidence of a broken
interpreter, ledger or replay.

The smallest proposed follow-on is to extract the existing checkpoint/context
construction into a Core-owned reference producer, with caller-supplied
history, exact selected artifacts and policies, source bytes, identifiers,
actors, timestamps and action record. Shop tests should call that same producer.
Its first RED should use a non-Shop history and prohibit Shop initialization
and test-helper imports. Preserve the existing atomic context/proposal pair,
exact input bindings, stale-input refusal and Shop regression evidence.

No extraction is implemented by this report. Do not introduce another
interpreter, domain defaults, Robotics vocabulary, implicit policy choice,
recovery behavior or SDK promotion to close this gap.

## Separate consumer evidence

Re-entry supplied its completed supplier handoff at isolated tip
`4ad362e6737432296bc0fc249213b7551a344251`, based on Core
`90146c380994621a2f8df25876affd03fc9e57e3`. Its committed handoff was read; it
reports 388 tests and no remaining Core prerequisite for that bounded
single-action slice. Those tests were not rerun here and are not added to the
Core total. No merge, rebind or adoption of that consumer branch occurred.
