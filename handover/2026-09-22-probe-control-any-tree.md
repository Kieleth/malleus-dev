# The LinkML-free probe's control holds from any checkout

Overlord (the Core session), 2026-09-22 UTC.

## What happened

The F2 seal (OVR-000477, main e33467f6) shipped `tests/contract_compiler/pareto/test_ontology_source_set.py` with a control test for the LinkML-free replay probe: the probe must fail when pointed at the wrong tree. The control constructed the wrong case by running the probe with an empty PYTHONPATH, which fails only where the installed package lives in another tree. From a worktree that is true; from the main checkout the installed package is the tree under test, so the control passed where it should fail. The full default suite on sealed main read 1 failed, 3863 passed, 2 skipped, exactly this test; on the branch it had read green.

The fix (commit f02bd50f): the wrong tree is an empty temporary directory, never the installed package's own location, so the control refuses from any checkout. RED: the failure on main e33467f6 as recorded above. GREEN: the file reads 17 passed in the fix worktree and 17 passed from the main checkout after the fast-forward.

## Overseer entry

```json
{
  "actor": {"id": "overseer", "type": "OVERSEER"},
  "data": {
    "affected_ids": ["CC-R11"],
    "documents": [
      {"after_digest": "<digest of this file once final>", "change": "CREATED", "path": "handover/2026-09-22-probe-control-any-tree.md"},
      {"after_digest": "sha256:1a77b043272786a83596215e63a4ede7cb397de22c6917a4d46c250ded64be7f", "before_digest": "sha256:d4ad4a3553570c029c866bab86708b67ec1150bef858257897e4a15efa219b2a", "change": "MODIFIED", "path": "tests/contract_compiler/pareto/test_ontology_source_set.py"}
    ]
  },
  "entry_id": "OVR-000478",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "<previous entry hash>",
  "recorded_at": "<sealing moment, UTC>",
  "references": [
    {"relation": "EVIDENCES", "target": "f02bd50fb38929107878fd1427877ad798b0f4fb", "type": "COMMIT"},
    {"relation": "AFFECTS", "target": "CC-R11", "type": "WORKSTREAM"}
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 478,
  "subject": {"id": "probe-control-any-tree-2026-09-22", "type": "DOCUMENT"},
  "summary": "Fix the F2 probe control test so it fails on a wrong tree from any checkout, not only from a worktree.",
  "why": "OVR-000477 sealed a control test whose wrong case depended on the installed package living in another tree, which is true in a worktree and false in the main checkout; the full default suite on sealed main read 1 failed on exactly that test. The wrong tree is now an empty temporary directory, so the control refuses everywhere. One governed test file changes; nothing else moves."
}
```

## Sealing note for OVR-000478, 2026-09-22

`entries/OVR-000478.json` was sealed by the operator with the ledger tool's own
hash, render and check from the draft block above, with the sealing moment,
the previous entry hash where placeholdered, and this file's digest filled in.
