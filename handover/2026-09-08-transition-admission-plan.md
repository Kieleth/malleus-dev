# Transition admission: implementation preparation

Status: **accepted direction, prepared for contract freeze; not implemented**.
Luis accepted the [revised design](2026-09-08-history-profile-enforcement.md):
"Correct, this is better, add to journal and prepare to implement."
This records preparation within the existing Core runtime workstream, not a
new protocol decision, workstream activation or shipped capability.

## What we will prove

When an adopter explicitly selects a deterministic transition restriction,
the owning history enforces it before committing a change and when replaying
that history. Skipping population preparation or supplying a successful check
event cannot bypass it. The selected rule contains the domain decision;
Python supplies generic execution.

Lowest affected scope: an `OPTIONAL_PROFILE` of compiler-bound semantic
history. Core supplies its bounded `REFERENCE_IMPLEMENTATION`. The chosen
domain-role restriction is `ADOPTER_CHOICE`; neutral tests and the separate
Shop witness are `CONFORMANCE_FIXTURE`. Without the restriction, the existing
structural profile makes no promise about adopter-selected replacement roles.

Smallest falsifier: a selected state-only replacement rule admits a replacement
of a record outside that role. The current public witness does this. Its
profile label is retained text, not an existing executable restriction.

Reuse the existing KCS, compiled contract, domain-history profile, normative
admission profile, machine/policy artifacts, atomic history and common replay
fold. The [foundation design, section 4.2](../design/PROTOCOL_FOUNDATION_GRAPH.md)
already owns this admission role. Do not create a replacement-specific type
list alongside the adopter's authoritative role mapping.

## Boundary to freeze before RED

The missing input is a pure, read-only transition view, derived by Core from
verified history. Its minimal contents are:

- Exact KCS identity and replacement operations in declared operation order.
- Full base ledger head/count, acceptance and materialization heads, and base
  state digest, all checked by the owning history.
- Prior active record IDs, operation families and exact types, resolved from
  owning replay rather than supplied as caller assertions.
- Exact compiled contract and selected history-profile identities, together
  with the rule/program identity that interprets them.

This view is neither a new change identity nor a second graph or persisted
ledger. It needs no whole-graph copy for the first restriction. Future inputs
must be declared when a real rule needs them.

The pure guard produces a deterministic pass or typed refusal with offending
operation references. It neither appends events nor mutates accepted state.
The existing admission path owns persistence. Refusal preserves the exact
bytes at the admission boundary; earlier successful preparation is a separate
transaction and is not silently undone.

Three encoding details remain to be settled and reviewed together before RED:

1. The smallest bounded instruction or declared pure capability in the owning
   machine, and its exact input/result schema. No arbitrary callback, new DSL,
   replacement service or second admission executor.
2. How the selected admission profile binds the retained history-profile role
   references and rule. Resolve every required type against the compiled
   contract. Make exact-type versus subtype matching explicit. Existing
   descriptive strings do not acquire executable meaning retroactively.
3. Exact grammar/capability version, typed refusal names and deterministic
   diagnostic order. Unknown, missing, mismatched or stale required inputs
   refuse. Reopen consumes the retained selection, not a current default.

These are unfinished contract details, not implicit authorization to invent
public names. The current machine rejects nonempty capability references;
opening that boundary requires this narrow contract, not a permissive parser.
The separate finite action interpreter and graph-only Prolog interface are
reuse evidence, not alternate KCS admission authorities.

## Dependency sequence and TDD

| Step | Deliverable and completion evidence |
|---|---|
| Freeze | Exact input, rule binding, version and refusal contract above. Literal expected outcomes written independently of the evaluator. No runtime edit. |
| RED | Tests through the owning history demonstrating the missing restriction and bypass protection, with exact command and failure output committed before production changes. Existing controls need not fail. |
| GREEN | Minimal generic transition lookup and rule execution, invoked by the common owning admission/replay fold. No domain type names or duplicated type allowlist in Python. |
| Integration | Full replay, maintained incremental replay and reopen agree; selected rule and input provenance survive retention. Run affected existing structural, history and machine tests. |
| Consumer | Publish the exact Core coordinate to Shop. Its owner reruns the existing public witness with its explicitly selected rule and reports the result. Core does not edit or silently rebind that fixture. |

The first test set is bounded to these observations:

1. A permitted state replacement admits and preserves its predecessor history.
2. A forbidden Event replacement refuses with admission bytes unchanged.
3. An ordinary Event addition still admits; the restriction is on replacement,
   not an accidental ban on Event records.
4. Direct low-level admission cannot skip the rule or substitute a successful
   caller-authored check result. Replay rejects an invalid selected transition
   rather than trusting that result.
5. Full, incremental and reopened state, provenance and supersession agree.
6. Changing only the selected rule changes the verdict. Renaming neutral
   fixture types requires no Core code edit. These show data-driven execution,
   not a second independent implementation.
7. Missing/stale rule, profile, contract or base references refuse before
   append. Unknown role types refuse at binding; existing structural refusal
   controls remain active.

Freeze the encoding before choosing new test filenames or public symbols.
Expected Core owner surfaces are `machine.py` and `knowledge.py` under
`src/malleus/_contract_pipeline`, plus their existing tests in
`tests/contract_compiler/pareto`. Touch `population.py`, the public facade or
installed artifacts only if the frozen binding actually requires them.
Do not reserve or change unrelated consumer files.

## Dependency view and limits

This is a view of the existing admission role, not a competing DAG:

| Subject | Relation | Object |
|---|---|---|
| Transition guard | implements | Existing normative state-transition admission role |
| Verified transition view | derivedFrom | Exact KCS and owning verified history |
| Transition guard | consumes | Verified transition view and compiled type meaning |
| Admission profile | binds | Retained rule/program and adopter history-profile roles |
| Pure guard | produces | Deterministic pass or typed refusal |
| Owning fold | enforces | Selected rule before atomic persistence and during replay |
| Reference implementation | conformsTo | Frozen neutral admission and replay cases |

Pure retained-data guards can recompute during replay. External check receipts
remain attestations with their documented trust limits; replay does not prove
an external engine ran or source assertions are true. This slice must not
rerun external effects or engines, or silently strengthen old receipt claims.

Excluded: general history-model compiler, complete projection closure,
ontology policy annotations, automatic event-derived state, policy migration,
rewriting old histories, full Assent cutover, new ledger or accepted-graph
writer, mandatory Prolog, public plugin framework, packaging/version projects,
Shop implementation, paper changes and Re-entry integration. One consumer
does not justify shared domain vocabulary. Cross-language replaceability
still requires a deliberately different interpreter and is not claimed here.

Preparation is complete when this plan and its approval are journaled and the
existing ledger validates. Runtime completion requires RED/GREEN and the
bounded evidence above; preparation must never be reported as that result.
