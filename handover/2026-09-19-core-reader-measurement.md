# Core: the stale reader measurement, and the class it belongs to

Date: 2026-09-19. Branch `worktree-agent-aed1befcdf8b82934`, from main `d89a0c47`.
Fix commit `b6f709173adc892641102bb4f0087f15b2599357`. ROADMAP F6.

## What was actually wrong

F6 was filed as one stale digest. It is three stale measurements, and the
seventeen failing tests split across them:

| Workstream | Retained measurement | Why it refused | Tests |
|---|---|---|---|
| CC-X04 | ten reader source digests pinned in `scripts/contract_compiler_historic_wire.py` | seven of ten changed since commit `5e4ec73e`; the set last moved at `851913c0`, 2026-09-08 | 6 |
| CC-X01 | `conformance/contract_compiler/v0/linkml_legacy_divergence/observations.json` | the retained `OntologyRegistry` digest was one revision old | 7 |
| CC-X02 | `conformance/contract_compiler/v0/bundled_declaration_scan.json` | the scanner required "exactly six packaged ontology YAML modules"; `pyproject.toml` packages ten | 4 |

Only six of the seventeen carried the message F6 quotes. The other eleven are
the same class with different text.

## How a measurement was meant to be recorded

There was no procedure for CC-X04. `render` could not run, because it calls
`_reader()` first and `_reader()` was the thing refusing. The previous
re-measurement,
`design/contract_compiler/overseer/evidence/CC-X04-reader-remeasurement.json`
(2026-09-03), was done by hand: a person compared ten files, typed ten digests
into the script, and wrote the comparison up in prose. Its own last limitation
says "Any later change to one of the ten bound reader inputs requires another
fresh forward-only measurement". Nothing enforced that, and the set changed
five days later.

CC-X01 and CC-X02 did have tools, `--render` and `--write`, which derive the
whole measurement from the files. Both were simply never re-run.

## Why it stayed invisible

`pyproject.toml` `[tool.pytest.ini_options] testpaths` did not list
`tests/test_contract_compiler_divergence.py`,
`tests/test_contract_compiler_duplicate_scan.py`,
`tests/test_contract_compiler_historic_wire.py` or
`tests/test_contract_compiler_baseline_inventory.py`. The default pytest run is
what `scripts/ci.py test` runs and what `.github/workflows/tests.yml` runs on
every push, and it collected none of them. The tests existed and no gate ever
asked them anything. They fail only when someone types an explicit path, which
is what the Overlord did.

## The guard, and what was rejected

**Chosen: the four files join `testpaths`, and a test refuses any
`tests/test_contract_compiler_*.py` outside it**
(`tests/contract_compiler/test_ci.py::test_every_compiler_measurement_test_is_inside_the_default_gate`).
This is the repository's own recorded preference, not a new idea: commit
`35be5c6c` ("Keep compiler tests out of shared pytest identity") decided that
compiler checks belong to ordinary pytest collection rather than a second CI
stage, and the neighbouring test is named
`test_default_pytest_collects_the_compiler_tests_without_a_duplicate_ci_stage`.

**Rejected: make the reader source modules governed documents of the overseer
ledger.** Measured, not assumed. Four of the ten reader sources are already
governed documents: `src/malleus/kg.py` and `src/malleus/ledger.py`
(OVR-000440), `src/malleus/accepted.py` and `src/malleus/staging.py`
(OVR-000387). All four had stale digests in `READER` anyway. Governance pins the
file to the ledger; it does not pin the measurement to the file. The mechanism
cannot do this job.

**Rejected: add the three `--check` commands to the `scripts/ci.py` `TEST`
profile.** `tests/contract_compiler/test_ci.py::test_default_ci_plan_covers_every_boundary_once`
asserts the plan is exactly nine named commands and that none is called
`compiler-tests`. Adding stages contradicts the decision in `35be5c6c`.

**Rejected: derive `READER` at import and pin it only by the retained
observations.** It removes the refusal three tests exercise, and it does not
help on its own: a stale retained artifact is still invisible while no gate
collects the test. The gate is the load-bearing half.

## What changed in the tools

`scripts/contract_compiler_historic_wire.py record` derives all ten digests
from the tracked files, rewrites the `READER` literal in place, re-renders
`observations.json`, and names the commit that last touched the reader set
rather than HEAD, so an unrelated commit does not move the coordinate. It
refuses while any reader source differs from HEAD: a measurement of uncommitted
bytes identifies nothing. The refusal a stale measurement raises now ends with
the command that fixes it.

`scripts/contract_compiler_ledger.py refresh-evidence <report>` re-derives every
bound artifact length and digest in a verification report or evidence
correction from the current bytes. It is the counterpart of `verify-evidence`,
which until now could only tell you a report was stale.

`scripts/contract_compiler_duplicate_scan.py` no longer hard-codes the packaged
module count. Membership is pinned by the retained scan, which `check_scan`
compares byte for byte; the literal `6` was a second, hand-typed pin of the same
fact, and it is the one that went stale.

## What the re-measurement found

`ReconProject.ledger` became private at commit `9a7fafc9`. The CC-X04
observation read it, so the render raised `AttributeError` even after the
digests were fresh. It now reads `ReconProject.snapshot_verified()`, the public
surface returning the same `MigrationVerification`. No private attribute is
read.

**No observed outcome changed.** CC-X04 still records two Recon acceptances,
one graph refusal and two artifacts not reached. CC-X01's fresh render differs
from the retained bytes in exactly two fields: the `OntologyRegistry`
implementation digest, and `execution_context.pyyaml.version` (6.0.2 to 6.0.3),
which `semantic_observations` excludes from the comparison.

**CC-X02 grew, and that is a finding.** The scan now covers the four packaged
modules it never saw: `packs/metrology.yaml`, `packs/chronology.yaml`,
`packs/research.yaml`, `profiles/object-event.yaml`. 525 declarations in 6
modules became 586 in 10, and four further duplicate groups appear:

- slot `claim_kind`: `domains/recon.yaml`, `packs/research.yaml`
- slot `unit`: `domains/ocr.yaml`, `packs/metrology.yaml`
- class `Claim`: `domains/recon.yaml`, `packs/research.yaml`
- class `Evidence`: `ontology/assent.yaml`, `packs/research.yaml`

Every occurrence has `adopts` ABSENT. That is an input to CC-D02, the explicit
adoption policy decision, not a decision taken here. Somebody should rule on
whether the research pack re-declaring `Claim` and `Evidence` beside recon and
assent is intended.

## Measurements

| Run | Result |
|---|---|
| clean main `d89a0c47`, `pytest -q tests` | 17 failed, 3605 passed, 3 skipped |
| this branch, `pytest -q tests` | 24 failed, 3602 passed, 3 skipped |

All 24 remaining failures trace to one refusal, `OVR-000468: latest document
digest mismatch for pyproject.toml`, raised by `load_ledger`: 14 in
`test_contract_compiler_integration.py`, 7 in
`test_contract_compiler_ledger.py`, 3 in `test_docs.py`, whose Sphinx build runs
the ledger projection. They clear when OVR-000469 is sealed. Ruff passes on
every file touched.

New tests, RED before GREEN:

- `test_pinned_reader_measurement_is_a_projection_of_the_tracked_bytes`: run
  against the unmodified `d89a0c47` checkout it fails on
  `src/malleus/recon/store.py`; it passes here.
- `test_every_compiler_measurement_test_is_inside_the_default_gate`: against
  `d89a0c47` it fails naming all four files outside `testpaths`; it passes here.
- `test_record_rewrites_the_pinned_measurement_from_the_tracked_bytes` and
  `test_record_refuses_to_measure_an_uncommitted_reader_source` have no RED at
  `d89a0c47`, because `record_reader` did not exist there.

## Residuals

- The three re-admitted test files have never run on Linux, or on Python 3.10,
  3.11 or 3.13. They were measured here on Darwin arm64, CPython 3.12.9. The
  CC-X01 check spawns a subprocess importing LinkML 1.11.1 from the retained
  pure-Python wheels, which are tracked, so it should be portable; that is an
  expectation, not an observation. The first CI run after this lands is the test
  of it.
- `scripts/ci.py` `QUALITY` lints `scripts/contract_compiler_ledger.py` and
  `scripts/contract_compiler_integration.py` but not the historic-wire or
  duplicate-scan scripts, nor the three test files now in the gate. Ruff was run
  on them by hand and passes. Widening the lint list is a separate change.
- `conformance/contract_compiler/v0/linkml_legacy_divergence/observations.json`
  and `scripts/contract_compiler_duplicate_scan.py` had never appeared in any
  `DOCUMENT_REVISION`. The CC-X01 retained measurement was ungoverned. They are
  entered in OVR-000469 as `MODIFIED` with `before_digest` taken from the
  committed bytes at `d89a0c47`; the ledger accepts `CREATED` for a path with no
  history, so change that if first appearance is the convention you want.
- `design/contract_compiler/overseer/evidence/CC-X04-reader-remeasurement.json`
  is untouched, per its own forward-only rule. The new measurement is in
  `-r2.json`, and the test now binds that.

## OVR-000469 draft

Not in `entries/`: an unsealed file there breaks `load_ledger`. Exactly two
placeholders, `<sealing moment, UTC>` and `<digest of this file once final>`.
`entry_hash` is a probe value computed over the block with those two
substituted, and must be recomputed at sealing.

Validated: substituting `2026-09-20T03:00:00Z` and a zero digest, the block has
zero errors against `design/contract_compiler/overseer/ledger.schema.json`
(Draft 2020-12, format checker on), and `entry_hash` is self-consistent under
`scripts/contract_compiler_ledger.entry_hash`. Probe hash
`sha256:586c34179206b57307506543e9cc2768c895a196cb54418379d7c0feefeb0363`.
Every `before_digest` was checked equal to the committed bytes at `d89a0c47`.

```json
{
    "actor": {
        "id": "overseer",
        "type": "OVERSEER"
    },
    "data": {
        "affected_ids": [
            "CC-X01",
            "CC-X02",
            "CC-X04"
        ],
        "documents": [
            {
                "after_digest": "sha256:e12d9a009e2528a7902b8b3d59d4cd53d60b400c7fd582ac50e7c15809ee2def",
                "before_digest": "sha256:f9d435fd79a5d577504b57f482fde41c2776ddf1e8c6dfb5f7b404b1d29fef48",
                "change": "MODIFIED",
                "path": "CHANGELOG.md"
            },
            {
                "after_digest": "sha256:65bc88dd008a2567fd04307214c566713d38bee05b96ba394534673736c564e3",
                "before_digest": "sha256:3070ad3c910451e022591545c664f12e838c585349cb3e06a54b2867cf893049",
                "change": "MODIFIED",
                "path": "conformance/contract_compiler/v0/bundled_declaration_scan.json"
            },
            {
                "after_digest": "sha256:83a5444a3dafda17bcbe5accca468e1562e20419997976bf6085eab3307d2448",
                "before_digest": "sha256:25b90ac90da285b6c03aed904452a3e2b6ad5ec6a292d45acd488a9ffc281e88",
                "change": "MODIFIED",
                "path": "conformance/contract_compiler/v0/evidence/CC-X01-environment-contract-correction.json"
            },
            {
                "after_digest": "sha256:656352f8e9dd08255237c5dbcf57d437cac91a6b4d4b6b3e3b342ca36b9b67e6",
                "before_digest": "sha256:ee9b2f11438a15ad3d4243addd250b03afb0769f71fb2ff13b43d7c1d3b03ada",
                "change": "MODIFIED",
                "path": "conformance/contract_compiler/v0/historic_wire/observations.json"
            },
            {
                "after_digest": "sha256:9e0a535805e4fcd73986ec72f351875dc65bc0b6bd95ca00e502c42df8064092",
                "before_digest": "sha256:cf8ae922d0a1b2efb83d7f99df374254882f9626608d3b96ae425f02737f8af9",
                "change": "MODIFIED",
                "path": "conformance/contract_compiler/v0/linkml_legacy_divergence/observations.json"
            },
            {
                "after_digest": "sha256:b1262ade29cb982e89bda5f662982c180890283b122184cb52b27b19345bb6db",
                "change": "CREATED",
                "path": "design/contract_compiler/overseer/evidence/CC-X04-reader-remeasurement-r2.json"
            },
            {
                "after_digest": "sha256:f85e979632fb68cc0a4f855f3135e08a46fe117ceac8d93da3f1b90a5df69de3",
                "before_digest": "sha256:88a2f72949e6e3e7d0344c5edb888769ebc3f560260e5d54fa0e9273ba1ce2b6",
                "change": "MODIFIED",
                "path": "design/contract_compiler/program.md"
            },
            {
                "after_digest": "sha256:2231d4d3d8cdb5e067e334840d32e5d28ca791e4e1f23acc8fde359ccb48036c",
                "before_digest": "sha256:9418e7dd42122c9c5e9164243b010b80e58e244dfb1d65c1efd35ead118aaf98",
                "change": "MODIFIED",
                "path": "docs/IMPLEMENTATION_STATUS.md"
            },
            {
                "after_digest": "<digest of this file once final>",
                "change": "CREATED",
                "path": "handover/2026-09-19-core-reader-measurement.md"
            },
            {
                "after_digest": "sha256:3f59e5956b9ba5efa7bbfdf5e1a78c507f717e6e2b5393245c4e686c1d1bcad9",
                "before_digest": "sha256:a590d79b3ca5a055127fc337995192a34309aa2f4511cd8338e1284aeb7b1117",
                "change": "MODIFIED",
                "path": "pyproject.toml"
            },
            {
                "after_digest": "sha256:54bcae833f6727ff5da6a6c7d81af76df6ed73df29ca60e5798b57df27f9501f",
                "before_digest": "sha256:546a5cd14326014c7eafae96002f050f990662c422c32a5494a5ce66648099be",
                "change": "MODIFIED",
                "path": "scripts/contract_compiler_duplicate_scan.py"
            },
            {
                "after_digest": "sha256:0729f997f70d2b9531b8f0e0af34656975ed4947052aab8890ad168e2d5fbe37",
                "before_digest": "sha256:fedce3245745292a7d733609130be7b73e1da8b5fb493f55f44f644f69eb33b6",
                "change": "MODIFIED",
                "path": "scripts/contract_compiler_historic_wire.py"
            },
            {
                "after_digest": "sha256:ca22ef6dcdf8a8a79f1f93690a3a71a6b0d462a45f4c6e22f9bbdc455be73e58",
                "before_digest": "sha256:83ae4082106bbfe5a43ab25380bdcd5bde3d1878d89d44e33526a34991e4540b",
                "change": "MODIFIED",
                "path": "scripts/contract_compiler_ledger.py"
            },
            {
                "after_digest": "sha256:3c208bfa01dc391f2993cb0e48421881a824a1862fedbb1596031d0b4b5e0a64",
                "before_digest": "sha256:bfe2265d667231b46aab94907bff4d00d80efb2844fb72387f38ab99ef0ee4dc",
                "change": "MODIFIED",
                "path": "tests/contract_compiler/test_ci.py"
            },
            {
                "after_digest": "sha256:c3e056e8ad540ee29f526916e587e9f2fc43d67beac348fac5a517512ef670ca",
                "before_digest": "sha256:d24ec20734a992b5d84cdddad26529bdbb3745022c9c091adb7ef29d327148af",
                "change": "MODIFIED",
                "path": "tests/test_contract_compiler_divergence.py"
            },
            {
                "after_digest": "sha256:dc9d41731a96660458935a69b5dacc298ec1fab495ab4f46143871a2a15a9bdd",
                "before_digest": "sha256:eb5bf674aab4550f661f7dbe5fe4d53a2a713ad540d788d95d72401a0102e01b",
                "change": "MODIFIED",
                "path": "tests/test_contract_compiler_duplicate_scan.py"
            },
            {
                "after_digest": "sha256:c7559040569fb97e489c69e84f0f3d01e12d5f99421cd4cad8cfd51ef4b31055",
                "before_digest": "sha256:e95f589a22e1652b9a8643a3246efab3359a847db9286a703eabcf6861eb1843",
                "change": "MODIFIED",
                "path": "tests/test_contract_compiler_historic_wire.py"
            }
        ]
    },
    "entry_id": "OVR-000469",
    "entry_type": "DOCUMENT_REVISION",
    "ledger": "overseer",
    "previous_entry_hash": "sha256:ac90aecc40c69a1d00aff8786d5da9f3a95c430adfe4c058c29a48491139c0e3",
    "recorded_at": "<sealing moment, UTC>",
    "references": [
        {
            "relation": "EVIDENCES",
            "target": "b6f709173adc892641102bb4f0087f15b2599357",
            "type": "COMMIT"
        },
        {
            "relation": "AFFECTS",
            "target": "CC-X01",
            "type": "WORKSTREAM"
        },
        {
            "relation": "AFFECTS",
            "target": "CC-X02",
            "type": "WORKSTREAM"
        },
        {
            "relation": "AFFECTS",
            "target": "CC-X04",
            "type": "WORKSTREAM"
        }
    ],
    "schema": "malleus.contract-compiler.ledger-entry/v1",
    "sequence": 469,
    "subject": {
        "id": "core-reader-measurement",
        "type": "DOCUMENT"
    },
    "summary": "Re-record the CC-X01, CC-X02 and CC-X04 measurements of repository bytes, derive them from the bytes, and put every compiler measurement test inside the default gate.",
    "why": "ROADMAP F6. 17 tests failed on clean main d89a0c47 from three stale measurements, not one. CC-X04 pinned ten reader digests recorded at 5e4ec73e; seven had changed by 851913c0 (2026-09-08). CC-X01 retained an OntologyRegistry digest one revision old. CC-X02 required exactly six packaged ontology modules while pyproject packaged ten. Why nothing noticed: pyproject testpaths omitted all three test files and the baseline-inventory one, so the default pytest run, which scripts/ci.py test and CI run, collected none of them. Governance was measured and rejected as the guard: kg.py, accepted.py, ledger.py and staging.py are already governed here and their pinned digests were stale anyway, because governance pins the file, not the measurement. The four files join testpaths and test_ci.py refuses any tests/test_contract_compiler_*.py outside it. Measurements became projections: historic_wire 'record' and ledger 'refresh-evidence'. CC-X04 also read ReconProject.ledger, private since 9a7fafc9, and now reads snapshot_verified. No observed outcome changed in CC-X01 or CC-X04. CC-X02 grew to 586 declarations in 10 modules with four further duplicate groups, a CC-D02 input, not a decision here.",
    "entry_hash": "sha256:586c34179206b57307506543e9cc2768c895a196cb54418379d7c0feefeb0363"
}
```

## Sealing note for OVR-000469, 2026-09-20

`entries/OVR-000469.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment,
the previous entry hash where placeholdered, and this file's digest filled in.
