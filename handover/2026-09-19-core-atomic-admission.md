# Compile, check and admit as one Core operation

ROADMAP F1. Luis ruled it on 2026-09-19 (paper ledger E-0486, E-0488): "this is
part of the malleus protocol and should be enforced by it." Built before any
further model run, ahead of the `RULE_DECLARES_ITS_READS` constraint that the
same ruling sequenced after it.

## The fact nobody had measured

F1 asked for it in writing: "RED first: a test that admits without a check and
shows what Core does today." Measured on a history with a Prolog `PolicyProgram`
installed, the Shop's own shape. Two results, and the second is the one that
matters.

**An admission carrying no `CHECK_RECORDED` event refuses.**
`KnowledgeChangeRefusal`, reason `PROTOCOL_REFUSAL`, detail exactly
`machine event refused: MISSING_REQUIRED_CHECK`, ledger bytes unchanged.
Through `admit` and through `admit_with_anchors` alike. A batch carrying only
`CHANGE_PROPOSED` refuses `INCOMPLETE_ADMISSION`.

**An admission carrying a fabricated `CHECK_RECORDED` is accepted.** The event
names the required contract id and identity and carries `outcome: "SATISFIED"`.
No engine ran, no receipt was anchored, and the records in the change set
violate the very rule that contract declares. The ledger accepted it: two
change sets, eighteen events.

So Core checked the *shape* of the event set and read the verdict off it. The
`SELECT_POLICY_VERDICT` instruction on `VERDICT_RECORDED` requires a
`CheckRecord` for every check the policy names, and `REQUIRE_POLICY_CHECK_OUTPUT`
on `CHECK_RECORDED` requires the contract identity to be one the policy
requires and the outcome to be one the policy maps. Neither runs anything. The
running lived in adopter code.

Both tests are in the new module and both passed before this change and after
it. They are the measurement, not the fix.

## What landed

`malleus.compiler.check_and_admit_population_plan`, on the public compiler and
population facade. Implementation in
`src/malleus/_contract_pipeline/admission.py`.

```python
admitted = compiler.check_and_admit_population_plan(
    history=history,                 # the semantic ledger
    plan_bytes=plan_bytes,           # the plan as its producer wrote it
    history_profile=profile,         # the bound DomainHistoryProfile
    transaction_time="2026-09-03T00:00:00Z",
    actor_id="actor:producer",
    retained_source_texts=(),        # sentences a rule compares against
)
```

Returns `PopulationAdmission`: the replay, the change set, the
`LogicCheckResult`, the check contract id and identity, the plan id and
identity, the receipt id and identity, the gap count. Refuses with
`PopulationAdmissionRefusal`, carrying `stage` (`COMPILE`, `CHECK`, `ADMIT`),
`reason`, `detail`, `ledger_unchanged`, and for a content-rule refusal the
`check`, the `violated_rule_ids` and the `witness_record_ids`.

The check engine is not a call-site choice. The history's `PolicyProgram` names
its required check by identity; the operation reads it from
`KnowledgeHistoryReplay.required_checks` and loads the retained descriptor and
rule bytes that reproduce it. A `LogicContract` names no engine and closes its
fields, so a retained check contract of that shape is a Prolog contract and
`PrologVerifier` runs it. No callback, no engine parameter, no outcome
parameter.

Whether a rule may read provenance is the contract's declaration too. A fact
contract that declares no `m_derivation` gets none; the plan's own derivations
become facts when it does; and supplying `retained_source_texts` against a
contract that cannot read them refuses rather than dropping them in silence.
Core resolves no locator into text itself.

Also landed, because the adopters were working around its absence:
`LogicContract.from_bytes(descriptor_bytes, rules_bytes)`. Both shipped runners
wrote retained bytes into a temporary directory to call `LogicContract.load`.
`load` now reads its two files and delegates to `from_bytes`.

`population_retention_events` moved from `compiler.py` into
`population.py`, where the logic it serves lives, so the new private module can
use it without a cycle. The public name and behaviour are unchanged.

## Bound slice

1. **Claim.** Under a history whose installed policy requires exactly one
   retained check contract, one Core operation compiles a producer-written
   plan, runs that check over the would-be accepted state, and appends the
   retained plan, its gaps, the profile artifact, the change set, the check
   receipt and the three protocol events in one act, or refuses naming the
   stage. The outcome recorded is the engine's.
2. **Smallest observation.** On the Shop-shaped fixture: a fabricated
   `SATISFIED` admits two conflicting records today; the same plan through the
   operation refuses at `CHECK` with `NO_CONFLICTING_QUANTITY` and both record
   ids as witnesses, and the ledger bytes are unchanged.
3. **Reused.** `compile_population_plan`, `prepare_population_change`,
   `population_retention_events`, `KnowledgeChangeHistory.admit_with_anchors`,
   `KnowledgeHistoryReplay.required_checks`, `PrologVerifier`, `stage_subgraph`,
   `LogicContract`, `execute_event`, `_staged_properties`.
4. **Excluded.** Source and evidence anchoring (unchanged). Export (unchanged).
   The content of the rules (unchanged). `REBIND_CHECK_CONTRACT` semantics
   (unchanged). Plan authoring: a document capture still reaches plan bytes
   through `adapt_document_assertions`. Locator-to-text resolution. Policies
   requiring other than one check. Histories whose required check is Core's own
   structural check, which keep `admit_structural_change`.

**Role classification.** The guarantee is `OPTIONAL_PROFILE`: semantic-history
with logic-monitoring. It binds only for an adopter that claims both, because a
history that claims neither has no ledger and no check contract. The shipped
function is the `REFERENCE_IMPLEMENTATION` of that admission path. The atomic
fail-closed refusal it preserves is an already-claimed `PROTOCOL_INVARIANT`;
this adds no new invariant. Lowest affected profile: semantic-history. An
adopter that does not claim it gives up every claim about ledger authority,
replay and admission, this operation included.

## Two consumers, not one adapter

The sequence was absorbed from the Shop experiment's runner at
`private/shop-progressive-01/producer/workspace-stage-c/runner.py`
(`compilation`, `_producer_plan`, `selected_contract`, `check_base`,
`check_writes`, `admit`, `_check_and_admit`). The second consumer with a
different shape is the document path at
`paper-v4/experiment-v4/content-rules-doc-02/admit.py`. They differ in four
places, and the operation is written against both:

| | Shop runner | Document path |
|---|---|---|
| Machine program | private-v1 with `admission_rules` | `STRUCTURAL_HISTORY_BUNDLE`'s |
| History profile | an adopter `DomainHistoryProfile` | `SOURCE_ASSERTION_PROFILE` |
| Fact contract | version 2, no provenance | version 3, derivations and sentences |
| Plan origin | a producer JSON file | `adapt_document_assertions` |

Tests cover both shapes: the Shop-shaped fixture for the machine program,
adopter profile and version-2 contract, and a version-3 contract whose rule
reads `m_derivation` and `m_source_text` for the document shape.

Neither consumer is modified here. `private/` and `paper-v4/` were out of
scope for this change.

## Two defects found in the consumers on the way

Both are in adopter code, both now fixed inside the operation, neither
patched in the consumers (out of scope).

**Shallow-copied frozen properties.** Both runners build the staged check graph
with `properties=dict(operation.properties)`. A change set freezes list values
into tuples and the ontology validator accepts only `list` for a multivalued
slot, so any multivalued property would refuse at the check. Core already knew:
`tests/contract_compiler/pareto/test_repository_guards.py::test_staged_writes_thaw_the_frozen_change_set_properties`
guards the same mistake inside `knowledge.py`. The operation uses
`_staged_properties`, and
`test_the_staged_check_writes_thaw_the_compiled_operations_properties` pins
that one call site by AST so the shallow copy cannot come back.

**A violated plan left its bytes in the ledger.** Both runners call
`prepare_population_change`, which appends the retained plan, gaps and profile,
*before* running the rules. A `VIOLATED` outcome then refuses the admission and
leaves the retained plan behind. The operation runs the check first, over the
compiled operations, so a `CHECK` refusal writes nothing at all.

## Residuals, named

**The raw path is still open.** `admit` and `admit_with_anchors` remain public
and still read a caller-supplied outcome off a `CHECK_RECORDED` event. Luis's
guarantee was "no admission exists in a ledger without its check, because there
is no other way in." There is still another way in. Closing it means Core
refusing a `CHECK_RECORDED` whose receipt it did not produce, which needs an
answer to "which check contracts can Core run?" (only Prolog ones today) and
would change `admit_structural_change` and every existing consumer. That is a
decision, not an omission. **Open for Luis.**

**`ADMIT` is not byte-total.** `COMPILE` and `CHECK` refusals write no byte. An
`ADMIT` refusal may leave the retention batch that precedes it, because a change
set binds ledger coordinates (`base_ledger_head`, `base_ledger_event_count`)
that exist only after that batch is appended, and `_admit` puts the change event
first in its batch so its anchors land after it. Folding retention into the same
batch means either predicting the ledger's hash chain in memory or letting
anchors precede the change event in `_admit`. Both are changes to the admission
primitive and neither is needed by any observation F1 asked for. Nothing is
admitted on an `ADMIT` refusal and every refusal reports `ledger_unchanged`.

**ROADMAP section F is not committed.** The skill's "Rules and the ontology"
section points at ROADMAP items F1, F3, F4 and F5. At `ff1c6931` `ROADMAP.md`
ends at section E; section F exists only in the main checkout's working tree.
Read F1 there.

## Evidence

- `tests/contract_compiler/pareto/test_atomic_population_admission.py`,
  18 tests. Against a pristine tree at `ff1c6931` with only this file added:
  16 failed, 2 passed, and the 2 that pass are exactly the two step-1
  measurement tests. With the change: 18 passed.
- CI quality command (`ruff check` over `scripts/`, `tests/contract_compiler`,
  `src/malleus`): all checks passed. Repository-wide `ruff check src tests`
  reports the same nine pre-existing findings as `ff1c6931`, none in the new
  files.
- Full default suite at `ff1c6931` before the change: 3518 passed, 3 skipped,
  0 failed. After the change: 3512 passed, 3 skipped, 24 failed. The arithmetic
  closes: 3518 + 18 new = 3536 = 3512 + 24.
- All 24 failures have one cause, the governance digest guard:
  `OVR-000463: latest document digest mismatch for pyproject.toml`.
  Seven in `test_contract_compiler_ledger.py`, fourteen in
  `test_contract_compiler_integration.py`, three in `test_docs.py` where the
  strict Sphinx build runs the same validation and the test asserts its return
  code. Every file this change touches except `src/malleus/logic.py` is a
  governed document, so the ledger's recorded digest for each is stale until
  OVR-000467 is sealed. Nothing else fails.

The draft entry is the last section of this file, validated in check mode
against the schema, the hash chain and the document history, and left unsealed.
The Overlord seals it.

## OVR-000467 draft, unsealed

The Overlord seals. This block lives here, not in
`design/contract_compiler/overseer/entries/`, because that directory holds
sealed entries only: an unsealed file there makes `load_ledger` refuse
`head entry_count is 466, found 467 entry files`, which costs five test
failures beyond the digest guard.

Two things the sealer settles, both the same ones OVR-000464 needed. The entry
number and `previous_entry_hash` are correct against this worktree's head,
`OVR-000466` at
`sha256:0eb70a735e843fe9d22bf3032e3efe8be49deea4cc6c8b7678449461f89aaa7b`; if
another block lands first, renumber and rechain, which changes `entry_hash`.
And this handover is deliberately absent from `documents`: its own digest
cannot be recorded inside itself. Add it at seal time with the sealed digest,
or leave it out, but do not record a value computed before this block existed.

Validated in check mode without sealing: `entry_hash` reproduces from the
ledger tool's own `entry_hash()`, `previous_entry_hash` equals the recorded
head, and `load_ledger` over a scratch copy of the overseer directory with the
head anchor advanced passes the whole validation against this working tree,
467 entries, head `OVR-000467`. `why` is 1198 of 1200 characters and every
commit reference is full 40-hex.

```json
{
  "actor": {
    "id": "overseer",
    "type": "OVERSEER"
  },
  "data": {
    "affected_ids": [
      "CC-R11"
    ],
    "documents": [
      {
        "after_digest": "sha256:95460b0cbdfe8f1f4556a646095fdfa6f6f57ce4948f194e69456f2ae1eccac3",
        "before_digest": "sha256:6b58a63c45cd80bba1855b50a68dccb3ff1d960d619e15722f4d4afc2678b49d",
        "change": "MODIFIED",
        "path": ".claude/skills/malleus-dev/references/CAPABILITIES.md"
      },
      {
        "after_digest": "sha256:f9d435fd79a5d577504b57f482fde41c2776ddf1e8c6dfb5f7b404b1d29fef48",
        "before_digest": "sha256:9c216950a24b79a26db18fe22a926fdab3aa7acbc3188b6247260ac7a037a241",
        "change": "MODIFIED",
        "path": "CHANGELOG.md"
      },
      {
        "after_digest": "sha256:9418e7dd42122c9c5e9164243b010b80e58e244dfb1d65c1efd35ead118aaf98",
        "before_digest": "sha256:7711f7ff8d3d1fb4cbe3ebc8c448cd1281529f82e85add0245f7a499459a2caa",
        "change": "MODIFIED",
        "path": "docs/IMPLEMENTATION_STATUS.md"
      },
      {
        "after_digest": "sha256:18722eac7d88e67cfc7ce569f5a296c38c729fc5a6d017d3d20e76d492a6b8bd",
        "before_digest": "sha256:e74485f203b8f0859f50b9e097740afadf0aa049ce51e73f31a74041417f2232",
        "change": "MODIFIED",
        "path": "docs/contract_compiler/index.md"
      },
      {
        "after_digest": "sha256:a590d79b3ca5a055127fc337995192a34309aa2f4511cd8338e1284aeb7b1117",
        "before_digest": "sha256:6d78a1a76564bb487b26f9bfe97e60b0b6706a002d1056e97dabbaf5037a997f",
        "change": "MODIFIED",
        "path": "pyproject.toml"
      },
      {
        "after_digest": "sha256:b77ffdc57b3dcbb060d02e688336647b1c01c00cb3ab4e5bea9fdd09f849ad19",
        "change": "CREATED",
        "path": "src/malleus/_contract_pipeline/admission.py"
      },
      {
        "after_digest": "sha256:5a0f32e40fe3f988a3cf6008e2a9ce32de93fd840af5da31c3699eae8a6a5b0b",
        "before_digest": "sha256:65813f59732134a7dda63ebd3e207509874278ded5594a8d62ade1cf4c5ea128",
        "change": "MODIFIED",
        "path": "src/malleus/_contract_pipeline/population.py"
      },
      {
        "after_digest": "sha256:b1e5d92e495455682f82cb765f2a001e253f21898da6028d1dbc79ac0058f892",
        "before_digest": "sha256:0da568741f94ecb3582a38f0b1a39eca9e3e7927f9bbe22218fda9667c415145",
        "change": "MODIFIED",
        "path": "src/malleus/compiler.py"
      },
      {
        "after_digest": "sha256:822c39a468be0b76c612ca306bd8e7db23514c72a73484e488ac05d8a9a88e12",
        "before_digest": "sha256:c6bff2ec648743c54a5f1d5cbb242d8f71b13c332d08d1840ebfa994653858b3",
        "change": "MODIFIED",
        "path": "src/malleus/logic.py"
      },
      {
        "after_digest": "sha256:2d28b7bf983d4987f03062f6b29dcb9ce02f4272b5aef7b7f78d5d68dc7206c6",
        "change": "CREATED",
        "path": "tests/contract_compiler/pareto/test_atomic_population_admission.py"
      }
    ]
  },
  "entry_hash": "sha256:1e1133e14c130d09bede826816faf9e66db35870a3b69f1f68dd1b66f37ae073",
  "entry_id": "OVR-000467",
  "entry_type": "DOCUMENT_REVISION",
  "ledger": "overseer",
  "previous_entry_hash": "sha256:0eb70a735e843fe9d22bf3032e3efe8be49deea4cc6c8b7678449461f89aaa7b",
  "recorded_at": "2026-09-19T12:00:00Z",
  "references": [
    {
      "relation": "EVIDENCES",
      "target": "605cf5197b3961833d5ea122e7706e30c62ed85a",
      "type": "COMMIT"
    },
    {
      "relation": "AFFECTS",
      "target": "CC-R11",
      "type": "WORKSTREAM"
    }
  ],
  "schema": "malleus.contract-compiler.ledger-entry/v1",
  "sequence": 467,
  "subject": {
    "id": "core-atomic-admission",
    "type": "DOCUMENT"
  },
  "summary": "Record one Core operation that compiles, checks and admits a population plan, and the measured hole it closes.",
  "why": "ROADMAP F1 (E-0486, E-0488): compile, check and admit become one Core operation, enforced by the protocol, not rewritten by every adopter. RED first, as F1 required. On a history with a Prolog policy installed, an admission carrying no CHECK_RECORDED refuses PROTOCOL_REFUSAL 'machine event refused: MISSING_REQUIRED_CHECK' and writes nothing; a fabricated CHECK_RECORDED with outcome SATISFIED is accepted with no engine run. Core checked the event set's shape and read the verdict off it. check_and_admit_population_plan takes plan bytes, compiles against the required contract, resolves the required check from required_checks, loads the retained bytes reproducing it, runs it over the would-be state, and appends plan, gaps, change set, receipt and three events. No parameter carries an outcome. PopulationAdmissionRefusal names COMPILE, CHECK or ADMIT; the first two write no byte. Absorbed from two consumers of different shape, the Shop runner and the document path, fixing two defects both carried. 18 tests: 16 failed at ff1c6931, 18 pass now; suite 3512 passed, 24 failed, all this block's digest guard. Residual: admit_with_anchors stays public, so the fabricated path remains reachable."
}
```
