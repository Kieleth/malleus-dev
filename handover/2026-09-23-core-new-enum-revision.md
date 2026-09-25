# Core candidate: adding a closed vocabulary to a live history

Status: implemented, uncommitted candidate. No consumer rebind, publication,
release, staging, or Git ref change is authorized by this handover.

## Scope and reason

Luis approved the bounded Core correction and sharing its findings with the
KGs reentry loop task. The adopter chooses the vocabulary and what its values
mean. Core must be able to add that vocabulary through its existing governed
revision path without changing the meaning of the earlier ledger prefix.

For example, an adopter can introduce an `Assessment` record with status
`PENDING` or `CONTESTED`. Previously source composition and ontology compilation
accepted that addition, but live revision compilation rejected the new enum
declaration. It recognized enum values without recognizing their new enum.
This was a missing capability, not a regression against the documented promise
of adding enum values.

The change adds `ADD_ENUM` alongside `ADD_ENUM_VALUE` in the existing revision
delta. A successor policy admits the new kind. Both historical policy artifacts
retain their exact bytes and permissions. No new public function, dependency,
history format, domain concept, or review authority is introduced.

## Baseline and exact candidate

Baseline commit: `ebff70f72dc4cd67b2f910b88575e558a2824728`.
Baseline tree: `7b9a81fb35c5cb2016830c289915a359fed7162f`.

The candidate is that baseline plus the eleven files listed below, not the
whole shared worktree. Unrelated paper, research, and roadmap edits are excluded.
An exact overlay archive is retained at
`/private/tmp/malleus-enum-candidate.4KEq1d/enum-overlay.tar`, SHA-256
`b687a960cdf9acf7d8bf94d1d3c4bab10ec9c123ed38343145740ac0ed75704b`.
The archive excludes this report to avoid a self-referential identity. It is a
local review artifact, not a package or permanent publication.

| Path | SHA-256 |
| --- | --- |
| `src/malleus/_contract_pipeline/revision.py` | `b2d20092bb1f9fb7fd5c3c20fc06f9aa187321bbd14a06cb04eea9f1de4ff51f` |
| `src/malleus/_contract_pipeline/knowledge.py` | `cd30fdbc5a6764781848c3e7e4f225cb5cbf1b2a565779d64ac6a49425e14488` |
| `tests/contract_compiler/pareto/test_new_enum_revision.py` | `65d797ed23c5dc652fe6453b18a7b944ad54605230a2036abae243580da7702e` |
| `tests/contract_compiler/pareto/test_contract_revision.py` | `356405664599410053bf3f7b26fecb422b871bb16ae983afffda5bfde38a767e` |
| `tests/contract_compiler/pareto/test_check_contract_rebinding.py` | `45883769c8c02c96fb5ee90d397630a4a7c500d71dbe94a77dbd1f4c957411c9` |
| `tests/contract_compiler/pareto/test_ontology_gap_answer.py` | `c7982a6196cffa761d9f6b94ce29c86c1decc71bd933e3ab27fe261d3b803ac9` |
| `.claude/skills/malleus-dev/references/CAPABILITIES.md` | `d3fe63238833d26766ef65745720dab8fb28a189ce4dfe0b82215eb8215eded2` |
| `docs/IMPLEMENTATION_STATUS.md` | `d3106eedf6388a2d8c5d246800caa2e1d49fea7c40a6d983879dd0d048f40d8f` |
| `docs/contract_compiler/index.md` | `ae7c342597abcee42d0d23177cfaa7e5bf74cd62b4ac54c07c2334b9c64eda42` |
| `docs/reference/index.md` | `c9ef53f19834fe98d8b3b4f29c5e3ba3fed0e2794289aa0f7b8dabf2e79f7a48` |
| `tests/test_docs.py` | `750fc942de741c4414352948be48feb9036b184241f8e2b7bf62b99df0e5484b` |

## Policy identities and compatibility

- Original: `sha256:05b6880517ae8287333973e421248e2eb803c2f50569adcea26ca114d154ce8e`.
- Previous, including check-contract rebinding: `sha256:e129b6e87bd06abc8d23b22bdefee2142c07574237b273a068040fc14d09db59`.
- Successor, including `ADD_ENUM`: `sha256:a2580f914cf91ccfea9374e5929d6d5f4892252c93caa3734a24dd332c9a8ede`.

Recorded revisions execute their named policy. Both earlier policies refuse
`ADD_ENUM`; neither is retroactively broadened. A history can retain an old
revision and then append a successor-policy revision with a chained migration
receipt. Its existing bytes remain an exact prefix.

Proposal retention still probes additivity using the current default policy.
It does not persist a separate historical proposal-policy identity. Acceptance
records the exact revision policy. Tests cover previously valid pending and
accepted proposals under the predecessor policy without changing their ledger
bytes. This is not a claim that proposal policy pinning has been implemented.

New revisions have new identities even when their resulting domain graph is
the same as an older example. Older runtimes are not claimed to understand the
new revision kind. Frozen consumer receipts have not been regenerated.

## TDD and verification

Tests use neutral synthetic records and two existing Core consumer paths:
population-plan history and composed-change-set history. They exercise proposal
retention, revision acceptance, enum-constrained admission, ledger-only reopen,
and preservation of prior entities, relations, record versions, and prefix bytes.

Final new test file against an untouched exported baseline: **7 failed,
5 passed**. Against the candidate: **12 passed**. The failures on the baseline
are the new policy/declaration classification and the previously blocked live
revision paths. Negative controls remain green. There is no RED commit because
commits were not authorized. An early RED attempt also exposed an overbroad
test-only string replacement; it was corrected before the meaningful RED run.

Commands use the existing declared project environment, with bytecode and pytest
cache writes disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/contract_compiler/pareto/test_new_enum_revision.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/contract_compiler/pareto/test_new_enum_revision.py tests/contract_compiler/pareto/test_contract_revision.py tests/contract_compiler/pareto/test_check_contract_rebinding.py tests/contract_compiler/pareto/test_ontology_gap_answer.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_docs.py -k 'repository_python_examples or approved_eval_rst_island'
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/contract_compiler/pareto tests/test_capability_declaration.py
```

Focused revision, historical policy, check-rebinding, and gap-answer suite:
**78 passed** from the final frozen overlay on the exported baseline, excluding
all unrelated worktree edits. Final exact-overlay documentation selection: **6 passed,
123 deselected**. Broader Pareto/capability suite: **986 passed, 1 failed**
in 593.50 seconds. This gate is not green.

The failure is
`test_fresh_shop_import.py::test_fresh_import_replays_and_traces_after_complete_shop`.
It compares newly generated Shop evidence with frozen predecessor-policy bytes.
The exact same test passes on the untouched baseline (**1 passed**). A fresh
run from the frozen candidate completed and was compared with that baseline:

- Both histories contain 59 events. The first changed line is 30, the contract
  revision. It selects the successor rather than predecessor revision policy.
- Exported records and complete temporal record histories are equal. Both graph
  state digests are
  `sha256:ac6bc4c2a6be7ee851e0229b49276b11a8e0dbf91ed203705d611093c783e998`.
- The only changed report fields are `ledger_head`, `ledger_sha256`, and
  `receipt_identity`. Source identities, records, derivations, counts, and the
  prior-record-preservation result are unchanged.
- Candidate diagnostic output is retained at
  `/private/tmp/malleus-enum-candidate.4KEq1d/shop-diagnostic/`.

This is an integration dependency, not permission to rewrite old evidence. The
Shop owner must record an explicitly selected successor evidence generation
before the broader gate can pass. No research runner, binding, fixture, or
consumer assertion was edited or bypassed by this correction.

Ruff check, Ruff format check, and scoped diff check pass on the changed Python
files. No complete repository, package, or final governance gate is claimed.

## Boundaries and next step

Removal, narrowing, changing an existing range, changed imports, stale revision
bases, and undeclared enum values remain refused. Retaining a proposal alone
does not activate its vocabulary or create domain records.

This is a mechanism in the optional compiler-enabled semantic-history profile.
It does not assess scientific truth, choose whether a new concept is warranted,
change an adopter's admission policy, or perform semantic repair automatically.
The requesting research task owns its domain model and independent consumer
experiment. It should verify the frozen candidate before proposing a rebind.
Commit, integration, and publication remain separate unapproved steps.
