# Document fixture producer repair

Operator-approved CONFORMANCE_FIXTURE correction for the optional
compiler-enabled, source-assertion profile. No runtime or protocol change.

## Contract

The document trace test must compare a current execution with a recorded
example from its exact compiler producer. The earlier inspection-note fixture
and the fixed two-producer compatibility audit remain byte-identical.

The observed failure at main `816eb2a` occurs before document admission:
`base_ledger_head` differs, while the other thirteen change-set fields agree.
The date/class-alternative compiler repair changed the retained producer
evidence. Its history hash must change; its domain meaning must not.

Reuse the existing document adapter, preparation, admission, reopen and trace
test path. Add only a separately versioned change-set example and a binding to
the compiler artifact, producer and unchanged historical input manifest.
Normal tests never regenerate their expected output or ignore hash fields.

RED must demonstrate the current failure and the absent producer/fixture
guard. GREEN must enforce exact producer and artifact identity, exact output,
unchanged input bytes, graph records, capture attribution, modality, assertion
time, domain time and batch valid time. Corrupted output or a different
producer must fail. The historical document tests also run at their recorded
producer, not against current runtime bytes.

Excluded: the other historical Shop comparisons, sequential actions, runtime
changes, package work, dependency installation, downstream edits, remote push
and a full-repository GREEN claim. This is independently consumable test and
evidence maintenance, not a new fixture framework.

## Evidence

Before edits, both the document trace and its dependent assertion-time test
failed at the same exact-output comparison. Their observed heads were
`sha256:9510c232e487d0b791b1984e7e75f2b0ab1cb38696600c7733096da795a1b105`
and historical
`sha256:5f52eeecdc80479f6b3a0133fd0390d67f39733c12b88fe0c4946790b405c390`.

Corrective RED and GREEN evidence will be recorded after execution.
