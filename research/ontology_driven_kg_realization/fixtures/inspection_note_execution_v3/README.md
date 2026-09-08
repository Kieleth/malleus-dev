# Inspection-note execution at the release candidate

CONFORMANCE_FIXTURE for the optional compiler-enabled, source-assertion
profile. This is a new execution of the unchanged `inspection_note_capture_v1`
inputs, not replacement evidence for either earlier execution.

The clean release check at `815ed63b` caught the old execution's compiler
producer mismatch. Commit `8d315fbd` had added exact-identity verification to
the compiled view for rule checks. That changed the producer fingerprint and
retained bootstrap bytes, but the document comparison still selected v2.

These bytes were captured from the real preparation result through the existing
document test helper at `815ed63b`. Admission, reopen and per-record trace then
completed. The only change-set field differing from the historical example is
`base_ledger_head`. Operations, source/evidence identities and valid time are
unchanged. No expected hash was substituted into the result.

`binding.json` binds the exact producer, compiled artifact, historical input
manifest, this output and the preceding v2 evidence. Tests compare the complete
canonical change set, reject a different producer, reopen and inspect every
record, and guard the earlier evidence against rewriting.

```sh
python -m pytest -q tests/contract_compiler/pareto/test_document_fixture_producer.py tests/contract_compiler/pareto/test_population_trace.py tests/contract_compiler/pareto/test_document_assertion_time.py
```

This repairs a current conformance selection. It changes no runtime semantics,
source material, domain meaning or wire grammar, and proves no source truth.
