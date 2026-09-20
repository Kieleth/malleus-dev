# Shop evidence after Core took over every required check

Captured from five fresh histories after the Small Shop programs stopped
running their own checks and writing their own outcomes. Paper ledger E-0502 to
E-0505, decision D option 1: Core runs every check; adopters supply contracts,
rules and change sets, never programs and never outcomes.

## What moved, and what did not

Every exported graph is byte-identical to the preceding generation.
`correction/graph.json` and `showcase/graph.json` have zero changed paths, and
`public_population/evidence.json` carries the same `graph` object and the same
`graph_state_digest` it carried before. No domain value, record, source or
count changed anywhere in the five scenarios.

What moved is identities and ledger coordinates, and two kinds of value that
are not digests. Both are declared leaf by leaf in `binding.json`, under
`changed_values` and `changed_keys`, because the successor guard in
`test_current_evidence.py` refuses an undeclared non-digest change.

**Ledger event counts.** Core retains one receipt per check it runs, where the
programs wrote a `CHECK_RECORDED` event and, in three of the five, retained
nothing at all. The counts:

| scenario | superseded | current |
|---|---|---|
| public population | 48 | 49 |
| object event | 14 | 15 |
| correction | 58 | 55 |
| showcase | 74 | 80 |

Correction's count fell. It wrote two check records and retained two receipts
per change, four events; it now carries one check record, Core's one receipt
and its own source-mapping verification record, three.

`fresh_import` keeps its count: it admits through `admit_structural_change`,
which this step did not touch. Its three changed paths are digests that follow
the moved `pareto/mapping.json` its plans pin as evidence.

**One field name.** `showcase/explanation.json` renamed
`source_mapping_receipts` to `source_mapping_verifications`, and its entries
renamed `receipt_identity` to `record_identity`. The showcase's source-mapping
recompute is still performed, still retained, and still verified from ledger
bytes alone by `verify_source_mapping_records`. What it is no longer is a check
the protocol accepted, so calling its output a receipt was wrong.

**One list length.** `correction/explanation.json` `/checks` went from six
entries to three: two per change to one per change. The correction policy
required two private-grammar check contracts whose executor was the correction
program itself; it now requires one `malleus.check-contract/v1` `CORE_BUILTIN`
document, which Core resolves and runs.

## The identities behind the move

| artifact | superseded | current |
|---|---|---|
| pareto policy | `sha256:c0ec653f…` | `sha256:433f2f9b…` |
| pareto mapping | `sha256:4e8851c5…` | `sha256:ba4291a2…` |
| correction machine | `sha256:825c8d99…` | `sha256:66913e1e…` |
| correction policy | `sha256:57972777…` | `sha256:724f1670…` |
| showcase policy | `sha256:efa0ac20…` | `sha256:c72450aa…` |

The one check contract every migrated program now requires is
`sha256:4cef2ab7e63c87ff3b3290026b6c0b1335b01cea18e30b353adfaf6ce52b8bd9`, a
`CORE_BUILTIN` document naming `malleus.core.operations-apply-atomically`
version `1`. Three check contracts are gone, and the reason is the same for all
three: their executor was the adopter's own program, or nothing at all.

- `retained-source-integrity` at `sha256:8208a293…` matched no file in the
  repository. The pareto programs wrote `SATISFIED` for it from a literal.
- `source-mapping-conformance` at `sha256:d98a2616…` (correction) and
  `sha256:ad5de0ee…` (showcase) named the run program as its executor.
- `structural-conformance` at `sha256:47e59912…` (correction) and
  `sha256:6a0c7419…` (pareto) did the same over Core's own primitive.

The two source-mapping recomputes were kept. They are declared research-local
now, under `malleus.small-shop.source-mapping-declaration/private-v0`, which
still pins the exact entrypoint bytes, and each stage retains its result as
evidence in the same batch as the change. Each program's module docstring says
in full that Core does not vouch for them.

## What this generation pins

`binding.json` retains the exact compiler artifacts and producer identity of
all five scenarios, the complete outputs, and all forty output files from the
four preceding generations, which remain untouched. The recorded
`changed_paths`, `changed_values` and `changed_keys` describe this transition
only.

`connected_story_chain` is carried forward unchanged from the preceding
generation. The connected story's own re-freeze, which the structural fold of
commit `7c3237f0` moved, has not been cut and is not part of this generation.
