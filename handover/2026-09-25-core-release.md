# Core release preparation, 0.15.0

Luis asked for Core to be merged and released. This record covers the release
candidate only. The Overlord seals the governance ledger, merges to main,
pushes and tags. None of those acts is claimed here.

## Scope

Publish the Python reference implementation as it stands on branch
`core/t3-enum-integration`: everything since 0.14.0 (2026-09-08) that the
changelog lists. That is T2's exact historical reads, T3's declared
`TRANSITION` and `REVISION` supersession under structural builtin version 2
(route C) with the state-version successor profile (route D), `ADD_ENUM` in
additive revision, check-contract re-binding, the check-contract grammar and
the `check_and_admit_*` operations (decision D closes caller-supplied check
events), ontology-gap answers (ROADMAP F2), the shipped-ontology profile
declaration, the hardened command-line reads and the sdist include fix.

Out: the standalone Assent stage stays 8c. Root ontology 0.4.0 and Assent
ontology 0.11.0 do not move. No `paper-v4/` or `private/` path is in the
forward diff from main. The unsealed branch-local draft `OVR-000483` stays as
it is. Wire formats named experimental in 0.14.0 stay experimental.

## Version

**0.15.0**, a minor pre-1.0 release. `pyproject.toml`,
`malleus.IMPLEMENTATION_STATUS.package_version`, the README, the status
document and the changelog name it. The status history gains a 0.15.0 row.
`CHANGELOG.md` turns `[Unreleased]` into `## [0.15.0] - 2026-09-25` with a lead
paragraph, under a fresh empty `[Unreleased]`.

## Candidate

Base: main and `origin/main` both at `ebff70f72dc4cd67b2f910b88575e558a2824728`
as read locally; the remote was not fetched. The branch is 35 commits ahead
after this record and 0 behind.

- RED `6567e8d4`: `tests/test_status.py` and the README claim in
  `tests/test_docs.py` expect 0.15.0. 2 failed, 12 passed.
- GREEN `4412d568`: version, documents, changelog and the regenerated
  measurements below. The same selection: 14 passed.
- This handover, in the commit after GREEN.

## Regenerated through declared producers

Nothing was typed by hand.

| path | producer | what moved |
|---|---|---|
| `conformance/ocr/v0/corpus/corpus.json`, `checksums.json` | `python conformance/ocr/v0/corpus/generate.py write` | `malleus_version` 0.14.0 to 0.15.0 and the digest of `corpus.json`; all 67 case artifacts byte-identical, checked by hashing every corpus file before and after |
| `conformance/contract_compiler/v0/bundled_declaration_scan.json` | `scripts/contract_compiler_duplicate_scan.py --write` | only `pyproject.source_sha256`; `--check` passes |
| `conformance/contract_compiler/v0/evidence/CC-X01-environment-contract-correction.json` | `scripts/contract_compiler_ledger.py refresh-evidence` | only the `pyproject.toml` artifact digest |

`pyproject.toml` moved from `sha256:7c6d162b…` to `sha256:8cec9bd3…` with the
same byte length. The last two rows are a release step that 0.14.0 did not
need: since the sdist include fix of 2026-09-22, CC-X01 and CC-X02 bind
`pyproject.toml`'s exact bytes, so every version change moves them. The first
full run found it as four failures (one in
`tests/test_contract_compiler_divergence.py`, three in
`tests/test_contract_compiler_duplicate_scan.py`).

## Corrections found

1. Four labels called shipped work "unreleased" and would be false once 0.15.0
   ships: `KnowledgeChangeHistory.replay_at` in `docs/IMPLEMENTATION_STATUS.md`,
   `docs/contract_compiler/index.md` and
   `.claude/skills/malleus-dev/references/CAPABILITIES.md`; the T3 kind field in
   `docs/IMPLEMENTATION_STATUS.md`; and the changelog entry "Unreleased exact
   historical compiler-history reads". Each now says "new in 0.15.0", or drops
   the word in the changelog entry.
2. The `[Unreleased]` section had two `### Fixed` headings. The second one's two
   entries now sit under the first. Entry text is unchanged.

Spot checks that found nothing wrong: the changelog's refusal counts (eleven
gap-answer, seven ontology-source, nine composition reasons), the six
`POPULATION_GAP_KINDS`, and the five route C and D identities all match the
running code.

## Test evidence

All local, macOS arm64, Python 3.12, `/Users/luis/Projects/malleus-dev/.venv`,
no paid model calls.

Full `pytest -q` at `4412d568`: **24 failed, 3,815 passed, 3 skipped**, one
warning, 901 seconds. All 24 are the governance guard,
`OVR-000479: latest document digest mismatch for pyproject.toml`, which holds
until the ledger records this branch's documents:

- `tests/test_contract_compiler_integration.py`: 14
- `tests/test_contract_compiler_ledger.py`: 7
- `tests/test_docs.py`: 3 (Sphinx builds; the manifests page validates the
  ledger)

The earlier run on the uncommitted GREEN tree, before the CC-X01 and CC-X02
regeneration, had 28 failed, 3,811 passed, 3 skipped: the same 24 plus the four
named above.

`ruff check` over the `scripts/ci.py` quality paths: all checks passed.
`scripts/contract_compiler_ledger.py check` fails on the same governance guard.

`scripts/ci.py package --require-clean`, with `PYTHONPATH` unset so the smoke
environment imports the installed wheel: `[ci] package passed`, exit 0. Build,
`twine check`, direct-versus-sdist wheel parity and clean-install smoke of the
four commands passed. Local distribution identities:

| Distribution | SHA-256 |
| :--- | :--- |
| `malleus_dev-0.15.0-py3-none-any.whl` | `fbbf02c9432ba4383b94ccfba089b75f092995b8584288cb0a5610397d0945f6` |
| `malleus_dev-0.15.0.tar.gz` | `cf583861fbba23954b69030da537ee2b2b4d93122dceed21b7437f22ba87679f` |

These are local builds, not the release job's. A first run with `PYTHONPATH`
pointing at the checkout also passed, but its smoke step imported Malleus from
the checkout, so it is not counted.

`scripts/ci.py docs --require-clean`: `docs-html` failed with status 2 on the
same governance guard. The strict HTML, doctest and link-check builds did not
run and are unverified.

## Before tagging

1. Seal the governance ledger for this branch's documents, then rerun
   `scripts/ci.py test --require-clean` and `scripts/ci.py docs --require-clean`
   on the sealed commit. The release job runs both; `test` starts with the ledger
   check, so it cannot pass before the seal.
2. Merge to main and push. The tag `v0.15.0` must sit on main history and equal
   `pyproject.toml`'s version, or `validate-release` refuses it.
3. Tests outside `testpaths` were not rerun for this candidate. Their state at
   the integration pass is in `handover/2026-09-24-t3-enum-integration.md`.
