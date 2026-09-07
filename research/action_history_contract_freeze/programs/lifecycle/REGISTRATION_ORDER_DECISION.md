# Registration needs a canonical string-list check

Status: DECISION_REQUIRED. No instruction or runtime has been added.

The approved registration rules preserve existing Assent semantics. They do
not permit us to accept a different list order or rewrite supplied records.
The remaining question is how the finite language expresses that rule.

## Exact witness

`registration-order-gap.json` preserves these two lists:

```json
{"positive": ["AMEND", "READ"], "negative": ["READ", "AMEND"]}
```

Both fit the complete compiled AuthorityGrant shape. Both contain the same
distinct strings. They have different record hashes. Existing
`src/malleus/assent.py::_canonical_unique` accepts the first and refuses the
second. `_artifact` calls this check for `permitted_action_types`.
`_validate_monitor_specification_artifact` also requires canonical ordering for
`input_artifact_ids`.

The retained candidate tries `REQUIRE_COMPARE`, STRING, LT on the two entries.
The instruction schema refuses it: STRING currently permits only EQ and NE.
Integer/time ordering cannot consume these strings, and no declared operation
converts them to comparable scalar keys.

There is a related operand gap, not another proposed feature. Current
`REQUIRE_UNIQUE` checks explicit field paths on record items. Its nonempty key
path cannot address an entire bare string item. The second retained witness
fails with `UNRESOLVED_PATH`. Wrapping arbitrary scalar items would require a
transformation that the language does not provide. A two-item wrapper specimen
shows keyed uniqueness itself is valid, not that real scalar lists are covered.

Restricting every list to one item would reject the valid two-action witness.
Sorting before retention would change the supplied record and its identity.
Ignoring order would weaken the existing registration contract. None is an
accepted fallback. This is a concrete gap in these declared operations, not a
proof that no conceivable alternative language can express ordering.

## Recommended bounded addition for Luis

Add one definition-only instruction, proposed name
`REQUIRE_SORTED_UNIQUE_STRINGS`, with an explicit finite string-list operand
and typed refusal. It requires strictly increasing lexicographic Unicode
code-point order, matching existing canonical string-list ordering. Repeated
items refuse. Empty and singleton lists satisfy the order/uniqueness check;
nonempty and nonblank requirements remain separate declared field constraints.

The operation must not sort, trim, normalize, case-fold, return transformed
data, call a comparator or change state. Non-string values refuse without
coercion. It adds no arbitrary expressions, loops or callback capability.

This recommendation is not part of `instructions.schema.json`. Approval would
cover only its schema, static checks and registration definitions. It would
not approve history resolution, instruction execution, monitor execution,
event append or effects. The separate read-only preparation approval remains
future and must be dependency-closed.

## Work that did not wait on the decision

`source-registration.json` declares the existing SourceArtifact record,
provenance and byte bindings plus its exact semantic-hash projection and field
checks. `initialization.json` declares checkpoint identity, verified prefix,
six applied prerequisite roles, a singleton initialization slot and the one
permitted initial action-head assignment. Both pass static checking only.

Grant and monitor registration stay incomplete while this language question
is open. Policy registration and the later lifecycle declarations must still
be checked against their complete existing rules. No claim is made that this
is the last possible language gap. The owning authenticated-input and atomic
persistence boundaries also remain unimplemented.
