# The include list governs the sdist, and three modules were missing from it

Core agent, 2026-09-22 UTC. Branch `worktree-agent-ada872a65bf36b8ec`, from main
`c4ef80d9` (OVR-000478). Fix commit
`efc60e3c875691bb3c7bdcb06fd1752b9fd96454`.

## The finding as filed, and what is true

Filed: the wheel's include list omits `gap_answer.py`, `linkml_addition.py` and
`ontology_source.py`, so an installed wheel cannot import `malleus.compiler`.
The edit was added at `a21962b3` and withdrawn at `3147ccd3` because CC-X02
pins `pyproject.toml`'s exact bytes.

The half about the wheel is wrong. A wheel built from main `c4ef80d9`, with the
list untouched, carries all 57 tracked `.py` files under `src/malleus`,
including the three, and imports `malleus.compiler` from an unpacked copy with
the tree off `sys.path`.

The mechanism is hatchling's own, read in the `include_spec` property of
`hatchling/builders/config.py`: every entry of a target's `packages` is appended
to that target's include patterns. `[tool.hatch.build.targets.wheel]` sets
`packages = ["src/malleus"]`, so `/src/malleus/` joins the wheel's include set
and the wheel ships the whole package directory whatever the list says. That was
confirmed by experiment, not only by reading: a scratch module written into
`src/malleus` and named nowhere was packaged into the wheel and absent from the
sdist. The comment above the list, which claimed only listed files are packaged,
was false for the wheel and is corrected in this change.

`[tool.hatch.build.targets.sdist]` declares no `packages`, so the list is the
sdist's entire include set. The sdist is the artifact the three missing lines
broke.

## Measured on main c4ef80d9

| Observation | Result |
|---|---|
| tracked `.py` under `src/malleus` | 57 |
| `.py` members of the repository wheel | 57, the three present |
| `.py` members of the sdist under `src/malleus` | 54, the three absent |
| wheel rebuilt from that sdist, against the repository wheel | differs by exactly those three members, nothing else |
| `import malleus.compiler` from the sdist-built wheel | `ModuleNotFoundError: No module named 'malleus._contract_pipeline.gap_answer'`, through `compiler`, `admission`, `check_contract`, `knowledge` |
| `scripts/ci.py package --require-clean` | `[ci] repository and source-archive wheels differ`, `[ci] package-parity failed with status 1` |
| unlisted scratch module under `src/malleus` | in the wheel, not in the sdist |

The cost is not a broken wheel. It is a broken source distribution, an install
from source that cannot import the compiler, and a release that stops:
`scripts/ci.py package` is RED on main today, and `release.yml` runs that
profile in its `build` job on a `v*` tag. `tests.yml` runs `test` and `docs`
only, which is why nothing on a push or a pull request ever looked.

## The guard

`tests/contract_compiler/test_packaging.py`, four tests, inside the default
pytest selection because `testpaths` already names `tests/contract_compiler`.

- `test_every_tracked_source_module_is_named_by_the_include_list` asks
  hatchling's own `SdistBuilder` which files it would take and compares that set
  with `git ls-files src/malleus`. No second matcher lives in the test.
- `test_every_include_pattern_selects_a_file` refuses a listed path that does not
  exist and a glob that selects nothing.
- `test_the_source_distribution_ships_every_tracked_source_module` builds the
  sdist offline with `--no-isolation`, against the pinned `hatchling==1.31.0`
  and `build==1.2.2.post1` of the `dev` extra, and reads its members.
- `test_a_wheel_rebuilt_from_the_source_distribution_imports_the_compiler`
  rebuilds the wheel from that sdist, unpacks it outside the tree and imports
  `malleus.compiler` in a subprocess whose `PYTHONPATH` is the unpacked copy. It
  asserts the import resolved inside that copy, so the observation is about the
  distribution and not about whatever is installed.

RED against the frozen `pyproject.toml` bytes: 3 failed, 1 passed.

```
FAILED test_every_tracked_source_module_is_named_by_the_include_list
FAILED test_the_source_distribution_ships_every_tracked_source_module
FAILED test_a_wheel_rebuilt_from_the_source_distribution_imports_the_compiler

pyproject.toml [tool.hatch.build] include does not name these tracked modules,
so the source distribution drops them:
['src/malleus/_contract_pipeline/gap_answer.py',
 'src/malleus/_contract_pipeline/linkml_addition.py',
 'src/malleus/_contract_pipeline/ontology_source.py']

the source archive malleus_dev-0.14.0.tar.gz drops: [the same three]

a wheel rebuilt from the source archive cannot import malleus.compiler:
ModuleNotFoundError: No module named 'malleus._contract_pipeline.gap_answer'
```

GREEN after the fix: 4 passed, about 2 seconds. The sdist and the rebuilt wheel
are module-scoped fixtures, built once each.

## The fix, and the re-recorded measurement

The three paths join the include list in its existing alphabetical order, where
`a21962b3` had put them. The comment above the list is corrected.

`pyproject.toml`: 12074 bytes, `sha256:037567e3...`, became 12643 bytes,
`sha256:7c6d162b...`. Both measurements that bind those bytes were re-derived by
their own tool, never typed, the way ROADMAP F6 did at `b6f70917`:

- `scripts/contract_compiler_duplicate_scan.py --write` rewrote
  `conformance/contract_compiler/v0/bundled_declaration_scan.json`. Only the
  `pyproject` block moved. The scan still reads 586 declarations in 10 modules,
  8 duplicate groups, 17 duplicate occurrences and 0 cross-kind repeats, so no
  CC-X02 observation changed. `--check` passes.
- `scripts/contract_compiler_ledger.py refresh-evidence` rewrote the eight bound
  artifact digests of
  `conformance/contract_compiler/v0/evidence/CC-X01-environment-contract-correction.json`.
  Only the `pyproject.toml` artifact moved; the other seven files are untouched
  by this change.

No test hard-coded 12074 or the old digest. The four tests named in `3147ccd3`,
three in `tests/test_contract_compiler_duplicate_scan.py` and
`test_environment_correction_replaces_only_the_availability_guarantee` in
`tests/test_contract_compiler_divergence.py`, derive both numbers from the live
bytes, so none of them needed an edit. What was stale was the two retained
artifacts.

## Residuals

`recorded_at` in the CC-X01 correction still reads `2026-09-01T19:48:03Z` and
`historical_evidence_commit` still names `f9a09e24`. `refresh-evidence` touches
neither, and F6's re-record at `b6f70917` left both alone, so the file carries
digests derived on 2026-09-22 under a September 1 timestamp. Moving that date is
a hand edit of a governed measurement and no tool owns it. Somebody should rule
on whether the correction gains a re-measurement coordinate its tool writes, the
way the CC-X04 reader measurement names the commit that last changed its source
set.

`scripts/contract_compiler_ledger.py verify-evidence` cannot check an evidence
correction, and could not before this change. It validates the report against
`ledger.schema.json`, the ledger *entry* schema, and then requires
`schema == "malleus.contract-compiler.verification-report/v1"`; an
`evidence-correction/v1` document fails both gates. Its counterpart
`refresh-evidence` accepts both schemas through `REFRESHABLE_REPORT_SCHEMAS`, so
the correction can be re-recorded by tool and never verified by tool. Reproduced
against the unmodified `c4ef80d9` bytes.

## Overseer entry

```json
{
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "data": {
    "affected_ids": [
      "CC-R11",
      "CC-X02"
    ],
    "documents": [
      {
        "after_digest": "sha256:b4caa1c5f57e6a8de5e4727ff563992789552041e89fc7db67888acc035d2766",
        "before_digest": "sha256:e457392794b3f7fb1a24c63ce177fc05c76d08cc3b6ed98e0b3dc7e5fbadef9a",
        "change": "MODIFIED",
        "path": "CHANGELOG.md"
      },
      {
        "after_digest": "sha256:2026a8f2d546ad4d246df438c64322cbc577450464e0302f626b988434026b36",
        "before_digest": "sha256:e30270a44e1305a355c27cf063ee99b4cd5112f4bb9bcfa74392315252f7e475",
        "change": "MODIFIED",
        "path": "conformance/contract_compiler/v0/bundled_declaration_scan.json"
      },
      {
        "after_digest": "sha256:359cad031d22059acd624a0893ddc27e317b03a4feba35d701ba01b3b79b4d96",
        "before_digest": "sha256:c481094613e46a6d28882a332cc9bd5dc6a1816639c5fba98aa34125c26fbd9c",
        "change": "MODIFIED",
        "path": "conformance/contract_compiler/v0/evidence/CC-X01-environment-contract-correction.json"
      },
      {
        "after_digest": "<digest of this file once final>",
        "change": "CREATED",
        "path": "handover/2026-09-22-wheel-include-list.md"
      },
      {
        "after_digest": "sha256:7c6d162bde1fcaf493972eceac3c1a2e92a234471c0fc3e6614ba1092849352d",
        "before_digest": "sha256:037567e39af4eca01f8ff0560625075d053729f8311d5dce3bc9270b0f47a47d",
        "change": "MODIFIED",
        "path": "pyproject.toml"
      },
      {
        "after_digest": "sha256:5de85a588c403c2cc1abd01897f24fbf3b493fa78a60db49f9ef69d32103860c",
        "change": "CREATED",
        "path": "tests/contract_compiler/test_packaging.py"
      }
    ]
  },
  "entry_id": "OVR-000479",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {
      "relation": "EVIDENCES",
      "target": "efc60e3c875691bb3c7bdcb06fd1752b9fd96454",
      "type": "COMMIT"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-R11",
      "type": "WORKSTREAM"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-X02",
      "type": "WORKSTREAM"
    }
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 479,
  "subject": {
    "id": "packaging-include-list-2026-09-22",
    "type": "DOCUMENT"
  },
  "summary": "Add gap_answer.py, linkml_addition.py and ontology_source.py to the packaging include list, which governs the source distribution, and re-record by tool the two measurements that bind pyproject.toml's bytes.",
  "why": "The finding said an installed wheel cannot import malleus.compiler. Measured on c4ef80d9 the wheel is complete: hatchling appends a target's packages to its include patterns (builders/config.py include_spec) and targets.wheel sets packages = [\"src/malleus\"], so the wheel ships all 57 tracked modules whatever the list says; an unlisted scratch module was measured into it. targets.sdist declares no packages, so the list is the sdist's whole include set, and the sdist carried 54 of 57. A wheel rebuilt from that sdist differs by exactly those three members and raises ModuleNotFoundError on malleus._contract_pipeline.gap_answer, so scripts/ci.py package is RED on main and release.yml's build job stops on a v* tag; tests.yml runs test and docs only, which is why no push saw it. tests/contract_compiler/test_packaging.py is the guard, inside the default selection: 3 failed 1 passed before the fix, 4 passed after. pyproject.toml moved from 12074 bytes sha256:037567e3 to 12643 bytes sha256:7c6d162b; the CC-X02 scan and the CC-X01 correction were re-recorded by --write and refresh-evidence, and no observation changed."
}
```

## Sealing note for OVR-000479

`entries/OVR-000479.json` is sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment, the
previous entry hash where placeholdered, and this file's digest filled in.
