# The wheelhouse was removed on 2026-09-01

Commit `ecc56d6453963759cfbdf38c9d6c510520a46a39` removed 82 built
wheels, about 33 MB, from `wheelhouse/`. The original removal note and review
said 90. Git records 82 deleted paths. The review response preserves and
corrects that discrepancy instead of rewriting the original review.

## Current contract

For the exact Linux compiler conformance environment, Malleus retains a
hash-pinned lock plus source and direct build inputs. Missing transitive
packages may be downloaded and must match their hashes. Malleus no longer
claims installation from repository-retained bytes without network access.
Normal cross-platform package metadata pins only the direct LinkML
compatibility requirement.

The two identities serve different jobs:

- `pyproject.toml` pins the direct `linkml` and `linkml-runtime` compatibility
  versions used by a normal Malleus installation.
- `requirements.lock` pins the complete selected Linux dependency closure by
  version and SHA-256 for exact conformance runs.

A lock proves which bytes are acceptable. It does not prove those bytes are
available offline. A clean conformance environment may fetch a missing locked
package from the network, but the fetched artifact must match the recorded
hash.

## Retained inputs

The repository still retains and hash-checks:

- the LinkML and linkml-runtime source archives and direct wheels;
- the selected pip and CFGraph direct wheels;
- the ANTLR source and setuptools build input;
- the upstream and locally derived PrefixCommons artifacts;
- the locally built ANTLR wheel;
- `requirements.lock` and the historical acquisition, derivation,
  resolution, and verification records.

The old manifest and evidence remain immutable records of the completed
offline experiment. Their `wheelhouse` sections are historical, not a current
repository inventory and not the current availability guarantee.

## Reconciliation

The divergence runner now reads and validates `requirements.lock`, validates
the retained direct and source inputs against `manifest.json`, and runs the
same semantic replay without reading `wheelhouse/`. The compiler tests are
collected by ordinary `pytest`; `scripts/ci.py` no longer invokes the same
directory a second time.

The original CC-X01 evidence remains bound to its historical Git bytes. A new
append-only correction report replaces only its environment-availability
claim. The compiler decision ledger likewise supersedes the offline guarantee
without altering the historical experiment.

Do not restore the wheelhouse to satisfy an old assertion. Do not claim that a
hash-pinned lock is an offline cache.

## Git history

The removed bytes remain in Git history. Removing them from history would
rewrite commit identities and invalidate evidence that binds those commits.
That operation was not attempted and is outside this correction.

The source review is
[`handover/2026-09-01-malleus-core-review.md`](../../../../handover/2026-09-01-malleus-core-review.md).
Its machine-readable response ledger is stored beside it.
