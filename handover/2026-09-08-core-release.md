# Core release preparation

Luis requested documentation, push and release after the maintained-projection
slice. This supersedes the earlier backlog's exclusion of release work, not
its exclusions of new runtime features or packaging experiments.

## Scope

Publish the existing Python reference implementation and optional profiles.
Do not advance the standalone Assent stage, stabilize private wire grammars,
claim cross-language parity, or include uncommitted paper/research work.
The changelog describes the public compiler/history path, profiles, packs,
ontology revision, maintained projection, experimental action interpreter,
and the independently bounded Recon/OCR changes since the previous package.

Approved version: **0.14.0**, a minor pre-1.0 release. Luis confirmed the
version and native-Git push/tag exception with "Go". The existing `v*` tag
workflow requires the exact package
version on main history, runs tests and distribution checks, then publishes to
PyPI using its configured trusted publisher. No tag or publication is claimed
by this preparation record.

The remote main read on September 8 resolves to
`dfa367aee7848a69cf6999b158ba1a1057c50b38`. The initial local candidate is
`815ed63b7be5ebc4e1bb1ebad96ac586e078ce93`, tree
`031a5edc2399c5c1fcfdc9540698258d8da9432a`, 299 commits ahead. No paper path is
in that forward diff. The dirty paper and research work remains outside the
candidate. Remote state must be rechecked before publication.

## Corrections found during preparation

The status document named Assent ontology 0.9.0, while the shipped schema and
runtime status name 0.11.0. The prose is corrected, with a hard test against
the runtime's declared ontology versions. Existing ontology-bound ledgers must
not be silently rebound to different source bytes.

The full clean baseline at `815ed63b` completed with **3,338 passed, 11 failed,
3 skipped**, one RDFLib deprecation warning, in 812.47 seconds. All eleven
failures shared an old producer binding in the current
inspection-note trace tests. Compiler-view change `8d315fbd` altered retained
producer evidence, but that current test still selected the preceding v2
execution. Its producer mismatch is an intended refusal, not a failed
source interpretation or a reason to weaken the identity check.

The separate `inspection_note_execution_v3` records the actual current
preparation result. All earlier evidence stays byte-identical. Only
`base_ledger_head` differs from the historical change set; domain operations,
source/evidence identities and valid time agree. Preparation, admission, reopen
and per-record trace all execute. The document boundary passes 22 tests;
status tests pass 13. The preparation documentation/status/current-ledger
selection passed 144 tests. Neither is a full release receipt.

The release version and README claims had a separate two-test RED, then
14 status/milestone tests passed after the version change. The runtime version,
package metadata, README, status document, changelog and guards name 0.14.0;
the standalone Assent stage remains 8c. No ontology byte changes are introduced
by this release transaction.

The last remote main CI run also exposed two test-harness defects still present
in this tree: unguarded `tomllib` imports on Python 3.10, and file-object doubles
missing methods used by Windows lock initialization. Three tests now use the
already-declared `tomli` dependency when the stdlib module is absent. The lock
doubles preserve the full stream interface. The new local compatibility guard
reproduces five failures before correction and passes all six cases afterward;
actual platform execution remains the remote matrix's responsibility.

The measured 812-second baseline exceeds the old main-job timeout of ten
minutes before installation and remaining gates. Main and release test jobs
now allow thirty minutes. No test, supported Python version or failure gate is
removed; build and publication timeouts remain unchanged.

The clean candidate `f717a3a8` full test run reported **3,353 passed, 2 failed,
3 skipped**, with one RDFLib warning. Both failures exposed the same omitted
release step: the generated OCR corpus manifest still bound package 0.13.3.
The declared corpus generator updates only `corpus.json` and `checksums.json`
for 0.14.0. All 67 case artifacts remain unchanged, including source documents,
readings, oracles and verification results. The existing full regeneration
and runtime-binding tests remain strict; the fast package-version test now
also checks the corpus version and names the regeneration command on failure.
No OCR runtime, ontology, dependency or case semantics changed.

The corrected `77d7b9b4` clean local gate passed 3,355 tests with 3 skips,
40 GraphRecipe tests, 229 Shop tests, governance and strict HTML/doctest/link
checks. Package build, archive-to-wheel member parity and clean install passed.
GitHub then exposed two publication/portability gaps absent from a local clone:

- The existing local `evidence/capture-coverage-2026-09-06` tag had not been
  pushed. Its three reviewed commits are cited by entry 419 but are not main
  ancestors. Publishing that existing evidence ref preserves the exact history;
  no ledger entry or commit reference is rewritten. CI now validates the ledger
  and integration before the expensive full suite, with a hard fail-fast test.
- Pillow's PNG compression produces different bytes on Linux despite the same
  declared library version. Generator v3 specifies a simple uncompressed PNG
  encoding independently of platform compressors. Source pixels and document
  meaning stay unchanged; the new compressed-byte-independent fixture encoding
  and its dependent hashes replace v2 in this release. This supersedes the
  preceding metadata-only correction, not its recorded observation. Six RED
  cases cover backend independence, multiple DEFLATE blocks, unsupported pixel
  mode and preflight ordering, then pass after the correction. No dependency,
  OCR verifier, Core runtime or ontology changes are introduced.

Python 3.10 also found the existing supplier initialization helper passing UTC
`Z` directly to a stdlib parser that only gained that spelling in Python 3.11.
The helper normalizes the parser input to `+00:00` while retaining the original
transaction-time text in ledger records. The Core supplier replay test now
exercises a Python-3.10-shaped parser on every platform. This is compatibility
for an existing fixture, not the pending undesired-observation integration.

The measured GitHub Python 3.12 suite took 27 minutes 44 seconds by itself.
The final main/release test allowance is therefore 45 minutes, leaving room
for declared installation and documentation steps. No test or platform is
removed. The original 30-minute adjustment above records the earlier local
measurement, not the final workflow setting.

Corrective checks: 79 status/OCR/CI tests pass. The supplier replay test fails
against the old UTC parser and passes after normalization. All 10 rewritten
PNGs retain exact dimensions, mode and pixel bytes; neither source PDF changes.
All 354 governance commit references resolve from the main commit and the two
evidence tags verified on GitHub. The subsequent clean full/package gates and
remote matrix still determine release readiness.

## Publication gate

Run the configured full test/documentation gate and package checks from a clean
exact commit, not the shared dirty checkout. Record actual counts and skips.
Keep direct-versus-sdist package parity and installed smoke checks, without
adding a new dependency-locking project. Push main first, then the matching
immutable version tag. The remote release workflow owns publication to PyPI.

The GitHub MCP connector can inspect refs but cannot transport the local Git
history or create a release tag. The operator authorized a narrow native-Git
exception for this publication. Other server operations continue through MCP.

The in-progress undesired-observation Re-entry integration is consumer-owned
and excluded from this release. Its future main landing remains a separate
Core-reviewed transaction after this frozen release boundary.

The maintained projection still verifies retained prefix bytes and copies
state. Actions still use repository-local producer/profile helpers. External
effects, source truth, general ontology migration, a stable action SDK and
multi-writer persistence are not release claims.

## Verified release candidate

The frozen release commit is
`e2b9e77912f9b36fdbfe2fca310548a789bffb4d`, tree
`162325eb0048816654d2df5b6b0f00270d06385d`. Its source tree is
`3b4fd1c9eb66d84c31050b5f0fd970a6fc2572a8`. Governance validates 447 entries at
`OVR-000447`, head
`sha256:a4c495ab75674ac49f73581d2e5ae2586eaa72a057370a169333a6d5b1b64d84`.

A clean detached checkout ran the configured `scripts/ci.py all --require-clean`:
3,359 tests passed, 3 skipped, with one RDFLib deprecation warning; the separate
GraphRecipe and Small Shop selections passed 40 and 229 tests respectively.
Strict HTML and doctest passed. The invocation exited 1 only when sandbox DNS
prevented external link checking. The unchanged `scripts/ci.py docs --require-clean`
then passed with network access. This is a composed verification result, not a
claim that the first `all` invocation exited successfully.

The configured `scripts/ci.py package --require-clean` also passed with network
access for declared build/install dependencies. It built the wheel and source
archive, checked their metadata, verified direct-versus-source-archive wheel
member parity, and passed clean-install CLI smoke checks. The verification
checkout remained clean. Local distribution identities are:

| Distribution | SHA-256 |
| :--- | :--- |
| `malleus_dev-0.14.0-py3-none-any.whl` | `e99ca688d07190aca7abb132909d3df22debef5db930924ba4e5fb3d0f307714` |
| `malleus_dev-0.14.0.tar.gz` | `e6cc4e1a381d92727a21591dc607498e75a3dda67ac9be6eafda0725698686bf` |

[Main CI run 34285960797](https://github.com/Kieleth/malleus-dev/actions/runs/34285960797)
passed on that exact commit. Each Linux Python 3.10, 3.11, 3.12 and 3.13 job
passed 3,359 tests with 3 skips, then 40 GraphRecipe tests. Python 3.12 also
passed strict documentation. The narrower Windows Recon job passed 144 tests;
it is not full Windows-suite evidence.

The annotated `v0.14.0` tag was published at that commit. Its tag-object identity
is `fcc969f9ade029db05890c88f591e2f84db04546`; it is not cryptographically signed.
[Release run 34288358949](https://github.com/Kieleth/malleus-dev/actions/runs/34288358949)
has passed immutable-ref validation and the package gate. Its distribution
bundle is [artifact 10080386835](https://github.com/Kieleth/malleus-dev/actions/runs/34288358949/artifacts/10080386835),
ZIP SHA-256 `ecf4f3ab7525ba6edf32c92da4c2aaa65b71d7f7d10d9d63606eb3a4dc79e464`.
The release matrix passed on all four declared Python versions, each with
3,359 tests passed and 3 skipped, followed by 40 GraphRecipe tests. Python 3.12
also passed strict documentation. Publication job `102277414615` verified the
downloaded distribution bundle digest and successfully uploaded both files
through the configured PyPI trusted publisher on September 8 at 23:32 UTC.
The publisher log records the same wheel and source-archive hashes listed above.
[Malleus 0.14.0 on PyPI](https://pypi.org/project/malleus-dev/0.14.0/) is the
published package coordinate. Release run `34288358949` finished with success.
No GitHub Release page was created; the Git tag and PyPI publication are the
release artifacts. The release tag remains fixed at the tested commit, not at
this later documentation update.

The separately approved Re-entry merge was checked only in an isolated clone:
merge `6f739b8b828c2e74a0a06b78b89043744183e02c`, tree
`446594e9e191cd6da07f5d7a4d19998977fce6d2`, combines this release candidate with
the frozen consumer tip `3724f70190f7720f234c2c3290aee69975116c17`.
All 18 maintained-reader and consumer-epoch tests passed. The combined ledger
check also passed, and the checkout stayed clean. This is not a main landing,
push, publication, or rebind of the earlier consumer receipts.
