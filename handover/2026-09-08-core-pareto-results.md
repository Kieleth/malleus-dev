# Core Pareto results: faster validation and partial shipments

The [approved sequence](2026-09-08-core-pareto-next.md) is implemented. The
[current backlog](2026-09-08-core-backlog.md) distinguishes shipped bounded
capabilities from the larger formal program. No formal workstream was promoted
to complete, and no consumer integration was absorbed.

## Faster validation without weaker checks

RED `b079a65` demonstrates 80 Git commands for 40 references. GREEN `39f9566`
replaces per-reference object/ancestry checks with one current HEAD/evidence-tag
ancestry read per validation. There is no cache across calls. Unknown commits,
unretained commits, moved HEAD, removed evidence tags, ordinary tags and changed
document anchors still refuse. Evidence bytes, schemas, hashes, chronology and
current document identities are still checked. Governance `81e7e42` binds the
changed source before the complete regression.

| Measurement | Before | After |
|---|---|---|
| One unprofiled ledger load | 15.110 seconds, 432 entries | 1.739 seconds, 433 entries |
| One unprofiled integration validation | 26.970 seconds | 14.673 seconds |
| Ledger module case time from JUnit | 374.867 seconds in the earlier clean baseline | 43.340 seconds |
| Integration module case time from JUnit | 424.025 seconds in that baseline | 150.631 seconds |

The two complete suites plus four new tests passed: **365 passed, zero skipped,
zero failures**, 194.91 seconds. The earlier module timings come from the
[recorded baseline](2026-09-08-core-default-suite.md), not a controlled benchmark
at identical commits. The narrow before/after call timings used the same
configured environment; they remain single observations. The mechanical
one-scan guard establishes the work reduction independently of elapsed time.
Remaining integration work is not optimized speculatively.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_governance_git_scan.py tests/test_contract_compiler_ledger.py tests/test_contract_compiler_integration.py --tb=short --junitxml=/tmp/malleus-pareto-next.hRjTJM/governance.xml
```

JUnit SHA-256: `3c1bb35742e5734e0cd517ac886e65d1eb364c96eb1e811dc447f5ccce38a495`.
The complete regression ran before the new shipment fixture changed any
governed status document. Final governance/document checks are separate.

## Partial-shipment Shop proof

Fixture RED: `5d564fa`, four failures because the runner was absent. Corrective
input/guard RED: `4aac817`. GREEN:
`907887046713a5135148be30a54636a28481ba97`, tree
`814111be08ed9cdf33712d538dcf1250b0301123`.

The [runnable example](../research/ontology_driven_kg_realization/experiments/small_shop/partial_shipments/README.md)
contains synthetic source rows, an explicit fixture mapping, an additive TBox,
an independently authored answer key and a runner. It extends the existing
default Shop, not a hand-built accepted graph. An order has two distinct units.
Its first tracked shipment contains one, leaving one unassigned. Its second
tracked shipment contains the other, leaving none. The old order/unit types are
reused; three new classes, one slot and two enum values supply the shipment
vocabulary. The pre-revision history cannot admit Shipment records.

All new domain records enter through the existing public population and
structural-admission path. No Core runtime or ontology root changed. The runner
uses the existing default Shop producer, not private runtime or test imports.
It does not manufacture check outcomes. Field derivations retain zero-based
source row locators, and trace retrieves the exact source and mapping bytes.
The projection and reader are unchanged; this fixed topology needs no new
recipe engine. Initial domain history and its supplier correction remain intact.

The five focused tests establish:

- The documented CLI and a second independent invocation produce identical
  history and report bytes. A copied ledger alone reopens with the same result.
- The initial order predates the shipment ontology; later changes bind its new
  contract identity. Two tracking identities and two physical units remain
  distinct, without supersession between them.
- Missing Shipment vocabulary and a dangling relation endpoint refuse before
  preparation writes. An intervening evidence append makes a prepared shipment
  stale and refuses without any additional write.
- The runner does not read its answer key or import private/test Core helpers.
- The fixture mapping does not impersonate a population-plan artifact.

The last guard records a real authoring error: the initial mapping used root
`grammar: malleus.population-plan/private-v0`, causing trace to find two claimed
plans. The corrected mapping names its target `plan_grammar` instead. This was
a mislabeled fixture, not a reason to weaken trace or change Core's protocol.

## Combined Shop evidence

**248 passed, zero skipped, zero failures**, 213.44 seconds. This is the complete
Shop research-directory selection plus its five public/Pareto integration test
files, including the new fixture. It does not mean every optional Shop profile
has been combined in one history. Object-event and executable-action examples
retain their own separate scope and prior receipts.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop tests/contract_compiler/pareto/test_small_shop_default_admission.py tests/contract_compiler/pareto/test_small_shop_contract_revision.py tests/contract_compiler/pareto/test_fresh_shop_import.py tests/contract_compiler/pareto/test_default_shop_walkthrough.py tests/contract_compiler/pareto/test_partial_shipments.py --tb=short --junitxml=/tmp/malleus-pareto-next.hRjTJM/shop.xml
```

JUnit SHA-256: `8c9988a55c7f0ef8b1d8de1f9081751cc45624ac8802d16d63680a39506dc595`.

A separate execution of the documented command writes the inspectable run at
`/tmp/malleus-pareto-next.hRjTJM/showcase/`:

- 71 ledger events; eight knowledge changes; two additive revisions.
- 20 current graph records and 21 historical records.
- Original 653,248-byte prefix unchanged, SHA-256
  `3f8478bba14f3612ec6c100c25666961a0869e79d0e0d157178f2d48be311e71`.
- Final 1,073,144-byte history SHA-256
  `4de60671c696b043e6bfdf02729db1ea26772cab43d199523792b238ed88b3ab`.
- Final ledger head
  `sha256:17367497fffca767f325b4af52eaa34c21d3de3d6995a5f9bb8dcb2fd7cbe68c`.
- Evidence JSON SHA-256
  `23474a0adc294a726273fe2cb7fd4f77a1c7c0e923159c754b4f8b1fe4cf3900`.

These temporary run artifacts are inspectable locally, not new canonical
protocol artifacts or a promise that temporary storage is archival. The source,
answer key and reproducible runner are committed. Historical Shop evidence was
not rewritten. Scoped Ruff, formatting and diff checks pass; all local links in
the plan, backlog and fixture guide resolve.

## Scope and self-review

Validation infrastructure and the backlog projection are
`REFERENCE_IMPLEMENTATION`. The Shop addition is `CONFORMANCE_FIXTURE` under
the optional compiler-enabled, state-version, structural-history profiles.
Shipment identity and associations are `ADOPTER_CHOICE`, not protocol vocabulary.
No new `PROTOCOL_INVARIANT` or `OPTIONAL_PROFILE` was introduced.

This proves recorded associations and reconstruction, not physical shipment,
source truth, epistemic acceptance, stock allocation or fulfilment policy. It
does not migrate an old shipment activity into a new entity, implement general
ontology migration, supply external effects or Semantic Re-entry, or establish
another interpreter's conformance. The demonstration is a sequence of atomic
commits, not one all-or-nothing transaction across the whole scenario.

The tests used the configured environment without installation or network
access. Unrelated paper and research worktree edits were preserved and excluded
from all commits. No full default-suite, package, external-linkcheck, release,
consumer-rebind or remote-push result is claimed by this slice.
