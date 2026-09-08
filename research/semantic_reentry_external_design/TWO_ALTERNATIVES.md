# Two valid amendments, explicit selection

Status: accepted bounded experiment, implementation not yet verified.
Base: local main `e2b9e77912f9b36fdbfe2fca310548a789bffb4d`.

## Bound slice

Claim: an aggregate goal may have two valid single-action translations. A
research-local Re-entry selector refuses ambiguity without a selection policy;
an explicit order preference selects one existing `SupplierOrderAmendment`
candidate. Selection gives no admission or execution authority. Observation,
ordinary KCS admission and replay remain necessary for acted satisfaction.

Smallest observation: accepted B/Y/1 and synthetic C/Y/1, goal at least three
committed Y units across exactly B and C. Both 1-to-2 amendments predict three.
REFUSE_IF_NOT_UNIQUE returns AMBIGUOUS and no candidate. ORDER_PREFERENCE with
the explicit order [B, C] returns B's candidate. One authorized B amendment,
independent source capture, ordinary KCS admission and replay yield B/Y/2,
C/Y/1 and quiescence. C and all unmentioned facts/history stay unchanged.

Reuse: existing compiled SupplierOrderState and SupplierOrderAmendment types,
RET-010 population, initial and observed supplier adapters, pure per-order
Re-entry synthesizer/model/strategy, accepted read view, action submission,
checks, authorization, controlled file effect, independent observer, KCS and
Core's public maintained reader. No accepted graph is constructed by a fixture.

Exclusions: Core or public API changes, new ontology terms, changes to locked
fixtures or earlier proof bytes, generalized planning, retries, simultaneous
actions, delivery or inventory claims, production supplier integration,
empirical synthesizer replacement, policy legitimacy, paper changes and
publication. Preference governs this producer, not every arbitrary caller of
the generic action-submission API. The ordinary authority policy remains a
separate boundary. The earlier maintained-reader follow-on remains separate.

## Roles and contracts

The selector and runnable composition are REFERENCE_IMPLEMENTATION under the
selected compiler-enabled state-version and experimental single-action
OPTIONAL_PROFILE. Without those profiles no composed accepted-state/action
guarantee is claimed. Aggregate scope, at-least-three predicate, preference,
one-attempt budget and preservation policy are ADOPTER_CHOICE. New C source,
explicit expected outputs and adversarial cases are CONFORMANCE_FIXTURE.
There is no new PROTOCOL_INVARIANT or public change identity.

The aggregate rule is a closed, canonical, retained SourceArtifact. It names
the exact two order alternatives, product, threshold, selection strategy,
evaluation/output/attempt budgets, stopping rule and implementation identity.
Each per-order original context binds it through its preservation source.
A local immutable Re-entry Contract binds that rule, the current seven Core
coordinates and the original contexts. Accepted lifecycle progress is read
from the same ledger. Rebinding at a new head is explicit and never rewrites
an applied original context.

The pure selector consumes only that contract, a graph-free AcceptedReadView
and explicitly selected child synthesizer, model and update strategy. It
produces existing ActionProposal bytes, or no candidate with a typed reason.
It performs no I/O, graph writes, retention, admission, dispatch or observation.
Unknown grammar, malformed/missing fields, stale coordinates, changed
implementation, unsupported operator, ambiguity and exhausted budget refuse.
Canonical alternative ordering is by explicit order ID, never a preference.
An explicit total preference may select among valid alternatives only.

Design dependencies:

```text
SupplierChoiceSynthesizer implements constrained aggregate GoalPredicate synthesis
SupplierChoiceSynthesizer consumes SupplierChoiceContract and AcceptedReadView
SupplierChoiceSynthesizer consumes explicit child synthesizer/model/strategy
SupplierChoiceSynthesizer produces existing SupplierOrderAmendment or refusal
SupplierChoiceContract governedBy retained aggregate rule and child contracts
SupplierChoiceSynthesizer conformsTo test_supplier_choice.py
Accepted supplier records derivedFrom ordinary observed-source KCS admission
```

Replacement criterion: another explicitly identified implementation must pass
the same conformance cases without changing downstream stages. This slice
does not supply one and claims no empirical replacement.

## Pre-action checklist

No server interaction or new endpoint is needed. Dependencies use the existing
declared Python project environment. Required data has no inferred defaults.
No existing mechanism is replaced. New failure classes require typed refusal,
atomicity checks and hard tests. Writes are confined to the isolated research
experiment and fresh controlled output directories. No merge or push.

## Verification plan

Freeze the input and independent outcome oracle, then capture failing tests
before implementing the selector. Test canonical round-trip, candidate-order
invariance, explicit preference, stale head, unsupported/missing contracts,
budget refusal, source/model/frame agreement, no graph/effect capability,
pending without reissue, initially satisfied no-op, observed-only acted
satisfaction, preserved complement and JSONL-only rebuild. Run focused tests
and the union of relevant existing supplier/public-reader gates. Audit the
base-to-head diff, immutable prior evidence and exact commit/tree/file hashes.
