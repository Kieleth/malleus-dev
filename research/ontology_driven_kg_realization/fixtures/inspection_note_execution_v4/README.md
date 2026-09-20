# Inspection-note execution once Core runs the check itself

CONFORMANCE_FIXTURE for the optional compiler-enabled, source-assertion
profile. This is a new execution of the unchanged `inspection_note_capture_v1`
inputs. It replaces nothing: `inspection_note_execution_v2` and
`inspection_note_execution_v3` stay exactly as they were, and their digests are
bound below and guarded by test.

What moved. Decision D closed the public admission door: `admit` and
`admit_with_anchors` refuse a caller-written `CHECK_RECORDED` or
`VERDICT_RECORDED`, and Core runs every check its policy requires through
`malleus.check-contract/v1`. The pareto fixture policy used to require two
check identities no document reproduced, `sha256:aaa…` and `sha256:bbb…`. It
now requires two retained `CORE_BUILTIN` contracts naming
`malleus.core.operations-apply-atomically` version `1`. That moved the policy
identity, the normative profile identity and the partial effective contract
identity, and the history retains two more artifacts.

Four change-set fields differ from `inspection_note_execution_v3`, and no
others:

| field | v3 | v4 |
|---|---|---|
| `contract_identity` | `sha256:0a9a02ce…` | `sha256:3a216cda…` |
| `base_ledger_head` | `sha256:c14f1f00…` | `sha256:cc8ce748…` |
| `base_ledger_event_count` | 9 | 11 |
| `evidence` | plan digest of the v3 plan | plan digest under the new contract identity |

Operations, sources, valid time and supersessions are unchanged. The
historical input manifest, the compiled artifact and the producer fingerprint
are unchanged, and `binding.json` binds all three.

These bytes were captured from the real preparation result through the
document test helper, then admitted, reopened and traced per record. No
expected hash was substituted into the result.

```sh
python -m pytest -q tests/contract_compiler/pareto/test_document_fixture_producer.py tests/contract_compiler/pareto/test_population_trace.py tests/contract_compiler/pareto/test_document_assertion_time.py
```

This repairs a current conformance selection. It changes no runtime semantics,
source material, domain meaning or wire grammar, and proves no source truth.
