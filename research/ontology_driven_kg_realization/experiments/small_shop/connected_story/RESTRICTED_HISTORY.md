# Shop replacement-rule compatibility

## What now works

A fresh history admits B's quantity correction from one Y to two Y while
refusing replacement of the occurrence that reported the update. Both e4 and
e7 remain current occurrence records. B/e4 remains retained as the predecessor
of the current B/e7 state. An identified machine rule enforces the restriction;
the descriptive profile label does not.

The positive input is the retained e4/e7 source data. The attempted occurrence
replacement is synthetic hostile input, not another chapter observation. No
supplier connection, external effect, business-policy verification or full
21-event population is claimed.

## Exact dependency and scope

Core: `2ef5442efec6e43f2b2623a288933f7c62d46d4e`, tree
`d7972839f45508f2a13451f4fd21f80e7db5240e`.

Shop implementation: `04794b4d6a14ebd9237311d77dc1a26ca8dd9a4e`, tree
`a0434519c1bae011371c83f23664012a4f49fdae`.

This is a new compatibility baseline, not a rebind of released `v0.14.0`
evidence. The earlier producer, counterexample, proposed profile and source
files remain byte-identical. Their structural-only history still admits the
Event-replacement counterexample. No old history is migrated or reinterpreted.

The new runner reuses the exact old Shop ontology and row mapper. It extends
only the installed structural machine's rule section. The
[instruction](replacement_instruction.json) references the profile's `state`
role, containing `SupplierOrderState`. There is no second replacement type
list in Python. The complete selected machine is identified, retained and
reconstructed on reopen. Core enforces the rule inside admission and replay;
`admit_structural_change` still owns the generated check events.

The old profile remains a proposal and its explanatory text describes the
earlier probe. The new machine supplies enforcement without rewriting that
text. The final connected profile, matching choice and time interpretation
are not selected by running this witness.

## Distinguishing observations

| Selection | Observed result |
|---|---|
| `SupplierOrderState` role, `EXACT` | State correction and Event additions admit; Event replacement refuses. |
| Same role, `SUBTYPE` | Same result for the current concrete Shop types. |
| Control role `Entity`, `EXACT` | State replacement refuses: `SupplierOrderState` is not exactly `Entity`. |
| Control role `Entity`, `SUBTYPE` | State replacement admits. This broad role is a test control, not a Shop proposal. |
| Original structural-only history | The same Event replacement still admits. |

The refusal preserves bytes from the start of admission. Successful preparation
has already retained evidence in a separate transaction, and the test takes
its byte snapshot after preparation. It does not claim preparation was rolled
back. Accepted records, change sets and accepted-state heads remain unchanged.

Each positive run retains 18 protocol events, two change sets, seven historical
records and six current records. Full replay, maintained incremental replay and
reopen agree within each run. Every historical record traces to the exact
retained table. Different matching rules have different machine and history
identities even when these inputs produce the same graph. Repeated
exact-matching runs produce byte-identical histories.

## TDD and reproduction

RED `0f793c54` fails collection because the new Shop consumer is absent, not
because Core is broken. All eight consumer tests pass with GREEN `04794b4d`.
The matching discriminator and old counterexample ensure the refusal is caused
by the selected rule, not malformed candidate data.

Run in the existing declared environment at the named Core coordinate:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/connected_story/test_restricted_history.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m research.ontology_driven_kg_realization.experiments.small_shop.connected_story.restricted_history /tmp/shop-restricted-exact.jsonl --match EXACT
```

The ledger path must be new. `SUBTYPE` is a separate explicit test choice. The
printed Core coordinate states the tested dependency; the command does not
install or switch Core automatically.

An isolated export of the exact Core commit plus only the Shop successor files
reproduces these identities. The imported runtime resolves inside that export.

| Identity | Exact matching | Subtype matching |
|---|---|---|
| Machine | `sha256:674ab56dd90b71fd4fa826eccccd472451da728e683baa79af9bd3fdc9ba649f` | `sha256:97a2c43f4d71ce57021f7b5716bf4d361268cb8d879f352b6a185e86907eff8b` |
| History bytes | `sha256:73abc028d691268abeb170562ef7d84c677163a8e5b7c776c88f524c2938b9d2` | `sha256:54d1fb0c3325b62a5dfea9a61b188fa371b22c4961743ab33e9d53534fdc0850` |
| Replay receipt | `sha256:f3a03210deab0830bf0676dcd45b4e90a5d83b191cc4cb3351e421247d94b42b` | `sha256:b612a9d5b306922c7902a25b6d3f848a75973c26f57adef27065aaf58dd30e0a` |

Both bind the unchanged proposed profile
`sha256:f19edb3fe3a1676c02bf0daa6963a8bfde7c184009d648de44e6071aa65c2fc7`.

The broader isolated gate passes **283 tests, zero skips**, selecting all of
`research/ontology_driven_kg_realization/experiments/small_shop` plus
`tests/contract_compiler/pareto/test_transition_admission.py`. Ruff lint,
formatting and scoped diff checks pass. The source/earlier-probe diff against
the Core baseline is empty.

The first broad attempt used a Git archive and returned 282 passes and one
failure: the existing Shop journal test could not resolve its historical commit
without a Git object database. The final gate uses a detached local checkout
of the exact Core commit with only the three Shop implementation/test files
overlaid. It verifies the journal's required commit exists before running.
The existing journal guard was not changed or excluded. No dependencies were
installed and no shared worktree files were used as runtime inputs.

No full-repository, package, release, source-truth or complete connected-story
claim follows from these consumer checks.

## Decision remaining

Recommendation for the first connected model: only named state types are
replaceable, with `EXACT`. A new specialized state type needs an explicit role
addition under a separately selected future contract. `SUBTYPE` permits such
specialized types automatically. Both modes now work. Selecting between them
is a policy decision for Luis, not a missing Core capability.
