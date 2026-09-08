# Supported observation, unsatisfied goal

Status: IMPLEMENTED and verified in an isolated branch. Base local main:
`f99c886f939db95a003f6d30d2e73d3f2a341020`.
Implementation commit: `aef6071479938e211e0103ad6a1b129a64ae96d6`, tree
`10fee0bfd5520a15b14d5958a88492fe93afe853`. No Core code, ontology, locked
fixture or paper changed. This follow-on has not been merged or pushed.

## Result

| Recorded or derived result | Observed value |
| :--- | :--- |
| Goal and proposed amendment | Exactly 2, from accepted 1 |
| Execution receipt | SUCCEEDED |
| Independent source capture | Actual B/Y/3 at reentry-amendment-1 |
| Observation against the action goal | CONTRADICTED |
| Accepted quantity after ordinary KCS admission | 3 |
| Fresh episode result | REFUSED / GOAL_UNSATISFIED |
| New candidates / total dispatch attempts | 0 / 1 |

The shortfall is zero, but the exact-two goal remains unsatisfied. The same
result survives JSONL-only reopen and repeated evaluation without a model,
effect, or new write. A separate corrupted-binding case admits the supported
quantity-three fact but refuses episode closure with EVIDENCE_DISAGREEMENT.
A false CONFIRMED observer judgment over captured 3 refuses preparation
before new retention. These are distinct tested boundaries.

Validation: one component RED and three selected E2E/model RED failures;
117 focused tests passed; the unified relevant selection has 435 passes and
one existing optional-private-doctrine skip. Its three disjoint groups account
for all 436 collected cases, with no omitted, extra or duplicate case. All
seven lifecycle histories match byte-for-byte between focused and unified runs.
An additional read-only process used production modules, not test helpers,
to reopen and evaluate the two quantity-three accepted histories.

The exact selections, hashes and temporary evidence paths are in
[observed-mismatch-result.json](observed-mismatch-result.json). Historical
receipts remain unchanged. These are configured-environment scoped runs, not
full repository CI, a clean-install claim or a new released capability.

Run the unified gate from the configured checkout. This allocates a fresh
temporary directory and uses only the declared Python test environment:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. python -c '
import json
from pathlib import Path
import tempfile
import pytest
run = Path(tempfile.mkdtemp(prefix="malleus-observed-mismatch-"))
gate = json.loads(Path("research/semantic_reentry_external_design/observed-mismatch-gate.json").read_bytes())
print(run, flush=True)
raise SystemExit(pytest.main([
    "-q", "-p", "no:cacheprovider",
    "--basetemp=" + str(run / "pytest"),
    "--junitxml=" + str(run / "junit.xml"),
    *gate["tests"],
]))'
```

The retained run split that same selection into groups [0,1,2,7,17],
[3,4,5,6,8,9,10], and [11,12,13,14,15,16,18,19,20], each with its own
temporary root and JUnit file. The ledger-only replay oracle is unchanged.

## Claim, observation, reuse, exclusions

Claim: an observed source can justify an ordinary accepted KCS even when it
contradicts the desired result of the action. Observation support and goal
satisfaction are different predicates. Neither a successful receipt nor zero
shortfall establishes satisfaction of an exact-equality goal.

Smallest observation: accepted B/Y/1, goal exactly 2, one synthesized and
authorized one-to-two amendment, a controlled write perturbation leaving
actual B/Y/3, independent CONTRADICTED observation, ordinary admission of 3,
JSONL-only reopen, and fresh evaluation refusing further action because this
one-attempt episode did not satisfy its goal. No automatic retry occurs.

Reuse the existing public Core source, action, observation, population, KCS,
admission and replay seams. Reuse the existing episode, IDs, complement and
test harness. Do not change locked fixture bytes or use the quantity-two
oracle as the source of the new observed fact. The perturbation is explicitly
a conformance intervention at the controlled file write, not a second executor
implementation, a second action, or evidence of production supplier behavior.

Exclude general correction, new operator semantics, arbitrary observed
quantities, retries, planners, public APIs, ontology changes, database or
projector work, paper changes, and production effects. The maintained-KG
request is separately assigned to Core's backlog.

## Roles and boundaries

The changed mapper and episode evaluator are REFERENCE_IMPLEMENTATION under
the selected compiler-enabled state-version and experimental single-action
OPTIONAL_PROFILE. Without those profiles no composed admission/action/replay
guarantee is claimed. Exact-two goal, supported replacements of 1 by 2 or 3,
unchanged source frame and one-attempt stopping are ADOPTER_CHOICE. The
perturbation and expected outcomes are CONFORMANCE_FIXTURE, not Core policy.

The observed-source adapter advances to research-v2, with its exact source
bytes and component bytes still bound by the existing retained identity. Its
bounded accepted input now includes integer quantity 3 at the declared new
occurrence, on the same order and product, with the same explicit supersession.
It must preserve the observed quantity, never normalize it to the requested 2.
Other changes and malformed inputs still refuse before population retention.
The model and action grammar remain strictly 1 to 2. A model predicting 3 is
not licensed by the observation mapper's wider support.

Preparation verifies the observation's result against the mapped quantity and
the exact goal, separately from whether a KCS can be prepared. CONTRADICTED is
not INDETERMINATE. The unchanged source still produces no KCS. The episode
verifies the accepted source and observation closure before classifying a
quantity-three replacement as REFUSED / GOAL_UNSATISFIED, with no candidate.
Bad higher-level closure still refuses EVIDENCE_DISAGREEMENT even when Core
properly admitted the actual observed fact.

Dependency tuples:

- Observed mapper consumes captured source, original context and explicit mapping.
- Observed mapper produces existing population-plan fields and ordinary KCS preparation.
- Core admission consumes the sole KnowledgeChangeSet identity.
- Replay derives the accepted quantity and retained provenance.
- Episode evaluation consumes that accepted state and the bound observation closure.
- Episode evaluation is governed by the exact goal and one-attempt rule.

## Mechanical gate

Before code: no server interaction, endpoint, new dependency, Core mechanism,
or required-data default. Changed behavior stays in the existing adopter
adapter; there is no fallback to the old mapper or second change identity.

RED then GREEN: pure mapping of supported 3; refusal of other quantities and
source-frame changes; strict model goal agreement; actual capture/admission of
3 with preserved complement and trace; stale preparation refusal; no closure
from candidate retention alone; no retry after reopen; and corrupted binding
refusal on the undesired-result path. Retain the original evidence files.
The new unified gate must bind this current Core source epoch separately from
the historical proof's pinned epoch, not relabel historical runs as fresh.
