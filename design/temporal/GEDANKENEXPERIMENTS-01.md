# Thought experiments before the temporal architecture decision

24 September 2026. Author requested broader worked experiments before choosing
the path. Neither the representation recommendation nor a storage backend is
approved. Core implementation remains paused.

## Objective and evidence level

Test whether one proposed approach can preserve scientific interpretation,
computational premises, temporal history and knowledge revision together, without
making each consumer invent a different meaning of change.

This is an OPTIONAL_PROFILE design investigation, with proposed
CONFORMANCE_FIXTURE cases. It adds no PROTOCOL_INVARIANT. Domain interpretations,
authority, persistence rules and model selection remain ADOPTER_CHOICE. No
generic implementation is promoted from a single specimen.

Four evidence levels must stay separate:

1. **Inspected existing result:** read another task's report and retained outputs.
   Its historical test count is not a fresh execution here.
2. **Worked trace:** specify inputs, intermediate state, exact questions and
   forbidden answers. This can expose an inconsistent design before code.
3. **Storage witness:** execute encode, query, decode and rebuild against an
   independently authored answer key. This proves only the selected cases.
4. **Core integration:** admission, actual required checks, replay and consumers
   pass together. Neither a worked trace nor a storage witness establishes this.

This pass supplies levels 1 and 2, plus the storage construction in
[STORAGE-FLOWS-01.md](STORAGE-FLOWS-01.md). New storage witnesses and integrated
temporal runs remain pending. The coverage is the named flows below, not all
possible future Malleus uses.

## Existing evidence inspected, not restarted

| Flow | Concrete existing evidence | Boundary relevant to this design |
|---|---|---|
| Marine reading | Retained reading blocks page:2:block:006 and page:5:block:006; paper marine-transfer-01 result and arithmetic witnesses | The graph reader's hard-bound inference was unsupported. Representation, reasoning and retrieval are distinct questions. |
| UMR whole clause | UMR MAIN-CLAUSE-RESULTS-04 and QUANTITY-FRAME-RESULTS-03 | Qualified linguistic structure and statistical roles survive the local bridge. Same-history scientific refinement and embedded temporal interpretation remain open. |
| Computation contexts | Computational RESULTS-03 and saved context artifacts | Original, hypothetical and corrected inputs/results are distinct; no general domain-time selection demonstrated. |
| Calculation revision | Computational RESULTS-04 and saved model-change checkpoints | Model storage, model selection, execution and result admission are distinct. The old calculation remains available. |
| Model-produced calculation | Computational RESULTS-05 | One acquired synthetic computation worked within supplied vocabulary after correction. No general ontology discovery or acquired-update guarantee. |
| Knowledge maintenance | KG re-entry RESULTS-01, coverage and history | An authored review changes only an assessment and its relation; full downstream impact discovery is not demonstrated. |
| Temporal Core | Local BASELINE-01 and RESULTS-01 | Exact historical prefix read is locally implemented; compiler-history bitemporal correction/selection remains pending. Assent has separate temporal mechanisms. |

Exact inspected paths and byte identities are in [flow-evidence-01.json](flow-evidence-01.json).
The consumer paths are read-only inspection inputs, not newly selected runtimes
or dependencies to import into Core. No paper or consumer file is modified.

## One common trace, without pretending every step is automatic

At each evidence boundary, work through these questions in order:

| Stage | Required account of what happens | What does not follow automatically |
|---|---|---|
| Source retention | Exact source and location remain identifiable | Arrival is not accepted interpretation |
| Interpretation proposal | State what the source reports, its qualifications, prior knowledge used and open issues | An LLM proposal is not evidence of its own truth |
| Representation check | Existing ontology can express the distinction, or a precise gap/revision proposal is needed | A new class does not populate facts |
| Review and admission | Review required items; bind the actual proposed changes; Core runs selected checks | Review completion is not resolution; checks do not prove arbitrary scientific meaning |
| Graph reconstruction | Keep original assertions, interpretation versions, links, contexts and accepted changes | Old records are not simultaneously applicable world states |
| Query or computation preparation | Declare exact premises, relevant times, context and model | A scalar answer does not permit discarding qualifications |
| Update/reconsideration | Follow declared dependencies and review the bounded affected set | Reachability is not a proof that a conclusion is false |

Names in these tables are design responsibilities, not newly shipped APIs.
Core can make structural selection and declared dependency traversal deterministic.
Discovering a previously unmodelled scientific connection still needs an
interpreter and evidence. A missing dependency must remain visible as a limit.

## GE-01. Marine estimate, application and later understanding

**Origin:** real article passage plus an explicitly synthetic later clarification.
The real passage reports western-flank crustal thickness, cites refraction work
and uses that estimate when discussing earthquakes beneath RC2. It does not give
permission to invent a hard physical bound or a measurement date.

**Worked trace:**

1. Retain the original block. Represent the attributed estimate E1 with its
   subject, scope, value/unit and unresolved statistical interpretation. An
   annotation may use UMR roles, but it remains an annotation of a statement.
2. Represent the reported application A1 of E1 to the RC2 interpretation. Do not
   create a second independent measurement or substitute RC2 for E1's origin.
3. Keep our interpretation I1 and application assessment J1 distinct from what
   the source said. Record a local citation pointer, not a claim to have read
   the cited publication.
4. Introduce a synthetic clarification that explicitly defines the uncertainty
   for this exact estimate. Review whether it genuinely applies to E1. Only
   then propose I2, with its extra source and connection, preserving I1.
5. The new knowledge position knows more about the statistic; it does not imply
   that crust thickness physically changed when the clarification was read.

**Required queries:** under the old position, uncertainty kind remains unresolved;
under the new position, return the accepted interpretation and its evidence.
Both still identify the same source estimate and its separate application.
Even an explicit standard deviation does not establish a guaranteed maximum.

**Ontology effect:** add vocabulary only if the distinction is absent. Otherwise
this is new interpretation content, not ontology growth. **Storage obligation:**
preserve E1, I1, I2 and their evidence links with stable addresses.

**Counterexample:** a single property updated from UNKNOWN to SD loses the old
interpretation unless the property's exact versions and qualifiers are exposed.
A new node without its parent proposition preserves a number but loses meaning.

**Still unproved:** model-produced interpretation, actual scientific transfer,
and the same-history UMR update. The synthetic clarification is not a new fact
about the article or its cited study.

## GE-02. Conditional saturation statement versus executable model

**Origin:** real reading page:5:block:006. It relates melt composition, pressure,
temperature, approximate depth and a cited solubility model in a conditional
saturation statement. The statement is not a table of independent measurements.

**Worked trace:** retain one qualified proposition with its conditions and model
reference. A question about what the article proposes can retrieve that whole
conditional account. A request to calculate saturation for new inputs must name
an actual executable model, implementation, units, parameter mapping and scope.
The cited model name alone is not that execution contract.

Add a synthetic executable model later. Storing it does not replace the source
claim or activate it. Prepare and execute only an explicitly selected model with
compatible inputs; separately admit its result and execution evidence.

**Required answers:** source claim available before execution; calculation not
available until its prerequisites and actual execution exist. Approximate depth
must not become an exact pressure-to-depth law. Temperature, pressure and
composition from unrelated contexts must not be combined.

**Storage obligation:** scope the conjunction and the exact model graph. Native
temporal scalar properties alone do not preserve which conditions belong together.
An identified proposition, application or assertion graph must carry that grouping.

**Still unproved:** marine prose-to-executable-model mapping. The order experiment
is evidence of a bounded computation path, not of this scientific calculation.

## GE-03. An application is challenged, not erased

**Origin:** existing synthetic KG re-entry example, extended with an authored
dependent argument. Preserve its existing frozen evidence.

Start with E1, source-reported application A1, assessment J1 and an argument D1
whose declared premises include J1. A new synthetic passage challenges the
application assumption. Review E1, A1, J1, D1, citation and an unrelated record.
Accept only the justified J2 assessment and required linking changes.

**Required state:** E1 and the fact that the source reported A1 remain. The old
J1 remains inspectable. D1 is flagged for reconsideration, not silently rewritten
or declared false. The unrelated record is unchanged.

Add a second authored justification D2 for the same conclusion. Weakening D1
does not remove D2. Whether D2 is sufficient is a declared reasoning/review
question, not a generic delete-every-descendant operation. Unknown dependencies
prevent a claim that every consequence was considered.

**Storage obligation:** different justifications and premise sets must be
individually identifiable. A bare SUPPORTS edge is insufficient if it hides the
conditions or alternative derivations being assessed.

**Deterministic portion:** enumerate registered exact uses; detect stale reviews;
enforce the permitted proposal footprint. **Interpretive portion:** whether new
evidence defeats a justification and whether another remains adequate.

**Existing versus missing:** the existing workflow exercised the assessment
replacement, not D1/D2 reasoning or automatic discovery. Its current graph drops
the replaced assessment while history retains it. Our intended full-version KG
must expose both without confusing their applicability.

## GE-04. Report, assumption and correction give different premises

**Origin:** existing synthetic order computation, not a product price timeline.
Line A has three items at EUR 12; B has two at EUR 7.50. The original amount is
EUR 51. A hypothetical B price of EUR 8 gives EUR 52. A separate correction of
the order's reported B price also gives EUR 52 only after its own execution.

**Worked trace:** retain input assertion B1, assumption H1 and correction B2 as
distinct records. Each calculation context binds exact inputs and the same
model M1. Accepting B2 does not turn H1's execution into a reported result.
Before new execution, the corrected-context answer is not computed. After
execution/admission it is EUR 52 with distinct provenance. B1's EUR 51 remains.

**Critical scope:** an order-line quote is not the product's globally applicable
price. Do not import the dates from GE-06 into this example. A computation using
an exact selected quote need not invent a domain date. A question asking what
price applied on a date has a different prerequisite.

**Storage discriminator:** equal value and equal time coordinates cannot be the
sole identity key. Basis, subject/scope, context and exact assertion remain
addressable. Both storage candidates must preserve equal-valued distinct claims.

**Observed predecessor:** saved results establish this research consumer's
behaviour. They do not establish a generic temporal Core computation API.

## GE-05. The calculation itself changes

**Origin:** existing model-change specimen and saved checkpoints.

M1 returns EUR 52 excluding delivery under corrected inputs. M2 adds a separately
reported EUR 3 delivery charge, yielding EUR 55 including delivery and excluding
tax. Shared RDF terms do not permit merging the two model definitions.

**Required sequence:** storing M2 leaves M1 selected and EUR 52 available.
Selecting M2 yields not computed. External execution alone still yields no
accepted answer. Admitting its result makes EUR 55 available for that context.
M1, earlier contexts and their old answers remain readable.

**Temporal extension to test:** if an adopter later declares that a model is
applicable only during a given period, selection must check that period and its
knowledge position. Merely accepting M2 later supplies neither that period nor
permission to relabel M1 results. A formula used historically stays tied to its
exact model, input selection and execution implementation.

**Storage obligation:** exact statement-set or graph identity per model, shared
immutable terms, separate selection and execution records. New ontology vocabulary
can be additive; storing new model data is not necessarily another schema change.

## GE-06. World transition, retrospective correction and old reads

Reuse NEXT-STAGE.md's independently authored price expectations. Here the subject
really is a dated price account, unlike the order quote in GE-04.

| Position | Accepted input | Account of 5 May | Account of 15 May |
|---|---|---|---|
| K1 | 750 from 1 May, open end explicitly part of this account | 750 | 750 under that then-open account |
| K2 | Actual transition to 800 on 12 May | 750 | 800 |
| K3 | Correction to 775 for 1 May to 12 May | 775 | 800 |

All reports and applicability versions remain queryable. At K1, neither later
closure is visible. An execution made at K1 still reaches its original premise.
Correcting the past does not change the later 800 period or mean the world changed
at K3. Start-included/end-excluded boundaries must be tested exactly.

**Storage obligation:** derive historical applicability from accepted changes,
or prove an equivalent indexed view. Filtering final values is insufficient if
the response leaks future closure metadata. Core, not the producer, maintains
derived knowledge-period ends. This does not yet specify arbitrary splitting.

## GE-07. Events, persistence, plans and uncertain clocks

The earlier T-LATE-REPORT example is under-specified: learning that a valve
opened on 3 June does not alone justify OPEN on 4 June. T-UNCERTAIN-TRANSITION
similarly assumes persistence after opening. Keep the old fixtures unchanged
as evidence; do not promote those expected answers without resolving the premise.

Run three deliberately distinct controls:

1. **Event only:** a timestamped opening is reported late. Before acceptance,
   no accepted report; afterwards, the historical event is retrievable. State
   on the next day remains unknown without more evidence or a persistence rule.
2. **Declared state rule:** under a selected rule and explicit completeness
   assumptions, opening starts an open interval and closing ends it. Late closing
   evidence revises the known interval, preserving the earlier account. No
   claim that absence of a recorded closing proves none occurred in reality.
3. **Planned action:** a command or intention to open a valve is retained.
   Without an observation or separately justified state inference, it does not
   establish opening. This is also the robotics/simulation boundary.

The Shop analogue is equally important: correcting the ordered quantity from
one to two does not assert that another item was delivered. Ordering, shipment
and receipt need their own propositions, evidence and domain times. The existing
synthetic order computation is not a substitute for that Core-owned Shop test.

For uncertain event time, retain the interval of possible transition times,
not a duration for which the valve necessarily transitions. Queries inside it
may be indeterminate. Simulator step, sensor time, observation receipt and ledger
acceptance are different coordinates. Episode IDs and clock mappings must be
explicit; a reset clock cannot collide with another episode or become UTC by guess.

**Storage obligation:** uncertainty kind, coordinate system and persistence
semantics survive export. An ordinary exact interval datatype is not enough.
Assent's existing precision support is a reuse candidate, not evidence that the
compiler/history integration or simulator case already works.

## GE-08. Ontology growth and rule changes

Begin with a graph unable to represent an estimate's application role. Record
the exact missing distinction, propose an additive ontology revision, and admit
the new application only under the resulting contract. Earlier knowledge reads
must still retrieve the old contract and the old unresolved gap.

Changing the interpretation is not the same as adding vocabulary. Reclassifying
a bibliography record cannot silently change the meaning of every old reference.
If the supported revision policy cannot express a requested change, retain that
limitation and specify the missing operation instead of assuming migration.

For checks, distinguish a source claim about a rule, a stored rule definition,
an activated required check and an actual check execution. Changing a policy now
does not rewrite the verdict or rule under which an old change was accepted.
Existing ontology-only check re-binding is not arbitrary policy migration.

**Storage obligation:** every accepted application and execution can recover its
actual contract/check identities. Temporal table versioning does not provide
this by itself. The new temporal representation must define how current-state
rules see a selected view and historical rules see qualified versions.

## GE-09. Competing accounts at the same times

Two independent reports disagree about a quantity for the same subject and
period. Both reports can be retained as reports without endorsing both quantities
as one physical state. Neither arrival order nor larger confidence supplied by
a producer automatically selects an authority.

**Required queries:** source-scoped requests return their respective accounts;
an unqualified request that requires one value reports ambiguity. A hypothetical
account stays separate even when its value matches a report. A later accepted
assessment can choose an account for a named use without erasing the others.

**Storage discriminator:** a temporal property keyed only by subject/property
and two times is insufficient for these inputs. It needs assertion/account
identity or a richer value structure. This is not impossibility for native
temporal storage; it identifies what its mapping must preserve. Explicit nodes
with an unqualified union query fail just as badly.

## GE-10. Withdrawal, pruning and rebuilding

Distinguish withdrawing an interpretation for current use, hiding it in a compact
view, discarding a derived cache and destroying retained evidence. They have
different consequences.

A synthetic withdrawal must leave the old claim and its former uses explainable.
If the selected Core policy cannot encode withdrawal yet, the experiment must
say so. The storage mapping still has to show where such a future accepted
withdrawal and its scope could be represented without overwriting the original.

A cache may be rebuilt only from retained closure. Deleting authoritative source,
contract or model bytes needed by an old result breaks that reconstruction.
Retention-law or privacy-driven erasure is a separate policy decision; this
design cannot promise both deletion and exact reconstruction of the deleted data.

**Required query:** old explanation still available after current-view hiding;
after a deliberately missing required artifact, explicit incomplete/refused
reconstruction, never a silently simplified explanation.

## GE-11. Evidence arrives during a calculation or review

An execution starts from K1. Before its result is submitted, K2 accepts a relevant
correction. The result may be a faithful record of the old invocation, but it
cannot silently become the current-context answer. Current Core stale-base
checks remain in force. Any later proposal to retain that execution as historical
evidence must bind the current admission base and explicitly preserve its old
execution context; this pass adds no such admission shortcut.

Repeat with unrelated evidence only. The earlier calculation's exact input
meaning may be unchanged while its proposed admission is stale. Keep semantic
dependency validity separate from concurrency safety. Do not weaken the latter
to make a cache appear reusable. A fresh review also needs its current declared
boundary, not merely the same prose as last time.

**Storage obligation:** exact ledger checkpoints, actual premise dependencies,
and execution/read snapshots. No clock timestamp substitutes for a content-bound
history position. No second database writer may independently accept the result.

## GE-12. Heterogeneous content and the size of a unit of knowledge

A coherent proposition can span blocks; a block can contain multiple propositions
and publication metadata. Keep original evidence, group interpreted meaning and
define classification separately. Captions and tables are eligible evidence,
not blanket exclusions. Their interpretation may require neighbouring context.

A dense measurement array or an executable model need not become one node per
byte or scalar. The graph can identify an exact retained artifact and its role,
while exposing the quantities/relations needed by the use. Formula/model scope,
array shape, units, locators and decoder identity must not disappear.

**Required query:** distinguish represented graph content, retained-only content
and unrepresented meaning. A missing graph relation cannot be silently supplied
by a reader and called graph retrieval. Conversely, retaining a source artifact
is useful without claiming every fact in it is queryable.

**Storage discriminator:** round-trip typed literals, exact record/graph IDs,
edge direction, scope and evidence addresses. Merely putting an opaque JSON/PDF
blob in every candidate store proves byte storage, not usable representation.

## What these traces already change

The proposed path remains plausible, but two clocks and version identities are
not sufficient. The next candidate must also account for assertion scope, context,
coherent premise groups, derivations, uncertainty and rule-governed persistence.
These need not be six new engines or six mandatory fields on every number.

The small selector must have two legitimate modes: inspect a qualified account
without claiming date applicability, or answer an applicability question with
the required time/context evidence. Keeping NONE_STATED must not disable the
first mode. A full-history graph and a selected-state view need different input
contracts for checks.

The event-persistence premise and date-free quote case are concrete amendments
to the proposed test programme, not runtime regressions or approved policies.
The previous architecture recommendation remains a candidate until the following
experiment sequence distinguishes it from alternatives.

## Sequence and decision gates

| Stage | Deliverable | What it can establish |
|---|---|---|
| G0, this pass | Named flows, source bindings, worked traces, counterexamples and storage mappings | Design consistency and explicit unknowns; no new runtime result |
| G1 | Small independently authored specimen per distinct obligation; exact expected reads and refusals | Agreed meaning before implementation; persistence and authority choices stay visible |
| G2 | The same specimens in ordinary graph records and an independent relational projection; assess a native temporal mapping separately | Lossless representation, actual queries and rebuild on those cases; not Core integration or general performance |
| G3 | Bounded Core composition using already shipped mechanisms, exposing exact remaining limitations | Reuse evidence and minimal Core requests rather than consumer substitutes |
| G4 | Compare alternatives against failures, change surface and measured workloads; author selects the cut | Informed representation, storage and profile decision |
| G5 | Exact approved contract, RED then GREEN and consumer regression checks | Implementation evidence only for the selected semantics |

Do not implement all future features merely because their storage representation
is possible. Existing read-only witnesses may be rerun during preparation; no
paid model, new active policy, schema migration, shared-tree mutation or runtime
selection is implied. No native database is selected by listing it in G2.

## Literature constraints, not automatic adoption

- [de Kleer's ATMS](https://www.dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf),
  introduction and sections 1.1 to 1.2, separates inference from maintenance of
  justifications and assumption contexts. It motivates GE-03/09. It does not
  supply Malleus admission, scientific interpretation or a selected rule engine.
- [Kowalski and Sergot's event calculus](https://www.doc.ic.ac.uk/~rak/papers/event%20calculus.pdf)
  is relevant prior work for event/state reasoning. No calculus or default
  persistence axiom is adopted here. The GE-07 counterexample is independently
  visible from its under-specified input.
- [PROV-O](https://www.w3.org/TR/prov-o/) distinguishes qualified uses, generation
  and revision. These are provenance roles, not automatic correction authority,
  temporal eligibility or a proof that an executor behaved honestly.
- [RDF dataset concepts](https://www.w3.org/TR/rdf11-concepts/#section-dataset)
  provides named graph grouping, but the graph name does not itself define the
  group's epistemic or temporal meaning. GE-02/05 need an explicit scope convention.

New sources and the bounded transfer are retained in the private Recon project.
No historical experiment result or declared Core capability is rewritten here.
