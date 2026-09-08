# Semantic Re-entry: verified local main landing

The completed supplier experiment is integrated locally. No push or publication
occurred. Core performed integration and governance only, not another consumer
implementation or public-runtime promotion.

## Frozen coordinates

- Previous Core main: `f3bcb620076da560476b3facdc3bf45dd7f214c4`.
- Fast-forwarded integration: `6f6453ee20b27405b251ba29f830cc0a8ce51862`,
  tree `836a825fb9bd7ae9c0822db2dc87d4e1ce80a0c8`.
- Final implementation/governance freeze:
  `a96e9e0dcb8a0475da3cd065b05ffd080b0f288e`,
  tree `7bc112140c67e7b9893790506e6757f5c47dbda5`.
- Ledger: 436 entries, `OVR-000436`, head
  `sha256:27bb362785c5fa4b15377cdc3ef56e60fbb969119fec2528e86c415c6cc8e484`.

The commit containing this receipt adds only the receipt after that freeze.
Historical branches, RED/GREEN commits, proof outputs and receipts are retained.

The incoming 100-file delta contains only
`research/semantic_reentry_external_design/` and a 23-line addition to
`.claude/skills/malleus-acolyte/SKILL.md`. The skill changed from
`sha256:4c74a274c52e34feff3493f9ee935fea908c6914e83a0006ba0918f260f9c06d`
to `sha256:e20f33af0159be22bbe16877fe4c28ce038aee93dad6c713447be3da641c65c6`.
The document revision binds that change and the incoming manifest, whose hash is
`sha256:a2907c4c8703fb764acf9ee95ac45ca03e3de70a699785b4451662c6fbe3922e`.

All 99 manifest content hashes, 18 fresh lifecycle/walkthrough artifact hashes,
and both retained JUnit hashes were checked before landing. The manifest is the
100th file and excludes itself from its content list. Ancestry, clean target paths,
empty index and exact permitted scope were checked before the local-only fetch
and fast-forward. No Core runtime, ontology, action-producer, package or Small Shop
fixture byte changed relative to the previous Core main. Unrelated tracked
Paper and Recon edits remained byte-identical; no unrelated file was staged.

## What this demonstrates

The research-local reference implementation starts with supplier quantity 1
and an explicit local goal of 2. It proposes an action, authorizes and executes
one controlled source-file amendment, independently observes the bytes,
proposes an ordinary KCS, admits it and replays quantity 2. Running the goal
again then emits no proposal. Execution receipts alone never change the KG.

The implementation claims only its selected experimental single-action and
state-version profiles. The exact-two goal, strategy and supplier semantics
are adopter choices. Tests and receipts are conformance evidence, not protocol
vocabulary. This does not establish a general planner, a shipped Re-entry API,
physical delivery, source truth, retries, exactly-once effects, independent
replacement, Robotics integration or delegation to the newer input constructors.

Start with the [supplier walkthrough](../research/semantic_reentry_external_design/SUPPLIER_WALKTHROUGH.md).
Its command uses a new output directory and the configured repository environment.
The [incoming landing report](../research/semantic_reentry_external_design/CURRENT_CORE_LANDING.md)
preserves the earlier test coordinates rather than relabeling them as this run.

## Validation

Retained consumer runs, independently checked here:

- Combined gate at `a857ef0`: 426 passed, 1 existing private-doctrine skip.
- Post-synchronization focused gate: 27 passed, the same skip.

Fresh local-main runs used `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:.`,
`.venv/bin/python -m pytest -q -p no:cacheprovider`, and `--tb=short`:

| Exact selection | Result |
|---|---|
| `tests/test_inquisition.py::TestSkillsAreInstallable`, `tests/test_inquisition.py::TestShippedGuidanceSaysWhatTheCodeDoes`, `research/semantic_reentry_external_design/test_supplier_replay_laws.py`, `research/action_history_contract_freeze/programs/test_action_inputs.py` | 36 passed, no skips or failures |
| `tests/test_governance_git_scan.py`, `tests/test_contract_compiler_ledger.py`, `tests/test_contract_compiler_integration.py` | 366 passed, no skips or failures |
| At committed `a96e9e0`: ledger `test_overseer_ledger_and_projection_are_current`, ledger `test_latest_document_revision_must_match_current_bytes`, integration `test_canonical_integration_manifest_is_valid` | 3 passed |

These are scoped runs in the shared configured checkout, not a clean full-suite
claim. Unlike the isolated consumer clone, the local checkout contains the
optional private doctrine, so that guidance check passed instead of skipping.
JUnit files are temporary evidence under `/tmp/malleus-reentry-main.FD3yHf/`:

- `focused.xml`: SHA-256
  `efc6f1b85a18a59bf3b41990ebfb0e2ecd20870f199b324ff066ef0b3268b98e`.
- `governance-final.xml`: SHA-256
  `f97999a9dfe835d0b6c7b72662d84c31e8d5a0883a02f81930ccb7d976d4e6c6`.
- `committed-head.xml` records the final three guards.

The standalone ledger check validates all 436 entries. Scoped Git diff checks
pass. During preparation, the existing schema rejected this writer's overlong
uncommitted explanation. The interrupted test run against that invalid draft
is not counted as a gate. The explanation was shortened, its hash recomputed,
and the projection regenerated before the complete successful rerun. Neither
the schema nor any validation rule was weakened.

Scoped self-inquisition: the optional profile remains optional, the consumer
remains research-local, and no fixture acquired Core authority. Future consumer
changes still require exact evidence and a separate integration decision.
