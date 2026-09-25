# Baseline: what exists and what is missing

Inspected and exercised against `ebff70f7`. This is a bounded capability map,
not a full certification of either temporal implementation.

| Requirement | Existing mechanism | Observation or remaining gap |
|---|---|---|
| Preserve an earlier accepted graph | `KnowledgeHistoryReplay.graph_at_change` | Already works. The old 750-cent record remains retrievable after an 800-cent replacement. |
| Keep source time separate from ledger order | `KnowledgeValidTime`, source-assertion profile | Already represented. Capture import order is not domain time. |
| Preserve explicitly unstated time | `NONE_STATED` | Admission/replay do not invent a timestamp. This alone supplies no date-based applicability query. |
| Do not guess inside an uncertain transition window | `ValidTime` on the Assent path | Existing before/after/indeterminate behavior works; compiler history does not consume that richer shape. |
| Restore a complete earlier knowledge position | No public compiler-history selector before T2 | An old graph snapshot alone does not supply old retained evidence, contract and record history. T2 adds the exact prefix reader. |
| Correct the value for the same starting time | Existing instantaneous supersession forbids it | Refusal reproduced through Core-run checking, with no admission write. The new correction operation remains unimplemented. |
| Correct an already retired historical period | Existing supersession forbids a second replacement of that record | Distinct from a genuine version fork. Must be specified as correction, not bypassed by dropping the guard. |
| Select by domain time, not latest admitted version | Assent has a different accepted-graph path | Compiler current graph selects the latest accepted replacement, even when its declared start is in the future. It is not an as-of-domain-time view. |
| Determine whether a calculation's temporal premises changed | Consumer has exact premise/context identities | Temporal Core must expose the selected view and record identities; it must not infer execution, copy a hypothetical result or rewrite an old result. |

## Why a reason string is insufficient

The current supersession mechanism closes a prior version at the successor's
starting time. Calling that operation a correction in prose does not change
what the projector does. Allowing equal times would instead create a zero-length
old version, without saying which accepted historical interpretation it corrects.
The runtime needs an explicit, tested distinction between replacing our account
of a period and asserting the boundary of a new period.

## Scope of the test evidence

`test_temporal_history.py` uses an authored PriceState schema and exact retained
JSON source bytes through public compilation, history and Core-run admission.
It tests temporal mechanics, not extraction or source truth. The precision test
is the existing pure `ValidTime` mechanism, not its integration into compiler
history. The catalogue guard protects declared examples; it does not execute all
six desired situations. In particular, calculation and domain-time selection
remain future milestones.
