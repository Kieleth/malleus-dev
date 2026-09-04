# Core population piece 6: explicit domain-history profiles

Status: implemented in Core, awaiting independent overseer verification.

## Coordinates

- Initial RED: `7b7eddbbbc236efb0853d0cf4e950a212e8d6601`
- Origin correction RED: `5ef011d83da30322b289f7a53c939cbb4fa1112a`
- Capture-batch semantics RED: `d79d3d70fa2799a6d8e88b11053008f9ac94adaa`
- GREEN: `7ad5b486e901902088e1a6872b790c6ec48d01a5`
- GREEN tree: `d4ea8f6a334a728bac01ab871f6932e839b2ba7a`

## What changed

`DomainHistoryProfile` is now a closed, immutable, content-addressed contract.
It declares one adopter's history origin and genesis boundary, completeness
scope, semantic unit, time semantics, change semantics, ontology-role roots,
projection-rule family, and grounding. Population plans retain and bind its
exact canonical bytes. The previous five-field `private-v0` profile is refused;
there is no fallback.

Core ships three profiles as data files:

| Profile | Artifact | Canonical identity |
| --- | --- | --- |
| Source assertion | `src/malleus/profiles/source-assertion.json` | `sha256:2317d88fd236fb63d5f4b68262619de6b5874946ab2ea8144b1b9a2995f471d5` |
| State version | `src/malleus/profiles/state-version.json` | `sha256:b18f3129942761e03ce754af6cec8c689c94b91468aa105a423f5b27ddf20dc3` |
| Object event | `src/malleus/profiles/object-event.json` | `sha256:38bb0e408d28d8785c6a85f92d4a833b68a18fac1371490de3587c1179780e78` |

`malleus.compiler` publicly exports `DomainHistoryProfile`,
`SOURCE_ASSERTION_PROFILE`, `STATE_VERSION_PROFILE`, and
`OBJECT_EVENT_PROFILE`.

## Source-assertion rule

One capture is one atomic partial-import batch. It is not a complete-world
snapshot, and it is not split into one change set per assertion. The exact
profile choices are:

- origin `PARTIAL_IMPORT`;
- genesis boundary `RETAINED_PARTIAL_IMPORT`;
- completeness `DECLARED_CAPTURE_ONLY`;
- semantic unit `COMPOSITION`;
- change-set valid time `CAPTURE_IMPORT_ORDER`, represented as `ORDER_ONLY`
  with the exact capture ID as its value;
- assertion and domain time `RETAINED_ASSERTION_EVIDENCE`;
- projection family
  `CURRENT_NON_SUPERSEDED_RECORDS_WITH_RETAINED_ASSERTION_TRACE`.

This resolves captures containing assertions with different domain times or no
stated domain time. The adapter derives this value and no longer accepts a
caller-supplied `valid_time`, so a source date cannot masquerade as the whole
batch's time. Ledger order supplies the ordering. The public trace reaches each
retained assertion, including its modality and optional `assertion_time` and
`domain_time` strings. These strings are exact lexical evidence, not normalized
Core time values; absence remains absence. An ordinary graph query may still
show an unqualified domain edge, so the edge alone is not evidence that the
source asserted it as fact.

## Small Shop rule

All five public Small Shop plans now bind the shipped `state-version` profile.
It starts from an empty accepted graph, limits completeness to declared
sources, treats one record as one state version, uses domain valid time, and
projects current non-superseded records. A fresh run still admits five change
sets around one additive contract revision, reopens nine current records,
retains ten historical records, and traces every record to its source and
mapping bytes.

The regenerated exact outputs are:

- history JSONL SHA-256:
  `a19a946e85ff00cae23fd91f93b19364de2bc5fba9d183e036b246eb5370fa52`;
- evidence JSON SHA-256:
  `c8dd95737ad907cc787cea623f0b7a5400b607fe9c30e7f7c900720372fd5567`.

## Mechanical evidence

- Profile, document-adapter, public-trace, public-compiler, and public Small
  Shop focused tests pass: 46 tests.
- The complete contract-compiler Pareto suite plus the public Small Shop run
  passes: 336 tests.
- Every Small Shop research test passes: 194 tests.
- Tests reject the old grammar, extra or missing fields, invalid origin/genesis
  pairs, unknown origins and units, unordered or duplicate role roots, and
  ungrounded profiles.
- One HYPOTHESISED assertion is admitted as an unqualified domain relation, then
  traced back to its exact retained modality. This mechanically guards the
  selected provenance-join boundary.
- Separate tests prove that callers cannot supply batch valid time, two
  assertions retain different assertion and domain times, a third retains no
  domain time, malformed time values refuse, and public replay trace returns
  the exact evidence.
- The shipped JSON files, not Python constants, own the three profile choices.

## Non-claims

This does not make one history model mandatory for Malleus. It does not infer a
profile from an ontology, interpret arbitrary projection programs, make Event
population executable, reify claims, define a stable wire grammar, or add a
mapping language. The object-event profile is declarative until a later Event
materialization contract lands. The source-assertion profile keeps modality and
per-assertion time in retained evidence, not necessarily in ordinary graph
records. Small Shop proves one state-version choice, not a universal domain
history.
