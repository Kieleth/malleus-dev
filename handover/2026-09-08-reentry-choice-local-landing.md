# Re-entry choice consumer: local integration

The user-authorized local merge is
`62655e444dc3188a92df08d9ea018cd1ecf84adc`, tree
`d128493761d88c7167a8c88203de0458b6be303b`. Its first parent is
`ccd62578f5ed0da17dbc897ac180566c0ba8da37`; its second is the sealed consumer
`14d995b22929ea28d14bb39e600f36177556c162`.

The merge adds exactly twelve files under
`research/semantic_reentry_external_design/`. Runtime source remains Git tree
`63bc5650bda806b99fe8fb9fa060f2b8d0b113e2`. No Core runtime, ontology,
dependency, existing Shop file or prior evidence byte changes. Unrelated
working-tree edits remain unstaged. No push, release or publication occurred.

## Bounded result

The original example starts with supplier order B requesting one unit and an
explicit goal of two. An action proposal and its execution receipt cannot
change accepted knowledge. Independent source observation followed by normal
KCS admission changes the accepted quantity; the next goal evaluation emits
no proposal.

The separate choice extension adds synthetic C=1 and an explicit aggregate
goal of three. Without a choice rule it refuses ambiguity. A declared
preference selects B, whose observed update changes B only. These goals are
test inputs, not customer demand inferred from the source.

This is research-local `REFERENCE_IMPLEMENTATION` and `CONFORMANCE_FIXTURE`
evidence under the selected optional history/action profiles. Both examples
keep their original private-v0 machine. They do not adopt the new optional
replacement rule, prove a real supplier service, delivery, generic planning,
independent synthesizer replacement or an installed Re-entry API.

## Verification

Core reviewed the incoming selector, walkthrough, tests and evidence, checked
the exact twelve-file additive merge, and verified the sealed receipt and
four JUnit report hashes and counts: **650 passed, one unchanged optional
private-doctrine skip**, over 651 manifest cases. These are the consumer's
isolated runs at `b5b713b7a65823a893b1077f73cce9ac14531f2a`, not a newly run
full suite on the merge. The executable and dependency closure is unchanged.

Receipt:
`research/semantic_reentry_external_design/supplier-choice-transition-result.json`,
SHA-256 `0359013dce659051a0bedfa895e067271f599776e321f0494c308a0ee9bddbd4`.
The original one-order history and seven companion artifacts, and the optional
two-order history and five companion artifacts, remain byte-identical in the
consumer's recorded compatibility runs. Historical receipts were not relabeled.

Fresh post-merge check in the configured project environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q --tb=short -p no:cacheprovider research/semantic_reentry_external_design/test_supplier_choice.py -k 'gate_'
```

Result: **12 passed, 27 deselected**. These guards check the current Core source
identity, historical evidence and exclusion of older positive epoch guards.
They are not another execution of the full consumer suite. The consumer owner
also independently verified the actual merge and all twelve resulting file
hashes. Start with the consumer's
[one-order explanation](../research/semantic_reentry_external_design/START_HERE.md).
