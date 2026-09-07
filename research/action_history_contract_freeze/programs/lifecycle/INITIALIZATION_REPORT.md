# Initialization and prerequisite definition evidence

Status: STATIC_VALID_PARTIAL. Definitions only, no action runtime activation.
The canonical-list instruction question remains DECISION_REQUIRED.

## Delivered

`initialization.json` contains a 49-instruction static specimen. It validates
the selected full SourceArtifact variant, binds checkpoint identity and the
current prefix/domain coordinates, names six applied prerequisite roles,
requires a singleton initialization slot, and assigns the computed checkpoint
digest to the separate action head. It has no domain-state target. The A value
is the raw checkpoint content digest under the already accepted rule; the
destination identifies the coordinate. Supplying a domain-tagged digest in its
place fails static validation.

`source-registration.json` contains a 13-instruction static specimen and the
explicit source semantic-hash projection. The projection maps record `id` to
preimage `artifact_id`, retains the six other existing source fields, and does
not hash record provenance as source semantics. Its field-check declarations
retain the existing version, nonblank, digest and nonnegative-integer rules.
Tests compare the declared projection with `source_artifact_digest` and verify
that a changed responsible actor changes record identity but not source
semantic identity. These tests do not execute the proposed HASH instruction.

The initialization program declares profile, record contract, machine and
history binding as applied byte-carrier inputs. Epistemic and authorization
policies resolve by their applied record hashes. No current-context dictionary
is authenticated merely because it has these fields.

`registration-order-gap.json` preserves the exact unsupported order and scalar
uniqueness attempts. The existing compiled grant accepts both selected array
shapes; existing Assent canonical-list validation distinguishes their order;
the research instruction checker refuses the attempted instructions. The
required decision and no-normalization rationale are in
`REGISTRATION_ORDER_DECISION.md`.

## Commits and tests

RED: `84ff65cee6b88c2ad7428997ca958a980a6732c2`, tree
`cc7701d1eaf11a23c5ec7be10ef8449d47a0afa8`. All 12 initial tests failed because
the three definition files were absent. Three additional conformance guards
were added before GREEN: full-grant reachability, the bare-string uniqueness
witness, and source field-check preservation. The latter two first failed on
their absent declaration fields, then passed with those fields retained.

GREEN: `8f980dfed207930b1d4a3093a4dcb71c686356cf`, tree
`272e36b82c1a73b0ce4fbe8a73f8273a6605dbc8`.

Focused: **15 passed, zero skipped**. The broader selected
research/compatibility gate passed in the owner checkout and a clean detached
checkout: **360 passed, zero skipped**. This is not the complete repository
suite and is owner-run evidence, not an independent audit.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m pytest -q -p no:cacheprovider -c pyproject.toml \
  research/action_history_contract_freeze/programs \
  research/action_history_contract_freeze/test_transaction_decision.py \
  research/action_history_contract_freeze/test_definition.py \
  tests/contract_compiler/pareto/test_assent_contract_compatibility.py \
  tests/contract_compiler/pareto/test_contract_alternatives.py \
  tests/contract_compiler/pareto/test_public_compiler.py \
  tests/test_assent_ontology.py \
  tests/test_compiler_compatibility_gate.py --tb=short
```

Actual configured interpreter: `/Users/luis/Projects/malleus-dev/.venv/bin/python`.
The owner checkout is `/private/tmp/malleus-action-contract.X6QNEw/repo`.
Clean validation ran at `/private/tmp/malleus-output-fields.vrZhR0/repo` and
left its status empty. Changed-test Ruff, format and base-to-GREEN diff checks
passed. No dependency installation or network access was used.

Exact SHA-256 identities, paths relative to this directory:

| File | SHA-256 |
| :--- | :--- |
| `initialization.json` | `343c7460050efcf0eaf27867860f4513f7cc3b5f818dd3f471bd747af3a0d48b` |
| `source-registration.json` | `6fb68d138c833519592f1918bed862a3f5711733095c279dbd621c26ed77634c` |
| `registration-order-gap.json` | `713af3cb9d15ae0d1a4756b0a78d7f2ae78479d8b36caeddb94f22de34df6a0d` |
| `test_initialization.py` | `7908f336a62645aaa030bd52b84a0c21b4877c27c7f0b6eeb09a11df94f0e7b1` |

## Remaining closure and approval boundary

The existing eleven-instruction grammar is unchanged. The proposed
`REQUIRE_SORTED_UNIQUE_STRINGS` definition needs Luis's approval before it is
added. This changes no grant or monitor rule; it makes an existing rule
expressible in the proposed language. Per the Malleus development skill, a new
instruction is not silently inferred from authorization to complete programs.

Initialization/source registration now have concrete static specimens, not
complete runtime implementations. Authentic retained-byte and applied-record
views, semantic-content parsing, transitive dependency order, actual producer
bindings, trusted headers and final commit checks remain unimplemented.
Grant/monitor registration and later lifecycle programs remain incomplete.
Do not claim the remaining language is sufficient until those programs close.

After definition closure, the next proposed executable deliverable remains
the research-only read-only preparation proof described in
`CONTEXT_PROPOSAL_REPORT.md`. Its separate approval has not been given by the
consumer messages, this report, or these passing tests. It excludes appends and
effects. Actual atomic persistence is a later, independently tested boundary.

## Non-claims

No history input was resolved, no proposed instruction ran, and no check
producer, event, action or KCS was executed. Nothing proves authentication,
retention, action legitimacy, transaction rollback, replay equivalence,
concurrency, durability or portability. Public/production code, instruction
grammar, ontology, package settings, shared main, Core governance, paper and
adopter files are untouched. The earlier context/proposal packet remains
unchanged. No merge or push occurred. The enclosing report commit identifies
this successor without rewriting the earlier evidence.
