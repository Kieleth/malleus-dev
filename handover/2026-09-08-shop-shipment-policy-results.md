# Shop policy proof: results

The [selected slice](2026-09-08-shop-shipment-policy-plan.md) is implemented.
The [runnable example](../research/ontology_driven_kg_realization/experiments/small_shop/shipment_policy/README.md)
now distinguishes a well-shaped shipment record from an assignment that passes
the selected Shop rule. The business rule remains a Prolog artifact and its
verdict policy remains JSON. Core executes them without knowing Shop names.

## Result in plain English

The order contains two physical units. The first shipment takes X1. A candidate
second shipment that also takes X1 is rejected, with X1 and both shipment-unit
associations as witnesses. No admission bytes or accepted graph changes escape.
The legitimate second shipment takes X2 and is accepted. Reopening the ledger
alone reproduces the same records and retained check evidence without invoking
Prolog again.

Preparation retains the submitted source/plan before admission. The acceptance
transaction then contains the KCS, receipt, proposal, check and derived verdict.
Rejection preserves that exact pre-admission prefix; it does not remove prior
evidence retention or persist a separate rejected-check audit event.

## TDD and exact scope

| Boundary | RED | GREEN |
|---|---|---|
| Compiled graph into the existing rule checker | `72da502`, then `dc505e96`: four failures for the absent identity method | `8d315fbd`: seven added lines in `ContractView.verifies` |
| Selected Shop policy through real history admission | `8436ec9c`: four failures for the missing consumer | `9a0e8b66`: fixture rule, exact check contract, policy, runner and integration tests |
| Exact current evidence after the compiler change | Full Shop: 238 passed, 15 producer-binding failures | `cb2427a1`: separately recorded evidence generation, 14 exact evidence guards passing |

There is no other Core runtime change in this slice. The compiled view verifies
its exact digest in bare or `sha256:` form, not raw-source aliases or unrelated
ontology identities. Its counterpart's legacy identity rules remain separate.
The old partial-shipment mapper gains only an explicit retained-source selector
so the negative source passes through the same mapping code.

During authoring, two test expectations were corrected from actual contracts:
the policy refusal is `REJECTED_CHANGE`, and witness IDs are canonically sorted.
The command/repeatability test compares canonical JSON at the serialization
boundary, not Python tuples against decoded JSON lists. None required changing
the protocol, weakening a refusal, or skipping a test.

## Why the old evidence needed a successor

The compiler binds implementation bytes into its producer identity. Adding the
identity method therefore changes compiler-dependent history fingerprints even
though the existing domain facts are unchanged. The old producer-bound tests
correctly refused comparison with the previous generation.

Five actual fresh runs produced
`research/ontology_driven_kg_realization/experiments/small_shop/evidence_2026_09_08_rule_check/`.
The binding records all current outputs, complete retained compiler artifacts,
the producer and the exact differing fingerprint paths. Recursive comparison
proved no changes to structure, scalar types, domain values, records, sources,
counts, operation fields or time semantics. Both graph files remain
byte-identical. All twenty predecessor output files remain unchanged. Tests do
not regenerate their expected answers or exclude identity fields.

## Validation

The source/evidence boundary is committed through
`fd293918839f195e2e42fd521475116bfeff8a79`, tree
`ddeab9984da9fb1a565ab4d119d7bec6bcdaa0fa`. Later result-only documentation does
not change those source bytes. The commands below use the configured repository
environment and its existing SWI-Prolog dependency, with no installation.
Selections overlap; their counts must not be added as distinct tests.

- Focused rule/Shop plus existing logic: **72 passed, zero skipped**.
- Compiled rule, existing logic and complete KG tests: **174 passed, zero skipped**.
- Complete Shop research directory plus its five Pareto integration files:
  **253 passed, zero skipped**.
- Exact evidence-generation guards: **14 passed, zero skipped**.
- Final complete governance, documentation and status selection at the bound
  source coordinate: **507 passed, zero skipped**.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop/shipment_policy tests/contract_compiler/pareto/test_compiled_shipment_rules.py tests/test_prolog_verifier.py tests/test_logic.py --tb=short
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_compiled_shipment_rules.py tests/test_prolog_verifier.py tests/test_logic.py tests/test_kg.py --tb=short
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider research/ontology_driven_kg_realization/experiments/small_shop tests/contract_compiler/pareto/test_small_shop_default_admission.py tests/contract_compiler/pareto/test_small_shop_contract_revision.py tests/contract_compiler/pareto/test_fresh_shop_import.py tests/contract_compiler/pareto/test_default_shop_walkthrough.py tests/contract_compiler/pareto/test_partial_shipments.py --tb=short
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_governance_git_scan.py tests/test_contract_compiler_ledger.py tests/test_contract_compiler_integration.py tests/test_docs.py tests/test_status.py --tb=short
```

Local JUnit receipts are in `/tmp/malleus-shipment-policy.s6KwOo/`:

| Receipt | SHA-256 |
|---|---|
| `focused.xml` | `fa86bd7f8ac3705d369b6e5c1cfd2ede31000a01d4bbd5f924ba615995778d55` |
| `logic-kg.xml` | `1d69379928e8838e5b8a9199ae62b425af59b3e0aae16dbaee99611eb3320d6c` |
| `shop.xml`, the initial failed comparison | `3e6c48da2620fbb6b005d4dded0c0ba03996a54e9eb6522f7b8321964ed2b2b8` |
| `shop-final.xml` | `ac7eabfc59b760ba02084c5322bb453339aff72c3c36626d6c62418b95d93bb1` |
| `governance-docs.xml` | `b1f04cf8a480362af1dffca3eb51eb30b53b49a58c259a9d099b0a16223764ab` |

Scoped Ruff and diff checks pass. Formatting checks pass on the fixture and
test files. Existing whole-file formatting in `view.py` was not swept into
this seven-line repair.

## Inspectable run

The documented command was executed separately into
`/tmp/malleus-shipment-policy.s6KwOo/history.jsonl`. It has 32 ledger events and
three accepted KCS values. Its two shipments contain X1 and X2 respectively.

- Ledger SHA-256: `633aa2ee2a8072b250831cb0667f24c99f16df2f404d05e155a80c9fcb0f3e14`.
- Replay receipt: `sha256:fd88dcb94b6fd3668215f69f29444798aa46b99aa793ebbf69a080559864df76`.
- Final executed-check receipt: `sha256:11f5996b507a612fa9077cc5ff5f48f0254074a71a1db148539af3be567fb1f3`.
- Rule contract: `sha256:6b389b70621923937927db66f6eb58b82eb41967fb0259f76483430cdcc6ec3a`.
- Rule bytes: `sha256:7b86988f34bec53fdfbe9c086e55014a133e0508e96b16aa4679d4223046470b`.

The repeatability test runs the CLI and a second independent invocation into
fresh paths, compares report/history bytes, and refuses reuse of an occupied
history path. The positive trace resolves the actual shipment source, rule and
contract bytes by ID. A stale preparation refuses before engine invocation;
an engine failure never becomes a successful check. Checking uses the exact
KCS operations, not an altered convenience copy in preparation metadata.

## Governance and non-claims

OVR-000437 binds the Core repair and selected policy proof. OVR-000438 binds the
inspected evidence successor and the separate design response. The validated
chain has 438 entries at
`sha256:d7d86faf3c56da4668247e1f71540c50e2ef3fae935a9f22bd5cfa0380e4fdf4`.
The Malleus development skill kept the domain rule outside Core and its stronger
guarantee optional. Self-inquisition found no fixture promoted to protocol law.

This remains a trusted, research-local, insert-only policy episode. Replayed
receipts are execution attestations, not independent verification that Prolog
ran, and low-level caller-authored events are not an anti-forgery boundary.
No shipment reassignment, cancellation, subclass generalization, stock or
physical delivery claim, policy migration, new public interpreter, stable wire,
full-repository gate, package build, release or remote push is claimed.
Paper, Robotics and Re-entry consumers and their exact pins remain untouched.
Unrelated Paper/Recon working-tree changes are preserved and excluded.

Re-entry's incoming incremental-projection request is answered in a separate
[Core design response](2026-09-08-incremental-projection-core-response.md).
No incremental implementation is active or authorized by this result.
