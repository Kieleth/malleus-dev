# Independent compiler compatibility gate check

This CONFORMANCE_FIXTURE closes the approved two-producer compatibility audit
under the compiler-enabled OPTIONAL_PROFILE. It adds no base-protocol guarantee.
Without that profile, this compiler-specific verification makes no claim.

The requirement is exact historical reproduction with the original producer,
current behavior with the repaired producer, and independent semantic parity.
The observation is the one-entry gate result plus its full raw reports and
paired probes. It reuses Core's gate and public compiler/Shop seams. It excludes
action implementation, new ontology or fixture semantics, and full repository CI.

The earlier [compiler input result](compiler-input-result.json) is frozen
historical evidence. Its then-unapproved gate disposition is not rewritten.
The later approval and new observations are recorded separately here.

## Independent result

Core gate implementation `2af45e03ee7d7bf528cef8db42c0798e6d99685b`, tree
`11704829d941e126424ee0e7138a74c8d2195b5b`, passed the complete one-entry
gate in an independent local clone. Its checkout remained clean.

| Observation | Actual result |
| --- | --- |
| Nine tests with original producer | 9 passed, no skip |
| Entire bound repaired-producer suite | 1165 passed, 9 failed, 1 existing xfail |
| Independent paired behavior probes | Six scenarios pass coverage and parity |
| Gate guards plus actual compiled Assent input checks | 36 passed |
| Bounded compatibility verdict | BOUNDED_COMPATIBILITY_PASS |
| Raw repaired suite is green | False |

The nine failures match their exact bound test, assertion location and typed
comparison operands. They are not waived by test name. The probes run past the
historical equality assertions and compare full graph records, retained source
evidence, supported plan traces, assertion times and supersession links.
The 32 differences are exactly the enumerated producer/receipt identity leaves.
No graph value, source hash, plan or time is excluded.

The receipt, raw reports, code closure and probe digests were checked again
after execution. The receipt binds both Python files, including the probe
helper, and the immutable manifest. A helper-only identity mutation has a hard
guard test. Changed-file Ruff, formatting and base-to-head whitespace checks pass.

## Refusal and regression

The first independent run at `88fd1db` refused an unexpected tenth failure:
an archive omitted Git history needed by the existing Shop journal test.
Its raw result was 1164 passed, 10 failed and 1 existing xfail.
The same journal test passed in a clean checkout containing the required commit.
Its semantic probes already passed; those did not override the refusal.

Core's corrective RED `e18eb368c52a9149e4d6c7a471cbe0e37582f9eb`, tree
`bed358c280c63b323c4d2430913e93f844c088ec`, adds a guard executing that real
journal test inside the selected snapshot. Independent execution reproduces
one failure. The corrected detached-checkout setup passes the same guard.
It retains required local Git objects and checks tracked-file cleanliness.
No extra failure allowance, changed equality or rewritten receipt was added.

## Evidence and landing dependency

[compiler-gate-result.json](compiler-gate-result.json) retains the independent
receipt value, both raw reports, exact file hashes, commands, RED/GREEN
coordinates and exclusions. Receipt-internal hashes cover canonical JSON values;
the separate file hashes also cover the files' trailing newline.

Core's evidence-only handoff is
`ff0e1b31f3b44be56a63465b9180d7bbf4c17e54`, tree
`b02650464120d2f43ba28c4613b9c01d7f8d6806`.
Its only changes after the verified implementation are its report and retained
result. Its receipt value equals the independently obtained value.
The Core gate adds six files relative to compiler handoff `1be958e`;
it changes no runtime, frozen receipt or old equality assertion.

This consumer packet adds only this report and its JSON evidence relative to
`67b7ec2`. The sixteen consumer tests and all earlier fixture/design bytes
remain unchanged. No dependency was installed, and no shared checkout or paper
work was edited.

Landing dependency remains Core's compiler repair and bounded gate first, then
this consumer evidence. No merge or push occurred. This clears the compiler
prerequisite for the already-approved action contract definition. It does not
finish that definition: initialization/context shapes, digest recipes, typed
capabilities and check-producer identities still need explicit closure.
Supplier action execution and the full observed external-world loop remain
unimplemented and outside this approval.
