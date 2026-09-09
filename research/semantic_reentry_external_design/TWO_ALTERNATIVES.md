# Two valid amendments, explicit selection

Status: bounded slice and authorization compatibility verified; Core owns local landing.
Original base: local main `e2b9e77912f9b36fdbfe2fca310548a789bffb4d`.
Original landing base: local main `55c038438ed67197b7e3345b9c80a885a7b6cf17`.
Current authorization base: `a0026cbd25a90b5c2b6c9eb7b31df4e42df16804`.

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
separate boundary. Core integrated the earlier maintained-reader follow-on
during this experiment. The final landing candidate consumes that exact
integration without changing its source or historical evidence.

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

## Exact Shop mapping

The original supplier fixture and RET-010 source/mapping path are unchanged.
B/Y/1 is the accepted `supplier-order-state:B:e4` from the existing retained
initial source. The extension adds C/Y/1 at
`supplier-order-state:C:choice-C-initial-1`, from the new explicit source row
in `fixtures/supplier_choice_v1/input/supplier-C.jsonl`. It uses the existing
SupplierOrderState type and ordinary initial-source population/admission.

The aggregate predicate scopes exactly B and C, product Y, and requires their
committed quantities to sum to at least three. It is contract-local input,
not a customer-demand fact and not a statement about delivered inventory.
Each child proposal still uses the existing exact 1-to-2 amendment contract.
B predicts occurrence `reentry-amendment-1`; C predicts
`choice-C-amendment-1`. The runnable effect path selects B. Its independently
captured replacement supersedes e4 through the ordinary observed-source KCS.
C's alternative is also tested through real proposal submission, not through
a second effect execution.

Candidate summaries expose only order IDs and modeled totals. They contain no
ActionProposal bytes. REFUSE_IF_NOT_UNIQUE emits no candidate; ORDER_PREFERENCE
emits exactly the selected existing candidate. The evaluation budget counts
both modeled alternatives, while the output budget permits only one result.
Both rules are retained before evaluating either, with different immutable
identities and preservation-source dependencies. This is not a policy change
after proposal or authorization.

The full episode reuses one public KnowledgeHistoryProjection reader across
its ledger appends. The context factory still performs full replay and the
accepted-read freezer validates a reconstructed graph. This is a maintained
reader consumer, not an end-to-end incremental-performance claim.

Supported acted closure remains the existing child action's linked observed
two-unit replacement. General observed quantities and translating a child's
exact-amendment failure into aggregate goal satisfaction are outside this
experiment. Those must not be inferred from the at-least predicate.

## Defects found during implementation

The first result carrier exposed unselected proposal bytes inside ambiguity
diagnostics. A RED test detected that field; the carrier now permits only
order ID and predicted total. Only the selected candidate leaves the selector.

A controlled model RuntimeError escaped the new composition. A behavioral RED
test confirmed it. The selected-engine boundary now returns ENGINE_FAILURE
with no candidate and does not silently try the other order. Ordinary typed
child refusals keep their reasons. The final focused and regression results
are recorded below.

The first broad regression selection included the original frozen epoch guard.
It correctly refused current Core source tree 3b4fd1c9 rather than silently
accepting it as the older 763d3b72 epoch. The new gate selection was wrong.
The historical test and evidence remain unchanged. A behavioral RED test now
catches either direct inclusion of that old guard or implicit inclusion via
its whole module. The current gate selects the other two replay laws by name,
verifies actual Core source and import location, rejects older/unknown epochs,
and hashes the frozen prior evidence. The historical refusal remains recorded
separately. All six current epoch/selection guard tests pass.

Final review found that a correctly typed child result could still name the
wrong contract or carry an invalid status, empty reason or malformed candidate
shape. Five behavioral RED cases reproduce this after a real proposal
submission. The shared child-result boundary now validates those fields before
any fresh, pending or terminal branch consumes the result. All five cases pass.

## Run the bounded demonstration

From this checkout in its configured Python environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -m research.semantic_reentry_external_design.supplier_choice_walkthrough /tmp/malleus-two-order-example
```

The output directory must not exist. Only that new directory is written.
An interrupted or refused run preserves its partial files and does not retry.
Dependencies and the dev test environment are the existing root pyproject
configuration; no additional installation or service is required.

`choice-result.json` reports measured outcomes only after the whole episode
passes. `choice-contract.json` and `action-proposal.json` expose the exact
selected inputs and proposal. `history.jsonl` is the sole accepted-state
authority and retains the sources, both selection rules, actual protocol
events, observation and KCS. The other files are inspection copies.

The protocol uses the original fixed September 8 fixture timestamps. They are
reproducible coordinates, not measurements of when this command ran.
The result is a controlled supplier-record amendment, not physical delivery,
customer-order fulfilment or production supplier integration.

## Original verification and landing evidence

The original landing-base union has **485 passed, one existing optional skip**:
40 focused/epoch cases, 112 supplier cases, 193 component cases, and 140 passes
plus one skip in the action/observation/reader group. The focused group includes
33 new cases and seven inherited epoch checks. The skip concerns private paper
doctrine absent from this checkout, not a Re-entry boundary.

The JUnit union matches all 486 collected case identities exactly, with no
missing, extra or duplicate cases. Its identity comparison preserves parameter
text containing `::`, slashes or nested brackets and checks four adversarial
normalization examples first. This corrected an audit-only parsing mistake;
it did not change or waive any test result.

The final focused run uses implementation commit
`e733438aeff3e3f0e1f69df65566248a28f96d9a`. The three regression groups ran at
`7c1accc7442e2f8b763c12aa025bae5061c7326c`; their code and inputs are unchanged
by the final selector/result-test fix. The earlier starting-base union is
separate evidence: 466 passed and the same optional skip. Neither union claims
full repository CI.

The standalone run and final E2E test produce identical bytes for the ledger,
contract, proposal, report and two source files. There are 91 ledger events and
one dispatch. A separate process reopens each of the three terminal histories,
then reevaluates without model, effect, history-replay or admission calls and
without further ledger writes. A failed receipt after an actual write still
allows the observed two-unit KCS. A successful receipt without a write leaves
B/Y/1 and C/Y/1 accepted and refuses another attempt.

The [completion receipt](supplier-choice-result.json) records exact tested
commit/tree coordinates, source and artifact hashes, gate groups, raw result
locations, RED evidence, historical refusal and landing order. Root ontology
rites were not run because no root ontology change is in scope. Scope review
applies `protocol_role_is_explicit`, `optional_profile_stays_optional`,
`single_ledger_knowledge_change`, `fail_closed` and `evidence_does_not_transfer`:
the roles and limits above remain explicit, the selector has no write owner,
and observed KCS admission is the only acted path to accepted domain change.
Composition is measured; replacement and general planning remain unproved.

All additions are isolated research files. Core runtime, ontology, locked
fixtures, prior evidence, dependencies, skills and paper work are unchanged.
Core owns the coordinated local landing. The original proof did not merge to
main, push or publish. The operator subsequently authorized local integration.

## Authorization compatibility and local integration

Core subsequently moved authorization outcome rules into an exact pinned data
artifact. This follow-on checks the unchanged two-order implementation against
that completed Core source, rather than treating the older proof as evidence
about an untested version. No selector, action, mapper, observer, source fixture,
public API or ontology change is part of this compatibility update.

The current `supplier-choice-gate.json` selects the supplier/Re-entry regression
suite plus Core's authorization, finite-control and independent expectation
tests. Earlier runtime-identity tests and receipts remain byte-identical and
bound to their historical versions. Their positive identity checks correctly
refuse newer source. Current verification uses its own exact source pin and
still runs the applicable historical negative checks. Five new failing tests
first exposed stale-source acceptance and accidental inclusion of old positive
identity checks; the current guard now rejects both classes.

Run every selector in the current manifest from the configured environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -c 'import json, pytest; from pathlib import Path; gate = json.loads(Path("research/semantic_reentry_external_design/supplier-choice-gate.json").read_bytes()); selectors = [s for group in gate["groups"].values() for s in group]; raise SystemExit(pytest.main(["-q", "-p", "no:cacheprovider", *selectors]))'
```

The compatibility union has **649 passed and one existing optional skip**:
204 focused/authorization cases, 305 supplier/component cases, and 140 passes
plus the private-paper-doctrine skip in the action/observation/reader group.
All 650 collected case identities match the three JUnit reports exactly, with
no missing, extra or duplicate case. All runtime and test bytes were those of
`d9b47923d665b4b0605ef904b25f64e593812dac`; only this documentation was edited
while the suites ran. This is the selected relevant gate, not full repository CI.

The new full episode reproduces the earlier standalone demonstration byte for
byte across its ledger, contract, proposal, result and both source files. It
still has 91 ledger events, one dispatch, accepted B/Y/1 and C/Y/1 until observed
admission, then B/Y/2 and C/Y/1 with no further candidate. Success without a
source change and failure after a real change remain separately tested.

The [authorization compatibility receipt](supplier-choice-authorization-result.json)
binds the tested snapshot, raw reports, five RED failures, historical version
refusals, source and file hashes, and the unchanged original proof receipt.
Core's later `ed4d26da4187283e2c82c9de77779c0512140feb` commit adds only separate
Shop expectations and Core preparation/journal work relative to the tested
authorization base. The runtime and consumed supplier dependencies were checked
unchanged. Any subsequent runtime change needs its own compatibility evidence.

The operator authorized reviewed local integration, which Core coordinates at
a committed boundary. This does not authorize a push, package release or
production supplier connection, and does not attest unfinished Core edits.
