# Frozen Core program packet: consumer review

Date: 7 September 2026. Scope: Core `fdb497251550f2b54b1346ad4991c2117c8d6781`,
tree `9216afdf649e8bba4923983a5051c0e755b68556`. This is not a review of the
membership successor being implemented by Core. No Core file was edited.

Successor disposition: SV-1 is CLOSED at Core `7f2f850` after the independent
check recorded at the end of this file. The original finding and observations
below remain evidence about `fdb4972`, not a current unresolved defect.

Verdict: retained test report reproduced within the focused scope; one static
type-checking defect OPEN. Complete executable programs and the action runtime
remain unproved. Transaction choice is CLOSED. Luis's reported membership
approval supersedes this historical packet's pending-choice wording; it is
not reopened by this review.

Classification: CONFORMANCE_FIXTURE review under the proposed compiler-enabled
one-history action OPTIONAL_PROFILE. No base protocol or root-ontology claim.
Malleus development/review discipline keeps definition, implementation and
execution evidence separate. No root report, ontology, paper or runtime change.

## Verified scope and observations

All 14 files in the packet were read. The exact diff from `4cf8efe` adds only
the programs directory, 1699 lines. Report and its five listed file hashes match.
The independent checkout remained clean; aggregate whitespace checking passed.

The 55 program-directory tests pass independently, with zero failure/error/skip,
in `/private/tmp/malleus-reentry-program-audit.LaFkRA/repo`. The invocation used
the existing project interpreter, explicit Core configuration and runtime-origin,
clean-tree and exact-HEAD preflight. JUnit is the sibling `independent-focused.xml`.
The reported 214 combined passes and final RED were not rerun here. No tests
were changed, skipped or marked xfail to obtain the independent result.

The packet validates declarations, paths and basic types, not actual event
execution. Its interval contents and ordered invocation-reference checks are
useful bounded additions. It preserves the distinction between static monitor
dependencies, invocation role order and actual assessment input IDs. No lexical
implementation digest is presented as an available producer.

## SV-1. Positional array schemas can falsely pass scalar type checking

Where: `programs/packet_validator.py:103`, `:116` and `:133` at the exact Core pin.
`_schema` admits `prefixItems` but does not inspect or refuse its semantics.
`_path` then treats every guaranteed array index as the trailing `items` schema.
This is unsound for a positional prefix and contradicts the claimed declared
path/basic-type check. It is not merely missing runtime authentication.

Concrete schema: an array with `minItems: 1`, `prefixItems: [{type: integer}]`
and `items: {type: string}`. The actual value `[7]` passes the installed
Draft202012Validator. Index zero is an integer. Nevertheless, a STRING
REQUIRE_COMPARE on that index returns STATIC_VALID.

This diagnostic ran against the exact clean frozen checkout. Reproduce using
the existing configured interpreter, `PYTHONDONTWRITEBYTECODE=1` and
`PYTHONPATH=src:.`, with that checkout as the working directory:

```python
from jsonschema import Draft202012Validator
from research.action_history_contract_freeze.programs.test_packet_validator import (
    specimen, obj, operand, validate,
)

p = specimen()
binding = obj(value={
    "type": "array", "minItems": 1,
    "prefixItems": [{"type": "integer"}], "items": {"type": "string"},
})
Draft202012Validator(binding).validate({"value": [7]})
p["inputs"]["artifact"]["context"] = binding
p["inputs"]["event"]["literal"] = obj(value={"type": "string", "const": "AMEND"})
p["steps"] = [{
    "opcode": "REQUIRE_COMPARE",
    "left": operand("artifact", "context", "value", 0),
    "right": operand("event", "literal", "value"),
    "comparison": "EQ", "value_kind": "STRING", "refusal": "NOT_STRING_EQUAL",
}]
print(validate(p))
```

Observed: `{'status': 'STATIC_VALID', 'steps': 1, 'runtime_executed': False}`.
Required: typed refusal, either unsupported schema semantics or operand type.

Smallest requested Core repair: keep the static schema subset explicitly closed
and reject positional-array semantics it does not interpret. Do not expand the
language merely to accept this witness. Add a hard negative with the program
above, recursive/nested coverage for the same schema class, and a positive
homogeneous-array control. Check this preflight also protects the newly approved
STRING-list membership operand from a mixed positional schema. Preserve RED,
then bind the narrow guard and GREEN at a successor commit. The regression and
fix are Core-owned and remain OPEN here; the diagnostic is not a passing guard.

This finding proves no graph mutation, dispatch eligibility or action-runtime
bypass. No instruction ran. It prevents promoting a false static-valid result
into evidence that the program's operand types are sound.

## Remaining dependency-closed gate

Repair SV-1 and consume the separately verified membership successor. Then the
existing work order still requires full executable JSON event programs, their
cross-record/content/static closure, actual retained monitor dependencies and
input instances, and separately reviewed producer/interpreter implementation.
LIFECYCLE.md is an obligation map, not those complete programs. This review
adds no new scheduling choice, action capability or public contract request.

| Claim | Role | Evidence | Unsupported transfer | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| Frozen static test selection passes | CONFORMANCE_FIXTURE | 55 independent passes | None within that selection | PASS |
| Unsupported schemas cannot falsify operand typing | CONFORMANCE_FIXTURE | Prefix-items counterexample accepted | Static-valid does not ensure this claimed check | SV-1 OPEN |
| Membership semantics selected | OPTIONAL_PROFILE | Core relays explicit operator approval | Approval is not successor implementation evidence | ACCEPTED, successor not reviewed here |
| Complete action programs and runtime | OPTIONAL_PROFILE | Explicitly absent/unexecuted | Static tests cannot prove action execution | OPEN |

## Rechecked SHA-256

Paths are under Core research/action_history_contract_freeze/programs.

| File | SHA-256 |
| :--- | :--- |
| REPORT.md | 7685006a2a8a6e38cbbaf25b895d04cbf1fb6458aaa75aa6ae73b56a5e06d655 |
| packet_validator.py | 8539270f8fef0a8b95130241a9c6e8d1c27d87f74d265c72f89c64abd885a00b |
| LIFECYCLE.md | f7bac83c6f47f5ea9ff8a6b51c716c660bc53ef632d0064e1e260fe8fe12487a |
| MONITORS.md | d750c39506aa55718f5180211360e4b1d4b096612bc90b21df0c460e80898877 |
| NEXT_DECISION.md | dbce26a315b488412b4e9b74d6dd62c40ecf882cf9a5143147f1f885415dd464 |
| missing-membership.json | d86b6952cb9ca4586685a9948cac4f53ff7a2b3ba08790cd82deb89951be93af |

Independent JUnit SHA-256:
`d607c0c7763e751133eb16330b96748b35057a09ed8a66a76df708ae8cea1f19`.

## Successor verification: SV-1 closed

Core `7f2f850ff3eca10fc86edbe0a763761f90949344`, tree
`566b2e8a523aa3cc22da178b8c6462447a110b38`, was independently inspected in
`/private/tmp/malleus-reentry-membership-audit.VWv63e/repo` after the explicit
sharing approval. All 12 changed files/deltas from `fdb4972` were read. The
scope remains isolated action research only. Exact report and declared GREEN
hashes match; the clone and aggregate whitespace check remain clean.

The report's three-file membership/array/definition selector passes independently:
45 passed, zero failures, errors or skips. It uses the configured interpreter,
explicit Core configuration and exact-HEAD/runtime-origin/clean-tree preflight.
The 231 combined tests and preceding RED commits remain Core-reported; they
were not rerun here. The sibling `independent-focused.xml` has SHA-256
`0a36be7f811a18b6573721e4e23af58cedc8df73de87692554f134e9778c4ba8`.

The recursive `_schema` guard now refuses `prefixItems`. Hard tests cover the
exact index-zero integer witness, nested object and array declarations, the
mixed membership case, and a homogeneous-array positive control. SV-1 is
therefore CLOSED at this exact successor. No positional-schema interpretation
or runtime capability was added to fix it.

The approved five-field REQUIRE_MEMBER definition checks explicit STRING and
STRING-list operands and produces no result. Legacy REQUIRE_COMPARE/IN remains
refused. The retained membership value outcomes are still expectations for a
future interpreter, not executed checks. No new semantic defect was found in
this bounded delta review. Complete lifecycle programs and actual monitor/input
bindings remain outstanding. The runtime cut still requires separate authority.

Rechecked successor SHA-256:

| File | SHA-256 |
| :--- | :--- |
| programs/MEMBERSHIP_REPORT.md | 765338bfebf2db2143e5e282ec42687aebf9f1d02b26371f7e4400c597dfbd47 |
| instructions.schema.json | ba6b8b04626a4511de20b4b9c3202386a6128681efea70c59d0d8aaef4820b94 |
| programs/packet_validator.py | 55dd53ba75764a74477a24fccfecc27bcd2a943224e34beb6e96ddf5670cf504 |
| programs/MEMBERSHIP_DECISION.md | 358e0a4d5175b8c0bcc5baaadb34f6ce519eb1b9dd842f0c0c36f33aa8b349ae |
| programs/test_static_arrays.py | 65c200be41bc7a4a615b36b75069da816cc6091c6bd3ce1bf9f43f25d9d300f8 |
| programs/test_membership_definition.py | c47b838b635a8ae5c129fe47774c7841123507abeb2b30813f1f876eea541522 |
