# Re-entry consumer, local landing after the release

Status: integrated and verified locally. Not pushed or included in 0.14.0.

Luis approved this separate landing after the maintained-reader work. The
release was published first. Remote main was then advanced only to the release
record, `74c715b4f17eff4e2dca3aaf48b99c13ef4c952f`. No subsequent push belongs
to this transaction.

## Exact integration

The reviewed consumer tip is `3724f70190f7720f234c2c3290aee69975116c17`, tree
`e63d18a27d1160a00dda884f02c4a8da9f2efdf4`. It was merged into local main at
`5f1ebb4d21ce99d7c37259b76dff17bf453a9c2a`, tree
`fbf1f76fbfa2f10751edb1a0002d6c14d5f54dc2`, with the release-record commit as
first parent and the reviewed consumer as second parent. The merge changes
exactly 17 paths, all under `research/semantic_reentry_external_design/`.

Core source remains tree `3b4fd1c9eb66d84c31050b5f0fd970a6fc2572a8`.
The resulting complete consumer directory is tree
`7ca1a1c6bd61bc0d9ff25cdfc01049ad3ba71242`.
The release tag remains at `e2b9e77912f9b36fdbfe2fca310548a789bffb4d`.
These are distinct coordinates, not a rebind of the release or earlier runs.

The consumer can retain a supported observation of quantity three while its
exact-two goal remains unsatisfied. Mapping an observation and satisfying a
goal are different decisions. A falsely recorded confirmation refuses at the
observation-to-change boundary. The maintained Core reader remains read-only;
ordinary knowledge-change admission remains the accepted-state writer.

The consumer remains a research-local `REFERENCE_IMPLEMENTATION`; its added
verification is a `CONFORMANCE_FIXTURE` under the selected optional
history/action profiles. Goal equality, supported
quantities and the no-retry policy remain adopter choices. It adds no Core
ontology term, public API, generic planner, retry mechanism or source-truth
claim. The separately proposed two-supplier aggregate-goal experiment is not
part of this landing.

## Verification on the actual merge

A clean detached checkout at the exact merge ran:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. /Users/luis/Projects/malleus-dev/.venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_maintained_projection.py research/semantic_reentry_external_design/test_maintained_reentry_epoch.py --junitxml=/tmp/malleus-reentry-core-final.g2gu2X/landing.xml
```

Result: **18 passed in 220.35 seconds**, using the declared project environment
with Python 3.12.9. This is thirteen Core maintained-reader cases and five
consumer-epoch cases, not a new full-repository or full-consumer-suite claim.
The checkout remained clean. Scoped Ruff, the merge diff check and governance
validation at 448 entries also passed.

Local JUnit receipt SHA-256:
`2f784726b141fa5ff9bab2674c4ea4a421652775342a05c1122b194ff8bc66d6`.
The captured test output is
`/tmp/malleus-reentry-core-final.g2gu2X/landing.log`, SHA-256
`22f4c13d16f9e74db607c996ca33a2cf7c2111251772556294fc616f1ef3ba41`.
These temporary files are execution receipts, not promised permanent archives;
the exact command, commit and results are retained here.

## Byte boundary

The source and consumer Git trees above bind those complete directories.
Selected boundary files are listed below for direct inspection; this table is
not a separately claimed complete import manifest.

| File | SHA-256 |
| :--- | :--- |
| `src/malleus/compiler.py` | `42e27b2c8946e6e54f578fe4537a36856b822a568004e4e2cc57d8c03debe301` |
| `src/malleus/_contract_pipeline/knowledge.py` | `bbf6416adab228a2d3b1d52c7f29b79fcbefaae30bbcc906830b4176be664441` |
| `accepted_read_view.py` | `fbf16e6a47e7870d8e1c0a5f6aa8d496695f0b0d547cf49454c620e18762cb69` |
| `supplier_initialization.py` | `9f00a5b01693ef23041b9ff2ed92362bf3044cac4c5f444c752688a393ff406d` |
| `supplier_components.py` | `2d7eedd9566fd9b5b062f09c194efdc4ba4b72d3589514cca4f98df6a5d3b172` |
| `supplier_observed_source.py` | `6ebfe4758d9146cc073ff920cb09030db86f73d61c4b48a067a324ad9edb0ccc` |
| `supplier_reentry.py` | `765791f62086b8d2fc29ba81370f2ef207b4994444e39954c2226dce4a5b030c` |

Unqualified filenames in the table belong to the consumer directory. The
initialization helper includes the release compatibility correction for UTC
`Z` parsing on Python 3.10. It preserves recorded timestamp text. That helper
change is explicit here; it is not silently attributed to the earlier consumer
gate.

The earlier `maintained-integration-result.json` remains byte-identical at
`a863f016c13160c123db655e7ea1ad83df59a3975ca2264039d106a1f2fdbb98`, and
`observed-mismatch-result.json` remains at
`92e16933cc574998d8255df76fbbd0bd851bde8c11f836fcc21c01865e4c0743`.
Their broader historical results are not relabeled as fresh runs on this merge.
Unrelated dirty paper and Recon research files were preserved and never staged.
