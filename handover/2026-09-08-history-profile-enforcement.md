# Domain-history declarations and replacement enforcement

Status: the audit is complete. Luis accepted the revised admission design
below and requested journaling plus implementation preparation: "Correct, this
is better, add to journal and prepare to implement." The initial
replacement-specific recommendation remains superseded. Exact instruction
encoding and public names are not frozen; no runtime has been changed by this
work. The [implementation preparation](2026-09-08-transition-admission-plan.md)
separates that remaining design step from RED, GREEN and consumer evidence.

Runtime inspected: `a0026cbd25a90b5c2b6c9eb7b31df4e42df16804`, tree
`ca0ace8bf60f5a0519acd4c020f3728021f51c27`. The live checkout also contained
Shop source-answer work at `50b7df40e56674b6e5a6e17fbdfad25a39268eb8`;
the inspected Core source and selected Core tests were byte-identical to
`a0026cbd`. This is a current-source audit, not a rebind of Shop's released
v0.14.0 evidence.

## Question and classification

Shop asks whether one history can retain occurrences while permitting only
selected state types to be replaced. Its exact request and public witness are
in [CORE_REQUIREMENT.md](../research/ontology_driven_kg_realization/experiments/small_shop/connected_story/CORE_REQUIREMENT.md).

- The intended restriction and selection of state types are `ADOPTER_CHOICE`.
- An explicitly selected replacement restriction would be `OPTIONAL_PROFILE`.
- The existing compiler/history/check executors are `REFERENCE_IMPLEMENTATION`.
- The Shop witness is `CONFORMANCE_FIXTURE`, not a retail rule for Core.

The smallest observation is already available: keep the profile's state-only
correction label, propose replacing an Event and its participation, and observe
whether the real admission path refuses. Reuse the current profile parser,
structural bundle, required-check policy and atomic history. Exclude a profile
DSL, retail vocabulary in Python, automatic event-derived state, old-history
migration, Re-entry and packaging work.

## What the fields actually do

All profile fields participate in the profile's canonical identity and are
retained when population preparation selects the profile. That establishes
which declaration was used. It does not execute every declaration.

| Declaration | Current mechanical meaning |
|---|---|
| Grammar, closed root/nested shape, nonempty labels, identity | Parsed and validated by `DomainHistoryProfile.from_data`. A constructed profile must agree with its canonical bytes. |
| `semantic_unit` | Checked against the declared vocabulary. It does not select a state-transition interpreter or limit operation count/families. |
| `origin` and `genesis.boundary` | Checked against the declared origin vocabulary and its boundary mapping. All executable histories still start with an empty graph. The label does not prove snapshot completeness or recover an external origin. |
| `genesis.completeness_scope` | Required retained text, not a source-coverage check. |
| `ontology_roles.event` | Its being nonempty enables the Event family during population compilation. With the optional EventParticipation type in the contract, that family is enabled too. The role entries are not a type allowlist or resolved class references. |
| Other `ontology_roles` lists | Sorted unique nonempty strings where present, retained as declarations. In particular, `state` does not restrict replacement targets. |
| `change_semantics` | Closed map of nonempty strings. No dispatch on `correction`, `transition`, `addition` or `retraction` labels. Unsupported operation kinds still refuse under the separate KCS grammar. |
| `projection_rule_family` | Retained label. The current projector applies explicit operations and supersession; it does not execute an arbitrary projection family. |
| `time_semantics` | Retained declarations in the generic profile. The document adapter specifically requires the shipped capture-import-order declaration and emits `ORDER_ONLY(capture_id)`. That adapter guarantee is not a general profile-time interpreter for arbitrary plans or KCS values. |
| `grounding` | Required nonempty retained object here. This is not the separate knowledge-pack citation rite or a judgment of adequacy. |

Implementation: [profile parsing](../src/malleus/_contract_pipeline/population.py),
particularly `DomainHistoryProfile.from_data`, `_profile_roles` and
`compile_population_plan`; [document time production](../src/malleus/_contract_pipeline/document.py)
in `adapt_document_assertions`.

The family gate belongs to population compilation. The low-level history
receives a KCS and its selected machine/policy, not a DomainHistoryProfile
interpreter. Do not describe preparation-only checks as an unavoidable
low-level admission restriction.

## What replacement already enforces

Population compilation and history application enforce known structural
invariants: fresh historical IDs, an active prior target, one successor per
prior record, equal operation family and exact type, equal valid-time kind,
strictly later INSTANT time, and a valid resulting graph. Old records remain in
record history; replacement removes them only from the current projection.

See `KnowledgeChangeHistory._apply_change` in
[knowledge.py](../src/malleus/_contract_pipeline/knowledge.py). These rules do
not ask whether the replaced type was listed in `ontology_roles.state`.

The mixed Shop history is therefore describable today as explicit occurrence
records plus explicit state-version replacements in atomic changes. It is not
an event-driven state calculator, nor does its state-only correction label
prevent occurrence replacement.

## Existing policy route and the missing convenience

The public building blocks can require an adopter-supplied executed check:

1. `PolicyProgram` binds exact required check IDs/digests and outcome-to-verdict
   mappings. `compose_normative_profile` binds that policy and its machine.
2. An adopter executes its check on exact inputs and retains its receipt.
3. `KnowledgeChangeHistory.admit_with_anchors` commits the receipt anchors,
   change and protocol events atomically. A rejecting verdict prevents the
   admission batch from persisting. Earlier preparation is separate.

The [shipment-policy runner](../research/ontology_driven_kg_realization/experiments/small_shop/shipment_policy/README.md)
demonstrates this route with a real Prolog execution. It does not fabricate a
successful result. Its wrapper is explicitly insert-only Entity/Relation
research code, not a generic Core change-policy executor.

`PolicyProgram` checks required results and derives a verdict; it does not
execute a replacement rule. `GraphFactCompiler` accepts graph snapshots and
its fact contract has no KCS operation, supersession or prior/current-state
role predicates. `PrologVerifier.verify_candidate_subgraph` therefore is not
already a KCS transition checker. Projecting transition metadata into new
domain records merely to feed it would add a different representation.

`admit_structural_change` is intentionally fixed to the shipped structural
bundle. Its signature provides no additional rule or check executor. The
low-level route remains a trusted check-attestation boundary, not proof that
caller-authored outcomes were actually computed.

Conclusion: public primitives permit adopter-owned check orchestration, but
there is no supplied end-to-end Core executor for this replacement restriction.
Shop should not copy that ceremony or call a private preflight an admission
guarantee. A new Core seam requires a bounded contract decision.

## Initial recommendation, superseded by the vision review below

Add one identified, closed replacement-check artifact naming permitted
operation families and exact replacement types. Do not assign executable
meaning to arbitrary existing profile labels. Core evaluates it against the
exact KCS and verified prior record history; the selected admission policy
requires its computed result alongside existing structural validation.

Bind selection before changes are admitted. Reopen must retain the selected
rule and check/KCS association. The existing low-level trust boundary must stay
explicit; a convenience wrapper alone cannot be advertised as anti-forgery or
unavoidable replay enforcement. Exact replay enforcement and receipt semantics
must be selected in the contract before implementation, not inferred here.

Smallest prospective TDD proof: a neutral allowed-state replacement succeeds;
an Event replacement refuses; an unchanged Event may be added; a bypass of the
owning selected gate or a changed/stale rule/change binding refuses; refusal
preserves admission bytes; successful reopen preserves rule and record history.
Type matching should be exact for this cut, with no inferred subclass policy.
These are proposed tests, not tests run or an approval of Shop's final rule.
This audit establishes one consumer, not two. The maintainer promotion gate
therefore permits a Core-owned bounded reference experiment, not automatic
promotion into generic shared vocabulary or a general public policy API.

## Observed evidence

The exact public `core_contract_probe` command in the Shop request reproduced:
`ADMITTED`, with retained e7 superseded by `e7:replacement-probe`. Its unchanged
profile declared `EXPLICIT_SAME_TYPE_STATE_SUPERSESSION` and state type
`SupplierOrderState`.

A separate temporary diagnostic changed only `ontology_roles.event` in the
proposed profile to `["UndeclaredProbeEvent"]`, then called the same public
`run_probe`. Two changes admitted; e4 and e7 were queryable even though
`contract_view.has_type("UndeclaredProbeEvent")` was false. This confirms the
nonempty-list capability behavior, not an approved new profile or a claim that
role labels already promise class resolution.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. .venv/bin/python -m pytest -q -p no:cacheprovider tests/contract_compiler/pareto/test_domain_history_profile.py tests/contract_compiler/pareto/test_public_compiler.py research/ontology_driven_kg_realization/experiments/small_shop/connected_story/test_history_probe.py research/ontology_driven_kg_realization/experiments/small_shop/shipment_policy/test_shipment_policy.py
```

Result: **33 passed**. No tests were weakened or added. This was classification
and reproduction, not a behavioral RED/GREEN cycle, full suite or release gate.
The audit does not select final Shop semantics or authorize a new runtime API.

## Vision review: complete the admission contract, not a replacement subsystem

Status: revised design direction accepted by Luis after rereading the original
vision and maintainer skill. Preparation is authorized; the exact executable
contract must be settled before runtime implementation. The factual audit
above and its historical evidence are unchanged.

### Sources and design correction

The original README at `c67d3c84` (2026-04-12) describes one domain definition
propagating through validators, typed graphs and rules, so those layers cannot
quietly disagree. The initial principles at `9a1d7458` (2026-08-14) put the gate
on commitment, distinguish representation from execution and governance, and
require an identified judge. Those historical documents also contain stronger
claims that later status documents qualify; they are design lineage, not
evidence of today's capabilities.

The current [principles](../docs/PRINCIPLES.md) and reloaded
[maintainer skill](../.claude/skills/malleus-dev/SKILL.md) place operational
meaning in identified programs. The
[foundation design, section 4.2](../design/PROTOCOL_FOUNDATION_GRAPH.md)
already assigns stateful write rules to `NormativeAdmissionProfile`, with an
`AdmissionRuleSet` in its `ProtocolMachineProgram`. Domain-history semantics
and projection closure remain separate under
[the accepted history-profile design](../design/KNOWLEDGE_PACKS.md).

My initial suggestion started with a replacement-specific artifact. That is a
possible encoding of one rule, not the missing architectural boundary. It
also risked duplicating the role/type selection already declared by the
adopter. The narrower architectural repair is to connect the existing owning
admission program to verified transition inputs and explicit rule data.

### Ownership and connection

| Existing role | Responsibility in the proposed cut |
|---|---|
| Domain ontology and compiled contract | Define record types, fields, inheritance and reference meaning. They do not decide whether a particular historical record may be replaced. |
| Adopter's domain-history profile | Define what a change means and which domain types play which roles. Keep one authoritative role/type mapping. |
| Normative admission profile and machine | Bind the exact selected history interpretation and require its executable transition guards before acceptance. A label alone is not a guard. |
| Check and policy artifacts | Define the predicate, its typed inputs and result, and any outcome-to-control decision. Keep domain choices in these artifacts, not Python branches. |
| Owning history and projector | Supply verified inputs, enforce the selected gate, commit atomically and derive accepted views. The projector does not invent a replacement policy or revise a past decision. |

Selecting a history interpretation must resolve its operational requirements
to supported checks/programs before accepting changes. Descriptive material
may remain retained, but an unresolved required rule must refuse, not become
an advisory string. No existing profile's free text gains new meaning
retroactively. This is an explicit new selection, not silent reinterpretation
of old histories.

### Smallest missing input

Expose a read-only, deterministic transition input to the selected check:
the exact KCS, verified prior records it replaces or references, compiled
contract, selected history-profile identity, and full base coordinates.
Derive it from the owning history, never from a caller's claimed prior types.
It is a view of existing authoritative data, not another ledger, graph,
proposal identity or compulsory persisted artifact.

For the present rule, that view needs replacement operations and their prior
record metadata. It does not need a full copied graph. A future rule needing a
candidate graph must declare that input rather than silently borrowing it.

The Shop rule can then mean: for each explicit replacement, the replaced and
replacement types must satisfy the selected state-role constraint. Shop owns
that choice; Core owns type resolution, collection traversal, comparison and
typed refusal. Exact-type versus subtype matching must be explicit in the
rule, not guessed from a name. Renaming all Shop classes must not require a
Core code edit. Allowing or forbidding a replacement must change the selected
rule identity, not the interpreter's domain-specific branches.

### Reuse and the actual implementation gap

Reuse the existing machine/policy identities, KCS, retained artifacts, atomic
append and replay. Express the guard using the selected machine's bounded
typed operations or an explicitly declared pure capability. Do not add a
replacement service, general rule-language frontend or arbitrary callback.

This is not already callable: the current `compose_normative_profile` refuses
nonempty capability references, and its machine executor receives protocol
records rather than a verified KCS transition view. The separate finite action
interpreter has comparison and membership operations, but attaching an action
program does not gate KCS admission. Its implementation may inform reuse; it
must not become a second admission authority. The existing Prolog checker is
graph-oriented and should not be extended into a new transition framework
merely because this one rule needs membership and type checks.

Two checking modes must stay distinct. A pure, deterministic admission guard
over retained data can run both before append and during replay using the same
selected interpretation. An external source assessment or engine execution
may instead be a retained attestation with explicit trust limits; replaying
its receipt does not prove that external computation occurred. The proposed
replacement constraint belongs to the first category. Do not make all checks
rerun external engines during replay, or accept a caller's successful receipt
as a substitute for this pure guard.

The owning KCS fold must invoke the selected guard, so a caller cannot bypass
it by skipping population preparation or a convenience helper. This means
protocol validation of inputs, not protection against arbitrary filesystem
rewriting. Historical hashes and integrity guarantees remain as documented.

### Dependency sequence and TDD boundary

1. Freeze the transition input and the binding from the existing admission
   profile to one pure guard. Resolve exact profile/type references and state
   unsupported cases. Choose the smallest existing instruction/capability
   extension; no public names or new wire are selected by this design note.
2. Write REDs through the owning history: allowed replacement; forbidden
   replacement; ordinary addition unaffected; missing or stale rule binding;
   direct low-level admission cannot skip the rule; refusal preserves bytes;
   successful full and incremental replay agree. Change only the selected
   rule to prove it controls the verdict, and rename fixture types to expose
   domain-specific branches.
3. Implement the bounded Core reference path, then have Shop consume it in
   its existing witness. Retain the current structural-only path as an
   explicitly different selection, never a fallback for the restricted one.

No general history-model compiler, complete projection closure, new state
authority, ontology policy annotation, mandatory Prolog dependency for this
guard, policy migration, full Assent cutover, or second-implementation claim.
This completes a slice of an already accepted admission role. Shop remains
one consumer, and does not justify promoting its vocabulary or claiming a
general policy platform.
