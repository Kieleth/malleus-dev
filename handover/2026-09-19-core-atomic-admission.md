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
  0 failed. After the change: 3511 passed, 3 skipped, 24 failed. The arithmetic
  closes: 3518 + 17 new = 3535 = 3511 + 24; the eighteenth test arrived after that run.
- All 24 failures have one cause, the governance digest guard:
  `LedgerValidationError: latest document digest mismatch for pyproject.toml`.
  Seven in `test_contract_compiler_ledger.py`, fourteen in
  `test_contract_compiler_integration.py`, three in `test_docs.py` where the
  strict Sphinx build runs the same validation and the test asserts its return
  code. Every file this change touches except `src/malleus/logic.py` is a
  governed document, so the ledger's recorded digest for each is stale until
  OVR-000467 is sealed. Nothing else fails.

The draft entry is `design/contract_compiler/overseer/entries/OVR-000467.json`,
validated in check mode against the schema and the document history, left
unsealed. The Overlord seals it.
