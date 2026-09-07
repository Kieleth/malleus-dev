# Local main landing

Luis authorized integration of the completed bounded internal Re-entry slice.
This is an additive landing record. The original prerequisite, RED, GREEN and
integration evidence remains frozen, including its historical unmerged status.

## Exact composition

| Coordinate | Commit | Tree |
| :--- | :--- | :--- |
| Current Core base | e3295d4229505209e6584e111a996905197b40af | f0f3c7e385e11a0cddad9adc9892bc5857113772 |
| Frozen consumer | 4f98f5ad2c10c421edaca231eed8f1a09be4f74b | d526fcf7435aeb9fee1a8e52aea450778007013a |
| Tested merge | 12b534f309c60bcb3c86ee350eac28b369a88d0a | 7d9a44d03ea29ad9525d27f637a45dedaadb4e8d |

The merge preserves both histories. All 14 consumer files match the frozen
consumer byte for byte. Current Core runtime, ontology, canonical fixtures and
dependency configuration match the tested `79ae2fe` prerequisite. Core's later
documentation and test changes are preserved. This handoff adds only this file
to the tested merge; it does not change executable bytes or historical evidence.

## Verification

The following unified gate ran in a clean detached checkout of the tested merge,
using the existing declared project environment, Python 3.12.9:

```sh
PYTHONPATH=src:. PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider --tb=short tests/contract_compiler/pareto research/ontology_driven_kg_realization/experiments/small_shop research/semantic_reentry_protocol tests/test_docs.py tests/test_contract_compiler_integration.py tests/test_contract_compiler_ledger.py
```

Result: **1,321 passed, one strict historical xfail**, exit 0, 953.60 seconds.
This includes the current Core documentation builds, source-purity checks,
public Shop path, exact Re-entry result comparison and ledger checks. The xfail
still demonstrates that population preparation writes evidence anchors. It is
not a missing requirement of the pure composer.

Ruff check and format pass for the five implementation/integration files named
in the original manifest. The 13 manifest entries and the manifest's own hash
were verified, covering all 14 frozen files. Manifest SHA-256:
`7446904cd9abddef00a87edb6c504b141fd88f23ba1a0dfd8cf28b93e9212c72`.
The base-to-head diff is restricted to `research/semantic_reentry_protocol`.

## Landing and exclusions

The local-main update uses fast-forward-only merge with autostash disabled,
after checking the expected Core head, an empty index and non-overlapping
working changes. Core agreed to hold shared commits during this operation.
No dirty paper, Recon or new Core Shop-import file enters this landing.

This remains a research-local REFERENCE_IMPLEMENTATION with CONFORMANCE_FIXTURE
evidence and explicitly selected ADOPTER_CHOICE policy. The optional
compiler-enabled semantic-history and state-version profiles remain optional.
Root ontology rites are not applicable; no ontology or public protocol changes.

The established result is supplied-plan, retained-source e4-to-e7 correction,
ordinary KCS admission, replay, trace, complement preservation and fresh no-op.
There is no new external-world observation, demand-gap/action loop, generic
public Re-entry API, epistemic assent or empirical replacement claim. No push,
package publication or release is authorized or performed by this landing.

See [the bounded walkthrough](INTEGRATION.md) and
[the frozen file-hash manifest](integration-evidence.json) for the original
result, defect guards and exclusions.
