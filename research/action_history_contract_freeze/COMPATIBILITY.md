# Exact Assent compiler compatibility

Operator-approved scope: a REFERENCE_IMPLEMENTATION repair within the optional
compiler-enabled profile. The tests are CONFORMANCE_FIXTURE evidence, not action
execution or base protocol rules. Work is isolated from shared main.

Claim: compile the exact shipped Assent import closure and its neutral
LocalAction import, retain the distinct date range, reload the resulting
artifact, and structurally validate selected action/assessment records.

Observation: positive imports, calendar-date and record negatives, class-level
ValidTime alternatives, source-free artifact reload, and unchanged Shop facts.
Reuse the existing binder, elaborator, identified metamodel, artifact reader,
and structural view. Date keeps its already-bound LinkML type IRI. Its current
string representation is a real YYYY-MM-DD calendar date, as in the pinned
LinkML XSDDate validator and Assent ValidTime's canonical calendar carrier.
No implicit conversion or normalization is introduced.

The previous metamodel explicitly permits five primitive targets. Date support
must therefore identify an exact additive metamodel extension when date is used,
not change the meaning of old identities. Non-date artifacts keep their existing
metamodel. Runtime validation must not require LinkML or a source checkout.

Dependencies: AssentCompatibility consumes ExactAssentClosure; Compiler produces
ValidatedContractArtifact; ContractView consumes ValidatedContractArtifact;
AssentCompatibility conformsTo test_assent_contract_compatibility.py.

Excluded: ontology edits, general scalar expansion, action runtime/interpreter,
policy expansion, executor, observer, substitute records, shared-main
integration, governance append, package/version change, and remote publication.
If another unsupported semantic feature appears on recompiling the complete
closure, report it before broadening this repair.

The predecessor README and snapshot tests describe commit 28cd4b7 only. They
remain historical evidence, not the acceptance suite for this successor.

## Isolated result: date repair, action-input gate still RED

RED `9ec32d40634c927f9c7c160e226152c3782f4c84` collected 20 failing
positive-contract tests, all stopped at the unsupported date range.
Implementation `591cea9bf2682d52071197aa15ba31e531552ed5`, tree
`21c011f65491dcc78894fd6be14ce0ada5134876`, changes exactly the existing
`model.py`, `elaborate.py` and `view.py`. It adds 82 lines and removes 18.
`e6bec7c9b8ef6b60f4743237225c18537abc2457`, tree
`fd2766d6b080de7383f95ca132f98528ead6803e`, updates the directly superseded
date-refusal test and adds a measured non-date Shop semantic-identity control.
Neither commit edits ontology, machine, policy, source, or frozen example bytes.

Both complete imports now compile. The exact Assent closure has 10,858 facts
and validated fact identity
`sha256:f8368d471d9d0dcdba25538ca90acd379cb033312ffc442a340f30c830ff6244`.
The neutral LocalAction closure has 11,015 facts and identity
`sha256:53397ddc9e6ced364f95b39aa97accb78536659527993d09e8875904d3ecca78`.
The range remains `https://w3id.org/linkml/types/date`, not String or DateTime.
No source declaration was omitted. The added primitive uses separately
identified metamodels; the original five-primitive identities are unchanged.

Focused new suite: **19 passed, 1 failed**. Date-only/selected-record selector:
**19 passed, 1 deselected**, not a complete GREEN gate. Public compiler plus
new suite after the diagnostic correction: **29 passed, 1 failed**.
These are overlapping selectors and their counts must not be added.

The selected records are LocalAction, TypeAssessment, AuthorityAssessment and
AuthorityGrant. Required fields, closed assessment kind, enum values, list
shape, integer versus Boolean, Boolean versus string, unknown fields, and
inherited record fields are exercised. This establishes structural validation,
not record authenticity, authority legitimacy or lifecycle enforcement.

## Newly exposed semantic blocker

The artifact retains ExactlyOneGroup, ExactlyOneAlternative and SlotCondition
facts from Assent's class-level ValidTime declaration. `_validate_expressions`
checks their structural integrity during loading. `ContractView.validate_instance`
does not execute them against records. The record validator uses only effective
slot constraints. This is not a date-parser failure or lost source annotation.

Exact counterexample after source-free artifact reload:

```json
{"valid_time_precision":"CALENDAR_DAY","calendar_date":"2026-09-07","timezone":"UTC","timezone_database_version":"2026c","indeterminacy_reason":"Only a day is known","exact_timestamp":"2026-09-07T00:00:00Z"}
```

The compiled view returns `[]`. The existing independent registry path refuses:
`Class 'ValidTime' must satisfy exactly one declared alternative; matched 0;
nearest alternative: Property 'exact_timestamp' must be absent`.
The compiled view also accepts a wrong timezone database string and a
CALENDAR_DAY record missing all day fields. The registry refuses both.
The committed source-free union test stays failing, with no skip or xfail.

The separate Semantic Re-entry task independently reproduced 19 passed and this
one failure against `591cea9b`. No action contract freeze can claim complete
record-semantic compatibility yet. The smallest pending scope is execution of
the already-retained class-alternative facts in the generic record validator,
including inherited/nested use and failure tests. Do not add a ValidTime-named
branch, a new grammar, or action execution. That scope awaits the operator.

## Evidence identity is not semantic identity

A recursive comparison of the entire Shop correction artifact, compiled from
identical sources at exported RED `9ec32d4` and candidate `591cea9b`, finds
exactly two changed leaves: `evidence.producer.sha256` and `evidence_sha256`.
Every fact, metamodel field, source attestation and semantic identity is equal.

| Coordinate | Predecessor | Candidate |
|---|---|---|
| Facts SHA-256 | `b20ea4ce27f052fc00b9310ca30cf437b451949e0daf33d717a690fb895beb3a` | unchanged |
| Validated fact SHA-256 | `0af9eb01495af3c7ed063cb8ca340b63b475eb72feeb2f81fe9be48720fd515e` | unchanged |
| Producer SHA-256 | `5eb3ca2ba74e8cee3d8e7f5d4710ae026f728ffa5923d215a00c40716c03edcf` | `909f04bfdb9aa946a5f8213361deea4aae1f2871589500ac5bae24b0b9bc19c9` |
| Whole artifact SHA-256 | `6db461526db4c1eb4e040cbf486505dcc630c7be5decc9a4df7f4ba0f2c4d7c8` | `6c81bb3a860d5266c0133ed616185d4a52fd4dec5d52f4a3934b4c6e47a98c34` |

`elaborate._evidence` hashes its compiler implementation files. Retaining the
new artifact therefore changes the history prefix and later change-set,
receipt and ledger hashes. These are genuinely new execution attestations;
they must not be relabeled as the predecessor's exact-byte reproduction.

Two real from-empty fresh-Shop runs, one under each coordinate, reopen to
exactly equal exported graph records and state digest
`sha256:ac6bc4c2a6be7ee851e0229b49276b11a8e0dbf91ed203705d611093c783e998`.
Both retain 12 historical records and 59 ledger events. Their reports differ
only in ledger_head, ledger_sha256 and receipt_identity. Imported records,
source identity, derivations, counts and unchanged-prior-record checks agree.
Candidate ledger SHA-256 is
`0d0387d244a50854865dc39b5e29b2cbbbf0f77dd9f5562a2bac0c64dbc03c63`;
predecessor is
`c20c0c802b695a34983de1245b8f20cd3eba6ecbf2ce580ac213c316fe0cba7f`.
The temporary runs did not overwrite any frozen receipt or oracle.

## Reproduction

Use the configured project environment, with this isolated checkout first on
PYTHONPATH. No installation or dependency change was performed.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_assent_contract_compatibility.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_assent_contract_compatibility.py -k 'not valid_time_union'
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_public_compiler.py tests/contract_compiler/pareto/test_assent_contract_compatibility.py
```

The failing union remains intentional evidence of an unresolved requirement,
not an expected-success assertion about unsupported behavior.

## Approved successor scope

The operator subsequently approved execution of the existing retained
ExactlyOneGroup/SlotCondition rules. This supersedes the pending-scope sentence
above, not the recorded partial result. New REDs exercise generic conditions,
zero and multiple matches, parent/mixin/local conjunction, nested records,
qualified property names, immutable inputs, source-free reload and deterministic
diagnostics. No ontology change, new expression grammar, action runtime or
effect is authorized. Existing frozen evidence stays untouched.
