# The wheelhouse was removed on 2026-09-01

`wheelhouse/` held 90 built wheels, 33 MB, including Babel at 9.7 MB, Sphinx at
3.7 MB and SQLAlchemy at 3.2 MB. It was removed from the index and the working
tree by owner decision. This note is the reason and the repair list.

## Why

The environment was already solved without it. `requirements.lock`, in this
directory, carries the exact pin the executor demands:

```
linkml==1.11.1 --hash=sha256:d1bbb97a8b1ea4a99b145007875733a5e5e89b3acfe3e9d1e369fa4a582990ed
linkml-runtime==1.11.1 --hash=sha256:b22c77d8fd920d0f4f43a6ece31393dc0b28bb47790f3e1c114210318c36b3da
```

`src/malleus/_contract_compiler.py` refuses any environment that is not exactly
`1.11.1`. `pyproject.toml` declares `linkml>=1.10`. So the pin exists, with
hashes, and is not wired to the dependency declaration. Vendoring 33 MB of
binaries beside an unused lockfile is the wrong half of that problem to solve,
and Sphinx and Babel binaries do not belong in the permanent history of a
protocol library.

Retained-input policy justifies keeping source roots. It does not extend to a
full transitive binary closure of a documentation toolchain.

## What was kept

- `roots/` — LinkML and linkml-runtime source tarballs, 3.7 MB. Retained input.
- `build-inputs/` — 1.1 MB.
- `requirements.lock`, `manifest.json`, `build-record.json`,
  `derivation-record.json`, `resolution-report.json`, `verification.json`.

## What this breaks, and what to do about it

Six tests fail, all in `tests/test_contract_compiler_divergence.py`:

```
test_retained_baseline_wheels_are_required_and_hash_checked
test_historical_context_is_explicit_but_foreign_context_does_not_hide_semantic_change
test_replay_is_byte_identical_and_matches_retained_observations
test_check_detects_any_retained_observation_mutation
test_cli_checks_retained_bytes_without_rewriting_them
test_cli_cannot_import_ontology_registry_from_hostile_pythonpath
```

Seven ledger entries under `design/contract_compiler/` pin wheel digests.

**These are not to be fixed by restoring the wheels.** The reconciliation is:

1. Rebind the CC-002 environment evidence to `requirements.lock` and its hashes
   rather than to retained binaries. The lock is the reproducibility claim; the
   wheels were a copy of what the lock already determines.
2. Change the six tests to assert the lock and the source roots, not a wheelhouse.
   `test_retained_baseline_wheels_are_required_and_hash_checked` should become a
   test that the lock is present, hash-pinned, and matches the executor's pin.
3. Record a ledger correction for the seven entries that pin wheel digests, in the
   normal append-only way. Do not edit them in place.

## The change that should have been made instead

Wire `requirements.lock` into `pyproject.toml` so `pip install -e ".[dev]"`
reproduces the environment the executor requires. Today CI passes only because
`1.11.1` happens to be the newest LinkML release, and it goes red on the next
release with no code change.

## Context

Full review: [`handover/2026-09-01-malleus-core-review.md`](../../../../handover/2026-09-01-malleus-core-review.md),
sections 5 and 7.

The 33 MB remains in git history. Removing it needs a rewrite, which changes every
commit hash after the first wheel commit, breaks the two paper repositories that
are worktrees of this object database, and invalidates every commit digest the
overseer ledger pins. Not attempted.
