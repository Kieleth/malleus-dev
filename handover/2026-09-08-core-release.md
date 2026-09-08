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

Proposed version: **0.14.0**, a minor pre-1.0 release, pending the operator's
version confirmation. The existing `v*` tag workflow requires the exact package
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

The full clean baseline exposed an old producer binding in the current
inspection-note trace tests. Compiler-view change `8d315fbd` altered retained
producer evidence, but that current test still selected the preceding v2
execution. Its producer mismatch is an intended refusal, not a failed
source interpretation or a reason to weaken the identity check.

The separate `inspection_note_execution_v3` records the actual current
preparation result. All earlier evidence stays byte-identical. Only
`base_ledger_head` differs from the historical change set; domain operations,
source/evidence identities and valid time agree. Preparation, admission, reopen
and per-record trace all execute. The document boundary passes 22 tests;
status tests pass 13. Neither is a full release receipt.

## Publication gate

Run the configured full test/documentation gate and package checks from a clean
exact commit, not the shared dirty checkout. Record actual counts and skips.
Keep direct-versus-sdist package parity and installed smoke checks, without
adding a new dependency-locking project. Push main first, then the matching
immutable version tag. The remote release workflow owns publication to PyPI.

The GitHub MCP connector can inspect refs but cannot transport the local Git
history or create a release tag. A narrow native-Git exception was requested
from the operator; no shell-based server access has been used.

The maintained projection still verifies retained prefix bytes and copies
state. Actions still use repository-local producer/profile helpers. External
effects, source truth, general ontology migration, a stable action SDK and
multi-writer persistence are not release claims.
