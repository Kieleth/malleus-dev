# G1 specimen format, draft 1

One JSON file per specimen, named `g1-*.json`, tagged
`"schema": "malleus.temporal-g1-specimen/draft-1"`. The format describes logical
meaning only. It prescribes no nodes, tables, property layout or Core API.
`validate_specimens.py` enforces everything below; where this text and the
validator disagree, report it rather than choosing one.

Role: `CONFORMANCE_FIXTURE` candidates under an `OPTIONAL_PROFILE`. The names
below are draft test vocabulary, not Core enums or wire.

## Conventions an encoder must follow

- **References.** A key named `ref`, or ending in `_ref`, holds one id (or null).
  A key ending in `_refs` holds a list of ids. Every reference resolves to an id
  in the same file. No other key holds an id.
- **Ids** are unique across objects, rejected objects, derived labels, queries,
  refusals and open choices. Positions are a separate namespace.
- **Typed literals** are `{"datatype", "lexical", "unit"?}`. `lexical` is always a
  string and must round-trip exactly: `"5.40"` is not `"5.4"`, `"0750"` as
  `xsd:string` is not a number. Datatypes: `xsd:integer`, `xsd:decimal`,
  `xsd:string`, `xsd:boolean`, `xsd:dateTime`, `enum`.
- **Times** are UTC instants `YYYY-MM-DDTHH:MM:SSZ`. Intervals include the start
  and exclude the end.
- **Applicability** is exactly one of `{"kind":"INTERVAL","from","until"}` (`until`
  null means no known end in that account, never unknown time),
  `{"kind":"INSTANT","instant"}`, or `{"kind":"NONE_STATED"}` (no domain time was
  stated; not forever, not acceptance time).
- **Positions** (`at`, `position`, `head`, `base`, `head_after`, `selection_at`,
  `knowledge_from`, `knowledge_until`) name completed accepted checkpoints of this
  specimen. They are labels, not hashes, and have no clock meaning.

## Top level

| Key | Meaning |
|---|---|
| `specimen_id` | Unique across the directory |
| `obligation` | Non-empty list from the eleven codes in README.md |
| `origin` | `flows` (GE-nn), `basis` (`SYNTHETIC`, `EXISTING_SYNTHETIC_EXAMPLE`, `REAL_SOURCE_POINTER`), `note`, optional `pointers` |
| `objects` | Logical objects that become accepted |
| `changes` | Ordered accepted changes; the order is the knowledge order |
| `queries` | Reads with exact expected answers |
| `forbidden` | Answers a lossy design would give |
| `refusals` | Write attempts that must be refused |
| `open_choices` | Undecided policy, with per-branch answers |
| `reused_files` | Optional. `{path, sha256}` of an answer key reused here, relative to the specimen |
| `derived_labels` | Optional. Labels for derived versions defined in a reused file (the price cells a1, a2, b, c) |
| `rejected_objects` | Optional. Objects only ever attempted, never accepted |
| `phantom_ids` | Optional. Ids deliberately never defined; only rejected objects may use them |

## Objects

Every object has `id`, `type`, optional `note` and optional `contract_ref`.

| Type | Required fields | Optional |
|---|---|---|
| `SUBJECT` | `label` | |
| `ACCOUNT` | `label` | |
| `SOURCE` | `source_kind` (`SYNTHETIC_TEXT`, `RETAINED_DECLARATION`, `REAL_BLOCK_POINTER`), `text` | `locator`, `pointer` |
| `CONTRACT` | `version`, `identity` | |
| `ASSERTION` | `subject_ref`, `property`, `value`, `basis`, `applicability`, `evidence_refs` | `qualifiers`, `account_ref`, `corrects_ref`, `revises_ref` |
| `RELATION` | `relation_type`, `from_ref`, `to_ref` (directed) | `qualifiers`, `basis`, `evidence_refs` |
| `GROUP` | `group_kind`, `member_refs` | `evidence_refs` |
| `ARGUMENT` | `premise_refs`, `conclusion_ref` | `evidence_refs` |
| `CONTEXT` | `context_kind`, `bindings` | `model_ref`, `basis_refs` |
| `MODEL` | `version`, `implementation`, `formula`, `parameters` | `member_refs` |
| `EXECUTION` | `model_ref`, `input_bindings` | `context_ref`, `implementation` |
| `RESULT` | `execution_ref`, `value` | |
| `RULE` | `semantics`, `scope_refs`, `assumptions` | |
| `PLAN` | `subject_ref`, `action`, `planned_for`, `evidence_refs` | |

`basis` is `REPORTED`, `ASSUMPTION`, `CORRECTION` or `INTERPRETATION`. A
`CORRECTION` names what it corrects in `corrects_ref`. `REPORTED` and
`CORRECTION` need at least one evidence reference. `subject_ref` may name any
object, so an assessment can be about a relation. `qualifiers` map names to typed
literals. A binding is `{parameter, assertion_ref, selection?}`; a `selection`
records the coordinates used to choose the premise: `{at, valid_at?, account_ref?}`.

## Changes

`{position, kind, adds_refs, target_refs?, note?}`. The first change is
`GENESIS` with no additions (the empty completed genesis). Every object is added
by exactly one change. An object may only reference objects added at or before
its own position. `target_refs` names earlier objects whose account the change
modifies. Kinds: `GENESIS`, `REPORT`, `TRANSITION`, `CORRECTION`, `ASSUMPTION`,
`INTERPRETATION`, `REASSESSMENT`, `ARGUMENT`, `MODEL_DEFINITION`,
`CONTEXT_BINDING`, `EXECUTION_RECORD`, `RULE_DECLARATION`, `PLAN`,
`CONTRACT_DECLARATION`.

A transition asserts a new world state and ends the targeted period. A
correction replaces our account of the targeted period and asserts no world
change. The kind is declared input, never inferred.

## Queries

`{id, kind, inputs, expected, expected_from?, open_choice_ref?, note?}`.

Kinds: `SELECT_APPLICABLE` (value applicable at a domain time), `SELECT_ACCOUNT`
(current accepted account, no domain time), `INSPECT_HISTORY` (all qualified
versions visible at a position), `EXACT_LOOKUP` (one identified object, selected
or not), `RESULT_FOR_CONTEXT`, `RESULT_FOR_SELECTION`, `EXPLAIN_EXECUTION`,
`COMPARE_PREMISES`, `PREPARE_INPUTS`.

Inputs: `at` is required. Others as the query needs: `valid_at`, `subject_ref`,
`property`, `account_ref`, `context_ref`, `target_ref`, `execution_ref`,
`model_ref`, `premise_refs`, `same_time`, `persistence_rule_ref`,
`withheld_refs` (retained objects made unavailable before a rebuild) and
`after_refusal_ref` (read after that refused attempt). An absent or null input
means the caller did not supply it. No ambient "now" or "latest" fills it.

Expected answer states:

| Group | States |
|---|---|
| Selection | `SELECTED`, `NO_ACCEPTED_ACCOUNT`, `NO_APPLICABLE_ACCOUNT`, `UNRESOLVED_APPLICABILITY`, `AMBIGUOUS_SELECTION` |
| Inspection | `QUALIFIED_HISTORY`, `EXACT_OBJECT` |
| Computation | `COMPUTED`, `NOT_COMPUTED` |
| Premises | `ORIGINAL_PREMISES_PRESERVED`, `SELECTED_PREMISES_CHANGED`, `SAME_PREMISES`, `DIFFERENT_PREMISES`, `NO_COMMON_APPLICABILITY`, `UNRESOLVED_REQUIRED_PREMISE`, `INPUTS_READY`, `INCOMPATIBLE_CONTEXTS` |
| Closure | `INCOMPLETE_RECONSTRUCTION` |

`NO_ACCEPTED_ACCOUNT`: nothing accepted answers the question. `NO_APPLICABLE_ACCOUNT`:
accounts exist but none covers that time. `UNRESOLVED_APPLICABILITY`: an account
exists but its applicability at that time is not established.

Other expected keys: `selected_refs`, `unresolved_refs`, `candidate_refs`,
`derived_from_refs`, `value`, `basis`, `applicability`, `qualifiers`,
`evidence_refs`, `visible_refs`, `absent_refs`, `metadata`, `premise_refs`,
`cell_refs`, `selection_at`, `model_ref`, `result_ref`, `previous_refs`,
`new_refs`, `new_cell_refs`, `conflict_refs`, `missing_refs`, `domain_time`.
List-valued refs compare as sets. `metadata` is a
list of `{ref, field: value}` rows; only the fields listed are asserted. An
expected answer may not name an object added after its `at`, nor a derived
label whose `knowledge_from` is after `at`.

`expected_from` points into a reused file as `path#/json/pointer`. The copied
fields must equal the source; the validator compares them.

When the answer depends on an open choice, `expected` is null and
`open_choice_ref` names the choice, which gives one answer per branch.

## Refusals, forbidden answers, open choices

A refusal is `{id, head, base?, operation, would_add_refs, target_refs?,
category, head_after}`. `would_add_refs` names rejected objects. `head_after`
must equal `head`: nothing from a refused change is accepted, including its
valid parts. Categories: `STALE_BASE`, `STALE_TARGET`, `MISSING_EVIDENCE`,
`MISSING_MODEL`, `MISSING_CONTRACT`, `UNKNOWN_REFERENCE`,
`UNSUPPORTED_SEMANTICS`, `PREMISE_MISMATCH`. These are outcome categories, not
Core refusal names.

A forbidden entry is `{query_ref, answer, why}`. `answer` is a partial answer:
the design fails if its real answer matches every listed field. It may not
match the expected answer, nor any branch answer.

An open choice is `{id, question, affects_query_refs, branches}` with at least
two branches, each `{label, expected, note?}`. `expected` maps every affected
query to its answer under that branch, or is null when no query is affected.

## Obligations that apply to every specimen

- **Round trip.** Encoding then decoding returns every object with the same id,
  type, typed literals, qualifiers, relation direction and group membership.
- **Rebuild.** Every query holds unchanged when the store is rebuilt from the
  ordered accepted changes alone. Derived labels are expected outputs, never
  encoder inputs.
- **Queries write nothing.**
