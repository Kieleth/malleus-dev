# Current-producer inspection-note execution

CONFORMANCE_FIXTURE for the optional compiler-enabled, source-assertion
profile. This directory records a new execution, not new source material or
a new protocol version.

The inputs remain in `../inspection_note_capture_v1`. That entire fixture,
including its older `document-change.json`, remains unchanged. The only
different field in the new change set is `base_ledger_head`: the compiler's
date/class-alternative repair changed its retained producer evidence. The
ontology meaning, operations, source/capture/plan identities and times agree.

`binding.json` records the exact producer, compiled artifact and historical
input manifest identities, plus the new change-set file digest. Its commit
coordinates identify the runtime used for each generation. This is test-local
metadata, not a shipped binding API or persisted protocol grammar.

The new bytes were captured from the actual preparation result of
`tests/contract_compiler/pareto/test_population_trace.py::_document_replay`
at RED `51e9bb2`, whose runtime is unchanged from `816eb2a`. No old expected
hash was substituted in the generated result. The corrected test compares the
whole change set, admits it, reopens the history and traces retained evidence.
The additional guard compares every reopened record with the frozen input plan.
Neither test writes or regenerates its expected files.

Run the document boundary using the repository's configured environment:

```sh
python -m pytest -q tests/contract_compiler/pareto/test_document_fixture_producer.py tests/contract_compiler/pareto/test_population_trace.py tests/contract_compiler/pareto/test_document_assertion_time.py
```

A different producer or changed compiled artifact fails explicitly. Do not
remove that check, overwrite historical evidence, or accept arbitrary hash
differences. A later intentional compiler change needs its own reviewed
execution example. The separate frozen two-producer audit still checks its
original exact commits and is not reinterpreted by this fixture.

No runtime, package, public API, source-truth, general compiler equivalence or
full-repository GREEN claim is made.
