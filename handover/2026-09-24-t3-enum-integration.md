# T3 and ADD_ENUM integration, route C with route D

Branch `core/t3-enum-integration`, from `aadddfe8` (tip of `codex/core-temporal`,
base main `ebff70f7`). Not sealed, not merged, not pushed. Luis authorized the
pass: "land T3 with ADD_ENUM in one pass". Ruling R-07
(`design/temporal/g4/RULINGS.md`) required route C together with route D before
T3 reaches main.

## What landed

1. `core/add-enum-revision` (`acbdd296`) merged with `--no-ff` as `c4b6e656`.
   No conflicts. Four files auto-merged (`CAPABILITIES.md`,
   `docs/IMPLEMENTATION_STATUS.md`, `docs/contract_compiler/index.md`,
   `knowledge.py`); the two changes touch different paragraphs and lines.
   After the merge: the ADD_ENUM files and the T3 temporal files, 129 passed.
2. Route C. Core's structural builtin `malleus.core.operations-apply-atomically`
   has version 1 and version 2. Version 2 applies `supersession_kind`
   (`TRANSITION`, `REVISION`). Version 1 keeps its behaviour and refuses the
   field with the new reason `SUPERSESSION_KIND_NOT_SELECTED`. Replay reads the
   version from the history's own retained check contract under each required
   identity, so a history whose policy does not require version 2 refuses the
   field by every door: the check, and replay, which also covers
   `admit_structural_change` (it appends Core-authored events without running
   the builtin). Route A's weakness, the same identity with different
   behaviour, is gone. `_apply_change` defaults to the version-1 behaviour.
3. The shipped default names version 2: new files
   `src/malleus/profiles/structural-admission-check-v2.json` and
   `structural-admission-policy-v2.json`. The version-1 files keep their paths
   and bytes. `SUPPORTED_STRUCTURAL_HISTORY_BUNDLES` holds both;
   `create_structural_history(bundle=...)` selects one explicitly (default
   `STRUCTURAL_HISTORY_BUNDLE`); `admit_structural_change` finds the bundle the
   history recorded and writes that bundle's events.
4. Route D. `STATE_VERSION_PROFILE` is a successor,
   `src/malleus/profiles/state-version-v2.json`: `correction` maps to
   `REVISE_STATE_VERSION`, `transition` stays `SUPERSEDE_STATE_VERSION`, nothing
   else moved. The predecessor keeps `state-version.json` and its identity in
   `SUPPORTED_STATE_VERSION_PROFILES`.

What executes the state-version profile, read before changing it: Core parses
`change_semantics` as closed text fields and executes none of the values. The
profile's identity is bound in population plans (`history_profile`), in
change-set evidence, in the trace (`_trace_profile` reads the retained bytes,
not the shipped constant), and in a transition program's
`admission_rules.history_profile_identity`. When a transition program runs,
Core reads only the profile's `ontology_roles`. So route D moves identities,
not behaviour. The predecessor is kept because a transition program or a plan
may pin its identity; replay itself uses retained bytes.

## Identities, read from Core

| artifact | before | after |
|---|---|---|
| structural check contract | `sha256:b923c279024e7a2cf18fab86b2e9e80e8f5afecbd8e7da83be437f2fba228f41` | `sha256:9c25c6db82ad6ddc29b6123b5b5592ea4cd07096102ac2b442b681de6b2cc8ca` |
| structural admission policy | `sha256:c1d696f237a80c15b07bafaa65e465d0c5d244fcea709fb79639b216ac507557` | `sha256:8239b685f42cdb5683465d87c06ab7a798b5b3de2379573e0baa28a5d1717560` |
| normative profile | `sha256:a39681c4e359a4ab66e4120e90aa05c3dbae052d5653bd2872a80c88b2423a40` | `sha256:b704e7fb8a08bb54f4481d34bc334396e4e2f8ebe1ca17b919164ca6e4c56c95` |
| structural history bundle | `sha256:8a994ed00fef8a253069808eaf68d429ed29fe2869eefe6cd30bd426c31977e8` | `sha256:5a5e0aca990d7ef4fd14b301c6d004cf319d92542608bab12cdb279d130788be` |
| state-version profile | `sha256:b18f3129942761e03ce754af6cec8c689c94b91468aa105a423f5b27ddf20dc3` | `sha256:5f6bd9ebab38f7a0ee1070ef9718b7b9b99124e34e9c42fa00b7fd30cd450d51` |
| contract revision policy (ADD_ENUM) | `sha256:e129b6e87bd06abc8d23b22bdefee2142c07574237b273a068040fc14d09db59` | `sha256:a2580f914cf91ccfea9374e5929d6d5f4892252c93caa3734a24dd332c9a8ede` |

The four route C values equal G3's prediction. The state-version value differs
from G3's `e2c8e163…`, which used `CORRECT_STATE_VERSION`; this pass uses
`REVISE_STATE_VERSION` after R-08.

## RED and GREEN

`tests/contract_compiler/pareto/test_structural_builtin_v2.py`, committed first
(`f8accd8c`): 10 tests, 9 failed and 1 passed on the untouched Core. The pass is
"a new structural history retains the shipped check", true before and after.
GREEN (`a098f592`): 10 passed; with the T3 and executor test files, 45 passed.
The GREEN commit also carries a lint fix to the RED file (a local fixture in
place of an imported one, and formatting); no assertion changed.

## Full suite

`pytest -q` after regeneration, started at `a8ee703e`; the docs commit `3d6bb31c` landed during the run and changes no code:
**24 failed, 3815 passed, 3 skipped.** All 24 are (a), the expected governance
guard: `OVR-000475: latest document digest mismatch for tests/test_docs.py`.
The merge brought ADD_ENUM's `tests/test_docs.py` edit; the validator stops at
the first mismatch, so the other governed documents this branch moves
(`docs/IMPLEMENTATION_STATUS.md`, `CAPABILITIES.md`, `knowledge.py` and more)
are behind it. 7 in `test_contract_compiler_ledger.py`, 14 in
`test_contract_compiler_integration.py`, 3 Sphinx builds in `test_docs.py`.

The first run, before regeneration, had 51 failed and 5 errors. The 27 non-(a)
failures and 5 errors were classes (b) and (c) and are all fixed:

| class | tests | cause | fix |
|---|---|---|---|
| (b) | `test_check_contract_executor.py`: 3 | the registry now holds version 2 | expectations name both versions; the probe calls version 1 through the registry |
| (b) | `test_temporal_revision.py`: 2 | the route-A guard pinned v1 identities; the rule-layer case used a v1 check | the guard now proves only identities moved (same records and graph as a v1 history built explicitly); the rule-layer case requires version 2 |
| (b) | `test_domain_history_profile.py`: 2, `test_governed_population.py`: 2, `test_population_plan.py`: 1 | the successor profile | expected data names `REVISE_STATE_VERSION`; the identity pin is written from Core; the public surface lists `SUPPORTED_STATE_VERSION_PROFILES` |
| (b) | `test_inquisition.py`: 1 | `.claude/skills/malleus-acolyte/SKILL.md` worked plan named `b18f3129…` | the example names the successor identity, written from Core |
| (c) | Shop: `test_fresh_shop_import.py` 10, `test_small_shop_default_admission.py` 4, `test_partial_shipments.py` 3, `test_maintained_projection.py` 1, `test_default_shop_walkthrough.py` 1, `public_population/test_run.py` 2, `test_compiler_cli.py` 5 errors | the five Shop plans pinned `b18f3129…`; the ADD_ENUM revision policy moved the fresh-import and public-population evidence | plans repinned; successor evidence generation |

Outside `testpaths`, run separately:

- `research/ontology_driven_kg_realization` except the connected story, with the
  Shop pareto tests: 691 passed, 1 failed, 1 skipped. The one failure,
  `document_paper/test_v2_experiment.py::test_driver_recompiles_the_exact_accepted_ontology_coordinate`,
  also fails on a `git archive` of `ebff70f7`. Not this branch.
- The connected story: 112 passed after its re-cut.
- `design/temporal/g1` and `g3`: 220 passed, 2 failed. See "Where meaning moved".
- `research/methodology_gedanken_e2e` 31 passed; `design/temporal/g2a` 38
  passed; `design/temporal/g2b` 40 passed.
- `research/semantic_reentry_external_design`: 470 passed, 4 failed, 2 errors.
  Three refuse "Unreviewed Core source epoch: cfb8eacc…" and one expects the
  reviewed epoch `763d3b72…`; the two errors need `MALLEUS_REENTRY_CORE_ROOT`.
  These gates pin a reviewed Core source epoch, so any Core source change
  trips them; recording a reviewed epoch is a review act, not a regeneration,
  and was not done. Not run on the base, so not attributed between T3, ADD_ENUM
  and this pass.
- `research/semantic_reentry_protocol`: 75 passed, 1 failed, 1 xfailed.
  `test_integration.py::test_observed_correction_admission_reopen_trace_complement_and_quiescence`
  differs from its pinned values in digests only (`final_ledger_sha256`,
  `contract_identity`, base coordinates, as far as the diff shows). It also
  fails on a `git archive` of `ebff70f7`, so it is not attributed and was not
  regenerated.
- `conformance`: 7 passed, 1 failed (`ModuleNotFoundError: No module named
  'boundary'`); also fails on the `ebff70f7` archive.
- `research/action_history_contract_freeze` (blocked audit, kept at its own
  Core): 589 passed, 3 failed, 20 errors. The errors are
  `CALLER_SUPPLIED_CHECK_EVENT`, the two-step door closed by decision D; the
  three `test_contract_inputs.py` failures also fail on the `ebff70f7` archive.

## Regeneration table

All through the artifact's own producer; nothing typed by hand.

| path | producer | old identity | new identity | what else is equal |
|---|---|---|---|---|
| `research/.../small_shop/public_population/plans/*.json` (5) | script that rewrites `history_profile.sha256` from `STATE_VERSION_PROFILE.identity`, checking each file is canonical before and after | `b18f3129…` | `5f6bd9eb…` | every other byte |
| `research/.../small_shop/evidence_2026_09_24_t3_enum_integration/` (new generation; predecessor `evidence_2026_09_20_core_runs_checks` kept) | the five scenario producers (`run_full_shop`, `run_object_event`, `run_correction`, `generate_evidence`, `fresh_import.run.run_import`) | public population `sha256:f0814b4842dc2aa9133e6912e9f915cd9ea8a24d7b6af4355a64ad84137b2cb0`; fresh import `sha256:36220dd940a917414e3d54587d1ded942ee1c45b8e48f9c846dd004d6d3a7c7d` | public population `sha256:24be9101c9bf0c0de96a113fca1be9efe227fa70467575c3812f9e840ee49eba`; fresh import `sha256:59848d94e5b3f821fc6545aae3edd0c68ecce88daf54758594f7765904a010fa` | public population: 46 leaves moved, all sha256; `graph` and `graph_state_digest` equal. fresh import: 3 leaves (`ledger_head`, `ledger_sha256`, `receipt_identity`). object event, correction, showcase: byte-identical. Compiler artifacts equal. |
| `research/.../small_shop/connected_story/` 8 receipts, 30 values | the stages' own functions in chain order | e.g. Table 1 ledger `dcd140c5…` | `0de63c15…` | graphs, record histories, three state digests (`4a890bb0…`, `e5f36981…`, `57e3839c…`) and reader reports equal to `ebff70f7`; reports differ only in history coordinates. `contract_facts` did not move. |
| `research/.../small_shop/evidence_assertions.py`, `test_current_evidence.py` | edit | `CURRENT` 09_20, 40 historical outputs | `CURRENT` 09_24, 50 | |

The superseded and current pair of every connected-story value is in the new
generation's `binding.json` under `connected_story_chain`.

## Adopters

Adapted in this branch: `research/.../small_shop/public_population/plans`
(route D), the Shop evidence and connected story (regenerated),
`design/temporal/g3/blast_radius.py` (measures from the v1 bundle and the
predecessor profile, selected by content, because that is what shipped at its
base), the acolyte skill example. The research correction runner calls
`_apply_change` for its own version-1 algorithm; it needs no edit because the
parameter defaults to version 1, and its declaration pins its own entrypoint
bytes. A first attempt edited it and broke that pin; the edit was undone
(`0376eae4`).

Not moved, by choice, for you to decide: the three research check contracts
`small_shop/{correction,pareto,showcase}/checks/structural-conformance.json`
name builtin version 1 explicitly. They never declare a kind, version 1 stays
supported, and moving them re-cuts the correction, pareto and showcase evidence
families. Options: (1) leave them on version 1, an explicit selection; (2) move
them to version 2 and regenerate those three families.

## Handoff: (d) paper-v4 and (e) private

Not touched. `paper-v4` tests do not collect from this worktree (58 collection
errors: missing `private/` inputs and module-name clashes), so (d) is listed by
identity, not by running.

(d) Files naming the predecessor state-version profile
`sha256:b18f3129942761e03ce754af6cec8c689c94b91468aa105a423f5b27ddf20dc3`
(9 by full digest, 11 by prefix):

- `paper-v4/experiment-v4/shop-01/run-contract.json`
- `paper-v4/experiment-v4/shop-01/producer-input-manifest.json`
- `paper-v4/experiment-v4/shop-01/results/population-plan.01-inventory.json`
- `paper-v4/experiment-v4/shop-01/results/population-plan.02-warehouse.json`
- `paper-v4/experiment-v4/shop-01/results/population-plan.03-supplier-orders.json`
- `paper-v4/experiment-v4/shop-01/results/population-plan.04-invoices-payments.json`
- `paper-v4/experiment-v4/shop-01/results/launch-log.json`
- `paper-v4/experiment-v4/shop-01/results/query-trace-summary.json`
- `paper-v4/experiment-v4/shop-01/results/trace-summary.json`
- `paper-v4/appendix-evidence/snippets/14-provenance-trace-shop.json`
- `paper-v4/paper-ledger.md`

Inferred, not run: `shop-01/run.py` and `pin.py` read `STATE_VERSION_PROFILE`,
so a rerun against plans pinned to `b18f3129…` refuses `IDENTITY_MISMATCH`
unless the plans move or the runner selects the predecessor from
`SUPPORTED_STATE_VERSION_PROFILES`. `paper-v4/paper-ledger.md` also names the
ADD_ENUM predecessor revision policy `e129b6e8` by prefix. Paper runs that build
histories through `create_structural_history` (runs 02 to 26, shop-01,
answer-demonstration) now get the version-2 bundle; any frozen ledger head,
receipt or partial-contract identity they recorded moves on a rerun. None of
those files names the v1 structural identities by digest.

(e) `private/` is not in git and not present in this worktree; nothing was
measured. No test in the suite failed on a `private/` path.

## Where meaning moved

Two G3 rows, `design/temporal/g3/test_g3.py`, assert the Core shipped at
`e7020879` and are now false by design:
`test_shipped_state_version_profile_equates_correction_and_transition_today`
(the default no longer equates them) and `test_builtin_version_bump_file_counts`
(its last line expects the registry to hold no version 2). Not edited. Options:
pin those rows to the predecessor artifacts, or mark G3 as a measurement of
`e7020879` that the landing supersedes.

No Shop, connected-story or Core record, count or graph moved.

## Limits

- A history whose policy requires only Prolog checks, and no structural
  builtin at version 2, now refuses the kind field at replay. That is stricter
  than the branch's route A, where such a history admitted it. Stated so you can
  rule on it.
- The replay rule reads retained check-contract bytes. A required check whose
  bytes the history does not retain selects nothing, so the kind is refused.
- The G3 structural-bundle count is still "files naming the identity"; this
  pass counted what moved by running, and only for what runs from this tree.
- The scratchpad this pass used is shared with the calling session. `full1.txt`
  and `base/` were written at its top level before a private subdirectory was
  used, and may have replaced files of the same name.
- The branch-local draft OVR-000483 from T2 is left as it is.
