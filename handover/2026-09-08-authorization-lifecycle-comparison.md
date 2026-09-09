# Authorization lifecycle comparison

## Approved bounded slice

Luis approved comparing standalone Assent with the existing finite action
history before a production cutover. This continues the existing Assent
replacement item, not a new protocol or policy decision.

Role: `CONFORMANCE_FIXTURE` for the common subset of the optional action
authorization profile.

1. Claim: the two owning histories admit or refuse the same declared
   authorization scenarios, publish only the permitted decision/transition,
   preserve their prior accepted knowledge, and reconstruct that result.
2. Observation: three literal outcome cases and bounded mutations of decision
   identity, actor, assessment order, grant, interval, transition and sources.
   Refusals must preserve exact pre-append bytes and replay state. A refused
   append must not poison a subsequent valid append.
3. Reuse: the existing protocol and finite authorization-history builders,
   public owning append/replay boundaries and immutable prefix reuse. The
   finite builder uses its existing Shop bootstrap as unchanged scaffolding;
   the compared action and rules are neutral protocol specimens, not supplier
   business semantics. No Shop file is edited.
4. Exclude: a complete Assent replacement, expanded finite-profile coverage,
   new hash recipe, production policy changes, a second interpreter, effects,
   packaging, consumer integration and a release.

Both paths receive the same outcome pair and logical mutation, not identical
record or ledger bytes. Their concrete identities, timestamps, ontology and
bootstrap differ. Each evaluation hash remains exact within its own history;
agreement between shared calculators is not an independent hash oracle.

The finite profile still requires two monitors, one ACCEPT decision, no
relied-on claims, a grant for every verdict and bounded intervals. Broader
standalone forms stay outside this comparison. Existing literal control tests
already cover all nine outcome pairs; do not duplicate that Cartesian product.

## Test sequence

Freeze the small case table before writing the history comparison. Then run
both actual owning append paths and reopen each persisted history. This is
conformance-test work, not an assertion that production is currently broken.
Negative inputs discriminate semantic refusal from a successful append. A
deliberately wrong expected permission tests that the comparison cannot merely
report shared agreement. Record any actual divergence before changing runtime.

## Observed result

The literal table was frozen at
`ccd62578f5ed0da17dbc897ac180566c0ba8da37`. The executable comparison is
`52df279c2897006754f7b0c535d17adabccba23c`, tree
`619fddaea4362e2356e8725b4d9c8ad14d05198d`. It changes only the new test file.
No runtime, ontology, policy or dependency changed.

Both histories produce the expected AUTHORIZE, BLOCK and CLARIFY permissions.
Each append introduces only its decision and transition, preserves previous
objects and accepted knowledge, and reconstructs the same result on reopen.
Eight mutations refuse through each native gate, preserve exact ledger bytes
and replay state, and permit a subsequent valid retry. They cover a forged
evaluation hash, wrong actor, reordered assessments, wrong grant hash, an
authorization interval beyond its grant, wrong transition, missing action
source dependency and stale acceptance head. This does not claim identical
native refusal codes or an independent evaluation-hash oracle.

The bounded behavioral comparison passes only with each path's currently
accepted claim-list shape. **Record-shape equivalence fails.**

### Concrete incompatibility, no silent repair

`AuthorizationDecision.relied_on_claim_version_ids` is required in
[`assent.yaml`](../ontology/assent.yaml). Standalone
`OntologyRegistry._missing_required` treats an empty list as missing. Compiled
`ContractView.validate_instance` checks absence, null and empty string, but not
an empty list. The finite authorization program then explicitly constrains
this field to `maxItems=0`.

The new test passes the same exact empty-list decision to both validators:
compiled validation succeeds; standalone admission refuses it as missing a
required slot without changing ledger bytes. Positive standalone episodes
therefore retain their one relied-on claim; finite episodes retain none. The
test asserts that difference rather than erasing it during comparison.

Relevant mechanisms:

- [`OntologyRegistry`](../src/malleus/ontology.py), `_missing_required`.
- [`ContractView`](../src/malleus/_contract_pipeline/view.py), required-field
  validation.
- [Finite authorization schema](../research/action_history_contract_freeze/programs/authorization_bundle.py),
  `relied_on_claim_version_ids=strings(maxItems=0)`.

The pending operator decision is whether a supported authorization may rely on
zero separately identified claims. Then cardinality must be explicit in the
identified contract and interpreted consistently. This is not permission to
relax all required fields, edit retained histories or change a persisted
profile silently. Full Assent replacement remains unproven and unselected.

## Executed checks

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q --tb=short -p no:cacheprovider research/action_history_contract_freeze/programs/test_authorization_lifecycle_comparison.py
```

Result: **12 passed, zero skipped**, in 181.99 seconds. Ruff and Ruff format
checks pass for the new test. Three literal positives, eight mutation cases
and one divergence witness make the twelve cases. Each positive also checks
that a deliberately incorrect expected permission fails the comparison.

The first development run exposed the empty-list mismatch. A later failure
was in the new comparison adapter: the finite decision index is introduced
only by its first decision. The adapter now requires that index whenever any
decision exists and checks its membership against stored records. Neither
failure was repaired in production code. This is a test-first conformance
investigation, not a production RED/GREEN implementation or an independent
interpreter claim. Historical comparison and rule-artifact receipts remain
unchanged.

The existing neighboring gate also passed, **398 passed, zero skipped**:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/test_control.py research/action_history_contract_freeze/programs/test_authorization_conformance.py research/action_history_contract_freeze/programs/test_control_executor.py tests/test_protocol.py
```

These are bounded development checks against the unchanged runtime source
tree `63bc5650bda806b99fe8fb9fa060f2b8d0b113e2`. No full-repository, package,
cross-language or public release gate was run for this tests/docs slice.
